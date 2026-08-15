"""check_trajectory.py — decision over architecture inputs (WI-277: split
verbatim from tests/test_trajectory.py by behavior boundary).

Interface-connectivity coverage (WI-056), the How-SW top-view right-sizing
bound (WI-073/FB5), knowledge⇒component coupling (WI-153), the [phase]-[g*]
anchors + phase-drop detector (WI-093), the ratification-brief hierarchy-view
lint (WI-146b), cross-CMP edges without a declared IF (WI-064), and specs
acting on declared interface boundaries (WI-191).
"""

import csv
import shutil


from conftest import SCRIPTS, load_script, run_py

wi_convert = load_script("wi_convert")


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
    "IF-ID,Direction,ThisProject,Counterpart,Contract,SR-Refs,Version,"
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
# `Status` is DROPPED here, since it retired with the ruling: a body that set
# `Status=Proposed` is translated to `approval = "draft"`, which is the rung
# that value became once WI-442 replaced `Stability` with `Approval`.
def _csv_body_to_toml(header, table, body):
    import csv as _csv
    import io as _io

    keys = {
        "Direction": "direction",
        "ThisProject": "this_project",
        "Counterpart": "counterpart",
        "Contract": "contract",
        "SR-Refs": "sr_refs",
        "Version": "version",
        "Stability": "approval",
        "Component": "component",
        "Notes": "notes",
        "Name": "name",
        "Category": "category",
        "Knowledge": "knowledge",
        "State": "state",
        "SupersededBy": "superseded_by",
        "PartOf": "part_of",
        "DetailDoc": "detail_doc",
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
        if not (row.get("Stability") or "").strip():
            row["Stability"] = (
                "draft"
                if (row.get("Status") or "").strip().lower() == "proposed"
                else "approved"
            )
        out.append("[{}.{}]".format(table, rid))
        if table == "interface":
            out.append('signal = "discrete"')
        for col, key in keys.items():
            value = (row.get(col) or "").strip()
            if not value:
                continue
            if key in ("sr_refs", "superseded_by", "part_of"):
                items = ", ".join('"{}"'.format(t) for t in value.split(";") if t)
                out.append("{} = [{}]".format(key, items))
            else:
                out.append('{} = """{}"""'.format(key, value))
        out.append("")
    return "\n".join(out) + "\n"


def write_arch(root, text):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "architecture.md").write_text(text, encoding="utf-8")


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
        "TC-001,SR-001;IF-001,Integration,seam,Full,,ok,Yes,tests/x.py,Verified\n",
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
    assert "no script declares it via a Contracts" in proc.stderr


def test_interface_warns_never_fail_strict(tmp_path):
    # Even under --strict, the connectivity warns never change the exit code
    # (they are warns, not the R-B..R-E coherence rules --strict promotes). With
    # no work-items registry the run is vacuously clean once the warns are printed.
    write_arch(tmp_path, ARCH_2MOD)
    proc = run_traj(tmp_path, "--strict")
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "connectivity undeclared" in proc.stderr


# --- WI-073/FB5: the How-SW top-view right-sizing rule -------------------------
# The software-architecture top view is bounded at 10 items (top-level CMP
# components that contain a module + uncontained modules); over the bound is a
# finding — WARN plain, ERROR under --strict (DevBar-Tests+). Opt-out docs/components-check;
# vacuous below the bound or with no arch-map inventory (the bound is the rule).

CMP_HDR = "CMP-ID,Name,Category,Knowledge,State,SupersededBy,PartOf,DetailDoc,Notes\n"
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
        "LLR-{:03d},SR-001,T,{},f,d,(see TC),Verified,{}\n".format(i + 1, mod, cmp)
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
    # No architecture.md at all -> nothing to bound (pre-arch-map / files-mode).
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


# --- WI-399: containment owed where a module is ADDED --------------------------
# docs/architecture.md is trunk-owned, so its freshness gate SKIPs on a claimed
# work branch (SR-006) and a module a branch adds enters the committed arch-map
# inventory only when the trunk lane's refresh regenerates it — AFTER the last
# review round, which made the station the FIRST place the knowledge⇒component
# red could exist (WI-374/drive.py, WI-387/handback.py). The same rule now also
# fires in the lane's own bar on the ADDED modules: shipped source files on disk
# under the declared arch-map scan root that the committed inventory lacks. Same
# pack arming, same components-check opt-out, same WARN-plain/ERROR-strict tier;
# the station's own rule is untouched (the backstop).

