## 2026-09-06 — Fable 5.1 at medium effort leads the strong Anthropic tier

**Decision (owner).** The strong Anthropic route is Fable 5.1 at medium
effort. `docs/agents.toml`'s ANTHROPIC-FABLE row now reads
`claude-fable-5-1`, version 5.1, `CLAUDE_CODE_EFFORT_LEVEL=medium`;
ANTHROPIC-OPUS-STRONG becomes catalog-only (its row stays for fallback).
`docs/agents-enabled` leads with ANTHROPIC-FABLE; the 2026-07-22 Opus stand-in
note is retired. Medium (Opus, effort medium) and quick (Sonnet) are unchanged,
as are the OpenAI and OpenCode cross-family rows.

Effect on the window: strong and medium builds now differ in model (Fable vs
Opus), so the window's rework-by-tier evidence can discriminate all three
tiers, not only quick. The stack.ini `[agent-loop]` model fallback is the
managed-routing-off path and is untouched.

Verification: `agent_route.py --list` resolves all eight entries;
`--select --tier strong` returns ANTHROPIC-FABLE. Routing, dual-plan routing
and dogfood-sync tests: 90 passed, 1 skipped. A live `claude -p --model
claude-fable-5-1` probe was blocked by this session's permission classifier
and is NOT claimed; the launch procedure's step 1 and the loop's pre-dispatch
probe establish reachability.
<!-- fig: cmd=".venv/bin/python -m pytest -q tests/test_agent_loop_routing.py tests/test_dogfood_sync.py tests/test_dual_plan_routing.py" rev=81ee8a52+fable-strong -->

Deferred open items: none.
