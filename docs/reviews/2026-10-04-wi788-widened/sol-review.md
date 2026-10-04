VERDICT: **NOT-READY**

The widened scope is suitable for a design checkpoint, but its current instructions cannot all be satisfied together. The largest blockers concern state persistence, lock coverage, and evidence produced after refresh.

References below: **W** = [WI-788](../../work/active/wi-788/WI-788-provider-homes-and-new-routes.md); **S** = `project-trajectory/scripts/`; **R/L/I** = `docs/requirements/{system-requirements,low-level-requirements,interfaces}.toml`; **T** = `docs/test/test-cases.toml`. Reviewed at `b61f450f`; no files modified.

FINDINGS:

1. **LS1/LS10’s committed record is not automatically “one truth,” and same-commit recording cannot cover runtime transitions.**  
   W:540–544,683–686 promises atomic evidence/state commits. That works for committed files, but acquiring a lease, launching a process, advancing trunk, and removing a worktree are separate effects. Today claim deliberately orders branch creation before trunk advancement to tolerate interruption (`S/bookkeeping.py:68–80`); dispatch reconstructs from evidence without a state file (`S/dispatch.py:682–690`).  
   **Fix:** distinguish durable decisions from observed execution state. Recommend: “The provider derives current state from committed evidence and live ownership; committed records carry decisions, not claims that a process or lock remains live.” Specify recovery at every effect boundary.

2. **Writing MERGE/ARCHIVE state into the merge tree breaks Bar-Green identity.**  
   W:528–529,683 requires transitions to be committed with their evidence. Today the merge reproduces the refreshed lane tree byte-for-byte (`S/integrate.py:9–14`); Bar-Green verifies the commit’s exact tree (`S/kitlib/verdict.py:414–425,458–461`). A lane commit recording MERGE after refresh loses the attestation; changing the merge tree violates identity. A later trunk bookkeeping commit preserves merge identity, but introduces another transaction and crash boundary.  
   **Fix:** derive completed MERGE from Git ancestry and completed ARCHIVE from retained refs/worktree inventory. Keep committed merge intent before the final bar. State explicitly where records live and which checkout writes them.

3. **LS4’s lock does not freeze all writers capable of invalidating its watermark.**  
   W:559–566 locks the merge slot; W:593–594 removes freshness checking. However, claims write trunk under the dispatch lock (`S/integrate.py:814–817`), intake CLI commands mint through bookkeeping (`S/intake.py:2266–2304`), selected plans allocate IDs directly (`S/plan_artifacts.py:310–351`), and keep-warm records commit on trunk (`S/session_service.py:574–578`). These do not all acquire `out/integrate.lock`.  
   **Consequence:** a locked lane can still become stale or collide with another allocation.  
   **Fix:** define one station-wide authority covering every relevant writer. Hold it through **trunk advancement**, not merely MERGE_ACTION. A lock replaces S11 freshness only after this coverage is established.

4. **The lease wait neither bounds slot occupancy nor prevents deadlock/starvation.**  
   W:564–566 treats risk 5’s twenty-minute wait as a bound. It bounds acquisition waiting, not the sitting or subsequent rounds. Current leases last 7,500 seconds and expire by time (`S/session_keep.py:543–544,464–493`). The dispatcher synchronously invokes integration while polling lanes (`S/dispatch.py:835–836,782`); a waiting transition there can prevent progress needed to release another resource. Existing kernel locks are non-reentrant across descriptors (`S/integrate.py:743–746`).  
   **Fix:** specify canonical lock location, acquisition order, ownership transfer, cancellation and expiry. Wait outside the merge slot and dispatcher tick; use nonblocking scheduling. Risk 5’s fresh session must still acquire station authority. Remove the unsupported-filesystem “run unguarded” behavior for this authority (`S/agent_common.py:946–957`).

