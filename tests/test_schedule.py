"""Scheduler contract fixtures — SR-057 (frontier + deterministic order) and
SR-058 (deterministic safety classification). Verifies TC-058 / TC-059.

Unit-level and fast (in the smoke tier by default): the scheduler is a pure
library over in-memory registry rows, so these never bootstrap a scaffold. Two
CLI tests exercise `schedule.py ready --format json` end-to-end over a temp
registry to pin the shared decision across the CLI surface."""

import json

from conftest import SCRIPTS, load_script, run_py

sched = load_script("schedule")

# The two concurrency values, named once — several fixtures below read them.
EXCL, PAR = sched.CONCURRENCY_EXCLUSIVE, sched.CONCURRENCY_PARALLEL


def row(wid, status="queued", preds="", safety="ordinary", **kw):
    """A raw registry row as csv.DictReader would yield it."""
    r = {
        "WI-ID": wid,
        "Title": kw.get("title", wid),
        "Status": status,
        "Predecessors": preds,
        "SafetyClass": safety,
        "Priority": kw.get("priority", ""),
        "Exclusive": kw.get("exclusive", ""),
        "SR-Refs": kw.get("srs", ""),
        "BlockRef": kw.get("blockref", ""),
        "EstTokens": kw.get("est", ""),
        "PlanMode": kw.get("PlanMode", ""),
    }
    return r


def ready_ids(wis, reserved=None):
    return [r["id"] for r in sched.frontier(wis, reserved)]


def disposition(wis, wid, reserved=None):
    return next(r for r in sched.evaluate(wis, reserved) if r["id"] == wid)


# --- SR-057: frontier + deterministic order ----------------------------------
def test_independent_roots_fill_all_workers():
    wis = sched.load_wis([row("WI-001"), row("WI-002"), row("WI-003")])
    assert ready_ids(wis) == ["WI-001", "WI-002", "WI-003"]
    assert sched.simulate(wis, 3) == [["WI-001", "WI-002", "WI-003"]]
    assert sched.simulate(wis, 2) == [["WI-001", "WI-002"], ["WI-003"]]


def test_direct_and_transitive_hard_deps_never_coschedule():
    wis = sched.load_wis(
        [row("WI-001"), row("WI-002", preds="WI-001"), row("WI-003", preds="WI-002")]
    )
    assert ready_ids(wis) == ["WI-001"]  # only the root is ready
    # A transitive chain schedules strictly serially even with many workers.
    assert sched.simulate(wis, 4) == [["WI-001"], ["WI-002"], ["WI-003"]]


def test_soft_edge_does_not_block():
    wis = sched.load_wis([row("WI-001"), row("WI-002", preds="~WI-001")])
    assert ready_ids(wis) == ["WI-001", "WI-002"]  # soft ~edge never blocks


def test_hard_pred_satisfied_by_done_predecessor():
    wis = sched.load_wis([row("WI-001", status="done"), row("WI-002", preds="WI-001")])
    assert ready_ids(wis) == ["WI-002"]


def test_dangling_hard_pred_fails_closed():
    wis = sched.load_wis([row("WI-002", preds="WI-999")])  # WI-999 absent
    assert ready_ids(wis) == []
    assert disposition(wis, "WI-002")["disposition"] == "waiting"


# --- WI-267: `cancelled` is a terminal WON'T-BUILD status ---------------------
# (Spelled `retired` until WI-384 gave it its own directory and, with it, an
# unambiguous name — `retired` can be read as finished-and-put-out-to-pasture.)
# Terminal like `done` (never ready, never scheduled) but — unlike `done` — a
# cancelled predecessor does NOT satisfy a successor's hard dependency (design-
# decision 3), so a live WI hard-blocked on a cancelled one surfaces rather than
# proceeding on a will-never-happen dependency.


def test_cancelled_wi_is_terminal_never_ready():
    wis = sched.load_wis([row("WI-001", status="cancelled")])
    assert ready_ids(wis) == []
    d = disposition(wis, "WI-001")
    assert d["disposition"] == "cancelled"
    assert d["reasons"] == ["cancelled:terminal-wont-build"]


def test_cancelled_predecessor_does_not_satisfy_a_hard_dependency():
    # Decision 3 (the DEAD-edge direction): a cancelled predecessor never
    # integrates, so the live successor can never become ready — it stays
    # `waiting`, and the dead edge is surfaced as its own reason code.
    wis = sched.load_wis(
        [row("WI-001", status="cancelled"), row("WI-002", preds="WI-001")]
    )
    assert ready_ids(wis) == []  # NOT satisfied the way a `done` pred would be
    d = disposition(wis, "WI-002")
    assert d["disposition"] == "waiting"
    assert "waiting:hard-pred-cancelled:WI-001" in d["reasons"]


