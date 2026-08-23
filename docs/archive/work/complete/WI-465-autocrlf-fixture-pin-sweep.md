+++
id = "WI-465"
title = "Pin core.autocrlf in every git-initing test fixture (or one shared builder): the CRLF-conviction fix's diagnosis (log 2026-08-16a) found Git for Windows' system gitconfig (core.autocrlf=true) silently folds CRLF at `git add` in any fixture repo that does not pin it — the clean filter erased the forged relay before it reached the object database, turning one conviction test red and its sibling excuse test VACUOUS on this box. test_integrate.py's git_repo fixture is pinned now, but 28 other git-initing fixture sites remain unpinned (measured at the 2026-08-16b adversarial round), including FIVE near-verbatim clones of git_repo itself — tests/test_check_lane.py, test_dispatch.py, test_intake.py, test_integrate.py, test_wi_folder_loaders.py — of which only one got the pin, so the siblings now diverge silently with nothing comparing them. None is red today because only test_integrate forges EOLs into committed blobs, but any future test asserting on committed bytes in those fixtures hits exactly this, and it will read as a mystery. Scope: EVALUATE THE KIT'S OWN SHIPPED MECHANISM FIRST — bootstrap writes .gitattributes with `* text=auto eol=lf`, which overrides core.autocrlf outright (the e2e scaffold repo in test_integrate.py is already immune this way, so it is NOT in this sweep); a fixture that writes the same .gitattributes matches production more honestly than 28 copies of a config pin. Then: one shared helper (or the conftest builders) carrying whichever remedy wins, the 28 sites swept onto it, the mechanism stated once, the five git_repo clones reconciled. Do NOT change what any test asserts."
workstream = "process"
sr_refs = []
needs = []
buildtier = "quick"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Re-measured the census (28 git-initing files / 43 call sites — the spec's
count plus two sites it missed and two new since; 5 sites already immune
via bootstrap's shipped `.gitattributes`). EVALUATED the spec's suggested
`.gitattributes` remedy and REVERSED it with the reasoning on record:
`* text=auto eol=lf` normalizes unconditionally, which would relocate the
exact byte-loss bug into the fixture layer and foreclose any future
byte-sensitive assertion — the config pin (`core.autocrlf false`, the
mechanism test_integrate.py::git_repo already proved) is inert on a
correct box and forecloses nothing. One shared `conftest.pin_autocrlf`
helper states the mechanism once; all 23 non-immune files swept onto it;
the five git_repo clones reconciled onto the identical call; no test
assertion changed. One self-caught bug mid-sweep (a replace_all planted
the call against the wrong parameter name in two closures — caught by
RUNNING the file). Full suite 2647 passed / 13 skipped; smoke green.

**CORRECTED CENSUS (2026-08-20, closing review ROUND-OPUS MINOR-17).** The
census above does not reproduce. Re-measured at the batch close: **30 files
git-init, not 28**, and **12 call sites were still unpinned** — one each in
`test_check_privacy.py`, `test_pre_push_hook.py`, `test_dispatch.py` and
`test_integrate.py`, and eight in `test_pre_commit_hook.py` (three modules
carried no `pin_autocrlf` import at all, which is how a per-file sweep loses
a file rather than a line). The helper claim and the zero-assertions-changed
claim both verify; only the coverage claim was wrong. All 12 are pinned in
this closing pass, and the census is now driven rather than counted by hand:
`git init` call sites 58, unpinned 0. The standing lesson is the shape of
the miss — a sweep counted by reading is a sweep whose gaps are invisible to
the reader who did the counting.

**And the mechanism gained the assertion it was missing** (ROUND-SOL
MINOR-15): five test modules rely on bootstrap's shipped `* text=auto
eol=lf` for CRLF-safety and nothing pinned that line —
`test_bootstrap.py::test_scaffold_pins_hook_line_endings` now asserts the
global default beside the per-hook rules. This does NOT reverse the ruling
above: the `.gitattributes` remedy stays rejected for the FIXTURE layer,
where the config pin is the correct mechanism; what is asserted is the
shipped scaffold's own contract, which those fixtures depend on.

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

(2026-08-19, repo-review triage: the 2026-08-19 repository review's M-17 —
archived at `docs/archive/repo-review-2026-08-19.md` — independently reached
this row's exact scope, 28 sites and the five `git_repo` clones. No scope
change; noted so the review's finding resolves here.)
