# WI-961 implementation plan, revision 2: Claude transcripts are recorded once per invocation in the usage record

Spec: `docs/work/active/wi-961/WI-961-subagent-usage-ingest.md` (specref: the
review-churn README, item 8, proposal steps 2 and 3, under owner ruling 8).
Item SR: SR-222. Planner: a fresh session that only read; it did not write
revision 1. Lane worktree: `C:/Projects/ai-template.wt/wi-961` (tip
`56d8a1ea1`, which holds revision 1 and critique 1).

## What this revision changes

- **F1, the in-flight message.** Revision 1 let the cursor pass a message
  whose records were still growing. Now a message is counted only once it is
  final (decision 2). A message that is not yet final is left for a later
  ingest and named. Each close-out also re-ingests the session the replaced
  handoff names, so that later ingest happens on the cycle's own route
  (decision 13).
- **F2, the name collision.** Revision 1 named a log by the second of its
  last message, and refused a second contribution that landed on the same
  name. Now the stamp moves one second past any stamp the invocation's
  earlier logs already hold (decision 4). The true times stay in
  `started-at` and `ended-at`.
- **A source limit, found while checking F1.** 9.2% of sub-agent messages
  never get a final record, so the transcript under-states their output.
  Such a log is now marked `usage-status partial` instead of `known`.
- **A consumer revision 1 missed.** The resume carrier in
  `scripts/coordinator/codex_call.py` reads every call log in a lane. The
  D6 test now covers it.
- **One test dropped.** Revision 1's same-name refusal and its test are
  gone: decision 4 means no ingest can reach an existing name.

## The critique's findings, judged

Both findings were treated as claims and checked against the code and the
box's transcripts (read-only, 2026-10-22, Claude Code 2.1.296). Both are
confirmed.

- **F1 [MAJOR]: confirmed.**
  - **Records grow after the cursor can pass them.** A message's records are
    written one per content block. In 186,272 assistant records on the box,
    `output_tokens` grows across a message's records, while input and cache
    counts never differ between them. The planner read the tail of its own
    live transcript while a Bash call ran. The message issuing the call had a
    `thinking` record (8 output tokens, no stop reason) and a later
    `tool_use` record (519 output tokens, `stop_reason` `tool_use`).
  - **Sub-agents often run a tool before the final record.** In sub-agent
    transcripts, 5,264 messages have a `user` (tool-result) record between
    their own records, and output changes after that `user` record in 5,024
    of them. So a running agent's current message can be read half-written.
  - **Revision 1 could not recover it.** Its cursor took the last message
    "as its records stand", and a later ingest reads only past the cursor.
    The earlier part of a message the cursor had passed was never counted
    again. D4's "summed equals the usage over every unique message id" failed
    for any read made while an agent was writing.
  - **Resolution: rows P0, P2, P3, P5, P6 and P8** (decisions 2, 5, 9, 10
    and 13).
- **F2 [MAJOR]: confirmed.**
  - `write_session_log` names a log `<session>-<stamp>.log` and writes it
    with `write_text`.
  - Revision 1 took the stamp from the last message's second and refused an
    existing name. Two contributions of one invocation whose last messages
    share a second would collide. That stamp never changes, so the second
    contribution would be refused on every retry.
  - It is rare, since the two last messages must be written within one
    second either side of an ingest. But it is a permanent wedge, it is
    reachable in a test fixture, and it is cheap to remove.
  - **Resolution: rows P2 and P5** (decision 4).

## What the code and the box hold today (read, not assumed)

**The code.**

- **`session_adapters.py`** holds the IF-245 surface.
  - It imports no kit sibling and measures 448 SLOC
    (`check_complexity.module_sloc`).
  - The one usage builder is `usage_record` (LLR-268): inclusive input,
    derived fresh input, and `""` for an unreported count. Its `usage-scope`
    is the caller's `scope`, else `unknown`.
  - `ClaudeAdapter`'s provider is `anthropic`.
- **`session_service.record(outcome, meta, report=)`** writes one log from
  the caller's row, overlaid by `outcome.metrics`. Its transcript section is
  `outcome.stream`. Where the log goes is derived from the root:
  - a claimed lane: the log is written to `docs/iteration/` and committed;
  - any other root: it goes to `spool_dir(root)` (the primary checkout's
    `out/sessions/spool/`; for a root outside any checkout,
    `<root>/out/sessions/spool/`) and nothing is committed.
- **The standard call-log name.** `CALL_LOG_RE`
  (`^call_[0-9a-f]{32}-(?P<stamp>\d{8}-\d{6})\.log$`) and `is_call_log`
  define it. WI-960's `codex_call.py` treats a commit that only adds such
  logs as no edit, so a derived invocation id must be 32 hex digits or a
  lane ingest would read as an edit.
- **`session_service.py` measures 999 SLOC.**
  `tests/test_module_size_ratchet.py` `THRESHOLD` is 1000, so this plan adds
  no code to it.
- **`agent_common` (at its ratchet baseline, 1110 SLOC).**
  - `write_session_log` writes a fixed tuple of header keys, every key on
    every log, an empty one as `# key:`. It names the file
    `<session>-<stamp>.log` (a `train` prefix only when one is set) and
    overwrites a log of the same name without warning.
  - `log_meta_text` reads a header and says whether the `# ---` terminator
    was reached.
  - `phase_draw_ordinal` skips `call_` names.
  - `worktree_records` is the one `git worktree list` walk.
- **The readers of these logs** (the spec's Trust list, plus one it does not
  name).
  - `kitlib.verdict.SESSION_LOG_RE` never matches a `call_` name.
  - `agent_brief.last_build_family` reads `# phase:` and takes only `BUILD`
    or empty; `_call_row` writes the role into `phase`.
  - **Not in the spec's list:** `codex_call.resume_carrier` walks a lane's
    call logs newest stamp first. It refuses the turn on a log whose header
    is unterminated or lacks `role`, `roster-row`, `wi` or `started-at`. A
    well-formed log whose `role` is not `AUTHOR` reads as "other" and is
    skipped. An ingested log carries every header key, so it is skipped. It
    can be stamped newer than the lane's AUTHOR log, so the D6 test pins the
    skip.
- **TC-265's structural guard** (`tests/test_session_service.py`):
  - only `session_service.py` calls `write_session_log`;
  - only `agent_common.py` holds the header literal `agent session log`;
  - no function whose string constants name `iteration` calls `write`,
    `write_text`, `write_bytes` or `open(..., "w"/"a")`;
  - only `session_service.py` and `agent_session.py` launch a provider
    runner.
