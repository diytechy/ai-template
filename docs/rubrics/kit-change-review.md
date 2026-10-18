# Rubric — Reviewing a change to this kit (WI-852)

**Adjudicates:** the checks a review of a change to this repository owes beyond
the kit's reviewer brief, which already asks for the failure classes, the
Done-when coverage map, the red-before test, the unrepresentable clause and the
requirement-row sweep.
**Used by:** an independent reviewer of a lane, when its brief is rendered with
`review_brief.py review --rubric docs/rubrics/kit-change-review.md`.

## Intent

The rules this repository holds its own lanes to (`CLAUDE.md`, and the owner
rulings the spine-authoring skill records) that the kit's shipped brief cannot
name, because an adopter's repository has its own.

## Anchors

**K1 — Requirement text is true, and the right way round.** Read every added or
amended SN, SR, LLR and TC cell against PROCESS.md and the code. *Bad:* a row
stating the inverse of the rule its code implements; earlier waves shipped
that, and code review missed it.

**K2 — Owner ruling R2, as review-churn ruling 5 refines it.** No SN or SR
cell names an implementation carrier (a script, command, file or function),
acceptance included. Current-carrier evidence lives in the TC rows that verify
the row, and a shipped boundary artifact (a registry, template, config file or
launcher) may be named at the LLR and TC tiers only. An approved cell keeps its
approved text, names included, until it is amended through its authority.

**K3 — Back-links and approved rows.** Each `Implements:` tag names the LLR
whose `module` is that file, and the function appears in that LLR's
`code_symbol`. An approved row changes only where the spec grants it, and no
Status flips.

**B1 — A finding stated as a guess.** Report a finding as a claim confirmed by
reading or running the code, never as a guess.