5. **The proposed sequence bars the tree before adjudication changes it.**  
   W:561–563 runs refresh/bar before JUDGE/MINT; W:570–584 then permits records, successors, acts and merge decisions. Those writes change the tree. S11 explicitly owes an independent post-act review (`docs/plans/2026-10-03-s11-in-lane-adjudication.md:124–134`), while today refresh stages the final tree before running the bar (`S/integrate.py:2653–2672`).  
   **Fix:** require final independent review after all substantive adjudication writes, then regeneration and Bar-Green on the final staged tree. No subsequent tracked write may alter that tree before merge. Define the rejection/back-edge and lock release.

6. **A lock cannot replace actor and scope checks. LS8 omits an existing refusal that will reject the new flow.**  
   W:637–643 permits acts under the lock, but `merge_approval_refusal` also requires first-approval and amendment scopes (`S/acceptance_record.py:805–824,873`). A work lane claiming no amendment row has empty re-attestation scope. LLR-278 and TC-278 explicitly enforce that condition (`L:2855`; `T:2830`).  
   **Fix:** replace claimed-adjudication-row scope with independently recorded, previewed lane scope. Preserve checks for actor independence, held-rung authority, named rows, snapshot coverage and out-of-scope acts. “ADJUDICATION under lock” alone is insufficient authorization.

7. **Restoring dual-plan pickup is not merely adding a PLANNING state.**  
   W:128–131 correctly distinguishes decomposition from planning a build, but W:522–525,623–624 combines them. Today selected decomposition plans file child WIs (`S/plan_artifacts.py:277–351`); they do not hand the parent directly to BUILD. Restoring the runner inside a lane also exposes its allocator before LS4’s MINT phase.  
   **Fix:** specify two products: an implementation plan for the assigned WI, and a decomposition yielding successor WIs and a terminal parent. Move selected-child allocation onto the one serialized allocator. Define parent closure, PAGE recovery and duplicate suppression before restoring automatic admission.

8. **LS3 is not mechanizable from today’s plan declarations.**  
   W:550–556 requires a strong plan declaring “one file or a few functions.” Existing plan tables declare `Plan-WI`, Title, Covers, Interfaces and Predecessors (`S/plan_artifacts.py:28–29,140–142`), not implementation scope or planner provenance. The routing pin currently yields only to escalation (`S/agent_loop.py:506–510`).  
   **Fix:** design a typed scope declaration with an approved threshold, planner tier, accepted-plan identity and applicability rules. Specify what happens when actual work exceeds that scope, and retain the escalation override.

9. **LS10’s unconditional session resume contradicts current interruption retirement.**  
   W:690–692 says interrupted sessions resume by ID. Today a launch exception retires the session (`S/session_service.py:238–243`), and an expired unreleased lease deliberately prevents reuse (`S/session_keep.py:475–493`). Logs and discovered session IDs are recorded after execution (`S/session_service.py:258–271,304–338`), so a hard interruption can precede either record.  
   **Fix:** “Resume the lane from evidence; resume its session only when its ID and ownership are valid under the reset rules.” Design durable invocation/session discovery and reconciliation; do not promise that a finished-session log exists after every interruption.

10. **BUILD-only attribution will miss authors introduced by this WI.**  
    W:377–383 reads BUILD logs as authorship evidence, while W:280–282 introduces adjudicator and author-review edits. Plain service calls also currently record no commit range (`S/session_service.py:342–351`).  
    **Fix:** record ranges for every authoring kind through the common entry point, and derive exclusion from all authors of the judged scope. Record OI-101’s non-mutating final-pass rule as the specific spine-authoring exception to W:299–302’s blanket session rule.

