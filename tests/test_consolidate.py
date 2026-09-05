"""consolidate.py — the CONSOLIDATION census (2026-09-02 restructure plan §1.3).

The census answers "which queued rows are one work item wearing several ids",
and the whole risk of a census (as opposed to a merge hook) is that it fires on
a STATE and so fires again on the next tick. So the tests here are in two
halves: the SELECTION (does the pre-filter find the cluster, and only the
cluster) and the GUARDS (does it refuse to ask a question it has already asked,
and refuse to overturn its own earlier answer).

The decision half needs no repository — that is why it lives in its own module —
so most of these run on hand-built rows and a bare `tmp_path`. The mint arm's
end-to-end drive is in `tests/test_consolidate_end_to_end.py`.
"""

import pytest
from conftest import load_script

consolidate = load_script("consolidate")
wi_convert = load_script("wi_convert")


def _row(wid, **kw):
    row = {column: "" for column in wi_convert.COLUMNS}
    # Distinct titles by default, in ONE token. `_title_tokens` drops
    # pure-number tokens (a WI id is not subject matter), so "row 001" and
    # "row 005" both reduce to {"row"} and every fixture row would pair on the
    # title signal, hiding whichever signal the test is actually about.
    row.update({"WI-ID": wid, "Title": "topic" + wid[3:], "Status": "queued"})
    row.update(kw)
    return row


def _repo(tmp_path, rows=(), llrs=""):
    """A tree with a work folder written by the real converter and the three
    spine registries present, so the digests are computed over real files."""
    work = tmp_path / "docs" / "work"
    for row in rows:
        wi_convert.write_spec_file(work, row)
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "system-requirements.toml").write_text("", encoding="utf-8", newline="\n")
    (req / "low-level-requirements.toml").write_text(
        llrs, encoding="utf-8", newline="\n"
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.toml").write_text(
        "", encoding="utf-8", newline="\n"
    )
    return tmp_path


# --- the digest pair -----------------------------------------------------------


def test_the_queue_digest_covers_the_four_fields_that_change_the_question():
    """A row's title, needs and safety_class change what a consolidation would
    decide; its Deliverable and BuildTier do not. Hashing the whole row would
    re-arm the census on an edit that changes no answer, and hashing too little
    would let a genuinely new queue read as already judged."""
    base = [_row("WI-001", Title="Alpha"), _row("WI-002", Title="Beta")]
    first = consolidate.queue_digest(base)

    # The four load-bearing fields each move it.
    for field, value in (
        ("Title", "Alpha prime"),
        ("Predecessors", "WI-009"),
        ("SafetyClass", "spine"),
        ("WI-ID", "WI-777"),
    ):
        moved = [dict(base[0], **{field: value}), base[1]]
        assert consolidate.queue_digest(moved) != first, field

    # ...and the ones that do not decide anything leave it alone.
    for field, value in (("BuildTier", "quick"), ("Deliverable", "shipped")):
        same = [dict(base[0], **{field: value}), base[1]]
        assert consolidate.queue_digest(same) == first, field


def test_the_queue_digest_is_a_property_of_the_set_not_of_the_order():
    a, b = _row("WI-001"), _row("WI-002")
    assert consolidate.queue_digest([a, b]) == consolidate.queue_digest([b, a])


def test_only_queued_rows_reach_the_queue_digest():
    """The census's subject is the ready queue. A row going terminal changes
    the queue and so must move the digest; a DRAFT row was never in it."""
    queued = [_row("WI-001")]
    assert consolidate.queue_digest(
        queued + [_row("WI-002", Status="draft")]
    ) == consolidate.queue_digest(queued)
    assert consolidate.queue_digest(
        queued + [_row("WI-002")]
    ) != consolidate.queue_digest(queued)


def test_the_spine_digest_moves_when_a_registry_moves(tmp_path):
    repo = _repo(tmp_path)
    first = consolidate.spine_digest(repo)
    (repo / "docs" / "requirements" / "system-requirements.toml").write_text(
        '[requirement.SR-001]\nrequirement = "x"\n', encoding="utf-8", newline="\n"
    )
    assert consolidate.spine_digest(repo) != first


