+++
id = "WI-961"
title = "Claude coordinator sessions and their sub-agents, nested agents included, are recorded once per invocation from their transcripts, under the usage ledger's invocation key"
workstream = "process"
sr_refs = ["SR-222"]
specref = ""
buildtier = "strong"
safety_class = "ordinary"
priority = 5
planmode = "single"
needs = ["WI-960"]
+++

## Deliverable

Landed by headless leg 14 of loop session `20261021T045653Z-213020`, squashed from lane `wi-961`.

- **The reader.** `session_adapters.claude_session` reads the Claude Code transcripts and metas of the one session its caller names, under the ambient Claude home, in a closed shape (21 main and 6 sub-agent record types): any depth of nesting, each message counted once from its last record, a final message counted partial where it carries no stop record, a transcript's last message left open unless a stop reason, a later message or, for a sub-agent, a finish notice (a task notification, or the spawner's tool result) makes it final, and a malformed transcript refused by file and field while the others stay recordable.
- **The command.** `usage_ingest.py [--session ID] [--root DIR]` records each transcript's not-yet-recorded final messages as one contribution log through `session_service.record` (committed in a claimed lane, spooled elsewhere), under an invocation id derived from the transcript's identity, so a repeated, resumed or interrupted run adds only what no earlier log holds; a session whose main transcript the service already recorded is skipped, its sub-agents still recorded. The logs carry a usage summary only, never transcript text, under roles no gate reads. Its arguments, stdout and exit codes are IF-305, IF-306 and IF-307.
- **Text.** The coordinator-cycle skill's close-out and headless-leg sections run the ingest before each handoff is written, naming the session, and ingest the replaced handoff's session tail (three copies byte-identical); Flow 8 in the runtime flows.
- **Spine.** SR-244 (derived, performance), LLR-347 to LLR-356 and TC-386 to TC-395 approved (act seq 153) by sitting 009 (`docs/reviews/wi-961/009-ADJUDICATE-941a256.md`), after sittings 007 and 008's returns were answered in the lane; IF-305 to IF-307 added and IF-065, IF-245 and IF-246 amended by addition. Reviews: counted rounds 1 and 2 and the gate (`docs/reviews/wi-961/003` to `011`); decisions `docs/decisions/wi-961.toml` D-001 to D-017.
- **Live run.** P8's ingest of leg 3's session reproduced the plan's figures exactly with no prompt text in any log (D-009). Owed after landing: the double-count scan's cost over this repository's worktrees, measured at the first close-out ingest.

## Context

Review-churn item 8, proposal steps 2 and 3, with revision 37's widening:
planners, builders and reviewers may spawn sub-agents, so nested agents are
in scope (queue row P2, second half). This row is split from WI-800. It
takes WI-800's ledger contract (one usage record per invocation, keyed by
invocation id, appended once), not WI-800's store. WI-960 is the first half.

**Size of the gap** (plan item 8, leg 3, counted once per message id):
builders were about 74% of the leg's Claude output, and all sub-agents about
80%. None of it is in the kit's records. The coordinator session itself
(attended, or a headless `claude -p` leg: `overnight_legs.py` launches it
with `--output-format text`, so no result usage is captured) is not recorded
either.

