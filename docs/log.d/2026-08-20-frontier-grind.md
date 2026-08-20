## 2026-08-20 — The frontier grind, in series (owner directive): per-WI record

The owner's 2026-08-20 directive: grind the open frontier in series with
opus/sonnet workers, one large adversarial review (internal Opus +
cross-family Sol via codex) at the end, consolidated and iterated in one
action. One entry per WI as it closes; adjacent findings accumulate at the
bottom for the closing review.

### WI-474 — the hats→spine_carrier seam (opus worker) — CLOSED complete

IF-133 minted (carrier-consumption shape per IF-118/119/120/122; owner
LLR-166, carried_by IF-102, req_refs SR-147, CMP-008, Drafted); two
consumer-side contract tests added and driven negative; `Contracts: IF-133`
docstring line; watermark IF 132→133; snapshot re-taken byte-identical.
`check_trajectory --strict` EXITS 0 — the first all-green strict trajectory
run on record. Worker's full suite: 2592 passed / 13 skipped in 492.66s
(one environmental posix-shell gate re-run gated).
<!-- fig: cmd="python -m pytest -q -n auto" rev=6a6d866d -->

### WI-476 — harness hygiene batch (sonnet worker) — CLOSED complete

`ruff check .` ALL CHECKS PASSED (was 6 errors; the trace.py dead unpacking
deleted with its ratchet entry re-stamped DOWN); the duplicate
`"bootstrap.py"` baseline entry merged (effective bound preserved) and the
baseline made duplicate-key-PROOF via an AST parse of the file's own source;
the nested smoke-budget child runs forced-UTF8 with a planted cp1252-byte
regression test; the gen_trajectory panel assert is an explicit raise with a
test. Touched modules 98 passed; smoke 1209/5 (two new tests joined the
tier). The worker's final report arrived AFTER the close (it had stalled on
its own background full run; the work was verified from the diff first) and
confirms: full unfiltered suite 2596 passed / 13 skipped in 453.88s; the
M-01 crash was REPRODUCED live before fixing (the cp1252 em dash killing
subprocess's reader thread); the spec's "malformed noqa" finding no longer
existed on the moved tree — the real sixth was a second F841. Two declared
deviations, both accepted: M-05 deliberately narrowed to the duplicate
merge + AST guard (stripping ~1,700 lines of per-entry history judged
disproportionate for a quick batch — if wanted it is its own WI), and no
RESYNC entry (no adopter-facing behavior moved).
<!-- fig: cmd="python -m pytest -q -n auto" rev=34a42f7e -->

### WI-475 — launcher interpreter selection (opus worker) — CLOSED complete

One selection policy in every probing launcher (.venv first, runnability
then version probe, refusal NAMES every rejected candidate), the `.command`
wrapper documented as the honest inherited exception, `call`-prefixed cmd
invocations (the shim trap: the old launcher exited 0 having run nothing),
and 27 executable selection tests replacing text inspection. Two live bugs
found by execution: PowerShell's empty-string argument drop and 7.4+'s
Stop-preference native-exit behavior. Scaffold-verified; RESYNC entry.
Worker full suite 2621/13 green.
<!-- fig: cmd="python -m pytest -q -n auto" rev=27a65c19 -->

### WI-478 — Contracts marker-line grammar (sonnet worker) — CLOSED complete

Marker-line-only grammar with `ContractsGrammarError` on an ambiguous
continuation (the alternative rejected on measurement: eight modules
legitimately re-mention foreign IF ids in flush-left prose); dispatch.py's
wrap fixed; the two false undeclared warnings gone, proven by a
before/after strict diff whose only delta is those two lines; two
regression tests. 117 arch/dispatch tests + smoke 1209/5 green.

### WI-482 — the three stale anchors (sonnet worker) — CLOSED complete

LLR-087/088 re-pointed to `traj_render._drill_layer_svg/_render_drill` and
`DRILL_SCRIPT` (module cells corrected; each target READ before citing),
LLR-112 to `gen_trajectory.HTML_TEMPLATE`; traced-cell moves only, snapshot
refreshed byte-identical, `check_doc_refs` clean on all three ids,
integrity 0, smoke 1209/5. The planned-symbol declared form deferred behind
WI-472's obligation SR, with reasoning on the row.

### WI-466 — the verified-triple display fix (sonnet worker) — CLOSED complete

The summary guard widened to any-leg-nonzero (was demonstrated-or-attested
only, hiding the common mechanized-only shape); regression test added;
goldens verified unaffected; ratchet re-stamped 4510→4515 with reason. The
attested-vs-mechanized split is visible again on the repo's own run
(69/3/0). test_trace.py 82 passed; smoke 1209/5.

### WI-480 — dev-toolchain currency (sonnet worker) — CLOSED complete

pytest moved to `>=9.0.3,<10` after a throwaway-venv full-suite
qualification produced the identical pass/fail set as 8.4.2 (the shared
two failures were WI-466's golden gap — see below); weekly `pip-audit` SCA
workflow (verified catching then clearing the pytest advisory);
`uv`-generated hash-pinned locks for both Pythons with a loud staleness
check instead of auto-commit (refused under push=human, reasoning in the
workflow); pip-audit + uv ledgered in docs/dependencies.md.

Post-close confirmation from the worker's finishing run: the FULL suite is
fully green under pytest 9.1.1 with the golden fix in — 2626 passed / 13
skipped in 483.65s, exit 0 — and the committed content matches the
worker's authored files byte-for-byte.
<!-- fig: cmd="python -m pytest -q -n auto" rev=94489f7a -->

**The golden episode, recorded for the closing review:** WI-466's widened
guard added the triple line to mechanized-only output; the clean/orphan
goldens (slow-tiered, invisible to the commit-bar smoke) went red at
8d7ff553 and stayed red for one commit until WI-480's qualification run
surfaced them — regenerated deliberately at 74c20704. Two lessons: a
smoke-invisible module can carry a red across a close, and a worker's
"goldens verified unaffected" claim was wrong where the orchestrator's
verification (smoke only) could not catch it.

### WI-481 — live performance budgets (sonnet worker) — CLOSED complete

Four PB rows seeded with warm-run measured bases + fig: markers (trace
0.97s/5s, regen pair 6.46s/20s, check_docs 1.94s/8s, whole hook 7.7s/30s),
declared-absence line retired with its three readers checked, PB watermark
0→4. check_perf moved from vacuous OK to an honest 4-budgets SKIP naming
the unwired metrics emitter — that emitter is the named residue for a
future WI.

### WI-485 — OI-41's three arms + always-on (opus worker) — CLOSED complete

All four pieces live: the allow-file OI-### grammar (hard, integrity floor,
17 entries migrated), the fragment deferral declaration (warn, none-forms
accepted, weakness pinned), the re-aimed vacuity check (names the entries),
and the always-on layer move (+987B PROCESS.md flagged; S-3 non-vacuous;
scaffold-verified across profiles; RESYNC ×2). Full suite 2635/13. **The
vacuity arm fired truthfully on day one**: 16 OI-34 entries + 1 OI-37 entry
whose ruled executions never landed — exactly OI-41's founding class —
now queued as **WI-489** (the OI-34 label migration, minted in this close;
watermark WI 488→489). ARM 1's state-gating deliberately narrowed to
present+resolves with the count left to ARM 3 (every live row is `ruled`;
reasoning in the Deliverable).

Deferred open items: none — WI-489 executes an ALREADY-ruled item; no new
owner decision was deferred by this session.

### WI-486 — harvester + reverse-coverage scanner (opus worker) — CLOSED complete

The fabricating harvester is dead: literal `Implements:` only, ONE shared
grammar with the reverse scanner, the map column 50/62 → 2/4 (the honest
state, pinned on the column). Coverage measured 1/161 (0.6%), report-only
at the shipped 0 dial, 50% = WI-487's target; guides re-worded onto the
dial (AGENTS −5B under cap; PROCESS +470B flagged); audit row corrected;
RESYNC ×2. The scanner's SR/LLR/TC mint deferred to the owner (WI-487's
outcome shapes it; every tier human-held). Full suite 2643/13. Worker
flagged its own transient `git stash`/pop incident, verified recovered.

