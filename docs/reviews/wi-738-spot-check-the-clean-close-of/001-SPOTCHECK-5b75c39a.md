# SPOTCHECK — WI-738 — the clean close of WI-736, judged at 5b75c39a

A sampled spot check of a GREEN close (`docs/process.toml [attestation]
complete_review = "sample"`). One question: does what shipped answer what the
row asked for? The row asked for the three numbered replacements in WI-736's
Context, one test, no code, and every `Status` left Drafted. The close stands
whatever is found here. A finding is a successor row, never a reversal.

What was read: the closed spec
`docs/archive/work/complete/WI-736-batch-i-returns-bound-sr-222.md`, and its
queued form at `5b75c39a^`. Its Context is byte-identical in both, so the
draft I checked against is the one the builder had. Also read: the squash
`5b75c39a` (`git show`, `--stat`, and the diffs of the two registries, the
test file, `docs/stage`, `docs/ratify/CURRENT.md` and the coordinator log);
the review `docs/reviews/2026-09-28-wave6/sonnet-wi736.md`; the rows SR-222
and SR-227 (`system-requirements.toml`), TC-264 (`test-cases.toml`), and
LLR-270's detail; `session_adapters.py` (`USAGE_KEYS`, `USAGE_COUNT_KEYS`,
`usage_record`, `PlainAdapter`, `_result_event`, `_claude_raw`,
`_claude_usage`, `ClaudeAdapter.one_turn`, `_basename`, `_BY_PREFIX`,
`adapter_for`); `session_keep.py` (`store_lock`, `_try_lock`, `_write_whole`,
`store_save`, `write_tombstone`, `load_honoured`, `keep_abandon`,
`keepwarm_due`, `due_routes`, `take_warm_lease`, `applies`); `session_service.py`
(`_identity`, the usage path in `act`, `KeepWarmer`, `keep_warmer`); the
routes in `project-trajectory/agents.template.toml` and `docs/agents.toml`;
the new test and its TC-264 neighbours in `tests/test_session_service.py`;
and the successor `docs/work/queued/WI-737-adjudicate-sr-222-sr-227-tc.md`.
I checked each clause against the registries, the code, the tests or the
diff, not against the builder's or the reviewer's account. HEAD stayed at
349eef9d throughout.

What was run, in this worktree:

- `python -m pytest -q -n 2 tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py -p no:cacheprovider`
  -> `105 passed in 23.24s`.
- `python -m pytest -q -p no:cacheprovider "tests/test_session_service.py::test_gemini_usage_is_recorded_with_unread_values_empty" -m smoke`
  -> `1 passed in 0.14s`. The new test is in the smoke tier, as TC-264's
  `tier = "Smoke"` requires.
- A verbatim check. A script parsed both registries at `5b75c39a^` and
  `5b75c39a` with `tomllib`. It pulled each backticked "replace X with Y",
  "insert before" and "replace the closing" pair out of the Context. It
  asserted each "before" string occurs exactly once, applied it to the
  parent cell, and compared the result with the squash cell by cell. The
  results:
  - SR-222: all fields match, with no residual difference;
  - SR-227: all fields match;
  - TC-264: all fields match;
  - the paths changed across the whole SR registry are exactly SR-222's
    `requirement`, `acceptance_criteria` and `rationale`, and SR-227's
    `requirement`;
  - across the whole TC registry, only TC-264's `method` changed.
- A probe of `adapter_for(...).usage(...)` over a hand-built gemini result,
  with `stats.models.<model>.tokens` filled and a `session_id`. It was
  written from the documented shape, not recorded from the CLI. It ran
  compact, pretty-printed, and pretty-printed after a stderr banner line. Each ran under argv[0]
  `gemini`, `C:\npm\gemini.cmd` and `/usr/bin/gemini`. All nine cases gave
  `PlainAdapter`. `cli`, `gen_ai.provider.name`, `raw-usage`, the five
  counts and `fresh-input-tokens` were all `""`, and the key set equalled
  `USAGE_KEYS`. `gen_ai.conversation.id` was `abc` without the banner and
  `""` with it. `gen_ai.response.model` was `""` and `usage-scope` was
  `unknown` in every case.
