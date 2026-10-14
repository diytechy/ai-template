# What `contract_split` holds that this branch never received

**Status: FINDINGS FOR OWNER REVIEW.** This report recovers nothing and mints
nothing. It records what the divergence lost, so that a review sitting can
decide what to bring back and under which new IDs. It was written 2026-10-13
on `refactor_again` at `bf45bd35`.

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
   ruling of 2026-09-06 as `docs/log.d/2026-09-06-sn036-owner-ruling.md`, a
   file that exists on neither branch. Its disposition record,
   `docs/reviews/2026-09-06-sn036-review-dispositions.md`, exists only on
   `contract_split`. **An owner ruling is therefore missing here, and this
   branch's SN-036 still states the design that ruling withdrew.**
4. **Lane close:** SR-144, LLR-144, LLR-161. A close of a branch holding
   anything other than exactly one claimed spec refuses before any report or
   state change.
5. **Other design rows:** LLR-058, 061, 123, 149, 150, 183. Mostly
   consequential edits that follow groups 1 and 2.
6. **Test cases:** TC-058, 061, 138, 143–148, 153, 154, 156, 161, 178, 205,
   211. Method, evidence or expected-result rewrites to match the rows above.

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

1. **SN-036 / SR-161 (group 3).** Does the 2026-09-06 perspective-record
   ruling stand? If it does, this branch's SN-036 and SR-161 need the
   amendment, plus a recorded ruling under a fresh OI. The original log
   fragment is missing on both branches.
2. **One WI per lane (group 1).** Adopt, reject or re-judge it against the
   lane model this branch now runs? It is owner-level scheduling policy, not
   a mechanical fix.
3. **Primary-turn adjudication (group 2 and §2).** Has this branch's redesign
   replaced the mechanism? If so, the group 2 amendments and the `primary_*`
   code can be recorded as superseded. If not, which pieces come back, and as
   which new WIs?
4. **Lane close (group 4) and the test-case rewrites (group 6).** Carry them
   with whichever of groups 1 and 2 survives, or drop them with it.
5. **IDs.** Whatever comes back is minted fresh here. Should this report's
   cross-reference table (§3) be kept as the record of the old meanings, so
   that `contract_split`'s records stay readable?

## Reproducing

```sh
git fetch origin contract_split   # the local ref matched origin at writing
python docs/plans/2026-10-13-contract-split-divergence-census.py \
    --base 607cf609 --lost contract_split --here HEAD
# one row's amendment in full:
git diff 607cf609 contract_split -- docs/requirements/stakeholder-needs.toml
```
