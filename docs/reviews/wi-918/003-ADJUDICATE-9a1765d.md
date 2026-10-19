# WI-918 adjudication 003: amendment of SR-209, LLR-248 and TC-242

I judged the three amended rows at `9a1765dfb`. Every amended approved cell keeps its approved text verbatim and adds to it. The SR, LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **The window arms:** the eight `tests/test_loop_provenance.py` tests the arms map names all exist.
- **The launcher test:** it is `tests/test_overnight_legs_git.py::test_check_lane_reads_a_reclaim_as_the_merge_slot_does`.
- **TC-242's citations:** its `Evidence` names `tests/test_loop_provenance.py` and `tests/test_pre_commit_hook.py` only, and its `Verifies` names SR-209, LLR-247, LLR-248, IF-194 and IF-197.

## amendment

- [MEANING+BLESS] SR-209 AcceptanceCriteria -> at the merge, every commit of a loop lane from its claim or first marked loop-writer commit on must carry the trailer -> the same, plus an attended re-claim (a commit with one parent and an unchanged tree, naming that lane in the re-claim form, with no provenance trailer) ends the loop's window for the commits after it; a commit failing any of those conditions is judged like any other; a later loop-writer commit re-opens the window -> a new exemption, so a person's unmarked commit after a re-claim, refused before, now passes the rung. **Blessed.**
  - **Upward,** the Requirement already bounds the rule to "a lane the loop owns from the point the loop took that lane over". The re-claim is the observable point at which the loop stops owning the lane, so the AC now makes that bound measurable.
  - **It is closed:** four conditions, each checkable, with anything else judged like any other commit.
  - **It is not a plausible escape** under PROCESS.md §6. A loop-started process cannot make a trailerless commit through the hook. Reaching the merge with one needs `--no-verify` or plumbing, which are forbidden hand acts.
  - **No file is named.**
- [MEANING+BLESS] LLR-248 Detail -> the writers carry the trailer, the hook and merge ladder check it, a lane's ownership is read from its claim or loop-writer commits, and commits before the first marked loop-writer commit are exempt from this rung -> it adds: lane commits are read oldest first with parents and trees, and each outside parent is read for its tree; the window opens at a loop claim or marked loop-writer commit and closes at an attended re-claim with exactly one parent, the same tree, this branch's exact re-claim subject and no trailer; a re-claim met while closed changes nothing; the commits after a re-claim are exempt from this rung until a marked loop-writer commit re-opens it; a lane never marked has no window; one composer makes the re-claim subject for the procedure and the reader -> the mechanism and its new exemption. **Blessed.**
  - It decomposes SR-209's new clause exactly.
  - "From this rung" keeps the held-status rung unaffected, and TC-242 pins that.
  - The single composer prevents the procedure and the reader from drifting.
  - It adds no carrier name beyond those the approved cell already held.
- [MEANING] TC-242 Expected and Method -> verify the trailer helpers, the marker, the hook, the merge-ladder judgement and the writers -> it adds the SR-209 re-claim clause to Expected, and to Method the re-claim cases plus "The coordinator's overnight launcher's lane check reads a re-claimed lane exactly as the merge ladder's trailer rung does" -> new verification obligations. **Not blessed**, for the last sentence only. Every re-claim case before it is sound, and each has a named, existing test in a file the Evidence cites.
  - **The launcher sentence claims a verification the row's Evidence does not carry.** Its only test is in `tests/test_overnight_legs_git.py`, a file the Evidence cell does not name. That is a TC claiming more than its cited evidence shows.
  - **No row TC-242 verifies states that obligation.** The arms map traces it to the spec's Done-when and this repository's own, unshipped coordinator tooling, not to SR-209, LLR-248 or the interfaces TC-242 verifies.
  - **A TC whose method tests an obligation no verified row makes, with unnamed evidence, is the unattested claim this rung exists to keep out of the record.**

VERDICT: MEANING rows=3

**For the later act turn:**
- **Re-attest:** SR-209 and LLR-248 are marked `[MEANING+BLESS]` on a released rung.
- **Not re-anchored:** TC-242 is marked plain `[MEANING]` and is returned through the draft below. It is the only drifted row in its registry, so the SR and LLR copies are not held by it.

**On the coordinator's question:** return TC-242. The better of the two fixes is to remove the method sentence, because the launcher check is this repository's coordinator tooling and a spec Done-when item, already pinned by its own test. Naming the test file in Evidence alone would still leave TC-242 verifying an obligation none of its rows states.

## Dispositions answered in the lane (sitting 004 blessed the reworked TC-242)

```toml
title = "WI-918 spine rework: TC-242's method claims only what its evidence and rows carry (answer checkpoint 003)"
workstream = "process"
sr_refs = ["SR-209"]
needs = ["WI-918"]
safety_class = "ordinary"
buildtier = "medium"
```

Spine text only; no code change is called for.

1. Remove the sentence "The coordinator's overnight launcher's lane check reads a re-claimed lane exactly as the merge ladder's trailer rung does" from TC-242's Method. The launcher check stays pinned by `tests/test_overnight_legs_git.py`, as evidence for the spec's Done-when in the lane's log.
2. The alternative, if the launcher's reading should be a traced obligation: state it in a row TC-242 verifies (or in its own row), and name `tests/test_overnight_legs_git.py` in TC-242's Evidence.
3. Re-sit TC-242 alone. SR-209 and LLR-248 are blessed here.

SITTING: JUDGED kinds=amendment
