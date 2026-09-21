# Technical research and action map

This is an intake map, not an adoption record. Community posts and articles are
leads, not evidence. An idea is incorporated only when it has a reviewed
decision and a concrete landing surface.

## Project action destinations

- Adjudication and requirements: spine-authoring and gate-advance.
- Planning and scoped execution: session-protocol, work items, and plans.
- Architecture and system design: LLRs, components, interfaces, and the derived
  architecture map.
- Delegation and ownership: agent routing, subagent_gate.py, and branch
  isolation.
- Verification and root-cause fixes: registry-hygiene, reviews, tests, and
  antidote.
- Continuity and skill lifecycle: status, log, handbacks, and shipped skills.

For prior outcomes, read the
[knowledge-pack review synthesis](plans/2026-08-29-knowledge-pack-review-synthesis.md)
and [project log](log.md). They record what was incorporated, mined, or left
out and why.

## Existing decisions and strong precedents

- [Fable 5 methodology](https://github.com/UnpaidAttention/fable5-methodology)
  — Candidate operating-method comparison; its broad method overlaps existing
  planning, architecture, verification, and eval machinery. Do not vendor it
  wholesale.
- [Stop subagent fanout](https://github.com/brefledev/stop-subagent-fanout)
  — Incorporated narrowly as the Claude-only unattended spawn gate.
- [TRIP workflow](https://github.com/PiLastDigit/TRIP-workflow) — Existing
  counterpart for plan/review/memory. Prior review found only its first-class
  research-task idea worth carrying forward.
- [One skill to rule them all](https://github.com/rebelytics/one-skill-to-rule-them-all)
  — External reference only; previously treated as tangential.
- [Antidote](https://github.com/Avtr99/antidote) — Incorporated and vendored for
  root-cause-over-patch review. Its skill-efficacy measurement idea remains
  research, not proof.
- [Headcount](https://github.com/cbrock84/headcount) — Screened. Its broad
  plugin payload was excluded; a write-surface ownership map is a deferred
  delegation candidate.
- [Rixels / Reforj](https://www.gamesindustry.biz/reforj-developer-4j-studios-unveils-rixels-modified-pixels-that-reduce-texture-memory-requirements-by-98)
  — Screened and excluded as a skill. Keep only as a texture-budget lead.

## Continuity, memory, and skill lifecycle

Use for handoff, project state, skill discovery, and turning recurring lessons
into durable instructions.

- [Private Claude session](https://claude.ai/code/session_017ebHPNpyMKahMrEVWu3on8) — Previous investigation; inspect before reopening its subject.
- [Private Claude session](https://claude.ai/code/session_01Rhfkybo7oVF8W7FL2h3stq) — Previous investigation; inspect before reopening its subject.
- [Private Claude session](https://claude.ai/code/session_01RSoLNrRSPbXSxt6iZXMQ3c) — Previous investigation; inspect before reopening its subject.
- [Private Claude session](https://claude.ai/code/session_01QL29wcD2vXgMpga1fMuuaS) — Previous investigation; inspect before reopening its subject.
- [Saipen](https://github.com/vacterro/saipen) — Candidate comparison for
  cold-agent handoff; compare with status/log/handback before adding state.
- [Engram skill](https://www.reddit.com/r/claudeskills/s/mlFK9KHShn) — Lead for durable learning capture.
- [Babysitting Claude](https://www.reddit.com/r/claudeskills/s/ChXxZS3ahR) — Lead for
  replacing repeated manual supervision with durable workflow and verification.
- [Data-file transformation skill](https://www.reddit.com/r/claudeskills/s/JSekLTtTXd) — Lead for repeatable task skills.
- [Magic Compact](https://www.reddit.com/r/ClaudeCode/s/R9YL7cJ7BM) — Lead for compaction and resume-state design.
- [Designer-originated skill](https://www.reddit.com/r/claudeskills/s/1vMVgOJVl6) — Lead for converting expert practice into a skill.
- [Plugin scaffolding](https://www.reddit.com/r/claudeskills/s/JE0W3gZgRO) — Candidate for skill/bootstrap ergonomics.
- [Skill navigator](https://www.reddit.com/r/claudeskills/s/vCkQ5iPJT0) — Lead for discovery and routing.
- [Budget skill stack](https://www.reddit.com/r/claudeskills/s/MGY45LY26t) — Lead for small, purpose-specific skill sets.
- [Session-close ritual](https://www.reddit.com/r/ClaudeAI/s/gCxQY699dp) — Lead for handoff/close checklists.
- [Knowledge-management system](https://www.reddit.com/r/claudeskills/s/GQR8p5601r) — Compare with git-readable source of truth; do not adopt an opaque store casually.
- [Skill discovery and vetting](https://www.reddit.com/r/claudeskills/s/wLyRU4JPNi) — Lead for external-skill intake.
- [Agent skill stack](https://www.reddit.com/r/claudeskills/s/br9e5q2nUC) — Lead for composable skill selection.
- [Website-to-CLI skill](https://www.reddit.com/r/claudeskills/s/Dtjxwznxj1) — Integration lead; assess security and egress before use.

## Planning, requirements, and architecture

Use for task framing, decomposition, architecture review, and durable decision
records. The likely landing surface is a small skill, plan, or existing-method
amendment—not another large instruction file.

- [Fable method](https://github.com/Sahir619/fable-method) — Candidate comparison for plan/act/prove and eval design.
- [Mise for Claude](https://github.com/emadd/mise) — Candidate for consent-first project initialization/recovery.
- [Claude Code output styles](https://code.claude.com/docs/en/output-styles) — Local presentation feature, not a project-method mechanism.
- [Fable availability article](https://www.xda-developers.com/claude-just-added-fable-5-back-to-your-subscription-but-theres-a-catch/) — Model context only; no stable policy.
- [CLAUDE.md structure article](https://www.xda-developers.com/your-claude-md-is-probably-wrong-how-anthropics-engineers-structure/) — Instruction-placement lead; test against byte caps and enforcement.
- [Claude Projects skills](https://www.xda-developers.com/gave-claude-projects-two-crucial-skills-now-they-finish-what-i-start/) — Planning/completion lead.
- [Fable skill reminder](https://www.reddit.com/r/ClaudeAI/s/Dojcz86dgq) — Lead for extracting repeatable method into skills.
- [Fable guidance](https://www.reddit.com/r/ClaudeAI/s/pnndJtm47K) — Operating-principle lead; require a mechanism before adding prose.
- [Fable CLAUDE.md migration](https://www.reddit.com/r/ClaudeAI/s/HFUM9LVWpS) — Migration lead, not a drop-in policy source.
- [Duplicate Fable migration link](https://www.reddit.com/r/ClaudeAI/s/WvZKkccbNx) — Same discussion retained from the original bookmarks.
- [Fable remediation](https://www.reddit.com/r/ClaudeAI/s/bzWKTSBpm1) — Lead for turning model-specific experience into durable method.
- [Deep-reasoning machine](https://www.reddit.com/r/ClaudeAI/s/YQVQf0dlru) — Planning/reasoning lead; validate on tasks, not claims.
- [Unresolved Claude discussion](https://www.reddit.com/r/ClaudeAI/s/7E4R1lhoXI) — Hold; title does not establish an objective.
- [Fable methodology announcement](https://www.reddit.com/r/claudeskills/comments/1uozmmd/i_had_fable_5_create_a_series_of_procedures/) — Supporting discussion for the Fable repository.
- [Fable prompt](https://www.reddit.com/r/claudeskills/s/xZMUWfY7nA) — Keep transferable decision rules, not literal incantations.
- [Fable method follow-up](https://www.reddit.com/r/ClaudeAI/s/QRpUEaOaB0) — Lead for method extraction/evaluation.
- [Requirements interrogation skill](https://www.reddit.com/r/claudeskills/s/LWz43I8iwj) — Candidate for requirements discovery; compare with spine-authoring.
- [Expectation versus reality](https://www.reddit.com/r/ClaudeAI/s/VL7mnKe8z0) — Claim-calibration lead; no direct method yet.
- [Prompt migration skill](https://www.reddit.com/r/claudeskills/s/5XKJ90ojRW) — Instruction-maintenance lead; avoid vendor-specific kit rules.
- [Architecture review skill](https://www.reddit.com/r/claudeskills/s/kTiGFoiGvU) — Candidate companion for architecture decisions; must point to requirements and evidence.
- [Engineering-process graph](https://www.reddit.com/r/claudeskills/s/9K1CjfF5Wm) — Strong lead for traceability/architecture visualization.
- [System design skill](https://www.reddit.com/r/ClaudeCode/s/bICp4hC49X) — Candidate for reasoning, separate from approval authority.
- [Claude Code complaint discussion](https://www.reddit.com/r/ClaudeCode/s/D09o8UHzWM) — Lead for evidence-backed defects over tool complaints.
- [Fable orchestration guidance](https://www.reddit.com/r/ClaudeCode/s/dWvuPhSLVt) — Plan/execute separation lead.
- [Stop asking AI for ideas](https://www.reddit.com/r/claudeskills/s/tbX4CnL1Rh) — Problem-framing and human-judgment lead.
- [Repository interface](https://www.reddit.com/r/ClaudeCode/s/Vij27TrKvJ) — Codebase exploration/architecture-map lead.
- [Skills and Wayfinder](https://www.reddit.com/r/ClaudeCode/s/W5le8F7yro) — Lead for evaluating architecture/discovery tools.
- [Rules in context](https://www.reddit.com/r/ClaudeCode/s/LrXHsLKJcu) — Favor targeted, enforceable instructions over static prompt bulk.
- [Stop adding every correction to docs](https://www.reddit.com/r/ClaudeAI/s/RqkfdGRMSu)
  — Strong lead for the existing receipt doctrine: context isolation and a
  redirect home outlast accumulating prohibitions.
- [Professional workflow](https://www.reddit.com/r/claudeskills/s/7dg01uJxyy) — End-to-end operating-practice lead.

## Delegation, orchestration, and ownership

Use for assignment, isolation, review independence, and completion signals.
The default remains bounded work items and verifiable artifacts, not autonomous
fan-out.

- [Subagent token waste](https://www.reddit.com/r/claudeskills/s/w91sGuXVER) — Bounded-delegation efficiency lead.
- [Claude as a company](https://www.reddit.com/r/AIDigitalServices/s/O81PDrfjgi) — Supporting lead only; require real responsibility boundaries.
- [Operator project](https://www.reddit.com/r/ClaudeAI/s/dduHy5R1ch) — Orchestrator/tool lead; inspect actual safety boundaries first.
- [Dopamine-loop agents](https://www.reddit.com/r/claudeskills/s/SSNt0KhQQN) — Low-confidence idea; no clear evidence-based fit.
- [Working-loop orchestrator](https://www.reddit.com/r/ClaudeAI/s/KQ7gs756II) — Compare its completion signal with work-item artifacts.
- [Multi-agent orchestration](https://www.reddit.com/r/ClaudeCode/s/KdM2aLLSIj) — Lead for role separation and review independence.
- [Senior-engineer loop](https://www.reddit.com/r/ClaudeAI/s/8hXvdnBraI) — Supervisor/reviewer topology lead.
- [Fable orchestration](https://www.reddit.com/r/ClaudeCode/s/jofVAo53R8) — Model-role allocation lead; do not vendor-lock policy.
- [Cost-reducing orchestration](https://www.reddit.com/r/vibecoding/s/OwGqDy8yS7) — Require reproducible quality and cost evidence.
- [Agent dispatcher](https://www.reddit.com/r/claudeskills/s/SpE66CMGo2) — Compare with existing agent-tier routing before adding a second dispatcher.

## Verification, review, and bounded autonomy

- [Recurring bug](https://www.reddit.com/r/ClaudeAI/s/jnyhQw0kIB) — Reproduction and regression-proof verification lead.
- [Over-agreement](https://www.reddit.com/r/claudeskills/s/sXbV1q48iU) — Adversarial review and explicit-dissent lead.
- [Autonomy control](https://www.reddit.com/r/ClaudeAI/s/bDkKKxm3Bt) — Consent, approval, and execution-boundary lead.

## Research inputs, model operations, and cost claims

These can inform a research plan or a local tool choice, but they do not justify
a kit rule. Verify time-sensitive token, benchmark, and subscription claims.

- [LLM token-saving claim](https://www.reddit.com/r/ClaudeAI/s/Zv6h0PgdSn) — Measure quality and cost on the same task.
- [Fable API pricing](https://www.reddit.com/r/Anthropic/s/km1l2jpKBI) — Vendor economics; no core-method impact.
- [Web-research cost reduction](https://www.reddit.com/r/ClaudeAI/s/Ev15FozQIY) — Research-efficiency lead; preserve source quality.
- [RDXMin](https://www.reddit.com/r/ClaudeAI/s/7VVUBB15Z7) — Token-saving claim; needs a reproducible comparison.
- [Plan quota](https://www.reddit.com/r/ClaudeAI/s/KF8TYYH3lG) — Subscription context only.
- [Deep-research efficiency](https://www.reddit.com/r/ClaudeAI/s/G3kTSSklaE) — Research-workflow lead, subject to source checks.
- [Unresolved Claude claim](https://www.reddit.com/r/ClaudeAI/s/oFJU7GpZrf) — Hold for manual review.
- [Opus product discussion](https://www.reddit.com/r/ClaudeAI/s/SrUFUxrrKI) — Vendor/product commentary.
- [Cloud computers](https://www.reddit.com/r/ClaudeAI/s/qbBXAFcqGV) — Platform capability, separate from process.
- [Claude translation plugin](https://www.reddit.com/r/ClaudeAI/s/s1AuZTTi3G) — Vendor utility, not portable method.
- [Email triage](https://www.reddit.com/r/ClaudeAI/s/9oRmScIkOz) — Product use case, out of scope.
- [AI-native development](https://www.reddit.com/r/ClaudeCode/s/u9MfW33FB1) — Research lead only; distinguish anecdotes from evidence.
- [Hidden token drains](https://www.reddit.com/r/ClaudeCode/s/jWdNX0J4kM) — Cost-diagnosis lead; never trade away verification.
- [Voice interface](https://www.reddit.com/r/ClaudeCode/s/Wjl2xxBfIm) — Product ergonomics, not a kit objective.
- [All code with Claude](https://www.reddit.com/r/ClaudeCode/s/13gHfXgfg7) — Anecdotal workflow; use only to form a testable question.
- [No-code-by-hand workflow](https://www.reddit.com/r/ClaudeCode/s/p7HY1RlkRf) — Anecdotal
  workflow report; use only to form a testable question.
- [Subagent usage window](https://www.reddit.com/r/ClaudeAI/s/lgRmd7bMrR) — Cost/capacity lead for delegation experiments.
- [Prompt cache](https://www.reddit.com/r/ClaudeCode/s/INnVEZBnQX) — Vendor performance detail, not durable policy.

## Domain-specific technical inspiration

These belong to optional product-domain knowledge packs or future domain skills,
not the core stack-agnostic process.

- [Steam Machine e-ink hardware](https://www.gamingonlinux.com/2026/07/valve-open-source-the-steam-machine-e-ink-screen-so-you-can-make-your-own/) — Hardware/embedded inspiration.
- [Claude-assisted CAD](https://www.makeuseof.com/stopped-using-cad-claude-design-3d-parts/) — CAD/3D workflow inspiration.
- [ESP32 projects](https://www.xda-developers.com/esp32-projects-that-punch-above-their-weight/) — Embedded/hardware inspiration.
- [AI 3D games](https://www.reddit.com/r/ClaudeAI/s/QcxywG5MFr) — Game/3D workflow lead.
- [Comma.ai](https://www.reddit.com/r/Comma_ai/s/zZ5pH7SXHd) — Autonomous-driving domain lead; no core action.
- [LLMs and robotics](https://www.reddit.com/r/robotics/comments/1uvcoey/robotics_researcher_argues_llms_may_be_the_wrong/) — Robotics architecture research question.
- [Claude vision skill](https://www.reddit.com/r/ClaudeAI/s/fYaAppfBdQ) — Computer-vision skill lead.
- [Hunyuan 3D](https://www.reddit.com/r/TopologyAI/s/OKRdxslOKi) — 3D-generation product lead.
- [Low-poly 3D](https://www.reddit.com/r/TopologyAI/s/hNGIMlm1eK) — 3D-generation product lead.
- [Frontend design](https://www.reddit.com/r/claudeskills/s/UORt8SeMqe) — UI-skill lead; existing accessibility rules remain the floor.
- [AI-coded site quality](https://www.reddit.com/r/ClaudeCode/s/oj1u9mzz3b) — UI/code-quality lead.
- [Image to 3D](https://www.reddit.com/r/TopologyAI/s/pq15FJ9k0l) — 3D-generation product lead.
- [Godot and Blender](https://www.reddit.com/r/TopologyAI/s/LsX7mLnKjv) — Game/3D pipeline lead.
- [UI prompts](https://www.reddit.com/r/ClaudeCode/s/k6yruEohjv) — UI exploration lead, not a substitute for accessibility checks.
- [JEV](https://www.reddit.com/r/LocalLLaMA/s/ddO4WZ1YNy) — Local-model technology lead; no process implication yet.
- [Qwen Image release](https://www.reddit.com/r/LocalLLaMA/s/G81DJsCwkb) — Image-domain product news only.
- [Unreal and Blender](https://www.reddit.com/r/TopologyAI/s/Qx0TFDZUNp) — Game/3D pipeline lead.

## Excluded or parked

- [Claude account switcher](https://github.com/realiti4/claude-swap) — Personal account/rate-limit utility, not project method.
- [ChatGPT student offer](https://chatgpt.com/students/2026/) — Product offer, not a technical source.
- [LetsFG MCP API](https://letsfg.co/developers/api/mcp) — Travel integration example, outside this project.
- [Windows optimization](https://www.xda-developers.com/windows-pc-has-built-in-optimization-tool-hidden-plain-sight-beats-every-paid-alternative/) — Local device maintenance, not a kit mechanism.
- [Screen-time report](https://www.reddit.com/r/technology/s/D4pgoS3iug) — General technology/social-policy topic.
- [Leaked backend code](https://www.reddit.com/r/vibecoding/s/2niUglStZk) — Do not ingest or rely on allegedly leaked material.
- [Human-like writing skill](https://www.reddit.com/r/claudeskills/s/1DQt5x5wZc) — Retained as a parked documentation-style lead.