ADDED_MSG = "not yet in the committed arch-map"

# A module body gen_arch_map WOULD inventory (docstring summary + a public
# symbol). The fixtures must ship real-symbol modules: build_map SKIPS
# symbol-empty files (bare __init__.py, comment-only, private-only) from the
# MODULE MAP, and the lane delta mirrors that skip (REVIEW-A finding 1), so an
# empty body could never red anything on either side.
MODULE_BODY = '"""M."""\n\n\ndef run():\n    """go"""\n'


def write_module(root, name, text=MODULE_BODY, src="scripts"):
    d = root / src
    d.mkdir(parents=True, exist_ok=True)
    (d / name).write_text(text, encoding="utf-8")


def write_arch_src(root, files, src="scripts", mode=None):
    """Write docs/stack.ini declaring the arch-map scan root (+ optional mode)
    and the shipped module files on disk under it — the lane-visible set. `.py`
    files get a real inventoried body (MODULE_BODY), anything else a comment."""
    (root / "docs").mkdir(parents=True, exist_ok=True)
    ini = "[paths]\nsrc = {}\n".format(src)
    if mode:
        ini += "\n[arch-map]\nmode = {}\n".format(mode)
    (root / "docs" / "stack.ini").write_text(ini, encoding="utf-8")
    for name in files:
        write_module(root, name, MODULE_BODY if name.endswith(".py") else "# m\n", src)


def regen_map(root, src="scripts", mode=None):
    """Run the REAL gen_arch_map over the fixture tree — the differential pin
    (REVIEW-A finding 1): the lane delta must be empty exactly when the
    regenerated map absorbs a module, so the mirror of build_map's
    symbol-emptiness skip cannot drift without a red here."""
    cmd = [SCRIPTS / "gen_arch_map.py", "--src", src, "--doc", "docs/architecture.md"]
    if mode:
        cmd += ["--mode", mode]
    proc = run_py(cmd, cwd=root)
    assert proc.returncode == 0, proc.stdout + proc.stderr


def _contained_two_module_tree(tmp_path, src="scripts"):
    """A pack-armed tree whose committed 2-module arch-map is fully contained —
    clean under the station rule — with the map's modules also on disk."""
    write_arch(tmp_path, _arch_n(2))
    write_pack(tmp_path, "prompt-image")
    write_cmps(tmp_path, "CMP-001,Core,software,,built,,,,\n")
    write_tagged_llrs(
        tmp_path, [("scripts/mod_0", "CMP-001"), ("scripts/mod_1", "CMP-001")]
    )
    write_arch_src(tmp_path, ["mod_0.py", "mod_1.py"], src=src)


def test_added_module_without_component_tag_reds_the_lane_bar(tmp_path):
    # The wi-387 topology, the class this row closes: the committed arch-map is
    # STALE (trunk-vintage — no regeneration on a work branch) and clean under
    # the station rule, yet the tree ships a new module with no Component tag.
    # The lane bar itself reds, so the station can never be the first to know.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "mod_new.py")
    plain = run_traj(tmp_path)
    assert plain.returncode == 0, plain.stdout + plain.stderr
    assert ADDED_MSG in plain.stderr
    assert "scripts/mod_new" in plain.stderr
    # The station rule has nothing to say here (the stale map IS contained) —
    # only the early firing point sees the red. That is the station-first shape.
    assert KN_MSG not in plain.stderr
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr
    assert "1 shipped module(s)" in strict.stderr


def test_added_module_greens_when_the_component_tag_lands(tmp_path):
    # The two-registry-row remedy (an LLR Component cell) clears the finding in
    # the same tree — no arch-map regeneration required.
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
    assert ADDED_MSG not in proc.stderr


