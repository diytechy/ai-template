"""SR-141 · SR-142 · SR-143 (under SN-025) — the loop-order contract, as a set
of driven rules.

The plan's §4 states the tick priority as *ratified prose the tests pin, not an
emergent property of the tick loop*: dispositions -> amendment adjudication ->
surface-or-dispatch by level -> spine batch -> non-spine -> red-TC intake. This
module pins the three rungs that were not already built:

  1. **Judgement first** (`dispatch._judgement_first`): an `adjudication` row
     outranks everything ready, including a spine batch — and the ruled §A1
     rank table is NOT renumbered to achieve it.
  6. **The red-TC census** (`dispatch.red_tc_census` + `intake._red_tc_draft`):
     a TC left red under a CLOSED implementation is a contradiction, routed to
     an adjudicator with an estimated tier rather than minted at a default one.
  3. **Queue-conflict vetting** (`check_trajectory.queue_conflict_findings`):
     the cheap mechanical half — two open rows that overlap are made VISIBLE,
     never blocked.

The census/parse grammar gets its own pin because it is a string contract
BETWEEN TWO MODULES, which is exactly the kind of seam that rots silently.
"""

import pytest
from conftest import load_script, wi_registry_header, wi_row, write_wi_registry

dsp = load_script("dispatch")
intake = load_script("intake")
sched = load_script("schedule")
ct = load_script("check_trajectory")


# --- rung 1: judgement first --------------------------------------------------


def test_an_adjudication_row_outranks_a_spine_batch():
    # The one place the loop-order contract and §A1's rank table disagree.
    # Spine is rank 0 and adjudication rank 1, so the FRONTIER hands them over
    # spine-first; admission re-orders. Why: an adjudication row exists because
    # a lane CLAIMED an outcome nothing has judged, and a spine batch
    # re-attests requirements — running the batch first ratifies a spine on a
    # premise the pending judgement may overturn, and the attestation ledger is
    # append-only by design.
    frontier = [("WI-001", "spine"), ("WI-002", "adjudication")]
    assert dsp._admission(frontier, False, busy=False, free=2) == (
        "admit-exclusive",
        ["WI-002"],
    )


def test_the_ruled_rank_table_is_NOT_renumbered_to_achieve_it():
    # The rung is an ADMISSION preference, not a re-ruling. Renumbering §A1's
    # table would change ordering for every downstream repo — and `--explain`
    # still reports the ruled total order, which is what makes the two
    # readable side by side rather than one silently shadowing the other.
    assert sched._KIND_RANK["spine"] == 0
    assert sched._KIND_RANK["adjudication"] == 1


def test_judgement_first_is_a_STABLE_partition_not_a_sort():
    # Everything that is not an adjudication keeps its relative order exactly
    # — the frontier arrives rank-sorted and this rung must not reshuffle it.
    frontier = [
        ("WI-001", "spine"),
        ("WI-002", "attestation"),
        ("WI-003", "adjudication"),
        ("WI-004", "ordinary"),
        ("WI-005", "adjudication"),
        ("WI-006", "ordinary"),
    ]
    assert dsp._judgement_first(frontier) == [
        ("WI-003", "adjudication"),
        ("WI-005", "adjudication"),
        ("WI-001", "spine"),
        ("WI-002", "attestation"),
        ("WI-004", "ordinary"),
        ("WI-006", "ordinary"),
    ]


def test_judgement_first_does_not_smuggle_work_past_a_human_held_stop():
    # The preference reorders; it never CHANGES what may run. A human-held
    # attestation still drains and surfaces, with the adjudication row waiting
    # behind the stop rather than being admitted ahead of it.
    frontier = [("WI-001", "attestation"), ("WI-002", "adjudication")]
    verb, payload = dsp._admission(frontier, True, busy=False, free=2)
    assert verb == "surface"
    assert payload == ["WI-001"]


# --- rung 6: the red-TC census ------------------------------------------------

SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,"
    "Priority,Verification,Status,Phase,Area,SupersededBy\n"
)
LLR_HEADER = (
    "LLR-ID,SR-Refs,Title,Design,Rationale,Module,CodeSymbol,TestRefs,Status,"
    "Phase,Component\n"
)
TC_HEADER = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,"
    "Status,Phase\n"
)


