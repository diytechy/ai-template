Reviewed: f7bdfe4f6e44adbc603c10b9d70aa2061a187650

WI-969 full-lane review (254e609c5..f7bdfe4f6), rubric docs/rubrics/kit-change-review.md. Independent reviewer r1b. The round is not in the convergence stance.

**Failure classes hunted first.** Three, worst first:
- A record admitted without validation (fail-open authority over the sweep).
- A successor or its lineage silently dropped (silent wrong content).
- The new per-commit rider refusing a supported close or landing, with no way back (the 016 FIX class).

**Verified.**
- **The reviewed checkout.** `git rev-parse HEAD` printed f7bdfe4f6e44adbc603c10b9d70aa2061a187650.
- **The F1 FIX (sitting 016) is built as ruled.** `kitlib.verdict.mechanical_close` is the one close-shape reader. The peel calls it with no oracle. `adoption_record._commit_close` injects `spec_move.exact_relink`, and `_outside_relinked` admits only `M` entries outside `docs/work/` whose blobs are the exact relink of the commit's own paired moves. The regression test `test_a_real_close_relinking_a_file_outside_docs_work_passes_the_rider_and_the_squash_hook` FAILS on the pre-fix behaviour. I checked this in a copy of the tip tree with the oracle argument removed: 1 failed, 3 passed. The hand-written-record-beside-the-relink tests still pass there.
- **Review 015's reproduction is fixed.** A valid block followed by an unclosed one gave this on base `parse_dispositions`: one draft, with the unclosed block folded into its `scope`, and no refusal. At the tip it is refused: "fence line '```toml' opens a block that no bare ``` fence closes".
- **No trunk section fails the tightened grammar.** I ran the tip parser over all 69 `## Dispositions` sections in the tree, then over them again with the old regex. No section changed its block count. Five sections are refused, all for draft-key reasons that base refuses identically (WI-563, WI-568, WI-574, one iteration log, and wi-544 001-ADJUDICATE). So the Done-when grammar claim holds.
- **The close.** It validates once, at lane HEAD, before any move, and a refusal moves nothing. It writes the record in the same rewrite, before `order`. The consolidation arm refuses an adoption before its first write.
- **The sweep.** It refuses each of: request without record, record without request, the two differing, a malformed record, and an unreadable merged spec. It re-points from the record and reads no history.
- **Mint lineage.** `_standing_successors` refuses a title match on another lineage. `_repoint_owed` keeps a replay with nothing left to re-point commit-free.
- **Riders.** The slot walks both riders, and only text then act's lines get `TEXT_THEN_ACT_REMEDY`. The hook's squash path for text then act walks only its own rider, so nothing is judged twice.
- **Done-when coverage map.** Every item maps to a test:
  - close accept and refusals: `test_handback.py::test_an_adoption_that_is_not_accepted_refuses_the_close`, covering missing, complete, cancelled, not-utf8, unparseable, other-lineage and no-supersedes; plus the untokened, repeated and drafted-beside-adoption tests, and `test_consolidate_close.py::test_a_consolidation_verdict_that_adopts_refuses_the_close`;
  - commit check, every case: `tests/test_adoption_record.py`;
  - sweep: `test_intake.py`, including the late dependent, completed successor, shallow clone, the four mismatch cases and the unreadable spec;
  - parser at the close and at the sweep, for adoptions and drafts;
  - trunk grammar: `test_every_dispositions_section_in_the_repository_passes_the_fence_grammar`;
  - RESYNC: one entry naming the three tightenings;
  - round-count decision: `docs/decisions/wi-969.toml` (review round count starts at zero).
  - Not run by me: the bar's smoke-tier item. Per the round facts, I ran no smoke or full suite.
