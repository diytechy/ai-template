"""The acceptance record as its readers see it: the needs file's two tiers
compared with their recorded copies, a spine row missing the cells every reader
keys on, each registry's own copy stamp on the operator's surfaces, a
re-acceptance held to its amendment's scope at merge, and the snapshot's
history reader taking the needs carrier from the file.

Driven on scaffolds made by the kit's own bootstrap and on real git
repositories, so this module is registered slow (tests/conftest.py).
"""

import re
import shutil
import subprocess

import pytest
from conftest import (
    SCRIPTS,
    load_script,
    pin_autocrlf,
    run_py,
    set_process_key,
    skip_without_env_gates,
)

SNAP = load_script("baseline_snapshot")
AR = load_script("acceptance_record")
HS = load_script("held_status")
from kitlib import sitting as SITTING_MOD  # noqa: E402  (scripts/ is on the path)

NEEDS_REL = "docs/requirements/stakeholder-needs.toml"
SR_REL = "docs/requirements/system-requirements.toml"
LLR_REL = "docs/requirements/low-level-requirements.toml"
TC_REL = "docs/test/test-cases.toml"

_NEED = (
    "\n[need.SN-001]\n"
    'status = "Approved"\n'
    'need = "The operator sees every accepted need whose text moved."\n'
    'why = "An amendment nobody was shown is blessed by nobody."\n'
    'priority = "M"\n'
    'acceptance = "A moved need is shown before and after."\n'
)
_SR = (
    "\n[requirement.{rid}]\n"
    'title = "{title}"\n'
    'requirement = "The kit shall keep {title}."\n'
    'rationale = "A fixture row."\n'
    'acceptance_criteria = "The row is read."\n'
    'priority = "M"\n'
    'verification_method = "Test"\n'
    'status = "Approved"\n'
    "phase = 1\n"
)


def _append(root, rel, text):
    """Append rows to a live registry as bytes, line endings untouched."""
    with (root / rel).open("ab") as fh:
        fh.write(text.encode("utf-8"))


def _rewrite(root, rel, old, new):
    """One substring edit to a live registry, asserted to change something."""
    path = root / rel
    data = path.read_bytes()
    assert old.encode("utf-8") in data, "fixture substring not found: " + old
    path.write_bytes(data.replace(old.encode("utf-8"), new.encode("utf-8"), 1))


def _script(root, name, *args):
    """A kit script as the scaffold carries it, run the way a person runs it."""
    return run_py([root / "scripts" / name, "--root", root, *args], cwd=root)


