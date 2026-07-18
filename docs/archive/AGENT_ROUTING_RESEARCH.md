# Agent routing & heterogeneous review — research notes (S8 input)

**Provenance:** three research passes run 2026-07-10 (owner-directed) as input
to the proposed **S8** phase of
[`specs/working-surface-and-architecture-restructure.2026-07-11.md`](specs/working-surface-and-architecture-restructure.2026-07-11.md):
a read-only seam map of this repo's unattended layer, a literature pass on
review-quality scoring / model routing, and a July-2026 ecosystem survey.
Condensed here; an input document, not a working surface. Web claims carry
their sources; single-preprint or vendor-grade items are flagged.

## 1. The repo's seams (what exists vs. what S8 adds)

- **Model/tier knobs today** (all in `agent_loop.py`; launchers only export
  slots): `AGENT_MODEL` default; `AGENT_MODEL_MAP` phase→model
  (`session_model`); `AGENT_CMD` template with `{model}`/`{prompt}` tokens
  substituted per-token, never through a shell (`build_argv`);
  **`AGENT_CMD_MAP` phase→whole-command** (`session_template`) — per-phase
  cross-provider routing is already first-class, with preflight validating
  each command's executable before iteration 1. `docs/run-phase` keys are
  free-form; `docs/guardrails-policy` substring-matches model names to inject
  the vendored discipline core into weak-tier sessions.
