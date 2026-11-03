# WI-978 checkpoint sitting at d3cfb73

## amendment

Two approved rows moved against their copies (SR-174 at dc7e2a5cf, TC-158 at 9a5952fb0). They carry WI-978's widening: identity allocation now covers the registry identities parallel lanes author, drawn from one shared reservation record, besides work items.

What I checked:
- **The text.** The live cells match the brief.
- **The lint.** `trace.py --strict` exits 0. Its only advisory on these rows is SR-174's "no Form", which nearly every SR carries.
- **The tests.** `pytest tests/test_id_carrier.py tests/test_id_watermark.py`: 112 passed, with TC-158's added cases among them.
- **Keep or mint.** The keep is argued as PROCESS.md §4 asks. The spirit is unchanged (one allocation per identity, counted from the high-water mark, never re-issued). Every findable user is cross-referenced in the Rationale (LLR-153, LLR-154, TC-147, TC-148, TC-158, the SR-170 and SR-173 rationales), each reading the unchanged work-item half. Minting would only re-point TC-158.

Both rows are MEANING, and I would bless both.

- [MEANING+BLESS] SR-174 Requirement, AcceptanceCriteria, Rationale, Title -> before: allocate each work-item identity at most once, so no two concurrent actors share one and a freed one is never re-issued; acceptance: no shared work-item id, no re-issue, counting from the recorded mark -> after: allocate each identity the content mints at most once. Work items are minted on the integration branch alone, and lane-authored registry identities are drawn from one shared reservation record, with the same two consequences. The acceptance adds disjoint ranges from any bases, refusal before landing of an added identity outside its work item's reservation, and a mark that rises only by allocation, ruled correction or recorded reservation. The Rationale adds the SN-027 contribution and the keep-or-mint cross-reference -> not the same: the scope widens from work items to every lane-authored identity, and three acceptance clauses are added. Ready to bless:
  - **One obligation.** The Requirement is the spec's own target text. I read its declarative sentences as the one `shall`'s two domains and their means (where each kind of identity is minted), not as independent obligations. Each traces to one obligation, "allocated at most once".
  - **The AC mints nothing new.** The reservation concept the acceptance tests is introduced in the Requirement, so the acceptance mints no obligation the Requirement lacks.
  - **Naming.** It names no file.
  - **The derived constraint is recorded.** "One shared reservation record" is an SN-027-derived constraint, argued in the Rationale.
- [MEANING+BLESS] TC-158 Expected, Method -> before: the watermark rules (above-mark, missing space, malformed line, absent file, lowered and hand-raised mark), deleted-row headroom, and the mint's next id -> after: the same verbatim, plus a rise covered by a reservation record passes, a rise above every record fails, an altered or deleted committed record fails, and a bump or correction keeps every record -> not the same: verification arms are added. Ready to bless:
  - The additions name no code. The kept text's names are approved text, kept verbatim.
  - Each new arm has an evidence node that exists and passes.

VERDICT: MEANING rows=2

## first-approval

Four new rows await a first approval under SR-174: LLR-362 and its TC-401 (allocation), and LLR-363 and its TC-402 (landing admission). The approved chain rows are evidence only.

**Stopping boundary.** SR-174's lane half splits into two independent decisions:
- **LLR-362, allocation:** who writes the record and how a range is chosen.
- **LLR-363, admission:** what a landing accepts against that record.

Either can fail while the other holds, and further splitting (per argument case, per route adapter) would restate one decision over different inputs. The work-item half stays with LLR-153 and LLR-154, unchanged. Each LLR has one TC, and TC-158 holds the record-history rules on the integrity floor.

