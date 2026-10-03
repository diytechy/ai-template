# WI-749 ADJUDICATE @ 579cd18 — LLR-116, TC-121, TC-262, TC-263, TC-264, TC-267

Independent spine-acts adjudication of approved cells amended after attestation
(anchor: docs/archive/last_approved, copied 2026-09-29 at a4919610). Checked
against the code and tests at 579cd187: `traj_render._svg_fit_style` emits
`min-width:ceil(width * 9 / min(NODE_TYPE_PX))` with `NODE_TYPE_PX = {nlabel 12,
nsub 10.5, nhead 13}`; `tests/golden/sessions/{codex-exec-json,codex-rollout,
opencode-run-json}.jsonl` carry no NOT LIVE line and record codex-cli 0.157.1 /
opencode 1.18.29 sessions; TC-121's two t7 tests and the 107 session-adapter /
keep / service tests pass.

- [MEANING] LLR-116 Detail -> every SVG carries min-width = natural x the declared SHRINK_FLOOR ratio (0.62), views wider than 390/SHRINK_FLOOR scroll -> every SVG carries min-width = ceil(natural x 9 / smallest emitted node type token), derived from NODE_TYPE_PX, so no node label renders below 9 px; a view whose min-width exceeds its container scrolls -> the shrink limit moved (0.62 -> ~0.857 of natural with 10.5 px sub-labels), its source changed from a hand-set ratio to a type-scale derivation, whole-pixel ceiling rounding was added, and the scroll condition changed; a correct old implementation (ratio 0.62) fails the new text.
- [MEANING] TC-121 Expected+Method -> assert the responsive style on every SVG and that the emitted min/max ratio equals SHRINK_FLOOR -> assert the responsive style, the emitted token sizes (12 / 10.5 px, all >= 9 px), 0 < min-width <= natural, every token >= 9 px at min-width, and that min-width minus 1 px would breach 9 px -> the ratio-equality check is removed and new acceptance conditions (token sizes, 9 px floor, minimality) are added; a test passing the old method fails the new one.
- [MEANING] TC-262 Method -> run over codex and opencode fixtures built from documented event shapes, NOT LIVE, with live recording and an opencode re-check owed to a person -> run over LIVE codex-cli 0.157.1 / opencode 1.18.29 recordings, opencode pathway re-checked on that version -> the test's input evidence changed (a test over documented-shape fixtures no longer satisfies the method) and an owed obligation is declared discharged; the assertions are otherwise identical.
- [MEANING] TC-263 Method -> opencode and codex occupancy asserted over NOT LIVE documented-shape fixtures, live recording owed -> asserted over the LIVE codex and opencode recordings (2026-09-30) -> same assertions, but the fixture provenance the method requires changed and the owed live recording is declared done.
- [MEANING] TC-264 Method -> codex and opencode usage records asserted over NOT LIVE documented-shape fixtures, live recording owed -> asserted over LIVE fixtures (claude 2026-09-28, codex and opencode 2026-09-30) -> fixture provenance requirement changed; assertions otherwise identical. Note (not a return): over the live codex line `cache_write_input_tokens` IS reported (0), so the unchanged clause "its unreported cache write ... stay[s] empty" now pins the adapter's known gap; WI-748 already owns reading that field and will amend this clause, so the amendment judged here is blessed as is.
- [MEANING] TC-267 Method -> retention assertions over claude LIVE and codex/opencode NOT LIVE fixtures, live recording owed -> over all three LIVE fixtures -> fixture provenance requirement changed and the owed recording declared done; every reset-clause and store assertion is unchanged.

VERDICT: MEANING rows=6
