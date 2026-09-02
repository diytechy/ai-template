### REVIEW-A — WI-569 + WI-575 — Round 002 — 2026-09-02 — supervisor-drawn (independent Opus, hostile brief)

**Subject:** this lane's own diff, `git diff 2f660cb7ad59..4566ca27` (7 commits,
10 files, +539/-11). Round 001 in this directory is the lane's *drawn* round and
its subject is the four SR-163 spine rows, not the diff; this round judges the
lane. Read-only: nothing outside this file was written, no commit, no
state-changing git.

## What I verified

**1. The absolute constraint — no `status` flip, no `docs/archive/last_approved/`
write. CLEAN, driven rather than read.**

```
$ git diff 2f660cb7ad59..4566ca27 --name-only | grep -i last_approved   ->  (empty)
$ git diff 2f660cb7ad59..4566ca27 -- 'docs/requirements/*' 'docs/test/*' | grep -E '^[+-].*status'
   (only the LLR-158 `detail` body, which contains the word; no `status = ` line on either side)
```
```
>>> acceptance_record.lane_approval_refusal('.', '2f660cb7ad59', '4566ca27')
None
>>> acceptance_record.approval_delta('.', '2f660cb7ad59', '4566ca27')
acts= []   snapshot_files= []   refusal= None
>>> acceptance_record.merge_approval_refusal('.', '2f660cb7ad59', '4566ca27', [], False)   # the
    judgement integrate._approval_act_refusal delegates to for a non-adjudication lane
None
>>> acceptance_record.staged_spine_amendments('.', '2f660cb7ad59', '4566ca27')
   low-level-requirements.toml LLR-158 / LLR-203 / LLR-204
>>> acceptance_record.staged_drafted_rows(...)   ->  []
```
`integrate._approval_act_refusal(root, branch)` itself derives its base from
`merge-base(HEAD, branch)`, which is degenerate inside this worktree, so I drove
the judgement it delegates to with the real base supplied. Three amendments to
approved text stage, which is the intended route: they mint the amendment
adjudication at merge. **No breach.**

**2. WI-569's spine-row corrections — each claim re-derived against the code.**

Every corrected statement is TRUE at the tip, and each removed statement was in
fact false (no true text was regressed):

| removed claim | driven refutation |
| --- | --- |
| LLR-203 "no cell joins an inventoried file to a requirement id … no check resolves" | `bootstrap.mapping_entries()` -> 148 rows, **21 carrying a third reference cell**; `gen_arch_map.resolve_requirement_reference` is the SR->live-need join |
| LLR-203 "every arm … walks the DESTINATIONS the inventory declares, never the shipped tree" | `bootstrap.delivery_inventory()` -> `213 physical sources / 31 exclusions / 86 conditional / 15 generated`, an `rglob` over `KIT` independent of MAPPING |
| LLR-203 "the installer is excluded … in prose at its module rather than as a row in the exclusion carrier" | `project-trajectory/mapping-source-exclusions:19` — `scripts/bootstrap.py — installer/generator run from the kit; deliberately not scaffolded`, parsed by `bootstrap._mapping_source_exclusions()` |
| LLR-204 "The grammar and the dial are what the parent's join and its policy would ride; neither runs for it today" | the delivered join rides `MAPPING_FINDING_POLICY` (`gen_arch_map.py:2003`) + the inventory's reference cell; `read_backlink_min`/`backlink_ids` are not in that path |

New claims independently confirmed: "all four … finding classes run over the
inventory today" —
```
$ .venv/bin/python project-trajectory/scripts/gen_arch_map.py --mapping-purpose --root .
mapping purpose: missing_file — 0 finding(s) [GATE]
mapping purpose: stale_entry — 0 finding(s) [GATE]
mapping purpose: unmapped_file — 152 finding(s) [WARN]
mapping purpose: unresolved_reference — 0 finding(s) [WARN]
```
"the reference cell is mostly UNFILLED" — 21/148 = 14 % filled, true. "the
unmapped class is warn and not gate" — `MAPPING_FINDING_POLICY["unmapped_file"] =
"warn"`, true. "tolerant by construction … a bare pair survives as a reference of
None" — `mapping_entries` returns `row[2] if len(row) > 2 else None`, true. "named
by no design row's Module or CodeSymbol" — `grep -n
'resolve_requirement_reference\|mapping_purpose_findings\|MAPPING_FINDING_POLICY'
docs/requirements/low-level-requirements.toml` -> no hits, true.

**3. WI-569's drawn round — real, not a rubber stamp.** `OPENAI-SOL`
(`gpt-5.6-sol`, medium), a different family from the author, returned
`VERDICT: CHANGES-REQUESTED findings=2`, both MAJOR, both against the `Approved`
rows — a stamp does not return CHANGES-REQUESTED against its own lane's premise.
Its anchors are real (`bootstrap.py:2261`, `:2341`, `gen_arch_map.py:2032`,
`:2085`, `mapping-source-exclusions:19`) and I re-derived each above. Its subject
is the four rows, as required. The re-verification section even records an
imprecision *against* the finding it accepts (the title/detail conflation). The
lane's own record does not over-claim: it reports the verdict as
CHANGES-REQUESTED, not as confirmation, and states the design half of both
remedies as deliberately NOT taken.

**4. The two routed `5175065` BLOCKERs — ANNOTATE, no successor; accurate.**
```
$ git log --diff-filter=A --oneline -- docs/plans/2026-08-25-blind-minimal-map-brief.md \
      docs/plans/2026-08-25-blind-minimal-map-derivation.md
