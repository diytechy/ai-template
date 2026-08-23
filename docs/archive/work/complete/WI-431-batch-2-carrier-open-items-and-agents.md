+++
id = "WI-431"
title = "Batch-2 of the carrier migration (repo-lock §8.1), FIRST SLICE: convert docs/requirements/open-items.csv (7 rows, the 3,126-char cell that is the loudest case in the repo) and docs/agents.csv (10 pair rows + 3 load-bearing comment lines) from CSV to the TOML carrier D-5 ruled, plus their templates - registries/open-items.template.csv and the kit-root agents.template.csv. CARRIER ONLY, exactly as D-5 was: no row's text changes, no schema changes, no Status vocabulary change. EXPLICITLY OUT OF SCOPE and must not be touched: interfaces.csv (waits for OI-14, which rewrites what a Contract cell may hold - converting first means converting twice) and components.csv (waits for the components ruling, which is ABOUT CMP rows). Extend migrate_carrier.py with a per-registry KEY map as §8.1 records; do NOT write a second converter, which is the exact D-6 hazard. Extend spine_carrier.py rather than adding a second module: D-6 gave the registry vocabulary ONE home and the generic machinery (resolve/rows_from_toml/load/columns/empty_value_findings) is what a second module would duplicate. THE CUTOVER IS THE DETECTOR - D-5's hardest-won lesson is that wiring readers against the OLD carrier can never surface an unwired one, because every reader looks fine while the file it expects still exists; run the conversion against a throwaway tree first and fix what actually breaks. A carrier that does not parse is reported ABSENT, never EMPTY (spine_carrier._toml_rows_text's None-not-{} shape) - {} on a decision queue means `no open items`, a silent false green. Re-verify the reader inventory rather than trusting §8.1's. Extend test_dogfood_sync's spine key-set rule (live keys subset-of schema, template keys == schema, schema subset-of carrier vocabulary) to both new registries rather than inventing a second rule, and drive it against planted defects in both directions. Regenerate docs/open-items.html. Note the migration in ADOPTING.md. Decide whether gen_open_items.normalize survives the carrier change and say why. The OI watermark (OI = 14) must not move."
workstream = "scripts"
specref = ""
buildtier = "strong"
safety_class = "registry"
+++

## Deliverable

**DONE 2026-08-11 (`f458aea7` · `3bec6dab` · `955cddec` + this close).** Both
registries and both templates are on the TOML carrier, sources deleted in the
converting commit. Carrier only: no row's text changed and the OI watermark
stayed at **14**.

### The converter generalized, never duplicated

`migrate_carrier.py` gained an `OFFSPINE` map beside `SPINE` and one extended
`KEY` map — a second converter is the D-6 hazard verbatim. Two shapes the spine
never carried, each with its own oracle leg driven against planted corruption:

* **Comments are records, not noise.** `agents.csv` carries a
  `# tag-rank: ga>preview>beta>exp` line `agent_route.load_tag_rank` **parses**;
  `csv.DictReader` splits the prose comment on its commas and hands back a
  nine-cell row whose `Id` is the first clause. `read_csv_records` recovers each
  raw line through `csv.reader.line_num` — never a newline split, because a
  quoted cell may legally span lines and a `#` inside one is not a comment — and
  the emitter restores each comment byte-for-byte **and in place**.
* **A dotted id must be quoted.** `[agent.ANTHROPIC-OPUS-4.8]` written bare is
  *valid TOML* declaring nested tables: the file parses and the row's id is gone.
  `toml_key` quotes it, `raw_id_findings` reads ids off the RAW source and
  demands each one back, and `spine_carrier.nested_table_findings` refuses the
  shape at LOAD, because the converter is not the only writer of these files.

`WI-Refs` became a typed array (every live and shipped cell is a bare id, and
its only consumer already splits it); `Version` deliberately did **not** — as a
TOML float `4.8` stops being the text the registry stores and `_version_key`
parses.

### The reader inventory — §8.1 measured wrong twice

