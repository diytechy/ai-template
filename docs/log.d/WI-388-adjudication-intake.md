## 2026-08-02 — WI-388: the adjudication kind and the unified intake mint

**Summary.** The last row of the concurrency-v2 program's core sequence, built
exactly as amended 2026-08-01: the `adjudication` kind fills the rank-1 slot
§A1 reserved (exclusive, NO product bar); the unified trunk-side intake mint
(`intake.py`, the new kit sibling) seals the R1/R3 id invariant — a WI id is
created only by a human trunk commit or that helper — with three triggers and
the drafts-not-mints arm; the `bar` strictness key crosses every loader table;
the context block renders the pure registry joins for three consumers; both
gate-policy arms of ruled decision 2 are built and tested; and the two cells
WI-380 left unclassified are RULED (below, loudly). Five build commits, each
at the smoke bar: the kind + schema + cell rulings (900dac6a), the mint +
triggers + wiring (b4e7cd0b), the context block (d0131ce6), the policy arms
(082dc25a), the registration (d5805460).

**The two-cell ruling (the spec's intake from WI-380 REVIEW-A finding 3),
disclosed loudly.** Recorded at the cell-split table's home
(`check_trajectory.SPINE_TRACED_CELLS` / `SPINE_RATIFIED_CELLS`) and pinned by
`tests/test_trajectory_staged.py`:

- **LLR `SR-Refs` → TRACED, routed to adjudication** like its two pointer
  siblings (`SN-Refs`, `Verifies`): it is the same shape of pointer — which SR
  owns this decomposition row — re-pointing it changes no attested prose on
  either side, and whether the re-point moved scope is exactly the judgement
  the adjudication kind exists to make. The asymmetry argument carries
  unchanged: a spurious window costs an owner sitting and four review rounds;
  a spurious adjudication costs one bar-less WI. Driven: an `SR-Refs`
  re-point is silent at the amend-without-flip warn but mints the
  adjudication row at intake; a `Module`-only move stays silent everywhere.
- **SR `SupersededBy` → RATIFIED, confirmed** (no longer the residual's
  accident): a supersession IS a scope statement — it terminates a
  requirement's lifecycle in favour of another, precisely the "prose and
  relevant field attributes" of the owner's spine-touch definition. Unlike
  the traced pointers it re-points no live chain; it ends one, and a silent
  supersession would be a missed window nobody sees.

**Deliverables.**

- **The kind** (§A5.2): `adjudication` in `SAFETY_CLASSES` — exclusive,
  rank 1 (the reserved slot, filled without renumbering the ruled table),
  dispatching per the §A8 table's existing exclusive arm. Its lane runs NO
  bar: `integrate._lane_bar_directives` (read off the same trunk claim the
  slot reads) + `_refresh_bar` — the refresh still merges trunk in, runs the
  trunk step and commits a verified `Bar-Green` attestation whose summary
  reads `no-bar (adjudication, §A5.2)` honestly; a mixed batch or unreadable
  frontmatter fails TOWARD the bar.
- **The unified mint** (`intake.py`; rulings R1 + R3): deterministic id =
  max+1 over every spec FILENAME under `docs/work/` (`active/<branch>/`
  included), derived descriptions, no model in the path, one claim-shaped
  bookkeeping commit (regen folded per RULING-6), all-or-nothing restore,
  idempotent by exact-title dedup (`intake.py sweep|census|adjudicate` is the
  by-hand/recovery surface). Trigger (a): the ratified/ROUTED-cell diff on
  the merged commit via `check_trajectory.staged_spine_amendments(root,
  before, after)` — the WI-380 seam consumed as-is — wired at the one honest
  hook point, `integrate_one`'s post-merge arm (merge landed, slot still
  held, serial by construction). Trigger (b): a merged spec carrying
  `## Handback` mints the DISPOSITION row — same kind, outcomes `cancel /
  defer / re-queue with drafted follow-up / surface an open item` verbatim in
  its title; the no-recursion invariant is STRUCTURAL at both ends
  (`handback._no_recursion_refusal` refuses the act; intake refuses to mint a
  disposition FOR an adjudication row). Trigger (c): the dispatcher's
  empty-frontier rung 1 now HANDS the census to `intake.mint_gap_rows` and
  KEEPS DRIVING the rows it minted; dedup against every existing row makes
  the ladder loop-proof, with the honest exhausted banner when every gap
  already carries a row. Drafts-not-mints: a merged adjudication row's
  `## Dispositions` fenced-TOML drafts mint at ITS merge, validated loudly
  (unknown key, a second `adjudication` kind, dual+declared-class
  contradiction, bad `bar` — each refuses with nothing minted);
  `planmode = "dual"` is the deeper-review route with the kind DERIVED from
  it. Tier signals are measurable: rows touched + a moved `docs/gate` (a),
  the handback reason class — NEEDS-HUMAN routes strong (b), census medium (c).