- [RETURN] LLR-362 -> the carrier holds the watermark for every lane-minted space; a reservation moves it by compare-and-swap and appends one record per space (range and work item); only a reservation writes a record and only a fold copies one; committed records are unchanged across every parent; every writer keeps the records -> the arms map makes this row SR-174's allocation half, and its traced symbols (`plan_reservation`, `fold`, `reserve`, `_mark_history_findings`, the reserve verb) implement much more than the text states. TC-401 and TC-158 verify that more -> not ready: the row omits the allocation rule it exists to state, so a builder could satisfy it while breaking SR-174's acceptance. Five gaps:
  - **Where a range starts.** The code starts each range "one above the larger of the carrier's mark and trunk's committed mark", so a ruled correction raises the floor. The row never says so, nor that successive and concurrent reservations are therefore disjoint. That is SR-174's "reservations in sequence or at once, from any bases, receive disjoint ranges".
  - **The refusals.** It does not say that a lost compare-and-swap, or any refused reserve argument, writes nothing.
  - **The first use.** It does not say that the first use creates the carrier from the integration branch's committed watermark.
  - **The fold.** It does not say what a fold yields: each space's maximum, the union of records, and the basis from the receiving tree's live ids.
  - **The rise rule.** It does not state SR-174's "a mark rises only by allocation, by a ruled correction, or by a recorded reservation". This row is that rule's home: its symbols carry `_mark_history_findings` and its TestRefs carry TC-158, yet its Detail never mentions a rise.

  Also, "the carrier" is used and never said to be a shared ref apart from any lane's branch. Define it once.
- [RETURN] TC-401 -> carrier unit and repository cases: every reserve refusal writes nothing, sequential and stale-base reservations are disjoint, a lost swap writes nothing, and a fold of clean and conflicted watermarks yields maximum marks and the deduplicated record union -> its 9 evidence entries exist, and the unit file passes. It verifies arms LLR-362 does not yet state -> not ready:
  - **Parent-first.** Its parent LLR-362 returns, and its arms must be re-read against LLR-362's restated text.
  - **A cited arm is unstated.** Its Expected omits the first-use seeding that `test_first_reservation_seeds_the_carrier_from_trunk` drives. Add it beside the restated LLR-362.
- [APPROVE] LLR-363 -> a code-only landing passes. A landing passes only when every added carrier-space identity lies in a record naming its claimed work item. It refuses, before landing:
  - an added identity outside such a record;
  - added identities under an unreadable claim;
  - a missing carrier;
  - a landing-only record;
  - an added identity a retirement record in the landing or its parent names, inside a reservation or out (sitting 008's FIX), naming the identity and the record.

  "Added" is held by the tip and not by its merge base, and a hand landing also judges what its staged tree adds over the integration branch's tip. Each route carries the carrier fold it read, and a watermark-only refresh conflict resolves to the fold -> it is closed over the spec's landing table and both callers, and matches the code (`landing_lines`, `_retired_lines`, `_reserved_id_refusal`, the squash step). Sitting 012's dismissal stands on the "merge base" definition stated here -> ready:
  - It names only the watermark, a shipped artifact.
  - Its refusals name what they refuse.
  - TC-402 verifies every arm.
- [APPROVE] TC-402 -> real merge-slot and hand-squash cases for every landing-table outcome: a stale-base lane minting another lane's number, a code-only lane after trunk retires an id, a reserved identity authored, retired and re-authored refused on both routes naming its record, a carrier moved after a lane's fold carried by each route, and a watermark-only refresh conflict -> its 25 evidence nodes exist and cover each arm on both callers, including sitting 008's regression -> ready. It is closed over LLR-363, and its Method names no code.

**What the act needs.**
- The rung is released, so the later act turn re-attests SR-174 and TC-158 and flips LLR-363 and TC-402.
- LLR-362 and TC-401 stay Drafted and re-sit together.
- Nothing is held for the owner.

### Returns answered in the lane (re-sat and approved by sitting 014-ADJUDICATE-e934cf2)

These are Done-when items of this row ("The carrier" items, and "SR-174 ... two new LLRs ... carry the target meaning"), so they are answered in this lane, not by a minted successor:

- **LLR-362 Detail:**
  - define the carrier (the shared ref holding the lane-minted spaces' watermark, apart from any lane's branch);
  - state that each range starts one above the larger of the carrier's mark and the integration branch's committed mark, so sequential and concurrent reservations from any bases are disjoint;
  - state that a lost compare-and-swap or a refused reserve argument writes nothing;
  - state that the first use creates the carrier from the integration branch's committed watermark;
  - state that a fold yields each space's maximum, the union of records and the receiving tree's basis;
  - state that a mark rises only by allocation, a ruled correction, or a covering reservation record.
- **TC-401 Expected:** add first-use seeding, and re-read its arms against the restated LLR-362.

OUTCOME: RETURN rows=4

SITTING: JUDGED kinds=amendment;first-approval
