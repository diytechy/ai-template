+++
id = "WI-465"
title = "Pin core.autocrlf in every git-initing test fixture (or one shared builder): the CRLF-conviction fix's diagnosis (log 2026-08-16a) found Git for Windows' system gitconfig (core.autocrlf=true) silently folds CRLF at `git add` in any fixture repo that does not pin it — the clean filter erased the forged relay before it reached the object database, turning one conviction test red and its sibling excuse test VACUOUS on this box. test_integrate.py's git_repo fixture is pinned now, but ~20 other test modules init their own repos without the pin, plus the end-to-end scaffold repo inside test_integrate.py (~line 2811); none is red today because only test_integrate forges EOLs into committed blobs, but any future test asserting on committed bytes in those fixtures hits exactly this, and it will read as a mystery. Scope: one shared fixture helper (or the pin copied into conftest.py's repo builders) so the pin exists once; sweep the ~20 modules onto it; state the mechanism once in the helper's docstring and delete the per-module copies of the explanation. Do NOT change what any test asserts."
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
