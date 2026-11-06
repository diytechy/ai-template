"""The merge slot's mint files the owner's held act as an open item (TC-147).

A sitting that rules MEANING on a row the approval dial holds cannot end in a
lane: the lane lands the text, and the act is the owner's on trunk. So the mint
at that landing (`intake.intake_after_merge`, and `intake.py sweep` replaying
it) files one queued owner row per registry and one pending open item naming the
rows, their verdicts and the act's command, the row's `needs` citing the item, in
its one commit, and those rows leave the landing's amendment row (LLR-153,
LLR-364). The act copies a whole registry, so the grouping is the registry's, and
the tests run each minted command through the real `intake.py snapshot`.

The writer's input is a closed set: every state the tests below do not mint for
writes nothing. Every repository, commit and snapshot here is the real one, as
`tests/test_intake_settled.py` builds them; a verdict's binding is written by
its one writer, `kitlib.sitting.write_binding`. A test of a state that writes
nothing names in its docstring the wrong arm it would catch.

Implements: TC-147
"""

import re
import shlex
import tomllib

import pytest
from conftest import env_gate_skipif, load_script, run_py, set_process_key
from test_intake_settled import (
    AMENDED,
    LLR_AMENDED,
    LLR_ORIGINAL,
    SCRIPTS,
    SR2_AMENDED,
    SR2_ORIGINAL,
    COPY_REL,
    SR_REL,
    _act,
    _amendment_rows,
    _commit,
    _frontmatter,
    _git,
    _llr001,
    _repo,
    _sr002,
    _sweep,
    _write_llrs,
    _write_srs,
)
from test_ruling_sync import _drop_blob

pytestmark = env_gate_skipif("git")

intake = load_script("intake")
ac = load_script("agent_common")
acceptance_record = load_script("acceptance_record")
adjudicate_brief = load_script("adjudicate_brief")
amendment_brief = load_script("amendment_brief")
gen_open_items = load_script("gen_open_items")
ct = load_script("check_trajectory")
sched = load_script("schedule")
SNAP = load_script("baseline_snapshot")
trace = load_script("trace")
# `scripts/` is on sys.path once `load_script` has run.
import kitlib.ladder as kit_ladder  # noqa: E402  (after the loads above)
import kitlib.sitting as ksitting  # noqa: E402  (after the loads above)
import kitlib.stage as kit_stage  # noqa: E402  (after the loads above)

OPEN_ITEMS = intake.OPEN_ITEMS_REL
SN_REL = "docs/requirements/stakeholder-needs.toml"
VERDICT = "docs/reviews/lane/001-ADJUDICATE-a.md"
LATER_VERDICT = "docs/reviews/lane/002-ADJUDICATE-b.md"
# The dial that holds the SR rung and releases the LLR rung above it.
HOLDS_SRS = kit_ladder.STAGE_REQS
# The dial that holds the needs alone.
HOLDS_NEEDS = kit_ladder.STAGE_NEEDS

NEED = (
    "[need.SN-001]\n"
    'status = "Approved"\n'
    'need = "{}"\n'
    'why = "It is the point."\n'
    'priority = "M"\n'
    'acceptance = "Two numbers add."\n'
)
NEED_ORIGINAL = "A user can add two numbers."
NEED_AMENDED = "A user can add two integers."


# --- the repository, its dial and its sittings -----------------------------------


def _held_repo(tmp_path, dial=HOLDS_SRS, extra="", llrs="", needs=""):
    """A trunk with the dial declared, an empty open-items registry and every
    row signed into the snapshot. `(root, sha)`: the range's `before`."""
    root, _first = _repo(tmp_path, seed=False, extra=extra, llrs=llrs)
    (root / OPEN_ITEMS).write_bytes(b"# The open items.\n")
    if needs:
        (root / SN_REL).write_bytes(needs.encode("utf-8"))
    set_process_key(root, "attestation", "human_approval_through", dial)
    SNAP.copy_live(root, seed=True)
    return root, _commit(root, "the dial, the registry and the first signing")


def _row_lines(rulings):
    return "".join(
        "- [{}] {} -> judged -> judged -> same\n".format(tag, rid)
        for rid, tag in rulings.items()
    )


