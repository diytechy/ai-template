# Shipped-docs staleness audit — 2026-08-17

**The question (owner, 2026-08-17):** have `PROCESS.md` and its associated
shipped files kept up with the newer processes, and is there a work item for
updating them? **The answer:** no general work item existed — WI-390 owns the
concurrency prose, WI-455 the architecture prose, WI-452 the resync-helper
surfaces, and nothing owned the rest. This audit is that missing sweep's
evidence; **[`WI-471`](../work/complete/WI-471-shipped-docs-resync-sweep.md)**
is the missing work item (executed 2026-08-17, log `2026-08-17j`).

**Method + provenance.** Two read-only subagent audits ran 2026-08-17 (log
`2026-08-17i`): one over the load-bearing core (`PROCESS.md`,
`PROCESS_OPTIONS.md`, `AGENTS.template.md`; `docs/process.md` +
`docs/process-options.md` are a declared omission — the masters live in
`project-trajectory/`, per `docs/declared-absences`), one over the satellite
shipped surfaces (`EXAMPLE.md`, `ADOPTING.md`, `MULTI_REPO.md`,
`RESYNC_PACK.md`, `registries/*.template.*`, the kit-scope skills, both
READMEs). Both audited against the ruling record — the log's
`2026-08-13`…`2026-08-17h` Decisions, sitting-3 §0.4, the live
`docs/requirements/*.toml` headers, `docs/registry-machinery-reference.md` —
and against `tests/test_dogfood_sync.py`, so nothing a test already pins is
re-reported. Every finding carries file:line and the ruling it contradicts;
findings are classed **A** (contradicts a landed ruling — update owed),
**B** (describes a state still open/provisional — must NOT be updated yet),
or covered-elsewhere (an open WI already owns it).

## Verdict

**Substantially healthier than feared, with the staleness concentrated, not
diffuse.** The heavyweight 2026-08 doctrine — the D-9 status vocabulary
`{Drafted, Approved, Modified}`, one-decision tiering R1/R2/R3, the interface
model (`owner`/`carried_by`/`approval`/direction-is-flow), the derived gate,
the WI spec-folder carrier, the gate-authority presets — **has landed in the
shipped docs**. `AGENTS.template.md` owes nothing outside WI-455's bullets;
22 of 23 kit skills are clean; the registry templates are current where the
dogfood census pins them. The real debt: **`EXAMPLE.md` is the stalest
surface** (retired markdown/CSV carriers, four illegal `Status=Implemented`
cells, an owner-less IF snippet); the two READMEs carry ~9 row-level ruling
contradictions (including a live-dial contradiction —
`human_ratification_through` documented as `0`, live value `4`); the core
docs carry ~20 residual retired-carrier/vocabulary tokens plus **three landed
mechanisms they never describe** (the hats registry, the `external.toml`
boundary frame, the `last_approved` snapshot); and `RESYNC_PACK.md` §3 has no
entry for the hats layer, so a range-selected resync never learns of it.
**No shipped surface prematurely adopts an unruled state** — that check ran
both directions and came back clean.

## Class A — contradicts a landed ruling (31 findings; WI-471's scope)

### Core (13)

