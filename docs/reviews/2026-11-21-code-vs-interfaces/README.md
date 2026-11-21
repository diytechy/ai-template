# Code against its interface and LLR rows (2026-11-21)

Evidence for WI-1015. Measured from the tree at a425ad9ba: every Python import between the 136 modules under project-trajectory/scripts (AST, nested imports included), set against the interface rows and the LLR Module and CodeSymbol cells. Membership and the kernel allowlist are the kit's own (kitlib.spine.module_components, docs/kernel-modules-allow).

## Imports no call row declares: 340 of 587

| What the cross-component rule (LLR-067) says | Imports |
|---|---|
| Into a kernel module: exempt by the allowlist | 189 |
| Both ends in one component: no row needed | 82 |
| Component sets overlap through a module tagged into several components: advisory only | 63 |
| Disjoint components | 6 |

The rule reports none of the 6, because any row naming both modules counts as cover, on any channel and whoever owns it:

- scripts/check_assumption_gate (CMP-007) imports scripts/record_observation (CMP-006); counted as covered by IF-215 (record_observation's cli)
- scripts/gen_trajectory (CMP-009) imports scripts/retire (CMP-006); counted as covered by IF-257 (retire's file)
- scripts/rejudge (CMP-008) imports scripts/record_observation (CMP-006); counted as covered by IF-200 / IF-214 / IF-215
- scripts/rejudge (CMP-008) imports scripts/kitlib/observation (CMP-006); counted as covered by IF-200 / IF-214 / IF-215
- scripts/review_brief (CMP-008) imports scripts/plan_coverage (CMP-006); counted as covered by IF-046 / IF-047 / IF-287 / IF-290 (rows owned by other modules)
- scripts/schedule (CMP-008) imports scripts/spine_carrier (CMP-006); counted as covered by IF-265 (spine_carrier call; schedule not a requestor)

Modules whose several component tags silence the rule, with the edges each silences:

adjudicate_brief (8), integrate (8), trace (7), intake (6), kitlib/verdict (6), acceptance_record (4), census (4), check_trajectory (4), coordinator_guard (4), amendment_brief (3), check (3), coordinator_adjudicate (3), pending (3), id_carrier (3), kitlib/authority (2), text_then_act (2), held_status (2), hats (2), assumption_rules (1), gen_open_items (1), gen_arch_map (1)

## Declared callers that do not import the owner: 15

Some reach the owner through a re-export (traj_status through traj_context, gen_trajectory likewise).

- IF-046: scripts/kitlib/verdict is a requestor of scripts/score_reviews
- IF-071: scripts/gen_trajectory is a requestor of scripts/schedule
- IF-175: scripts/adjudicate_act is a requestor of scripts/kitlib/verdict
- IF-102: scripts/traj_status is a requestor of scripts/spine_carrier
- IF-195: scripts/acceptance_record is a requestor of scripts/kitlib/authority
- IF-195: scripts/agent_common is a requestor of scripts/kitlib/authority
- IF-195: scripts/integrate is a requestor of scripts/kitlib/authority
- IF-256: scripts/agent_common is a requestor of scripts/kitlib/decisions
- IF-256: scripts/agent_loop is a requestor of scripts/kitlib/decisions
- IF-256: scripts/gen_open_items is a requestor of scripts/kitlib/decisions
- IF-287: scripts/consolidate is a requestor of scripts/kitlib/sitting
- IF-287: scripts/review_brief is a requestor of scripts/kitlib/sitting
- IF-291: scripts/agent_loop is a requestor of scripts/agent_policy
- IF-291: scripts/session_service is a requestor of scripts/agent_policy
- IF-291: scripts/dispatch is a requestor of scripts/agent_policy

## Signatures in data cells that do not match the owner: 9 of 101

- IF-044 (scripts/agent_route): resolve_enabled - argument `tokens` not in def resolve_enabled(enabled, registry, tag_rank)
- IF-129 (scripts/acceptance_record): accepted_text_digest - argument `registry` not in def accepted_text_digest(csv_path, id_col, row)
- IF-177 (scripts/check_trajectory): queue_conflict_pairs - argument `model` not in def queue_conflict_pairs(wis)
- IF-178 (scripts/spine_carrier): resolve - argument `root` not in def resolve(path, suffixes)
- IF-179 (scripts/agent_common): git - argument `argv` not in def git(root, *args)
- IF-186 (scripts/bookkeeping): scope - no such function in owner
- IF-186 (scripts/bookkeeping): write - no such function in owner
- IF-246 (scripts/session_service): route_runner - no such function in owner
- IF-282 (scripts/session_service): route_runner - no such function in owner

## LLR CodeSymbols

274 of 345 LLRs carry an Implements: tag in code. Named symbols that exist nowhere:

- _nav (LLR-055, LLR-115)
- build_module_map (LLR-080)
- critique_failure_action (LLR-082)
- VERIFICATION_VALUES (LLR-083)
- _descend (LLR-086)
- sw_view (LLR-099)
- claim_work (LLR-319)

Named symbols in another module than the row says:

- _implemented_ids (LLR-159: in census.py, not dispatch.py)
- _split_lines (LLR-161: in kitlib/station.py, not handback.py)
- evidence_verdict (LLR-192: in kitlib/stage.py, not kitlib/evidence.py)

About 25 CodeSymbol cells hold prose or CSS tokens rather than symbols (LLR-011, LLR-104, LLR-107, LLR-108, LLR-110, LLR-111, LLR-113, LLR-117, LLR-171, LLR-176, LLR-190, LLR-311, LLR-356 among them).

## Interface rows no test case verifies: 125 of 268

No row uses verified_by to point at a parent test instead.

