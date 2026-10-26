"""The shared architecture-decomposition rubric, as shipped and as seeded.

The kit ships one rubric a critic judges a component scope's decomposition
against: at the architecture stage, when a work item's plan answers its
architectural-delta question, and in an audit. These in-process pins hold
its text to the shape the planners and critics rely on:

  * each clarification it asks is asked inside the anchor that owns it, and
    none of them is a new failure pattern;
  * its stopping anchor keeps requirement descent and component descent
    apart, each with its own rule, and names what a stopping record holds;
  * every reference it makes reads in an adopter's repository: its only link
    is its sibling README, it cites no record of this repository, and each
    quoted section title is found in the section it names;
  * the scaffold mapping seeds it once, with its purpose reference, and the
    scaffold layout `bootstrap.py --help` prints names it.

The scaffold run that sees the seeded destination is in test_bootstrap.py,
which is in the slow tier.
"""

import re

from conftest import KIT, ROOT, load_script

TEMPLATE = KIT / "rubrics" / "architecture-decomposition.template.md"
SEEDED = "docs/rubrics/architecture-decomposition.md"

# An anchor head: `**A1 — <title>.**` or `**B1 — <title>.**` at a line start.
_HEAD = re.compile(r"^\*\*([AB]\d+) — ", re.MULTILINE)
# The ids of this repository's own records; an adopter has none of them.
_RECORD_ID = re.compile(r"\b(?:WI|SN|SR|LLR|TC|IF|OI|CMP)-\d+\b")
_LINK = re.compile(r"\]\(([^)\s]+)\)")


def _flat(text):
    return " ".join(text.split())


def _template():
    assert TEMPLATE.is_file(), "the kit ships no rubric at {}".format(TEMPLATE)
    return TEMPLATE.read_text(encoding="utf-8")


def _anchors(text):
    """Each anchor id mapped to its slice: from its head to the next anchor
    head or `## ` heading."""
    heads = list(_HEAD.finditer(text))
    out = {}
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        heading = text.find("\n## ", head.start(), end)
        out[head.group(1)] = text[head.start() : end if heading < 0 else heading]
    return out


# Each clarification's key phrases, in the anchor that asks it.
CLARIFICATIONS = {
    "A6": ("implementation owner", "obligation allocation", "kernel"),
    "A7": (
        "transaction scope",
        "lock order",
        "retry",
        "durable effect",
        "access constraint",
        "migration plan",
        "new endpoint crossing",
        "shared schema",
        "unknown remainder",
        "insufficient evidence for approval",
    ),
    "A4": ("not supplied", "not assessable"),
}


def test_each_clarification_is_asked_in_its_anchor():
    """Adequacy: a rubric that put a clarification in the Terms or in a
    neighbouring anchor would leave the anchor's own question unchanged, and
    a critic citing that anchor would not be asked it."""
    anchors = _anchors(_template())
    for anchor, phrases in CLARIFICATIONS.items():
        assert anchor in anchors, anchor
        body = _flat(anchors[anchor]).lower()
        for phrase in phrases:
            assert phrase in body, (anchor, phrase)


def test_no_failure_pattern_is_added_for_them():
    heads = {a for a in _anchors(_template()) if a.startswith("B")}
    assert heads == {"B1", "B2", "B3", "B4"}


A8_TESTS = (
    "A describable state",
    "An invented number",
    "A paraphrase",
    "No pass/fail of its own",
)
A8_RECORD = ("candidate children", "evidence", "remaining uncertainty", "revisit")


def test_a8_separates_requirement_descent_from_component_descent():
    """Adequacy: an A8 that kept only the four obligation tests would give a
    component leaf no cost-based stop, and one that dropped the record fields
    would let a leaf stop with no record of what would reopen it."""
    anchors = _anchors(_template())
    assert "A8" in anchors
    body = _flat(anchors["A8"])
    for label in A8_TESTS:
        assert label in body, label
    lower = body.lower()
    assert "requirement" in lower and "component descent" in lower
    assert "information-hiding cut" in lower and "A1/A4/A7" in body
    for field in A8_RECORD:
        assert field in lower, field


def _section(text, number):
    """`## <number>.` up to the next `## ` heading, whitespace-flattened."""
    start = text.index("\n## {}.".format(number))
    end = text.find("\n## ", start + 1)
    return _flat(text[start : end if end >= 0 else len(text)])


def test_references_read_in_an_adopters_repo():
    """Adequacy: a rubric copied from its draft would keep the draft's
    `../../../rubrics/README.md` link (which resolves nowhere in a scaffold),
    and a misquoted section title sends the critic to a rule that is not
    there."""
    text = _template()
    flat = _flat(text)
    links = _LINK.findall(text)
    assert links and set(links) == {"README.md"}, links
    assert _RECORD_ID.findall(text) == []
    assert "docs/plans/" not in text and not re.search(r"\bW3\b", text)

    process = (KIT / "PROCESS.md").read_text(encoding="utf-8")
    process_quotes = re.findall(r"\bprocess\.md §(\d+),? \"([^\"]+)\"", flat)
    assert process_quotes
    for number, quote in process_quotes:
        assert quote in _section(process, number), (number, quote)

    options = _flat((KIT / "PROCESS_OPTIONS.md").read_text(encoding="utf-8"))
    options_quotes = re.findall(r"process-options\.md,? \"([^\"]+)\"", flat)
    assert options_quotes
    for quote in options_quotes:
        assert quote in options, quote

    home = (KIT / "prompts" / "spine-questions.md").read_text(encoding="utf-8")
    home_quotes = re.findall(r"spine-questions\.md`? §(\d+),? \"([^\"]+)\"", flat)
    assert home_quotes
    for number, quote in home_quotes:
        assert quote in _section(home, number), (number, quote)

    destinations = {
        dst for _src, dst, _ref in load_script("bootstrap").mapping_entries()
    }
    for named in ("docs/process.md", "docs/process-options.md"):
        assert named in destinations, named
    assert "prompts/spine-questions.md" in destinations


def test_the_manifest_seeds_it_once_with_its_purpose():
    """The in-process pin of the scaffold destination (the scaffold run itself
    is slow). Adequacy: a row without its purpose reference warns as unmapped,
    and a second row seeding the same destination is a copy conflict."""
    entries = load_script("bootstrap").mapping_entries()
    row = ("rubrics/architecture-decomposition.template.md", SEEDED, "SR-186")
    assert row in entries
    assert [e for e in entries if e[1] == SEEDED] == [row]
    assert (ROOT / SEEDED).is_file()


def test_the_scaffold_layout_an_adopter_reads_names_every_seeded_rubric():
    """The layout `bootstrap.py --help` prints lists each rubric the manifest
    seeds. Adequacy: a layout listing only the README and the inert example
    tells an adopter the shared rubric is not part of their scaffold."""
    bootstrap = load_script("bootstrap")
    layout = bootstrap.__doc__
    seeded = [
        dst
        for _src, dst, _ref in bootstrap.mapping_entries()
        if dst.startswith("docs/rubrics/")
    ]
    assert SEEDED in seeded
    for dst in seeded:
        assert dst in layout, dst
