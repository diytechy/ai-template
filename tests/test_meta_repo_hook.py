"""The meta-repo's pre-commit floor is a thin WRAPPER over the shipped hook.

This repo's harness lives under project-trajectory/scripts/ (not scripts/), so
.githooks/pre-commit points the shipped floor there via KIT_SCRIPTS_DIR and
delegates to project-trajectory/hooks/pre-commit. The floor logic lives once, so
there is nothing here to drift (WI-1.42; it used to be a hand copy guarded by a
step-parity test). These pin the delegation contract — the wrapper points at this
repo's harness, delegates rather than re-implementing, and the shipped hook
actually honors the override.
"""

from conftest import KIT

SHIPPED = KIT / "hooks" / "pre-commit"
META = KIT.parent / ".githooks" / "pre-commit"


def test_meta_hook_points_kit_scripts_dir_at_this_repos_harness():
    assert "KIT_SCRIPTS_DIR=project-trajectory/scripts" in META.read_text(
        encoding="utf-8"
    )


def test_meta_hook_delegates_to_the_shipped_hook():
    text = META.read_text(encoding="utf-8")
    # Delegates (exec) rather than re-implementing the floor steps — a wrapper
    # can't drift on which checks it runs.
    assert "project-trajectory/hooks/pre-commit" in text
    assert "exec" in text


def test_shipped_hook_honors_the_kit_scripts_dir_override():
    # The delegation only works if the shipped hook actually reads the override.
    assert "KIT_SCRIPTS_DIR" in SHIPPED.read_text(encoding="utf-8")
