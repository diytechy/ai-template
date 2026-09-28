# The OI-37 absolutes sweep — needs, then requirements

**Status: SWEEP RECORD** (WI-616, absorbing WI-617), taken with the absolute-term
check this lane added (`project-trajectory/scripts/absolute_terms.py`, design row
LLR-274) over the registries at trunk `0ded5c77`. It answers WI-617's three
Done-when items: every absolute the check reports in a need, and then in a
requirement, classified with a one-line reason; the rewrites routed for approval;
and the open-world absolutes that are really premises listed for the assumption
tier's C2 (WI-655), not written into it. The design question it came from is
[the owner-notes plan §1.1](2026-09-23-owner-notes-spine-sessions-and-tests.md#11-absolutes-note-0).

## How to read it

The check reports an absolute whose domain names nothing from its closed word
list (a registry and its row nouns, an id, a declared set). It is lexical, so a
report is a question, not a verdict; the classes below are the answers.

| Class | Meaning | What happens to the cell |
|---|---|---|
| **C** | Closed: the absolute ranges over a domain the system controls or declares, which the word list cannot see (its own sessions, commits, scripts, emitted views, declared platforms). It is the invariant, finite and checkable. | Stands. |
| **E** | Not a promise over a domain: a disclaimer, an explanation, or a case description the tokenizer read as a universal. | Stands. |
| **B** | Open world or open time, unwarranted: bounded by a rewrite in this lane. | Amended, for approval. |
| **M** | A prohibited mechanism in a need: a design decision, moved down a tier (a requirement already carries it). | Amended, for approval. |
| **A** | Open world, and really a premise about something outside the system (a person, an adopter, a platform). | Listed for C2 below; the cell is left for C2 to bound once the premise has its row. |

Counts: needs 48 reported (33 C, 4 E, 3 B, 3 M, 5 A); requirements 166 reported
(160 C, 4 E, 2 A). Three C entries are closed normative obligations the
tokenizer reads as case descriptions: SR-137's "no dotted keys", SR-144's
"merges like any other branch" and SR-177's "no threshold" are each an enforced
obligation over a declared set, not an explanation. The requirement tier's closed share is the check's measured
precision on that tier: its word list names the kit's registries, not the system's
own nouns, and a project's nouns are the reader's call, not the list's.

## The rewrites, for the approval route

Needs go to the owner's brief (`human_approval_through` holds the need tier).
Each is an in-place amendment of an Approved row; the status stays Approved and
the snapshot records the drift until the brief is ruled.

| Need | Cell | Before | After | Class |
|---|---|---|---|---|
| SN-003 | `need` | "A team in any language can use this process: it is **stack-agnostic**, ..." | "A team can use this process on a stack whose tools it declares in a stack profile: it is **stack-agnostic**, ..." | B |
| SN-008 | `need` | "... and a pass verdict never hides a skipped check, a stub, or an unmet criterion." | "... and a pass verdict never hides a skipped check, a stub, or an unmet declared criterion." | B |
| SN-009 | `need` | "... it is caught before it publishes, in **every** repo, without extra setup." | "... in a repository that adopts this process, it is caught before it publishes, without extra setup." | B |
| SN-025 | `acceptance` | "A plain launch derives what to do next from the tracked WI DAG plus Git — never from prose or a hand-maintained pointer, and never from predefined tracks; ...; the status surface a human reads is generated, never hand-copied." | "A plain launch derives what to do next from the tracked WI DAG plus Git alone; ...; the status surface a human reads is generated from that tracked state." | M (SR-148 states "no prose surface and no predefined track in the derivation, no hand-curated next-work ... pointer") |

**No requirement is rewritten.** Every requirement absolute the check reports
ranges over the system's own behaviour or a declared set (C), is not a promise
over a domain (E), or is a premise already stated on its row and listed for C2
(A: SR-017, SR-019, whose own text records the hook as bypassable and pairs it
with the hosted re-run). None was an unwarranted open-world promise to bound in
place, so there is nothing to send the adjudicator from this sweep.

## Listed for C2 (WI-655): open-world absolutes that are premises

Each is a premise about a party outside the system. C2 decides whether it earns
an assumption row, with the falsifying observation this list suggests; the cells
are left as they are until it does.

| From | Absolute | The premise | What would show it false |
|---|---|---|---|
| SN-007 `need` | "through every change" | Changes reach trunk only through the gated path; a maintainer can bypass the hooks and a hand merge skips the merge slot. | A trunk commit whose tree fails the declared bar, or a merge with no slot record. |
| SN-009 `acceptance`; SR-017, SR-019 `requirement` | "every commit's staged diff" | Contributors commit and push through the installed hooks; a bypassed pre-push hook publishes before the hosted re-run can catch the secret. | A pushed commit carrying a secret-class match the hook would have refused. |
| SN-027 `acceptance` | "every finished branch lands through one serial, fail-closed integrator" | A person does not hand-merge a loop lane; when one does, the merge-slot sweep is run after it. | A merged lane with no merge-slot intake rows. |
| SN-028 `acceptance` | "an adopter never meets that refusal unaided" | Adopters upgrade through bootstrap or the documented re-sync, which run the migration. | An adopter report of the legacy-file refusal after a hand-copied upgrade. |
| SN-041 `need` | "what each part does and why it exists" | A sampled part's readability stands for the rest (C2 already plans this as SN-041's sampled assumption row). | A sampled reader failing on a part the sample did not reach. |

