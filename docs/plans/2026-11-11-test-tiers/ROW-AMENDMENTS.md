# Row amendments ruled 2026-11-16: drafts for the operator's acceptance

Written in the post-§10.5 vocabulary ("accepted", `Accepted`). Apply after
§10.5 lands, as Drafted changes the operator accepts in one act. Only the
cells shown change; new text is marked **[new]** in the explanation, the cell
itself is the full replacement.

## 1. SR-195: the count line while no stakeholder is agreed

`requirement`, full replacement:

> The delivered harness shall report each stakeholder need an assumption
> serves that none of the assumption's landing crossings reaches, and each
> landing crossing that reaches none of those needs, where a crossing reaches a
> need when it belongs to the party of one of the need's accepted stakeholders
> or to a party that mediates for it; while no stakeholder is agreed with a
> party, it shall report those findings as one line giving their count.

`acceptance_criteria`: append one sentence:

> While no stakeholder is agreed (accepted, or founded, with a party), the
> reports above are given as one line with their count in place of one line
> each, because reach cannot be judged until one is; they are listed one by
> one again once a stakeholder is agreed.

## 2. LLR-227: the same, in the design row

`code_symbol`: `assumption_reach_advisories/reaching_parties/held_until_agreed`
(the fold is bound to no row today).

`detail`: append:

> held_until_agreed(lines, stks, what) passes the reach-caused lines through
> unchanged once a stakeholder is agreed (Accepted or Founded, with a Party);
> while none is, it returns one line in their place giving the count and
> asking for the stakeholders to be accepted. assumption_reach_advisories
> returns its lines through it.

TC-223 (verifies SR-195, LLR-227): `method` gains one sentence, `evidence`
already names the file:

> With every stakeholder Drafted, the reach advisories are one line giving
> their count, and the per-row lines return once one stakeholder is accepted
> with a party.

## 3. SR-205: the gate honours `delivered_with` (and the count line)

`requirement`, full replacement:

> Where the assumption gate is enabled, the delivered harness shall fail the
> boundary gate for each system requirement not recorded as coincident and not
> delivered jointly with a sibling that shares one of its needs, that cites no
> assumption, and for each requirement that cites an assumption which is not
> accepted, not active, does not reach the stakeholders of its needs, or is a
> fidelity assumption naming a surrogate that is not accepted.

`acceptance_criteria`, full replacement:

> With the gate enabled, a requirement recorded as coincident passes; a
> requirement whose every cited assumption is accepted, active, reaching and,
> for a fidelity assumption, backed by an accepted surrogate passes; a
> requirement citing no assumption and carrying no waiver fails, unless its
> `delivered_with` names a sibling sharing one of its needs, in which case it
> passes; any assumption a joint requirement does cite is judged like any
> other; any other cited assumption fails the boundary gate naming the
> requirement, the assumption and the unmet condition; with the gate disabled
> the same conditions are advisory, and while no stakeholder is agreed the
> advisories the reach check causes are one line with their count; the gate
> is enabled or disabled by one declared setting; a project declaring no frame
> is vacuous.

`title` (vocabulary only): "With the assumption gate on, the boundary rung
requires accepted, active assumptions that reach their stakeholders".

## 4. LLR-242

`code_symbol`: add `_fold_reach_caused`.

`detail`: replace "it fails each requirement with no Coincident whose DA-Refs
is empty" with:

> it fails each requirement with no Coincident whose DA-Refs is empty, unless
> the requirement is joint (its Delivered-With names a declared sibling sharing
> one of its SN-Refs, the class `_classify` already gives it)

and append:

> With the gate off, check_assumption_gate's `_fold_reach_caused` passes only
> the reach-caused advisories (those absent when the same judgement runs with
> an empty reach map) through held_until_agreed; every other advisory stays
> listed, and a failure is never folded.

Code change behind it: in `boundary_gate_findings`, skip the "cites no
assumption" finding when `_classify` returns `joint`; the loop over cited
assumptions is unchanged. One test each way (joint with no citation passes;
joint citing an unaccepted assumption still fails), tagged to SR-205's TC.

