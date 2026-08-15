#!/usr/bin/env python3
"""Spine-row TEXT rules and the row primitives they share (WI-329).

Split out of `trace.py`, which owns the JOIN — this module owns the question
"is this one row readable and decidable on its own?", asked four ways:

| function                | tier     | what it catches                          |
|-------------------------|----------|------------------------------------------|
| `provenance_findings`   | gating   | the row carries its own history          |
| `form_findings`         | gating   | the row is not one testable obligation   |
| `paraphrase_advisories` | advisory | the child re-words its parent            |
| `ac_advisories`         | advisory | a comparative with no named predicate    |

They are PURE predicates — rows in, findings out. No I/O, no git, no
filesystem, no argv — which is the pure-core / I-O-shell split process.md §3
asks for, and what makes them cheap to test in isolation.

The row primitives (`refs`, `is_example`, `is_drafted`) live here because this is
the lower layer: `trace.py` imports them back rather than the reverse, so the
dependency runs one way and there is no cycle.

This is NOT the shared-`_kitcommon` shape that was ruled out for breaking a
script's independent copy-ability: it is one module's own core, imported by that
one module. A re-sync copies two files where it copied one (ADOPTING.md §6).

Contracts: IF-076 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.csv).

Requirements: LLR-004 (ac_advisories), LLR-133 (provenance_findings),
LLR-134 (form_findings), LLR-135 (paraphrase_advisories).
"""

import re


def refs(value):
    """Split a multi-ref cell (';', ',' or whitespace separated) into ids."""
    return [t for t in re.split(r"[;,\s]+", (value or "").strip()) if t]


def is_example(rid):
    return (rid or "").endswith("-000")


def is_drafted(row):
    """A row in the pre-approval `Drafted` state (derived-gate model §3): exempt
    from the child-completeness orphan rules (a Drafted SR needs no LLR/TC, a
    Drafted LLR needs no TC) and from the --require-verified criterion, so a
    requirement lives in the live spine while it is being drafted.

    RENAMED FROM `is_draft` AT D-9 MIGRATION STEP 5 with the value it reads
    (`Draft` -> `Drafted`). `Status` is a CLOSED vocabulary since step 1 and
    narrows to `{Drafted, Approved, Modified}` here; no predicate anywhere
    honours the retired words, which `tests/test_rule_sync.py` asserts
    negatively over the source of every script."""
    return (row.get("Status") or "").strip().lower() == "drafted"


# Comparative/absolute terms that demand a predicate. Matched on word
# boundaries, case-insensitive ("schema-identical" matches "identical";
# "mismatches" does not match "matches").
COMPARATIVE_TERMS = (
    "identical",
    "indistinguishable",
    "equivalent",
    "interchangeable",
    "same as",
    "matches",
    "cannot distinguish",
    "cannot be distinguished",
    "no difference",
)
_TERM_RES = {
    t: re.compile(r"(?<!\w)" + re.escape(t).replace(r"\ ", r"\s+") + r"(?!\w)", re.I)
    for t in COMPARATIVE_TERMS
}

# Markers that (heuristically) pin a predicate in the same cell: an explicit
# definition/enumeration, a measurement/tolerance, or an exact-comparison basis.
# Word markers match on a WORD BOUNDARY, so "per"/"within" pin "as per the list"
# / "within 1 ULP" but NOT "proper"/"wrapper"/"notwithstanding" — a bare
# substring silently over-suppressed the advisory (warn-only, so this only
# sharpens lint quality). Symbol/abbreviation markers carry their own boundaries
# and match literally.
_PREDICATE_WORDS = (
    "namely",
    "defined",
    "specified",
    "listed",
    "enumerated",
    "per",
    "measured",
    "within",
    "tolerance",
    "predicate",
    "byte-for-byte",
    "bit-for-bit",
    # Self-pinning comparatives: "byte-identical"/"bit-identical" *name* their
    # predicate (the comparison basis is raw bytes/bits), exactly like
    # "byte-for-byte" — the bare comparative "identical" alone still warns.
    "byte-identical",
    "bit-identical",
    "golden",
    "regex",
    "checksum",
)
_PREDICATE_SYMBOLS = ("i.e.", "e.g.", "±", "==")
_PREDICATE_RE = re.compile(
    "|".join(
        [r"\b" + re.escape(w) + r"\b" for w in _PREDICATE_WORDS]
        + [re.escape(s) for s in _PREDICATE_SYMBOLS]
    ),
    re.IGNORECASE,
)


