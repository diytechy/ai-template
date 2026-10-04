# Review brief: the widened WI-788 (read-only; do not modify any file)

You are an independent reviewer for the ai-template repo (cwd), at HEAD b61f450f. Do NOT read, cite or act on `OWNER_SCRATCHPAD.md`. Do not edit, create or delete any file.

## Artifact under review

`docs/work/queued/WI-788-provider-homes-and-new-routes.md`. It began as provider homes and new routes and has been widened by the owner, in passes, to: session families and reset terms; a glossary; one labelled entry point for every model call (nine design risks ruled); OI-101's rulings; plan kinds and the lost dual-plan auto-dispatch; the arbiter evidence; the delegated-decisions record on every path; and, largest, ONE LANE-STATE PROVIDER with a state enum (PLANNING single/dual; BUILD; REVIEW_REWORK; ADJUDICATION: LOCK, REFRESH, RESOLVE, JUDGE, MINT, MERGE_ACTION; MERGE; ARCHIVE) and items LS1-LS10, with an eight-slice plan. Half 1 is a design note that STOPS for the owner; half 2 becomes successor rows. Context docs: `docs/iteration/wi-lifecycle.html` (today's lifecycle as drawn from the code), `docs/plans/2026-10-03-s11-in-lane-adjudication.md`, `docs/plans/2026-10-04-planning-before-build-research.md`, `docs/work/queued/WI-790-wi-cites-the-oi-it-waits-on.md`, `docs/requirements/open-items.toml` (OI-100..102 ruled).

Owner standing rules to apply: fix a single point of failure rather than add fallback/degenerate/legacy paths; a RESYNC entry is the migration; judgements and reviews are independent of what they judge; enforce coupling rules at the commit that makes the change (commit vs its parent), not by history archaeology; scripts stdlib-only, cross-platform; templates copy-ready; repo and shipped template structurally in sync.

## What to do

1. **Coherence across passes.** The spec accreted sections over two days. Find contradictions or superseded text a builder could follow by mistake (e.g. "retained by default" vs builder reset-every-call; arbiter options vs the ARBITRATION state; risk 5's fresh non-replacing session vs the LS4 lock; risk 8 vs LS1; the original Done-when half-2 bullets vs the successor-row shape; slice plans stated twice with different numbering; the S11 freshness rung vs LS4). Name each with line numbers and the wording that should win.
2. **The lane-state provider (LS1-LS10) against the code.** Check the inventory of today's carriers and modules against `dispatch.py`, `lane.py`, `integrate.py`, `agent_loop.py`, `handback.py`, `intake.py`, `schedule.py`, `trunk_step.py`, `kitlib/`. Anything missing? Is LS1's recommendation (one committed record written only by the provider, transitions gated on evidence, written in the same commit as the evidence) sound against: worktree commits vs trunk commits; the merge reproducing the refreshed tree byte for byte (Bar-Green tree identity, integrate.py ~:9-14) — does committing the record at MERGE/ARCHIVE time break tree identity?; crash between evidence and record; concurrent lanes; the dispatcher's tick. Is LS4 (lock held from REFRESH through MERGE_ACTION) compatible with today's merge slot (`out/integrate.lock`), refresh outside the slot, and the lease wait? What is the deadlock/starvation risk? Is LS3's tier step-down mechanizable from what a plan declares?
3. **Rulings changed.** Verify LS8's list is complete: every refusal, rung, contract (IF rows), SR/LLR/TC, and doc that assumes minting/acts happen only on trunk, post-merge intake, or the S11 freshness rung. Cite rows (grep docs/requirements, docs/test, PROCESS.md, PROCESS_OPTIONS.md, prompts/).
4. **Scope and sliceability.** Is the eight-slice plan ordered by real dependencies? Can slice 3 ("today's flow moved onto the provider unchanged in behaviour") be built and tested before slice 5 changes the flow? Is WI-788 now too big for one design note, and if so, how should the note itself be split (still one owner checkpoint)?
5. **Unasked owner questions** a design note would otherwise have to guess.

## Output (final message)

- `VERDICT:` READY-FOR-DESIGN / READY-WITH-FIXES / NOT-READY.
- `FINDINGS:` numbered, most severe first; claim, evidence (file:line), consequence, proposed fix (spec wording where useful).
- `OWNER QUESTIONS:` only decisions the owner must make, each with options and a recommendation.
- `INVENTORY GAPS:` carriers, modules, rows or docs missing from the spec's lists.
Be concrete and terse. Findings are claims: back each with evidence.
