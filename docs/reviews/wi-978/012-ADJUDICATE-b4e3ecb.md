# WI-978 dispute sitting at b4e3ecb

DISPUTE: findings=F1

## F1: a refresh moves the lane's merge base past the owner's landing

**The claim.** Lane WI-401 holds the reservation SR-007, but drafts SR-006. WI-402 owns SR-006 and lands it first. The dispatcher's drain then refreshes WI-401. Because the reserved-ids rung (`integrate._reserved_id_refusal`) judges only the ids the tip holds that the lane's merge base does not, SR-006 is no longer "added". So WI-401 lands, against SR-174's "a landing that adds a registry identity outside its own work item's reservation is refused".

**Reproduced at this range, both ways.** I used the landing suite's own fixtures (`tests/test_id_landing.py` `_trunk`/`_close`, a planted carrier holding `SR 6-6 (WI-402)` and `SR 7-7 (WI-401)`, and the real `integrate.refresh` and `integrate.integrate_one`). I ran it with the loop-provenance variable unset, so that the trailer rung did not answer first.
- **WI-401's SR-006 row byte-identical to the owner's**, the reviewer's case, whose fixture writes the same minimal `_rows` text in both lanes:
  - before the owner lands, the slot refuses: "SR-006 is added outside every reservation of WI-401";
  - after the owner lands and the lane refreshes, the slot lands it (`None`).
- **WI-401's SR-006 row different from the owner's**, the case two lanes actually drafting the same number produce:
  - the refresh is refused: "merging trunk ... CONFLICTS; resolve it on the branch";
  - the lane parks, and nothing merges.

**Why that is no defect.** The reproduction holds mechanically, but what it admits is not the collision the finding describes.
- **An identical row.** WI-401's landing contributes nothing in the SR space. After it lands, trunk holds exactly one SR-006, the owner's, unchanged. No identity is reissued, and no second meaning hides behind one number. That is the harm SR-174 and the landing table exist to prevent. The rung's attribution is right: the tip's SR-006 is trunk's row, not the lane's. That is also how the legitimate case reads, where a lane stacked on the owner's branch carries the owner's row. The rung cannot tell that case apart from "drafted the same bytes", and it must not refuse it.
- **A different row.** A second lane's real draft under the same number is different text. The refresh then fails closed at the merge, before any admission is asked.
- **The hand resolution.** The refused refresh hands the conflict to a resolver. The registries row of the recipes directs that resolver to "judge same-row conflicts" and "keep independent changes from both sides". A resolution that overwrote the owner's landed row with the lane's text would be that hand act done wrong, not the route the finding reproduces. It changes an existing row rather than adding an identity, and §6 places it outside the promise.

So no supported workflow reaches a landing that reissues an identity outside its reservation through this path.

The finding's suggested redesign would move attribution from the tree's content to the lane's history. That would refuse a stacked lane carrying the owner's own row, and it is not owed for a scenario whose only reachable form is harmless.

RULING: F1 DISMISS refuted at this range a lane's different SR-006 row conflicts at the refresh and the lane parks (driven: refresh REFUSED, nothing merged), and only a row byte-identical to the owner's landed row survives the refresh, which reissues nothing since trunk then holds one SR-006 with the owner's text unchanged, so no landing adds an identity outside its own reservation
