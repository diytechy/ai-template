# Appendix C — the external tool landscape against the kit's home-grown objectives

Produced 2026-09-05 by twelve research sub-agents from direct GitHub, PyPI,
npm and vendor page fetches. The parent agent that was to merge them hit the
session limit, so this appendix is distilled from each sub-report's own
headline and bottom-line sections. Star counts came from rendered pages (the
GitHub API was rate-limited) and are approximate; several sub-agents noted
that GitHub omits the year on current-year release dates and re-verified
against Atom feeds and PyPI. Everything unverified is marked as such.

**The one-paragraph answer.** For every objective, the survey found tools that
cover a slice and none that cover the shape: the kit's spine-with-approval,
its typed committed verdicts, its stage-derived bar and its heterogeneous
review protocol each have no substitute in the 2026 market, and nearly all
candidates fail at least one of the kit's constraints (stdlib-preferred shipped
checks, Windows + POSIX, git-native plain text, no LLM vendor lock). What the
survey did find is a short list of tools worth shelling out to, several
standards worth conforming to, and about a dozen design ideas worth stealing
without taking the code.


The kit's objectives, as posed to the survey:

- **A** requirement spine in TOML (SN→SR→LLR→TC + IF/CMP), tracer, approval
  state per cell, byte-exact approved baseline, derived stage ladder.
- **B** work-item registry (status = directory), scheduler, unattended
  coordinator over git-worktree lanes, LLM CLI sessions, heterogeneous-family
  review, gated merge station.
- **C** adjudication briefs and consolidation.
- **D** check harness over a declared stack file with ratchets.
- **E** owner surfaces: open-items briefs, dashboard, approval brief, status
  and log.

## C.1 Objective B, the lane and the merge station — worktree orchestrators

