# Brief — the OI-63 legibility round (simplify + cross-review)

Provider: OPENAI family, `OPENAI-SOL` (`gpt-5.6-sol`) via `codex exec`, the row
`docs/agents.toml` declares and `docs/agents-enabled` lists. No substitution:
the owner asked for "OpenAI sol" and that entry exists. Probed live before
dispatch (PONG).

Two tasks, dispatched as two separate runs. Each run is told which task is
its. **Both runs are READ-ONLY: edit no file, run no write command. Your final
message is the whole deliverable** — it is saved verbatim into this directory
and adjudicated by the coordinating session before anything is applied.

The owner's request, verbatim, which is this round's charter:

> Can you kick up an OpenAI sol reviewer, esspecially to go through and
> simplify the Open-items.toml text, it's very hard for me to follow precisely
> what was found, what the blast radius was, what catagories were identified,
> and what the exact options are and what they expose. I suppose OpenAI sol
> could run a cross-review at the same time just to get a second opinon on the
> findings.

## Shared context (read before either task)

- `docs/requirements/open-items.toml`, the `[open_item.OI-63]` row (near the
  end of the file) — the text the owner finds hard to follow.
- `docs/plans/2026-08-25-if-contract-verdicts.md` — the WI-516 measuring
  pass's durable per-row verdict record: one line per IF id over all 108
  non-CLI `contract` cells, the taxonomy, and the derivation table whose sums
  reproduce every headline figure.
- `docs/requirements/interfaces.toml` — the registry the verdicts are about.
- Background: OI-62's ruled option (e) (MEASURE, DON'T REWRITE) is recorded in
  the `[open_item.OI-62]` row of the same file; WI-516 executed it and filed
  OI-63 as its close obligation.

## TASK 1 — the simplification draft

Audience: the human owner, who must RULE on OI-63 and reports the current text
does not let them follow (their words) *what was found, what the blast radius
was, what categories were identified, and what the exact options are and what
they expose*.

Produce replacement text for the OI-63 row's four long cells — `one_line`,
`decision`, `blast_radius`, `options` — and, if you judge it also needs it,
`recommendation`. Deliver each as a clearly labelled block of plain text (the
cells are TOML multi-line strings; give the content only, no TOML quoting).

Hard constraints — a draft that violates one is rejected whole:

1. Every measured number stays EXACT (the per-family table, the character
   counts, the row counts 108/71/19/18, the 57-of-76 anchor, all of it).
2. Text inside quotation marks attributed to the owner stays VERBATIM.
3. No option may be dropped, and no FOR/AGAINST substance may be silently
   lost — compress, structure, deduplicate, but do not decide.
4. The provenance stays: that the row discharges obligation 2 of OI-62's
   ruling, and what OI-62 ruled.
5. Invent no fact. If something in the current text looks wrong or
   inconsistent, FLAG it in a separate "findings" section of your reply — do
   not silently fix it.
6. The CATEGORIES must be stated as a definition list the owner can hold in
   mind while reading (restatement / irreducible remainder and its classes /
   non-crossing) — the verdict document defines them; today the OI row uses
   them without defining them, which is part of the illegibility.

Aim: roughly half the current character count, structure over prose (short
headed sections, bullets, one table is fine), every sentence earning its
place. State the character counts of your draft cells at the end.

## TASK 2 — the cross-review (second opinion on the findings)

You are a cross-family REVIEWER. The WI-516 pass's outputs are CLAIMS; your
job is to independently confirm, refute, or qualify them. Do not extend the
work; judge it.

1. **Spot-check the verdicts.** Pick at least 12 rows — spread over both
   tranches (Provides and Consumes), including at least two rows the document
   marks pure restatement, two with a large remainder, and two with heavy
   non-crossing content. For each: read the LIVE cell in
   `docs/requirements/interfaces.toml`, form your own clause classification,
   and compare. Verdict per row: AGREE / DISAGREE (with the clause and the
   reason).
2. **Check the arithmetic.** Re-sum the verdict table's columns and compare
   against every headline figure quoted in OI-63 (the per-family table, 71
   rows with remainder, 19 pure restatement, 18 zero-remainder-but-long).
3. **Judge the taxonomy.** The pass extended WI-512's three remainder
   categories by seven. Are the extensions real categories or relabelled
   restatement? Is CONSUMER-SIDE OBLIGATION genuinely unplaceable in a
   provider-side header, as claimed?
4. **Verify the two rot exhibits.** IF-117's three claims (a present-tense
   reference to a retired module map, a false claim about which oracle the
   `sym:` tier reads, a stale 149 against a live 184) — check each against the
   live tree. IF-055 likewise if quick.
5. **Judge the recommendation.** OI-63 recommends (d)-then-re-ask with (c) as
   strong second. Given the numbers as YOU verify them, is that the reading
   the evidence supports? A one-paragraph answer, not a re-derivation.

Format: a findings list, most severe first, each with CONFIRMED / REFUTED /
QUALIFIED and the evidence (file + line or quoted clause). End with a verdict
paragraph: does the measurement stand as a basis for ruling OI-63?
