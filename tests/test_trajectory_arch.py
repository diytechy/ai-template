"""check_trajectory.py — decision over architecture inputs (WI-277: split
verbatim from tests/test_trajectory.py by behavior boundary).

Interface-connectivity coverage (WI-056), the How-SW top-view right-sizing
bound (WI-073/FB5), knowledge⇒component coupling (WI-153), the phase anchors +
phase-drop detector (WI-093), the approval-brief hierarchy-view
lint (WI-146b), cross-CMP edges without a declared IF (WI-064), and specs
acting on declared interface boundaries (WI-191).

check_vocab: allow-file — THE ANCHOR FIXTURES MUST AUTHOR THE RETIRED SPELLING.
`check_trajectory` TRANSLATES `[p]-[g1]`/`[p]-[reqs]` on read and never rewrites
a committed WI title, so the only way to prove the translation still works is to
build titles carrying it. A file-level marker rather than ~25 line-level ones:
every occurrence here is one fixture class with one reason, and a marker per line
would say the same thing 25 times while hiding whether a NEW one had appeared.
"""

import csv
import re
import shutil
import sys
from pathlib import Path


from conftest import ROOT, SCRIPTS, load_script, run_py

# `kitlib` is a PACKAGE UNDER scripts/, which nothing puts on `sys.path` until
# the first `load_script` call — so a module-level `from kitlib import ...` in a
# test file resolves only when some earlier-collected module happens to have
# called it first. That held by accident until an xdist worker collected this
# module first (WI-498 slice 4). Stated explicitly here rather than inherited.
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from kitlib import stage as kitstage  # noqa: E402

wi_convert = load_script("wi_convert")
check_trajectory = load_script("check_trajectory")


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
# ...plus the SpecRef + BlockRef columns (S1) — used by the SSOT-rule tests.
SR_WI_COLUMNS = WI_COLUMNS + ",SpecRef,BlockRef"

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
# `status = "Approved"` (OI-67 put the spine's own two words on the row).
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
            else "approved"
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
                    else "Approved"
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
                body += "\n\nContracts: " + ", ".join(mod["contracts"])
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


def test_interface_coverage_warns(tmp_path):
    # Multi-module arch-map with NO interfaces.csv -> "connectivity undeclared"
    # (the ruled opt-out, default-on posture), and the exit code is still 0.
    write_arch(tmp_path, ARCH_2MOD)
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" in proc.stderr


def test_interface_check_off_silences(tmp_path):
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
    # One Provides seam a->b: a has no Consumes, b has no Provides -> both
    # missing-direction warns fire (exit 0).
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"call",SR-001,v1,Stable,Active,,\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares no Consumes seam" in proc.stderr  # mod_a
    assert "declares no Provides seam" in proc.stderr  # mod_b


def test_source_sink_marker_suppresses_direction_warn(tmp_path):
    # mod_a marked source (consumes nothing), mod_b marked sink (provides nothing)
    # -> both missing-direction warns suppressed by the honesty valve.
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"call",SR-001,v1,Stable,Active,,source\n'
        'IF-002,Consumes,scripts/mod_b,docs/stack.ini,"reads",SR-001,v1,Stable,Active,,sink\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares no Consumes seam" not in proc.stderr
    assert "declares no Provides seam" not in proc.stderr


def test_seam_tc_citation_warn(tmp_path):
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
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,approved,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Approved\n",
        encoding="utf-8",
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares no Consumes seam" not in proc.stderr  # symmetric -> covered
    seam = [ln for ln in proc.stderr.splitlines() if "cited by no TC" in ln]
    assert len(seam) == 1, proc.stderr
    assert "1 IF seam(s)" in seam[0] and "IF-002" in seam[0]
    assert "IF-001" not in seam[0]  # the TC citation suppresses it
    # IF-002 is `draft` and IF-001 `approved`, so the row that warns is the one
    # NO TC cites regardless of maturity — the arming key really is gone, not
    # merely renamed.


def test_contracts_docstring_citation_warns(tmp_path):
    # A module's `Contracts (interfaces):` arch-map line names IF-003 (absent from
    # the registry) -> forward warn; and once the convention is in use, a registry
    # IF declared by no module warns in reverse.
    arch = ARCH_2MOD.replace("_A._\n", "_A._\nContracts (interfaces): IF-003\n")
    write_arch(tmp_path, arch)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,approved,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "declares Contracts: IF-003 but no such IF-### row" in proc.stderr
    # OWNER-EXACT since OI-67 slice 2: IF-001 is owned by mod_a, whose marker
    # names IF-003 only, so the warn names the OWNER — not "no script".
    assert (
        "IF IF-001 is owned by 'scripts/mod_a', but that module's Contracts: "
        "line does not declare it" in proc.stderr
    )


