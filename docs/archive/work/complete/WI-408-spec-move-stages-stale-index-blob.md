+++
id = "WI-408"
title = "spec_move stages a stale index blob when the moved file carries unstaged edits (WI-401 builder disclosure + WI-401 REVIEW-A doc-precision items, minted trunk-side at intake per the R3 invariant). THE SHARP EDGE, driven live during WI-401's close: the worker filled the spec's Deliverable (an unstaged working-tree edit) and then ran spec_move.py for the close move - the ritual staged the rename FROM INDEX CONTENT, silently dropping the just-written Deliverable; caught only because git's rename-similarity read 100 percent where the Deliverable should have lowered it, and repaired by amending the close commit. THE FIX: the move must stage the WORKING-TREE content of the source file (stage the file first, or read/write through the filesystem before git add), so an unstaged edit rides the move instead of vanishing; a test drives the exact shape - edit the spec body, run move_spec, assert the destination blob carries the edit. This is the WI-393 module's first field defect and the failure direction is silent content loss at every future close, so it goes first among the quick rows' follow-ups. RIDING ALONG, record-grade (WI-401 REVIEW-A findings 1-3): correct the registry-machinery-reference 8.3 exhibit to the tree it claims (its LLR/TC counts were captured mid-WI under the same as-of stamp); add the one doc sentence on the whole-text SN id scrape (a prose-mentioned ratified SN id caps the gate at G0 - downstream sharp edge, and the scrape duplicate at derive_gate/trace is unpinned by test_rule_sync: pin it); soften the uncovered= phrasing for the vacuous-branch corner (uncovered can be nonzero with nothing capped when zero real SRs exist). Scope: spec_move.py staging fix + test, the rule_sync pin, three doc sentences."
workstream = "scripts"
buildtier = "quick"
safety_class = "ordinary"
+++

## Deliverable

**Built 2026-08-02 (work commit d1dfb07d).** The staging fix shipped and the
three REVIEW-A riders taken.

**The fix.** `spec_move.py::_place_moved_file` now ends BOTH arms with
`git add` on the destination. `git mv` moves the working-tree file but stages
the rename from the INDEX blob, so a source carrying unstaged edits — the
close shape: a just-filled `## Deliverable` — had those edits silently
dropped from the staged copy while the working file kept them; the `git mv`
arm gains the add the `new_text` arm always had, staging the destination's
WORKING-TREE bytes. Driven red-then-green in the exact field shape
(`tests/test_spec_move.py::test_the_move_stages_the_working_tree_content_not_the_stale_index_blob`):
a committed spec with no rewritable links (so the rebase half cannot mask the
defect by re-adding the destination as its own rewrite), an unstaged
Deliverable appended, `move_spec`, then `git show :dest` must carry the edit
and equal the on-disk file byte-for-byte — red on the pre-fix tree with the
stale pre-Deliverable blob reproduced verbatim.

**Dogfood.** THIS close was performed with the fixed ritual and WITHOUT the
pre-stage workaround every close since WI-401 carried (the worker-brief SHARP
EDGE, hereby retired): this Deliverable was written into the working tree,
left unstaged, and the spec moved active/ -> complete/ by `spec_move.py`
itself; the destination's staged blob was then verified to contain this text
before the close commit.

**The riders (WI-401 REVIEW-A findings 1-3).** (1) The
registry-machinery-reference §8.3 exhibit now quotes the cache of the tree it
claims — `LLR=130 TC=127` under the same `as-of d35c3b93` stamp. (2) The SN
id-universe scrape is extracted to a named F5 twin `sn_all_ids` in
derive_gate.py AND trace.py and pinned equal by
`test_rule_sync::test_sn_all_ids_agrees` like its siblings (red first:
AttributeError on the trunk-vintage modules); the whole-text sharp edge — a
prose-mentioned ratified SN id with no citing SR caps the gate at G0 — is a
doc sentence in §2.1. trace.py ratchet re-stamped 2919 -> 2930; dupes census
+1 spine-loader block (5d6159709c2c), 20 -> 21. (3) `uncovered=` phrasing
softened in §8.3 and the `compute()` comment: with zero real SRs the
vacuous-G1 branch returns before the rung runs, so the count can be nonzero
with nothing capped — the requirements-drafting corner, deliberately visible.

**Verification, measured on d1dfb07d (clean tree):** red first — 2 failed on
the pre-fix tree (the staged-blob test, the sn_all_ids pin) — then green:
smoke tier 623 passed / 6 skipped in 11.68s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=d1dfb07d -->
full suite 1889 passed / 10 skipped in 296.09s (0:04:56)
<!-- fig: cmd="python -m pytest -q -n auto" rev=d1dfb07d -->
`tests/test_spec_move.py` 17 passed; `test_rule_sync` + `test_derive_gate`
37 passed; `check_dupes` OK over 49 files; ruff clean. Close verify:
`check_trajectory` / `check_doc_refs` / `check_figures` rc=0 under
`--strict`, `derive_gate --check` rc=0 — totals quoted in the log fragment.
