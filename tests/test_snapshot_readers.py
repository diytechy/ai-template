"""The acceptance record as its readers see it: the needs file's two tiers
compared with their recorded copies, a spine row missing the cells every reader
keys on, each registry's own copy stamp on the owner's surfaces, a
re-attestation held to its amendment's scope at merge, and the snapshot's
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
from kitlib import sitting as SITTING_MOD  # noqa: E402  (scripts/ is on the path)

NEEDS_REL = "docs/requirements/stakeholder-needs.toml"
SR_REL = "docs/requirements/system-requirements.toml"
LLR_REL = "docs/requirements/low-level-requirements.toml"
TC_REL = "docs/test/test-cases.toml"

_NEED = (
    "\n[need.SN-001]\n"
    'status = "Approved"\n'
    'need = "The owner sees every approved need whose text moved."\n'
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
    'verification = "Test"\n'
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


def test_a_drifted_approved_need_is_reported_and_briefed_with_its_diff(scaffold):
    """The comparison reports the need and the approval brief shows its moved
    cell before and after; a need whose text did not move is not reported."""
    root = scaffold
    _append(root, NEEDS_REL, _NEED)
    SNAP.copy_live(root, seed=True)
    assert SNAP.needs_owing(root) == []
    _rewrite(
        root,
        NEEDS_REL,
        'need = "The owner sees every approved need whose text moved."',
        'need = "The owner sees every approved need whose text moved, at once."',
    )
    ((rid, why, cells, _row),) = SNAP.needs_owing(root)
    assert (rid, why) == ("SN-001", "DRIFTED")
    assert [c[0] for c in cells] == ["Need"]
    proc = _script(root, "trace.py", "--approve", "modified")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    brief = proc.stdout
    assert "### SN-001 — DRIFTED" in brief, brief
    assert "  - before: The owner sees every approved need whose text moved." in brief
    assert (
        "  - after: The owner sees every approved need whose text moved, at once."
        in (brief)
    )


def test_a_drifted_need_refuses_the_snapshot_until_it_is_reattested(scaffold):
    """On a scaffold, through the scaffold's own `intake.py snapshot`: an act
    naming the needs registry is refused while an approved need's text moved,
    naming the need and the cell; `--reattests SN-001` re-anchors it, the copy
    then equals the live file, the act ledger names it, and it owes nothing."""
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
    ref = ("--approves", "stakeholder-needs.toml=the sitting")
    proc = _script(root, "intake.py", "snapshot", *ref)
    assert proc.returncode != 0, proc.stdout + proc.stderr
    assert "{} SN-001: Why".format(NEEDS_REL) in proc.stderr, proc.stderr
    assert (SNAP.snapshot_root(root) / NEEDS_REL).read_bytes() == recorded
    proc = _script(root, "intake.py", "snapshot", *ref, "--reattests", "SN-001")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (SNAP.snapshot_root(root) / NEEDS_REL).read_bytes() == (
        root / NEEDS_REL
    ).read_bytes()
    assert "SN-001" in SNAP.read_acts(root)[-1]["reattested"]
    assert SNAP.needs_owing(root) == []


def test_an_approved_stakeholder_is_recorded_by_the_act_that_approves_it(scaffold):
    """The act ledger names a stakeholder the act carried into approval, as it
    names every other tier's rows, so the approval is recorded in a typed field
    and not only in the snapshot's prose stamp."""
    root = scaffold
    _append(
        root,
        NEEDS_REL,
        '\n[stakeholder.STK-01]\nname = "The owner"\n'
        'description = "Owns the kit\'s outcomes."\nstatus = "Drafted"\n',
    )
    SNAP.copy_live(root, seed=True)
    _rewrite(root, NEEDS_REL, 'status = "Drafted"\n', 'status = "Approved"\n')
    SNAP.copy_live(root, approves={NEEDS_REL: "the sitting"})
    last = SNAP.read_acts(root)[-1]
    assert "STK-01" in last["approved"], last


