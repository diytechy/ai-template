"""check_trajectory.py — decision over architecture inputs (WI-277: split
verbatim from tests/test_trajectory.py by behavior boundary).

Interface-connectivity coverage (WI-056), the How-SW top-view right-sizing
bound (WI-073/FB5), knowledge⇒component coupling (WI-153), cross-CMP edges
without a declared IF (WI-064), specs
acting on declared interface boundaries (WI-191), the component
partition's derivation record (WI-999), and an accepted automated test case
no test declares (WI-1001).

check_vocab: allow-file — THE ANCHOR FIXTURES MUST AUTHOR THE RETIRED SPELLING.
`check_trajectory` TRANSLATES `[p]-[g1]`/`[p]-[reqs]` on read and never rewrites
a committed WI title, so the only way to prove the translation still works is to
build titles carrying it. A file-level marker rather than ~25 line-level ones:
every occurrence here is one fixture class with one reason, and a marker per line
would say the same thing 25 times while hiding whether a NEW one had appeared.
"""

import ast
import csv
import re
import shutil
import sys
from pathlib import Path

import pytest


from conftest import ROOT, SCRIPTS, load_script, run_py

# `kitlib` is a PACKAGE UNDER scripts/, which nothing puts on `sys.path` until
# the first `load_script` call — so a module-level `from kitlib import ...` in a
# test file resolves only when some earlier-collected module happens to have
# called it first. That held by accident until an xdist worker collected this
# module first (WI-498 slice 4). Stated explicitly here rather than inherited.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))


wi_convert = load_script("wi_convert")
check_trajectory = load_script("check_trajectory")
trajectory_arch = load_script("trajectory_arch")


def test_architecture_rules_are_reexported_from_their_behavior_module():
    """Implements: TC-080"""
    for name, home in (
        ("interface_findings", "arch_interfaces"),
        ("component_findings", "arch_components"),
        ("cross_component_findings", "arch_seams"),
        ("spec_interface_findings", "trajectory_arch"),
    ):
        facade = getattr(check_trajectory, name)
        behavior = getattr(load_script(home), name)
        assert facade.__module__ == home
        assert facade.__code__.co_code == behavior.__code__.co_code


# The modules `trajectory_arch` composes (WI-1007): the rules it held moved into
# them, and it re-exports their surface to `check_trajectory` (IF-263).
COMPOSED = (
    "arch_inputs",
    "arch_interfaces",
    "arch_tags",
    "arch_seams",
    "arch_components",
)


def _defined_names(path):
    """The top-level names a module defines: its defs, classes and assignments."""
    names = set()
    for node in ast.parse(path.read_text(encoding="utf-8")).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names.add(node.name)
        elif isinstance(node, ast.Assign):
            names.update(t.id for t in node.targets if isinstance(t, ast.Name))
    return names


def test_the_composer_exposes_every_public_name_of_the_modules_it_composes():
    """Each public name a composed module defines, and each name the composer's
    `__all__` lists, resolves on `trajectory_arch`. The split moved
    `derivation_record_findings`, a public name of the module before it, and
    left it off the composer, which no caller happened to read.

    Implements: TC-080"""
    composer = load_script("trajectory_arch")
    missing = [
        "{}.{}".format(module, name)
        for module in COMPOSED
        for name in sorted(_defined_names(SCRIPTS / (module + ".py")))
        if not name.startswith("_") and not hasattr(composer, name)
    ]
    missing += [name for name in composer.__all__ if not hasattr(composer, name)]
    assert missing == []


def _loads_composer(node):
    """True for a `load_script("trajectory_arch")`-shaped call."""
    return (
        isinstance(node, ast.Call)
        and bool(node.args)
        and isinstance(node.args[0], ast.Constant)
        and node.args[0].value == "trajectory_arch"
    )


def _composer_binding(node):
    """`(aliases, names)` that one statement binds from `trajectory_arch`."""
    if isinstance(node, ast.Import):
        return {
            a.asname or a.name for a in node.names if a.name == "trajectory_arch"
        }, set()
    if isinstance(node, ast.ImportFrom) and node.module == "trajectory_arch":
        return set(), {a.name for a in node.names}
    if isinstance(node, ast.Assign) and _loads_composer(node.value):
        return {t.id for t in node.targets if isinstance(t, ast.Name)}, set()
    return set(), set()


def _composer_names(tree):
    """`(aliases, names)`: the names a module binds to `trajectory_arch`, by
    an import or by loading it, and the names it imports from it."""
    aliases, names = set(), set()
    for node in ast.walk(tree):
        bound, imported = _composer_binding(node)
        aliases |= bound
        names |= imported
    return aliases, names


def _composer_reads(tree):
    """Every name a module reads through `trajectory_arch`."""
    aliases, names = _composer_names(tree)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Attribute):
            continue
        value = node.value
        if _loads_composer(value) or (
            isinstance(value, ast.Name) and value.id in aliases
        ):
            names.add(node.attr)
    return names


def test_every_name_a_caller_reads_through_the_composer_resolves():
    """A kit script, a repository tool or a test that imports a name from
    `trajectory_arch`, or reads one off it, finds it there.

    Implements: TC-080"""
    composer = load_script("trajectory_arch")
    unresolved = []
    for tree_root in (SCRIPTS, ROOT / "scripts", ROOT / "tests"):
        for path in sorted(tree_root.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            reads = _composer_reads(ast.parse(path.read_text(encoding="utf-8")))
            unresolved += [
                "{}: {}".format(path.relative_to(ROOT).as_posix(), name)
                for name in sorted(reads)
                if not hasattr(composer, name)
            ]
    assert unresolved == []


# The registry-fixture writers below are copied from tests/test_trajectory.py
# rather than imported — no test module in this suite imports another, and
# conftest is not this module's to extend (the suite idiom test_integrate.py's
# `git_repo` states; WI-277 kept it when splitting the monolith).
# The fixture bodies below stay CSV-SHAPED — one line per work item, cells in one
# of these two column orders — because a table is how a registry fixture reads.
# The registry's one HOME is the `docs/work/` spec folder (concurrency-restructure
# Phase 5, RULING-4: the CSV home retired, and a work-items.csv left on disk is
# now itself an integrity error), so the writers below map each line through the
# format's own writer instead of writing a CSV.
WI_COLUMNS = "WI-ID,Title,Workstream,SR-Refs,Predecessors,Status,Deliverable"
# ...plus the SpecRef column (S1) — used by the SSOT-rule tests. (A BlockRef
# column retired with the blockref vocabulary at WI-553/OI-70.)
SR_WI_COLUMNS = WI_COLUMNS + ",SpecRef"

# `active/<branch>/` is the only status two levels deep and the branch is the
# integrator's, so a fixture writing an active row has to name one.
ACTIVE_BRANCH = "wi-fixture"


def _wi_rows(body, columns):
    """`body`'s lines as full 17-column registry rows, read with `csv` so a
    quoted cell parses exactly as it did when the body WAS the file."""
    names = columns.split(",")
    rows = []
    for cells in csv.reader(body.splitlines()):
        if not cells or not cells[0].strip():
            continue
        row = dict.fromkeys(wi_convert.COLUMNS, "")
        row.update(dict(zip(names, cells)))
        rows.append(row)
    return rows


def _write_spec_row(work, row, order):
    """Write one row as its spec file under `work`.

    Everything goes through `wi_convert`, the format's single writer — except the
    directory for an `active` row, which that writer deliberately does not know:
    the integrator's BRANCH names `active/<branch>/`, so a fixture supplies one
    and reuses the same renderer for the file itself."""
    if (row.get("Status") or "").strip() != "active":
        return wi_convert.write_spec_file(work, row, order=order)
    text = wi_convert.FENCE + "\n"
    text += wi_convert.render_frontmatter(wi_convert.frontmatter_pairs(row, order))
    text += wi_convert.FENCE + "\n"
    if row.get("Deliverable"):
        text += wi_convert.DELIVERABLE_PREFIX + row["Deliverable"] + "\n"
    path = work / "active" / ACTIVE_BRANCH / wi_convert.spec_filename(row)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def write_wis(root, body, columns=WI_COLUMNS):
    """Write the work-item registry — the `docs/work/` spec folder — from the
    CSV-shaped `body`, one spec file per line.

    The folder is REPLACED on every call: one call writes the whole registry, so
    a test that re-writes it (a status flip) MOVES the item's file rather than
    leaving a second copy in the old status directory. Two rows sharing an id
    stay two files (their titles differ, so their slugs do), which is what keeps
    the duplicate-id integrity error reachable."""
    work = root / "docs" / "work"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    for order, row in enumerate(_wi_rows(body, columns), 1):
        _write_spec_row(work, row, order)
    return root


def run_traj(root, *extra):
    return run_py([SCRIPTS / "check_trajectory.py", "--root", root, *extra], cwd=root)


# --- WI-056: architecture-connectivity coverage (warn-first, opt-out default-on)
# The views-checker runs at the same `trajectory` step; every finding is a WARN
# (never an exit-code change, even under --strict) and the meta driver is the
# "connectivity undeclared" warn a multi-module arch-map with no seams emits.

ARCH_2MOD = """# Arch
<!-- BEGIN GENERATED MODULE MAP -->
### `scripts/mod_a`
_A._

| Public item | Summary | Implements |
|---|---|---|
| `run()` | go |  |

### `scripts/mod_b`
_B._

| Public item | Summary | Implements |
|---|---|---|
| `go()` | g |  |
<!-- END GENERATED MODULE MAP -->
"""

ARCH_1MOD = """# Arch
<!-- BEGIN GENERATED MODULE MAP -->
### `scripts/mod_a`
_A._

| Public item | Summary | Implements |
|---|---|---|
| `run()` | go |  |
<!-- END GENERATED MODULE MAP -->
"""

IF_HDR = (
    "IF-ID,Direction,ThisProject,Counterpart,Contract,Req-Refs,Version,"
    "Stability,Status,Component,Notes\n"
)


# The IF/CMP tiers moved to the TOML carrier at WI-443 (OI-14 part B). The two
# writers below TRANSLATE the CSV bodies this module's ~24 call sites already
# hold rather than rewriting every one of them: what those tests are about is
# coverage, cross-component edges and spec citations, not the carrier — and a
# translating writer keeps the SUBJECT of each test visible instead of burying
# it under a schema migration. `test_seam_tc_citation_warn` is ABOUT the
# vocabulary and still goes through this translator, which is why the
# default-never-overwrite rule below is load-bearing rather than tidy. (Its
# former sibling `test_spec_interfaces_experimental_needs_rationale` was
# replaced at WI-442 by the test that pins that arm's REMOVAL.)
#
# The two maturity columns these bodies carry collapse into the ONE the tier
# has: a body that reads `Stability=draft`, or `Status=Proposed` with no
# `Stability`, translates to `status = "Drafted"`; anything else to
# `status = "Accepted"` (OI-67 put the spine's own two words on the row).
def _csv_body_to_toml(header, table, body):
    import csv as _csv
    import io as _io

    # WI-455: the CSV bodies keep their three-cell shape (it is what the legacy
    # carrier holds); the translation applies the rename the registry took —
    # `Direction` DROPPED, `ThisProject` -> `provider`, `Counterpart` ->
    # `consumers` (a list, emitted below).
    #
    # OI-67 moved the same three cells again: `provider` became `owner` (one
    # spelling for both endpoints, read verbatim), `contract` became the typed
    # `data`, and `Req-Refs` is DROPPED because the seam reaches the spine
    # through its owner rather than by stating a ref.
    keys = {
        "ThisProject": "owner",
        "Contract": "data",
        "Version": "version",
        "Component": "component",
        "Notes": "notes",
        "Name": "name",
        "Category": "category",
        "Knowledge": "knowledge",
        "State": "state",
        "SupersededBy": "superseded_by",
        "PartOf": "part_of",
    }
    id_col = header.split(",", 1)[0]
    out = []
    for row in _csv.DictReader(_io.StringIO(header + body)):
        rid = (row.get(id_col) or "").strip()
        if not rid:
            continue
        # DEFAULT, never overwrite. The first version of this line assigned
        # unconditionally and silently discarded whatever maturity the caller's
        # fixture set — which made `test_seam_tc_citation_warn` unable to detect
        # the very re-arming its comment reasons about (its two rows both became
        # `approved`, so re-keying the rule on `approval == "approved"` passed
        # the whole file). A fixture translator that rewrites the cell under
        # test is a test that cannot fail.
        maturity = (row.get("Stability") or "").strip() or (
            "draft"
            if (row.get("Status") or "").strip().lower() == "proposed"
            else "accepted"
        )
        out.append("[{}.{}]".format(table, rid))
        if table == "interface":
            # `channel` is REQUIRED and closed since OI-67, and the bodies here
            # state none: `call` is the honest default for a module<->module
            # seam, which is what every fixture in this module declares. The
            # maturity lands on `status` in the spine's own two words — the
            # column these bodies spell `Stability`, kept caller-first above.
            out.append('channel = "call"')
            consumers = [
                c.strip()
                for c in (row.get("Counterpart") or "").split(";")
                if c.strip()
            ]
            out.append(
                "consumers = [{}]".format(", ".join('"%s"' % c for c in consumers))
            )
            out.append(
                'status = "{}"'.format(
                    "Drafted"
                    if maturity.lower() in ("draft", "drafted", "proposed")
                    else "Accepted"
                )
            )
        for col, key in keys.items():
            value = (row.get(col) or "").strip()
            if not value:
                continue
            if key in ("superseded_by", "part_of"):
                items = ", ".join('"{}"'.format(t) for t in value.split(";") if t)
                out.append("{} = [{}]".format(key, items))
            else:
                out.append('{} = """{}"""'.format(key, value))
        out.append("")
    return "\n".join(out) + "\n"


def write_arch(root, text):
    """TRANSLATING writer (the WI-443 _csv_body_to_toml idiom, applied at
    WI-455): the ~30 call sites state their inventory as the old committed
    MODULE-MAP markdown because a table is how an inventory fixture reads —
    but `arch_inventory` now scans the SOURCE TREE under the declared
    `[paths] src` root, so this parses the fixture and writes real `.py`
    files (docstring summary, `Contracts:` docstring line, public defs) plus
    the `[paths] src = scripts` profile (kept if the test wrote its own).
    What each test is ABOUT — coverage, containment, seams — stays visible
    at its call site; the carrier change lives here once."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    ini = root / "docs" / "stack.ini"
    if not ini.exists():
        ini.write_text("[paths]\nsrc = scripts\n", encoding="utf-8")
    mods, current = [], None
    for line in text.splitlines():
        m = re.match(r"^### `([^`]+)`", line)
        if m:
            current = {
                "name": m.group(1),
                "summary": "",
                "contracts": [],
                "imports": [],
                "funcs": [],
            }
            mods.append(current)
            continue
        if current is None:
            continue
        s = re.match(r"^\| `(\w+)\(([^)]*)\)`", line)
        if s:
            current["funcs"].append((s.group(1), s.group(2)))
            continue
        if line.strip().startswith("Contracts (interfaces):"):
            current["contracts"] += re.findall(r"IF-\d+", line)
            continue
        if line.strip().startswith("Imports (internal):"):
            current["imports"] += re.findall(r"`([^`]+)`", line)
            continue
        d = re.match(r"^_(.+)_$", line.strip())
        if d and not current["summary"]:
            current["summary"] = d.group(1)
    for mod in mods:
        rel = Path(mod["name"] + ".py")
        dest = root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        doc = mod["summary"] or ""
        body = ""
        if doc or mod["contracts"]:
            body += '"""' + doc
            if mod["contracts"]:
                # Declared AND stated (OI-67 slice 6): the armed definition
                # gate fails a declared seam with no body, and these fixtures
                # are about coverage, containment and seams — not about that
                # gate, which has its own scenarios below.
                body += "\n\nContracts: " + ", ".join(mod["contracts"]) + "\n"
                for iid in mod["contracts"]:
                    body += "\nContract {}: the fixture's contract for {}.".format(
                        iid, iid
                    )
            body += '"""\n'
        for imp in mod["imports"]:
            body += "import {}\n".format(imp)
        for fn, args in mod["funcs"]:
            body += "\n\ndef {}({}):\n    return None\n".format(fn, args)
        dest.write_text(body or "# empty\n", encoding="utf-8")


def write_ifs(root, body):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "interfaces.toml").write_text(
        _csv_body_to_toml(IF_HDR, "interface", body), encoding="utf-8"
    )


def _two_components(root):
    """mod_a declares CMP-001 and mod_b CMP-002, both live rows: the rows
    name components, so connectivity is judged per component."""
    write_cmps(root, TWO_CMPS)
    declare_components(
        root, [("scripts/mod_a", "CMP-001"), ("scripts/mod_b", "CMP-002")]
    )


def test_interface_coverage_warns(tmp_path):
    """Implements: TC-080"""
    # Multi-module arch-map with NO interfaces.csv -> "connectivity undeclared"
    # (the ruled opt-out, default-on posture), and the exit code is still 0.
    write_arch(tmp_path, ARCH_2MOD)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" in proc.stderr


