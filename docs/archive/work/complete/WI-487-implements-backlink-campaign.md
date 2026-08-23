+++
id = "WI-487"
title = "The back-link campaign: write the Implements: tags across the declared source surface with a code-review pass, raise the coverage dial to a bar the tree clears, and answer decay (OI-42 ruled, 2026-08-20)"
workstream = "process"
sr_refs = []
needs = ["WI-486"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Executed the campaign half of OI-42's ruling. 83 of 165 live LLR rows (50.3%)
now carry a literal `Implements:` declaration in the declared source surface
(`project-trajectory/scripts`), up from 1/165 (0.6%) measured at WI-486's
close — reproducible with `python project-trajectory/scripts/gen_arch_map.py
--backlink-coverage --src project-trajectory/scripts --root .`. Every tag
went through a code-review pass reading both the LLR row's `detail` text and
the actual code body before landing, across 17 modules (check_trajectory.py,
traj_render.py, agent_loop.py, agent_route.py, trace.py, trace_text.py,
integrate.py, agent_common.py, schedule.py, dispatch.py, bootstrap.py,
gen_trajectory.py, check.py, derive_gate.py, traj_views.py, trunk_step.py,
check_privacy.py, plus one in check_doc_refs.py). One candidate tag was
placed and then REMOVED at review: LLR-005's registry `code_symbol`
(`module_findings`) names a function-local variable inside `trace.analyze`,
never a real module-scope binding, so no placement in the file honestly
carried the claim — banked as a finding rather than forced. `docs/process.toml`
`[checks] backlink_coverage_min` rises 0 → 50 (this repo's own instance value;
the shipped `process.toml.template` default stays at `0` for a fresh
adopter — a VALUE divergence, not a STRUCTURE one). `dispatch.py:310`'s
dangling `SR-141` citation (merged into SR-148 on 2026-08-14) is repointed,
closing the row's "rides along" item. The module-size ratchet's 8 legitimate
growers (all prose/docstring lines, zero executable change) are re-stamped
with reasons in `tests/test_module_size_ratchet.py`. The decay answer is
below, under Context.

## Context

Executes the campaign half of OI-42's ruling, under the owner direction that
coverage is low BECAUSE THE TAGS ARE MISSING, so the remedy is to write them
— not to lower the bar. Hard-blocked on WI-486: the tightened harvester and
the report-only scanner are this campaign's instrument and progress bar.

- **The population:** 781 public symbols measured 2026-08-18 (the row's own
  AST method); reverse coverage starts at 1 of 161 live LLRs. Target: 50%,
  recorded on the ruling. Each tag lands with a CODE-REVIEW pass so it names
  the requirement the symbol genuinely fulfils — a wrong back-link is worse
  than none, because the column reads as evidence.
- **The dial rises AFTER the tags land:** the scanner's threshold moves from
  `0`/off to a value the tree already clears — the number goes up because
  the tags landed, never because the bar came down.
- **The decay answer is owed at close, not skipped:** the row's measured
  hazard is decay, not initial effort (WI-425's own hand repair went stale in
  three days; `adjudicate_brief.py` was born citing retired ids). At close,
  RE-CONSIDER option (c) — the OFT-style revisioned marker, the one surveyed
  mechanism that converts silent decay into loud failure — and record the
  recommendation either way; the ruling reversed the premise that refused it.
- **Rides along:** `dispatch.py:310`'s dangling SR-141 citation (merged into
  SR-148) — the one non-historical dangling id the row's census found.

Tags are source comments/docstrings — no spine cell moves; `ordinary` class.
Priority 2: deliberately after WI-486 lands and the scanner's first honest
number is on record.

### Decay answer, recorded at close (2026-08-21)

RE-CONSIDERED option (c), the OFT-style `artifact~name~revision` marker, as
OI-42's ruling directed. RECOMMENDATION: DO NOT BUILD (c) NOW; build a
cheaper partial mitigation instead, and record (c) as the design to reach
for if that mitigation proves insufficient.

**Why not (c) now.** It remains the only surveyed mechanism that reaches
MEANING rather than presence — but it mints a revision field on every spine
row, a new marker grammar, a re-authoring pass over every existing marker,
and a downstream migration, all to guard an annotation convention this same
campaign just spent a full session writing by hand. That is a large,
spine-touching, human-held decision (`docs/gate` tiers stay human-held per
`docs/process.toml`) for a problem this campaign's own evidence says has a
narrower shape than "every tag decays" implies.

**What the campaign's code-review pass actually found**, which sharpens the
decay question rather than just restating OI-42's WI-425 evidence: at least
three of the 165 LLR rows' OWN `code_symbol` cells were ALREADY stale before
any tag was written — `LLR-147` names `sn_gate` where the live function is
`sn_bar`; `LLR-077` names `spec_ref_findings` where the live function is
`specref_findings`; `LLR-005` names `module_findings`, which is not a
module-scope symbol at all (a function-local inside `trace.analyze` — the
same class WI-472 already flagged for `budget_findings`/
`component_findings`). None of these are decay FROM this campaign's tags —
they are pre-existing registry drift the mandatory read-the-code step
surfaced. That is direct evidence that the decay risk OI-42 priced is real
and already live in the registry `code_symbol` cells the campaign's tags
now sit beside, independent of whether the tags themselves ever move.

**The cheaper mitigation:** extend `gen_arch_map`'s existing scan (the same
module (c) would have touched, and the same one WI-486 already tightened)
with a companion, report-only check that, for each declared `Implements:`
line, confirms the symbol it is textually adjacent to still parses as a
real definition in that file — an EXISTENCE check on the TAG's own site,
not a meaning check, costing no spine field and no marker-grammar
migration. It would not have caught `dispatch.py:310` (that is (a)'s job,
still blocked on a history-marker convention per OI-42's own recommendation)
but it would catch the more common failure this campaign observed: a tagged
function renamed or deleted out from under its own docstring. Sized as its
own small WI if the owner wants it; not built here (out of this row's
scope, and a new checker is itself a reviewed addition).

**Deferred to the owner:** whether to mint the mitigation above as a WI,
and whether (c) should be revisited once the tagged surface is larger than
50%.
