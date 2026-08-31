# WI-550 — REVIEW-A (compiled)

The WI-level verdict the merge slot reads (RULING-7), compiled by the
supervising session from the round files below — ordered by commit time,
the governing verdict last. Every line is quoted from its round file;
nothing is judged here that a reviewer did not judge.

Heterogeneity: RELAXED, recorded (the C5 rung by the owner's 2026-08-30
direction). Both cross-family families failed on this lane before these
rounds: OPENAI-TERRA answered its usage limit in 4 s (reset 08:40 UTC) and
OPENCODE-GROK went silent and was cut by the idle deadline at 902 s with no
verdict; the two rounds below are ANTHROPIC-OPUS-STRONG, the same family as
the adjudicator, drawn by the supervising session through the kit's own
reviewer brief and route.

## Round 1 — 002-REVIEW-A-b9e5dea.md

# WI-550 — REVIEW-A of the disposition close (adjudication of the WI-540 partial close)

Reviewed diff: `git diff contract_split...HEAD` (docs-only): the WI-550 spec moved
`active/ -> archive/work/complete/`, `## Deliverable` + `## Dispositions` added,
`specref` cleared.

## What I verified (drove the real paths, quoted real output)

- **Close mechanics (adjudicate-disposition.template.md §50).** `## Deliverable`
  filled with the `OUTCOME:` line + verdict path, placed BEFORE `## Context`;
  `specref = ""` cleared; spec moved to `docs/archive/work/complete/`; both the
  verdict commit (`547c3505`) and the close commit (`9aa2158b`) carry the
  `WI: WI-550` trailer. All present.
- **Successor draft mints cleanly.** Drove `intake.parse_dispositions` on the
  shipped spec → `refusal=None`, 1 draft, `kind=ordinary`, `supersedes="WI-540"`.
  Title 109 chars (≤120). `safety_class="ordinary"` ∈ `schedule.SAFETY_CLASSES`;
  all keys ∈ `_DRAFT_KEYS`; no `[table]` header. `_terminal_hits` unions
  `WORK`+`ARCHIVE_WORK`, so the archived spec is scanned — the successor will be
  found and minted at merge.
- **Factual basis of the ruling holds.** `git diff 9abdb5d982 contract_split --
  project-trajectory/scripts tests` is EMPTY (trunk byte-identical to the WI-540
  base); `adjudicator_session.py` + its test absent from trunk; IF-174 reverted
  out of `interfaces.toml` while its mark stays burned. The DISCARD-all ruling
  and "no red on trunk" claim are true. Referenced `wi-540-...patch` and
  `WI-541` queued spec both exist.
- **Harness.** `check.py --jobs 0` → `RESULT: PASS`. `trace.py --strict-integrity`
  → `integrity=0`. The LLR-197 provenance FINDING and `orphans=2` are pre-existing
  trunk-side rows this docs-only diff does not touch.

Four disposition answers all covered: outcome PARTIAL upheld against commit facts;
keep/discard split ruled (DISCARD product commits — already reverted, verified;
KEEP report/patch/mark bookkeeping); one successor drafted; cost strong, no dual.

## Findings

- [MINOR] docs/archive/work/complete/WI-550-dispose-the-close-recorded-at.md:52 -> the successor's rationale prose (WI-541 blocks, re-land-don't-rebuild, resolve DESIGN-CHECK first, strong-tier justification) is placed BEFORE the ```toml block, so `parse_dispositions` captures `scope=''` and the minted successor's `## Context` will hold only the "Drafted by WI-550 … drafts-not-mints" boilerplate — the two hard boundaries the adjudication stressed do not ride into the minted row (prior dispositions WI-542/WI-544 put substantive scope prose AFTER the block, which intake carries verbatim into Context); the successor still mints and its `specref` defaults back to this archived spec, so the loss is recoverable, not silent -> move the scope/boundary prose to AFTER the ```toml block (a short "Scope of the successor: re-land the preserved patch inert at dial 0, do not rebuild; first reproduce and resolve the DESIGN-CHECK error/timeout, then get the §A2 refresh bar green" paragraph) so it rides into the minted successor's Context -> @owner

