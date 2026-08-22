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

Also pinned here: the vocabulary duplicated across `spine_rules.py` and
`check.py` under the F5 no-shared-module rule, which nothing else compares.
"""

import re
import subprocess
import sys

import pytest
from conftest import ROOT, SCRIPTS, load_script

dg = load_script("spine_rules")
check = load_script("check")
vocab = load_script("check_vocab")


# --- condition 1: no lexical comparison of a ladder value ----------------------

# A comparison operator with a `DevStg-`/`DevStg-` literal or a known
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
    # `kitlib/*.py` is in scope too, and that is not housekeeping: WI-498 slice 0
    # moved the ladder ITSELF into that package, so a top-level-only glob would
    # have stopped scanning the very module that defines the values this rule
    # protects — the enforcer must follow the data.
    return sorted(SCRIPTS.glob("*.py")) + sorted((SCRIPTS / "kitlib").glob("*.py"))


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
        "kitlib.ladder.stage_ord (OI-21 banned ordering operators "
        "on the raw value; the labels do NOT alphabetize, so this is wrong "
        "even where the retired G-tags made it accidentally right):\n  "
        + "\n  ".join(offenders)
    )


def test_the_grep_would_actually_catch_the_thing_it_bans():
    """A guard that cannot fail is not a guard. Prove the pattern fires on the
    exact shapes the ruling names, including the one that USED to be correct."""
    must_catch = [
        'if stage > "DevStg-Reqs":',
        'return bar >= "DevStg-Tests"',
        "top = max(bars)",
        "for g in sorted(gates, reverse=True):",
    ]
    for line in must_catch:
        assert _LEXICAL.search(line), line
    must_not_catch = [
        "assert stage_ord(a) > stage_ord(b)",
        '_LEGACY_BAR_THRESHOLD[STAGE_REQS] = "DevStg-Reqs"',
        "max(bars, key=_BAR_GATES.index)",
        "min(rungs, key=_kitladder.stage_ord)",
    ]
    for line in must_not_catch:
        assert not _LEXICAL.search(line), line


# --- the F5-duplicated vocabulary, pinned equal --------------------------------


def test_check_selects_on_the_SHARED_ladder_and_restates_no_vocabulary():
    """The F5 duplication this test used to police is GONE (WI-498 slice 2).

    `check.py` restated the three bar names because it must stay a wholesale
    drop-in that never imports a SIBLING SCRIPT — and nothing but an equality
    pin stopped its selection vocabulary from drifting away from the value
    `spine_rules.py` writes, a drift that would have presented as "no checks
    defined": a green that ran nothing. It restates nothing now. Selection keys
    on `kitlib.ladder`, the sanctioned shared package, so the drift became
    UNREPRESENTABLE rather than detected — the WI-448 precedent slice 0 followed.
    What is pinned instead is that the retirement actually happened, because a
    re-introduced private copy would silently restore the hazard."""
    assert check.STAGES == list(dg.STAGE_ORDER) + ["all"]
    for gone in ("BAR_ORDER", "GATES", "bar_ord", "GATE_FILE"):
        assert not hasattr(check, gone), "the bar axis is retired from check.py"
    # AND IT IS RETIRED FROM THE PRODUCER TOO (WI-498 slice 5). `derive_gate.py`
    # became `spine_rules.py` — a pure library of row predicates and the rung
    # fall-through — when `docs/gate` was deleted, so the bar constants this
    # pin used to compare against are gone at BOTH ends rather than one.
    for gone in ("BAR_ORDER", "BAR_NAMES", "RETIRED_BAR_ALIASES", "GATE_FILE"):
        assert not hasattr(dg, gone), "the bar axis is retired from spine_rules"
    for gone in ("main", "compute", "basis_line", "bar_label"):
        assert not hasattr(dg, gone), "spine_rules writes nothing and has no CLI"


def test_selection_is_at_or_above_and_routes_through_the_shared_ordinal():
    """The owner's rule (OI-51) pinned as BEHAVIOR rather than as prose: a step
    runs because the repo is at or above its threshold, `all` is above
    everything without being a rung, and an unknown rung RAISES instead of
    degrading to a default that would silently change which checks run."""
    assert check.at_or_above(dg.STAGE_RELEASE, dg.STAGE_NEEDS)
    assert check.at_or_above(dg.STAGE_IMPL, dg.STAGE_IMPL)
    assert not check.at_or_above(dg.STAGE_ARCH, dg.STAGE_IMPL)
    assert check.at_or_above(check.ALL, dg.STAGE_RELEASE)
    assert check.ALL not in dg.STAGE_ORDER
    with pytest.raises(ValueError):
        check.at_or_above("DevStg-SomethingNew", dg.STAGE_NEEDS)


def test_the_integrate_and_intake_WI_stage_vocabularies_agree_too():
    """The WI `bar:` key is read by two modules, each with its own copy of the
    translation (F5 again). A row accepted by one and refused by the other would
    strand a claimed lane.

    RE-ANCHORED AT WI-498 slice 5. The three copies used to be pinned against
    `derive_gate.BAR_ORDER`; the bar axis is deleted, so the anchor is now the
    LADDER itself — the key's three values were always ladder rungs, which is
    exactly why slice 2 could re-key selection without touching them. Pinning
    them as a SUBSET of `STAGE_ORDER` rather than as a list keeps the real
    guarantee (the copies agree, and every value they accept is a real rung)
    without freezing WHICH rungs a WI may name.

    The KEY is still spelled `bar:`, and that is the last adopter-authored
    surface carrying the retired word. Renaming it is a migration entry of its
    own and is deliberately NOT folded in here (no WI spec in this repo sets it,
    so nothing is wrong today — only old-flavoured)."""
    intake = load_script("intake")
    integrate = load_script("integrate")
    assert set(intake.WI_BARS) == set(integrate._BAR_GATES)
    assert set(intake.WI_BARS) <= set(dg.STAGE_ORDER)
    # The two hand-authored RETIRED-tag tables still have to agree with each
    # other — that half of the pin never depended on the bar axis.
    for retired, canonical in intake._RETIRED_WI_BARS.items():
        assert intake.normalize_bar(retired) == canonical
        assert integrate._normalize_bar(retired) == canonical
    # ...and a correctly-authored value survives BOTH readers unchanged. The
    # retired readers case-folded with `.upper()`, which would have mangled every
    # canonical value into `DEVBAR-REQS` and refused it.
    for name in intake.WI_BARS:
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
    The harness wires `--strict` from DevStg-Tests on, exactly like
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


def test_every_token_the_regex_MATCHES_has_a_translation_to_offer():
    """`findings_for` indexes `SUGGEST` by the first matched token, so a token the
    regex can match but the table cannot translate is a KeyError — the enforcer
    CRASHING instead of reporting, on the one input it exists to catch.

    This is not hypothetical: WI-498 slice 5 shipped `\\[g[123]\\]` against a
    SUGGEST table holding only `[g1]`/`[g2]`, so any line naming `[g3]` took the
    checker down. There was never a `g3` anchor — `check_trajectory`'s
    `PHASE_ANCHOR_RE` accepts `g[12]` — so the fix narrowed the regex to the real
    vocabulary rather than inventing a translation for a token that never existed.
    Pinned structurally, because the next author to widen the alternation has no
    other way to be told that the table must widen with it."""
    for tag in ("G0", "G1", "G2", "G3", "G-Release", "G-Final"):
        assert tag in vocab.SUGGEST, tag
    for token in ("[g1]", "[g2]", "[reqs]", "[tests]"):
        assert token in vocab.SUGGEST, token
        assert vocab.RETIRED_TAG_RE.search("[4]-" + token), token
    # The token the crash rode in on: matched, untranslatable. Neither now.
    assert not vocab.RETIRED_TAG_RE.search("[4]-[g3]")
    # And the general form — nothing the regex matches may be missing a mapping.
    probe = "G0 G1 G2 G3 G-Release G-Final DevBar-Reqs DevBar-Tests "
    probe += "DevBar-Below DevBar-Release [4]-[g1] [4]-[g2] [4]-[reqs] [4]-[tests]"
    for tag in vocab.RETIRED_TAG_RE.findall(probe):
        assert tag in vocab.SUGGEST, "regex matches {!r} with no SUGGEST".format(tag)


def test_the_WORD_gate_survives_wherever_it_means_a_check_that_can_fail(planted):
    """The load-bearing half of "tag-scoped". A blanket find-replace on the word
    would rename `docs/gate-policy`, `subagent_gate.py` and the `--gate` flag —
    paths and flags adopters invoke literally — and destroy working code for a
    cosmetic gain. (`docs/gate` and `derive_gate.py` DID retire, at WI-498
    slice 5; the word did not retire with them, which is what this pins.)"""
    (planted / "docs" / "status.md").write_text(
        "Run the gate: `check.py --gate` reads docs/gate-policy. The freshness "
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
