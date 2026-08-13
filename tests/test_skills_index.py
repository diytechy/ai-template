"""gen_skills_index.py: the skills applicability index stays generated + honest.

The kit's `skills/` folder holds agent-neutral SKILL.md definitions; INDEX.csv is
a generated scan surface over their frontmatter (like the code map). These tests
pin the frontmatter contract and the generator's behavior.
"""

import re

from conftest import KIT, load_script

SKILLS = KIT / "skills"


def test_kit_ships_the_skills_layer():
    assert SKILLS.is_dir(), "kit must ship a skills/ source dir"
    assert (SKILLS / "README.md").exists(), "skills/README.md (the contract) missing"
    assert (SKILLS / "INDEX.csv").exists(), "generated skills/INDEX.csv missing"
    # At least the five authored skills, each a dir with a SKILL.md.
    skill_dirs = [p for p in SKILLS.iterdir() if p.is_dir()]
    assert len(skill_dirs) >= 5
    for d in skill_dirs:
        assert (d / "SKILL.md").exists(), "missing SKILL.md in " + d.name


def test_every_skill_frontmatter_is_valid():
    gen = load_script("gen_skills_index")
    for skill_md in sorted(SKILLS.glob("*/SKILL.md")):
        fm = gen.parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        # name + description are the two agent-required fields; name == dir name.
        assert fm.get("name") == skill_md.parent.name, skill_md
        assert fm.get("description"), "missing description: " + str(skill_md)
        # scope is the kit-vs-this-repo split driver.
        assert fm.get("scope") in ("kit", "this-repo"), skill_md


def test_index_row_count_matches_skill_dirs():
    gen = load_script("gen_skills_index")
    rows = gen.collect_skills(SKILLS)
    n_dirs = len(list(SKILLS.glob("*/SKILL.md")))
    assert len(rows) == n_dirs


def test_downstream_resync_skill_points_at_the_pack_rather_than_restating_it():
    """The re-sync rules have ONE home: RESYNC_PACK.md (OI-27, ruled 2026-08-13).

    The skill used to restate ADOPTING.md §6's migration recipes — including a
    hand-maintained note that had drifted from the authority within weeks at zero
    re-sync traffic. §6's recipe half then moved into the pack, and the skill
    became a router: it names the pack and nothing else. This pin is deliberately
    shaped as "no WI-keyed content", because that is the exact form the
    duplication took and the exact form it would come back in — the entries are
    keyed by kit SHA now, so a WI id OR a `[since <sha>]` anchor reappearing here
    means someone copied an entry across instead of linking it.
    """
    text = (SKILLS / "downstream-resync" / "SKILL.md").read_text(encoding="utf-8")
    body = text.split("---", 2)[2]  # frontmatter is not prose
    assert "RESYNC_PACK.md" in body, "the skill must name its authority"
    strays = sorted(set(re.findall(r"\bWI-\d+\b", body)))
    assert not strays, (
        "the skill restates pack entry content again ({}) — the entries are "
        "keyed by WI id and kit SHA, so point at the pack instead of copying it "
        "across; the copy is what drifted last time (OI-27)".format(", ".join(strays))
    )
    anchors = sorted(set(re.findall(r"\[since [0-9a-f]{7,40}\]", body)))
    assert not anchors, (
        "the skill carries a pack ENTRY anchor ({}) — an anchored entry belongs "
        "in RESYNC_PACK.md §3/§4, never in a second home".format(", ".join(anchors))
    )


def test_generator_rejects_name_dir_mismatch(tmp_path):
    gen = load_script("gen_skills_index")
    bad = tmp_path / "skills" / "wrong-name"
    bad.mkdir(parents=True)
    (bad / "SKILL.md").write_text(
        "---\nname: different\ndescription: x\n---\nbody\n", encoding="utf-8"
    )
    try:
        gen.collect_skills(tmp_path / "skills")
        assert False, "expected a ValueError on name/dir mismatch"
    except ValueError as e:
        assert "!=" in str(e)
