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

### WI-790 (OI-102): work items cite the open items they wait on; Decisions to review

Claimed on `wi-790` (`15874031`) after WI-791 landed (both touch `intake.py`), and
landed by squash; the lane tip is in `archive/lanes`.

- **Build** (Opus builder): the `OI-###` token in `needs` is the one edge, and every
  `wi_refs` reader is deleted; one queue projection feeds the owner surface, the
  status snapshot and the uncited-pending ERROR; the commit-time sync rule (a
  commit against its parent, at the hook and per lane commit at the merge slot);
  blocked, not waiting; placeholders on every open-item creation path; "Decisions
  to review" at the bottom of `open-items.html` with the `reviewed` key; OI-98's
  `wi_refs` moved into WI-684's `needs`. The shipped template's OI-1/OI-2 went, and
  two slow-tier trace fixtures that leaned on them now file their own row.
- **Spine** (GPT Terra): new LLR-298, LLR-299, TC-313, TC-314; LLR-289 and TC-302
  retired with records; about twenty-five rows amended. One scripted edit turned
  IF-073's `consumers` list into a string; the smoke tier caught it.
- **Sol round 1** (`9c39bab2`): 5 MAJOR, 3 MINOR, all confirmed. The worst: the
  sync rule read a ruling commit at a shallow boundary as a root commit and passed
  it; the CSV carrier bypassed it; the claim-time comparator discarded an added
  criterion carrying a path.
- **The full unfiltered suite** on `9c39bab2`, from a detached worktree with a fixed
  basetemp: 5030 passed, 17 skipped, 0 failed, in 2140.8 s on a loaded box.
- **In-lane adjudication** (independent Opus): round 1 returned all sixteen rows
  (blessing the two retirements). The authored cells had replaced lists of cases
  with "the existing cases hold", dropped clauses the code keeps, and claimed
  untested behaviour; 12 of 45 mutation probes survived. Round 2 settled every row
  (44 of 45 caught; I3, a narrower variant of the old join, noted). **Act seq 30**
  (`6f67736b`): LLR-298, LLR-299, TC-313 and TC-314 approved; SR-225, LLR-010,
  LLR-058, LLR-118, LLR-153, LLR-283, LLR-288, TC-010, TC-123, TC-147, TC-293,
  TC-301 and the two retirements re-attested.
- **Sol final review** of the post-act tree: one MAJOR (an unreadable listed parent
  blob read as absent, a partial clone offline reaches it) fixed in `59215dca` with
  one reader that refuses by name; IF-073's specref clause corrected. Re-check:
  SOUND. The builder folded the new cases into the existing TC-313 test rather
  than raise the smoke tier's membership budget.
- **Sessions:** 1 builder (resumed 5 times), 1 Terra session (resumed 5 times), 1
  adjudicator (resumed once), 3 Sol sessions, 1 full suite.
- **Follow-ups, not filed:** IF-073's consumers and notes are slightly off; no SR
  states the coupling between owner decisions and the work items that cite them
  (LLR-298/299 sit under SR-148); LLR-198's detail does not describe
  `open_item_queue`; a refresh merge that brings in a trunk ruling of an item cited
  only by a lane-side row must itself carry the citer's update, or it is refused
  for good, and the lane workflow should say so.

### WI-788 half 1: the design note reaches the owner's checkpoint

Claimed on `wi-788` (`c3be7be0`) and drafted alongside the builds, as the order
of work allowed (docs only).

- **Drafting:** four Claude Opus planners wrote one chapter each (state, evidence
  and recovery; sessions, routing and accounts; planning and tiering;
  adjudication, mint and landing authority), and an Opus integrator wrote the
  index: what the note decides, every binding input mapped to where it is
  settled, 26 stated changes to existing rulings, the glossary draft, one
  amend/preserve/retire matrix, one graph of twenty `S788-*` successor rows, and
  the owner's questions.
- **Probes** (authorized): claude 2.1.289 and codex 0.160.0 resume a session by id
  from another directory; opencode 1.18.30 runs the turn and then hangs unless
  given `--dir <session dir>`. FreeLLMAPI was probed only as an OpenCode custom
  provider config; the end-to-end call waits on the owner's endpoint (Q-4).
- **Findings from the record:** eight recorded dual-plan rounds (DP-001 here,
  seven in the downstream gilbert repo), every one with the two arbiter runs
  agreeing and nothing ported; 71% of 48 loop lanes failed their first review;
  75 of 77 closes since 2026-09-28 carry no decisions record (accepted as
  history, since a backfill would fabricate disclosures).
- **Codex 6.1 Sol** rated `e3754af6` NOT YET READY (5 BLOCKER, 7 MAJOR, 3 MINOR).
  The integrator confirmed 14, partly refuted one, and turned two into owner
  questions (Q-8 and Q-11 are collisions between the owner's own rulings).
- **An independent Opus adjudicator** ruled the three disputed points (all three
  amended, applied verbatim) and checked the five blockers resolved.
- **The checkpoint:** OI-104, with the queued placeholder WI-794 (filed after
  WI-790 landed, the new way). The note stays on its lane; WI-788 stays claimed;
  no successor row is filed. Its decisions record is
  `docs/decisions/wi-788.toml` on the lane (31 entries).

### Session close

Stopped because no row on the frontier can move without the owner: WI-788 waits
on OI-104, WI-684 on OI-98, WI-794 is OI-104's placeholder, and WI-625 is deferred.
The resume map is
[handoff-2026-10-04-wave12-coordinator.md](../handoff-2026-10-04-wave12-coordinator.md),
which lists every delegated decision for review, high risk first.

- **Approval acts:** seq 29 (WI-791) and 30 (WI-790), both taken in their lanes.
- **The full unfiltered suite** on trunk at `b0e7a6f2` (the session close), from a
  detached worktree with a fixed basetemp: 5046 passed, 17 skipped, 0 failed, in
  2015.2 s (about 3.5 times 2026-10-03's 9.5 min, cause not claimed).
- **Sol sessions:** 7 (one note review, two lane reviews, two final reviews, two
  narrow re-checks), with no rate limit reached.
- **Kit findings, not filed:**
  - The claim reads the working tree's pause file, not HEAD's.
  - An in-lane act never meets the merge slot's held-rung re-attestation refusal.
  - A refresh merge that brings in a trunk ruling of an item cited only by a
    lane-side row must itself carry the citer's update, or it is refused for good.
  - IF-073's consumers and notes are slightly off, and LLR-198's detail does not
    describe `open_item_queue`.
  - No SR states the coupling between owner decisions and the rows citing them.
