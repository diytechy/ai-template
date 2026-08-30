<!-- Copied verbatim on 2026-08-30 from C:/Projects/ai-template-plans/knowledge-pack-review/00-SYNTHESIS.md — the plan of record for the rows that cite it; its companions there (the source reports, the prototype, the drafts, the review transcripts) stay outside the repo. -->

# Knowledge-pack review — synthesis (2026-08-29)

Ten links reviewed by five Opus agents; source reports `01`–`05` in this folder (3,128 lines).
`ai-template` was **read-only** throughout — another session was mid-WI-534 in the working tree
the whole time, so any numbers below were taken at HEAD `fb482e95` via `git show`, not the tree.

The kit's three landing zones for anything kept (from `PROCESS_OPTIONS.md` "Skills layer" and
"Research track & knowledge packs"): a `scope: kit` skill (`skills/<name>/SKILL.md`, ~20–30
lines, three-way byte-identical fan-out), a **knowledge pack** (`knowledge/<label>.md`, advisory,
never gates), or a PROCESS/AGENTS rule (both near their byte caps — `AGENTS.template.md` is at
9,980 / 10,000). A fourth non-kit surface is `EXTERNAL_SKILLS.md` ("mine, don't install").

---

## 1. Verdict per link

| # | Source | What it is | Verdict | Report |
|---|---|---|---|---|
| 1 | **cbrock84/headcount** | 143 business-function Claude Code plugin skills, 2 days old, 84 recycled from author's prior repos | **Payload excluded; one real mechanism** — the *write-surface ownership map* (agents split by exclusive write globs, machine-checked **total** and **disjoint**) and the `check`/`diff` guard split. Kit has no analogue; gated on Q1 below | 01 |
| 2 | **Reddit — multi-agent orchestration** | 37 comments, mostly vendor plugs | Corroborates the kit's five-tier roster and "artifact is the completion signal". **Nothing new** beyond the partial-search rule (C1) | 02 |
| 3 | **Reddit — "My Opus 5 solution"** | Phase-per-clean-session with Contract + Verification | Re-derives `WI row + fresh headless session`. Yields one sharpening: **spec-determinacy as the `BuildTier` discriminator** ("cites a pattern" → medium; "figure out" → strong) | 02 |
| 4 | **Reddit — stop adding every correction to docs** | 62 comments; the best thread | Gives the **mechanism** behind PROCESS §3's "reads stand-alone to someone with none of your history": the parenthetical is the model's *receipt* for compliance, so prohibitions decay and **context isolation + a redirect home** outlast wording. Kit already owns both the rule and the redirect targets; lacks the mechanism text and a restatement test | 02 |
| 5 | **Yu-369/VibeCurb** | 348 KB of aesthetic prompt dogma across 7 monolithic SKILL.md files, stale, CLI doesn't implement its README, writes into `.agents/skills/` | **Exclude wholesale — actively hazardous to an adopter** (turns `--check-agents` red). Mine only the motion Accessibility/Technical check tables and the greppable "three-curve maximum" | 03 |
| 6 | **Reddit — don't downgrade from Opus 5** | Orchestrator/executor split; OP's hook-injected rule failed, the split worked | Natural control in-thread (`scytob`): **ground truth is the discriminating variable, not the model** — OP has no test suite. This is the kit's own §6 thesis corroborated from outside; bounds transfer to gated repos | 02 |
| 7 | **bendrape1-byte/silk-design** | A real design method: nine CSS role tokens + one `--radius` knob; 23 consistent theme templates; thin-router skill structure | **Mine the token architecture** (it is 0→A→B applied to CSS) into the existing `knowledge/ui-design-systems.md`. **Zero accessibility content** — no `prefers-reduced-motion`, Lenis scroll-jacking with no escape hatch; fails the kit's own `ui-accessible-component` Done-when. Runtime React/GSAP assets excluded | 03 |
| 8 | **Avtr99/antidote** | Already vendored | **No re-vendor**: upstream HEAD == pinned sha `8e0350e3`, SKILL.md byte-identical. Nothing else in the repo worth taking. One *method* nugget: with/without-skill oracle benchmarking (numbers are author-run, tiny N) | 03 |
| 9 | **Rixels (4J / Reforj)** | Texel = two colours + index into 23 analytic vector shapes | **Exclude as a skill**: patent-pending, no spec/SDK/code, art-style-locked; the 98% is against *uncompressed* RGBA8 (vs BCn baselines it's ~62–91%), and public numbers don't close internally (~9× gap). Not novel — Tumblin & Choudhury's *Bixels* (EGSR 2004) family. Value: one ladder rung + the "re-base the denominator" lesson | 04 |
| 10 | **CodeAbra/iai-personal-memory-engine** | Serious local MCP memory engine: Python+Rust+TS, a dozen heavy deps, encrypted per-machine store | **Exclude entirely** — inverts every property the kit's git-shaped SSOT depends on (undiffable, unreviewable, absent on a teammate's box). Its benchmark-honesty rules are already kit doctrine | 01 |

