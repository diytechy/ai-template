"""A COMBINED lane-checkpoint sitting: its scope tokens and its verdict sections.

WHY THIS EXISTS (WI-841). A lane can owe several in-lane judgements at one
checkpoint - drifted approved rows (the amendment kind), Drafted rows (the
first-approval kind) and a changed Done-when - and one sitting judges them
all. Its row's `Adjudicates` cell holds `<kind>:<id>` tokens and its verdict
holds one `## <kind>` section per kind. Three readers ask about that shape and
must not disagree: the brief that composes the sitting
(`adjudicate_brief`), the act scopes the merge reads each section's act against
(`acceptance_record`), and the merge-time mint that reads the Done-when
section's own drafts (`intake`). So the token form and the section form have
one home, here, below all three.

Contracts: IF-287 - the seam this module declares (process.md §8; row of
record in docs/requirements/interfaces.toml).

Contract IF-287: a combined sitting's grammar. `SITTING` is the brief class and
    `KINDS` the kinds it composes, in section order; `scopes(tokens)` returns
    `({kind: [ids]}, [malformed tokens])` for `<kind>:<id>` tokens;
    `sections(text)` returns `[(kind, section text)]` in file order for a
    verdict's `## <kind>` headings, `[]` for a single-kind verdict;
    `brief_scope(meta, kind)` is the row ids a claimed row's frontmatter scopes
    to an act of `kind`, a combined row's tokens included; `own_section(text,
    kind, keyword)` is one kind's own part of a verdict, or None when that is
    ambiguous; `GRAMMAR` holds the machine line of each kind it composes
    and its own `SITTING:` line; `parse(text, brief, kinds)` is the ONE
    parser of a verdict file into `{kind: (label, fields)}` (exactly one
    complete machine line per kind; a combined sitting judged against its
    requested kinds), which the coordinator's verdict check and the Done-when
    holds both consume; `requested_path`/`render_requested`/`read_requested`
    are the binding of a sitting's requested kinds beside its verdict;
    `write_binding` is its one writer and `accepted`/`accepted_at` the one
    reader every consumer of a verdict goes through (round 11). Pure functions
    over text, except `write_binding` (one file) and `accepted_at` (git reads).
"""

import re

from .git import git_out
from .verdict import row_rulings

__all__ = [
    "SITTING",
    "KINDS",
    "GRAMMAR",
    "DONE_WHEN_OUTCOMES",
    "scopes",
    "sections",
    "own_section",
    "brief_scope",
    "line_refusal",
    "named_kinds",
    "sitting_refusal",
    "parse",
    "requested_path",
    "render_requested",
    "read_requested",
    "REQUESTED_SUFFIX",
    "OUTCOMES",
    "write_binding",
    "accepted",
    "accepted_part",
    "accepted_at",
    "unaccepted_refusal",
    "REVIEWS",
    "branch_verdicts",
    "uncovered_refusal",
]

SITTING = "combined"
KINDS = ("amendment", "first-approval", "done-when")
# A combined verdict's section heading: a KIND-FORM heading (a lower-case,
# hyphenated brief-class token) alone on its line - any kind, not only the
# composable three, so an unrequested section is seen and refused (round 9).
# Prose headings (`## Dispositions`) are capitalised and never match.
_HEADING_RE = re.compile(r"^## ([a-z][a-z0-9-]*)[ \t]*$", re.M)


def scopes(tokens):
    """`({kind: [ids]}, [malformed tokens])` for a combined row's
    `<kind>:<id>` tokens, a kind being one of `KINDS`.

    Implements: SR-232, LLR-310
    """
    found, bad = {}, []
    for token in tokens:
        kind, sep, rid = str(token).strip().partition(":")
        if sep and kind in KINDS and rid.strip():
            found.setdefault(kind, []).append(rid.strip())
        else:
            bad.append(str(token))
    return found, bad


def sections(text):
    """`[(kind, section text)]` in file order for a combined verdict's
    kind-form `## <kind>` sections (any kind, requested or not), `[]` for a
    verdict that has none; a kind may repeat,
    which the caller refuses as ambiguous.

    Implements: SR-232, LLR-310
    """
    parts = _HEADING_RE.split(text or "")
    return list(zip(parts[1::2], parts[2::2]))