def test_the_snapshot_history_reader_takes_the_needs_carrier_from_the_file(tmp_path):
    """At a commit whose needs file is TOML declaring no need, no need is read
    (a markdown table row in a string is not one), and at a commit whose needs
    file does not parse the reader refuses, naming the commit and the file."""
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
    and the cell; the approval brief lists every one of them as owing an act."""
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
    proc = _script(root, "trace.py", "--approve", "modified")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    brief = proc.stdout
    assert "## SR-001 — the phased row" in brief, brief
    assert "### TC TC-001" in brief, brief
    assert "### SN-002 — no Status cell, never approved" in brief, brief
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


# --- each registry's own copy on the owner's surfaces (TC-271) ---------------


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
    SNAP.copy_live(root, approves={TC_REL: "a later act"})
    later = _commit(run_git, "a later act copies the test-case registry")
    # The row the brief must show: an approved requirement drifted from a copy
    # the directory-wide stamp does not name.
    _rewrite(root, SR_REL, 'title = "the anchored row"', 'title = "the moved row"')
    assert seeded != later and SNAP.stamp(root)[0] == later
    return seeded, later


def test_the_owners_brief_and_open_items_name_each_registrys_own_copy(scaffold):
    root = scaffold
    seeded, later = _two_copy_scaffold(root)
    proc = _script(root, "trace.py", "--approve", "modified")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    brief = dict(
        re.findall(r"^_Baseline: `(\S+)` copied \S+ \((\w+)\)", proc.stdout, re.M)
    )
    assert brief[SR_REL] == seeded and brief[LLR_REL] == seeded, proc.stdout
    assert brief[TC_REL] == later, proc.stdout
    page = load_script("gen_open_items").render(root)
    shown = dict(re.findall(r"<code>(\S+)</code> — copied \S+ \((\w+)\)", page))
    assert shown[SR_REL] == seeded and shown[TC_REL] == later, page
    model = load_script("trace").reattest_model(
        root, *(_load(root, rel, col) for rel, col in _SPINE)
    )
    (entry,) = [e for e in model if e["id"] == "SR-001"]
    assert entry["baselines"]["SR"][0] == seeded, entry
    assert entry["baselines"]["TC"][0] == later, entry


_SPINE = ((SR_REL, "SR-ID"), (LLR_REL, "LLR-ID"), (TC_REL, "TC-ID"))


def _load(root, rel, id_col):
    return load_script("spine_carrier").load(root / rel, id_col, keep_examples=False)


# --- a re-attestation held to its amendment's scope at merge (TC-271) ---------


def _release(root):
    """Release every rung to the loop. The scaffold's shipped dial holds them
    all, and a held rung's re-attestation by an adjudication is the separate
    rule `test_a_held_rung_reattestation_*` pins (WI-791)."""
    set_process_key(root, "attestation", "human_approval_through", "DevStg-Below")


_VERDICT = "docs/reviews/v.md"


# A valid machine line per sitting kind, for the adjudication verdict a lane's
# act is tied to (WI-841 round 14).
_KIND_LINES = {
    "amendment": "VERDICT: CLARITY rows=1",
    "first-approval": "OUTCOME: APPROVE rows=1",
}


def _bind_branch(
    root, rows, outcome="accepted", name="000-ADJUDICATE-x.md", returned=()
):
    """Write the adjudication verdict, and its binding recording `outcome`,
    that a route leaves in the lane before the act it authorises. `rows` maps
    each kind to the rows its section JUDGES - an amendment section rules them
    CLARITY, a first-approval section APPROVE - since every row an added act
    flips or re-attests must be judged so by an accepted verdict in the branch
    (round 16). One kind is a single-kind verdict; several, one sitting."""
    kinds = tuple(k for k in ("amendment", "first-approval") if k in rows)
    tag = {"amendment": "CLARITY", "first-approval": "APPROVE"}

    def part(kind):
        # A row in `returned` is ruled RETURN in the first-approval section.
        lines = "".join(
            "- [{}] {} -> judged -> judged -> same\n".format(
                "RETURN" if rid in returned else tag[kind], rid
            )
            for rid in rows[kind]
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
    root, reattests, held=False, verdict=None, binding=None, judged=None
):
    """Amend two approved rows, commit that as the merge base, then take the
    act re-attesting `reattests` as the head; returns (base, head). `held`
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
    for rid in sorted(reattests):
        title = "row one" if rid == "SR-001" else "row two"
        _rewrite(root, SR_REL, '"{}"'.format(title), '"{}, amended"'.format(title))
    base = _commit(run_git, "the amendments")
    if verdict is not None:
        (root / _VERDICT).parent.mkdir(parents=True, exist_ok=True)
        (root / _VERDICT).write_text(verdict, encoding="utf-8")
        if binding is None:
            binding = SITTING_MOD.render_requested(
                "amendment", ("amendment",), "accepted"
            )
        (root / SITTING_MOD.requested_path(_VERDICT)).write_text(
            binding, encoding="utf-8"
        )
    if verdict is None:
        _bind_branch(root, {"amendment": sorted(judged or reattests)})
    SNAP.copy_live(
        root,
        reattests=frozenset(reattests),
        verdict=_VERDICT if verdict is not None else None,
    )
    head = _commit(run_git, "the re-attesting act")
    return base, head


