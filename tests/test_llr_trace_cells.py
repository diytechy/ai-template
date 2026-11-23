"""Design rows lose their down-pointing cells (WI-1023, variant F's third row).

An LLR row carries no `module`, `code_symbol` or `component` cell, and the
loader refuses a key a requirement tier does not declare (LLR-404). The files
realizing a row are read up from the code's `Implements:` tags, one index every
former reader of the cells reads (LLR-405). A row's placement is derived: the
owner component of each interface a test case verifying it names, and a row
placed nowhere is listed and counted, never refused (LLR-403). A test case's
`evidence` cell is generated from the test files' tags, its other parts kept
verbatim (LLR-406), and a migration removes the three cells from an adopter's
registry (LLR-407).

In-process: synthetic registries under `tmp_path`, plus the live test-case
registry read as data, so the module rides the per-commit smoke tier.
"""

import shutil
import sys
import tomllib
from pathlib import Path

import pytest
from conftest import ROOT, load_script
from kitlib import spine

spine_carrier = load_script("spine_carrier")
acceptance_record = load_script("acceptance_record")
coherence = load_script("coherence")
intake = load_script("intake")
baseline_snapshot = load_script("baseline_snapshot")
spine_rules = load_script("spine_rules")
arch_inputs = load_script("arch_inputs")
arch_tags = load_script("arch_tags")
gen_components = load_script("gen_components")
migrate_carrier = load_script("migrate_carrier")
trace = load_script("trace")

LLR_REL = "docs/requirements/low-level-requirements.toml"
TC_REL = "docs/test/test-cases.toml"


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))
    return path


def _main(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["trace.py", *[str(a) for a in argv]])
    with pytest.raises(SystemExit) as exc:
        trace.main()
    return exc.value.code


def test_a_design_row_is_placed_through_the_interfaces_its_cases_name():
    """Implements: TC-480"""
    tcs = [
        {"TC-ID": "TC-001", "Verifies": "LLR-001; IF-001; IF-002"},
        {"TC-ID": "TC-002", "Verifies": "LLR-001; LLR-002; IF-001"},
        {"TC-ID": "TC-003", "Verifies": "LLR-003; IF-003"},
        {"TC-ID": "TC-004", "Verifies": "LLR-004"},
        {"TC-ID": "TC-000", "Verifies": "LLR-004; IF-001"},
    ]
    ifs = [
        {"IF-ID": "IF-001", "Owner": "CMP-001"},
        {"IF-ID": "IF-002", "Owner": "CMP-002"},
        {"IF-ID": "IF-003", "Owner": "external:git"},
    ]
    placement = spine.llr_placement(tcs, ifs)
    # Per (case, row) pair: LLR-001 sits at both interfaces' owners; LLR-002 at
    # the one its case names; an `external:` owner places nothing; a case naming
    # no interface places nothing; an example row is not read.
    assert placement == {"LLR-001": ["CMP-001", "CMP-002"], "LLR-002": ["CMP-001"]}
    llrs = [{"LLR-ID": rid} for rid in ("LLR-001", "LLR-002", "LLR-003", "LLR-004")]
    assert spine.unplaced_llrs(llrs, placement) == ["LLR-003", "LLR-004"]
    # Listed and counted, never refused: one advisory line.
    line = trace.placement_line(llrs, tcs, ifs)
    assert line == (
        "placement: 2 design row(s) placed, 2 unplaced (LLR-003, LLR-004); "
        "unplaced is counted, never refused"
    )
    # The component view reads the derived placement and lists the rest.
    cmps = [{"CMP-ID": "CMP-001", "Name": "one"}, {"CMP-ID": "CMP-002", "Name": "two"}]
    srs = [{"SR-ID": "SR-001"}, {"SR-ID": "SR-002"}]
    for row in llrs:
        row["SR-Refs"] = "SR-001" if row["LLR-ID"] == "LLR-001" else "SR-002"
    view, unplaced = gen_components.build(cmps, srs, llrs, ifs, tcs, {})
    assert view["CMP-001"]["llr_refs"] == {"LLR-001", "LLR-002"}
    assert view["CMP-002"]["llr_refs"] == {"LLR-001"}
    assert view["CMP-002"]["sr_refs"] == {"SR-001"}
    assert unplaced["llr_refs"] == ["LLR-003", "LLR-004"]
    # Of twelve unplaced rows the line names the first ten and counts the rest.
    many = [{"LLR-ID": "LLR-{:03d}".format(n)} for n in range(10, 22)]
    line = trace.placement_line(many, tcs, ifs)
    assert line.startswith("placement: 0 design row(s) placed, 12 unplaced (LLR-010, ")
    assert "LLR-019, +2 more)" in line and "LLR-020" not in line, line


