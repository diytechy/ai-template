Amended the reviewed spine rows and added six drafted interface seams. No status changed.

| Row / cell | Before | After |
|---|---|---|
| SR-229 `requirement` | “delivered work-item admission…” | “delivered **guarded** work-item admission…” |
| SR-229 `acceptance_criteria` | No dispatcher exception. | Adds: “The unattended dispatcher’s own admission remains available without consulting this guard.” |
| LLR-301 `detail` | Claimed detached launch did not wait; said `exec_claude` dispatched guard operations. | States grace-period confirmation, restoration on every pre-confirmation failure, `exec_claude` invokes `claude`, and `main` dispatches guard operations. |
| TC-315 `verifies` | `["SR-229", "LLR-300"]` | Adds `IF-274`. |
| TC-315 `method` | “Drive recorded transcript fixtures…” | Distinguishes one Claude Code 2.1.289 recorded compaction fixture from synthetic version-stamped fixtures. |
| TC-315 `evidence` | Eight reader tests. | Adds the three recorded-compaction tests and unrounded-admission test. |
| TC-316 `verifies` | `["SR-229", "LLR-300"]` | Adds `IF-275`, `IF-276`. |
| TC-317 `verifies` | `["SR-229", "LLR-300"]` | Adds `IF-271`, `IF-272`, `IF-273`. |
| TC-317 `tier` | `"Smoke"` | `"Full"`; its evidence includes slow E2E tests. |
| TC-318 `verifies` | `["SR-230", "LLR-301"]` | Adds `IF-276`. |
| TC-318 `tier` | `"Smoke"` | `"Full"`; its platform-launcher evidence is slow. |
| TC-318 `evidence` | Existing relaunch tests. | Adds fenced-heading, prompt-write-failure, and non-zero-launcher restoration tests. |
| `id-watermark` | `IF = 270` | `IF = 276`, via `trace.py --bump-ids`. |

New interface rows, all cells new:

```toml
[interface.IF-271]
owner = "scripts/coordinator_guard"
requestors = ["scripts/integrate"]
channel = "call"
data = "claim_refusal(root, env=None) -> None | refusal text"
version = "v1"
status = "Drafted"
component = "CMP-008"
rationale = "The integrator must ask one guard-owned admission question, so every non-dispatcher route receives the same lease and drain decision."

[interface.IF-272]
owner = "scripts/session_keep"
requestors = ["scripts/coordinator_guard"]
channel = "call"
data = "primary_out_dir(root) -> Path"
version = "v1"
status = "Drafted"
component = "CMP-008"
rationale = "Coordinator and retained-session state must resolve the same primary checkout, or a lane worktree can split their runtime state."

[interface.IF-273]
owner = "scripts/session_keep"
requestors = ["scripts/coordinator_guard"]
channel = "call"
data = "dir_lock(directory, wait=10.0) -> context manager yielding Path; raises StoreBusy"
version = "v1"
status = "Drafted"
component = "CMP-008"
rationale = "One exclusive-file lock primitive keeps coordinator lease updates and other runtime-store updates from growing incompatible lock behavior."

[interface.IF-274]
owner = "scripts/coordinator_guard"
requestors = ["external:Claude Code"]
channel = "bytes"
data = "hook-event JSON on stdin: hook_event_name, session_id, transcript_path, agent_id?, reason?, trigger?"
version = "v1"
status = "Drafted"
component = "CMP-008"
rationale = "The guard can identify the lease holder and event only from the hook payload, so its accepted event vocabulary must have one declared surface."

[interface.IF-275]
owner = "scripts/coordinator_guard"
consumers = ["external:Claude Code"]
channel = "stdout"
data = "hook response JSON with hookSpecificOutput.hookEventName and optional additionalContext"
version = "v1"
status = "Drafted"
component = "CMP-008"
rationale = "The hook caller needs one response shape so a latch instruction reaches the coordinator without turning a hook response into a tool refusal."

[interface.IF-276]
owner = "scripts/coordinator_guard"
consumers = ["scripts/coordinator_guard"]
channel = "file"
data = "out/coordinator/: lease.json, events.jsonl, relaunch.json, consumed request and prompt files"
version = "v1"
status = "Drafted"
component = "CMP-008"
rationale = "Separate hook and admission invocations share durable coordinator state; one owner and file shape prevent a relaunch or latch record from being interpreted differently."
```

Builder header required in `coordinator_guard.py`:

```python
Contracts: IF-271, IF-274, IF-275, IF-276 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-271: claim_refusal(root, env=None) returns None when a guarded
    claim may proceed, else refusal text. The live dispatcher does not call it.

Contract IF-274: hook stdin is one JSON object carrying hook_event_name,
    session_id and transcript_path, with agent_id, reason and trigger where
    the event provides them.

Contract IF-275: a hook response is JSON containing hookSpecificOutput with
    hookEventName and, when the guard has context to add, additionalContext.

Contract IF-276: out/coordinator/ under the primary checkout holds lease.json,
    events.jsonl, relaunch.json, consumed-request files and prompt files. Lease
    and request records are whole-file atomic writes; the directory lock
    serializes their read-modify-write operations.
```

Builder header amendment in `session_keep.py`:

```python
Contracts: IF-247, IF-248, IF-272, IF-273 — the interface seams this module declares
(process.md §8; rows of record in docs/requirements/interfaces.toml).

Contract IF-272: primary_out_dir(root) returns the primary checkout's out/
    directory, derived from the git common directory or root when unavailable.

Contract IF-273: dir_lock(directory, wait=10.0) is an exclusive-file context
    manager yielding directory and raising StoreBusy after the bounded wait.
```

Checks:

- `check_trajectory.py --strict`: PASS — `clean (820 work item(s), 723 done (88%), 26 cancelled, graph acyclic).`
- `trace.py --strict`: expected exit 1 only for pre-existing LLR-292’s untestable “minimal”; new integrity result: `integrity=0`, `orphans=0`, `interfaces=227`.
- Evidence-symbol and TOML-list assertions: PASS.
- `git diff --check`: PASS.
- Required pytest command with `--basetemp .../wi-822-terra2`: started and reached 69 passing dots, but could not complete within the execution host’s 30-second child-process limit; lingering test-owned Python children were terminated afterward. No assertion failure was observed before termination.