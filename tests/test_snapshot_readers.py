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


def _amendment_act(root, reattests, held=False, verdict=None):
    """Amend two approved rows, commit that as the merge base, then take the
    act re-attesting `reattests` as the head; returns (base, head). `held`
    keeps the scaffold's dial; `verdict`, when given, is the verdict file's
    text, committed with the act and named by it."""
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
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _AMENDMENT, True, trunk=head
    )
    assert refusal and "SR-002" in refusal and "OUTSIDE" in refusal, refusal
    assert "SR-001 " not in refusal, refusal


def test_a_reattestation_inside_the_amendment_scope_merges(scaffold):
    base, head = _amendment_act(scaffold, {"SR-001"})
    assert (
        AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, True, trunk=head)
        is None
    )
    # The same act claimed by a first-approval row holds no re-attestation scope.
    first = [("WI-901.md", {"brief": "first-approval", "adjudicates": ["SR-001"]})]
    refusal = AR.merge_approval_refusal(scaffold, base, head, first, True, trunk=head)
    assert refusal and "SR-001" in refusal, refusal


def test_a_held_rung_reattestation_without_a_verdict_is_refused(scaffold):
    """OI-100 gap 2 (WI-791): on a held rung an adjudication re-attests only a
    row its verdict rules CLARITY, and the act names that verdict so the act
    ledger shows it. The scaffold's dial holds every rung; an act naming no
    verdict is refused at merge, by row."""
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True)
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _AMENDMENT, True, trunk=head
    )
    assert refusal and "SR-001" in refusal and "names no verdict" in refusal, refusal


def test_a_held_rung_reattestation_its_verdict_rules_CLARITY_merges(scaffold):
    text = "- [CLARITY] SR-001 title -> same obligation\n\nVERDICT: CLARITY rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    assert (
        AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, True, trunk=head)
        is None
    )


def test_a_held_rung_reattestation_of_a_MEANING_row_is_refused(scaffold):
    """A MEANING row on a held rung is the owner's to sign, whatever the act
    names: the adjudicator recommends it and never re-attests it."""
    text = "- [MEANING] SR-001 title -> moved\n\nVERDICT: MEANING rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _AMENDMENT, True, trunk=head
    )
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
    SNAP.copy_live(scaffold, reattests=frozenset({"SR-001"}))
    head = _commit(run_git, "the lane's re-attesting act, no verdict")
    run_git("checkout", "-q", trunk_branch)
    set_process_key(scaffold, "attestation", "human_approval_through", "DevStg-Release")
    trunk = _commit(run_git, "trunk holds every rung")
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _AMENDMENT, True, trunk=trunk
    )
    assert refusal and "SR-001" in refusal and "names no verdict" in refusal, refusal
    # ...and the same act under a trunk that still releases the rung merges.
    assert (
        AR.merge_approval_refusal(scaffold, base, head, _AMENDMENT, True, trunk=base)
        is None
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
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _AMENDMENT, True, trunk=head
    )
    assert refusal and "SR-001" in refusal and "below approval" in refusal, refusal


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


def _mixed_act(root, approve_scope, amend_scope):
    """Batch B's shape (act seq 4 of this repository's ledger): one act that
    carries a Drafted row into approval AND re-attests an amended approved
    row, claimed by a first-approval row and an amendment row together."""
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
    SNAP.copy_live(root, approves={SR_REL: "WI-681"}, reattests={"SR-001"})
    head = _commit(run_git, "the one act: approve SR-002, re-attest SR-001")
    metas = [
        ("WI-680.md", {"brief": "amendment", "adjudicates": amend_scope}),
        ("WI-681.md", {"brief": "first-approval", "adjudicates": approve_scope}),
    ]
    return AR.merge_approval_refusal(root, base, head, metas, True, trunk=head)


def test_a_mixed_approval_and_reattestation_act_merges(scaffold):
    """The legitimate case stays legitimate: each half of the act inside the
    scope of the row that claims it."""
    assert _mixed_act(scaffold, ["SR-002"], ["SR-001"]) is None


def test_a_mixed_act_reattesting_outside_its_amendment_scope_is_refused(scaffold):
    refusal = _mixed_act(scaffold, ["SR-002"], ["SR-009"])
    assert refusal and "SR-001 re-attested OUTSIDE" in refusal, refusal
