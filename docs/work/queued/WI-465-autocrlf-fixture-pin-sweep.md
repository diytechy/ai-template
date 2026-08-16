+++
id = "WI-465"
title = "Pin core.autocrlf in every git-initing test fixture (or one shared builder): the CRLF-conviction fix's diagnosis (log 2026-08-16a) found Git for Windows' system gitconfig (core.autocrlf=true) silently folds CRLF at `git add` in any fixture repo that does not pin it — the clean filter erased the forged relay before it reached the object database, turning one conviction test red and its sibling excuse test VACUOUS on this box. test_integrate.py's git_repo fixture is pinned now, but 28 other git-initing fixture sites remain unpinned (measured at the 2026-08-16b adversarial round), including FIVE near-verbatim clones of git_repo itself — tests/test_check_lane.py, test_dispatch.py, test_intake.py, test_integrate.py, test_wi_folder_loaders.py — of which only one got the pin, so the siblings now diverge silently with nothing comparing them. None is red today because only test_integrate forges EOLs into committed blobs, but any future test asserting on committed bytes in those fixtures hits exactly this, and it will read as a mystery. Scope: EVALUATE THE KIT'S OWN SHIPPED MECHANISM FIRST — bootstrap writes .gitattributes with `* text=auto eol=lf`, which overrides core.autocrlf outright (the e2e scaffold repo in test_integrate.py is already immune this way, so it is NOT in this sweep); a fixture that writes the same .gitattributes matches production more honestly than 28 copies of a config pin. Then: one shared helper (or the conftest builders) carrying whichever remedy wins, the 28 sites swept onto it, the mechanism stated once, the five git_repo clones reconciled. Do NOT change what any test asserts."
specref = "docs/log.md"
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Context

Found at WI-461's close (2026-08-16, the re-tier v2 precondition wave). The
mechanism, verified on this box: Git for Windows writes `core.autocrlf=true`
into the SYSTEM gitconfig, fixtures inherited it, and `git add` normalized
working-tree CRLF to LF on the way into the object database — so byte-exact
assertions about committed content silently tested LF-only content. POSIX
boxes default to false and never see it, which is exactly the shape of bug
that survives until someone runs the suite on a stock Windows install.
The fix pattern is already in the tree: `test_integrate.py::git_repo` pins
`core.autocrlf false` repo-locally beside its existing `commit.gpgsign
false` pin, with the mechanism recorded in the fixture docstring.
