# WI-389 — REVIEW-A (2026-08-02)

Verdict: APPROVE — the drawn cycle is the shipped machinery. I walked every
edge and label of the station SVG against `dispatch.py` / `lane.py` /
`integrate.py` / `intake.py` (not against the design doc), mutation-tested all
three sync pins myself (each reds or follows exactly as claimed), regenerated
the dashboard in the worktree and read the pixels across light+dark at 1280,
1680 (station element crops) and 390. Both of the builder's driven fixes are
visible in the shots. Two findings, both MINOR — a wrong git verb on one card
note and a 390px legibility observation — neither of which misstates the
cycle's order, its topology, or the serial-waist property the row was minted
to make visible.

Reviewed independently against the spec
(`docs/work/complete/WI-389-process-tab-station-flow.md`), drain-plan row 12
("verify by pixels, not by reading the generator"), and the shipped flow
modules. Diff = `56dc580d` (work) + `8874f695` (close) on
`wi-389-process-tab-station-flow`; the branch's own delta measured from the
trunk-side claim commit `78944578` (verified: `git merge-base
ConcurrencyTrainRewrite HEAD` = `78944578`, and `merge-base --is-ancestor`
confirms it on trunk). `docs/log.d/` was not read. All commands run under
`/Users/diytechy/Documents/ai-template/.venv/bin/python` from the worktree;
pin mutations were made in the worktree's scripts and restored via `git
checkout --` immediately after each single-test run (`git status` clean after
each restore); renders shot with the repo's `scripts/dashboard-shots` tooling
plus two `#process .station` element crops.

## Findings

