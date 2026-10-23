"""The held-rung rule on real git: every lane judged at landing, a marked
commit judged outside a lane, and a squash judged by what it folds in.

A held-rung spine row's approval lands from a lane only as a CLARITY
re-attestation bound to the text its verdict judged (the binding's identity).
Each lane commit is judged against each of its parents by the merge slot's
lane-commit walk, whoever built the lane: a loop's, a coordinator's, or a
re-claimed one. The pre-commit `held-status` step judges a squash landing by
its lane commits, and judges a commit made under the loop marker outside a
claimed lane; an unmarked plain trunk commit is not judged (the ruled
residual). The loop writers refuse the same change before they write, outside
a lane.

Every fixture is a real git repository built like the merge slot's own tests
(`tests/integrate_fixtures.py`): a trunk declaring the dial, the needs file
with its recorded copy, and a claimed lane. The dial holds every rung
(`DevStg-Release`), so a stakeholder need sits on a held rung (`DevStg-Needs`).

Two cases are characterizations of what the old rules already got right,
each naming the wrong rule it would catch.

Real git and the merge slot end to end, so this module is registered slow
(`tests/conftest.py` SLOW_MODULES); the pure halves are
`tests/test_held_status.py`'s.
"""

import pytest
from conftest import SCRIPTS, env_gate_skipif, load_script, run_py
from integrate_fixtures import (
    T_BASE,
    T_CODE,
    T_LATER,
    _commit,
    _git,
    _rev,
    claim_repo,
    integ,
    refused,
)

from kitlib import provenance as kprovenance  # noqa: E402  (scripts/ is on the path)
from kitlib import sitting as ksitting  # noqa: E402

pytestmark = env_gate_skipif("git")

ar = load_script("acceptance_record")
held_status = load_script("held_status")
adjudicate_act = load_script("adjudicate_act")
spine_carrier = load_script("spine_carrier")
snap = load_script("baseline_snapshot")
tta = load_script("text_then_act")

DIAL = "DevStg-Release"
NEEDS_RUNG = "DevStg-Needs"
FRAME_RUNG = "DevStg-Boundary"
NEEDS = "docs/requirements/stakeholder-needs.toml"
FRAME = "docs/requirements/external.toml"
COPY = "{}/{}".format(snap.SNAPSHOT_DIR, NEEDS)
VERDICT = "docs/reviews/lane/000-ADJUDICATE-x.md"
MARK = kprovenance.LOOP_SESSION_ENV
SESSION = "20261023T101500Z-a1b2c3"
STEP = [SCRIPTS / "check.py", "--run-steps", "held-status"]
NO_REGEN = "import sys\nsys.exit(0)\n"
BAR = "no [product] test declaration"
GAP = "SR-001 is not Approved (Status=Drafted)"

# Each need: (status, need text, source). `source` is a traced cell.
BASE = {
    "SN-001": ("Drafted", "a team can use it", "interview 1"),
    "SN-002": ("Drafted", "a team can adopt it", "interview 2"),
}


def _with(rows, rid, status=None, need=None, source=None):
    """`rows` with row `rid` changed; a `None` cell keeps its value."""
    was = rows.get(rid, ("Drafted", "a new need", "interview 3"))
    out = dict(rows)
    out[rid] = (status or was[0], need or was[1], source or was[2])
    return out


def _needs_text(rows):
    text = '[stakeholder.STK-01]\nstatus = "Drafted"\n\n'
    for rid, (status, need, source) in sorted(rows.items()):
        text += (
            "[need.{}]\n"
            'status = "{}"\n'
            'need = "{}"\n'
            'why = "the owner asked"\n'
            'priority = "M"\n'
            'acceptance = "it is shown"\n'
            'source = "{}"\n\n'
        ).format(rid, status, need, source)
    return text


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _write_needs(root, rows):
    _write(root, NEEDS, _needs_text(rows))


def _frame_text(rows):
    return "".join(
        '[boundary.{}]\nstatus = "{}"\n\n'.format(rid, status)
        for rid, status in sorted(rows.items())
    )


def _marked(message):
    return "{}\n\nLoop-Session: {}".format(message, SESSION)


def _no_regen(home, monkeypatch):
    """The trunk step stood in by a no-op: what these tests judge is the tree
    a writer or a lane commits, and the real regeneration adds nothing to it."""
    stub = home / "no-regen"
    stub.mkdir(exist_ok=True)
    (stub / "trunk_step.py").write_text(NO_REGEN, encoding="utf-8", newline="\n")
    monkeypatch.setattr(integ.bookkeeping, "SCRIPTS", stub)


