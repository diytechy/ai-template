"""trace.py golden-master net (WI-081 Slice A).

A behavior-preserving decomposition of trace.py's main() into analyze() +
render_report() (docs/specs/main-decomposition.md §4) must not move a byte of
the generated report, the console summary, or the exit code. These tests pin
exactly that: for three fixture states (a clean spine, an off-spine-rich spine,
and an orphaned spine) they regenerate the report and compare it — plus the
normalized stdout and the return code — against committed golden files captured
from the pre-refactor code. Slices B–D are byte-locked by this net.

Regenerate the goldens (only when a change to trace.py's OUTPUT is intended and
reviewed) with:  UPDATE_TRACE_GOLDEN=1 python -m pytest tests/test_trace_golden.py
"""

import os

from conftest import make_minimal_project, record_ids, run_py

GOLDEN = os.path.join(os.path.dirname(__file__), "golden")

# --- An off-spine-rich, orphan-free spine ------------------------------------
# Exercises every report section the minimal chain does not: the PB/REPO/PART/
# ASSET/CMP/IF back-link renders, the knowledge-pack + AC advisories, the draft
# artifacts section (a Draft SR + a section-as-state Draft SN), the three-way
# verification-basis split (an Attest SR — mechanized/demonstrated/attested,
# WI-259), and the per-Area counts.

RICH_SN = """# Stakeholder Needs (SN-###)

| SN-ID | Need | Why | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-001 | Add two numbers. | Demo. | M | add(1,2) gives 3. |
| SN-002 | Document the adder. | Trust. | S | A page exists. |

## Draft needs (unratified)

| SN-ID | Need | Why | Priority | Acceptance intent |
|---|---|---|---|---|
| SN-003 | A future capability. | Later. | C | TBD. |
"""