- **The two usage columns.**
  - `usage-source` takes `reported` or `unknown`, and `usage-scope` takes
    `invocation`, `thread` or `unknown`. No script reads either.
  - `usage-status` takes `known` (input and output both reported),
    `partial` (some counts reported) or `unavailable` (LLR-269). No script
    reads it either.
- **The blackout hook.** `coordinator_guard.model_clis` matches a command
  word against the `docs/agents.toml` runners. The command's word is the
  Python interpreter, so the window does not deny it.

**The box's transcripts.** Revision 1's survey, re-checked where this plan
relies on it, and extended on 2026-10-22 over every ambient project
directory (Claude Code 2.1.276 to 2.1.306; 1,271 transcripts; no model
call).

- **Record types.**
  - Main transcripts in this repository's slugs carry 20 record types:
    `queue-operation`, `user`, `attachment`, `file-history-snapshot`,
    `atis-latch`, `last-prompt`, `ai-title`, `assistant`,
    `file-history-delta`, `system`, `cost-state`, `mode`, `bridge-session`,
    `api-request-shape`, `api-request-blob`, `api-request`,
    `artifact-comment-monitor`, `artifact-autoreact-ledger`, `frame-link`
    and `custom-title`.
  - Sub-agent transcripts carry 6: `user`, `attachment`, `assistant`,
    `api-request-shape`, `api-request-blob` and `api-request`. The
    `api-request*` records carry request parameters and digests, never
    response usage.
- **What every assistant record has.**
  - `message.id`, `message.model`, an ISO-Z `timestamp`, and the four
    integer counts: `input_tokens`, `cache_read_input_tokens`,
    `cache_creation_input_tokens` and `output_tokens`.
  - A `message.stop_reason` key, null or a string, on every one of 186,272
    records.
  - In a main transcript, `isSidechain: false` and no `agentId`. In a
    sub-agent's, `isSidechain: true` and an `agentId` equal to its file's.
  - No record carries another session's `sessionId`.
- **Only `assistant` records are usage sources.** `usage` also appears in
  `user` records (the parent's tool-result summaries, at
  `toolUseResult.usage`) and in `attachment` records (at
  `attachment.usage`). Neither is ever read.
- **Finality, the facts decision 2 rests on.**
  - **A stop record does not change.** Once a record of a message carries a
    stop reason, no later record of that message differs in any count: 0
    exceptions in 90,324 messages. That record already carries the
    message's largest output count.
  - **Messages never interleave.** No assistant message's records
    interleave with another assistant message's (0 cases). `user` records
    do sit between a message's own records in 7,605 messages (streaming tool
    execution). So a following tool result does not show a message is
    finished. A following assistant message does.
  - **Input and cache counts never change within a message.** Only
    `output_tokens` grows. `output_tokens_details.thinking_tokens` appears
    only on stop records.
  - **Some messages never get a stop record.** That is 5,556 of 60,553
    sub-agent messages (9.2%, in every version surveyed) and 1 of 29,805 main
    ones. Their last record is an early one, recording 10 output tokens on
    average, so the transcript under-states their output. They hold 11% of
    sub-agent input.
  - **Some agents end on an open message.** 93 of 1,070 sub-agent
    transcripts end on a message with no stop record: 88 followed by a tool
    result and nothing more, 5 by nothing. These are agents stopped mid-tool.
    Those messages hold 0.17% of sub-agent input.
  - **Message ids stay in one file.** Of 98,875 message ids, 47 sit in two
    files. All 47 are the one desktop scratch session held in two project
    directories. No message id was copied into another session's file.
- **Repeated records.** "Once per message id" must take each message's
  **last** record. The first record under-counts: leg 3's builders read
  65,107 output tokens by the first record against 564,463 by the last.
- **Two outside checks confirm the last-record rule** (revision 1's
  witnesses).
  - Nine adjudications ran ambient and were recorded by the service (for
    example `call_0dca566165df4b72bc02e5c1a6c2b46a`). Each one's result
    `usage` equals, exactly, the last-record sum over its main transcript's
    unique message ids.
  - Their `modelUsage` also lists a background haiku model (18 to 383 output
    tokens) that no transcript holds.
  - The plan's leg 3 is session `4a3bd3cb-802b-4914-bf20-2ea3b5f2ad23`
    (2026-10-11: nine `kit-builder` agents and one `Plan`). Under the
    last-record rule it reproduces the plan's figures exactly:
    - the coordinator: 156 messages, 151,014 output and 33,486,394 cache
      read;
    - the builders: 585 messages and 564,463 output;
    - Plan: 47 messages and 51,313 output.
- **Metas.**
  - Every meta carries `agentType`, `description`, `toolUseId`,
    `spawnDepth`, `requestShape` and `requestNonInteractive`. Some carry
    `model`.
  - `spawnDepth` is 1 or 2. `parentAgentId` appears exactly on the
    depth-2 metas, and every one resolves.
  - 862 of 1,038 Agent tool results the parents hold are `async_launched`.
    So a parent's tool result does not mark an agent as finished.
- **Shapes outside the spec's layout exist on this box**, in another
  project:
  - one sub-agent transcript with no meta;
  - a `subagents/workflows/wf_*/` directory of Workflow-tool agents;
  - one session id held in two project directories.
- **Fixture candidates for D2.**
  - Session `d628449b…`: its depth-1 agent `a1e796bd…` has exactly two
    depth-2 children.
  - Sessions `5b1f7546…` and `9c7d73b2…` are alternatives.
- **The environment.**
  - `CLAUDE_CODE_SESSION_ID` is set in a sub-agent's shell to its parent
    session's id. The planner checked it in its own shell.
  - `CLAUDE_CONFIG_DIR` is unset, so the ambient home is `~/.claude`.

## Decisions this plan takes (for the coordinator to confirm at the claim's records)

1. **Where the code goes.**
   - **The reader** goes in `session_adapters` (Deliverable 1), as module
     functions beside the claude adapter. It is the only code that knows the
     transcript shape, and the module still imports no kit sibling.
   - **The command** is a new shipped module,
     `project-trajectory/scripts/usage_ingest.py`. It holds:
     - the exactly-once read;
     - the double-count skip;
     - the composition of each log;
     - the call to `session_service.record`.

     It is not placed in `session_service`, which sits at 999 SLOC against
     the 1000 threshold. A command is its own CLI anyway, like
     `coordinator_adjudicate.py`.
   - **The new header columns** go in `agent_common.write_session_log`.
