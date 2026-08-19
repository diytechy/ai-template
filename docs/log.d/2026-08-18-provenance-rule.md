## 2026-08-18m — NO provenance citation in a living registry cell (owner ruling, in-session)

**The ruling, as given.** Recorded verbatim because it *is* the authorizing
ruling — there is no earlier written form of it:

> **no provenance citations in any living registry cell.** A reason cell
> (`rationale`/`why`/`notes`) must state what breaks without the row and which
> alternative lost, in standing prose, with NO ruling reference, sitting
> reference, OI id, decision id, review-round code, edit-history verb, or date
> stamp. The detailed history belongs in `docs/log.md` and the archive. This
> REPEALS the permission at PROCESS.md:143-148 ("A review, ruling or design-thread
> reference is optional context *on top of* a sentence that already stands
> alone"). The substance of the reasoning STAYS; only the citation frame goes.

Two standing holds were respected: `docs/cmp/` was NOT materialized, and no new
spine or open-item rows were minted.

Filed as a **log fragment with no WI row**, on this month's precedent for
in-session owner-directive sweeps (`2026-08-18-doc-diet`, `-okf-off`,
`-scripts-sweep`, `-spine-hardening`, `-budget-guard`, `-sn-artifact-voice`).
Every registry edit below is **provisional** — every spine tier is human-held
here (`human_ratification_through = 4`), no `status` cell moved, nothing was
attested. The re-attest sitting countersigns.

---

### 1. The rule

**`project-trajectory/PROCESS.md` §3**, two bullets.

The stand-alone bullet was scoped to `SR`/`LLR`/`TC` normative text and two
token shapes. It now names **all four spine tiers** (`SN` joins) and the
**reason cell** beside the normative ones, and enumerates the whole citation
frame: work-item id, process-doc citation, ruling / sitting / review-round /
open-item reference, decision id, edit-history verb, date stamp. It also states
the split severity in the same sentence — gating under `--strict` on the two
original shapes, warn-first on the rest — so a reader cannot mistake the
widening for a new gate.

The rationale bullet is where the repeal lands. It read:

> A review, ruling or design-thread reference is optional context *on top of* a
> sentence that already stands alone — never a substitute for one.

It now reads that a rationale carries its own reason **and only that**, as
standing prose, carrying no citation frame of any kind, with the account moved
to the log. **The bullet's original purpose is intact and was the thing to
protect**: its worry was an author deleting a citation *and the reasoning with
it*, and the new text still forbids that in terms — "**Drop the frame, keep the
reason**: where deleting the citation would leave a bare assertion, restate the
reasoning as prose that stands on its own. Deleting the citation *and* the
reasoning with it is the failure this exists to prevent."

`PROCESS.md` is byte-watched. Measured: **81,602 → 82,190 (+588)**; the watched
row is re-stamped replace-style in all three `byte-budget-guard/SKILL.md` copies
(source + `.claude/` + `.agents/`, byte-identical). No capped file moved except
that skill itself, 4,124 → 4,206 against a 5,000 cap (794 headroom).

**`spine-authoring/SKILL.md`** carries the author-facing version, in all three
copies. §6 *Cell hygiene* gains two bullets — "The reason cell is not a
changelog" and "When you strip a frame, keep the reason", the second with a
worked before/after — and §1(e)'s carve-out is corrected: it had told authors
that a **provenance citation** needs no artifact-naming waiver "because it is not
a carrier", which after this ruling reads as permission to put one in the cell.
It now says a provenance citation does not belong in the cell at all.

### 2. The detector

`trace_text.provenance_findings` is **UNCHANGED** — same two token shapes, same
three tiers, same `--strict` gating. The three live class-1 findings
(LLR-013/038/067) kept their severity throughout and are now cleared on their
merits, not by a severity change.

Two new **warn-first, never gating** producers:

- `trace_text.provenance_advisories(needs, srs, llrs, tcs, allow)` — the SN tier
  (`need`/`why`/`acceptance`, lower-cased keys off `load_needs`) plus the wider
  vocabulary over SR/LLR/TC.
- `trace.if_note_advisories(ifs, allow)` — the IF tier's `Notes`/`SignalNote`.
  A **separate** arm from `if_contract_advisories` rather than another cell in
  its loop: that arm's connective and 500-character rules say "this cell is not
  the place to argue", and a `Notes` cell arguing is that cell working correctly.

Severity is warn-first **by the ruling's own terms**: the repo is mid-program at
`DevStg-Reqs`, the measured population was ~300 tokens over ~150 live rows, and a
new gate would have wedged the harness on a prose campaign. `exit_code` is
untouched, so the advisory tier physically cannot gate.

**Vocabulary — structured shapes only, never bare English words.** `OI-\d+`,
`sitting-\d+`, `C-[A-Z]{2,5}-\d+`, `D-\d+`, `RULING-\d+`, an edit verb followed
within one clause by an ISO date, and a bare ISO date **in a reason cell only**
(a normative cell may carry a date as data).

**Both documented false-positive hazards were re-measured, not assumed.**

1. *The reverted `<LETTER>-<n>` pattern.* `trace.py`'s `_IF_DECISION_RE` records
   that a general id shape was tried and reverted for reading the data pack's
   `M-10` crossing ids as rulings. Nothing here generalises over id shapes;
   measured over the live registries, `M-10` is matched by none of them.
2. *The subject-noun population.* `ruling`/`retired`/`attestation`/`amended` are
   subject nouns in every row specifying the ratification machinery itself —
   **measured at 217 occurrences across 108 live SR/LLR/TC rows**, with SR-149,
   SR-165 and LLR-118 the worked instances. The edit-stamp shape requires a date
   behind the verb, so **0 of those 217** are flagged; SR-165 and LLR-118 are
   silent outright, and SR-149 reports only its `OI-21` / `C-MNT-3` / dated
   `added` frames, which are real.

**Measured false-positive rate: 0 of 319 findings** on the pre-sweep registries.
One class was found and suppressed before finalizing: a date inside a
slash-joined path token (`docs/plans/2026-08-16-blind-derivation-c-hats.md`) is a
POINTER, not a stamp, and reporting "cites 2026-08-16" about it names the wrong
thing — 12 of 76 date matches. `_in_path_token` drops them. One borderline
survives as a true positive by the ruling's letter: SR-144's "merged rejected
code onto trunk on 2026-08-03" is a date stamp inside an otherwise durable
argument; it was restated without the date.

Regression tests in `tests/test_trace_rules.py`, matching the module's idiom
(positive half, negative half, message shape), including the negative tests that
pin the `M-10` and subject-noun cases silent, the dated-path case silent, and the
normative-cell bare date silent.

`trace.py`'s shipped advice was reworded where it taught the repealed rule:
"Move it to Rationale" / "Move the citation to Rationale" / "the Rationale column
is its home" now point at the log. `interfaces.template.toml`'s rationale charter
("the sentence that used to squat in Contract") now says the column takes the
ARGUMENT, never the CITATION; `system-requirements.template.toml` and
`low-level-requirements.template.toml` carry the same clause.

### 3. The sweep, per row

Every edit is a text edit in a reason or normative cell. **No `status` cell
moved, no row's meaning changed, no id minted or retired.**

**(a) The three class-1 violations — pure changelog tails, deleted.**

| Row | Before (tail) | After |
|---|---|---|
| LLR-013 `detail` | `WI-455 landed the ruled retirement of docs/architecture.md, which previously held the Runtime flows section — and the obligation FOLLOWED THE HOME rather than standing down…` | `The recorded dependency is on the authored-flow surface as a class, not on any one file, so re-homing the flows re-points the default --doc rather than standing the obligation down.` |
| LLR-038 `detail` | `(module tail -> public symbols; WI-455 - the committed-map parse retired)` | `(module tail -> public symbols)` |
| LLR-067 `detail` | `(gen_arch_map.scan_inventory; WI-455 retired the committed docs/architecture.md block it used to parse back)` | `(gen_arch_map.scan_inventory), never parsed back out of a committed map, so the join cannot read a stale inventory` |

**(b) The SN tier — 9 rows, 28 tokens, now 0.**

| Row | Cell | Frame dropped | Reason kept / restated |
|---|---|---|---|
| SN-005 | `acceptance` | `(Narrowed 2026-08-13 per OI-24: …)` | the narrowing is normative scope, restated: "Full local-CI equivalence on every input is deliberately NOT claimed: it is not mechanizable, so promising it would be a bar nothing can check." |
| SN-006 | `why` | `AMENDED 2026-08-16 (WI-467, provisional):` | kept whole and re-voiced forward: a `why` cell is context, not normative text, so the safety half is stated in the need itself |
| SN-008 | `why` | `AMENDED 2026-08-17 (C-ACC-2, hat.ACCESSIBILITY; sitting-3 §0.4 item 8 ruling):` | **"the signal is the word PASS, never a hue"** kept verbatim in substance, plus the durable reason (a colour word as the only name does not exist for a class of readers) |
| SN-011 | `why` | `(owner RULING-3, 2026-07-28)` | the argument (argument, not abstinence) already stood alone |
| SN-025 | `acceptance` | `retired by WI-180` | "the hand-maintained next-step pointer this need made unnecessary" — the dead id named nothing a reader can resolve |
| SN-027 | `why` | `REWORDED 2026-08-17 (C-PRF-1, hat.PERFORMANCE; sitting-3 §0.4 item 8 ruling):` | **"this states a structural property, not a throughput claim: no instrument here measures speedup"** kept, plus the observability pointer re-voiced without the SR id's mint date |
| SN-034 | `acceptance` | `(Ruled 2026-08-13, OI-17 option (d): …)` | **deleted entirely** — the preceding sentence carries the whole normative content |
| SN-035 | `acceptance` | `(Ruled 2026-08-13, OI-17: …)` | **deleted entirely**, same reading |

**(c) The mechanical duplicate / bookkeeping blocks — pure wins.**

| Block | Rows | Action |
|---|---|---|
| `owner ruling (2026-08-10, repo-lock D-6) amending F5` | IF-102, 104, 105, 106, 107, 108, 109, 110, 111 (9 rows, 3 text variants) | replaced by the single standing reason, once, no citation: "The vocabulary has one home rather than a copy per script: a duplicated vocabulary fails silently, handing back a row with a cell missing instead of raising." |
| `provisional 2026-08-13 (P5, owner ratification owed at return)` | CMP-006, 007, 008, 009 | **deleted** — `status = "Drafted"` already carries that fact mechanically |
| `Minted 2026-08-15 (log …)` / `MINTED … as IF-123; RENUMBERED to IF-131 …` | IF-123 … IF-132 | **deleted** — git and the log hold minting dates, and naming a dead id (`IF-123`, `IF-124`) is actively harmful: it reads as authority and resolves to a live row that is not it |
| `derived at the WI-443 conversion:` (25) / `typed at mint (WI-45x):` (10) | 35 `signal_note` cells | `DERIVED, NOT HAND-TYPED:` / `typed at mint:` — the standing property (this typing was mechanical) survives; the conversion's id does not |

**(d) The reason-cell frames, swept where the forward-looking reason survives.**

Worked through to completion on the spine. Representative shape, repeated ~60
times: `ABSORBS SR-133, 2026-08-15: that row's own rationale read …` →
`ABSORBS the sanctioned-skip row, whose own rationale read …`; `SPLIT 2026-08-16
(re-tier v2 S4, ruling R1 — one decision per row):` → `SPLIT ON THE
ONE-DECISION-PER-ROW RULE:`; `RE-VOICED 2026-08-17 (Sol F14, applied): the shall
was a MENU SPECIFICATION` → `The shall states ONE obligation rather than a menu
specification. It had enumerated …`. Where a block was pure changelog with no
forward half it went (`MINTED 2026-08-17 (Sol F12, applied).`). Where dropping
the frame would have left a bare assertion the reason was **restated**, which is
the whole point — SR-031's stale-crossing note became "read off that row's
current crossings rather than restated here, so a revision there cannot leave a
stale pair here", and SR-168's phase note became "because a phase records WHEN a
piece shipped, and child-later-than-parent is the ordinary case".

Rows touched: **SR** 006, 007, 015, 019, 020, 026, 027, 031, 034, 046, 049, 053,
070, 137, 139, 140, 144, 148, 151, 152, 154, 156, 160, 162, 166, 168, 169, 170,
171, 172, 173, 174, 175, 178, 179 · **LLR** 013, 037*, 038, 067, 146, 147, 148,
154, 158, 166, 168, 173, 176, 178 · **TC** 145, 153, 161, 167 · **IF** 001, 004,
005, 008, 010, 012, 015, 016, 017, 020, 043, 046, 047, 048, 055, 057, 058, 059,
060, 061, 065, 068, 069, 071, 072, 073, 074, 075, 083, 084, 085, 086, 093, 094,
102–111, 116, 120–132 · **CMP** 006, 007, 008, 009 · **B** 04, 05.
(*LLR-037 allow-listed, not edited.)

**Result:** the citation-frame advisory reports **0 findings** across
SN/SR/LLR/TC/IF, the gating stand-alone rule reports **0**, and
`orphans=0 integrity=0`.

### 4. Deferred, and why

Each of these is recorded rather than swept. The seven open-question markers get
a **declared exception** in `docs/provenance-allow` — the `docs/need-form-allow`
idiom, ` — <reason>` separator, `#` comments ignored, a line with no separator
declaring nothing (fail-soft in the loud direction). Every entry states that the
row **owes an open-item row at the sitting**; no such row was minted here, per
the hold.

| Deferred | Disposition |
|---|---|
| SR-043 + SN-006 fail-open contradiction | allow-listed. The pure frame `(2026-08-16 adversarial round, finding F1)` may be dropped inside it; the question is preserved. The `adapted from stop-subagent-fanout, MIT` clause is a **licence attribution** and survives regardless — the allow entry says so. |
| SR-040 carrier-less obligation residue | allow-listed. The row records an obligation nothing satisfies and two dispositions only the owner may pick. |
| LLR-037 + TC-040 tripwire | allow-listed, both halves, ruled together or not at all. |
| IF-117 flagged candidate-gap | allow-listed. |
| IF-123 / IF-127 / IF-130 "PROVISIONAL, for the review sitting to overturn" | allow-listed. |
| `(Derived-requirement label, added 2026-08-16 — PROVISIONAL, unsigned.)` | allow-listed on **15** rows (SR-024, 033, 052, 054, 111, 112, 129, 144, 146, 147, 149, 167, 175, 176, 177) — measured, not the "~8" the brief estimated; SR-040 and SR-043 carry it too and are listed above. Nothing mechanical carries "unsigned", so deleting the parenthetical would silently promote 17 provisional labels to ratified ones. |
| SN-027 `acceptance` "Spec of record", SR-049, SR-043's archived-plan pointer (`docs/archive/specs/**`) | **BLOCKED on the `docs/cmp/` ruling**, not swept. With `docs/cmp/` held, these can only be dropped, which loses the design pointer. Left standing; the detector does not flag a path, so they are invisible to the worklist and this entry is their only record. |
| `docs/archive/last_approved/` citations (SR-140, LLR-173, IF-123, LLR-145, LLR-170) | class 3, declared live machinery — untouched. The paths are not in the detector's vocabulary. (SR-140 and LLR-173 were swept for their *other* frames, `D-9` and `RE-BASED 2026-08-15`; their `last_approved` pointers stand.) |
| `docs/requirements/open-items.toml` | excluded wholesale — it is a decision log whose subject IS provenance. Not scanned, not swept. |
| 49 pre-existing IF `Contract` work-item / decision citations | outside this ruling's scope (the Contract cell has its own rule and its own backlog). Still warn-only; their message now points at the log. |

### 5. Discipline

- Module-size ratchet: `trace.py` **4,298 → 4,406 (+108)**, re-stamped with the
  measured value and the reason (wiring + `if_note_advisories`, which cannot move
  because it composes with the IF rules already in the file, + the loading-layer
  allow reader). `trace_text.py` stays under `THRESHOLD` at 1,163.
- Regenerated: `docs/test/report.{md,html}`, `PROJECT_STATE.html`, `docs/gate`
  (unchanged at `DevStg-Reqs`). `gen_okf` NOT run — dial off.
- `ruff format` applied to the three touched Python files; `ruff format --check`
  clean over `project-trajectory/scripts/` and `tests/` (181 files). The 4
  `ruff check` findings are **pre-existing at HEAD** (verified by stash) and were
  not touched.
- `RESYNC_PACK.md`: one Reserved entry appended, newest-last, naming the widened
  scope, the repealed permission, the two warn-first checks, the adopter's
  worklist procedure, the open-question carve-out and the allow-file convention.
