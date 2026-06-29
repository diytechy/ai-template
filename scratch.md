# Scratch Notes

Brainstorming and open questions feeding `IMPROVEMENT_PLAN.md` — rough notes,
not a spec. Resolved items are tagged with the thread that addressed them;
still-open items are grouped at the bottom for a future session.

## Resolved — folded into IMPROVEMENT_PLAN.md

### Agent guide directives — Thread 3 (landed) + Thread 0b (landed)

How to encode general directives into the agent guide (`AGENTS.md`) — these
would likely be beneficial in all general cases:

1. **Ask, don't assume.** If something is unclear, ask before writing a single
   line. Never make silent assumptions about intent, architecture, or
   requirements. When running unattended, pick the most reasonable
   interpretation, proceed, and record the assumption rather than blocking.
2. **Right-size the solution.** Implement the simplest solution for simple
   problems, a better solution for harder problems. Don't over-engineer or add
   flexibility that isn't needed yet — but judge "simple" against the overall
   scope; don't shoehorn in a reusable/simple method if it actually produces
   complex architecture to wire it in.
3. **Stay in your lane.** Don't touch unrelated code, but do surface bad code or
   design smells you discover so we can address them as a separate issue.
4. **Flag uncertainty explicitly.** If unsure, see #1. Where it makes sense, run
   a small, localized, low-risk experiment and bring the hypothesis + results
   back to discuss. Confidence without certainty causes more damage than
   admitting a gap.
5. **Suggest better ways.** Always open to ideas for a better approach —
   including one with longer-lasting impact over a tactical fix.

Follow-up: are there places where hooks would be more appropriate than
`AGENTS.md` directives to *guarantee* execution (vs. just stating intent)?

### Traceability rendering — Thread 1 (landed)

Documentation gaps / requirement clarity: ideally a mind map or other diagram
breaks stakeholder needs into individual components (e.g. SN → SR → LLR). Could
that be HTML for easy browsability? Markdown probably can't render a diagram
that large. Can it be regenerated at each gate?

Related: emphasize line-by-line reviewability; composite/generated artifacts
should generally be excluded from repo change tracking. A full SN→SR→LLR→TC map
as an HTML artifact would make every connection clear without hitting
Markdown's diagram-size limits.

### Process/product segmentation — Thread 2 (landed)

How to emphasize infrastructure needs? Ideally documentation/traceability all
use the same toolset (Python, since it's already in use here), but testing for
the actual deliverable depends on its implementation language. How should that
segmentation be clarified?

### TDD emphasis — Thread 4 (landed)

The main focus of this template should be test-driven development — does that
need to be emphasized anywhere else in the template?

### Lifecycle phases (ready / set / go) — Thread 5 (spec recorded; build queued, Session B) + Thread 6 (landed)

Requirements/needs should clarify *when* in the process lifecycle they apply:
get ready (install / dependency fetching), get set (first-run configuration), go
(normal runtime operation) — plus how to review needs/requirements for mutual
contradictions and solicit human input for clarification (that last part →
Thread 6).

Follow-up: does Thread 5 need refinement for lifecycle vs. external
configuration/dependencies? E.g. an app may need dependencies before it can even
execute, and configuration before it can enter normal runtime — distinct from
what gets set up *during* typical execution (connecting to external services,
allocating memory, etc).

Confirmed semantics:

- **Provision** — may include defining configuration, when that configuration is
  required at launch and the app has no way to obtain it at startup (can't
  prompt the user, must error or fall back to defaults instead). Whether config
  counts as Provision or Startup depends on the app's own startup capability.
- **Startup**
- **Runtime**

### Stakeholder vs. user need — Thread 7 (landed)

The label "user need" can be a misnomer: sometimes the system doesn't serve a
human user directly — sometimes it serves another system (another
program/application module). Would "stakeholder need" be a better term? →
Adopted as `SN-###`.

### Companion-tooling survey — Thread 8 (landed) + Thread 9 (queued, Session C)

Two questions before continuing into the later threads:

1. Is there anything in the sibling project `ai-native-toolkit`
   (`C:\Projects\ai-native-toolkit`) that should be leveraged here?
2. Is the code structuring/mapping sufficient as-is? Should we consider
   integrating something like code-graph or Serena?

### Performance / NFR tracking — Threads 10 & 11 (queued, Sessions B & D)

How to thread in performance-related checks? Most test content is oriented
around LLRs/SRs (the key functional component), but there may be insufficient
audits around minimizing processing/RAM/VRAM usage and overall application
size. How should those metrics be tracked so a sudden regression — or an
already-worse-than-expected value — raises a warning/alert?

Concern: the author of a stakeholder need may not know an appropriate budget,
especially when the repo is one module within a larger whole — budgets depend
on many factors but should generally be minimized within reason. Because of
cross-module interactions, it's likely best to place budgets separately in
`performance-budgets.csv`, owned by a coordinator who can update it
independently. That costs some visibility from the functional requirements, but
also reduces clutter in the rest of the breakdown (keeps SN→SR→LLR focused on
function). Carried into Thread 10: what other non-functional requirements
should at least be *considered* (not mandated) in the template?

### Session sequencing — folded into IMPROVEMENT_PLAN.md "Sequencing & session strategy"

Original proposal: a 4-session breakdown — Threads 4/6/8 prose batch → 5/10
capture-enrichment batch → 9 solo → 11 solo — with the rationale for batching
4+6 (both touch AGENTS.md's ~12k-char budget) and pairing 5+10 (both touch
templates/EXAMPLE.md). This is now the live plan in `IMPROVEMENT_PLAN.md`'s
"Sequencing & session strategy" section — don't maintain two copies.

## Open — not yet threaded

- **Agent verbosity.** What other settings/characteristics would keep an agent
  (Opus specifically) less verbose?
- **Multi-module scoping.** Clarify that this template is currently scoped to a
  single module. A multi-module template would also be valuable for larger
  projects, but needs careful design.
- **Multi-repo coordination.** How can AI tools handle multiple repositories,
  and create new repositories for new modules?
- **End-to-end testing.** What's the best way to handle end-to-end testing,
  especially across modules/repos?
- **Coordinator-repo idea.** Maybe a single "coordinator" repository holds the
  high-level SN → SR → LLR chain, and at some point an LLR in the coordinator
  becomes the SN for a lower-level, separate-repo module. At what point does
  that handoff happen?
- **Cross-repo interface composition.** Each module could "subscribe" to a set
  of interfaces — but that gets complicated quickly. Interfaces aren't only
  code: there could be physical ones too (plugs, power, networking, an axle
  connecting components, screws joining two assemblies). Ideally these would
  compose like code interfaces do, while keeping change management legible.
  Idea: a parent interface could be a set/group/port of sub-interfaces that
  another interface links to.
- **Notes from previous search related to cross-repo interfacing** AI tools can handle multiple repositories by implementing a centralized management system that allows for easy navigation and integration between different codebases. This can include features such as repository linking, dependency management, and automated updates across repositories. Additionally, AI tools can utilize version control systems to track changes and ensure consistency across multiple repositories.
- **Other guardrails.** What other AI skills should this template make
  available? What other guardrails belong in `AGENTS.md`?

---