def test_done_predecessor_still_satisfies_a_hard_dependency():
    # Decision 3 (the LIVE-edge direction, the control): a `done` pred DOES
    # satisfy — cancellation is the only terminal that leaves the edge dead.
    wis = sched.load_wis([row("WI-001", status="done"), row("WI-002", preds="WI-001")])
    assert ready_ids(wis) == ["WI-002"]


def test_cancelled_wi_is_never_scheduled_in_simulate():
    wis = sched.load_wis(
        [row("WI-001", status="cancelled"), row("WI-002"), row("WI-003")]
    )
    scheduled = [wid for rnd in sched.simulate(wis, 4) for wid in rnd]
    assert "WI-001" not in scheduled
    assert set(scheduled) == {"WI-002", "WI-003"}


# --- WI-384: `draft` is never-ready, exactly like `deferred` ------------------


def test_draft_is_never_ready_and_keeps_its_own_reason_code():
    """The two never-ready OPEN states differ only in what they SAY. Asserting
    both in one place is what stops a later edit folding `draft` into
    `deferred`: they would still both be excluded, and the --explain output
    would quietly stop distinguishing a decision from the absence of one."""
    wis = sched.load_wis(
        [row("WI-001", status="draft"), row("WI-002", status="deferred")]
    )
    assert ready_ids(wis) == []
    draft, deferred = disposition(wis, "WI-001"), disposition(wis, "WI-002")
    assert (draft["disposition"], draft["reasons"]) == ("draft", ["excluded:draft"])
    assert (deferred["disposition"], deferred["reasons"]) == (
        "deferred",
        ["excluded:deferred"],
    )


def test_draft_wi_is_never_scheduled_in_simulate():
    wis = sched.load_wis([row("WI-001", status="draft"), row("WI-002"), row("WI-003")])
    scheduled = [wid for rnd in sched.simulate(wis, 4) for wid in rnd]
    assert "WI-001" not in scheduled
    assert set(scheduled) == {"WI-002", "WI-003"}


def test_priority_outranks_downstream_within_a_rank():
    # WI-050: higher Priority but zero downstream. WI-010: default Priority but two
    # downstream dependents. Priority must win within one rank.
    wis = sched.load_wis(
        [
            row("WI-010"),
            row("WI-011", preds="WI-010"),
            row("WI-012", preds="WI-011"),
            row("WI-050", priority="5"),
        ]
    )
    order = ready_ids(wis)
    assert order.index("WI-050") < order.index("WI-010")


def test_lowest_rank_sorts_first():
    # A spine WI (rank 0) sorts ahead of an ordinary WI (rank 6) regardless of
    # Priority, because rank is the primary key.
    wis = sched.load_wis(
        [row("WI-001", safety="ordinary", priority="9"), row("WI-002", safety="spine")]
    )
    assert ready_ids(wis) == ["WI-002", "WI-001"]


def test_shared_srrefs_do_not_serialize():
    wis = sched.load_wis(
        [
            row("WI-001", srs="SR-010"),
            row("WI-002", srs="SR-010"),
        ]
    )
    assert ready_ids(wis) == ["WI-001", "WI-002"]  # a shared SR-Ref is not a mutex


def test_shared_exclusive_key_serializes():
    wis = sched.load_wis([row("WI-001", exclusive="db"), row("WI-002", exclusive="db")])
    assert ready_ids(wis) == ["WI-001"]  # lower id wins the contested key
    d = disposition(wis, "WI-002")
    assert d["disposition"] == "excluded"
    assert any("exclusive-conflict:db@WI-001" in c for c in d["reasons"])
    # The emitted key is `exclusive_keys` — the mutex-key SET from the
    # `Exclusive` column, which is a different idea from the `concurrency`
    # value beside it and must not be spelled the same on the wire.
    assert d["exclusive_keys"] == ["db"]
    assert "exclusive" not in d and d["concurrency"] == PAR


def test_disjoint_exclusive_keys_do_not_serialize():
    wis = sched.load_wis(
        [row("WI-001", exclusive="db"), row("WI-002", exclusive="cache")]
    )
    assert ready_ids(wis) == ["WI-001", "WI-002"]