RICH_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status,Aspect
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified,process
SR-002,Docs,SN-002,"The system shall ship a doc.","Realizes SN-002.","the page is identical to the source",,S,Attest,Verified,trajectory
SR-003,Future,SN-002,"The system shall do a future thing.","Drafted first.","TBD",,C,Test,Draft,process
"""

RICH_LLRS = """LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component
LLR-001,SR-001,Pure adder,src/demo,add,"Pure function: two numbers -> sum.",(see TC),Implemented,CMP-001
"""

RICH_TCS = """TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status
TC-001,SR-001;LLR-001,Unit,call add,Smoke,"a=1; b=2","Satisfies SR-001",Yes,tests/test_demo.py::test_add_sr001,Verified
TC-002,SR-002,Manual,read the page,Full,,"The page exists",No,,Verified
"""

RICH_PBS = """PB-ID,Metric,Refs,Budget,Unit,Tolerance,Direction,Tier,Gate,Owner,Notes
PB-001,latency,SR-001,10,ms,1,<=,Smoke,DevBar-Release,core,demo budget
"""

RICH_REPOS = """REPO-ID,Name,Repo,DelegatedSRs,Version,Type,Owner,Notes
REPO-001,adder-lib,git@x:adder,SR-001,1.0,library,core,demo delegation
"""

RICH_PARTS = """PART-ID,Name,IF-Ref,Vendor,Cost,Status,Quantity,Notes,Component
PART-001,widget,IF-001,acme,0,in-use,1,demo part,CMP-001
"""

RICH_ASSETS = """ASSET-ID,Name,Refs,Kind,Provenance,License,Attribution,ContractRef,Location,Hash,Version,Notes,Component
ASSET-001,logo,SR-001,image,made,MIT,none,none,assets/logo.png,abc,1,demo asset,CMP-001
"""

RICH_CMPS = """[component.CMP-001]
name = "Adder"
category = "core"
knowledge = "docs/knowledge/missing-pack"
state = "built"
detail_doc = "docs/cmp/adder.md"
notes = "demo component"
"""

# `direction` READS `Provides` here and read `out` until 2026-08-15, when the IF
# tier's `Direction` vocabulary was finally closed and caught it: `in|out|inout`
# is the depth-0 BOUNDARY tier's vocabulary, and it had leaked into an interface
# fixture where nothing could see it. `counterpart` is a cross-repo endpoint, so
# it carries the external marker rather than reading as a dangling path.
RICH_IFS = """[interface.IF-001]
direction = "Provides"
this_project = "src/demo"
counterpart = "external:acme/widget"
contract = "call"
signal = "discrete"
req_refs = ["SR-001"]
owner = "SR-001"
version = "1"
approval = "approved"
component = "CMP-001"
notes = "demo seam"
"""

ORPHAN_SRS = """SR-ID,Title,SN-Refs,Requirement,Rationale,AcceptanceCriteria,Permutations,Priority,Verification,Status
SR-001,Addition,SN-001,"The system shall add two numbers.","Realizes SN-001.","add(1,2) == 3",,M,Test,Verified
SR-002,Orphaned,SN-001,"The system shall do something untested.","Demo orphan.","n/a",,M,Test,Planned
"""


def _make_rich(root):
    make_minimal_project(root)
    req = root / "docs" / "requirements"
    (req / "stakeholder-needs.md").write_text(RICH_SN, encoding="utf-8")
    (req / "system-requirements.csv").write_text(RICH_SRS, encoding="utf-8")
    (req / "low-level-requirements.csv").write_text(RICH_LLRS, encoding="utf-8")
    (root / "docs" / "test" / "test-cases.csv").write_text(RICH_TCS, encoding="utf-8")
    (req / "performance-budgets.csv").write_text(RICH_PBS, encoding="utf-8")
    (req / "repos.csv").write_text(RICH_REPOS, encoding="utf-8")
    (req / "procurement.csv").write_text(RICH_PARTS, encoding="utf-8")
    (req / "assets.csv").write_text(RICH_ASSETS, encoding="utf-8")
    (req / "components.toml").write_text(RICH_CMPS, encoding="utf-8")
    (req / "interfaces.toml").write_text(RICH_IFS, encoding="utf-8")
    record_ids(root)


def _normalize(text, root):
    """Strip the run-specific tmp path from the summary's `Report -> <path>` tail
    and force POSIX separators, so one golden set is location- AND platform-
    independent — a Windows run emits `docs\\test\\report.md` in that tail where
    a POSIX run emits forward slashes (WI-192)."""
    text = text.replace(str(root).replace("\\", "/"), "<ROOT>").replace(
        str(root), "<ROOT>"
    )
    return text.replace("\\", "/")


def _assert_golden(name, report, stdout, root):
    body = report + "\n===STDOUT===\n" + _normalize(stdout, root)
    path = os.path.join(GOLDEN, name)
    if os.environ.get("UPDATE_TRACE_GOLDEN"):
        os.makedirs(GOLDEN, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(body)
        return
    with open(path, encoding="utf-8") as fh:
        expected = fh.read()
    assert body == expected, (
        "golden mismatch for {} — regenerate deliberately with "
        "UPDATE_TRACE_GOLDEN=1 only if the output change is intended".format(name)
    )


def _report(root):
    return (root / "docs" / "test" / "report.md").read_text(encoding="utf-8")


def test_golden_clean_spine(scaffold):
    make_minimal_project(scaffold)
    proc = run_py(
        [
            "scripts/trace.py",
            "--strict-schema",
            "--no-placeholders",
            "--require-verified",
        ],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    _assert_golden("clean.txt", _report(scaffold), proc.stdout, scaffold)


def test_golden_offspine_rich_spine(scaffold):
    _make_rich(scaffold)
    proc = run_py(
        ["scripts/trace.py", "--require-verified", "--html"],
        cwd=scaffold,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
    _assert_golden("offspine.txt", _report(scaffold), proc.stdout, scaffold)


def test_golden_orphaned_spine(scaffold):
    make_minimal_project(scaffold)
    (scaffold / "docs" / "requirements" / "system-requirements.csv").write_text(
        ORPHAN_SRS, encoding="utf-8"
    )
    record_ids(scaffold)
    proc = run_py(["scripts/trace.py", "--strict"], cwd=scaffold)
    assert proc.returncode == 1
    _assert_golden("orphan.txt", _report(scaffold), proc.stdout, scaffold)


def test_normalize_forces_posix_separators():
    """WI-192 separator stability: the compared body must not depend on os.sep,
    so a Windows-captured `Report -> docs\\test\\report.md` tail normalizes to
    the same forward-slash form a POSIX run produces."""
    root = os.path.join("tmp", "run")
    assert _normalize("Report -> docs\\test\\report.md", root) == (
        "Report -> docs/test/report.md"
    )


def test_goldens_are_platform_stable():
    """WI-192 encoding + separator stability: the checked-in goldens must be one
    set that passes on both platforms — no os.sep backslash (a Windows-captured
    path tail) and no cp1252 mojibake (an em-dash decoded through the console
    codepage). Guards the net against a silent per-platform re-fork on the next
    UPDATE_TRACE_GOLDEN regeneration."""
    for name in ("clean.txt", "offspine.txt", "orphan.txt"):
        with open(os.path.join(GOLDEN, name), encoding="utf-8") as fh:
            text = fh.read()
        assert "\\" not in text, name + " carries an os.sep backslash separator"
        assert "â€”" not in text, name + " carries cp1252 mojibake"
