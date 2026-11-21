+++
id = "WI-1034"
title = "The spine rows and docs that name the folded configuration files say where each setting lives now"
workstream = "requirements"
sr_refs = ["SR-036", "SR-031"]
needs = ["WI-1032", "WI-1033"]
specref = "docs/plans/2026-10-11-review-churn/README.md#10-one-configuration-file-in-toml"
buildtier = "medium"
safety_class = "spine"
priority = 4
+++

## Context

Filed on trunk on 2026-11-21 so the review-churn plan's phase 3 is not lost
(queue-drill hand-off §3.3 N2). This is item 10's step 6. The plan bundled
it with item 5's spine rows and one RESYNC entry. The operator ruled on
2026-11-21 that re-sync need not be one entry, so this row stands apart
from variant F (WI-1021 to WI-1030) and carries its own.

Counted on trunk at filing (each row's text and cells, `-000` examples
excluded), these rows name `stack.ini`, `process.toml`, `agents.toml` or
`agents-enabled`:

| Tier | Rows | Accepted | By file |
|---|---|---|---|
| SR | 4 | 4 | `stack.ini` 3, `agents.toml` 1, `agents-enabled` 1 |
| LLR | 25 | 25 | `stack.ini` 16, `process.toml` 10, `agents.toml` 2, `agents-enabled` 1 |
| TC | 8 | 8 | `stack.ini` 6, `process.toml` 2 |
| IF | 9 | 0 | `stack.ini` 5, `process.toml` 2, `agents.toml` 1, `agents-enabled` 2 |

Recount at the build: WI-1032 and WI-1033 may amend some rows they must
touch to stay true.

Settled here:

- **LLR and TC rows may name `process.toml`,** a shipped boundary file
  (item 5's ruling). They are amended to the new home: the table and key,
  not a dead file name.
- **SR and IF rows name no file** (item 5's ruling). Their mentions are
  reworded to the setting's meaning. If variant F's text migration (F-8)
  lands first and removes some of them, this row takes what is left.
- **Accepted rows change text only.** Each drifts, and its act goes to an
  adjudication sitting (operator, 2026-11-21, hand-off §3.3 N4). This lane
  ends with the text committed and the owed acts listed. No status moves in
  it.
- The generated references (`docs/cli-reference.md`,
  `docs/interface-reference.md`) regenerate. Live docs outside
  `docs/archive/`, `docs/plans/` and dated hand-offs are updated where they
  give instructions. Historical records are left as written.

## Done-when

- [ ] Every counted row, recounted at the build, names the new home or no
      file, by the rules above. `trace.py --strict` stays clean.
- [ ] The live docs that give instructions name the new home (recounted at
      the build), and the generated references are regenerated.
- [ ] The owed acts are listed for the adjudication sitting.
- [ ] `RESYNC_PACK.md` carries this row's entry for an adopter's own rows
      and docs that name the folded files.