2. **The counting rule and the finality boundary (F1).**
   - **Where usage is read.** Usage is read only from `assistant` records'
     `message.usage`. Messages are ordered by first appearance, and each
     message id is counted once, from its last record in file order.
   - **Final or open.** A message is final when either holds:
     - one of its records carries a non-null `stop_reason`;
     - a record of a later assistant message follows it.

     Only a transcript's last message can be neither. It is open: not
     counted, never passed by a cursor, and named by the reader. A later
     ingest counts it once it is final. A final message's counts cannot
     change (the survey above), so a counted message never needs
     re-counting.
   - **Final without a stop record.** Such a message is counted at its last
     record. Its output count is a lower bound, because the transcript
     states no other. The log marks this through `usage-status` (decision
     9) and names the number of such messages in its body.
   - **`transcript_usage(messages)`** maps a run of counted messages to the
     usage record through `usage_record`, LLR-268's one builder:
     - `fresh` is the sum of `input_tokens`;
     - cache read and cache write are the sums of
       `cache_read_input_tokens` and `cache_creation_input_tokens`;
     - output is the sum of `output_tokens`;
     - reasoning is the sum of `output_tokens_details.thinking_tokens` when
       every counted message's stop record reports it, else `""`. A partial
       sum is never shown as a count.
     - `cli` is `claude` and the provider name `anthropic`.
   - **The model** is that of the last counted message whose model is not
     `<synthetic>`.
3. **Identity.**
   - **An invocation is one transcript:**
     - the session's own: agent id `""`, depth 0, agent type `""`;
     - one sub-agent's: its agent id, and its meta's `spawnDepth`,
       `agentType` and `parentAgentId`.
   - **`invocation-id`** is `uuid.uuid5(<a fixed namespace constant in the
     command>, "<session id>/<agent id>").hex`. That is 32 hex digits,
     deterministic, never `uuid4`, and `is_call_log` accepts the name it
     gives.
   - **The role** is `COORDINATOR` for the session's own transcript and
     `SUBAGENT` for a sub-agent at any depth. `phase` takes the same value,
     as `_call_row` does.
4. **The contribution and its name (F2).** A log records one contribution:
   - `message-count`, the number of unique message ids it counted;
   - `message-cursor`, the last message id counted, always a final one;
   - `contribution-key`, `<invocation-id>:<first message id>:<last message
     id>`, immutable once written;
   - `started-at` and `ended-at`, the first and last counted messages'
     transcript `timestamp` values, verbatim;
   - `date`, the last counted message's time in `_call_row`'s local form;
   - `stamp`, the name's `YYYYmmdd-HHMMSS`:
     - normally, the last counted message's local time;
     - when an earlier log of the same invocation already holds that stamp
       or a later one, **one second after the latest stamp those logs
       hold**.

   The exactly-once read (decision 5) already lists every log of the
   invocation by name, and the directory `record` writes to is always one it
   reads. So the stamp is known before the write. Names therefore stay
   inside `CALL_LOG_RE`, rise strictly within an invocation and never
   collide. Two invocations cannot share a name, because their hex differs.
   No same-name refusal is kept: only a concurrent ingest could reach an
   existing name, and that is outside the promise (see Bounds).
5. **What exactly-once reads.**
   - **Which logs.** It reads the logs already recorded for this
     invocation, found by **name** (`call_<invocation-id>-*.log`, so no
     header is read to decide what belongs) in:
     - `session_service.spool_dir(root)`;
     - the root's own `docs/iteration/`;
     - the `docs/iteration/` of every worktree `git worktree list` names
       (`agent_common.worktree_records`).

     Logs are de-duplicated by file name.
   - **The cursor.** Each log's header is read with
     `agent_common.log_meta_text`. The new contribution is the **final**
     messages after the furthest recorded cursor, in the transcript's order.
     The latest stamp among the logs feeds decision 4.
   - **Refusals.** The command refuses that invocation (exit 1, naming the
     log) when:
     - a header is unterminated or unreadable;
     - a header lacks `message-cursor` or `contribution-key`;
     - a cursor is not in the transcript.

     The reason: re-counting or skipping would break exactly-once (Trust).
   - **Nothing new to record.** When no final message follows the cursor,
     nothing is recorded and the command prints `unchanged`, plus `open` for
     an open last message.
   - **Where the function lives.** The read sits in its own function, which
     holds no `write` call (the TC-265 guard).
6. **No double count (D5).**
   - **When a session counts as service-recorded.** Any log in the set
     above (all names, header read) carries its `session-id` with a
     `usage-source` other than `transcript`. Its main transcript is then
     skipped and named.
   - **Its sub-agents** are skipped when, and only when,
     `session_adapters.CLAUDE_RESULT_COUNTS_SUBAGENTS` is true. That
     constant is set from P0's probe B, and its docstring cites the decision
     id.
   - **An unreadable log in that set** refuses what the skip governs: the
     main transcript, and the sub-agents too when the constant is true.
     Such a log may be the service's record of this session.
7. **The closed shape (S3).** `TRANSCRIPT_TYPES` is the allow-set of record
   types, fixed from P0's survey.
   - **Every record** must be one JSON object whose `type` is in the set.
   - **An `assistant` record also needs:**
     - `message.id`, `message.model` and `timestamp` as strings;
     - a `message.stop_reason` key, null or a string;
     - `message.usage` with the four integer counts;
     - `sessionId` equal to the session;
     - in a main transcript, `isSidechain` false and no `agentId`;
     - in a sub-agent's, `isSidechain` true and `agentId` equal to its
       file's.
   - **A meta needs** `agentType` (a string) and `spawnDepth` (an integer of
     1 or more, not a bool). It needs `parentAgentId` when `spawnDepth` is 2
     or more. Other meta keys are ignored.
   - **Any `spawnDepth` value** is accepted and recorded. A parent that names
     no agent in the directory is recorded as written and printed as
     `parent unresolved`.
   - **What is refused, per transcript, naming the file and the field:**
     - a torn or non-JSON line;
     - a missing meta;
     - any entry under `subagents/` other than an `agent-<id>.jsonl` and
       `agent-<id>.meta.json` pair, the Workflow layout included.

     Nothing is recorded for that transcript. The others are recorded, and
     the exit is 1.