def _trunk(home, monkeypatch, needs=BASE, frame=None):
    """WI-401 queued on a trunk that declares the dial and carries the needs
    file (and, when given, the frame), with their recorded copy seeded."""
    home.mkdir(parents=True, exist_ok=True)
    root = claim_repo(home)
    _write(
        root,
        "docs/process.toml",
        '[attestation]\nhuman_approval_through = "{}"\n'.format(DIAL),
    )
    _write_needs(root, needs)
    if frame is not None:
        _write(root, FRAME, _frame_text(frame))
    snap.copy_live(root, seed=True)
    _commit(root, "the needs, their record and the dial", when=T_BASE)
    _no_regen(home, monkeypatch)
    return root


def _verdict(root, kind, rows, identities=None, tag=None):
    """The verdict and its accepted binding that a route leaves in the lane:
    an amendment part ruling `rows` CLARITY (or `tag`), or a first-approval
    part APPROVING them; `identities` is the binding's identity cell."""
    word = tag or {"amendment": "CLARITY", "first-approval": "APPROVE"}[kind]
    label = "MEANING" if word.startswith("MEANING") else word
    line = {"amendment": "VERDICT", "first-approval": "OUTCOME"}[kind]
    text = "".join(
        "- [{}] {} -> judged -> judged -> same\n".format(word, r) for r in rows
    )
    _write(root, VERDICT, text + "\n{}: {} rows={}\n".format(line, label, len(rows)))
    if identities is None:
        binding = ksitting.render_requested(kind, (kind,), "accepted")
    else:
        render = ksitting.render_requested
        binding = render(kind, (kind,), "accepted", identities=identities)
    _write(root, ksitting.requested_path(VERDICT), binding)


def _digest(root, rid, rev="HEAD"):
    """The approved-text digest of need `rid` as committed at `rev`."""
    digest = ar.approved_text_digest
    row = ar.rows_at(root, rev, NEEDS, "SN-ID")[rid]
    return digest(NEEDS, "SN-ID", row)


def _lane(root, monkeypatch, steps, kind="ordinary"):
    """Claim WI-401 on `wi-401`, commit each `(message, write)` step on it,
    close it into complete/ and return to trunk. `kind` is whose lane it is:
    "loop" claims it under the loop marker and marks every commit; "reclaimed"
    claims it under the marker, then takes the attended re-claim, after which
    its commits are unmarked; "ordinary" marks nothing."""
    if kind in ("loop", "reclaimed"):
        monkeypatch.setenv(MARK, SESSION)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    monkeypatch.delenv(MARK, raising=False)
    mark = _marked if kind == "loop" else (lambda message: message)
    _git(root, "checkout", "-q", "wi-401")
    if kind == "reclaimed":
        _git(
            root,
            "commit",
            "--allow-empty",
            "-qm",
            kprovenance.reclaim_subject("wi-401"),
        )
    for message, write in steps:
        write(root)
        _commit(root, mark(message), when=T_CODE)
    (root / "docs" / "work" / "complete").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/complete/WI-401-widget.md",
    )
    _commit(root, mark("close: WI-401 -> complete"), when=T_LATER)
    _git(root, "checkout", "-q", "main")
    return root


def _refused_by_the_rule(root, rid, rung):
    """The slot refuses the lane, merging nothing, naming the row, its rung
    and the dial."""
    refusal = refused(root, "wi-401", "smoke")
    for word in (rid, rung, DIAL):
        assert word in refusal, (word, refusal)
    return refusal


def _lands(root):
    """The slot admits the lane through every rule, stopping only at this
    fixture's undeclared product bar."""
    refusal = integ.integrate_one(root, "wi-401", "smoke")
    assert refusal and BAR in refusal, refusal


def _the_rule_rides_the_walk():
    """A held lane lands here only because the lane rule judged it."""
    names = [rider.__name__ for rider in tta.LANE_COMMIT_RIDERS]
    assert "commit_held_approval_lines" in names, names


# --- the lane steps -------------------------------------------------------------


def _approve_sn1_with_its_copy(root):
    _write_needs(root, _with(BASE, "SN-001", status="Approved"))
    snap.copy_live(root)
    _verdict(root, "first-approval", ["SN-001"])


def _flip_sn1_without_its_copy(root):
    _write_needs(root, _with(BASE, "SN-001", status="Approved"))
    _verdict(root, "first-approval", ["SN-001"])


APPROVED = _with(BASE, "SN-001", status="Approved")


def _amend(need="a team can use the kit", **more):
    def write(root):
        rows = _with(APPROVED, "SN-001", need=need)
        for rid, cells in more.items():
            rows = _with(rows, rid.replace("_", "-"), **cells)
        _write_needs(root, rows)

    return write


def _bound_verdict(tag=None, bind=True):
    def write(root):
        ids = {"SN-001": _digest(root, "SN-001")} if bind else None
        _verdict(root, "amendment", ["SN-001"], identities=ids, tag=tag)

    return write


def _reattest(named=True):
    def write(root):
        snap.copy_live(
            root, reattests=frozenset({"SN-001"}), verdict=VERDICT if named else None
        )

    return write


