# WI-918 adjudication 004: re-sit of TC-242

This re-sits TC-242, which sitting 003 returned, on the text at `58d479938`. Compared with what sitting 003 judged (`9a1765dfb`), the only changed cell is `method`, and the only change is the removed sentence about the coordinator's overnight launcher; the Method now ends at the literal-recipe case. The TC rung is released (`human_approval_through = "DevStg-Boundary"`).

## amendment

- [MEANING+BLESS] TC-242 Expected and Method -> (anchor `96c6ce1dc`) verify the trailer helpers, the marker, the hook, the merge-ladder judgement of loop lanes and the writers -> it adds the SR-209 re-claim clause to Expected, and to Method the re-claim cases:
  - a re-claimed lane's later unmarked commit passes, while the same commit before the re-claim is refused;
  - a lane marked by telemetry is judged from that mark and cleared by a later re-claim;
  - a trailer-carrying or other-branch re-claim is not one;
  - a tree-changing or two-parent exact-subject commit neither closes the window nor escapes refusal;
  - a marked loop-writer commit re-opens the window;
  - a never-marked lane stays a person's, and the held-status rung judges a re-claimed lane whole;
  - a literal recipe subject reads as a composed one.

  -> new verification obligations. **Blessed.** Sitting 003's single finding is answered:
  - **The launcher sentence is gone,** so the Method now claims only what its cited evidence (`tests/test_loop_provenance.py`, `tests/test_pre_commit_hook.py`) carries and what its verified rows state.
  - **Every remaining case decomposes** SR-209's re-claim clause and LLR-248's window mechanism, both blessed at sitting 003, and each has a named, existing test in a cited file.
  - **The held-status case** verifies LLR-248's "exempt from this rung" scope.

VERDICT: MEANING rows=1

**For the later act turn:** TC-242 is marked `[MEANING+BLESS]` on a released rung, so the act turn re-attests it. No row is held, and no row is returned.

SITTING: JUDGED kinds=amendment
