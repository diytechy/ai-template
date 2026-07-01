# Scratch Notes

Brainstorming and open questions feeding `IMPROVEMENT_PLAN.md` — rough notes,
not a spec. Resolved items are tagged with the thread that addressed them, in
thread order, so this file stays a quick index of "where did that idea go."
Still-open items are grouped at the bottom for a future session.

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

### Sibling-project survey (DonnyClaude, Ponytail) — Threads 12–14 (queued, Sessions E/F)

Surveyed two sibling projects for ideas worth reusing: DonnyClaude
(`C:\Projects\donnyclaude`) and Ponytail (`C:\Projects\ponytail`).

→ Verdict: **mine ideas, don't vendor/depend.** Both are different-layer
runtime packages (npm/plugins) that violate the kit's stdlib-only /
stack-agnostic / agent-neutral constraints, so neither is a dependency or
vendoring candidate. Thread 12 = DonnyClaude as an optional runtime-harness
accelerator (PROCESS §7, mirrors Thread 8); Thread 13 = Ponytail's right-size
guardrails + a kit-neutral shortcut-comment convention; Thread 14 = the no-stub
"existence ≠ implementation" substance gate (decided: A+C — a G3 criterion plus
an optional Python-reference stub detector that ships). Take nothing wholesale
— the kit's SN→SR→LLR→TC spine is more rigorous than either sibling has.

### Onboarding & dev-environment provisioning — Thread 15 (queued, Sessions G prose + H build) + Thread 16 (stub)

Original question: should this template's setup script also provision the
surrounding dev environment (Python, ruff, git, IDE + extensions, WSL on
Windows, etc.), not just the project's own dependencies — across Windows/Linux/
Mac, possibly via Chocolatey or containers? Tension: this risks conflating
"procurement for the tool/product" with "procurement for developing the tool,"
and risks shoehorning infra choices into downstream projects that may have
different needs. Most users (~80%) probably want a shared dev environment (IDE,
extensions, supporting hardware), so a setup script should detect the IDE
(default to VS Code if none found), tell the user what it's about to install
with a short countdown to interrupt, and offer a granular choice (install all /
install required-only / cancel) rather than installing silently. Should also
support non-code contributors (art, UI, physical assemblies, electronics,
marketing/publications) — git-trackable work that doesn't require them to
understand repos or change control if an agent can commit on their behalf,
provided the workspace setup itself is trivial. Framing check from the
discussion: aim for "thin advisory, recommended" rather than a "full installer"
— a simple, consent-first "download → run → tool states intent → user accepts →
pick save location → export repo → kick off platform dev-setup" flow.

→ Resolved into **Thread 15** and **Thread 16**. Three named setup layers:
process (stdlib, nothing required) · product (stack tools) · developer
workstation (new) — plus a `Stage 0 → dev-setup → setup → check` onboarding
ladder (the Provision/Startup/Runtime split from Thread 5, applied to
development itself). Decision: **"guided skeleton"** — readable, consent-first
scripts with a native GUI folder picker (no compiled exe, no pipe-to-shell);
ensure-git + HTTPS clone (auth delegated to `gh`, never hand-rolled keygen); an
end banner naming the cloned repo dir and telling a non-code contributor they
can point an AI agent at it; then `dev-setup` (tiered `--check`/baseline/full;
code vs. domain-contributor profiles; offline renderers only). The kit ships
the skeleton and scaffolds it; signing/distributing it as a Release asset is
the downstream project's call. **Parked:** agent auto-selection/install
(banner-only for now). Thread 16 covers verifying non-code artifacts (CAD/art/
PCB/publication) — already expressible via the existing §4 Demonstration/
Inspection methods; the missing piece is render/diff tooling, which is
product-layer (sketch now, build later).

### Voice / agent personality — Thread 17 (queued, Session I)

Original question: how to get more humor/personality into an agent's feedback
— both in this repo and in repos templated from here — and whether there's a
standard convention all LLM agents could follow. Would added levity help the
human-facing experience while risking ambiguity or wasted tokens in
agent-to-agent communication?

