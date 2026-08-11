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


# --- WI-339: the comparison is of CONTENT, not of a checkout --------------------
# `.gitattributes` declares the vendored docs `text eol=lf`, so they are STORED
# LF — but a working tree can hold CRLF anyway (edit residue on Windows; WI-337
# found 67 such files in this repo). Hashing raw bytes then reports EVERY vendored
# file as drifted at once, and the message blames upstream: "differs from pinned
# upstream — re-vendor or re-pin". Re-vendoring "fixes" it until the next Windows
# edit; re-pinning records a hash of somebody's checkout. Same defect class as the
# duplicate census before WI-337: a checksum of the checkout used as a checksum of
# the content.
#
# THE CARE THIS NEEDED THAT WI-337's DID NOT: a vendored file may legitimately be
# BINARY, and stripping CR bytes from a PNG or a zip would corrupt the comparison
# — the opposite failure. So the rule is content-sniffed rather than applied
# blindly, and both sides get the same treatment, because the fetched remote may
# itself be served with either ending.

# Control bytes that legitimately occur in text. Everything else below 0x20 is
# not something a vendored document contains.
_TEXT_CONTROLS = frozenset(b"\t\r\n\f\v")


def looks_text(data):
    """Whether `data` is confidently TEXT, and may therefore be line-normalized.

    POSITIVE identification, not "binary means contains a NUL". 130-REVIEW-A
    refuted the negative form: a valid binary PPM whose single pixel is
    `(13, 10, 255)` contains CRLF and **no NUL**, so it was normalized — and two
    byte-distinct images then produced the SAME digest, which is a false MATCH in
    a drift detector, the worst direction to be wrong in. Confirmed here before
    fixing:

        byte-distinct : True
        NUL in either : False
        DIGESTS COLLIDE: True

    The test is therefore what text IS: decodable as UTF-8, and free of control
    bytes other than the whitespace ones. That PPM fails on the first clause
    (`0xFF` is an invalid start byte), which is exactly the discrimination the
    NUL heuristic could not make.

    Deliberately not inferred from the file EXTENSION: an unknown extension must
    not silently opt a file out of the line-ending fix. Empty content is text —
    there is nothing to mangle."""
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return False
    return not any(b < 0x20 and b not in _TEXT_CONTROLS for b in data)


def looks_binary(data):
    """The complement of `looks_text` — kept as a name because the call sites and
    the guards read better in the negative, and because a reader coming from the
    original NUL heuristic will look for it."""
    return not looks_text(data)


def content_digest(data):
    """The sha256 of `data` as CONTENT: CRLF and lone CR collapse to LF for text,
    while binary is hashed exactly as it is.

    Returns `(digest, normalized)` so the caller can say WHICH rule it applied —
    a comparison that silently changes its own basis is how the original defect
    stayed invisible."""
    if looks_binary(data):
        return hashlib.sha256(data).digest(), False
    canonical = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(canonical).digest(), True


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
        local_digest, normalized = content_digest(local.read_bytes())
        remote_digest, _ = content_digest(remote)
        if local_digest != remote_digest:
            print(
                "check_vendored: WARN - {} differs from pinned upstream "
                "({}/{}) [{}] — re-vendor or re-pin.".format(
                    local_rel,
                    base,
                    up_rel,
                    "line endings normalized" if normalized else "binary, exact bytes",
                )
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