Beside the list, and not a reported absolute: SR-034's "a clean Python 3.11+"
is open-ended in time (interpreter releases after the CI matrix's sampled
versions), a premise of the same kind.

## Needs: every reported absolute, classified

| # | Row | Cell | Absolute (as reported) | Class | Reason |
|---|---|---|---|---|---|
| 1 | SN-001 | `acceptance` | never clobbers the repo | C | the re-sync's own writes; which files are the repo's own is declared by the kit/project ownership split |
| 2 | SN-002 | `acceptance` | any stage | C | the declared stage ladder |
| 3 | SN-003 | `need` | any language can use | B | open world: languages the kit has never met; rewritten to a stack whose tools the team declares in a stack profile, which is what the kit offers |
| 4 | SN-004 | `acceptance` | never silently skips | C | the harness's own runs on a declared condition; restates "fails" |
| 5 | SN-005 | `acceptance` | never replace it | C | the per-agent configs the kit ships (a declared set) |
| 6 | SN-005 | `acceptance` | every input | E | named in order to exclude it: the acceptance puts full local-CI equivalence outside the claim |
| 7 | SN-006 | `need` | never waits for interactive | C | the unattended run's own execution, stdin closed by the coordinator |
| 8 | SN-006 | `need` | never one the model | C | the declared override channels the limits read |
| 9 | SN-006 | `acceptance` | each end state | C | the loop's declared typed end states |
| 10 | SN-006 | `acceptance` | no agent cli | E | one enumerated preflight case in a parenthesis, not a universal |
| 11 | SN-006 | `acceptance` | every spawned worker and | C | workers the loop spawns and actions it takes, the system's own |
| 12 | SN-006 | `acceptance` | never when its own | C | the run's own surfacing behaviour |
| 13 | SN-007 | `need` | every change | A | open time and outside actors: holds only for changes that land through the gated path; hooks can be bypassed and a hand merge skips the slot |
| 14 | SN-007 | `acceptance` | every delivered script | C | the shipped-file inventory |
| 15 | SN-008 | `need` | never hides a skipped | B | open world: "an unmet criterion" ranges over criteria nobody declared; rewritten to an unmet declared criterion |
| 16 | SN-008 | `acceptance` | never a ci gate | C | the declared gate and CI defaults |
| 17 | SN-009 | `need` | every repo | B | open world, the plan's own example; rewritten to a repository that adopts this process |
| 18 | SN-009 | `acceptance` | every commit s staged | A | commits and pushes made through the installed hooks; a bypassed pre-push hook publishes before the hosted re-run can catch it |
| 19 | SN-010 | `acceptance` | every generated artifact carries | C | the declared generator set |
| 20 | SN-011 | `need` | every check on a | C | the kit's declared checks |
| 21 | SN-011 | `acceptance` | every non-stdlib import in | C | imports in the shipped scripts (closed source tree) |
| 22 | SN-011 | `acceptance` | every adopter to install | E | explanatory: why the shipped tier stays stdlib-preferred, true by construction of a hard dependency |
| 23 | SN-024 | `need` | never by the session | C | the loop's own session assignment (an authority constraint) |
| 24 | SN-025 | `acceptance` | never from prose or | M | a prohibited mechanism in a need; the outcome now reads "from the tracked graph plus Git alone" and SR-148 carries the prohibition |
| 25 | SN-025 | `acceptance` | never from predefined tracks | M | same; SR-148 states "no predefined track in the derivation" |
| 26 | SN-025 | `acceptance` | never hand-copied | M | the contrast of "generated", a mechanism; the need now asks for a status generated from the tracked state |
| 27 | SN-026 | `acceptance` | every selection before launch | C | the coordinator's own model selections |
| 28 | SN-026 | `acceptance` | never a silent model | C | restates that selections are logged |
| 29 | SN-027 | `acceptance` | every finished branch lands | A | holds for lanes the loop merges; a person's hand merge bypasses the integrator (the case the merge-slot sweep recovers) |
| 30 | SN-027 | `acceptance` | any lifecycle boundary recovers | C | the loop's declared lifecycle boundaries |
| 31 | SN-028 | `acceptance` | every shape only one | E | explanatory: why the shape is a checked contract, over the two declared grammars |
| 32 | SN-028 | `acceptance` | never meets that refusal | A | adopters who upgrade through bootstrap or the documented re-sync; a hand-copied upgrade meets the refusal unaided |
| 33 | SN-029 | `acceptance` | every failure direction | C | the failure directions the dash enumerates |
| 34 | SN-029 | `acceptance` | each acceptance is anchored | C | recorded acceptance acts |
| 35 | SN-029 | `acceptance` | any status movement | C | the closed Status vocabulary |
| 36 | SN-034 | `need` | each of the two | C | the two enumerated contributor actions |
| 37 | SN-034 | `acceptance` | each supported platform in | C | the declared supported platforms |
| 38 | SN-034 | `acceptance` | each launches its action | C | the declared entry points |
| 39 | SN-035 | `need` | each platform this repository | C | the declared supported platforms |
| 40 | SN-036 | `acceptance` | each decomposition has a | C | recorded decompositions (SN to SR derivations) |
| 41 | SN-037 | `need` | each promised system behavior | C | the requirement registry |
| 42 | SN-037 | `acceptance` | every system-requirement input and | C | the requirement registry's input and output references |
| 43 | SN-038 | `need` | every file supplied by | C | the shipped-file inventory |
| 44 | SN-041 | `need` | each part does and | A | the acceptance samples a part; that a sampled part stands for the rest is the premise (C2's planned sampled assumption row) |
| 45 | SN-041 | `acceptance` | each change is measured | C | changes submitted for acceptance through the declared gate |
| 46 | SN-042 | `need` | every required behavior being | C | requirements approved after adoption, as the acceptance bounds it |
| 47 | SN-043 | `need` | each of those premises | C | the assumption registry |
| 48 | SN-043 | `acceptance` | each premise shows whether | C | the assumption registry |

## Requirements: every reported absolute, classified

| # | Row | Cell | Absolute (as reported) | Class | Reason |
|---|---|---|---|---|---|
| 1 | SR-006 | `requirement` | every non-freshness step still | C | the gate's declared step plan |
| 2 | SR-006 | `acceptance_criteria` | never a silent pass | C | the harness's own runs on a declared condition; restates "fails" |
| 3 | SR-006 | `acceptance_criteria` | every non-freshness step still | C | the gate's declared step plan |
| 4 | SR-006 | `acceptance_criteria` | never skips them | C | the declared lanes (trunk vs claimed branch) |
| 5 | SR-007 | `acceptance_criteria` | each step s command | C | the declared stack profile's steps |
| 6 | SR-010 | `acceptance_criteria` | every delivered script against | C | the shipped-file inventory (delivered scripts) |
| 7 | SR-011 | `acceptance_criteria` | every existing file | C | the files present at re-run time in the destination; the operation's own writes |
| 8 | SR-017 | `requirement` | every commit s staged | A | commits made through the installed hook; a bypassed hook is the premise, which SR-019 already records as bypassable |
| 9 | SR-019 | `requirement` | every commit | A | same premise as SR-017; the row itself states the bypass and the hosted pair |
| 10 | SR-019 | `requirement` | never alone | E | a disclaimer: the row says the hook alone does not discharge the claim |
| 11 | SR-020 | `acceptance_criteria` | always | C | a declared mode: secrets are scanned whatever the privacy dial says |
| 12 | SR-026 | `requirement` | never blocking on a | C | the coordinator's own session launches (stdin closed) |
| 13 | SR-026 | `requirement` | never a session input | C | one declared generated artifact |
| 14 | SR-026 | `acceptance_criteria` | every mode runs with | C | the coordinator's declared modes |
| 15 | SR-028 | `requirement` | each session in a | C | the coordinator's own sessions |
| 16 | SR-031 | `requirement` | every other enforcer | C | the declared dial enforcers (a closed set of readers in the kit) |
| 17 | SR-031 | `acceptance_criteria` | every enforcer reads the | C | the declared dial enforcers |
| 18 | SR-033 | `requirement` | never fail a gate | C | the declared warn tier of the budget registry |
| 19 | SR-034 | `requirement` | every kit script shall | C | the shipped kit scripts (inventory) |
| 20 | SR-034 | `acceptance_criteria` | every kit script s | C | the shipped kit scripts (inventory) |
| 21 | SR-040 | `requirement` | each in-process session phase | C | the declared session phases |
| 22 | SR-043 | `requirement` | any error so a | C | the gate's own code paths (it catches its own errors by construction) |
| 23 | SR-043 | `requirement` | never wedges the tools | C | the gate's own failure behaviour |
| 24 | SR-049 | `requirement` | never accepting a hand-set | C | the stage derivation's inputs (a derived cell, never a hand-set one) |
| 25 | SR-049 | `requirement` | never hides | C | the derived stage's own report surface |
| 26 | SR-052 | `requirement` | every interactive element | C | the elements the generator emits (a closed output) |
| 27 | SR-052 | `requirement` | no information is encoded | C | the generator's emitted encodings |
| 28 | SR-052 | `acceptance_criteria` | every interactive element | C | the elements the generator emits |
| 29 | SR-052 | `acceptance_criteria` | every interactive element announces | C | the elements the generator emits |
| 30 | SR-052 | `acceptance_criteria` | every status | C | the status/phase/type encodings the generator emits |
| 31 | SR-052 | `acceptance_criteria` | every emitted view | C | the views the generator emits; the sweep is over the whole closed output by design |
| 32 | SR-052 | `acceptance_criteria` | never a sampled subset | C | restates that the sweep is exhaustive over a closed output |
| 33 | SR-053 | `acceptance_criteria` | every tab | C | the tabs, views and emitters the generator emits |
| 34 | SR-053 | `acceptance_criteria` | every font size resolves | C | the emitted font sizes against the declared type scale |
| 35 | SR-053 | `acceptance_criteria` | every spacing value to | C | the emitted spacing values against the declared rhythm |
| 36 | SR-053 | `acceptance_criteria` | every status | C | the emitted encodings against the declared colour vocabulary |
| 37 | SR-053 | `acceptance_criteria` | every emitter | C | the generator's emitters (a new one joins by existing) |
| 38 | SR-054 | `requirement` | each within one tab | C | the three enumerated reading tasks |
| 39 | SR-054 | `acceptance_criteria` | each core reading task | C | the core reading tasks the row enumerates |
| 40 | SR-054 | `acceptance_criteria` | every view whose element | C | views over the declared threshold |
| 41 | SR-054 | `acceptance_criteria` | any oversized view starting | C | a failure condition over the emitted views, judged by inspection |
| 42 | SR-054 | `acceptance_criteria` | any lost return path | C | a failure condition over the emitted views |
| 43 | SR-054 | `acceptance_criteria` | any illegible label is | C | a failure condition over the emitted labels |
| 44 | SR-070 | `requirement` | each artifact it produces | C | the generator set's own outputs |
| 45 | SR-129 | `requirement` | any conversion attempted while | C | conversions the harness itself attempts |
| 46 | SR-137 | `requirement` | no dotted keys | C | a closed normative obligation: an enforced shape prohibition over the one declared dial file's grammar |
| 47 | SR-137 | `requirement` | never resolving by precedence | C | the declared dial file's reading rule |
| 48 | SR-138 | `requirement` | every legacy one-word policy | C | the legacy policy files the kit shipped (a closed, known set) |
| 49 | SR-138 | `requirement` | never deleting a file | C | the fold's own writes |
| 50 | SR-139 | `requirement` | every unreadable or out-of-range | C | the declared approval inputs (stage, level, dial) |
| 51 | SR-139 | `acceptance_criteria` | all read as human-held | C | the three enumerated inputs |
| 52 | SR-140 | `requirement` | each acceptance as a | C | the recorded approval acts |
| 53 | SR-140 | `acceptance_criteria` | never rode a record | E | a case description (an approval with no record) inside the acceptance |
| 54 | SR-178 | `requirement` | any recorded artifact whose | C | recorded artifacts with an acceptance copy (the snapshot tree) |
| 55 | SR-178 | `requirement` | any status movement | C | the Status vocabulary (closed) |
| 56 | SR-178 | `acceptance_criteria` | never read as the | C | the Status cell's own reading rule |
| 57 | SR-144 | `requirement` | any other branch | C | a closed normative obligation: the partial close merges through the same declared merge path as the loop's other lane branches |
| 58 | SR-144 | `acceptance_criteria` | every report it wrote | C | the reports the close itself wrote |
| 59 | SR-146 | `requirement` | every prompt the delivered | C | the prompts the loop launches (the shipped prompt catalogue) |
| 60 | SR-146 | `requirement` | each session recording which | C | the loop's own sessions |
| 61 | SR-146 | `acceptance_criteria` | every shipped prompt with | C | the shipped prompt catalogue |
| 62 | SR-148 | `requirement` | any live instruction or | C | live instruction and executable surfaces of the kit (closed tree) |
| 63 | SR-148 | `acceptance_criteria` | every other class | C | the ruled rank table's classes |
| 64 | SR-148 | `acceptance_criteria` | each higher level holds | C | the declared approval levels |
| 65 | SR-148 | `acceptance_criteria` | every selection records the | C | the scheduler's own selections |
| 66 | SR-148 | `acceptance_criteria` | no prose surface participates | C | the derivation's declared inputs; the prohibition sits at SR tier, where SN-025's mechanism now lives |
| 67 | SR-148 | `acceptance_criteria` | no live instruction or | C | the kit's live surfaces (closed tree) |
| 68 | SR-149 | `requirement` | every occurrence of a | C | the declared retired tags over the live authored surfaces |
| 69 | SR-150 | `acceptance_criteria` | each offending phrase separately | C | the phrases the need-form check finds in one planted cell |
| 70 | SR-152 | `requirement` | each step s outcome | C | the harness's declared steps |
| 71 | SR-154 | `requirement` | every selection logged before | C | the coordinator's own model selections |
| 72 | SR-154 | `acceptance_criteria` | never a silent skip | C | restates the declared degrade to the documented mode |
| 73 | SR-154 | `acceptance_criteria` | every selection is logged | C | the coordinator's own model selections |
| 74 | SR-154 | `acceptance_criteria` | never a silent model | C | restates that selections are logged |
| 75 | SR-156 | `requirement` | every lane back to | C | the loop's own lanes (the integration seam the loop runs) |
| 76 | SR-156 | `requirement` | any crash boundary | C | the loop's declared lifecycle boundaries |
| 77 | SR-156 | `acceptance_criteria` | any lifecycle boundary recovers | C | the loop's declared lifecycle boundaries |
| 78 | SR-157 | `acceptance_criteria` | each recorded at its | C | the declared rule inventory's declaration sites |
| 79 | SR-158 | `requirement` | each class | C | the declared finding classes |
| 80 | SR-158 | `acceptance_criteria` | each class s declaration | C | the declared finding classes |
| 81 | SR-158 | `acceptance_criteria` | never gating | C | the declared severity of untraced references |
| 82 | SR-160 | `requirement` | each supported platform | C | the declared supported platforms |
| 83 | SR-160 | `requirement` | each starting its action | C | the declared entry points |
| 84 | SR-160 | `acceptance_criteria` | each carry both launcher | C | the fresh scaffold and this repository (two named trees) |
| 85 | SR-160 | `acceptance_criteria` | each launches its action | C | the declared entry points |
| 86 | SR-160 | `acceptance_criteria` | each root launcher reports | C | the declared root launchers |
| 87 | SR-161 | `requirement` | every decomposition it produces | C | decompositions the planning content produces |
| 88 | SR-162 | `requirement` | every system-requirement boundary reference | C | requirement boundary references (a registry cell) |
| 89 | SR-162 | `requirement` | each as an advisory | C | the enumerated finding kinds, each an advisory |
| 90 | SR-162 | `acceptance_criteria` | each one advisory line | C | the three enumerated counts |
| 91 | SR-163 | `requirement` | every file the delivered | C | shipped files, through the declared inventory |
| 92 | SR-163 | `acceptance_criteria` | each reported | C | the four enumerated finding classes |
| 93 | SR-165 | `requirement` | each candidate s score | C | candidates the decomposition run recorded |
| 94 | SR-165 | `requirement` | any of those elements | C | the enumerated record elements |
| 95 | SR-165 | `acceptance_criteria` | any candidate s score | C | the recorded candidates |
| 96 | SR-166 | `requirement` | every file the manifest | C | the manifest's declared rows |
| 97 | SR-166 | `requirement` | each failing rather than | C | the two enumerated failure kinds |
| 98 | SR-168 | `acceptance_criteria` | each reachable within the | C | the enumerated reading content of the view |
| 99 | SR-169 | `acceptance_criteria` | each visible level | C | the rendered containment levels |
| 100 | SR-170 | `requirement` | never from a parallel | C | the declared merge step versus work branches (closed set of writers) |
| 101 | SR-170 | `acceptance_criteria` | never committed from a | C | the loop's own writers |
| 102 | SR-173 | `acceptance_criteria` | every consumer that reads | C | the declared artifact families and their declared order |
| 103 | SR-174 | `requirement` | each work-item identity at | C | the work-item id space |
| 104 | SR-174 | `requirement` | never re-issued | C | the work-item id space |
| 105 | SR-175 | `requirement` | each dispatched brief | C | the loop's dispatched brief classes (declared) |
| 106 | SR-175 | `acceptance_criteria` | each brief class the | C | the loop's declared brief classes |
| 107 | SR-175 | `acceptance_criteria` | never as filtered | C | the declared pull channel's presentation |
| 108 | SR-176 | `requirement` | any durable record the | C | durable records the kit itself produces |
| 109 | SR-176 | `requirement` | never by the matched | C | the kit's own finding records |
| 110 | SR-176 | `acceptance_criteria` | any tracked artifact after | C | tracked artifacts (the repository's git tree) |
| 111 | SR-176 | `acceptance_criteria` | never the matched text | C | the kit's own finding records |
| 112 | SR-177 | `acceptance_criteria` | no threshold | C | a closed normative obligation: the advisory's declared warn-only boundary (no threshold, no exit-code change) |
| 113 | SR-177 | `acceptance_criteria` | always visible | C | the loop's own serial-lane report line |
| 114 | SR-180 | `acceptance_criteria` | all fail to resolve | C | the named symbols of one row |
| 115 | SR-180 | `acceptance_criteria` | any one of them | C | the units one row names |
| 116 | SR-181 | `acceptance_criteria` | any strict exit | C | the declared strict exits |
| 117 | SR-182 | `requirement` | never gating a bar | C | the harness's own gating bars |
| 118 | SR-182 | `acceptance_criteria` | any count above baseline | C | counts against the stamped baseline |
| 119 | SR-182 | `acceptance_criteria` | any count below baseline | C | counts against the stamped baseline |
| 120 | SR-182 | `acceptance_criteria` | no baseline yet | E | a case description (an unstamped repository) |
| 121 | SR-182 | `acceptance_criteria` | every one of those | C | the enumerated cases |
| 122 | SR-183 | `requirement` | each source function s | C | source functions under the declared source tree |
| 123 | SR-183 | `requirement` | any divergence from that | C | divergences from the stamped baseline |
| 124 | SR-183 | `acceptance_criteria` | every function whose cognitive | C | functions under the declared source tree |
| 125 | SR-183 | `acceptance_criteria` | never graded | C | the reported public-symbol count |
| 126 | SR-183 | `acceptance_criteria` | each reported as a | C | the two enumerated finding kinds |
| 127 | SR-183 | `acceptance_criteria` | every one of those | C | the enumerated cases |
| 128 | SR-183 | `acceptance_criteria` | no per-site suppression is | C | the declared source tree's comments |
| 129 | SR-184 | `requirement` | each verdict and finding | C | verdicts and findings in one acceptance record |
| 130 | SR-184 | `acceptance_criteria` | every verdict and finding | C | verdicts and findings in one acceptance record |
| 131 | SR-184 | `acceptance_criteria` | never the adequacy of | C | scopes the judgement to the record, excluding artifact adequacy |
| 132 | SR-185 | `acceptance_criteria` | every reviewed change that | C | reviewed changes in the review record (recorded acts) |
| 133 | SR-191 | `acceptance_criteria` | every other approval of | C | approvals of approved content (recorded acts) |
| 134 | SR-192 | `requirement` | each stand-in that answers | C | stand-ins used in the project's own tests (declared surrogate rows) |
| 135 | SR-198 | `acceptance_criteria` | each declares the inputs | C | observation test cases in the registry |
| 136 | SR-199 | `requirement` | each observation result apart | C | observation results the writer records |
| 137 | SR-199 | `acceptance_criteria` | any of these | C | the enumerated record fields |
| 138 | SR-199 | `acceptance_criteria` | never read as a | C | the checker's reading rule for a partial record |
| 139 | SR-202 | `acceptance_criteria` | any later change to | C | the enumerated triggers (a failed sample, a changed bound text) |
| 140 | SR-202 | `acceptance_criteria` | never reopens it | C | the declared triggers; time alone is excluded |
| 141 | SR-209 | `acceptance_criteria` | every process the loop | C | processes the loop itself starts |
| 142 | SR-209 | `acceptance_criteria` | any commit one of | C | commits the loop's own writers made |
| 143 | SR-209 | `acceptance_criteria` | every commit of a | C | commits in a loop lane's range |
| 144 | SR-210 | `requirement` | each commit carrying the | C | commits in the committed history carrying the trailer |
| 145 | SR-210 | `acceptance_criteria` | each commit carrying the | C | commits in the committed history carrying the trailer |
| 146 | SR-212 | `acceptance_criteria` | any other fails the | C | the declared boundary rule's cases |
| 147 | SR-216 | `requirement` | each measure and part | C | the declared measures and the touched parts |
| 148 | SR-216 | `acceptance_criteria` | each measure the project | C | the declared measures |
| 149 | SR-216 | `acceptance_criteria` | each against its own | C | each declared measure's stamped baseline |
| 150 | SR-216 | `acceptance_criteria` | every worsening any of | C | the declared measures' findings |
| 151 | SR-216 | `acceptance_criteria` | any of them finds | C | the declared measures |
| 152 | SR-217 | `acceptance_criteria` | never as a pass | C | the declared history-reading outcome |
| 153 | SR-218 | `acceptance_criteria` | all coincident shows that | C | the requirements the registry holds for the need |
| 154 | SR-218 | `acceptance_criteria` | any color | E | redundant cue: status is marked in text as well as colour |
| 155 | SR-219 | `acceptance_criteria` | all belong to one | C | the declared crossings a requirement names |
| 156 | SR-219 | `acceptance_criteria` | each system | C | the two declared systems |
| 157 | SR-220 | `requirement` | any one state of | C | states of the queued work-item registry |
| 158 | SR-220 | `requirement` | each absorbed item is | C | items of the enacted consolidation |
| 159 | SR-220 | `acceptance_criteria` | no judgement is started | C | judgements the census starts (a case list follows, each refusal named) |
| 160 | SR-220 | `acceptance_criteria` | each refusal naming that | C | the refusals the census raises |
| 161 | SR-220 | `acceptance_criteria` | never itself a member | C | judgement rows in the registry |
| 162 | SR-220 | `acceptance_criteria` | never seeded by | C | items the registry records as judgement-created |
| 163 | SR-220 | `acceptance_criteria` | never re-absorbs | C | items created by an enacted judgement |
| 164 | SR-220 | `acceptance_criteria` | each absorbed item in | C | items of the enacted consolidation |
| 165 | SR-220 | `acceptance_criteria` | every item it supersedes | C | items the successor supersedes (registry cell) |
| 166 | SR-221 | `acceptance_criteria` | each refused with a | C | the declared module names |
