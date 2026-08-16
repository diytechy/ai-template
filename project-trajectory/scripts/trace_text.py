#!/usr/bin/env python3
"""Spine-row TEXT rules and the row primitives they share (WI-329).

Split out of `trace.py`, which owns the JOIN — this module owns the question
"is this one row readable and decidable on its own?", asked seven ways:

| function                    | tier     | what it catches                        |
|-----------------------------|----------|----------------------------------------|
| `provenance_findings`       | gating   | the row carries its own history        |
| `form_findings`             | gating   | the row is not one testable obligation |
| `paraphrase_advisories`     | advisory | the child re-words its parent          |
| `ac_advisories`             | advisory | a comparative with no named predicate  |
| `sr_artifact_advisories`    | advisory | a requirement cell names an artifact   |
| `sr_fanout_advisories`      | advisory | an SR's direct-LLR fan-out is merged   |
| `if_this_project_advisories`| advisory | an endpoint disagrees with its owner   |

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


# Source-file extensions stripped when normalizing a module path so the two
# module-naming conventions in play align: an LLR `Module` cell carries the full
# repo path with extension (`project-trajectory/scripts/check.py`) while the
# arch-map / an IF endpoint may use the shorter map form (`scripts/check`).
# Normalization strips a leading `project-trajectory/` segment and any one of
# these tails so both collapse to the same key.
MODULE_EXTS = (".py", ".sh", ".ps1", ".ts", ".js", ".go", ".rs", ".cmd")

# The ONE declared way an IF row says "this endpoint is deliberately outside this
# tree" (2026-08-15 interface rework, plan step 2). A controlled PREFIX on the
# endpoint value, not a new column, and the shape was chosen for three reasons a
# column does not have: it needs no schema change so it rides the carrier and the
# CSV fallback unaltered, it reads at the point of use (the cell that is
# unresolvable is the cell that says why), and it cannot drift out of sync with
# the endpoint it qualifies the way a parallel `external = true` flag would.
#
# Before it existed, an external actor and a rotted path were INDISTINGUISHABLE:
# the classifier guessed from spelling — anything without a slash or an extension
# "read as an external actor" — so `docs/subagent-gate` (a real path, dead since
# the policy moved to docs/process.toml) was a finding while `agent CLI` was
# silently fine, and a rot that happened to look like a name would have been
# silently fine too. The marker replaces the guess with a claim someone made.
EXTERNAL_ENDPOINT_PREFIX = "external:"

# MODULE_EXTS, EXTERNAL_ENDPOINT_PREFIX and `norm_module` MOVED HERE FROM trace.py
# at re-tier v2 S5 (WI-464), unchanged: `if_this_project_advisories` below asks the
# same endpoint-vs-module question and is a PURE predicate, so the choice was a
# fourth copy of the normalizer or ONE home in the lower layer. trace.py imports
# all three back — the same direction it already imports `refs`/`is_example`, so no
# cycle — and keeps `_norm_module` as a local alias, leaving its call sites
# untouched. (check_trajectory.py and gen_arch_map.py still carry their own
# copies; consolidating those is the WI-448 common-module program, not this WI.)


def norm_module(path):
    """A module path reduced to a naming-convention-neutral key (see MODULE_EXTS):
    strip a leading `project-trajectory/`, any source extension, and `/__init__`."""
    p = (path or "").strip().replace("\\", "/")
    if p.startswith("project-trajectory/"):
        p = p[len("project-trajectory/") :]
    for ext in MODULE_EXTS:
        if p.endswith(ext):
            p = p[: -len(ext)]
            break
    if p.endswith("/__init__"):
        p = p[: -len("/__init__")]
    return p


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


# --- Re-tier v2 R2/R3: the two warn-first tiering detectors -------------------
# Both are ADVISORY and stay advisory. They report a TIERING smell — a row that
# decided which artifact carries a capability, or a row that merged several
# decisions and grew a fan of children to cover them — and a smell is exactly
# what a human decides. Neither ever joins the exit code under any flag.

# A concrete Python artifact named in a cell: a bare script (`trace.py`) or a
# path-qualified one (`scripts/trace.py`). Anchored on the literal `.py`
# extension with a word boundary each side, so "numpy", "happy" and "occupy" —
# words that merely END in "py" — cannot match: the dot is the whole signal.
_PY_ARTIFACT_RE = re.compile(r"\b[A-Za-z_][\w./-]*\.py\b")

# The recorded per-row waiver marker. The corpus writes it as
# "One-shall waiver (13v): <reason>" (log decision 2026-08-13v — the one-decision
# form rule is a GUIDELINE with recorded per-row waivers), and this reads the
# same token rather than minting a second waiver grammar for authors to learn.
# NOTE: `form_findings` does not itself suppress on this marker — the two
# standing waivers (SR-140, SR-147) are recorded and their findings still fire,
# accepted knowingly. This is the first executable reader of the token.
_WAIVER_RE = re.compile(r"\b13v\b", re.IGNORECASE)

# The declared SR->direct-LLR fan-out bound (re-tier v2 R3). A DIAL of the
# `TOP_VIEW_MAX` family — a declared number the project may re-stamp per row with
# a stated reason — and deliberately NOT a hard cap: a cap on children invites
# merging two LLRs into one to slip under it, which hides the very defect the
# number exists to surface. Measured basis: 48 of 60 SRs have children and 39 of
# those carry <= 5, so 7 sits above the honest population and flags the merged
# rows rather than scheduling a cleanup.
SR_FANOUT_MAX = 7

# The per-row fan-out escape, written in `Rationale` as
# "fan-out re-stamp: <reason>". Matched as a case-insensitive SUBSTRING (not a
# word-boundary token) because the phrase is multi-word and authors punctuate it
# freely.
_FANOUT_RESTAMP = "fan-out re-stamp"


def sr_artifact_advisories(srs):
    """Warn-only: an SR `Requirement` cell that names a concrete artifact
    (re-tier v2 R2, which SUPERSEDES sitting-1 ruling 2.7(a)'s license).

    **The SR tier says what is delivered, not which file delivers it.** A
    requirement that names `trace.py` has decided two things in one row — that
    the capability exists, and that *this artifact* carries it — so the row
    cannot be re-carried without re-writing an obligation, and the binding is
    stated in a tier that has no business holding it. The concrete name has three
    better homes: `AcceptanceCriteria` as rewritable current-carrier evidence
    ("read off the current carrier, as the current set: ..."), the LLR `Module`
    cell (who implements), and the shipped-file inventory (why it ships).

    Two independent censuses, deliberately not folded together:

      * PER ROW — a `*.py` token in `Requirement`, unless the row's `Rationale`
        carries the recorded waiver token (13v). The waiver is the same valve the
        one-`shall` rule declares, not a second grammar.

      * PER ARTIFACT — more than one SR naming the same artifact token, WAIVED
        ROWS INCLUDED. A waiver excuses one row from stating a binding; it says
        nothing about two rows sharing one artifact identity, which is the
        tiering defect R1 names ("one home per method") and a strictly different
        finding. Counting waived rows here is what keeps the second census
        honest.

    PRESENCE ONLY. Whether the surviving wording is genuine capability or
    artifact-CLASS voice is judgement, and stays the consistency review's — this
    reports a token, never a voice. Known and accepted under-detect: identity is
    the token AS WRITTEN, so `trace.py` and `scripts/trace.py` read as two
    artifacts. Warn-only, so an under-detect costs a missed hint, while guessing
    that two spellings mean one file would put a false accusation in the report.
    """
    out = []
    by_artifact = {}
    for rid, r in _real(srs, "SR-ID"):
        req = (r.get("Requirement") or "").strip()
        if not req:
            continue
        named = sorted(set(_PY_ARTIFACT_RE.findall(req)))
        if not named:
            continue
        for token in named:
            by_artifact.setdefault(token, []).append(rid)
        if _WAIVER_RE.search(r.get("Rationale") or ""):
            continue
        out.append(
            "SR {} Requirement names concrete artifact {} — an SR states the "
            "delivered capability or the artifact CLASS ('the delivered "
            "harness', 'the launchers at the repository root'); move the "
            "concrete name to AcceptanceCriteria as current-carrier evidence, "
            "or to the LLR Module cell (process.md §3 'a requirement cell never "
            "names a concrete artifact'; warn-only, never the exit code)".format(
                rid, ", ".join(repr(t) for t in named)
            )
        )
    for token in sorted(by_artifact):
        owners = by_artifact[token]
        if len(owners) > 1:
            out.append(
                "SRs {} all name {!r} in Requirement — two rows sharing one "
                "artifact identity is a tiering defect (one decision per row, "
                "one home per method), not a naming style: decide which row "
                "owns the capability and decompose the rest, or re-carry the "
                "binding at the LLR Module cell (process.md §3; a recorded "
                "waiver excuses a row's own naming, never a shared identity; "
                "warn-only, never the exit code)".format(", ".join(owners), token)
            )
    return out


def sr_fanout_advisories(srs, llrs, bound=SR_FANOUT_MAX):
    """Warn-only: an SR whose DIRECT LLR children outnumber the declared bound
    (re-tier v2 R3, `SR_FANOUT_MAX`).

    A DETECTOR, NOT A CAP. The number does not say "an SR may have at most seven
    children"; it says "a row this many children deep is usually a row that
    merged several decisions", which is R1's defect ("one decision per row, one
    home per method") seen from the child side. Treating it as a cap would be
    actively harmful — the cheapest way under a cap is to merge two LLRs into
    one, which destroys the evidence and leaves the merged SR untouched.

    So the escape is per row and it is a re-stamp, not a suppression list: an
    author who has read the row and judged the fan legitimate writes
    "fan-out re-stamp: <reason>" in `Rationale`, and the reason is the artifact a
    later reader argues with. Bound is a parameter so a downstream project can
    declare its own without editing the rule.

    Counted over the JOIN this module otherwise leaves to `trace.py`, but only
    the trivial half — an LLR's `SR-Refs` naming this SR. No resolution, no
    transitive walk, no filesystem: still a pure row predicate."""
    out = []
    counts = {}
    for _, lr in _real(llrs, "LLR-ID"):
        for parent in refs(lr.get("SR-Refs")):
            counts[parent] = counts.get(parent, 0) + 1
    for rid, r in _real(srs, "SR-ID"):
        n = counts.get(rid, 0)
        if n <= bound:
            continue
        if _FANOUT_RESTAMP in (r.get("Rationale") or "").lower():
            continue
        out.append(
            "SR {} has {} direct LLR children, over the declared bound of {} — "
            "a DETECTOR for a row that merged several decisions, not a cap "
            "(capping children invites merging LLRs to slip under it): split "
            "the row by observable class, or record a per-row 'fan-out "
            "re-stamp: <reason>' in Rationale (process.md §3 'one decision per "
            "row'; warn-only, never the exit code)".format(rid, n, bound)
        )
    return out


# Which endpoint cell the OWNER answers for, by `Direction`. The owner answers for
# the PROVIDING side: on a `Provides` row that side is written in `ThisProject`, on
# a `Consumes` row the providing side is the `Counterpart` (Q2, 2026-08-15 — a
# Consumes row is a COVERAGE declaration written from the consumer's viewpoint, so
# the row's own `ThisProject` is the consumer, not the owner's module). Keyed
# lower-case off the closed `Direction` vocabulary; any other value (blank, or a
# word the enum does not know) resolves to None and the row is skipped, because
# the required-field and enum rules already say what is wrong with it.
_OWNER_SIDE_COLUMN = {"provides": "ThisProject", "consumes": "Counterpart"}


def _module_shaped(endpoint):
    """Is this endpoint a MODULE reference at all — the only class the
    derivability question ranges over?

    Everything else in the endpoint grammar (module-or-path-or-`external:`) is
    wi455's counterpart-TRANSFORM business, not a disagreement: 45 of 122
    counterparts are non-module facts (B2, measured), and reading a data file or a
    named external actor as "the module the owner should have named" would put a
    false accusation in the report for every one of them.

    So: an `external:` claim is out (someone declared it outside this tree), a
    `docs/` path is out (the documentation tree holds no modules), an endpoint
    carrying WHITESPACE is out (`agent CLI`, `downstream adopter` — prose names an
    actor, never a path), and a path whose extension is not a source extension is
    out (`.csv`, `.toml`, `.md`). A path with no extension stays IN, because the
    short arch-map form (`scripts/check_perf`) is spelled exactly that way.

    KNOWN OVER-DETECT, accepted: a bare DIRECTORY endpoint is indistinguishable
    from a short-form module path without touching the filesystem, and this
    predicate is pure. Warn-only, so the cost is one hint to argue with."""
    e = (endpoint or "").strip().replace("\\", "/")
    if not e or e.startswith(EXTERNAL_ENDPOINT_PREFIX) or e.startswith("docs/"):
        return False
    if any(ch.isspace() for ch in e):
        return False
    if "." not in e.rsplit("/", 1)[-1]:
        return True
    return e.endswith(MODULE_EXTS)


def _module_endpoints(cell):
    """The MODULE-shaped endpoints of one `;`-joined endpoint cell.

    Split on `;` ONLY — an endpoint may legitimately contain a space or a comma,
    and reading a multi-endpoint cell as one string is how a real seam gets
    reported as a disagreement (IF-097 names three modules)."""
    parts = (p.strip() for p in (cell or "").split(";"))
    return [p for p in parts if _module_shaped(p)]


def _owner_llr_module(row, modules):
    """``(owner_id, module)`` for a row owned by exactly one LLR, else ``("", "")``.

    Deliberately silent in three cases, each already owned by another rule: an
    `SR-###` owner (the SR tier names no module, so nothing is derivable and
    nothing disagrees), a cell naming zero or several owners
    (`if_ownership_advisories`' "exactly one owner" arm), and an owner id that
    resolves to NO LLR row or to a row with an empty `Module`
    (`if_ownership_advisories` reports the dangling owner by name, and the
    required-field rule reports the empty cell — a second message here would be
    one defect reported twice under two headings)."""
    owners = refs(row.get("Owner"))
    if len(owners) != 1 or not owners[0].startswith("LLR-"):
        return "", ""
    return owners[0], modules.get(owners[0], "")


def if_this_project_advisories(ifs, llrs):
    """Warn-only: an IF row whose OWNER-SIDE endpoint disagrees with the `Module`
    its owner LLR names (re-tier v2 R4, owner ruling 2026-08-15).

    **One endpoint cell is on its way out — but WHICH ONE depends on the row's
    direction, and saying otherwise is how this advisory misread itself.** R4 ruled
    the end-state schema: `owner` stays id-typed and points at the design tier
    wherever a design row exists, and once it does, the endpoint the owner ANSWERS
    FOR is DERIVABLE — owner → LLR → `module` — so THAT cell restates a fact which
    already has a home. One artifact binding, stated once, at the LLR `Module` cell.

    Under the providing-side reading this predicate implements (`_OWNER_SIDE_COLUMN`),
    the derivable cell differs by direction, and only one of the two is
    `ThisProject`:

    * `Provides` — the owner's module IS `ThisProject`, so **`ThisProject` is the
      derivable cell** and `Counterpart` stays as the consumer/coverage fact.
    * `Consumes` — the owning design row is the PROVIDER and its module is written
      in `Counterpart`, so **`Counterpart` is the derivable cell**; `ThisProject`
      here names the CONSUMER, which no derivation reaches and which R4's
      consumers/endpoints list is what carries forward.

    So "drop `ThisProject`" is the whole story only if the owner is read as
    the-module-that-holds-the-code (the IF-031/F6 reading) on every row. That
    question is OPEN and the owner's to rule (log 2026-08-16g flags it); this
    predicate does not presume the answer — it compares whichever endpoint the
    CURRENT reading makes the owner's, and its finding text names that column
    rather than asserting a derivation the compared cell does not support.
    (Corrected 2026-08-16, S6 second top-down read, finding M7: the message
    previously read `Counterpart` on a Consumes row while claiming `this_project`
    was thereby derivable. The comparison was right; the sentence about it was not,
    and it is the sentence a sitting would have signed.)

    Both sides are normalized (`norm_module`), so the arch-map short form and the
    full repo path with its extension read as one module rather than as a
    disagreement, and a `;`-joined cell matches on ANY endpoint — a bundle that
    names the owner's module among several is not misfiled.

    wi455 owns the removal (the schema's existing HELD note names it); this is the
    ADVISORY THAT RUNS FIRST, because a cell cannot be dropped as redundant while
    the two spellings of it still disagree — the disagreement is the one thing a
    derivation cannot survive, and it has to be visible and settled before any
    column goes.

    Warn-only, never the exit code, and permanently so as far as this rule is
    concerned: clearing it means re-pointing owners and correcting endpoints across
    the registry, which is the re-tier campaign's schedule, not the checker's."""
    modules = {rid: (r.get("Module") or "").strip() for rid, r in _real(llrs, "LLR-ID")}
    out = []
    for r in ifs:
        iid = (r.get("IF-ID") or "").strip()
        oid, module = _owner_llr_module(r, modules)
        col = _OWNER_SIDE_COLUMN.get((r.get("Direction") or "").strip().lower())
        if not iid or is_example(iid) or not module or not col:
            continue
        endpoints = _module_endpoints(r.get(col))
        want = norm_module(module)
        if not endpoints or any(norm_module(e) == want for e in endpoints):
            continue
        out.append(
            "IF {} {}={!r} names no module matching owner {}'s LLR Module {!r} — "
            "{} is the endpoint this owner answers for, so it is the cell that "
            "becomes derivable as owner→LLR→module once the two agree, and the "
            "one dropped once it is (re-tier v2 R4; wi455 owns the removal): "
            "re-point Owner at the LLR that implements this endpoint, or correct "
            "the endpoint — a redundant cell can be deleted, a DISAGREEING one "
            "cannot (warn-only, never the exit code)".format(
                iid, col, (r.get(col) or "").strip(), oid, module, col
            )
        )
    return out
