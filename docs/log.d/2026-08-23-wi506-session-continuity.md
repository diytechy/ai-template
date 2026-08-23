## 2026-08-23 — WI-506 closes: session continuity (OI-57 ruled (b), (c) investigated)

Deferred open items: none — the template review, the ritual, and the trigger
investigation all land findings rather than open questions; the two
fold-ins mint `Drafted` with their own honest debt stated on the row.

**Summary.** Executes OI-57 (b) plus (c)'s trigger investigation in one row:
the twelve `project-trajectory/prompts/` templates read against what this
week's grinds actually did; `prompts/worker.template.md` gains a
standing-state (resume-pack) contract; the proactive context-restart trigger
is investigated per provider rather than assumed. Both orphan fold-ins
(`SR-177`, `LLR-164`) discharge their decomposition debt in the same surface.

### Review findings

The owner's split question — what the ADJUDICATOR is told about lane state
versus what the WORKER is told — reads as a DELIBERATE design split, not an
accident, once the twelve templates are read side by side with
`agent_loop.worker_prompt` / the `adjudicate-*` brief builders:

1. **The adjudicator briefs are narrow, single-verdict, and structurally
   redact the judged party's self-assessment** (`prompts/README.md` rule 3;
   `tests/test_prompts.py::test_no_judging_brief_asks_for_the_judged_partys_self_assessment`).
   `adjudicate-disposition.template.md` even labels the one place a claim
   DOES appear ("a claim under judgement, never as the premise") rather than
   silently trusting it. Every adjudicate-* template gets exactly the
   evidence its one question needs (a report + spec + commit facts; a
   census + spine; a candidate row + open rows + mechanical pre-filter;
   before/after cells + baseline) and nothing more — no predecessor
   context, no branch diff, no lane history.
2. **The worker brief is the opposite shape on purpose: cumulative and
   self-referential.** `worker_prompt` (agent_loop.py ~L359) recomputes,
   FRESH at every launch, predecessor deliverables (`pred_block`), advisory
   registry joins (`context_block` — cancelled precedent, pending OIs, the
   LLR/TC code map, knowledge packs, IF seams, precedent reviews), the
   branch's own accepted-not-yet-reviewed diff (`diff_block`), and any
   rework finding (`rework_block`). This is strictly MORE standing lane
   state than any adjudicator ever receives — correct given the
   adjudicators' whole job is judging one claim independent of a narrative
   it might rationalize around, and the worker's whole job is continuing a
   multi-session build coherently.
3. **The real drift is not the split — it is that the worker brief never
   told the session WHEN to make its own state resumable.** Nothing in
   `worker.template.md` (pre-this-row) instructed the worker to commit
   anything before its FINAL commit. Practice paid for that gap concretely:
   `docs/log.d/2026-08-21-wi498-stage-unification.md` records "RECONCILIATION
   OF AN INTERRUPTED SESSION — THIS SLICE RAN IN THREE SITTINGS, and the
   third is a recovery... Sittings one and two were each interrupted before
   committing, leaving ~121 modified/renamed files in the working tree and a
   slice-5 section here already claiming LANDED — with no gates block and no
   close account." Nine defects were found only by re-running things in the
   recovery sitting — invisible to reading. This is exactly the class of
   residue a written-early resume record would have avoided or shrunk.
4. **The reviewer/critique briefs pin their load-bearing clauses by test
   (`tests/test_prompts.py`); the worker brief carried no equivalent pin
   before this row**, so a future edit could silently drop interruption-
   relevant prose with nothing to catch it (`prompts/README.md` rule 6, "do
   not re-wrap", covers reviewer/critique explicitly and worker only via the
   brace-safety test). Closed here: `test_the_worker_brief_carries_the_standing_state_ritual`.
5. **`LLR-164`'s `test_refs` cell was a wrong citation, not a missing one**
   (see Fold-in B below) — a smaller instance of the same class: a cell that
   LOOKS filled reads as discharged to a casual pass, and only running
   `trace.py` (which checks the TC's own `verifies` list, not just the LLR's
   `test_refs` string) surfaced it as an orphan.

Fixed in-template (uncontroversial wording): the worker's standing-state
bullet (below). Banked as design-shaped, not touched here: whether the
adjudicate-* briefs should ALSO receive a "prior verdict on this same row"
history field for multi-round rows (`adjudicate-conflict` already takes
`{digests}` for staleness detection, which is close but not that) — flagged
as a possible future OI, not built, since it is a scope decision about
adjudicator design, not a resumability gap.

### The resume-pack ritual (the contract, verbatim addition to `prompts/worker.template.md`)

