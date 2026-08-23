> **ARCHIVE** — design history as of 2026-08-13; not current guidance.

# Backlog drain plan — 2026-08-01 (Part 2 of the wrap-up)

The owner-approved plan for closing the remaining concurrency-v2 backlog once
the two open lanes merge. **Part 1** — diagnosing the refresh red and merging
`wi-387` then `wi-391` — is not restated here; it is
[handoff-2026-08-01.md](handoff-2026-08-01.md) §2 and §5 executed as written.
This file carries what that handoff does not: the drain order for the queued
rows, the standing rules every builder inherits, and the **four rulings the
owner must make**, each with its background, options, and a recommendation.

Everything below is scored against two fixed points:

- **The kit's purpose** (the `PROJECT-VISION:` tag in the root README):
  downstream code that is **maintainable and trustworthy** — readable, deeply
  tested, advanced only through explicit gates. A green gate that certifies
  something false is the worst failure this repo can produce.
- **The governing principle** ([concurrency-v2.md](../../concurrency-v2.md) Part I,
  owner 2026-07-31): **prefer a constraint that makes a bad state
  unrepresentable over a check that detects it.** Recurring issues usually mean
  the root cause wants further *restriction* — which is less code, not more.

---

## Standing rules for every drain agent

- **Serial, one row at a time**, claimed through `integrate.py` (the station
  protocol). The shipped loop is serial; the dispatcher row is unbuilt. Running
  lanes concurrently by hand is what produced the id collision (handoff §4).
- **Boot from the spec, not from an orchestrator's summary** — an inherited
  framing is how a population of 20 got measured as 4 (handoff §4).
- **One APPROVE closes review.** Round inflation was a named cost of the last
  session; rounds beyond the first need a real finding, not diligence.
- **Never sanction, skip, or mothball a red to green a step.** A test that is
  red *by construction* in some context means its **premise needs narrowing**
  (the lane-canary fix named the primary checkout — it did not delete the
  test). That fix shape is usually smaller than the workaround.
- **A figure is evidence only with its command and revision**; paste real
  output, never report a green you did not watch (the two formulations in
  handoff §3).
- **No new WI ids are minted on a work branch — ever** (Ruling 1 below). Until
  the enforcement rung lands, this is discipline; after it lands, it is
  refused mechanically. Corollary for the gap before `wi-391` merges: no new
  ids on trunk either, because trunk's max is 394 and the branch carries
  395/396 — a trunk mint would recreate the exact collision this rule exists
  to end.

---

## Execution order

Thirteen rows, strictly serial. "Ruling" names the decision (below) that must
be made before that row starts; everything else is claimable as specced. Rows
are named by **plain id, deliberately un-linked**: a row's file moves folder
with every state change (claiming one broke trunk's doc-navigability on
2026-08-01 — the driven instance is in the log), so this table points once at
[docs/work/](../../work/) and lets the id be found there.

