+++
id = "WI-502"
title = "Mechanize the Implements-tag vs CodeSymbol cross-check, warn-first (OI-53 ruled (d) follow-up, 2026-08-22)"
specref = "docs/requirements/open-items.toml#OI-53"
workstream = "scripts"
sr_refs = []
needs = ["WI-501"]
buildtier = "quick"
safety_class = "ordinary"
priority = 2
+++

## Context

Executes the (d) half of OI-53's ruling: promote the cross-check the
2026-08-21 closing review ran by hand — every `Implements:` tag's ENCLOSING
SYMBOL compared against its row's `CodeSymbol` and `Module` — into
`check_trajectory` as a warn-first finding, so the stale-cell population is
measured continuously instead of rediscovered by campaign. The reviewer's
manual method is the spec: resolve each tag's enclosing def/class, compare
by containment (a tag on `RoutingState.note_session` satisfies a cell
naming `RoutingState`), warn on mismatch naming both sides. Runs after
WI-501 so it arms on a clean baseline; if residual mismatches survive the
repair, they seed the finding's initial count honestly (never an
allowlist — this is warn-first by design). Share the tag-parsing grammar
with gen_arch_map (ONE home — the WI-486 rule); regression tests: a
planted mismatch warns, the containment case does not, a function-local
cell name is reported as unresolvable rather than matched.