- A probe of `one_turn` per adapter. claude appends `--max-turns 1`. codex,
  opencode and the plain adapter return the argv unchanged.

The scratch scripts lived in the session scratchpad, outside the worktree.
At the end, `git status --short` shows only this record.

## Per-item findings (WI-736 Context, items 1 to 3)

1. [MET] SR-222. All four replacements and the one rationale insertion
   landed verbatim, and nothing else in the row moved (script above).
   `sn_refs`, `boundary_refs`, `hat_refs`, `da_refs` and `title` are
   unchanged. Each new sentence is true of the code:
   - "empty for any other runner": `PlainAdapter.provider = ""`, and
     `OpencodeAdapter` inherits it. Only claude and codex set a constant.
   - "the runner name is left empty": `PlainAdapter.cli = ""`, and
     `adapter_for` gives the plain adapter to every basename not starting
     `claude`, `codex` or `opencode`. The shipped gemini route
     (`agents.template.toml`, `gemini -p {prompt} --output-format json`) is
     one of these.
   - "every count or raw usage the loop cannot read ... empty": the plain
     adapter reads only a claude-shaped `usage` object. A gemini result has
     none, so every count is `None` and `usage_record` blanks it. `raw` comes
     from `_claude_raw`, which keeps only `type: result` lines, so it is
     `""`. The probe shows this over all three output shapes.
   - "also when that runner is reconfigured": the provider is a class
     constant chosen by basename alone, so no argument changes it. The
     existing codex reconfiguration test holds this.
   - "a stand-in included ... carries the same columns": the `python`
     stand-in row in `test_every_provider_row_carries_the_same_columns`
     asserts the empty provider and the full column set. Its counts are
     filled because its fixture is claude-shaped, which the "cannot read"
     wording allows.
   - The ambiguous "including when ..." clause (WI-735 observation 1) is
     gone.
2. [MET] TC-264. The Method insertion landed verbatim after the named
   anchor, and nothing else in the row moved.
   `test_gemini_usage_is_recorded_with_unread_values_empty` is exactly the
   test the draft named. It uses a `gemini` argv over a gemini-shaped
   result, and asserts `cli`, `gen_ai.provider.name`, `raw-usage`,
   `*USAGE_COUNT_KEYS` and `fresh-input-tokens` are `""`, and that the key
   set equals `USAGE_KEYS`. It sits under the file's TC-264 banner, and it
   passes with no code change, as the draft predicted.