def _amendment_part(rulings):
    """An amendment verdict's row lines and machine line: MEANING when any row
    is, as the verdict's own rule reads it."""
    word = "MEANING" if any("MEANING" in t for t in rulings.values()) else "CLARITY"
    return "{}\nVERDICT: {} rows={}\n".format(_row_lines(rulings), word, len(rulings))


def _combined_part(rulings):
    """The same rulings as the amendment section of a combined sitting."""
    return (
        "## amendment\n\n{}\n## first-approval\n\n- [APPROVE] LLR-009 -> judged\n\n"
        "OUTCOME: APPROVE rows=1\n\n"
        "SITTING: JUDGED kinds=amendment;first-approval\n".format(
            _amendment_part(rulings)
        )
    )


def _write_verdict(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def _judged(root, rids):
    """`{row id: digest}` as a sitting binds it: the amendment brief's identity
    lines over the live rows, read back by the binding's one reader."""
    chained = [(rid.split("-")[0], rid) for rid in rids]
    lines = amendment_brief._identity(root, chained, ())
    return adjudicate_brief.requested_identities(lines)


def _sit(root, rulings, rel=VERDICT, outcome="accepted", identities=None):
    """A single-kind amendment verdict and its binding recording `outcome`,
    bound to `identities`, by default the rows' live text."""
    path = _write_verdict(root, rel, _amendment_part(rulings))
    bound = _judged(root, rulings) if identities is None else identities
    ksitting.write_binding(
        str(path), "amendment", ("amendment",), outcome, identities=bound or None
    )


def _landed(tmp_path, tag, **repo):
    """The landing the arm reads: the range amends SR-001 and carries a sitting
    ruling it `tag`, and nothing re-attests it. `(root, before, after)`."""
    root, before = _held_repo(tmp_path, **repo)
    _write_srs(root, requirement=AMENDED)
    _sit(root, {"SR-001": tag})
    return root, before, _commit(root, "amend SR-001 and sit it")


# --- what the mint did -----------------------------------------------------------


def _items(root):
    """`{id: cells}` of the open-items registry, the mint's item or none."""
    text = (root / OPEN_ITEMS).read_text(encoding="utf-8")
    return tomllib.loads(text).get("open_item", {})


def _owner_rows(root):
    """`[(relpath, frontmatter)]` of the queued rows citing an open item, the
    only rows in these repositories that do."""
    specs = sorted((root / "docs/work/queued").glob("*.md"))
    rows = [
        (path.relative_to(root).as_posix(), _frontmatter(root, path.relative_to(root)))
        for path in specs
    ]
    return [(rel, meta) for rel, meta in rows if meta.get("needs")]


def _one_owner_row(root):
    """The one owner row and the one item: `(relpath, frontmatter, id, cells)`."""
    rows, items = _owner_rows(root), _items(root)
    assert len(rows) == 1, rows
    assert len(items) == 1, items
    (oi, cells) = next(iter(items.items()))
    return rows[0][0], rows[0][1], oi, cells


def _brief(cells):
    """The text the item's card shows."""
    return " ".join(str(cells[cell]) for cell in intake.OPEN_ITEM_CELLS)


def _command(cells):
    """The act's command, as option (a) publishes it."""
    return re.search(r"`(intake\.py snapshot [^`]+)`", cells["options"]).group(1)


def _run_act(root, command):
    """`command` through the real CLI, its <record> filled in."""
    argv = shlex.split(command.replace("<record>", "docs/log.md"))
    return run_py([SCRIPTS / argv[0], "--root", root, *argv[1:]], cwd=root)


def _assert_the_act_anchors(root, command, *rids):
    """`command` exits 0 and leaves `rids` equal to their copies."""
    proc = _run_act(root, command)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    head = _commit(root, "the owner's act")
    assert acceptance_record.unanchored_rows(
        root, head, rids, intake.ROUTED_TRACED_CELLS
    ) == ({}, None)


def _last_act(root):
    return acceptance_record._ledger_acts(root, "HEAD")[-1]


def _assert_no_owner_row(root):
    assert _owner_rows(root) == []
    assert _items(root) == {}


def _assert_stays_on_the_amendment_row(root, minted, refusal):
    """The act route is unchanged: no owner row, and SR-001 is an ordinary
    amendment record."""
    assert refusal is None, refusal
    _assert_no_owner_row(root)
    assert [row["adjudicates"] for row in _amendment_rows(root, minted)] == [["SR-001"]]


def _mint(root, before, after):
    return intake.intake_after_merge(root, before, after, {}, "")


# --- the one minting state -------------------------------------------------------


def test_a_held_meaning_verdict_mints_one_owner_row_and_one_pending_item(tmp_path):
    root, before, after = _landed(tmp_path, "MEANING")
    minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    rel, meta, oi, cells = _one_owner_row(root)
    assert [path for _wid, path in minted] == [rel]
    assert cells["status"] == "pending"
    # The item names the rows, the verdict and the act's command.
    brief = _brief(cells)
    assert "SR-001" in brief and VERDICT in brief
    assert "intake.py snapshot" in brief
    assert '--approves "{}=<record>"'.format(SR_REL) in brief
    assert "--reattests SR-001" in brief
    assert "--verdict" not in brief
    # The row is the item's placeholder, titled from its rows and verdict.
    assert meta["needs"] == [oi]
    assert meta["specref"] == "{}#{}".format(OPEN_ITEMS, oi)
    assert "SR-001" in meta["title"] and "001-ADJUDICATE-a" in meta["title"]
    # Item, row and watermark land in the mint's one commit.
    assert _git(root, "rev-list", "--count", after + "..HEAD") == "1"
    changed = _git(root, "show", "--name-only", "--format=", "HEAD").splitlines()
    assert {OPEN_ITEMS, rel, trace.WATERMARK} <= set(changed)


def test_each_registry_files_its_own_row_and_item(tmp_path):
    """The act is per registry, so one verdict over two registries files two
    items, and each item's command takes its own registry's act."""
    root, before = _held_repo(tmp_path, needs=NEED.format(NEED_ORIGINAL))
    (root / SN_REL).write_bytes(NEED.format(NEED_AMENDED).encode("utf-8"))
    _write_srs(root, requirement=AMENDED)
    _sit(root, {"SN-001": "MEANING", "SR-001": "MEANING"})
    after = _commit(root, "amend both rows and sit them")
    _minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    rows, items = _owner_rows(root), _items(root)
    assert len(rows) == 2 and len(items) == 2, (rows, items)
    assert sorted(oi for _rel, meta in rows for oi in meta["needs"]) == sorted(items)
    commands = sorted(_command(cells) for cells in items.values())
    for command, rid, rel in zip(
        commands, ("SN-001", "SR-001"), (SN_REL, SR_REL), strict=True
    ):
        assert '--approves "{}=<record>"'.format(rel) in command
        assert command.endswith("--reattests " + rid)
        _assert_the_act_anchors(root, command, rid)


@pytest.mark.parametrize("shape", ["single", "combined"])
def test_a_blessed_meaning_on_a_held_rung_mints_the_same(tmp_path, shape):
    """A bless authorizes no act on a held rung, so it files the item too,
    whether the ruling is a verdict's own or a combined sitting's section."""
    root, before = _held_repo(tmp_path)
    _write_srs(root, requirement=AMENDED)
    rulings = {"SR-001": "MEANING+BLESS"}
    if shape == "single":
        _sit(root, rulings)
    else:
        path = _write_verdict(root, VERDICT, _combined_part(rulings))
        kinds = ("amendment", "first-approval")
        ksitting.write_binding(
            str(path),
            ksitting.SITTING,
            kinds,
            "accepted",
            identities=_judged(root, rulings),
        )
    after = _commit(root, "amend SR-001 and sit it")
    minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    _rel, meta, oi, cells = _one_owner_row(root)
    assert meta["needs"] == [oi]
    assert "SR-001" in _brief(cells) and VERDICT in _brief(cells)
    assert _amendment_rows(root, minted) == []


def test_a_held_row_leaves_the_amendment_row_beside_a_released_one(tmp_path):
    """LLR-364: the owner row carries the held record out of the amendment row,
    and the released row ruled the same stays on it."""
    root, before = _held_repo(tmp_path, llrs=_llr001(LLR_ORIGINAL))
    _write_srs(root, requirement=AMENDED)
    _write_llrs(root, _llr001(LLR_AMENDED))
    _sit(root, {"SR-001": "MEANING", "LLR-001": "MEANING"})
    after = _commit(root, "amend both rows and sit them")
    minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    assert [row["adjudicates"] for row in _amendment_rows(root, minted)] == [
        ["LLR-001"]
    ]
    _rel, _meta, _oi, cells = _one_owner_row(root)
    assert "SR-001" in _brief(cells) and "LLR-001" not in _brief(cells)


def test_the_hold_is_read_per_registry_not_from_the_stage(tmp_path):
    """IF-224: the dial holds the needs alone and the repo's stage stands past
    them, so a reader asking about the stage calls the SN row released and an
    unreadable stage would call the SR row held. Each row is read at its own
    rung: the SN row mints and the SR row stays on the amendment row."""
    root, before = _held_repo(
        tmp_path, dial=HOLDS_NEEDS, needs=NEED.format(NEED_ORIGINAL)
    )
    (root / SN_REL).write_bytes(NEED.format(NEED_AMENDED).encode("utf-8"))
    _write_srs(root, requirement=AMENDED)
    _sit(root, {"SN-001": "MEANING", "SR-001": "MEANING"})
    with (root / kit_stage.STAGE_FILE).open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(
            "stage = {}\nfingerprint = {}\n".format(
                kit_ladder.STAGE_TESTS, kit_stage.fingerprint(root, memo=None)
            )
        )
    after = _commit(root, "amend both rows and sit them")
    # The premise: the stage's answer is the wrong one for the SN row.
    assert ac.spine_stage_of(root) == kit_ladder.STAGE_TESTS
    assert not ac.human_holds(root / "docs", ac.spine_stage_of(root))
    minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    _rel, _meta, _oi, cells = _one_owner_row(root)
    assert "SN-001" in _brief(cells) and "SR-001" not in _brief(cells)
    assert [row["adjudicates"] for row in _amendment_rows(root, minted)] == [["SR-001"]]


def test_a_row_with_no_amendment_record_in_the_range_still_mints(tmp_path):
    """IF-091: the text moved in an earlier range and only the verdict lands in
    this one, so no amendment record names the row. The arm turns on the row
    against its copy, never on the walk."""
    root, _start = _held_repo(tmp_path)
    _write_srs(root, requirement=AMENDED)
    before = _commit(root, "amend SR-001 in an earlier range")
    _sit(root, {"SR-001": "MEANING"})
    after = _commit(root, "the sitting lands")
    assert acceptance_record.staged_spine_amendments(root, before, after) == []
    minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    _rel, _meta, _oi, cells = _one_owner_row(root)
    assert "SR-001" in _brief(cells)
    assert _amendment_rows(root, minted) == []


@pytest.mark.parametrize(
    "first, second, deciding",
    [
        pytest.param(
            ("MEANING", "accepted"),
            ("CLARITY", "accepted"),
            None,
            id="meaning-then-clarity",
        ),
        pytest.param(
            ("CLARITY", "accepted"),
            ("MEANING", "accepted"),
            LATER_VERDICT,
            id="clarity-then-meaning",
        ),
        pytest.param(
            ("MEANING", "accepted"),
            ("CLARITY", "failed"),
            VERDICT,
            id="meaning-then-failed",
        ),
    ],
)
def test_the_latest_accepted_verdict_decides_a_row_sat_twice(
    tmp_path, first, second, deciding
):
    """Each sitting's `(ruling, outcome)`, and the verdict that decides the row
    or None. The `meaning-then-clarity` case's witness is an arm that reads any
    MEANING in the range rather than the row's latest accepted ruling, which
    would mint for a row the later sitting ruled CLARITY."""
    root, before = _held_repo(tmp_path)
    _write_srs(root, requirement=AMENDED)
    _sit(root, {"SR-001": first[0]}, VERDICT, first[1])
    _commit(root, "amend SR-001 and sit it")
    _sit(root, {"SR-001": second[0]}, LATER_VERDICT, second[1])
    after = _commit(root, "sit it again")
    minted, refusal = _mint(root, before, after)
    if deciding is None:
        _assert_stays_on_the_amendment_row(root, minted, refusal)
        return
    assert refusal is None, refusal
    _rel, _meta, _oi, cells = _one_owner_row(root)
    assert deciding in _brief(cells)
    assert _amendment_rows(root, minted) == []


def test_two_verdicts_on_one_registry_file_one_item_whose_command_runs(tmp_path):
    """Refreshing the copy for one row copies every row, so an item per verdict
    publishes a command the other row refuses. One item names both rows and
    both verdicts in its prose."""
    root, before = _held_repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_AMENDED))
    _sit(root, {"SR-001": "MEANING"}, VERDICT)
    _sit(root, {"SR-002": "MEANING"}, LATER_VERDICT)
    after = _commit(root, "amend both rows and sit each")
    _minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    _rel, meta, oi, cells = _one_owner_row(root)
    assert meta["needs"] == [oi]
    assert VERDICT in _brief(cells) and LATER_VERDICT in _brief(cells)
    command = _command(cells)
    assert "--reattests SR-001,SR-002" in command
    assert "--verdict" not in command
    _assert_the_act_anchors(root, command, "SR-001", "SR-002")
    assert "verdict" not in _last_act(root)


