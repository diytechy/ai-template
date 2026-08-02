## 2026-08-02 — WI-411: the dotted-absolute first segment, pinned

**Summary.** WI-410 REVIEW-A finding 1 (minted trunk-side at intake), closed
as specced — fixtures only. The reviewer's probe showed the first-segment
`.split(".")[0]` read INSIDE both absolute arms of `_has_internal_import`
unpinned: with both arms structurally intact, reducing each to whole-name
membership left all 61 trajectory-arch tests green (the WI-410 modules' flat
stems ARE whole names in the names universe), so a module whose only internal
reference is a DOTTED absolute import could drift mirror-side without a red —
the wi-387 station-first topology back, for the dotted shape.

**Deliverables.**

- **One differential fixture** (`tests/test_trajectory_arch.py`, WI-411
  section, work commit 91462f79) through the full lifecycle: lane red on the
  untagged dotted modules BEFORE any regeneration (the mirror keeps them), a
  REAL `gen_arch_map` regen absorbs both and the delta empties — a
  mirror-only keep would be a permanent lane red here — with the station rule
  holding the same red, and the Component tags clearing both. The
  names-universe geometry is the load-bearing move: a comment-only `notes`
  module inside the fixture's scanned `pkg` directory donates `pkg` to the
  universe (both sides collect stems +
  package directory parts from every scanned file BEFORE the symbol-emptiness
  filter) while never itself entering the delta, and the whole dotted name
  `pkg.notes` is in the universe on NEITHER side — only a first-segment read
  can keep the two dotted modules.
- **The recorded terminus — with one named residue** (wording corrected by
  the REVIEW-A rework, below): every branch of `_would_be_inventoried` and
  every arm of `_has_internal_import` — including the first-segment read
  inside both absolute arms and the REVIEW-A-unmasked docstring /
  public-symbol pair — is fixture-pinned EXCEPT the read-failure branch;
  the section comment states it, so the pinning series
  (WI-399 → WI-406 → WI-410 → WI-411) has a recorded end.
- **No production-code change** — the fixture was GREEN on its first watched
  run (1 passed in 0.23s): no divergence exposed (generator and mirror both
  split the first segment), so no mirror fix was owed.

**Deviations and judgments.**

1. **The spec's "one fixture: a module"** is delivered as one fixture TEST
   with two one-form dotted modules — the WI-410 two-module lesson, one
   grain finer: the arms are disjoint syntactic branches, so each arm's
   split must be dropped against its own module (`import pkg.notes` /
   `from pkg.notes import go`); a both-forms module would pin neither split
   alone. The section comment records the why.
2. **The pin was proven to bite** before being trusted: scratch mutations
   (rsync copy, never the worktree) dropping the ImportFrom split alone, the
   ast.Import split alone, and the review's both-dropped probe (previously
   all-green across 61 tests) each red exactly the new fixture — 1 failed,
   61 passed, all three; the single-split drops on the two name asserts, the
   both-dropped probe on the rc assert (the delta empties) — with the
   scratch restored byte-identical (`cmp` clean) and re-green (62 passed).
3. **Registration: none owed** — a fixture inside the already-cited
   `tests/test_trajectory_arch.py` suite; no module added, no new LLR/TC
   rows (the WI-406 REVIEW-A precedent).
4. Budgeted docs untouched (no byte deltas).
5. **Session note:** the commit bar's `check_docs.py --stale` reports 4
   broken link(s) in WI-070/173/288-vintage complete specs — verified
   identical at the trunk checkout, so pre-existing residue, out of this
   WI's fixtures-only scope; left for owner triage.

**Watched, measured on the work commit 91462f79 (clean tree):**
`tests/test_trajectory_arch.py` 62 passed in 1.64s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev=91462f79 -->;
smoke tier 625 passed / 6 skipped in 10.29s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=91462f79 -->;
full suite 1893 passed / 10 skipped in 0:05:04
<!-- fig: cmd="python -m pytest -q -n auto" rev=91462f79 -->.
Green-on-first-run is the correct watched outcome for this WI: the fixture
pins semantics the review's probe had already measured consistent on both
sides; red would have meant a real divergence, and the mutation drive
supplied the red-side evidence instead.

**Rework (2026-08-02, REVIEW-A CHANGES-REQUESTED findings=2, one commit).**
Finding 1 (MAJOR): the terminus over-claimed — the reviewer's mutations
dropped the mirror's docstring arm alone and public-symbol arm alone and
each left all 62 tests green, because MODULE_BODY satisfies both arms at
once. Remedied with two one-form fixtures in the same real-regen
differential pattern (a docstring-ONLY and a public-symbol-ONLY module,
both green on their first watched runs); scratch drives: docstring-arm
drop 1 failed / 64 passed redding exactly the doc-only fixture on its rc
assert, public-symbol-arm drop 1 failed / 64 passed redding exactly the
sym-only fixture on its rc assert. Finding 2 (MINOR): the read-failure
branch (OSError/UnicodeDecodeError -> False) was omitted from the terminus
enumeration and cannot be driven green-green — the crash probe was re-run,
not taken on faith: gen_arch_map on a non-UTF-8 .py dies with
UnicodeDecodeError in scan_module's read_text, rc 1, so there is no absorb
side. The terminus comment now names it as the argued exception, and the
UnicodeDecodeError half carries a LANE-SIDE-only pin (a deterministic
invalid-start-byte fixture — judged worth its few lines since either drift
direction reds: flip-to-True 1 failed / 64 passed, except-drop
1 failed / 64 passed; the OSError half is not stageable portably and stays
argued). The original three first-segment drives re-red exactly the dotted
fixture in the enlarged suite (1 failed / 64 passed, all three); scratch
restored byte-identical, re-green 65 passed. Watched on the rework tree
(91462f79 + the rework diff; tests/ byte-identical to the rework commit):
`tests/test_trajectory_arch.py` 65 passed in 1.84s
<!-- fig: cmd="python -m pytest -q -n auto tests/test_trajectory_arch.py" rev="91462f79 plus the rework diff, tests identical to the rework commit" -->;
smoke tier 629 passed / 2 skipped in 10.16s
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev="91462f79 plus the rework diff, tests identical to the rework commit" -->.