def ac_advisories(srs):
    """Warn-only findings: real SR rows whose AcceptanceCriteria uses a
    comparative term with no pinning marker anywhere in the cell."""
    out = []
    for r in srs:
        cell = (r.get("AcceptanceCriteria") or "").strip()
        if not cell:
            continue
        terms = [t for t, rx in _TERM_RES.items() if rx.search(cell)]
        if terms and not _PREDICATE_RE.search(cell):
            out.append(
                "SR {} AcceptanceCriteria uses {} without a named predicate — "
                "say identical/equivalent *in what*, judged *how* (process.md "
                "§4 consistency review; heuristic, warn-only)".format(
                    r["SR-ID"], ", ".join(repr(t) for t in sorted(terms))
                )
            )
    return out


_WI_TOKEN_RE = re.compile(r"\bWI-\d+")
_PROCESS_DOC_RE = re.compile(r"\bprocess(?:-options)?\.md\b", re.IGNORECASE)

# Requirement FORM (process.md §3). The stand-alone rule below says a row must not
# carry its own history; these say it must be ONE testable obligation. They are
# 29148's individual-requirement characteristics restricted to the half a checker
# can decide with no judgement — singular, unambiguous, verifiable. Every pattern
# was measured across all three registries before it shipped, and five of the six
# fire on 0-1 rows: these are guards, not a cleanup schedule.
_SHALL_RE = re.compile(r"\bshall\b", re.IGNORECASE)
# Non-`shall` modals in a REQUIREMENT only. An AcceptanceCriteria legitimately
# says "may" (a permitted outcome) and a Rationale says "would" (the consequence
# of the alternative), so widening this cries wolf on correct prose.
# `must` is deliberately ABSENT. 29148 reserves `shall`, but a project that uses
# `must` as its obligation keyword is following a different convention, not making
# an error — and this rule ships downstream, where flagging it would red every SR
# in such a repo on their first re-sync. The kit does not adjudicate that choice;
# it flags the modals that are ambiguous ALONGSIDE an obligation keyword.
_MODAL_RE = re.compile(
    r"\b(?:should|may|might|could|would|can|will|ought to)\b", re.IGNORECASE
)
# Unfalsifiable adjectives: a criterion no test can settle. `ac_advisories` warns
# on a comparative with no predicate; this gates on the terms that have no
# predicate to name.
# `etc\.` leads the alternation and carries NO trailing \b: a word boundary after
# a period only exists mid-sentence, so `\betc\.\b` silently never fires. The
# first version had it inside the \b-wrapped group and matched nothing; the test's
# positive half is what caught it.
_VAGUE_RE = re.compile(
    r"\betc\.|"
    r"\b(?:as appropriate|as needed|if possible|where practical|user-friendly|"
    r"efficient(?:ly)?|robust|flexible|sufficient(?:ly)?|adequate(?:ly)?|"
    r"reasonable|state of the art|seamless(?:ly)?|intuitive|easy to use|"
    r"minimal|optimal|appropriate(?:ly)?|and so on|TBD|TBC)\b",
    re.IGNORECASE,
)
# Open-ended clauses: the scope cannot be closed, so the row cannot be completed.
_ESCAPE_RE = re.compile(
    r"(?:including but not limited to|at a minimum|among others|such as)",
    re.IGNORECASE,
)
# "shall be logged" names no logger. Passive with a `by <actor>` is fine.
_ACTORLESS_RE = re.compile(r"\bshall be\s+\w+(?:ed|en)\b(?!\s+by\b)", re.IGNORECASE)


# Every spine cell whose text a reader treats as the SPECIFICATION — the columns
# a downstream adopter reads to learn what the system does and why. `Module`,
# `CodeSymbol`, `TestRefs`, `Evidence` and the id/status columns are pointers by
# design and are deliberately out of scope.
PROVENANCE_COLS = (
    ("SR", "SR-ID", ("Title", "Requirement", "Rationale", "AcceptanceCriteria")),
    ("LLR", "LLR-ID", ("Title", "Detail", "Rationale")),
    ("TC", "TC-ID", ("Method", "Expected", "Parameters")),
)


