ROUND 2: 8 edits

**Edits**

1. [spine-authoring/SKILL.md](drafts/spine-authoring/SKILL.md): restored the exact original description, then appended only the lane clause. Preserves adopter triggering.
2. Same file: corrected “below the dial,” shortened the mode guidance, and stated the held-rung CLARITY exception. Retained the parent rule unchanged.
3. [in-lane.md](drafts/spine-authoring/references/in-lane.md): replaced automatic derived-SR routing with the distinction between a derived obligation and a missing stakeholder outcome; clarified existing statuses remain unchanged during authoring.
4. Same file: replaced review-timing instructions with reconciliation before judgement and requirement-text changes within an open window. Removes lane orchestration.
5. Same file: clarified arm-coverage judgement, separate combined-brief verdict sections and act commits, and chain-only returns. Avoids unnecessary child rewrites.
6. Same file: replaced blanket exclusion of held rows from the sitting with first-draft chain evidence and amendment classification; added verdict-linked CLARITY re-attestation and snapshot-refusal handling. Aligns authority with PROCESS.
7. [coordinator-cycle/SKILL.md](drafts/coordinator-cycle/SKILL.md): shortened the Never introduction and clarified the two-hour threshold. Preserved every prohibition and the confirmed relaxation.
8. [recipes.md](drafts/coordinator-cycle/references/recipes.md): changed the rollup prohibition into an actionable restore-before-commit instruction, retaining trunk regeneration.

The lane reference fell from **568 to 497 words**.

**Flagged, not changed**

- Inherited trunk-only approval wording conflicts with coordinator lane acts.
- Recipes group amendments and first approvals into one act; the combined brief requires separate acts.
- PROCESS §4 retains an earlier numeric dial description alongside the later rung-based definition.
- No disagreement with the owner’s rulings.

**Commands**

- `Get-Content`, `rg`: inspected drafts, earlier review, PROCESS, briefs, and rollup implementation.
- `git diff --no-index`: compared pre-Sol and pre-round-two drafts; no whitespace errors.
- Python assertions and SHA-256 checks: verified only four authorized files and permitted regions changed, original description preserved, and `SKILL.orig.md` unchanged.
- `quick_validate.py`: blocked by missing PyYAML; no installation performed.
- `git status --short`: drafts are not a Git checkout.