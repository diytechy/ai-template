"""One authoritative status contract — the shipped and reference prose is
checked against the enforcement constants it describes (WI-477, repo review
2026-08-19 H-06).

WHY THIS MODULE EXISTS. The maturity vocabulary has been renamed four times
(`Stability` -> an undeclared `Status` -> `Approval` -> `Status`) and re-valued
twice (`Draft`/`Verified`/`Planned` folded to `Drafted`/`Approved`; `Modified`
retired, `Founded` added at the 2026-08-20 signing). Every rename landed in the
enforcing constants and in SOME of the ten documents that teach them, and the
review found the residue: `INTERFACES.template.md` documented an `Approval`
column its own worked example did not use, two spec templates taught a
`Status=Proposed` row that has never been legal, and the release checklist
still spoke of `Stable` interfaces. An adopter following the shipped docs
authored fields the shipped checker rejects.

THE FIX IS NOT ANOTHER SWEEP. Hand-maintaining one vocabulary in ten places is
what produced the drift, so this module makes the DOCS answer to
`trace.ENUM_FIELDS` -- the same dict `schema_findings` and the integrity floor
read. Rename a value there and these tests fail until the prose follows, which
is the property the tenth hand-sweep did not buy.

Deliberately a CONTRACT test, not a generator: the surfaces are prose with
per-tier argument in them (why `Founded` cannot apply to a seam, which columns
retired into which), and generating that from a frozenset would either lose the
argument or push it into the constants. Pinning the vocabulary while leaving
the prose hand-written is the split that keeps both honest.
"""

import re

from conftest import KIT, ROOT, load_script

trace = load_script("trace")


# The enforced sets, read from the one home rather than restated here.
SPINE_STATUS = frozenset(trace.ENUM_FIELDS["SR"]["Status"])
IF_STATUS = frozenset(trace.ENUM_FIELDS["IF"]["Status"])
FRAME_STATUS = frozenset(trace.ENUM_FIELDS["B"]["Status"])

# Every word that has ever been a status value in this kit. Retired = the ones
# the live enum no longer contains, computed rather than listed twice so that
# promoting a value out of retirement cannot leave this set contradicting
# `STATUS_VALUES`.
EVER_STATUS_WORDS = frozenset(
    {
        "Draft",
        "Drafted",
        "Proposed",
        "Planned",
        "Modified",
        "Verified",
        "Approved",
        "Founded",
        "Implemented",
        "Stable",
        "Experimental",
        "Provisional",
    }
)
RETIRED_STATUS_WORDS = EVER_STATUS_WORDS - frozenset(trace.STATUS_VALUES)

# The INSTRUCTING surfaces: what a downstream adopter reads and follows before
# authoring a row. An illegal value here is copied into a real registry, which
# is the damage. Generated views, archived history, plans, reviews and logs are
# deliberately absent -- they record what was true when written, and rewriting
# history to match today's vocabulary is exactly the dishonesty this kit exists
# to prevent.
INSTRUCTING_SURFACES = (
    KIT / "PROCESS.md",
    KIT / "PROCESS_OPTIONS.md",
    KIT / "INTERFACES.template.md",
    KIT / "EXAMPLE.md",
    KIT / "KICKOFF_PROMPT.md",
    KIT / "MULTI_REPO.md",
    KIT / "ADOPTING.md",
    KIT / "AGENTS.template.md",
    KIT / "specs" / "README.template.md",
    KIT / "specs" / "WI-000.template.md",
    ROOT / "README.md",
)

# The two reference docs join the COLUMN-NAME scan but not the value scan.
# Their whole job is to say what each rule was and became ("Was nothing -- an
# invented citation passed every strict gate while its row read
# `Status=Verified`"), so a retired value in a past-tense clause is the content,
# not drift. A retired COLUMN name is different: `Approval` names a key nothing
# reads, in a doc a maintainer consults as current.
REFERENCE_SURFACES = (
    ROOT / "docs" / "registry-machinery-reference.md",
    ROOT / "docs" / "enforcement-audit.md",
)

COLUMN_SCAN_SURFACES = INSTRUCTING_SURFACES + REFERENCE_SURFACES


def _existing(paths):
    return [p for p in paths if p.is_file()]


def _text(path):
    return path.read_text(encoding="utf-8")


def test_the_retired_and_live_status_words_never_overlap():
    """The premise the other tests stand on. If a retired word were also live,
    every scan below would be vacuous in the one direction that matters."""
    assert RETIRED_STATUS_WORDS.isdisjoint(trace.STATUS_VALUES)
    assert "Modified" in RETIRED_STATUS_WORDS, (
        "Modified retired at D-9 step 7 (2026-08-20 signing) — if it is live "
        "again, this module's premise changed and the docs need re-reading"
    )
    assert {"Drafted", "Approved"} <= frozenset(trace.STATUS_VALUES)


