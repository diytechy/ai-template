"""The agent-neutral pre-commit hook (Thread 0b).

The hook is a thin POSIX wrapper around the kit's fast process checks, so we test
its *underlying logic* directly (run the same checks the hook runs) rather than
shelling out to `git commit`. Where a POSIX shell is available we also run the
hook script end-to-end to confirm the wiring.
"""

import json
import os
import shutil
import subprocess

from conftest import (
    KIT,
    LLRS,
    make_minimal_project,
    pin_autocrlf,
    process_key,
    run_py,
    set_process_key,
    skip_without_env_gates,
    write_wi_registry,
)
from kitlib import stage as kitstage

HOOK = ".githooks/pre-commit"


def set_dial(scaffold, section, key, value):
    """Write a policy dial AND regenerate `docs/stage` — the pair a real repo
    performs, so a hook test reds on the thing under test and not on setup.

    `docs/process.toml` is a DECLARED derivation input (`kitlib/stage.py`
    DECLARED_INPUTS), so writing ANY dial changes the stage fingerprint and the
    commit floor's `derived-stage` step then correctly reports the committed
    record as stale. That is deliberate (WI-498 slice 1: the fingerprint catches
    staleness a value comparison cannot), and it is why the re-sync recipe
    re-keys the dial BEFORE regenerating. Fixtures that write a dial and then run
    the hook must do the same or they fail two steps early, with the real
    assertion never reached — which is exactly how these tests failed at the
    slice-5 close, silently, in a module the smoke tier does not carry."""
    set_process_key(scaffold, section, key, value)
    run_py(["scripts/derive_stage.py", "--root", "."], cwd=scaffold)


def test_bootstrap_copies_pre_commit_hook(scaffold):
    hook = scaffold / HOOK
    assert hook.exists(), "bootstrap must copy the pre-commit hook to .githooks/"
    assert hook.read_text(encoding="utf-8").startswith("#!/bin/sh")


def test_hook_checks_pass_on_clean_project(scaffold):
    # The stdlib integrity check the hook always runs must pass on a fully
    # traced project (the hook's "green commit" path). (The gen_arch_map
    # --check arm retired at WI-455 with the committed map itself.)
    make_minimal_project(scaffold)
    trace = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert trace.returncode == 0, trace.stdout + trace.stderr


def test_hook_floor_no_longer_runs_the_retired_arch_map_step(scaffold):
    # WI-455: the committed docs/architecture.md is not scaffolded and the
    # arch-map step is gone from check.py, so the hook's batched floor must
    # not name it — a named-but-unknown step would fail every commit.
    hook_text = (scaffold / HOOK).read_text(encoding="utf-8")
    line = next(
        ln
        for ln in hook_text.splitlines()
        if "--run-steps" in ln and ln.strip().startswith('"$PY"')
    )
    assert "arch-map" not in line
    assert "okf" in line and "trajectory-map" in line


