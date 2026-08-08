+++
id = "WI-416"
title = "dispose: WI-413 handed back (e56f4e2c201a) - cancel / defer / re-queue with drafted follow-up / surface an open item (a disposition row never hands back; R3)"
workstream = "process"
buildtier = "strong"
safety_class = "adjudication"
+++

## Deliverable

**CANCELLED 2026-08-08 — superseded; its disposition mechanism is no longer live.**

This row was the adjudication of WI-413's handback. WI-413 is itself cancelled as
superseded (above), and the mechanism that minted this row — `handback.py`'s
mutating return plus `intake._handback_drafts` — is retired by decisions D-4.
The expected result the plan §13 recorded ("cancellation/supersession once its old
disposition mechanism is no longer live") is what happened.

**Its evidence is preserved, because it is the sharpest statement of the general
defect this program fixes:** an adjudication brief that opens with the defendant's
own verdict, clipped mid-word. That is now a prompt-contract obligation — a judge's
brief never includes the judged party's self-assessment (plan §10.4) — carried by
P4's `adjudicate-disposition` template rather than by a per-incident correction.

## Context

The handed-back spec is `docs/work/queued/WI-413-bare-sweep-re-mints-open-dispositions.md`.

**Amended trunk-side before claim (owner, 2026-08-03).** The mint's derived Context quoted the returned spec's `## Handback` first line clipped at `_LINE_CLIP` = 140, which made THIS row's premise a *verdict* ("NEEDS-HUMAN … Owner ruling needed on widening scope") instead of a finding — the lane prescribing the disposition that R3 gives to the disposition row (`rulings-context-2026-08-01.md` §R3 point 2: surface an open item *"where a human ruling is genuinely needed"* — that judgement is this row's). The returned spec's `## Handback` note is deliberately UNTOUCHED: it is the permanent record of what that lane concluded. Only this brief is corrected. (The clip-anchors-the-judge defect itself is filed separately, not here.)

**The finding, neutrally stated.** Two independent REVIEW-A rounds (`docs/reviews/WI-413-REVIEW-A.md`) rejected both *derived-identity* approaches the builder tried. (a) The returned spec's last-touch commit: `git log -1 -- <path>` names the last touch for any reason, so clearing a `blockref` or moving `queued/`→`deferred/` re-mints; untracked/shallow history falls back to a changing observer; and truncating git's unambiguous `%h` to 7 chars collided on a real 80k-commit drive and minted ZERO for a genuinely owed second judgement. (b) A SHA-256 digest of the `## Handback` note: the hash was not section-bounded (appending a `## Context` re-minted), 48-bit truncation preserved the same silent-suppression class, empty notes collapsed to one universal token, and a moved spec left the disposition's `specref` dangling and unclaimable under R-E.

**Judge this FIRST: the reviewer's second recorded direction was never attempted.** WI-413's own title carries it — *"or make the handback arm dedupe against an OPEN disposition row citing the same spec (state-based dedup instead of title-token)"*. The builder took the derived-token direction twice; option B has no driven result either way. Read against the code it appears to need NO scope widening and NO identity persisted at handback time: dedup is `_mint`'s exact-title filter (`intake.py:735-736`) over titles built in `_handback_drafts` (`intake.py:493`), both inside this row's declared scope of "intake.py's sweep arm + tests"; `_OPEN` (`intake.py:171`) and `read_spec_rows`' Status/SafetyClass/SpecRef fields already exist. Keyed on the WI **id** rather than the spec **path**, it would also answer round-2 finding 3, since an id never moves. It also cannot silently suppress — it compares no identities, it asks whether a judgement is already pending. **NOT DRIVEN.** Verify against the reviewer's two required behaviours before ruling: sweep twice against one still-marked spec mints ONE row; a genuine second handback mints a second.

If option B holds, the honest disposition is re-queue AS SCOPED — the handback's "outside this row's declared scope" premise is true only of the derived-token direction, not of the row.

Outcomes (R3): cancel / defer / re-queue with drafted follow-up / surface an open item. Clearing its blockref re-queues it; moving it to cancelled/ (reason in the Deliverable) cancels it; a drafted follow-up goes in THIS row's ## Dispositions section; an open item goes to docs/requirements/open-items.csv.
