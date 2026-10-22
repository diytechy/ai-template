# WI-902 adjudication 011: dispute on review 010

Range: `cfd357930..7768b93f2`. The code is unchanged at HEAD `a54bf4dc5`, which adds only the review and the findings file. Scope bound: project-trajectory/PROCESS.md §6 "Review threat model". Only finding DC (review 010 F1) is before me. The coordinator sent it here as the third round of the replay-eligibility class, not because anyone contests the merits. F2 (lossy blob decode) and F3 (the checkpoint note) are not before me.

## Finding DC: in a shallow clone, the boundary commit is taken as the landing

**What the code does.** `_landing_commit` (`intake.py:1837-1853`) runs `git rev-list --first-parent --reverse HEAD -- <both complete/ paths>` and takes the first SHA as the commit that landed the disposition. `_merged_dispositions` then judges the adoption in that commit's tree, and treats only "no SHA" as unknown (`_UNLANDED`).

In a shallow repository, git treats the shallow boundary as a root. A root touches every path in its tree, so whenever the true landing lies beyond the depth window, the boundary is the "oldest touch". The adoption is then judged in a tree that is not the landing tree.

**Reproduction.** I ran it myself, outside this worktree, with `tests/test_intake.py`'s real-git constructors and the actual bare `_sweep`. The repository was made shallow the way git records it: the boundary SHA in the file `git rev-parse --git-path shallow` names, after which `git rev-parse --is-shallow-repository` answers `true`.

1. **An accepted adoption is overturned.** The adoption of a queued WI-020 is accepted at landing. WI-020 then completes normally.
   - On full history, `_landing_commit` returns the true landing (`6b4a86c024`) and the sweep exits 0.
   - With HEAD made the shallow boundary, `_landing_commit` returns HEAD itself (`19a2f10d0a`). The sweep judges the adoption against a tree where WI-020 is complete, refuses with "names no open row", and exits 1.

   That is a false refusal of an adoption that was valid at landing, with no reopened row involved.
2. **A refused adoption is accepted.** The landing refuses the adoption of a cancelled WI-020, and the full-history replay keeps refusing (exit 1, WI-021 still needs WI-005).
   - Once the boundary sits at a later commit whose tree shows WI-020 open, the same bare sweep exits 0 and prints `re-pointed queued/WI-021-waiter.md's edge(s) WI-005 -> WI-020`.

   My probe got the open state by hand-moving the terminal spec back to `queued/`. The reviewer's probe reached the same overturn under a newer open-state snapshot. Either way, the verdict tracks whatever tree the window happens to start at, not the landing.

Ruling 009 asked for replay to reproduce the landing verdict. This misreading breaks that in both directions, and it contradicts the round's own rule that an unknown landing refuses.

**Scope.** This is not a contrived host. A shallow repository is ordinary, native git state (`git clone --depth N`, the default of most CI checkouts). The reviewer wrote the shallow file directly only because `clone --depth` hit a Windows environment limit, and the state is identical. The kit already treats shallow history as a supported configuration that refuses rather than guesses:
- `baseline_snapshot._shallow_commits`, with its "history too shallow" refusal;
- the ruling-sync reader in `acceptance_record.py`, which refuses an unreadable shallow parent by name (TC-313: "a shallow boundary is judged from the commit object's parent, never read as a root commit").

That makes this "supported configurations" under §6, not a tampered environment.

**Worth.** The fix is small and changes no contract:
- **The landing reader answers "unknown" when its oldest touch is a shallow-boundary commit.** The sweep then gives the `_UNLANDED` refusal it already has (exit 1, nothing minted), as IF-244's refusal contract and the spec's unknown-landing rule require. A genuine root commit in a full repository remains a real landing.
- **The shallow set should come from one shared reader**, not a second copy beside `baseline_snapshot._shallow_commits`.
- **One regression on a real shallow repository**, plus the LLR-335/TC-360 wording at the declared spine checkpoint, which F3 already owes.

With that change, incomplete history becomes "unknown" rather than an eligible SHA, so this class closes structurally instead of round by round. ESCALATE does not apply: the approved spine and ruling 009 already settle the question, and the coordinator does not contest it.

RULING: DC FIX _landing_commit takes the oldest visible path-touch as the landing even when it is a shallow-boundary commit (git reads it as a root), so a shallow repository judges the adoption in the wrong tree: reproduced, an accepted adoption flips to exit 1 and a refused one to exit 0 with WI-021 re-pointed; a shallow-boundary result must read as unknown and take the existing _UNLANDED refusal, with a real shallow-repository regression
