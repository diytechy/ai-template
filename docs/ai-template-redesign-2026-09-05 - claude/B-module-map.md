# Appendix B — module map against the four-stage loop

Produced 2026-09-05 by a research agent over `project-trajectory/scripts` at
trunk `a9bf6cee`, with a stdlib AST walk (deferred imports inside function
bodies included). SLOC here is non-blank, non-comment, **docstrings excluded**;
appendix A's 58k figure counted docstrings. Both are stated so the reader can
pick one.

**Headline.** 76,337 raw lines / **38,995 SLOC** across 82 modules; 87,679
lines of tests / 3,255 test functions in 154 files; **164,016 lines of Python
in total**. About 49% of kit source is prose (comments, docstrings, blanks).
The spine governed is 653 rows (27 SN + 76 SR + 192 LLR + 191 TC + 167 IF) plus
797 WI specs (583 archived): roughly 60 SLOC of kit per governed row, 250
lines of Python (code + tests) per row. Nine modules exceed the declared
1,000-SLOC module cap; `docs/complexity-baseline` carries 198 accepted
complexity-debt rows (21 in `trace`, 16 in `check_trajectory`, 13 in
`gen_arch_map`, 8 in `agent_loop`).

## B.1 Mass per stage

| Stage | Modules | SLOC | % | Own test fns |
|---|---:|---:|---:|---:|
| dashboard / render | 16 | 8,036 | **20.6%** | 349 |
| spine-trace | 12 | 6,297 | **16.1%** | 385 |
| dispatch | 7 | 5,280 | 13.5% | 337 |
| wi-create | 5 | 4,683 | 12.0% | 144 |
| check-harness | 10 | 2,874 | 7.4% | 468 |
| review | 10 | 2,697 | 6.9% | 195 |
| integrate / merge | 5 | 2,646 | 6.8% | 223 |
| scaffold / bootstrap | 1 | 1,661 | 4.3% | 59 |
| doc-checks | 5 | 1,382 | 3.5% | 144 |
| migration / legacy | 3 | 1,163 | 3.0% | 54 |
| schedule | 2 | 1,100 | 2.8% | 95 |
| arbitrate / adjudicate | 2 | 972 | 2.5% | 55 |
| misc | 4 | 204 | 0.5% | 13 |

The owner's four stages (wi-create + schedule + dispatch + review/arbitrate)
total **14,732 SLOC, 37.8%**. The other 62% renders state (20.6%), proves the
spine consistent (16.1%), checks (10.9%), merges (6.8%), scaffolds (4.3%) and
migrates (3.0%). The render stage is the largest and produces zero decisions.

**Import closure.** From the seven loop modules (`dispatch`, `agent_loop`,
`lane`, `integrate`, `handback`, `intake`, `schedule`) the transitive STATIC
import closure, deferred imports included, is **46 of 82 modules, 25,490 SLOC,
65% of the kit's SLOC** (the round-1 reviewer's independent traversal; the
first draft said 45 / 25,376, missing `kitlib/evidence.py`). This is possible
dependency, not measured load — `check_trajectory.doc_anchors` tolerates a
missing `check_docs` — and it drags in
`trace`, `check_trajectory`, `check_docs`, `gen_arch_map`, `coherence`,
`hats`, all five `plan_*` modules and `wi_convert`. The loop cannot run
without loading two-thirds of the kit.

## B.2 The largest modules