def test_interface_check_off_silences(tmp_path):
    """Implements: TC-080"""
    write_arch(tmp_path, ARCH_2MOD)
    (tmp_path / "docs" / "interfaces-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" not in proc.stderr


def test_single_module_inventory_is_vacuous(tmp_path):
    # <=1 module: nothing to connect, so the coverage layer stays silent.
    write_arch(tmp_path, ARCH_1MOD)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" not in proc.stderr


def test_uncovered_direction_warns(tmp_path):
    """Implements: TC-080"""
    # One row CMP-001 -> CMP-002: CMP-001 has no Consumes, CMP-002 no Provides
    # -> both missing-direction warns fire, each naming its component (exit 0).
    write_arch(tmp_path, ARCH_2MOD)
    _two_components(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Provides,CMP-001,CMP-002,"call",SR-001,v1,Stable,Active,,\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "component 'CMP-001' declares no Consumes seam" in proc.stderr
    assert "component 'CMP-002' declares no Provides seam" in proc.stderr


def test_source_sink_marker_suppresses_direction_warn(tmp_path):
    """Implements: TC-080"""
    # CMP-001 marked source (consumes nothing); CMP-002's only far side is a
    # party marked sink -> both missing-direction warns suppressed.
    write_arch(tmp_path, ARCH_2MOD)
    _two_components(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Provides,CMP-001,CMP-002,"call",SR-001,v1,Stable,Active,,source\n'
        'IF-002,Consumes,CMP-002,external:git,"reads",SR-001,v1,Stable,Active,,sink\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares no Consumes seam" not in proc.stderr
    assert "declares no Provides seam" not in proc.stderr


def test_seam_tc_citation_warn(tmp_path):
    """Implements: TC-080"""
    # A symmetric pair covers both directions, so only the seam-TC warn fires; a
    # TC that cites IF-001 suppresses its warn, IF-002 still warns.
    #
    # RE-KEYED TWICE, and the second time the arming key left ENTIRELY. It armed
    # on `Status=Active` until OI-14 part B retired that column, and measured on
    # the live registry `Active` marked EXACTLY the rows already TC-cited — the
    # rule could only report zero. WI-443 re-keyed it to `Stability=Stable`.
    # WI-442 retired `Stability` for `Approval`, where every live row reads
    # `draft`, so copying the shape forward as `Approval == "approved"` would
    # have rebuilt the ORIGINAL tautology in a new column. It arms on EVERY real
    # IF row now: an interface is backed by a contract test or it is not, and
    # that is the one spelling no vocabulary change can silently disarm. It still
    # reports a COUNT plus the first few ids rather than a line per row (this runs
    # in the shipped pre-commit hook, where a hundred warn lines is a check
    # nobody reads).
    write_arch(tmp_path, ARCH_2MOD)
    _two_components(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Provides,CMP-001,CMP-002,"a to b",SR-001,v1,accepted,Active,,\n'
        'IF-002,Provides,CMP-002,CMP-001,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n",
        encoding="utf-8",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares no Consumes seam" not in proc.stderr  # symmetric -> covered
    seam = [ln for ln in proc.stderr.splitlines() if "cited by no TC" in ln]
    assert len(seam) == 1, proc.stderr
    assert "1 IF seam(s)" in seam[0] and "IF-002" in seam[0]
    assert "IF-001" not in seam[0]  # the TC citation suppresses it
    # IF-002 is `draft` and IF-001 `accepted`, so the row that warns is the one
    # NO TC cites regardless of maturity — the arming key really is gone, not
    # merely renamed.


def test_contracts_docstring_citation_warns(tmp_path):
    """Implements: TC-080"""
    # A module's `Contracts:` line names IF-003 (absent from the registry) ->
    # forward warn. No reverse check holds a row to a declaration site: where
    # a body sits, and that one exists, is the definition gate's.
    arch = ARCH_2MOD.replace("_A._\n", "_A._\nContracts (interfaces): IF-003\n")
    write_arch(tmp_path, arch)
    _two_components(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Provides,CMP-001,CMP-002,"a to b",SR-001,v1,accepted,Active,,\n'
        'IF-002,Provides,CMP-002,CMP-001,"b to a",SR-001,v1,draft,Active,,\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares Contracts: IF-003 but no such IF-### row" in proc.stderr
    assert "is owned by" not in proc.stderr


def test_a_body_in_a_file_of_another_component_is_named(tmp_path):
    # The id-global hole the OI-66 build round named, in component terms: IF-001
    # is owned by CMP-002 and stated in mod_a, a CMP-001 file, so the body's
    # file belongs to the wrong component and the gate names it.
    arch = ARCH_2MOD.replace("_A._\n", "_A._\nContracts (interfaces): IF-001\n")
    write_arch(tmp_path, arch)
    _two_components(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Provides,CMP-002,CMP-001,"b to a",SR-001,v1,accepted,Active,,\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (
        "IF IF-001 is owned by CMP-002, but its body sits in 'scripts/mod_a.py', "
        "whose header declares CMP-001" in proc.stderr
    )


def test_interface_warns_never_fail_strict(tmp_path):
    """Implements: TC-080"""
    # Even under --strict, the REMAINING connectivity warns never change the
    # exit code (they are warns, not the R-B..R-E coherence rules --strict
    # promotes). With no work-items registry the run is vacuously clean once
    # the warns are printed. This scenario has no IF rows at all, so the
    # seam-TC PROMOTION (WI-488, below) is vacuous here too — it is tested on
    # its own scenario, not this one.
    write_arch(tmp_path, ARCH_2MOD)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" in proc.stderr


# --- WI-488 (OI-43 ruled (a)): the seam-TC coverage promotion + its migration --
# allowlist. `interface_findings`' own "cited by no TC" line (tested above,
# `test_seam_tc_citation_warn`) stays pure warn-first forever and reports the
# TOTAL uncited count; `if_tc_coverage_findings` is the promotable half — WARN
# plain / ERROR under --strict — and reports only the seams NOT on
# `docs/if-tc-coverage-allow`.


def test_seam_tc_promotion_errors_under_strict_when_not_allowlisted(tmp_path):
    # Same fixture as test_seam_tc_citation_warn (IF-001 TC-cited, IF-002 not),
    # no allowlist file present -> IF-002 is a plain WARN, and --strict promotes
    # it to an ERROR (exit 1) — distinct from, and in ADDITION to, the
    # `interface_findings` total-uncited line.
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,accepted,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n",
        encoding="utf-8",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    promo = [ln for ln in proc.stderr.splitlines() if "migration allowlist" in ln]
    assert len(promo) == 1 and "IF-002" in promo[0] and "IF-001" not in promo[0]
    assert "WARN" in promo[0]

    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    promo_strict = [
        ln for ln in strict.stderr.splitlines() if "migration allowlist" in ln
    ]
    assert len(promo_strict) == 1 and "ERROR" in promo_strict[0]
    # The informational total (interface_findings, never promoted) still prints
    # under --strict, unaffected.
    total = [ln for ln in strict.stderr.splitlines() if "cited by no TC" in ln]
    assert len(total) == 1 and "1 IF seam(s)" in total[0]


def test_seam_tc_promotion_allowlisted_seam_stays_warn_under_strict(tmp_path):
    # Same uncited IF-002, but listed on the migration allowlist: --strict
    # keeps passing (no ERROR, no "migration allowlist" WARN line either — an
    # allowlisted seam is silent on THIS check), while the informational total
    # in `interface_findings` still reports it (the debt stays visible).
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,accepted,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "if-tc-coverage-allow").write_text(
        "IF-002 — seeded baseline (test fixture)\n", encoding="utf-8"
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert "migration allowlist" not in strict.stderr
    total = [ln for ln in strict.stderr.splitlines() if "cited by no TC" in ln]
    assert len(total) == 1 and "IF-002" in total[0]


def test_if_tc_allow_hygiene_reports_stale_and_unknown_entries(tmp_path):
    # A listed seam that HAS gained a TC (IF-001), and a listed id that names no
    # live IF row (IF-999) -> both reported, never blocking, not even --strict.
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,accepted,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n",
        encoding="utf-8",
    )
    (tmp_path / "docs" / "if-tc-coverage-allow").write_text(
        "IF-001 — already covered, deliberately left to test the stale arm\n"
        "IF-002 — still genuinely uncited, kept off the promotion for this test\n"
        "IF-999 — deliberately unresolvable, to test the unknown arm\n",
        encoding="utf-8",
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    stale = [ln for ln in strict.stderr.splitlines() if "prune them" in ln]
    assert len(stale) == 1 and "IF-001" in stale[0] and "WARN" in stale[0]
    unknown = [ln for ln in strict.stderr.splitlines() if "no live IF-### row" in ln]
    assert len(unknown) == 1 and "IF-999" in unknown[0] and "WARN" in unknown[0]


SEEDED_IF_TC_ALLOW = (
    # THE EXACT SEEDED SET, not its count (2026-08-21 review, W-4 / Sol 2 /
    # Opus m-16). A count pin would let an id be SWAPPED inside the baseline —
    # drop a seam that has since gained a TC, add the new uncited one — with no
    # signal at all, which is precisely the one-line edit the reviewers showed
    # passes the gate. Do NOT relitigate the seed itself: it was independently
    # reproduced as an honest measurement of the seeding tree (120 uncited of
    # 130 live, nothing padded, nothing pre-empted). This pin exists so that
    # the list's FUTURE is reviewed. Pruning an entry whose seam gained a TC is
    # the intended end state — when you prune, lower `seed-count` in the file
    # and delete the id here, in the same commit, and say so in the log.
    # PRUNED 2026-08-29 (OI-67 slice 4): IF-075, whose seam gained TC-161's
    # citation when IF-127 collapsed into it, and IF-116, which collapsed into
    # IF-101 — 120 -> 118, seed-count lowered in the same commit.
    # PRUNED 2026-09-28 (WI-651): IF-112, whose seam gained TC-272's citation
    # (the README floor reading needs under the file's own carrier), and
    # IF-126, whose seam gained TC-271's (the open-items view naming each
    # registry's own copy) — 118 -> 116, seed-count lowered in the same commit.
    # PRUNED 2026-11-21 (WI-1022): the seventeen whose rows retired as `call`
    # seams inside one component — 116 -> 99, seed-count lowered with them.
    # PRUNED 2026-11-22 (WI-1023): IF-117, whose row retired with the design
    # rows' symbol anchor it served — 99 -> 98, seed-count lowered with it.
    "IF-001 IF-002 IF-003 IF-004 IF-005 IF-006 IF-008 IF-009 IF-010 IF-011 IF-012 "
    "IF-013 IF-014 IF-015 IF-016 IF-017 IF-018 IF-019 IF-020 IF-021 IF-022 IF-023 "
    "IF-024 IF-025 IF-026 IF-028 IF-029 IF-030 IF-031 IF-032 IF-033 IF-034 IF-035 "
    "IF-036 IF-037 IF-038 IF-039 IF-040 IF-041 IF-042 IF-043 IF-045 IF-046 IF-047 "
    "IF-048 IF-049 IF-050 IF-051 IF-054 IF-056 IF-057 IF-059 IF-060 IF-068 IF-069 "
    "IF-070 IF-071 IF-072 IF-073 IF-074 IF-077 IF-078 IF-079 IF-080 IF-081 IF-082 "
    "IF-083 IF-084 IF-085 IF-086 IF-088 IF-089 IF-092 IF-098 IF-102 IF-103 IF-104 "
    "IF-105 IF-106 IF-107 IF-108 IF-109 IF-110 IF-111 IF-114 IF-115 IF-118 "
    "IF-119 IF-120 IF-121 IF-122 IF-125 IF-130 IF-131 IF-132 IF-133 IF-134 IF-135"
).split()


def test_the_cover_is_each_call_rows_requestor_and_owner_pairs(tmp_path):
    """A `;`-joined requestor cell is several requestors, each paired with the
    owner; a row on another channel pairs nothing."""
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (req / "interfaces.toml").write_text(
        '[interface.IF-001]\nowner = "CMP-002"\n'
        'requestors = ["CMP-001", "CMP-003", "external:git"]\nchannel = "call"\n\n'
        '[interface.IF-002]\nowner = "CMP-004"\nrequestors = ["CMP-001"]\n'
        'channel = "cli"\n',
        encoding="utf-8",
    )
    assert check_trajectory._call_cover(tmp_path) == {
        ("CMP-001", "CMP-002"),
        ("CMP-003", "CMP-002"),
        ("external:git", "CMP-002"),
    }


def test_this_repos_seam_tc_allowlist_is_exactly_its_seeded_set():
    entries, seed = check_trajectory.parse_if_tc_allow(
        (ROOT / "docs" / "if-tc-coverage-allow").read_text(encoding="utf-8")
    )
    assert seed == 98, "the declared seed-count moved without this pin moving"
    assert len(SEEDED_IF_TC_ALLOW) == 98
    assert [i for i, _ in entries[:98]] == SEEDED_IF_TC_ALLOW
    # And every entry past the seed carries its reason, or it suppresses
    # nothing — the reader drops it, so this is a statement about the FILE
    # being honest rather than about the reader being lenient.
    assert all(reason for _id, reason in entries[98:]), entries[98:]


def test_a_bare_addition_past_the_seed_suppresses_nothing(tmp_path):
    # THE ONE-LINE EDIT THE REVIEW EXECUTED: a new seam fails --strict, and
    # appending its bare id greened it — indistinguishable from the 120 seeded
    # lines, no hygiene line, no test. Now the bare addition is DROPPED by the
    # reader (the seam still errors) and the growth is reported.
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,accepted,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n",
        encoding="utf-8",
    )
    allow = tmp_path / "docs" / "if-tc-coverage-allow"
    allow.write_text("# seed-count: 0\nIF-002\n", encoding="utf-8")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    promo = [ln for ln in strict.stderr.splitlines() if "migration allowlist" in ln]
    assert len(promo) == 1 and "IF-002" in promo[0] and "ERROR" in promo[0]
    grown = [ln for ln in strict.stderr.splitlines() if "past the declared seed" in ln]
    assert len(grown) == 1 and "suppress nothing" in grown[0] and "WARN" in grown[0]

    # The SAME addition with a reason does suppress — the cost of growth is a
    # sentence, not a refusal — and the growth is still reported.
    allow.write_text(
        "# seed-count: 0\nIF-002 — no seam test yet; owed by the next slice\n",
        encoding="utf-8",
    )
    ok = run_traj(tmp_path, "--strict")
    assert ok.returncode == 0, ok.stdout + ok.stderr
    assert "migration allowlist" not in ok.stderr
    grown = [ln for ln in ok.stderr.splitlines() if "past the declared seed" in ln]
    assert len(grown) == 1 and "suppress nothing" not in grown[0]


def test_if_tc_allow_entry_that_does_not_parse_as_an_id_is_reported(tmp_path):
    # PARSE HONESTY (WI-519): `docs/provenance-allow` and
    # `docs/kernel-modules-allow` already report a declaring line the grammar
    # cannot read, rather than silently reading it as an empty file — this
    # carries the same arm to `docs/if-tc-coverage-allow`, the last of the
    # three readers that lacked it.
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "if-tc-coverage-allow").write_text(
        "# seed-count: 0\n"
        "IF-001 — a fine entry\n"
        "not-an-id — this token does not parse as IF-###\n"
        "also bad\n",
        encoding="utf-8",
    )
    findings = check_trajectory.if_tc_allow_parse_findings(tmp_path)
    assert len(findings) == 1, findings
    assert "if-tc-coverage-allow:3" in findings[0]
    assert "2 such line(s)" in findings[0]
    assert "grammar cannot read it" in findings[0]

    # A well-formed file stays silent on this arm.
    (tmp_path / "docs" / "if-tc-coverage-allow").write_text(
        "# seed-count: 0\nIF-001 — a fine entry\n", encoding="utf-8"
    )
    assert check_trajectory.if_tc_allow_parse_findings(tmp_path) == []


def test_if_tc_allow_parse_honesty_shares_the_interfaces_check_opt_out(tmp_path):
    # Shares `if_tc_coverage_findings`' own `[checks] interfaces_check`
    # opt-out — the file is part of the interfaces layer, not a
    # spine-integrity surface, so it rides that gate the same way
    # `kernel_allow_parse_findings` rides `components_check`.
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "if-tc-coverage-allow").write_text(
        "not-an-id\n", encoding="utf-8"
    )
    (tmp_path / "docs" / "interfaces-check").write_text("off\n", encoding="utf-8")
    assert check_trajectory.if_tc_allow_parse_findings(tmp_path) == []


# --- OI-67 slice 6: the armed definition gate -------------------------------
# A row is STATED — declared on its owner's `Contracts:` marker with a
# `Contract IF-###:` body there — or it is an interface with no definition.
# WARN plain, ERROR under `--strict`, the `if_tc_coverage_findings` idiom.


def _gate_repo(
    tmp_path,
    mod_a_doc,
    mod_b_doc='"""B.\n\nContracts: IF-002\n\nContract IF-002: b states it."""\n',
):
    """mod_a (CMP-001) and mod_b (CMP-002); IF-001 owned by CMP-001, IF-002
    by CMP-002, each cited by a TC so the seam-TC promotion stays quiet."""
    write_arch(tmp_path, ARCH_2MOD)
    (tmp_path / "scripts" / "mod_a.py").write_text(
        mod_a_doc + "\n\ndef run():\n    return None\n", encoding="utf-8"
    )
    (tmp_path / "scripts" / "mod_b.py").write_text(
        mod_b_doc + "\n\ndef go():\n    return None\n", encoding="utf-8"
    )
    _two_components(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Provides,CMP-001,CMP-002,"a to b",SR-001,v1,accepted,Active,,\n'
        'IF-002,Provides,CMP-002,CMP-001,"b to a",SR-001,v1,accepted,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001;IF-002,Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n",
        encoding="utf-8",
    )
    return tmp_path


def test_a_declared_seam_with_no_body_warns_plain_and_fails_strict(tmp_path):
    """Implements: TC-474"""
    root = _gate_repo(tmp_path, '"""A.\n\nContracts: IF-001"""\n')
    proc = run_traj(root)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (
        "WARN - IF IF-001 is declared by 'scripts/mod_a.py' but states no "
        "`Contract IF-001:` body there" in proc.stderr
    )
    proc = run_traj(root, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "ERROR - IF IF-001 is declared by 'scripts/mod_a.py'" in proc.stderr
    assert "IF-002" not in [ln for ln in proc.stderr.splitlines() if "ERROR" in ln][0]


def test_a_stated_seam_is_silent_under_the_gate(tmp_path):
    root = _gate_repo(
        tmp_path, '"""A.\n\nContracts: IF-001\n\nContract IF-001: a states it."""\n'
    )
    proc = run_traj(root, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "states no `Contract" not in proc.stderr
    assert "neither declares nor states" not in proc.stderr


def test_a_row_no_file_states_is_valid_and_not_warned(tmp_path):
    # Zero bodies is the pre-build state: the row's `data` cell is the
    # contract's home until code states it, so neither the gate nor a
    # reverse check reports it.
    root = _gate_repo(tmp_path, '"""A, silent."""\n')
    proc = run_traj(root, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "IF IF-001" not in proc.stderr
    assert check_trajectory.contract_body_findings(root) == []


def test_an_external_owned_seam_is_stated_by_its_far_side(tmp_path):
    # An external party's header is not ours to write: OUR READING of its
    # surface is stated in a file of a component on the row's far side, by at
    # most one file, and a file of another component may not state it.
    root = _gate_repo(
        tmp_path, '"""A.\n\nContracts: IF-001\n\nContract IF-001: a."""\n'
    )
    write_ifs(
        root,
        'IF-001,Provides,CMP-001,CMP-002,"a to b",SR-001,v1,accepted,Active,,\n'
        'IF-002,Provides,CMP-002,CMP-001,"b to a",SR-001,v1,accepted,Active,,\n'
        'IF-003,Provides,external:git,CMP-002,"refs",SR-001,v1,accepted,Active,,\n',
    )
    (root / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001;IF-002;IF-003,Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n",
        encoding="utf-8",
    )
    proc = run_traj(root, "--strict")  # no body yet: valid
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # The far side states it: silent.
    (root / "scripts" / "mod_b.py").write_text(
        '"""B.\n\nComponent: CMP-002\n\nContracts: IF-002, IF-003\n\n'
        "Contract IF-002: b.\n"
        'Contract IF-003: our reading of git."""\n\ndef go():\n    return None\n',
        encoding="utf-8",
    )
    proc = run_traj(root, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    # A file of a component NOT on the far side states it too: two bodies.
    (root / "scripts" / "mod_a.py").write_text(
        '"""A.\n\nComponent: CMP-001\n\nContracts: IF-001, IF-003\n\n'
        "Contract IF-001: a.\n"
        'Contract IF-003: not mine to state."""\n\ndef run():\n    return None\n',
        encoding="utf-8",
    )
    proc = run_traj(root, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "ERROR - IF IF-003 is stated by 2 files" in proc.stderr
    # ...and alone, it sits in a component the row does not list.
    (root / "scripts" / "mod_b.py").write_text(
        '"""B.\n\nComponent: CMP-002\n\nContracts: IF-002\n\n'
        'Contract IF-002: b."""\n\ndef go():\n    return None\n',
        encoding="utf-8",
    )
    proc = run_traj(root, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert (
        "ERROR - IF IF-003 is owned by 'external:git'; its body sits in "
        "'scripts/mod_a.py', whose header declares CMP-001" in proc.stderr
    )


def test_a_second_body_in_another_file_is_a_finding(tmp_path):
    # At most one file states a contract; a second copy is a second definition
    # waiting to disagree.
    root = _gate_repo(
        tmp_path,
        '"""A.\n\nContracts: IF-001, IF-002\n\nContract IF-001: a.\nContract IF-002: a copy."""\n',
    )
    proc = run_traj(root, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert (
        "ERROR - IF IF-002 is stated by 2 files (scripts/mod_a.py, scripts/mod_b.py)"
        in proc.stderr
    )


def test_a_refused_header_is_a_finding_and_does_not_disarm_the_other_sources(
    tmp_path,
):
    # mod_a's body opens and states nothing (the grammar refuses it); mod_b
    # declares IF-002 and states no body at all. BOTH must be reported: the
    # regression is not "the refusal is missed", it is "the refusal takes every
    # other source's verdict down with it".
    root = _gate_repo(
        tmp_path,
        '"""A.\n\nContracts: IF-001\n\nContract IF-001:"""\n',
        mod_b_doc='"""B.\n\nContracts: IF-002"""\n',
    )
    findings = check_trajectory.contract_body_findings(root)
    assert any(
        "'scripts/mod_a' declares seams but its header is refused by the "
        "contract grammar"
        in f
        and "opens a contract body and states nothing" in f
        and "its declared rows count as unstated" in f
        for f in findings
    ), findings
    assert any(
        "IF IF-002 is declared by 'scripts/mod_b.py' but states no "
        "`Contract IF-002:` body there" in f
        for f in findings
    ), findings
    # ...and the refused source is NOT entered as "declares nothing".
    sites, refused = check_trajectory._declaration_sites(root)
    assert "scripts/mod_a.py" not in sites, sites
    assert [rel for rel, _msg in refused] == ["scripts/mod_a"], refused


def test_a_python_file_listed_outside_the_source_root_is_read_as_a_module(tmp_path):
    """Implements: TC-474"""
    # Review round 1: a Python file `[arch-map] headers` lists outside the
    # source root was read through the comment-header reader, which finds no
    # contract in a docstring, so its body escaped the uniqueness and header
    # rules. It is read through the module reader.
    root = _gate_repo(
        tmp_path, '"""A.\n\nContracts: IF-001\n\nContract IF-001: a states it."""\n'
    )
    (root / "tools").mkdir()
    (root / "tools" / "helper.py").write_text(
        '"""Helper.\n\nComponent: CMP-002\n\nContracts: IF-001\n\n'
        'Contract IF-001: a second copy."""\n',
        encoding="utf-8",
    )
    (root / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = scripts\n[arch-map]\nheaders = tools/helper.py\n",
        encoding="utf-8",
    )
    findings = check_trajectory.contract_body_findings(root)
    assert any(
        "IF IF-001 is stated by 2 files (scripts/mod_a.py, tools/helper.py)" in f
        for f in findings
    ), findings


def test_a_body_with_no_marker_is_refused_not_skipped(tmp_path):
    """Implements: TC-474"""
    # Review round 1: a file with a `Contract IF-###:` body and no `Contracts:`
    # marker was skipped before its bodies were read, a module and a header
    # file alike, so a second body there escaped uniqueness. The body is read
    # and the missing marker refused, naming the source.
    root = _gate_repo(
        tmp_path, '"""A.\n\nContracts: IF-001\n\nContract IF-001: a states it."""\n'
    )
    (root / "scripts" / "mod_c.py").write_text(
        '"""C.\n\nComponent: CMP-002\n\nContract IF-001: a body with no marker."""\n'
        "\n\ndef go():\n    return None\n",
        encoding="utf-8",
    )
    (root / "docs" / "conf.toml").write_text(
        "# Component: CMP-002\n#\n# Contract IF-002: no marker here either.\n",
        encoding="utf-8",
    )
    (root / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = scripts\n[arch-map]\nheaders = docs/conf.toml\n",
        encoding="utf-8",
    )
    findings = check_trajectory.contract_body_findings(root)
    for source in ("'scripts/mod_c'", "'docs/conf.toml'"):
        refused = [f for f in findings if f.startswith(source)]
        assert len(refused) == 1, (source, findings)
        assert "no `Contracts:` marker" in refused[0], refused


def test_an_unparseable_listed_python_header_is_unreadable_not_a_crash(tmp_path):
    # Review round 2: a listed Python header reaches `ast.parse` through the
    # grammar-findings walk, which caught nothing, so one file that will not
    # parse aborted `interface_findings`. It is the reference's "could not
    # read" entry, as a module under the source root is.
    root = _gate_repo(
        tmp_path, '"""A.\n\nContracts: IF-001\n\nContract IF-001: a states it."""\n'
    )
    (root / "tools").mkdir()
    (root / "tools" / "broken.py").write_text(
        '"""Broken.\n\nComponent: CMP-002\n"""\n\ndef (:\n', encoding="utf-8"
    )
    (root / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = scripts\n[arch-map]\nheaders = tools/broken.py\n",
        encoding="utf-8",
    )
    findings = check_trajectory.interface_findings(root)
    assert not any("tools/broken.py" in f for f in findings), findings
    gen_arch_map = load_script("gen_arch_map")
    headers = gen_arch_map.header_files(root, [root / "scripts"])
    reference = gen_arch_map.build_contract_reference([root / "scripts"], headers)
    assert "- `tools/broken.py` — SyntaxError" in reference, reference


def test_a_refused_header_reds_the_cli_under_strict(tmp_path):
    """Implements: TC-474"""
    # End-to-end through the real `main()` wiring, at the WARN-plain /
    # ERROR-under-`--strict` severity the gate's other three shapes ride.
    root = _gate_repo(
        tmp_path,
        '"""A.\n\nContracts: IF-001\n\nContract IF-001:"""\n',
    )
    plain = run_traj(root)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert (
        "WARN - 'scripts/mod_a' declares seams but its header is refused by "
        "the contract grammar" in plain.stderr
    )
    strict = run_traj(root, "--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    assert (
        "ERROR - 'scripts/mod_a' declares seams but its header is refused by "
        "the contract grammar" in strict.stderr
    )


def test_the_reference_generators_scan_still_raises_without_the_arm(tmp_path):
    # The per-source arm is OPT-IN. `--contracts-doc` must keep failing loudly
    # on a refused header — a reference that silently omitted a source would
    # report a clean, fresh document over a tree it had not actually read.
    root = _gate_repo(
        tmp_path,
        '"""A.\n\nContracts: IF-001\n\nContract IF-001:"""\n',
    )
    gen_arch_map = load_script("gen_arch_map")
    with pytest.raises(gen_arch_map.ContractsGrammarError):
        gen_arch_map.scan_contracts([root / "scripts"])
    collected = []
    records, unreadable = gen_arch_map.scan_contracts(
        [root / "scripts"], grammar_errors=collected
    )
    assert [rel for rel, _msg in collected] == ["scripts/mod_a"], collected
    assert unreadable == []
    assert [rel for rel, _s, _i, _b in records] == ["scripts/mod_b"], records


def test_an_unreadable_source_is_still_not_a_finding(tmp_path):
    # Unchanged by the refusal arm: a source the scan could not PARSE is the
    # reference's own "could not read" list and `arch_inventory`'s skip, never
    # this gate's finding — the two live in different halves of the tuple on
    # purpose.
    root = _gate_repo(
        tmp_path, '"""A.\n\nContracts: IF-001\n\nContract IF-001: a states it."""\n'
    )
    (root / "scripts" / "broken.py").write_text("def (:\n", encoding="utf-8")
    assert check_trajectory.contract_body_findings(root) == []
    sites, refused = check_trajectory._declaration_sites(root)
    assert refused == []
    assert "scripts/broken.py" not in sites and "scripts/mod_a.py" in sites


def test_the_gate_shares_the_interfaces_check_opt_out_and_the_files_mode_vacuity(
    tmp_path,
):
    """The process settings' `[checks] interfaces_check = false` and its
    legacy one-word file each silence the gate, and a scan with no surface,
    files mode or an absent source root, is vacuous: a listed header whose
    body is a finding while the source root is scanned is not read then.

    Implements: TC-474"""
    root = _gate_repo(tmp_path, '"""A.\n\nContracts: IF-001"""\n')
    (root / "docs" / "interfaces-check").write_text("off\n", encoding="utf-8")
    assert check_trajectory.contract_body_findings(root) == []
    (root / "docs" / "interfaces-check").unlink()
    assert check_trajectory.contract_body_findings(root)
    process = root / "docs" / "process.toml"
    process.write_text("[checks]\ninterfaces_check = false\n", encoding="utf-8")
    assert check_trajectory.contract_body_findings(root) == []
    process.write_text("[checks]\ninterfaces_check = true\n", encoding="utf-8")
    assert check_trajectory.contract_body_findings(root)
    process.unlink()
    (root / "docs" / "conf.toml").write_text(
        "# Component: CMP-002\n#\n# Contracts: IF-001\n#\n"
        "# Contract IF-001: a body in another component's file.\n",
        encoding="utf-8",
    )
    stack = root / "docs" / "stack.ini"
    listed = "[arch-map]\nheaders = docs/conf.toml\n"
    stack.write_text("[paths]\nsrc = scripts\n" + listed, encoding="utf-8")
    scanned = check_trajectory.contract_body_findings(root)
    assert any("docs/conf.toml" in f for f in scanned), scanned
    stack.write_text(
        "[paths]\nsrc = scripts\n" + listed + "mode = files\n", encoding="utf-8"
    )
    assert check_trajectory.contract_body_findings(root) == []
    stack.write_text("[paths]\nsrc = absent\n" + listed, encoding="utf-8")
    assert check_trajectory.contract_body_findings(root) == []


def test_the_rows_the_gate_did_not_judge_are_counted_in_one_warn_line(tmp_path):
    # A vacuous pass says so, and no verdict moves: an external-owned row with
    # no in-tree far side is one no module can state, and files-mode leaves
    # every row unjudged.
    root = _gate_repo(
        tmp_path, '"""A.\n\nContracts: IF-001\n\nContract IF-001: a."""\n'
    )
    write_ifs(
        root,
        'IF-001,Provides,CMP-001,CMP-002,"a to b",SR-001,v1,accepted,Active,,\n'
        'IF-002,Provides,CMP-002,CMP-001,"b to a",SR-001,v1,accepted,Active,,\n'
        'IF-003,Provides,external:git,external:ci,"refs",SR-001,v1,accepted,Active,,\n',
    )
    (root / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001;IF-002;IF-003,Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n",
        encoding="utf-8",
    )
    assert check_trajectory.unchecked_contract_rows(root) == [
        "contract bodies not checked for 1 IF row(s): external-owned, and no "
        "component on the far side to state them"
    ]
    assert check_trajectory.contract_body_findings(root) == []
    proc = run_traj(root, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WARN - contract bodies not checked for 1 IF row(s)" in proc.stderr
    (root / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = scripts\n[arch-map]\nmode = files\n", encoding="utf-8"
    )
    assert check_trajectory.unchecked_contract_rows(root) == [
        "contract bodies not checked for 3 IF row(s): [arch-map] mode = files "
        "reads no source headers"
    ]
    assert check_trajectory.contract_body_findings(root) == []


def test_with_no_scan_surface_the_body_check_reports_itself_dormant(tmp_path):
    """With the source root scanned, a listed header's second body is an
    error under strict checking and no dormant line prints; in files mode,
    and with the source root absent, one warning line counts the interface
    rows left unchecked and names why, the second body is not read, and the
    exit is 0 on a plain run and under strict checking alike; with the
    interfaces check off, or with no interface row, there is no line.

    Implements: TC-504"""
    root = _gate_repo(
        tmp_path, '"""A.\n\nContracts: IF-001\n\nContract IF-001: a states it."""\n'
    )
    (root / "docs" / "conf.toml").write_text(
        "# Component: CMP-001\n#\n# Contracts: IF-001\n#\n"
        "# Contract IF-001: a second body in a listed header.\n",
        encoding="utf-8",
    )
    stack = root / "docs" / "stack.ini"
    listed = "[arch-map]\nheaders = docs/conf.toml\n"

    def dormant_lines(proc):
        return [ln for ln in proc.stderr.splitlines() if "not checked for" in ln]

    files_mode = "[paths]\nsrc = scripts\n" + listed + "mode = files\n"
    stack.write_text("[paths]\nsrc = scripts\n" + listed, encoding="utf-8")
    proc = run_traj(root, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "ERROR - IF IF-001 is stated by 2 files" in proc.stderr
    assert dormant_lines(proc) == []
    for profile, why in (
        (files_mode, "[arch-map] mode = files reads no source headers"),
        ("[paths]\nsrc = absent\n" + listed, "the scan root 'absent' is absent"),
    ):
        stack.write_text(profile, encoding="utf-8")
        for extra in ((), ("--strict",)):
            proc = run_traj(root, *extra)
            assert proc.returncode == 0, proc.stdout + proc.stderr
            assert dormant_lines(proc) == [
                "check_trajectory: WARN - contract bodies not checked for 2 IF "
                "row(s): " + why
            ], proc.stderr
            assert "stated by 2 files" not in proc.stderr
    stack.write_text(files_mode, encoding="utf-8")
    process = root / "docs" / "process.toml"
    process.write_text("[checks]\ninterfaces_check = false\n", encoding="utf-8")
    proc = run_traj(root, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert dormant_lines(proc) == [], proc.stderr
    process.unlink()
    write_ifs(root, "")
    proc = run_traj(root, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert dormant_lines(proc) == [], proc.stderr


def test_if_tc_allow_malformed_line_is_reported_end_to_end(tmp_path):
    # The same fixture `test_a_bare_addition_past_the_seed_suppresses_nothing`
    # uses, proving the new arm rides the real `main()` wiring at the same
    # WARN-plain / ERROR-under-`--strict` severity `if_tc_coverage_findings`
    # already uses, not a parallel channel.
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,accepted,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n",
        encoding="utf-8",
    )
    allow = tmp_path / "docs" / "if-tc-coverage-allow"
    allow.write_text("# seed-count: 0\nnot-an-id\n", encoding="utf-8")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "grammar cannot read it" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "grammar cannot read it" in strict.stderr


def test_seam_tc_promotion_shares_the_one_module_vacuity(tmp_path):
    # <=1 module: the promotion must arm on no MORE than the warn it promotes
    # (test_single_module_inventory_is_vacuous, above) — an uncited seam here
    # stays silent on both checks, strict or not.
    write_arch(tmp_path, ARCH_1MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,downstream adopter,"a to world",SR-001,v1,accepted,Active,,\n',
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert "migration allowlist" not in strict.stderr
    assert "cited by no TC" not in strict.stderr


# --- WI-073/FB5: the How-SW top-view right-sizing rule -------------------------
# The software-architecture top view is bounded at 10 items (top-level CMP
# components that contain a module + uncontained modules); over the bound is a
# finding — WARN plain, ERROR under --strict (DevStg-Tests+). Opt-out docs/components-check;
# vacuous below the bound or with no arch-map inventory (the bound is the rule).

CMP_HDR = "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,Notes\n"
TAGGED_LLR_HDR = (
    "LLR-ID,SR-Refs,Title,Module,CodeSymbol,Detail,TestRefs,Status,Component\n"
)


def _arch_n(n):
    """A generated MODULE MAP block of n modules scripts/mod_0..mod_{n-1}."""
    body = "".join(
        "### `scripts/mod_{i}`\n_M{i}._\n\n| Public item | Summary | Implements |\n"
        "|---|---|---|\n| `f{i}()` | go |  |\n\n".format(i=i)
        for i in range(n)
    )
    return (
        "# Arch\n<!-- BEGIN GENERATED MODULE MAP -->\n"
        + body
        + "<!-- END GENERATED MODULE MAP -->\n"
    )


# SR-165 (WI-999): a live CMP row with no derivation record is a component
# finding. These fixtures are about containment and seams, not the record, so
# the first row holds a one-candidate record and every other row cites it.
FIXTURE_RECORD = (
    'candidates = ["A"]\nobjective = "minimize cut"\nconstraints = ["none"]\n'
    'scores = ["A=1"]\nselected = "A"\nruling = "the fixture"\n'
)


def write_cmps(root, body):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    text = _csv_body_to_toml(CMP_HDR, "component", body)
    ids = re.findall(r"(?m)^\[component\.(CMP-\d+)\]$", text)
    for rid in ids:
        cells = (
            FIXTURE_RECORD if rid == ids[0] else 'derivation = "{}"\n'.format(ids[0])
        )
        head = "[component.{}]\n".format(rid)
        text = text.replace(head, head + cells, 1)
    (req / "components.toml").write_text(text, encoding="utf-8")


def write_tagged_llrs(root, pairs):
    """`pairs` = [(module, CMP-id)]: each module's `Component:` header, written
    into the docstring of `<module>.py` where that file exists (membership is
    the file's header, WI-1021), and an LLR csv naming the same pairs. Its
    Component column is read by nothing since WI-1023: a design row's place is
    derived from the interfaces its verifying cases name."""
    declare_components(root, pairs)
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    body = "".join(
        "LLR-{:03d},SR-001,T,{},f,d,(see TC),Accepted,{}\n".format(i + 1, mod, cmp)
        for i, (mod, cmp) in enumerate(pairs)
    )
    (req / "low-level-requirements.csv").write_text(
        TAGGED_LLR_HDR + body, encoding="utf-8"
    )


def declare_components(root, pairs):
    """`pairs` = [(module, CMP-id)]: a `Component:` line in the docstring of each
    existing `<module>.py`, a docstring added where it has none and a line the
    file already carries replaced."""
    for module, cmp in pairs:
        path = root / (module + ".py")
        if not path.is_file():
            continue
        text = re.sub(r"\n\nComponent: CMP-\d+\n", "", path.read_text(encoding="utf-8"))
        text = re.sub(r'^"""Component: CMP-\d+"""\n', "", text)
        if text.startswith('"""'):
            end = text.index('"""', 3)
            text = text[:end] + "\n\nComponent: {}\n".format(cmp) + text[end:]
        else:
            text = '"""Component: {}"""\n'.format(cmp) + text
        path.write_text(text, encoding="utf-8", newline="\n")


def test_top_view_over_bound_warns_plain_fails_strict(tmp_path):
    """Implements: TC-049"""
    # 12 modules, no CMP rows -> 12 uncontained top items > 10.
    write_arch(tmp_path, _arch_n(12))
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "How-SW top view has 12 items" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "How-SW top view has 12 items" in strict.stderr


def test_declaring_components_below_bound_clears_it(tmp_path):
    """Implements: TC-049"""
    # 3 components containing all 12 modules -> top view = 3 <= 10.
    write_arch(tmp_path, _arch_n(12))
    write_cmps(
        tmp_path,
        "CMP-001,A,software,,built,,,,\n"
        "CMP-002,B,software,,built,,,,\n"
        "CMP-003,C,software,,built,,,,\n",
    )
    write_tagged_llrs(
        tmp_path,
        [("scripts/mod_{}".format(i), "CMP-00{}".format(i % 3 + 1)) for i in range(12)],
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_nested_cmp_counts_only_at_top_level_root(tmp_path):
    """Implements: TC-049"""
    # CMP-003 nests under CMP-001 (PartOf); its members count under CMP-001, so
    # the roots are {CMP-001, CMP-002} = 2 top items, well under the bound.
    write_arch(tmp_path, _arch_n(12))
    write_cmps(
        tmp_path,
        "CMP-001,Core,software,,built,,,,\n"
        "CMP-002,Other,software,,built,,,,\n"
        "CMP-003,Nested,software,,built,,CMP-001,,\n",
    )
    pairs = []
    for i in range(12):
        cmp = "CMP-001" if i < 4 else ("CMP-003" if i < 8 else "CMP-002")
        pairs.append(("scripts/mod_{}".format(i), cmp))
    write_tagged_llrs(tmp_path, pairs)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_uncontained_modules_count_toward_the_bound(tmp_path):
    # One component holding a single module leaves 11 uncontained -> 1 + 11 = 12.
    write_arch(tmp_path, _arch_n(12))
    write_cmps(tmp_path, "CMP-001,Only,software,,built,,,,\n")
    write_tagged_llrs(tmp_path, [("scripts/mod_0", "CMP-001")])
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "1 top-level component(s) + 11 uncontained module(s)" in strict.stderr


def test_top_view_off_switch_silences(tmp_path):
    """Implements: TC-049"""
    write_arch(tmp_path, _arch_n(12))
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_ten_module_inventory_is_vacuous(tmp_path):
    """Implements: TC-049"""
    # Exactly at the bound with no CMP rows -> passes trivially (the bound, not
    # the registry, is the rule).
    write_arch(tmp_path, _arch_n(10))
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_absent_inventory_top_view_is_vacuous(tmp_path):
    """Implements: TC-049"""
    # No source tree at all -> nothing to bound (pre-code / files-mode).
    (tmp_path / "docs").mkdir(parents=True, exist_ok=True)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


# --- WI-153: knowledge⇒component coupling (research-knowledge.md §3a) -----------
# When docs/knowledge/ holds a real pack, an uncontained arch-map module is a
# finding *regardless of* the 10-item bound — WARN plain, ERROR under --strict —
# so the knowledge⇒component web must be complete wherever packs are enabled. It
# reuses the Component-tag join (no new join), the docs/components-check opt-out,
# and stays dormant until a real pack (not the README index) exists.

KN_MSG = "arch-map module(s) are in no CMP-### component"


def write_pack(root, label, body="# Pack\n"):
    d = root / "docs" / "knowledge"
    d.mkdir(parents=True, exist_ok=True)
    (d / (label + ".md")).write_text(body, encoding="utf-8")


def test_pack_presence_arms_coupling_below_bound(tmp_path):
    # 3 modules (well under the 10-item bound), none contained, + one pack: the
    # top-view rule is vacuous here, but the pack arms the coupling finding.
    write_arch(tmp_path, _arch_n(3))
    write_pack(tmp_path, "prompt-image")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "docs/knowledge/ holds 1 pack(s) but 3 " + KN_MSG in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert KN_MSG in strict.stderr


def test_coupling_dormant_without_packs(tmp_path):
    # Same uncontained 3-module arch-map but no pack -> below the bound, silent.
    write_arch(tmp_path, _arch_n(3))
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


def test_readme_index_alone_does_not_arm_coupling(tmp_path):
    # The scaffolded README.md is the index, not a pack -> still dormant.
    write_arch(tmp_path, _arch_n(3))
    (tmp_path / "docs" / "knowledge").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "knowledge" / "README.md").write_text("# idx\n", "utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


def test_coupling_clears_when_every_module_contained(tmp_path):
    # A pack exists, but every module is tagged into a CMP -> web complete, silent.
    write_arch(tmp_path, _arch_n(3))
    write_pack(tmp_path, "prompt-image")
    write_cmps(tmp_path, "CMP-001,Core,software,,built,,,,\n")
    write_tagged_llrs(
        tmp_path, [("scripts/mod_{}".format(i), "CMP-001") for i in range(3)]
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


def test_coupling_reports_only_the_uncontained_modules(tmp_path):
    # A pack + a CMP holding one of three modules -> two remain uncontained.
    write_arch(tmp_path, _arch_n(3))
    write_pack(tmp_path, "prompt-image")
    write_cmps(tmp_path, "CMP-001,Core,software,,built,,,,\n")
    write_tagged_llrs(tmp_path, [("scripts/mod_0", "CMP-001")])
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "holds 1 pack(s) but 2 " + KN_MSG in strict.stderr


def test_coupling_respects_the_components_check_off_switch(tmp_path):
    # docs/components-check: off silences the coupling as it does the top view.
    write_arch(tmp_path, _arch_n(3))
    write_pack(tmp_path, "prompt-image")
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


def test_coupling_needs_an_arch_map_inventory(tmp_path):
    # A pack but no arch-map -> no modules to leave uncontained -> dormant.
    write_pack(tmp_path, "prompt-image")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


# --- WI-388 (consumer 3 of the context block): the pack-citation warn ----------
# A hand-authored OPEN spec whose rows' components declare knowledge packs the
# spec never cites is warned, warn-FIRST (never an exit-code change, like
# backlog staleness): the pack is the recorded how-knowledge behind the rows
# the WI touches, so a spec that never names it is building blind. A minted
# row's ## Context block cites the packs at mint, so minted rows satisfy the
# rule by construction — the warn reaches exactly the hand-authored residue.

PACK_MSG = "the spec never cites"


def _pack_repo(tmp_path, spec_body=""):
    write_cmps(tmp_path, "CMP-001,Core,software,docs/knowledge/widgetry,built,,,,\n")
    write_pack(tmp_path, "widgetry")  # the token must RESOLVE to a real pack
    write_tagged_llrs(tmp_path, [("scripts/mod_0", "CMP-001")])
    # LLR-001 sits in CMP-001: its case names IF-001, which CMP-001 owns.
    (tmp_path / "docs" / "requirements" / "interfaces.toml").write_text(
        '[interface.IF-001]\nowner = "CMP-001"\nconsumers = ["CMP-001"]\n'
        'channel = "call"\n',
        encoding="utf-8",
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.toml").write_text(
        '[test.TC-001]\nverifies = ["LLR-001", "IF-001"]\nstatus = "Drafted"\n',
        encoding="utf-8",
    )
    work = tmp_path / "docs" / "work" / "queued"
    work.mkdir(parents=True, exist_ok=True)
    (work / "WI-005-thing.md").write_text(
        '+++\nid = "WI-005"\ntitle = "a thing"\nsr_refs = ["SR-001"]\n'
        'specref = "docs/requirements/components.csv"\n+++\n' + spec_body,
        encoding="utf-8",
        newline="\n",
    )
    return tmp_path


def test_an_open_spec_that_never_cites_its_packs_warns(tmp_path):
    _pack_repo(tmp_path)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "WI-005" in proc.stderr and PACK_MSG in proc.stderr
    assert "docs/knowledge/widgetry" in proc.stderr
    # Warn-first means warn-ONLY: --strict does not promote it (advisory,
    # never gating — the block's contract).
    strict = run_traj(tmp_path, "--strict")
    assert PACK_MSG not in [ln for ln in strict.stderr.splitlines() if "ERROR" in ln], (
        strict.stderr
    )


def test_a_spec_that_cites_its_packs_is_silent(tmp_path):
    _pack_repo(
        tmp_path,
        "\n## Context\n\n- packs: docs/knowledge/widgetry (read first)\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert PACK_MSG not in proc.stderr


def test_rows_without_declared_packs_stay_silent(tmp_path):
    write_cmps(tmp_path, "CMP-001,Core,software,,built,,,,\n")
    write_tagged_llrs(tmp_path, [("scripts/mod_0", "CMP-001")])
    work = tmp_path / "docs" / "work" / "queued"
    work.mkdir(parents=True, exist_ok=True)
    (work / "WI-005-thing.md").write_text(
        '+++\nid = "WI-005"\ntitle = "a thing"\nsr_refs = ["SR-001"]\n'
        'specref = "docs/requirements/components.csv"\n+++\n',
        encoding="utf-8",
        newline="\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert PACK_MSG not in proc.stderr


# --- WI-455: the inventory is the LIVE source tree ----------------------------
# The WI-399/406/410/411 committed-vs-disk delta family that lived here is
# RETIRED with its machinery: arch_inventory reads the source AST directly
# (gen_arch_map.scan_inventory — ONE walk, so there is no mirror left to
# drift), and a module a lane adds is simply IN the inventory, where the
# station containment rule fires on it at once. What stays pinned below:
# the profile reads (declared src root, absolute src, files-mode dormancy),
# the walk's keep/skip shapes as arch_inventory consumes them, and the
# fail-quiet posture on an undecodable file.

MODULE_BODY = '"""M."""\n\n\ndef run():\n    """go"""\n'


def write_module(root, name, text=MODULE_BODY, src="scripts"):
    d = root / src
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(text, encoding="utf-8")


def write_src_profile(root, files, src="scripts", mode=None):
    """docs/stack.ini declaring the scan root (+ optional mode) and the module
    files on disk under it."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    ini = "[paths]\nsrc = {}\n".format(src)
    if mode:
        ini += "\n[arch-map]\nmode = {}\n".format(mode)
    (root / "docs" / "stack.ini").write_text(ini, encoding="utf-8")
    for name in files:
        write_module(root, name, MODULE_BODY if name.endswith(".py") else "# m\n", src)


def _contained_two_module_tree(tmp_path, src="scripts"):
    """A pack-armed tree whose 2-module source inventory is fully contained —
    clean under the containment rule."""
    write_pack(tmp_path, "prompt-image")
    write_cmps(tmp_path, "CMP-001,Core,software,,built,,,,\n")
    write_src_profile(tmp_path, ["mod_0.py", "mod_1.py"], src=src)
    write_tagged_llrs(
        tmp_path, [("scripts/mod_0", "CMP-001"), ("scripts/mod_1", "CMP-001")]
    )


def test_untagged_module_on_disk_reds_the_containment_rule(tmp_path):
    # The WI-387 topology under the live inventory: a new module on disk with
    # no Component tag is uncontained the moment it exists — the lane's own
    # checks fail; no committed-map staleness can hide it from anyone.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "mod_new.py")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert KN_MSG in plain.stderr and "scripts/mod_new" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert KN_MSG in strict.stderr


def test_component_tag_clears_the_added_module(tmp_path):
    # The two-registry-row remedy (an LLR Component cell) clears it — no map
    # regeneration exists to wait for anymore.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "mod_new.py")
    write_tagged_llrs(
        tmp_path,
        [
            ("scripts/mod_0", "CMP-001"),
            ("scripts/mod_1", "CMP-001"),
            ("scripts/mod_new", "CMP-001"),
        ],
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert KN_MSG not in proc.stderr


def test_absolute_declared_src_scans_like_the_generator(tmp_path):
    # An absolute [paths] src scans the directory it names (gen_arch_map
    # treats --src as a path, absolute or not) — no silent repo-relative miss.
    _contained_two_module_tree(tmp_path, src=str(tmp_path / "scripts"))
    write_module(tmp_path, "mod_new.py")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert KN_MSG in strict.stderr and "scripts/mod_new" in strict.stderr


def test_files_mode_keeps_the_whole_family_dormant(tmp_path):
    # [arch-map] mode = files has no parser, so the inventory is EMPTY and the
    # containment family stays dormant — the same posture the files-mode
    # committed map produced (a table has no module headers).
    write_pack(tmp_path, "prompt-image")
    write_src_profile(tmp_path, ["mod_0.py", "helper.sh"], mode="files")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert KN_MSG not in strict.stderr


def test_symbols_mode_sees_only_python(tmp_path):
    # Default symbols mode scans *.py exactly as the generator does: a .sh
    # file never enters the inventory, so it cannot be "uncontained". (It still
    # declares its component: the header scope is every carrier type.)
    _contained_two_module_tree(tmp_path)
    (tmp_path / "scripts" / "helper.sh").write_text(
        "# Component: CMP-001\n# h\n", encoding="utf-8"
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


def test_inventory_skips_hidden_and_pycache(tmp_path):
    # The hidden-part rule (dot-/__pycache__-prefixed parts under the root are
    # not source) holds in the live scan, so caches never fail a lane.
    _contained_two_module_tree(tmp_path)
    for sub in ("__pycache__", ".vendored"):
        write_module(tmp_path, "mod_cache.py", src="scripts/" + sub)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


def test_inventory_keeps_every_generator_shape(tmp_path):
    # The walk's keep-arms, pinned at the consumer: docstring-only,
    # public-symbol-only, contracts-comment-only, re-exporting __init__,
    # absolute and dotted-absolute import-only, and a parse-error module all
    # enter the inventory (each is real code the generator inventoried);
    # symbol-EMPTY files (bare __init__, comment-only, private-only) do not.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "doc_only.py", '"""Docstring-only module."""\n')
    write_module(tmp_path, "sym_only.py", "def run():\n    pass\n")
    write_module(tmp_path, "seam.py", "# Contracts: IF-001\n")
    write_module(tmp_path, "__init__.py", "from . import notes\n", src="scripts/pkg")
    write_module(tmp_path, "notes.py", "# comment-only sibling\n", src="scripts/pkg")
    write_module(tmp_path, "abs_imp.py", "import mod_0\n")
    write_module(tmp_path, "dot_from.py", "from pkg.notes import go\n")
    write_module(tmp_path, "broken.py", "def broken(:\n    pass\n")
    write_module(tmp_path, "priv.py", "def _hidden():\n    pass\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    kn = [ln for ln in strict.stderr.splitlines() if KN_MSG in ln]
    assert len(kn) == 1, strict.stderr
    line = kn[0]
    for kept in (
        "scripts/doc_only",
        "scripts/sym_only",
        "scripts/seam",
        "scripts/pkg",
        "scripts/abs_imp",
        "scripts/dot_from",
        "scripts/broken",
    ):
        assert kept in line, (kept, line)
    assert "7 " + KN_MSG in line  # the symbol-empty files are NOT in it
    assert "scripts/pkg/notes" not in line
    assert "scripts/priv" not in line


def test_undecodable_module_is_skipped_without_a_crash(tmp_path):
    # The fail-quiet arm: a non-UTF-8 .py cannot be judged, so the strict=False
    # consumer read skips that file rather than crashing a warn-tier rule
    # (\xff is an invalid UTF-8 start byte on every platform). The file costs
    # itself, not the run: its header cannot be read, so it declares no
    # component, and that is the run's one finding.
    _contained_two_module_tree(tmp_path)
    (tmp_path / "scripts" / "bin_mod.py").write_bytes(b"\xff\xfe\x00not utf-8")
    strict = run_traj(tmp_path, "--strict")
    assert "Traceback" not in strict.stderr, strict.stderr
    errors = [ln for ln in strict.stderr.splitlines() if "ERROR - " in ln]
    assert len(errors) == 1, strict.stderr
    assert "scripts/bin_mod.py: declares no component" in errors[0]


# --- WI-064: the cross-CMP-edge-without-IF rule ---------------------------------
# An internal import edge between two DIFFERENT components with no covering
# IF-### row is a finding (the AXES accepted model's enforceability ruling) —
# WARN plain, ERROR under --strict, sharing the docs/components-check opt-out.
# Edges come from the MODULE MAP block's `Imports (internal):` lines; the seam
# side joins interfaces.csv endpoints in either direction. Vacuous whenever any
# input is absent (never-breaking).

ARCH_2MOD_IMPORT = """# Arch
<!-- BEGIN GENERATED MODULE MAP -->
### `scripts/mod_a`
_A._
Imports (internal): `mod_b`

| Public item | Summary | Implements |
|---|---|---|
| `run()` | go |  |

### `scripts/mod_b`
_B._

| Public item | Summary | Implements |
|---|---|---|
| `go()` | g |  |
<!-- END GENERATED MODULE MAP -->
"""

TWO_CMPS = "CMP-001,A,software,,built,,,,\nCMP-002,B,software,,built,,,,\n"


def _cross_cmp_repo(tmp_path, cmp_b="CMP-002"):
    """mod_a (CMP-001) imports mod_b (cmp_b); no IF row unless a test adds one."""
    write_arch(tmp_path, ARCH_2MOD_IMPORT)
    write_cmps(tmp_path, TWO_CMPS)
    write_tagged_llrs(
        tmp_path, [("scripts/mod_a", "CMP-001"), ("scripts/mod_b", cmp_b)]
    )


def test_cross_cmp_import_without_seam_warns_plain_fails_strict(tmp_path):
    """Implements: TC-067"""
    _cross_cmp_repo(tmp_path)
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert (
        "cross-component import scripts/mod_a (CMP-001) -> scripts/mod_b (CMP-002)"
        in plain.stderr
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "has no declared IF-### seam" in strict.stderr


def _write_tc_citing(tmp_path, if_id):
    """A minimal TC citing `if_id` — WI-488's seam-TC promotion errors under
    `--strict` on any declared, uncited seam, so a fixture whose SUBJECT is a
    different rule (cross-component coverage, the overlap advisory, …) must
    cite its own IF row to stay a clean `--strict` scenario."""
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;{},Integration,seam,Full,,ok,Yes,tests/x.py,Accepted\n".format(
            if_id
        ),
        encoding="utf-8",
    )


def _write_call_row(tmp_path, owner, requestor):
    """One `call` row, owned by `owner`, naming `requestor` among its requestors."""
    (tmp_path / "docs" / "requirements" / "interfaces.toml").write_text(
        '[interface.IF-001]\nowner = "{}"\nrequestors = ["{}"]\n'
        'channel = "call"\nstatus = "Drafted"\n'.format(owner, requestor),
        encoding="utf-8",
    )


def test_cross_cmp_import_with_declared_seam_is_silent(tmp_path):
    """Implements: TC-067"""
    # A `call` row owned by the imported file's component (CMP-002) naming the
    # importer's (CMP-001) among its requestors covers the a -> b import.
    _cross_cmp_repo(tmp_path)
    _write_call_row(tmp_path, "CMP-002", "CMP-001")
    _write_tc_citing(tmp_path, "IF-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_cross_cmp_seam_covers_only_its_own_direction(tmp_path):
    """Implements: TC-067"""
    # The row authored the other way round (CMP-001 owns it, CMP-002 calls)
    # declares that b calls a, not that a calls b: the a -> b import stays
    # uncovered (WI-1015's first loophole, closed).
    _cross_cmp_repo(tmp_path)
    _write_call_row(tmp_path, "CMP-001", "CMP-002")
    _write_tc_citing(tmp_path, "IF-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "has no declared IF-### seam" in proc.stderr


def test_intra_cmp_import_is_silent(tmp_path):
    # Both endpoints in CMP-001: internal wiring, never a finding.
    _cross_cmp_repo(tmp_path, cmp_b="CMP-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_cross_cmp_unmapped_endpoint_is_unclassified(tmp_path):
    """mod_b's header declares no component, so the edge cannot be judged: it
    is reported as unclassified, beside the census finding naming mod_b, where
    it was once skipped in silence. WARN plain, ERROR under --strict, as every
    component finding is.

    Implements: TC-458, TC-459"""
    write_arch(tmp_path, ARCH_2MOD_IMPORT)
    write_cmps(tmp_path, TWO_CMPS)
    write_tagged_llrs(tmp_path, [("scripts/mod_a", "CMP-001")])
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert (
        "cross-component import scripts/mod_a (CMP-001) -> scripts/mod_b "
        "(no component) is unclassified" in plain.stderr
    )
    assert "WARN - scripts/mod_b.py: declares no component" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "ERROR - scripts/mod_b.py: declares no component" in strict.stderr


def test_cross_cmp_no_imports_lines_is_vacuous(tmp_path):
    # An arch-map without `Imports (internal):` lines (older gen, or no internal
    # imports) contributes no edges — the rule costs nothing.
    write_arch(tmp_path, ARCH_2MOD)
    write_cmps(tmp_path, TWO_CMPS)
    write_tagged_llrs(
        tmp_path, [("scripts/mod_a", "CMP-001"), ("scripts/mod_b", "CMP-002")]
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_components_check_off_silences_cross_cmp(tmp_path):
    """Implements: TC-067"""
    _cross_cmp_repo(tmp_path)
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


# --- WI-1021: one component per file -----------------------------------------
# A file's header declares one component, so no endpoint sits in two and
# silences an edge; the multi-membership advisory (WI-440) retired with that
# cause. An edge is internal only inside one component.


def test_single_tagged_same_component_edge_raises_nothing(tmp_path):
    # Both endpoints declare CMP-001: ordinary intra-component wiring.
    _cross_cmp_repo(tmp_path, cmp_b="CMP-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_disjoint_uncovered_edge_is_still_a_hard_finding(tmp_path):
    # Disjoint components, no covering IF row: WARN plain and ERROR under
    # --strict.
    _cross_cmp_repo(tmp_path)
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert (
        "cross-component import scripts/mod_a (CMP-001) -> scripts/mod_b "
        "(CMP-002) has no declared IF-### seam" in plain.stderr
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1


# --- OI-48 (d): the declared shared-kernel exemption (WI-494) -----------------
# `docs/kernel-modules-allow` — an import edge whose DESTINATION is listed there
# is not a seam at all. Fail-safe by construction: absence of a valid
# declaration grants no exemption, so a module not listed (or listed with a
# malformed entry) stays fully policed.


def write_kernel_allow(root, body):
    (root / "docs" / "kernel-modules-allow").write_text(body, encoding="utf-8")


def test_declared_kernel_destination_is_not_a_seam(tmp_path):
    """Implements: TC-067"""
    # mod_a (CMP-001) imports mod_b (CMP-002); mod_b is declared kernel — no
    # finding, clean even under --strict.
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(tmp_path, "scripts/mod_b — WI-494 test: shared reader.\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert "cross-component import" not in strict.stderr


def test_undeclared_module_still_fires_the_hard_finding(tmp_path):
    """Implements: TC-067"""
    # The fail-safe default AND the "still fully live for every other edge"
    # half: a kernel-modules-allow file that declares OTHER modules does not
    # blanket-exempt an edge into a module it does not name.
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(
        tmp_path, "scripts/some_other_module — WI-494 test: not this edge.\n"
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "cross-component import" in strict.stderr


def test_absent_kernel_allow_file_exempts_nothing(tmp_path):
    """Implements: TC-067"""
    # No file at all: read_kernel_modules answers {} and the ordinary rule
    # runs exactly as it did before OI-48 — the fail-safe default.
    _cross_cmp_repo(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "cross-component import" in strict.stderr


def test_kernel_exemption_is_one_directional(tmp_path):
    """Implements: TC-067"""
    # Declaring mod_a (the SOURCE) kernel does not exempt ITS OWN outbound
    # edge — the exemption keys on the destination only.
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(tmp_path, "scripts/mod_a — WI-494 test: wrong side.\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "cross-component import" in strict.stderr


def test_kernel_allow_entry_without_a_reason_is_dropped_and_reported(tmp_path):
    """Implements: TC-067"""
    # No ` — <reason>` separator: the entry DECLARES NOTHING (OI-41 ARM
    # precedent) — no exemption, AND the malformed line is reported rather
    # than silently read as an empty file.
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(tmp_path, "scripts/mod_b\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "cross-component import" in plain.stderr
    assert "grammar cannot read it" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "grammar cannot read it" in strict.stderr


def test_kernel_allow_entry_with_empty_reason_is_dropped_and_reported(tmp_path):
    """Implements: TC-067"""
    # A separator present but nothing after it — same fail-safe: dropped,
    # reported, no exemption.
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(tmp_path, "scripts/mod_b — \n")
    plain = run_traj(tmp_path)
    assert "cross-component import" in plain.stderr
    assert "grammar cannot read it" in plain.stderr


def test_kernel_allow_hygiene_shares_the_components_check_opt_out(tmp_path):
    """Implements: TC-067"""
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(tmp_path, "scripts/mod_b\n")  # malformed, no reason
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "grammar cannot read it" not in proc.stderr


# --- specs act on declared interface boundaries (WI-191) ----------------------

# Two declared seams for the spec-citation checks.
SPEC_IFS_ONE = (
    'IF-001,Consumes,scripts/mod_a,docs/stack.ini,"reads",SR-001,v1,accepted,Stable,,\n'
)
SPEC_IFS_PROPOSED = SPEC_IFS_ONE + (
    'IF-050,Provides,scripts/mod_a,scripts/mod_b,"new seam",SR-001,v1,'
    "draft,Proposed,,\n"
)


def write_spec_file(root, name, body):
    d = root / "docs" / "specs"
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(body, encoding="utf-8")


def _spec_repo(root, spec_name, spec_body, ifs=SPEC_IFS_ONE):
    # A non-vacuous WI registry (the spec check runs past the WI-load) + the IF
    # registry + one spec file. The done WI keeps R-A clean; no open WI leaves
    # R-E vacuous, so the only findings are the spec-interface ones.
    write_wis(root, "WI-001,A,scripts,,,done,Shipped it.\n")
    write_ifs(root, ifs)
    write_spec_file(root, spec_name, spec_body)


def test_spec_interfaces_unarmed_is_vacuous(tmp_path):
    """Implements: TC-068"""
    _spec_repo(tmp_path, "WI-001.md", "# WI-001\n\n## Approach\n\nNo section.\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Interfaces" not in proc.stderr  # no `## Interfaces` -> not armed


def test_spec_interfaces_resolvable_passes(tmp_path):
    """Implements: TC-068"""
    _spec_repo(
        tmp_path,
        "WI-001.md",
        "# WI-001\n\n## Interfaces\n\n- IF-001: acts on the stack reader.\n\n"
        "## Done-when\n",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "resolves to no row" not in proc.stderr


def test_spec_interfaces_unresolvable_warns_then_errors_under_strict(tmp_path):
    """Implements: TC-068"""
    body = "# WI-001\n\n## Interfaces\n\n- IF-999: no such seam.\n\n## Done-when\n"
    _spec_repo(tmp_path, "WI-001.md", body)
    proc = run_traj(tmp_path)  # WARN plain, exit 0
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "IF-999 which resolves to no row" in proc.stderr
    strict = run_traj(tmp_path, "--strict")  # ERROR, exit 1
    assert strict.returncode == 1
    assert "IF-999 which resolves to no row" in strict.stderr


def test_the_anti_duplication_rationale_arm_is_RETIRED_not_re_keyed(tmp_path):
    """WI-442 removed WI-191's forced nearest-existing-IF search, and this pins
    the removal so it cannot drift back in half-fed.

    The arm demanded a rationale on the citation line of any
    `Stability = Experimental` seam. Its input was DELETED by decision 4: the
    slimmed tier has one maturity field with two values, and neither means
    "proposed and not yet pinned by a second consumer". Re-keying onto
    `approval == "draft"` was the obvious move and is the wrong one — it
    silently becomes "not yet accepted", which on a repo that accepts nothing
    before its sitting arms 100% of rows instead of ~4%, at a severity that
    ERRORS under --strict.

    So a bare citation of a `draft` seam is CLEAN, and the resolution arm below
    it still bites. If sitting 3 wants the forced search back, it needs a value
    that means "proposed" — a vocabulary decision, not a checker's to invent.

    Implements: TC-068
    """
    bare = "# WI-001\n\n## Interfaces\n\n- IF-050 (Proposed)\n\n## Done-when\n"
    _spec_repo(tmp_path, "WI-001.md", bare, ifs=SPEC_IFS_PROPOSED)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "with no rationale" not in proc.stderr
    assert "IF-050" not in proc.stderr
    # ...and --strict promotes nothing about IF-050 either. (The fixture's own
    # R-F "live spec cited by no open WI" finding is what --strict does still
    # error on, which is why the assertion is about the id and not the code.)
    assert "IF-050" not in run_traj(tmp_path, "--strict").stderr


def test_spec_interfaces_empty_section_warns(tmp_path):
    _spec_repo(tmp_path, "WI-001.md", "# WI-001\n\n## Interfaces\n\nTBD.\n\n## X\n")
    assert (
        "cites no IF-### and states no intra-module escape" in run_traj(tmp_path).stderr
    )


def test_spec_interfaces_intra_module_escape_passes(tmp_path):
    """Implements: TC-068"""
    body = (
        "# WI-001\n\n## Interfaces\n\nIntra-module: acts only within scripts/mod_a; "
        "no cross-module seam (PROCESS.md §8).\n"
    )
    _spec_repo(tmp_path, "WI-001.md", body)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cites no IF-###" not in proc.stderr


def test_spec_interfaces_readme_and_example_not_armed(tmp_path):
    # The specs/ README documents the rule and the inert WI-000 example both carry
    # the heading, but neither is an armed spec-of-record.
    _spec_repo(
        tmp_path, "README.md", "# Specs\n\n## Interfaces\n\nThe rule: cite IF-###.\n"
    )
    write_spec_file(tmp_path, "WI-000.md", "# WI-000\n\n## Interfaces\n\n- IF-999 x\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "IF-999" not in proc.stderr


# --- Test files name their test cases: the check's surface --------------------
# A finding prints as `<level> - <repo-relative file>:<line>: <shape>`, so one
# prefix proves all three, and a path that is not repo-relative fails it.

TAGGED_FILE = "tests/test_tagged.py"
TAG_CLEAN_FILE = '"""Module text.\n\nImplements: TC-001\n"""\n'
TAG_MISPLACED_FILE = '"""Module text."""\n\n# Implements: TC-001\n'
TAG_UNKNOWN_FILE = '"""Module text.\n\nImplements: TC-404\n"""\n'


def _tag_finding(proc, level, rel, line, shape):
    """The lines of `proc`'s stderr reporting one finding at `level`."""
    prefix = "check_trajectory: {} - {}:{}: {}".format(level, rel, line, shape)
    return [ln for ln in proc.stderr.splitlines() if ln.startswith(prefix)]


def _tc_rows(statuses, evidence=TAGGED_FILE):
    """TC registry text holding one row per `{id: status}`, each citing `evidence`."""
    return "".join(
        '[test.{}]\nverifies = ["SR-001"]\nlevel = "Unit"\nmethod = "m"\n'
        'tier = "Full"\nexpected = "e"\nautomated = "Yes"\n'
        'evidence = "{}"\nstatus = "{}"\n\n'.format(tc, evidence, status)
        for tc, status in statuses.items()
    )


def _write_tc_rows(root, statuses, evidence=TAGGED_FILE):
    path = root / "docs" / "test" / "test-cases.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_tc_rows(statuses, evidence), encoding="utf-8")


def _write_test_file(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.mark.parametrize(
    "work_items", [False, True], ids=["no-work-items", "with-work-items"]
)
def test_tag_findings_warn_plain_and_error_under_strict(tmp_path, work_items):
    """Implements: TC-409"""
    if work_items:
        write_wis(tmp_path, "WI-001,A,scripts,,,done,Shipped it.\n")
    _write_tc_rows(tmp_path, {"TC-001": "Accepted"})
    rel = "tests/test_tagged.py"
    _write_test_file(tmp_path, rel, TAG_CLEAN_FILE)
    clean = run_traj(tmp_path, "--strict")
    assert clean.returncode == 0, clean.stdout + clean.stderr

    _write_test_file(tmp_path, rel, TAG_MISPLACED_FILE)
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert _tag_finding(plain, "WARN", rel, 3, "misplaced"), plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    assert _tag_finding(strict, "ERROR", rel, 3, "misplaced"), strict.stderr


@pytest.mark.parametrize("wrap", [", TC-002", "and TC-002"], ids=["comma", "and"])
def test_a_wrapped_tag_list_is_refused_under_strict(tmp_path, wrap):
    """Implements: TC-409"""
    _write_tc_rows(tmp_path, {"TC-001": "Accepted", "TC-002": "Accepted"})
    rel = "tests/test_tagged.py"
    text = '"""Module text.\n\nImplements: TC-001\n{}\n"""\n'.format(wrap)
    _write_test_file(tmp_path, rel, text)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert _tag_finding(proc, "ERROR", rel, 4, "malformed"), proc.stderr


def test_the_tag_check_is_vacuous_with_no_tests_root_or_no_registry(tmp_path):
    """Implements: TC-409"""
    rel = "tests/test_tagged.py"
    _write_test_file(tmp_path, rel, TAG_UNKNOWN_FILE)
    no_registry = run_traj(tmp_path, "--strict")
    assert no_registry.returncode == 0, no_registry.stdout + no_registry.stderr
    assert rel not in no_registry.stderr

    _write_tc_rows(tmp_path, {"TC-001": "Accepted"})
    paired = run_traj(tmp_path, "--strict")
    assert paired.returncode == 1, paired.stdout + paired.stderr
    assert _tag_finding(paired, "ERROR", rel, 3, "unknown"), paired.stderr

    shutil.rmtree(tmp_path / "tests")
    no_tests = run_traj(tmp_path, "--strict")
    assert no_tests.returncode == 0, no_tests.stdout + no_tests.stderr
    assert rel not in no_tests.stderr


def test_a_nested_tests_root_reports_repo_relative_paths(tmp_path):
    """Implements: TC-409"""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\ntests = qa/tests\n", encoding="utf-8"
    )
    _write_tc_rows(tmp_path, {"TC-001": "Accepted"})
    rel = "qa/tests/test_tagged.py"
    _write_test_file(tmp_path, rel, TAG_MISPLACED_FILE)
    _write_test_file(tmp_path, "tests/test_undeclared.py", TAG_MISPLACED_FILE)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert _tag_finding(proc, "ERROR", rel, 3, "misplaced"), proc.stderr
    assert "test_undeclared" not in proc.stderr


def test_a_draft_tc_is_clean_and_an_absent_one_is_refused(tmp_path):
    """Implements: TC-407"""
    rel = "tests/test_tagged.py"
    example = '"""Module text.\n\nImplements: TC-000\n"""\n'
    _write_tc_rows(tmp_path, {"TC-000": "Drafted", "TC-001": "Drafted"})
    _write_test_file(tmp_path, rel, example)
    example_row = run_traj(tmp_path, "--strict")
    assert example_row.returncode == 1, example_row.stdout + example_row.stderr
    assert _tag_finding(example_row, "ERROR", rel, 3, "unknown"), example_row.stderr

    _write_test_file(tmp_path, rel, TAG_CLEAN_FILE)
    draft = run_traj(tmp_path, "--strict")
    assert draft.returncode == 0, draft.stdout + draft.stderr
    live = load_script("spine_carrier").load(
        tmp_path / "docs" / "test" / "test-cases.toml", "TC-ID", False
    )
    tags, _findings = load_script("gen_arch_map").read_test_tags(
        tmp_path, "tests", {row["TC-ID"] for row in live}
    )
    assert tags == {"TC-001": [rel]}

    _write_tc_rows(tmp_path, {"TC-002": "Accepted"})
    deleted = run_traj(tmp_path, "--strict")
    assert deleted.returncode == 1, deleted.stdout + deleted.stderr
    assert _tag_finding(deleted, "ERROR", rel, 3, "unknown"), deleted.stderr


def test_the_tag_check_on_a_bootstrapped_scaffold(scaffold):
    """Implements: TC-409"""
    registry = scaffold / "docs" / "test" / "test-cases.toml"
    registry.write_text(
        registry.read_text(encoding="utf-8") + "\n" + _tc_rows({"TC-001": "Accepted"}),
        encoding="utf-8",
    )
    rel = "tests/test_tagged.py"

    def trajectory_at(stage):
        return run_py(
            ["scripts/check.py", "--stage", stage, "--run-steps", "trajectory"],
            cwd=scaffold,
        )

    _write_test_file(scaffold, rel, TAG_CLEAN_FILE)
    clean = trajectory_at("DevStg-Impl")
    assert clean.returncode == 0, clean.stdout + clean.stderr

    _write_test_file(scaffold, rel, TAG_MISPLACED_FILE)
    below = trajectory_at("DevStg-Tests")
    assert below.returncode == 0, below.stdout + below.stderr
    assert "{}:3: misplaced".format(rel) in below.stdout + below.stderr
    at_rung = trajectory_at("DevStg-Impl")
    assert at_rung.returncode != 0, at_rung.stdout + at_rung.stderr
    assert "=== trajectory" in at_rung.stdout, at_rung.stdout
    assert "ERROR - {}:3: misplaced".format(rel) in at_rung.stdout + at_rung.stderr


# --- Tags and evidence cells are one fact: the equality check's surface -------
# A finding prints as `<level> - <TC>: <kind>: <node>`, and every comparison is
# of the whole list of them, which pins their number and order as well as their
# text.

TAGGED_NODE = TAGGED_FILE + "::test_a"
UNTAGGED_TEST = "def test_a():\n    pass\n"
TAGGED_TEST = 'def test_a():\n    """Implements: TC-001"""\n'
SECOND_TAGGED_TEST = '\n\ndef test_b():\n    """Implements: TC-001"""\n'
TAGGED_METHOD = (
    'class TestC:\n    def test_m(self):\n        """Implements: TC-001"""\n'
)


def _no_tag(node):
    """The finding for a part of TC-001's cell that no tag declares."""
    return "TC-001: evidence without a tag: {}".format(node)


def _no_evidence(node):
    """The finding for a tag naming TC-001 that no part of its cell names."""
    return "TC-001: tag without evidence: {}".format(node)


def _equality_findings(proc, level):
    """`proc`'s equality findings at `level` in print order, prefix dropped."""
    prefix = "check_trajectory: {} - ".format(level)
    kinds = (": evidence without a tag: ", ": tag without evidence: ")
    return [
        line[len(prefix) :]
        for line in proc.stderr.splitlines()
        if line.startswith(prefix) and any(kind in line for kind in kinds)
    ]


def _write_equality_tree(root, evidence, text, status="Accepted", rel=TAGGED_FILE):
    """TC-001 citing `evidence`, and the one test file `text` beside it."""
    _write_tc_rows(root, {"TC-001": status}, evidence)
    _write_test_file(root, rel, text)


@pytest.mark.parametrize(
    "work_items", [False, True], ids=["no-work-items", "with-work-items"]
)
def test_evidence_without_a_tag_is_named(tmp_path, work_items):
    """Implements: TC-410"""
    if work_items:
        write_wis(tmp_path, "WI-001,A,scripts,,,done,Shipped it.\n")
    _write_equality_tree(tmp_path, TAGGED_NODE, TAGGED_TEST)
    clean = run_traj(tmp_path, "--strict")
    assert clean.returncode == 0, clean.stdout + clean.stderr

    _write_equality_tree(tmp_path, TAGGED_NODE, UNTAGGED_TEST)
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert _equality_findings(plain, "WARN") == [_no_tag(TAGGED_NODE)], plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert _equality_findings(strict, "ERROR") == [_no_tag(TAGGED_NODE)], strict.stderr
    assert strict.returncode == 1, strict.stdout + strict.stderr


def test_a_tag_without_evidence_is_named(tmp_path):
    """Implements: TC-410"""
    _write_equality_tree(tmp_path, TAGGED_NODE, TAGGED_TEST + SECOND_TAGGED_TEST)
    second = TAGGED_FILE + "::test_b"
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert _equality_findings(plain, "WARN") == [_no_evidence(second)], plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert _equality_findings(strict, "ERROR") == [_no_evidence(second)], strict.stderr
    assert strict.returncode == 1, strict.stdout + strict.stderr


def test_a_draft_tc_is_judged(tmp_path):
    """Implements: TC-410"""
    _write_equality_tree(tmp_path, TAGGED_NODE, UNTAGGED_TEST, status="Drafted")
    proc = run_traj(tmp_path, "--strict")
    assert _equality_findings(proc, "ERROR") == [_no_tag(TAGGED_NODE)], proc.stderr
    assert proc.returncode == 1, proc.stdout + proc.stderr


def test_the_equality_check_on_a_bootstrapped_scaffold(scaffold):
    """Implements: TC-410"""
    registry = scaffold / "docs" / "test" / "test-cases.toml"
    rows = _tc_rows({"TC-001": "Accepted"}, TAGGED_NODE)
    registry.write_text(
        registry.read_text(encoding="utf-8") + "\n" + rows, encoding="utf-8"
    )

    def trajectory_at(stage):
        return run_py(
            ["scripts/check.py", "--stage", stage, "--run-steps", "trajectory"],
            cwd=scaffold,
        )

    _write_test_file(scaffold, TAGGED_FILE, TAGGED_TEST)
    clean = trajectory_at("DevStg-Impl")
    assert clean.returncode == 0, clean.stdout + clean.stderr

    _write_test_file(scaffold, TAGGED_FILE, UNTAGGED_TEST)
    below = trajectory_at("DevStg-Tests")
    assert below.returncode == 0, below.stdout + below.stderr
    assert _no_tag(TAGGED_NODE) in below.stdout + below.stderr
    at_rung = trajectory_at("DevStg-Impl")
    assert at_rung.returncode != 0, at_rung.stdout + at_rung.stderr
    assert "=== trajectory" in at_rung.stdout, at_rung.stdout
    finding = "ERROR - " + _no_tag(TAGGED_NODE)
    assert finding in at_rung.stdout + at_rung.stderr


def test_a_parametrized_part_matches_its_tests_tag(tmp_path):
    """Implements: TC-411"""
    case = TAGGED_NODE + "[case one]"
    _write_equality_tree(tmp_path, case, TAGGED_TEST)
    tagged = run_traj(tmp_path, "--strict")
    assert tagged.returncode == 0, tagged.stdout + tagged.stderr

    _write_equality_tree(tmp_path, case, UNTAGGED_TEST)
    untagged = run_traj(tmp_path, "--strict")
    assert _equality_findings(untagged, "ERROR") == [_no_tag(TAGGED_NODE)], (
        untagged.stderr
    )
    assert untagged.returncode == 1, untagged.stdout + untagged.stderr


def test_a_file_only_part_matches_a_module_tag_and_not_a_tests_tag(tmp_path):
    """Implements: TC-411"""
    _write_equality_tree(tmp_path, TAGGED_FILE, TAG_CLEAN_FILE)
    module_tag = run_traj(tmp_path, "--strict")
    assert module_tag.returncode == 0, module_tag.stdout + module_tag.stderr

    _write_equality_tree(tmp_path, TAGGED_FILE, TAGGED_TEST)
    test_tag = run_traj(tmp_path, "--strict")
    assert _equality_findings(test_tag, "ERROR") == [
        _no_tag(TAGGED_FILE),
        _no_evidence(TAGGED_NODE),
    ], test_tag.stderr
    assert test_tag.returncode == 1, test_tag.stdout + test_tag.stderr


def test_a_test_part_does_not_match_a_module_tag(tmp_path):
    """Implements: TC-411"""
    # Adequacy witness: a comparison letting a test part fall back to its file's
    # declaration reads this cell as clean, and this test fails.
    text = TAG_CLEAN_FILE + "\n\n" + UNTAGGED_TEST
    _write_equality_tree(tmp_path, TAGGED_NODE, text)
    proc = run_traj(tmp_path, "--strict")
    assert _equality_findings(proc, "ERROR") == [
        _no_evidence(TAGGED_FILE),
        _no_tag(TAGGED_NODE),
    ], proc.stderr
    assert proc.returncode == 1, proc.stdout + proc.stderr


def test_a_test_repeating_its_modules_case_needs_its_own_part(tmp_path):
    """Implements: TC-411"""
    # Adequacy witness: a comparison letting a file-level tag cover the tests
    # beneath it reads the file-only cell below as clean, and this test fails.
    text = TAG_CLEAN_FILE + "\n\n" + TAGGED_TEST
    _write_equality_tree(tmp_path, TAGGED_FILE, text)
    file_only = run_traj(tmp_path, "--strict")
    assert _equality_findings(file_only, "ERROR") == [_no_evidence(TAGGED_NODE)], (
        file_only.stderr
    )
    assert file_only.returncode == 1, file_only.stdout + file_only.stderr

    both_parts = "{} {}".format(TAGGED_FILE, TAGGED_NODE)
    _write_equality_tree(tmp_path, both_parts, text)
    named = run_traj(tmp_path, "--strict")
    assert named.returncode == 0, named.stdout + named.stderr


def test_a_class_method_part_matches_its_tag(tmp_path):
    """Implements: TC-411"""
    method = TAGGED_FILE + "::TestC::test_m"
    _write_equality_tree(tmp_path, method, TAGGED_METHOD)
    matched = run_traj(tmp_path, "--strict")
    assert matched.returncode == 0, matched.stdout + matched.stderr

    other_class = TAGGED_FILE + "::TestD::test_m"
    _write_equality_tree(tmp_path, other_class, TAGGED_METHOD)
    mismatched = run_traj(tmp_path, "--strict")
    assert _equality_findings(mismatched, "ERROR") == [
        _no_evidence(method),
        _no_tag(other_class),
    ], mismatched.stderr
    assert mismatched.returncode == 1, mismatched.stdout + mismatched.stderr


def test_a_whitespace_separated_cell_reads_as_its_items(tmp_path):
    """Implements: TC-411"""
    second = TAGGED_FILE + "::test_b"
    cell = "{} {}".format(TAGGED_NODE, second)
    text = TAGGED_TEST + "\n\ndef test_b():\n    pass\n"
    _write_equality_tree(tmp_path, cell, text)
    proc = run_traj(tmp_path, "--strict")
    assert _equality_findings(proc, "ERROR") == [_no_tag(second)], proc.stderr
    assert proc.returncode == 1, proc.stdout + proc.stderr


def test_a_non_python_node_part_reads_both_findings(tmp_path):
    """Implements: TC-411"""
    rel = "tests/test_export.rs"
    text = "// Implements: TC-001\n"
    _write_equality_tree(tmp_path, rel, text, rel=rel)
    whole_file = run_traj(tmp_path, "--strict")
    assert whole_file.returncode == 0, whole_file.stdout + whole_file.stderr

    node = rel + "::test_export"
    _write_equality_tree(tmp_path, node, text, rel=rel)
    proc = run_traj(tmp_path, "--strict")
    assert _equality_findings(proc, "ERROR") == [
        _no_evidence(rel),
        _no_tag(node),
    ], proc.stderr
    assert proc.returncode == 1, proc.stdout + proc.stderr


@pytest.mark.parametrize(
    "tests_dir, also_inside",
    [
        ("qa/tests", []),
        ("qa/tests/", []),
        ("./qa/tests", []),
        (".", ["docs/notes.md", TAGGED_NODE]),
    ],
    ids=["plain", "trailing-slash", "dot-slash", "repo-root"],
)
def test_a_part_outside_the_tests_root_is_ignored(tmp_path, tests_dir, also_inside):
    """Implements: TC-412"""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\ntests = {}\n".format(tests_dir), encoding="utf-8"
    )
    inside = "qa/tests/test_tagged.py::test_a"
    cell = "docs/notes.md#anchor; {}; {}".format(TAGGED_NODE, inside)
    _write_equality_tree(tmp_path, cell, UNTAGGED_TEST, rel="qa/tests/test_tagged.py")
    proc = run_traj(tmp_path, "--strict")
    expected = [_no_tag(part) for part in sorted(also_inside + [inside])]
    assert _equality_findings(proc, "ERROR") == expected, proc.stderr
    assert proc.returncode == 1, proc.stdout + proc.stderr


def test_a_declaration_outside_the_tests_root_is_not_read(tmp_path):
    """Implements: TC-412"""
    # Adequacy witness: a reading that walks the repository rather than the
    # declared root finds the outside test's tag, and this test fails.
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "stack.ini").write_text(
        "[paths]\nsrc = src\ntests = qa/tests\n", encoding="utf-8"
    )
    inside = "qa/tests/test_tagged.py"
    _write_equality_tree(tmp_path, inside + "::test_a", TAGGED_TEST, rel=inside)
    _write_test_file(tmp_path, TAGGED_FILE, TAGGED_TEST)
    proc = run_traj(tmp_path, "--strict")
    assert _equality_findings(proc, "ERROR") == [], proc.stderr
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_a_placeholder_row_is_outside_the_equality_rule(tmp_path):
    """Implements: TC-412"""
    # Adequacy witness: a comparison judging every registry row reads TC-000's
    # untagged part as a difference, and this test fails in both phases.
    _write_test_file(tmp_path, TAGGED_FILE, UNTAGGED_TEST)
    _write_tc_rows(tmp_path, {"TC-000": "Accepted"}, TAGGED_NODE)
    placeholder_only = run_traj(tmp_path, "--strict")
    assert _equality_findings(placeholder_only, "ERROR") == [], placeholder_only.stderr
    assert placeholder_only.returncode == 0, (
        placeholder_only.stdout + placeholder_only.stderr
    )

    _write_tc_rows(tmp_path, {"TC-000": "Accepted", "TC-001": "Accepted"}, TAGGED_NODE)
    beside_a_live_row = run_traj(tmp_path, "--strict")
    assert _equality_findings(beside_a_live_row, "ERROR") == [_no_tag(TAGGED_NODE)], (
        beside_a_live_row.stderr
    )
    assert beside_a_live_row.returncode == 1, (
        beside_a_live_row.stdout + beside_a_live_row.stderr
    )


def test_the_equality_check_is_vacuous_with_no_tests_root_or_no_registry(tmp_path):
    """Implements: TC-412"""
    _write_test_file(tmp_path, TAGGED_FILE, UNTAGGED_TEST)
    no_registry = run_traj(tmp_path, "--strict")
    assert no_registry.returncode == 0, no_registry.stdout + no_registry.stderr
    assert _equality_findings(no_registry, "ERROR") == [], no_registry.stderr

    _write_tc_rows(tmp_path, {"TC-001": "Accepted"}, TAGGED_NODE)
    paired = run_traj(tmp_path, "--strict")
    assert _equality_findings(paired, "ERROR") == [_no_tag(TAGGED_NODE)], paired.stderr
    assert paired.returncode == 1, paired.stdout + paired.stderr

    shutil.rmtree(tmp_path / "tests")
    no_tests = run_traj(tmp_path, "--strict")
    assert no_tests.returncode == 0, no_tests.stdout + no_tests.stderr
    assert _equality_findings(no_tests, "ERROR") == [], no_tests.stderr


def test_an_unreadable_file_adds_no_equality_finding(tmp_path):
    """Implements: TC-412"""
    broken = "tests/test_broken.py"
    cell = "{}::test_x; {}".format(broken, TAGGED_NODE)
    _write_equality_tree(tmp_path, cell, UNTAGGED_TEST)
    _write_test_file(tmp_path, broken, "def broken(:\n")
    proc = run_traj(tmp_path, "--strict")
    assert len(_tag_finding(proc, "ERROR", broken, 1, "unreadable")) == 1, proc.stderr
    assert _equality_findings(proc, "ERROR") == [_no_tag(TAGGED_NODE)], proc.stderr
    assert proc.returncode == 1, proc.stdout + proc.stderr


def test_a_note_only_cell_has_no_part_and_a_tag_on_it_is_a_finding(tmp_path):
    """Implements: TC-412"""
    note = "(owed by WI-900)"
    _write_equality_tree(tmp_path, note, UNTAGGED_TEST)
    untagged = run_traj(tmp_path, "--strict")
    # The case is accepted and automated, so its missing test is WI-1001's
    # finding; the equality rule this test pins reads nothing.
    assert _equality_findings(untagged, "ERROR") == [], untagged.stderr

    _write_equality_tree(tmp_path, note, TAG_CLEAN_FILE)
    tagged = run_traj(tmp_path, "--strict")
    assert _equality_findings(tagged, "ERROR") == [_no_evidence(TAGGED_FILE)], (
        tagged.stderr
    )
    assert tagged.returncode == 1, tagged.stdout + tagged.stderr


# --- WI-1001: an accepted automated case has a test declaring it --------------
# A finding prints as `<level> - <TC>: no test declares it`. Each comparison is
# of the whole list of them, so their number and order are pinned too. TC-428
# pins the ruling's input table and TC-429 the sequence a case walks, each
# verifying LLR-395; TC-475 pins the clause neither covers, that a declared
# test that fails leaves its case clean.

OWED_NOTE = "(owed by the tests commit)"
TAG_MALFORMED_FILE = '"""Module text.\n\nImplements: TC-001, SR-002\n"""\n'


def _undeclared(proc, level):
    """`proc`'s `no test declares it` findings at `level` in print order, prefix
    dropped."""
    prefix = "check_trajectory: {} - ".format(level)
    return [
        line[len(prefix) :]
        for line in proc.stderr.splitlines()
        if line.startswith(prefix) and line.endswith(": no test declares it")
    ]


def _no_test(tc="TC-001"):
    """The finding for an accepted automated case no test declares."""
    return "{}: no test declares it".format(tc)


def _case_row(tc="TC-001", status="Accepted", automated="Yes", evidence=OWED_NOTE):
    """One TOML test-case row; `None` leaves a cell's key out."""
    cells = ['verifies = ["SR-001"]', 'level = "Unit"', 'method = "m"']
    cells += ['tier = "Full"', 'expected = "e"']
    if automated is not None:
        cells.append('automated = "{}"'.format(automated))
    if evidence is not None:
        cells.append('evidence = "{}"'.format(evidence))
    cells.append('status = "{}"'.format(status))
    return "[test.{}]\n{}\n\n".format(tc, "\n".join(cells))


def _write_case_tree(root, rows, text=UNTAGGED_TEST, rel=TAGGED_FILE):
    """The TOML registry holding `rows`, and the one test file `text`."""
    path = root / "docs" / "test" / "test-cases.toml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(rows), encoding="utf-8")
    _write_test_file(root, rel, text)


def test_the_undeclared_rule_is_vacuous_with_no_tests_root_or_no_registry(tmp_path):
    """Implements: TC-428"""
    _write_test_file(tmp_path, TAGGED_FILE, UNTAGGED_TEST)
    no_registry = run_traj(tmp_path, "--strict")
    assert _undeclared(no_registry, "ERROR") == [], no_registry.stderr
    assert no_registry.returncode == 0, no_registry.stdout + no_registry.stderr

    _write_case_tree(tmp_path, [_case_row()])
    paired = run_traj(tmp_path, "--strict")
    assert _undeclared(paired, "ERROR") == [_no_test()], paired.stderr
    assert paired.returncode == 1, paired.stdout + paired.stderr

    shutil.rmtree(tmp_path / "tests")
    no_tests = run_traj(tmp_path, "--strict")
    assert _undeclared(no_tests, "ERROR") == [], no_tests.stderr
    assert no_tests.returncode == 0, no_tests.stdout + no_tests.stderr


def test_an_unparseable_registry_stops_the_run_before_the_undeclared_rule(tmp_path):
    """Implements: TC-428"""
    _write_test_file(tmp_path, TAGGED_FILE, UNTAGGED_TEST)
    registry = tmp_path / "docs" / "test" / "test-cases.toml"
    registry.parent.mkdir(parents=True)
    registry.write_text("[test.TC-001\nverifies = [", encoding="utf-8")
    for extra in ([], ["--strict"]):
        proc = run_traj(tmp_path, *extra)
        assert "spine_carrier:" in proc.stderr, proc.stderr
        assert "does not parse as TOML" in proc.stderr, proc.stderr
        assert "no test declares it" not in proc.stderr, proc.stderr
        assert proc.returncode == 1, proc.stdout + proc.stderr


def test_a_placeholder_row_owes_no_declaration(tmp_path):
    """Implements: TC-428"""
    _write_case_tree(tmp_path, [_case_row("TC-000")])
    placeholder_only = run_traj(tmp_path, "--strict")
    assert _undeclared(placeholder_only, "ERROR") == [], placeholder_only.stderr
    assert placeholder_only.returncode == 0, (
        placeholder_only.stdout + placeholder_only.stderr
    )

    _write_case_tree(tmp_path, [_case_row("TC-000"), _case_row()])
    beside = run_traj(tmp_path, "--strict")
    assert _undeclared(beside, "ERROR") == [_no_test()], beside.stderr


def test_a_drafted_case_owes_no_declaration_and_its_parts_are_still_held(tmp_path):
    """Implements: TC-428"""
    _write_case_tree(tmp_path, [_case_row(status="Drafted")])
    noted = run_traj(tmp_path, "--strict")
    assert _undeclared(noted, "ERROR") == [], noted.stderr
    assert noted.returncode == 0, noted.stdout + noted.stderr

    _write_case_tree(tmp_path, [_case_row(status="Drafted", evidence=TAGGED_NODE)])
    parted = run_traj(tmp_path, "--strict")
    assert _undeclared(parted, "ERROR") == [], parted.stderr
    assert _equality_findings(parted, "ERROR") == [_no_tag(TAGGED_NODE)], parted.stderr
    assert parted.returncode == 1, parted.stdout + parted.stderr


@pytest.mark.parametrize(
    "automated, carrier",
    [("No", "toml"), ("Sometimes", "toml"), (None, "toml"), ("", "csv")],
    ids=["no", "another-word", "absent-column", "blank"],
)
def test_a_case_not_automated_owes_no_declaration(tmp_path, automated, carrier):
    """Implements: TC-428"""
    if carrier == "toml":
        _write_case_tree(tmp_path, [_case_row(automated=automated)])
    else:
        # The TOML carrier refuses an explicit empty cell, so a blank one is the
        # legacy CSV carrier's.
        path = tmp_path / "docs" / "test" / "test-cases.csv"
        path.parent.mkdir(parents=True)
        path.write_text(
            "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,"
            "Evidence,Status\nTC-001,SR-001,Unit,m,Full,,e,,{},Accepted\n".format(
                OWED_NOTE
            ),
            encoding="utf-8",
        )
        _write_test_file(tmp_path, TAGGED_FILE, UNTAGGED_TEST)
    proc = run_traj(tmp_path, "--strict")
    assert _undeclared(proc, "ERROR") == [], proc.stderr
    assert proc.returncode == 0, proc.stdout + proc.stderr


@pytest.mark.parametrize(
    "status, automated",
    [("Accepted", "Yes"), ("Founded", "Yes"), ("Accepted", " YES ")],
    ids=["accepted", "founded", "padded-upper-case"],
)
def test_an_eligible_case_is_clean_when_tagged_and_named_when_not(
    tmp_path, status, automated
):
    """Implements: TC-428"""
    row = _case_row(status=status, automated=automated, evidence=TAGGED_NODE)
    _write_case_tree(tmp_path, [row], TAGGED_TEST)
    tagged = run_traj(tmp_path, "--strict")
    assert _undeclared(tagged, "ERROR") == [], tagged.stderr
    assert tagged.returncode == 0, tagged.stdout + tagged.stderr

    _write_case_tree(tmp_path, [_case_row(status=status, automated=automated)])
    untagged = run_traj(tmp_path, "--strict")
    assert _undeclared(untagged, "ERROR") == [_no_test()], untagged.stderr
    assert untagged.returncode == 1, untagged.stdout + untagged.stderr


def test_a_part_in_an_unreadable_file_adds_no_undeclared_finding(tmp_path):
    """Implements: TC-428"""
    # Adequacy witness: a rule blind to the refused set reads both rows below
    # as undeclared, and this test fails in both phases.
    broken = "tests/test_broken.py"
    _write_case_tree(tmp_path, [_case_row(evidence=broken + "::test_x")])
    _write_test_file(tmp_path, broken, "def broken(:\n")
    alone = run_traj(tmp_path, "--strict")
    assert len(_tag_finding(alone, "ERROR", broken, 1, "unreadable")) == 1, alone.stderr
    assert _undeclared(alone, "ERROR") == [], alone.stderr
    assert alone.returncode == 1, alone.stdout + alone.stderr

    cell = "{}::test_x; {}".format(broken, TAGGED_NODE)
    _write_case_tree(tmp_path, [_case_row(evidence=cell)])
    beside = run_traj(tmp_path, "--strict")
    assert _undeclared(beside, "ERROR") == [], beside.stderr
    assert _equality_findings(beside, "ERROR") == [_no_tag(TAGGED_NODE)], beside.stderr


@pytest.mark.parametrize(
    "evidence, untagged_parts",
    [
        (OWED_NOTE, []),
        (None, []),
        (TAGGED_FILE, [TAGGED_FILE]),
        ("docs/notes.md#anchor", []),
        ("tests/test_missing.py::test_x", ["tests/test_missing.py::test_x"]),
    ],
    ids=["note", "no-cell", "whole-file", "outside-the-root", "absent-path"],
)
def test_an_eligible_untagged_case_is_named_whatever_its_cell_holds(
    tmp_path, evidence, untagged_parts
):
    """Implements: TC-428"""
    _write_case_tree(tmp_path, [_case_row(evidence=evidence)])
    proc = run_traj(tmp_path, "--strict")
    assert _undeclared(proc, "ERROR") == [_no_test()], proc.stderr
    expected = [_no_tag(part) for part in untagged_parts]
    assert _equality_findings(proc, "ERROR") == expected, proc.stderr
    assert proc.returncode == 1, proc.stdout + proc.stderr


@pytest.mark.parametrize(
    "text, shape",
    [(TAG_MISPLACED_FILE, "misplaced"), (TAG_MALFORMED_FILE, "malformed")],
    ids=["misplaced", "malformed"],
)
def test_a_refused_tag_declares_nothing(tmp_path, text, shape):
    """Implements: TC-428"""
    _write_case_tree(tmp_path, [_case_row(evidence=TAGGED_FILE)], text)
    only = run_traj(tmp_path, "--strict")
    assert len(_tag_finding(only, "ERROR", TAGGED_FILE, 3, shape)) == 1, only.stderr
    assert _undeclared(only, "ERROR") == [_no_test()], only.stderr
    assert only.returncode == 1, only.stdout + only.stderr

    _write_case_tree(tmp_path, [_case_row(evidence=TAGGED_NODE)], text + TAGGED_TEST)
    beside = run_traj(tmp_path, "--strict")
    assert len(_tag_finding(beside, "ERROR", TAGGED_FILE, 3, shape)) == 1, beside.stderr
    assert _undeclared(beside, "ERROR") == [], beside.stderr


FAILING_TAGGED_TEST = TAGGED_TEST + "    assert False\n"


def test_a_declared_test_that_fails_leaves_its_case_clean(tmp_path):
    """The rule reads declarations, not test outcomes: the case's one test is
    validly tagged and fails when run, and the case reads clean.

    Implements: TC-475"""
    namespace = {}
    exec(FAILING_TAGGED_TEST, namespace)
    with pytest.raises(AssertionError):
        namespace["test_a"]()
    row = _case_row(evidence=TAGGED_NODE)
    _write_case_tree(tmp_path, [row], FAILING_TAGGED_TEST)
    proc = run_traj(tmp_path, "--strict")
    assert _undeclared(proc, "ERROR") == [], proc.stderr
    assert _equality_findings(proc, "ERROR") == [], proc.stderr
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_one_tag_clears_the_part_and_the_declaration_findings(tmp_path):
    """Implements: TC-428"""
    _write_case_tree(tmp_path, [_case_row(evidence=TAGGED_NODE)])
    untagged = run_traj(tmp_path, "--strict")
    assert _equality_findings(untagged, "ERROR") == [_no_tag(TAGGED_NODE)], (
        untagged.stderr
    )
    assert _undeclared(untagged, "ERROR") == [_no_test()], untagged.stderr

    _write_case_tree(tmp_path, [_case_row(evidence=TAGGED_NODE)], TAGGED_TEST)
    tagged = run_traj(tmp_path, "--strict")
    assert _equality_findings(tagged, "ERROR") == [], tagged.stderr
    assert _undeclared(tagged, "ERROR") == [], tagged.stderr
    assert tagged.returncode == 0, tagged.stdout + tagged.stderr


def test_a_lanes_order_never_meets_the_undeclared_finding(tmp_path):
    """Implements: TC-429"""
    _write_case_tree(tmp_path, [_case_row(status="Drafted")])
    intent = run_traj(tmp_path, "--strict")
    assert _undeclared(intent, "ERROR") == [], intent.stderr
    assert intent.returncode == 0, intent.stdout + intent.stderr

    drafted = _case_row(status="Drafted", evidence=TAGGED_NODE)
    _write_case_tree(tmp_path, [drafted], TAGGED_TEST)
    tests_commit = run_traj(tmp_path, "--strict")
    assert tests_commit.returncode == 0, tests_commit.stdout + tests_commit.stderr

    _write_case_tree(tmp_path, [_case_row(evidence=TAGGED_NODE)], TAGGED_TEST)
    act = run_traj(tmp_path, "--strict")
    assert _undeclared(act, "ERROR") == [], act.stderr
    assert act.returncode == 0, act.stdout + act.stderr


@pytest.mark.parametrize(
    "work_items", [False, True], ids=["no-work-items", "with-work-items"]
)
def test_an_accepted_case_with_no_tag_warns_plain_and_errors_strict(
    tmp_path, work_items
):
    """Implements: TC-429"""
    if work_items:
        write_wis(tmp_path, "WI-001,A,scripts,,,done,Shipped it.\n")
    _write_case_tree(tmp_path, [_case_row()])
    plain = run_traj(tmp_path)
    assert _undeclared(plain, "WARN") == [_no_test()], plain.stderr
    assert plain.returncode == 0, plain.stdout + plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert _undeclared(strict, "ERROR") == [_no_test()], strict.stderr
    assert strict.returncode == 1, strict.stdout + strict.stderr

    _write_case_tree(tmp_path, [_case_row(evidence=TAGGED_NODE)], TAGGED_TEST)
    tagged = run_traj(tmp_path, "--strict")
    assert tagged.returncode == 0, tagged.stdout + tagged.stderr


def test_the_undeclared_finding_on_a_bootstrapped_scaffold(scaffold):
    """Implements: TC-429"""
    registry = scaffold / "docs" / "test" / "test-cases.toml"
    template = registry.read_text(encoding="utf-8") + "\n"

    def trajectory_at(stage):
        return run_py(
            ["scripts/check.py", "--stage", stage, "--run-steps", "trajectory"],
            cwd=scaffold,
        )

    registry.write_text(template + _case_row(), encoding="utf-8")
    _write_test_file(scaffold, TAGGED_FILE, UNTAGGED_TEST)
    below = trajectory_at("DevStg-Tests")
    assert below.returncode == 0, below.stdout + below.stderr
    assert _no_test() in below.stdout + below.stderr
    at_rung = trajectory_at("DevStg-Impl")
    assert at_rung.returncode != 0, at_rung.stdout + at_rung.stderr
    assert "=== trajectory" in at_rung.stdout, at_rung.stdout
    assert "ERROR - " + _no_test() in at_rung.stdout + at_rung.stderr

    registry.write_text(template + _case_row(evidence=TAGGED_NODE), encoding="utf-8")
    _write_test_file(scaffold, TAGGED_FILE, TAGGED_TEST)
    tagged = trajectory_at("DevStg-Impl")
    assert tagged.returncode == 0, tagged.stdout + tagged.stderr


# --- SR-165 / WI-999: the partition's derivation record (TC-166) --------------
# In-process over `component_findings`, the record's one reader. The record is
# eight flat cells on a CMP row; one row per partition holds it and the
# partition's other rows cite it with `derivation`. The numbers are OI-130's
# ruling on this repository's own partition (minimize cut: P5 140, P3 152,
# P4 235, every candidate violating the one constraint), so the clean case is
# the record the kit's own CMP-006 holds.

RECORD = {
    "candidates": '["P5", "P3", "P4"]',
    "objective": '"minimize cut"',
    "constraints": '["one-home-per-behaviour: P3 P4 P5"]',
    "scores": '["P5=140", "P3=152", "P4=235"]',
    "selected": '"P5"',
    "ruling": '"the operator, 2026-11-16, recorded under OI-130"',
}
CITE = {"derivation": '"CMP-001"'}
CMP_CSV_PATH = "docs/requirements/components.toml"
HELD = CMP_CSV_PATH + " CMP-001 (record cited by CMP-002, CMP-003): derivation record: "


def _record(**changes):
    """RECORD with each `changes` cell replaced by a TOML literal, or dropped
    when the value is None."""
    cells = dict(RECORD, **changes)
    return {key: value for key, value in cells.items() if value is not None}


def _derivation_findings(root, rows):
    """`component_findings` over a registry of `rows`, `[(id, {key: TOML
    literal})]`, written as live `Accepted` rows."""
    blocks = [
        '[component.{0}]\nname = "{0}"\nstatus = "Accepted"\n'.format(rid)
        + "".join("{} = {}\n".format(key, value) for key, value in cells.items())
        for rid, cells in rows
    ]
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "components.toml").write_text("\n".join(blocks), encoding="utf-8")
    return trajectory_arch.component_findings(root)


def _partition(root, **changes):
    """A three-row partition: CMP-001 holds the record, the others cite it."""
    rows = [("CMP-001", _record(**changes)), ("CMP-002", CITE), ("CMP-003", CITE)]
    return _derivation_findings(root, rows)


def test_a_complete_derivation_record_passes_silently(tmp_path):
    """(a) The record OI-130 ruled, held once and cited twice, is silent; so is
    a record declaring no constraint and maximizing its metric.

    Implements: TC-166"""
    assert _partition(tmp_path) == []
    assert (
        _partition(
            tmp_path,
            objective='"maximize cohesion"',
            constraints='["none"]',
            candidates='["P4", "P3", "P5"]',
            selected='"P4"',
        )
        == []
    )


@pytest.mark.parametrize(
    "changes,element",
    [
        ({"candidates": None}, "`candidates` is missing"),
        ({"objective": None}, "`objective` is missing"),
        ({"constraints": None}, "`constraints` is missing"),
        ({"scores": '["P5=140", "P4=235"]'}, "`scores` has no score for candidate P3"),
        ({"scores": None}, "`scores` is missing"),
        ({"selected": None}, "`selected` is missing"),
        ({"ruling": None}, "`ruling` is missing"),
    ],
)
def test_each_omitted_record_element_is_reported_once(tmp_path, changes, element):
    """(b) Each element omitted in turn is one finding, naming the row and the
    element: reported on the holding row, which names the rows citing it.

    Implements: TC-166"""
    assert _partition(tmp_path, **changes) == [HELD + element]


def test_a_ranking_that_does_not_recompute_is_reported(tmp_path):
    """(c) The recompute: a feasible candidate ranks above every infeasible one,
    then by score in the objective's direction, and a tie may be listed in
    either order.

    Implements: TC-166"""
    misordered = _partition(tmp_path, candidates='["P3", "P5", "P4"]')
    assert misordered == [HELD + "the recompute ranks P5 above P3, listed before it"]
    reversed_direction = _partition(tmp_path, objective='"maximize cut"')
    assert reversed_direction[0].startswith(HELD + "the recompute ranks P3 above P5")
    # P5 alone violates the constraint, so the worse-scoring P3 and P4 rank
    # above it, and P3 is the selection the scores rank first.
    feasible_first = {
        "candidates": '["P3", "P4", "P5"]',
        "constraints": '["one-home-per-behaviour: P5"]',
        "selected": '"P3"',
    }
    assert _partition(tmp_path, **feasible_first) == []
    tied = {"scores": '["P5=140", "P3=140", "P4=235"]'}
    assert _partition(tmp_path, **tied) == []
    assert _partition(tmp_path, candidates='["P3", "P5", "P4"]', **tied) == []
    assert _partition(tmp_path, selected='"P3"', **tied) == []


def test_a_selection_not_ranked_first_needs_an_override_naming_it(tmp_path):
    """(d) A selection the scores do not rank first is a finding; the same
    record with an override naming the selection is silent; an override
    naming anything else does not silence it; and an override where the
    selection ranks first is itself a finding.

    Implements: TC-166"""
    unexplained = _partition(tmp_path, selected='"P3"')
    assert unexplained == [
        HELD + "`selected` P3 is not ranked first and has no `override`"
    ]
    overridden = '"P3: the operator keeps the actor split for the review path"'
    assert _partition(tmp_path, selected='"P3"', override=overridden) == []
    elsewhere = _partition(tmp_path, selected='"P3"', override='"P4: a reason"')
    assert elsewhere == [HELD + "`override` names P4, not the selected P3"]
    needless = _partition(tmp_path, override='"P5: a reason"')
    assert needless == [
        HELD + "`override` is present although `selected` P5 ranks first"
    ]


def test_no_components_and_the_example_row_are_vacuous(tmp_path):
    """(e) A project declaring no components, and the shipped `-000` row, are
    vacuous; `[checks] components_check = false` turns the whole pass off.

    Implements: TC-166"""
    assert trajectory_arch.component_findings(tmp_path) == []
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    shutil.copyfile(
        ROOT / "project-trajectory" / "registries" / "components.template.toml",
        req / "components.toml",
    )
    assert trajectory_arch.component_findings(tmp_path) == []
    (tmp_path / "docs" / "process.toml").write_text(
        "[checks]\ncomponents_check = false\n", encoding="utf-8"
    )
    assert _derivation_findings(tmp_path, [("CMP-001", {})]) == []


@pytest.mark.parametrize(
    "changes,cause",
    [
        ({"objective": '"optimize cut"'}, "`objective` 'optimize cut' is not"),
        ({"objective": '"minimize"'}, "`objective` 'minimize' is not"),
        ({"scores": '["P5=140", "P3=many", "P4=235"]'}, "'P3=many' is not `<"),
        ({"scores": '["P5=140", "P3=152", "P4=235", "P9=1"]'}, "'P9=1' is an extra"),
        ({"scores": '["P5=140", "P5=141", "P3=152", "P4=235"]'}, "'P5=141' is an ex"),
        ({"candidates": '["P5", "P3", "P4", "P3"]'}, "lists P3 more than once"),
        ({"selected": '"P9"'}, "`selected` P9 is not a candidate"),
        ({"constraints": '["one-home: P3 P9"]'}, "violator P9, which is not a cand"),
        ({"constraints": '["one-home P3"]'}, "entry 'one-home P3' is not `<name>"),
        ({"constraints": '["none", "one-home: P3"]'}, "entry 'none' is not `<name>"),
        ({"override": '"P5"'}, "`override` 'P5' is not `<candidate>: <reason>`"),
        ({"override": '"P5:"'}, "`override` 'P5:' is not `<candidate>: <reason>`"),
    ],
)
def test_each_malformed_record_cell_is_reported(tmp_path, changes, cause):
    """Each value outside the record's form is one finding naming the cell and
    the cause; the ranking does not run on it.

    Implements: TC-166"""
    findings = _partition(tmp_path, **changes)
    assert len(findings) == 1 and findings[0].startswith(HELD), findings
    assert cause in findings[0], findings


@pytest.mark.parametrize(
    "citing,cause",
    [
        ({"derivation": '"CMP-099"'}, "names CMP-099, which is no live component"),
        ({"derivation": '"CMP-000"'}, "names CMP-000, which is no live component"),
        ({"derivation": '"CMP-002"'}, "points at the row itself"),
        ({"derivation": '"CMP-003"'}, "names CMP-003, which itself cites another"),
        (dict(CITE, selected='"P5"'), "sits beside record cells"),
    ],
)
def test_each_malformed_derivation_is_reported(tmp_path, citing, cause):
    """A `derivation` that is dangling (the vacuous `-000` row included),
    points at its own row, chains to another citing row, or sits beside record
    cells is a finding on the citing row.

    Implements: TC-166"""
    rows = [
        ("CMP-001", _record()),
        ("CMP-002", citing),
        ("CMP-003", CITE),
    ]
    findings = _derivation_findings(tmp_path, rows)
    prefix = CMP_CSV_PATH + " CMP-002: derivation record: `derivation` "
    assert len(findings) == 1 and findings[0].startswith(prefix), findings
    assert cause in findings[0], findings


def test_an_absent_record_is_reported_once_on_the_row_its_citers_name(tmp_path):
    """Absent: a row with neither record cells nor `derivation`. A held record
    is reported once, on the holding row, naming the rows citing it.

    Implements: TC-166"""
    held = _derivation_findings(
        tmp_path, [("CMP-001", {}), ("CMP-002", CITE), ("CMP-003", CITE)]
    )
    assert len(held) == 1, held
    assert held[0].startswith(
        CMP_CSV_PATH
        + " CMP-001 (record cited by CMP-002, CMP-003): no derivation record"
    )
    alone = _derivation_findings(tmp_path, [("CMP-001", _record()), ("CMP-002", {})])
    assert len(alone) == 1 and alone[0].startswith(
        CMP_CSV_PATH + " CMP-002: no derivation record"
    ), alone


def test_the_ranking_runs_only_on_a_complete_well_formed_record(tmp_path):
    """A record that fails the element or form checks has already failed
    closed: its misordered ranking is not also reported.

    Implements: TC-166"""
    findings = _partition(tmp_path, candidates='["P3", "P5", "P4"]', ruling=None)
    assert findings == [HELD + "`ruling` is missing"]


def test_a_derivation_finding_warns_plain_and_fails_strict(tmp_path):
    """Implements: TC-166"""
    _derivation_findings(tmp_path, [("CMP-001", {})])
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "WARN - " + CMP_CSV_PATH + " CMP-001: no derivation record" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1, strict.stdout + strict.stderr
    assert "ERROR - " + CMP_CSV_PATH + " CMP-001: no derivation record" in strict.stderr