def test_the_owner_act_is_never_listed_as_a_sessions_own(tmp_path):
    """One verdict covers every row and the item's prose names it, but the act
    is the owner's: a verdict in the ledger would list it on the owner page as
    a session's CLARITY act, on a verdict that ruled MEANING."""
    root, before = _held_repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_AMENDED))
    _sit(root, {"SR-001": "MEANING", "SR-002": "MEANING"})
    after = _commit(root, "amend both rows and sit them")
    _minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    _rel, _meta, _oi, cells = _one_owner_row(root)
    assert VERDICT in _brief(cells)
    command = _command(cells)
    assert command.endswith("--reattests SR-001,SR-002")
    _assert_the_act_anchors(root, command, "SR-001", "SR-002")
    assert "verdict" not in _last_act(root)
    audit = gen_open_items.render(root).split('class="verdict-audit"')[1]
    assert "None recorded." in audit.split("</div>")[0], audit


def test_two_landings_widen_the_act_as_the_item_states(tmp_path):
    """A second landing's row waits in the same registry when the owner acts:
    each item's own command is refused by name, and the act option (a) states,
    naming the other row, exits 0."""
    root, first = _held_repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_ORIGINAL))
    _sit(root, {"SR-001": "MEANING"}, VERDICT)
    landed = _commit(root, "the first landing")
    assert _mint(root, first, landed)[1] is None
    second = _git(root, "rev-parse", "HEAD")
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_AMENDED))
    _sit(root, {"SR-002": "MEANING"}, LATER_VERDICT)
    after = _commit(root, "the second landing")
    assert _mint(root, second, after)[1] is None
    items = _items(root)
    assert len(items) == 2, items
    commands = sorted(_command(cells) for cells in items.values())
    for command, other in zip(commands, ("SR-002", "SR-001"), strict=True):
        proc = _run_act(root, command)
        assert proc.returncode == 1, proc.stdout + proc.stderr
        assert "ABSORB" in proc.stderr and other in proc.stderr, proc.stderr
    for cells in items.values():
        assert "copies the whole registry" in cells["options"], cells["options"]
        assert "--verdict" not in cells["options"], cells["options"]
    widened = commands[0].replace("SR-001", "SR-001,SR-002")
    _assert_the_act_anchors(root, widened, "SR-001", "SR-002")
    assert "verdict" not in _last_act(root)


