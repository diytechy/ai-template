+++
id = "WI-078"
title = "Wire [step:dupes] + docs/dupes-allow census (F5 bound)"
workstream = "scripts"
sr_refs = []
needs = ["WI-037"]
order = 77
+++

## Deliverable

WI-078 (2026-07-13): wired the duplicate-code gate + populated its census (the 2026-07-12 review's M2/M6, owner-ruled option (b) - gate NEW duplication over an allowlist that IS the census; keep every script independently copy-able, the shared-helper module rejected). Added [step:dupes] to docs/stack.ini (command {py} project-trajectory/scripts/check_dupes.py --src {src}; gates=G3, layer=product) so check.py extra_steps slots it beside format/lint/tests in the G3 plan + CI gate job - NO kit-shipped file touched, the machinery (check_dupes.py + the extra_steps [step:<name>] hook) already existed. Populated docs/dupes-allow (the default --allowlist path) as the census: all 57 file-PAIRS currently carrying duplication (128 blocks), split + annotated - 51 cross-file F5 sanctioned small-helper pairs (the _utf8_console emitter, the one-line declared-policy readers, refs()/argparse/exit scaffolding) and 6 intra-file GRANDFATHERED debris pairs (agent_loop/trace/check_trajectory/gen_arch_map/gen_okf/gen_trajectory) recorded for removal under the WI-080/081 decomposition effort, not blessed. The gate now turns G3 RED on new copy-paste between an UNLISTED pair; the honest limitation (pair-level granularity - the finding form carries no block identity, so new dupes between already-listed files are not caught; finer censusing would need a check_dupes change) is stated in the census header, out of scope here. Verified: check_dupes --src project-trajectory/scripts OK (0 findings post-census, was 128); full derived G3 gate PASS incl. the new dupes step (dupes 0.5s), full suite 695 passed/3 skipped at 91.26%, smoke 543 passed, check_docs --stale OK. No spine change (no new SR/LLR/TC - proceed at G3), no byte-budgeted file touched.

**2026-08-11 (WI-426, repo-lock D-7):** the duplication census was torn down by owner ruling — `check_dupes.py`, its census file and the spine chain SR-039 → LLR-036 → TC-039 are DELETED (D-4: supersession is deletion, ids are never reused). This row's `sr_refs` is cleared because it is a machine-read join field and the row it named no longer exists; the prose above keeps its citations, which are accurate history. The forwarding pointer for the retired ids is the `docs/log.md` Decisions entry of 2026-08-11.
