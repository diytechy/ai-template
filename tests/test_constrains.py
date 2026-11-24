"""A requirement names the interface it constrains (WI-1024, variant F's fourth row).

A design row or a system requirement may name, in its `constrains` cell, the
interfaces whose behaviour it states; a dead id fails the strict check
(LLR-417). Beside it a design row may state that behaviour's input set in the
permutation grammar and what the interface does outside it; a cell that does
not parse, or sits on a row constraining nothing, fails (LLR-418), and a
constraining row without them is reported, never failing (LLR-419, the
operator's warn-first ruling of 2026-11-21). The cell is traced and routed to
adjudication; its two companions are accepted text (LLR-420). Every interface
reaches a test case the harness runs through a row constraining it or a case
naming it, reported warn-first (LLR-421), and a case naming an interface every
row it verifies already constrains is reported (LLR-422). Placement reads the
cell (LLR-403).

In-process: synthetic registries under `tmp_path`, and the checker driven
through `trace.main`, so the module rides the per-commit smoke tier. The one
git-backed case builds a two-commit repository for the routed-amendment walk.
"""

import os
import subprocess
import sys

import pytest
from conftest import load_script
from kitlib import spine

coherence = load_script("coherence")
trace = load_script("trace")
gen_cases = load_script("gen_cases")
gen_components = load_script("gen_components")
acceptance_record = load_script("acceptance_record")
intake = load_script("intake")
spine_carrier = load_script("spine_carrier")

SR_REL = "docs/requirements/system-requirements.toml"
LLR_REL = "docs/requirements/low-level-requirements.toml"
TC_REL = "docs/test/test-cases.toml"
IF_REL = "docs/requirements/interfaces.toml"
CMP_REL = "docs/requirements/components.toml"

SR = {"title": "t", "requirement": "The system shall add.", "status": "Accepted"}
SR.update({"acceptance_criteria": "adds", "verification_method": "Test", "phase": 1})


def _llr(**cells):
    row = {"sr_refs": ["SR-001"], "title": "t", "detail": "d.", "status": "Accepted"}
    row["phase"] = 1
    row.update(cells)
    return row


def _child(parent, **cells):
    """A design row below `parent` in the requirement tree: it names its
    parent and no requirement."""
    row = _llr(parent=parent, **cells)
    row.pop("sr_refs")
    return row


def _tc(verifies, automated="Yes", **cells):
    row = {"verifies": verifies, "level": "Unit", "method": "m", "tier": "Smoke"}
    row.update({"expected": "e", "automated": automated, "status": "Accepted"})
    row.update({"evidence": "tests/test_a.py", "phase": 1})
    row.update(cells)
    if automated == "No":
        row.pop("evidence")
        row.update({"inputs": ["SR-001"], "max_age": 30})
    return row


def _if(owner="CMP-001", channel="exit-code"):
    return {
        "owner": owner,
        "consumers": ["external:git"],
        "channel": channel,
        "version": "v1",
        "status": "Drafted",
    }


def _registry(table, rows):
    return "".join(
        "[{}.{}]\n{}\n".format(table, rid, spine.toml_fields(cells.items()))
        for rid, cells in rows.items()
    )


def _project(root, llrs, tcs, ifs=None, srs=None, header=""):
    """A minimal project: the given rows, two components, the `git` party, and
    an id watermark raised over them, so its strict check fails only on the
    rule under test."""
    ifs = {"IF-001": _if(), "IF-002": _if("CMP-002", "cli")} if ifs is None else ifs
    files = {
        SR_REL: _registry("requirement", srs or {"SR-001": SR}),
        LLR_REL: _registry("design", llrs),
        TC_REL: _registry("test", tcs),
        IF_REL: "# External party: git\n\n" + header + _registry("interface", ifs),
        CMP_REL: _registry(
            "component",
            {
                c: {"name": c, "category": "software", "status": "Accepted"}
                for c in ("CMP-001", "CMP-002")
            },
        ),
    }
    for rel, text in files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    trace.bump_watermark(root)
    return root