# --- the slot: every lane judged at landing ----------------------------------------


def test_a_lane_approving_a_held_SN_with_its_copy_is_refused(tmp_path, monkeypatch):
    # Backed by an accepted APPROVE verdict, so the approval-act rung admits
    # it: the gap is that nothing held the rung.
    root = _trunk(tmp_path, monkeypatch)
    _lane(root, monkeypatch, [("WI-401: approve SN-001", _approve_sn1_with_its_copy)])
    _refused_by_the_rule(root, "SN-001", NEEDS_RUNG)


def _rider_lines(root, commit):
    """The lane rule's lines for one lane commit, joined: the rider the merge
    slot's lane-commit walk runs. Asked directly where an earlier rung of the
    slot already refuses the lane, so the rule's own answer is still pinned."""
    rider = held_status.commit_held_approval_lines
    return "\n".join(rider(root, commit))


def test_a_lane_flipping_a_held_rows_status_without_its_copy_is_refused(
    tmp_path, monkeypatch
):
    # The slot's copy check refuses this lane before the walk; the rider, run
    # on the lane commit, refuses it too, by row, rung and dial.
    root = _trunk(tmp_path, monkeypatch)
    _lane(root, monkeypatch, [("WI-401: flip SN-001", _flip_sn1_without_its_copy)])
    refused(root, "wi-401", "smoke")
    lines = _rider_lines(root, _rev(root, "wi-401~1"))
    for word in ("SN-001", NEEDS_RUNG, DIAL):
        assert word in lines, (word, lines)


def test_loop_coordinator_and_reclaimed_lanes_are_judged_alike(tmp_path, monkeypatch):
    for kind in ("loop", "ordinary", "reclaimed"):
        root = _trunk(tmp_path / kind, monkeypatch)
        steps = [("WI-401: approve SN-001", _approve_sn1_with_its_copy)]
        _lane(root, monkeypatch, steps, kind=kind)
        _refused_by_the_rule(root, "SN-001", NEEDS_RUNG)


def _clarity_lane(home, monkeypatch, *steps, needs=APPROVED):
    root = _trunk(home, monkeypatch, needs=needs)
    return _lane(root, monkeypatch, list(steps))


@pytest.mark.parametrize("named", [True, False], ids=["named", "unnamed"])
def test_a_held_CLARITY_reattestation_bound_to_the_exact_text_lands(
    tmp_path, monkeypatch, named
):
    # Naming the verdict is for audit only: both acts land.
    _the_rule_rides_the_walk()
    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: amend SN-001", _amend()),
        ("WI-401: the verdict", _bound_verdict()),
        ("WI-401: re-attest SN-001", _reattest(named)),
    )
    _lands(root)


def test_held_text_changed_after_its_CLARITY_verdict_is_refused_at_the_slot(
    tmp_path, monkeypatch
):
    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: amend SN-001", _amend()),
        ("WI-401: the verdict", _bound_verdict()),
        ("WI-401: amend SN-001 again", _amend("a team can use the whole kit")),
        ("WI-401: re-attest SN-001", _reattest()),
    )
    _refused_by_the_rule(root, "SN-001", NEEDS_RUNG)


def test_a_binding_with_no_identity_cell_is_refused(tmp_path, monkeypatch):
    # A verdict sat before the identity existed binds no text: it is re-sat.
    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: amend SN-001", _amend()),
        ("WI-401: the verdict", _bound_verdict(bind=False)),
        ("WI-401: re-attest SN-001", _reattest()),
    )
    _refused_by_the_rule(root, "SN-001", NEEDS_RUNG)


def test_a_held_MEANING_BLESS_reattestation_is_refused(tmp_path, monkeypatch):
    # A blessing is a released rung's act; on a held rung only CLARITY is.
    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: amend SN-001", _amend()),
        ("WI-401: the verdict", _bound_verdict(tag="MEANING+BLESS")),
        ("WI-401: re-attest SN-001", _reattest()),
    )
    _refused_by_the_rule(root, "SN-001", NEEDS_RUNG)


# The bound-CLARITY exception's other refusals, as the lane rule reads them.
# Each is `(verdict text, binding outcome)`, the binding recording SN-001's
# digest at the sitting; the slot's backing rung refuses these lanes before
# the walk, so the lane rule's own answer is asked of the act commit directly.
_RULED_TWICE = "- [{}] SN-001 -> judged -> judged -> same\n"
_UNEXCEPTED = {
    # Witness: an exception reading the first tag a row carries (or any
    # CLARITY tag) would admit this.
    "ruled MEANING then CLARITY": (
        _RULED_TWICE.format("MEANING") + _RULED_TWICE.format("CLARITY"),
        "accepted",
    ),
    # Witness: an exception reading the last tag a row carries would admit
    # this.
    "ruled CLARITY then MEANING": (
        _RULED_TWICE.format("CLARITY") + _RULED_TWICE.format("MEANING"),
        "accepted",
    ),
    # Witness: an exception reading the verdict text without its binding's
    # recorded outcome would admit these two.
    "failed outcome": (_RULED_TWICE.format("CLARITY"), "failed"),
    "pending outcome": (_RULED_TWICE.format("CLARITY"), "pending"),
    # Witness: an exception taking any accepted CLARITY verdict whose binding
    # names the row's digest, without the verdict ruling that row, would
    # admit this.
    "another row ruled": (
        "- [CLARITY] SN-002 -> judged -> judged -> same\n",
        "accepted",
    ),
}