64e9bf2a WI-508: run the blind minimal-map derivation on two axes, and disclose what it could not hold blind
```
One commit adds both — the anti-post-hoc defect is real and the caveat states it
correctly. The contamination caveat points at the teams' own §1 disclosure, which
is where it lives. Both annotations are additive (`+47`/`+15`, no `-` lines
except the one stale `docs/work/active/` path corrected to
`docs/work/partial/`), so the record stays the record. The Deliverable says which
route was taken, for both, in a bolded sentence, with the three grounds for
refusing a re-run. **Obligation discharged.**

**5. WI-575's correction — re-derived by import.**
```
SPINE_CSVS n=3   APPROVAL_ACT_CSVS n=4   OUTSIDE_THE_APPROVAL_ACT n=3   SNAPSHOTTED n=7
SNAPSHOTTED == APPROVAL_ACT_CSVS + OUTSIDE_THE_APPROVAL_ACT : True   disjoint: True
_spine_row_sides(root, base, head, registries=SPINE_CSVS)   # default is the three
acceptance_record.py:558   `root, base, head, APPROVAL_ACT_CSVS`  # only staged_approval_acts' body
all 12 code_symbol names resolve as attributes of acceptance_record: True
```
Every statement in the new `detail` clause is true; `code_symbol` now names all
three constants and every symbol is a real attribute. The pin the cell cites is
`tests/test_acceptance_record.py::test_no_snapshotted_tier_can_go_unseen_by_the_approval_rung`.
No WI/OI citation frame entered any spine cell: `trace.py --strict-integrity`
reports `provenance-findings=1`, the pre-existing LLR-197 finding, unchanged from
base.

**6. Records.** Both closed specs carry `## Deliverable` before `## Context`,
filled, `specref = ""`. `docs/ratify/CURRENT.md` is byte-current — regenerated to
a scratch path with `trace.py --root . --approve modified --out <scratch>` and
`diff` against the committed file is EMPTY — and carries LLR-158, LLR-203,
LLR-204. Two log.d fragments exist; WI-575's file-level line is at line 3, above
its first heading, and is accepted. **WI-569's is not — see finding 1.**

