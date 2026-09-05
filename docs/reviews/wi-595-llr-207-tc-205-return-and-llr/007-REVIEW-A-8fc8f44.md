# REVIEW-A (007) — WI-595 `LLR-207/TC-205 return and LLR-208/TC-206 amendment`

Reviewed rev `8fc8f441`, scope `git diff contract_split...HEAD` less telemetry,
verdict records and generated artifacts. Independent context; the implementer's
session notes and self-assessment were not read.

## Instruments run (once each, summary quoted)

`python project-trajectory/scripts/check.py --jobs 0` — exit 0:

```
Check summary (stage DevStg-Tests, tier all):
  PASS  registry-integrity 3.1s
  SKIP  derived-stage    work branch 'wi-595-…' — generated freshness is the trunk lane's
  PASS  vocabulary / need-form / privacy / doc-navigability / design-flows
  PASS  trajectory       4.9s
  SKIP  approval-fresh   work branch … / SKIP verdict-rollup   work branch …
  PASS  skills-index / prompt-catalog / staged-divergence / approval-immutable
RESULT: PASS
```

`python project-trajectory/scripts/trace.py --strict-integrity` — final line:

```
Traceability: SN=27 SR=76 LLR=191 TC=190 orphans=0 integrity=0 verified-mechanized=72
verified-demonstrated=3 verified-attested=0 drafts=11 budgets=4 budget-findings=0
components=4 component-findings=0 interfaces=164 interface-findings=0
paraphrase-advisories=3. Report -> docs/test/report.md
```

`python -m pytest -q tests/test_verdict_record.py` at the tip — `59 passed in 57.11s`.

## Worst failure classes this change admits, hunted first

1. **Fail-open at the peel** — the changed function decides which commits escape
   the verdict gate; anything it admits is work no reviewer judged. Driven.
2. **A regression test that pins nothing** — the round-1/round-2 remedies are
   recorded as measured facts in a `Drafted` cell about to be adjudicated. Driven.
3. **Fail-closed regression on real closes** — the new derivation could stop
   admitting genuine closes. Driven: `mechanical_close_attestation` was run
   against the nine real historical `adjudicate: … (mechanical close)` commits
   in this repo's history (`41980b2e 49dc0f0a f0528530 6b066486 e2b3cf8a
   c1806388 02a92f22 4d9dba7f 825fc966`) and every one still peels to its parent.
   A three-row close built through the real `integrate._claimed_specs` +
   `station.mechanical_close_subject` writer path also peels, so the new
   writer↔verifier ordering agrees today.

Positive confirmations: `test_a_forged_mechanical_close_middle_does_not_peel`
genuinely fails on the pre-fix module (`8fc8f441^:…/verdict.py` restored in a
probe worktree → `AssertionError: assert '59846fa5…' is None`), so the round-2
regression is a real detector. Every one of TC-205's 51 evidence citations
resolves to an existing `def` in the file it names. The tier basis holds: 3
citations in `test_integrate_admission` + 5 in `test_integrate_station` = 8, both
stems present in `tests/conftest.py` `SLOW_MODULES`.

## Findings

- [MAJOR] project-trajectory/scripts/kitlib/verdict.py:394 -> the `not deleted` clause is DEAD: `branches` is only ever added to inside the same `if active:` arm that appends to `deleted`, so an empty `deleted` always implies an empty `branches` and `len(branches) != 1` on :395 refuses first — measured by deleting the clause in a probe worktree and re-running the module: `59 passed`, IDENTICAL to the tip, with `test_an_empty_close_is_refused_and_the_walk_covers_it_regardless` still green. The round-1 remedy therefore pins nothing, and two records now assert the opposite of the shipped code: tests/test_verdict_record.py:1729 ("the non-empty path set is the only clause that can refuse this one") and docs/test/test-cases.toml:2083 THE EMPTY-PATH REFUSAL ("with the clause deleted … the boundary assertion is the only thing that flips") — both were measured against the pre-round-2 `not paths or` implementation and not re-measured after the pairing rewrite replaced it -> delete the redundant `not deleted` disjunct, and re-word TC-205's empty-path paragraph and the test comment to name the clause that actually refuses an empty close (the one-source-branch requirement), so the cell's measured claim is true of the tree it is about to be approved over -> @owner

- [MAJOR] project-trajectory/scripts/kitlib/verdict.py:377 -> `_closed_wi_ids` inspects only the A/D entries it RECOGNISES and silently ignores every other addition or deletion under `docs/work/`, so a close can carry unreviewed data loss and unreviewed new content past the gate. Driven on a real repo: a commit with the exactly-composed subject `adjudicate: WI-401 -> complete/ (mechanical close)` that moved `active/br/WI-401-x.md` → `complete/` AND deleted the pre-existing terminal record `docs/work/complete/WI-300-terminal.md` AND added a brand-new `docs/work/queued/WI-999-smuggled.md` still peels (`peels -> 4f7ad2f3…`), so the destruction of an archived judged row and the injection of a new spec are both measured at the parent and never judged. `spec_move`'s inbound relink only ever needs `M` entries, so nothing legitimate requires unpaired A/D -> refuse when any `A` or `D` entry under `docs/work/` is not one of the paired move entries (leave `M` unrestricted for the relink); this is validation at the one owning trust boundary the spec itself names — the attestor cannot construct the externally-authored git object it judges, so the antidote skill's "smallest change that makes this fix unnecessary" has no construction available here -> @owner

- [MINOR] project-trajectory/scripts/kitlib/verdict.py:390 -> the rewrite makes the ORDER of the composed WI ids load-bearing across two independently-chosen sortings — `handback.close_adjudication` (project-trajectory/scripts/handback.py:624) composes from `integrate._claimed_specs`' `sorted(Path.glob(...))`, while the attestor re-derives it from `deleted.sort()` over raw path bytes — and no test drives a multi-row close, the only shape where they can disagree. I verified they agree today (three-row probe through both real code paths), but a future change to either sort silently stops every BATCH close from peeling and re-opens the staled-APPROVE failure this mechanism exists to close; batch lanes are real (four rows on one lane, 2026-09-03) -> have `close_adjudication` compose its subject through the SAME canonical-order helper the attestor derives, so the two orders cannot diverge by construction (that is the antidote here — the guard becomes unnecessary rather than tested), and add a two-row close arm to TC-205's evidence either way -> @owner

- [MINOR] docs/archive/work/complete/WI-595-llr-207-tc-205-return-and-llr.md:49 -> the Deliverable's tier basis says "8 of the row's 50 citations"; TC-205's `evidence` now carries 51 (counted by splitting the cell on `;`) after this lane added the forged-middle and empty-close citations — a stale count in the record that justifies the `Smoke` -> `Full` ruling -> restate as 51, or drop the total and keep the "8 in SLOW_MODULES" fact the ruling actually rests on -> @owner

- [MINOR] docs/requirements/interfaces.toml:1080 -> for clarity: `IF-175.notes` still describes `governing_rev` as walking "to reach a refresh it would otherwise hide" — the single-class silence this WI just corrected in `LLR-207.detail`, left standing in a `Drafted` row that TC-205 explicitly `verifies` (`verifies = ['SR-156','LLR-207','IF-175']`), so one adjudication approves two cells that describe the same peel at different widths -> name both disposable classes in the IF-175 sentence (or state that the class list is LLR-207's alone and the seam row speaks only to the two peel SHAPES), so the reader is not left choosing which row is current -> @owner

VERDICT: CHANGES-REQUESTED findings=5
