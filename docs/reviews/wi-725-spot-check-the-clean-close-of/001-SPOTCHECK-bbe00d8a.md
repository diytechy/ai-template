# SPOTCHECK — WI-725 — the clean close of WI-720, judged at bbe00d8a

A sampled spot check of a GREEN close (`docs/process.toml [attestation]
complete_review = "sample"`). One question: does what shipped answer what the
row asked for, which is the eleven numbered cell fixes in WI-720's Context and
its OUT OF SCOPE list? The close stands whatever is found here. A finding is a
successor row, never a reversal.

What was read: the closed spec
`docs/archive/work/complete/WI-720-sr-222-sr-227-chains-name-the.md`; the
squash `bbe00d8a` (`git show`, `--stat`, `--numstat`); the lane's review
`docs/reviews/2026-09-28-wave6/sonnet-wi720.md`; the log section "WI-720
lands" in `docs/log.d/2026-09-28-wave6-coordinator.md`; the ten rows at HEAD
(SR-222 and SR-227; LLR-266 to LLR-270; TC-262, TC-264 and TC-268), plus
TC-263, TC-265, TC-266, TC-267 and LLR-177; `.claude/skills/spine-authoring/SKILL.md`
§6; `project-trajectory/scripts/session_adapters.py` (the module and IF-245
docstrings, `PlainAdapter`, `_claude_raw`, `_claude_usage`, `_claude_model`,
the three adapters' `prepare`, `final_text`, `provider` and `usage`, and
`_codex_lastmsg_setup`); `session_service.py` (`_identity`, `KeepWarmer.tick`,
`_start`) and every `Call(` site in `agent_loop.py` and `plan_runner.py`;
`agent_common.redact_secrets` / `write_session_log`; `tests/test_session_keep.py`
(the TC-268 evidence test), `tests/test_session_service.py` and
`tests/test_session_adapters.py` (the semconv and provider assertions); and
the queued adjudication `docs/work/queued/WI-724-adjudicate-llr-266-llr-267.md`.
I checked every clause against the registries, the code, the tests or the
diff, not against the builder's or the reviewer's account. HEAD stayed at
28d35286 throughout.

What was run, in this worktree:

- `python -m pytest -q -n 2 tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py -p no:cacheprovider`
  -> `103 passed in 37.14s`.
- `python project-trajectory/scripts/trace.py --root . --strict` at HEAD ->
  exit 0, `orphans=0 integrity=0 ... drafts=12`.
- The flip check. A script set `status = "Approved"` on exactly the ten rows
  (`git diff --stat`: 10 insertions, 10 deletions over the three registries).
  I then ran the same `trace.py --root . --strict` and restored the three
  files with `git checkout --`. The run exited 1 with `integrity=10
  approval-record=10`. All twenty new lines are the expected "reads
  Status=Approved but its docs/archive/last_approved copy reads
  Status=Drafted" pair, one pair per row, because no snapshot was taken.
  There was no `requirement form` line (`grep -ic` gave 0) and no new
  citation-frame or paraphrase advisory. The only other change is that the
  two "LLR-267/LLR-269 reads 'Drafted' but every citing TC is Approved"
  advisories cleared. After the restore, `git status --short` was empty and
  `git diff --quiet HEAD` held. The flip script and the trace captures lived
  in the session scratchpad, outside the worktree, and were deleted
  afterwards.
- `git show --numstat bbe00d8a`: 7/7 lines in `low-level-requirements.toml`,
  4/4 in `system-requirements.toml`, 2/2 in `test-cases.toml`, 2/2 in
  `session_adapters.py` and 1/1 in `tests/test_session_keep.py`.
- A regex scan of every string cell of the ten rows, and of TC-263 and
  TC-265 to TC-267, for receipt words (before, already, now, no longer,
  today, fixed, defect, was, were, misread, existed, still, owed, NOT LIVE).
  The hits are judged below.

## Per-clause findings (WI-720 Context, items 1 to 11)

