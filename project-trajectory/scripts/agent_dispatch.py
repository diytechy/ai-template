#!/usr/bin/env python3
"""The parallel dispatcher + serialized integrator, extracted VERBATIM from
agent_loop.py (WI-218 slice D — a file split, not a rewrite; behaviors, spec
citations, and WI history unchanged).

`dispatch_run` is the WI-182 engine (SR-061; docs/specs/parallel-wi-dispatch.md
§4/§6/§11/§12): reconcile owned trains -> gate -> build-out. It derives the
ready frontier through `schedule`, packs traincars, atomically reserves each
selected traincar's constituent WIs (refs/llm/reservations/*), leases a linked
worktree per train, and runs worker processes — re-launching the sibling
`agent_loop.py` engine per assignment — in parallel up to the ceiling. The
serialized integrator (WI-184, SR-063) composes ready trains onto
refs/heads/llm/integration by CAS only, runs the combined bar on the composed
tree, and publishes the development branch through the durable publish-intent
protocol. Migration gating (SR-065), the blocked/dual-plan dispositions, the
out/dispatch journal/telemetry, and the recovery reconcile all live here.

Stdlib only, Python 3.8+, Windows/POSIX.

Contracts: IF-055, IF-067 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import atexit
import csv
import datetime
import io
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Sibling scripts (the WI-218 split + the S8 routing half). The guard covers an
# in-process import (a test) whose sys.path doesn't yet carry scripts/ — the
# same sanctioned-sibling-import idiom agent_loop uses.
try:
    import agent_route
    import schedule
    from agent_common import (
        EXIT_BLOCKED,
        EXIT_DONE,
        EXIT_NEEDS_HUMAN,
        EXIT_PAUSED,
        EXIT_PREFLIGHT,
        EXIT_STALL,
        EXIT_TRAIN_END,
        EXIT_WAITING,
        TRAIN_BRANCH_PREFIX,
        WI_TOKEN_RE,
        _read_csv_rows,
        _refs,
        _write_runstate,
        acquire_lock,
        blackout_wake,
        git,
        head_sha_full,
        parse_map,
        pause_reason,
        preflight,
        read_declared,
        regenerate_index,
        release_lock,
        stop_banner,
    )
    from plan_runner import PLAN_MODE_DUAL, run_dual_plan_round, wi_plan_mode
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_route
    import schedule
    from agent_common import (
        EXIT_BLOCKED,
        EXIT_DONE,
        EXIT_NEEDS_HUMAN,
        EXIT_PAUSED,
        EXIT_PREFLIGHT,
        EXIT_STALL,
        EXIT_TRAIN_END,
        EXIT_WAITING,
        TRAIN_BRANCH_PREFIX,
        WI_TOKEN_RE,
        _read_csv_rows,
        _refs,
        _write_runstate,
        acquire_lock,
        blackout_wake,
        git,
        head_sha_full,
        parse_map,
        pause_reason,
        preflight,
        read_declared,
        regenerate_index,
        release_lock,
        stop_banner,
    )
    from plan_runner import PLAN_MODE_DUAL, run_dual_plan_round, wi_plan_mode

# The worker ENGINE this dispatcher re-launches per assignment (spawn_worker).
# A worker is an agent_loop.py process; before the WI-218 split this was
# `Path(__file__)` — dispatch_run lived in that file — so the sibling entry
# point is now named explicitly (spec WI-218 "relocation hazard 1").
_ENGINE = Path(__file__).resolve().parent / "agent_loop.py"
# =============================================================================
# WI-182: the parallel dispatcher (SR-061; spec §4/§6/§11/§12)
# =============================================================================
# `--jobs N|auto` (or the AGENT_JOBS env the launchers wire at migration)
# switches agent_loop from the legacy resume loop to the DISPATCHER: derive the
# ready frontier from the WI registry via schedule.py, pack it into traincars,
# reserve each selected traincar's constituent WIs atomically in Git, lease a
# linked worktree per train, and run Slice-C workers in parallel up to the
# ceiling — rescanning for dynamic refill on every worker exit. Reservations
# and train branches are the DURABLE state (out/dispatch/ is a rebuildable
# journal/cache, spec §11); a built train parks ready-to-integrate with its
# reservations held until the integrator (Slice F) advances the durable
# disposition, so nothing is double-run even across dispatcher restarts.

RESERVATION_NS = "refs/llm/reservations/"


# WI-232: a needs-re-review source conflict is HUMAN work (option (b)) — the
# dispatcher cannot resolve it, so it records the conflict's merge inputs (the
# train tip + the integration head it composed against) and the conflicted paths
# under this durable ref namespace. A relaunch whose inputs are UNCHANGED skips
# re-attempting the identical 3-way merge (the idempotence guard) and pages the
# human; inputs that changed (a new integration head or an amended train) retry
# once. Git-durable like the reservation/train refs — the out/dispatch/ journal
# is a cache, never authority (§11).
CONFLICT_NS = "refs/llm/conflict/"


DISPATCH_DIR = "out/dispatch"


# A worker that rate-limited (exit 5) is retried after this cooldown.
TRAIN_RETRY_SECONDS = 300


# WI-185 (SR-064): the fault-injection hook the crash matrix drives. Setting
# AGENT_FAULT_POINT=<point> hard-kills the dispatcher (os._exit, no cleanup,
# no atexit — a real crash) the first time execution reaches that named
# lifecycle boundary. Production runs never set it; recovery must reconstruct
# from Git alone afterwards.
FAULT_EXIT = 86


def _fault(point):
    if os.environ.get("AGENT_FAULT_POINT", "") == point:
        print("FAULT-INJECTED: {}".format(point), flush=True)
        os._exit(FAULT_EXIT)


def list_reservations(root):
    """{WI-ID: reservation-commit-sha} from refs/llm/reservations/* — the
    durable claims. Empty on error (a broken git surfaces elsewhere)."""
    code, out = git(
        root,
        "for-each-ref",
        "--format=%(refname)%09%(objectname)",
        RESERVATION_NS.rstrip("/"),
    )
    claims = {}
    if code != 0:
        return claims
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) == 2 and parts[0].startswith(RESERVATION_NS):
            wid = parts[0][len(RESERVATION_NS) :]
            if WI_TOKEN_RE.match(wid):
                claims[wid] = parts[1]
    return claims


def reservation_meta(root, sha):
    """The metadata JSON a reservation commit carries ({train, wis, base}), or
    None when unreadable/malformed — the caller quarantines that claim."""
    code, out = git(root, "log", "-1", "--format=%B", sha)
    if code != 0:
        return None
    try:
        meta = json.loads(out)
    except ValueError:
        return None
    if not isinstance(meta, dict) or not meta.get("train") or not meta.get("wis"):
        return None
    return meta


def reserve_traincar(root, train_id, wis, base):
    """Atomically claim a traincar: ONE off-history metadata commit
    (`git commit-tree` — base tree + base parent, message = the {train, wis,
    base} JSON) and ONE `git update-ref --stdin` transaction creating the
    train branch and every constituent reservation ref with zero-old-value
    checks. If ANY WI is already reserved (or the branch exists) the whole
    transaction fails and nothing is created (SR-061 all-or-none). Returns
    None on success, else the failure text."""
    code, tree = git(root, "rev-parse", base + "^{tree}")
    if code != 0:
        return "cannot resolve base tree for {}: {}".format(base, tree)
    meta = json.dumps(
        {"train": train_id, "wis": list(wis), "base": base}, sort_keys=True
    )
    proc = subprocess.run(
        ["git", "-C", str(root), "commit-tree", tree, "-p", base, "-m", meta],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode != 0:
        return "commit-tree failed: {}".format(proc.stderr.strip())
    commit = proc.stdout.strip()
    _fault("reserve-pre-txn")
    # `create` = an atomic zero-old-value check: the fixed ref name is the
    # uniqueness claim for that WI, and one stdin transaction makes the branch
    # + every constituent ref all-or-none (spec §6).
    lines = ["start", "create {} {}".format(TRAIN_BRANCH_HEADS + train_id, base)]
    for wid in wis:
        lines.append("create {}{} {}".format(RESERVATION_NS, wid, commit))
    lines += ["prepare", "commit"]
    # Bytes, not text mode: Windows text mode would rewrite \n as \r\n and
    # git update-ref --stdin would read "start\r" as an unknown command.
    proc = subprocess.run(
        ["git", "-C", str(root), "update-ref", "--stdin"],
        input=("\n".join(lines) + "\n").encode("utf-8"),
        capture_output=True,
    )
    if proc.returncode != 0:
        return "reservation transaction failed (already claimed?): {}".format(
            proc.stderr.decode("utf-8", "replace").strip()[:300]
        )
    _fault("reserve-post-txn")
    return None


TRAIN_BRANCH_HEADS = "refs/heads/" + TRAIN_BRANCH_PREFIX


def release_reservations(root, wis):
    """Transactionally delete the reservation refs of `wis` (one update-ref
    --stdin transaction — the release-on-early-end rule, SR-062). Returns None
    on success, else the failure text. A no-op on an empty list."""
    wis = [w for w in wis if WI_TOKEN_RE.match(w)]
    if not wis:
        return None
    lines = ["start"]
    for wid in wis:
        lines.append("delete {}{}".format(RESERVATION_NS, wid))
    lines += ["prepare", "commit"]
    proc = subprocess.run(
        ["git", "-C", str(root), "update-ref", "--stdin"],
        input=("\n".join(lines) + "\n").encode("utf-8"),
        capture_output=True,
    )
    if proc.returncode != 0:
        return "release transaction failed: {}".format(
            proc.stderr.decode("utf-8", "replace").strip()[:300]
        )
    return None


def record_conflict(root, tid, tip, ihead, paths):
    """Durably record a needs-re-review conflict's merge inputs (train `tip` +
    the `ihead` it composed against) and conflicted `paths` under
    refs/llm/conflict/<tid> (WI-232). One off-history metadata commit
    (`commit-tree`, message = the JSON), mirroring reserve_traincar; the ref is
    force-set so a retry-with-new-inputs overwrites the prior record. Best-effort
    (a broken git surfaces elsewhere)."""
    meta = json.dumps(
        {"train": tid, "tip": tip, "ihead": ihead or "", "paths": paths},
        sort_keys=True,
    )
    code, tree = git(root, "rev-parse", tip + "^{tree}")
    if code != 0:
        return
    proc = subprocess.run(
        ["git", "-C", str(root), "commit-tree", tree.strip(), "-p", tip, "-m", meta],
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode == 0:
        git(root, "update-ref", CONFLICT_NS + tid, proc.stdout.strip())


def read_conflict(root, tid):
    """The recorded conflict metadata for a train ({train, tip, ihead, paths}),
    or None when the ref is absent/unreadable/malformed."""
    code, sha = git(root, "rev-parse", "--verify", "--quiet", CONFLICT_NS + tid)
    if code != 0 or not sha.strip():
        return None
    code, out = git(root, "log", "-1", "--format=%B", sha.strip())
    if code != 0:
        return None
    try:
        meta = json.loads(out)
    except ValueError:
        return None
    return meta if isinstance(meta, dict) else None


def clear_conflict(root, tid):
    """Delete a train's conflict record — it integrated or moved past the
    conflict. A no-op when the ref is absent."""
    git(root, "update-ref", "-d", CONFLICT_NS + tid)


def _conflict_inputs_match(root, tid, rec):
    """True when the CURRENT merge inputs (train tip + integration head) equal
    those recorded in `rec` — the idempotence guard: an unchanged input pair
    means re-running the identical merge would re-park byte-identically."""
    code, tip = git(root, "rev-parse", TRAIN_BRANCH_PREFIX + tid)
    if code != 0:
        return False
    return rec.get("tip") == tip.strip() and rec.get("ihead") == (
        integration_head(root) or ""
    )


def train_branch_evidence(root, train_id, base):
    """(built, blocked) trailer evidence read off the train BRANCH (not a
    worktree) — usable from the primary checkout for reconcile, the early-end
    release decision, and the blocked-disposition transaction. `built` is a
    set; `blocked` maps WI id -> its committed BlockRef ('' when omitted)."""
    code, tip = git(root, "rev-parse", TRAIN_BRANCH_PREFIX + train_id)
    built, blocked = set(), {}
    if code != 0:
        return built, blocked
    fmt = (
        "T%x09%(trailers:key=WI,valueonly,separator=;)%x09"
        "%(trailers:key=Blocked-WI,valueonly,separator=;)%x09"
        "%(trailers:key=BlockRef,valueonly,separator=;)"
    )
    code, out = git(root, "log", "--format=" + fmt, base + ".." + tip.strip())
    if code != 0:
        return built, blocked
    for line in out.splitlines():
        parts = (line.split("\t")[1:] + ["", "", ""])[:3]
        built.update(
            x.strip() for x in parts[0].split(";") if WI_TOKEN_RE.match(x.strip())
        )
        refs = [t.strip() for t in parts[2].split(";")]
        for j, tok in enumerate(t.strip() for t in parts[1].split(";")):
            if WI_TOKEN_RE.match(tok) and tok not in blocked:
                blocked[tok] = refs[j] if j < len(refs) else ""
    return built, blocked


def worktree_root(root):
    """Where train worktrees live: a sibling directory of the repo
    (`../<repo>-trains/<train-id>`) — outside the repo so a linked worktree
    never nests inside the primary checkout or the disposable out/."""
    root = Path(root).resolve()
    return root.parent / (root.name + "-trains")


def existing_worktrees(root):
    """{branch: worktree-path} parsed from `git worktree list --porcelain`."""
    code, out = git(root, "worktree", "list", "--porcelain")
    trees = {}
    if code != 0:
        return trees
    path = None
    for line in out.splitlines():
        if line.startswith("worktree "):
            path = line[len("worktree ") :].strip()
        elif line.startswith("branch ") and path:
            trees[line[len("branch ") :].strip()] = path
    return trees


def lease_worktree(root, train_id):
    """The linked worktree for a train — reuse the one already checked out on
    its branch (recovery), else `git worktree add`. Returns (path, err)."""
    branch_ref = TRAIN_BRANCH_HEADS + train_id
    trees = existing_worktrees(root)
    if branch_ref in trees:
        return Path(trees[branch_ref]), None
    wt = worktree_root(root) / train_id
    wt.parent.mkdir(parents=True, exist_ok=True)
    code, out = git(root, "worktree", "add", str(wt), TRAIN_BRANCH_PREFIX + train_id)
    if code != 0:
        return None, "worktree add failed for {}: {}".format(train_id, out[:300])
    return wt, None


def train_phase_gate(root, wi_rows, wid):
    """The `{phase}-{gate}` train-id prefix (spec §6): the WI's first SR's
    delivery Phase (or `p0`) + the derived gate cache (or `g0`)."""
    phase = ""
    srs = _refs((wi_rows.get(wid) or {}).get("SR-Refs", ""))
    if srs:
        for r in _read_csv_rows(
            Path(root) / "docs" / "requirements" / "system-requirements.csv"
        ):
            if (r.get("SR-ID") or "").strip() == srs[0]:
                phase = (r.get("Phase") or "").strip()
                break
    gate = read_declared(Path(root) / "docs" / "gate", "").strip().lower() or "g0"
    phase = re.sub(r"[^A-Za-z0-9._-]", "", phase) or "p0"
    return "{}-{}".format(phase, gate)


def pack_traincars(records, wis_by_id, cap=4):
    """Pack the evaluated schedule records into dispatchable traincars —
    resource-constrained list scheduling with conservative clustering (spec
    §7): every ready WI starts its own traincar in the deterministic order;
    an ORDINARY ready WI then absorbs its unary hard-successor chain (each
    successor `ordinary`-classified, all its other hard preds already done,
    single hard successor edge) up to the cap. Protected/single-wi classes
    never join a multi-WI traincar. **Spine packs with spine, never with
    anything else** (WI-204, the SR-058 amendment; owner ruling 2026-07-17
    "drafted together, reviewed together, attested together"): every READY
    spine-serial WI — mutually independent by construction, a ready WI's
    hard preds are all done — clusters into ONE spine-only traincar, which
    then absorbs queued spine-serial WIs whose every hard pred is done or
    already aboard (hard-edge order holds: a member boards only after its
    aboard-preds), chunked at the cap; the whole-project drain and the
    one-active-spine-train dispatch invariants are the caller's and are
    unchanged. Returns a list of {wis, sched_class} dicts in dispatch
    order (spine cars first — they rank first in `records` anyway)."""
    by_id = {r["id"]: r for r in records}
    # children[x] = hard successors of x among tracked WIs
    children = {}
    for w in wis_by_id.values():
        for p in w["preds"]:
            children.setdefault(p, []).append(w["id"])
    consumed = set()
    cars = []

    # --- the spine-only batch (WI-204) -----------------------------------
    # Seed: every ready spine-serial WI, in deterministic record order.
    aboard = []
    aboard_set = set()
    for r in records:
        if (
            r["disposition"] == "ready"
            and r["sched_class"] == schedule.SCHED_SPINE_SERIAL
        ):
            aboard.append(r["id"])
            aboard_set.add(r["id"])
    # Closure: absorb queued spine-serial WIs unlocked by the batch (every
    # hard pred done or aboard). A fixed-point sweep in record order keeps
    # the append topological — a member is appended only after its aboard
    # predecessors, so the worker builds the train in dependency order.
    changed = bool(aboard)
    while changed:
        changed = False
        for r in records:
            if (
                r["id"] in aboard_set
                or r["sched_class"] != schedule.SCHED_SPINE_SERIAL
                or r["disposition"] not in ("ready", "waiting")
            ):
                continue
            wi = wis_by_id.get(r["id"])
            if wi is None or wi["status"] != "queued":
                continue
            if all(
                (wis_by_id.get(p) or {}).get("status") == "done" or p in aboard_set
                for p in wi["preds"]
            ):
                aboard.append(r["id"])
                aboard_set.add(r["id"])
                changed = True
    # The safety cap still applies (spec §7): overflow forms the next spine
    # car(s); a later chunk whose preds ride an earlier one is simply not
    # dispatched until that one integrates (spine serializes whole-project,
    # and each rescan re-derives the cars fresh).
    for i in range(0, len(aboard), cap):
        cars.append(
            {"wis": aboard[i : i + cap], "sched_class": schedule.SCHED_SPINE_SERIAL}
        )
    consumed |= aboard_set

    for r in records:
        if r["disposition"] != "ready" or r["id"] in consumed:
            continue
        car = [r["id"]]
        consumed.add(r["id"])
        if r["sched_class"] == schedule.SCHED_ORDINARY:
            cur = r["id"]
            while len(car) < cap:
                succs = children.get(cur, [])
                if len(succs) != 1:
                    break
                nxt = succs[0]
                nrec = by_id.get(nxt)
                nwi = wis_by_id.get(nxt)
                if (
                    nrec is None
                    or nwi is None
                    or nxt in consumed
                    or nrec["sched_class"] != schedule.SCHED_ORDINARY
                    or nrec["disposition"] not in ("waiting", "ready")
                    or nwi["status"] != "queued"
                ):
                    break
                # Every OTHER hard pred of the successor must already be done
                # (accepted-on-train covers only `cur`, which rides this car).
                others = [p for p in nwi["preds"] if p != cur]
                if any(
                    (wis_by_id.get(p) or {}).get("status") != "done" for p in others
                ):
                    break
                # The successor must itself have a single-successor shape to
                # keep the chain unary (a fork ends the train, spec §7).
                car.append(nxt)
                consumed.add(nxt)
                cur = nxt
        cars.append({"wis": car, "sched_class": r["sched_class"]})
    return cars


class _Journal:
    """The out/dispatch/ runtime journal — a CACHE, never authority (§11).
    Events append before the corresponding external action where possible;
    the manifest is rewritten atomically (temp file + os.replace).

    WI-185: every event is stamped with this dispatcher process's `run` id so
    telemetry aggregates by `(run, train, WI, session)` — a parallel session
    number from one worker can never collide with another's across runs
    (SR-065). The id is `<utc-stamp>-<pid>-<rand>`, unique per launch."""

    def __init__(self, root, run_id=None):
        self.dir = Path(root) / DISPATCH_DIR
        self.run_id = run_id or "{}-{}-{:04x}".format(
            time.strftime("%Y%m%dT%H%M%S"),
            os.getpid(),
            int.from_bytes(os.urandom(2), "big"),
        )
        try:
            self.dir.mkdir(parents=True, exist_ok=True)
            (self.dir / "trains").mkdir(exist_ok=True)
        except OSError:
            pass

    def event(self, event, **fields):
        rec = {
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "run": self.run_id,
            "event": event,
        }
        rec.update(fields)
        try:
            with (self.dir / "events.jsonl").open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, sort_keys=True) + "\n")
        except OSError:
            pass
        detail = " ".join(
            "{}={}".format(k, v) for k, v in sorted(fields.items()) if v != ""
        )
        print("dispatch: {}{}".format(event, " " + detail if detail else ""))

    def manifest(self, data):
        try:
            tmp = self.dir / "manifest.json.tmp"
            tmp.write_text(json.dumps(data, indent=2, sort_keys=True), "utf-8")
            os.replace(str(tmp), str(self.dir / "manifest.json"))
        except OSError:
            pass

    def train(self, train_id, data):
        try:
            tmp = self.dir / "trains" / (train_id + ".json.tmp")
            tmp.write_text(json.dumps(data, indent=2, sort_keys=True), "utf-8")
            os.replace(str(tmp), str(self.dir / "trains" / (train_id + ".json")))
        except OSError:
            pass


# -----------------------------------------------------------------------------
# WI-184: the atomic serialized integrator (SR-063; spec §9)
# -----------------------------------------------------------------------------
# One logical writer against refs/heads/llm/integration. The ref is advanced
# ONLY by compare-and-swap and is never checked out in the user's primary
# worktree: each ready train composes on a temporary staging branch
# llm/integrate/<train-id> in its own worktree, and the development branch is
# a published PROJECTION of the integration ref — synchronized through the
# durable refs/llm/publish-intent protocol, never half-applied.

INTEGRATION_REF = "refs/heads/llm/integration"


INTEGRATE_BRANCH_PREFIX = "llm/integrate/"


PUBLISH_INTENT_REF = "refs/llm/publish-intent"


STATUS_GENERATED_MARKER = "GENERATED by scripts/agent_loop.py integrator"


def integration_head(root):
    """The integration ref's commit, or None when the ref does not exist."""
    code, out = git(root, "rev-parse", "--verify", "--quiet", INTEGRATION_REF)
    return out.strip() if code == 0 and out.strip() else None


def cas_ref(root, ref, new, old):
    """Compare-and-swap `ref` from exactly `old` to `new` (one update-ref
    transaction). `old` = None asserts creation. Returns True on success; a
    False is HARMLESS — the caller recomposes from the ref's new value."""
    if old:
        line = "update {} {} {}".format(ref, new, old)
    else:
        line = "create {} {}".format(ref, new)
    proc = subprocess.run(
        ["git", "-C", str(root), "update-ref", "--stdin"],
        input=("start\n{}\nprepare\ncommit\n".format(line)).encode("utf-8"),
        capture_output=True,
    )
    return proc.returncode == 0


def ensure_integration_ref(root, journal):
    """Create refs/heads/llm/integration from the selected development branch
    on a GENUINE cold start only (spec §11 rule 2): if the ref is absent while
    dispatcher-owned evidence exists (train/integrate branches, reservations,
    a publish intent), something deleted it — fail closed rather than silently
    blessing the development branch. Returns (head, err)."""
    head = integration_head(root)
    if head:
        return head, None
    code, out = git(
        root,
        "for-each-ref",
        "--format=%(refname)",
        "refs/heads/llm/train",
        "refs/heads/llm/integrate",
        RESERVATION_NS.rstrip("/"),
        PUBLISH_INTENT_REF,
    )
    evidence = [ln for ln in out.splitlines() if ln.strip()] if code == 0 else []
    if evidence:
        return None, (
            "refs/heads/llm/integration is absent but dispatcher-owned "
            "evidence exists ({} ref(s)) — a deleted/corrupt integration ref "
            "is reconstructed or fails closed (spec §11), never re-seeded "
            "from the development branch.".format(len(evidence))
        )
    dev = head_sha_full(root)
    if not dev or not cas_ref(root, INTEGRATION_REF, dev, None):
        return None, "cannot initialize the integration ref from HEAD"
    journal.event("integration-ref-init", head=dev[:12])
    return dev, None


def registry_rows_at(root, ref):
    """The WI registry rows as read from `ref` (the integrated disposition),
    falling back to the checkout when unreadable. The integration ref — not
    the development checkout — is the scheduling authority once it exists."""
    proc = subprocess.run(
        ["git", "-C", str(root), "show", ref + ":docs/requirements/work-items.csv"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode != 0:
        return None
    import io

    return list(csv.DictReader(io.StringIO(proc.stdout)))


def reviewed_train_head(root, tid, base):
    """The exact code HEAD a train's review must name: the LAST commit in
    base..tip carrying a WI trailer (verdict/telemetry commits come after)."""
    fmt = "%H%x09%(trailers:key=WI,valueonly,separator=;)"
    code, out = git(
        root, "log", "--format=" + fmt, base + ".." + TRAIN_BRANCH_PREFIX + tid
    )
    if code != 0:
        return None
    for line in out.splitlines():  # newest first
        parts = line.split("\t")
        if len(parts) == 2 and any(
            WI_TOKEN_RE.match(x.strip()) for x in parts[1].split(";")
        ):
            return parts[0]
    return None


def train_verdicts(root, tid, reviewed_sha):
    """[(phase, verdict)] parsed from the verdict files committed on the train
    branch that NAME the exact reviewed commit (reviews/<train>/NNN-<PHASE>-
    <sha7>.md). A verdict naming an older head does not count (spec §8)."""
    tip = TRAIN_BRANCH_PREFIX + tid
    prefix = "docs/reviews/{}/".format(tid)
    code, out = git(root, "ls-tree", "-r", "--name-only", tip, prefix)
    results = []
    if code != 0 or not reviewed_sha:
        return results
    want = reviewed_sha[:7]
    for name in out.splitlines():
        m = re.match(r".*/(\d+)-(REVIEW-[AB]|CRITIQUE)-([0-9a-f]+)\.md$", name.strip())
        if not m or m.group(3) != want:
            continue
        code2, text = git(root, "show", "{}:{}".format(tip, name.strip()))
        if code2 != 0:
            continue
        verdict = ""
        for line in text.splitlines():
            vm = re.match(r"\s*VERDICT:\s*(APPROVE|CHANGES-REQUESTED)", line)
            if vm:
                verdict = vm.group(1)
        results.append((m.group(2), verdict))
    return results


