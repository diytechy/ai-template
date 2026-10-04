# ADJUDICATE (amendment): WI-791, eight amended rows at ab061501

An independent spine adjudicator (Claude Opus) judged this amendment. It made none of the
changes it judges. The judgement used the kit brief composed for this lane's merge, read in the
lane as the owner directed on 2026-10-03 (S11). The anchor is `docs/archive/last_approved/`:
system-requirements copied 2026-10-03 (1fda46ed), low-level-requirements 2026-10-03 (439a2bb0),
test-cases 2026-10-03 (a9791303).

A row-by-row comparison of that copy with the live registries (every cell, both halves) finds
approved text moved in SR-178, LLR-153, LLR-158, LLR-245, LLR-278, TC-147 and TC-278, a routed
traced cell (`Verifies`) moved in TC-153, and traced-only moves outside this brief's scope
(LLR-118, LLR-167 and LLR-271 `CodeSymbol`; TC-123, TC-161 and TC-240 `Evidence`). No `Status`
moved. The brief's listing shows the approved cells; TC-153 is judged here from the same
comparison, since its `Verifies` cell routes.

The adjudicator read PROCESS.md §3 and §4, OI-100 and its ruling record, the work item, Codex
Sol's review 1, and the code each row describes at ab061501: `acceptance_record.py`
(`AMENDMENT_CSVS`, `staged_spine_amendments`, `_amended_cells`, `merge_approval_refusal`,
`held_reattest_refusal` and its helpers), `intake.py` (`next_wi_id`, `ROUTED_TRACED_CELLS`,
`adjudication_action`, `flip_verified`, `_apply_flips`), `baseline_snapshot.py` (`verdict_rel`,
`_refuse_verdict`, `copy_live`, `_record_act`, the ledger parser) and `integrate.py`
(`_approval_act_refusal`).

## Baseline and mutation probes

Baseline, in the unmodified lane, on the tests the four test-case rows cite:

- 31 passed: snapshot readers, acceptance record, staged trajectory, open-items render and
  adjudicate brief.
- 26 passed: intake and baseline snapshot.

The probes ran on a scratch export of ab061501, made with `git archive` outside the lane. Each
probe is a single-point mutation against a clause one of these rows states, and each was reverted
before the next. The lane was never touched.

| # | Mutation | Clause it breaks | Result |
|---|---|---|---|
| M1 | the dial read at the merge base, not trunk's tip | LLR-278; TC-278 "read at trunk's tip" | caught (`..._is_read_from_trunk_not_from_the_merge_base`) |
| M2 | a conflicting tag: the last one wins | LLR-278 "a MEANING ruling winning a conflicting tag" | **survived** |
| M3 | the below-approval guard removed | SR-228 "a first draft is not re-attested" | caught (`..._of_a_DRAFTED_row_is_refused`) |
| M4 | a row of a tier outside the walk read as released | stated by no row | survived (observation only) |
| M5 | only a MEANING ruling refused | SR-228 "an absent, unreadable or non-CLARITY verdict ... refused by row" | **survived** |
| M6b | the row and its verdict read at the merge base | LLR-278 "reads the named verdict at the head" | caught (`..._its_verdict_rules_CLARITY_merges`) |
| M7 | any held verdict re-attests | LLR-153, TC-147 "reattest held with a CLARITY verdict" | caught (`test_an_unreadable_dial_or_stage_fails_toward_recommend`) |
| M8 | AMENDMENT_CSVS drops DA and SUR | LLR-153, LLR-158, TC-147 | caught (2 tests) |
| M9 | staged_spine_amendments walks SPINE_CSVS again | LLR-158, TC-147 | caught (3 tests) |
| M10 | backslashes not normalized | LLR-245 | caught |
| M11 | an absolute path outside the repository admitted | LLR-245 "refuses one outside it" | **survived** |
| M12 | a verdict without `--reattests` admitted | the `_refuse_verdict` rule; TC-240 evidence | **survived** |
| M13 | the ledger entry drops the verdict (snapshot side) | SR-228 "the recorded act names the verdict" | caught (2 tests) |
| M13b | the same, judged at merge | SR-228 | caught |

M6 as first written read `base` inside `_held_act_lines`, where `base` is not in scope. Its three
failures were a NameError, not a kill, so it was re-run at the call site as M6b.

Score: 14 valid probes, 9 caught and 5 survived. Four of the five survivors are findings below;
M4 is not.

