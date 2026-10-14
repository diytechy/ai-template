# What `contract_split` holds that this branch never received

**Status: ANSWERED** (§5; questions 1–5 on 2026-10-13, question 6 on 2026-10-14). This report recovers nothing and mints
nothing. It records what the divergence lost, so that a review sitting can
decide what to bring back and under which new IDs. It was written 2026-10-13
on `refactor_again` at `bf45bd35`. Later the same day, §4 gained what this
branch built under group 3 since the split, and the ruling's surviving text
was located.

<!-- fig: cmd="python docs/plans/2026-10-13-contract-split-divergence-census.py --base 607cf609 --lost contract_split --here bf45bd35" rev=bf45bd35 -->
Every count and table below comes from that one read-only command, using the
census script
[`2026-10-13-contract-split-divergence-census.py`](2026-10-13-contract-split-divergence-census.py)
in this folder. The meaning of each row (§4) was read by hand from the
field-level diffs.

## 1. The divergence

- **Common ancestor:** `607cf609` (2026-09-06, "docs: Refresh redesign status
  and add a session handoff").
- **`contract_split` after it:** 110 commits, 2026-09-06 to 2026-09-07, ending
  at `961f9e47` ("adjudicate: WI-623 primary publication"). `origin/contract_split`
  is the same commit, so nothing exists only locally.
- **This branch after it:** its own history resumes on 2026-09-20.
- **Recovered so far: nothing.** `git cherry` finds none of the 110 commits
  patch-equivalent here, and no merge from `contract_split` exists. No document
  on this branch cites the 2026-09-07 handoff or the `primary_*` mechanism.
  The divergence reads as accidental, not as a recorded decision to drop the
  work.
- **Size:** 504 files, +94,025 / −3,393 lines. Most of that is records
  (`docs/reviews/` alone is 282 files); the parts that govern behavior are §2
  to §4.

## 2. Code that does not exist here

About 2,000 lines of kit code and 2,200 lines of tests, all from the "primary
adjudication" mechanism. In it, adjudication runs as an in-process turn in the
primary checkout under the station lock and publishes through one verified
commit.

| Lines | File |
|---:|---|
| 844 | `project-trajectory/scripts/primary_approval.py` |
| 348 | `project-trajectory/scripts/primary_close.py` |
| 348 | `project-trajectory/scripts/primary_publication.py` |
| 174 | `project-trajectory/scripts/primary_turn.py` |
| 143 | `project-trajectory/scripts/primary_adjudication.py` |
| 115 | `project-trajectory/scripts/publication_verify.py` |
| 60 | `project-trajectory/scripts/kitlib/adjudication.py` |
| 133 | `project-trajectory/prompts/primary-adjudication.template.md` |
| 738 | `tests/test_primary_approval.py` |
| 686 | `tests/test_primary_publication.py` |
| 423 | `tests/test_primary_session.py` |
| 163 | `tests/test_primary_adjudication.py` |
| 134 | `tests/test_implementation_spine_boundary.py` |
| 51 | `tests/test_kitlib_git.py` |

The branch also edited 61 files that exist here (+6,747 / −2,045 lines under
`project-trajectory/` and `tests/`), including `agent_loop`, `dispatch`,
`handback`, `integrate`, `intake`, `consolidate`, `spec_move`, `kitlib/verdict`,
`kitlib/git`, `PROCESS.md` and four skills. This branch has since rewritten
many of those files, so the edits would not apply cleanly.

## 3. ID collisions: why a merge is unsafe

This branch minted its own WI-605 to WI-611 on 2026-09-24 (`dfa478f1`) and kept
numbering from there, so the IDs `contract_split` used now name different
things here. A straight merge would put duplicate `[open_item.OI-88]` and
`[interface.IF-180]` tables in the registries, and two unrelated archived specs
under one WI number. It would also leave each branch's review and log records
citing an ID that now means something else.

**Spine rows minted on `contract_split`.** All four collide; no SN, SR, LLR or
TC row was minted, and none was removed.

| ID | On `contract_split` | Same ID here |
|---|---|---|
| IF-180 | Drafted; owner `scripts/primary_publication`, requestors `agent_loop`, `integrate`, `dispatch`: root + exact commit → verified candidate or none | the frame/need-tier join layer beside the coherence rules |
| OI-86 | OI-49 (b)'s exception read: the two unargued interface picks and the loaders-versus-frontier ownership split | re-attest the stand-in's signatures on SN-041 to SN-044 |
| OI-87 | the wording round's two banked findings: SR/LLR overlap on seven chains, and LLR-041's drifted Detail | when a test case becomes a requirement's, for the test-first check |
| OI-88 | a one-time reviewed transfer of WI-601, WI-603 and WI-605 into one combined adjudication | the assumption extension's gate sits at DevStg-Arch |

**Work items.** These are examples, not a full census:

| ID | On `contract_split` | Same ID here |
|---|---|---|
| WI-610 | adjudicate combined approved (complete) | reconcile OI-76's ruling text (restructured) |
| WI-612 | redistribute publication responsibility (complete) | make trunk bookkeeping commits stage only what they wrote (complete) |
| WI-619 | adjudicate complete combined (complete) | point builders at the tests (restructured) |
| WI-620 | correct counterpart proof mapping (complete) | one session service for every model call (complete) |
| WI-623 | adjudicate complete combined (complete) | report a flag-axis count (restructured) |
| WI-625 | complete cumulative impact (queued) | rename the ID prefixes (deferred) |
| WI-626 | pending primary-turn resume (queued) | make the shared-spec warning … (restructured) |

Anything recovered from `contract_split` therefore needs fresh IDs here.

## 4. Requirement amendments: where the behavior lives

`contract_split` changed behavior by amending 40 existing rows, not by minting
new ones. None of those amendments reached this branch. Each row kept its
existing Status (37 Approved, 3 Drafted). Ten commits on `contract_split` touch
the registries (`git log 607cf609..contract_split -- docs/requirements
docs/test`). Among them are `0f106ce9` ("sitting: Move approval adjudication
into exclusive primary publication"), `7a7a07a0` ("sitting: Apply OI-86/OI-87
and complete the perspective-review sample") and `c40144d0` ("spine: Apply the
exact PC amendments after the OI-88 ruling"), plus the WI-611, WI-612 and
WI-620 builds. The WI-610, WI-619 and WI-623 adjudication publications changed
no registry row. Grouped by theme:

1. **One work item per lane:** SR-148, SR-156, LLR-151. Every admission,
   claim and resume names exactly one WI, and empty or multi-WI input refuses
   before any state change. Historical multi-WI records stay readable as
   evidence and are never run again. LLR-151 records the trade it makes: N
   exclusive re-attestation windows for N spine WIs instead of one shared
   window.
2. **Primary-turn adjudication replaces adjudication lanes:** LLR-140, 152,
   153, 154, 158, 167, 207 and IF-077, IF-123, IF-175. Adjudication runs in the
   primary checkout under the existing station lock, with no worktree, branch or
   claim. A pending turn blocks claim, merge and integration until it returns
   or publishes. Completion is the terminal spec plus one verified publication
   commit, the "verified carrier" that LLR-207 admits beside the station's
   refresh. LLR-158 makes that turn the only writer allowed to change a
   snapshot or the approval ledger. Several of these rows name the `primary_*`
   modules from §2 in their `module` cell.
3. **SN-036 and SR-161, the perspective-record ruling.** This branch's SN-036
   still requires "a machine-readable record of the declared perspectives …
   A check reports any applicable declared perspective missing from that
   record". The amended need instead asks that each decomposition round be
   reviewed against every applicable perspective, with the review record
   naming each perspective and its outcome. SR-161 follows, and its
   verification changes from Test to Inspection. The amendment cites an owner
   ruling of 2026-09-06 as `docs/log.d/2026-09-06-sn036-owner-ruling.md`. That
   fragment was added in `f6c7360f` and later compiled into `contract_split`'s
   `docs/log.md`, under "2026-09-06 — SN-036 / SR-161 owner ruling", so the
   path exists on neither branch but the ruling's full text survives there.
   Its disposition record,
   `docs/reviews/2026-09-06-sn036-review-dispositions.md`, exists only on
   `contract_split`. **An owner ruling is therefore missing here, and this
   branch's SN-036 still states the design that ruling withdrew.** This
   branch has since built that design (below).
4. **Lane close:** SR-144, LLR-144, LLR-161. A close of a branch holding
   anything other than exactly one claimed spec refuses before any report or
   state change.
5. **Other design rows:** LLR-058, 061, 123, 149, 150, 183. Mostly
   consequential edits that follow groups 1 and 2.
6. **Test cases:** TC-058, 061, 138, 143–148, 153, 154, 156, 161, 178, 205,
   211. Method, evidence or expected-result rewrites to match the rows above.

### Group 3 since the split: this branch built what the ruling withdrew

The ruling lists four acts: amend SN-036, re-point SR-161, close LLR-183's
NOT DISCHARGED clause, and re-point TC-211 at a real review record. So LLR-183
(listed in group 5) and TC-211 (group 6) belong to this group too. The ruling
ends: "Do NOT build `hats_no_finding`, a sidecar record, or a coverage check."

It landed at `f6c7360f` (2026-09-06 17:45), after the common ancestor (17:04
the same day). Every pointer to the old design was already in the ancestor,
so this branch kept all four:

- SR-161's Approved text: a machine-readable record, and a reportable finding
  when an applicable perspective is missing from it.
- LLR-183's NOT DISCHARGED clause: "the no-finding half needs a
  per-decomposition artifact that does not exist".
- The `docs/status.md` line "Next implementation: resolve the existing SR-161
  per-decomposition perspective-record gap and complete TC-211's normal
  sample".
- The decomposition proportionality inspection in
  `docs/test/inspection-procedures.md`, which TC-211's method follows. It
  reads "the existing scoped decomposition/review record and its applicable
  SR-161 applicability/no-finding record".

`contract_split` retired all four (`7a7a07a0`). Here, a merge checkpoint filed
WI-688 to re-judge TC-211. Its first judgement, on 2026-09-28
(`docs/reviews/wi-688-re-judge-tc-211-no-result-rec/001-ADJUDICATE-fe96ec6.md`),
blocked on the missing record. Citing LLR-183's clause and the status line, it
named building the producer as the owed work. It also named the other way out:
re-attest TC-211's dependence on that record, "a decision for the tier
authority". The owner folded the build into WI-688 on 2026-09-30, and
`a9791303` (2026-10-03) shipped it:

- `hats.py record` writes a `<stem>.perspectives.toml` sidecar holding an
  authored `no_finding` for each applicable hat that produced no row.
  `record --check` reports MISSING, STALE and CONFLICT.
- LLR-297 and TC-312, approved in act 26, which also re-attested LLR-183;
  act 27 re-attested TC-211.
- Text that tells sessions to use it: the `Hat-Refs` paragraph of `PROCESS.md`
  §1, item (c3) of `prompts/spine-questions.md`, and a comment in
  `registries/hats.template.toml`. A `RESYNC_PACK.md` entry ("The
  per-decomposition perspective record") carries it to adopters.
- One record:
  `docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.perspectives.toml`.

The check is warn-first. No gate, hook or CI step runs it; (c3) tells the
adjudicator to. The per-need `hats_no_finding` cell the ruling named was never
built. The rest is the sidecar record and coverage check the ruling withdrew.
None of it was built against the ruling knowingly: nothing on this branch,
including what the owner saw at the fold, recorded the ruling.

### Per-row state against this branch

For each field `contract_split` changed: "unchanged here" means this branch
still holds the common-ancestor value, so the amendment would re-apply without
conflict. "Rewritten here" means this branch changed that field on its own
since, so the two need a three-way read. "Already matches" means this branch
holds `contract_split`'s value.

Summary: 24 rows are unchanged here in every amended field, 10 are partly
rewritten, 5 are fully rewritten, and 1 (TC-161) partly matches already.
<!-- fig: derived="tallied from the per-row table below, a row counted by the states of its amended fields" -->

| Row | Status at the ancestor | Amended fields, and their state here |
|---|---|---|
| IF-077 | Drafted | `data` unchanged here; `requestors` unchanged here |
| IF-123 | Drafted | `requestors` unchanged here |
| IF-175 | Drafted | `notes` rewritten here; `requestors` rewritten here |
| LLR-058 | Approved | `title` unchanged here |
| LLR-061 | Approved | `detail` unchanged here |
| LLR-123 | Approved | `detail` unchanged here; `rationale` unchanged here; `title` unchanged here |
| LLR-140 | Approved | `code_symbol` rewritten here; `detail` rewritten here; `module` unchanged here |
| LLR-144 | Approved | `detail` unchanged here |
| LLR-149 | Approved | `detail` unchanged here |
| LLR-150 | Approved | `detail` unchanged here |
| LLR-151 | Approved | `detail` rewritten here; `rationale` unchanged here; `title` unchanged here |
| LLR-152 | Approved | `code_symbol` unchanged here; `detail` unchanged here; `module` unchanged here |
| LLR-153 | Approved | `code_symbol` rewritten here; `detail` rewritten here; `module` unchanged here |
| LLR-154 | Approved | `code_symbol` unchanged here; `detail` rewritten here; `module` unchanged here |
| LLR-158 | Approved | `code_symbol` rewritten here; `detail` rewritten here; `module` unchanged here |
| LLR-161 | Approved | `detail` unchanged here |
| LLR-167 | Approved | `code_symbol` rewritten here; `detail` rewritten here; `module` unchanged here |
| LLR-183 | Approved | `detail` rewritten here |
| LLR-207 | Approved | `code_symbol` rewritten here; `detail` rewritten here; `module` unchanged here |
| SN-036 | Approved | `acceptance` unchanged here |
| SR-144 | Approved | `acceptance_criteria` unchanged here; `requirement` unchanged here |
| SR-148 | Approved | `acceptance_criteria` unchanged here; `rationale` unchanged here; `requirement` unchanged here |
| SR-156 | Approved | `acceptance_criteria` rewritten here; `requirement` unchanged here |
| SR-161 | Approved | `acceptance_criteria` unchanged here; `rationale` unchanged here; `requirement` unchanged here; `verification` unchanged here |
| TC-058 | Approved | `method` unchanged here |
| TC-061 | Approved | `method` rewritten here |
| TC-138 | Approved | `method` unchanged here |
| TC-143 | Approved | `method` unchanged here |
| TC-144 | Approved | `method` unchanged here |
| TC-145 | Approved | `method` rewritten here |
| TC-146 | Approved | `method` unchanged here |
| TC-147 | Approved | `evidence` unchanged here; `method` rewritten here |
| TC-148 | Approved | `evidence` unchanged here; `method` unchanged here |
| TC-153 | Approved | `method` rewritten here |
| TC-154 | Approved | `method` unchanged here |
| TC-156 | Approved | `method` unchanged here |
| TC-161 | Approved | `method` rewritten here; `tier` already matches |
| TC-178 | Approved | `expected` unchanged here |
| TC-205 | Approved | `evidence` rewritten here; `level` unchanged here; `method` rewritten here; `verifies` rewritten here |
| TC-211 | Drafted | `expected` unchanged here; `method` unchanged here; `verifies` unchanged here |

"Unchanged here" means only that the amendment would apply mechanically. It
does not mean the amendment still fits: the surrounding rows, and the redesign
since 2026-09-20, may have made it wrong. For example, this branch's WI-620
routes every model call through one session service, which may cover ground
group 2 covered differently. That has not been checked.

## 5. Questions for the review

1. **SN-036 / SR-161 (group 3). Answered 2026-10-13:** the owner directed
   that the ruling stands. The retirement of WI-688's build and the ruling's
   four row acts are planned as
   [item 14 of the review-churn plan](2026-10-11-review-churn/README.md#14-retire-the-perspective-record-sidecar-apply-the-2026-09-06-hat-ruling-here).
   No fresh OI is needed: on `contract_split` the SN-036 act cited the
   ruling's log fragment directly, and a fragment here can do the same.
2. **One WI per lane (group 1). Answered 2026-10-13:** adopted. The owner:
   "if the rest of the mechanisms in the current branch are only built for a
   single WI, agreed scope should be configured to match". Planned as
   [item 15](2026-10-11-review-churn/README.md#15-one-work-item-per-lane).
3. **Primary-turn adjudication (group 2 and §2). Answered 2026-10-13:**
   superseded. What it fixed was a snapshot copied in a lane before review had
   settled (WI-605's incident, recorded in `contract_split`'s
   `CONTROL-RETRY.md`); the owner's 2026-09-07 answer then was "a worktree
   should absolutely never touch a snapshot". The owner now rules that
   snapshots are permitted in a lane when they are ruled in that lane, which
   is this branch's practice: the coordinator takes the act mechanically after
   the sitting's verdict. So the group 2 amendments and the `primary_*` code
   do not come back. The hazard the owner named instead, the id watermark
   rising in parallel lanes, is planned as
   [item 16](2026-10-11-review-churn/README.md#16-one-mint-across-parallel-lanes).
   WI-605's preserved lane worktree (`668edaf4`) is that incident's evidence.
4. **Lane close (group 4) and the test-case rewrites (group 6). Answered by
   2 and 3:** lane close and the test cases under groups 1 and 4 travel with
   item 15. Those verifying group 2 rows drop. TC-178 and TC-211 belong to
   group 3 (item 14).
5. **IDs. Settled by default:** whatever comes back is minted fresh, and this
   report stays as the record of the old meanings (§3).
6. **Stable id meaning. Answered 2026-10-14:** the owner's keep-or-mint rule
   replaces the stranded 2026-09-07 one ("an ID's meaning must remain stable
   or every use and reference needs an impact review", which `contract_split`
   built into `PROCESS_OPTIONS.md`, the amendment brief, `gate-advance` and one
   LLR). The owner: "in general to lean into minting IDs, but to retain IDs if
   the spirit of the ID is retained and it would be less changes overall to
   continue using the same ID and potentially modifying some of its current
   usage locations compared to minting a new ID and potentially touching more
   downstream users than just reusing." No tracked record on this branch held
   the rule before; it is recorded now, and item 16 of the review-churn plan
   states it once in PROCESS.md §4.

## Reproducing

```sh
git fetch origin contract_split   # the local ref matched origin at writing
python docs/plans/2026-10-13-contract-split-divergence-census.py \
    --base 607cf609 --lost contract_split --here HEAD
# one row's amendment in full:
git diff 607cf609 contract_split -- docs/requirements/stakeholder-needs.toml
# group 3: the ruling's text, its timing, and what this branch built since:
git show contract_split:docs/log.md | grep -n -A40 'SN-036 / SR-161 owner ruling'
git show -s --format='%h %ad %s' --date=iso 607cf609 f6c7360f 7a7a07a0
git show --stat a9791303
```
