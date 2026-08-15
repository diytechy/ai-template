"""check.py's SILENT-SKIP GUARD: a PRODUCT-layer step that SKIPped because its
tool is missing gets a boxed, unmissable stderr banner on the hook path.

The defect this closes was measured, not imagined. The pre-commit hook runs
`check.py --run-step` / `--run-steps` LENIENT on purpose — a missing tool is
SKIP with exit 0, so a not-yet-set-up repo can still commit — and a lane
worktree with no `ruff` therefore SKIPped `format` on every one of a nine-commit
branch, sending two unformatted files to the merge. Nothing was hidden: one dim
`SKIP format ...` line printed each time, in the middle of a twelve-step batch.
A dim line repeated nine times is a line nobody reads.

So the guard does NOT change what the commit is allowed to do (refusal would
break every adopter whose contributor has not run dev-setup, a migration the
owner has to choose). It makes the same fact impossible to miss. What this
module pins is the SELECTOR, because that is the part a later edit can quietly
get wrong in the silently-less-safe direction:

  1. A product-layer SKIP banners. That is the case that bit.
  2. A PROCESS-layer SKIP does NOT. Process steps are kit-owned and stdlib-only,
     and every trunk-lane freshness skip is process-layer — dressing a
     deliberate, already-explained skip as a defect is how a banner earns the
     ignore that made the original SKIP invisible.
  3. PASS and FAIL never banner, at either layer.
  4. Nothing skipped prints nothing at all.
"""

import pytest
from conftest import load_script


@pytest.fixture
def check():
    return load_script("check")


def _plan():
    """A two-step by_name map in the shape `steps()` returns: (name, requires,
    cmd, gates, layer)."""
    return {
        "format": ("format", ("ruff",), ["ruff", "format"], {"all"}, "product"),
        "arch-map": ("arch-map", (), ["python", "x"], {"all"}, "process"),
    }


def test_product_layer_skip_is_selected(check):
    results = [("format", "SKIP", "command 'ruff' not found")]
    assert check._skipped_product_steps(results, _plan()) == [
        ("format", "command 'ruff' not found")
    ]


def test_process_layer_skip_is_not_selected(check):
    """The trunk-lane freshness skips are all process-layer, and they are
    DELIBERATE. A banner over an explained skip is noise, and noise is what
    trained the eye past the original SKIP line."""
    results = [("arch-map", "SKIP", "work branch 'wi-1' — trunk lane's")]
    assert check._skipped_product_steps(results, _plan()) == []


def test_pass_and_fail_never_banner(check):
    results = [
        ("format", "PASS", "0.3s"),
        ("arch-map", "FAIL", "exit 1"),
        ("format", "FAIL", "exit 1"),
    ]
    assert check._skipped_product_steps(results, _plan()) == []


def test_banner_names_the_step_and_is_silent_when_empty(check, capsys):
    check.missing_tool_banner([])
    assert capsys.readouterr().err == ""
    check.missing_tool_banner([("format", "command 'ruff' not found")])
    err = capsys.readouterr().err
    assert "format" in err
    assert "command 'ruff' not found" in err
    assert "DID NOT RUN" in err
    assert "!!!!" in err  # the boxed shape is the point: it must not scan as a line