On the same scratch export, the tests proposed in Fixes 6 and 7 passed clean (5 passed) and
killed each survivor they target: M2 (1 test), M5 (2 tests), M11 (1 test), and M12 (the
narrowed assertion).

## Rulings

- [MEANING] LLR-153 detail -> before: a WI id is minted only by a human trunk commit or this helper; next_wi_id counts from max(the id-watermark, the spec-filename sweep) + 1, never max(live), and lets read_watermark's refusal stand; three triggers serial by construction, (a) the approved/routed-cell diff via staged_spine_amendments -> one adjudication row with before/after, routed traced cells named, (b) a merged ## Handback -> the disposition row, never for an adjudication row, (c) the gap census -> deduped gap rows; drafts-not-mints at the adjudication row's own merge; measurable tier signals; context_block's ordered joins, advisory; flip_verified flips under single-approve/autonomous; deterministic titles make the sweep idempotent -> after: the mint invariant; trigger (a) routes approved text movement in SR, LLR, TC, SN, DA and SUR rows into one amendment row; "the other mint triggers and deterministic id allocation remain as stated by this row"; flip_verified writes nothing on either arm and an unreadable dial or stage is held; adjudication_action returns flip, reattest for held CLARITY, or recommend -> not the same, twice over. The flip_verified arm inverted (a test that the old text's flips happen fails the new), a reattest arm was added and trigger (a)'s universe widened: these three moves are correct to the code and I would bless them. But the new text also DELETES the watermark rule, triggers (b) and (c), drafts-not-mints, the routed traced cells, the tier signals, context_block and the idempotence clause, and points at them with a sentence that refers to text the row no longer holds. No other LLR carries the watermark rule (SR-174's "counts from the recorded high-water mark") or drafts-not-mints, so a correct implementation of the new text could drop both. Not one I would bless: RETURN, Fix 1.
- [MEANING] LLR-158 detail -> before: split_changed_cells is the one basis (id and Status excluded structurally; the rest split by spine_cell_class, the classifier the warn reads), PUBLIC because is_drifted reads it; _APPROVED_TEXT requires the SAME Approved value on both sides; one two-tree walk with four consumers incl. lane_approval_refusal; the de-approval subtraction (an Approved -> Drafted withdrawal is exempt from the amendment reader, unreported by the approval-act reader, and raised by staged_drafted_rows); the per-row judgement in _approval_act; SPINE_CSVS (three tiers) is the default read by staged_spine_amendments and staged_drafted_rows, the warn's and the mint's universe; APPROVAL_ACT_CSVS adds SN, DA and SUR so a lane signing a need is refused; OUTSIDE_THE_APPROVAL_ACT; the exhaustive-and-disjoint pin -> after: split_changed_cells excludes id and Status and splits the rest; _spine_row_sides is shared; SPINE_CSVS is staged_drafted_rows' default; AMENDMENT_CSVS aliases APPROVAL_ACT_CSVS for staged_spine_amendments, consumed by the warn and the mint; the Hat-Refs arm is silent for SN, DA and SUR; OUTSIDE_THE_APPROVAL_ACT; the sets stay exhaustive and disjoint -> not the same. The widened amendment universe is the intended move and is correct to the code. But the new text also deletes obligations the code still keeps and no other row states: the same-Status rule on both sides, the de-approval subtraction, the classifier shared with the warn, is_drifted as the second reader of the basis, the per-row judgement in _approval_act, and lane_approval_refusal over the six tiers (a lane signing a need, assumption or surrogate). Not one I would bless: RETURN, Fix 2.
- [MEANING] LLR-245 detail -> before: refresh_refusal refuses while a drifted approved row is neither flipped nor named by --reattests; --approves clears nothing; every row and cell listed; --reattests parsed; the act's record stamps the re-attested ids; every SNAPSHOT_TIERS tier covered -> after: the same, plus a verdict path normalized repository-relative with forward slashes, "verdict_rel ... refuses one outside it", and the record "stamps the re-attested ids and normalized verdict" -> not the same: a verdict argument and its recording are new obligations. Not blessable as written: verdict_rel refuses nothing (it returns an outside path unchanged; _refuse_verdict refuses it, and also refuses a verdict given without --reattests and one naming no file, neither of which the text states); the prose stamp carries no verdict, only the act ledger entry does; the verdict half decomposes SR-228's "the recorded act names the verdict for later audit" while the row traces SR-207 alone; and TC-240, the row's only test case, states none of it in its Method (probes M11 and M12 below survive). RETURN, Fix 3, with Fix 7 for its test case.
- [MEANING] LLR-278 detail, title -> before: an adjudication lane's re-attestations are held to the Adjudicates scope of its claimed amendment rows, read from the ledger entries the merge adds -> after: the same, plus held_reattest_refusal: on a tier the dial at trunk's tip holds, a row below approval or absent is refused, and otherwise the named verdict must rule the row CLARITY, MEANING winning a conflicting tag; the title restates the rule more widely -> not the same: a new refusal case (the title alone would be CLARITY). Correct to the code, and probes M1, M3 and M6b below show the trunk-tip dial, the below-approval guard and the head-side verdict read are pinned. Not blessable as written: "whose tier trunk's tip holds at the commit the merge lands on" drops its subject (the dial) and names one commit twice, and the row calls that commit "the head", "the act head" and "the merge head"; "a MEANING ruling winning a conflicting tag" is verified by nothing (probe M2 survives). RETURN, Fix 4, with the tests in Fix 6.
- [CLARITY] SR-178 acceptance_criteria -> before: any artifact whose normative text moved from the copy recording its acceptance is reported whatever its Status did; approved cells report, traced cells do not, rows below approval never; the marker is never the movement; a stakeholder need is held to the same rule -> after: the same, with "stakeholder needs, assumptions and surrogates are held to the same rule" -> the same obligation. The first clause already obliges every artifact whose text moved from its recorded copy. Assumptions and surrogates were recorded artifacts before this lane: assumptions.toml is in SNAPSHOTTED and DA-ID/SUR-ID are in SNAPSHOT_TIERS, so the copy-based drift readers already reported them. The rider names two more instances of a rule that already covered them, as the need rider did; no behaviour, limit or actor moved, and a correct implementation of the old text passes the new.
- [MEANING] TC-147 method -> before: both gate-policy arms enact: attended recommends byte-identical; single-approve and autonomous flip only the named Status cells, cell-exact elsewhere, idempotent -> after: a held dial recommends byte-identical; a released dial writes nothing, refusing by name a row not already Approved and skipping one that is; an unreadable dial or stage reads as held; adjudication_action returns flip released, reattest held with CLARITY, recommend otherwise; an amended approved need, assumption or surrogate mints one amendment row (Verifies gains SR-228) -> not the same: the released arm's expected outcome inverted, and three cases were added. I would bless it: every new clause is pinned by an existing test (test_under_attended_adjudication_recommends_and_never_flips, test_below_the_human_dial_a_NON_FLIPPABLE_row_is_NAMED_not_skipped, test_a_FOUNDED_row_is_refused_with_the_reattest_remedy_naming_it, test_a_row_already_at_the_written_value_is_the_ONE_silent_skip, test_an_unreadable_dial_or_stage_fails_toward_recommend, test_an_amended_approved_need_mints_one_amendment_row, test_amended_approved_assumption_and_surrogate_mint_one_row), and probes M7, M8 and M9 are caught. It is not re-attested this round, because LLR-153, the row it verifies, is returned.
- [MEANING] TC-153 verifies, evidence -> before: verifies SR-178 and LLR-158 through the drift half (the amend+flip blindness premise and the four drift corners) -> after: also claims IF-091, with evidence adding the amendment-walk constant test and the staged need-amendment test, while method and expected are unchanged -> not the same: the row now claims to verify IF-091's walk universe and LLR-158's widened amendment walk, and its method states neither. A test case whose evidence names tests its method does not describe makes a claim no reader of the method can check. RETURN, Fix 5.
- [MEANING] TC-278 expected, method -> before: scope refusal by name; an in-scope act merges; a first-approval claim holds no re-attestation scope; mixed acts merge or refuse by scope -> after: the same, plus the held authority read at trunk's tip, and on a held rung a re-attestation without a verdict, of a row below approval or with a MEANING verdict refused by row while a CLARITY verdict merges (parents SR-178 and SR-228) -> not the same: a held-rung arm was added. Accurate to its tests, and probes M1, M3, M6b and M13b are caught. Not blessable as written: SR-228's acceptance also refuses an "unreadable or non-CLARITY" verdict, and LLR-278 states that a MEANING tag wins a conflict; the method claims neither, and probes M2 and M5 survive. RETURN, Fix 6.

