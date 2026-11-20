"""Policy behaviours that had more than one home and disagreed on some input,
each walked to one home with the disputed inputs pinned (WI-1004).

The OI-130 re-score (`docs/plans/2026-11-11-oi130-rescore/README.md`, "One
home per behaviour") found eleven policy behaviours whose copies disagreed.
Each section below is one behaviour: the inputs on which its copies
disagreed, each named in a test with the answer the one home keeps, and a
check that no former holder still carries a copy. The kept answers and their
reasons are the spec's (`WI-1004`, "The eleven, in landing order"). B3's and
B5's pins repair the vacuous ones in `tests/test_rule_sync.py` and live there.

Implements: TC-439, TC-440, TC-441, TC-442, TC-443, TC-444
"""

import tomllib

import pytest
from conftest import load_script

migrate_carrier = load_script("migrate_carrier")
wi_convert = load_script("wi_convert")
check_docs = load_script("check_docs")
check_flows = load_script("check_flows")
consolidate = load_script("consolidate")
adjudicate_brief = load_script("adjudicate_brief")
intake = load_script("intake")
agent_common = load_script("agent_common")
integrate = load_script("integrate")
handback = load_script("handback")

import kitlib.decisions as kitlib_decisions  # noqa: E402  (after load_script)
import kitlib.registry as kitlib_registry  # noqa: E402
import kitlib.spine as kitlib_spine  # noqa: E402


# --- 2. B12 the module key -----------------------------------------------------
# `migrate_carrier._short_module` folded an id-typed IF owner through its LLR's
# one module by stripping only a `.py` suffix; `kitlib.spine.norm_module`, the
# key the endpoint check compares an owner through, also strips any source
# extension and a trailing `/__init__`. Kept: `norm_module`'s, so the owner the
# migration writes names a module the check resolves.


def _old_shape_if_repo(tmp_path, modules):
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    llrs, ifs = [], []
    for n, module in enumerate(modules, start=1):
        llrs.append(
            '[design.LLR-{0}]\nsr_refs = ["SR-1"]\nmodule = "{1}"\n'.format(n, module)
        )
        ifs.append(
            '[interface.IF-{0}]\nowner = "LLR-{0}"\nsignal = "a retired cell"\n'
            'consumers = ["scripts/far"]\nstatus = "Drafted"\n'.format(n)
        )
    (req / "low-level-requirements.toml").write_text("\n".join(llrs), encoding="utf-8")
    (req / "interfaces.toml").write_text("\n".join(ifs), encoding="utf-8")
    return req / "interfaces.toml"


def test_the_if_shape_migration_folds_an_owner_through_the_one_module_key(tmp_path):
    """Implements: TC-439"""
    assert not hasattr(migrate_carrier, "_short_module")
    registry = _old_shape_if_repo(
        tmp_path,
        [
            "project-trajectory/scripts/kitlib/__init__.py",  # disputed: __init__.py
            "hooks/pre-commit.sh",  # disputed: a non-.py source path
            "project-trajectory/scripts/plain.py",  # control: both agreed
        ],
    )
    migrate_carrier.convert_if_shape(tmp_path, write=True)
    owners = {
        rid: row["owner"]
        for rid, row in tomllib.loads(registry.read_text(encoding="utf-8"))[
            "interface"
        ].items()
    }
    assert owners == {
        "IF-1": "scripts/kitlib",
        "IF-2": "hooks/pre-commit",
        "IF-3": "scripts/plain",
    }


# --- 3. the id number read from an id --------------------------------------------
# `kitlib.spine._id_number` and `kitlib.decisions._id_number` read the digits
# after the last dash (0 when that tail is not all digits);
# `kitlib.registry.spec_id_number` and `wi_convert._id_number` read the first
# run of digits. Every id a supported route mints reads the same either way.
# Kept: the digits after the last dash, which the open-item coverage rule
# matches covered numbers through; the other answer reads `OI-35abc` as OI-35.


def test_an_id_number_is_the_digits_after_the_last_dash():
    """Implements: TC-440"""
    for absent in (
        (kitlib_registry, "spec_id_number"),
        (kitlib_decisions, "_id_number"),
        (kitlib_spine, "_id_number"),
        (wi_convert, "_id_number"),
    ):
        assert not hasattr(*absent), absent
    cases = {
        "X2-5": 5,  # disputed: the first digit run read 2
        "WI-12a": 0,  # disputed: the first digit run read 12
        "OI-35abc": 0,
        "WI-0012": 12,
        "OI-98": 98,
        "D-001": 1,
        "WI-": 0,
        "": 0,
    }
    for rid, number in cases.items():
        assert kitlib_spine.id_number(rid) == number, rid


