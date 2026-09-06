# redesign-authoring-final — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `573ad6ed31d1b1f3aa078ece368ae9ddb4a07edddfcdda286ec68fbac65fcfca`

Tracked invocation: [session log](../iteration/call_b4bb3eaca33842d693b87dbf99f6e184-20260906-105947.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

## CHANGES_REQUESTED — findings=21

Tools disabled; I read only the supplied source. No test was run and I claim no result. All line/row citations are the supplied contents.

**What holds.** All three new SRs decompose text that is genuinely in the parent's *normative* cell (SN-024's acceptance, SN-037's last clause, SN-012's granularity clause) — none is a derived requirement owing a lens label. The homes are argued correctly against the incumbents (SR-154/155, SR-162, SR-157/159/183). `Inspection` + direct TC is permitted by PROCESS.md:737-744. Nothing claims a passing run. The adopter record does distinguish missing-need / missing-constraint / implementation-gap, refuses the O1–O6 copy, and disclaims the vendor route. No new permission gate is invented. The blockers below are live-state defects and over-claims, not a re-litigation of the authored decisions.

---

### BLOCKER

**1. `LLR-048.sr_refs` re-point attaches a mechanism that does not realize SR-184 — and manufactures structural completeness.**
`docs/requirements/low-level-requirements.toml` LLR-048 → issue: LLR-048's detail is *brief assembly* ("assembles a fresh … rubric/intent/artifact brief"); SR-184's `shall` is about the **acceptance record** written afterward (reviewer identity, intent sources, numbered anchor ids). The packet concedes the mechanism doesn't exist ("The implementation gap is explicit rubric derivation … and per-finding numbered anchor citations"). Three consequences: (a) SR-184 now has an LLR *and* a TC, so on approval it can derive `Founded` (PROCESS.md:449-451, "the artifacts the row calls for EXIST") on structure alone with zero implementation; (b) LLR-048 is `Approved` and its cell changed, so it now drifts from `docs/archive/last_approved/` — which the packet's "No Status, approval snapshot … changed" does not disclose; (c) an `Approved` child hangs under a `Drafted` parent. → **Revert `sr_refs` to `["SR-154"]`.** SR-184 is `Inspection` and LLR-exempt; it needs no LLR. Evidence reuse belongs in TC-209's `evidence` cell, not in a child's parent list. *Antidote:* this is the deletion that makes the guard unnecessary — with no re-point there is no false-Founded path to detect, no LLR-048 re-attest, and no cross-status edge.

**2. SR-162's rationale is now a live falsehood.**
`docs/requirements/system-requirements.toml` SR-162 rationale → "the need's last clause … is a REVIEW obligation this row does not claim to mechanize, **and no SR states it yet**." SR-185 now states it. Nothing detects a stale NOT-DISCHARGED clause on an `Approved` row, so this survives indefinitely. → Strip the transient half and keep the durable one: "…is a REVIEW obligation this row does not claim to mechanize." (Do not substitute "SR-185 states it" — that is provenance the join already carries via SN-037.) Record the resulting SR-162 drift with the others (finding 10). LLR-187's "The cross-side requirement/interface amendment rule is also unimplemented" stays true and needs no edit.

---

### MAJOR

**3. SR-184 drops SN-024's "not the possibly-lax TC" — so TC-209 tests something the SR does not require.**
SN-024's acceptance: "a written rubric derived from the SN/SR intent **(not the possibly-lax TC)**". SR-184's `shall` and AC require only that the record "names the rubric and its SN/SR intent sources" — a rubric copied verbatim from a permissive TC can name those sources nominally and pass. Yet the H2 Inspection procedure demands exactly that catch ("a record whose rubric is copied only from a permissive TC … it must find both gaps"). The TC is presently unfalsifiable against its parent. → Add the exclusion to SR-184's `acceptance_criteria`: a rubric taken from the verifying TC without independent derivation from the SN/SR intent is a finding.

