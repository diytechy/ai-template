"""The subjective-quality critique loop (WI-068). Managed mode: a committing
build whose WI touches a Verification=Critique SR schedules a fresh,
provider-heterogeneous CRITIQUE session against a rubric before the next build.
Exercised end-to-end against a fake agent that plays both builder and critic, so
no test touches a real CLI. Absent an enable-list OR any Critique SR, nothing
changes (the never-breaking guarantee)."""

import csv
import subprocess
import sys

import pytest
from conftest import set_process_key, SCRIPTS, load_script, run_py, write_wi_registry

agent_loop = load_script("agent_loop")

# The fake agent: a critic (prompt names a verdict path) writes its scripted
# verdict + commits; a builder commits `WI-050: ...` progress (so build_scope_srs
# reads WI-050 off the commit subject) and, after N builds, writes DONE.
FAKE = r"""
import argparse, os, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "models.txt"), "a", encoding="utf-8") as fh:
    fh.write(args.model + "\n")
with open(str(ctl / "prompts.txt"), "a", encoding="utf-8") as fh:
    fh.write("=== " + args.model + " ===\n" + args.prompt + "\n=== end ===\n")


def commit(path, msg):
    subprocess.run(["git", "add", str(path)], check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], check=True)


m = re.search(r"Write your verdict to (\S+)", args.prompt)
if m:
    vpath = pathlib.Path(m.group(1))
    vpath.parent.mkdir(parents=True, exist_ok=True)
    vpath.write_text((ctl / "verdict.txt").read_text(encoding="utf-8"), encoding="utf-8")
    commit(vpath, "critique verdict")
else:
    cf = ctl / "builds.txt"
    n = len(cf.read_text(encoding="utf-8").splitlines()) if cf.exists() else 0
    with open(str(cf), "a", encoding="utf-8") as fh:
        fh.write("b\n")
    pathlib.Path("art.txt").write_text("render " + str(n), encoding="utf-8")
    done_after = (
        int((ctl / "done_after").read_text(encoding="utf-8"))
        if (ctl / "done_after").exists()
        else 999
    )
    # WI-210: the end state is committed worker evidence (the WI trailer).
    if n + 1 >= done_after:
        commit("art.txt", "WI-050: build the render " + str(n) + "\n\nWI: WI-050")
    else:
        commit("art.txt", "WI-050: build the render " + str(n))
sys.exit(0)
"""

STATUS_MD = """# Status

## Current State

- **Open items:**
  - **Needs <human>**: OI-9 — a pending ask
"""

# SR-050 is Critique; its Requirement carries a marker so the redaction test can
# assert the intent reached the critic. TC-050 names the rubric in Parameters.
SR_HEADER = (
    "SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,"
    "Permutations,Priority,Verification,Status\n"
)
SR_CRITIQUE = (
    'SR-050,Render realism,SN-001,"SR-INTENT-MARKER the render shall look real.",'
    '"Subjective.","Judged against the rubric.",,S,Critique,Approved\n'
)
SR_TEST = (
    'SR-050,Render realism,SN-001,"The render shall look real.",'
    '"Objective.","render(x)==y.",,S,Test,Approved\n'
)

TC_ROW = (
    "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
    "TC-050,SR-050,System,critique against the rubric,Release,"
    '"rubric=docs/rubrics/render.md; artifact=art.txt","Critic APPROVE",No,,Approved\n'
)

# The registry's one home is `docs/work/` spec files, so the fixture hands
# conftest cell-lists under this (non-default) column order. Status is the spec's
# DIRECTORY now: `queued/`, which is what a worker builds — the preflight refuses
# only the terminal statuses, so the CSV era's `active` cell carried no weight here.
WI_HEADER = [
    "WI-ID",
    "Title",
    "Workstream",
    "SR-Refs",
    "Predecessors",
    "Status",
    "Deliverable",
    "SpecRef",
    "CritiqueBudget",
    "CritiqueExhaustion",
]


def _wi_row(budget="", exhaustion=""):
    """WI-050 — the assigned work item, whose SR-050 reaches the Critique SR."""
    return [
        "WI-050",
        "Render",
        "scripts",
        "SR-050",
        "",
        "queued",
        "",
        "docs/specs/WI-050.md",
        budget,
        exhaustion,
    ]


