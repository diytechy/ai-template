# Integration Plan — ClaudeGuardChecks findings → ai-template kit

**Date:** 2026-07-10 · **Status:** ✅ **LANDED (Phases 1–5) + archived** — the
ai-template-side integration is done and traced by WI-045…049 (commits b443c9d,
379ed76, e6afac7, 73b5bd0, plus the Phase-5 effort paragraph); Phase 6 (closure)
is this archiving act. The **one open remnant is external**: Phase 2's *upstream
content enrichment* (a JUDGMENT.md playbook + the claim vocabulary), owner-ruled
to be done **in `TheColliny/FableClaudeMDForOpus`** and pulled downstream via the
vendoring layer, never redistributed by this kit. This file is a **field-report
input**, kept for the integration rationale — not a working surface.
**Inputs:** `OVERVIEW.md` (the 2026-07-09 first-pass triage of all 12 sources,
retained in the external ClaudeGuardChecks reference checkout) + the 2026-07-05
Guardrails-Kit review conclusions.
**Goal:** integrate the durable findings into `ai-template` so they **disperse to
downstream adopters** through the kit's existing channels — not as new machinery.

---

## Ground rules (all pre-existing ai-template doctrine; restated once)

1. **Licensing / provenance.**
   | Source | License | Handling |
   |---|---|---|
   | fable-method | MIT | may adapt with attribution recorded in plan/log |
   | stop-subagent-fanout | MIT | may adapt with attribution (re-implemented, see Phase 4) |
   | effortmining | MIT | idea only; no code needed |
   | fable5-methodology | **none** | distill ideas in kit voice; never transplant prose |
   | FableClaudeMDForOpus | none — **owner's own repo** | free to edit/extend directly |
   | Reddit threads 1–3 | informal user content | distill; credit as "external synthesis" in the plan entry, not in shipped templates |
2. **Vendored, not shipped.** Agent-behavior *content* reaches downstream repos
   via the tier-conditional guardrails layer (PROCESS_OPTIONS: repo vendors an
   upstream verbatim under `docs/guardrails/`, pinned by `UPSTREAM`, drift-checked
   by `check_vendored.py`). The kit never redistributes third-party text.
3. **Byte budgets.** `AGENTS.template.md` and `PROCESS.md` are budget-watched;
   anything that doesn't fit the working agreement goes into the vendorable
   playbooks instead.
4. **Stdlib-only, agent-neutral core.** Any *code* adoption is re-implemented in
   stdlib Python 3.8+; Claude-specific config ships only through the per-agent
   materialization path (`bootstrap.py --agents claude`), never the neutral core.
