"""The evidence join — a test case's `Evidence` cell, read two ways: which
tests the spine links to a module (`trace.py --tests-for`, over
`kitlib.spine.module_tests`), and whether an approved case's `Tier` agrees with
the tier its evidence runs in (`kitlib.spine.tier_findings`).

In-process throughout: synthetic registries under `tmp_path` and the live
registries read as data, with no scaffold, subprocess or git, so the module
rides the per-commit smoke tier. That placement is the point of its last case:
the tier check over the live registry, bound to this repository's module
tiering, runs in the commit bar itself, so an approved Smoke case whose
evidence moved to a slow module (or whose slow module carries a stale pin
nobody runs per commit) fails the next commit rather than waiting for a close
run to notice.
"""

import sys
import warnings
from pathlib import Path

import pytest
from conftest import ROOT, load_script, smoke_tier_for
from kitlib import spine

spine_carrier = load_script("spine_carrier")
trace = load_script("trace")

LLR_REL = "docs/requirements/low-level-requirements.toml"
TC_REL = "docs/test/test-cases.toml"


def _case(tier, evidence, status="Approved", cid="TC-001"):
    return {
        "TC-ID": cid,
        "Verifies": "LLR-001",
        "Tier": tier,
        "Evidence": evidence,
        "Status": status,
    }


def _tiers(table):
    """A `tier_of` over a literal {path: tier} table; anything else is not a
    test the harness runs."""
    return lambda path: table.get(path)


# --- the evidence cell, as the registry actually spells it --------------------


def test_evidence_items_read_every_spelling_the_registry_uses():
    # Separators seen in the live cells: `;`, `; `, and a bare space between
    # node ids. A parenthetical note and a `#anchor` are not paths.
    cell = (
        "tests/test_a.py; tests/test_b.py::test_x tests/test_c.py::test_y[live];"
        "tests/test_d.py (to be extended at implementation);"
        "docs/test/inspection-procedures.md#some-anchor"
    )
    assert spine.evidence_items(cell) == [
        ("tests/test_a.py", ""),
        ("tests/test_b.py", "test_x"),
        ("tests/test_c.py", "test_y[live]"),
        ("tests/test_d.py", ""),
        ("docs/test/inspection-procedures.md", ""),
    ]
    assert spine.evidence_items("") == []
    assert spine.evidence_items(None) == []


def test_a_spaced_parametrization_stays_one_node():
    # A separator inside a node's brackets belongs to the node: pytest ids may
    # carry spaces and `;`, and splitting there would invent two paths.
    cell = "tests/test_a.py::test_x[param one]; tests/test_b.py::test_y[a;b c]"
    assert spine.evidence_items(cell) == [
        ("tests/test_a.py", "test_x[param one]"),
        ("tests/test_b.py", "test_y[a;b c]"),
    ]


# --- the tier rule --------------------------------------------------------------


def test_a_smoke_case_with_slow_only_evidence_is_reported():
    tier_of = _tiers({"tests/test_heavy.py": "slow", "tests/test_other.py": "slow"})
    case = _case("Smoke", "tests/test_heavy.py::test_a; tests/test_other.py")
    errors, advisories = spine.tier_findings([case], tier_of)
    assert len(errors) == 1 and advisories == []
    assert "TC-001" in errors[0] and "tests/test_heavy.py" in errors[0]


def test_a_smoke_case_with_fast_evidence_is_not_reported():
    # One evidence item running per commit is enough: the case's in-memory
    # clauses keep fast evidence while its driven clauses run at close.
    tier_of = _tiers({"tests/test_heavy.py": "slow", "tests/test_fast.py": "smoke"})
    case = _case("Smoke", "tests/test_heavy.py; tests/test_fast.py::test_b")
    assert spine.tier_findings([case], tier_of) == ([], [])


def test_a_smoke_case_whose_evidence_is_no_test_is_reported():
    # A document runs in no tier, so it cannot be what makes a case per-commit.
    errors, _advisories = spine.tier_findings(
        [_case("Smoke", "docs/review.md")], _tiers({})
    )
    assert len(errors) == 1 and "TC-001" in errors[0]


def test_a_full_case_none_of_whose_evidence_is_slow_is_an_advisory():
    # Advisory, never a failure: the full tier runs everything, so a Full case
    # whose evidence runs per commit, or names no test at all, understates where
    # its evidence runs and is never false about it.
    tier_of = _tiers({"tests/test_fast.py": "smoke"})
    cases = [
        _case("Full", "tests/test_fast.py", cid="TC-001"),
        _case("Full", ".github/workflows/test.yml", cid="TC-002"),
    ]
    errors, advisories = spine.tier_findings(cases, tier_of)
    assert errors == [] and len(advisories) == 2
    assert "TC-001" in advisories[0] and "TC-002" in advisories[1]


