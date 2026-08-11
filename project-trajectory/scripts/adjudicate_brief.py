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
     found)" filler. On a refusal the caller sends the ordinary worker
     assignment and PRINTS the reason — a worse brief, never a wrong one, and
     never a silent swap.

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

TWO OF THE FOUR BRIEFS ARE ROUTED (`ROUTED`), and the other two are left on the
worker assignment on purpose — their evidence has no producer:

  * `conflict` — nothing mints a queue-conflict adjudication row at all
    (`check_trajectory.queue_conflict_findings` is a warn that never becomes a
    row), so there is no session to brief; and its `{digests}` slot names a
    scope+spine digest pair no function computes.
  * `amendment` — its `{rows}` slot names `trace.reattest_model`, which selects
    rows whose Status is `Modified`; but `check_trajectory.staged_spine_amendments`,
    the function that MINTS these rows, fires only when the row and its owning
    SR both stayed `Verified` (the amend-without-flip case). The two populations
    are disjoint by construction, so that producer returns nothing here. Worse,
    `{baseline}` asks for "the accepted anchor this diff is measured against"
    and `trace._attested_baseline` — for a row that never flipped — resolves to
    the amendment commit ITSELF, i.e. the text under judgement. Presenting that
    as the accepted anchor would be the exact failure rule 2 exists to prevent.
    An amendment row still DECLARES `brief = "amendment"`: the declaration is a
    fact about the row, and routing it is one entry in `_ASSEMBLERS` away once
    the anchor question has an answer.

Contracts: consumed by `agent_loop.route_session`; the templates and their
strict fill are `prompts.py`'s (IF-097).
"""

from __future__ import annotations

import re
from pathlib import Path

import agent_common as ac
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


def declared_brief(row):
    """The row's declared `Brief` cell, normalized; `""` when it declares none."""
    return (row.get("Brief") or "").strip().lower()


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

    THE CENSUS IS RE-RUN LIVE, not remembered. `dispatch.red_tc_census` is the
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
    carries none of that."""
    try:
        import dispatch
    except Exception as exc:  # a stripped-down copy without the sibling
        return None, "the census producer is unavailable ({})".format(exc)
    census = dispatch.red_tc_census(root)
    if not census:
        return None, "the red-TC census is now empty — there is nothing to judge"
    tc_rows = {
        r.get("TC-ID"): r for r in spine_carrier.load(Path(root) / TC_REGISTRY, "TC-ID")
    }
    lines = []
    targets = set()
    for line in census:
        parsed = dispatch.parse_red_tc(line)
        if parsed is None:
            return None, "a census line did not parse: {!r}".format(line)
        tc_id, tc_targets = parsed
        row_cells = tc_rows.get(tc_id)
        if row_cells is None:
            return None, "{} is in the census but not in {}".format(tc_id, TC_REGISTRY)
        targets.update(tc_targets)
        lines.append(
            "- {id} — verifies {ver} — Status {st}\n"
            "  - Method/Expected: {method} / {expected}\n"
            "  - Evidence LOCATION (not a result): {ev}".format(
                id=tc_id,
                ver=(row_cells.get("Verifies") or "—").strip() or "—",
                st=(row_cells.get("Status") or "—").strip() or "—",
                method=(row_cells.get("Method") or "—").strip() or "—",
                expected=(row_cells.get("Expected") or "—").strip() or "—",
                ev=(row_cells.get("Evidence") or "—").strip() or "—",
            )
        )
    spine = _spine_excerpt(root, targets)
    if not spine:
        return None, (
            "none of the census's targets ({}) resolve in the spine registries".format(
                ", ".join(sorted(targets)) or "—"
            )
        )
    return {"tcs": "\n".join(lines), "spine": spine}, None


def _spine_excerpt(root, ids):
    """`- <id> — <normative text>` for each wanted SR/LLR row, registry order.
    Registry-derived; the requirement text and nothing around it."""
    out = []
    for rel, id_col, text_col in SPINE_REGISTRIES:
        for cells in spine_carrier.load(Path(root) / rel, id_col):
            rid = (cells.get(id_col) or "").strip()
            if rid in ids:
                out.append(
                    "- {} — {}".format(rid, (cells.get(text_col) or "—").strip() or "—")
                )
    return "\n".join(out)


# The briefs whose EVERY slot has a real producer today. A key absent here is
# documented in this module's header with the derivation it is missing; adding
# one is adding its assembler, never relaxing the fill.
_ASSEMBLERS = {
    "disposition": disposition_values,
    "red-tc": red_tc_values,
}
ROUTED = tuple(sorted(_ASSEMBLERS))


def compose(root, row, verdict_path, prompt_templates=None):
    """`(prompt_text, None)` when this adjudication row's declared brief could
    be filled IN FULL, else `(None, reason)` — the caller then sends the
    ordinary worker assignment and prints the reason.

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
