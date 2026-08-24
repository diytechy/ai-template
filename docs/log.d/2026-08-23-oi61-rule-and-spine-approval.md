## 2026-08-23 — OI-61 ruled, the surfaced spine set approved, and nineteen drafts the owner surface never showed

Two owner acts landed in one sentence, in session 2026-08-23. The owner's
words, verbatim, because both halves are load-bearing and the second half is a
warrant rather than an opinion:

> **"OI-61: I agree with the recommendation, let's see where it lands, and I
> approve of the other spine changes surfaced in open-items.html"**

One commit, not two, on `d16ddbb2`'s precedent from the day before: a ruling and
the acts it authorizes are one event, and splitting them leaves a ruling in the
registry whose execution record lives somewhere else.

Deferred open items: none — the item this sitting ruled is RULED, and its
execution row is queued WORK rather than a deferral (the id is deliberately not
repeated on this line: the deferral scanner reads it as a deferral, and it is
the opposite of one). The one thing this sitting could not close is a
mechanism gap, recorded in full below and in `docs/status.md`; it is not a
decision anyone owes today.

### Act 1 — `OI-61` ruled: the recommendation as written

`status = "ruled"`, `ruled_date = "2026-08-23"`, `ruling_ref` = this fragment,
`wi_refs = ["WI-512"]`. The ruling is written into the row's `recommendation`
cell above the pre-ruling text, which is kept verbatim — the `OI-60` form from
the day before. The four parts, restated so no executor infers them from prose:

1. **(a) NOW, declared as the first step toward (b)** — the 27 CLI `contract`
   cells thin to the typed crossing statement, and the argparse-derived
   generated CLI reference rides along as (a)'s second step rather than a
   separate row.
2. **(d)'s named-symbol tripwire folded in, scoped to surviving prose** — one
   warn-first rule in `trace.if_contract_advisories` on WI-502's AST grammar.
   Taken WITH (a), never instead of it.
