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
