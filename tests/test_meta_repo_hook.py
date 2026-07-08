"""The meta-repo's own pre-commit floor stays in step with the shipped hook.

This repo dogfoods the kit's process floor, but its harness lives under
`project-trajectory/scripts/` (not `scripts/`), so it carries a layout-adapted
copy of the shipped pre-commit at `.githooks/pre-commit`. That hand copy can
silently drift from `project-trajectory/hooks/pre-commit` — the same risk
`test_onboard_devsetup` guards for dev-setup. These tests fail if the shipped
hook gains a floor step the meta copy lacks, or if the copy stops pointing at
this repo's harness location. (Folding the two into one via a shipped-hook
scripts-dir override is tracked as IMPROVEMENT_PLAN WI-1.42.)
"""

import re

from conftest import KIT

SHIPPED = KIT / "hooks" / "pre-commit"
META = KIT.parent / ".githooks" / "pre-commit"


def _floor_steps(text):
    """The path-independent set of floor-step tokens a hook actually invokes.

    Reads only non-comment lines, so a step merely *named* in a comment doesn't
    count; keyed by the distinctive flag rather than the script path, so the
    `scripts/` vs `project-trajectory/scripts/` difference is ignored.
    """
    steps = set()
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("#") or not s:
            continue
        m = re.search(r"--run-step ([\w-]+)", s)
        if m:
            steps.add("run-step:" + m.group(1))
        if "--strict-integrity" in s:
            steps.add("trace-integrity")
        if "check_privacy.py" in s and "--author" in s:
            steps.add("privacy-author")
        elif "check_privacy.py" in s:
            steps.add("privacy-floor")
    return steps


def test_meta_repo_hook_covers_every_shipped_floor_step():
    shipped = _floor_steps(SHIPPED.read_text(encoding="utf-8"))
    meta = _floor_steps(META.read_text(encoding="utf-8"))
    # Guard against a vacuous pass (both empty): the shipped floor is non-trivial.
    assert "run-step:arch-map" in shipped, "shipped hook floor parsed as empty"
    missing = shipped - meta
    assert not missing, (
        "meta-repo .githooks/pre-commit is missing floor steps the shipped hook "
        "runs: " + ", ".join(sorted(missing)) + " — update the copy (or fold it "
        "into the shipped hook, WI-1.42)."
    )


def test_meta_repo_hook_targets_this_repos_harness_location():
    # The whole reason the copy exists: point the floor at project-trajectory/
    # scripts/, since this repo's own scripts/ holds only dev-setup.
    assert "project-trajectory/scripts" in META.read_text(encoding="utf-8")
