+++
id = "WI-1044"
title = "The author's prompt template and TC-385 name roles, not models; recipes §5's carriage-return escapes restored"
workstream = "docs"
sr_refs = []
needs = []
specref = "docs/archive/work/complete/WI-1037-skill-names-roles-not-models.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 4
planmode = "none"
+++

## Context

Filed on trunk on 2026-11-21 from WI-1037's close-out, which found three
things outside its files (its Deliverable, "Found, not changed"; its
decision D-003).

- `scripts/coordinator/terra-spine-prompt.template.md` still names models
  ("GPT Terra", "a Claude Opus builder", "Claude Opus adjudicator") where it
  means roles, and `tests/test_prompts.py` pins one of those phrases. The
  operator's rule behind WI-1037: which model fills a role is a setting.
- TC-385 (Accepted) names Sol and Terra in its method and expected cells.
  WI-1037 left it, since amending it owes an act a text-only row did not
  take.
- In `coordinator-cycle` recipes §5, the bullet about counting carriage
  returns has lost its `\r` escapes in three places: a raw newline sits
  between the backticks. The defect predates WI-1037.

The three ride one row because each is a small text fix the same review
reads; none changes behaviour. The template's file name stays (renaming it
is a launch-path change outside this row).

## Done-when

- [ ] The template names the roles (the author, the builder, the
      adjudicator); an observation tied to one model keeps its evidence,
      labelled "observed with <model>"; its pin in `tests/test_prompts.py`
      follows.
- [ ] TC-385's method and expected cells name the roles (text only, its
      status unchanged); the Deliverable lists its drift for automated
      adjudication.
- [ ] Recipes §5's three escapes read `\r` again, in all three byte-equal
      copies of the skill (regenerated, not hand-edited).