- **Requirement and interface relationships, with my decision on each counterpart.**
  - SR-148 acceptance amended. LLR-161 carries it (TC-156 method carried). LLR-312 carries the consolidation refusal (TC-254 method carried). The new LLR-335 and LLR-345 are its decomposition, with TC-360 and TC-383. LLR-153 detail amended, but its counterpart TC-147 did NOT carry it (finding 1).
  - LLR-302: only its code_symbol pointer changed (`_with_text_then_act_remedy`). TC-173 is retained, justified: the text-then-act rule's behaviour is unchanged, and only the remedy's composition point moved.
  - IF-175 data amended. Its owner verdict.py does carry `mechanical_close`, and its new requestor adoption_record does call it.
  - IF-303 and IF-304 match adoption_record's calls and CLI.
  - IF-294 does not match its owner (finding 5).
  - Decomposition, LLR-335 and LLR-345:
    - LLR-335's independent decision is what an adoption is, and how it is validated, recorded and replayed.
    - LLR-345's independent decision is which commit may write that record.
    - Splitting LLR-345 further, into a slot form and a hook form, would add no independent value: both are one comparison over two trees.
    - LLR-335's last sentence overlaps LLR-345 (finding 7).
- **K3.** Every new `Implements:` tag names an LLR whose `module` holds the file and whose `code_symbol` lists the function. Statuses: no Status flips. The approved rows were edited only among those the spec grants for a re-sit, with LLR-302's pointer cell the one exception.

**Commands.**
- `git rev-parse HEAD` -> f7bdfe4f6e44adbc603c10b9d70aa2061a187650
- `python -m pytest -q -p no:cacheprovider -n 2 --basetemp .../r1b/wi-969 tests/test_disposition_adoption.py tests/test_adoption_record.py tests/test_intake.py tests/test_handback.py` -> `245 passed in 233.58s (0:03:53)`. The posix-shell env gate skipped 0.
- `python project-trajectory/scripts/check_trajectory.py --strict` -> `check_trajectory: clean (966 work item(s), 850 done (88%), 34 cancelled, graph acyclic).`
- `python project-trajectory/scripts/trace.py --strict-integrity` -> `Traceability: SN=31 SR=134 LLR=312 TC=338 orphans=0 integrity=0 verified-mechanized=127 verified-demonstrated=6 verified-attested=0 drafts=5 budgets=4 budget-findings=0 components=4 component-findings=0 interfaces=251 interface-findings=0 ac-advisories=1 paraphrase-advisories=2.`
- Red-before probe, tip copy with the relink oracle removed from `_commit_close`: `pytest tests/test_adoption_record.py -k "relinking or beside_the_same_relink"` -> `1 failed, 3 passed` (the F1 regression goes red).
- Grammar probe over every `## Dispositions` section, tip parser against the old regex -> `sections 69`, `count differs: []`. The 5 refusals are pre-existing; on base, `parse_dispositions` refuses each too (`True` x4 checked).
- Indented-fence probe, a valid draft then a bullet-nested adoption block, through `intake.parse_disposition_section`:
  - tip -> one draft and `[]` adoptions, refusal None; the adoption block sits in the draft's `scope`;
  - base -> refusal "block 2 carries unknown key(s) ['adopts']", so base did see the block.
- Request-edit probe, a real `close_adjudication`, then a lane commit editing only `adopts = "WI-450"` to `"WI-777"` in the complete spec:
  - `commit_adoption_record_lines` -> `[]`;
  - slot walk -> `None`;
  - `intake._recorded_lineage` -> refusal "record WI-450 does not match the adoption its ## Dispositions section requests WI-777".

**Findings.**

