# Instruction-file length, rule count, and adherence

This pack preserves what published evidence (retrieved 2026-08-18) actually
supports about agent instruction files — CLAUDE.md / AGENTS.md / system
prompts — and what it does not. The repo's own doc budgets and caps remain
policy in `byte-budget-guard`; this pack records the evidence behind them.

## Findings retained

**The operative variable is rule count, not byte count.** Per-instruction
reliability barely degrades as instructions accumulate, but all-rules-satisfied
compliance collapses multiplicatively — well modelled as p^n. Verified against
ManyIFEval ([arXiv:2509.21051](https://arxiv.org/abs/2509.21051), EMNLP 2025):
Claude 3.5 Sonnet holds 93% per-instruction accuracy at 10 simultaneous
instructions yet satisfies all ten only 48% of the time; GPT-4o 85% → 21%.
Count-driven collapse is confirmed by ~6 independent labs (ManyIFEval, CFBench,
FollowBench/SIFo, Multi-IF, IFScale, MOSAIC). Reasoning-class models mitigate
substantially (o3-mini-high: 78% at n=10) but do not eliminate it.

**File length per se is weakly evidenced or contradicted.** The one direct
factorial study on Claude Code configuration files
([arXiv:2605.10039](https://arxiv.org/abs/2605.10039), 1,650 sessions) found an
*affirmative null* for file size (25–500 lines) and for a single planted
conflict (BF10 0.05–0.10 — evidence *for* no effect). Anthropic reports
removing >80% of Claude Code's system prompt with no measurable eval loss:
length is usually *waste*, not *harm*. Vendor "keep it short" guidance
(Anthropic's 200-line target, "bloated CLAUDE.md causes ignored instructions")
is published without any eval or citation; Anthropic's own engineering guidance
adds "minimal does not necessarily mean short." The only enforced vendor limit
is OpenAI Codex's 32 KiB combined AGENTS.md cap.

**Conflicting rules fail silently.** Models detect instruction conflicts well
(85–91% F1) but rarely surface them: GPT-4o resolved conflicts without
acknowledgment 97% of the time, with recency bias toward the later rule
(ConInstruct, [arXiv:2511.14342](https://arxiv.org/abs/2511.14342), AAAI 2026).
Conflict vs aligned instructions cost 22–78 points, and prompt engineering
alone did not fix it (IHEval,
[arXiv:2502.08745](https://arxiv.org/abs/2502.08745)). GPT-5-era vendor
guidance says contradictions burn reasoning tokens reconciling; so paraphrase
spread — the same rule restated in different words across files — is the
highest-risk bloat class, because drift between wordings becomes an invisible
conflict.

**Adherence decays over the session, robustly.** Multi-turn drop averages 39%
([arXiv:2505.06120](https://arxiv.org/abs/2505.06120)); SysBench
([arXiv:2408.10943](https://arxiv.org/abs/2408.10943)) measured full
system-prompt compliance falling from 84.8% (turn 1) to 33.7% (turn 5); the
config-file study's largest effect was per-step decay within one session
(OR ≈ 0.944/function), not any file-structure variable. Re-anchoring rules at
session and phase boundaries has better support than any static layout choice.

**Position effects exist but have no universal direction.** IFScale
([arXiv:2507.11538](https://arxiv.org/abs/2507.11538)) finds primacy bias
peaking at 150–200 instructions; MOSAIC (EACL 2026) finds primacy for some
model families and *recency* for Claude/Gemini; ConInstruct finds recency under
conflict. "Put it at the top" is not a portable rule. Vendors disagree too:
OpenAI's GPT-4.1 guide recommends instructions at both top *and* bottom of long
context; Anthropic/Google say query-last.

**Retrieval degradation is real but is a different failure.** Lost-in-the-
Middle, RULER, NoLiMa, and "context rot" measure *recall from* long context,
not *obedience to* it; NoLiMa shows effective lengths of 2–8K when lexical
shortcuts are removed. Relevant to finding a fact in a big doc; not evidence
that a long instruction file's rules get ignored.

## Application here

- Budget *rules in the always-loaded surface*, not repo doc volume. A 172 KB
  indexed reference doc loaded on demand is near-harmless; every extra
  always-on rule multiplies into the p^n joint-compliance loss.
- One rule, one wording, one home. Repetition at boundaries is defensible
  (re-anchoring evidence); five *wordings* of one rule is the silent-conflict
  seed. Converge wording before deleting placements.
- Prefer on-demand loading (skills, applies-when indexes, path-scoped rules)
  over always-on prose — the one pattern all vendors and the evidence agree on.
- Hard caps with a test restrain growth; "watched" baselines do not (this
  repo, 60 days: hard-capped file −14%; watched files +263% to +1,092%).
- Expect silent rule-dropping, not visible refusal: enforce mechanically
  (harness/tests/hooks) anything that must hold, per the enforcement audit.

## Failed or bounded approaches

- Trimming bytes while keeping rule count constant targets the wrong variable.
- "Important rules first" as a cross-model rule — direction is model-specific.
- Trusting one upfront load for a long session — compliance decays by turn 5.
- Citing vendor length targets as evidence — they are asserted, not measured;
  cite the peer-reviewed count/conflict results instead.