def test_unclassified_wi_never_holds_an_exclusive_key():
    # WI-001 is unclassified (fails closed, never schedulable). It must not claim
    # the contested key: the key serializes CONCURRENT execution, and a
    # quarantined WI is not executing — letting it hold the key would starve the
    # classified WI-002 forever (2026-07-17b review H1).
    wis = sched.load_wis(
        [row("WI-001", safety="", exclusive="db"), row("WI-002", exclusive="db")]
    )
    assert ready_ids(wis) == ["WI-002"]
    d = disposition(wis, "WI-001")
    assert d["disposition"] == "excluded"
    assert any("unclassified" in c for c in d["reasons"])


def test_reserved_wi_keeps_its_exclusive_key_even_unclassified():
    # A reserved WI is a live train: it owns its keys outright, whatever its row
    # now classifies as — a mid-flight SafetyClass edit must not hand its mutex
    # to a rival.
    wis = sched.load_wis(
        [row("WI-001", safety="", exclusive="db"), row("WI-002", exclusive="db")]
    )
    d = disposition(wis, "WI-002", reserved={"WI-001"})
    assert d["disposition"] == "excluded"
    assert any("exclusive-conflict:db@WI-001" in c for c in d["reasons"])


# --- excluded dispositions carry reason codes --------------------------------
def test_blocked_deferred_reserved_excluded_with_reason_codes():
    wis = sched.load_wis(
        [
            row("WI-001", blockref="OI-9"),  # blocked = queued + blockref (Phase 5)
            row("WI-002", status="deferred"),
            row("WI-003"),
            row("WI-004"),
        ]
    )
    assert ready_ids(wis, reserved={"WI-004"}) == ["WI-003"]
    assert disposition(wis, "WI-001")["reasons"] == ["excluded:blocked:OI-9"]
    assert disposition(wis, "WI-002")["reasons"] == ["excluded:deferred"]
    d4 = disposition(wis, "WI-004", reserved={"WI-004"})
    assert d4["disposition"] == "reserved"
    assert d4["reasons"] == ["reserved:claimed-by-live-train"]


def test_legacy_blocked_status_is_excluded_fail_closed():
    # `blocked` stopped being a status at Phase 5 (it is queued + blockref);
    # a stray literal must never fall through to ready.
    wis = sched.load_wis([row("WI-001", status="blocked")])
    assert disposition(wis, "WI-001")["reasons"] == ["excluded:unknown-status:blocked"]


# --- SR-058 / §A1: classification on TWO independent axes ---------------------
# WI-383 collapsed the five-value ladder (`spine-serial | protected-serial |
# single-wi | ordinary | unclassified`) that answered two questions at once into
# a `concurrency` (what may share the station) and a `rank` (who goes first).
# The tests below pin each axis SEPARATELY and then pin the independence itself,
# because a re-conflation would pass any test that only ever reads one of them.

# §A1's ruled table, restated as data the tests read: kind -> (concurrency, rank).
# Rank 1 was RESERVED for `adjudication` when the ladder was written whole
# (§A1's gap); WI-388 fills it — exclusive, rank 1, the §A5.2 no-bar kind.
RULED_TABLE = {
    "spine": (EXCL, 0),
    "adjudication": (EXCL, 1),
    "attestation": (EXCL, 2),
    "gate": (EXCL, 2),
    "protected": (EXCL, 3),
    "high-risk": (EXCL, 4),
    "critique": (PAR, 5),
    "ordinary": (PAR, 6),
}


def test_classify_every_declared_value_is_deterministic():
    """Both axes, for every kind, twice — the table verbatim from §A1."""
    for declared, (concurrency, rank) in RULED_TABLE.items():
        # `critique` is a flag on an ordinary row, not a SafetyClass cell.
        wi = (
            {"safetyclass": "ordinary", "critique": True}
            if declared == "critique"
            else {"safetyclass": declared}
        )
        expected = (concurrency, rank, ["%s:%s" % (concurrency, declared)])
        assert sched.classify(wi) == expected, declared
        assert sched.classify(wi) == expected, declared  # idempotent/deterministic


def test_rank_1_is_the_adjudication_kind():
    """The `adjudication` gap, FILLED (WI-388). §A1 reserved rank 1 for the
    kind; filling it adds one mapping instead of renumbering a ruled table.
    The slot's occupant is pinned by name so a later edit cannot quietly hand
    1 to something else."""
    assert sched._KIND_RANK["adjudication"] == 1
    assert sched._KIND_CONCURRENCY["adjudication"] == EXCL
    assert "adjudication" in sched.SAFETY_CLASSES
    assert sorted(sched._KIND_RANK.values()) == [0, 1, 2, 2, 3, 4, 5, 6]


