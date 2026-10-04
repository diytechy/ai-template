**VERDICT: NOT-SOUND.**

The edge reversal is buildable. Design 6 lacks a complete mechanical definition, and designs 3–5 omit readers, writers and checks that would contradict the promised result.

Reviewed HEAD `83abd4d2`; no files changed. In-memory probes confirmed placeholder parsing and R-A/R-E validity. Script references below are under `project-trajectory/scripts/`.

**FINDINGS:**

1. **Design 6’s transition baseline is ambiguous and unavailable on supported paths.**  
   **Evidence:** WI-790:179–191 specifies the *first* non-pending commit and leaves missing history/uncommitted rulings unresolved. This repo fetches full history (`.github/workflows/test.yml:68–70`), but shipped CI supplies no depth setting (`project-trajectory/ci/check.yml:46`). Existing staleness deliberately skips missing/uncommitted history (`check_trajectory.py:2354–2376`). Refresh checks an uncommitted composed merge before committing it (`integrate.py:2570`, `2653–2659`).  
   **Consequence:** borrowing staleness’s skip behavior creates the prohibited degraded path. Reopened items compare against the wrong ruling; a working-tree ruling has no transition commit; merge history offers multiple parents. An absent WI baseline also needs a definition for rows created after the ruling.  
   **Fix:** replace the unresolved paragraph with an explicit contract, for example:

   > “For the current ruled episode, the transition is the latest pending→ruled change along the checked revision’s first-parent history. Compare each affected WI by immutable id, resolving its path separately in each tree. The candidate index/worktree is an uncommitted child of HEAD; a merge candidate has the actual ordered merge parents. Missing required history is an environment ERROR, never a skipped comparison. A WI absent before the transition must contain non-empty decided criteria when introduced.”

   Use the same tree-comparison engine for committed, staged and merge candidates. Never use another checkout’s current files. Set full history in shipped CI and document the requirement for shallow clones and adopters. A history-free scaffold carrying only pending OIs is vacuous; a copied ruled dependency without a recoverable baseline must fail explicitly.

2. **Design 6 can pass without updated criteria, or lose the obligation entirely.**  
   **Evidence:** WI-790:182–185 compares section lines; `registry.done_when_section:243–256` preserves blank lines and checkbox text. Thus whitespace/ticking can differ, and deleting previously present criteria also differs. WI-790:178 selects only current `needs` citations, so removing a token removes the check. The second-pass reading expressly treats token removal as sufficient (:115–116), whereas the third pass demands updated Done-when (:124–127).  
   **Consequence:** cosmetic edits, deletion of criteria or removal of the edge can satisfy or evade the ERROR without incorporating the ruling.  
   **Fix:** define affected WIs from the transition’s **before tree**, retaining that obligation until fulfilled or terminal; also validate newly introduced ruled citations. Require non-empty resulting criteria and a substantive change, using the existing item comparison (`kitlib/done_when.py:75–87`, `113–138`). Proposed wording:

   > “Removing an OI token does not discharge a ruling’s update obligation. An open affected WI must retain non-empty Done-when criteria with a substantive change; whitespace, ticks and appended completion evidence alone do not satisfy it.”

   Independent review must judge whether those changes implement the ruling and whether other fields need amendment. The script establishes a mechanical condition; it approves nothing.

3. **Design 4 can hide an owed decision while both owner projections appear empty.**  
   **Evidence:** WI-790:156–159 filters to queued citations. Draft/deferred WIs are open (`check_trajectory.py:387`) but excluded before scheduler gate classification (`schedule.py:767–768`). `gen_open_items.py:465` currently claims “the owner queue is empty” when no cards render. More seriously, `check_trajectory.py:3287–3303` returns vacuously clean before OI findings when no real WIs exist.  
   **Consequence:** moving the sole citer to draft/deferred/terminal, deleting it, or minting an OI without a WI makes the decision invisible. An ERROR in console output does not ensure the owner sees it on the specified surface. The no-WI case can miss the ERROR altogether.  
   **Fix:** evaluate uncited-pending integrity before WI vacuity, as an unconditional ERROR independent of `--strict`. Derive cards, counts, status entries and uncited findings from one queue projection. Render an explicit integrity notice naming uncited pending IDs and linking their registry records; suppress the empty-queue claim while that set is nonempty. Historical ruled rows need no queued citer.

