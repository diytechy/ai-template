## 2026-08-02 — WI-408: spec_move stages the working-tree content; the pre-stage workaround is retired

**Summary.** The WI-393 module's first field defect, driven live at WI-401's
close: the worker filled the spec's `## Deliverable` (an unstaged working-tree
edit) and ran `spec_move.py` for the close move — `git mv` moves the working
file but stages the rename FROM THE INDEX, so the staged destination blob was
the stale pre-edit content and the Deliverable silently vanished from the
close commit (caught only because rename-similarity read 100% where the edit
should have lowered it; repaired by amending). The move now stages the
WORKING-TREE content of the source, so an unstaged edit rides the move instead
of vanishing. Riding along, WI-401 REVIEW-A findings 1–3 (record-grade), all
taken.

**Deliverables.**

- **The staging fix** (`project-trajectory/scripts/spec_move.py`,
  `_place_moved_file`): both arms now end with `git add` on the destination.
  The `new_text` arm always did; the `git mv` arm gains it, and that add is
  the fix — after `git mv` the working tree at the destination already carries
  the unstaged edit, so re-adding the destination stages exactly the
  working-tree bytes. The fallback plain-rename arm shares the same tail, so
  the two arms now behave identically (a no-op outside a repo, per the
  ritual's existing contract). The test drives the exact field shape
  (`tests/test_spec_move.py::test_the_move_stages_the_working_tree_content_not_the_stale_index_blob`):
  a committed spec with NO rewritable links — so the rebase half cannot mask
  the defect by re-adding the destination as one of its own rewrites, the
  WI-401 spec shape — an unstaged `## Deliverable` appended, `move_spec`, then
  `git show :dest` must carry the edit and equal the on-disk file
  byte-for-byte.
- **WORKAROUND RETIRED.** Every close since WI-401 carried the worker-brief
  SHARP EDGE "stage the spec before spec_move". That workaround is retired:
  an unstaged-edit close now works without the pre-stage, and this WI's own
  close was performed exactly that way — Deliverable written, left unstaged,
  moved with the fixed ritual — as the dogfood proof (staged blob verified to
  carry the Deliverable before the close commit).
- **The scrape pin** (REVIEW-A finding 2): the SN id-universe scrape — the
  third SN policy duplicate in the derive_gate/trace pair, and the one the
  WI-401 "both surfaces read the same state" promise rested on with no pin —
  is extracted to a named twin `sn_all_ids` in BOTH files (the F5 shape) and
  pinned equal by `tests/test_rule_sync.py::test_sn_all_ids_agrees` across
  prose mentions, table rows, draft sections, `-000` placeholders and empty
  text, exactly like its `sn_draft_ids`/`sn_cited_ids` siblings. The
  downstream sharp edge is now a doc sentence in
  `docs/registry-machinery-reference.md` §2.1: the scrape is whole-text, so
  an SN id mentioned only in ratified PROSE and cited by no SR caps the
  derived gate at G0 exactly as an uncovered table row does.
- **The exhibit correction** (finding 1): the §8.3 `docs/gate` exhibit now
  quotes the cache of the tree it claims — `LLR=130 TC=127` under the same
  `as-of d35c3b93` stamp (the shipped counts were captured mid-WI, before
  WI-401's own registration rows landed).
- **The `uncovered=` softening** (finding 3): §8.3 and the `compute()`
  comment in `derive_gate.py` no longer state the count as always "behind the
  coverage rung's G0 cap" — with zero real SRs the vacuous-G1 branch returns
  before the rung runs, so a requirements-drafting repo legitimately shows
  `uncovered>0` with nothing capped, and the count staying visible there is
  called out as deliberate.

**Judgment calls / deviations.** (1) Registration Class B: a defect fix
inside the shipped `spec_move` behavior plus doc-precision riders — no new
LLR/TC rows owed; the new tests land beside the module's existing evidence.
(2) `trace.py` size ratchet re-stamped 2919 → 2930 (+11, the `sn_all_ids`
docstring recording the sharp edge), reason in the baseline comment.
<!-- fig: derived="len(text.splitlines()) at d1dfb07d, the ratchet's own metric (tests/test_module_size_ratchet.py)" -->
(3) Dupes census: one new spine-loader block (`5d6159709c2c`, the sn_all_ids
body run), count 20 → 21, recorded with reason in `docs/dupes-allow`.
(4) `check_docs --stale` reports 4 broken links in three old
`docs/work/complete/` specs (WI-070/WI-173/WI-288) — measured identical with
this WI's changes stashed, files last touched by WI-384 — pre-existing at
claim, not chargeable here and not repaired (out of scope).

**Byte budgets:** AGENTS.template.md / PROCESS.md / PROCESS_OPTIONS.md all
untouched.

**Watched, measured on the work commit d1dfb07d (clean tree):** red first —
2 failed on the pre-fix tree: the staged-blob test reproducing the defect
verbatim (the staged destination blob held the stale pre-Deliverable
content) and the `sn_all_ids` pin (AttributeError on the trunk-vintage
modules) — then green.
`tests/test_spec_move.py` 17 passed
<!-- fig: cmd="python -m pytest -q tests/test_spec_move.py" rev=d1dfb07d -->
`tests/test_rule_sync.py` + `tests/test_derive_gate.py` 37 passed
<!-- fig: cmd="python -m pytest -q tests/test_rule_sync.py tests/test_derive_gate.py" rev=d1dfb07d -->
smoke tier 623 passed / 6 skipped in 11.68s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=d1dfb07d -->
full suite 1889 passed / 10 skipped in 296.09s (0:04:56)
<!-- fig: cmd="python -m pytest -q -n auto" rev=d1dfb07d -->
`check_dupes` OK — no duplicate blocks in 49 file(s); `ruff check` + format
clean on every changed file; `check_trajectory` / `check_doc_refs` /
`check_figures` rc=0 under `--strict` (residual WARNs are the pre-existing
connectivity and WI-389/390 SpecRef-clock ones).
