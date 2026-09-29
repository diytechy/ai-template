# SPOTCHECK — WI-735 — the clean close of WI-732, judged at 03debc71

A sampled spot check of a GREEN close (`docs/process.toml [attestation]
complete_review = "sample"`). One question: does what shipped answer what the
row asked for? The row asked for the seven numbered items in WI-732's Context,
plus its carry-over. The close stands whatever is found here. A finding is a
successor row, never a reversal.

What was read: the closed spec
`docs/archive/work/complete/WI-732-batch-h-returns-fix-gen-ai-pr.md`; the
squash `03debc71` (`git show`, `--stat`, `--numstat`, and a word diff of the
three registries); the review `docs/reviews/2026-09-28-wave6/sonnet-wi732.md`;
ruling 1 of `docs/reviews/2026-09-28-wave6/ARBITRATION.md`; the log section
"WI-732 lands" in `docs/log.d/2026-09-28-wave6-coordinator.md`; the rows at
HEAD: SR-177, SR-193, SR-222 and SR-227; LLR-223, LLR-266, LLR-268 and LLR-270;
TC-220, TC-264 and TC-267; DA-015, DA-016 and DA-017, and the header of
`assumptions.toml`; `.claude/skills/spine-authoring/SKILL.md` §2(b), §2(d2), §3
and §6; `session_adapters.py` (`PlainAdapter`, `ClaudeAdapter.provider`,
`CodexAdapter.provider`, `OpencodeAdapter.usage`, `adapter_for`);
`session_keep.py` (`keep_for`, `_lease_held`); `assumption_rules.py`
(`SR_CLASSES`, `_classify`, `classify_srs`, `sr_classification_advisories`,
`da_citing_srs`); the provider assertions in `tests/test_session_service.py`
and the TC-267 test in `tests/test_session_keep.py`; the bookkeeping commit
`22e7b247`; and the two adjudications minted at this merge,
`docs/work/queued/WI-733-adjudicate-llr-223-sr-177-t.md` and
`docs/work/queued/WI-734-adjudicate-llr-266-llr-268.md`. I checked every
clause against the registries, the code, the tests or the diff, not against
the builder's, the reviewer's or the arbiter's account. HEAD stayed at
22e7b247 throughout.

What was run, in this worktree:

- `python -m pytest -q -n 2 tests/test_session_adapters.py tests/test_session_service.py tests/test_session_keep.py tests/test_assumption_rules.py -p no:cacheprovider`
  -> `297 passed in 58.78s`.
- `python project-trajectory/scripts/trace.py --root . --strict` at HEAD ->
  exit 0, `SN=31 SR=120 LLR=268 TC=271 orphans=0 integrity=0 ... drafts=11`.
  SR-222 and SR-227 are absent from the unclassified advisories (SR-024,
  SR-129, SR-224 and SR-226 remain). No line names DA-016 or DA-017.
- The landing check. A script set `effect_at = ["B-10"]` on DA-016 and DA-017
  (`git diff --stat`: 2 insertions, 2 deletions). I ran the same `trace.py
  --root . --strict`, then restored the file with `git checkout --`. The run
  still exited 0, and the only difference from the HEAD run is four new
  advisories: for each of the two rows, "serves need SN-026 / SN-025, but none
  of its landing crossings belongs to a party of the need's approved
  stakeholders or one mediating for it", and "lands on B-10 (EXT-005), which
  reaches none of the needs it serves". This confirms the arbiter's reach
  claim independently. After the restore, `git diff --quiet HEAD` held.
- An in-memory probe of `classify_srs` and `sr_classification_advisories`
  over eleven synthetic rows. It used one declared assumption, one sibling
  sharing the row's need and one disjoint sibling. The results:

  | case | class | advisories | failures |
  |---|---|---|---|
  | joint + waiver | joint | joint-waiver contradiction | 0 |
  | non-joint DA-Refs + waiver | both | DA-plus-waiver contradiction | 0 |
  | disjoint-only sibling + waiver | coincident | disjoint sibling | 0 |
  | joint + DA-Refs + waiver | joint | joint-waiver contradiction only | 0 |
  | disjoint sibling + DA-Refs + waiver | both | disjoint sibling, DA-plus-waiver contradiction | 0 |
  | waiver only | coincident | none | 0 |
  | joint + DA-Refs, no waiver | joint | none | 0 |
  | undeclared DA + waiver | (none) | none | 1 |
  | joint + undeclared DA + waiver | (none) | none | 1 |
  | undeclared sibling + DA-Refs + waiver | (none) | none | 1 |
  | whitespace DA-Refs + waiver | coincident | none | 0 |

The probe and trace captures lived in the session scratchpad, outside the
worktree. At the end, `git status --short` shows only this record.