4. **Historical `wi_refs` will remain behaviorally live unless additional consumers are removed.**  
   **Evidence:** WI-790:70 says no code reads the historical cell. Besides readiness (`schedule.py:322`) and validation (`check_trajectory.py:938`), intake uses it to select premise-risk context (`intake.py:567–601`) and the renderer displays it (`gen_open_items.py:448`).  
   **Consequence:** removing only the gate reader leaves the old relationship influencing worker briefs, while new OIs disappear from that context. This contradicts inert history and leaves two relationship models.  
   **Fix:** rewrite `_pending_oi_lines` to join kin WIs’ typed OI `needs`; derive rendered citing WIs from the queue. Delete `open_item_wi_ref_findings`. Clarify the history promise:

   > “Historical `wi_refs` is preserved as opaque metadata. No readiness, validation, context-selection or rendering consumer derives relationships from it.”

   Passive carrier preservation is distinct from a transition reader; the carrier and converter currently map the field (`spine_carrier.py:400`; `migrate_carrier.py:227`).

5. **Dropping template `wi_refs` conflicts with the current schema-sync invariant.**  
   **Evidence:** `kitlib/spine.py:860–871` declares it in `OFFSPINE_KEYS`. Dogfood requires template keys equal schema keys and live keys be a subset (`tests/test_dogfood_sync.py:385–411`); it counts actual TOML keys, not explanatory comments (:362–367).  
   **Consequence:** removing the template key while retaining historical live keys cannot satisfy the unchanged invariant. Removing the schema key instead rejects historical rows.  
   **Fix:** specify historical-field treatment in the structural contract and amendment list. Keep one carrier with opaque historical preservation, and make the copy-ready template/schema test distinguish declared historical metadata from fields new pending rows author. Do not silently exempt the entire OI registry from sync checking.

6. **Design 5 does not cover all OI creation paths or fresh templates.**  
   **Evidence:** the shipped registry contains real pending `OI-1` and `OI-2` citing only `WI-000` (`open-items.template.toml:80–98`). Bootstrap appends pending `OI-3` and raises its watermark without creating a WI (`bootstrap.py:1600–1624`, `1667–1702`). The manifest seeds only the inert WI exemplar (`kitlib/bootstrap_manifest.py:236`).  
   **Consequence:** fresh adopters acquire hidden, uncited decisions—and, once finding 3 is fixed, a red first check. Changing intake and the hand-filing instructions is insufficient.  
   **Fix:** remove non-inert illustrative decisions from the active template, or ship valid paired work. Bootstrap must create OI-3 and its queued placeholder together, including the WI watermark. Apply the same rule to RESYNC: migrate every pending adopter OI, including those without `wi_refs`.

7. **The proposed minimum placeholder is valid, but intake does not guarantee that shape.**  
   **Evidence:** a valid `id`/filename is required (`registry.py:398–406`), so the four listed fields are insufficient literally. R-A permits an empty open Deliverable (`check_trajectory.py:1452–1465`), and a registry file satisfies R-E (:1266–1278). Claim checks the path before readiness (`integrate.py:687–704`). However, the disposition brief’s minimum omits `specref` (`adjudicate-disposition.template.md:42`), and `_draft_row` writes an omitted reference as empty (`intake.py:2016`).  
   **Consequence:** a correctly blocked handback successor can still fail R-E or claim after release.  
   **Fix:** say “`id`, valid filename, title, safety_class, OI needs and resolving specref”; `_inject_open_item` must supply the registry reference when the OI-bearing successor lacks a real one. Keep S13 warn-first; the pending edge prevents claim. The later sync rule supplies criteria before normal work proceeds.

   Also specify the registry-reference staleness join: today it clocks the entire file (`check_trajectory.py:2384–2392`). Unanchored references additionally make unrelated placeholders share a spec and trigger overlap warnings (`LLR-160`, `low-level-requirements.toml:1622`). Row-specific registry references would make that attribution clearer.

8. **Design 7 requires coordinated disposition and rendering changes, not a reason-code rename.**  
   **Evidence:** OI tokens currently yield `waiting:open-item-pending` (`schedule.py:742–744`); blocked records require attached `open_items` (:777–781), presently populated through `wi_refs` (:315–339). Status prints those attached gates (`traj_status.py:389–398`). Next-work selects only ready/waiting records and names only WI predecessors (`rendering/traj_panels.py:1197–1226`).  
   **Consequence:** moving OI edges to `blocked` alone removes them from Next-work without displaying their gates.  
   **Fix:** populate gating IDs/titles from `oi_preds`, include blocked records in Next-work, and reuse the same records for status. Preserve ordinary WI waiting reasons when a row has both dependency types. Missing OIs must remain unsatisfied and receive the existing dangling-edge ERROR (`schedule.py:475–478`; `check_trajectory.py:824–830`).

