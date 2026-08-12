+++
id = "WI-432"
title = "OVERTURN WI-423 and fold the six check-enablement toggles into docs/process.toml as explicit keys with positive defaults (owner ruling 2026-08-11, repo-lock 8.5: `creating files to toggle something off is also very confusing ... far better to tie those into process.toml and key them all to on / true`). The six: docs/trajectory-check, docs/interfaces-check, docs/components-check, docs/subagent-gate, docs/live-status, docs/okf-export. NONE exists in this repo, which is exactly the confusion the owner names: absence IS today's declaration, and an absent file declares nothing a reader can see. Ship them as a `[checks]` section in process.toml.template AND docs/process.toml, each key visible with its CURRENT default stated honestly - the ruling is that the DECLARATION becomes explicit, never that a default flips inside a refactor. PRESERVE EVERY CURRENT BEHAVIOUR EXACTLY. Each of the readers (check_trajectory, subagent_gate, agent_loop, gen_okf, gen_trajectory-via-check_trajectory, bootstrap) must keep working, including the legacy one-word file as a MIGRATION-WINDOW FALLBACK for an adopter who already carries one - follow the precedent check_privacy.py sets for docs/privacy-check (TOML first, else the legacy file) and state the fallback's expiry. THE F5 COST IS REAL AND MUST BE DECLARED, NOT HIDDEN: the checkers that import nothing of the config layer each grow their own small tomllib read; measure the line cost rather than repeating the estimate, and pin the duplicated shape BEHAVIOURALLY in tests/test_rule_sync.py per D-7, which is the anti-drift tool of record now the duplication census is gone. process.toml.template's header currently states the OVERTURNED ruling as item 4 and docs/process.toml mirrors it as item 4; both must state the new one - a header describing a reversed decision is worse than no header. Update the README dial table, which currently prints these as `on (no file)` / `off (no file)`."
workstream = "scripts"
specref = ""
buildtier = "strong"
safety_class = "ordinary"
+++

## Deliverable

**DONE 2026-08-11.** The six check-enablement toggles are the `[checks]` section
of `docs/process.toml`, shipped VISIBLE in `process.toml.template` and mirrored
in this repo's own instance. Both headers now state the 2026-08-11 ruling; the
overturned WI-423 text is gone from both.

### The six keys, and what each one shipped as

| key | shipped | why that value |
|---|---|---|
| `trajectory_check` | `true` | was on when the file was absent |
| `interfaces_check` | `true` | was on when the file was absent |
| `components_check` | `true` | was on when the file was absent |
| `okf_export` | `true` | was on when the file was absent |
| `live_status` | `false` | **opt-in** — `agent_loop` read `read_declared(docs/live-status, "false")`, so absence read OFF |
| `subagent_gate` | `"off"` | **opt-in**, and a three-word enum (`off`/`ask`/`deny`), never a bool |

**The brief said five were on-by-default. Four are.** `live-status` is the
second opt-in dial, not a fifth on-by-default one — measured, not assumed:
`agent_loop.py` passes the literal default `"false"` to its reader, so an absent
file disables the live console line. Shipping it `true` would have changed what
every fresh scaffold's coordinator console does, under cover of a re-homing.

**How an opt-in dial stayed opt-in while still shipping visibly.** The ruling is
about the DECLARATION, not the default: "key them all to on / true" answers "how
does a reader see this dial", not "which gates are armed". So both opt-in dials
ship at their current value with a comment that says `OPT-IN, and shipped at its
current default`, and `test_bootstrap.test_scaffold_ships_every_policy_dial_in_one_home`
pins the exact six-key table — a `live_status = true` or `subagent_gate = "ask"`
now reds. `subagent_gate` also keeps its **string** vocabulary rather than being
bent to a bool: `ask` and `deny` are different restrictions, and collapsing them
would have been a second, unrequested decision.

### The F5 cost, measured rather than estimated

The prior estimate was "~15 lines in three stdlib checkers". **Three checkers is
right; the line count depends on what you count**, so all three numbers:

| module | local reader (total lines) | executable lines | whole-file diff |
|---|---|---|---|
| `check_trajectory.py` | 24 | 10 | +77 / −33 |
| `gen_okf.py` | 22 | 10 | +44 / −6 |
| `subagent_gate.py` | 36 | 7 | +58 / −10 |

<!-- fig: cmd="ast-count of each local reader between its def and the next def; git diff --numstat" rev=70ce891c -->

