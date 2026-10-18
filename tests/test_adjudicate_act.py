"""The act a committed verdict authorizes, and the bless mark it reads (WI-912).

A sitting ends at its committed verdict; its act is a later adjudicator turn
taken from that verdict (revision 32 of the review-churn plan, Q1). These
tests pin the two pieces that turn reads: the amendment verdict's bless mark
(`kitlib.verdict.blessed_rows`, Q2) and the act assembler
(`scripts/adjudicate_act.py`), which derives from the verdict and the lane's
committed tree every act still owed, refuses every input that authorizes none,
and never returns a partial brief.

Each fixture is a real git repository: the derivation reads the verdict, its
binding, the registries, their recorded copies and the dial at a revision, so
an in-memory fake would test a reader the module does not have.
"""

import shlex
import shutil
import subprocess

import pytest
from conftest import env_gate_skipif, load_script, pin_autocrlf, set_process_key

act = load_script("adjudicate_act")
baseline_snapshot = load_script("baseline_snapshot")
from kitlib import sitting as ksitting  # noqa: E402  (scripts/ is on the path)
from kitlib import verdict as kverdict  # noqa: E402

pytestmark = env_gate_skipif("git")

VERDICT = "docs/reviews/wi-301/001-ADJUDICATE-abc1234.md"
WI = "WI-301"
SRS = "docs/requirements/system-requirements.csv"
LLRS = "docs/requirements/low-level-requirements.csv"
TCS = "docs/test/test-cases.csv"
LLR_REL = "docs/requirements/low-level-requirements.toml"
TC_REL = "docs/test/test-cases.toml"

SPINE_SRS = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Priority,"
    "Verification,Status,Phase,Area\n"
    "SR-001,Adds,SN-001,The system shall add two numbers.,arithmetic is the "
    "demo,the sum is right,Must,Test,Approved,P1,core\n"
)
SPINE_LLRS = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component,Phase\n"
    "LLR-001,SR-001,add impl,src/demo.py,add,add() returns a + b.,TC-001,"
    "Approved,,P1\n"
)
SPINE_TCS = (
    "TC-ID,Verifies,Level,Method,Tier,Expected,Automated,Evidence,Status,Phase\n"
    'TC-001,LLR-001,unit,run pytest,fast,"add(2, 2) == 4",yes,'
    "tests/test_demo.py::test_add,Approved,P1\n"
)
NEW_LLR = (
    "LLR-002,SR-001,sub impl,src/demo.py,sub,sub() returns a - b.,TC-002,Drafted,,P1\n"
)
NEW_TC = (
    'TC-002,LLR-002,unit,run pytest,fast,"sub(4, 2) == 2",yes,'
    "tests/test_demo.py::test_sub,Drafted,P1\n"
)


def _git(repo, *args):
    proc = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _write(repo, rel, text):
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def _append(repo, rel, text):
    _write(repo, rel, (repo / rel).read_text(encoding="utf-8") + text)


def _replace(repo, rel, old, new):
    text = (repo / rel).read_text(encoding="utf-8")
    assert old in text, old
    _write(repo, rel, text.replace(old, new))


def _commit(repo, message):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)