def _git(root):
    skip_without_env_gates("git")
    git = shutil.which("git")

    def run_git(*a):
        proc = subprocess.run(
            [git, "-C", str(root), *a], capture_output=True, text=True
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        return proc.stdout.strip()

    run_git("init", "-q")
    pin_autocrlf(root)
    run_git("config", "user.email", "t@example.com")
    run_git("config", "user.name", "T")
    return run_git


def _commit(run_git, message):
    run_git("add", "-A")
    run_git("commit", "-q", "-m", message)
    return run_git("rev-parse", "--short", "HEAD")


# --- the needs file's two tiers against their recorded copies (TC-269) --------


def test_a_drifted_accepted_need_is_reported_and_briefed_with_its_diff(scaffold):
    """The comparison reports the need and the acceptance brief shows its moved
    cell before and after; a need whose text did not move is not reported.

    Implements: TC-269
    """
    root = scaffold
    _append(root, NEEDS_REL, _NEED)
    SNAP.copy_live(root, seed=True)
    assert SNAP.needs_owing(root) == []
    _rewrite(
        root,
        NEEDS_REL,
        'need = "The operator sees every accepted need whose text moved."',
        'need = "The operator sees every accepted need whose text moved, at once."',
    )
    ((rid, why, cells, _row),) = SNAP.needs_owing(root)
    assert (rid, why) == ("SN-001", "DRIFTED")
    assert [c[0] for c in cells] == ["Need"]
    proc = _script(root, "trace.py", "--accept", "modified")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    brief = proc.stdout
    assert "### SN-001 — DRIFTED" in brief, brief
    assert (
        "  - before: The operator sees every accepted need whose text moved." in brief
    )
    assert (
        "  - after: The operator sees every accepted need whose text moved, at once."
        in (brief)
    )


def test_a_drifted_need_refuses_the_snapshot_until_it_is_reaccepted(scaffold):
    """On a scaffold, through the scaffold's own `intake.py snapshot`: an act
    naming the needs registry is refused while an accepted need's text moved,
    naming the need and the cell; `--reaccepts SN-001` re-anchors it, the copy
    then equals the live file, the act ledger names it, and it owes nothing.

    Implements: TC-269
    """
    root = scaffold
    _append(root, NEEDS_REL, _NEED)
    run_git = _git(root)
    SNAP.copy_live(root, seed=True)
    _commit(run_git, "the seeding signature")
    _rewrite(
        root,
        NEEDS_REL,
        'why = "An amendment nobody was shown is blessed by nobody."',
        'why = "An amendment nobody was shown is blessed by nobody at all."',
    )
    recorded = (SNAP.snapshot_root(root) / NEEDS_REL).read_bytes()
    ref = ("--accepts", "stakeholder-needs.toml=the sitting")
    proc = _script(root, "intake.py", "snapshot", *ref)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "{} SN-001: Why".format(NEEDS_REL) in proc.stderr, proc.stderr
    assert (SNAP.snapshot_root(root) / NEEDS_REL).read_bytes() == recorded
    proc = _script(root, "intake.py", "snapshot", *ref, "--reaccepts", "SN-001")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (SNAP.snapshot_root(root) / NEEDS_REL).read_bytes() == (
        root / NEEDS_REL
    ).read_bytes()
    assert "SN-001" in SNAP.read_acts(root)[-1]["reattested"]
    assert SNAP.needs_owing(root) == []


def test_an_accepted_stakeholder_is_recorded_by_the_act_that_accepts_it(scaffold):
    """The act ledger names a stakeholder the act carried into acceptance, as it
    names every other tier's rows, so the acceptance is recorded in a typed field
    and not only in the snapshot's prose stamp.

    Implements: TC-269
    """
    root = scaffold
    _append(
        root,
        NEEDS_REL,
        '\n[stakeholder.STK-01]\nname = "The operator"\n'
        'description = "Owns the kit\'s outcomes."\nstatus = "Drafted"\n',
    )
    SNAP.copy_live(root, seed=True)
    _rewrite(root, NEEDS_REL, 'status = "Drafted"\n', 'status = "Approved"\n')
    SNAP.copy_live(root, accepts={NEEDS_REL: "the sitting"})
    last = SNAP.read_acts(root)[-1]
    assert "STK-01" in last["approved"], last


def test_the_snapshot_history_reader_takes_the_needs_carrier_from_the_file(tmp_path):
    """At a commit whose needs file is TOML declaring no need, no need is read
    (a markdown table row in a string is not one), and at a commit whose needs
    file does not parse the reader refuses, naming the commit and the file.

    Implements: TC-297
    """
    root = tmp_path / "repo"
    (root / "docs" / "requirements").mkdir(parents=True)
    run_git = _git(root)
    (root / NEEDS_REL).write_text(
        '[stakeholder.STK-01]\nname = "Owner"\ndescription = """\n'
        '| SN-005 | a need nobody declared | nobody | M | later |\n"""\n',
        encoding="utf-8",
    )
    clean = _commit(run_git, "needs declaring none")
    assert SNAP._needs_at(root, clean) == {}
    (root / NEEDS_REL).write_text(
        '[need.SN-007]\nneed = "unterminated\n', encoding="utf-8"
    )
    broken = _commit(run_git, "a needs file that does not parse")
    with pytest.raises(SystemExit, match=re.escape(broken) + ".*stakeholder-needs"):
        SNAP._needs_at(root, broken)


# --- a spine row missing the cells its readers key on (TC-270) ----------------


def test_a_row_missing_its_status_or_phase_cell_is_an_integrity_finding(scaffold):
    """Once the spine is phased, a test case with neither `status` nor `phase`,
    and a need with no `status`, each fail the integrity floor naming the row
    and the cell; the acceptance brief lists every one of them as owing an act.

    Implements: TC-270
    """
    root = scaffold
    _append(root, SR_REL, _SR.format(rid="SR-001", title="the phased row"))
    _append(
        root,
        TC_REL,
        '\n[test.TC-001]\nverifies = ["SR-001"]\nlevel = "Unit"\n'
        'method = "Run the check."\ntier = "Smoke"\n'
        'expected = "It passes."\nautomated = "No"\n'
        'evidence = "docs/test/check-one.md"\n',
    )
    _append(
        root,
        NEEDS_REL,
        _NEED.replace('status = "Approved"\n', "").replace("SN-001", "SN-002"),
    )
    # The hand-authored ids recorded first, so the missing cells are the only
    # integrity findings left to fail the run.
    assert _script(root, "trace.py", "--bump-ids").returncode == 0
    proc = _script(root, "trace.py", "--strict-integrity")
    out = proc.stdout + proc.stderr
    assert proc.returncode != 0, out
    found = sorted(re.findall(r"FINDING \(integrity\): (\S+ \S+ has no \w+ cell)", out))
    assert found == [
        "SN SN-002 has no Status cell",
        "TC TC-001 has no Phase cell",
        "TC TC-001 has no Status cell",
    ], out
    assert "integrity=3" in out, out
    proc = _script(root, "trace.py", "--accept", "modified")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    brief = proc.stdout
    assert "## SR-001 — the phased row" in brief, brief
    assert "### TC TC-001" in brief, brief
    assert "### SN-002 — no Status cell, never accepted" in brief, brief
    # With the cells written, the floor passes.
    _rewrite(
        root,
        TC_REL,
        'evidence = "docs/test/check-one.md"\n',
        'evidence = "docs/test/check-one.md"\nstatus = "Drafted"\nphase = 1\n',
    )
    _rewrite(root, NEEDS_REL, "[need.SN-002]\n", '[need.SN-002]\nstatus = "Drafted"\n')
    proc = _script(root, "trace.py", "--strict-integrity")
    assert proc.returncode == 0, proc.stdout + proc.stderr


# --- each registry's own copy on the operator's surfaces (TC-271) ---------------


def _two_copy_scaffold(root):
    """A scaffold whose record was seeded at one commit and whose test-case
    copy alone was re-written at a later one; returns both short revisions."""
    _append(root, SR_REL, _SR.format(rid="SR-001", title="the anchored row"))
    run_git = _git(root)
    SNAP.copy_live(root, seed=True)
    seeded = _commit(run_git, "the seeding signature")
    _rewrite(
        root, TC_REL, 'evidence = "docs/test/manual-smoke.md"', 'evidence = "x.md"'
    )
    SNAP.copy_live(root, accepts={TC_REL: "a later act"})
    later = _commit(run_git, "a later act copies the test-case registry")
    # The row the brief must show: an accepted requirement drifted from a copy
    # the directory-wide stamp does not name.
    _rewrite(root, SR_REL, 'title = "the anchored row"', 'title = "the moved row"')
    assert seeded != later and SNAP.stamp(root)[0] == later
    return seeded, later


def test_the_operators_brief_and_open_items_name_each_registrys_own_copy(scaffold):
    """Implements: TC-271"""
    root = scaffold
    seeded, later = _two_copy_scaffold(root)
    proc = _script(root, "trace.py", "--accept", "modified")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    brief = dict(
        re.findall(r"^_Baseline: `(\S+)` copied \S+ \((\w+)\)", proc.stdout, re.M)
    )
    assert brief[SR_REL] == seeded and brief[LLR_REL] == seeded, proc.stdout
    assert brief[TC_REL] == later, proc.stdout
    page = load_script("gen_open_items").render(root)
    shown = dict(re.findall(r"<code>(\S+)</code> — copied \S+ \((\w+)\)", page))
    assert shown[SR_REL] == seeded and shown[TC_REL] == later, page
    model = load_script("trace").reaccept_model(
        root, *(_load(root, rel, col) for rel, col in _SPINE)
    )
    (entry,) = [e for e in model if e["id"] == "SR-001"]
    assert entry["baselines"]["SR"][0] == seeded, entry
    assert entry["baselines"]["TC"][0] == later, entry


_SPINE = ((SR_REL, "SR-ID"), (LLR_REL, "LLR-ID"), (TC_REL, "TC-ID"))


def _load(root, rel, id_col):
    return load_script("spine_carrier").load(root / rel, id_col, keep_examples=False)


# --- a re-acceptance held to its amendment's scope at merge (TC-271) ---------


def _release(root):
    """Release every rung to the loop. The scaffold's shipped dial holds them
    all, and a held rung's re-acceptance by an adjudication is the separate
    rule `test_a_held_rung_reacceptance_*` pins (WI-791)."""
    set_process_key(root, "authority", "operator_accepts_through", "DevStg-Below")


_VERDICT = "docs/reviews/v.md"


# A valid machine line per sitting kind, for the adjudication verdict a lane's
# act is tied to (WI-841 round 14).
_KIND_LINES = {
    "amendment": "VERDICT: CLARITY rows=1",
    "first-acceptance": "OUTCOME: ACCEPT rows=1",
}


def _bind_branch(
    root, rows, outcome="recorded", name="000-ADJUDICATE-x.md", returned=(), tags=None
):
    """Write the adjudication verdict, and its binding recording `outcome`,
    that a route leaves in the lane before the act it authorises. `rows` maps
    each kind to the rows its section JUDGES - an amendment section rules them
    CLARITY, a first-acceptance section ACCEPT - since every row an added act
    flips or re-accepts must be judged so by a recorded verdict in the branch
    (round 16). One kind is a single-kind verdict; several, one sitting.
    `tags` maps a row id to the tags its lines carry instead, one line each
    (`["MEANING+BLESS", "CLARITY"]` tags the row two ways)."""
    kinds = tuple(k for k in ("amendment", "first-acceptance") if k in rows)
    tag = {"amendment": "CLARITY", "first-acceptance": "ACCEPT"}

    def row_tags(kind, rid):
        # A row in `returned` is ruled RETURN in the first-acceptance section.
        if tags and rid in tags:
            return tags[rid]
        return ["RETURN" if rid in returned else tag[kind]]

    def part(kind):
        lines = "".join(
            "- [{}] {} -> judged -> judged -> same\n".format(word, rid)
            for rid in rows[kind]
            for word in row_tags(kind, rid)
        )
        return "{}\n{}\n".format(lines, _KIND_LINES[kind])

    if len(kinds) == 1:
        brief, text = kinds[0], part(kinds[0])
    else:
        brief = "combined"
        text = "".join("## {}\n\n{}\n".format(k, part(k)) for k in kinds)
        text += "SITTING: JUDGED kinds={}\n".format(";".join(kinds))
    rel = "docs/reviews/lane/" + name
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text(text, encoding="utf-8")
    binding = SITTING_MOD.render_requested(brief, kinds, outcome)
    (root / SITTING_MOD.requested_path(rel)).write_text(binding, encoding="utf-8")


def _amendment_act(
    root, reaccepts, held=False, verdict=None, binding=None, judged=None, tags=None
):
    """Amend two accepted rows, commit that as the merge base, then take the
    act re-accepting `reaccepts` as the head; returns (base, head). `held`
    keeps the scaffold's dial; `verdict`, when given, is the verdict file's
    text, committed with the act and named by it, beside its `binding` - by
    default the one the route that ran the call records for an accepted
    single-kind amendment verdict (WI-841 round 11)."""
    run_git = _git(root)
    if not held:
        _release(root)
    _append(root, SR_REL, _SR.format(rid="SR-001", title="row one"))
    _append(root, SR_REL, _SR.format(rid="SR-002", title="row two"))
    SNAP.copy_live(root, seed=True)
    _commit(run_git, "seed")
    for rid in sorted(reaccepts):
        title = "row one" if rid == "SR-001" else "row two"
        _rewrite(root, SR_REL, '"{}"'.format(title), '"{}, amended"'.format(title))
    base = _commit(run_git, "the amendments")
    if verdict is not None:
        (root / _VERDICT).parent.mkdir(parents=True, exist_ok=True)
        (root / _VERDICT).write_text(verdict, encoding="utf-8")
        if binding is None:
            binding = SITTING_MOD.render_requested(
                "amendment", ("amendment",), "recorded"
            )
        (root / SITTING_MOD.requested_path(_VERDICT)).write_text(
            binding, encoding="utf-8"
        )
    if verdict is None:
        _bind_branch(root, {"amendment": sorted(judged or reaccepts)}, tags=tags)
    SNAP.copy_live(
        root,
        reaccepts=frozenset(reaccepts),
        verdict=_VERDICT if verdict is not None else None,
    )
    head = _commit(run_git, "the re-accepting act")
    return base, head


_AMENDMENT = [("WI-900.md", {"brief": "amendment", "adjudicates": ["SR-001"]})]


def test_a_reacceptance_outside_the_amendment_scope_is_refused_by_name(scaffold):
    """Implements: TC-278"""
    base, head = _amendment_act(scaffold, {"SR-001", "SR-002"})
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-002" in refusal and "OUTSIDE" in refusal, refusal
    assert "SR-001 " not in refusal, refusal


def test_a_reacceptance_inside_the_amendment_scope_merges(scaffold):
    """Implements: TC-278"""
    base, head = _amendment_act(scaffold, {"SR-001"})
    assert (
        AR.merge_acceptance_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
        is None
    )
    # The same act claimed by a first-acceptance row holds no re-acceptance scope.
    first = [("WI-901.md", {"brief": "first-acceptance", "adjudicates": ["SR-001"]})]
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, first, trunk=head)
    assert refusal and "SR-001" in refusal, refusal


