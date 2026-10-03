# WI-755 adjudication: LLR-268 Detail, TC-264 Method (amendment, trunk 6e89705b)

Adjudicator: Claude Opus 5.5, independent of WI-748 (built by Codex Sol, reviewed by Claude Sonnet 5.5).
Judged on the before/after cells only. The code (`CodexAdapter.usage` in `session_adapters.py`) and the tests
(`test_codex_usage_is_mapped_inclusive_with_fresh_input_derived`,
`test_codex_cache_write_present_or_absent_inline_recording_variant`) were read only to decide whether the new
text is blessable for re-attestation. The three session modules pass at 6e89705b: 123 passed.

- [MEANING] LLR-268 Detail -> codex: fresh = input_tokens - cached_input_tokens; no cache write is reported, so the cache-write column is always empty whatever the stream carries -> codex: input_tokens is taken as including cache writes as well as cached input (stated as not yet verified live); fresh = input_tokens - cached_input_tokens - cache_write_input_tokens, clamped at zero; cache_write_input_tokens and reasoning_output_tokens are read when reported and empty when absent -> not the same: an implementation correct under the old text leaves cache write empty on a stream reporting it (the live line reports 0) and never clamps fresh, so it fails the new text. The adapter now reads a field it was obliged to ignore, and the fresh formula changed.
- [MEANING] TC-264 Method -> assert codex's cache write and reasoning, being unreported, stay empty -> assert codex's input is taken as including cache writes, fresh subtracts both cache counts and is never below zero, cache write and reasoning are read when reported and empty when absent, and drive cache-write absence and a nonzero count as inline variants of the live line -> not the same: the old check (cache write empty on the live line) is now a failure (it reads 0), and two new cases (absent, nonzero with clamping) are required.

Re-attestation: I would bless both new texts. They match the code and its tests. The hedge ("not yet verified live") is stated honestly in both rows. The clamp is consistent with LLR-268's general builder formula: input_tokens is fresh + read + write, so a clamped fresh yields input_tokens = read + write, which is what the 4000 variant asserts. Observation, not a finding: if a live recording ever shows that codex's input_tokens EXCLUDES cache writes, both rows and the clamp need revisiting, and the hedge already says so.

VERDICT: MEANING rows=2
