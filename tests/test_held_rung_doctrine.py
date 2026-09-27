"""Who takes a held rung's approval: stated once, pointed at everywhere else.

process.md §4 holds the one statement that a held rung's approval is the
owner's act (the owner, or an attended session on the owner's explicit
delegation; never a mechanically triggered session) and which half of that is
mechanical. The dial's comments and the gate-advance skill point at it. A
second home would drift from the first the way the dial's "the human approves"
comments already had, so these tests pin one statement and its pointers.

In-memory: they read files and nothing else, so they sit in the smoke tier.
"""

import re

from conftest import KIT, ROOT

PROCESS = KIT / "PROCESS.md"

# The canonical paragraph's bold lead, which appears nowhere else.
CANONICAL_LEAD = "**A held rung's approval is the owner's act**"

# What each pointer names: the section and the paragraph's lead, quoted.
POINTER = "process.md §4 \"A held rung's approval is the owner's act\""

# Phrases only the statement itself uses. A file outside PROCESS.md carrying
# one is restating the rule rather than pointing at it.
DOCTRINE_PHRASES = ("explicit delegation", "mechanically triggered")

# AGENTS.template.md sits within a few bytes of its hard cap, so its ladder
# line points at the section alone rather than quoting the paragraph's lead.
AGENTS_POINTER = "per `docs/process.toml` and process.md §4"

# The homes that must point at the statement, each with the pointer it carries.
POINTER_HOMES = {
    ROOT / "docs" / "process.toml": POINTER,
    KIT / "process.toml.template": POINTER,
    KIT / "skills" / "gate-advance" / "SKILL.md": POINTER,
    ROOT / ".claude" / "skills" / "gate-advance" / "SKILL.md": POINTER,
    ROOT / ".agents" / "skills" / "gate-advance" / "SKILL.md": POINTER,
    KIT / "AGENTS.template.md": AGENTS_POINTER,
}

# RESYNC_PACK.md narrates what changed for adopters, so its entry for this
# change describes the statement; it is history, not a second home.
EXEMPT = {KIT / "RESYNC_PACK.md"}


def _flat(path):
    """The file's text with comment markers at line starts removed and all
    whitespace collapsed, so a phrase wrapped across lines (or across `# `
    comment lines) still reads as one phrase."""
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"\n[ \t]*#[ \t]?", "\n", text)
    return " ".join(text.split())


def _shipped_prose():
    """Every shipped prose or template file (the gate-authority tripwire's
    population in test_gate_policy), plus this repository's own dial file."""
    for path in sorted(KIT.rglob("*")):
        if not path.is_file() or "scripts" in path.relative_to(KIT).parts:
            continue
        if path.suffix == ".md" or ".template" in path.name:
            yield path
    yield ROOT / "docs" / "process.toml"


def test_process_md_holds_the_canonical_paragraph_once():
    text = _flat(PROCESS)
    assert text.count(CANONICAL_LEAD) == 1, (
        "process.md must carry the held-rung approval paragraph exactly once "
        "(keyed on {!r}); found {}".format(CANONICAL_LEAD, text.count(CANONICAL_LEAD))
    )
    for phrase in DOCTRINE_PHRASES:
        assert phrase in text.lower(), (
            "the canonical paragraph lost {!r}; update DOCTRINE_PHRASES with it".format(
                phrase
            )
        )


def test_the_doctrine_is_stated_only_in_process_md():
    restated = {}
    for path in _shipped_prose():
        if path == PROCESS or path in EXEMPT:
            continue
        text = _flat(path).lower()
        hits = [p for p in DOCTRINE_PHRASES if p in text]
        if CANONICAL_LEAD.lower() in text:
            hits.append(CANONICAL_LEAD)
        if hits:
            restated[str(path.relative_to(ROOT))] = hits
    assert not restated, (
        "the held-rung approval rule is restated outside process.md §4 — point "
        "at it with {!r} instead: {}".format(POINTER, restated)
    )


def test_each_home_points_at_the_statement():
    missing = {
        str(path.relative_to(ROOT)): pointer
        for path, pointer in POINTER_HOMES.items()
        if pointer not in _flat(path)
    }
    assert not missing, "these homes lost their pointer to process.md §4: {}".format(
        missing
    )