_AMENDMENT = [("WI-900.md", {"brief": "amendment", "adjudicates": ["SR-001"]})]


def test_a_reattestation_outside_the_amendment_scope_is_refused_by_name(scaffold):
    base, head = _amendment_act(scaffold, {"SR-001", "SR-002"})
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-002" in refusal and "OUTSIDE" in refusal, refusal
    assert "SR-001 " not in refusal, refusal


def test_a_reattestation_inside_the_amendment_scope_merges(scaffold):
    base, head = _amendment_act(scaffold, {"SR-001"})
    assert (
        AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head) is None
    )
    # The same act claimed by a first-approval row holds no re-attestation scope.
    first = [("WI-901.md", {"brief": "first-approval", "adjudicates": ["SR-001"]})]
    refusal = AR.merge_approval_refusal(scaffold, base, head, first, trunk=head)
    assert refusal and "SR-001" in refusal, refusal


def test_a_held_rung_reattestation_without_a_verdict_is_refused(scaffold):
    """OI-100 gap 2 (WI-791): on a held rung an adjudication re-attests only a
    row its verdict rules CLARITY, and the act names that verdict so the act
    ledger shows it. The scaffold's dial holds every rung; an act naming no
    verdict is refused at merge, by row."""
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True)
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001" in refusal and "names no verdict" in refusal, refusal


def test_a_held_rung_reattestation_its_verdict_rules_CLARITY_merges(scaffold):
    text = "- [CLARITY] SR-001 title -> same obligation\n\nVERDICT: CLARITY rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    assert (
        AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head) is None
    )


def test_a_held_rung_reattestation_of_a_MEANING_row_is_refused(scaffold):
    """A MEANING row on a held rung is the owner's to sign, whatever the act
    names: the adjudicator recommends it and never re-attests it."""
    text = "- [MEANING] SR-001 title -> moved\n\nVERDICT: MEANING rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001" in refusal and "CLARITY" in refusal, refusal


def test_a_held_rung_is_read_from_trunk_not_from_the_merge_base(scaffold):
    """Sol review 1, MAJOR 1 (WI-791): the act lands under TRUNK's authority.
    A lane forks while the rung is released and re-attests with no verdict;
    trunk then holds the rung. The merge slot judges a branch before its
    in-slot refresh, against the old merge base, so a guard reading the merge
    base's dial would admit the act under an authority trunk has withdrawn."""
    run_git = _git(scaffold)
    _release(scaffold)
    _append(scaffold, SR_REL, _SR.format(rid="SR-001", title="row one"))
    SNAP.copy_live(scaffold, seed=True)
    _commit(run_git, "seed")
    trunk_branch = run_git("rev-parse", "--abbrev-ref", "HEAD")
    _rewrite(scaffold, SR_REL, '"row one"', '"row one, amended"')
    base = _commit(run_git, "the amendment")
    run_git("checkout", "-q", "-b", "lane")
    _bind_branch(scaffold, {"amendment": ["SR-001"]})
    SNAP.copy_live(scaffold, reattests=frozenset({"SR-001"}))
    head = _commit(run_git, "the lane's re-attesting act, no verdict")
    run_git("checkout", "-q", trunk_branch)
    set_process_key(scaffold, "attestation", "human_approval_through", "DevStg-Release")
    trunk = _commit(run_git, "trunk holds every rung")
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=trunk)
    assert refusal and "SR-001" in refusal and "names no verdict" in refusal, refusal
    # ...and the same act under a trunk that still releases the rung merges.
    assert (
        AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=base) is None
    )


def test_a_held_rung_reattestation_of_a_DRAFTED_row_is_refused(scaffold):
    """Sol review 1, MINOR 2 (WI-791; SR-228's acceptance): a CLARITY verdict
    says the owner's signature still describes the row, and a row below
    approval carries no signature to carry over, so the held-rung allowance
    never re-attests one, whatever its verdict says."""
    run_git = _git(scaffold)
    _append(
        scaffold,
        SR_REL,
        _SR.format(rid="SR-001", title="row one").replace(
            'status = "Approved"', 'status = "Drafted"'
        ),
    )
    SNAP.copy_live(scaffold, seed=True)
    _commit(run_git, "seed")
    _rewrite(scaffold, SR_REL, '"row one"', '"row one, amended"')
    base = _commit(run_git, "the amendment")
    (scaffold / _VERDICT).parent.mkdir(parents=True, exist_ok=True)
    (scaffold / _VERDICT).write_text("- [CLARITY] SR-001 title -> same\n", "utf-8")
    SNAP.copy_live(scaffold, reattests=frozenset({"SR-001"}), verdict=_VERDICT)
    head = _commit(run_git, "a held-rung act re-attesting a Drafted row")
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001" in refusal and "below approval" in refusal, refusal


