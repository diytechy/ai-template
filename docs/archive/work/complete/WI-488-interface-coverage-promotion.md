+++
id = "WI-488"
title = "Promote interface contract-test coverage to an ERROR from DevStg-Tests onward, with a migration allowlist seeded at the measured 115 and a declared burn-down expectation (OI-43 ruled (a), 2026-08-20)"
specref = ""
workstream = "process"
sr_refs = []
needs = ["~WI-469", "~WI-455"]
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Deliverable

Executed in full: the promotion, the migration allowlist, and the burn-down
expectation, sequenced behind WI-469 (closed) and the wi455 lane's landed
crossing-half, per the spec's own sequencing clause.

**The promotion.** `check_trajectory.py` gains a new function,
`if_tc_coverage_findings` — an IF seam cited by no TC and NOT on the migration
allowlist is WARN plain, ERROR under `--strict`, wired through `main()` the
same way `component_findings`/`spec_interface_findings` already are (so
`check.py`'s existing gate-conditional `--strict` — passed from `DevStg-Tests`
on, per its own unmodified logic — carries the promotion for free; nothing in
`check.py` itself needed to change). `interface_findings`' own "cited by no
TC" line is UNCHANGED and stays warn-first forever, reporting the total
(allowlisted seams included), so the whole debt stays visible even once the
actionable subset goes quiet. A companion `if_tc_allow_hygiene_findings`
reports (never blocks, not even under `--strict`) an allowlist entry that has
gone stale — its seam gained a TC, or its id no longer resolves — so the
burn-down is visible rather than silently absorbed. Both new functions share
`interface_findings`' `[checks] interfaces_check` opt-out AND its ≤1-module
arch-map vacuity, so the promotion arms on no MORE than the warn it promotes —
a `files`-mode or single-module adopter who never saw the warn does not
suddenly see the error (caught in review before landing: the first draft
skipped this gate and would have widened scope, not just severity).

**The allowlist.** `docs/if-tc-coverage-allow`, a new file (not a kit-shipped
template — like `docs/provenance-allow`, it is absent-tolerant and each
adopting repo seeds its own once the promotion starts to bite). Seeded with
**120** ids, one per line, with a header stating the basis (command,
revision, date) and the burn-down expectation. **Re-measured figure vs the
ruling's 115:** the ruling's own text anticipated this ("record both figures
if they differ") — the tree moved between the 2026-08-19 measurement and this
row's execution: WI-455 minted IF-134/135, WI-390 minted IF-136/137 and
declared IF-055/080/081 (existed but declared no script), WI-483 re-pointed
IF-093 — none of the five new/re-declared seams carry a TC. 130 live IF rows
today (was 125 at the ruling), 120 uncited (was 115). The ruling's INTENT —
seed at the measured uncovered population — governs over the stale number.

**Verified on a real scaffold, not just this repo** (bootstrapped via
`bootstrap.py`, a two-module fixture with one uncited seam):
`check.py --stage-cleared DevStg-Reqs --run-step trajectory` runs
`check_trajectory.py` with NO `--strict` (WARN only, PASS, exit 0);
`--stage-cleared DevStg-Tests --run-step trajectory` runs it WITH `--strict`
(the uncited, unallowlisted seam ERRORs, FAIL, exit 1); seeding the
scaffold's own `docs/if-tc-coverage-allow` with that one id turns the same
DevStg-Tests run green again. Confirms the ruling's own framing exactly: "This
repo is at DevStg-Reqs today, so a DevStg-Tests promotion bites nobody until
the bar rises" — demonstrated, not assumed, and reproduced on this repo's own
tree (`check_trajectory.py --root . --strict` is clean, exit 0, with the
seeded allowlist; removing one entry reproduces the ERROR).

**Deliberately deferred, recorded rather than executed: no spine row claims
the new mechanism.** `LLR-042` (`SR-159`), the design row `interface_findings`
already cites, is `Approved` and its `detail` says the connectivity layer
emits its findings "without changing exit status" — still TRUE of
`interface_findings`, which this row does not touch, and would be FALSE if
cited from `if_tc_coverage_findings`. Amending an Approved cell overrides
attestation (the SR-006/LLR-060 precedent, WI-473, same session). Minting a
fresh Drafted LLR under `SR-159` was considered and declined: `SR-159` is
phase 1 (currently `DevStg-Tests`), and a Drafted child would drag that
phase's derived bar down as a side effect of unrelated work — the WI-448
lesson, hit again. **Recommendation for the owner:** either rule that a
Drafted LLR under `SR-159` may land accepting the phase-1 drop (the
content-correct parent), or find/ground a more suitable existing design row;
until then the built behaviour is ahead of its requirement, honestly
unclaimed rather than falsely claimed.

**Docs.** `PROCESS_OPTIONS.md`'s "Intra-repo interfaces & the architecture
graph" section splits the now-inaccurate "all warn-first" claim into the two
true halves (the two warns that stay forever, and the one that promotes) and
states the allowlist + burn-down. `RESYNC_PACK.md` §3 gains an entry telling
an adopter what changes, what they may notice on their first DevStg-Tests run
after re-sync, and that seeding their own allowlist is theirs to do (the
`docs/provenance-allow` / product-floor entries' shape). `PROCESS.md`'s and
`README.md`'s "every interface is backed by a contract/fixture test" claim is
UNCHANGED, per the spec — the promotion is what makes it true, not a rewording.

**Two ratchets re-stamped, both reviewed bumps with reasons in place** (module
size `check_trajectory.py` 4,096 → 4,295, complexity `check_trajectory.py:main`
22 → 24) — see Gates in the session log for the full account and the
line-ending catch on `tests/test_complexity_ratchet.py` (pre-existing CRLF
residue, normalized before staging).

## Context

Executes OI-43's ruling — (a) as recommended. The measured population:
`check_trajectory.py --strict` reports 115 of 125 IF seams cited by no TC
(verified 2026-08-19); the coverage class is deliberately warn-only at every
bar today (`PROCESS_OPTIONS.md` ~:2177-2188, `check_trajectory.py`
~:1014-1017) — this row is the ruled reversal of that posture at one bar.

- **The promotion:** a seam with no citing TC becomes an ERROR when the
  cleared bar is DevStg-Tests or above; below that bar the class stays
  warn-only. This repo is at DevStg-Reqs today, so the promotion bites
  nobody here until the bar rises — which is the point of adopting it now.
- **The allowlist:** seeded with the current 115 seams, each entry a declared
  exemption with the standing never-green-by-list-edit rule in force —
  adding an entry to clear a NEW seam's finding is accepting what it
  measures, and the list carries a declared burn-down expectation rather
  than living as a permanent exemption surface.
- **The prose stays:** `PROCESS.md`'s and `README.md`'s "every interface is
  backed by a contract/fixture test" claim is NOT softened — the promotion
  is what makes it true. (WI-477's docs sweep deliberately does not touch
  this claim.)
- **Sequencing (the soft edges):** the wi455 lane holds the 49
  provenance-held Contract cells and WI-469 re-authors the 27 file-as-
  endpoint Consumes rows — tests written against cells about to be
  re-authored pin the wrong thing, so this lands BEHIND both. Downstream:
  the promotion ships to every adopter at the same bar — RESYNC entry owed.