def own_section(text, kind, keyword):
    """`kind`'s own part of a verdict: the whole text for a single-kind
    verdict, its one `## <kind>` section for a combined one; None when that is
    ambiguous - no such section or more than one, or a `<keyword>:` machine
    line under another kind's heading.

    Implements: SR-232, LLR-310
    """
    found = sections(text)
    if not found:
        return text
    own = [body for k, body in found if k == kind]
    stray = [k for k, body in found if k != kind and _keyword_lines(body, keyword)]
    return own[0] if len(own) == 1 and not stray else None


def brief_scope(meta, kind):
    """The row ids a claimed row's frontmatter scopes to an act of `kind`: its
    whole `adjudicates` list for a row of that brief (False when the cell is
    not a list), its `kind:` tokens for a combined sitting, None when it scopes
    nothing to `kind`. The one reader both act scopes go through, so a combined
    sitting's sections each keep their own act (`acceptance_record`).

    Implements: SR-232, LLR-310
    """
    brief, cell = meta.get("brief"), meta.get("adjudicates")
    if brief == kind:
        if not isinstance(cell, list):
            return False
        return [str(rid).strip() for rid in cell if str(rid).strip()]
    if brief != SITTING or not isinstance(cell, list):
        return None
    return scopes(cell)[0].get(kind)


# --- the sitting's verdict grammar and its ONE parser (WI-841 rounds 9, 10) ---
#
# Parse, don't validate: `parse` turns a verdict file into the structured
# verdict every reader consumes - the coordinator's verdict check
# (`adjudicate_brief.verdict_refusal`) and the Done-when holds' covering reader
# (`kitlib.done_when`) - so no reader reads raw machine lines on its own. A
# verdict carries EXACTLY ONE complete machine line per kind, and a combined
# sitting is judged against the kinds its brief REQUESTED, bound beside the
# verdict at reservation (`requested_path`), never against its own claim.
DONE_WHEN_OUTCOMES = ("CLARITY", "BLESSED", "SUCCESSOR")
GRAMMAR = {
    "amendment": ("VERDICT", ("MEANING", "CLARITY"), ("rows",)),
    "first-approval": ("OUTCOME", ("APPROVE", "RETURN"), ("rows",)),
    "done-when": ("DONE-WHEN", DONE_WHEN_OUTCOMES, ("changes", "digest")),
    SITTING: ("SITTING", ("JUDGED",), ("kinds",)),
}
# The binding: a file beside the verdict, written by the entry point at
# reservation, which the adjudicator's rewrite of the verdict cannot touch.
REQUESTED_SUFFIX = ".requested"


def requested_path(verdict_path):
    """The binding file's path for a verdict path.

    Implements: SR-232, LLR-310
    """
    return str(verdict_path) + REQUESTED_SUFFIX


# The OUTCOME a binding records: `pending` from reservation until the route
# that ran the call records `accepted` (its own validation passed) or `failed`.
OUTCOMES = ("pending", "accepted", "failed")


def render_requested(brief, kinds, outcome="pending"):
    """The binding's text: the brief class, the kinds it requested and the
    call's recorded outcome.

    Implements: SR-232, LLR-310
    """
    return "brief = {}\nkinds = {}\noutcome = {}\n".format(
        brief, ";".join(kinds), outcome
    )


def read_requested(text):
    """`(brief, kinds, outcome)` from a binding's text, or None when it is not
    one; a binding recording no outcome reads `pending`.

    Implements: SR-232, LLR-310
    """
    cells = dict(
        line.split(" = ", 1) for line in (text or "").splitlines() if " = " in line
    )
    brief, kinds = cells.get("brief", "").strip(), cells.get("kinds", "").strip()
    if not brief or not kinds:
        return None
    outcome = cells.get("outcome", "pending").strip()
    return brief, tuple(k for k in kinds.split(";") if k), outcome


def line_refusal(grammar, text, where):
    """Why `text` does not carry the machine line `grammar` (keyword, labels,
    fields) declares, or None - the first such line; `parse` is the reader
    that also requires it to be the only one.

    Implements: SR-232, LLR-310
    """
    return _machine_lines(grammar, text, where)[1]


def _keyword_lines(text, keyword):
    """Every PHYSICAL line of `text` whose first token is `keyword:`, as the
    whitespace-split tokens after the colon - complete or not, a bare keyword
    included. Strictly one line at a time: nothing here spans a newline
    (WI-841 round 19), so a label carried onto the next line is a bare keyword
    line followed by prose, never a machine line."""
    out = []
    for line in (text or "").splitlines():
        head, sep, rest = line.strip().partition(":")
        if sep and head == keyword:
            out.append(rest.split())
    return out


