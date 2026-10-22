# WI-960 implementation plan, revision 2: Sol and Terra calls go through the session service

Spec: `docs/work/active/wi-960/WI-960-sol-terra-via-session-service.md`
(specref: review-churn README item 8, proposal step 1). Item SR: SR-222.
Planner: a fresh session, read-only. Lane worktree:
`C:/Projects/ai-template.wt/wi-960` (tip `56cf98765`).

## What changed from revision 1, and why

The critique's two findings were checked against the spec and the code. Both
hold.

- **F1, confirmed.** Settlement 1 classes the primary checkout as outside a
  lane, and so does D7 ("From the primary checkout ... spools"). It adopts
  "the predicate `lane_refusal` already states", which reads the claim off the
  branch's own tree (`coordinator_adjudicate.lane_refusal` ->
  `integrate.claimed_ids_on_branch`). Revision 1 replaced that with a
  trunk-only reading and made the primary checkout on a claimed branch a lane.
  It then treated both departures as build instructions. That was wrong.
  - **Departure (b) is dropped.** The primary checkout is never a lane, on any
    branch. The case was weak anyway: `integrate.lane_worktree`'s docstring
    says `refresh` and `attest` refuse a primary checkout sitting on the
    branch (`_lane_off_trunk`), so such a lane cannot land by the normal route.
  - **Departure (a) is narrowed and taken to the spec first.** The defect it
    answers is real. `agent_loop.run_iteration` records every worker session
    through `session_service.record` (line 3407), the REVIEW session included.
    The integrator's verdict gate (`integrate._verdict_gate` ->
    `kitlib.verdict.logged_rounds`) counts only rounds whose REVIEW session log
    a commit in `base..branch` added. The process orders "close before the
    final verdict round" (PROCESS_OPTIONS.md, the LLM-gate verdict protocol),
    so the spec leaves `active/<branch>/` on the branch before the final
    round. Under the branch-tree reading alone, that final round's log would
    spool, and every loop lane with `review-policy >= 1` would be refused at
    merge. The plan no longer swaps the reading. It keeps `lane_refusal`'s
    predicate whole and adds one case: a linked worktree on branch B whose
    claim under `active/B/` is gone from B's tree but still held on trunk's
    committed tree (closed, not yet merged) stays a lane. Row P0 brings that
    one addition to the spec as an amendment and has it judged before any test
    is written. If the amendment is refused, the lane stops at P0 and closes
    partial (see P0). The plan does not build around a refusal.
- **F2, confirmed.** In revision 1, P5 found candidates with `git grep "^#
  role: AUTHOR$"`. The header writes `role` near its end (after `session-id`,
  `invocation-id` and the rest; `agent_common.write_session_log`), so a log
  truncated or damaged before that line never becomes a candidate, and the
  reader would continue an older thread. Candidates are now found by **name**,
  not by content. The reader walks every standard-call log, newest first by
  the stamp in its name, and refuses on any log it cannot classify before it
  reaches the carrier. P2 adds the case the critique names: an older valid
  committed `AUTHOR` log, then a newer malformed or truncated one, committed or
  not. The result must be no launch, with the offending path named.

## What the code holds today (read, not assumed)

- `scripts/coordinator/sol_review.sh` and `terra_author.sh` run `codex exec`
  straight from bash: `-m <model> -c model_reasoning_effort=<e> -c
  'windows.sandbox="unelevated"' -s workspace-write --add-dir $TMPROOT -C <wt>
  --skip-git-repo-check -o <out> - < <prompt>`, with `<out>.log` as the
  transcript. Sol compares `rev-parse HEAD` and `status --porcelain` before
  and after the launch. Terra compares HEAD only. Either exits 3 on a
  difference. `luna_review.sh` has the same shape, and only recipes §7 (the
  D-017 Luna substitution) and the README's Luna section still mention it.
- Recipes §1 "Terra, resumed" is a hand-typed `codex exec resume <id> ...`
  using `-c sandbox_mode=...` and `-c sandbox_workspace_write.writable_roots=[...]`,
  because `resume` takes no `-s` or `-C`. Recipes §7 also probes with a
  hand-run `codex exec -m gpt-6.1-sol`.
- `session_service.record` writes the log through
  `agent_common.write_session_log`, then calls `commit_telemetry` and
  **discards its return value**. That value is the refusal text: a hook veto,
  an index lock, or the loop marker's `held` refusal. `record` returns the
  path and has no out-of-lane arm. Its callers are `session_service.call` and
  `agent_loop.run_iteration`. `_call_row` names a standard log
  `call_<uuid4 hex>-<YYYYmmdd-HHMMSS>.log`, which
  `kitlib.verdict.SESSION_LOG_RE` never matches.
- `act` marks `session-mode = resumed` only for `call.keep` with a session id.
  A resume comes only through the retained store (`keep_argv` ->
  `adapter.resume`). `CodexAdapter.resume` inserts `resume <id>` after `exec`
  and drops `-C`/`--ephemeral`. `CodexAdapter.prepare` adds `--json` and the
  `-o` temp file, and `final_text` reads it.
- `act` refuses before anything is built: first `HooksOffRefused`, then
  `launch_refusal` -> `BlackoutRefused` for every role except an ADJUDICATE
  of an actively claimed WI. D10 therefore needs no new refusal, only routing
  and an exit mapping.