RUBRIC = "# render rubric\n\n- DevBar-Reqs contact shadows are consistent\n- B1 RUBRIC-MARKER seam artifacts\n"

APPROVE = "- [MINOR] art.txt -> DevBar-Reqs mostly holds -> tidy -> @owner\nVERDICT: APPROVE findings=1\n"
CHANGES = (
    "- [MAJOR] art.txt -> B1 seam artifact at the join -> reseat the mesh -> @owner\n"
    "VERDICT: CHANGES-REQUESTED findings=1\n"
)


def _git(repo, *args):
    p = subprocess.run(
        ["git", "-C", str(repo)] + list(args),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
    )
    assert p.returncode == 0, p.stdout + p.stderr
    return p.stdout.strip()


@pytest.fixture
def critique_repo(tmp_path):
    """A git repo wired for managed routing with a Critique SR: a medium PROVA
    builder + a strong PROVB critic (different provider). Returns (repo, control,
    cmd-template)."""
    repo = tmp_path / "repo"
    (repo / "docs" / "requirements").mkdir(parents=True)
    (repo / "docs" / "test").mkdir(parents=True)
    (repo / "docs" / "rubrics").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    set_process_key(repo, "policies", "review_rounds", 0)  # critique only
    (repo / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + SR_CRITIQUE, encoding="utf-8"
    )
    write_wi_registry(repo, [_wi_row()], header=WI_HEADER)
    (repo / "docs" / "test" / "test-cases.csv").write_text(TC_ROW, encoding="utf-8")
    (repo / "docs" / "rubrics" / "render.md").write_text(RUBRIC, encoding="utf-8")

    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "checkout", "-q", "-b", "llm/train/t1")

    ctl = tmp_path / "control"
    ctl.mkdir()
    (ctl / "verdict.txt").write_text(APPROVE, encoding="utf-8")
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    cmd = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    rows = [
        ["Id", "Provider", "Model", "Version", "Tier", "CmdTemplate", "Notes"],
        ["PROVA-BUILD-1", "PROVA", "builda", "1", "medium", cmd, ""],
        ["PROVB-CRIT-1", "PROVB", "critb", "1", "strong", cmd, ""],
    ]
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(rows)
    (repo / "docs" / "agents-enabled").write_text(
        "PROVA-BUILD-1\nPROVB-CRIT-1\n", encoding="utf-8"
    )
    return repo, ctl, cmd


def _commit_config(repo):
    # A worker's DONE is judged from committed evidence + a CLEAN tree
    # (WI-210), so the fixture/test config written after the seed commit
    # must be committed before the worker starts.
    subprocess.run(["git", "-C", str(repo), "add", "-A"], capture_output=True)
    subprocess.run(
        ["git", "-C", str(repo), "commit", "-q", "-m", "test config", "--allow-empty"],
        capture_output=True,
    )


def _loop(repo, cmd, *extra):
    _commit_config(repo)
    return run_py(
        [
            SCRIPTS / "agent_loop.py",
            "--root",
            repo,
            "--agent-cmd",
            cmd,
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--max-iterations",
            "8",
            "--wi",
            "WI-050",
            "--train",
            "t1",
            *extra,
        ],
        cwd=repo,
    )


def _models(ctl):
    p = ctl / "models.txt"
    return p.read_text(encoding="utf-8").split() if p.exists() else []


def _set_critique_control(repo, budget, exhaustion):
    # Re-writing the id replaces its spec file in docs/work/ (the registry's one
    # home), so the two control cells are re-declared rather than patched in place.
    write_wi_registry(repo, [_wi_row(budget, exhaustion)], header=WI_HEADER)
    _git(repo, "add", "docs/work")
    _git(repo, "commit", "-qm", "set critique control")


