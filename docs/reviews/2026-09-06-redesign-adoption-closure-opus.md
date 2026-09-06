# redesign-adoption-closure — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `82d4477930df9d42b3c01d93db957344805cc29efd27a6ce668b84928a96e4b4`

Tracked invocation: [session log](../iteration/call_9299e2c17b4f4a82a0e3ca740804f3f4-20260906-095929.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

# Intermediate closure review — CHANGES_REQUESTED? No: **APPROVE**

Verdict: **APPROVE** (no blocking defect attributable to this patch)

## Closure of the four findings

**F1 — closed.** The canonical skill restores both deleted facts: the roster path (`docs/requirements/hats.toml`) and the audit's three outputs (SN × conditional-hat matrix, needs reaching no conditional hat, per-hat reach count). They now live in "Check the real brief" rather than §1(a), which is the better home — §1(a) is per-row intake, the audit is a sweep — and §1(a) points at it. The reach count, the instrument case (7) depends on, is back. The stale "Four questions:" over five bullets is fixed as a side effect.

**F2 — closed.** CONSISTENCY's `listens_for` carries the template-vs-instance axis again ("a rule stated differently by template and instance"), in both the instance and the template. Both neighbouring comments are corrected in place rather than deleted, preserving the original finding's history while stating the wider scope — the method-flip sweep this file asks for, applied to itself. PERFORMANCE's comment gets the same treatment.

**F3 — closed, and the residue is honest.** "Or reversed" is gone, so no rollback obligation is minted. The five questions collapse to one completion question with a compound preservation clause; that clause is answerable per row. Retaining the name over renaming is a defensible reading of the governing disposition, and the stranger test survives verbatim in `listens_for`, so the name still describes a real half of the charter. The predicate gap is stated beside the predicate instead of being papered over, and adoption/resync reassess applicability at their own entry point rather than widening every adopter's predicates — the proportionate choice.

**F4 — closed.** All 27 worksheet rows now cite live README anchors, so the markers have a consumer. The paraphrase concern is a judgement the user has already made; the anchors are declared prose without acceptance, tier or approval stage, so nothing derives from them that an SN/SR does not already carry.

**Cases 5/6 — closed.** "When changing or removing a hat, review its inbound Hat-Refs" now covers refinement, and the no-semantic-impact conclusion is homed in the resync commit. No existing attribution is falsified by these four broadenings (each new failure class is a superset), so no re-point is owed.

## Non-blocking, verify before merge

1. `VISION-OBJECTIVES.md` links `README.md#vision` — confirm a heading generating that slug exists; the `#objective-oN` ids are explicit and fine.
2. Six `###` headings land with no `##` parent, ahead of the License line; check the generated TOC and front-door reading order.
3. Confirm `.claude/` and `.agents/` mirrors match the canonical skill (`test_dogfood_sync`).

Authority, schema, queue and test cadence are untouched. Scope is proportionate.
