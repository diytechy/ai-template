#!/usr/bin/env python3
"""Derive the active gate from artifact states — the hybrid, cached gate.

Stack-agnostic, standard-library only. This replaces the hand-set `docs/gate`
marker with one *computed* from the spine's own maturity states
(docs/specs/derived-gate-model.md): **the repo is at gate G iff every in-scope
SN/SR/LLR/TC meets G's bar.** SSOT applied to the gate itself — you no longer bump
a line, you ratify artifacts (in a reviewed commit) and the gate follows.

The model is **hybrid**: the computed value is *cached* to `docs/gate` (now a
generated file) with a compute date, so the gate is known on checkout with no
recompute; `--check` recomputes and guards the cache against rot, the same
freshness discipline the kit already runs for the arch-map / OKF / dashboard.
`check.py`'s `resolve_gate()` still reads the first non-comment line of
`docs/gate` — the value is simply derived now, not declared.

Per-artifact gate (docs/specs/derived-gate-model.md §3), on the ladder
G0 < G1 < G2 < G3:
  - **SN** — Draft (under a stakeholder-needs.md heading containing "draft",
    section-as-state §4a) => G0; ratified => it has no obligation past G1, so it
    never caps the repo (contributes G3 to the min).
  - **SR** — Draft (Status) => G0; ratified but not decomposed => G1; decomposed
    (has its required LLR — unless the Verification is LLR-exempt
    Analysis/Inspection/Attest — AND a TC) => G2; decomposed AND Status=Verified
    => G3.
  - **LLR / TC** — Draft => G0 (the new-phase signal). Once present, its Status
    does not independently gate: the SR's Verified status drives G2->G3 (matching
    trace.py's --require-verified, which checks SRs, not LLR/TC status), so a
    present LLR/TC never caps below G3.

Aggregation: the repo gate = **min over all in-scope artifacts** (a phase gate is
the min over that phase's artifacts; the repo gate is the min over phases, which
is the same set — also reported per-phase). A repo with **no** real SRs yet (a
fresh scaffold) is at **G1** (the requirements-drafting start), never a vacuous
G3. A draft artifact is at G0, so introducing draft/reopened content **drops** the
derived gate — the signal that a new phase is due (the `[phase]-[g*]` detector
lives in check_trajectory). The cached runnable value is floored at G1 (check.py's
gate vocabulary is G1..G3); the raw computed level, including a G0 drop, is
recorded in the `# basis:` comment so nothing hides.

This script reads STATES and picks the LEVEL; `trace.py` (run by check.py at that
level) ENFORCES the structure — orphans/decomposition/verified — at the derived
gate. The two compose: a draft is exempt from trace's orphan rule (so it can live
in the live spine) yet sits at G0 here (so it drops the gate). Auditing
correctness is the whole point, so every rule is fixture-tested.

Note: the derived range is G1..G3 (the SN/SR/LLR/TC-derivable gates). G-Release /
G-Final are release milestones beyond the spine and stay separately recorded.

Usage:
    python scripts/derive_gate.py [--root .] [--docs DIR]   # compute + write docs/gate
    python scripts/derive_gate.py --check                    # recompute + guard rot (exit 1 on drift)
    python scripts/derive_gate.py --print                    # compute + print, do not write

Small CSV/heading loaders below are duplicated from trace.py per the kit's
independently-copyable-script convention (the F5 rule) — derive_gate.py stays a
self-contained drop-in, never importing the joined-spine engine.

Contracts: IF-050, IF-051 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import datetime
import re
import subprocess
import sys
from pathlib import Path

# The derived ladder. G0 = pre-ratification (draft); G1..G3 are the runnable gates
# check.py knows. GATE_NAMES maps the internal int back to the marker string.
G0, G1, G2, G3 = 0, 1, 2, 3
GATE_NAMES = {G0: "G0", G1: "G1", G2: "G2", G3: "G3"}

# SR Verification methods with no code to decompose, so they need a TC but no LLR
# (kept in sync with trace.py's orphan rule — Critique is NOT here: its artifact
# is produced by code, only its acceptance is subjective).
LLR_EXEMPT = {"Analysis", "Inspection", "Attest"}

GATE_FILE = "docs/gate"


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is (the same
    guard as trace.py / check.py — a non-ASCII path can't wedge a cp1252 console)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# --- small self-contained loaders (duplicated from trace.py per the F5 rule) ---
def load_csv(path):
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def refs(value):
    """Split a multi-ref cell (';', ',' or whitespace separated) into ids."""
    return [t for t in re.split(r"[;,\s]+", (value or "").strip()) if t]


def is_example(rid):
    return (rid or "").endswith("-000")


def is_draft(row):
    """A row in the pre-ratification `Draft` state (open-vocab Status)."""
    return (row.get("Status") or "").strip().lower() == "draft"


_HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.*)")


def sn_draft_ids(text):
    """Draft SN ids (section-as-state §4a): every SN-### under a heading whose text
    contains "draft". `-000` excluded. Duplicated from trace.py per the F5 rule."""
    draft, in_draft = set(), False
    for line in text.splitlines():
        m = _HEADING_RE.match(line)
        if m:
            in_draft = "draft" in m.group(1).lower()
            continue
        if in_draft:
            for u in re.findall(r"\bSN-\d+\b", line):
                if not is_example(u):
                    draft.add(u)
    return draft


# --- per-artifact gate rules (docs/specs/derived-gate-model.md §3) -------------
def sr_gate(sr, has_llr, has_tc):
    """The gate an SR row has reached, from its Status + whether it is decomposed."""
    if is_draft(sr):
        return G0
    exempt = (sr.get("Verification") or "").strip() in LLR_EXEMPT
    decomposed = (exempt or has_llr) and has_tc
    verified = (sr.get("Status") or "").strip() == "Verified"
    if decomposed and verified:
        return G3
    if decomposed:
        return G2
    return G1  # a ratified requirement not yet decomposed


def maturity_gate(row):
    """An LLR/TC caps the gate only when it is Draft (G0 — the new-phase signal).
    Once present, its own Status does NOT independently gate G3: the SR's Verified
    status drives G2->G3 (matching trace.py's --require-verified bar, which checks
    SRs, not LLR/TC status), and the LLR/TC's *existence* is what makes its SR
    decomposed (G2, decided in sr_gate). So a present LLR/TC contributes G3 and
    never caps — a downstream repo whose LLRs read `Implemented` still reaches G3
    on its SRs, exactly as trace.py's gate does."""
    return G0 if is_draft(row) else G3


