## 2026-08-23 — WI-455 slice 4: the held IF `Contract` provenance citations are swept, and the hold expires on its own terms

`OI-36` ruled (b) on 2026-08-19 — SWEEP THE 8, HOLD THE 49 — and named the
hold's expiry condition rather than leaving it to drift: the 49 wait on
`WI-455`'s interface lane, itself blocked behind `WI-469`. `WI-469` landed, so
the hold's blocker cleared and this slice executes the ruled pass. The live
`Contract` cells no longer cite the work items and repo-lock decisions that
shaped them; the log holds that account, which is what the ruling said.

Deferred open items: OI-60

**Scope discipline.** Item 1 of the lane's STILL OWED list (the
`direction`/`this_project` shed and the counterpart→consumers transform) was
NOT touched — it is blocked on `OI-60`, pending, and no column or endpoint cell
moved in this commit. Item 3 (the `external.toml` context view) is unstarted
and untouched.

### The population, re-measured before editing: 48, not 49

The lane spec and `docs/provenance-allow`'s header both record **49** (46
`Contract names WI-###` + 3 `Contract cites decision`), last re-measured
2026-08-22. Live at this slice's start it is **48** (45 + 3) over **35 rows**.
One `Contract names WI-###` finding left with `WI-469`'s re-authoring of the
`Consumes` rows — exactly the drift the hold was pinned onto a read surface to
make visible, and the reason the expiry record below states both numbers
instead of only the one that executed.

<!-- fig: cmd="python project-trajectory/scripts/trace.py --root ." rev=0f3b4eca -->

| advisory arm | before | after |
| --- | ---: | ---: |
| `Contract names WI-###` | 45 | **0** |
| `Contract cites decision D-#` | 3 | **0** |
| *(the held population)* | **48** | **0** |
| `Contract argues (...)` — a DIFFERENT rule, not this pass | 28 | 27 |
| `Contract is N characters` — a DIFFERENT rule, not this pass | 36 | 35 |
| all `WARNING (advisory)` lines, whole run | 125 | **75** |

The two out-of-scope arms each drop by one as a side effect of a deleted
sentence; neither was aimed at, and 27/35 remain for whoever rules on them.

### Per-row disposition — 35 rows, 24 plain deletions and 11 rewrites

**Plain deletion** = the citation was a parenthetical tag or a whole provenance
sentence, and removing it leaves the cell stating what crosses. **Rewrite** =
the citation was load-bearing — deleting the clause would have taken contract
content with it — so the cell re-states the fact plainly under its own steam.

