## 2026-10-19 — WI-897: the coordinator guard's hook, per-call cost

### The no-op hook call, before the change

Taken on the lane at its trunk base (`9f934456f`), before any code edit,
on the 4-core / 8-thread workstation. The box was not quiet: about 15
`claude` processes, 6 `codex` processes and 8 `node` processes were
running, the processor load read 14 to 17 % across the run, and the
coordinator's bars had read 54 to 72 s against the 60 s smoke budget in the
hour before. So these figures are indicative; the after-figures are to be
read against them taken the same way.

The command was `coordinator_guard.py --root <scratch> hook`, run 20 times
per root with the lane's interpreter (`.venv`, Python 3.11), each fed a
PostToolUse payload for tool `Read` on stdin and timed by process wall
clock from a timing script outside the repository. Both scratch roots sit
outside every checkout, so `primary_out_dir` falls back to the root itself
and nothing was written in the repository. Every run exited 0 and printed
nothing.

| Root | Median | Minimum | Maximum |
|---|---|---|---|
| off: `context_guard_pct = 0`, `blackout = ""` | 213 ms | 207 ms | 283 ms |
| not the holder: `context_guard_pct = 50`, a lease naming another session | 242 ms | 235 ms | 320 ms |

`-X importtime` for `import coordinator_guard` (bytecode not written; three
runs): `coordinator_guard` cumulative 152.4, 148.6 and 135.7 ms, of which
`agent_common` cumulative 75.2, 73.1 and 67.8 ms, `argparse` 18.4, 19.7 and
16.9 ms, and `agent_policy` 9.7, 9.3 and 8.8 ms.

### The deferred imports

`coordinator_guard.py` now imports `agent_policy` at module level, and
`agent_common` and `agent_route` only inside `model_clis`, their one user,
which only a shell tool inside an open blackout window reaches. `argparse`
is imported by the parser, which the hook's own command lines (`hook`,
`--root R hook`) no longer build. `session_keep.py`, whose lock the hook
takes, reads the dials and the window from `agent_policy` and asks
`kitlib.git` for the primary checkout, so it no longer imports
`agent_common`. The new e2e pin, run on two no-op paths (guard off; guard
on with the caller not the holder), listed `agent_common`, `agent_route`
and `argparse` at the base and `agent_common` alone with only the guard's
imports moved (on both paths, since the guard imports `session_keep` at
module level), and lists nothing after.

`tests/test_import_layers.py`'s stamped window of deferred function-body
imports moves from 33 to 35: the two edges `coordinator_guard ->
agent_common` and `coordinator_guard -> agent_route` existed before at
module level and now sit in a function body, so no cycle or layer edge
grew.

### The no-op hook call, after the change

Taken by the coordinator after stage 2 (`8905a23c5`), with the same timing
script, roots and payload, and the trunk base (`9f934456f`, the primary
checkout) timed again in the same window for a same-load comparison. The
box was still not quiet (about 38 `claude`, `codex`, `node` and `python`
processes; the bars of the last hour read 62 to 76 s against the 60 s
budget), so the figures are indicative.

| Root | Base, same window | Lane, first run | Lane, second run |
|---|---|---|---|
| off | 217 ms (min 209) | 160 ms (min 152) | 159 ms (min 155) |
| not the holder | 242 ms (min 232) | 189 ms (min 180) | 187 ms (min 181) |

The no-op call is about 55 to 58 ms cheaper per process on both paths,
about a quarter of its cost, matching the base's before-figures (213 and
242 ms). With the matcher, a tool outside the four also skips the
PreToolUse call altogether, so a call to such a tool now pays one hook
process where it paid two.
