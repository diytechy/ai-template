+++
id = "WI-534"
title = "The arms the split surfaced: nine rows minted and stated — derive_stage's exit code, the two report media, docs/log.d/'s deletion arm, the gate's payload and log, schedule's CLI and listing, integrate's call surface — and gen_arch_map runs every target it is named (OI-67 follow-on)"
workstream = "architecture"
sr_refs = ["SR-159"]
needs = ["WI-533"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

The nine arms the split surfaced are rows, each stated beside its owner, and
`gen_arch_map` runs every target it is named. Record:
[../../../log.d/2026-08-29-wi534-if-arms.md](../../../log.md#2026-08-29--wi-534-the-arms-the-split-surfaced--nine-rows-minted-and-stated-oi-67-follow-on).

`IF-165` `derive_stage`'s exit code (three measured consumers: `check`,
`trunk_step`, `kitlib/stage`); `IF-166` `docs/test/report.html` (`trace
--html`); `IF-167` `docs/test/perf-report.md` (`check_perf`); `IF-168`
`docs/log.d/`'s write-and-delete arm (`trunk_step` and the adopter's session);
`IF-169` the PreToolUse verdict payload on stdout and `IF-170` the decision log
under `out/` (`subagent_gate`; `IF-020` keeps the exit code); `IF-171`
`schedule.py`'s own argv and `IF-172` what it prints (no exit-code row — the
answer is the listing); `IF-173` `integrate`'s in-process call surface
(`dispatch`, `handback`, `lane` — the reverse of `IF-055`). 154 → 163 rows; the
reference reads 74 / 163 / 163; nine reasoned allowlist entries; `IF-156` and
`IF-020` each lost the clause a new row took. Riding with it: `gen_arch_map.main`
runs every named mode and exits with the worst code (one invocation naming both
references reported a green over a stale one); `schedule simulate --jobs` below
1 is refused with 2 and the module's Usage puts `--root` before the subcommand;
the gate's prose says a defer never logs; this repo's `.gitignore` ignores the
perf artifacts the shipped template ignores, the template ignores
`out/subagent-gate.log`, and `docs/test/perf-report.md` is a declared absence.
