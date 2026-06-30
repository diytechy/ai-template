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
- **Cross repo idea** Coordinator does not contain any code or definition that builds into a functional output (apart from assumbly definition noted below).  It only defines the interfaces and connections that connect / join two separate modules that are connected in different repositories.  Main contains all individual interface definitions, where an interface could be a physical connection (Nema mounting plate / screw hole pattern / Harness plug), a data interface (MQTT / A signal with required range / resolution / rate - like acceleration), interfaces are published to some domain like maven?  Local publish?  This would quickly grow but it also ensures a single interface definition contract that interfaces from other repos must adhere to?  Not sure how to rectify - on one handle, each branch off the coordinator should define a collection / assembly of modules that connect via there interfaces to define a full product.  Ideally those interfaces are sharable easily across branches (maybe even between projects?).  However, that creates a giant single list of interfaces - the shareability is nice but... is that really sustainable?  The other alternative is that each branch / assembly constructs / maintains interfaces.  The detriment is interface proliferation.  One variant might have an interface that is extremely close but different to another variant, that should have been shared.  How can the coordinator prevent that?  Is it even possible to prevent.  New direction: For each module, each module's interface can be owned or inherited by the component / module it's connecting to.  This can result in proliferation, but usually global databases end up getting proliferated anyways (1 standard to unify 15 standards just becomes 16 standards).  This also relaxes the coordinator roll.  So, the coordinator might need to define a bunch of modules to create an assembly.  Sometimes those components are purchase components (so those purchased components are the interface owner - their interface can't change), but if two new components are needed, the coordinator decides which one gets the be the interface owner, and then just records that interface in it's list that can be PR'd back into the main branch.  This way a growing list of interfaces is retained, but the coordinator is not in charge of the details.  So the entire workflow looks like:
    - This template repository can be used to instantiate a new coordinator repository and any module repositories needed by the template.
    - Coordinator defines the requirement breakdown to accomplish the high level task.
    - All SN / SR / LLR / TC are maintained in main based on current scope.
    - Coordinator repository creates first branch from main to maintain an assembly definition of modules used to create a full product, taking only applicable SN / SR / LLR / TC applicable to the branch.
    - What method should the coordinator use to understand what module repositories are required?
    - What if a module is a reuse part (like a motor) or a reusable software asset?  Should the coordinator carve out a definition (csv file?) with it's interfaces?  Link to the purchased part?
    - How would coordinator track / suggest potential modules?
    - LLR of branch becomes SN of module?
    - Coordinator communicates to agents of module repo using a text document just like STATUS.md maintains changes in repo itself.  
    - Note the coordinate likely needs to actually communicate to modules on the status.  In many ways that opposes the human element of this template, but managing gate flows from multiple modules is not tenable.  Instead, the coordinator should perform the core gating actions a human would do where possible, and only surface them up to the human user in the coordinator context when necessary.

  → Threaded (2026-06-30) → IMPROVEMENT_PLAN.md **Threads 19, 20, 21**. Split the
    two conflated problems: **multi-module (one repo)** = near-term, mostly naming
    what exists (Thread 19, Session H — sub-trees by `Module`/`Area`, module-scoped
    gates, integration TCs, intra-repo `IF-###`); **multi-repo (coordinator)** =
    design-first (Thread 20, Session I). Four decisions confirmed with the user:
    (1) stage multi-module first; (2) handoff at the **SR tier** (a delegated SR →
    module SN, back-linked — not LLR→SN); (3) assemblies as **configuration**, not
    coordinator branches; (4) coordinator gating = **mechanical aggregation, escalate
    judgment to the human** (the §6 triage at coordinator level — doesn't remove the
    human). Key alignments to the kit's existing grain: the coordinator is the §1
    Integration/Coordination hat elevated to a repo; the interface model is the §8
    `IF-###` ICD ownership the user re-derived; the interface **catalog references
    owner `IF-###`, never copies** (single-source-of-truth, dissolves the "giant
    list" worry); physical interfaces are `IF-###` with an Inspection/Demonstration
    backing test; communication is **async text + PR** (STATUS.md across the
    boundary), never a live bus; the §8 "no multi-repo build system" line is the
    guardrail. Cautions: don't reinvent PLM/SysML/ICD tooling — stay in the
    legible-text lane; keep multi-repo an **optional layer** (opt-in coordinator
    `bootstrap` variant). Heavy tooling (cross-repo trace pull-vs-push, gate
    aggregation, repo creation, module discovery, cross-repo E2E) → **Thread 21
    stub**, research-grade, deferred.
- **Other guardrails.** What other AI skills should this template make
  available? What other guardrails belong in `AGENTS.md`?  Note 'AGENTS.md' is already filled to the gemini quota (12 kb), there are some items there the could be consolidated, but the repetition could be beneficial?  That could be handled per project.
  
- **Ensure full provision.** Both in this template repositories and repositories created from this template, the repo setup script should contain dependencies for both the main project content, but also for surrounding infrastructure on applicable platforms for development.  That would include python, ruff, git, and - depending on the environment - visual studio - relevant extensions, wsl (windows), ect.  A repo setup script should exist for all applicable platforms (windows / linux / mac) to make development environment readiness as fast as possible (take advantage of choclatey?  Other bundlers?).  Sometimes it may make sense to contain these in a podman container, but care would have to be taken to ensure that doesn't block some testing where other devices need to communicate.  Problem: This can be conflated with setup / procurement for the tool itself.  It needs to be a separate development setup script to configure the development environment.  In a way this may appear anathema to this tool's core "no required tools" but since it's development related, there needs to be some baseline for testing.  The kew note is that this template can bootstrap a new project and that project's dependencies / procurement can be customized as it needs, but at the end some toolset is necessary to do the very basic view document / view code / run test suite.  How can that be crafted carefully to ensure this repo supports itself, but doesn't shoehorn in projects it templates into that might have different infra?

If user is checking out repo, they want to do development, but they might not want plugins / extensions?  In most (80% ?) cases users should share environment setup.  This means IDE, extensions, and potentially supporting hardware.

Idea: User starts setup script, it checks for IDE, and informs users it will install extensions in 10 seconds.  IMPORTANT: Rendering should not require offboard solution either, so local kroki / mermain previous ect should always install if available to the environment.  What if user doesn't have IDE?  Answer: Install one.  Visual code, because we are assuming a developer still needs to be able to cross-check low level outputs like text.  So full developer setup batch script does the following (both for this template and repos created by this template):

Setup Dependency flow:
- Script attempts to detect ide, and if it's detected, determine what extensions will allow for the view of the various artifacts (markdown, mermaid diagrams, ect) and which other programs will be installed (like python, ruff, podman).  Note if IDE is not detected, script chooses visual code. The most important part - The development setup script must be able to be run from any development platform (mac / linux / windows), the only case this would not be true is if the scope of the application m/ module is a runtime environment that is restricted to a single platform (like a powershell 7 script that performs some complex operations - that would only realistically need development in windows and as such only needs a development setup file in batch, no sh file(s) required.)
- Informs user applications and extensions will be installed or updated to view documentation and diagrams in 10 s, press any key to interrupt and review tools before proceeding.
- If user press key, present user with list of programs and extension intended to installed.  User is given the choice to install all, install only those required for development, or to cancel and close.

Noted during discussion, just to keep my own framing in perspective:
Before proceeding, let's make sure we're aligned on what the scope of the decision really entails.  I am amicable to "thin-advisory-recommended" but what I'm envisioning is probably still splashing into "full-installer-rejected".  I want the the user to have a simple "download this thing"-> user runs it -> It indicates in cli what it's going to do -> User accepts if they want to proceed -> Tool kicks off window for the user to choose where they want their repo to be saved -> Tool exports repo and then launches the dev tool setup scripts according to the platform.

Some developers are not developing code, they may be developing art / UI elements, they might be developing physical assemblies or electrical circuits.  They may be developing publications / marketing material.  That act of design and iteration for projects using this template would still live as reviewable changes in git, but the contributor needs their focus on their design skills within a domain, I'm trying to avoid forcing non-code developers to have a detailed understanding of repositories and change control when ai agents can commit / push their work for them, but that is predicated on getting the machine / workspace setup very easily and still take advantage of the change management  and reviewability that git offers.  Of course that bubbles up an entirely new question - how would those sort of artifacts be "tested", but it is still possible.  Point is I want onboarding to be trivial - not required reading - but again - there is a balance to all these wants.

→ Resolved (2026-06-30) → IMPROVEMENT_PLAN.md **Thread 15** (queued, Sessions G prose
  + H build) + **Thread 16** (stub). Untangle "setup" into three named layers
  (process = stdlib, none required · product = stack tools · developer workstation =
  new) and a `Stage 0 → dev-setup → setup → check` onboarding ladder (≈ Provision/
  Startup/Runtime *for development*, Thread 5). Decision = **"guided skeleton"**:
  readable, consent-first scripts with a native GUI folder picker (no compiled exe,
  no pipe-to-shell); ensure-git + HTTPS clone (auth delegated to `gh`, never
  hand-rolled keygen); an **end banner** naming the cloned repo dir + telling a
  non-code contributor they can point an AI agent at it; then kick off `dev-setup`
  (tiered `--check`/baseline/full; code vs. domain contributor profiles; offline
  renderers only). Kit ships the skeleton + scaffolds it; signing / serving it as a
  Release asset is the downstream project's call. **Parked:** agent auto-selection/
  install (banner-only for now). **Thread 16:** verifying non-code artifacts (CAD/
  art/PCB/publication) — already expressible via the §4 Demonstration/Inspection
  methods; the missing render/diff tooling is product-layer (sketch now, build later).

Other considerations:
- Donnyclaude (C:\Projects\donnyclaude)
- Ponytail (C:\Projects\ponytail)
  → Surveyed 2026-06-30 → IMPROVEMENT_PLAN.md Threads 12–14 (queued, Sessions E/F).
    Verdict: **mine ideas, don't vendor/depend** — both are different-layer runtime
    packages (npm/plugins) that violate the kit's stdlib-only / stack-agnostic /
    agent-neutral constraints, so neither is a dependency or vendor candidate.
    Thread 12 = Donny as an optional runtime-harness accelerator (PROCESS §7, mirrors
    Thread 8); Thread 13 = Ponytail's right-size guardrails + a kit-neutral
    shortcut-comment convention; Thread 14 = no-stub "existence ≠ implementation"
    substance gate (decision-first, like Thread 7). Dump nothing — the kit's
    rigorous SN→SR→LLR→TC spine is exactly what neither sibling has.

Voice:
- How to get more humor into agent's feedback?  How to augment agents "personality" to add a bit of levity or light-heartedness?  That applies both to this repo itself but also repos templated from here.  Is there a standard proceedure that all llm agents can work off?  That's nice / encouraging for user, but could that be negative for agent to agent communication?  Any risk there?
  → Threaded (2026-06-30) → IMPROVEMENT_PLAN.md **Thread 17** (queued, Session I).
    Real deliverable = the **carve-out**, not the humor: levity is fine on
    **human-facing** surfaces, banned in the **machine/agent-facing** layer
    (findings, subagent prompts, §5 verdicts, registries, commits) where it costs
    tokens, adds parse-ambiguity for the next agent, and erodes the honesty signal.
    Yes, agent-to-agent risk is real — that's why the carve-out exists. Ship a
    restrained default + an optional tone dial, **not** a baked-in persona. Standard
    home = AGENTS.md communication block (single-sourced in PROCESS.md given the cap).

Token / Agent efficiency:
How to force correct model for task? That's already been templated to an extent, but how to make sure during agent driven development an appropriate agent is used or spawned for efficiency.  How can that be baked into the template?
  → Threaded (2026-06-30) → IMPROVEMENT_PLAN.md **Thread 18** (queued, Session I).
    Honest ceiling: the kit **can't force** a model (host concern, doesn't
    standardize — the Thread 0b lesson; gates run after the work). So it
    **recommends + records**: a task→tier mapping extending §6 (planning/decision/
    high-risk → strong; mechanical/well-specced/prose → cheap), the insight that
    **gates make tiering-down safe** (a cheap executor can't silently drift), a
    **recorded model-tier hint** convention (the "Model tier:" line Threads 12–17
    already dogfood), and host levers (opusplan, subagent overrides) as optional
    per-host examples. No model-selection engine (that was DonnyClaude's rejected
    Claude-specific path). The advisor-strategy link below is this pattern, generic.

Maybe for later, not really important:
https://claude.com/blog/the-advisor-strategy?
---