def _repo(tmp_path, dial="DevStg-Needs"):
    """A spine of three Approved rows, its recorded copy seeded, and a dial
    that releases (by default) every spine rung, all committed."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    pin_autocrlf(repo)
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _write(repo, ".gitignore", "out/\n")
    _write(repo, SRS, SPINE_SRS)
    _write(repo, LLRS, SPINE_LLRS)
    _write(repo, TCS, SPINE_TCS)
    set_process_key(repo, "attestation", "human_approval_through", dial)
    baseline_snapshot.copy_live(repo, seed=True)
    _commit(repo, "seed the spine and its record")
    return repo


def _amend(repo):
    """Move the approved text of SR-001 and LLR-001, Status left put."""
    _replace(repo, SRS, "add two numbers.", "add two integers.")
    _replace(repo, LLRS, "add() returns a + b.", "add() returns the sum a + b.")
    _commit(repo, "amend SR-001 and LLR-001")


def _draft(repo):
    """Add a Drafted LLR and a Drafted TC under the approved SR."""
    _append(repo, LLRS, NEW_LLR)
    _append(repo, TCS, NEW_TC)
    _commit(repo, "draft LLR-002 and TC-002")


def _verdict(repo, text, brief, kinds=None, outcome="accepted", commit=True):
    """The verdict and the binding a route writes beside it."""
    _write(repo, VERDICT, text)
    binding = ksitting.render_requested(brief, kinds or (brief,), outcome)
    _write(repo, ksitting.requested_path(VERDICT), binding)
    if commit:
        _commit(repo, "the verdict\n\nWI: {}".format(WI))


AMENDMENT_CLARITY = (
    "- [CLARITY] SR-001 Requirement -> add -> add -> same\n\nVERDICT: CLARITY rows=1\n"
)
FIRST_APPROVAL_MIXED = (
    "- [APPROVE] LLR-002 -> sub -> chain holds -> ready\n"
    "- [RETURN] TC-002 -> sub -> no evidence -> not ready\n\n"
    "OUTCOME: RETURN rows=2\n"
)
COMBINED = (
    "## amendment\n\n"
    "- [CLARITY] SR-001 Requirement -> add -> add -> same\n\n"
    "VERDICT: CLARITY rows=1\n\n"
    "## first-approval\n\n"
    "- [APPROVE] LLR-002 -> sub -> chain holds -> ready\n\n"
    "OUTCOME: APPROVE rows=1\n\n"
    "SITTING: JUDGED kinds=amendment;first-approval\n"
)
COMBINED_KINDS = ("amendment", "first-approval")


def _take_amendment_act(repo, ids):
    baseline_snapshot.copy_live(repo, reattests=frozenset(ids))
    _commit(repo, "re-attest {}\n\nWI: {}".format(",".join(ids), WI))


def _take_approval_act(repo, ids, registries):
    for rid in ids:
        rel = LLRS if rid.startswith("LLR") else TCS
        text = (repo / rel).read_text(encoding="utf-8")
        line = next(ln for ln in text.splitlines() if ln.startswith(rid + ","))
        _replace(repo, rel, line, line.replace(",Drafted,", ",Approved,"))
    baseline_snapshot.copy_live(
        repo, approves=baseline_snapshot.parse_approves(registries)
    )
    _commit(repo, "approve {}\n\nWI: {}".format(",".join(ids), WI))


# --- the bless mark (Q2) ---------------------------------------------------


def test_a_MEANING_BLESS_row_reads_MEANING_and_blessed():
    text = "- [MEANING+BLESS] SR-001 Requirement -> a -> b -> differs\n"
    assert kverdict.row_rulings(text, "amendment") == {"SR-001": "MEANING"}
    assert kverdict.verdict_rulings(text) == {"SR-001": "MEANING"}
    assert kverdict.blessed_rows(text) == frozenset({"SR-001"})


def test_an_unmarked_MEANING_row_is_not_blessed():
    text = "- [MEANING] SR-001 Requirement -> a -> b -> differs\n"
    assert kverdict.row_rulings(text, "amendment") == {"SR-001": "MEANING"}
    assert kverdict.blessed_rows(text) == frozenset()


def test_a_row_tagged_both_ways_is_not_blessed():
    for other in ("MEANING", "CLARITY"):
        text = (
            "- [MEANING+BLESS] SR-001 Requirement -> a -> b -> differs\n"
            "- [{}] SR-001 Rationale -> a -> b -> why\n".format(other)
        )
        assert kverdict.row_rulings(text, "amendment") == {"SR-001": "MEANING"}
        assert kverdict.blessed_rows(text) == frozenset(), other


# --- the assembler's refusals (the Trust section's inputs) -------------------


def _absent(repo):
    pass


def _uncommitted(repo):
    _verdict(repo, AMENDMENT_CLARITY, "amendment", commit=False)


def _unbound(repo):
    _write(repo, VERDICT, AMENDMENT_CLARITY)
    _commit(repo, "a verdict with no binding")


def _pending(repo):
    _verdict(repo, AMENDMENT_CLARITY, "amendment", outcome="pending")


def _failed(repo):
    _verdict(repo, AMENDMENT_CLARITY, "amendment", outcome="failed")


def _malformed(repo):
    _verdict(repo, "- [CLARITY] SR-001 Requirement -> a\n", "amendment")


def _done_when(repo):
    _verdict(repo, "DONE-WHEN: CLARITY changes=1 digest=sha256:00\n", "done-when")


def _disposition(repo):
    _verdict(repo, "VERDICT: ACCEPT\n", "disposition")


@pytest.mark.parametrize(
    "state, words",
    [
        (_absent, "not committed"),
        (_uncommitted, "not committed"),
        (_unbound, "no binding"),
        (_pending, "pending"),
        (_failed, "failed"),
        (_malformed, "not a valid"),
        (_done_when, "owes no act"),
        (_disposition, "owes no act"),
    ],
)
def test_each_unaccepted_or_unreadable_verdict_is_refused_naming_why(
    tmp_path, state, words
):
    repo = _repo(tmp_path)
    _amend(repo)
    state(repo)
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None
    assert words in why, why
    values, why_values = act.act_values(repo, VERDICT, WI)
    assert values is None and why_values
    text, why_text = act.compose_act(repo, VERDICT, WI)
    assert text is None and why_text


# --- what each ruling authorizes ------------------------------------------


def test_a_mixed_first_approval_verdict_approves_only_its_approved_rows_registries(
    tmp_path,
):
    repo = _repo(tmp_path)
    _draft(repo)
    _verdict(repo, FIRST_APPROVAL_MIXED, "first-approval")
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert acts == {"first-approval": {"approves": {LLR_REL: ["LLR-002"]}}}
    values, why = act.act_values(repo, VERDICT, WI)
    assert why is None
    assert values["registries"] == "{}={}".format(LLR_REL, WI)
    assert TC_REL not in values["registries"]
    assert "LLR-002" in values["approves_rows"]
    assert "TC-002" not in values["approval_act"]


def test_a_MEANING_row_without_the_bless_mark_is_left_unacted(tmp_path):
    repo = _repo(tmp_path)
    _amend(repo)
    _verdict(
        repo,
        "- [MEANING] SR-001 Requirement -> add -> add ints -> differs\n"
        "- [CLARITY] LLR-001 Detail -> sum -> sum -> same\n\n"
        "VERDICT: MEANING rows=2\n",
        "amendment",
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert acts == {"amendment": {"reattests": ["LLR-001"], "verdict": False}}


def test_a_blessed_MEANING_row_on_a_released_rung_is_reattested(tmp_path):
    repo = _repo(tmp_path)
    _amend(repo)
    _verdict(
        repo,
        "- [MEANING+BLESS] SR-001 Requirement -> add -> add ints -> differs\n\n"
        "VERDICT: MEANING rows=1\n",
        "amendment",
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert acts == {"amendment": {"reattests": ["SR-001"], "verdict": False}}


def test_a_blessed_MEANING_row_on_a_held_rung_is_left_unacted(tmp_path):
    repo = _repo(tmp_path, dial="DevStg-Release")
    _amend(repo)
    _verdict(
        repo,
        "- [MEANING+BLESS] SR-001 Requirement -> add -> add ints -> differs\n"
        "- [CLARITY] LLR-001 Detail -> sum -> sum -> same\n\n"
        "VERDICT: MEANING rows=2\n",
        "amendment",
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert acts == {"amendment": {"reattests": ["LLR-001"], "verdict": True}}


def test_a_held_rung_CLARITY_row_is_reattested_naming_its_verdict(tmp_path):
    repo = _repo(tmp_path, dial="DevStg-Release")
    _amend(repo)
    _verdict(repo, AMENDMENT_CLARITY, "amendment")
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert acts == {"amendment": {"reattests": ["SR-001"], "verdict": True}}
    values, why = act.act_values(repo, VERDICT, WI)
    assert why is None
    assert "--reattests SR-001 --verdict {}".format(VERDICT) in values["amendment_act"]
    assert values["approval_act"] == act.NONE_OWED


def test_a_held_rung_APPROVE_row_owes_no_act(tmp_path):
    repo = _repo(tmp_path, dial="DevStg-Release")
    _draft(repo)
    _verdict(repo, FIRST_APPROVAL_MIXED, "first-approval")
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None
    assert "owes no act" in why, why


# --- order, re-runs and the committed tree --------------------------------


def _combined_repo(tmp_path):
    repo = _repo(tmp_path)
    _replace(repo, SRS, "add two numbers.", "add two integers.")
    _append(repo, LLRS, NEW_LLR)
    _commit(repo, "amend SR-001, draft LLR-002")
    _verdict(repo, COMBINED, "combined", COMBINED_KINDS)
    return repo


def test_a_combined_verdict_lists_the_amendment_act_before_the_first_approval_act(
    tmp_path,
):
    repo = _combined_repo(tmp_path)
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert list(acts) == ["amendment", "first-approval"]
    text, why = act.compose_act(repo, VERDICT, WI)
    assert why is None
    assert text.index("--reattests SR-001") < text.index("--approves")


def test_a_combined_act_interrupted_between_its_commits_lists_only_the_first_approval_act(
    tmp_path,
):
    repo = _combined_repo(tmp_path)
    _take_amendment_act(repo, ["SR-001"])
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert acts == {"first-approval": {"approves": {LLR_REL: ["LLR-002"]}}}
    values, _why = act.act_values(repo, VERDICT, WI)
    assert values["amendment_act"] == act.NONE_OWED
    assert "--reattests" not in values["approval_act"]


def test_a_flip_committed_without_its_copy_is_refused_naming_the_row(tmp_path):
    repo = _repo(tmp_path)
    _draft(repo)
    _verdict(repo, FIRST_APPROVAL_MIXED, "first-approval")
    _replace(repo, LLRS, ",Drafted,,P1", ",Approved,,P1")
    _commit(repo, "flip LLR-002 with no copy")
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None
    assert "LLR-002" in why and "inconsistent" in why, why


def test_a_Drafted_row_present_unchanged_in_a_whole_registry_copy_is_owed(tmp_path):
    repo = _repo(tmp_path)
    _draft(repo)
    copy = repo / baseline_snapshot.SNAPSHOT_DIR / LLRS
    shutil.copyfile(repo / LLRS, copy)
    _commit(repo, "a whole-registry copy carrying LLR-002 Drafted")
    _verdict(repo, FIRST_APPROVAL_MIXED, "first-approval")
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert acts == {"first-approval": {"approves": {LLR_REL: ["LLR-002"]}}}


def test_a_reattest_of_a_row_below_Approved_is_refused_naming_the_row(tmp_path):
    repo = _repo(tmp_path)
    _draft(repo)
    _verdict(
        repo,
        "- [CLARITY] LLR-002 Detail -> sub -> sub -> same\n\nVERDICT: CLARITY rows=1\n",
        "amendment",
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None
    assert "LLR-002" in why and "inconsistent" in why, why


def test_a_completed_act_owes_none_and_is_refused(tmp_path):
    repo = _combined_repo(tmp_path)
    values, why = act.act_values(repo, VERDICT, WI)
    assert why is None
    _take_amendment_act(repo, ["SR-001"])
    _take_approval_act(repo, ["LLR-002"], values["registries"])
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None
    assert "owes no act" in why, why
    text, why = act.compose_act(repo, VERDICT, WI)
    assert text is None and "owes no act" in why


def _shell_command_count(line):
    """How many commands a POSIX shell reads `line` as: `shlex` with
    `punctuation_chars` yields an unquoted `;` as its own token and keeps a
    quoted one inside its string."""
    lex = shlex.shlex(line, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    return sum(1 for token in lex if token == ";") + 1


def test_the_rendered_act_commands_survive_a_shell(tmp_path):
    repo = _repo(tmp_path)
    _draft(repo)
    _verdict(
        repo,
        "- [APPROVE] LLR-002 -> sub -> chain holds -> ready\n"
        "- [APPROVE] TC-002 -> sub -> chain holds -> ready\n\n"
        "OUTCOME: APPROVE rows=2\n",
        "first-approval",
    )
    text, why = act.compose_act(repo, VERDICT, WI)
    assert why is None
    lines = [ln.strip() for ln in text.splitlines() if "snapshot --approves" in ln]
    commands = [ln for ln in lines if ln.startswith("python ")]
    assert len(commands) == 1, lines
    assert _shell_command_count(commands[0]) == 1, commands[0]
    argv = shlex.split(commands[0])
    approves = baseline_snapshot.parse_approves(argv[argv.index("--approves") + 1])
    assert approves == {LLR_REL: WI, TC_REL: WI}


def test_the_act_reads_HEAD_not_the_working_tree(tmp_path):
    repo = _repo(tmp_path)
    _draft(repo)
    _verdict(repo, FIRST_APPROVAL_MIXED, "first-approval")
    _replace(repo, LLRS, ",Drafted,,P1", ",Approved,,P1")
    baseline_snapshot.copy_live(
        repo, approves=baseline_snapshot.parse_approves("{}={}".format(LLR_REL, WI))
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert acts == {"first-approval": {"approves": {LLR_REL: ["LLR-002"]}}}


def test_the_composed_act_brief_names_its_verdict_and_trailer(tmp_path):
    repo = _repo(tmp_path)
    _amend(repo)
    _verdict(repo, AMENDMENT_CLARITY, "amendment")
    text, why = act.compose_act(repo, VERDICT, WI)
    assert why is None
    assert VERDICT in text
    assert "WI: {}".format(WI) in text
    assert not act.prompts.slots(text)


def test_a_two_registry_act_says_which_rows_each_approves_token_covers(tmp_path):
    # Moved from the judging brief (WI-572 REVIEW-A round 7, MAJOR 3), where
    # the `--approves` argument was fixed at composition and the session had
    # to drop a returned registry's token by hand. The act derives it from
    # the committed verdict, and still says which rows each token covers.
    repo = _repo(tmp_path)
    _draft(repo)
    _verdict(
        repo,
        "- [APPROVE] LLR-002 -> sub -> chain holds -> ready\n"
        "- [APPROVE] TC-002 -> sub -> chain holds -> ready\n\n"
        "OUTCOME: APPROVE rows=2\n",
        "first-approval",
    )
    values, why = act.act_values(repo, VERDICT, WI)
    assert why is None
    covers = values["approves_rows"]
    assert "`{}={}` covers LLR-002".format(LLR_REL, WI) in covers
    assert "`{}={}` covers TC-002".format(TC_REL, WI) in covers
    for rel in baseline_snapshot.parse_approves(values["registries"]):
        assert "`{}=".format(rel) in covers, rel


def test_a_row_ruled_on_two_lines_is_listed_once(tmp_path):
    # Moved from the judging brief's two-SR token test: a row named twice
    # reads as two rows, and the act's lists are what the session counts.
    repo = _repo(tmp_path)
    _draft(repo)
    _verdict(
        repo,
        "- [APPROVE] LLR-002 -> sub -> chain of SR-001 -> ready\n"
        "- [APPROVE] LLR-002 -> sub -> chain of SR-002 -> ready\n\n"
        "OUTCOME: APPROVE rows=1\n",
        "first-approval",
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None
    assert acts == {"first-approval": {"approves": {LLR_REL: ["LLR-002"]}}}
    values, _why = act.act_values(repo, VERDICT, WI)
    assert values["approves_rows"].count("LLR-002") == 1


# --- a retired row (WI-912, the S3 Re-runs partition) ----------------------

RETIRE_COMBINED = (
    "## amendment\n\n"
    "- [CLARITY] TC-001 Status -> Approved -> (deleted) -> retirement\n\n"
    "VERDICT: CLARITY rows=1\n\n"
    "## first-approval\n\n"
    "- [APPROVE] TC-002 -> sub -> chain holds -> ready\n\n"
    "OUTCOME: APPROVE rows=1\n\n"
    "SITTING: JUDGED kinds=amendment;first-approval\n"
)


def _retire(repo, draft=True):
    """Delete the Approved TC-001 from its live registry and, by default,
    draft TC-002 in the same registry, committed."""
    text = (repo / TCS).read_text(encoding="utf-8")
    kept = [ln for ln in text.splitlines() if not ln.startswith("TC-001,")]
    _write(repo, TCS, "\n".join(kept) + "\n")
    if draft:
        _append(repo, TCS, NEW_TC.replace("LLR-002", "LLR-001"))
    _commit(repo, "retire TC-001")


def test_a_retired_row_ruled_CLARITY_beside_a_first_approval_is_listed_in_the_reattests(
    tmp_path,
):
    repo = _repo(tmp_path)
    _retire(repo)
    _verdict(repo, RETIRE_COMBINED, "combined", COMBINED_KINDS)
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None, why
    assert acts == {
        "amendment": {"reattests": ["TC-001"], "verdict": False, "retires": ["TC-001"]},
        "first-approval": {"approves": {TC_REL: ["TC-002"]}},
    }
    text, why = act.compose_act(repo, VERDICT, WI)
    assert why is None, why
    assert "Retire" in text and "TC-001" in text
    assert text.index("--reattests TC-001") < text.index("--approves")


def test_a_retirement_and_its_first_approval_taken_through_the_snapshot_writer_leave_nothing_owed(
    tmp_path,
):
    repo = _repo(tmp_path)
    _retire(repo)
    _verdict(repo, RETIRE_COMBINED, "combined", COMBINED_KINDS)
    values, why = act.act_values(repo, VERDICT, WI)
    assert why is None, why
    _take_amendment_act(repo, ["TC-001"])
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None, why
    assert acts == {"first-approval": {"approves": {TC_REL: ["TC-002"]}}}
    _take_approval_act(repo, ["TC-002"], values["registries"])
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None and "owes no act" in why, why
    assert act.left_owed(repo, VERDICT, "HEAD") is None


def test_a_retirement_on_a_held_rung_owes_no_act(tmp_path):
    repo = _repo(tmp_path, dial="DevStg-Release")
    _retire(repo, draft=False)
    _verdict(
        repo,
        "- [CLARITY] TC-001 Status -> Approved -> (deleted) -> retirement\n\n"
        "VERDICT: CLARITY rows=1\n",
        "amendment",
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None and "owes no act" in why, why
    _amend(repo)
    _verdict(
        repo,
        "- [CLARITY] TC-001 Status -> Approved -> (deleted) -> retirement\n"
        "- [CLARITY] SR-001 Requirement -> add -> add -> same\n\n"
        "VERDICT: CLARITY rows=2\n",
        "amendment",
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert why is None, why
    assert acts == {"amendment": {"reattests": ["SR-001"], "verdict": True}}


def test_a_first_approval_of_a_row_absent_from_the_committed_tree_is_refused_naming_it(
    tmp_path,
):
    repo = _repo(tmp_path)
    _verdict(
        repo,
        "- [APPROVE] LLR-009 -> x -> chain holds -> ready\n\nOUTCOME: APPROVE rows=1\n",
        "first-approval",
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None
    assert "LLR-009" in why and "inconsistent" in why, why


# --- refusals no other case reaches -----------------------------------------


def test_an_approval_owed_where_no_approval_record_exists_is_refused(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    pin_autocrlf(repo)
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _write(repo, SRS, SPINE_SRS)
    _write(repo, LLRS, SPINE_LLRS + NEW_LLR)
    _write(repo, TCS, SPINE_TCS)
    set_process_key(repo, "attestation", "human_approval_through", "DevStg-Needs")
    _commit(repo, "a spine with no approval record")
    _verdict(repo, FIRST_APPROVAL_MIXED, "first-approval")
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None
    assert "no approval record" in why, why


def test_a_ruled_row_no_compared_tier_holds_is_refused_naming_it(tmp_path):
    # CLARITY, since an APPROVE of such a row reads as held and owes no act.
    repo = _repo(tmp_path)
    _verdict(
        repo,
        "- [CLARITY] PB-001 Title -> a -> a -> same\n\nVERDICT: CLARITY rows=1\n",
        "amendment",
    )
    acts, why = act.owed_acts(repo, VERDICT, "HEAD")
    assert acts is None
    assert "PB-001" in why and "no compared tier" in why, why


def test_a_verdict_path_outside_the_root_is_refused(tmp_path):
    repo = _repo(tmp_path)
    _amend(repo)
    _verdict(repo, AMENDMENT_CLARITY, "amendment")
    outside = tmp_path / "elsewhere" / "001-ADJUDICATE-abc1234.md"
    acts, why = act.owed_acts(repo, outside, "HEAD")
    assert acts is None
    assert "lies outside" in why, why


# --- the arm each ruling owes follows the held-rung policy's one home -------


def test_each_rows_act_arm_follows_the_adjudication_action_policy_on_every_rung():
    # Every (held, ruling) pair the verdict grammar admits, with and without
    # the bless mark: the assembler's arm is read from
    # `intake.adjudication_action`, so a change there moves both together.
    intake = load_script("intake")
    rulings = {
        word
        for kind in ("amendment", "first-approval")
        for word in kverdict.ROW_RULINGS[kind][0].values()
    }
    assert rulings == {"MEANING", "CLARITY", "APPROVE", "RETURN"}
    for held in (True, False):
        for ruling in sorted(rulings):
            for blessed in (True, False):
                policy = intake.adjudication_action(held, ruling)
                arm = act._arm(ruling, held, blessed)
                case = (held, ruling, blessed, policy, arm)
                if ruling == "RETURN" or policy == "recommend":
                    assert arm is None, case
                elif ruling == "MEANING" and not blessed:
                    assert arm is None, case
                elif ruling == "APPROVE":
                    assert arm == "approve", case
                else:
                    assert arm == "reattest", case
