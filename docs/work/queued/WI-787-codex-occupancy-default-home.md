+++
id = "WI-787"
title = "Read codex occupancy from codex's default home when the launch sets no CODEX_HOME"
workstream = "process"
specref = "project-trajectory/scripts/session_adapters.py"
sr_refs = ["SR-222", "SR-227"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by hand by the wave-9 coordinator on 2026-10-03, at the owner's direction:
"Agreed to an adapter fix, it should fall to default so every adopter is able to
inherit."

WI-541's closing measurement found that the kit's own codex route records no
occupancy. WI-688's judge session (`docs/iteration/wi-688-001-20261003-160206.log`)
left `context-used`, `context-window` and `context-pct` blank. Yet
`CodexAdapter.context` computes 114,766 / 258,400 = 44% from that session's rollout
as soon as it is given `CODEX_HOME`.

The blank is by rule. LLR-267 (Approved) says the codex occupancy is read "from the
rollout file named for exactly this thread id under the launch environment's
CODEX_HOME, and blank with no CODEX_HOME". LLR-290 (Approved) reads compaction and
per-request inputs the same way (`session_adapters.py` `CodexAdapter.context`,
`_codex_rollout`). No route in `docs/agents.toml` sets `CODEX_HOME`, so every kit codex
session on every adopter's machine records blank occupancy, and the retention reset
has nothing to read.

The original reason was to avoid reading another route's thread from an ambient home.
That is already prevented by the lookup itself, which is keyed by the exact thread id
(`rollout-*-<thread>.jsonl`). codex itself uses `~/.codex` when `CODEX_HOME` is unset.

Relation to OI-69 (e1), ruled 2026-08-30 ("dedicated config homes for the
orchestrator's CLIs"): a route that sets its own `CODEX_HOME` keeps it, unchanged. This
row covers only the unset case. Per-route homes, multiple accounts and new providers
are WI-788.

## Done-when

- With no `CODEX_HOME` in the launch environment, the codex adapter resolves the
  rollout under codex's own default home, the same location codex itself uses when
  the variable is unset. Occupancy, compaction and per-request inputs are then read
  as they are under an explicit home. An explicit `CODEX_HOME` still wins.
- Occupancy stays blank, rather than guessed, when no rollout for exactly that thread
  id exists under the resolved home.
- LLR-267's and LLR-290's `detail` say so. They are Approved, so the amendment is
  adjudicated in this lane (S11 direction) and re-attested in the lane's act.
- Tests:
  - a red-then-green test with `CODEX_HOME` unset and a fake home holding the thread's
    rollout, which yields the percent;
  - an explicit `CODEX_HOME` wins over the default;
  - a missing rollout stays blank.
  Set the default home through the test's environment, never the real `~/.codex`.
- A RESYNC_PACK entry says that adopters' codex sessions start recording occupancy,
  with nothing for them to configure.

## Deliverable
