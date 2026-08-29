## 2026-08-29 — WI-528: the interface row shape in code (OI-67 slice 1)

Deferred open items: none — the shape was ruled the same day, and the two
questions this slice raised were answered by the owner in-session and folded
in (below).

**Summary.** The IF tier's row is now one OWNER, its FAR SIDE, and a TYPED
STATEMENT. Every reader and check in the plan's §2 table reads the new cells;
the kit's own registry is converted, mechanically, with the legacy `contract`
cell kept readable and counted until slice 3 gives its content a home.
Record of the shape: [plans/2026-08-29-if-row-shape-plan.md](../plans/2026-08-29-if-row-shape-plan.md)
§1 (its decisions 8 and 9 were added by this slice).

**What the owner changed while the slice was under way, and why it was
cheap to take now.** The first build flattened direction into one
`consumers` list and let `channel` imply it. The owner's objection — *"the
owner defines the arguments, but receives them"* — had no cell. The far side
now NAMES the direction: `requestors` put information into the surface the
owner defines (they call, invoke, set, write), `consumers` take what it emits
(they read the file, the exit code, the stdout); exactly one per row, checked
by `trace.py` under `--strict`. A call is one row; a CLI's arguments and its
exit code are two. The graphs draw the arrow the way the information runs
(`gen_arch_map._seam_edges`, both `traj_views` seam graphs); placement and the
cross-component rule are direction-blind and read `seam_far_side`. Seeded
from the channel — `cli`, `env`, `call` rows name requestors (70 rows), the
rest consumers (66) — and confirmed row by row in slice 3. The second
question, parallel workers coding against a header that does not exist yet,
is answered header-first (plan decision 9) and lands in `PROCESS.md` §8 at
slice 5.

**The shape, as shipped.**

- `owner` — the providing THING, one spelling with the far side: a module
  path, a file or directory path, or `external:<party>`. An id-shaped owner
  and a multi-endpoint owner are strict findings; a module-shaped owner that
  no design row's `Module` names and whose header declares no `Implements:`
  line is a warn-only advisory (`_implementing_modules` reads the AST surface
  the symbol tripwire already read). 4 rows warn on this tree.
- `requestors` | `consumers` — exactly one; both typed arrays.
- `channel` — closed, `kitlib.spine.IF_CHANNELS`: `cli`, `exit-code`,
  `stdout`, `file`, `call`, `env`, `git`, `bytes`. Named `channel`, not
  `kind`: `kind` is the relationship tier's column (D-3). Seeded from the
  2026-08-29 per-row classification — a classification, not a reading, and
  the header says so.
- `data` — optional, ≤160 characters; the five rules that policed `contract`
  (`if_data_advisories`) read it unchanged, symbol/path tripwire included.
- `contract` — LEGACY: read, counted by ONE summarizing advisory
  (`if_legacy_contract_advisories`: 136 rows today), retired at slice 6.
- Retired outright: `provider`, `req_refs`, `signal`, `signal_note`;
  `if_ownership_advisories`, `if_provider_advisories`, `_owner_llr_module`,
  `seam_provider`, `load_seam_modules`, `spine_carrier.llr_modules`, the
  derivability report section and its `Findings` field.

**The registry conversion, and where judgement entered.** `owner` folded
from the stated `provider` (30 rows) or the LLR owner's single module (85);
the 21 published-media rows no cell ever named got their medium by hand
(`docs/requirements/`, `docs/stack.ini`, `docs/work/`, `docs/process.toml`,
`docs/reviews/`, `project-trajectory/skills/`, …) — every one resolves in the
tree and every one is a slice-3 confirmation. `IF-144` is owned by
`scripts/check`, where OI-66's build declared it. `IF-045`'s two-file
provider (`agents.toml; agents-enabled`) is one owner now (`agents.toml`) —
the second medium is a slice-4 split. The header of `interfaces.toml` was
rewritten for the shape (the old one described five cells that no longer
exist); the notes cells arguing "owner = SR-006, not SR-007" are now moot
and leave in slice 3 with the contract text.

**Shipped surfaces pulled forward from slice 5,** because a template that
documents cells the code no longer reads is the WI-527 4b defect again:
`interfaces.template.toml` (header and the `-000` row, which carries the
legacy `contract` key while the schema still states it — the three-leg
dogfood rule requires it) and `INTERFACES.template.md`'s field table.
`PROCESS.md` §8, `PROCESS_OPTIONS.md` and the two reference docs still
describe the old shape and are slice 5's.

**Tests.** 31 modules touched the IF tier; two Opus workers rewrote the
fixture-based and trace-based halves against the code (their reports are in
the session transcript; every test's intent was kept, names changed only
where the old name would lie), and the seam-resolution invariants were
rewritten for the new shape. Three renamed tests: `TC-182`'s evidence cell is
re-pointed at `test_channel_refuses_an_unknown_value_as_a_warn`. Ratchets:
`trace.py` +3 net (5819 → 5822 — a larger swap, reason on the stamp),
`intake.py` +4 (the direction arrow in a brief's seam lines),
`check_trajectory.py` −2 and `gen_arch_map.py` −20 re-stamped down in the
same commit.

**Gates.** Commit bar (smoke tier + budget + `check_docs --stale`) and the
full suite, both green; totals at the foot of this entry.

**Deviations from spec:** the far-side pair (`requestors`/`consumers`) is
NOT in the ruled brief or the plan's first cut — it is the owner's in-session
addition, recorded as plan decision 8. The seeded `channel` and far side are
classifications, confirmed in slice 3, not readings.

**Byte deltas on budgeted files:** none touched.

**pytest totals:** full suite `python -m pytest -q -n auto`: 3068 passed, 15 skipped in 581.27s (0:09:41); smoke tier: 1362 passed, 6 skipped in 19.61s; `check_smoke_budget.py --mode enforce`: 21.3s and 23.9s vs 60s -> within (one earlier reading of 95.7s came straight after the full suite on the same box and was not reproduced — one machine, one data point; the budget is not moved). `check.py` harness: PASS.