@pytest.mark.parametrize("case", sorted(_UNEXCEPTED))
def test_an_unaccepted_or_unruled_CLARITY_binding_is_no_exception(
    tmp_path, monkeypatch, case
):
    """Characterization: already-correct behaviour of the bound-CLARITY
    exception (the case's witness names the wrong implementation it would
    catch). The copy claim on SN-001 is refused by the lane rule, naming the
    row, its rung and the dial."""
    text, outcome = _UNEXCEPTED[case]

    def verdict(root):
        label = "MEANING" if "MEANING" in text else "CLARITY"
        _write(root, VERDICT, text + "\nVERDICT: {} rows=1\n".format(label))
        binding = ksitting.render_requested(
            "amendment",
            ("amendment",),
            outcome,
            identities={"SN-001": _digest(root, "SN-001")},
        )
        _write(root, ksitting.requested_path(VERDICT), binding)

    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: amend SN-001", _amend()),
        ("WI-401: the verdict", verdict),
        ("WI-401: re-attest SN-001", _reattest()),
    )
    refused(root, "wi-401", "smoke")
    lines = _rider_lines(root, _rev(root, "wi-401~1"))
    for word in ("SN-001", NEEDS_RUNG, DIAL):
        assert word in lines, (case, word, lines)


def test_a_held_retirement_is_refused(tmp_path, monkeypatch):
    def retire(root):
        rows = dict(APPROVED)
        del rows["SN-001"]
        _write_needs(root, rows)

    def verdict(root):
        _verdict(root, "amendment", ["SN-001"])

    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: retire SN-001", retire),
        ("WI-401: the verdict", verdict),
        ("WI-401: re-attest SN-001", _reattest()),
    )
    _refused_by_the_rule(root, "SN-001", NEEDS_RUNG)


def test_a_held_CLARITY_act_carrying_an_edited_Drafted_sibling_lands(
    tmp_path, monkeypatch
):
    # The whole-registry copy carries SN-002, Drafted and edited in the lane;
    # it claims approval nowhere, so it is not judged.
    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: amend SN-001 and SN-002", _amend(SN_002={"need": "a team adopts"})),
        ("WI-401: the verdict", _bound_verdict()),
        ("WI-401: re-attest SN-001", _reattest(named=False)),
    )
    _lands(root)


def test_a_traced_only_copy_move_lands(tmp_path, monkeypatch):
    # SN-002 is approved and moves only its traced `source` in the copy.
    needs = _with(APPROVED, "SN-002", status="Approved")
    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        (
            "WI-401: amend SN-001",
            _amend(SN_002={"status": "Approved", "source": "a survey"}),
        ),
        ("WI-401: the verdict", _bound_verdict()),
        ("WI-401: re-attest SN-001", _reattest(named=False)),
        needs=needs,
    )
    _lands(root)


def test_a_refresh_merge_carrying_trunks_approvals_lands(tmp_path, monkeypatch):
    """Characterization. Trunk's owner approves SN-002 in a plain commit; the
    lane takes it in by a refresh merge. The merge claims SN-002 against its
    lane parent but not against its trunk parent, so it claims nothing.
    Adequacy witness: a rule judging a merge against its first parent alone
    would read trunk's approval as the lane's and refuse this lane."""
    root = _trunk(tmp_path, monkeypatch)
    assert integ.claim(root, "WI-401", "wi-401") == 0
    _git(root, "checkout", "-q", "wi-401")
    _write(root, "notes.txt", "lane work\n")
    _commit(root, "WI-401: lane work", when=T_CODE)
    _git(root, "checkout", "-q", "main")
    _write_needs(root, _with(BASE, "SN-002", status="Approved"))
    snap.copy_live(root)
    _commit(root, "owner: approve SN-002", when=T_CODE)
    _git(root, "checkout", "-q", "wi-401")
    _git(root, "merge", "-q", "--no-ff", "-m", "refresh: main into wi-401", "main")
    (root / "docs" / "work" / "complete").mkdir(parents=True, exist_ok=True)
    _git(
        root,
        "mv",
        "docs/work/active/wi-401/WI-401-widget.md",
        "docs/work/complete/WI-401-widget.md",
    )
    _commit(root, "close: WI-401 -> complete", when=T_LATER)
    _git(root, "checkout", "-q", "main")
    _lands(root)