def sn_gate(sn_id, draft_ids):
    """A Draft SN (section-as-state) is G0; a ratified SN has no obligation past G1
    and so never caps the repo (contributes G3 to the min)."""
    return G0 if sn_id in draft_ids else G3


def compute(docs):
    """Derive the gate from the spine registries under `docs`. Returns a result
    dict: counts, the raw computed level (may be G0), the per-phase breakdown, and
    the runnable gate name (raw floored to G1)."""
    raw_srs = load_csv(docs / "requirements" / "system-requirements.csv")
    raw_llrs = load_csv(docs / "requirements" / "low-level-requirements.csv")
    raw_tcs = load_csv(docs / "test" / "test-cases.csv")
    srs = [r for r in raw_srs if r.get("SR-ID") and not is_example(r["SR-ID"])]
    llrs = [r for r in raw_llrs if r.get("LLR-ID") and not is_example(r["LLR-ID"])]
    tcs = [r for r in raw_tcs if r.get("TC-ID") and not is_example(r["TC-ID"])]

    sn_md = docs / "requirements" / "stakeholder-needs.md"
    sn_ids, sn_draft = set(), set()
    if sn_md.exists():
        text = sn_md.read_text(encoding="utf-8")
        sn_ids = {u for u in re.findall(r"\bSN-\d+\b", text) if not is_example(u)}
        sn_draft = sn_draft_ids(text)

    # The joins the SR gate needs: which SRs have an LLR, which SR/LLR ids have a TC.
    llr_sr_refs = {x for r in llrs for x in refs(r.get("SR-Refs"))}
    tc_refs = {x for r in tcs for x in refs(r.get("Verifies"))}

    sr_g = {
        r["SR-ID"]: sr_gate(r, r["SR-ID"] in llr_sr_refs, r["SR-ID"] in tc_refs)
        for r in srs
    }
    llr_g = {r["LLR-ID"]: maturity_gate(r) for r in llrs}
    tc_g = {r["TC-ID"]: maturity_gate(r) for r in tcs}
    sn_g = {u: sn_gate(u, sn_draft) for u in sn_ids}

    n_draft = (
        sum(1 for r in srs if is_draft(r))
        + sum(1 for r in llrs if is_draft(r))
        + sum(1 for r in tcs if is_draft(r))
        + len(sn_draft)
    )

    # Aggregation. A repo with no real SRs yet is at G1 (requirements-drafting),
    # never a vacuous G3 from ratified-SN-only. Otherwise the raw level is the min
    # over every in-scope artifact's gate (SN drafts, SR maturity, LLR/TC maturity).
    if not srs:
        raw = G1
    else:
        raw = min(
            [sr_g[k] for k in sr_g]
            + [sn_g[k] for k in sn_g]
            + [llr_g[k] for k in llr_g]
            + [tc_g[k] for k in tc_g]
        )

    per_phase = _per_phase(srs, sr_g, llrs, tcs)

    return {
        "counts": {"SN": len(sn_ids), "SR": len(srs), "LLR": len(llrs), "TC": len(tcs)},
        "drafts": n_draft,
        "raw": raw,
        "per_phase": per_phase,
        "gate": GATE_NAMES[max(G1, raw)],  # the runnable value (floored to G1)
    }