**7. Bar at the tip (run once).**
```
$ .venv/bin/python -m pytest -q -n auto -m smoke
1463 passed, 4 skipped in 22.36s                                    [exit 0]
$ .venv/bin/python project-trajectory/scripts/check_docs.py --root . --stale
check_docs: OK - 1234 doc(s), 1595 intra-repo link(s), 0 broken (1 orphan warning(s)).
$ .venv/bin/python project-trajectory/scripts/check_trajectory.py --root .
check_trajectory: clean (574 work item(s), 531 done (93%), 21 cancelled, graph acyclic).
$ .venv/bin/python project-trajectory/scripts/trace.py --root . --strict-integrity
Traceability: SN=27 SR=76 LLR=188 TC=187 orphans=2 integrity=0 … provenance-findings=1
$ .venv/bin/python project-trajectory/scripts/gen_open_items.py --root . --check   ->  exit 1
```
The four named checks are green. `gen_open_items --check` is RED, and two of its
three findings are this lane's (finding 1). I also confirmed the pre-existing
third: `git archive 2f660cb7ad59 | tar -x -C <scratch>` and re-running the check
there emits only `docs/open-items.html STALE`, so that one is trunk's, not this
lane's. Targeted: `tests/test_acceptance_record.py tests/test_gen_arch_map.py
tests/test_bootstrap.py` -> `130 passed in 57.89s`.

## Findings

- [MAJOR] docs/log.d/WI-569-wi508-spine-reseal.md:139 -> the fragment's `Deferred open items:` line is NOT file-level and the file fails the check the close claims it passes -> `grep -n '^### '` puts the first heading at line 13 and the declaration at line 139, inside the last section, so `gen_open_items.py --root . --check` exits 1 with two findings this lane introduced: `3 of 4 sections carry no deferral declaration, and the 1 that do speak only for their own section` and `:139 declares OI-78 deferred, but that row reads 'ruled'` (`open_items.toml:3190 status = "ruled"`); at base the same check emits only the pre-existing `open-items.html STALE` -> move the line into the fragment's top matter above line 13 and drop the `OI-78` token from it (`Deferred open items: none.`), putting the OI-78 account in the prose below; no new check is warranted because `gen_open_items --check` already makes this unrepresentable-on-detection — what failed is that the lane's stated commit bar (smoke + check_docs + trace) does not include it -> WI-569 close, before merge.
- [MAJOR] docs/archive/work/complete/WI-569-wi-508-spine-reseal-one-clean.md:70 -> the Deliverable asserts in the present tense that "all four rows are cell-for-cell identical to the round-010-approved tree `b8d57e9f`", which is false at the tip and contradicted by the same Deliverable four paragraphs above -> loading both trees with `tomllib`, `LLR-203` differs from `b8d57e9f` in `title`, `detail`, `rationale` and `LLR-204` in `detail` at `4566ca27`, while both ARE identical at base `2f660cb7` — this lane's own `33aee707` is what broke the identity -> re-tense the clause to the moment the ruling was made ("were identical when the reseal question was ruled; the amendment below is what now drifts them, deliberately, back into the re-attestation brief"); the defect is a stale present-tense claim in a hand-written record and no guard can make prose self-updating -> WI-569 close, before merge.
- [MAJOR] docs/reviews/wi-569-wi-508-spine-reseal-one-clean/001-REVIEW-A-2f660cb7-spine-rows.md:9 -> the round file states "The lane's OWN verdict is a separate artifact (`docs/reviews/WI-569-REVIEW-A.md`) and is not this file", and that artifact does not exist -> `ls docs/reviews/WI-569-REVIEW-A.md` -> `No such file or directory`, and the path appears in no commit of `2f660cb7ad59..4566ca27`; `check_docs --stale` misses it because it is a backticked path, not a markdown link -> delete the clause, or point it at the round that actually carries the lane's verdict; the general fix is to write cross-references as markdown links, which `check_docs`' broken-link arm already makes unrepresentable, rather than as backticked prose paths -> WI-569 close, before merge.
- [MINOR] docs/requirements/low-level-requirements.toml:2139 -> LLR-203's new `detail` states the exclusion carrier's grammar as "one `<source> - <reason>` row per kit-only file"; the parser requires an EM DASH -> `bootstrap._mapping_source_exclusions` partitions on the literal `" — "` (`bootstrap.py:2335`) and the carrier's own header says "One `<source> — <reason>` per line"; a hyphen row is silently skipped (`if sep and …`), the source stays unclassified, and it surfaces as a GATE-class `missing_file` finding — so the grammar is load-bearing and the cell mis-states it -> quote the em dash in the cell; the cell's uniform ` - ` prose dashing is the likely cause, so quoting the separator inside a code span rather than as prose is the durable form -> follow-on, or WI-569 close if the row is reopened anyway.
- [MINOR] docs/archive/work/complete/WI-569-wi-508-spine-reseal-one-clean.md:22 -> the amendment of two `Approved` rows is a THIRD act beyond the scope WI-572 narrowed this row to ("(1) the one clean … round … (2) rule the two `5175065` BLOCKERs"), and the amended text itself entered the lane with no independent round over it — round 001's subject is the PRE-amendment rows -> the Context's WI-572 UPDATE enumerates exactly two remaining arms and neither is "amend the rows"; `staged_spine_amendments` over base..tip returns three rows the drawn round never read in their new form -> no rework: the corrections are each verified true in section 2 above and this round supplies the missing independent read of the new text, so record the scope extension in the Deliverable as taken knowingly rather than leaving it implicit; the amendment adjudication minted at merge is the structural backstop that already makes an unreviewed approved-text change non-silent -> WI-569 close, one sentence.

VERDICT: CHANGES-REQUESTED findings=5