def _spec(work, folder, wid, extra=""):
    path = work / folder / "{}-x.md".format(wid)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '+++\nid = "{}"\ntitle = "t"\n{}+++\n'.format(wid, extra),
        encoding="utf-8",
        newline="\n",  # the converter reads newline="", as a checkout holds it
    )
    return path


def test_both_spec_folder_orderings_read_the_one_id_number(tmp_path):
    """Implements: TC-440"""
    work = tmp_path / "docs" / "work"
    for wid in ("WI-3", "WI-12a", "WI-20"):
        _spec(work, "queued", wid)
    expected = ["WI-12a", "WI-3", "WI-20"]  # WI-12a reads 0, so it sorts first
    assert [r["WI-ID"] for r in kitlib_registry.read_spec_rows(work)] == expected
    assert [row["WI-ID"] for row, _o, _r in wi_convert.read_specs(work)] == expected


# --- 4. B5 the SN-id universe ------------------------------------------------------
# `check_docs._registry_needs` (the README inventory's existence set) and
# `check_flows.load_ids` (the ids a runtime flow may cite) each scraped every
# `SN-###` token out of the whole needs file; `kitlib.spine.sn_all_ids` reads
# the need tables only under TOML and drops `-000`. On a TOML needs file the
# scrapes counted an id written only in a comment or a stakeholder description
# as a need, and `check_flows` counted `SN-000`. Kept: the home's answer, the
# rule SR-189 states and the gate derivation already reads.

NEEDS_TOML = """# SN-098 is named in a comment and is no need.
[need.SN-000]
status = "Accepted"
need = "The template's example need."
priority = "M"

[need.SN-001]
status = "Accepted"
need = "A real need, which cites SN-002 in its own text."
priority = "M"

[need.SN-002]
status = "Accepted"
need = "A second real need."
priority = "C"

[stakeholder.STK-01]
name = "Operator"
description = "Owns SN-099, which no need table declares."
status = "Accepted"
"""


def _needs_repo(tmp_path):
    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    path = req / "stakeholder-needs.toml"
    path.write_text(NEEDS_TOML, encoding="utf-8")
    return path


def test_the_readme_inventory_reads_the_one_sn_universe_on_a_toml_needs_file(
    tmp_path,
):
    """Implements: TC-441"""
    path = _needs_repo(tmp_path)
    all_ids, must_should = check_docs._registry_needs(path)
    # The comment's SN-098 and the stakeholder description's SN-099 are no need.
    assert all_ids == {"SN-001", "SN-002"}
    assert all_ids == kitlib_spine.sn_all_ids(path.read_text(encoding="utf-8"), ".toml")
    assert must_should == {"SN-001"}


def test_the_flow_check_reads_the_one_sn_universe_on_a_toml_needs_file(tmp_path):
    """Implements: TC-441"""
    _needs_repo(tmp_path)
    known = check_flows.load_ids(tmp_path / "docs")
    # Neither the comment's nor the description's id is a need, and the
    # template's -000 placeholder is not counted either.
    assert known["SN"] == {"SN-001", "SN-002"}


# --- 5. B10 the ref split ----------------------------------------------------------
# `kitlib.spine.refs` splits a ref cell on `;`, `,` or whitespace, and
# `split_pred_edges` partitions a `Predecessors` cell over it: the reading the
# scheduler, the validator and the dashboard take. `consolidate`,
# `adjudicate_brief` and `intake` split their ref cells on `;` only, so a
# hand-written `SR-1, SR-2` read as one token naming nothing, and
# `consolidate._commissioning_docs` missed open-item edges and counted `OI-5x`
# as one. `agent_common._refs` was an agreeing copy. Kept: the home's reading.

PREDECESSOR_CELLS = (
    "OI-5",
    "WI-1;OI-5",
    "WI-1, OI-5",  # disputed: a comma
    "WI-1 OI-5",  # disputed: whitespace
    "OI-5;OI-6, OI-8\tOI-9",
    "~OI-7",  # a soft marker on an open item is ignored: OI edges are hard
    "OI-5x",  # disputed: not an open-item token, a hard work-item token
    "~WI-2;WI-3",
    "",
)