**4. SN-007's new CI sentence has no citing SR.**
"Hosted CI runs the same declared bar for each trigger." SR-151/SR-152 carry that obligation under **SN-005/SN-004/SN-008** — neither cites SN-007. So the amendment adds a clause to an approved need with zero SR occurrence, the precise failure SR-154 and SR-162's own rationales describe ("ZERO textual occurrence anywhere in the SR layer while `orphans=0` still held"). The alternatives are re-pointing SR-151 (more Approved-row drift for no gain) or deletion. → **Delete the sentence.** SN-005 already owns per-moment CI; SN-007's subject is the kit's own maintenance bar.

**5. TC-209/210/211: `evidence` restates `method`.**
`docs/test/test-cases.toml` → all three point `method` *and* `evidence` at the same document anchor. `Evidence` is where the artifact/result lives (spine-authoring §3); pointing it at the instructions means the release checklist that finds `Automated=No / Tier=Release` rows can never distinguish an executed inspection from an unexecuted one — and PROCESS.md:730 expects a human-method TC to record *who* and *when*. → Keep the procedure in `method`; make `evidence` name where the completed inspection record will land (and say "not yet produced" if that is the truth today).

**6. The Inspection procedures live in a dated redesign folder.**
All three TCs bind to `docs/ai-template-redesign-2026-09-05-codex/DECOMPOSITION-AMENDMENTS.md#…`, a review workspace whose own header says parts "remain a proposal". When the redesign closes or archives, three live TCs cite a moved instrument — spine-authoring §5's "a citation that outlives its instrument". → Move the three procedures to a durable home under `docs/test/` and re-point.

**7. The reviewer prompt inverts the re-attest rule.**
`project-trajectory/prompts/reviewer.template.md:37` → "a design replacement must retain parent acceptance, enduring regressions and **applicable child approval**." The skill says the opposite for the child: "Preserve unchanged **parent** approval, **re-attest changed child content** through the applicable authority." As written, a reviewer can bless an amended `Approved` LLR that kept its signature. This ships to adopters. → "…must retain the parent's approval and the enduring behavioral regressions, and re-attest the changed child through its applicable authority."

**8. PROCESS.md §5's new intro contradicts its own diagram's step 1.**
`project-trajectory/PROCESS.md:863-864` now says routing is by "which obligation or design needs changing", while node `C` at :868 still asks "which row does it contradict?" — two statements of step 1. The edit also deleted "**that classification, not the fix, is step 1**", which was the only clause forbidding a jump straight to the remedy. → Restore that clause and keep the intro's wording aligned to node `C`; the new `D` decision is a *second* question, not a replacement first one.

**9. The P0 adopter record over-claims what the fixture measures.**
"The preservation test proves that those records and their Git history survive the supported copy upgrade." Only the **add-only** arm proves that (`assert _digests(repo, preserved) == preserved` after bootstrap/regenerate/sync). The `--force` arm hand-restores every owner file (`for rel in restored: (supported / rel).write_bytes((repo / rel).read_bytes())`) *before* the later `_digests(supported, …) == _digests(repo, …)` assertion — that comparison reads bytes the test itself just wrote, so it cannot fail and proves nothing about the overwrite. The test's docstring is honest about this; the review record is not. → Say precisely: preservation is measured on the add-only route; on the overwrite route the fixture demonstrates the *operator's documented hand-merge plus carrier conversion* (SN-701 text/status and SR-701 `sn_refs` survive conversion — those assertions **are** genuine), not a property of `--force`.

**10. The re-attest debt is under-stated.**
The packet names only "H1/SR-175 re-attestation", but four `Approved` rows now diverge from `docs/archive/last_approved/`: **SN-007** (acceptance), **SN-026** (tags), **LLR-048** (sr_refs — see finding 1), and **SR-162** once finding 2 is applied. → Enumerate all of them in "Review and sequencing". Amending freely is correct for an authoring session (worker template's rule); leaving the adjudicator to discover the drift by diff is not.

**11. SR-186's `shall` and its acceptance criteria have different subjects.**
The `shall` binds "the delivered requirements process" to *keep* decompositions proportionate — an outcome in the adopter's authoring behavior, over which the delivered package holds no design control. The AC then correctly binds a *reviewed decomposition record*. This repo already reasons carefully about exactly this gap (SR-151/SR-152's DESIGN-CONTROL passages); SR-186 makes the stronger claim with no such argument. → Restate the `shall` as what the delivered process **requires and records** ("shall require each additional child within a required tier to carry an independent decision or verification purpose, and shall record the stopping decision in the scoped decomposition record"), or add the design-control reading to the rationale.

