# Duplicated-stage detection, measured against this repository's consolidations

**Status: RESULT FOR OWNER RULING.** This is WI-624's research write-up, carried
by WI-657 part 4. It adopts no detector: adoption is the owner's ruling on this
result. The prototype that produced the §2 to §4 figures is
[`2026-09-28-duplicated-stage-detection-measure.py`](2026-09-28-duplicated-stage-detection-measure.py),
beside this file. It sits outside `project-trajectory/scripts/` and `tests/`,
so no gate, hook or commit bar runs it.

<!-- fig: cmd="python docs/plans/2026-09-28-duplicated-stage-detection-measure.py --show-truth --sample 12" rev=0ded5c77 -->
The recall, noise, sample and queue-similarity figures (§2 to §4) come from
that one command, run at `0ded5c77`. The code half checks out each
consolidation's parent in a detached worktree and removes it afterwards. The
whole run takes about 12 minutes. Three kinds of figure come from elsewhere,
and each carries its own provenance marker where it appears:

- the standing census's reading against its stamp (`check_dupes_census.py`);
- the census signals' recall on the 2026-09-27 groups, quoted from WI-679's
  Deliverable, not re-derived here;
- the history of the derived stage (`git log` over `docs/stage`).

## 0. The answer in brief

- **The shared stage the owner described (A→B→C beside A→B→D) is findable, but
  not at a volume anyone would read.** Two methods find 11 or 12 of the 12
  shared-stage instances in this repository's history: call runs of three or
  four callees, and 30-token normalized windows. Today's census finds 0 of the
  12. At `0ded5c77` the finding methods report 1,007 to 21,300 function pairs
  inside `project-trajectory/scripts/` alone. None of the 36 findings sampled
  from the three methods judged here was a stage a reviewer would extract;
  two were borderline.
- **The reason is structural, and one test shows it.** A shared stage is made
  of plumbing calls (read the file, check it exists, strip the cell, run git),
  and that plumbing is also what every idiom shares. Filtering the sequence
  down to the project's own operations removes the idioms, and recall falls
  with them, from 11 of 12 to 3 of 12 at best.
- **Near-miss whole-function similarity is the one method with clean output.**
  Normalized-token Jaccard of 0.7 or more reports 6 pairs in the scripts at
  `0ded5c77`, and 5 of the 6 are real duplicates the census cannot see. One is
  a policy table held in two modules under two names. On the historical ground
  truth it adds nothing to the census (11 of 27 whole-function instances, all
  of which the census also finds).
- **Recommendation:** adopt no shared-stage detector. If the owner wants a
  wider burn-down number, the near-miss pairs can be listed as a report beside
  the census, warn-only and never a gate (the D-7 posture). Anything
  fragment-level waits on the judged-once ledger in §6 and on a signal that
  separates a stage from plumbing, which this pass did not find.
- **The queue half (the named work-item consolidations):** text similarity
  over specs finds 13 of the 66 pairs of the 2026-09-27 groups among its 66
  most-similar pairs. The census signals WI-679 measured found 12 (§4.4
  gives the source). That is no gain worth a new signal, and WI-679's
  decision stands.
- **A finding the measurement turned up:** the standing census reads
  `5 group(s) / 5 redundant copy/copies / 52 redundant line(s)` against its
  stamped `0 / 0 / 0`, and nothing reported it (§7 gives the command). Its `[step:dupes-census]`
  selects at `DevStg-Impl`, a rung this repository's derived stage has never
  reached. It is the same selection defect WI-657 found in `[step:complexity]`
  (§7).

## 1. The question

The owner's ruling (the [owner-notes plan](2026-09-23-owner-notes-spine-sessions-and-tests.md)
§4.1, S14, 2026-09-24): *"Two modules processing A→B→C and A→B→D express four
stages; extracting A→B makes it three."* Today's census,
`check_dupes_census.py`, hashes whole function bodies, so it cannot see a
shared prefix inside two different functions, and exact matching misses small
deviations. The pass was to measure two candidate methods against past
consolidation findings: **call-sequence fingerprints** and **near-miss
similarity**. It was also to design a judged-once ledger, so that an accepted
idiom is never raised again.

## 2. The ground truth

### 2.1 Code: 39 instances read from 13 consolidation commits

