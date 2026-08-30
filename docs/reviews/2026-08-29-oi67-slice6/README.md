# OI-67 slice 6 — the cross-family adversarial round (2026-08-29)

The round the WI-533 close owed ([the fragment](../../log.md#2026-08-29--wi-533-the-gate-is-armed-oi-67-slice-6),
"Owed, stated"): the slice-4 adversarial prompt re-targeted at the slice-6
build — the armed definition gate, the retired cells, the one CSV reader, the
external rule, the `gen_okf` fix, the slice-4 dispositions — and run by a
different model family (gpt-5.6-sol, medium effort) read-only in a throwaway
git worktree at `8599f2b0`, the branch tip. Every finding was reproduced by
the coordinator before it was acted on; the real ones were fixed at their
root in the commit that carries this folder.

- `PROMPT-ADVERSARIAL.md` — what the reviewer was told: the build list from
  the fragment, the files to read, eight things to find (false greens by
  planting, the reader's edge cases, the external bodies' truth, the slice-4
  dispositions on the tree, the HTML-comment skip, citation rot, the migration,
  the record vs the tree).
- `RAW-SOL-ADVERSARIAL.md` — the reviewer's answer, verbatim: `VERDICT:
  CHANGES-REQUESTED findings=11`, with every plant it made and restored.

## Dispositions

| # | Finding | Reproduced | Disposition |
|---|---|---|---|
| 1 | CRITICAL — one malformed body (an empty `Contract IF-069:` opener) makes `_declaration_sites` swallow the grammar error and return no surface, so the whole gate goes vacuous: `--strict` exits 0 | yes — empty and whitespace-only bodies both exit 0; the reference freshness step is what reds (`STALE`) | **APPLIED** — `scan_contracts` grows a per-source grammar arm the gate opts into; a refused header is the gate's fourth finding shape and the scan continues past it; the reference generator's path still raises |
| 2 | MAJOR — an `external:`-owned row whose far side is all external owes no body anywhere | yes — `owner = "external:git"`, `consumers = ["external:y"]`, declaration removed: exit 0 | **APPLIED** — `trace.interface_findings` fails a row with no in-tree endpoint (decision 6.8) |
| 3 | MAJOR — the ordinary harness runs `check_trajectory` without `--strict` below `DevStg-Impl`; this tree is at `DevStg-LLReqs`, so "armed" means a direct strict run | yes — `check.py` promotes at `STAGE_IMPL`; `docs/stage` reads `DevStg-LLReqs` | **KEPT, on record** — the gate rides the severity ladder by design (the seam-TC idiom); decision 6.7 states why and what the floor catches instead; the fragment is annotated |
| 4 | MAJOR — six shipped and live texts say an owner that declares nothing is a strict finding, contradicting decision 6.2 and the code | yes — `interfaces.toml` header, the template header, `INTERFACES.template.md`, `PROCESS.md` §8, the RESYNC entry, `enforcement-audit.md` | **APPLIED** — all six say warn-only, and name the new grammar-refused shape |
| 5 | MAJOR — "every kit reader goes through" the one CSV reader is false: `agent_route.py:236`, `intake.py:1600`, `check_flows.py:80` are raw | yes, plus a fourth the reviewer did not name: `spine_carrier.columns` (`:731`) reads a CSV header raw | **APPLIED** — the three routed through `kitlib.spine.csv_body`; `check_flows.col` (unused) deleted; `migrate_carrier.py:409` stays raw by design (a comment is a record there) |
| 6 | MAJOR — `csv_body` keeps a blank line after the comment block, which `DictReader` takes as the header | yes — `csv_rows("# c\n\na,b\n1,2\n")` → `[{None: [...]}, ...]` | **APPLIED** — blank lines are preamble until the first header row |
| 7 | MAJOR — retired cells are detected by non-empty VALUE: `provider = ""` and a nested `[interface.X.legacy] contract = …` pass | PARTLY — the two plants are REFUSED by the carrier before the rule runs (`spine_carrier.load` raises on an empty string and on a nested table; the refusal prints to stderr, which the reviewer's exit-code reading missed — the coordinator's first reproduction made the same mistake); the real hole is the one behind them: a retired COLUMN in a legacy CSV header stayed silent as long as no cell was filled, and a test pinned that as correct | **APPLIED** — detection by key PRESENCE through `spine_carrier.columns` (one finding per retired key naming its rows; on a CSV carrier the header column, once); the two carrier refusals pinned by tests as the mechanism that owns those shapes. Downstream: an un-migrated `interfaces.csv` whose header still declares a retired column now reds `trace --strict` (a one-line edit; the RESYNC entry says so) |
| 8 | MAJOR — `EXAMPLE.md` §9/§10 still teach `provider` / `contract` / `req_refs` rows with an SR-id owner | yes | **APPLIED** — §9 rewritten to one owner-row with the header body beside the code and the TC citing the seam; §10's coordinator rows rewritten as `external:`-owned rows with an in-tree far side (decision 6.8) |
| 9 | MINOR — `_doc_title_and_summary` drops the text after `-->` on the opener's line | yes — `<!-- hidden --> # Real` → `('', 'Para')` | **APPLIED** — the remainder after a comment close is parsed as a line |
| 10 | MINOR — "sixteen reason cells trimmed" does not reproduce from `docs/if-tc-coverage-allow` | the PROMPT mis-located the cells (they are `interfaces.toml` reason cells, in `87c1fc38`); measured there: **fourteen**, not sixteen | **APPLIED to the record** — the fragment says fourteen with the derivation; not a defect of the build |
| 11 | MINOR — `trace --strict` is red at baseline (`LLR-197`, `SR-181` ×2) | yes — the three standing reds named in the WI-531 fragment, predating the program | **KEPT** — a standing red, on record; the fragment claimed `--strict-integrity`, which is clean |

Two things the reviewer checked and found true, worth keeping: the three
external bodies match the code beside them, and every count in the record
reproduced (154 rows, 74/154/154, the four line ratchets, the PROCESS.md
bytes, the smoke stamp).