def _staging_worktree(root, tid, base):
    """A staging branch llm/integrate/<tid> at `base` checked out in its own
    worktree. Reuses an existing branch/worktree (recovery). Returns
    (worktree_path, err)."""
    branch = INTEGRATE_BRANCH_PREFIX + tid
    trees = existing_worktrees(root)
    ref = "refs/heads/" + branch
    if ref in trees:
        return Path(trees[ref]), None
    code, _ = git(root, "rev-parse", "--verify", "--quiet", ref)
    wt = worktree_root(root) / ("integrate-" + tid)
    wt.parent.mkdir(parents=True, exist_ok=True)
    if code == 0:
        code2, out = git(root, "worktree", "add", str(wt), branch)
    else:
        code2, out = git(root, "worktree", "add", "-b", branch, str(wt), base)
    if code2 != 0:
        return None, "staging worktree failed for {}: {}".format(tid, out[:300])
    return wt, None


def _rewrite_wi_rows(path, updates):
    """Surgically rewrite specific WI rows (Status/Deliverable/BlockRef) in a
    work-items.csv, touching ONLY the named rows so the integrator never
    reflows an adopter's registry. Returns the list of updated ids."""
    with open(str(path), newline="", encoding="utf-8-sig") as fh:
        rows = list(csv.reader(fh))
    if not rows:
        return []
    header = rows[0]
    idx = {h: i for i, h in enumerate(header)}
    done = []
    for r in rows[1:]:
        if not r or r[0] not in updates:
            continue
        for col, val in updates[r[0]].items():
            if col in idx:
                while len(r) <= idx[col]:
                    r.append("")
                r[idx[col]] = val
        done.append(r[0])
    with open(str(path), "w", newline="", encoding="utf-8") as fh:
        csv.writer(fh, lineterminator="\n").writerows(rows)
    return done


