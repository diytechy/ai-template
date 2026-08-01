+++
id = "WI-347"
title = "Extract the four remaining one-off same-file duplications triaged under WI-340 (docs/dupes-allow: bootstrap-copy 2, source-walk 1, brief-row-render 1, declared-file-local 1 = 5 sanctioned blocks): check_docs.py's read/strip/skip-comment declared-file loop, which appears twice in that one file (once collecting every non-comment line, once taking the last) and which WI-340 wrongly filed under the CROSS-script declared-file F5 sanction - 129-REVIEW-A MAJOR 3; bootstrap.py's copy-if-absent-or-forced loop and skills-refresh walk, gen_arch_map.py's rglob('*.py') walk with the dot/__pycache__ skip repeated in its single-root and multi-root arms, and trace.py's `for k, v in row['full'].items()` bullet renderer in the no-baseline and added-row arms of the re-attestation brief writer. Small and independent - each is a helper, not a design change."
workstream = "scripts"
needs = ["WI-340"]
buildtier = "medium"
priority = 0
safety_class = "ordinary"
order = 344
+++

## Deliverable

Extracted all five one-off same-file duplications, none sanctioned: check_docs.declared_lines (the declared-file idiom stated once, replacing the read/strip/skip-comment loop in load_orphan_classes and _status_lint_policy); bootstrap.copy_if_new (write-once scaffold copy, 3 sites) and bootstrap._skill_rel (the refreshed-path identity shared by the write and delete arms); gen_arch_map._walk_roots (the dot/__pycache__ source-walk shared by _module_files and _source_files); and trace._full_row_bullets (the whole-row renderer shared by the no-baseline and added-row arms of the re-attestation brief). Census 201 -> 196; each fingerprint proven absent from --emit-census before its sanction was deleted. Two things the extraction surfaced: the declared-file class needed a 3-fingerprint RE-STAMP (same 11 blocks, new extents, because removing check_docs' copy from the clique changed how the remaining pair matches), and the header's declared TOTAL had been stale by 6 since before this commit, unchecked by the audit guard -> WI-356.