| row | citation(s) removed | disposition |
| --- | --- | --- |
| `IF-010` | `WI-455` | deleted |
| `IF-015` | `WI-374`, `WI-381` | **rewritten** — the parenthetical also named the sibling modules (`dispatch.py` + `lane.py`); the ids go, the siblings stay |
| `IF-023` | `WI-455` | deleted (the whole "the retired parse became a live AST scan" parenthetical; the cell already names the `[paths]` src tree it reads) |
| `IF-024` | `WI-280`, `WI-455` | **rewritten** — the `WI-280` clause states WHERE the registry read lives; re-voiced as a plain clause and the `WI-455` history dropped |
| `IF-028` | `WI-455` | deleted |
| `IF-029` | `WI-455` | **rewritten** — the clause carried the doc path; now `(docs/runtime-flows.md)` plainly |
| `IF-044` | `WI-196` | **rewritten** — everything after `WI-196:` is the planner-pair contract; only the id label goes |
| `IF-052` | `WI-280` | **rewritten** — same shape: the id label goes, the `traj_parse._stage_value` / `traj_panels.process_panel` naming stays |
| `IF-056` | `WI-280`, `WI-064`, `WI-290` | **rewritten** — the `Declared at WI-064 … reworded at WI-290` sentence DELETED whole (it carried the two retired `CMP-002`/`CMP-001` ids); the `WI-280 split the consumer:` opener re-voiced so the sibling seams `IF-082`/`IF-083`/`IF-084` are still named |
| `IF-058` | `WI-194` | deleted |
| `IF-061` | `WI-198` | deleted |
| `IF-064` | `WI-218`, `WI-216`, `WI-217` | deleted (three bare tags) |
| `IF-065` | `WI-218`, `WI-148` | deleted (`the WI-148 blackout window` → `the blackout window`) |
| `IF-066` | `WI-218`, `WI-194` | **rewritten** — `the WI-194..198 modules` named its collaborators only by id; now `the dual-plan round-lifecycle and round-artifact modules` |
| `IF-068` | `WI-274` | deleted |
| `IF-071` | `WI-280`, `WI-284` | **rewritten** — `WI-280:` opener re-voiced; `(the WI-284 try/except)` → `(a guarded try/except)`, which is the property the seam actually has |
| `IF-072` | `WI-308` | deleted |
| `IF-073` | `WI-322` | deleted — the whole `(WI-322, OI-10 ruled option (b))` parenthetical, both citations together: leaving the `OI-10` half would have left a provenance clause of the same shape the pass exists to remove |
| `IF-074` | `WI-322`, `WI-266` | **rewritten** — the masking rule keeps its reason (`refs/llm/* facts do not transport with clone/push`) and loses `the M-10/WI-266 rule inherited from the markdown block it replaces` |
| `IF-075` | `WI-322` | deleted |
| `IF-076` | `WI-329` | deleted |
| `IF-077` | `WI-326`, `WI-354` | deleted — the `Declared at WI-354 …` sentence whole (it carried the retired `CMP-001`/`CMP-003` ids) and the trailing `the split that let WI-326 cite a truncated heading for two days` clause; nothing re-worded |
| `IF-082` | `WI-280` | deleted |
| `IF-083` | `WI-280` | deleted |
| `IF-084` | `WI-280` | deleted |
| `IF-085` | `WI-280` | deleted |
| `IF-090` | `WI-388` | deleted |
| `IF-091` | `WI-380`, `WI-388` | **rewritten** — `the WI-380 amendment seam` named the seam ONLY by the work item that built it; now `the spine-amendment seam`. `per the WI-388 ruling` dropped from the routed-subset parenthetical |
| `IF-094` | `WI-389` | deleted |
| `IF-102` | `D-5` (`OI-12 / repo-lock D-5`) | deleted |
| `IF-108` | `D-6` (`repo-lock D-6`) | deleted |
| `IF-117` | `WI-429`, `D-9` | deleted (the whole `(WI-429, the discharge test repo-lock D-9 leaves open for the LLR tier)` parenthetical) |
| `IF-121` | `WI-454` | **rewritten** — `(gating is an owner ruling not yet made)` is the live reason `--strict` is off and STAYS; `; WI-454's scope guard` goes |
| `IF-131` | `WI-455` | deleted |
| `IF-132` | `WI-455` | deleted |

Verified as the spec required: the two retired `CMP-00x` ids that were
deliberately left inside `IF-056`'s and `IF-077`'s held clauses **died with
their sentences** — both `Contract` cells now carry no `CMP-` token at all, and
correcting a number inside a sentence already scheduled for deletion was indeed
the two-passes-for-one-fix the lane declined.