## Per-item findings (WI-732 Context, items 1 to 7, and the carry-over)

1. [MET; the acceptance wording is for WI-734, see Observation 1]
   `SR-222.requirement` now takes the item's second option and states the
   limit plainly: gen_ai.provider.name holds "the runner's default provider —
   anthropic for claude and openai for codex — and empty for a
   provider-agnostic runner or a stand-in, with runner reconfiguration to
   another provider not detected". It says what the value is. "Set by the
   adapter" is gone from both the requirement and the acceptance. The
   classification was decided: `da_refs = ["DA-016"]`, and trace no longer
   reports the row unclassified. DA-016 is a premise about the world. It
   claims that the vendors' runners serve their vendor unless redirected, and
   its falsifier can be observed: a call with no override served by another
   provider. Its obstacle is exactly the limit SR-222 accepts. Its obstacle hat
   (PERFORMANCE) is one SR-222 carries.
2. [MET; no code change was needed] The item said "implement and state". The
   rule chosen in item 1 is the one the code already held:
   - `ClaudeAdapter.provider = "anthropic"` and
     `CodexAdapter.provider = "openai"` are class constants;
   - `PlainAdapter.provider = ""`, and `OpencodeAdapter` inherits it (its
     docstring says "it names no provider");
   - `adapter_for` chooses by `argv[0]`'s basename alone, so no argument
     changes the provider.

   `session_adapters.py` is therefore rightly absent from the squash.
   `LLR-268.detail` now names each constant as "the ... runner's default
   provider" and adds "The provider constants do not detect a runner
   reconfigured to another provider". The rest of the Detail is unchanged
   (word diff).
3. [MET] `TC-264.method` adds "default" to the claude and codex clauses, says
   codex stays openai "even when its runner is reconfigured", and gives the
   stand-in its own "provider name is empty" clause.
   - `test_codex_provider_name_stays_at_its_default_when_reconfigured` passes
     `-c model_provider="third-party"` and asserts `openai`.
   - `test_every_provider_row_carries_the_same_columns` now asserts
     `rows[-1]["gen_ai.provider.name"] == ""`, and `rows[-1]` is the `python`
     stand-in over the claude fixture.
   - The existing claude (`:63`), codex (`:117`) and opencode (`:141`)
     assertions cover the remaining clauses.
   - The rest of the Method is unchanged.
4. [MET] `SR-227.acceptance_criteria` now reads "waits a bounded time and
   then runs unretained, stating why". This is the item's own "smallest fix",
   and it matches the row's shall and LLR-270 ("waits up to lease_wait
   seconds ... saying why").
   - The lane neither declared the bound nor put the reason in the
     accounting, so LLR-270 rightly did not move.
   - `TC-267.method` now says the adjudication "runs unretained with the
     stated reason naming the holder".
   - The test captures stderr and asserts `"held by keep-warm:x"`. That string
     is `keep_for`'s printed line, with `busy` taken from `_lease_held`, the
     live lease's holder.
   - Classification is DA-017, a premise about the runners (the documented
     resume form continues the named transcript). Its falsifier can be
     observed, and its obstacle hat (INTEGRITY-RECOVERABILITY) is one SR-227
     carries.
   - TC-267 stays Approved and is in WI-733's `adjudicates` for the
     re-attestation its amendment re-opens.
5. [MET] `LLR-266.detail`: "and no codex command template carries -o" is
   dropped. The item offered dropping it, or stating the last-`-o` behaviour,
   as alternatives, and dropping it is the smaller. The clause now reads "codex
   gets both --json and an -o/--output-last-message temp file", which claims
   nothing about templates adopters write.
6. [MET; one residue in the same row, see Observation 3] `SR-177.rationale`
   no longer contains "must" or any token or per-lane aggregation. It states
   the gap as a reason: "The existing telemetry does not join configured
   lanes, occupied lanes and integrated work per wall-hour into the per-run
   aggregation the acceptance requires. Without that aggregation, the
   telemetry columns alone cannot distinguish configured capacity from
   run-level utilisation." Its three quantities are the acceptance's three,
   and it adds no inputs. The other sentences argue the need for the row and
   the refused alternative (a numeric target). No sentence obliges anything
   beyond the acceptance.
7. [MET; one precedence edge for WI-733, see Observation 2]
   `LLR-223.detail` now reads "A joint row with Coincident, or a non-joint row
   with both DA-Refs and Coincident, is an advisory naming the contradiction".
   The probe matches it on every classified case:
   - joint + waiver and joint + DA-Refs + waiver give only the joint-waiver
     advisory;
   - a disjoint-only sibling + waiver classifies coincident, with only the
     disjoint advisory, as the item described;
   - a non-joint row with DA-Refs + waiver, with or without a disjoint
     sibling, gives the `both` contradiction.

   This agrees with SR-193's acceptance ("both assumption citations and a
   waiver, or both joint delivery and a waiver"), TC-220's method ("joint with
   a waiver is reported ... A citation with a waiver is reported") and the
   `sr_classification_advisories` docstring. No code or TC changed, which is
   right, since the lane kept the code's reading.

