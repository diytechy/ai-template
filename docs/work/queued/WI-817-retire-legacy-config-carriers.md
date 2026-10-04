+++
id = "WI-817"
title = "Retire the SN-028 one-word config window and the non-TOML carriers"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-retire-legacy-config-and-carriers"
sr_refs = ["SR-137", "SR-139"]
needs = ["WI-798"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-retire-legacy-config-and-carriers (ch.1 §7,
§9.2; ch.2 §7; risks 7 and 9). It retires D1 (the one-word config window and its
copies, with `config_conflicts`), D2 (approval-dial spellings, keeping
`dial_from_config`), D3 (`gates =` and retired bar aliases), D4 (raw `[stack] test`),
D5 (`weak`/`quick`, `Provider`/`Family`, `--provider`) and D6 (CSV/markdown carriers
and `agents.csv`). `migrate_carrier.py` stays as the one-shot converter. **This
forces migration:** adopters still on one-word config or CSV/markdown carriers must
run the migrators at their next resync; the owner accepted that (README Q-1, "Yes
forced migration"). It needs WI-798 because both edit IF-045 and `agent_route`.

Knowledge packs (CMP-008), read before building: `docs/knowledge/agent-routing.md`,
`docs/knowledge/effort-tiering.md`, `docs/knowledge/prompt-image-token-efficiency.md`.

## Done-when

- The runtime reads only `process.toml`, `[product]`, `from-stage` and TOML
  carriers.
- The RESYNC entry runs `migrate_legacy_config` and `migrate_carrier.py`.
- A scaffold bootstrapped from an old-form fixture migrates and passes `check.py`.
- Each spine row the README matrix gives this row (SR-137 `requirement` and
  `acceptance_criteria`, SR-139 `acceptance_criteria`, LLR-155 `detail` and
  `code_symbol`, LLR-277 `detail`, IF-079 `data`, as listed in ch.1 §9.1) is amended
  and passes adjudication of that row, on whichever adjudication path is the one
  path when this row lands (it needs no sitting row; D-026).
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`,
  plus one scaffold bootstrap (the forced migration).
- Review bar: A+B (REVIEW-A plus an independent REVIEW-B).
- RESYNC_PACK: an entry anchored at a trunk commit that runs both migrators; it
  forces migration on un-migrated adopters (Q-1).