1. [MET] `SR-222.requirement` / `acceptance_criteria` now name "the route's
   provider filled from its roster row for every routed call, the runner
   named, the vocabulary's gen_ai.provider.name filled where the runner
   reports one", and the acceptance says the same, with the name "empty
   where it does not". This is true of the code. `session_service._identity`
   writes `provider` from `Call.provider`. Every routed `Call` fills it from
   the route: `agent_loop.launch_session` uses `plan["route_family"]`, the
   route probe (`agent_loop.py:3623`) and the keep-warm `_start`
   (`session_service.py:531`) use `row.family`, and `plan_runner` uses
   `route.family`. The one `Call` that passes no provider is the hands-on
   `INTERACTIVE` sitting (`agent_loop.py:2161`), which has no route id, so
   "routed" excludes it correctly. `gen_ai.provider.name` is `anthropic` for
   claude, `openai` for codex, and "" for opencode and the plain adapter.
   `test_act_launches_through_the_adapter_and_accounts_the_call` asserts
   `m["provider"] == "OPENAI"`, and the claude and codex usage tests assert
   the two names. The obligation set is unchanged. No other acceptance cell
   moved: SR-227's acceptance appears in the diff as context only.
2. [MET] `SR-222.rationale`: "was the owner's choice" is gone. The argument
   the item names is kept: the problem is not novel, and because the
   vocabulary has no tagged release the record pins the exact revision. The
   builder also dropped "every name in it is still at development stability
   and its repository moved in 2026". The first half was a standing reason,
   but the item did not ask for it, and the `OTEL_SEMCONV` comment still
   carries it. No argument the row needs is lost.
3. [MET] `SR-227.rationale` now reads "a run that spins a fresh adjudicator
   for every small work item reloads the spine on each call, and the usage
   record makes that cost visible". That is present voice, with no past
   observation and no "extreme".
   The reviewer's accepted minor is fine, and I judge it so on the
   argument, not only because the sentence is still true. The dropped text
   was "costs about what a standing process would under the provider's
   hour-long prompt cache", and its two parts fare differently:
   - The "hour-long" figure is a per-provider quantity. The row does not
     own it, and nothing on this box has measured it for codex or opencode:
     measuring their cache TTLs is WI-541's Done-when. Keeping it would
     have left an unverified number in a standing cell.
   - The standing-process comparison is the alternative that lost, and the
     same rationale still states it: "a session is retained as a transcript
     a bounded process replays, never as a long-lived process, so an
     unattended run still cannot wait on a prompt".
   The performance argument still holds without either: a fresh session
   per item reloads the spine, and resuming uses the prompt cache.
4. [MET as asked; residue in the same cell, see Observation 1]
   `LLR-266.detail` now reads "run_session captures the whole stream; the
   adapter, not the launch, reads the final text". `LLR-266.rationale`
   states what breaks without the row, as item 4 asked. Both are true of
   `CodexAdapter.final_text` and `OpencodeAdapter.final_text`.
5. [MET] `LLR-267.rationale`: "34,836%" is gone. "Their sum over the window
   overstates occupancy" stands alone.
6. [MET] `LLR-268.detail` now says "raw-usage is the whole result event line
   verbatim. That line carries the result text, so the log writer redacts
   header values (LLR-177)". This matches `_claude_raw`, which returns the
   last `type: result` line through `_verbatim`, and
   `test_claude_usage_is_mapped_to_the_pinned_otel_names`, which asserts
   `raw-usage == "[" + result_line + "]"`. It also matches LLR-177's detail,
   which says `write_session_log` passes every header value through
   `redact_secrets`. The IF-245 docstring sentence was changed in the same
   commit to match (`session_adapters.py:33-34`). `LLR-268.rationale` now
   gives the standing reasons, which match `_claude_usage` (it reads
   `output_tokens_details.thinking_tokens`) and `_claude_model` (the last
   assistant event's model first).
7. [MET] `LLR-269.rationale`: "a launch or logging path per role lets a fix
   ... reach one path and miss the others" is the standing consequence.
8. [MET] `TC-262.expected`: "codex's final text is its last-message file and
   opencode's is its last speaking step". The cell is about a successful
   call, so this is true of `final_text` (the last-message file on exit 0)
   and of the opencode step walk.
9. [MET; the optional part not taken, see Observation 2] `TC-264.expected`
   now states the two conditions in place of "the two claude defects
   fixed".
10. [MET] TC-268's evidence now asserts `lines == ["keep-warm: skipped (a
    ping is in flight)"]`. At HEAD this is deterministic. The first tick
    starts the ping, whose thread blocks on `release.wait(10)`. On the
    second tick `KeepWarmer.tick` finds the thread alive and
    `due_routes(...)` true, so it appends the skip line and returns before
    `take_warm_lease`. `_once` returns the line because the previous tick
    said nothing. The Method's "a second tick starts nothing and says so"
    is now what the evidence asserts. The exact-line equality rules out
    the start path, because that path would have produced `[]` or a
    lease-skip line. The later `(log,) = ...` and
    `committed == [<one thread>]` also confirm that only one ping ran.
    `session_service.py` did not change in the squash, so the Deliverable's
    "green before and after" holds.