def test_the_interfaces_template_teaches_exactly_the_enforced_if_vocabulary():
    """`INTERFACES.template.md`'s `Status` row is the adopter's field guide for
    the tier. It documented an `Approval` column with `draft`/`approved` while
    the checker enforced `Status` with `Drafted`/`Approved` — and its own worked
    example, twenty lines below, already wrote `status = "Approved"`."""
    text = _text(KIT / "INTERFACES.template.md")
    row = next(
        (ln for ln in text.splitlines() if ln.startswith("| `Status` |")),
        None,
    )
    assert row is not None, (
        "INTERFACES.template.md has no `| `Status` |` column row — the IF tier's "
        "one maturity field must be documented under the name enforcement reads"
    )
    # Only the DECLARED clause, not every backticked word on the row: the row
    # also names `Founded` (to rule it out) and the columns that retired into
    # this one, and both of those belong there.
    clause = re.search(r"maturity field:\s*(.+?)\.", row)
    assert clause is not None, (
        "INTERFACES.template.md's `Status` row no longer declares its values in "
        "a 'maturity field: ...' clause — this contract reads that clause"
    )
    declared = {
        w
        for w in re.findall(r"`([A-Za-z]+)`", clause.group(1))
        if w in EVER_STATUS_WORDS
    }
    assert declared == IF_STATUS, (
        "the taught IF vocabulary {} does not match the enforced {} "
        "(trace.ENUM_FIELDS['IF']['Status'])".format(
            sorted(declared), sorted(IF_STATUS)
        )
    )


def test_the_worked_example_uses_the_vocabulary_the_table_teaches():
    """The self-contradiction the review actually caught: a column documented in
    the table that the file's own copy-ready example never writes."""
    text = _text(KIT / "INTERFACES.template.md")
    written = set(re.findall(r'^status = "([A-Za-z]+)"', text, re.MULTILINE))
    assert written, "INTERFACES.template.md's worked example writes no status cell"
    assert written <= IF_STATUS, (
        "the example writes {} but the tier enforces {}".format(
            sorted(written), sorted(IF_STATUS)
        )
    )


def test_no_surface_names_the_retired_approval_column_as_current():
    """`Approval` was the transitional name between `Stability` and `Status`.
    A doc still naming it as a column sends an adopter to author a key nothing
    reads.

    A line that names it AND says it retired is exempt: recording that this
    tier has been renamed three times is precisely what stops the fourth
    rename from looking arbitrary, and the exemption cannot hide live guidance
    because a sentence claiming `Approval` is current does not also call it
    retired.

    Scanned in ONE test over all surfaces rather than parametrized per file:
    the whole scan costs a few milliseconds, the failure names every offending
    file:line anyway, and the per-commit smoke tier is a membership budget that
    thirteen ids would spend for no signal."""
    hits = []
    for path in _existing(COLUMN_SCAN_SURFACES):
        for n, line in enumerate(_text(path).splitlines(), 1):
            if "`Approval`" in line and not re.search(r"retire", line, re.IGNORECASE):
                hits.append("{}:{}".format(path.name, n))
    assert not hits, (
        "these surfaces name the retired `Approval` column as current (it is "
        "`Status` since the 2026-08-17 registry status unification): "
        "{}".format(", ".join(hits))
    )


def test_no_instructing_surface_assigns_a_retired_status_value():
    """A `Status=<word>` / `status = "<word>"` assignment is an instruction to
    author that cell. It must name a value the enum still carries — this is
    what caught `Status=Proposed` in both spec templates and `Status=Modified`
    in the README's derived-gate paragraph."""
    pattern = re.compile(r'\bstatus\s*=\s*"?([A-Za-z]+)"?', re.IGNORECASE)
    bad = []
    for path in _existing(INSTRUCTING_SURFACES):
        for n, line in enumerate(_text(path).splitlines(), 1):
            for word in pattern.findall(line):
                if word.capitalize() in RETIRED_STATUS_WORDS:
                    bad.append("{}:{} ({})".format(path.name, n, word))
    assert not bad, (
        "these surfaces instruct an author to set a RETIRED status value — "
        "live values are {}: {}".format(sorted(trace.STATUS_VALUES), ", ".join(bad))
    )


def test_the_frame_and_interface_tiers_share_one_subset():
    """PROCESS.md §8 and the registry reference both promise the IF tier's
    maturity field is 'shared with the boundary tier'. Pin the promise so a
    per-registry divergence has to change the prose too."""
    assert IF_STATUS == FRAME_STATUS
    assert IF_STATUS < SPINE_STATUS, (
        "the off-spine subset must stay a strict subset of the spine's ladder — "
        "`Founded` means settled AND demonstrated, which an approval never says"
    )