- The roster rows `OPENAI-SOL` and `OPENAI-TERRA` are enabled on
  `docs/agents-enabled`. Their `cmd_template` carries
  `--dangerously-bypass-approvals-and-sandbox`, which is not the wrappers'
  sandbox, so the launch template cannot be the row's (decision 1).
- `coordinator_adjudicate.lane_refusal(root)` decides lane-ness from two
  readers:
  - `agent_common.worktree_records` plus `_worktree_index`: not the top of a
    worktree, index 0 (the primary checkout) or a detached HEAD is not a lane;
  - `integrate.claimed_ids_on_branch(root, B)`: `ls-tree` of `active/B/` on
    B's committed tree, where `None` (git cannot say) or empty is not a lane.

  `integrate` does not import `session_service`, directly or through its
  imports (grep: only `agent_loop`, `coordinator_adjudicate`, `dispatch` and
  `plan_runner` import it), so a deferred import from `session_service` makes
  no cycle.
- `write_session_log` prefixes the file name with `meta["train"]` when it is
  set, so a standard-call log cannot carry its lane in `train` and stay in the
  `call_` grammar. The header carries `phase` early and `session-id`,
  `invocation-id`, `role`, `roster-row` and `started-at` late, then the
  `# ---` terminator. `read_log_meta` stops at the first non-`#` line and
  records no sign of whether it reached the terminator.
- `conftest.hooked_checkout` makes every service-route test root a bare
  **primary** checkout. Under the spec's rule every such root spools, so each
  test that asserts `record`'s commit must move onto a claimed **linked
  worktree**.
- `scripts/coordinator/layout.py` derives `TMPROOT` from the script's own
  location. Run from a lane's copy, that gives `<lane>.wt/review-tmp`, which
  is wrong, and the live runs before landing (D12) do run the lane's copy.

## Decisions this plan takes (for the coordinator to confirm at the claim's records)

1. **C4, where the launch template lives: a template the entry point
   declares.** No row is added to `docs/agents-enabled`, so no owner act is
   needed before the build. The family, model, tier and route id come from
   the enabled roster row (`resolve_route` + `entry_route`), so SR-222's
   "provider filled from its roster row" holds. The executable is the row
   template's first token (`codex`). One template serves both the first turn
   and the resume:

       codex exec -c model_reasoning_effort=<effort> -c windows.sandbox=unelevated
         -c sandbox_mode=workspace-write
         -c sandbox_workspace_write.writable_roots=['<scratch root>']
         --skip-git-repo-check --model {model}

   - The prompt goes on stdin, and the adapter adds `--json` and `-o`.
   - The single-quoted TOML literal avoids the double quotes that the recipes
     warn a `.cmd` shim re-quotes.
   - `sandbox_mode` and `writable_roots` are the recipe's resume form, which is
     equivalent to `-s workspace-write --add-dir` and is accepted by `resume`.
   - The scratch root is the primary checkout's `<checkout>.wt/review-tmp`,
     derived from the call root (`session_keep.primary_out_dir(root).parent`),
     never from the script's location.
   - D12 confirms the sandbox flags live (P8).
2. **The entry point lives at `scripts/coordinator/codex_call.py`**, beside
   `overnight_legs.py` (CMP-008 through an LLR module cell). The roles, the
   sandbox template and the review-tmp layout are this repo's conventions.
   Only the service changes ship: the spool arm, the refusal report, the
   unretained resume and the call-log grammar. The script imports the kit's
   scripts from its own checkout (`parents[2]/project-trajectory/scripts`), so
   a lane's copy runs that lane's service.
3. **The lane predicate is the spec's, plus one judged addition.**
   `session_service.lane_branch(root)` returns B or None.
   - **Not a lane** (exactly `lane_refusal`'s cases): the worktree records are
     unreadable or `root` is not the top of one; index 0 (the primary
     checkout, on trunk **or on a claimed branch**); a detached HEAD.
   - **A lane:** a linked worktree on B whose committed tree still holds a WI
     spec under `active/B/` (`integrate.claimed_ids_on_branch`).
   - **The P0 addition:** a linked worktree on B whose own tree no longer
     holds the claim while trunk's committed tree
     (`refs/heads/<agent_common.trunk_name>`, `ls-tree active/B/`) still does.
     This is a lane closed under close-first and not yet merged.
   - **Every unreadable read decides "not a lane":** a failing `ls-tree`,
     `TrunkUndeclared`, or an absent trunk ref. With no trunk declared, the
     predicate is therefore exactly `lane_refusal`'s.

   The predicate reuses `lane_refusal`'s two readers. It does not copy their
   logic. `_worktree_index` moves to `agent_common` beside `worktree_records`
   (as `worktree_index`), and `coordinator_adjudicate` imports it from there.
   That is a pure move, and `lane_refusal`'s behaviour and SR-231 are
   unchanged. `lane_refusal` itself is left as the spec requires.
4. **Terra's carrier binds to the lane.** The log's `wi` must be one of the
   lane's WIs (the ids decision 3's claim reads return, branch side ∪ trunk
   side). Its `role` must be `AUTHOR`, and its `roster-row` must be the
   resolved Terra row id. The spec says "branch", but the call log has no
   branch column (`train` renames it out of the `call_` grammar). A WI is
   claimed by one lane at a time, so its claim names the lane without a
   log-schema change. P5 gives the selection walk.