VERDICT: MEANING rows=8

## Aftermath: nothing re-anchored this round

Six of the eight rows are returned. Under the owner's in-lane direction the follow-up is not
drafted as `## Dispositions`: the coordinator routes the fixes below to the author and resumes
this adjudicator to re-judge. No registry cell was edited and no act was taken. SR-178 (CLARITY)
and TC-147 (MEANING, blessed) wait for the act after the re-judge, so that one act re-anchors
every row in these registries together.

## Required fixes (to be applied in this lane, then re-judged)

Each replacement is the WHOLE cell value, byte-exact, between the fences (one line, no trailing
newline). Every other cell of every row stays byte-exact. Fixes 1 and 2 start from the ANCHOR
text in `docs/archive/last_approved/`, not from the live text: they restore what the amendment
deleted and change only the spans that the code really moved.

### Fix 1: LLR-153 `detail`

Derivation: the anchor text, with three spans changed. (a) Trigger (a) gains "whose walk covers
the SR, LLR, TC, SN, DA and SUR tiers". (b) The routed traced cells are named as
`intake.ROUTED_TRACED_CELLS` declares them; the anchor omitted the SR `Boundary-Refs` cell the code
routes. (c) The flip_verified sentence becomes the live text's two sentences (OI-45's write-nothing
arms, and adjudication_action's three arms). The spec-filename sweep also names
`docs/archive/work/`, which `next_wi_id` sweeps beside `docs/work/`.