11. [MET] `LLR-270.rationale`: "at the off dial the launch is exactly a fresh
    session's". This matches SR-227's acceptance and
    `test_at_dial_zero_an_adjudication_launches_exactly_as_a_fresh_session`.

## OUT OF SCOPE held

- Only the named cells moved. The registry hunks touch SR-222's
  requirement, rationale and acceptance, SR-227's rationale, the details and
  rationales item by item for LLR-266 to LLR-270, and TC-262's and TC-264's
  expected cells. TC-268 has no registry hunk; only its evidence test moved.
- No `hat_refs`, `sn_refs`, `boundary_refs`, `sr_refs`, `verifies`, `tier`,
  `level` or `phase` value is in the diff.
- All ten rows read `Drafted` at HEAD.
- TC-263, TC-265, TC-266 and TC-267 are absent from the diff and read
  `Approved`.
- The codex and opencode `NOT LIVE ... owed to a person` wording in the TC
  methods was left alone, as the row directed.
- The only code change is the one docstring sentence.

## Observations (none is a gap in what the row asked; the first two are for WI-724)

WI-724, the first-approval adjudication minted at this merge, already reads
LLR-266, SR-222 and TC-264 whole. Observations 1 and 2 belong in its reading.
They are not a new row.

1. `LLR-266.detail` still carries two receipts that item 4 did not name.
   - "a plain adapter that changes nothing, so a stand-in agent is
     accounted as before". This is the same time-relative class as TC-262's
     "read as before" (item 8) and LLR-270's "today's" (item 11), and it
     echoes `PlainAdapter`'s docstring ("accounted exactly as before").
   - "codex gets --json beside the --output-last-message temp file it
     already carried". This is a receipt, and it is also not accurate at
     HEAD: `CodexAdapter.prepare` adds both flags
     (`_codex_lastmsg_setup(_ensure(argv, "--json"))`), and no codex
     `cmd_template` in `docs/agents.toml` carries `-o`. The IF-245
     docstring states it correctly: "codex `--json` and an
     `--output-last-message` temp file".
   The Deliverable's line "LLR-266 to LLR-270: each detail and rationale
   carries no history or receipt" is therefore an overstatement for this
   one cell. Suggested standing wording: "a stand-in agent's claude-shaped
   result is read the claude way with no provider named"; "codex gets
   --json and an --output-last-message temp file". The flip check does not
   catch either phrase, because trace.py's frame detector reads citation
   frames, not receipts.
2. `TC-264.method` claims that "each adapter's usage record carries the
   pinned revision". The evidence asserts `semconv` only for claude
   (`test_session_service.py:61` and `:252`). For codex and opencode,
   `test_every_provider_row_carries_the_same_columns` checks the key set,
   not the value. The row offered the fix as optional and the builder did
   not take it, so this is not a gap in WI-720. It is the TC-268 class of
   mismatch, though (the row claims more than its evidence asserts), and
   WI-724 should weigh it. The one-line fix is to assert
   `usage["semconv"].endswith("@" + PINNED)` in the codex and opencode usage
   tests.
3. SR-222's "gen_ai.provider.name filled where the runner reports one" uses
   the row's own phrase. Strictly, no runner reports its provider: claude's
   and codex's adapters name it as a class constant, and opencode's
   (a gateway) names none. The cell is true in effect. A tighter reading
   is "where the runner's adapter names one". This is for the adjudicator's
   judgement, not a defect.
4. The count "Fourteen cells across ten Drafted rows", used in both the
   row's Context and the Deliverable, is thirteen registry cells across nine
   rows plus TC-268's evidence test and the docstring sentence (`--numstat`
   7 + 4 + 2 cell lines). WI-724 correctly lists nine rows. This is
   accounting on an archived surface, not a scope gap.
5. Other history in code comments, outside this row's scope, for a later
   docstring pass: the `session_adapters.py` module docstring ("the codex
   route threw its usage away on every successful call") and
   `_claude_usage`'s "(the old reader looked for a `reasoning_tokens`
   field ...)".

Eleven items checked: eleven met, with item 4 met as asked but leaving
residue in the same cell, and item 9's optional part not taken. The OUT OF
SCOPE list held on every clause. The flip check showed no requirement-form
finding, and the session modules ran 103 passed. What shipped answers the
row. The two observations for WI-724 are refinements the adjudication that
already owns these cells can take or return; neither needs a successor row.

VERDICT: CONFIRMED