def test_a_seam_declared_on_the_wrong_module_is_named(tmp_path):
    # The id-global hole the OI-66 build round named: IF-001 declared on mod_a
    # while the registry owns it to mod_b used to PASS. The owner is the one
    # declaration site, so the mismatch is named; the id-global fallback stays
    # only for an owner the tree cannot resolve.
    arch = ARCH_2MOD.replace("_A._\n", "_A._\nContracts (interfaces): IF-001\n")
    write_arch(tmp_path, arch)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,approved,Active,,\n',
    )
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert (
        "IF IF-001 is owned by 'scripts/mod_b', but that module's Contracts: "
        "line does not declare it" in proc.stderr
    )
    assert "no source declares it" not in proc.stderr


def test_interface_warns_never_fail_strict(tmp_path):
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
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,approved,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Approved\n",
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
    # stays green (no ERROR, no "migration allowlist" WARN line either — an
    # allowlisted seam is silent on THIS check), while the informational total
    # in `interface_findings` still reports it (the debt stays visible).
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,approved,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Approved\n",
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
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,approved,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Approved\n",
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
    # greens the gate. Do NOT relitigate the seed itself: it was independently
    # reproduced as an honest measurement of the seeding tree (120 uncited of
    # 130 live, nothing padded, nothing pre-empted). This pin exists so that
    # the list's FUTURE is reviewed. Pruning an entry whose seam gained a TC is
    # the intended end state — when you prune, lower `seed-count` in the file
    # and delete the id here, in the same commit, and say so in the log.
    # PRUNED 2026-08-29 (OI-67 slice 4): IF-075, whose seam gained TC-161's
    # citation when IF-127 collapsed into it, and IF-116, which collapsed into
    # IF-101 — 120 -> 118, seed-count lowered in the same commit.
    "IF-001 IF-002 IF-003 IF-004 IF-005 IF-006 IF-008 IF-009 IF-010 IF-011 "
    "IF-012 IF-013 IF-014 IF-015 IF-016 IF-017 IF-018 IF-019 IF-020 IF-021 "
    "IF-022 IF-023 IF-024 IF-025 IF-026 IF-028 IF-029 IF-030 IF-031 IF-032 "
    "IF-033 IF-034 IF-035 IF-036 IF-037 IF-038 IF-039 IF-040 IF-041 IF-042 "
    "IF-043 IF-044 IF-045 IF-046 IF-047 IF-048 IF-049 IF-050 IF-051 IF-052 "
    "IF-053 IF-054 IF-055 IF-056 IF-057 IF-058 IF-059 IF-060 IF-061 IF-064 "
    "IF-065 IF-066 IF-068 IF-069 IF-070 IF-071 IF-072 IF-073 IF-074 "
    "IF-076 IF-077 IF-078 IF-079 IF-080 IF-081 IF-082 IF-083 IF-084 IF-085 "
    "IF-086 IF-087 IF-088 IF-089 IF-092 IF-097 IF-098 IF-099 IF-100 IF-102 "
    "IF-103 IF-104 IF-105 IF-106 IF-107 IF-108 IF-109 IF-110 IF-111 IF-112 "
    "IF-113 IF-114 IF-115 IF-117 IF-118 IF-119 IF-120 IF-121 IF-122 "
    "IF-125 IF-126 IF-130 IF-131 IF-132 IF-133 IF-134 IF-135 IF-136 IF-137"
).split()


def test_a_multi_valued_endpoint_cell_declares_every_pair_in_it(tmp_path):
    """2026-08-21 review, M-14: `trace.py` splits an endpoint cell on `;` and
    this reader did not, so the registry's two readers disagreed about seven
    rows — every combination named in a `;`-joined cell is a declared pair, or
    a real seam reads as undeclared to half the machinery."""
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,"scripts/mod_b; scripts/mod_c","a to b and c",'
        "SR-001,v1,approved,Active,,\n",
    )
    pairs = check_trajectory._declared_seam_pairs(tmp_path)
    assert ("scripts/mod_a", "scripts/mod_b") in pairs
    assert ("scripts/mod_a", "scripts/mod_c") in pairs
    assert ("scripts/mod_c", "scripts/mod_a") in pairs  # stored both ways
    # And nothing carries the unsplit cell as if it were one module name.
    assert not [p for p in pairs if any(";" in e for e in p)], sorted(pairs)


def test_this_repos_seam_tc_allowlist_is_exactly_its_seeded_set():
    entries, seed = check_trajectory.parse_if_tc_allow(
        (ROOT / "docs" / "if-tc-coverage-allow").read_text(encoding="utf-8")
    )
    assert seed == 118, "the declared seed-count moved without this pin moving"
    assert len(SEEDED_IF_TC_ALLOW) == 118
    assert [i for i, _ in entries[:118]] == SEEDED_IF_TC_ALLOW
    # And every entry past the seed carries its reason, or it suppresses
    # nothing — the reader drops it, so this is a statement about the FILE
    # being honest rather than about the reader being lenient.
    assert all(reason for _id, reason in entries[118:]), entries[118:]


