# ADJUDICATE — WI-737 — first approval at 349eef9

Independent adjudication, spine-acts batch J, of the three rows the brief
marks `[AWAITING FIRST APPROVAL]`: SR-222, SR-227 and TC-264. TC-268 is another
adjudication's row and was read as chain evidence only. LLR-266 to LLR-270,
TC-262, TC-263, TC-265 to TC-267 are approved and were read as the chain. I
read the brief (`adjudicate_brief.compose`) in full, and I directed none of the
amendments judged here.

Earlier verdicts (WI-724, WI-731, WI-734) are context, not authority. What
WI-736 changed was read from `git show 5b75c39a` and its archived spec. Its
three registry replacements match batch I's draft word for word, and it added
one test (`test_gemini_usage_is_recorded_with_unread_values_empty`). DA-016
and DA-017 (Drafted) were read as chain evidence and are not flipped here.

`Approved` blesses the TEXT; whether the tests pass is the harness's answer.

Method: each row is restated as its obligation and read three ways:

- upward, to its need, hats, boundary and assumption;
- sideways, to its sibling LLRs;
- downward, to its test cases and to the code at HEAD
  (`session_adapters.py`, `session_service.py`, `session_keep.py` and their
  test modules).

Each routed pointer cell was ruled on its own. The question list is the
spine-authoring skill's.

