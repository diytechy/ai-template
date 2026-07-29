+++
id = "WI-363"
title = "gen_arch_map scans EMPTY, without a warning, for any repo whose ABSOLUTE path contains a dot-prefixed directory. _walk_roots skips a file when any(part.startswith(('.', '__pycache__')) for part in path.parts) — over the file's absolute parts, not its repo-relative parts — so a checkout under ~/.local/src, a CI cache dir, or a dot-prefixed pytest temp root (measured 2026-07-29: PYTEST_DEBUG_TEMPROOT=C:/Projects/.pytest-tmp made all 10 of tests/test_gen_arch_map.py's tmp-tree tests scan to '(no source scanned)' while the same tests pass under a non-dot temp root) produces an empty module map with exit 0. Pre-existing, not Phase 5 (the absolute-parts form predates the WI-347 extraction — verified against ac348ac). Fix: apply the dot/__pycache__ skip to parts RELATIVE to the scan root only, and consider a loud warning when a scan yields zero modules from a non-empty --src. Pin with a fixture whose tmp root is deliberately dot-prefixed, both directions."
workstream = "scripts"
specref = "docs/concurrency-restructure.md"
buildtier = "quick"
priority = 2
safety_class = "ordinary"
order = 363
+++
