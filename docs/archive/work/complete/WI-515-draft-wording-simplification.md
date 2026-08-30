+++
id = "WI-515"
title = "Cross-family wording review of the approval-pending Drafted spine text, adjudicated and applied"
specref = ""
workstream = "requirements"
buildtier = "strong"
safety_class = "spine"
priority = 2
+++

## Deliverable

The nineteen `Drafted` rows the owner must approve are shorter to read, and
every suggestion behind that is dispositioned in writing. Dossier:
[../../../reviews/2026-08-24-draft-wording-round/RESUME.md](../../../reviews/2026-08-24-draft-wording-round/RESUME.md).
Record:
[../../../log.d/2026-08-24-wi515-draft-wording-review.md](../../../log.md#2026-08-24--wi-515-the-cross-family-wording-round-on-the-approval-pending-drafted-text).

**The round.** Routed by PROVIDER, not gateway: `OPENAI-TERRA`
(`gpt-5.6-terra` via `codex exec`) — the OpenAI-family entry the owner named,
which exists in `docs/agents.toml` and is listed in `docs/agents-enabled`, so
no substitution was needed. Probed live before dispatch. Four batches, each row
sent with its anchor SR's `Requirement` and `AcceptanceCriteria` as the intent
anchor, prompt on stdin, result captured with `--output-last-message`; the raw
returns are committed unedited beside the dossier.

**The adjudication.** **38 suggestions over 19 rows: 21 ACCEPTED (5 amended),
17 REJECTED.** Fourteen of the seventeen rejections fall into three classes
stated once rather than seventeen times: every `Expected` suggestion made its
cell 400-600 characters where the registry's 181 test rows carry a one-line
pointer (10); five `Method` rewrites promoted the anchor SR's acceptance
criteria into the case as though they were executed steps no `Evidence` entry
covers; and `TC-182`'s rewrite drove a seam-signal-compatibility case that
`LLR-187` — the row it verifies — states has no executable form. The amendments
restored what a cut would have dropped: the "reports clearly instead of dying
deep inside the engine" link to SR-160's acceptance (`LLR-193`), the "no place
in shipped machinery" and "never implies exclusive ownership" guards
(`LLR-199`), an invented description of unbuilt SN scope machinery (`LLR-194`,
removed), and an imported copy of SR-177's own never-gated/no-target contract
(`LLR-196`, removed).

**The measured effect.** The reviewable population fell from **29,441 to
25,564 characters (-13.2%)**: nine LLR `Title` cells down 28-67% (the decisive
argument was measured, not stylistic — over the 175 approved LLR rows the title
median is 36 characters and only 4 reach 90, while these nine ran 63-137),
seven LLR `Detail` cells down 10-42%, five TC `Method` cells down 4-18%. The
owner's brief itself, `docs/ratify/CURRENT.md`, went **67,180 -> 62,667 bytes**
even while now carrying a before/after pair for each re-worded row — by the
brief's own declared design, a `Drafted` row that differs from the snapshot
renders its movement rather than its full content, and those "before" halves
leave the brief entirely at the approval that re-seeds the snapshot.

**Held to the checkers, which were the acceptance gate.** `trace.py
--strict-integrity` is byte-for-byte where it was: integrity=0, drafts=19,
provenance-findings=1 (the pre-existing `LLR-197`) and, the number specifically
watched because shortening a child raises its lexical overlap with its parent,
paraphrase-advisories=3 (unchanged, the same three pre-existing rows). Every
accepted text was screened for the vague/open-ended vocabulary and the
citation-frame shapes before it was applied, and no LLR `Detail` gained a
"shall".

**Nothing was approved and nothing else moved.** No `Status` cell changed, the
`docs/archive/last_approved` snapshot was not re-seeded, the nine anchor SRs
and `LLR-041`'s drifted cell were not touched (both are `Approved` — the two
things the round surfaced about them are banked as findings for the owner in
the dossier, and neither needs a ruling to proceed). Surfaces regenerated:
`docs/ratify/CURRENT.md`, `docs/open-items.html`, `docs/stage`,
`PROJECT_STATE.html`.

## Context

The owner's ask, verbatim (2026-08-24, in-session):
*"The text on these items that need approval still seems pretty heavy. Can you
spin up an openai terra review to suggest more simplified wording and accept
suggestions that still fit the intent of the SR?"*

The approval-pending set is what `docs/ratify/CURRENT.md` renders: nine anchor
SRs (already `Approved` — review context only, never rewritten here), the
nineteen `Drafted` chain rows under them (nine LLR `Title`/`Detail`, ten TC
`Method`/`Expected`), and `LLR-041`'s drifted `Detail` cell. Only the nineteen
`Drafted` rows are editable — they carry no approval and so need no warrant to
reword; a suggestion against an `Approved` cell is banked as a finding for the
owner instead.

Route by PROVIDER: the OpenAI-family reviewer the owner named is the
`OPENAI-TERRA` row of `docs/agents.toml` (`gpt-5.6-terra` via `codex exec`),
probed live before dispatch. Every returned suggestion is adjudicated
row-by-row — accepted only where the full normative intent survives AND the
spine checkers stay green — with the accept/reject reason recorded per cell.
Guard clauses, negative claims and stated residuals are load-bearing and a
simplification that drops one is refused. Nothing is approved by this row: the
owner's approval act stays queued, and this only makes the brief he signs
lighter to read.