def test_consolidate_finds_every_open_item_edge_split_pred_edges_finds():
    """Implements: TC-442"""
    for cell in PREDECESSOR_CELLS:
        _spec, ois = consolidate._commissioning_docs(
            {"Predecessors": cell, "SpecRef": "docs/x.md"}
        )
        assert ois == set(kitlib_spine.split_pred_edges(cell)[1]), cell


def test_every_ref_cell_read_splits_through_the_one_home(tmp_path):
    """Implements: TC-442"""
    assert agent_common._refs is kitlib_spine.refs
    pair = "SR-1, SR-2"  # the disputed input: a comma-separated ref cell
    assert consolidate._superseded({"Supersedes": "WI-1 WI-2"}) == {"WI-1", "WI-2"}
    model = consolidate._model([{"WI-ID": "WI-9", "SR-Refs": pair}])
    assert model[0]["srs"] == ["SR-1", "SR-2"]
    llrs = [{"LLR-ID": "LLR-1", "SR-Refs": "SR-2 SR-3", "Module": "a/one.py"}]
    assert consolidate._llr_modules({"SR-3"}, llrs) == {"one.py"}
    assert consolidate.touched_modules(
        tmp_path, {"SR-Refs": "SR-9, SR-3"}, llrs=llrs
    ) == {"one.py"}
    assert intake._owning_srs(
        [{"id": "LLR-1", "routed": {"SR-Refs": ("SR-1, SR-2", "SR-4")}}]
    ) == ["SR-1", "SR-2"]

    req = tmp_path / "docs" / "requirements"
    req.mkdir(parents=True)
    (req / "low-level-requirements.toml").write_text(
        '[design.LLR-1]\nsr_refs = "SR-2, SR-3"\nmodule = "a/one.py"\n',
        encoding="utf-8",
    )
    wanted = adjudicate_brief._cited_spine(
        tmp_path, ["WI-9"], {"WI-9": {"SR-Refs": pair}}
    )
    assert wanted == {"SR-1", "SR-2", "LLR-1"}


# --- 6. B8b the spec parse ----------------------------------------------------------
# `kitlib.registry.parse_spec_row` (every registry reader) and
# `wi_convert.parse_spec` (the converter) each parsed a spec file. The registry
# wrote a non-string scalar as its text and refused an id its filename does not
# carry and an `adjudicates` value its one parser refuses; the converter refused
# the first and accepted the other two. Kept: refused, all three. The converter
# keeps only its own precondition, the `active/` refusal, and calls the home.

SPEC_REFUSALS = {
    "title = 5": (
        '+++\nid = "WI-7"\ntitle = 5\n+++\n',
        "queued/WI-7-x.md",
        "`title` must be a string",
    ),
    "a non-string list element": (
        '+++\nid = "WI-7"\nsr_refs = [5]\n+++\n',
        "queued/WI-7-x.md",
        "`sr_refs` must be a string",
    ),
    "a non-string supersedes element": (
        '+++\nid = "WI-7"\nsupersedes = [5]\n+++\n',
        "queued/WI-7-x.md",
        "`supersedes` must be a string",
    ),
    "an id the filename does not carry": (
        '+++\nid = "WI-7"\ntitle = "t"\n+++\n',
        "queued/WI-8-x.md",
        "filename does not carry its own id",
    ),
    'adjudicates = ["a;b"]': (
        '+++\nid = "WI-7"\nadjudicates = ["a;b"]\n+++\n',
        "queued/WI-7-x.md",
        "`adjudicates` is",
    ),
    'adjudicates = "a"': (
        '+++\nid = "WI-7"\nadjudicates = "a"\n+++\n',
        "queued/WI-7-x.md",
        "`adjudicates` is",
    ),
}