def _strict(monkeypatch, capsys, root, *flags):
    """`trace.py --strict` (or the given flags) over `root`: (exit, stdout)."""
    argv = ["trace.py", "--root", str(root), *(flags or ("--strict",))]
    monkeypatch.setattr(sys, "argv", argv)
    try:
        trace.main()  # a clean run returns; a failing one exits nonzero
        code = 0
    except SystemExit as exc:
        code = exc.code
    return code, capsys.readouterr().out


def _rows(root, rel, col):
    return [
        r for r in spine_carrier.load(root / rel, col) if not r[col].endswith("-000")
    ]


# --- LLR-417: the cell and its one finding ---------------------------------


def test_a_constrains_id_naming_no_live_interface_fails_the_strict_check(
    tmp_path, monkeypatch, capsys
):
    """Implements: TC-527"""
    llrs = {
        "LLR-001": _llr(constrains=["IF-001"]),
        "LLR-002": _llr(constrains=["IF-009"]),
        "LLR-003": _llr(constrains=["SR-001", "IF-000"]),
    }
    srs = {"SR-001": dict(SR, constrains=["IF-002", "IF-008"])}
    tcs = {"TC-001": _tc(["SR-001", "LLR-001", "LLR-002", "LLR-003"])}
    _project(tmp_path, llrs, tcs, srs=srs)
    code, out = _strict(monkeypatch, capsys, tmp_path)
    assert code == 1, out
    for rid, iid in (
        ("LLR-002", "IF-009"),
        ("LLR-003", "SR-001"),
        ("LLR-003", "IF-000"),
        ("SR-001", "IF-008"),
    ):
        assert (
            "{} Constrains names {}, which is no live interface row".format(rid, iid)
            in out
        ), out
    # A live id on either tier is no finding.
    assert "LLR-001 Constrains" not in out and "names IF-001" not in out
    assert "names IF-002" not in out


def test_a_live_constrains_cell_passes_and_an_empty_one_is_refused_on_read(
    tmp_path, monkeypatch, capsys
):
    """Implements: TC-527"""
    _project(
        tmp_path,
        {"LLR-001": _llr(constrains=["IF-001", "IF-002"])},
        {"TC-001": _tc(["SR-001", "LLR-001"])},
    )
    code, out = _strict(monkeypatch, capsys, tmp_path)
    assert code == 0, out
    # An explicit empty list is the carrier's explicit-empty cell: refused when
    # the registry is read, naming the row and the cell.
    path = tmp_path / LLR_REL
    path.write_bytes(
        path.read_bytes().replace(
            b'constrains = ["IF-001", "IF-002"]', b"constrains = []"
        )
    )
    with pytest.raises(SystemExit) as exc:
        spine_carrier.load(path, "LLR-ID")
    assert "LLR-001 sets `Constrains` to an EMPTY STRING" in str(exc.value)


# --- LLR-418: the companion cells ------------------------------------------


def test_a_companion_cell_that_does_not_parse_or_constrains_nothing_fails(
    tmp_path, monkeypatch, capsys
):
    """Implements: TC-528"""
    good = {"dimensions": "state=set{current,stale}", "out_of_domain": "Refused."}
    llrs = {
        "LLR-001": _llr(constrains=["IF-001"], **good),
        "LLR-002": _llr(constrains=["IF-001"], dimensions="state=list(a)"),
        "LLR-003": _llr(constrains=["IF-001"], dimensions="a=bool; @sometimes"),
        "LLR-004": _llr(
            constrains=["IF-001"],
            out_of_domain="It is refused. Nothing is written.",
        ),
        "LLR-005": _llr(constrains=["IF-001"], out_of_domain="No full stop"),
        "LLR-008": _llr(
            constrains=["IF-001"], out_of_domain="Refused. nothing changes."
        ),
        "LLR-009": _llr(constrains=["IF-001"], out_of_domain="Refused at 2.5 MB."),
        "LLR-006": _llr(dimensions="a=bool"),
        "LLR-007": _llr(out_of_domain="Refused."),
    }
    tcs = {"TC-001": _tc(["SR-001", *llrs])}
    _project(tmp_path, llrs, tcs)
    code, out = _strict(monkeypatch, capsys, tmp_path)
    assert code == 1, out
    assert "LLR-002 Dimensions does not parse in the permutation grammar: " in out
    assert "unrecognized dimension type: 'state=list(a)'" in out
    assert "LLR-003 Dimensions does not parse" in out
    assert "unknown strategy: sometimes" in out
    assert "LLR-004 OutOfDomain is not one sentence" in out
    assert "LLR-005 OutOfDomain is not one sentence" in out
    assert "LLR-008 OutOfDomain is not one sentence" in out
    assert "LLR-009 OutOfDomain" not in out
    assert "LLR-006 carries Dimensions but constrains no interface" in out
    assert "LLR-007 carries OutOfDomain but constrains no interface" in out
    assert "LLR-001 Dimensions" not in out and "LLR-001 OutOfDomain" not in out