5. **Exit codes of the entry point.**
   - 0: the call succeeded with no edit, and its log was committed in a lane
     or spooled.
   - 1: the call failed: non-zero exit, timeout, or a reported error.
   - 2: refused before launch: an argument, the route, the brief, a blackout,
     hooks off, or the resume carrier.
   - 3: an edit, with the paths printed.
   - 4: the log was not committed in a lane, or the spool could not be
     written. The log path and the refusal are named.
   - 5: the change check could not run.

   After launch the precedence is 5 > 3 > 4 > 1 > 0.
6. **`luna_review.sh` retires with no substitute.** The D-017 line in recipes
   §7 becomes `--route <the enabled Luna row>` through the entry point.

## The architectural-delta question

The WI does all four:
- **It adds a state:** a recorded call that is spooled, not committed.
- **It adds values to domains:**
  - the entry point's role set `REVIEW-A | CRITIQUE | AUTHOR`;
  - its exit codes 3, 4 and 5;
  - `session-mode = resumed` for an unretained call;
  - `record`'s "commit refused" outcome, surfaced to its caller.
- **It makes outputs depend on new inputs:**
  - where `record` writes depends on the root's lane-ness, which reads
    worktree records, the branch tree and the trunk tree;
  - the change check's verdict depends on the commit range's shape and on
    uncommitted content;
  - a resumed turn's thread depends on the committed call logs at HEAD.
- **It crosses a new boundary:** this repo's coordinator tooling calls the
  shipped service (IF-246, IF-282).

All of it fits modules this item may amend: `session_service.py`, the new
entry point, `agent_common` (`log_meta_text`, `worktree_index`) and the
one-line import in `coordinator_adjudicate.py`. It also fits rows amended in
place: IF-246, IF-282, LLR-269 and TC-265. The new rows are one derived SR, one
LLR and two TCs. No component changes. The one spec-level question, the
close-first case, is a spec amendment this lane owns (P0), not a refactor
outside it. The table carries the change:
- P0 settles the predicate's scope;
- P3 holds the service's new state and inputs on IF-246;
- P4 and P5 are the new boundary's caller and its domains;
- P7 is the records.

DELTA: within

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P0 | Spec amendment, judged before any test: Settlement 1's parenthesis and Trust's out-of-lane ruling gain the close-first case (a linked worktree whose branch has closed its claim while trunk's committed tree still holds `active/<branch>/` is a lane), with its reason (the final verdict round's REVIEW log is gate evidence, `kitlib.verdict.logged_rounds`). The primary checkout stays outside a lane on every branch, as written. One confirming critique judges the amendment. If it is refused, the lane stops here and closes partial, with the conflict drafted as a successor | F1; D7; SR-222 | no interface: spec text only, no code seam crossed | |
| P1 | Spine intent turn, TC-first (Terra by today's `terra_author.sh`, before build round 1, because the route does not exist yet). Terra drafts: the derived SR under SN-026; its LLR (the coordinator's codex call); two new TCs (entry-point behaviour; cycle text); amendments to LLR-269 (spool arm with the P0 predicate, refused-commit report, unretained resume), IF-246 (data, requestors) and TC-265 (spool arm, report, retired shell launchers). Each TC names the tests P2 adds | D1; D13; F1; SR-222; TC-265 | IF-246 | P0 |
| P2 | Test commit: every test below, marked strict expected-failure with the red it raises; the `claimed_lane` conftest helper (a claimed linked worktree); the existing record-path tests moved onto it (green on today's code, because today's `record` ignores lane-ness) | D1; D2; D3; D4; D5; D6; D7; D8; D9; D10; D11; F1; F2; SR-222; TC-265 | IF-246; IF-282 | P1 |
| P3 | `session_service.py`: `lane_branch(root)` per decision 3 (`worktree_index` moved to `agent_common`, `coordinator_adjudicate` re-pointed, no behaviour change); `record`'s spool arm into `out/sessions/spool/` of the primary checkout; the caller-owned `report` dict (`committed`/`spooled`/`refusal`); `Call.resume`; `is_call_log(name)` beside `_call_row`. Plus the IF-246 contract body | D4; D7; D8; D9; F1; SR-222; TC-265 | IF-246 | P2 |
| P4 | `scripts/coordinator/codex_call.py`: the route, the template, the change check. It resolves the role's enabled row, refuses before launch (exit 2), snapshots, runs `act`, snapshots, judges, runs `record`, writes `--out`, prints. The judge is a pure function over two snapshots and the commit range | D2; D3; D4; D6; D7; D8; D10; SR-222 | IF-246; IF-282 | P3 |
| P5 | The resume arm: the name-ordered walk over every standard-call log at HEAD (decision 4, P5 detail), header completeness read by `agent_common.log_meta_text` (which `read_log_meta` calls), the uncommitted-log check over the same name grammar, every bad input refused before launch naming the path; launch through `Call.resume` | D5; D9; F2; SR-222 | IF-246 | P4 |
| P6 | Text, with the shell launchers retired: `sol_review.sh`, `terra_author.sh` and `luna_review.sh` deleted. Recipes §1 (Terra first turn and resumed; the review, scope-critique and plan-critique launches; "note the session id"), §7 (the Sol probe, the D-017 line) and SKILL Roles name the entry point and its blackout refusal. The three skill copies are synced. `scripts/coordinator/README.md` lists the entry point. `docs/runtime-flows.md` gains Flow 7 | D10; D11; SR-222; TC-265 | no interface: skill, README and flow text only, no code seam crossed | P5 |
| P7 | Records: IF-246 (requestors gain `scripts/coordinator/codex_call`; data names the spool arm, the report, `resume`, `is_call_log`), IF-282 (requestors), the new LLR's traced cells, `Implements:` lines, module-size and complexity re-stamps the growth crosses, and one RESYNC §4 entry listing the callers whose root is outside a lane | D13; SR-222; TC-265 | IF-246; IF-282 | P6 |
| P8 | Live runs through the lane's copy of the route: the lane's REVIEW-A round 1 (Sol) and its spine checkpoint turn (Terra), from the lane's linked worktree, each log committed there; one scope critique from the detached `trunk-tmp` checkout, its log spooled, nothing committed | D12; SR-222 | IF-246 | P7 |
| P9 | Landing: the commit bar, `check_trajectory.py --strict` and `trace.py --strict` clean; the derived SR, LLR, new TCs and the amendments judged at the lane's sitting; the RESYNC entry re-anchored at the landing's parent; the full suite runs TC-262, TC-263, TC-264, TC-351 and TC-362 unchanged | D13; SR-222; TC-262; TC-263; TC-264; TC-265; TC-351; TC-362 | no interface: landing bookkeeping, no code seam crossed | P8 |

