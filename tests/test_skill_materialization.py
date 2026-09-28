"""Verifies SR-112 / LLR-279 / IF-035 (TC-289): a skill materializes as its
whole directory, not its SKILL.md alone.

A skill may cite a file beside its SKILL.md. The per-agent fan-out check
compares every file of a skill against its source, so a first copy of the
SKILL.md alone is drifted the moment it is written. The unit is stated once
(`bootstrap.skill_copies`) and read by both the scaffold copy and the
delivered-package inventory; each is driven here on a planted two-file skill.
In-process: a planted kit and destination under tmp_path, no scaffold run, no
subprocess, no git.
"""

from conftest import load_script

COMPANION = "references/extra.md"


def _plant_skill(root, name="two"):
    """A one-skill neutral source: a SKILL.md plus one companion file it cites."""
    skill = root / "skills" / name
    (skill / "references").mkdir(parents=True)
    (skill / "SKILL.md").write_bytes(
        "---\nname: {0}\ndescription: x\nscope: kit\n---\nsee {1}\n".format(
            name, COMPANION
        ).encode("utf-8")
    )
    (skill / COMPANION).write_bytes(b"cited\n")
    return skill


def test_a_multi_file_skill_materializes_whole_and_passes_the_drift_check(tmp_path):
    boot = load_script("bootstrap")
    gen = load_script("gen_skills_index")
    skill = _plant_skill(tmp_path / "kit")
    dest = tmp_path / "dest"
    created = boot.materialize_agent_layer(
        dest, ["claude"], [("two", skill / "SKILL.md")], False, False
    )
    assert ".claude/skills/two/SKILL.md" in created
    assert ".claude/skills/two/" + COMPANION in created
    copy = dest / ".claude" / "skills" / "two" / COMPANION
    assert copy.read_bytes() == b"cited\n"
    drifts, _orphans, checked = gen.check_agent_sync(tmp_path / "kit" / "skills", dest)
    assert (drifts, checked) == ([], 1)


def test_the_delivery_inventory_lists_a_skills_companion_file(tmp_path, monkeypatch):
    # The inventory is the universe the delivered-package check grades MAPPING
    # against. A kit-scope skill's files are conditional deliveries, one per
    # agent skills directory; listing only its SKILL.md would leave the
    # companion file a physical source with no accounted destination.
    boot = load_script("bootstrap")
    kit = tmp_path / "kit"
    _plant_skill(kit)
    monkeypatch.setattr(boot, "KIT", kit)
    sources, _exclusions, conditional, _generated = boot.delivery_inventory()
    assert "skills/two/" + COMPANION in sources
    for spec in boot.AGENTS.values():
        for rel in ("SKILL.md", COMPANION):
            pair = ("skills/two/" + rel, "{}/two/{}".format(spec["skills_dir"], rel))
            assert pair in conditional, pair