→ Threaded into **Thread 17**. The real deliverable is the **carve-out**, not
the humor: levity is fine on human-facing surfaces, banned on the machine/
agent-facing layer (findings, subagent prompts, §5 verdicts, registries,
commits), where it costs tokens, adds parse ambiguity for the next agent, and
erodes the honesty signal. The agent-to-agent risk is real — that's the whole
reason the carve-out exists. Ship a restrained default plus an optional tone
dial, not a baked-in persona. Home for this = the AGENTS.md communication
block (single-sourced in PROCESS.md, given the character cap).

### Model/agent tiering — Thread 18 (queued, Session I)

Original question: how to force the correct model for a task. Partially
templated already, but how do we make sure agent-driven development spawns/
uses an appropriately efficient model, and bake that into the template?

→ Threaded into **Thread 18**. Honest ceiling: the kit can't *force* a model
choice — that's a host concern and doesn't standardize (the Thread 0b lesson;
gates run after the work is done). So it recommends + records instead: a
task→tier mapping extending §6 (planning/decision/high-risk → strong model;
mechanical/well-specced/prose → cheap model), the insight that **gates make
tiering down safe** (a cheap executor can't silently drift past a gate), a
recorded model-tier hint convention (the "Model tier:" line Threads 12–17
already dogfood), and host levers (opusplan, subagent overrides) offered as
optional per-host examples — not a model-selection engine (that was
DonnyClaude's rejected Claude-specific path).

### Multi-module & multi-repo coordination — Threads 19, 20, 21 (landed 2026-06-30)

Original questions: this template is currently scoped to a single module —
what would a multi-module template look like? How should AI tools coordinate
across multiple repositories, including creating new repos for new modules?
How does end-to-end testing work across modules/repos?

Original "coordinator repo" idea: a top-level repo holds the high-level
SN→SR→LLR chain; at some point an LLR in the coordinator becomes the SN for a
module that lives in its own repo. Interfaces aren't just code — they can be
physical (mounting plates, connectors, harnesses) or data (MQTT topics, signal
ranges/resolution/rate) — and ideally compose the way code interfaces do.
Worked through the ownership question: does the coordinator own one shared
interface catalog (clean single source of truth, but risks becoming an
unsustainable monolith), or does each module own/inherit its own interfaces
(avoids the monolith, but risks near-duplicate interfaces proliferating)?
Landed on: each interface is owned by whichever module defines it (or by the
purchased/reused part itself, if it's off-the-shelf and immutable); the
coordinator decides ownership only when two new components need to agree on
one, then records the result so it can be reused. Also flagged: the
coordinator needs some way to push status to module repos (a STATUS.md-style
doc, mirroring how this template already tracks repo state) — in tension with
the template's human-centered gating, but unavoidable once multiple modules
are in play, so the coordinator should perform the *mechanical* gating a
human would do and escalate only judgment calls.

(A background research pass on cross-repo tooling patterns turned up only
generic findings — centralized repo management, dependency linking, version
control for consistency — superseded by the concrete design below.)

→ Resolved into **Threads 19, 20, 21**. Split into two problems:
**multi-module, one repo** (Thread 19, Session H — near-term, mostly naming
what already exists: sub-trees by Module/Area, module-scoped gates,
integration TCs, intra-repo `IF-###`) and **multi-repo coordinator** (Thread
20, Session I — design-first). Four decisions: (1) stage multi-module first;
(2) handoff happens at the **SR tier** — a delegated SR becomes the module's
SN, back-linked, not LLR→SN; (3) assemblies are **configuration**, not
coordinator branches; (4) coordinator gating is **mechanical aggregation,
escalate judgment to the human** (the existing §6 triage, just lifted to
coordinator level). Maps onto the kit's existing grain: coordinator = the §1
Integration/Coordination hat elevated to a repo; interfaces = the §8 `IF-###`
ICD ownership model the user re-derived independently; the interface catalog
**references the owning `IF-###`, never copies it** (resolves the "giant
shared list" worry); physical interfaces are `IF-###` backed by an
Inspection/Demonstration test; cross-repo communication is **async text + PR**
(STATUS.md across the boundary), never a live bus; "no multi-repo build
system" (§8) is the guardrail. Clarified later: "no orchestration engine"
means no central *build/runtime* engine — the coordinator only coordinates
contracts and aggregates each module's self-reported gate status; the
integration/**plant** environment (assembled modules + a plant model,
SIL/HIL/E2E) is itself a delegated repo that gates itself, with the
coordinator just sequencing "deps green → trigger it." Two requirement
scopes: **module-scoped** (verified in the module repo) vs **composition-
scoped/emergent** (held in the coordinator chain, verified by the plant repo
via Demonstration). Multi-repo should be **rare** — docs lead with an
escalation ladder: (1) single-module/one-repo [default] → (2) multi-module/
one-repo [Thread 19] → (3) multi-repo+coordinator [Thread 20, only when
modules need independent versioning/ownership/release] — decided at project
creation (KICKOFF/bootstrap/G1), defaulting to rung 1, and revisitable (a
module can be promoted to its own repo later). Heavy tooling (cross-repo
trace pull-vs-push, gate aggregation, repo creation, module discovery,
cross-repo E2E) deferred to **Thread 21**, a research-grade stub.

## Open — not yet threaded

- **Agent verbosity.** What settings or characteristics would keep an agent
  (Opus specifically) less verbose?
- **AGENTS.md budget vs. guardrail coverage.** What other AI skills should the
  template make available, and what other guardrails belong in `AGENTS.md`?
  It's already filled to the Gemini quota (12 KB); some existing items could
  be consolidated, though the repetition may be worth keeping. Could be
  handled on a per-project basis.

Next set of considerations (raw dump 2026-07-01, reorganized same day):

- **Cost / economic NFRs (part cost, BOM, licensing, cloud spend).** Financial
  optimization and part-cost minimization are non-functional trade-offs the kit
  never prompts for. The §9 NFR consideration checklist anchors on ISO/IEC 25010,
  which is a *software-quality* model and omits cost entirely — yet for a
  hardware/mechatronics scope (or a cloud bill) cost is a first-class NFR. It's
  very project-specific, so the kit likely can't *mandate* a method; but *naming*
  cost as a category to consider — and noting a quantitative cost target is
  structurally already a `PB-###` row (metric + budget + `lower-better` + Gate,
  owned by the Integration hat) — would reduce rework. The broader point: make the
  non-functional attributes that need consideration harder to forget at G1.
  → **proposed: light amendment to Thread 10** (broaden the §9 checklist past
  25010's software-only set; note `performance-budgets.csv` already fits cost as a
  metric). Not a new mechanism. Low priority.

- **Documentation / publication composition (operator + technical manuals).** Can
  a composite technical/operator manual be *generated* from the doc flow — and, in
  a complex multi-repo/multi-version product, composed across repos and versions?
  The kit already generates human docs from the registries
  (`gen_release_checklist.py` from SN/SR/TC/IF), so the same single-source
  technique could *scaffold* a manual; but a full publishing toolchain (PDF / DITA
  / static site) is heavyweight, product-layer, and "don't recreate the world."
  Open question raised: is an operator manual even the right artifact anymore, or
  is a different concept (queryable / agent-navigated docs) better? → **proposed:
  new stub thread (design-first, low priority)** — name the
  generate-from-registries opportunity + the product-layer boundary; the
  multi-repo/multi-version composition is the hard half, adjacent to Thread 21.

- **Cross-repo interface-ID namespacing.** A concrete hole in the just-shipped
  Thread 20 model: each repo owns its own `IF-###` space, so `IF-001` in repo A and
  `IF-001` in repo B collide as strings when the coordinator references them. User's
  proposed fix (correct — matches distributed-id practice): each repo keeps its
  **local** id set; the coordinator references an owner interface either by the
  qualified pair `(owner-repo, IF-id)` or via a **coordinator-level id** that maps
  to it, so local ids never need to be globally unique. The coordinator-level-id
  option composes better with assemblies-as-config (a stable handle whose concrete
  owner can vary by assembly). → **proposed: fold the *principle* into
  MULTI_REPO.md §3.3/§6 now** (real gap in freshly-shipped work) + route the catalog
  *format/tool* that enforces it to **Thread 21**.
- **Parked, low priority:** the [advisor-strategy
  post](https://claude.com/blog/the-advisor-strategy) — possibly relevant to
  the Thread 18 model-tiering pattern, not yet read closely.
