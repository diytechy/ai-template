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


# --- the close's typed verdict block (restructure plan §1.5) -------------------


def _spec(body, needs="[]"):
    return (
        "+++\n"
        'id = "WI-401"\n'
        'title = "a row"\n'
        "needs = {}\n"
        'specref = "docs/plans/a.md"\n'
        "+++\n" + body
    ).format(needs)


def _verdict(block):
    return "\n## Consolidation\n\n```toml\n" + block + "```\n"


def test_a_row_with_no_consolidation_section_is_not_this_arms_case():
    """`(None, None)` — not a refusal. Every other adjudication brief reads this
    way, which is what lets ONE close serve all five."""
    assert consolidate.parse_verdict(_spec("\n## Context\n\nx\n"), "at") == (None, None)


def test_the_verdict_block_is_parsed_into_a_typed_record():
    record, why = consolidate.parse_verdict(
        _spec(
            _verdict('outcome = "queue-with-edge"\nedges = ["WI-402 needs WI-401"]\n')
        ),
        "at",
    )
    assert why is None, why
    assert record["outcome"] == "queue-with-edge"
    assert record["edges"] == [("WI-402", "WI-401")]
    assert record["returns"] == [] and record["finding"] == ""


@pytest.mark.parametrize(
    "block,expect",
    [
        ('outcome = "looks-fine"\n', "not one of"),
        ("outcome = [1]\n", "not one of"),
        ('outcome = "queue"\ntypo = 1\n', "unknown key(s)"),
        ('outcome = "queue"\nedges = ["WI-1 needs WI-2"\n', "not valid TOML"),
        (
            'outcome = "queue-with-edge"\nedges = ["WI-402 blocks WI-401"]\n',
            "is not `<WI-###> needs <WI-###>`",
        ),
        (
            'outcome = "queue-with-edge"\nedges = ["WI-402 needs WI-402"]\n',
            "wait on itself",
        ),
        ('outcome = "queue-with-edge"\n', "names no `edges`"),
        ('outcome = "return-to-draft"\n', "names no `returns`"),
        (
            'outcome = "return-to-draft"\nreturns = ["WI-402"]\n',
            "carries no `finding`",
        ),
        (
            'outcome = "queue"\nreturns = ["WI-402"]\n',
            "carries `returns`, which it does not enact",
        ),
        # TYPED, not coerced. `returns = 1` reached a `for` loop and RAISED an
        # uncaught TypeError out of a parser whose whole contract is
        # `(record, refusal)`; `returns = "WI-401"` iterated the STRING and
        # parsed as six single-character targets, so a verdict naming one row
        # enacted six nonexistent ones.
        ('outcome = "queue-with-edge"\nedges = 1\n', "a TOML LIST"),
        ('outcome = "return-to-draft"\nreturns = 1\nfinding = "x"\n', "a TOML LIST"),
        (
            'outcome = "return-to-draft"\nreturns = "WI-401"\nfinding = "x"\n',
            "a TOML LIST",
        ),
        (
            'outcome = "return-to-draft"\nreturns = [1]\nfinding = "x"\n',
            "non-string entr",
        ),
        # A DUPLICATE is not harmless: the close walks the list and MOVES each
        # target, so the second pass finds the row already gone and fails
        # half-way through a close that advertises itself as all-or-nothing.
        (
            'outcome = "return-to-draft"\nreturns = ["WI-401", "WI-401"]\nfinding = "x"\n',
            "names WI-401 twice",
        ),
        (
            'outcome = "queue-with-edge"\nedges = ["WI-1 needs WI-2", "WI-1 needs WI-2"]\n',
            "twice",
        ),
        (
            'outcome = "return-to-draft"\nreturns = ["nonsense"]\nfinding = "x"\n',
            "is not a WI-### id",
        ),
    ],
)
def test_a_malformed_verdict_block_refuses_and_never_defaults(block, expect):
    """Reading a malformed block as `queue` would silently discard a judgement
    that closes rows — so every arm names what is wrong instead. Both DIRECTIONS
    of the shape rule are here: an outcome that names nothing to enact, and an
    outcome carrying targets it would quietly ignore."""
    record, why = consolidate.parse_verdict(_spec(_verdict(block)), "at")
    assert record is None, record
    assert expect in why, why


