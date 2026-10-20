# WI-897 implementation plan: the guard hook's per-call cost

Planner: a fresh Claude Opus session, 2026-10-19. Plan mode `single`. Input:
the spec `docs/work/active/wi-897/WI-897-guard-hook-per-call-cost.md` and
the code and rows it names, read in the lane `wi-897` at `9f934456f`.

DELTA: within

**The architectural-delta answer.** The row makes one output depend on a new
input. Whether the guard runs before a tool call, and so where the latch is
measured and its instruction injected, now depends on the tool's name, through
the PreToolUse matcher. That is the spec's own answer (Scope answers S5), and
these rows carry it: P5 (the matcher in the examples and the consented
install), P6 (the moved measurement pinned) and P8 (the IF-274, IF-275,
IF-281 and LLR-300 reading against the event and tool contract, with the
decisions record). The row adds no state and no domain value. It crosses no
new boundary:
- `coordinator_guard` calling `agent_policy.blackout_at` directly crosses
  IF-291, which already lists `scripts/coordinator_guard` as a requestor;
- `session_keep` calling `agent_policy` crosses IF-291 too, which already
  lists `scripts/session_keep`;
- `session_keep` calling `kitlib.git` uses the declared shared kernel
  (`docs/kernel-modules-allow`, `kitlib/git.py`);
- `session_keep` stops requesting IF-065 (`agent_common`), so P8 removes it
  from that row's requestors.

`process_config` is re-pointed from `agent_common`'s re-export
(`agent_common.process_config = agent_policy.process_config`, the same
function object) to the module that defines it. That call stays inside
CMP-008 and is as undeclared today as it was through the re-export. P8
records this as a decision; it does not widen IF-291, whose subject is the
blackout window. No refactor beyond this row is needed.

## A finding the plan rests on: `session_keep` imports `agent_common`

Deliverable (1) says the hook's do-nothing path needs only three things: the
config read, `agent_policy.blackout_at` and the `session_keep` lock. But
`session_keep.py` imports `agent_common` at module level (lines 147-151), so
moving the imports in `coordinator_guard.py` alone cannot meet Done-when (1).
I measured it in the lane with `-X importtime`, without writing bytecode:
- importing `coordinator_guard` costs about 160 ms, of which `agent_common`
  is about 70 ms;
- importing `agent_policy`, `session_keep` and the kitlib modules the hook
  needs costs about 145 ms, because `session_keep` pulls in `agent_common`;
- the same set without `agent_common` costs about 90 ms.

`session_keep` uses `agent_common` for four calls only:
- `process_config` and `blackout_at` (twice), both `agent_policy`'s own
  functions, which `agent_common` re-exports;
- `git`, in `primary_out_dir`.

So the fix at the root is to re-point `session_keep` to `agent_policy` and to
the kernel's `kitlib.git.git_out` (P3). Deferring `agent_common` inside
`session_keep` would not help: `primary_out_dir` is on the hook's path. In
this repository the dial is on (`context_guard_pct = 50`), and the spec's
measured no-op is "not the holder, no blackout", which takes the lease lock.
So D1's test pins two no-op paths:
- the shipped default: guard off, no window;
- guard on, with the caller not the holder.

