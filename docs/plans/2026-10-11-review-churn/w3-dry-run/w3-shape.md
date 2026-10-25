# W3 Autonomy: its current shape (facts only)

Read from the ai-template repository at trunk `refactor_again`, commit `e39fff2dc`, on 2026-10-25. Every line below is copied or computed from a registry, a generated view or the source; nothing here assesses the shape or proposes a cut.

Sources: `docs/requirements/components.toml` (the authored component rows), `docs/requirements/components.derived.toml` (the generated component view), `docs/requirements/low-level-requirements.toml` (LLR rows), `docs/requirements/interfaces.toml` (IF rows), `docs/runtime-flows.md` (authored flows), the files' own docstrings and headers, `check_complexity.module_sloc` for SLOC, and an `ast` pass over the files for imports.

## How membership and seams are computed today

- **No file declares its component.** A file belongs to a component when an LLR row tagged with that component names the file in its `module` cell, so a file named by two components' LLRs is listed under both. The authored component row carries only a name, a category, a status, knowledge pointers and notes.
- **Internal or boundary** is the generated view's rule: an interface is *internal* to W3 when its owner and at least one far-side endpoint both resolve to files W3's LLRs name. Every other interface W3 touches, including one placed in W3 only by its optional `component` cell, is *boundary*.
- **An IF row** names one owner (the providing side) and a far side: `req` (requestors put information into the owner's surface: call it, invoke it, write it) or `cons` (consumers take what the owner emits). `channel` is one of `cli`, `exit-code`, `stdout`, `file`, `call`, `env`, `git`, `bytes`. `cmp` is the row's optional `component` cell; `crosses B-##` marks a row that realizes a declared system-boundary crossing. The summary after the last `·` is the row's `data` cell, cut at 90 characters.
- In the interface lists, an endpoint in *italics* is not on W3's file list: another component's file, or an `external:` party. Paths drop the leading `scripts/`.

## 1. The component row and its siblings

`CMP-008` (authored): name `W3 Autonomy` · category `software` · status `Approved` · knowledge `docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency`.

> notes: The unattended coordinator end to end: the agent_* family plus adjudicate_brief, the 5 plan_* round modules, dispatch, handback, intake, integrate, lane, prompts, schedule, score_reviews, spec_move, trunk_step.

The depth-0 frame is four components. No row fills `part_of`, so W3 has no nested components, and neither has any sibling.

- `CMP-006` W1 Registry & conformance, notes' first sentence: The spine and everything that decides whether it holds: spine_carrier, trace, trace_text, spine_rules, check_trajectory, plan_coverage, migrate_carrier, wi_convert, gen_arch_map.
- `CMP-007` W2 Gatekeeper, notes' first sentence: Every verdict a hook, CI job or gate run consumes: check, check_privacy, subagent_gate, the 8 check_* lints, and the shipped pre-commit/pre-push hooks.
- `CMP-009` W4 Human & adopter surfaces, notes' first sentence: Everything a person or an adopting repo reads or runs: bootstrap, run_menu, the 7 remaining gen_*, the 6 traj_* dashboard modules, and the onboard/dev-setup templates.

The CMP-006 row's notes say of two files in the shared `kitlib` package: "kitlib/station.py (LLR-182) and kitlib/verdict.py (LLR-207) are the package modules NOT owned here: both stay CMP-008, each one's cross-component edges declared and policed as an interface row - IF-093 for the station, IF-175 for the verdict record". The rest of the shared core (`kitlib/__init__`, `config`, `git`, `registry`, `ladder`, `stage`, `evidence`) is listed in `docs/kernel-modules-allow` as a declared shared kernel owned by CMP-006; per the same notes, its consumption from every component is recorded on that surface rather than as interface rows.

## 2. Derived counts

- SRs reached through W3's LLRs: 47, of which 8 are also reached through another component's LLRs (SR-139, SR-146, SR-155, SR-161, SR-170, SR-176, SR-178, SR-228).
- LLRs tagged CMP-008: 126. Hats on them (inherited through their SRs): CONSISTENCY, DATA-PROTECTION, INTEGRITY-RECOVERABILITY, LEGAL, MAINTAINER, PERFORMANCE, SECURITY, TEST-ENGINEER, UNATTENDED-OPS.
- Files those LLRs name: 78: 66 Python files (35225 SLOC in all) and 12 others (process text, prompt templates, a skill, hooks, launchers, setup scripts). 52 are named by W3's LLRs alone; 26 also by another component's LLRs.
- Interfaces: 65 internal, 121 boundary.
- SR ids: SR-026, SR-027, SR-028, SR-040, SR-137, SR-139, SR-144, SR-146, SR-148, SR-154, SR-155, SR-156, SR-161, SR-170, SR-171, SR-172, SR-173, SR-174, SR-175, SR-176, SR-177, SR-178, SR-208, SR-209, SR-215, SR-220, SR-222, SR-223, SR-225, SR-227, SR-228, SR-229, SR-230, SR-231, SR-232, SR-233, SR-234, SR-235, SR-237, SR-238, SR-239, SR-240, SR-241, SR-242, SR-243, SR-244, SR-246.

## 3. Files

One line each: path, size (SLOC for Python, physical lines otherwise), the W3 LLRs naming the file (count: numbers), and the first sentence of the file's own docstring or header. Section 3b adds the other components whose LLRs name the file, with their LLR counts. Paths drop `project-trajectory/`.

### 3a. Named by W3's LLRs alone (52)

- `PROCESS.md` · 1461 lines · LLR 1: 311 · Development Process (template)
- `hooks/commit-msg` · 57 lines · LLR 1: 248 · commit-msg hook — secrets + privacy scan of the commit MESSAGE (title + body).
- `prompts/adjudicate-dispute.template.md` · 73 lines · LLR 1: 311 · A CONTESTED OR REPEATED REVIEW FINDING (WI-865).
- `prompts/reviewer.template.md` · 71 lines · LLR 1: 311 · THE REDACTED REVIEWER BRIEF (S8).
- `scripts/adjudicate_act.py` · 282 SLOC · LLR 2: 338,359 · adjudicate_act.py — the ACT a committed, accepted verdict still owes, and the act brief filled from it.
- `scripts/adoption_record.py` · 216 SLOC · LLR 2: 335,345 · adoption_record.py - only the close writes a disposition's adoption record (WI-969, carrying WI-902's spec of record).
- `scripts/agent_brief.py` · 611 SLOC · LLR 6: 037,045,048,061,262,280 · Session brief construction and assignment-facing evidence.
- `scripts/agent_common.py` · 1117 SLOC · LLR 12: 027,029,030,138,177,196,246,248,339,343,346,354 · Shared coordinator primitives, extracted VERBATIM from agent_loop.py (WI-218 slice C — a file split, not a rewrite; behaviors and WI history unchanged…
- `scripts/agent_loop.py` · 2528 SLOC · LLR 20: 028,037,045,061,082,095,096,132,174,175,247,262,269,270,309,318,336,340,343,344 · Headless session engine: one claimed worker assignment, a reviewer/critique round, a dual-plan round, or an interactive sitting.
- `scripts/agent_policy.py` · 571 SLOC · LLR 4: 155,246,282,316 · Declared process policy, approval authority, and coordinator dials.
- `scripts/agent_route.py` · 956 SLOC · LLR 4: 044,072,081,336 · Model routing for the unattended coordinator — the enable-list + availability selector and the fixed escalation policy (process-options.md "Unattended…
- `scripts/agent_session.py` · 376 SLOC · LLR 2: 026,163 · One headless agent session: argv/stdin construction, launch, and capture.
- `scripts/bookkeeping.py` · 315 SLOC · LLR 4: 151,246,248,340 · bookkeeping.py — the ONE trunk bookkeeping commit: build it away from the owner's checkout, install exactly what it wrote, and advance trunk.
- `scripts/consolidate.py` · 806 SLOC · LLR 1: 210 · consolidate.py — the CONSOLIDATION census: which queued rows are one work item wearing several ids, and the guard that stops the question being asked…
- `scripts/dispatch.py` · 758 SLOC · LLR 7: 143,149,159,247,270,319,343 · dispatch.py — the dispatcher: tick loop, admission, merge slot (the scheduling front end).
- `scripts/handback.py` · 527 SLOC · LLR 6: 144,161,246,248,312,335 · handback.py — the lane closes that are not a clean merge (concurrency-v2 §A3, rewritten onto the SR-144/LLR-161 outcome model).
- `scripts/kitlib/adoption.py` · 117 SLOC · LLR 2: 335,345 · A disposition's ADOPTION of an already-filed successor: its block, the row it disposes, whether a listing accepts it, and the record the close writes.
- `scripts/kitlib/commit_hooks.py` · 68 SLOC · LLR 1: 340 · Whether this checkout's commit hooks are on: the one check every agent route calls before it starts.
- `scripts/kitlib/decisions.py` · 372 SLOC · LLR 3: 283,303,304 · The DELEGATED-DECISIONS RECORD: what one delegated run tells the owner about the calls it made on the owner's behalf — its path, its format, which clo…
- `scripts/kitlib/dispute.py` · 146 SLOC · LLR 1: 314 · A DISPUTE sitting: the findings file it rules, and its verdict grammar.
- `scripts/kitlib/done_when.py` · 303 SLOC · LLR 2: 262,307 · A lane's Done-when, fixed at claim: what an item IS, and what counts as a CHANGE.
- `scripts/kitlib/plan_pass.py` · 189 SLOC · LLR 1: 337 · A `single` row's plan records: the plan, its filed critiques and its pass record, in one grammar with one reader (WI-913).
- `scripts/kitlib/provenance.py` · 123 SLOC · LLR 2: 247,248 · Loop provenance: the trailer every commit the unattended loop makes carries, and the marker that tells a commit floor a commit is the loop's.
- `scripts/kitlib/shell_line.py` · 203 SLOC · LLR 1: 300 · The one reading of a shell command line: its simple commands, each the list of its words, with the shell's own quoting.
- `scripts/kitlib/sitting.py` · 430 SLOC · LLR 2: 310,359 · A COMBINED lane-checkpoint sitting: its scope tokens and its verdict sections.
- `scripts/kitlib/station.py` · 163 SLOC · LLR 2: 182,189 · The station's TERMINAL-OUTCOME vocabulary — the lane-close read model.
- `scripts/kitlib/winjob.py` · 78 SLOC · LLR 1: 026 · The Windows job-object helpers the kit's job callers share.
- `scripts/lane.py` · 74 SLOC · LLR 1: 150 · lane.py — one lane's mechanics (docs/concurrency-v2.md §A4.2, WI-381).
- `scripts/migrate_decisions.py` · 44 SLOC · LLR 1: 304 · Rewrite every delegated-decisions record off the retired `reviewed` key (WI-818), in place.
- `scripts/observation_cadence.py` · 121 SLOC · LLR 2: 293,294 · Observation cadence: closed-work history and declared checkpoint triggers.
- `scripts/plan_artifacts.py` · 172 SLOC · LLR 1: 074 · The dual-plan round artifact filer: the coordinator's write-side of a round (DP-001 selected plan P5 / WI-198; the protocol it serves is process-optio…
- `scripts/plan_briefs.py` · 222 SLOC · LLR 2: 071,176 · Redacted dual-plan brief assembler + the three hat prompt-map keys (DP-001 selected plan P2 / WI-195; the protocol is process-options.md "Dual-plan de…
- `scripts/plan_coverage_step.py` · 86 SLOC · LLR 1: 073 · Coverage step adapter: run the dual-plan coverage pre-pass headless and turn its exit/report contract into the round state machine's typed step outcom…
- `scripts/plan_gate.py` · 367 SLOC · LLR 1: 337 · plan_gate.py - a `single` row builds only after its plan passes (WI-913).
- `scripts/plan_round.py` · 242 SLOC · LLR 1: 070 · The dual-plan round state machine: a pure, side-effect-free library the coordinator drives (DP-001 selected plan P1 / WI-194; the protocol it models i…
- `scripts/plan_runner.py` · 434 SLOC · LLR 3: 076,269,336 · The dual-plan round RUNNER: the coordinator fan-in over the WI-194..WI-198 modules, extracted VERBATIM from agent_loop.py (WI-218 slice C — a file spl…
- `scripts/prompts.py` · 144 SLOC · LLR 1: 162 · prompts.py — the kit's prompt templates as FILES, and their strict fill.
- `scripts/rejudge.py` · 319 SLOC · LLR 1: 254 · rejudge.py — the CHECKPOINT RE-JUDGE decision: which observation test cases are due for a fresh judgment at a work-item merge or at release preparatio…
- `scripts/review_brief.py` · 778 SLOC · LLR 2: 313,341 · review_brief.py — an attended launcher's review and critique briefs, rendered from the kit's own templates, and its review filed as a kit round file.
- `scripts/schedule.py` · 446 SLOC · LLR 8: 058,059,089,095,123,131,152,288 · Derive the dependency-ready WI frontier and its deterministic schedule.
- `scripts/score_reviews.py` · 417 SLOC · LLR 1: 046 · The substance scorer — score a review verdict block by how USEFUL it is, not how long it is (process-options.md "Unattended operation" -> the routing/…
- `scripts/session_adapters.py` · 775 SLOC · LLR 11: 026,266,267,268,270,290,347,348,351,352,353 · One adapter per provider CLI: the only place a CLI's differences live.
- `scripts/session_keep.py` · 883 SLOC · LLR 3: 270,290,336 · The session service's keep operation: adjudicator and loop reviewer session retention.
- `scripts/session_service.py` · 999 SLOC · LLR 8: 269,270,305,310,317,336,340,346 · The session service: the one path every model call takes (act, keep, record).
- `scripts/spec_move.py` · 222 SLOC · LLR 1: 145 · spec_move.py — the link-aware spec-move ritual: move a registry/spec file and keep every markdown link in the repo true, as ONE indivisible operation.
- `scripts/trunk_step.py` · 369 SLOC · LLR 4: 060,124,137,142 · The serial trunk step — compile the log fragments, regenerate the trunk artifacts.
- `scripts/usage_ingest.py` · 235 SLOC · LLR 7: 348,349,350,351,353,354,355 · Record the usage of a Claude Code session and its sub-agents, once per invocation, from the session's transcripts.
- `skills/coordinator-cycle/SKILL.md` · 583 lines · LLR 1: 356 · Use when coordinating work in this template repo, from scope critique at filing or minting through lane claims, code iteration, spine checkpoints, ind…
- `scripts/coordinator-relaunch.cmd` · 28 lines · LLR 1: 301 · Coordinator relaunch, Windows (WI-822): started detached, in a new console, by the coordinator guard at the lease holder's true session end.
- `scripts/coordinator-relaunch.sh` · 43 lines · LLR 1: 301 · Coordinator relaunch, POSIX (WI-822): started detached by the coordinator guard at the lease holder's true session end.
- `scripts/coordinator/codex_call.py` · 518 SLOC · LLR 1: 346 · codex_call.py — the coordinator's codex calls (a Sol review or critique, a Terra turn) through the kit's session service.
- `scripts/coordinator/overnight_legs.py` · 342 SLOC · LLR 1: 340 · overnight_legs.py — run coordinator sessions back to back, unattended, as headless `claude -p` legs (owner, 2026-10-09: "Headless leg loop").

### 3b. Also named by another component's LLRs (26)

- `hooks/pre-commit` · 324 lines · LLR 1: 358 · also CMP-007 (1) · Pre-commit hook — the agent-neutral *process floor*.
- `scripts/acceptance_record.py` · 857 SLOC · LLR 3: 298,358,359 · also CMP-006 (8), CMP-007 (1) · THE ACCEPTANCE RECORD — what an amendment IS, and the mirror it is measured against.
- `scripts/adjudicate_brief.py` · 984 SLOC · LLR 7: 167,295,305,308,310,315,359 · also CMP-006 (1) · adjudicate_brief.py — the EVIDENCE an adjudication session's brief is filled with, and the rule for when it must not be sent at all.
- `scripts/bootstrap.py` · 1517 SLOC · LLR 1: 339 · also CMP-009 (7) · Scaffold a new project from this trajectory kit.
- `scripts/census.py` · 100 SLOC · LLR 1: 188 · also CMP-006 (1) · census.py — the registry-gap census: what the registries themselves say is missing.
- `scripts/check.py` · 1340 SLOC · LLR 3: 246,298,358 · also CMP-006 (1), CMP-007 (9) · The check harness — one command that runs every quality gate locally and in CI.
- `scripts/check_trajectory.py` · 1656 SLOC · LLR 1: 299 · also CMP-006 (9) · Validate the work-item registry — stdlib only.
- `scripts/coordinator_adjudicate.py` · 372 SLOC · LLR 3: 306,310,336 · also CMP-009 (1) · The coordinator's adjudication entry point: one retained session, the loop's.
- `scripts/coordinator_guard.py` · 996 SLOC · LLR 3: 300,301,340 · also CMP-009 (1) · The coordinator context guard: stop new lanes at a context threshold, close out, hand off, and relaunch at session end (WI-822; docs/specs/WI-822.md).
- `scripts/dev-setup.template.ps1` · 390 lines · LLR 1: 336 · also CMP-009 (3) · dev-setup (Windows) — provision the *developer workstation* rung of the onboarding ladder (process.md §7):
- `scripts/dev-setup.template.sh` · 418 lines · LLR 1: 336 · also CMP-009 (4) · dev-setup (Linux/macOS) — provision the *developer workstation* rung of the onboarding ladder (process.md §7):
- `scripts/gen_open_items.py` · 933 SLOC · LLR 1: 283 · also CMP-009 (1) · The owner decision surface, generated (WI-322, OI-10 ruled option (b)).
- `scripts/gen_release_checklist.py` · 315 SLOC · LLR 1: 255 · also CMP-009 (2) · Generate the human release checklist from the registries.
- `scripts/hats.py` · 835 SLOC · LLR 2: 168,297 · also CMP-006 (1) · hats.py — the HATS ROSTER reader: which declared expert perspectives apply to a decomposition, and the block a brief embeds so the session has to face…
- `scripts/held_status.py` · 349 SLOC · LLR 1: 246 · also CMP-006 (1) · THE HELD STATUS — which status cells a delta moves, and whether the dial holds them (SR-208, SR-210).
- `scripts/intake.py` · 1861 SLOC · LLR 8: 153,246,248,255,262,264,265,335 · also CMP-006 (1) · intake.py — the unified trunk-side intake mint (WI-388; docs/concurrency-v2.md §A5.2).
- `scripts/integrate.py` · 1750 SLOC · LLR 14: 140,151,154,207,246,248,262,284,298,300,309,340,345,358 · also CMP-006 (1) · integrate.py — the local integrator: the station protocol and its merge slot.
- `scripts/kitlib/authority.py` · 95 SLOC · LLR 1: 246 · also CMP-006 (1) · Approval authority: which rung a registry's status cells are approved into, whether a declared approval level holds that rung for a human, and what th…
- `scripts/kitlib/config.py` · 225 SLOC · LLR 2: 270,343 · also CMP-006 (1), CMP-007 (3) · Declared policy readers: process toggles, stack-step selectors and console encoding.
- `scripts/kitlib/git.py` · 101 SLOC · LLR 2: 246,303 · also CMP-006 (2), CMP-007 (1) · The best-effort-off-git subprocess pattern — one home for "git, or None".
- `scripts/kitlib/spine.py` · 474 SLOC · LLR 1: 299 · also CMP-006 (15) · The SPINE ROW vocabulary — what one registry row's cells MEAN, stated once.
- `scripts/kitlib/verdict.py` · 743 SLOC · LLR 6: 207,262,310,341,343,345 · also CMP-006 (1) · THE VERDICT RECORD: which artifact carries a lane's governing review verdict, and what binds that verdict to the tree it judged.
- `scripts/pending.py` · 130 SLOC · LLR 1: 283 · also CMP-009 (2) · pending.py — the pending-owner-action read model: what the OWNER still owes.
- `scripts/text_then_act.py` · 128 SLOC · LLR 4: 246,298,345,358 · also CMP-006 (1) · TEXT THEN ACT — the spine text before the approval act (WI-806).
- `scripts/dev-setup.ps1` · 515 lines · LLR 1: 336 · also CMP-009 (2) · dev-setup for THIS repo (the ai-template meta-repo) — the concrete dogfood of the onboarding ladder's dev-setup rung (project-trajectory/PROCESS.md §7…
- `scripts/dev-setup.sh` · 472 lines · LLR 1: 336 · also CMP-009 (1) · dev-setup for THIS repo (the ai-template meta-repo) — the concrete dogfood of the onboarding ladder's dev-setup rung (project-trajectory/PROCESS.md §7…

## 4. Import graph inside W3

From an `ast` pass over each of the 66 Python files: every `import` and `from … import` in the file, function-local ones included, resolved against the kit's own Python files; standard-library imports are dropped. `a -> b, c` means file `a` imports `b` and `c`, both on W3's file list; the kit files outside W3 that `a` imports follow `||`. Paths drop `project-trajectory/scripts/`. Imports do not show subprocess calls or handoffs through files.

```text
acceptance_record -> kitlib/decisions, kitlib/done_when, kitlib/git, kitlib/sitting, kitlib/spine, kitlib/verdict  || kitlib/registry, spine_carrier
adjudicate_act -> acceptance_record, intake, kitlib/authority, kitlib/git, kitlib/sitting, kitlib/spine, prompts  || baseline_snapshot
adjudicate_brief -> acceptance_record, adjudicate_act, agent_brief, agent_common, census, consolidate, handback, intake, kitlib/dispute, kitlib/done_when, kitlib/sitting, prompts, rejudge  || baseline_snapshot, spine_carrier, trace
adoption_record -> acceptance_record, intake, kitlib/adoption, kitlib/config, kitlib/git, kitlib/verdict, spec_move  || kitlib/registry
agent_brief -> agent_common, agent_route, agent_session, intake, integrate, kitlib/decisions, kitlib/done_when, kitlib/provenance, kitlib/verdict, prompts, schedule, score_reviews  || spine_carrier
agent_common -> agent_policy, agent_session, kitlib/config, kitlib/provenance, kitlib/spine  || kitlib/registry, kitlib/secret_classes
agent_loop -> adjudicate_brief, agent_brief, agent_common, agent_route, agent_session, dispatch, intake, integrate, kitlib/commit_hooks, kitlib/config, kitlib/done_when, kitlib/provenance, kitlib/verdict, plan_round, plan_runner, prompts, score_reviews, session_service
agent_policy -> held_status, kitlib/authority, kitlib/config, kitlib/decisions, kitlib/git, kitlib/provenance  || kitlib/ladder, kitlib/stage
agent_route -> agent_session, kitlib/config, kitlib/spine, session_adapters  || spine_carrier
agent_session -> kitlib/winjob
bookkeeping -> agent_common, kitlib/commit_hooks, kitlib/provenance, trunk_step
bootstrap -> kitlib/config, kitlib/spine  || kitlib/bootstrap_manifest
census -> agent_common, schedule  || assumption_rules, trace
check -> acceptance_record, agent_common, held_status, kitlib/authority, kitlib/config, kitlib/git, kitlib/provenance, text_then_act  || kitlib/ladder, kitlib/stage
check_trajectory -> acceptance_record, held_status, kitlib/authority, kitlib/config, kitlib/git, kitlib/provenance, kitlib/spine, observation_cadence  || check_docs, derive_stage, gen_arch_map, kitlib/ladder, kitlib/registry, kitlib/stage, spine_carrier, trajectory_arch
consolidate -> agent_common, check_trajectory, kitlib/spine, schedule, spec_move  || kitlib/registry, spine_carrier
coordinator_adjudicate -> adjudicate_act, adjudicate_brief, agent_brief, agent_common, agent_route, integrate, kitlib/config, kitlib/git, session_service
coordinator_guard -> agent_common, agent_policy, agent_route, kitlib/commit_hooks, kitlib/shell_line, session_keep  || kitlib/guard_hooks, kitlib/observation
dispatch -> agent_common, census, handback, intake, integrate, kitlib/config, kitlib/provenance, kitlib/verdict, lane, pending, schedule, score_reviews, session_service
gen_open_items -> kitlib/config, pending  || baseline_snapshot, spine_carrier, trace
gen_release_checklist -> kitlib/config, kitlib/spine, rejudge  || assumption_rules, spine_carrier
handback -> adoption_record, agent_common, consolidate, intake, integrate, kitlib/adoption, kitlib/provenance, kitlib/spine, kitlib/station, spec_move
hats -> kitlib/config, kitlib/spine  || kitlib/observation, spine_carrier
held_status -> acceptance_record, kitlib/authority, kitlib/git, kitlib/sitting, kitlib/spine  || spine_carrier
intake -> acceptance_record, agent_common, bookkeeping, census, consolidate, kitlib/adoption, kitlib/done_when, kitlib/sitting, kitlib/spine, rejudge, schedule  || baseline_snapshot, kitlib/stage, spine_carrier, trace, wi_convert
integrate -> acceptance_record, agent_common, bookkeeping, coordinator_guard, intake, kitlib/commit_hooks, kitlib/config, kitlib/decisions, kitlib/done_when, kitlib/git, kitlib/provenance, kitlib/station, kitlib/verdict, plan_gate, schedule, score_reviews, spec_move, text_then_act  || kitlib/registry
kitlib/adoption -> (none)  || kitlib/registry
kitlib/authority -> kitlib/git  || kitlib/ladder, kitlib/stage
kitlib/commit_hooks -> kitlib/git
kitlib/config -> (none)  || kitlib/ladder
kitlib/decisions -> (none)
kitlib/dispute -> (none)
kitlib/done_when -> kitlib/decisions, kitlib/git, kitlib/sitting  || kitlib/registry
kitlib/git -> (none)
kitlib/plan_pass -> kitlib/done_when, kitlib/git  || kitlib/registry
kitlib/provenance -> (none)
kitlib/shell_line -> (none)
kitlib/sitting -> kitlib/git, kitlib/verdict  || kitlib/registry
kitlib/spine -> kitlib/config
kitlib/station -> kitlib/config
kitlib/verdict -> kitlib/config, kitlib/git, kitlib/station
kitlib/winjob -> (none)
lane -> agent_common, integrate
migrate_decisions -> kitlib/decisions
observation_cadence -> kitlib/spine  || assumption_rules, spine_carrier
pending -> kitlib/decisions, kitlib/spine  || baseline_snapshot, kitlib/registry, traj_parse
plan_artifacts -> kitlib/spine  || kitlib/registry, trace, wi_convert
plan_briefs -> hats, kitlib/config, kitlib/spine, prompts  || spine_carrier
plan_coverage_step -> kitlib/config
plan_gate -> agent_common, kitlib/config, kitlib/dispute, kitlib/done_when, kitlib/git, kitlib/plan_pass, kitlib/sitting, kitlib/station, kitlib/verdict, score_reviews, spec_move, text_then_act, trunk_step
plan_round -> kitlib/config
plan_runner -> agent_route, agent_session, plan_artifacts, plan_briefs, plan_coverage_step, plan_round, session_service
prompts -> kitlib/config
rejudge -> kitlib/spine, observation_cadence  || assumption_rules, kitlib/observation, kitlib/registry, record_observation, spine_carrier
review_brief -> agent_brief, agent_common, kitlib/config, kitlib/dispute, kitlib/done_when, kitlib/plan_pass, kitlib/spine, kitlib/verdict, plan_gate, prompts, score_reviews  || plan_coverage
schedule -> kitlib/config, kitlib/spine  || kitlib/registry, spine_carrier, trace
score_reviews -> kitlib/config, kitlib/sitting, kitlib/verdict
session_adapters -> (none)
session_keep -> agent_policy, agent_route, kitlib/config, kitlib/git, kitlib/verdict
session_service -> adjudicate_brief, agent_common, agent_route, agent_session, integrate, kitlib/commit_hooks, kitlib/provenance, session_adapters, session_keep
spec_move -> agent_common
text_then_act -> acceptance_record, adoption_record, held_status, kitlib/git  || spine_carrier
trunk_step -> kitlib/config, kitlib/git, plan_artifacts, spec_move  || spine_carrier
usage_ingest -> agent_common, session_adapters, session_service
scripts/coordinator/codex_call -> agent_common, agent_route, coordinator_adjudicate, kitlib/config, session_keep, session_service
scripts/coordinator/overnight_legs -> agent_brief, agent_common, coordinator_guard, kitlib/commit_hooks, kitlib/provenance
```

290 import edges inside W3. In-degree inside W3: kitlib/config 28, agent_common 21, kitlib/git 19, kitlib/spine 19, kitlib/provenance 12, kitlib/verdict 11, kitlib/done_when 9, acceptance_record 9, kitlib/sitting 8, intake 8, agent_route 8, kitlib/decisions 7, integrate 7, prompts 6, spec_move 6, agent_session 6, schedule 6, score_reviews 6, kitlib/commit_hooks 6, session_service 6, kitlib/authority 5, agent_brief 5, held_status 4, kitlib/station 4, census 3, consolidate 3, kitlib/dispute 3, rejudge 3, kitlib/adoption 3, agent_policy 3, adjudicate_brief 3, session_adapters 3, text_then_act 3, session_keep 3, adjudicate_act 2, handback 2, plan_round 2, trunk_step 2, observation_cadence 2, pending 2, adoption_record 2, bookkeeping 2, coordinator_guard 2, plan_gate 2, kitlib/plan_pass 2, plan_artifacts 2, dispatch 1, plan_runner 1, kitlib/winjob 1, check_trajectory 1, kitlib/shell_line 1, lane 1, hats 1, plan_briefs 1, plan_coverage_step 1, coordinator_adjudicate 1. Python files no other W3 file imports: agent_loop, bootstrap, check, gen_open_items, gen_release_checklist, migrate_decisions, review_brief, usage_ingest, scripts/coordinator/codex_call, scripts/coordinator/overnight_legs.

Kit files outside W3 that W3 files import (number of W3 importers): spine_carrier 17, kitlib/registry 14, trace 6, baseline_snapshot 5, kitlib/ladder 5, kitlib/stage 5, assumption_rules 4, kitlib/observation 3, wi_convert 2, kitlib/secret_classes 1, kitlib/bootstrap_manifest 1, check_docs 1, derive_stage 1, gen_arch_map 1, trajectory_arch 1, kitlib/guard_hooks 1, traj_parse 1, record_observation 1, plan_coverage 1.

## 5. Interfaces

### 5a. Internal interfaces (65; by channel: call 52, exit-code 6, cli 4, file 2, env 1)

- IF-009 `exit-code` check_trajectory → cons: check · 0 clean · 1 hard error · 2 usage
- IF-040 `exit-code` check → cons: project-trajectory/hooks/pre-commit · 0 pass or SKIP · 1 any step FAILs
- IF-044 `call` agent_route → req: agent_loop, session_service, plan_runner, coordinator_adjudicate · resolve_enabled(tokens, registry) -> enabled entries, errors; resolve_entry(token, registr…
- IF-046 `call` score_reviews → req: agent_loop, dispatch, integrate, *gen_verdict_rollup*, kitlib/verdict, *plan_coverage*, review_brief · parse_verdict: typed verdict findings, where a finding is a bullet whose bracket names one…
- IF-053 `call` schedule → req: census, dispatch, intake · cmp CMP-008 · load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and in…
- IF-055 `call` schedule → req: integrate · cmp CMP-008 · frontier over the loaded rows, in deterministic order
- IF-058 `call` plan_round → req: plan_runner, agent_loop · cmp CMP-008 · disposition: CONTINUE · SELECTED · PAGE
- IF-061 `call` plan_artifacts → req: plan_runner · cmp CMP-008 · allocate_round_dir, write_stage, append_log_summary, file_selected_wis
- IF-064 `call` agent_session → req: agent_loop, session_service, plan_runner · build_argv, run_session, parse_json_result and the console renderers
- IF-065 `call` agent_common → req: agent_loop, integrate, session_service, usage_ingest · END_STATES, git, head_sha, acquire_lock, release_lock, preflight, parse_map, process_confi…
- IF-066 `call` plan_runner → req: agent_loop · plan_runner.wi_plan_mode and run_dual_plan_round -> (SELECTED | PAGE, detail)
- IF-081 `exit-code` trunk_step → cons: integrate, bookkeeping, *external:downstream adopter* · cmp CMP-008 · crosses B-05 · 0 all clean · 1 any failure, the offending file named
- IF-088 `call` pending → req: dispatch · cmp CMP-008 · pending.owner_cards -> PendingItem(kind, line) with kind blocked or spine; the pause kind…
- IF-090 `call` intake → req: integrate, dispatch, agent_loop, adjudicate_act, adjudicate_brief · cmp CMP-008 · merge intake, gap minting, advisory context, and adjudication-action policy
- IF-091 `call` acceptance_record → req: intake, integrate · cmp CMP-008 · Approval delta plus merge_approval_refusal(root, base, head, metas, trunk) acceptance or r…
- IF-097 `call` prompts → req: agent_loop, plan_briefs · cmp CMP-008 · load | fill | preflight | digest | template_path | strip_dispatcher_block; KIT_PROMPTS | K…
- IF-099 `call` prompts → req: agent_loop · cmp CMP-008 · WORKER · REVIEWER · CRITIQUE
- IF-100 `call` prompts → req: plan_briefs · cmp CMP-008 · strip_dispatcher_block, strict_check — the {{NAME}} hat fill
- IF-113 `call` prompts → req: adjudicate_brief, adjudicate_act · cmp CMP-008 · ADJUDICATE-AMENDMENT · ADJUDICATE-DISPOSITION · ADJUDICATE-RED-TC · ADJUDICATE-DONE-WHEN ·…
- IF-115 `call` adjudicate_brief → req: agent_loop · cmp CMP-008 · compose(...) -> text | reason; record_outcome(...) -> (accepted | failed, why | None)
- IF-129 `call` acceptance_record → req: *baseline_snapshot*, held_status, adjudicate_brief, adjudicate_act · split_changed_cells; approved_text_digest(registry, id_col, row) -> sha256:<16 lowercase h…
- IF-136 `call` lane → req: dispatch · cmp CMP-008 · lane.ensure_worktree -> (path, error); spawn_worker -> (Popen, refusal); spawn_refresh ->…
- IF-137 `call` handback → req: dispatch · cmp CMP-008 · close_partial and quarantine
- IF-154 `cli` integrate → req: lane, *external:downstream adopter* · cmp CMP-008 · claim --wi --branch · refresh --branch --tier · attest --branch --bar --tests --message-fi…
- IF-155 `cli` trunk_step → req: integrate, bookkeeping, *external:downstream adopter* · cmp CMP-008 · --compile-log · --regen · neither = both, compile first; --root and --dry-run on either
- IF-173 `call` integrate → req: agent_loop, dispatch, handback, lane · cmp CMP-008 · claim, refresh, attest, integrate, finished_branches, branch_outcomes, lane_worktree, the…
- IF-175 `call` kitlib/verdict → req: integrate, agent_loop, dispatch, *gen_verdict_rollup*, score_reviews, acceptance_record, adjudicate_act, review_brief, adoption_record · cmp CMP-008 · tree identity; branch rounds/trailers; row rulings and blessed rows; scope, phase, filing…
- IF-177 `call` check_trajectory → req: consolidate · cmp CMP-006 · queue_conflict_pairs(model) -> the (row, row, signal) pairs the queue-conflict detector re…
- IF-186 `call` bookkeeping → req: integrate, intake · cmp CMP-008 · commit(root, scope | scope(scratch) -> (paths, refusal), write(scratch), message, label, b…
- IF-194 `call` kitlib/provenance → req: agent_common, agent_loop, bookkeeping, check, check_trajectory, dispatch, handback, integrate, session_service · cmp CMP-008 · LOOP_TRAILER/LOOP_SESSION_ENV;format/parse_loop_trailer, loop_{trailer_refusal,writer_comm…
- IF-195 `call` kitlib/authority → req: acceptance_record, agent_common, check, check_trajectory, integrate, adjudicate_act · cmp CMP-006 · APPROVAL_RUNGS, SPINE_APPROVAL_RUNGS; rung_for -> rung|None; read_dial -> (rung, legacy);…
- IF-196 `call` held_status → req: agent_policy, check, check_trajectory, text_then_act · cmp CMP-008 · status moves; held_status_lines; held_status_refusal; HELD_TIERS; HELD_PATHS; registry_hel…
- IF-197 `exit-code` check → cons: hooks/commit-msg · cmp CMP-007 · --loop-trailer MSGFILE: 0 unmarked, or a valid trailer naming the marked session · 1 marke…
- IF-228 `call` rejudge → req: intake, gen_release_checklist, adjudicate_brief · cmp CMP-008 · observation_test_cases(root, rev) · due_cases(root, rev, now) -> tc, row, why, digest, rec…
- IF-242 `call` kitlib/done_when → req: integrate, intake, agent_loop, *plan_coverage*, adjudicate_brief · cmp CMP-008 · Done-when item and comparison schema; see Contract IF-242 in the owner module.
- IF-245 `call` session_adapters → req: session_service, agent_route, usage_ingest · cmp CMP-008 · USAGE_KEYS, OTEL_SEMCONV; adapter_for(argv) -> adapter; adapter methods; HOME_VARIABLES, T…
- IF-246 `call` session_service → req: agent_loop, plan_runner, dispatch, coordinator/codex_call, usage_ingest · cmp CMP-008 · Call (including wi and resume), Outcome; act -> Outcome or BlackoutRefused or HooksOffRefu…
- IF-247 `file` session_keep → cons: agent_loop, dispatch · cmp CMP-008 · out/adjudicator/<FAMILY>-<hash of route id, NUL scope, NUL account>.json; identity family,…
- IF-248 `call` session_keep → req: session_service · cmp CMP-008 · KeepConfig; keep_for; keep_bookkeep; keep_release; keep_abandon; take_warm_lease; review_r…
- IF-255 `file` kitlib/decisions → cons: acceptance_record, integrate, pending · cmp CMP-008 · docs/decisions/<run>.toml: high_risk (entry ids); [decision.D-<n>] decided, alternative, r…
- IF-256 `call` kitlib/decisions → req: acceptance_record, agent_common, agent_loop, gen_open_items, integrate, migrate_decisions, pending · cmp CMP-008 · record_path (raises ValueError for a run name no record can carry: # or a character git re…
- IF-260 `call` agent_brief → req: agent_loop, adjudicate_brief, coordinator_adjudicate · cmp CMP-008 · brief constructors, prompt routing, guardrails payload selection, and assignment-facing la…
- IF-261 `call` agent_policy → req: agent_common · cmp CMP-008 · process-config readers and findings, approval authority decisions, and normalized coordina…
- IF-264 `call` schedule → cons: *traj_status*, agent_brief, dispatch, integrate · cmp CMP-008 · work rows and their needs OI edges -> readiness records carrying unmet item ids and titles
- IF-266 `call` session_adapters → cons: session_service, session_keep · cmp CMP-008 · compaction(stream, env, session_id) -> {reported: bool, prompts: list[int], totals: list[i…
- IF-267 `cli` check → cons: hooks/pre-commit · cmp CMP-007 · --path-triggered: run only path-declaring steps except smoke selected by the shared rung-o…
- IF-269 `call` observation_cadence → req: rejudge, check_trajectory · cmp CMP-008 · Cadence(root, revision, snapshot, checkpoint, git).eligible(row, since, checkpoint) -> boo…
- IF-271 `call` coordinator_guard → req: integrate · cmp CMP-008 · claim_refusal(root, env=None) -> None | blackout or guard refusal text
- IF-272 `call` session_keep → req: coordinator_guard · cmp CMP-008 · primary_out_dir(root) -> Path
- IF-273 `call` session_keep → req: coordinator_guard · cmp CMP-008 · dir_lock(directory, wait=10.0) -> context manager yielding Path; raises StoreBusy
- IF-278 `env` coordinator_guard → req: coordinator-relaunch.cmd, coordinator-relaunch.sh · cmp CMP-008 · PT_COORDINATOR_TAKE: successor token supplied for SessionStart lease take
- IF-279 `cli` coordinator_guard → cons: coordinator-relaunch.cmd, coordinator-relaunch.sh · cmp CMP-008 · REPO_ROOT PROMPT_FILE TOKEN; POSIX reads PROMPT_FILE, Windows calls exec-claude --prompt-f…
- IF-282 `call` session_service → req: agent_loop, coordinator_adjudicate, coordinator/codex_call · cmp CMP-008 · AdjudicationRequest(route, scope, account); route_runner(entry); prepare_launch(root, row,…
- IF-286 `call` kitlib/done_when → req: agent_loop, integrate, intake, adjudicate_brief · cmp CMP-008 · Done-when blessing, cover, hold and closure schema; see Contract IF-286 in the owner modul…
- IF-287 `call` kitlib/sitting → req: adjudicate_brief, acceptance_record, consolidate, intake, review_brief, score_reviews, *plan_coverage*, adjudicate_act, held_status · cmp CMP-008 · binding/path grammar; requested, identity and findings-file cells; outcome; combined-scope…
- IF-290 `call` kitlib/dispute → req: adjudicate_brief, *plan_coverage*, plan_gate, review_brief · cmp CMP-008 · read_findings(text, where); request_line(ids); file_line(path); requested_ids(brief_text);…
- IF-291 `call` agent_policy → req: agent_loop, session_service, session_keep, dispatch, coordinator_guard · cmp CMP-008 · blackout_at(docs, t=None) -> Blackout(window, at, end?, last_end?); inside and wake_second…
- IF-294 `call` kitlib/adoption → req: intake, handback, adoption_record · cmp CMP-008 · parse_block; disposed_id; row_refusal over a supplied listing; record_ids and record-chang…
- IF-295 `exit-code` plan_gate → cons: check · cmp CMP-008 · [--root DIR]: exit 0 when the commit being made is not held, 1 naming each hold; writes no…
- IF-296 `call` adjudicate_act → req: coordinator_adjudicate, adjudicate_brief · cmp CMP-008 · ACTABLE; owed_acts; left_owed; bound_brief; amendment retires; act_values; compose_act; he…
- IF-297 `call` kitlib/commit_hooks → req: agent_loop, session_service, bookkeeping, integrate, coordinator_guard · cmp CMP-008 · hooks_refusal(root) -> None | cause and matching repair text
- IF-302 `call` kitlib/winjob → req: agent_session · cmp CMP-008 · win32() -> (kernel32, ntdll); JobAccounting; job_active_processes(job) -> int; create_join…
- IF-303 `call` adoption_record → req: handback, text_then_act · cmp CMP-008 · tree_specs(root, rev); validate_at(root, rev, title, owes, adoptions) -> record or refusal…
- IF-304 `exit-code` adoption_record → cons: check · cmp CMP-008 · [--root DIR]: exit 0 when the staged adoption-record change is admitted, 1 naming each ref…
- IF-308 `call` acceptance_record → req: check, text_then_act · cmp CMP-008 · staged_parent_first_lines(root) and commit_parent_first_lines(root, rev) return parent-fir…

### 5b. Boundary interfaces (121; by channel: call 40, exit-code 29, file 25, cli 14, stdout 9, bytes 2, git 1, env 1)

- IF-001 `stdout` *trace* → cons: check · orphan, integrity, status and advisory findings, printed whole for the harness to relay
- IF-002 `exit-code` *check_docs* → cons: check · 0 pass · 1 broken link, README finding, or strict-mode orphan
- IF-003 `exit-code` *check_flows* → cons: check · 0 pass | 1 findings | 2 usage
- IF-004 `stdout` *check_perf* → cons: check · check_perf: OK - <summary> or FAIL - <summary>, plus one <status> - <PB-ID> <metric> line…
- IF-005 `stdout` *check_privacy* → cons: check · one line per leak: <location>: [<label>] <excerpt>, then one summary line naming the scan…
- IF-006 `exit-code` *check_stubs* → cons: check · 0 pass or warn · 1 stub found under --strict
- IF-008 `stdout` *check_doc_refs* → cons: check · dangling and untraced findings by file:line, with per-tier counts
- IF-010 `cli` *gen_arch_map* → req: check, trunk_step · --doc | --cli-doc | --contracts-doc | --src | --mode | --check | --strict-parse | --backli…
- IF-011 `exit-code` *gen_trajectory* → cons: check · 0 clean or vacuous · 1 invalid registry, stale HTML, or stale status snapshot under --chec…
- IF-012 `exit-code` *gen_okf* → cons: check, trunk_step · 0 clean, vacuous or opted out · 1 stale, missing or extra bundle file under --check
- IF-013 `exit-code` check → cons: *external:downstream adopter* · crosses B-05 · 0 pass · 1 fail · 2 usage
- IF-014 `bytes` bootstrap → cons: *external:downstream adopter* · crosses B-05 · the scaffolded template tree written under the destination root
- IF-015 `git` agent_loop → cons: *external:downstream adopter* · crosses B-05 · 0 DONE · 2 preflight · 3 BLOCKED · 4 stall · 5 WAITING · 6 budget · 7 NEEDS-HUMAN · 8 paus…
- IF-018 `file` gen_release_checklist → cons: *external:downstream adopter* · crosses B-05 · docs/release-checklist.md — human-verified rows use `- [ ] <ID> — <what to confirm> (refs)…
- IF-022 `file` *docs/stack.ini* → cons: check, *external:downstream adopter* · crosses B-05 · sections: paths, product, tiers, coverage, arch-map, readability, bars, step:NAME
- IF-023 `file` *docs/work/* → cons: check_trajectory, *external:downstream adopter* · crosses B-05 · one Markdown spec per row; status is the directory
- IF-034 `file` *docs/requirements/* → cons: gen_release_checklist, *external:downstream adopter* · crosses B-05 · (no data cell)
- IF-035 `file` *project-trajectory/skills/* → cons: *gen_skills_index*, bootstrap · SKILL.md frontmatter: name, scope, stacks, domains, phases, tags; each other file in the s…
- IF-037 `file` *docs/process.toml* → cons: agent_common, agent_loop, bootstrap, *check_privacy*, check_trajectory, dispatch, *gen_arch_map*, *gen_okf*, integrate, kitlib/config, *subagent_gate*, *external:downstream adopter* · crosses B-05 · sections: attestation, policies, checks, build; one key = value per line
- IF-039 `bytes` *registries* → cons: bootstrap · one template file per registry tier
- IF-041 `cli` *external:agent CLI* → req: agent_session · headless invocation; the prompt on stdin
- IF-042 `exit-code` *trace* → cons: project-trajectory/hooks/pre-commit · 0 no integrity finding · 1 integrity finding
- IF-045 `file` *docs/agents.toml* → cons: agent_route · route rows: Id, Family, Model, Version, Tier, CmdTemplate, Env, Notes; account tables: cli…
- IF-047 `file` *docs/reviews/* → cons: score_reviews, check_trajectory, integrate, kitlib/verdict, *gen_verdict_rollup*, *plan_coverage*, review_brief · VERDICT: APPROVE | CHANGES-REQUESTED findings=N; finding is - [BLOCKER|MAJOR|MINOR] <text>…
- IF-050 `file` *derive_stage* → cons: check, agent_common, check_trajectory, *traj_parse*, intake · cmp CMP-006 · docs/stage — key = value fields plus a sha256 fingerprint of the declared inputs
- IF-054 `file` *docs/work/* → cons: schedule, *external:downstream adopter* · cmp CMP-008 · crosses B-05 · status; needs edges (WI-### or OI-###; ~ is soft); pending OI blocks its citer; absent saf…
- IF-056 `call` check_trajectory → req: *gen_trajectory* · cmp CMP-009 · check_trajectory loaders: validate, read_registry_rows, load_wis, load_known_srs, read_tra…
- IF-059 `file` *docs/requirements/* → cons: plan_briefs, *external:downstream adopter* · cmp CMP-008 · crosses B-05 · SR id, title, requirement; IF id, owner, far side, channel, data
- IF-060 `exit-code` *plan_coverage* → cons: plan_coverage_step · cmp CMP-008 · 0 clean | 1 findings, including unexplained clause gaps or SINGLE SR/TC misses | 2 malform…
- IF-068 `file` *docs/stack.ini* → cons: agent_loop, *external:downstream adopter* · crosses B-05 · [agent-loop]: model, model-map
- IF-069 `exit-code` *check_coverage* → cons: check · 0 every floor holds or unmeasured · 1 below floor, absent module, or corrupt input
- IF-071 `call` schedule → req: *gen_trajectory* · cmp CMP-009 · load_registry_rows, load_wis, frontier, evaluate; empty when the module is absent
- IF-073 `file` *docs/requirements/open-items.toml* → cons: gen_open_items, *external:downstream adopter* · crosses B-05 · status: pending | ruled; queued work-item needs edges cite pending items
- IF-074 `file` gen_open_items → cons: *external:downstream adopter* · crosses B-05 · docs/open-items.html — cited pending decisions, uncited-item notice, approval/re-attest ch…
- IF-075 `call` *trace* → req: gen_open_items, adjudicate_brief · reattest_model entries: chain rows, changed cells, baseline rev and date, and each spine r…
- IF-077 `call` *check_docs* → req: check_trajectory · cmp CMP-006 · parse_doc: one document's outbound links and its anchor set
- IF-078 `call` *wi_convert* → req: plan_artifacts · cmp CMP-008 · wi_convert.write_spec_file with work_dir_for and spec_paths; ConvertError on a status the…
- IF-080 `exit-code` integrate → cons: *external:downstream adopter* · cmp CMP-008 · crosses B-05 · claim | refresh | attest | integrate | done-when-hold | audit; nonzero exit on any refusal…
- IF-082 `call` check_trajectory → req: *traj_parse* · cmp CMP-009 · check_trajectory loaders: read_rows, spine_carrier, SR_CSV, _arch_scan_profile
- IF-083 `call` check_trajectory → req: *rendering/traj_views* · cmp CMP-009 · check_trajectory joins: read_rows, load_seams, component_top_view, _norm_module, _split_re…
- IF-084 `call` check_trajectory → req: *traj_status* · cmp CMP-009 · check_trajectory loaders: load_ifs, IF_CSV, spine_carrier
- IF-085 `call` schedule → req: *traj_parse* · cmp CMP-009 · the module object or None, the guarded import's two outcomes
- IF-086 `exit-code` *check_figures* → cons: check · 0 warn-first · 1 under --strict
- IF-089 `call` *trace* → req: census, *check_assumption_gate* · cmp CMP-008 · load_registries then analyze: orphans, status_findings and the findings bag; load_registri…
- IF-092 `call` *wi_convert* → req: intake · cmp CMP-008 · wi_convert.COLUMNS (the 19-column row schema) and write_spec_file; ConvertError is the min…
- IF-093 `call` kitlib/station → req: *rendering/traj_panels* · cmp CMP-009 · OUTCOME_DIRS: complete · cancelled · partial; BAR_GREEN
- IF-094 `call` schedule → req: *rendering/traj_panels* · cmp CMP-009 · _KIND_CONCURRENCY, _KIND_RANK and CONCURRENCY_EXCLUSIVE, read as constants
- IF-098 `call` prompts → req: *gen_prompt_catalog* · cmp CMP-009 · catalog_rows() -> (key, file, slots, digest); fragment_rows() -> (file, slot, digest)
- IF-101 `call` *trace* → req: intake, plan_artifacts · cmp CMP-008 · read_watermark and bump_watermark over docs/id-watermark; a mint counts from max(mark, liv…
- IF-102 `call` *spine_carrier* → req: *trace*, acceptance_record, text_then_act, check_trajectory, *gen_arch_map*, *plan_coverage*, *spine_rules*, *traj_status*, *check_test_first*, rejudge, *retire*, observation_cadence · cmp CMP-006 · spine_carrier readers: load, resolve, tier_carriers, tier_rows_from_text, rows_from_text,…
- IF-107 `call` *spine_carrier* → req: gen_release_checklist · cmp CMP-009 · spine_carrier.load for SR, TC, LLR and IF rows by phase; folded_needs for the need tier; a…
- IF-108 `call` *spine_carrier* → req: plan_briefs · cmp CMP-008 · spine_carrier.load over system-requirements and interfaces; rows in file order under today…
- IF-109 `call` *spine_carrier* → req: agent_brief · cmp CMP-008 · spine_carrier.load over the SR and TC tiers; SR Verification gates the critique round, SR…
- IF-110 `call` *spine_carrier* → req: intake · cmp CMP-008 · spine_carrier.load over LLR, TC, IF, CMP and open-item rows; resolve, stem, CARRIERS, NEED…
- IF-114 `call` *spine_carrier* → req: adjudicate_brief · cmp CMP-008 · spine_carrier.load over the TC, SR and LLR tiers; every listed cell required, read-only
- IF-118 `call` *spine_carrier* → req: gen_open_items · cmp CMP-009 · spine_carrier.resolve and load over docs/requirements/open-items; [] only when absent, Sys…
- IF-119 `call` *spine_carrier* → req: agent_route · cmp CMP-008 · spine_carrier.resolve and rows_seq_from_text over docs/agents; an unparseable registry is…
- IF-120 `call` *spine_carrier* → req: trunk_step · cmp CMP-008 · spine_carrier.resolve as the applicability predicate; None when absent, raises on a stem l…
- IF-121 `exit-code` *check_need_form* → cons: check · 0 warn-first · 1 under --strict
- IF-123 `call` *baseline_snapshot* → req: intake · copy_live, parse_approves, parse_reattests, act_summary, tier_owing, load_all, rows_for, e…
- IF-124 `call` *baseline_snapshot* → req: adjudicate_brief, adjudicate_act · exists, stamp, SNAPSHOT_DIR, SNAPSHOT_TIERS and format_approves
- IF-125 `call` *baseline_snapshot* → req: pending · load_all, rows_for, is_drifted and SNAPSHOT_DIR
- IF-126 `call` *baseline_snapshot* → req: gen_open_items · registry_stamps and SNAPSHOT_DIR
- IF-131 `call` *gen_arch_map* → req: check_trajectory · cmp CMP-006 · scan_inventory, contracts_grammar_findings, file_contracts, file_grammar_findings, owner_f…
- IF-133 `call` *spine_carrier* → req: hats · cmp CMP-008 · spine_carrier.load_needs, load, resolve, stem, folded, NEED_CARRIERS; absent registry [] a…
- IF-134 `exit-code` hooks/pre-commit → cons: *external:git* · cmp CMP-007 · crosses B-04 · exit 0 admits the commit; nonzero refuses it
- IF-139 `exit-code` *gen_components* → cons: check · 0 current or vacuous · 1 stale or missing
- IF-144 `exit-code` check → cons: *external:downstream adopter* · crosses B-05 · severity: OK · SKIP · WARN · FAIL
- IF-145 `exit-code` *trace* → cons: check · 0 clean · 1 a finding under --strict, an integrity finding under --strict-integrity, or a…
- IF-147 `exit-code` *check_perf* → cons: check · 0 OK, SKIP or WARN · 1 a Gate=fail budget breached in the run tier, or --update-baseline w…
- IF-148 `exit-code` *check_privacy* → cons: check · 0 clean or both layers off · 1 one or more findings in the tracked-file sweep
- IF-150 `exit-code` *gen_arch_map* → cons: check, trunk_step · 0 current · 1 a stale target under --check, an unparseable module under --strict-parse, or…
- IF-152 `cli` *plan_coverage* → req: plan_coverage_step · cmp CMP-008 · --goal | --item [--findings], --root, --out, then the plan paths
- IF-153 `file` *plan_coverage* → cons: plan_coverage_step · cmp CMP-008 · the --out coverage report: coverage and exclusions per plan, a SINGLE SR/TC diff, and a pa…
- IF-156 `file` *docs/log.d/* → cons: trunk_step · one fragment per session, <id>-<slug>.md, opening with a `## ` heading; links written rela…
- IF-160 `file` *docs/reviews/* → req: score_reviews · scoreboard.txt — the decayed per-provider substance tallies and the round history
- IF-161 `file` *docs/test/* → cons: acceptance_record, adjudicate_brief, agent_loop, *baseline_snapshot*, *check_doc_refs*, *check_flows*, check_trajectory, *gen_okf*, gen_release_checklist, intake, *plan_coverage*, *spine_rules*, *trace*, *traj_parse*, *external:downstream adopter* · crosses B-05 · test-cases.toml: id-keyed TOML, one [test.TC-###] table per case; ids are the table keys
- IF-162 `file` *docs/agents-enabled* → cons: agent_route, dispatch · one entry per line in preference order (a registry id, optionally ROUTE@ACCOUNT), optional…
- IF-163 `file` *docs/status.md* → cons: agent_common, *check_docs*, check_trajectory, *gen_okf*, integrate, trunk_step · the hand-authored blackboard outside the GENERATED STATUS marker pair; the block between t…
- IF-164 `file` *traj_status* → cons: agent_common, *external:downstream adopter* · crosses B-05 · docs/status.md generated block: stage, spine counts, ready frontier, cited items and held…
- IF-165 `exit-code` *derive_stage* → cons: check, trunk_step, *kitlib/stage* · 0 fresh, placeholder, printed or written · 1 an absent or stale docs/stage under --check,…
- IF-168 `file` *docs/log.d/* → req: trunk_step, *external:downstream adopter* · a session adds one fragment; trunk_step --compile-log unlinks each fragment it appended, a…
- IF-170 `file` *subagent_gate* → cons: agent_loop, *external:downstream adopter* · crosses B-05 · one tab-separated line per non-deferred decision - tool, decision, reason - appended best-…
- IF-171 `cli` schedule → req: *external:downstream adopter* · cmp CMP-008 · --root before the subcommand; ready --explain --format text|json; simulate --jobs N --form…
- IF-172 `stdout` schedule → cons: *external:downstream adopter* · cmp CMP-008 · crosses B-05 · the frontier or the simulation rounds: fixed-width text lines, or JSON - a record array fo…
- IF-176 `call` *trace* → req: schedule · cmp CMP-006 · open_item_states(root) -> {OI-###: lowercased status}, or None where the repo carries no o…
- IF-178 `call` *spine_carrier* → req: consolidate · cmp CMP-006 · resolve(root) -> the spine carrier (TOML or CSV) the repo declares; the consolidation dige…
- IF-179 `call` agent_common → req: *gen_verdict_rollup* · cmp CMP-008 · git(root, *argv) -> (code, out); trunk_name(root) -> the declared trunk's name, or raises…
- IF-187 `exit-code` *check_readability* → cons: check · cmp CMP-007 · 1 only when a gating measure worsened · 0 otherwise: no or only reporting worsenings, no o…
- IF-189 `call` agent_common → req: *check_readability* · cmp CMP-008 · default_base(root) -> the merge base of HEAD with the declared trunk (HEAD on an unrelated…
- IF-198 `exit-code` *check_test_first* → cons: check · cmp CMP-007 · 0 for every report: none, a finding, an unreadable history or an unreadable declared start…
- IF-200 `call` *assumption_rules* → req: *trace*, rejudge, *record_observation*, observation_cadence, gen_release_checklist · cmp CMP-006 · observation_tc_findings -> (failures, advisories); data: is_observation_tc, sampling_model…
- IF-201 `call` *assumption_rules* → req: *derive_stage*, census · cmp CMP-006 · da_citing_srs(srs) -> {assumption id: [requirement ids]}
- IF-215 `cli` *record_observation* → req: *external:downstream adopter*, *check_assumption_gate*, rejudge, *trace* · cmp CMP-006 · --tc --outcome pass|fail --by [--expires] [--root]: one record or a REFUSED line and exit…
- IF-220 `file` *baseline_snapshot* → cons: acceptance_record · cmp CMP-006 · the act ledger acts.toml beside the snapshot copies: [[act]] seq (a positive integer, uniq…
- IF-224 `call` agent_common → req: *trace* · cmp CMP-008 · human_approves_spine(docs, registry) -> True when the dial holds the registry's rung or no…
- IF-229 `cli` intake → req: *external:downstream adopter* · cmp CMP-008 · rejudge --checkpoint release [--rev <commit>] [--root]: one queued rejudge adjudication ro…
- IF-230 `exit-code` *check_assumption_gate* → cons: check · cmp CMP-007 · --step assumption-gate|crossing-allocation|interface-allocation|assumption-evidence [--roo…
- IF-243 `cli` intake → req: *external:downstream adopter* · cmp CMP-008 · consolidate [--dry-run] [--root] · exit 0 minted one row, proposed nothing (its reason pri…
- IF-244 `cli` intake → req: *external:downstream adopter* · cmp CMP-008 · sweep [--before SHA] [--after SHA] [--branch LABEL] [--with-terminal | --merged WI-###[;WI…
- IF-253 `file` agent_loop → cons: *external:downstream adopter* · cmp CMP-008 · crosses B-05 · core.<substring>.md beside the vendored guardrails core: a payload for models whose name c…
- IF-254 `exit-code` *gen_skills_index* → cons: check · cmp CMP-009 · --check: 0 index fresh and descriptions at or over the floor, or no skills dir · 1 stale i…
- IF-262 `call` *kitlib/bootstrap_manifest* → req: bootstrap · cmp CMP-009 · MAPPING and mapping_entries: the ordered scaffold source, destination, and optional requir…
- IF-263 `call` *trajectory_arch* → req: check_trajectory · cmp CMP-006 · architecture inventories and findings for seams, contracts, components, code symbols, and…
- IF-265 `call` *spine_carrier* → cons: schedule · cmp CMP-006 · open-items registry path -> carrier-neutral OI rows
- IF-274 `cli` coordinator_guard → req: *external:agent CLI* · cmp CMP-008 · hook event JSON on stdin: hook_event_name, session_id, transcript_path, agent_id?, reason?…
- IF-275 `stdout` coordinator_guard → cons: *external:agent CLI* · cmp CMP-008 · hook JSON: hookEventName/context; blackout denial adds permissionDecision=deny and reason,…
- IF-277 `env` *external:agent CLI* → cons: coordinator_guard · cmp CMP-008 · CLAUDE_CODE_SESSION_ID: session id; CLAUDE_PROJECT_DIR: default repository root for guard…
- IF-280 `cli` coordinator_guard → req: *external:agent CLI* · cmp CMP-008 · take | request-relaunch --handoff | handback --handoff | release --reason | clear --reason…
- IF-281 `exit-code` coordinator_guard → cons: *external:agent CLI* · cmp CMP-008 · 0 success; 1 refusal or window-check inside blackout; 2 usage error; hook always 0
- IF-283 `cli` coordinator_adjudicate → req: *external:coordinator* · cmp CMP-008 · adjudicate and act command lines; --route names an enabled entry (default ANTHROPIC-OPUS-S…
- IF-284 `exit-code` coordinator_adjudicate → cons: *external:coordinator* · cmp CMP-008 · adjudicate: 0 valid|1 failed|2 pre-launch/blackout refusal|7 account authentication, accou…
- IF-285 `stdout` coordinator_adjudicate → cons: *external:coordinator* · cmp CMP-008 · adjudicate and act readings: keep, exit and refusal; act also reports owed-after, verdict-…
- IF-288 `cli` review_brief → req: *external:coordinator* · cmp CMP-008 · review / critique [--plan --sha] / file / plan [--revise] / plan-file (--critique --sha |…
- IF-289 `exit-code` review_brief → cons: *external:coordinator* · cmp CMP-008 · 0 brief written, or review, critique, dispute findings or pass record filed | 2 refused; a…
- IF-292 `cli` dev-setup.template.sh → req: *external:run.* launcher templates* · crosses B-05 · bare run invokes --for-run/-ForRun once from the repository root, passing --python/-Python…
- IF-293 `exit-code` dev-setup.template.sh → cons: *external:run.* launcher templates* · crosses B-05 · 0 says the handed interpreter meets the runtime floor; nonzero, including none handed, lea…
- IF-298 `stdout` *check_privacy* → cons: hooks/pre-commit, hooks/commit-msg, *hooks/pre-push* · cmp CMP-007 · one answer, no newline: privacy=off | privacy=on review=require | privacy=on review=warn-u…
- IF-305 `cli` usage_ingest → req: *external:coordinator* · cmp CMP-008 · [--session ID] [--root DIR]; ambient home and session selection
- IF-306 `stdout` usage_ingest → cons: *external:coordinator* · cmp CMP-008 · recorded, unchanged, open, skipped, refused, absent, parent-unresolved lines prefixed by r…
- IF-307 `exit-code` usage_ingest → cons: *external:coordinator* · cmp CMP-008 · 0 no refusal, absence, or record-commit refusal; 1 refusal, absent transcript, or refused…

## 6. The lane's runtime flow: Flow 4, verbatim

Quoted from `docs/runtime-flows.md`, its heading demoted one level. The parenthesised ids are the requirement rows the flow cites.

#### Flow 4 — Station cycle: admission, lane, refresh, merge slot, intake (LLR-058, LLR-059, LLR-123, LLR-138, LLR-140)

One tick of `dispatch.run`. The three properties hardest to read off the rows:
the **spine barrier** is a property of admission (nothing slips past an
exclusive kind into a free lane), the **bar is attested to a tree** on the
branch *before* the merge slot rather than run on a composed tree inside it,
and **every lane ends in a merge** — a worker that cannot finish hands back and
the run keeps going.

```mermaid
sequenceDiagram
    participant Sched as schedule.py frontier (LLR-058/LLR-123, LLR-152)
    participant Disp as dispatch.py tick loop (LLR-149)
    participant Lane as lane.py worktree + subprocesses (LLR-150)
    participant Hand as handback.py (LLR-144)
    participant Slot as integrate.py merge slot (LLR-140/LLR-151)
    participant Intake as intake.py (LLR-153/LLR-154)
    loop each tick, until a fatal code or a drained queue
        Disp->>Disp: tracked pause? dirty trunk? (LLR-138) — freeze admission, let lanes come home
        Disp->>Disp: blackout window open? (LLR-300) — claim nothing; an idle station waits it out
        Disp->>Sched: re-derive the ready frontier as (WI, kind) pairs
        Sched-->>Disp: exclusive kinds ranked ahead of parallel ones (LLR-059/LLR-123)
        alt an exclusive kind is on the frontier
            Note over Disp: THE SPINE BARRIER — admission stops outright;<br/>the batch admits alone, sole toucher of trunk
        else free lane and parallel work
            Disp->>Slot: claim, dispatch lock held (LLR-140/LLR-151)
            Note over Disp,Slot: inactive commit hooks refuse before the coordinator guard<br/>and dispatch lock (SR-240/LLR-340)
            Slot-->>Disp: spec to active/&lt;branch&gt;/ on a trunk commit, branch cut from it
            Disp->>Lane: spawn the worker subprocess on the lane worktree
        end
        Lane-->>Disp: worker exit
        alt decided non-DONE exit (NEEDS-HUMAN, blocked, budget, stall, red cap)
            Disp->>Hand: close_partial — commit as-is, spec to terminal partial/ with a per-close report
            Note over Disp,Hand: the lane still closes into trunk and the run<br/>continues; only a FAILED handback stops it (LLR-144)
        else crash (traceback, signal)
            Note over Disp: claim stays in active/&lt;branch&gt;/; the next tick<br/>resumes it, bounded by the stall guard
        end
        Disp->>Lane: spawn the refresh — mechanical, no agent
        Lane->>Lane: merge trunk in, then trunk_step, then the check.py bar
        Lane->>Lane: commit a Bar-Green trailer naming the landing bar (or no-bar), the tree it barred and its work parent
        alt refresh red
            Note over Disp,Hand: a branch asserting DONE stops the run; one that merges<br/>nothing is quarantined once (code reverted, diff kept<br/>as a bar-inert patch) and refreshed again
        else refresh green
            Disp->>Slot: merge this lane's branch only — the slot is sub-second
            Slot->>Slot: is trunk already an ancestor, and does the tip attest its OWN tree for the landing bar?
            Slot->>Slot: merge --no-ff, ff trunk, unload, audit
            Slot->>Intake: post-merge arm, still inside the held slot (LLR-154)
            Intake-->>Slot: rows the merge forces, as ONE bookkeeping commit on trunk (LLR-153)
        end
    end
    Disp->>Intake: empty frontier — gap census mints gap-closure rows, else drain and exit 0
```

The same document's other flows with W3 participants, by title and participants only:

- Flow 1 — Unattended coordinator session (SR-026, SR-027, SR-028, LLR-029): agent-resume launcher; agent_loop.py (coordinator); dispatch lock — out/agent-loop.lock (LLR-029); dispatch.run — the station (Flow 4); agent_loop --wi (lane subprocess); agent CLI.
- Flow 5 — The blackout window on both routes (SR-227, SR-229, SR-230, LLR-270, LLR-300, LLR-301): blackout window function (agent_policy); integrate.claim (LLR-300); session service launch boundary; agent_loop / dispatcher; coordinator guard hooks (LLR-300/LLR-301); retained adjudicator keep (LLR-270).
- Flow 6 — The coordinator's judging turn and act turn (SR-231, SR-232, SR-209, SR-178, LLR-306, LLR-338, LLR-359): coordinator adjudication entry; claimed clean lane; committed verdict and binding; retained adjudicator plan; adjudicator session; approved-row records.
- Flow 7 — A coordinator codex call (SR-243, SR-222, LLR-346, LLR-269): coordinator codex entry point (LLR-346); the call's root (a lane or another checkout); session service (LLR-269); codex model session; primary checkout's session spool.
- Flow 8 — A usage ingest at close-out (SR-244, SR-222, LLR-347, LLR-350, LLR-351, LLR-269): coordinator close-out; usage ingest (LLR-350, LLR-351); transcript reader (LLR-347); ambient Claude home; recorded logs (spool and every worktree's records); session service (LLR-269).

## 7. W3's LLRs, by title

Each LLR tagged CMP-008: its id, its SRs, and its `title` cell, cut at 80 characters. Section 3 maps them to files.

- LLR-026 (SR-026, SR-238): Headless session launch
- LLR-027 (SR-027): Preflight footing guard
- LLR-028 (SR-028): Typed outcome + ERROR handling
- LLR-029 (SR-027): Kernel advisory lock
- LLR-030 (SR-027): Lock mutual exclusion
- LLR-037 (SR-040): Per-phase cmd map and the reviewer dial
- LLR-044 (SR-154): Agent pair-row routing
- LLR-045 (SR-154): Managed review dispatch
- LLR-046 (SR-154): Review substance scorer
- LLR-048 (SR-154): Independent critique dispatch
- LLR-058 (SR-148): WI-DAG frontier + deterministic traincar ordering
- LLR-059 (SR-148): Pure safety classifier
- LLR-060 (SR-148, SR-170): next-wi/run-phase retirement + generated status/run-state
- LLR-061 (SR-026): Explicit WI/train/worktree worker assignment
- LLR-070 (SR-155): Typed dual-plan round lifecycle
- LLR-071 (SR-155): Allowlist-only dual-plan briefs
- LLR-072 (SR-155): Dual-plan planner pair and fallback
- LLR-073 (SR-155): Coverage-step result adapter
- LLR-074 (SR-155): Dual-plan artifact persistence and filer
- LLR-076 (SR-155): Fresh-session dual-plan runner
- LLR-081 (SR-154): Fixed review escalation
- LLR-082 (SR-154): Bounded critique rework
- LLR-089 (SR-148): Structural safety cross-check
- LLR-095 (SR-155): Dual-plan path isolation
- LLR-096 (SR-155): Serialized dual-plan disposition
- LLR-123 (SR-148): Deterministic traincar ordering
- LLR-124 (SR-170): Generated status + run-state
- LLR-131 (SR-148): Contradiction-safe dual-plan class
- LLR-132 (SR-155): PAGE approval-level mapping
- LLR-137 (SR-170): Serial trunk step (log compile + regen)
- LLR-138 (SR-156): Tracked pause reader (dual-home)
- LLR-140 (SR-156): Local integrator (claim + queue + audit)
- LLR-142 (SR-173): Trunk-step artifact regen (dependency order)
- LLR-143 (SR-026): Plain-launch drive loop (claim->build->integrate)
- LLR-144 (SR-144): Terminal lane outcomes (handback + quarantine)
- LLR-145 (SR-156): Link-aware spec-move ritual (move + relink indivisible)
- LLR-149 (SR-148): §A8 admission: the kind x approval-level table + the spine barrier
- LLR-150 (SR-156): Lane mechanics: worktree, worker subprocess, §A2 refresh subprocess
- LLR-151 (SR-156): Dispatch-lock claim rung + the spine batch claim
- LLR-152 (SR-148): The adjudication kind: rank-1 slot + no-bar arm + the bar strictness key
- LLR-153 (SR-174, SR-228): The unified trunk-side intake mint + the context block + the approval-level arms
- LLR-154 (SR-174): The merge slot's post-merge intake arm
- LLR-155 (SR-137, SR-139): The config layer: one reader, checked shape, one comparison
- LLR-159 (SR-148): Admission order and the red-TC census
- LLR-161 (SR-144): The close ritual and the disposition it owes
- LLR-162 (SR-146): Prompts as loaded files, catalogued and fingerprinted
- LLR-163 (SR-146): Argv arrays, and the adjudicator as a routed phase
- LLR-167 (SR-146, SR-144, SR-148): The adjudicator briefs' evidence, and the refusal that keeps a half-filled one u…
- LLR-168 (SR-155): Hats roster reader + planner-brief injection
- LLR-174 (SR-171): Rate-limit recognition + bounded, surfaced wait
- LLR-175 (SR-172): Consecutive no-progress stall guard
- LLR-176 (SR-175): The push-channel inclusion conventions, pinned as they exist
- LLR-177 (SR-176): Transcript redaction: matched values never land in tracked history
- LLR-182 (SR-144): The lane-close terminal-outcome vocabulary, one home below its readers
- LLR-188 (SR-148): The registry-gap census as a read model, sited below every module that reads it
- LLR-189 (SR-144): The per-close report's shape, one home below the module that writes it and the o…
- LLR-196 (SR-177): Per-session fan-out utilisation telemetry, unaggregated
- LLR-207 (SR-156): The verdict record: what carries a governing verdict, and what binds it to the t…
- LLR-210 (SR-220): The consolidation census: which queued rows are one work item, and the memory th…
- LLR-246 (SR-208, SR-228): Refusing held-rung claims from a lane or marked autonomous commit
- LLR-247 (SR-209): The loop provenance trailer and the loop marker
- LLR-248 (SR-209): Every loop writer carries the trailer, and the floor checks it
- LLR-254 (SR-215): The checkpoint re-judge decision
- LLR-255 (SR-215): The merge, release and stage-gate checkpoints file the re-judge items
- LLR-262 (SR-154, SR-156): The record a merge judges stays as its author committed it
- LLR-264 (SR-220): The consolidation census as a command, its reason included
- LLR-265 (SR-215): The merge-slot intake re-run for a merge made outside the slot
- LLR-266 (SR-222): One adapter per provider runner captures its structured output
- LLR-267 (SR-222): Context occupancy is read from the latest request's prompt
- LLR-268 (SR-222): Each adapter maps its runner's usage to the pinned OpenTelemetry names
- LLR-269 (SR-222, SR-227, SR-239, SR-243): One session service launches and records every model call
- LLR-270 (SR-227, SR-238, SR-239): The keep operation retains adjudicator and loop reviewer sessions through act an…
- LLR-280 (SR-223): The guardrails payload is chosen by the policy's substring matcher, longest firs…
- LLR-282 (SR-225): The decision_recording dial reads off when undeclared and record when unrecogniz…
- LLR-283 (SR-225): The decisions record's owner verdict, format findings and session note
- LLR-284 (SR-225): The merge slot refuses a close that owes its decisions record and carries none
- LLR-288 (SR-148): Registry-owned owner gates in shared readiness
- LLR-290 (SR-227): Record reported and inferred codex compaction within a retained session
- LLR-293 (SR-215): The observation cadence policy
- LLR-294 (SR-215): The observation rubric-reference advisory
- LLR-295 (SR-146, SR-215): Assumption-only observation cases in adjudicator briefs
- LLR-297 (SR-161): The per-decomposition perspective record: derived applicability and production,…
- LLR-298 (SR-148): Ruling-to-citer synchronization
- LLR-299 (SR-148): Pending open-item citation integrity
- LLR-300 (SR-229, SR-237): Coordinator context occupancy, lease, and drain latch
- LLR-301 (SR-230): Coordinator relaunch request and exit acquisition
- LLR-303 (SR-225): Commit-local overrule-to-work synchronization
- LLR-304 (SR-225): Delegated-decisions retired-verdict migration
- LLR-305 (SR-227, SR-239): Coordinator adjudication shares the keep request and refuses an unsigned account
- LLR-306 (SR-227, SR-231, SR-209): Coordinator adjudication entry attributes a current verdict to its claimed lane…
- LLR-307 (SR-156): A Done-when blessing binds the exact changed checklist
- LLR-308 (SR-156): Done-when adjudication brief binds its claim and context
- LLR-309 (SR-156): Changed Done-when text is held at every build, close and merge transition
- LLR-310 (SR-232): Combined sitting composes and validates kind-scoped adjudications
- LLR-311 (SR-233): Review threat-model definition and reviewer reference
- LLR-312 (SR-220): Consolidation close preserves every effect owed to a work-item specification
- LLR-313 (SR-146, SR-154, SR-235): Attended review, critique and single-plan briefs and records
- LLR-314 (SR-234): Dispute findings and verdict grammar is parsed once
- LLR-315 (SR-234): Dispute brief assembly carries bounded findings to the adjudicator
- LLR-316 (SR-237): Blackout policy computes the active and most recently ended interval
- LLR-317 (SR-237): The shared session-service boundary admits only active-lane wrap-up adjudication…
- LLR-318 (SR-237): The unattended loop waits and retries at the blackout boundary
- LLR-319 (SR-237): The dispatcher retains an earlier claim while blackout blocks new work
- LLR-335 (SR-148): Disposition adoption is validated once and recorded at close
- LLR-336 (SR-154, SR-227): Accounts bind a routed entry to its declared credential home
- LLR-337 (SR-154): Single-plan pass gate
- LLR-338 (SR-231, SR-232): Act assembly from a committed accepted verdict
- LLR-339 (SR-156): The trunk is one declared name
- LLR-340 (SR-240): Commit-floor activation check and route refusal
- LLR-341 (SR-241): Verified review-record search before review rendering
- LLR-343 (SR-242): Red review-bar round cap and partial-close outcome
- LLR-344 (SR-154): Verified-attestation gate for unattended review draws
- LLR-345 (SR-148): Adoption records are admitted only by the close or unchanged carriage
- LLR-346 (SR-243): Coordinator calls launch, judge changes, and retain attributable results
- LLR-347 (SR-244): Transcript usage is finalized once per message
- LLR-348 (SR-244): Transcript identity determines each invocation identity
- LLR-349 (SR-244): Each recorded range is an ordered contribution
- LLR-350 (SR-244): Existing contributions determine the next transcript range
- LLR-351 (SR-244): A service-recorded session is excluded from transcript duplication
- LLR-352 (SR-244): The transcript reader refuses shapes outside its closed contract
- LLR-353 (SR-244): Ingest reads the ambient transcript home for one selected session
- LLR-354 (SR-244): Ingested logs carry contribution usage without transcript text
- LLR-355 (SR-244): Usage ingest reports one defined command outcome per invocation
- LLR-356 (SR-244): Close-out and headless completion ingest current and prior session tails
- LLR-358 (SR-246): Parent-first commit judgement refuses a moved inconsistent approval relationship
- LLR-359 (SR-178, SR-208): A held re-attestation carries the text identity its verdict judged