VIEW_REGISTRIES = {
    "docs/requirements/components.toml": (
        '[component.CMP-001]\nname = "one"\ncategory = "software"\nstatus = "Accepted"\n'
        '\n[component.CMP-002]\nname = "two"\ncategory = "software"\n'
        'status = "Accepted"\n'
    ),
    "docs/requirements/system-requirements.toml": (
        '[requirement.SR-001]\ntitle = "t"\nstatus = "Accepted"\n'
    ),
    "docs/requirements/low-level-requirements.toml": "".join(
        '[design.LLR-00{}]\nsr_refs = ["SR-001"]\ntitle = "t{}"\nstatus = "Accepted"\n\n'.format(
            n, n
        )
        for n in (1, 2, 3)
    ),
    "docs/requirements/interfaces.toml": (
        '[interface.IF-001]\nowner = "CMP-001"\nconsumers = ["CMP-001"]\n'
        'channel = "call"\n\n[interface.IF-002]\nowner = "CMP-002"\n'
        'consumers = ["CMP-002"]\nchannel = "call"\n'
    ),
    "docs/test/test-cases.toml": (
        '[test.TC-001]\nverifies = ["LLR-001", "IF-001", "IF-002"]\n\n'
        '[test.TC-002]\nverifies = ["LLR-002", "IF-001"]\n\n'
        '[test.TC-003]\nverifies = ["LLR-003"]\n'
    ),
}


def test_the_views_show_where_each_design_row_sits(tmp_path):
    """Implements: TC-480"""
    for rel, text in VIEW_REGISTRIES.items():
        _write(tmp_path, rel, text)
    # The component view, rendered: the unplaced row listed and counted.
    doc = tomllib.loads(gen_components.render(tmp_path))
    assert doc["unplaced"]["llr_refs"] == ["LLR-003"]
    assert doc["derived"]["design_rows_unplaced"] == 1
    # The state view's design-row detail: each row's components, or unplaced.
    _svg, details, _desc = load_script("gen_trajectory").arch_icicle(tmp_path)
    assert details["LLR-001"]["meta"] == "Placed: CMP-001, CMP-002"
    assert details["LLR-002"]["meta"] == "Placed: CMP-001"
    assert details["LLR-003"]["meta"] == "Placed: unplaced"


def test_a_design_row_is_discharged_by_a_case_of_any_kind():
    """Implements: TC-485"""
    srs = [{"SR-ID": "SR-001", "Status": "Accepted"}]
    llrs = [
        {"LLR-ID": "LLR-001", "SR-Refs": "SR-001", "Status": "Accepted"},
        {"LLR-ID": "LLR-002", "SR-Refs": "SR-001", "Status": "Accepted"},
        {"LLR-ID": "LLR-003", "SR-Refs": "SR-001", "Status": "Accepted"},
        {"LLR-ID": "LLR-004", "SR-Refs": "SR-001", "Status": "Drafted"},
    ]
    tcs = [
        # An automated case, and an inspection a person carries out.
        {"TC-ID": "TC-001", "Verifies": "SR-001; LLR-001", "Automated": "Yes"},
        {"TC-ID": "TC-002", "Verifies": "LLR-002", "Automated": "No"},
    ]
    findings, at_fault = coherence.spine_orphan_findings(
        srs, llrs, tcs, [], {"SR-001"}, {r["LLR-ID"] for r in llrs}, set(), set()
    )
    # Either kind discharges its row; the Drafted row owes no case yet.
    assert [f for f in findings if f.startswith("LLR ")] == [
        "LLR LLR-003 has no test (TC)"
    ]
    assert "LLR-003" in at_fault
    assert not {"LLR-001", "LLR-002", "LLR-004"} & at_fault


