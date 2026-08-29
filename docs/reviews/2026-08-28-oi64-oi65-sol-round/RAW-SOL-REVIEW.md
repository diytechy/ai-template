## 1. What is actually being decided

### OI-64

OI-64 asks whether all shipped checkers should follow one stated interface contract. That contract would cover finding location, severity labels, strict-mode behavior, missing optional inputs, exceptions, and exit codes. Several SR rows state parts of this behavior while describing different checks. The live choices are to add one shared interface definition and later remove duplicate wording, add it without cleaning existing SRs, or keep the rules local to each checker. The measurement option has already been completed. It found consistent advisory exit behavior, but inconsistent labels and strict-mode flags. OI-64 does not decide whether interface contracts live in registry cells or component headers; OI-65 does.

### OI-65

OI-65 first asks where interface facts not stated elsewhere should live: in each IF row or beside the component that implements the interface. It offers full relocation, no relocation, a family split, partial relocation, or a pricing step before commitment. Second, it asks what to do with ten passages left in `contract`: eight irrelevant or duplicated passages and two false claims. Third, it asks whether the 37 IF `rationale` cells should be linted and whether malformed `wI-280` references should be detected. It does not decide whether the checker protocol in OI-64 should exist. The two items are related, but they are not the same question.

## 2. Registry effect per option

The requested `software-requirements.toml` does not exist. The SR registry is `system-requirements.toml`. It contains 75 SRs; the LLR registry contains 187 rows; the IF registry contains 135 rows. All 13 SRs cited by OI-64 are `Approved`; all 135 IF rows are `Drafted`.

### OI-64

| Option | Actual effect |
|---|---|
| (a) | Self-contradictory. The option and blast-radius text say: add 1 SR, add an unspecified number of LLR/TC rows, later edit 13 Approved SRs, delete duplicate clauses, and change checker code/tests. The later owner direction instead says: add no SR or LLR and define 1 interface contract. The IF owner, endpoints, and SR-to-IF reference method are missing. |
| (b) | Same contradiction about the new row: the original text adds 1 SR plus unspecified LLR/TC rows; the owner direction implies 1 IF definition instead. It consolidates no existing SR. It still requires checker/test changes if the new contract includes a closed severity vocabulary or one strict-mode rule. |
| (d) | Adds no SR, LLR, or IF row; edits no requirement content; deletes nothing; changes no checker or test. Only the OI ruling record and log would change. |
| (c), completed | Added no row and changed no registry, checker, or test. It was a read-only measurement and is no longer a ruling choice. |

The claim that (b) costs “almost nothing” is wrong. A new closed vocabulary would require output and test changes. The measurement also found six finding sites without a complete location.

### OI-65 part 1: placement

| Option | Actual effect |
|---|---|
| (a) | Edits the 108 existing non-CLI IF rows and adds no SR, LLR, or IF row. It deletes the text judged to restate another source, formerly counted as 28,305 characters. No code or test changes. The count now needs remeasurement. |
| (b) | Edits the same 108 IF rows, moves contract facts from 71 of them into source headers, and adds no registry row. It also changes source docstrings, templates, process text, generator/check code, tests, a new generated reference, and its freshness check. The number of files and tests is not priced. |
| (b′) | Immediately adds 1 pricing WI, not an SR/LLR/IF row. It changes no interface cell or code until the estimate is accepted. It is internally inconsistent: it says the header direction is committed, but also says a high price can send the decision back to (a). |
| (c) | Edits all 108 IF rows. Under the original table it moves 2,180 characters from 16 of 19 former `Provides` rows to headers and keeps 6,795 characters from 55 of 89 former `Consumes` rows in cells. It adds no registry row but changes the same shipped header/generator/test surfaces as (b). Those character counts need remeasurement. |
| (e) | Edits an unspecified subset of existing IF rows and source headers; adds no registry row. The table marks 39 rows as containing at least one written-artifact or fail-loud clause, but gives no character count for those clauses. The option also conflicts with the blast-radius text over whether a generated reference and check are required. |

### OI-65 part 2: ten passages

