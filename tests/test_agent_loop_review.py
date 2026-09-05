"""Loop-side reviewer dispatch + docs/agents.csv routing (WI-059, S8). Managed
mode: the enable-list's presence turns on model routing + reviewer scheduling.
Exercised end-to-end against a fake agent that plays both implementer and
reviewer, so no test touches a real CLI. Absent files keep the legacy behavior
(covered byte-for-byte by test_agent_loop.py)."""

import csv
import json
import subprocess
import sys

import pytest
from conftest import SCRIPTS, load_script, pin_autocrlf, run_py, write_wi_registry

agent_loop = load_script("agent_loop")

# The fake agent: records the model + prompt it was handed, then acts by ROLE —
# a reviewer (the prompt names a verdict path) writes its scripted verdict and
# commits; an implementer commits progress and, after N builds, writes DONE so
# the run terminates.
# Distinct per-reviewer verdicts — two INDEPENDENT reviews must not read as
# near-identical (that legitimately trips the anti-gaming tripwire).
REVB_BODY = (
    "- [MAJOR] work.txt:1 -> revb: an unhandled boundary condition slips "
    "through -> add a guard clause before the loop -> @owner\n"
    "VERDICT: APPROVE findings=1\n"
)
REVC_BODY = (
    "- [MINOR] work.txt:1 -> revc: the progress message wording is stale after "
    "the rename -> reword it to name the new step -> @owner\n"
    "VERDICT: APPROVE findings=1\n"
)

FAKE = r"""
import argparse, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "models.txt"), "a", encoding="utf-8") as fh:
    fh.write(args.model + "\n")
with open(str(ctl / "prompts.txt"), "a", encoding="utf-8") as fh:
    fh.write("=== " + args.model + " ===\n" + args.prompt + "\n")
BODIES = __import__("json").loads((ctl / "bodies.json").read_text(encoding="utf-8"))


def commit(path, msg):
    subprocess.run(["git", "add", str(path)], check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], check=True)


m = re.search(r"Write your verdict to (\S+)", args.prompt)
if m:
    vpath = pathlib.Path(m.group(1))
    override = ctl / "verdict_body.txt"
    text = (
        override.read_text(encoding="utf-8")
        if override.exists()
        else BODIES.get(args.model, BODIES["_default"])
    )
    vpath.parent.mkdir(parents=True, exist_ok=True)
    vpath.write_text(text, encoding="utf-8")
    commit(vpath, "review verdict")
else:
    cf = ctl / "builds.txt"
    n = len(cf.read_text(encoding="utf-8").splitlines()) if cf.exists() else 0
    with open(str(cf), "a", encoding="utf-8") as fh:
        fh.write("b\n")
    pathlib.Path("work.txt").write_text("build progress " + str(n), encoding="utf-8")
    done_after = (
        int((ctl / "done_after").read_text(encoding="utf-8"))
        if (ctl / "done_after").exists()
        else 999
    )
    # WI-210: the end state is committed worker evidence (the WI trailer).
    if n + 1 >= done_after:
        commit("work.txt", "build progress " + str(n) + "\n\nWI: WI-201")
    else:
        commit("work.txt", "build progress " + str(n))
sys.exit(0)
"""

# A variant of FAKE whose FIRST session on a chosen model fails before working —
# either a rate-limit signal (fail_mode=limit -> the WAITING outcome) or a plain
# nonzero exit with no JSON (fail_mode=error -> the ERROR outcome). Every other
# model builds normally. Used to pin the managed cool-and-re-route branches
# (agent_loop.py rate-limit WAITING / ERROR paths) from outside.
FAKE_FIRST_FAILS = r"""
import argparse, json, pathlib, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "models.txt"), "a", encoding="utf-8") as fh:
    fh.write(args.model + "\n")


def _read(name):
    p = ctl / name
    return p.read_text(encoding="utf-8").strip() if p.exists() else ""


if args.model == _read("fail_model"):
    if _read("fail_mode") == "limit":
        print(json.dumps({"is_error": True,
                          "result": "You've hit your session limit; resets 3:45pm"}))
        sys.exit(1)
    print("fatal: model endpoint unreachable")  # no JSON, nonzero -> ERROR
    sys.exit(2)
cf = ctl / "builds.txt"
n = len(cf.read_text(encoding="utf-8").splitlines()) if cf.exists() else 0
with open(str(cf), "a", encoding="utf-8") as fh:
    fh.write("b\n")
pathlib.Path("work.txt").write_text("build " + str(n), encoding="utf-8")
subprocess.run(["git", "add", "work.txt"], check=True)
done_after = int(_read("done_after")) if _read("done_after") else 999
msg = "build " + str(n)
if n + 1 >= done_after:
    msg += "\n\nWI: WI-201"  # WI-210: committed worker evidence
subprocess.run(["git", "commit", "-q", "-m", msg], check=True)
sys.exit(0)
"""

# A variant of FAKE where a chosen reviewer model writes NO verdict file (it just
# exits): the loop must cool it and re-dispatch the SAME review phase to another
# enabled reviewer. Every other reviewer/implementer behaves like FAKE.
FAKE_REVIEWER_SKIPS = r"""
import argparse, json, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "models.txt"), "a", encoding="utf-8") as fh:
    fh.write(args.model + "\n")
BODIES = json.loads((ctl / "bodies.json").read_text(encoding="utf-8"))
skip = (
    (ctl / "skip_verdict_model").read_text(encoding="utf-8").strip()
    if (ctl / "skip_verdict_model").exists()
    else ""
)


def commit(path, msg):
    subprocess.run(["git", "add", str(path)], check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], check=True)


m = re.search(r"Write your verdict to (\S+)", args.prompt)
if m:
    if args.model == skip:
        sys.exit(0)  # write NO verdict -> the loop cools + re-routes the phase
    vpath = pathlib.Path(m.group(1))
    vpath.parent.mkdir(parents=True, exist_ok=True)
    vpath.write_text(BODIES.get(args.model, BODIES["_default"]), encoding="utf-8")
    commit(vpath, "review verdict")
else:
    cf = ctl / "builds.txt"
    n = len(cf.read_text(encoding="utf-8").splitlines()) if cf.exists() else 0
    with open(str(cf), "a", encoding="utf-8") as fh:
        fh.write("b\n")
    pathlib.Path("work.txt").write_text("build " + str(n), encoding="utf-8")
    done_after = (
        int((ctl / "done_after").read_text(encoding="utf-8"))
        if (ctl / "done_after").exists()
        else 999
    )
    if n + 1 >= done_after:
        commit("work.txt", "build " + str(n) + "\n\nWI: WI-201")
    else:
        commit("work.txt", "build " + str(n))
sys.exit(0)
"""