- [MAJOR] docs/test/test-cases.toml:1465 -> The re-sat Approved TC-147 changed its `evidence` from the whole module, `tests/test_intake.py`, to six new lineage and adoption nodes, and left its `method` (line 1461) unchanged. The evidence now cites no test for the Method's standing clauses: the SR amendment mint, the handback disposition row, the malformed-block refusals, `[open_item]`, the census, the context block, the held and released dial, and `adjudication_action`. Meanwhile the Method states none of the LLR-153 clauses this lane added and the cited tests verify: an adopts-only block allocates no id, title identity and lineage resolve together, and a replay re-points to the full successor set. Both directions of the TC-147 <-> LLR-153 relationship are now false. TC-156, by contrast, kept its module evidence and appended. Anchors K1 and K3. -> Keep `tests/test_intake.py` in TC-147's evidence and append the six nodes, as TC-156 does. Add the three new LLR-153 behaviours to TC-147's method in the same re-sit. -> @owner
- [MINOR] project-trajectory/scripts/intake.py:1539 -> `_fenced_blocks` treats only lines that begin in column 0 with three backticks as fences. An indented fenced block, such as one nested under a list bullet, is not paired or refused. It is folded silently into the previous block's `scope` prose. Base's regex parsed it as a block. Case: a valid draft followed by a bullet-nested `adopts` block. At the tip, the adoption vanishes with no refusal; the close writes no record and the sweep re-points nothing to it. A second indented draft would vanish the same way, though base minted it. The input is outside the plan's declared grammar, and the change fails open on it: the silent-loss class this lane's deliverable (A) exists to close. It is rare (0 of 69 trunk sections), so MINOR. Anchor B1, confirmed by the probe. -> Judge every line whose `lstrip()` starts with three backticks as a fence line, so an indented fence refuses the section by name. A guard is not the right fix here: the grammar's one owning parser should simply recognise the full fence set, and nothing else has to check it. -> @owner
- [MINOR] project-trajectory/scripts/adoption_record.py:311 -> `_spec_refusal` returns None whenever the record is carried unchanged and the spec did not move into `complete/`, without reading the request. So a later commit that rewrites a closed spec's adoption request while keeping its record passes the slot and the hook. It then fails closed only at the post-merge sweep, which stops the run with the merge already standing. The spec's Trust names the admitted later commit as one that "carries an existing record and request unchanged". LLR-345 (low-level-requirements.toml:3565) says the same. Confirmed by the probe: rider `[]`, slot `None`, sweep refusal. Anchor K1. -> When the record is carried, also compare the request with a parent's request, and refuse a change, so the commit check enforces what LLR-345 states. Why this cannot be made unrepresentable within this diff: the spec makes the sweep compare request with record, so the request stays a live input after the close. The structural alternative is that the close becomes the request's last reader, and that exceeds this diff. -> @owner
- [MINOR] project-trajectory/scripts/adoption_record.py:275 -> `_spec_paths`, the `{wi: [path]}` of the specs under `docs/work` and `docs/archive/work` at a tree or the index, repeats in intent `acceptance_record._tree_specs` (project-trajectory/scripts/acceptance_record.py:2000). That function lists the same two roots at a tree or the index, into `{WI id: path}`. This module already imports from acceptance_record. The difference is that `_tree_specs` collapses duplicate ids where this rule must refuse them. PROCESS.md §3, "Consolidate, don't duplicate". -> Extract one tree-spec listing, path lists per id, that both callers read: acceptance_record keeps its single-path view, and adoption_record keeps its duplicate refusal. Or record why the two must stay apart. -> @owner
- [MINOR] docs/requirements/interfaces.toml:2718 -> IF-294's `data` lists `parse_disposition_section` as a call of its owner `scripts/kitlib/adoption`. That function lives in `intake.py`. The owner's own contract (kitlib/adoption.py:27) declares `parse_block`, which the row omits. The interface row misstates its seam. Anchor K1. -> Replace `parse_disposition_section` with `parse_block` in IF-294's `data`. -> @owner
- [MINOR] docs/requirements/system-requirements.toml:642 -> For clarity: SR-148's amended acceptance reads "names an already-open item that supersedes it as its successor". In this kit, an "item" beside "open" reads as an open item (OI), not a work item. The rule the code enforces is an open work item whose supersedes names the closed row. Anchor K2: wording only; the cell names no carrier. -> Say "an already-open work item that supersedes it". -> @owner
- [MINOR] docs/requirements/low-level-requirements.toml:3553 -> For clarity: LLR-335's last sentence, "A record changes only in the close that created it or remains unchanged with its request", restates LLR-345's admission rule. That puts one decision in two rows. LLR-345 (line 3565) also scopes the requesting move to `docs/work/complete`, while the code (`_in_complete`) judges `docs/archive/work/complete` too. -> Drop the sentence from LLR-335, leaving LLR-345 as the rule's one home, and name both complete folders in LLR-345. -> @owner

VERDICT: CHANGES-REQUESTED findings=7