**Honest yield:** the orchestration material mostly re-derives what the kit already specifies —
worth knowing as corroboration, worth *not* rewriting. The genuinely new items are few, and the
most valuable one for your stated interest came from the complexity survey (report 05), not the
links.

---

## 2. The compact-code / complexity finding (report 05) — read this first

**The kit is already better instrumented than the literature recommends** — three armed ratchets
(`test_complexity_ratchet.py` C901 per-function, `test_module_size_ratchet.py`, the import-layer
SCC test), a warn-only dupes census, byte caps, PROCESS §3 doctrine, the vendored antidote skill.
The problem is **four blind spots, not missing sensors**:

| Blind spot | Evidence at HEAD |
|---|---|
| **Nothing ships.** All three ratchets live in `tests/`, `scope: this-repo`; the C901 one `skipif`s without ruff | An adopter inherits prose + a warn-only dupes census — no complexity sensor at all |
| **Cyclomatic misses nesting.** Of 179 script functions over cognitive 15, only 43 appear in the 47-entry C901 baseline — **136 are invisible to ruff**; 41 of 199 have textbook McCabe ≤ 10 (validated prototype, see `complexity-pushback/prototype/`) | `traj_views.py::_layer_edges` cog 26 / cyc 10; `traj_graph.py::_seg_hits_rect` 19/7; `dispatch.py::_poll` 20/9 |
| **`tests/` is unratcheted on complexity** (77k lines, 20 functions over 15) | `test_import_layers.py::import_graph` is cognitive **58** — the 7th-worst function in the repo lives *inside a complexity sensor* |
| **No sensor for what predicts defects best**: relative churn, net-LOC per WI, interface surface | 4.3% of 775 commits are net-negative; `agent_common.py` exposes 59 public symbols |

Growth baseline: `project-trajectory/scripts` **1,792 → 67,351 lines in 11 weeks**; `tests/`
667 → 76,979; the last fortnight was the largest ever. Cyclomatic here is 61% explained by SLOC;
cognitive only 35% — so cognitive adds real information, and the 47-entry C901 baseline is partly
a ruff-version artifact (ruff-CC vs textbook-CC r = 0.727). **Erratum (2026-08-29, later the same
day):** report 05's per-function cognitive figures came from an unvalidated walker and read high;
the validated prototype's census (199 over 15: 179 scripts + 20 tests; worst
`plan_runner.run_dual_plan_round` 95, `plan_round.record` 61 not 135) supersedes them everywhere.