LLR_ROW = '[design.LLR-001]\nsr_refs = ["SR-001"]\ntitle = "t"\nstatus = "Drafted"\n'


def test_the_loader_refuses_a_key_a_requirement_tier_does_not_declare(tmp_path):
    """Implements: TC-481"""
    reg = _write(tmp_path, LLR_REL, LLR_ROW + 'module = "src/a.py"\n')
    with pytest.raises(SystemExit) as exc:
        spine_carrier.load(reg, "LLR-ID")
    assert "LLR-001" in str(exc.value) and "`module`" in str(exc.value)
    # Every requirement tier, the example row included.
    sr = _write(
        tmp_path,
        "docs/requirements/system-requirements.toml",
        '[requirement.SR-000]\ntitle = "t"\nowner = "CMP-001"\n',
    )
    with pytest.raises(SystemExit) as exc:
        spine_carrier.load(sr, "SR-ID")
    assert "SR-000" in str(exc.value) and "`owner`" in str(exc.value)
    tc = _write(
        tmp_path, TC_REL, '[test.TC-001]\nverifies = ["LLR-001"]\nmodule = "x"\n'
    )
    with pytest.raises(SystemExit):
        spine_carrier.load(tc, "TC-ID")
    # A declared row loads; an off-spine tier is not judged here.
    assert spine_carrier.load(_write(tmp_path, LLR_REL, LLR_ROW), "LLR-ID")
    ifs = _write(
        tmp_path,
        "docs/requirements/interfaces.toml",
        '[interface.IF-001]\nowner = "CMP-001"\nextra = "kept"\n',
    )
    assert spine_carrier.load(ifs, "IF-ID")[0]["extra"] == "kept"
    # The approval snapshot is the act's record, read without the key rule:
    # its copy keeps the retired cells until the act that re-takes it.
    snap = baseline_snapshot.snapshot_root(tmp_path)
    _write(snap, LLR_REL, LLR_ROW.replace("Drafted", "Accepted") + 'module = "a"\n')
    rows = baseline_snapshot.load_all(tmp_path)
    assert rows[(spine_carrier.stem(LLR_REL), "LLR-ID")]["LLR-001"]["Module"] == "a"
    # History is read as it was written, too: a revision before the change
    # keeps the cells, so the stage's before-side and the id sweep read it.
    hist = tmp_path / "history"
    _write(hist, LLR_REL, LLR_ROW + 'module = "src/a.py"\n')
    spine = spine_rules.load_spine(hist / "docs", declared=False)
    assert spine["llrs"][0]["Module"] == "src/a.py"
    assert ("LLR", 1) in trace.live_ids(hist)


def test_every_refusal_names_the_file_the_row_and_the_key(tmp_path):
    """Implements: TC-481"""
    # Each of the three retired design-row cells, not the file cell alone.
    for key in ("module", "code_symbol", "component"):
        reg = _write(tmp_path, LLR_REL, LLR_ROW + '{} = "x"\n'.format(key))
        with pytest.raises(SystemExit) as exc:
            spine_carrier.load(reg, "LLR-ID")
        why = str(exc.value)
        assert str(reg) in why and "LLR-001" in why and "`{}`".format(key) in why
    # The need tier too, its example row included.
    sn = _write(
        tmp_path,
        "docs/requirements/stakeholder-needs.toml",
        '[need.SN-000]\nneed = "n"\nowner = "STK-01"\n',
    )
    with pytest.raises(SystemExit) as exc:
        spine_carrier.load(sn, "SN-ID")
    why = str(exc.value)
    assert str(sn) in why and "SN-000" in why and "`owner`" in why


def test_the_retired_design_cells_stay_classed_traced():
    """Implements: TC-481"""
    # Removing them is a traced change: the accepted text does not move.
    for column in ("Module", "CodeSymbol", "Component"):
        assert acceptance_record.spine_cell_class(LLR_REL, column) == "traced"
    row = {"LLR-ID": "LLR-001", "SR-Refs": "SR-001", "Title": "t", "Detail": "d"}
    old = dict(row, Module="src/a.py", CodeSymbol="run", Component="CMP-001")
    digest = acceptance_record.accepted_text_digest
    assert digest(LLR_REL, "LLR-ID", old) == digest(LLR_REL, "LLR-ID", row)