def test_fresh_map_module_is_the_station_rules_not_the_deltas(tmp_path):
    # A module IN the committed map but untagged is the existing rule's finding;
    # the added-module firing point must not double-report it (the delta is
    # exactly the modules the map lacks).
    write_arch(tmp_path, _arch_n(3))
    write_pack(tmp_path, "prompt-image")
    write_cmps(tmp_path, "CMP-001,Core,software,,built,,,,\n")
    write_tagged_llrs(
        tmp_path, [("scripts/mod_0", "CMP-001"), ("scripts/mod_1", "CMP-001")]
    )
    write_arch_src(tmp_path, ["mod_0.py", "mod_1.py", "mod_2.py"])
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert KN_MSG in strict.stderr
    assert ADDED_MSG not in strict.stderr


def test_added_module_check_shares_the_pack_arming(tmp_path):
    # No pack -> dormant at the early firing point too: this row moves WHERE the
    # containment rule fires, never WHEN it arms (no new policy).
    write_arch(tmp_path, _arch_n(2))
    write_arch_src(tmp_path, ["mod_0.py", "mod_1.py", "mod_new.py"])
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADDED_MSG not in strict.stderr


def test_added_module_check_respects_components_check_off(tmp_path):
    # The one opt-out silences the early firing point exactly as it does the
    # station rule (shared switch, shared policy).
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "mod_new.py")
    (tmp_path / "docs" / "components-check").write_text("off\n", encoding="utf-8")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADDED_MSG not in strict.stderr


def test_added_module_check_needs_an_arch_map_inventory(tmp_path):
    # A pack + shipped modules but NO committed arch-map -> dormant, exactly as
    # the station rule is (a pre-arch-map repo is not punished for adopting it
    # late; the arming is shared, not new).
    write_pack(tmp_path, "prompt-image")
    write_arch_src(tmp_path, ["mod_new.py"])
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADDED_MSG not in strict.stderr


def test_added_module_delta_symbols_mode_sees_only_python(tmp_path):
    # Default symbols mode scans `*.py` exactly as gen_arch_map does: a .sh file
    # the regeneration would never inventory must not red the lane either — the
    # delta mirrors what the refresh WOULD add, no more.
    _contained_two_module_tree(tmp_path)
    (tmp_path / "scripts" / "helper.sh").write_text("# h\n", encoding="utf-8")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADDED_MSG not in strict.stderr


def test_files_mode_real_map_keeps_the_whole_family_dormant(tmp_path):
    # REVIEW-A finding 2, the honest claim: a REAL files-mode map (gen_arch_map
    # --mode files) is a table with no `### ` module headers, so arch_inventory
    # reads it as EMPTY and the whole containment family is dormant there —
    # station rule and early firing point alike. Parity, no lane-only hole: the
    # lane must NOT invent a delta the regeneration could never absorb.
    write_arch(tmp_path, _arch_n(0))  # just the marker pair
    write_pack(tmp_path, "prompt-image")
    write_arch_src(tmp_path, ["mod_0.py", "helper.sh"], mode="files")
    regen_map(tmp_path, mode="files")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADDED_MSG not in strict.stderr
    assert KN_MSG not in strict.stderr


def test_added_module_delta_skips_hidden_and_pycache(tmp_path):
    # The scan mirrors gen_arch_map's hidden-part rule (dot- and __pycache__-
    # prefixed parts under the root are not source), so caches never red a lane
    # — pinned with REAL module bodies, so the skip is the hidden rule, not the
    # symbol-emptiness mirror.
    _contained_two_module_tree(tmp_path)
    for sub in ("__pycache__", ".vendored"):
        write_module(tmp_path, "mod_cache.py", src="scripts/" + sub)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADDED_MSG not in strict.stderr