1. **MINOR — the "Trunk advance" card says "ff trunk to the barred tree",
   but the shipped machinery never fast-forwards trunk.** The advance IS the
   `--no-ff` merge commit: `integrate.integrate_one` runs `git merge --no-ff`
   on the trunk checkout (`integrate.py:2171-2183`) and that one act moves
   trunk; there is no separate ff step anywhere in the module, and a true
   fast-forward is the thing the machinery *forbids* — it would land the
   branch's work commits on trunk as non-merge product commits, exactly what
   the RULING-6 `audit` reds ("every trunk commit in --since..HEAD that
   touches product paths must be a merge commit"). The wording is copied from
   the ruled sketch's mermaid (`docs/concurrency-v2.md` §A2: `"merge --no-ff ·
   ff trunk · unload"`), a two-step shape the shipped code collapsed into one
   act — so this is design-doc shorthand, not invention. But the requirement
   surface is the SHIPPED flow, and drawn one card after the slot's own
   "ancestor check → --no-ff merge" it reads as a self-contradiction (--no-ff,
   then ff). The card's real claim — trunk ends at a commit whose tree is
   byte-identical to the barred branch tip — is true and worth keeping.
   One-string fix: `"advance trunk to the barred tree"` (31 chars, inside the
   34-char `notemax` budget; the `<title>` full text follows for free).
   -> @builder

2. **MINOR — at 390px the station's note lines are illegible without zoom;
   content survives, so this is an observation to file, not a defect in the
   row's scope.** Read off `390px-{light,dark}-process-full.png` plus my own
   390-viewport element crop: the 900-unit viewBox maps to ~350 CSS px, so
   `.stgn` notes render at ≈3.3 CSS px effective. Verified there is NO
   horizontal overflow, NO truncation, and no overlap at that width (the
   builder's claim holds exactly as stated — "390px scales without horizontal
   overflow" is what the spec's constraint asked); titles remain marginally
   readable, the esc list below restates the barrier / arms / ladder /
   lost-race notes in body type, and every card's full text rides a `<title>`
   (mouse-only — a touch reader must pinch-zoom, which vector text supports
   cleanly). The other SVG tabs share this fixed-viewBox behavior, and the
   repo's critique discipline routes render findings to their own WI rather
   than an inline edit — recording it here so it is a named observation, not
   silent. -> @owner (file as its own WI only if 390px reading matters)

## None against — what I tried and could not break

- **The ring is the shipped order, edge by edge.** tick → claim → build →
  {cancelled, handback, merged} → refresh → slot → advance → intake → tick,
  against the code: admission claims serially on trunk then cuts the branch
  (`integrate._claim_locked`: spec move → `commit-tree` → `git branch` →
  trunk advance; the card's "serial trunk commit · branch cut / specs →
  active/<branch>/" is that sequence); one worker session per lane on its own
  worktree (`lane.spawn_worker` → `agent_loop.py --worktree`, N lanes'
  refreshes as overlapping subprocesses — the stacked-shadow multiplicity);
  the three outcome cards derive from `integrate.OUTCOME_DIRS` and are the
  §A3 tree-declared outcomes (`complete/`→merged, `cancelled/`→cancelled,
  `queued/ draft/ deferred/`→handback), all three fanning into the refresh —
  three arrows into one merge, drawn exactly as `branch_outcomes` reads them.
- **The refresh card is `integrate.refresh`'s fixed order, verbatim.**
  "merge trunk in · trunk_step · bar" against the shipped sequence
  (`integrate.py:1980-2033`: `merge --no-ff --no-commit trunk` →
  `_run_trunk_step` → stage → `_refresh_bar` → commit), and "green ⇒
  Bar-Green @ branch tip" against `BAR_GREEN` on the refresh commit —
  derived from `integrate.BAR_GREEN`, not a literal. The slot card's
  "serial · one branch at a time / ancestor check → --no-ff merge" is
  `_slot` (the one lock-acquisition site) + `_merge_ready`
  (`merge-base --is-ancestor` + attestation verify) + the `--no-ff` merge.
- **The barrier, the arms, the ladder and the lost race all trace to the
  dispatcher.** The gate glyph sits on the tick→claim admission edge, which
  is where `_admission`'s wait arm lives ("any exclusive-kind row … stops NEW
  admission outright"); its kind list derives from
  `schedule._KIND_CONCURRENCY` in `_KIND_RANK` order. The esc list's
  empty-frontier ladder is `_station_exit` rung for rung (gap census →
  `intake.mint_gap_rows`, "keep driving" on a mint; else pending cards
  surface; else the honest drain), and "after one lost race the branch takes
  the slot for its retry" is `integrate_one`'s pessimistic arm (the in-slot
  refresh), reached exactly when `_advance`'s per-lane merge finds trunk
  moved — the one dashed edge. The intake card's "amendment · disposition ·
  drafts" maps one-to-one onto `intake_after_merge`'s triggers
  (`_amendment_drafts` / `_handback_drafts`' disposition rows /
  `_disposition_drafts`).
- **Pin 1 bites: one cell of `dispatch._kind_action` flipped reds the pin.**
  Mutation `"spine" → return "exclusive"` (was `"batch"`) →
  `FAILED …::test_station_barrier_and_admission_arms_pin_to_the_dispatcher`
  on `assert set(tp._ADMISSION_ARMS) == truth` ("Extra items in the left set:
  'batch'") — **1 failed in 0.03s**. Restored, clean.
- **Pin 2 follows: an `OUTCOME_DIRS` key rename moves the render, honestly.**
  Mutation `"complete" → "completed"` → the derived station SVG emits
  `specs → completed/` and drops the old label (verified by calling
  `_station_svg` directly: `completed/ in svg: True`, `complete/ … : False`),
  and `test_station_outcomes_derive_from_the_integrator` stays green because
  it derives from the same constant — the follow-the-module contract, not a
  self-pin. Restored, clean.
- **Pin 3 is behavioral, not nominal: it calls what it claims.** Mutation
  making `intake.tier_signal`'s amendment arm return `"medium"`
  unconditionally →
  `FAILED …::test_station_intake_arm_pins_to_the_intake_mint` on
  `assert ink.tier_signal("amendment", rows_touched=4) == "strong"` —
  **1 failed in 0.04s**; the same test asserts the five mint-arm callables
  plus `dispatch.gap_census` exist. Restored, clean; the full module then
  re-ran **34 passed in 6.03s**.
- **The pixels, read not reported.** 1280 light+dark full pages, 1680
  light+dark `.station` element crops (2x), 390 light+dark: the ring reads as
  one directed cycle (13 arrowheads, all visible in both themes); the three
  fan-in arrows converge unmistakably on the refresh card; the slot pops
  white-on-`--slot` (#4f46e5) in BOTH themes with legible sub-labels; the
  double-bar barrier glyph sits on the tick→claim edge with its accent label.
  Both driven fixes verified in the crops: the refresh note reads
  "green ⇒ Bar-Green @ branch tip" WHOLE (no mid-token cut), and the dashed
  lost-race edge starts visibly clear of the slot card's drop-shadow, its
  "lost race → refresh again" label clear of the dashes. The mid-page header
  ghost in the 390 full shot is the documented fullPage sticky-header capture
  artifact, absent from the fold shots.
- **Freshness, determinism, offline.** After the shoot's regen,
  `gen_trajectory.py --check` → "project-state dashboard up to date", rc=0 —
  the fixed-trig/.1f constraint held through the redraw. Zero `http(s)://`
  occurrences in the built page; `test_generates_self_contained_dashboard`
  additionally forbids `<script src` and `cdn`, and the station suite
  re-asserts offline per panel — the no-external-assets claim is honest.
  `test_station_byte_identical_without_data` covers the data-less-repo
  constraint.
- **Hygiene.** `PROJECT_STATE.html` is NOT in the branch's own delta
  (`git diff 78944578..8874f695 --name-only` — ten files, no dashboard; the
  claim commit carrying it is trunk-side bookkeeping, on trunk).
  `check_trajectory.staged_spine_amendments(root, 78944578, 8874f695)` →
  exactly 3 records, ALL `"ratified": {}` — LLR-056 `CodeSymbol`
  (`process_panel/_loop_panel` → `process_panel/_station_panel`) and
  TC-051/TC-056 `Evidence` (→ the real `tests/test_traj_panels.py` nodes,
  all of which exist and ran) — traced cells outside `ROUTED_TRACED_CELLS`,
  silent by the §A5 ruling exactly as the Deliverable claims. The
  SR-050/SR-055/LLR-051/LLR-056/TC-051/TC-056 ratified-prose deferral is
  honest per §A9.1: the prose amendment is clause-1 program-close scope,
  WI-390's spec carries the catch-all ("Any further amendments the seven
  builds surface land here too") plus the `~WI-389` edge, and the deviation
  is recorded on the closed row's Deliverable where that builder claims from.
  The SpecRef re-validation is recorded and checks out: `git show f822e336`
  touches only the §B2 "Specs mirror it" restatement (~line 880), not
  §A2/§A3/§A4/§A8 — and the WI-389 SpecRef WARN is gone
  (`check_trajectory --strict` shows only the WI-390 clock WARN, present on
  trunk too, count-verified).
- **The record, re-run at `8874f695`.** `tests/test_traj_panels.py` →
  **34 passed in 6.03s** (the Deliverable fig says 34 in 6.12s — exact count
  agreement; this is the spot-checked declared figure). Smoke → **667
  passed, 2 skipped in 12.79s**, re-run clean AFTER all mutation restores
  (the Deliverable's 663/6 is stamped at `56dc580d`; the delta is trunk-side
  suite growth + environment skips, the shape this review family has recorded
  before). `check_trajectory --strict` rc=0 (WARN set: the pre-existing
  connectivity/IF drift §A9.1 hands to WI-390, plus WI-390's own clock —
  nothing about WI-389); `check_doc_refs --strict` rc=0;
  `check_figures --strict` rc=0, **72 declared figure(s), every one carrying
  its command and revision** — matching the close claim exactly.
  `test_complexity_ratchet` + `test_traj_render` + `test_traj_render_sweeps`
  → **45 passed**; `test_module_size_ratchet` → **1 passed** (traj_panels
  1145 lines, gen_trajectory 952 — the facade grew only the re-export rename
  + the `--hub`→`--slot` token block, exactly as claimed, seen in the diff).
  `ruff check` over the five changed Python files: All checks passed.
  `docs/work` delta is WI-389-only (the one spec, active/ → complete/). The
  full-suite fig (1959/10 at `56dc580d`) is the BUILDER'S, attributed not
  re-run — module + smoke + strict + my own renders are this review's tier.

**THIS IS AN APPROVE:** the redraw's load-bearing promises — a truthful
picture of the shipped cycle, vocabulary derived or pinned so the dashboard
can never again be green while the loop changed, pixels verified rather than
source read — all held under adversarial checking: the topology walk found
the machinery, all three pins red (or follow) under my own mutations, and
both driven fixes are visible in shots I took myself. The two findings are a
one-string vocabulary correction the merge does not need to wait for (it is
the design doc's own shorthand, wrong only against the sharper truth the
shipped code earned) and a recorded 390px observation. Neither changes what a
reader takes away: every lane ends in a merge, through one serial slot.

VERDICT: APPROVE findings=2