@pytest.mark.parametrize(
    "spec",
    [
        "size=range[0..2GiB]; mode=set{a,b,c}; @pairwise",
        "n=range[1..100|50]",
        "flag=bool",
        "a=set{}",
        "no-equals-sign",
        "a=list(b)",
        "@full",
        "",
    ],
)
def test_the_cell_and_the_generator_read_one_grammar(spec):
    """Implements: TC-528"""
    try:
        expected = gen_cases.parse_spec(spec)
    except SystemExit as exc:
        with pytest.raises(ValueError) as refused:
            spine.parse_dimensions(spec)
        assert str(refused.value) == str(exc.code)
    else:
        assert spine.parse_dimensions(spec) == expected


# --- LLR-419: the warn-first missing-cell report ---------------------------


def test_a_constraining_row_without_its_companions_is_counted_and_passes(
    tmp_path, monkeypatch, capsys
):
    """Implements: TC-529"""
    both = {"dimensions": "state=set{current,stale}", "out_of_domain": "Refused."}
    llrs = {
        "LLR-001": _llr(constrains=["IF-001", "IF-002"], **both),
        "LLR-002": _llr(constrains=["IF-001"]),
        "LLR-003": _llr(constrains=["IF-002"], dimensions="a=bool"),
    }
    llrs.update(
        {"LLR-{:03d}".format(n): _llr(constrains=["IF-001"]) for n in range(4, 13)}
    )
    _project(tmp_path, llrs, {"TC-001": _tc(["SR-001", *llrs])})
    code, out = _strict(monkeypatch, capsys, tmp_path)
    assert code == 0, out
    line = next(x for x in out.splitlines() if "constrains: " in x)
    assert line.startswith(
        "WARNING (advisory): constrains: 11 design row(s) constrain an interface "
        "without both a Dimensions and an OutOfDomain cell (LLR-002, LLR-003, "
        "LLR-004, LLR-005, LLR-006, LLR-007, LLR-008, LLR-009, LLR-010, LLR-011, "
        "+1 more); per constrained interface's channel, with both/without: "
        "cli 1/1, exit-code 1/10."
    ), line
    assert line.endswith("Reported, never failing --strict"), line


# --- LLR-420: the cells' class ---------------------------------------------


def test_constrains_is_traced_and_routed_and_its_companions_are_accepted():
    """Implements: TC-530"""
    for rel in (SR_REL, LLR_REL):
        assert acceptance_record.spine_cell_class(rel, "Constrains") == "traced"
        assert "Constrains" in intake.ROUTED_TRACED_CELLS[rel]
    for column in ("Dimensions", "OutOfDomain"):
        assert acceptance_record.spine_cell_class(LLR_REL, column) == "accepted"
        assert column in acceptance_record.SPINE_ACCEPTED_CELLS[LLR_REL]
    # The schema declares the three cells, and the carrier names their columns.
    assert "constrains" in spine.SPINE_TIER_KEYS["SR-ID"]
    for key, column in (
        ("constrains", "Constrains"),
        ("dimensions", "Dimensions"),
        ("out_of_domain", "OutOfDomain"),
    ):
        assert key in spine.SPINE_TIER_KEYS["LLR-ID"]
        assert spine_carrier.SPINE_COLUMN[key] == column
    assert "dimensions" not in spine.SPINE_TIER_KEYS["SR-ID"]