| # | Row | What it does | Direction (simplicity lens) | Ruling |
|---|-----|--------------|------------------------------|--------|
| 1 | WI-397 *(**shipped** 2026-08-01; R1 ruled and recorded)* | Refusal rung: a finished branch whose `docs/work/` delta adds a spec id outside its claimed set cannot merge | Constraint at the merge slot; deletes the id-reservation problem from the dispatcher's scope | **R1** |
| 2 | WI-396 *(**shipped** 2026-08-01)* | Citation checker cannot see a line-suffixed reference into the kit's own tree | Shipped as the strip-the-suffix rule at both call sites, verdict BOTH-CLEAN pinned with its mutation twin | — |
| 3 | WI-395 | `blocked` rows promise a self-release that never happens | Fix the false promise in prose; do not build a cross-registry subscription | **R3** |
| 4 | WI-394 | A Verified spine row can cite evidence that never existed | File-existence half only; the node-id half is ruled prose | **R2** |
| 5 | WI-393 | Restore the link-aware spec-archival ritual Phase 5 deleted | Genuinely constraint-shaped: one indivisible move+relink operation nobody can perform two-thirds of. A claim-time instance was driven 2026-08-01 (the claim move broke this very table's links), so the ritual is owed at claim as well as at archival | — |
| 6 | WI-392 | Declared figures carry the command and revision that produced them | **Rung 1 only** (presence check on opt-in markers). Rung 2 (re-derivation) is deliberately not built | — |
| 7 | WI-398 *(minted 2026-08-01 from Part 1's findings)* | A red bar's refusal message must carry the failing step's own output — today it structurally cannot (three lost diagnoses of one red) | One anchor fix + keep the bar log a refusal points at; no log-management layer | — |
| 8 | WI-399 *(minted 2026-08-01)* | Containment is owed where a module is **added**, not where the station regenerates the inventory (second instance of the class) | Move an existing rule's firing point into the lane's own bar; no new policy | — |
| 9 | WI-400 *(minted 2026-08-01)* | The unload must distinguish declared tool-residue from evidence — today every worker-built lane ends `UNLOAD INCOMPLETE`, forever | Shed the declared residue set, keep refusing on any remainder; don't loosen the orphan read | — |
| 10 | WI-381 | Dispatcher split (`dispatch.py` + `lane.py`), spine barrier, lanes dial | Scope **shrinks** under R1 — no id reservation ever gets designed. Scaffold-surface change: verify by bootstrapping a scaffold | — |
| 11 | WI-388 | The adjudication kind; mechanical trunk-side WI minting | Becomes the *only* automated minting path — consistent with R1 by construction. Rules its two unclassified cells per its intake | — |
| 12 | WI-389 | Dashboard Process tab draws the station/lane model | Verify by pixels (render-dashboard-critique), not by reading the generator | — |
| 13 | WI-390 | Program close: spine amendment batch, connectivity, prose, stamps | **Spine class — waits, batches, runs alone, one owner sitting.** Last, by hard edges | — |

---

## The four rulings

Each ruling below states the background in plain language (the specs assume
context the owner should not need), the options with honest costs, a
recommendation, and how the choice bears on the kit's purpose. An accepted
ruling is recorded in [log.md](../../log.md)'s Decisions by the agent that executes
the affected row; R4 additionally clears through the open-items flow once
`wi-391` lands it on the owner surface.

**Status 2026-08-01, after the first ruling pass:** **R1 and R2 are RULED as
recommended.** R3 and R4 are **pending**, with the fuller background the owner
asked for in [rulings-context-2026-08-01.md](rulings-context-2026-08-01.md) —
including the owner's stated direction on handback disposition (the dispatcher
completes it; recovery is loop machinery, never a work item), held there for
confirmation. Part 1's three mechanical findings (handoff §6: the
failure-message extractor, containment-at-add, the unload residue
distinction) are **minted** as rows 7–9 in the table above.

**PARKED 2026-08-01 (owner direction), after row 2 shipped.**
`docs/work/pause` is present, so the claim rung refuses new claims
mechanically — rows 3–13 wait, and nothing needs to remember not to build.
Resume: rule R3 and R4 (context in
[rulings-context-2026-08-01.md](rulings-context-2026-08-01.md)), then delete
the pause file in a tracked commit — an unpause is auditable by design.

### R1 — Where may a new work-item id be created?

- **Background.** Work items are files under `docs/work/`; a new one takes
  `max(existing id) + 1`. Last session, work branches filed follow-up WIs
  *on their own branches*. Two branches cannot see each other's trees, so two
  lanes independently minted "WI-392" — an id collision. Three rows (WI-393,
  WI-395, WI-396) currently exist **only on the `wi-391` branch**; the handoff
  calls them "claimable," which is false until that branch merges. The design
  doc discusses id reservation as an unsolved dispatcher problem.
- **The question.** Do we coordinate concurrent minting, or forbid it?
- **Options.**