def _undecodable(root):
    (root / NEEDS).write_bytes(b"\xff\xfe[need.SN-001]\n")


def _unparseable(root):
    _write(root, NEEDS, "[need.SN-001\nstatus = \n")


def _copy_unparseable(root):
    _write(root, COPY, "[need.SN-001\nstatus = \n")


@pytest.mark.parametrize(
    "write, rel",
    [(_undecodable, NEEDS), (_unparseable, NEEDS), (_copy_unparseable, COPY)],
    ids=["live undecodable", "live unparseable", "copy unparseable"],
)
def test_an_unreadable_or_unparseable_registry_or_copy_is_refused_by_name(
    tmp_path, monkeypatch, write, rel
):
    # The slot refuses each such lane at an earlier rung today; the rider,
    # run on the lane commit, names the file and the commit it was read at.
    root = _trunk(tmp_path, monkeypatch)
    _lane(root, monkeypatch, [("WI-401: break a registry", write)])
    commit = _rev(root, "wi-401~1")
    refused(root, "wi-401", "smoke")
    lines = _rider_lines(root, commit)
    assert rel in lines and commit[:10] in lines, lines


def test_an_off_spine_demotion_and_a_born_Drafted_row_land_from_a_loop_lane(
    tmp_path, monkeypatch
):
    # What loop lanes lose: a held status move that claims no approval is no
    # longer refused at the slot.
    frame = {"B-01": "Drafted", "B-02": "Approved"}
    root = _trunk(tmp_path, monkeypatch, frame=frame)

    def move(root):
        _write(
            root,
            FRAME,
            _frame_text({"B-01": "Drafted", "B-02": "Drafted", "B-03": "Drafted"}),
        )

    _lane(root, monkeypatch, [("WI-401: demote B-02, add B-03", move)], kind="loop")
    _lands(root)


# --- the hook step and the loop writers --------------------------------------------


def _stage_sn1_approval(root):
    _write_needs(root, _with(BASE, "SN-001", status="Approved"))
    snap.copy_live(root)
    _git(root, "add", "-A")


