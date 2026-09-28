# ADJUDICATE — WI-716 — first approval at d7e1be0e

Independent adjudication of the three rows WI-618 authored `Drafted`, batch E
returned (WI-712) and WI-715 amended in place: SR-226 (a labelled derived
requirement), LLR-287 and TC-300. The `human_approval_through =
"DevStg-Boundary"` dial releases their rungs to this session, so what is
approved here is approved. The one question: is each row ready to be APPROVED
as it stands. `Approved` blesses the TEXT; whether the cited tests pass is the
harness's answer, produced below, not a cell's.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chain of SR-226 in full; anchor
`docs/archive/last_approved` copied at e7fe487d for the SR registry and
6763d08d for the LLR and TC registries). Batch E's verdict
(`docs/reviews/wi-712-adjudicate-llr-286-llr-287/001-ADJUDICATE-8cd77ea6.md`)
was read as the record of the three findings WI-715 answers, never as evidence
that the answers are true: every amended cell was re-read against the live
registries, the code and the tests at HEAD. The brief does not render the
routed pointer cells, so `SN-Refs`, `Boundary-Refs`, `SR-Refs` and `Verifies`
were read from the registries and are ruled below. The arbitration file
(rulings 47 to 52) was context for why the lane built what it built.

- [APPROVE] SR-226 -> when a spine row is retired, the delivered harness leaves one record found by the retired id, written in the same change that deletes the row, naming the id, the date, the successor if any and the reason, and kept in view by two warn-only reports (a record changed after it landed; a spent id retired since the record began with no record); the acceptance fixes the exact-row deletion, the refusal set with nothing written, survival of the log fold, the two reports and their silences, and the deleting commit read from history or reading unknown -> the three cells batch E returned are answered: `Requirement` now carries ONE `shall` (the two reports are the response's qualifier, not a second obligation; the acceptance criteria and the four children are byte-exact, so the obligation set is unchanged), the `coincident` waiver is gone (the row is honestly unclassified under approved SR-193, the state the SR rung reports without failing; there is no waiver left to test), and `Boundary-Refs` reads `B-01;B-09` — B-01 HOLDS (the same-change write of a registry and a tracked record is the governed write from a session that EXT-001 crosses) and B-09 HOLDS (the record, the Retired tab and the console advisories are what EXT-006 reads); `SN-Refs` SN-010 HOLDS, the nearest stated outcome (references a reader can follow and trust), and rule (c) holds in all three parts: (i) `Hat-Refs` MAINTAINER, whose `listens_for` ("a requirement whose reason lives only in the session that wrote it") is the failure a deleted row's lost reason is, and which applies always; (ii) the rationale argues the lens, states why SN-010's text does not name the outcome, and names the alternatives that lost (the watermark, a forwarding map in the log, a record carrying its own commit); (iii) it feeds back upward in its last sentence. EARS `When` states the trigger; the voice names no file; the rationale carries no citation frame, no history and no vague or open-ended term; `Verification` Test and `Priority` S are true of the chain (LLR-286 and TC-299 approved by batch E, LLR-287 and TC-300 below). Flipped in a scratch tree with the whole batch, `trace.py --strict` raises no form finding on it -> ready.
- [APPROVE] LLR-287 -> `retired_panel(rows, before)` returns None with no record and otherwise the Retired tab and its table (id, date, successor or a dash, reason, deleting commit inside `<code class="retcommit" data-id>`), every cell escaped, under a caption naming lookup, render-time git and the census count when positive; `_retired_view` builds it from `retire.records` and `retire.read_census` as one-element or empty lists that `build_html` extends after the Process tab; `fresh_view(text, unresolved)` is what `--check` compares, the as-of stamp removed and the retcommit elements of `_unresolved(root)`'s ids emptied, every other commit held exactly -> `SR-Refs` SR-226 HOLDS: the parent's acceptance says the deleting commit is read from history when the record is shown and reads unknown where history cannot answer, and this is the one surface that shows it. The one cell WI-715 amended, `Rationale`, now closes the set it names — the checkouts that read unknown are "an uncommitted record, and a record landed by a commit with no parent (a shallow clone's boundary, a squashed history's root)", exactly the cases `retire.records` reads as `unknown` (a parentless landing, `retire.py` 650-651) and TC-300 (a) drives — with no escape phrase; it states the standing system, not its history. The four code symbols resolve at HEAD (`traj_views.retired_panel` 1322; `gen_trajectory.fresh_view` 299, `_unresolved` 316, `_retired_view` 886, `RETCOMMIT_RE` 296), both modules and CMP-009 resolve, `Hat-Refs` is rightly empty (the parent carries MAINTAINER; this design row raises no hat of its own). In the scratch flip the form gate is silent -> ready.
- [APPROVE] TC-300 -> records read from temporary git repositories, a shallow clone included, and the real generator over the shared fixture project: (a) a landed record reads its landing short hash with its four cells, an uncommitted record, a root-commit record and a depth-one clone read unknown, tier-then-number order; (b) no record no tab whatever the census counts, two escaped rows with retcommit elements, a dash and a lookup caption, the census count stated only when positive; (c) the tab only once a record exists, `--check` failing on a fabricated commit or on unknown where history resolves, passing in a depth-one clone of a page rendered with full history, failing on a changed reason -> twelve evidence pointers in `tests/test_retire_dashboard.py`, each resolving by function name; the two cells WI-715 amended hold: `Method` says "the shared fixture project" (no vague term left) and the new `Parameters` cell names `tests/traj_fixtures.py make_repo (re-exported from tests/traj_core_fixtures.py)` and `tests/test_retire_dashboard.py _rendered_history` — both exist at HEAD (`traj_fixtures.py` 39 re-exports `make_repo`; `test_retire_dashboard.py` 183 defines `_rendered_history`, used at 197). `Verifies` HOLDS: SR-226 (the acceptance's last clause), LLR-286 (`records`, arm (a)), LLR-287 (arms (b) and (c)), IF-257 (the record files the readers consume). Expected states the condition; Level Integration is true (real git, the real generator); Tier Full is honest and required — `test_retire_dashboard` is in `tests/conftest.py` `SLOW_MODULES`, so a Smoke tier would have been a finding; Automated Yes. Ran at HEAD: 12 passed. Form gate silent in the scratch flip -> ready.

## How the chain and the anchor were read

- Upward: SN-010 (`need`, `why`, `acceptance`); the MAINTAINER hat's
  `applies_when`, `asks` and `listens_for`; B-01 and B-09 from
  `external.toml`; SR-193 for the coincident test (no waiver remains to
  test). Sideways: LLR-286 and TC-299, approved by batch E, unchanged since.
  Downward: every TC-300 pointer resolved and read; every LLR-287 symbol
  located.
- Routed pointer cells: SR-226 `SN-Refs` HOLD, `Boundary-Refs` B-01 HOLD and
  B-09 HOLD; LLR-287 `SR-Refs` HOLD; TC-300 `Verifies` HOLD on all four ids.
- The form gate: all seventeen rows of batch F were flipped in a scratch tree
  and driven through `trace.py --strict`: no `requirement form` finding on
  any of them (only the expected pre-snapshot approval-record findings), and
  the flips were reverted before the act.
- Anchor: none of the three rows is `Approved` in the copies at e7fe487d /
  6763d08d, so nothing here is a re-attest of a returned row's text. The act
  for this batch (one snapshot with WI-718's approvals and WI-717's
  re-attestations) names all three registries.
- Advisory left standing, not a finding: `trace.py` reports SR-226 "declares
  no Form" — no SR in the registry declares one.

## Bar I produced (not claimed)

`python -m pytest -q -n 4 tests/test_session_adapters.py
tests/test_session_service.py tests/test_session_keep.py
tests/test_retire_dashboard.py
tests/test_agent_loop.py::test_session_log_redacts_credential_shapes
tests/test_agent_loop.py::test_session_log_redacts_credential_shapes_in_header_values
-p no:cacheprovider`: **117 passed in 72.92s** (21 + 34 + 48 + 12 + 2), no
failures. `python project-trajectory/scripts/trace.py --root . --strict` at
d7e1be0e: rc 0, orphans=0 integrity=0.

OUTCOME: APPROVE rows=3