def test_a_held_rung_is_read_from_trunk_not_from_the_lane(scaffold):
    """The lane rule judges a lane commit under the dial committed at the
    checkout's HEAD, which is trunk at the merge slot: a lane that forked while
    the rung was released, and whose own tree still releases it, is refused
    once trunk holds the rung. Its CLARITY verdict binds no text, so the act
    is no exception.

    Implements: TC-278
    """
    run_git = _git(scaffold)
    _release(scaffold)
    _append(scaffold, SR_REL, _SR.format(rid="SR-001", title="row one"))
    SNAP.copy_live(scaffold, seed=True)
    _commit(run_git, "seed")
    trunk_branch = run_git("rev-parse", "--abbrev-ref", "HEAD")
    _rewrite(scaffold, SR_REL, '"row one"', '"row one, amended"')
    _commit(run_git, "the amendment")
    run_git("checkout", "-q", "-b", "lane")
    _bind_branch(scaffold, {"amendment": ["SR-001"]})
    SNAP.copy_live(scaffold, reaccepts=frozenset({"SR-001"}))
    head = _commit(run_git, "the lane's re-accepting act")
    assert HS.commit_held_acceptance_lines(scaffold, head) == []
    run_git("checkout", "-q", trunk_branch)
    set_process_key(scaffold, "authority", "operator_accepts_through", "DevStg-Release")
    _commit(run_git, "trunk holds every rung")
    lines = " ".join(HS.commit_held_acceptance_lines(scaffold, head))
    assert "SR-001" in lines and "DevStg-Release" in lines, lines


# --- a released rung's MEANING re-acceptance needs the bless mark (TC-278) ---

_SCOPES = pytest.mark.parametrize("metas", [_AMENDMENT, []], ids=["scoped", "unscoped"])


@_SCOPES
def test_a_released_plain_MEANING_reacceptance_is_refused_naming_the_row_and_the_mark(
    scaffold, metas
):
    """An amendment verdict ruling a row plain MEANING says the adjudicator
    would not bless its new text, so it authorizes no re-acceptance of it,
    whether or not the lane is scoped to that amendment.

    Implements: TC-278
    """
    base, head = _amendment_act(scaffold, {"SR-001"}, tags={"SR-001": ["MEANING"]})
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head)
    assert "SR-001 (amendment) is authorized by no recorded verdict" in refusal, refusal
    assert "[MEANING+BLESS]" in refusal, refusal


@_SCOPES
def test_a_released_MEANING_BLESS_reacceptance_merges(scaffold, metas):
    """Implements: TC-278"""
    tags = {"SR-001": ["MEANING+BLESS"]}
    base, head = _amendment_act(scaffold, {"SR-001"}, tags=tags)
    assert AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head) is None


@pytest.mark.parametrize(
    "tags",
    [["MEANING+BLESS", "CLARITY"], ["MEANING+BLESS", "MEANING"]],
    ids=["bless-and-clarity", "bless-and-meaning"],
)
def test_a_released_row_tagged_two_ways_is_refused(scaffold, tags):
    """Implements: TC-278"""
    base, head = _amendment_act(scaffold, {"SR-001"}, tags={"SR-001": tags})
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001 (amendment)" in refusal, refusal


def test_a_named_verdict_ruling_the_row_plain_MEANING_is_refused_naming_the_verdict(
    scaffold,
):
    """Implements: TC-278"""
    text = "- [MEANING] SR-001 title -> moved\n\nVERDICT: MEANING rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, verdict=text)
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and _VERDICT in refusal, refusal
    assert "does not authorize SR-001" in refusal, refusal
    assert "[MEANING+BLESS]" in refusal, refusal


def test_a_named_verdict_blessing_the_row_merges(scaffold):
    """Implements: TC-278"""
    text = "- [MEANING+BLESS] SR-001 title -> moved\n\nVERDICT: MEANING rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, verdict=text)
    assert (
        AR.merge_acceptance_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
        is None
    )


# --- a retirement alone in its registry (TC-278) ------------------------------


def _retirement_act(root, held=False, judged=("SR-002",), beside=False):
    """Seed two accepted rows (the merge base), delete SR-002 from the live
    registry, rule `judged` CLARITY in an accepted amendment verdict, then
    take the act re-accepting SR-002 alone. SR-001 stays untouched, so the
    registry holds an accepted row but no other act, unless `beside` amends
    SR-001 afterwards and takes a second act re-accepting it. Returns (base,
    head, the paths the retirement act's snapshot write copied)."""
    run_git = _git(root)
    if not held:
        _release(root)
    _append(root, SR_REL, _SR.format(rid="SR-001", title="row one"))
    _append(root, SR_REL, _SR.format(rid="SR-002", title="row two"))
    SNAP.copy_live(root, seed=True)
    base = _commit(run_git, "seed")
    _rewrite(root, SR_REL, _SR.format(rid="SR-002", title="row two"), "")
    _commit(run_git, "retire SR-002")
    _bind_branch(root, {"amendment": list(judged)})
    written = SNAP.copy_live(root, reaccepts=frozenset({"SR-002"}))
    head = _commit(run_git, "the retirement act")
    if beside:
        _rewrite(root, SR_REL, '"row one"', '"row one, amended"')
        _commit(run_git, "amend SR-001")
        SNAP.copy_live(root, reaccepts=frozenset({"SR-001"}))
        head = _commit(run_git, "the re-acceptance beside the retirement")
    return base, head, written


