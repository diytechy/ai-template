# ADJUDICATE (first approval, re-judgement): WI-822, TC-316 and TC-318 at 02c5a93

The same independent in-lane spine adjudicator (Claude Opus) that wrote `003-ADJUDICATE-4e8f207.md`
re-judges the two rows `003` returned. It authored neither row, nor the tests. The question is
`003`'s: is each row ready to be APPROVED as it stands? The rows are judged as committed at
02c5a936, on trunk eae1f486.

## Basis (probed, not trusted)

- **The range since `003` (c5228db2..02c5a936).** It changes three files: two test modules and
  `docs/test/test-cases.toml`. No product code moved. `coordinator_guard.py`, `integrate.py` and
  `session_keep.py` are identical to what `003` judged.
- **The cells.**
  - TC-316's and TC-318's `method` and `evidence` each equal a block of `003`'s Fix 1 and Fix 2
    exactly (checked by program).
  - `verifies`, `expected`, `tier` and `level` are as `003` left them, and both rows are still
    `Drafted`.
  - The registry diff over the range touches only those four cells. One evidence cell's TOML
    quoting changed from `'...'` to `"..."`, and its value equals Fix 1.
- **The tests (309dcb93).** All four owed changes exist under the cited names and assert what
  `003` asked:
  - `test_a_claim_names_its_caller_by_claude_code_session_id` uses the literal keys
    `CLAUDE_CODE_SESSION_ID` and `CLAUDE_SESSION_ID`.
  - `test_the_latch_holds_after_a_compaction_drops_the_reading` fires a holder `PostToolUse`
    after the 5% post-compaction reply. It then asserts that `draining` is still True and the
    claim still refuses.
  - `test_the_successor_takes_the_lease_through_pt_coordinator_take` uses the literal key
    `PT_COORDINATOR_TAKE`.
  - `test_the_guard_cli_takes_requests_releases_and_clears` now asserts the refusal's stderr
    starts with `coordinator guard: ` and names the holder. It also asserts that `release` with
    no `--reason` exits 2.
- **Probes.** The export `review-tmp/adj822-r2-mut/` was refreshed with 02c5a936's two test
  modules and test-case registry; its three product modules are byte-identical to the lane's.
  Each mutation ran against the cited evidence of each TC it concerns, run alone. The baseline:
  TC-316 and TC-318's evidence gave 51 passed, and the three guard and session modules gave 143
  passed.

| # | Mutation | TC-316 evidence | TC-318 evidence |
|---|---|---|---|
| P19 | the guard reads `CLAUDE_SESSION_ID` | **caught** (`test_a_claim_names_its_caller_by_claude_code_session_id`) | - |
| P20 | the guard reads `PT_COORDINATOR_TOKEN` | survives, correctly: IF-278 is TC-318's | **caught** (`test_the_successor_takes_the_lease_through_pt_coordinator_take`) |
| P22 | a CLI refusal prints no reason | - | **caught** (the CLI e2e test) |
| P25 | a lower reading unlatches (hook path) | **caught** (`test_the_latch_holds_after_a_compaction_drops_the_reading`) | - |
| P30 | a usage error exits 0 | - | **caught** (the CLI e2e test) |
| P31 | the hook CLI exits 1 on bad stdin | - | **caught**, now by TC-318's own citation |

  Every probe `003` recorded as caught for these two rows is still caught by the row's own
  evidence: P1, P2, P3, P5, P29 and P32 for TC-316, and P7, P10, P11, P12, P16, P17, P18, P21
  and P24 for TC-318. P27b was caught in the same sweep by
  `test_a_heading_inside_the_prompt_fence_is_prompt_text`, which TC-318 cites unchanged. P27,
  the first form, did not change behaviour (its branch could not be reached) and counts for
  nothing.

## Rulings

- [APPROVE] TC-316 -> the obligation: verify single ownership of admission and the latch's lifetime: a claim names its caller by the session variable the agent CLI exports; the no-lease, other-session and unnamed-caller refusals name their recovery; release and clear require and record a reason; ownership passes only by release or a successor take; the latch survives a lower reading measured by a hook or by a claim, compaction and resume; reminders are bounded; and compaction telemetry is recorded and classified -> the chain: every clause of the new `Method` has a cited test that holds it. The two gaps `003` returned it for are closed: the literal session key (P19) and retention on the hook path (P25). `Verifies` (SR-229, LLR-300, IF-274, IF-275, IF-277) is now true, IF-277's session-identity half included. Smoke is honest, since every citation sits in an in-process smoke module -> ready.
- [APPROVE] TC-318 -> the obligation: verify the owned relaunch request, its single atomic acquisition at a true exit, restoration after any failure (including under lock contention), both launchers, the successor-token variable they export being the one the guard takes the lease by, and the command line's operations and exit codes -> the chain: every clause of the new `Method` has a cited test that holds it. The guard's side of IF-278 is now pinned to the literal name (P20); the launchers' side was already pinned by the two cited launcher tests. All four of IF-281's clauses are held by this row's own evidence: success, a refusal with its reason on stderr (P21, P22), a usage error exiting 2 (P30), and the hook's exit 0 (P31). Full is honest, since the row cites slow e2e tests -> ready.

## Owed to the builder

Nothing.

## Aftermath

With `003`'s six approvals and these two, route (a) of `003`'s Aftermath is the act. It is taken
uncommitted in the lane, and the coordinator commits it as the lane's last commit, after this
verdict. Each verdict commit ends with the trailer `WI: WI-822`.

1. Flip `status` from `Drafted` to `Approved` on SR-229 and SR-230
   (`docs/requirements/system-requirements.toml`), LLR-300 and LLR-301
   (`docs/requirements/low-level-requirements.toml`), and TC-315, TC-316, TC-317 and TC-318
   (`docs/test/test-cases.toml`), and nothing else. LLR-140 and LLR-270 stay `Approved`;
   `004-ADJUDICATE-4e8f207.md` re-attests them.
2. From the lane root, with `GIT_CEILING_DIRECTORIES=C:/Projects/ai-template.wt`:

       python project-trajectory/scripts/intake.py snapshot --approves "docs/requirements/low-level-requirements.toml=WI-822;docs/requirements/system-requirements.toml=WI-822;docs/test/test-cases.toml=WI-822" --reattests LLR-140,LLR-270

OUTCOME: APPROVE rows=2