```
The mint invariant: a WI id is created only by a human trunk commit or this helper - lanes never mint. next_wi_id counts from max(the docs/id-watermark mark, the sweep of every spec FILENAME under docs/work/ and docs/archive/work/, active/<branch>/ included) + 1 - never max(live) alone, so an id freed by a deleted spec is never re-issued - and trace.read_watermark's refusal on an absent or malformed mark is deliberately NOT caught: a mint with no record of what has been allocated must not proceed on a guess (TC-158, IF-101). Three triggers, serial by construction: (a) the approved/routed-cell diff on the merged commit via check_trajectory.staged_spine_amendments, whose walk covers the SR, LLR, TC, SN, DA and SUR tiers -> one adjudication row listing each changed row/cell/before-after (routed traced cells: SR SN-Refs and Boundary-Refs, LLR SR-Refs and TC Verifies per the declared cell split); (b) a merged spec carrying ## Handback -> the disposition row (outcomes cancel / defer / re-queue with drafted follow-up / surface an open item; NEVER minted for an adjudication row - no recursion, and handback.hand_back refuses the act itself); (c) the dispatcher's gap census -> concrete gap-closure rows, deduped against every existing row. Drafts-not-mints: a merged adjudication row's ## Dispositions fenced-toml drafts mint at ITS merge, validated loudly. Tier signals are measurable (rows touched, gate delta, handback reason class). context_block renders the pure registry joins (cancelled precedent WITH REASONS first, pending OIs, the LLR/TC code map, CMP knowledge packs, IF seams, precedent reviews) - advisory-never-gating, three consumers. flip_verified resolves the hold from the approval dial: held prints a recommendation and writes nothing; released requests the flip, but _apply_flips skips an already Approved row and refuses every other Status by name, so it writes nothing; an unreadable dial or stage reads as held. adjudication_action(human_held, verdict) returns flip when released, reattest when held with a CLARITY verdict, and recommend otherwise. The mint commit mirrors the claim's bookkeeping shape; every derived title is deterministic, so the sweep CLI re-run is idempotent.
```

### Fix 2: LLR-158 `detail`

Derivation: the anchor text, with two spans changed. The SPINE_CSVS sentence no longer claims
`staged_spine_amendments` or the warn and mint as its readers. One new sentence after the
need-tier sentence states AMENDMENT_CSVS, its consumers and the silent Hat-Refs arm.

