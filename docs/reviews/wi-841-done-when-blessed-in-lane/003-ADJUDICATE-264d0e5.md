# WI-841 amendment adjudication at 264d0e5

Question: did each amendment change the requirement's MEANING, or only its CLARITY?
Judged on the before/after cells only, against the anchor copied at de1b1cde.

- [MEANING] LLR-262 Detail -> at merge intake evaluates every claimed non-adjudication row whose closed Done-when changed; the text says nothing about the claim itself being missing or unreadable -> the same evaluation, but only for a readable claim: an UNREADABLE claim refuses the mint, and an ABSENT claim mints nothing and states that the check did not run -> two new arms. An intake that was correct under the old text, and that skipped silently or minted on a missing or unreadable claim, fails the new text: one arm adds a refusal, the other adds a stated skip. The rest of the cell is unchanged
- [MEANING] LLR-278 Detail -> a snapshot is WIDENED only when the act neither flipped nor re-attested a row "in that registry" -> the same rule, but the registry is now named by "the carrier file that supplies that registry's rows (TOML, legacy CSV or markdown)" -> the new text pins which file counts as the registry and requires all three carrier formats. An implementation that keyed the registry on its TOML path met a literal reading of the old text. It fails the new text for a CSV- or markdown-carried registry: a copy the act did move would be refused WIDENED. The acceptance condition now covers those carriers, and the rest of the cell is unchanged

Both rows are MEANING, and the tier's rung is RELEASED, so the blessing is the adjudicator's to give:

- LLR-278: I would bless it. The text is closed and readable.
- LLR-262: I would NOT bless it as written. The spliced sentence "For a readable claim, it whose closed spec's Done-when changed against trunk's pre-merge copy under active/<branch>/: ..." has no verb. Its subject, "it", stands for the row, but "it" also names the intake, two clauses earlier and later in the same sentence. "An unreadable claim refuses the mint" does not say whether the merge as a whole is refused. "States that the check did not run" names no channel. The obligation can be recovered and matches `intake.py`'s `kdone.claim_copy` arm. But a normative cell a human signs has to read as one obligation, not as a recovery exercise. The correction is drafted under `## Dispositions` in `docs/work/active/wi-841/WI-841-done-when-blessed-in-lane.md`.

Because LLR-262 stays drifted in `docs/requirements/low-level-requirements.toml`, the snapshot copy for that registry is refused. So LLR-278 cannot be re-anchored in this sitting either: it is left unanchored, to be re-attested with LLR-262 once LLR-262's text is restated.

VERDICT: MEANING rows=2
