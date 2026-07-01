"""The agent-neutral pre-commit hook (Thread 0b).

The hook is a thin POSIX wrapper around the kit's fast process checks, so we test
its *underlying logic* directly (run the same checks the hook runs) rather than
shelling out to `git commit`. Where a POSIX shell is available we also run the
hook script end-to-end to confirm the wiring.
"""

import json
import shutil
import subprocess

from conftest import KIT, LLRS, make_minimal_project, run_py

HOOK = ".githooks/pre-commit"
ARCH = "docs/architecture.md"
MAP_BEGIN = "<!-- BEGIN GENERATED MODULE MAP -->"


def test_bootstrap_copies_pre_commit_hook(scaffold):
    hook = scaffold / HOOK
    assert hook.exists(), "bootstrap must copy the pre-commit hook to .githooks/"
    assert hook.read_text(encoding="utf-8").startswith("#!/bin/sh")


def test_hook_checks_pass_on_clean_project(scaffold):
    # The two stdlib checks the hook always runs must pass on a fully-traced,
    # freshly-mapped project (the hook's "green commit" path).
    make_minimal_project(scaffold)
    archmap = run_py(["scripts/gen_arch_map.py", "--check"], cwd=scaffold)
    assert archmap.returncode == 0, archmap.stdout + archmap.stderr
    trace = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert trace.returncode == 0, trace.stdout + trace.stderr


def test_hook_blocks_stale_generated_block(scaffold):
    # A hand-edited GENERATED region must be caught by gen_arch_map --check (the
    # hook's "protect the GENERATED regions" guarantee).
    make_minimal_project(scaffold)
    arch = scaffold / ARCH
    text = arch.read_text(encoding="utf-8")
    assert MAP_BEGIN in text
    arch.write_text(
        text.replace(MAP_BEGIN, MAP_BEGIN + "\nHAND-EDITED — should be rejected.\n"),
        encoding="utf-8",
    )
    archmap = run_py(["scripts/gen_arch_map.py", "--check"], cwd=scaffold)
    assert archmap.returncode != 0, "stale generated block must fail --check"


def test_hook_blocks_duplicate_id_but_not_orphan(scaffold):
    # The hook's traceability command is --strict-integrity: a duplicated id is
    # wrong at any stage and must block, but an orphan is a G2+ *gate* criterion
    # (a mid-G1 registry legitimately has SRs with no LLR/TC) and must NOT block
    # a commit — the regression that made the hook wedge every G1-stage commit.
    make_minimal_project(scaffold)
    llr = scaffold / "docs" / "requirements" / "low-level-requirements.csv"
    llr.write_text(LLRS + LLRS.splitlines()[1] + "\n", encoding="utf-8")
    trace = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert trace.returncode != 0, "duplicate LLR id must fail --strict-integrity"

    # Restore, then simulate end-of-G1: an SR exists, its LLR/TC don't yet.
    llr.write_text(LLRS.splitlines()[0] + "\n", encoding="utf-8")
    (scaffold / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Status\n",
        encoding="utf-8",
    )
    strict = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert strict.returncode != 0, "orphans still fail the gate-scoped --strict"
    floor = run_py(["scripts/trace.py", "--strict-integrity"], cwd=scaffold)
    assert floor.returncode == 0, (
        "a G1-stage registry must stay committable: " + floor.stdout + floor.stderr
    )


def test_hook_runs_end_to_end_when_sh_available(scaffold):
    # Where a POSIX shell exists (Linux/macOS CI; Git Bash on Windows), run the
    # actual hook so its interpreter discovery + command wiring are exercised.
    sh = shutil.which("sh")
    if not sh:
        import pytest

        pytest.skip("no POSIX shell on PATH")
    make_minimal_project(scaffold)
    ok = subprocess.run([sh, HOOK], cwd=str(scaffold), capture_output=True, text=True)
    assert ok.returncode == 0, ok.stdout + ok.stderr

    # Tamper with the generated block; the hook must now block the commit.
    arch = scaffold / ARCH
    arch.write_text(
        arch.read_text(encoding="utf-8").replace(
            MAP_BEGIN, MAP_BEGIN + "\nHAND-EDITED — should be rejected.\n"
        ),
        encoding="utf-8",
    )
    blocked = subprocess.run(
        [sh, HOOK], cwd=str(scaffold), capture_output=True, text=True
    )
    assert blocked.returncode != 0, blocked.stdout + blocked.stderr


def test_optional_agent_hook_configs_are_valid_json():
    # The optional extras ship as real JSON the user can drop into .claude/.gemini.
    for name in ("claude.settings.json", "gemini.settings.json"):
        path = KIT / "agent-hooks" / name
        data = json.loads(path.read_text(encoding="utf-8"))
        assert "hooks" in data, name + " must define a hooks block"