The ground truth is read **mechanically from each consolidation's own diff**,
never from a method's output, so no method grades itself. At the consolidation
commit's parent, a function is a **copy** of a home in either of two cases:

- the commit deletes it and binds its name to an import of the home (the
  re-export form every WI-448 slice used); or
- the commit keeps it but removes at least two of its lines, and the function
  newly calls a function the commit added.

An **instance** is either:

- two or more copies of one home; or
- one function whose own body now calls the new home at least twice. That is
  two arms of one function carrying one stage, the shape in WI-345, WI-347 and
  WI-657 part 1.

Every instance the reader produced was checked against its commit message.
None was dropped.

| commit | consolidation | instances |
|---|---|---|
| `3b7ae3fd` | WI-346: one spine loader and one capture helper in `gen_trajectory` | 2 stage |
| `8fc5f813` | WI-345: the verdict plumbing two arms carried, one of them diverged | 3 stage (arms) |
| `ac348ac6` | WI-347: five one-off duplications extracted, not sanctioned | 6 stage (3 arms) |
| `9ecb934f` | WI-657 part 1: `load_registries` 42 → 6 through `_working_set` | 1 stage (arms) |
| `46de9442` | WI-448 slice 1: the spec-folder reader, the declared-line reader, `_git_out` | 10 whole |
| `2eae651e` | WI-448 slice 2: 33 `_utf8_console` copies | 1 whole |
| `0f3b4eca` | WI-448 slice 3: the spine row vocabulary (includes the `llr_exempt` drift incident) | 11 whole |
| `23890e5d` | WI-448 slice 4: the residual groups (includes the `_sn_rows` drift incident) | 4 whole |
| `fe6173d3` | WI-448 slice 5: the TOML emitter, three bodies that genuinely differed | 1 whole |
| `a3373b94` | WI-465: fixtures pin `core.autocrlf` through one helper | 0 |
| `87bd45dd` | WI-498: the stage ladder gets one home | 0 |
| `e1c01f2b` | WI-520: the credential class vocabulary | 0 |
| `dd7bc7fd` | WI-583 round 3: Done-when had three readers and two rules | 0 |

That is **27 whole-function instances** (the WI-448 program, 99 copies) and
**12 shared-stage instances** (7 of them arms of one function). The four
commits with no instance were examined and yield none for a stated reason:

- **WI-465** is a call-site consolidation. It swept one repeated
  configuration call into a shared helper, `conftest.pin_autocrlf`, at every
  git-initing fixture, and it removed no function copy. The duplicated
  statement sat inside fixtures that differ everywhere else, so neither a
  body hash nor this pass's reader (which needs a removed copy, or one
  function calling the home twice) can see it.
- **WI-498 and WI-520** moved data (a rung table, a pattern table).
- **`dd7bc7fd`'s** second reader was a module-level regex constant, not a
  function.

The last three are a class in their own right: **duplicated data and
constants are invisible to every function-level method measured here**. That
includes the census, and it includes the constant half of slice 4's
`MODULE_EXTS` finding. WI-465's class, a repeated statement spread across
call sites, is invisible to the function-body methods in the same way.

### 2.2 The queue: the named work-item consolidations

The 2026-09-02 restructure, the 2026-09-27 hand consolidation and the WI-689
census and verdict group **work items** by the surface they edit. They do not
record consolidations of code, so a code detector has nothing to find in them.
The measurement uses them for the one method family that applies to prose:
near-miss similarity (word-trigram Jaccard over each queued spec's whole
text). The three sets are:

- **8aae3af3**, the 50 open rows before the 2026-09-27 consolidation, with the
  table's 11 groups (66 pairs). The source is
  [`docs/log.d/2026-09-27-wave4-consolidation.md`](../log.d/2026-09-27-wave4-consolidation.md).
- **9de63e78**, the 18 rows before the 2026-09-02 restructure, with the four
  groups of absorbed rows each new host drew from (10 pairs). The source is
  [§2.2 of that plan](2026-09-02-backlog-restructure-and-consolidation.md).
- **e26e22aa**, the WI-689 census's seven candidates. The judge absorbed none
  of them and ordered one pair (WI-655 needs WI-616), so all 21 pairs are
  judged negatives for consolidation.

## 3. The methods

