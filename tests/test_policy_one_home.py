"""Policy behaviours that had more than one home and disagreed on some input,
each walked to one home with the disputed inputs pinned (WI-1004).

The OI-130 re-score (`docs/plans/2026-11-11-oi130-rescore/README.md`, "One
home per behaviour") found eleven policy behaviours whose copies disagreed.
Each section below is one behaviour: the inputs on which its copies
disagreed, each named in a test with the answer the one home keeps, and a
check that no former holder still carries a copy. The kept answers and their
reasons are the spec's (`WI-1004`, "The eleven, in landing order"). B3's and
B5's pins repair the vacuous ones in `tests/test_rule_sync.py` and live there.

Implements: TC-439
"""

import tomllib

from conftest import load_script

migrate_carrier = load_script("migrate_carrier")


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
