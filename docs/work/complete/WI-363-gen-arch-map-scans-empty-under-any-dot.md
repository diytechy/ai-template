+++
id = "WI-363"
title = "gen_arch_map scans EMPTY, without a warning, for any repo whose ABSOLUTE path contains a dot-prefixed directory. _walk_roots skips a file when any(part.startswith(('.', '__pycache__')) for part in path.parts) — over the file's absolute parts, not its repo-relative parts — so a checkout under ~/.local/src, a CI cache dir, or a dot-prefixed pytest temp root (measured 2026-07-29: PYTEST_DEBUG_TEMPROOT=C:/Projects/.pytest-tmp made all 10 of tests/test_gen_arch_map.py's tmp-tree tests scan to '(no source scanned)' while the same tests pass under a non-dot temp root) produces an empty module map with exit 0. Pre-existing, not Phase 5 (the absolute-parts form predates the WI-347 extraction — verified against ac348ac). Fix: apply the dot/__pycache__ skip to parts RELATIVE to the scan root only, and consider a loud warning when a scan yields zero modules from a non-empty --src. Pin with a fixture whose tmp root is deliberately dot-prefixed, both directions."
workstream = "scripts"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
order = 363
+++

## Deliverable

DONE 2026-07-29. The dot/__pycache__ skip applies to parts RELATIVE to each scan root (_is_hidden_rel) — a dot-prefixed ancestor of the checkout no longer empties the map; dot-dirs inside a root still skip (pinned both directions; the bug-direction tests fail against the pre-fix predicate). A sharper stderr warning names the hidden directory that swallowed a non-empty --src (mode-aware wording; exit stays 0; dot-FILES and __pycache__ deliberately not reported so a fresh scaffold's .gitkeep never cries wolf). The adversarial review could not break relative_to under trailing slashes, case, nested roots, dot-prefixed roots, or file-roots.