**One point to note, not ruled:** if every row of a joint group cites
nothing, the gate now passes them all although no row carries the argument.
Requiring one member of the group to carry an assumption or a waiver would
close that. It is not in the ruling and is left out unless the operator asks.

## 5. LLR-172: drop "NOT BUILT YET"

`detail`, full replacement:

> Extends the existing component pass (trajectory_arch.component_findings,
> run by check_trajectory.py), the one home that already reads
> docs/requirements/components.toml and already emits CMP findings, with the
> derivation-record rules SR-165 states, rather than adding a second reader of
> the same registry. derivation_record_findings: each live CMP row either holds
> the record (candidates, objective, constraints, a score per candidate, the
> selected partition and the operator ruling) or cites, with `derivation`, the
> one live row that holds it. An absent record, a missing element (one finding
> naming the row and the element) and a malformed cell are each reported, and a
> finding against a held record is reported once, on the holding row, naming
> the rows that cite it. Two derived rules run only on a complete, well-formed
> record, because presence alone is satisfiable by a record that says nothing:
> (1) THE RANKING RECOMPUTES: a feasible candidate ranks above every infeasible
> one, then by score in the objective's direction, and an order the recompute
> contradicts is a finding, which makes the record falsifiable without a
> reviewer re-running a model session; (2) A SELECTION THE SCORES DO NOT RANK
> FIRST is a finding unless the record carries an override naming that choice,
> and an override where the selection does rank first is also a finding.
> Findings warn plain and fail under --strict; `[checks] components_check =
> false` turns the pass off. Vacuous on a project declaring no components and
> on the example -000 rows. Built by WI-999; CMP-006 holds this repository's
> record and CMP-007 to CMP-009 cite it.

## 6. TC-166: the method names what runs

`method`, full replacement:

> Run trajectory_arch's component pass (derivation_record_findings, through
> component_findings as check_trajectory.py runs it) over fixture component
> registries: (a) a complete derivation record passes silently; (b) a record
> omitting each element in turn (candidate partitions, objective, constraints,
> any candidate's score, the selected partition, the operator ruling) is
> reported once per omission, naming the row and the missing element; (c) each
> malformed record cell, and each malformed `derivation` citation, is reported;
> (d) an absent record is reported once, on the row its citers name; (e) a
> record whose recorded ranking does not recompute from its own objective,
> constraints and scores is reported, and the recompute runs only on a
> complete, well-formed record; (f) a selected partition the recorded scores
> do not rank first is reported, and the SAME record with an override naming
> that choice is silent; (g) a finding warns plain and fails under --strict;
> (h) a project declaring no components, and the shipped example -000 rows,
> are vacuous.

`expected` and `evidence`: unchanged (the evidence already names the ten
tests).

## D11: the legacy readers leave the core (§10.7 item 8)

Built on `maint/vocabulary` (HANDOFF §9.14) as `D11-PLAN.md` drafted them.
Apply after the last migrator run, and accept in the one act that accepts
SR-247, LLR-369 and TC-427 (D18): a migrator run made after these are applied
would absorb them into the record without the act. The traced cells already
moved with the code (D4) and the record absorbed them: LLR-155 `module` and
`code_symbol`, LLR-156 `code_symbol`, LLR-246 `code_symbol` (`read_dial` is
`dial_from_config`), and the `evidence` of TC-150, TC-152 and TC-241. Only the
text cells below are left.

## 7. SR-139: the gate-policy word is not read

`acceptance_criteria`, full replacement:

> Level N holds exactly the tiers the shipped template documents (cumulative,
> strictly-less-than the stage); the terminal stage rung is held by no level,
> the end-of-run hold being its own dial; an unreadable stage, an absent dial,
> and a wrong-typed dial all read as operator-held; an out-of-range level falls
> back to the conservative end AND is refused loudly.

(The clause "a legacy gate-policy word reads as all three dials it meant" goes.
SR-138 already requires the fold to expand the word, and bootstrap's fold and
`--gate-policy` preset still do, from `GATE_POLICY_DIALS`.)

## 8. LLR-155: the dial-key rename left with bootstrap's step

`detail`: delete the last sentence, "A legacy dial key the migration cannot
rename in place is refused rather than altered." The migrator's Drafted rows
carry it now (LLR-369: a key the line edit cannot reach raises `Unsafe` and
the file is left; TC-427's inline-table case).

## 9. TC-150: the inline-table rename moved to the migrator

`method`, full replacement:

> Run the process-config suite over a duplicated declaration, wrong-typed dials
> and out-of-range dials, and valid policy files containing a dotted key, an
> inline table or a multi-line string. Assert each guarded entry point refuses
> a duplicated declaration by naming its key and both homes, that invalid
> values are refused rather than defaulted, and that valid TOML forms cause no
> configuration refusal.

## 10. TC-151: no legacy-word translation; a bare integer is malformed

`method`: delete "the legacy-word translation, " and add "a bare integer" to
the malformed inputs, so it reads:

> Run the acceptance-level suite: the full level x stage matrix against the
> ladder the shipped template documents, every malformed input (negative,
> out-of-range, a bare integer, string, float, bool, absent, unparseable), and
> the spine-stage corners (draft need, empty spine, uncited need, Modified SR,
> missing child, LLR-exempt SR).

## 11. LLR-156: one table for the preset and the fold

`detail`: the sentence "`LEGACY_ACCEPTANCE` is F5-duplicated from
`agent_common` (bootstrap imports no kit sibling — it must run standing on
nothing but the kit directory it copies FROM) and pinned equal by
`test_rule_sync`." becomes:

> `GATE_POLICY_DIALS` is the one statement of the three dials each word means:
> the `--gate-policy` preset writes them and the fold of a `docs/gate-policy`
> file writes them, and no other script holds a copy.

`rationale`, full replacement:

> One table for the preset and the fold means a repository scaffolded with a
> word and one folded from the same word get the same three dials. A copy that
> could disagree about what `single-approve` meant would let a repository
> scaffold with one posture and run with another, the shadowing defect the
> dial was introduced to remove.

## 12. TC-152: no ordinal step; the table pinned by meaning

`method`: delete "the ordinal migration ignores a string decoy; " and replace
"that the F5 translation tables are pinned equal" with "that each gate-policy
word lands the three dials it always meant", so it reads:

> Run the migration and bootstrap writer cases: a full conversion deletes every
> legacy file and lands all three acceptance dials; a second pass is a no-op; a
> hand-trimmed process.toml leaves the legacy file in place with its value
> intact; an inline table, dotted key, key-like line inside a multi-line
> string, and an unparseable policy file each refuse an unconfirmable in-place
> write without changing the file; a refused migration keeps its legacy file;
> and an ordinary policy file still migrates and accepts an in-place update.
> Assert that a scaffold flag reports refusal without a value it did not
> write, that each gate-policy word lands the three dials it always meant, and
> that the retired enum key is absent from the shipped template.

(The evidence already names `test_each_gate_policy_word_lands_the_three_dials_it_always_meant`
in place of `test_the_legacy_acceptance_translation_agrees`, and no longer the
two bootstrap dial-step tests.)

## 13. LLR-246: the live reader translates nothing

`detail`: "translating each legacy spelling exactly as
agent_common.acceptance_through does and printing nothing" becomes:

> reading it as agent_common.acceptance_through does, an absent or
> unrecognised dial as the most-held rung, and printing nothing

## 14. TC-241: the dial is read silently, never translated

`method`: "never from the working file and translating each legacy spelling
silently." becomes:

> never from the working file, and printing nothing.

(The evidence already names
`test_the_live_dial_reads_the_current_spelling_silently_from_a_chosen_tree`.)

## 15. LLR-038 (optional): the step's stage key

`detail`: "(gates = DevStg-Impl," becomes "(from-stage = DevStg-Impl,". The
text was already stale: `docs/stack.ini` declares `[step:doc-refs]` with
`from-stage`, and a `gates =` list is now refused.