def test_two_blocks_under_one_heading_refuse():
    text = _spec(
        '\n## Consolidation\n\n```toml\noutcome = "queue"\n```\n\n'
        '```toml\noutcome = "return-to-draft"\n```\n'
    )
    record, why = consolidate.parse_verdict(text, "at")
    assert record is None and "one verdict, one block" in why


def _rec(outcome="consolidate", **kw):
    record = {"outcome": outcome, "edges": [], "returns": [], "finding": ""}
    record.update(kw)
    return record


def _close(tmp_path, rows, record, absorbed, *, scope=None, drafts=None, recorded=None):
    """`close_refusal` over a real tree, with the cluster and the digest pair
    defaulting to the ones the census itself would have recorded — so a test
    that is about ONE rung is not tripped by another.

    Only the WRITABLE rows are materialised: `active/` has no status directory
    of its own (a claimed spec lives under `active/<branch>/`), so a fixture row
    modelling a claimed one is handed to the guard rather than written."""
    repo = _repo(
        tmp_path, [r for r in rows if r.get("Status") in wi_convert.STATUS_DIRS]
    )
    if recorded is None:
        recorded = consolidate.digests(repo, rows)
    if scope is None:
        scope = {(r.get("WI-ID") or "") for r in rows if r.get("Status") == "queued"}
    if drafts is None:
        drafts = [{"supersedes": list(absorbed)}] if absorbed else []
    return consolidate.close_refusal(
        repo,
        record,
        absorbed,
        rows,
        "at",
        scope=scope,
        drafts=drafts,
        recorded=recorded,
    )


def test_the_close_refuses_a_row_that_left_the_queue_by_name(tmp_path):
    """The census guard makes a claimed cluster row a race only a hand claim can
    produce (plan §1.5). When it happens the close refuses BY NAME rather than
    archiving work a lane is in the middle of building.

    ORDER IS THE MESSAGE: claiming a row also moves the queue digest, so the
    drift rung would fire on the same fixture. The by-name rung runs first
    because "WI-402 is no longer queued" is actionable and "the queue has moved"
    is the same fact with the row filed off."""
    rows = [_row("WI-401"), _row("WI-402", Status="active")]
    why = _close(
        tmp_path,
        rows,
        _rec(),
        ["WI-401", "WI-402"],
        scope={"WI-401", "WI-402"},
    )
    assert why and "WI-402" in why and "no longer queued" in why
    assert "WI-401" not in why


def test_the_outcome_and_the_absorbed_set_must_agree_both_ways(tmp_path):
    rows = [_row("WI-401")]
    why = _close(tmp_path, rows, _rec(), [])
    assert why and "absorbs no row is not one" in why
    why = _close(tmp_path, rows, _rec("queue"), ["WI-401"])
    assert why and "only a CONSOLIDATE verdict absorbs rows" in why


def test_a_consolidation_drafting_two_successors_is_refused(tmp_path):
    """Plan §1.2: the session drafts ONE successor. Two drafts each superseding
    part of the cluster used to close cleanly and mint two rows that split the
    scope, with nothing recording the split."""
    rows = [_row("WI-401"), _row("WI-402")]
    why = _close(
        tmp_path,
        rows,
        _rec(),
        ["WI-401", "WI-402"],
        drafts=[{"supersedes": ["WI-401"]}, {"supersedes": ["WI-402"]}],
    )
    assert why and "drafted 2 successor(s)" in why and "ONE row" in why
    assert _close(tmp_path, rows, _rec(), ["WI-401", "WI-402"]) is None


