+++
id = "WI-986"
title = "adjudicate: LLR-058, LLR-061, LLR-123, LLR-144, LLR-149, LLR-150, LLR-151, LLR-152, LLR-161, LLR-207, SR-144, SR-148, SR-156, TC-058, TC-061, TC-138, TC-143, TC-144, TC-145, TC-146, TC-154, TC-156, TC-205 - approved/routed cell(s) amended on merged trunk cf21e8c..dc7e2a5 (§A5.2); judge whether scope moved, then flip or draft follow-ups in ## Dispositions"
workstream = "process"
sr_refs = ["SR-144", "SR-148", "SR-156"]
specref = ""
buildtier = "strong"
safety_class = "adjudication"
brief = "amendment"
adjudicates = ["LLR-058", "LLR-061", "LLR-123", "LLR-144", "LLR-149", "LLR-150", "LLR-151", "LLR-152", "LLR-161", "LLR-207", "SR-144", "SR-148", "SR-156", "TC-058", "TC-061", "TC-138", "TC-143", "TC-144", "TC-145", "TC-146", "TC-154", "TC-156", "TC-205"]
+++

## Deliverable

Already adjudicated in the range this row was minted from, so no second
sitting is held (the re-mint trap, S11 plan section 4.2; owner-agreed
close, 2026-10-03). WI-977's in-lane whole-set sitting
`docs/reviews/wi-977/014-ADJUDICATE-fddc055.md` blessed all 23 rows
(22 MEANING+BLESS, LLR-058 CLARITY), and the lane's act turn took act seq
163. At the landing dc7e2a5cf the system, low-level and test registries
are byte-equal to their approved snapshots under docs/archive/last_approved/.

## Context

Derived from `staged_spine_amendments` on the merged commit (§A5.2).
Approved and ROUTED traced cells only; other traced cells are silent
by ruling. Each line: registry row / cell: before -> after.