| Module | Stage | SLOC | Top-level fns | Own tests | Fan-in | Fan-out |
|---|---|---:|---:|---:|---:|---:|
| trace | spine-trace | 3,372 | 115 | 197 | 7 | 10 |
| agent_loop | dispatch | 2,613 | 107 | 224 | 0 | 13 |
| check_trajectory | wi-create | 2,331 | 112 | 0 | 7 | 11 |
| bootstrap | scaffold | 1,661 | 55 | 59 | 0 | 2 |
| gen_arch_map | render | 1,433 | 70 | 61 | 4 | 3 |
| integrate | merge | 1,426 | 79 | 156 | 4 | 8 |
| intake | wi-create | 1,397 | 78 | 59 | 4 | 11 |
| agent_common | dispatch | 1,338 | 89 | 20 | 11 | 7 |
| check | harness | 1,177 | 39 | 349 | 0 | 4 |
| traj_panels | render | 896 | 15 | 40 | 1 | 6 |
| traj_views | render | 875 | 20 | 45 | 1 | 4 |
| gen_trajectory | render | 820 | 4 | 33 | 0 | 8 |
| gen_open_items | render | 818 | 31 | 48 | 0 | 5 |
| agent_route | dispatch | 751 | 30 | 57 | 2 | 3 |
| consolidate | wi-create | 682 | 53 | 59 | 3 | 5 |
| dispatch | schedule | 678 | 31 | 47 | 1 | 10 |

`kitlib` is 11 modules / 1,614 SLOC (4.1%) and is a genuine leaf layer (fan-out
zero everywhere); `kitlib.config` has fan-in 40, `spine_carrier` 24,
`kitlib.spine` 21. `agent_loop` is the largest un-layered module: it imports
13 kit modules including `dispatch`, legal only because it sits outside the
declared lifecycle band.

## B.3 The multi-WI lane (spine batch)

**Only one kind batches.** `dispatch._kind_action` (`dispatch.py:364`) returns
`"batch"` for `kind == "spine"` alone; the batch is built at `dispatch.py:452`
as every ready spine row together in one branch and one session. Everything
else is already one WI per lane.

**Code that exists only because a lane may hold more than one WI — about 100
code-only SLOC (0.25% of the kit) plus about 360 test lines.** (Corrected in
review round 1: the figures below are docstring-INCLUSIVE and summed to 314;
recounted by AST excluding docstrings the same fourteen functions are 97 SLOC,
and the "about 69" of partly-batch code was never enumerated finely enough to
reproduce. The first draft quoted 314 + 69 ≈ 383 against a docstring-free
denominator.) Fully batch-only, each with a docstring saying a one-row lane
cannot observe it (docstring-inclusive line counts):
`agent_loop.assignment_block` (40), `agent_loop.current_assignment_wi` (32),
`agent_loop.lane_completion` (14), `agent_loop.claimed_on_branch` (15),
`agent_common.stale_terminal_assignment` (24), `agent_common.train_evidence`
(14), `integrate.claimed_ids_on_branch` (19), `kitlib.station.
mechanical_close_order` + `_close_sort_key` + `mechanical_close_subject` (26),
`kitlib.verdict.mechanical_close_attestation` (57), `kitlib.verdict.
_closed_wi_ids` (43), `handback.open_claimed_specs` (18), `dispatch.
_residue_wi_count` (12) — 314 SLOC. Partly batch-shaped portions of
`handback.close_adjudication`, `dispatch._claim_lanes`, `dispatch._admission`,
`integrate.claim` and the `--wi 'A;B'` parse add about 69.

**Why it exists.** Not throughput: the throughput knob (the "traincar") was
killed with a recorded 19 reservations → 8 integrations → 0 gate-verified
(`docs/concurrency-v2.md` §A6). The batch is an **atomicity device for the
human re-attestation window**: one window over the whole spine means an
amendment cannot land half-attested (§A4.4). §A4.4 already writes the
component-scoped replacement and declines to build it: "no repo running this
kit has a spine large enough to pay for it."

**What it cost, from the record** (`docs/log.md:60492`, the four-row batch of
2026-09-03): (1) the walk skipped a built-but-unclosed row and stranded the
lane for ten sessions until a human closed it; (2) the mechanical close read a
spec already moved and the whole loop exited 2; (3) the preflight refused
three of four rows as stale because the lane itself had closed them; (5) the
legacy rollup compiled once per merged row. All four are lane-cardinality
defects a one-row lane cannot hit. Defect (4), the close staling its own round,
also bit the single-row WI-586; defect (6), `EXIT_PAUSED` before a parked lane
resumes, is cardinality-independent.