| file:line | quote fragment | what the record says | ruling |
|---|---|---|---|
| PROCESS.md:326-330 | "dial in docs/process.toml, one of three levels: `attended`… `single-ratify`… `autonomous`" | the dial is 0–4; the three words are `--gate-policy` presets, translated and never stored (SN-029 retired the enum); the record already flags this paragraph as rot | `2026-08-15m` (v) |
| PROCESS.md:59-63 | hat table paths `stakeholder-needs.md`, `system-requirements.csv`, `test-cases.csv` | every spine + IF/CMP/OI registry ships and lives as TOML | carrier cutover (2026-08-08; WI-442/443) |
| PROCESS.md:147, 183, 296, 861, 945 | "CSV columns are authoritative" et al. | same — retired-carrier tokens | same |
| PROCESS.md:407-408 | "changed `Stable` interface versions" | `stability` retired; the one maturity field is `approval` | `2026-08-13u` D4 |
| PROCESS.md:345-346 + PROCESS_OPTIONS.md:179-182, 266 | "an SN out of its draft section" / heading-contains-"draft" | SN maturity is a FIELD (`kind`), not a section. *Timing: fix rides item 6's execution (SN gains `status`; `kind` dies) so it isn't rewritten twice* | template header; §0.4 item 6 |
| PROCESS_OPTIONS.md:1778, 1787-1789 | "a `Status=Proposed` row at filing" | interfaces have no `Status`/`Proposed`; maturity is `approval = drafted\|approved` | `2026-08-13u` D4; D-9 5b |
| PROCESS_OPTIONS.md:2160 | "each `Active` seam" | no `Active` value exists | same |
| PROCESS_OPTIONS.md:2145-2147 | "`SR-Refs` links the spine" | renamed `req_refs` (Q1 polymorphism) | `2026-08-15e` |
| PROCESS_OPTIONS.md:711, 917, 1739, 1751, 1776, 1796, 1804, 2138, 2151, 2167, 2242, 2447 | `*.template.csv` / live-voice `work-items.csv` | all TOML; WI carrier is the `docs/work/` folder (the legacy-CSV dual-read paragraph at 1664-1668 is correct and stays) | WI-442/443; Phase 2c |
| PROCESS.md:68-80 (§1) | "add discipline hats at setup… record the active hats in `status.md`" | hats are a shipped registry (`hats.toml`, `applies_when`, roster at DevStg-Boundary, hat-derived labels); status.md is not the home | OI-19; `2026-08-16l`; `2026-08-17a` |
| PROCESS.md §4/§8 (gap) | DevStg-Boundary described with no registry named | the frame is a shipped registry — `external.toml` entities/crossings/relationships, `boundary_refs`, tie-backs | `2026-08-13i/l/m` |
| PROCESS.md §4 ~355-368 (gap) | re-attest described with no baseline mechanism | approvals copy registries to `docs/archive/last_approved/`; diffs run against the snapshot (replaced the hash anchor). *Describe the mechanism only; first seed + UNANCHORED ERROR are step-7/sitting pending* | `2026-08-15d/g` |

### Satellite (18)

| file:line | quote fragment | what the record says | ruling |
|---|---|---|---|
| EXAMPLE.md:11, 31, 41, 61 | `system-requirements.csv` / `stakeholder-needs.md` + SN section-as-state tables | TOML carriers; section-as-state retired for `kind` | repo-lock D-5 |
| EXAMPLE.md:36, 45, 46, 162, 276 | `Status=Implemented` (SR-002, LLR-001/002, SR-101, SR-050) | closed vocabulary; out-of-vocab = integrity finding on the always-on floor (the 3771c003 sweep missed these) | `2026-08-15g/m` |
| EXAMPLE.md:285-305 | §9 IF rows with no `owner` key | exactly one `owner` per IF row | `2026-08-15a/e` |
| ADOPTING.md:293, 297 | "four CSV tiers" / "a CSV catalog" | TOML | carrier cutover |
| MULTI_REPO.md:238 | "inert like `interfaces.csv`" | TOML | same |
| RESYNC_PACK.md §3 (absence) | no `[since]` entry for `hats.template.toml` + `scripts/hats.py` + SN `tags` | a shipped registry + reader + schema addition landed post-3771c003 | OI-19; `2026-08-16l/m`; `2026-08-17a` |
| registries/stakeholder-needs.template.toml (absence) | no `tags` key | hats `applies_when` ships `tags contains "…"`; SN is outside the dogfood key census, so nothing catches it | `2026-08-16l` (R-2) |
| skills/autonomous-gate-operations/SKILL.md:22 | "Draft/Blocked items never claimed" | `Draft` retired (same class fixed on two skills at `2026-08-16p`) | `2026-08-15m` |
| README.md:354 | `human_ratification_through` … `0` | live dial is `4` (docs/process.toml:69) | `2026-08-14a` |
| README.md:380 | "a stage … 0–5" | eight-rung ladder (README itself says "1 of 8" at :334) | `2026-08-13c` (OI-21) |
| README.md:201 | `work-items.template.csv` as the execution DAG | live carrier is `docs/work/`; CSV is legacy migration format | Phase 2c/5 |
| README.md:301 + project-trajectory/README.md:167 | "grouped by `Module`/`Area`" | `Area` retired for closed `Aspect` | `2026-08-14h` |
| README.md:196 (+ :163 mermaid `SR-Refs` edge) | IF row "does not say who provides or consumes it" | ownership is the `owner` cell; the column is `req_refs` | `2026-08-15a/e` |
| README.md:118-132 | SN-036/SN-037 "machinery is scheduled, not built" | hats machinery + Boundary-Refs resolution built and shipping | OI-19; WI-453 |
| project-trajectory/README.md:36 (+ bootstrap.py:1659 comment) | "thirteen starting hats" | sixteen, all ratified | `2026-08-17a` |
| project-trajectory/README.md:23 | "every `Draft`/`Modified` spine row" | `Drafted` | `2026-08-15m` |
| project-trajectory/README.md:47 | "the DevBar-Release `Verified` criterion" | `Verified` retired; phase cells numeric-only once armed | WI-402; `2026-08-15m` |
| registries/interfaces.template.toml:41-44 (minor) | "Both are legitimate" (owner: SR vs LLR), no preference | ruled reading: `owner` points at the design tier wherever a design row exists | `2026-08-17c` |

