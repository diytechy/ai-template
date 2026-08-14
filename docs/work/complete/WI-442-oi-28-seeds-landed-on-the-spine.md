+++
id = "WI-442"
title = "Mint external.toml and slim interfaces.toml — the D3/D4/D5/D12 schema execution (owner-ruled 2026-08-13i/l/m/u; supersedes this row's OI-28 seed framing, whose three clauses re-homed: the entity declaration lands here, the template-set SR moved to the re-tier campaign as B-05's delivered-capability family, and the two accidental 'agent CLI' rows are a step of this migration). Land the three row kinds per sitting-2 §1R.5: [entity.EXT-###] for the five locked entities with class in operational|interoperating|deliverable; [relationship.REL-###] for the three external-to-external rows (no interface vocabulary — that line is what keeps D-6 satisfied); [boundary.BIF-###] for the six locked crossings B-01/02/04/05/06/07 with entity + direction + carries. Then slim interfaces.toml: an IF row states what the interface concretely IS, sheds direction/counterpart, and carries a tie-back ONLY when boundary-realizing — interface_from_external = 'B-##' for IN, interface_to_external = 'B-##' for OUT (owner naming 13m). RETIRE stability across all 113 rows for the approval schema (draft vs approved, 13u) and design the approval element into external.toml FROM ITS FIRST COMMIT (D12 — otherwise the frame is un-ratifiable), coordinating the value set with the combined D-9/D12 vocabulary program: either wait on sitting 3's D-9 ruling or ship a provisional value set with a stated migration — STATE WHICH. HARD COUPLING, do not split across commits: derive_gate.boundary_incomplete reads Stability and NOTHING ELSE (derive_gate.py ~L593) — deleting the column without re-keying the predicate in the same commit silently retires rung 1's gate. Also resolve, stated not assumed: whether the re-keyed predicate gates on BIF *approval* (13u wording) or BIF *realization coverage* (§1R.5 wording) — they are different predicates. Mint the SR-side interface-reference field (a bif_refs-style column resolving into [boundary.*]) and build SN-037's SR→IF checker against it — the checker cannot be re-tier slice work because its input column does not exist until this row mints it; the re-tier then populates it. Absorbs: IF-020/IF-041 ('agent CLI' counterpart — no such entity under the locked frame; re-key or retire deliberately); sitting-2 §6 item 6 (IF-038's docs/subagent-gate counterpart, a field this slimming deletes); §6 item 16's IF-064 SN-016 stray. STATE THE FLIP AUTHORITY for the new approval elements in the registry header prose (the human_ratification_through dial covers spine tiers only — sitting-3 §3.6 owns the mechanized extension; until it lands, external.toml and the slimmed interfaces.toml declare in prose that their approval values are the owner's to flip). Verified by: the throwaway-clone lesson (run the conversion against a scaffold first), the dogfood-sync pins, and boundary_incomplete demonstrably still gating after the re-key."
workstream = "lock-program"
sr_refs = []
needs = ["WI-441"]
buildtier = "medium"
safety_class = "spine"
priority = 2
+++

## Deliverable

Completed 2026-08-14 in two commits — the coupled schema change, then the
SR-side reference and its checker. Eleven of the row's twelve clauses landed as
ruled; the twelfth is HELD with evidence and bound to WI-455 (below).

THE FRAME IS ROWS. `docs/requirements/external.toml` carries the locked frame in
three tiers on one path: 5 `[entity.EXT-###]`, 6 `[boundary.B-##]`, 3
`[relationship.REL-###]` (§1R.1/1R.2/1R.3), each row carrying `absorbs`
provenance so §1R.4's reclassification ledger survives by id. The carrier needed
no loader change — keying registries by ID COLUMN rather than by path already
made a three-tier file work. Shipped as `registries/external.template.toml`,
scaffolded by `bootstrap.py`, pinned in `test_bootstrap` and on all three legs of
`test_dogfood_sync` (whose `TOML_REGISTRIES` map re-keyed from path to id column,
since three tiers cannot share one path-keyed entry).

ROW IDS ARE `B-##`, NOT `BIF-###` — a stated deviation from §1R.5's schema
sketch, resolving a contradiction inside the source. §1R.2's locked table, §3R's
form rule and this row's own tie-back examples all write `B-01`…`B-07`; only the
sketch writes `BIF-###`, and v1's `BIF-001`…`BIF-031` are a DIFFERENT set of 31
crossings still cited by id in the archive, so that prefix would recycle live ids
onto new meanings. `B-03` is absent on purpose (removed 13u), keeping id and
frame name aligned 1:1 rather than renumbering a locked table.

THE COUPLING, LANDED AS ONE COMMIT. `Stability` retired for `Approval` and
`derive_gate.boundary_incomplete` re-keyed onto `[boundary.B-##]` approval in the
same commit, because `_maturity` maps an unrecognized value to DRAFTED: deleting
the column alone would have pinned rung 1 open forever on a column that no longer
exists — the right stage for entirely the wrong reason. Demonstrated rather than
asserted: with the six crossings `draft` the repo reads `DevStg-Boundary`; flip
all six to `approved` and the rung releases (the next unfinished rung, Needs,
then shows). The applies-when moved with the predicate — a repo carrying
`interfaces.toml` and no `external.toml` now skips rung 1 instead of being held
by its internal seams, which is decision 3's correction, and a fresh scaffold
reads `DevStg-Needs` rather than being held by inert `-000` rows.

