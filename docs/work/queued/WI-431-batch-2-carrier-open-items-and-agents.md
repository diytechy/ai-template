+++
id = "WI-431"
title = "Batch-2 of the carrier migration (repo-lock §8.1), FIRST SLICE: convert docs/requirements/open-items.csv (7 rows, the 3,126-char cell that is the loudest case in the repo) and docs/agents.csv (10 pair rows + 3 load-bearing comment lines) from CSV to the TOML carrier D-5 ruled, plus their templates - registries/open-items.template.csv and the kit-root agents.template.csv. CARRIER ONLY, exactly as D-5 was: no row's text changes, no schema changes, no Status vocabulary change. EXPLICITLY OUT OF SCOPE and must not be touched: interfaces.csv (waits for OI-14, which rewrites what a Contract cell may hold - converting first means converting twice) and components.csv (waits for the components ruling, which is ABOUT CMP rows). Extend migrate_carrier.py with a per-registry KEY map as §8.1 records; do NOT write a second converter, which is the exact D-6 hazard. Extend spine_carrier.py rather than adding a second module: D-6 gave the registry vocabulary ONE home and the generic machinery (resolve/rows_from_toml/load/columns/empty_value_findings) is what a second module would duplicate. THE CUTOVER IS THE DETECTOR - D-5's hardest-won lesson is that wiring readers against the OLD carrier can never surface an unwired one, because every reader looks fine while the file it expects still exists; run the conversion against a throwaway tree first and fix what actually breaks. A carrier that does not parse is reported ABSENT, never EMPTY (spine_carrier._toml_rows_text's None-not-{} shape) - {} on a decision queue means `no open items`, a silent false green. Re-verify the reader inventory rather than trusting §8.1's. Extend test_dogfood_sync's spine key-set rule (live keys subset-of schema, template keys == schema, schema subset-of carrier vocabulary) to both new registries rather than inventing a second rule, and drive it against planted defects in both directions. Regenerate docs/open-items.html. Note the migration in ADOPTING.md. Decide whether gen_open_items.normalize survives the carrier change and say why. The OI watermark (OI = 14) must not move."
workstream = "scripts"
specref = "docs/repo-lock.md"
buildtier = "strong"
safety_class = "registry"
+++

## Context

Owner-approved 2026-08-11 as the first slice of the batch-2 sweep recorded in
[repo-lock.md](../../repo-lock.md) §8.1, unblocked by D-5's execution the same
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
