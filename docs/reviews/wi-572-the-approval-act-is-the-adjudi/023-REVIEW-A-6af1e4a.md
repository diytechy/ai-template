# Review A — WI-572 (the approval act is the adjudicator's), scope `contract_split...HEAD`

Model: claude-opus-5 (independent reviewer, fresh context)

## Instruments actually run

- `python project-trajectory/scripts/check.py --jobs 0` — `Check summary (stage
  DevStg-LLReqs, tier all)`: 9 PASS, 2 SKIP (`derived-stage`, `approval-fresh` —
  both skipped as "generated freshness is the trunk lane's"). `RESULT: PASS`.
- `python project-trajectory/scripts/trace.py --strict-integrity` — exit 0; final
  line `Traceability: SN=27 SR=76 LLR=188 TC=187 orphans=2 integrity=0
  verified-mechanized=72 verified-demonstrated=3 verified-attested=0 drafts=9
  budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=162
  interface-findings=0 provenance-findings=1 paraphrase-advisories=3.`
- `pytest -q -n auto -m smoke` — `1461 passed, 4 skipped in 20.47s` (budget 60 s).
- `pytest -q -n auto` (full) — `1 failed, 3280 passed, 20 skipped in 573.02s`.
  The one failure is `test_derive_stage.py::test_this_repo_s_committed_stage_is_current`,
  the `docs/stage` digest — the same artifact `check.py` SKIPs as the trunk
  lane's on a work branch; not attributed to this diff.
- `python project-trajectory/scripts/check_complexity.py` — `OK - 202 row(s) over
  15, unchanged from baseline` (and re-run against `contract_split`'s baseline to
  attribute the re-stamps; see MINOR below).

## What I drove (real shipped paths, not probes)

- `acceptance_record.staged_approval_acts(root, '580df781^', '580df781')` on this
  repo — reproduces the pre-ruling census the spec claims: exactly the four flips
  `LLR-203`, `LLR-204`, `TC-199`, `TC-200`, all `Drafted -> Approved`.
- `integrate._approval_act_refusal` on scaffolded claim repos built from
  `tests/integrate_fixtures.py` — flip, born, snapshot, adjudication-scope arms.
- `adjudicate_brief.first_approval_values` / `compose` on THIS repo's live
  registries with a real `Adjudicates` scope; the rendered prompt line inspected.
- `baseline_snapshot.copy_live` on a throwaway copy of `docs/`, with the record
  first synced to live so nothing unauthorised was pending.
- Mutation check of the headline regression: replacing `in_scope = rid in scope`
  with `in_scope = True` in `_render_chain` makes
  `test_the_first_approval_act_cannot_widen_past_the_rows_the_merge_handed_over`
  and `test_a_scope_whose_rows_are_all_settled_REFUSES_by_naming_them` FAIL
  (`2 failed, 3 passed`). The regression test genuinely bites the pre-fix
  behaviour; the file was restored byte-identical.

## Findings

- [MAJOR] project-trajectory/scripts/acceptance_record.py:122 -> `SPINE_CSVS` names only SR/LLR/TC, so `lane_approval_refusal` is blind to the other four status-carrying snapshotted registries — a worker lane that flips `stakeholder-needs.toml` `SN-001` `Drafted -> Approved` merges clean (driven: `_adjudication_lane` False, `_approval_act_refusal` returns `None`), while the doctrine this same diff ships states the ban without that carve-out (`PROCESS_OPTIONS.md` "Flips `Status` | **Never.** A flip in the lane's delta refuses the merge", and `gate-advance/SKILL.md` names the SN flip as part of the DevStg-Reqs approval the acceptor takes). It is the tier the shipped default dial holds for the HUMAN, and in a fresh adopter repo `unanchored_findings` is vacuous by design until the snapshot holds a registry, so nothing catches it there at all -> either widen the reader's registry set to the approval-carrying tiers, or narrow the three doctrine surfaces to say SR/LLR/TC explicitly -> @owner. (Antidote: the defect is representable only because the reader's registry set is a hand-written constant sitting a few hundred lines from `baseline_snapshot.SNAPSHOTTED`/`SNAPSHOT_TIERS`, which already enumerate every tier whose `Status` a snapshot anchors — one owning boundary deriving both would make "a tier no approval reader sees" unconstructible rather than detectable, which is exactly the `antidote` skill's "smallest change that makes this fix unnecessary".)