- SR-144 `AcceptanceCriteria`: 'A partial close is clean under the real validator (the terminal Deliverable rule is exempt, because an early close leav…' -> 'A partial close is clean under the real validator (the terminal Deliverable rule is exempt, because an early close leav…'
- SR-144 `Requirement`: 'The delivered loop content shall close a lane that cannot finish into a TERMINAL partial state that merges like any oth…' -> 'The delivered loop content shall close a lane that cannot finish into a TERMINAL partial state that merges like any oth…'
- SR-148 `AcceptanceCriteria`: 'A ready adjudication row admits ahead of every other class, the ruled rank table unchanged (--explain still reports it)…' -> 'Each assignment admits exactly one work item, including exclusive spine admission; an ordinary frontier may fill severa…'
- SR-148 `Requirement`: "The delivered loop content shall select the work an unattended run does next from the repository's tracked registries a…" -> 'The delivered loop content shall select exactly one work item for each assignment an unattended run admits from the rep…'
- SR-156 `AcceptanceCriteria`: 'A launch with independent ready work runs up to the configured lane ceiling concurrently in isolated working trees, and…' -> 'Every executable lane claim names exactly one work item; empty or multi-item claim, assignment and resume inputs refuse…'
- SR-156 `Requirement`: 'The delivered loop content shall run ready work on bounded, mutually isolated lanes and narrow every lane back to the i…' -> 'The delivered loop content shall run exactly one work item per lane on bounded, mutually isolated lanes and narrow ever…'
- LLR-058 `Title`: 'WI-DAG frontier + deterministic traincar ordering' -> 'WI-DAG dependency-ready frontier'
- LLR-061 `Detail`: 'Replaces internal --track assumptions with explicit --wi/--train/worktree assignment; assembles the worker prompt from …' -> 'Replaces internal --track assumptions with explicit --wi/--train/worktree assignment; assembles the worker prompt from …'
- LLR-061 `Title`: 'Explicit WI/train/worktree worker assignment' -> 'Explicit work-item/train/worktree worker assignment'
- LLR-123 `Detail`: 'Orders eligible traincars by (gate, Priority desc, downstream-dependent count desc, hard-path desc, first WI id). The d…' -> 'Orders eligible work items by (gate, Priority desc, downstream-dependent count desc, hard-path desc, work-item id). The…'
- LLR-123 `Title`: 'Deterministic traincar ordering' -> 'Deterministic work-item ordering'
- LLR-144 `Detail`: "close_partial: commits the lane's work as-is, moves each claimed spec to the TERMINAL partial/ (nothing re-claims it, s…" -> "close_partial: commits the lane's work as-is, moves the one claimed spec to the TERMINAL partial/ (nothing re-claims it…"
- LLR-149 `Detail`: "The dispatcher's one scheduling decision (docs/concurrency-v2.md §A4/§A8), consuming schedule.kind_of - the §A1 classif…" -> "The dispatcher's one scheduling decision (docs/concurrency-v2.md §A4/§A8), consuming schedule.kind_of - the §A1 classif…"
- LLR-150 `Detail`: "One lane's mechanics extracted from the dispatcher (docs/concurrency-v2.md §A4.2): ensure the lane worktree (integrate.…" -> "One lane's mechanics extracted from the dispatcher (docs/concurrency-v2.md §A4.2): ensure the lane worktree (integrate.…"
- LLR-151 `Detail`: "The §A4.1 authority flip's integrator half (docs/concurrency-v2.md §A4.1): _claim_refusal's safety_class != ordinary ar…" -> "The §A4.1 authority flip's integrator half (docs/concurrency-v2.md §A4.1): _claim_refusal's safety_class != ordinary ar…"
- LLR-151 `Rationale`: 'A constraint instead of a check: the state the old refusal guarded against (a claim written beside live lanes) is now u…' -> 'A constraint instead of a check: the state the old refusal guarded against is unrepresentable, and separate exclusive t…'
- LLR-151 `Title`: 'Dispatch-lock claim rung + the spine batch claim' -> 'Dispatch-lock ownership and single-WI claim'
- LLR-152 `Detail`: 'The `adjudication` kind (docs/concurrency-v2.md §A5.2) joins the declared SafetyClass vocabulary: exclusive on the conc…' -> 'The `adjudication` kind (docs/concurrency-v2.md §A5.2) joins the declared SafetyClass vocabulary: exclusive on the conc…'
- LLR-161 `Detail`: "`close_partial` writes the report FIRST (it is the event's identity), refuses when one already exists, and restores EVE…" -> "`close_partial` writes the report FIRST (it is the event's identity), refuses when one already exists, and restores the…"
- LLR-207 `Detail`: 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…' -> 'tree_identity folds raw NUL-delimited `git ls-tree -r -z` entries after dropping docs/reviews/, docs/log.d/ and docs/it…'
- TC-058 `Method`: 'Run schedule.py against a fixture registry; the ready frontier, the exclusions with reason codes, and the deterministic…' -> 'Run schedule.py against a fixture registry; the ready frontier, the exclusions with reason codes, and the deterministic…'
- TC-061 `Method`: 'Drive the real worker loop as a subprocess against a fake agent CLI in throwaway git repos, from explicit --wi/--train …' -> 'Drive the real worker loop as a subprocess against a fake agent CLI in throwaway git repos, from explicit --wi/--train …'
- TC-138 `Method`: 'Run the handback suite: a partial close moves each claimed spec to the terminal partial/ and writes its immutable per-c…' -> 'Run the handback suite: a partial close moves its one claimed spec to the terminal partial/ and writes its immutable pe…'
- TC-143 `Method`: 'Run the dispatch admission suite: an exclusive row + a busy lane answers wait (never a parallel claim slipped past the …' -> 'Run the dispatch admission suite: an exclusive row + a busy lane answers wait (never a parallel claim slipped past the …'
- TC-144 `Method`: 'Run the dispatch loop suite on real git repos with the real bar: a spine batch claims as one commit and its worker rece…' -> 'Run the dispatch loop suite on real git repos with the real bar: each spine claim carries one work item in its one comm…'
- TC-145 `Method`: 'Run the integrator claim suite: a spine claim succeeds on an idle station (the deleted safety-class arm, red-then-green…' -> 'Run the integrator claim suite: a spine claim succeeds on an idle station (the deleted safety-class arm, red-then-green…'
- TC-146 `Method`: "Run the schedule + integrate suites' adjudication cases: the kind classifies exclusive at rank 1 (the reserved slot, pi…" -> 'Run adjudication cases: the kind is exclusive at rank one; an adjudication-only lane runs no product bar yet records a …'
- TC-154 `Method`: 'Run the loop-order suite: an adjudication row admits ahead of a ready spine batch while the ruled rank table is unchang…' -> 'Run the loop-order suite: an adjudication row admits ahead of a ready spine work item while the ruled rank table is unc…'
- TC-156 `Method`: 'Run the handback suite over real git worktrees: a partial close is clean under the REAL trajectory check (not a stub), …' -> 'Run the handback suite over real git worktrees: a partial close is clean under the REAL trajectory check (not a stub), …'
- TC-205 `Method`: "The verdict record's two halves, each driven beside its opposite so neither reads as a rule with one answer. THE IDENTI…" -> "The verdict record's two halves, each driven beside its opposite so neither reads as a rule with one answer. THE IDENTI…"