def _spine(root, *, tc_status, wi_status="done", verifies="SR-001"):
    """A minimal repo: one SR, one TC verifying it, one WI citing the SR."""
    req = root / "docs" / "requirements"
    test = root / "docs" / "test"
    req.mkdir(parents=True)
    test.mkdir(parents=True)
    (req / "stakeholder-needs.md").write_text(
        "# Needs\n\nSN-001: A thing.\n", encoding="utf-8", newline="\n"
    )
    (req / "system-requirements.csv").write_text(
        SR_HEADER + "SR-001,Widget,SN-001,Shall widget.,Because.,Widgets.,,1,"
        "Test,Approved,,,\n",
        encoding="utf-8",
        newline="\n",
    )
    (req / "low-level-requirements.csv").write_text(
        LLR_HEADER + "LLR-001,SR-001,Widget impl,Do it.,Because.,w.py,widget,"
        "tests/test_w.py,Approved,,\n",
        encoding="utf-8",
        newline="\n",
    )
    (test / "test-cases.csv").write_text(
        TC_HEADER
        + "TC-001,{},Unit,Run it.,Smoke,,Satisfies AC,Yes,tests/test_w.py,{},\n".format(
            verifies, tc_status
        ),
        encoding="utf-8",
        newline="\n",
    )
    row = wi_row("WI-001", sr="SR-001", status=wi_status)
    if wi_status in ("partial", "cancelled"):
        # The registry writer fills a Deliverable only for `done`; `cancelled`
        # needs one too (R-A), and `partial` must NOT have one (SR-144).
        row[wi_registry_header().index("Deliverable")] = (
            "" if wi_status == "partial" else "never shipped"
        )
    write_wi_registry(root, [row])


def test_a_red_tc_under_a_closed_row_is_named(tmp_path):
    # The contradiction the registries state plainly and nothing was reading:
    # the work item is CLOSED and the evidence for it is not green.
    _spine(tmp_path, tc_status="Failed")
    census = dsp.red_tc_census(tmp_path)
    assert len(census) == 1
    assert dsp.parse_red_tc(census[0]) == ("TC-001", ["SR-001"])


@pytest.mark.parametrize("status", ["Approved", "Drafted", "Founded"])
def test_the_three_exempt_statuses_are_never_red(tmp_path, status):
    # Stated as EXEMPTIONS rather than as a list of red words: anything else is
    # red, so the rule fails toward naming a gap rather than missing one, and it
    # keeps working for a downstream repo mid-migration.
    # Approved is green; Drafted is pre-ratification, where "not yet green" is
    # correct; Founded (armed at D-9 step 8) is Approved plus a demonstration, so
    # it is green a fortiori. It REPLACED `Modified` here at step 7 — that word
    # belonged to the §A5.1 amendment adjudication and retired with the marker,
    # and a set still exempting it would be a live reader of a retired word.
    _spine(tmp_path, tc_status=status)
    assert dsp.red_tc_census(tmp_path) == []


def test_an_OPEN_row_never_makes_a_tc_red(tmp_path):
    # The whole premise is "a closed row CLAIMS the work". A queued row claims
    # nothing, so its TC being red is simply work not started — which the
    # orphan/status rungs already name, and a second row would double-count.
    _spine(tmp_path, tc_status="Failed", wi_status="queued")
    assert dsp.red_tc_census(tmp_path) == []


def test_a_partial_close_never_makes_a_tc_red(tmp_path):
    # `partial` and `cancelled` are precisely the outcomes that say the work is
    # NOT delivered, so a red TC under one of them is expected rather than a
    # contradiction — and that close already earned a disposition row of its
    # own. Naming it here would judge one event twice.
    _spine(tmp_path, tc_status="Failed", wi_status="partial")
    assert dsp.red_tc_census(tmp_path) == []


def test_a_tc_verifying_a_MIX_of_claimed_and_unclaimed_is_not_red(tmp_path):
    # "All of whose targets are implemented" is the rule, and the reason is the
    # premise: if any target is still open the TC is legitimately not green yet.
    _spine(tmp_path, tc_status="Failed", verifies="SR-001;SR-999")
    assert dsp.red_tc_census(tmp_path) == []


def test_the_red_tc_line_grammar_round_trips():
    # A STRING CONTRACT BETWEEN TWO MODULES — the seam carries finding strings,
    # so the formatter and the parser are pinned against each other. The
    # alternative (intake re-splitting the prose) is prose carrying control
    # flow, which is exactly the `NEEDS-HUMAN` defect SR-145 removed.
    line = dsp._red_tc_line("TC-042", "failed", ["SR-007", "LLR-009"])
    assert dsp.parse_red_tc(line) == ("TC-042", ["SR-007", "LLR-009"])
    assert line.startswith(dsp.RED_TC_PREFIX)


def test_parse_red_tc_returns_None_for_every_other_census_line():
    # The router must not match by accident: an ordinary gap line that merely
    # mentions a TC id is NOT a red-TC event.
    assert dsp.parse_red_tc("SN-002 is a draft need (unratified)") is None
    assert dsp.parse_red_tc("TC-003 has no Evidence") is None
    assert dsp.parse_red_tc("") is None
    assert dsp.parse_red_tc(None) is None