def provenance_findings(srs, llrs, tcs):
    """A spine row whose text carries its own PROVENANCE — a work-item id, or a
    citation of the process doc the row obeys (the rule in process.md §3).

    **A requirement states the system, not its own history.** A reader — human,
    agent, or a downstream adopter with none of this project's history — must read
    one row and know what the system does and why, without resolving a work item
    they cannot see. Both facts have better homes: which WI delivered or amended a
    row lives in `work-items.csv` and the log, why it was decided that way lives in
    the log's Decisions, and the row OBEYS the process rather than citing it.

    Applied to every SPINE registry, not just the SR. The rule shipped SR-only and
    that was the wrong scope: measured across the whole spine afterwards, 2 SRs
    carried a WI id in their normative text — and **26 LLRs, 8 TCs and 9 more SR
    Title/Rationale cells did too**, none of them watched. The largest pocket was
    the layer the SR-only rule could not see, and it kept growing while the rule
    was green (an `LLR` written the same week the lint landed carried three).

    Narrow BY MEASUREMENT, not by taste. It flags exactly two token shapes. A
    SCRIPT name (65 SR rows), an ARTIFACT PATH (6) and a RUBRIC (5) are NOT
    flagged and must never be: this kit's product IS its scripts, so the name is
    the system under specification, and for a `Verification=Critique` row the
    rubric is the acceptance instrument. A rule that cries wolf on 65 legitimate
    rows is a rule that gets scrolled past — the `check_doc_refs` lesson.

    GATING under `--strict` (owner ruling 2026-07-27, raised at the first
    re-attestation sitting on finding `LLR-050`'s `WI-316:` changelog prefix). It
    shipped warn-only on the argument that cleaning a `Verified` row flips it
    `Modified` and owes a re-attestation, so the checker should not pick the
    owner's schedule. The counter-argument won and is the stronger one: a warn
    nobody must act on is how 43 rows accumulated, and the whole population was
    cleaned in one pass at the same sitting, so the rule now guards zero-to-zero
    rather than dictating a cleanup.

    KNOWN COST, accepted deliberately: a WI id is forbidden even where it is the
    DATA rather than a citation — a row describing the dashboard's own rendered
    nodes cannot name one. That case is real (it occurred once, in a measurement
    of which node box a wire grazed) and the row was reworded to describe the node
    instead of naming it, with the specific id kept in the log. A carve-out would
    cost more than it buys: any exemption a checker cannot distinguish from the
    defect is one an author can reach for."""
    out = []
    for rows, (label, key, cols) in zip((srs, llrs, tcs), PROVENANCE_COLS):
        for r in rows:
            rid = (r.get(key) or "").strip()
            if not rid or is_example(rid):
                continue
            for col in cols:
                cell = (r.get(col) or "").strip()
                cited = sorted(set(_WI_TOKEN_RE.findall(cell))) + sorted(
                    {m.group(0).lower() for m in _PROCESS_DOC_RE.finditer(cell)}
                )
                if cited:
                    out.append(
                        "{} {} {} cites {} — a spine row states the system, not "
                        "its own history: move provenance to work-items.csv / "
                        "the log's Decisions, and obey the process rather than "
                        "citing it".format(
                            label, rid, col, ", ".join(repr(c) for c in cited)
                        )
                    )
    return out


def _real(rows, key):
    """The non-placeholder rows of one registry, with their id."""
    for r in rows:
        rid = (r.get(key) or "").strip()
        if rid and not is_example(rid):
            yield rid, r