**Orchestrator's own close-ritual defect, fixed in this close:** nine of
the day's terminal specs still carried `specref` (R-F: a terminal WI's
SpecRef is EMPTY — learned at WI-464, not applied to the grind closes
until WI-486's worker surfaced the nine strict errors). All nine stripped;
strict back to ZERO errors. The worker's companion claim that
LLR-015/LLR-172's symbols "no longer exist in trace.py" REFUTES on grep
(12–13 occurrences each) — banked for the closing review with the
check_doc_refs --strict 54-dangling figure it rode in on.

### WI-470 — open-items A3 coverage (sonnet worker) — CLOSED complete

The A3 closure reaches gen_open_items via two regression tests (the source
idioms were already right — the closure gained teeth, not changes); the
process-flow now-marker gains a worded cue in the proven 6:1 accent-text
idiom after the badge form MEASURED 2.98:1 dark and was rejected; the hero
meters carry aria-label identities. Three tests; smoke green.

### WI-465 — autocrlf fixture sweep (sonnet worker) — CLOSED complete

Census re-measured (28 files / 43 sites; 5 bootstrap-immune), the spec's
`.gitattributes` remedy REVERSED with reasoning (unconditional LF
normalization relocates the bug), one shared conftest.pin_autocrlf helper,
23 files swept, five clones reconciled, zero assertions changed. Full
suite 2647/13.

