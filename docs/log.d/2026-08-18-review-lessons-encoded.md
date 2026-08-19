## 2026-08-18 — the four durable lessons of the review round get one home each

The round's 23 applied findings were mostly mechanized in the same commit
(`cfbcab9d`) — a test or a detector arm now holds them, and prose about them
would be a second wording of a rule a check already owns. Four lessons had **no
mechanical home at all** and were still unwritten. This change encodes only
those four, each in exactly one place, chosen by the enforcement hierarchy
(Harness > Test > Reviewer > Prose) and by whether the lesson is universal
(shipped layer) or about maintaining this kit (meta-repo layer).

**1. Measure the enforcer; a detector is a worklist.** The round's central
failure was circular: a sweep was graded by the detector co-designed with it,
and that detector's false-positive rate was *reported* ("0 of 319") without ever
being *measured* — it was 100% on one arm. The cleanup then stopped when the
detector went quiet and left 33 framed cells behind. Both halves are universal,
so they land in the **shipped** discipline they belong to:
`project-trajectory/PROCESS_OPTIONS.md` "Enforcement audit — which file enforces
this rule tomorrow?", whose framing was already half the question. Two sentences,
placed before the existing honesty bar: a new or widened check has its
false-positive rate measured against the live corpus, with negative cases pinning
the known hazards, before any claim is made about what it found; and a detector's
vocabulary is always narrower than the rule it stands for, so a cleanup that
stops when the checker goes quiet has proved only that the checker is quiet.

**2. A mandated token must mean something downstream.** The `13v` waiver marker
named *this repo's* log decision `2026-08-13v`, so every adopter was instructed
to write, into their own registry cell, a citation of a ruling they can never
read — and the marker was itself a decision id, which the provenance rule bans
from that very cell. That is a rule about **editing the kit**, not about a
downstream project's method, so it extends the existing *Templates must stay
copy-ready* bullet in `CLAUDE.md` rather than minting a new always-on rule.

**3. A spine rule must name every tier it governs.** Measured twice in one day:
the artifact-voice rule shipped governing `SR` alone and the provenance rule
governing `SR`/`LLR`/`TC` — both omitted `SN`, the tier a stakeholder actually
reads, and both had to be extended to the need tier afterwards. It goes in the
on-demand `spine-authoring` skill's *Known failure modes*, which is the
adjudicator's per-tier question list and already carries one-line entries of
exactly this shape. All three materialized copies stay byte-identical.

**4. The resync worklist carries the same caution.** The two sweep-class RESYNC
entries (artifact-voice, provenance) tell an adopter to run `trace.py` and
rewrite what it reports — which walks them into the identical circularity. Each
gains one sentence at the step where the operator reads the detector: it is a
worklist, not a definition of done; the checker's vocabulary is narrower than the
rule, so stop when the *cells* are right. No new entry, and
`skills/downstream-resync/SKILL.md` is untouched — it is a deliberate pure
router.

**Deliberately NOT written.** Nothing was added to `AGENTS.template.md` (47 bytes
of headroom, parked at its cap, and these are authoring-time rules rather than
session-time ones) or to `PROCESS.md` (none of the four is a process rule for a
downstream project's method). The "never report a green you didn't produce" rule
was left exactly as it stands — its wording was converged to one form earlier
today, and restating it here would re-fragment it.

**Enforcement-audit bookkeeping.** Three edits to `docs/enforcement-audit.md`,
the register of which file holds which rule:

- The artifact-naming row named only the requirement tier — the register was
  itself an instance of lesson 3. Corrected to "a **need or** requirement cell",
  with the `trace_text.sn_artifact_advisories` arm and its three deliberate
  narrowings (acceptance-only, wider extension list, no shared census) named.
- **New row** for the provenance rule (all four spine tiers, reason cells
  included). It had no row at all: `trace_text.provenance_advisories` plus the
  `if_note_advisories`/`off_spine_advisories` siblings, the unchanged strict
  gating rule, the token-scoped `docs/provenance-allow`, and the two tests that
  hold it (`test_the_provenance_allow_file_is_read_token_scoped`,
  `test_this_repos_own_provenance_allow_entries_all_still_bite`). Honest residue
  recorded: the token vocabulary is fixed, and whether the durable reason
  survived the frame's deletion is the reviewer's.
- **New row** for lesson 1 itself, classed **Reviewer (accepted gap) + Test
  (negative cases only)** — nothing mechanical can measure a detector's error
  rate against a corpus with no labelled ground truth, so the rate stays
  Reviewer and is recorded as a stated reason rather than implied as covered.

No rows were added for M1 (the flows gate — `check_flows.py` already has a row,
and the fix hardened the enforcer rather than adding a rule) or for the byte
caps (already a row; the round widened its enforcer, not its rule).

**Byte deltas.**

```
CLAUDE.md                                              6,805 -> 6,981  (+176; cap 8,500, 1,519 free / 18%)
project-trajectory/PROCESS_OPTIONS.md                173,374 -> 173,985 (+611; watched)
project-trajectory/skills/byte-budget-guard/SKILL.md   4,803 -> 4,882  (+79;  cap 5,000, 118 free / 2.4%)
project-trajectory/AGENTS.template.md                  9,953 -> 9,953  (unchanged)
project-trajectory/PROCESS.md                         82,511 -> 82,511 (unchanged)
```

The guard's own growth was paid for in the same edit, per its step 2: the
doc-size parenthetical was tightened by 20 bytes and the CLAUDE.md row's derived
headroom figure dropped (the row already states cap and baseline). Its
parked-at-the-cap note read "every other capped file holds 7–20%", which the
guard's own new size falsified — re-measured to 2–18%. Both changed rows plus
the guard's own were re-stamped replace-style across all three copies.

**Verification.**

```
$ ./.venv/bin/python -m pytest -q tests/test_dogfood_sync.py tests/test_skills_sync.py \
    tests/test_rule_sync.py tests/test_bootstrap.py tests/test_resync_pack.py tests/test_check_docs.py
218 passed, 1 skipped in 64.07s

$ ./.venv/bin/python -m pytest -q tests/test_bootstrap.py -k "byte_caps or size_budget"
2 passed, 53 deselected

$ check_docs.py --stale   -> OK - 919 doc(s), 1323 intra-repo link(s), 0 broken
$ check_vocab.py          -> clean (420 live authored file(s); no retired gate tags)
$ gen_skills_index.py --check / --check-agents -> index fresh; 14 per-agent copies match
```

**Finding surfaced, not fixed (out of scope).** `tests/test_bootstrap.py`'s
comment above `BYTE_CAPS` still justifies the caps with the 60-day figures
("shrank 14% … grew 263% and 1,092%") that
`docs/knowledge/instruction-file-adherence.md` **withdrew as unreproducible**
earlier the same day. A withdrawn measurement restated as standing fact in a
second home is the paraphrase-drift class the knowledge pack names; the comment
should cite the pack rather than carry its own copy of the numbers.
