# WI-411 — REVIEW-A (2026-08-02)

_Two rounds: round 1 CHANGES-REQUESTED (its record below, unedited); round 2
APPROVE after rework `71b7937d` — every remedy claim re-driven and held, see
the Round 2 section at the end._

## Round 1

Verdict: CHANGES-REQUESTED — the fixture itself is exactly right: I re-ran all
three scratch mutations myself (drop the `ImportFrom` first-segment split
alone, the `ast.Import` split alone, both) and each reds EXACTLY the new
fixture — `1 failed, 61 passed` all three times, two name asserts and one rc
assert, scratch restored byte-identical and re-green (`62 passed`). The
names-universe donor geometry is verified in code on both sides and is
rot-resistant. But this WI's distinguishing requirement was the RECORDED
TERMINUS, and the terminus statement shipped is false as written: the section
comment claims "every branch of _would_be_inventoried (parse-error keep,
docstring, public symbol, internal import, Contracts comment, symbol-empty
skip) … is fixture-pinned", and my own mutations dropped the docstring arm
alone (**62 passed**) and the public-symbol arm alone (**62 passed**) — two
branches the comment names as pinned are not, because `MODULE_BODY` satisfies
both at once (the exact masked-pair phenomenon WI-410 taught). The
`_has_internal_import` half of the terminus DOES hold — all five arms are
fixture-pinned, verified below. The series must not close on a record that
mutation testing disproves; the fix is small (make the comment true, or make
the claim true), hence a round, not a rejection.