def test_a_replay_mints_no_second_item(tmp_path):
    """The title is the event's identity, so a sweep of the same range mints
    nothing, and the dedup still reads the row once it closes to the archive."""
    root, before, after = _landed(tmp_path, "MEANING")
    proc, _head, _new = _sweep(root, before, after)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    rel, _meta, oi, _cells = _one_owner_row(root)
    proc, head, new_head = _sweep(root, before, after)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing to mint." in proc.stdout, proc.stdout
    assert new_head == head
    # The owner rules the item and the row closes.
    registry = root / OPEN_ITEMS
    text = registry.read_bytes().replace(b'status = "pending"', b'status = "ruled"')
    registry.write_bytes(text)
    closed = root / "docs/archive/work/complete" / rel.rsplit("/", 1)[-1]
    closed.parent.mkdir(parents=True, exist_ok=True)
    (root / rel).rename(closed)
    _commit(root, "the ruling closes the owner row")
    proc, head, new_head = _sweep(root, before, after)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "nothing to mint." in proc.stdout, proc.stdout
    assert new_head == head
    assert list(_items(root)) == [oi]
    assert _owner_rows(root) == []


def test_a_non_toml_registry_refuses_and_the_merge_stands(tmp_path):
    """A CSV open-items adopter gets a named refusal at a landing that owes an
    item, and the mint writes nothing, its amendment row included. The remedy
    it states clears it: convert the carrier, then sweep the range."""
    root, _start = _held_repo(tmp_path)
    (root / OPEN_ITEMS).unlink()
    csv_rel = OPEN_ITEMS.replace(".toml", ".csv")
    (root / csv_rel).write_bytes(b"OI-ID,Title,Status\n")
    before = _commit(root, "an adopter on the CSV carrier")
    _write_srs(root, requirement=AMENDED)
    _sit(root, {"SR-001": "MEANING"})
    after = _commit(root, "amend SR-001 and sit it")
    minted, refusal = _mint(root, before, after)
    assert refusal, "no refusal"
    assert "TOML" in refusal and OPEN_ITEMS in refusal, refusal
    assert "migrate_carrier.py" in refusal and "intake.py sweep" in refusal, refusal
    assert minted == [], minted
    assert _git(root, "rev-parse", "HEAD") == after
    assert list((root / "docs/work/queued").glob("*.md")) == []
    proc = run_py([SCRIPTS / "migrate_carrier.py", "--root", root], cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    (root / csv_rel).unlink()
    _commit(root, "the carrier converted, the old file removed with it")
    proc, _head, _new = _sweep(root, before, after)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "SR-001" in _brief(_one_owner_row(root)[3])


def test_a_minted_item_passes_the_strict_checks(tmp_path):
    """No uncited error, no dangling edge, no brief-lint warning, and the row
    the item holds reads blocked. The row carries no Done-when, the placeholder
    shape the checks already pass."""
    root, before, after = _landed(tmp_path, "MEANING")
    _minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    rel, _meta, oi, _cells = _one_owner_row(root)
    wid = rel.rsplit("/", 1)[-1][: len("WI-001")]
    rows = ct.read_registry_rows(root / ct.WI_CSV)
    wis = ct.load_wis(rows)[0]
    assert ct.uncited_open_item_findings(root, rows) == []
    assert ct.open_item_specref_findings(root, wis) == []
    assert ct.validate(wis, set(), ct.load_known_ois(root)) == []
    assert ct.approval_brief_findings(root) == []
    records = sched.evaluate(sched._load(root), oi_status=sched.load_oi_status(root))
    held = {r["id"]: r for r in records}[wid]
    assert held["disposition"] == "blocked"
    assert held["reasons"] == ["blocked:open-item-pending:{}".format(oi)]


def test_a_copy_that_cannot_be_read_is_the_refusal(tmp_path):
    """IF-091: the tree lists the copy and its blob is gone, which is never the
    missing copy that reads as differing. An act moves trunk on first, so HEAD
    holds no dropped blob and the refusal is the arm's alone.

    Implements: TC-147
    """
    root, before, after = _landed(tmp_path, "MEANING")
    _act(root, "SR-001")
    _drop_blob(root, after, COPY_REL)
    rows, refusal = acceptance_record.unanchored_rows(
        root, after, {"SR-001"}, intake.ROUTED_TRACED_CELLS
    )
    assert rows == {}, rows
    assert COPY_REL in refusal and after in refusal, refusal
    assert "cannot be read" in refusal, refusal
    minted, refusal = _mint(root, before, after)
    assert minted == [], minted
    assert COPY_REL in refusal and "the merge stands" in refusal, refusal
    assert "intake.py sweep --before {} --after {}".format(before, after) in refusal
    _assert_no_owner_row(root)


def test_a_retired_row_has_no_text_to_differ_and_still_mints(tmp_path):
    """The row is gone from its registry, so the text its verdict bound cannot
    be compared. The act still names it, the one way a removal clears. Witness:
    an arm that reads a gone row as differing from its bound text."""
    root, before = _held_repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    judged = _judged(root, ["SR-002"])
    _write_srs(root)
    _sit(root, {"SR-002": "MEANING"}, identities=judged)
    after = _commit(root, "retire SR-002 and sit it")
    _minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    _rel, _meta, _oi, cells = _one_owner_row(root)
    proc = _run_act(root, _command(cells))
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- every other state writes nothing --------------------------------------------


@pytest.mark.parametrize("state", ["edited-after", "binds-nothing", "names-another"])
def test_a_row_off_its_bound_text_stays_on_the_amendment_row(tmp_path, state):
    """A verdict rules the text its binding records. The row moved after the
    sitting, or the binding records no text for it, so no sitting saw this text
    and it is sat again. Witness: an arm reading the ruling alone mints here."""
    root, before = _held_repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_ORIGINAL))
    if state == "edited-after":
        _sit(root, {"SR-001": "MEANING"})
        _write_srs(root, requirement=AMENDED + " Edited.", extra=_sr002(SR2_ORIGINAL))
    elif state == "binds-nothing":
        _sit(root, {"SR-001": "MEANING"}, identities={})
    else:
        _sit(root, {"SR-001": "MEANING"}, identities=_judged(root, ["SR-002"]))
    after = _commit(root, "amend SR-001 and sit it")
    minted, refusal = _mint(root, before, after)
    _assert_stays_on_the_amendment_row(root, minted, refusal)