def test_a_bare_addition_past_the_seed_suppresses_nothing(tmp_path):
    # THE ONE-LINE EDIT THE REVIEW EXECUTED: a new seam reds --strict, and
    # appending its bare id greened it — indistinguishable from the 120 seeded
    # lines, no hygiene line, no test. Now the bare addition is DROPPED by the
    # reader (the seam still errors) and the growth is reported.
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,approved,Active,,\n'
        'IF-002,Provides,scripts/mod_b,scripts/mod_a,"b to a",SR-001,v1,draft,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Approved\n",
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


def test_if_tc_allow_malformed_line_is_reported_end_to_end(tmp_path):
    # The same fixture `test_a_bare_addition_past_the_seed_suppresses_nothing`
    # uses, proving the new arm rides the real `main()` wiring at the same
    # WARN-plain / ERROR-under-`--strict` severity `if_tc_coverage_findings`
    # already uses, not a parallel channel.
    write_arch(tmp_path, ARCH_2MOD)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_a,scripts/mod_b,"a to b",SR-001,v1,approved,Active,,\n',
    )
    (tmp_path / "docs" / "test").mkdir(parents=True, exist_ok=True)
    (tmp_path / "docs" / "test" / "test-cases.csv").write_text(
        "TC-ID,Verifies,Level,Method,Tier,Parameters,Expected,Automated,Evidence,Status\n"
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Approved\n",
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
        'IF-001,Provides,scripts/mod_a,downstream adopter,"a to world",SR-001,v1,approved,Active,,\n',
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


def write_cmps(root, body):
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    (req / "components.toml").write_text(
        _csv_body_to_toml(CMP_HDR, "component", body), encoding="utf-8"
    )


def write_tagged_llrs(root, pairs):
    """`pairs` = [(module, CMP-id)]; writes an LLR csv (Component column) so a
    module joins its CMP through its LLR's Component tag (the AXES membership)."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    body = "".join(
        "LLR-{:03d},SR-001,T,{},f,d,(see TC),Approved,{}\n".format(i + 1, mod, cmp)
        for i, (mod, cmp) in enumerate(pairs)
    )
    (req / "low-level-requirements.csv").write_text(
        TAGGED_LLR_HDR + body, encoding="utf-8"
    )


def test_top_view_over_bound_warns_plain_fails_strict(tmp_path):
    # 12 modules, no CMP rows -> 12 uncontained top items > 10.
    write_arch(tmp_path, _arch_n(12))
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert "How-SW top view has 12 items" in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "How-SW top view has 12 items" in strict.stderr


def test_declaring_components_below_bound_clears_it(tmp_path):
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
    write_arch(tmp_path, _arch_n(12))
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_ten_module_inventory_is_vacuous(tmp_path):
    # Exactly at the bound with no CMP rows -> passes trivially (the bound, not
    # the registry, is the rule).
    write_arch(tmp_path, _arch_n(10))
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "How-SW top view" not in proc.stderr


def test_absent_inventory_top_view_is_vacuous(tmp_path):
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
    write_tagged_llrs(
        tmp_path, [("scripts/mod_0", "CMP-001"), ("scripts/mod_1", "CMP-001")]
    )
    write_src_profile(tmp_path, ["mod_0.py", "mod_1.py"], src=src)


def test_untagged_module_on_disk_reds_the_containment_rule(tmp_path):
    # The WI-387 topology under the live inventory: a new module on disk with
    # no Component tag is uncontained the moment it exists — the lane's own
    # bar reds; no committed-map staleness can hide it from anyone.
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
    # file never enters the inventory, so it cannot be "uncontained".
    _contained_two_module_tree(tmp_path)
    (tmp_path / "scripts" / "helper.sh").write_text("# h\n", encoding="utf-8")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


def test_inventory_skips_hidden_and_pycache(tmp_path):
    # The hidden-part rule (dot-/__pycache__-prefixed parts under the root are
    # not source) holds in the live scan, so caches never red a lane.
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
    # (\xff is an invalid UTF-8 start byte on every platform).
    _contained_two_module_tree(tmp_path)
    (tmp_path / "scripts" / "bin_mod.py").write_bytes(b"\xff\xfe\x00not utf-8")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


# --- WI-502 (OI-53 ruled (d)): Implements-tag vs CodeSymbol crosscheck --------
# The 2026-08-21 closing review's manual method, mechanized: resolve every
# `Implements:` tag's ENCLOSING def/class (gen_arch_map.implements_report, the
# shared AST grammar) and compare it against its row's CodeSymbol/Module by
# CONTAINMENT. WARN-FIRST FOREVER — codesymbol_crosscheck_findings is called
# in-process (no subprocess/CLI), the fast in-process posture the WI asks the
# new tests to keep.


def write_symbol_llrs(root, rows):
    """`rows` = [(llr_id, module_cell, code_symbol_cell)] written as the LLR
    csv carrier `write_tagged_llrs` already uses — same header, Component left
    blank (this crosscheck never joins on it)."""
    req = root / "docs" / "requirements"
    req.mkdir(parents=True, exist_ok=True)
    body = "".join(
        "{},SR-001,T,{},{},d,(see TC),Approved,\n".format(lid, mod, sym)
        for lid, mod, sym in rows
    )
    (req / "low-level-requirements.csv").write_text(
        TAGGED_LLR_HDR + body, encoding="utf-8"
    )


MOD_A_SRC = (
    '"""M."""\n\n\n'
    "class ClassA:\n"
    "    def method_a(self):\n"
    '        """go.\n\n'
    "        Implements: LLR-900, LLR-901\n"
    '        """\n'
    "        return 1\n\n\n"
    "class ClassB:\n"
    "    def method_b(self):\n"
    "        return 2\n"
)