def _machine_line(tokens, fields):
    """`(label, {field: value})` for one keyword line's tokens: its first
    token, and each `field=value` token naming a declared field."""
    pairs = (t.partition("=") for t in tokens[1:])
    values = {k: v for k, sep, v in pairs if sep and v and k in fields}
    return (tokens[0] if tokens else ""), values


def _incomplete(grammar, label, values, where):
    """Why one parsed keyword line is not complete, or None."""
    keyword, labels, fields = grammar
    if label not in labels:
        return "{} says `{}: {}` - its label is not one of {}".format(
            where, keyword, label or "(nothing)", "|".join(labels)
        )
    missing = [f for f in fields if f not in values]
    if missing:
        return "{} says `{}: {}` but omits {}".format(
            where, keyword, label, ", ".join(missing)
        )
    return None


def _machine_lines(grammar, text, where):
    """`([(label, {field: value})], refusal)`: every `grammar` keyword line in
    `text` parsed from its own physical line, and why ANY of them is not
    complete (no line at all, a bare keyword, a label outside the enum, or a
    missing `field=value` token), or None."""
    keyword, _labels, fields = grammar
    out = [_machine_line(tokens, fields) for tokens in _keyword_lines(text, keyword)]
    if not out:
        return out, "{} carries no `{}:` machine line".format(where, keyword)
    refusals = (_incomplete(grammar, label, values, where) for label, values in out)
    return out, next((r for r in refusals if r), None)


def _one_line(kind, body, where):
    """`((label, fields), None)` for the ONE complete `kind` machine line in
    `body`, or `(None, refusal)`; a second line of the kind refuses."""
    found, refusal = _machine_lines(GRAMMAR[kind], body, where)
    if refusal:
        return None, refusal
    if len(found) != 1:
        return None, "{} carries {} `{}:` lines; a verdict carries exactly one".format(
            where, len(found), GRAMMAR[kind][0]
        )
    return found[0], None


def named_kinds(text):
    """The kinds a text's `SITTING:` line names, in its order; () when it
    carries no such line or no `kinds=` field. Read off a composed brief, it
    is the kinds the sitting REQUESTED.

    Implements: SR-232, LLR-310
    """
    for tokens in _keyword_lines(text, "SITTING")[:1]:
        pairs = (t.partition("=") for t in tokens[1:])
        named = [v for k, sep, v in pairs if sep and k == "kinds"]
        return tuple(k for k in (named or [""])[0].split(";") if k)
    return ()


def parse(text, brief, kinds, where=""):
    """THE ONE PARSER: `({kind: (label, fields)}, None)` for a valid verdict
    of `brief` requesting `kinds`, or `(None, refusal)`. A single-kind brief's
    verdict carries no kind-form section and exactly one complete machine
    line of its kind. A combined sitting's names exactly the requested kinds
    in its one `SITTING:` line, holds exactly one `## <kind>` section for each
    and no other (an unrequested section refuses), and each section holds
    exactly one complete line of its own kind and none of another's, so one
    invalid section refuses the whole sitting (SR-232).

    Implements: SR-232, LLR-310
    """
    if brief != SITTING and brief not in GRAMMAR:
        return None, "{}: no sitting grammar for brief {!r}".format(where, brief)
    if brief != SITTING:
        if sections(text):
            return (
                None,
                "{}: a single-kind verdict carries no `## <kind>` section".format(
                    where
                ),
            )
        line, why = _one_line(brief, text, where)
        why = why or _keyword_count_refusal(text, {brief: 1}, where)
        return (None, why) if why else ({brief: line}, None)
    return _parse_sitting(text, kinds, where)


def _keyword_count_refusal(text, expected, where):
    """Why `text`'s machine keyword lines are not exactly `expected` -
    `{kind: count}`, every other sitting kind's (and the sitting's own,
    unless named) expected zero - counted per physical line over the WHOLE
    text, complete or not; or None. So a keyword line outside every section,
    or another kind's keyword inside one, invalidates the verdict."""
    for kind, (keyword, _labels, _fields) in GRAMMAR.items():
        found = len(_keyword_lines(text, keyword))
        if found != expected.get(kind, 0):
            return (
                "{} carries {} `{}:` line(s), expected {}: a verdict carries "
                "exactly one complete machine line per kind it judges".format(
                    where, found, keyword, expected.get(kind, 0)
                )
            )
    return None