def test_a_full_case_with_slow_evidence_or_a_release_case_is_silent():
    tier_of = _tiers({"tests/test_fast.py": "smoke", "tests/test_heavy.py": "slow"})
    cases = [
        _case("Full", "tests/test_fast.py; tests/test_heavy.py", cid="TC-001"),
        _case("Release", "tests/test_fast.py", cid="TC-003"),
    ]
    assert spine.tier_findings(cases, tier_of) == ([], [])


def test_a_case_below_approval_is_not_judged():
    # A Drafted row's tier is a proposal still in work; the tier cell the rule
    # holds true is the one a human approved.
    case = _case("Smoke", "tests/test_heavy.py", status="Drafted")
    assert spine.tier_findings([case], _tiers({"tests/test_heavy.py": "slow"})) == (
        [],
        [],
    )


# --- the module map -------------------------------------------------------------

LLRS = """[design.LLR-001]
sr_refs = ["SR-001"]
module = "src/pay.py;src/ledger.py"
status = "Approved"

[design.LLR-002]
sr_refs = ["SR-001"]
module = "src/other.py"
status = "Approved"

[design.LLR-003]
sr_refs = ["SR-001"]
module = "lib/pay.py"
status = "Drafted"
"""

TCS = """[test.TC-001]
verifies = ["SR-001", "LLR-001"]
tier = "Smoke"
evidence = "tests/test_checkout.py::test_total; tests/test_ledger.py"
status = "Approved"

[test.TC-002]
verifies = ["SR-001"]
tier = "Smoke"
evidence = "tests/test_sr_only.py"
status = "Approved"

[test.TC-003]
verifies = ["LLR-002"]
tier = "Full"
evidence = "tests/test_other.py"
status = "Approved"

[test.TC-004]
verifies = ["LLR-001"]
tier = "Full"
evidence = "docs/review.md; tests/test_checkout.py::test_refund"
status = "Drafted"

[test.TC-005]
verifies = ["LLR-003"]
tier = "Smoke"
evidence = "tests/test_lib.py"
status = "Drafted"
"""


def _docs(docs, stack=None):
    """The synthetic registries (and optionally a `stack.ini`) in a docs dir."""
    (docs / "requirements").mkdir(parents=True)
    (docs / "test").mkdir(parents=True)
    (docs / "requirements" / "low-level-requirements.toml").write_text(
        LLRS, encoding="utf-8"
    )
    (docs / "test" / "test-cases.toml").write_text(TCS, encoding="utf-8")
    if stack is not None:
        (docs / "stack.ini").write_text(stack, encoding="utf-8")
    return docs


def _spine(root, stack=None):
    _docs(root / "docs", stack)
    return root


def _rows(root):
    llrs = spine_carrier.load(root / LLR_REL, "LLR-ID", keep_examples=False)
    tcs = spine_carrier.load(root / TC_REL, "TC-ID", keep_examples=False)
    return llrs, tcs


def test_the_module_map_follows_design_rows_not_file_names(tmp_path):
    # src/pay.py's tests are named for checkout and the ledger, not for `pay`:
    # the map reaches them through LLR-001 and the cases that verify it, a
    # Drafted case included (a builder iterating runs the case being written).
    # A case that verifies only the SR, another module's case, and a document
    # among the evidence all stay out.
    llrs, tcs = _rows(_spine(tmp_path))
    assert spine.module_tests(llrs, tcs, "src/pay.py") == [
        "tests/test_checkout.py",
        "tests/test_ledger.py",
    ]
    assert spine.module_tests(llrs, tcs, "src/other.py") == ["tests/test_other.py"]
    assert spine.module_tests(llrs, tcs, "src/pay.py", test_root="spec") == []


def test_a_module_resolves_by_path_suffix_or_stem(tmp_path):
    llrs, _tcs = _rows(_spine(tmp_path))
    assert spine.resolve_modules(llrs, "src/ledger.py") == ["src/ledger.py"]
    assert spine.resolve_modules(llrs, "ledger.py") == ["src/ledger.py"]
    assert spine.resolve_modules(llrs, "src/ledger") == ["src/ledger.py"]
    assert spine.resolve_modules(llrs, "ledger") == ["src/ledger.py"]
    # `pay` names two declared modules; the caller is told both, never one
    # picked for it.
    assert spine.resolve_modules(llrs, "pay") == ["lib/pay.py", "src/pay.py"]
    assert spine.resolve_modules(llrs, "nothing") == []
    assert spine.resolve_modules(llrs, "") == []


