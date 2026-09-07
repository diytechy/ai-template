## 2026-09-06 — Snapshot-ownership repair: three gaps closed in the plan

Reviewed codex's `98c6dd8a`, `4c26e432` and `1711b214` against the live code.
The audit's findings are sound and its two new ones (the WI-551 patch's
root-relative session store, and the keep-warm tick's lack of exclusion) are
independently confirmed by reading the preserved patch. Three gaps found and
corrected in the plan documents; no code, registry, queue or pause change.

**1. The defect is a mechanical permission, not only a prompt direction.**
The audit located the write at the briefs and `adjudicate_brief._aftermath`,
and cited `lane_approval_refusal` as prohibiting approval acts. That is only
the `False` arm. `integrate._approval_act_refusal` calls `_adjudication_lane`
— true when every claimed spec on the branch declares
`safety_class = "adjudication"` — and hands the flag to
`acceptance_record.merge_approval_refusal`, which then selects
`adjudication_approval_refusal`: flips bounded by the `Adjudicates` cell, and
the snapshot permitted to cover the registries those flips changed. So an
adjudication worktree is mechanically authorized to write `SNAPSHOT_DIR`
today, which is what the WI-605 lane did. Removing the instruction leaves the
door open. Recorded as a second "Snapshot write (permission)" row in
WORK-FLOWS.md's boundary table, and step 3 of the resolution now names the
exception: a rule phrased against "worker-originated" changes is a no-op
against exactly the path that failed.

**2. The ownership boundary is already ruled.** CONTROL-RETRY records the
owner's clarification as new. Owner ruling 2026-09-01 already states it, and
`lane_approval_refusal`'s docstring carries the concurrency argument verbatim:
two lanes touching the spine conflict at merge and the snapshot must not move
across a workstream, whereas a serial trunk-side act cannot conflict. That
ruling assumed a trunk-side act; the adjudication-lane exception landed the
same day with WI-572's first-approval arm and made it a claimed worktree,
removing the guarantee the ruling rested on. WORK-FLOWS.md now says so, so the
repair reads as closing an exception to a standing rule rather than
establishing a new one.

**3. Step 2 restated WI-596's scope.** The absorb clause is that row's
declared scope; step 2 now depends on it and cites its ledger instead.

Blast radius on committed work: none found. Since `1e78ada3` the only commit
touching the snapshot write path, the mirror readers, the merge-slot refusal
or the adjudicate prompts is `a7f57c3f`, made inside the window. OI-85, P9R,
the selector, the guidance and the SN-036 amendment are all outside it. What
is affected is the unmerged WI-605 lane, the two adjudicate prompt templates
and the brief composer.

Standing observation, not corrected here: a withdrawal to a previously
accepted snapshot is not a modeled operation. The mirror invariant can only
read it as a malformed new copy, which is why it refused correctly. The plan's
revised route avoids needing one; if a withdrawal is ever wanted, it is its
own contract.

Deferred open items: none.