3. **(c) deferred on a CONDITION, not on discomfort** — re-raise when (a) has
   landed, (d) is reporting, and a residual rot class is DEMONSTRATED that
   neither reached (`IF-080`'s class is the standing candidate). *"Let's see
   where it lands"* is read as exactly this: (a)'s outcome is a NUMBER, and
   that number is what makes (b) obvious or refutable across the other 108
   rows.
4. **The sub-question SANCTIONED now** — an optional `verified_by` cell on the
   IF row (a TC id or an LLR id, empty meaning "verified in its own right"),
   warn-first that the pointer resolves.

**Execution row minted: `WI-512`**, queued, `buildtier = "strong"`, workstream
`requirements`, safety_class `spine`, `needs = ["WI-455"]`, priority 3 —
[../archive/work/complete/WI-512-if-contract-generalization.md](../archive/work/complete/WI-512-if-contract-generalization.md).
`strong` rather than `medium` deliberately: the row re-authors 27 cells of a
SHIPPED registry, adds a cell to its schema, and moves
`INTERFACES.template.md`, `registries/interfaces.template.toml`, PROCESS.md §8's
field list, `EXAMPLE.md`, `test_dogfood_sync.py` parity and a `RESYNC_PACK.md`
entry — spine-touching and design-shaping on both counts. The hard `needs` edge
is the ruling's own sequencing: (a) runs after the `counterpart` → `consumers`
rename, which is what gives the short form a real cell to point at. Its Context
carries the ruling's four stages and the brief's census pointers, and it OWES
BACK the number (c)'s deferral is conditioned on. Watermark raised through
`trace.py --bump-ids`: `WI 511 -> 512`. **Nothing was executed in this session**
— the pass itself is the row's, not the ruling's.

### Act 2 — the spine approval, executed against the surfaces the owner read

**The dated brief was minted FIRST**, before a single cell moved, because it is
the record of the signing moment and not of its consequences:
[../ratify/2026-08-23-spine-approval.md](../ratify/2026-08-23-spine-approval.md)
(`trace.py --mint-approval-brief spine-approval`, immutable thereafter under
`check.py approval-immutable`). It is a byte copy of the `CURRENT.md` the owner
was reading — including its `Approval provenance: … 77d67c38` line, which a
regeneration would have moved to `098278ae`. That one-line staleness is the only
respect in which the committed `CURRENT.md` differed from a fresh render at
HEAD, verified by diff before minting; the brief keeps what was on screen.

**The approved set, enumerated from the surfaces — THREE rows, one SR chain.**
`docs/open-items.html` at HEAD: *"1 spine row(s) owing a approval or a
re-attest, across 3 chain row change(s); 1 row(s) drifted from the approved
snapshot."* `CURRENT.md`: one section, `SR-049`.

| Row | State on the surface | What the act did |
| --- | --- | --- |
| `LLR-147` | DRIFTED — `Detail`, the sole approved-cell drift in the tree | blessed by the baseline re-seed; the cell's text was NOT edited |
| `LLR-197` | ADDED since the snapshot, `Drafted` | `Status` → `Approved` |
| `TC-193` | ADDED since the snapshot, `Drafted` | `Status` → `Approved` |

The flip is **`Status` cells only** — two lines, `"Drafted"` → `"Approved"`, and
the whole registry diff is exactly `2 +status = "Approved"` / `2 -status =
"Drafted"`. No row's text was edited, which is what keeps this an approval
rather than an amendment. That `LLR-147` is the ONE drifted approved row was
re-verified against the machinery rather than taken from the rendering: `trace.py
--approve modified` re-run on a stashed-clean tree at HEAD emits one `##`
section and three `###` rows, the same three. (A hand-rolled cell diff over the
raw TOML *also* flagged `LLR-139` and `LLR-164` — that comparison is WRONG and is
recorded as such: it used the TOML key names, so `split_changed_cells` could not
apply the §A5.1 approved/traced split and defaulted everything to "approved".
Those two rows moved TRACED cells, which by the WI-388 ruling never arm a
re-attest window.)

**The authority.** `docs/process.toml`'s `human_approval_through` reads
`DevStg-Needs`, so the SR/LLR/TC tier is agent-performable at this dial — and
here it is additionally owner-directed in writing. All 27 SN rows read
`Approved`; nothing on the human-held tier was touched.

**The baseline re-seed.** `intake.py snapshot --approves "<the owner's words
verbatim> — recorded at docs/log.d/2026-08-23-oi61-rule-and-spine-approval.md"`
— **7 registry files copied**, the warrant recorded in the snapshot's own prose
stamp (`docs/archive/last_approved/README.md`). The `--approves` flag was given
rather than ridden on the two `Status` flips because the refresh absorbs
`LLR-147`'s ratified `Detail`, and the record of WHO authorized that belongs in
the stamp. Absorbed alongside it is every registry change committed since the
last copy at `27a30842` — but only `LLR-147` was an approved-cell amendment;
everything else is `Drafted` rows and off-spine (IF) content that no approval
claim rides.

**The standing `LLR-147` refusal is CLEARED — verified, not assumed.**
`baseline_snapshot.refresh_refusal('.')` returns `None` after the re-seed, and
`trace.py --approve modified --check` reports *"no row owes an approval or a
re-attest — the window is closed"* (exit 0). The `docs/status.md` bullet that
carried the block since WI-483 slice 3 is rewritten to say so.

### THE DISCREPANCY — nineteen `Drafted` spine rows the owner surface does not enumerate

This is the sitting's real finding, and it is why the approved set is three rows
and not twenty-one. It was STOPPED ON rather than resolved.

The registries carry **21 `Drafted` spine rows** (10 LLR: `LLR-187`, `-193`,
`-194`, `-196`, `-197`, `-198`, `-199`, `-200`, `-201`, `-202`; 11 TC: `TC-182`,
`-188`, `-189`, `-191`, `-192`, `-193`, `-194`, `-195`, `-196`, `-197`, `-198`),
and `docs/stage` reports `drafted = 21` honestly. The owner surface reported
**one** row owing. Only `LLR-197` and `TC-193` were visible, and only because
they are chain rows of `SR-049`, which owed for a different reason —
`LLR-147`'s drift.

The mechanism, read out of the code rather than inferred:
`trace.reattest_model`'s `owes(sr)` returns `is_drafted(sr) or
sr_chain_drifts(...)`. The `is_drafted` arm tests the **SR row only**. A
`Drafted` LLR or TC under an Approved, undrifted SR therefore reaches no
surface: `sr_chain_drifts` cannot see it either, because
`baseline_snapshot.is_drifted` returns False for a row below approval ("it has
made no claim to fall from") and False for a row absent from the snapshot
("unanchored, not drifted"). Both of those individual rules are right. The gap
is that nothing then asks the `Drafted` question of a child. The model's own
docstring states the contract it misses: *"A row now owes an act when it is
`Drafted` (a first approval is owed)"*.

**So nineteen rows owing a first approval are invisible to the surface a human
approves from**, while `docs/stage` and the generated block in `docs/status.md`
report the count correctly — two surfaces disagreeing about the same registry
state, which is exactly the class the brief's own header warns about ("if the
two ever disagree, the brief is authoritative and this view is the bug"; here
they agree with each other and both disagree with the tree).

**What was done about it: nothing, deliberately.** The owner approved *"the
other spine changes surfaced in open-items.html"*, and those nineteen were not
surfaced there. Approving them under this warrant would be exactly the
laundering the whole apparatus exists to prevent. No row was minted for the fix
either: whether the answer is a widened `owes()` or a ruled scoping of what a
brief is FOR is an owner-level question, and the sitting that found the gap is
not the sitting to rule it. It is recorded in `docs/status.md` as an unfiled,
owner-facing item and reported back to the owner directly.

### The ladder — unmoved, and that is the honest reading

| Field | Before | After |
| --- | --- | --- |
| `stage` (selection) | `DevStg-LLReqs` (ord 4) | `DevStg-LLReqs` |
| `settled-stage` | `DevStg-LLReqs` | `DevStg-LLReqs` |
| `live-stage` | `DevStg-LLReqs` | `DevStg-LLReqs` |
| `per-phase-live` | `1=LLReqs;3=Impl;4=LLReqs;5=LLReqs` | unchanged |
| `drafted` | `21` | **`19`** |

Nothing moved but the draft count, and the mechanism says why: unlike the
2026-08-22 act — where fifteen drafts were holding `live-stage` a rung below
`settled-stage` — `live` and `settled` were ALREADY equal here, so the two
approvals had no rung to close. **What holds the ladder at `DevStg-LLReqs` is
the orphan debt, unchanged by this act and outside its scope**: `SR-163` and
`SR-181` each have no LLR and no TC (4 orphan findings, the same 4 as at HEAD).
The nineteen remaining drafts are NOT what the ladder is waiting on — they are
excluded from the settled fold by design — so the surface gap above is an
approval-record defect, not a stage-ladder one.

Surfaces re-derived through the ordered path — `trunk_step.py --regen`
(derived-stage, trajectory, status, open-items, component-view; okf skipped,
`docs/okf/` absent by the 2026-08-18 dial) — plus `trace.py --approve modified
--out docs/ratify/CURRENT.md`, which `--regen` does not cover, and `trace.py`
for the gitignored `docs/test/report.md`. `open-items.html` now reads **0
pending decision(s) · 0 spine row(s) owing · 0 row(s) drifted**. The
one-commit lag in the surfaces' `Baseline: … (27a30842)` stamp is the house
state, not an error: `27a30842`'s own `open-items.html` cited `0cfb2e6f` the
same way, because the stamp is a `git log` read over `docs/archive/last_approved`
and this commit is the one writing it.

### Gates — registry and record work, so the commit bar, not the gate bar

No executable code changed (registries, generated surfaces, one WI spec, one
fragment, one immutable brief), so no full suite is owed.

- Smoke: **1311 passed, 5 skipped in 25.54 s**, and
  `check_smoke_budget.py --mode enforce` reads **26.0 s vs 60 s → within**.
  One condition stated rather than folded into the green: the same tier run
  through the SYSTEM interpreter on this box read **68.63 s** on a cold cache
  in the same sitting. The budget checker drives
  `C:\Projects\ai-template\.venv\Scripts\python.exe`, which is the declared
  interpreter, so 26.0 s is the figure the bar is measured on — but a worker
  who types `python -m pytest` here will see a number past the ceiling, and
  that is an environment fact worth knowing, not a budget argument.
- `check_docs --stale`: **1050 docs, 1363 intra-repo links, 0 broken**, 1
  orphan warning (`docs/test/report.md`, the generated matrix — pre-existing).
- `check_trajectory.py --strict`: exit 0 — **clean, 509 work items, 482 done
  (95%), 21 cancelled, graph acyclic**. Two WARNs this act introduced were
  FIXED rather than accepted: `WI-512`'s title was 177 chars (ceiling 120) and
  its filename stem 40 (ceiling 37, the Windows MAX_PATH cliff `WI-462`
  closed) — both trimmed before the commit.
- `gen_open_items.py --check`: view up to date; this fragment's
  `Deferred open items` line is clean.
- `trace.py --strict-integrity`: exit 0 — `SN=27 SR=75 LLR=184 TC=181
  orphans=4 integrity=0 drafts=19 interface-findings=0 provenance-findings=1`.
  Verification basis stated rather than folded into "green": **72 mechanized,
  3 demonstrated, 0 attested**.
- **`trace.py --strict` exits 1, and it did at HEAD too** — the 4 orphan
  findings (`SR-163`/`SR-181`) plus one provenance finding, *"LLR-197 Detail
  cites 'WI-448'"*. Both predate this act and neither was created by it; the
  provenance finding sits on a row this act APPROVED, which is worth saying
  plainly rather than leaving to be discovered: it is warn-class in the
  advisory tier and gating under `--strict`, and it belongs to whoever next
  sweeps `LLR-197`'s citation frame. The declared bar for this class of work is
  `integrity=0`, which is met.