**The two `WI-390` banked interface-tier hits did NOT ride along, and that is
the honest answer rather than a skip.** `IF-055`'s dead `SCHED_*` constants and
`IF-080`'s "candidate worktree" phrase are not in this pass's population —
neither cell carries a `WI-###` or `D-#` citation, so neither is one of the 48.
They stay banked in
[`WI-390`'s closed spec](../archive/work/complete/WI-390-concurrency-v2-program-close.md);
this pass had no warrant to open cells it was not ruled over.

### `docs/provenance-allow`: the hold EXPIRES, recorded rather than deleted

The file's own contract governs this. Its entry list is unaffected — it has
been empty since 2026-08-20, and the 49 never had entries because
`trace.if_contract_advisories` takes no `allow` parameter, so an entry naming
them would have declared nothing. The hold lived in the HEADER, and the header
is what changes:

- The `THE HELD POPULATION THIS FILE CANNOT LIST` clause becomes
  `… COULD NOT LIST — EXPIRED 2026-08-23, EXECUTED`, stating what the pass did,
  that the detector now reports zero on both arms, and that it stays warn-only
  so a NEW citation re-opens the question by reporting rather than by an entry.
- The `WHAT THE HOLD IS WAITING ON` clause folds into it: the blocker chain
  (`WI-455` → `WI-469`) is named as discharged rather than struck, because the
  clause existed so the hold could expire visibly.
- The 49-vs-48 drift is written into that record. Pinning the hold on a read
  surface was the whole point of `OI-36`'s "a population could grow or shrink
  with no artifact changing and no one told"; the one citation that left with
  `WI-469` is the first and only thing that pin ever caught, and deleting the
  clause would have thrown away its single measurement.
- The `NO ACTIVE ENTRIES` block stops excepting the `Contract` hold from its
  own all-clear, since there is no longer a held population to except.

**Consumer coherence, checked not assumed.** The file's readers are
`trace.load_provenance_allow` / `parse_provenance_allow` (entry lines only —
every `#` line is comment), `trace.provenance_allow_findings` and
`provenance_allow_parse_findings` (integrity floor, over entries), and
`gen_open_items.deferral_findings` (entry count vs pending rows). No entry line
moved, so every one of them reads exactly what it read before. `OI-36`'s
`open-items.toml` row is already `status = "ruled"` (2026-08-19) and needs no
edit; the ruling was already recorded, only its execution was outstanding.

### Approval authority — verified, not asserted

The concern was real and the answer is clean: **all 35 rows are
`status = "Drafted"`**, so no approved text moved. `agent_common.human_approves`
governs a WRITER of an off-spine `status` cell, not the content of a `contract`
cell, and this pass writes no `status`. `intake.py snapshot`'s
`baseline_snapshot.refresh_refusal` (the `--approves` warrant) fires only when a
refresh would absorb APPROVED text no `Status` flip authorises — no refresh is
run here and no approved text exists in this set. `check_trajectory.
staged_snapshot_findings` triggers only on a commit that touches
`docs/archive/last_approved/`, which this one does not. `interfaces.toml` is
off-spine and outside `SPINE_CSVS`, so no re-attestation arm engages. **No cell
was stopped on; nothing is owed to a human warrant.**

### Deviations from spec

1. **Population is 48, not the 49 the lane spec states.** Measured, recorded
   above, and written into the expiry record rather than silently reconciled.
2. **`IF-073`: one non-`WI`/non-`D` citation went with its clause.** The
   parenthetical was `(WI-322, OI-10 ruled option (b))` — the detector saw only
   `WI-322`, but the clause is one provenance unit and half of it is still a
   citation clause. Deleting the whole parenthetical is the pass's own rule
   applied honestly; leaving `(OI-10 ruled option (b))` behind would have been
   the letter against the ruling.
3. **Two citation-shaped phrases left standing, deliberately, as findings not
   fixes.** `IF-090`'s `flip_verified/adjudication_action enact ruled decision
   2` and `IF-094`'s `the ruled A1/A8 tables read as constants` name a ruling in
   prose with no id the detector matches. They read as contract-by-reference and
   are a smell, but they are outside the ruled population and re-voicing them is
   a judgement about what those functions DO — surfaced here rather than fixed
   inline (`CLAUDE.md`, "Communication style").

### Gates

<!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=0f3b4eca -->
<!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=0f3b4eca -->

- `python -m pytest -q -n auto -m smoke` — **1266 passed, 5 skipped in 20.03s**
- `python scripts/check_smoke_budget.py --mode enforce` — **1266 passed, 5
  skipped in 24.86s**; `smoke wall-clock budget: 25.3s vs 60s budget ->
  within`, exit 0
- `python project-trajectory/scripts/check_docs.py --root . --stale` — `OK -
  1032 doc(s), 1356 intra-repo link(s), 0 broken (1 orphan warning(s))`, exit 0
- `python project-trajectory/scripts/check_trajectory.py --root . --strict` —
  `clean (507 work item(s), 480 done (95%), 21 cancelled, graph acyclic)`,
  exit 0 (pre-existing WARNs unchanged)
- `python project-trajectory/scripts/trace.py --root . --strict-integrity` —
  `integrity=0 … interfaces=129 interface-findings=0`, exit 0
- Surfaces regenerated: `gen_trajectory.py` (`wrote PROJECT_STATE.html`),
  `gen_open_items.py --check` (`open-items view up to date`)

Full unfiltered suite NOT owed: this is registry-cell + declared-file work, and
no executable code changed (`docs/provenance-allow` is a declared config
surface, and only its comment header moved).

Byte deltas on budgeted files: none — no budgeted file was touched.
