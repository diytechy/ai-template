#!/usr/bin/env python3
"""Drift check for vendored third-party docs (stdlib only, network-gated, warn-first).

Some repos vendor a *verbatim* copy of an upstream doc set — e.g. the
tier-conditional guardrails core + playbooks (process-options.md "Tier-conditional
guardrails"). Vendoring keeps them offline and reviewable, but a copy silently
rots against its source. This compares each vendored file against its PINNED
upstream raw URL and WARNS on any difference (locally modified, or upstream
re-pinned). It never fetches anything into the workspace and never auto-updates:
updating is a human-reviewed re-copy that bumps the commit in the manifest.

Network-gated: any fetch failure degrades to a clean per-file skip (like
check_docs --stale off-git), so it never blocks an offline run or a CI without
egress. Warn-only by default (exit 0); `--strict` exits 1 on drift/missing.

Manifest (docs/guardrails/UPSTREAM by default) — `base` is the raw URL prefix
INCLUDING the pinned commit, then one `<local-path> = <upstream-path>` per file:

    # guardrails vendored from the upstream kit, pinned
    base = https://raw.githubusercontent.com/OWNER/REPO/<COMMIT_SHA>
    docs/guardrails/core.md = CLAUDE.md
    docs/guardrails/PLAN.md = docs/guardrails/PLAN.md

Usage:
    python scripts/check_vendored.py [--root .] [--manifest docs/guardrails/UPSTREAM]
                                     [--strict] [--timeout 10]

Contracts: IF-016, IF-036 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import hashlib
import sys
import urllib.error
import urllib.request
from pathlib import Path


def _utf8_console():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def parse_manifest(text):
    """(base, [(local_path, upstream_path), ...]) from the UPSTREAM manifest.
    Blank/`#` lines are skipped; the `base = URL` line sets the fetch prefix."""
    base = None
    files = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip()
        if key == "base":
            base = val.rstrip("/")
        else:
            files.append((key, val))
    return base, files


def fetch(url, timeout):
    """(bytes, None) on success; (None, reason) on any network failure — so the
    caller degrades to a skip rather than failing without egress."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as resp:
            return resp.read(), None
    except (urllib.error.URLError, ValueError, OSError) as exc:
        return None, str(getattr(exc, "reason", exc) or exc)


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--manifest", default="docs/guardrails/UPSTREAM")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="exit 1 on drift/missing (default: warn-only, exit 0)",
    )
    ap.add_argument("--timeout", type=float, default=10.0)
    args = ap.parse_args()

    root = Path(args.root).resolve()
    manifest = root / args.manifest
    if not manifest.exists():
        print(
            "check_vendored: no manifest at {} — nothing vendored to check.".format(
                args.manifest
            )
        )
        return 0
    base, files = parse_manifest(manifest.read_text(encoding="utf-8"))
    if not base or not files:
        print("check_vendored: manifest has no base/files — nothing to check.")
        return 0

    drift = 0
    for local_rel, up_rel in files:
        local = root / local_rel
        if not local.exists():
            print("check_vendored: WARN - vendored file missing: {}".format(local_rel))
            drift += 1
            continue
        remote, err = fetch(base + "/" + up_rel.lstrip("/"), args.timeout)
        if remote is None:
            print(
                "check_vendored: skipped {} (network unavailable: {})".format(
                    local_rel, err
                )
            )
            continue
        if (
            hashlib.sha256(local.read_bytes()).digest()
            != hashlib.sha256(remote).digest()
        ):
            print(
                "check_vendored: WARN - {} differs from pinned upstream "
                "({}/{}) — re-vendor or re-pin.".format(local_rel, base, up_rel)
            )
            drift += 1

    if drift and args.strict:
        print("check_vendored: FAIL - {} vendored file(s) drifted.".format(drift))
        return 1
    if drift:
        print("check_vendored: {} finding(s) (warn-only).".format(drift))
    else:
        print("check_vendored: OK - vendored copies match the pinned upstream.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