def _parse_sitting(text, kinds, where):
    """`parse` for a combined sitting judged against requested `kinds`."""
    if not kinds:
        return None, (
            "{}: a combined verdict is judged against the kinds its sitting "
            "requested, and none were given".format(where)
        )
    _line, refusal = _one_line(SITTING, text, where)
    want, named = sorted(set(kinds)), named_kinds(text)
    if refusal or sorted(named) != want:
        return None, refusal or "{} names kinds={} but the sitting requested {}".format(
            where, ";".join(named) or "(none)", ";".join(want)
        )
    found = sections(text)
    headed = sorted(kind for kind, _body in found)
    if headed != want:
        return None, "{} requested {} but carries the section(s) {}".format(
            where, ";".join(want), ", ".join("## " + k for k in headed) or "(none)"
        )
    lines, refusal = _parse_sections(found, where)
    expected = dict.fromkeys([SITTING, *want], 1)
    refusal = refusal or _keyword_count_refusal(text, expected, where)
    return (None, refusal) if refusal else (lines, None)


def _parse_sections(found, where):
    """Each section's one complete own-kind line, none of another kind's."""
    lines = {}
    for kind, body in found:
        at = "{} (## {})".format(where, kind)
        line, refusal = _one_line(kind, body, at) if kind in GRAMMAR else (None, None)
        stray = [
            g[0]
            for k, g in GRAMMAR.items()
            if k not in (kind, SITTING) and _keyword_lines(body, g[0])
        ]
        if refusal or line is None or stray:
            return None, refusal or "{}: carries {} line(s) of another kind".format(
                at, "/".join(stray) or "no sitting grammar for this kind's"
            )
        lines[kind] = line
    return lines, None


def sitting_refusal(text, where, kinds):
    """Why a combined sitting's verdict is not acceptable against its
    requested `kinds`, or None: `parse`'s refusal.

    Implements: SR-232, LLR-310
    """
    return parse(text, SITTING, kinds, where)[1]


# --- acceptance is a RECORDED fact (WI-841 round 11) --------------------------


def write_binding(verdict_path, brief, kinds, outcome, exclusive=False):
    """THE one writer of a verdict's binding: its brief class, requested kinds
    and recorded outcome, beside the verdict. `exclusive` creates it (the
    entry point's reservation, which refuses an existing one); otherwise it
    overwrites, which is how the route that ran the call records `accepted`
    or `failed`. Raises OSError as `open` does; the caller says what it means.

    Implements: SR-232, LLR-310
    """
    mode = "x" if exclusive else "w"
    with open(requested_path(verdict_path), mode, encoding="utf-8", newline="\n") as fh:
        fh.write(render_requested(brief, kinds, outcome))


def accepted(text, binding_text):
    """THE one reader every consumer of a verdict file goes through:
    `{kind: (label, fields, body, rows)}` (`rows`: the part's per-row
    rulings, `kitlib.verdict.row_rulings`) for a verdict whose binding records it
    ACCEPTED by the route that ran the call and which `parse` reads as valid
    against that binding's brief and requested kinds; None for anything else -
    no binding, a pending or failed outcome, an invalid verdict, or a brief
    class this grammar does not cover (which is simply no blessing of these
    kinds, never an error). A verdict's acceptance is the recorded fact, never
    an inference from its text.

    Implements: SR-232, LLR-310
    """
    bound = read_requested(binding_text)
    if not bound or bound[2] != "accepted":
        return None
    brief, kinds, _outcome = bound
    lines, _refusal = parse(text or "", brief, kinds)
    if not lines:
        return None
    bodies = dict(sections(text)) if brief == SITTING else {brief: text}
    return {
        k: (label, fields, bodies.get(k, ""), row_rulings(bodies.get(k, ""), k))
        for k, (label, fields) in lines.items()
    }


def accepted_part(text, binding_text, kind):
    """`kind`'s own text in an accepted verdict (`accepted`), or None.

    Implements: SR-232, LLR-310
    """
    found = accepted(text, binding_text) or {}
    return found[kind][2] if kind in found else None


def accepted_at(root, rev, verdict_path):
    """`accepted` for the verdict file at `verdict_path` and its binding, both
    read at the commit `rev` (None: the index) - the git side of the one
    reader, so no consumer fetches a verdict and decides about it alone.

    Implements: SR-232, LLR-310
    """
    at = "" if rev is None else rev
    texts = [
        git_out(root, ["show", "{}:{}".format(at, rel)])
        for rel in (verdict_path, requested_path(verdict_path))
    ]
    return accepted(*texts) if verdict_path else None


# The rulings that authorize each kind's act on a row: a first approval's
# APPROVE flips it, an amendment's MEANING or CLARITY re-attests it (the
# held-rung CLARITY-only rule is acceptance_record's, on top of this).
_AUTHORIZING = {"first-approval": ("APPROVE",), "amendment": ("MEANING", "CLARITY")}


