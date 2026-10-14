#!/usr/bin/env node
import { pathToFileURL } from 'node:url';
import { readLock } from './upstreams.mjs';

// Released upstreams are compared by version (npm or GitHub latest release).
// Unreleased snapshots are compared by the tracked branch's current commit.
function metadataUrl(pinned) {
  const slug = pinned.repository.slice('https://github.com/'.length);
  if (pinned.npmPackage) return `https://registry.npmjs.org/${encodeURIComponent(pinned.npmPackage)}/latest`;
  if (pinned.version === 'unreleased') return `https://api.github.com/repos/${slug}/commits/${encodeURIComponent(pinned.branch)}`;
  return `https://api.github.com/repos/${slug}/releases/latest`;
}

export async function latestVersions(lock, fetchImpl = fetch) {
  const reports = [];
  for (const [name, pinned] of Object.entries(lock.upstreams)) {
    const url = metadataUrl(pinned);
    try {
      const response = await fetchImpl(url, {
        headers: { Accept: 'application/json', 'User-Agent': 'pi-tools-and-skills-update-check' },
        signal: AbortSignal.timeout(15_000), redirect: 'error',
      });
      if (!response.ok) throw new Error(`Metadata HTTP ${response.status}`);
      const data = await response.json();
      if (pinned.version === 'unreleased') {
        const latest = data?.sha;
        if (!/^[a-f0-9]{40}$/.test(latest || '')) throw new Error('Unexpected commit metadata.');
        const differs = latest !== pinned.commit;
        reports.push({ name, pinned: pinned.commit, branch: pinned.branch, latest, differs, action: differs ? 'review-diff-before-changing-pins' : 'none' });
        continue;
      }
      const latest = pinned.npmPackage ? data.version : data.tag_name?.replace(/^v/, '');
      if (!/^\d+\.\d+\.\d+$/.test(latest || '')) throw new Error('Unexpected release metadata.');
      reports.push({ name, pinned: pinned.version, latest, differs: latest !== pinned.version, action: latest === pinned.version ? 'none' : 'review-before-changing-pins' });
    } catch {
      // Do not log remote bodies, headers, or ambient credentials.
      reports.push({ name, pinned: pinned.version === 'unreleased' ? pinned.commit : pinned.version, error: 'Metadata unavailable, rate-limited, or invalid. Pins unchanged.' });
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
