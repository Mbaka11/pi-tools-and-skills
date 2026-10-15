import { readFile, readdir, stat } from 'node:fs/promises';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { rejectSymlinks } from './upstreams.mjs';

export const MAX_EXAMPLE_BYTES = 1024 * 1024;
export const MAX_GALLERY_BYTES = 8 * 1024 * 1024;
const KINDS = new Set(['original-mockup', 'measured-helper-output', 'illustrative-report']);

export function checkMediaRecord(relative, record, bytes) {
  const errors = [];
  if (!/^examples\/media\/[a-z0-9]+(?:-[a-z0-9]+)*\.(gif|png|mp4|wav)$/.test(relative)) errors.push('Invalid example media path');
  if (!record || record.origin !== 'original-synthetic' || record.license !== 'UNLICENSED' || record.generator !== 'examples/build.py') errors.push('Missing original example provenance');
  if (!Number.isSafeInteger(record?.bytes) || record.bytes < 1 || record.bytes > MAX_EXAMPLE_BYTES || bytes.length !== record.bytes) errors.push('Example media size mismatch or limit exceeded');
  if (!/^[a-f0-9]{64}$/.test(record?.sha256 || '') || createHash('sha256').update(bytes).digest('hex') !== record.sha256) errors.push('Example media hash mismatch');
  const ext = path.posix.extname(relative);
  const magic = ext === '.png' ? bytes.subarray(0, 8).equals(Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]))
    : ext === '.gif' ? /^GIF8[79]a$/.test(bytes.subarray(0, 6).toString('ascii'))
    : ext === '.wav' ? bytes.subarray(0, 4).toString('ascii') === 'RIFF' && bytes.subarray(8, 12).toString('ascii') === 'WAVE'
    : ext === '.mp4' ? bytes.subarray(4, 8).toString('ascii') === 'ftyp' : false;
  if (!magic) errors.push('Example media signature mismatch');
  if (['.gif', '.mp4', '.wav'].includes(ext) && !(Number.isFinite(record?.duration_s) && record.duration_s > 0 && record.duration_s <= 4)) errors.push('Example must last at most four seconds');
  if (['.png', '.gif'].includes(ext)) {
    if (!(Number.isSafeInteger(record?.width) && record.width > 0 && record.width <= 1920 && Number.isSafeInteger(record?.height) && record.height > 0 && record.height <= 1920)) errors.push('Invalid example dimensions');
    if (magic && ext === '.png' && bytes.length >= 24 && (bytes.readUInt32BE(16) !== record.width || bytes.readUInt32BE(20) !== record.height)) errors.push('PNG dimensions differ from manifest');
    if (magic && ext === '.gif' && bytes.length >= 10 && (bytes.readUInt16LE(6) !== record.width || bytes.readUInt16LE(8) !== record.height)) errors.push('GIF dimensions differ from manifest');
  }
  return errors;
}

export async function validateExamples(root, expectedSkills) {
  const errors = [], mediaPaths = new Set();
  let manifest;
  try { manifest = JSON.parse(await readFile(path.join(root, 'examples/manifest.json'), 'utf8')); }
  catch { return { errors: ['Missing or invalid examples/manifest.json'], mediaPaths }; }
  if (!manifest || manifest.schema !== 1 || !Array.isArray(manifest.entries) || !Array.isArray(manifest.tools) || !manifest.media || typeof manifest.media !== 'object' || Array.isArray(manifest.media)
      || manifest.entries.some(e => !e || typeof e.id !== 'string' || !Array.isArray(e.artifacts))
      || manifest.tools.some(t => !t || typeof t.path !== 'string' || typeof t.example !== 'string')) {
    return { errors: ['Invalid example manifest schema'], mediaPaths };
  }
  const ids = manifest.entries.map(e => e.id);
  if (JSON.stringify([...ids].sort()) !== JSON.stringify([...expectedSkills].sort())) errors.push('Every curated skill must have exactly one example');
  async function link(target) {
    if (typeof target !== 'string' || !target || /[\\:]/.test(target)) { errors.push(`Invalid example link: ${target}`); return; }
    const [file, anchor] = target.split('#');
    try {
      const resolved = await rejectSymlinks(root, file);
      const bytes = await readFile(resolved);
      if (!bytes.length) errors.push(`Empty example: ${target}`);
      if (anchor && !bytes.toString('utf8').split(/\r?\n/).some(l => /^#{1,6} /.test(l) && l.replace(/^#+\s*/, '').toLowerCase().replace(/[^a-z0-9 -]/g, '').replace(/ +/g, '-') === anchor)) errors.push(`Missing example anchor: ${target}`);
    } catch { errors.push(`Missing or unsafe example link: ${target}`); }
  }
  const usedMedia = new Set();
  for (const entry of manifest.entries) {
    if (!KINDS.has(entry.kind) || !entry.skill?.startsWith('skills/') || path.posix.basename(path.posix.dirname(entry.skill)) !== entry.id || !entry.example?.startsWith('examples/') || !Array.isArray(entry.artifacts) || !entry.artifacts.length) errors.push(`Invalid example entry: ${entry.id}`);
    await link(entry.skill);
    await link(entry.example);
    for (const artifact of entry.artifacts || []) {
      await link(artifact);
      if (artifact.startsWith('examples/media/')) usedMedia.add(artifact);
    }
  }
  // Inventory shipped helpers/references, not every optional tool in the research catalog.
  const helpers = [];
  async function collect(dir, prefix) {
    for (const item of await readdir(dir, { withFileTypes: true })) {
      if (item.name === '__pycache__') continue;
      const relative = `${prefix}/${item.name}`;
      if (item.isDirectory()) await collect(path.join(dir, item.name), relative);
      else if (/\/scripts\/[^/]+\.(?:py|ps1|mjs)$/.test(relative)) helpers.push(relative);
    }
  }
  await collect(path.join(root, 'skills'), 'skills');
  helpers.push(...(await readdir(path.join(root, 'scripts'))).filter(f => f.endsWith('.mjs')).map(f => `scripts/${f}`));
  helpers.push('examples/build.py', 'tools/rea/README.md', 'tools/reverse-api-engineer/README.md', 'vendor/vox-editorial/README.md', 'vendor/cinematic-score-and-sfx/README.md');
  if (JSON.stringify(manifest.tools.map(t => t.path).sort()) !== JSON.stringify(helpers.sort())) errors.push('Every included helper/tool reference must have exactly one example link');
  for (const tool of manifest.tools) { await link(tool.path); await link(tool.example); }
  let total = 0;
  for (const [relative, record] of Object.entries(manifest.media)) {
    try {
      const file = await rejectSymlinks(root, relative);
      const info = await stat(file);
      if (!info.isFile() || info.size > MAX_EXAMPLE_BYTES) { errors.push(`Oversized/non-file example media: ${relative}`); continue; }
      const bytes = await readFile(file);
      for (const e of checkMediaRecord(relative, record, bytes)) errors.push(`${relative}: ${e}`);
      total += bytes.length;
      mediaPaths.add(relative);
      if (!usedMedia.has(relative)) errors.push(`Media not linked by a skill example: ${relative}`);
    } catch { errors.push(`Missing or unsafe example media: ${relative}`); }
  }
  for (const relative of usedMedia) if (!mediaPaths.has(relative)) errors.push(`Undeclared example media: ${relative}`);
  if (total > MAX_GALLERY_BYTES) errors.push('Example gallery exceeds its 8 MiB budget');
  return { errors, mediaPaths };
}
