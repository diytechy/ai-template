## 2026-08-20 — The pre-sign readability sweep: 47 spine cells condensed across four registries, every edit reviewed twice

**The directive.** The owner (2026-08-20) asked for an independent review of
the spine text they are about to approve, for condensation and readability,
with the session judging and applying the suggestions it approves. Four
reviewer agents ran on the Opus model the harness routes (requested as "Opus
4.6"; the harness exposes one Opus tier), one per registry, each capped at
its twelve highest-value suggestions and bounded by the house rules: meaning
never changes, one shall per SR, EARS conformance, condition-voice
acceptance, artifact-class voice, rationale carries the durable reason not
chronology, no provenance added, no ids/fields/statuses/-000 rows touched.

**The judgment.** 48 suggestions returned; **47 applied, 1 rejected, 1
applied modified**. Byte-exact before/after for every cell is this commit's
own diff on the four registry files — deliberately not restated here.

- **Rejected:** SN-027 `acceptance`'s trailing "Spec of record" pointer
  (`docs/concurrency-restructure.md` + the archived dispatch spec). Not a
  wording-only cut: that citation is entangled with the held SN-027
  allow-file question (recorded in OI-32's recommendation) and is named in
  the archive README as a reason `concurrency-restructure.md` stays at the
  docs root. Its removal is a decision, not a condensation.
- **Modified:** SR-167 `rationale` — the suggestion deleted a LIVE pending
  sitting act along with the chronology ("LLR-014.sr_refs and TC-014.verifies
  are deliberately NOT re-pointed here ... the sitting's act"). The
  chronology went; the pending-act sentence stays, reworded as "One act is
  deliberately still owed".
- **Verified before accepting:** the two SN cross-cell redundancy claims
  (SN-029's dropped acceptance tail is verbatim in its `need` cell; SN-034's
  dropped SN-025 boundary sentence is stated in SN-025's `need` cell) and
  LLR-032's new factual claim (the onboard/dev-setup templates live under
  `project-trajectory/scripts/` — confirmed by listing).

**What the 47 edits are, by class:**

- **SN (11 of 12 applied):** SN-029 acceptance semicolon-chain → sentences
  (duplicate tail dropped, verified redundant) and why-cell past-tense
  history → standing argument; SN-034 duplicate enumeration + cross-row
  chronology dropped (verified redundant); SN-005 the two non-claims
  collected into one closing sentence; SN-006/SN-007/SN-025 review-history
  and Thread/pointer chronology dropped; SN-008 the twice-stated
  never-by-hue rule stated once; SN-026 one sentence split; SN-027 why-cell
  meta-comment folded; SN-028 "checked contract rather than a convention".
- **SR (12 applied):** the two worst offenders by the 2026-08-19 review's
  measure — SR-140 rationale (the abandoned on-row-anchor narrative, the
  reversed-sign changelog, the adversarial-read finding, a plan-doc citation
  and an orphans-census all removed; every durable reason kept) and SR-148
  rationale (the SR-141/153/059 merge chronology and census-F5 references
  removed; the one-home invariant, the rejected alternative and the
  migrated-repo argument kept, `Fan-out re-stamp:` marker preserved with a
  self-contained reason) — plus SR-148's requirement REORDERED (no clause
  added or removed, still one shall: the 220-char negative parenthetical
  moved out of the subject position into the trailing qualifier list);
  SR-167/SR-166/SR-156/SR-173/SR-179/SR-053/SR-049/SR-046/SR-015 rationales
  each losing their edit-history/citation passages while the durable
  partition or reason stands.
- **LLR (12 applied):** LLR-028 and LLR-032 rewritten from parent-paraphrase
  to siting detail — the two live paraphrase advisories cleared; LLR-173's
  parent restatement and sibling-claim duplicate dropped; LLR-170's four
  review-round markers removed with each durable reason kept; LLR-153/159/
  172/008/176/171 losing dated log/ruling/plan citations; LLR-144 one
  dangling sentence repaired + design-history count dropped; LLR-161's
  "earlier cut" changelog restated as the standing rejected-alternative.
- **TC (12 applied):** the "Guard proven to bite / Verified to fail against /
  Source restored byte-identical" build-history tails removed from expected
  cells (TC-108/117/118/119/122/123/124/125) — the pass conditions survive
  verbatim, and the anti-vacuity property those tails narrated is held by
  the tests themselves (the mutation-twin tests exist; the log holds the
  build account); TC-055's decision-history parenthetical and an
  ungrammatical fragment repaired; TC-153/TC-161 methods split into
  sentences with all named cases kept; TC-140's dated fixture label
  de-dated.

**Verification after the sweep.** `trace.py --strict`: SN=27 SR=72 LLR=161
TC=157, orphans=0, integrity=0 — and the paraphrase-advisory count fell 5 →
3 (LLR-028/LLR-032 cleared; LLR-007/020/027 remain, pre-existing and outside
the reviewers' top-12).
<!-- fig: cmd="python project-trajectory/scripts/trace.py --root . --strict" rev=fd6c87be -->
No `status` cell moved anywhere in the sweep — countersign-only wording
amendments inside the still-open window, the 2026-08-18k precedent.

**Flagged to the sitting, not acted on** (each is a decision or its own
sanctioned path, not a wording edit):

1. The 15 `(Derived-requirement label, added <date> — PROVISIONAL, unsigned.)`
   date stamps: each is individually allow-listed and each is the only
   record the label is unsigned — ruling them at the sitting retires marker
   and allow-entry together; a wording pass must not touch them.
2. TC-120 and TC-167 expected cells carry the same removable
   build-history tails as the eight swept ones (reviewer flagged, out of its
   cap); same treatment available if wanted.
3. SR-137/SR-175 rationales read long but are ~90% durable — deliberately
   not cut.
4. The reviewers found the SN-023/SN-027 inline TOML comments carry dated
   rulings; header/inline comments were out of the sweep's bounds by rule.