3. [MET on the row's terms; see Observations 2 and 3] SR-227. The
   requirement replacement landed verbatim, and nothing else in the row
   moved. The two lifted clauses match the acceptance's existing wording,
   which is what the item asked for. In the code:
   - "whole": every write of the store goes through `_write_whole`, which
     writes a `mkstemp` file and then calls `os.replace`.
   - "by one writer at a time": every record write (`store_save`) is under
     `store_lock`, an `O_EXCL` lock file.
   - "one bounded turn": the keep-warm ping is `one_turn=True` with a 300 s
     wall (`KEEPWARM_TIMEOUT`).
   - "never blocks the scheduler": the ping runs on its own thread, and a
     tick while one is in flight starts no second one.

   The two observations below are edges of the new shall that the draft's
   "LLR-270 already implements them" did not look at.

## Scope held

- There is no change under `project-trajectory/` and none to the LLR
  registry. The out-of-scope rows LLR-266 to LLR-270, DA-016 and DA-017 are
  untouched.
- SR-222, SR-227 and TC-264 read `Drafted` at HEAD. WI-737 (queued) holds
  their first approval: `adjudicates = ["SR-222", "SR-227", "TC-264"]`.
- No gemini output reader was added, and WI-733's two unrelated
  observations were left alone.
- The other files in the squash are bookkeeping:
  - the generated `PROJECT_STATE.html`, `docs/open-items.html` and
    `docs/ratify/CURRENT.md`. The ratify brief restates the new cells;
  - `docs/stage`, where only the fingerprint and as-of line move;
  - the closed spec's Deliverable;
  - the review;
  - the coordinator log. Its log also carries an unrelated section on the
    second full unfiltered suite. That is not a spine row or code, so the
    draft's refusal list does not reach it.

## Observations

None is a gap in what the row asked for: every replacement and the test are
as drafted. Each observation belongs to WI-737, which already owns the first
approval of these cells, so none needs a new row.

1. `gen_ai.conversation.id` for another runner is not covered by SR-222. The
   plain adapter fills it from any top-level `session_id` or `session-id`.
   The fixture carries one (the reviewer's accepted minor), and so may a
   real gemini result. I did not run the CLI, so this rests on the fixture
   and my probe, not on a recording. SR-222's new text is silent on the column,
   so this is no violation. The acceptance's "every count or raw usage the
   loop cannot read" does not claim it either way. WI-737 may want to decide
   whether the conversation id is read or left empty for another runner.
   Today it is read, but only when the output is exactly one JSON object. A
   stderr banner before the object leaves it empty, as the probe shows.
2. The keep-warm one-turn bound holds only when the ANTHROPIC route runs
   claude. `keepwarm_due` selects by the record's `family == "ANTHROPIC"`.
   `applies` retains any adjudication route, whatever its runner. But only
   `ClaudeAdapter.one_turn` bounds the argv (`--max-turns 1`), and the
   opencode, codex and plain adapters return it unchanged. So an adopter's
   ANTHROPIC-family route served through opencode, say `opencode run -m
   anthropic/...`, would ping with only the 300 s wall as its bound. That is
   not "one bounded turn". The shipped template and this repo's roster
   route ANTHROPIC through claude only, so no shipped configuration hits
   this. The clause was already in SR-227's acceptance before this lane.
   For WI-737: narrow the clause to the claude runner, or make keep-warm
   depend on the runner rather than the family.
3. The shall's "write the retention state only whole, by one writer at a
   time" reads more strictly than the tombstone does. `write_tombstone`
   writes `<record>.retire` whole but with no lock, by design. LLR-270 says
   so ("written whole with no lock"), and `load_honoured` unlinks it under
   the lock. Every record write is serialized. The tombstone is a lockless
   mark, and each write of it is whole (`os.replace`), so no reader sees
   half of one. Whether the tombstone counts as "retention state" under
   "one writer at a time" is WI-737's reading. The code and LLR-270 agree
   with each other. Also, "never blocks the scheduler" allows
   `take_warm_lease`'s bounded `store_lock(wait=0.5)` on the dispatcher's
   own tick. That wait is bounded and small, but it is a wait.
4. Prefix matching. `adapter_for` matches by basename prefix, so
   `claudette` gets `ClaudeAdapter`, and `codex-proxy` and `opencode2` get
   theirs. SR-222's "a runner other than claude, codex and opencode" is
   therefore bounded by name prefix in the code. This is LLR-266's approved
   rule and outside this lane. It is noted only so WI-737 reads "runner" as
   the code does.
5. The commit bar's seconds read 72.8 s against the 60 s budget. The
   squash message says so and attributes it to contention. One 0.14 s test
   cannot account for 12 s. This is outside the one question here, and I
   did not re-measure it.

Three items were checked: all met, verbatim, with nothing else moved in
either registry. The new test passes in the smoke tier, and the three
session modules ran 105 passed. The new SR-222 sentences are true of the
plain adapter over every gemini output shape probed. What shipped answers
the row. The observations are refinements for WI-737, which already owns
these cells.

VERDICT: CONFIRMED
