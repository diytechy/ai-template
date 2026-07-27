# 125-REVIEW-A — adversarial review of the 13 requirement splits

**Trigger:** WI-328's own Done-when. The WI split 13 compound system requirements
into 28 rows; a self-review is the weakest possible basis for the signature that
follows, and the immediately preceding review of a smaller prose change found 7
real defects including two BLOCKERs.

**Critic:** a fresh **OpenAI/`codex`** session at the strong tier
(`gpt-5.6-sol`) — family-heterogeneous, since the editor was Claude/Anthropic.
Gateway probed live first (a one-token `PONG`) rather than planned around: the
OpenCode route has died mid-session twice before. The sandbox held **only** the
13 BEFORE/AFTER pairs and the invariant being claimed — no repo, no commit
messages, no spec, no rationale for the change, no self-assessment.

**The claim under test:** *the split PARTITIONS the obligations — it does not
add, drop, weaken, widen or otherwise alter any of them.*

**Verdict:** `CHANGES-REQUESTED findings=6` over 4 pairs; 9 pairs returned `OK`
with their obligation inventories stated.

**Disposition: 6 confirmed, 6 fixed. Plus 3 more the critic missed.**

---

## Confirmed and fixed — the critic's six

Two are genuine losses. Four are the opposite failure and the more interesting
one: **scope creep introduced while "improving" a row.** Splitting invited
tightening, and tightening a `Verified` row's acceptance criteria mid-attestation
is a change the owner never agreed to.

### F1 BLOCKER · `SR-057` · DROPPED — "never from prose"

*"…from the tracked WI registry plus dispatcher reservations **— never from
prose —** excluding…"* The prohibition is the point of the requirement: it is
what retired the hand-curated pointer file. The rewrite kept the positive input
list and dropped the negative constraint. **Fixed:** restored verbatim.

The critic's reasoning is worth preserving: *"Mentioning the problem in a
rationale does not preserve a normative requirement."*

### F2 BLOCKER · `SR-059` · DROPPED — a list member

*"gate-first**/check** logic"* → *"gate-first logic"*. A silently lost member of
an enumerated removal list. **Fixed.**

### F3 BLOCKER · `SR-057` · ADDED — reason codes widened to a fifth class

The BEFORE requirement excluded five classes and its acceptance criterion
attached the reason-code obligation to **four**, omitting protected-conflicting.
The rewrite moved *"with a reason code"* into the requirement, silently binding
all five. **Fixed:** the reason-code obligation stays in the AC at its original
scope.

### F4 BLOCKER · `SR-112` · ADDED — orphan-copy severity

*"an orphan copy warns without failing"* is real system behavior, but it lived at
the `LLR` layer and was never an `SR` acceptance condition. Promoting it into a
new SR's AC widened the attested surface. **Fixed:** reverted to the BEFORE
scope. The behavior remains where it always was.

### F5 BLOCKER · `SR-113` · ADDED — an implementation narrowing

*"core.hooksPath points at the kit's hooks"* prescribes a specific hooks
directory where BEFORE required only that the floor be active. **Fixed.**

### F6 BLOCKER · `SR-035` · ADDED — an invented acceptance condition

*"concrete harness commands are marked as a swappable reference rather than a
requirement"* is a real principle of this kit, but it was not an acceptance
condition of this row and the editor introduced it. **Fixed.**

---

## Found by the word-level delta, not by the critic

A second instrument — a normalised BEFORE-vs-AFTER vocabulary diff over
`Requirement` + `AcceptanceCriteria` for all 13 splits — run precisely because
the previous review recorded that one instrument was *"necessary and not
sufficient"*. It surfaced 28 candidate losses, of which most are stemming
artifacts (`wires`/`wire`, `reserves`/`reserve`, `hard-gating`/`hard-gate`) and
**three are real**:

- **`SR-115`** — *"shall order eligible traincars **deterministically** by…"*.
  The adverb is the normative content; determinism was left implied by the title
  and the AC. Restored.
- **`SR-122`** — *"excluded from **stamp-only** comparisons"* became *"excluded
  from the comparison"*, widening the exclusion from stamp-only diffs to every
  comparison. Restored.
- **`SR-114`** — *"language/**stdlib** guarantee"* and the parenthetical *"(3.11
  has arm64 macOS builds)"*, which is what makes *"not a runner-availability
  workaround"* checkable rather than merely asserted. Restored.

Two instruments, **disjoint finding sets**, for the second consecutive review.
That is now a pattern rather than an anecdote: the critic reads for meaning and
misses vocabulary; the delta reads vocabulary and cannot judge meaning.

---

## What the critic checked and cleared

It stated an obligation inventory per pair and cleared 9, including the hardest
one — `SR-062`, split four ways across continuation conditions, build/review
shape, release-on-early-end and blocked-constituent disposition. It swept
explicitly for changed actors, changed thresholds, conditional-to-unconditional
flips, other enumerated-list mutations, and orphaned acceptance conditions, and
reported none beyond the six above.

On the secondary question it cleared **every** rewritten `Rationale` against the
new contract: each supplies a consequence-if-absent and a genuine rejected
alternative, without requiring project-history lookup.

---

## The transferable lesson

The previous review's defects were **things left behind** when text was removed.
This review's were the mirror image: **things added** when text was rewritten.
Four of six findings are the editor improving rows that nobody asked to improve,
inside a window where a human is signing them.

A split is a partition. When the temptation is to also fix what you notice while
partitioning, that is a separate work item — and saying so is the whole reason
this repo files rather than escalates.
