#!/usr/bin/env python3
"""Validate the work-item registry (docs/requirements/work-items.csv) — stdlib only.

The `SN->SR->LLR->TC` spine answers *what must be true*. A **work item**
(`WI-###`) decomposes *how the work executes*: it delivers SR(s), belongs to a
**workstream** (a mutable grouping category — the legacy `Track` header is still
read), and depends on **predecessor** work items (the DAG edges), moving
`queued -> active -> done`. This is the validation half of the trajectory layer;
the offline dashboard that renders the same registry is generated separately (a
*view*, never a source of truth — the `trace.py` / `gen_arch_map.py` idiom).

Checks (integrity, in the spirit of `trace.py`):
  - `WI-###` id shape + uniqueness — a malformed or duplicated id is an ERROR.
  - every `Predecessors` id resolves to a real work item — an ERROR (a DAG edge
    to a work item that does not exist).
  - the work-item graph is ACYCLIC over its **hard** edges — a cycle is an
    ERROR (a trajectory that depends on itself can never start).
  - a predecessor may be marked **soft** with a `~` prefix (`~WI-013`): an
    advisory-ordering hint, not a blocker. A soft edge must still resolve
    (ERROR if not), but it is excluded from the cycle rule — a cycle that
    exists only through soft edges is a WARN (conflicting hints), never an
    error — and it never constrains readiness.
  - every `SR-Refs` id exists in `system-requirements.csv` — a WARN, not a
    failure (a draft SR referenced ahead of its registry row is legitimate).

**The status.md ↔ registry SSOT rules** (S1; process-options.md "Trajectory /
work-items layer"). status.md is **forward-only** (what happens next) and the WI
`Deliverable` is **backward-only** (what shipped); the bridge is a per-WI
`SpecRef` that lives while the WI is open and clears at close. Cross-reading
`work-items.csv` and `docs/status.md` mechanizes five rules:
  - **R-A** — a WI's `Deliverable` is non-empty **iff** `Status = done`. An open
    (queued/active/deferred) WI with a filled Deliverable, or a `done` WI with an
    empty one, is a hard **ERROR at every run** (no flag needed): a commit is the
    agent handoff point, so an incoherent WI state launches the next session
    wrong.
  - **R-B** — every open WI id appears as a token in `status.md` (its context).
  - **R-C** — `status.md` names at least one open WI id (the next/active work).
  - **R-D** — no `done` WI id token appears in `status.md` (closed work leaves the
    working surface).
  - **R-E** — every open WI carries a non-empty `SpecRef` resolving to an in-repo
    target (`path` or `path#anchor`; the path part must exist).
R-B…R-E are **WARN by default, ERROR under `--strict`** (wired at G2+). If
`status.md` is absent, R-B/R-C/R-D are vacuous (a repo may not use a status
blackboard). `--staged` adds the warn-first **no-validation-delta** check.

**Opt-out and vacuous by default** — the posture of the always-on
`docs/secrets-scan` floor. The check is on unless `docs/trajectory-check` reads
the one word `off`; and an *absent* or *placeholder-only* registry (nothing but
the inert `WI-000` example row) passes vacuously. So a fresh scaffold and a repo
that never adopts the layer both stay green for free — WI is an off-spine
optional registry, like procurement / assets, whose placeholder never blocks a
gate (`trace.py` does not read WI ids at all).

Usage:  python scripts/check_trajectory.py [--root .] [--strict] [--staged]
Exit codes: 0 clean / vacuous / opted-out, 1 a hard error, 2 usage/environment.
"""

import argparse
import configparser
import csv
import re
import subprocess
import sys
from pathlib import Path

WI_CSV = "docs/requirements/work-items.csv"
SR_CSV = "docs/requirements/system-requirements.csv"
TC_CSV = "docs/test/test-cases.csv"
STATUS_MD = "docs/status.md"