def synth_deliverable(root, tid, wid, base):
    """The integrator's Deliverable text for a WI it marks done: the train,
    the exact commit, and the worker's own commit subject — derived facts,
    never invented prose."""
    fmt = "%H%x09%s%x09%(trailers:key=WI,valueonly,separator=;)"
    code, out = git(
        root, "log", "--format=" + fmt, base + ".." + TRAIN_BRANCH_PREFIX + tid
    )
    subject, sha = "", ""
    if code == 0:
        for line in out.splitlines():
            parts = line.split("\t")
            if len(parts) == 3 and wid in [x.strip() for x in parts[2].split(";")]:
                sha, subject = parts[0][:7], parts[1]
                break
    return "Integrated from train {} @ {}: {}".format(tid, sha or "?", subject or wid)


def generate_status(docs, root, last_train=""):
    """The integrator-generated root status snapshot (SR-059's generation
    half; spec §10): derived gate/bar pointers, queue counts, pending human
    items, the last integrated train — links, never copies. Written ONLY when
    docs/status.md is absent or already generated (a hand-authored status is
    the un-migrated state and is left alone until the migration flips it)."""
    path = docs / "status.md"
    try:
        if path.exists() and STATUS_GENERATED_MARKER not in path.read_text(
            encoding="utf-8", errors="replace"
        ):
            return False
    except OSError:
        return False
    rows = registry_rows_at(root, INTEGRATION_REF) or []
    counts = {"queued": 0, "deferred": 0, "blocked": 0, "done": 0}
    for r in rows:
        st = (r.get("Status") or "").strip().lower()
        if st in counts:
            counts[st] += 1
    gate = read_declared(docs / "gate", "(none)")
    reserved = sorted(list_reservations(root))
    lines = [
        "<!-- " + STATUS_GENERATED_MARKER + " — do not hand-edit -->",
        "# Status (generated)",
        "",
        "- **Derived gate:** {} ([docs/gate](gate); the harness is the bar)".format(
            gate
        ),
        "- **Work items:** {queued} queued · {deferred} deferred · "
        "{blocked} blocked · {done} done — the registry "
        "[work-items.csv](requirements/work-items.csv) is the source; the "
        "dashboard is generated from it.".format(**counts),
        "- **Reserved (in flight):** {}".format(", ".join(reserved) or "none"),
        "- **Last integrated train:** {}".format(last_train or "none this run"),
        "- **Needs <human>:** see [open-items.md](open-items.md) if present.",
        "",
        "_Regenerated by the integrator on the integration branch after every"
        " successful integration — never written on a worker branch._",
    ]
    try:
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    except OSError:
        return False
    return True


