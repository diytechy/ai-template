SKILLS REVIEWED: 18 edits

Only the three permitted drafts changed. `SKILL.orig.md` remains byte-identical; nothing was staged or committed.

**Edits**

[coordinator-cycle/SKILL.md](drafts/coordinator-cycle/SKILL.md):

1. Shortened the description and introduction, added sibling-skill links, and moved local restrictions into recipes. **Concision.**
2. Required an approved SN/SR anchor; distinguished Drafted spine rows from interfaces, which have no approval status. **Truth, consistency.**
3. Kept spec and Drafted intent as narrow-review obligations while deferring row wording; preserved the reviewer template’s antidote exceptions. **Consistency.**
4. Required search evidence even for single-site findings; allowed reviewers to report that no unlisted site exists. **Concision, usability.**
5. Added commitment of reconciled text before composition, retired-row scope, affected-chain returns, and omission of empty sittings. **Truth.**
6. Made the Done-when hold explicit, including early checkpoints when it blocks iteration. **Truth.**
7. Changed “last commit” to “last spine commit,” required renewed review after substantive rebase changes, and clarified owner checkpoints and decision recording. **Truth, consistency.**

[spine-authoring/SKILL.md](drafts/spine-authoring/SKILL.md):

8. Shortened the widened description while retaining both authoring modes. **Concision.**
9. Tightened the new section from **42 to 32 lines**; aligned phases, approved anchors, arms coverage, whole-repo checks, Done-when holds, gate authority and returns. Preserved §1–§6 and all existing body text. **Scope, consistency, concision.**

[coordinator-cycle/references/recipes.md](drafts/coordinator-cycle/references/recipes.md):

10. Added executable-path aliases, Git Bash conventions and checkout context. **Truth.**
11. Added builder/Terra/Sol brief overrides needed to implement the new procedure; identified prompt rendering and findings coverage as unwired follow-ups. **Consistency.**
12. Specified the rubric and reading inputs the existing critique template requires. **Truth.**
13. Documented combined brief `kind:id` tokens, supported kinds, empty-section refusals and the separate arms-map input. **Truth.**
14. Corrected sign-in interpretation, verdict reservation, adjudication exits, primary-checkout telemetry location and preview limitations. **Truth.**
15. Supplied claim flags and required pause restoration after failed claims. **Truth.**
16. Expanded landing commands, snapshot/verdict flags, full artifact paths and verifiable archive-parent construction. **Truth, usability.**
17. Corrected the claim that every lane hook forces generated-view freshness: normal claimed branches skip those checks. **Truth.**
18. Separated squash-merging from rebase replay resolution; preserved higher retired-ID watermarks and qualified sandbox, capacity, slug and relaunch observations. **Truth.**

**Not changed, but flagged**

- **Approval location conflicts:** the existing spine preamble and `PROCESS.md` §4 reserve acts to the serial trunk side; later handoffs and `coordinator_adjudicate.py` perform them in lanes. Those authoritative texts remain untouched.
- **Act grouping conflicts:** recipes retain one act for amendments and first approvals sharing registries; `adjudicate-combined.template.md` instructs separate acts for its sections. The owner should settle this explicitly.
- **Scope critique remains an adaptation:** `critique.template.md` judges artifacts against rubrics, rather than directly implementing a scope critique. The recipe now supplies appropriate inputs; the eventual renderer needs an agreed scope rubric.
- **Live verification remains owed:** no stale-amendment lane trial, adjudicator launch, OAuth refresh or guard relaunch ran. Neither integrity CLI supports a row-set filter; the drafts now state that limitation.

**Balance verdict**

**Coordinator — 195 lines:** appropriate for the procedure. Its biggest remaining risk is dependence on older dispatch templates whose instructions require explicit overrides.

**Recipes — 300 lines:** the growth earns its place through runnable paths, scope grammar and landing mechanics. Its biggest risk is the unresolved act-grouping conflict.

**Spine — 530 lines:** slightly above the approximate target because the original already occupied 498 lines. The 32-line section earns its length; further substantial reduction would require editing existing material. Its biggest risk is the inherited trunk-only approval wording.

**Commands**

- `Get-Content` and `rg`: checked the proposal, repo contract, PROCESS references, session protocol, all twelve handoffs, templates and tool implementations.
- `--help`: checked integrity/trajectory, adjudication, claim, snapshot, sweep, guard, complexity, regeneration, spec-moving and Codex resume interfaces; all returned exit 0.
- Git help and archive inspection: verified `commit-tree`, `update-ref` syntax and existing archive-parent structure.
- In-memory validation using shipped parsers: frontmatter, vocabularies, description floors, links and combined tokens passed; existing spine body/numbering and original-file preservation passed.
- `git diff --no-index --check`: no whitespace errors.