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
rewrite. The boundary set comes from an explicit `boundary` class on the
shipped-file inventory's entries (`kitlib/bootstrap_manifest.MAPPING`;
revision 6), matched on the destination path, so the launchers shipped from
`scripts/run.template.*` count; no second list. The defined-name reader is
WI-1025's, reused here.

**Layer 3, the judgement.** The sitting brief and the spine-authoring
skill state contract voice for every requirement tier: an LLR states the
observable obligation and survives a refactor that keeps behaviour.

**The migration, and its amendment rule (HANDOFF §3.3 N5).** A rough
pattern finds code-like tokens in the title, detail or rationale of 222 of
347 LLR rows; component rows' `notes` list member files, which the
`Component:` headers (WI-1021) made a second home. Each row is rewritten in
place to contract voice, keeping every obligation. The coordinator's recipe
"amend an accepted row by addition"
(`project-trajectory/skills/coordinator-cycle/references/recipes.md`)
forbids that today, so this row amends it: removing code names from an
accepted cell is a rewrite that keeps each obligation, checked sentence by
sentence against the accepted text. Where a row no longer fits the design,
PROCESS.md §5's re-cut (retire and mint) applies, in its own row filed on
trunk, not in this lane. WI-1020 was cancelled in favour of this rule.

## Scope answers

- **S1.** Deliverables, in order on one branch: (1) the inventory's
  `boundary` class and the commit check; (2) the rewrite of existing rows
  and the recipe amendment; (3) layer 3's text. Kept together: (1)'s token
  classes define what (2) removes, stated once.
- **S2.** The `boundary` class decides whether a file name is admitted in
  an LLR or TC row, so a `## Trust` section follows.
- **S3.** The token classes are closed in Done-when 2; text outside them is
  admitted by the check and judged by layer 3. Bounded to supported
  workflows and kit routes (PROCESS.md §6): hand-chosen aliases and
  hand-edited kit-written state are outside it.
- **S4.** `single`: a commit check, an inventory schema and a migration.
- **S5.** No new state or boundary. Re-cut LLRs (text only, drifting):
  LLR-133 (the stand-alone rule in `trace_text`), LLR-203 (the shipped-file
  inventory), LLR-276 (the mapping-purpose classes); the lane's plan names
  the rows behind the artifact advisories and completes the list. The
  migration's rewrites keep each obligation, so they are not re-cuts; a
  row that needs one is filed on trunk (Done-when 4).
- **S6.** `needs` WI-1023: the code cells are gone, so only text remains;
  WI-1025: interface rows hold symbol-free forms, so the check can include
  them without failing every `call` row, and its name reader is reused. No
  new package, tool or service.

## Trust

The inventory's `boundary` class gains authority over which file names a
commit may add to LLR and TC rows (PROCESS.md §3, "When a guard is owed").

- **Producer.** A person or model editing `kitlib/bootstrap_manifest.py` in
  a lane (the supported route), and this row's classification. No script
  writes it.
- **Failed write.** An entry with a class value other than `boundary`, or a
  malformed entry: the manifest reader reports it as a finding.
- **Consumers.** The commit check (in `trace_text.py`, run by the hook),
  `gen_arch_map.mapping_purpose_findings` and `bootstrap.py`, all through
  `bootstrap_manifest.mapping_entries`.
- **Ruling, shared by every consumer.** An entry with no class, or an
  invalid one, is not a boundary file: its name is refused where only
  boundary files are admitted.

## Done-when

- [ ] Each shipped-file inventory entry may carry the `boundary` class;
      every registry, template, configuration file and launcher entry does.
- [ ] **The commit check.** It refuses a token added to an SN, SR, LLR, IF
      or CMP text cell when the token is (a) the repository path or the
      basename with suffix of a file under `[paths] src` that is not a
      boundary file, or (b) a name `ast` finds defined in a `.py` file under
      `[paths] src` (a module-level or class-level `def`, `async def` or
      `class`, or a module-level assigned name) written as code: inside
      backticks, containing `_`, with an internal capital, or followed by
      `(`. It refuses a boundary file's destination path or basename added
      to an SN, SR, IF or CMP row. Any other text is admitted and left to
      layer 3. It reads only the commit against its parent and only added
      tokens.
- [ ] Every existing SN, SR, LLR, IF and CMP row passes the same rule as if
      all its text were added; each rewrite keeps every obligation. The
      Deliverable lists each row changed and each act owed; the acts go to
      automated adjudication (HANDOFF §3.3 N4), and the lane holds for none.
- [ ] A row that no longer fits the design is left as it is, listed in the
      Deliverable, and filed on trunk at the merge as its own re-cut row.
- [ ] The recipe line is amended as above; PROCESS.md §5 is cited, not
      restated.
- [ ] The Deliverable says which of WI-1018's cases B1 to B9 this row
      closed; the coordinator narrows WI-1018 on trunk at the merge to
      what is left.
- [ ] The sitting brief and the spine-authoring skill state contract voice
      for every requirement tier, once, with a pointer from
      `spine-questions.md`.
- [ ] A RESYNC entry (variant F) gives adopters the check and the
      `boundary` class; their existing rows warn until rewritten.
- [ ] Red-before tests for each token class, the admitted text, the Trust
      ruling and the added-only rule; every importer of a changed module
      runs green; `trace.py --strict` is clean.
