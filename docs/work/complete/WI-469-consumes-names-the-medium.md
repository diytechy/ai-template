+++
id = "WI-469"
title = "Consumes rows that name the MEDIUM, not whom the medium serves — re-author the 27 SR-owned file-as-endpoint Consumes rows in docs/requirements/interfaces.toml (sitting-3 §0.4 item 3, ruled 2026-08-17): each row's counterpart names a data file or directory, and the owner's correction stands — 'if the output is just a file, that file is being provided to someone or something for some reason, that is what the interface should show… The file itself is the actual interface.' Measured 2026-08-17: 0 of the 27 are terminal — every endpoint is a file something reads — so the rows are UNDER-SPECIFIED, not underivable. Two sub-shapes, and they do not take the same fix: LOW FAN-OUT rows name the actual consumer module (coverage.json is read by check/check_coverage only; docs/declared-absences by five checkers) and the endpoint becomes derivable; PUBLISHED-CONTRACT / HIGH FAN-OUT rows (docs/stack.ini: 17 readers; docs/architecture.md: 12) serve a CLASS of consumer where naming one would be false — there the file IS the interface, and where the class includes the adopter the row ties back to B-05 exactly as IF-013…IF-018/IF-048 already do (counterpart = 'external:downstream adopter' + interface_to_external = 'B-05'). WHICH consumer each of the 27 names is per-row judgement NOT done at the ruling — a mechanical attribution attempt stem-matched docs/work and was discarded as unsound; this WI is that judgement pass. Unblocks wi455's column-drop: re-author first, then drop what has become derivable."
specref = ""
workstream = "requirements"
sr_refs = []
needs = []
buildtier = "medium"
safety_class = "spine"
priority = 3
+++

## Deliverable

All 27 SR-owned file-as-endpoint `Consumes` rows in
`docs/requirements/interfaces.toml` re-authored per-row, each landing in
exactly one of the two shapes the ruling named:

- **10 LOW fan-out rows** (IF-025, IF-026, IF-029, IF-035, IF-037, IF-045,
  IF-047, IF-052, IF-070, IF-072) now name the verified actual consumer
  module(s) as `counterpart` — a closed, nameable reader set re-measured
  directly against the current codebase rather than trusted from the
  2026-08-17 quoted counts (several had shifted, or over-counted a comment
  mention as a read). IF-052 was re-pointed at `scripts/traj_parse`, the
  module that actually performs the docs/gate read post-WI-280, rather than
  left pointed at the file it wraps.
- **16 PUBLISHED-CONTRACT / HIGH fan-out rows** (IF-021, IF-022, IF-023,
  IF-024, IF-030, IF-033, IF-034, IF-038, IF-049, IF-051, IF-054, IF-057,
  IF-059, IF-068, IF-073, IF-079) now carry `counterpart =
  "external:downstream adopter"` + `interface_to_external = "B-05"`,
  following the IF-013…IF-018/IF-048 pattern exactly: each names a
  spine/config registry with an open, growing reader population that every
  downstream adopter also authors and reads with the same shipped scripts.
- **IF-028** needed no change: the concurrent WI-455 crossing-half slice had
  already re-pointed its counterpart from the retired `docs/architecture.md`
  to `scripts/gen_arch_map` (a module, not a medium) before this WI ran,
  which already satisfies this WI's own goal.

Every touched row carries a `notes` cell recording the pick and its verified
evidence (the measured reader set), written as standalone argument prose per
`trace.py`'s citation-frame rule — no WI id or date stamp inside the cell;
the full account is in `docs/log.d/2026-08-20-program-grind.md`. No
`status`, `direction`, `owner`, or `contract` cell was touched, and the
wi455 column-drop itself was left to that lane, as scoped.

**Unblocks, precisely.** The wi455 lane's item 2 (the 49 held `Contract`-cell
provenance citations, `docs/provenance-allow`'s header) is now UNBLOCKED —
its sole named blocker was this WI landing. Its item 1 (the
`direction`/`this_project` shed + counterpart→consumers transform) has this
WI's precondition satisfied but stays blocked on a SEPARATE, still-unruled
owner question (which reading of `owner` governs a `Consumes` row) that this
WI deliberately left untouched and undecided — that call is the owner's.

## Context

