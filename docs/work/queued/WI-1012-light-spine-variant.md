+++
id = "WI-1012"
title = "A light-spine variant an adopter can take: stakeholder needs and open items, with no work-item registry"
workstream = "docs"
sr_refs = ["SR-009"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#126-progress-log"
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by hand on 2026-11-19 at the operator's direction. Some downstream
repositories will carry only the light spine: their stakeholder needs, plus
open items to track decisions, without work items, requirements below the
needs, or tests traced to them. HomeHub is the first. Its hand-numbered
`open-items.md` (sections A to G) is to move onto the kit's registries.

The shipped open-items template now says such a repository may move an item
from `ruled` to `implemented` once its work is done, since it has no work
item to record that. That needed only a comment, because every reader treats
a status other than `pending` as settled. The operator asked for no
mechanism or test change for it here.

The comment cannot cover the rest. The full kit assumes a work-item registry
in several places:

- a pending open item that no queued or claimed work item cites is an error;
- the generated `docs/open-items.html` renders a pending item as a card only
  when such a work item cites it;
- IF-073, the open-items contract, says `status` is `pending` or `ruled`.

So a light-spine repository needs a variant it can adopt, not just the
full templates with parts deleted. This item scopes that variant. It is a
follow-up and depends on what HomeHub's adoption shows; the scope critique
decides whether it is a bootstrap profile, a documented subset in
`ADOPTING.md`, or both.

## Done-when

- [ ] A light-spine adopter has a documented way in: which templates it
      takes (stakeholder needs, open items, the dashboard if wanted), which
      checks it runs, and what it leaves out.
- [ ] In that variant, open items move `pending` -> `ruled` -> `implemented`
      without a work-item registry, and the checks it runs do not report the
      missing placeholder rows as errors.
- [ ] Whether IF-073 should name `implemented` is put to the operator, since
      it changes an accepted contract.
- [ ] HomeHub, or a scratch copy of it, adopts the variant and its checks
      pass.