**The load-bearing conclusion:** three independent sources converge — the ETH AGENTS.md study
(context files don't improve success, cost > 20% more tokens; *specific* instructions are followed,
overviews aren't), Anthropic's own "if Claude already does it, delete the rule or convert it to a
hook", and **this repo's own 48-day natural experiment: capped doc +2.6%, byte-*watched* docs +91%
and +1,101%**. A prose rule about compactness is near-worthless; a mechanical check is worth
building. So: **do not add a compactness rule to CLAUDE.md/AGENTS.md. Build the sensor.**

Two rulings constrain every proposal: **D-7** (the gating dupes census was torn down — 93%
accepted idioms, blind to both real drift incidents; any new duplication gate is dead on arrival)
and **OI-16** (owner: "the monolith risk was really function size/complexity, not file size";
whether the line ratchet retires is a banked open question).

---

## 3. Ranked distillation backlog

Ordered by (value to the complexity concern) × (evidence) ÷ (machinery added). Nothing here is
applied; each needs a WI. Items marked **[ruling]** need an owner decision first.

| Rank | Item | Surface | Source | Cost |
|---|---|---|---|---|
| **1** | **`check_complexity.py`** — stdlib-`ast` Sonar cognitive complexity + SLOC per function, public-symbol count per module (reported); central TSV baseline `docs/complexity-baseline`, exact-equality both directions, `--restamp`/`--report`, **no inline pragmas**; ships `--report` only, arming is an opt-in layer. **Offered as a trade [ruling]**: land it and retire `test_module_size_ratchet.py` on the same ruling (OI-16) — net-zero instrument count, strictly better axis. Arm against `tests/` too | new script + PROCESS_OPTIONS layer + `stack.ini` step | 05 P1 | ~200 lines script, ~150 tests, ~190-row seeded baseline; two sittings |
| **2** | **`deep-module-design` skill** — the one real content gap: state the secret in one sentence; size interface against what it hides; a pass-through is a defect; define errors out of existence; two call sites before extracting; a flag on a shared helper means go *back* (re-inline, then re-abstract); branches-as-table; extract on purity; **no line-count rule** (evidence rejects 5-line methods) | `skills/deep-module-design/` `scope: kit`, < 4 KB | 05 P2 | one sitting + INDEX regen |
| **3** | **"A structural move is its own commit"** — moves and changes never share a commit; a pure move is proven by *equality* (byte-identical symbols, node-id set equality), not a green suite. Formalizes what WI-521 slices 1–2 already did | PROCESS.md §3, one bullet (~450 B on a watched file) | 05 P3 | zero machinery |
| **4** | **Partial-search rule** — "not found in the path I checked" ≠ "does not exist"; corroborated by this repo's own four value-vs-constant-name blind spots | `AGENTS.template.md` one bullet — **must be paid for by tightening another** (20 B headroom) | 02 C1 | bytes only |
| **5** | **`subagent-brief` skill** — the seven-part contract three threads independently reinvent: exact delta · output artifact · stopping condition · explicit exclusions · compact structured return · no recursive delegation · completion is the artifact. Pairs with `subagent_gate.py` (governs *whether* to spawn, says nothing about the brief). Fold in headcount's six-section return contract ("what was checked and found clean") | `skills/subagent-brief/` `scope: kit` | 02 C2 + 01 N3 | one sitting |
| **6** | **Receipt doctrine + fresh-context restatement test** — the mechanism behind §3's stand-alone rule and a cheap verification: hand the cell to a reader with no history; if they can reconstruct the correction, it's provenance | `spine-authoring` skill body + one sentence of mechanism in §3 | 02 C3 | bytes |
| **7** | **Spec-determinacy `BuildTier` discriminator** + inline-vs-dispatch three conditions | PROCESS_OPTIONS "Per-WI build tier", PROCESS §6 | 02 C4 | bytes |
| **8** | **`visual-system-floors` skill** — the UI gap the kit *uniquely* owns: closed scales, one-concept-one-colour with a measured ΔE floor, both-theme contrast, default density — solved and enforced here (`docs/rubrics/dashboard-*.md` U1–U5/A1–A4/T2–T8 + tests) and distilled nowhere an adopter can reach **[ruling: `domains: [web]` vs `[any]`]** | `skills/visual-system-floors/` + extend `knowledge/ui-design-systems.md` | 04 P2 | one sitting |
| **9** | **Extend `knowledge/ui-design-systems.md`** — silk's nine-role/one-radius token architecture as a *named alternative* to Radix scales with the trade-off stated (compact, rebrand-in-one-edit vs guaranteed contrast steps) **[ruling]**; VibeCurb's a11y motion rows (`@media (hover:hover) and (pointer:fine)`, `aria-label` on split text, WCAG 2.2.2 pausable, transform/opacity-only, IntersectionObserver, Lenis `smoothTouch:false`); the greppable three-curve max. With attribution + pinned shas | knowledge pack (0→A→B: one UI home, not a fourth UI skill) | 03 B1/N1/N3/N4 | one sitting |
| **10** | **`texture-budget-ladder` skill** — budget on the lowest supported device first; climb delete → compress (BCn/ASTC via KTX2/Basis) → pack → mip/stream → atlas → procedural → analytic-detail → virtual texturing; exit = pasted before/after byte counter; needs a new `knowledge/texture-memory.md` | `skills/texture-budget-ladder/` `domains: [game, web]` | 04 P1 | one sitting |
| **11** | **Relative-churn sensor** — `git log --numstat` parse, ~80 stdlib lines, churn ÷ SLOC per module + net-LOC per WI; **report-only permanently** (D-7 posture); a reading list for review rounds and a WI-521 prioritizer | new script | 05 P5 | small; no precedent in the instrument set |
| **12** | **`EXTERNAL_SKILLS.md` rows**: silk-design (caveat: zero a11y), VibeCurb (caveat: broken CLI, IF-035 violations), headcount (mine `executive:agent-hierarchy`'s playbook only), Vercel Web Interface Guidelines (**licence unverified**; prefers APCA — don't adopt its contrast rule wholesale); **amend** the `anthropics/skills` row — `frontend-design` is a design-*quality* skill, not an "orthogonal task tool" | doc rows | 01 C5, 03 B3, 04 §4 | trivial |
| **13** | `gen_skills_index.py --check` description-length floor | 2 lines | 01 N4 | rides any WI |
| **14** | Per-model posture payloads (extend "Tier-conditional guardrails" to one payload per model substring, reusing the existing `[policies] guardrails` matcher; no kit-owned model names) | `agent_loop.py` small delta | 02 C6 | small |

### Route to plans, not the kit (need a ruling and a kill criterion before code)

- **Delta-vs-ask reverting pass** (02 C7) — the only proposal that would close a gap
  `docs/enforcement-audit.md` openly declares ("every line is a liability → Reviewer, no hard
  check"), and the one most likely to become a false-positive machine. Has the exact geometry of
  `check_dupes.py` (deleted at D-7). Prompt-side in the reviewer brief first; script-side unbuilt
  until it earns it, shipped with its own kill criterion.
- **Write-surface map + `check_surfaces.py`** (01 C1/C2) — **Q1 gates it**: claim-branch isolation
  already means two workers never share a tree; the map earns its keep only in a shared-tree
  model. If the answer is "branches solve it", it collapses to a skill paragraph with no script.
- **Skill-efficacy measurement** (03 B4) — 30 shipped skills, zero evidence any changes model
  output; antidote's with/without-oracle method is the template. Collides with the stdlib bar and
  `llm-vision-convergence-loop`'s turf; research plan only.
- **Stall-guard tier escalation** (02 P2) — behaviour change to `agent_loop.py` with cost
  implications; interacts with tier-up-never-down.
- **Effort non-monotonicity hypothesis** (02 P3) — "high effort over-builds": 2 anecdotes vs the
  kit's ~450-run evidence on a different axis; measurable here by holding the WI constant and
  varying effort. Knowledge-pack open question, not a rule.
- **Critique→test migration** (04) — the most transferable idea in the UI material (an anchor
  stops being a verdict and becomes an assertion; a dissenting critic files a test gap, not a
  finding) but it's a gate method, not a UI one — possible `gate-advance` companion.

---

## 4. Excluded — and why (consolidated)

| Excluded | Why |
|---|---|
| headcount's 143 business skills; its plugin/marketplace packaging; `agent-guard.mjs` as vendored Node | Scope (an engineering-process kit has no `finance:*` adopter); restates enforced gates as suggestions; every description loads into context on every session; marketplace packaging breaks three-agent neutrality; a Node shipped check forces every adopter to install Node |
| iai-pme in any tier; MCP-server integration generally | numpy/scipy/numba/pandas/cryptography/Rust/Node against a stdlib-only kit; encrypted per-machine undiffable store inverts the git-shaped SSOT; a daemon a gate cannot assume is a daemon a gate cannot use (the context7 argument, already made in `EXTERNAL_SKILLS.md`) |
| All eleven vendor plugs in thread 1; Claude-Code-harness internals; "ask Claude how to use Claude"; brand advocacy; token-economics claims | Unvalidated self-promotion; version-volatile and agent-locked; self-report is not evidence; kit names no vendor model in kit-owned text; plan-specific numbers rot in weeks |
| Append-only never-delete docs with `*_superseded` paths (thread 3 minority) | Directly contradicts one-fact-one-home and forward-only `status.md`; its transferable half (give history a home) is already `log.md`/`archive/` |
| Literal prompt incantations ("no ketchup mentioned at all") | Posters in the same thread report they decay; keep the doctrine, drop the phrasings |
| Comment-to-code ratio gate | Proxy metric for a semantic property — D-7 shape |
| VibeCurb verbatim; `brandkit-gen`/`imagegen-frontend`; its `index.js` | 348 KB dogma, IF-035 violations, internally contradictory, stale; image-gen prompt craft; the installer injects unindexed skills into a kit-owned dir |
| silk-design `assets/` and 23 templates | React/Tailwind/GSAP/Lenis runtime code forces a stack on every web adopter, five npm deps with no ledger row; mood-boards are outside a delivery kit |
| A rixels/"vector-shape texel" skill; the 98% figure; the "70–80% VT saving" figure; texture-*authoring* craft; a VT implementation guide | Patent-pending with no spec — a skill about a press release; borrowed numbers fail the "never report a green you didn't produce" bar; art craft is tool-locked; engine-specific and the wrong rung for nearly every adopter |
| A Refactoring-UI aesthetics skill; a composition/hierarchy skill | Largely unfalsifiable taste; Vercel and Anthropic's `frontend-design` already occupy the layer — point, don't restate |
| Sandi Metz numeric rules; Maintainability Index/Halstead; hard global complexity caps; inline suppression pragmas; deletion quotas; an LLM "slop detector" gate; ruff/radon/lizard as *shipped* checks; Grug as a source | Arbitrary and contradicted by measurement (~24-line median on 785k methods; this repo's longest function is 670 lines at cognitive 14); uncalibrated composites; Goodhart → classitis; suppression migration (4,000+ disables in reported cases); gameable; reviewers rate AI PRs *more* positively (MSR 2026) so a judgment gate is the thing that fails; every linter forces an adopter install; zero evidence, restated better elsewhere |
| A new compactness rule in CLAUDE.md/AGENTS.template.md | ETH + Anthropic + this repo's own capped-vs-watched data: prose is the weakest lever and both files are at cap. The existing "every line is a liability" bullet is already specific |
| Waiver expiry dates (`recorded waiver: … (expires <date>)`) | Genuinely useful but likely a direct conflict with §3 "no date stamp in a living registry cell" — flagged, not recommended |

---

## 5. Recommended plan folders

1. **`complexity-pushback/`** (from 05 P6) — four phases, each landing independently:
   **0 ruling** (one OI brief with three questions: does `check_complexity.py` *replace* the line
   ratchet; does it cover `tests/`; armed or report-only) → **1 sensor** (script + tests incl.
   the `elif`-flattening and `and`/`or`-run traps + seeded TSV; census in the log) → **2 arm it
   here** (retire whichever sensor was ruled; re-stamp) → **3 ship** (PROCESS_OPTIONS layer with
   applies-when ≈ "a repo past ~5k lines whose agents author most of the diff",
   `stack.ini.template` report step, `RESYNC_PACK.md` entry, `deep-module-design` skill, §3
   structure-commit bullet; **verify by bootstrapping a scaffold**).
2. **`ui-and-texture-packs/`** — backlog items 8, 9, 10, 12; two rulings (domains axis; Radix vs
   nine-roles: record both or pick one); resolve the Vercel licence; settle the attribution shape
   for mined pack prose (current pack says only `source: curated from a private research library`).
3. **`agent-brief-and-scope/`** — items 4, 5, 6, 7, 13, 14 as small byte-paid edits; the
   delta-vs-ask pass as a plan with a kill criterion; Q1 on surface maps.

---

## 6. Findings about the kit that fell out (not asked for; file separately)

- **B5 (03, unconfirmed by scaffold):** `bootstrap.py materialize_agent_layer` hardcodes
  `…/SKILL.md` while `gen_skills_index.py check_agent_sync` compares the whole `rglob` set — a
  multi-file skill would scaffold incomplete and red-gate until `--sync`. No test covers it. May be
  an intentional limit worth documenting in `skills/README.md`; confirm by bootstrapping a
  two-file skill before filing.
- **`EXTERNAL_SKILLS.md` `anthropics/skills` row is now wrong** to call that repo's skills purely
  "orthogonal task tools" — `frontend-design` is a design-quality skill.
- The antidote `docs/dependencies.md` row and SKILL.md header date the source commit 2026-08-22;
  GitHub says 2026-08-20 (the sha pins the content — not worth a WI).
- Shipped skills run 19–27 lines, not the 100–200 my briefs assumed; proposals are written to the
  real house shape.

## 7. Caveats on the evidence

- Reddit's JSON/HTML endpoints were blocked; only the Atom comment feed worked, so **report 02 has
  no comment scores** — entries were ranked by substance (37/7/62/58 captured).
- Report 01 read 4 of headcount's 143 SKILL.md files and none of iai's ~305 modules.
- Antidote's benchmark numbers are author-run on 4 cases × 2 runs; the *method* is the nugget.
- Rixels analysis rests on press coverage; no primary technical source exists.
- Everything in §2 was measured by one agent in one pass on one box; the ratchet baselines and
  growth figures are from HEAD and reproducible from git, the cognitive-complexity census is from a
  scratchpad `ast` walk that would be re-derived by the P1 script itself.