So the *reader* is 7–10 executable lines each (24/22/36 lines with its
docstring — `subagent_gate`'s is longest because it records a deliberate
divergence); the rest of each diff is the TOML-first arm on the public readers,
the message rewrites and the module docstrings. `agent_loop.py` grew **no** local
reader — `live-status` is the one of the six that routes through
`agent_common.declared_policy` — and **`bootstrap.py` grew none either**: it
converts and deletes the legacy files but never reads these keys, so the
"bootstrap may need its own" contingency did not arise.

**Where the copies are pinned.** `tests/test_rule_sync.py` gained six tests
driving all three copies against one table of file shapes (declared true/false,
undeclared, wrong section, empty value, unparseable, wrong-typed) and asserting
the value, not merely the sameness — the D-7 bar, since the census is gone.
**Red-proof:** drifting `gen_okf._process_check` to return `None` on an
unparseable file, and flipping the template's `subagent_gate` to `"ask"`, failed
3 of the 27 tests in the module; restoring both returned 27 passed.

**The one place the copies deliberately disagree, pinned as such:** an
unparseable `process.toml` reads **ON** in `check_trajectory`/`gen_okf` (a check
that quietly stops running is the failure worth avoiding) and **undeclared** in
`subagent_gate`, whose module contract is *fail OPEN with a paper trail* — an
unreadable file must not defer every spawn in an unattended run. A later reader
"harmonizing" the three now reds.

### Behaviour preserved, and the migration window

Every reader takes `docs/process.toml` first and falls back to its legacy
one-word file — the precedent `check_privacy.read_privacy_enabled` /
`read_secrets_scan` already set for `docs/privacy-check` and `docs/secrets-scan`.
Verified on this repo: all three trajectory dials, `okf_export` and the loop's
`live-status` read exactly what they read before, and `config_conflicts` is
empty.

**The fallback's expiry, stated once:** it is **SN-028's existing dual-read
window, not a second clock**. The six join `PROCESS_KEYS` (so the mixed-config
refusal covers them) and `bootstrap.LEGACY_CONFIG` (so `--migrate-config`
converts and DELETES them), and bootstrap runs that on every scaffold pass. An
adopter's window is therefore exactly **one re-sync long**, and it closes for
everyone when SN-028's does. Driven end to end on a fresh scaffold: planting
`docs/trajectory-check: off` + `docs/subagent-gate: ask` produced the two-line
mixed-config refusal, and `bootstrap.py --migrate-config --dest .` folded them to
`trajectory_check = false` / `subagent_gate = "ask"` and deleted both files.

### Everything that named the old home

The **remedy strings** mattered most and were rewritten first: `check_trajectory`
told an adopter to "set docs/components-check: off", which in a scaffolded repo
is now the mixed-config *refusal*. Also updated: the `gen_okf` banner stamped
into all 594 bundle files, the two `off (…)` short-circuit prints, the root
README dial table (four rows that read "on (no file)" / "off (no file)" became
six explicit `process.toml` rows), `PROCESS_OPTIONS.md` "Where the dials live"
plus its five layer notes, `ADOPTING.md` (three opt-out recipes + the re-sync
note, which now records the six as having come **in**), `project-trajectory/README.md`,
`agent-hooks/README.md`, the shipped `hooks/pre-commit` comment, and
`docs/declared-absences` — where the six moved from "absence is a legal state"
to RETIRED rows, which is what took `check_doc_refs` from 32 dangling to 27.

**Deliberately not touched:** spine registry row text (SR/LLR/TC/IF cells that
name the legacy paths) is fenced for this row; those rows describe the checkers
and are now imprecise about the dial's home. Filed as a finding, not fixed.

## Context

### The measurement the ruling rests on

The overturn's cost premise is that folding costs "~15-line `tomllib` reads in
three stdlib checkers, not five copies of a shell contract" — because the git
hooks' pure-sh parse (M-42) reads only `privacy_check` and `privacy_review`,
never these six. That premise is to be **re-measured here**, not inherited: the
number that goes in the Deliverable is the one this session counted.

### What "positive defaults" can and cannot mean

The owner's words are "key them all to on / true". Four of the six really are
on-by-default (`trajectory-check`, `interfaces-check`, `components-check`,
`okf-export` — absence reads on). Two are **opt-in**: `subagent-gate` (absent =
gate off; `ask`/`deny` arm it) and `live-status` (`agent_loop` reads
`read_declared(docs/live-status, "false")`, so absence reads off). Shipping
those two as `true` would flip behaviour for every fresh scaffold under cover of
a formatting change, which is the failure `test_scaffold_ships_every_policy_dial_in_one_home`
already names: "a default reversed inside a refactor is a prior ruling
overturned without its own review". So all six become **visible**; each carries
the default it has today.
