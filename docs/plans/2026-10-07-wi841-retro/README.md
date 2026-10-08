# WI-841 retrospective (2026-10-07)

Why the WI-841 lane took about a day, what to change, and the reviewed drafts
of the first change. **Live until its rows are filed**; then it archives to
`../../archive/plans/` as a unit. The owner's rulings from it are recorded in
[`../../log.d/2026-10-07-wi841-retro-owner-rulings.md`](../../log.d/2026-10-07-wi841-retro-owner-rulings.md)
until that fragment compiles into `docs/log.md`.

| File | What it is |
|---|---|
| [`PROPOSAL.md`](PROPOSAL.md) | The diagnosis and the proposal: scope at filing (§1), a trust section (§2), consolidation first (§3), the class sweep (§4), in-lane spine work by checkpoint (§5), the coordinator path (§6), guards on spine approval (§7), and the reconciliation with the 29 queued rows, with five owner questions (§8) |
| [`drafts/`](drafts/) | The current drafts: a new `coordinator-cycle` skill (this-repo) with `references/recipes.md`, and `spine-authoring`'s "Three ways a spine grows" with `references/in-lane.md`. Not installed: they land through their own row |
| [`sol-skill-review.md`](sol-skill-review.md), [`sol-skill-review-r2.md`](sol-skill-review-r2.md) | Codex 6.1 Sol's two review-edit rounds on the drafts. Their links were re-pointed from the drafting folder outside the repo to `drafts/`; nothing else in them was changed |
| `history/1-author-draft.diff` | The author's first draft, against the `spine-authoring` skill as it stood at `14ad9077` |
| `history/2-sol-round-1.diff` | Sol round 1's edits |
| `history/3-sol-round-2-and-author.diff` | Sol round 2's edits, then the author's follow-ups the owner accepted: the restored settled-code rule in `in-lane.md`, one act per kind in the recipes, and plain skill names in place of links that resolve only once installed |

Drafted outside the repo in `C:/Projects/ai-template-plans/wi-841-retro/` and
copied here on 2026-10-07 for traceability. This folder is now the copy of
record.
