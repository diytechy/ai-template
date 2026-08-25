# Adjudication - the OI-63 legibility round (simplify + cross-review)

Owner-requested (2026-08-25, in session; the request is quoted verbatim in
[BRIEF.md](BRIEF.md)). Provider: **`OPENAI-SOL`** (`gpt-5.6-sol`) via
`codex exec` - the row `docs/agents.toml` declares and `docs/agents-enabled`
lists; no substitution, probed live before dispatch. Two read-only runs; raw
returns unedited in [RAW-TASK1-SIMPLIFY.md](RAW-TASK1-SIMPLIFY.md) and
[RAW-TASK2-CROSSREVIEW.md](RAW-TASK2-CROSSREVIEW.md). Both runs verified to
have written nothing (`git status` clean over their lifetime). Every finding
below was confirmed or refuted against the tree before it was acted on
(findings-are-claims, owner directive 2026-07-30).

## TASK 1 - the simplification draft: ACCEPTED WITH AMENDMENTS

The draft replaces OI-63's five long cells at 8,596 characters against the
prior 15,667 (54.9%), with the taxonomy defined once as a list - the owner's
stated pain. Applied to `docs/requirements/open-items.toml` with these
amendments, each on cause:

1. **The `21` in option (b) corrected via re-derivation, not carried.** The
   reviewer preserved-and-flagged the count conflict (its finding 1); the
   verdict table gives **19** pure-restatement rows, and the truthful (b)
   AGAINST is the fuller **37 rows carrying no remainder** (19 pure + 18 whose
   only other content is non-crossing) - that is what (b) "moves nothing" on.
   This was the one site the `057d47e9` figure-correction commit missed.
2. **The blast-radius opening corrected, not preserved.** The old text called
   (a) the only option inside the kit line while (d)'s own case says it needs
   no kit change (the reviewer's finding 2, found independently by both runs).
   Corrected form: (a) AND (d) stay inside this repo; (b)/(c)/(e) cross the
   kit line. The correction is noted in the cell itself.
3. **The consumer-side-obligation claims qualified per TASK 2's refutation**
   (see below): "structurally cannot state it" became "statable provider-side
   but not synchronizable there - an ownership question a ruling must still
   answer".
4. **Formatting transposed to the owner surface's renderer** (`md_block`:
   `### ` headings, `- ` bullets, paragraphs). The draft's pipe table and
   definition-list syntax would have collapsed into single-paragraph walls -
   the exact 2026-08-12 rendering defect the renderer's docstring records.
   The numbers keep the registry's existing bullet form; content unchanged.
5. **The draft's internal "See Findings" pointers resolved** - they referenced
   the reply's own findings section, which does not travel into a registry
   cell; the two conflicts they pointed at are fixed (items 1-2), so the
   pointers dissolve.
6. **The second opinion appended** to the recommendation cell's "not claiming"
   section, so the ruler sees the qualification beside the numbers it
   qualifies.

## TASK 2 - the cross-review: dispositioned finding by finding

1. **Spot-check (12 AGREE / 3 DISAGREE over 15 rows): ACCEPTED.** The sharpest
   DISAGREE was verified directly: `IF-050`'s "every consumer reads it through
   kitlib.stage.read_stage" is a false universal - `kitlib/stage.py` (the
   "WHO THE FRESHNESS GUARANTEE COVERS" block) states the display surfaces
   deliberately parse the recorded file instead. `IF-061` (retired dual-write
   described as live) and `IF-098` (remainder partly recoverable from public
   docstrings) are recorded as re-adjudication candidates. All three ride the
   verdict document's addendum and OI-63's second-opinion paragraph; the
   per-row verdicts themselves are NOT rewritten here - they are the closed
   WI-516's record, and re-judging three rows is the follow-on pass's act,
   with this round's record as its input.
2. **Consumer-side obligations "structurally unplaceable": REFUTED - ACCEPTED
   AS A QUALIFICATION.** Provider contracts do state caller preconditions;
   what a provider header cannot do is keep the consumer synchronized. OI-63's
   absolute phrasing (and its "WHOLE remainder" claim about four rows, which
   the taxonomy's own mixed tags contradict) is softened accordingly in the
   applied text.
3. **Taxonomy "not ten peer categories" (E/I subtypes of D, H an overlay, F an
   ownership axis): RECORDED, no action.** The taxonomy lives in WI-516's
   durable verdict document; the qualification now rides beside it (addendum)
   and in OI-63. Whether the follow-on pass collapses the classes is that
   pass's call.
4. **The two presentation errors: CONFIRMED AND FIXED** (TASK 1 amendments 1-2
   above).
5. **Arithmetic: CONFIRMED EXACT** by independent re-sum (both the per-family
   table and the 19/18/37 row partition). **Banked, not fixed:** the WI-512
   dossier's per-row `new` column sums to 2,605 against its reported 2,613 -
   an 8-character discrepancy inside a closed row's historical log fragment
   (`docs/log.d/2026-08-24-wi512-contract-generalization.md`), which does not
   touch any figure OI-63 quotes. Left for whoever next opens that record.
6. **Both rot exhibits (IF-117's three falsehoods, IF-055's deleted
   `SCHED_*`): CONFIRMED** against the live tree, with citations. No action
   here - their fix belongs to whatever row owns them (WI-516's own scoping).
7. **The recommendation ((d)-then-re-ask, (c) strong second): directionally
   supported, with the (c) case told not to lean on the refuted absolute.**
   Carried into the applied wording exactly so.

**The reviewer's verdict, quoted:** "The measurement stands, with
qualifications, as a basis for ruling OI-63."

## What changed on disk

- `docs/requirements/open-items.toml` - OI-63's five cells replaced
  (15,667 -> ~9,100 characters after amendments); `title`, `status`,
  `raised` untouched; no other row touched.
- `docs/plans/2026-08-25-if-contract-verdicts.md` - cross-review addendum
  appended (the three flagged rows + this round's pointer); no verdict line
  edited.
- The generated owner surfaces regenerated.

OI-63 stays `pending` - nothing here rules it; the round only makes it
readable and gives the ruler a second opinion beside the numbers.
