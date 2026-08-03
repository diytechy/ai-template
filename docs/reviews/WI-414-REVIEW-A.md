# WI-414 — REVIEW-A (2026-08-02)

**Reviewer:** OPENAI-SOL (`gpt-5.6-sol`) via the `codex` CLI — cross-family,
fresh context, independent of the builder. Charter:
[code-review-adversarial](../rubrics/code-review-adversarial.md).

**Verdict: REWORK** — the reviewer DISAGREED with both halves of the builder's
judgment, and was right on both. The builder's "scope did not move" rested on
intra-branch commit order rather than on the adjudicated merge range, and the
drafted disposition was misrouted (`ordinary`/`quick` for work that edits
ratified cells and owes a re-attest), duplicative (WI-390 already owns the
amendment, as WI-389's own Deliverable records) and too narrow (SR-055 and
LLR-056 are equally false). The judgment was rewritten to **scope moved**, the
`## Dispositions` section removed, and nothing minted.

---

Subject: WI-414 at `7861dd97`, reviewed against parent `536a19a7` and the adjudicated trunk range `7894457..5211f07`. The worktree was clean. The actual close commit also contains `docs/log.d/WI-414-adjudicate-tc-056.md`; the findings below apply to both records.

## What I ran

The requested command could not run because this host has no `python` executable:

```text
zsh:1: command not found: python
```

The identical code under `python3` parsed one draft without refusal. A concise follow-up census produced:

```text
drafts: 1
refusal: None
route: {'workstream': 'process', 'buildtier': 'quick', 'kind': 'ordinary', 'specref': 'docs/test/test-cases.csv'}
exact-title already exists: False
WI-390: {'Status': 'queued', 'BuildTier': 'medium', 'SafetyClass': 'spine', 'SpecRef': 'docs/concurrency-v2.md'}
```

The merged-range cell census returned:

```text
LLR-056
  traced CodeSymbol: process_panel/_loop_panel -> process_panel/_station_panel
TC-051
  traced Evidence: tests/test_gen_trajectory.py... -> tests/test_traj_panels.py...
TC-056
  traced Evidence: old process-loop nodes -> WI-389 station-cycle nodes
  traced Verifies: SR-055;LLR-056 -> SR-055;LLR-056;IF-093;IF-094
```

There were no ratified-cell changes. Only TC-056 `Verifies` belongs to the routed traced-cell set; the other three cells are mechanically silent under the ruling in `concurrency-v2.md` lines 604-616 and `intake.py` lines 355-368.

The TC-056 timeline was:

```text
7894457
  Verifies: SR-055;LLR-056
  Evidence: ...test_process_tab_renders_intake_and_decision_loops...
56dc580d
  Verifies: SR-055;LLR-056
  Evidence: ...test_process_tab_renders_the_station_cycle...
575610f2
  Verifies: SR-055;LLR-056;IF-093;IF-094
  Evidence: ...test_process_tab_renders_the_station_cycle...
5211f07
  Verifies: SR-055;LLR-056;IF-093;IF-094
  Evidence: ...test_process_tab_renders_the_station_cycle...
```

The eight Evidence nodes passed using the repository’s available virtual environment:

```text
........ [100%]
8 passed, 1 warning in 0.53s
```

The disposition-focused intake tests passed:

```text
..... [100%]
5 passed, 14 deselected, 1 warning in 1.23s
```

The warnings were environment-only: CPU capping and pytest cache writes were unavailable.

Strict trajectory integrity passed:

```text
check_trajectory: clean (414 work item(s), 393 done (95%), 17 cancelled, graph acyclic).
```

It emitted 11 warn-only pre-existing connectivity/SpecRef-clock messages, including WI-390’s changed SpecRef warning. `git diff --check HEAD^..HEAD` exited 0 with no output.

The completed spec body also parses in its current order:

```text
Status: done
Deliverable chars: 1823
Deliverable starts: Adjudicated 2026-08-02. The judgment, and the follow-up it surfaced:
```

## Findings

1. BLOCKING — “SCOPE DID NOT MOVE” is not supported by the adjudicated merge range.

   The strongest case for the builder is real: by commit `575610f2`, the station tests already existed, and that commit only registered IF-093/IF-094 and added their IDs. The tests genuinely pin the main derived values: integrator outcomes and `BAR_GREEN` in `test_traj_panels.py` lines 375-423, and schedule’s exclusive-kind tables in `test_traj_panels.py` lines 426-448.

   But WI-414 adjudicates `7894457..5211f07`, not merely `56dc580d..575610f2`. On the pre-merge baseline, TC-056 cited the hoop tests. The same merged range replaced that Evidence with station-cycle tests and then added two new interface contracts to `Verifies`. The “tests already sitting” argument in `WI-414-adjudicate-tc-056-ratified-routed-cel.md` lines 20-22 relies on intra-branch commit ordering and hides the trunk-to-trunk movement the adjudication exists to judge.

   This is material re-scope:

   - SR-055 still requires two circular loops and one shared `LLM_Agent`, `system-requirements.csv` line 56.
   - LLR-056 still describes those loops, `low-level-requirements.csv` line 55.
   - TC-056 Method/Expected still specify two hoops and 11 arrows, `test-cases.csv` line 55.
   - The implementation now emits one station cycle, `traj_panels.py` lines 563-571 and 788-802.
   - `Verifies` formally states everything a test verifies, including IF contracts, `PROCESS_OPTIONS.md` lines 2136-2143.

   The stale Method/Expected are therefore not an unrelated defect “elsewhere in the same row”; they are direct evidence that the WI-389 merge changed the test case’s behavioral scope without moving its ratified definition.

   Remedy: rewrite the Deliverable and log fragment to judge scope moved and route the already-owned spine amendment through WI-390.

2. MAJOR — The disposition is syntactically valid but semantically misrouted and duplicative.

   The proposed work edits ratified TC cells, yet declares `safety_class = "ordinary"` and `buildtier = "quick"`. Section A5.2 says a real scope change files a `spine` WI, `concurrency-v2.md` lines 638-642. An ordinary lane is not the correct route for ratified Method/Expected amendments and their re-attestation.

   More importantly, that work already exists. WI-389 explicitly records the stale ratified SR/LLR/TC prose for WI-390 in `WI-389-process-tab-station-flow.md` lines 73-79. WI-390 is queued, spine-class, and owns “THE SPINE AMENDMENT” plus any further amendments surfaced by the builds, `WI-390-concurrency-v2-program-close.md` line 3.

   Intake deduplicates only by exact title, `intake.py` lines 729-736. The driven result says `exact-title already exists: False`, so merging WI-414 would mint a redundant ordinary WI despite WI-390’s existing spine scope. The draft is also too narrow: it names only TC-056 Method/Expected even though SR-055 and LLR-056 remain false as well.

   Remedy: remove `## Dispositions`, point the adjudication to WI-390’s existing spine amendment, and correct the permanent log fragment. No cancellation or open item is warranted: the work and authority are already settled. No immediate Status flip is appropriate either; WI-390 should amend the ratified cells and perform the corresponding Modified/re-attestation flow.

The section order itself is legitimate, not a workaround. `check_trajectory.py` lines 479-499 require Deliverable before Context, while `intake.py` lines 553-586 parses Dispositions independently. The live parser confirmed the Deliverable remains visible.

Builder judgment (1): DISAGREE.

Builder judgment (2): DISAGREE overall. I agree that Method/Expected are stale, but disagree that a new ordinary/quick disposition is correct; the staleness is part of the real scope movement and is already owned by WI-390.

VERDICT: REWORK