def _per_phase(srs, sr_g, llrs, tcs):
    """`{phase-label: gate-name}` — the SRs grouped by their optional `Phase` column
    (blank => "(default)"), each phase's gate the min over its SRs and the LLR/TC
    that decompose/verify them. Reporting-only here; the phase-drop detector and
    the `[phase]-[g*]` archetype live in check_trajectory (WI-093)."""
    llr_by_sr = {}
    for r in llrs:
        for s in refs(r.get("SR-Refs")):
            llr_by_sr.setdefault(s, []).append(maturity_gate(r))
    tc_by_ref = {}
    for r in tcs:
        for s in refs(r.get("Verifies")):
            tc_by_ref.setdefault(s, []).append(maturity_gate(r))

    phases = {}
    for r in srs:
        label = (r.get("Phase") or "").strip() or "(default)"
        sid = r["SR-ID"]
        gates = [sr_g[sid]] + llr_by_sr.get(sid, []) + tc_by_ref.get(sid, [])
        phases.setdefault(label, []).extend(gates)
    return {
        label: GATE_NAMES[max(G1, min(gs))] if gs else GATE_NAMES[G1]
        for label, gs in sorted(phases.items())
    }


def _git(root, args):
    """`git -C root <args>` stdout on success, else None (git absent / not a repo)."""
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
    return proc.stdout.strip() if proc.returncode == 0 else None


def basis_line(result):
    """The single, deterministic `# basis:` comment line compared by --check
    (the counts + raw computed level + per-phase breakdown — everything that must
    stay in step with the states, excluding the volatile compute date)."""
    c = result["counts"]
    per_phase = ";".join(f"{k}={v}" for k, v in result["per_phase"].items())
    return (
        "# basis: SN={SN} SR={SR} LLR={LLR} TC={TC} drafts={d} computed={raw} "
        "per-phase={pp}".format(
            SN=c["SN"],
            SR=c["SR"],
            LLR=c["LLR"],
            TC=c["TC"],
            d=result["drafts"],
            raw=GATE_NAMES[result["raw"]],
            pp=per_phase or "(none)",
        )
    )


HEADER = [
    "# DERIVED GATE — generated by scripts/derive_gate.py (do not hand-edit).",
    "#",
    "# The active gate is COMPUTED from artifact states, not declared",
    "# (docs/specs/derived-gate-model.md): the repo is at gate G iff every in-scope",
    "# SN/SR/LLR/TC meets G's bar. You advance it by RATIFYING artifacts in a",
    "# reviewed commit (Draft->Planned, or moving an SN out of a draft section),",
    "# not by editing this line. Regenerate: python scripts/derive_gate.py",
    "# Freshness is guarded by `--check` (a pre-commit + gate step). check.py / CI",
    "# read the first non-comment line below, exactly as before.",
    "#",
]


