# WI-451 slice 2 — the execution ledger (running; the WI-444 method with real counts)

**Method of record:** owner ruling `2026-08-14g` (layer-by-layer), executed
against the RATIFIED census
([2026-08-14-wi451-slice1-sr-census.md](2026-08-14-wi451-slice1-sr-census.md),
ruling `2026-08-14b`) and the SR-layer design
(sitting-3 §0.2/§0.3 rows 1–3; the target layer recorded here). **The bar:**
WI-444 token verification — no obligation weakened; every re-stated cell's
obligations accounted for below; every shed clause has a NAMED destination,
and a destination reading "act 3" is OWED, not discharged.

## Act 1 — the 26 tombstones deleted (D-4, `2026-08-14b`)

Executed as its own commit; the forwarding map for all 26 ids is the log
entry (fragment `../log.d/WI-451-slice2-tombstones.md` until merge). SR
149 → 123 · TC 149 → 147 (TC-099 + TC-133) · orphan set bit-identical at 9 ·
no SN lost coverage. IF-053/054 edited; IF-055 re-pointed to SR-132 with its
recorded reason. `trace.py` supersession machinery, the SR-tier carrier key,
the template's example key and the six pinning tests retired; module-size
baselines re-stamped down (`trace.py` 3947→3833, `check_trajectory.py`
4120→4117).
<!-- fig: cmd="python project-trajectory/scripts/trace.py --strict # SR=123 TC=147 orphans=9 integrity=0, commit fd26a966" rev=fd26a966 -->

## Act 2 — the SN→SR layer landed

**The layer (counts):** 34 census HOLDS reattached · 14 census RE-STATES
re-worded in place (the 15th, SR-141, merged into SR-148 per census F5) ·
SR-150 classified HOLD post-census (§ below) · **15 new SRs minted
SR-151…SR-165** (id watermark SR 150 → 165) · `boundary_refs` stamped on all
64 surviving/new rows · SR registry now **137 rows** (123 − 1 merge + 15
mints). Statuses after the act: 65 Verified · 44 Modified · 13 Planned · 15
Draft (the mints; nothing self-ratifies, `human_ratification_through = 4`).
<!-- fig: cmd="python project-trajectory/scripts/trace.py --strict # SN=27 SR=137 LLR=152 TC=147 orphans=1 integrity=0 drafts=42 form-findings=9" rev="act-2 commit tree" -->