def test_hook_trajectory_map_step(scaffold):
    # THREAD_52_REVIEW.md F2: the hook runs the trajectory-dashboard freshness
    # step (delegated, like arch-map) so a registry edit that stales
    # docs/trajectory.html is caught at commit, not first in CI. The floor rule:
    # vacuous for a repo that never adopted the layer; with real work items a
    # missing/stale dashboard blocks, actionably; regenerating turns it green.
    make_minimal_project(scaffold)
    # Non-adopter: the scaffolded placeholder-only registry passes vacuously.
    ok = run_py(["scripts/check.py", "--run-step", "trajectory-map"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    # Adopter with a real work item and no generated dashboard: blocked. The
    # registry's one home is `docs/work/` spec files (status = directory), so a
    # real item is a spec beside the inert scaffolded `-000` example.
    real = ["WI-001", "Real work", "core", "", "", "queued", "a real row"]
    write_wi_registry(scaffold, [real])
    stale = run_py(["scripts/check.py", "--run-step", "trajectory-map"], cwd=scaffold)
    assert stale.returncode != 0, "a missing dashboard over real WIs must block"
    assert "STALE" in (stale.stdout + stale.stderr)
    # Regenerate: the same step goes green.
    regen = run_py(["scripts/gen_trajectory.py"], cwd=scaffold)
    assert regen.returncode == 0, regen.stdout + regen.stderr
    ok = run_py(["scripts/check.py", "--run-step", "trajectory-map"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    # The opt-out stays free: `off` silences the step even with a stale dashboard.
    write_wi_registry(
        scaffold,
        [real, ["WI-002", "More work", "core", "", "WI-001", "queued", "stales it"]],
    )
    set_process_key(scaffold, "checks", "trajectory_check", False)
    ok = run_py(["scripts/check.py", "--run-step", "trajectory-map"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    # And the hook script itself carries the delegated step (batched).
    hook_text = (scaffold / HOOK).read_text(encoding="utf-8")
    assert "--run-steps" in hook_text and "trajectory-map" in hook_text


def test_hook_skills_sync_step(scaffold):
    # S7: the hook runs the cross-agent skill-sync freshness step (delegated to
    # check.py, like arch-map/okf). In a scaffold the kit-only gen_skills_index
    # isn't beside check.py, so the step is a vacuous no-op that still passes —
    # never `check: no step named` — and the shipped hook carries the line.
    make_minimal_project(scaffold)
    ok = run_py(["scripts/check.py", "--run-step", "skills-sync"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    hook_text = (KIT / "hooks" / "pre-commit").read_text(encoding="utf-8")
    assert "--run-steps" in hook_text and "skills-sync" in hook_text


def test_hook_skills_index_and_prompt_catalog_steps(scaffold):
    # WI-427: the hook also runs the two generated-artifact freshness steps that
    # SN-010 declares and nothing enforced — skills/INDEX.csv vs the SKILL.md
    # frontmatter, and prompts/CATALOG.md vs the shipped templates.
    #
    # A SCAFFOLD IS THE CASE THAT MATTERS HERE. Both generators are kit-only, so
    # downstream neither is beside check.py and both steps must degrade to a
    # vacuous no-op that still RESOLVES — the 130-REVIEW-A failure (`check: no
    # step named 'ratify-fresh'`, exit 1, every commit blocked for an adopter)
    # is the reason these are built-in steps rather than docs/stack.ini
    # `[step:]` sections. Their ability to actually go RED where the generator
    # IS present is pinned in tests/test_generated_freshness_wiring.py.
    make_minimal_project(scaffold)
    for step in ("skills-index", "prompt-catalog"):
        ok = run_py(["scripts/check.py", "--run-step", step], cwd=scaffold)
        assert ok.returncode == 0, ok.stdout + ok.stderr
        assert "no step named" not in (ok.stdout + ok.stderr)
    hook_text = (KIT / "hooks" / "pre-commit").read_text(encoding="utf-8")
    floor = [
        ln
        for ln in hook_text.splitlines()
        if "--run-steps" in ln and not ln.lstrip().startswith("#")
    ]
    assert (
        len(floor) == 1 and "skills-index" in floor[0] and "prompt-catalog" in floor[0]
    )


def test_hook_trajectory_step_is_the_ra_floor(scaffold):
    # S1: the hook runs `check.py --run-step trajectory` (the SSOT floor). It is
    # WARN-FIRST (gate=all): only R-A (Deliverable non-empty iff done) is a hard
    # error at commit — an incoherent WI handoff must block; the softer status.md
    # / SpecRef rules (R-B..R-E) warn here and gate only at DevStg-Tests+ (--strict).
    make_minimal_project(scaffold)

    def _wi_001(deliverable, specref):
        # One spec under docs/work/queued/ (the registry's one home; status is the
        # directory). Re-writing the id replaces its spec, so each state below is
        # the whole registry again, exactly as the CSV rewrites were.
        write_wi_registry(
            scaffold,
            [["WI-001", "Real", "core", "", "", "queued", deliverable, specref]],
        )

    # Non-adopter: the scaffolded placeholder-only registry passes vacuously.
    ok = run_py(["scripts/check.py", "--run-step", "trajectory"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    # R-A violation: an open WI carrying a filled Deliverable -> the step blocks.
    _wi_001("already filled", "")
    blocked = run_py(["scripts/check.py", "--run-step", "trajectory"], cwd=scaffold)
    assert blocked.returncode != 0, "an open WI with a Deliverable must block (R-A)"
    assert "R-A" in (blocked.stdout + blocked.stderr)
    # A dangling SpecRef alone (R-E) is warn-first at the hook -> does NOT block.
    _wi_001("", "docs/specs/WI-404.md")
    warn = run_py(["scripts/check.py", "--run-step", "trajectory"], cwd=scaffold)
    assert warn.returncode == 0, "R-E must warn, not block, at the commit floor"
    # Coherent open row (empty Deliverable + resolvable SpecRef) -> green.
    (scaffold / "docs" / "specs").mkdir(parents=True, exist_ok=True)
    (scaffold / "docs" / "specs" / "WI-001.md").write_text("# spec\n", "utf-8")
    _wi_001("", "docs/specs/WI-001.md")
    ok = run_py(["scripts/check.py", "--run-step", "trajectory"], cwd=scaffold)
    assert ok.returncode == 0, ok.stdout + ok.stderr
    # The shipped hook script carries both the floor step (batched) and the
    # staged warn.
    hook_text = (KIT / "hooks" / "pre-commit").read_text(encoding="utf-8")
    assert "--run-steps" in hook_text and "trajectory" in hook_text
    assert "check_trajectory.py" in hook_text and "--staged" in hook_text


def test_run_steps_gate_promotes_the_warn_first_floor(scaffold):
    # WI-355, the behavioral half of test_step_gate_honours_an_explicit_gate: the
    # two halves must be pinned together, because the fix is only correct if BOTH
    # hold. Same R-E fixture as test_hook_trajectory_step_is_the_ra_floor (a
    # dangling SpecRef — warn-first at the commit floor, an ERROR under --strict).
    make_minimal_project(scaffold)

    def _wi_001(specref):
        write_wi_registry(
            scaffold, [["WI-001", "Real", "core", "", "", "queued", "", specref]]
        )

    _wi_001("docs/specs/WI-404.md")
    # No --gate (what the pre-commit hook passes): the floor stays warn-first even
    # though the scaffold's own derived state declares a real rung — a defaulted
    # --gate must not be resolved through it, or every commit would be held to
    # that rung. RE-KEYED at WI-498 slice 5, which retired `docs/gate` and its
    # three-value BAR: the derived carrier is now `docs/stage`, read through the
    # carrier's own parser rather than by scraping a bare line. What matters here
    # is only that the declared rung is ABOVE the warn-first floor.
    #
    # THE FRAME HAS TO GO FIRST, and that is not fixture noise — it is slices 2
    # and 3's banked finding driven here. `boundary_incomplete` applies whenever
    # `external.toml` EXISTS, and the scaffold ships one carrying no ratified
    # crossing, so a minimal project reads `DevStg-Boundary` and FLOORS to
    # `DevStg-Reqs` — the floor itself, which would make this test vacuous
    # (nothing is above the warn-first floor, so a defaulted `--gate` resolving
    # through the derived state could not be distinguished from one that does
    # not). Declaring no frame is a legal adopter shape and is what the
    # at-or-above fixtures use for the same reason; frame-free, this spine reads
    # `DevStg-Impl`, which is genuinely above the floor.
    for frame in ("external", "components"):
        for suffix in (".toml", ".csv"):
            carrier = scaffold / "docs" / "requirements" / (frame + suffix)
            if carrier.exists():
                carrier.unlink()
    run_py(["scripts/derive_stage.py", "--root", "."], cwd=scaffold)
    stage_text = (scaffold / "docs" / "stage").read_text(encoding="utf-8")
    declared = kitstage.parse(stage_text)
    assert declared and declared["stage"] == "DevStg-Impl", declared
    warn = run_py(["scripts/check.py", "--run-steps", "trajectory"], cwd=scaffold)
    assert warn.returncode == 0, "R-E must warn, not block, at the commit floor"
    # Explicitly asking for the DevStg-Impl bar really gates it (the WI-354 session read
    # 18/18 PASS from this command while two real DevStg-Impl errors were live).
    gated = run_py(
        ["scripts/check.py", "--gate", "DevStg-Impl", "--run-steps", "trajectory"],
        cwd=scaffold,
    )
    assert gated.returncode != 0, (
        "--gate DevStg-Impl --run-steps must run the --strict command"
    )
    assert "R-E" in (gated.stdout + gated.stderr)
    # Not a blanket "--gate DevStg-Impl always fails": repair the SpecRef and it goes green.
    (scaffold / "docs" / "specs").mkdir(parents=True, exist_ok=True)
    (scaffold / "docs" / "specs" / "WI-001.md").write_text("# spec\n", "utf-8")
    _wi_001("docs/specs/WI-001.md")
    ok = run_py(
        ["scripts/check.py", "--gate", "DevStg-Impl", "--run-steps", "trajectory"],
        cwd=scaffold,
    )
    assert ok.returncode == 0, ok.stdout + ok.stderr


def test_hook_blocks_duplicate_id_but_not_orphan(scaffold):
    # The hook's traceability command is --strict-integrity: a duplicated id is
    # wrong at any stage and must block, but an orphan is a DevStg-Tests+ *gate* criterion
    # (a mid-DevStg-Reqs registry legitimately has SRs with no LLR/TC) and must NOT block
    # a commit — the regression that made the hook wedge every DevStg-Reqs-stage commit.
    make_minimal_project(scaffold)
    llr = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr.write_text(LLRS + LLRS.splitlines()[1] + "\n", encoding="utf-8")
    trace = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert trace.returncode != 0, "duplicate LLR id must fail --strict-integrity"

    # Restore, then simulate end-of-DevStg-Reqs: an SR exists, its LLR/TC don't yet.
    llr.write_text(LLRS.splitlines()[0] + "\n", encoding="utf-8")
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status\n",
        encoding="utf-8",
    )
    strict = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert strict.returncode != 0, "orphans still fail the gate-scoped --strict"
    floor = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert floor.returncode == 0, (
        "a DevStg-Reqs-stage registry must stay committable: "
        + floor.stdout
        + floor.stderr
    )


def test_hook_runs_end_to_end_when_sh_available(scaffold):
    # Where a POSIX shell exists (Linux/macOS CI; Git Bash on Windows), run the
    # actual hook so its interpreter discovery + command wiring are exercised.
    # A pre-commit hook only ever runs inside a git repo (its step 3 secrets
    # floor reads the staged diff), so init one — the realistic footing.
    skip_without_env_gates("posix-shell", "git")
    sh = shutil.which("sh")
    make_minimal_project(scaffold)
    subprocess.run(["git", "init"], cwd=str(scaffold), capture_output=True)
    pin_autocrlf(scaffold)  # WI-461/WI-465; see conftest.pin_autocrlf
    ok = subprocess.run([sh, HOOK], cwd=str(scaffold), capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # Tamper with a generated artifact (the OKF bundle, since WI-455 retired
    # the committed arch map); the hook's batched floor must block the commit.
    (scaffold / "docs" / "okf" / "index.md").write_text(
        "# HAND-EDITED — should be rejected\n", encoding="utf-8"
    )
    blocked = subprocess.run(
        [sh, HOOK], cwd=str(scaffold), capture_output=True, text=True
    )
    assert blocked.returncode != 0, blocked.stdout + blocked.stderr


def test_hook_honors_kit_scripts_dir_override(scaffold):
    # WI-1.42: a repo whose harness is not at scripts/ (e.g. the kit's own
    # meta-repo, under project-trajectory/scripts/) points the shipped hook via
    # KIT_SCRIPTS_DIR, so one hook fits any layout. Positive: an explicit override
    # to the real dir runs green (the override branch produces a working
    # SCRIPTS_DIR); negative: a bogus override skips CLEARLY (a wrong override must
    # never silently pass as if the tree were clean).
    skip_without_env_gates("posix-shell", "git")
    sh = shutil.which("sh")
    make_minimal_project(scaffold)
    subprocess.run(["git", "init"], cwd=str(scaffold), capture_output=True)
    pin_autocrlf(scaffold)  # WI-461/WI-465; see conftest.pin_autocrlf

    ok = subprocess.run(
        [sh, HOOK],
        cwd=str(scaffold),
        capture_output=True,
        text=True,
        env=dict(os.environ, KIT_SCRIPTS_DIR="scripts"),
    )
    assert ok.returncode == 0, ok.stdout + ok.stderr

    bad = subprocess.run(
        [sh, HOOK],
        cwd=str(scaffold),
        capture_output=True,
        text=True,
        env=dict(os.environ, KIT_SCRIPTS_DIR="nope-not-here"),
    )
    assert bad.returncode == 0, bad.stdout + bad.stderr  # skip, not crash
    assert "cannot find" in bad.stderr.lower(), bad.stderr


def test_hook_skips_clearly_when_no_working_python3(scaffold):
    # SN-013 / SR-019: python3 may resolve on PATH yet exit nonzero (the Windows
    # Store app-execution alias). The hook probes by *running* a candidate, so it
    # must skip-or-report clearly, never crash. Shadow python3/python with fakes
    # that exit nonzero and confirm the hook exits 0 with a clear message.
    skip_without_env_gates("posix-shell", "git")
    sh = shutil.which("sh")
    make_minimal_project(scaffold)
    subprocess.run(["git", "init"], cwd=str(scaffold), capture_output=True)
    pin_autocrlf(scaffold)  # WI-461/WI-465; see conftest.pin_autocrlf
    fakebin = scaffold / "fakebin"
    fakebin.mkdir()
    for name in ("python3", "python"):
        cand = fakebin / name
        cand.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        cand.chmod(0o755)
    # Prepend the fakes so they shadow any real interpreter; keep the rest of PATH
    # so sh/git/coreutils stay available.
    env = dict(os.environ, PATH=str(fakebin) + os.pathsep + os.environ.get("PATH", ""))
    proc = subprocess.run(
        [sh, HOOK], cwd=str(scaffold), capture_output=True, text=True, env=env
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "not found" in proc.stderr.lower(), proc.stderr


def _shadow_python(scaffold):
    """A PATH prefix dir whose python3/python fakes exit nonzero (the Store-
    alias shape the hooks probe for) — sh/git/coreutils stay available."""
    fakebin = scaffold / "fakebin"
    fakebin.mkdir()
    for name in ("python3", "python"):
        cand = fakebin / name
        cand.write_text("#!/bin/sh\nexit 1\n", encoding="utf-8")
        cand.chmod(0o755)
    return dict(os.environ, PATH=str(fakebin) + os.pathsep + os.environ.get("PATH", ""))


def test_hook_fails_closed_when_privacy_on_but_no_python(scaffold):
    # M-42: the Python-less exit-0 skip must never silently drop a DECLARED
    # privacy policy — with docs/privacy-check `true` (parsed in pure sh, the
    # pre-push pattern) and no working python, the hook REFUSES the skip. The
    # privacy-off scaffold default keeps the free skip (previous test).
    skip_without_env_gates("posix-shell", "git")
    sh = shutil.which("sh")
    make_minimal_project(scaffold)
    subprocess.run(["git", "init"], cwd=str(scaffold), capture_output=True)
    pin_autocrlf(scaffold)  # WI-461/WI-465; see conftest.pin_autocrlf
    set_process_key(scaffold, "policies", "privacy_check", True)
    env = _shadow_python(scaffold)
    proc = subprocess.run(
        [sh, HOOK], cwd=str(scaffold), capture_output=True, text=True, env=env
    )
    assert proc.returncode != 0, "privacy-true + no python must FAIL CLOSED"
    assert "refusing to skip" in proc.stderr.lower(), proc.stderr


def test_commit_msg_hook_fails_closed_when_privacy_on_but_no_python(scaffold):
    # M-42, commit-msg twin: the message scan of a privacy-checked repo must
    # fail closed rather than skip when no working python is found.
    skip_without_env_gates("posix-shell", "git")
    sh = shutil.which("sh")
    make_minimal_project(scaffold)
    subprocess.run(["git", "init"], cwd=str(scaffold), capture_output=True)
    pin_autocrlf(scaffold)  # WI-461/WI-465; see conftest.pin_autocrlf
    (scaffold / "MSG.txt").write_text("an innocent message\n", encoding="utf-8")
    env = _shadow_python(scaffold)

    def run_msg_hook():
        return subprocess.run(
            [sh, ".githooks/commit-msg", "MSG.txt"],
            cwd=str(scaffold),
            capture_output=True,
            text=True,
            env=env,
        )

    # Privacy off (scaffold default): the skip stays free.
    ok = run_msg_hook()
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "not found" in ok.stderr.lower(), ok.stderr
    # Privacy declared true: fail closed with the named reason.
    set_process_key(scaffold, "policies", "privacy_check", True)
    blocked = run_msg_hook()
    assert blocked.returncode != 0, "privacy-true + no python must FAIL CLOSED"
    assert "refusing to skip" in blocked.stderr.lower(), blocked.stderr


def test_hook_secrets_floor_blocks_staged_key_with_privacy_off(scaffold):
    # Thread 44: the pre-commit hook now runs the always-on secrets floor for
    # every repo, so a staged credential is blocked before the commit exists —
    # even with the scaffolded privacy gate off — and the opt-out lifts it.

    skip_without_env_gates("posix-shell", "git")
    sh = shutil.which("sh")
    make_minimal_project(scaffold)

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=str(scaffold), capture_output=True, text=True
        )

    assert git("init").returncode == 0
    pin_autocrlf(scaffold)  # WI-461/WI-465; see conftest.pin_autocrlf
    git("config", "user.name", "Test User")
    git("config", "user.email", "someone@example.com")
    key = "-----BEGIN RSA " + "PRIVATE KEY-----\n"  # split so this line is not a match
    (scaffold / "cfg.txt").write_text(key, encoding="utf-8")
    assert git("add", "cfg.txt").returncode == 0

    blocked = subprocess.run(
        [sh, HOOK], cwd=str(scaffold), capture_output=True, text=True
    )
    assert blocked.returncode != 0, "a staged private key must block with privacy off"
    assert "private key header" in (blocked.stdout + blocked.stderr)

    # The opt-out lifts the floor for a repo that needs it.
    set_dial(scaffold, "policies", "secrets_scan", False)
    ok = subprocess.run([sh, HOOK], cwd=str(scaffold), capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr


def test_hook_privacy_author_guard(scaffold):
    # Identity->privacy reframe: with docs/privacy-check on, the hook's --author
    # step blocks a private (non-exempt) author before the commit exists and
    # passes an exempt no-reply one; the scaffolded default (privacy off) skips.

    skip_without_env_gates("posix-shell", "git")
    sh = shutil.which("sh")
    make_minimal_project(scaffold)

    def git(*args):
        return subprocess.run(
            ["git", *args], cwd=str(scaffold), capture_output=True, text=True
        )

    assert git("init").returncode == 0
    pin_autocrlf(scaffold)  # WI-461/WI-465; see conftest.pin_autocrlf
    git("config", "user.name", "Test User")
    git("config", "user.email", "real.person@gmail.com")

    def run_hook():
        return subprocess.run(
            [sh, HOOK], cwd=str(scaffold), capture_output=True, text=True
        )

    # The scaffolded default is privacy-check false: any identity passes.
    assert process_key(scaffold, "policies", "privacy_check") is False, (
        "scaffold must default privacy_check to false"
    )
    ok = run_hook()
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # privacy-check on + a private (non-exempt) author: a designed block.
    set_dial(scaffold, "policies", "privacy_check", True)
    blocked = run_hook()
    assert blocked.returncode != 0, "a private author must be blocked"
    assert "exempt allowlist" in blocked.stderr

    # An exempt no-reply author: green again.
    git("config", "user.email", "12345+user@users.noreply.github.com")
    ok = run_hook()
    assert ok.returncode == 0, ok.stdout + ok.stderr


def test_bootstrap_copies_commit_msg_hook(scaffold):
    hook = scaffold / ".githooks" / "commit-msg"
    assert hook.exists(), "bootstrap must copy the commit-msg hook to .githooks/"
    assert hook.read_text(encoding="utf-8").startswith("#!/bin/sh")


def test_commit_msg_hook_scans_message(scaffold):
    # The pile-up fix: pre-commit runs before the message exists, so the message
    # goes unscanned until push. The commit-msg hook closes the gap — git passes
    # the message file as $1 and a nonzero exit aborts the commit. The always-on
    # secrets floor scans every repo's message; the privacy layer adds its
    # classes only when docs/privacy-check is `true`.

    skip_without_env_gates("posix-shell", "git")
    sh = shutil.which("sh")
    make_minimal_project(scaffold)
    subprocess.run(["git", "init"], cwd=str(scaffold), capture_output=True)
    pin_autocrlf(scaffold)  # WI-461/WI-465; see conftest.pin_autocrlf
    HOOK_CM = ".githooks/commit-msg"

    def run_msg(text):
        msg = scaffold / "MSG.txt"
        msg.write_text(text, encoding="utf-8")
        return subprocess.run(
            [sh, HOOK_CM, "MSG.txt"], cwd=str(scaffold), capture_output=True, text=True
        )

    # Secrets floor (always on): a credential in the message body blocks.
    key = "-----BEGIN RSA " + "PRIVATE KEY-----"  # split so this line is not a match
    blocked = run_msg("add config\n\n" + key + "\n")
    assert blocked.returncode != 0, "a secret in the message must block"
    assert "private key header" in (blocked.stdout + blocked.stderr)

    # Privacy layer off (scaffold default): a private email in the message is a
    # privacy class, not a secret, so it passes.
    ok = run_msg("fix\n\nReported-by: real.person@gmail.com\n")
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # Privacy layer on: the same private email now blocks; the exempt no-reply
    # co-author trailer passes.
    set_process_key(scaffold, "policies", "privacy_check", True)
    blocked = run_msg("fix\n\nReported-by: real.person@gmail.com\n")
    assert blocked.returncode != 0, "a private email in the message must block when on"
    assert "exempt allowlist" in (blocked.stdout + blocked.stderr)
    ok = run_msg("fix\n\nCo-Authored-By: Claude <noreply@anthropic.com>\n")
    assert ok.returncode == 0, ok.stdout + ok.stderr


def test_optional_agent_hook_configs_are_valid_json():
    # The optional extras ship as real JSON the user can drop into .claude/.gemini.
    for name in ("claude.settings.json", "gemini.settings.json"):
        path = KIT / "agent-hooks" / name
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "hooks" in data, name + " must define a hooks block"
