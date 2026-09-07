# Control-launch preflight

The final candidate is the reviewed commit carrying this preparation on
`contract_split`, based on `a6b545849e0552de898b68e838b4eb6c1f8e5b33`.
Its exact completed hash and pause-deletion diff are recorded after the commit
exists. This record prepares the launch; it is not a control observation.

## Settled limits and remaining act

The [later owner ruling](CONTROL-DECISION.md#owner-ruling-2026-09-06) governs:
first eight completed WIs or two active days, at most twelve active coordinator
hours. US$1000 (raised from US$100, 2026-09-06 later sitting) is a watched bound over reported spend; missing spend is recorded
and does not stop admission. Sampling, consolidation, authority and provider
consent remain unchanged. The retained-adjudicator patch is outside the window.

`docs/work/pause` remains tracked and the runner has not launched. The owner
has since (2026-09-06, later sitting) instructed the next session to perform
the deletion commit and start the window; that commit is the frozen launch
commit and its hash is recorded here by the session that makes it. No
additional permission is requested merely because spend is unavailable.

## Actual route evidence

The enabled registry resolves eight entries across Anthropic, OpenAI and
OpenCode. **Re-lined 2026-09-06 (later sitting):** ANTHROPIC-FABLE (Fable 5.1
at medium effort) leads the strong tier; ANTHROPIC-OPUS-STRONG is catalog-only.
`agent_route.py --select --tier strong` returns ANTHROPIC-FABLE. WI-551 (the
adjudicator session-retention patch) is moved to `deferred/` for the window,
which the ruling's configuration row requires and the queue had not enforced. The Fable
route has not been live-probed from this sitting; the launch's step 1 and the
loop's pre-dispatch probe establish it. `agent_route.py --list` and tier selections, including exclusion of
Anthropic, resolve without registry errors. The strong/medium/quick OpenAI
choices are **Astra/Sol/Luna** since the owner re-lineup of 2026-09-06 (later
sitting; Terra is catalog-only, and Astra is not yet live-probed from a
sitting). Earlier in this record "Sol/Terra/Luna" names the line-up at the
time. Local version probes returned Claude 2.1.207,
Codex 0.153.4 and OpenCode 1.18.26.

**Provider requests did occur during preparation:** the
[Claude readiness probe](../reviews/2026-09-06-oi86-sn036-probe-structured-opus.md)
and subsequent Opus reviews/Inspection used the requested `claude-opus-5`
route. Initialization and result usage identify that model, and tracked
invocation logs retain the actual results. Those calls establish availability
of that review route on this account. Other control routes received registry,
selection and installation checks only; their authentication, credit, live
model availability and billing remain unverified until their normal pre-dispatch
probes. Sol, Terra and Luna collaboration sessions are not evidence of Codex
CLI authentication.

No inspected setting imposes an aggregate provider-dollar limit. The runner
records provider-reported cost where supplied but does not enforce the US$1000 watch.
That remains the ruled accounting limitation, not an admission gate. The dials
remain in `docs/process.toml`: Needs-held authority, final review always,
keep-nondependent false, clean-close sampling at its declared rate, and one
review round. No policy value changed.

## Current queue

The final preparation read of
`.venv/bin/python project-trajectory/scripts/schedule.py --root . ready --format json`
returned **18 ready WIs**. The new amendment adjudication and documentation
follow-up are ready; the new first-approval batch is held on the amendment.
Complete ready specs were read during preparation; eligibility is not a claim
or a decision to implement every older proposal. Revalidate this same queue and
route registry at the completed frozen hash before presenting the launch diff.
<!-- fig: cmd=".venv/bin/python project-trajectory/scripts/schedule.py --root . ready --format json" rev=a6b54584+oi86-sn036-final; out/run-logs/oi86-ready.json refreshed at frozen commit -->

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