def test_the_implements_index_feeds_the_module_listing(tmp_path, capsys, monkeypatch):
    """Implements: TC-482"""
    _write(
        tmp_path,
        "docs/stack.ini",
        "[paths]\nsrc = src\ntests = tests\n[arch-map]\nheaders = docs/reg.toml\n",
    )
    _write(tmp_path, "src/pay.py", '"""Pay.\n\nImplements: LLR-001, SR-001\n"""\n')
    _write(
        tmp_path, "src/lib/ledger.py", "# Implements: LLR-002\n# Implements: LLR-001\n"
    )
    _write(tmp_path, "src/notes.py", '"""Prose naming LLR-009 is no declaration."""\n')
    _write(tmp_path, "docs/reg.toml", "# Implements: LLR-003\n")
    index = arch_inputs.implements_index(tmp_path)
    assert index == {
        "LLR-001": ["src/lib/ledger.py", "src/pay.py"],
        "LLR-002": ["src/lib/ledger.py"],
        "LLR-003": ["docs/reg.toml"],
        "SR-001": ["src/pay.py"],
    }
    tcs = [
        {
            "TC-ID": "TC-001",
            "Verifies": "LLR-001",
            "Evidence": "tests/test_checkout.py",
        },
        {"TC-ID": "TC-002", "Verifies": "LLR-002", "Evidence": "tests/test_ledger.py"},
        {"TC-ID": "TC-003", "Verifies": "SR-001", "Evidence": "tests/test_sr.py"},
    ]
    assert spine.module_tests(index, tcs, "src/pay.py") == ["tests/test_checkout.py"]
    assert spine.module_tests(index, tcs, "src/lib/ledger.py") == [
        "tests/test_checkout.py",
        "tests/test_ledger.py",
    ]
    assert spine.resolve_modules(index, "ledger") == ["src/lib/ledger.py"]
    assert spine.resolve_modules(index, "notes") == []
    # The command reads the index of the repository holding the docs directory.
    _write(
        tmp_path,
        TC_REL,
        '[test.TC-001]\nverifies = ["LLR-001"]\nevidence = "tests/test_checkout.py"\n',
    )
    _write(tmp_path, LLR_REL, LLR_ROW)
    assert _main(monkeypatch, "--root", tmp_path, "--tests-for", "pay") == 0
    assert capsys.readouterr().out.splitlines() == ["tests/test_checkout.py"]
    assert _main(monkeypatch, "--root", tmp_path, "--tests-for", "notes") == 1
    assert "no file an Implements: tag" in capsys.readouterr().err


def test_the_index_reads_past_what_it_cannot_read(tmp_path, monkeypatch):
    """Implements: TC-482"""
    _write(
        tmp_path,
        "docs/stack.ini",
        "[paths]\nsrc = src\n[arch-map]\nheaders = docs/reg.toml docs/gone.toml\n",
    )
    _write(tmp_path, "src/pay.py", "# Implements: LLR-001\n")
    _write(tmp_path, "docs/reg.toml", "# Implements: LLR-003\n")
    # Bytes that do not decode, a read that fails, and a listed header that is
    # not there add nothing; the rest is indexed.
    (tmp_path / "src" / "latin.py").write_bytes(b"# Implements: LLR-007 \xff\xfe\n")
    _write(tmp_path, "src/locked.py", "# Implements: LLR-008\n")
    read_text = Path.read_text

    def refusing(path, *args, **kwargs):
        if path.name == "locked.py":
            raise OSError("locked")
        return read_text(path, *args, **kwargs)

    monkeypatch.setattr(Path, "read_text", refusing)
    assert arch_inputs.implements_index(tmp_path) == {
        "LLR-001": ["src/pay.py"],
        "LLR-003": ["docs/reg.toml"],
    }
    # With the source root gone, the listed header's declarations remain.
    shutil.rmtree(tmp_path / "src")
    assert arch_inputs.implements_index(tmp_path) == {"LLR-003": ["docs/reg.toml"]}