def test_codesymbol_crosscheck_reports_a_planted_mismatch(tmp_path):
    # LLR-900's CodeSymbol names a real class (ClassB) that is NOT where the
    # tag sits (ClassA.method_a) — a genuine, resolvable mismatch, the kit's
    # own WI-501 CodeSymbol-dozen shape.
    write_src_profile(tmp_path, [])
    write_module(tmp_path, "mod_a.py", MOD_A_SRC)
    write_symbol_llrs(tmp_path, [("LLR-900", "scripts/mod_a.py", "ClassB")])
    findings = check_trajectory.codesymbol_crosscheck_findings(tmp_path)
    assert len(findings) == 1, findings
    assert "LLR-900" in findings[0]
    assert "ClassA.method_a" in findings[0]
    assert "ClassB" in findings[0]


def test_codesymbol_crosscheck_containment_case_is_silent(tmp_path):
    # LLR-901's CodeSymbol names the CLASS (ClassA) rather than the full
    # `ClassA.method_a` path — containment (a tag inside `RoutingState.
    # note_session` satisfies a cell naming `RoutingState`) is satisfied, so
    # this is not a finding.
    write_src_profile(tmp_path, [])
    write_module(tmp_path, "mod_a.py", MOD_A_SRC)
    write_symbol_llrs(tmp_path, [("LLR-901", "scripts/mod_a.py", "ClassA")])
    findings = check_trajectory.codesymbol_crosscheck_findings(tmp_path)
    assert findings == []


def test_codesymbol_crosscheck_function_local_name_is_unresolvable(tmp_path):
    # LLR-902's CodeSymbol names `a_local_var` — a real identifier in the
    # file, but a FUNCTION-LOCAL variable, never a def/class or a module-level
    # binding. It must report as unresolvable rather than silently reading as
    # a match (the false-quiet shape docs/enforcement-audit.md item 5 names
    # for a neighboring grammar, that this rule does not inherit).
    write_src_profile(tmp_path, [])
    write_module(
        tmp_path,
        "mod_b.py",
        '"""M.\n\nImplements: LLR-902\n"""\n\n'
        "def helper():\n    a_local_var = 5\n    return a_local_var\n",
    )
    write_symbol_llrs(tmp_path, [("LLR-902", "scripts/mod_b.py", "a_local_var")])
    findings = check_trajectory.codesymbol_crosscheck_findings(tmp_path)
    assert len(findings) == 1, findings
    assert "LLR-902" in findings[0]
    assert "unresolvable" in findings[0]


def test_codesymbol_crosscheck_vacuous_in_files_mode(tmp_path):
    # No AST, no containment question to ask.
    write_src_profile(tmp_path, ["mod_a.py"], mode="files")
    write_symbol_llrs(tmp_path, [("LLR-900", "scripts/mod_a.py", "ClassB")])
    assert check_trajectory.codesymbol_crosscheck_findings(tmp_path) == []


# --- WI-093: the phase-anchor archetype + phase-drop detector ------------------
# The derived-gate model (docs/archive/specs/derived-gate-model.2026-07-20.md
# §7/§9.3): a phase's pre-dev batch is a WI whose Title carries a phase-anchor
# tag; the phase reading BELOW the rung its closed anchor recorded warns to open
# a new phase-anchor WI. RE-KEYED TO THE STAGE AXIS by WI-498 slice 4 — the
# anchor records a LADDER RUNG and the current reading comes from `docs/stage`'s
# `per-phase-live`. All warn-first; the logic is unit-tested via load_script.


def _wis(ct, rows):
    return ct.load_wis(rows)[0]


def test_phase_anchors_parse_and_duplicate_warn():
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [
            {
                "WI-ID": "WI-201",
                "Title": "[v2]-[g1] structure v2 reqs",
                "Status": "done",
            },
            {
                "WI-ID": "WI-202",
                "Title": "[v2]-[g2] decompose v2",
                "Predecessors": "WI-201",
                "Status": "queued",
            },
            {
                "WI-ID": "WI-203",
                "Title": "[v2]-[g2] a duplicate g2",
                "Status": "queued",
            },
            {"WI-ID": "WI-204", "Title": "an ordinary WI", "Status": "queued"},
        ],
    )
    anchors, warns = ct.phase_anchors(wis)
    assert ("v2", "DevStg-LLReqs") in anchors and ("v2", "DevStg-Impl") in anchors
    assert anchors[("v2", "DevStg-Impl")]["id"] == "WI-202"  # first wins
    # The RETIRED `[phase]-[g2]` spelling still PARSES (the ~20 committed anchors
    # carry it and D-4 refuses re-pointing history), but the message names the
    # CANONICAL spelling, because what it is asking for is a NEW row.
    assert any("duplicate phase anchor [v2]-[DevStg-Impl]" in w for w in warns)