```
An approval that records what it blessed by COPYING the registries needs no canonical text to hash, no separator that cannot occur in a cell and no second exclusion list, so no digest engine sits behind this row — the comparison basis is discharged by split_changed_cells(csv_path, id_col, head, row) -> {"approved": {cell: (before, after)}, "traced": {...}}: the id column and Status are excluded STRUCTURALLY - the id is the join key rather than content, and folding Status in would make every flip read as an amendment and every amendment invisible behind its own flip - and the remainder is split by spine_cell_class, the SAME classifier the amend-without-flip guard reads, so the two can never disagree about what normative means. It is PUBLIC for exactly one reason: baseline_snapshot.is_drifted reads it as the drift basis (LLR-173), so the snapshot comparison and the staged-amendment guard are one rule with one home rather than two rules that agree until they do not. _APPROVED_TEXT names the one Status value whose row TEXT is approved (Approved — the status fold collapsed Verified and Planned into it) and requires the SAME value on both sides, so prose rewritten under an Approved row is never invisible. It returns the before/after PAIRS a brief has to render anyway, which is why it replaced a hash rather than being wrapped by one. Needs are compared row by row through the same basis, their approved and traced cells split like every other tier's. ONE TWO-TREE WALK feeds every reader that asks what a spine delta did: _spine_row_sides pairs each row's before and after side once, and four consumers read it — staged_spine_amendments (the rows whose approved text moved), staged_approval_acts (the rows that crossed INTO an approval claim, or arrived already making one), staged_drafted_rows (the rows a lane authored below approval, which the first-approval mint is raised over) and lane_approval_refusal, the judgement over the second, worded for the merge slot that refuses a work branch performing an approval act. The walk is shared rather than copied so that the set one reader EXEMPTS is the set another REPORTS, MINUS the de-approvals: an Approved -> Drafted withdrawal moves Status, so the amendment reader exempts it, but it blesses nothing, so the approval-act reader does not report it and staged_drafted_rows raises the re-approval it now owes instead. Subject to that one subtraction, an approval act is invisible to the amendment reader by construction, and a row that no reader saw is unrepresentable. The per-row judgement is stated once, in _approval_act, so the flip arm and the born arm are read side by side rather than as two branches of the walk that could drift apart. UNREPRESENTABLE WITHIN A DECLARED BOUND, and the bound is named rather than left as an absence — the walk's universe is a PARAMETER over two declared sets, not one set every reader shares. SPINE_CSVS is the THREE registries whose rows carry an id column and an approved text — system-requirements, low-level-requirements, test-cases — and is the walk's default, so staged_drafted_rows, and the first-approval mint over it, read exactly it. APPROVAL_ACT_CSVS is those three PLUS stakeholder-needs and the assumptions registry's two tiers (assumptions and surrogates), and staged_approval_acts passes it, so lane_approval_refusal — the judgement over that reader — refuses a lane signing a NEED as readily as one signing an LLR. The need tier is inside because it is a spine tier carrying the same status vocabulary, and because the rung the approval act was moved off the writer's lane for is precisely the one a lane must not sign for itself. AMENDMENT_CSVS is an alias of APPROVAL_ACT_CSVS rather than a second list, and staged_spine_amendments passes it, so the amend-without-flip warn and the intake amendment mint, which both consume that walk, cover the need, assumption and surrogate tiers beside the three; the warn's Hat-Refs arm stays structurally silent on those three tiers, none of which carries Hat-Refs. The three registries a snapshot anchors that no approval reader walks — interfaces, external, components — are listed in OUTSIDE_THE_APPROVAL_ACT: off-spine, their approval cells governed by their own rung rather than this one. The two lists are pinned as one exhaustive, disjoint statement, SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT, against baseline_snapshot.SNAPSHOTTED's eight. A tier added to the snapshot therefore lands on one side or the other by a deliberate edit, and cannot reach no approval reader at all.
```

### Fix 3: LLR-245 `detail` and `sr_refs`

`sr_refs` becomes `["SR-207", "SR-228"]`: the verdict half decomposes SR-228's "the recorded act
names the verdict". In `detail`, the two verdict sentences are replaced. The new text attributes
each refusal to the function that makes it, states the two `_refuse_verdict` refusals the live
text omitted, and puts the verdict in the act ledger entry rather than the prose stamp, which does
not carry it.

```
refresh_refusal computes, per registry, the absorbed rows (approved text drifted from the recorded copy) minus the rows the act flips minus the rows named by --reattests, and refuses while that set is non-empty; naming a registry in --approves no longer clears its other rows. _refusal_text lists every such row and cell, with no cap. parse_reattests reads comma-separated row ids, and intake.py snapshot gains --reattests and --verdict, the verdict file that ruled the re-attested rows: verdict_rel spells it repository-relative with forward slashes, making an absolute path under the repository relative, and _refuse_verdict refuses a verdict named without --reattests, an absolute path outside the repository, and a path naming no file in the tree. The act's record stamps the re-attested ids beside the approvals, and its act ledger entry records the normalized verdict. The two snapshot tests that pin the old any-flip-authorizes-the-file behaviour change with it, since that behaviour is the one this row removes. The rule covers every tier in SNAPSHOT_TIERS, including the frame's three tiers, the assumptions registry's two and the needs file's two (needs and stakeholders), so an act copying the needs registry is refused while an approved need's text moved unread, and --reattests names a need or a stakeholder to re-anchor it.
```