**Where the data is: verified on this box, 2026-10-20** (Claude Code; the
reads are in NOTES):
- A session's transcript is `~/.claude/projects/<cwd slug>/<session
  id>.jsonl`. Attended (`entrypoint` `claude-vscode`) and headless
  (`sdk-cli`) sessions both write there. The slug's drive-letter case
  varies (`c--Projects-...` and `C--Projects-...` are one directory on
  NTFS).
- Every sub-agent of that session, **depth 2 included**, is a flat file
  `<session id>/subagents/agent-<agentId>.jsonl` beside
  `agent-<agentId>.meta.json`. The meta names `agentType`, `description`,
  `toolUseId`, `spawnDepth` (1 or 2 observed: 462 and 22 metas), and, for
  depth 2, `parentAgentId`, the depth-1 agent in the same directory. A
  `model` key appears only when the spawner overrode it. No depth-3 agent
  was observed.
- Each assistant message's `usage` repeats across records: one depth-2
  transcript held 86 assistant records for 41 message ids. Count once per
  `message.id`.
- The parent's tool result for a sub-agent carries a `usage` that is **not**
  the sub-agent's total: one depth-1 agent's summary reported 633 output
  tokens against 53,412 summed over its 20 unique messages. The summary is
  never a source.
- A sub-agent's environment carries `CLAUDE_CODE_SESSION_ID`, equal to its
  parent session's id.
- A session launched under a declared account home (`CLAUDE_CONFIG_DIR`,
  WI-798) writes under that home's `projects/`: the ADJUDICATOR home
  (`%APPDATA%/project-trajectory/accounts/ADJUDICATOR/projects/`) holds
  `C--Projects-ai-template` and lane slugs. `session_keep.account_home`'s
  docstring says "the kit never reads, moves, copies or deletes what a
  provider writes there". LLR-336 (approved) narrows that to "provider
  authentication state is never read ...; Codex rollout telemetry is the
  LLR-267 exception". So this row reads the ambient home only. Reading an
  account home's transcripts would need an LLR-336 exception like the codex
  one (NOTES, call C6).

**Not verified** (the lane's first step, recorded in its decisions before
any coverage claim): whether a resumed session (`--resume`, or `SendMessage`
to a finished agent) appends to the same file or starts another; whether a
`claude -p --output-format json` result's usage includes its sub-agents
(plan step 3; if it does, a service-launched Claude call's sub-agents are
already counted and must not be counted again); and whether any depth-3
agent can exist.

**Anchor.** SN-026 (approved) through SR-222 (approved, derived). SR-222
binds the sessions the loop launches. A session the coordinator's own
harness or an agent's tool spawns is not launched by the kit, so the lane
drafts one derived SR under SN-026, performance lens, with a TC per arm. In
capability voice (ruling 5): "every model session spent on the project's
coordinated work, including sessions an agent spawns within its own session
at any nesting depth, is recorded once in the usage record, and a repeated
or resumed recording adds nothing". Its LLR states the reader's refusal on
an unknown transcript shape.

## Deliverables

1. **The reader, in one adapter.** The transcript format belongs to Claude
   Code (plan item 8, "Trade-off"), so its reader lives beside the claude
   adapter in `session_adapters` and is the only code that knows the shape.
   For one session it yields the session itself and each sub-agent at any
   depth. Each comes with its identity (session id, agent id, parent agent
   id, depth, agent type), its model, its usage summed once per message id
   in the vocabulary SR-222 pins (`usage_record` keys, input inclusive of
   cache), the message ids counted, and its first and last timestamps.
   It refuses, naming the file and the field, on a record shape it does not
   know. It never skips one silently.
2. **The invocation identity and exactly-once.** The ledger contract's
   minimal part, carried here because WI-800's ledger does not exist yet:
   - Each ingested invocation's `invocation-id` is derived from its
     transcript identity (session id and agent id), not from `uuid4`.
   - The log records the message ids it counted, as a count and a cursor,
     the last message id. The cursor is a column of the log, no new carrier.
   - A second ingest over the same transcript records only messages after
     the recorded cursor (a resumed transcript) or nothing (a repeated
     close-out), reading the logs already recorded, committed and spooled.
   - Each log also carries a contribution key, immutable and bound to
     the message range it counted (the invocation identity with the
     first and last message ids counted), so a resumed transcript's
     later log is a second contribution to the same invocation, never
     a duplicate of the first.
   - WI-800's ledger folds each contribution once, keyed by its
     contribution key, into its invocation's total (WI-800's
     Done-when, amended at this row's filing).
3. **Recording through the service's writer.** Each ingested invocation is
   one session log written by `session_service.record`. It carries a role
   of its own (`SUBAGENT` for a sub-agent, `COORDINATOR` for the session
   itself; never `BUILD`, `REVIEW-A`, `REVIEW-B` or empty) and the standard
   `call_` log name. Run from the primary checkout at close-out, it
   therefore spools under WI-960's out-of-lane arm. The log body is a usage
   summary only, never the transcript: prompts and outputs stay out of
   tracked records (SR-176). The usage source is marked as read from a
   transcript (`usage-source`), not reported by a launch.
4. **The command and its place in the cycle.** One command ingests the
   current session (`CLAUDE_CODE_SESSION_ID`) or a named one, from the
   ambient home's `projects/` (account homes stay unread, per LLR-336,
   unless call C6 rules otherwise). The coordinator runs it at close-out
   (`coordinator-cycle` §6) and a headless leg at its end (§7). It skips the
   main transcript of a session the service already recorded, matched by
   the log's `session-id`, so an adjudicator call is not counted twice.
   Whether it skips that session's sub-agents follows the plan-step-3
   finding above.
5. **Records.** IF-245's contract body (the reader), the command's
   interface row, the derived SR, its LLR and TCs, and one RESYNC entry
   (a new adapter and command in shipped modules).

## Trust

Ingested logs land where a gate reads session logs (`docs/iteration/`, via
the spool and WI-800's harvest). This row's ruling keeps them out of every
gate. Written under [PROCESS.md §3, "When a guard is owed"](../../../../project-trajectory/PROCESS.md#3-traceability--anti-duplication).

- **Producer:** the ingest command, through `session_service.record`. Its
  input is Claude Code's transcript files, which neither the kit nor the
  owner writes. Failed writes: a log spooled for some invocations and not
  others (killed mid-run), or a spool write that raises.
- **Consumers** of the logs it writes (grep; the list WI-960's Trust gives):
  `project-trajectory/scripts/kitlib/verdict.py` (`session_log`,
  `review_logs`, `logged_rounds`, the integrator's verdict gate), which
  reads only `SESSION_LOG_RE` names; `project-trajectory/scripts/agent_common.py`
  `phase_draw_ordinal` (skips `call_`) and `next_session_number`;
  `project-trajectory/scripts/agent_brief.py` `last_build_family` (phase
  `BUILD` or empty only); this row's own exactly-once read; WI-800's
  harvest and ledger once built.
- **Ruling:**
  - The ingested logs carry no gate authority: a `call_` name and a role
    outside `BUILD`, `REVIEW-A`, `REVIEW-B` and empty, so no consumer above
    reads one as a round, a build or a draw.
  - A transcript that is absent: nothing recorded for it, and the command
    names it. Unreadable, or of an unknown shape: the command exits nonzero
    naming the file and field, and records nothing for that transcript. It
    never records a partial sum as complete.
  - A sub-agent whose meta is missing or malformed: refused the same way.
    A depth-2 agent whose `parentAgentId` names no agent in the directory:
    recorded with its parent unresolved and the command says so. Its usage
    is real and is never dropped.
  - A killed run is recovered by the next run through exactly-once
    (Deliverable 2): what was recorded is not repeated; what was not is
    recorded.
  - The cursor binds to the logs already recorded, committed or spooled.
    An unreadable earlier log: the command refuses, rather than re-count
    or skip.
- **The bound** (PROCESS.md §6): transcripts as Claude Code writes them
  under the ambient home. A hand-edited transcript, and a session run under
  a declared account home (the adjudicator's), are outside the promise
  unless call C6 widens it. The adjudicator's own calls are recorded by the
  service already.

## Done-when

Each named test fails on the code before the change.
- **The reader**, on fixtures cut from real transcripts (usage values kept,
  text removed): a session with one depth-1 and two depth-2 agents yields
  four invocations with their identities. Each usage equals the sum over
  unique message ids. Repeated records add nothing. The parent's tool-result
  summary is not read.
- **Unknown shape.** A transcript record or meta missing a field the reader
  needs: nonzero exit, file and field named, nothing recorded for it.
- **Exactly once.** Ingesting one session twice records nothing the second
  time. Appending messages to a fixture transcript and ingesting again
  records only the appended messages, under the same invocation identity.
  A run killed after some logs were spooled, then re-run, ends with each
  invocation recorded once. An initial ingest, a resumed transcript's
  ingest and a repeated ingest give two logs under one invocation
  identity with distinct contribution keys, whose usage summed equals
  the usage over every unique message id.
- **No double count.** A session whose id a service-recorded log already
  carries: its main transcript is skipped; its sub-agents follow the
  recorded plan-step-3 finding.
- **No gate authority.** An ingested log in a lane's `docs/iteration/` is
  not a round to `logged_rounds`, not a build to `last_build_family`, and
  not counted by `phase_draw_ordinal`.
- **No transcript text** in any written log (a planted prompt string
  appears 0 times).
- The three unverified facts are recorded in the lane's decisions with the
  probe that settled each, before the coverage claim in the derived SR is
  judged.
- The coordinator-cycle close-out (§6) and headless-leg (§7) text runs the
  command; all three skill copies byte-identical.
- One live ingest of a real coordinator session with sub-agents has run,
  and its totals are compared with the plan's leg-3 method.
- On the landing tip, the commit bar is green, `check_trajectory.py
  --strict` and `trace.py --strict` are clean, the derived rows are judged
  at the lane's sitting, and the RESYNC entry anchors at the landing's
  parent.

## Scope answers

- **S1.** One deliverable: the ingest. It is the second of item 8's two and
  lands after WI-960. Plan step 3 (does a `-p` result include its
  sub-agents) is folded in as a verification, not a deliverable. Plan step
  4 (per-WI reports from the rows) is a query over the ledger. It needs
  WI-800's ledger and is not filed here.
- **S2.** `## Trust`: the logs land in a gate-read directory; the ruling
  keeps them out of every gate.
