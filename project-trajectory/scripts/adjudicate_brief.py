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

FOUR OF THE FIVE BRIEFS ARE ROUTED (`ROUTED`); the last has no producer for
its evidence, so a row declaring it is HELD for a human (rule 3) rather than
built:

  * `consolidate` — the fifth brief, which REPLACES the retired `conflict`.
    `conflict` had a template and a verdict grammar and never had any of the
    three things that make a brief real: nothing minted a queue-conflict row
    (`check_trajectory.queue_conflict_findings` is a warn that never became a
    row), no assembler filled its slots, and nothing read the `needs=` field its
    grammar demanded. Its `{digests}` slot named a scope+spine digest pair no
    function computed. `consolidate` keeps its three questions, adds the
    CONSOLIDATE exit, and is minted by a census — so all three are buildable,
    and this entry moves down to `ROUTED` when its assembler lands.
  * `consolidate`'s sibling `amendment` USED to be the second one, and it is the
    capability the `last_approved` snapshot unlocked (D-9 step 4b, owner
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

import agent_common as ac
import baseline_snapshot
import prompts
import spine_carrier

# The declared `Brief` cell -> the prompt key its session is composed from.
BRIEF_PROMPTS = {
    "amendment": prompts.ADJUDICATE_AMENDMENT,
    "first-approval": prompts.ADJUDICATE_FIRST_APPROVAL,
    "disposition": prompts.ADJUDICATE_DISPOSITION,
    "consolidate": prompts.ADJUDICATE_CONSOLIDATE,
    "red-tc": prompts.ADJUDICATE_RED_TC,
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
# `VERDICT: APPROVE|CHANGES-REQUESTED`, which is the review vocabulary. Three
# of these four say `OUTCOME:` and none says `APPROVE`, so reusing it would
# have parsed every adjudication verdict as unreadable.
VERDICT_GRAMMAR = {
    "amendment": ("VERDICT", ("MEANING", "CLARITY"), ("rows",)),
    "first-approval": ("OUTCOME", ("APPROVE", "RETURN"), ("rows",)),
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
    "consolidate": (
        "OUTCOME",
        ("QUEUE", "QUEUE-WITH-EDGE", "RETURN-TO-DRAFT", "CONSOLIDATE"),
        ("needs", "absorbs"),
    ),
    "red-tc": ("OUTCOME", ("DRAFTED", "NEEDS-JUDGEMENT"), ("cases", "drafts")),
}


def declared_brief(row):
    """The row's declared `Brief` cell, normalized; `""` when it declares none."""
    return (row.get("Brief") or "").strip().lower()


def adjudicates(row):
    """The registry row ids this adjudication's act is SCOPED to — the `;`-joined
    `Adjudicates` cell as a set; empty when the row declares none.

    The typed companion to `declared_brief`, and typed for the same reason:
    `Brief` says which judgement is asked for, this says over WHAT, and an
    assembler that re-derives its population live needs both or it re-derives a
    wider question than the mint asked (WI-572 REVIEW-A). Reading it from the
    mint's title or `## Context` prose instead is the WI-417 fold — prose
    carrying control flow — which is why it is a `wi_convert` column."""
    return {
        part.strip()
        for part in (row.get("Adjudicates") or "").split(";")
        if part.strip()
    }


def verdict_refusal(brief, verdict_path):
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
    not something a human can act on at 3am."""
    keyword, labels, counters = VERDICT_GRAMMAR.get(brief, (None, (), ()))
    if keyword is None:
        return "unknown brief {!r} — no verdict grammar".format(brief)
    text = _read(verdict_path) if verdict_path else None
    if text is None:
        return "no verdict was written to {}".format(verdict_path or "(no path)")
    matched = re.search(r"^\s*{}:\s*(\S+)(.*)$".format(keyword), text, re.M)
    if matched is None:
        return "{} carries no `{}:` machine line".format(verdict_path, keyword)
    label, rest = matched.group(1).strip(), matched.group(2)
    if label not in labels:
        return "{} says `{}: {}` — not one of {}".format(
            verdict_path, keyword, label, "|".join(labels)
        )
    missing = [c for c in counters if not re.search(r"\b{}\s*=\s*\S+".format(c), rest)]
    if missing:
        return "{} says `{}: {}` but omits {}".format(
            verdict_path, keyword, label, ", ".join(missing)
        )
    return None


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
    one would ask the judge to rule on an absence."""
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
    evidence is missing"."""
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


# --- the amendment brief (SN-029; routed at D-9 step 4b) ----------------------


def amendment_values(root, row):
    """`({baseline, rows}, None)` for a spine row whose approved text moved after
    it was approved, or `(None, reason)`.

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
    question the ruling already answers.

    NO SNAPSHOT IS A HOLD, AND IT SAYS WHY. A repo that has never signed has no
    accepted anchor at all, so "did this amendment change the meaning?" is not
    the question its rows pose — a FIRST APPROVAL is. Refusing names that
    exactly, rather than fabricating an anchor (rule 1) or rendering a
    before/after with an empty before (rule 2). The stamp itself is advisory:
    off git, or before the snapshot's own commit lands, it is empty and the
    baseline line simply omits the date."""
    import trace as tr

    root = Path(root)
    if not baseline_snapshot.exists(root):
        return None, (
            "no {} snapshot exists yet, so nothing has been approved — every row "
            "here poses a FIRST-APPROVAL question rather than a "
            "meaning-or-clarity one, and there is no accepted anchor to measure "
            "an amendment against".format(baseline_snapshot.SNAPSHOT_DIR)
        )
    reg = tr.load_registries(root / "docs")
    model = tr.reattest_model(root, reg.srs, reg.llrs, reg.tcs)
    if not model:
        return None, (
            "no spine row differs from its {} copy and none awaits a first "
            "approval — there is nothing to judge".format(
                baseline_snapshot.SNAPSHOT_DIR
            )
        )
    stamp_rev, stamp_date = baseline_snapshot.stamp(root)
    baseline = (
        "{}{} — the approved text as a human last blessed it. This is the text "
        "BEFORE the change below; it is not the change under judgement, and it "
        "could only have been written by copying a live registry in an approval "
        "commit.".format(
            baseline_snapshot.SNAPSHOT_DIR,
            ", copied {} (commit {})".format(stamp_date, stamp_rev)
            if stamp_rev
            else " (not yet committed, so no copy stamp)",
        )
    )
    lines, tiers = [], set()
    for entry in model:
        for chain_row in entry["rows"]:
            approved = chain_row.get("approved") or frozenset()
            cells = [c for c in chain_row["cells"] if c[0] in approved]
            if not cells:
                continue
            tiers.add(chain_row["kind"])
            lines.append(
                "- {} {} (chain of {})".format(
                    chain_row["kind"], chain_row["id"], entry["id"]
                )
            )
            for name, before, after in cells:
                lines.append("  - {}".format(name))
                lines.append("    - before: {}".format(before or "(empty)"))
                lines.append("    - after: {}".format(after or "(empty)"))
    if not lines:
        return None, (
            "every selected row awaits a FIRST approval or moved only TRACED "
            "cells — neither is a meaning-or-clarity question, so there is no "
            "amendment to rule on"
        )
    return {
        "baseline": baseline,
        "rows": "\n".join(lines),
        "aftermath": _aftermath(root, tiers),
    }, None


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
    """What a MEANING verdict owes NEXT, derived from the declared gate
    authority for the tiers actually shown (owner ruling 2026-09-01).

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
    held, mine = [], []
    for tier in sorted(tiers):
        (mine if _loop_approves(root, tier) else held).append(tier)
    parts = []
    if mine:
        parts.append(
            "THE DIAL FOR THIS ROW: the {} tier(s) sit on a rung the declared "
            "gate authority has RELEASED, so a MEANING verdict on them is "
            "re-attested BY YOU, in this session, in its own reviewed "
            "commit.".format("/".join(mine))
        )
    if held:
        parts.append(
            "THE DIAL FOR THIS ROW: the {} tier(s) sit on a rung the declared "
            "gate authority still HOLDS for a human, so a MEANING verdict on "
            "them stops at your verdict and the signature is the owner's — do "
            "not re-anchor them.".format("/".join(held))
        )
    return "\n\n".join(parts)


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

    mine, drafted_ids = False, set()
    for kind, rid, full in tr.spine_chain(entry["id"], srs, llrs_by_sr, tcs_by_ref):
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


def first_approval_values(root, row):
    """`({chain, baseline, registries}, None)` for the spine rows a lane
    authored `Drafted` and did not approve, or `(None, reason)`.

    THE APPROVAL ACT IS THE ADJUDICATOR'S, on the serial trunk side: a work
    lane's merge is refused if it flips a `Status` or writes the approval
    record (`integrate._approval_act_refusal`), so these rows are waiting on a
    session like the one this brief composes. Two reasons the owner gave.
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
    session remembered to type."""
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
    wi_id = (row.get("WI-ID") or "").strip()
    stamp_rev, stamp_date = baseline_snapshot.stamp(root)
    baseline = (
        "{}{}. Approving these rows moves it for the registries you flip and "
        "for no others (WI-571), so an off-spine census computed against it "
        "survives your act.".format(
            baseline_snapshot.SNAPSHOT_DIR,
            ", copied {} (commit {})".format(stamp_date, stamp_rev)
            if stamp_rev
            else " does not exist yet — your act is this repo's FIRST signing, "
            "and `--seed` is what creates it",
        )
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
    }, None


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


# The briefs whose EVERY slot has a real producer today. A key absent here is
# documented in this module's header with the derivation it is missing; adding
# one is adding its assembler, never relaxing the fill.
_ASSEMBLERS = {
    "amendment": amendment_values,
    "first-approval": first_approval_values,
    "disposition": disposition_values,
    "red-tc": red_tc_values,
}
ROUTED = tuple(sorted(_ASSEMBLERS))


def compose(root, row, verdict_path, prompt_templates=None):
    """`(prompt_text, None)` when this adjudication row's declared brief could
    be filled IN FULL, else `(None, reason)` — on which the caller HOLDS the
    row for a human (rule 3), never quietly downgrading it to a build.

    An operator override wired through `--prompt-map` under the brief's prompt
    key wins over the shipped template, exactly as it does for the reviewer and
    critique briefs; a `PromptError` from either one (an unreadable file, an
    override declaring slots this evidence cannot fill) is a refusal, never a
    partially-filled send."""
    brief = declared_brief(row)
    if not brief:
        return None, "the row declares no `brief`"
    key = BRIEF_PROMPTS.get(brief)
    if key is None:
        return None, "unknown brief {!r} (expected one of {})".format(
            brief, ", ".join(sorted(BRIEF_PROMPTS))
        )
    assembler = _ASSEMBLERS.get(brief)
    if assembler is None:
        return None, (
            "the {} brief has no evidence assembler — its slots have no "
            "producer yet (see adjudicate_brief.py's header)".format(brief)
        )
    values, reason = assembler(root, row)
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
