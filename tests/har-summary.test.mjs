import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, readFile, rm, open } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { summarizeHar, parseArgs, MAX_BYTES, MAX_ENTRIES } from '../skills/reverse-api-investigation/scripts/har-summary.mjs';

const script = fileURLToPath(new URL('../skills/reverse-api-investigation/scripts/har-summary.mjs', import.meta.url));
const marker = 'SYNTHETIC_PRIVATE_CANARY';
function entry(url = `https://private-${marker}.example.test/users/${marker}?token=${marker}#${marker}`) {
  return {
    startedDateTime: marker, serverIPAddress: marker, _custom: marker,
    request: { method: 'GET', url, headers: [{ name: 'Authorization', value: marker }], cookies: [{ name: 'session', value: marker }], postData: { text: marker }, queryString: [{ name: marker, value: marker }] },
    response: { status: 200, headers: [{ name: 'Set-Cookie', value: marker }], cookies: [{ value: marker }], content: { mimeType: 'application/json; charset=utf-8', text: marker, encoding: 'base64' }, _secret: marker },
  };
}
const har = entries => ({ log: { creator: { name: marker }, pages: [{ title: marker }], entries } });

async function temp(t) {
  const dir = await mkdtemp(path.join(tmpdir(), 'pi-toolbox-har-'));
  t.after(() => rm(dir, { recursive: true, force: true }));
  return dir;
}
function cli(args) { return spawnSync(process.execPath, [script, ...args], { encoding: 'utf8', timeout: 10000 }); }

test('default report omits all raw identifiers, queries, headers, cookies, bodies and HAR extensions', () => {
  const input = har([entry()]);
  const before = JSON.stringify(input);
  const result = summarizeHar(input);
  const json = JSON.stringify(result);
  assert.equal(result.mode, 'structure-only');
  assert.equal(result.reviewRequired, true);
  assert.equal(result.hostCount, 1);
  assert.equal(result.endpoints[0].pathDepth, 2);
  assert.equal(result.endpoints[0].responseTypes['application/json'], 1);
  for (const forbidden of [marker, 'private-', 'example.test', 'Authorization', 'Set-Cookie', 'users/', 'utf-8']) assert.ok(!json.includes(forbidden), forbidden);
  assert.equal(JSON.stringify(input), before);
});

test('route preview is explicit, labeled unsafe, and excludes query and fragment', () => {
  const result = summarizeHar(har([entry('https://api.example.test/users/customer123?secret=fixture-token#fragment')]), { includeRoutes: true });
  assert.equal(result.mode, 'route-preview-not-sanitized');
  assert.equal(result.endpoints[0].route, 'https://api.example.test/users/customer123');
  assert.ok(!JSON.stringify(result).includes('fixture-token'));
  assert.ok(!JSON.stringify(result).includes('fragment'));
  assert.equal(result.reviewRequired, true);
});

test('query variants aggregate without their values; methods and origins remain distinct', () => {
  const a = entry('https://api.example.test/items?page=1');
  const b = entry('https://api.example.test/items?page=2&limit=5'); b.response.status = 429;
  const c = entry('https://api.example.test/items'); c.request.method = 'POST';
  const d = entry('https://other.example.test/items');
  const result = summarizeHar(har([a, b, c, d]));
  assert.equal(result.hostCount, 2);
  assert.equal(result.endpoints.length, 3);
  assert.equal(result.endpoints[0].requests, 2);
  assert.equal(result.endpoints[0].maxQueryParameterCount, 2);
  assert.deepEqual(result.endpoints[0].statuses, { 200: 1, 429: 1 });
});

test('malformed, non-HTTP and credential-bearing URLs are skipped without echoing them', () => {
  const result = summarizeHar(har([entry('not a URL'), entry('file:///private'), entry(`https://user:${marker}@example.test/api`), null, entry('https://api.example.test/')]), { includeRoutes: true });
  assert.equal(result.skippedEntries, 4);
  assert.equal(result.endpoints.length, 1);
  assert.ok(!JSON.stringify(result).includes(marker));
});