def test_the_build_brief_marks_a_design_row_no_declaration_names(tmp_path):
    """Implements: TC-482"""
    _write(tmp_path, "docs/stack.ini", "[paths]\nsrc = src\n")
    _write(tmp_path, "src/pay.py", "# Implements: LLR-001\n")
    _write(
        tmp_path,
        LLR_REL,
        LLR_ROW + '\n[design.LLR-002]\nsr_refs = ["SR-001"]\ntitle = "u"\n'
        'status = "Drafted"\n',
    )
    text = intake.context_block(tmp_path, {"WI-ID": "WI-001", "SR-Refs": "SR-001"}, [])
    lines = text.splitlines()
    assert [ln for ln in lines if ln.startswith("- LLR-001 [src/pay.py]")], text
    assert [ln for ln in lines if ln.startswith("- LLR-002 [no Implements: tag]")], text


def test_the_evidence_column_is_generated_from_the_tags(tmp_path, monkeypatch):
    """Implements: TC-483"""
    gen = arch_tags.generated_evidence
    tagged = {"tests/test_a.py", "tests/test_b.py::test_x", "tests/test_n.py::test_y"}
    cell = (
        "tests/test_a.py; docs/review.md; tests/test_b.py::test_x[case one]; "
        "tests/test_old.py (a note)"
    )
    # Outside the root, a note and a tagged part (its case kept) stay verbatim;
    # an untagged part goes with its separator; a declared node is appended.
    assert gen(cell, tagged, "tests") == (
        "tests/test_a.py; docs/review.md; tests/test_b.py::test_x[case one]; "
        "(a note); tests/test_n.py::test_y"
    )
    # A part in a file refused as unreadable is kept: its tags are unknown.
    assert gen("tests/test_bad.py", set(), "tests", {"tests/test_bad.py"}) == (
        "tests/test_bad.py"
    )
    # The identity wherever the parts equal the tags, whatever the separators.
    for same in ("tests/test_a.py", "tests/test_a.py;tests/test_b.py::test_x"):
        parts = {p + ("::" + n if n else "") for p, n in spine.evidence_items(same)}
        assert gen(same, parts, "tests") == same
    assert gen("", {"tests/test_a.py"}, "tests") == "tests/test_a.py"
    # The writer changes the stale cell alone, and a second run nothing.
    _write(tmp_path, "docs/stack.ini", "[paths]\nsrc = src\ntests = tests\n")
    _write(tmp_path, "tests/test_a.py", '"""Implements: TC-001"""\n')
    _write(tmp_path, "tests/test_b.py", '"""Implements: TC-002"""\n')
    reg = _write(
        tmp_path,
        TC_REL,
        "# header\n\n[test.TC-001]\n"
        'verifies = ["LLR-001"]\nmethod = """evidence = "x"\n"""\n'
        'evidence = "tests/test_a.py"\n\n'
        '[test.TC-002]\nverifies = ["LLR-001"]\nevidence = "tests/test_gone.py"\n',
    )
    assert _main(monkeypatch, "--root", tmp_path, "--regen-evidence") == 0
    assert reg.read_text(encoding="utf-8") == (
        "# header\n\n[test.TC-001]\n"
        'verifies = ["LLR-001"]\nmethod = """evidence = "x"\n"""\n'
        'evidence = "tests/test_a.py"\n\n'
        '[test.TC-002]\nverifies = ["LLR-001"]\nevidence = "tests/test_b.py"\n'
    )
    assert arch_tags.evidence_regen(tmp_path, "tests") == {}
    # This repository's generated cells equal today's on every row.
    assert arch_tags.evidence_regen(ROOT, "tests") == {}


def test_an_emptied_cell_loses_its_key_and_the_command_names_the_cases(
    tmp_path, capsys, monkeypatch
):
    """Implements: TC-483"""
    _write(tmp_path, "docs/stack.ini", "[paths]\nsrc = src\ntests = tests\n")
    _write(tmp_path, "tests/test_b.py", '"""Implements: TC-002"""\n')
    reg = _write(
        tmp_path,
        TC_REL,
        '[test.TC-001]\nverifies = ["LLR-001"]\nevidence = "tests/test_gone.py"\n'
        'status = "Drafted"\n\n'
        '[test.TC-002]\nverifies = ["LLR-001"]\nstatus = "Drafted"\n',
    )
    assert _main(monkeypatch, "--root", tmp_path, "--regen-evidence") == 0
    assert capsys.readouterr().out.splitlines() == [
        "trace: evidence regenerated for TC-001, TC-002"
    ]
    # TC-001's only part leaves, and its key with it; TC-002 gains one.
    assert reg.read_text(encoding="utf-8") == (
        '[test.TC-001]\nverifies = ["LLR-001"]\nstatus = "Drafted"\n\n'
        '[test.TC-002]\nverifies = ["LLR-001"]\nstatus = "Drafted"\n'
        'evidence = "tests/test_b.py"\n'
    )


