Deferred open items: OI-98

## 2026-10-04 — wave 11 coordinator (unattended): WI-791 lands; WI-788's design note reaches its checkpoint

Resumed from [the wave-11 handoff](../handoff-2026-10-04-wave11-coordinator.md),
unattended under the owner's written session authorization. Roles (owner,
2026-10-04): Claude Opus builds and plans (`kit-builder`, medium); GPT Terra
(`gpt-5.6-terra`, medium) authors spine rows; Codex 6.1 Sol (`gpt-6.1-sol`,
high) reviews code; independent Opus sessions adjudicate. Reviews for this wave:
[reviews/2026-10-04-wave11/](../reviews/2026-10-04-wave11/). The coordinator's
own calls: [decisions/coordinator-2026-10-04.toml](../decisions/coordinator-2026-10-04.toml).

### Claims under scoped unpauses

WI-791 and WI-788 were each claimed through `integrate.py claim` between a
pause-deletion commit and a byte-identical restore (sha256 `b0a709c8...`).

The first deletion commit was refused by the pre-commit hook (`open-items.html`
stale: the owner surface shows the pause), but `integrate.py claim` then ran and
CLAIMED, because it reads the pause file in the working tree, where the staged
deletion had already removed it, not in HEAD's tree. The claim commit sat on a
HEAD that still tracked the pause. The coordinator reset its unpushed local
commits to `423ec57c`, deleted the orphan branch, and redid deletion, claim and
restore in the authorized order (coordinator decision D-002). Kit finding, not
filed: the claim's pause check should read the committed trunk tree.

### WI-791 (OI-100): amended needs reach the meaning-or-clarity adjudication

Claimed on `wi-791` (`484b411c`) and landed by squash; the lane tip is in
`archive/lanes`.

- **Build** (Opus builder): the amendment walk reads the approval-act set
  (SR, LLR, TC, SN, DA, SUR), so an amended need, assumption or surrogate mints
  one amendment row; the held-rung CLARITY arm (`reattest`); an act names its
  verdict; the merge slot refuses a held-rung re-attestation the verdict does
  not rule CLARITY; PROCESS.md §4's one stated case (+429 bytes, watched); the
  owner surface's audit list; a RESYNC entry. Departure, recorded (D-005): the
  brief had to change, against OI-100's "the brief is unchanged".
- **Spine** (GPT Terra): new SR-228 and 19 amended rows, then two cell fix
  rounds. Terra's `apply_patch` fails on the registries' long single-line cells
  ("Failed to find expected lines"); a guarded Python replace works.
- **Sol round 1** (`523d576a`): 3 MAJOR, 2 MINOR, all confirmed. The worst: the
  merge slot read the held rung's dial at the lane's fork point, before its own
  refresh, so a rung the owner held after the fork read as released.
- **In-lane adjudication** (independent Opus, S11): three rounds, the bound. Round
  1 returned six rows and SR-228 (LLR-153 and LLR-158 had lost clauses the code
  still keeps; tests missing for two SR-228 clauses); round 2 returned two rows for
  untested clauses; round 3 settled all fourteen. Mutation probes: 14 in round 1
  (5 survived), 7 in round 2 (4 survived); every survivor is now killed. **Act seq
  29** (`38709c82`): SR-228 approved; SR-178, LLR-118, LLR-153, LLR-158, LLR-167,
  LLR-245, LLR-271, LLR-278, TC-123, TC-147, TC-153, TC-161, TC-240 and TC-278
  re-attested.
- **Sol final review** of the post-act tree: no BLOCKER or MAJOR; two MINORs
  (a relative verdict path escaped the repository; a test blind to half its
  rendering) fixed in `2eaa8ebd`, re-checked SOUND.
- **Sessions:** 1 builder (resumed 4 times), 1 Terra session (resumed 4 times),
  1 adjudicator (resumed twice), 3 Sol sessions. No row minted for a round.
- **Follow-up, not filed:** an in-lane act never reaches the merge slot's
  `held_reattest_refusal` (it runs only for all-adjudication lanes), so on a held
  rung an in-lane re-attestation would not meet SR-228's refusal. It belongs to
  WI-788's in-lane sitting (`S788-sitting`).