def test_differential_delta_empties_exactly_when_the_regen_absorbs(tmp_path):
    # REVIEW-A finding 1's pin, the wi-387 lifecycle against the REAL
    # generator: the lane reds on the added public-symbol module BEFORE any
    # regeneration; the real gen_arch_map run absorbs it and the delta empties
    # (ADDED_MSG gone) with the station rule now holding the same red — the
    # backstop equivalence — and the Component tag clears both.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "mod_new.py")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr and "scripts/mod_new" in strict.stderr
    regen_map(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG not in strict.stderr  # the delta emptied on absorption
    assert KN_MSG in strict.stderr  # the station rule holds the same red
    write_tagged_llrs(
        tmp_path,
        [
            ("scripts/mod_0", "CMP-001"),
            ("scripts/mod_1", "CMP-001"),
            ("scripts/mod_new", "CMP-001"),
        ],
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


def test_symbol_empty_module_reds_neither_side_of_the_regen(tmp_path):
    # REVIEW-A finding 1, the class: build_map SKIPS symbol-empty modules
    # (bare __init__.py, comment-only, private-only), so the regeneration can
    # never absorb one — a lane red on it would be PERMANENT (still red after
    # regen, forever), which is new policy by accident. The mirror must skip
    # exactly what the generator skips: green in the lane AND green after the
    # real regen (the differential, both sides).
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "__init__.py", "", src="scripts/pkg")
    write_module(tmp_path, "notes.py", "# comment-only, no symbols\n")
    write_module(tmp_path, "priv.py", "def _hidden():\n    pass\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADDED_MSG not in strict.stderr
    regen_map(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADDED_MSG not in strict.stderr


def test_absolute_declared_src_scans_like_the_generator(tmp_path):
    # REVIEW-A finding 3: an absolute [paths] src must scan the directory the
    # generator would (gen_arch_map treats --src as a path, absolute or not),
    # not remap to a silent repo-relative miss.
    _contained_two_module_tree(tmp_path, src=str(tmp_path / "scripts"))
    write_module(tmp_path, "mod_new.py")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr
    assert "scripts/mod_new" in strict.stderr


# --- WI-406: the unpinned mirror arms, pinned (REVIEW-A round-2 finding 4) -----
# The finding-1 differential fixtures above drive only the arms they contain
# (public-symbol, bare __init__, comment-only, private-only, hidden-skip,
# absolute src); the import-only, contracts-comment-only and parse-error arms of
# _would_be_inventoried were consistent with the generator but UNPINNED — an
# edit to either side of the mirror could drift them without a red. Each fixture
# below drives one arm through the full differential: the lane reds on the
# untagged module BEFORE any regeneration (the mirror KEEPS it), the REAL
# gen_arch_map run absorbs it and the delta empties (the generator keeps it
# too — a mirror-only keep would leave ADDED_MSG as a permanent red here) with
# the station rule holding the same red, and the Component tag clears both.


def _tag_three(tmp_path, third):
    write_tagged_llrs(
        tmp_path,
        [
            ("scripts/mod_0", "CMP-001"),
            ("scripts/mod_1", "CMP-001"),
            (third, "CMP-001"),
        ],
    )


def test_reexporting_init_is_inventoried_on_both_sides_of_the_regen(tmp_path):
    # The import-only arm, in its most common downstream shape: a re-exporting
    # __init__.py whose ONLY content is a relative import of a sibling.
    # internal_imports keeps it (node.level), so _has_internal_import must too,
    # under the same /__init__-stripped key (scripts/pkg) _norm_module and
    # scan_module share. `from . import notes` (module=None) isolates the
    # node.level arm — `from .notes import x` would survive losing it via the
    # absolute-segment-in-names arm, since the sibling's stem is in the names
    # universe (watched: that mutation stayed green until this shape). The
    # comment-only sibling pins the flip side in the same tree: the
    # symbol-emptiness skip holds inside a package too, on both sides.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "__init__.py", "from . import notes\n", src="scripts/pkg")
    write_module(tmp_path, "notes.py", "# comment-only sibling\n", src="scripts/pkg")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr and "scripts/pkg" in strict.stderr
    assert "1 shipped module(s)" in strict.stderr  # the sibling is not a delta
    assert "scripts/pkg/notes" not in strict.stderr
    regen_map(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG not in strict.stderr  # the real generator absorbed the key
    assert KN_MSG in strict.stderr  # the station rule holds the same red
    _tag_three(tmp_path, "scripts/pkg")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


def test_contracts_comment_only_module_is_inventoried_on_both_sides(tmp_path):
    # The contracts-comment arm: a module whose only content is a first-8-lines
    # `# Contracts: IF-###` comment. module_contracts keeps it (CONTRACTS_RE on
    # comment lines), so the mirror's first-8-lines arm must too.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "seam.py", "# Contracts: IF-001\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr and "scripts/seam" in strict.stderr
    regen_map(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG not in strict.stderr
    assert KN_MSG in strict.stderr
    _tag_three(tmp_path, "scripts/seam")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


def test_parse_error_module_stays_inventoried_on_both_sides(tmp_path):
    # The parse-error arm: a syntax-broken module is KEPT by the generator
    # (rendered as a PARSE ERROR summary, rc still 0 without --strict-parse —
    # regen_map's rc==0 assert pins that half), so the mirror's SyntaxError ->
    # True arm must red the lane rather than skip: a skip here would let a
    # broken shipped file dodge containment until the trunk refresh.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "broken.py", "def broken(:\n    pass\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr and "scripts/broken" in strict.stderr
    regen_map(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG not in strict.stderr  # the PARSE ERROR entry absorbed it
    assert KN_MSG in strict.stderr
    _tag_three(tmp_path, "scripts/broken")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


# --- WI-410: the absolute-import arms, pinned (WI-406 REVIEW-A finding 1) ------
# The WI-406 fixtures above never drive _has_internal_import's ABSOLUTE arms:
# reducing the ImportFrom test to `if node.level:` and deleting the whole
# ast.Import branch left all 60 tests green, so an absolute-import-ONLY module
# could drift mirror-side without a red — the wi-387 station-first topology
# back, for exactly that shape. The two arms are disjoint syntactic branches
# (one import statement trips exactly one), so no single module can pin both:
# the fixture tree ships BOTH flat-layout shapes as separately driftable
# modules, and dropping EITHER arm alone drops exactly its module from the
# delta and reds this one test on the name assert (watched: each single-arm
# scratch mutation reds this fixture and nothing else; the review's
# both-dropped probe empties the delta and reds it on the rc assert).


def test_absolute_import_only_modules_are_inventoried_on_both_sides(tmp_path):
    # No relative form anywhere and no other inventoried content (docstring,
    # public symbol, Contracts comment): each module's ONLY internal reference
    # is one absolute import, so only an absolute arm can keep it. The names
    # universe BOTH sides build is module stems + package directory parts —
    # the scan root's own name (`scripts`) is in NEITHER, so the flat stem
    # (`mod_0`) is the internal shape; `from scripts import mod_0` would be
    # external on both sides alike.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "abs_imp.py", "import mod_0\n")
    write_module(tmp_path, "abs_from.py", "from mod_0 import run\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr
    assert "scripts/abs_imp" in strict.stderr  # the ast.Import arm keeps it
    assert "scripts/abs_from" in strict.stderr  # the names-membership arm keeps it
    assert "2 shipped module(s)" in strict.stderr
    regen_map(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG not in strict.stderr  # the real generator absorbed both
    assert KN_MSG in strict.stderr  # the station rule holds the same red
    write_tagged_llrs(
        tmp_path,
        [
            ("scripts/mod_0", "CMP-001"),
            ("scripts/mod_1", "CMP-001"),
            ("scripts/abs_imp", "CMP-001"),
            ("scripts/abs_from", "CMP-001"),
        ],
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


# --- WI-411: the dotted-absolute first segment, pinned (WI-410 REVIEW-A f.1) ---
# The WI-410 modules above pin the two absolute ARMS, but their flat stems are
# whole names IN the names universe, so dropping the `.split(".")[0]`
# first-segment read inside either arm (whole-name membership) left all 61
# tests green: a module whose ONLY internal reference is a DOTTED absolute
# import — first segment a scanned package directory, the whole dotted name in
# the universe on NEITHER side — could drift mirror-side station-first, the
# WI-406-finding-1 way. The WI-410 lesson holds one grain finer: the arms are
# disjoint syntactic branches, so each arm's split must be dropped against its
# own one-form module — two dotted modules, and dropping EITHER split alone
# drops exactly its module from the delta and reds this one test on the name
# assert (watched: each single-split scratch mutation reds this fixture and
# nothing else; the review's both-dropped probe empties the delta and reds it
# on the rc assert). REVIEW-A drove two corrections, folded in below. (1) The
# docstring and public-symbol arms were MASKED, not pinned: MODULE_BODY
# satisfies both at once, so dropping either alone left the whole suite green
# — a docstring-ONLY and a public-symbol-ONLY module pin the pair (watched:
# each single-arm drop reds exactly its fixture, on the rc assert — the
# mutated mirror empties that tree's one-module delta). (2) The honest
# terminus: every arm of _would_be_inventoried (parse-error keep, docstring,
# public symbol, internal import, Contracts comment, symbol-empty skip) and
# of _has_internal_import (relative node.level, absolute ImportFrom
# membership, ast.Import membership, the first-segment read inside both) is
# fixture-pinned EXCEPT the read-failure branch (OSError/UnicodeDecodeError
# -> False), which the green-green differential cannot drive: gen_arch_map
# itself CRASHES on a non-UTF-8 .py (probed: UnicodeDecodeError in
# scan_module's read_text, rc 1), so there is no absorb side to run. Its
# UnicodeDecodeError half is pinned LANE-SIDE only below; the OSError half
# (an unreadable file — not stageable portably) stays the argued exception.
# That is the pinning series' recorded terminus, with the one named residue.


def test_dotted_absolute_import_modules_are_inventoried_on_both_sides(tmp_path):
    # The comment-only pkg/notes.py is the names-universe donor: both sides
    # collect stems + package directory parts from every scanned file BEFORE
    # the symbol-emptiness filter, so it contributes `pkg` and `notes` while
    # never itself entering the delta or the map. `pkg.notes` as a whole is in
    # the universe on neither side: only a first-segment read keeps these two.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "notes.py", "# names-universe donor\n", src="scripts/pkg")
    write_module(tmp_path, "dot_imp.py", "import pkg.notes\n")
    write_module(tmp_path, "dot_from.py", "from pkg.notes import go\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr
    assert "scripts/dot_imp" in strict.stderr  # the ast.Import first segment
    assert "scripts/dot_from" in strict.stderr  # the ImportFrom first segment
    assert "2 shipped module(s)" in strict.stderr  # the donor is not a delta
    regen_map(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG not in strict.stderr  # the real generator absorbed both
    assert KN_MSG in strict.stderr  # the station rule holds the same red
    write_tagged_llrs(
        tmp_path,
        [
            ("scripts/mod_0", "CMP-001"),
            ("scripts/mod_1", "CMP-001"),
            ("scripts/dot_imp", "CMP-001"),
            ("scripts/dot_from", "CMP-001"),
        ],
    )
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


def test_docstring_only_module_is_inventoried_on_both_sides(tmp_path):
    # REVIEW-A finding 1, first of the masked pair: every MODULE_BODY fixture
    # carries a docstring AND a public symbol, so each arm alone was covered
    # by the other. This module's ONLY inventoried content is its docstring —
    # the generator keeps it (summary non-empty), so only the mirror's
    # docstring arm can keep it lane-side.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "doc_only.py", '"""Docstring-only module."""\n')
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr and "scripts/doc_only" in strict.stderr
    regen_map(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG not in strict.stderr  # the real generator absorbed it
    assert KN_MSG in strict.stderr  # the station rule holds the same red
    _tag_three(tmp_path, "scripts/doc_only")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


def test_public_symbol_only_module_is_inventoried_on_both_sides(tmp_path):
    # REVIEW-A finding 1, second of the masked pair: no docstring, one public
    # def — the generator keeps it (a public row exists), so only the mirror's
    # public-symbol arm can keep it lane-side.
    _contained_two_module_tree(tmp_path)
    write_module(tmp_path, "sym_only.py", "def run():\n    pass\n")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG in strict.stderr and "scripts/sym_only" in strict.stderr
    regen_map(tmp_path)
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 1
    assert ADDED_MSG not in strict.stderr
    assert KN_MSG in strict.stderr
    _tag_three(tmp_path, "scripts/sym_only")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr


def test_undecodable_module_is_skipped_lane_side_without_a_crash(tmp_path):
    # REVIEW-A finding 2, the read-failure branch — the one arm the
    # green-green differential CANNOT drive: gen_arch_map itself crashes on a
    # non-UTF-8 .py (probed: UnicodeDecodeError in scan_module's read_text,
    # rc 1), so there is no absorb side. Lane-side pin only: the mirror's
    # UnicodeDecodeError -> False must skip the file quietly — no delta red,
    # no crash (either drift direction reds here: a raise crashes the run, a
    # True puts the never-absorbable file in the delta). \xff is an invalid
    # UTF-8 start byte on every platform, so the fixture is deterministic;
    # the OSError half (an unreadable file — not stageable portably) stays
    # the argued exception.
    _contained_two_module_tree(tmp_path)
    (tmp_path / "scripts" / "bin_mod.py").write_bytes(b"\xff\xfe\x00not utf-8")
    strict = run_traj(tmp_path, "--strict")
    assert strict.returncode == 0, strict.stdout + strict.stderr
    assert ADDED_MSG not in strict.stderr


# --- WI-093: the [phase]-[g*] archetype + phase-drop detector ------------------
# The derived-gate model (docs/archive/specs/derived-gate-model.2026-07-20.md §7/§9.3): a phase's
# pre-dev batch is a WI whose Title carries a `[<phase>]-[g<N>]` tag; the derived
# gate dropping below a phase's closed anchor level warns to open a new phase-gate
# WI. All warn-first; the logic is unit-tested via load_script.


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
    assert ("v2", 1) in anchors and ("v2", 2) in anchors
    assert anchors[("v2", 2)]["id"] == "WI-202"  # first wins
    # The RETIRED `[phase]-[g2]` spelling still PARSES (the ~20 committed anchors
    # carry it and D-4 refuses re-pointing history), but the message names the
    # CANONICAL spelling, because what it is asking for is a NEW row.
    assert any("duplicate phase anchor [v2]-[tests]" in w for w in warns)


def test_the_CANONICAL_anchor_spelling_parses_to_the_same_levels():
    """OI-21 contract break 4: the ARCHETYPE converted, the live anchors did not.
    `[phase]-[reqs|tests]` is what a new title takes; `[phase]-[g1|g2]` is read
    forever so the committed history keeps resolving. Both must land on ONE
    internal level, or a phase would carry two independent anchor sets."""
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
    assert set(anchors) == {("v9", 1), ("v9", 2)}
    assert warns == []
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
    assert any("duplicate phase anchor [v9]-[reqs]" in w for w in mixed_warns)


def test_phase_anchor_g2_without_g1_predecessor_warns():
    ct = load_script("check_trajectory")
    wis = _wis(
        ct,
        [
            {"WI-ID": "WI-201", "Title": "[v3]-[g1] x", "Status": "done"},
            {"WI-ID": "WI-202", "Title": "[v3]-[g2] y", "Status": "queued"},  # no pred
        ],
    )
    _, warns = ct.phase_anchors(wis)
    assert any("does not list its [v3]-[reqs]" in w for w in warns)


def _write_gate(root, per_phase, value="DevBar-Reqs"):
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "docs" / "gate").write_text(
        "# header\n# basis: SN=1 SR=3 LLR=3 TC=3 drafts=0 computed={} "
        "per-phase={}\n# computed 2026-07-12 (as-of x)\n{}\n".format(
            value, per_phase, value
        ),
        encoding="utf-8",
    )


def test_read_derived_phases_parses_basis(tmp_path):
    ct = load_script("check_trajectory")
    _write_gate(tmp_path, "v1=DevBar-Release;v2=DevBar-Below")
    assert ct.read_derived_phases(tmp_path) == {"v1": 3, "v2": 0}
    # A legacy hand-set gate with no basis line yields no phase data (vacuous).
    (tmp_path / "docs" / "gate").write_text("# legacy\nG3\n", encoding="utf-8")
    assert ct.read_derived_phases(tmp_path) == {}


def test_phase_drop_detector_warns(tmp_path):
    ct = load_script("check_trajectory")
    # v2 closed at [g2] (done) but the derived level for v2 is now DevBar-Below (a reopen).
    _write_gate(tmp_path, "v1=DevBar-Release;v2=DevBar-Below")
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
        "phase 'v2' dropped to DevBar-Below" in w and "[v2]-[tests]" in w for w in warns
    )
    # Back at DevBar-Tests: no drop warn (the phase re-cleared its anchor level).
    _write_gate(tmp_path, "v1=DevBar-Release;v2=DevBar-Tests", value="DevBar-Tests")
    assert ct.phase_findings(tmp_path, wis) == []


def test_phase_findings_vacuous_without_anchors(tmp_path):
    ct = load_script("check_trajectory")
    _write_gate(
        tmp_path, "v1=DevBar-Below"
    )  # a phase at DevBar-Below but NO anchor records a close
    wis = _wis(ct, [{"WI-ID": "WI-220", "Title": "ordinary", "Status": "queued"}])
    assert ct.phase_findings(tmp_path, wis) == []


# --- WI-146(b): the ratification-brief hierarchy-view lint --------------------
# An open-items ROW whose decision is a `[phase]-[g1|g2]` ratification should
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


def test_ratify_brief_without_view_warns(tmp_path):
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        _oi_row("OI-20", "ratify the [v3]-[g2] dashboard batch.")
        + _oi_row("OI-21", "something else, no anchor here."),
    )
    warns = ct.ratify_brief_findings(tmp_path)
    # Exactly the ratification brief warns; the unrelated row does not.
    assert len(warns) == 1
    assert warns[0].startswith("OI-20:")
    assert "hierarchy view" in warns[0]


def test_ratify_brief_with_generator_command_only_warns(tmp_path):
    # A bare `trace.py --ratify` command mention is NOT proof the view exists and
    # is carried — the brief must name the generated view (WI-146 REVIEW-A).
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        _oi_row(
            "OI-20", "ratify the [v3]-[g2] batch. Hierarchy: run trace.py --ratify v3."
        ),
    )
    warns = ct.ratify_brief_findings(tmp_path)
    assert len(warns) == 1 and warns[0].startswith("OI-20:")


def test_ratify_brief_with_view_link_is_silent(tmp_path):
    ct = load_script("check_trajectory")
    _write_open_items(
        tmp_path,
        _oi_row(
            "OI-20", "ratify the [v3]-[g2] batch. See the tree: docs/ratify/v3-g2.md."
        ),
    )
    assert ct.ratify_brief_findings(tmp_path) == []


def test_ratify_brief_lint_is_vacuous_off_the_pending_queue(tmp_path):
    ct = load_script("check_trajectory")
    # No registry at all -> nothing to check.
    assert ct.ratify_brief_findings(tmp_path) == []
    # A ratification word with no [phase]-[g*] anchor -> not a brief.
    _write_open_items(tmp_path, _oi_row("OI-30", "whether to ratify a policy change."))
    assert ct.ratify_brief_findings(tmp_path) == []
    # ...an anchor with no ratification language -> also not a brief.
    _write_open_items(tmp_path, _oi_row("OI-31", "sequence [v3]-[g2] after v2 work."))
    assert ct.ratify_brief_findings(tmp_path) == []
    # ...and a RULED row is history, not a pending decision, so it never warns
    # even when it carries both (the negative half WI-322 added).
    _write_open_items(
        tmp_path,
        _oi_row("OI-32", "ratify the [v3]-[g2] batch.", status="ruled"),
    )
    assert ct.ratify_brief_findings(tmp_path) == []


# --- WI-064: the cross-CMP-edge-without-IF rule ---------------------------------
# An internal import edge between two DIFFERENT components with no covering
# IF-### row is a finding (the AXES ratified model's enforceability ruling) —
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


def test_cross_cmp_import_with_declared_seam_is_silent(tmp_path):
    _cross_cmp_repo(tmp_path)
    write_ifs(
        tmp_path,
        'IF-001,Consumes,scripts/mod_a,scripts/mod_b,"call",SR-001,v1,Stable,Active,,\n',
    )
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
    silently becomes "not yet ratified", which on a repo that ratifies nothing
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
