#!/usr/bin/env node
// Optional exact source checkout. Default is a plan; never installs dependencies.
import { mkdir, lstat } from 'node:fs/promises';
import { spawn } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import { ROOT, readLock, rejectSymlinks } from './upstreams.mjs';

export function sourcePlan(lock, name) {
  if (!Object.hasOwn(lock.upstreams, name)) throw new Error(`Choose one of: ${Object.keys(lock.upstreams).join(', ')}.`);
  const item = lock.upstreams[name];
  return {
    name, repository: item.repository, commit: item.commit,
    destination: `.local/upstreams/${name}-${item.commit.slice(0, 12)}`,
    installsDependencies: false, executesUpstreamPrograms: false,
  };
}

async function git(args, cwd) {
  return new Promise((resolve, reject) => {
    const child = spawn('git', ['-c', 'core.hooksPath=.git/disabled-hooks', ...args], { cwd, shell: false, stdio: ['ignore', 'pipe', 'pipe'] });
    let stdout = '', stderr = '';
    const timer = setTimeout(() => { child.kill(); reject(new Error('Git timed out. Partial checkout retained for inspection.')); }, 120_000);
    child.stdout.on('data', data => { if (stdout.length < 100_000) stdout += data; });
    child.stderr.on('data', data => { if (stderr.length < 100_000) stderr += data; });
    child.on('error', error => { clearTimeout(timer); reject(error); });
    child.on('close', code => {
      clearTimeout(timer);
      if (code === 0) resolve(stdout.trim());
      else reject(new Error(`Git exited ${code}; partial checkout retained. No dependencies were installed.`));
    });
  });
}

export async function main(args) {
  if (args.length < 1 || args.length > 2 || (args[1] && args[1] !== '--fetch')) throw new Error('Usage: node scripts/fetch-source.mjs <upstream-name-from-tools/upstreams.lock.json> [--fetch]');
  const plan = sourcePlan(await readLock(), args[0]);
  console.log(JSON.stringify({ ...plan, mode: args[1] ? 'fetch' : 'plan-only' }, null, 2));
  if (!args[1]) return;
  const dest = await rejectSymlinks(ROOT, plan.destination);
  try { await lstat(dest); throw new Error('Destination already exists; refusing to alter or overwrite it.'); }
  catch (error) { if (error.code !== 'ENOENT') throw error; }
  await mkdir(dest, { recursive: true });
  await git(['-c', 'init.templateDir=', 'init', '-b', 'source'], dest);
  await git(['remote', 'add', 'origin', `${plan.repository}.git`], dest);
  await git(['fetch', '--depth=1', '--no-tags', 'origin', plan.commit], dest);
  await git(['-c', 'advice.detachedHead=false', 'checkout', '--detach', 'FETCH_HEAD'], dest);
  const actual = await git(['rev-parse', 'HEAD'], dest);
  if (actual !== plan.commit) throw new Error('Commit verification failed. Checkout is not approved for use.');
  console.log(`Verified ${plan.name} at ${actual}. Source only; no installation or activation.`);
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main(process.argv.slice(2)).catch(error => { console.error(error.code ? `File/process error: ${error.code}` : error.message); process.exitCode = 1; });
}
