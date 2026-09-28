# ADJUDICATE — WI-683 — first approval at 1d84d77c

Independent adjudication of the five spine rows WI-679 authored or re-authored
`Drafted` that the `human_approval_through = "DevStg-Boundary"` dial releases
to an adjudication session: SR-220 (batch B's return, re-authored to one
`shall`), LLR-264, LLR-265, TC-260 and TC-261. The one question: is each row
ready to be APPROVED as it stands, or does it go back with findings.
`Approved` blesses the row's TEXT; the harness answers whether its tests
pass, and I ran them anyway, because a cell describing a test the suite does
not run, or a mechanism no module holds, is not blessable text.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chains of SR-215 and SR-220 in full; anchor
`docs/archive/last_approved` copied at 464dc7ac). Every row was read upward
(its parent SR and the need that SR cites), sideways (the approved siblings in
the brief) and downward (its test cases, each evidence pointer resolved by
file and function name; each named code symbol located in the module its
`module` cell names). Disclosure: I read WI-683's queued spec for its Context,
WI-681's recorded verdict as the precedent on SR-220 and LLR-210, and the
spine-authoring skill for rule (c); the arbitration file (rulings 5 to 9) was
context for why, never evidence. HEAD stayed at 1d84d77c throughout; the
worktree was clean before this file was written.

- [APPROVE] SR-220 -> while the queued work items include an overlapping set, the delivered loop content hands that set to a single judgement, at most once per state of the queued work items and never while another judgement is in progress, queued over an item of the set or queued to run before it, the outcome taking effect only as a recorded restructuring in which each absorbed item is closed terminal naming its one successor with its scope text unchanged; the acceptance fixes one judgement row per state including after the judgement closed, the four named refusals and the one that holds nothing back, a judgement never a member, no seeding by and no re-absorption of an item an enacting judgement created while an item of a non-enacting judgement or a hand consolidation is not read as judged, the not-queued refusal by name, and the terminal absorbed items with their successor's record -> a labelled DERIVED requirement under SN-025, judged by the skill's rule (c): (i) recorded where something reads it, `Hat-Refs` UNATTENDED-OPS and PERFORMANCE, both roster names whose `listens_for` names a failure this row prevents (an unbounded retry that pages nobody; an operating-cost risk left unassessed), and SN-025 carries the `unattended`/`loop` tags that reach UNATTENDED-OPS; (ii) the rationale argues both lenses and says why the need's text alone yields work selection only; (iii) fed back upward: the rationale states the sentence SN-025's acceptance could carry, and this verdict's recommendation section carries it to the owner. Sideways, SR-148 keeps work selection and SR-157 the overlap warning, and the row says so; downward, LLR-210 (re-attested in WI-682) decomposes every acceptance clause including the four refusals, the enacted-absorption test and the population, and TC-208 plus TC-254 split the in-memory decisions from the repository act -> ready: batch B's one return is answered — the Requirement now carries one `shall` under a `While` opening, the enactment folded into the same obligation as "whose outcome takes effect only as ..." — and `trace.py --strict` on the flipped tree raises no requirement-form finding on it (driven; only the expected never-rode-a-copy findings the act clears). Boundary-Refs B-01;B-10 and DA-Refs DA-015 resolve (traced cells, WI-696's amendment, not this act's to judge).
- [APPROVE] LLR-264 -> `intake.py consolidate` runs `consolidate.census_draft` over the checkout's registry; when the census proposes nothing it prints the reason on stdout and exits 0; otherwise it prints the candidate set, its Digests pair and each pre-filter finding, mints the one row through `_mint` as one bookkeeping commit and exits 0; a mint refusal prints on stderr and exits 1; `--dry-run` prints the same census and mints nothing -> SR-220 asks that the set be handed to a single judgement, and the dispatcher's idle arm was the only caller, discarding the reason; the rationale says what breaks without the row (a person or a non-loop adopter had no command and the census was bypassed) and which alternative lost (a snippet reaching into the mint). Every clause is true of `intake._cmd_consolidate`: `census_draft` returns `(draft, reason)`, the reason is `_say`'d at exit 0, the `> ` finding lines and the digests pair are printed, `_mint` is the one allocator, and `_cli_result` sends a refusal to stderr with 1; `--dry-run` returns before the mint. Component CMP-008 is the loop's, where LLR-210 sits; TC-260 drives every clause -> ready.
- [APPROVE] LLR-265 -> `intake.py sweep --before --after --branch --merged` runs `intake_after_merge` with an outcomes map holding exactly the named rows, each read from the one terminal folder holding its spec, so the closes' dispositions, spot checks and a merged adjudication's drafted follow-ups are minted for those rows and no others, beside the range's diff triggers and the merge checkpoint's re-judge drafts at `--after`; `--merged` refuses without both range ends, a zero-length range or no `--branch`; the branch is the claim identity the Done-when check reads, a row with no claim under it named on stderr with why the arm did not run; a row in no or two terminal folders refuses the whole sweep; `--merged` and `--with-terminal` are mutually exclusive; range and bare shapes unchanged; idempotent by exact-title dedup -> SR-215's `When a work item merges` checkpoint is the obligation a hand merge skipped, and the row's own decision is the outcomes map such a merge never built; the other rows the sweep mints are the intake's standing arms (`intake_after_merge`, LLR-255's) restated, not new obligations. Every clause is true of `_cmd_sweep`, `_sweep_outcomes`, `_merged_shape_refusal`, `merged_outcomes` and `_done_when_drafts` ("NEVER SILENT WHEN IT WAS ASKED TO LOOK"), and the parser puts `--merged` and `--with-terminal` in one mutually exclusive group; wave-5 rulings 5 and 8 are answered in the text; TC-261 drives every clause -> ready. Noted, not returned: the row's `SR-Refs` names SR-215 alone while its Detail also names the disposition, spot-check and first-approval arms, which belong to the intake rows those SRs own; the row decides only which closes the hand merge owes, which is SR-215's checkpoint applied outside the slot.
- [APPROVE] TC-260 -> through intake's command line on a real repository: a two-row queue sharing a spec, `--dry-run` printing both ids and the shared-spec finding with no commit; the mint of one queued consolidate row whose Adjudicates names both, the digests pair printed as the Digests cell records, a second run refusing by name with no commit; a disjoint queue printing the no-overlap reason; each exit 0; an uncommitted edit to a path the mint must write exiting 1 with the `intake: ` reason on stderr naming the path and no commit -> four named pointers in `tests/test_intake.py`, each resolving by function name and passing in the slow batch; every LLR-264 clause has an arm (ruling 8); Tier Full is true, `test_intake` is in `SLOW_MODULES`; IF-243 exists -> ready.
- [APPROVE] TC-261 -> through intake's command line on real repositories: a range with two early closes only one of which the merge landed, the sweep naming that one minting the amendment row and that disposition alone and a re-run minting nothing; a hand merge handing over a Drafted row, a claimed row with its Done-when reworded, a sampled clean row and an adjudication row drafting a follow-up, naming the three with the branch minting the first-approval row, the spot check of the closed sampled row and not of the one on file, the drafted follow-up and the Done-when adjudication, and naming on stderr the clean row the branch never claimed; a branch holding no claim minting no Done-when row and printing one stderr line; two-folder and no-folder rows exiting 1 moving no commit; a missing range end, a zero-length range and a missing branch each exiting 1; `--merged` with the terminal scan refused by the parser; a merge changing an observation case's declared input minting one re-judge row and a re-run minting none; the range shape judging no close and the bare sweep judging the folders -> ten named pointers in `tests/test_intake.py`, each resolving and passing in the slow batch; the Done-when arm is driven in both branches (ruling 5); Tier Full is true; IF-244 exists -> ready.