### Fix 4: LLR-278 `detail`

One sentence is replaced. It names the dial as the subject, names the commit once, uses "the
head" as the row's other sentences do, and lists the three refusals the code makes.

```
acceptance_record.merge_approval_refusal calls reattest_scope_refusal and held_reattest_refusal for an adjudication lane, and they act only when the merge delta wrote the act ledger. reattested_between reads the ledger at the merge base and the head and takes the ids re-attested by the entries whose seq the base does not hold, refusing by name when either side does not parse. Every such id outside amendment_scope - the union of the Adjudicates cells of the claimed amendment rows, empty when none is claimed - is refused by name before the first-approval judgement runs. For each re-attested row whose tier the dial at trunk's tip holds - trunk's tip being the commit the merge lands on, not the merge base - held_reattest_refusal refuses the row by name when it is below approval or absent at the head, when its act names no verdict, or when verdict_rulings, reading the named verdict at the head, does not rule the row CLARITY; a row tagged both MEANING and CLARITY reads MEANING. An act that both approves rows and re-attests rows, claimed by a first-approval row and an amendment row together, merges when each half lies inside the scope of the row claiming it and every held re-attestation has its CLARITY verdict.
```

### Fix 5: TC-153 `method`

One sentence is appended, stating the two tests that the row's `evidence` already names.

```
Run the drift half of the baseline-snapshot suite. It first drives the premise: test_the_amendment_seam_is_BLIND_to_an_amend_plus_flip shows the staged-amendment guard silent on a sanctioned amend+flip over a real two-commit git repo. It then pins exactly what a change is taken over, in four corners: test_a_approved_cell_moving_under_an_approved_row_is_DRIFT (an approved cell must move it), test_a_TRACED_cell_moving_is_NOT_drift (the traced half must not), test_status_itself_is_never_the_amendment (the marker is excluded structurally, so a flip is neither an amendment nor a mask for one), and test_a_row_below_approval_can_never_be_drifted (no claim to fall from). The guard and the snapshot comparison share one public basis, split_changed_cells, called by both staged_spine_amendments and baseline_snapshot.is_drifted, so their agreement carries no case of its own. The amendment walk's universe is pinned beside them: test_the_amendment_walk_covers_every_tier_an_approval_act_blesses shows AMENDMENT_CSVS equal to APPROVAL_ACT_CSVS and naming the need, assumption and surrogate tiers while SPINE_CSVS keeps its three, and test_an_approved_needs_amendment_is_recorded_and_warned shows, over a real git repository, an approved need whose need cell moves in the index read as one amendment record carrying that cell's before and after, named by the amend-without-flip warn, with the Hat-Refs arm silent.
```

### Fix 6: TC-278 `method`, `evidence`, and three tests

`method`, with its held-rung sentence widened to the cases SR-228 and LLR-278 state:

```
Driven on real git repositories made from scaffolds. An adjudication lane claiming an amendment row scoped to one requirement, whose act re-attests two amended requirements, is refused at merge naming the one outside the scope; an act re-attesting only the scoped row merges, and the same act claimed by a first-approval row is refused naming the row, since that lane holds no re-attestation scope. The held authority is read at trunk's tip rather than the merge base. With the rung held, a re-attestation without a verdict, of a row below approval, with a MEANING verdict, with a verdict that does not rule the row, with a named verdict file absent at the act's head, or with a verdict tagging the row both MEANING and CLARITY is refused by row, while a verdict ruling an approved row CLARITY merges. One act that approves a Drafted requirement and re-attests an amended one, claimed by a first-approval row scoped to the first and an amendment row scoped to the second, merges; the same act whose amendment row is scoped to another requirement is refused naming the re-attested row.
```

`evidence`:

