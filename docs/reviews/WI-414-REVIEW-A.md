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

---

## Round 2 & 3

Round 2 accepted **scope moved** and that WI-390 owns the amendment, but returned
BLOCKING: "route to WI-390 and produce nothing" is not an authorized §A5.2
outcome. Round 3 accepted the re-scope of WI-390 as authorized, substantively
sufficient and legitimately placed, and confirmed the SpecRef-clock warning
cleared for the intended reason; it returned two record-accuracy defects (a log
fragment still carrying the superseded account, and an overstated claim about
the notes shape), both since corrected.

### Round 3 verdict, verbatim

## Subject

REVIEW-A round 3 of HEAD 9823b951 against claim base 536a19a7. Read-only review; worktree clean. Primary risks examined: a nominal re-scope invisible to WI-390’s future worker, a falsely cleared SpecRef clock, and disagreement between the completed spec and permanent log fragment.

## What I ran

Worktree and whitespace:

```text
## wi-414-adjudicate-tc-056
git diff --check rc=0
```

Current strict trajectory check:

```text
check_trajectory: clean (414 work item(s), 393 done (95%), 17 cancelled, graph acyclic).
```

It emitted ten unrelated connectivity warnings and no WI-390 warning. Running the same checker in a detached clone at parent 225dccdf reproduced the removed warning:

```text
check_trajectory: WARN - WI-390: its SpecRef docs/concurrency-v2.md changed after the WI row was last touched — re-validate the WI against the amended requirement ...
check_trajectory: clean (414 work item(s), 393 done (95%), 17 cancelled, graph acyclic).
```

The clock cleared for the designed reason: backlog_staleness_findings accepts a body-content edit at the same path as a re-affirmation; WI-390 was last touched by 9823b951 after the SpecRef’s f822e336 amendment. This was neither a status move nor filename rename. Source: project-trajectory/scripts/check_trajectory.py:2488-2553.

Direct R-A and intake probe:

```text
loader integrity=0 R-A=0
disposition drafts=0 refusal=None
```

Context/parser/worker-prompt probe:

```text
agent_common WI-390 status/deliverable chars: queued/0
schedule WI-390 status/deliverable chars: queued/0
check_trajectory WI-390 status/deliverable chars: queued/0
worker prompt contains Re-scope heading: False
worker prompt contains TC-056: False
raw queued spec contains Re-scope heading: True
```

Focused tests:

```text
.......                                                                  [100%]
7 passed in 0.83s
```

The merged-range amendment probe confirmed no ratified-cell edit in the triggering range: LLR-056 changed traced CodeSymbol; TC-056 changed traced Evidence and routed-traced Verifies. Source: docs/concurrency-v2.md:604-616.

## Findings

1. MAJOR — The permanent log fragment still records the superseded “route only” account and omits the real §A5.2 output.

   docs/log.d/WI-414-adjudicate-tc-056.md:29-48 says “Routed, not filed” but never records that WI-390’s spec was amended with the WI-414 re-scope note. The session protocol requires the fragment to record material deliverables; once compiled, this becomes the durable session account.

   The fragment also retains both MINOR formulations that were corrected only in the Deliverable:

   - Lines 8-18 still emphasize “only then” ordering without stating that Verifies is traced and that endpoint disagreement carries the judgment.
   - Lines 44-47 say “Flipping TC-056 would assert…”, although TC-056 is already Verified and no Modified → Verified flip exists.

   Update the fragment to record the WI-390 amendment and use the corrected endpoint/status reasoning. Source: .agents/skills/session-protocol/SKILL.md:80-98.

2. MINOR — The Deliverable overstates the note’s exact shape.

   docs/work/complete/WI-414-adjudicate-tc-056-ratified-routed-cel.md:71-76 says WI-390 carries a `## Re-scope` section “naming the three cells.” The actual structure is `## Context` containing a `### Re-scope` subsection, and it names three affected rows/surfaces—not three cells. SR-055 and LLR-056 contain multiple stale ratified fields, while TC-056 alone names Method and Expected explicitly.

   The note remains sufficient for routing because it incorporates WI-389’s broader “ratified prose” route and leaves exact amendment construction to WI-390’s owner sitting. Correct the structural/counting claim.

## Explicit determinations

- AGREE — Re-scoping WI-390 is authorized. §A5.2 says:

  > “Its only outputs are (a) flipping `Modified` rows back to `Verified` … or (b) filing real WIs — a `spine` WI for the scope change, and cancellations or re-scopes of queued WIs whose premise moved.”

  Source: docs/concurrency-v2.md:638-642.

- AGREE — This note is substantively sufficient. It identifies WI-414 and range 7894457..5211f07 as origin; names SR-055, LLR-056, and TC-056; retains WI-389’s broader route; and leaves Modified/re-attest work to WI-390.

- AGREE, qualified — `## Context` is valid on a queued row and preserves R-A. The structured loaders deliberately discard it, and agent_loop’s generated worker prompt does not include the stored note. Nevertheless it is not invisible to every mandated reader: session-protocol explicitly requires opening the scoped WI spec. Sources: project-trajectory/scripts/agent_common.py:696-702,776-796; project-trajectory/scripts/agent_loop.py:423-474; .agents/skills/session-protocol/SKILL.md:21-27.

- AGREE — The SpecRef-clock warning cleared, for the intended same-path content-edit reason.

- AGREE — Both corrections in the Deliverable are now correct. DISAGREE that they were corrected across the complete permanent record; the fragment remains stale.

- AGREE — R-A holds, strict check_trajectory exits 0, and intake._disposition_drafts returns zero drafts with no refusal.

VERDICT: REWORK

---

## Rounds 4 & 5 — APPROVE

Round 4 confirmed the substantive corrections held and found two record defects
(an overreaching claim that `## Context` is not machine-consumed, and an
orphaned sentence left by a botched string replacement). Round 5 verified both
fixed and returned **APPROVE**.

### Round 5 verdict, verbatim

No findings.

- `## Context` characterization is precise: registry parsing clips it, while the knowledge-pack advisory reads the full spec (`check_trajectory.py:479-499`, `2437-2485`). The Context-only citation regression test passed (`test_trajectory_arch.py:508-515`).
- The Deliverable paragraph is complete, headed, and explains that filing the other arm would duplicate WI-390 (`WI-414-adjudicate-tc-056-ratified-routed-cel.md:71-79`).
- Neither correction introduces a new inaccuracy.
- Mechanical checks:
  - strict `check_trajectory`: exit 0; clean, with only existing advisory warnings.
  - Registry integrity: 0; R-A findings: 0.
  - `_disposition_drafts`: 0 drafts; refusal `None`.
  - `check_docs`: exit 0; 0 broken links, with existing warn-only status/staleness output.
  - Focused regression: 1 passed.
  - Worktree remains clean.

VERDICT: APPROVE