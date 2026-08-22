## 2026-08-22 — WI-483 slice 2: the lifecycle SCC is broken to ZERO

**Summary.** Two extractions — the registry-gap census into a new sibling
`scripts/census.py`, and the per-close report's shape down into
`scripts/kitlib/station.py` — cut two of the five-module component's three back
edges, and the whole component dissolved: **5 modules / 9 intra-cycle edges ->
0 / 0**. The 2026-08-19 review's H-02 finding is closed as a cycle; the layering
it also asked for is not, and this fragment says exactly what remains.

Deferred open items: none — the slice was deliberately built to need no owner
ruling. Both spine rows are NEW (`LLR-188`, `LLR-189` with `TC-183`, `TC-184`),
not amendments, so no `Approved` ratified cell was rewritten and no approval act
had to be cited; `baseline_snapshot.refresh_refusal` reads clean (`''`) because
the registry diff is new rows plus TRACED cells only.

### The per-edge census, read before the cut was designed

| back edge | what actually crossed | verdict |
| --- | --- | --- |
| `intake -> dispatch` | `dispatch.parse_red_tc` (in `_census_drafts`) and `dispatch.gap_census` (in `_cmd_census`). Behind them a self-contained ~180-line block: `gap_census`, `red_tc_census`, `_red_tc_line`/`parse_red_tc`, `_implemented_ids`, `RED_TC_PREFIX`, `_TC_NOT_RED`, depending only on `trace`, `schedule`, `agent_common`. | CUT — the block is a read model over the registries and decides nothing about lanes. |
| `integrate -> handback` | `handback.report_path` and `handback.report_refusal`, called from `_partial_report_refusal`: a path built from two strings and a rule over a dict, reached by importing the module that WRITES reports. | CUT — the shape moved down; the writes stayed. |
| `integrate -> intake` | `intake.intake_after_merge` from `integrate_one`'s post-merge arm: amendment drafts + close drafts + disposition drafts + the mint, all-or-nothing inside the held slot. | LEFT — real lifecycle behaviour, not extractable behind a read model. |

A fourth deferred edge fell out incidentally and is recorded rather than
claimed: `adjudicate_brief -> dispatch` (the disposition brief re-running the
red-TC census live) now points at `census` instead. It was never inside the SCC.

### What was cut, and how

- **`project-trajectory/scripts/census.py` (NEW, 242 lines).** The whole census
  block, verbatim in behaviour. One real change inside it: `_implemented_ids`
  now reads the work registry through `agent_common.load_registry_rows` instead
  of `ac.read_spec_rows(root / intake.WORK)` — same derivation (`spec_work_dir`
  resolves `docs/requirements/work-items.csv` to `docs/work`, with an
  absent-folder guard), and it removes the module's only reason to import the
  minting module for a layout constant.
- **`project-trajectory/scripts/kitlib/station.py` (+240 lines).** `REPORTS`,
  `CLAIMED_OUTCOMES`, `SUGGESTED_TIERS`, `SPLIT_DECIDERS`, `report_path`,
  `render_report`, `read_report`, `report_refusal` and their two private
  helpers. One addition: `read_toml_block`, the `+++` frontmatter parse, which
  replaces BOTH `handback`'s `_FRONT_RE` + `ac.read_toml_text` pair and the
  copy of the same regex that `integrate._partial_report_refusal` had inline.
  It calls `tomllib` directly rather than `agent_common.read_toml_text` because
  a `kitlib` module may not import a sibling (`tests/test_bootstrap.py::
  test_bootstrap_imports_only_the_common_package`) — that rule is why the
  census could NOT go here and the report could.
- **Re-export shims, slice 1's pattern.** `dispatch` re-exports `gap_census`,
  `red_tc_census`, `parse_red_tc`, `RED_TC_PREFIX`; `handback` re-exports all
  eight report names. No caller moved, and CLI behaviour is byte-identical —
  including `intake.py census`, whose only change is that a local variable was
  renamed off the now-shadowed module name.
- **A prose repair that was owed rather than optional.** `handback.py`'s header
  had claimed the dependency on `integrate` runs one way "never the reverse"
  while `integrate` imported it back; the header now says the sentence was FALSE
  and what made it true, instead of softening it.

### Deliverables

