+++
id = "WI-233"
title = "Dispatcher git() drops stderr - hook and porcelain failures park with blank error details (2026-07-18 field finding 4 - downstream gilbert)"
workstream = "unattended"
sr_refs = ["SR-156"]
needs = ["~WI-232"]
buildtier = "medium"
safety_class = "high-risk"
order = 230
+++

## Deliverable

agent_common.git() now appends git's stripped stderr to the returned text on a NONZERO exit (newline-joined when both streams are non-empty), so every detail=out[:200] park/quarantine reason built from a failed call carries the real cause - hook rejections and stderr-only fatals report on stderr, which the wrapper discarded. The success path is unchanged: stdout-stripped only, byte-identical, so all rev-parse/status/trailer parsers are untouched and no caller changed. Three regressions prove it: a pre-commit hook rejection surfaces its failing check, a stderr-only fatal (rev-parse --verify on a missing ref) returns non-empty text, and a successful commit with a stderr-warning hook returns stdout alone with no stderr bleed. No structured triple.