| id | method | what counts as a finding |
|---|---|---|
| M0 | today's census | identical docstring-stripped body AST, 4+ lines |
| M1-k3, k4, k6 | call-sequence fingerprint | two functions share a contiguous run of k callee names, in evaluation order; `cap5` drops a run shared by more than 5 functions |
| M1L-k2-cap5, M1L-k3 | the same, over the project's own operations | only callees named like a module-level script function and not like a builtin or a str/list/dict/set/Path/ArgumentParser method |
| M2-w30, w50 | near-miss fragment | two functions share a window of w Type-2-normalized tokens (identifiers become `ID`, literals become `LIT`, nested defs dropped) |
| M2-j0.5, j0.7 | near-miss whole function | Jaccard of normalized 8-token shingles at or above the threshold |

The M1 and M2 fragment methods also report a function paired with itself when
its own stream repeats a run at two non-overlapping places. That is how they
can see the arms instances. Every method scans `project-trajectory/scripts/`
and `tests/`. Noise is reported for the scripts alone as well, because the
census's own scope is scripts.

## 4. Results

### 4.1 Recall

An instance is recalled when the method links at least two of its copies, or
reports the self-pair for an arms instance.

| method | whole-function (27) | shared stage (12) | copies linked (117) |
|---|---|---|---|
| M0 census | **24** | **0** | 87 |
| M1-k3 | 16 | 11 | 57 |
| M1-k4 | 12 | 11 | 48 |
| M1-k4-cap5 | 10 | 9 | 39 |
| M1-k6 | 8 | 3 | 26 |
| M1L-k2-cap5 | 2 | 3 | 9 |
| M1L-k3 | 2 | 1 | 7 |
| M2-w30 | 15 | **12** | 88 |
| M2-w50 | 10 | 1 | 29 |
| M2-w50-cap5 | 10 | 1 | 29 |
| M2-j0.5 | 11 | 0 | 30 |
| M2-j0.7 | 11 | 0 | 30 |

The census misses three whole-function instances: `is_example` and `refs` in
slice 3, and slice 5's TOML emitter. No whole-function method catches any of
the three (the fragment methods M1-k3 and M2-w30 catch the emitter), so no
whole-function method **adds** recall to the census on this history. The union of M0 and M2-j0.7 is still 24
of 27.

### 4.2 Noise

These are the pairs each method reports at `0ded5c77` over 7,559 functions.
"Summed over parents" is the report volume at the 13 consolidation parents
added together: what a reviewer would have faced at those commits.

| method | pairs | both in scripts | within one function | summed over parents |
|---|---|---|---|---|
| M0 | 91 | 5 | 0 | 4,425 |
| M1-k3 | 51,471 | 21,300 | 533 | 347,378 |
| M1-k4 | 11,358 | 4,988 | 202 | 84,969 |
| M1-k4-cap5 | 3,394 | 1,208 | 162 | 27,711 |
| M1-k6 | 1,418 | 612 | 39 | 11,355 |
| M1L-k2-cap5 | 1,644 | 341 | 212 | 11,347 |
| M1L-k3 | 4,547 | 300 | 102 | 28,442 |
| M2-w30 | 18,106 | 1,007 | 245 | 166,740 |
| M2-w50 | 1,060 | 86 | 27 | 9,508 |
| M2-w50-cap5 | 839 | 86 | 27 | 7,429 |
| M2-j0.5 | 316 | 20 | 0 | 4,068 |
| M2-j0.7 | 104 | 6 | 0 | 1,853 |

### 4.3 What the findings are: a judged sample

Each method's scripts-only findings at `0ded5c77` were sampled with a fixed
seed (12 per method, or all when fewer) and judged by reading both functions.
The four verdicts:

- **E**: a shared stage or copy a reviewer applying the 0→A→B rule would
  extract.
- **B**: borderline, meaning a small shared setup or sibling builders.
- **I**: an idiom (the argparse preamble, a format/append report loop, a
  repeated accessor).
- **U**: a coincidence of shape.

One judge (the builder) made every call. The pairs and verdicts are listed in
the appendix so the owner can re-judge them.

| method | sampled of | E | B | I | U |
|---|---|---|---|---|---|
| M0 | 5 of 5 | 4 | 0 | 1 | 0 |
| M1-k4-cap5 | 12 of 1,208 | 0 | 1 | 9 | 2 |
| M1-k6 | 12 of 612 | 0 | 0 | 10 | 2 |
| M1L-k2-cap5 | 12 of 341 | 0 | 6 | 0 | 6 |
| M1L-k3 | 12 of 300 | 0 | 2 | 10 | 0 |
| M2-w30 | 12 of 1,007 | 0 | 1 | 8 | 3 |
| M2-w50-cap5 | 12 of 86 | 3 | 4 | 4 | 1 |
| M2-j0.7 | 6 of 6 | 5 | 0 | 1 | 0 |