```
tests/test_snapshot_readers.py::test_a_reattestation_outside_the_amendment_scope_is_refused_by_name; tests/test_snapshot_readers.py::test_a_reattestation_inside_the_amendment_scope_merges; tests/test_snapshot_readers.py::test_a_held_rung_reattestation_without_a_verdict_is_refused; tests/test_snapshot_readers.py::test_a_held_rung_reattestation_its_verdict_rules_CLARITY_merges; tests/test_snapshot_readers.py::test_a_held_rung_reattestation_of_a_MEANING_row_is_refused; tests/test_snapshot_readers.py::test_a_held_rung_is_read_from_trunk_not_from_the_merge_base; tests/test_snapshot_readers.py::test_a_held_rung_reattestation_of_a_DRAFTED_row_is_refused; tests/test_snapshot_readers.py::test_a_held_rung_reattestation_its_verdict_does_not_rule_is_refused; tests/test_snapshot_readers.py::test_a_held_rung_reattestation_whose_verdict_is_unreadable_is_refused; tests/test_snapshot_readers.py::test_a_held_rung_row_ruled_both_ways_reads_MEANING_and_is_refused; tests/test_snapshot_readers.py::test_a_mixed_approval_and_reattestation_act_merges; tests/test_snapshot_readers.py::test_a_mixed_act_reattesting_outside_its_amendment_scope_is_refused
```

Add these three tests to `tests/test_snapshot_readers.py`, after
`test_a_held_rung_reattestation_of_a_DRAFTED_row_is_refused`. They use only that module's own
helpers. On a scratch export of ab061501 they pass, and they kill probes M2 and M5:

```python
def test_a_held_rung_reattestation_its_verdict_does_not_rule_is_refused(scaffold):
    """SR-228: a verdict that rules other rows and not this one is a
    non-CLARITY verdict for it, so the held-rung act is refused by row."""
    text = "- [CLARITY] SR-002 title -> same obligation\n\nVERDICT: CLARITY rows=1\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _AMENDMENT, True, trunk=head
    )
    assert refusal and "SR-001 is not ruled CLARITY" in refusal, refusal


def test_a_held_rung_reattestation_whose_verdict_is_unreadable_is_refused(scaffold):
    """SR-228: an act naming a verdict its own head does not carry has no
    readable ruling, so the held-rung act is refused by row."""
    text = "- [CLARITY] SR-001 title -> same obligation\n\nVERDICT: CLARITY rows=1\n"
    base, _head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    run_git = _git(scaffold)
    run_git("rm", "-q", _VERDICT)
    head = _commit(run_git, "the named verdict leaves the head")
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _AMENDMENT, True, trunk=head
    )
    assert refusal and "SR-001 is not ruled CLARITY" in refusal, refusal


def test_a_held_rung_row_ruled_both_ways_reads_MEANING_and_is_refused(scaffold):
    """LLR-278: a verdict tagging one row both CLARITY and MEANING rules it
    MEANING, whichever tag comes first, so the held-rung act is refused."""
    for order in (("CLARITY", "MEANING"), ("MEANING", "CLARITY")):
        text = "".join("- [{}] SR-001 title -> ruled\n".format(w) for w in order)
        assert AR.verdict_rulings(text) == {"SR-001": "MEANING"}, order
    text = "- [MEANING] SR-001 a -> b\n- [CLARITY] SR-001 c -> d\n"
    base, head = _amendment_act(scaffold, {"SR-001"}, held=True, verdict=text)
    refusal = AR.merge_approval_refusal(
        scaffold, base, head, _AMENDMENT, True, trunk=head
    )
    assert refusal and "SR-001 is not ruled CLARITY" in refusal, refusal
```

### Fix 7: TC-240 `method`, `expected`, `verifies`, `evidence`, one test and one assertion

`verifies` becomes `["SR-207", "SR-228", "LLR-245"]`.

`method`, with one sentence appended:

```
Driven on real git repositories through the snapshot command, parameterized over every row-compared tier: requirements, design rows, test cases, interfaces, components, the frame's entities, crossings and relationships, assumptions and surrogates, needs and stakeholders. For each, an act approving row A while row B of the same tier carries drifted approved text is refused naming B and the cell; naming the registry alone in the approves option does not clear B; adding B through the re-attests option clears it, and the act's record names B. In a file holding two tiers, drift in one tier refuses an act approving a row of the other. A registry with no drifted row outside the act refreshes as before. Seven drifted rows are all named, with none cut off. A drifted approved need refuses an act naming the needs registry, naming the need and the cell, until the re-attests option names it, and the act ledger then records it. An act re-attesting a row with a named verdict records that verdict in its act ledger entry, spelt repository-relative with forward slashes whether it was given with backslashes, as an absolute path under the repository or with a leading ./; a verdict given without the re-attests option, a verdict naming no file and a verdict outside the repository are each refused, the last leaving the act ledger unchanged.
```

`expected`, with one clause appended:

