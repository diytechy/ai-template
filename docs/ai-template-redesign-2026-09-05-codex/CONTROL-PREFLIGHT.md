# Control-launch preflight

The final candidate is the reviewed commit carrying this preparation on
`contract_split`, based on `a6b545849e0552de898b68e838b4eb6c1f8e5b33`.
Its exact completed hash and pause-deletion diff are recorded after the commit
exists. This record prepares the launch; it is not a control observation.

## Settled limits and remaining act

The [later owner ruling](CONTROL-DECISION.md#owner-ruling-2026-09-06) governs:
first eight completed WIs or two active days, at most twelve active coordinator
hours. US$100 is a watched bound over reported spend; missing spend is recorded
and does not stop admission. Sampling, consolidation, authority and provider
consent remain unchanged. The retained-adjudicator patch is outside the window.

`docs/work/pause` remains tracked and the runner has not launched. The remaining
owner act is its reviewed deletion against the selected frozen commit after
queue/route revalidation. General plan continuation supplied neither that exact
hash nor the review of that deletion. No additional permission is requested
merely because spend is unavailable.

## Actual route evidence

The enabled registry resolves eight entries across Anthropic, OpenAI and
OpenCode. `agent_route.py --list` and tier selections, including exclusion of
Anthropic, resolve without registry errors. The strong/medium/quick OpenAI
choices are Sol/Terra/Luna. Local version probes returned Claude 2.1.207,
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
records provider-reported cost where supplied but does not enforce US$100.
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