The argparse preamble alone accounts for 8 of 12 M1-k6 findings and 6 of 12
M2-w30 findings.

### 4.4 The queue half

Word-trigram Jaccard over the queued specs:

| queue | rows | truth pairs | top-N most similar | recalled | Jaccard ≥ 0.02 | Jaccard ≥ 0.04 |
|---|---|---|---|---|---|---|
| 8aae3af3 | 50 | 66 | top 66 | 13 | 101 reported, 19 truth | 35 reported, 5 truth |
| 9de63e78 | 18 | 10 | top 10 | 3 (8 in top 20) | 49 reported, 10 truth | 22 reported, 8 truth |

<!-- fig: cmd="quoted from docs/archive/work/complete/WI-679-run-queue-consolidation-throu.md, Deliverable, 'The surface signal: not added, on measurement'; not re-derived here" rev=8aae3af3 -->
On the same 66 pairs, the census's signals found 12 and joined 1 of the 11
groups. That figure is WI-679's, measured at 8aae3af3 and quoted from its
Deliverable ([`WI-679`](../archive/work/complete/WI-679-run-queue-consolidation-throu.md)),
not re-derived by this pass. At e26e22aa the 21 judged-negative
pairs read from 0.000 to 0.065, while the 90th percentile of the whole queue
is 0.051. The highest of them (WI-616 with WI-651, 0.065) sit above most of
the queue, partly because every host carries the same "Consolidated
2026-09-27" paragraph. A text signal would re-propose exactly the rows the
judge had just separated. The census's digest guard exists to stop that, and
a text signal would work against it.

## 5. What the numbers say

1. **The census is the right instrument for what it measures.** On
   whole-function copies it has the best recall (24 of 27) and the smallest
   report (5 pairs in the scripts, 4 of them real). Nothing measured adds
   recall to it on this history.
2. **A shared stage looks like plumbing to both method families.** The
   methods that recall the stage class are the short-run ones: M1-k3 and
   M1-k4 at 11 of 12, M2-w30 at 12 of 12. They recall it because a stage is a
   short run of ordinary calls (`exists`, `read_text`, `csv_rows`; `unlink`,
   `read_verdict`), and that is also what every idiom is made of. Lengthening
   the run (k6, w50) or capping by frequency (cap5) cuts the idioms and the
   stages together. Keeping only the project's own operations (M1L) cuts the
   stages hardest (3 of 12). None of the 36 sampled findings of M1-k4-cap5,
   M1-k6 and M2-w30 was an extractable stage. This is not a tuning problem
   that more thresholds would fix: the signal and the noise are the same
   tokens.
3. **Near-miss whole-function similarity finds what the census cannot, where
   it matters now.** M2-j0.7's six scripts pairs at `0ded5c77` include:
   - `intake.normalize_bar` and `integrate._normalize_bar`, one bar vocabulary
     read through two tables under two names, which is the `MODULE_EXTS` class
     slice 4 recorded;
   - `plan_artifacts.parse_plan_wis`, whose docstring still justifies the copy
     by the retired F5 rule;
   - the two `_clip` functions, whose elision markers have already diverged.

   It recalls no shared stage, because a stage inside a larger function never
   makes two whole functions similar.
4. **The arms class is already under pressure from another sensor.**
   WI-657 part 1's `_working_set` came from the complexity ratchet: nine
   repeated stanzas in one function scored as cognitive complexity. Seven of
   the twelve stage instances are arms of one function, and they are the
   shape the complexity census and the deep-module-design skill already push
   on.
5. **The dangerous duplicates are data.** Both drift incidents D-7 named were
   whole-function copies at consolidation time, and the census found them.
   Three of the thirteen commits, though, consolidated tables and constants
   that no function-level method sees, and a fourth (WI-465) consolidated a
   statement repeated across call sites, which the function-body methods do
   not see either.

## 6. The judged-once ledger (designed, not built)

Any fragment-level method needs this ledger before it can run at all. It also
makes a near-miss report cheap to live with.