def test_an_absent_registry_hashes_as_empty_rather_than_being_skipped(tmp_path):
    """A repo that GAINS its first LLR registry has moved the spine, so a
    verdict recorded against the old pair must read as stale. Skipping the
    absent file would have made those two states hash identically."""
    repo = _repo(tmp_path)
    (repo / "docs" / "requirements" / "low-level-requirements.toml").unlink()
    absent = consolidate.spine_digest(repo)
    (repo / "docs" / "requirements" / "low-level-requirements.toml").write_text(
        "", encoding="utf-8", newline="\n"
    )
    assert consolidate.spine_digest(repo) == absent  # empty file == absent text
    (repo / "docs" / "requirements" / "low-level-requirements.toml").write_text(
        '[detail.LLR-001]\ndetail = "x"\n', encoding="utf-8", newline="\n"
    )
    assert consolidate.spine_digest(repo) != absent


@pytest.mark.parametrize(
    "cell", ["", "   ", "no-separator", "|only-spine", "only-queue|", "|"]
)
def test_a_malformed_digests_cell_reads_as_no_recorded_digest(cell):
    """It fails OPEN — into "this state has not been judged". The alternative
    direction is worse: a typo'd cell that silences the census forever."""
    assert consolidate.parse_digests(cell) == ("", "")


def test_a_well_formed_digests_cell_splits_into_its_pair():
    assert consolidate.parse_digests(" aaa|bbb ") == ("aaa", "bbb")


# --- the two signals the mechanical pre-filter does not carry ------------------


def test_a_shared_open_item_edge_is_a_commissioning_signal(tmp_path):
    """Two rows cut from ONE ruling routinely carry different specrefs — one
    points at the plan, one at the open-items registry — while the thing that
    makes them one question is the OI id they both wait on. The shared-SpecRef
    signal cannot see that; this one can."""
    rows = [
        _row("WI-001", SpecRef="docs/plans/a.md", Predecessors="OI-077"),
        _row(
            "WI-002",
            SpecRef="docs/requirements/open-items.toml",
            Predecessors="~OI-077",
        ),
    ]
    repo = _repo(tmp_path, rows)
    findings = consolidate.pair_findings(repo, rows)
    assert any("commissioned by the same OI-077" in f[2] for f in findings), findings


def test_the_module_signal_reads_both_the_llr_join_and_the_row_prose(tmp_path):
    """Both halves, because each is blind where the other sees: the LLR join is
    traceable but says nothing about a row citing no SR (most process rows), and
    the prose scan sees those. Compared by BASENAME — a row writes `intake.py`
    where an LLR's Module cell writes the full path."""
    llrs = (
        "[design.LLR-001]\n"
        'sr_refs = ["SR-001"]\n'
        'module = "project-trajectory/scripts/intake.py"\n'
        'detail = "d"\n'
    )
    rows = [
        _row("WI-001", **{"SR-Refs": "SR-001"}),
        _row("WI-002", Title="rework the mint in intake.py"),
    ]
    repo = _repo(tmp_path, rows, llrs=llrs)
    findings = consolidate.pair_findings(repo, rows)
    assert any("both touch intake.py" in f[2] for f in findings), findings


def test_the_module_signal_does_not_fire_on_a_bare_module_name(tmp_path):
    """Anchored on the `.py` suffix: a sentence mentioning `intake` is not a
    claim about a file, and a pre-filter that fires on everything selects
    nothing."""
    rows = [
        _row("WI-001", Title="rework the intake mint"),
        _row("WI-002", Title="rework the intake sweep"),
    ]
    repo = _repo(tmp_path, rows)
    assert not [f for f in consolidate.pair_findings(repo, rows) if "touch" in f[2]]


def test_the_module_signal_reads_the_spec_body_not_only_the_cells(tmp_path):
    """The plan says the signal reads each row's Context and Done-when, and
    those live in the spec BODY — which `read_spec_rows` does not carry."""
    rows = [_row("WI-001"), _row("WI-002")]
    repo = _repo(tmp_path, rows)
    work = repo / "docs" / "work" / "queued"
    for path in sorted(work.iterdir()):
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n## Context\n\nTouches project-trajectory/scripts/handback.py.\n",
            encoding="utf-8",
            newline="\n",
        )
    assert any(
        "both touch handback.py" in f[2] for f in consolidate.pair_findings(repo, rows)
    )


# --- the clusters --------------------------------------------------------------