def test_a_held_rung_reattestation_its_verdict_does_not_rule_is_refused(scaffold):
    """SR-228: a verdict that rules other rows and not this one is a
    non-CLARITY verdict for it, so the held-rung act is refused by row."""
    text = "- [CLARITY] SR-002 title -> same obligation\n\nVERDICT: CLARITY rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001 is not ruled CLARITY" in refusal, refusal


def test_a_held_rung_reattestation_whose_verdict_is_unreadable_is_refused(scaffold):
    """SR-228: an act naming a verdict its own head does not carry has no
    readable ruling, so the held-rung act is refused by row."""
    text = "- [CLARITY] SR-001 title -> same obligation\n\nVERDICT: CLARITY rows=1\n"
    base, _head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    run_git = _git(scaffold)
    run_git("rm", "-q", _VERDICT)
    head = _commit(run_git, "the named verdict leaves the head")
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001 is not ruled CLARITY" in refusal, refusal


def test_a_held_rung_row_ruled_both_ways_reads_MEANING_and_is_refused(scaffold):
    """LLR-278: a verdict tagging one row both CLARITY and MEANING rules it
    MEANING, whichever tag comes first, so the held-rung act is refused."""
    for order in (("CLARITY", "MEANING"), ("MEANING", "CLARITY")):
        text = "".join("- [{}] SR-001 title -> ruled\n".format(w) for w in order)
        assert AR.verdict_rulings(text) == {"SR-001": "MEANING"}, order
    text = "- [MEANING] SR-001 a -> b\n- [CLARITY] SR-001 c -> d\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001 is not ruled CLARITY" in refusal, refusal


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
    "| SN-001 | The owner sees a moved need. | Unseen is unblessed. | M |"
    " Shown before and after. |\n"
)


def test_a_markdown_needs_file_is_compared_like_a_toml_one(scaffold):
    """The legacy markdown carrier is still a supported needs file: its
    approved need is recorded, its drift reported naming the cell, an act
    copying it refused until the need is re-attested, and nothing is reported
    unanchored while it matches its copy."""
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
    ref = ("--approves", "stakeholder-needs=the sitting")
    proc = _script(root, "intake.py", "snapshot", *ref)
    assert proc.returncode != 0 and "SN-001: Need" in proc.stderr, proc.stderr
    proc = _script(root, "intake.py", "snapshot", *ref, "--reattests", "SN-001")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    copy = SNAP.snapshot_root(root) / "docs" / "requirements" / "stakeholder-needs.md"
    assert copy.read_bytes() == md.read_bytes()
    assert SNAP.needs_owing(root) == []


def test_a_drifted_approved_stakeholder_is_reported_and_briefed(scaffold):
    """The stakeholder tier drifts like the need tier beside it."""
    root = scaffold
    _append(
        root,
        NEEDS_REL,
        '\n[stakeholder.STK-01]\nname = "The owner"\n'
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
    proc = _script(root, "trace.py", "--approve", "modified")
    assert "### STK-01 — DRIFTED" in proc.stdout, proc.stdout
    assert "  - after: Owns every outcome." in proc.stdout, proc.stdout


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
    missing Phase in an unphased spine is none."""
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


def _mixed_act(root, approve_scope, amend_scope, metas=None):
    """Batch B's shape (act seq 4 of this repository's ledger): one act that
    carries a Drafted row into approval AND re-attests an amended approved
    row, claimed by a first-approval row and an amendment row together, or by
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
    _bind_branch(root, {"amendment": ["SR-001"], "first-approval": ["SR-002"]})
    SNAP.copy_live(root, approves={SR_REL: "WI-681"}, reattests={"SR-001"})
    head = _commit(run_git, "the one act: approve SR-002, re-attest SR-001")
    metas = metas or [
        ("WI-680.md", {"brief": "amendment", "adjudicates": amend_scope}),
        ("WI-681.md", {"brief": "first-approval", "adjudicates": approve_scope}),
    ]
    return AR.merge_approval_refusal(root, base, head, metas, trunk=head)