```
- Standing-state discipline: before spending effort on heavy verification (a
  full test suite, a broad multi-file sweep, a wide read), START your log.d
  fragment and land the spec's own `## Context`/`## Deliverable` edits in a
  commit — so a session killed or reaped mid-verification leaves a resumable
  record behind it instead of silent, uncommitted residue. This is not a
  one-shot write at the end: keep both current as the session continues. A
  relaunched session reads this branch's own diff and the fragment fresh,
  same as any other committed state — there is no separate hand-off file to
  produce.
```

No loop-side change is needed to relaunch from that record: the relaunch
mechanism already exists and already works off committed branch state —
`worker_prompt`'s `diff_block` recomputes the branch's own `{base}..HEAD`
diff FRESH at every session launch (agent_loop.py ~L415-426), and
`tests/test_agent_loop_worker.py::test_worker_resume_with_complete_evidence_spends_no_session`
already pins that a relaunch reads committed evidence rather than restarting
blind. Writing the standing-state record EARLY is what makes that existing
mechanism actually useful on an interruption partway through a session,
instead of only after a clean finish. This is the "smallest honest loop
change" the WI asked for: none, because the diff-replay seam was already
built for a different reason (branch resumption across sessions in general)
and generalizes to interruption recovery for free. What remains undone: the
loop still cannot distinguish "died mid-verification, resume from a
deliberately-written record" from "died mid-verification, resume from
whatever happened to be committed" — both look identical to a relaunch today,
because the record IS just ordinary commits. That is fine for what this WI
asked (a resumable record exists), and is recorded here as the honest
residual rather than silently declared solved.

### The trigger, per provider (OI-57 (c))

Investigated by reading how each of the three routed families is invoked and
what the coordinator parses back (`docs/agents.toml`, `agent_session.py`,
`agent_loop.py` ~L2619-2650):

- **ANTHROPIC** (`claude -p --model {model} --output-format stream-json
  --verbose --dangerously-skip-permissions`): the ONLY family whose CLI
  reports token/cache accounting at all — `usage.input_tokens`,
  `usage.output_tokens`, `usage.cache_read_input_tokens`,
  `usage.cache_creation_input_tokens`, `num_turns`, `duration_api_ms`,
  `ttft_ms` — parsed from the transcript's `type: result` event
  (`parse_json_result`). But that event is the LAST line of a completed
  process's output: it exists only AFTER the session has already exited.
  There is no tool or channel by which a still-running `claude -p` agentic
  turn can query its own current context usage mid-session and act on it —
  the accounting is real, but it is post-hoc telemetry for offline
  analysis (exactly what Fold-in A's `LLR-196` cites), not a live signal a
  session could read to decide "restart now."
- **OPENAI** (`codex exec --model {model}
  --dangerously-bypass-approvals-and-sandbox`, result captured via
  `-o/--output-last-message` because codex echoes its banner and the whole
  prompt into stdout): no JSON, no usage/token fields captured by the
  harness at all, live or post-hoc.
- **OPENCODE** (`opencode run -m {model} --auto`, Kimi/Grok): plain stdout,
  same as OPENAI — no usage/token accounting captured.

**Verdict: (c)'s proactive ~66%-context restart is not implementable on real
context accounting for ANY provider this kit routes through today** — not
because the heuristic is merely unproven, but because even the one family
with real usage numbers exposes them only after the process a running
session cannot query has already ended. This confirms OI-57's ruling
((b), no (c) trigger) as investigated fact rather than a deferred guess, and
no guesswork heuristic was built in its place.

### Fold-in A — `SR-177`'s decomposition debt discharged

`LLR-196` (Drafted, `project-trajectory/scripts/agent_common.py`,
`regenerate_index/per_turn_pace/per_turn_context`) cites the real,
already-shipped per-session telemetry columns and the real folding function
that writes `docs/iteration_index.md` — the seam a fan-out utilisation
report would extend — and states plainly that the GROUPING pass (lanes
configured vs occupied, work items per wall-hour) does not exist yet, so
`SR-177` stays undischarged on its own honest terms (the `LLR-193`/`LLR-194`
pattern this repo already uses for a partially-built parent).

`TC-191` (Drafted, Integration/Full) verifies the telemetry INPUT half only,
over 3 EXISTING node ids:
`tests/test_generated_newlines.py::test_the_three_crash_paths_actually_run`
(calls `agent_common.regenerate_index` directly on a synthetic tree),
`tests/test_agent_loop.py::test_done_exit_writes_logs_and_index` and
`::test_stream_json_echo_and_result_parse` (drive a live fake-CLI session
end to end and assert the exact telemetry columns land in the log header).

### Fold-in B — `LLR-164`'s missing TC minted, and a wrong citation fixed

Investigation found `LLR-164`'s `test_refs` cell was not empty — it read
`"TC-157"` — but `TC-157`'s own `verifies = ["SR-146", "LLR-162", "LLR-163"]`
never names `LLR-164`, which is why `trace.py` still reported it orphaned.
`TC-192` (Drafted, Unit/Smoke) verifies `SR-146` + `LLR-164` for real, over 4
existing node ids: `tests/test_routing_and_prompts.py::test_the_catalogue_lists_every_shipped_prompt_with_its_digest`,
`::test_the_catalogue_on_disk_is_FRESH`,
`::test_a_template_edit_moves_its_digest_and_so_the_catalogue`, and
`tests/test_generated_freshness_wiring.py::test_prompt_catalog_step_reds_when_a_template_changes`
(the wired `[step:]` enforcer, driven over a bootstrapped scaffold).
`LLR-164`'s `test_refs` is corrected `"TC-157"` -> `"TC-192"`.

### Watermarks and orphan count

<!-- fig: cmd="python project-trajectory/scripts/trace.py" rev=7507c569 -->

Watermarks `LLR` 195 -> 196, `TC` 190 -> 192, via `trace.py --bump-ids`.
Before: **orphans=7** (`SR-163`, `SR-177`, `SR-181` each missing LLR+TC, plus
`LLR-164` missing a REAL TC citation — 3 SRs x2 + 1 = 7). After:
**orphans=4** (`SR-163`, `SR-181` remain, x2 = 4; owned by other queued rows,
out of this row's scope). `integrity=0` throughout (a transient
citation-frame provenance finding on `LLR-196`'s first draft was corrected
before commit — the argument was kept, the `(WI-119/WI-124)` frame dropped,
per `spine-authoring` §6).

### Adopter-facing surfaces

`prompts/worker.template.md` (kit-owned, not overridable) changed, so
`RESYNC_PACK.md` gains a `[since 7507c569]` entry, and
`prompts/CATALOG.md` is regenerated (`gen_prompt_catalog.py`) — its digest
for `WORKER` moves.

### Gates

- `python -m pytest -q -n auto -m smoke` — **1266 passed, 5 skipped in 20.97s**
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=7507c569 -->
- `python scripts/check_smoke_budget.py --mode enforce` — re-ran the tier
  (21.02s) and reported **smoke wall-clock budget: 21.4s vs 60s budget ->
  within**, exit 0.
- `python project-trajectory/scripts/check_docs.py --root . --stale` — **OK -
  1029 doc(s), 1354 intra-repo link(s), 0 broken (1 orphan warning(s))**
  (pre-existing staleness hints unrelated to this row).
- `python project-trajectory/scripts/check_trajectory.py --strict` —
  **clean (507 work item(s), 479 done, 21 cancelled, graph acyclic)**
  (pre-existing WARNs, e.g. shared open-items.toml SpecRef across sibling
  queued rows, unrelated to this row; the transient R-A "Deliverable filled
  while status=queued" finding this row triggered mid-session cleared once
  the spec moved to `docs/archive/work/complete/`, its intended close home).
- `python project-trajectory/scripts/trace.py` — **orphans=4** (down from 7),
  **integrity=0**, drafts 9 (was 6 — `LLR-196`, `TC-191`, `TC-192` are the
  three new `Drafted` rows this row mints).
- Full unfiltered suite (owed: script/loop-machinery template edit + registry
  change), one background run, `--basetemp=D:\pytest-tmp-w506`:
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-w506" rev=7507c569 -->
  first pass **1 failed, 2903 passed, 14 skipped in 1079.11s** —
  `tests/test_derive_stage.py::test_this_repo_s_committed_stage_is_current`,
  a stale `docs/stage` fingerprint (this row's registry edits changed the
  spine content and nothing had re-derived the committed stage snapshot
  yet). Fixed by running `derive_stage.py --root .` (wrote
  `docs/stage -> DevStg-LLReqs`, unchanged rung); re-ran the one test green,
  then re-ran smoke (`1266 passed, 5 skipped in 22.21s`) to confirm nothing
  else regressed. Not re-run in full a second time — the failure was in a
  single, already-isolated generated-artifact-freshness test with no other
  interaction, and re-running the whole ~18-minute suite to re-observe the
  same 2903 passes would not add information session-protocol's bar asks
  for.

### Deviations from spec

None material. The spec named the ritual as "the fragment section + lane-spec
Context written BEFORE heavy verification" — this session practiced exactly
that ordering for its own close (this fragment and the WI-506
`## Deliverable`/`## Context` reorder were written to disk before the
full-suite gate ran). One incidental fix along the way: the full suite's one
failure was a stale committed `docs/stage` fingerprint, corrected with
`derive_stage.py --root .` in the same window rather than deferred — a
generated-artifact regen, not a design deviation.