TC-262, TC-263, TC-264 and TC-362 verify the adapters' capture, occupancy,
usage mapping and account homes. TC-351 verifies reviewer retention. This item
uses those paths and changes none of them. P9 runs them in the full suite, and
they need no amendment.

## Step detail

### P0: the spec amendment (before the tests)

- **Edit.** In the lane's spec only:
  - Settlement 1's ruling keeps "the primary checkout, a detached HEAD, or a
    branch with no claim under `docs/work/active/<branch>/`, the predicate
    `lane_refusal` already states". It adds: "a linked worktree whose branch
    has moved its claim out under close-first while trunk's committed tree
    still holds it is a lane: its final verdict round's REVIEW session log is
    the integrator's gate evidence, which must commit on the branch".
  - Trust's out-of-lane ruling adds that any unreadable claim read decides
    "not a lane".
  - The Critique dispositions record the amendment and its cause: the plan
    critique's F1, confirmed. Done-when is unchanged. D7's three spool cases
    stand as written.
- **Judgement.** One confirming critique of the amended spec (Sol, medium,
  convergence stance), run by the coordinator's existing recipe.
- **Refused.** If the amendment is refused, the literal predicate would refuse
  every loop lane's merge (above). The lane does not build that predicate and
  does not build around it. It closes partial, and the conflict between
  close-first and the branch-tree reading is drafted as its own successor.

### P1: spine intent turn (TC-first; Terra, before build round 1)

All requirement-voice text is in capability voice, with no file, module or
path in a requirement cell (ruling 5). `module` and `code_symbol` are the
traced cells, filled at P7.

- **The trigger.** SR-222 binds "the delivered loop content". The
  coordinator's codex calls are launched by this repo's own tooling, which is
  not delivered. SR-222 also does not say where a call's record goes outside a
  unit of work. So the spec's conditional applies.
- **Derived SR** (new, Drafted, labelled derived), `sn_refs = ["SN-026"]`,
  with SR-231's rationale as its lens. Its text is the spec's. Its acceptance
  lists:
  - the recorded lane call;
  - the spooled out-of-lane call, outside meaning the shared line's own
    checkout, a detached checkout or an unclaimed branch;
  - a closed-but-unmerged unit of work still committing its record (P0);
  - a refused commit, reported and never success;
  - a resumed authoring turn continuing the recorded thread, refused on a
    missing, damaged, foreign or newer-uncommitted record;
  - the edit check's verdicts, with the other-call discount and the
    unreadable arm.
- **New LLR** (Drafted, CMP-008) under the derived SR. Its detail covers:
  - role to route, and the declared sandbox template;
  - the refusals before launch;
  - the two snapshots (HEAD; every uncommitted path with its content identity);
  - Sol's and Terra's rules;
  - the discount: a non-merge commit in the range that only adds
    standard-call logs; an uncommitted log that is new, or that a discounted
    commit added with the same content;
  - a non-descendant HEAD is an edit, and git unreadable means the check
    could not run;
  - the resume walk (P5) and its binding;
  - the exit codes and the out file.
- **LLR-269 amendment:** `record`'s two arms; the lane test with its
  close-first case and the "unreadable is not a lane" direction; a spool-write
  failure raising; a refused commit reported to the caller; the unretained
  resume.
- **IF-246 amendment:**
  - `data` gains `Call.resume`, `record(..., report=)`, `is_call_log` and the
    spool;
  - `requestors` gain `scripts/coordinator/codex_call`.
- **TC (new), the codex call** (Integration, Test). It verifies the derived
  SR, the new LLR, LLR-269 and IF-246. Its evidence is P2's `test_codex_call.py`
  and `test_codex_call_git.py` and the new `test_session_service.py` tests.
- **TC (new), the cycle text** (Test, a text pin). It verifies the derived SR
  and the new LLR. Its evidence is P2's two `test_prompts.py` pins.
- **TC-265 amendment:** the method gains the spool arm, the report and the
  resume field. "Retired wrappers ... referred to nowhere" names the three
  shell launchers.
- Terra's prompt follows recipes §1: `CHANGES=none`, `TESTS=` empty. Record
  the session id in `docs/decisions/wi-960.toml`. This is the last turn whose
  id lives there.
- Keep the intent set as a patch where a row names a module the build creates.
  It rides the build commit that creates the module (wi-940 D-002).

### P2: the tests, first (one commit, strict expected-failure marks)

