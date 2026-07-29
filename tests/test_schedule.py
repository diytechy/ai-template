"""Scheduler contract fixtures — SR-057 (frontier + deterministic order) and
SR-058 (deterministic safety classification). Verifies TC-058 / TC-059.

Unit-level and fast (in the smoke tier by default): the scheduler is a pure
library over in-memory registry rows, so these never bootstrap a scaffold. Two
CLI tests exercise `schedule.py ready --format json` end-to-end over a temp
registry to pin the shared decision across the CLI surface."""

import json

from conftest import SCRIPTS, load_script, run_py

sched = load_script("schedule")


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


# --- WI-267: `retired` is a terminal WON'T-BUILD status ------------------------
# Terminal like `done` (never ready, never scheduled) but — unlike `done` — a
# retired predecessor does NOT satisfy a successor's hard dependency (design-
# decision 3), so a live WI hard-blocked on a retired one surfaces rather than
# proceeding on a will-never-happen dependency.


def test_retired_wi_is_terminal_never_ready():
    wis = sched.load_wis([row("WI-001", status="retired")])
    assert ready_ids(wis) == []
    d = disposition(wis, "WI-001")
    assert d["disposition"] == "retired"
    assert d["reasons"] == ["retired:terminal-wont-build"]


def test_retired_predecessor_does_not_satisfy_a_hard_dependency():
    # Decision 3 (the DEAD-edge direction): a retired predecessor never
    # integrates, so the live successor can never become ready — it stays
    # `waiting`, and the retired dead edge is surfaced as its own reason code.
    wis = sched.load_wis(
        [row("WI-001", status="retired"), row("WI-002", preds="WI-001")]
    )
    assert ready_ids(wis) == []  # NOT satisfied the way a `done` pred would be
    d = disposition(wis, "WI-002")
    assert d["disposition"] == "waiting"
    assert "waiting:hard-pred-retired:WI-001" in d["reasons"]


def test_done_predecessor_still_satisfies_a_hard_dependency():
    # Decision 3 (the LIVE-edge direction, the control): a `done` pred DOES
    # satisfy — retirement is the only terminal state that leaves the edge dead.
    wis = sched.load_wis([row("WI-001", status="done"), row("WI-002", preds="WI-001")])
    assert ready_ids(wis) == ["WI-002"]


def test_retired_wi_is_never_scheduled_in_simulate():
    wis = sched.load_wis(
        [row("WI-001", status="retired"), row("WI-002"), row("WI-003")]
    )
    scheduled = [wid for rnd in sched.simulate(wis, 4) for wid in rnd]
    assert "WI-001" not in scheduled
    assert set(scheduled) == {"WI-002", "WI-003"}


def test_priority_outranks_downstream_within_a_gate_class():
    # WI-050: higher Priority but zero downstream. WI-010: default Priority but two
    # downstream dependents. Priority must win within one gate class.
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


def test_lowest_gate_class_sorts_first():
    # A spine WI (serial, gate-rank 0) sorts ahead of an ordinary WI regardless of
    # Priority, because the gate class is the primary key.
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


# --- SR-058: deterministic safety classification -----------------------------
def test_classify_every_declared_value_is_deterministic():
    cases = {
        "ordinary": (sched.SCHED_ORDINARY, ["ordinary:optimistic-packing-eligible"]),
        "spine": (sched.SCHED_SPINE_SERIAL, ["serial-whole-project:spine"]),
        "gate": (sched.SCHED_SPINE_SERIAL, ["serial-whole-project:gate"]),
        "attestation": (sched.SCHED_SPINE_SERIAL, ["serial-whole-project:attestation"]),
        "protected": (sched.SCHED_PROTECTED, ["serial-whole-project:protected"]),
        "high-risk": (sched.SCHED_SINGLE_WI, ["single-wi:high-risk"]),
    }
    for declared, expected in cases.items():
        wi = {"safetyclass": declared}
        assert sched.classify(wi) == expected
        assert sched.classify(wi) == expected  # idempotent / deterministic


