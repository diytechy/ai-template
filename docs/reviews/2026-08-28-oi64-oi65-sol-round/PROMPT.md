You are reviewing two open decision items in the repo at c:\Projects\ai-template. Read them yourself:

- `docs/requirements/open-items.toml` — the TOML blocks `[open_item.OI-64]` and `[open_item.OI-65]` (also read `[open_item.OI-63]` and `[open_item.OI-62]` for context; they are already ruled).
- Supporting records: `docs/plans/2026-08-25-oi64-checker-uniformity.md`, `docs/plans/2026-08-25-if-contract-verdicts.md`, `docs/plans/2026-08-25-blind-minimal-map-derivation.md`, `docs/plans/2026-08-25-remap-alignment.md`.
- Registry shapes: `docs/requirements/interfaces.toml`, `docs/requirements/software-requirements.toml`, `docs/requirements/low-level-requirements.toml`.

CONTEXT ON WHO IS READING. The repo owner is the person who must RULE these two items. He works across several projects, does not remember the history, and says he cannot tell what is being talked about. He quoted two lines back as examples of writing he cannot parse:
  - "ADVISORY NEVER GATES: unanimous. trace.exit_code composes from named finding classes only; seven modules carry the phrase 'never the exit code' / 'never gating' 25 times between them."
  - "MINT THE ROW, SWEEP THE CITATIONS"
He wants very short, straightforward language. No special vocabulary, no rhetorical flourish, no emphasis-by-capitals, no invented terms of art. He specifically wants to know, for each option: what it does, whether it CONSOLIDATES existing requirement rows (SR / LLR / IF), whether it ADDS new ones, and why.

YOUR JOB — return a written review with these five sections:

1. WHAT IS ACTUALLY BEING DECIDED. In plain language, at most 8 sentences per item, state the question OI-64 asks and the question OI-65 asks. Assume no memory of the history. If the two rows are really asking one question, say so.

2. REGISTRY EFFECT PER OPTION. For every option in both rows (OI-64 a/b/d; OI-65 part 1 a/b/b'/c/e, part 2 i/ii/iii, part 3 iv/v), state in one line each: does it ADD a row, CONSOLIDATE/edit existing rows, DELETE content, change code/tests, or change nothing — and give the count where the brief gives one. Flag any option where the brief is vague or self-contradictory about this. This is the section the owner most needs; be concrete and check the claims against the actual registry files rather than trusting the brief.

3. SUBSTANTIVE CHECK. Confirm or refute the load-bearing factual claims. In particular:
   - OI-64 lists 13 SR rows as "restating" a finding/severity/exit contract. Spot-check them in `software-requirements.toml`: are they genuinely restating one contract, or are they different obligations that merely share vocabulary? Name any that do not belong in the list.
   - OI-64 claims SR-158's acceptance declares itself unsatisfied. Verify.
   - OI-65 claims the numbers 8,975 remainder chars over 71 rows / 28,305 restatement chars / anchor on 57 of 76 modules. Say whether these are checkable from the tree and whether they hold.
   - OI-65's Part 3 claims nothing reads an interface `rationale` cell (`IF_REASON_CELLS` in `trace.py`), and that `_WI_TOKEN_RE` in `trace_text.py` is case-sensitive. Verify both in the source.
   - Is the recommended sequencing (rule OI-65 before OI-64) sound, or is it circular?

4. WHAT TO CUT. Both briefs are long. List the specific passages that are history, self-justification, or rhetoric rather than information the owner needs to rule — quote the first few words of each so they can be found. Also name anything MISSING that a ruler would need.

5. A REWRITE. Supply a plain-language replacement for the `one_line`, `options`, and `recommendation` fields of BOTH rows. Hard constraints: short sentences; no capitalised slogans; no coined phrases; each option stated as "Do X. This adds/consolidates/changes Y. Cost: Z."; keep every factual claim that survives your section 3 check and drop the ones that do not. Do not lose an option or invent a new one.

Do not edit any file. Return the review as your final message.
