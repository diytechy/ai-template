## 2026-11-24 — WI-1072: only the composer's own judged-text identity lines reach a sitting's binding

Built on `maint/wi-1072` (cut from `refactor_again` at `c31642461`) under the
plan `docs/plans/WI-1072/plan.md`, which the coordinator approved on
2026-11-24 before any build, D1 to D10 confirmed (D1 with the refusal naming
where the line sits; D6 on a condition the build read from the code). The
spec's Deliverable holds the per-item record, the red-first lines and the
acts owed.

- **What changed.** A composed adjudication brief, of any kind, whose text
  holds a line shaped as a judged-text identity line that its composer did
  not write (in a shown row's cell, a later section of a combined sitting, a
  spec's context, a template) is refused at composition, naming the row the
  line names, its line, the row whose text holds it and the heading above it;
  so is a brief whose identity block ends its text. Measured at the base: in
  an amendment brief such a line added an identity for a row not shown; in a
  first-acceptance brief it added identities where none belong; in a
  combined sitting a later section replaced the amendment section's genuine
  digest. No registry cell, spec or stored brief here held one.
- **D6.** Text appended to a composed brief before the coordinator's command
  binds it (a disposition's `## Owner route` section, the arms map) carries
  spec and row text no kit code composes, so reservation checks the brief it
  binds: it takes only one block of distinct rows, none for a brief
  requesting no amendment, and otherwise refuses before launch naming each
  line, writing no binding.
- **Rows.** Amended, text only, owed to a sitting: LLR-359 (Detail,
  Rationale), TC-398 (Method, Expected). No id minted.
- **Deviations from the plan:** the D6 extension (reservation's check,
  `coordinator_adjudicate.py` and its IF-284 exit list) and the end-of-text
  refusal, with four tests beyond the plan's table; LLR-359's rationale
  avoids `such as` (a `trace.py --strict` form finding);
  `adjudicate_brief.py` 782 -> 868 SLOC. The Deliverable holds each, with its
  reason.
- **Byte deltas on budgeted files:** none (no budgeted file touched).
- **Tests:** red first `23 failed, 3 passed in 4.27s` (the 3: the clean
  controls); after the code `26 passed in 4.22s`; the 40 importer and named
  modules `53 failed, 2171 passed, 17 skipped in 501.92s`, all 53 in five
  git-heavy modules failing to read a fixture's recorded copy past Windows'
  path limit under a long `--basetemp`, and those five rerun under a short
  one `303 passed in 1308.20s`; `trace.py --strict` and
  `check_trajectory.py --strict` clean; `run_menu.py smoke` exit 0, the
  smoke tier `3981 passed, 3 skipped, 18 warnings in 310.72s` (CPU 905.1 s
  over 540, reported only). The unfiltered suite is the coordinator's,
  before the merge.

<!-- fig: cmd="python -m pytest -q -n auto -p no:randomly --basetemp <scratch> <the 40 modules>; the five failing modules again with --basetemp D:/review-tmp/2026-11-24-wi1072/pt; python project-trajectory/scripts/run_menu.py smoke" rev="maint/wi-1072 at 98b7fe483 (modules, uncommitted then) and the close-out tree (smoke), 2026-11-24" -->
- Deferred open items: none — the operator owes no decision from this row;
  the amended rows go to the next sitting as owed acts.
