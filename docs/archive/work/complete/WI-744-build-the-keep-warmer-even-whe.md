+++
id = "WI-744"
title = "Build the keep-warmer even when one routing row's argv cannot be built: KeepWarmer builds every row's argv at construction, so a row the prompt-transport check refuses raises and stops the dispatcher before its first poll with the dial on"
specref = ""
workstream = "process"
sr_refs = ["SR-227"]
buildtier = "medium"
priority = 3
safety_class = "spine"
+++

## Deliverable

The keep-warmer is built even when a routing row's command line cannot be:
`KeepWarmer.__init__` leaves out a row whose argv `agent_session.build_argv`
refuses with `ValueError`, so `dispatch.run` no longer stops before its first poll
with the keep-warm dial on. Every other row is classified as before.

- **Code:** `project-trajectory/scripts/session_service.py`, `KeepWarmer.__init__`:
  the route set is built in a loop that skips a refused row.
- **Test:** `tests/test_session_keep.py::test_keep_warmer_excludes_a_route_whose_argv_is_refused`
  forces the refusal on every platform (monkeypatching the prompt-transport check)
  and asserts the warmer is built, the refused row is absent and the claude row
  present. Red before the fix, green after.
- **Rows:** none changed (LLR-270 already states the obligation).
- **Review:** Sonnet 5.5, SOUND at 9d19e88d
  (`docs/reviews/2026-10-02-wave7/sonnet-wi744.md`); its one minor (a malformed
  template is skipped too) accepted as built.

## Context

Drafted by WI-741 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

THE DEFECT, reproduced at 768b209.

- WI-740 made `KeepWarmer.__init__` call `agent_session.build_argv` for
  EVERY row of the routing registry, of every family, to classify its adapter.
- `build_argv` raises `ValueError` for a row it refuses. One case is a
  `{prompt}`-in-argv row behind a Windows `.cmd`/`.bat` shim. The kit's own
  template row `gemini -p {prompt}` is such a row wherever `gemini` is an npm
  `.cmd` shim.
- So with `[adjudicator]` `context_reset_pct` and `keepwarm_minutes` both on,
  `session_service.keep_warmer` raises. `dispatch.run` then stops before its
  first poll, where before only that route's own launch was refused.
- This breaks LLR-270's approved "built by keep_warmer when keepwarm_minutes
  is also on, ticked once per dispatcher poll by run".
- Nothing changes at the shipped dial 0, where `keep_warmer` returns before it
  builds anything.

IN SCOPE, exactly the following:

1. **Code.** In `KeepWarmer.__init__`, a row whose argv `build_argv` refuses
   with `ValueError` is left out of the eligible routes, so it is never
   pinged. The warmer is still built, and every other row is classified
   exactly as today. Change nothing else:
   - do not move or weaken the prompt-transport check;
   - do not change `bounds_one_turn`;
   - leave every route's retention, resume, drain and retirement untouched.
2. **One test, in `tests/test_session_keep.py`.**
   - Build a `KeepWarmer` over a registry holding a claude row and a row whose
     argv build is refused. Force the refusal on every platform, for example
     by monkeypatching the prompt-transport check, because CI runs POSIX.
   - Assert the warmer is built, the refused row is not in its routes, and
     the claude row still is.
3. **The rows: none change.** LLR-270's text already states the obligation,
   and TC-268's method already covers the warmer being built from the routing
   registry.

OUT OF SCOPE, and a lane touching any of it is refused at review:

- `bounds_one_turn`'s method-identity inference. WI-741 ruled it honest, and
  a declared attribute is its own intake if one is ever wanted.
- Any cell of any row, LLR-270 and TC-268 included.
- The prompt-transport rule itself.
- The session-adapter interface row's method list.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/store_lock/store_load/write_tombstone/load_honoured/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/take_warm_lease;cli_version/plan_keep/KeepWarmer/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/PlainAdapter.bounds_one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error;adjudication_keep;run] tests: (see TC-266, TC-267, TC-268) — The keep operation retains adjudicator sessions through act…
- TC-266 -> tests/test_session_keep.py
- TC-267 -> tests/test_session_keep.py
- TC-268 -> tests/test_session_keep.py

### Knowledge packs the touched components declare (read before building)
- CMP-008 W3 Autonomy: docs/knowledge/agent-routing;docs/knowledge/effort-tiering;docs/knowledge/prompt-image-token-efficiency

### Interface seams via the touched modules
- IF-037 docs/process.toml -> scripts/agent_common;scripts/agent_loop;scripts/bootstrap;scripts/check_privacy;scripts/check_trajectory;scripts/dispatch;scripts/gen_arch_map;scripts/gen_okf;scripts/integrate;scripts/kitlib/config;scripts/subagent_gate;hooks/pre-commit;hooks/commit-msg;hooks/pre-push;external:downstream adopter: file sections: attestation, policies, checks; one key = value per line
- IF-162 docs/agents-enabled -> scripts/agent_route;scripts/dispatch: file one registry id per line in preference order, optional <PHASE>=<weight> annotations; presence turns managed r…
- IF-053 scripts/schedule <- scripts/census;scripts/dispatch;scripts/intake: call load_wis · _load, frontier, kind_of · SAFETY_CLASSES — the symbols census, dispatch and intake take; no write…
- IF-173 scripts/integrate <- scripts/dispatch;scripts/handback;scripts/lane: call claim, refresh, integrate, finished_branches, branch_outcomes, lane_worktree, the ACTIVE and WORK constants, …
- IF-088 scripts/pending <- scripts/dispatch: call pending.owner_cards -> PendingItem(kind, line) with kind blocked or spine; the pause kind excluded
- IF-090 scripts/intake <- scripts/integrate;scripts/dispatch;scripts/agent_loop: call intake_after_merge (integrate) · mint_gap_rows (dispatch) · context_block (agent_loop, advisory)