- **Reviewer sessions:** no loop-native scheduler. `docs/review-policy`
  (`0|1|2`) is read and surfaced but deliberately never enforced ("the loop
  stays dumb"). The archived, **ratified** `AGENT_ROLES.md` pipeline defines
  `run-phase ∈ {PLAN, BUILD, REVIEW-A, REVIEW-B, INTEGRATE}`, reviewer ≠
  implementer (fresh context), dual reviewers splitting *charters* not
  coverage, integrator as single writer. Of its build-calls, `AGENT_CMD_MAP` /
  `review-policy` / the status-size guard landed; **`--prompt-map` and
  loop-side reviewer dispatch did not** — that is S8's scheduling half.
- **Scoreable review artifacts already exist:** the `log.md` verdict block
  (`Verdict: APPROVE|CHANGES-REQUESTED` + `- [BLOCKER|MAJOR|MINOR] id →
  issue → change → @owner` lines, `Model:` header for LLM-gate reviews) and
  the per-session iteration-log header (`phase/model/outcome/commits/tokens/
  cost-usd`), rolled into `docs/iteration_index.md`. Nothing scores them.
- **Doctrine S8 must preserve:** stdlib-only; one-word declared-policy files;
  never-breaking (absent knob = today's behavior); agent-neutral (git +
  `run-state` are ground truth, JSON parsing best-effort); **no silent model
  swap** (an unavailable agent is named, never repointed — the human consented
  to a specific tier); the **reviewer strong-model floor** ("never delegated
  down"); kit-owned files are take-wholesale on downstream re-sync, so
  project-specific values belong in declared files/registries.

## 2. Review-quality scoring & routing (literature)

**LLM-as-judge biases (established, multiply replicated):**
- Self-preference: judges recognize and over-score their own family's text
  (Panickssery et al., NeurIPS 2024,
  <https://proceedings.neurips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf>;
  perplexity mechanism: <https://arxiv.org/abs/2410.21819>). **A provider must
  never judge a contest it competes in.**
- Verbosity bias (length ≠ substance; survey
  <https://arxiv.org/pdf/2411.15594>) and position bias (order swaps shift
  pairwise verdicts 10–15pp, <https://arxiv.org/html/2406.07791v5>).
- Panels of small, family-disjoint judges beat one big judge, ~7× cheaper
  (PoLL, <https://arxiv.org/abs/2404.18796>).

**What correlates with real review value:**
- **Change-triggering is the canonical usefulness measure** — reviewers judge
  a comment useful iff it triggers a nearby change; specific, functional
  findings rank highest (Bosu/Greiler/Bird, MSR 2015,
  <https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/bosu2015useful.pdf>).
- Independent cross-reviewer overlap is a strong precision signal (GPT-4 vs
  human reviewer overlap study, <https://arxiv.org/pdf/2310.01783>).
- LLM critics' dominant failure is **confident false findings**, not misses
  (CriticGPT, <https://arxiv.org/abs/2407.00215>) — counting findings rewards
  the failure mode; rebuttal mechanics are needed.
- CRScore (NAACL 2025, <https://arxiv.org/abs/2409.19801>): ground review
  scoring in the *diff*, not the review's prose (design lesson; the tool
  itself is beyond stdlib).

**Separation & heterogeneity:**
- Role-label effect: relabeling a model's own claim as *external input* lifts
  correction rates 23–93pp (<https://arxiv.org/html/2606.05976>, verified
  abstract). Fresh-session review beats same-session self-review (F1 28.6% vs
  24.6%, p=0.008; single-author preprint,
  <https://arxiv.org/abs/2603.12123>).
- Family diversity: same-family consensus falls into a "popularity trap";
  two-model cross-family ensembles recover most of the diversity gain
  (<https://arxiv.org/abs/2510.21513>).
- **Multi-agent debate does not beat independent parallel review at equal
  compute** (ICLR'25 five-framework study,
  <https://d2jud02ci9yv69.cloudfront.net/2025-04-28-mad-159/blog/mad/>).

**Routing & escalation:**
- Learned routers (RouteLLM <https://arxiv.org/abs/2406.18665>) and cascades
  (FrugalGPT <https://arxiv.org/pdf/2305.05176>) are established, but assume
  training data / large sample counts. Key FrugalGPT insight: escalation pays
  only when the failure is *idiosyncratic* to the cheap model; **shared
  failures (hard/ambiguous spec) are where you page the human.**
- **No published precedent** for review-substance as the routing reward — the
  nearest anchors are bandit selection over feedback sources (LASeR,
  <https://arxiv.org/html/2410.01735>) and review quality as an RL training
  reward (CRScore++, <https://arxiv.org/abs/2506.00296>). S8's mechanism is a
  novel composition; at per-project sample sizes (tens of rounds) a fixed,
  legible win-stay/lose-shift policy beats any learned router.
- Reward hacking is benchmarked and worsens with chain length — observable
  metrics *will* be gamed; tripwires must be non-scored hard stops
  (<https://arxiv.org/html/2603.11337>, <https://arxiv.org/html/2605.02964v1>).
- Practitioner-converged ladder (not academically validated): 2 failures at
  cheap tier → 1 attempt strong → notify owner
  (e.g. <https://www.agentpatterns.ai/instructions/codified-effort-escalation-policy/>).

## 3. Ecosystem survey (July 2026)

**Headless CLIs — one-shot machine-readable invocation is now universal:**
`claude -p --output-format json` (+ `--bare` for hermetic runs, `--json-schema`;
<https://code.claude.com/docs/en/headless>); `codex exec --json
--output-schema --output-last-message <file>` (third-party providers via
`model_providers` config — Responses wire API only since Feb 2026;
<https://developers.openai.com/codex/noninteractive>); `gemini -p
--output-format json` (the only CLI with documented exit codes 0/1/42/53;
<https://geminicli.com/docs/cli/headless/>); also `copilot -p`, `qwen -p`,
`goose run`, `opencode run --model provider/model` (75+ providers via the
models.dev registry; <https://opencode.ai/docs/cli/>), `aider --message`
(LiteLLM-backed breadth, weak report channel). The kit's command-slot
architecture is the ecosystem-native pattern; only the **verdict convention**
differs per CLI — hence file-based verdicts, exit codes as diagnostics only.

**Routing layers route API calls, not agent sessions** — OpenRouter
(`openrouter/auto`), LiteLLM proxy, RouteLLM, Not Diamond (recommendation-only
router — the only shape matching the kit's "ask, then run the CLI yourself"),
Martian, Vercel AI Gateway. None routes sessions by problem type or reviewer
performance. **Static declarative routing in repo files has no incumbent to
defer to.**

**Model catalogs — point, don't vendor:** models.dev `api.json` (MIT,
schema-validated community TOML, production consumers — it *is* opencode's
registry; <https://models.dev> / <https://github.com/sst/models.dev>); LiteLLM
`model_prices_and_context_window.json` (auto-updated, fetched at runtime by
LiteLLM itself); OpenRouter `GET /api/v1/models`. Provider-native `/models`
endpoints are too thin (OpenAI's especially). **Tier aliases mostly dissolve
the catalog problem**: Claude Code resolves `sonnet|opus|haiku` (remappable
via `ANTHROPIC_DEFAULT_*_MODEL`), Gemini resolves aliases, Codex has a
vendor-maintained default — three alias cells per provider row rot at
CLI-flag pace, not model-release pace.

**Cross-provider review in the field:**
- OpenAI ships a Codex plugin *into Claude Code* for standard/adversarial
  review and handoff (<https://github.com/openai/codex-plugin-cc>; "official"
  framing is secondary-press-grade).
- 96-review field experiment (Todd Orr,
  <https://medium.com/@ribrewguy/what-i-found-when-claude-reviewed-codexs-work-5d83a348a2d9>,
  practitioner-grade): cross-vendor reviewers caught what the implementer's
  own family missed, both directions; **leaking the implementer's
  self-assessment to the reviewer collapsed finding rates 3–4×** — redact it,
  frame "assume the implementer was careful but missed something."
- LLM-Council-style tools independently converge on **anonymization** before
  peer ranking (<https://github.com/karpathy/llm-council>).
- Multi-CLI role orchestrators exist (kodo, ORCH — see
  <https://github.com/bradAGI/awesome-cli-coding-agents>) but all are heavier
  runtimes; none is repo-text-memory/stdlib-shaped.

## 4. The distilled recommendations (as adopted into S8)

1. Provider = "a shell command that produces a verdict": an `AGENT-###`
   registry row (`CmdTemplate` + three tier aliases), composed with the
   existing phase→tier map; defaults preserve today's behavior.
2. Reviewer scheduling = the ratified AGENT_ROLES dispatch (`REVIEW-A/B`
   phases) + `--prompt-map`, finally built; reviewer prompt gets diff +
   requirements, never the implementer's self-assessment.
3. Substance scoring is **mechanical** (confirmed-finding rate,
   cross-reviewer corroboration, anchored precision capped, actionability
   rate; severity hygiene + tripwires as gates, never scores; length never
   positive). LLM-judge, if ever, is a third-provider panel and only a
   tiebreaker.
4. Routing policy is **fixed and declared**: win-stay/lose-shift with a ≥2
   margin, provider swap after 2 consecutive failed gates, tier escalation
   only after the swap fails, human-page on shared-failure/contradiction/
   tripwires; scoreboard = one decayed-tally text file.
5. No vendored model catalog; documented pointers to models.dev/LiteLLM, a
   pinned `check_vendored`-style snapshot only if a consumer ever needs one.