9. **The spec contains stale or broader interpretations that need reconciling.**  
   **Evidence:** WI-790:170 still says “sync warning”; :176 says ERROR. :130 equates leaving pending with leaving the page, although design 4 also removes items when their sole citer leaves queued. :138 names cancellation/restructuring as exemptions; :188 exempts every terminal state, including partial/done (`check_trajectory.py:396`). :212–214 promises readiness after ruling, while :228–237 permits a red sync check after that release.  
   **Consequence:** the builder must choose scope and timing rules.  
   **Fix:** replace “sync warning” with “sync ERROR”; define the trigger by registry state, independently of page membership; state the terminal set explicitly. State that readiness is satisfied by the ruling while the sync check can still reject the tree—claim currently checks readiness, not sync (`integrate.py:695–704`). Preserve normal R-A terminal records and lineage obligations. For criteria, read **raw spec text**: `done_when_section` does not open files; Deliverable parsing alone clips Context (`registry.py:374–375`). The probe confirmed Done-when after Context is readable without violating R-A.

Design-point assessment: **1** buildable using the existing splitter; **2** buildable as a recorder/reviewer obligation; **3** needs findings 4–5; **4** needs finding 3; **5** needs findings 6–7; **6** is not sufficiently defined; **7** needs finding 8; **8** covers this repo’s three pending OIs, but needs the broader adopter/bootstrap migration above.

**OWNER QUESTIONS:**

1. **Must a pure release gate change acceptance criteria?** OI-98 concerns a person’s act (`docs/requirements/open-items.toml:3679–3683`); WI-684 already specifies the observation to perform (`docs/work/queued/WI-684-re-judge-tc-036-no-result-rec.md:15–25`). Options: require an explicit ruling-confirmation criterion; or distinguish release-only gates from decisions changing scope. **Recommendation:** require the confirmation criterion, preserving the confirmed universal rule without adding another gate kind.

2. **What should the owner see when a pending OI has no queued citer?** Options: retain queued-only decision cards plus an integrity notice; or widen decision visibility to draft/deferred citations. **Recommendation:** queued-only cards plus the named integrity notice, matching design 4 while making invalid state visible.

3. **Is full Git history a prerequisite for this ERROR?** Options: require it and fail explicitly when necessary history is missing; or redesign around durable ruling/update records that are verifiable without history. **Recommendation:** require history for this design, update shipped CI, and support uncommitted candidate trees through the same comparison engine. Never inherit the advisory checker’s silent skip.

**MISSING ROWS / FILES:**

- **Additional definite row changes:** IF-264/IF-265 (`interfaces.toml:2356–2374`); IF-164 (:715–723); LLR-118/TC-123 (“every pending row”: `low-level-requirements.toml:1178`, `test-cases.toml:1203`); LLR-153/TC-147 for intake context/mint behavior (:1538, :1459).
- **Coverage to extend:** LLR-010/TC-010 for green scaffolds (`low-level-requirements.toml:106`; `test-cases.toml:103`). New traced coverage is needed for the unconditional sync ERROR and uncited-pending ERROR. WI-205 itself records a never-gating advisory, not a suitable requirement for this new ERROR (`docs/archive/work/complete/WI-205-backlog-staleness-warn-warn-tier-check.md:11`).
- **Additional implementation/files:** `kitlib/spine.py`, `spine_carrier.py`, `migrate_carrier.py`, intake’s `_pending_oi_lines`, `bootstrap.py`, shipped `ci/check.yml`, structural-sync tests, and both copies of the WI exemplar guidance.
- **Additional test amendments:** `tests/test_prompts.py:43–45`; `test_intake.py:1413–1440`, `1484`, `1756–1764`; `test_schedule.py:183`; `test_open_item_readiness.py`; `test_gen_open_items.py`; `test_traj_status.py`; `test_bootstrap.py`; `test_dogfood_sync.py`; `test_migrate_carrier.py:687–700`; staleness fixtures in `test_trajectory_staged.py` and `test_wi_folder_loaders.py`.
- Add explicit cases for no WIs, draft/deferred-only citations, reopen/re-rule, newly created ruled citations, token removal, cosmetic/deleted Done-when, renamed specs, staged/working-tree rulings, composed merges, shallow/missing history and fresh non-Python scaffolds. Regenerate derived reports after adjudicated row changes; preserve archived ruling history.