def test_a_rewrite_that_does_not_re_read_is_refused_and_writes_nothing(
    tmp_path, monkeypatch
):
    """Implements: TC-483"""
    # A quoted key reads as the same cell, but the line rewrite cannot see it:
    # it adds a second key, the result does not re-read, and nothing is written.
    _write(tmp_path, "docs/stack.ini", "[paths]\nsrc = src\ntests = tests\n")
    _write(tmp_path, "tests/test_b.py", '"""Implements: TC-001"""\n')
    reg = _write(
        tmp_path,
        TC_REL,
        '[test.TC-001]\nverifies = ["LLR-001"]\n"evidence" = "tests/test_gone.py"\n',
    )
    before = reg.read_bytes()
    code = _main(monkeypatch, "--root", tmp_path, "--regen-evidence")
    assert "REFUSED" in str(code) and "nothing written" in str(code), code
    assert reg.read_bytes() == before


def test_with_no_registry_or_no_tests_root_the_regeneration_says_so(
    tmp_path, capsys, monkeypatch
):
    """Implements: TC-483"""
    # No test-case registry: nothing is read or written, and the command names
    # the missing input rather than calling every cell current.
    _write(tmp_path, "docs/stack.ini", "[paths]\nsrc = src\ntests = tests\n")
    _write(tmp_path, "tests/test_a.py", '"""Implements: TC-001"""\n')
    assert _main(monkeypatch, "--root", tmp_path, "--regen-evidence") == 0
    out = capsys.readouterr().out
    assert "no test-case registry" in out and "current" not in out, out
    assert not (tmp_path / TC_REL).exists()
    # No tests root: the registry stays byte for byte, and the command says so.
    other = tmp_path / "other"
    _write(other, "docs/stack.ini", "[paths]\nsrc = src\ntests = spec\n")
    reg = _write(
        other,
        TC_REL,
        '[test.TC-001]\nverifies = ["LLR-001"]\nevidence = "spec/test_a.py"\n',
    )
    before = reg.read_bytes()
    assert _main(monkeypatch, "--root", other, "--regen-evidence") == 0
    out = capsys.readouterr().out
    assert "no tests root" in out and "spec" in out and "current" not in out, out
    assert reg.read_bytes() == before


def test_the_migration_drops_the_three_cells_and_nothing_else(tmp_path):
    """Implements: TC-484"""
    before = (
        "# the registry header\n\n"
        "[design.LLR-001]\n"
        'sr_refs = ["SR-001"]\n'
        'title = "t"\n'
        'module = "src/a.py;src/b.py"\n'
        'code_symbol = """run/\n'
        'classify"""\n'
        'detail = """Prose quoting a cell:\n'
        'module = "kept, it is text"\n'
        '"""\n'
        'status = "Accepted"\n'
        'component = "CMP-001"\n'
        "phase = 1\n\n"
        "[design.LLR-002]\n"
        'sr_refs = ["SR-001"]\n'
        'title = "u"\n'
        'status = "Drafted"\n'
    )
    after = (
        "# the registry header\n\n"
        "[design.LLR-001]\n"
        'sr_refs = ["SR-001"]\n'
        'title = "t"\n'
        'detail = """Prose quoting a cell:\n'
        'module = "kept, it is text"\n'
        '"""\n'
        'status = "Accepted"\n'
        "phase = 1\n\n"
        "[design.LLR-002]\n"
        'sr_refs = ["SR-001"]\n'
        'title = "u"\n'
        'status = "Drafted"\n'
    )
    reg = _write(tmp_path, LLR_REL, before)
    report, written = migrate_carrier.drop_llr_trace_cells(tmp_path, write=False)
    assert written == [] and reg.read_text(encoding="utf-8") == before
    assert report[0].endswith("1 row(s) lose module, code_symbol and component")
    report, written = migrate_carrier.drop_llr_trace_cells(tmp_path, write=True)
    assert written == [reg] and reg.read_text(encoding="utf-8") == after
    assert spine_carrier.load(reg, "LLR-ID")
    report, written = migrate_carrier.drop_llr_trace_cells(tmp_path, write=True)
    assert written == [] and report[0].endswith(
        "0 row(s) lose module, code_symbol and component"
    )
    assert migrate_carrier.main(["--root", str(tmp_path), "--llr-trace-cells"]) == 0