```
Satisfies SR-207's acceptance: a drifted row outside the act refuses the refresh naming row and cell; adding it clears the refusal and is named in the record; no drift refreshes as before; every compared tier covered, including tiers sharing a file; and, for SR-228, a re-attesting act's named verdict is recorded in its act ledger entry in repository-relative form, while a verdict with no re-attested row, naming no file or outside the repository is refused.
```

`evidence`:

```
tests/test_baseline_snapshot.py::test_a_reattesting_act_records_its_verdict_and_refuses_a_bad_one; tests/test_baseline_snapshot.py::test_a_verdict_path_is_recorded_repo_relative_with_forward_slashes; tests/test_baseline_snapshot.py::test_a_verdict_outside_the_repository_is_refused; tests/test_baseline_snapshot.py
```

Add this test to `tests/test_baseline_snapshot.py`, after
`test_a_verdict_path_is_recorded_repo_relative_with_forward_slashes`. It passes at ab061501 and
kills probe M11:

```python
def test_a_verdict_outside_the_repository_is_refused(tmp_path):
    """LLR-245: the act ledger records a verdict by its repository path, so a
    verdict file outside the repository is refused although it exists, and
    the ledger does not move."""
    root, _run_git = _git_tree(tmp_path)
    sid, row = _first_row_at(root, "approved")
    _rewrite(root, SR_REL, row["Title"], row["Title"] + " (clarified)")
    outside = tmp_path / "v.md"
    outside.write_text("- [CLARITY] {} title -> same\n".format(sid), "utf-8")
    acts = len(SNAP.read_acts(root))
    with pytest.raises(SystemExit) as refused:
        SNAP.copy_live(root, reattests={sid}, verdict=str(outside))
    assert "not a file in the tree" in str(refused.value), refused.value
    assert len(SNAP.read_acts(root)) == acts
```

In `test_a_reattesting_act_records_its_verdict_and_refuses_a_bad_one`, replace

```
    assert "--verdict" in str(no_rows.value), no_rows.value
```

with

```
    assert "names no re-attested row" in str(no_rows.value), no_rows.value
```

The shipped assertion also matches the missing-file refusal, which fires for the same call, so it
cannot tell the two rules apart. That is why probe M12 survives. The narrowed assertion kills M12.

## Findings outside the judged rows (owed, not ruled here)

These rows' approved text did not move, so no adjudication routed them. Each is a behaviour this
lane added whose code names an LLR (`Implements:` and the `CodeSymbol` pointer) while that LLR's
approved `detail` does not state it. A `CodeSymbol` move is traced and unrouted, which is how each
one passed the amendment mint unseen.

- **LLR-118**: `gen_open_items.verdict_reattest_block`, the open-items audit list of every act
  that names a verdict. This is the work item's Done-when "every held-rung CLARITY re-attestation
  stays listed on the owner's surface for audit", and no approved row states it.
- **LLR-167**: `adjudicate_brief._unchained_amended_rows`, which makes the amendment brief render
  drifted need, assumption and surrogate rows. The detail still says `amendment_values` renders
  "the drifted rows `trace.reattest_model` finds", and that model holds none of those three tiers.
  This behaviour is load-bearing for gap 1: without it a routed need amendment refuses as
  "nothing in scope".
- **LLR-271**: `baseline_snapshot.tier_owing` is named in `CodeSymbol`; the detail mentions only
  `needs_owing`. This one is minor.

## Observations (no fix required by this verdict)

- **The unknown-tier fail-safe is unpinned (probe M4).** `_held_row` reads a row of a tier outside
  the amendment walk as held. LLR-278 does not state this, so it is not a finding; it is
  defensible as it stands.
- **TC-147's expected cell names SR-174 only**, although its `verifies` cell now includes SR-228.
  The kit applies no rule here (TC-153's expected cell does not name IF-091 either), so this is
  left to the author.
- **The S11 in-lane route never reaches this lane's merge-slot rule.** `held_reattest_refusal`
  runs only for a lane whose every claimed spec declares `safety_class = "adjudication"`. An
  ordinary lane carrying an in-lane act would be refused by `lane_approval_refusal`, so in-lane
  acts land by the coordinator's squash, and no merge-slot rule ever reads them. For this lane the
  point is moot, because the dial releases SR, LLR and TC. On a held rung, though, SR-228's
  refusal would not see an in-lane act. The work item scopes in-lane routing to the S11 plan; this
  is for that plan.