8. **The home and the session.**
   - **The home** is `CLAUDE_CONFIG_DIR` when the command's environment sets
     it, else `~/.claude`: the home Claude Code itself uses there. The
     command never selects an account home (LLR-336 and the spec's bound).
   - **The session** is `--session ID`, else `CLAUDE_CODE_SESSION_ID`. With
     neither, the command exits 2.
   - **Locating it.** The session is found as `<home>/projects/*/<id>.jsonl`
     and `<home>/projects/*/<id>/`:
     - two project directories holding it: refused, both paths named;
     - neither: named absent, exit 1;
     - a missing main transcript beside a present `subagents/`: the main is
       named absent and the sub-agents are read.
9. **What a log holds.** The row the command composes carries:
   - `session` `call_<invocation-id>`, and `stamp` and `date` from decision
     4;
   - `phase` and `role`;
   - `outcome` `INGESTED`;
   - `model`, the response model;
   - `gen_ai.request.model`, the meta's `model` when present, else `""`;
   - `session-id` and `gen_ai.conversation.id`, the session id;
   - the usage record from decision 2;
   - `usage-source` `transcript` and `usage-scope` `contribution`;
   - `usage-status`, using LLR-269's existing values:
     - `known` when every counted message is final by its stop record;
     - `partial` when any was counted without one, so its output is a lower
       bound.

     The closed shape guarantees that the input and output counts are
     present, so `unavailable` cannot arise.
   - the identity columns (`agent-id`, `parent-agent-id`, `spawn-depth`,
     `agent-type`);
   - the contribution columns from decision 4.

   Provider, tier, roster row, cost, wall time, occupancy, train,
   `session-mode` and `raw-usage` stay `""`.
   - **Why `raw-usage` stays empty.** One verbatim usage object per message
     would put megabytes on one tracked header line. The transcript is the
     raw source. The recorded range lets a mapping later found wrong be
     re-derived from it, while Claude Code keeps it.
   - **The body** is a fixed usage summary built only from counts, message
     ids and timestamps. It includes how many messages were counted without
     a stop record. It never holds a prompt, an output, a tool input or
     result, a meta `description`, or any other transcript text.
10. **The command line and its results.** The command is
    `usage_ingest.py [--session ID] [--root DIR]`. It prints one stdout line
    per invocation, each naming the role, agent type and agent id. The line
    is one of:
    - `recorded`: message count, input and output totals, `known` or
      `partial`, the path, and spooled, committed or commit refused;
    - `unchanged`;
    - `open <message id>`: the transcript's last message, left for a later
      ingest; it can follow `recorded` or `unchanged`;
    - `skipped`, with the service log;
    - `refused <file>: <field>`;
    - `absent`;
    - `parent unresolved`.

    | Exit | When |
    |---|---|
    | 0 | nothing was refused or absent and no commit was refused (an `open` line does not change the exit) |
    | 1 | a refusal, an absent transcript or a refused record commit |
    | 2 | no session |

    `print` is the only output (the TC-265 guard).
11. **Fixtures.** Fixtures are cut from real transcripts by a throwaway
    script kept in the scratch root, not the repository. The cut:
    - keeps every record's `type`, `uuid`, `parentUuid`, `isSidechain`,
      `sessionId`, `agentId`, `timestamp` and `requestId`;
    - keeps each assistant record's `message.id`, `message.model`,
      `message.usage` and `stop_reason`, and only the `type` of each content
      block;
    - keeps the numbers of a parent's tool-result summary
      (`user.toolUseResult.usage`) and of an `attachment.attachment.usage`
      object, the two places `usage` appears outside `assistant` records;
    - keeps the meta keys other than `description`;
    - removes all text, tool inputs and outputs, `cwd` and `gitBranch`;
    - puts the slug at a neutral `projects/work/`.

    Each transcript is cut to a bounded prefix **ending on a final
    message's stop record**, so the fixture stays under about 200 KB and
    passes `check_privacy`. At least one sub-agent fixture keeps a message
    with no stop record that a later message follows. Open tails are made in
    tmp copies by the tests, never in the committed fixture. The fixtures
    live in `tests/golden/sessions/claude-transcripts/`, and the test
    module's docstring states their provenance, as
    `test_session_adapters.py` does.
12. **The live run (D10)** ingests leg 3's own session into a scratch root:
    an empty directory outside every checkout. `record` then spools into
    `<scratch>/out/sessions/spool/`, and this repository's spool and records
    stay untouched until the landed code runs. The comparison is against:
    - the plan's leg-3 figures;
    - an independent count over the same transcripts: once per message id,
      last record, with the first-record figure shown beside it to name the
      difference.

    Claude Code's default 30-day clean-up removes the leg-3 transcripts
    around 2026-11-10. If they are gone, the leg's own coordinator session
    stands in, by the same method.
13. **The tail after a close-out is picked up by the next one (F1).** A
    session's last ingest cannot see what the session writes after it: its
    closing reply, and an open message of an agent still running. The cycle
    text closes that gap:
    - a close-out's handoff names its own session id;
    - the next close-out runs the command for its own session, and again
      with `--session <id>` for the session the replaced handoff names.

    Exactly-once makes the second run record only that session's tail, or
    nothing. The open messages decision 2 leaves behind are recorded there,
    once they are final.

## The architectural-delta question

Yes on all four counts, all within this item's scope:

- **A new input.** The usage record now depends on Claude Code's transcript
  files.
- **New domain values.**
  - role `SUBAGENT` and `COORDINATOR`;
  - `usage-source` `transcript`;
  - `usage-scope` `contribution`;
  - `outcome` `INGESTED`.

  Revision 2 adds no domain value. The finality rule is internal to the
  reader. `usage-status partial` is LLR-269's existing value, and `open` is
  a stdout word in the command's own CLI row.
- **New state in an existing carrier.** The cursor, count and contribution
  key are session-log columns: no new carrier, as Deliverable 2 says. The
  stamp rule reads only names the exactly-once read already lists.
- **A new boundary.** The kit reads a third party's files under the user's
  Claude home. IF-245's notes say today that the module touches only the
  codex temp file and rollout.

The rows below carry each change:

| Change | Row |
|---|---|
| IF-245's data, requestors and notes | P1 and P7 |
| the command's own CLI row | proposed at P1 |
| IF-246's and IF-065's requestors | P1 and P7 |
| the reader, with its finality rule | P3 |
| the header columns | P4 |
| the command, with its stamp rule | P5 |
| the cycle text, with the previous-session ingest | P6 |

No refactor this item does not own is needed. The service's SLOC ceiling is
met by placement (the command's own module), not by splitting the service.
WI-800's ledger is not needed, because the contribution key travels in the
log.

DELTA: within

## Steps

| Plan-WI | Title | Covers | Interfaces | Predecessors |
|---|---|---|---|---|
| P0 | Probes, before any coverage claim: the three unverified facts (A: a `--resume` and a `SendMessage` to a finished agent, append or new file; B: does a `claude -p --output-format json` result's usage include its sub-agents, and does a `-p` session's shell see `CLAUDE_CODE_SESSION_ID`; C: can a depth-3 agent exist), probe E (a running main session's message carries its stop record when its own Bash call runs), and survey D (the record-type allow-set, meta fields, the last-record rule and the finality facts, re-run over the box). Each is recorded in `docs/decisions/wi-961.toml` with its command, the Claude Code version and what settled it. A resume found writing earlier message ids into a second file stops the lane: a spec amendment judged by one confirming critique before P1, or a partial close | D8; F1; SR-222 | no interface: probes from a scratch directory and a decisions record, no code seam crossed | |
| P1 | Spine intent turn, TC-first (Terra through `scripts/coordinator/codex_call.py`): the derived SR under SN-026, performance lens, in capability voice; its LLR (the closed shape and its refusal, the last-record rule and the finality boundary, identity, contribution, cursor and name stamp, the exactly-once read set, the double-count skip, `usage-status`, the new values); one TC per arm, each naming the tests P2 adds; IF-245 amended (data, requestors, notes); IF-246 and IF-065 requestors gain the command; the command's CLI row | D8; D11; F1; F2; SR-222 | IF-245; IF-246; IF-065; Proposed: the ingest command's own CLI row (owner the new command, requestor the coordinator); nearest existing IF-283, the adjudication command's CLI, which is another command's argv | P0 |
| P2 | Test commit, alone before the code: the cut fixtures and their helper; every test below as a strict expected failure; stubs so each red reaches its own assertion (checked with `--runxfail` and recorded); the manifest entry for the stub command; the RESYNC entry anchored at the lane base; the `SLOW_MODULES` entry with its in-process pin | D1; D2; D3; D4; D5; D6; D7; D9; F1; F2; SR-222 | IF-245; IF-246; IF-065 | P1 |
| P3 | `session_adapters.py`: the reader (`TranscriptRefused`, `TRANSCRIPT_TYPES`, `claude_session` with final and open messages, `transcript_usage`, `CLAUDE_RESULT_COUNTS_SUBAGENTS`) and the IF-245 contract body; `adapter_for` and the usage builder untouched | D2; D3; D7; F1; SR-222; TC-262; TC-264 | IF-245 | P2 |
| P4 | `agent_common.write_session_log`: seven header columns (`agent-id`, `parent-agent-id`, `spawn-depth`, `agent-type`, `message-count`, `message-cursor`, `contribution-key`); the module-size ratchet re-stamped with its reason | D4; D6; SR-222; TC-265 | IF-065 | P2 |
| P5 | `usage_ingest.py`: locate and read; the exactly-once read, the cursor over final messages and the latest stamp; the name stamp; the double-count skip; compose (with `usage-status` known or partial) and record through `session_service.record`; report lines including `open`, and exit codes; its contract docstring | D3; D4; D5; D6; D7; F1; F2; SR-222; TC-265 | IF-245; IF-246; IF-065; Proposed: the ingest command's own CLI row; nearest existing IF-283, which is another command's argv | P3; P4 |
| P6 | Text: coordinator-cycle §6 (close-out) and §7 (headless leg) run the command for this session and for the session the replaced handoff names, and the handoff names its own session id; the three copies synced; `docs/runtime-flows.md` gains Flow 8 | D9; F1; SR-222 | no interface: skill text and the runtime-flow narrative, no code seam crossed | P5 |
| P7 | Records: the LLR's traced cells, `Implements:` lines, the IF rows' final text, regenerated derived files (CLI reference, interface reference, derived components, dashboard), and the smoke budget if its count is crossed | D11; SR-222; TC-262; TC-263; TC-264; TC-265; TC-351; TC-362 | IF-245; IF-246; IF-065 | P6 |
| P8 | Live run (decision 12): leg 3's session into a scratch root, compared with the plan's figures and an independent count; a planted-text check on the real logs; the current leg's session ingested twice, the second run after more messages land, showing an open message recorded once final and the two contributions equal to an independent count over the completed transcript | D10; D7; F1; SR-222 | IF-245; IF-246 | P7 |
| P9 | Landing: the commit bar green; `check_trajectory.py --strict` and `trace.py --strict` clean; the derived SR, the LLR, the new TCs and the IF amendments judged at the lane's sitting; the RESYNC entry re-anchored at the landing's parent; the full suite runs TC-262, TC-263, TC-264, TC-265, TC-351 and TC-362 unchanged | D11; SR-222; TC-262; TC-263; TC-264; TC-265; TC-351; TC-362 | no interface: landing bookkeeping, no code seam crossed | P8 |

The cycle's review rounds run between P7 and P8 on an attested tip. The
checkpoint sitting is P9's.

## Step detail

### P0 — the probes (D8; F1's premise)

The coordinator runs every probe from an empty scratch directory outside
every checkout, so its transcripts land in a scratch project directory. Each
uses `--model haiku`. No probe runs inside the blackout window, where the
guard denies a model CLI.

- **Probe A, resume.**
  - **A1, `--resume`.** Run `claude -p --model haiku --session-id <uuid>
    "Reply with the word one."`, then `claude -p --model haiku --resume
    <uuid> "Reply with the word two."`. Record:
    - the project directory's files before and after;
    - whether `<uuid>.jsonl` grew, with its earlier message ids unchanged
      and new ones appended, or a new session file appeared;
    - whether any message id is in two files.

    The box's history already shows no message id copied across sessions
    (survey above). The probe settles the current version.
  - **A2, `SendMessage`.** In the coordinator session (foreground), spawn
    one sub-agent with a one-line task. After it finishes, `SendMessage` it
    once. Record whether `agent-<id>.jsonl` grew or a new agent file
    appeared, and whether any message id repeats across files.
- **Probe B, the `-p` result.** Run `claude -p --model haiku --output-format
  json` with a prompt that uses the Agent tool once for a one-word reply,
  and whose Bash step prints `$CLAUDE_CODE_SESSION_ID`.
  - Compare the result's `usage` with the main transcript's last-record sum,
    and with that sum plus the sub-agent's. Record which one it equals.
  - The nine service-recorded adjudications above (no sub-agents; the
    result equals the main sum) are the recorded baseline.
  - The finding sets `CLAUDE_RESULT_COUNTS_SUBAGENTS`. The printed id
    settles whether a headless leg's command finds its session without
    `--session`; if it does not, §7's text passes it.
- **Probe C, depth 3.** Prompt a chain: a sub-agent told to start a
  sub-agent, told to start one more. Record either the deepest `spawnDepth`
  among the metas, or that a depth-2 agent has no Agent tool (read from the
  scratch session's own transcript). The reader accepts any depth either
  way. The finding shapes only the derived SR's coverage wording.
- **Probe E, the close-out command's own message.** In the coordinator
  session, run one Bash command that prints the session's main transcript's
  last three assistant records: id, `stop_reason` and output count. Record
  whether the message issuing the call already carries its stop record. The
  planner observed it in its own sub-agent transcript: message
  `msg_011CgJ47VB5vAgKrb57YpakP` had a `tool_use` stop record with 519
  output tokens before its tool ran. Either answer is safe under decision 2.
  It only decides whether that message is recorded at the close-out or by
  the next one (decision 13).
- **Survey D.** Re-run the read-only survey and record its counts and the
  Claude Code version:
  - record types, meta keys and the last-record rule;
  - the stop-reason key on every assistant record, and no count change
    after a stop record;
  - no interleaving between assistant messages, and input and cache counts
    constant within a message;
  - the share of messages without a stop record, and the transcripts ending
    open.

  It fixes `TRANSCRIPT_TYPES`, and confirms decision 2's premises on the
  version the lane lands on.

**The stop rule.** Suppose A1 or A2 shows a resumed session or agent writing
earlier message ids into a second file. Two invocation identities would then
carry the same messages, and the spec's per-invocation cursor would double
count. The lane brings that to the spec as an amendment, judged by one
confirming critique before P1. If the amendment is refused, the lane closes
partial with the conflict drafted as a successor. It does not build around
it. The same applies if survey D finds a count changing after a stop
record, or assistant messages interleaving: decision 2's finality rule would
then not hold.

### P1 — the set Terra authors

- **The derived SR**, in the spec's capability voice. Its acceptance names
  each arm:
  - every session, and every session an agent spawns at the depths P0
    found, is recorded with its identity;
  - usage is counted once per message;
  - a message is recorded once it is complete, never at a count still
    being written;
  - a count the source states only in part is marked so;
  - a repeated, resumed or interrupted recording adds nothing;
  - a session already recorded by the service is not counted twice;
  - an ingested record carries no gate authority;
  - no transcript text is recorded;
  - an unknown shape is refused, naming what is wrong;
  - the published coordinator guidance runs it at close-out and at a
    headless leg's end, and picks up the previous session's tail.
- **The LLR (CMP-008).**
  - Its module cell is `project-trajectory/scripts/session_adapters.py;
    project-trajectory/scripts/usage_ingest.py;
    project-trajectory/scripts/agent_common.py`.
  - Its detail states decisions 2 to 10 in design voice, the finality
    boundary and the name stamp included. It names no code carrier.
- **TCs**, one per arm. Each names its tests in the table below.
- **IF-245.**
  - The data gains the reader's names.
  - The requestors gain `scripts/usage_ingest`.
  - The notes gain: the module also reads the Claude Code transcripts and
    metas of the one session its caller names, under the ambient Claude
    home, and never writes there.
- **IF-246 and IF-065.** Their requestors gain `scripts/usage_ingest`.
  IF-065's data names `log_meta_text` and `worktree_records`, where the seam
  check needs it.
- **The command's CLI row:**
  - owner `scripts/usage_ingest`;
  - requestor `external:coordinator`;
  - channel `cli`;
  - data: the arguments, the home and session rules, the stdout lines
    (`open` included) and the exits of decision 10.
- **Unchanged.** SR-222 and LLR-266 to LLR-269 keep their approved text.

### P2 — the tests (D1)

Every test below is committed first, as a strict expected failure:
`@pytest.mark.xfail(strict=True, raises=(AssertionError,
pytest.fail.Exception))`.

**The stubs.** They make each test reach its own assertion:

- `session_adapters`:
  - `TranscriptRefused`;
  - `claude_session` returning an empty read, with no invocations, no open
    messages and no refusals;
  - `transcript_usage` returning an empty usage record;
  - the constant.
- `usage_ingest.py`:
  - `invocation_id` returning `""`;
  - `main` recording nothing and returning 0.

**The commit also carries:**

- the fixtures and the helper, including tmp-copy builders:
  - cut after a message's first, no-stop-reason record;
  - append a fixture's later records;
  - restamp an appended message into a given second;
- the bootstrap-manifest entry for the new script
  (`kitlib/bootstrap_manifest.py`);
- the RESYNC §4 entry anchored at the lane base: a new adapter reader, a
  new shipped command and seven header columns. The kit-owned files to
  overwrite are `scripts/session_adapters.py`, `scripts/usage_ingest.py`
  and `scripts/agent_common.py`;
- `test_usage_ingest_git` in `SLOW_MODULES`, with `test_usage_ingest`
  (non-git tmp roots) as the family's in-process pin.

The coordinator re-runs the set with `--runxfail` and records in decisions
that each test fails at its own assertion. The tests:

| Test | Clause | Red before the change |
|---|---|---|
| `test_claude_transcripts.py::test_a_session_with_nested_agents_yields_four_invocations_with_their_identities` (session id, agent id, parent, depth 0/1/2/2, agent type, request and response model, first and last timestamps) | D2 | the stub's empty read |
| `test_claude_transcripts.py::test_each_invocation_usage_is_its_unique_message_sum` (literal expected values per invocation; the sub-agent fixture holds a message with no stop record that a later message follows; adequacy witness in the test: over the same fixture, the all-records sum and the first-record sum both differ from the literal) | D2 | empty usage |
| `test_claude_transcripts.py::test_a_repeated_record_adds_nothing` (a verbatim duplicate line and an earlier partial record of a message, added in a tmp copy) | D2 | empty usage |
| `test_claude_transcripts.py::test_the_parents_tool_result_summary_is_never_read` (the cut summary's usage, and a large planted value in it and in an `attachment` record, change no total) | D2 | empty usage |
| `test_claude_transcripts.py::test_the_main_sum_equals_the_clis_own_result` (a cut adjudication transcript beside its recorded result usage line: the four counts equal) | D2 | empty usage |
| `test_claude_transcripts.py::test_an_open_last_message_is_named_and_not_counted` (a tmp copy cut after the first, no-stop-reason record of its last message: the usage excludes it and the reader names its id as open; the same copy with the message's later records restored counts it once, at its stop record's output) | F1; D4 | the stub names no open message |
| `test_claude_transcripts.py::test_a_message_without_a_stop_record_is_final_once_a_later_message_follows` (counted at its last record, and reported as counted without a stop record; the same message as the transcript's last is open) | F1; D2 | empty read |
| `test_claude_transcripts.py::test_an_unknown_shape_is_refused_naming_file_and_field`, parametrized (see the list below) | D3 | the stub never refuses |
| `test_claude_transcripts.py::test_a_depth_two_agent_whose_parent_is_absent_is_kept_and_named_unresolved` | D3 | empty read |
| `test_claude_transcripts.py::test_any_spawn_depth_is_accepted_and_recorded` (a depth-3 meta) | D2 | empty read |
| `test_claude_transcripts.py::test_a_session_held_in_two_project_directories_is_refused_naming_both` | D3 | empty read |
| `test_usage_ingest.py::test_one_ingest_records_four_logs_with_the_usage_vocabulary` (non-git tmp root, so it spools; checks `cli`, `semconv`, provider name, inclusive input, fresh input, `usage-source transcript`, `usage-scope contribution`, `usage-status` known for the main log and partial for the sub-agent holding the no-stop message, roles, `phase`, `outcome`, empty `raw-usage`, and the identity and contribution columns; every name passes `is_call_log`) | D2; D4 | no log written |
| `test_usage_ingest.py::test_the_invocation_id_is_derived_from_the_transcript_identity` (deterministic, 32 hex, distinct per agent) | D4 | `""` |
| `test_usage_ingest.py::test_ingesting_one_session_twice_records_nothing_the_second_time` | D4 | no first log |
| `test_usage_ingest.py::test_appended_messages_are_recorded_alone_under_the_same_identity` | D4 | no log |
| `test_usage_ingest.py::test_initial_resumed_and_repeated_ingests_give_two_contributions_summing_to_the_whole` | D4 | no log |
| `test_usage_ingest.py::test_an_open_message_is_recorded_once_final_and_the_contributions_equal_the_completed_transcript` (first ingest on a tmp copy cut after the first, no-stop-reason record of a sub-agent's last message: it prints `open` for that message and records the rest; then the message's later records and further messages are appended, the second ingest runs, then a third. Assert: the second log counts the once-open message at its final output; the two logs' four counts sum to the last-record sum over every unique message id of the completed transcript; their contribution keys differ; the third ingest records nothing) | F1; D4 | no log |
| `test_usage_ingest.py::test_two_contributions_whose_last_messages_share_a_second_both_survive` (the appended range's last message restamped into the same second as the first contribution's last: two logs under one invocation, the second's name stamp one second after the first's, each header's `ended-at` its own message's transcript time, both cursors present; a third ingest records nothing) | F2; D4 | no log |
| `test_usage_ingest.py::test_a_run_killed_after_some_logs_then_rerun_records_each_invocation_once` (`record` raises KeyboardInterrupt on its third call) | D4 | no log |
| `test_usage_ingest.py::test_a_torn_earlier_log_refuses_that_invocation_naming_it` (no `# ---`), and `..._a_cursor_missing_from_the_transcript_refuses` | D4 | exit 0, nothing named |
| `test_usage_ingest.py::test_an_unknown_shape_exits_nonzero_and_records_nothing_for_that_transcript` (one bad sub-agent; the other three recorded) | D3 | exit 0 |
| `test_usage_ingest.py::test_a_service_recorded_session_skips_its_main_transcript` (both arms of the constant; a `transcript`-sourced log carrying the id skips nothing) | D5 | main recorded or nothing written |
| `test_usage_ingest.py::test_no_transcript_text_reaches_any_written_log` (a planted string in user, assistant text, thinking, tool input, `api-request-blob` and meta `description`: 0 occurrences in every log) | D7 | no log written, so the count assertion's precondition (four logs) fails |
| `test_usage_ingest.py::test_no_session_is_a_usage_error` (exit 2) and `..._an_absent_transcript_is_named` (exit 1) | D3 | exit 0 |
| `test_usage_ingest_git.py::test_an_ingested_log_in_a_lane_is_no_round_no_build_and_no_draw` (`conftest.claimed_lane`; the logs commit there; a round file present: `logged_rounds` reads none, while the same setup with a REVIEW gate log reads one; `last_build_family` returns the planted BUILD log's family, though the reverse name order visits the ingested log first; `phase_draw_ordinal` is 0 for SUBAGENT and COORDINATOR and unchanged for BUILD; `codex_call.resume_carrier` over the lane's call logs returns the planted AUTHOR log's carrier, though the ingested log's stamp is newer) | D6 | no log committed, so the precondition fails |
| `test_usage_ingest_git.py::test_a_log_in_another_worktree_counts_toward_exactly_once` | D4 | no log |
| `test_usage_ingest_git.py::test_from_the_primary_checkout_the_logs_spool_and_nothing_is_committed` (HEAD and status unchanged) | D4 | no log in the spool |
| `test_prompts.py::test_the_close_out_and_headless_leg_run_the_usage_ingest` (§6 and §7 of all three copies name `usage_ingest.py`, its run with `--session` for the replaced handoff's session, and the handoff naming its own session id; `test_skills_sync` keeps the copies byte-identical) | D9; F1 | the name is absent |

The unknown-shape cases, each naming the file and the field:

- an unknown `type`;
- a missing `type`;
- a non-JSON or torn line;
- an assistant record without `message.id`;
- one without `message.model`;
- one without `timestamp`;
- one without the `message.stop_reason` key;
- one without `message.usage`;
- a usage count that is a string;
- a `sessionId` that is another session's;
- a sub-agent `agentId` that is not its file's;
- a main-transcript assistant record with `isSidechain` true;
- a meta without `spawnDepth`, or with a bool `spawnDepth`;
- a meta without `agentType`;
- a depth-2 meta without `parentAgentId`;
- a transcript without its meta;
- a `subagents/workflows/` directory.

### P3 to P5 — the code

- **P3, the reader.**
  - `claude_session(home, session_id)` returns the session's invocations in
    a fixed order: the main, then agents by depth and id. Each invocation
    carries its final messages in order (id, first and last timestamps, the
    four counts, the thinking count where reported, whether it had a stop
    record) and its open message id or `""`. The result also holds the
    refusals and the absences. It applies decisions 2, 7 and 8.
  - `transcript_usage(messages)` builds the usage record for any run of
    final messages.
  - The IF-245 contract text in the module docstring gains the reader.
  - Function complexity stays under the ratchet, and the module stays far
    from 1000 SLOC.
- **P4, the header.** The seven keys join `write_session_log`'s tuple, and
  `agent_common.py` is re-stamped from 1110 to 1117. The reason: it is not
  decomposable here, since the header's one home is beside its writer, as
  for WI-958's `bar-red`.
- **P5, the command.**
  - It implements decisions 3 to 6, 9 and 10.
  - The exactly-once read, the latest-stamp read and the double-count scan
    sit in one function with no write.
  - It makes one `session_service.record(Outcome(root, 0, "", False,
    <summary>, metrics), row, report=report)` call per contribution, with
    `stamp` from decision 4.
  - Its contract docstring names the CLI row.

### P6 — the text (D9; F1's live route)

- **§6, Close-out.** Before the handoff is written, run from the primary
  checkout:

  ```bash
  "$PY" "$SCRIPTS/usage_ingest.py"
  "$PY" "$SCRIPTS/usage_ingest.py" --session <the replaced handoff's session id>
  ```

  - The first command records this session and its sub-agents into the
    spool. The second records the previous session's tail (decision 13); it
    is skipped when the replaced handoff names no id.
  - The handoff then names this session's id (`$CLAUDE_CODE_SESSION_ID`)
    under its state, with any nonzero exit, which is never hand-patched. The
    lease handback or the relaunch request follows, as today.
- **§7, Headless legs.** A leg runs the same pair as its close-out, before
  it writes its handoff and ends its reply. The commands are not model CLIs,
  so the blackout window does not deny them.
- **Copies.** The three copies are synced.
- **Flow 8** in `docs/runtime-flows.md`, "A usage ingest at close-out",
  cites the derived SR, the LLR, SR-222 and LLR-269.

### P8 — the live run (D10)

Run the lane's copy:

```bash
usage_ingest.py --session 4a3bd3cb-802b-4914-bf20-2ea3b5f2ad23 --root <scratch>
```

Record in decisions:

- per role and agent type, the logs' sums against:
  - the plan's figures (151,014; 33,486,394; 564,463; 51,313);
  - the independent once-per-message count;
- the first-record figure beside them;
- the number of messages counted without a stop record, and any open tail;
- any difference and its cause;
- a grep of every scratch log for a distinctive line of that leg's prompt:
  0 occurrences.

Then run the command on the current leg's session into a second scratch
root while one of its foreground sub-agents is mid-turn, and again after it
and more messages have landed. Record:

- any `open` line from the first run;
- that the second run recorded only later messages, the once-open message
  among them;
- that the two contributions sum to an independent last-record count over
  the completed transcript.

## Bounds and risks, stated and not built

- **New record types refuse.** A Claude Code update that adds a record type
  makes the ingest refuse that transcript until `TRANSCRIPT_TYPES` learns
  it. The refusal names the type, and the addition is a kit change with a
  RESYNC line. This is the closed shape the spec rules (S3, ruling 1).
- **The Workflow-tool layout is refused, not read.** A successor row
  extends the reader if the coordinator adopts Workflows.
- **The transcript under-states some output, and the log says so.** A
  message that never gets its stop record (9.2% of sub-agent messages on
  this box) is counted at an early output count. No other source on disk
  holds its final count: the `api-request*` records carry none. Its log is
  marked `usage-status partial`, and its body gives the number of such
  messages. The plan's leg-3 figures share this limit, since they use the
  same method.
- **An agent stopped mid-tool keeps its last message unrecorded.** Its
  transcript ends on an open message that will never become final: 93 of
  1,070 sub-agent transcripts here, 0.17% of sub-agent input. The message
  is named `open` at every ingest. Recording it would record an output
  count the transcript never completed. Its input and cache counts are
  known, but splitting one message across two contributions would break the
  cursor's one-message unit.
- **Usage no transcript holds.** Background model calls that appear in a
  result's `modelUsage` are absent from every transcript, so they are not
  recorded: 18 to 383 output tokens per session in the nine witnesses.
- **The last session's tail waits for a later run.** The tail after a
  session's last ingest is recorded by the next close-out (decision 13). It
  stays unrecorded until the session is ingested by name when:
  - no later close-out names the session (the last before a gap);
  - a handoff omits its id;
  - Claude Code's 30-day clean-up removes the transcript first.
- **Tampering and concurrency are outside the promise:**
  - a hand-edited transcript;
  - a hand-removed or moved log;
  - two ingests of one session at the same moment (they may write one name
    twice, and the writer overwrites);
  - a transient `git worktree list` failure that hides a log held only in
    another lane.
- **Account homes stay unread.** A session run under an account home (call
  C6) is outside the promise.
- **Cost.** The double-count scan reads every worktree's log headers: 41
  worktrees on this box, with trunk's `docs/iteration/` alone holding 675
  logs. That costs seconds per close-out, and P8 records the measured time.
  The exactly-once read and the stamp read glob by name, so they stay
  cheap. The close-out runs the command twice.

## Observed elsewhere, not changed here

- **`write_session_log` overwrites a same-named log** for every caller. The
  command's stamp rule never hands it an existing name; the writer is
  unchanged.
- **One session id can sit in two project directories** after Claude Code
  moves a desktop session's directory. The command refuses rather than
  chooses.
- **For WI-800's spec, a constraint this lane does not build.** Its harvest
  must leave a harvested log where this command's exactly-once read finds
  it, or teach the read its new home. A log that leaves those directories
  takes its cursor with it. The next ingest would then re-record from the
  invocation's first message under a new contribution key, and the ledger's
  per-key fold would not catch the overlap. The coordinator files this as a
  line on WI-800 at landing.
