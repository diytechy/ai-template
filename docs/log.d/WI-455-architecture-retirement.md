## 2026-08-14 — WI-455 (open): docs/architecture.md retired — the architecture derives into the dashboard

**One line:** the sitting-2 decision-8 program executed through its last act —
the markdown way-station between the registries and the dashboard is deleted,
its narrative moved to an authored-and-checked home, its structure derived
live — with the D-3 `direction`/`counterpart` shed and the `external.toml`
context view left as the recorded remainder (the lane stays open).

**Five commits** (`b80a7816` → `2ffa85a4` → `fc750548` → `e670b030` → `7001818f`, the last regenerating the derived gate after LLR-038's in-process flip moved the basis to modified=52 — the WI-442/WI-454 precedent):

1. **The flows move** (deliverable 1): the "Shape of the product" narrative
   and the four Runtime flows moved **verbatim** to
   [`../runtime-flows.md`](../runtime-flows.md); `check_flows.py` re-pointed
   its default there (the obligation followed the home — SR-013's checker
   never lapsed); `gen_okf`'s process-guide entry followed;
   `RUNTIME_FLOWS.template.md` scaffolds it downstream.
2. **Registries/source → dashboard, no way-station**:
   `gen_arch_map.scan_inventory()` is the ONE AST walk, and
   `check_trajectory.arch_inventory`, `traj_parse.sw_modules` and
   `check_doc_refs`' `sym:` oracle read it live instead of parsing the
   committed MODULE MAP block back. The dashboard's How-SW tab now also
   **embeds the authored flows** (`traj_views.flows_block`), so
   `PROJECT_STATE.html` carries the full architecture. The WI-399
   committed-vs-disk delta family retired with the gap it bridged; the
   containment finding now names the uncontained modules. Draft seam rows
   IF-123/IF-124 minted for the two new imports (id watermark IF 122 → 124).
3. **The scaffold surface** (deliverable 2): `ARCHITECTURE.template.md`
   deleted, the MAPPING row removed, the `arch-map` harness step retired
   (check.py, the hook's batched floor, `trunk_step --regen`, the
   `[generated]` rows), `[arch-map] mode` re-purposed as the AST-inventory
   dormancy dial, `check_doc_refs --arch` retired, `gen_arch_map --doc` now
   required (opt-in agent-file routing only). `RESYNC_PACK.md` carries the
   `[since c7adf7dc]` migration entry (anchored at the LANDED sha; `b80a7816` was the pre-rebase one). **Verified by driving a real
   scaffold**: bootstrap → no `docs/architecture.md`, `docs/runtime-flows.md`
   present, `check_flows` OK, `check.py --gate DevStg-Reqs` PASS, the hook's
   batched floor PASS. (Re-driven at the 2026-08-18 landing on the rebased
   branch — same result, now under the `DevStg-*` one-vocabulary spelling.)
4. **The deletion + records**: six referrer links repaired mechanically (the
   `659f9b84` precedent — targets move, record text does not);
   `docs/declared-absences` gains the retired path with its reason (closed-WI
   citations reclassify as explained-untraced — the mechanism's designed
   purpose); IF-010/023/024/028/029 contract cells and LLR-038 re-pointed
   in-process (LLR-038 Verified → **Modified**; nothing self-ratified);
   PROCESS/PROCESS_OPTIONS/ADOPTING/AGENTS.template re-pointed; ratchets and
   byte baselines re-stamped with reasons.

**Deliverable 3 — the per-block disposition of the ~192 hand-authored lines**
(line numbers in the pre-move file at `2780c1a1`):

| Block | Lines | Disposition |
|---|---|---|
| Title + intro | 1–10 | **retired** — superseded by `runtime-flows.md`'s own intro (the self-adoption framing moved with it) |
| "Shape of the product" | 12–30 | **moved verbatim** → [`../runtime-flows.md`](../runtime-flows.md) §"Shape of the product" |
| "Module dependencies (generated)" header | 32–39 | **retired** — its two claims re-homed: the cross-CMP rule's input is stated in `check_trajectory.arch_inventory`'s docstring; the freshness story died with the step |
| GENERATED DEPENDENCY DIAGRAM block | 41–271 | **derived** — the import graph + seams render from `scan_inventory` + the registries (dashboard); the Mermaid twin remains producible via `gen_arch_map --doc` |
| "Module map" header | 273–278 | **retired** — the step description died with the `arch-map` step; the map's story lives in PROCESS.md §3 + `gen_arch_map`'s docstring |
| GENERATED MODULE MAP block | 280–1469 | **derived** — `scan_inventory` → the dashboard's How-SW module table/drill |
| "Runtime flows" heading + intro | 1471–1475 | **moved** (re-authored intro) → `runtime-flows.md` |
| Flow-4 inherited-drift note | 1477–1487 | **moved verbatim** → `runtime-flows.md` |
| Flows 1–4 (diagrams + prose) | 1489–1613 | **moved verbatim** → `runtime-flows.md`; `check_flows` validates 4 diagrams, 47 cited ids, all known |

**Deviations / recorded residue:**

- **The honest remainder (lane stays open):** the sitting-2 **D-3/D-4
  `direction`+`counterpart` deletion** (115 rows each, held by
  `interfaces.toml`'s header with this WI named as owner) and the
  **`external.toml` context view** (entities/BIF/relationships rendered into
  the dashboard — the spec's own "may land as its own slice"). Measured this
  session: the docstring `Contracts:` convention recovers only 3/66 seam
  edges and covers 0/32 cross-CMP pairs without `counterpart`, so the shed
  requires re-authoring the ~85 consumption-shaped IF rows into
  definition-shaped rows plus a re-keyed seam-of-record — spine-heavy design
  colliding with the live WI-451 re-tier, not landable at quality in this
  session's remainder.
- `docs/work/queued/WI-452`'s Context still cites the deleted path — another
  WI's spec, deliberately not edited by this lane.
- `docs/status.md`:48 hand prose still names the retirement as pending —
  hand prose is not this lane's to edit; the next sitting owns it.
- Sequencing for the queued gen_arch_map programs recorded at the seam:
  `scan_inventory`'s docstring names WI-390 clause (2) and WI-448 as
  inheriting it as the consumers' single entry point.

**Byte deltas:** AGENTS.template.md 9,994 → 9,953 (47 headroom under 10,000);
PROCESS.md 73,617 → 73,500 (−117, re-pointing shrank it; baseline re-stamped);
PROCESS_OPTIONS.md 171,916 → 171,915 (−1; baseline re-stamped).

**Ratchets** (reviewed, reasons at each stamp): bootstrap.py 2848→2852→2830;
check_trajectory.py 4120→4001; check.py 1806→1787; C901
`gen_arch_map.py:main` 17→18.

**Bars:** full unfiltered suite green — 2481 passed, 11 skipped
<!-- fig: cmd="python -m pytest -q -n auto" rev=7001818f -->
`check_trajectory.py --root . --strict` clean (452 work items, graph acyclic;
two pre-existing shared-specref WARNs)
<!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev=7001818f -->
`check_docs --stale` 0 broken links; `check_doc_refs` at its 30-dangling
pre-program baseline; a real scaffold bootstrapped and green end to end.

---

## 2026-08-18 — LANDED: rebased onto the EARS/vocabulary trunk

The five program commits above plus this fragment were authored 2026-08-14 and
never merged. They are **rebased onto `ff03d323`** (the
`requirements/ears-and-quality-characteristics` tip) as
`c7adf7dc` -> `42a40660` -> `f3f60a60` -> `5f4c5274` -> `ad6aeb97` -> tip; the
pre-rebase shas are dead. ~22 conflicts, resolved on ONE rule: **keep HEAD's
newer vocabulary and re-tiered spine, apply WI-455's retirement.** The three
dispositions that were more than a re-spelling:

- **The flows themselves are HEAD's, not the branch's.** The branch's
  `runtime-flows.md` carried a 2026-08-14 copy citing `SR-029/030/060/057/093/
  115/131/132` — ids the **WI-451 re-tier deleted**. Keeping it would have
  shipped a flows doc that `check_flows` refuses. The moved section is
  therefore taken from HEAD's `docs/architecture.md` at `ff03d323`, whose
  citations the re-tier had already re-pointed onto the carrying LLRs. The MOVE
  is the branch's; the TEXT is trunk's.
- **`IF-123`/`IF-124` renumbered to `IF-131`/`IF-132`.** The branch minted the
  two `scan_inventory` seams at 123/124; trunk had since minted 123–130 for the
  baseline-snapshot family. Same crossings, new numbers, ported onto the
  interface schema trunk now carries (`req_refs`/`owner`/`status`, not
  `sr_refs`/`approval`). Watermark raised IF 130 -> 132.
- **`Shape of the product` still cited two deleted ids.** Moving it into the
  doc `check_flows` scans is what exposed it: the section cited `SR-057`/
  `SR-132`, deleted by the re-tier, and was never swept because it sat OUTSIDE
  the scanned section in its old home. Re-pointed onto `LLR-058`/`LLR-140`,
  matching the re-pointing Flow 4 already carried.

Three HEAD-side tests (`test_trunk_step.py`, SR-173, added 2026-08-17) pinned
the regen contract THROUGH the `arch-map` step this WI retires. Their intent is
live, so they are **ported, not deleted**: the dependency-order list drops
`arch-map`, and the two no-partial-commit pins move onto `okf` as the green
producer with the failure planted at `derived-gate`'s output path — `okf` is
step 1 now and reads every registry, so a malformed-registry failure can no
longer land *after* a green step. Contract asserted is unchanged.

`traj_views.FLOWS_STYLE` (the new How-SW flows panel) shipped literal
`border-radius:8px`/`font-size:12px`, which trunk's U1/U3 design-token tests
refuse; re-pointed onto `var(--r-ctl)`/`var(--tiny)` (12px is `--tiny` exactly,
so the render is byte-equivalent in size). Dead `ARCH_MD` constant deleted with
the file it named.

**Bars at landing:** full unfiltered suite **2568 passed, 11 skipped**
<!-- fig: cmd="python -m pytest -q -n auto" rev=PENDING -->
`check_flows` OK (4 diagrams, 40 ids, all known); `check_vocab --strict` clean;
a real scaffold bootstrapped green (`check.py --gate DevStg-Reqs` PASS, no
`docs/architecture.md`, `docs/runtime-flows.md` present).

**Byte deltas at landing** (against the `ff03d323` baselines this branch
carries): AGENTS.template.md 9,994 -> 9,953 (47 headroom under 10,000);
PROCESS.md 81,763 -> 81,649 (-114, re-pointing shrank it; baseline re-stamped);
PROCESS_OPTIONS.md 172,037 -> 172,036 (-1; baseline re-stamped).

**Merge-time reconciliation owed:** `CLAUDE.md` and `PROCESS.md` have
uncommitted edits in the main working tree (a CLAUDE.md diet and a PROCESS.md
prose pass) that this branch could not see; the byte baselines above are stamped
against `ff03d323`, so whichever lands second re-measures. The lane also still
owes the honest remainder recorded above (the D-3/D-4 `direction`/`counterpart`
shed and the `external.toml` context view).

