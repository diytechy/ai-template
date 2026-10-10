#!/usr/bin/env python3
"""adjudicate_brief.py — the EVIDENCE an adjudication session's brief is filled
with, and the rule for when it must not be sent at all.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX).

WHY THIS MODULE EXISTS (SN-026 x SN-032, WI-424). SN-032 moved the loop's
prompts into files and authored four adjudicator briefs; SN-026 gave an
adjudication row its own phase, its own tier and its own cross-family rule. The
seam between them was never built: `agent_loop.route_session` composed EVERY
non-review session from the generic worker template, so an adjudication row
routed to a strong cross-family model and then received an implementer's
instructions. **The judge was briefed as a builder.** This module is the seam.

TWO RULES GOVERN EVERYTHING BELOW, and both are load-bearing.

  1. **A judge's brief never contains the claim under judgement as its
     premise** (`prompts/README.md` §3, the generalized WI-418 finding). Every
     value assembled here is derived from a registry, a git range, or an
     immutable per-close report — never from the judged lane's session notes,
     `docs/status.md`, `docs/log.md`, or a prior verdict. The one place a claim
     appears at all is the disposition brief's `{report}`, which the template
     itself labels as *a claim under judgement, never a premise*, because
     judging that claim is the whole job.

  2. **A half-filled brief is WORSE than the generic prompt.** A brief whose
     evidence section is thin does not fail loudly — it reads as a completed
     investigation that found nothing, which is the most expensive way for this
     machinery to be wrong. So every assembler returns `(values, None)` or
     `(None, reason)`: there is no partial success, no placeholder, no "(none
     found)" filler. A cell the registry never filled refuses; a target with no
     normative text refuses; an empty census refuses.

  3. **A refusal is a HOLD, not a downgrade.** The caller does not fall back to
     the worker assignment — that would put the judge back in the builder's
     chair, and a builder session ends DONE like any other, so the miss would
     be silent. `agent_loop.session_body` returns the reason and
     `route_session` pages (`EXIT_NEEDS_HUMAN`), which `dispatch._lane_close`
     turns into an immutable per-close report and a move to the TERMINAL
     partial/ — a durable record, not a line in a terminal buffer. A row that
     declares NO brief is
     untouched by all of this: that is an adjudication class the kit never
     authored a brief for, not a claim it failed to honour.

WHICH BRIEF: A DECLARED CELL, NOT AN INFERENCE. The row carries `Brief`
(frontmatter `brief`), written by `intake` at the mint because the mint is what
knows which judgement it is asking for. Deriving it from `SpecRef` instead
would cost no schema, and is unsound: `intake._amendment_drafts` sets
`specref` to the amended registry, so an amendment to a TEST-CASE row and a
red-TC census row BOTH read `docs/test/test-cases.toml` — and those two briefs
give contradictory instructions (one forbids touching a registry, the other
asks for a `Status` cell to be judged). Deriving it from the TITLE instead is
the `NEEDS-HUMAN` fold this repo wrote in blood (WI-417): prose that carries
control flow must be a typed field. So it is a typed field.

ALL NINE BRIEFS ARE NOW ROUTED (`ROUTED`), which they were not for most of this
module's life. Two came with WI-841: `done-when`, a lane's own Done-when
change judged in the lane, and `combined`, one lane-checkpoint sitting that
composes the pending amendment, first-approval and done-when briefs. The
newest (WI-865) is `dispute`: a review finding the lane contests, or one at
its third round, ruled by the adjudicator. The two that were unrouted are worth keeping on record, because
each says something about what "routed" costs:

  * `conflict` is RETIRED, not filled. It had a template and a verdict grammar
    and never had any of the three things that make a brief real: nothing minted
    a queue-conflict row (`check_trajectory.queue_conflict_findings` is a warn
    that never became a row), no assembler filled its slots, and nothing read
    the `needs=` field its grammar demanded — its `{digests}` slot named a
    scope+spine digest pair no function computed. `consolidate` replaces it: the
    same three questions, plus the CONSOLIDATE exit and the idle-station census
    that mints it, so all three gaps close together (the 2026-09-02
    backlog-restructure plan §1).
  * `amendment` was the OTHER one, and it is the capability the `last_approved`
    snapshot unlocked (D-9 step 4b, owner
    directive 2026-08-15). Two things blocked it and the snapshot answers both.
    Its `{rows}` slot named `trace.reattest_model`, which selected rows whose
    Status was `Modified`, while `check_trajectory.staged_spine_amendments` —
    the function that MINTS these rows — fires only when the row and its owning
    SR both stayed put: the two populations were disjoint BY CONSTRUCTION, so
    the producer returned nothing. The model now selects on DRIFT, a property of
    two files rather than of a status word, and the two populations become the
    same population. And `{baseline}` asked for "the accepted anchor this diff
    is measured against", which `trace._attested_baseline` — for a row that
    never flipped — resolved to the amendment commit ITSELF, i.e. the text under
    judgement. The snapshot is an accepted anchor that is PROVABLY not the text
    under judgement: the mirror invariant proves it was copied in a reviewed
    approval commit, and nothing but a copy can write it.

Contracts: IF-115 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-115: `compose(root, row, verdict_path, prompt_templates)` returns
    `(text, None)` when the row's brief could be filled IN FULL, else
    `(None, reason)`. The brief is chosen by the row's DECLARED brief cell, not
    inferred from its reference cell, because that inference is ambiguous — two
    different judgements can carry the same reference. ALL-OR-NOTHING is the
    whole contract: every assembler fills its template's slots from a real
    derivation or returns a reason, an operator override that declares slots the
    evidence cannot fill is a refusal too, and the caller therefore never
    receives a partially-filled judge's brief. The reason is named so the caller
    can act on it, and what the caller owes in return is the fail-closed half: a
    row declaring a brief this cannot compose is HELD for a human, never
    dispatched as ordinary work, because a judge briefed as a builder ends its
    session done like any other and the miss is silent.
"""

from __future__ import annotations

import re
from pathlib import Path

import agent_brief
import agent_common as ac
import baseline_snapshot
import consolidate as cons
import prompts
import rejudge
import spine_carrier
from kitlib import dispute as kdispute
from kitlib import done_when as kdone
from kitlib import sitting as ksitting

# The Done-when brief and the combined lane-checkpoint sitting (WI-841).
DONE_WHEN = "done-when"
COMBINED = ksitting.SITTING
# The kinds one combined sitting composes, in section order.
COMBINABLE = ksitting.KINDS
# The contested or repeated review finding (WI-865); its grammar is
# `kitlib.dispute`'s.
DISPUTE = kdispute.BRIEF

# The declared `Brief` cell -> the prompt key its session is composed from.
BRIEF_PROMPTS = {
    "amendment": prompts.ADJUDICATE_AMENDMENT,
    "first-approval": prompts.ADJUDICATE_FIRST_APPROVAL,
    "disposition": prompts.ADJUDICATE_DISPOSITION,
    "consolidate": prompts.ADJUDICATE_CONSOLIDATE,
    "red-tc": prompts.ADJUDICATE_RED_TC,
    rejudge.BRIEF: prompts.ADJUDICATE_REJUDGE,
    DONE_WHEN: prompts.ADJUDICATE_DONE_WHEN,
    COMBINED: prompts.ADJUDICATE_COMBINED,
    DISPUTE: prompts.ADJUDICATE_DISPUTE,
}

# The per-close reports' home (`intake.REPORTS` / `handback.REPORTS`, restated
# rather than imported so this module loads without either sibling).
REPORTS = "docs/handbacks"
TC_REGISTRY = "docs/test/test-cases.toml"
# The TC cells `{tcs}` lists. REQUIRED, every one: the brief's whole method is
# "run the cited evidence and say what you observed", which a row missing its
# Evidence, Method or Expected cannot support — and a dash there reads as
# "checked, not applicable" rather than "the registry never said".
TC_CELLS = ("Verifies", "Status", "Method", "Expected", "Evidence")
SPINE_REGISTRIES = (
    ("docs/requirements/system-requirements.toml", "SR-ID", "Requirement"),
    ("docs/requirements/low-level-requirements.toml", "LLR-ID", "Detail"),
)

# The closed spec a disposition row's SpecRef points at.
_SPEC_WI_RE = re.compile(r"(WI-\d+)-")
# The commit range a per-close report declares, as a typed frontmatter field.
_RANGE_RE = re.compile(r"^[0-9a-fA-F]{4,40}\.\.[0-9a-fA-F]{4,40}$")
# The declared clip on `{evidence}` (adjudicate-disposition dispatcher notes).
EVIDENCE_CLIP = 80