def test_the_two_axes_are_declared_separately_over_the_same_kinds():
    # Two tables, one key set: neither axis is derivable from the other's table,
    # and a kind cannot be given a rank while silently losing its concurrency.
    assert set(sched._KIND_CONCURRENCY) == set(sched._KIND_RANK) == set(RULED_TABLE)


def test_rank_does_not_determine_concurrency():
    # The killer case for the old ladder: rank 4 and rank 5 are ADJACENT and land
    # on opposite concurrency values. Nothing about being ranked early makes a WI
    # exclusive — a critique goes ahead of ordinary work AND runs beside it.
    hi_c, hi_r, _ = sched.classify({"safetyclass": "high-risk"})
    cr_c, cr_r, _ = sched.classify({"safetyclass": "ordinary", "critique": True})
    assert (hi_c, cr_c) == (EXCL, PAR)
    assert hi_r + 1 == cr_r


def test_concurrency_does_not_determine_rank():
    # And the reverse: the six exclusive kinds hold five distinct ranks, so
    # "exclusive" says nothing about order. (This is the pair `protected-serial`
    # and `single-wi` used to encode as two classes — both mean run alone.)
    #
    # Read off the SHIPPED tables, not off RULED_TABLE: an assertion over this
    # module's own literal would only prove the test file is self-consistent,
    # and would pass unchanged with `_KIND_RANK` mutated so concurrency fully
    # determines rank (REVIEW-A round 1).
    ranks = {}
    for kind, concurrency in sched._KIND_CONCURRENCY.items():
        ranks.setdefault(concurrency, set()).add(sched._KIND_RANK[kind])
    assert ranks == {EXCL: {0, 1, 2, 3, 4}, PAR: {5, 6}}


def test_reordering_the_frontier_never_moves_the_concurrency_axis():
    """A rank change must not alter concurrency. Priority reorders two ordinary
    WIs; both stay `parallel`, and the ordering swaps."""
    flat = sched.load_wis([row("WI-001"), row("WI-002")])
    bumped = sched.load_wis([row("WI-001"), row("WI-002", priority="5")])
    assert ready_ids(flat) == ["WI-001", "WI-002"]
    assert ready_ids(bumped) == ["WI-002", "WI-001"]
    for wis in (flat, bumped):
        assert {r["concurrency"] for r in sched.evaluate(wis)} == {PAR}


def test_the_frontier_orders_one_concurrency_group_by_rank():
    """The ordering axis pinned AT ITS CALL SITE — the only place it can break.

    `order_key` takes a rank rather than a classification, but Python does not
    enforce that: passing the concurrency value instead is a one-token edit, and
    REVIEW-A round 1 drove exactly that mutation past the whole suite with
    byte-identical counts. What convicts it is a frontier whose leading run is
    FOUR KINDS THAT SHARE ONE CONCURRENCY VALUE and hold four distinct ranks —
    order the concurrency string instead and all four tie, collapsing to id
    order and dropping the spine WI from first to fourth. Nothing here hands
    `order_key` a literal; the assertion runs through `evaluate`."""
    wis = sched.load_wis(
        [
            row("WI-001", safety="gate"),  # rank 2
            row("WI-002", safety="protected"),  # rank 3
            row("WI-003", safety="high-risk"),  # rank 4
            row("WI-004", safety="spine"),  # rank 0
            row("WI-009", safety="ordinary"),  # rank 6, and the only `parallel`
        ]
    )
    assert ready_ids(wis) == ["WI-004", "WI-001", "WI-002", "WI-003", "WI-009"]
    records = {r["id"]: r for r in sched.evaluate(wis)}
    # The four leaders are indistinguishable on the concurrency axis, so the
    # order asserted above cannot have come from it.
    leaders = ("WI-004", "WI-001", "WI-002", "WI-003")
    assert {records[w]["concurrency"] for w in leaders} == {EXCL}
    assert [records[w]["rank"] for w in leaders] == [0, 2, 3, 4]


def test_rank_outranks_every_tiebreaker_in_the_order_key():
    # Rank is the LEADING term: a better rank wins against a maxed Priority,
    # more downstream dependents and a longer hard path all at once. The rest
    # only ever break a tie within one rank.
    early = {"priority": 0, "id": "WI-002"}
    late = {"priority": 9, "id": "WI-001"}
    assert sched.order_key(early, 0, 0, 0) < sched.order_key(late, 6, 99, 99)
    assert sched.order_key(early, 3, 0, 0) == sched.order_key(early, 3, 0, 0)


