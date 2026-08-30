# Decisions taken without consulting the owner — 2026-08-29, OI-67 slices 4 and 6

**Why this exists.** The owner ruled `OI-67` (a) and directed the driver to take
the decisions the ruling leaves open, escalate the high-risk ones to a
cross-family reviewer, and file the rest as their own document. The first
session's decisions are in
[decisions-for-review-2026-08-29.md](decisions-for-review-2026-08-29.md) and the
plan's §4; this file carries the ones slices 4 and 6 took. Each entry states
what was decided, the alternative, why, and what it costs to reverse. Nothing
here is a ruling.

---

## Slice 4 — the split (WI-531)

### 4.1 The harness's argv into each checker is NOT a row — recorded as a class

**Decided:** `check.py`'s step table invokes some twenty checkers and
generators with flags; that argv arm gets no `cli` row per checker. The
exit-code rows are where the harness's decision plugs in; the argv surface is
the generated CLI reference's.

**The alternative:** the literal reading of "a CLI's arguments and its exit
code are two rows" — one `cli` row per checker, ~20 rows, each body restating
its module's argparse surface.

**Why:** plan decision 7 rejects "always split"; the requestor of all twenty
is one module, and the coupling it names (a renamed flag breaks a step) is
already caught by the step running. Rows were minted for every argv arm a kit
module OTHER than the harness drives (`plan_coverage_step` → `plan_coverage`,
`lane` → `integrate`, `integrate`/`intake` → `trunk_step`) and for the
launchers and the agent CLI.

**Reversal cost:** twenty rows and twenty bodies — the same authoring as this
slice's whole mint. **This is the entry most worth a second opinion**, because
it is the largest population the ruled shape left un-split by a decision
rather than by a reading.

### 4.2 Two duplicate pairs collapsed; the test is the symbol set

**Decided:** `IF-127` → `IF-075` and `IF-116` → `IF-101`. Same owner, same
channel, the same functions taken; only the requestor differed. Where a second
requestor takes a DISTINCT symbol subset (`IF-056`/`082`/`083`/`084`/`138`,
`IF-097`/`099`/`100`) the rows stay.

**Cost:** `TC-161`'s `verifies` re-pointed (a traced cell); its approved
`method` prose still names `IF-127` and was not edited — an approved cell is
the owner's. The ids are spent (watermark), never re-minted.

### 4.3 A generated document's far side is the class that reads it

