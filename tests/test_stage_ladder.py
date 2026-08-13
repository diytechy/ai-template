"""The stage ladder's two non-negotiable conditions, and the enforcer that holds
the conversion in place (OI-21, ruled 2026-08-13).

The label carrier was ruled with conditions attached, and both are the kind that
a reviewer cannot hold by reading:

  1. **Ordering operators on a stage/bar value are BANNED.** Every comparison
     routes through a lookup that RAISES on an unknown label. Under the retired
     tags a lexical comparison was *accidentally* correct (`G1 < G2 < G3`
     alphabetizes), which is how `check.py` came to compare gate names as raw
     strings for months; the new labels do not alphabetize, so the same code is
     now wrong — silently, in whichever direction the strings happen to fall.
     `test_no_module_compares_a_ladder_value_lexically` greps for it.
  2. **The sweep lands WITH its enforcer or not at all** — the ruling's own
     words, and the evidence behind them is on the record: the retired `at G1`
     construct regenerated in this repo's own registry within days of an earlier
     sweep. `check_vocab.py` is that enforcer and the rest of this module is its
     acceptance suite.

Also pinned here: the vocabulary duplicated across `derive_gate.py` and
`check.py` under the F5 no-shared-module rule, which nothing else compares.
"""

import re
import subprocess
import sys

import pytest
from conftest import ROOT, SCRIPTS, load_script

dg = load_script("derive_gate")
check = load_script("check")
vocab = load_script("check_vocab")


# --- condition 1: no lexical comparison of a ladder value ----------------------

# A comparison operator with a `DevStg-`/`DevBar-` literal or a known
# ladder-valued expression on either side. Deliberately a GREP and not an AST
# walk: the rule is about what a reader can see in the source, the false-positive
# cost is one `# noqa`-style exemption, and an AST rule would silently stop
# covering the shell scripts and templates a later change might add.
_LEXICAL = re.compile(
    r"""
    (?:                                   # a ladder literal, then an operator
      ["'](?:DevStg|DevBar)-\w+["']\s*(?:<=|>=|<|>)
    )
    |
    (?:                                   # an operator, then a ladder literal
      (?:<=|>=|<|>)\s*["'](?:DevStg|DevBar)-\w+["']
    )
    |
    (?:\b(?:max|min|sorted)\(\s*(?:bars|stages|levels|gates)\b(?![^)]*key=))
    """,
    re.VERBOSE,
)

# Lines allowed to trip the grep, each because it is the RULE rather than a
# violation of it. Keyed by the marker the line must carry, not by line number,
# so the exemption survives an edit above it.
_GREP_ALLOW = "ladder-compare: allow"


def _kit_sources():
    return sorted(SCRIPTS.glob("*.py"))


def test_no_module_compares_a_ladder_value_lexically():
    offenders = []
    for path in _kit_sources():
        for n, line in enumerate(
            path.read_text(encoding="utf-8", errors="replace").split("\n"), 1
        ):
            if _GREP_ALLOW in line:
                continue
            if _LEXICAL.search(line):
                offenders.append("{}:{}: {}".format(path.name, n, line.strip()))
    assert not offenders, (
        "a ladder value is being ordered lexically — route it through "
        "derive_gate.stage_ord / check.bar_ord (OI-21 banned ordering operators "
        "on the raw value; the new labels do NOT alphabetize, so this is wrong "
        "even where the retired G-tags made it accidentally right):\n  "
        + "\n  ".join(offenders)
    )


def test_the_grep_would_actually_catch_the_thing_it_bans():
    """A guard that cannot fail is not a guard. Prove the pattern fires on the
    exact shapes the ruling names, including the one that USED to be correct."""
    must_catch = [
        'if stage > "DevStg-Reqs":',
        'return bar >= "DevBar-Tests"',
        "top = max(bars)",
        "for g in sorted(gates, reverse=True):",
    ]
    for line in must_catch:
        assert _LEXICAL.search(line), line
    must_not_catch = [
        "assert stage_ord(a) > stage_ord(b)",
        'STAGE_BAR[STAGE_REQS] = "DevBar-Reqs"',
        "max(bars, key=_BAR_GATES.index)",
        "sorted(higher_bars, key=bar_ord, reverse=True)",
    ]
    for line in must_not_catch:
        assert not _LEXICAL.search(line), line


# --- the F5-duplicated vocabulary, pinned equal --------------------------------


def test_check_and_derive_gate_agree_on_the_bar_vocabulary():
    """`check.py` restates the bar names rather than importing them, because it
    must stay a wholesale drop-in that never imports a sibling (the F5 rule). So
    nothing but this test stops the harness's step-selection vocabulary from
    drifting away from the value `derive_gate.py` writes into `docs/gate` — and
    that drift would present as "no checks defined", a green that ran nothing."""
    assert check.BAR_ORDER == dg.BAR_ORDER
    assert check.RETIRED_BAR_ALIASES == dg.RETIRED_BAR_ALIASES
    assert check.GATES == dg.BAR_ORDER + ["all"]
    for name in dg.BAR_ORDER:
        assert check.bar_ord(name) == dg.bar_ord(name)


def test_the_integrate_and_intake_bar_vocabularies_agree_too():
    """The WI `bar:` key is read by two modules, each with its own copy of the
    translation (F5 again). A row accepted by one and refused by the other would
    strand a claimed lane."""
    intake = load_script("intake")
    integrate = load_script("integrate")
    assert set(intake.WI_BARS) == set(integrate._BAR_GATES) == set(dg.BAR_ORDER)
    for retired, canonical in dg.RETIRED_BAR_ALIASES.items():
        assert intake.normalize_bar(retired) == canonical
        assert integrate._normalize_bar(retired) == canonical
    # ...and a correctly-authored value survives BOTH readers unchanged. The
    # retired readers case-folded with `.upper()`, which would have mangled every
    # canonical value into `DEVBAR-REQS` and refused it.
    for name in dg.BAR_ORDER:
        assert intake.normalize_bar(name) == name
        assert integrate._normalize_bar(name) == name


