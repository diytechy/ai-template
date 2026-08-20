+++
id = "WI-390"
title = "PROGRAM CLOSE for concurrency-v2 (docs/concurrency-v2.md §A9 deletion ledger). NOT a sweep-up-dead-code row, and must not be built as one: EVERY ROW IN THIS PROGRAM DELETES ITS OWN MACHINERY as part of its own scope, and deferring a deletion to this row is the mothballing the governing principle exists to prevent. This row owns ONLY the surfaces no single builder can own. (1) THE SPINE AMENDMENT, which is why this is safety_class=spine. Live SRs describe the model the program replaces and will be FALSE once it lands: SR-093 `Pure safety classification` and SR-124 `Contradiction-safe dual-plan dispatcher class` both describe the five-scheduling-class ladder WI-383 collapses into two axes (exclusive|parallel + rank), and SR-124 names `single-WI` specifically, a class that ceases to exist; SR-132 `Local integrator: serial fail-closed merge queue` describes the composed-tree bar and candidate worktree WI-386 deletes outright. Check SR-131 (tracked pause drains claiming to a merged stop) against WI-387's terminal outcomes and SR-133 (work-branch lane skip for freshness steps) against WI-386's refresh, both of which MAY be affected - verify, do not assume. Any further amendments the seven builds surface land here too. THE POINT OF BATCHING THEM: per §A4 all spine WIs admit together as ONE re-attest window and ONE owner sitting, so this program costs the owner a single sitting instead of one per row - which is the WI-280 pain the whole design exists to prevent, applied to the design itself. Follow the repo's existing convention for rows the program retires rather than amends: mark them `Superseded: <title>` as Phase 5 did for the deleted dispatcher's SRs, never delete the row. (2) CONNECTIVITY AND THE INTERFACE REGISTRY. drive.py -> dispatch.py + lane.py moves the arch-map entry and the Contracts: docstring declarations. Note the registry is ALREADY drifting before this program starts - check_trajectory currently WARNs that scripts/drive, traj_graph, traj_panels and traj_render sit in the arch-map with no IF-### row naming them, that trunk_step declares no Consumes seam, and that IF-055, IF-080 and IF-081 are in the registry with no script declaring them - so close the drift this program CAUSES and record, without silently absorbing, the drift it merely inherits. (3) THE PROSE THAT DESCRIBES THE OLD MODEL: PROCESS_OPTIONS.md (rewritten onto the seam model at Phase 5, and the station protocol changes that seam), AGENTS.template.md, and concurrency-restructure.md's forward-looking claims - the last is HISTORY and must be read as the account of what was built, never edited into a claim about what now exists. (4) THE STAMPS: deletions SHRINK modules, and the standing rule is that a size/complexity entry is retired or deleted rather than re-stamped up - the mirror obligation is to re-stamp DOWN rather than leave a generous ceiling that would silently permit regrowth, and to check whether any docs/dupes-allow census sanction has gone vacuous. VERIFY MECHANICALLY, NOT BY EYE: run check_stubs.py, check_dupes.py, the size ratchet, and check_trajectory.py --strict unfiltered, and quote the real output - the question `is anything left behind?` has mechanized answers in this repo and must not be answered by reading code. Hard-blocked on every row that changes a contract so the spine amendment reflects the final state; soft edge on the Process-tab render, which changes no contract."
workstream = "process"
specref = "docs/concurrency-v2.md"
buildtier = "medium"
safety_class = "spine"
needs = ["WI-380", "WI-381", "WI-383", "WI-384", "WI-386", "WI-387", "WI-388", "~WI-389", "~WI-464"]
+++

## Context

### The `~WI-464` soft edge (2026-08-19, repo-review triage)

The 2026-08-13w section below already rules that this row's spine amendment
"does not open its own window: it runs INSIDE the re-tier campaign's window" —
that campaign is WI-464. The ordering lived in prose only; the soft edge now
encodes it for the scheduler. Nothing else about this row moved.

### The verify list lost a member (WI-426, 2026-08-11)

This row's title names `check_dupes.py` in its VERIFY MECHANICALLY list and asks
its §4 stamp step to "check whether any `docs/dupes-allow` census sanction has
gone vacuous". **Neither is runnable any more:** repo-lock D-7 (owner ruling
2026-08-10, executed as WI-426) tore the duplication census down — the script,
the census file and the spine chain `SR-039 → LLR-036 → TC-039` are deleted, and
F5 duplication is unbounded again by ruling.

**The substitute, so the list stays complete rather than merely shorter:**
`tests/test_rule_sync.py` is the anti-drift tool of record. Where this program's
deletions leave duplicated POLICY behind (not plumbing), the obligation is a
behavioural pin there; duplicated plumbing is accepted unbounded. Everything
else in the verify list — `check_stubs.py`, the size ratchet, and
`check_trajectory.py --strict` unfiltered, all quoted from real output — is
unchanged, as is the §4 obligation to re-stamp module sizes DOWN rather than
leave a generous ceiling. Nothing else in this row's scope moves.