## Class B — open/provisional; deliberately NOT in WI-471's scope

- **`Modified` retirement / two-word enum / UNANCHORED-as-ERROR / intake
  refusal** (D-9 step 7) — post-sign/seed; the docs correctly still teach the
  three-word enum.
- **SR-as-attestation-unit chain rule** (PROCESS.md:363-365) — current rule;
  item 15's challenge is recorded, unruled.
- **`Direction`/`ThisProject`/`Counterpart` IF columns** — the R4 shed is
  ruled but held (dashboard dependency + the 27 WI-469 rows); removal is
  wi455's.
- **All architecture.md / runtime-flows / `gen_arch_map` / `check_flows`
  prose** — execution is the unmerged wi455 lane.
- **SN `kind`/`attestation`/`amended` → `status` unification** — item 6;
  direction ruled, execution open. The SN-maturity core finding above rides
  its execution.
- **`founded` (item 16), chain-flip (item 15), B/EXT watermark spaces
  (item 17)** — recorded, unruled; correctly absent from every shipped
  surface.
- **Kit-level edge-SN template question — NEEDS A RULING, flagged here.**
  OI-18 dissolved *this repo's* edge tier (all SNs `kind = "core"`), and the
  `2026-08-17g` steer leaned on that retirement — but the shipped SN template
  still declares `kind = "edge"` and EXAMPLE.md:25-29 / ADOPTING.md:188 still
  teach the edge-case table. Whether the kit-level row kind follows the
  instance dissolution is unruled; WI-471 must not edit those sites until it
  is.

## Covered elsewhere (already owned; not WI-471's)

- **WI-390** — PROCESS_OPTIONS' concurrency/seam-model + attended-mode prose,
  AGENTS.template.md concurrency prose, root README:70-74 "phase v4" framing.
- **WI-455** — architecture prose retirement, the IF-registry end-state, the
  resync-pack entry it owes, README rows describing `docs/architecture.md` /
  `gen_arch_map`.
- **WI-452** — the resync surfaces naming `migrate_carrier.py`.
- **WI-448** — future common-module resync entries. **WI-469** — the
  `counterpart` column stays until the 27 rows re-author.
- Adjacent and self-admittedly stale, outside the shipped-kit scope:
  `docs/registry-machinery-reference.md` §1 (still describes .md/.csv
  carriers), `external.toml`'s own header ("LOCKED at 5·6·3" vs the live
  4·4·3), the SN header's "five always hats" vs ten — named in WI-471 as a
  same-sweep cleanup candidate since two are one-line.

## Sizing

`EXAMPLE.md` is the one real job (§1-§4 + §9 rewritten onto the TOML carrier
with legal Status cells — roughly a half-day with a verification pass, and
worth weighing a test pin beyond the gen_cases grammar while there).
Everything else is line-level: ~10 README fixes, one RESYNC_PACK §3 entry,
one `tags` key + doc line in the SN template (plus optionally adding SN to
the dogfood census), three wording fixes across ADOPTING/MULTI_REPO, one
line in autonomous-gate-operations, ~20 token fixes in the core pair.
PROCESS.md sizes at net +0.5 to +1.5 KB against its byte budget (the
attestation reword *shrinks*; hats/frame/snapshot paragraphs pay for
themselves by trimming the superseded domain-hats prose); PROCESS_OPTIONS
~neutral; AGENTS.template.md zero.