# The TYPED line each brief ends in: (keyword, the closed enum, the counter
# keys). Held HERE, beside the assemblers, because the brief and the verdict it
# demands are ONE contract — a template edit that changes the enum and a
# checker that still expects the old one is the drift this table prevents.
#
# `score_reviews.parse_verdict` deliberately does not serve this: it knows only
# `VERDICT: APPROVE|CHANGES-REQUESTED`, which is the review vocabulary. Five
# of these six say `OUTCOME:`, and the sixth says `VERDICT:` with a word
# outside that pair, so reusing it would have parsed every adjudication verdict
# as unreadable.
VERDICT_GRAMMAR = {
    # The kinds a combined sitting composes, and its own closing line, take
    # their grammar from `kitlib.sitting.GRAMMAR`, the one home the Done-when
    # holds validate a sitting with too (WI-841 round 9).
    "amendment": ksitting.GRAMMAR["amendment"],
    "first-approval": ksitting.GRAMMAR["first-approval"],
    "disposition": ("OUTCOME", ("COMPLETE", "PARTIAL", "CANCELLED"), ("successors",)),
    # The CONSOLIDATION grammar (restructure plan §1.2). Its first three
    # alternatives are the retired `conflict` grammar verbatim; the fourth is
    # the exit that brief lacked, and `absorbs` is the counter that makes it
    # readable — a verdict saying CONSOLIDATE without naming what it absorbed
    # is a judgement the close cannot enact. BOTH counters are required on
    # EVERY alternative, `-` being the honest "none": a counter that appears
    # only on the alternative that uses it lets a session omit it and still
    # parse, which is the silent half-verdict `verdict_refusal` exists to
    # refuse.
    #
    # BOTH ARE `;`-JOINED LISTS AND BOTH ARE RECONCILED. `absorbs=` restates the
    # `## Dispositions` draft's `supersedes`, `needs=` the WAITERS of the
    # `## Consolidation` block's `edges` - and `consolidate.reconcile_refusal`
    # refuses the close on any divergence. `needs=` was spelled singular here
    # and in the template while `edges` was already a list, so a conformant
    # two-edge verdict was refused with no way to write one that passed; the
    # grammar, the brief and the check are ONE fact now (review round 3).
    "consolidate": (
        "OUTCOME",
        ("QUEUE", "QUEUE-WITH-EDGE", "RETURN-TO-DRAFT", "CONSOLIDATE"),
        ("needs", "absorbs"),
    ),
    "red-tc": ("OUTCOME", ("DRAFTED", "NEEDS-JUDGEMENT"), ("cases", "drafts")),
    # The CHECKPOINT RE-JUDGE (SR-215): the session judged the observation case
    # and committed its record, naming the outcome, or the judgment is a
    # person's act and it recorded nothing (`result=-`).
    rejudge.BRIEF: ("OUTCOME", ("RECORDED", "NEEDS-JUDGEMENT"), ("result",)),
    # The DONE-WHEN judgement (WI-841): its own keyword, so the line is found
    # wherever it sits (a combined sitting's section included), and `digest=`
    # binds the verdict to the exact text it judged (`kitlib.done_when`).
    DONE_WHEN: ksitting.GRAMMAR[DONE_WHEN],
    # The COMBINED sitting: one `## <kind>` section per composed kind, each
    # judged by its own grammar, and this closing line naming them all.
    COMBINED: ksitting.GRAMMAR[COMBINED],
    # Not here: the DISPUTE verdict, one `RULING:` line per requested finding
    # rather than one closing line, parsed by `kitlib.dispute.parse`.
}


def declared_brief(row):
    """The row's declared `Brief` cell, normalized; `""` when it declares none.
    The normalization is `kitlib.sitting.declared_brief`'s, which the merge
    reads a claimed row's frontmatter through, so composition and admission
    cannot read one claim two ways (WI-849).

    Implements: SR-146, LLR-167"""
    return ksitting.declared_brief(row.get("Brief"))


def adjudicates(row):
    """The registry row ids this adjudication's act is SCOPED to — the `;`-joined
    `Adjudicates` cell as a set; empty when the row declares none.

    The typed companion to `declared_brief`, and typed for the same reason:
    `Brief` says which judgement is asked for, this says over WHAT, and an
    assembler that re-derives its population live needs both or it re-derives a
    wider question than the mint asked (WI-572 REVIEW-A). Reading it from the
    mint's title or `## Context` prose instead is the WI-417 fold — prose
    carrying control flow — which is why it is a `wi_convert` column. Its
    tokens are `kitlib.sitting.scope_tokens`', the merge's own reading.

    Implements: SR-146, LLR-167"""
    return set(ksitting.scope_tokens(row.get("Adjudicates")))


def verdict_refusal(brief, verdict_path, kinds=None):
    """Why this adjudication's verdict is not acceptable evidence, or None.

    THE SESSION'S OUTPUT IS THE VERDICT FILE, not its commit. A worker session
    is judged DONE from committed `WI:` trailers, and an adjudicator that
    committed anything at all would clear that bar while having ruled on
    nothing — the shape where the machinery reports a judgement was made and no
    judgement exists. So completion is gated on the artifact the brief named,
    carrying the closed-enum line the brief demanded.

    Checked in the order a reader would: is the file there, does it carry the
    line, is the label one of the declared alternatives, are the counters
    present. Every arm names what is wrong, because "the verdict is invalid" is
    not something a human can act on at 3am.

    A COMBINED verdict is judged against `kinds`, the kinds its sitting
    requested (`requested_kinds` of the composed brief): without them it is
    refused, since a verdict naming its own kinds could judge none. A DISPUTE
    verdict is judged the same way against the finding ids its brief
    requested (`kitlib.dispute.parse`)."""
    if brief not in VERDICT_GRAMMAR and brief != DISPUTE:
        return "unknown brief {!r} — no verdict grammar".format(brief)
    text = _read(verdict_path) if verdict_path else None
    if text is None:
        return "no verdict was written to {}".format(verdict_path or "(no path)")
    if brief == DISPUTE:
        return kdispute.parse(text, kinds or (), verdict_path)[1]
    if brief in ksitting.GRAMMAR:
        # The sitting's kinds and the sitting itself go through the ONE
        # parser the Done-when holds consume (WI-841 round 10).
        requested = kinds if brief == COMBINED else (brief,)
        return ksitting.parse(text, brief, requested, verdict_path)[1]
    return _line_refusal(brief, text, verdict_path)


def _line_refusal(brief, text, verdict_path):
    """Why `text` does not carry `brief`'s machine line, or None
    (`kitlib.sitting.line_refusal` over this brief's grammar).

    Implements: SR-146, LLR-167
    """
    return ksitting.line_refusal(VERDICT_GRAMMAR[brief], text, verdict_path)


def requested_kinds(brief_text):
    """The kinds a composed combined brief requested, read off the one
    `SITTING:` line its wrapper template carries: what the verdict is then
    judged against (`verdict_refusal(..., kinds=...)`).

    Implements: SR-232, LLR-310
    """
    return ksitting.named_kinds(brief_text)


def requested_for(brief, prompt):
    """The kinds a call of `brief` requests: a combined brief's, read off its
    composed `SITTING:` line; a dispute's finding ids, read off its composed
    `DISPUTE:` line (`kitlib.dispute.requested_ids`); a single-kind brief's
    own class. What both routes bind beside the verdict before the call
    (WI-841 round 17).

    Implements: SR-232, LLR-310
    """
    if brief == DISPUTE:
        return kdispute.requested_ids(prompt)
    return requested_kinds(prompt) if brief == COMBINED else (brief,)


def bind_pending(verdict_path, brief, prompt, exclusive=False):
    """Bind what this call was asked - its brief and requested kinds, outcome
    `pending` - beside its verdict, through the one writer; the kinds, or ()
    when a combined brief names none (no binding is then written). Both routes
    call it before the call: the coordinator's entry point exclusively at
    reservation, the loop at composition.

    Implements: SR-232, LLR-310
    """
    kinds = requested_for(brief, prompt)
    if kinds:
        ksitting.write_binding(verdict_path, brief, kinds, "pending", exclusive)
    return kinds


def bound_kinds(verdict_path, brief):
    """The kinds the binding beside `verdict_path` records this call
    requested, read back for its outcome; `(brief,)` when none is bound.

    Implements: SR-232, LLR-310
    """
    bound = ksitting.read_requested(_read(ksitting.requested_path(verdict_path)))
    return bound[1] if bound else (brief,)


def record_outcome(root, verdict_path, brief, kinds, call_ok, session):
    """THE one place a route DECIDES and records whether the adjudication it
    ran was ACCEPTED or FAILED, in the verdict's binding, committed in its own
    bookkeeping commit; returns `(outcome, why)`, `why` None when accepted.
    ONE RULE for both routes (the coordinator's entry point and the loop):
    accepted only when the CALL succeeded (`call_ok`: exit 0 within its
    deadline, no reported error - `session_service.call_succeeded`) AND the
    verdict validates against `kinds` (`verdict_refusal`, judged here, so no
    route can skip it). A failed call is recorded failed without its verdict
    being read. The loop's completion consumes this same decision, so a
    failed call keeps its obligation (WI-841 rounds 11-15). `kinds` None reads
    back the request bound beside the verdict (`bound_kinds`, round 17).

    Implements: SR-232, LLR-310
    """
    kinds = bound_kinds(verdict_path, brief) if kinds is None else kinds
    if call_ok:
        why = verdict_refusal(brief, verdict_path, kinds=kinds)
    else:
        why = "the call failed (a non-zero exit, a timeout or a reported error)"
    outcome = "failed" if why else "accepted"
    ksitting.write_binding(verdict_path, brief, kinds, outcome)
    binding = ksitting.requested_path(verdict_path)
    ac.commit_telemetry(root, session, "verdict " + outcome, [binding])
    return outcome, why


def _clip(text, limit):
    """`text` cut to `limit` lines, with the cut STATED — a brief whose caller
    silently truncates is a brief whose author cannot know what was read."""
    lines = (text or "").splitlines()
    if len(lines) <= limit:
        return "\n".join(lines)
    return "\n".join(lines[:limit] + ["… clipped at {} lines".format(limit)])