| Option | Actual effect |
|---|---|
| (i) | Edits 10 existing Drafted IF rows. It deletes irrelevant or duplicated content from 8 and corrects `IF-061` and `IF-117`. It adds no row and changes no code/test. The replacement text for the two corrections is not specified. |
| (ii) | Adds no row. It changes the live and shipped `rationale` grammar and moves an unspecified subset of the ten passages into existing IF cells. This contradicts the claim that part 2 has “no kit surface.” It also fails to explain how moving text fixes the two false claims or the duplicate. |
| (iii) | Changes nothing. All ten passages remain, including the two false claims. |

### OI-65 part 3: lint

| Option | Actual effect |
|---|---|
| (iv) | Adds no registry row. It changes `trace.py`, `trace_text.py`, and tests. A read-only scan of the current 37 `rationale` cells finds 0 citation-frame findings; making WI matching case-insensitive would expose `wI-280` in `IF-082`, `IF-083`, and `IF-084`. Downstream repositories could receive additional warnings. |
| (v) | Changes nothing. IF `rationale` remains outside this lint, and the three malformed WI references remain invisible. |

## 3. Substantive check

### The 13 SR rows

The claim that 13 SRs restate one contract is not supported by the registry. They are mainly different obligations that use similar words for findings and severity.

- `SR-149`, `SR-150`, `SR-157`, `SR-158`, `SR-159`, `SR-162`, and `SR-163` contain recognizable shared protocol clauses. They still govern different checks and retain local severity decisions.
- `SR-167`, `SR-180`, `SR-181`, and `SR-182` make severity or exit behavior part of their main obligation. That text cannot simply be replaced with a citation without losing substantive behavior.
- `SR-015` does not state severity, strict mode, vacuity, carve-outs, or exit composition. Its acceptance merely says a broken PB reference “is a finding.” It does not belong in the list.
- `SR-164` requires an invalid scope value to be reported with the row id. It says nothing about severity or exit behavior. It does not belong in the list.

`SR-157` already states much of the proposed protocol for spine and work-registry checks: row attribution, declared severity, gating classes, advisory classes, and vacuity. Therefore “stated by none” is also too strong. What is absent is one package-wide rule covering every checker.

### SR-158

The quoted sentence exists in `SR-158`. The brief misreads it.

It says that a class is unsatisfied if its severity is stated at no declaration site. It does not say that this condition currently exists, or that one central requirement must be that declaration site. The same acceptance text points to per-class declaration sites, and the checker measurement found such local declarations. `SR-158` is also `Approved`. It does not currently declare itself unsatisfied.

### OI-64 measurement

The narrow claim that advisories do not affect the exit code holds. `trace.exit_code` uses named failure collections and excludes advisory collections. The cited case-sensitive search also produces 25 matches across seven modules.

The broader claim that “the protocol is honoured” needs qualification:

- Six finding sites have a location available but do not name it.
- Twelve labels describe four outcomes.
- Strict behavior uses six flag names, four checkers have no promotion path, and two use per-row controls.
- The “every degrade is named” clause was not measured.

The measurement supports a common protocol. It does not support one uniform implementation without code changes.

### OI-65 numbers

| Claim | Result |
|---|---|
| 8,975 remainder characters over 71 rows | The original per-row table sums to exactly 8,975 and 71. The row count survives. The character count does not: the record says character spans are judgment estimates, and its later addendum changes `IF-098` from 219 characters to either 166 or 81 without updating the total. `IF-061` is also reclassified. |
| 28,305 restatement characters | The original table sums to exactly 28,305. It is not a stable current total because the `IF-098` reclassification moves at least 53 characters from remainder to restatement. |
| 57 of 76 modules have an anchor | This was historical. The current source tree has 78 Python modules and 57 real lines beginning `Contracts: IF-`; the current figure is 57 of 78, leaving 21, not 19. |
| 36 rows changed; rationale usage 1 to 37 | Holds in the current registry. The 108 cleaned contract cells total 37,859 characters and 37 IF rows carry `rationale`. |

There is an additional source issue. `gen_arch_map.module_contracts` currently reports 58 modules with contracts because it treats this sentence in `handback.py` as a declaration: “No `Contracts:` line … IF-080.” The file explicitly says there is no declaration, but the parser extracts `IF-080`. The proposed header mechanism should not be priced on the assumption that the present harvester is already reliable.

The cleanup record also has a small arithmetic error: 6,715 estimated non-crossing characters minus 6,136 removed is 579, not the stated 679.

### Source checks

