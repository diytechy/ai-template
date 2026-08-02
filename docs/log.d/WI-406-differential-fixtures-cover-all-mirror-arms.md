## 2026-08-02 — WI-406: differential fixtures cover all mirror arms

**Summary.** WI-399 REVIEW-A round-2 finding 4 (advisory), closed as specced —
fixtures only. `check_trajectory._would_be_inventoried` mirrors
`gen_arch_map.build_map`'s emptiness predicate arm by arm, but the shipped
regen_map differential suite drove only the arms its fixtures contained; the
import-only (re-exporting `__init__`), contracts-comment-only and
PARSE-ERROR-stays-inventoried arms were consistent yet unpinned, so a future
edit to either side of the mirror could drift them without a red.

**Deliverables.**

- **Three differential fixtures** (`tests/test_trajectory_arch.py`, WI-406
  section, work commit 29af0fcb), one per unpinned arm, each through the full
  lifecycle: the lane reds on the untagged module BEFORE any regeneration (the
  mirror keeps it), a REAL `gen_arch_map` regen absorbs it and the delta
  empties — a mirror-only keep would be a permanent lane red here — with the
  station rule holding the same red, and the Component tag clearing both. The
  re-exporting `__init__` (`from . import notes` beside a comment-only
  sibling, both sides sharing the `__init__`-stripped package key), the
  module whose only content
  is a first-8-lines `# Contracts: IF-001` comment, and the syntax-error
  module the generator KEEPS as a `PARSE ERROR` entry (regen rc==0 asserted —
  the kept-not-crashed half of that arm's claim).
- **No production-code change** — all three fixtures were GREEN on their first
  watched run: no divergence exposed, as the review's 17-case harness
  predicted, so no mirror fix was owed.

**Deviations and judgments.**

1. **Each pin was proven to bite** before being trusted: a scratch mutation of
   each mirror arm (drop `node.level` from `_has_internal_import`, delete the
   first-8-lines Contracts block, flip SyntaxError to False) reds exactly its
   fixture; all mutations reverted. That watching sharpened the `__init__`
   fixture: the natural `from .notes import x` shape SURVIVED the node.level
   mutation — the sibling's stem sits in the names universe, so the
   absolute-segment arm kept it — and `from . import notes` (module=None) is
   the shape that isolates the relative-import arm. The fixture comment
   records the why.
2. **Registration: none owed** — fixtures inside the already-cited
   `tests/test_trajectory_arch.py` suite; no module added, no new LLR/TC rows.
3. Budgeted docs untouched (no byte deltas).

**Watched, measured on the work commit 29af0fcb (clean tree):**
`tests/test_trajectory_arch.py` 60 passed in 1.52s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=29af0fcb -->;
smoke tier 621 passed / 6 skipped in 11.50s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=29af0fcb -->;
full suite 1883 passed / 10 skipped in 0:04:44
<!-- fig: cmd="python -m pytest -q -n auto" rev=29af0fcb -->.
Green-on-first-run is the correct watched outcome for this WI: the fixtures
pin arms the review's harness had already measured consistent; red would have
meant a real divergence, and the mutation drives supplied the red-side
evidence instead.
