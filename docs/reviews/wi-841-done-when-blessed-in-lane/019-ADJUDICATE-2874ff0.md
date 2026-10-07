# WI-841 amendment adjudication at 2874ff0

Question: did each amendment change the requirement's MEANING, or only its CLARITY?
Judged on the before/after cells only, against the anchor copied at acdf221a (LLR).

- [MEANING] LLR-308 Detail -> the done-when verdict carries exactly one complete DONE-WHEN line with an allowed label and both fields -> each physical line is read on its own, still exactly one complete DONE-WHEN line, and a split or bare DONE-WHEN line invalidates the verdict -> the old text counted only COMPLETE lines. A parser that ignored a stray bare `DONE-WHEN:` line, or joined a label carried onto the next line, met the old text and is refused by the new one, which adds a refusal case
- [MEANING] LLR-310 Detail -> a combined sitting has exactly one complete own-kind machine line IN EACH SECTION; a single-kind verdict has exactly one complete machine line -> every line whose first token is a machine keyword counts, complete or not, so a bare, split, bad-label or field-missing line invalidates; a combined sitting has, ACROSS THE WHOLE FILE, exactly one complete line per bound kind and exactly one SITTING line, and no line for another kind -> the count moves from per section to the whole file, so a keyword line outside every section now invalidates. Exactly one SITTING line is now required, incomplete keyword lines count, and other-kind lines are forbidden file-wide. A verdict valid under the old text can be refused by the new one

Both rows are MEANING. The LLR tier's rung is RELEASED, so the blessing is the adjudicator's to give. I would bless both new texts:

- The cells state one rule. A machine line is one physical line, and every keyword line counts toward the exact-count check, so nothing outside a well-formed line can pass unseen.
- The code matches:
  - `kitlib.sitting._keyword_lines` reads strictly one physical line at a time and keeps bare and incomplete lines.
  - `_machine_lines` / `_incomplete` refuse a bare, bad-label or field-missing line.
  - `_keyword_count_refusal` counts every kind's keyword over the WHOLE text against exactly one per bound kind plus one `SITTING`, and zero for any other kind.
  - The done-when grammar (`DONE-WHEN`, `changes`, `digest`) is read through the same parser.

The re-attestation is taken in its own act.

VERDICT: MEANING rows=2
