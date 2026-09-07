# Control-launch preflight

**Launch evidence, now historical:** the control was started and stopped on
correctness findings. [Results and the required repair](CONTROL-OBSERVATIONS.md)
govern continuation; the new tracked pause must not be deleted using the
original launch instruction below.
For the next repaired segment, use the
[September 7 handoff](../handoff-2026-09-07.md) and record a fresh preflight;
the CLI probes below remain historical availability evidence.

The launch preparation is based on reviewed `22285df4182dd2b69b4e658d77732afaf145c165`
on `contract_split`. The frozen pause-deletion launch commit is
`de9a2bfa7febe32ae16099cc09008f43a2240165` (hooks enabled). Runtime observations belong in the
[control observation record](CONTROL-OBSERVATIONS.md); preparation is not a
control observation.

## Settled limits and remaining act

The [later owner ruling](CONTROL-DECISION.md#owner-ruling-2026-09-06) governs:
first eight completed WIs or two active days, at most twelve active coordinator
hours. US$1000 (raised from US$100, 2026-09-06 later sitting) is a watched bound over reported spend; missing spend is recorded
and does not stop admission. Sampling, consolidation, authority and provider
consent remain unchanged. The retained-adjudicator patch is outside the window.

The owner authorized the pause-deletion commit and supervised launch, and
reaffirmed that instruction after the CLI update and successful Fable probe.
The deletion commit is the frozen launch baseline. No additional permission
is requested merely because spend is unavailable.

## Actual route evidence

The enabled registry resolves eight entries across Anthropic, OpenAI and
OpenCode. **Re-lined 2026-09-06 (later sitting):** ANTHROPIC-FABLE (Fable 5.1
at medium effort) leads the strong tier; ANTHROPIC-OPUS-STRONG is catalog-only.
`agent_route.py --select --tier strong` returns ANTHROPIC-FABLE. WI-551 (the
adjudicator session-retention patch) is moved to `deferred/` for the window,
which the ruling's configuration row requires and the queue had not enforced.
`agent_route.py --list` and tier selections, including exclusion of
Anthropic, resolve without registry errors. The strong/medium/quick OpenAI
choices are **Astra/Sol/Luna** since the owner re-lineup of 2026-09-06;
Terra is catalog-only. Claude Code was updated with owner authorization from
2.1.207 to 2.1.263 after the Fable request rejected the older executable
(minimum required: 2.1.251). Codex reported 0.153.4; the earlier OpenCode
version check reported 1.18.26.

**Live probes in this supervising conversation, before launch:**

- Astra: `printf 'Reply with the single word READY.' | codex exec -c model_reasoning_effort=medium --model gpt-6-astra --dangerously-bypass-approvals-and-sandbox`.
  Exit 0, `READY`; CLI header identified Astra and medium effort. Provider
  session `01a07963-4b42-7680-8fcc-8dfb9834c16f`. Cost not reported.
- Fable after updating: `printf 'Reply with the single word READY.' | CLAUDE_CODE_EFFORT_LEVEL=medium claude -p --model claude-fable-5-1 --output-format stream-json --verbose --dangerously-skip-permissions`.
  Exit 0, `READY`, `is_error=false`; initialization and response identified
  Fable 5.1 on Claude Code 2.1.263. Provider session
  `36967d6d-5fcb-460e-97d9-c6542e580d05`, result timestamp
  `2026-09-07T01:03:46.316Z`, raw `total_cost_usd=0.31372675`.
  The earlier incompatible-CLI request exited 1 with API status 400 and raw
  `total_cost_usd=0.000594`; that failure is not erased by the successful retry.

These are actual tool results from this conversation, not reconstructed
coordinator telemetry. They are preparation calls outside the window. Listing
routes is not a live probe: `select_with_probe` probes suspect routes during
recovery and skips fresh routes. Re-probe an unverified changed launch route
explicitly instead of relying on that recovery mechanism.

**Provider requests did occur during preparation:** the
[Claude readiness probe](../reviews/2026-09-06-oi86-sn036-probe-structured-opus.md)
and subsequent Opus reviews/Inspection used the requested `claude-opus-5`
route. Initialization and result usage identify that model, and tracked
invocation logs retain the actual results. Those calls establish availability
of that review route on this account. Apart from those Opus calls and the
Astra/Fable probes above, other control routes received registry, selection
and installation checks only; their live availability and billing remain
unverified. Collaboration sessions are not evidence of provider CLI authentication.

No inspected setting imposes an aggregate provider-dollar limit. The runner
records provider-reported cost where supplied but does not enforce the US$1000 watch.
That remains the ruled accounting limitation, not an admission gate. The dials
remain in `docs/process.toml`: Needs-held authority, final review always,
keep-nondependent false, clean-close sampling at its declared rate, and one
review round. No policy value changed.

## Current queue

The final preparation read of
`.venv/bin/python project-trajectory/scripts/schedule.py --root . ready --format json`
returned **17 ready WIs** at `22285df4`, after WI-551 was deferred. The new amendment adjudication and documentation
follow-up are ready; the new first-approval batch is held on the amendment.
Complete ready specs were read again by the supervisor. The returned ids are
WI-582, WI-605, WI-601, WI-602, WI-603, WI-604, WI-581, WI-570, WI-577,
WI-557, WI-596, WI-597, WI-536, WI-539, WI-556, WI-607 and WI-598.
Eligibility is not a claim or a decision to implement every older proposal.
The scheduler listing is not dispatch order: admission applies its existing
adjudication-first partition and batching. Revalidate the queue and route
registry at the completed frozen hash before starting.
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/schedule.py --root . ready --format json" rev=22285df4; out/run-logs/control-launch-ready.json -->

## Artifact approval remains separate

The queued amendment adjudication judges SR-161/LLR-183/TC-178 and the complete
snapshot absorption population before any copy. Its dependent first-approval
batch judges only SR-184–186 and TC-209–211, reading the amended chain and actual
Inspection evidence. Existing unrelated adjudications keep their own scopes.
The comment/rubric advisories are a separate ordinary documentation WI.

The live dial releases these tiers to an independent serial-trunk adjudicator.
The adjudicator must read the whole chain, current review/Inspection evidence
and every live/snapshot delta, then approve or return findings. A snapshot
copies its named registry whole: older cells may be absorbed only with an
explicit judgment and approval record for each. This applies to SR, LLR and TC
registries alike. The needs-only SN-036 act is no permission to refresh them.
No artifact approval or snapshot permission follows from queueing a spec or
from passing a document Inspection.