# --- condition 2: the enforcer ------------------------------------------------


def _run_vocab(root, *args):
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "check_vocab.py"), "--root", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


@pytest.fixture
def planted(tmp_path):
    """A tiny repo shape with one live authored surface and one of each carve-out
    class, so scope is tested as behaviour rather than asserted from the glob
    list."""
    (tmp_path / "docs" / "archive").mkdir(parents=True)
    (tmp_path / "docs" / "ratify").mkdir(parents=True)
    (tmp_path / "docs" / "work" / "complete").mkdir(parents=True)
    (tmp_path / "docs" / "okf").mkdir(parents=True)
    for rel in (
        "docs/archive/old.md",
        "docs/ratify/2026-01-01-reattest.md",
        "docs/work/complete/WI-001-x.md",
        "docs/okf/k.md",
        "docs/log.md",
        "OWNER_SCRATCHPAD.md",
    ):
        (tmp_path / rel).write_text(
            "the repo passed G1 and G2 on 2026-01-01\n", encoding="utf-8"
        )
    return tmp_path


def test_a_retired_tag_in_a_live_surface_is_reported(planted):
    (planted / "docs" / "status.md").write_text(
        "Active gate: the repo is at G2.\n", encoding="utf-8"
    )
    warn = _run_vocab(planted)
    assert "docs/status.md:1" in warn.stdout
    assert "G2" in warn.stdout


def test_severity_is_WARN_FIRST_and_promotes_under_strict(planted):
    """The ruled posture. A repo mid-conversion must SEE every remaining site
    without being blocked by it; a repo past its requirements bar has no excuse.
    The harness wires `--strict` from DevBar-Tests on, exactly like
    check_trajectory."""
    (planted / "docs" / "status.md").write_text("at G2\n", encoding="utf-8")
    warn = _run_vocab(planted)
    assert warn.returncode == 0, warn.stdout + warn.stderr
    assert "WARN" in warn.stdout and "warn-first" in warn.stdout
    strict = _run_vocab(planted, "--strict")
    assert strict.returncode == 1
    assert "ERROR" in strict.stdout


@pytest.mark.parametrize(
    "rel",
    [
        "docs/archive/old.md",
        "docs/ratify/2026-01-01-reattest.md",
        "docs/work/complete/WI-001-x.md",
        "docs/okf/k.md",
        "docs/log.md",
        "OWNER_SCRATCHPAD.md",
    ],
)
def test_the_ruled_carve_outs_are_never_reported(planted, rel):
    """History is not rewritten and attestations are not re-worded — the ruling's
    hardest condition, because the tempting fix (sweep everything) makes a signed
    record claim something was signed that was not. Each carve-out is planted with
    a real tag, so a glob that stopped matching shows up as a NEW finding here."""
    out = _run_vocab(planted, "--strict")
    assert rel not in out.stdout, out.stdout
    assert out.returncode == 0, out.stdout


def test_a_deep_path_under_a_carved_out_directory_is_still_exempt(planted):
    # `fnmatch` alone would let `docs/archive/specs/x.md` through — the subtree
    # rule is what makes the carve-out mean the directory rather than its
    # immediate children, and deep history is exactly where the tags live.
    deep = planted / "docs" / "archive" / "specs" / "model.md"
    deep.parent.mkdir(parents=True)
    deep.write_text("G3 was met\n", encoding="utf-8")
    assert _run_vocab(planted, "--strict").returncode == 0


def test_the_allow_markers_exempt_a_declaration_site(planted):
    """Translation tables must be able to NAME what they translate. The marker is
    explicit rather than heuristic ("the line also says 'retired'") because a
    heuristic that can be satisfied by accident is how the vocabulary grows back
    through the enforcer meant to stop it."""
    live = planted / "docs" / "status.md"
    live.write_text("at G2  # check_vocab: allow\nand G3 here\n", encoding="utf-8")
    out = _run_vocab(planted)
    assert "status.md:1" not in out.stdout
    assert "status.md:2" in out.stdout
    live.write_text("check_vocab: allow-file\nat G2\nand G3\n", encoding="utf-8")
    assert _run_vocab(planted, "--strict").returncode == 0


def test_the_WORD_gate_survives_wherever_it_means_a_check_that_can_fail(planted):
    """The load-bearing half of "tag-scoped". A blanket find-replace on the word
    would rename `docs/gate`, `derive_gate.py` and `--gate` — paths and flags
    adopters invoke literally — and destroy working code for a cosmetic gain."""
    (planted / "docs" / "status.md").write_text(
        "Run the gate: `derive_gate.py --check` guards docs/gate. The freshness "
        "gate is wired into subagent_gate and test_env_gates; check_perf's budget "
        "gates fail loudly.\n",
        encoding="utf-8",
    )
    out = _run_vocab(planted, "--strict")
    assert out.returncode == 0, out.stdout


def test_this_repo_is_clean_at_the_ERROR_severity():
    """Not a fixture test: the meta-repo's OWN tree must carry no retired tag in
    any live authored surface. Without this every assertion above could pass
    against planted files while the conversion this module exists to hold in place
    had quietly rotted."""
    out = _run_vocab(ROOT, "--strict")
    assert out.returncode == 0, out.stdout + out.stderr
    assert "clean" in out.stdout