def test_critique_scheduled_when_critique_sr_in_scope(critique_repo):
    repo, ctl, cmd = critique_repo
    (ctl / "done_after").write_text(
        "2", encoding="utf-8"
    )  # build -> critique -> build(DONE)
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # The build touching SR-050 scheduled a CRITIQUE round, logged before launch.
    assert "scheduling CRITIQUE round" in proc.stdout
    assert "SR-050" in proc.stdout
    # The critic ran on a DIFFERENT provider (heterogeneity) and wrote a verdict.
    models = _models(ctl)
    assert "builda" in models and "critb" in models
    assert list((repo / "docs" / "reviews" / "t1").glob("*-CRITIQUE-*.md"))


def test_no_critique_when_no_critique_sr(critique_repo):
    # Same setup but SR-050 is Test, not Critique -> the layer is vacuous.
    repo, ctl, cmd = critique_repo
    (repo / "docs" / "requirements" / "system-requirements.csv").write_text(
        SR_HEADER + SR_TEST, encoding="utf-8"
    )
    _git(repo, "commit", "-aqm", "make SR-050 Test")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "scheduling CRITIQUE round" not in proc.stdout
    assert "critb" not in _models(ctl)
    assert not (repo / "docs" / "reviews").exists()


def test_critique_prompt_is_redacted_and_carries_rubric_and_intent(critique_repo):
    repo, ctl, cmd = critique_repo
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    crit_block = prompts.split("=== critb ===\n", 1)[1].split("\n=== end ===", 1)[0]
    assert "INDEPENDENT critic" in crit_block
    # The brief carried the rubric text AND the SN/SR intent...
    assert "RUBRIC-MARKER" in crit_block
    assert "SR-INTENT-MARKER" in crit_block
    # ...and NEVER the implementer's driver resume prompt / self-assessment.
    assert "resume from docs/status.md Current State" not in crit_block
    assert "assume no human is watching" not in crit_block


def test_prompt_map_slots_a_custom_critique_template(critique_repo):
    repo, ctl, cmd = critique_repo
    (ctl / "done_after").write_text("2", encoding="utf-8")
    tmpl = repo / "docs" / "prompts" / "crit.md"
    tmpl.parent.mkdir(parents=True)
    tmpl.write_text(
        "CUSTOM-CRITIQUE-MARKER — {brief}\nWrite your verdict to {verdict}\n",
        encoding="utf-8",
    )
    proc = _loop(repo, cmd, "--prompt-map", "CRITIQUE=docs/prompts/crit.md")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    assert "CUSTOM-CRITIQUE-MARKER" in prompts  # the mapped template was used
    assert "RUBRIC-MARKER" in prompts  # {brief} still slotted


def test_critique_budget_exhaustion_pages_human(critique_repo):
    # A perpetually CHANGES-REQUESTED critique trips the budget after
    # AGENT_CRITIQUE_MAX rounds and pages the human (attended -> NEEDS-HUMAN, 7).
    import os

    repo, ctl, cmd = critique_repo
    (ctl / "verdict.txt").write_text(CHANGES, encoding="utf-8")
    (ctl / "done_after").write_text("999", encoding="utf-8")  # never self-terminates
    env = dict(os.environ)
    env["AGENT_CRITIQUE_MAX"] = "2"
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "agent_loop.py"),
            "--root",
            str(repo),
            "--agent-cmd",
            cmd,
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--max-iterations",
            "10",
            "--wi",
            "WI-050",
            "--train",
            "t1",
        ],
        cwd=str(repo),
        capture_output=True,
        text=True,
        stdin=subprocess.DEVNULL,
        env=env,
    )
    assert proc.returncode == 7, proc.stdout + proc.stderr
    assert "critique budget exhausted" in proc.stdout
    # A worker never writes run-state (WI-210): the exit code pages the
    # dispatcher, which generates the root file.
    assert not (repo / "docs" / "run-state").exists()


def test_per_wi_infinite_budget_keeps_iterating(critique_repo):
    repo, ctl, cmd = critique_repo
    _set_critique_control(repo, "inf", "move-on")
    (ctl / "verdict.txt").write_text(CHANGES, encoding="utf-8")
    proc = _loop(repo, cmd, "--max-iterations", "6")
    assert proc.returncode == 6, proc.stdout + proc.stderr
    assert _models(ctl).count("critb") >= 2
    assert "critique budget exhausted" not in proc.stdout