def _git(root, *args):
    env = dict(os.environ, GIT_AUTHOR_DATE="@1000000 +0000")
    env["GIT_COMMITTER_DATE"] = env["GIT_AUTHOR_DATE"]
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        encoding="utf-8",
        errors="replace",
        env=env,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc.stdout.strip()


def _two_ranges(tmp_path):
    """A project committed three times: the requirement and the first design
    row accepted with no constrains cell and the second constraining IF-001;
    then a constrains cell alone added to the requirement and the first design
    row; then a dimensions and an out-of-domain cell alone added to the second.
    Returns the root and the three commits."""
    tcs = {"TC-001": _tc(["SR-001", "LLR-001", "LLR-002"])}
    llr2 = _llr(constrains=["IF-001"])
    root = _project(tmp_path, {"LLR-001": _llr(), "LLR-002": llr2}, tcs)
    _git(root, "init", "-q")
    _git(root, "config", "user.email", "t@example.invalid")
    _git(root, "config", "user.name", "t")
    _git(root, "config", "core.autocrlf", "false")
    commits = []

    def commit(message):
        _git(root, "add", "-A")
        _git(root, "commit", "-qm", message)
        commits.append(_git(root, "rev-parse", "HEAD"))

    commit("accepted")
    llrs = {"LLR-001": _llr(constrains=["IF-001"]), "LLR-002": llr2}
    srs = {"SR-001": dict(SR, constrains=["IF-002"])}
    _project(root, llrs, tcs, srs=srs)
    commit("constrains alone")
    companions = {"dimensions": "a=bool", "out_of_domain": "A negative is refused."}
    llrs["LLR-002"] = dict(llr2, **companions)
    _project(root, llrs, tcs, srs=srs)
    commit("companions alone")
    return root, commits


def test_a_constrains_only_change_routes_with_no_accepted_cell_moved(tmp_path):
    """Implements: TC-530"""
    root, (accepted, constrained, _companions) = _two_ranges(tmp_path)
    records = acceptance_record.staged_spine_amendments(root, accepted, constrained)
    by_id = {r["id"]: r for r in records}
    assert set(by_id) == {"SR-001", "LLR-001"}
    for rec in by_id.values():
        # The pointer moves no accepted text, on either tier.
        assert set(rec["traced"]) == {"Constrains"} and not rec["accepted"], rec
    routed, refusal = intake._routed_amendments(root, accepted, constrained)
    assert refusal is None
    assert {r["id"]: set(r["routed"]) for r in routed} == {
        "SR-001": {"Constrains"},
        "LLR-001": {"Constrains"},
    }
    drafts, refusal = intake._amendment_drafts(root, accepted, constrained)
    assert refusal is None
    (draft,) = drafts
    assert draft["kind"] == "adjudication"
    assert draft["adjudicates"] == ["LLR-001", "SR-001"]


def test_a_companion_cell_change_amends_accepted_text_alone(tmp_path):
    """Implements: TC-530"""
    root, (_accepted, constrained, companions) = _two_ranges(tmp_path)
    records = acceptance_record.staged_spine_amendments(root, constrained, companions)
    (rec,) = records
    assert rec["id"] == "LLR-002"
    assert set(rec["accepted"]) == {"Dimensions", "OutOfDomain"}
    assert not rec["traced"], rec
    routed, refusal = intake._routed_amendments(root, constrained, companions)
    assert refusal is None
    (minted,) = routed
    assert minted["id"] == "LLR-002" and not minted["routed"]
    drafts, refusal = intake._amendment_drafts(root, constrained, companions)
    assert refusal is None
    (draft,) = drafts
    assert draft["adjudicates"] == ["LLR-002"]


# --- LLR-421: interface coverage, warn-first --------------------------------


