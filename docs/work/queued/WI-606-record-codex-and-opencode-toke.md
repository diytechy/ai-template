+++
id = "WI-606"
title = "Record codex and opencode token usage losslessly: JSON output on both routes, raw usage kept verbatim (review pack C2)"
workstream = "unattended"
specref = "docs/plans/2026-09-24-owner-review-pack.md#part-c--defects-found-along-the-way"
buildtier = "medium"
priority = 3
safety_class = "ordinary"
+++

## Context

Found by the 2026-09-23 telemetry research; filed by the owner from the
review pack's Part C.

On a successful codex call `run_session` replaces the captured stream with
the `-o` text (`agent_session.py:536-538`, `:617-621`), so every usage field is
blank: 27 of 188 codex logs hold any token line, and none is from a successful
call under the current capture. The opencode route requests no structured
output.

The owner's S8 ruling (sister plan §3.2, 2026-09-24) adds `exec --json` to the
codex route (it works together with `-o`) and `run --format json` to the
opencode route, and puts the OTel GenAI field mapping in S7's record step, one
adapter per provider. So this row CAPTURES and does not map: the usage exists
from now on, and S7's adapter maps it once. Claude's two parse defects
(`reasoning-tokens`, `reported-model`) are defects of today's mapping, which
S7's adapter replaces; the S8 ruling assigns them there. NOT IN SCOPE: any new
field mapping, and the OTel schema.

ABSORBED from WI-611: `docs/agents.toml`'s OPENCODE notes record the
pathway as tested on 1.17.18 while 1.18.29 is installed. The recorded checks
are stdin prompt delivery, the global `--auto` flag, final-text-only stdout
and auth; the third changes with `run --format json`. Re-run the checks on
the changed route and the installed version; bumping the number alone would
claim a test nobody ran.

ABSORBED from WI-611: `docs/agents.toml`'s OPENCODE notes record the
pathway as tested on 1.17.18 while 1.18.29 is installed. The recorded checks
are stdin prompt delivery, the global `--auto` flag, final-text-only stdout
and auth; the third changes with `run --format json`. Re-run the checks on
the changed route and the installed version; bumping the number alone would
claim a test nobody ran.

## Done-when

- The codex route runs `exec --json` beside `-o`: a successful session's final
  text still comes from `-o`, and its raw usage events are kept verbatim in the
  session's raw record.
- The opencode route runs `run --format json`, and its raw usage events are
  kept verbatim the same way.
- Each route is pinned by a test over a recorded fixture of that CLI's output,
  showing the usage survives a successful call.
- Today's parsed columns are unchanged: no new field mapping is added.
- The opencode pathway checks are re-run on the installed version over the
  changed route, their output quoted in the log fragment, and
  `docs/agents.toml` records the version actually tested; a failing check
  disables the route or is filed, and the version is not bumped over it.
