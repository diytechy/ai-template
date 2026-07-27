# 124-REVIEW-A — adversarial review of the provenance cleanup's 48 edited cells

**Trigger:** the owner, mid-attestation, asked whether an adversarial review had
been run against the prose changes, saying they would re-attest but were not
going through 44 rows with a fine-tooth comb. It had **not** — only a
self-review. That is the weakest possible basis for a signature, so this was
dispatched before the sitting continued.

**Critic:** a fresh **OpenAI/`codex`** session — family-heterogeneous (the editor
was Claude/Anthropic). Sandbox held **only** the 48 BEFORE/AFTER pairs and the
invariant being claimed. No repo access, no commit message, no rationale, no
self-assessment: the critic could not see who made the edit or why, only whether
the AFTER still says what the BEFORE said.

**Verdict:** `CHANGES-REQUESTED findings=30`.

**Disposition: 5 confirmed, 2 found independently by the editor, 23 re-scoped.**
The count is not the number of defects. The critic was given the claim *"only
provenance was removed"* and correctly noticed that **other kinds of provenance
survive** — thread ids, review numbers, ruling dates, discovery chronology. That
is an argument that the RULE is too narrow, not that this edit broke anything,
and it is a real argument: it is filed as its own work item rather than acted on
inside an attestation window. Rewriting 23 more cells on a critic's say-so, in
rows a human is mid-way through blessing, would be exactly the drive-by this
whole thread exists to prevent.

---

## Confirmed and fixed

### F1 — MAJOR (pair 8) · `SR-046` Rationale · an orphaned cross-reference

Removing the `process.md` citation left a later bare `§7` with no antecedent:
*"…which previously rode §7 prose only."* The reader can no longer resolve what
`§7` is a section OF. **Fixed:** *"…which previously existed only as process
prose."* Caught by the critic, missed by me — my sweep checked each removal site
and never asked what the removal orphaned **elsewhere in the same cell**.

### F2 — BLOCKER (pair 39) · `LLR-120` Detail · a measurement made unreproducible

*"ONE wire rides within the router's own 3px clearance of `WI-043`'s edge"* became
*"…of a neighbouring node box's edge"*. The id was **not** attribution — it named
the exact rendered node in a specific measurement, and the paraphrase makes the
observation impossible to reproduce.

This is precisely the known cost I flagged and accepted when writing the rule,
which is worth noting: **I predicted this failure, judged it acceptable, and an
independent reader called it a BLOCKER.** Predicting a cost does not discharge it.

**Fixed by scoping rather than paraphrasing.** The row now states the fact it
genuinely owns — 264 wires, 0 through a box, and that `_detour_d` exhausting its
lane candidates is a *reachable* state rather than theoretical — and explicitly
does **not** claim the one-off datum. The grazing node's identity lives in the
open work item, which is where a specific id belongs and where the rule does not
apply.

### F3 — BLOCKER (pair 46) · `TC-120` Method · a citation that cites nothing

*"owned by the cited `WI-305` tests"* → *"owned by the cited next-work tests"*.
The word **"cited"** survived with nothing to point at, so test ownership stopped
being resolvable. **Fixed:** *"owned by the next-work tests named in this row's
Evidence"* — a pointer to a column that actually lists them.

### F4 — BLOCKER (pair 48) · `TC-124` Parameters · fixture lost its only identity

*"the 109-character `WI-308` clause"* → *"the 109-character clause the critic
read"*. The id was carrying the fixture's sole distinguishing identity; the
replacement is both ambiguous **and still historical**. **Fixed:** named the
actual constant, `_NW_LONG`.

### F5 — MINOR (pair 47) · `TC-124` Method · same defect, same fix

---

## Found by the editor's own second pass, not by the critic

Two defects the review did not report, caught by a word-level delta run as a
deliberately different instrument from the sentence read-through:

- **`SR-050`** — the replacement produced a tautology: *"downgrades verification
  to Critique **(the Critique verification vocabulary)**"*. The parenthetical only
  ever pointed at where the vocabulary was defined. Removed.
- **`LLR-101` / `LLR-112` / `LLR-113`** — *"and delivered by WI-313: every
  element…"* became *"and delivered: every element…"*, leaving a participle with
  no subject. Now reads *"…under the (f) decomposition ruling: every element…"*.

Worth recording because it cuts against the obvious lesson: the independent
critic was necessary and **not sufficient**. Two instruments found disjoint sets.

---

## Re-scoped, not fixed: the rule is narrower than "provenance"

23 findings say a variant of *"you removed the work-item id but left
`IMPROVEMENT_PLAN.md Thread 53` / `119-CRITIQUE` / `the 2026-07-26 owner ruling`
/ `REWORKED same day after adversarial review`."*

The critic is right that these are history rather than specification. It is also
right that a row saying *"REWORKED same day after adversarial review refuted two
claims"* is telling a reader about the edit, not the system. But:

- **Critique and rubric references were explicitly ruled legitimate** for a
  `Verification=Critique` row — the critique *is* the acceptance instrument, so
  naming it is what makes the row verifiable.
- **Some dated items are measurements, not stamps** — the critic itself drew this
  line correctly, clearing *"137 rows / ~60 files by 2026-07-20"* as a snapshot.
- Acting on the rest means **rewriting 23 more cells mid-sitting**, in rows the
  owner is actively attesting.

Filed as **WI-328** so the question survives with its evidence. Escalating it in
prose and calling that a decision is the failure mode this repo has already
recorded three times.

---

## What the critic checked and cleared

It swept all 48 pairs clause by clause and cleared the rest, and it correctly
declined to flag script names, artifact paths, rubric paths, sibling
`SR`/`LLR`/`TC`/`SN` ids, CSS selectors, fixture names and concrete
measurements — the exact negative half the rule depends on. It also stated its
own limit plainly: it judged textual equivalence only, not whether the system
implements the claims.
