## 2026-08-30 — WI-548: the stall guard stops booking a reviewer outage as the builder's stall (C1–C7)

Built BY HAND on the claim branch under the tracked pause (the loop never
builds the loop), from the plan of record
[2026-08-30-stall-guard-plan.md](../plans/2026-08-30-stall-guard-plan.md) —
the owner's direction after WI-521's finished, committed slice was closed
`partial` over three failed reviewer draws: *"the fallback is an independent
opus reviewer, not a partial WI."*

**What shipped, by change:**

- **C1 — route-aware stall accounting** (`agent_loop.RoutingState`): a JUDGING
  session (review/critique draw) never touches the builder's stall streak
  (`note_session(judging=)`); failed draws count on their own
  `review_draw_failures` streak, reset by any recorded verdict.
- **C2 — "review owed" is a parked state, not a handback**:
  `EXIT_REVIEW_OWED = 9` (end of the alphabet; 10 stays retired). When the
  build is committed and `--stall-limit` consecutive draws fail — or no
  reviewer is routable at all — the worker writes the lane-local
  `out/review-owed` marker and exits 9. The dispatcher treats 9 like a crash
  (parked, resumed), never a decided close; the resumed worker reads the
  marker and schedules the owed round FIRST. A completed round clears the
  marker.
- **C3 — idle deadline** (`agent_session.run_session(idle_timeout=)`): the
  reader thread stamps the last output line; a silent child is killed
  `idle_timeout` seconds after it (engine default 900 s, slot
  `AGENT_SESSION_IDLE_TIMEOUT` in all four launchers, flag
  `--session-idle-timeout`, 0 disables). The wall kill still reports
  `timed_out is True`; the idle kill reports `"idle"` (truthy) and the session
  log gains the typed `timeout: wall|idle` header key.
- **C4 — pre-dispatch liveness probe** (`probe_route`/`select_with_probe`): a
  route cooled earlier in the run (ERROR/TIMEOUT/limit/garble) is a SUSPECT
  and must answer a 30 s `OK` probe on its own CmdTemplate — verbatim, so a
  template defect is caught by the probe, not a burned draw — before another
  real session is spent on it. A clean route is never probed.
- **C5 — the same-family reviewer fallback rung**: when the cross-family
  ladder is exhausted the draw retries with heterogeneity relaxed, and ANY
  same-family review draw (however reached) is recorded — `-relaxed` on the
  verdict filename, `heterogeneity=relaxed` on the round line, a typed
  `heterogeneity: relaxed` telemetry key.
- **C6 — the close ritual + the unload**: `worker.template.md` gains the close
  step (Deliverable before Context, specref cleared, ratify render when spine
  rows minted, `## <date> — <title>` fragment heading, `spec_move.py`, the
  `WI:` trailer on the close commit); `adjudicate-disposition.template.md`
  now has the adjudicator close its OWN row the same way (the judged row
  stays untouchable) and pins the draft's shape (this spec's `## Dispositions`,
  top-level keys, title ≤ 120). `integrate.unload` sheds the loop's own
  `out/run-logs/` streams and the `out/review-owed` marker as declared
  residue — their clipped copies are tracked under `docs/iteration/`, and on
  2026-08-30 every mechanized lane ended UNLOAD INCOMPLETE over exactly them.
- **C7 — the review brief's reading scope**: the brief names the exact
  three-dot diff against the CURRENT trunk with telemetry/record/generated
  exclusions, harness output is read as summaries (one run, quote the summary
  block), registries are grepped by cited row, and `{trunk}` +
  `{process_doc}` are SLOTS `reviewer_prompt` renders per repo
  (`trunk_name`, `process_doc_path`) — this meta-repo has no
  `docs/process.md` while every adopter does, so a literal was right
  downstream and wrong here. The TERRA review leg carries
  `-c model_reasoning_effort=medium` as a measured experiment (note on the
  row; keep or revert on round wall + `tokens used`).

**Deviations from the plan, each deliberate:**

- One row (WI-548) instead of the plan §3's two — its own fold-in option; the
  pause lifts after a single reviewed merge.
- C6's adjudication closer is the ADJUDICATOR (brief instruction), not a new
  dispatcher close path — smaller diff, no new machinery, and the dispatcher
  keeps zero authority over spec moves. The plan called the dispatcher path
  "cleaner"; a mechanized closer can land later as its own row if the brief
  proves insufficient.
- Two shipped unload pins were OVERTURNED with the behavior change, stated in
  the tests themselves (`test_the_shed_covers_the_loops_own_stream_but_never_the_root_out`,
  the declared-set test): the ignored session stream was the canonical
  sole-copy example, and C6's measurement says it is the loop's own artifact
  with a tracked clipped copy. The `.env` example carries the sole-copy
  lesson now.
- `RESYNC_PACK.md` gains the two entries the previous run owed
  (`check_docs` HTML-comment fix since 59f52549; opencode `--dir .` since
  59ab2951) plus this change set's own entry.

**Byte deltas on watched files:**
`project-trajectory/PROCESS_OPTIONS.md` 179,258 → 180,984 (**+1,726**
FLAGGED: the REVIEW-OWED exit-9 bullet and the two-deadline / stall-split
paragraphs in "Unattended operation" — the exit alphabet is a documented
contract and the plan's §6.1 requires the entry). No capped file touched.

**Verification:** unit + e2e suites green in the lane
(`tests/test_agent_loop_routing.py`, `test_session_stdin.py`,
`test_agent_loop_review.py` — including the outage→park→resume→round e2e,
the single-family relaxed recording, and the rendered-slot brief —
`test_dispatch.py`, `test_integrate_unload.py`, `test_module_size_ratchet.py`,
`test_prompts.py`, `test_dogfood_sync.py`); a scaffold was bootstrapped from
this branch's kit and one fake-agent `--wi` session driven in it (the brief
renders `docs/process.md` THERE — the slot proving both sides); full-suite
totals in the Deliverable. Module-size ratchet re-stamped with reasons:
agent_loop 3622 → 3924, agent_common 2660 → 2678, integrate 2626 → 2647.

Deferred open items: none — the owner's review of this run rides
`docs/decisions-for-review-2026-08-31.md` (decisions 33+).