Filed 2026-08-17 out of the item-3 ruling at the sitting-3 desk
(docs/plans/2026-08-13-sitting-3-spine-verification.md §0.4 item 3; log
2026-08-17c). The same ruling settled the other two thirds of the 49 SR-owned
`Consumes` population mechanically: 19 rows whose counterpart resolves to a
live LLR `module` had their `owner` re-pointed to the design tier in the
ruling session, and the 3 rows already naming an external actor
(`IF-032` `external:git`, `IF-036` `external:upstream docs`, `IF-041`
`external:agent CLI`) are correctly shaped and stand. These 27 are the
remainder, and they are MIS-AUTHORED, not residue: the cell is the single
home for the endpoint (nothing to derive it from), but what it records is the
medium instead of whom the medium serves.

No status flips and no requirement text changes ride this WI: every touched
row is `approval = "drafted"` and `owner` is not an attested claim.

### The 27 rows (population measured at the ruling — do not re-derive)

Each line: row id, consumer (`this_project`), file-endpoint (`counterpart`).

| IF | this_project | counterpart |
|---|---|---|
| IF-021 | scripts/trace | docs/requirements/system-requirements |
| IF-022 | scripts/check | docs/stack.ini |
| IF-023 | scripts/check_trajectory | docs/work |
| IF-024 | scripts/gen_trajectory | docs/work |
| IF-025 | scripts/gen_arch_map | project-trajectory/scripts |
| IF-026 | scripts/check_stubs | project-trajectory/scripts |
| IF-028 | scripts/check_doc_refs | docs/architecture.md |
| IF-029 | scripts/check_flows | docs/architecture.md |
| IF-030 | scripts/check_docs | docs |
| IF-033 | scripts/gen_okf | docs/requirements/system-requirements |
| IF-034 | scripts/gen_release_checklist | docs/requirements/stakeholder-needs |
| IF-035 | scripts/gen_skills_index | project-trajectory/skills |
| IF-037 | scripts/agent_common | docs/status.md |
| IF-038 | scripts/subagent_gate | docs/process.toml |
| IF-045 | scripts/agent_route | docs/agents |
| IF-047 | scripts/score_reviews | docs/reviews |
| IF-049 | scripts/run_menu | docs/stack.ini |
| IF-051 | scripts/derive_gate | docs/requirements/system-requirements |
| IF-052 | scripts/gen_trajectory | docs/gate |
| IF-054 | scripts/schedule | docs/work |
| IF-057 | scripts/plan_coverage | docs/requirements/interfaces.toml |
| IF-059 | scripts/plan_briefs | docs/requirements/system-requirements |
| IF-068 | scripts/agent_loop | docs/stack.ini |
| IF-070 | scripts/check_coverage | coverage.json |
| IF-072 | scripts/check_doc_refs | docs/declared-absences |
| IF-073 | scripts/gen_open_items | docs/requirements/open-items |
| IF-079 | scripts/wi_convert | docs/work |

(For the avoidance of a re-derivation: the full population is IF-021,
IF-022, IF-023, IF-024, IF-025, IF-026, IF-028, IF-029, IF-030, IF-033,
IF-034, IF-035, IF-037, IF-038, IF-045, IF-047, IF-049, IF-051, IF-052,
IF-054, IF-057, IF-059, IF-068, IF-070, IF-072, IF-073, IF-079 — 27 rows.
`IF-039`'s `project-trajectory/registries` looked file-shaped but resolved to
LLR-171 at the ruling and converted with the 19; it is NOT in this set.)

### What the session is to produce

A per-row re-authoring of the 27, each row landing in exactly one of the two
shapes:

- **Low fan-out** — the counterpart cell names the actual consumer(s) of the
  file (e.g. `coverage.json` → `scripts/check`/`scripts/check_coverage`), so
  the seam states who is served and the endpoint becomes derivable. The
  fan-out counts quoted in the title are the desk's 2026-08-17 exact-path
  measurements; re-verify the reader set for each row you re-author rather
  than trusting a quoted count.
- **Published contract / high fan-out** — the row publishes a contract to a
  CLASS of consumer (a `docs/stack.ini` with 17 readers has no one honest
  consumer). The file is the interface; where the consumer class includes the
  downstream adopter, follow the existing IF-013…IF-018/IF-048 pattern:
  `counterpart = "external:downstream adopter"` (or the honest class name) +
  `interface_to_external = "B-05"`.

WHICH shape each row takes, and which consumer a low-fan-out row names, is
this session's per-row judgement — it was deliberately NOT decided at the
ruling. Record the pick and its evidence (the measured reader set) per row.

Out of scope: the 19 converted rows and the 3 `external:` rows (settled at
the ruling); any `approval`/`direction`/contract-text edit; the wi455 column
drop itself (it follows this WI, never precedes it).
