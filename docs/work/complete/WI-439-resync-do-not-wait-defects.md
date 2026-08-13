+++
id = "WI-439"
title = "OI-27's three do-not-wait defects, taken ahead of the re-sync pack: (1) the tarball adopter path stamps an anchorless `unknown (kit not a git checkout)` silently at exit 0 — add the loud warning the -dirty path already has; (2) the downstream-resync skill's hand-maintained WI-381 recipe duplicates ADOPTING section 6 and has drifted — point, do not restate (through the materializer, never three hand edits); (3) zero tests re-sync from an old kit state — build the first old-kit test: scaffold at an older kit commit, sync forward, harness green. That third test is what makes any re-sync method's claims evidence rather than prose, and it is owed under every option OI-27 weighed."
workstream = "lock-program"
sr_refs = ["SR-036", "SR-111"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 1
+++

## Deliverable

Completed 2026-08-13. (1) The tarball stamp path warns loudly on stderr with
exit unchanged, the `unknown` label now one constant with a one-home pin — and
the adversarial round then found the sharper defect: `git rev-parse` searches
parents, so a tarball extracted inside an unrelated repo stole THAT repo's HEAD
as a false anchor; fixed with a tracked-file probe (the kit is only anchored
when its own files are tracked in the checkout found), pinned by a new
foreign-repo test, and the warning now names all three degraded causes.
(2) The downstream-resync skill points at ADOPTING §6 instead of restating the
WI-keyed recipes, re-materialized through the generator with a pin refusing
WI-keyed recipe content; the round's residual (three undated operational
restatements) is deliberately deferred to WI-447, which replaces that surface.
(3) tests/test_old_kit_resync.py — the first old-kit test: scaffolds from
pinned kit fd5916b9 (2026-07-22, chosen past the vacuous-green line and across
five documented recipes), runs §6's documented add-only steps forward, asserts
substantive green, and PINS the finding that matters: the add-only re-sync
leaves both carriers live and the surviving OLD checkers green a tree the
current kit refuses — SN-008's dishonest green one level up. The review round
added the missing halves: the `--force` overwrite leg (current checkers
installed byte-for-byte; the verdict must be honest green-with-substance or a
loud named refusal, never silence) and `fetch-depth: 0` on all three CI
checkouts, without which the module would have skipped forever in CI while
reading green. Module 6 passed; full suite 2318 passed / 6 skipped on the
branch. The bootstrap module-size ratchet took a documented +26 reviewed bump
(reason at the baseline entry; log entry in this session's record).