def test_each_interface_reaches_a_run_case_through_a_constraining_row_or_a_naming_case(
    tmp_path, monkeypatch, capsys
):
    """Implements: TC-531"""
    ifs = {"IF-{:03d}".format(n): _if() for n in range(1, 7)}
    llrs = {
        "LLR-001": _llr(constrains=["IF-001"]),
        "LLR-002": _llr(),
        "LLR-003": _llr(sr_refs=["SR-002"]),
        "LLR-004": _llr(constrains=["IF-006"]),
    }
    srs = {
        "SR-001": SR,
        "SR-002": dict(SR, constrains=["IF-002"]),
        "SR-003": dict(SR, verification_method="Inspection"),
    }
    tcs = {
        "TC-001": _tc(["SR-001", "LLR-001"]),
        "TC-002": _tc(["SR-002", "LLR-003"]),
        "TC-003": _tc(["SR-001", "LLR-002", "IF-003"]),
        "TC-004": _tc(["SR-003", "IF-004"], automated="No"),
        "TC-005": _tc(["SR-001", "LLR-004"], automated="No"),
    }
    _project(tmp_path, llrs, tcs, ifs=ifs, srs=srs)
    srs_, llrs_ = _rows(tmp_path, SR_REL, "SR-ID"), _rows(tmp_path, LLR_REL, "LLR-ID")
    tcs_, ifs_ = _rows(tmp_path, TC_REL, "TC-ID"), _rows(tmp_path, IF_REL, "IF-ID")
    # The reach is the blast radius: the rows constraining an interface or
    # observed at it, then every case verifying those rows or naming it.
    reach = spine.interface_reach(ifs_, srs_, llrs_, tcs_)
    assert reach["IF-001"] == (["LLR-001"], ["TC-001"])
    assert reach["IF-002"] == (["SR-002"], ["TC-002"])
    assert reach["IF-003"] == (["LLR-002", "SR-001"], ["TC-001", "TC-003", "TC-005"])
    assert reach["IF-005"] == ([], [])
    assert coherence.interface_coverage(srs_, llrs_, tcs_, ifs_) == {
        "IF-001": "design row",
        "IF-002": "requirement",
        "IF-003": "case",
        "IF-004": "observation",
        "IF-005": "unreached",
        "IF-006": "observation",
    }
    code, out = _strict(monkeypatch, capsys, tmp_path)
    # Warn-first: reported, naming each, and the strict check still passes.
    assert code == 0, out
    assert (
        "interface coverage: 6 interface(s): 1 through a constraining design row, "
        "1 through a constraining requirement, 1 through a naming test case, "
        "2 by observation alone, 1 unreached"
    ) in out
    assert (
        "interface coverage: 1 interface(s) reach no test case through a row "
        "constraining them or a case naming them: IF-005."
    ) in out
    assert (
        "interface coverage: 2 interface(s) are reached by observation cases "
        "alone: IF-004, IF-006."
    ) in out


def test_a_requirement_a_naming_case_verifies_brings_its_run_cases_into_the_reach(
    tmp_path,
):
    """Implements: TC-531"""
    # An observation case names IF-001 beside the requirement it verifies; a
    # case the harness runs verifies that requirement, so the interface is
    # reached through a naming case, not by observation alone.
    tcs = {
        "TC-001": _tc(["SR-001", "LLR-001"]),
        "TC-002": _tc(["SR-001", "IF-001"], automated="No"),
    }
    _project(tmp_path, {"LLR-001": _llr()}, tcs)
    srs_, llrs_ = _rows(tmp_path, SR_REL, "SR-ID"), _rows(tmp_path, LLR_REL, "LLR-ID")
    tcs_, ifs_ = _rows(tmp_path, TC_REL, "TC-ID"), _rows(tmp_path, IF_REL, "IF-ID")
    reach = spine.interface_reach(ifs_, srs_, llrs_, tcs_)
    assert reach["IF-001"] == (["SR-001"], ["TC-001", "TC-002"])
    assert coherence.interface_coverage(srs_, llrs_, tcs_, ifs_)["IF-001"] == "case"


