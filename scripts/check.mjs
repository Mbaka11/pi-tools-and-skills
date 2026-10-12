#!/usr/bin/env node
import { readFile, readdir, lstat } from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { pathToFileURL } from 'node:url';
import { ROOT, readLock, rejectSymlinks } from './upstreams.mjs';

export function frontmatter(text) {
  const match = text.match(/^---\r?\n([\s\S]*?)\r?\n---(?:\r?\n|$)/);
  if (!match) throw new Error('Missing skill frontmatter.');
  const fields = {};
  for (const line of match[1].split(/\r?\n/)) {
    const field = line.match(/^([a-z][a-z-]*):\s*(.*?)\s*$/);
    if (field) fields[field[1]] = field[2].replace(/^"(.*)"$/, '$1');
  }
  if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(fields.name || '') || fields.name.length > 64) throw new Error('Invalid skill name.');
  if (!fields.description || fields.description.length > 1024) throw new Error('Invalid skill description.');
  return fields;
}

export async function validate() {
  const errors = [], skills = [];
  const pkg = JSON.parse(await readFile(path.join(ROOT, 'package.json'), 'utf8'));
  if (!/^\d+\.\d+\.\d+$/.test(pkg.version)) errors.push('Invalid package version.');
  if (pkg.license !== 'UNLICENSED' || pkg.private !== true) errors.push('Personal licensing/publication policy changed. Review RIGHTS.md.');
  if (pkg.dependencies || pkg.scripts?.postinstall || pkg.scripts?.prepare) errors.push('Unexpected automatic dependency or install hook.');
  if (JSON.stringify(pkg.pi) !== JSON.stringify({ skills: ['./skills'] })) errors.push('Unexpected package resource exposure.');
  const dirs = await readdir(path.join(ROOT, 'skills'), { withFileTypes: true });
  for (const dir of dirs) {
    if (!dir.isDirectory()) { errors.push(`Unexpected skill entry: ${dir.name}`); continue; }
    const file = `skills/${dir.name}/SKILL.md`;
    try {
      const meta = frontmatter(await readFile(path.join(ROOT, file), 'utf8'));
      if (meta.name !== dir.name || skills.includes(meta.name)) errors.push(`Skill name mismatch/collision: ${file}`);
      skills.push(meta.name);
    } catch (error) { errors.push(`${file}: ${error.message}`); }
  }
  if (skills.length !== 6) errors.push('Expected six curated skills. Update checks deliberately when adding more.');
  const lock = await readLock();
  const lockedFiles = new Set();
  for (const [name, item] of Object.entries(lock.upstreams)) {
    if (item.license !== 'MIT' || !item.files || !Object.keys(item.files).length) errors.push(`Missing third-party provenance: ${name}`);
    for (const [relative, digest] of Object.entries(item.files || {})) {
      lockedFiles.add(relative);
      if (!relative.startsWith(`vendor/${name}/`) || !/^[a-f0-9]{64}$/.test(digest)) { errors.push(`Invalid vendor lock: ${relative}`); continue; }
      try {
        const file = await rejectSymlinks(ROOT, relative);
        if (createHash('sha256').update(await readFile(file)).digest('hex') !== digest) errors.push(`Vendor digest mismatch: ${relative}`);
      } catch { errors.push(`Missing/unsafe vendor file: ${relative}`); }
    }
  }
  const example = JSON.parse(await readFile(path.join(ROOT, 'tools/rea/mcp.example.json'), 'utf8'));
  if (example.mcpServers?.rea?.enabled !== false || !example.mcpServers.rea.args.includes(`rea-agents@${lock.upstreams.rea.version}`)) errors.push('MCP example must be disabled and match the REA pin.');
  const readme = await readFile(path.join(ROOT, 'README.md'), 'utf8');
  const changelog = await readFile(path.join(ROOT, 'CHANGELOG.md'), 'utf8');
  if (!readme.includes(`@v${pkg.version}`) || !changelog.includes(`## ${pkg.version}`)) errors.push('Release documentation does not match the package version.');
  const ignored = new Set(['.git', '.local', 'node_modules', '__pycache__']);
  async function walk(dir, prefix = '') {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      if (ignored.has(entry.name)) continue;
      const rel = prefix + entry.name, file = path.join(dir, entry.name);
      if (entry.isSymbolicLink()) { errors.push(`Symlink is not portable: ${rel}`); continue; }
      if (entry.isDirectory()) { await walk(file, `${rel}/`); continue; }
      if (/\.(?:har|jsonl|sqlite|db|pem|key|pfx|pcap|pcapng|aep|aepx|mp4|pdf|log|tgz|zip|pyc)$/i.test(rel) || /^(?:\.env(?:\..*)?|auth\.json|mcp-auth\.json|settings\.json|mcp\.json)$/i.test(entry.name)) errors.push(`Private/generated artifact outside .local: ${rel}`);
      if (rel.startsWith('vendor/') && !lockedFiles.has(rel)) errors.push(`Untracked vendor snapshot: ${rel}`);
      const stat = await lstat(file);
      if (stat.size > 512 * 1024) { errors.push(`Unexpected large file: ${rel}`); continue; }
      const text = await readFile(file, 'utf8');
      if (/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\bgh[pousr]_[A-Za-z0-9]{30,}|\bgithub_pat_[A-Za-z0-9_]{40,}/.test(text)) errors.push(`Potential secret: ${rel}`);
      if (/[A-Z]:[\\/]Users[\\/][^\s<>"']+/i.test(text)) errors.push(`Personal absolute path: ${rel}`);
      if (rel.endsWith('.md') && !rel.startsWith('vendor/')) {
        for (const [, target] of text.matchAll(/\[[^\]]*\]\(([^\s)]+)\)/g)) {
          if (/^(?:https?:|#|mailto:)/.test(target) || target.includes('<')) continue;
          const relative = decodeURIComponent(target.split('#')[0]);
          try { await lstat(path.resolve(path.dirname(file), relative)); }
          catch { errors.push(`Broken local link in ${rel}: ${target}`); }
        }
      }
    }
  }
  await walk(ROOT);
  return { ok: errors.length === 0, version: pkg.version, skills, errors };
}
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  validate().then(result => { console.log(JSON.stringify(result, null, 2)); if (!result.ok) process.exitCode = 1; })
    .catch(error => { console.error(error.message); process.exitCode = 1; });
}
