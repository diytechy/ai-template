# Handoff — the 2026-08-13 pre-absence charge-through

**Boot order for a fresh session:** this file → `docs/status.md` START HERE →
the log's `2026-08-13b` session entry → the Decisions entry of 2026-08-13 (the
batch ruling that authorizes everything here) →
[archive/plans/2026-08-13-sitting-pack.md](archive/plans/2026-08-13-sitting-pack.md) (the
owner's reading order at return). Branch: `infra/mechanized-loop`, local only —
**push and merge-to-main are the owner's** (`push = "human"`).

## What this session was

The owner ruled all 14 open items (OI-14, OI-16..OI-28) in one sitting and
directed a charge-through before their absence. Execution rows WI-436..WI-450
were minted; each built by an Opus/Sonnet worktree agent, merged serially with
the commit bar at every merge, and adversarially reviewed per slice (codex
`gpt-5.6-sol`, medium, hostile brief; findings re-verified before fixing —
the rounds found real defects on every slice, and one review proposal was
itself refuted on measurement and the refutation recorded in-module).

## Landed and CLOSED (spec + Deliverable in docs/work/complete/)

- **WI-436** OI-26 loose end records its ruling.
- **WI-437** `gate_policy` runtime label → `session_hold`; PROCESS_OPTIONS
  swept; the four blocked verdicts (SR-082/085/108/125) unblocked — they are
  OI-23-class amendments still OWED (sitting pack §2.6).
- **WI-438** `[ci-tiers]` moment→tier table declared once; both workflows
  pinned; four pin-defeats fixed with bite tests.
- **WI-439** tarball stamp warns; skill points at §6; the first old-kit
  re-sync test (pinned old kit fd5916b9); false-anchor probe; `--force` leg;
  CI `fetch-depth: 0`.
- **WI-440** cross-component overlap suppression → warn-only advisory;
  PROCESS.md §8 declares the planning-brief consumption; lazy seam read +
  one-scan cache.
- **WI-441** Part A: data pack + ranked shortlist; **P5 narrow-waist adopted
  provisionally warn-first** — CMP-006..009 minted, CMP-001..005 retired
  (D-4), 149 LLR + 54 IF Component cells re-pointed, advisories 15→0
  exactly as predicted. `SR.Area` verdict: retire free-text, six spanning
  values become a closed aspect vocabulary (NOT yet executed — see owed).
- **WI-444** the applied re-attest batch: prose batch (12/12 laundered rows
  verified), edge-tier dissolution (SN-013..022 deleted; re-anchors
  SR-021→SN-001, SR-029→SN-025; two orphaned obligations caught and folded
  into SR-021/SR-026), OI-17 reframe, OI-23 stale-row amendments (+ four
  adjacent [policies] rows), SN-005 narrowed. Ledger:
  `archive/plans/2026-08-13-wi444-batch-application.md`.
- **WI-446** six-hat roster (OWNER TEXT — edit at return) + planner-brief
  injection; coverage record deliberately deferred (SN-036's second half).
  LLR-168 + TC-162 (Draft) seed the machinery onto the spine.
- **WI-447** `RESYNC_PACK.md` — 51+1 SHA-anchored entries, ADOPTING §6 shrank
  804→31 lines, skill deduped; content-loss audit 34/34 accounted (2 weakened
  → restored). Deliberate deviation accepted: the pack is NOT scaffolded
  (kit-checkout home; pinned by test).
- **WI-449** CodeSymbol grammar stated where it binds; the four unfounded
  rows re-confirmed and kept; non-py skip now a visible ADVISORY ink (5 rows).
- **WI-450** drill pin partition-independent; top-view reads snapshot-atomic.
- **WI-443** Part B: PROCESS.md §8 contract; **interfaces + components on the
  TOML carrier, CSVs deleted** (carrier work now COMPLETE across every
  registry); IF `Status` retired (Stability the one maturity field);
  `signal`/`rationale` columns; warn-first schema tier + four Contract
  negative rules + endpoint classifier (9 endpoints resolving to nothing —
  real rot, partially fixed); two hidden Status readers discovered and
  re-keyed. Adopter recipe: pack entry `[since 2eb1c0c8]`.
- **B10** `split_refs` joined the canonical splitter, pinned in
  `test_rule_sync`.

## WI-445 — LANDED COMPLETE, merged, closed (finalized at phase close)

The stage-ladder program shipped whole: the gate vocabulary is RETIRED
repo-wide. `docs/gate` now reads `DevBar-Reqs` with
`stage=DevStg-Needs stage-ord=0 stage-of=8` on the basis line; the three
bars are DevBar-Reqs / DevBar-Tests / DevBar-Release (DevBar-Below the
floor); `check_vocab` enforces the retirement warn-first (bite-proven);
`--gate` keeps G1/G2/G3 as warned aliases; `## Gate Sign-offs` became
`## Sittings`. Its own grep test caught a live lexical-sort bug in
`check.py --list` on first run. New Draft spine rows: SR-149/LLR-169/TC-163
(the enforcer's home, CMP-007). SR-004 + SR-053 flipped Modified by the
sweep. Full account: the WI-445 Deliverable in docs/work/complete/. NOTE
FOR EVERY FUTURE SESSION: author stage/bar vocabulary, never G-tags —
check_vocab will warn now and error once promoted.

## NOT started — the next session's queue, in order

0. **WI-445's codex round** — the program self-verified hard (bite tests, a
   composed full bar) and the coordinator reviewed the merge, but the
   per-slice hostile codex pass was deferred at context exhaustion; run it
   over the 445 diff (8a0fb5ad..the merge) first, findings re-verified
   before fixing, per the session's standing method.
1. **WI-442 boundary seeds** (after 445): the 19 missing boundary IF rows
   (data pack §1b) as Draft rows on the NEW toml carrier, the direct-session
   actor declaration, the template-set SR, regularize the two accidental
   'agent CLI' rows. Also the A6 warn-first boundary-rung check if 445's
   rung-1 predicate didn't already cover it.
2. **WI-448 common-module inversion** (after 445 — its sweep touches the same
   scripts): consolidation per D-8, bootstrap imports FROM the common module,
   MAPPING row, real scaffold verification, ratchet re-stamps, first pack
   entries for the renames.
3. **Area→aspect execution** (from WI-441's verdict): retire `SR.Area`
   free-text, closed aspect vocabulary — belongs with the next SR-registry
   touch; flagged in the shortlist ruling.
4. **SN-036 coverage record** (WI-446's deferred half).
5. The **six form-finding splits / SR-082 / Draft-status lifts / rationale
   sweep / four unblocked verdicts** — ALL sitting-gated; do not execute
   without the owner (sitting pack §2).

## Standing facts a resumer must not rediscover

- **Worktrees spawn stale** (`3abeb636`) — every agent brief must open with
  `git log --oneline -1` + `git reset --hard infra/mechanized-loop`.
- **Pipe-masking**: `pytest | tail -1 && git commit` commits on a red — the
  pipeline exit is tail's. Two ratchet re-stamps happened one commit late
  this way. Run the bar, THEN commit, separately.
- The full unfiltered suite takes 10-25 min under agent contention; `-n 4`
  survives where `-n auto` gets workers killed.
- Ratchets/byte-budgets: compose reason chains at merges, measure the real
  file, never discard either side's reasons.
- `trace.py --ratify modified` PRINTS; regenerating the brief needs
  `--out docs/ratify/2026-08-13-wi444.md` (ratify-fresh reds otherwise).
- The gate reads **G1 honestly** (`modified=64, drafts=51, uncovered=0, components=4`,
  stage=DevStg-Needs, DevBar-Reqs approaching); it will not rise until the
  sitting — that is the design. Final composed-tree full bar: 2452 passed /
  6 skipped, zero failures.
- **Cap agents' full-suite runs in every brief.** The ladder builder spent
  77 of its 149 minutes re-running the full unfiltered suite (8+ times,
  ~7 min each) because its brief said "verify each stage" — instruct:
  targeted modules per stage, the full bar ONCE at the end. The transcript
  timing skeleton is extractable from the task output JSONL when a runtime
  needs auditing.
- Codex reviews: `codex exec --model gpt-5.6-sol -c
  model_reasoning_effort=medium --sandbox read-only "<hostile brief>"`.

## The owner's return (the short list)

Read [archive/plans/2026-08-13-sitting-pack.md](archive/plans/2026-08-13-sitting-pack.md).
One consolidated re-attest sitting covers everything; then merge-to-main.