def test_the_red_tc_census_rides_the_gap_census_seam(tmp_path):
    # The dispatcher hands ONE list of strings to intake; the new class travels
    # on it rather than growing the seam a second shape.
    _spine(tmp_path, tc_status="Failed")
    assert any(dsp.parse_red_tc(line) for line in dsp.gap_census(tmp_path))


# --- rung 6, intake side: the estimator ---------------------------------------


def test_a_red_tc_mints_an_ADJUDICATION_row_not_an_ordinary_gap_row(tmp_path):
    # The difference is WHO DECIDES. An ordinary gap row says "the registry is
    # missing a link, go add it". A red TC is one of three quite different
    # situations (stale TC / optimistic close / moved requirement) and picking
    # between them is a judgement — which is what the kind is for.
    _spine(tmp_path, tc_status="Failed")
    drafts = intake._census_drafts(tmp_path, dsp.gap_census(tmp_path))
    red = [d for d in drafts if d["kind"] == "adjudication"]
    assert len(red) == 1
    assert red[0]["specref"] == "docs/test/test-cases.csv"
    assert "TC-001" in red[0]["title"]


def test_the_red_tc_tier_is_ESTIMATED_from_breadth_not_defaulted():
    # §4 rung 1's "estimator": one target is a local question; several mean the
    # closed row's claim spans requirements and the judgement has to hold all
    # of them at once. Counted, never judged — the same shape as the amendment
    # arm, with the threshold at 1 because a red TC is already a contradiction.
    assert intake.tier_signal("red-tc", rows_touched=1) == "medium"
    assert intake.tier_signal("red-tc", rows_touched=2) == "strong"
    one = intake._red_tc_draft(".", "red TC TC-1 [SR-1] is failed", ["SR-1"])
    many = intake._red_tc_draft(
        ".", "red TC TC-1 [SR-1;SR-2] is failed", ["SR-1", "SR-2"]
    )
    assert one["buildtier"] == "medium"
    assert many["buildtier"] == "strong"


def test_the_red_tc_draft_declares_NO_planmode():
    """The defect this row shipped with for exactly one review round.

    `planmode = "dual"` beside `safety_class = "adjudication"` is a shape
    `schedule.classify` REFUSES — it reads `unclassified`, so the row drops off
    the frontier, and exact-title dedup then guarantees it is never minted
    again. The contradiction rung 6 exists to surface would have been minted
    and then permanently parked, silently, while the census reported the gap as
    handled. Breadth is carried by the TIER, which is a dial the scheduler
    accepts on any kind."""
    draft = intake._red_tc_draft(
        ".", "red TC TC-1 [SR-1;SR-2] is failed", ["SR-1", "SR-2"]
    )
    assert not draft.get("planmode")


def test_every_MINTED_row_is_one_the_scheduler_can_actually_classify():
    """The structural half, and the reason this is a test rather than a fixed
    cell: `_draft_refusal` validated only the follow-ups a HUMAN wrote into a
    `## Dispositions` block. Every DERIVED draft went straight to `_draft_row`
    and was validated by nothing — so the mint could emit a row that is not
    work at all, with nobody watching at either end."""
    import pytest as _pytest

    for draft in (
        {"title": "t", "kind": "adjudication", "planmode": "dual"},
        {"title": "t", "kind": "not-a-kind"},
    ):
        assert intake._mint_shape_refusal(draft, "the census") is not None
    assert (
        intake._mint_shape_refusal({"title": "t", "kind": "adjudication"}, "x") is None
    )
    assert (
        intake._mint_shape_refusal(
            {"title": "t", "kind": "high-risk", "planmode": "dual"}, "x"
        )
        is None
    )
    del _pytest


def test_a_minted_red_tc_row_reaches_the_FRONTIER(tmp_path):
    """End to end, through the real scheduler: the census names it, the draft
    is built, and `schedule.classify` gives it a real kind and rank rather than
    `unclassified`. Nothing else in the suite drove a minted row through the
    scheduler, which is how the shape above survived a green suite."""
    _spine(tmp_path, tc_status="Failed", verifies="SR-001")
    drafts = intake._census_drafts(tmp_path, dsp.gap_census(tmp_path))
    red = [d for d in drafts if d["kind"] == "adjudication"]
    assert len(red) == 1
    row = intake._draft_row("WI-900", red[0])
    wis = sched.load_wis([row])
    assert wis, "the minted row must load"
    concurrency, rank, _reasons = sched.classify(wis[0])
    assert concurrency != "unclassified", (concurrency, rank)
    assert rank == sched._KIND_RANK["adjudication"]


def test_the_red_tc_brief_names_all_three_readings_without_choosing():
    # A brief that pre-selects an outcome is not a brief. The judge is told the
    # contradiction and where to read it, and the three live readings are
    # listed as alternatives — including the one where nothing is wrong with
    # the code at all and the TC's Status is merely stale.
    draft = intake._red_tc_draft(".", "red TC TC-1 [SR-1] is failed", ["SR-1"])
    context = draft["context"]
    assert "STALE" in context
    assert "OPTIMISTIC" in context
    assert "REQUIREMENT moved" in context
    assert "supersedes" in context  # the successor keeps the thread


