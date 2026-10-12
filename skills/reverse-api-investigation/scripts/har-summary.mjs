#!/usr/bin/env node
// Offline structural minimization, NOT a sanitizer or a replay client.
import { open } from 'node:fs/promises';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';

export const MAX_BYTES = 25 * 1024 * 1024;
export const MAX_ENTRIES = 50_000;
const METHODS = new Set(['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'CONNECT', 'TRACE']);
const MIMES = new Set(['application/json', 'application/xml', 'text/html', 'text/plain', 'text/css', 'text/javascript', 'application/javascript', 'application/octet-stream', 'application/pdf', 'image/png', 'image/jpeg', 'image/webp', 'multipart/form-data', 'application/x-www-form-urlencoded']);

export function summarizeHar(har, { includeRoutes = false } = {}) {
  if (!har || !Array.isArray(har.log?.entries)) throw new Error('Invalid HAR: log.entries must be an array.');
  if (har.log.entries.length > MAX_ENTRIES) throw new Error('HAR exceeds the 50000-entry limit. Split it locally first.');
  const hosts = new Map();
  const endpoints = new Map();
  let skipped = 0;
  for (const entry of har.log.entries) {
    let url;
    try {
      if (typeof entry?.request?.url !== 'string' || entry.request.url.length > 8192) throw new Error();
      url = new URL(entry.request.url);
      if (!['https:', 'http:'].includes(url.protocol) || url.username || url.password) throw new Error();
    } catch { skipped++; continue; }
    const method = METHODS.has(entry.request.method) ? entry.request.method : 'OTHER';
    if (!hosts.has(url.origin)) hosts.set(url.origin, `host_${hosts.size + 1}`);
    // Query values are deliberately not part of an endpoint identity.
    const key = JSON.stringify([method, url.origin, url.pathname]);
    if (!endpoints.has(key)) {
      const item = {
        id: `endpoint_${endpoints.size + 1}`, host: hosts.get(url.origin), method,
        pathDepth: url.pathname.split('/').filter(Boolean).length,
        requests: 0, statuses: {}, responseTypes: {}, maxQueryParameterCount: 0,
      };
      if (includeRoutes) item.route = `${url.origin}${url.pathname}`;
      endpoints.set(key, item);
    }
    const item = endpoints.get(key);
    item.requests++;
    item.maxQueryParameterCount = Math.max(item.maxQueryParameterCount, [...url.searchParams].length);
    const status = entry.response?.status;
    const statusKey = Number.isInteger(status) && status >= 100 && status <= 599 ? String(status) : 'unknown';
    item.statuses[statusKey] = (item.statuses[statusKey] || 0) + 1;
    const rawMime = entry.response?.content?.mimeType;
    const mime = typeof rawMime === 'string' ? rawMime.split(';', 1)[0].trim().toLowerCase() : '';
    const mimeKey = MIMES.has(mime) ? mime : 'other';
    item.responseTypes[mimeKey] = (item.responseTypes[mimeKey] || 0) + 1;
  }
  return {
    schema: 1,
    mode: includeRoutes ? 'route-preview-not-sanitized' : 'structure-only',
    reviewRequired: true,
    limitations: includeRoutes
      ? 'Hosts and paths may contain secrets or personal data. Review locally before sharing. Queries, headers, cookies and bodies are omitted.'
      : 'Opaque identities and counts only; insufficient to reconstruct API semantics. This is not a sanitized HAR or a guarantee that derived usage statistics are non-sensitive.',
    totalEntries: har.log.entries.length, skippedEntries: skipped,
    hostCount: hosts.size, endpoints: [...endpoints.values()],
  };
}

export function parseArgs(args) {
  let input, output;
  let includeRoutes = false;
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === '--include-routes') includeRoutes = true;
    else if (arg === '--out') {
      if (output || !args[i + 1] || args[i + 1].startsWith('--')) throw new Error('Provide --out once with a new file path.');
      output = args[++i];
    } else if (arg.startsWith('--') || input) throw new Error('Unexpected argument.');
    else input = arg;
  }
  if (!input) throw new Error('Usage: node har-summary.mjs INPUT [--out NEW_FILE] [--include-routes]');
  return { input, output, includeRoutes };
}

export async function main(args) {
  const { input, output, includeRoutes } = parseArgs(args);
  const handle = await open(input, 'r');
  let bytes;
  try {
    const stat = await handle.stat();
    if (!stat.isFile() || stat.size > MAX_BYTES) throw new Error('Input must be a regular HAR file of at most 25 MiB.');
    // Bounded read also protects against a file growing after stat().
    const buffer = Buffer.alloc(MAX_BYTES + 1);
    let length = 0;
    while (length < buffer.length) {
      const { bytesRead } = await handle.read(buffer, length, buffer.length - length, null);
      if (!bytesRead) break;
      length += bytesRead;
    }
    if (length > MAX_BYTES) throw new Error('Input exceeds the 25 MiB limit.');
    bytes = buffer.subarray(0, length);
  } finally { await handle.close(); }
  let har;
  try { har = JSON.parse(bytes.toString('utf8').replace(/^\uFEFF/, '')); }
  catch { throw new Error('Invalid HAR JSON. No input content was printed.'); }
  const report = summarizeHar(har, { includeRoutes });
  report.sourceSha256 = createHash('sha256').update(bytes).digest('hex');
  const json = `${JSON.stringify(report, null, 2)}\n`;
  if (includeRoutes) console.error('WARNING: literal routes may expose secrets or personal data. Review locally before sharing.');
  if (output) {
    // Exclusive creation also refuses an existing symlink and the input itself.
    const out = await open(output, 'wx', 0o600);
    try { await out.writeFile(json, 'utf8'); } finally { await out.close(); }
    console.log('Summary written to the requested new file. Review it before sharing.');
  } else process.stdout.write(json);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).catch(error => {
    // Filesystem messages can reveal user paths; report only the code.
    console.error(error.code ? `File operation failed (${error.code}); input unchanged.` : error.message);
    process.exitCode = 1;
  });
}