## The plan

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P1 | Measure a no-op hook call before any code changes, and record it in the lane log | D4 | IF-274; IF-281 (the hook's stdin and its exit 0, run as the settings run it; read only) | |
| P2 | Defer `agent_common`, `agent_route` and `argparse` in `coordinator_guard.py`; read the dials and the window from `agent_policy` | D1; SR-229; TC-315; TC-316; TC-317 | IF-291 (coordinator_guard is already a requestor); IF-274; IF-280; IF-281 (the `hook` command line, unchanged) | P1 |
| P3 | Re-point `session_keep.py` from `agent_common` to `agent_policy` and `kitlib.git`, so the lease lock no longer drags `agent_common` in | D1; SR-229; TC-317; TC-370 | IF-272; IF-273; IF-291 (session_keep is already a requestor); IF-065 (session_keep stops requesting it) | P1 |
| P4 | Pin the hook's no-op paths as importing no `agent_common`, `agent_route` or `argparse` | D1; SR-229; TC-317 | IF-274; IF-281 | P2; P3 |
| P5 | The guard's PreToolUse matcher in the kit example and this repo's example, carried by the consented install, with its pins | D2; SR-229; TC-339; TC-345; TC-317 | IF-280 (`hooks --example E --offer`, the install that copies the group); IF-274 (which PreToolUse payloads arrive); IF-275 (the denial, unchanged) | P4 |
| P6 | Pin the moved measurement for a tool outside the four (`Read`) at PostToolUse and PostToolUseFailure | D3; SR-229; TC-316; TC-339 | IF-274; IF-275 | P5 |
| P7 | Measure the no-op hook call again after the change, and record it in the lane log | D4 | IF-274; IF-281 (read only) | P5; P6 |
| P8 | The lane's checkpoint: read LLR-300, IF-274, IF-275 and IF-281 against the contract, amend what turns untrue, add the evidence, record the decisions | D5; SR-229; TC-316; TC-317; TC-339; TC-345 | IF-274; IF-275; IF-281; IF-065 (requestors amended per P3) | P5; P6; P7 |
| P9 | The RESYNC_PACK entry for (2), anchored at the lane's trunk base | D6; SR-229 | IF-280 (the consented install it tells adopters to re-run) | P2; P3; P5 |

## The steps

### P1: the measurement before the change (D4)

Take this first, before any code edit, on a quiet box. Record the load as
you see it, for example no other pytest or agent session running.

- **Scratch roots.** Use two roots outside every checkout, under the lane's
  scratch directory, not in the repository:
  - **off:** `docs/process.toml` with `[coordinator] context_guard_pct = 0`
    and `[policies] blackout = ""`;
  - **not the holder:** `context_guard_pct = 50`, with an
    `out/coordinator/lease.json` naming another session as holder. Because
    the scratch root is not a git repository, `primary_out_dir` falls back
    to the root itself, so the runs write nothing in the repository.
- **The command.** Run `<interpreter> <lane>/project-trajectory/scripts/coordinator_guard.py --root <scratch> hook`
  20 times per root and per payload, where the interpreter is
  `C:/Projects/ai-template/.venv/Scripts/python.exe`. Feed each run a
  PostToolUse payload for tool `Read` on stdin. Time each process's wall
  clock from a small timing script kept in the scratch directory.
- **Record.** Write the median and the minimum for each case in the lane's
  log fragment (`docs/log.d/`), together with the
  `-X importtime` cumulative figure for `coordinator_guard`.
- **No test.** This is a measurement.

### P2: deferred imports in `coordinator_guard.py` (D1, the guard-off path)

- **The module-level imports.** In both branches of the module-level
  `try/except ImportError`, drop `import agent_common` and
  `import agent_route` and add `import agent_policy`. Keep the
  `session_keep` and kitlib imports at module level: the existing tests read
  `guard.session_keep` and `guard.guard_hooks` as module attributes
  (`tests/test_coordinator_guard.py` line 902, `tests/test_blackout_window.py`
  line 1074), and D1 requires those tests to pass unchanged. The `except`
  branch still puts the scripts directory on `sys.path` for an in-process
  import, which the imports deferred below rely on.
- **The config read and the window.**
  - `guard_config` calls `agent_policy.process_config`.
  - `hook`, `window_refusal` and `window_check` call
    `agent_policy.blackout_at`. `window_refusal`'s docstring names
    `agent_policy.blackout_at` in place of `agent_common.blackout_at`.
  - It is the same function either way, and the tests' clock still patches
    `sys.modules["agent_policy"]._utcnow`.
- **`model_clis`.** It imports `agent_common` (for `split_cmd`) and
  `agent_route` (for `load_registry`) inside its body. It is the only user
  of either. `launch_reason` reaches it only on a shell tool inside an open
  window.
- **`argparse`.** `_parser` imports `argparse` itself. `main` reads `hook`
  before building a parser, but only when argv is exactly `["hook"]` or
  `["--root", R, "hook"]`. Every other argv goes through the parser
  unchanged, so `--root=R hook`, a stray argument or `--help` keeps
  argparse's behaviour and its exit 2 (IF-280 and IF-281 unchanged). The
  root is resolved by one small helper (`--root`, else `CLAUDE_PROJECT_DIR`,
  else `.`) that both branches call, never by a second copy of that rule.
- **Constraints.**
  - `coordinator_guard.py` is at 985 SLOC against
    `tests/test_module_size_ratchet.py`'s `THRESHOLD = 1000`. The change nets
    about +5. If it would cross 1000, shrink the change rather than add a
    baseline entry.
  - Run `check_complexity` on `main`.
  - `docs/cli-reference.md` is derived from the AST, which still sees
    `ArgumentParser(`. Confirm it with `gen_arch_map.py --cli-doc ... --check`.
    Run `gen_arch_map --check` as well: imports inside functions are still
    walked (`ast.walk`), and `coordinator_guard -> agent_policy` is IF-291.
- **Tests.**
  - The existing coordinator-guard tests run unchanged:
    `tests/test_coordinator_guard.py` (TC-315 and TC-316 evidence),
    `tests/test_coordinator_guard_e2e.py` (TC-317),
    `tests/test_blackout_window.py`, `tests/test_hooks_on_routes.py` and
    `tests/test_overnight_legs_git.py`.
  - P4 adds the new pin. It fails before P2 and P3.

### P3: `session_keep.py` stops importing `agent_common` (D1, the not-the-holder path)

- **The import.** Replace the module-level `import agent_common` (both
  branches) with `import agent_policy`, keeping the `sys.path` fallback.
  Then re-point the four call sites:
  - `keep_config`'s `process_config` (line 221) moves to `agent_policy`;
  - the two `blackout_at` reads (lines 1170 and 1714) move to `agent_policy`;
  - `primary_out_dir` (line 266) asks
    `kitlib.git.git_out(root, ["rev-parse", "--path-format=absolute", "--git-common-dir"])`.
    A `None` answer reads as no common directory.
- **The module docstring.** Its "It imports `agent_common` (the policy-file
  reader and git)" sentence names `agent_policy` and `kitlib.git` instead.
  Line 1156's mention changes the same way.