def test_the_interface_check_opt_out_silences_coverage(tmp_path, monkeypatch, capsys):
    """Implements: TC-531"""
    _project(tmp_path, {"LLR-001": _llr()}, {"TC-001": _tc(["SR-001", "LLR-001"])})
    (tmp_path / "docs" / "process.toml").write_bytes(
        b"[checks]\ninterfaces_check = false\n"
    )
    code, out = _strict(monkeypatch, capsys, tmp_path)
    assert code == 0, out
    assert "interface coverage" not in out
    # No interface row: the rule is vacuous.
    (tmp_path / "docs" / "process.toml").unlink()
    (tmp_path / IF_REL).write_bytes(b"# External party: git\n")
    code, out = _strict(monkeypatch, capsys, tmp_path)
    assert code == 0, out
    assert "interface coverage" not in out


def test_a_constraining_design_row_brings_the_cases_of_the_design_rows_below_it(
    tmp_path, monkeypatch, capsys
):
    """Implements: TC-531"""
    # IF-001 is constrained only by LLR-001, whose only run case verifies its
    # child; IF-002 only by LLR-003, whose only run case verifies its
    # grandchild. Each parent's own case is an observation case.
    llrs = {
        "LLR-001": _llr(constrains=["IF-001"]),
        "LLR-002": _child("LLR-001"),
        "LLR-003": _llr(constrains=["IF-002"]),
        "LLR-004": _child("LLR-003"),
        "LLR-005": _child("LLR-004"),
    }
    tcs = {
        "TC-001": _tc(["SR-001", "LLR-002"]),
        "TC-002": _tc(["LLR-005"]),
        "TC-003": _tc(["LLR-001", "LLR-003", "LLR-004"], automated="No"),
    }
    _project(tmp_path, llrs, tcs)
    srs_, llrs_ = _rows(tmp_path, SR_REL, "SR-ID"), _rows(tmp_path, LLR_REL, "LLR-ID")
    tcs_, ifs_ = _rows(tmp_path, TC_REL, "TC-ID"), _rows(tmp_path, IF_REL, "IF-ID")
    reach = spine.interface_reach(ifs_, srs_, llrs_, tcs_)
    assert reach["IF-001"] == (["LLR-001"], ["TC-001", "TC-003"])
    assert reach["IF-002"] == (["LLR-003"], ["TC-002", "TC-003"])
    assert coherence.interface_coverage(srs_, llrs_, tcs_, ifs_) == {
        "IF-001": "design row",
        "IF-002": "design row",
    }
    code, out = _strict(monkeypatch, capsys, tmp_path)
    assert code == 0, out
    assert (
        "interface coverage: 2 interface(s): 2 through a constraining design row, "
        "0 through a constraining requirement, 0 through a naming test case, "
        "0 by observation alone, 0 unreached"
    ) in out
    assert "reach no test case" not in out
    assert "reached by observation cases alone" not in out


def test_a_row_only_observed_at_an_interface_brings_its_own_cases_alone(tmp_path):
    """Implements: TC-531"""
    # LLR-001 constrains IF-001 and is only observed at IF-002, beside its
    # requirement, through an observation case naming both; the run cases of
    # its child and grandchild reach IF-001 and not IF-002.
    llrs = {
        "LLR-001": _llr(constrains=["IF-001"]),
        "LLR-002": _child("LLR-001"),
        "LLR-003": _child("LLR-002"),
    }
    tcs = {
        "TC-001": _tc(["LLR-002"]),
        "TC-002": _tc(["LLR-003"]),
        "TC-003": _tc(["SR-001", "LLR-001", "IF-002"], automated="No"),
    }
    _project(tmp_path, llrs, tcs)
    srs_, llrs_ = _rows(tmp_path, SR_REL, "SR-ID"), _rows(tmp_path, LLR_REL, "LLR-ID")
    tcs_, ifs_ = _rows(tmp_path, TC_REL, "TC-ID"), _rows(tmp_path, IF_REL, "IF-ID")
    reach = spine.interface_reach(ifs_, srs_, llrs_, tcs_)
    assert reach["IF-001"] == (["LLR-001"], ["TC-001", "TC-002", "TC-003"])
    assert reach["IF-002"] == (["LLR-001", "SR-001"], ["TC-003"])
    assert coherence.interface_coverage(srs_, llrs_, tcs_, ifs_) == {
        "IF-001": "design row",
        "IF-002": "observation",
    }


