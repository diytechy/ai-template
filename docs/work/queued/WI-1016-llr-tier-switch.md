+++
id = "WI-1016"
title = "A repository can switch off the implementation layer: LLRs, components and the code-level interfaces"
workstream = "process"
sr_refs = ["SR-186", "SR-157", "SR-049", "SR-159"]
specref = "docs/plans/2026-11-11-test-tiers/HANDOFF.md#126-progress-log"
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by hand on 2026-11-21 at the operator's direction. The operator wants
to evaluate projects with and without the LLR scope: the spine should still
break a problem down and structure the architecture without the design tier.
Interfaces other than the code-level ones stay.

Today there is no project-level switch. An SR skips LLRs only when its
verification method is Analysis, Inspection or Vouch (`llr_exempt`). SR-186,
accepted, says the process keeps "the required SN-to-SR-to-LLR-to-TC tiers"
and "never permits omitting a required SN→SR→LLR→TC tier", and the README
and `trace.py` call the four registries the required spine. So this row
reverses an accepted requirement. SR-186's amendment and the setting's own
requirement (under SN-012, heavy layers are opt-in) are the operator's to
accept.

What reads LLRs today, each of which needs an answer with the tier off:

- `trace.py`'s joins and zero-orphan rule (a TC verifies SRs and LLRs);
- `derive_stage`'s DevStg-LLReqs rung, and DevStg-Arch, whose component
  membership is the LLR Module → Component join
  (`kitlib.spine.module_components`) that the cross-component rule and the
  dashboard's component view also read;
- the back-link coverage gate (`Implements: SR-…, LLR-…`, minimum 50%) and
  the tag/CodeSymbol check;
- the review test set (`review_set` walks SR → LLR → TC);
- the acceptance brief, the open-items page, the planning briefs and the
  spine-authoring questions;
- the dashboard's architecture views.

"Code-level interfaces" here means the module-to-module call seams: a kit
module owns them and kit modules call them, and they hang off LLR-pinned
modules. A row that realizes a boundary crossing, or whose channel is a
file, CLI, exit code, stdout, env, git or bytes surface, stays. The scope
critique confirms the cut.

**Components go with the tier (operator, 2026-11-21).** The component
registry, the DevStg-Arch rung, the cross-component rule and the component
views decompose the implementation, so they drop out with the LLRs. The
depth-0 frame (`external.toml`: outside parties, boundary crossings,
outside relationships) decomposes the system boundary, not the
implementation, and stays, with the assumption tier that lands on it. Under
the review-churn plan's variant F
(`docs/plans/2026-10-11-review-churn/pointer-rules.md`, ruled, not built) an
interface's owner is a component id, so an interface that survives with the
tier off needs an owner that is not a component: today's file path, or an
`external:` party.

Related: WI-1012 (the light spine: needs and open items, no work-item
registry) sits further down the same axis; the critique decides whether one
depth setting serves both. WI-1015 changes the same checks, so this row
builds after it or with it.

## Done-when

- [ ] One declared setting in `docs/process.toml` turns the LLR tier off.
      The default stays on, and this repository stays on.
- [ ] With it off: no LLR registry is required; a TC verifies its SR
      directly; the stage derives without the DevStg-LLReqs rung; back-links
      and the review test set read SR tags; the code-level call seams are not
      required. Every other interface, the frame and the assumption tier are
      unchanged.
- [ ] With the tier off, the component registry, the DevStg-Arch rung, the
      cross-component rule and the component views are off too, while the
      depth-0 frame and the assumption tier stay. Each surviving interface
      keeps an owner that is not a component.
- [ ] Switching off with LLR rows present, and back on, is defined: what
      happens to the rows, their acceptances and the code tags.
- [ ] SR-186's amendment and the setting's own SR are drafted for the
      operator's acceptance. The README and PROCESS.md state the required
      tiers under each setting.
- [ ] A scaffold under each setting passes its own checks, so a downstream
      project can be run and compared both ways.
- [ ] A RESYNC entry tells adopters the setting exists and that its default
      changes nothing.
