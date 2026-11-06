# WI-993 checkpoint sitting at 73e7aee

## amendment

This sitting re-sits the whole set after sitting 007 returned LLR-153. The other six rows carry the same JUDGED-TEXT identities that sitting 007 ruled, and their text has not moved since. Their rulings stand here on 007's reasons. Since 007, the lane changed one cell, LLR-153 `detail`. I confirmed with a word diff from `1a00dcd6d` to `73e7aee` that nothing else in the design registry moved. The lane also renamed 007's `## Dispositions` heading to `## Answered in the lane`, so no successor is minted for a return the lane has already answered. It recorded this as wi-993 D-007.

Checks I ran at HEAD 73e7aee:
- `python -m pytest -q -n 4 -p no:cacheprovider tests/test_intake_held_act.py "tests/test_intake.py::test_the_oi_mint_refuses_on_a_non_toml_registry" tests/test_open_item_queue.py tests/test_open_item_readiness.py tests/test_gen_open_items.py`: **92 passed in 59.94s**, with no failures, errors or skips reported.
- `trace.py --strict` exits 0.
- I read the mint path to confirm the new refusal sentence holds for both routes it names. The trigger (d) owner item and a drafted `[open_item]` table both file through one open-item mint. That mint refuses on a non-TOML carrier, and its message names the conversion and the sweep. Every trigger's drafts, the amendment row included, go into one all-or-nothing mint. So a refusal writes nothing, the merge stands, and the earlier amendment row is withheld with the rest.

All seven rows changed MEANING, and I would bless all seven.

**Consequence for the act:**
- No row is left unblessed.
- The design registry (LLR-118, LLR-153, LLR-299, LLR-364) and the test-case registry (TC-123, TC-147, TC-314) can both be re-attested from this verdict.
- No row here sits on a rung held for the owner.

- [MEANING+BLESS] LLR-118 Detail -> before: the owner page briefs pending items cited by queued work items beside those queued rows, and its integrity notice names pending items that no queued row cites -> after: the same with "queued or claimed" for both the cards and the notice -> not the same: a claimed citer now turns a notice into a card. Unchanged since sitting 007 blessed it.
  - It imports the queue from the one projection.
  - It matches IF-073 v2 and LLR-299.
  - It adds no name.
  - TC-123 holds the claimed case.
- [MEANING+BLESS] TC-123 Method -> before: briefs, notice and snapshot for queued citers -> after: the same for queued or claimed citers, plus a claimed citer's card and Blocked line -> not the same: a new case and a wider population. Unchanged since 007. Its claimed-citer evidence exists and passes.
- [MEANING+BLESS] LLR-299 Detail -> before: a pending item that no queued item cites is an error, and a non-queued citer does not count -> after: the error applies only when no queued or claimed item cites it, and a citer that is neither does not count -> not the same: a claimed-only citer now clears an error that the old text required. Unchanged since 007. It decomposes SR-148's surfacing of held work, and TC-314 holds every arm.
- [MEANING+BLESS] TC-314 Expected, Method -> before: queued citers, with only deferred named as not counting -> after: queued or claimed citers clear the error and appear as cards, while draft, deferred and closed citers do not -> not the same: the expected condition and the negative set both changed. Unchanged since 007. The parametrized negatives (draft, deferred, cancelled) and the claimed-citer cases pass.
- [MEANING+BLESS] LLR-153 Detail -> before: three triggers, with trigger (a) minting every amended approved record except those LLR-364 settles -> after: four triggers. The changes:
  - Trigger (d) mints one queued owner row and one pending item per landing per registry. It applies to an accepted, held-rung MEANING ruling, blessed or not, on a row that is unanchored and at its bound text or removed. The command names no verdict.
  - The item's option (a) directs the owner to name any other unanchored row of the registry.
  - Every other non-refusing state writes nothing, and a left-over row stays on the amendment row.
  - Where a landing owes an open item and the open-items registry is not TOML, the mint refuses by naming the carrier. It writes nothing, the amendment row included, and the merge stands. Recovery is conversion, then a sweep.
  - Trigger (a) excludes the carried rows.

  -> not the same: a new trigger, a narrower trigger (a) and a stated refusal. Ready to bless. Both of sitting 007's findings are answered:
  - **The refusal is stated.** It covers both item-filing routes, which share one mint. `test_a_non_toml_registry_refuses_and_the_merge_stands` and `test_the_oi_mint_refuses_on_a_non_toml_registry` hold it for those two routes, and TC-147 states it.
  - **The actor is named.** The item's option (a) directs the owner, which matches the option text the mint writes.

  007's optional point is also taken: "Those rows leave the amendment row" is gone, and the carry is stated once, in trigger (a)'s exclusion. LLR-364 keeps the drift-side statement.

  Read upward: it decomposes SR-228, where a meaning change on a held rung stays the owner's decision and the owner's act needs no CLARITY verdict, and SR-174's single minting route. It adds no implementation name, and no `shall`.
- [MEANING+BLESS] LLR-364 Detail, Rationale -> before: the trunk mint excludes only records that a re-attesting act in the range settled -> after: the settled filter excludes the same records, an owner row carries a held-MEANING record out of the amendment row, and the rationale says such a record is moved, not hidden, because it stays on the approval brief as drift and the owner's item names it -> not the same: a record the old text minted now leaves the amendment row. Unchanged since 007. This is SR-178's drift-side statement. LLR-153's edit means it now overlaps LLR-153 in one clause only, and `test_a_held_row_leaves_the_amendment_row_beside_a_released_one` passes.
- [MEANING+BLESS] TC-147 Method -> before: the intake mint arms, with no held-act trigger -> after: the same plus the held-act clause. It covers the per-landing and per-registry mint, blessed or not, and retired rows. The minted command runs with no ledger verdict. It covers the widened act, the non-mint states, the non-TOML refusal and recovery, the latest accepted verdict deciding, and carried rows leaving the amendment row -> not the same: many new arms. Unchanged since 007. Every clause has a passing case, and it already states the refusal that LLR-153 now carries, so the two rows agree.

VERDICT: MEANING rows=7

SITTING: JUDGED kinds=amendment