def test_an_unmarked_plain_trunk_commit_approving_a_held_row_passes(
    tmp_path, monkeypatch
):
    """Characterization: the ruled residual. A person's plain trunk commit
    is not judged where it is made. Adequacy witness: a step that judged every
    commit, marked or not, would exit 1 here."""
    root = _trunk(tmp_path, monkeypatch)
    _stage_sn1_approval(root)
    proc = run_py(STEP, cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_the_same_commit_marked_is_refused_by_the_hook_step(tmp_path, monkeypatch):
    root = _trunk(tmp_path, monkeypatch)
    _stage_sn1_approval(root)
    monkeypatch.setenv(MARK, SESSION)
    proc = run_py(STEP, cwd=root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    # The row, its rung and the dial it is held under, all named.
    for word in ("SN-001", NEEDS_RUNG, DIAL):
        assert word in proc.stdout + proc.stderr, word


def test_a_marked_held_SN_demotion_outside_a_lane_is_refused(tmp_path, monkeypatch):
    root = _trunk(tmp_path, monkeypatch, needs=APPROVED)
    _write_needs(root, BASE)
    _git(root, "add", "-A")
    monkeypatch.setenv(MARK, SESSION)
    proc = run_py(STEP, cwd=root)
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "SN-001" in proc.stdout + proc.stderr


def _flip_sn1(root):
    _write_needs(root, _with(BASE, "SN-001", status="Approved"))


def _claim_writer(root, monkeypatch, capsys):
    moves = integ.spec_move
    real_plan, real_move = moves.planned_writes, moves.move_spec

    def plan(r, pairs):
        return list(real_plan(r, pairs)) + [NEEDS]

    def move(r, src, dest, **kw):
        out = real_move(r, src, dest, **kw)
        _flip_sn1(r)  # the tree the claim is about to commit approves SN-001
        return out

    monkeypatch.setattr(moves, "planned_writes", plan)
    monkeypatch.setattr(moves, "move_spec", move)
    monkeypatch.setenv(MARK, SESSION)
    assert integ.claim(root, "WI-401", "wi-401") == 1
    return capsys.readouterr().err


def _mint_writer(root, monkeypatch, capsys):
    intake = load_script("intake")
    monkeypatch.setattr(intake.bookkeeping, "SCRIPTS", integ.bookkeeping.SCRIPTS)
    real_scope, real_draft = intake._mint_scope, intake._write_draft

    def scope(r, drafts):
        planned, refusal = real_scope(r, drafts)
        return (None, refusal) if refusal else (list(planned) + [NEEDS], None)

    def draft(r, *args, **kw):
        out = real_draft(r, *args, **kw)
        _flip_sn1(r)
        return out

    monkeypatch.setattr(intake, "_mint_scope", scope)
    monkeypatch.setattr(intake, "_write_draft", draft)
    monkeypatch.setenv(MARK, SESSION)
    minted, refusal = intake.mint_gap_rows(root, [GAP])
    assert minted == []
    return refusal


def _telemetry_writer(root, monkeypatch, capsys):
    _flip_sn1(root)
    monkeypatch.setenv(MARK, SESSION)
    return integ.ac.commit_telemetry(root, "001", "iteration log", [root / NEEDS])


@pytest.mark.parametrize(
    "writer",
    [_claim_writer, _mint_writer, _telemetry_writer],
    ids=["claim", "mint", "telemetry"],
)
def test_each_loop_writer_outside_a_lane_refuses_a_held_approval(
    tmp_path, monkeypatch, capsys, writer
):
    root = _trunk(tmp_path, monkeypatch)
    head = _rev(root, "HEAD")
    refusal = writer(root, monkeypatch, capsys)
    assert refusal, refusal
    for word in ("SN-001", NEEDS_RUNG, DIAL):
        assert word in refusal, (word, refusal)
    assert _rev(root, "HEAD") == head


def test_a_marked_commit_inside_a_lane_passes_at_commit_and_is_judged_at_landing(
    tmp_path, monkeypatch
):
    # A session in its lane approves the held frame row B-01: the hook step
    # and the handback residue writer pass it, and the slot refuses the lane.
    root = _trunk(tmp_path, monkeypatch, frame={"B-01": "Drafted", "B-02": "Approved"})
    assert integ.claim(root, "WI-401", "wi-401") == 0
    wt, err = integ.lane_worktree(root, "wi-401")
    assert err is None, err
    _write(wt, FRAME, _frame_text({"B-01": "Approved", "B-02": "Approved"}))
    _git(wt, "add", "--", FRAME)
    monkeypatch.setenv(MARK, SESSION)
    proc = run_py(STEP, cwd=wt)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    handback = load_script("handback")
    closed, refusal = handback.close_partial(root, "wi-401", "the lane stopped")
    assert refusal is None and closed, refusal
    monkeypatch.delenv(MARK, raising=False)
    landing = refused(root, "wi-401", "smoke")
    for word in ("B-01", FRAME_RUNG, DIAL):
        assert word in landing, (word, landing)


def _squash(root, monkeypatch, write, marked):
    """`write` committed on a branch cut from trunk's HEAD, then squashed
    onto trunk and staged; the loop marker set when `marked`. Returns the
    lane commit."""
    _git(root, "checkout", "-q", "-b", "lane")
    write(root)
    _commit(root, "lane: the change", when=T_CODE)
    commit = _rev(root, "HEAD")
    _git(root, "checkout", "-q", "main")
    _git(root, "merge", "--squash", "-q", "lane")
    if marked:
        monkeypatch.setenv(MARK, SESSION)
    return commit


def _born_drafted_sn3(root):
    _write_needs(root, _with(BASE, "SN-003"))


@pytest.mark.parametrize("marked", [True, False], ids=["marked", "unmarked"])
def test_a_squash_landing_is_judged_by_its_lane_commits(tmp_path, monkeypatch, marked):
    root = _trunk(tmp_path / "held", monkeypatch)
    commit = _squash(root, monkeypatch, _approve_sn1_with_its_copy, marked)
    proc = run_py(STEP, cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 1, out
    assert commit[:10] in out and "SN-001" in out, out
    # A clean lane's squash passes.
    monkeypatch.delenv(MARK, raising=False)
    clean = _trunk(tmp_path / "clean", monkeypatch)
    _squash(clean, monkeypatch, _born_drafted_sn3, marked)
    proc = run_py(STEP, cwd=clean)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_a_squash_not_admitted_is_judged_as_one_commit(tmp_path, monkeypatch):
    # The staged needs file differs from the squashed tip's, so the squash is
    # not admitted on its commits: the index is judged as one lane commit.
    root = _trunk(tmp_path, monkeypatch)
    _squash(root, monkeypatch, _approve_sn1_with_its_copy, marked=False)
    _write_needs(
        root, _with(_with(BASE, "SN-001", status="Approved"), "SN-002", need="edited")
    )
    _git(root, "add", "--", NEEDS)
    proc = run_py(STEP, cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 1, out
    assert "SN-001" in out and "rebase" in out, out


# --- the checkpoint's arms map: arms no cited test exercised -----------------------
#
# Characterizations of already-correct behaviour, each naming the wrong
# implementation it would catch (its adequacy witness).


def _parsed_need(rows, rid):
    """Need `rid` as the carrier reader parses `rows`' text, not yet committed."""
    text = _needs_text(rows)
    return spine_carrier.tier_rows_from_text(text, "SN-ID", ".toml")[rid]


def _act_commit_lines(root):
    """The lane rule's lines for the lane's last work commit (the one before
    its close)."""
    return _rider_lines(root, _rev(root, "wi-401~1"))


def _assert_named_by_rule(lines, rid, rung):
    for word in (rid, rung, DIAL):
        assert word in lines, (word, lines)


def test_a_first_draft_under_a_bound_CLARITY_verdict_is_no_exception(
    tmp_path, monkeypatch
):
    """A Drafted need flipped to Approved with its copy, under an accepted
    CLARITY verdict bound to its exact text, is refused: a first draft carries
    no signature to re-attest. Witness: an exception that admitted any claim
    whose row an accepted CLARITY binding names at its digest, without
    requiring the row approving on both sides, would admit it."""
    rows = _with(BASE, "SN-002", status="Approved")

    def act(root):
        _write_needs(root, rows)
        snap.copy_live(root)
        ids = {
            "SN-002": ar.approved_text_digest(
                NEEDS, "SN-ID", _parsed_need(rows, "SN-002")
            )
        }
        _verdict(root, "amendment", ["SN-002"], identities=ids)

    root = _trunk(tmp_path, monkeypatch)
    _lane(root, monkeypatch, [("WI-401: approve SN-002 under a CLARITY verdict", act)])
    refused(root, "wi-401", "smoke")
    _assert_named_by_rule(_act_commit_lines(root), "SN-002", NEEDS_RUNG)


def test_a_copy_unequal_to_its_live_row_is_no_exception(tmp_path, monkeypatch):
    """The act writes a copy whose approved text differs from the live row's,
    under a CLARITY verdict bound to the live row's text: refused. Witness: an
    exception that did not compare the live row with its copy at the commit
    would admit it, since the binding matches the live row."""

    def other_copy(root):
        text = _needs_text(_with(APPROVED, "SN-001", need="a text nobody judged"))
        _write(root, COPY, text)

    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: amend SN-001", _amend()),
        ("WI-401: the verdict", _bound_verdict()),
        ("WI-401: a copy of other text", other_copy),
    )
    refused(root, "wi-401", "smoke")
    _assert_named_by_rule(_act_commit_lines(root), "SN-001", NEEDS_RUNG)


def _no_verdict(root):
    _write(root, "notes.txt", "no sitting was held\n")


def _undecodable_verdict(root):
    (root / VERDICT).parent.mkdir(parents=True, exist_ok=True)
    (root / VERDICT).write_bytes(b"\xff\xfe- [CLARITY] SN-001 -> a -> a -> same\n")
    binding = ksitting.render_requested(
        "amendment",
        ("amendment",),
        "accepted",
        identities={"SN-001": _digest(root, "SN-001")},
    )
    _write(root, ksitting.requested_path(VERDICT), binding)


@pytest.mark.parametrize(
    "verdict",
    [_no_verdict, _undecodable_verdict],
    ids=["no verdict or binding", "verdict undecodable"],
)
def test_an_absent_or_unreadable_CLARITY_verdict_is_no_exception(
    tmp_path, monkeypatch, verdict
):
    """A held re-attestation with no verdict at all, or with a verdict that
    cannot be read beside a binding recording the row's digest, is refused by
    the lane rule. Witnesses: an exception reading a binding's identity cell
    without its verdict being accepted would admit the undecodable verdict;
    one reading "no candidate binding" as no objection would admit the
    absent one."""
    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: amend SN-001", _amend()),
        ("WI-401: the verdict", verdict),
        ("WI-401: re-attest SN-001", _reattest(named=False)),
    )
    refused(root, "wi-401", "smoke")
    _assert_named_by_rule(_act_commit_lines(root), "SN-001", NEEDS_RUNG)


@pytest.mark.parametrize(
    "frame, row",
    [
        ({"B-01": "Drafted", "B-02": "Approved", "B-03": "Drafted"}, "B-03"),
        ({"B-01": "Drafted"}, "B-02"),
    ],
    ids=["row added with a status", "row removed with a status"],
)
def test_a_marked_commit_adding_or_removing_a_held_status_row_is_refused(
    tmp_path, monkeypatch, frame, row
):
    """Under the loop marker outside a lane, a staged frame row added with a
    status, or removed with one, is a held status move: the hook step refuses
    it, naming the row, its rung and the dial. Witness: a status walk that
    compared only the rows both sides carry would pass it."""
    root = _trunk(tmp_path, monkeypatch, frame={"B-01": "Drafted", "B-02": "Approved"})
    _write(root, FRAME, _frame_text(frame))
    _git(root, "add", "--", FRAME)
    monkeypatch.setenv(MARK, SESSION)
    proc = run_py(STEP, cwd=root)
    out = proc.stdout + proc.stderr
    assert proc.returncode == 1, out
    _assert_named_by_rule(out, row, FRAME_RUNG)


def test_a_handback_commit_outside_a_lane_refuses_a_held_status_move(
    tmp_path, monkeypatch
):
    """The handback writers' one commit (`handback._loop_commit`), made under
    the loop marker in a worktree no lane claimed, refuses a staged held
    status move before it commits. Witness: a handback commit that skipped
    the marker arm would commit it."""
    root = _trunk(tmp_path, monkeypatch, frame={"B-01": "Drafted", "B-02": "Approved"})
    wt = tmp_path / "scratch-wt"
    _git(root, "worktree", "add", "-q", "-b", "scratch", str(wt))
    _write(wt, FRAME, _frame_text({"B-01": "Approved", "B-02": "Approved"}))
    _git(wt, "add", "--", FRAME)
    monkeypatch.setenv(MARK, SESSION)
    tip = _rev(wt, "HEAD")
    handback = load_script("handback")
    code, out = handback._loop_commit(root, wt, "close: a handback commit")
    assert code == 1, out
    _assert_named_by_rule(out, "B-01", FRAME_RUNG)
    assert _rev(wt, "HEAD") == tip  # nothing committed


@pytest.mark.parametrize(
    "cell",
    [
        "rows = SN-001\n",
        "rows = SN-001=sha256:abc\n",
        "rows = SN-001=sha256:0123456789abcdef;SN-001=sha256:0123456789abcdef\n",
    ],
    ids=["bad token", "short hex", "repeated id"],
)
def test_a_malformed_identity_cell_refuses_the_held_act_by_row(
    tmp_path, monkeypatch, cell
):
    """The act turn's derivation refuses a held CLARITY act whose binding's
    identity cell is malformed, naming the row and its committed digest.
    Witness: an act turn reading a malformed cell as no objection (owing the
    act) would owe it."""
    root = _clarity_lane(
        tmp_path,
        monkeypatch,
        ("WI-401: amend SN-001", _amend()),
        ("WI-401: the verdict", _bound_verdict(bind=False)),
    )
    _git(root, "checkout", "-q", "wi-401")
    binding = (root / ksitting.requested_path(VERDICT)).read_text(encoding="utf-8")
    _write(root, ksitting.requested_path(VERDICT), binding + cell)
    _commit(root, "WI-401: a malformed identity cell", when=T_LATER)
    acts, why = adjudicate_act.owed_acts(root, VERDICT, "HEAD")
    assert acts is None, acts
    assert "SN-001" in why and _digest(root, "SN-001") in why, why


def test_an_unparseable_act_ledger_at_the_head_is_refused_by_name(
    tmp_path, monkeypatch
):
    """A lane whose head carries an act ledger that does not parse is refused
    at the merge's approval rung, naming the ledger. Witness: a ledger reader
    taking an unparseable side for an empty one would admit the lane."""
    root = _trunk(tmp_path, monkeypatch)
    base = _rev(root, "HEAD")
    ledger = "{}/{}".format(snap.SNAPSHOT_DIR, ar.SNAPSHOT_ACTS)
    _write(root, ledger, "[[act]\nseq = \n")
    _commit(root, "an unparseable act ledger", when=T_CODE)
    head = _rev(root, "HEAD")
    refusal = ar.merge_approval_refusal(root, base, head, [], trunk=head)
    assert refusal and ar.SNAPSHOT_ACTS in refusal, refusal
    assert "does not parse" in refusal, refusal


def test_an_act_already_on_trunk_is_not_re_read(tmp_path, monkeypatch):
    """Trunk's own unbacked act (an owner's re-attestation, recorded in the
    act ledger) is in the merge base; a lane that adds one act of its own,
    backed by an accepted verdict, is admitted at the approval rung. Witness:
    a ledger reader taking the head's every entry, not only those the base
    lacks, would refuse the lane for trunk's unbacked act."""
    both = _with(APPROVED, "SN-002", status="Approved")
    root = _trunk(tmp_path, monkeypatch, needs=both)
    _write_needs(root, _with(both, "SN-001", need="the owner's own wording"))
    snap.copy_live(root, reattests=frozenset({"SN-001"}))
    _commit(root, "owner: re-attest SN-001", when=T_CODE)
    base = _rev(root, "HEAD")
    _git(root, "checkout", "-q", "-b", "lane")
    lane_rows = _with(
        _with(both, "SN-001", need="the owner's own wording"),
        "SN-002",
        need="a team adopts the kit",
    )
    _write_needs(root, lane_rows)
    _commit(root, "lane: amend SN-002", when=T_CODE)
    _verdict(root, "amendment", ["SN-002"])
    _commit(root, "lane: the verdict", when=T_CODE)
    snap.copy_live(root, reattests=frozenset({"SN-002"}))
    _commit(root, "lane: re-attest SN-002", when=T_LATER)
    head = _rev(root, "HEAD")
    assert ar.merge_approval_refusal(root, base, head, [], trunk=head) is None