---

### MINOR

12. **SR-186's AC re-homes two rules it does not own** — "every required SN→SR→LLR→TC tier remains present and each SR/LLR has its required verification link" restates the DevStg-Tests gate (PROCESS.md:482-487), and "absent optional features remain cheap" restates SN-012's *first* clause, which the packet itself says existing SRs own. Cut both; leave the AC stating only the proportionality condition no other row carries.
13. **SN-007's acceptance restates the moment-to-tier table.** Its first clause ("the declared bar for the moment is green before a change lands") is sufficient and cannot drift; the Smoke/Full/Release enumeration is a second home for `docs/stack.ini`, which for *this* repo declares `all` on push and pull_request. Delete the enumeration.
14. **Drop the H1 `why` expansion rather than leaving it pending.** SN-026's applicability is already derivable from SR-175's `hat_refs = [DATA-PROTECTION, LEGAL, SECURITY]`; adding a `why` sentence that points at a child SR is the "do not declare what the row already derives" case (spine-authoring §6) and would go stale if SR-175 is re-homed.
15. **Verify `legal` / `personal-data` against `hats.toml` predicates — now, not at intake.** The prior closure review deferred this while the tags were a proposal; they are live. A tag no `applies_when` reads is an unwired marker that `hats.py audit`'s unknown-predicate-tag finding does not catch (it looks the other way down the join). I could not verify it from the supplied source.
16. **SR-184 silently drops SN-024's "family-heterogeneous" for attended Critique.** Dropping it is *right* — mandating a second family on an attended human reviewer would push a vendor/roster requirement onto adopters — but spine-authoring §5 says name the tier you leave out. One clause in the rationale.
17. **Hat-Refs calibration.** `PERFORMANCE` on SR-186 (a requirement-decomposition row) is the case §2(c2) warns about: attribute only where that hat's own `listens_for` names a failure this row prevents. Re-read the three-name cells on SR-185/SR-186 against `hats.py list`.
18. **The TC anchors are probably wrong.** Under GitHub's slugger, "H2 Inspection procedure — Critique acceptance record" yields `h2-inspection-procedure--critique-acceptance-record` (em dash removed, both spaces kept → double hyphen); H3's `/` is dropped as well. All three cells use single hyphens. Resolve them, or make the anchors moot via finding 6.
19. **Mixed tense.** §H1 and §H4 read as proposals ("Proposed changed cells", "This proposal is pending human need-tier approval") while the diff shows both landed. The header discloses it; the sections do not. Restate the two sections as *authored, re-attest owed*.
20. **"enduring regressions"** (PROCESS.md:891 and both prompt templates) reads as "keep the bugs". The skill's phrasing is "retained parent clauses and behavioral regressions" — use "the enduring behavioral regression tests".
21. **Two unanswered carry-overs.** The prior review's `aspect` question (present on SR-186, absent on SR-184/SR-185) is still open — answer it or record that `aspect` is optional. And the P0 record's evidence basis, "`83f2c7aa…` plus the continuation changes", is unpinned: nobody can re-drive it. Also `O1–O6` is used twice with no definition or link.

**Not raised as findings, deliberately:** the H2/H3/H5 tiering decisions, the direct-TC-without-LLR route, the change-intake `D` node's three edges (it widens routing, narrows nothing), and the adopter record's three-way question table. Those are sound.

**One caution on the remedies:** eleven of the twenty-one fixes above are deletions or re-pointings, and none of them adds a form, schema, field, or checker. If a later round proposes a new detector for any of these, the question to ask first is why the row could not simply stop asserting the thing.