| Option | What it is | For | Against |
|---|---|---|---|
| **(a) Trunk-only minting + a merge-slot refusal rung** *(recommended)* | Ids are created only in serial trunk-side commits (claim bookkeeping, WI-388's mechanical mint, a human commit). A finished branch whose `docs/work/` delta adds an id outside its claimed set is refused at the merge slot. Lane-discovered findings are recorded as prose in the spec/log/review record; the id is assigned at or after merge. | Collision becomes **unrepresentable**, not detected. Deletes id reservation from WI-381's scope before it is ever designed — net less code. One small rung plus tests. | A lane cannot file a claimable row mid-flight; follow-ups wait as prose until merge (a delay, not a loss). `wi-391`'s three rows need a one-time grandfather (they merge before the rung exists). |
| (b) Id-reservation machinery in the dispatcher | WI-381 builds a reservation table lanes consult before minting. | Lanes keep the convenience of filing immediately. | New coordination state + crash/cleanup semantics; enforcement-layer growth of exactly the shape the 2026-07-28 audit named; solves a problem option (a) deletes. |
| (c) Lane-namespaced draft ids, renumbered at merge | Branches mint under a prefix; the merge slot renumbers. | No coordination needed. | Two id grammars; a renumber step that rewrites cross-references; worse for every future reader of the record. |

- **Recommendation: (a).** Owner directive of 2026-08-01 (this conversation);
  record it as such in Decisions when WI-397 lands.
- **Purpose fit.** The registry is the kit's single source of truth about work;
  an id collision corrupts the *identity* of records. (a) is the textbook
  constraint-over-check move and the only option whose total code goes down.

### R2 — WI-394: Evidence cells that point at nothing

- **Background.** The spine (SN→SR→LLR→TC) is the kit's traceability chain —
  its core product promise. Pointers *between* registries are validated
  mechanically. But the four cells that point *out* of the registries into the
  code and test tree — `Evidence`, `Module`, `CodeSymbol`, `TestRefs` — are
  never checked at all. Measured, not argued: an invented citation
  (`tests/this_file_has_never_existed.py`) passes every strict gate at rc=0 <!-- path-ok: the invented citation R2 is ABOUT, quoted as WI-394's measured evidence; it must never exist, and the same quoting in docs/specs/WI-394.md carries the same marker -->
  while the row reads `Automated=Yes, Status=Verified`. Real dead citations
  already exist (a test module deleted 2026-07-29 is still cited as Evidence).
  A complication the spec maps honestly: the checker's current behaviour is a
  *deliberate, comment-and-test-guarded* decision, so any fix amends a guarded
  decision rather than filling an oversight.
- **The question.** The spec's own words: the one thing definitely wrong today
  is that the current state **implies a check nobody performs**. Which way is
  it resolved?
- **Options.**

| Option | What it is | For | Against |
|---|---|---|---|
| (a) Full resolver | Validate file, `::node` test-id (needs pytest), and symbol (arch-map oracle). | Cells fully mean what they say. | The largest new check; the shape the design doc's §0 warns about; needs triage of existing dead citations and an answer to the renamed-but-present question the original decision was protecting. |
| (b) Rule the cells prose | Templates/process text stop implying validation; the gap is recorded as accepted. | Zero code. | `Automated=Yes, Status=Verified` beside an unchecked evidence pointer leaves the kit's central claim hollow — the worst outcome for trust. |
| **(c) File-existence half only** *(recommended)* | Check the cited FILE exists (stdlib `Path.exists`); rule the `::node` selector prose. Measured at +4/−2 in the core with both call sites changed; 6 true dangling findings, 0 false positives. | Closes the **entire observed failure class** — every dead citation here died because its file was deleted, not because a node was renamed. Smallest honest mechanization; warn-first triage precedent exists. | Renamed-but-present test nodes stay unchecked (documented as accepted, not implied as covered). Still amends the guarded decision — only the size differs from (a). |

- **Recommendation: (c).**
- **Purpose fit.** "Trustworthy" *is* this cell: `Evidence` is what answers
  "how do you know this is Verified." (c) is the minimal restriction that makes
  the green gate honest; (b) would leave the flagship promise decorative; (a)
  buys the remainder at a cost the governing principle argues against.

### R3 — WI-395: `blocked` promises a self-release it does not provide

- **Background.** A "parked" work item is `queued` plus a `blockref` key naming
  what blocks it. The scheduler derives `blocked` from the key's **presence**
  and never reads the blocker's **state** — so ruling an open item or closing
  the blocking WI does *not* return the parked row to the frontier. Every park
  is permanent until a human notices. The repo's own exemplar text promises the
  opposite ("readiness is the scheduler's to derive"). This bit for real: the
  first genuine park (`wi-391`) was taken on the assumption the ruling would
  release it, measured to be permanent, and had to be cancelled instead.
- **The question.** Is a park re-checkable (build the subscription) or
  human-swept (fix the promise)? The spec files the question and explicitly
  does not rule it; both options touch kit-shipped surfaces.
- **Options.**

| Option | What it is | For | Against |
|---|---|---|---|
| (A) Make the derivation consult the blocker | The scheduler resolves each `blockref` across two registries (work specs + open items) and releases rows whose blocker is ruled/terminal. | Parks self-release; matches every reader's intuition. | A cross-registry resolver inside a deliberately self-contained module; a brand-new dangling-blockref failure mode with a fail-open/fail-closed dilemma; changes readiness semantics under **five shipped modules and the shipped pre-commit hook** — the largest downstream blast radius of any option in this file. |
| **(B) Rule parks human-swept and say so** *(recommended)* | Fix the promising sentence in the two byte-identical exemplar files (repo copy + shipped template — a sync test binds them), and name the sweep and its owner in process text. | The defect *as filed* is the **silence** — a mechanism implying a subscription it does not provide. One paragraph in each of two files; no behaviour change for adopters. | Parks stay manual; the sweep is a habit someone must own (the owner surface already lists parked rows, which is where the sweep lives). |

- **Recommendation: (B).** The root cause is a wrong sentence, not a missing
  subsystem. If parks ever become frequent, (A) can be re-filed with usage
  evidence — nothing in (B) forecloses it.
- **Purpose fit.** Maintainability includes **docs that do not lie about
  mechanisms**. (B) restores promise/mechanism agreement at prose cost; (A)
  buys convenience with cross-registry machinery and a new failure mode —
  against the grain of both fixed points.

### R4 — OI-11: the "specs mirror the terminal folders" sentence

- **Background.** The design doc ([concurrency-v2.md](../../concurrency-v2.md) §B2)
  says archived spec-of-record files should be split into `complete/` vs
  `cancelled/` folders so location answers "shipped or cancelled?" without
  opening the file. `wi-391` was filed to build exactly that and instead
  **refuted it by measurement**: the mapping is not total (16 of 111 archived
  files map to no terminal state), contradictory for at least one file, has no
  regenerator to keep it fresh, duplicates an answer the live registry already
  gives by location, and has no consumer. The row is cancelled under every
  option; this ruling decides only what the **design text** should say. The
  full decision brief (with a measured trap for the executor: two
  declared-absences lines must be restated, never deleted) lands on the owner
  surface when `wi-391` merges.
- **Options.**

| Option | What it is | For | Against |
|---|---|---|---|
| **(a) RESTATE** *(recommended — also the brief's own recommendation)* | Amend the sentence to record what measurement found: the goal is met by the registry half; no folder layout can meet it for the 16 unattributable files. | The correction lives **where readers meet the claim**; the undecidable files stay named, which is what stops the next reader re-proposing the same tidy-up (which is exactly how this row got filed). | Leaves text in a design doc describing something deliberately not done. |
| (b) STRIKE | Delete the sentence. | State-once-and-link purity; a design doc describes only the design. | The next reader of a flat archive re-proposes the tidy-up, because the refutation lives only where they are not looking. |
| (c) BUILD anyway | Hand-adjudicate the 16 and ship the split. | The navigation gain is real for direct browsing. | Asserts a terminal state that is false for 14% of the corpus; a second un-cross-checked home for a registry fact; a wrong-answer mode added to every future close. |

- **Recommendation: (a) RESTATE.**
- **Purpose fit.** Single-source-of-truth with reachability: the record must be
  findable from where the claim is read, or the same work gets refiled. (c)
  would trade a real invariant for a browsing convenience — the exact trade
  this repo exists to refuse.

---

## After the drain

WI-390 closes the concurrency-v2 program: the spine amendment batch runs alone
and costs the owner **one sitting**. What remains on the owner surface
afterwards is what has always been there — push, hosted CI, and merge-to-main
(push-policy: human).
