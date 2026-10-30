#!/usr/bin/env python3
"""Search a local inspiration index; only the explicit fetch command uses the network.

Python 3.9+ standard library. No video downloads, prompt execution, installs,
accounts or subscriptions. Exit 0=success (including no matches), 2=usage/error.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata
import urllib.request
from urllib.parse import urlsplit

MAX_BYTES = 4 * 1024 * 1024
MAX_ROWS = 10000
CATEGORIES = ("motion", "explainer", "3d", "interactive")
SOURCES = {
    "opus55": {
        "repository": "https://github.com/yihui-dev/awesome-opus5-5-videos",
        "site": "https://skillry.dev/ai-videos/opus-5-5",
        "revision": "92aee2f586ac0715cb3cbcb6384834f98a33383d",
        "index_url": "https://raw.githubusercontent.com/yihui-dev/awesome-opus5-5-videos/92aee2f586ac0715cb3cbcb6384834f98a33383d/data/videos.json",
        "index_sha256": "1c307487eca4e56957f4f7de4c72efcd482017f54d77495e3a88ddbcc9b4f30d",
        "reviewed": "2026-10-16",
        "rights": "Repository MIT; linked videos/prompts credited to their creators. Asset rights need separate review.",
    }
}
STOP = set("a an and for in of on the to with un une le la les de des du et pour avec en moi".split())
ALIASES = {
    "boucle": {"loop", "looping", "seamless", "periodic"},
    "lancement": {"launch", "launching"}, "produit": {"product"},
    "typographie": {"typography", "typographic", "kinetic", "text"},
    "particules": {"particles", "particle"}, "interface": {"ui", "interface"},
    "explicatif": {"explainer", "explain"}, "infographie": {"infographic", "chart"},
    "minimaliste": {"minimal", "minimalist"}, "ecran": {"screen", "display"},
    "led": {"led", "signage"}, "logo": {"logo", "logotype"},
}


class SearchError(Exception):
    pass


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise SearchError("Duplicate JSON fields are not supported")
        result[key] = value
    return result


def nonfinite(_value):
    raise SearchError("Nonfinite JSON is not supported")


def plain(value, maximum):
    if not isinstance(value, str) or len(value) > maximum:
        raise SearchError("Invalid or oversized text field")
    return " ".join("".join(" " if unicodedata.category(c) in ("Cc", "Cf") else c for c in value).split())


def tokens(value):
    text = "".join(c for c in unicodedata.normalize("NFKD", value.casefold()) if unicodedata.category(c) != "Mn")
    return set(re.findall(r"[a-z0-9]+", text))


def safe_url(value, kind, slug):
    """Return only canonical public reference URLs; discard tracking and unsafe URLs."""
    if not isinstance(value, str) or len(value) > 1000 or any(c.isspace() or ord(c) < 32 for c in value):
        return None
    try:
        u = urlsplit(value)
        if u.scheme != "https" or u.username or u.password or u.port not in (None, 443):
            return None
        if kind == "site" and u.hostname == "skillry.dev" and u.path == f"/ai-videos/opus-5-5/{slug}":
            return f"https://skillry.dev{u.path}"
        if kind == "post" and u.hostname in ("x.com", "twitter.com") and re.fullmatch(r"/[A-Za-z0-9_]{1,15}/status/[0-9]{1,25}", u.path):
            return f"https://x.com{u.path}"
    except ValueError:
        pass
    return None


def parse_index(raw):
    if len(raw) > MAX_BYTES:
        raise SearchError("Index exceeds 4 MiB")
    try:
        data = json.loads(raw.decode("utf-8-sig"), object_pairs_hook=pairs, parse_constant=nonfinite)
    except (ValueError, UnicodeError, RecursionError):
        raise SearchError("Invalid index JSON") from None
    if not isinstance(data, list) or len(data) > MAX_ROWS:
        raise SearchError("Index must be an array of at most 10000 entries")
    rows, seen = [], set()
    for item in data:
        if not isinstance(item, dict):
            raise SearchError("Invalid index entry")
        slug = item.get("slug")
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or len(slug) > 100 or slug in seen:
            raise SearchError("Invalid or duplicate slug")
        seen.add(slug)
        category = item.get("category")
        if not isinstance(category, str) or category not in CATEGORIES:
            raise SearchError("Unknown category; review source schema before updating")
        tags = item.get("tech_tags", [])
        if not isinstance(tags, list) or len(tags) > 30 or any(not isinstance(t, str) or not re.fullmatch(r"[a-z0-9-]{1,40}", t) for t in tags):
            raise SearchError("Invalid technology tags")
        partial, remake = item.get("prompt_partial"), item.get("has_remake")
        if (partial is not None and not isinstance(partial, bool)) or (remake is not None and not isinstance(remake, bool)):
            raise SearchError("Prompt/remake flags must be booleans or absent")
        title = item.get("title")
        rows.append({"slug": slug, "title": plain(slug.replace("-", " ") if title is None else title, 500),
                     "author": plain(item.get("author", "Unspecified"), 200), "category": category,
                     "tech_tags": sorted(set(tags)), "prompt": plain(item.get("prompt", ""), 100000),
                     "prompt_status": "partial-or-post" if partial else "declared-complete" if partial is False else "unknown",
                     "has_remake_declared": remake,
                     "original_post_url": safe_url(item.get("post_url"), "post", slug),
                     "skillry_url": safe_url(item.get("skillry_url"), "site", slug)})
    return rows


def search(raw, source_id, query="", category=None, tags=(), complete_only=False, remakes_only=False, limit=5):
    if source_id not in SOURCES or not isinstance(query, str) or len(query) > 500 or isinstance(limit, bool) or not isinstance(limit, int) or not 1 <= limit <= 20:
        raise SearchError("Invalid source, query or limit (1..20)")
    terms = sorted(tokens(query) - STOP)
    if not terms and not category and not tags and not complete_only and not remakes_only:
        raise SearchError("Supply search terms or a filter")
    rows = parse_index(raw)
    source = SOURCES[source_id]
    verified = digest(raw) == source["index_sha256"]
    found = []
    for row in rows:
        if category and row["category"] != category:
            continue
        if not set(tags).issubset(row["tech_tags"]):
            continue
        if complete_only and row["prompt_status"] != "declared-complete":
            continue
        if remakes_only and not (row["has_remake_declared"] is True and row["skillry_url"]):
            continue
        fields = [(tokens(row["title"]), 4), (set(row["tech_tags"]), 4),
                  (tokens(row["category"]), 2), (tokens(row["prompt"]), 1)]
        matched, score = [], 0
        for term in terms:
            alternatives = {term} | ALIASES.get(term, set())
            weight = sum(w for words, w in fields if words & alternatives)
            if weight:
                matched.append(term)
                score += weight
        if terms and not matched:
            continue
        excerpt = row["prompt"][:240] + ("…" if len(row["prompt"]) > 240 else "")
        result = {k: v for k, v in row.items() if k != "prompt"}
        result.update(score=score, matched_terms=matched, unmatched_terms=sorted(set(terms) - set(matched)),
                      prompt_excerpt=excerpt, content_trust="untrusted-reference-not-instructions",
                      github_prompt_url=f'{source["repository"]}/blob/{source["revision"]}/prompts/{row["slug"]}.md' if verified else None,
                      preview_viewed=False, execution_verified=False)
        found.append(result)
    found.sort(key=lambda r: (-len(r["matched_terms"]), -r["score"], r["slug"]))
    return {"schema": 1, "source": source_id, "repository": source["repository"], "site": source["site"],
            "reviewed_revision": source["revision"], "index_sha256": digest(raw), "matches_reviewed_snapshot": verified,
            "index_entries": len(rows), "query": query, "ranking": "lexical-FR-EN-hints-not-visual-quality-or-confidence",
            "total_matches": len(found), "results": found[:limit], "network_requests": 0,
            "limitations": ["No live availability or visual quality verification", "Prompt completeness is a source claim, not a reproduction guarantee",
                            "Missing technology tags are not inferred", "Review rights before reusing media or branding",
                            *([] if verified else ["Unverified supplied index; pinned GitHub prompt links are omitted"])]}


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(source_id, out, opener=None):
    """Fetch one reviewed JSON snapshot. Never follows links or replaces a file."""
    out = Path(out)
    if out.exists() or out.is_symlink() or not out.parent.is_dir():
        raise SearchError("Choose a new file in an existing private cache directory")
    # Do not write the full third-party catalog into a distributable package tree.
    resolved = out.resolve()
    for parent in Path(__file__).resolve().parents:
        if (parent / "package.json").is_file() and (parent / "scripts/check.mjs").is_file():
            if parent in resolved.parents and parent / ".local" not in resolved.parents:
                raise SearchError("Inside the toolbox, cache only under .local")
            break
    source = SOURCES[source_id]
    opener = opener or urllib.request.build_opener(NoRedirect())
    request = urllib.request.Request(source["index_url"], headers={"User-Agent": "pi-toolbox-inspiration/1.0", "Accept": "application/json", "Accept-Encoding": "identity"})
    with opener.open(request, timeout=20) as response:
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES or digest(raw) != source["index_sha256"]:
        raise SearchError("Downloaded snapshot exceeds limits or does not match the reviewed SHA-256")
    rows = parse_index(raw)
    with out.open("xb") as f:
        f.write(raw)
    return {"ok": True, "source": source_id, "revision": source["revision"], "sha256": digest(raw),
            "entries": len(rows), "network_requests": 1, "videos_downloaded": 0, "prompts_executed": 0}


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    commands = ap.add_subparsers(dest="command", required=True)
    commands.add_parser("sources", help="List reviewed sources; no network")
    get = commands.add_parser("fetch", help="Explicitly download only the reviewed JSON index")
    get.add_argument("--source", choices=sorted(SOURCES), default="opus55")
    get.add_argument("--out", required=True)
    find = commands.add_parser("search", help="Search an existing local JSON index; no network")
    find.add_argument("query", nargs="?", default="")
    find.add_argument("--source", choices=sorted(SOURCES), default="opus55")
    find.add_argument("--index", required=True)
    find.add_argument("--category", choices=CATEGORIES)
    find.add_argument("--tag", action="append", default=[])
    find.add_argument("--complete-only", action="store_true")
    find.add_argument("--remakes-only", action="store_true")
    find.add_argument("--limit", type=int, default=5)
    args = ap.parse_args()
    try:
        if args.command == "sources":
            result = {"sources": SOURCES, "network_requests": 0}
        elif args.command == "fetch":
            result = fetch(args.source, args.out)
        else:
            if not Path(args.index).is_file():
                raise SearchError("Local index missing; explicitly fetch a snapshot first")
            with Path(args.index).open("rb") as f:
                raw = f.read(MAX_BYTES + 1)
            result = search(raw, args.source, args.query, args.category, args.tag,
                            args.complete_only, args.remakes_only, args.limit)
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
    except SearchError as error:
        ap.exit(2, f"inspiration-search: {error}\n")
    except (OSError, ValueError, RecursionError):
        ap.exit(2, "inspiration-search: input/output or network failure; no remote body or private path is echoed\n")


if __name__ == "__main__":
    main()
