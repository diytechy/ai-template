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

STATUS_MD = """# Status

## Current State

- **Open items:**
  - **Needs <human>**: OI-9 — a pending ask
"""


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
    assert (repo / "docs" / "run-state").read_text(
        encoding="utf-8"
    ).strip() == "NEEDS-HUMAN"


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
    assert (repo / "docs" / "run-state").read_text(
        encoding="utf-8"
    ).strip() == "NEEDS-HUMAN"


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


# --- per-WI BuildTier pin (WI-126) --------------------------------------------
# docs/next-wi names the WI the coordinator picks up next; that WI's BuildTier
# column overrides the BUILD phase default as the session's STARTING tier. The
# managed_repo registry carries a medium implementer (builda) and a strong one
# (stronga), so a pin is observable as the model the build session was handed.


def _write_next_wi(repo, wid):
    (repo / "docs" / "next-wi").write_text(
        "# the WI the coordinator picks up next (WI-126)\n{}\n".format(wid),
        encoding="utf-8",
    )


def _write_work_items(repo, rows):
    # A minimal work-items.csv the pin reads by name (WI-ID + BuildTier); rows is
    # a list of (wi-id, build-tier).
    req = repo / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    body = "\n".join("{},{}".format(w, t) for (w, t) in rows)
    (req / "work-items.csv").write_text(
        "WI-ID,BuildTier\n" + body + "\n", encoding="utf-8"
    )


def test_build_tier_pin_routes_the_build_session(managed_repo):
    # (a) pin honored: next-wi + a BuildTier=strong row routes BUILD to the
    # pinned tier's model (stronga), not the medium phase default (builda).
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    _write_work_items(repo, [("WI-200", "strong")])
    _write_next_wi(repo, "WI-200")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    models = _models(ctl)
    assert "stronga" in models and "builda" not in models, models
    assert "BuildTier pin WI-200 -> starting tier strong" in proc.stdout


def test_build_tier_pin_absent_is_unchanged_routing(managed_repo):
    # (b) pin absent: the BuildTier column exists but NO docs/next-wi pointer,
    # so it is never consulted — BUILD rides the medium default (builda),
    # byte-identical to today, and no pin line prints.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    _write_work_items(repo, [("WI-200", "strong")])  # pinnable, but unpinned
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    models = _models(ctl)
    assert "builda" in models and "stronga" not in models, models
    assert "BuildTier pin" not in proc.stdout


def test_build_tier_pin_bad_value_warns_and_falls_back(managed_repo):
    # (c) bad value: a BuildTier the tier vocabulary does not know is LOUD but
    # never fatal — a warning line to stdout, phase default still routes.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    _write_work_items(repo, [("WI-200", "turbo")])
    _write_next_wi(repo, "WI-200")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "is not one of" in proc.stdout
    assert "using the phase default" in proc.stdout
    models = _models(ctl)
    assert "builda" in models and "stronga" not in models, models


def test_build_tier_pin_unknown_wi_warns_and_falls_back(managed_repo):
    # (d) unknown WI id: docs/next-wi naming a WI with no registry row is the
    # same loud-fallback — warn to stdout, phase default routes, no crash.
    repo, ctl, cmd = managed_repo
    (repo / "docs" / "review-policy").write_text("0\n", encoding="utf-8")
    (ctl / "done_after").write_text("1", encoding="utf-8")
    _write_work_items(repo, [("WI-200", "strong")])
    _write_next_wi(repo, "WI-404")
    proc = _loop(repo, cmd)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "no such WI-ID row" in proc.stdout
    models = _models(ctl)
    assert "builda" in models and "stronga" not in models, models