test('untrusted methods, MIME values and statuses cannot escape through dynamic keys', () => {
  const e = entry(); e.request.method = marker; e.response.status = marker; e.response.content.mimeType = marker;
  const result = summarizeHar(har([e]));
  assert.equal(result.endpoints[0].method, 'OTHER');
  assert.deepEqual(result.endpoints[0].statuses, { unknown: 1 });
  assert.deepEqual(result.endpoints[0].responseTypes, { other: 1 });
  assert.ok(!JSON.stringify(result).includes(marker));
});

test('empty captures are supported but invalid structures and oversized entry arrays fail closed', () => {
  assert.equal(summarizeHar(har([])).endpoints.length, 0);
  for (const input of [null, [], {}, { log: {} }, { log: { entries: {} } }]) assert.throws(() => summarizeHar(input));
  assert.throws(() => summarizeHar(har(Array(MAX_ENTRIES + 1).fill(null))), /limit/);
});

test('CLI preserves source bytes and exclusively creates a private summary', async t => {
  const dir = await temp(t), input = path.join(dir, 'input.har'), output = path.join(dir, 'summary.json');
  const original = '\uFEFF' + JSON.stringify(har([entry()]));
  await writeFile(input, original);
  const result = cli([input, '--out', output]);
  assert.equal(result.status, 0, result.stderr);
  const summary = JSON.parse(await readFile(output, 'utf8'));
  assert.match(summary.sourceSha256, /^[a-f0-9]{64}$/);
  assert.ok(!JSON.stringify(summary).includes(marker));
  assert.ok(!JSON.stringify(summary).includes(dir));
  assert.equal(await readFile(input, 'utf8'), original);
  const retry = cli([input, '--out', output]);
  assert.equal(retry.status, 1);
  assert.match(retry.stderr, /EEXIST/);
  assert.deepEqual(JSON.parse(await readFile(output, 'utf8')), summary);
  const overwrite = cli([input, '--out', input]);
  assert.equal(overwrite.status, 1);
  assert.equal(await readFile(input, 'utf8'), original);
});

test('CLI route preview warns on stderr; stdout still contains valid JSON', async t => {
  const dir = await temp(t), input = path.join(dir, 'input.har');
  await writeFile(input, JSON.stringify(har([entry('https://api.example.test/items')])));
  const result = cli([input, '--include-routes']);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stderr, /WARNING/);
  assert.equal(JSON.parse(result.stdout).endpoints[0].route, 'https://api.example.test/items');
});

test('CLI fails on invalid JSON without printing input or file paths', async t => {
  const dir = await temp(t), input = path.join(dir, 'input.har');
  await writeFile(input, `{${marker}`);
  const result = cli([input]);
  assert.equal(result.status, 1);
  assert.ok(!result.stderr.includes(marker));
  assert.ok(!result.stderr.includes(dir));
  assert.equal(result.stdout, '');
  const missing = cli([path.join(dir, 'missing.har')]);
  assert.equal(missing.status, 1);
  assert.ok(!missing.stderr.includes(dir));
});

test('CLI rejects oversized files before parsing and writes no output', async t => {
  const dir = await temp(t), input = path.join(dir, 'large.har'), output = path.join(dir, 'out.json');
  const handle = await open(input, 'w'); await handle.truncate(MAX_BYTES + 1); await handle.close();
  const result = cli([input, '--out', output]);
  assert.equal(result.status, 1);
  assert.match(result.stderr, /25 MiB/);
  await assert.rejects(readFile(output), { code: 'ENOENT' });
});

test('argument parser rejects missing paths, extra positional input, and unknown flags', () => {
  assert.deepEqual(parseArgs(['in.har', '--out', 'out.json', '--include-routes']), { input: 'in.har', output: 'out.json', includeRoutes: true });
  for (const args of [[], ['--out'], ['x', 'y'], ['x', '--unknown'], ['x', '--out', '--include-routes'], ['x', '--out', 'a', '--out', 'b']]) assert.throws(() => parseArgs(args));
});
