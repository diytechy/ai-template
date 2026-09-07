# Work types, approval snapshots and adjudicator continuity

This audit supplements the [target flow](README.md#3-the-target-loop) and
[control repair](CONTROL-RETRY.md#owner-clarification-and-revised-resolution).
Source baseline: `4c26e432`. It records the owner's clarification and proposed
repair; the diagrams do not claim that the runtime already implements it.

## Meaning and approval

The earlier “stale approval evidence” framing was too broad. A changed byte or
requirement attribute triggers mechanical drift detection and a semantic
comparison with the last approved snapshot. It does not establish changed
meaning. If the adjudicator confirms that meaning is unchanged and accepts
the wording, existing implementation judgments remain valid and the mechanical
approval step updates the snapshot. Do not add another implementation approval
requirement merely because that text or its hash changed.

An existing ID denotes a stable meaning. In the owner's clarification,
“reapproval” of edited prose asks whether that meaning stayed the same; it is
not permission to assign a new meaning to the same ID. If equivalence cannot
be established, keep the prior approved snapshot and resolve the semantic
question. An actual meaning change requires impact review of every use and
reference to the ID, including downstream requirements, tests, implementation
and approval evidence, before the changed obligation can be accepted. A local
MEANING verdict followed by a new snapshot is not sufficient. No new-ID policy
or replacement status is introduced here: `Modified` remains retired because
the snapshot detects textual drift.

Implementation WIs do not amend their governing SN/SR/LLR prose. A needed
change returns as a handback; a separate exclusive spine WI authors it. The
exclusive window prevents implementation from racing a requirement change.
Judging a handback from ordinary work is still an exclusive adjudication turn;
it does not entitle the ordinary worker to share the adjudicator conversation.

This ownership boundary is not new. Owner ruling **2026-09-01** already states
it, with the same concurrency reasoning, and `lane_approval_refusal` carries the
argument verbatim: two lanes touching the spine conflict at merge and the
snapshot must not move across a workstream, whereas a serial trunk-side act
cannot conflict. The ruling assumed the act was trunk-side; the adjudication-lane
exception landed the same day with the first-approval arm (WI-572) and made it a
claimed worktree, which is what removed the guarantee the ruling rested on. The
repair closes an exception to a standing rule; it establishes no new one.

The snapshot always represents the last approved state. Proposed wording may
be on trunk while awaiting judgment, with the previous snapshot still intact
and drift still visible. Approval and its mechanically produced snapshot must
be published together before the window releases dependent work. Rejection or
a request for revision leaves that baseline intact. A whole-registry copier
must not absorb pending, unapproved cells outside the accepted change.

Identifying which proposal was approved is still necessary to copy the right
content. That bookkeeping is not a second semantic judgment. Likewise, the
existing review of an implementation candidate's tree is a different question
from whether requirement prose preserves its meaning.

## Where adjudication runs

The owner's “active branch” means the integration branch in the coordinator's
primary checkout: currently `contract_split` in this repository. It does not
mean an arbitrary WI branch, and it does not require switching to `main`.
Use the coordinator's designated checkout and branch, not the adjudicator's
ambient working directory, to identify that location.

Adjudication runs there as an exclusive coordinator turn. It does not receive
a separate adjudication worktree. Existing coordinator/integration ownership
must keep lane admission, merges and other writers from interleaving with
that turn; the retained conversation also has only one caller. Work-item and
verdict records still identify the judgment and its scope, without creating a
branch to carry the approval act. Findings requiring new prose return to a
separate exclusive authoring WI; the judge does not rewrite the requirement
it is judging.

For a new item, the accepted judgment, approval Status change and mechanically
generated snapshot are published in the same trunk commit. For confirmed
equivalent wording, retain the existing approval and implementation judgments,
and publish the equivalence decision with its mechanical snapshot update on
trunk. This advances the accepted wording without pretending it is a new
obligation. For unresolved or changed meaning, hold the baseline until the
semantic question and any required impact review are resolved.

## What the runtime does today

```mermaid
flowchart TD
    subgraph Trunk[Current trunk]
        M[Merge lane under integration lock]
        M --> D[Post-merge changed-cell scan]
        D --> Q[Mint amendment adjudication WI]
        Q --> E[Dispatcher drains lanes and admits exclusively]
    end
    subgraph Lane[Current exclusive adjudication worktree]
        B[Brief reads approved snapshot and live requirement chain]
        B --> J[Fresh provider invocation judges amendment]
        J --> P[Prompt directs model to run snapshot copier]
        P --> R[Review and integration still pending]
    end
    E --> B
```

The final two nodes expose the ownership defect: the copy can precede accepted
approval, and the adjudicator runs in a worktree even though worker guidance
describes approval as a trunk act. The stopped retry is evidence of this path;
its proposed snapshots have not been integrated into primary.

| Boundary | Read-only finding and source |
|---|---|
| Admission | `dispatch._kind_action` and `_admission` admit ordinary work in parallel, spine batches exclusively, and adjudication exclusively. `_branch_exclusive` also reads claimed safety classes when resuming parked work. These are scheduler guarantees for classified WIs, not proof that every actual edit obeys its class. |
| Location | `lane.spawn_worker` launches the claimed worktree; `agent_loop._resolve_root` makes that worktree the effective root. Exclusive does not mean trunk-resident. |
| Detection | `integrate.integrate_one` calls `intake.intake_after_merge` while holding the integration slot. `_routed_amendments` uses `acceptance_record.staged_spine_amendments` over the before/after merge trees; the amendment brief separately supplies the last-approved snapshot and live chain. The trigger scan itself is not a semantic comparison. |
| Authoring scope | `worker.template.md` permits authoring Drafted rows and amending cell text in its generic worker rules. `acceptance_record.lane_approval_refusal` prohibits approval acts but expressly permits amendments. This does not enforce the owner's implementation-versus-spine separation. |
| Snapshot write (direction) | The amendment and first-approval briefs direct the model to invoke the copier; `adjudicate_brief._aftermath` reinforces this. Move the write to the trunk approval boundary and remove that worker permission. |
| Snapshot write (permission) | Removing that direction is insufficient. `integrate._approval_act_refusal` passes `_adjudication_lane`'s actor flag to `acceptance_record.merge_approval_refusal`. First approvals enter `adjudication_approval_refusal`, which bounds flips by `Adjudicates` and requires their registry snapshots in the same branch delta. An amendment with no Status flip instead returns the delta-read error alone, permitting snapshot writes without that scope check; this is the WI-605 path. The ordinary-lane arm prohibits snapshot writes. Replace both adjudication exceptions with trunk-side approval publication, preserving scope checks there. |
| Trunk-turn concurrency | Moving the turn onto the primary checkout makes it a SECOND writer on the branch the merge slot writes. `integrate._slot` takes `out/integrate.lock`, and its own docstring states the design assumption the change breaks: the slot is "held for well under a second". An adjudication turn is a provider session lasting minutes. Taking the slot for its duration queues every merge behind an LLM call; not taking it leaves two processes writing one working tree with nothing detecting the interleave — worse than today's merge conflict, which Git catches. `integrate()` also refuses on a dirty trunk BEFORE taking the lock, so a mid-turn trunk makes the queue refuse itself. Decide which, and state the throughput consequence. |
| Adjudication close | `dispatch._close_done_adjudication(root, branch)` and `handback.close_adjudication(root, branch)` are branch-keyed. A turn with no branch has no key for them, and that path exists precisely because the dispatcher once resumed a finished adjudication row forever (OI-70 decision 21, the C6 loop). Rehome the close to the trunk turn's own record or the loop returns. |
| Bar on the approval commit | A lane branch is attested by `Bar-Green:` verified at the merge slot. A direct trunk commit has only the installed commit hooks, and the merge slot's refresh/bar/merge sequence never runs. Name the bar that attests an approval commit made this way. |
| Semantic aftermath | The amendment prompt stops after CLARITY without updating the snapshot, and directs an authorized MEANING re-anchor while Status stays Approved. `trace.reattest_model` detects post-approval drift from the snapshot, not a Modified status. The repaired path must preserve judgments and mechanically advance accepted equivalent wording, while changed meaning requires the owner's ID-use impact review. |

These mechanisms are reusable. The correction is to their ownership and
ordering, not a reason to replace mechanical drift detection or discard
valid implementation work. The existing exclusivity machinery needs an
end-to-end check that the spine window stays held until its judgment and
approval effects settle, including across coordinator restarts.

## Retained adjudicator context

**Cross-WI retention has not landed.** `adjudicator_session.py` and the
`[adjudicator]` configuration table are absent from the current runtime.
`agent_loop.family_context_telemetry` reports provider session metadata but
does not resume a conversation. Restoration is queued in
[WI-551](../work/queued/WI-551-re-land-the-adjudicator-sessio.md), followed by
[WI-541's on-box verification](../work/queued/WI-541-verify-retention-layer.md).
Consequently the current control runs did not deliver the intended continuity,
and this audit found no active retained conversation for parallel WIs to race.

The [preserved patch](../work/handback/wi-540-adjudicator-retention-layer.patch)
needs correction before restoration, based on a static read of its source
diffs, not a claim that it was enabled or exercised here:

- `adjudicator_session.store_dir(root)` and `adjudicator_home_root(root)` use
  the caller's root. Launch and bookkeeping receive the WI worktree root.
  A later WI in a different worktree therefore misses the prior record by
  default. The CLI-home override alone does not move the session-record store.
- The dispatcher's optional `_keepwarm_tick` reads the primary root's store
  and can run while its lane subprocess is active. Merely centralizing the
  store would expose overlapping resume calls: the ping has no exclusion for
  a session already in use. Both calls must pass through the same serial
  owner, including their transcript and bookkeeping updates. An atomic JSON
  replacement does not serialize provider conversation use.
- Retention is selected by adjudication brief class and provider route;
  ordinary worker reviews do not acquire it through that selection. Preserve
  that role separation and per-route identity when moving session ownership
  to trunk. A retained adjudicator must not become its own independent reviewer.
- WI-551 currently combines runtime restoration with spine amendments and is
  classified ordinary. Reconcile that assignment into the required exclusive
  spine work and subsequent implementation before admitting it; “re-land the
  patch” is not sufficient under the clarified work-type rule.

The intended context flow is:

```mermaid
sequenceDiagram
    participant T as Trunk coordinator: sole session owner
    participant A as Retained adjudicator conversation per route
    participant W as Separate worktree
    T->>A: Exclusive judgment for WI A using trunk evidence
    A-->>T: Decision or handback disposition
    T->>W: Dispatch scoped follow-up with its own worker context
    W-->>T: Return outcome and evidence through integration
    T->>A: Resume same conversation for WI B or returned chain
    A-->>T: Judgment
    Note over T,A: One invocation at a time; optional keep-warm uses the same owner
    Note over T,W: Spine authoring is exclusive; workers never write approved snapshots
```

Verify this with outcomes from two distinct WI worktrees and the same eligible
route: both adjudications run in the primary checkout, and the second resumes
the first conversation while ordinary reviewers remain separate. Exercise an
active judgment plus a due keep-warm tick, a
restart, and the existing reset policy. Keep-warm must not resume an in-use
session, and reset must not be mistaken for withdrawal of recorded approvals.
This is a retention acceptance check, not a new requirement staleness gate.

The repair plan remains paused. This documentation neither restores the patch
nor launches the coordinator, and it approves no disputed requirement cells.
