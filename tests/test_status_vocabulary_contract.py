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

# The kit-root surfaces DELIBERATELY outside the value scan, each with its
# reason. The list exists so that adding a new `.md` to the kit root forces a
# choice — join the scan or say why — rather than silently landing outside it
# (2026-08-20, the batch review's MINOR-15 / ROUND-SOL MAJOR-7: "a new
# instructing surface outside the fixed list is also invisible").
NON_INSTRUCTING_KIT_DOCS = {
    "CLAUDE.stub.template.md": "a three-line pointer at AGENTS.md; teaches nothing",
    "GEMINI.stub.template.md": "the same stub for a second agent",
    "LOG.template.md": "an empty append-only log; records, never instructs",
    "OWNER_SCRATCHPAD.template.md": "the owner's free-form notes surface",
    "PLAN.template.md": "an empty plan surface a session fills",
    "STATUS.template.md": "the scaffolded status surface, filled per repo",
    "RUNTIME_FLOWS.template.md": "an authored-narrative shell",
    "README.template.md": "the scaffold's own README shell",
    "RESYNC_PACK.md": "a dated migration ledger — its entries are history by "
    "construction, and a retired value in one is the content",
    "EXTERNAL_SKILLS.md": "a pointer index to sibling repos",
    "README.md": "the kit's own front door; the ROOT README is scanned instead",
}

# The prose-sentence channel's HISTORICAL markers. A retired value is legitimate
# in a sentence that says it retired — recording that this tier has been renamed
# is what stops the next rename looking arbitrary. Token-scoped (see
# `_exempt_near`), never line-scoped.
_HISTORICAL = re.compile(
    r"retire|renamed|folded|legacy|superseded|no longer|used to|until |was |"
    r"before |historical|status-ok",
    re.IGNORECASE,
)
# How far from the retired word a historical marker still speaks for it. One
# clause, roughly — wide enough for "`Stability` — `Experimental`/`Stable` —
# retired at WI-442", narrow enough that a retirement note elsewhere on a long
# table row cannot excuse live guidance beside it.
_NEAR = 120


def _existing(paths):
    return [p for p in paths if p.is_file()]


def _text(path):
    return path.read_text(encoding="utf-8")


def _exempt_near(line, match, pattern=_HISTORICAL, near=_NEAR):
    """True when `pattern` appears within `near` characters of `match` on this
    line — the TOKEN-SCOPED exemption idiom.

    The line-scoped form is what these scans used until 2026-08-20, and it is
    the same defect the `docs/provenance-allow` key had one file over: a table
    row that legitimately records one retirement then excuses every other
    retired word on the same row, including live guidance. Scoping the
    exemption to the token it explains is what makes it an exemption rather
    than an off-switch."""
    lo = max(0, match.start() - near)
    return bool(pattern.search(line[lo : match.end() + near]))