- **Behaviour.** It is unchanged on every path but one. Where git cannot be
  run at all, the old `agent_common.git` raised `FileNotFoundError`;
  `git_out` returns `None`, so the store falls back to `root/out`. That is
  exactly IF-272's stated contract ("else `root` itself (git unavailable,
  or not a repository)"), so this aligns the code to its contract. Record it
  in the lane's decisions.
  - `git_out` passes no `stdin=DEVNULL`. `git rev-parse` reads no stdin, so
    this changes nothing.
- **IF-065.** P8 removes `scripts/session_keep` from IF-065's `requestors`.
  The row is Drafted, and the cell stays true for the other three
  requestors.
- **Tests.** No new test here; P4's not-the-holder case is this step's pin
  (it fails before P3). The existing suites run unchanged:
  - `tests/test_session_keep.py` (TC-266, TC-267, TC-268, TC-329, TC-351);
  - the session-keep cases of `tests/test_blackout_window.py` (TC-341);
  - `tests/test_coordinator_guard_e2e.py::test_a_lane_worktree_shares_the_primary_checkouts_lease`,
    the IF-272 and IF-273 evidence in TC-317;
  - TC-370's evidence (`tests/test_commit_hooks.py`,
    `tests/test_hooks_on_routes.py`), whose session launch runs through the
    blackout reading re-pointed here;
  - `tests/test_overnight_legs.py`, whose fixture patches
    `agent_common.git`. The launcher's lease read is patched separately, so
    no case should depend on `primary_out_dir` going through that fake.
    Confirm it.

### P4: the no-op import pin (D1)

- **New test.**
  `tests/test_coordinator_guard_e2e.py::test_the_no_op_hook_imports_no_route_or_cli_module`,
  parametrized over two cases:
  - `off`: guard off, no window;
  - `not-holder`: guard at 50, a lease naming another session, the payload
    from this session.

  In each case a subprocess (`sys.executable -c`) does the following:
  - puts the kit's scripts directory on `sys.path`;
  - imports `coordinator_guard`;
  - calls `coordinator_guard.main(["--root", <tmp root>, "hook"])` with a
    PostToolUse payload for `Read` on stdin;
  - prints one JSON line naming which of `agent_common`, `agent_route` and
    `argparse` are in `sys.modules`.

  The test asserts:
  - exit 0;
  - the hook printed nothing;
  - the list is empty.

  It lives in the e2e module, the guard-by-subprocess file, which sits in
  `SLOW_MODULES`. So it costs the 60-second smoke tier nothing and runs in the
  full suite.
