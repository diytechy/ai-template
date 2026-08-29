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

_(filled as the slice lands)_
