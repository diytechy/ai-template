# WI-958 dispute adjudication: F1 (the gate over 4b36948)

Range: `30e7c02c000cbaecb03e78bd6df01e809bd557ae..4b369488229b9dfb287ed5ac4a1d0ba120cdc813`.
Ruled against PROCESS.md §6 "Review threat model" and the code at this range.

## F1: `out/review-owed` is dirt to the attest preflight under the shipped ignore template

**What holds, observed at this range:**
- The shipped `project-trajectory/gitignore.template` ignores `out/run-logs/`, the two locks and `out/subagent-gate.log`, but not `out/review-owed`. This repository's own `.gitignore` ignores all of `out/`.
- `review_owed_marker` (`agent_loop.py:3125`) puts the marker in the lane worktree's `out/`, and `review_owed_stop` (`:3262`) writes it.
- `integrate._unstaged_dirt` (`:2966`) counts any untracked file git does not ignore. The attest preflight refuses on that dirt, with the cause "holds work the index does not".
- Both `attest_build` (`:2482`) and `review_draw_gate` (`:3397`) call `integrate.attest` and record a refusal as a red.

So the mechanism the finding names is real. If `attest` runs in an adopter's lane while the marker is present, it records a red.

**What does not hold: a supported route never runs `attest` while the marker is present.** The finding's scenario is "a lane resumed after REVIEW-OWED (exit 9) has its owed round refused as a red round even when its bar is green", plus "every later build stays red". Neither follows from the code:

- **The marker is written only over an attested tip.** `review_owed_stop` fires only when `review_draw_failures` reaches the stall limit. A failure is counted by `note_review_draw_failure`, after a review was actually routed. Routing a queued review happens only after `review_draw_gate` returns None, at the top of every iteration (`:3479`), and that requires a verified review attestation at HEAD: either one already there, or one the gate's own green `attest` just wrote. A red at the gate drops the round (`refuse_round`), so no draw is attempted and exit 9 cannot follow. So when exit 9 writes the marker, the lane's tip carries a verified attestation.
- **Nothing between exit 9 and the resume moves the tip off that attestation.** The dispatcher's exit-9 arm (`dispatch.py:649`) parks the lane unchanged, with no refresh, no merge and no decided outcome, and the next cycle resumes it. The failed draws above the attested commit commit only record paths (session logs and telemetry), and the review-attestation walk steps through those. So the resumed worker's `review_draw_gate` finds the attestation and never calls `attest`. The owed round draws, and the marker does not matter.
- **"Every later build stays red" does not follow either.** `complete_review_round` clears the marker as its first act (`:2112`), for every verdict, before CHANGES-REQUESTED routes a rework. So the next build's `attest_build` runs with the marker already gone.

The reviewer's Probe 1 reached the refusal differently: "a green hand build, and an `out/review-owed` marker" placed together. That is an unattested tip carrying the marker. The exit-9 route never leaves that state, because it writes the marker only above an attestation. Under §6, this is ordinary tools put in an order no supported workflow or kit route produces, so it reaches nothing a spec promises.

**The one residual path I found, recorded so it is not lost, and not a ground for FIX.** The attestation search is bounded at 64 commits (LLR-341). A lane parked at exit 9 again and again could, over many resume cycles, pile more than 64 record-only commits above its attested commit. The gate would then call `attest` with the marker present and record a red. That needs a total reviewer outage across every enabled family, sustained for many cycles. It also fails closed: the lane reaches its cap and closes partial with its work kept, rather than landing anything unreviewed. §6 grades such a rare, fail-closed path MINOR at most. It is also no convergence-class defect: it is not a fail-open path, it loses no data, and it leaves no gap in the Done-when.

The reviewer's remedy (ignore `out/review-owed` in the template, with a RESYNC line) is cheap hygiene. The coordinator may take it as a follow-up if it wishes, but a cheap fix does not make the stated scenario reachable.

RULING: F1 DISMISS refuted — exit 9 writes the marker only after the draw gate passed over a verified attestation, the dispatcher parks the lane unchanged, so the resumed gate reads that attestation and never runs attest; and complete_review_round clears the marker before any rework build. The reviewer's probe needed a hand-built unattested tip beside the marker, a state no supported route produces.
