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