**Verdict.** One WI per lane removes about 100 code-only SLOC, ~360 test
lines and four of six stranding defects. Note that the two verdict helpers
(`mechanical_close_attestation`, `_closed_wi_ids`) also exist because the
single-row WI-586 lane staled its own round, so they are removed by
close-before-round (PLAN §4.4), not by cardinality. The property given up — N spine amendments land in N
re-attest windows instead of one — is worth less than the failure modes it
bought while the spine is this size, and the loss shrinks further once the
spine stops describing the kit's plumbing (appendix A). The owner's suspicion
is right about causation and wrong about magnitude: batches are not where the
complexity mass lives.

## B.4 Duplication and sprawl signals

**(a) Registry reading.** Six intended one-homes (`kitlib/spine`,
`kitlib/registry`, `kitlib/config`, `kitlib/station`, `spine_carrier`,
`trace`); 21 modules use `spine_carrier.load` (86 sites). **Sixteen modules
keep their own parser.** `docs/process.toml` is parsed raw in four places with
three different failure defaults. The `+++` frontmatter fence is parsed seven
different ways (`kitlib/registry.py:311`, `integrate.py:236`,
`wi_convert.py:401`, `handback.py:104`, `check_docs.py:221`,
`consolidate.py:1064`, `kitlib/station.py:359`), each with a different
failure behaviour; `check_docs.py:230` documents keeping its copy in sync by
hand.

**(b) LLM prompt composition — seven mechanisms.** `prompts.load` +
`prompts.fill` is the declared contract and has exactly one true caller
(`adjudicate_brief.compose`). The worker, reviewer and critique prompts —
the three `prompts.py` was written for — bypass it via `str.format`, chained
`str.replace` (an absent slot is a silent no-op), a second template loader in
`plan_briefs` with its own key map and a `{{NAME}}` syntax, nine hand-built
markdown block concatenations, and two raw whole-prompt concatenations.
Templates are declared in two places (8 in `prompts.KIT_PROMPTS`, 3 dual-plan
hats in `plan_briefs.HAT_KEYS`), so the hats are absent from the catalogue,
the preflight and the per-session digest telemetry.

**(c) Result conventions — eight.** `(value, refusal)` tuples in 19 modules;
bare refusal-string-or-None in 12 modules (48 functions); `(ok, msg)` tuples;
list-of-strings findings in 31 modules (95 `*_findings` functions);
six custom exception classes; ~50 stdlib raises; `main()` returning int (24
modules, only 2 using the `EXIT_*` vocabulary); and 109 `sys.exit`/
`SystemExit` sites across 38 modules — 78 of them in library code, 24 in
`check.py` alone. Eighteen result dataclasses with no shared base; no
`Refusal`, `Result` or `Outcome` type.

**(d) CLI entry points.** 47 `__main__` guards, 46 argparse parsers, 6 with
subparsers — **57 distinct CLI verbs**; `docs/cli-reference.md` documents 45.

**(e) Generated artifacts.** 13 declared in `stack.ini [generated]`; 11
generators (5,939 SLOC in `gen_*`); `trunk_step.py --regen` regenerates only
5 of the 13; one (`tests/test_module_size_ratchet.py`) has no regenerator and
is re-stamped by hand. `check.py` runs 33 steps at `--stage all`; **14 at
DevStg-Tests, none of them a test step**.

## B.5 The legacy tail — about 1,530 SLOC (3.9%)

`migrate_carrier.py` (558, one-shot .md/.csv → TOML), `wi_convert.py` (406,
CSV ↔ spec interchange), `check_vocab.py` (199, retired `G*` and `ratif*`
vocabulary), five `bootstrap._migrate_*` functions (~217), `integrate.
_legacy_rollup_refusal` and `_legacy_window_refusal` (64, the migration window
that accepts a hand-compiled rollup — load-bearing today because a finished
lane cannot draw a round), `agent_common._in_legacy_window` and friends (27),
the CSV carrier half of `kitlib.spine` (40, still fan-in 21) and
`spine_carrier.rows_from_csv` (9).