def test_the_CANONICAL_anchor_spelling_parses_to_the_same_rungs():
    """Both retired spellings and the canonical one land on ONE rung per level,
    or a phase would carry two independent anchor sets.

    THE TRANSLATION IS BY MEANING AND THE SPELLINGS ARE A TRAP, which is the
    whole reason this is a table and not a string manipulation: `[p]-[reqs]`
    records `DevStg-LLReqs` (the rung the phase stands at once its requirements
    are approved), NOT `DevStg-Reqs` (the rung it has just left), and
    `[p]-[tests]` records `DevStg-Impl`, NOT `DevStg-Tests`. Both are off by two
    rungs from the spelling, in the direction that would make the detector fire
    on healthy phases."""
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [
            {"WI-ID": "WI-301", "Title": "[v9]-[reqs] structure", "Status": "done"},
            {
                "WI-ID": "WI-302",
                "Title": "[v9]-[tests] decompose",
                "Predecessors": "WI-301",
                "Status": "queued",
            },
        ],
    )
    anchors, warns = ct.phase_anchors(wis)
    assert set(anchors) == {("v9", "DevStg-LLReqs"), ("v9", "DevStg-Impl")}
    assert warns == []
    # The canonical form is the rung itself, and it lands on the same keys.
    canonical = _wis(
        ct,
        [
            {
                "WI-ID": "WI-321",
                "Title": "[v9]-[DevStg-LLReqs] structure",
                "Status": "done",
            },
            {
                "WI-ID": "WI-322",
                "Title": "[v9]-[DevStg-Impl] decompose",
                "Predecessors": "WI-321",
                "Status": "queued",
            },
        ],
    )
    canon_anchors, canon_warns = ct.phase_anchors(canonical)
    assert set(canon_anchors) == set(anchors)
    assert canon_warns == []
    # ...and a phase spelled BOTH ways is one anchor set, so the changeover
    # collision is caught rather than silently doubling the phase's anchors.
    mixed = _wis(
        ct,
        [
            {"WI-ID": "WI-311", "Title": "[v9]-[g1] old", "Status": "done"},
            {"WI-ID": "WI-312", "Title": "[v9]-[reqs] new", "Status": "queued"},
        ],
    )
    _, mixed_warns = ct.phase_anchors(mixed)
    assert any("duplicate phase anchor [v9]-[DevStg-LLReqs]" in w for w in mixed_warns)


def test_a_phase_anchor_naming_no_rung_at_all_warns_rather_than_parsing():
    """The canonical form admits any `DevStg-*` token, so the token set is no
    longer closed by the regex — a title naming a rung this ladder does not have
    must be REFUSED loudly, not folded into some neighbour."""
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [{"WI-ID": "WI-331", "Title": "[v9]-[DevStg-Nonsense] x", "Status": "done"}],
    )
    anchors, warns = ct.phase_anchors(wis)
    assert anchors == {}
    assert any("is not a rung on the stage ladder" in w for w in warns)


def test_phase_anchor_higher_rung_without_lower_predecessor_warns():
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [
            {"WI-ID": "WI-201", "Title": "[v3]-[g1] x", "Status": "done"},
            {"WI-ID": "WI-202", "Title": "[v3]-[g2] y", "Status": "queued"},  # no pred
        ],
    )
    _, warns = ct.phase_anchors(wis)
    assert any("does not list its [v3]-[DevStg-LLReqs]" in w for w in warns)


