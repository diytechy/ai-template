# Existing work and the redesign

**Status:** proposed reconciliation, 2026-09-05; snapshot `fa17b85f` on
`contract_split`. No WI was edited, claimed, completed, cancelled or reprioritized.
The table is planning evidence; the spec directory remains the queue authority.

## 1. How the queue affects implementation

Existing WIs carry requested outcomes, prior decisions and regression evidence.
They constrain what must survive, but the entire queue is not a prerequisite
for the redesign. A high priority does not silently widen the current task,
and selecting a redesign does not silently supersede a queued obligation.

P0 reads every open spec and relevant spec-of-record. Before a slice is minted
or enabled, give overlapping work one explicit disposition: implement in the
current runner first; fulfill through a named redesign slice; keep independent;
defer with preserved obligations; or retire only through an authorized scope
decision. These are planning dispositions, not new runtime WI states.

“Fulfill through a slice” requires a clause-to-evidence map and the ordinary
reviewed WI close/successor transaction. It does not permit marking an old WI
complete because a similarly named package was created. Retain archived source
specs, preserved patches, burned IDs and hard predecessor semantics.

## 2. Queued-item snapshot and proposed treatment

All 18 non-example files in `docs/work/queued/` at the source revision are
represented below. The command in §5 reproduces the inventory; the treatments
are engineering proposals, not facts mechanically derived from the titles.

| Existing WI/spec | Proposed treatment | Relevant slice and obligation to retain |
|---|---|---|
| [WI-536 — agent brief and scope](../work/queued/WI-536-agent-brief-and-scope.md) | Reconcile its cited knowledge-pack plan before editing brief doctrine; integrate only the overlapping clauses | P2a/P7a: clear scope and suitable brief content. Its thin spec does not mean no obligation; read its `specref`. |
| [WI-539 — ship complexity sensor](../work/queued/WI-539-ship-complexity-sensor.md) | Keep a separate optional-capability decision; do not add a new mandatory ratchet as part of the kernel | P9a: preserve the existing OI-68 outcome and downstream opt-in contract unless explicitly amended. |
| [WI-541 — verify retention](../work/queued/WI-541-verify-retention-layer.md) | Keep paired with WI-551; validate whichever retained-adjudicator implementation is selected before enabling it | P7a: provider/session continuity, occupancy semantics, resets and replay. Builder rework remains fresh by default. |
| [WI-545 — decomposition debt](../work/queued/WI-545-the-decomposition-debt-owner.md) | Reconcile with package extraction; avoid separately moving the same runtime functions twice | P2a/P6a/P9R: reduce responsibility coupling and preserve behavioral regressions. Read its dependencies before changing the order. |
| [WI-551 — restore retention layer](../work/queued/WI-551-re-land-the-adjudicator-sessio.md) | Preserve patch and owner-approved capability; decide old-runner restoration versus adaptation to the new invocation boundary | P0a/P7a: no blind application of the large old patch to a new architecture. No cancellation by calling retention unnecessary. |
| [WI-556 — children coverage doctrine](../work/queued/WI-556-children-coverage-doctrine.md) | Keep the existing owner ruling as an authoring obligation; coordinate with LLR replacement wording | P1/P9a: dimension coverage and independence conditions survive; do not turn a trust-based doctrine act into a new validator or implicitly remove an LLR tier. |
| [WI-557 — delegated decision records](../work/queued/WI-557-delegated-decisions-record.md) | Keep the already-ruled reporting obligation; explicitly compare it with proposed review receipts | P7a/P7b: decisions and alternatives/reversal cost are reported. Owner free-text review is not machine approval. A receipt cannot silently replace the owner-editable per-run report promised here. |
| [WI-570 — typed owner brief](../work/queued/WI-570-the-typed-open-item-brief-an.md) | Reuse its contract in the shared intake/owner-decision boundary; ship a targeted current-loop repair if needed for the measurement workload | P3a/P7b: concrete question, affected scope, options and recommendation; no bare question masquerading as a complete brief. |
| [WI-577 — approval brief population](../work/queued/WI-577-rule-whether-the-owner-s-appro.md) | Remains held on OI-82; do not choose the display population as an incidental renderer change | P7b/P9R: display and approval authority are distinct. Reuse the current policy reader when the ruling lands. |
| [WI-581 — close hygiene](../work/queued/WI-581-lane-close-hygiene-quarantine.md) | Address before exercising affected recovery paths, or carry its exact guarantees into the prototype and prove them before use | P0b/P5a: burned IDs, review/log evidence, sole-copy artifacts and approval-brief generation survive quarantine and cleanup. |
| [WI-582 — parsed dependencies and trace seam](../work/queued/WI-582-the-wi-552-residual-sweep-sch.md) | Fold compatible parser/seam work into one scoped repair; preserve the branch-versus-trunk freshness distinction | P2a/P4a: OI-77 parsed-value rule, declared seam or justified membership, and a test that remains red for stale trunk. No second regex parser. |
| [WI-596 — snapshot absorbed approvals](../work/queued/WI-596-the-anchoring-copy-s-absorb-le.md) | Treat as an authority concern before broad re-anchoring or approval-snapshot migration | P1A/P9a: account for every changed row a whole-file snapshot would absorb; never bless unrelated text by reseeding the baseline. |
| [WI-597 — contradictory refusal wording](../work/queued/WI-597-stop-the-snapshot-refusal-s-op.md) | Small independent correction, or preserve its two-message cases when that code is replaced | P0b/P1A: report the actual scoped authorization; change no already-ruled scoping policy. It does not gate the entire redesign. |
| [WI-598 — regeneration table coverage](../work/queued/WI-598-drive-the-trunk-regen-step-tab.md) | Reuse as contract coverage for the selected regeneration path | P5a/P9R: assert declared order and explicit skip behavior for every applicable step; preserve named behavioral examples so testing a table is not the only oracle. |
| [WI-601 — LLR-061 amendment](../work/queued/WI-601-adjudicate-llr-061-approved.md) | Resolve under current authority if needed by the baseline, or include the specific amendment judgment in a reviewed replacement transaction | P1A/P7a: assignment-scoped brief/evidence obligations. Do not discard an owed judgment because the old module is scheduled for deletion. |
| [WI-602 — sampled WI-580 close](../work/queued/WI-602-spot-check-the-clean-close-of.md) | Keep under the current sampling policy during control; separately decide any later sampling treatment | P0c/P7a: no defect is alleged by this spec. Count sampling separately from corrective rework; do not classify it automatically as waste. |
| [WI-603 — LLR-167 amendment](../work/queued/WI-603-adjudicate-llr-167-approved.md) | Reconcile its pending brief-selection judgment with prompt consolidation | P1A/P2a: applicable brief selection and approval of changed normative text; one prompt catalog does not satisfy the judgment by itself. |
| [WI-604 — first approval of LLR-210/TC-208](../work/queued/WI-604-adjudicate-llr-210-tc-208.md) | Decide what governs the old-runner control period; when replacing census behavior, amend the contract explicitly instead of first approving obsolete text merely to green the stage | P0c/P1A/P3a: unapproved content stays visibly unapproved; preserve consolidation scope and verification through the replacement. |

