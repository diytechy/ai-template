# ADJUDICATE — WI-693 — amendment at 1d84d77c

Independent adjudication of the six approved rows WI-651 amended in place
under the owner's OI-91 ruling (a) and the coordinator's wave-5 grants (17, 24,
25): LLR-173, TC-167, SR-178, LLR-158, LLR-245 and TC-240. The one question,
per row: MEANING or CLARITY, and for each MEANING row whether its new text is
one I would bless. Brief: the kit's amendment brief rendered for this row
(`adjudicate_brief.compose`, anchor `docs/archive/last_approved` copied at
464dc7ac for the SR, LLR and TC registries), with the caller's addition: each
new text was checked against the code and tests it names on this tree, and
against the spine-authoring skill's cell hygiene, before being blessed. I
directed none of the amendments and read no session's account of them; the
arbitration file was context for why, never evidence. HEAD stayed at 1d84d77c
throughout; the worktree was clean before this file was written.

The dial: `human_approval_through = "DevStg-Boundary"`, so the SR, LLR and TC
rungs are released and a MEANING verdict is re-attested by this session in the
one snapshot act batch C shares — for the rows it blesses.

- [MEANING] LLR-173 Detail -> `copy_live` mirrors seven registries (the four spine tiers plus interfaces, external and components); `unanchored_findings` is "ADVISORY TODAY", returning strings that join no failure set, to be promoted to the integrity floor at migration step 7 -> `copy_live` mirrors the snapshotted registries, assumptions included; `unanchored_findings` asks its question of every tier `SNAPSHOT_TIERS` lists, the needs file's needs and stakeholders included, and reads a legacy markdown needs copy as present; and it joins the integrity failure set, failing the always-on `--strict-integrity` floor at every stage, vacuous until the record holds a registry so a tree that has signed nothing is never redded by it -> three obligations moved: the copied set widened to eight, the rule's coverage widened to the two need tiers, and its severity moved from advisory to gating. BLESSED on the final text (second sitting, 2026-09-28, below): `SNAPSHOTTED` holds eight entries, `SNAPSHOT_TIERS` ends in `NEED_TIERS`, `_copy_file` resolves the needs copy under either carrier, `record_findings` (unanchored plus act-ledger faults) is appended to `findings.integrity` in `trace.py` at every invocation of the floor, `unanchored_findings` returns `[]` when `load_all` finds no record and again when no `SNAPSHOTTED` registry resolves under the snapshot root (the two vacuity arms the sentence states), and TC-167's `test_an_approved_NEED_or_STAKEHOLDER_without_its_anchor_is_unanchored` drives the need arm (slow batch, green). The first sitting's wording, which ended "it was armed there at migration step 7 and not before, because against a pre-seed or pre-rename snapshot it would red every row", was withheld as the row's own arming history (the receipt shape batch B returned TC-203 for) and is kept only as sitting history.
- [MEANING] TC-167 Expected, Method -> Expected: IF-124 rides TC-161 and IF-125/126 are uncited; Method arm (d): an approved row absent from the snapshot, an approval whose copy reads below approval, a registry missing from an existing snapshot, an unparseable snapshot raising -> Expected: IF-126 rides TC-271 and IF-125 is uncited; Method arm (d): the same, "each as true of an approved need and an approved stakeholder as of a spine row" -> new arms a test must drive (the need and stakeholder unanchored cases) and a seam-coverage claim moved. Blessed: `test_an_approved_NEED_or_STAKEHOLDER_without_its_anchor_is_unanchored` exists beside the two spine unanchored tests in `tests/test_baseline_snapshot.py` and passed; TC-271's `Verifies` names IF-126 at HEAD (judged in WI-694), so the Expected's claim is true of the registry; Tier Full is true, `test_baseline_snapshot` is slow.
- [MEANING] SR-178 Requirement, AcceptanceCriteria, Rationale -> Requirement and acceptance: needs are held to the drift rule "despite their carrying no status cell"; Rationale: needs "are covered by the whole-file copy rather than by a per-need projection", because a need has no Status cell at all -> Requirement and acceptance: needs are held to the same rule, the false premise dropped; Rationale: the rider is normative because the need tier is the one a sitting most wants to hold and each rule walks the tiers it is given, and "needs are compared row by row under the same approved and traced split as every other tier" -> the requirement and acceptance cells lose a false parenthetical and impose the same obligation, which alone would be clarity; the rationale's comparison basis for a need moved from the whole file to the row under the approved/traced split, so a traced cell moving on a need is no longer movement — an acceptance condition read from the rationale, and the cell that carries the meaning. Blessed: needs carry a `status` cell in `stakeholder-needs.toml`, `NEED_TIERS` puts both need tiers through `owing_rows`/`drifted_cells` (the same `split_changed_cells` basis, LLR-158), and TC-269's tests drive a drifted need and a drifted stakeholder row by row. Noted, not returned on: the rationale's "the one the amendment-watching rules were last to reach" is a flourish about the rules' order of arrival that the argument does not need; it names no event, date or status of the row, so I read it as the failure-class argument the cell is for and surface it below.
- [MEANING] LLR-158 Detail -> needs are covered by the whole-file copy rather than a per-need projection; `APPROVAL_ACT_CSVS` is the three spine registries plus stakeholder-needs; the two lists are pinned against `SNAPSHOTTED`'s seven -> needs are compared row by row through the same basis, their approved and traced cells split; `APPROVAL_ACT_CSVS` is the three plus stakeholder-needs and the assumptions registry's two tiers (assumptions and surrogates); pinned against `SNAPSHOTTED`'s eight -> the lane-approval refusal now walks two more tiers: a work branch signing a DA or SUR row is refused by name where the old text let it through, and the need comparison changed basis. Blessed: `acceptance_record.APPROVAL_ACT_CSVS` lists `SN-ID`, `DA-ID` and `SUR-ID` beside the three, `baseline_snapshot.SNAPSHOTTED` has eight entries, `OUTSIDE_THE_APPROVAL_ACT` still names the three off-spine registries, and `tests/test_acceptance_record.py` pins the partition.
- [MEANING] LLR-245 Detail -> the refresh refusal covers every tier in `SNAPSHOT_TIERS`, the frame's three and the assumptions registry's two, and "the needs file is outside SNAPSHOT_TIERS and stays outside" -> it also covers the needs file's two tiers (needs and stakeholders), so an act copying the needs registry is refused while an approved need's text moved unread, and `--reattests` names a need or a stakeholder to re-anchor it -> a refusal class the old text excluded by name is now in force. Blessed: `SNAPSHOT_TIERS` is the ten row tiers plus `NEED_TIERS`, `refresh_refusal`'s docstring and `_unattested_rows` walk that tuple, and TC-240's parametrization is `SNAPSHOT_TIERS` itself (`test_the_row_rule_is_driven_over_EVERY_compared_tier` asserts `SN-ID` and `STK-ID` are in it). Noted, not this amendment's: the unchanged sentence "The two snapshot tests that pin the old any-flip-authorizes-the-file behaviour change with it" is the row's own history in an approved cell, surfaced below.
- [MEANING] TC-240 Method -> parameterized over ten row-compared tiers; "A drifted need is not covered." -> parameterized over the same ten plus needs and stakeholders; "A drifted approved need refuses an act naming the needs registry, naming the need and the cell, until the re-attests option names it, and the act ledger then records it." -> a case the old text disclaimed is now required. Blessed: `_TIERS` in `tests/test_baseline_snapshot.py` is built from `SNAP.SNAPSHOT_TIERS` so the need tiers ride every parametrized case, and the need-refusal arm is driven end to end in `tests/test_snapshot_readers.py::test_a_drifted_need_refuses_the_snapshot_until_it_is_reattested` (TC-269's pointer, slow batch, green); Tier Full is true.

## How the cells were read

- Before and after were compared as obligations, per the brief. All six rows
  add or withdraw a case, a tier, a registry or a severity, so all six are
  MEANING; each new clause was located in `baseline_snapshot.py`,
  `acceptance_record.py`, `trace.py` and a named test before being blessed.
- Five rows are blessed and join the act's `--reattests`. LLR-173 is not:
  its new text is true of the code and its meaning change is right, but the
  sentence that carries the change also records the row's own arming history,
  and blessing it would anchor a receipt as approved text. The fix is one
  clause; it is drafted in `docs/work/queued/WI-693-adjudicate-llr-158-llr-173.md`
  under `## Dispositions

At the first sitting LLR-173 was withheld and a corrective clause was drafted
in this row's spec. At the second sitting (below) the cell carries that
clause and is blessed; the draft is withdrawn from the spec and none is owed.
Every cell of every row in scope is left byte-exact by this verdict.

## Non-blocking findings (surfaced, not acted on)

1. **SR-178's rationale, "the one the amendment-watching rules were last to
   reach"**, narrates the rules' order of arrival; the sentence stands without
   it. A clarity trim at the next amendment.
2. **LLR-245's unchanged sentence about "the two snapshot tests that pin the
   old any-flip-authorizes-the-file behaviour"** is the row's own history in an
   approved cell, older than this amendment; the same trim applies.
3. **LLR-158's parenthetical "(Approved — the status fold collapsed Verified
   and Planned into it)"** and **TC-167's "IF-125 is uncited today"** are
   history and status words in approved cells that predate this amendment.
4. **LLR-173's code docstring** carries the same migration-step narrative the
   cell does; the docstring is code and outside the spine's hygiene rule, but
   a reader who copied it into the cell would repeat the return.

## Second sitting, 2026-09-28 — LLR-173 re-judged on its amended clause

The coordinator replaced the withheld sentence (2f9912cb, status left
Approved, no other cell changed — driven: a cell-by-cell diff of the row
against 6e55d405 moves `detail` alone, and within it only the closing
sentence) with the standing wording the first sitting drafted, under wave-5
ruling 37: "unanchored_findings joins the integrity failure set, so it fails
the always-on --strict-integrity floor at every stage; it is vacuous until
the record holds a registry, so a tree that has signed nothing is never
redded by it." I authored the draft but not the amendment, and the cell is
judged on its text against the code, not on its provenance. Judged again on
the full amended Detail: the severity clause is true (`record_findings` joins
`findings.integrity` in `trace.py`, which every `--strict-integrity` run
reads, at every stage); the vacuity clause is true and is exactly the two
early returns in `baseline_snapshot.unanchored_findings` (`load_all` returning
None; no `SNAPSHOTTED` registry resolving under the snapshot root); the
sentence states what holds now and names no event, step or date; and the
rest of the cell is byte-identical to the text the first sitting found true
of the code.

- LLR-173: MEANING, BLESSED. Joins `--reattests`; the act re-attests all six
  rows of this item. The corrective draft is removed from the spec's
  Dispositions, since the cell carries the fix, and that section is renamed
  so no block-less `## Dispositions` reaches the merge.

Counts after this sitting: 6 MEANING, all blessed; 6 rows in the act's
`--reattests`.

## Third sitting note, 2026-09-28 — the act narrowed under wave-5 ruling 38

The six rulings above stand. The narrowed act re-attests this item's LLR and
TC rows (LLR-158, LLR-173, LLR-245, TC-167, TC-240); SR-178 is blessed but
not re-attested by it, since the SR registry is not copied, and stays
drifted and visible until an act copying that registry names it.

VERDICT: MEANING rows=6