def test_the_close_refuses_a_row_outside_the_adjudicates_cluster(tmp_path):
    """THE SCOPE CELL IS BINDING, not decorative. A draft superseding a row the
    census never clustered used to close, merge and archive it — the row's own
    Context says "judge those rows and no others", the brief template says it,
    and plan §1.3 clause 2 says it, while nothing enforced it. The
    first-approval sibling has bounded its act this way since WI-572."""
    rows = [_row("WI-401"), _row("WI-402"), _row("WI-409")]
    why = _close(
        tmp_path,
        rows,
        _rec(),
        ["WI-401", "WI-402", "WI-409"],
        scope={"WI-401", "WI-402"},
    )
    assert why and "WI-409" in why and "OUTSIDE this row's `Adjudicates` scope" in why
    assert "WI-401" not in why.split("scope (")[0]
    # ...and the bound covers every id the verdict MOVES, not only the absorbed.
    why = _close(
        tmp_path,
        rows,
        _rec("return-to-draft", returns=["WI-409"], finding="x"),
        [],
        scope={"WI-401", "WI-402"},
    )
    assert why and "WI-409" in why and "OUTSIDE" in why
    why = _close(
        tmp_path,
        rows,
        _rec("queue-with-edge", edges=[("WI-402", "WI-409")]),
        [],
        scope={"WI-401", "WI-402"},
    )
    assert why and "WI-409" in why and "OUTSIDE" in why


def test_the_close_refuses_a_verdict_whose_digests_have_drifted(tmp_path):
    """The pair is recorded at the mint precisely so a stale verdict is
    detectable, and nothing compared it: a forged or simply out-of-date cell
    enacted a verdict against a queue that had moved underneath it."""
    rows = [_row("WI-401"), _row("WI-402")]
    absorbed = ["WI-401", "WI-402"]
    assert _close(tmp_path, rows, _rec(), absorbed) is None
    why = _close(tmp_path, rows, _rec(), absorbed, recorded="deadbeefdead|cafebabecafe")
    assert why and "QUEUE has moved" in why and "deadbeefdead" in why
    # The spine half fails differently, and the message says which.
    repo = _repo(tmp_path, rows)
    live_queue = consolidate.queue_digest(rows)
    why = _close(
        tmp_path, rows, _rec(), absorbed, recorded=live_queue + "|cafebabecafe"
    )
    assert why and "SPINE has moved" in why
    # A missing cell is its own refusal: an unverifiable verdict is not enacted.
    why = _close(tmp_path, rows, _rec(), absorbed, recorded="")
    assert why and "no usable `Digests` cell" in why
    assert repo.is_dir()


def test_the_close_refuses_the_lineage_the_mint_would_have_refused(tmp_path):
    """The close/mint split was NOT all-or-nothing: `reabsorption_refusal` ran
    only inside `_pre_mint_refusal`, one commit after the close had committed
    and the merge had stood. A verdict absorbing an earlier consolidation's
    successor closed, merged, minted NOTHING, and left the queue byte-identical
    to the state its own `Digests` cell recorded — so `_judged_refusal` answered
    "already judged" forever and the cluster was un-consolidatable by hand.
    A refusal evaluable before the close is now evaluated before the close."""
    rows = [
        _row("WI-390", Status="restructured"),
        _row("WI-412", Supersedes="WI-390"),
        _row("WI-401"),
    ]
    why = _close(
        tmp_path,
        rows,
        _rec(),
        ["WI-401", "WI-412"],
        scope={"WI-401", "WI-412"},
    )
    assert why and "WI-412" in why and "RETURN-TO-DRAFT" in why


def test_the_verdict_files_machine_line_and_the_typed_block_are_one_fact():
    """`absorbs=` and `needs=` are required on every alternative of this brief's
    grammar and NOTHING read them: a verdict file could say `OUTCOME: QUEUE
    needs=- absorbs=-` while the block said `consolidate` and three rows were
    archived. The counters are now reconciled with the block and the drafts."""
    line = "- [MINOR] a finding\nOUTCOME: CONSOLIDATE needs=- absorbs=WI-401;WI-402\n"
    machine = consolidate.parse_machine_line(line)
    assert machine == ("CONSOLIDATE", {"needs": "-", "absorbs": "WI-401;WI-402"})
    rec = _rec()
    assert (
        consolidate.reconcile_refusal(machine, rec, ["WI-402", "WI-401"], "at") is None
    )
    why = consolidate.reconcile_refusal(machine, rec, ["WI-401"], "at")
    assert why and "absorbs=" in why and "one fact" in why
    why = consolidate.reconcile_refusal(
        ("QUEUE", {"needs": "-", "absorbs": "-"}), rec, [], "at"
    )
    assert why and "OUTCOME: QUEUE" in why and "outcome = 'consolidate'" in why
    # The `needs=` counter is reconciled against the edges the same way.
    edged = _rec("queue-with-edge", edges=[("WI-402", "WI-401")])
    ok = ("QUEUE-WITH-EDGE", {"needs": "WI-402", "absorbs": "-"})
    assert consolidate.reconcile_refusal(ok, edged, [], "at") is None
    why = consolidate.reconcile_refusal(
        ("QUEUE-WITH-EDGE", {"needs": "WI-999", "absorbs": "-"}), edged, [], "at"
    )
    assert why and "needs=WI-999" in why
    # A verdict file with no machine line is not this rung's business: the
    # session's DONE was already gated on it by `agent_loop.worker_endstate`.
    assert consolidate.parse_machine_line("no line here") is None