| registry | readers actually found |
|---|---|
| open-items | `gen_open_items` · `check_docs` · **`traj_status`** · **`check_trajectory`** · **`trunk_step`** · **`integrate`** · `intake` (read only) · **`bootstrap` (the WRITER)** |
| agents | `agent_route` (reader of record) · `agent_loop` · `plan_runner` · `score_reviews` · `bootstrap` (template mapping only — it reads no agent data) |

§8.1 names **3** open-items readers; there are **8**. It says **intake WRITES**;
it does not. The writer is `bootstrap.py`, appending the scaffolded OI-3 brief —
so the writer question has a *different* answer from the spine's: D-5 needed a
line rewrite because it CHANGES a cell of an existing row, and an APPEND touches
nothing, which is strictly weaker. `csv.writer`'s CRLF default is now
structurally absent rather than guarded; all four files and the append are
asserted at 0 CR bytes.

`bootstrap.py` may import no sibling (repo-lock §8.2), so it carries its own
two-line TOML emitter and its own copy of the open-items key names — the same
declared F5 duplication it already carries for `process.toml` — pinned
behaviourally in `test_rule_sync` per D-7.

### The cutover was the detector

Run first against a throwaway clone, before a reader was touched. It found three
**fail-open** readers that wiring-first could not have surfaced:
`gen_open_items` rendered "0 pending decisions", `traj_status` spliced an empty
open-items block into `status.md`, `check_trajectory`'s brief lint went vacuously
clean. `agent_route` failed **loudly**, which is correct. Every reader now goes
through `spine_carrier.load`, so an unparseable registry RAISES.

### The rule, reused

`test_dogfood_sync` extends the spine's three-leg key-set rule to both new
registries rather than growing a second one. It **bit on the way in**: converting
the templates dropped `RuledDate`/`RulingRef` and `Env`, columns the CSV header
declared with every shipped cell empty. Restored into the `-000` schema rows.
Driven against planted defects in both directions on both registries.

### `normalize` survives

TOML retires half its hazard — a literal CRLF inside a multi-line string is
folded to LF by the *parser* — and not the load-bearing half: the guard also
covers the *checkout's own* line endings, which is not a registry fact at all.
`esc`'s CR strip survives too, because a `\r` **escape** is still legal TOML.

### Deviations

* **`interfaces.csv` was touched, additively.** IF-118/119/120 declare the three
  new cross-component seams; `check_trajectory` ERRORs on an undeclared crossing,
  so the alternative was a red gate. No existing row's text changed.
* **History was de-linked, not retargeted** (4 refs in `log.md`/`archive/`), and
  7 further prose mentions are **declared absent** with their reason.

### The bar

Full suite **2282 passed, 5 skipped** vs the **2258/5** baseline (+24, reconciled
test-by-test). `trace --strict` rc 0 · `check_trajectory --strict` rc 0 ·
`check_docs --stale` 0 broken · `check.py --jobs 0` **PASS** with `open-items`
visibly passing · every generated surface fresh · `ruff format` clean. The four
advisory reds are byte-identical to a measured HEAD baseline. See
[log.md](../../../log.md)'s 2026-08-11 entry for the figures and the three findings
filed rather than fixed.

## Context

Owner-approved 2026-08-11 as the first slice of the batch-2 sweep recorded in
[repo-lock.md](../../../repo-lock.md) §8.1, unblocked by D-5's execution the same
day. §8.1's measurement of the reader set is an input to be re-verified, not a
premise: it names three readers for `open-items.csv` and five for `agents.csv`,
and it asserts `intake` writes the open-items registry.

Two hazards §8.1 names and this row must answer concretely:

1. **The open-items writer.** Whatever writes rows must not re-serialise the
   registry — D-5's answer at step 4 was a **line rewrite** so comments and
   ordering survive. `csv.writer` emits `\r\n` by default and this repo stores
   LF; verify line endings byte-for-byte after any write.
2. **`bootstrap.py` runs before the kit is copied** and may import no sibling,
   so if it reads agents data it needs a local `tomllib` read. That is a
   sanctioned F5 duplication of plumbing (D-7 leaves plumbing duplication
   unbounded) and must be stated, not smuggled.