- New: `project-trajectory/scripts/census.py`; `bootstrap.py` MAPPING row +
  reason; `tests/test_bootstrap.py` scaffold file list;
  `project-trajectory/README.md` kit-contents row (and the `kitlib/` row
  extended for the report's shape).
- Spine: `LLR-188` (`scripts/census.py`, `SR-148`, `CMP-008`) and `LLR-189`
  (`scripts/kitlib/station.py`, `SR-144`, `CMP-008`), both `Approved`, with
  `TC-183` / `TC-184`. `IF-089` re-pointed (`this_project` `scripts/census`).
  `docs/id-watermark` bumped LLR 187->189, TC 182->184 via `trace.py
  --bump-ids`. `docs/archive/last_approved/` refreshed (`intake.py snapshot`,
  no `--approves` needed or used). `docs/stage` regenerated — unchanged at
  `DevStg-LLReqs`, `drafted` still 2.
- Tests: `tests/test_import_layers.py` (baselines + the walker self-test's pin),
  `tests/test_loop_order.py` (the grammar pins follow the grammar, plus a new
  assertion that the dispatcher's re-exports answer), `tests/test_rule_sync.py`
  (`_TC_NOT_RED`'s pin follows the set), `tests/test_module_size_ratchet.py`.
- Docs: `docs/status.md`, and the WI-483 spec's Context (slice-2 block + the
  STILL OWED list rewritten truthfully).

### TOPOLOGY DECISION — why two NEW rows and not three amendments

The cheaper diff was to re-point `LLR-149`/`LLR-159`'s module cells and extend
`LLR-182`'s detail. It was rejected on AUTHORITY. `Module`, `CodeSymbol`,
`TestRefs`, `Component` (LLR) and `Verifies`, `Evidence` (TC) are TRACED cells
and free to move; `Title`, `Detail`, `Rationale` on an `Approved` row are
RATIFIED, and `baseline_snapshot.refresh_refusal` exists precisely to stop a
session absorbing its own rewrite of ratified text into the baseline. Its third
escape, `--approves <ref>`, is "a HUMAN's citation of the act" — there is no such
act here, and citing this session's own work item would be exactly the hole the
guard closes. So the slice was built to need nothing but new rows and traced
cells, and the refusal check confirms it rather than the other way round.

What keeps the untouched rows TRUE is the re-export shims, not luck:
`dispatch.gap_census` and `dispatch.red_tc_census` still exist and the dispatcher
is still rung 1's caller, so `LLR-149`/`LLR-159` describe a surface that is still
there. `LLR-182` is untouched and its "imports nothing" clause still reads true
in its own idiom — the module imported `enum` and `MappingProxyType` before this
slice, so the phrase never meant literal zero imports; `LLR-189` is the row that
names what `station.py` gained. `LLR-182`'s `CMP-008` tag, its absence from
`docs/kernel-modules-allow` and `IF-093` are all exactly as WI-494 left them.

`IF-089` had to move or go false: `dispatch -> trace` no longer exists and
`census -> trace` is a CMP-008 to CMP-006 crossing that would otherwise be an
undeclared seam. Verified live rather than assumed —
`check_trajectory._classifiable_edges` reports
`('scripts/census', 'scripts/trace', {'CMP-008'}, {'CMP-006'})` and
`_declared_seam_pairs` contains that pair. Both new modules carry a component
tag, so neither joins the How-SW containment count's `uncontained` list.

### Driven figures

Every figure below was driven on the WORKING TREE whose base commit is
`b48cce86`; that base is what `rev=` names, the same stamping this repo's
recent fragments use, and the before-figures were driven in a detached
worktree checked out at it.

- SCC before this slice: **5 modules** `(dispatch, handback, intake, integrate,
  lane)`, **9 intra-cycle edges**, 21 deferred function-body imports repo-wide
  <!-- fig: cmd="git worktree add /d/wi483-before HEAD --detach && cd /d/wi483-before && python -c \"import sys;sys.path[:0]=['tests','project-trajectory/scripts'];import test_import_layers as t;g=t.import_graph();print(t.strongly_connected(g), len(t.intra_cycle_edges(g)))\"" rev=b48cce86 -->
- SCC after: **0 modules, 0 intra-cycle edges**, 19 deferred
  <!-- fig: cmd="python -c \"import sys;sys.path[:0]=['tests','project-trajectory/scripts'];import test_import_layers as t;g=t.import_graph();print(t.strongly_connected(g), len(t.intra_cycle_edges(g)))\"" rev=b48cce86 -->
- Module lines after: `census.py` 242, `dispatch.py` 1352 -> 1195,
  `handback.py` 650 -> 490, `kitlib/station.py` 101 -> 341, `intake.py` 1940 ->
  1937, `integrate.py` 2569 -> 2578
  <!-- fig: cmd="wc -l project-trajectory/scripts/census.py project-trajectory/scripts/dispatch.py project-trajectory/scripts/handback.py project-trajectory/scripts/kitlib/station.py project-trajectory/scripts/intake.py project-trajectory/scripts/integrate.py" rev=b48cce86 -->

### Ratchets re-stamped, each deliberately

- **`tests/test_import_layers.py` `CYCLES`: the five-module entry DELETED**, the
  list now empty. Because the test compares for EQUALITY this is a tightening,
  not a removal: any new cycle anywhere under `scripts/` now reds.
- **`MAX_INTRA_CYCLE_EDGES` 9 -> 0** (owed downward re-stamp; the test asserts
  equality both ways). The count is kept rather than deleted — it is the half
  that survives a component reappearing at a different size, which is the hole
  the 2026-08-21 review proved by mutation.
- **The walker's self-test pin moved** off `integrate -> handback` (an edge this
  slice cut) onto `integrate -> intake` (the one still owed). A self-test pinned
  to an edge the program is paid to remove cannot survive the program.
- **The deferred-import window 14..26 is UNMOVED**; the reading went 21 -> 19,
  and the comment records both numbers.
- **`tests/test_module_size_ratchet.py`**: `bootstrap.py` 3023 -> 3030 (+7, the
  MAPPING row and its reason — a manifest growing), `integrate.py` 2569 -> 2578
  (+9, a nine-line parenthesised import list and the docstring paragraph
  recording which import was cut; the executable change was a net DELETION),
  `intake.py` 1940 -> 1937 (DOWN, the two deferred `import dispatch` sites).
  Reasons inline in the baseline dict, per that file's convention.

### Deviations from the brief

- The brief said extractions go to `kitlib/` themed modules and allowed "a new
  themed module … if it's the smallest-total-code answer". The census could NOT
  go to `kitlib` — the package rule forbids sibling imports and the census's
  purpose is to reuse `trace.analyze` — so it is a plain sibling. The report's
  shape DID go to the station theme, exactly as the brief nudged.
- The brief's preferred outcome (whole SCC to 0) was reached with TWO of the
  three back edges, not three. `integrate -> intake` survives as a
  no-longer-cyclic layering inversion; hoisting it would change what
  `integrate.py merge` does standalone, which this slice's byte-identical-CLI
  contract forbids. Recorded as STILL OWED item 1 on the WI, rewritten from the
  old item 1.
- M-06 rode along and found nothing to split: the three test modules this cut
  touched are all under 400 lines. The four monoliths the review named are
  untouched and still await their subsystems.

### Gates (Windows, `-n auto`, `--basetemp` on `D:`; real output, none sanctioned)

- `python -m pytest -q -n auto -m smoke`: **1368 passed, 5 skipped in 112.52s**
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke --basetemp=D:\\pytest-tmp" rev=b48cce86 -->
  — GREEN but far over the WI-281 60 s budget, and this is a BOX reading rather
  than a tier reading: the same tier measured 59.28 s on this machine one day
  earlier (WI-494) with the same membership, and this slice adds no smoke tests
  and removes none. Two readings were taken this sitting, 150.60 s and 112.52 s,
  the spread itself being the evidence that the machine and not the tier is what
  moved. One machine is one data point; the budget is not moved, and nothing here
  is offered as evidence that it should be.
- `python project-trajectory/scripts/check_docs.py --root . --stale`: OK —
  1006 doc(s), 1345 intra-repo link(s), 0 broken (1 pre-existing orphan
  warning, plus the usual staleness hints).
- `python project-trajectory/scripts/check_trajectory.py --root . --strict`:
  clean, exit 0 (507 work items, graph acyclic; pre-existing warns only — the
  shared-spec-of-record advisories, the SpecRef-changed batch and one
  filename-length warn, none touching this diff).
- `python project-trajectory/scripts/trace.py --root . --strict
  --strict-integrity`: exit 1 on the SAME ten pre-existing `FINDING (orphan)`
  lines WI-494 recorded (SR-151/152/160/163/164, no LLR and no TC);
  `system-requirements.toml` carries zero diff here. Zero
  `FINDING (spine stand-alone)` lines, and zero advisories naming any id this
  slice authored — the first draft of `IF-089`'s Notes cell DID carry a
  `WI-483` citation frame, `trace.py` caught it, and the cell was reworded to
  timeless prose before the snapshot was refreshed.
- `python project-trajectory/scripts/derive_stage.py --root . --check`: up to
  date (`DevStg-LLReqs`) after one regen.
- `python -m pytest -q -n auto` (full, unfiltered): **2847 passed, 14 skipped
  in 1039.11s (0:17:19)**
  <!-- fig: cmd="python -m pytest -q -n auto --basetemp=D:\pytest-tmp-wi483" rev=b48cce86 -->
  — single foreground process, not batched, `--basetemp` on `D:` per the
  standing low-disk note on this box. Same pass count as WI-494 recorded the
  same day (2847/14), which is the expected reading: this slice adds no test
  cases, it re-points existing ones at the modules their subjects moved to.

**Line-ending discipline.** Several in-place Python rewrites of registry and
script files wrote CRLF on this box (`pathlib.write_text` translates to
`os.linesep`); caught with `git ls-files --eol | grep 'w/crlf'` before any
measurement and normalized back to LF, leaving only the `*.cmd`/`*.ps1` files
that are supposed to be there.