def test_the_absorbed_done_when_blocks_are_quoted_verbatim(tmp_path):
    """Plan §1.5 / Done-when 4. The shipped brief PROMISES this, so a judge who
    follows it writes a boundary sentence and nothing else — without the
    quoting, the successor a lane then builds carries no acceptance criteria."""
    rows = [_row("WI-401"), _row("WI-402")]
    repo = _repo(tmp_path, rows)
    work = repo / "docs" / "work" / "queued"
    for path, body in zip(
        sorted(work.iterdir()), ("Ship the adder.", "Test the adder.")
    ):
        path.write_text(
            path.read_text(encoding="utf-8")
            + "\n## Context\n\nctx\n\n## Done-when\n\n1. {}\n".format(body),
            encoding="utf-8",
            newline="\n",
        )
    quoted = consolidate.absorbed_done_when(repo, ["WI-401", "WI-402"])
    assert "WI-401 (absorbed)" in quoted and "WI-402 (absorbed)" in quoted
    assert "1. Ship the adder." in quoted and "1. Test the adder." in quoted
    assert "ctx" not in quoted  # the Done-when block, not the whole body
    # A row with no Done-when section is STATED, never silently dropped.
    stated = consolidate.absorbed_done_when(repo, ["WI-409"])
    assert "WI-409 (absorbed)" in stated and "declared no `## Done-when`" in stated
    assert consolidate.absorbed_done_when(repo, []) == ""


def test_the_absorbed_set_has_exactly_one_carrier():
    """It is the drafts' `supersedes` and nothing else — the value the mint
    actually uses. A second copy in the verdict block could disagree with it."""
    drafts = [
        {"supersedes": ["WI-401", "WI-402"]},
        {"supersedes": "WI-402;WI-403"},
        {"title": "no lineage"},
    ]
    assert consolidate.absorbed_ids(drafts) == ["WI-401", "WI-402", "WI-403"]
    assert consolidate.absorbed_ids([]) == []


# --- the pure text transforms --------------------------------------------------


def test_an_absorbed_rows_scope_text_is_byte_identical_and_specref_kept():
    """The same rule `partial` follows, for the reason R-F's carve-out states:
    the successor's lineage is worth nothing if the thread it continues has
    already been cut. The ONLY edit is the one-line Deliverable, and it sits
    BEFORE `## Context` — after it, `parse_spec_deliverable` clips the body and
    the cell reads EMPTY (R-A hard error)."""
    original = _spec("\n## Context\n\nThe original scope, untouched.\n")
    moved = consolidate.restructured_text(original, "WI-500")
    assert moved.index("## Deliverable") < moved.index("## Context")
    assert moved.count("Restructured into WI-500.") == 1
    assert 'specref = "docs/plans/a.md"' in moved
    assert "The original scope, untouched." in moved
    # ...and nothing else moved: the frontmatter is byte-identical.
    assert moved.split("+++")[1] == original.split("+++")[1]


def test_a_returned_rows_finding_is_quoted_verbatim_into_its_context():
    """Quoted, not summarised: a row bounced back with no named referent is a
    row that gets re-queued unchanged, which is the loop this outcome breaks."""
    text = _spec("\n## Context\n\nThe original context.\n")
    out = consolidate.returned_text(text, "WI-402 re-proposes what WI-390 refuted.")
    assert "> WI-402 re-proposes what WI-390 refuted." in out
    assert "The original context." in out
    # A row with no Context yet gains one rather than losing the finding.
    bare = consolidate.returned_text(_spec(""), "the reason")
    assert "## Context" in bare and "> the reason" in bare