Outcomes (§A5.2): re-attest the rows ruled CLARITY (and, where the
dial releases the rung, the MEANING rows you would bless) by naming
them in the act's `--reattests`; on a HUMAN-HELD tier a CLARITY row
is re-attested, bound to the text the verdict judged, and a MEANING row is
recommended to the owner (ruled decision 2 as OI-100 amends it). Or
draft the real scope-change / re-scope / cancellation rows in a
`## Dispositions` section of THIS spec — intake mints them at this
row's merge (drafts-not-mints, R1).

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-058 [project-trajectory/scripts/schedule.py :: ready/frontier/evaluate] tests: (see TC-058) — WI-DAG dependency-ready frontier
- LLR-059 [project-trajectory/scripts/schedule.py :: classify/safety_class] tests: (see TC-059) — Pure safety classifier
- LLR-060 [project-trajectory/scripts/trunk_step.py :: REGEN_STEPS/regen] tests: (see TC-060) — next-wi/run-phase retirement + generated status/run-state
- LLR-089 [project-trajectory/scripts/schedule.py :: kind_of/classify] tests: (see TC-091) — Structural safety cross-check
- LLR-123 [project-trajectory/scripts/schedule.py :: frontier/evaluate] tests: (see TC) — Deterministic work-item ordering
- LLR-131 [project-trajectory/scripts/schedule.py :: classify] tests: (see TC) — Contradiction-safe dual-plan class

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-010 scripts/gen_arch_map <- scripts/check;scripts/trunk_step: cli --doc | --cli-doc | --contracts-doc | --src | --mode | --check | --strict-parse | --backlink-coverage | --str…
- IF-150 scripts/gen_arch_map -> scripts/check;scripts/trunk_step: exit-code 0 current · 1 a stale target under --check, an unparseable module under --strict-parse, or coverage below the…
- IF-012 scripts/gen_okf -> scripts/check;scripts/trunk_step: exit-code 0 clean, vacuous or opted out · 1 stale, missing or extra bundle file under --check
- IF-014 scripts/bootstrap -> external:downstream adopter: bytes the scaffolded template tree written under the destination root
- IF-161 docs/test/ -> scripts/acceptance_record;scripts/adjudicate_brief;scripts/amendment_brief;scripts/agent_loop;scripts/baseline_snapshot;scripts/check_doc_refs;scripts/check_flows;scripts/check_trajectory;scripts/gen_okf;scripts/gen_release_checklist;scripts/intake;scripts/plan_coverage;scripts/spine_rules;scripts/trace;scripts/traj_parse;external:downstream adopter: file test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-035 project-trajectory/skills/ -> scripts/gen_skills_index;scripts/bootstrap: file SKILL.md frontmatter: name, scope, stacks, domains, phases, tags; each other file in the skill directory, mat…
