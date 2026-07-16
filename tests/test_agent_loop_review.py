"""Loop-side reviewer dispatch + docs/agents.csv routing (WI-059, S8). Managed
mode: the enable-list's presence turns on model routing + reviewer scheduling.
Exercised end-to-end against a fake agent that plays both implementer and
reviewer, so no test touches a real CLI. Absent files keep the legacy behavior
(covered byte-for-byte by test_agent_loop.py)."""

import csv
import subprocess
import sys

import pytest
from conftest import SCRIPTS, run_py

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
    commit("work.txt", "build progress " + str(n))
    done_after = (
        int((ctl / "done_after").read_text(encoding="utf-8"))
        if (ctl / "done_after").exists()
        else 999
    )
    if n + 1 >= done_after:
        pathlib.Path("docs/run-state").write_text("DONE", encoding="utf-8")
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
subprocess.run(["git", "commit", "-q", "-m", "build " + str(n)], check=True)
done_after = int(_read("done_after")) if _read("done_after") else 999
if n + 1 >= done_after:
    pathlib.Path("docs/run-state").write_text("DONE", encoding="utf-8")
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
    commit("work.txt", "build " + str(n))
    done_after = (
        int((ctl / "done_after").read_text(encoding="utf-8"))
        if (ctl / "done_after").exists()
        else 999
    )
    if n + 1 >= done_after:
        pathlib.Path("docs/run-state").write_text("DONE", encoding="utf-8")
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


@pytest.fixture
def managed_repo(tmp_path):
    """A git repo wired for managed routing: docs/agents.csv (all rows point at
    ONE fake, distinguished by Provider/Model/Tier) + docs/agents-enabled +
    run-phase=BUILD. Returns (repo, control-dir, base-template, cmd-template)."""
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    (repo / "docs" / "status.md").write_text(STATUS_MD, encoding="utf-8")
    (repo / "docs" / "run-phase").write_text("BUILD\n", encoding="utf-8")
    _git(repo, "init")
    _git(repo, "config", "user.email", "loop@example.com")
    _git(repo, "config", "user.name", "Loop Test")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "initial")

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


def _loop(repo, cmd, *extra):
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
    assert list((repo / "docs" / "reviews").glob("*-REVIEW-A.md"))


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
    assert list((repo / "docs" / "reviews").glob("*-REVIEW-B.md"))
    # The advisory scoreboard recorded the round.
    assert (repo / "docs" / "reviews" / "scoreboard.txt").exists()


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
    assert "not a row in docs/agents.csv" in proc.stderr


def test_two_top_tier_failures_page_the_human(managed_repo):
    # Strong-tier BUILD + reviewer, both rounds CHANGES-REQUESTED -> the
    # shared-failure regime pages the human; under attended the loop stops
    # NEEDS-HUMAN (exit 7).
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (ctl / "verdict_body.txt").write_text(
        "- [MAJOR] work.txt:1 -> broken -> fix -> @owner\n"
        "VERDICT: CHANGES-REQUESTED findings=1\n",
        encoding="utf-8",
    )
    proc = _loop(repo, cmd, "--tier-map", "BUILD=strong,REVIEW-A=strong")
    assert proc.returncode == 7, proc.stdout + proc.stderr
    assert "PAGE-HUMAN" in proc.stdout
    assert "top-tier review failures" in proc.stdout  # the shared-failure regime
    state = (repo / "docs" / "run-state").read_text(encoding="utf-8").splitlines()
    assert state[0].strip() == "NEEDS-HUMAN"
    assert state[1].startswith("ask: review escalation")  # WI-127 ask line


def test_changes_requested_rework_scope_is_honored_and_clears_on_approve(managed_repo):
    # WI-170 / WI-180: a CHANGES-REQUESTED review keeps docs/rework-wi on the
    # reviewed WI; the next build gets a REWORK OVERRIDE prompt, and an APPROVE of
    # that scope clears it. next-wi is retired, so the session's claimed scope is
    # seeded via rework-wi here — the dispatcher supplies the explicit --wi
    # assignment in Slice C.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("1\n", encoding="utf-8")
    (repo / "docs" / "rework-wi").write_text("WI-OLD\n", encoding="utf-8")
    (ctl / "verdict_body.txt").write_text(
        "- [MAJOR] work.txt:1 -> broken -> fix -> @owner\n"
        "VERDICT: CHANGES-REQUESTED findings=1\n",
        encoding="utf-8",
    )
    first = _loop(repo, cmd, "--max-iterations", "2")
    assert first.returncode == 6, first.stdout + first.stderr
    assert (repo / "docs" / "rework-wi").read_text(encoding="utf-8").strip() == "WI-OLD"

    (ctl / "verdict_body.txt").write_text(
        "VERDICT: APPROVE findings=0\n", encoding="utf-8"
    )
    second = _loop(repo, cmd, "--max-iterations", "2")
    assert second.returncode == 6, second.stdout + second.stderr
    prompts = (ctl / "prompts.txt").read_text(encoding="utf-8")
    assert "REWORK OVERRIDE: docs/rework-wi names WI-OLD" in prompts
    assert not (repo / "docs" / "rework-wi").exists()


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
    state = (repo / "docs" / "run-state").read_text(encoding="utf-8").splitlines()
    assert state[0].strip() == "NEEDS-HUMAN"
    assert state[1].startswith("ask: no routable model")  # WI-127 ask line


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
    (ctl / "done_after").write_text("3", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
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
    (ctl / "done_after").write_text("4", encoding="utf-8")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
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
    assert list((repo / "docs" / "reviews").glob("*-REVIEW-A.md"))
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
