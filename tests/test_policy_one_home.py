"""Policy behaviours that had more than one home and disagreed on some input,
each walked to one home with the disputed inputs pinned (WI-1004).

The OI-130 re-score (`docs/plans/2026-11-11-oi130-rescore/README.md`, "One
home per behaviour") found eleven policy behaviours whose copies disagreed.
Each section below is one behaviour: the inputs on which its copies
disagreed, each named in a test with the answer the one home keeps, and a
check that no former holder still carries a copy. The kept answers and their
reasons are the spec's (`WI-1004`, "The eleven, in landing order"). B3's and
B5's pins repair the vacuous ones in `tests/test_rule_sync.py` and live there.

Implements: TC-439, TC-440, TC-441
"""

import tomllib

from conftest import load_script

migrate_carrier = load_script("migrate_carrier")
wi_convert = load_script("wi_convert")
check_docs = load_script("check_docs")
check_flows = load_script("check_flows")

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