def render_cache(result, as_of, date):
    """The full docs/gate file text: static header, the compared `# basis:` line,
    the informational (never-compared) compute stamp, then the runnable gate."""
    lines = list(HEADER)
    lines.append(basis_line(result))
    lines.append("# computed {} (as-of {})".format(date, as_of))
    lines.append(result["gate"])
    return "\n".join(lines) + "\n"


def parse_cache(text):
    """`(gate_value, basis_line)` from a cached docs/gate: the first non-comment
    line, and the `# basis:` comment. Either may be None (a legacy hand-set gate
    file has no basis line — --check then reports it as needing the first compute)."""
    gate, basis = None, None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# basis:"):
            basis = s
        elif s and not s.startswith("#") and gate is None:
            gate = s
    return gate, basis


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--docs", default=None, help="docs directory (default: <root>/docs)"
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="recompute and compare to the cached docs/gate; exit 1 on drift "
        "(the gate value or the basis moved but the cache did not)",
    )
    ap.add_argument(
        "--print",
        dest="print_only",
        action="store_true",
        help="compute and print the derived gate + basis; do not write docs/gate",
    )
    args = ap.parse_args()
    root = Path(args.root)
    docs = Path(args.docs) if args.docs else root / "docs"

    result = compute(docs)
    basis = basis_line(result)

    if args.print_only:
        print(basis)
        print("derived gate: {}".format(result["gate"]))
        return 0

    gate_path = root / GATE_FILE
    if args.check:
        if not gate_path.exists():
            print(
                "derive_gate: {} is absent — run `python scripts/derive_gate.py` "
                "to generate it".format(GATE_FILE),
                file=sys.stderr,
            )
            return 1
        cached_gate, cached_basis = parse_cache(
            gate_path.read_text(encoding="utf-8", errors="replace")
        )
        # A legacy, hand-set docs/gate has no `# basis:` line (pre-migration). Then
        # --check compares only the VALUE (so the meta + fresh scaffolds stay green
        # until the one-time migration runs derive_gate); a value mismatch is still
        # a hard fail. Once migrated (basis present), the full rot guard applies.
        if cached_basis is None:
            if cached_gate == result["gate"]:
                print(
                    "derive_gate: {} value OK ({}) but not yet in derived form — run "
                    "`python scripts/derive_gate.py` once to migrate.".format(
                        GATE_FILE, result["gate"]
                    ),
                    file=sys.stderr,
                )
                return 0
            print(
                "derive_gate: {} STALE — hand-set {} but the derived gate is {}.\n"
                "  run `python scripts/derive_gate.py` and commit the result.".format(
                    GATE_FILE, cached_gate, result["gate"]
                ),
                file=sys.stderr,
            )
            return 1
        if cached_gate == result["gate"] and cached_basis == basis:
            print("derive_gate: {} up to date ({}).".format(GATE_FILE, result["gate"]))
            return 0
        print(
            "derive_gate: {} STALE — the derived gate moved but the cache did not.\n"
            "  cached: gate={} basis={!r}\n"
            "  now:    gate={} basis={!r}\n"
            "  run `python scripts/derive_gate.py` and commit the result.".format(
                GATE_FILE, cached_gate, cached_basis, result["gate"], basis
            ),
            file=sys.stderr,
        )
        return 1

    as_of = _git(root, ["rev-parse", "--short", "HEAD"]) or "no-git"
    date = (
        _git(root, ["log", "-1", "--format=%cs"]) or datetime.date.today().isoformat()
    )
    gate_path.parent.mkdir(parents=True, exist_ok=True)
    gate_path.write_text(render_cache(result, as_of, date), encoding="utf-8")
    print("derive_gate: wrote {} -> {} ({}).".format(GATE_FILE, result["gate"], basis))
    return 0


if __name__ == "__main__":
    sys.exit(main())
