#!/usr/bin/env python3
"""Derive the dependency-ready WI frontier and its deterministic schedule.

Stack-agnostic, standard-library only (Python 3.8+, Windows/POSIX). This is the
scheduler contract of the parallel-WI-dispatch work (Slice A;
docs/specs/parallel-wi-dispatch.md SR-057/SR-058). It is a **pure, side-effect-free
library + CLI** shared by validation, the dashboard, the dispatcher, and tests —
it never mutates the registry, spawns a worker, or touches git. Readiness is
DERIVED from the tracked WI registry (`docs/requirements/work-items.csv`) plus any
dispatcher reservations the caller passes in; it is never copied into prose.

Two contracts live here:

  * **Frontier + deterministic order (SR-057).** A queued WI is *ready* when every
    hard predecessor is integrated `done` (soft `~` edges never block). The ready
    set excludes `blocked`/`deferred`/reserved WIs and any WI the safety
    classifier deems ineligible, then orders the survivors by
    `(gate class, Priority desc, transitive downstream-dependent count desc,
    remaining hard-path length desc, WI id)`.

  * **Deterministic safety classification (SR-058).** One pure classifier maps a
    WI's declared `SafetyClass` (`ordinary|spine|gate|attestation|protected|
    high-risk`) plus review/critique policy and structural evidence to a
    scheduling class + reason codes. `spine|gate|attestation` serialize
    whole-project; `protected` serializes whole-project; `high-risk`, a critique
    requirement, an integration checkpoint, or a registry `PlanMode=dual` signal
    (SR-066 — derived from the signal itself, never a second hand-set cell; a
    contradicting declared SafetyClass quarantines) force a single-WI traincar; only
    classified `ordinary` work packs optimistically; anything missing, unknown, or
    contradicting its structural evidence returns `unclassified`, which **fails
    closed** (never scheduled) for that WI without stopping disjoint classified
    work.

The optional schema columns (`Priority`, `Exclusive`, `BlockRef`, `EstTokens`,
`SafetyClass`) are read via `DictReader`, so a legacy registry without them reads
every value as its documented default — `Priority=0`, empty `Exclusive`,
`SafetyClass` absent => `unclassified` (empty is never silently `ordinary`).

Usage:
    python scripts/schedule.py ready [--explain] [--format text|json] [--root .]
    python scripts/schedule.py simulate --jobs N [--root .] [--format text|json]

Small CSV loaders are duplicated from trace.py / check_trajectory.py per the kit's
independently-copyable-script convention (the F5 rule): schedule.py stays a
self-contained drop-in, never importing the sibling engines.

Contracts: IF-053, IF-054 — the interface seams this module declares (process.md
§8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

WI_ID_RE = re.compile(r"^WI-\d+$")
REGISTRY = "docs/requirements/work-items.csv"

# --- safety classification vocabulary (SR-058; spec §4 "Deterministic safety
# classification"). The DECLARED values a WI may carry in its SafetyClass cell. ---
SAFETY_CLASSES = ("ordinary", "spine", "gate", "attestation", "protected", "high-risk")

# Scheduling classes the classifier RETURNS (distinct from the declared vocabulary).
SCHED_SPINE_SERIAL = "spine-serial"  # spine/gate/attestation — serial, whole-project
SCHED_PROTECTED = "protected-serial"  # protected — serial, whole-project
SCHED_SINGLE_WI = "single-wi"  # high-risk / critique / checkpoint — own traincar
SCHED_ORDINARY = "ordinary"  # optimistic multi-WI packing eligible
SCHED_UNCLASSIFIED = "unclassified"  # fail closed — never scheduled

# Lowest-gate-first ordering rank (spec §4 step 4): the most gate-constraining
# work sorts first. unclassified is excluded from the frontier, so its rank only
# matters for a stable total order in --explain output.
_GATE_RANK = {
    SCHED_SPINE_SERIAL: 0,
    SCHED_PROTECTED: 1,
    SCHED_SINGLE_WI: 2,
    SCHED_ORDINARY: 3,
    SCHED_UNCLASSIFIED: 4,
}

# Tracked Status vocabulary (spec §3.1). Anything other than `done` is not-ready;
# `blocked`/`deferred`/reserved carry their own disposition (never silently
# scheduled) — the same fail-closed spirit.
_DONE = "done"


def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (the trace.py/check.py guard)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# --- small self-contained loaders (duplicated per the F5 rule) ----------------
def load_rows(path):
    if not Path(path).exists():
        return []
    with Path(path).open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def _split_refs(value):
    """Split a `;`/`,`/whitespace-separated ref cell into tokens."""
    return [t for t in re.split(r"[;,\s]+", (value or "").strip()) if t]


def _int(value, default=0):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


def load_wis(rows):
    """Parse work-item rows into a list of scheduler WI dicts (skips the inert
    `-000` example row and any malformed/duplicate id, exactly like
    check_trajectory.load_wis — a broken registry is the validator's job to
    report, not the scheduler's to crash on)."""
    wis, seen = [], set()
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if not wid.startswith("WI-") or not WI_ID_RE.match(wid) or wid in seen:
            continue
        seen.add(wid)
        if wid.endswith("-000"):
            continue
        preds, soft = [], []
        for p in _split_refs(r.get("Predecessors", "")):
            (soft if p.startswith("~") else preds).append(p.lstrip("~"))
        wis.append(
            {
                "id": wid,
                "title": (r.get("Title") or "").strip(),
                "status": (r.get("Status") or "queued").strip().lower(),
                "preds": preds,
                "soft": soft,
                "srs": _split_refs(r.get("SR-Refs", "")),
                "priority": _int(r.get("Priority"), 0),
                "exclusive": _split_refs(r.get("Exclusive", "")),
                "blockref": (r.get("BlockRef") or "").strip(),
                "est_tokens": _int(r.get("EstTokens"), 0),
                "safetyclass": (r.get("SafetyClass") or "").strip().lower(),
                "planmode": (r.get("PlanMode") or "").strip().lower(),
            }
        )
    return wis


# --- deterministic safety classification (SR-058) -----------------------------
def classify(wi, *, structural=None):
    """`(scheduling_class, [reason_codes])` for one WI — a pure function.

    Inputs (spec §4): the declared `SafetyClass`, a critique/integration-checkpoint
    requirement (read off the WI's flags), the registry `PlanMode` signal, and
    optional `structural` evidence (the class the repository graph implies,
    supplied by the validator). Ordered rules:

      0. PlanMode=dual -> single-WI traincar, DERIVED from the signal itself
         (SR-066/WI-201: never a second hand-set cell; a declared SafetyClass
         other than empty or high-risk contradicts and quarantines unclassified)
      1. spine/gate/attestation  -> serial whole-project (never a multi-WI traincar)
      2. protected               -> serial whole-project
      3. high-risk / critique / integration-checkpoint -> single-WI traincar
      4. ordinary                -> optimistic multi-WI packing
      5. missing / unknown / contradicting structural evidence -> unclassified
         (fails closed for this WI; disjoint classified work is unaffected)

    The cross-check (rule 5) fails closed when a WI DECLARES `ordinary` but the
    structural evidence says spine/gate/attestation/protected/high-risk — a
    mis-declaration is never silently upgraded, it is quarantined as unclassified.
    """
    declared = (wi.get("safetyclass") or "").strip().lower()
    critique = bool(wi.get("critique"))
    checkpoint = bool(wi.get("checkpoint"))

    # PlanMode=dual derives the single-WI-traincar class FROM THE SIGNAL ITSELF
    # (SR-066, the WI-201 ruling): a dual-plan round is never packed with other
    # WIs and never needs a second hand-set SafetyClass cell (single-source). A
    # declared SafetyClass that contradicts the derivation (anything whose own
    # scheduling class is not single-wi) quarantines as unclassified — the same
    # cross-check posture as rule 5, never a silent override in either direction.
    dual = (wi.get("planmode") or "").strip().lower() == "dual"
    if dual and declared and declared != "high-risk":
        return SCHED_UNCLASSIFIED, [
            "unclassified:planmode-dual-vs-declared-%s" % declared
        ]

    if not dual and declared not in SAFETY_CLASSES:
        code = "missing" if not declared else "unknown-value:%s" % declared
        return SCHED_UNCLASSIFIED, ["unclassified:%s" % code]

    struct = (structural or "").strip().lower() or None
    if declared == "ordinary" and struct in SAFETY_CLASSES and struct != "ordinary":
        return SCHED_UNCLASSIFIED, [
            "unclassified:declared-ordinary-vs-structural-%s" % struct
        ]

    if declared in ("spine", "gate", "attestation"):
        return SCHED_SPINE_SERIAL, ["serial-whole-project:%s" % declared]
    if declared == "protected":
        return SCHED_PROTECTED, ["serial-whole-project:protected"]
    if dual or declared == "high-risk" or critique or checkpoint:
        reasons = ["single-wi:dual-plan"] if dual else []
        if declared == "high-risk":
            reasons.append("single-wi:high-risk")
        if critique:
            reasons.append("single-wi:critique")
        if checkpoint:
            reasons.append("single-wi:integration-checkpoint")
        return SCHED_SINGLE_WI, reasons
    return SCHED_ORDINARY, ["ordinary:optimistic-packing-eligible"]


def is_schedulable_class(sched_class):
    """Only a positively-classified WI is eligible; unclassified fails closed."""
    return sched_class != SCHED_UNCLASSIFIED


# --- graph derivations (SR-057) ----------------------------------------------
def _by_id(wis):
    return {w["id"]: w for w in wis}


def _status(wis):
    return {w["id"]: w["status"] for w in wis}


def hard_preds_satisfied(wi, status):
    """Every hard predecessor is integrated `done`. An unknown predecessor id
    (dangling edge — the validator's error) counts as NOT satisfied, so the
    scheduler fails closed rather than scheduling on a broken graph."""
    return all(status.get(p) == _DONE for p in wi["preds"])


def _hard_children(wis):
    """`{id: [hard-successor ids]}` — the hard-edge adjacency both graph
    derivations below walk (shared so the map is built once, one way)."""
    children = {w["id"]: [] for w in wis}
    ids = set(children)
    for w in wis:
        for p in w["preds"]:
            if p in ids:
                children[p].append(w["id"])
    return children


def downstream_counts(wis):
    """`{id: transitive hard-descendant count}` — how many distinct WIs depend on
    this one through hard edges (the unblocking-value signal in the order key)."""
    children = _hard_children(wis)
    out = {}

    def reach(wid, seen):
        for c in children[wid]:
            if c not in seen:
                seen.add(c)
                reach(c, seen)
        return seen

    for wid in children:
        out[wid] = len(reach(wid, set()))
    return out


def hard_path_lengths(wis):
    """`{id: remaining hard-path length}` — the longest chain of hard descendants
    from this WI to a terminal (critical-path signal). Iterative memoized DFS."""
    children = _hard_children(wis)
    memo = {}

    def depth(wid, stack):
        if wid in memo:
            return memo[wid]
        if wid in stack:  # a cycle — the validator's error; bound it at 0 here
            return 0
        stack.add(wid)
        best = 0
        for c in children[wid]:
            best = max(best, 1 + depth(c, stack))
        stack.discard(wid)
        memo[wid] = best
        return best

    return {wid: depth(wid, set()) for wid in children}


def order_key(wi, sched_class, downstream, hardpath):
    """The deterministic sort key (spec §4 step 6): lowest gate class first, then
    the human Priority override, then structural criticality, then WI id."""
    return (
        _GATE_RANK.get(sched_class, _GATE_RANK[SCHED_UNCLASSIFIED]),
        -wi["priority"],
        -downstream,
        -hardpath,
        wi["id"],
    )


def evaluate(wis, reserved=None):
    """Classify every WI and compute its readiness disposition — the one pass the
    frontier, --explain, and simulate all share. Returns a list of records dicts,
    one per WI, ordered by the deterministic key. `reserved` is an optional set of
    WI ids already claimed by a live train (excluded from the ready frontier)."""
    reserved = set(reserved or ())
    status = _status(wis)
    downstream = downstream_counts(wis)
    hardpath = hard_path_lengths(wis)
    exclusive_ready = _exclusive_conflicts(wis, status, reserved)

    records = []
    for w in wis:
        sched_class, class_reasons = classify(w)
        disposition, reasons = _disposition(
            w, status, reserved, sched_class, class_reasons, exclusive_ready
        )
        records.append(
            {
                "id": w["id"],
                "status": w["status"],
                "sched_class": sched_class,
                "disposition": disposition,
                "priority": w["priority"],
                "downstream": downstream[w["id"]],
                "hard_path": hardpath[w["id"]],
                "exclusive": w["exclusive"],
                "reasons": reasons,
                "_key": order_key(
                    w, sched_class, downstream[w["id"]], hardpath[w["id"]]
                ),
            }
        )
    records.sort(key=lambda r: r["_key"])
    for r in records:
        del r["_key"]
    return records


def _exclusive_conflicts(wis, status, reserved):
    """`{exclusive-key: winning WI id}` — among the WIs that would otherwise be
    ready and share a non-empty `Exclusive` key, the deterministically-first one
    (by id) wins the key; the rest are exclusive-conflicting. A key held by a
    reserved/active WI is owned by it."""
    holders = {}
    # A reserved WI owns each of its keys outright.
    for w in wis:
        if w["id"] in reserved:
            for k in w["exclusive"]:
                holders.setdefault(k, w["id"])
    # Otherwise the first ready WI (lowest id) claims each contested key.
    candidates = sorted(
        (
            w
            for w in wis
            if w["status"] == "queued"
            and w["id"] not in reserved
            and hard_preds_satisfied(w, status)
        ),
        key=lambda w: w["id"],
    )
    for w in candidates:
        for k in w["exclusive"]:
            holders.setdefault(k, w["id"])
    return holders


def _disposition(wi, status, reserved, sched_class, class_reasons, exclusive_ready):
    """`(disposition, [reason_codes])` for one WI: ready | waiting | reserved |
    blocked | deferred | done | excluded. The reason list is the disposition's own
    codes; the classifier's reason is carried only where classification decides the
    outcome (`ready` shows why eligible, `unclassified` shows the fail-closed
    cause) — never as noise on a blocked/deferred/reserved/waiting item."""
    st = wi["status"]
    if st == _DONE:
        return "done", ["done:integrated"]
    if st == "blocked":
        return "blocked", ["excluded:blocked:%s" % (wi["blockref"] or "no-blockref")]
    if st == "deferred":
        return "deferred", ["excluded:deferred"]
    if wi["id"] in reserved:
        return "reserved", ["reserved:claimed-by-live-train"]
    if not hard_preds_satisfied(wi, status):
        unmet = [p for p in wi["preds"] if status.get(p) != _DONE]
        return "waiting", ["waiting:hard-preds-not-done:%s" % ",".join(unmet)]
    if not is_schedulable_class(sched_class):
        return "excluded", list(class_reasons) + ["excluded:unclassified-fail-closed"]
    # Exclusive-key conflict: another WI owns a key this one needs.
    for k in wi["exclusive"]:
        owner = exclusive_ready.get(k)
        if owner and owner != wi["id"]:
            return "excluded", ["excluded:exclusive-conflict:%s@%s" % (k, owner)]
    return "ready", list(class_reasons) + ["ready"]


def frontier(wis, reserved=None):
    """The ordered ready frontier: records whose disposition is `ready`."""
    return [r for r in evaluate(wis, reserved) if r["disposition"] == "ready"]


def simulate(wis, jobs, reserved=None):
    """Greedy list-scheduling simulation over the hard DAG: each round assigns up
    to `jobs` ready WIs (in the deterministic order), marks them integrated, and
    rescans — the shape the dispatcher's dynamic refill produces. Returns a list
    of rounds, each a list of assigned WI ids. `--jobs 1` yields the serial order.

    This is a planning aid: it treats an assigned WI as immediately `done` and
    does not model build time, reservations beyond the initial set, or traincar
    continuation (those are the dispatcher's runtime concerns, Slices D/E)."""
    if jobs < 1:
        raise ValueError("jobs must be >= 1")
    # Work on shallow copies so the caller's WIs are never mutated.
    work = [dict(w) for w in wis]
    reserved = set(reserved or ())
    rounds = []
    guard = len(work) + 1
    while guard >= 0:
        guard -= 1
        ready = [r["id"] for r in frontier(work, reserved)]
        if not ready:
            break
        assigned = ready[:jobs]
        rounds.append(assigned)
        done = set(assigned)
        for w in work:
            if w["id"] in done:
                w["status"] = _DONE
    return rounds


# --- CLI ----------------------------------------------------------------------
def _load(root):
    return load_wis(load_rows(Path(root) / REGISTRY))


def _cmd_ready(args):
    wis = _load(args.root)
    if args.explain:
        records = evaluate(wis)
    else:
        records = frontier(wis)
    if args.format == "json":
        print(json.dumps(records, indent=2, sort_keys=True))
        return 0
    if not records:
        print(
            "schedule: no ready work items"
            if not args.explain
            else "schedule: (empty registry)"
        )
        return 0
    for r in records:
        if args.explain:
            display = dict(r)
            display["reasons"] = ";".join(r["reasons"])
            print(
                "{id:<10} {disposition:<9} {sched_class:<14} "
                "P{priority:<3} down={downstream:<3} path={hard_path:<3} {reasons}".format(
                    **display
                )
            )
        else:
            print(
                "{id:<10} {sched_class:<14} P{priority} down={downstream} "
                "path={hard_path}".format(**r)
            )
    return 0


def _cmd_simulate(args):
    wis = _load(args.root)
    rounds = simulate(wis, args.jobs)
    if args.format == "json":
        print(json.dumps({"jobs": args.jobs, "rounds": rounds}, indent=2))
        return 0
    if not rounds:
        print("schedule: nothing to schedule")
        return 0
    for i, rnd in enumerate(rounds, 1):
        print("round {:<3} ({}): {}".format(i, len(rnd), " ".join(rnd)))
    return 0


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    sub = ap.add_subparsers(dest="cmd")

    ready = sub.add_parser("ready", help="print the dependency-ready frontier")
    ready.add_argument(
        "--explain", action="store_true", help="show every WI + reason codes"
    )
    ready.add_argument("--format", choices=("text", "json"), default="text")
    ready.set_defaults(func=_cmd_ready)

    sim = sub.add_parser(
        "simulate", help="greedy list-schedule the frontier over N workers"
    )
    sim.add_argument("--jobs", type=int, default=2, help="worker ceiling (default 2)")
    sim.add_argument("--format", choices=("text", "json"), default="text")
    sim.set_defaults(func=_cmd_simulate)

    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