- **The `bar` key**: optional `bar = G1|G2|G3`; the refresh passes the
  batch's strictest value to `check.py --gate` (driven off the recording
  stub's own argv), a malformed value refuses loudly, and the schema note is
  verbatim in every loader table: *bar declares verification strictness for
  this row's lane; it never affects scheduling* — `load_wis` structurally
  never parses it. The column landed in wi_convert / the three F5 reader
  copies / plan_artifacts / the shipped template header together, pinned by
  `test_wi_loader_sync` and the header pins.
- **The context block** (`intake.context_block`): pure registry joins in
  failure-cost order — cancelled precedent sharing `sr_refs` WITH ITS
  REASONS first (the measured WI-391 failure mode), pending OIs whose
  WI-Refs intersect kin, the LLR/TC code map, CMP knowledge packs, IF seams
  via LLR.Module, precedent reviews — advisory-never-gating, clipped like
  `pred_block`. Three consumers: every minted row's `## Context` at mint;
  `agent_loop.worker_prompt` computed FRESH at claim with the one new
  instruction line; and the warn-ONLY pack-citation check
  (`check_trajectory.knowledge_pack_findings` — the same join re-derived
  under that module's F5 independence; zero warns on this repo's live
  registry, measured).
- **The gate-policy arms** (ruled decision 2): `adjudication_action` —
  recommend-only under `attended` (the flip is a ratification and under
  attended ratification is the human's; the prepared brief is most of this
  row's win), flip under `single-ratify`/`autonomous`; unknown levels fail
  toward recommend, never toward a machine ratification. `flip_verified` +
  the `adjudicate` CLI move ONLY the named `Modified` Status cells
  (cell-exact elsewhere; byte-identical on the live registries — measured),
  idempotent, whole-or-nothing on an unknown id. Both arms tested; attended
  is the kit default even though this repo runs autonomous.

**Deviations from spec, recorded.** (1) §A5.2's "a Deliverable body listing
each changed row, cell and before/after" predates R-A (Deliverable non-empty
iff terminal), so the derived listing lands in the minted row's TITLE plus
the advisory `## Context` section — which the amendment added to the body
grammar anyway. (2) Consumer 3 re-derives the pack join inside
check_trajectory instead of importing `context_block`: the F5
independently-copyable rule wins over "one function, three importers" for the
module the shipped hook runs. (3) The census dedup is against EVERY row, not
open rows only — a gap row that closed without clearing its gap must not
re-mint on the next idle tick of a walk-away loop; re-opening a failed gap is
a human judgement. (4) `test_dispatch`'s rung-one pin ("reports the census
and mints nothing") was REWRITTEN to the ruled behaviour it was explicitly
holding the door for: mint, drive, dedupe, honest exit. (5) TC-144's Method
was amended to match (a ratified cell of a Verified row, no flip) — so this
WI's own merge is expected to mint the adjudication row for it: the machinery
dogfooding itself; expected judgement no-scope-moved, enacted with
`python project-trajectory/scripts/intake.py adjudicate` under this repo's
autonomous policy.