# A well-formed work-item id: `WI-` then digits (`WI-001`). The `-000` example
# row matches this shape but is inert (skipped from the graph — see load_wis).
WI_ID_RE = re.compile(r"^WI-\d+$")
# A word-bounded WI id token as it appears in prose (status.md): `re.findall`
# grabs each maximal `WI-<digits>` run, so `WI-053…WI-059` yields both ids and
# `WI-05` never matches inside `WI-053` (R-D's "bare id token" rule).
WI_TOKEN_RE = re.compile(r"WI-\d+")

# The work-item lifecycle vocabulary (S1). `deferred` is a first-class,
# queued-but-not-next state carrying a recorded reason; an unknown status is a
# lint (warn-first). "Open" = anything not yet `done`.
OPEN_STATUSES = ("queued", "active", "deferred")
KNOWN_STATUSES = ("queued", "active", "done", "deferred")


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII work-item title / path can't raise UnicodeEncodeError on a legacy
    Windows cp1252 console (same guard as check.py / check_privacy.py)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _first_declared_line(path):
    """The first non-empty, non-comment line of a declared-policy file, or None
    (absent/empty) — the parse every kit reader shares (hooks, check_privacy.py,
    agent_loop.py)."""
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None


def read_trajectory_enabled(root):
    """Whether the trajectory check is on. `docs/trajectory-check` with the one
    word `off` opts out; absent or any other value reads on (the safe default),
    so an ordinary repo runs it without declaring anything — opt-out, like
    `docs/secrets-scan`."""
    return (
        _first_declared_line(root / "docs" / "trajectory-check") or ""
    ).lower() != "off"


def _split_refs(cell):
    """Ref cells hold ids separated by ; , or whitespace; empty -> []."""
    return [t for t in re.split(r"[;,\s]+", (cell or "").strip()) if t]


def read_rows(path):
    """The CSV rows of `path` as dicts, or [] when the file is absent."""
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def load_wis(rows):
    """Parse work-item rows into `(wis, integrity_errors)`.

    `wis` are the real, well-formed items that form the graph; the inert `-000`
    example row is skipped (the `trace.py` placeholder rule — an off-spine
    optional registry's placeholder never blocks a gate). Integrity errors
    (malformed or duplicated ids) are collected on the raw rows so a broken id is
    *reported*, never silently dropped."""
    wis, integrity, seen = [], [], set()
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if not wid.startswith("WI-"):
            continue  # blank line / non-WI row
        if not WI_ID_RE.match(wid):
            integrity.append(
                "malformed work-item id {!r} (expected WI-<digits>)".format(wid)
            )
            continue
        if wid in seen:
            integrity.append("duplicate work-item id {}".format(wid))
            continue
        seen.add(wid)
        if wid.endswith("-000"):
            continue  # inert template example row (like trace.py)
        # A `~` prefix marks a soft (advisory-ordering) predecessor edge; the
        # bare id is a hard (blocking) edge — see the module docstring.
        preds, soft = [], []
        for p in _split_refs(r.get("Predecessors", "")):
            if p.startswith("~"):
                soft.append(p[1:])
            else:
                preds.append(p)
        wis.append(
            {
                "id": wid,
                "title": (r.get("Title") or "").strip(),
                "workstream": (r.get("Workstream") or r.get("Track") or "").strip()
                or "other",
                "srs": _split_refs(r.get("SR-Refs", "")),
                "preds": preds,
                "soft": soft,
                "status": (r.get("Status") or "queued").strip().lower(),
                # Backward-only summary (R-A) and the forward bridge (R-E). A
                # legacy CSV without the column reads as "" (DictReader -> None).
                "deliverable": (r.get("Deliverable") or "").strip(),
                "specref": (r.get("SpecRef") or "").strip(),
            }
        )
    return wis, integrity