def test_the_converter_parses_a_spec_through_the_one_parser():
    """Implements: TC-443"""
    for name in ("split_spec", "parse_deliverable", "status_from_location", "_text"):
        assert not hasattr(wi_convert, name), name
    # The control: an integer priority is the one non-string scalar both read.
    good = '+++\nid = "WI-7"\ntitle = "t"\npriority = 4\n+++\n'
    for parse in (kitlib_registry.parse_spec_row, wi_convert.parse_spec):
        row, _order = parse(good, "queued/WI-7-x.md")
        assert (row["Title"], row["Priority"]) == ("t", "4")
    for label, (text, rel, words) in SPEC_REFUSALS.items():
        with pytest.raises(ValueError) as reg:
            kitlib_registry.parse_spec_row(text, rel)
        assert words in str(reg.value), label
        with pytest.raises(wi_convert.ConvertError) as conv:
            wi_convert.parse_spec(text, rel)
        assert words in str(conv.value), label


def test_a_spec_with_a_non_string_title_is_reported_and_skipped(tmp_path):
    """Implements: TC-443"""
    work = tmp_path / "docs" / "work"
    _spec(work, "queued", "WI-8")
    bad = work / "queued" / "WI-7-x.md"
    bad.write_text('+++\nid = "WI-7"\ntitle = 5\n+++\n', encoding="utf-8")
    errors = []
    rows = kitlib_registry.read_spec_rows(work, on_error=errors.append)
    assert [r["WI-ID"] for r in rows] == ["WI-8"]
    assert len(errors) == 1 and "WI-7-x.md" in errors[0], errors
    assert "`title` must be a string" in errors[0]


# --- 7. the queued-spec lookup ------------------------------------------------------
# `integrate._queued_spec` (claim), `handback._queued_spec` (the edge and return
# writes) and the inline glob in `consolidate._archive_plan` (the consolidation
# close) each found an id's queued spec. Given two queued specs carrying one id,
# the claim refused while handback and the close acted on the first. Kept:
# refused, everywhere: each caller writes or moves the file, and acting on one
# copy leaves the other standing as a live queued row of the same id. None
# matching: every caller refused already, each in its own words.


def _two_queued(tmp_path, wid="WI-401"):
    work = tmp_path / "docs" / "work"
    first = _spec(work, "queued", wid)
    second = first.with_name("{}-y.md".format(wid))
    second.write_bytes(first.read_bytes())
    return work


def test_the_queued_spec_lookup_refuses_two_specs_of_one_id(tmp_path):
    """Implements: TC-444"""
    assert not hasattr(handback, "_queued_spec")
    work = _two_queued(tmp_path)
    with pytest.raises(ValueError) as exc:
        kitlib_registry.queued_spec(work, "WI-401")
    assert "2 queued specs carry WI-401" in str(exc.value)
    assert kitlib_registry.queued_spec(work, "WI-402") is None
    (work / "queued" / "WI-401-y.md").unlink()
    assert kitlib_registry.queued_spec(work, "WI-401").name == "WI-401-x.md"
    assert kitlib_registry.queued_spec(tmp_path / "absent", "WI-401") is None


def test_every_act_on_a_queued_spec_refuses_two_of_one_id(tmp_path):
    """Implements: TC-444"""
    _two_queued(tmp_path)
    before = sorted(p.name for p in (tmp_path / "docs/work/queued").iterdir())
    # The claim (it already refused; the wording is now the home's).
    with pytest.raises(ValueError) as exc:
        integrate._queued_spec(tmp_path, "WI-401")
    assert "2 queued specs carry WI-401" in str(exc.value)
    # A handback edge write: refused, nothing planned.
    plan, refusal = handback._enact_plan(
        tmp_path, {"edges": [("WI-401", "WI-399")], "returns": [], "finding": ""}
    )
    assert plan == [] and "2 queued specs carry WI-401" in refusal, refusal
    # The consolidation close archiving an absorbed row: refused, nothing planned.
    plan, refusal = consolidate._archive_plan(tmp_path, [("WI-500", ["WI-401"])])
    assert plan == [] and "2 queued specs carry WI-401" in refusal, refusal
    after = sorted(p.name for p in (tmp_path / "docs/work/queued").iterdir())
    assert before == after
    # None matching: each still refuses in its own words.
    with pytest.raises(ValueError):
        integrate._queued_spec(tmp_path, "WI-402")
    _plan, refusal = handback._enact_plan(
        tmp_path, {"edges": [("WI-402", "WI-399")], "returns": [], "finding": ""}
    )
    assert "is not a queued spec on this lane" in refusal
    _plan, refusal = consolidate._archive_plan(tmp_path, [("WI-500", ["WI-402"])])
    assert "no longer a queued spec" in refusal