**Decided:** `IF-019`, `IF-074`, `IF-140` (and the new `IF-146`, `IF-149`,
`IF-164`) name `external:downstream adopter` — the adopting repo's people and
agents — with a `B-05` tie-back, the `IF-018` precedent. Where a kit module
does read the artifact (`traj_parse` reads `docs/okf/`; `agent_common` reads
the status block's section) it is named too.

**The alternative:** name the artifact (the shape slice 3 flagged as
systemic), or a finer external vocabulary (`external:human owner`).

**Why:** the far side is who the information SERVES; a file cannot be served.
One class keeps the vocabulary the frame already has.

### 4.4 A `requestors` row with an external requestor carries no tie-back

**Decided:** `IF-151` (the agent CLI's stdin payload), `IF-154`, `IF-157` —
information coming IN from a party the frame declares no IN crossing for —
carry no `interface_from_external`; the sibling that goes OUT keeps `B-05`.
The reasoning is `IF-041`'s: invoking our hook or launcher is the session's
own act, and a tie-back to an OUT crossing on an IN arm would be a claim the
crossing's own text does not state.

### 4.5 `docs/log.d/` owns a row, and its README is exempt from fragment discovery

**Decided:** `trunk_step.fragment_paths` skips `README.md` by name. The
alternative — owning the fragment grammar on `scripts/trunk_step` instead of
the directory — would put a hand-written medium's definition on its reader,
against the rule that a hand-edited medium declares in its own header.

**Reversal cost:** one line and one test.

### 4.6 Six undeclared `spine_carrier` importers JOIN `IF-102` rather than mint carried rows

**Decided:** `acceptance_record`, `check_trajectory`, `gen_arch_map`,
`plan_coverage`, `spine_rules`, `traj_status` join `IF-102`'s requestor list.
The row's own note said the readers would join as they converted; a carried
row was minted only where the cross-component rule demanded a seam of record,
and `_declared_seam_pairs` covers every pair on the row either way.

### 4.7 Inherited reds closed at the sitting, with reasons on record

**Decided:** `IF-144` (uncited, unlisted since OI-64) gets a reasoned
allowlist entry; the four closed program rows (`WI-528`/`529`/`530`/`532`)
had their `specref` cleared, as R-F says a terminal row does. Both were red
under `--strict` before this slice and unrelated to it.

**Why:** the strict bar is the claim bar; a red inherited is still a red, and
a reasoned entry is the allowlist's own device — accepting what it measures,
not laundering it.

### 4.8 The new rows are allowlisted, not TC-cited

**Decided:** twenty reasoned entries past the seed, each naming its parent and
what closes it. The alternative — widening the parents' TCs to cite both
kinds — is spine authoring under approval (approved `method` cells), which the
plan's slice 4 does not include ("every citation re-pointed", not "new
citations minted"). `if_tc_allow_hygiene_findings` reports the growth every
run; the burn-down is visible.

### 4.9 `--since` is a flag, not a connective

**Decided:** `trace._IF_CONNECTIVE_RE` ignores a token opening with a hyphen.
A `cli` row's `Data` legitimately lists `audit --since`; the form rule reads
form only, so the form must be a word. One lookbehind, one test.

---

## Slice 6 — arm the gate (WI-533)

### 6.1 Our reading of an external surface lives in the far-side module's header

**Decided:** an `external:`-owned row is declared and stated by the kit
module on its far side — the consumer that reads the surface (`check_privacy`
for git, `check_vendored` for the upstream docs) or the requestor that drives
it (`agent_session` for the agent CLI) — and a module that is not the far side
may not state it (a strict finding). The body is written as "our reading of":
what is read or sent, what is assumed, what a failure does.

**The alternative:** the `data` cell (160 characters — too short for a
definition), or a dedicated `docs/external/` document per party (a second
home, hand-maintained, that no check ties to the code that faces the surface).

**Why:** the far-side module is the one in-tree place a check can hold to the
code; the header moves with the code that honours the reading.

**Reversal cost:** three bodies move; one arm of the gate changes.

### 6.2 The strict arm is the ruled rule — declared-not-stated; an undeclared owner stays a warn

**Decided:** `contract_body_findings` fails (under `--strict`) a row its
owner DECLARES but does not state, an external-owned row no far side states,
and a stray declaration. An owner that declares nothing stays the owner-exact
reverse check's warn.

**The alternative:** promote the undeclared case too, closing the dodge
"never declare, never owe a body". Built first, then withdrawn: it reds every
fixture and adopter row whose owner has not been headed at all — the migration
list, not a defect in a stated definition — and the plan's words are "a
declared seam with no body".

**What it leaves:** the dodge is visible (the reverse check's warn, the
reference's summary line) but not gated. **This is the entry most worth a
second opinion.** Reversal cost: one branch in the gate and one test.

### 6.3 One CSV reader, and a header on a CSV is a header everywhere

**Decided:** `kitlib.spine.csv_body` / `csv_reader` / `csv_rows`, and every
kit reader of a CSV — twelve sites, `trace.structure_findings`' raw-line
column counter included — goes through it. The shipped budgets template stays
headerless (a spreadsheet opens it clean); a copy with a header reads
identically.

**The alternative:** fix the five loaders slice 3 named. Rejected: the sixth
(trace's integrity counter) broke the moment the header landed, which is what
"five" was hiding.

### 6.4 The converter reports a lingering `contract` cell and never drops it

**Decided:** `migrate_carrier --if-shape` names every row still carrying a
`contract` cell on every pass; the cell's content has no mechanical home, so
dropping it would lose the definition. `trace.py --strict` names the row until
it moves. The RESYNC entry gives the two commands that list what will red.

### 6.5 The retired cells are strict in `trace`, both spellings

**Decided:** `Contract`/`contract`, `Provider`/`provider`, `Req-Refs`/`req_refs`,
`Signal`/`signal`, `SignalNote`/`signal_note` — a carrier that still maps the
column hands the column name, one that no longer maps it hands the key back
as itself; both are the same retired cell. `contract` left the schema, so the
dogfood three-leg rule (template = schema ⊇ live) holds with the cell gone.

### 6.6 Slice-4 verdict corrections folded, five findings deferred with reasons

**Decided:** six cheap findings applied here (bodies made true, an overlap
narrowed, a clause moved, a case-fold, a count); five deferred: two row mints
(`IF-156`'s deletion arm, `IF-020`'s stdout and log kinds — the next
worklist, with the arms the split surfaced), three non-conforming tracked
fragments (the trunk lane's), the approved `TC-161` prose (the owner's), and
"strict allows invalid ownership/body states" (this slice's gate). The
slice-6 round itself is owed, not skipped: the sitting closed at the commit
bar plus the full suite.
