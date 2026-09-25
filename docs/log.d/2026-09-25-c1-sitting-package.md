## 2026-09-25 — The C1 sitting package, prepared

An attended session resumed from the
[2026-09-24 handoff](../handoff-2026-09-24.md) and prepared the package its
"What is next" item 1 describes:
[plans/2026-09-25-c1-sitting-package.md](../plans/2026-09-25-c1-sitting-package.md).
Documentation only: no script, test, registry row or template changed, and no
work item was filed.

Deferred open items: none — the owner answered the package's three items in the
same session (below).

**Owner ruling.** *"I'm good with the recommendations you have laid out."* That
decides §0.1 (b), build first with the arms off, and §0.2 (a), the headline
needs Drafted until a complete chain answers each. It also accepts §1–§4 as
written. The owner will be absent: a Fable reviewer stands in for the owner's
approvals of the spine work that follows, and a codex Sol review (medium
effort) runs on each spine iteration. Stand-in approvals are recorded as the
stand-in's, so the owner can re-attest them on return.

**What the package states.** The frame rows with their ids (`EXT-006` human
operator, `EXT-007` hosted CI, `B-09` read, `B-10` model runner, `B-11` hosted
CI, the narrowed `EXT-001`, `B-02` re-pointed, `EXT-003`/`REL-001`/`REL-003`
dropped, a `system` cell on every bundle), each reversed ruling with its
replacement text, four stakeholder rows and every need's owner, the two headline
needs as SN-041 and SN-042 with a `source` pointer column, the dial move (Q14),
the build list with its arms off, and a checklist for the sitting commit.

**Found while preparing** (each checked against the code, and recorded in the
package's §0):

- **Approving the two headline needs lowers the derived stage.** An Approved
  need no Approved requirement cites reads DevStg-Needs in every phase, and the
  fold floors the headline at DevStg-Reqs, which deselects `smoke`,
  `design-flows` and `trajectory`. An Approved requirement with no design rows
  still reads DevStg-LLReqs. AT §11's "approved with the needs" is marked
  REOPENED, and the package recommends landing both needs Drafted until a
  complete chain answers each.
  <!-- fig: derived="derive_stage._effective over spine_rules.load_spine(docs) at c3134d78, with SN-041/SN-042 added to sn_ids (Approved) or sn_draft (Drafted), and with two Approved SR rows copied from SR-182 citing them" -->
- **The live registries refuse a key their template does not ship**
  (`test_dogfood_sync`'s key rule), so the frame, stakeholder and need rows can
  only land after the build. That fact frames the handoff's question: sign
  first, or build first with the arms off.
- **The plan's frame counts predate Q28**: with hosted CI the frame has 5
  entities, 7 bundles and 1 relationship, not 4, 6 and 1.
- **The sitting commit must move `test_dogfood_sync`'s `REL-ID` bite-proof**
  off `[relationship.REL-001]`: the test plants into the live row and asserts
  the plant landed.
- **Nine rows restate a reversed ruling** (LLR-051, -056, -057, -124, -139; the
  rationales of SR-151, -152 and -175; IF-041's note). The package recommends one
  sweep work item, filed at the sitting.

**Surfaces.** `docs/status.md`'s assumption-tier bullet, the handoff's item 1
and `docs/plans/README.md` point at the package.

**Byte deltas on budgeted files:** `docs/status.md`, one bullet replaced
(within its declared 160-line budget); no capped file edited.

**Checks run before this commit.**

- `check_docs.py --root . --stale`: **OK**, 1496 docs, 2339 links, 0 broken,
  3 orphan warnings, all present before this session.
- `check_trajectory.py --root . --strict`: **clean** (623 work items; 128
  advisory warnings, mostly the known shared-spec pairs).
- Commit bar, results: smoke **1681 passed, 3 skipped** in 397.5 s.
  <!-- fig: cmd="python -m pytest -q -n auto -m smoke" rev=c3134d78 -->
- Commit bar, seconds: **FAIL**. `check_smoke_budget.py --mode enforce`
  measured 406.6 s against the 60 s budget (its own run: 1681 passed, 3
  skipped). This 8-core machine fails the budget on every run, as the handoff
  records. The change is documentation only and cannot move the tier's timing,
  and one machine is one data point, so the budget was not re-stamped.
  <!-- fig: cmd="python scripts/check_smoke_budget.py --mode enforce" rev=c3134d78 -->