def _cycles(wis, pred_map):
    """Cycle strings found by DFS colouring over `pred_map` ([] = acyclic).

    Iterative (explicit stack), not recursive: a work-item registry may encode an
    arbitrarily long dependency chain, and a recursive DFS would raise a raw
    ``RecursionError`` past CPython's ~1000-frame limit — the kit fails on bad
    data with a clear message, never an uncaught traceback (THREAD_52_REVIEW.md
    F4). ``stack`` holds ``[node, next-pred-index]`` frames and ``path`` mirrors
    their nodes, so a back-edge to a GREY (on-path) node reconstructs the cycle
    exactly as the former recursion did."""
    WHITE, GREY, BLACK = 0, 1, 2
    colour = {w["id"]: WHITE for w in wis}
    found = []
    for w in wis:
        if colour[w["id"]] != WHITE:
            continue
        stack = [[w["id"], 0]]
        path = [w["id"]]
        colour[w["id"]] = GREY
        while stack:
            node, i = stack[-1]
            preds = pred_map[node]
            if i < len(preds):
                stack[-1][1] += 1
                p = preds[i]
                if colour[p] == GREY:
                    found.append(" -> ".join(path[path.index(p) :] + [p]))
                elif colour[p] == WHITE:
                    colour[p] = GREY
                    stack.append([p, 0])
                    path.append(p)
            else:
                colour[node] = BLACK
                stack.pop()
                path.pop()
    return found


def validate(wis, known_srs):
    """Return the hard-error strings for the work-item graph ([] = clean).

    Dangling `SR-Refs` are WARNED on stderr (a draft SR referenced ahead of its
    row is legitimate), never failed — and only when the SR registry is
    non-empty, so a repo without SRs yet does not spuriously warn. Soft (`~`)
    predecessors must resolve like hard ones, but only **hard** edges are
    subject to the acyclicity ERROR — a cycle that needs a soft edge to close
    is a WARN (conflicting ordering hints), never a failure."""
    ids = {w["id"] for w in wis}
    errors = []

    for w in wis:
        for p in w["preds"] + w["soft"]:
            if p not in ids:
                errors.append(
                    "{}: predecessor {!r} is not a work item".format(w["id"], p)
                )
        for s in w["srs"]:
            if known_srs and s not in known_srs:
                print(
                    "check_trajectory: WARN - {} references {} "
                    "(not in the SR registry; draft?)".format(w["id"], s),
                    file=sys.stderr,
                )

    # A hard cycle makes the trajectory unstartable -> ERROR.
    hard_map = {w["id"]: [p for p in w["preds"] if p in ids] for w in wis}
    for cyc in _cycles(wis, hard_map):
        errors.append("dependency cycle: {}".format(cyc))

    # A cycle that only closes through soft edges is a hint conflict -> WARN.
    if not any(e.startswith("dependency cycle") for e in errors):
        both_map = {
            w["id"]: [p for p in w["preds"] + w["soft"] if p in ids] for w in wis
        }
        for cyc in _cycles(wis, both_map):
            print(
                "check_trajectory: WARN - soft-edge cycle (advisory ordering "
                "hints conflict; not a blocker): {}".format(cyc),
                file=sys.stderr,
            )
    return errors


def load_known_srs(root):
    """The set of real SR ids from system-requirements.csv (for the SR-ref warn)."""
    return {
        (r.get("SR-ID") or "").strip()
        for r in read_rows(root / SR_CSV)
        if (r.get("SR-ID") or "").startswith("SR-")
    }


def _read_status_tokens(root):
    """`(text, {WI ids named in status.md})`, or `(None, set())` when status.md
    is absent (R-B/R-C/R-D are then vacuous — a repo may keep no status
    blackboard). Read errors="replace" so a stray byte degrades, never crashes
    (the declared-policy reader idiom)."""
    path = root / STATUS_MD
    if not path.exists():
        return None, set()
    text = path.read_text(encoding="utf-8", errors="replace")
    return text, set(WI_TOKEN_RE.findall(text))