def test_a_bound_row_mints_beside_one_edited_after_the_sitting(tmp_path):
    """The read is per row: the row still at its bound text is the owner's, and
    the one edited after the sitting goes back to be sat."""
    root, before = _held_repo(tmp_path, extra=_sr002(SR2_ORIGINAL))
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_AMENDED))
    _sit(root, {"SR-001": "MEANING", "SR-002": "MEANING"})
    _write_srs(root, requirement=AMENDED, extra=_sr002(SR2_AMENDED + " Edited."))
    after = _commit(root, "amend both, sit them, and edit one")
    minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    _rel, _meta, _oi, cells = _one_owner_row(root)
    assert "SR-001" in _brief(cells) and "SR-002" not in _brief(cells)
    assert [row["adjudicates"] for row in _amendment_rows(root, minted)] == [["SR-002"]]


def test_the_same_ruling_on_a_row_equal_to_its_copy_mints_nothing(tmp_path):
    """IF-091: the lane sat the row and its act copied the text, so at the
    landing the row equals its copy and no act is owed. Witness: an arm that
    skips the copy comparison mints an owner row here."""
    root, before = _held_repo(tmp_path)
    _write_srs(root, requirement=AMENDED)
    _sit(root, {"SR-001": "MEANING+BLESS"})
    _commit(root, "amend SR-001 and sit it")
    after = _act(root, "SR-001")
    minted, refusal = _mint(root, before, after)
    assert refusal is None, refusal
    assert minted == [], minted
    _assert_no_owner_row(root)
    assert _git(root, "rev-parse", "HEAD") == after


