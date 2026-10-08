+++
id = "WI-848"
title = "The coordinator's procedure is one skill, and spine-authoring states the three ways a spine grows"
workstream = "process"
specref = "docs/plans/2026-10-07-wi841-retro/PROPOSAL.md"
needs = ["WI-846", "WI-860", "WI-852", "WI-853"]
buildtier = "medium"
safety_class = "ordinary"
priority = 8
+++

## Context

Filed by hand on 2026-10-07 from the WI-841 retrospective
(`docs/plans/2026-10-07-wi841-retro/`, proposal §5 and §6, row P1). The owner's
rulings 1, 3, 9 and 10 of 2026-10-07
(`docs/log.d/2026-10-07-wi841-retro-owner-rulings.md`) shape it.

The coordinator's procedure lives in a chain of twelve handoffs, each a delta
on the last. This row moves it into one this-repo skill, so handoffs hold state
only. It also gives the kit skill `spine-authoring` the three modes of spine
growth: from the vision, tier by tier; in a lane on released rungs, one closed
change set judged in one sitting; in a lane touching a held rung, split at the
dial. In every mode a child is approved only after its parent.

Both drafts exist, reviewed by Codex 6.1 Sol in two review-edit rounds with the
owner's three rulings on the balance applied:
`docs/plans/2026-10-07-wi841-retro/drafts/`. The authoring model is ruling 10's:
an author (GPT Terra here, or another declared author role) drafts, and the
adjudicator judges.

`references/in-lane.md` describes approval acts taken in the lane, so land this
row after WI-849 or in one batch with it.

## Done-when

- `project-trajectory/skills/coordinator-cycle/` (`scope: this-repo`) lands from
  the reviewed draft with `references/recipes.md`. It is materialized to
  `.claude/skills/` and `.agents/skills/` by `bootstrap.py --dest . --sync`,
  listed in `project-trajectory/skills/README.md`, and `INDEX.csv` is
  regenerated.
- `spine-authoring` gains "Three ways a spine grows" (the mode table and the
  parent-first rule) and `references/in-lane.md` from the draft. Its §1 to §6
  are unchanged, and its description is the original wording extended only by
  the lane clause.
- Before landing, the drafts are reconciled with every row landed since
  2026-10-07 (proposal §8.4). In particular, `in-lane.md`'s held CLARITY line
  follows WI-851 if it has landed, and the preamble's approval-act wording
  follows WI-849.
- The next coordinator handoff points at the skill for procedure and carries
  no cycle, recipe or "corrections learned" section of its own.
- The skills-index, skills-sync and materialization tests pass, plus the smoke
  tier.
- The coordinator-cycle recipes carry WI-846's sign-in as landed: the
  adjudication recipe's sign-in step names the long-lived token read through
  the environment variable OI-110 (b) declares, and dev-setup's one-time
  `claude setup-token` step as the remedy for a home that is not signed in.
  The draft's 'pending WI-846; the owner runs `/login` at expiry' line does
  not land, and no recipe makes an interactive sign-in the procedure.
- The coordinator-cycle review steps carry the 2026-10-08 ruling (`docs/log.d/2026-10-08-owner-ruling-review-threat-model.md`):
  rule 1 by a link to PROCESS.md §6's review threat model, and rules 2 and 3
  as the procedure that holds until WI-811 lands (the coordinator applies
  rule 1 to each review, records each dismissal in the lane's decisions
  record, and sends a contested or third-round finding to the adjudicator).
  (WI-864's sitting, `docs/reviews/wi-864-adjudicate-review-response-overlap/001-ADJUDICATE-89298d9.md`.)
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit for the kit skill
  `spine-authoring`; `coordinator-cycle` is this-repo and ships to no adopter.