- `trace.py` defines `IF_REASON_CELLS = ("Notes", "SignalNote")`. Therefore the citation-frame lint does not inspect `Rationale`.
- “Nothing reads an IF rationale at all” is literally false. The registry loader parses and retains that field, and the shared schema declares it. The accurate statement is: no current IF content lint inspects its text.
- `trace_text.py` defines `_WI_TOKEN_RE` without `IGNORECASE`. It matches `WI-280` but not `wI-280` or `wi-280`. The brief is correct on this point.

### Sequencing

Ruling OI-65 before implementing OI-64 is sensible. It avoids defining the shared checker contract in a place that may immediately change.

It is not circular. OI-65 does not depend on whether OI-64 chooses a shared checker contract. OI-64 can also be ruled in principle first, provided implementation waits for OI-65. The brief should describe the order as avoiding rework, not as a logical prerequisite.

## 4. What to cut

The root problem is that both rows combine the decision, execution plan, historical record, and defense of the author’s reasoning.

### Cut from OI-64

- “Where this came from, and why it is not a worker’s call” — historical method.
- “The remap’s method is a blind re-derivation” — supporting-record summary.
- “Two agents ran it on deliberately different axes” — self-justification.
- “Both teams enumerated them independently” — keep the corrected row list, not the origin story.
- “The corpus concedes the hole in its own words” — rhetoric based on an incorrect reading of SR-158.
- “Three adjacent restatements the same teams counted” — adds an unmeasured fourth subject to this decision.
- “What is not being proposed” — process defense.
- “The measurement is run” and “Method: an AST census” — replace with four result bullets and a link to the record.
- “What it costs to leave it” — remove the named “failure class”; keep one sentence about new checkers being unconstrained.
- “Owner direction … recorded verbatim” — keep the one-definer rule, not the transcript.
- “The pre-measurement recommendation” — obsolete history; delete the entire retained block.
- “What the program will not do without a ruling” — implementation discipline, not ruling information.

### Cut from OI-65

- “Why this row exists at all” — filing history.
- “That is the failure OI-62 named” — rhetoric.
- “What has changed since OI-63 was ruled” — replace the repeated changed/not-changed framing with three current facts.
- The long quote beginning “note that C says” — replace with: files and external boundaries can have an owning contract.
- “Not changed — the sizes” — the exact numbers are no longer reliable.
- “Not changed — the rot exposure” — the ten-row section already names the affected rows.
- “Which options cross the kit line” — shorten to one concrete file/code list under each affected option.
- “What it costs to leave it” — shorten to one sentence.
- “Small but shipped” — rhetoric; state the code and downstream-warning effect directly.
- The repeated `FOR`/`AGAINST` paragraphs — replace with action, registry effect, and cost.
- “Placement. The field is now” — long recommendation defense.
- “The sequencing claim, stated so it can be disagreed with” — replace with one sentence about avoiding rework.

### Missing information

Before OI-64 can be implemented, the owner needs:

1. The proposed IF row’s provider, consumers, owner, and `req_refs`.
2. The exact shared contract text and chosen severity vocabulary.
3. The exact SR clauses to remove. The current count of 13 is not valid.
4. A legal SR-to-IF reference method; SR rows have no IF-reference field.
5. A code/test estimate for label changes, strict flags, and six incomplete locations.
6. A decision on whether the unmeasured “every degrade is named” rule is in scope.

Before OI-65 part 1 can be ruled for headers, the owner needs:

1. The generated artifact’s name and format.
2. Which component headers will change.
3. The freshness check and downstream migration.
4. A corrected current character count.
5. A fix for the negated `Contracts:` false positive.
6. A cost threshold for (b′), and whether that option is binding or provisional.
7. The corrected text for `IF-061`, `IF-117`, and the separately recorded false universal in `IF-050`.

## 5. A rewrite

### OI-64

