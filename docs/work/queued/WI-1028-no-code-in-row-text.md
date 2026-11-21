+++
id = "WI-1028"
title = "Requirement and architecture rows name no code: a commit check on added tokens, and the existing rows rewritten"
workstream = "process"
sr_refs = ["SR-157", "SR-186", "SR-163"]
specref = "docs/plans/2026-10-11-review-churn/README.md#5-requirements-never-reference-code-code-points-up"
needs = ["WI-1023", "WI-1025"]
buildtier = "strong"
safety_class = "ordinary"
priority = 2
planmode = "single"
+++

## Context

Variant F's eighth row (F-8), filed on trunk on 2026-11-21 (queue-drill
HANDOFF §3.3). It is item 5's layers 2 and 3 (owner ruling 2026-10-11,
ruling 5 as refined): no implementation carrier (code file, function,
symbol) in any SN, SR, LLR, IF or CMP row; shipped boundary files
(registries, templates, configuration, launchers) may be named at LLR and
TC only; SN and SR rows name no file in any cell, rationale included.

**Layer 2, the commit check.** It grows from `trace_text`'s warn-only
advisories (`sr_artifact_advisories`, `sn_artifact_advisories`). It compares
the commit with its parent and judges only tokens added to a requirement or
architecture text cell, so a lane touching a row for another reason owes no
rewrite. Code tokens: paths to implementation files, and names defined in
the shipped scripts (read by `ast` each run) written as code (backticked,
snake_case, CamelCase or a call). The boundary set comes from an explicit
`boundary` class on the shipped-file inventory's entries
(`kitlib/bootstrap_manifest.MAPPING`; revision 6), matched on the
destination path, so the launchers shipped from `scripts/run.template.*`
count; no second list.

**Layer 3, the judgement.** The sitting brief and the spine-authoring
skill state contract voice for every requirement tier: an LLR states the
observable obligation and survives a refactor that keeps behaviour.

**The migration, and its amendment rule (HANDOFF §3.3 N5).** A rough
pattern finds code-like tokens in the title, detail or rationale of 222 of
347 LLR rows; the CMP rows' notes list member files, which the `Component:`
headers (WI-1021) made a second home. Each row is rewritten in place to
contract voice, keeping every obligation. The coordinator's recipe
"amend an accepted row by addition"
(`project-trajectory/skills/coordinator-cycle/references/recipes.md`)
forbids that today, so this row amends it: removing code names from an
accepted cell is a rewrite that keeps each obligation, checked sentence by
sentence against the accepted text; where a row no longer fits the design,
PROCESS.md §5's re-cut (retire and mint) applies instead. Accepted rows keep
their status and drift; the acts go to automated adjudication (N4), listed
in the Deliverable. WI-1020 was cancelled in favour of this rule.

**WI-1018's cases.** Its first set (B1 to B9) is taken here where this
migration covers it; WI-1018 runs after this row on what is left.

**Needs:** WI-1023 (the code cells are gone, so only text remains) and
WI-1025 (interface rows hold symbol-free forms, so the check can include
them without failing every `call` row).

## Scope answers

- **S1.** Deliverables, in order on one branch: (1) the inventory's
  `boundary` class and the commit check; (2) the rewrite of existing rows
  and the recipe amendment; (3) layer 3's text. Kept together: (1)'s token
  grammar defines what (2) removes, stated once.
- **S2.** The check refuses a commit, an existing gate class (the commit
  hook's checks); no file gains authority over a hold or an act.
- **S3.** Deny by default over the closed token classes in Done-when 2;
  prose that names mechanism in plain words is layer 3's, not the check's.
- **S4.** `single`: a commit check, an inventory schema and a migration.
- **S5.** No new state or boundary; rows are re-cut only where they no
  longer fit, each named in the Deliverable.
- **S6.** No new package, tool or service.

## Done-when

- [ ] Each shipped-file inventory entry may carry the `boundary` class;
      every registry, template, configuration file and launcher entry does.
- [ ] A commit check refuses a token added to an SN, SR, LLR, IF or CMP
      text cell when it is a path to an implementation file or a name
      defined in the shipped scripts written as code (backticked,
      snake_case, CamelCase or a call); and refuses a boundary-file name
      added to an SN, SR, IF or CMP row. It reads only the commit against
      its parent and only added tokens.
- [ ] Every existing SN, SR, LLR, IF and CMP row passes the same rule as if
      all its text were added; each rewrite keeps every obligation, and the
      Deliverable lists each row changed and each act owed.
- [ ] The recipe line is amended as above; PROCESS.md §5 is cited, not
      restated.
- [ ] The sitting brief and the spine-authoring skill state contract voice
      for every requirement tier, once, with a pointer from
      `spine-questions.md`.
- [ ] A RESYNC entry (variant F) gives adopters the check and the
      `boundary` class; their existing rows warn until rewritten.
- [ ] Red-before tests for each token class and the added-only rule; every
      importer of a changed module runs green; `trace.py --strict` is clean.