- **S3.** Closed: the transcript shapes the reader knows, every other shape
  refused; depth by the meta's `spawnDepth`, any value accepted and
  recorded, with the parent resolved or named unresolved; exactly-once by
  invocation identity and cursor.
- **S4.** `single`: a Trust section, an input space (a third party's
  format), two script families (`session_adapters`, the command and its
  caller in the cycle text).
- **S5.** A new input (Claude Code's transcripts), a new value in the role
  domain (`SUBAGENT`, `COORDINATOR`), a new usage source (transcript-read).
  No new component, no new carrier: the logs and the spool are WI-960's.
- **S6.** `WI-960` (hard): its out-of-lane arm is where a close-out ingest's
  logs go; without it a trunk-rooted `record` commits on trunk. WI-800 is
  not needed: the exactly-once key travels in the log, and WI-800's
  backfill reads these logs like any other. WI-798 (account homes; its
  LLR-336 promise bounds which homes are read) is complete. WI-799, WI-851 and
  OI-109, WI-800's other edges, are not needed by this row: they serve
  WI-800's store, harvest-at-discard and held-status work. No new
  dependency: stdlib `json` only.
- **B3.** Exactly-once trusts the logs already recorded, the record each
  earlier ingest wrote at its event. It does not recompute from history.
- **B4.** No owner act. The live ingest reads the box's own transcripts.

## Critique dispositions

Scope critique round 1 (Codex Sol, medium, 2026-10-20; CHANGES-REQUESTED,
findings=1):

- **MAJOR, S5 (a resumed transcript's second log shares the invocation id
  WI-800 appends once by): adopted.** Deliverable 2 now reads "Each log also
  carries a contribution key, immutable and bound to the message range it
  counted" and "WI-800's ledger folds each contribution once, keyed by its
  contribution key, into its invocation's total"; Done-when's "Exactly
  once" gains the initial, resumed and repeated ingest example. WI-800's
  Done-when gains the matching line on trunk in the same commit as this
  disposition, before either row's claim: "The ledger folds each
  contribution once by its contribution key into its invocation's total, so
  a repeated harvest adds nothing and a resumed transcript's later
  contribution is kept."

Confirming round (Codex Sol, medium, convergence stance, 2026-10-20): APPROVE, findings=0; the disposition above is confirmed.
