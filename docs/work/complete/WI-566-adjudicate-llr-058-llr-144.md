+++
id = "WI-566"
title = "adjudicate: LLR-058, LLR-144, LLR-198, TC-138, TC-147, TC-194 - approved/routed cell(s) amended on merged trunk a024e76..fa92323 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
+++

## Deliverable

Adjudication verdict recorded on the lane; this row is closed MECHANICALLY at its DONE (OI-70/OI-73). The verdict artifact is `docs/reviews/wi-566-adjudicate-llr-058-llr-144/001-ADJUDICATE-05fb6a3.md`, governing line `VERDICT: MEANING rows=6` over LLR-058, LLR-144, LLR-198, TC-138, TC-147, TC-194 (re-issued 2026-09-01 after REVIEW-A finding 1: the first issue said `rows=23`, having re-counted seventeen SR rows WI-547 had already closed as CLARITY; those lines are retained in the file, marked as the WI-547 restatement and excluded from the counter).

**No `## Dispositions` successors are owed, and none are drafted — deliberately, on the record** (REVIEW-A finding 2). All six rows are MEANING, so §A5.2's "flip back to Approved" arm does not apply; but the work a scope-change successor would carry is already DONE, and the human act the amendment owes is already carried elsewhere:

- **The code already matches the amended text.** WI-553 is the merge that wrote these cells; it moved `schedule.py`, `handback.py` and the pending-owner-action derivation to the terminal-`partial/` design in the same change. There is no build gap for a successor to close — an implementation of the OLD text is not what is in the tree.
- **The re-attestation obligation is carried by snapshot drift, not by a WI.** The six rows' chains have drifted from `docs/archive/last_approved/`, so `trace.py --approve modified` renders every one of them into the owner's re-attestation brief; the obligation persists in that brief until the owner blesses the rows and re-snapshots (`intake.py snapshot` in the same commit, per PROCESS.md §7). Verified in this worktree 2026-09-01: the brief renders all six — `### LLR LLR-144` and `### TC TC-138` under `## SR-144`, `### LLR LLR-058` under `## SR-148`, `### LLR LLR-198` and `### TC TC-194` under `## SR-168`, `### TC TC-147` under `## SR-174`. Six of six.
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --approve modified | grep -cE '^### (LLR|TC) (LLR-058|LLR-144|LLR-198|TC-138|TC-147|TC-194)$'" rev=520ca00a -->
- **Minting a WI to hold that signature would be wrong.** It is a HUMAN act on a generated brief, not schedulable work; a row for it would be a lane that can only wait. (The kit has no `## Dispositions` shape for "no successor owed" either: `intake.parse_dispositions` REFUSES a section with no fenced `toml` block, so a prose-only section would halt the merge sweep. This reasoning therefore lives here, in the Deliverable.)

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- LLR-058 `Detail`: 'Derives the dependency-ready frontier from the WI registry + dispatcher reservations (never prose), excludes blocked/de…' -> 'Derives the dependency-ready frontier from the WI registry + dispatcher reservations (never prose), excludes terminally…'
- LLR-144 `Detail`: "close_partial: commits the lane's work as-is, moves each claimed spec to the TERMINAL partial/ (nothing re-claims it, s…" -> "close_partial: commits the lane's work as-is, moves each claimed spec to the TERMINAL partial/ (nothing re-claims it, s…"
- LLR-198 `Detail`: 'The pending-owner-action derivation, in one module that renders no page and decides nothing about lanes. Its three comm…' -> 'The pending-owner-action derivation, in one module that renders no page and decides nothing about lanes. Its two commit…'
- TC-138 `Method`: 'Run the handback suite: a partial close moves each claimed spec to the terminal partial/ and writes its immutable per-c…' -> 'Run the handback suite: a partial close moves each claimed spec to the terminal partial/ and writes its immutable per-c…'
- TC-147 `Method`: "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…" -> "Run the intake suite against real git repos, red-then-green per trigger (trigger (b) keys on the close's immutable REPO…"
- TC-194 `Method`: 'Drive blocked rows, Drafted or drifted SRs, tracked pauses and malformed pauses through the facade that used to own the…' -> 'Drive Drafted or drifted SRs, tracked pauses and malformed pauses through the facade that used to own the derivation. A…'
- TC-194 `Verifies`: 'SR-168;LLR-198;IF-138' -> 'SR-168;LLR-198'

Outcomes (§A5.2): flip rows back to Approved where no scope moved
(per the declared approval level in docs/process.toml — recommend-only while the tier is HUMAN-HELD, ruled decision
2), or draft the real scope-change / re-scope / cancellation rows in
a `## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).