def _run_combined_bar(worktree, root):
    """The combined commit bar on the composed tree: the declared stack test
    command (docs/stack.ini [stack] test). Returns (ok, detail); no declared
    command reports ('skipped', True) — a stackless fixture, not a pass."""
    import configparser

    ini = Path(worktree) / "docs" / "stack.ini"
    if not ini.exists():
        return True, "skipped (no docs/stack.ini)"
    cp = configparser.ConfigParser()
    try:
        cp.read(str(ini), encoding="utf-8")
        cmd = (cp.get("stack", "test", fallback="") or "").strip()
    except configparser.Error as exc:
        return False, "stack.ini unreadable: {}".format(exc)
    if not cmd:
        return True, "skipped (no declared test command)"
    try:
        argv = shlex.split(cmd)
    except ValueError as exc:
        return False, "cannot parse test command: {}".format(exc)
    proc = subprocess.run(
        argv,
        cwd=str(worktree),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    tail = ((proc.stdout or "") + (proc.stderr or "")).strip()[-400:]
    return proc.returncode == 0, ("pass" if proc.returncode == 0 else tail)


def _regenerate_disposition_artifacts(worktree):
    """Regenerate freshness-gated views after a disposition edits registries.

    The generators are kit-owned siblings of this dispatcher even when the
    checkout is a downstream scaffold. Artifact presence is the opt-in signal:
    a non-adopter must not depend on either generator.
    """
    worktree = Path(worktree)
    scripts = Path(__file__).resolve().parent
    generators = []
    if (worktree / "docs" / "okf").is_dir():
        generators.append("gen_okf.py")
    if (worktree / "PROJECT_STATE.html").is_file():
        generators.append("gen_trajectory.py")
    for name in generators:
        proc = subprocess.run(
            [sys.executable, str(scripts / name), "--root", str(worktree)],
            cwd=str(worktree),
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
        if proc.returncode != 0:
            tail = ((proc.stdout or "") + (proc.stderr or "")).strip()[-400:]
            return False, "disposition regen failed ({}): {}".format(
                name, tail or "exit {}".format(proc.returncode)
            )
    return True, ""


def _salvage_round_evidence(root, worktree, tid, old_head=None):
    """Best-effort copy of DP-* evidence before a hard reset: uncommitted
    changes via porcelain (the only scan that sees untracked files) plus,
    when the reset target is known, tracked changes already committed past
    it — those files are still on disk because salvage runs pre-reset. Both
    scans use NUL-delimited output so Git never C-quotes non-ASCII/special
    path bytes; malformed records simply contribute no round name."""
    round_names = set()

    def note(rel):
        rel = rel.replace("\\", "/")
        parts = rel.split("/")
        if len(parts) >= 3 and parts[:2] == ["docs", "plans"]:
            if parts[2].startswith("DP-"):
                round_names.add(parts[2])

    code, out = git(
        worktree,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        "--",
        "docs/plans",
    )
    if code == 0:
        records = out.split("\0")
        index = 0
        while index < len(records):
            record = records[index]
            index += 1
            if len(record) < 4 or record[2] != " ":
                continue
            status = record[:2]
            note(record[3:])
            # Porcelain -z records a rename/copy destination first, followed
            # by its source as a second NUL record (there is no `->` marker).
            if "R" in status or "C" in status:
                index += 1
    if old_head:
        code, out = git(
            worktree,
            "diff",
            "--name-only",
            "-z",
            old_head,
            "--",
            "docs/plans",
        )
        if code == 0:
            for rel in out.split("\0"):
                note(rel)
    if not round_names:
        return ""
    destination = Path(root) / DISPATCH_DIR / "salvage" / tid
    try:
        destination.mkdir(parents=True, exist_ok=True)
        for name in sorted(round_names):
            source = Path(worktree) / "docs" / "plans" / name
            target = destination / name
            if source.is_dir():
                shutil.copytree(str(source), str(target), dirs_exist_ok=True)
            elif source.is_file():
                shutil.copy2(str(source), str(target))
        return str(destination)
    except OSError:
        return ""


def _reset_failed_disposition(root, worktree, tid, old_head, detail, merge=False):
    """Preserve round evidence, clean staging, and retain the original error."""
    salvage = _salvage_round_evidence(root, worktree, tid, old_head)
    if merge:
        git(worktree, "merge", "--abort")
    git(worktree, "reset", "--hard", old_head)
    if salvage:
        return "{}; round evidence salvaged to {}".format(detail, salvage)
    return detail


# --- WI-231: composition-conflict auto-resolution --------------------------------
# The registry the row-level union merge (Slice B) keys by WI-ID.
REGISTRY_REL = "docs/requirements/work-items.csv"

# The generated-artifact set (Slice A): paths a harness `--check` step OWNS — see
# project-trajectory/scripts/check.py's arch-map / trajectory-map / status-map /
# okf steps. A composition conflict CONFINED to these is resolved by REGENERATING
# from the cleanly-merged sources instead of hand-merging, honoring the kit's
# generated-not-hand-maintained principle.
#
# The set is DECLARED, not discovered (WI-235): each repo names its generated
# artifacts in the [generated] section of its own docs/stack.ini, so a downstream
# repo with its own artifacts (or one that relocates a default) teaches the
# integrator without forking kit code. The tuple below is the built-in DEFAULT an
# ABSENT section falls back to — byte-identical legacy behavior — and the value
# bootstrap.py scaffolds into a fresh repo's stack.ini.
#
# Each row: (matcher, block, kind). `matcher` is an exact repo-relative path or a
# "/"-terminated directory prefix. `block` is None for a FULLY generated artifact
# (any conflict is regenerable) or a (BEGIN, END) marker pair for a PARTIALLY
# generated file where ONLY the marked region is generated — a conflict OUTSIDE it
# must still park (status.md's hand-authored prose; architecture.md's prose).
# `kind` selects the regenerator argv (_generated_regen_argv). The skills index is
# deliberately absent: its neutral source lives only in the kit repo and its
# per-agent copies are hand-authored source that must park, not regenerate.
DEFAULT_GENERATED_ARTIFACTS = (
    ("PROJECT_STATE.html", None, "trajectory"),
    ("docs/okf/", None, "okf"),
    (
        "docs/architecture.md",
        ("<!-- BEGIN GENERATED MODULE MAP -->", "<!-- END GENERATED MODULE MAP -->"),
        "archmap",
    ),
    (
        "docs/status.md",
        ("<!-- BEGIN GENERATED STATUS -->", "<!-- END GENERATED STATUS -->"),
        "status",
    ),
)

# The regenerator kinds a [generated] row may name (each maps to a generator argv
# in _generated_regen_argv); an unknown kind is a malformed row.
_GENERATED_KINDS = ("trajectory", "okf", "status", "archmap")


def _parse_generated_row(matcher, value):
    """Parse one docs/stack.ini [generated] declaration `<path> = <kind>` (a
    FULLY generated artifact) or `<path> = <kind> | <BEGIN> | <END>` (a PARTIALLY
    generated file) into a (matcher, block, kind) row. Raises ValueError on any
    malformed row — the caller FAILS CLOSED and parks, so an unparseable
    declaration never widens auto-resolution."""
    matcher = matcher.strip()
    if not matcher:
        raise ValueError("blank artifact path")
    parts = [p.strip() for p in value.split("|")]
    kind = parts[0]
    if kind not in _GENERATED_KINDS:
        raise ValueError("unknown regenerator kind {!r}".format(kind))
    if len(parts) == 1:
        block = None
    elif len(parts) == 3 and parts[1] and parts[2]:
        block = (parts[1], parts[2])
    else:
        raise ValueError(
            "expected '<path> = <kind>' or '<path> = <kind> | BEGIN | END'"
        )
    return (matcher, block, kind)


def _generated_artifacts(wt):
    """The generated-artifact set governing composition auto-resolution, read from
    the INTEGRATE worktree's OWN docs/stack.ini (the primary worktree may differ
    mid-merge). Returns (artifacts, error): an ABSENT [generated] section falls
    back to DEFAULT_GENERATED_ARTIFACTS (byte-identical legacy behavior) with
    error None; a present-but-MALFORMED section returns ((), <non-blank reason>)
    so the caller fails closed and parks."""
    import configparser

    cp = configparser.ConfigParser(interpolation=None)
    cp.optionxform = str  # artifact paths are case-sensitive (PROJECT_STATE.html)
    try:
        cp.read(str(Path(wt) / "docs" / "stack.ini"), encoding="utf-8")
    except configparser.Error as exc:
        return (), "docs/stack.ini unreadable: {}".format(exc)
    if not cp.has_section("generated"):
        return DEFAULT_GENERATED_ARTIFACTS, None
    rows = []
    try:
        for matcher, value in cp.items("generated"):
            rows.append(_parse_generated_row(matcher, value))
    except (configparser.Error, ValueError) as exc:
        return (), "malformed [generated] row in docs/stack.ini: {}".format(exc)
    return tuple(rows), None


def _generated_entry(rel, artifacts):
    """The `artifacts` row matching a repo-relative path, or None."""
    rel = rel.replace("\\", "/")
    for matcher, block, kind in artifacts:
        if matcher.endswith("/"):
            if rel.startswith(matcher):
                return (matcher, block, kind)
        elif rel == matcher:
            return (matcher, block, kind)
    return None


def _declared_src(wt):
    """The docs/stack.ini [paths] src the arch-map generator scans (default
    'src'), so regeneration matches the harness `--check` invocation."""
    import configparser

    cp = configparser.ConfigParser()
    try:
        cp.read(str(Path(wt) / "docs" / "stack.ini"), encoding="utf-8")
        return (cp.get("paths", "src", fallback="src") or "src").strip()
    except configparser.Error:
        return "src"


def _generated_regen_argv(kind, wt):
    """The generator argv for a generated-artifact `kind`, run in the integrate
    worktree against its merged tree (never the primary worktree)."""
    scripts = Path(__file__).resolve().parent
    py = sys.executable
    if kind == "trajectory":
        return [py, str(scripts / "gen_trajectory.py"), "--root", str(wt)]
    if kind == "okf":
        return [py, str(scripts / "gen_okf.py"), "--root", str(wt)]
    if kind == "status":
        return [py, str(scripts / "gen_trajectory.py"), "--root", str(wt), "--status"]
    if kind == "archmap":
        return [
            py,
            str(scripts / "gen_arch_map.py"),
            "--src",
            _declared_src(wt),
            "--doc",
            "docs/architecture.md",
        ]
    return None


def _resolve_block_conflict(text, block):
    """Resolve conflict hunks by taking the OURS side, but ONLY when every hunk
    lies WHOLLY inside the generated `block` (a (BEGIN, END) marker pair); return
    None (park) when a conflict touches the hand-authored region. A hunk that
    STARTS in-block but whose either side re-includes a BEGIN/END marker line has
    straddled the block edge and swallowed hand-authored prose — regeneration
    cannot stand in for that, so it parks too. Markers are compared LF-clean so an
    autocrlf (CRLF) checkout still latches `inside` (WI-231 rework). The block is
    regenerated afterward, so which side wins inside it is moot."""
    begin, end = block
    markers = (begin, end)
    lines = text.split("\n")
    out = []
    inside = False
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        if line.startswith("<<<<<<<"):
            if not inside:
                return None
            ours = []
            i += 1
            while i < n and not lines[i].startswith("======="):
                ours.append(lines[i])
                i += 1
            i += 1  # skip the ======= divider
            theirs = []
            while i < n and not lines[i].startswith(">>>>>>>"):
                theirs.append(lines[i])
                i += 1
            i += 1  # skip the >>>>>>> closer
            if any(ln.rstrip("\r") in markers for ln in ours + theirs):
                return None  # a straddling hunk: park rather than drop prose
            out.extend(ours)
            continue
        stripped = line.rstrip("\r")
        if stripped == begin:
            inside = True
        elif stripped == end:
            inside = False
        out.append(line)
        i += 1
    return "\n".join(out)


def _resolve_generated_path(wt, rel, entry):
    """Resolve one conflicted generated path in the merge index. A fully
    generated artifact takes OURS wholesale (regeneration overwrites it); a
    block-generated file strips only in-block conflicts. Returns False (park)
    when the conflict escapes the block. Stages the resolved path."""
    _, block, _ = entry
    if block is None:
        git(wt, "checkout", "--ours", "--", rel)
        git(wt, "add", "--", rel)
        return True
    path = Path(wt) / rel
    try:
        resolved = _resolve_block_conflict(
            path.read_text(encoding="utf-8", errors="replace"), block
        )
        if resolved is None:
            return False
        path.write_text(resolved, encoding="utf-8")
    except OSError:
        return False
    git(wt, "add", "--", rel)
    return True


def _stage_rows(wt, stage, rel):
    """(header, data_rows) parsed from a merge index stage (1=base, 2=ours,
    3=theirs) of `rel`; (None, []) when that stage is absent (add/add). The blob
    is read RAW — un-stripped, via cat-file rather than git() (which strips), and
    parsed straight through the csv module — so a quoted cell with an embedded
    newline survives instead of being collapsed and corrupting an untouched
    neighbor row on re-serialization (WI-231 rework)."""
    proc = subprocess.run(
        ["git", "-C", str(wt), "cat-file", "-p", ":{}:{}".format(stage, rel)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    if proc.returncode != 0:
        return None, []
    rows = list(csv.reader(io.StringIO(proc.stdout)))
    if not rows:
        return [], []
    header = list(rows[0])
    if header:
        header[0] = header[0].lstrip("﻿")
    return header, rows[1:]


def _ordered_wi_rows(merged, sequences):
    """Merged rows in a deterministic order: base order first, then ours-only,
    then theirs-only additions — each id emitted once."""
    order = []
    seen = set()
    for seq in sequences:
        for r in seq:
            if r and r[0] in merged and r[0] not in seen:
                seen.add(r[0])
                order.append(merged[r[0]])
    return order


def _merge_wi_rows(base_rows, ours_rows, theirs_rows):
    """Row-level WI-ID-keyed 3-way union: a row changed on one side only takes
    that side; a row changed on BOTH sides (or a modify/delete race) returns None
    so the train parks as a genuine conflict."""
    base = {r[0]: r for r in base_rows if r}
    ours = {r[0]: r for r in ours_rows if r}
    theirs = {r[0]: r for r in theirs_rows if r}
    merged = {}
    for key in set(ours) | set(theirs):
        b, o, t = base.get(key), ours.get(key), theirs.get(key)
        if o == t:
            winner = o
        elif o == b:  # unchanged on our side -> take theirs
            winner = t
        elif t == b:  # unchanged on their side -> take ours
            winner = o
        else:  # a genuine both-sides edit of the same row
            return None
        if winner is not None:
            merged[key] = winner
    return _ordered_wi_rows(merged, (base_rows, ours_rows, theirs_rows))


def _union_registry(wt, rel):
    """Slice B: resolve a work-items.csv conflict by a WI-ID-keyed row union.
    Returns True (resolved + staged) or False (a genuine row/header conflict —
    park). Header comes from the merged result (ours, when both sides agree)."""
    ours_h, ours = _stage_rows(wt, 2, rel)
    theirs_h, theirs = _stage_rows(wt, 3, rel)
    _, base = _stage_rows(wt, 1, rel)
    if ours_h is None or theirs_h is None or ours_h != theirs_h:
        return False  # add/add or a header edit conflict: park
    merged = _merge_wi_rows(base, ours, theirs)
    if merged is None:
        return False
    with open(str(Path(wt) / rel), "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(ours_h)
        writer.writerows(merged)
    git(wt, "add", "--", rel)
    return True


def _regenerate_generated(wt, paths, artifacts):
    """Re-run the sibling generators for the conflicted generated `paths`
    (deduplicated by kind) IN the integrate worktree against its merged tree.
    Returns (ok, detail)."""
    kinds = []
    for rel in paths:
        entry = _generated_entry(rel, artifacts)
        if entry and entry[2] not in kinds:
            kinds.append(entry[2])
    for kind in kinds:
        argv = _generated_regen_argv(kind, wt)
        if argv is None:
            continue
        proc = subprocess.run(
            argv,
            cwd=str(wt),
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
        if proc.returncode != 0:
            tail = ((proc.stdout or "") + (proc.stderr or "")).strip()[-400:]
            return False, "conflict regen failed ({}): {}".format(
                kind, tail or "exit {}".format(proc.returncode)
            )
    return True, ""


def _resolve_composition_conflict(wt, root, artifacts):
    """Auto-resolve the conflicts the harness OWNS after a conflicted 3-way
    merge: disjoint WI rows (Slice B) and regenerated artifacts (Slice A) declared
    in `artifacts`. Parks the moment a non-generated path — or a both-sides row /
    in-prose block edit — conflicts. Leaves the index conflict-free + staged on
    success. Returns (resolved, regenerated_paths, park_reason)."""
    code, out = git(wt, "diff", "--name-only", "--diff-filter=U", "-z")
    if code != 0:
        return False, [], "cannot list conflicted paths"
    conflicted = [p.replace("\\", "/") for p in out.split("\0") if p]
    if not conflicted:
        return False, [], "merge failed without conflicts"
    regenerated = []
    for rel in conflicted:
        if rel == REGISTRY_REL:
            if not _union_registry(wt, rel):
                return False, [], "registry row conflict in {}".format(rel)
            continue
        entry = _generated_entry(rel, artifacts)
        if entry is None:
            return False, [], "conflict in non-generated path {}".format(rel)
        if not _resolve_generated_path(wt, rel, entry):
            return False, [], "generated conflict outside its block: {}".format(rel)
        regenerated.append(rel)
    ok, detail = _regenerate_generated(wt, regenerated, artifacts)
    if not ok:
        return False, [], detail
    return True, regenerated, None


def _compose_train(wt, root, journal, tid, tip):
    """Merge train `tip` onto the staged integration HEAD (spec §9 steps 1+3+4).
    A clean 3-way apply, or an auto-resolved generated/registry conflict, returns
    None to proceed; a genuine textual conflict aborts the merge, journals it, and
    returns a park detail demanding a focused re-review."""
    code, out = git(wt, "merge", "--no-ff", "--no-commit", tip)
    if code == 0:
        return None
    artifacts, decl_error = _generated_artifacts(wt)
    if decl_error:
        resolved, regenerated, park = False, [], decl_error
    else:
        resolved, regenerated, park = _resolve_composition_conflict(wt, root, artifacts)
    if not resolved:
        git(wt, "merge", "--abort")
        detail = (park or out).strip()[
            :200
        ] or "textual conflict against the integrated tree"
        journal.event("integration-conflict", train=tid, detail=detail)
        # Return the SPECIFIC reason (it names the conflicted path) so the park
        # state, the durable conflict record, and the NEEDS-HUMAN ask all name it.
        return detail
    journal.event(
        "integration-regenerated", train=tid, paths=";".join(regenerated)[:200]
    )
    return None


def integrate_train(root, docs, journal, tid, wis, base, required_verdicts):
    """Compose one ready train into the integration ref (spec §9 steps 1-11).
    Returns (state, detail): 'integrated', 'needs-re-review' (a textual conflict
    outside the auto-resolvable set — generated artifacts / disjoint WI rows,
    WI-231 — needing a focused re-review before this train can land), 'rework'
    (verdict missing/stale or the combined bar failed), or 'error'. The
    integration ref moves ONLY via the final CAS."""
    old_head = integration_head(root)
    if old_head is None:
        return "error", "integration ref vanished"
    code, tip = git(root, "rev-parse", TRAIN_BRANCH_PREFIX + tid)
    if code != 0:
        return "error", "train branch missing"
    tip = tip.strip()

    # Step 2: verify reservation scope + the exact-head review verdicts.
    claims = list_reservations(root)
    for wid in wis:
        meta = reservation_meta(root, claims.get(wid, ""))
        if not meta or meta.get("train") != tid:
            return "error", "reservation for {} does not name train {}".format(wid, tid)
    reviewed = reviewed_train_head(root, tid, base)
    if required_verdicts:
        verdicts = train_verdicts(root, tid, reviewed)
        approvals = {ph for ph, v in verdicts if v == "APPROVE"}
        if len(approvals) < required_verdicts:
            return "rework", (
                "review verdicts naming {}: {} approval(s) of {} required".format(
                    (reviewed or "?")[:7], len(approvals), required_verdicts
                )
            )

    # Step 1+3+4: compose on the staging branch from the CURRENT integration
    # HEAD. A clean 3-way apply takes the fast path (no re-review); a conflict
    # confined to generated artifacts (Slice A) or disjoint WI rows (Slice B) is
    # auto-resolved and composition continues; any OTHER textual conflict aborts
    # and demands a focused re-review (_compose_train, WI-231).
    wt, err = _staging_worktree(root, tid, old_head)
    if err:
        return "error", err
    code, _ = git(wt, "reset", "--hard", old_head)
    if code != 0:
        return "error", "cannot reset staging to the integration HEAD"
    park = _compose_train(wt, root, journal, tid, tip)
    if park is not None:
        # Durably record the merge inputs so a relaunch with UNCHANGED inputs
        # skips this identical merge instead of re-parking silently (WI-232).
        record_conflict(root, tid, tip, old_head, park)
        return "needs-re-review", park

    # Steps 6-8: durable disposition + evidence + regenerated artifacts,
    # composed INTO the same integration commit.
    reg = Path(wt) / "docs" / "requirements" / "work-items.csv"
    updates = {
        wid: {
            "Status": "done",
            "Deliverable": synth_deliverable(root, tid, wid, base),
        }
        for wid in wis
    }
    updated = _rewrite_wi_rows(reg, updates) if reg.exists() else []
    stamp = time.strftime("%Y-%m-%d %H:%M")
    log_path = Path(wt) / "docs" / "log.md"
    try:
        with log_path.open("a", encoding="utf-8") as fh:
            fh.write(
                "\n## {} — integrated train {} ({})\n\n"
                "Head {} composed onto {} by the serialized integrator; "
                "{} verdict(s) verified on the exact reviewed head; combined "
                "bar ran on the composed tree (result below). WI row(s) {} "
                "-> done.\n".format(
                    stamp,
                    tid,
                    ";".join(wis),
                    tip[:7],
                    old_head[:7],
                    required_verdicts,
                    ";".join(updated) or "(none present)",
                )
            )
    except OSError:
        pass
    regenerate_index(Path(wt) / "docs")
    generate_status(Path(wt) / "docs", root, last_train=tid)
    regen_ok, regen_detail = _regenerate_disposition_artifacts(wt)
    if not regen_ok:
        return "error", _reset_failed_disposition(
            root, wt, tid, old_head, regen_detail, merge=True
        )

    # Step 9: the combined bar always runs — even after a clean apply.
    ok, bar_detail = _run_combined_bar(wt, root)
    journal.event("integration-bar", train=tid, result=bar_detail[:120])
    if not ok:
        detail = "combined bar failed: {}".format(bar_detail[:300])
        return "rework", _reset_failed_disposition(
            root, wt, tid, old_head, detail, merge=True
        )

    # Step 10: ONE integration commit carrying the trailers.
    git(wt, "add", "-A")
    trailers = "".join("Integrated-WI: {}\n".format(w) for w in wis)
    msg = "integrate: train {} ({})\n\n{}Train-Head: {}\nTrain: {}\n".format(
        tid, ";".join(wis), trailers, tip, tid
    )
    code, out = git(wt, "commit", "-q", "-m", msg)
    if code != 0:
        detail = "integration commit failed: {}".format(out[:200])
        return "error", _reset_failed_disposition(
            root, wt, tid, old_head, detail, merge=True
        )
    code, new_head = git(wt, "rev-parse", "HEAD")
    new_head = new_head.strip()
    _fault("pre-integration-cas")

    # Step 11: advance the integration ref by CAS. A stale expected-old is
    # HARMLESS — the train re-enters composition from the new HEAD.
    if not cas_ref(root, INTEGRATION_REF, new_head, old_head):
        journal.event("integration-cas-stale", train=tid)
        detail = _reset_failed_disposition(
            root,
            wt,
            tid,
            old_head,
            "integration ref moved; recomposing",
        )
        return "recompose", detail
    _fault("post-integration-cas")
    journal.event("integrated", train=tid, wis=";".join(wis), head=new_head[:12])
    # Reservation refs release transactionally ONLY after the durable
    # disposition advanced (spec §6).
    err = release_reservations(root, wis)
    if err:
        journal.event("release-failed", train=tid, reason=err[:200])
    return "integrated", new_head


def blocked_disposition(root, docs, journal, tid, wis, base):
    """The smaller serialized blocked-disposition transaction (spec §9): from
    the current integration HEAD change ONLY the blocked WI's row
    (Status=blocked + BlockRef), append the log evidence, commit with
    Blocked-WI/BlockRef/Train trailers, CAS — and only then release the
    blocked WI's reservation (unstarted ones were already released at the
    early end). Built constituents keep theirs (their partial-train re-review
    path hardens in Slice G). Returns (state, detail)."""
    old_head = integration_head(root)
    if old_head is None:
        return "error", "integration ref vanished"
    built, blocked_map = train_branch_evidence(root, tid, base)
    hit = {w: blocked_map[w] for w in wis if w in blocked_map}
    if not hit:
        return "error", "no Blocked-WI trailer evidence on train " + tid
    wt, err = _staging_worktree(root, tid, old_head)
    if err:
        return "error", err
    code, _ = git(wt, "reset", "--hard", old_head)
    if code != 0:
        return "error", "cannot reset staging to the integration HEAD"
    reg = Path(wt) / "docs" / "requirements" / "work-items.csv"
    updates = {
        wid: {"Status": "blocked", "BlockRef": ref or "(uncommitted — a finding)"}
        for wid, ref in hit.items()
    }
    updated = _rewrite_wi_rows(reg, updates) if reg.exists() else []
    try:
        with (Path(wt) / "docs" / "log.md").open("a", encoding="utf-8") as fh:
            fh.write(
                "\n## {} — blocked disposition: {} (train {})\n\n"
                "Worker-reported blocker with committed evidence at {}; "
                "BlockRef: {}.\n".format(
                    time.strftime("%Y-%m-%d %H:%M"),
                    ";".join(sorted(hit)),
                    tid,
                    base[:7],
                    "; ".join(v or "(none)" for v in hit.values()),
                )
            )
    except OSError:
        pass
    generate_status(Path(wt) / "docs", root, last_train="")
    regen_ok, regen_detail = _regenerate_disposition_artifacts(wt)
    if not regen_ok:
        return "error", _reset_failed_disposition(root, wt, tid, old_head, regen_detail)
    git(wt, "add", "-A")
    trailers = "".join("Blocked-WI: {}\n".format(w) for w in sorted(hit))
    trailers += "".join("BlockRef: {}\n".format(v or "(none)") for v in hit.values())
    msg = "blocked: {} (train {})\n\n{}Train: {}\n".format(
        ";".join(sorted(hit)), tid, trailers, tid
    )
    code, out = git(wt, "commit", "-q", "-m", msg)
    if code != 0:
        detail = "disposition commit failed: {} (rows: {})".format(
            out[:200], ";".join(updated)
        )
        return "error", _reset_failed_disposition(root, wt, tid, old_head, detail)
    code, new_head = git(wt, "rev-parse", "HEAD")
    if not cas_ref(root, INTEGRATION_REF, new_head.strip(), old_head):
        detail = _reset_failed_disposition(
            root, wt, tid, old_head, "integration ref moved; recomposing"
        )
        return "recompose", detail
    journal.event("blocked-disposition", train=tid, wis=";".join(sorted(hit)))
    err = release_reservations(root, sorted(hit))
    if err:
        journal.event("release-failed", train=tid, reason=err[:200])
    return "integrated", new_head.strip()


def dual_plan_disposition(
    root, journal, tid, wid, row, template, model, timeout, prompt_map
):
    """Auto-dispatch one PlanMode=dual frontier WI as a dual-plan round
    (WI-209, the SR-066 auto-dispatch AC): the round — the WI-199 engine,
    reused as-is — runs in a staging worktree reset to the current integration
    HEAD, so its artifact writes (docs/plans/DP-*, the filed child rows, the
    log summary) compose into ONE serialized disposition commit exactly like
    blocked_disposition (the smaller docs-only transaction — no product code
    changes, so the combined bar belongs to the children's own trains, not
    here). On SELECT the parent row closes done (its deliverable IS the
    selected decomposition; the filed children hang off it as hard
    predecessors, so an open parent would park the subtree and a queued one
    would re-run the round). On PAGE the artifacts still commit (the honest
    evidence the serial --dual-plan entry leaves in its checkout) and the
    parent row is untouched. Returns (outcome, detail): 'SELECTED', 'PAGE',
    or 'error'. The caller owns reservations and the gate-policy mapping."""
    old_head = integration_head(root)
    if old_head is None:
        return "error", "integration ref vanished"
    wt, err = _staging_worktree(root, tid, old_head)
    if err:
        return "error", err
    code, _ = git(wt, "reset", "--hard", old_head)
    if code != 0:
        return "error", "cannot reset staging to the integration HEAD"
    outcome, detail = run_dual_plan_round(
        Path(wt), wid, row, template, model, timeout, prompt_map
    )
    if outcome == "SELECTED":
        reg = Path(wt) / "docs" / "requirements" / "work-items.csv"
        if reg.exists():
            _rewrite_wi_rows(
                reg,
                {
                    wid: {
                        "Status": "done",
                        "Deliverable": "dual-plan round (train {}): {}".format(
                            tid, detail
                        ),
                    }
                },
            )
        generate_status(Path(wt) / "docs", root, last_train=tid)
    code, porcelain = git(wt, "status", "--porcelain")
    if code == 0 and not porcelain.strip():
        # A pre-artifact PAGE (missing goal brief/rubric) writes nothing.
        return outcome, detail
    regen_ok, regen_detail = _regenerate_disposition_artifacts(wt)
    if not regen_ok:
        # Ratified WI-223 posture: selected rows and their generated views are
        # one atomic disposition. Preserve the round and surface validation;
        # never make a known-invalid registry authoritative.
        return "error", _reset_failed_disposition(root, wt, tid, old_head, regen_detail)
    git(wt, "add", "-A")
    msg = "dual-plan {}: {} (train {})\n\nDual-Plan-WI: {}\nTrain: {}\n".format(
        "select" if outcome == "SELECTED" else "page", wid, tid, wid, tid
    )
    code, out = git(wt, "commit", "-q", "-m", msg)
    if code != 0:
        commit_detail = "dual-plan disposition commit failed: {}".format(out[:200])
        return "error", _reset_failed_disposition(
            root, wt, tid, old_head, commit_detail
        )
    code, new_head = git(wt, "rev-parse", "HEAD")
    if not cas_ref(root, INTEGRATION_REF, new_head.strip(), old_head):
        # The dispatcher loop is single-threaded, so a stale CAS means an
        # EXTERNAL actor moved the ref mid-round — surface, never overwrite.
        cas_detail = "integration ref moved externally during the round"
        return "error", _reset_failed_disposition(root, wt, tid, old_head, cas_detail)
    journal.event(
        "dual-plan-" + ("selected" if outcome == "SELECTED" else "paged"),
        train=tid,
        wi=wid,
        detail=detail[:200],
    )
    return outcome, detail


def _intent_meta(root):
    """(sha, meta) of the current publish intent, or (None, None). Unreadable
    metadata returns (sha, None) — recovery evidence, never overwritten
    silently."""
    code, sha = git(root, "rev-parse", "--verify", "--quiet", PUBLISH_INTENT_REF)
    if code != 0 or not sha.strip():
        return None, None
    return sha.strip(), reservation_meta(root, sha.strip())


def _publish_diff_paths(root, base, target):
    """Tracked paths the publication advances: `git diff --name-only` between
    `base` and `target`, NUL-delimited so Git never C-quotes special path
    bytes (as WI-224's salvage scans do) and `--no-renames` so BOTH sides of a
    rename are listed — the disjointness test must never miss a touched path.
    None when git cannot be read."""
    code, out = git(root, "diff", "--name-only", "-z", "--no-renames", base, target)
    if code != 0:
        return None
    return {p for p in out.split("\0") if p}


def _worktree_dirt(root, base):
    """Tracked paths whose worktree OR index differs from `base` — the user
    dirt measured against the pre-publication baseline. Untracked files never
    count (the never-stash contract); `git diff` ignores them. NUL-delimited,
    rename-split as above. None when git cannot be read."""
    dirt = set()
    for scan in (("diff",), ("diff", "--cached")):
        code, out = git(root, *scan, "--name-only", "-z", "--no-renames", base)
        if code != 0:
            return None
        dirt.update(p for p in out.split("\0") if p)
    return dirt


def _untracked_paths(root):
    """Untracked, non-ignored working-tree paths (`ls-files --others
    --exclude-standard -z`). Ignored files are excluded to match git's own
    checkout machinery, which overwrites those without complaint. None when
    git cannot be read."""
    code, out = git(root, "ls-files", "--others", "--exclude-standard", "-z")
    if code != 0:
        return None
    return {p for p in out.split("\0") if p}


def _publish_dirt(root, base, target):
    """Classify the primary worktree for a publication that advances `base` to
    `target` (spec §9 disjointness rule):

    - `clean` — no tracked dirt vs `base`: the mechanically-stale / at-baseline
      case, finished by the exact-hash `reset --hard`;
    - `disjoint` — tracked dirt exists but no dirty path is in the
      `base..target` diff: the edits ride the sync forward untouched;
    - `intersect` — a dirty path is also published, OR an untracked file sits at
      a path the publication would materialize: defer, never reset/stash;
    - `error` — git could not be read.

    An untracked file at a published path would be clobbered by `reset --hard`
    (and is refused by `read-tree`); classifying it here defers BEFORE the
    dev-ref CAS so the file is never lost and the dev ref never moves. No
    path-name allowlist: disjointness derives what a hardcoded list (the owner
    scratchpad, the generated run-state) would only approximate."""
    diff = _publish_diff_paths(root, base, target)
    if diff is None:
        return "error"
    untracked = _untracked_paths(root)
    if untracked is None:
        return "error"
    if untracked & diff:
        return "intersect"
    dirt = _worktree_dirt(root, base)
    if dirt is None:
        return "error"
    if not dirt:
        return "clean"
    return "intersect" if (dirt & diff) else "disjoint"


def _carry_dirt_forward(root, base, target):
    """Advance the worktree/index from `base` to descendant `target` with git's
    own two-way merge (`read-tree -m -u`): it updates the published paths and
    keeps uncommitted edits to every OTHER path byte-for-byte. Git REFUSES
    (nonzero) rather than clobber a locally-modified published path — the
    backstop that upholds the never-reset-user-edits contract even if a caller
    misjudged disjointness. True on a completed sync; a refusal defers."""
    code, _ = git(root, "read-tree", "-m", "-u", base, target)
    return code == 0


def _sync_worktree(root, base, target):
    """Bring the primary worktree from `base` to `target` under the disjointness
    rule (spec §9/§11): 'clean' (exactly at `base`) → the exact-hash
    `reset --hard`; disjoint dirt → carry it forward across git's own merge;
    intersecting dirt, a refused carry, or an unreadable tree leaves the
    checkout untouched. Returns 'synced', 'deferred', or 'error'."""
    disp = _publish_dirt(root, base, target)
    if disp == "error":
        return "error"
    if disp == "clean":
        code, _ = git(root, "reset", "--hard", target)
        return "synced" if code == 0 else "error"
    if disp == "disjoint" and _carry_dirt_forward(root, base, target):
        return "synced"
    return "deferred"


def publish_integration(root, journal, dev_branch):
    """Publish the integration HEAD to the development branch (spec §9): when no
    uncommitted edit intersects the publish diff (disjoint dirt rides the sync
    forward untouched); guarded by the durable publish-intent ref written before
    the dev-ref CAS and deleted only after the verified sync. Returns
    (state, detail) where state is 'published', 'deferred', 'noop', or
    'error'."""
    target = integration_head(root)
    if not target:
        return "noop", "no integration ref"
    dev_ref = "refs/heads/" + dev_branch
    code, dev_head = git(root, "rev-parse", "--verify", "--quiet", dev_ref)
    if code != 0:
        return "error", "development ref {} unreadable".format(dev_ref)
    dev_head = dev_head.strip()
    intent_sha, intent = _intent_meta(root)

    if dev_head == target:
        # Published already (this or a prior attempt). A dirty checkout with a
        # PENDING intent is the crash-window recovery: sync against the intent's
        # expected old hash. Without a pending intent there is no sync to
        # finish, so publication is simply complete — any (disjoint) worktree
        # dirt is its owner's, left alone (the post-publish idempotent replay).
        code, porcelain = git(root, "status", "--porcelain")
        tracked_dirty = [
            ln for ln in porcelain.splitlines() if ln and not ln.startswith("??")
        ]
        if tracked_dirty and intent_sha:
            diverges = (
                "development ref already at the target but the worktree "
                "diverges — left untouched and reported, never reset"
            )
            base = intent.get("old") if intent else None
            if not base:
                # Unreadable/absent intent metadata: keep the ref as recovery
                # evidence, never sync against an unknown baseline.
                return "deferred", diverges
            # A mechanically stale checkout (still exactly at old) resets to
            # target; disjoint dirt is carried across; intersecting dirt or a
            # refused carry leaves the checkout untouched.
            outcome = _sync_worktree(root, base, target)
            if outcome == "error":
                return "error", "cannot inspect the primary worktree for publication"
            if outcome == "deferred":
                return "deferred", diverges
        if intent_sha:
            git(root, "update-ref", "-d", PUBLISH_INTENT_REF, intent_sha)
            journal.event("publish-intent-cleared", target=target[:12])
        return "noop", "development branch already at the integration head"

    # Defense in depth: publication is a fast-forward operation. Refuse any
    # caller that presents a target which does not retain the development
    # branch's current history.
    code, _ = git(root, "merge-base", "--is-ancestor", dev_head, target)
    if code != 0:
        journal.event(
            "publish-deferred",
            reason="non-descendant-target",
            integration_head=target,
            development_head=dev_head,
        )
        return "deferred", (
            "integration target {} is not a descendant of development head {}"
        ).format(target, dev_head)

    # Dirty-at-outset disjointness (spec §9): dirt that intersects the publish
    # diff defers (never stash/reset); dirt disjoint from it rides the sync
    # forward untouched, so publication proceeds. No path-name allowlist.
    disp = _publish_dirt(root, dev_head, target)
    if disp == "error":
        return "error", "cannot inspect the primary worktree for publication"
    if disp == "intersect":
        journal.event("publish-deferred", reason="dirty-worktree")
        return "deferred", (
            "primary worktree carries uncommitted edits to a path the "
            "publication would advance — deferred, checkout untouched"
        )

    # The durable intent: {target, old, ref}. Reuse only an EXACT match; a
    # differing intent is replaced by an expected-old-object CAS (a failed
    # prior attempt retained as evidence until this recomposition).
    meta = {
        "train": "publish",
        "wis": ["publish"],
        "base": target,
        "target": target,
        "old": dev_head,
        "ref": dev_ref,
    }
    if intent and (
        intent.get("target") == target
        and intent.get("old") == dev_head
        and intent.get("ref") == dev_ref
    ):
        new_intent = intent_sha  # identical — reuse
    else:
        code, tree = git(root, "rev-parse", target + "^{tree}")
        if code != 0:
            return "error", "cannot resolve the target tree"
        proc = subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "commit-tree",
                tree.strip(),
                "-p",
                target,
                "-m",
                json.dumps(meta, sort_keys=True),
            ],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
        )
        if proc.returncode != 0:
            return "error", "intent commit failed"
        new_intent = proc.stdout.strip()
        if intent_sha:
            ok = cas_ref(root, PUBLISH_INTENT_REF, new_intent, intent_sha)
        else:
            ok = cas_ref(root, PUBLISH_INTENT_REF, new_intent, None)
        if not ok:
            return "deferred", "publish intent raced; retrying next pass"
        journal.event("publish-intent", target=target[:12], old=dev_head[:12])

    _fault("post-intent")
    # Second CAS: the development ref, against the intent's expected old.
    if not cas_ref(root, dev_ref, target, dev_head):
        # Moved to a third hash: no publication occurred; the stale intent is
        # kept as recovery evidence through the next recomposition.
        journal.event("publish-cas-stale", ref=dev_ref)
        return "deferred", "development ref moved; recomposing from its new head"

    _fault("post-dev-cas")
    # Verified sync (spec §9/§11). Clean at the expected old hash → the exact
    # `reset --hard`. Dirt disjoint from the publish diff (already vetted at
    # outset) rides git's own two-way merge across the sync. Any intersection or
    # a post-CAS divergence defers: the intent ref still names the
    # pre-publication hash for the next pass.
    outcome = _sync_worktree(root, dev_head, target)
    if outcome == "error":
        return "error", "sync failed: could not reach the target tree"
    if outcome == "deferred":
        journal.event("publish-sync-deferred", reason="worktree-diverged")
        return "deferred", (
            "edits landed between the CAS and the sync — the intent ref "
            "identifies the pre-publication hash; sync deferred, not reset"
        )
    git(root, "update-ref", "-d", PUBLISH_INTENT_REF, new_intent)
    journal.event("published", ref=dev_ref, head=target[:12])
    return "published", target


def parse_jobs(value):
    """The --jobs/AGENT_JOBS value: a positive int, or `auto` (adaptive up to
    the configured ceiling — AGENT_JOBS_CEILING, default 2). Raises ValueError
    on anything else."""
    v = (str(value) or "").strip().lower()
    if v == "auto":
        try:
            ceiling = int(os.environ.get("AGENT_JOBS_CEILING", "2"))
        except ValueError:
            ceiling = 2
        return max(1, ceiling)
    n = int(v)  # ValueError propagates to the caller's preflight
    if n < 1:
        raise ValueError("--jobs must be >= 1, got {}".format(n))
    return n


# -----------------------------------------------------------------------------
# WI-186 (SR-065/SR-059; spec §13/§14): telemetry, banner, downstream migration
# -----------------------------------------------------------------------------

PARALLEL_READY_FILE = "parallel-ready"


def assess_migration(root):
    """The two audits that gate the two-worker promotion (spec §14 items 9-10).
    Returns a dict:

    - `safetyclass_ok` — every OPEN WI (queued/blocked/legacy-active) carries a
      resolvable, non-`unclassified` SafetyClass (schedule.classify over the
      declared value). A single unclassified open WI holds the whole repo at
      `--jobs 1` (an unaudited row cannot be promoted, §14.10).
    - `soft_edges` — the `(wi, soft-pred)` pairs the optimistic scheduler would
      treat as safe-to-run-concurrently; each must be human-audited before
      first parallel enable (§14.9).
    - `softedge_ok` — True when there are no soft edges, OR `docs/parallel-ready`
      records the human sign-off (its presence IS the recorded audit).
    - `legacy_active` / `legacy_tracks` — migration residue to reconcile.

    A FRESH scaffold passes by construction: no soft edges, every drafted WI
    classified, no legacy rows — so it runs parallel-by-default with no marker
    (SR-059). A MIGRATED repo holds at 1 until both audits pass."""
    wis = schedule.load_wis(
        schedule.load_rows(root / "docs" / "requirements" / "work-items.csv")
    )
    open_states = ("queued", "blocked", "active", "ready", "reserved")
    unclassified = []
    for w in wis:
        if w["status"] in open_states:
            sched_class, _ = schedule.classify(w)
            if sched_class == schedule.SCHED_UNCLASSIFIED:
                unclassified.append(w["id"])
    soft_edges = [(w["id"], s) for w in wis for s in w["soft"]]
    legacy_active = [w["id"] for w in wis if w["status"] == "active"]
    tracks_dir = root / "docs" / "tracks"
    legacy_tracks = (
        sorted(p.name for p in tracks_dir.iterdir() if p.is_dir())
        if tracks_dir.is_dir()
        else []
    )
    signed = (root / "docs" / PARALLEL_READY_FILE).exists()
    return {
        "safetyclass_ok": not unclassified,
        "unclassified": unclassified,
        "soft_edges": soft_edges,
        "softedge_ok": (not soft_edges) or signed,
        "signed": signed,
        "legacy_active": legacy_active,
        "legacy_tracks": legacy_tracks,
    }


def reconcile_legacy(root, journal, assessment):
    """Reconcile migration residue within the one compatibility window (§14.3-4):
    a legacy `active` WI row returns to `queued` with a logged finding (runtime
    activity is dispatcher state, not a tracked column); `docs/tracks/*` lanes
    stay readable but are flagged (the new dispatcher never schedules from
    them). Returns the count of reconciled active rows."""
    reg = root / "docs" / "requirements" / "work-items.csv"
    reconciled = []
    if assessment["legacy_active"] and reg.exists():
        updates = {w: {"Status": "queued"} for w in assessment["legacy_active"]}
        reconciled = _rewrite_wi_rows(reg, updates)
        if reconciled:
            journal.event(
                "legacy-active-reconciled",
                wis=";".join(reconciled),
                finding="active->queued (runtime activity is dispatcher state)",
            )
    if assessment["legacy_tracks"]:
        journal.event(
            "legacy-tracks-flagged",
            tracks=";".join(assessment["legacy_tracks"]),
            finding="docs/tracks/* readable this window; dispatcher never "
            "schedules from them (declare Priority/edges instead)",
        )
    return len(reconciled)


def resolve_ceiling(root, requested, journal):
    """Apply the migration gate to the requested worker ceiling (SR-065): a
    repo may run >1 worker only once BOTH audits pass. Returns (ceiling,
    assessment). A held repo drops to 1 with a reason-coded event; a repo that
    passes at a ceiling>1 for the first time records the deliberate promotion."""
    assessment = assess_migration(root)
    if requested <= 1:
        return 1, assessment
    if not assessment["safetyclass_ok"]:
        journal.event(
            "migration-hold",
            requested=requested,
            reason="unclassified-open-wi:" + ";".join(assessment["unclassified"]),
        )
        return 1, assessment
    if not assessment["softedge_ok"]:
        journal.event(
            "migration-hold",
            requested=requested,
            reason="soft-edge-audit-unsigned:{}-edge(s); review and create "
            "docs/parallel-ready".format(len(assessment["soft_edges"])),
        )
        return 1, assessment
    # Both audits pass — record the deliberate two-worker promotion once.
    if requested > 1:
        journal.event(
            "parallel-enabled",
            ceiling=requested,
            soft_edges=len(assessment["soft_edges"]),
        )
    return requested, assessment


def dispatch_banner(jobs, active, parked, cars, journal, integrating=0):
    """The one-line dispatcher banner (SR-065): active lanes, ready-frontier
    width, integration-queue depth, and the cost/concurrency ceiling — so
    parallel spend is visible at a glance."""
    ready_frontier = sum(len(c["wis"]) for c in cars)
    queued_to_integrate = sum(
        1
        for p in parked.values()
        if p["state"] in ("ready-to-integrate", "blocked", "train-end")
    )
    print(
        "dispatch banner | lanes {}/{} | frontier {} WI in {} car(s) | "
        "integration-queue {} | ceiling {}".format(
            len(active),
            jobs,
            ready_frontier,
            len(cars),
            queued_to_integrate,
            jobs,
        )
    )


def telemetry_summary(journal):
    """The end-of-run telemetry rollup (spec §13): the required measurements
    derived from the reason-coded event stream, aggregated by `(run, train,
    WI, session)`. Written to out/dispatch/telemetry.json and printed — the
    evidence a downstream adopter tunes capacity from."""
    events = []
    try:
        with (journal.dir / "events.jsonl").open(encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except ValueError:
                        continue
    except OSError:
        events = []
    run = journal.run_id
    mine = [e for e in events if e.get("run") == run]

    def count(name):
        return sum(1 for e in mine if e.get("event") == name)

    trains = sorted({e["train"] for e in mine if e.get("train")})
    summary = {
        "run": run,
        # ready-frontier decisions + reservation/worker/integration lifecycle
        "reservations": count("reserve"),
        "workers_started": count("worker-start"),
        "workers_done": count("worker-done"),
        "integrations": count("integrated"),
        "blocked_dispositions": count("blocked-disposition"),
        # overlap / conflict / re-review rates (spec §13 required measurements)
        "conflicts": count("integration-conflict"),
        # composition conflicts auto-resolved by regeneration/row-union (WI-231)
        "regenerated": count("integration-regenerated"),
        "re_reviews_needed": sum(
            1
            for e in mine
            if e.get("event") == "integration-parked"
            and e.get("state") == "needs-re-review"
        ),
        "rework_parks": sum(
            1
            for e in mine
            if e.get("event") == "integration-parked" and e.get("state") == "rework"
        ),
        # train continuation / early-end reasons
        "train_ends": count("worker-train-end"),
        "released_unstarted": count("release-unstarted"),
        # recovery outcomes
        "reconciles": count("reconcile"),
        "quarantines": count("quarantine"),
        "trains": trains,
        # combined-bar failures after individually-green trains
        "bar_failures": sum(
            1
            for e in mine
            if e.get("event") == "integration-bar"
            and e.get("result")
            not in (
                "pass",
                "skipped (no docs/stack.ini)",
                "skipped (no declared test command)",
            )
        ),
    }
    try:
        (journal.dir / "telemetry.json").write_text(
            json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8"
        )
    except OSError:
        pass
    print(
        "dispatch telemetry | {} reservation(s) -> {} integration(s), "
        "{} conflict(s)/{} re-review(s)/{} rework, {} recovery reconcile(s), "
        "{} quarantine(s), {} bar-failure(s) after green | trains: {}".format(
            summary["reservations"],
            summary["integrations"],
            summary["conflicts"],
            summary["re_reviews_needed"],
            summary["rework_parks"],
            summary["reconciles"],
            summary["quarantines"],
            summary["bar_failures"],
            ", ".join(trains) or "none",
        )
    )
    return summary


def _head_reconcile_decision(ihead, dhead, integration_is_ancestor, dev_is_ancestor):
    """Choose the launch-time ref action from an already-observed relation."""
    if ihead and dhead and ihead != dhead:
        if integration_is_ancestor and not dev_is_ancestor:
            return "fast-forward"
        if not integration_is_ancestor and not dev_is_ancestor:
            return "needs-human"
    return "publish"


def _train_evidence_decision(wis, built, blocked):
    """Classify proven branch evidence without reading refs or the registry."""
    foreign = (set(built) | set(blocked)) - set(wis)
    if foreign:
        return "quarantined", tuple(sorted(foreign))
    if blocked:
        return "blocked", ()
    if set(wis) <= set(built):
        return "ready-to-integrate", ()
    return "resume", ()


def _dispatch_allowed(paused, blacked_out, needs_human_ask):
    return paused is None and not blacked_out and not needs_human_ask


def _retry_due(state, now, retry_at):
    return state == "resume" or (state == "waiting" and now >= retry_at)


def _worker_exit_decision(code, spine, gate_policy):
    """Return the lane state, event, and human action for a worker exit."""
    if code == EXIT_DONE:
        ask = "ratify" if spine and gate_policy != "autonomous" else ""
        return "ready-to-integrate", "worker-done", ask
    if code == EXIT_BLOCKED:
        return "blocked", "worker-blocked", "release-unstarted"
    if code == EXIT_TRAIN_END:
        return "train-end", "worker-train-end", "release-unstarted"
    if code == EXIT_WAITING:
        return "waiting", "worker-waiting", "retry"
    if code == EXIT_NEEDS_HUMAN:
        return "needs-human", "worker-needs-human", "page"
    return "quarantined", "worker-quarantined", ""


def _integration_result_decision(result, source_state):
    """Map an integrator result to parked state and rescan/journal actions."""
    if result == "integrated":
        state = "integrated" if source_state == "ready-to-integrate" else "blocked-done"
        return state, True, False
    if result == "recompose":
        return source_state, True, False
    state = result if result != "error" else "quarantined"
    return state, False, True


def _idle_decision(paused, needs_human_ask, blacked_out, dispatchable, waiting):
    """Choose the no-active-lane action; the caller performs any effects."""
    if paused is not None:
        return "paused"
    if needs_human_ask:
        return "needs-human"
    if blacked_out and dispatchable:
        return "blackout-wait"
    if waiting and not dispatchable:
        return "waiting"
    if not dispatchable and not waiting:
        return "drained"
    return "poll"


def _terminal_decision(attention, queued_left, unpublished, current_head, blocked_rows):
    """Choose generated run-state, banner text, and exit code."""
    if attention:
        return (
            "RUNNING",
            "trains need attention (re-review / rework / quarantine)",
            EXIT_STALL,
        )
    if queued_left:
        return "RUNNING", "build-out wave complete", EXIT_DONE
    if unpublished and unpublished != current_head:
        return "RUNNING", "integration complete; publication deferred", EXIT_DONE
    if blocked_rows:
        return "BLOCKED", "run-state=BLOCKED", EXIT_BLOCKED
    return "DONE", "run-state=DONE", EXIT_DONE


def _reservation_trains(root, journal):
    """Read reservation metadata and group its proven claims by train."""
    trains = {}
    quarantined_wis = set()
    for wid, sha in sorted(list_reservations(root).items()):
        meta = reservation_meta(root, sha)
        if meta is None:
            journal.event("quarantine", wi=wid, reason="unreadable-reservation")
            quarantined_wis.add(wid)
            continue
        trains.setdefault(meta["train"], {"wis": [], "base": meta["base"]})
        trains[meta["train"]]["wis"].append(wid)
    return trains, quarantined_wis


def _reconcile_reserved_train(root, journal, tid, train, parked, quarantined_wis):
    """Apply effects for one durable train after pure evidence classification."""
    wis = train["wis"]
    base = train["base"]
    int_rows = registry_rows_at(root, INTEGRATION_REF) or []
    int_status = {
        (row.get("WI-ID") or "").strip(): (row.get("Status") or "").strip().lower()
        for row in int_rows
    }
    if wis and all(int_status.get(wid) == "done" for wid in wis):
        err = release_reservations(root, wis)
        if err:
            journal.event("release-failed", train=tid, reason=err[:200])
        clear_conflict(root, tid)  # WI-232: this train landed; drop any record
        parked[tid] = {"state": "integrated", "wis": wis, "base": base}
        journal.event("reconcile", train=tid, state="integrated")
        return
    code, _ = git(root, "rev-parse", "--verify", "--quiet", TRAIN_BRANCH_HEADS + tid)
    if code != 0:
        journal.event("quarantine", train=tid, reason="reservation-without-branch")
        quarantined_wis.update(wis)
        return
    built, blocked = train_branch_evidence(root, tid, base)
    state, foreign = _train_evidence_decision(wis, built, blocked)
    if foreign:
        journal.event(
            "quarantine",
            train=tid,
            reason="claims-unreserved-wi:" + ";".join(foreign),
        )
        quarantined_wis.update(wis)
        parked[tid] = {"state": state, "wis": wis, "base": base}
        return
    parked[tid] = {"state": state, "wis": wis, "base": base}
    journal.event("reconcile", train=tid, state=state)


def _reconcile_owned_trains(root, journal):
    parked = {}
    trains, quarantined_wis = _reservation_trains(root, journal)
    for tid, train in sorted(trains.items()):
        _reconcile_reserved_train(root, journal, tid, train, parked, quarantined_wis)
    return parked, quarantined_wis


def _spawn_worker(args, root, journal, active, parked, tid, wis, base, spine):
    wt, err = lease_worktree(root, tid)
    if err:
        journal.event("quarantine", train=tid, reason=err)
        parked[tid] = {"state": "quarantined", "wis": wis}
        return False
    argv = [
        sys.executable,
        str(_ENGINE),
        "--worktree",
        str(wt),
        "--wi",
        ";".join(wis),
        "--train",
        tid,
        "--base",
        base,
        "--max-iterations",
        str(args.worker_iterations),
        "--pause",
        str(args.pause),
        "--no-session-echo",
    ]
    if args.agent_cmd is not None:
        argv += ["--agent-cmd", args.agent_cmd]
    if args.model:
        argv += ["--model", args.model]
    if args.session_timeout:
        argv += ["--session-timeout", str(args.session_timeout)]
    logdir = journal.dir / "logs"
    out_fh = None
    try:
        logdir.mkdir(parents=True, exist_ok=True)
        out_fh = (logdir / (tid + ".out")).open("ab")
    except OSError:
        pass
    proc = subprocess.Popen(
        argv,
        cwd=str(wt),
        stdout=out_fh if out_fh is not None else subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
        stdin=subprocess.DEVNULL,
    )
    active[tid] = {
        "proc": proc,
        "wis": wis,
        "base": base,
        "worktree": str(wt),
        "spine": spine,
        "log_fh": out_fh,
    }
    journal.event(
        "worker-start", train=tid, wis=";".join(wis), pid=proc.pid, spine=spine
    )
    journal.train(tid, {"wis": wis, "base": base, "state": "building"})
    return True


def _close_worker_log(info):
    log_fh = info.get("log_fh")
    if log_fh is None:
        return
    try:
        log_fh.close()
    except OSError:
        pass


def _release_unstarted(root, journal, tid, info):
    built, blocked = train_branch_evidence(root, tid, info["base"])
    unstarted = [wid for wid in info["wis"] if wid not in built and wid not in blocked]
    err = release_reservations(root, unstarted)
    if err:
        journal.event("release-failed", train=tid, reason=err[:200])
    elif unstarted:
        journal.event("release-unstarted", train=tid, wis=";".join(unstarted))
    return [wid for wid in info["wis"] if wid not in unstarted]


def _worker_event_fields(state, code):
    if state == "ready-to-integrate":
        return {"state": state}
    if state == "waiting":
        return {"retry_s": TRAIN_RETRY_SECONDS}
    if state == "quarantined":
        return {"exit": code}
    return {}


def _handle_worker_exit(
    root, journal, active, parked, retry_at, tid, code, gate_policy
):
    info = active.pop(tid)
    _close_worker_log(info)
    state, event, action = _worker_exit_decision(code, info["spine"], gate_policy)
    wis = info["wis"]
    if action == "release-unstarted":
        wis = _release_unstarted(root, journal, tid, info)
    if action == "retry":
        retry_at[tid] = time.time() + TRAIN_RETRY_SECONDS
    parked[tid] = {"state": state, "wis": wis, "base": info["base"]}
    journal.event(event, train=tid, **_worker_event_fields(state, code))
    if state == "ready-to-integrate":
        journal.train(tid, {"wis": wis, "base": info["base"], "state": state})
    if action == "ratify":
        journal.event("gate-ratification-exit", train=tid)
        return "spine/gate train {} is built and needs ratification (docs/gate-policy: {})".format(
            tid, gate_policy
        )
    if action == "page":
        return "worker train {} paged (no routable model / escalation) — see {}".format(
            tid, journal.dir / "logs" / (tid + ".out")
        )
    return ""


def _resume_reconciled(args, root, journal, active, parked, retry_at, jobs):
    spine_active = any(lane["spine"] for lane in active.values())
    for tid, lane in sorted(parked.items()):
        if len(active) >= jobs or spine_active:
            break
        if _retry_due(lane.get("state"), time.time(), retry_at.get(tid, 0)):
            del parked[tid]
            _spawn_worker(
                args,
                root,
                journal,
                active,
                parked,
                tid,
                lane["wis"],
                lane["base"],
                spine=False,
            )


def _frontier_snapshot(root, quarantined_wis):
    reg_rows = registry_rows_at(root, INTEGRATION_REF)
    if reg_rows is None:
        reg_rows = schedule.load_rows(root / "docs" / "requirements" / "work-items.csv")
    wi_rows = {}
    for row in reg_rows:
        wid = (row.get("WI-ID") or "").strip()
        if WI_TOKEN_RE.match(wid) and wid not in wi_rows:
            wi_rows[wid] = row
    wis = schedule.load_wis(reg_rows)
    reserved = set(list_reservations(root)) | quarantined_wis
    records = schedule.evaluate(wis, reserved)
    cars = pack_traincars(records, {wi["id"]: wi for wi in wis})
    return wi_rows, cars


def _integrate_one_ready(root, docs, journal, tid, wis, base, required_verdicts):
    """Integrate a ready train under the WI-232 conflict-idempotence guard: a
    train whose merge inputs are UNCHANGED since a recorded needs-re-review
    conflict is NOT re-merged — it stays parked for the human (the identical
    3-way merge would only re-park). Inputs that changed (a new integration head
    or an amended train) retry the merge once, and any non-conflict outcome
    clears the record. Returns (result, detail) like integrate_train."""
    rec = read_conflict(root, tid)
    if rec is not None and _conflict_inputs_match(root, tid, rec):
        detail = rec.get("paths") or "textual conflict against the integrated tree"
        journal.event("integration-conflict-held", train=tid, detail=detail[:200])
        return "needs-re-review", detail
    result, detail = integrate_train(
        root, docs, journal, tid, wis, base, required_verdicts
    )
    if result not in ("needs-re-review", "recompose"):
        clear_conflict(root, tid)
    return result, detail


def _integrate_parked(root, docs, journal, parked, required_verdicts, needs_human):
    integrated_any = False
    for tid in sorted(parked):
        if needs_human:
            break
        source_state = parked[tid]["state"]
        if source_state not in ("ready-to-integrate", "blocked"):
            continue
        lane = parked[tid]
        base = lane.get("base")
        if not base:
            meta = reservation_meta(
                root, list_reservations(root).get(lane["wis"][0], "")
            )
            base = (meta or {}).get("base", "")
        if source_state == "ready-to-integrate":
            result, detail = _integrate_one_ready(
                root, docs, journal, tid, lane["wis"], base, required_verdicts
            )
        else:
            result, detail = blocked_disposition(
                root, docs, journal, tid, lane["wis"], base
            )
        next_state, ref_moved, should_journal = _integration_result_decision(
            result, source_state
        )
        if result != "recompose":
            parked[tid] = {"state": next_state, "wis": lane["wis"]}
        integrated_any = integrated_any or ref_moved
        if should_journal:
            journal.event(
                "integration-parked", train=tid, state=result, detail=detail[:200]
            )
    return integrated_any


def _apply_idle_action(action, root, docs, parked, needs_human_ask):
    if action == "paused":
        stop_banner(
            docs / "status.md",
            "paused (docs/pause present)",
            "no new reservations; delete docs/pause and relaunch to "
            "resume ({} in-flight train(s) already wrapped safely).".format(
                len(parked)
            ),
        )
        return EXIT_PAUSED
    if action == "needs-human":
        _write_runstate(docs, "NEEDS-HUMAN", needs_human_ask)
        stop_banner(docs / "status.md", "NEEDS-HUMAN", needs_human_ask)
        return EXIT_NEEDS_HUMAN
    if action == "blackout-wait":
        wake = blackout_wake(
            read_declared(docs / "blackout", ""), datetime.datetime.utcnow()
        )
        time.sleep(min(wake or 60, 60))
        return "continue"
    if action == "waiting":
        _write_runstate(docs, "RUNNING")
        stop_banner(
            docs / "status.md",
            "WAITING on rate limits",
            "every dispatchable train is rate-limited; relaunch later.",
        )
        return EXIT_WAITING
    if action == "drained":
        return "break"
    return None


def _needs_review_ask(root, parked):
    """The WI-127 ask for trains parked on a source-conflict re-review (WI-232,
    option (b)): name each train and its conflicted path(s), read from the
    durable conflict record. Empty when no train is parked needs-re-review —
    those conflicts are genuine human merges the dispatcher must not retry."""
    trains = sorted(
        tid for tid, lane in parked.items() if lane["state"] == "needs-re-review"
    )
    if not trains:
        return ""
    parts = []
    for tid in trains:
        rec = read_conflict(root, tid)
        paths = (rec or {}).get(
            "paths"
        ) or "textual conflict against the integrated tree"
        parts.append("{} ({})".format(tid, paths))
    return (
        "re-review needed — resolve the source conflict by hand (merge/rebase "
        "the train), then relaunch: " + "; ".join(parts)
    )


def _finish_dispatch(root, docs, journal, parked):
    telemetry_summary(journal)
    # WI-232: a train parked on a real source conflict is HUMAN work — page
    # NEEDS-HUMAN with an ask naming the train(s) and path(s) instead of the
    # silent RUNNING/STALL that let an operator relaunch expecting progress.
    review_ask = _needs_review_ask(root, parked)
    if review_ask:
        _write_runstate(docs, "NEEDS-HUMAN", review_ask)
        stop_banner(docs / "status.md", "NEEDS-HUMAN", review_ask)
        return EXIT_NEEDS_HUMAN
    integrated = [
        tid
        for tid, lane in parked.items()
        if lane["state"] in ("integrated", "blocked-done")
    ]
    attention_states = {
        "quarantined",
        "needs-human",
        "needs-re-review",
        "rework",
        "dual-paged",
    }
    attention = [
        tid
        for tid, lane in parked.items()
        if lane["state"] in attention_states
        or (lane["state"] == "train-end" and lane["wis"])
    ]
    blocked_done = [
        tid for tid, lane in parked.items() if lane["state"] == "blocked-done"
    ]
    reg_rows = registry_rows_at(root, INTEGRATION_REF) or schedule.load_rows(
        root / "docs" / "requirements" / "work-items.csv"
    )
    wis = schedule.load_wis(reg_rows)
    reserved = set(list_reservations(root))
    queued_count = sum(
        1 for wi in wis if wi["status"] == "queued" and wi["id"] not in reserved
    )
    queued_left = bool(queued_count)
    blocked_rows = any(wi["status"] == "blocked" for wi in wis)
    summary = (
        "trains: {} integrated ({} blocked-disposition), {} needing attention "
        "(re-review/rework/quarantine/partial); {} unreserved queued WI(s) remain"
    ).format(len(integrated), len(blocked_done), len(attention), queued_count)
    unpublished = ""
    current_head = ""
    if not attention and not queued_left:
        unpublished = integration_head(root)
        if unpublished:
            current_head = head_sha_full(root)
    run_state, banner, exit_code = _terminal_decision(
        attention, queued_left, unpublished, current_head, blocked_rows
    )
    _write_runstate(docs, run_state)
    detail = summary
    if banner == "integration complete; publication deferred":
        detail += " — clean the checkout and relaunch to publish."
    stop_banner(docs / "status.md", banner, detail)
    return exit_code


def dispatch_run(args, root):
    """The dispatcher/integrator loop (SR-061): reconcile -> gate -> build-out.

    Returns an exit code. Concurrency is bounded by --jobs; every worker exit,
    block, or reservation event triggers a rescan (dynamic refill — never a
    static wave). Spine-class traincars serialize whole-project: one runs with
    every other lane drained, and nothing else dispatches meanwhile."""
    docs = root / "docs"
    journal = _Journal(root)
    try:
        jobs = parse_jobs(args.jobs)
    except ValueError as exc:
        print("agent_loop: --jobs: {}".format(exc), file=sys.stderr)
        return EXIT_PREFLIGHT
    try:
        # The dual-round hat overrides (WI-209): the same --prompt-map surface
        # the serial --dual-plan entry honors, parsed once for the whole run.
        dual_prompt_map = parse_map(args.prompt_map)
    except ValueError as exc:
        print("agent_loop: --prompt-map: {}".format(exc), file=sys.stderr)
        return EXIT_PREFLIGHT

    template = (
        args.agent_cmd
        if args.agent_cmd is not None
        else os.environ.get("AGENT_CMD", "")
    )
    failures = preflight(root, template, args)
    if failures:
        print("agent_loop: preflight failed —", file=sys.stderr)
        for f in failures:
            print("  - " + f, file=sys.stderr)
        return EXIT_PREFLIGHT

    # One dispatcher per checkout — the same kernel lock the legacy loop takes,
    # so a legacy coordinator and a dispatcher can never grind one worktree.
    lock_err = acquire_lock(root / "out" / "agent-loop.lock")
    if lock_err:
        print("agent_loop: {}".format(lock_err), file=sys.stderr)
        return EXIT_PREFLIGHT
    atexit.register(release_lock, root / "out" / "agent-loop.lock")

    gate_policy = read_declared(docs / "gate-policy", "attended")
    # The integrator's review requirement: managed routing + the reviewer dial
    # decide how many exact-head APPROVE verdicts a train needs to integrate.
    managed = bool(agent_route.load_enabled(docs / "agents-enabled"))
    try:
        rp_int = max(0, min(2, int(read_declared(docs / "review-policy", "1"))))
    except ValueError:
        rp_int = 1
    required_verdicts = rp_int if managed else 0

    # The selected development branch — the publication target. A detached
    # dispatcher checkout has no publishable projection: fail closed.
    code, dev_branch = git(root, "branch", "--show-current")
    if code != 0 or not dev_branch.strip():
        print(
            "agent_loop: the dispatcher requires a checked-out development "
            "branch (detached HEAD cannot receive publications).",
            file=sys.stderr,
        )
        return EXIT_PREFLIGHT
    dev_branch = dev_branch.strip()

    # The downstream-migration gate (SR-065, spec §14): a repo runs >1 worker
    # only once its soft-edge AND SafetyClass audits pass; until then it holds
    # at --jobs 1. A fresh scaffold passes by construction. Legacy `active`
    # rows + docs/tracks/* reconcile within this one compatibility window.
    requested_jobs = jobs
    jobs, assessment = resolve_ceiling(root, jobs, journal)
    reconcile_legacy(root, journal, assessment)

    print("=== parallel dispatcher (scripts/agent_loop.py --jobs {}) ===".format(jobs))
    if jobs < requested_jobs:
        hold = (
            "unclassified open WI(s): " + ";".join(assessment["unclassified"])
            if not assessment["safetyclass_ok"]
            else "{} unaudited soft edge(s) — sign off by creating "
            "docs/parallel-ready".format(len(assessment["soft_edges"]))
        )
        print(
            "MIGRATION HOLD: requested {} worker(s) but held at 1 until the "
            "migration audits pass ({}). See the downstream-resync skill.".format(
                requested_jobs, hold
            )
        )
    print(
        "repo: {} | gate-policy: {} | dev branch: {} | worktrees: {} | run {}".format(
            root, gate_policy, dev_branch, worktree_root(root), journal.run_id
        )
    )
    print(
        "CONSENT: workers run headless with the wired permission-bypass "
        "template; reservations + train branches are durable Git state."
    )

    # The integration ref is the authoritative integrated disposition (spec
    # §11); create it only on a genuine cold start, else fail closed.
    _ihead, err = ensure_integration_ref(root, journal)
    if err:
        print("agent_loop: {}".format(err), file=sys.stderr)
        return EXIT_PREFLIGHT
    # Reconcile the integration ref against the development branch at launch
    # (spec §9 "creates or reconciles it from the selected development branch").
    # Classify the relationship BEFORE acting so a human's new work is never
    # discarded by a mistaken publish:
    ihead = integration_head(root)
    dhead = head_sha_full(root)
    int_is_anc = False
    dev_is_anc = False
    if ihead and dhead and ihead != dhead:
        int_is_anc = git(root, "merge-base", "--is-ancestor", ihead, dhead)[0] == 0
        dev_is_anc = git(root, "merge-base", "--is-ancestor", dhead, ihead)[0] == 0
    head_action = _head_reconcile_decision(ihead, dhead, int_is_anc, dev_is_anc)
    if head_action == "needs-human":
        ask = (
            "integration head {} and development head {} have diverged; "
            "preserve both histories, then merge/rebase development onto "
            "integration or explicitly restore the intended ref"
        ).format(ihead, dhead)
        journal.event(
            "integration-diverged",
            integration_head=ihead,
            development_head=dhead,
            ask=ask,
        )
        _write_runstate(docs, "NEEDS-HUMAN", ask)
        stop_banner(Path(docs) / "status.md", "NEEDS-HUMAN", ask)
        print("dispatch: NEEDS-HUMAN — {}".format(ask), file=sys.stderr)
        return EXIT_NEEDS_HUMAN
    if head_action == "fast-forward":
        # Dev is strictly AHEAD of integration: a human added WIs on the
        # development branch. Fast-forward the ref to absorb that new work
        # (never over unpublished integration commits — the divergent case
        # above is logged and left for a human/later rung).
        if cas_ref(root, INTEGRATION_REF, dhead, ihead):
            journal.event("integration-fast-forward", head=dhead[:12])
    else:
        # Integration ahead-or-equal of dev: resume any interrupted publication
        # idempotently (this also finishes a crash-stranded worktree sync when
        # the dev ref already equals the integration head, spec §11).
        state, detail = publish_integration(root, journal, dev_branch)
        if state == "published":
            print(
                "dispatch: resumed an interrupted publication ({})".format(detail[:12])
            )

    # --- stage 1: reconcile owned trains to a clean baseline (spec §4.1) -----
    # Group durable reservation claims into trains; resume the incomplete,
    # park the built (ready-to-integrate, Slice F), quarantine the unreadable.
    active = {}  # train_id -> {proc, wis, base, worktree, spine}
    parked, quarantined_wis = _reconcile_owned_trains(root, journal)
    retry_at = {}  # train_id -> epoch when a WAITING train may retry
    needs_human_ask = ""

    # --- stages 2+3: gate-first, then build-out with dynamic refill ----------
    # The lowest-gate-first order (schedule.py) puts spine/gate work at the
    # frontier head; the dispatcher serializes it whole-project by draining
    # every other lane before it runs and dispatching nothing beside it.
    last_banner_sig = None
    while True:
        # Pause: stop NEW reservations at this boundary; in-flight workers
        # finish their safe boundary and stay recoverable (spec §12).
        # Blackout: start no NEW worker inside the window (spec §12); the
        # in-flight ones continue (their own session loop honors it too).
        paused = pause_reason(docs)
        blacked_out = bool(
            blackout_wake(
                read_declared(docs / "blackout", ""), datetime.datetime.utcnow()
            )
        )
        may_dispatch = _dispatch_allowed(paused, blacked_out, needs_human_ask)

        if may_dispatch:
            # Resume reconciled trains first (they already hold reservations).
            _resume_reconciled(args, root, journal, active, parked, retry_at, jobs)

        # Scan the frontier every pass (cheap, and the end-state test below
        # needs it even while paused/blacked out). Once the integration ref
        # exists it is the authoritative integrated disposition (spec §11) —
        # the development checkout is only its published projection.
        wi_rows, cars = _frontier_snapshot(root, quarantined_wis)

        if may_dispatch:
            spine_active = any(a["spine"] for a in active.values())
            for car in cars:
                if len(active) >= jobs or spine_active or needs_human_ask:
                    break
                is_spine = car["sched_class"] in (
                    schedule.SCHED_SPINE_SERIAL,
                    schedule.SCHED_PROTECTED,
                )
                if is_spine and active:
                    break  # spine serializes whole-project: drain lanes first
                first = car["wis"][0]
                tid = "{}-{}-{}".format(
                    train_phase_gate(root, wi_rows, first),
                    first,
                    "%04x" % int.from_bytes(os.urandom(2), "big"),
                )
                # New trains compose from the CURRENT integration HEAD (spec
                # §9) — never from the (possibly stale) development checkout.
                base = integration_head(root) or head_sha_full(root)
                err = reserve_traincar(root, tid, car["wis"], base)
                if err:
                    journal.event("reserve-failed", train=tid, reason=err[:200])
                    continue
                journal.event(
                    "reserve",
                    train=tid,
                    wis=";".join(car["wis"]),
                    cls=car["sched_class"],
                    base=base[:12],
                )
                row0 = wi_rows.get(first) or {}
                if len(car["wis"]) == 1 and wi_plan_mode(row0) == PLAN_MODE_DUAL:
                    # WI-209 (the SR-066 auto-dispatch AC): a dual row's
                    # traincar — always single-WI, the classifier derives it
                    # from the PlanMode signal — runs the decomposition round
                    # in the dispatcher itself instead of spawning a BUILD
                    # worker (the worker path keeps its fail-closed refusal as
                    # the backstop). The run is synchronous, so rounds
                    # naturally serialize: one at a time, never packed.
                    import plan_round as _plan_round

                    outcome, detail = dual_plan_disposition(
                        root,
                        journal,
                        tid,
                        first,
                        row0,
                        template,
                        args.model,
                        args.session_timeout or None,
                        dual_prompt_map,
                    )
                    if outcome == "SELECTED":
                        err = release_reservations(root, car["wis"])
                        if err:
                            journal.event("release-failed", train=tid, reason=err[:200])
                        parked[tid] = {"state": "integrated", "wis": car["wis"]}
                        state_pub, detail_pub = publish_integration(
                            root, journal, dev_branch
                        )
                        if state_pub == "deferred":
                            print(
                                "dispatch: publication deferred — {}".format(detail_pub)
                            )
                        break  # the ref advanced: rescan (children just filed)
                    if outcome == "error":
                        journal.event(
                            "dual-plan-error", train=tid, wi=first, reason=detail[:200]
                        )
                        quarantined_wis.add(first)
                        parked[tid] = {
                            "state": "quarantined",
                            "wis": car["wis"],
                            "base": base,
                        }
                        continue
                    # PAGE: the CLI entry's gate-policy mapping, dispatcher-side
                    # (plan_round.page_action) — attended stops for the human,
                    # autonomous routes on without pausing disjoint work (the
                    # pause-free-under-autonomous invariant).
                    action = _plan_round.page_action(gate_policy)
                    journal.event(
                        "dual-plan-page-action", train=tid, wi=first, action=action
                    )
                    if action == "stop-needs-human":
                        parked[tid] = {
                            "state": "needs-human",
                            "wis": car["wis"],
                            "base": base,
                        }
                        needs_human_ask = (
                            "dual-plan round for {} paged: {} — resolve, then "
                            "relaunch (or run agent_loop --dual-plan {})".format(
                                first, detail, first
                            )
                        )
                    else:
                        err = release_reservations(root, car["wis"])
                        if err:
                            journal.event("release-failed", train=tid, reason=err[:200])
                        quarantined_wis.add(first)
                        parked[tid] = {
                            "state": "dual-paged",
                            "wis": car["wis"],
                            "base": base,
                        }
                    continue
                _spawn_worker(
                    args,
                    root,
                    journal,
                    active,
                    parked,
                    tid,
                    car["wis"],
                    base,
                    spine=is_spine,
                )
                if is_spine:
                    break

        # --- the serialized integrator (WI-184, SR-063): one logical writer,
        # deterministic queue order, CAS-advanced. Ready trains compose one at
        # a time; a worker-reported blocker takes the smaller disposition
        # transaction. Each success is followed by a publication attempt and
        # triggers a fresh rescan (the frontier may have grown).
        integrated_any = _integrate_parked(
            root,
            docs,
            journal,
            parked,
            required_verdicts,
            needs_human_ask,
        )
        if integrated_any:
            state_pub, detail_pub = publish_integration(root, journal, dev_branch)
            if state_pub == "deferred":
                print("dispatch: publication deferred — {}".format(detail_pub))

        journal.manifest(
            {
                "jobs": jobs,
                "run": journal.run_id,
                "active": {t: a["wis"] for t, a in active.items()},
                "parked": {t: p["state"] for t, p in parked.items()},
                "updated": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
        )
        # The banner (SR-065) — only when the picture changed, so the poll loop
        # does not spam it every cadence tick.
        banner_sig = (
            len(active),
            tuple(sorted(p["state"] for p in parked.values())),
            sum(len(c["wis"]) for c in cars),
        )
        if banner_sig != last_banner_sig:
            dispatch_banner(jobs, active, parked, cars, journal)
            last_banner_sig = banner_sig
        if integrated_any:
            continue  # the integrated frontier may have unlocked successors

        if not active:
            waiting = [t for t, p in parked.items() if p["state"] == "waiting"]
            resumable = [t for t, p in parked.items() if p["state"] == "resume"]
            dispatchable = bool(cars) or bool(resumable)
            idle_action = _idle_decision(
                paused, needs_human_ask, blacked_out, dispatchable, waiting
            )
            idle_result = _apply_idle_action(
                idle_action, root, docs, parked, needs_human_ask
            )
            if idle_result == "continue":
                continue
            if idle_result == "break":
                break  # frontier + lanes drained — evaluate the end state
            if idle_result is not None:
                return idle_result

        # Poll workers; every exit is a rescan trigger (dynamic refill).
        exited = [
            (t, a["proc"].poll())
            for t, a in list(active.items())
            if a["proc"].poll() is not None
        ]
        for tid, code in exited:
            ask = _handle_worker_exit(
                root,
                journal,
                active,
                parked,
                retry_at,
                tid,
                code,
                gate_policy,
            )
            needs_human_ask = ask or needs_human_ask
        if not exited:
            time.sleep(args.poll_seconds)

    # --- end state (spec §10: run-state is a generated dispatcher outcome) ---
    return _finish_dispatch(root, docs, journal, parked)