def _read(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


# --- the disposition brief (SN-031) -------------------------------------------


def disposition_values(root, row):
    """`({report, spec, evidence}, None)` for a `partial`/`cancelled` lane close,
    or `(None, reason)`.

    Every value is typed-cell-derived: `SpecRef` names the closed spec, the
    closed spec's id finds its IMMUTABLE per-close report (the report is the
    event's identity — SR-144), and the report's `commit_range` frontmatter
    field drives the git facts. Nothing here reads the lane's session notes.

    Refuses on the clean-close spot-check arm, which mints no report: the whole
    brief is built around the lane's report, and a disposition brief without
    one would ask the judge to rule on an absence.

    Implements: SR-146, LLR-167
    """
    root = Path(root)
    specref = (row.get("SpecRef") or "").strip()
    if not specref:
        return None, "the row declares no SpecRef, so the closed spec is unknown"
    spec_text = _read(root / specref)
    if not spec_text:
        return None, "the closed spec {} is not readable".format(specref)
    matched = _SPEC_WI_RE.search(Path(specref).name)
    if matched is None:
        return None, "{} does not name a WI id, so its report cannot be found".format(
            specref
        )
    wi_id = matched.group(1)
    # Newest name last, `intake._close_reports`' convention: a second close is
    # a second file, which is why the report can identify the event at all.
    reports = sorted((root / REPORTS).glob(wi_id + "-*.md"))
    if not reports:
        return None, (
            "{} has no per-close report under {}/ — a clean close writes none, "
            "and the disposition brief is built around one".format(wi_id, REPORTS)
        )
    report_text = _read(reports[-1])
    if not report_text:
        return None, "{} is not readable".format(reports[-1])
    span = _report_range(reports[-1])
    if span is None:
        return None, (
            "{} declares no usable `commit_range`, so the commit facts cannot "
            "be derived".format(reports[-1].name)
        )
    evidence = _commit_facts(root, span)
    if evidence is None:
        return None, "the range {} does not resolve in this repository".format(span)
    return {"report": report_text, "spec": spec_text, "evidence": evidence}, None


def _report_range(path):
    """The report's typed `commit_range` field, or None. A TYPED read (the
    module's own TOML parser), never a substring search of the body."""
    try:
        import handback

        meta = handback.read_report(Path(path))
    except Exception:  # a missing sibling is a refusal, not a crash
        meta = None
    span = str((meta or {}).get("commit_range") or "").strip()
    return span if _RANGE_RE.match(span) else None


def _commit_facts(root, span):
    """`git log --oneline` + `--name-status` over the declared range, clipped at
    `EVIDENCE_CLIP` lines. Facts, not narrative — no commit BODIES, so a lane's
    self-assessment cannot ride in through its own commit message."""
    code, log_out = ac.git(root, "log", "--oneline", "--no-decorate", span)
    if code != 0:
        return None
    _code, stat_out = ac.git(root, "diff", "--name-status", span)
    body = "{}\n\n{}".format(log_out.rstrip("\n"), stat_out.rstrip("\n")).strip()
    return _clip(body, EVIDENCE_CLIP) if body else None


# --- the red-TC brief (SN-030 rung 6) -----------------------------------------


def red_tc_values(root, row):
    """`({tcs, spine}, None)` for the idle-frontier census's unverified test
    cases, or `(None, reason)`.

    THE CENSUS IS RE-RUN LIVE, not remembered. `census.red_tc_census` is the
    same producer that minted the row, so re-running it at composition time
    gives the judge the state of the world it is actually ruling on — a row
    whose gap closed between mint and claim refuses here rather than briefing a
    session about a contradiction that no longer exists. It also means the
    brief shows EVERY currently-red case, not only the one line that minted
    this row: the template asks for one drafted row per distinct CAUSE
    precisely because one missing helper often explains several, and the row's
    own line is untyped (it lives inside the Title), so selecting by it would
    be the magic-substring fold.

    `{tcs}` is assembled from the TC registry — id, what it verifies,
    Method/Expected, and the Evidence LOCATION — because the census line alone
    carries none of that. EVERY one of those cells is REQUIRED: a row missing
    one refuses here rather than rendering a dash, because a dash in an
    evidence listing reads as "looked for, not applicable" when the truth is
    "the registry never said". Same for a target whose normative text is
    absent. This is the empty-census refusal applied one level down — the rule
    is not "refuse when there is nothing", it is "refuse when any part of the
    evidence is missing".

    Implements: SR-146, LLR-167
    """
    try:
        import census
    except Exception as exc:  # a stripped-down copy without the sibling
        return None, "the census producer is unavailable ({})".format(exc)
    lines_in = census.red_tc_census(root)
    if not lines_in:
        return None, "the red-TC census is now empty — there is nothing to judge"
    tc_rows = {
        r.get("TC-ID"): r for r in spine_carrier.load(Path(root) / TC_REGISTRY, "TC-ID")
    }
    lines = []
    targets = set()
    for line in lines_in:
        parsed = census.parse_red_tc(line)
        if parsed is None:
            return None, "a census line did not parse: {!r}".format(line)
        tc_id, tc_targets = parsed
        row_cells = tc_rows.get(tc_id)
        if row_cells is None:
            return None, "{} is in the census but not in {}".format(tc_id, TC_REGISTRY)
        targets.update(tc_targets)
        cells = {}
        for name in TC_CELLS:
            value = (row_cells.get(name) or "").strip()
            if not value:
                return None, (
                    "{} has no `{}` cell, so that line of the evidence listing "
                    "would be a placeholder".format(tc_id, name)
                )
            cells[name] = value
        lines.append(
            "- {id} — verifies {Verifies} — Status {Status}\n"
            "  - Method/Expected: {Method} / {Expected}\n"
            "  - Evidence LOCATION (not a result): {Evidence}".format(id=tc_id, **cells)
        )
    spine, missing = _spine_excerpt(root, targets)
    if missing:
        return None, (
            "no normative text for {} — the obligation the case covers would "
            "be a placeholder".format(", ".join(missing))
        )
    return {"tcs": "\n".join(lines), "spine": spine}, None


def _spine_excerpt(root, ids):
    """`([lines], [missing ids])` — `- <id> — <normative text>` for each wanted
    SR/LLR row in registry order, and every wanted id that either does not
    resolve or whose normative cell is empty. Registry-derived; the requirement
    text and nothing around it.

    Missing ids are RETURNED rather than skipped: a target silently dropped
    from the listing is the half-filled brief in its quietest form — the
    section still looks complete."""
    out, found = [], set()
    for rel, id_col, text_col in SPINE_REGISTRIES:
        for cells in spine_carrier.load(Path(root) / rel, id_col):
            rid = (cells.get(id_col) or "").strip()
            if rid in ids and (cells.get(text_col) or "").strip():
                found.add(rid)
                out.append("- {} — {}".format(rid, (cells[text_col]).strip()))
    return "\n".join(out), sorted(set(ids) - found)


# --- the tier questions, composed from one home (WI-854) ----------------------

#: The ONE home of the questions an adjudicator puts to a spine row, per tier,
#: shipped beside the prompt templates and resolved script-relatively as they
#: are, so a brief composes them in a repo with no skills installed. The
#: spine-authoring skill points here and holds no copy.
QUESTIONS_HOME = prompts.PROMPTS / "spine-questions.md"
# The line under each section heading naming the tiers it serves; `*` is every
# tier.
_TIERS_LINE = re.compile(r"<!-- tiers: ([A-Z* ]+) -->")
ANY_TIER = "*"
# The briefs whose `{questions}` slot the home fills; the combined sitting
# composes both, so the home governs it too.
QUESTION_BRIEFS = ("amendment", "first-approval", COMBINED)


def _question_sections(text):
    """`(sections, None)` — each `## ` section of the home as `(tiers, text)`,
    its tiers line dropped — or `([], heading)` naming the first section
    with no tiers line. Text before the first heading is not a section.

    Implements: SR-146, LLR-167"""
    sections = []
    for chunk in re.split(r"(?m)^(?=## )", text)[1:]:
        heading, _, rest = chunk.partition("\n")
        marker, _, body = rest.partition("\n")
        match = _TIERS_LINE.fullmatch(marker.strip())
        if match is None:
            return [], heading
        sections.append((frozenset(match.group(1).split()), heading + "\n" + body))
    return sections, None


def tier_questions(tiers):
    """`(text, None)`: the home's sections serving any of `tiers` (its
    every-tier sections included), in the home's order, or `(None, reason)`.

    NO FALLBACK. An absent or unreadable home, a section with no tiers line,
    or a judged tier no section serves refuses the brief (rule 2): a judge
    handed a brief with its questions missing reads the gap as "nothing to
    ask", and there is no second copy of them to fall back on.

    Implements: SR-146, LLR-167
    """
    path = QUESTIONS_HOME
    try:
        text = Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        return None, "the tier questions' home {} cannot be read: {}".format(path, exc)
    sections, bad = _question_sections(prompts.strip_dispatcher_block(text))
    if bad is not None:
        return (
            None,
            "the tier questions' home {}: section {!r} declares no tiers".format(
                path, bad
            ),
        )
    served = set().union(*(declared for declared, _body in sections))
    missing = [] if ANY_TIER in served else sorted(set(tiers) - served)
    if missing or not sections:
        return None, "the tier questions' home {} declares no questions for {}".format(
            path, ", ".join(missing) or "any tier"
        )
    return "\n\n".join(
        body.rstrip()
        for declared, body in sections
        if ANY_TIER in declared or declared & set(tiers)
    ), None


# --- the amendment brief (SN-029; routed at D-9 step 4b) ----------------------


def amendment_values(root, row):
    """`({baseline, rows, aftermath}, None)` for the spine rows whose approved
    text moved after they were approved, or `(None, reason)`.

    `{baseline}` is the SNAPSHOT STAMP, and the substitution is the whole point
    of this assembler existing. The slot asks for "the accepted anchor this diff
    is measured against"; the old derivation resolved, for a row that never
    flipped, to the amendment commit ITSELF — presenting the text under
    judgement as its own accepted anchor, which is precisely the failure rule 1
    exists to prevent. `docs/archive/last_approved/` is an anchor that is
    provably NOT the text under judgement: the mirror invariant means it can
    only have been written by copying a live registry in a reviewed approval
    commit.

    `{rows}` is `trace.reattest_model`'s APPROVED cells — the same model behind
    `trace.py --approve` and `open-items.html`, so the judge, the brief and the
    owner surface can never show three different diffs. Traced cells are
    deliberately excluded: §A5.1 rules them non-attesting, and a judge asked to
    rule "meaning or clarity" on a re-pointed `Module` cell is being asked a
    question the ruling already answers. The need, assumption and surrogate
    tiers, which that model does not hold, are read beside it from the same
    recorded copy (`_unchained_amended_rows`; OI-100 gap 1, WI-791), so a row
    the widened mint routes is briefed rather than held.

    NO SNAPSHOT IS A HOLD, AND IT SAYS WHY. A repo that has never signed has no
    accepted anchor at all, so "did this amendment change the meaning?" is not
    the question its rows pose — a FIRST APPROVAL is. Refusing names that
    exactly, rather than fabricating an anchor (rule 1) or rendering a
    before/after with an empty before (rule 2). The stamp itself is advisory:
    off git, or before the snapshot's own commit lands, it is empty and the
    baseline line says so rather than naming a date.

    WHICH ROWS IS THE ROW'S OWN `Adjudicates` SCOPE, intersected with the
    model — `first_approval_values`' rule, for its reason. The model is
    REPO-WIDE: it walks every SR, so a brief built from it alone handed each
    amendment row every drifted approved row in the tree, and each verdict had
    to count its own rows by hand and list the rest as excluded (three
    adjudications that each named one row were each handed the same twenty).
    The mint writes the rows it routes into the cell; the live model answers
    for those rows only, so a row re-anchored since the mint drops out and a
    scope with nothing left REFUSES by name. A row with NO scope refuses too:
    reading the empty cell as "everything" is the widening itself.

    THE ANCHOR IS STAMPED PER REGISTRY. A refresh copies only the registries
    its act authorises, so the copies were written at different commits, and
    the directory's newest write named one registry's copy as the provenance of
    all of them. `{baseline}` names, for each registry shown, the commit that
    last wrote ITS copy.

    Implements: SR-146, LLR-167
    """
    import trace as tr

    root = Path(root)
    scope = adjudicates(row)
    if not scope:
        return None, (
            "this amendment adjudication declares no `Adjudicates` scope, so the "
            "rows the merge routed to it are unknown — and an unstated boundary "
            "read as 'every drifted row in the repo' is the widening this cell "
            "exists to make unrepresentable. Re-mint the row, or rule on it by "
            "hand"
        )
    if not baseline_snapshot.exists(root):
        return None, (
            "no {} snapshot exists yet, so nothing has been approved — every row "
            "here poses a FIRST-APPROVAL question rather than a "
            "meaning-or-clarity one, and there is no accepted anchor to measure "
            "an amendment against".format(baseline_snapshot.SNAPSHOT_DIR)
        )
    reg = tr.load_registries(root / "docs")
    model = tr.reattest_model(root, reg.srs, reg.llrs, reg.tcs)
    lines, tiers = _amended_rows(model, scope)
    more, more_tiers = _unchained_amended_rows(root, scope)
    lines, tiers = lines + more, tiers | more_tiers
    if not lines:
        # One refusal for every way the SCOPED population empties, naming the
        # scope: a repo-wide "nothing to judge" beside it would be two answers
        # to one question (`first_approval_values`' rule).
        return None, (
            "none of the {} row(s) this adjudication was minted over ({}) still "
            "carries approved text that differs from its {} copy — re-anchored, "
            "withdrawn or renumbered since the mint, awaiting a FIRST approval, "
            "or moved only TRACED cells — so there is no amendment in its scope "
            "to rule on".format(
                len(scope), ", ".join(sorted(scope)), baseline_snapshot.SNAPSHOT_DIR
            )
        )
    questions, why = tier_questions(tiers)
    if questions is None:
        return None, why
    return {
        "baseline": _amendment_baseline(root, tiers),
        "rows": "\n".join(lines),
        "aftermath": _aftermath(root, tiers),
        "questions": questions,
    }, None


def _amended_rows(model, scope):
    """`(lines, tiers)`: the approved-cell before/after of each drifted row IN
    `scope`, and the spine tiers those rows sit in.

    ONE BLOCK PER ROW, naming every chain it hangs under. The model groups by
    owning SR, so a row with two parents sits in two entries with the same
    cells; rendered per entry, a one-row scope showed its row twice and the
    verdict's `rows=N` could not be counted against the brief."""
    chains, cells_of = {}, {}
    for entry in model:
        for chain_row in entry["rows"]:
            approved = chain_row.get("approved") or frozenset()
            cells = [c for c in chain_row["cells"] if c[0] in approved]
            if chain_row["id"] not in scope or not cells:
                continue
            key = (chain_row["kind"], chain_row["id"])
            chains.setdefault(key, []).append(entry["id"])
            cells_of[key] = cells
    lines = []
    for (kind, rid), sids in chains.items():
        lines.append("- {} {} (chain of {})".format(kind, rid, ", ".join(sids)))
        for name, before, after in cells_of[(kind, rid)]:
            lines.append("  - {}".format(name))
            lines.append("    - before: {}".format(before or "(empty)"))
            lines.append("    - after: {}".format(after or "(empty)"))
    return lines, {kind for kind, _rid in chains}


# The amended tiers the requirement-chain model does not hold (OI-100 gap 1,
# WI-791): the need tier and the assumption registry's two tiers, each
# `(kind, registry, id column)`. The mint routes their amendments since WI-791,
# so the brief must render them or every such row would refuse as "nothing in
# scope" and hold for a human.
_UNCHAINED_TIERS = (
    ("SN", "docs/requirements/stakeholder-needs.toml", "SN-ID"),
    ("DA", "docs/requirements/assumptions.toml", "DA-ID"),
    ("SUR", "docs/requirements/assumptions.toml", "SUR-ID"),
)


def _unchained_amended_rows(root, scope):
    """`(lines, tiers)` for the drifted need, assumption and surrogate rows IN
    `scope`, each rendered like `_amended_rows`' blocks — the approved cells'
    before/after against the recorded copy (`baseline_snapshot.tier_owing`).

    Implements: SR-146, LLR-167"""
    snapshot = baseline_snapshot.load_all(root)
    lines, shown = [], set()
    for kind, rel, id_col in _UNCHAINED_TIERS:
        owing = baseline_snapshot.tier_owing(root, [(rel, id_col)], snapshot)
        for rid, why, cells, _row in owing:
            if rid not in scope or why != "DRIFTED":
                continue
            shown.add(kind)
            lines.append("- {} {}".format(kind, rid))
            for name, before, after in cells:
                lines.append("  - {}".format(name))
                lines.append("    - before: {}".format(before or "(empty)"))
                lines.append("    - after: {}".format(after or "(empty)"))
    return lines, shown


def _amendment_baseline(root, tiers):
    """`{baseline}`: the snapshot as the accepted anchor, with the commit that
    last wrote the copy of EACH registry the listing shows — the provenance of
    the text actually under judgement, in spine order."""
    rels = list(dict.fromkeys(r for tier, r in _REGISTRY_OF.items() if tier in tiers))
    return (
        "{} — the approved text as a human last blessed it, each registry's copy "
        "as last written:\n{}\nThis is the text BEFORE the change below; it is "
        "not the change under judgement, and it could only have been written by "
        "copying a live registry in an approval commit.".format(
            baseline_snapshot.SNAPSHOT_DIR, _copy_stamp_lines(root, rels)
        )
    )


def _copy_stamp_lines(root, rels):
    """One `  - <registry>: copied <date> (commit <rev>)` line per registry in
    `rels`, each naming the commit that last wrote THAT registry's copy — a
    refresh copies only what its act authorises, so the directory's newest
    write is one copy's provenance, not every copy's.

    Implements: SR-146, LLR-273"""
    lines = []
    for rel in rels:
        rev, date = baseline_snapshot.stamp(root, rel)
        lines.append(
            "  - {}: {}".format(
                rel,
                "copied {} (commit {})".format(date, rev)
                if rev
                else "not yet committed, so no copy stamp",
            )
        )
    return "\n".join(lines)


# The spine tier a chain row's `kind` names -> the registry it lives in. The
# ONE join this module owns: a rendered chain row carries its tier, and both
# questions asked of it downstream — "is this tier's approval mine or the
# owner's" (`agent_common.human_approves_spine`, keyed by registry stem) and
# "what `--approves` argument does the act owe" (keyed by registry path) — are
# registry-keyed. A second, tier-keyed rung table lived here until WI-572's
# rework; it answered the same question as `agent_common.SPINE_APPROVAL_RUNGS`
# and was wired into only ONE of the two briefs that needed it.
_REGISTRY_OF = {
    "SR": "docs/requirements/system-requirements.toml",
    "LLR": "docs/requirements/low-level-requirements.toml",
    "TC": TC_REGISTRY,
    # The amendment brief's unchained tiers (OI-100, WI-791). Only the
    # amendment arm ever renders these kinds; a first-approval chain holds
    # SR, LLR and TC rows alone.
    **{kind: rel for kind, rel, _col in _UNCHAINED_TIERS},
}


def _loop_approves(root, kind):
    """Is a `Drafted` row of spine tier `kind` THIS session's to approve?

    The one place this module turns a rendered chain row's tier into the dial's
    answer. An unrecognised tier has no registry, so it is HELD — the same
    direction `human_approves_spine` fails an unmapped one."""
    registry = _REGISTRY_OF.get(kind)
    if registry is None:
        return False
    return not ac.human_approves_spine(
        Path(root) / "docs", spine_carrier.stem(registry)
    )


def _aftermath(root, tiers):
    """What each verdict owes NEXT, derived from the declared gate authority for
    the tiers actually shown (owner ruling 2026-09-01) and from ruled decision
    2's one home, `intake.adjudication_action`, as OI-100 amended it
    (2026-10-03, WI-791): on a released rung the session re-attests what it
    rules CLARITY and the MEANING rows it would bless; on a held rung it
    re-attests a CLARITY row naming its verdict, and recommends a MEANING row
    to the owner.

    THIS SLOT REPLACED A SENTENCE THAT HAD GONE FALSE. The template used to end
    "the flip, if one is owed, is the mechanical tool's act, not yours" — true
    when written, and false since OI-45 ruled (b) retired that tool
    (`intake._apply_flips` writes nothing, permanently). A MEANING verdict on a
    loop-held rung therefore ended at a brief nobody was owed, contradicting the
    loop-held doctrine itself.

    DERIVED, NOT LEFT TO THE SESSION. The dial is a repo-level declaration the
    judge would otherwise have to go read and interpret mid-verdict, which is
    the shape that produces a session confidently doing the owner's act. An
    unrecognised tier is reported as HELD, the same direction `human_holds`
    fails."""
    import intake  # ruled decision 2's one home; deferred, a leaf read

    held, mine = [], []
    for tier in sorted(tiers):
        (mine if _loop_approves(root, tier) else held).append(tier)
    parts = []
    if mine:
        parts.append(_RELEASED_AFTERMATH.format("/".join(mine)))
    if held:
        arms = {v: intake.adjudication_action(True, v) for v in ("CLARITY", "MEANING")}
        parts.append(
            _HELD_AFTERMATH.format(
                "/".join(held), _HELD_ARMS[arms["CLARITY"]], _HELD_ARMS[arms["MEANING"]]
            )
        )
    return "\n\n".join(parts)


# The aftermath's wording per dial arm. The ARM each verdict takes on a held
# rung is `intake.adjudication_action`'s answer, read above, never restated.
_RELEASED_AFTERMATH = (
    "THE DIAL FOR THIS ROW: the {} tier(s) sit on a rung the declared gate "
    "authority has RELEASED, so a CLARITY verdict, and a MEANING verdict you "
    "would bless, is re-attested BY YOU, in this session, in its own reviewed "
    "commit: name each such row in `--reattests`."
)
_HELD_AFTERMATH = (
    "THE DIAL FOR THIS ROW: the {} tier(s) sit on a rung the declared gate "
    "authority still HOLDS for a human. A CLARITY verdict on them {}. A MEANING "
    "verdict on them {}."
)
_HELD_ARMS = {
    "reattest": "is re-attested BY YOU as a judgement act, in its own reviewed "
    "commit, naming the verdict that ruled it: `python scripts/intake.py "
    "snapshot --reattests <ROW-ID>[,<ROW-ID>...] --verdict <your verdict "
    "file>`; the act ledger records the verdict and the owner's surface lists "
    "the act for audit",
    "recommend": "stops at your verdict and the signature is the owner's — "
    "recommend it to the owner and do not re-anchor it",
}


# --- the first-approval brief (owner ruling 2026-09-01) -----------------------


def _render_chain(root, entry, scope, srs, llrs_by_sr, tcs_by_ref, registries):
    """One SR chain rendered for the first-approval brief:
    `(lines, has_a_row_of_this_session's, the_Drafted_ids_seen)`.

    Extracted from `first_approval_values` rather than nested in it because the
    per-row judgement is where every rule of this arm lands — the three-way
    intersection, the label that says WHY a row is not yours, and the registry
    the act will name — and the assembler around it is then just "walk the model,
    keep the chains that hold one of mine, refuse if none do". `registries` is
    accumulated through rather than returned so the caller's `--approves` set has
    one home; a chain the caller then DROPS contributes none, because a dropped
    chain has no `yours` row by construction."""
    lines = ["- chain of {} — {}".format(entry["id"], entry.get("title") or "")]
    import trace as tr

    body, mine, drafted_ids = _render_approval_rows(
        root,
        tr.spine_chain(entry["id"], srs, llrs_by_sr, tcs_by_ref),
        scope,
        registries,
    )
    return lines + body, mine, drafted_ids


def _render_approval_rows(root, rows, scope, registries):
    """Apply the same scope and authority to requirement and assumption chains."""
    import trace as tr

    lines, mine, drafted_ids = [], False, set()
    for kind, rid, full in rows:
        drafted = tr.is_drafted(full)
        # THE INTERSECTION, in one expression: `Drafted` (the live model's
        # answer), IN SCOPE (the mint's question) and RELEASED (the dial's).
        # Nothing downstream can promote a row that fails any of the three,
        # because `yours` is what mints both the label and the registry.
        in_scope = rid in scope
        yours = drafted and in_scope and _loop_approves(root, kind)
        if drafted:
            drafted_ids.add(rid)
        lines.append(
            "  - {} {} [{}]".format(kind, rid, _chain_label(drafted, in_scope, yours))
        )
        lines += [
            "    - {}: {}".format(name, str(full[name]).strip())
            for name in sorted(full)
            if str(full[name] or "").strip()
        ]
        if yours:
            mine = True
            # The ROWS each `--approves` token covers, not just that the token
            # is owed. `{registries}` is fixed at composition time while the
            # approve/return split exists only after the verdict, so a mixed
            # batch has to be able to DROP a token whose rows it returned in
            # full — and dropping is only mechanical if the brief says which
            # rows a token stands for. Accumulated through, same as before.
            #
            # A DICT AS AN ORDERED SET, per registry, because this walk visits
            # one row ONCE PER SR CHAIN IT HANGS UNDER: an LLR reachable from
            # two SRs was listed twice when this was a list (driven against
            # this repo's live spine, `LLR-205` under two chains). Chain order
            # is kept — it reads SR, LLR, TC, which is the order the session
            # reads the rows in above.
            registries.setdefault(_REGISTRY_OF[kind], {})[rid] = True
    return lines, mine, drafted_ids


def _assumption_case_chain(root, srs, tcs, cases):
    """Reuse the assumption approval view for observation cases' premises.

    Implements: SR-146, SR-215, LLR-295
    """
    import trace as tr

    ids = sorted(
        {
            ref
            for case in cases
            for ref in re.split(r"[;,\s]+", case.get("Assumption-Refs", ""))
            if ref
        }
    )
    declared = {
        r["DA-ID"]
        for r in spine_carrier.load(Path(root) / tr.ASSUMPTIONS_REL, "DA-ID", False)
    }
    missing = set(ids) - declared
    if missing:
        raise ValueError(
            "no assumption chain for {}".format(", ".join(sorted(missing)))
        )
    return tr.assumption_brief_lines(root, srs, tcs, ids=ids)


def _render_assumption_cases(root, reg, scope, registries):
    """Assumption-only cases bypass the SR forest, retaining its approval rules.

    Implements: SR-146, LLR-295
    """
    cases = [
        case
        for case in reg.tcs
        if case.get("Assumption-Refs")
        and not case.get("Verifies")
        and case["TC-ID"] in scope
    ]
    body, mine, awaiting = _render_approval_rows(
        root, [("TC", case["TC-ID"], case) for case in cases], scope, registries
    )
    if not mine:
        return [], awaiting
    return _assumption_case_chain(root, reg.srs, reg.tcs, cases) + body, awaiting


def first_approval_values(root, row):
    """`({chain, baseline, registries}, None)` for the spine rows a lane
    authored `Drafted` and did not approve, or `(None, reason)`.

    THE APPROVAL ACT IS AN INDEPENDENT ADJUDICATOR'S, in the authoring lane or
    on trunk (owner ruling 6, 2026-10-07): a lane's merge is refused if it
    flips a `Status` or writes the approval record with no accepted verdict
    judging those rows behind it (`integrate._approval_act_refusal`), so rows
    a lane left `Drafted` are waiting on a session like the one this brief
    composes. Two reasons the owner gave.
    CONTEXT: approving means holding the row's WHOLE chain, which one work item
    does not — so `{chain}` is the whole chain, not the changed cells.
    CONCURRENCY: an adjudication lane runs alone, so the act cannot race a
    second one.

    WHICH ROWS IS THE ROW'S OWN `Adjudicates` SCOPE, INTERSECTED with
    `trace.reattest_model`'s `approve` half — the same model behind `trace.py
    --approve` and `open-items.html`, so the judge, the brief and the owner
    surface cannot show three different pictures of one spine. Its `Drafted`
    selector is chain-wide (the OI-61-sitting widening), so a `Drafted` LLR
    under an `Approved` SR is a first approval owed and no drift arm can see it
    — a row below approval has made no claim to fall from.

    BOTH HALVES ARE LOAD-BEARING, and shipping only the second is the WI-572
    REVIEW-A finding this arm was rebuilt around. The model is REPO-WIDE: it
    walks every SR. Re-deriving from it alone gave this brief the whole repo's
    `Drafted` backlog rather than the rows the merge handed over — the mint
    named one row in its title and `## Context`, and the template then told the
    session it held the approval authority for every row shown. Measured here
    before the fix: 4 SR chains, 11 `[AWAITING FIRST APPROVAL]` rows and all
    three spine registries in the derived `--approves` argument, from a mint of
    one row. That contradicts the doctrine this same change wrote (the merge
    "MINTS a first-approval adjudication over the `Drafted` rows the lane handed
    over") and the owner's own concurrency reason for moving the act to trunk:
    the approval snapshot must not move across a workstream. It also
    manufactured owner interrupts — a second merge's adjudication, minted while
    the first was still queued, found nothing left and composed to a rule-3 HOLD.

    SO THE SCOPE IS A FACT THE ROW CARRIES (`wi_convert`'s `Adjudicates`
    column), never one recomputed from the world, and the intersection is taken
    at the CHAIN ROW: a rendered row is this session's only if it is `Drafted`,
    IN SCOPE, and on a rung the dial releases. The wider population is not
    filtered out downstream — it is never constructible, because no code path
    turns a repo-wide `Drafted` row into a `yours` label. A row declaring NO
    scope REFUSES: an empty cell is an unstated boundary, and reading it as
    "everything" is exactly the widening, so it fails toward the human.

    WHAT IS RENDERED is the WHOLE CHAIN of each selected SR, through
    `trace.spine_chain` — NOT the model's own `rows`. That list carries only the
    rows that changed or are `Drafted`, which is the right answer to the
    re-attest brief's question ("what must I re-bless?") and the wrong one to
    this brief's: the settled parent and the passing sibling test ARE the
    evidence that a drafted row belongs where it sits. Rendering the model's
    subset here would have shipped a chain brief with the chain missing —
    plausible-looking, and exactly rule 2's failure.

    STILL RE-COMPUTED LIVE, never simply replayed from the mint
    (`red_tc_values`' rule): the row was minted at a merge, and by the time a
    session claims it another lane may have approved or withdrawn some of those
    rows. A brief replaying the mint's listing would ask the judge to rule on a
    world that no longer exists — so a scope whose rows are all settled REFUSES
    here rather than composing a session whose whole evidence section is stale.
    The scope BOUNDS the question; the live model ANSWERS it.

    AND THE DIAL IS RE-APPLIED TO IT, which is the half the first cut missed
    (WI-572 REVIEW-A). `intake._released_drafted_rows` hands over only the rows
    on a rung the dial RELEASES, and this assembler re-derived the population
    from `reattest_model` — which is dial-blind by design — without putting that
    filter back. At any dial holding a spine rung (every dial above this repo's,
    including the shipped `DevStg-Release` default) the brief therefore rendered
    the owner's HELD rows as this session's to approve and derived a
    `--approves` argument for their registry: a prompt instructing an
    adjudicator to perform a signature the owner owes. So `human_approves_spine`
    is consulted PER CHAIN ROW here, from the same table the mint reads. The
    dial is checked as well as the scope, not instead of it: the mint filtered
    by the dial AT THE MINT, and a dial the owner tightens afterwards must bind
    the act it has not yet authorised.

    AN OUT-OF-SCOPE OR HELD ROW IS STILL SHOWN, and shown as not yours. It is
    the chain — the whole reason the act is the adjudicator's is that the chain
    is what a row must be judged against — but it is labelled, it contributes no
    registry, and an SR whose chain holds no row of this session's at all is
    dropped entirely. If nothing survives, this REFUSES: a brief whose every row
    belongs to the owner or to another act is not this arm's question.

    `{registries}` is the `--approves REGISTRY=REF` argument the approving
    commit owes, derived from the registries the RELEASED rows live in.
    Building it here rather than leaving it to the session is the difference
    between an act that records its own scope and one that names whatever the
    session remembered to type.

    Implements: SR-146, LLR-167
    """
    import trace as tr

    root = Path(root)
    scope = adjudicates(row)
    if not scope:
        return None, (
            "this adjudication row declares no `Adjudicates` scope, so the rows "
            "the merge handed it are unknown — and an unstated boundary read as "
            "'every `Drafted` row in the repo' is the widening this cell exists "
            "to make unrepresentable (WI-572). Re-mint the row, or rule on it by "
            "hand"
        )
    reg = tr.load_registries(root / "docs")
    model = [
        entry
        for entry in tr.reattest_model(root, reg.srs, reg.llrs, reg.tcs)
        if entry.get("kind") == "approve"
    ]
    # No early "the model is empty" return: an empty model is one way the
    # SCOPED population empties, and the refusal below names which of the three
    # filters did it. Two refusals for one state is two answers to one question.
    llrs_by_sr, tcs_by_ref = tr.chain_buckets(reg.llrs, reg.tcs)
    lines, registries, awaiting = [], {}, set()
    for entry in model:
        chain, mine, drafted_here = _render_chain(
            root, entry, scope, reg.srs, llrs_by_sr, tcs_by_ref, registries
        )
        awaiting |= drafted_here
        # An SR whose chain holds no row of this session's is not this session's
        # question — dropped whole rather than rendered as evidence for a
        # verdict it cannot be asked to give.
        if mine:
            lines += chain
    try:
        chain, drafted_here = _render_assumption_cases(root, reg, scope, registries)
    except ValueError as exc:
        return None, str(exc)
    lines += chain
    awaiting |= drafted_here
    if not lines:
        # WHICH of the three filters emptied it, named. "Nothing to rule on" is
        # a HOLD a human then has to diagnose, and the three causes take
        # opposite actions: the rows were ruled on already (drop the row), the
        # owner holds their rung (sign, or move the dial), or the scope names
        # rows this spine no longer has (the mint and the tree disagree).
        live = sorted(scope & awaiting)
        if not live:
            return None, (
                "none of the {} row(s) this adjudication was minted over ({}) is "
                "still awaiting a first approval — they have been ruled on, "
                "withdrawn or renumbered since the mint, so its question no "
                "longer has a subject".format(len(scope), ", ".join(sorted(scope)))
            )
        return None, (
            "every row in this adjudication's scope that still awaits a first "
            "approval ({}) sits on a rung the declared gate authority HOLDS for "
            "a human (`human_approval_through` = {}), so the signature is the "
            "owner's and this arm has nothing to rule on".format(
                ", ".join(live), ac.approval_through(root / "docs")
            )
        )
    questions, why = tier_questions(_judged_tiers(registries))
    if questions is None:
        return None, why
    wi_id = (row.get("WI-ID") or "").strip()
    # Each registry the act would copy, with the commit that last wrote ITS
    # copy rather than the directory's newest write (another registry's copy).
    baseline = (
        "{}, each registry this act copies as last written:\n{}\nApproving "
        "these rows moves it for the registries you flip and for no others "
        "(WI-571), so an off-spine census computed against it survives your "
        "act.".format(
            baseline_snapshot.SNAPSHOT_DIR,
            _copy_stamp_lines(root, sorted(registries)),
        )
        if baseline_snapshot.exists(root)
        else "{} does not exist yet — your act is this repo's FIRST signing, "
        "and `--seed` is what creates it.".format(baseline_snapshot.SNAPSHOT_DIR)
    )
    return {
        "chain": "\n".join(lines),
        "baseline": baseline,
        # No empty fallback: `registries` is non-empty exactly when `lines` is,
        # and an empty `lines` refused above. The placeholder that used to sit
        # here ("(no registry — nothing here is Drafted)") described a state the
        # refusal now makes unreachable — and rendering it would have been rule
        # 2's failure, a `--approves` slot filled with prose.
        "registries": baseline_snapshot.format_approves(
            {rel: wi_id or "this adjudication" for rel in registries}
        ),
        # WHICH ROWS EACH TOKEN COVERS. The argument above is written for an
        # ALL-APPROVE verdict, which the template blesses this session not to
        # give ("a MIXED batch is normal"). Naming a registry whose rows were
        # all returned re-anchors text nobody approved, and the merge slot
        # refuses it as WIDENED — so the drop rule needs the mapping, derived
        # here rather than left to the session to reconstruct from row kinds.
        "approves_rows": "\n".join(
            "    - `{}={}` covers {}".format(
                rel, wi_id or "this adjudication", ", ".join(rids)
            )
            for rel, rids in registries.items()
        ),
        # The questions for the tiers of the rows marked as this session's,
        # from the one home (`tier_questions`).
        "questions": questions,
    }, None


def _judged_tiers(registries):
    """The chain tiers of the rows a first approval marks as this session's:
    the tiers whose registry its `--approves` walk collected.

    Implements: SR-146, LLR-167"""
    return {kind for kind in ("SR", "LLR", "TC") if _REGISTRY_OF[kind] in registries}


def _chain_label(drafted, in_scope, yours):
    """How a rendered chain row is labelled — and WHY it is not this session's
    when it is not.

    Three states, not two, and the reason is the point. A `Drafted` row can fail
    to be yours because the OWNER holds its rung, or because it belongs to
    ANOTHER act's scope, and those are opposite instructions: the first waits
    for a signature, the second is already somebody's. Collapsing them into one
    "HELD FOR THE OWNER" line would have told a session to wait on the owner for
    a row a sibling adjudication is about to rule on — a true label for the
    wrong reason is still a false brief (rule 2)."""
    if not drafted:
        return "approved"
    if yours:
        return "AWAITING FIRST APPROVAL"
    if not in_scope:
        return (
            "AWAITING FIRST APPROVAL - OUTSIDE THIS ACT'S SCOPE, ANOTHER "
            "ADJUDICATION'S ROW; SHOWN AS CHAIN EVIDENCE ONLY"
        )
    return "AWAITING FIRST APPROVAL - HELD FOR THE OWNER, NOT YOURS TO FLIP"


# --- the consolidation brief (the 2026-09-02 restructure plan §1.4) -----------

#: The `{spine}` literal for a cluster that cites no requirement. STATED, never
#: blank: contradiction with the spine is one of the brief's three questions,
#: and a blank section reads as "looked, found nothing" when the truth is
#: "these rows cite nothing to look at". The other two questions still stand,
#: which is why this composes rather than refusing.
NO_SPINE = "(the cluster cites no SR/LLR)"
#: The `{prior}` literal for a repository where no consolidation has closed yet.
#: Same rule, same reason — the slot asks "what did earlier judgements already
#: merge", and "nothing yet" is an answer.
NO_PRIOR = "(no consolidation has absorbed anything in this repository yet)"
#: Clip on one candidate row's rendered spec, so a cluster of six rows with
#: multi-page Contexts cannot produce a brief nobody reads.
CANDIDATE_CLIP = 120
#: Clip on one `{open_rows}` title. A WI title in this repo is routinely a
#: multi-thousand-character paragraph, and 140 is the width the validator's own
#: queue-overlap warn settled on.
TITLE_CLIP = 140
#: The statuses `{open_rows}` lists — the ones a row occupies while it is still
#: somebody's to run.
OPEN_STATUSES = ("draft", "queued", "active", "deferred")


def consolidate_values(root, row):
    """`({candidate, open_rows, spine, mechanical, digests, prior}, None)` for
    the queued cluster an idle-station census handed this judge, or
    `(None, reason)`.

    THE CLUSTER IS THE ROW'S OWN `Adjudicates` CELL, and the population is
    RE-DERIVED LIVE against it — the two halves `first_approval_values` was
    rebuilt around, for the same two reasons. The cell BOUNDS the question (a
    live re-derivation with no scope to intersect asks a wider question than the
    mint asked), and the live read ANSWERS it (`red_tc_values`' rule: brief the
    world the judge is actually in, so a cluster whose overlap dissolved between
    mint and claim refuses rather than briefing a session about a contradiction
    that no longer exists).

    EVERY ROW OF THE CLUSTER OR NONE. A cluster row that has been claimed,
    closed or deleted since the mint makes this refuse by name rather than
    composing a brief over the survivors: the verdict this brief asks for
    ABSORBS rows, and a judge shown four of five rows would draft a successor
    whose `supersedes` silently omits one — which the close cannot detect,
    because the absent row is absent from the verdict too.

    `{digests}` renders BOTH the recorded pair and the pair as it is now. The
    slot's declared purpose is "so a verdict that has gone stale is detectable
    rather than assumed fresh", and a recorded pair alone is not detectable —
    it is a number with nothing to compare against.

    Implements: SR-146, LLR-167
    """
    root = Path(root)
    scope = adjudicates(row)
    if not scope:
        return None, (
            "this consolidation declares no `Adjudicates` scope, so the cluster "
            "the census handed it is unknown — and an unstated boundary read as "
            "'every queued row' would let one verdict absorb the whole backlog. "
            "Re-mint the row, or rule on it by hand"
        )
    recorded = (row.get("Digests") or "").strip()
    if not cons.parse_digests(recorded)[0]:
        return None, (
            "this consolidation carries no usable `Digests` cell, so the queue "
            "state it was minted against is unrecorded — the verdict could not "
            "be told stale from fresh, and the census could not tell that this "
            "state had been judged"
        )
    rows = cons.read_rows(root)
    by_id = {(r.get("WI-ID") or "").strip(): r for r in rows}
    gone = sorted(
        wid for wid in scope if (by_id.get(wid) or {}).get("Status") != cons.QUEUED
    )
    if gone:
        return None, (
            "{} of the cluster is no longer queued — a consolidation absorbs "
            "the rows it is shown, so a brief over the survivors would produce "
            "a verdict that silently drops it".format(", ".join(gone))
        )
    candidate, missing = _candidate_specs(root, sorted(scope))
    if missing:
        return None, "no readable spec for {}".format(", ".join(missing))
    findings = [
        line
        for first, second, line in cons.pair_findings(root, rows)
        if first in scope and second in scope
    ]
    if not findings:
        return None, (
            "the pre-filter now finds no overlap among {} — the cluster this "
            "row was minted over has dissolved, and there is nothing left to "
            "judge".format(";".join(sorted(scope)))
        )
    spine, _absent = _spine_excerpt(root, _cited_spine(root, scope, by_id))
    return {
        "candidate": candidate,
        "open_rows": _other_open_rows(rows, scope),
        "spine": spine or NO_SPINE,
        "mechanical": "\n".join("- " + line for line in findings),
        "digests": "recorded at the mint: {}\nas the tree is now:    {}".format(
            recorded, cons.digests(root, rows)
        ),
        "prior": _prior_lines(cons, rows, cons.spec_bodies(root)),
    }, None


def _candidate_specs(root, ids):
    """`(rendered, [ids with no readable spec])` — each cluster row's whole
    spec, frontmatter and body, under a header naming its id.

    THE WHOLE SPEC, not selected cells: the verdict may quote each absorbed
    row's Done-when into the successor's Context verbatim, and a judge shown a
    summary would paraphrase. Clipped per row, with the clip STATED."""
    out, missing = [], []
    for wid in ids:
        hit = None
        for path in ac.spec_files(Path(root) / "docs/work"):
            if path.name.startswith(wid + "-"):
                hit = path
                break
        text = _read(hit) if hit else None
        if not text:
            missing.append(wid)
            continue
        out.append(
            "=== {} ({}) ===\n{}".format(wid, hit.name, _clip(text, CANDIDATE_CLIP))
        )
    return "\n\n".join(out), missing


def _cited_spine(root, scope, by_id):
    """The SR ids the cluster cites, plus the LLR ids hanging under them.

    Read off the rows' own `SR-Refs` cells and the LLR registry's `SR-Refs` —
    the same join `intake._code_map_lines` makes — so `{spine}` shows the
    requirement text a contradiction would be against, at both tiers."""
    srs = set()
    for wid in scope:
        cell = (by_id.get(wid) or {}).get("SR-Refs") or ""
        srs |= {tok.strip() for tok in cell.split(";") if tok.strip()}
    wanted = set(srs)
    for llr in spine_carrier.load(
        Path(root) / "docs/requirements/low-level-requirements.toml", "LLR-ID"
    ):
        owned = {tok.strip() for tok in (llr.get("SR-Refs") or "").split(";")}
        if srs & owned and (llr.get("LLR-ID") or "").strip():
            wanted.add(llr["LLR-ID"].strip())
    return wanted


def _other_open_rows(rows, scope):
    """Every OPEN row that is NOT in the cluster, as id / title / sr_refs /
    needs — the "is this already answered, or does it collide with something
    else" evidence. The cluster itself is `{candidate}` and is not repeated."""
    lines = []
    for r in rows:
        wid = (r.get("WI-ID") or "").strip()
        if wid in scope or (r.get("Status") or "") not in OPEN_STATUSES:
            continue
        title = " ".join(str(r.get("Title") or "(untitled)").split())
        lines.append(
            "- {} — {} — sr_refs {} — needs {}".format(
                wid,
                title if len(title) <= TITLE_CLIP else title[: TITLE_CLIP - 1] + "…",
                (r.get("SR-Refs") or "").strip() or "-",
                (r.get("Predecessors") or "").strip() or "-",
            )
        )
    return "\n".join(sorted(lines))


def _prior_lines(cons, rows, bodies):
    """`{prior}`: what every earlier consolidation absorbed, from the REGISTRY
    (the successors' lineage and the judging rows' recorded verdicts) and never
    from a verdict file - rule 1, a judge's evidence is a record and not a
    claim. Each absorbed row says whether a judgement enacted it or a hand
    commit did (`cons.prior_line`), because the brief's "overturning one pages
    the owner" is true only of the first."""
    prior = cons.prior_absorbs(rows)
    if not prior:
        return NO_PRIOR
    judged = cons.judged_absorbed(rows, bodies)
    return "\n".join(
        cons.prior_line(succ, prior[succ], judged) for succ in sorted(prior)
    )


# --- the checkpoint re-judge brief (SR-215) -----------------------------------

# The case cells `{case}` lists, each REQUIRED: Method and Expected are the
# whole instruction, a dash there would read as "nothing to check", and MaxAge
# is the expiry backstop the cadence floor never overrides.
REJUDGE_CELLS = ("Verifies", "Method", "Expected", "MaxAge")


def rejudge_values(root, row):
    """`({case, reason, tc}, None)` for a re-judge row, or `(None, reason)`.

    THE DECISION IS RE-RUN LIVE (`red_tc_values`' rule). The row's typed
    `Adjudicates` cell names its one case, and `rejudge.due_cases` at HEAD, the
    decision that filed it, says why it is due now; a case re-judged since the
    mint refuses here rather than briefing a session to judge it twice. A case
    declaring no lifetime refuses too, because the observation writer refuses
    to record a result for it, so the session could not finish.

    Implements: SR-215, LLR-255
    """
    scope = sorted(adjudicates(row))
    if len(scope) != 1:
        return None, (
            "a re-judge row names exactly one case in `Adjudicates`; this one "
            "names {}".format(";".join(scope) or "none")
        )
    tc = scope[0]
    try:
        checkpoint = rejudge.checkpoint_for(root, "HEAD", tc)
        due = [
            d
            for d in rejudge.due_cases(root, "HEAD", checkpoint=checkpoint)
            if d["tc"] == tc
        ]
    except rejudge.RejudgeError as exc:
        return None, "the re-judge decision could not be read: {}".format(exc)
    if not due:
        return None, "{} is no longer due for re-judging at HEAD".format(tc)
    try:
        text = _rejudge_case_text(root, tc, due[0]["row"])
    except ValueError as exc:
        return None, str(exc)
    return {"case": text, "reason": rejudge.explain(due[0]), "tc": tc}, None


def _rejudge_case_text(root, tc, case):
    """The observation instruction with its declared requirement or assumption targets.

    Implements: SR-215, LLR-295
    """
    cells = {name: (case.get(name) or "").strip() for name in REJUDGE_CELLS}
    assumption_only = bool(case.get("Assumption-Refs")) and not cells["Verifies"]
    missing = [
        name
        for name, value in cells.items()
        if not value and not (name == "Verifies" and assumption_only)
    ]
    if missing:
        raise ValueError("{} has no `{}` cell".format(tc, "`, `".join(missing)))
    inputs = (case.get("Inputs") or "").strip()
    rubric = (case.get("Rubric") or "").strip()
    text = (
        "- {tc} — {relation} {targets}\n"
        "  - Method: {Method}\n"
        "  - Expected: {Expected}\n"
        "  - Declared inputs: {inputs}\n"
        "  - Rubric: {rubric}\n"
        "  - Result lifetime: {age} days"
    ).format(
        tc=tc,
        relation="observes" if assumption_only else "verifies",
        targets=case["Assumption-Refs"] if assumption_only else cells["Verifies"],
        rubric=rubric or "none declared",
        inputs=inputs or "none declared, so only its expiry makes it due",
        age=case["MaxAge"].strip(),
        **cells,
    )
    chain = []
    if assumption_only:
        import trace as tr

        reg = tr.load_registries(Path(root) / "docs")
        chain = _assumption_case_chain(root, reg.srs, reg.tcs, [case])
    return "\n".join(chain + [text])


# --- the Done-when brief and the combined sitting (WI-841) --------------------

_ACTIVE = "docs/work/active"
_ACTIVE_SPEC_RE = re.compile(r"^docs/work/active/([^/]+)/(WI-\d+)-[^/]*\.md$")


def _subject_claim(root, wi_id):
    """`(claimed text, anchor, branch)` for `wi_id`'s Done-when as claimed;
    the text is None when no claim copy is readable, and the anchor then says
    why.

    In a lane (the spec still under `active/<branch>/` at HEAD) the claim copy
    is read at the lane's integration base, the copy every hold point reads
    (`agent_common.default_base`). After the merge (a closed spec: the
    goalposts row a merge minted) it is the copy the claim commit added, the
    newest commit that added the spec under `active/`.

    Implements: SR-156, LLR-308
    """
    code, listing = ac.git(root, "ls-tree", "-r", "--name-only", "HEAD", _ACTIVE)
    for path in listing.splitlines() if code == 0 else ():
        matched = _ACTIVE_SPEC_RE.match(path)
        if matched and matched.group(2) == wi_id:
            base = ac.default_base(root) or ""
            return _claim_at(root, base, matched.group(1), wi_id, "the lane's base")
    code, added = ac.git(
        root,
        "log",
        "-1",
        "--diff-filter=A",
        "--format=%H",
        "--name-only",
        "HEAD",
        "--",
        "{}/*/{}-*.md".format(_ACTIVE, wi_id),
    )
    lines = added.split() if code == 0 else []
    matched = _ACTIVE_SPEC_RE.match(lines[-1]) if len(lines) >= 2 else None
    if matched is None:
        return None, "no claim of {} under {}/ is readable".format(wi_id, _ACTIVE), None
    return _claim_at(root, lines[0], matched.group(1), wi_id, "the claim commit")


def _claim_at(root, rev, branch, wi_id, what):
    """`(claimed text or None, anchor, branch)` read at `rev`; an absent or an
    unreadable claim (`kdone.claim_copy`) refuses, naming which."""
    claimed, why = kdone.claim_copy(root, rev, branch, wi_id)
    if claimed is None:
        why = why or "no copy of it sits under docs/work/active/{}/".format(branch)
        return (
            None,
            "{}'s claim at {} cannot be briefed: {}".format(wi_id, what, why),
            None,
        )
    return claimed, "the claim copy at {} {}".format(what, rev[:10]), branch


def done_when_values(root, row):
    """`({subject, context, anchor, claimed, current, changes, digest}, None)` for the
    one work item this row's `Adjudicates` cell names, whose Done-when differs
    from the one it was claimed with, or `(None, reason)`.

    Re-derived live from git (`red_tc_values`' rule): a change since blessed
    away, or reverted, refuses rather than briefing a judge on a text that is
    no longer the lane's. The digest is `kitlib.done_when.digest`, the one the
    hold points compute, so the verdict line binds exactly the text shown.

    Implements: SR-156, LLR-308
    """
    scope = sorted(adjudicates(row))
    if len(scope) != 1:
        return None, (
            "a done-when row names exactly one work item in `Adjudicates`; this "
            "one names {}".format(";".join(scope) or "none")
        )
    wi_id = scope[0]
    claimed, anchor, branch = _subject_claim(root, wi_id)
    if claimed is None:
        return None, anchor
    path, current, why = kdone.spec_at(root, "HEAD", branch, wi_id)
    if current is None:
        return None, "{}'s current spec cannot be briefed: {}".format(
            wi_id, why or "no copy of it sits in the tree at HEAD"
        )
    found = kdone.changes(claimed, current)
    if not found:
        return None, (
            "{}'s Done-when at HEAD is the claimed one (ticks and evidence "
            "aside), so there is no change to judge".format(wi_id)
        )
    context = _spec_context(current)
    if context is None:
        return None, (
            "{} at {} carries no `## Context`, so the purpose a Done-when "
            "change is judged against is absent".format(wi_id, path)
        )
    return {
        "subject": "{} — its spec at {}".format(wi_id, path),
        "context": context,
        "anchor": anchor,
        "claimed": _item_lines(claimed),
        "current": _item_lines(current),
        "changes": "\n".join(kdone.describe(found)),
        "digest": kdone.digest(wi_id, claimed, current),
    }, None


_HEADING_RE = re.compile(r"^#{1,2}\s")
_CONTEXT_RE = re.compile(r"^##\s+Context\s*$")


def _spec_context(text):
    """The spec's `## Context` section, clipped at `CANDIDATE_CLIP` lines with
    the cut stated, or None when it has none: the purpose a Done-when change
    is judged against (round 2: a brief without it cannot tell a change that
    keeps the purpose from one that drops part of it).

    Implements: SR-156, LLR-308
    """
    lines, inside = [], False
    for line in (text or "").splitlines():
        if _HEADING_RE.match(line):
            if inside:
                break
            inside = bool(_CONTEXT_RE.match(line))
        elif inside:
            lines.append(line)
    body = "\n".join(lines).strip()
    return _clip(body, CANDIDATE_CLIP) if body else None


def _item_lines(text):
    """A spec's Done-when items, normalized, one `- ` line each."""
    return "\n".join("- " + item for item in kdone.items(text)) or "(no items)"


def _sitting_scopes(row):
    """`({kind: [ids]}, None)` from a combined row's `Adjudicates` tokens,
    each `<kind>:<id>` with a composable kind, or `(None, reason)`.

    Implements: SR-232, LLR-310
    """
    scopes, bad = ksitting.scopes(sorted(adjudicates(row)))
    if bad:
        return None, (
            "combined scope token {!r} is not `<kind>:<id>` with a kind of {}".format(
                bad[0], ", ".join(COMBINABLE)
            )
        )
    if not scopes:
        return None, (
            "this combined sitting declares no `Adjudicates` scope, so the "
            "judgements it composes are unknown"
        )
    return scopes, None


def combined_values(root, row, verdict_path, prompt_templates=None):
    """`({sections, kinds}, None)`: ONE sitting composing every pending in-lane
    judgement its scope names, or `(None, reason)`.

    A COMPOSITION, NOT A FORK. Each section is the kind's own brief, composed
    by `compose` for a row scoped to that kind's ids, its verdict path naming
    its `## <kind>` section of this sitting's one file, so each keeps its own
    grammar, its own acts and its own refusals. ALL OR NOTHING: a section that
    cannot be composed refuses the sitting, naming the kind (rule 2).

    Implements: SR-232, LLR-310
    """
    scopes, reason = _sitting_scopes(row)
    if scopes is None:
        return None, reason
    kinds = [kind for kind in COMBINABLE if kind in scopes]
    sections = []
    for kind in kinds:
        sub = dict(row, Brief=kind, Adjudicates=";".join(scopes[kind]))
        where = "the `## {}` section of {}".format(kind, verdict_path)
        text, why = compose(root, sub, where, prompt_templates)
        if text is None:
            return None, "the {} section: {}".format(kind, why)
        sections.append("=== SECTION `## {}` ===\n\n{}".format(kind, text))
    return {"sections": "\n\n".join(sections), "kinds": ";".join(kinds)}, None


# --- the dispute brief (WI-865) ------------------------------------------------


def dispute_values(root, row):
    """`({range, commits, request, findings, process_doc}, None)` for the one
    findings file this row's `Adjudicates` cell names, or `(None, reason)`.

    The file is the coordinator's (shape: `kitlib.dispute`), and every value
    but the commit facts is a CLAIM the template labels as under judgement:
    the finding as the reviewer wrote it, and the position on it. The range
    it declares is re-derived from git (`_commit_facts`), so a range git
    cannot resolve refuses rather than briefing a judge on nothing.

    Implements: SR-234, LLR-315
    """
    scope = sorted(adjudicates(row))
    if len(scope) != 1:
        return None, (
            "a dispute row names exactly one findings file in `Adjudicates`; "
            "this one names {}".format(";".join(scope) or "none")
        )
    text = _read(Path(root) / scope[0])
    if text is None:
        return None, "the findings file {} cannot be read".format(scope[0])
    found, why = kdispute.read_findings(text, scope[0])
    if found is None:
        return None, why
    span = found["range"]
    if not _RANGE_RE.match(span):
        return None, "the findings file's `range` {!r} is not <base>..<head>".format(
            span
        )
    commits = _commit_facts(root, span)
    if commits is None:
        return None, "git cannot resolve the range {} to any commit".format(span)
    ids = [f["id"] for f in found["findings"]]
    return {
        "range": span,
        "commits": commits,
        "request": kdispute.request_line(ids),
        "findings": "\n".join(_render_finding(f) for f in found["findings"]),
        "process_doc": agent_brief.process_doc_path(root),
    }, None


def _render_finding(finding):
    """One finding's block: its id and who holds the position, then the two
    texts verbatim between labelled delimiters."""
    return (
        "=== FINDING {id} (the position is held by the {held_by}) ===\n"
        "--- as the reviewer wrote it ---\n{finding}\n"
        "--- the {held_by}'s position on it ---\n{position}\n".format(**finding)
    )


# Each shipped brief's assembler, the producer of EVERY slot its template
# declares. The key set equals `BRIEF_PROMPTS`' (the suite pins both
# directions), so shipping a new brief means adding its assembler here, never
# relaxing the fill.
_ASSEMBLERS = {
    "amendment": amendment_values,
    "first-approval": first_approval_values,
    "consolidate": consolidate_values,
    "disposition": disposition_values,
    "red-tc": red_tc_values,
    rejudge.BRIEF: rejudge_values,
    DONE_WHEN: done_when_values,
    # Composes the others, so it is handed the verdict path and the overrides
    # each section's own brief is composed under (`_assemble`).
    COMBINED: combined_values,
    DISPUTE: dispute_values,
}
ROUTED = tuple(sorted(_ASSEMBLERS))


def _assemble(brief, root, row, verdict_path, prompt_templates):
    """The declared brief's assembler, called with what it reads."""
    if brief == COMBINED:
        return combined_values(root, row, verdict_path, prompt_templates)
    return _ASSEMBLERS[brief](root, row)


def governing_templates(classes, prompt_templates=None):
    """`(template_paths, template_texts)`: the identity of the templates the
    brief `classes` are composed from, as the retention layer's governing
    input. Each class contributes the operator's override text when one is
    wired under its prompt key (it wins, as in `compose`), else the shipped
    template's path; a class with no template contributes nothing. Given the
    whole retained set, every call of a retained class shares one identity,
    so switching classes is not a change of rules.

    Implements: SR-227, LLR-305
    """
    paths, texts = [], []
    for brief in sorted(set(classes or ())):
        key = BRIEF_PROMPTS.get(brief)
        override = (prompt_templates or {}).get(key) if key else None
        if override:
            texts.append(override)
        elif key:
            paths.append(prompts.template_path(key))
    # The tier questions' home fills those briefs' `{questions}` slot, so it
    # governs them whether or not their template is overridden.
    if set(classes or ()) & set(QUESTION_BRIEFS):
        paths.append(QUESTIONS_HOME)
    return paths, texts


def compose(root, row, verdict_path, prompt_templates=None):
    """`(prompt_text, None)` when this adjudication row's declared brief could
    be filled IN FULL, else `(None, reason)` — on which the caller HOLDS the
    row for a human (rule 3), never quietly downgrading it to a build.

    An operator override wired through `--prompt-map` under the brief's prompt
    key wins over the shipped template, exactly as it does for the reviewer and
    critique briefs; a `PromptError` from either one (an unreadable file, an
    override declaring slots this evidence cannot fill) is a refusal, never a
    partially-filled send.

    Implements: SR-146, LLR-167
    """
    brief = declared_brief(row)
    if not brief:
        return None, "the row declares no `brief`"
    key = BRIEF_PROMPTS.get(brief)
    if key is None:
        return None, "unknown brief {!r} (expected one of {})".format(
            brief, ", ".join(sorted(BRIEF_PROMPTS))
        )
    values, reason = _assemble(brief, root, row, verdict_path, prompt_templates)
    if values is None:
        return None, "the {} brief cannot be filled: {}".format(brief, reason)
    values["verdict"] = str(verdict_path)
    # The result trailer: a verdict commit without it leaves the row open,
    # because committed trailers are the worker contract's ONLY result channel
    # (`agent_loop.worker_endstate`) and an adjudicator brief is not the worker
    # assignment that would otherwise have carried the protocol.
    values["wi"] = (row.get("WI-ID") or "").strip()
    try:
        base = (prompt_templates or {}).get(key) or prompts.load(key)
        return prompts.fill(key, base, values), None
    except prompts.PromptError as exc:
        return None, str(exc)