- **Home:** `docs/dupes-judged`, a tab-separated file beside
  `docs/complexity-baseline`. It is the central escape hatch, with no inline
  pragma, for the reason LLR-206 gives for the complexity baseline: scattered
  opt-outs self-replicate.
- **Two keys, because there are two kinds of judgement:**
  - An **idiom** is keyed by the fingerprint of the shared run itself (the
    normalized window or callee run). Judging the argparse preamble once
    silences it everywhere it recurs, including in scripts not yet written.
  - A **kept pair** (two functions that stay apart for a stated reason, like
    `human_approves` and `human_approves_spine`, two contracts on one body) is
    keyed by the two `(path, qualname)` names plus a digest of each normalized
    body. It is raised again only when either body changes, because a changed
    body is a new question.
- **Verdicts:** `idiom` or `kept`, each with a reason a reader can argue with.
  A third verdict, `owed WI-###`, keeps a pair listed until the extraction
  lands.
- **Burn-down:** the report prints the unjudged count, and that is the number
  a baseline would stamp, downward-only like `[dupes-census]`. It is never a
  gate.
- **What it would buy, from the sample:** idiom entries would remove most I
  findings, since a dozen entries cover the argparse and report-loop shapes.
  They cannot remove U findings, and U is what sinks M1. The ledger makes
  M2-w50-cap5's 86 scripts pairs reviewable. It does not make M1 or M2-w30
  usable.

## 7. Findings on the way

<!-- fig: cmd="python project-trajectory/scripts/check_dupes_census.py --root ." rev=0ded5c77 -->
- **The census has drifted silently.** It reads 5/5/52 against a stamped
  0/0/0 at `0ded5c77`. The five groups are the census's own view of the five
  M0 scripts pairs in the appendix; four are small real copies and one is a
  deliberate pair. `[step:dupes-census]` is declared
  `from-stage = DevStg-Impl`. Since the census was armed, this repository's
  derived stage has never read DevStg-Impl, so no derived-stage gate run has
  ever selected the step.
<!-- fig: cmd="for c in $(git log --format=%h --since=2026-08-20 -- docs/stage docs/gate); do for f in docs/stage docs/gate; do git show $c:$f 2>/dev/null | grep -E '^(stage|gate) ='; done; done | sort | uniq -c" rev=0ded5c77 -->
  Over every commit that touched `docs/stage` or its predecessor `docs/gate`
  since 2026-08-20, the recorded stage read DevStg-Arch 9 times,
  DevStg-LLReqs 206 times and DevStg-Tests 95 times.
  `[step:complexity]` has the same defect, which is WI-657's own finding;
  WI-657's report carries the decision on it.
- **Real duplicates at `0ded5c77`** (from the judged samples; not fixed here,
  because this item adopts nothing and changes no code):
  - the bar vocabulary's two homes (`intake.normalize_bar`,
    `integrate._normalize_bar`);
  - the plan-table parser's F5-era copy (`plan_artifacts.parse_plan_wis`);
  - two `_clip`s;
  - `trace.if_note_advisories`, a near-copy of `trace_text.cite_advisories`;
  - two open-items readers sharing the load, skip and status-filter stage
    (`check_trajectory.approval_brief_findings`,
    `trace.ruled_open_item_texts`), which is the owner's A→B→C / A→B→D shape
    exactly;
  - two `trunk_step` argv builders that differ by one flag;
  - `spec_move.rewrite_text` and `trunk_step.rebase_links`;
  - the four small M0 copies.

  Each is a candidate for a row, filed if the owner wants the burn-down.

## 8. Options for the owner

| option | what it adds | cost |
|---|---|---|
| **(a) Adopt nothing; record the result.** *Recommended.* | The census stays as it is. Shared-stage work stays with review, the 0→A→B rule and the complexity ratchet | none |
| (b) Add M2-j0.7 near-miss pairs to the census report, warn-only | about 6 pairs today, most real; no historical recall gain | a small stdlib extension of `check_dupes_census.py`, a baseline beside `[dupes-census]`, and the ledger's `kept` half |
| (c) Build the ledger, then M2-w50-cap5 as a report | 86 scripts pairs to judge once; 1 of 12 stage instances | the ledger, a judging sitting, and ongoing entries |
| (d) Pursue call-sequence (M1) further | 9 to 11 of 12 stages | thousands of findings, 0 of 36 sampled extractable; not recommended on this evidence |

