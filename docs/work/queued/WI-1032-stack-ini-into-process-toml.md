+++
id = "WI-1032"
title = "docs/stack.ini's settings move into docs/process.toml, and a repository still holding docs/stack.ini is refused by name"
workstream = "process"
sr_refs = ["SR-031", "SR-046", "SR-138"]
needs = ["WI-1031"]
specref = "docs/plans/2026-10-11-review-churn/README.md#10-one-configuration-file-in-toml"
buildtier = "strong"
safety_class = "ordinary"
priority = 4
+++

## Context

Filed on trunk on 2026-11-21 so the review-churn plan's phase 3 is not lost
(queue-drill hand-off §3.3 N2). This is item 10's step 4, ruled 2026-10-11:
one configuration file, in TOML, in `docs/process.toml`.

Today `docs/stack.ini` is 1,395 lines, about 98 of them settings, in 20
sections: `[paths]` `[product]` `[tiers]` `[smoke-budget]` `[ci-tiers]`
`[coverage]`, the `[step:*]` gates, `[dupes-census]` `[readability]`
`[arch-map]` `[generated]` `[agent-loop]` `[run]` `[check-suites]`.
`[smoke-budget]` runs from line 82 to line 1036, almost all of it a history
log of past budget stamps. One reader parses the file (`kitlib/config.py`'s
`read_stack_ini`, from WI-915), and 38 scripts reach it through that reader.
67 test files and 12 shipped kit docs name the file.

Settled here, so the lane does not re-argue them:

- **The TOML shape follows the plan's fit notes.** `[step:smoke]` becomes
  `[step.smoke]`, `smoke` plus `smoke.desc` becomes `[run.smoke]` with
  `command` and `desc`, `[generated]` path keys are quoted, Windows paths
  use literal strings, and packed lists become arrays. INI key case-folding
  goes, so each reader's key case, which WI-915 kept, is fixed in the schema.
- **`[agent-loop]` moves unchanged.** It lands as `[agent-loop]` in
  `process.toml`, and WI-1033 retires it into the routes. That keeps this
  row landable on its own.
- **The history log leaves configuration.** `[smoke-budget]`'s history
  moves verbatim into this lane's `docs/log.d/` fragment, under a heading
  naming where it came from. New stamps go to each lane's fragment.
- **No dual read.** Readers use only the new home. A repository that still
  holds `docs/stack.ini` is refused by name, pointing at the RESYNC entry.
  An unmigrated file is never silently ignored.
- **Adopters migrate by the RESYNC entry, applied by an LLM;** no new
  migrator is built (the ruling). The existing `bootstrap.py --migrate-config`
  may stay. Gilbert, Finance-Auditor and NotHomeWrecker carry small
  `stack.ini` files: paths, product, tiers, coverage, `arch-map` and a few
  `[step:*]` gates.

## Done-when

- [ ] Every `stack.ini` setting has a home in `process.toml` and in its
      template, declared in WI-1031's schema. Adopter-declared `[step.*]`
      and `[run.*]` tables are open tables with a fixed per-entry shape.
- [ ] `kitlib/config.py`'s reader reads the new tables. No script reads
      `stack.ini`, and none imports `configparser`. A characterization test,
      committed first, pins every reader's outcome before and after.
- [ ] A repository holding `docs/stack.ini` is refused by name, with the
      RESYNC entry's pointer.
- [ ] `[smoke-budget]`'s history is in this lane's log fragment, verbatim.
- [ ] `stack.ini.template` and `docs/stack.ini` are deleted. `bootstrap`
      scaffolds the new tables, and `test_dogfood_sync` checks them.
- [ ] `RESYNC_PACK.md` carries this row's own entry, saying what moves where.
      The shipped docs naming the file are updated (`ADOPTING.md`,
      `PROCESS.md`, `PROCESS_OPTIONS.md`, `GLOSSARY.md`, the READMEs,
      `KICKOFF_PROMPT.md`, `prompts/worker.template.md`, the
      `session-protocol` skill), and this repo's `CLAUDE.md` with its
      byte-budget delta reported.
