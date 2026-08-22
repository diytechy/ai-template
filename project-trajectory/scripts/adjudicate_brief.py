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
     turns into an immutable per-close report plus a `blockref` — a durable
     record, not a line in a terminal buffer. A row that declares NO brief is
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

THREE OF THE FOUR BRIEFS ARE ROUTED (`ROUTED`); the last has no producer for
its evidence, so a row declaring it is HELD for a human (rule 3) rather than
built:

  * `conflict` — nothing mints a queue-conflict adjudication row at all
    (`check_trajectory.queue_conflict_findings` is a warn that never becomes a
    row), so there is no session to brief; and its `{digests}` slot names a
    scope+spine digest pair no function computes.
  * `conflict`'s sibling `amendment` USED to be the second one, and it is the
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

Contracts: IF-113, IF-114, IF-115, IF-124, IF-127 — the interface seams this
module declares (process.md §8; rows of record in
docs/requirements/interfaces.toml). Four are CONSUMED sides: IF-113 is the
prompt loader whose strict fill becomes this module's refusal (the provider side
is IF-097), IF-114 is the spine carrier the red-TC evidence is read through,
IF-124 is the `last_approved` baseline (IF-123) this module measures an
amendment against, and IF-127 is the re-attestation MODEL read lazily through
`trace` so the brief and the document the owner signs are one traversal rather
than two that could disagree. IF-115 is what this module PROVIDES to
`agent_loop.session_body`, its one caller — and the half of that contract the
CALLER owes is the fail-closed rule: a row declaring a brief this seam cannot
compose is held for a human, never dispatched as a build. IF-124/IF-127 were
minted 2026-08-15 (log 2026-08-15h); the IF-127 edge had been undeclared since
before that session.
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
    "disposition": prompts.ADJUDICATE_DISPOSITION,
    "conflict": prompts.ADJUDICATE_CONFLICT,
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
    "disposition": ("OUTCOME", ("COMPLETE", "PARTIAL", "CANCELLED"), ("successors",)),
    "conflict": (
        "OUTCOME",
        ("QUEUE", "QUEUE-WITH-EDGE", "RETURN-TO-DRAFT"),
        ("needs",),
    ),
    "red-tc": ("OUTCOME", ("DRAFTED", "NEEDS-JUDGEMENT"), ("cases", "drafts")),
}


def declared_brief(row):
    """The row's declared `Brief` cell, normalized; `""` when it declares none."""
    return (row.get("Brief") or "").strip().lower()


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
    """`({baseline, rows}, None)` for a spine row whose ratified text moved after
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

    `{rows}` is `trace.reattest_model`'s RATIFIED cells — the same model behind
    `trace.py --ratify` and `open-items.html`, so the judge, the brief and the
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
    lines = []
    for entry in model:
        for chain_row in entry["rows"]:
            ratified = chain_row.get("ratified") or frozenset()
            cells = [c for c in chain_row["cells"] if c[0] in ratified]
            if not cells:
                continue
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
    return {"baseline": baseline, "rows": "\n".join(lines)}, None


# The briefs whose EVERY slot has a real producer today. A key absent here is
# documented in this module's header with the derivation it is missing; adding
# one is adding its assembler, never relaxing the fill.
_ASSEMBLERS = {
    "amendment": amendment_values,
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