# --- rung 3: queue-conflict vetting -------------------------------------------


def _open(wid, title="Some work", srs=(), specref="", status="queued"):
    return {
        "id": wid,
        "title": title,
        "srs": list(srs),
        "specref": specref,
        "status": status,
    }


def test_two_open_rows_with_near_identical_titles_are_named():
    rows = [
        _open("WI-001", "Add the privacy gate to the push boundary"),
        _open("WI-002", "Add the privacy gate at the push boundary"),
    ]
    found = ct.queue_conflict_findings(rows)
    assert any("near-identical titles" in f for f in found)
    assert all("WI-001 and WI-002" in f for f in found)


def test_two_open_rows_answering_one_SR_are_named():
    rows = [
        _open("WI-001", "Alpha", srs=["SR-010", "SR-011"]),
        _open("WI-002", "Beta", srs=["SR-011"]),
    ]
    assert ct.queue_conflict_findings(rows) == [
        "WI-001 and WI-002 are both open and both answer SR-011"
    ]


def test_two_open_rows_sharing_one_spec_of_record_are_named():
    # The sharpest of the three: a spec IS a row's definition, so two open rows
    # sharing one is either a duplicate or a split nobody wrote down. The
    # anchor is stripped — `spec.md#a` and `spec.md#b` are one document.
    rows = [
        _open("WI-001", "Alpha", specref="docs/specs/thing.md#part-a"),
        _open("WI-002", "Beta", specref="docs/specs/thing.md#part-b"),
    ]
    assert ct.queue_conflict_findings(rows) == [
        "WI-001 and WI-002 are both open and share one spec of record "
        "(docs/specs/thing.md)"
    ]


def test_a_CLOSED_row_never_conflicts():
    # The rung is about the QUEUE. A done row's overlap with a queued one is
    # the normal shape of follow-up work, not a duplicate mint.
    rows = [
        _open("WI-001", "Alpha", srs=["SR-010"], status="done"),
        _open("WI-002", "Alpha", srs=["SR-010"]),
    ]
    assert ct.queue_conflict_findings(rows) == []


def test_unrelated_open_rows_are_silent():
    # The bar is deliberately high (Jaccard 0.8): this rung catches the same
    # job minted twice, not two rows in the same area. A warn that fires on
    # ordinary work gets ignored, which is worse than not having it.
    rows = [
        _open("WI-001", "Add the privacy gate", srs=["SR-010"], specref="a.md"),
        _open("WI-002", "Retire the legacy loader", srs=["SR-020"], specref="b.md"),
    ]
    assert ct.queue_conflict_findings(rows) == []


def test_a_shared_stopword_is_not_a_signal():
    # Titles are compared on SUBJECT MATTER: stopwords and bare numbers carry
    # no meaning, so two short titles must not collide on "the" and "a".
    rows = [
        _open("WI-001", "The loader"),
        _open("WI-002", "The dashboard"),
    ]
    assert ct.queue_conflict_findings(rows) == []


def test_each_conflicting_pair_is_reported_once_per_signal_not_per_direction():
    rows = [
        _open("WI-002", "Alpha work", srs=["SR-010"], specref="x.md"),
        _open("WI-001", "Alpha work", srs=["SR-010"], specref="x.md"),
    ]
    found = ct.queue_conflict_findings(rows)
    assert len(found) == 3  # title, SR, spec — one each
    assert all(f.startswith("WI-001 and WI-002") for f in found), found
    assert found == sorted(found), "deterministic order"


def test_queue_conflicts_NEVER_join_the_exit_code(tmp_path, monkeypatch):
    # Overlap between two open rows is frequently correct — two rows may
    # legitimately answer one SR from different sides — and a checker that
    # cannot tell that apart from a duplicate must not block on the difference.
    # The judgement half lives in the `adjudicate-conflict` prompt, not here.
    rows = [
        _open("WI-001", "Alpha", srs=["SR-1"]),
        _open("WI-002", "Alpha", srs=["SR-1"]),
    ]
    assert ct.queue_conflict_findings(rows), "the fixture must actually conflict"
    # The wiring: the findings are printed on the WARN-ONLY line, alongside
    # backlog-staleness and the pack-citation warn, and never appended to
    # `errors`. Pinned by source inspection because the alternative is standing
    # up a whole repo to observe a print.
    source = (ct.__file__ and open(ct.__file__, encoding="utf-8").read()) or ""
    warn_block = source.split("+ queue_conflict_findings(wis)")[1][:200]
    assert "WARN" in warn_block
    assert "errors.append" not in warn_block