def test_critique_is_parallel_and_ranks_ahead_of_ordinary():
    """§A1: a critique WI may share the station — nothing about a critique
    touches product code — and still sorts ahead of ordinary work. It was
    `single-wi` only to keep it out of a packed session; packing is gone."""
    concurrency, rank, reasons = sched.classify(
        {"safetyclass": "ordinary", "critique": True}
    )
    assert (concurrency, rank, reasons) == (PAR, 5, ["parallel:critique"])
    # A declared EXCLUSIVE kind is the more constraining statement: the flag
    # never relaxes it.
    assert sched.classify({"safetyclass": "spine", "critique": True}) == (
        EXCL,
        0,
        ["exclusive:spine"],
    )


def test_missing_and_unknown_safetyclass_fail_closed_only_for_that_wi():
    wis = sched.load_wis(
        [row("WI-001", safety=""), row("WI-002", safety="bogus"), row("WI-003")]
    )
    # Only the well-classified WI-003 is ready; the other two fail closed.
    assert ready_ids(wis) == ["WI-003"]
    # BOTH axes are refused, never one — a quarantined WI has no rank to sort by
    # and no concurrency to admit it.
    assert sched.classify({"safetyclass": ""}) == (
        sched.CONCURRENCY_UNCLASSIFIED,
        sched.RANK_UNCLASSIFIED,
        ["unclassified:missing"],
    )
    assert sched.classify({"safetyclass": "bogus"}) == (
        sched.CONCURRENCY_UNCLASSIFIED,
        sched.RANK_UNCLASSIFIED,
        ["unclassified:unknown-value:bogus"],
    )
    assert (
        disposition(wis, "WI-001")["reasons"][-1] == "excluded:unclassified-fail-closed"
    )


def test_unclassified_ranks_behind_every_real_kind():
    # It is excluded from the frontier, so the rank only has to keep --explain in
    # a stable total order — behind everything that could actually run.
    assert sched.RANK_UNCLASSIFIED > max(RULED_TABLE[k][1] for k in RULED_TABLE)


def test_ordinary_declaration_with_structural_spine_fails_closed():
    concurrency, rank, reasons = sched.classify(
        {"safetyclass": "ordinary"}, structural="spine"
    )
    assert (concurrency, rank) == (
        sched.CONCURRENCY_UNCLASSIFIED,
        sched.RANK_UNCLASSIFIED,
    )
    assert reasons == ["unclassified:declared-ordinary-vs-structural-spine"]
    # A matching declaration is NOT a mismatch.
    assert sched.classify({"safetyclass": "spine"}, structural="spine")[:2] == (EXCL, 0)


def test_is_schedulable_gates_on_the_concurrency_axis_only():
    # Eligibility is fail-closed-or-not, nothing finer: every positively
    # classified kind is schedulable whatever its concurrency or rank.
    for kind in RULED_TABLE:
        wi = (
            {"safetyclass": "ordinary", "critique": True}
            if kind == "critique"
            else {"safetyclass": kind}
        )
        assert sched.is_schedulable(sched.classify(wi)[0]), kind
    assert not sched.is_schedulable(sched.CONCURRENCY_UNCLASSIFIED)


# --- CLI surface (same decision, inspectable) --------------------------------
def _write_registry(root, rows):
    """The fixture registry in its one home, `docs/work/` spec files (Phase 5;
    written through the format's single writer, wi_convert)."""
    wc = load_script("wi_convert")
    work = root / "docs" / "work"
    work.mkdir(parents=True, exist_ok=True)
    for n, r in enumerate(rows, 1):
        full = {c: "" for c in wc.COLUMNS}
        full.update(r)
        full["Status"] = full.get("Status") or "queued"
        if full["Status"] == "done" and not full.get("Deliverable"):
            full["Deliverable"] = "shipped"
        wc.write_spec_file(work, full, order=n)