_RETIRE = [("WI-900.md", {"brief": "amendment", "adjudicates": ["SR-002"]})]


def test_a_retirement_alone_in_its_registry_merges(scaffold):
    """A retired row's re-acceptance authorizes its own registry's copy, so
    an act whose registry carries no other act is not WIDENED, on a lane
    scoped to the amendment and on an unscoped lane alike.

    Implements: TC-278
    """
    base, head, _written = _retirement_act(scaffold)
    for metas in (_RETIRE, []):
        refusal = AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head)
        assert refusal is None, refusal


def test_the_acted_set_names_a_retired_rows_registry(scaffold):
    """The acted set places a retired row in the registry its id's tier
    names, though the head no longer holds the row.

    Implements: TC-278
    """
    base, head, written = _retirement_act(scaffold)
    assert written == ["docs/archive/last_approved/" + SR_REL], written
    acted = AR.lane_acted_set(
        scaffold, base, head, AR.acceptance_delta(scaffold, base, head)
    )[0]
    assert acted == {"accept": {}, "reaccept": {"SR-002": SR_REL}}, acted


def test_a_retirement_beside_another_act_in_its_registry_merges(scaffold):
    """A retired row's re-acceptance authorizes its registry's copy whether
    or not another act moved that registry: beside a second act re-accepting
    another row of the same registry, both ruled by the recorded verdict and
    inside the amendment scope, the merge is admitted.

    Implements: TC-278
    """
    base, head, _written = _retirement_act(
        scaffold, judged=("SR-001", "SR-002"), beside=True
    )
    acted = AR.lane_acted_set(
        scaffold, base, head, AR.acceptance_delta(scaffold, base, head)
    )[0]
    assert acted == {
        "accept": {},
        "reaccept": {"SR-001": SR_REL, "SR-002": SR_REL},
    }, acted
    both = [("WI-900.md", {"brief": "amendment", "adjudicates": ["SR-001", "SR-002"]})]
    for metas in (both, []):
        refusal = AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head)
        assert refusal is None, refusal


def test_a_lone_retirement_on_a_held_rung_is_refused_by_row(scaffold):
    # The lane rule, asked of the retirement act under the scaffold's held
    # dial: a copy retiring an accepted row is a held acceptance claim.
    _base, head, _written = _retirement_act(scaffold, held=True)
    lines = " ".join(HS.commit_held_acceptance_lines(scaffold, head))
    assert "SR-002" in lines and "held rung" in lines, lines


def test_a_retirement_outside_the_amendment_scope_is_refused(scaffold):
    """Implements: TC-278"""
    base, head, _written = _retirement_act(scaffold)
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-002 re-accepted OUTSIDE" in refusal, refusal


def test_a_retirement_no_recorded_verdict_rules_is_refused(scaffold):
    """Implements: TC-278"""
    base, head, _written = _retirement_act(scaffold, judged=("SR-001",))
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, _RETIRE, trunk=head)
    assert refusal and "no RECORDED verdict" in refusal and "SR-002" in refusal, refusal
    assert "WIDENED" not in refusal, refusal


def test_the_scripts_under_test_are_the_scaffolds_copies(scaffold):
    """The scaffold runs its own copies of the kit's scripts; a stale copy would
    make every CLI assertion above test old code."""
    for name in ("trace.py", "baseline_snapshot.py", "acceptance_record.py"):
        assert (scaffold / "scripts" / name).read_bytes() == (
            SCRIPTS / name
        ).read_bytes()


# --- the review's coverage: the legacy carrier, the stakeholder tier, every
# --- tier's missing cell and the mixed act ------------------------------------

_MD_NEEDS = (
    "# Stakeholder needs\n\n## Core needs\n\n"
    "| SN-ID | Need | Why it matters | Priority | Acceptance intent |\n"
    "|---|---|---|---|---|\n"
    "| SN-001 | The operator sees a moved need. | Unseen is unblessed. | M |"
    " Shown before and after. |\n"
)


def test_a_markdown_needs_file_is_compared_like_a_toml_one(scaffold):
    """The legacy markdown carrier is still a supported needs file: its
    accepted need is recorded, its drift reported naming the cell, an act
    copying it refused until the need is re-accepted, and nothing is reported
    unanchored while it matches its copy.

    Implements: TC-297
    """
    root = scaffold
    (root / NEEDS_REL).unlink()
    md = root / "docs" / "requirements" / "stakeholder-needs.md"
    md.write_text(_MD_NEEDS, encoding="utf-8")
    run_git = _git(root)
    SNAP.copy_live(root, seed=True)
    _commit(run_git, "the seeding signature")
    assert SNAP.needs_owing(root) == []
    assert SNAP.unanchored_findings(root) == []
    md.write_text(
        _MD_NEEDS.replace("sees a moved need", "sees every moved need"),
        encoding="utf-8",
    )
    ((rid, why, cells, _row),) = SNAP.needs_owing(root)
    assert (rid, why, [c[0] for c in cells]) == ("SN-001", "DRIFTED", ["Need"])
    ref = ("--accepts", "stakeholder-needs=the sitting")
    proc = _script(root, "intake.py", "snapshot", *ref)
    assert proc.returncode != 0 and "SN-001: Need" in proc.stderr, proc.stderr
    proc = _script(root, "intake.py", "snapshot", *ref, "--reaccepts", "SN-001")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    copy = SNAP.snapshot_root(root) / "docs" / "requirements" / "stakeholder-needs.md"
    assert copy.read_bytes() == md.read_bytes()
    assert SNAP.needs_owing(root) == []


def test_a_drifted_accepted_stakeholder_is_reported_and_briefed(scaffold):
    """The stakeholder tier drifts like the need tier beside it.

    Implements: TC-269
    """
    root = scaffold
    _append(
        root,
        NEEDS_REL,
        '\n[stakeholder.STK-01]\nname = "The operator"\n'
        'description = "Owns the outcomes."\nstatus = "Approved"\n',
    )
    SNAP.copy_live(root, seed=True)
    _rewrite(
        root,
        NEEDS_REL,
        'description = "Owns the outcomes."',
        'description = "Owns every outcome."',
    )
    ((rid, why, cells, _row),) = SNAP.needs_owing(root)
    assert (rid, why, [c[0] for c in cells]) == ("STK-01", "DRIFTED", ["Description"])
    proc = _script(root, "trace.py", "--accept", "modified")
    assert "### STK-01 — DRIFTED" in proc.stdout, proc.stdout
    assert "  - after: Owns every outcome." in proc.stdout, proc.stdout


# --- the operator's open-items page shows the needs owing an act (TC-269) --------

_EMPTY_SECTION_2 = "no SR owes an acceptance or a re-accept"


def _card(page, rid):
    """The `<article>` the open-items page renders for `rid`'s act, failing
    the test (not raising a lookup error) when the page has none."""
    found = re.search(
        r'<article class="card" id="{}-accept">.*?</article>'.format(re.escape(rid)),
        page,
        re.S,
    )
    if found is None:
        pytest.fail("no card for {} on the open-items page".format(rid))
    return found.group(0)