BOTH AMBIGUITIES RESOLVED, STATED NOT ASSUMED.
(1) The predicate gates on BIF **approval**, not realization coverage. 13u's
wording says approval; §1R.5's adds "every BIF realized (or explicitly
deferred)". Realization is decision 6, deferred BY RULING to post-schema, and
gating on it would take a decision nobody has — not hypothetically: four of the
six crossings are realized by no IF row today, so the second conjunct would hold
rung 1 down on unscoped work under a predicate that reads like ratification.
(2) The approval vocabulary ships PROVISIONAL — `draft` | `approved` — with the
D-9 migration written into the registry header (`draft`→`drafted` a rename,
`approved` unchanged, `founded` an addition) rather than waiting on sitting 3,
which the whole campaign sits downstream of.

EVERY ROW LANDS `draft`, INCLUDING ALL 113 IF ROWS, and that is a deliberate
non-claim: `Stable` was a MATURITY assertion, `approved` is a RATIFICATION one,
and mapping the first onto the second would have manufactured 108 approvals
nobody signed. The five rows that carried `Experimental` (IF-057, IF-103,
IF-118, IF-119, IF-120) are recorded in the registry header, not in their own
cells, so no row carries migration history. Flip authority is written into both
registries' prose: `human_ratification_through` covers the spine tiers only, so
until sitting-3 §3.6 these cells are the owner's to flip and no loop or script
may. `tests/test_external_frame.py` pins that as a tripwire — an approval
authored by anything but a ratification turns a test red rather than passing
quietly in a diff.

NEW ENFORCEMENT. `trace.frame_findings` + `tieback_findings` — a crossing's
`Entity`, a relationship's `From`/`To` and an IF row's directional tie-back must
resolve — as their own `--strict` failure class with its own report section, so
"Interface findings: relationship REL-002 From references unknown EXT-009" can
never be a label lying about its contents. The three frame tiers join the
advisory schema tier (required fields + closed vocabularies) on WI-443's ruled
warn-first sequencing.

SN-037'S CHECKER, AT TWO SEVERITIES. `SR.Boundary-Refs` minted (carrier, writer map,
tier schema, template with its guidance) and `trace.sr_boundary_findings` built
on it. Resolution is HARD — an SR naming an undeclared crossing is a dangling
reference like an SR citing a deleted SN. Coverage is ADVISORY, one summary line:
enforcing "every SR names a crossing" the day the column shipped would have
redded all 148 rows for work WI-451 slice 2 owns, under a form rule that is
itself a guideline with recorded per-row waivers (13v), and a gate 100% red on
day one is a gate someone turns off. SN-037's third clause (every crossing has an
interface row) is REPORTED, not gated — decision 6 again. `Boundary-Refs` joins
§A5.1's traced half on `SN-Refs`' own argument and ROUTES to adjudication rather
than arming a re-attest window; nothing escapes attestation by that choice, since
the campaign's re-statements touch `Requirement`, which is ratified.

<!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev=8d777da4 -->
The baseline the checker lands with — SR→boundary coverage **148 of 148**
requirements name no crossing;
crossings named by NO requirement **B-01 B-02 B-04 B-05 B-06 B-07**; crossings
realized by NO interface row **B-01 B-02 B-06 B-07**; **8** IF rows carry a
directional tie-back (7→B-05, 1→B-04).

ABSORBED DISPOSITIONS, each deliberate. IF-020's `agent CLI` counterpart names no
entity in the locked frame, and what actually crosses is the verdict, so it
re-keys `interface_to_external = "B-04"`. IF-041's `agent CLI` gets NO tie-back:
the loop launching its CLI dissolved into the session at 13o, and the provider
behind it is REL-003. IF-036 likewise (B-08 removed 13o). §6 item 6's
`docs/subagent-gate` counterpart survives the held clause, but the stale contract
cells on IF-020 and IF-038 now name `docs/process.toml [checks] subagent_gate`
— a knowingly-false contract cell was not worth leaving to be tidy about scope.

THE ONE CLAUSE HELD, AND THE FINDING IT IS. §1R.5 also rules that an IF row sheds
`direction` and `counterpart`. Those two columns are the SOLE input to the
dashboard's How-SW seam graph and its containerized component drill, and the
second is ratified work — **SR-091**, "shall attach IF seams to visible block
input/output ports and aggregate cross-container seams to container boundaries",
Verification = Test. **Decision 8 makes `PROJECT_STATE.html` the ONE home for
architecture in the same sitting decision 4 deletes what it draws from.** The
full shed was implemented first and measured: 41 tests red, 30 of them the
dashboard failing to render at all. So the columns are HELD, their deletion is
bound to WI-455 (which owns the replacement view). The EVIDENCE has one home —
`interfaces.toml`'s header, where a maintainer deciding whether to drop the
columns will look; the carrier, the migrator and the checker carry a one-line
pointer to it, not a fourth copy of the argument. The `direction` name now means two things across two tiers,
which is the D-3 defect; it is stated as a WATCHED collision that closes itself
when WI-455 lands the deletion, with renaming the boundary column as the fix if
WI-455 slips.

TWO CHECKS CHANGED SHAPE RATHER THAN BEING COPIED FORWARD INTO TAUTOLOGIES. The
seam-TC citation rule now arms on EVERY real IF row: it had already been re-keyed
once off a column whose values marked exactly the rows that passed it, and
`Approval == "approved"` would have rebuilt that (every row reads `draft`).
WI-191's anti-duplication rationale arm is RETIRED, not re-keyed: its input meant
"proposed, not yet pinned by a second consumer", `draft` means "not yet
ratified", and the swap would have multiplied its arming set from ~4% to 100% at
a severity that ERRORS under `--strict`. A rule whose blast radius multiplies
twentyfold while its sentence stays the same is not the same rule. Both losses
are pinned by tests that assert the removal, so neither can drift back half-fed.