def test_a_mixed_approval_and_reattestation_act_merges(scaffold):
    """The legitimate case stays legitimate: each half of the act inside the
    scope of the row that claims it."""
    assert _mixed_act(scaffold, ["SR-002"], ["SR-001"]) is None


def test_a_mixed_act_reattesting_outside_its_amendment_scope_is_refused(scaffold):
    refusal = _mixed_act(scaffold, ["SR-002"], ["SR-009"])
    assert refusal and "SR-001 re-attested OUTSIDE" in refusal, refusal


def _combined(tokens):
    return [("WI-682.md", {"brief": "combined", "adjudicates": tokens})]


def test_a_combined_sittings_sections_each_take_their_own_act(scaffold):
    """WI-841 round 2, MAJOR 2: one combined sitting judged a first approval
    and an amendment; the one act approving SR-002 and re-attesting SR-001 is
    inside the scope each section's `<kind>:<id>` tokens give it."""
    tokens = ["first-approval:SR-002", "amendment:SR-001", "done-when:WI-682"]
    assert _mixed_act(scaffold, [], [], metas=_combined(tokens)) is None


def test_a_combined_sittings_act_outside_its_kinds_tokens_is_refused(scaffold):
    """The tokens bind per kind: SR-001 named for first approval does not
    authorise its re-attestation."""
    tokens = ["first-approval:SR-002", "first-approval:SR-001"]
    refusal = _mixed_act(scaffold, [], [], metas=_combined(tokens))
    assert refusal and "SR-001 re-attested OUTSIDE" in refusal, refusal


def _split_act(root, approve, copy_needs=None, sr_rel=SR_REL, append=None):
    """WI-841 round 3 (Sol r2): a combined sitting whose two sections act in
    DIFFERENT registries. SR-001 is approved and amended (the amendment
    section re-attests it, copying the SR registry); SN-001 is Drafted in the
    needs registry (the first-approval section approves it when `approve`,
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
    _rewrite(root, NEEDS_REL, "The owner sees", "The owner now sees")
    base = _commit(run_git, "the amendment and the drafted need")
    if approve:
        _rewrite(
            root,
            NEEDS_REL,
            _SPLIT_NEED.format('"Drafted"'),
            _SPLIT_NEED.format('"Approved"'),
        )
    approves = {NEEDS_REL: "WI-682"} if approve or copy_needs else None
    # The first-approval section APPROVES SN-091 when the act flips it, and
    # RETURNS it otherwise (the all-return case, Sol final8 MINOR).
    _bind_branch(
        root,
        {"amendment": ["SR-001"], "first-approval": ["SN-091"]},
        returned=() if approve else ("SN-091",),
    )
    SNAP.copy_live(root, approves=approves, reattests={"SR-001"})
    return base, _commit(run_git, "the one act of the sitting")


# A need of its own, so the act flips exactly it (the scaffold ships others).
_SPLIT_NEED = (
    _NEED.replace("SN-001", "SN-091")
    .replace("The owner sees", "The owner now sees")
    .replace('"Approved"', "{}")
)
_SPLIT = ["amendment:SR-001", "first-approval:SN-091", "done-when:WI-682"]


def test_a_combined_act_in_two_registries_merges(scaffold):
    """The re-attested SR registry's copy is the amendment section's act, not
    a widening of the first-approval section's."""
    base, head = _split_act(scaffold, approve=True)
    assert (
        AR.merge_approval_refusal(scaffold, base, head, _combined(_SPLIT), trunk=head)
        is None
    )


def test_a_combined_act_whose_first_approval_returned_everything_merges(scaffold):
    """The first-approval section returned its row and flipped nothing; the
    amendment section's re-attestation alone is accepted, as it is for an
    amendment-only sitting (the control)."""
    base, head = _split_act(scaffold, approve=False)
    lane_verdict = "docs/reviews/lane/000-ADJUDICATE-x.md"
    parsed = SITTING_MOD.accepted_at(scaffold, head, lane_verdict)
    assert parsed["first-approval"][3] == {"SN-091": "RETURN"}, parsed
    added = [
        a
        for a in AR._ledger_acts(scaffold, head)
        if a.get("seq") not in {x.get("seq") for x in AR._ledger_acts(scaffold, base)}
    ]
    assert [(a["approved"], a["reattested"]) for a in added] == [([], ["SR-001"])]
    assert (
        AR.merge_approval_refusal(scaffold, base, head, _combined(_SPLIT), trunk=head)
        is None
    )
    amendment_only = _combined(["amendment:SR-001"])
    assert (
        AR.merge_approval_refusal(scaffold, base, head, amendment_only, trunk=head)
        is None
    )