### WI-452 — resync helper surfacing (sonnet worker) — CLOSED complete

The three surfaces verified correct as-is (the pack names the converter +
contract; the other two defer under OI-27's one-home rule); the converter
RUN live against a rebuilt pre-cutover scaffold (round-trip clean);
TC-160's dead evidence pointer repaired to the four covering tests
(traced cell, snapshot mirrored); no orchestration built. 174 targeted
tests green.

### WI-489 — the OI-34 label migration (opus worker) — CLOSED complete
### · post-sign amendment batch #1, the record

17 SR rationale cells amended in one reviewed state (population
re-measured 17: 16 dated markers + SR-053's signed variant; SR-040 left
with OI-38's strike). Thirteen were pure marker removals; four carried
prose repairs, before/after quoted in the worker report and compressed
here: SR-033 "the earlier label read as though it did" → "the derivation
stated here must not be read as though it did"; SR-052 "narrower than the
label suggests" → "narrower than the unmeasurable-clauses opening
suggests"; SR-175's "labelled so the deriving lens is reviewable" → the
lens-derivation stated without the label claim; SR-043's OPEN QUESTION FOR
THE SITTING paragraph retired per OI-37's own ruling with the standing
fail-open reason in its place (requirement/acceptance untouched — the
ruling relaxed the NEED, not the behavior). All 17 allow entries retired
with records; snapshot byte-identical; vacuity 2→0; the anti-vacuity test
guard strengthened to one-key-per-line (valid at zero). Full suite
2647/13.

### WI-477 — the one-contract docs sweep (opus worker) — CLOSED complete

The taught schema re-verified against the LIVE constants before sweeping
(the words had moved again at the signing), then swept across every
checklist surface + two live retired-value claims the review missed, and
PINNED: a mutation-verified contract test reads the enforcement constants
so the class cannot re-accrete. Three-category frame inventory; the ledger
restated with derive-from-rows DECLINED on evidence; the gate honestly
renamed with corruption-vs-absence tests; status.md to exactly 120 by
relocation not deletion. Full suite 2657/13. The worker caught its own
CRLF introduction via the rule it had just relocated.

### WI-479 — dashboard title defense (sonnet worker) — CLOSED complete

The hero routes through the existing Next-work disclosure (2,253 chars →
187 rendered, verified on the live WI-455 title), the grid aligns start,
and a one-line warn-only title advisory lands (12 open titles named, none
reworded). Screenshot-verified 390/1280/1680 + 320px reflow + keyboard.
Full suite 2660/13. **The one red it surfaced was the orchestrator's:**
the WI-477 close left "by WI-477" in status.md's hand prose — R-D fired
exactly as restored (WI-200), fixed at this close by dating the reference
instead of naming the id. Lesson: a close that ADDS a WI id to status
prose plants a delayed R-D red for its own close.

### Adjacent findings accumulating for the closing review

- (WI-479 worker) `_title_clause` splits at the first dash — WI-455's
  disclosed clause ends mid-quotation with no cue; pre-existing shared
  property (Next-work card too), now more visible. A smarter boundary
  heuristic is its own small review.
- (WI-479 worker) the 10px/8.5px fixed graph label sizes are a real
  legibility concern whose fix risks the text-fitting math in both
  icicle and DAG views — own WI (font bump vs a co-equal table view).
- (WI-477 worker) LLR-172's `module` cell anchors `component_findings` to
  trace.py while the def lives at check_trajectory.py:1489 (the trace.py
  occurrences are the Findings-field extension point) — WI-484's execution
  settles which is the intended landing; check_doc_refs warns meanwhile.
- (WI-477 worker) smoke wall-clock volatile on this box (53.8–113.9s over
  four runs of a tier that moved by ten cheap tests) against the
  CI-enforced 60s — the budget-vs-box question deserves its own look.
- (WI-489 worker) PROCESS.md ~:79-81 + spine-authoring SKILL still mandate
  "a labelled derived SR" — not violated today (the Hat-derived prose
  satisfies the naming half) but the vocabulary retires WITH WI-484's
  field, owing a RESYNC entry then.
- (WI-489 worker) two shipped docstrings (trace_text.is_allowed,
  trace.load_provenance_allow) still use the retired parenthetical as
  their worked example — true as history, misleading to grep.
- (WI-489 worker) OI-37 left two sub-questions unruled with no rows (the
  unparseable-process.toml gate-OFF asymmetry in subagent_gate vs its two
  twins; the unread fail-open log) — recorded in the allow-file retirement
  note so they cannot vanish.

- (WI-452 worker) IF-103's Contract and the kit README still frame
  `migrate_carrier.py` as "ONE-SHOT ... retirable" — in tension with the
  ruling that made it a live resync helper with no terminus. IF-103 is
  Drafted; cheap fix for the wi455 lane or the closing review.
- (WI-465 worker) Five test files rely on bootstrap's `.gitattributes` for
  CRLF-safety with NOTHING pinning that invariant — a change to
  gitattributes.template or make_minimal_project's write order silently
  reopens the hole in five files. Worth a defensive assertion.

- (WI-475 worker) `run.template.{sh,cmd}` carry the IDENTICAL pre-WI-475
  runnability-only pattern — same defect class, product-launcher surface,
  worth its own WI.
- (WI-475 worker) the smoke tier measures ~56s against the declared 60s
  budget on this box — the stamp's headroom is gone; and smoke membership
  is 1214/1216 — the next new smoke module trips the membership ratchet.

- (WI-474 worker) `check_vocab.py:71` declares `Contracts: IF-118`, which is
  NOT its row (IF-118 is gen_open_items→spine_carrier) — and the checker
  verifies only that a cited id EXISTS, never that the row names the citing
  module: a `Contracts:` line can cite any live IF id and be believed. Real
  checker hole.
- (WI-474 worker) LLR-168's detail/code_symbol omit hats.py's entire `audit`
  subcommand (~170 lines incl. the newly declared seam) — Approved row, so
  the coverage amendment is owner-adjacent.
- (WI-474 worker) IF-118/119/120 `notes` cite a retired CMP numbering
  ("this module is CMP-002...") — stale, reads authoritative.
- (step-7 worker) `intake._apply_flips` now writes nothing — whether any
  mechanical ratification authority returns is an owner policy call
  (docstring carries both candidates).
