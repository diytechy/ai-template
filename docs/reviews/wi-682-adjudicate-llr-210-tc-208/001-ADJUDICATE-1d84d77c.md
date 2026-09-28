# ADJUDICATE — WI-682 — amendment at 1d84d77c

Independent adjudication of the two approved rows WI-679 amended in place:
LLR-210 (Detail) and TC-208 (Method). The one question, per row: MEANING or
CLARITY. Brief: the kit's amendment brief rendered for this row
(`adjudicate_brief.compose`, anchor `docs/archive/last_approved` copied at
464dc7ac for the LLR and TC registries), with the caller's one addition to its
method: each new text was checked against the code and the tests it names on
this tree before it was blessed, and the tier cell against `tests/conftest.py`
`SLOW_MODULES` loaded in process. I directed neither amendment and read no
session's account of it; the wave-5 arbitration file was read as context for
why, never as evidence that a cell is true. HEAD stayed at 1d84d77c throughout
and the worktree was clean before this file was written.

The dial: `human_approval_through = "DevStg-Boundary"` in `docs/process.toml`,
so the LLR and TC rungs are released and a MEANING verdict is re-attested by
this session, in the one snapshot act batch C shares across its nine rows.

- [MEANING] LLR-210 Detail -> `clusters` seeds candidate sets from the queue-conflict pairs plus the commissioning and module signals; `census_draft` carries the scope in `Adjudicates` and a queue sha over the queued rows plus a spine sha in `Digests`; three refusals: none beside ANY queued or active judgement, none for a queue sha a consolidation row already carries, and a row an earlier consolidation minted (read from any consolidation's scope) neither seeds nor may be re-absorbed; `parse_verdict`/`close_refusal` refuse a moved row that is not queued; `archive_absorbed` moves the absorbed rows at the mint -> the same selection over a stated POPULATION (`queued_work`: a judgement row and the `-000` example row are never candidates, and the queue sha is taken over the work rows alone); guard 1 restated as four named refusals (a judgement active; another consolidation queued; a queued judgement whose `Adjudicates` names a candidate; a queued judgement sorting at or before the would-be row in `schedule.evaluate`'s own order) while a queued judgement that does neither refuses nothing; guard 3 keyed on an ENACTED absorption (`enacted_absorbs`: a done consolidation row whose recorded `## Consolidation` outcome is `consolidate` and whose `## Dispositions` draft supersedes a restructured row), so a queue, edge or return verdict, a cancelled row, a scope-only row or a hand consolidation makes no successor and its host seeds clusters and may be absorbed; and the brief's prior lines read every absorption from the successors' `Supersedes` (`prior_absorbs`), kept after a successor's own absorption, each absorbed row marked judged-by or by hand (`prior_line`, `HAND_LABEL`) -> cases were added and one was removed: the old guard 1 refused beside any queued judgement and the new one lets an unrelated, lower-sorting one stand; the old guard 3 read any consolidation's scope as judged and the new one reads only an enacted absorption, so a hand host the old text protected is now absorbable. Blessed: `queued_work`, `queue_digest`, `_order_refusal` (the probe row ordered by `schedule.evaluate` with an id above every id on file), `enacted_absorbs`/`_enacted_supersedes`, `judged_absorbed`, `consolidation_successors`, `prior_absorbs`, `prior_line` and `HAND_LABEL` in `project-trajectory/scripts/consolidate.py` read exactly as the cell says, all fourteen named symbols resolve there, and the cell states the standing mechanism with no history in it.
- [MEANING] TC-208 Method -> in process on hand-built rows: THE SELECTION (the digest's four moving and two still fields, the malformed digest, the two widened signals and the bare module name, one set from two disjoint pairs, a detector-only pair, the carrier-aware spine digest) and THE GUARDS (no draft beside a queued or active judgement, a judged queue state, a consolidation's own successor, re-absorption, a malformed verdict, the close's not-queued refusal, the byte-identical archived spec) -> the same selection, plus THE POPULATION (two judgement rows sharing a spec make no candidate set and leave the queue digest unmoved; the example row makes none) and the guards restated for the widened rule: four refusals each naming the judgement, a lower-priority no-candidate judgement refusing nothing, the successor of a done consolidate-outcome row seeding nothing, a queue/edge/return, cancelled or verdict-less row and a hand host making no successor, the prior lines' per-row marks and the nested hand chain keeping both absorptions -> new arms a test must drive, and one old arm (any queued judgement refuses) withdrawn in favour of its narrower successors. Blessed: all twenty-seven named pointers resolve by function name in `tests/test_consolidate.py` and passed (fast batch below); Tier Smoke is true, `test_consolidate` is not in `SLOW_MODULES`; the Method states the test as it stands and carries no history or status.

## How the cells were read

- Before and after were compared as obligations, per the brief. Both rows
  add cases and withdraw one, so both are MEANING; each new clause was located
  in `consolidate.py` and in a named test before being blessed. Neither cell
  narrates its own history: the amendment replaced the old guard text rather
  than appending a "now ... was" account to it.
- The two rows are the only cells in scope. SR-220, the parent both rows
  hang under, is judged in WI-683 and WI-696 (first approval), not here.

Bar I produced (not claimed), on this tree with `python -m pytest -q -n 4 -p
no:cacheprovider`: `tests/test_consolidate.py` ran in the fast batch shared
across batch C (`test_consolidate`, `test_spine_carrier`, `test_absolute_terms`,
`test_verification_coherence`, `test_mapping_purpose`, `test_assumption_rules`,
`test_registry_id_inputs`, `test_skill_materialization`,
`test_guardrails_payload`, `test_skills_index`, `test_kitlib_secret_classes`,
`test_check_complexity`, `test_evidence_join`, `test_baseline_drift`): **448
passed, 1 skipped in 16.80s** (the skip is `test_kitlib_secret_classes.py:214`,
a class with no pre-table scan pattern, by design). No failures, no errors.

## Dispositions

None owed: both rows are blessed and join the act's `--reattests`.

VERDICT: MEANING rows=2