def _write_stage(root, per_phase_live, stage="DevStg-Impl"):
    """A `docs/stage` carrying `per_phase_live`, written through the REAL
    renderer so the fixture cannot drift from the parser."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    record = {
        "stage": stage,
        "stage-ord": kitstage.order(stage),
        "stage-of": 8,
        "floored": False,
        "settled-stage": stage,
        "live-stage": stage,
        "phase": 1,
        "per-phase": dict(per_phase_live),
        "per-phase-live": dict(per_phase_live),
        "drafted": 0,
        "fingerprint": "sha256:" + "0" * 64,
    }
    (root / "docs" / "stage").write_text(
        kitstage.render(record, "abc1234", "2026-08-21"),
        encoding="utf-8",
        newline="\n",
    )


def _pin_reader(monkeypatch, root):
    """Short-circuit the common reader to the RECORDED values of the fixture.

    The detector reads through `derive_stage.read`, which recomputes the
    fingerprint over the declared inputs and derives fresh on a miss — correct in
    production and useless for a fixture that wants to state a per-phase reading
    directly. Patching that ONE call is the seam; the file format, the parse and
    the comparison are all real."""
    derive_stage = load_script("derive_stage")
    text = (root / "docs" / "stage").read_text(encoding="utf-8")
    monkeypatch.setitem(sys.modules, "derive_stage", derive_stage)
    monkeypatch.setattr(derive_stage, "read", lambda _root: kitstage.parse(text))


def test_phase_drop_detector_warns(tmp_path, monkeypatch):
    ct = load_script("check_trajectory")
    # v2 closed at [g2] (recorded reach DevStg-Impl) but v2 now reads
    # DevStg-Tests — a TC went back to Drafted, i.e. reopened content.
    _write_stage(tmp_path, {"v1": "DevStg-Impl", "v2": "DevStg-Tests"})
    _pin_reader(monkeypatch, tmp_path)
    wis = _wis(
        ct,
        [
            {"WI-ID": "WI-210", "Title": "[v2]-[g1] x", "Status": "done"},
            {
                "WI-ID": "WI-211",
                "Title": "[v2]-[g2] y",
                "Predecessors": "WI-210",
                "Status": "done",
            },
        ],
    )
    warns = ct.phase_findings(tmp_path, wis)
    assert any(
        "phase 'v2' dropped to DevStg-Tests" in w and "[v2]-[DevStg-Impl]" in w
        for w in warns
    ), warns
    # Back at DevStg-Impl: no drop warn (the phase re-earned its anchor's reach).
    _write_stage(tmp_path, {"v1": "DevStg-Impl", "v2": "DevStg-Impl"})
    _pin_reader(monkeypatch, tmp_path)
    assert ct.phase_findings(tmp_path, wis) == []


def test_phase_findings_vacuous_without_anchors(tmp_path, monkeypatch):
    ct = load_script("check_trajectory")
    # a phase below every rung but NO anchor records a close
    _write_stage(tmp_path, {"v1": "DevStg-Below"})
    _pin_reader(monkeypatch, tmp_path)
    wis = _wis(ct, [{"WI-ID": "WI-220", "Title": "ordinary", "Status": "queued"}])
    assert ct.phase_findings(tmp_path, wis) == []


# --- WI-146(b): the approval-brief hierarchy-view lint --------------------
# An open-items ROW whose decision is a `[phase]-[g1|g2]` approval should
# name the generated batch-scoped hierarchy view rather than hand-copy rows.
# Warn-first (never a gate fail); vacuous without such a brief. WI-322 moved the
# briefs from markdown sections into `docs/requirements/open-items.csv`, so the
# lint reads rows and the evidence it accepts is a view PATH in the cell.

_OI_HEADER = (
    "OI-ID,Title,Status,Raised,OneLine,Decision,BlastRadius,Options,"
    "Recommendation,WI-Refs,RuledDate,RulingRef\n"
)


def _write_open_items(root, rows):
    (root / "docs" / "requirements").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "requirements" / "open-items.csv").write_text(
        _OI_HEADER + rows, encoding="utf-8"
    )
    return root


def _oi_row(oid, decision, title="a decision", status="pending"):
    return '{},{},{},,,"{}",,,,,,\n'.format(oid, title, status, decision)


def test_approval_brief_without_view_warns(tmp_path):
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        _oi_row("OI-20", "approve the [v3]-[g2] dashboard batch.")
        + _oi_row("OI-21", "something else, no anchor here."),
    )
    warns = ct.approval_brief_findings(tmp_path)
    # Exactly the approval brief warns; the unrelated row does not.
    assert len(warns) == 1
    assert warns[0].startswith("OI-20:")
    assert "hierarchy view" in warns[0]


def test_approval_brief_with_generator_command_only_warns(tmp_path):
    # A bare `trace.py --approve` command mention is NOT proof the view exists and
    # is carried — the brief must name the generated view (WI-146 REVIEW-A).
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        _oi_row(
            "OI-20",
            "approve the [v3]-[g2] batch. Hierarchy: run trace.py --approve v3.",
        ),
    )
    warns = ct.approval_brief_findings(tmp_path)
    assert len(warns) == 1 and warns[0].startswith("OI-20:")


def test_approval_brief_with_view_link_is_silent(tmp_path):
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        _oi_row(
            "OI-20", "approve the [v3]-[g2] batch. See the tree: docs/ratify/v3-g2.md."
        ),
    )
    assert ct.approval_brief_findings(tmp_path) == []


def test_approval_brief_lint_is_vacuous_off_the_pending_queue(tmp_path):
    ct = load_script("check_trajectory")
    # No registry at all -> nothing to check.
    assert ct.approval_brief_findings(tmp_path) == []
    # An approval word with no [phase]-[g*] anchor -> not a brief.
    _write_open_items(tmp_path, _oi_row("OI-30", "whether to approve a policy change."))
    assert ct.approval_brief_findings(tmp_path) == []
    # ...an anchor with no approval language -> also not a brief.
    _write_open_items(tmp_path, _oi_row("OI-31", "sequence [v3]-[g2] after v2 work."))
    assert ct.approval_brief_findings(tmp_path) == []
    # ...and a RULED row is history, not a pending decision, so it never warns
    # even when it carries both (the negative half WI-322 added).
    _write_open_items(
        tmp_path,
        _oi_row("OI-32", "approve the [v3]-[g2] batch.", status="ruled"),
    )
    assert ct.approval_brief_findings(tmp_path) == []


# --- WI-064: the cross-CMP-edge-without-IF rule ---------------------------------
# An internal import edge between two DIFFERENT components with no covering
# IF-### row is a finding (the AXES approved model's enforceability ruling) —
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
        "TC-001,SR-001;{},Integration,seam,Full,,ok,Yes,tests/x.py,Approved\n".format(
            if_id
        ),
        encoding="utf-8",
    )


def test_cross_cmp_import_with_declared_seam_is_silent(tmp_path):
    _cross_cmp_repo(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Consumes,scripts/mod_a,scripts/mod_b,"call",SR-001,v1,Stable,Active,,\n',
    )
    _write_tc_citing(tmp_path, "IF-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_cross_cmp_seam_covers_either_direction(tmp_path):
    # The seam row authored from mod_b's side (b -> a) still covers the a -> b
    # import edge — a seam is one declared relationship, not a directed pair.
    _cross_cmp_repo(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Provides,scripts/mod_b,scripts/mod_a,"call",SR-001,v1,Stable,Active,,\n',
    )
    _write_tc_citing(tmp_path, "IF-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_intra_cmp_import_is_silent(tmp_path):
    # Both endpoints in CMP-001: internal wiring, never a finding.
    _cross_cmp_repo(tmp_path, cmp_b="CMP-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


def test_cross_cmp_unmapped_endpoint_is_vacuous(tmp_path):
    # mod_b has no Component membership: coverage is the containment rule's job,
    # so the cross-CMP rule stays silent rather than double-reporting.
    write_arch(tmp_path, ARCH_2MOD_IMPORT)
    write_cmps(tmp_path, TWO_CMPS)
    write_tagged_llrs(tmp_path, [("scripts/mod_a", "CMP-001")])
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


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
    _cross_cmp_repo(tmp_path)
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "cross-component import" not in proc.stderr


# --- WI-440: the multi-membership overlap ADVISORY (OI-14's third do-not-wait) --
# The old guard skipped an edge whose endpoint component sets merely OVERLAPPED,
# so tagging a module into MORE components monotonically SILENCED the rule — a
# fail-open the author controls. The overlap now REPORTS instead of suppressing:
# warn-only, never the exit code (the partition it questions has not been ruled),
# and the hard finding's semantics are untouched.

ADVISORY = "suppress the cross-component seam rule on import"


def _overlap_repo(tmp_path):
    """mod_a is tagged into BOTH CMP-001 and CMP-002; mod_b only CMP-002 — so
    the sets overlap on CMP-002 and the old guard skipped the a -> b edge."""
    write_arch(tmp_path, ARCH_2MOD_IMPORT)
    write_cmps(tmp_path, TWO_CMPS)
    write_tagged_llrs(
        tmp_path,
        [
            ("scripts/mod_a", "CMP-001"),
            ("scripts/mod_a", "CMP-002"),
            ("scripts/mod_b", "CMP-002"),
        ],
    )


def test_multi_membership_overlap_advises_instead_of_silencing(tmp_path):
    _overlap_repo(tmp_path)
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert ADVISORY in plain.stderr
    # It NAMES the multi-tagged module and the edge, so the partition work can
    # consume the list.
    assert "multi-component module(s) scripts/mod_a" in plain.stderr
    assert "scripts/mod_a (CMP-001/CMP-002) -> scripts/mod_b (CMP-002)" in plain.stderr
    # ...and it is NOT the hard finding: no seam error, and the message says so.
    assert "has no declared IF-### seam" not in plain.stderr
    assert "advisory only" in plain.stderr


def test_overlap_advisory_never_reaches_the_exit_code(tmp_path):
    # WARN-ONLY even under --strict, where the sibling FINDING is an error.
    _overlap_repo(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADVISORY in strict.stderr


def test_overlap_advisory_yields_to_a_declared_seam(tmp_path):
    # A declared IF row covering the pair means nothing was silenced BY the
    # overlap — the seam is declared, so there is no partition question to raise.
    _overlap_repo(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Consumes,scripts/mod_a,scripts/mod_b,"call",SR-001,v1,Stable,Active,,\n',
    )
    _write_tc_citing(tmp_path, "IF-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert ADVISORY not in proc.stderr


def test_single_tagged_same_component_edge_raises_nothing(tmp_path):
    # Both endpoints single-tagged into CMP-001: ordinary intra-component
    # wiring, neither a finding nor an advisory. The advisory is about
    # MULTI-membership, not about overlap as such.
    _cross_cmp_repo(tmp_path, cmp_b="CMP-001")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert ADVISORY not in proc.stderr


def test_disjoint_uncovered_edge_is_still_a_hard_finding(tmp_path):
    # The scope guard: the FINDING's semantics are exactly as they were —
    # disjoint sets, no covering IF row, WARN plain and ERROR under --strict —
    # and it does not double-report as an advisory.
    _cross_cmp_repo(tmp_path)
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert (
        "cross-component import scripts/mod_a (CMP-001) -> scripts/mod_b "
        "(CMP-002) has no declared IF-### seam" in plain.stderr
    )
    assert ADVISORY not in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADVISORY not in strict.stderr


def test_untagged_endpoint_stays_vacuous_for_the_advisory_too(tmp_path):
    # The deliberate vacuousness the docstring documents (containment rule's
    # job) survives: mod_b has no Component tag, so mod_a's DOUBLE tag raises
    # nothing here — an untagged endpoint is not a partition finding.
    write_arch(tmp_path, ARCH_2MOD_IMPORT)
    write_cmps(tmp_path, TWO_CMPS)
    write_tagged_llrs(
        tmp_path, [("scripts/mod_a", "CMP-001"), ("scripts/mod_a", "CMP-002")]
    )
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert ADVISORY not in proc.stderr
    assert "cross-component import" not in proc.stderr


def test_components_check_off_silences_the_overlap_advisory(tmp_path):
    # It shares the component layer's opt-out — an adopter who turned the layer
    # off does not get half of it back.
    _overlap_repo(tmp_path)
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert ADVISORY not in proc.stderr


# --- OI-48 (d): the declared shared-kernel exemption (WI-494) -----------------
# `docs/kernel-modules-allow` — an import edge whose DESTINATION is listed there
# is not a seam at all (neither the hard finding nor the multi-membership
# advisory). Fail-safe by construction: absence of a valid declaration grants
# no exemption, so a module not listed (or listed with a malformed entry) stays
# fully policed.


def write_kernel_allow(root, body):
    (root / "docs" / "kernel-modules-allow").write_text(body, encoding="utf-8")


def test_declared_kernel_destination_is_not_a_seam(tmp_path):
    # mod_a (CMP-001) imports mod_b (CMP-002); mod_b is declared kernel — no
    # finding, no advisory, clean even under --strict.
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(tmp_path, "scripts/mod_b — WI-494 test: shared reader.\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert "cross-component import" not in strict.stderr
    assert ADVISORY not in strict.stderr


def test_undeclared_module_still_fires_the_hard_finding(tmp_path):
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
    # No file at all: read_kernel_modules answers {} and the ordinary rule
    # runs exactly as it did before OI-48 — the fail-safe default.
    _cross_cmp_repo(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "cross-component import" in strict.stderr


def test_kernel_exemption_also_silences_the_overlap_advisory(tmp_path):
    # A declared kernel module that still carries a residual multi-tag is not
    # ALSO advised about: the advisory exists to surface undeclared
    # candidates, and a declared one is a settled candidate, not an open one.
    _overlap_repo(tmp_path)  # mod_a tagged CMP-001+CMP-002, mod_b tagged CMP-002
    write_kernel_allow(tmp_path, "scripts/mod_b — WI-494 test: declared kernel.\n")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert ADVISORY not in plain.stderr


def test_kernel_exemption_is_one_directional(tmp_path):
    # Declaring mod_a (the SOURCE) kernel does not exempt ITS OWN outbound
    # edge — the exemption keys on the destination only.
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(tmp_path, "scripts/mod_a — WI-494 test: wrong side.\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert "cross-component import" in strict.stderr


def test_kernel_allow_entry_without_a_reason_is_dropped_and_reported(tmp_path):
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
    # A separator present but nothing after it — same fail-safe: dropped,
    # reported, no exemption.
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(tmp_path, "scripts/mod_b — \n")
    plain = run_traj(tmp_path)
    assert "cross-component import" in plain.stderr
    assert "grammar cannot read it" in plain.stderr


def test_kernel_allow_hygiene_shares_the_components_check_opt_out(tmp_path):
    _cross_cmp_repo(tmp_path)
    write_kernel_allow(tmp_path, "scripts/mod_b\n")  # malformed, no reason
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "grammar cannot read it" not in proc.stderr


# --- specs act on declared interface boundaries (WI-191) ----------------------

# Two declared seams for the spec-citation checks.
SPEC_IFS_ONE = (
    'IF-001,Consumes,scripts/mod_a,docs/stack.ini,"reads",SR-001,v1,approved,Stable,,\n'
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
    _spec_repo(tmp_path, "WI-001.md", "# WI-001\n\n## Approach\n\nNo section.\n")
    proc = run_traj(tmp_path)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "Interfaces" not in proc.stderr  # no `## Interfaces` -> not armed


def test_spec_interfaces_resolvable_passes(tmp_path):
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
    silently becomes "not yet approved", which on a repo that approves nothing
    before its sitting arms 100% of rows instead of ~4%, at a severity that
    ERRORS under --strict.

    So a bare citation of a `draft` seam is CLEAN, and the resolution arm below
    it still bites. If sitting 3 wants the forced search back, it needs a value
    that means "proposed" — a vocabulary decision, not a checker's to invent."""
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
