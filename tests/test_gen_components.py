"""WI-484 phase 3 — the generated component view (OI-32 ruled option (d)).

The claims this module holds, one per thing the ruling actually decided:

  * the JOIN — design rows placed through the interfaces their verifying
    test cases name (a row names no component since WI-1023), the requirement
    tier reached THROUGH them, the perspectives DERIVED (never copied), each
    file's membership from its `Component:` header, the seams placed by their
    endpoints;
  * the THREE COVERAGE EDGES the brief refused to let the execution paper
    over — a requirement that reaches no component, one that reaches several,
    and whether seams enter the view at all. Each is asserted as a VISIBLE
    answer, because "the generator drops it" and "the generator has a bug"
    are indistinguishable from the outside;
  * the STANDING CONSTRAINT — a generated file never carries an acceptance
    (OI-30 D3);
  * the FRESHNESS CONTRACT — `--check` fails on a stale view and passes once
    regenerated. A check that cannot fail converts a visible gap into an
    invisible one.
"""

import pytest

from conftest import SCRIPTS, load_script, run_py

GEN = "gen_components"


def _write(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


CMPS = """[component.CMP-001]
name = "Alpha"
category = "software"
status = "Accepted"

[component.CMP-002]
name = "Beta"
category = "software"
status = "Drafted"
"""

SRS = """[requirement.SR-001]
title = "shared across two components"
hat_refs = ["SECURITY"]
status = "Accepted"

[requirement.SR-002]
title = "alpha only"
status = "Accepted"

[requirement.SR-003]
title = "no design child at all"
status = "Accepted"
"""

LLRS = """[design.LLR-001]
sr_refs = ["SR-001"]
title = "in alpha"
status = "Accepted"

[design.LLR-002]
sr_refs = ["SR-001", "SR-002"]
title = "in beta"
hat_refs = ["MAINTAINER"]
status = "Accepted"
"""

# Each design row sits at the owner of the interface its verifying case names.
TCS = """[test.TC-001]
verifies = ["LLR-001", "IF-002"]
status = "Accepted"

[test.TC-002]
verifies = ["LLR-002", "IF-004"]
status = "Accepted"
"""

IFS = """[interface.IF-001]
owner = "CMP-001"
consumers = ["CMP-002"]
channel = "call"

[interface.IF-002]
owner = "CMP-001"
consumers = ["CMP-001"]
channel = "call"

[interface.IF-003]
owner = "external:somebody"
consumers = ["external:somebody-else"]
channel = "bytes"

[interface.IF-004]
owner = "CMP-002"
consumers = ["external:somebody"]
channel = "bytes"
"""


@pytest.fixture
def repo(tmp_path):
    """A two-component spine small enough to reason about by hand and wide
    enough to carry all three coverage edges at once, its two source files
    each declaring the component its design row is placed in."""
    _write(tmp_path, "docs/requirements/components.toml", CMPS)
    _write(tmp_path, "docs/requirements/system-requirements.toml", SRS)
    _write(tmp_path, "docs/requirements/low-level-requirements.toml", LLRS)
    _write(tmp_path, "docs/requirements/interfaces.toml", IFS)
    _write(tmp_path, "docs/test/test-cases.toml", TCS)
    _write(tmp_path, "docs/stack.ini", "[paths]\nsrc = project-trajectory/scripts\n")
    _declare(tmp_path, "alpha", "CMP-001")
    _declare(tmp_path, "beta", "CMP-002")
    return tmp_path


def _declare(root, stem, component):
    _write(
        root,
        "project-trajectory/scripts/{}.py".format(stem),
        '"""{}.\n\nComponent: {}\n"""\n'.format(stem, component),
    )


def _view(root):
    import tomllib

    gen = load_script(GEN)
    return tomllib.loads(gen.render(root))


# --- the join ----------------------------------------------------------------


def test_membership_and_the_requirement_reach(repo):
    """Implements: TC-195"""
    view = _view(repo)["component_view"]
    assert view["CMP-001"]["llr_refs"] == ["LLR-001"]
    assert view["CMP-002"]["llr_refs"] == ["LLR-002"]
    # An SR carries no component cell — it is reached THROUGH its design rows.
    assert view["CMP-001"]["sr_refs"] == ["SR-001"]
    assert view["CMP-002"]["sr_refs"] == ["SR-001", "SR-002"]
    assert view["CMP-001"]["modules"] == ["project-trajectory/scripts/alpha.py"]


def test_a_design_row_sits_where_the_interface_it_constrains_is_owned(repo):
    """Implements: TC-195"""
    # A row no case places by an interface sits at the owner of the interface
    # it constrains, beside the place its case gives it, and its requirement
    # reaches that component through it.
    llrs = repo / "docs" / "requirements" / "low-level-requirements.toml"
    llrs.write_text(
        LLRS.replace(
            'title = "in alpha"', 'title = "in alpha"\nconstrains = ["IF-004"]'
        )
        + '\n[design.LLR-003]\nsr_refs = ["SR-003"]\ntitle = "constrains only"\n'
        'constrains = ["IF-002"]\nstatus = "Accepted"\n',
        encoding="utf-8",
        newline="\n",
    )
    doc = _view(repo)
    view = doc["component_view"]
    assert view["CMP-001"]["llr_refs"] == ["LLR-001", "LLR-003"]
    assert view["CMP-002"]["llr_refs"] == ["LLR-001", "LLR-002"]
    assert view["CMP-001"]["sr_refs"] == ["SR-001", "SR-003"]
    assert doc["unplaced"]["sr_refs"] == []


def test_the_hat_union_is_DERIVED_from_the_parent_not_copied(repo):
    """Implements: TC-195"""
    # The anti-staleness decision, one tier up: LLR-001 carries no hat cell at
    # all, and its component still records SECURITY because its SR parent does.
    view = _view(repo)["component_view"]
    assert view["CMP-001"]["hat_refs"] == ["SECURITY"]
    assert view["CMP-002"]["hat_refs"] == ["MAINTAINER", "SECURITY"]


def test_a_parent_re_ruling_moves_the_view_with_no_design_cell_edited(repo):
    """Implements: TC-195"""
    # The whole point of deriving rather than copying: re-rule ONE requirement
    # and every component that reaches it follows on the next regeneration.
    srs = repo / "docs" / "requirements" / "system-requirements.toml"
    srs.write_text(
        SRS.replace('hat_refs = ["SECURITY"]', 'hat_refs = ["ACCESSIBILITY"]'),
        encoding="utf-8",
        newline="\n",
    )
    view = _view(repo)["component_view"]
    assert view["CMP-001"]["hat_refs"] == ["ACCESSIBILITY"]


# --- coverage edge 1: a requirement that reaches no component ----------------


def test_a_childless_requirement_is_listed_ONCE_and_never_dropped(repo):
    """Implements: TC-195"""
    doc = _view(repo)
    assert doc["unplaced"]["sr_refs"] == ["SR-003"]
    assert doc["derived"]["requirements_unplaced"] == 1
    assert doc["derived"]["requirements_placed"] == 2
    # ...and it is in no component's section, which is the correct answer for a
    # constraint that names no object — but it is COUNTED, so a reader can tell
    # "deliberately outside every component" from "the generator lost it".
    for row in doc["component_view"].values():
        assert "SR-003" not in row["sr_refs"]


# --- coverage edge 2: a requirement that reaches several ---------------------


def test_a_shared_requirement_appears_in_EVERY_component_it_reaches(repo):
    """Implements: TC-195"""
    view = _view(repo)["component_view"]
    assert "SR-001" in view["CMP-001"]["sr_refs"]
    assert "SR-001" in view["CMP-002"]["sr_refs"]
    # ...and is marked shared in both, so the view never implies exclusive
    # ownership and a reader is not left thinking one of the two is a mistake.
    assert view["CMP-001"]["sr_shared_refs"] == ["SR-001"]
    assert view["CMP-002"]["sr_shared_refs"] == ["SR-001"]
    assert view["CMP-002"]["sr_refs"].count("SR-002") == 1
    assert "SR-002" not in view["CMP-002"]["sr_shared_refs"]


# --- coverage edge 3: the seams ----------------------------------------------


def test_seams_enter_the_view_split_internal_from_boundary(repo):
    """Implements: TC-195"""
    view = _view(repo)["component_view"]
    # IF-002's endpoints are both inside CMP-001 -> internal to it.
    assert view["CMP-001"]["seam_internal_refs"] == ["IF-002"]
    # IF-001 crosses the two, so it is a BOUNDARY of BOTH — a seam belongs to
    # each side of itself, which is what makes the view show a component's edges.
    assert view["CMP-001"]["seam_boundary_refs"] == ["IF-001"]
    # IF-004 has an external party on its far side: a boundary of CMP-002 and
    # internal to nothing.
    assert view["CMP-002"]["seam_boundary_refs"] == ["IF-001", "IF-004"]


def test_a_seam_is_placed_by_the_components_its_endpoints_name(repo):
    """Implements: TC-195"""
    # No row carries a placement cell (it left the schema): a row is placed
    # from its endpoint cells, which name components, so both rows naming
    # CMP-001 appear in it.
    view = _view(repo)["component_view"]
    placed = set(view["CMP-001"]["seam_internal_refs"]) | set(
        view["CMP-001"]["seam_boundary_refs"]
    )
    assert placed == {"IF-001", "IF-002"}


def test_seam_placement_reads_the_endpoint_cells_and_no_join(repo, monkeypatch):
    """The generator holds no membership join of its own (WI-1005), and since
    a row names components (WI-1022) a seam is placed from its endpoint cells
    alone: stubbing `kitlib.spine.module_components` to answer nothing moves
    no seam, and the one row naming no component is still the only one
    unplaced.

    Implements: TC-435"""
    gen = load_script(GEN)
    assert not hasattr(gen, "module_components"), "the generator's copy is deleted"
    monkeypatch.setattr(gen._kitspine, "module_components", lambda declared: {})
    declared = gen.arch_inputs.component_headers(repo)[0]
    view, unplaced = gen.build(*gen._load(repo), declared)
    assert unplaced["seam_refs"] == ["IF-003"]
    assert view["CMP-001"]["seam_internal_refs"] == {"IF-002"}


def test_the_modules_and_the_seams_follow_the_headers(repo):
    """A file's component is its header: moving alpha's header to CMP-002 moves
    alpha into CMP-002's modules, while the case verifying LLR-001 at an
    interface CMP-001 owns still places the row there and the seams stay where
    their endpoint cells put them. A file no design row names is listed by its
    header alone.

    Implements: TC-460"""
    _declare(repo, "alpha", "CMP-002")
    _declare(repo, "gamma", "CMP-002")
    view = _view(repo)["component_view"]
    assert view["CMP-001"]["modules"] == []
    assert view["CMP-002"]["modules"] == [
        "project-trajectory/scripts/alpha.py",
        "project-trajectory/scripts/beta.py",
        "project-trajectory/scripts/gamma.py",
    ]
    assert view["CMP-001"]["seam_internal_refs"] == ["IF-002"]
    assert view["CMP-002"]["seam_internal_refs"] == []
    assert view["CMP-001"]["llr_refs"] == ["LLR-001"]


def test_an_unplaceable_seam_is_REPORTED_not_silently_excluded(repo):
    """Implements: TC-195"""
    # IF-003 is external at both ends: it names no component. It cannot be
    # placed — and it is named, because a seam that vanishes reads exactly
    # like a seam the generator failed on.
    doc = _view(repo)
    assert doc["unplaced"]["seam_refs"] == ["IF-003"]
    assert doc["derived"]["seams_unplaced"] == 1


# --- the standing constraint: no acceptance, ever ------------------------------


def test_the_generated_view_carries_NO_acceptance_cell(repo):
    """Implements: TC-195"""
    # OI-30 D3. `components.toml` says CMP-001 is Accepted and CMP-002 Drafted;
    # neither word may appear here in any cell, because a generator that wrote
    # one would route around the very dial operator_accepts_through governs.
    text = load_script(GEN).render(repo)
    doc = _view(repo)
    for row in doc["component_view"].values():
        assert not {"status", "standing", "approval"} & set(row)
    body = "\n".join(ln for ln in text.splitlines() if not ln.lstrip().startswith("#"))
    assert "Accepted" not in body and "Drafted" not in body


# --- the freshness contract --------------------------------------------------


def test_check_reds_on_a_stale_view_and_greens_once_regenerated(repo):
    """Implements: TC-195"""
    gen = load_script(GEN)
    assert gen.main(["--root", str(repo)]) == 0
    assert gen.main(["--root", str(repo), "--check"]) == 0
    # The real failure mode: a registry row moves and nobody regenerates. Its
    # verifying case now names an interface CMP-001 owns, which moves the row.
    tcs = repo / "docs" / "test" / "test-cases.toml"
    tcs.write_text(
        TCS.replace('["LLR-002", "IF-004"]', '["LLR-002", "IF-002"]'),
        encoding="utf-8",
        newline="\n",
    )
    assert gen.main(["--root", str(repo), "--check"]) == 1
    assert gen.main(["--root", str(repo)]) == 0
    assert gen.main(["--root", str(repo), "--check"]) == 0


def test_check_reds_when_the_view_is_missing_entirely(repo):
    """Implements: TC-195"""
    assert load_script(GEN).main(["--root", str(repo), "--check"]) == 1


def test_the_written_file_is_LF_and_reproducible(repo):
    """Implements: TC-195"""
    gen = load_script(GEN)
    assert gen.main(["--root", str(repo)]) == 0
    out = repo / "docs" / "requirements" / "components.derived.toml"
    assert b"\r\n" not in out.read_bytes(), (
        "a CRLF copy fails --check immediately after being generated"
    )
    assert gen.render(repo) == gen.render(repo)


def test_a_repo_with_no_real_component_is_VACUOUS(tmp_path):
    """Implements: TC-195"""
    # The layer is optional and off-spine: a fresh scaffold ships only the inert
    # CMP-000 row, and the gate must not fail it over something it never adopted.
    _write(
        tmp_path,
        "docs/requirements/components.toml",
        '[component.CMP-000]\nname = "EXAMPLE"\ncategory = "software"\n',
    )
    gen = load_script(GEN)
    assert gen.main(["--root", str(tmp_path)]) == 0
    assert gen.main(["--root", str(tmp_path), "--check"]) == 0
    assert not (tmp_path / "docs/requirements/components.derived.toml").exists()


def test_the_cli_runs_out_of_process(repo):
    """Implements: TC-195"""
    # The step check.py wires is a subprocess, so the import path has to hold
    # there too (a sibling import that only resolves in-process is a pass here
    # and a failure in the gate).
    proc = run_py([SCRIPTS / "gen_components.py", "--root", str(repo)], cwd=repo)
    assert proc.returncode == 0, proc.stdout + proc.stderr