def ssot_findings(wis, root):
    """The status.md ↔ work-items.csv coherence findings (R-A…R-E) + the
    unknown-status lint, each as `(rule, hard, message)`.

    `hard=True` (R-A only) is an ERROR at every run — the incoherent-handoff
    rule. The rest are warn-first; the caller promotes them to errors under
    `--strict`. Kept OUT of `validate()` so the dashboard renderer
    (`gen_trajectory`, which imports `validate`) is unaffected by a status.md it
    never reads."""
    out = []
    status_text, status_tokens = _read_status_tokens(root)
    open_ids = {w["id"] for w in wis if w["status"] in OPEN_STATUSES}
    done_ids = {w["id"] for w in wis if w["status"] == "done"}

    for w in wis:
        st = w["status"]
        if st not in KNOWN_STATUSES:
            out.append(
                (
                    "status-vocab",
                    False,
                    "{}: unknown status {!r} (expected queued|active|done|"
                    "deferred)".format(w["id"], st),
                )
            )
        # R-A: Deliverable non-empty IFF done.
        if st == "done" and not w["deliverable"]:
            out.append(
                (
                    "R-A",
                    True,
                    "{}: status=done but the Deliverable is empty (a done WI "
                    "records what shipped)".format(w["id"]),
                )
            )
        elif st != "done" and w["deliverable"]:
            out.append(
                (
                    "R-A",
                    True,
                    "{}: status={} (open) but the Deliverable is non-empty (an "
                    "open WI's Deliverable is filled only at close)".format(
                        w["id"], st
                    ),
                )
            )
        # R-E: an open WI names a resolvable SpecRef (path or path#anchor).
        if st in OPEN_STATUSES:
            spec = w["specref"]
            if not spec:
                out.append(
                    (
                        "R-E",
                        False,
                        "{}: open WI has no SpecRef (name its spec-of-record: "
                        "docs/specs/WI-###.md or a doc#anchor)".format(w["id"]),
                    )
                )
            else:
                pathpart = spec.split("#", 1)[0].strip()
                if pathpart and not (root / pathpart).exists():
                    out.append(
                        (
                            "R-E",
                            False,
                            "{}: SpecRef {!r} does not resolve to an in-repo "
                            "file".format(w["id"], spec),
                        )
                    )

    # R-B/R-C/R-D need status.md; absent -> vacuous.
    if status_text is not None:
        for wid in sorted(open_ids):
            if wid not in status_tokens:
                out.append(
                    (
                        "R-B",
                        False,
                        "{}: open WI is not named in docs/status.md (its "
                        "context/lane)".format(wid),
                    )
                )
        if open_ids and not (open_ids & status_tokens):
            out.append(
                (
                    "R-C",
                    False,
                    "docs/status.md names no open WI id (it must name the "
                    "next/active work)",
                )
            )
        for wid in sorted(done_ids & status_tokens):
            out.append(
                (
                    "R-D",
                    False,
                    "{}: a done WI id appears in docs/status.md (closed work "
                    "leaves the working surface)".format(wid),
                )
            )
    return out


def _git(root, args):
    """`git -C <root> <args>` stdout on success, else None (git absent, not a
    repo, no such object). Every staged-mode git call degrades to None so the
    no-validation-delta warn is a silent no-op outside a git checkout."""
    try:
        proc = subprocess.run(
            ["git", "-C", str(root)] + args,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, ValueError):
        return None
    return proc.stdout if proc.returncode == 0 else None


def _tests_dir(root):
    """The declared tests root (docs/stack.ini [paths] tests), default `tests` —
    the surface a real validation-logic change would touch."""
    ini = root / "docs" / "stack.ini"
    if ini.exists():
        cp = configparser.ConfigParser(interpolation=None)
        try:
            cp.read_string(ini.read_text(encoding="utf-8", errors="replace"))
            if cp.has_option("paths", "tests"):
                return cp.get("paths", "tests").strip() or "tests"
        except configparser.Error:
            pass
    return "tests"


def _wi_status_map(rows):
    """`{wid: {"status", "srs"}}` for the real (non-`-000`) rows of a WI CSV."""
    out = {}
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if WI_ID_RE.match(wid) and not wid.endswith("-000"):
            out[wid] = {
                "status": (r.get("Status") or "queued").strip().lower(),
                "srs": _split_refs(r.get("SR-Refs", "")),
            }
    return out


