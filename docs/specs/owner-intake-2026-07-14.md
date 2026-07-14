# Owner intake 2026-07-14 — eight items: triage, dedupe, WIs

Owner-handed batch (eight items), triaged against the open registry per the
change-intake flow (PROCESS.md §5). Item 1 is **feedback on the pending
OI-8/OI-9 briefs** — folded into those surfaces and the draft
[research-knowledge spec](research-knowledge.md) (pre-ratification revision),
not new decisions. **Dedupe findings first** — what already exists, so no
queued work is duplicated:

| Item | Already covered? | Disposition |
|---|---|---|
| 1/OI-8 (hierarchy at ratification) | **Partially**: the dashboard What-icicle + `trace.py`'s forest exist, but nothing batch-scoped and nothing *guaranteed* at a ratification | Answered → [hierarchy-view](#hierarchy-view); the v3 tree hand-built into the pending OI-8 brief; mechanize → **WI-146** |
| 1/OI-9 (research tier, meta packs, component web, interfaces-at-WI-time) | **Mostly answered by existing design** → [component-web](#component-web); the strong-tier preference amends the draft spec | Spec §3a/§3b/§6/§8 revised pre-ratification; meta packs were already §4.4 |
| 2 (model preference sets) | **Fully covered** — `docs/agents.csv` pair rows + `docs/agents-enabled` preference order + `AGENT_MODEL_MAP`/tier maps + the per-WI `BuildTier` pin; the live config already runs fable-plan / opus-build | No new mechanism → [model-preferences](#model-preferences). "Opus to extra high" = the deferred **WI-110** → **re-queued** (owner directive) |
| 3 (lowest-gate-first) | **Partially** — parallel-pre-dev/series-dev, `[phase]-[g*]` anchors + drop detector (WI-093), run-state coherence warn (WI-115) | Advisory gap → **WI-149** ([gate-first](#gate-first)) |
| 4 (pause + weekday blackout) | Not covered | **WI-147** (pause) + **WI-148** (blackout) ([pause-blackout](#pause-blackout)) |
| 5 (prompt→image) | Not covered; research-shaped | Answered → [prompt-image](#prompt-image); seeds the research track's **first research WI** (spec §9) — no build now |
| 6 (throughline) | Process side already covered; UI side is a domain package | Pointer note → **WI-151** ([throughline](#throughline)) |
| 7 (tier-down inference) | **Partially** — the `BuildTier` pin (WI-126) is the mechanism; assignment is manual today | Planner-assigned BuildTier rule → **WI-150** ([tier-routing](#tier-routing)) |
| 8 (knowledge kits for adopters) | **Partially** — the draft spec creates the per-repo home; *shipping a curated library* is new | Spec §4/§6/§8 extended → [knowledge-kits](#knowledge-kits); implementation WIs file at the OI-9 ratification |

## hierarchy-view

**The ask (OI-8 feedback):** at every G1/G2 ratification, present the
SN → SR → LLR tree of the batch, prose included; what restrictions/checks can
*guarantee* that view?

**What exists:** `trace.py` already builds the whole-spine forest (rendered
into `docs/test/report.md`) and the dashboard's What-icicle renders
SN→SR→LLR/TC; neither is scoped to *the batch being ratified* and nothing
requires a ratification brief to carry the view. For the pending sitting the
v3 tree is hand-built into the OI-8 brief (ephemeral by design — the section
dies at ruling).

**Guarantee ladder (the enforcement-audit vocabulary):**

- **Harness (warn-first)** — the recommended floor: a lint that an
  `## OI-N` section whose decision is a `[phase]-[g1|g2]` ratification links a
  batch-scoped hierarchy view (the WI-132 S-lint idiom; warn, never a gate
  fail — the house stance for prose surfaces, WI-129/WI-132 precedent).
- **Reviewer** — the LLM-gate ratification review charter names the view a
  required input (prompt text; catches substance the lint can't).
- **Prose** — the `gate-advance` skill's ratification section makes producing
  the view a step.

Hard-gating (hook-refusing a ratification commit without the view) is
rejected: it gates on prose shape and would fight legitimate small batches.

**WI-146 — ratification package (scripts, queued).** Done-when:
(a) a batch-scoped SN→SR→LLR/TC markdown tree **with full registry prose** is
*generated* from the registries (a `trace.py` mode or small `gen_` script:
input = a phase tag or SR-id list; output embeds Requirement/AC, LLR Detail,
TC Method/Expected, and names any rubrics), so a brief links it instead of
hand-copying rows; (b) the warn-tier brief lint above; (c) the `gate-advance`
skill + LLM-gate review prompt name the view; (d) one guidance line in the
decomposition recipe: a `[g2]` batch also authors/updates the IF-### rows its
LLRs imply (see [component-web](#component-web)). Fixture-tested both ways.

## component-web

Answers to the OI-9 architecture questions, in order:

- **How does a component store/allocate against implementation? Does it
  contain SRs/LLRs?** A component is a `CMP-###` row in
  `docs/requirements/components.csv`. **LLRs carry a `Component` column** —
  the allocation is LLR→CMP, stated once on the LLR (WI-073). A *module* maps
  to components through the LLRs that implement it (the arch-map inventory ×
  LLR Component tags — `check_trajectory.component_top_view` is the one home
  of that join). **SRs are not directly on components**: an SR's component set
  is derived through its LLRs (SR→LLR→CMP), never duplicated. The CMP row also
  carries the knowledge hooks — `Knowledge` (`;`-joined refs, including
  `docs/knowledge/` labels) and `DetailDoc` — so components are exactly the
  tie between the *what* (SR/LLR via allocation) and the knowledge that
  supports the *how*.
- **"A check that every implementation module ties back to a component" —
  it exists:** `check_trajectory.component_findings` (WI-073) warns on any
  arch-map module not contained by a top-level component (ERROR under
  `--strict` at G2+). The meta repo runs it live: 24 modules → 5 components,
  0 uncontained. The **gap** the owner's conditional exposes: the check is
  vacuous when a repo skips the CMP layer entirely. The research-knowledge
  spec (§3a, revised 2026-07-14) now couples them: **knowledge packs present
  ⇒ the component layer is expected** — a warn-first finding when
  `docs/knowledge/` holds packs but no CMP row contains a module.
- **Should interfaces be defined at WI-definition time?** Largely yes, and
  the intake flow already points there: PROCESS.md §5's change-intake routes a
  problem through **IF/CMP/PART scoping before the WI**. What's genuinely
  missing is decomposition-time authoring: when a `[g2]` batch mints LLRs that
  imply new seams, the IF-### rows should be authored/updated in the same
  batch (WI-056/057 did this retroactively for the whole kit). That guidance
  line rides **WI-146(d)**. A new `IF-Refs` column on `work-items.csv` is
  **deliberately not filed** — a registry schema change with downstream
  migration cost, not yet earned; revisit if the guidance line proves weak.
- **External start/end points and circular file references:** already
  modeled. `interfaces.csv` rows declare endpoints including file-mediated and
  external ones; the meta's 52 seams include the owner/user entry points and
  the circular edited-and-ingested hubs (`status.md`, the registries,
  `docs/stack.ini`) as first-class file endpoints.
- **Does this influence OI-8?** The two views complement: the ratification
  tree (WI-146) is the *requirements* hierarchy; the architecture-by-
  components-connected-by-interfaces view is the dashboard's How-SW
  containment + IF wiring (WI-073/056), becoming Simulink-style with
  descend-a-layer in the already-queued **WI-141** (SR-051 rev). No new WI.

## model-preferences

**Covered — no new mechanism.** The preference-set ask is the shipped routing
stack: `docs/agents.csv` (pair rows: identity + access + Env),
`docs/agents-enabled` (preference *order*; version-less resolution),
`AGENT_MODEL_MAP`/`AGENT_TIER_MAP` (per-phase), `DEFAULT_PHASE_TIER`
(PLAN/DESIGN-CHECK/CRITIQUE=strong, BUILD/REVIEW=medium), the per-WI
`BuildTier` pin (WI-126), cooldown re-route on failure (the "else another
tiered model if not available" semantics), and tier-up-never-down. The live
meta config is already the requested policy: PLAN/plan-shaped phases →
**FABLE** (strong, first in the enable order), BUILD → **OPUS** (medium,
`AGENT_MODEL_MAP BUILD=opus`), reviews cross-family.

**"Opus implementation should be set to extra high" — owner directive; the
deferred WI-110 is exactly this and is re-queued.** Scope: pin
`CLAUDE_CODE_EFFORT_LEVEL=xhigh` via the ANTHROPIC-OPUS row's `Env` (one
cell), and verify with the WI-124 telemetry (before/after `s/turn` +
`Ctx/turn` on real BUILD sessions). Effort ladder per the current API docs:
`low/medium/high/xhigh/max`; `xhigh` sits between `high` and `max` and is the
documented Claude Code default on Opus 4.8 — WI-109 recorded `high` as the
then-default, so WI-110 re-verifies the live default before claiming a delta.

**"Are there effort parameters for OpenAI?" Yes** — the API exposes
`reasoning_effort` (values `minimal/low/medium/high` on the GPT-5 family;
model-dependent extremes). The `opencode` CLI surfaces it as a per-model
config option (its config file's model options, e.g. `reasoningEffort`), not
an env var — so wiring the OPENAI rows needs an opencode config file rather
than an `Env` cell. Verifying that live is in WI-110's scope.

## gate-first

**The ask:** always clear WIs affecting the lowest gate level first, so
implementation never rides on unratified requirements; prompt NEEDS-HUMAN for
the relevant ratifications.

**Covered by design:** the derived-gate model's *parallel for pre-dev, series
for dev* workflow; `[phase]-[g1|g2]` anchor WIs + the phase-drop detector
(WI-093); the WI-145 pattern (the human sitting as an `active` registry row
that dev slices hard-depend on — the DAG itself records the pause); the
WI-115 run-state coherence warn. NEEDS-HUMAN prompting at ratification is
therefore already mechanized *when the batch is filed with the anchor +
predecessor discipline*.

**The gap → WI-149 (scripts, queued):** nothing warns when the *queue order*
violates the doctrine — e.g. `docs/next-wi` (or the queued set) points at a
dev WI whose phase still has open `[g1]/[g2]` anchor work or Draft rows below
its target level. Done-when: a warn-first `check_trajectory` finding
("dev WI-X queued ahead of open gate work WI-Y in phase Z — clear the lowest
gate first"), vacuous with no anchors/next-wi; the driver prompt
(agent-resume `AGENT_PROMPT`) gains the lowest-gate-first line; fixture tests
both ways. Never a gate fail (warn-first; the queue is owner-ordered).

## pause-blackout

Two WIs, one wrap-up semantic: **finish the in-flight session normally
(commit + telemetry), never kill mid-session; take effect at the
next-session boundary.**

**WI-147 — graceful pause (unattended, queued).** A declared `docs/pause`
file (run-phase idiom: presence = pause requested; content free-form reason).
The coordinator checks it at each session boundary: wraps the current
session, commits its own bookkeeping, and stops the loop with a clear banner
(and the run-state `ask:` line naming `docs/pause`); an `agent-resume` launch
with the file present refuses to start new work naming the file; deleting it
resumes. A TTY keypress (the WI-136 VT machinery) may write the file as a
convenience — the file is the contract. Done-when: mid-run request → clean
stop after the current session; launch-time refusal; delete-to-resume; tests.

**WI-148 — weekday blackout window (unattended, queued).** A declared
`docs/blackout` policy file: first line `HH:MM-HH:MM` (UTC, weekdays
Mon–Fri). Inside the window the coordinator **starts no new sessions**
(in-flight work wraps per the same semantic) and either waits or exits with a
banner naming the window end. `start == end` disables. **Default: weekdays
12:00–19:00 UTC**, per the owner — shipped as the scaffolded file's default so
fresh scaffolds get it; an **absent file = disabled** so existing adopters'
behavior is byte-identical (never-breaking; the owner's "always on" is
honored via the scaffold default, not a hidden built-in). Done-when: a
session start inside the window is refused with the banner + wake time;
outside unaffected; `start==end` disables; the scaffold ships the default;
tests cover the boundary minutes and the disable form.

## prompt-image

**What it would take:** a "print prompt to image" tool (text → 1-bit PNG) +
handing the image to the agent CLI. Rendering needs Pillow or platform text
rasterization — **not stdlib**, so it could never be a kit script (SR-034);
it would be a downstream opt-in tool.

**Why it loses today (the token math):** Anthropic vision pricing is
area-based (≈ `w×h/750` tokens; up to ~4,784 tokens/image on high-res
models). A page of prose (~500 words ≈ 650–750 text tokens) rendered at a
legible ~1000×1400 px costs ~1,850 image tokens — **2–3× more than the same
text as text**, before OCR-fidelity risk. It also forfeits prompt caching
(text prefix caching is the cost lever the loop leans on), grep-ability, and
determinism. The research direction the owner has in mind is real ("optical
context compression", DeepSeek-OCR-class results, late 2025: ~7–10×
compression claims) but applies to models *trained* for it with lossy
retrieval — hosted Claude/GPT tokenizers price pixels, so there is no
arbitrage on the providers this repo routes to.

**Disposition:** no opt-in built now. Filed as the research track's **seed
research WI** (spec §9): named questions = per-provider image-vs-text token
cost on three representative prompt shapes; fidelity loss at readable
resolutions; caching interaction. It files with the §8 batch at the OI-9
ratification and doubles as the track's end-to-end dogfood.

## throughline

**What it is** (fetched 2026-07-14, `github.com/jrpease/throughline`): a
Claude Code plugin that automates production design systems — Figma token
systems (light/dark, multi-brand), icon + component libraries, a
pnpm/Turborepo scaffold, a Figma→code token sync adapter, Storybook +
Chromatic visual-regression CI. Its process machinery: twelve sequential
skills, a `design-system.json` manifest tracking state/prerequisites, a
`tokens:validate` gate, a zero-reference guard, a 7-phase retrofit with human
checkpoints, model routing (expensive thinking on strong models, mechanical
work on cheap ones), and a "read-before-assert" brownfield discipline.

**What this framework already contains:** every *process* idea has a more
general counterpart here — model routing (`agents.csv` + tier maps),
gates/manifest (check.py + the registries + derived gate), human checkpoints
(gate-policy/ratification), read-before-assert (the reviewer grounding +
working-agreement evidence rules), subjective UI acceptance (the SR-047
Critique loop — stronger than visual-regression snapshots for our generated
HTML). Nothing to adopt structurally.

**What's leverageable:** as a **domain package for UI-heavy downstream
projects** — most adopters need a front end, and throughline is a worked,
vendorable design-system layer the way `FableClaudeMDForOpus` is for
guardrails and RDXmin is for token efficiency. **WI-151 (docs, queued):** one
pointer note in PROCESS_OPTIONS' vendorable-packages discussion (the WI-083
precedent — a "related opt-in" paragraph with applies-when: the product has a
UI/design-system need), plus the caveat that its manifest/gates overlap our
harness and a downstream repo should keep check.py as the single gate runner.

## tier-routing

**The ask:** the coordinator should infer when the preferred strong model
isn't necessary and run plan+build at the mid tier.

**Covered:** the enforcement point exists — the per-WI `BuildTier` pin
(WI-126: strongest-member batch rule, loud route line, escalation still wins)
and the WI-121 relax already made **medium the BUILD default**, so the
strong tier is opt-in per WI today. What's manual is the *assignment*.

**Disposition → WI-150 (docs, queued):** the honest version of "inference" is
that the strong-tier session *filing* a WI decides its tier while it still
has the design context — not a mid-loop autonomous downgrade (routing
decisions stay loud and pre-declared; silent downgrades fight the
no-silent-swap rule). Done-when: the session-protocol skill, the driver
`AGENT_PROMPT`s, and the PROCESS_OPTIONS unattended bullet gain the
assignment rule — *when filing or triaging a WI, set `BuildTier`
deliberately: `quick` for mechanical/off-spine work, default `medium`,
`strong` only where the change is design-shaping or spine-touching* — with
the skill fan-out re-synced. A mechanized classifier stays unfiled until the
WI-124 `s/turn` evidence shows the human/planner assignment leaving money on
the table.

## knowledge-kits

**Can the kit provision knowledge kits for downstream adopters? Yes — and the
staging content already targets this repo.**
`C:\Projects\ClaudeGuardChecks\skill-knowledge-library` (reviewed 2026-07-14)
holds: **21 drop-in skills** (schema-matched to `project-trajectory/skills/`;
7 field-proven), **6 research knowledge packs** (UI, rendering, inference /
perception, kinematics, simulation) and **8 field-knowledge packs** (F1–F4
NotHomeWrecker, G1–G4 gilbert; incident-backed). Its README maps skills → the
existing skills pipeline and packs → `docs/knowledge/` — and names the one
missing kit mechanism: a **domains filter** at materialize time
(`bootstrap.py --agents` currently fans out every kit skill; domain skills
must materialize only into repos that opt into that domain).

**Disposition — extend the research-knowledge campaign, don't fork it.** The
draft spec (revised 2026-07-14) gains: §4 a *kit-provisioned pack library*
surface (domain-tagged packs shipped in `project-trajectory/`, scaffolded on
opt-in — distribution of packs, distinct from the per-repo authored home);
§6 open decisions **5** (import scope — rec: the domain-general research
packs; the field packs stay project-local per the library's own
prune-before-promoting caveat) and **6** (the skills domains filter — rec:
yes); §8 the matching implementation WIs, filing at the OI-9 ratification
like the rest of the batch.
