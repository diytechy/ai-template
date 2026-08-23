## 2026-08-23 — WI-483 slice 4: the first engine split (`trace.analyze`), and its two attribute bags typed

**Summary.** Program shape item 5, one engine of the three. `trace.analyze` —
the largest and by far the most complex function in the kit — is decomposed
OUTWARD into a composer plus named rule families, its cross-row half moved to a
new sibling `project-trajectory/scripts/coherence.py`, and the two attribute
bags around it (`Registries`, `Findings`) are now typed dataclasses: the
immutable-config / mutable-runtime-state pair the program shape asks for. CLI
output, `test/report.md` and the gap census are byte-identical, proven by
before/after compare rather than asserted.

Deferred open items: none — the two new spine rows are authored rather than
amended, so no approved cell was rewritten and no ruling was needed; the
`LLR-147` snapshot refusal this slice worked around is a pre-existing finding
already reported to `docs/status.md` by slice 3, not a decision this session
withheld.

### Today's re-measurement, before choosing

The review's 2026-08-19 figures had moved, and two of the three had moved UP.
Re-measured on this tree at `fe6173d3` (`wc -l`; ruff C901 at
`lint.mccabe.max-complexity=10`, the ratchet's pin):

| engine | review 2026-08-19 | today, before | after |
| --- | --- | --- | --- |
| `trace.analyze` | 514 lines / C901 50 | **553 / 50** | **218 / under 10 (off the census)** |
| `check.steps` | 494 lines | **628 / under 10** | untouched |
| `agent_loop.main` | 402 / 27 | **402 / 27** | untouched |

fig: `wc -l` + `python -m ruff check --select C901 --config
"lint.mccabe.max-complexity=10"` over the three modules, at `fe6173d3`.

Worst-offender-first picked `trace.analyze` with no argument: 553 lines at five
times the complexity limit, versus `check.steps`, which is LONGER but is a flat
sequence of step declarations that C901 does not even flag. Line count and
complexity disagree about `check.steps`, and the axis this program is paying
down is complexity (the owner's own `OI-16` correction). `agent_loop.main` at
402/27 is the honest second target and it is NOT started — see "what remains".

### The split design — the boundary, stated

`analyze` mixed four kinds of statement in one body: rules that JOIN ACROSS
ROWS, sweeps that ask whether a FILE or a raw row is well-formed, the delivery
filter and status criterion, and the assembly of a 37-field result.

**The policy/effect line, and it is one sentence:** a rule that needs more than
one row to have an opinion moved to `coherence.py`; a rule that inspects one
row's prose, or asks whether a carrier parses, stayed with the engine. So:

- **OUT** to `coherence.py` (425 lines, under the size THRESHOLD, no ratchet
  entry of its own): the four-tier orphan rules, `tc_citation_findings`, the
  PB/REPO/CMP back-link and membership resolutions, the knowledge-pack
  resolution, `PhaseScope` (was the nested `in_phase` closure) and the
  `--require-verified` status criterion.
- **STAYS** in `trace.py`: the carrier sweeps, now named —
  `integrity_sweep` / `placeholder_sweep` / `schema_sweep` — plus
  `verification_basis` (a COUNTER, not a rule) and `aspect_counts`, the per-row
  prose lints, the renderers, the approval/watermark machinery and the CLI.

**Decomposition is OUTWARD, and the recorded trap is why.** ruff's C901 charges
a nested def to its enclosing function, so the `in_phase` closure inside
`analyze` was costing the number the extraction exists to lower. It is now
`coherence.PhaseScope.covers` — a frozen record with a method, resolved once.

**The bags, typed.** `Registries` is a **frozen** dataclass with 34 declared
fields, constructed at exactly one site (the loader) — which is asserted, not
hoped: a frozen record is only a guarantee while one place fills it. Two
defensive `getattr(reg, ..., [])` reads inside `analyze` are gone, because a
total record cannot be missing a field. `Findings` is the **mutable** half, a
plain dataclass whose two post-analyze fields (`watermark_advisories`,
`snapshot_findings` — their rules read git and the filesystem, which analyze's
purity forbids) are now DECLARED with empty defaults rather than conjured at a
call site. A third record, `AnalysisFlags`, is the engine's config: `census.py`
had been importing `argparse` to forge a four-field `Namespace`, which is what a
non-CLI caller must do when the CLI namespace IS the config type.

**Behaviour preserved byte-identically, and measured that way.** Before/after
diff of (a) `trace.py --root . --strict --strict-schema --no-placeholders
--require-verified` console + exit code, (b) the full `render_report` text, and
(c) `census.gap_census(".")` — all three empty diffs, run against a `git stash`
of this slice's script diff. Finding ORDER is now a property of the composer
(SR → LLR → TC → SN, stated in its docstring as load-bearing) rather than of
where an `append` happened to sit; every tier returns the same
`(at_fault_id, finding)` pair `tc_citation_findings` already returned, so the
id set the views flag is collected once instead of at eight append sites.

### Before / after figures

fig: `wc -l`; ruff C901 at `max-complexity=10`; `python -m pytest -q`.

- `trace.analyze`: **553 → 218 lines**, **C901 50 → under 10** (entry DELETED
  from `tests/test_complexity_ratchet.py`, the largest number that census ever
  held).
- `trace.py`: **5,373 → 5,316 lines** (−57). Re-stamped DOWN in the same commit.
  A net shrink DESPITE ~75 lines of new field declarations for the two typed
  bags, because 323 lines of rules left for the new sibling.
- `coherence.py`: **425 lines, zero C901 entries.** `spine_orphan_findings`
  measured 15 as a straight lift, so it was split again — `_sr_` / `_llr_` /
  `_sn_orphan_findings` — rather than opening a new baseline row. The census
  count therefore drops 6 → 5 and its sum 140 → 105.
- Smoke membership: **1,294 → 1,320 re-stamped** (`docs/stack.ini`
  `[smoke-budget] max-tests`). +16 collected, all sixteen in the one new
  in-process module, all pure (dict rows built in the test, or `ast` over a
  script — no subprocess, no scaffold, no git), 0.86 s for the module. The
  tier's wall clock is **26.9 s against the 60 s budget**, ~2x headroom and
  untouched. They belong in the COMMIT bar because what they guard is
  ACCRETION — `analyze` growing back past the composer, or a field springing
  into existence on a bag again — both introduced by an ordinary-looking edit.
  fig: `python -m pytest -q -n auto -m smoke [--collect-only]`, stamped in
  `docs/stack.ini`.
- `bootstrap.py`: **3,132 → 3,138 (+6), reviewed bump.** One MAPPING row plus
  the five comment lines saying why `coherence.py` ships. Declaration only, no
  logic — the identical shape slice 3 took for `pending.py` (+8) yesterday.

### Spine

New rows, not amendments — the slice-2 rule, and for the same reason: nothing
here rewrites an `Approved` approved cell, so no approval act has to be cited.
`LLR-201` (`scripts/coherence.py`, `SR-157`, `CMP-006`, `TC-197`) and `TC-197`
are **`Drafted`**, following slice 3's recorded deviation: `LLR-147`'s snapshot
drift still refuses `intake.py snapshot`, that refusal predates this slice
(unchanged from HEAD), and blessing another row's drift is not a session's to
do. `integrity=0` is unchanged. `CMP-006` is trace.py's own component, so the
new module opens no cross-component seam and needs no `IF-###` row —
`check_trajectory --strict` is clean, including the containment error the new
module raised before the row existed. `docs/id-watermark` bumped LLR 200 → 201,
TC 196 → 197 via `--bump-ids`. `docs/stage` and `PROJECT_STATE.html`
regenerated (drafted 17 → 19).

### M-06 (test monoliths)

No monolith split: this engine's split did not make one necessary, and a
standalone split slice is out of scope by the program's own terms. The new
module gets its own new test file `tests/test_trace_coherence.py` (16 tests) —
the `pending.py` shape from slice 3 — which guards the BOUNDARY rather than
re-asserting rules already covered end to end through `trace`: the rules driven
directly one tier at a time, the frozen/total registry record and its single
construction site, per-instance list defaults on the findings record (the
dataclass trap that would otherwise let two analyses share a list), the flags
record, that `coherence.py` imports no sibling of `scripts/`, and that `analyze`
STAYS a composer — a measured line span plus "no nested def", so the 553-line
function accreting back is a red rather than a discovery.

### Deviations from spec

1. **A new shipped module, where the brief allowed but did not require one.**
   The first cut kept every extracted rule inside `trace.py`; that grew the file
   +264 lines (declarations and docstrings) and would have demanded an UPWARD
   size-ratchet bump on the very slice that removed the kit's worst function.
   `test_module_size_ratchet.py` names the alternative in its own docstring —
   "moving lines into a new module is exactly the intended escape hatch" — so
   the rules moved and the file re-stamped DOWN instead.
2. **`census.py` edited (5 lines).** Outside the engine, but it is the engine's
   only non-CLI caller and the reason `AnalysisFlags` is worth having; leaving
   the forged `argparse.Namespace` in place would have shipped the record and
   kept the smell it was written to remove.

### Gates

- smoke: (see the commit) + `check_smoke_budget.py --mode enforce`
- full unfiltered suite: (see the commit)
- `check_docs.py --root . --stale`, `check_trajectory.py --root . --strict`,
  `trace.py --root . --strict`: clean (orphans=4 / provenance-findings=1 are
  the pre-existing SR-163/SR-181 and LLR-197 state, unchanged from HEAD).

### What remains of item 3 (the engine splits)

Two of three engines are UNTOUCHED and the item stays open:

- **`check.steps` — 628 lines, under the complexity limit.** The longest
  function in the kit by line count and the one whose split needs a decision
  rather than a technique: it is a flat declaration of the gate's steps, so
  "decompose" here means choosing a carrier for a declaration, not extracting
  branches. Worth its own slice, and possibly worth arguing it is fine as it is.
- **`agent_loop.main` — 402 lines / C901 27**, plus `session_bookkeeping` (325 /
  31) and `run_iteration` (326 / 20) around it, and the `LoopContext` attribute
  bag, which is the direct analogue of the two bags typed here. This is the
  honest next target: same defect, same fix, a bigger blast radius because the
  loop's state is genuinely mutable across an iteration.

Items 1 (the `integrate -> intake` layering) and 4 (M-06's monoliths) are also
unchanged.

**The banked WI-448 finding stays banked.** The `k = v` joiner's two homes with
different absence rules (`kitlib.evidence.render_fields` vs
`kitlib.spine.toml_fields`) were checked against this slice's surface and are
untouched by it: `coherence.py` renders no fields and emits no TOML, and nothing
moved in or out of either module. Left recorded for whoever takes the surface
that actually uses them.