def judged_rows(parsed):
    """`{(kind, row)}` an accepted parsed verdict (`accepted`) judged in a way
    that authorizes that kind's act on the row.

    Implements: SR-232, LLR-310
    """
    return {
        (kind, rid)
        for kind, part in (parsed or {}).items()
        for rid, ruling in part[3].items()
        if ruling in _AUTHORIZING.get(kind, ())
    }


def _named_line(root, rev, act):
    """The refusal line for one act naming a verdict, or None: the verdict is
    not accepted, or it does not judge a row the act re-attests."""
    verdict = str(act["verdict"]).strip()
    parsed = accepted_at(root, rev, verdict)
    if not parsed:
        return "  {}".format(verdict)
    judged = judged_rows(parsed)
    rows = [str(r) for r in act.get("reattested") or []]
    unjudged = [r for r in rows if ("amendment", r) not in judged]
    if not unjudged:
        return None
    return "  {} (does not judge {})".format(verdict, ", ".join(unjudged))


def unaccepted_refusal(root, rev, acts):
    """Why a merge must refuse the approval acts it adds, or None: EVERY act
    that names a verdict must name one `accepted_at` reads as accepted at
    `rev` AND that judges each row the act re-attests (round 16). An act naming
    no verdict is `uncovered_refusal`'s; acts already on trunk are never
    passed here.

    Implements: SR-232, LLR-310
    """
    named = (a for a in acts if isinstance(a, dict) and a.get("verdict"))
    lines = [line for line in (_named_line(root, rev, act) for act in named) if line]
    if not lines:
        return None
    return (
        "the adjudication's act names a verdict no route recorded ACCEPTED, or "
        "one that does not judge the rows it re-attests; nothing was merged:\n"
        "{}\nRemedy: re-sit the adjudication through the loop or the "
        "coordinator's entry point, which records its outcome beside the "
        "verdict, and name the accepted verdict that judged those rows.".format(
            "\n".join(lines)
        )
    )


# The review records a lane's verdicts and their bindings live under.
REVIEWS = "docs/reviews"
# Which adjudication kind an act-ledger entry's key needs: a flip is a first
# approval's act, a re-attestation an amendment's.
_ACT_KINDS = (("approved", "first-approval"), ("reattested", "amendment"))


def branch_verdicts(root, base, rev):
    """The verdict paths whose bindings the branch changed between `base` and
    `rev` - the adjudications this lane ran, through either route.

    Implements: SR-232, LLR-310
    """
    args = ["diff", "--name-only", "--no-renames", base, rev, "--", REVIEWS]
    changed = (git_out(root, args) or "").splitlines()
    return sorted(
        p[: -len(REQUESTED_SUFFIX)] for p in changed if p.endswith(REQUESTED_SUFFIX)
    )


def uncovered_refusal(root, base, rev, acts):
    """Why a merge must refuse the approval acts it adds, or None, WHETHER OR
    NOT an act names a verdict (WI-841 rounds 14, 16): every ROW an added act
    flips must be ruled APPROVE in a first-approval part, and every row it
    re-attests ruled MEANING or CLARITY in an amendment part, of an ACCEPTED
    verdict (`accepted_at`) among the bindings this branch carries
    (`branch_verdicts`), single-kind or combined. An act's authority is the
    judgement of ITS rows: an accepted verdict over other rows authorizes
    nothing here. Each unjudged row is named with its kind.

    Implements: SR-232, LLR-310
    """
    needed = sorted(
        {
            (kind, str(rid))
            for act in acts
            if isinstance(act, dict)
            for key, kind in _ACT_KINDS
            for rid in act.get(key) or []
        }
    )
    judged = set()
    for verdict in branch_verdicts(root, base, rev) if needed else ():
        judged |= judged_rows(accepted_at(root, rev, verdict))
    missing = [(kind, rid) for kind, rid in needed if (kind, rid) not in judged]
    if not missing:
        return None
    return (
        "the adjudication's act takes rows no ACCEPTED verdict in this branch "
        "judged (an act's authority is the judgement of its own rows, named "
        "or not); nothing was merged:\n{}\nRemedy: re-sit the adjudication of "
        "those rows through the loop or the coordinator's entry point, whose "
        "binding records it accepted.".format(
            "\n".join(
                "  {} ({}) is judged by no accepted verdict".format(r, k)
                for k, r in missing
            )
        )
    )