def test_two_disjoint_overlapping_pairs_make_one_candidate_set(tmp_path):
    """Plan §4: five rows with two overlapping pairs mint EXACTLY ONE row. Two
    disjoint pairs are still one question — "which of these are the same work
    item?" — and guard 1 means a second judgement could not run beside the first
    anyway, so the census hands one judge the whole picture."""
    rows = [
        _row("WI-001", SpecRef="docs/plans/a.md"),
        _row("WI-002", SpecRef="docs/plans/a.md"),
        _row("WI-003", SpecRef="docs/plans/b.md"),
        _row("WI-004", SpecRef="docs/plans/b.md"),
        _row("WI-005", SpecRef="docs/plans/lonely.md"),
    ]
    repo = _repo(tmp_path, rows)
    ids, findings = consolidate.clusters(repo, rows)
    assert ids == ["WI-001", "WI-002", "WI-003", "WI-004"]
    assert findings and "WI-005" not in "".join(f[2] for f in findings)


def test_a_queue_with_no_overlap_selects_nothing(tmp_path):
    rows = [
        _row("WI-001", Title="Alpha", SpecRef="docs/plans/a.md"),
        _row("WI-002", Title="Beta", SpecRef="docs/plans/b.md"),
    ]
    repo = _repo(tmp_path, rows)
    assert consolidate.clusters(repo, rows) == ([], [])


# --- the guards ----------------------------------------------------------------


def test_no_row_is_minted_beside_another_judgement(tmp_path):
    rows = [
        _row("WI-001", SpecRef="docs/plans/a.md"),
        _row("WI-002", SpecRef="docs/plans/a.md"),
        _row("WI-003", SafetyClass="adjudication"),
    ]
    repo = _repo(tmp_path, rows)
    draft, why = consolidate.census_draft(repo, rows)
    assert draft is None
    assert "WI-003" in why and "never stacks" in why
    # ...and the same for one a lane is HOLDING. (`active/` has no directory in
    # `wi_convert.STATUS_DIRS` — a claimed spec lives under `active/<branch>/`
    # — so the row is handed to the guard directly rather than written.)
    held = [
        rows[0],
        rows[1],
        _row("WI-004", Status="active", SafetyClass="adjudication"),
    ]
    draft, why = consolidate.census_draft(repo, held)
    assert draft is None and "WI-004" in why


def test_a_queue_state_that_has_been_judged_is_never_judged_again(tmp_path):
    """And the ARCHIVED arm is the load-bearing half: an active-only guard reads
    "nobody has judged this" the moment the consolidation closes, and mints the
    identical row on the very next idle tick."""
    queue = [
        _row("WI-001", SpecRef="docs/plans/a.md"),
        _row("WI-002", SpecRef="docs/plans/a.md"),
    ]
    repo = _repo(tmp_path, queue)
    draft, why = consolidate.census_draft(repo, queue)
    assert draft is not None, why
    judged = _row(
        "WI-009",
        Status="done",
        SafetyClass="adjudication",
        Brief="consolidate",
        Digests=draft["digests"],
    )
    blocked, why = consolidate.census_draft(repo, queue + [judged])
    assert blocked is None
    assert "WI-009" in why and "never judged again" in why


def test_a_changed_queue_is_a_new_question(tmp_path):
    queue = [
        _row("WI-001", SpecRef="docs/plans/a.md"),
        _row("WI-002", SpecRef="docs/plans/a.md"),
    ]
    repo = _repo(tmp_path, queue)
    draft, _ = consolidate.census_draft(repo, queue)
    judged = _row(
        "WI-009",
        Status="done",
        SafetyClass="adjudication",
        Brief="consolidate",
        Digests=draft["digests"],
    )
    grown = queue + [judged, _row("WI-010", SpecRef="docs/plans/a.md")]
    again, why = consolidate.census_draft(repo, grown)
    assert again is not None, why
    assert again["digests"] != draft["digests"]


def test_a_consolidations_own_successor_does_not_seed_the_next_census(tmp_path):
    """Plan §4's third measurement: after the close absorbed two rows, the
    census mints nothing — "the digest changed but the only overlap is the
    consolidation's own successor". A successor is recognisable from the
    registry alone (it supersedes a `restructured` row), so the census can
    decline to re-litigate the judgement it just enacted."""
    rows = [
        _row("WI-001", Status="restructured", SpecRef="docs/plans/a.md"),
        _row("WI-002", Status="restructured", SpecRef="docs/plans/a.md"),
        _row("WI-010", SpecRef="docs/plans/a.md", Supersedes="WI-001;WI-002"),
        _row("WI-003", SpecRef="docs/plans/a.md"),
    ]
    repo = _repo(tmp_path, rows)
    assert consolidate.consolidation_successors(rows) == {"WI-010"}
    ids, _findings = consolidate.clusters(repo, rows)
    assert ids == []
    draft, why = consolidate.census_draft(repo, rows)
    assert draft is None and "nothing to consolidate" in why