VERDICT: APPROVE findings=1

## Round 2 — 002-REVIEW-A-e8e49cd.md

# WI-550 — REVIEW-A of the disposition close (adjudication of the WI-540 partial close)

Reviewed diff: `git diff contract_split...HEAD` (docs-only). Two files: the WI-550
spec moved `active/ -> archive/work/complete/` (`## Deliverable` + `## Dispositions`
added, `specref` cleared to `""`), and the HEAD commit `e8e49cda` moved the
successor's rationale prose to AFTER the ```toml block.

## What I verified (drove the real paths, quoted real output)

- **The HEAD fix is real and complete.** `e8e49cda` addresses the prior review's
  one MINOR (prose before the block → `scope=''`). Drove `intake.parse_dispositions`
  on the shipped spec at both revisions: PRE-fix (`766de4b1`) → 1 draft, `scope`
  length **0** (the whole rationale would have been dropped from the minted
  successor's Context); POST-fix (HEAD) → `refusal=None`, 1 draft, `scope` length
  **1107**, carrying all five boundaries the adjudication stressed (preserved
  `wi-540-…patch`, the DESIGN-CHECK error/timeout blocker, "does not rebuild",
  the WI-541 block, the strong-tier justification). The simulated minted Context
  is 1214 chars — the substantive scope now rides into the row, as intake does
  for WI-542/WI-544. The scope prose is the file's last section, so
  `section.split("\n## ")` does not truncate it.
- **Successor draft mints cleanly.** `refusal=None`; `kind=ordinary`,
  `supersedes="WI-540"`, `buildtier="strong"`, `priority=2`, `workstream="process"`;
  title 109 chars (≤120); all keys ∈ `_DRAFT_KEYS`; `safety_class="ordinary"`
  (not `adjudication`, which `_draft_refusal` would reject). Omitted `specref`
  defaults to this archived spec (`intake.py:1084`) whose scope prose already
  names the plan (§2–§5 / OI-69 a–e) and patch — a serviceable spec-of-record.
- **Cited facts hold.** `docs/id-watermark` shows `IF = 174`, matching the prose's
  "id-watermark IF=174"; IF-174 is absent from `interfaces.toml` (mark burned,
  row reverted). WI-540 is terminal in `docs/work/partial/`; the referenced
  `docs/work/handback/wi-540-adjudicator-retention-layer.patch` and
  `docs/work/queued/WI-541-verify-retention-layer.md` (`needs = ["WI-540"]`) both
  exist. No content lost vs the deleted active spec — Context preserved verbatim,
  `specref` cleared as WI-542/WI-544 also do for a disposition row.
- **Placement.** Spec in `docs/archive/work/complete/` (integrator derives the
  outcome from the folder, not the free-text `OUTCOME:` line — no machine parses
  it); the active dir holds no tracked files. status.md's WI-550 line sits inside
  the GENERATED status block (regenerated trunk-side on merge) — the diff
  correctly does not hand-edit it.
- **Harness.** `check.py --jobs 0` → `RESULT: PASS`. `trace.py --strict-integrity`
  → `integrity=0`. The LLR-197 provenance FINDING and `orphans=2` are pre-existing
  trunk rows this docs-only diff does not touch.

Four disposition answers all covered: outcome PARTIAL upheld against commit facts;
keep/discard ruled (DISCARD product commits — reverted, verified; KEEP
report/patch/mark); one successor drafted and mints with full scope; cost strong,
no dual. The prior review's MINOR is resolved and I found nothing new.

## Findings

(none)

VERDICT: APPROVE findings=0

## Governing verdict

The final round above governs:

    VERDICT: APPROVE findings=0