def test_the_migration_keeps_crlf_line_ends(tmp_path):
    """Implements: TC-484"""
    # Every other byte kept means the line ends too: a CRLF registry comes back
    # CRLF, a multi-line value's inner line end included.
    before = (
        "# the registry header\r\n\r\n"
        "[design.LLR-001]\r\n"
        'sr_refs = ["SR-001"]\r\n'
        'module = "src/a.py"\r\n'
        'code_symbol = """run/\r\n'
        'classify"""\r\n'
        'detail = """Two\r\n'
        'lines"""\r\n'
        'component = "CMP-001"\r\n'
        'status = "Accepted"\r\n'
    )
    after = (
        "# the registry header\r\n\r\n"
        "[design.LLR-001]\r\n"
        'sr_refs = ["SR-001"]\r\n'
        'detail = """Two\r\n'
        'lines"""\r\n'
        'status = "Accepted"\r\n'
    )
    reg = _write(tmp_path, LLR_REL, before)
    report, written = migrate_carrier.drop_llr_trace_cells(tmp_path, write=True)
    assert written == [reg] and reg.read_bytes() == after.encode("utf-8")


def test_the_migration_drops_a_multi_line_literal_value(tmp_path):
    """Implements: TC-484"""
    # A multi-line literal string is a multi-line value too, and a kept literal
    # cell quoting a basic-string delimiter and an assignment stays whole.
    before = (
        "[design.LLR-001]\n"
        'sr_refs = ["SR-001"]\n'
        "code_symbol = '''run/\n"
        "classify'''\n"
        "detail = '''Prose quoting \"\"\" and a cell:\n"
        'module = "kept, it is text"\n'
        "'''\n"
        'status = "Drafted"\n'
    )
    after = (
        "[design.LLR-001]\n"
        'sr_refs = ["SR-001"]\n'
        "detail = '''Prose quoting \"\"\" and a cell:\n"
        'module = "kept, it is text"\n'
        "'''\n"
        'status = "Drafted"\n'
    )
    reg = _write(tmp_path, LLR_REL, before)
    report, written = migrate_carrier.drop_llr_trace_cells(tmp_path, write=True)
    assert written == [reg] and reg.read_bytes() == after.encode("utf-8")
    assert report[0].endswith("1 row(s) lose module, code_symbol and component")


def test_an_absent_registry_is_reported_and_nothing_is_written(tmp_path, capsys):
    """Implements: TC-484"""
    report, written = migrate_carrier.drop_llr_trace_cells(tmp_path, write=True)
    assert written == []
    assert report == ["{}: absent, nothing to migrate".format(LLR_REL)]
    assert migrate_carrier.main(["--root", str(tmp_path), "--llr-trace-cells"]) == 0
    assert "absent, nothing to migrate" in capsys.readouterr().out
    assert not (tmp_path / LLR_REL).exists()


def test_a_migration_that_does_not_re_read_is_refused_and_writes_nothing(tmp_path):
    """Implements: TC-484"""
    # A quoted key reads as the file cell, but the line remover cannot see it:
    # the rewrite keeps the cell, does not re-read as the rows less the three
    # cells, and nothing is written.
    reg = _write(tmp_path, LLR_REL, LLR_ROW + '"module" = "src/a.py"\n')
    before = reg.read_bytes()
    with pytest.raises(SystemExit) as exc:
        migrate_carrier.drop_llr_trace_cells(tmp_path, write=True)
    assert "REFUSED" in str(exc.value) and str(reg) in str(exc.value)
    assert reg.read_bytes() == before