**Detector movement:** orphans 9 → **1** — SN-034…SN-040 all gained first
coverage (SN-035 via SR-046's re-homed `sn_refs`, no mint — 13p clean), and
the SR-141→SR-148 merge cured SR-148's missing-LLR/TC pair by re-grounding
LLR-159 and its TC. The remaining orphan is **intended**: SR-035's
Analysis→Test flip owes an LLR+TC minted in act 3. Form findings 18 → 9: the
7 that remain on demote rows (SR-042/050/057/130/131/142/145) dissolve when
those rows land as LLRs (an LLR Detail carries no shall); the other 2 are the
recorded waivers below.

**Boundary-Refs coverage** (uncovered advisory 149 → 73, all 73 the demote
rows that leave the tier in act 3): B-01×5 · B-02×4 · B-04×5 · B-05×53 ·
B-06×1 · B-07×1 — every crossing named by ≥1 SR for the first time.

### One-shall reconciliations (13v)

Re-worded to ONE shall, obligations carried as participles/acceptance —
token-checked against the prior cell: SR-137, SR-138, SR-139, SR-144
(actor named: "the delivered loop content"), SR-146, SR-148 (the merge
re-word), SR-149, SR-017, SR-018, SR-031, SR-040, SR-049 (actor named:
"the delivered harness"), SR-059, SR-070.

**Recorded waivers (kept multi-shall, reason on the row's rationale):**
- **SR-140** (3 shalls): record / report-drift / refuse-same-commit-stamp are
  one anti-tamper contract whose clauses deliberately fail in different
  directions; splitting mints three rows for one (SN-029, B-02) pair.
- **SR-147** (2 shalls): the single-carrier claim and its converter-proof are
  one contract; the converter is the migration's evidence.

### The shed-clause map (every clause a re-statement dropped, and where it lives)

| Row | Clause shed | Destination | State |
|---|---|---|---|
| SR-017 | module name; legacy `docs/secrets-scan` window read | its LLR chain | **act 3** |
| SR-018 | module name; legacy `docs/privacy-check` window read | its LLR chain | **act 3** |
| SR-019 | OI-24 moment→tier CI clause (ACC) | SR-151 REQ+ACC (test pin included) | **LANDED** |
| SR-021 | SN-013-fold history parenthetical (ACC) | rationale (one line) + git | LANDED |
| SR-026 | retired-serial-loop narration; SR-132 cross-ref; SN-016-fold parenthetical | history (git); backoff/stall obligations KEPT in ACC | LANDED |
| SR-031 | one-home refusal clause (ACC) | SR-137 ACC (verified present, verbatim-close) | LANDED |
| SR-031 | shared-parse mechanism; legacy window read | its LLR chain | **act 3** |
| SR-040 | AGENT_CMD_MAP/--cmd-map mechanism; legacy `docs/review-policy` window; retired run-phase narration | LLR chain; history | **act 3** |
| SR-046 | RUN_CMD-retired narration | history (git) | LANDED |
| SR-049 | Draft/Verified/Modified three-value recognition table; basis-line format | its LLR chain (current recognition set recorded there; D-9 re-labels once) | **act 3** |
| SR-059 | migration-deletion narrative; `docs/run-state` parenthetical; `{phase}-{gate}` branch-name token | history; the branch-name mechanism to its LLR | **act 3** (branch token) |
| SR-070 | three-views enumeration (REQ) | its ACC (verbatim list) | LANDED |
| SR-114 | macOS-exclusion argument (ACC) | rationale (full sentence moved) | LANDED |
| SR-129 | "proven … before the authority flip" (past event) | "provable"; history in git | LANDED |
| SR-141 | whole row (merge) | SR-148 REQ/ACC absorbed all clauses (partition-stability, --explain, rank-table-unchanged, drains-behind-stop, never-past-hold); the stable-partition mechanism itself | **act 3** (LLR under SR-148) |

### SR-141 — the merge forwarding record

SR-141 ("The loop's priority order is stated and pinned", Planned, never
attested) is DELETED, its id spent; SR-148 absorbs the adjudication-first
partition and the never-past-a-human-held-stop guard into its single
ordered-selection shall; `sn_refs` union `["SN-025","SN-029"]`; LLR-159 and
its TC re-grounded on SR-148. Census F5's alternative (explicit partition)
rejected: the partition already existed textually and still produced the
duplicated acceptance.

### SR-150 — the post-census row, dispositioned deliberately

Landed after the census froze (WI-454). Census logic would read
`check_need_form.py` as an internal harness step (DEMOTE), but demoting it
would orphan SN-033 (its only citer), and its requirement subject is already
"The harness" — the SR-149 model form the census holds up. **Classified
HOLD**, `boundary_refs = ["B-05"]`, no text change. Recorded here as the
census's one post-hoc row rather than silently folded; the owner's sitting
can overrule at ratification.

### Riders executed in act 2

- **SR-035 observable minted** (13u rider, candidate as ruled): no
  language-specific token in shipped registries/ID vocabulary; a non-Python
  scaffold passes trace.py unmodified. Verification Analysis → Test.
- **SR-049 `area` minted** (census F7): "Gate harness" — pending the
  Area→aspect conversion (below).
- **B-06/B-07 first SRs** (census F1): SR-151/SR-152, the honest-limit pair
  stated both ways (B-04's note ↔ SR-152's backstop clause).
- **F6 pair kept deliberately**: SR-015 (data invariant) ↔ the checker
  decomposing under SR-157; each rationale names the other.

## Act 3 — the 73 demotions landed (SR→LLR), and the spine closed

**SR 137 → 64.** Every demoted row left the tier under the parent the design
named; the fan-out held exactly as derived: SR-157×15 · SR-158×4 · SR-159×5 ·
SR-006×3 · SR-070×15 · SR-112×1 · SR-153×5 · SR-154×6 · SR-155×10 ·
SR-156×5 · SR-026×1 · SR-030×1 · SR-148×1 · SR-144×1 = 73.

**The finding that matters, recorded as a deliverable (13s): ZERO new LLRs
were needed.** All 73 obligations fit an *existing* component-level carrier —
83 LLRs re-grounded on their new parent, 68 of them taking a `detail`
addendum that folds the obligation tokens the LLR did not already state. That
is the census's "these rows were always LLRs" reading confirmed mechanically
rather than asserted: had the demotion been a re-tier of substance rather than
of altitude, rows would have had no home to land in.

**These counts are RE-DERIVED FROM THE APPLIED DIFF, not from the manifests'
intent** — the first version of this ledger reported the latter and four of
the five figures were wrong. The verdict round caught it (act 4, F4); this is
the corrected set.

| measurement | value |
|---|---|
| LLR rows re-grounded on a new parent (`sr_refs` changed) | **83** |
| LLR rows taking a `detail` addendum | **68** |
| LLR rows flipped `Verified` → `Modified` | **58** |
| TC rows re-pointed (`verifies` changed) | **78** |
| TC `expected` cells rewritten | **42** |
| SR rows deleted (26 tombstones + 73 demotions + the SR-141 merge) | **100** |
| SR rows minted | **15** |
| surviving SR rows whose requirement/acceptance text changed | **25** |

<!-- fig: cmd="python - # tomllib over `git show ad0d0456:<registry>` vs the working tree; count rows whose detail / sr_refs / status / verifies / expected cell differs" rev="act-4 commit tree" -->

- **TC re-points:** 78 test cases moved from the demoted SR to its parent
  (LLR refs kept); 42 `expected` cells that read *"Satisfies SR-NNN
  AcceptanceCriteria"* were rewritten to name the parent and the LLR that now
  carries the acceptance — a dangling "satisfies" pointer is exactly the
  silent-rot class this campaign exists to remove.
- **Status movement:** the 58 re-parented LLRs that were `Verified` flip
  `Modified` (the sanctioned amend-and-flip; `modified` 65 → 102). Nothing
  self-ratifies.
- **SR-035's chain minted** (its Analysis→Test flip's debt): **LLR-171 +
  TC-165**, both `Draft`; watermark TC 164 → 165.
- **`orphans=0 integrity=0`** — SN=27 · SR=64 · LLR=153 · TC=148. The spine
  is fully joined, both directions, for the first time in the campaign; the
  bottom-up sweep the method asks for found nothing dangling because the
  top-down pass closed it.
  <!-- fig: cmd="python project-trajectory/scripts/trace.py --strict # SN=27 SR=64 LLR=153 TC=148 orphans=0 integrity=0 form-findings=2" rev="act-3 commit tree" -->
- **Form findings 9 → 2** — exactly the two recorded 13v waivers (SR-140,
  SR-147). Every other multi-shall row dissolved on landing at the tier where
  its detail belongs, which is the form rule's own prediction.
- **Boundary-Refs coverage advisory: 0 uncovered of 64** (was 149 of 149 at
  slice start). Sitting-3 decision 8's deferral condition — *"until slice 2
  populates Boundary-Refs"* — is now MET on the SR side.

### Riders executed in act 3

- **SR-126's script-name carve-out NARROWED** (13u rider): from any `.py` to
  exactly the ten declared external-port scripts (check, bootstrap,
  agent_loop, check_vendored, gen_cases, gen_release_checklist,
  subagent_gate, run_menu, integrate, trunk_step) — the sitting-2
  port/internal discriminator applied. TC-126's fixture set narrows with it
  (noted for the implementation touch).
- **SR-060's dead `docs/next-wi` clause STRUCK** (sitting-2 §6 item 7); its
  live obligations (claim-cut binding, root-truth no-writes, trailer evidence
  channel) fold into LLR-061.
- **MW scrub-or-keep calls, each on mechanical evidence, none silent:**
  SR-067's window KEPT (`check_trajectory.py` still reads legacy
  `docs/trajectory-check`), SR-042's KEPT (`gen_okf.py` still reads the legacy
  `docs/okf-export` sentinel), SR-131's pause window CLOSED and scrubbed,
  LLR-140's `docs/review-policy` read KEPT.