@pytest.mark.parametrize(
    "dial, tag",
    [
        pytest.param(HOLDS_SRS, "CLARITY", id="clarity-on-a-held-rung"),
        pytest.param(HOLDS_NEEDS, "MEANING", id="meaning-on-a-released-rung"),
    ],
)
def test_clarity_or_a_released_rung_mints_no_owner_row(tmp_path, dial, tag):
    """The act route is unchanged for both. Witness: an arm that ignores the
    ruling mints on the first case, and one that ignores the dial on the
    second."""
    root, before, after = _landed(tmp_path, tag, dial=dial)
    minted, refusal = _mint(root, before, after)
    _assert_stays_on_the_amendment_row(root, minted, refusal)


@pytest.mark.parametrize("state", ["no-binding", "pending", "failed", "invalid"])
def test_an_unaccepted_verdict_leaves_the_row_on_the_amendment_row(tmp_path, state):
    """An unsettled row is sat again. Witness: an arm that reads the verdict's
    text without `accepted_at` finds the MEANING row in the pending, failed and
    invalid cases, and one that walks the verdict files rather than their
    bindings finds it in the no-binding case too."""
    root, before = _held_repo(tmp_path)
    _write_srs(root, requirement=AMENDED)
    if state == "no-binding":
        _write_verdict(root, VERDICT, _amendment_part({"SR-001": "MEANING"}))
    elif state == "invalid":
        # The row line stands, but the verdict carries no machine line.
        _sit(root, {"SR-001": "MEANING"})
        _write_verdict(root, VERDICT, _row_lines({"SR-001": "MEANING"}))
    else:
        _sit(root, {"SR-001": "MEANING"}, outcome=state)
    after = _commit(root, "amend SR-001 and sit it")
    minted, refusal = _mint(root, before, after)
    _assert_stays_on_the_amendment_row(root, minted, refusal)