STATUS_MD = """# Status

## Current State

- **Open items:**
  - **Needs <human>**: OI-9 — a pending ask
"""

CHANGES_REQUESTED_BODY = (
    "- [MAJOR] work.txt:1 -> broken -> fix -> @owner\n"
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


def _wi_201_row(tier):
    """The assigned work item, as a 10-wide conftest WI row at `tier` — the
    BuildTier the worker pins its build session to (WI-181)."""
    return [
        "WI-201",
        "Scoped work for WI-201",
        "ws",
        "",
        "",
        "queued",
        "",
        "",
        tier,
        "ordinary",
    ]


@pytest.fixture
def managed_repo(tmp_path):
    """A git repo wired for managed routing: docs/agents.csv (all rows point at
    ONE fake, distinguished by Provider/Model/Tier) + docs/agents-enabled +
    run-phase=BUILD. Returns (repo, control-dir, base-template, cmd-template)."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    (repo / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    write_wi_registry(repo, [_wi_201_row("medium")])
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    _git(repo, "init")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "checkout", "-q", "-b", "llm/train/t1")

    ctl = tmp_path / "control"
    ctl.mkdir()
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    cmd = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )

    # One fake, four registry rows: a medium implementer (PROVA) and two
    # different-provider medium reviewers (PROVB, PROVC), plus a strong PROVA.
    rows = [
        ["Id", "Provider", "Model", "Version", "Tier", "CmdTemplate", "Notes"],
        ["PROVA-BUILD-1", "PROVA", "builda", "1", "medium", cmd, ""],
        ["PROVB-REV-1", "PROVB", "revb", "1", "medium", cmd, ""],
        ["PROVC-REV-1", "PROVC", "revc", "1", "medium", cmd, ""],
        ["PROVA-STRONG-1", "PROVA", "stronga", "1", "strong", cmd, ""],
    ]
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(rows)
    (repo / "docs" / "agents-enabled").write_text(
        "# preference order\nPROVA-BUILD-1\nPROVB-REV-1\nPROVC-REV-1\nPROVA-STRONG-1\n",
        encoding="utf-8",
    )
    import json

    (ctl / "bodies.json").write_text(
        json.dumps(
            {
                "revb": REVB_BODY,
                "revc": REVC_BODY,
                "_default": "- [MINOR] work.txt:1 -> a minor nit -> tidy it -> @owner\n"
                "VERDICT: APPROVE findings=1\n",
            }
        ),
        encoding="utf-8",
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
            cmd,  # the base template (preflight); managed uses the registry
            "--pause",
            "0",
            "--model",
            "default-tier",
            "--max-iterations",
            "8",
            "--wi",
            "WI-201",
            "--train",
            "t1",
            *extra,
        ],
        cwd=repo,
    )


def _models(ctl):
    p = ctl / "models.txt"
    return p.read_text(encoding="utf-8").split() if p.exists() else []


def _routes(stdout, phase):
    """The `route [<phase>]:` selection lines the loop logs before each launch —
    the no-silent-swap record (each names the chosen registry id + tier)."""
    tag = "route [{}]".format(phase)
    return [ln for ln in stdout.splitlines() if ln.startswith(tag)]


def test_review_policy_1_dispatches_one_heterogeneous_reviewer(managed_repo):
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    models = _models(ctl)
    # The implementer routed to PROVA (builda); the reviewer to a DIFFERENT
    # provider (PROVB revb) — heterogeneity preference honored.
    assert "builda" in models and "revb" in models
    assert "revc" not in models, "policy 1 schedules only REVIEW-A"
    assert "dispatch: review-policy 1" in proc.stdout
    assert "route [BUILD]" in proc.stdout  # the selection is logged before launch
    # The verdict landed as a repo file the loop read back.
    assert list((repo / "docs" / "reviews" / "t1").glob("*-REVIEW-A-*.md"))


def test_prefer_map_routes_build_then_reviewer_heterogeneity_wins(managed_repo):
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd, "--prefer-map", "BUILD=PROVB-REV-1")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    models = _models(ctl)
    assert models[0] == "revb"  # phase preference beats enable-list order
    assert "builda" in models[1:]  # reviewer differs from the PROVB implementer


def test_invalid_prefer_map_id_fails_preflight(managed_repo):
    repo, ctl, cmd = managed_repo
    proc = _loop(repo, cmd, "--prefer-map", "BUILD=bad id")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "prefer-map [BUILD]" in proc.stderr


def test_review_policy_2_schedules_two_providers(managed_repo):
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("2\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    models = _models(ctl)
    # Two reviewers, two providers, both differing from the implementer's.
    assert "revb" in models and "revc" in models
    assert list((repo / "docs" / "reviews" / "t1").glob("*-REVIEW-B-*.md"))
    # The advisory scoreboard recorded the round.
    assert (repo / "docs" / "reviews" / "t1" / "scoreboard.txt").exists()


def test_review_policy_0_schedules_no_reviewer(managed_repo):
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    models = _models(ctl)
    assert "revb" not in models and "revc" not in models
    assert not (repo / "docs" / "reviews").exists()


def test_reviewer_prompt_is_redacted_by_construction(managed_repo):
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    # Isolate exactly the revb reviewer prompt (up to the next session entry).
    rev_block = prompts.split("=== revb ===\n", 1)[1].split("\n=== ", 1)[0]
    # The reviewer got the independent-review framing.
    assert "INDEPENDENT reviewer" in rev_block
    # Redaction by construction: the reviewer prompt must NOT carry the driver
    # resume prompt (the implementer's self-assessment surface).
    assert "resume from docs/status.md Current State" not in rev_block
    assert "assume no human is watching" not in rev_block


def test_reviewer_prompt_carries_requirement_consistency_sweep(managed_repo):
    # Option A (WI-084): when a diff changes requirement rows, the reviewer is
    # directed to sweep them (new AND historical) for contradiction/overlap and
    # flag wording that sharper SN/SR/TC language would clarify. Assert the
    # standing directive rides the deployed reviewer prompt.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    rev_block = prompts.split("=== revb ===\n", 1)[1].split("\n=== ", 1)[0]
    assert "contradiction" in rev_block
    assert "SN/SR/TC" in rev_block
    assert "status.md prose that contradicts a declared policy" in rev_block


def test_reviewer_prompt_carries_adversarial_clauses(managed_repo):
    # WI-241: the embedded reviewer prompt gained three field-proven adversarial
    # clauses (drive the real shipped paths, severity-ordered failure classes,
    # verdict discipline). Assert each rides the DEPLOYED prompt by a fragment
    # match (not full-text equality — no brittleness), and that the pre-existing
    # redaction sentence + verdict machine line survived byte-for-byte.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    rev_block = prompts.split("=== revb ===\n", 1)[1].split("\n=== ", 1)[0]
    # Clause 1 — drive the real shipped code paths.
    assert "REAL shipped code paths" in rev_block
    assert "primitive probes" in rev_block
    # Clause 2 — name and hunt the worst failure classes first, severity-ordered.
    assert "worst failure classes THIS change admits" in rev_block
    assert "severity-ordered" in rev_block
    # Clause 3 — verdict discipline: tried-and-failed, Done-when coverage, and
    # regression tests that fail on the pre-fix behavior.
    assert "tried to break it" in rev_block
    assert "UNCOVERED" in rev_block
    assert "fails on the pre-fix behavior" in rev_block
    # The load-bearing bones are byte-unchanged: the redaction sentence and the
    # verdict machine line ride the deployed prompt exactly.
    assert (
        "a leaked self-assessment collapses review finding-rates several-fold"
        in rev_block
    )
    assert "VERDICT: APPROVE|CHANGES-REQUESTED findings=N" in rev_block


def test_prompt_map_slots_a_custom_reviewer_template(managed_repo):
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    tmpl = repo / "docs" / "prompts" / "rev.md"
    tmpl.parent.mkdir(parents=True)
    tmpl.write_text(
        "CUSTOM-REVIEW-MARKER — write your verdict.\nWrite your verdict to {verdict}\n",
        encoding="utf-8",
    )
    proc = _loop(repo, cmd, "--prompt-map", "REVIEW-A=docs/prompts/rev.md")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    assert "CUSTOM-REVIEW-MARKER" in prompts  # the mapped template was used
    assert "prompt-map [REVIEW-A]" in proc.stdout  # surfaced in the banner


def test_prompt_map_missing_file_fails_preflight(managed_repo):
    repo, ctl, cmd = managed_repo
    proc = _loop(repo, cmd, "--prompt-map", "REVIEW-A=docs/prompts/nope.md")
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "prompt-map [REVIEW-A]" in proc.stderr


def test_enabled_id_not_in_registry_fails_preflight(managed_repo):
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "agents-enabled").write_text("GHOST-MODEL-9\n", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "not a row in docs/agents.toml" in proc.stderr


def test_two_top_tier_failures_page_the_human(managed_repo):
    # Strong-tier BUILD + reviewer, both rounds CHANGES-REQUESTED -> the
    # shared-failure regime pages the human; under attended the loop stops
    # NEEDS-HUMAN (exit 7).
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    # The worker pins the BUILD tier from the WI row (WI-181), so the row —
    # not just the tier-map — must declare strong for a top-tier build. Re-writing
    # the id replaces its spec file in docs/work/ (the registry's one home).
    write_wi_registry(repo, [_wi_201_row("strong")])
    (ctl / "verdict_body.txt").write_text(
        "- [MAJOR] work.txt:1 -> broken -> fix -> @owner\n"
        "VERDICT: CHANGES-REQUESTED findings=1\n",
        encoding="utf-8",
    )
    proc = _loop(repo, cmd, "--tier-map", "BUILD=strong,REVIEW-A=strong")
    assert proc.returncode == 7, proc.stdout + proc.stderr
    assert "PAGE-HUMAN" in proc.stdout
    assert "top-tier review failures" in proc.stdout  # the shared-failure regime
    # A worker never writes run-state (WI-210): its exit code is the page
    # and the dispatcher generates the root file.
    assert not (repo / "docs" / "run-state").exists()


def test_changes_requested_rework_finding_reaches_the_next_build(managed_repo):
    # WI-170 / WI-210: a CHANGES-REQUESTED review round sets the worker's
    # assignment-scoped rework state (never a lane docs/rework-wi file — that
    # pointer is retired with the serial driver); the next build session's
    # prompt embeds the finding so the rework happens before new work.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    (ctl / "verdict_body.txt").write_text(
        "- [MAJOR] work.txt:1 -> broken -> fix -> @owner\n"
        "VERDICT: CHANGES-REQUESTED findings=1\n",
        encoding="utf-8",
    )
    proc = _loop(repo, cmd, "--max-iterations", "4")
    assert proc.returncode in (6, 7), proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    assert "REWORK FINDING" in prompts  # the worker-prompt embed
    assert "an unhandled boundary condition" in prompts or "broken" in prompts
    assert not (repo / "docs" / "rework-wi").exists()  # the file is retired


def test_absent_enable_list_keeps_legacy_behavior(managed_repo):
    # No agents-enabled -> routing off -> the base --agent-cmd runs and NO review
    # is scheduled (the never-breaking guarantee; managed banner absent).
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "agents-enabled").unlink()
    (ctl / "done_after").write_text("1", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "routing: docs/agents-enabled present" not in proc.stdout
    assert "dispatch: review-policy" not in proc.stdout
    assert not (repo / "docs" / "reviews").exists()


def test_no_routable_model_pages_with_pool_context(managed_repo):
    # WI-109: the NEEDS-HUMAN "no routable model" banner lists the enabled pool
    # with each row's Notes — so an exhausted/misconfigured pool tells the human
    # what to DO (here: the opencode sign-in hint). Staged by enabling ONLY a
    # weak row while BUILD routes medium: select() finds nothing at tier+.
    repo, ctl, cmd = managed_repo
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(
            [
                [
                    "Id",
                    "Family",
                    "Model",
                    "Version",
                    "Tier",
                    "CmdTemplate",
                    "Env",
                    "Notes",
                ],
                [
                    "OPENAI-LUNA",
                    "OPENAI",
                    "gpt-5.6-luna",
                    "5.6",
                    "weak",
                    cmd,  # launchable (preflight checks it) — just never routable
                    "",
                    "sign in: opencode auth login",
                ],
            ]
        )
    (repo / "docs" / "agents-enabled").write_text("OPENAI-LUNA\n", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 7, proc.stdout + proc.stderr
    assert "no routable model" in proc.stdout
    assert "enabled pool" in proc.stdout
    assert "sign in: opencode auth login" in proc.stdout
    # A worker never writes run-state (WI-210): the exit code pages the
    # dispatcher, which generates the root file.
    assert not (repo / "docs" / "run-state").exists()


def test_preflight_missing_cli_carries_notes_hint(managed_repo):
    # WI-109: a registry row whose CmdTemplate CLI is absent fails preflight
    # (unchanged) — now WITH the row's Notes install/sign-in hint appended.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "agents.csv").write_text(
        "Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes\n"
        "OPENAI-SOL,OPENAI,gpt-5.6-sol,5.6,strong,"
        "definitely-not-a-cli-93135 run {prompt},,"
        "install: npm i -g opencode-ai; then: opencode auth login\n",
        encoding="utf-8",
    )
    (repo / "docs" / "agents-enabled").write_text("OPENAI-SOL\n", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 2, proc.stdout + proc.stderr
    assert "is not on PATH" in proc.stderr
    assert "install: npm i -g opencode-ai" in proc.stderr


# --- WI-080 Slice A golden net: the escalation + cool-and-reroute transitions --
# These pin observable behavior (route lines / models.txt / exit codes / verdict
# files) of the serial-loop transitions ahead of a behavior-preserving decompose.


def test_changes_requested_swaps_implementer_family(managed_repo):
    # Two consecutive medium-tier CHANGES-REQUESTED rounds -> agent_route.escalate
    # returns swap-implementer (a non-top tier, so the shared-failure page never
    # fires first). The loop applies impl_exclude and the NEXT build routes a
    # DIFFERENT Family (the PROVA implementer -> a PROVB one). Build cadence:
    # sessions 1/3 build PROVA, 2/4 review CHANGES-REQUESTED, 5 is the swapped
    # build (done_after=3 ends the run there).
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "verdict_body.txt").write_text(CHANGES_REQUESTED_BODY, encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    # Cadence: b1(trailer) r1(CR) b2 r2(CR -> swap) b3(swapped) — the budget
    # ends the run there (a perpetually CHANGES-REQUESTED train never DONEs).
    proc = _loop(repo, cmd, "--max-iterations", "5")
    assert proc.returncode == 6, proc.stdout + proc.stderr
    assert "escalate: swap-implementer" in proc.stdout
    builds = _routes(proc.stdout, "BUILD")
    # First build routed the PROVA implementer; the post-swap build a PROVB one.
    assert "PROVA-BUILD-1" in builds[0]
    assert "PROVB-REV-1" in builds[-1]
    assert "PROVA" not in builds[-1]  # a genuinely different Family, not PROVA


def test_escalation_tiers_up_after_swap(managed_repo):
    # One CHANGES-REQUESTED round beyond the swap -> escalate returns tier-up; the
    # loop sets impl_tier_override=strong (tier-up-never-down) and the next BUILD
    # routes the strong-tier registry row at the strong tier. Only a same-family
    # strong row is enabled, so the pick is the DEGRADED PROVA-STRONG-1 — the tier
    # is the observable that matters. done_after=4 ends the run on that build.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "verdict_body.txt").write_text(CHANGES_REQUESTED_BODY, encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    # Cadence: b1(trailer) r1(CR) b2 r2(CR -> swap) b3 r3(CR -> tier-up) b4
    # at strong — the budget ends the run on that build.
    proc = _loop(repo, cmd, "--max-iterations", "7")
    assert proc.returncode == 6, proc.stdout + proc.stderr
    assert "escalate: swap-implementer" in proc.stdout
    assert "escalate: tier-up" in proc.stdout
    builds = _routes(proc.stdout, "BUILD")
    assert "PROVA-STRONG-1" in builds[-1]  # the strong-tier row
    assert "[strong]" in builds[-1]  # routed at the strong tier, never dropped
    assert "stronga" in _models(ctl)  # and actually launched


def test_managed_rate_limit_cools_and_reroutes(managed_repo):
    # A managed BUILD session that emits a rate-limit signal must NOT exit WAITING:
    # the managed branch cools that model and CONTINUES (unlike the legacy WAITING
    # exit). The next session re-routes to the other enabled same-tier family and
    # the run finishes DONE.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8")  # build-only
    (ctl / "fail_model").write_text("builda", encoding="utf-8")
    (ctl / "fail_mode").write_text("limit", encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    (repo.parent / "fake.py").write_text(FAKE_FIRST_FAILS, encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr  # DONE, not EXIT_WAITING(5)
    assert "PROVA-BUILD-1 rate-limited; cooled" in proc.stdout
    assert "re-routing" in proc.stdout
    assert "WAITING on a rate limit" not in proc.stdout  # never took the WAITING exit
    # builda hit the limit and was cooled; the run re-routed to the other family.
    assert _models(ctl) == ["builda", "revb"]


def test_review_no_verdict_cools_and_reroutes_same_phase(managed_repo):
    # A reviewer that writes NO verdict file is cooled and the SAME review phase is
    # re-dispatched to a different enabled reviewer next iteration; the round still
    # completes (a REVIEW-A verdict lands from the re-routed reviewer).
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "skip_verdict_model").write_text("revb", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    (repo.parent / "fake.py").write_text(FAKE_REVIEWER_SKIPS, encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PROVB-REV-1 review [REVIEW-A] wrote no verdict" in proc.stdout
    assert "re-routing" in proc.stdout
    reviews = _routes(proc.stdout, "REVIEW-A")
    assert len(reviews) >= 2  # the SAME phase was re-dispatched, not dropped
    assert "PROVC-REV-1" in reviews[-1]  # to a different enabled reviewer
    # The round completed: the re-routed reviewer's verdict landed as a repo file.
    assert list((repo / "docs" / "reviews" / "t1").glob("*-REVIEW-A-*.md"))
    assert "revc" in _models(ctl)


def test_managed_error_session_cools_and_reroutes(managed_repo):
    # A managed BUILD session that ERRORS (nonzero exit, no JSON) cools that model
    # and re-routes to the other enabled same-tier family the next iteration.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8")  # build-only
    (ctl / "fail_model").write_text("builda", encoding="utf-8")
    (ctl / "fail_mode").write_text("error", encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    (repo.parent / "fake.py").write_text(FAKE_FIRST_FAILS, encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "PROVA-BUILD-1 session outcome=ERROR" in proc.stdout
    assert "cooled" in proc.stdout and "re-routing" in proc.stdout
    assert _models(ctl) == ["builda", "revb"]


def test_review_unparseable_verdict_cools_and_reroutes_same_phase(managed_repo):
    # Repo-review 2026-07-21 H-1: a verdict FILE whose machine line doesn't
    # parse (a routine LLM garble — wrong keyword, no colon) is neither an
    # approval nor a burnable round. Fail closed exactly like a missing file:
    # cool the reviewer and re-route the SAME phase; the round then completes
    # via the other reviewer's parseable verdict.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    bodies = json.loads((ctl / "bodies.json").read_text(encoding="utf-8"))
    bodies["revb"] = (
        "- [MAJOR] work.txt:1 -> a real finding -> fix it -> @owner\n"
        "Approved, ship it! (no machine line)\n"
    )
    (ctl / "bodies.json").write_text(json.dumps(bodies), encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "verdict file has no parseable VERDICT line" in proc.stdout
    assert "re-routing" in proc.stdout
    reviews = _routes(proc.stdout, "REVIEW-A")
    assert len(reviews) >= 2  # the SAME phase re-dispatched, not consumed
    # The round completed via the re-routed reviewer's real verdict.
    assert "revc" in _models(ctl)
    assert list((repo / "docs" / "reviews" / "t1").glob("*-REVIEW-A-*.md"))


# (test_scheduler_and_gate_agree_on_reviewer_phases retired with the
# dispatcher's _required_phases at concurrency-restructure Phase 5 — the
# integrator's verdict gate reads the review-policy dial itself, test_integrate.)


# --- WI-264: win-stay routes live through the managed draw (M-34) ------------ #
# A rich REVIEW-A body outscores a sparse REVIEW-B, so the round's escalation
# names REVIEW-A's family as next_primary (win). The WI-263 weighted baseline
# would rotate the NEXT REVIEW-A draw to the other provider; the wiring must
# instead keep it on the winning family (win-STAY), OVERRIDING the weighted
# baseline. Proves the policy executes end-to-end through agent_loop's real
# draw/escalation path, not just the pure helpers.
# REVIEW-A's body anchors to work.txt:1 (the real line the fake writes) with a
# concrete, actionable fix -> higher substance; REVIEW-B's cites a non-existent
# line -> unanchored, lower substance. So the round's higher-substance family is
# REVIEW-A's (the win-stay primary). Both CHANGES-REQUESTED (forces a rework +
# a SECOND review round) and lexically distinct (no near-duplicate tripwire).
WINSTAY_ANCHORED = (  # REVIEW-A body: well-anchored -> the round's primary family
    "- [MAJOR] work.txt:1 -> the progress line is rewritten in place, so a "
    "crash between builds loses the prior step's marker -> append the step "
    "index instead of overwriting, and fsync before returning -> @owner\n"
    "VERDICT: CHANGES-REQUESTED findings=1\n"
)
WINSTAY_UNANCHORED = (  # REVIEW-B body: cites a line that does not exist (sparse)
    "- [MINOR] work.txt:42 -> a distant comment somewhere reads awkwardly to a "
    "reviewer skimming quickly -> consider softening the tone later -> @owner\n"
    "VERDICT: CHANGES-REQUESTED findings=1\n"
)


def _winstay_repo(tmp_path):
    """A managed repo with THREE distinct-family reviewers + a weighted enable
    list whose REVIEW rotation sends REVIEW-A to PROVB then PROVD across rounds —
    so win-stay keeping PROVB is observably different from the baseline."""
    repo = tmp_path / "repo"
    (repo / "docs" / "requirements").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    (repo / "docs" / "review-policy").write_text("2\n", encoding="utf-8")
    write_wi_registry(repo, [_wi_201_row("medium")])
    (repo / ".gitignore").write_text("out/\n", encoding="utf-8")
    _git(repo, "init")
    pin_autocrlf(repo)  # WI-461/WI-465; see conftest.pin_autocrlf
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")
    _git(repo, "checkout", "-q", "-b", "llm/train/t1")

    ctl = tmp_path / "control"
    ctl.mkdir()
    fake = tmp_path / "fake.py"
    fake.write_text(FAKE, encoding="utf-8")
    cmd = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    rows = [
        ["Id", "Family", "Model", "Version", "Tier", "CmdTemplate", "Env", "Notes"],
        ["PROVA-BUILD-1", "PROVA", "builda", "1", "medium", cmd, "", ""],
        ["PROVB-REV-1", "PROVB", "revb", "1", "medium", cmd, "", ""],
        ["PROVC-REV-1", "PROVC", "revc", "1", "medium", cmd, "", ""],
        ["PROVD-REV-1", "PROVD", "revd", "1", "medium", cmd, "", ""],
    ]
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(rows)
    # REVIEW weights: PROVB:PROVD = 1:2 rotates the REVIEW-A draw PROVB (ordinal 0)
    # then PROVD (ordinal 1); PROVC held out (0 = fallback-only).
    (repo / "docs" / "agents-enabled").write_text(
        "# preference order + per-phase draw weights\n"
        "PROVA-BUILD-1\n"
        "PROVB-REV-1 REVIEW=1\n"
        "PROVC-REV-1 REVIEW=0\n"
        "PROVD-REV-1 REVIEW=2\n",
        encoding="utf-8",
    )
    (ctl / "bodies.json").write_text(
        json.dumps(
            {
                "revb": WINSTAY_ANCHORED,  # REVIEW-A: the higher-substance primary
                "revd": WINSTAY_UNANCHORED,  # REVIEW-B: lower substance
                "revc": WINSTAY_UNANCHORED,
                "_default": WINSTAY_UNANCHORED,
            }
        ),
        encoding="utf-8",
    )
    # done_after=1: each build immediately signals DONE -> a review round; a
    # CHANGES-REQUESTED round reworks and DONEs again -> a SECOND review round,
    # which is where win-stay biases the REVIEW-A draw.
    (ctl / "done_after").write_text("1", encoding="utf-8")
    return repo, ctl, cmd


def test_winstay_biases_the_next_review_draw_over_the_weighted_baseline(
    tmp_path, monkeypatch
):
    # A low-but-producible margin threshold (bounded by 1.0; the pipeline emits
    # fractional margins — the impossible margin:3 of the old fixture is exactly
    # what left this policy dead, M-34). The anchored REVIEW-A body clears it.
    monkeypatch.setenv("AGENT_ROUTE_MARGIN", "0.05")
    repo, ctl, cmd = _winstay_repo(tmp_path)
    proc = _loop(repo, cmd, "--max-iterations", "12")
    out = proc.stdout + proc.stderr
    review_a = _routes(out, "REVIEW-A")
    assert len(review_a) >= 3, out  # rounds 1 (baseline), 2 (win-stay), 3 (shift)
    # Round 1 escalation recorded a WIN naming PROVB as next round's feedback.
    assert "PROVB leads next round's feedback" in out, out
    # Round-1 REVIEW-A drew PROVB as the weighted baseline's first pick (ordinal 0).
    assert "PROVB-REV-1" in review_a[0], review_a
    # Round-2 REVIEW-A: the weighted baseline (ordinal 1) would rotate to PROVD,
    # but win-stay OVERRIDES it back to the winning family PROVB. This is the
    # live-wiring bite: revert the draw/apply_decision wiring and this draw falls
    # back to PROVD (the ordinary weighted baseline).
    assert "PROVB-REV-1" in review_a[1], (
        "win-stay must keep round-2 REVIEW-A on the winner PROVB, "
        "not the weighted-baseline PROVD: {}".format(review_a)
    )
    # Round-3 REVIEW-A: the two-round CHANGES-REQUESTED streak swapped the
    # implementer (escalate returned next_primary=None), so win-stay is cleared
    # and the draw SHIFTS to the weighted baseline (ordinal 2 -> PROVD) — proving
    # the baseline genuinely rotates and round 2's PROVB was the override, not a
    # baseline that always picks PROVB.
    assert "PROVD-REV-1" in review_a[2], review_a


# --- WI-548 (the 2026-08-30 stall-guard plan): C2 / C5 / C7 -------------------

# A reviewer fake whose EVERY reviewer session writes no verdict while
# ctl/skip_all exists — the whole-ladder outage under test — and records each
# session's KIND so a resume's first session is observable. Builders behave
# like FAKE with done_after=2.
FAKE_REVIEWER_TOGGLE = r"""
import argparse, pathlib, re, subprocess, sys
ap = argparse.ArgumentParser()
ap.add_argument("--control", required=True)
ap.add_argument("--model", default="")
ap.add_argument("-p", "--prompt", default="")
args, _ = ap.parse_known_args()
ctl = pathlib.Path(args.control)
with open(str(ctl / "models.txt"), "a", encoding="utf-8") as fh:
    fh.write(args.model + "\n")
is_review = "Write your verdict to" in args.prompt
with open(str(ctl / "kinds.txt"), "a", encoding="utf-8") as fh:
    fh.write(("review" if is_review else "build") + "\n")


def commit(path, msg):
    subprocess.run(["git", "add", str(path)], check=True)
    subprocess.run(["git", "commit", "-q", "-m", msg], check=True)


m = re.search(r"Write your verdict to (\S+)", args.prompt)
if m:
    if (ctl / "skip_all").exists():
        sys.exit(0)  # the outage: NO reviewer writes a verdict
    vpath = pathlib.Path(m.group(1))
    vpath.parent.mkdir(parents=True, exist_ok=True)
    vpath.write_text("VERDICT: APPROVE findings=0\n", encoding="utf-8")
    commit(vpath, "review verdict")
    sys.exit(0)
cf = ctl / "builds.txt"
n = len(cf.read_text(encoding="utf-8").splitlines()) if cf.exists() else 0
with open(str(cf), "a", encoding="utf-8") as fh:
    fh.write("b\n")
pathlib.Path("work.txt").write_text("build " + str(n), encoding="utf-8")
if n + 1 >= 2:
    commit("work.txt", "build " + str(n) + "\n\nWI: WI-201")
else:
    commit("work.txt", "build " + str(n))
sys.exit(0)
"""


def _write_registry(repo, cmd, rows):
    table = [["Id", "Provider", "Model", "Version", "Tier", "CmdTemplate", "Notes"]]
    table += [[rid, fam, model, "1", tier, cmd, ""] for rid, fam, model, tier in rows]
    with open(
        str(repo / "docs" / "agents.csv"), "w", encoding="utf-8", newline=""
    ) as fh:
        csv.writer(fh).writerows(table)
    (repo / "docs" / "agents-enabled").write_text(
        "".join(rid + "\n" for rid, _f, _m, _t in rows), encoding="utf-8"
    )


def test_reviewer_outage_parks_review_owed_then_resume_draws_the_round(
    managed_repo, tmp_path
):
    # C1+C2 end to end: the build commits, every review draw fails, and the
    # run ends EXIT_REVIEW_OWED (9) with the lane's work committed and the
    # out/review-owed marker written — never a stall abort of finished work.
    # A relaunch (the dispatcher's resume) schedules the OWED ROUND first and
    # ends DONE once a reviewer answers.
    repo, ctl, cmd = managed_repo
    fake = tmp_path / "fake_toggle.py"
    fake.write_text(FAKE_REVIEWER_TOGGLE, encoding="utf-8")
    cmd2 = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    _write_registry(
        repo,
        cmd2,
        [
            ("PROVA-BUILD-1", "PROVA", "builda", "medium"),
            ("PROVB-REV-1", "PROVB", "revb", "medium"),
            ("PROVC-REV-1", "PROVC", "revc", "medium"),
        ],
    )
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "skip_all").write_text("on\n", encoding="utf-8")

    proc = _loop(repo, cmd2, "--stall-limit", "2")
    assert proc.returncode == 9, proc.stdout + proc.stderr
    assert "REVIEW OWED" in proc.stdout
    assert (repo / "out" / "review-owed").is_file()
    kinds = (ctl / "kinds.txt").read_text(encoding="utf-8").split()
    assert kinds[:2] == ["build", "build"]

    # The outage ends; the resumed worker owes the ROUND, not another build.
    (ctl / "skip_all").unlink()
    boundary = len(kinds)
    proc2 = _loop(repo, cmd2, "--stall-limit", "2")
    assert proc2.returncode == 0, proc2.stdout + proc2.stderr
    kinds2 = (ctl / "kinds.txt").read_text(encoding="utf-8").split()
    assert kinds2[boundary] == "review", kinds2
    assert not (repo / "out" / "review-owed").exists()


def test_single_family_pool_review_is_drawn_relaxed_and_recorded(managed_repo):
    # C5: with only one family enabled, the cross-family ladder is empty by
    # construction — the draw is legal, and now RECORDED: the verdict filename
    # carries -relaxed and the round line says heterogeneity=relaxed.
    repo, ctl, cmd = managed_repo
    _write_registry(
        repo,
        cmd,
        [
            ("PROVA-BUILD-1", "PROVA", "builda", "medium"),
            ("PROVA-REV-1", "PROVA", "reva", "medium"),
        ],
    )
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")

    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    relaxed = list((repo / "docs" / "reviews" / "t1").glob("*-REVIEW-A-*-relaxed.md"))
    assert relaxed, list((repo / "docs" / "reviews" / "t1").glob("*"))
    assert "heterogeneity=relaxed" in proc.stdout


def test_reviewer_prompt_renders_trunk_and_process_doc_slots(managed_repo):
    # C7: the brief's reading scope renders per repo — the trunk name and the
    # process-doc path are SLOTS resolved at composition (this fixture has no
    # docs/process.md, so the kit-master fallback renders), and the rendered
    # text carries the three-dot diff with its telemetry/generated exclusions.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("2", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    rev_block = prompts.split("=== revb ===\n", 1)[1].split("\n=== ", 1)[0]
    assert "{trunk}" not in rev_block and "{process_doc}" not in rev_block
    assert "git diff llm/train/t1...HEAD" in rev_block
    assert "':(exclude)docs/iteration'" in rev_block
    assert "project-trajectory/PROCESS.md" in rev_block
    # Round 2: the script directory is the same hazard — this fixture has no
    # scripts/ dir, so the kit's own directory renders; nothing literal.
    assert "{scripts}" not in rev_block
    assert "python project-trajectory/scripts/check.py --jobs 0" in rev_block


def test_review_owed_resume_keeps_the_relaxed_audit_trail(managed_repo, tmp_path):
    # Round 2 finding: a REVIEW OWED restart used to reconstruct only the
    # train range and the queue, so the resumed draw forgot the build's
    # family and a same-family reviewer wrote an UNMARKED verdict. The marker
    # now carries the family; on a single-family roster the resumed round is
    # drawn relaxed and RECORDED as such.
    repo, ctl, cmd = managed_repo
    fake = tmp_path / "fake_toggle_single.py"
    fake.write_text(FAKE_REVIEWER_TOGGLE, encoding="utf-8")
    cmd2 = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    _write_registry(
        repo,
        cmd2,
        [
            ("PROVA-BUILD-1", "PROVA", "builda", "medium"),
            ("PROVA-REV-1", "PROVA", "reva", "medium"),
        ],
    )
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "skip_all").write_text("on\n", encoding="utf-8")

    proc = _loop(repo, cmd2, "--stall-limit", "2")
    assert proc.returncode == 9, proc.stdout + proc.stderr
    marker = (repo / "out" / "review-owed").read_text(encoding="utf-8")
    assert "family = PROVA" in marker

    (ctl / "skip_all").unlink()
    proc2 = _loop(repo, cmd2, "--stall-limit", "2")
    assert proc2.returncode == 0, proc2.stdout + proc2.stderr
    relaxed = list((repo / "docs" / "reviews" / "t1").glob("*-REVIEW-A-*-relaxed.md"))
    assert relaxed, list((repo / "docs" / "reviews" / "t1").glob("*"))
    assert "heterogeneity=relaxed" in proc2.stdout


def test_review_owed_survives_a_failed_marker_write(managed_repo, tmp_path):
    # Round 3 finding: the marker write used to be swallowed, and a resumed
    # worker with no marker reported DONE ("review round approved") on
    # unreviewed work. Owed-ness now rides COMMITTED evidence: with the marker
    # path made unwritable (a directory sits on it), the run still parks
    # REVIEW OWED loudly, and the resumed worker still draws the round FIRST
    # and ends DONE only once a verdict names HEAD.
    repo, ctl, cmd = managed_repo
    fake = tmp_path / "fake_toggle_nomarker.py"
    fake.write_text(FAKE_REVIEWER_TOGGLE, encoding="utf-8")
    cmd2 = '"{}" "{}" --control "{}" --model {{model}} -p {{prompt}}'.format(
        sys.executable, fake, ctl
    )
    _write_registry(
        repo,
        cmd2,
        [
            ("PROVA-BUILD-1", "PROVA", "builda", "medium"),
            ("PROVB-REV-1", "PROVB", "revb", "medium"),
            ("PROVC-REV-1", "PROVC", "revc", "medium"),
        ],
    )
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "skip_all").write_text("on\n", encoding="utf-8")
    (repo / "out" / "review-owed").mkdir(parents=True)  # the write cannot succeed
    # The fixture's primary checkout IS the branch, so the merge-base default
    # is HEAD; a real lane worktree merge-bases to the claim commit. Name the
    # integration base the way the dispatcher's lane would resolve it.
    _commit_config(repo)  # the fixture's own review-policy write is NOT the lane's diff
    base = _git(repo, "rev-parse", "HEAD")

    proc = _loop(repo, cmd2, "--stall-limit", "2", "--base", base)
    assert proc.returncode == 9, proc.stdout + proc.stderr
    assert "could not be written" in proc.stderr
    assert (repo / "out" / "review-owed").is_dir()  # no marker survived

    (ctl / "skip_all").unlink()
    boundary = len((ctl / "kinds.txt").read_text(encoding="utf-8").split())
    proc2 = _loop(repo, cmd2, "--stall-limit", "2", "--base", base)
    assert proc2.returncode == 0, proc2.stdout + proc2.stderr
    assert "committed evidence" in proc2.stdout
    kinds2 = (ctl / "kinds.txt").read_text(encoding="utf-8").split()
    assert kinds2[boundary] == "review", kinds2


def test_default_base_is_the_merge_base_with_the_trunk(tmp_path):
    # Round 3 (WI-548): a resumed worker's default base used to be HEAD, so
    # its committed evidence read empty. In a lane WORKTREE the default is
    # now the merge-base with the primary checkout's branch — the claim
    # commit — while a single-checkout repo keeps HEAD.
    import subprocess as _sp

    trunk = tmp_path / "trunk"
    trunk.mkdir()
    _git(trunk, "init", "-q", "-b", "main")
    pin_autocrlf(trunk)
    _git(trunk, "config", "user.email", "t@example.com")
    _git(trunk, "config", "user.name", "T")
    (trunk / "seed.txt").write_text("seed\n", encoding="utf-8")
    _git(trunk, "add", "-A")
    _git(trunk, "commit", "-q", "-m", "seed")
    seed = _git(trunk, "rev-parse", "HEAD")
    lane = tmp_path / "lane"
    _sp.run(
        ["git", "-C", str(trunk), "worktree", "add", "-q", "-b", "wi-1", str(lane)],
        check=True,
        capture_output=True,
    )
    (lane / "work.txt").write_text("built\n", encoding="utf-8")
    _git(lane, "add", "-A")
    _git(lane, "commit", "-q", "-m", "build\n\nWI: WI-1")
    al = load_script("agent_loop")
    assert al.default_base(lane) == seed  # the lane: its claim commit
    assert al.default_base(trunk) == seed  # the primary: HEAD, as before
    built, _blocked = al.train_evidence(lane, al.default_base(lane))
    assert "WI-1" in built


# --- WI: MINOR-only refusals do not block routing (measured 2026-09-03/04) ----
#
# Four rounds refused a lane over a single `[MINOR]` finding each (WI-586 rounds
# 006 and 010, WI-590 round 013). Each refusal bought a rework session AND
# another round to land a wording nit the reviewer had not called a defect. The
# rule lives in `kitlib.verdict.effective_verdict`, and this is its ROUTING arm;
# the merge-gate arm is driven in tests/test_verdict_record.py.

MINOR_ONLY_BODY = (
    "- [MINOR] work.txt:1 -> a wording nit -> reword it -> @owner\n"
    "VERDICT: CHANGES-REQUESTED findings=1\n"
)
MINOR_AND_MAJOR_BODY = (
    "- [MINOR] work.txt:1 -> a wording nit -> reword it -> @owner\n"
    "- [MAJOR] work.txt:1 -> broken -> fix it -> @owner\n"
    "VERDICT: CHANGES-REQUESTED findings=2\n"
)
EMPTY_REFUSAL_BODY = "VERDICT: CHANGES-REQUESTED findings=0\n"


def _one_round(managed_repo, body, iterations="4"):
    """Run the loop to one completed review round whose verdict file is `body`."""
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    (ctl / "verdict_body.txt").write_text(body, encoding="utf-8")
    proc = _loop(repo, cmd, "--max-iterations", iterations)
    return repo, ctl, proc


def test_a_minor_only_refusal_routes_as_an_approve(managed_repo):
    repo, ctl, proc = _one_round(managed_repo, MINOR_ONLY_BODY)
    assert (
        "review round: CHANGES-REQUESTED with MINOR-only findings routed as "
        "APPROVE (1 findings carried)" in proc.stdout
    ), proc.stdout + proc.stderr
    assert "review round: merged=APPROVE" in proc.stdout
    # The consequence that costs the sessions: no rework is scoped, so no
    # further build session is spent re-running the harness for the nit.
    assert "REWORK FINDING" not in (ctl / "prompts.txt").read_text(encoding="utf-8")
    # THE RECORD IS NOT REWRITTEN — the reviewer's own word stands in the file
    # the gate will re-read at the merge slot.
    written = [
        p for p in (repo / "docs" / "reviews").rglob("*.md") if "REVIEW-A" in p.name
    ]
    assert written and all(
        "VERDICT: CHANGES-REQUESTED" in p.read_text(encoding="utf-8") for p in written
    )


def test_a_minor_beside_a_major_still_requests_changes(managed_repo):
    _repo, ctl, proc = _one_round(managed_repo, MINOR_AND_MAJOR_BODY)
    assert "MINOR-only findings routed as" not in proc.stdout
    assert "review round: merged=CHANGES-REQUESTED" in proc.stdout
    assert "REWORK FINDING" in (ctl / "prompts.txt").read_text(encoding="utf-8")


def test_a_refusal_with_no_findings_still_requests_changes(managed_repo):
    # A reviewer that refuses without naming anything is a DIFFERENT defect and
    # is deliberately left alone: promoting it would clear the round on nobody's
    # judgement.
    _repo, _ctl, proc = _one_round(managed_repo, EMPTY_REFUSAL_BODY)
    assert "MINOR-only findings routed as" not in proc.stdout
    assert "review round: merged=CHANGES-REQUESTED" in proc.stdout