- **D8 dependencies recorded, not silently retired:** LLR-023/LLR-080 (arch-map
  halves) and LLR-013 (Runtime-flows input) each state that their target
  surface is ruled to retire and the obligation moves with the flows/dashboard
  rendering.
- **B03 reframing** on the dashboard/status render rows: the generated views
  are adopted-toolkit outputs (REL-002), not system outputs — framing fixed,
  every render obligation kept.
- **F6 pair closed as designed:** LLR-005 now names itself the checker half
  paired with SR-015's data invariant.
- **Live-surface re-points** (mechanical, successor-named): 15 kit scripts'
  prose comments, 4 IF `sr_refs` arrays, and the `check_need_form`/`gen_cases`
  example ids moved to surviving rows. One test fixture followed the registry:
  `test_dogfood_sync`'s planted-defect header (SR-001 → SR-006).

## Act 4 — the verdict round's first finding, fixed: 111 dangling WI back-refs

**Found by the adversarial round, not by the author.** Deleting 100 SR rows
(26 tombstones + 73 demotions + the SR-141 merge) left **111 `sr_refs`
entries across 81 work-item specs** pointing at ids that no longer resolve —
`check_trajectory` reported each as *"references SR-NNN (not in the SR
registry; draft?)"*, a misdiagnosis that would have read as noise forever.
Act 3's applier had swept `queued/active/draft/deferred` (which held none)
and never touched `complete/` and `cancelled/`, which held all 111.