def test_the_edge_write_is_surgical_and_idempotent():
    text = _spec("\n## Context\n\nkeep me\n", needs='["WI-300"]')
    edged = consolidate.edged_text(text, "WI-401")
    assert 'needs = ["WI-300", "WI-401"]' in edged
    assert "keep me" in edged
    # Already waiting — hard or soft — comes back UNCHANGED, so the caller
    # reports a no-op instead of committing one.
    assert consolidate.edged_text(edged, "WI-401") == edged
    soft = _spec("", needs='["~WI-401"]')
    assert consolidate.edged_text(soft, "WI-401") == soft
    # A row with no readable needs line is a refusal, not a silent skip.
    assert consolidate.edged_text('+++\nid = "WI-1"\n+++\n', "WI-401") is None


def test_the_text_transforms_survive_a_crlf_checkout():
    """LINE-WISE against the shared fence constant, like the canonical reader.

    A `text.partition("\\n+++\\n")` finds nothing on a CRLF checkout (Windows with
    `core.autocrlf=true`), so `restructured_text` returned None and
    `_absorbed_move` skipped the row silently — on EVERY absorbed row, on that
    platform — and `returned_text` appended a SECOND `## Context` heading. The
    suite could not see it because every fixture calls `conftest.pin_autocrlf`,
    which is exactly why this case is built by hand rather than checked out."""
    crlf = (
        "+++\r\n"
        'id = "WI-401"\r\n'
        'specref = "docs/plans/a.md"\r\n'
        "+++\r\n"
        "\r\n## Context\r\n\r\nThe original scope.\r\n"
    )
    moved = consolidate.restructured_text(crlf, "WI-500")
    assert moved is not None
    assert "Restructured into WI-500." in moved
    assert "The original scope." in moved
    assert moved.index("## Deliverable") < moved.index("## Context")
    returned = consolidate.returned_text(crlf, "the finding")
    assert returned.count("## Context") == 1
    assert "> the finding" in returned
    # ...and LF is unchanged by the same reader.
    lf = crlf.replace("\r\n", "\n")
    assert consolidate.restructured_text(lf, "WI-500") is not None
    assert consolidate.returned_text(lf, "the finding").count("## Context") == 1


def test_the_census_never_mints_a_row_whose_specref_cannot_resolve(tmp_path):
    """`integrate.claim` REFUSES a row whose SpecRef does not resolve to an
    in-repo file (R-E, WI-370). A hard `docs/work/README.md` on a repo that does
    not ship it mints a judgement that can never be claimed — and because
    `_judgement_first` puts a judgement at the head of the frontier, the run
    exits 1 on every tick from then on, the queue wedged by the census that was
    meant to unblock it.

    Measured the moment the census was wired into `dispatch._admit`, on a
    fixture repo with no `docs/work/README.md`. The probes are ordered, and the
    census DECLINES rather than minting an unclaimable row when none resolves."""
    rows = [
        _row("WI-401", SpecRef="docs/plans/a.md"),
        _row("WI-402", SpecRef="docs/plans/a.md"),
    ]
    repo = _repo(tmp_path, rows)
    # `_repo` writes the SR registry, which is the fallback probe.
    assert consolidate._specref(repo) == "docs/requirements/system-requirements.toml"
    draft, why = consolidate.census_draft(repo, rows)
    assert why is None, why
    assert (repo / draft["specref"]).is_file()
    # The first probe wins where the repo ships it.
    (repo / "docs" / "work" / "README.md").write_text(
        "# the work registry\n", encoding="utf-8", newline="\n"
    )
    assert consolidate.census_draft(repo, rows)[0]["specref"] == "docs/work/README.md"
    # ...and with NO probe resolving, the census declines by name.
    (repo / "docs" / "work" / "README.md").unlink()
    (repo / "docs" / "requirements" / "system-requirements.toml").unlink()
    draft, why = consolidate.census_draft(repo, rows)
    assert draft is None
    assert why and "no candidate spec-of-record resolves" in why
