# ADJUDICATE — WI-694 — first approval at 1d84d77c

Independent adjudication of the ten spine rows WI-651 authored `Drafted` that
the `human_approval_through = "DevStg-Boundary"` dial releases to an
adjudication session: five design rows (LLR-271, LLR-272, LLR-273, LLR-277,
LLR-278) and five test cases (TC-269, TC-270, TC-271, TC-272, TC-278). The one
question: is each row ready to be APPROVED as it stands, or does it go back
with findings. `Approved` blesses the row's TEXT; I ran the tests anyway.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chains of SR-146, SR-147, SR-157 and SR-178
in full, LLR-274, TC-273 and TC-275 shown as another adjudication's rows;
anchor `docs/archive/last_approved` copied at 464dc7ac). Every row was read
upward, sideways and downward; every evidence pointer resolved by file and
function name; every named code symbol located in its module; every Tier cell
checked against `tests/conftest.py` `SLOW_MODULES` loaded in process.
Disclosure: I read WI-694's queued spec for its Context, WI-681's verdict for
the Smoke-tier precedent (TC-204), and the arbitration file (rulings 17 to
25) as context for why, never evidence. HEAD stayed at 1d84d77c throughout;
the worktree was clean before this file was written.

- [APPROVE] LLR-271 -> `NEED_TIERS` names the needs file's need and stakeholder tiers and `SNAPSHOT_TIERS` lists both, so every compared-tier reader walks them; `load_all` reads both off the record under the live column names; `owing_rows` is the one owing rule (Drafted, no Status cell, or approved cells moved, with before and after) read by the need and assumption sections; `needs_owing` runs it over `NEED_TIERS`; `trace.need_brief_lines` renders one block per owing row outside any collapsed block and keeps the freshness window open; `_approved_by_act` counts the need tiers so the act ledger names a need or stakeholder it approves -> SR-178 holds a stakeholder need to the same drift rule, and this row is the need tiers' half of that rule beside LLR-158 (the basis) and LLR-173 (the record); every clause is true of `baseline_snapshot.NEED_TIERS`, `SNAPSHOT_TIERS`, `owing_rows`, `needs_owing`, `_approved_by_act` and `trace.need_brief_lines` (called at line 4747, before the `_waiting_lines` block at 4771); the rationale argues the failure without the row and the one-rule choice; TC-269 drives every clause; ruling 20's split leaves it one decision -> ready.
- [APPROVE] TC-269 -> on bootstrapped scaffolds: an approved need recorded by a seed owing nothing, then drifted after its need cell is amended with Status left Approved, reported naming the cell and briefed with the cell before and after; an approved stakeholder amended, reported and briefed the same way; a Drafted stakeholder approved in an act naming the needs registry, named in the act ledger's newest entry; through the scaffold's snapshot command, an act refused while an approved need moved, naming the need and the cell, and re-attesting it re-anchoring it with the copy equal to the live file -> four named pointers in `tests/test_snapshot_readers.py`, resolving and green (slow batch); Tier Full is true, the module is slow -> ready.
- [APPROVE] LLR-272 -> `kitlib.spine.missing_cell_findings(tiers)` returns one line per row missing its Status cell on any of the four tiers, and per SR/LLR/TC row missing its Phase once any of those rows is phased, skipping `-000` and id-less rows; `trace.integrity_sweep` appends them so they fail `--strict-integrity` at every stage; `trace._owes_first` reads a row with no Status cell as owing a first approval and `reattest_model` uses it wherever it tested Drafted; `baseline_snapshot.owing_rows` does the same -> SR-157's acceptance says a rule added at a declaration site is in its scope by default and this is such a rule, integrity-class because it is wrong at any stage (the rationale says why the schema tier would not do); every clause is true of `missing_cell_findings` (`PHASED_TIERS`, the `phased` arming), `integrity_sweep` (line 5441), `_owes_first` and `owing_rows`; TC-270 drives it -> ready.
- [APPROVE] TC-270 -> on a scaffold: one requirement phased, a test case with neither status nor phase, a need with no status: the strict integrity run failing with exactly three findings naming the two cells and the need's Status, none for the requirement; the re-attestation brief rendering the requirement's chain with the test case and the need's block labelled as having no Status cell; passing once the cells are written; in memory, one finding per tier and cell, and none for Phase once no row is phased -> two named pointers in `tests/test_snapshot_readers.py`, resolving and green; Tier Full is true; ruling 21's parametrization is in the second pointer -> ready.
- [APPROVE] LLR-273 -> `baseline_snapshot.registry_stamps(root)` returns (registry, short rev, date) per registry the record holds a committed copy of, from `stamp(root, registry)`; the re-attestation brief's baseline lines name each copy and its commit with the derived-stamp prefix; the open-items view lists the same pairs; `reattest_model` entries carry `baselines` (`_spine_stamps`) with `baseline` the requirement registry's; the off-spine census counts since each registry's own copy; the first-approval and amendment briefs' anchor names the commit of each registry the act copies -> SR-178 and SR-146 (the judge's brief is LLR-167's, under SR-146) both want the provenance of the text a reader is measured against, and the rationale states the failure without the row (one directory-wide stamp standing for every copy); every clause is true of `registry_stamps`, `trace._baseline_lines`, `trace._spine_stamps`, `gen_open_items` (line 863) and `adjudicate_brief._copy_stamp_lines` — and the brief I was handed carries exactly those per-registry lines; ruling 20's split leaves it one decision (the scope check went to LLR-278) -> ready.
- [APPROVE] TC-271 -> on real repositories: a record seeded at one commit whose test-case copy alone is re-written later, the directory-wide stamp naming the later commit: the re-attestation brief naming the requirement and design copies with the seeding commit and the test-case copy with the later one, the open-items view listing the same pairs, the model's entry carrying each spine registry's own stamp; the first-approval brief's anchor naming the design registry it copies with the seeding commit alone -> two named pointers, one in `tests/test_snapshot_readers.py` and one in `tests/test_adjudicate_brief.py`, both resolving and green; Tier Full is true, both modules are slow; IF-126 exists and this case is what cites it (TC-167's amended Expected, WI-693, says so) -> ready.
- [APPROVE] LLR-277 -> `spine_carrier.needs_from_text(text, carrier)` reads `.toml` text as its need tables only and `.md` text as the legacy tables, raising on a `.toml` that does not parse or on a carrier the tier lacks; `needs_or_refuse(path, text)` takes the carrier from the suffix and refuses naming the file; the README floor, the approval view's need prose and `baseline_snapshot._needs_at` read through them; `load_need_tier(path, id_col)` is the one need-tier row loader, TOML through `load`, markdown as SN-ID rows under today's column names with status off the section and no stakeholders; `_tier_rows` reads every `NEED_TIERS` tier through it on both sides; `_copy_file` finds the needs registry or its copy under either carrier -> SR-147 holds every spine tier in one machine-parseable representation and LLR-166 is its one reader with the dual-home refusal; this row is that reader's rule for the one tier with two carriers (ruling 19), and the rationale names the two failures without it (sniffing; the shared loader knowing TOML and CSV alone); every clause is true of `needs_from_text`, `needs_or_refuse`, `load_need_tier`, `_needs_at` (line 1900), `_tier_rows`, `_copy_file`, `check_docs.py:582` and `trace.py:3498`; Component CMP-006 -> ready; its test case is returned below, which leaves the row's chain incomplete until that case is re-authored, a state the derived stage reports rather than a defect in this text.
- [RETURN] TC-272 -> in memory and over real repositories: under the TOML carrier a comment-only text, a table row inside a stakeholder's description string and an empty text yielding no need while the markdown carrier reads the string text's row; an unparseable TOML text and an unknown carrier raising, the refusing reader naming the file; the README floor and the approval view reading no need from a TOML file declaring none and the floor refusing an unparseable one; the record's history reader reading no need at a commit whose needs file declares none and refusing one that does not parse, naming the commit and the file; a markdown-needs scaffold recording its approved need, reporting it drifted once amended, refusing an act until re-attested, and reporting nothing unanchored -> five named pointers, all resolving and green: three in `tests/test_spine_carrier.py` (fast) and two in `tests/test_snapshot_readers.py`, a `SLOW_MODULES` member; LLR-277's every clause has an arm -> not ready as it stands: `tier = "Smoke"` while two of its five pointers (`test_the_snapshot_history_reader_takes_the_needs_carrier_from_the_file`, `test_a_markdown_needs_file_is_compared_like_a_toml_one`) sit in a slow module, so the Method's history-reader and markdown-scaffold arms do not run in the per-commit tier the cell claims. This is the assignment's rule and batch B's TC-204 return applied to the same fact. The remedy is the split TC-204 took (a Full case carrying the two repository arms and their sentence, this case keeping the three in-memory arms) or re-tiering the whole case to Full; every other cell stands, and the row's spec carries the draft.
- [APPROVE] LLR-278 -> `acceptance_record.merge_approval_refusal` calls `reattest_scope_refusal` first for an adjudication lane, acting only when the delta wrote the act ledger; `reattested_between` reads the ledger at base and head and takes the ids re-attested by the entries the base lacks, refusing by name when either side does not parse; every such id outside `amendment_scope` (the union of the claimed amendment rows' `Adjudicates`, empty when none is claimed) is refused by name before the first-approval judgement; a mixed act merges when each half lies inside the scope of the row claiming it -> SR-178's rule is only as good as the record it reports against, and the rationale states the hole without the row (a re-attestation moves no cell, so the flip-based scope check could not see it) and the one record that makes it checkable; every clause is true of `merge_approval_refusal` (line 796), `reattest_scope_refusal`, `reattested_between` and `amendment_scope`; TC-278 drives all four arms; this batch's own act (four amendment rows and five first-approval rows claimed together) is the mixed shape the row admits -> ready.
- [APPROVE] TC-278 -> on scaffold-made repositories: an adjudication lane claiming an amendment row scoped to one requirement whose act re-attests two, refused naming the one outside; the same act re-attesting only the scoped row merging; the same act claimed by a first-approval row refused naming the row; one act approving a Drafted requirement and re-attesting an amended one under a first-approval row and an amendment row each scoped to its half merging, and the same act with the amendment row scoped elsewhere refused naming the re-attested row -> four named pointers in `tests/test_snapshot_readers.py`, resolving and green; Tier Full is true; IF-091 exists -> ready.

## How the chain and the anchor were read

- Upward: SR-146, SR-147, SR-157 and SR-178 as the brief printed them (SR-178
  as amended by WI-651, judged in WI-693). Sideways: LLR-158, LLR-162 to
  LLR-167, LLR-165, LLR-166, LLR-260 and their cases as approved siblings;
  LLR-274, TC-273 and TC-275 as WI-691's rows, read and left byte-exact.
  Downward: every pointer of the five cases resolved by test function; every
  symbol of the five design rows located.
- Anchor: the record at 464dc7ac holds none of the ten, so nothing here is a
  re-attest; the act names the LLR and TC registries.
- The flipped tree was driven through `trace.py --root . --strict` and
  `--strict-integrity`: no form or provenance finding on any of the ten;
  only the expected never-rode-a-copy findings the act clears.

Bar I produced (not claimed), on this tree with `python -m pytest -q -n 4 -p
no:cacheprovider`: the slow batch (`tests/test_snapshot_readers.py`,
`tests/test_adjudicate_brief.py`, `tests/test_baseline_snapshot.py`,
`tests/test_intake.py`, `tests/test_mapping_purpose_cli.py`,
`tests/test_check_complexity_cli.py`, `tests/test_skills_sync.py`,
`tests/test_dogfood_sync.py`): **372 passed, 1 skipped in 195.57s** (the
skip is `test_dogfood_sync.py:189`, an empty parameter set, unrelated); the
fast batch (`tests/test_spine_carrier.py` among fourteen modules): **448
passed, 1 skipped in 16.80s**. No failures, no errors.

## Dispositions

One row is returned (TC-272) with every cell byte-exact; the follow-up is
drafted in `docs/work/queued/WI-694-adjudicate-llr-271-llr-272.md` under
`## Dispositions` as one fenced TOML block, and intake mints it at this row's
merge or the coordinator folds it into an open item.

## Non-blocking findings (surfaced, not acted on)

1. **LLR-277 is approved with its only test case returned**, so its chain
   reads incomplete until TC-272 is split or re-tiered; the derived stage
   carries that, and the approval of the design text does not depend on it.
2. **LLR-273's `SR-Refs` names SR-146** for the judge's brief; the tie runs
   through LLR-167 (the brief composer, under SR-146) rather than through
   SR-146's own prompt-file text. Honest, but a reader may look for it.

OUTCOME: RETURN rows=10