## B.6 Layering

`tests/test_import_layers.py` declares: no cycles (`CYCLES = []`, compared for
equality); zero intra-cycle edges; views (`traj_*`, `gen_*`) never import
lifecycle; a lifecycle rank `dispatch 0 → handback/lane 1 → integrate 2 →
intake 3` with edges pointing strictly down; the walker descends into function
bodies. It passes (7 tests, 1.7 s) and an independent AST walk confirms
`kitlib` is a leaf. But the layering is thin: `kitlib` is 4% of the kit, the
39k-SLOC bulk is a flat namespace with no declared rank outside the five-module
band, and every recorded fix is "move what crosses to a module below both" —
producing a shelf of tiny read-model modules rather than a domain core.

## B.7 The agent's assessment

1. The batch is real but small; delete it. The atomicity it buys is worth less
   than the stranding class it caused.
2. Batches are not where the complexity is. The measured churn is review
   wording: 4 of 20 rounds lost to MINOR-only refusals, 2 plus a reroll
   refusal to record-only reworks, 4 drawn by hand outside the machinery, 3
   hand refreshes, 3 forced unloads (handoff 09-04). None is lane cardinality.
3. The real cost centre is the verdict-freshness identity: a rework that
   edits only records leaves the tree unchanged and the next APPROVE is
   refused; a finished lane cannot draw another round; recovery is a
   supervisor-drawn reviewer plus a hand-compiled legacy rollup. That is a
   design flaw, and it is why a "migration window" is load-bearing.
4. Rendering is the single largest stage and produces no decisions; eight of
   thirteen generated artifacts are read occasionally and gated on every
   commit.
5. `trace.py` at 3,372 SLOC and 21 complexity-debt rows is the true monolith:
   it reads, joins, reports orphans, computes approval sets, mints briefs and
   renders three formats, and seven modules import it.
6. **A minimal kit is eight modules:** `spine.py` (one carrier, one row
   vocabulary, one reader — absorbs `spine_carrier`, `kitlib.spine`,
   `kitlib.registry`, `kitlib.ladder`, `trace_text` and the 16 private
   parsers); `trace.py` (the join and the orphan report only, ≤1,000 SLOC);
   `work.py` (minting, contradiction/consolidation judgement, the frontier —
   absorbs `intake`, `consolidate`, `census`, `check_trajectory`,
   `schedule`); `loop.py` (dispatcher + lane + session, one WI per lane —
   absorbs `dispatch`, `lane`, `agent_loop`, `agent_common`, `agent_session`,
   `agent_route`; 5,958 SLOC today and the coupling problem); `merge.py`
   (claim, refresh, merge slot, handback — absorbs `integrate`, `handback`,
   `spec_move`, `trunk_step`, `kitlib.station`); `review.py` (verdict,
   scoring, briefs, arbitration — absorbs `kitlib.verdict`, `score_reviews`,
   `adjudicate_brief`, `acceptance_record`, `hats`, `gen_verdict_rollup` and
   the five `plan_*` modules); `check.py` (the harness, with the ten
   `check_*` leaves as steps); `render.py` (one generator with pluggable
   views, replacing 16 modules / 8,036 SLOC).
7. Three cross-cutting conventions are worth more than any single merge:
   **one result type**, **one prompt fill**, **one registry read**. Today a
   reader holds eight contracts to follow one call chain.
8. Retire the legacy tail.
9. In one sentence: 164,016 lines of Python and 198 accepted complexity-debt
   rows to govern 653 spine rows, with a loop whose import closure is 65% of
   the kit — so every change to scheduling risks the dashboard, and every
   change to the dashboard risks the merge slot.
