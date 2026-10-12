#!/usr/bin/env node
import { pathToFileURL } from 'node:url';
import { readLock } from './upstreams.mjs';

export async function latestVersions(lock, fetchImpl = fetch) {
  const reports = [];
  for (const [name, pinned] of Object.entries(lock.upstreams)) {
    const url = pinned.npmPackage
      ? `https://registry.npmjs.org/${encodeURIComponent(pinned.npmPackage)}/latest`
      : `https://api.github.com/repos/${pinned.repository.slice('https://github.com/'.length)}/releases/latest`;
    try {
      const response = await fetchImpl(url, {
        headers: { Accept: 'application/json', 'User-Agent': 'pi-tools-and-skills-update-check' },
        signal: AbortSignal.timeout(15_000), redirect: 'error',
      });
      if (!response.ok) throw new Error(`Metadata HTTP ${response.status}`);
      const data = await response.json();
      const latest = pinned.npmPackage ? data.version : data.tag_name?.replace(/^v/, '');
      if (!/^\d+\.\d+\.\d+$/.test(latest || '')) throw new Error('Unexpected release metadata.');
      reports.push({ name, pinned: pinned.version, latest, differs: latest !== pinned.version, action: latest === pinned.version ? 'none' : 'review-before-changing-pins' });
    } catch {
      // Do not log remote bodies, headers, or ambient credentials.
      reports.push({ name, pinned: pinned.version, error: 'Metadata unavailable, rate-limited, or invalid. Pins unchanged.' });
    }
  }
  return reports;
}

export async function main() {
  const report = await latestVersions(await readLock());
  console.log(JSON.stringify({ changesApplied: false, upstreams: report }, null, 2));
  if (report.some(item => item.error)) process.exitCode = 1;
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(() => { console.error('Update check failed; no files changed.'); process.exitCode = 1; });
}