Reviewed independently against the spec
(`docs/work/complete/WI-411-dotted-absolute-first-segment-unpinned.md`:
fixtures only, the first-segment `.split(".")[0]` read inside BOTH absolute
arms driven through the full differential lifecycle, the scratch-mutation
drive, and "state that [the arm list is exhausted] in the fixture comment so
the pinning series has a recorded terminus") and the WI-399/406/410 sections
of `tests/test_trajectory_arch.py`. Diff = `91462f79` (work, test file only,
+55) + `e5a204aa` (close) on `wi-411-dotted-absolute-first-segment-unpinned`,
delta measured from `48c11bb7` (the WI-410 integrate the branch claims from).
`docs/log.d/` was not read. All commands run under
`/Users/diytechy/Documents/ai-template/.venv/bin/python` from the worktree;
mutations in a scratch rsync copy, never in the worktree.

## Findings

1. **MAJOR — the recorded terminus over-claims: the docstring and
   public-symbol branches of `_would_be_inventoried` are each singly
   unpinned, and the comment names both as pinned.** The shipped section
   comment (`tests/test_trajectory_arch.py`, WI-411 section): "this EXHAUSTS
   the mirror's arms: every branch of _would_be_inventoried (parse-error
   keep, docstring, public symbol, internal import, Contracts comment,
   symbol-empty skip) … is fixture-pinned — the pinning series' recorded
   terminus." Scratch mutations against
   `project-trajectory/scripts/check_trajectory.py`: deleting the docstring
   arm (`if (ast.get_docstring(tree) or "").strip(): return True`) alone →
   **62 passed in 1.61s**; deleting the public-symbol arm (the
   `FunctionDef/AsyncFunctionDef/ClassDef` block) alone → **62 passed in
   1.65s**. Deleting BOTH together reds 3 tests
   (`test_added_module_without_component_tag_reds_the_lane_bar`,
   `test_absolute_declared_src_scans_like_the_generator`,
   `test_differential_delta_empties_exactly_when_the_regen_absorbs`) — the
   pair mutually masks because every fixture module that must be KEPT via
   these arms is `MODULE_BODY` (`'"""M."""\n\n\ndef run():\n    """go"""\n'`),
   which carries a docstring AND a public symbol; no docstring-only or
   public-symbol-only module exists anywhere in the file. This is precisely
   the WI-410 lesson the same comment cites ("disjoint syntactic branches …
   one-form module"), unapplied to `_would_be_inventoried`'s own keep arms: a
   docstring-only module (a real downstream shape — a constants module with a
   summary line and only private names) is kept by the generator (summary
   non-empty) but skippable by a drifted mirror with no red — the wi-387
   station-first topology returns for the docstring shape, the
   WI-406-finding-1 way. **Required:** make the record true — either narrow
   the terminus statement to what is proven (the `_has_internal_import` arm
   inventory, which I verified exhaustively below, matching the spec's "per
   the WI-410 arm inventory"), or pin the masked pair with two one-form
   modules through the lifecycle. Whether the pair-pinning fixtures land here
   or as an intake row is the owner's call; the false record merging is the
   blocker. -> @builder

2. **MINOR — the read-failure branch is a branch of `_would_be_inventoried`
   the "every branch" enumeration omits, and it is unpinned too.** The
   mirror's first branch — `except (OSError, UnicodeDecodeError): return
   False` ("an unreadable file cannot be judged and is left out", its own
   docstring) — is absent from the comment's six-item list. Scratch mutation
   flipping it to `return True` → **62 passed in 1.65s**. The honest bound:
   this branch CANNOT be pinned by the series' green-green differential
   method — I probed the generator with a non-UTF-8 `.py`
   (`printf '\xff\xfe…' > scripts/bad.py`; `gen_arch_map.py --src scripts`)
   and it CRASHES, rc=1 with a `UnicodeDecodeError` traceback out of
   `scan_module`'s unguarded `path.read_text(encoding="utf-8")`
   (`gen_arch_map.py:246`), so `regen_map`'s rc==0 assert can never pass over
   such a tree; only a lane-side-only fixture (invalid-UTF-8 file, assert no
   ADDED red pre-regen, no regen step) could pin the skip half. Fixable
   inside finding 1's correction: the reworded terminus should either name
   this branch as the recorded, argued exception or add the lane-side pin.
   (The generator crash itself predates this WI and is out of scope — noted,
   not counted.) -> @builder

## None against — what I tried and could not break

- **Pin 1 bites, and only its fixture.** Scratch mutation dropping the
  `ImportFrom` split (`(node.module or "").split(".")[0] in internal_names` →
  `(node.module or "") in internal_names`) →
  `FAILED tests/test_trajectory_arch.py::test_dotted_absolute_import_modules_are_inventoried_on_both_sides`
  on `assert "scripts/dot_from" in strict.stderr` — **1 failed, 61 passed in
  1.63s**. No collateral reds.
- **Pin 2 bites, and only its fixture.** Dropping the `ast.Import` split
  (`a.name.split(".")[0] in internal_names` → `a.name in internal_names`) →
  the same test, on `assert "scripts/dot_imp" in strict.stderr` — **1 failed,
  61 passed in 1.65s**.
- **The both-dropped probe bites on the rc assert.** Both splits dropped (the
  exact shape WI-410 REVIEW-A finding 1 ran green across 61 tests) → the same
  test, on `assert strict.returncode == 1` (the mirror keeps neither dotted
  module, the delta empties, rc 0) — **1 failed, 61 passed in 1.62s**. All
  three failure modes land exactly where the section comment and Deliverable
  promise (two name asserts, one rc assert). Scratch then restored: `cmp`
  against the worktree's `check_trajectory.py` **byte-identical**, module
  re-ran **62 passed in 1.69s** — the mutations were the only cause.
- **The names-universe donor geometry, verified in code on BOTH sides.**
  Generator (`gen_arch_map.py` `_module_files`): `names.add(path.stem)` +
  `names.add(part)` for the rel-path directory parts, for EVERY scanned file,
  before `build_map`'s symbol-emptiness `continue`. Mirror
  (`check_trajectory.py` `shipped_modules`): `names.add(path.stem);
  names.update(rel.parts[:-1])` in the collection loop, before the
  `_would_be_inventoried` filter. So the comment-only `pkg/notes.py` donates
  `pkg` (and `notes`) on both sides while entering the delta on neither
  (comment-only → skipped by `build_map`'s emptiness filter AND by
  `_would_be_inventoried`'s fall-through) — and both universes hold only
  single path segments, so the whole dotted `pkg.notes` is in NEITHER: only a
  first-segment read can keep `dot_imp`/`dot_from`, exactly as the fixture
  comment states. Rot-resistance: the geometry is asserted live, not merely
  commented — `"2 shipped module(s)"` reds loudly if the donor ever gains
  symbols and enters the delta, and `ADDED_MSG not in strict.stderr` after
  the REAL regen reds if either side's collection order ever moves the names
  build behind the emptiness filter. The fixture cannot rot green.
- **The terminus HOLDS for `_has_internal_import` — all five arms, each with
  its isolating fixture.** Enumerated from the shipped code: (1) `ImportFrom
  node.level` — WI-406's `from . import notes` (module=None) isolates it; (2)
  `ImportFrom` absolute membership — WI-410's `abs_from`; (3) the `ImportFrom`
  first-segment split — this WI's `dot_from` (re-proven above); (4)
  `ast.Import` membership — WI-410's `abs_imp`; (5) the `ast.Import`
  first-segment split — this WI's `dot_imp` (re-proven above). At arm grain
  that list is exhaustive — the spec's actual requirement ("per the WI-410
  arm inventory") was deliverable as stated; the findings are about the
  comment widening the claim to `_would_be_inventoried`.
- **Differential integrity — real generator, both sides, all four stations.**
  rc==1 + ADDED naming BOTH dotted modules + the `2 shipped module(s)` count
  BEFORE any regen; `regen_map` runs the REAL `gen_arch_map.py` (asserts
  rc==0); after regen the ADDED red is gone while `KN_MSG` holds the same
  red; tagging all four modules clears to rc==0. Same lifecycle as the WI-406
  and WI-410 sections it extends.
- **The record, re-run rather than read.** In the worktree at `e5a204aa`:
  `python -m pytest -q -n auto tests/test_trajectory_arch.py` → **62 passed
  in 1.67s** — the Deliverable's module fig re-driven with exact agreement
  (this is the spot-checked declared figure). Smoke tier → **629 passed, 2
  skipped in 10.29s** — matches the close commit's 629/2 (the Deliverable fig
  at `91462f79` says 625/6 — the environment-dependent-skip delta this review
  family has recorded before). The full-suite fig (**1893 passed / 10 skipped
  in 0:05:04** at `91462f79`) is the BUILDER'S, attributed not re-run —
  module + smoke + strict is this review's tier. `check_trajectory --strict`
  rc=0 — WARN set diffed line-for-line against trunk: **identical, 11 each**,
  none about WI-411; `check_doc_refs --strict` rc=0; `check_figures --strict`
  rc=0, **60 declared figure(s), every one carrying its command and
  revision** — matching the close claim exactly. `ruff check` All checks
  passed; `ruff format --check` 1 file already formatted.
- **Fixtures-only, proven from the delta.** The whole WI-411 delta vs
  `48c11bb7`: `tests/test_trajectory_arch.py` (+55, the work commit's only
  file), the mint→claim→complete spec lifecycle (net: exactly the one
  complete spec under `docs/work/`, nothing else), the unread `docs/log.d/`
  fragment, `PROJECT_STATE.html` + `docs/gate` (claim bookkeeping), and one
  generated `docs/status.md` frontier line. Zero production `.py` hunks.
  Matches the spec's "Scope: tests/test_trajectory_arch.py only"; budgeted
  docs untouched, as claimed.
- **R-A / R-F.** Strict trajectory rc=0 carries both rungs; the complete
  spec's frontmatter has no `specref` (cleared at close, R-F) and a filled,
  dated Deliverable naming the work commit (R-A). The `WI-411` token at
  `docs/status.md:173` sits inside the GENERATED STATUS ready-frontier block
  (exempt from forward-only; drops at the merge regen — the same shape the
  WI-410 review recorded).
- **Registration judgment — sound.** No new LLR/TC rows: one fixture inside
  the already-cited `tests/test_trajectory_arch.py` suite, no module added,
  no public surface — the WI-406/WI-410 REVIEW-A precedent the Deliverable
  cites.

**THIS IS A CHANGES-REQUESTED:** every claim the builder scratch-PROVED
re-proved true here — both split pins bite exactly as recorded, the donor
geometry is real and rot-resistant, the branch is provably fixtures-only, and
the mechanical record re-ran green. What fails is the one claim the builder
asserted WITHOUT a mutation: the terminus's `_would_be_inventoried` half,
where two named branches fall to single-arm drops (62 green each, a masked
pair via `MODULE_BODY`) and a third branch is missing from the enumeration.
The series' recorded terminus is the deliverable this WI was minted to leave
behind; it must be true before it merges.

## Round 2 (2026-08-02) — the remedy, judged on its own evidence

Verdict: APPROVE — rework `71b7937d` (test file +79, the complete spec's
Deliverable, the unread `docs/log.d/` fragment; nothing else) remedies both
findings, and every remedy claim was re-driven here rather than read. Scratch
re-synced to the rework tree, mutations never in the worktree, restored
byte-identical (`cmp` clean) and re-green **65 passed** at the end.

- **Finding 1 RESOLVED — the masked pair is now pinned by one-form
  modules.** `test_docstring_only_module_is_inventoried_on_both_sides`
  (`'"""Docstring-only module."""\n'`) and
  `test_public_symbol_only_module_is_inventoried_on_both_sides`
  (`"def run():\n    pass\n"`), each through the same real-regen lifecycle
  (lane red → absorb → station parity → tag clears). Re-driven: dropping the
  docstring arm alone →
  `FAILED …::test_docstring_only_module_is_inventoried_on_both_sides` on
  `assert strict.returncode == 1` — **1 failed, 64 passed in 1.75s**;
  dropping the public-symbol arm alone →
  `FAILED …::test_public_symbol_only_module_is_inventoried_on_both_sides` on
  the same rc assert — **1 failed, 64 passed in 1.76s**. Each single drop
  reds exactly its fixture and nothing else — the round-1 62-green masking is
  gone, exactly as the rework's Deliverable records.
- **Finding 2 RESOLVED — the terminus is reworded honestly AND the builder
  went further than asked: the `UnicodeDecodeError` half is now lane-side
  pinned, both drift directions.**
  `test_undecodable_module_is_skipped_lane_side_without_a_crash` stages
  `b"\xff\xfe\x00not utf-8"` (`\xff` is an invalid UTF-8 start byte on every
  platform — deterministic) and asserts quiet skip, no regen step (there is
  no absorb side — my round-1 crash probe, re-confirmed by the builder).
  Re-driven both ways: flip `return False` → `return True` under the except →
  the never-absorbable file enters the delta —
  `FAILED …::test_undecodable_module_is_skipped_lane_side_without_a_crash`,
  **1 failed, 64 passed in 1.81s**; delete the
  `except (OSError, UnicodeDecodeError)` handler entirely → the checker
  crashes with the `UnicodeDecodeError` traceback, rc 1 — same test,
  **1 failed, 64 passed in 1.84s**. The reworded section comment now claims
  every arm pinned "EXCEPT the read-failure branch", names the crash-probe
  reason, and scopes the remaining residue to exactly the `OSError` half ("an
  unreadable file — not stageable portably" — true: not stageable on Windows,
  and unreliable under root). I re-audited the enumeration against the
  shipped code: with the two new one-form fixtures and the lane-side pin,
  every arm of `_would_be_inventoried` and `_has_internal_import` is pinned
  except that one named, argued residue. **The terminus as now recorded is
  honest.**
- **The original pins still bite in the enlarged suite.** Re-driven all
  three: ImportFrom split dropped → `FAILED
  …::test_dotted_absolute_import_modules_are_inventoried_on_both_sides` —
  **1 failed, 64 passed in 1.74s**; ast.Import split dropped → same test —
  **1 failed, 64 passed in 1.88s**; both dropped → same test — **1 failed,
  64 passed in 1.92s**. No collateral reds anywhere in the battery; scratch
  restored `cmp`-byte-identical against the worktree mirror, re-green
  **65 passed in 2.01s**.
- **The record, re-run at `71b7937d`.** Module suite in the worktree:
  **65 passed in 1.85s** (the rework fig says 65 passed in 1.84s — exact
  count agreement, the spot-checked figure; its `rev` is honestly worded as
  the pre-commit rework tree, "tests identical to the rework commit", which
  I confirmed by re-running at the commit itself). Smoke → **629 passed, 2
  skipped in 10.77s** (fig: 629/2 in 10.16s — exact counts).
  `check_trajectory --strict` rc=0; `check_doc_refs --strict` rc=0;
  `check_figures --strict` rc=0, **64 declared figure(s), every one carrying
  its command and revision**. `ruff check` All checks passed; `ruff format
  --check` 1 file already formatted. The rework delta is WI-411-only:
  `tests/test_trajectory_arch.py`, the complete spec's Deliverable (rework
  paragraph dated, every number in it matching my measurements), and the
  log fragment. Still zero production `.py` hunks — fixtures only, as
  specced.

**THIS IS AN APPROVE:** both findings were remedied the strong way — the
masked pair pinned rather than talked around, the residue named and halved
with a deterministic lane-side pin — and every number in the rework's record
reproduced exactly under reviewer-run mutations. With the two one-form
fixtures and the undecodable pin in place, the pinning series' recorded
terminus is now true as written: every arm fixture-pinned except the argued,
named `OSError` residue. The series closes.

VERDICT: APPROVE findings=2