- [MAJOR] project-trajectory/prompts/adjudicate-first-approval.template.md:78 -> the derived `{registries}` slot is `;`-joined by `baseline_snapshot.format_approves` and is rendered UNQUOTED into `` `python scripts/intake.py snapshot --approves {registries}` ``, so a multi-registry batch hands the adjudicator a line the shell splits at `;`. Rendered from this repo's own live spine (`ab.compose` with `Adjudicates="LLR-205;TC-199"`): `--approves docs/requirements/low-level-requirements.toml=WI-599;docs/test/test-cases.toml=WI-599` — the second registry runs as a separate command, so only one registry is snapshotted and the merge then refuses the act as unanchored. This repo currently has drafted rows in two registries, so the two-registry batch is today's state, not a hypothetical -> quote the argument in the template (and in `intake.py:800`'s placeholder line, same shape) -> @owner.

- [MAJOR] project-trajectory/scripts/adjudicate_brief.py:766 -> `{registries}` is derived from every registry the batch is OFFERED, but the template blesses a mixed batch ("A MIXED batch is normal: approve the rows that are ready, return the rest") and step 2 tells the session to run `{registries}` verbatim. Driven end to end: with the record in sync and one new `Drafted` TC row authored by a lane, `copy_live(root, approves={test-cases.toml: ..., low-level-requirements.toml: ...})` WROTE both snapshot files even though no TC row was flipped; feeding that delta to `acceptance_record.adjudication_approval_refusal` returns `snapshot WIDENED to docs/test/test-cases.toml without an approved row`. So an adjudication that returns all of one registry's rows re-anchors that registry's unreviewed live text on its branch and is then refused at the merge slot with a message that describes neither what it did nor what to do -> make step 2 tell the session to drop registries whose rows it returned in full, or let the refusal admit a `--approves`-named registry whose snapshot moved without a flip -> @owner. (Antidote: the merge-slot guard cannot be designed away here because `{registries}` is fixed at composition time while the approve/return split exists only after the verdict — the structural fix is to stop typing the scope ahead of the act at all and have `intake.py snapshot` derive its authorised set from the `Status` flips staged in the same tree, one owning boundary that validates once; naming that is as far as this diff's scope reaches.)

- [MINOR] docs/complexity-baseline:1 -> the file's own header rule is "the baseline only ever tightens — re-stamp DOWNWARD or delete a row, never up to clear a finding", and the reason column records why a row is carried; this commit re-stamps `intake.py::_disposition_drafts` UPWARD 21 -> 25 and adds four rows (`handback.py::close_adjudication` 16, `gen_open_items.py::_none_declaration_findings` 16, `intake.py::_replace_inbound_edges` 18, `trace.py::_cell_diff_lines` 18) with an EMPTY reason, for functions this diff does not touch. Verified pre-existing rather than introduced: running `check_complexity.py` with `contract_split`'s baseline against the untouched current tree FAILS on exactly those five -> record the absorbed trunk overages with their reason (or repair them on trunk) so the ratchet's loosening is a reviewed act rather than a side effect of regenerating -> @owner.

- [MINOR, for clarity] project-trajectory/scripts/trace.py:3983 -> this diff corrects PROCESS.md §4 from "replaced wholesale at each approval" to "scoped to the registries that act authorises", but the two generators that tell a HUMAN SIGNER the same fact were left saying the retired thing — `trace.py:3983` and `gen_open_items.py:810` both emit "`intake.py snapshot` copies them WHOLESALE alongside any spine approval", and the sentence is live in the `docs/ratify/CURRENT.md` this diff regenerates -> re-word both strings to the scoped statement PROCESS.md now makes -> @owner.

## Done-when coverage

Spec items 1–5 map to covering tests, all of which I ran green: item 1 to the
seven merge-slot cases in `test_integrate_admission.py` (flip, born, snapshot,
clean-lane admission, trunk-side approval, rename trap, unreadable frontmatter)
plus the four reader cases; item 2 to the six scope cases at the merge slot and
the ten brief cases in `test_adjudicate_brief.py`, with the widening regression
mutation-proven above; item 3 to
`test_the_MEANING_aftermath_is_DERIVED_from_the_dial_not_left_to_the_judge`;
item 4 is prose, checked by reading (and by `prompt-catalog` / `skills-index` /
`doc-navigability` PASSing, and by the byte-budget rows, which I verified by
`wc -c` against all five watched files — every stamped number is exact); item 5
to `test_wi_loader_sync` and the `format_approves`/`parse_approves` round trip.
The `read_specs`/`spec_paths` repair is covered by the four re-armed
`test_wi_convert.py` guards.

UNCOVERED: the ban's behaviour on the four non-`SPINE_CSVS` approval-carrying
registries (MAJOR 1) — no test asserts either that they are refused or that they
are deliberately out of scope; and the mixed-batch `--approves` shape (MAJOR 3),
which no test exercises against the merge slot's own scope refusal.

VERDICT: CHANGES-REQUESTED findings=5