**Key finding: no tool ships git-worktree lane claiming plus merge-with-gate
as a reusable, importable library.** The ecosystem has converged on worktree
isolation almost universally but packages it as desktop apps, TUIs or
single-binary CLIs. The largest curated index
([awesome-agent-orchestrators](https://github.com/andyrewlee/awesome-agent-orchestrators),
about 200 tools) tags the overwhelming majority Desktop/Web/TUI/CLI.

| Tool | What it is | License | State (Sept 2026) | Covers | Does not cover | Fit |
|---|---|---|---|---|---|---|
| **Worktrunk** ([max-sixty/worktrunk](https://github.com/max-sixty/worktrunk)) | Rust CLI for worktree management "for parallel AI agent workflows"; `wt switch -x claude …` launches an agent; **`wt merge` = commit → squash → rebase onto target → blocking pre-merge hooks → ff-merge → cleanup**; hooks in `.config/wt.toml` | MIT or Apache-2.0 | ~6,800 stars; v0.76.0 on 2026-09-01; five releases in Aug 2026 | Lane claiming, agent launch, **the merge station** | Work items, scheduling, review | Vendor-neutral, **Windows supported** (Winget, installed as `git-wt`), no daemon, state is real git. CLI; crate has a lib target but no documented API. **The candidate to prototype against the station contract** — its default squash and rebase rewrite the history that carries the kit's review evidence, and a conflict leaves an open rebase; an adapter would use `--no-commit --no-rebase` (review round 1, finding 14). |
| Composio Agent Orchestrator ([ComposioHQ/agent-orchestrator](https://github.com/ComposioHQ/agent-orchestrator)) | Electron + Go desktop IDE with a local daemon; orchestrator plans, spawns workers each in a branch + worktree, watches CI/PR/review, auto-fixes CI and review comments | Apache-2.0 | ~11,000 stars; last commit 2026-09-05 | Lanes, 26 agent CLIs, a live kanban of working/blocked/review/mergeable, CI-gated merge | Dependency scheduling between tasks, a declarative gate language, plain-text git state, any library surface | Vendor-neutral, three OSes; forces a desktop app and daemon |
| emdash ([generalaction/emdash](https://github.com/generalaction/emdash)) | Electron "agentic development environment"; each agent in its own worktree + branch; review, PR, CI, merge in one place | Apache-2.0 | ~5,600 stars, very fast-moving | Lanes, nine provider CLIs, PR/CI review, merge | Gates you define, scheduler, library | Vendor-neutral, three OSes, SQLite state; GUI-forced |
| Claude Squad ([smtg-ai/claude-squad](https://github.com/smtg-ai/claude-squad)) | Go TUI multiplexing terminal agents, each in its own worktree and branch, with background auto-accept | **AGPL-3.0** | ~8,400 stars; v1.0.20 on 2026-08-20 | Lane claiming, multi-CLI sessions | Merge gate, registry, scheduler, review | tmux/POSIX TUI; AGPL matters for embedding |
| container-use ([dagger/container-use](https://github.com/dagger/container-use)) | MCP server + CLI: each agent gets a fresh container and its own git **branch** | Apache-2.0 | ~4,000 stars; last release v0.4.2 on 2025-08-19, commits continue; self-described experimental | Agent-neutral isolation via MCP, full command history, Windows since v0.4.0 | Worktrees, merge station, gates, registry | Needs a container runtime; release stagnation |
| Vibe Kanban ([BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban)) | Local web kanban; each task runs an agent in a worktree; diff review, PR, merge | Apache-2.0 | **~28,000 stars and sunsetting** — the company shut down (v0.1.42, 2026-04-10) | Lanes, ten agent CLIs, a board | Gated station, scheduler, review protocol | The highest star count in the field is the biggest trap |
| Crystal ([stravu/crystal](https://github.com/stravu/crystal)) | Electron app running Codex and Claude Code sessions in worktrees | MIT | ~3,100 stars; **EOL** — v0.3.5 (2026-02-26) says migrate to the commercial Nimbalyst | Lanes, sessions, GUI merge | Everything else | Dead upstream |
| uzi ([devflowinc/uzi](https://github.com/devflowinc/uzi)) | Go CLI spawning N agents in worktrees + tmux; `checkpoint` = commit + rebase | MIT | ~580 stars; last commit 2025-06-04 | Lanes, agent launch, primitive merge | Gates, registry, scheduler, Windows | Abandoned |
| orca ([orca-cli/orca](https://github.com/orca-cli/orca)) | On paper the closest to the whole stack: worktree per run, DAG scheduler, constraint gates before review, MCP server, Windows binaries | MIT | **1 star, 5 commits, last 2026-05-08** | — | — | An announcement, not a dependency |
| vnx-orchestration ([Vinix24/vnx-orchestration](https://github.com/Vinix24/vnx-orchestration)) | pip-installable Python driving `claude`/`codex`/`gemini`/`kimi`/`ollama` **as subprocesses, never importing a provider SDK**; per-worker worktrees; dual-LLM review gates; `vnx gate-check` deterministic pre-merge GO/HOLD | (not recorded) | 57 stars, single author | The closest philosophical match to the kit's own loop | Parallel multi-track, merge lock and file-scope derivation are "Tier 3 — designed, not built"; tmux + `gh` + POSIX bound | Worth reading, not adopting |
| orc ([spencermarx/orc](https://github.com/spencermarx/orc)) | "Markdown is the control plane, Beads are the only state": goals → beads → engineers in worktrees → automatic review → merge to goal branch; hooks per lifecycle phase | (not recorded) | 24 stars | Plain-text in-repo state, worktree lanes, review-before-merge | Windows; needs bash, tmux, `bd` | The design most like the kit's own; tiny |
| Sculptor ([imbue-ai/sculptor](https://github.com/imbue-ai/sculptor)) | Desktop app, parallel agents each in worktree + branch + terminal + diff | MIT | ~220 stars; last commit 2026-09-03 | Lanes | Gate, registry, scheduler; no Windows build | Python codebase but GUI |
| Conductor (conductor.build) | Mac desktop app running parallel Claude Code / Codex / Cursor / OpenCode agents in isolated workspaces with GUI merge | Proprietary | Commercial; Free / $50 Pro / $60 Teams | Lanes, sessions, GUI merge | Scripting, gate language, non-Mac | Not usable as a library |
| Cursor background agents | Cloud VMs cloning the repo, working on `agent/<slug>` branches, opening PRs; API-triggerable | Proprietary | Well adopted | Branch-per-task, API trigger | Local lanes, your gates, registry | Fails vendor neutrality and runs only in Cursor's cloud |
| Zed parallel agents | Editor feature (2026-04-22): threads isolated via git worktrees, external agents (Claude Code, Codex) | Zed's licence | Active | Worktree isolation, background threads | Merge gate, registry, scripting API | Editor-forced |
| Terragon | Cloud background-agent orchestrator | Apache-2.0 snapshot | **Shut down 2026-01-16** | — | — | Dead |
| Claude Code `isolation: worktree` | Subagent frontmatter runs the subagent in a temp worktree branched from the default branch ([docs](https://code.claude.com/docs/en/sub-agents)) | — | Shipped | Lane creation natively | Merge gate; Anthropic only | Covers half the lane primitive for one vendor |
| gwq ([d-kuro/gwq](https://github.com/d-kuro/gwq)), wtx ([aixolotls/wtx](https://github.com/aixolotls/wtx)) | Worktree managers; wtx keeps a **reusable pool of worktrees assigned to branches** — the closest thing to literal lane claiming named as such | Apache-2.0 / MIT | ~470 / 9 stars | Plumbing only | Merge, gates | — |

**Bottom line for objective B.** The only projects modelling the kit's full
stack (registry + gates + DAG scheduling + multi-model review) are single-author
and POSIX-bound (vnx-orchestration, orc), abandoned (orca, uzi), sunsetting
(Vibe Kanban) or GUI-forced (Composio, emdash, Conductor, Crystal, Sculptor).
The realistic choices are: **(a) shell out to Worktrunk** for worktree
lifecycle and the rebase → blocking-hook → ff-merge station — MIT/Apache,
Windows-capable, vendor-neutral, no daemon, state as real git — and keep the
registry, scheduler and review protocol in the kit's own Python; or **(b) build
the station yourself**, which is what the kit did. Note that (a) is a
`system`-tier dependency under `docs/dependencies.md` (a binary the adopter
installs), not a shipped-check dependency, and it would replace roughly the
`lane` + `integrate` refresh/merge half of the loop while the claim, the
verdict gate and the intake stay.

Not verified: Worktrunk's lib target as a stable public API; container-use as
an importable Go module; Conductor's worktree usage and API; Zed's Windows
support for parallel agents; the claim that the Composio repo moved
organisations.


## C.2 Objective A — the requirement spine and approval

| Tool | What it is | License | State | Would replace | Would not cover | Fit |
|---|---|---|---|---|---|---|
| **Doorstop** ([doorstop-dev](https://github.com/doorstop-dev/doorstop)) | One YAML (or Markdown + front-matter) file per item in git; documents form a parent/child tree; validates suspect links, unreviewed changes, cycles, orphans; publishes HTML with a trace matrix | **LGPL-3.0** | ~660 stars; v3.2 on 2026-07-10; commits to 2026-09-03; Python ≥3.10; 16 deps; Zephyr's safety WG used it and moved off | **Part of the approval mechanism**: each item has a SHA-256 fingerprint over UID, text, ref and links; `reviewed:` stores the fingerprint at last review; a link is (parent UID, parent fingerprint at review time) so a parent edit marks children **suspect**; `attributes: reviewed:` chooses which fields count as approved content | Per-cell approval, the three-rung Drafted/Approved/Founded ladder, the byte snapshot, the derived stage, attestation of who approved, the dashboard | Closest in philosophy; LGPL that adopters inherit; strict tree, not a DAG; two releases a year |
| **StrictDoc** | Richest feature set: traceability matrices, coverage views, requirement→source coverage, ReqIF interchange; optional server | Apache-2.0 | ~380 stars; 0.29.0 on 2026-08-30; still 0.x after six years | Registries + generator as a package | Per-cell approval, stage | **86 transitive packages** including pandas, numpy, fastapi, uvicorn, plotly, selenium and webdriver-manager |
| **Sphinx-Needs** | Typed need objects with IDs, links, `needtable`/`needflow` matrices, `needs.json` export; `sphinx-test-reports` ingests JUnit XML into linked needs | MIT | ~300 stars; 8.5.0 on 2026-09-03; 29 deps | A data layer under a smaller generator | Everything not in Sphinx; PlantUML pulls Java | Its **JSON-Schema validation** (local / network / network_back with 4-hop chain validation, declared in JSON) is the best design input for the registry schema layer, implementable against stdlib `json` |
| **OpenFastTrace** | Java tracer with the sharpest defect vocabulary in the field | GPL | Active | — | Needs a Java 17 runtime | Steal the vocabulary: **Orphaned / Outdated / Predated / Ambiguous / Unwanted / Duplicate**, shallow-vs-deep coverage, transitive defects |
| **trudag / Eclipse TSF** | The one project pushing on attestation and scoring of evidence; Eclipse-backed since 2025; dropped Doorstop as its backend | (not verified) | Early | — | — | Watch: a gap is opening that looks like the one the kit fills |

**Verdicts from the sub-report.** The label pattern across the field is
unenforced status (StrictDoc's STATUS "only affects the statistics screen";
OFT's draft/approved is filterable but unbound to content). Nothing records
*who* approved with any auditable binding. **No open-source requirements tool
derives a project maturity state from spine health — the eight-rung ladder is
unambiguously the kit's.** The defensible claim, in the sub-agent's words:
"Doorstop is the only open-source tool that binds approval to content via a
fingerprint and propagates invalidation to children. No tool stores the
approved bytes, tracks approval per field, offers more than a binary review
state, attests the approver, or derives a project stage from spine health."
If the stdlib-preferred constraint holds, the answer is keep `trace.py`. Two
cheap wins regardless: emit **ReqIF** as an export target (interop with
DOORS/Polarion for nothing architectural), and borrow Doorstop's
**fingerprint-on-the-link** idea, which is a cleaner statement of "this child
was approved against that parent text" than a separate snapshot diff.

## C.3 Objective B — the work-item registry, scheduler and loop

**Registries (plain text in git).**

| Tool | What it is | License | State | Verdict |
|---|---|---|---|---|
| **Beads** ([gastownhall/beads](https://github.com/gastownhall/beads)) | Agent-native issue tracker with `bd ready` dependency readiness; vendor-neutral setup for Claude Code, Codex, Cursor, Mux | MIT | Active | **Fails the plain-text constraint.** Its docs: "Beads issue data lives in Dolt… the local Dolt database is the source of truth"; `.beads/issues.jsonl` "is an export… not the canonical sync channel"; history lives under `refs/dolt/data`, so canonical changes are outside source-branch diffs unless the export is committed |
| **gastown** ([gastownhall/gastown](https://github.com/gastownhall/gastown), Yegge) | Multi-agent orchestration on Beads: Convoys, Molecules (TOML workflows), Hooks (worktree-persistent storage), **Refinery** (per-rig Bors-style bisecting merge queue with verification gates) | MIT | ~17.9k stars; v1.2.1 June 2026; Go | The closest full-system analogue and the Refinery is a direct competitor to the station. Inherits Dolt; requires a daemon fleet (`gt up`); Windows is "minimal CLI-only", real workflows need WSL. **Steal the bisecting merge queue idea** for when lane count grows |
| **wedow/ticket** | A single bash script; tickets are Markdown + YAML frontmatter in `.tickets/`; `ready`, `blocked`, `dep add/tree/cycle`, priority 0–4 | MIT | ~890 stars, young | The one close match to the kit's registry + scheduler design; bash + jq, so Windows means WSL; status is a field, not a directory |
| **ticket-rs** | Rust CLI, Markdown + YAML in `.tickets/`, deps DAG; PageRank, critical path, topological sort; `tk plan` batches work into parallel-executable stages; "every invocation reads, computes, writes, exits" | not verified | repo not located | The most sophisticated scheduler found; the plan-into-stages idea maps to lanes |
| **Backlog.md** ([MrLesk/Backlog.md](https://github.com/MrLesk/Backlog.md)) | Markdown tasks in `backlog/`, acceptance criteria, Definition-of-Done, dependency graph, cycle detection, kanban view; MCP | MIT | ~6.6k stars; v1.51.0 on 2026-09-02; macOS/Linux/Windows | Plain text, local-first, but a Node/Bun binary |
| hmans/beans | Markdown in `.beans/`, GraphQL query engine so agents fetch exactly what they need | Apache-2.0 | ~915 stars, "APIs may change significantly" | Token-efficient query is the idea worth noting |
| GitHub Issues + Projects | **Issue dependencies are GA** (`blocked_by`/`blocking`) with REST, webhooks and `gh` since 2026-06-10 | — | GA | A viable one-way **mirror** for human visibility; state leaves git, so never the source of truth |
| Ruled out | Taskwarrior 3 (SQLite), git-bug (git objects "not files", GPLv3, no release in 16 months), git-appraise (review store, dormant), claude-task-master (one JSON blob) | | | |

**Loops and orchestration.** Besides the worktree tools in §C.1:

| Tool | What it is | License | State | Verdict |
|---|---|---|---|---|
| **Bernstein** ([chernistry/bernstein](https://github.com/chernistry/bernstein)) | Python, `pipx install bernstein`: Goal → LLM planner → task graph → orchestrator → agents (one worktree each) → **Janitor** (tests pass, files exist, lint clean, types correct) → merge. **No LLM in the coordination loop**, deterministic replay; 40+ CLI agent adapters; file-based state in `.bernstein/` and `.sdd/` YAML; optional HMAC-chained audit log with Ed25519 receipts; PyPI classifiers list Windows | Apache-2.0 | ~1.1k stars; v3.19.1 on 2026-09-03; Python 3.12; solo-maintained beta | The one credible library-shaped replacement for worktree-claiming + janitor-gate + merge, leaving the kit the registry and the review protocol. Solo beta is the blocker; watch it |
| Claude Code native primitives | `claude --worktree <name>` (fresh worktree on a branch; four isolation checks; no merge); subagents in `.claude/agents/` with per-agent `model`, up to 20 concurrent, nesting to 3; hooks (`SessionStart`, `PermissionRequest` can deny, `PostToolUse`, `WorktreeCreate/Remove`, prompt- and agent-based hooks); Agent SDK (Python, self-hosted) | — | Shipped | Would delete the kit's worktree creation, simple spawning, permission gating and session persistence; the coordinator logic, multi-step gates and cross-vendor portability stay hand-built. Betting on the SDK is betting on one vendor |
| LangGraph, Temporal, Prefect/Dagster, OpenHands, SWE-agent, Aider | General agent/workflow frameworks | various | active | None reads a git diff, models approved text or mints work items; all add a runtime the adopter installs. Not candidates for the shipped kit |

**Review protocol.** The sub-agent's finding: "the multi-model adversarial
review protocol with scored win-stay/lose-shift escalation is, as far as I can
find, unique." The two GitHub projects doing cross-family review
([ng/adversarial-review](https://github.com/ng/adversarial-review), weighted
escalation across model families, ~13 stars;
[alecnielsen/adversarial-review](https://github.com/alecnielsen/adversarial-review),
Claude + Codex four-phase loop with a circuit breaker, ~39 stars) are tiny;
the one mature multi-LLM ensemble reviewer (CodeRabbit) is closed SaaS with no
escalation ladder. Research backing for cross-family review exists (arXiv
2604.19049, 2606.10315).

## C.4 Objective C — adjudication briefs, verdict records and consolidation

Three sub-surveys, one conclusion: **nothing in the market commits a typed
verdict to git.**

- **Multi-model deliberation tools** (PAL MCP Server, formerly zen, ~11.7k
  stars, last commit 2025-12-15; MassGen; ai-counsel; llm-council) return an
  ephemeral chat response or a log directory. The most telling detail: PAL's
  `consensus_confidence` field is a hardcoded string `"high"`, and the tool
  ends by instructing the calling agent to write the synthesis itself. The
  tools that do write a typed git record (adrkit, structured-madr) contain no
  deliberation; the one project spanning both (amiable-dev/llm-council) is a
  41-star beta.
- **LLM-as-judge and eval frameworks** (promptfoo — acquired by OpenAI
  2026-03-09; Inspect AI — binary `.eval` logs by default, "run artifacts, not
  version-controlled"; DeepEval, Ragas, Opik, Braintrust, W&B Weave) all start
  from a dataset of (input, output) rows and emit a run record. The kit's
  problem starts from a git state and mints a decision. Overlap is exactly one
  of the kit's five functions: reviewer-quality scoring, which about ten of
  these do well. OpenAI's hosted Evals platform shuts down (read-only
  2026-10-31).
- **PR review bots** (CodeRabbit, Qodo/PR-Agent, Cursor BugBot, Copilot code
  review, Ellipsis, Graphite, Semgrep Assistant) commit **input** config only
  (`.coderabbit.yaml`, `.pr_agent.toml`, `.cursor/BUGBOT.md`,
  `.github/copilot-instructions.md`); outputs are comments, inline suggestions
  and a check status; the accumulated "learnings" live on the vendor's servers
  and the only control is an irrevocable opt-out. Two permissively licensed
  harnesses could be made to emit a committed file under the kit's own
  detectors and validator: `anthropics/claude-code-action` (MIT) and PR-Agent
  CLI (MIT, `publish_output=false`).
- **Schema-validating the verdict record** is well served off the shelf;
  **detecting that a required verdict is missing** is not — conftest/OPA only
  evaluate files they are handed, so the open-conflict index must be computed
  first, which is the expensive 80% of the kit's code here. If anything is
  taken: `check-jsonschema` (Apache-2.0, pure Python, Windows-clean) for the
  verdict schema alone, as a ledger row; CUE (`cue vet`) is the strongest
  technical fit but a Go binary; conftest + Rego adds a second language.

Two conventions the market has validated and the kit should copy: **Copilot
reads review instructions from the PR head branch**, so a policy amendment and
the code it governs land in one reviewable commit; **BugBot resolves policy by
walking upward from each changed file**, giving path-scoped policy with no
central registry. And one line for the kit's own docs, because it is true and
unique: every one of these products' decisions is ephemeral and vendor-held;
the kit's verdicts are typed, committed, diffable and CI-gated.

## C.5 Objective D — the check harness, ratchets and floors

**Runners.** Nothing implements a monotone rung ladder ("run every step whose
`from-stage` ≤ current stage"). Tags (tox labels, Nox tags, lefthook tags,
just groups) are sets, not orders; per-step shell predicates (go-task `if:`,
lefthook `skip:`) work but re-type the comparison on every step. Nox is the
only runner where the ladder can live natively in config, because `noxfile.py`
is Python — which is roughly what `check.py` already is. **pre-commit does not
make adopters install nothing**: it needs five third-party packages plus a
Python, its zipapp still needs a system Python and does nothing for hook
environments, first runs need network, there is no offline mode, and its
`stages:` are git hook types, not project phases. pre-commit is the right
answer for adopters who already use it, and the wrong base for the kit.

**Metrics.** [lizard](https://github.com/terryyin/lizard) (MIT, ~2.5k stars,
1.24.0 on 2026-08-19, 1.29M PyPI downloads a month, 26 languages, token-scan
so no build system) emits one CSV row per function with NLOC, CCN, tokens and
parameters, has threshold exits and a whitelist, and would replace the kit's
complexity ratchet with a 50-line stdlib diff script — at the price of a pip
dependency on every adopter, which is the argument `check_complexity.py`'s
docstring already makes against it. radon (Python-only), scc/tokei (per-file
SLOC, Go/Rust binaries), jscpd (Node) and qlty (Fair Source) fill the other
slots the same way. The kit's cognitive-complexity measure is stdlib and
language-specific; lizard is the right optional step for a polyglot adopter.

**Secrets and links.** Gitleaks is feature-complete and in wind-down; its
creator lost admin control and shipped **Betterleaks** (MIT, March 2026); the
gitleaks CLI stays MIT but `gitleaks-action` needs a paid key for org repos.
Nosey Parker is archived. **lychee** (`--offline --include-fragments`)
validates local paths and Markdown heading anchors with no network and ships a
Windows binary — it covers the path half of `check_doc_refs` and all of
`check_docs`'s link check; it cannot check a bare `SR-042` in prose, which
none of the four traceability tools can either without owning the document
format. That id-in-prose check is the kit's.

**Meta-linters** (MegaLinter — AGPL, Docker + Node mandatory; super-linter;
trunk; qlty; reviewdog) orchestrate linters with no notion of a stage and
touch none of complexity ratchet, size ratchet, time budget, coverage floor,
id check or generated freshness. Disqualified on dependency cost.

**cleat** (`svetdev/cleat`, MIT, ~24 stars): the ratchet-only quality-gate
pack evaluated in `decisions-for-review-2026-09-05.md` §3. Its **escapes
ratchet** (suppression counts against a stamped baseline) is the one gate the
kit lacks.

## C.6 Objective E — owner surfaces, specs, skills and conventions

**Spec-driven frameworks.** GitHub **Spec-Kit** (MIT, ~133k stars, v1.0.4 on
2026-09-02, Python, bash + PowerShell + Python script variants, 30+ agents)
mints `FR-001`/`SC-001` ids but nothing downstream references them, its
coverage table is LLM keyword inference in a read-only chat message, and ids
are per-feature-file. Its checklists are the only soft approval gate in the
category (an LLM instruction to STOP, overridable), and its
`constitution.md` carries `Version`/`Ratified`/`Last Amended` (Spec-Kit's own field names, quoted <!-- check_vocab: allow -->). **Kiro** has
the strongest requirement→task link (`_Requirements: 1.1, 1.5_`) but no test
tier, no validation and no persisted approval; closed, per-seat, IDE-locked.
**OpenSpec** (MIT, ~67k stars, Node ≥20) is the only one with a durable
cumulative spec corpus and real deterministic tooling (`openspec validate
--strict`, exit non-zero) and rejects gates by design. **BMAD** (MIT, ~53k
stars, Node + uv) has checkpoints and no record. None traces requirements to
tests; the tools that do are the objective-A set. Spec-Kit's four-layer
template resolution means **the kit could ship as a Spec-Kit preset**
enforcing the spine format instead of rebuilding the authoring front-end.

**Agent Skills is now an open standard** ([agentskills.io](https://agentskills.io/),
Apache-2.0/CC-BY-4.0, ~25k stars; adopters include Claude Code, OpenAI Codex,
Gemini CLI, Cursor, Copilot, VS Code, Kiro, JetBrains, Goose, OpenHands).
`SKILL.md` frontmatter: `name` (≤64 chars, must match the directory),
`description` (≤1024), optional `license`, `compatibility`, `metadata`,
`allowed-tools`; a `skills-ref validate` reference validator ships. The kit's
skills are already nearly this shape; conforming costs almost nothing and
makes them portable unchanged. Distribution has consolidated on Vercel's
`skills` CLI and skills.sh; MCP's Skills Extension (SEP-2640) is in review and
excludes installable bundles — ship plain files in git.

**AGENTS.md** is substantially cross-vendor (Cursor, Copilot, Kiro, Devin/
Windsurf read it; ~60k projects claimed) with **Claude Code the holdout**:
Anthropic's docs say create a `CLAUDE.md` that imports it with `@AGENTS.md`,
and on Windows use the import because a symlink needs Administrator. That
validates the kit's thin-stub pattern on the platform it cares about. Gemini
CLI support is unresolved.

**Dashboard.** No off-the-shelf tool shows spine coverage, stage, work-item
flow and architecture together. Datasette is a server; Evidence.dev needs 641
npm packages; Observable Framework is near-dormant; Backstage needs Node,
Docker, 20 GB and no native Windows, and its scorecards are proprietary;
Quarto is the only tool producing a genuine single self-contained HTML file,
at 140–236 MB of bundled toolchain. Keep the generator; cut it to what the
ladder needs (PLAN §4.5).

**Open items.** **MADR** (MIT/CC0, v4.0.0) is the best format match —
`status: proposed | rejected | accepted | deprecated | superseded`, `date`,
`decision-makers`, `consulted`, Considered Options, Decision Outcome — and it
has **no field for a recommendation**; nothing in any ADR tool means "the
author proposes X; the decider has not ruled." That is the kit's invention.
Only pyadr models the lifecycle as commands (`accept`/`reject` rewrite status
and rename the file) and it is dormant since 2022. The genre mismatch is real:
ADRs are an immutable record, an open-items registry is a mutable queue.

**Approval brief.** The pattern exists (the release-PR pattern; rfcbot's
per-signer checkboxes, registered blocking concerns and named dispositions),
the tool does not — rfcbot's state is Postgres + GitHub comments. Steal the
three fields as plain text in `CURRENT.md`. GitHub CODEOWNERS + branch
protection genuinely enforces "these paths need the owner's signature" but
any one owner suffices and the record is GitHub's; Environments with required
reviewers need one of six and are not on free plans for private repos.

**The log.** towncrier, scriv, changie and changesets all represent "compiled"
by deleting the fragment (`--keep` re-emits everything), and towncrier/scriv
splice newest-first at a marker. reno re-derives from git history (stale since
2024). **blurb** (CPython's, zero deps, 2.1.0 on 2026-08-27) is the closest
shape: datetime-named fragments, `release` moves them into dated bundles,
`merge` recombines all bundles. Keep the compiler and adopt blurb's algorithm:
compiled-ness as directory location, not deletion.

**Forward-only status.** Nothing found. The transferable idea is TC39's
proposals README, which is forward-only by **filtering a generated table from
per-item state** so finished items drop out mechanically — the fix for the
kit's recorded "scrub every done-WI token" sharp edge.

## C.7 Ranked: the adoptions that would remove the most kit code while keeping the vision

1. **Worktrunk for the merge station** (§C.1) — replaces the refresh/merge
   half of `lane` + `integrate` (~1,500 SLOC); system-tier dependency.
2. **Conform the skills to the Agent Skills standard** — removes nothing but
   makes 15 process skills portable to every major vendor for near-zero cost.
3. **lychee for link and anchor checking**, optional step — retires
   `check_docs`'s link walk and the path tier of `check_doc_refs` for adopters
   who accept one binary; the id-in-prose tier stays.
4. **lizard as the polyglot complexity step**, optional — retires the
   Python-only measure for non-Python adopters; the stdlib measure stays the
   default.
5. **blurb's algorithm for the log compiler** — not the tool, the shape;
   ~200 lines replacing the fragment-deletion model and its link rebasing.

Ideas to steal without code: Doorstop's fingerprint-on-the-link; OFT's defect
vocabulary; sphinx-needs' declarative schema validation; gastown's bisecting
merge queue (only if lanes grow); Copilot's policy-from-head-branch and
BugBot's walk-upward policy; MADR's status vocabulary; rfcbot's per-signer
checkboxes and blocking concerns; TC39's filter-don't-scrub status; GitHub
Issues as a one-way mirror; ReqIF as an export.

## C.8 Where the kit's investment is justified — no substitute exists

1. **The spine with per-cell approval, the byte-exact baseline and the
   derived stage ladder.** Doorstop has a binary review fingerprint; nothing
   else binds approval to content, and nothing derives a project stage from
   spine health.
2. **Typed, committed, CI-gated verdicts and the adjudication briefs.** Every
   deliberation tool, judge framework and review bot returns an ephemeral
   answer or vendor-held state; the "recommendation awaiting a ruling" field
   exists nowhere.
3. **The heterogeneous-family review protocol with fixed escalation**, and the
   honest-harness doctrine (fail, never skip; stage-ordered steps). Two
   13- and 39-star projects gesture at the first; no runner implements the
   second.

## C.9 Not verified

Worktrunk's lib target; container-use as a Go module; Conductor's internals;
Zed's Windows support; ticket-rs's repo, license and stars; Bernstein's core
dependency list and Windows behaviour; Linear's MCP specifics; the Agentic AI
Foundation stewardship of AGENTS.md (claimed on the site, absent from the
repo); Gemini CLI's AGENTS.md support; whether Kiro persists approvals to
disk; Tessl's original spec framework after its pivot to skills governance;
blurb's configurability away from CPython's paths; Windows support statements
for reno, scriv, blurb, pyadr, Danger and every eval framework; CODEOWNERS
plan-tier availability; whether GitHub Environments record the approver's
identity; adoption figures self-reported by promptfoo and Opik. Several
sub-agents exhausted their web-search budgets and closed gaps with direct
fetches only.
