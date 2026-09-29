+++
id = "WI-740"
title = "Keep warm only a route whose runner bounds a call to one turn: an ANTHROPIC-family route served through opencode, codex or any other runner is pinged today with no turn bound, which breaks SR-227's approved keep-warm clause"
workstream = "process"
sr_refs = ["SR-227"]
specref = ""
buildtier = "medium"
priority = 3
safety_class = "spine"
+++

## Deliverable

Keep-warm now pings only a route whose runner's adapter bounds a call to one
turn, which restores SR-227's approved keep-warm clause for every
configuration. No shipped configuration changes behaviour.

- **The code:**
  - `KeepWarmer` restricts its lease-eligible routes through
    `session_adapters.adapter_for` over each row's command template, once, at
    construction;
  - `PlainAdapter.bounds_one_turn` reports whether an adapter bounds
    `one_turn`, so a runner that gains the bound needs no second edit, and
    `session_keep` carries no runner-name list;
  - a non-bounding route takes no lease and starts no ping, and its
    retention is untouched.
- **The rows:**
  - LLR-270's `detail` takes the drafted replacement, and its `code_symbol`
    the new symbol. It stays Approved.
  - TC-268's `method` takes the drafted insertion. It stays Drafted.
  - The opencode and claude twin test pins the rule.
- **Evidence:** red, then green. The affected modules ran `111 passed`.
- **Review:** Sonnet found it SOUND
  ([sonnet-wi740.md](../../../reviews/2026-09-28-wave6/sonnet-wi740.md)).
  - Its one major (the capability inferred from the override, not declared)
    is accepted as built, because the draft required no second edit.
  - The trade-off is for the adjudication this merge mints to weigh.

## Context

Drafted by WI-737 (its ## Dispositions section) and minted at its merge - drafts-not-mints, ruling R1/R3.

THE DEFECT, confirmed at 349eef9. SR-227 (Approved) requires the loop to
"make any keep-warm call one bounded turn that never blocks the scheduler".
The keep-warm picks its sessions by family: `keepwarm_due` reads
`record["family"] == "ANTHROPIC"`, and `due_routes` globs `ANTHROPIC-*.json`.
It does not look at the runner. But only `ClaudeAdapter.one_turn` bounds the
argv (`--max-turns 1`). The codex, opencode and plain adapters return it
unchanged. A roster row's `family` is "who trained it" (`agents.template.toml`),
so an adopter's row `family = "ANTHROPIC"` with `cmd_template = "opencode run
-m anthropic/..."` is admissible. Its retained session would be pinged as an
open agentic session, bounded only by `KEEPWARM_TIMEOUT`'s 300 s wall. No
shipped route does this (the template and `docs/agents.toml` route ANTHROPIC
through claude only), so the fix changes no behaviour of a shipped
configuration.

IN SCOPE, exactly the following:

1. **Code.** The dispatcher's keep-warm pings a retained session only on a
   route whose runner's adapter bounds a call to one turn. Today that is the
   claude runner alone. The decision reads the route's adapter
   (`session_adapters.adapter_for` over the row's command template), so a
   runner gaining a one-turn bound later needs no second edit. Do not add a
   runner-name list to `session_keep.py`. A route that fails the test is
   never pinged. Leave its retention, resume, drain and retirement exactly as
   they are.
2. **LLR-270 (Approved)**, `detail`: replace
   `keepwarm_due is true for an ANTHROPIC active session idle keepwarm_minutes while lanes are out;`
   with
   `keepwarm_due is true for an ANTHROPIC active session idle keepwarm_minutes while lanes are out, and a ping is taken only on a route whose runner's adapter bounds a call to one turn (claude's), so a route served through any other runner is never pinged;`.
   If the code adds a symbol, append it to `code_symbol` in the group of the
   module that holds it. Nothing else in LLR-270 changes.
3. **TC-268**, `method`: immediately after
   `for an active ANTHROPIC session idle past the minutes while work is pending,`
   insert
   ` and only on a route whose runner bounds a call to one turn (an ANTHROPIC route served through opencode is never pinged),`.
   Add the one matching test to `tests/test_session_keep.py`. It uses a
   retained ANTHROPIC session, idle past the minutes, whose registry row
   launches `opencode`. Assert that the warmer takes no lease and starts no
   ping. Beside it, the same session on a `claude` row is pinged with
   `--max-turns 1` in its argv. Nothing else in TC-268 changes. If TC-268's
   Method no longer carries that anchor, stop and report it: do not re-place
   the clause.

OUT OF SCOPE, and a lane touching any of it is refused at review:

- SR-227, SR-222 and TC-264, which this sitting approved. Their text is right
  as it stands.
- Every other cell of LLR-270 and TC-268, and every other row, DA-016 and
  DA-017 included.
- A one-turn bound for opencode or codex. If one is wanted, it is its own
  intake.
- The sitting's other readings of the WI-738 observations: the conversation
  id for another runner, the tombstone's lock-free whole write, the 0.5 s
  lock wait on the tick, and basename-prefix matching. They were ruled
  wording, not defects.

Advisory registry joins (WI-388; never gating):

### Decomposition code map (LLR/TC on the same SRs)
- LLR-270 [project-trajectory/scripts/session_keep.py;project-trajectory/scripts/session_service.py;project-trajectory/scripts/session_adapters.py;project-trajectory/scripts/agent_loop.py;project-trajectory/scripts/dispatch.py :: KeepConfig/keep_config/applies/FAMILY_RESET_CAP/GOVERNING_INPUT_FILES/GOVERNING_INPUT_GLOBS/HOME_VARIABLES/store_lock/store_load/write_tombstone/load_honoured/retire_stale_lease/dedicated_home_env/governing_hash/drain_reason/lineage/chain_pending/is_clear_point/keep_for/keep_argv/keep_bookkeep/keep_abandon/keepwarm_due/take_warm_lease;cli_version/plan_keep/KeepWarmer/keep_warmer;ClaudeAdapter.mint/ClaudeAdapter.resume/ClaudeAdapter.one_turn/CodexAdapter.resume/OpencodeAdapter.resume/reported_error;adjudication_keep;run] tests: (see TC-266, TC-267, TC-268) — The keep operation retains adjudicator sessions through act…
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
