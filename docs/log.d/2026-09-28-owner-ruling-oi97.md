## 2026-09-28 — The owner rules OI-97 (a): a joint-delivery class for requirements

After the breakdown of the nine unclassified requirements, the owner took the
recommendation. Their words are quoted in the row's `decision` cell in
[../requirements/open-items.toml](../requirements/open-items.toml).

**What it sets in motion.** A requirement that is one link of a need several
requirements deliver together names those siblings in a `delivered_with`
cell and is classified joint. **WI-723** amends SR-193, LLR-222, LLR-223,
TC-220 and TC-222 in place, builds the class, and writes the cell on SR-015,
SR-024, SR-033, SR-111, SR-129, SR-174, SR-177, SR-223 and SR-225. Their
attestation re-opens, so the next spine-acts batch judges them.

**The owner's directions.**

- A joint requirement does not inherit its siblings' assumptions: each
  assumption stays coupled to the requirements that cite it. Citations are
  already many-to-many, so an assumption serving several requirements needs
  nothing new.
- An adjudicator checks that siblings and their assumptions line up. This
  goes on the `spine-authoring` question list, not into a rule.
- Changing `delivered_with` re-opens attestation. The owner framed this as a
  trial, to back off if it causes too much iteration.

**The owner's unease, answered as a check.** SRs are meant to be
boundary-driven. A joint row still states a behaviour at a boundary; joint
delivery only describes how the need's argument is assembled. A row whose
output crosses no boundary and only feeds a sibling is a design decision, and
belongs at LLR. The adjudicator's list gains that check beside the alignment
one.

Deferred open items: none.