**Budgets and stamps** (each with its reason at the entry): sizes —
integrate 2251→2353, check_trajectory 3428→3531, agent_common 1824→1839,
agent_loop 2985→3007, bootstrap 2267→2278; intake.py enters at 1050 lines
(under the 1500 threshold); complexity held under C901 by extraction
(`_refresh_bar`, the flip's locate/apply split, `_no_recursion_refusal`,
`_cli_result`) — no baseline bumped. Dupes census: the reader + schema
classes re-fingerprinted (six lines), one new `intake-mint` class (9 blocks,
each reasoned), cli 90→96; two would-be blocks dissolved by reusing
`agent_common._read_csv_rows`/`_refs` instead of copying them. Smoke budget
max-tests 660→700 —
declared figure: 661 smoke-tier tests collected
<!-- fig: cmd="python -m pytest -q -n auto -m smoke --collect-only" rev=d5805460 -->
No byte-budgeted doc (AGENTS.template.md / PROCESS.md / PROCESS_OPTIONS.md)
was touched. `docs/gate` re-derived (basis counts moved with the three new
LLR + three new TC rows; value G3 unchanged).

**REVIEW-A rework (2026-08-02; CHANGES-REQUESTED findings=5, all closed —
the verdict record is [WI-388-REVIEW-A.md](../reviews/WI-388-REVIEW-A.md)).**
Finding 1 (MAJOR): the no-bar arm was kind-gated only, and the reviewer
drove a product file with a red check harness through an adjudication-only
lane onto trunk unbarred — an un-run green against §A8's fixed points. Closed
structurally with the diff-scope rung: `integrate._adjudication_scope_ok`
honours the no-bar path only when the branch's non-refresh delta
(merge-base → peeled work tip, the `_minted_id_refusal` read) stays on the
§A5.2 surfaces — docs/work/, the three spine registries, open-items.csv
(the R3 surface-an-open-item outcome), docs/gate, docs/log.d/,
docs/reviews/, plus the declared [generated] set; ANY other path fails
toward the full bar. The reviewer's drive is the shipped regression
(red-then-green: the harness now RUNS and reds; the pure-registry lane with
a spine Status edit keeps no-bar). Finding 2 (MAJOR): the intake→wi_convert
cross-component import was undeclared and the branch would have redded its
own merge refresh at the arch-map regen; IF-092 (Consumes, the IF-078
shape) + the Contracts line close it — verified by scratch regen:
`check_trajectory --strict` rc=0 and the warn list byte-identical to the
trunk baseline (11 warns, zero delta), which also proves finding 4's
TC-147/148 Verifies citations (IF-091/IF-090) cleared the two Active-seam
warns. Finding 3: the disposition title now carries the handback MERGE's
sha (`_rev7`), so a re-queued row's second handback mints its own
disposition — two-handback sequence driven red-then-green, same-event
re-runs still dedupe. Finding 5: the smoke-budget figure re-measured under
its own rev pin (669 collected at 81147e33; budget 700, ~4.6% headroom).
Sizes: integrate 2353→2417 (the rung, reasoned at the entry).

**Verification** (watched, this tree):
full suite, post-rework: 1961 passed / 5 skipped in 318.50s (0:05:18)
<!-- fig: cmd="python -m pytest -q -n auto" rev=81147e33 -->
(the pre-rework close measured 1959/5 at d5805460; a first run there red one
test on the stale `docs/gate` cache mid-close, re-derived then fully green)
smoke tier, post-rework: 667 passed / 2 skipped
<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=81147e33 -->
`trace.py --strict` rc=0 · `check_trajectory.py --strict` rc=0 ·
`check_doc_refs.py --strict` rc=0 · `check_figures.py --strict` rc=0 ·
`derive_gate.py --check` rc=0.