def test_the_retired_and_live_status_words_never_overlap():
    """The premise the other tests stand on — REPAIRED 2026-08-20 (the batch
    review's MINOR-15). The disjointness assertion was TRUE BY CONSTRUCTION:
    `RETIRED_STATUS_WORDS` is `EVER - STATUS_VALUES`, so it cannot intersect
    `STATUS_VALUES` however wrong either side is, and a test that cannot fail
    reads as coverage while proving nothing.

    What CAN fail, and is the property actually needed, is the other direction:
    the hand-written `EVER_STATUS_WORDS` must contain every live value. Add a
    value to the enum and forget it here and the retired set silently narrows —
    the scans below keep passing while a whole word goes unwatched."""
    assert frozenset(trace.STATUS_VALUES) <= EVER_STATUS_WORDS, (
        "the enum carries {} which this module's EVER_STATUS_WORDS does not "
        "list — add it, or the retired set is computed against a stale "
        "universe".format(sorted(frozenset(trace.STATUS_VALUES) - EVER_STATUS_WORDS))
    )
    assert "Modified" in RETIRED_STATUS_WORDS, (
        "Modified retired at D-9 step 7 (2026-08-20 signing) — if it is live "
        "again, this module's premise changed and the docs need re-reading"
    )
    assert {"Drafted", "Approved"} <= frozenset(trace.STATUS_VALUES)
    assert RETIRED_STATUS_WORDS, "a scan for retired words with none to find"


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

    A mention that names it AND says it retired is exempt: recording that this
    tier has been renamed three times is precisely what stops the fourth
    rename from looking arbitrary.

    TOKEN-SCOPED SINCE 2026-08-20 (the batch review's MINOR-15). The exemption
    used to search the WHOLE LINE for "retire", which on a long table row —
    exactly where these column tables live — meant one legitimate retirement
    note excused every other `Approval` mention on the row, live guidance
    included. It now has to stand beside the token it explains.

    Scanned in ONE test over all surfaces rather than parametrized per file:
    the whole scan costs a few milliseconds, the failure names every offending
    file:line anyway, and the per-commit smoke tier is a membership budget that
    thirteen ids would spend for no signal."""
    hits = []
    for path in _existing(COLUMN_SCAN_SURFACES):
        for n, line in enumerate(_text(path).splitlines(), 1):
            for m in re.finditer(r"`Approval`", line):
                if not _exempt_near(line, m, re.compile(r"retire", re.I)):
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


def test_no_instructing_surface_TEACHES_a_retired_status_value_IN_PROSE():
    """THE SECOND CHANNEL (2026-08-20, the batch review's MINOR-15 / ROUND-SOL
    MAJOR-7). The assignment scan above reads `status = "<word>"`, which is one
    of the two ways a document teaches a value. The other is a sentence:

        Valid statuses are Drafted, Modified, and Approved.

    That plants a retired word in an adopter's head just as effectively, carries
    no `=`, and passed the contract clean — which is what the review demonstrated.

    NARROW BY DESIGN, and the narrowness is the reason it can ship at all. A
    retired word alone is not a finding: `Draft`, `Stable` and `Planned` are
    ordinary English and this kit's prose is dense. The line must ALSO be talking
    about the field — it must carry `status` — and the retired word must not
    stand beside a historical marker (`retired`, `renamed`, `folded`, `was`,
    `no longer`, …) within one clause, or an explicit `status-ok`. Measured on
    the live surfaces before shipping: one line matched, `INTERFACES.template.md`'s
    `Status` row recording the two columns that retired into it, and the
    token-scoped historical exemption clears it — so this guards zero-to-zero,
    which is the only honest place to start a prose scan.

    What it does NOT reach, stated rather than implied: a sentence that teaches
    the value without using the word `status`, and any surface outside
    `INSTRUCTING_SURFACES` (the test below makes that list answer to the kit)."""
    retired = sorted(RETIRED_STATUS_WORDS)
    word = re.compile(r"\b(" + "|".join(retired) + r")\b")
    field = re.compile(r"status", re.IGNORECASE)
    bad = []
    for path in _existing(INSTRUCTING_SURFACES):
        for n, line in enumerate(_text(path).splitlines(), 1):
            if not field.search(line):
                continue
            for m in word.finditer(line):
                if not _exempt_near(line, m):
                    bad.append("{}:{} ({})".format(path.name, n, m.group(1)))
    assert not bad, (
        "these instructing surfaces name a RETIRED status value in a sentence "
        "about the status field, with no historical marker beside it — live "
        "values are {}. Say when it retired, or drop it: {}".format(
            sorted(trace.STATUS_VALUES), ", ".join(bad)
        )
    )


def test_every_kit_root_doc_either_JOINS_the_scan_or_says_why():
    """THE THIRD CHANNEL: the surface list itself. `INSTRUCTING_SURFACES` is a
    hand-written enumeration, so a new instructing document lands OUTSIDE every
    scan above and nothing says so — the review's second planted case.

    Derived rather than re-listed: every `.md` at the kit root and under
    `specs/` must be either in the scan or in `NON_INSTRUCTING_KIT_DOCS` with a
    stated reason. Adding a doc then forces the choice, which is the cheapest
    form of "derive the instructing set from the shipped kit" that does not
    guess at what instructs."""
    scanned = {p.name for p in INSTRUCTING_SURFACES}
    unclassified = []
    for path in sorted(KIT.glob("*.md")) + sorted((KIT / "specs").glob("*.md")):
        if path.name in scanned or path.name in NON_INSTRUCTING_KIT_DOCS:
            continue
        unclassified.append(path.name)
    assert not unclassified, (
        "these kit documents are in neither the status-vocabulary scan nor the "
        "declared non-instructing list — a new instructing surface outside the "
        "list is invisible to every check in this module: {}".format(
            ", ".join(unclassified)
        )
    )
    # The exclusion list must not outlive its files, or it becomes a place to
    # park a name that no longer exists.
    stale = [
        n
        for n in NON_INSTRUCTING_KIT_DOCS
        if not (KIT / n).is_file() and not (KIT / "specs" / n).is_file()
    ]
    assert not stale, "declared non-instructing docs that do not exist: {}".format(
        ", ".join(stale)
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