Each new test carries `xfail(strict=True, raises=(...))` naming the red it
raises today. The marks come off in the step that delivers it. A loader helper
in the entry-point tests calls `pytest.fail` when
`scripts/coordinator/codex_call.py` is absent, so the red is
`pytest.fail.Exception`, never a collection error.

**The stand-in** is a `codex` executable put first on `PATH`: a Python
script, plus `codex.cmd` on Windows (reuse TC-362's fixture-CLI helper in
`tests/test_accounts.py` if it fits). It reads a scenario from an environment
variable, then:
- records its argv and a "launched" marker;
- writes the `-o` file;
- prints the live `tests/golden/sessions/codex-exec-json.jsonl` stream;
- performs the scenario's git act in its cwd: commit a work file; leave one
  uncommitted; run `session_service.record` in-process for a second call;
  `reset --hard HEAD~1`; leave `.git` index locked; or make git unreadable.

**`claimed_lane(tmp)`** goes in `conftest.py`.
- It builds a primary checkout with `hooked_checkout` and declares
  `[policies] trunk = "main"`.
- It commits `docs/work/active/wi-1/WI-1-x.md` on `main`, cuts `wi-1`, and adds
  a **linked worktree** on `wi-1` beside the primary.
- It returns the worktree, which is a lane under decision 3.
- Variants for `test_lane_ness...` close the claim on the branch, or drop it
  from trunk.

New tests, smoke tier (in-process):