def _tests_for(monkeypatch, root, module, *extra):
    monkeypatch.setattr(
        sys, "argv", ["trace.py", "--root", str(root), *extra, "--tests-for", module]
    )
    with pytest.raises(SystemExit) as exc:
        trace.main()
    return exc.value.code


def test_the_command_prints_one_test_file_per_line(tmp_path, capsys, monkeypatch):
    root = _spine(tmp_path)
    assert _tests_for(monkeypatch, root, "src/pay") == 0
    assert capsys.readouterr().out.splitlines() == [
        "tests/test_checkout.py",
        "tests/test_ledger.py",
    ]


def test_the_command_reads_the_declared_test_root(tmp_path, capsys, monkeypatch):
    root = _spine(tmp_path, stack="[paths]\nsrc = src\ntests = spec\n")
    assert _tests_for(monkeypatch, root, "src/pay.py") == 0
    assert capsys.readouterr().out == ""


def test_the_command_reads_the_docs_directory_it_is_pointed_at(
    tmp_path, capsys, monkeypatch
):
    # `--docs` names the registries and `stack.ini` wherever they are; the
    # unrelated `--root` holds nothing, so a listing can only come from them.
    docs = _docs(
        tmp_path / "elsewhere" / "spine-docs", stack="[paths]\ntests = tests\n"
    )
    root = tmp_path / "unrelated"
    root.mkdir()
    assert _tests_for(monkeypatch, root, "src/pay.py", "--docs", str(docs)) == 0
    assert capsys.readouterr().out.splitlines() == [
        "tests/test_checkout.py",
        "tests/test_ledger.py",
    ]
    (docs / "stack.ini").write_text("[paths]\ntests = spec\n", encoding="utf-8")
    assert _tests_for(monkeypatch, root, "src/pay.py", "--docs", str(docs)) == 0
    assert capsys.readouterr().out == ""


def test_the_command_refuses_an_unknown_or_ambiguous_module(
    tmp_path, capsys, monkeypatch
):
    root = _spine(tmp_path)
    assert _tests_for(monkeypatch, root, "nothing") == 1
    assert "no module a design row declares" in capsys.readouterr().err
    assert _tests_for(monkeypatch, root, "pay") == 2
    err = capsys.readouterr().err
    assert "lib/pay.py" in err and "src/pay.py" in err


def test_the_live_map_reaches_tests_not_named_for_their_module():
    # coherence.py's design rows are verified by `test_trace_coherence.py`, and
    # no test file is named `test_coherence*`: a file-name match finds nothing
    # for this module, while the spine reaches its suite. frame_rules.py shows
    # the other half, a driven scaffold suite beside its own unit module.
    llrs, tcs = _rows(ROOT)
    files = spine.module_tests(llrs, tcs, "project-trajectory/scripts/coherence.py")
    assert "tests/test_trace_coherence.py" in files
    assert not any(Path(f).stem.startswith("test_coherence") for f in files)
    frame = spine.module_tests(llrs, tcs, "project-trajectory/scripts/frame_rules.py")
    assert {"tests/test_frame_rules.py", "tests/test_frame_system.py"} <= set(frame)


# --- the check, over this repository's own registry ----------------------------


def _live_tier_of(path):
    """This repository's tier for an evidence path: a test module under
    `tests/` is smoke unless `tests/conftest.py` files it slow; anything else
    (a missing file, a document, a workflow) runs in no tier."""
    p = Path(path)
    if p.parts[:1] != ("tests",) or p.suffix != ".py" or not (ROOT / p).is_file():
        return None
    return smoke_tier_for(p.stem)


def test_every_approved_smoke_case_has_evidence_in_the_smoke_tier():
    _llrs, tcs = _rows(ROOT)
    errors, advisories = spine.tier_findings(tcs, _live_tier_of)
    for advisory in advisories:
        warnings.warn(advisory, stacklevel=1)
    if errors:
        pytest.fail(
            "{} approved Smoke test case(s) have no evidence in the per-commit "
            "tier. Move the case's in-memory clauses into a fast module and "
            "point `evidence` at it, or amend `tier` to Full:\n  {}".format(
                len(errors), "\n  ".join(errors)
            )
        )