def test_a_successor_is_read_from_lineage_and_not_from_how_many_it_absorbed():
    """`len(Supersedes) > 1` would have been the guess: a disposition names one
    predecessor, and a consolidation that absorbed exactly one row would be
    invisible to it. The signal is that the absorbed row is `restructured`."""
    rows = [
        _row("WI-001", Status="restructured"),
        _row("WI-010", Supersedes="WI-001"),
        # A disposition successor: its predecessor stopped early, not absorbed.
        _row("WI-002", Status="partial"),
        _row("WI-011", Supersedes="WI-002"),
    ]
    assert consolidate.consolidation_successors(rows) == {"WI-010"}


def test_re_absorbing_a_row_a_consolidation_minted_is_refused_by_name():
    """Overturning a consolidation is a RETURN-TO-DRAFT of THAT judgement (plan
    §1.3) — the owner's to rule, never a second machine mint. Distinct from
    `intake._supersedes_refusal`'s absorbed arm, which refuses continuing a row
    somebody already absorbed (a lineage chain)."""
    rows = [_row("WI-001", Status="restructured"), _row("WI-010", Supersedes="WI-001")]
    assert consolidate.reabsorption_refusal(rows, ["WI-099"]) is None
    why = consolidate.reabsorption_refusal(rows, ["WI-010", "WI-099"])
    assert "WI-010" in why and "RETURN-TO-DRAFT" in why
    assert "WI-099" not in why  # only the edges the draft actually held


def test_prior_absorbs_reports_each_consolidations_absorbed_set():
    rows = [
        _row("WI-001", Status="restructured", Supersedes="WI-010"),
        _row("WI-002", Status="restructured", Supersedes="WI-010"),
        _row("WI-003", Status="restructured", Supersedes="WI-011"),
        _row("WI-004", Status="cancelled", Supersedes="WI-011"),
    ]
    assert consolidate.prior_absorbs(rows) == {
        "WI-010": ["WI-001", "WI-002"],
        "WI-011": ["WI-003"],
    }


# --- the draft ------------------------------------------------------------------


def test_the_minted_draft_carries_the_scope_the_digests_and_the_evidence(tmp_path):
    rows = [
        _row("WI-001", SpecRef="docs/plans/a.md"),
        _row("WI-002", SpecRef="docs/plans/a.md"),
    ]
    repo = _repo(tmp_path, rows)
    draft, why = consolidate.census_draft(repo, rows)
    assert why is None, why
    assert draft["kind"] == "adjudication"
    assert draft["brief"] == "consolidate"
    assert draft["priority"] == consolidate.PRIORITY == 9
    assert draft["buildtier"] == "strong"
    assert draft["adjudicates"] == ["WI-001", "WI-002"]
    queue_sha, spine_sha = consolidate.parse_digests(draft["digests"])
    assert queue_sha == consolidate.queue_digest(rows)
    assert spine_sha == consolidate.spine_digest(repo)
    # The title is deterministic for the queue state, so the mint's exact-title
    # dedup is a real second line of defence behind the digest guard.
    assert queue_sha in draft["title"]
    assert consolidate.census_draft(repo, rows)[0]["title"] == draft["title"]
    # The context states the evidence and concludes NOTHING.
    assert "concluded NOTHING" in draft["context"]
    assert "share one spec of record" in draft["context"]


def test_a_busy_station_is_not_the_moment_and_not_an_error(tmp_path):
    """The judgement it would mint must run alone, and the rows it would judge
    may be the ones those lanes are holding — so a busy station is a no-op with
    no refusal to report.

    The mint arm lives in `intake` and not here, and the arrow is the reason:
    `intake._mint` is the one allocator of a WI id (ruling R1), so this module
    decides and never writes. Wiring it the other way made a real import cycle
    that `tests/test_import_layers.py` caught."""
    intake = load_script("intake")
    assert intake.mint_consolidation(tmp_path, busy=True) == ([], None)
    assert not hasattr(consolidate, "census_mint")