11. **The accreted text needs an explicit precedence table.** Builders can still follow superseded instructions:

    | Conflict or stale instruction | Wording that should win |
    |---|---|
    | General retention discussion, W:235–244,279 | W:312–320: shipped adjudication retained; builder resets every call; repo dial may remain unchanged. |
    | Spine-authoring “as an option,” W:306–307 | OI-101 final pass, W:79–85: approval only on a non-mutating pass, bounded at three rounds. |
    | Trunk guard “may need removing,” W:400–402 | W:83–85: text/snapshot separation applies on lane **and trunk**. |
    | Separate SuperGrok/CLI research, W:60–73 | W:86–96: Grok/FreeLLMAPI through OpenCode; Google documentation-only and untested. |
    | Arbiter alternatives, W:166–178; ARBITRATION, W:522–524 | ARBITRATION is selection under the chosen protocol; it does not mandate an arbiter model call. |
    | Fresh non-replacing session, W:394–396; LS4 lease requirement, W:559 | Fresh timeout behavior remains a session choice within the same station-locked lifecycle. |
    | Risk 8/common call, W:411–417; LS1/common setter, W:534–536 | `ask` owns model/session calls; lane provider owns lifecycle effects. Both attended and loop paths use their common landing operation. |
    | Six slices, W:220–229; delegated records “slice 2,” W:448; eight slices, W:617–630 | One authoritative dependency graph; replace ordinal references with successor identifiers. |
    | Original half-2 list, W:105–113 | Successor rows deliver the **whole widened scope**; WI-788 closes on approved design and row filing only. |
    | S11 freshness/retake/fallback, S11 plan:122–143,331–357 | LS4 replaces freshness only with complete writer exclusion; explicitly restate the retained exhaustion behavior. |

    LS9’s refined wording at W:659–677 supersedes its earlier proposed wording at W:609–615.

12. **The eight slices are not dependency-correct, and the current Done-when does not expose most widened obligations.**  
    Slice 5 introduces acts/minting before slice 7 supplies text/act separation and dispute prompts (`W:625–629`). Homes also affect retained sessions earlier than slice 6: retained launch homes currently override route environments and are keyed by family (`S/session_service.py:164–171`; `S/session_keep.py:316–328`). Widened obligations sit outside Done-when, which the parser ends at the next sibling heading (`S/kitlib/registry.py:229–253`).  
    **Fix:** make half-1 acceptance explicitly reference every design section and its successor matrix. Slice 3 **can** precede slice 5 as a representation-only refactor, preserving today’s effects; it cannot simultaneously introduce new locking, mint authority or archive ordering.

    Split the design package into linked chapters: **state/evidence and recovery; session/routing and accounts; planning/tiering; adjudication/mint/landing authority**. Finish with one amendment matrix and dependency graph, reviewed at **one owner checkpoint**. Build ordering should be: shared contracts → session/account foundation and behavior-preserving provider → planning → adjudication with text/act split and final evidence → remaining routes. Each shipping slice carries its RESYNC entry; migration cannot wait until slice 8.

OWNER QUESTIONS:

1. **Does adjudication freeze every trunk writer, or only other lane merges?**  
   Options: freeze claims/mints/acts/telemetry too; permit selected writes with explicit invalidation and retake. **Recommend complete exclusion of writers affecting the adjudication tree, queue or watermark.**

2. **What happens when adjudication needs owner input or exhausts its rounds?**  
   Options: release authority and park, then refresh/rejudge on return; land unresolved work using S11’s ruled exhaustion behavior. **Recommend release-and-park for owner input; explicitly preserve or amend the already-ruled three-return landing behavior. Never wait for a person while holding the slot.**

3. **Can RESOLVE clear a reviewer’s CHANGES-REQUESTED without another reviewer verdict?**  
   Options: a scoped adjudication resolution clears named findings; a new independent review must endorse the resulting tree. **Recommend a new independent review**, with the adjudicator’s resolution included as evidence.

4. **Which landing/ref-retention policy becomes universal?**  
   Options: current loop `--no-ff` and deletion; attended squash and retained archive refs. These differ today (`docs/iteration/wi-lifecycle.html:123,269`). **Recommend one policy for both paths, retaining recoverable lane tips.** The owner must choose squash versus preserved lane commits.