```toml
one_line = """Decide whether all shipped checkers should use one shared interface contract for finding location, severity labels, missing optional inputs, and exit codes. Existing SR rows describe different checks; some repeat parts of this shared behavior."""

options = """- (a) Do add one shared IF definition and remove only wording that it replaces. This adds 1 interface definition, consolidates an unconfirmed subset of 13 Approved SR rows, and changes checker code and tests. Cost: define the IF owner and endpoints, choose the severity words, identify the exact SR clauses, fix 6 incomplete location messages, and reapprove every changed SR.
- (b) Do add the same shared IF definition but leave the existing SR text unchanged. This adds 1 interface definition, consolidates no existing row, and still changes checker code and tests to meet the chosen contract. Cost: the duplicate wording remains and can conflict with the new definition; the IF owner, endpoints, and severity words still need definition.
- (c) Do measure checker behavior before ruling. This adds or consolidates nothing and changes no code or tests. Cost: already paid; the result found consistent advisory exit behavior, 12 severity labels, 6 incomplete locations, and several strict-mode mechanisms.
- (d) Do keep each checker's protocol local. This adds or consolidates nothing and changes no checker code or tests. Cost: no package-wide rule controls a new checker, but each check's local severity and exit behavior remains explicit."""

recommendation = """Recommend (a), but do not implement it from the present brief. Rule OI-65 first, then specify the IF owner, endpoints, severity vocabulary, and exact SR clauses to remove. Keep local severity and exit rules where they are part of the check's main obligation. Do not include SR-015 or SR-164 in the consolidation based on their current text."""
```

### OI-65

```toml
one_line = """Decide whether interface facts not stated elsewhere stay in the 108 IF contract cells or move beside the component that implements them. Also decide how to fix ten remaining irrelevant or false passages and whether to lint the 37 IF rationale cells."""

options = """Part 1 - placement

- (a) Do keep these facts in the IF contract cells and remove duplicated text there. This consolidates 108 existing IF rows and adds no SR, LLR, or IF row; code and tests do not change. Cost: edit 108 Drafted rows; the old estimate of 28,305 deleted characters must be remeasured.
- (b) Do move these facts to structured component headers, generate a committed reference, and check its freshness. This consolidates 108 existing IF rows, adds no SR, LLR, or IF row, and changes source headers, generator and check code, tests, templates, and one generated artifact. Cost: an unpriced kit-wide migration; the old 8,975-character estimate is not exact, and the current tree has 57 real anchors across 78 modules.
- (b') Do provisionally choose component headers and price the build before moving text. This adds 1 pricing WI and changes no SR, LLR, IF row, code, or test until the owner accepts the estimate. Cost: another owner decision; state the cost limit and whether exceeding it returns the choice to (a).
- (c) Do move facts for the 19 former Provides rows and keep facts for the 89 former Consumes rows in their cells. This consolidates all 108 IF rows, adds no registry row, and changes the same shipped header, generator, and test surfaces as (b) for the header side. Cost: two writing rules based on a deleted registry distinction; the old table places header text on 16 rows and 2,180 characters, but that count must be remeasured.
- (e) Do move only written-output and fail-loud clauses to component headers. This changes an unconfirmed subset of existing IF rows and the shipped header convention, and adds no SR, LLR, or IF row. Cost: 39 rows contain at least one such clause, but mixed clauses and character counts are not defined, and the artifact and check scope is unclear.

Part 2 - ten passages

- (i) Do delete the eight irrelevant or duplicated passages and correct IF-061 and IF-117. This edits 10 existing Drafted IF rows, deletes content from 8, corrects 2, and adds no row or code change. Cost: specify the true replacement text for the two corrections.
- (ii) Do allow citations in IF rationale and move the cited text there. This changes the current and shipped rationale grammar and edits an unspecified subset of the 10 IF rows; it adds no row. Cost: it does not correct the two false claims or remove the duplicate, and it conflicts with the current no-history rule.
- (iii) Do leave the ten passages where they are. This changes nothing. Cost: eight irrelevant or duplicated passages and two false claims remain in live contract cells.

Part 3 - rationale checks

- (iv) Do lint IF rationale and match WI ids without case sensitivity. This changes trace.py, trace_text.py, and tests and adds no registry row. Cost: downstream repositories may receive new warnings; the current 37 rationale cells produce none, while IF-082, IF-083, and IF-084 would expose wI-280.
- (v) Do leave the checks as they are. This changes nothing. Cost: IF rationale remains unchecked and the three malformed WI references remain invisible."""

recommendation = """Recommend (b') only as a pricing step, followed by a final choice between (a) and (b). The estimate must name the generated artifact, freshness check, source headers, migration work, and cost limit. Recommend (i) for the ten passages and (iv) for the checks. Settle OI-65 before implementing OI-64, but OI-64's policy choice can be ruled earlier without circularity."""
```

No files were edited.