## How the chain and the anchor were read

- Upward: SR-215 and SR-220 as the brief printed them and as the live file
  holds them; SN-025 from `docs/requirements/stakeholder-needs.toml`; the hats
  roster through `python scripts/hats.py list` for both names in SR-220's
  `Hat-Refs`. Sideways: LLR-210, LLR-254, LLR-255, TC-208, TC-247, TC-248 and
  TC-254 as approved siblings. Downward: every evidence pointer of TC-260 and
  TC-261 resolved by file and test function; every named code symbol of
  LLR-264 and LLR-265 located in `intake.py`.
- Anchor: `docs/archive/last_approved` at 464dc7ac holds SR-220 at `Drafted`
  (batch B's return) and none of the other four, so nothing here is a
  re-attest; the act names the three registries that hold at least one
  approved row.
- SR-220 appears in WI-696's brief as well; it is ruled once, on its text at
  HEAD, and WI-696 carries the same line.

Bar I produced (not claimed), on this tree with `python -m pytest -q -n 4 -p
no:cacheprovider`: `tests/test_intake.py` in the slow batch (eight modules):
**372 passed, 1 skipped in 195.57s** (the skip is `test_dogfood_sync.py:189`,
an empty parameter set, unrelated); `tests/test_consolidate.py` in the fast
batch (fourteen modules): **448 passed, 1 skipped in 16.80s**. No failures,
no errors. The flipped tree (every batch-C approval moved to `Approved`) was
driven through `trace.py --root . --strict` and `--strict-integrity`: the
only findings are the 35 "reads Status=Approved but is ABSENT from / reads
Drafted in the snapshot" lines the act's copy clears; `check_trajectory.py
--strict` is clean.

## The derived requirement: recommendation to the owner

SR-220 passes rule (c) as written, and the recommendation does not change the
verdict. **Keep it derived; widen SN-025's acceptance anyway**, as batch B
advised: the loop mints work one finding at a time, so an overlapping queue is
its ordinary state and SN-025's "no human curating what comes next" is broken
the moment a person has to merge duplicates. Adding the rationale's own
sentence, "the loop keeps its own queue free of duplicated work", to SN-025's
acceptance lets a blind re-derivation yield the row and the label then comes
off at the next amendment; the once-per-state bound and the strong-tier cost
stay in the rationale as the two lenses' reasons.

## Dispositions

None owed: every row is approved. The act (flip plus scoped snapshot) is
batch C's one shared act; its status is recorded in the coordinator's report
and the act's own commit, not here.

## Non-blocking findings (surfaced, not acted on)

1. **LLR-265 cites SR-215 alone** while describing the sweep's disposition,
   spot-check and first-approval arms; those arms are the intake's and are
   owned by the rows under their own SRs. If a later reader wants the hand
   merge traced to those SRs too, that is a traced-cell re-point.
2. **`check_trajectory` warns that WI-696 and WI-702 share a spec of record
   and near-identical titles** — the ordinary shape of two adjudication rows
   minted over one registry, not one job minted twice.

## Second sitting note, 2026-09-28 — the act narrowed under wave-5 ruling 38

The verdict above stands unchanged: SR-220 is APPROVE on its text. The act
batch C re-takes copies the LLR and TC registries only, so SR-220's flip and
copy are not in it and the row stays `Drafted` until an act copying the SR
registry takes this verdict up; LLR-264, LLR-265, TC-260 and TC-261 are
flipped and anchored by the narrowed act.

OUTCOME: APPROVE rows=5
