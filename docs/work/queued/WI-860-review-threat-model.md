+++
id = "WI-860"
title = "A review's scope excludes defects that need a compromised host"
workstream = "process"
specref = "docs/log.d/2026-10-08-owner-ruling-review-threat-model.md"
buildtier = "medium"
safety_class = "ordinary"
priority = 8
+++

## Context

Filed by hand by the coordinator on 2026-10-08 from the owner's ruling
([log.d/2026-10-08-owner-ruling-review-threat-model.md](../../log.d/2026-10-08-owner-ruling-review-threat-model.md)).
WI-846's lane drew six Codex Sol rounds; the later ones chased reproductions
that need a fake runner binary or a cwd-dependent shim. The kit already says
"the threat model is bugs and fail-open, not malice" for forge mode
(PROCESS_OPTIONS.md), but no rule bounds what a code review may demand, so a
reviewer can keep finding contrived cases and a coordinator keeps building
against them.

## Done-when

- PROCESS.md §6 states the review threat model in one paragraph, its one
  home: in scope are defects in a normal working environment, content agents
  write into the repository (the gates exist to check it), supported
  configurations and regressions of supported behaviour; out of scope is any
  finding whose reproduction needs the host itself compromised or contrived
  (a fake or hostile binary, a shim whose output depends on cwd, the
  environment or PATH changed by another process mid-call, a tampered OS or
  tool), which is dismissed in one recorded line and never answered with
  code.
- The kit's reviewer template and every adjudication brief template that
  judges a finding link to that paragraph rather than restating it; the
  byte-budget skill's rows are re-stamped.
- The spine carries the obligation (Terra authors it; an independent
  adjudicator judges it in the lane).
- Review bar: A (one cross-family REVIEW-A).