def test_cli_ready_json_matches_library(tmp_path):
    _write_registry(
        tmp_path,
        [
            row("WI-001"),
            row("WI-002", preds="WI-001"),
            row("WI-003", safety=""),
        ],
    )
    proc = run_py(
        [SCRIPTS / "schedule.py", "--root", str(tmp_path), "ready", "--format", "json"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert [r["id"] for r in data] == ["WI-001"]  # WI-002 waiting, WI-003 unclassified


def test_cli_explain_reports_every_wi_and_reasons(tmp_path):
    _write_registry(tmp_path, [row("WI-001"), row("WI-002", status="deferred")])
    proc = run_py(
        [
            SCRIPTS / "schedule.py",
            "--root",
            str(tmp_path),
            "ready",
            "--explain",
            "--format",
            "json",
        ],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stderr
    data = {r["id"]: r for r in json.loads(proc.stdout)}
    assert data["WI-001"]["disposition"] == "ready"
    assert data["WI-002"]["disposition"] == "deferred"
    assert data["WI-002"]["reasons"] == ["excluded:deferred"]


def test_cli_explain_text_formats_reason_lists(tmp_path):
    _write_registry(tmp_path, [row("WI-001"), row("WI-002", status="deferred")])
    proc = run_py(
        [SCRIPTS / "schedule.py", "--root", str(tmp_path), "ready", "--explain"],
        cwd=tmp_path,
    )
    assert proc.returncode == 0, proc.stderr
    assert "WI-001" in proc.stdout and "ready" in proc.stdout
    assert "WI-002" in proc.stdout and "excluded:deferred" in proc.stdout


def test_cli_simulate_serial_and_parallel(tmp_path):
    _write_registry(
        tmp_path, [row("WI-001"), row("WI-002"), row("WI-003", preds="WI-001")]
    )
    serial = run_py(
        [
            SCRIPTS / "schedule.py",
            "--root",
            str(tmp_path),
            "simulate",
            "--jobs",
            "1",
            "--format",
            "json",
        ],
        cwd=tmp_path,
    )
    assert serial.returncode == 0, serial.stderr
    rounds = json.loads(serial.stdout)["rounds"]
    # jobs=1 -> one WI per round, deterministic order, dependency respected.
    assert rounds == [["WI-001"], ["WI-002"], ["WI-003"]]
    par = run_py(
        [
            SCRIPTS / "schedule.py",
            "--root",
            str(tmp_path),
            "simulate",
            "--jobs",
            "2",
            "--format",
            "json",
        ],
        cwd=tmp_path,
    )
    assert json.loads(par.stdout)["rounds"] == [["WI-001", "WI-002"], ["WI-003"]]


# --- SR-066 (WI-209): PlanMode=dual derives the `high-risk` kind --------------
def test_planmode_dual_derives_the_high_risk_kind_from_the_signal():
    # Both axes come from the registry PlanMode signal itself — no SafetyClass
    # cell needed (single-source, the WI-201 ruling wired by WI-209).
    wis = sched.load_wis([row("WI-001", safety="", PlanMode="dual")])
    concurrency, rank, reasons = sched.classify(wis[0])
    assert (concurrency, rank) == RULED_TABLE["high-risk"]
    assert reasons == ["exclusive:dual-plan"]
    # And the frontier schedules it as ready (never fail-closed for the missing
    # SafetyClass cell a dual row deliberately does not carry).
    assert disposition(wis, "WI-001")["disposition"] == "ready"


def test_planmode_dual_contradicting_safetyclass_quarantines():
    # A second hand-set cell that contradicts the derivation fails closed —
    # the same cross-check posture as declared-ordinary-vs-structural.
    for declared in ("ordinary", "spine", "gate", "attestation", "protected"):
        wis = sched.load_wis([row("WI-001", safety=declared, PlanMode="dual")])
        concurrency, rank, reasons = sched.classify(wis[0])
        assert concurrency == sched.CONCURRENCY_UNCLASSIFIED, declared
        assert rank == sched.RANK_UNCLASSIFIED, declared
        assert reasons == ["unclassified:planmode-dual-vs-declared-" + declared]
        assert disposition(wis, "WI-001")["disposition"] == "excluded"
    # high-risk agrees with the derivation (the same kind): no quarantine, and
    # both signals are named.
    wis = sched.load_wis([row("WI-001", safety="high-risk", PlanMode="dual")])
    assert sched.classify(wis[0]) == (
        EXCL,
        4,
        ["exclusive:dual-plan", "exclusive:high-risk"],
    )


def test_planmode_absent_or_other_changes_nothing():
    # A legacy registry without the column and a non-dual token both classify
    # exactly as before (the never-breaking optional-column rule).
    assert sched.classify({"safetyclass": "ordinary"})[:2] == RULED_TABLE["ordinary"]
    wis = sched.load_wis([row("WI-001", PlanMode="single")])
    assert sched.classify(wis[0])[:2] == RULED_TABLE["ordinary"]
