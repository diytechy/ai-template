# Control-launch preflight (read-only)

Observed 2026-09-06 15:56 -05:00 at repository `HEAD`
`1e78ada3194c8806578cccf90a23afe2b64b9775`. The working tree had 65 tracked
changes and untracked preparation records, so this is a preflight snapshot,
not a frozen launch commit. No provider command, queue mutation, pause change,
or policy change was made for this record.

## Control and authority

`CONTROL-DECISION.md` records the owner's **Short control**: stop at eight
completed items or two active days, and at 12 active coordinator hours or
US$100 aggregate provider spend, whichever is first. Possible in-flight drain
cost belongs inside that US$100 cap. It requires the dependency-ready queue at
launch, frozen code from the repair commit, and unchanged sampling,
consolidation, authority, and provider-consent dials. It also says that a
route without reported spend or a defensible reservation must stop admission;
unknown is never zero.

The same ruling names the launch act precisely: the **owner's reviewed deletion
of `docs/work/pause` at or after the repair commit**, with the ruling unchanged.
That file is present at this snapshot and says deletion in a reviewed commit is
the way to resume. Therefore the control has not launched.

The current OI-85 ruling is complete (`status = "ruled"`), including the
SN-007/SN-026 re-attestation and SN-024 qualification. Its decision explicitly
says that the need-tier act does not cause a policy dial, queue state,
unattended launch, or SR/TC approval. The latest plan-execution authorization
does not substitute for the control's still-required owner-reviewed deletion.

## Routes, policy, and spend evidence

`docs/agents-enabled` is present. Its eight entries resolve without parser or
registry errors against `docs/agents.toml`'s nine rows: strong, medium, and
quick routes across Anthropic, OpenAI, and OpenCode. The enabled command
templates invoke `claude`, `codex exec`, or `opencode run`; they are capable of
incurring provider use. This read-only preflight did not test CLI installation,
authentication, account credit, provider spending limits, or provider billing
semantics, so each is unknown.

The declared operating dials are `human_approval_through = "DevStg-Needs"`,
`final_review = "always"`, `keep_nondependent = false`,
`complete_review = "sample"`, and `complete_sample_rate = 4` in
`docs/process.toml`; `docs/stack.ini` still maps the loop phases to `opus`.
No inspected policy dial sets a provider-dollar ceiling.

The router registry supplies identity, tier, command template, environment, and
failure notes, but no price, account-limit, reservation, or cap field.
`agent_loop.py` and `agent_session.py` only copy a provider-result
`total_cost_usd` into telemetry. The session accounting reader deliberately
leaves billing scope unknown and refuses to infer an aggregate. No inspected
reader aggregates cost across sessions, reserves drain cost before admission,
or blocks a new admission at US$100.

**Finding:** on repository evidence, US$100 including drain cannot be enforced
or defensibly reserved without an additional accounting arrangement. An
external provider/account limit could in principle supply that arrangement
without changing these route or policy files, but none is recorded or verified
here. It remains unknown, which the control ruling says must stop admission.

## Queue observation

Read-only command:

```sh
.venv/bin/python project-trajectory/scripts/schedule.py --root . ready --format json
```

At the observed revision it returned 15 `ready` queued entries: five exclusive
(one spine, four adjudication) and ten ordinary parallel entries. This is only
a census; it neither claims nor reprioritizes any work. Re-run it immediately
before any reviewed launch action because status, dependencies, and the
working-tree launch commit can change.

## Outstanding launch gate

The smallest immediate gate is route-complete, drain-inclusive evidence that
US$100 is reserved and that admission will stop before exceeding it. Until
that evidence exists, the Short-control ruling requires no admission. After
it, the remaining ordered conditions are: land and review the repair/frozen
launch commit named by `CONTROL-DECISION.md`, revalidate the queue and route
preflight at that commit, and have the owner review the deletion of
`docs/work/pause`. This record does not authorize or perform any of them.

## Sources inspected

- `docs/ai-template-redesign-2026-09-05-codex/CONTROL-DECISION.md` — Short
  control, spend rule, repair-commit precondition, and launch act.
- `docs/work/pause` — current pause remains present.
- `docs/agents-enabled` and `docs/agents.toml` — enabled routing and command
  templates; parser resolution performed with `agent_route` loaders.
- `docs/process.toml` and `docs/stack.ini` — current operating dials.
- `project-trajectory/scripts/agent_route.py`, `agent_loop.py`, and
  `agent_session.py` — route schema and telemetry-only cost handling.
- `docs/requirements/open-items.toml` (`OI-85`) — completed ruling and its
  explicit non-authorization of unattended launch.
