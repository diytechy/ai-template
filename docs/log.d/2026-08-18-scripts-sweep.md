## 2026-08-18 — Scripts sweep: stale-CSV docstrings, the DAG caption, and the `docs/work/*` orphan glob

**Why.** Two carrier migrations landed without their prose: the spine moved to
id-keyed TOML (OI-12, batches through WI-443) and the work-item registry became
the `docs/work/` spec folder (concurrency-restructure Phase 5). Docstrings and
one user-facing dashboard caption were still naming the retired `.csv` homes, so
a reader — human or agent — was being pointed at files that no longer exist. And
this repo's `docs/orphans-allow` had never gained the `docs/work/*` glob the
shipped template declares, which is why `check_docs.py` was emitting 454 orphan
warnings of which 453 were the registry itself.

**What changed.**

- **Docstring tokens, conservatively.** Only hits that describe the CURRENT read
  were corrected; every hit that legitimately names the legacy dual-read or the
  migration path was left alone. Fixed: `check.py` (the `Tier` field now names
  `test-cases.toml`), `agent_loop.load_critique_srs` (the docstring said `.csv`
  while the line below it opened `.toml`), `plan_briefs._cmd_surface`'s printed
  heading, `trace.py`'s module `Reads:`/`Writes:` block (the spine is TOML read
  through `spine_carrier`, which still resolves the legacy carriers; the
  off-spine list is now split TOML vs the genuinely-CSV PB/REPO/PART/ASSET), and
  five sites in `check_trajectory.py`. Left standing on purpose: `WI_CSV` and the
  stray-CSV finding it powers, the F5 spec-folder reader's `csv.DictReader`
  comment, the two-carrier reporting comment in the staged-diff record, and the
  40-module `Contracts:` boilerplate naming `interfaces.csv` (a declared absence
  — see below).
- **The DAG caption.** `gen_trajectory.py` told the reader the trajectory came
  from `docs/requirements/work-items.csv` in three places (module docstring, the
  DAG panel caption, the page footer); `traj_panels.py` said the same in the
  Process tab's two captions and two comments. No legacy-CSV mention was kept:
  `check_trajectory.read_registry_rows` treats a resurrected CSV as an integrity
  ERROR, so there is no dual-read left to describe. The path constants at
  `traj_panels.py:583` and `:1116` are untouched — they are resolved to the spec
  folder by the reader.
- **`docs/orphans-allow`.** Added `docs/work/*` with the shipped template's
  reason (each file IS a registry entry, not a navigation node). Removed the
  pre-migration `docs/specs/WI-*.md` glob and its citation of the retired
  `work-items.csv`, and the header's claim that a named parallel-dispatch
  design-notes file under `docs/specs/` is reachable from a companion plan —
  that file no longer exists, so the example was pointing at nothing.

**Measured.** `check_docs.py --root .` orphan warnings **454 -> 1** (the survivor
is `docs/test/report.md`, a generated artifact, pre-existing and out of scope
here). Expected live-orphans matched by the census rose 140 -> 596. Dropping the
`docs/specs/WI-*.md` glob introduced no new warning: both files under
`docs/specs/` are reachable.

**Regenerated.** `docs/architecture.md`'s module block (`gen_arch_map.py --src
project-trajectory/scripts`) — two rows, both mine. `docs/test/report.{md,html}`
(`trace.py --html`), which cleared the 13/14 retired `DevBar-*` tokens the local
`test_stage_ladder.py` fails on. `PROJECT_STATE.html` is deliberately NOT
regenerated here — the caption edits above will land with the OKF lane's
regeneration.

**Reported, not changed.**

- The `traj_parse._sn_rows` / `gen_okf.sn_rows` twin that `open-items.toml`
  OI-12 records as "pinned by nothing but a docstring… HAS ALREADY DRIFTED ONCE"
  is **structurally closed**. Both are now one-line delegations to
  `spine_carrier.folded_needs` (`traj_parse.py:72`, `gen_okf.py:131`), as is
  `trace._sn_prose`; the fold rule has one home at `spine_carrier.py:968`. The
  hazard cannot recur by drift — there is only one copy to drift from. The OI row
  was left untouched for the adjudicator.
- `interfaces.csv` appears in the `Contracts:` boilerplate of 40 script modules.
  It is a declared absence (`docs/declared-absences:37`) so `check_doc_refs` does
  not flag it, and no test pins the line — but the row of record is
  `interfaces.toml`, and a single mechanical sweep would retire the last 40
  copies. Filed as a finding rather than swept, per the conservative brief.
- `check_trajectory.staged_findings` still calls its subject "the staged WI CSV"
  (`:3128`, and the `LINE_BREAK_CHARS` comment at `:745`). Whether that reflects
  what `_staged_wi_registry` reads today needs a look at the function, not a
  token swap — not attempted here.
- `ruff check` reports three pre-existing `F841`s at `trace.py:3847`
  (`exts`/`bifs`/`rels`), outside this lane's hunks.

**Verification.** `tests/test_check_docs.py test_generated_freshness_wiring.py
test_stage_ladder.py` — 83 passed. Every module touched: `test_trace*`,
`test_trajectory*`, `test_gen_trajectory*`, `test_traj_panels`,
`test_plan_briefs`, `test_gen_arch_map`, `test_check_doc_refs`,
`test_dogfood_sync` — 496 passed, 1 skipped. `test_agent_loop*` — 74 passed, 1
skipped. `test_check_harness` + `test_check_docs` — 80 passed, 1 skipped.