def _drifted_need(root):
    """One accepted need recorded, then its `need` cell moved."""
    _append(root, NEEDS_REL, _NEED)
    SNAP.copy_live(root, seed=True)
    _rewrite(
        root,
        NEEDS_REL,
        'need = "The operator sees every accepted need whose text moved."',
        'need = "The operator sees every accepted need whose text moved, at once."',
    )


def test_a_drifted_need_has_its_card_on_the_open_items_page(scaffold):
    """The page reads the same detector as the brief: a drifted need gets a
    card in the acceptance and re-acceptance section with its moved cell
    before and after, and the section no longer says nothing is owed.

    Implements: TC-269
    """
    root = scaffold
    _drifted_need(root)
    page = load_script("gen_open_items").render(root)
    card = _card(page, "SN-001")
    assert ">DRIFTED<" in card, card
    assert '<div class="cellname">Need' in card, card
    # Before and after: the unchanged run once, the moved words both ways.
    assert "The operator sees every accepted need whose text " in card, card
    assert "<del>moved.</del><ins>moved, at once.</ins>" in card, card
    assert _EMPTY_SECTION_2 not in page


def test_a_first_acceptance_need_and_stakeholder_show_their_cells_in_full(scaffold):
    """A `Drafted` need and a stakeholder with no Status cell each get a card
    showing every cell whole: a first acceptance rules on all of the row's
    text, so a cell past the page's context clip is shown to its end.

    Implements: TC-269
    """
    root = scaffold
    trace = load_script("trace")
    long_why = "x " * (trace.CELL_TRUNCATE_LIMIT // 2 + 50) + "END-OF-WHY"
    _append(
        root,
        NEEDS_REL,
        '\n[need.SN-002]\nstatus = "Drafted"\n'
        'need = "The operator reads a new need before accepting it."\n'
        'why = "{}"\npriority = "M"\n'
        'acceptance = "The need is shown in full."\n'
        '\n[stakeholder.STK-01]\nname = "The operator"\n'
        'description = "Owns the outcomes."\n'.format(long_why),
    )
    page = load_script("gen_open_items").render(root)
    need = _card(page, "SN-002")
    assert ">Drafted, never accepted<" in need, need
    assert "The operator reads a new need before accepting it." in need, need
    assert "END-OF-WHY" in need, need
    assert "more chars — read the registry row" not in need, need
    stakeholder = _card(page, "STK-01")
    assert ">no Status cell, never accepted<" in stakeholder, stakeholder
    assert "The operator" in stakeholder and "Owns the outcomes." in stakeholder
    for card in (need, stakeholder):
        assert "<del>" not in card and "<ins>" not in card, card


def test_the_open_items_counts_include_the_needs_that_owe(scaffold):
    """The page's header counts the needs owing an act, and its drifted count
    takes in a drifted need beside the drifted SR chains.

    Implements: TC-269
    """
    root = scaffold
    _drifted_need(root)
    reg = load_script("trace").load_registries(root / "docs")
    model = load_script("trace").reaccept_model(root, reg.srs, reg.llrs, reg.tcs)
    sr_drifted = sum(1 for e in model if not e["no_baseline_reason"])
    page = load_script("gen_open_items").render(root)
    assert "1 stakeholder need(s) or stakeholder(s)" in page
    assert "{} row(s) drifted".format(sr_drifted + 1) in page


def _complete(label, rid, phase=True):
    row = {label + "-ID": rid, "Status": "Approved"}
    if phase and label != "SN":
        row["Phase"] = "1"
    return row


@pytest.mark.parametrize(
    "label,cell",
    [
        ("SN", "Status"),
        ("SR", "Status"),
        ("LLR", "Status"),
        ("TC", "Status"),
        ("SR", "Phase"),
        ("LLR", "Phase"),
        ("TC", "Phase"),
    ],
)
def test_each_tiers_missing_cell_is_named(label, cell):
    """Every tier's missing Status, and every phased tier's missing Phase once
    the spine is phased, is one finding naming the row and the cell; the same
    missing Phase in an unphased spine is none.

    Implements: TC-270
    """
    spine = load_script("trace")._spine
    tiers = {t: [_complete(t, t + "-001")] for t in ("SN", "SR", "LLR", "TC")}
    broken = _complete(label, label + "-002")
    del broken[cell]
    tiers[label].append(broken)
    (found,) = spine.missing_cell_findings(tiers)
    assert found.startswith("{} {}-002 has no {} cell".format(label, label, cell))
    if cell == "Phase":
        for rows in tiers.values():
            for row in rows:
                row.pop("Phase", None)
        assert spine.missing_cell_findings(tiers) == []


def _mixed_act(root, accept_scope, amend_scope, metas=None, amend_tag="CLARITY"):
    """Batch B's shape (act seq 4 of this repository's ledger): one act that
    carries a Drafted row into acceptance AND re-accepts an amended accepted
    row, claimed by a first-acceptance row and an amendment row together, or by
    the claiming rows `metas` names (a combined sitting's one row)."""
    run_git = _git(root)
    _release(root)
    _append(root, SR_REL, _SR.format(rid="SR-001", title="row one"))
    _append(
        root,
        SR_REL,
        _SR.format(rid="SR-002", title="row two").replace(
            'status = "Approved"', 'status = "Drafted"'
        ),
    )
    SNAP.copy_live(root, seed=True)
    _commit(run_git, "seed")
    _rewrite(root, SR_REL, '"row one"', '"row one, amended"')
    base = _commit(run_git, "the amendment and the drafted row")
    _rewrite(
        root, SR_REL, 'status = "Drafted"\nphase = 1', 'status = "Approved"\nphase = 1'
    )
    _bind_branch(
        root,
        {"amendment": ["SR-001"], "first-acceptance": ["SR-002"]},
        tags={"SR-001": [amend_tag]},
    )
    SNAP.copy_live(root, accepts={SR_REL: "WI-681"}, reaccepts={"SR-001"})
    head = _commit(run_git, "the one act: accept SR-002, re-accept SR-001")
    metas = metas or [
        ("WI-680.md", {"brief": "amendment", "adjudicates": amend_scope}),
        ("WI-681.md", {"brief": "first-acceptance", "adjudicates": accept_scope}),
    ]
    return AR.merge_acceptance_refusal(root, base, head, metas, trunk=head)


def test_a_mixed_acceptance_and_reacceptance_act_merges(scaffold):
    """The legitimate case stays legitimate: each half of the act inside the
    scope of the row that claims it.

    Implements: TC-278
    """
    assert _mixed_act(scaffold, ["SR-002"], ["SR-001"]) is None


def test_a_mixed_act_reaccepting_outside_its_amendment_scope_is_refused(scaffold):
    """Implements: TC-278"""
    refusal = _mixed_act(scaffold, ["SR-002"], ["SR-009"])
    assert refusal and "SR-001 re-accepted OUTSIDE" in refusal, refusal


def test_a_combined_act_carrying_a_plain_MEANING_reacceptance_is_refused_whole(
    scaffold,
):
    """The first acceptance is backed, the re-acceptance is not: the merge
    takes nothing of the act, and names only the unauthorized row.

    Implements: TC-278
    """
    refusal = _mixed_act(scaffold, ["SR-002"], ["SR-001"], amend_tag="MEANING")
    assert refusal and "SR-001 (amendment)" in refusal, refusal
    assert "SR-002 (first-acceptance)" not in refusal, refusal
    assert "[MEANING+BLESS]" in refusal, refusal


def test_a_combined_act_with_a_blessed_reacceptance_merges(scaffold):
    """Implements: TC-278"""
    refusal = _mixed_act(scaffold, ["SR-002"], ["SR-001"], amend_tag="MEANING+BLESS")
    assert refusal is None, refusal


def _combined(tokens):
    return [("WI-682.md", {"brief": "combined", "adjudicates": tokens})]


def test_a_combined_sittings_sections_each_take_their_own_act(scaffold):
    """WI-841 round 2, MAJOR 2: one combined sitting judged a first acceptance
    and an amendment; the one act accepting SR-002 and re-accepting SR-001 is
    inside the scope each section's `<kind>:<id>` tokens give it.

    Implements: TC-278
    """
    tokens = ["first-acceptance:SR-002", "amendment:SR-001", "done-when:WI-682"]
    assert _mixed_act(scaffold, [], [], metas=_combined(tokens)) is None


def test_a_combined_sittings_act_outside_its_kinds_tokens_is_refused(scaffold):
    """The tokens bind per kind: SR-001 named for first acceptance does not
    authorise its re-acceptance.

    Implements: TC-278
    """
    tokens = ["first-acceptance:SR-002", "first-acceptance:SR-001"]
    refusal = _mixed_act(scaffold, [], [], metas=_combined(tokens))
    assert refusal and "SR-001 re-accepted OUTSIDE" in refusal, refusal


def _split_act(root, accept, copy_needs=None, sr_rel=SR_REL, append=None):
    """WI-841 round 3 (Sol r2): a combined sitting whose two sections act in
    DIFFERENT registries. SR-001 is accepted and amended (the amendment
    section re-accepts it, copying the SR registry); SN-001 is Drafted in the
    needs registry (the first-acceptance section accepts it when `accept`,
    copying the needs registry, or returns it). `copy_needs` forces the needs
    copy without a flip, the WIDENED case. `sr_rel` and `append` put the SR
    registry on another carrier (round 5: the legacy CSV). Returns
    (base, head)."""
    run_git = _git(root)
    _release(root)
    (append or _append)(root, sr_rel, _SR.format(rid="SR-001", title="row one"))
    seeded = _SPLIT_NEED.format('"Drafted"').replace("now sees", "sees")
    _append(root, NEEDS_REL, seeded)
    SNAP.copy_live(root, seed=True)
    _commit(run_git, "seed")
    _rewrite(root, sr_rel, '"row one"', '"row one, amended"')
    # The drafted need's text moves too, so its copy differs from the seed's.
    _rewrite(root, NEEDS_REL, "The operator sees", "The operator now sees")
    base = _commit(run_git, "the amendment and the drafted need")
    if accept:
        _rewrite(
            root,
            NEEDS_REL,
            _SPLIT_NEED.format('"Drafted"'),
            _SPLIT_NEED.format('"Approved"'),
        )
    accepts = {NEEDS_REL: "WI-682"} if accept or copy_needs else None
    # The first-acceptance section ACCEPTS SN-091 when the act flips it, and
    # RETURNS it otherwise (the all-return case, Sol final8 MINOR).
    _bind_branch(
        root,
        {"amendment": ["SR-001"], "first-acceptance": ["SN-091"]},
        returned=() if accept else ("SN-091",),
    )
    SNAP.copy_live(root, accepts=accepts, reaccepts={"SR-001"})
    return base, _commit(run_git, "the one act of the sitting")


# A need of its own, so the act flips exactly it (the scaffold ships others).
_SPLIT_NEED = (
    _NEED.replace("SN-001", "SN-091")
    .replace("The operator sees", "The operator now sees")
    .replace('"Approved"', "{}")
)
_SPLIT = ["amendment:SR-001", "first-acceptance:SN-091", "done-when:WI-682"]


def test_a_combined_act_in_two_registries_merges(scaffold):
    """The re-accepted SR registry's copy is the amendment section's act, not
    a widening of the first-acceptance section's.

    Implements: TC-278
    """
    base, head = _split_act(scaffold, accept=True)
    assert (
        AR.merge_acceptance_refusal(scaffold, base, head, _combined(_SPLIT), trunk=head)
        is None
    )


def test_a_combined_act_whose_first_acceptance_returned_everything_merges(scaffold):
    """The first-acceptance section returned its row and flipped nothing; the
    amendment section's re-acceptance alone is accepted, as it is for an
    amendment-only sitting (the control).

    Implements: TC-278
    """
    base, head = _split_act(scaffold, accept=False)
    lane_verdict = "docs/reviews/lane/000-ADJUDICATE-x.md"
    parsed = SITTING_MOD.recorded_at(scaffold, head, lane_verdict)
    assert parsed["first-acceptance"][3] == {"SN-091": "RETURN"}, parsed
    added = [
        a
        for a in AR._ledger_acts(scaffold, head)
        if a.get("seq") not in {x.get("seq") for x in AR._ledger_acts(scaffold, base)}
    ]
    assert [(a["approved"], a["reattested"]) for a in added] == [([], ["SR-001"])]
    assert (
        AR.merge_acceptance_refusal(scaffold, base, head, _combined(_SPLIT), trunk=head)
        is None
    )
    amendment_only = _combined(["amendment:SR-001"])
    assert (
        AR.merge_acceptance_refusal(scaffold, base, head, amendment_only, trunk=head)
        is None
    )


def test_a_combined_act_copying_a_registry_neither_section_moved_is_widened(
    scaffold,
):
    """The union is of what each section legitimately moves: a needs copy with
    no accepted need and no re-accepted need is still WIDENED.

    Implements: TC-278
    """
    base, head = _split_act(scaffold, accept=False, copy_needs=True)
    refusal = AR.merge_acceptance_refusal(
        scaffold, base, head, _combined(_SPLIT), trunk=head
    )
    assert refusal and "WIDENED" in refusal and NEEDS_REL in refusal, refusal


SR_CSV_REL = "docs/requirements/system-requirements.csv"
_SR_CSV_COLS = [
    "SR-ID",
    "Title",
    "Requirement",
    "Rationale",
    "AcceptanceCriteria",
    "Priority",
    "VerificationMethod",
    "Status",
    "Phase",
]


def _csv_sr_carrier(root):
    """Put the SR registry on the legacy CSV carrier (a supported one); return
    the appender that writes `_SR`-shaped rows into it."""
    import csv

    (root / SR_REL).unlink()
    with (root / SR_CSV_REL).open("w", newline="", encoding="utf-8") as fh:
        csv.DictWriter(fh, fieldnames=_SR_CSV_COLS, quoting=csv.QUOTE_ALL).writeheader()

    def append(root_, rel, text):
        rows = AR.spine_carrier.rows_from_text(text, "SR-ID", ".toml")
        with (root_ / rel).open("a", newline="", encoding="utf-8") as fh:
            writer = csv.DictWriter(fh, fieldnames=_SR_CSV_COLS, quoting=csv.QUOTE_ALL)
            writer.writerows(rows.values())

    return append


def test_a_combined_act_on_a_csv_carrier_authorizes_the_copy_it_writes(scaffold):
    """WI-841 round 5 (Sol r3): the re-accepted registry is named by the
    carrier the row actually sits in, so the CSV copy the act writes is the
    one it is authorized for, not the canonical TOML path.

    Implements: TC-278
    """
    append = _csv_sr_carrier(scaffold)
    base, head = _split_act(scaffold, True, sr_rel=SR_CSV_REL, append=append)
    # Named by registry identity (round 7): the CSV copy is that registry's.
    acted = AR.lane_acted_set(
        scaffold, base, head, AR.acceptance_delta(scaffold, base, head)
    )[0]
    assert set(acted["reaccept"].values()) == {SR_REL}
    refusal = AR.merge_acceptance_refusal(
        scaffold, base, head, _combined(_SPLIT), trunk=head
    )
    assert refusal is None, refusal


def test_a_combined_act_on_a_markdown_needs_carrier_authorizes_its_copy(scaffold):
    """WI-841 round 6 (Sol r4): the needs file on its supported legacy
    markdown carrier. A combined act re-accepting SN-001 (drifted, accepted)
    and accepting SR-001 (Drafted) writes the markdown copy, which is the one
    its re-acceptance is authorized for, resolved through the kit's one
    tier-carrier reader rather than a format list of this module's own.

    Implements: TC-278
    """
    root = scaffold
    run_git = _git(root)
    _release(root)
    (root / NEEDS_REL).unlink()
    md = root / "docs" / "requirements" / "stakeholder-needs.md"
    md.write_text(_MD_NEEDS, encoding="utf-8")
    _append(
        root,
        SR_REL,
        _SR.format(rid="SR-001", title="row one").replace('"Approved"', '"Drafted"'),
    )
    SNAP.copy_live(root, seed=True)
    _commit(run_git, "seed")
    md.write_text(
        _MD_NEEDS.replace("sees a moved need", "sees every moved need"),
        encoding="utf-8",
    )
    base = _commit(run_git, "the need drifts")
    _rewrite(
        root, SR_REL, 'status = "Drafted"\nphase = 1', 'status = "Approved"\nphase = 1'
    )
    _bind_branch(root, {"amendment": ["SN-001"], "first-acceptance": ["SR-001"]})
    SNAP.copy_live(root, accepts={SR_REL: "WI-683"}, reaccepts={"SN-001"})
    head = _commit(run_git, "the one act of the sitting")
    md_rel = "docs/requirements/stakeholder-needs.md"
    acted = AR.lane_acted_set(root, base, head, AR.acceptance_delta(root, base, head))[
        0
    ]
    assert set(acted["reaccept"].values()) == {NEEDS_REL}
    assert AR._registry_identity(md_rel) == NEEDS_REL
    tokens = ["amendment:SN-001", "first-acceptance:SR-001", "done-when:WI-683"]
    refusal = AR.merge_acceptance_refusal(
        root, base, head, _combined(tokens), trunk=head
    )
    assert refusal is None, refusal


_TOML_NEEDS = (
    "\n[need.SN-001]\n"
    'status = "Approved"\n'
    'need = "The operator sees every moved need."\n'
    'why = "Unseen is unblessed."\n'
    'priority = "M"\n'
    'acceptance = "Shown before and after."\n'
)
_TOML_DRAFT_NEED = (
    "\n[need.SN-002]\n"
    'status = "Drafted"\n'
    'need = "The operator sees a second need."\n'
    'why = "A second need."\n'
    'priority = "M"\n'
    'acceptance = "Shown."\n'
)


def _converted_needs(root, extra="", amend=True):
    """WI-841 round 7 (Sol r5): seed the needs file on its legacy markdown
    carrier, then commit its conversion to TOML (SN-001's text amended unless
    not `amend`, plus `extra` rows) as the merge base. Returns (run_git, base)."""
    run_git = _git(root)
    _release(root)
    (root / NEEDS_REL).unlink()
    md = root / "docs" / "requirements" / "stakeholder-needs.md"
    md.write_text(_MD_NEEDS, encoding="utf-8")
    _append(
        root,
        SR_REL,
        _SR.format(rid="SR-002", title="row two").replace('"Approved"', '"Drafted"'),
    )
    SNAP.copy_live(root, seed=True)
    _commit(run_git, "seed, the needs on markdown")
    md.unlink()
    (root / NEEDS_REL).write_text(
        (root / NEEDS_REL).read_text(encoding="utf-8")
        if (root / NEEDS_REL).is_file()
        else "",
        encoding="utf-8",
    )
    need = _TOML_NEEDS if amend else _TOML_NEEDS.replace("every moved", "a moved")
    _append(root, NEEDS_REL, need + extra)
    return run_git, _commit(run_git, "convert the needs to TOML, SN-001 amended")


def test_a_combined_act_across_a_needs_carrier_conversion_merges(scaffold):
    """Sol r5's sequence: the act re-accepts SN-001 and accepts SR-002; the
    snapshot writer writes the TOML needs copy and deletes the obsolete
    markdown one. The registry is authorized by IDENTITY, so both of its
    carrier paths are its own act, not a widening.

    Implements: TC-278
    """
    run_git, base = _converted_needs(scaffold)
    _rewrite(
        scaffold,
        SR_REL,
        'status = "Drafted"\nphase = 1',
        'status = "Approved"\nphase = 1',
    )
    _bind_branch(scaffold, {"amendment": ["SN-001"], "first-acceptance": ["SR-002"]})
    SNAP.copy_live(scaffold, accepts={SR_REL: "WI-684"}, reaccepts={"SN-001"})
    head = _commit(run_git, "the one act")
    tokens = ["amendment:SN-001", "first-acceptance:SR-002", "done-when:WI-684"]
    refusal = AR.merge_acceptance_refusal(
        scaffold, base, head, _combined(tokens), trunk=head
    )
    assert refusal is None, refusal


def test_a_plain_flip_across_a_needs_carrier_conversion_merges(scaffold):
    """The same conversion under a plain first acceptance of a need: the flip's
    registry is the needs file, whose obsolete markdown copy the act deletes.

    Implements: TC-278
    """
    run_git, base = _converted_needs(scaffold, extra=_TOML_DRAFT_NEED)
    _rewrite(
        scaffold,
        NEEDS_REL,
        'status = "Drafted"\nneed = "The operator sees a second need."',
        'status = "Approved"\nneed = "The operator sees a second need."',
    )
    _bind_branch(scaffold, {"amendment": ["SN-001"], "first-acceptance": ["SN-002"]})
    SNAP.copy_live(scaffold, accepts={NEEDS_REL: "WI-685"}, reaccepts={"SN-001"})
    head = _commit(run_git, "the one act")
    metas = [
        ("WI-685.md", {"brief": "first-acceptance", "adjudicates": ["SN-002"]}),
        ("WI-686.md", {"brief": "amendment", "adjudicates": ["SN-001"]}),
    ]
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal is None, refusal


def test_an_unauthorized_registrys_obsolete_copy_is_still_widened(scaffold):
    """Identity authorizes a registry's own carriers only: an act accepting
    SR-002 alone, after a pure (text-preserving) conversion of the needs file,
    that also copies the needs file (writing its TOML copy, deleting the
    markdown one) copies a registry it neither flipped nor re-accepted in:
    WIDENED, on both of that registry's carrier paths.

    Implements: TC-278
    """
    run_git, base = _converted_needs(scaffold, amend=False)
    _rewrite(
        scaffold,
        SR_REL,
        'status = "Drafted"\nphase = 1',
        'status = "Approved"\nphase = 1',
    )
    # `--accepts` naming the needs file copies it (TOML written, the obsolete
    # markdown deleted) although no need was flipped or re-accepted.
    _bind_branch(scaffold, {"first-acceptance": ["SR-002"]})
    SNAP.copy_live(scaffold, accepts={SR_REL: "WI-687", NEEDS_REL: "WI-687"})
    head = _commit(run_git, "the act, a first acceptance alone")
    metas = [("WI-687.md", {"brief": "first-acceptance", "adjudicates": ["SR-002"]})]
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "WIDENED to docs/requirements/stakeholder-needs" in refusal, (
        refusal
    )


_REJECTED_SITTING = (
    "## amendment\n- [CLARITY] SR-001 title -> same obligation\n"
    "VERDICT: CLARITY rows=1\n\n## done-when\nno machine line\n"
    "SITTING: JUDGED kinds=amendment;done-when\n"
)


def test_a_released_tier_act_naming_an_unrecorded_verdict_is_refused(scaffold):
    """WI-841 round 12 (Sol final4 MAJOR 2): on a RELEASED rung, a
    re-acceptance naming a verdict its route recorded FAILED (a rejected
    sitting) is refused like a held one: every act a merge adds that names a
    verdict must name an accepted one.

    Implements: TC-278
    """
    binding = SITTING_MOD.render_requested(
        "combined", ("amendment", "done-when"), "failed"
    )
    base, head = _amendment_act(
        scaffold, {"SR-001"}, verdict=_REJECTED_SITTING, binding=binding
    )
    metas = _combined(["amendment:SR-001", "done-when:WI-900"])
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "RECORDED" in refusal and _VERDICT in refusal, refusal
    # The verdict is not recorded at all, so no bless mark is involved.
    assert "[MEANING+BLESS]" not in refusal, refusal


def _rejected_mixed_act(root, name_verdict):
    """One act on a released rung that accepts SR-002 and re-accepts SR-001,
    taken after a combined `amendment;first-acceptance` sitting its route
    recorded FAILED. `name_verdict` passes `--verdict` (the named path) or
    omits it (the unnamed path, round 14). Returns (base, head)."""
    run_git = _git(root)
    _release(root)
    _append(root, SR_REL, _SR.format(rid="SR-001", title="row one"))
    drafted = _SR.format(rid="SR-002", title="row two").replace(
        '"Approved"', '"Drafted"'
    )
    _append(root, SR_REL, drafted)
    SNAP.copy_live(root, seed=True)
    _commit(run_git, "seed")
    _rewrite(root, SR_REL, '"row one"', '"row one, amended"')
    base = _commit(run_git, "the amendment, SR-002 drafted")
    # SR-002 itself, never the scaffold's SR-000 example (Sol final6 MINOR).
    _rewrite(root, SR_REL, drafted, drafted.replace('"Drafted"', '"Approved"'))
    (root / _VERDICT).parent.mkdir(parents=True, exist_ok=True)
    (root / _VERDICT).write_text(_REJECTED_SITTING, encoding="utf-8")
    failed = SITTING_MOD.render_requested(
        "combined", ("amendment", "first-acceptance"), "failed"
    )
    (root / SITTING_MOD.requested_path(_VERDICT)).write_text(failed, encoding="utf-8")
    SNAP.copy_live(
        root,
        accepts={SR_REL: "WI-901"},
        reaccepts=frozenset({"SR-001"}),
        verdict=_VERDICT if name_verdict else None,
    )
    head = _commit(run_git, "one act: accept SR-002, re-accept SR-001")
    (act,) = [
        a
        for a in AR._ledger_acts(root, head)
        if a.get("seq") not in {x.get("seq") for x in AR._ledger_acts(root, base)}
    ]
    assert act["approved"] == ["SR-002"] and act["reattested"] == ["SR-001"], act
    return base, head


def test_a_first_acceptance_in_an_act_naming_an_unrecorded_verdict_is_refused(
    scaffold,
):
    """An act may name a verdict only beside a re-acceptance (the snapshot
    tool refuses `--verdict` without `--reaccepts`), so Sol's case is one act
    accepting SR-002 and re-accepting SR-001 on a released rung, naming a
    rejected sitting its route recorded FAILED. The whole act is refused, its
    first acceptance with it.

    Implements: TC-278
    """
    base, head = _rejected_mixed_act(scaffold, name_verdict=True)
    metas = _combined(["first-acceptance:SR-002", "amendment:SR-001"])
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "RECORDED" in refusal and _VERDICT in refusal, refusal


def test_an_act_omitting_its_verdict_is_still_tied_to_a_recorded_one(scaffold):
    """Sol final6 MAJOR: the same act with `--verdict` OMITTED. Its authority
    is the adjudication the lane claims, so it must be covered by a RECORDED
    verdict of each kind it takes among the bindings the branch carries; the
    only binding here records FAILED, so the act is refused.

    Implements: TC-278
    """
    base, head = _rejected_mixed_act(scaffold, name_verdict=False)
    metas = _combined(["first-acceptance:SR-002", "amendment:SR-001"])
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "RECORDED" in refusal, refusal


def test_a_recorded_sitting_over_other_rows_does_not_authorize_this_act(scaffold):
    """Sol final7 MAJOR 1 (owner: an act's authority comes from the
    judgement of ITS rows): a failed sitting's act accepts SR-002 and
    re-accepts SR-001 without naming a verdict; a second, RECORDED sitting
    judged SR-003 and SR-004 in the same kinds. Kind coverage would pass it;
    row coverage refuses it, naming each unjudged row and its kind.

    Implements: TC-278
    """
    base, head = _rejected_mixed_act(scaffold, name_verdict=False)
    _bind_branch(
        scaffold,
        {"amendment": ["SR-003"], "first-acceptance": ["SR-004"]},
        name="001-ADJUDICATE-y.md",
    )
    head = _commit(_git(scaffold), "a recorded sitting over other rows")
    metas = _combined(["first-acceptance:SR-002", "amendment:SR-001"])
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "SR-001 (amendment)" in refusal, refusal
    assert "SR-002 (first-acceptance)" in refusal, refusal


def test_a_single_kind_verdict_over_other_rows_does_not_authorize(scaffold):
    """An accepted amendment verdict of the right kind that judged SR-002
    does not authorize re-accepting SR-001.

    Implements: TC-278
    """
    base, head = _amendment_act(scaffold, {"SR-001"}, judged=["SR-002"])
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001 (amendment)" in refusal, refusal


def test_a_named_verdict_must_judge_the_rows_it_reaccepts(scaffold):
    """A named `--verdict` that is accepted but rules a different row does
    not carry the re-acceptance of SR-001.

    Implements: TC-278
    """
    text = "- [CLARITY] SR-002 title -> same obligation\n\nVERDICT: CLARITY rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, verdict=text)
    refusal = AR.merge_acceptance_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001" in refusal and _VERDICT in refusal, refusal


def test_a_single_kind_first_acceptance_of_its_judged_row_merges(scaffold):
    """The ordinary happy path: a first-acceptance verdict ACCEPTS SR-002 and
    the act flips exactly it.

    Implements: TC-278
    """
    run_git = _git(scaffold)
    _release(scaffold)
    drafted = _SR.format(rid="SR-002", title="row two").replace(
        '"Approved"', '"Drafted"'
    )
    _append(scaffold, SR_REL, drafted)
    SNAP.copy_live(scaffold, seed=True)
    base = _commit(run_git, "seed, SR-002 drafted")
    _rewrite(scaffold, SR_REL, drafted, drafted.replace('"Drafted"', '"Approved"'))
    _bind_branch(scaffold, {"first-acceptance": ["SR-002"]})
    SNAP.copy_live(scaffold, accepts={SR_REL: "WI-902"})
    head = _commit(run_git, "the first acceptance of SR-002")
    metas = [("WI-902.md", {"brief": "first-acceptance", "adjudicates": ["SR-002"]})]
    assert AR.merge_acceptance_refusal(scaffold, base, head, metas, trunk=head) is None
