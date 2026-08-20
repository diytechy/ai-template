# The consolidated iterate worklist (Opus round + Sol round, deduped)

Execute in c:\Projects\ai-template as ONE coherent working-tree state.
Worker rules + SHARED POST-SIGN CONTEXT apply (foreground only; no
commits; ruff format last; full real output in the report). The two
review rounds are docs/reviews/2026-08-20-batch-close/ROUND-SOL-RAW.md
and (being written) ROUND-OPUS.md — consult them for the exact evidence
lines. Items are grouped; each names its source finding.

## GROUP 1 — the approval-record floor becomes load-bearing (the CRITICALs)

1a (Opus-1). Replace the grep-based arming test
(tests/test_baseline_snapshot.py:536) with a REAL subprocess pin: over a
seeded scaffold, delete an Approved row from the snapshot copy and assert
`trace.py --strict-integrity` returncode == 1 and the finding lands in
integrity (the same shape as test_an_unresolved_allow_entry_reds_...).
Then re-run Opus-1's exact mutant (route snapshot findings under
strict_schema) and prove the new test goes RED against it. Keep any grep
halves only as secondary.

1b (Opus-2/Sol-1). Authority-gate the non-seed snapshot write:
`baseline_snapshot.copy_live(seed=False)` (via intake snapshot) REFUSES
when the copy would absorb a RATIFIED-cell difference (use
split_changed_cells' ratified half against the current snapshot) UNLESS
the same working tree also moves >=1 Status cell in that registry
(amend+flip= ratification) OR an explicit `--approves <ref>` argument is
given, in which case the ref is recorded into the snapshot README stamp.
TRACED-cell-only refreshes stay legal with no flag (the WI-482/452 class,
verified clean by the review). Tests: all three paths + the laundering
scenario from Opus-2 now REFUSES at commit B.

1c (Opus-3/Sol-2). Whole-tree mirror arm: extend the always-on integrity
pipe with a committed-state comparison — every file under
docs/archive/last_approved byte-compared to its live counterpart — so a
LANDED divergence reds every subsequent strict-integrity run, not just
the staged one. (The refresh path from 1b keeps this green in normal
operation.) Test: commit a hand-edited snapshot in a scaffold clone →
next strict-integrity run exit 1.

1d (Opus-4). `trace.py:2795-2799`: reword the brief's stamp line to what
stamp() actually is ("the commit that last wrote this record") AND add
beside it the last commit that moved a Status cell in a snapshotted
registry (derive via git log -S or the pickaxe over `status = "`), which
is the approval provenance the owner needs.

1e (Opus-11). ratify_check: exclude the derived stamp line from the
freshness comparison so the brief reds only when row CONTENT it renders
moved. Test: a snapshot-README-only change leaves ratify-fresh green.

## GROUP 2 — the OI-41 arms harden (Opus 5/6/7, Sol 3)

2a. Vacuity/parse honesty (Opus-6): parse_provenance_allow counts
DECLARING non-comment lines; parsed < declared is an integrity finding
naming the first unparsed line (kills the `--` silencing). Replace
gen_open_items.py:965's hardcoded all-clear literal with the measured
counts (entries parsed, fragments declaring). Registry-absent no longer
disarms silently: absent registry + >=1 allow entry = a finding.
2b. ARM-1 wording (Opus-5): the enforcement is present+resolves BY
RECORDED DESIGN (state is ARM 3's) — fix the three overclaiming surfaces
(the WI-485 Deliverable in docs/work/complete/, enforcement-audit.md:42's
row wording, and any commit-title-derived prose in the fragment) to say
"resolves to a row" honestly. Do NOT state-gate ARM 1.
2c. ARM-2 scope (Opus-7): a `Deferred open items:` declaration in a
multi-section fragment speaks only for content ABOVE the next `### `
heading (or: require one declaration per fragment FILE and define the
fragment as one session's record — pick the cheaper rule, state it in the
checker's docstring, and make the grind fragment conform by adding the
per-section declarations it now needs: the orchestrator will hand you the
two new OI ids minted for the announced-but-rowless decisions — leave
`OI-45`/`OI-46` placeholders where the fragment declares them).

## GROUP 3 — false or stale records trued up (Opus 8/9/18/19, Sol 4/7)

3a. WI-466's completed spec (Opus-18/Sol-4): append a dated CORRECTION
paragraph inside its Deliverable stating the golden claim was wrong, what
actually happened (red at 8d7ff553, repaired 74c20704), and that the
lesson is recorded in the grind fragment. Never delete the original text
— strike it honestly ("CORRECTION (2026-08-20): ...").
3b. WI-481's overclaim (Opus-8): in its completed spec Deliverable and
the grind fragment entry, correct "stops being vacuous" to the honest
form ("the SKIP names what is missing; the gate still cannot fail while
all rows sit at Gate=warn and no emitter is wired — both deliberate,
recorded postures"). Also fix Opus-19: trace.py:2005-2010 and
tests/test_trace.py:1259-1262 still use performance-budgets.csv as the
worked ABSENT example — re-point both to a path that is genuinely absent
(check docs/declared-absences for a real one).
3c. Figures (Opus-9): add `fig-ok` exemptions to WI-481's two spec prose
lines; add a dated note to the grind fragment stating that the seven
worker-reported full-suite figures are worker self-reports whose
provenance is the workers' session transcripts (honest label, not
retroactive markers); WI-452's converter-run claim gets the same honest
label in its completed spec.
3d. Vocabulary contract test (Opus-15/Sol-7): add the two planted-case
channels where cheap (a prose-sentence scan for retired STATUS words in
instructing sentences is allowed to be narrow — e.g. flag `Modified`
adjacent to `Status`/`reads`/`set` within a line on the instructing
surfaces; keep historical/example exclusions tight), fix the
true-by-construction assertion at :108, make the :164 exemption
token-scoped, and re-word WI-477's "cannot re-accrete" claim in its
Deliverable to the covered channels.

## GROUP 4 — mechanical closures

4a (Opus-12). intake.py:1684-1700: delete the unreachable post-raise
statements and dead write loops; re-point the source-string test at
_cmd_snapshot's live path.
4b (Sol-5). LLR-015: re-point code_symbol to `analyze` (the enclosing
module-level def) or the Findings field name that module_bindings
resolves — verify with check_doc_refs before/after; LLR-172: module cell
→ check_trajectory.py (where component_findings is module-level).
Traced-cell edits + snapshot refresh (legal under 1b's gate).
4c (Sol-6). derive_gate: UNKNOWN spine statuses fail closed (BAR_BELOW)
— keep the documented transitional 'modified'→approved read exactly as
is; the typo hole closes, the migration tolerance stays. Update the
pinning test to cover both: 'modified' → Release bar (transitional,
documented), 'Approvd' → BAR_BELOW.
4d (Opus-16). Re-measure the smoke tier twice warm and re-stamp
CLAUDE.md's "~17.6 s" figure honestly with the current machine-condition
figure + date; if the second warm run exceeds 60s, say so beside the
declared budget rather than adjusting the budget (the budget re-derivation
is banked as its own item).
4e (Opus-17). WI-465's remainder: pin the 12 remaining unpinned git-init
sites via conftest.pin_autocrlf (the census correction: 30 files, not
28), and append the corrected census to WI-465's completed Deliverable as
a dated correction.
4f (Sol-15). Add the missing assertion: bootstrap/scaffold test asserts
gitattributes carries `* text=auto eol=lf`.
4g (Opus-13). Comment beside SNAPSHOTTED stating the IF/CMP tiers'
comparison is vacuous while every row reads Drafted (protection begins at
their first approval).
4h (Opus-14). tests/test_trace.py:1878: pytest.skip("no declaring lines")
when the allow file declares nothing, so zero-population vacuity is
visible in the run.
4i (Sol-10). Add the WI-479 behavioral regression: an overlong active WI
title must emit the native details/summary disclosure markup (assert the
elements, not just the class).
4j (Opus-20). Backlink scanner truths: update the three hand-carried
1/161 figures to the live number (re-measure it); fix
process.toml.template's false "WARNS at a plain run" sentence; add the
missing check.py wiring test (the step exists at DevStg-Tests+ with
--strict-backlinks); note the position-restriction caveat (string
literals count as coverage — false PASSES only) beside the dial where the
number is read. Grammar hardening itself rides WI-487.

## OUT OF SCOPE (banked, do not touch)
IF-registry staleness cluster (11 stale CMP notes, IF-103 one-shot,
IF-117 contract) — the wi455 lane's; LLR-168/TC-162 audit expansion — a
spine amendment batch of its own; _title_clause + graph fonts — own WIs;
the smoke-budget re-derivation — own WI; hook strict promotion (Opus-10)
— DECLINED with reasons recorded by the orchestrator (the warn-first
floor is a ruled design; the class closes as the bar rises).