def test_a_combined_act_copying_a_registry_neither_section_moved_is_widened(
    scaffold,
):
    """The union is of what each section legitimately moves: a needs copy with
    no approved need and no re-attested need is still WIDENED."""
    base, head = _split_act(scaffold, approve=False, copy_needs=True)
    refusal = AR.merge_approval_refusal(
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
    "Verification",
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
    """WI-841 round 5 (Sol r3): the re-attested registry is named by the
    carrier the row actually sits in, so the CSV copy the act writes is the
    one it is authorized for, not the canonical TOML path."""
    append = _csv_sr_carrier(scaffold)
    base, head = _split_act(scaffold, True, sr_rel=SR_CSV_REL, append=append)
    # Named by registry identity (round 7): the CSV copy is that registry's.
    acted = AR.lane_acted_set(
        scaffold, base, head, AR.approval_delta(scaffold, base, head)
    )[0]
    assert set(acted["reattest"].values()) == {SR_REL}
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _combined(_SPLIT), trunk=head
    )
    assert refusal is None, refusal


def test_a_combined_act_on_a_markdown_needs_carrier_authorizes_its_copy(scaffold):
    """WI-841 round 6 (Sol r4): the needs file on its supported legacy
    markdown carrier. A combined act re-attesting SN-001 (drifted, approved)
    and approving SR-001 (Drafted) writes the markdown copy, which is the one
    its re-attestation is authorized for, resolved through the kit's one
    tier-carrier reader rather than a format list of this module's own."""
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
    _bind_branch(root, {"amendment": ["SN-001"], "first-approval": ["SR-001"]})
    SNAP.copy_live(root, approves={SR_REL: "WI-683"}, reattests={"SN-001"})
    head = _commit(run_git, "the one act of the sitting")
    md_rel = "docs/requirements/stakeholder-needs.md"
    acted = AR.lane_acted_set(root, base, head, AR.approval_delta(root, base, head))[0]
    assert set(acted["reattest"].values()) == {NEEDS_REL}
    assert AR._registry_identity(md_rel) == NEEDS_REL
    tokens = ["amendment:SN-001", "first-approval:SR-001", "done-when:WI-683"]
    refusal = AR.merge_approval_refusal(root, base, head, _combined(tokens), trunk=head)
    assert refusal is None, refusal


_TOML_NEEDS = (
    "\n[need.SN-001]\n"
    'status = "Approved"\n'
    'need = "The owner sees every moved need."\n'
    'why = "Unseen is unblessed."\n'
    'priority = "M"\n'
    'acceptance = "Shown before and after."\n'
)
_TOML_DRAFT_NEED = (
    "\n[need.SN-002]\n"
    'status = "Drafted"\n'
    'need = "The owner sees a second need."\n'
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
    """Sol r5's sequence: the act re-attests SN-001 and approves SR-002; the
    snapshot writer writes the TOML needs copy and deletes the obsolete
    markdown one. The registry is authorized by IDENTITY, so both of its
    carrier paths are its own act, not a widening."""
    run_git, base = _converted_needs(scaffold)
    _rewrite(
        scaffold,
        SR_REL,
        'status = "Drafted"\nphase = 1',
        'status = "Approved"\nphase = 1',
    )
    _bind_branch(scaffold, {"amendment": ["SN-001"], "first-approval": ["SR-002"]})
    SNAP.copy_live(scaffold, approves={SR_REL: "WI-684"}, reattests={"SN-001"})
    head = _commit(run_git, "the one act")
    tokens = ["amendment:SN-001", "first-approval:SR-002", "done-when:WI-684"]
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _combined(tokens), trunk=head
    )
    assert refusal is None, refusal


def test_a_plain_flip_across_a_needs_carrier_conversion_merges(scaffold):
    """The same conversion under a plain first approval of a need: the flip's
    registry is the needs file, whose obsolete markdown copy the act deletes."""
    run_git, base = _converted_needs(scaffold, extra=_TOML_DRAFT_NEED)
    _rewrite(
        scaffold,
        NEEDS_REL,
        'status = "Drafted"\nneed = "The owner sees a second need."',
        'status = "Approved"\nneed = "The owner sees a second need."',
    )
    _bind_branch(scaffold, {"amendment": ["SN-001"], "first-approval": ["SN-002"]})
    SNAP.copy_live(scaffold, approves={NEEDS_REL: "WI-685"}, reattests={"SN-001"})
    head = _commit(run_git, "the one act")
    metas = [
        ("WI-685.md", {"brief": "first-approval", "adjudicates": ["SN-002"]}),
        ("WI-686.md", {"brief": "amendment", "adjudicates": ["SN-001"]}),
    ]
    refusal = AR.merge_approval_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal is None, refusal