- [APPROVE] SR-222 -> the delivered loop content records every model session it launches in one usage record. The record holds the pinned vocabulary and revision, input inclusive of cached input, one fresh-input formula, the raw usage verbatim, the roster provider for every routed call, the runner named, and `gen_ai.provider.name` as the default provider for claude and codex (empty for any other runner, reconfiguration not detected). Occupancy of the latest request is kept apart from billed tokens. For a runner other than claude, codex and opencode, the runner name is left empty, and so is every count or raw usage the loop cannot read -> the pointer cells hold. `SN-Refs` SN-026 HOLDS as a labelled derived row: the rationale argues both lenses and feeds back to the need. `Hat-Refs`: PERFORMANCE's `listens_for` ("incomparable or unavailable measurements reported as a reliable total") is exactly the inclusive-input and empty-not-zero clauses, and CONSISTENCY's ("readers disagreeing after a one-sided change") is the one-record, one-path clause, so both HOLD. `Boundary-Refs` B-10 HOLDS: the loop invoking a model runner, the output coming back. `DA-Refs` DA-016 HOLDS: it bridges the default-provider premise, with its obstacle as the stated reconfiguration limit. Batch I's finding is answered. The full record is now bounded to the three runners the loop reads, and any other runner's record is stated as a closed default: the plain adapter (LLR-266's "else a plain adapter"), with `cli = ""` and `provider = ""`, reads a claude-shaped result only. The shipped gemini route therefore records the same columns with its runner, its provider name, its raw usage and every count empty, and TC-264's new clause asserts this. Spot-check observation 1 is gone: the acceptance now reads "anthropic for claude and openai for codex, also when that runner is reconfigured … and empty for opencode", which matches `ClaudeAdapter.provider`, `CodexAdapter.provider` and opencode's inherited `""`. A stand-in's claude-shaped result is still read by the plain adapter (raw usage and counts filled), and "every count or raw usage the loop *cannot read*" states exactly that, so it is not a contradiction. The absolute advisories ("every model session it launches", "every routed call", "any other runner", "every count … the loop cannot read") each range over the loop's own launches, its routing registry or its own reader, so each domain is closed. The shall's "the runner named" followed by "the runner name is left empty" for other runners is an explicit exception, not an ambiguity. TC-262 to TC-265 cover every clause -> ready. There is no requirement-form finding with the row flipped.
- [APPROVE] SR-227 -> where the retention dial is above zero, the delivered loop content does the following for each adjudication of a retained class. It resumes the route's active, unheld session in its runner's resume form, or mints and records an id. It waits a bounded time on a held session, then runs unretained and states why. It records each call like any other. It drains the session at the dial or when the inputs it judges under change, retires it only when no work it has a stake in is pending, and retires it at once on a failed call. No two calls use one retained session at once. The retention state is written only whole, by one writer at a time, and any keep-warm call is one bounded turn that never blocks the scheduler -> the pointer cells hold. `SN-Refs` SN-025 HOLDS as a labelled derived row (the rationale argues three lenses and feeds back). `Hat-Refs` PERFORMANCE (operating cost left unassessed), UNATTENDED-OPS (the silent degrade of a full, stale or failed session) and INTEGRITY-RECOVERABILITY (a store updated in place, a hold nothing reclaims) each name a failure this row states, so they HOLD. `Boundary-Refs` B-10 HOLDS. `DA-Refs` DA-017 HOLDS: it bridges the resume premise, and its obstacle (a runner update changing resume semantics) is what the runner-version drain answers. Batch I's finding is answered. The shall now carries the whole-write single-writer clause and the bounded, non-blocking keep-warm clause, so LLR-270's store and keep-warm machinery and TC-268 trace to a shall that demands them. Checked against the code: `_write_whole` (mkstemp plus `os.replace`), `store_lock`, the keep-warm ping on its own thread under `one_turn`, and `keep_for`'s bounded wait with a stated reason. I re-read the shall against the acceptance clause by clause for the same class of gap and found none that is load-bearing. Four readings, recorded so a later reader need not re-argue them. (1) The acceptance's "runner version changed" falls within the shall's "the inputs it judges under change": the runner carries the judgement, and the acceptance only names those inputs. (2) "Active" in the shall means not retired, and the acceptance fixes that a draining session is still resumed. (3) At the run's end, waiting out a ping in flight delays the exit and blocks no scheduling. (4) The raising-launch tombstone is written whole without the store lock, by the session's lease holder. It is a blind whole-file write, not a read-modify-write, and the one overlap it can meet (a holder writing after its lease expired) names a session that `retire_stale_lease` has already retired. The absolutes ("each adjudication of a retained class", "any keep-warm call", "never blocks the scheduler") range over the loop's own calls and its own dispatcher, so each domain is closed. The dial-zero sentence observes the absence of the `Where` feature. One real gap sits under the text, not in it. It is WI-738's observation 2, confirmed at HEAD. Keep-warm selects by family (`keepwarm_due` reads `family == "ANTHROPIC"`, and `due_routes` globs `ANTHROPIC-*.json`), and only `ClaudeAdapter.one_turn` adds `--max-turns 1`. So an admissible adopter row with family ANTHROPIC served through opencode would be pinged with only the 300 s wall, which is not "one turn". No shipped route does this. The clause is the right obligation: a ping exists to refresh a cache, and an open agentic session is not what it should launch. The defect is therefore in LLR-270's selection and in the code, not in SR-227's words. Returning the SR would send unchanged text round a fourth time (skill §2: a sound requirement violated by code needs a fix). The fix is drafted in WI-737's `## Dispositions`: keep warm only a route whose runner bounds a call to one turn, with LLR-270 and TC-268 amended narrowly. LLR-270 and TC-266 to TC-268 cover every other clause -> ready. There is no requirement-form finding with the row flipped.
- [APPROVE] TC-264 -> over each runner's recorded fixture, the case asserts the pinned revision and names, inclusive input and one fresh formula for every adapter. claude: reasoning from `output_tokens_details.thinking_tokens`, the response model of the last request despite a background model's entry, or the one matching `modelUsage` entry, and anthropic. codex: cached input already inside its input, empty cache write and reasoning, and openai even when reconfigured. opencode: steps summed with reasoning inside output, and an empty provider. A stand-in's provider is empty. A runner other than the three, over a gemini `--output-format json` result, gets the same columns with its runner, provider name, raw usage and every count empty. Every record carries exactly the same columns -> `Verifies` SR-222 and LLR-268 HOLD. Each clause maps to a test in `tests/test_session_service.py` (`:58` to `:183`), the new one included, which asserts `cli`, `gen_ai.provider.name`, `raw-usage`, the five `USAGE_COUNT_KEYS` and `fresh-input-tokens` are `""` and the keys equal `USAGE_KEYS`. This closes batch I's return: the SR-222 clause for any other runner now has its verifying case. `Evidence`, `Level` Unit, `Tier` Smoke and `Automated` Yes are consistent with the module -> ready. One observation, not a finding: the gemini fixture's `stats.models` is empty, so the case shows that no zero is invented, but not that populated gemini token stats stay unread. The claude reader never reads `stats`, so the assertion holds for a populated result too. A stronger fixture would be a test-quality choice, not an unverified obligation. There is no requirement-form finding with the row flipped.

Checks I ran at 349eef9 (results seen, not claimed):

- `python -m pytest -q -n auto tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py -p no:cacheprovider` gave **105 passed in 19.96s**.
- Form gate: SR-222, SR-227 and TC-264 were flipped in the working tree and `trace.py --root . --strict` was run. There was **no `FINDING (requirement form)` line**. The only new lines against the unflipped run (rc=0) were the expected pre-snapshot `approval record` and `integrity` pairs, one per flipped row (rc=1 from those). The report's absolute and no-`Form` advisories for SR-222 and SR-227 are warn-only; the absolutes are ruled above, and the no-`Form` line is carried by all 120 SRs. The flips were then restored for this verdict commit.
- Snapshot pre-check, read-only: `baseline_snapshot.refresh_refusal` with `--approves "docs/requirements/system-requirements.toml=WI-737;docs/test/test-cases.toml=WI-737"` returned an empty refusal, so the act is **accepted**.

The WI-738 spot check of WI-736's close (CONFIRMED) was passed to me during
the sitting as chain evidence. I ruled its observations as follows:

- **(1)** `gen_ai.conversation.id` is filled from an unread runner's top-level
  `session_id`. SR-222 obliges nothing about that column for another runner.
  The value is the runner's own id, not a count or raw usage, so it is not a
  defect.
- **(2)** The keep-warm one-turn gap is real and load-bearing. It is ruled on
  the SR-227 line and drafted as the one successor.
- **(3)** The tombstone's lock-free whole write is ruled on the SR-227 line,
  reading (4). The 0.5 s bounded `store_lock` wait in `take_warm_lease` is
  lease bookkeeping, not the keep-warm call. The clause concerns the call not
  stalling the tick, and a bounded half-second lock attempt does not. This is
  wording, not a defect.
- **(4)** Basename-prefix matching is LLR-266's approved rule for telling
  runners apart (it covers `.exe` and `.cmd` shims). SR-222's "a runner other
  than claude, codex and opencode" leaves the identification to the design
  row, as the SR tier should.

The act, in the next commit: SR-222, SR-227 and TC-264 are flipped `Drafted`
-> `Approved`, and the scoped snapshot is taken with both `--approves` tokens.
Nothing is returned. The one `## Dispositions` draft in WI-737's spec is a
successor for the keep-warm code gap, and it changes no text this sitting
approved.

OUTCOME: APPROVE rows=3