**Why re-pointing is right, and not a falsification of history.** Measured:
the base tree carried **ZERO** dangling WI `sr_refs` even though SR-039 was
deleted under this same doctrine on 2026-08-11 — so resolvable back-refs are
this repo's standing state, not an accident. And the tombstones' own text
ordered exactly this: *"active requirements, **implementation links, and
decomposition evidence** shall cite the replacement rows."* A closed WI's
`sr_refs` is an implementation link. The prose mentions of spent ids inside
those same specs' bodies are left untouched — those are history, and D-4
does not rewrite history.

**The fix** chases each dead id through the forwarding map and then through
the demote map (several tombstone successors were themselves demoted in act
3 — e.g. `SR-037 → SR-067/068/069 → SR-157`), deduping the result: 81 specs
re-pointed, **0 dangling, 0 unresolved**, and the whole WARN class cleared.
<!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --strict --root . # 0 lines matching 'not in the SR registry'; clean (452 work items, graph acyclic)" rev="act-4 commit tree" -->

### Act 4's verdict round — CHANGES-REQUESTED, 5 findings, all fixed

Full record: [../reviews/wi451-slice2/round1-terra.md](../reviews/wi451-slice2/round1-terra.md).
All five confirmed on re-verification, none refuted. Four were **invisible to
the commit bar the author ran** — the arch-map destruction (1,413 generated
lines, from invoking the generator with default args instead of the declared
`--src`), a stale `SupersededBy` test assertion, a child/parent phase break,
and false signed counts in this very ledger. The fifth was a rider claimed as
executed but not executed (SR-060's dead `next-wi` clause).

**The process failure, stated plainly:** only the **smoke** tier was run, and
the protocol requires the **full unfiltered suite** before claiming a slice
done. Smoke was green through every one of those failures. After the fixes:
`pytest -q -n auto` → **2489 passed, 11 skipped**.

**One systemic issue the round's F2 uncovered**, larger than the finding: the
demotions re-parented phase-1 children onto phase-5 mints, taking child/parent
phase mismatches from **19 (base) to 144**. Each new parent now takes the phase
its decomposed work actually shipped in; mismatches stand at **38** — still
above base, and carried below as owed rather than declared clean.

### Still OWED inside this slice (the open lane's remainder)

1. ~~The Area→aspect conversion~~ — **DONE in act 5** (owner ruling
   `2026-08-14h`): `Area` retired for the closed `Aspect` vocabulary, the
   derivable values DROPPED per decision 10 rather than remapped (21 of 64 rows
   keep an aspect, 42 carry none — the ruled end state). Vocabulary now
   enforced in `ENUM_FIELDS`; adopters carry a `RESYNC_PACK` entry.
2. **SR-043's MW clause** (a HOLD row not re-worded in act 2): scrub-or-keep
   call still owed.
3. **The re-iteration pass the method names** has run once in each direction
   and closed the orphan set; a *second* top-down read of the 64-row layer
   against the six crossings — now that the layer exists to read — is the
   honest remaining check before the owner's sitting.
4. **The residual child/parent phase spread: 38, against a base of 19.** The
   19 pre-existing are tolerated by the registry's own convention; the ~19 this
   campaign added sit on rows whose parent legitimately spans phases. Either
   reconcile them or record the spread as intended — do not leave it as an
   unexplained delta.
5. **What slice 2 does NOT do:** the D-9/D12 vocabulary migration
   (`2026-08-14e` — one atomic act after these drafts land) and any
   ratification (every status movement above is into in-process states).