- Carry-over [MET]. `22e7b247` adds LLR-267, LLR-269 and LLR-270 to WI-734's
  `adjudicates` (first approval), and LLR-222, LLR-286 and SR-193 to WI-733's
  (re-attestation). WI-733 also carries the three amended Approved rows:
  SR-177, LLR-223 and TC-267. WI-734 carries SR-222, SR-227, LLR-266, LLR-268
  and TC-264.

## Scope held

- The registry hunks touch only these cells:
  - SR-177's rationale;
  - SR-222's requirement, acceptance and new `da_refs`;
  - SR-227's acceptance and new `da_refs`;
  - the details of LLR-223, LLR-266 and LLR-268;
  - the methods of TC-264 and TC-267.

  `--numstat` gives 6/4 lines in the SR file, 3/3 in the LLR file and 2/2 in
  the TC file.
- The diff moves no `status`. SR-177, SR-193, LLR-223 and TC-267 read
  Approved at HEAD. SR-222, SR-227, LLR-266, LLR-268 and TC-264 read Drafted.
- DA-016 and DA-017 are new Drafted rows. They are well formed:
  - every cell the neighbouring rows carry is present;
  - `standing = "active"`;
  - trace raises no assumption-tier, reach or obstacle-hat line for either.
- The codex and opencode "NOT LIVE ... owed to a person" wording was left
  alone, as the row directed.
- The code is unchanged. Only two test files moved, by 4/1 and 9/0 lines.

## Observations

None is a gap in what the row asked for. Each belongs to the adjudication
that already owns the cell: WI-734 for Drafted SR-222, and WI-733 for the
Approved SR-177 and LLR-223 it re-attests. None needs a new row.

1. The acceptance clause in `SR-222.acceptance_criteria` is ambiguous. It
   reads: "gen_ai.provider.name is anthropic for claude, openai for codex, and
   empty for a provider-agnostic runner or a stand-in, including when runner
   reconfiguration means the default-provider value does not identify the
   provider serving the call". The "including when" clause follows the
   "empty for ..." item, so it can be read as "empty when reconfigured". That
   is the opposite of the requirement ("reconfiguration ... not detected"),
   TC-264 and the test, which all keep `openai`. The intended reading also
   leaves the observable implicit. A tighter wording: "gen_ai.provider.name
   is the runner's default provider (anthropic for claude, openai for codex),
   also for a runner reconfigured to another provider, and empty for a
   provider-agnostic runner or a stand-in". This is for WI-734.
2. The runner-to-provider pairs now sit in four cells: SR-222's requirement
   and its acceptance, LLR-268's detail, and TC-264's method. Item 1's own
   option ("the runner's default provider, with a reconfigured runner not
   detected") would stand in the SR without naming claude and codex. Whether
   the pairs earn a place in the SR tier (§2(b); §3's "no second home") is
   WI-734's judgement. It is not a defect.
3. `LLR-223.detail` does not state what happens when a row has an undeclared
   reference, and the probe shows it. A row with an undeclared assumption or
   sibling is failed and left unclassified, and it gets no contradiction
   advisory even beside a waiver. This includes a row whose declared sibling
   shares its need, which the detail's own first sentence would call joint.
   Item 7 did not ask about this, and SR-193 and TC-220 are silent on it too.
   One clause would close it: "a row with an undeclared reference is failed
   and not classified". This is for WI-733's reading of LLR-223.
4. SR-177 still has a residue after item 6. Its acceptance ends "the
   aggregation itself is the row's stated build gap". That points at a gap the
   rationale now states without using those words, and it is not a fit
   criterion (§3). The rationale's "The existing telemetry does not join ..."
   and that acceptance sentence both become false the moment the aggregation
   ships, so that work must amend both Approved cells. The item asked for the
   gap to be restated as a reason, and it was. This is for WI-733.
5. In `keep_for`, a wait that times out on the store lock rather than on a
   lease prints "held by the store lock". This names no holder. SR-227's
   "stating why" still holds, and TC-267 claims the holder only for the
   keep-warm lease it drives, so the claim and the evidence agree.

Seven items and the carry-over were checked: all met. Item 2 needed no code,
because the code already held the chosen rule. Scope held on every clause. The
landing check confirmed the arbiter's reach claim, and the four session and
assumption modules ran 297 passed. What shipped answers the row. The
observations are refinements for WI-733 and WI-734, which already own these
cells.

VERDICT: CONFIRMED