def test_an_unauthorized_registrys_obsolete_copy_is_still_widened(scaffold):
    """Identity authorizes a registry's own carriers only: an act approving
    SR-002 alone, after a pure (text-preserving) conversion of the needs file,
    that also copies the needs file (writing its TOML copy, deleting the
    markdown one) copies a registry it neither flipped nor re-attested in:
    WIDENED, on both of that registry's carrier paths."""
    run_git, base = _converted_needs(scaffold, amend=False)
    _rewrite(
        scaffold,
        SR_REL,
        'status = "Drafted"\nphase = 1',
        'status = "Approved"\nphase = 1',
    )
    # `--approves` naming the needs file copies it (TOML written, the obsolete
    # markdown deleted) although no need was flipped or re-attested.
    _bind_branch(scaffold, {"first-approval": ["SR-002"]})
    SNAP.copy_live(scaffold, approves={SR_REL: "WI-687", NEEDS_REL: "WI-687"})
    head = _commit(run_git, "the act, a first approval alone")
    metas = [("WI-687.md", {"brief": "first-approval", "adjudicates": ["SR-002"]})]
    refusal = AR.merge_approval_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "WIDENED to docs/requirements/stakeholder-needs" in refusal, (
        refusal
    )


def test_a_rejected_bound_sitting_cannot_carry_a_held_rung_reattestation(scaffold):
    """WI-841 round 11 (Sol final3 MAJOR 1): a bound, accepted
    `amendment;done-when` sitting whose done-when section has no machine line
    is not a valid verdict, so its amendment section's CLARITY ruling carries
    no held-rung re-attestation: the integrator refuses the act."""
    text = (
        "## amendment\n- [CLARITY] SR-001 title -> same obligation\n"
        "VERDICT: CLARITY rows=1\n\n## done-when\nno machine line\n"
        "SITTING: JUDGED kinds=amendment;done-when\n"
    )
    binding = SITTING_MOD.render_requested(
        "combined", ("amendment", "done-when"), "accepted"
    )
    base, head = _amendment_act(
        scaffold, {"SR-001"}, held=True, verdict=text, binding=binding
    )
    metas = _combined(["amendment:SR-001", "done-when:WI-900"])
    refusal = AR.merge_approval_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "SR-001" in refusal, refusal


_REJECTED_SITTING = (
    "## amendment\n- [CLARITY] SR-001 title -> same obligation\n"
    "VERDICT: CLARITY rows=1\n\n## done-when\nno machine line\n"
    "SITTING: JUDGED kinds=amendment;done-when\n"
)


def test_a_released_tier_act_naming_an_unaccepted_verdict_is_refused(scaffold):
    """WI-841 round 12 (Sol final4 MAJOR 2): on a RELEASED rung, a
    re-attestation naming a verdict its route recorded FAILED (a rejected
    sitting) is refused like a held one: every act a merge adds that names a
    verdict must name an accepted one."""
    binding = SITTING_MOD.render_requested(
        "combined", ("amendment", "done-when"), "failed"
    )
    base, head = _amendment_act(
        scaffold, {"SR-001"}, verdict=_REJECTED_SITTING, binding=binding
    )
    metas = _combined(["amendment:SR-001", "done-when:WI-900"])
    refusal = AR.merge_approval_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "ACCEPTED" in refusal and _VERDICT in refusal, refusal