The mapping deliberately does not invent new hard dependencies between all
rows. Implementation checks the actual predecessor graph and rewrites an edge
only through the reviewed intake transaction. A soft edge orders work; it
must not accidentally become a delivery prerequisite.

## 3. Relevant decisions outside the queued specs

- **OI-83/OI-84:** the stopped-code/durable-base fixes are paired. A safe
  coordinator restart must not lose the evidence base. The redesign proposes
  the remedies but still applies the existing ruling/authority path before
  changing live behavior.
- **OI-82:** determines approval-brief presentation, not whether a machine
  may approve an artifact. Keep its held decision separate from runner work.
- **OI-69 retention:** an existing owner-approved capability, with partial
  work preserved. Its implementation can be replaced; its intent cannot be
  silently dropped to simplify the new session diagram.
- **OI-74/OI-75 reporting:** already-ruled decision-report semantics must be
  reconciled with the proposed receipt, telemetry and owner surfaces. Those
  records answer different questions; consolidating storage must preserve all
  required editing and authority semantics.
- **Existing pause and preserved branches/patches:** the working surface
  records paused operation and special preserved work. P0 inventories active,
  deferred and preserved state as well as queued files before live migration.
  This queued-file table is not a complete export of all unfinished work.

No pause removal, approval baseline copy, owner ruling or retained-patch
application is part of editing this plan.

## 4. Applying the reconciliation at implementation time

For each authorized slice:

1. Refresh this snapshot against current specs and Git; identify new/changed
   items, active assignments, pending amendments and retained partial work.
2. Read the complete spec-of-record and prior ruling for every overlap, not
   merely its title. Split multi-clause items into obligations in the review
   worksheet, without multiplying runtime WIs automatically.
3. Record: original WI/clause, retained outcome, proposed implementing slice,
   required authority, tests/evidence, dependent IDs and retained assets.
4. Choose whether targeted repair is necessary for a safe representative
   baseline. Do not run a known damaging cleanup path just to collect control
   data, and do not use that concern to require every queued cosmetic fix.
5. Publish actual spec/successor/dependency changes together through intake.
   Preserve unresolved obligations; an obsolete mechanism is not an accepted
   outcome. Never change an active assignment's scope without the explicit
   stop/reconcile route.
6. Close only when the mapped acceptance has evidence, or the owner has
   deliberately retired the obligation. Re-run the ordinary integrity checks.

If the runner is retained, the queue continues with independently justified
repairs. If replaced, new work must reference the new contract while old
active lanes drain under their existing one. Exactly one implementation may
mutate the authoritative queue at a time.

## 5. Reproduction and cross-check

The inventory was produced by parsing TOML frontmatter with Python 3.11's
`tomllib`, excluding `WI-000`, then reading the resulting specs. Reproduce the
count and identities from the repository root:

```python
from pathlib import Path
import tomllib

rows = []
for path in sorted(Path("docs/work/queued").glob("WI-*.md")):
    if path.name.startswith("WI-000"):
        continue
    text = path.read_text(encoding="utf-8")
    row = tomllib.loads(text.split("+++", 2)[1])
    rows.append((row["id"], row["title"], row.get("needs", []), str(path)))
print(len(rows))
for row in rows:
    print(row)
```

This is a bounded census recipe for the known current carrier, not a proposed
runtime parser. Runtime consolidation must use the existing parsed boundary.
Cross-check all 18 identities, then challenge the proposed treatment with the
spec's complete acceptance and rulings. A new queue revision requires a new
inventory; do not keep this table current by hand indefinitely after cutover.