# --- LLR-422: the per-pair repeat check, warn-first -------------------------


def test_a_name_every_verified_row_already_constrains_is_reported_per_pair(
    tmp_path, monkeypatch, capsys
):
    """Implements: TC-532"""
    llrs = {
        "LLR-001": _llr(constrains=["IF-001"]),
        "LLR-002": _llr(),
        "LLR-003": _llr(constrains=["IF-001"]),
    }
    tcs = {
        # every verified row constrains IF-001: the name repeats them
        "TC-001": _tc(["LLR-001", "LLR-003", "IF-001"]),
        # the mixed case: one verified row constrains it, the other does not
        "TC-002": _tc(["LLR-001", "LLR-002", "IF-001"]),
        # a verified requirement that constrains nothing keeps the name
        "TC-003": _tc(["SR-001", "LLR-001", "IF-001"]),
    }
    _project(tmp_path, llrs, tcs)
    llrs_, tcs_ = _rows(tmp_path, LLR_REL, "LLR-ID"), _rows(tmp_path, TC_REL, "TC-ID")
    srs_ = _rows(tmp_path, SR_REL, "SR-ID")
    found = coherence.repeat_findings(srs_, llrs_, tcs_)
    assert found == [
        "TC-001 names IF-001, which every row it verifies already constrains "
        "(LLR-001, LLR-003): a test case names an interface only where it "
        "differs from its rows'"
    ]
    # A case verifying no design row or requirement repeats nothing.
    assert (
        coherence.repeat_findings([], [], [{"TC-ID": "TC-9", "Verifies": "IF-001"}])
        == []
    )
    code, out = _strict(monkeypatch, capsys, tmp_path)
    assert code == 0, out
    assert "repeat: TC-001 names IF-001" in out and "TC-002 names" not in out
    # The integrity check the commit hook runs is never failed by it.
    code, out = _strict(monkeypatch, capsys, tmp_path, "--strict-integrity")
    assert code == 0, out


# --- LLR-403: placement reads the cell --------------------------------------


def test_a_design_row_is_placed_through_the_interfaces_it_constrains():
    """Implements: TC-480"""
    ifs = [
        {"IF-ID": "IF-001", "Owner": "CMP-001"},
        {"IF-ID": "IF-002", "Owner": "CMP-002"},
        {"IF-ID": "IF-003", "Owner": "external:git"},
    ]
    llrs = [
        {"LLR-ID": "LLR-001", "Constrains": "IF-001", "SR-Refs": "SR-001"},
        {"LLR-ID": "LLR-002", "Constrains": "IF-003", "SR-Refs": "SR-001"},
        {"LLR-ID": "LLR-003", "Constrains": "IF-002", "SR-Refs": "SR-001"},
        {"LLR-ID": "LLR-000", "Constrains": "IF-001"},
    ]
    tcs = [
        {"TC-ID": "TC-001", "Verifies": "LLR-001"},
        {"TC-ID": "TC-002", "Verifies": "LLR-003; IF-001"},
    ]
    placement = spine.llr_placement(tcs, ifs, llrs)
    # A component owner places, an external owner places nothing, the case's
    # interface joins the constrained one, and an example row is not read.
    assert placement == {"LLR-001": ["CMP-001"], "LLR-003": ["CMP-001", "CMP-002"]}
    assert spine.llr_placement(tcs, ifs) == {"LLR-003": ["CMP-001"]}
    assert trace.placement_line(llrs[:3], tcs, ifs).startswith(
        "placement: 2 design row(s) placed, 1 unplaced (LLR-002)"
    )