def _rejected_mixed_act(root, name_verdict):
    """One act on a released rung that approves SR-002 and re-attests SR-001,
    taken after a combined `amendment;first-approval` sitting its route
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
        "combined", ("amendment", "first-approval"), "failed"
    )
    (root / SITTING_MOD.requested_path(_VERDICT)).write_text(failed, encoding="utf-8")
    SNAP.copy_live(
        root,
        approves={SR_REL: "WI-901"},
        reattests=frozenset({"SR-001"}),
        verdict=_VERDICT if name_verdict else None,
    )
    head = _commit(run_git, "one act: approve SR-002, re-attest SR-001")
    (act,) = [
        a
        for a in AR._ledger_acts(root, head)
        if a.get("seq") not in {x.get("seq") for x in AR._ledger_acts(root, base)}
    ]
    assert act["approved"] == ["SR-002"] and act["reattested"] == ["SR-001"], act
    return base, head


def test_a_first_approval_in_an_act_naming_an_unaccepted_verdict_is_refused(
    scaffold,
):
    """An act may name a verdict only beside a re-attestation (the snapshot
    tool refuses `--verdict` without `--reattests`), so Sol's case is one act
    approving SR-002 and re-attesting SR-001 on a released rung, naming a
    rejected sitting its route recorded FAILED. The whole act is refused, its
    first approval with it."""
    base, head = _rejected_mixed_act(scaffold, name_verdict=True)
    metas = _combined(["first-approval:SR-002", "amendment:SR-001"])
    refusal = AR.merge_approval_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "ACCEPTED" in refusal and _VERDICT in refusal, refusal


def test_an_act_omitting_its_verdict_is_still_tied_to_an_accepted_one(scaffold):
    """Sol final6 MAJOR: the same act with `--verdict` OMITTED. Its authority
    is the adjudication the lane claims, so it must be covered by an ACCEPTED
    verdict of each kind it takes among the bindings the branch carries; the
    only binding here records FAILED, so the act is refused."""
    base, head = _rejected_mixed_act(scaffold, name_verdict=False)
    metas = _combined(["first-approval:SR-002", "amendment:SR-001"])
    refusal = AR.merge_approval_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "ACCEPTED" in refusal, refusal


def test_an_accepted_sitting_over_other_rows_does_not_authorize_this_act(scaffold):
    """Sol final7 MAJOR 1 (owner: an act's authority comes from the
    judgement of ITS rows): a failed sitting's act approves SR-002 and
    re-attests SR-001 without naming a verdict; a second, ACCEPTED sitting
    judged SR-003 and SR-004 in the same kinds. Kind coverage would pass it;
    row coverage refuses it, naming each unjudged row and its kind."""
    base, head = _rejected_mixed_act(scaffold, name_verdict=False)
    _bind_branch(
        scaffold,
        {"amendment": ["SR-003"], "first-approval": ["SR-004"]},
        name="001-ADJUDICATE-y.md",
    )
    head = _commit(_git(scaffold), "an accepted sitting over other rows")
    metas = _combined(["first-approval:SR-002", "amendment:SR-001"])
    refusal = AR.merge_approval_refusal(scaffold, base, head, metas, trunk=head)
    assert refusal and "SR-001 (amendment)" in refusal, refusal
    assert "SR-002 (first-approval)" in refusal, refusal


def test_a_single_kind_verdict_over_other_rows_does_not_authorize(scaffold):
    """An accepted amendment verdict of the right kind that judged SR-002
    does not authorize re-attesting SR-001."""
    base, head = _amendment_act(scaffold, {"SR-001"}, judged=["SR-002"])
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001 (amendment)" in refusal, refusal


def test_a_named_verdict_must_judge_the_rows_it_reattests(scaffold):
    """A named `--verdict` that is accepted but rules a different row does
    not carry the re-attestation of SR-001."""
    text = "- [CLARITY] SR-002 title -> same obligation\n\nVERDICT: CLARITY rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, verdict=text)
    refusal = AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, trunk=head)
    assert refusal and "SR-001" in refusal and _VERDICT in refusal, refusal


def test_a_single_kind_first_approval_of_its_judged_row_merges(scaffold):
    """The ordinary happy path: a first-approval verdict APPROVES SR-002 and
    the act flips exactly it."""
    run_git = _git(scaffold)
    _release(scaffold)
    drafted = _SR.format(rid="SR-002", title="row two").replace(
        '"Approved"', '"Drafted"'
    )
    _append(scaffold, SR_REL, drafted)
    SNAP.copy_live(scaffold, seed=True)
    base = _commit(run_git, "seed, SR-002 drafted")
    _rewrite(scaffold, SR_REL, drafted, drafted.replace('"Drafted"', '"Approved"'))
    _bind_branch(scaffold, {"first-approval": ["SR-002"]})
    SNAP.copy_live(scaffold, approves={SR_REL: "WI-902"})
    head = _commit(run_git, "the first approval of SR-002")
    metas = [("WI-902.md", {"brief": "first-approval", "adjudicates": ["SR-002"]})]
    assert AR.merge_approval_refusal(scaffold, base, head, metas, trunk=head) is None
