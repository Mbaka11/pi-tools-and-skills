import { readFile, lstat } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

export const ROOT = fileURLToPath(new URL('../', import.meta.url));
export const LOCK_PATH = path.join(ROOT, 'tools/upstreams.lock.json');

export async function readLock() {
  const lock = JSON.parse(await readFile(LOCK_PATH, 'utf8'));
  if (lock.schema !== 1 || !lock.upstreams || Array.isArray(lock.upstreams)) throw new Error('Invalid upstream lock schema.');
  for (const [name, item] of Object.entries(lock.upstreams)) {
    if (!/^[a-z][a-z0-9-]+$/.test(name) || !/^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(item.repository)) throw new Error('Invalid upstream identity.');
    if (!/^[a-f0-9]{40}$/.test(item.commit) || !/^\d+\.\d+\.\d+$/.test(item.version)) throw new Error('Upstreams must use an exact version and full commit.');
  }
  return lock;
}

export async function rejectSymlinks(root, relative) {
  const parts = relative.split('/');
  if (parts.some(part => !part || part === '..' || part.includes('\\') || part.includes(':'))) throw new Error('Unsafe relative path.');
  let current = root;
  for (const part of parts) {
    current = path.join(current, part);
    try { if ((await lstat(current)).isSymbolicLink()) throw new Error('Symlink paths are not accepted.'); }
    catch (error) { if (error.code !== 'ENOENT') throw error; }
  }
  return current;
}