def form_findings(srs, llrs, tcs):
    """A spine row whose text is not ONE testable obligation (process.md §3).

    The stand-alone rule says a row must not carry its own HISTORY. This says the
    part that is left must be *decidable*: 29148's individual-requirement
    characteristics — singular, unambiguous, verifiable — restricted to the half a
    checker settles without judgement. What it deliberately cannot see is whether
    the requirement is NECESSARY, CORRECT or FEASIBLE; those stay the consistency
    review's, and no proxy metric is offered for them (the readability-score
    refusal, kept).

    Narrow BY MEASUREMENT over all three registries, the discipline the SR-only
    scoping error taught: five of the six patterns fire on 0-1 rows and the sixth
    (one `shall` per requirement) on 13 of 110, so every one of them lands as a
    guard rather than a cleanup schedule. The negative half matters as much: a
    multi-clause `AcceptanceCriteria` is legitimate and untouched — an AC
    enumerates the ways ONE obligation is checked, which is the opposite of a row
    holding two obligations."""
    out = []
    for rid, r in _real(srs, "SR-ID"):
        if is_drafted(r):
            continue
        req = (r.get("Requirement") or "").strip()
        if not req:
            continue
        # MORE than one, never zero. A row with no `shall` is not necessarily
        # wrong — a placeholder, or a project whose obligation keyword is not the
        # English word "shall" — and flagging it would red a legitimate scaffold.
        # The measured defect was two-obligations-in-one-row, and that is what
        # this catches.
        n = len(_SHALL_RE.findall(req))
        if n > 1:
            out.append(
                "SR {} Requirement carries {} 'shall' — one row states one "
                "obligation, or a partial pass has no id to report against: "
                "split it".format(rid, n)
            )
        weak = sorted({w.lower() for w in _MODAL_RE.findall(req)})
        if weak:
            out.append(
                "SR {} Requirement uses {} in normative text — 'shall' is the "
                "obligation; 'should'/'may'/'will' are a goal, a permission and "
                "a statement of fact, and a reader cannot tell which is "
                "binding".format(rid, ", ".join(repr(w) for w in weak))
            )
        passive = _ACTORLESS_RE.search(req)
        if passive:
            out.append(
                "SR {} Requirement says {!r} with no actor — name what performs "
                "it, or the row cannot say who failed".format(rid, passive.group(0))
            )
    for rows, (label, key, cols) in zip((srs, llrs, tcs), PROVENANCE_COLS):
        for rid, r in _real(rows, key):
            # A `Draft` row is pre-ratification and process.md §4 already exempts
            # it from the decomposition rules. "TBD" in a Draft acceptance
            # criterion is what Draft MEANS; flagging it would make the state
            # unusable for the drafting it exists to allow.
            if is_drafted(r):
                continue
            for col in cols:
                cell = (r.get(col) or "").strip()
                for rx, why in (
                    (_VAGUE_RE, "no test can settle it — name the measurable"),
                    (
                        _ESCAPE_RE,
                        "the scope cannot be closed, so the row cannot"
                        " be completed — enumerate it",
                    ),
                ):
                    hits = sorted({h.lower() for h in rx.findall(cell)})
                    if hits:
                        out.append(
                            "{} {} {} uses {} — {}".format(
                                label,
                                rid,
                                col,
                                ", ".join(repr(h) for h in hits),
                                why,
                            )
                        )
                if label == "LLR" and col == "Detail" and _SHALL_RE.search(cell):
                    out.append(
                        "LLR {} Detail uses 'shall' — the SR states the "
                        "obligation and the LLR decomposes it; a 'shall' here is "
                        "either a restatement of the parent or a requirement "
                        "hiding a tier below where it is traced".format(rid)
                    )
    return out


def paraphrase_advisories(srs, llrs):
    """Warn-only: a child cell that mostly RE-WORDS its parent (process.md §3
    'decompose, don't paraphrase'). Lexical overlap is a heuristic and is labelled
    as one — it never gates. Measured at 38 of 118 LLRs, which is exactly why: a
    short `Detail` legitimately shares vocabulary with the SR it decomposes, so a
    gating version would cry wolf on correct rows and get scrolled past."""
    out = []

    def words(s):
        return {w for w in re.findall(r"[a-z_]{4,}", (s or "").lower())}

    for rid, r in _real(srs, "SR-ID"):
        req, rat = words(r.get("Requirement")), words(r.get("Rationale"))
        if rat and len(req & rat) / len(rat) > 0.55:
            out.append(
                "SR {} Rationale mostly re-words its own Requirement — a "
                "rationale says WHY the requirement exists (what breaks without "
                "it, which alternative lost), not what it says again".format(rid)
            )
    by_id = {rid: r for rid, r in _real(srs, "SR-ID")}
    for rid, r in _real(llrs, "LLR-ID"):
        det = words(r.get("Detail"))
        for p in refs(r.get("SR-Refs")):
            parent = by_id.get(p)
            if parent and det:
                req = words(parent.get("Requirement"))
                if len(req & det) / len(det) > 0.6:
                    out.append(
                        "LLR {} Detail mostly re-words {} — a child adds "
                        "detail (module, mechanism, the decomposition choice); "
                        "if it would repeat the parent, link instead".format(rid, p)
                    )
                    break
    return out