### Re-scope (WI-414, 2026-08-02)

Added by the WI-414 adjudication of `TC-056 Verifies` on merged trunk
`7894457..5211f07`, as the §A5.2 scope-moved output. This row's spine amendment
explicitly covers the ratified prose WI-389 left describing the deleted
two-intersecting-hoops render, which the merge made false:

- `SR-055` — still requires "two circular working loops" and one shared
  `LLM_Agent` hub; still `Verified`.
- `LLR-056` — still describes those loops.
- `TC-056` `Method` + `Expected` — still specify two hoops and the 6+5=11 edge
  count, while the row's `Evidence` now cites the station-cycle tests and the
  shipped render emits ONE station cycle.

WI-389's own Deliverable already routed these here ("amending it is the program
close's spine scope, not this ordinary row's") and names SR-050/LLR-051/TC-051
alongside them; WI-414 confirms the routing from the adjudication side and adds
nothing new to own. The Modified/re-attest flow for these cells belongs to this
row's owner sitting — deliberately NOT flipped at WI-414, which is why no Status
moved there.

This section also re-dates this row against its amended SpecRef
(`docs/concurrency-v2.md`), which is the re-affirmation the standing
`check_trajectory` SpecRef-clock warning asks for.

### Post-re-tier correction (2026-08-18b — READ FIRST, before the section below)

**SIX OF THIS ROW'S AMENDMENT TARGETS NO LONGER EXIST.** The 2026-08-13w bullet
below says "do not quote a Status from this file — re-measure at claim", and
that guard is now too weak: the question is not what these rows' Status reads,
it is that the rows are **gone**. Measured against the live registries at
`2026-08-18b`, this file cites **ten ids that no longer resolve**:

| Cited here | Live? | Where it went |
|---|---|---|
| `SR-050` `SR-055` `SR-093` `SR-124` `SR-131` `SR-132` `SR-133` | **gone** | the WI-451 re-tier campaign — the 26-row tombstone class DELETED per D-4 (`2026-08-14b`), plus absorptions (`SR-133` folded into `SR-006`, which now states its clause verbatim) |
| `SR-039` `LLR-036` `TC-039` | **gone** | already named as deleted in this file's own WI-426 section above — knowingly dangling, no action |
| `LLR-051` `LLR-056` `TC-051` `TC-056` | live, all `Modified` | the ratified-prose amendment targets that DO survive |

**What this changes for a claiming session:** the "two intersecting hoops"
ratified-prose amendment now has to be re-derived against the surviving rows and
whichever re-tiered SR absorbed each deleted one — the parent for that prose may
now be a different id, or may need minting. **That is a re-scope, and a re-scope
of a `spine`-class row is not a builder's call**: raise it at the sitting rather
than inventing a mapping. Nothing here retires this row; the deletion ledger and
the connectivity scope are untouched.

*(Found by the open-WI id sweep at the `2026-08-18b` merge, which read every
open work item's citations against the live registries. This note re-validates
this file's ID CITATIONS only — its `docs/concurrency-v2.md` SpecRef content is
NOT re-validated here.)*

### Post-sitting-2 corrections (2026-08-13w — read before claiming)

- **Do not quote a Status from this file — re-measure at claim.** The WI-414
  re-scope bullet above says SR-055 "still `Verified`" — true when written,
  false now. (Measured 2026-08-13: SR-055 `Modified`, SR-050 `Modified`;
  SR-093/124/131/132/133 `Verified`; LLR-051/056 and TC-051/056 `Verified`.)
- **IF-080/081 are ruled, not drift (13m · 13u).** Decision 2 confirmed both
  internal; the `counterpart = "downstream adopter"` label is the mislabel, and
  it is the external-schema row's to fix — under sitting-2 §1R.5 `counterpart`,
  `direction` and `stability` are all fields the slimming deletes. **This row's
  connectivity scope covers IF-055 and the arch-map/`Contracts:` declarations
  only.** Record the IF-080/081 finding as inherited-and-owned-elsewhere; do
  not edit those two rows here.
- **Window sequencing vs. the SR re-tier (13q · 13s).** Four of this row's five
  amendment targets (SR-093/124/131/132/133) name internal scheduling
  machinery, not a boundary crossing — they are re-tier *demotion* candidates
  under §3R, not merely amendment candidates. **This row's spine amendment does
  not open its own window: it runs INSIDE the re-tier campaign's window, after
  the campaign's census has classified these five rows.** If the census demotes
  a row, its amendment is written at the LLR tier the demotion lands it in and
  this row's obligation is discharged there; if the census keeps it at SR, the
  amendment lands here as written. §A4's one-window principle is honoured by
  joining the larger window, not by opening a competing one.
- **The boundary/entity vocabulary is NOT this row's prose pass.** The §1a
  entity-plus-interface rule and the "enabling system" vocabulary are kit-facing
  process doctrine produced by the external-schema row's program; WI-390's
  prose pass stays scoped to the concurrency seam model.