- **Fails before:**
  - at `9f934456f`, both cases list all three modules, because they are
    imported at module level;
  - after P2 alone, `not-holder` still lists `agent_common`, through
    `session_keep`.
- **Also:** the existing coordinator-guard tests pass unchanged (P2's list).

### P5: the PreToolUse matcher (D2)

**The change.**
- In `project-trajectory/agent-hooks/claude.settings.json`, the guard's
  PreToolUse group gains `"matcher"` (written first, as the `subagent_gate`
  group writes it) holding the four names `Agent`, `SendMessage`, `Bash`
  and `PowerShell`, joined by bars. The spec's Context gives the literal
  string.
- The same edit goes into this repository's `.claude/settings.json.example`,
  this repo's instance of the same example. The CLAUDE.md dogfood rule
  applies, and the take in this repo reads it, so P7's measurement means
  something here.
- `project-trajectory/agent-hooks/README.md`'s phrase "on every event the
  guard reads" gains one clause: its PreToolUse group runs only for the
  launch and shell tools.
- No code changes. `guard_hooks.bind` copies the group whole, and the state
  reading reads commands, never matchers.

**New tests. Each fails before because the example has no matcher.**
1. `tests/test_coordinator_guard.py::test_the_pre_tool_use_matcher_names_exactly_the_launch_and_shell_tools`.
   It runs over both examples, the kit's `KIT_EXAMPLE` and `ROOT/.claude/settings.json.example`.
   It asserts that:
   - the guard's PreToolUse group (one group) carries a matcher;
   - its bar-separated alternatives, as a set, equal
     `set(guard.LAUNCH_TOOLS) | set(guard.SHELL_TOOLS)`;
   - each alternative is a plain name (`[A-Za-z]+`);
   - the PostToolUse and PostToolUseFailure guard groups, and every other
     guard group, carry no `matcher` key.

   Before the change it fails on the missing key. Afterwards it fails if a
   tool is added to either table without the matcher, or the reverse.
2. `tests/test_blackout_window.py::test_the_consented_install_writes_the_pre_tool_use_matcher`.
   It is parametrized over machine-local settings that hold no guard group:
   no file, and a file holding only `permissions`. It runs
   `guard.guard_hooks.consent_install(root, _kit_example(tmp_path), _yes)`
   and asserts:
   - the reading is `on`;
   - the written PreToolUse guard group's matcher equals the example's;
   - the written PostToolUse and PostToolUseFailure groups carry none.

   Before the change it fails because no matcher is written.
3. `tests/test_blackout_window.py::test_every_denied_launch_reaches_the_pre_tool_use_matcher`.
   It is one test looping over the module's `DENIED` list, which covers
   WI-834's four tools. It asserts that each payload's `tool_name`
   full-matches the example's PreToolUse matcher. A full match implies a
   match under an unanchored reading too, so the claim holds whichever way
   Claude Code reads it. Before the change it fails because there is no
   matcher.

**Run unchanged:**
- `test_the_hooks_deny_each_launch_form_with_the_guard_off`: the denial for
  each tool (TC-317, TC-339);
- `test_the_hooks_allow_everything_else`;
- the WI-822 claim-boundary fixture (TC-317):
  `test_the_crossing_replys_claim_refuses_with_no_hook_run` and
  `test_the_crossing_replys_claim_refuses_via_the_pre_tool_use_reading`.
  The latter's `Bash` is inside the matcher;
- TC-345's install and state tests, including
  `test_an_absent_install_binds_every_group_and_keeps_other_keys` and
  `test_the_guard_hooks_are_this_repos_opt_in_not_its_tracked_settings`;
- `tests/test_dogfood_sync.py` and `tests/test_run_devsetup.py`. The latter
  is in `SLOW_MODULES`, so run it explicitly at this step.

### P6: the moved measurement, pinned for `Read` (D3)

New tests:
1. `tests/test_coordinator_guard.py::test_a_tool_outside_the_matcher_latches_at_its_post_tool_event`,
   parametrized over `PostToolUse` and `PostToolUseFailure`.
   - **Premise:** `Read` does not match the example's PreToolUse matcher,
     even unanchored (`re.search` is None), and that event's guard group
     has no matcher.
   - **Then:** take a held lease, have the transcript cross the threshold,
     and call `guard.hook(ev(event, transcript=tx.path, tool_name="Read", tool_input={"file_path": "x"}), root, env={})`.
     It returns `hookEventName == event`, with the instruction text starting
     "COORDINATOR CONTEXT GUARD: this session's context reached"; the lease
     reads `draining`; and exactly one `latch` event is recorded.
   - **Fails before** at the premise, because there is no matcher. The hook
     half passes before: the hook's code does not change, and the test pins
     that the measurement the matcher moves still happens after the call.
2. `tests/test_blackout_window.py::test_a_tool_outside_the_matcher_hears_the_close_down_after_the_call`,
   parametrized over the same two events, with the guard off inside the
   window.
   - **Then:** `REMINDER_EVERY + 1` hook calls for `Read` are told the
     close-down on the first and the last only, and no output carries
     `permissionDecision`.
   - **Passes before,** as a pin; nothing in the hook changes.
   - **Its bite is shown once by mutation:** take
     `PostToolUseFailure` out of `MONITORED`, or have `_close_down` deny
     every PreToolUse and PostToolUse, see the test fail, revert, and
     record the red in the lane log.

Each parametrized pair adds four smoke cases, about 0.1 s in process. That
keeps within the tier's membership budget, as the module's comments ask.

### P7: the measurement after the change (D4)

Re-run P1's script on a quiet box, with the same roots, payloads and counts,
and record both runs side by side in the lane log. Add one derived line: with
the matcher, a PreToolUse for a tool outside the four starts no guard process
at all. This is stated from the matcher, not measured, because Claude Code's
dispatcher is external. No test.

### P8: the lane's checkpoint (D5)

This is the coordinator's spine checkpoint. It reads each row against
Context's event and tool contract: four tool names at PreToolUse, PostToolUse
and PostToolUseFailure unmatched, `MONITORED` unchanged, the latch and its
instruction moved after the call, and the reminder cadence spanning more
calls. It amends every sentence the matcher makes untrue and records why the
rest stays true in `docs/decisions/wi-897.toml`.

Each row, and what I expect the reading to find:
- **LLR-300.** No sentence claims a measurement before every tool call:
  - "Only the holder's own hook payload ... is measured" stays true;
  - "hooks ... deny the closed list of the main session's Agent call,
    SendMessage call, Bash/PowerShell ..." stays true, because those are the
    four tools in the matcher;
  - the close-down "at that session's first monitored event in the window
    and every twentieth thereafter" counts events the hook receives, so it
    stays true while spanning more calls.

  The decision says so.
- **IF-274** (stdin: "on PreToolUse `tool_name` and `tool_input`"). This
  stays true of each payload that arrives. That fewer arrive is the
  contract's tool set, recorded as a decision.
- **IF-275** (deny for exactly the launch forms, refuse nothing else). This
  stays true: the four tools still reach PreToolUse.
- **IF-281** (`hook` always exits 0). This stays true.
- If the reading finds an untrue sentence anyway, it amends that sentence in
  the row, and in `coordinator_guard.py`'s matching `Contract IF-###`
  docstring with `--contracts-doc` regenerated.
- **Traced cells otherwise.** Each new test is added to a TC evidence cell:
  - TC-317 gains P4's test;
  - TC-345 gains P5's tests 1 and 2;
  - TC-339 gains P5's test 3 and P6's test 2;
  - TC-316 gains P6's test 1.

  A TC's method or expected text is amended only where the reading finds it
  untrue, and an amendment to an Approved row's meaning goes through the
  repo's re-attestation route. IF-065 drops `scripts/session_keep` from its
  requestors (P3).
- **Also read, with no change expected:**
  - `docs/runtime-flows.md` Flow 5, whose hook denies Agent, SendMessage and
    a model CLI; all three are in the matcher;
  - `docs/requirements/components.toml`, where CMP-008 is unchanged;
  - SR-229's text, which is about admission and is untouched.
- **The decisions.** Also record P3's git-unavailable alignment to IF-272,
  and the `process_config` re-point (see the delta answer).
- **Run:** `trace.py --strict-integrity` and `check_trajectory --strict`.

### P9: the RESYNC_PACK entry (D6)

- **Placement.** Add one `### <title> [since <sha>]` heading at the end of
  §4, before `## 5`. Anchor it at the lane's trunk base, the trunk commit
  the lane was cut from or last refreshed onto, with the pack's usual
  "Anchored at the preceding commit" line.
- **Sequencing.** `scripts/check_resync.py`, part of the commit bar, refuses
  any commit that changes a shipped file without an added entry anchored at
  that base. So the heading is written in P2 and P3's commit, and that
  commit's text already describes what overwriting the two scripts gives an
  adopter. The P5 commit then completes it for (2). Editing an existing
  entry adds no heading, so the base-to-tree count stays at one.
- **Its content:**
  - **What changed.** The guard's PreToolUse group in the example runs only
    for `Agent`, `SendMessage`, `Bash` and `PowerShell`. PostToolUse,
    PostToolUseFailure and the other events stay unmatched. For any other
    tool, the context measurement and the latch instruction come at its
    PostToolUse or PostToolUseFailure, and the drain and close-down
    reminders count only the events the hook receives. Nothing that refuses
    moves. The hook also imports less on a call with nothing to do.
  - **Kit-owned files, overwrite:** `scripts/coordinator_guard.py`,
    `scripts/session_keep.py`, `agent-hooks/README.md`, and
    `agent-hooks/claude.settings.json` (re-copy it as
    `.claude/settings.json.example`, the pack's phrasing for this file).
  - **What to do.** The guard state is read by command name, so a
    matcher-only change still reads `on`, and nothing reinstalls the groups.
    To take the new matcher, remove the installed guard groups from
    `.claude/settings.local.json` and run the consented install again: the
    next first run (dev-setup at a terminal, `hooks --offer`, or the lease
    take) reads `absent`, asks, and installs the new ones. `hooks --enable`
    no longer exists (WI-927). An older, unmatched group keeps working: it
    runs the guard on every tool, costs time and refuses nothing it should
    not. No registry, setting or record format changes.
- **Tests:** `tests/test_resync_pack.py` and `tests/test_check_resync.py`,
  plus `scripts/check_resync.py` itself in the bar. No new test; the grammar
  and anchor checks exist.

## Commit order

1. P1's before-figures (lane log), then P2, P3 and P4 with the first RESYNC
   draft (P9). This is behaviour-preserving, and P4 goes red to green across
   it.
2. P5 and P6, with the RESYNC entry completed for (2).
3. P7's after-figures, then P8's checkpoint: spine cells, the decisions
   record and the TC evidence.

Every commit passes `run.cmd smoke`. The slow modules this lane touches run
explicitly before the commit that touches them: `test_coordinator_guard_e2e`
and `test_run_devsetup`.

## The coverage, restated

- D1: P2, P3, P4.
- D2: P5.
- D3: P6.
- D4: P1, P7.
- D5: P8.
- D6: P9.

SR-229, the item's only SR, is cited by every row except P1 and P7. These are
the TCs that verify it:
- TC-315: P2, run unchanged;
- TC-316: P2, P6 and P8;
- TC-317: P2, P3, P4, P5 and P8;
- TC-339: P5, P6 and P8;
- TC-345: P5 and P8;
- TC-370: P3, run, because its session launch reads the re-pointed blackout
  window.

No clause is excluded.

## Outside this row (surfaced, not fixed)

- `project-trajectory/agent-hooks/README.md` still says the guard's groups
  "are merged into the machine-local `.claude/settings.local.json` beside any
  hooks already there". That has been stale since WI-927, which installs only
  from `absent` and never merges. P5 touches the paragraph's first sentence
  only, so this is a separate finding for the coordinator to file.
- `primary_out_dir` spawns git once per process, so every hook call pays one
  `git rev-parse` on the guard-on path. Caching the answer across processes
  is a lifecycle the spec rules out of scope.