def staged_findings(root):
    """The no-validation-delta warn (S0 ruling #2 corollary; warn-first).

    When a commit **closes** a WI (queued/active/deferred → done) that is a
    *follow-up* on an SR a previously-`done` WI already delivered (a shared
    `SR-Ref`), yet the staged change set touches neither the TC registry nor a
    file under the tests dir, the fix landed in the code but not the validation
    chain — so the same failure can recur. Returns warning strings ([] when not
    applicable). Compares the staged WI CSV against its HEAD version via git;
    any missing git context makes it a silent no-op (the hook has git; a gate
    run does not, and pays nothing). Line-splitting the HEAD CSV is safe here —
    a WI row is one physical line (no embedded newlines)."""
    staged = _git(root, ["diff", "--cached", "--name-only"])
    if staged is None:
        return []
    staged_names = set(staged.splitlines())
    if WI_CSV not in staged_names:
        return []  # no registry change staged -> nothing was closed here
    head_text = _git(root, ["show", "HEAD:" + WI_CSV])
    if head_text is None:
        return []  # first commit / file not in HEAD
    cur_map = _wi_status_map(read_rows(root / WI_CSV))
    head_map = _wi_status_map(list(csv.DictReader(head_text.splitlines())))

    prev_done_srs = {}  # SR id -> the done WI(s) that already delivered it
    for wid, h in head_map.items():
        if h["status"] == "done":
            for sr in h["srs"]:
                prev_done_srs.setdefault(sr, set()).add(wid)

    followups = []
    for wid, c in cur_map.items():
        was = head_map.get(wid, {}).get("status")
        if c["status"] == "done" and was != "done":
            shared = sorted(sr for sr in c["srs"] if sr in prev_done_srs)
            if shared:
                followups.append((wid, shared))
    if not followups:
        return []

    tests_prefix = _tests_dir(root).rstrip("/") + "/"
    chain_touched = any(f == TC_CSV or f.startswith(tests_prefix) for f in staged_names)
    if chain_touched:
        return []
    return [
        "{}: closes as a follow-up on {} (already delivered by a done WI) but "
        "the change set touches neither {} nor {} — the validation chain did "
        "not change (the fix must land in the chain, not just the code)".format(
            wid, ";".join(shared), TC_CSV, tests_prefix
        )
        for wid, shared in followups
    ]


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--root", default=".", help="repo root (default: current directory)"
    )
    ap.add_argument(
        "--strict",
        action="store_true",
        help="promote the status↔registry coherence rules R-B…R-E from WARN to "
        "ERROR (wired at gate G2+; R-A always fails regardless)",
    )
    ap.add_argument(
        "--staged",
        action="store_true",
        help="run ONLY the warn-first no-validation-delta check over the staged "
        "commit (needs git; a silent no-op outside a git checkout)",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()

    if not read_trajectory_enabled(root):
        print("check_trajectory: off (docs/trajectory-check) — nothing to check.")
        return 0

    # --staged is the commit-time no-validation-delta warn only: never blocks,
    # never re-runs the full validation (the trajectory step already did).
    if args.staged:
        for w in staged_findings(root):
            print("check_trajectory: WARN - {}".format(w), file=sys.stderr)
        return 0

    wis, integrity = load_wis(read_rows(root / WI_CSV))
    if not wis and not integrity:
        print(
            "check_trajectory: clean (no work items — placeholder-only or absent "
            "registry; vacuously clean)."
        )
        return 0

    errors = integrity + validate(wis, load_known_srs(root))
    # The SSOT coherence layer: R-A is always an error; R-B…R-E + the
    # unknown-status lint are WARN unless --strict promotes them.
    for rule, hard, msg in ssot_findings(wis, root):
        line = "{} {}".format(rule, msg)
        if hard or args.strict:
            errors.append(line)
        else:
            print("check_trajectory: WARN - {}".format(line), file=sys.stderr)
    if errors:
        for e in errors:
            print("check_trajectory: ERROR - {}".format(e), file=sys.stderr)
        print(
            "check_trajectory: {} error(s) in {}.".format(len(errors), WI_CSV),
            file=sys.stderr,
        )
        return 1

    done = sum(1 for w in wis if w["status"] == "done")
    print(
        "check_trajectory: clean ({} work item(s), {} done ({}%), graph "
        "acyclic).".format(len(wis), done, round(100 * done / len(wis)))
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
