# Repaired approval control — stopped on correctness, 2026-09-07

The supervised retry is stopped. The tracked pause is restored and every owned
coordinator/provider process group was verified absent. Do not run the launcher:
a pending primary selection takes precedence over the pause. This record is the
continuation authority after the [fresh preflight](CONTROL-APPROVAL-PREFLIGHT.md).
No further control window, replacement selection, or merge/push is implied.

## Frozen configuration and actual segment

Repair: `0f106ce9c1e13a5f86b744311d649a4f69df32f2`.
Hooks-enabled pause-removal launch: `b830f202c551c7c11d1a63ea4baff84a7ff6e596`.
The final read-only setup proof was clean, selected WI-605 first through normal
admission, and composed the exact amendment prompt. Runtime, prompts, policy,
stack and enabled routes were unchanged from the verified repair. Retention
remained absent and excluded.

The root `./agent-resume.sh` started at `2026-09-07T09:09:15.781350+00:00`,
launcher PID 76491. Normal dispatch selected WI-605 on primary at
`65eda1bff8ec37a2594f2d205e12569df350663d`, without a claim branch or new
worktree. Its immutable turn binds the frozen launch base, proposal blob
`9e5967174d0e38727273e1d31a34c7bf4c8d167d`, and exactly SR-161, LLR-183,
TC-178. The supervisor ran the normal read-only validator successfully against
the selected clean checkout.

The supervisor sent SIGINT to the owned process groups at
`2026-09-07T09:19:31.599517+00:00` after confirming the candidate-binding
failure below. Launcher exit was -2 at `2026-09-07T09:19:31.941204+00:00`.
All three owned PIDs (76491, 76495, 78772) and their process groups were absent
at the subsequent check; no provider was left running. The checkout was clean
at interruption. Pause recreation and the retention requeue are post-segment
supervisor actions, not measured runtime changes.

This segment used **616.129 active seconds** and completed/integrated **zero
WIs**. Across all three segments the carried total is **3666.384 seconds**,
leaving **39533.616 seconds** of the original twelve-hour allowance. Earlier
segments used local September 6; this segment used local September 7, the
second active date. These are carried observations, not a new allowance. No
coordinator restart occurred.
<!-- fig: derived="out/run-logs/control-retry-approval/launch.json: 616.1287817920092 + prior 3050.2552113749553 = 3666.3839931669645; 43200 - total = 39533.616006833035; stop-state-proof.json records zero terminal/mint/publication changes" rev=79115aab -->

## Attempts, judgment and reported usage

| Attempt | Actual route | Result | Reported usage |
|---|---|---|---|
| 001 | ANTHROPIC-FABLE, claude-fable-5-1, medium effort | ADJUDICATE committed the typed MEANING verdict and an Approval carrier with three RETURN decisions and two continuation drafts | 465 seconds; raw reported USD 5.948853000000001; usage scope unknown |
| 002 | Same configured Fable route | Redundant ADJUDICATE rework started; interrupted before a new committed verdict | No completed coordinator telemetry or final reported cost |

The first invocation is `9eb3f1cc06284cb9bfd41a956c0600b7`, provider session
`074472b9-d7cd-43bf-bfd1-b20b445b1f50`. Its coordinator-written record is
[contract_split-001](../iteration/contract_split-001-20260907-040924.log).
The interrupted provider session is `4a68f249-da9a-4414-a552-544bf7240e59`.
Both provider transcripts are preserved in the ignored segment directory,
with SHA-256 values in its provider-transcript-manifest.json. Missing cost is
not zero; the USD1000 watch remains over reported spend, not an invented
aggregate. Earlier per-call reports stay in the prior observation records.
<!-- fig: derived="committed first-call metadata, out/run-logs/control-retry-approval/launcher.log and provider-transcript-manifest.json" rev=79115aab -->

The first verdict is `be785dcc9cddac3d86a2fa32d5d38f018e04c1a4`; its carrier
commit is `fa90a5b73ead04ee8dfbf151a53eeca5cddf1c86`. It returns the scoped
amendment for the dangling ruling citation and unjudged whole-file absorption
population. Its chain judgments and proposed continuations remain unaccepted
findings. In particular, no supervisor endorsement follows for its direct
TC-178 linkage argument or its successor scopes/classification.

## Confirmed correctness findings

1. **The coordinator cannot validate its own judgment metadata.**
   `session_commit_range` supplies the intentionally abbreviated `head_sha`
   result to `primary_adjudication.session_binding`. That function records it
   unchanged as `candidate = fa90a5b7`. The primary verifier requires a full
   40-hex immutable commit, so it excludes the actual judgment record and
   refuses the carrier's evidence reference. The supervisor reproduced the
   refusal read-only before stopping. The engine had already begun a second
   ADJUDICATE call. The
   [independent candidate audit](../reviews/2026-09-07-control-approval-candidate-luna.md)
   records the caller, full identity, and test gap. Preserve the historical
   metadata; do not edit it retrospectively to manufacture acceptance.
2. **Review routing misses a successor's derived risk class.** The log says
   `adjudication review not owed ... when-minting -> no round`, although a
   continuation draft uses `planmode = dual` and later minting classifies it
   as high-risk. The predicate sees only the raw parsed kinds, before that
   derivation. The [independent review-boundary audit](../reviews/2026-09-07-control-approval-review-boundary-terra.md)
   reproduces the mismatch without changing policy. Zero independent review
   rounds ran in this segment. Fixing only the candidate identity would leave
   this separate review defect exposed.

The stopping intervention was the supervisor's single correctness stop, not a
provider fallback, a policy waiver, or a replacement experiment. No source was
changed inside the measured segment. The prelaunch full and smoke greens are
real evidence; this actual invocation exposed a boundary their fixtures missed.
No post-stop runtime fix is claimed in this record.

## Preserved state and next boundary

Stopped primary HEAD is `79115aab19d4bdb023a14f19f4b7d852cd8db56b`. Its delta
from launch contains only the immutable turn, one verdict, the queued spec's
Approval/Dispositions and the first invocation log. There is no live governing
cell change, Status flip, snapshot registry change, successor mint, terminal
WI or publication commit. The pending selection and candidate remain exactly
as evidence; there is no manufactured completion or rewritten invocation.

The original legacy branch/worktree remains at
`668edaf49896608e48bc6ff3cec014840312476a` and the original forensic patch
remains SHA-256 `995df79351faa234f99054a5a947b892613edffae03c2d1d747c2b24b50238f3`.
The new pending primary selection is a separate preserved incident. A tracked
pause is required after this stop, but its supervisor commit changes the old
turn's candidate surface: do not resume that binding or bypass its validator.
Any later continuation needs explicit supervisor reconciliation of this
preserved candidate under the repaired contract before admission can resume.

WI-551 is re-queued as required, with its separate spine-authoring,
cross-WI ownership and serialized keep-warm prerequisites retained. Its patch
was not applied. WI-596 remains queued with its uncompleted brief/rollup/intake
obligations. Existing WI-601/603/604/606 scopes and dependencies remain.

The owner-authorized [PC package](IMPLEMENTATION.md#pc--the-independently-agreed-cuts-unconditional-after-the-control-window)
is the next package; it is not contingent on this weak control sample. Its
batch-contract authoring/judgment precedes deletion, and the preserved pending
primary turn must be reconciled before any new claimed work can start. The two
runtime findings above are unresolved technical follow-ups, not permission to
silently change PC's scope or start another control window. Replacement and
retirement choices outside PC remain conditional on their own evidence.
