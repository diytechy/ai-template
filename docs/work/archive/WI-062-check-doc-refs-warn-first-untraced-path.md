+++
id = "WI-062"
title = "check_doc_refs warn-first untraced-path tier"
workstream = "scripts"
needs = ["WI-035"]
safety_class = "ordinary"
order = 61
+++

## Deliverable

check_doc_refs.py's path tier now splits UNTRACED from DANGLING, on a mechanical REASON rather than a suppression list: a missing path is untraced when it resolves under --kit-root (a kit's prose names its portable unit by the paths an ADOPTING repo will have after copy-in, so scripts/check.py is correct for its reader) or when the doc is a --record-prefix surface (log/archive/reviews/plans/review reports, where a since-retired path is accurate history and 'fixing' it would falsify the record). Also dropped three placeholder shapes that were never paths: … (and-the-rest), ###/NNN (your-id-here), and # (an anchored reference is a LINK, check_docs.py's job). Untraced findings are counted, never gate, and print only with --show-untraced; --strict gates on dangling alone. The count is ALWAYS reported even when the list is silent, because a classification whose size you cannot see is a suppression list. Effect on this repo: 561 findings -> 22, all reviewable; the residue is now visible enough to triage, filed as WI-308. Guards: tests/test_check_doc_refs.py::test_kit_relative_path_is_untraced_not_dangling, ::test_record_surface_path_is_untraced_not_dangling, ::test_untraced_count_is_always_reported_even_when_silent, ::test_placeholder_and_anchored_shapes_are_not_paths - each carries a negative half (the same token still gates when the reason does not apply), and all were verified to fail with the tier disabled.