5. **What qualifies for LS3’s tier reduction?**  
   Options: an exact file/function-count threshold; an independently approved scope classification. **Recommend a small explicit threshold plus approved plan identity**, with scope expansion returning to the declared tier.

INVENTORY GAPS:

- **Carriers omitted from W:502–511:** claim commits and branch refs; disposable refresh commits and parent/tree attestations; per-WI outcomes for mixed batches; immutable `docs/handbacks` reports; partial patches; `docs/id-watermark`; `last_approved/acts.toml`; decisions records; planning artifacts; retained-session leases/tombstones; uncommitted/stashed residue; retained archive refs and worktree presence. Evidence: `S/integrate.py:33–53`; `S/kitlib/station.py:118,196`; `S/handback.py:115–119,415`; `S/bookkeeping.py:68–80`; `S/session_keep.py:264–299`.

- **Modules omitted from W:512–519:** `trunk_step`, `bookkeeping`, `spec_move`, `acceptance_record`, `baseline_snapshot`, `agent_common`, `agent_policy`, `agent_brief`, `agent_route`, `session_service`, `session_keep`; `plan_runner`, `plan_round`, `plan_artifacts`, coverage/composition modules; `consolidate`, `rejudge`; `kitlib.registry`, `.station`, `.verdict`, `.done_when`, `.decisions`, `.provenance`, `.authority`; commit-floor/hook consumers. The provider must orchestrate these owners without duplicating their judgments.

- **LS8 row inventory is incomplete.** Add an explicit **amend/preserve/retire** matrix:
  - Lifecycle/serialization: SR-148, SR-156, SR-170, SR-173, SR-174 (`R:640,740,941,984,999`); LLR-137/140/144/149–154 (`L:1343,1382,1431,1490–1551`); TC-132/143–148 (`T:1303,1412–1472`).
  - Approval/snapshot scope: SR-140/178/179/207; LLR-158/173/178/**220/278**; TC-153/167/173/**218/278** (`L:2326,2855`; `T:2258,2830`). Preserve mirror, foreign-drift and human-authority rules; locking does not discharge them.
  - Review/provenance: SR-208/209; LLR-246/262; TC-257 (`R:1445,1460`; `L:2578,2742`; `T:2689`). A state-record write inside a REVIEW range currently violates verdict-only scope.
  - Checkpoints/consolidation/attended recovery: SR-215/220; LLR-255/264/265; TC-248/260/261 (`R:1545,1615`; `L:2654,2748,2759`; `T:2577,2709,2720`). Include idle census, release/stage-gate minting and sampled clean closes—not only LS8’s six post-merge arms.
  - Contracts: IF-080/154/173; IF-081/155; IF-090/091/**101/186**; IF-123/129/220; IF-228/229/242/243/244; planning IF-058/060/**061**/066; decisions IF-255/256; retention IF-247/248. Relevant rows: `I:515–569,1103–1158,1262–1275,1372,1602,1650,1852,2047,2102–2194,2232–2248,2298–2314`.

- **Docs/prompts omitted from the amendment list:** PROCESS.md:447–451; PROCESS_OPTIONS.md:445–458,1990,2037–2041,2189–2192,2814–2858; worker prompt:68–71; first-approval prompt:6,62,99; amendment prompt:43,91,96; disposition prompt:50; consolidate prompt:97,114; red-TC prompt:50; concurrency-v2’s slot/refresh rules:264–285; runtime-flows.md:168–191; registry-machinery-reference.md:204,797–818; enforcement-audit.md:61; lifecycle drawing:120–123,247–285. Several already contradict today’s refresh implementation; distinguish existing drift from changes this WI introduces.

- **Adjacent ruled work needs explicit dependencies:** OI-100/WI-791 adds need/assumption/surrogate routing and held-rung CLARITY acts while retaining registry coupling (`docs/requirements/open-items.toml:3703–3704`). WI-790 requires OI placeholders and commit-versus-parent synchronization (`WI-790:176–190,312–350`). LS6 must consume those contracts, not redesign them independently.