| Test | Clause | Red on today's code |
|---|---|---|
| `test_session_service.py::test_a_call_outside_a_lane_spools_its_log_and_commits_nothing` (a primary-checkout root) | D7; F1 | the log is under `docs/iteration/` and the commit spy is called |
| `test_session_service.py::test_an_unreadable_lane_reading_spools` (the worktree readers or `ls-tree` failing) | D7 | as above |
| `test_session_service.py::test_an_unwritable_spool_raises_and_commits_nothing` | D8 | no raise; it commits |
| `test_session_service.py::test_a_refused_telemetry_commit_is_reported_to_the_caller` (the spy returns a veto) | D8 | `TypeError`: `record` takes no `report` |
| `test_session_service.py::test_a_resumed_call_launches_the_resume_form_and_logs_resumed` | D9 | `TypeError`: `Call` has no `resume` |
| `test_session_service.py::test_a_call_with_both_keep_and_resume_is_refused_before_accounting` | D9 | `TypeError` |
| `test_session_service.py::test_the_standard_call_log_name_is_never_a_gate_log_name` (round trip with `_call_row`) | D4 | `AttributeError`: no `is_call_log` |
| `test_coordinator_adjudicate.py::test_lane_refusal_is_unchanged_by_the_shared_worktree_index` (its existing primary/detached/unclaimed/claimed cases, run against the moved reader) | F1 | `AttributeError`: `agent_common` has no `worktree_index` |
| `test_codex_call.py::test_each_role_launches_its_enabled_roster_row` (a disabled or unknown entry: exit 2) | D2 | module absent |
| `test_codex_call.py::test_the_launch_keeps_the_wrappers_sandbox` (unelevated, workspace-write, the primary's review-tmp as the writable root from a lane root, effort, `--skip-git-repo-check`, roster model, stdin prompt, no `--dangerously-bypass...`) | D2 | module absent |
| `test_codex_call.py::test_sol_reads_any_change_but_the_discount_as_an_edit` | D3 | module absent |
| `test_codex_call.py::test_only_a_commit_adding_standard_call_logs_is_discounted` (a gate-grammar log, a modified log, a deleted log, a work path, a mixed commit, a merge) | D4 | module absent |
| `test_codex_call.py::test_an_uncommitted_call_log_committed_during_the_call_is_discounted_only_unchanged` | D4 | module absent |
| `test_codex_call.py::test_terra_keeps_uncommitted_output_and_reads_only_an_undiscounted_head_move` | D3 | module absent |
| `test_codex_call.py::test_a_head_that_is_not_a_descendant_is_an_edit` | D6 | module absent |
| `test_codex_call.py::test_an_unreadable_snapshot_never_reads_clean` | D6 | module absent |
| `test_codex_call.py::test_the_resume_walk_refuses_each_bad_carrier` (see the list below), each naming the log and the cause | D5; F2 | module absent |
| `test_codex_call.py::test_an_older_valid_carrier_behind_a_newer_damaged_log_is_never_continued` (an older valid lane `AUTHOR` log committed, then a newer `call_` log committed with its header cut before `role`; and the same newer log uncommitted; and one that is garbage bytes: refused, the newer path named, nothing launched) | D5; F2 | module absent |
| `test_codex_call.py::test_newer_well_formed_logs_of_other_roles_or_lanes_are_skipped` (a newer Sol `REVIEW-A` log and a newer foreign-lane `AUTHOR` log carried in by a refresh: the older lane carrier is taken) | D5; D9 | module absent |
| `test_prompts.py::test_the_cycle_says_sol_and_terra_calls_are_refused_in_the_blackout_window` | D10 | the phrase is absent |
| `test_prompts.py::test_no_recipe_launches_sol_or_terra_outside_the_entry_point` (all three copies: no `codex exec` line naming `gpt-6.1-sol`, `gpt-5.6-terra` or `resume`, and no `sol_review`, `terra_author` or `luna_review`) | D11 | recipes §1 and §7 carry them |
| `test_session_service.py` structural guard: the retired-name list gains the three shell launchers | D11 | `scripts/coordinator/*.sh` and the recipes name them |

The bad-carrier list for `test_the_resume_walk_refuses_each_bad_carrier`:
- no lane `AUTHOR` log at all;
- a blob `git show` cannot read;
- a header with no `# ---` terminator;
- a header with no `role`, `started-at` or `roster-row`;
- an empty `session-id`;
- a lane `AUTHOR` log on another route;
- two lane `AUTHOR` logs with the same name stamp;
- an uncommitted lane `AUTHOR` log newer than the carrier.

New tests, slow tier: `tests/test_codex_call_git.py`, added to `SLOW_MODULES`
(it runs real git and subprocesses). The in-process judge and walk tests above
keep the family's smoke pin.

| Test | Clause | Red on today's code |
|---|---|---|
| `test_a_sol_review_in_a_lane_commits_one_call_log_with_codex_usage` (on `claimed_lane`: one new `telemetry:` commit adding exactly one `docs/iteration/call_*.log`; `gen_ai.usage.input_tokens`/`output_tokens` filled; `cli = codex`, `provider = OPENAI`, `roster-row = OPENAI-SOL`; `--out` holds the final text; exit 0) | D2 | the script is absent |
| `test_a_committed_work_file_is_an_edit_and_the_log_is_still_recorded` | D3 | absent |
| `test_an_uncommitted_work_file_is_an_edit_for_sol_and_output_for_terra` | D3 | absent |
| `test_another_calls_log_commit_during_the_run_is_not_an_edit`, plus its parametrized edits (a gate-grammar log, a modified log, a work path: exit 3) | D4 | absent |
| `test_a_waiting_call_log_committed_by_its_own_record_is_not_an_edit` (exit 0; modified or deleted instead: exit 3) | D4 | absent |
| `test_a_resumed_turn_with_a_bad_carrier_never_launches` (the smoke walk's cases, the newer-damaged case included, through the CLI; exit 2, the path and cause on stdout, no "launched" marker) | D5; F2 | absent |
| `test_a_rewritten_history_is_an_edit` and `test_git_unreadable_after_the_call_is_never_success` | D6 | absent |
| `test_a_call_outside_a_lane_spools_and_changes_nothing` (primary checkout on trunk; primary checkout on a claimed branch; a detached linked worktree; an unclaimed branch. For each, `for-each-ref`, HEAD and status are unchanged, the log is under the primary's `out/sessions/spool/`, and the path is printed) | D7; F1 | absent |
| `test_concurrent_calls_from_one_detached_checkout_each_spool_their_own_log` (three processes; three distinct logs) | D7 | absent |
| `test_a_refused_telemetry_commit_exits_nonzero_naming_the_log` (index locked; exit 4; the log path printed; the log uncommitted) | D8 | absent |
| `test_a_second_terra_turn_resumes_the_first_turns_thread` (turn 1 commits a log with the stand-in's `thread.started` id; `docs/decisions` names another id; turn 2's argv is `exec resume <logged id>` with no `-C`; its log has `session-mode: resumed`) | D9 | absent |
| `test_a_call_inside_the_blackout_window_is_refused_before_launch` (each role; exit 2; no log; no "launched" marker) | D10 | absent |
| `test_lane_ness_follows_the_written_predicate_and_the_close_first_case` (see the claim-state matrix below) | D7; F1 | `AttributeError`: no `lane_branch` |

The claim-state matrix for `test_lane_ness_follows_the_written_predicate_and_the_close_first_case`:

| Root | Claim on the branch | Claim on trunk | Expected |
|---|---|---|---|
| primary checkout on trunk | none | none | not a lane |
| primary checkout on claimed B | yes | yes | not a lane |
| detached linked worktree | n/a | n/a | not a lane |
| linked worktree on B | yes | yes | lane |
| linked worktree on B | no (closed) | yes | lane, the P0 case |
| linked worktree on B | yes | no | lane, as `lane_refusal` |
| linked worktree on B | no | no | not a lane |
| no trunk declared | yes | n/a | lane |
| no trunk declared | no | n/a | not a lane |
| trunk's `ls-tree` failing, branch closed | no | unreadable | not a lane |

**Existing tests moved onto `claimed_lane`.** Every test that asserts
`record`'s commit or a log under `docs/iteration/` from a service route moves.
They stay green on both sides. By grep that is:
- `test_session_service.py`, `test_session_keep.py`,
  `test_coordinator_adjudicate.py` (its lane fixture already is a linked
  worktree; it gains the trunk-side claim `integrate.claim` writes),
  `test_adjudicator_token.py`, `test_blackout_window.py`;
- `test_agent_loop*.py`, `test_dual_plan_*.py`, `test_loop_provenance.py`,
  `test_verdict_record.py`, `test_integrate_admission.py`.

The full suite at the end of P3 is the inventory. No assertion is weakened,
and no seam replaces the predicate where a claimed linked worktree can be
built. A linked worktree costs one `git worktree add`. If the move or the new
smoke tests cross `[tiers] max-tests` or the smoke budget, re-stamp in this
commit with the reason (wi-927 D-002). Never fold cases.

### P3: the service (`session_service.py`)

- **`lane_branch(root)`**, per decision 3.
  - It reads `agent_common.worktree_records` and `worktree_index` (moved
    verbatim from `coordinator_adjudicate._worktree_index`, which now imports
    it).
  - The branch side is `integrate.claimed_ids_on_branch(root, B)`, through a
    deferred `import integrate`. That makes no cycle (above).
  - The trunk side is one `ls-tree -r --name-only refs/heads/<trunk>
    docs/work/active/B/`, with ids parsed as `integrate._spec_id` does (called,
    not copied).
  - It returns B when either side holds a claim. It returns None on index 0,
    a detached HEAD, a root that is not the top of a worktree, or both sides
    empty or unreadable.
  - A sibling `lane_wis(root)` returns the union of ids, for P5.
- **`record(..., report=None)`.**
  - When `lane_branch(root)` is None, it writes through `write_session_log`
    into `session_keep.primary_out_dir(root) / "sessions" / "spool"`, ignoring
    `iter_dir`. It keeps the raw stream and commits nothing.
  - A spool it cannot create or write raises `OSError`.
  - Otherwise it commits as today and keeps `commit_telemetry`'s return value.
  - `report` is filled with `{"path", "spooled", "committed", "refusal"}`. The
    return value stays the path.
  - The rule is derived from the root alone (C3).
- **`Call.resume: str = ""`.** A non-empty `resume` together with `keep`
  raises `ValueError` before anything is accounted. Otherwise
  `argv = adapter.resume(argv, call.resume)`, and `_identity` sets
  `session-mode = resumed` for `keep.session_id or resume`.
- **`CALL_LOG_RE` / `is_call_log(name)`** match `call_<32 hex>-<8 digits>-<6
  digits>.log`, with group `stamp`. `SESSION_LOG_RE` must not match the same
  names, and `_call_row` keeps producing that exact name.
- The module docstring's IF-246 contract body states the spool arm with its
  predicate, the report, the unretained resume and the grammar.
- The strict marks come off P2's service, adjudicator-reader and lane-ness
  tests.

### P4: the entry point (`scripts/coordinator/codex_call.py`)

Usage: `codex_call.py ROLE --prompt-file P --out O [--root DIR] [--wi WI-N]
[--effort medium] [--route ENTRY] [--resume] [--timeout 7200]`. `--resume`,
and a required `--wi`, apply to `AUTHOR` only. The idle bound is 900 s.

1. **Refusals before launch (exit 2):**
   - an unknown role, or `--resume` off `AUTHOR`;
   - an unreadable prompt;
   - `resolve_route` or `launch_env` failing (`SigninRefused` included);
   - for `--resume`, the P5 walk.
2. **Snapshot before:**
   - `rev-parse HEAD`;
   - `status --porcelain=v1 -z --untracked-files=all`;
   - `hash-object` of every listed path still on disk.
3. **`session_service.act(Call(...))`** with `role`, the template, the row's
   `family`/`tier`/`id`/`model`, `source_event="coordinator"`, and
   `attribution={"wi": wi}`. `BlackoutRefused`/`HooksOffRefused` map to exit 2.
4. **Snapshot after, then judge.** The judge is a pure function of the two
   snapshots, the range and the role.
   - `merge-base --is-ancestor before after` must hold, else it is an edit.
   - Any merge in `rev-list --parents before..after` is an edit.
   - A commit is discounted only when every `diff-tree --no-renames -r
     --name-status` entry is an `A` of a `docs/iteration/` path that
     `is_call_log` accepts.
   - For Sol, every changed path in the status is an edit, with two
     exceptions: a new standard-call log, and a log that was uncommitted
     before and that a discounted commit added with a blob equal to its
     before identity.
   - For Terra, the status is output.
   - Any failing git read means "could not run", never clean.
5. **`session_service.record(outcome, row, report=r)`** with `_call_row`'s row,
   also after an edit. Then `--out` gets `outcome.text`.
6. **Print** the route, model and effort; the edit paths; the log path with
   `committed`, `spooled` or `NOT COMMITTED: <refusal>`; and the out path.
   Return per decision 5.

### P5: Terra's resume arm (the name-ordered walk)

- **Candidates are found by name.** Every path from `git ls-tree --name-only
  HEAD docs/iteration/` that `is_call_log` accepts is a candidate, whatever its
  content. They are sorted newest first by the name's `stamp`, which
  `_call_row` fixes before the write and which no truncation can remove.
- **The walk** reads each candidate with `git show HEAD:<path>` and parses it
  with `agent_common.log_meta_text(text)`, which returns the header fields and
  whether the `# ---` terminator was reached. `read_log_meta` calls it, so
  there is one header grammar. Newest first:
  - **Refuse, naming the path,** when the blob cannot be shown, or the header
    has no terminator, or it lacks any of `role`, `roster-row`, `wi` or
    `started-at`. Such a log might be a damaged newest carrier, so it is never
    stepped over.
  - **Skip** a well-formed log whose `role` is not `AUTHOR`, or whose `wi` is
    not among `lane_wis(root)`. These are other calls' logs and other lanes'
    logs carried in by a refresh.
  - **Refuse, naming it,** a well-formed lane `AUTHOR` log on another
    `roster-row`, or one with an empty `session-id`.
  - **Take** the first well-formed lane `AUTHOR` log on the Terra route. A
    second one with the same stamp is a tie, and the turn is refused naming
    both.
  - **Refuse** when the walk ends with nothing taken (no carrier).
- **The uncommitted check.** Every uncommitted or untracked path under
  `docs/iteration/` that `is_call_log` accepts, and whose stamp is not older
  than the taken carrier's, is read from the working tree.
  - If it is malformed by the same test, or it is a lane `AUTHOR` log, the
    turn is refused, naming it, so the coordinator commits or inspects it
    first. A log killed mid-write lands here.
  - A well-formed log of another role or lane is ignored.
- **Every refusal** exits 2 and names the path and the cause. Nothing is
  launched, no fresh thread starts, and the decisions record is never read.
  Recovery is the coordinator's explicit choice: commit or inspect the named
  log, or run a first turn without `--resume`.
- **On success**, it launches `Call(resume=<session-id>, role="AUTHOR", ...)`.
  The strict marks come off D5, D9 and F2's tests.
- **The cost.** A committed malformed `call_` log of another role, newer than
  the carrier, also refuses until a newer turn supersedes it. That is the
  deny-by-default direction the spec's ruling asks for. A committed log is
  rare, because `record` commits only after the write completes.

### P6: text, with the shell launchers retired

- Delete `sol_review.sh`, `terra_author.sh` and `luna_review.sh`.
- Recipes §1:
  - Terra's first and resumed turns become `"$PY" "$TOOLS/codex_call.py"
    AUTHOR --root <lane worktree> --wi WI-NNN --prompt-file <prompt> --out
    <out> [--resume]`.
  - "Note the session id" becomes "commit a turn's log before the next turn".
  - The review, plan-critique and scope-critique launches become `REVIEW-A`
    or `CRITIQUE` with `--root <lane worktree>` or `--root <trunk-tmp>`. The
    trunk-tmp form states that its log spools.
  - The orphaned-bash note retires.
- Recipes §7: the Sol probe is a one-word `CRITIQUE` call from the detached
  checkout. The D-017 line becomes `--route <enabled Luna row>`.
- Recipes and SKILL Roles state:
  - inside the blackout window, a Sol or Terra call is refused before launch
    (exit 2), as every non-adjudication call is;
  - exit 3 is an edit, exit 4 an uncommitted log, exit 5 a check that could
    not run;
  - a call from the primary checkout spools.
- Edit `project-trajectory/skills/coordinator-cycle/`, then sync the
  `.claude/` and `.agents/` copies byte for byte.
- `scripts/coordinator/README.md`: the codex-call section replaces the Luna
  one.
- `docs/runtime-flows.md` gains Flow 7, "A coordinator codex call".
- Flagged, not changed: recipes' TC-055 dashboard judges run `codex exec -i
  <png>` on the CLI's default model. That is neither Sol nor Terra, and it is
  unrecorded.

### P7: records

- IF-246's `requestors` gain `scripts/coordinator/codex_call`, and its `data`
  is amended. IF-282's `requestors` gain it.
- The new LLR's `module` is
  `scripts/coordinator/codex_call.py;project-trajectory/scripts/session_service.py`,
  with its `code_symbol`s. LLR-269's `code_symbol` gains
  `lane_branch/lane_wis/is_call_log`. LLR-306's `code_symbol` follows
  `worktree_index` if it names `_worktree_index`.
- Add `Implements:` lines. Re-stamp any module-size or complexity row the
  growth crosses (`session_service.py`, `agent_common.py`), with the reason in
  `docs/decisions/wi-960.toml`.
- **RESYNC §4, one entry:** "`record` spools a session log outside a claimed
  lane". Overwrite `session_service.py`, `agent_common.py` and
  `coordinator_adjudicate.py`.
  - In an adopter's repo, calls rooted at the primary checkout, a detached
    checkout or an unclaimed branch now spool under `out/sessions/spool/` and
    commit nothing. The builder confirms each caller's root by reading it:
    the keep-warm pings, an `--interactive` sitting, the recovery probe from
    the primary checkout, and dual-plan hats rooted there.
  - Workers in claimed linked worktrees (closed-but-unmerged ones included)
    and the adjudicator commit as before.
  - The entry also says that spooled logs are machine-local until WI-800, that
    `record` reports a refused commit, and that `Call` gains `resume`.
  - It is a forced migration only for an adopter who relied on trunk telemetry
    commits. That includes attended serial work on the primary checkout,
    whose logs now spool. Flag it for the owner.

### P8: live runs (D12)

- From the lane's linked worktree, with the lane's copy of the entry point:
  - REVIEW-A round 1. Confirm that Sol's pytest ran under the writable root
    and that the `call_` log is committed in the lane.
  - The spine checkpoint Terra turn: a fresh first turn, its log committed in
    the lane.
- One scope critique from `$REPO.wt/trunk-tmp`. Its log is under the primary's
  `out/sessions/spool/`, and HEAD, status and refs are unchanged.
- If the route is defective so that a launch cannot run, that one launch runs
  by hand, attended and recorded, and the defect is fixed forward with a
  regression test ("Machinery landing alone").

### P9: landing

- The commit bar (`run.cmd smoke`) is green, and `check_trajectory.py
  --strict` and `trace.py --strict` are clean.
- The derived SR, the new LLR, both new TCs and the amendments (LLR-269,
  IF-246, IF-282, TC-265) are judged at the lane's sitting. The P0 spec
  amendment is already judged.
- The RESYNC entry is re-anchored at the landing's parent.
- The full suite at phase close runs TC-262, TC-263, TC-264, TC-351 and TC-362
  unchanged.
- The route lands alone.

## Observed elsewhere, not changed here

`coordinator_adjudicate.lane_refusal` reads the claim only off the branch's
tree, so a lane closed by close-first reads as unclaimed to the adjudicator.
P0's amendment covers `record` only. SR-231's entry point is left as it is. If
adjudications after close occur, that is a separate row.