@pytest.mark.parametrize("disposition,expected", [("move-on", 6), ("block", 7)])
def test_per_wi_exhaustion_disposition_overrides_autonomous(
    critique_repo, disposition, expected
):
    repo, ctl, cmd = critique_repo
    _set_critique_control(repo, "1", disposition)
    # SN-029: the loop-held end of the ordinal.
    set_process_key(repo, "attestation", "human_ratification_through", 0)
    _git(repo, "add", "docs/process.toml")
    _git(repo, "commit", "-qm", "set the loop-held ratification level")
    (ctl / "verdict.txt").write_text(CHANGES, encoding="utf-8")
    proc = _loop(repo, cmd, "--max-iterations", "3")
    assert proc.returncode == expected, proc.stdout + proc.stderr
    if disposition == "block":
        # A worker never writes run-state (WI-210): exit 7 is the page.
        assert not (repo / "docs/run-state").exists()
    else:
        # docs/run-phase is retired (WI-180): the design-check escalation sets the
        # phase in-process, observable as the next session routing DESIGN-CHECK.
        assert "phase=DESIGN-CHECK" in proc.stdout


def test_absent_enable_list_no_critique(critique_repo):
    # No agents-enabled -> managed off -> no critique scheduled (never-breaking).
    repo, ctl, cmd = critique_repo
    (repo / "docs" / "agents-enabled").unlink()
    (ctl / "done_after").write_text("1", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "scheduling CRITIQUE round" not in proc.stdout
    assert not (repo / "docs" / "reviews").exists()


# The stock FAKE reads one shared verdict.txt; this variant keys the scripted
# verdict per model so two critics can disagree within one run.
FAKE_PER_MODEL = FAKE.replace(
    '(ctl / "verdict.txt")', '(ctl / ("verdict-" + args.model + ".txt"))'
)

GARBLED = (
    "- [MAJOR] art.txt -> B1 seam artifact at the join -> reseat the mesh -> @owner\n"
    "Approved, looks great! (no machine line)\n"
)


def test_critique_unparseable_verdict_not_treated_as_approved(critique_repo, tmp_path):
    # Repo-review 2026-07-21 H-1 (the WI-243 "fail closed" lesson one layer
    # down): a critique verdict FILE with no parseable `VERDICT:` machine line
    # was previously treated as APPROVED — scope reset, queue cleared. It must
    # fail closed like a missing file: cool + re-critique; a second enabled
    # critic then closes the round with a real APPROVE.
    repo, ctl, cmd = critique_repo
    (tmp_path / "fake.py").write_text(FAKE_PER_MODEL, encoding="utf-8")
    (ctl / "verdict-critb.txt").write_text(GARBLED, encoding="utf-8")
    (ctl / "verdict-critc.txt").write_text(APPROVE, encoding="utf-8")
    rows = [
        ["Id", "Provider", "Model", "Version", "Tier", "CmdTemplate", "Notes"],
        ["PROVA-BUILD-1", "PROVA", "builda", "1", "medium", cmd, ""],
        ["PROVB-CRIT-1", "PROVB", "critb", "1", "strong", cmd, ""],
        ["PROVC-CRIT-2", "PROVC", "critc", "1", "strong", cmd, ""],
    ]
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(rows)
    (repo / "docs" / "agents-enabled").write_text(
        "PROVA-BUILD-1\nPROVB-CRIT-1\nPROVC-CRIT-2\n", encoding="utf-8"
    )
    (ctl / "done_after").write_text("1", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "verdict file has no parseable VERDICT line" in proc.stdout
    assert "re-critiquing" in proc.stdout
    # The garble was NOT approved: the round closed via the second critic.
    assert "critique [PROVC-CRIT-2]: verdict=APPROVE" in proc.stdout
    models = _models(ctl)
    assert "critb" in models and "critc" in models


# (test_critique_requirement_is_orthogonal_to_the_reviewer_dial retired with
# the dispatcher's _required_phases at concurrency-restructure Phase 5 — the
# integrator's verdict gate reads the review-policy dial itself, test_integrate.)
