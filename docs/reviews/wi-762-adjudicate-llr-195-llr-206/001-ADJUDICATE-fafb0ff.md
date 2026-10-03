# WI-762 adjudication: LLR-195 and LLR-206 Detail amendments (WI-657)

Independent adjudicator (Claude Opus 5.5), 2026-10-03, over the cells shown in
the composed amendment brief only. Anchor: docs/archive/last_approved
low-level-requirements.toml as copied at 87736778.

- [MEANING] LLR-195 Detail -> before: the dupes-census step is wired at layer=product, from-stage=DevStg-Impl, so it is selected only when the repo is at or above that rung -> after: the same measure()/main() contract, plus a selection rule: a step with declared paths also runs below its rung when a changed path matches a declared pattern, runs whenever the change is unknown (failed reads, or no staged diff and no usable lane-base diff), stays rung-only without paths, and its per-stack patterns must include its baseline, script and config -> not the same: an implementation correct under the old text (rung-only selection, no paths declaration) fails the new text, which adds a selection case below the rung, an unknown-change fallback and a declaration-content obligation; the measurement and always-0 exit are unchanged, the obligation added is in the selection sentences.
- [MEANING] LLR-206 Detail -> before: this repo's [step:complexity] is layer=product at DevStg-Impl and runs --mode enforce, i.e. the enforce gate is armed only at or above DevStg-Impl -> after: the same counting, census and CLI-mode contract, plus "ARMED means selected by the rung OR path trigger, including below DevStg-Impl", the path-match and unknown-change selection rule, rung-only without paths, and per-stack patterns that include the baseline, script and config -> not the same: the enforce gate now fires below DevStg-Impl on a matching or unknown change, a scope the old text did not impose; a rung-only implementation that met the old text fails the new one.

VERDICT: MEANING rows=2
