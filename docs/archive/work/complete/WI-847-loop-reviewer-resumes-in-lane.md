+++
id = "WI-847"
title = "The loop's narrow review round renders its delta through the one reviewer render"
workstream = "process"
sr_refs = ["SR-154"]
specref = ""
needs = ["WI-852", "WI-834"]
buildtier = "medium"
safety_class = "ordinary"
priority = 5
+++

## Deliverable

`agent_brief.narrow_reviewer_prompt` renders the loop's narrow review round
by strictly filling the phase's reviewer template, or the shipped one,
through `prompts.fill`, the fill the attended render uses. The round's delta
is its reading scope. `agent_brief.narrow_scope_line` is the one home of the
narrow range sentence, which `review_brief._scope_lines` now reads. An
override that cannot carry the slots refuses. Nothing in the loop schedules a
narrow round yet: that arrives with WI-884, the owner's split of reviewer
retention and the gate binding (decisions coordinator-2026-10-10 D-008,
D-011). Spine: LLR-045 and TC-082 amended by GPT Terra and blessed MEANING by
amendment sitting `docs/reviews/wi-847/001-ADJUDICATE-7825c62.md` (act seq
92). Gate: Codex 6.1 Sol's fresh full-lane review
`docs/reviews/wi-847/002-REVIEW-A-8e8af95.md`, APPROVE with 0 findings.

## Context

Filed by the wave-18 coordinator on 2026-10-07. The owner confirmed it for the
hand path that day: narrow rounds resume the reviewer while a lane iterates,
and the last review before a landing is a fresh, full-lane review from the
lane's trunk base to its tip. Today the loop's reviewer is never retained
(`session_keep.keep_for` covers only ADJUDICATE). Every loop review round is
a fresh, full-lane session, so the merge gate is already right, but each round
pays the full context cost again. On WI-841 the hand path's fresh Sol rounds
cost 115k to 160k tokens each, mostly re-reading the same context, and they
hit the Codex plan limit twice.

**Owner ruling, 2026-10-10** (attended; decisions
`coordinator-2026-10-10.toml` D-008): the row is split. This row lands
step 1, the narrow round's brief rendered through the one reviewer render.
Reviewer retention and the merge gate's freshness binding move to their
own row, filed on trunk with the builder's design and the gate hazards it
found. That row's `## Trust` section carries the one written here before the
split. The owner added one requirement: the final reviewer is configurable,
either a fresh session or a persisted independent final reviewer.

## Done-when

- The narrow round's reading scope (the round's delta) is a render of
  `prompts/reviewer.template.md` through `prompts.py`, the same render the
  coordinator's reviews use, with one home for the narrow range sentence.
- A template override that cannot carry the slots refuses the render.
- Tests: the loop's narrow render carries the delta and the attended
  render's range sentence; an override without the slots refuses.
- The rows the change makes untrue or incomplete (LLR-045, TC-082) state
  it and pass adjudication on the one adjudication path.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit.