5. **Process compliance.** Each phase lands as a WI row (+ `SpecRef` → this
   file's anchors, once the SSOT restructure adds that column). Phase 4 is the
   only phase adding SR/LLR/TC spine rows.

---

## Disposition of all 12 sources

| Source | Disposition | Phase |
|---|---|---|
| reddit thread 2 (15 commandments) | **distill** → working agreement + playbook | 1, 2 |
| FableClaudeMDForOpus (Guardrails Kit) | **extend** → the reference vendorable upstream | 2 |
| fable5-methodology | **distill** → enforcement-audit discipline + CONTEXT rules | 2, 3 |
| fable-method | **distill** → reviewer-charter language + eval model reference | 3 |
| stop-subagent-fanout | **adapt (code)** → stdlib spawn gate | 4 |
| effortmining + reddit thread 3 | **document** → per-phase effort recipe | 5 |
| magic-compact | reference only — external validation of the status.md-prune design | 6 |
| DeepReason | reference only — adversarial-review harness design notes | 6 |
| craft | reference only — notebook idea noted against the trajectory layer | 6 |
| reddit thread 1 | mined; discounted (LLM-written; one durable comment already reflected in kit stance) | 6 |
| webify-mcp | no action (orthogonal utility) | 6 |
| lytenyte, engram | no action (out of scope) | 6 |

---

## Phase 1 — Distill thread 2's commandments into `AGENTS.template.md`

**Target:** `project-trajectory/AGENTS.template.md` "Working agreement".
**Constraint:** byte-budgeted — run the `byte-budget-guard` skill before/after;
overflow goes to Phase 2's playbooks, not the template.

Mapping pass first (avoid restating what's already there):

| Commandment | Already in working agreement? | Action |
|---|---|---|
| scope is a promise / the silent extra destroys trust | partially ("don't change unrelated code") | sharpen to the promise framing |
| when reality contradicts the plan, the contradiction IS the deliverable | no | **add** |
| every line is a liability | implied by "edit conservatively" | **add** (5 words, high leverage) |
| your confidence is data about you, not the code | no | **add** |
| fluent ≠ true / never report a claim you haven't watched be true | yes (self-test/evidence rules) | skip |
| run the thing | yes (verify discipline) | skip |
| one-way vs two-way doors; ask by reversibility | partially ("ask before irreversible") | tighten wording only if budget allows |
| timebox the struggle; kill sunk costs | no | playbook (Phase 2), not template |
| manage context as a finite resource | covered by status.md/R3 doctrine | skip |
| ask one good question, not five hedges | no | playbook (Phase 2) |

**Deliverables:** the 3–4 added lines; byte-budget report (before/after); plan
entry crediting "distilled from an external synthesis (Reddit, 2026-07)".
**Effort:** small (one short session). **No spine change.**

---

## Phase 2 — Enrich the sibling Guardrails Kit as the reference vendorable upstream

**Target:** `C:\Projects\FableClaudeMDForOpus` → `TheColliny/FableClaudeMDForOpus`
(owner's repo — no licensing friction), plus one paragraph in ai-template.

1. **New playbook** `docs/guardrails/JUDGMENT.md` (or extend TRAPS.md): the
   thread-2 distillate that didn't fit the template — timebox-the-struggle,
   sunk-cost kill rule, one-good-question, one-way/two-way doors.
2. **Fold in fable5-methodology's CONTEXT-class rules** (the ones its own AUDIT.md
   classifies as unmechanizable judgment — e.g. one-hypothesis-per-change,
   reproduce-before-fix). Distill, don't copy: no license.
3. **Adopt the claim vocabulary** (`Verified:` / `UNVERIFIED` markers) from the
   Guardrails Kit review + fable-method's judge — every guardrail rule should
   leave a **greppable transcript artifact** ("paste, don't check"), which is the
   single most transferable idea in the whole checkout.
4. **ai-template side (one paragraph):** PROCESS_OPTIONS "Tier-conditional
   guardrails" currently describes the vendoring mechanism with **no worked
   example**. Name this repo as the reference upstream: an example
   `docs/guardrails/UPSTREAM` pin block + the recommended
   `all except <frontier>` policy line it already documents.

**Deliverables:** upstream repo commits; one PROCESS_OPTIONS paragraph + example
pin; version bump in the upstream so `check_vendored.py` semantics are exercised.
**Effort:** medium (most work is in the sibling repo). **No spine change.**

---

## Phase 3 — Enforcement-audit discipline ("which file enforces this tomorrow?")

The best transplantable *idea* in the set (fable5-methodology `AUDIT.md`).
The kit already answers this question for **requirements** (trace + gates); this
extends it to the **behavioral rules** it ships.

1. **PROCESS_OPTIONS subsection** (short): every working-agreement / process
   rule gets a named enforcer class, in kit vocabulary —
   `git-hook/CI script` (deterministic) → `reviewer charter` (independent agent)
   → `prose guide` (judgment; the honest CONTEXT class) → `test/eval`.
   Rules with no enforcer are flagged honestly, never left as wishful text.
   *(This is the four-layer HOOK/AGENT/CONTEXT/EVAL model, renamed to the kit's
   own mechanisms; zero WISHFUL without stated reason is the audit's bar.)*
2. **One-time audit table** over `AGENTS.template.md`'s working agreement +
   PROCESS.md's disciplines, applied to the meta-repo itself. Known first
   finding (from the 2026-07-10 deep review): **TC-034** ("scripts are
   stdlib-only") is an Inspection that is trivially mechanizable — a ~20-line
   AST import scan in the suite upgrades it to Method=Test, Automated=Yes.
3. **Reviewer-charter language** (fable-method's judge, MIT): fold into the R1
   REVIEW-A/B charter text — *"an implementation report is a set of claims;
   verify by re-running the claimed checks, believe nothing unobserved."*

**Deliverables:** PROCESS_OPTIONS subsection; the audit table (docs/, meta-repo);
TC-034 upgrade (spine edit: TC Method/Automated + new test — small, rides the
next re-attestation); charter text edit.
**Effort:** small-medium. **Spine change:** TC-034 row + one test.

---

## Phase 4 — Subagent-spawn gate for the unattended layer (the one code adoption)

Adapted from `stop-subagent-fanout` (MIT; single-file PreToolUse gate). The
kit's autonomous `agent_loop` currently has **no fan-out control** — a session
it launches can spawn subagents freely.

**Design (kit-shaped, not a port):**
- **Re-implement in stdlib Python** (~100–150 lines; original is Node — kit
  scripts are stdlib-py). MIT attribution recorded in the plan entry.
- **Semantics:** deny-by-default for subagent-spawning tool calls during
  unattended runs; interactive runs ask. Override is an env var
  (`SUBAGENT_GATE=allow`) **held by the human who launched the run** — set in
  the launcher environment, never writable by the model. Fail-open on gate
  error (a broken gate must not wedge tools) **with a paper trail**: every
  decision appended to `docs/iteration/<session>/subagent-gate.log`.
- **Shipping path:** agent-*specific* hook config (Claude `PreToolUse`) is
  materialized only via `bootstrap.py --agents claude` (the skills pattern) —
  the agent-neutral core is untouched (Codex has no hooks; the neutral floor
  stays git+CI). A `docs/subagent-gate` declared-policy word
  (`off|ask|deny`, absent = off) keeps it opt-in and vacuous for non-adopters.
- **Honesty note carried over from upstream:** this is *supervision*, not a
  security boundary — a model that can edit files can remove it. Say so in the
  docs, exactly as the kit already does for hooks generally.

**Deliverables:** the gate script + policy word + materialization wiring;
**new SR** (unattended Area) + LLR + TC + tests (gate fires, override works,
fail-open logs, non-adopter vacuous).
**Effort:** medium (one full session). **Spine change: yes — the only phase
that adds an SR; schedule against a planned re-attestation sitting.**

---

## Phase 5 — Per-phase effort routing (docs only)

`AGENT_CMD_MAP` per-phase command templates can already carry an effort choice
(an effort-tiered agent file or CLI flag per phase) — no code is needed.

**Deliverable:** one PROCESS_OPTIONS paragraph in the unattended layer:
- Tier effort by task class (grep-phase ≠ crash-debug phase).
- **Caution 1 (evidenced):** at low effort the model doesn't just skim — it
  *fabricates* (effortmining's published finding); route hard work **up**.
- **Caution 2:** the mechanism only bites via agent-frontmatter effort (verified
  in thread 3's comments; prompt-level cues are ignored on subagents) — keep the
  layer thin and replaceable, since native per-spawn effort will likely obsolete it.

**Effort:** trivial (rides any docs commit). **No spine change.**

---

## Phase 6 — Closure

- Record the reference-only dispositions (table above) in the plan entry so this
  checkout reads as *resolved*, the TEMPLATE_REVIEW pattern.
- Move/copy `OVERVIEW.md` into ai-template `docs/archive/` as a field-report
  input (this file goes with it once converted to WIs).
- Convert phases to WI rows.

---

## WI conversion stubs (fill ids on ingest; SpecRef = this file's anchors)

| Title | Workstream | SR-Refs | Predecessors | Notes |
|---|---|---|---|---|
| Working-agreement distill (thread-2 commandments) | docs | — | — | Phase 1; byte-budget-guard before/after |
| Guardrails upstream enrichment + worked-example pointer | docs | — | Phase-1 WI | Phase 2; work mostly in sibling repo |
| Enforcement-audit subsection + audit table + TC-034 upgrade | scripts | (TC-034's SR-034) | — | Phase 3; small spine edit |
| Reviewer-charter claims language | docs | — | — | Phase 3.3; can merge with above |
| Subagent spawn gate (stdlib) + policy word + materialization | unattended | **new SR** | WI-024;WI-025 | Phase 4; the only new-SR item |
| Per-phase effort recipe paragraph | docs | — | — | Phase 5 |
| Closure: dispositions + archive OVERVIEW | docs | — | all above | Phase 6 |

## Owner rulings needed before ingest

1. **Phase 2 home:** enrich `FableClaudeMDForOpus` in place vs. a fresh curated
   repo (recommendation: in place — it's already published and already the
   reviewed sibling).
2. **Phase 4 scope approval:** new SR under the unattended Area (R4 new-SR
   escalation path applies).
3. **Phase 3 audit surface:** working agreement only, or also the PROCESS.md
   disciplines (recommendation: both, one table).
4. **Sequencing vs. the SSOT restructure:** recommendation — SSOT restructure
   first (it creates the `SpecRef` mechanism these WIs should use), then
   Phases 1→6 in order; 1, 5, 6 can share one session.
