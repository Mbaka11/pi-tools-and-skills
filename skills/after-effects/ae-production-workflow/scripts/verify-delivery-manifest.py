#!/usr/bin/env python3
"""Verify a strict AE delivery manifest (relative path, byte size, SHA-256)."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
from typing import Any

SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def within_root(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def failure(path: Any, reason: str, **details: Any) -> dict[str, Any]:
    return {"path": path, "reason": reason, **details}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", help="Path to delivery_manifest.json")
    parser.add_argument("--root", default=".", help="Project root; defaults to cwd")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    manifest_path = Path(args.manifest).resolve()
    failures: list[dict[str, Any]] = []
    checked: list[dict[str, Any]] = []

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        result = {
            "ok": False,
            "manifest": str(manifest_path),
            "root": str(root),
            "entriesChecked": 0,
            "canonicalOk": False,
            "failures": [failure(str(manifest_path), "manifest read/JSON error", error=str(exc))],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1

    if not isinstance(manifest, dict):
        failures.append(failure(str(manifest_path), "manifest root must be an object"))
        manifest = {}

    files = manifest.get("files")
    if not isinstance(files, list) or not files:
        failures.append(failure("files", "must be a non-empty array"))
        files = []

    canonical = manifest.get("canonical")
    canonical_hash = manifest.get("canonical_sha256")
    if not isinstance(canonical, str) or not canonical.strip():
        failures.append(failure("canonical", "must be a non-empty relative path"))
        canonical = None
    if not isinstance(canonical_hash, str) or not SHA256_RE.fullmatch(canonical_hash):
        failures.append(failure("canonical_sha256", "must be a 64-character SHA-256 hex string"))
        canonical_hash = None

    seen: set[str] = set()
    canonical_entry_found = False

    for index, item in enumerate(files):
        label = f"files[{index}]"
        if not isinstance(item, dict):
            failures.append(failure(label, "entry must be an object"))
            continue

        rel = item.get("path")
        expected_size = item.get("size")
        expected_digest = item.get("sha256")

        if not isinstance(rel, str) or not rel.strip():
            failures.append(failure(label, "path must be a non-empty string"))
            continue
        rel_path = Path(rel)
        if rel_path.is_absolute():
            failures.append(failure(rel, "path must be relative to project root"))
            continue
        normalized = rel_path.as_posix()
        key = normalized.casefold()
        if key in seen:
            failures.append(failure(rel, "duplicate path entry"))
            continue
        seen.add(key)

        if not isinstance(expected_size, int) or isinstance(expected_size, bool) or expected_size < 0:
            failures.append(failure(rel, "size must be a non-negative integer"))
            continue
        if not isinstance(expected_digest, str) or not SHA256_RE.fullmatch(expected_digest):
            failures.append(failure(rel, "sha256 must be a 64-character hex string"))
            continue
        expected_digest = expected_digest.lower()

        path = (root / rel_path).resolve()
        if not within_root(root, path):
            failures.append(failure(rel, "path escapes project root"))
            continue
        if not path.is_file():
            failures.append(failure(rel, "missing or not a regular file"))
            continue

        try:
            size = path.stat().st_size
            digest = sha256(path)
        except Exception as exc:
            failures.append(failure(rel, "file read/hash error", error=str(exc)))
            continue

        ok = size == expected_size and digest == expected_digest
        checked.append({"path": normalized, "size": size, "sha256": digest, "ok": ok})
        if not ok:
            failures.append(
                failure(
                    normalized,
                    "size/hash mismatch",
                    expectedSize=expected_size,
                    actualSize=size,
                    expectedSha256=expected_digest,
                    actualSha256=digest,
                )
            )

        if canonical and normalized.casefold() == Path(canonical).as_posix().casefold():
            canonical_entry_found = True

    canonical_ok = False
    if canonical and canonical_hash:
        canonical_rel = Path(canonical)
        if canonical_rel.is_absolute():
            failures.append(failure(canonical, "canonical path must be relative"))
        else:
            canonical_path = (root / canonical_rel).resolve()
            if not within_root(root, canonical_path):
                failures.append(failure(canonical, "canonical path escapes project root"))
            elif not canonical_path.is_file():
                failures.append(failure(canonical, "canonical file is missing"))
            else:
                try:
                    canonical_ok = sha256(canonical_path) == canonical_hash.lower()
                except Exception as exc:
                    failures.append(failure(canonical, "canonical hash error", error=str(exc)))
                if not canonical_ok:
                    failures.append(failure(canonical, "canonical hash mismatch"))
        if not canonical_entry_found:
            failures.append(failure(canonical, "canonical must also appear in files[]"))

    result = {
        "ok": not failures,
        "manifest": str(manifest_path),
        "root": str(root),
        "entriesChecked": len(checked),
        "canonicalOk": canonical_ok,
        "failures": failures,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