def test_missing_and_unknown_safetyclass_fail_closed_only_for_that_wi():
    wis = sched.load_wis(
        [row("WI-001", safety=""), row("WI-002", safety="bogus"), row("WI-003")]
    )
    # Only the well-classified WI-003 is ready; the other two fail closed.
    assert ready_ids(wis) == ["WI-003"]
    assert sched.classify({"safetyclass": ""}) == (
        sched.SCHED_UNCLASSIFIED,
        ["unclassified:missing"],
    )
    assert sched.classify({"safetyclass": "bogus"}) == (
        sched.SCHED_UNCLASSIFIED,
        ["unclassified:unknown-value:bogus"],
    )
    assert (
        disposition(wis, "WI-001")["reasons"][-1] == "excluded:unclassified-fail-closed"
    )


def test_ordinary_declaration_with_structural_spine_fails_closed():
    wi = {"safetyclass": "ordinary"}
    cls, reasons = sched.classify(wi, structural="spine")
    assert cls == sched.SCHED_UNCLASSIFIED
    assert reasons == ["unclassified:declared-ordinary-vs-structural-spine"]
    # A matching declaration is NOT a mismatch.
    assert sched.classify({"safetyclass": "spine"}, structural="spine")[0] == (
        sched.SCHED_SPINE_SERIAL
    )


def test_critique_and_checkpoint_force_single_wi_traincar():
    assert sched.classify({"safetyclass": "ordinary", "critique": True}) == (
        sched.SCHED_SINGLE_WI,
        ["single-wi:critique"],
    )
    assert sched.classify({"safetyclass": "ordinary", "checkpoint": True}) == (
        sched.SCHED_SINGLE_WI,
        ["single-wi:integration-checkpoint"],
    )


def test_spine_serial_sched_class_is_not_multi_wi_packable():
    # A serialized class is scheduled (it is a valid single-WI train) but is never
    # ordinary/optimistic — the packer (Slice E) keys off the class, checked here.
    assert sched.is_schedulable_class(sched.SCHED_SPINE_SERIAL)
    assert not sched.is_schedulable_class(sched.SCHED_UNCLASSIFIED)


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


# --- SR-066 (WI-209): PlanMode=dual derives the single-WI-traincar class ------
def test_planmode_dual_derives_single_wi_from_the_signal():
    # The class comes from the registry PlanMode signal itself — no SafetyClass
    # cell needed (single-source, the WI-201 ruling wired by WI-209).
    wis = sched.load_wis([row("WI-001", safety="", PlanMode="dual")])
    cls, reasons = sched.classify(wis[0])
    assert cls == sched.SCHED_SINGLE_WI
    assert "single-wi:dual-plan" in reasons
    # And the frontier schedules it as ready single-wi (never fail-closed for
    # the missing SafetyClass cell a dual row deliberately does not carry).
    assert disposition(wis, "WI-001")["disposition"] == "ready"


def test_planmode_dual_contradicting_safetyclass_quarantines():
    # A second hand-set cell that contradicts the derivation fails closed —
    # the same cross-check posture as declared-ordinary-vs-structural.
    for declared in ("ordinary", "spine", "gate", "attestation", "protected"):
        wis = sched.load_wis([row("WI-001", safety=declared, PlanMode="dual")])
        cls, reasons = sched.classify(wis[0])
        assert cls == sched.SCHED_UNCLASSIFIED, declared
        assert reasons == ["unclassified:planmode-dual-vs-declared-" + declared]
        assert disposition(wis, "WI-001")["disposition"] == "excluded"
    # high-risk agrees with the derivation (same scheduling class): no quarantine.
    wis = sched.load_wis([row("WI-001", safety="high-risk", PlanMode="dual")])
    cls, reasons = sched.classify(wis[0])
    assert cls == sched.SCHED_SINGLE_WI
    assert reasons == ["single-wi:dual-plan", "single-wi:high-risk"]


def test_planmode_absent_or_other_changes_nothing():
    # A legacy registry without the column and a non-dual token both classify
    # exactly as before (the never-breaking optional-column rule).
    assert sched.classify({"safetyclass": "ordinary"})[0] == sched.SCHED_ORDINARY
    wis = sched.load_wis([row("WI-001", PlanMode="single")])
    assert sched.classify(wis[0])[0] == sched.SCHED_ORDINARY
