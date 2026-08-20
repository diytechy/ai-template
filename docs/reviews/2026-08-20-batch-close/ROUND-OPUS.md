# Internal adversarial round — the 2026-08-20 batch (Opus, in-harness)

Range `28466711..46616726` (the review triage → the WI-472 mint), run
read-only with mutations executed in private clones; dispatched by the
orchestrating session under the owner's one-large-review directive, same
brief as the cross-family Sol round (ROUND-SOL-RAW.md beside this file).
Verdict shape: 2 CRITICAL · 9 MAJOR · 9 MINOR, every banked adjacent
finding dispositioned, three hardest-refute claims held.

**The through-line (the reviewer's own words):** "The signing itself is
the most honest artifact I have audited in this repo — exact, scoped, and
disclosed. The mechanism built to protect that signing is not yet
load-bearing: its arming is guarded by a grep (1), its writer has no
authority check (2), its invariant expires at commit (3), and its own
brief mislabels a refresh as an approval (4). Those four compose into one
working laundering path that was exercised, benignly and with owner-ruled
content, seventeen times on the same day the mechanism armed."

## CRITICAL
1. The step-7/8 arming test is a source grep; a plausible routing refactor
   (executed twice) disarms the approval-record floor with the whole suite
   green (tests/test_baseline_snapshot.py:536; trace.py:4607).
2. `intake.py snapshot` re-blesses arbitrary text with no authority check
   — the two-commit laundering path executed end-to-end reaches
   strict-integrity exit 0 with a rewritten Approved requirement; the
   day's WI-489 (17 ratified-cell amendments, owner-ruled content)
   exercised the same path benignly.

## MAJOR (compressed; the dispatch record carries each disposition)
3. The mirror invariant is staged-only — a landed divergence is silent
   forever (check_trajectory.py:3476).
4. The ratify brief renders any snapshot write as "the reviewed commit
   that last moved an approval" (trace.py:2795; at HEAD it names c5e19720,
   which moved zero approvals).
5. OI-41 ARM 1 enforces present+resolves while three surfaces claim
   state-gating (trace.py:1698; the weakness is pinned by a test).
6. The vacuity arm silences via one pending row, an absent registry, or a
   separator typo — and then prints a hardcoded all-clear literal
   (gen_open_items.py:886/:965).
7. OI-41's founding class reproduced at HEAD on arming day: three
   announced owner decisions with no rows, all arms green (the
   _apply_flips authority call; OI-37's two residues).
8. "The perf gate stops being vacuous" is refuted: all four PB rows warn,
   SKIP returns exit 0, the step is dormant at the repo's gate — the
   MESSAGE stopped being vacuous, not the gate (check_perf.py:354).
9. Seven of eleven full-suite figures in the grind fragment are
   unprovenanced worker self-reports; WI-452's converter-run claim has no
   artifact; check_figures went 16→18 and is dormant.
10. Seventeen of twenty-six harness steps are dormant at the derived gate;
    the R-D/R-F catches came from hand-run strict — the class stays open
    by design of the warn-first floor (disposition: declined, reasons
    recorded).
11. ratify-fresh is red on a clean checkout via the stamp line alone — a
    guard that fires on every commit is learned as noise.

## MINOR (compressed)
12. intake.py:1684-1700 unreachable post-raise code; a test pins a guard
    on the dead path via source-string grep.
13. 130 of 534 snapshotted rows (all IF/CMP, all Drafted) are compared by
    no rule — the off-spine protection is currently zero.
14. The strengthened allow-list test is vacuous at zero population.
15. The status-vocabulary contract test covers the assignment channel
    only; a prose-instruction sentence passes; two internal weaknesses.
16. CLAUDE.md's "~17.6 s" smoke figure is stale (95.8 s measured under
    load at HEAD; 53–58 s typical warm).
17. WI-465's census does not reproduce: 30 git-initing files (not 28) and
    12 unpinned sites remain; the helper and zero-assertion claims verify.
18. WI-466's completed Deliverable still carries the refuted golden claim
    (the fragment corrected the record; the spec did not).
19. WI-481 left two readers using its now-present CSV as the worked
    ABSENT example (trace.py:2005; tests/test_trace.py:1259).
20. The backlink scanner counts string literals and negated examples as
    coverage (false PASSES only); 1/161 is stale in three hand-carried
    places; a template sentence is false; the check.py wiring is unpinned.

## Hardest-refute (held)
1. The signing commit: 243 flips exact, nothing rode along, the two
   declared non-status edits are the only ones, seven registries
   byte-identical at the commit.
2. WI-472's spine: the shall genuinely language-agnostic; all 12 TC-175
   evidence nodes collect and map to the Method with no gap either way.
3. The mutation-verified pins are real: 23 of 25 independent mutations
   went red (the two escapes are findings 1 and 14); no ratchet bound was
   quietly raised anywhere in the range.