Whatever the ruling, the census's own selection (§7) should be decided with
`[step:complexity]`'s: a sensor that never runs reports nothing, however good
its method is.

## Appendix: the judged sample

These are the scripts-only pairs at `0ded5c77` in the order the command
prints them, with seed 624. A pair that names one function twice is that
function's repeated stream (arms).

**M0.** E read_toml_text / `_toml_tables`; I human_approves /
human_approves_spine (two contracts on one body, deliberate); E read_rows /
load_csv; E `_is_docstring` / `_is_docstring`; E `_entries` / seam_endpoints.

**M1-k4-cap5.** I hat_findings / sr_boundary_findings; I `_finding_text` /
`_one_correction_findings`; I `_archive_plan` / gen_release_checklist.main;
I component_findings / if_tc_allow_hygiene_findings; I `_ctx_rel_arc` /
sw_graph; I parse_wi_list / load_floors; U if_tc_coverage_findings /
interface_findings; I load_spine_index / load_registries; B `_run_bar` /
`_run_trunk_step`; I if_tc_allow_hygiene_findings / `_touch_refusal`;
I `_declared_packs` / load_wis; U symbol_findings / `_load_critique_srs`.

**M1-k6.** I ×8 argparse preambles (check_vendored/trunk_step,
agent_loop.parse_args/check_stubs, gen_skills_index/trace,
check_vendored/gen_release_checklist, check_perf/spec_move,
check_docs/trunk_step, agent_route/check_docs, check_docs/gen_arch_map);
I trace.render_report (repeated `len` run); U critique_brief /
`_stakeholder_row_findings`; U consolidate_values / status_dir;
I staged_divergence / check_figures.main (print run).

**M1L-k2-cap5.** B flat_graph / `_drill_layer_svg`; B intake_after_merge /
mint_rejudge; U default_base / `_lane_verdict`; B `_migrate_gate_policy` /
migrate_legacy_config; U `_pack_lines` / `_pending_oi_lines`; B
`_admit_frontier` / `_paused_exit`; U `_audit_lines` / `_cmd_list`; U
`_add_members` / hat_findings; B `_admit_frontier` / `_station_exit`; U
`_settled_off_spine` / `_tier_holds`; U `_implemented_ids` / `_frontier_lines`;
B classify_srs / interface_bridge_findings.

**M1L-k3.** I ×10 repeated `esc`, `_cell` or `refs` accessor runs (queue_digest
/ llr_block, arch_icicle.draw / sw_graph, word_diff / `_da_item`,
context_block / `_da_item`, `_model` / tc_block, `_unmet` / sr_block,
word_diff / `_render_drill`, arch_icicle.draw / dag_svg, `_attestation_cards`
/ dag_svg, `_phase_groups` / `_add_members`); B dag_svg / sw_graph;
B `_approval_act_refusal` / `_held_status_refusal`.

**M2-w30.** U symbol_findings / module_components; I ×6 argparse preambles
(check_docs/trace, check_stubs/gen_prompt_catalog, check/record_observation,
gen_verdict_rollup/trace, agent_route/check_perf, check_readability/hats);
U `_predecessor_lines` / gen_okf.emit; I gen_components.main / close_partial
(print run); U `_okf_type_edges` / `_layer_edges`; B falsification_worklist /
release_gate_findings; I analyze / render_console (`len` run).

**M2-w50-cap5.** E if_note_advisories / cite_advisories; U
build_cli_reference / build_map; B gen_okf.emit (per-tier stanzas); E
normalize_bar / `_normalize_bar`; B sr_block / tc_block; B llr_block /
tc_block; B `_approved_by_act` / `_authorised_registries`; I ×4 argparse
preambles (intake/schedule, check_dupes_census/trunk_step,
check_stubs/gen_verdict_rollup, check_dupes_census/check_test_first);
E approval_brief_findings / ruled_open_item_texts.

**M2-j0.7.** E normalize_bar / `_normalize_bar`; E `_clip` / `_clip`;
E `_amendment_drafts` / `_first_approval_drafts`; I
declared_absences_parse_findings / kernel_allow_parse_findings (a documented
idiom whose messages differ); E `_cli_reference_cmd` /
`_interface_reference_cmd`; E parse_plan_wis / parse_plan.
