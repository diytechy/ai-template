## 2026-08-19 — The repository review triaged: 31 findings dispositioned, eleven WIs minted, two owner briefs raised, the review archived

**The input.** `REPOSITORY_REVIEW_2026-08-19.md` (committed at `0c7afad7`,
external "Reviewer" author, target `2b867c0f`): 1 Critical, 9 High, 17 Medium,
4 Low, 9 positives, plus a known-deferred-risk section. **The method,** per the
standing owner directive that findings are claims: every finding intended for
action was CONFIRMED OR REFUTED against the live tree first — executable
claims re-run, documentation claims re-read at their cited anchors, frontier
claims checked against `docs/work/` and `docs/requirements/open-items.toml`.
Two claims were refuted in part, two findings were declined with reasons, and
three were already owned by frontier rows.

**The output.** Eleven WIs minted (`WI-473`…`WI-483`, watermark risen by
`--bump-ids`), two owner briefs raised (`OI-43`, `OI-44`), two pending briefs
corroborated in place (`OI-41`, `OI-42`), six frontier specs updated where the
review interacts with them, and the review archived to
[repo-review-2026-08-19.md](../archive/repo-review-2026-08-19.md) with its
ledger row in [../archive/README.md](../archive/README.md).

### Dispositions, finding by finding

| Finding | Verdict on this tree | Disposition |
|---|---|---|
| C-01 gate min-selector drops product checks | CONFIRMED — `check.py:574-576` schedules format/lint/tests+coverage at `BAR_RELEASE` only; `docs/gate` header states the MIN rule; aggravated by OI-30 D2 (`sr_bar` ceilings at DevStg-Tests, so `BAR_RELEASE` is unreachable-by-cell today) | **WI-473** (strong, spine: design proposal first) |
| H-01 launcher interpreter selection | CONFIRMED — `agent-resume.cmd:89-105` and siblings probe runnability only, never version, never `.venv` | **WI-475** |
| H-02 seven-module import SCC | CONFIRMED — cycle as mapped; `handback.py:56-57` asserts a direction `integrate.py:2186` violates | **WI-483** (structure) + WI-477 (the false sentence) |
| H-03 `hats -> spine_carrier` undeclared seam | CONFIRMED — reproduced as the ONE strict ERROR | **WI-474** (owns status.md's "trajectory gating red") |
| H-04 interface contract-test prose vs warn-only | CONFIRMED — 115 of 125 seams cited by no TC, reproduced; warn-only is a recorded deliberate choice | **OI-43** (owner posture call) |
| H-05 core scale + debt owner closed | CONFIRMED — ratchet commentary points at WI-280 (complete/, scoped to dashboard + bootstrap.main) | **WI-483** (first slice re-points the ratchet's owner) |
| H-06 taught schema vs enforced schema | CONFIRMED, all five sub-claims — verification also found the same retired words in `derive_gate.py:592,:634` comments | **WI-477** |
| H-07 depth-0 frame taught as optional | CONFIRMED both halves (honest gloss: always-scaffolded, inert-until-filled — `bootstrap.py:167-172`) | **WI-477** |
| H-08 README ledger false both directions | CONFIRMED — `hats.py:14-18` vs `README.md:121-123`; SN-033 checker shipped/wired/traced vs `:126-127`; nuance: SR-161 exists but Drafted, no LLR/TC — `uncovered=0` records a citing SR was filed, not that the record shipped | **WI-477** |
| H-09 duplicated plumbing unbounded | CONFIRMED — already owned | **WI-448** (context gains the review's themed-package shape constraint) |
| M-01 smoke nested UTF-8 decode crash | CONFIRMED by inspection — `test_smoke_budget.py` decodes the child `utf-8` with no error policy; not reproduced here (POSIX shell on PATH avoids the trigger message) | **WI-476** |
| M-02 script topology vs library reality | CONFIRMED — 59 modules, `sys.path` injection sites as claimed | **WI-483** |
| M-03 unbounded WI title breaks the dashboard | CONFIRMED — the concat site and equal-height grid as cited; ten of eleven live frontier titles are multi-sentence, so the fix is defensive rendering first | **WI-479** |
| M-04 dense normative cells / mega docs | CONFIRMED as description; **DECLINED as work** — see below | recorded only |
| M-05 ratchet baseline duplicate key | CONFIRMED — `"bootstrap.py"` at :1275 (2808) and :1283 (2859), latter silently wins | **WI-476** |
| M-06 test-module monoliths | CONFIRMED | folded into **WI-483** (split per-subsystem, no standalone slices) |
| M-07 lint red | CONFIRMED — exactly 6 errors | **WI-476** |
| M-08 stale live CodeSymbol anchors | **PARTIAL — 3 of 5.** Stale: LLR-087, LLR-088, LLR-112. REFUTED: LLR-015 (`budget_findings` exists in `trace.py` doing the row's stated job) and LLR-172 (honestly Drafted/"NOT BUILT YET", symbol names the intended extension point) | **WI-482** (the three repairs + a declared planned-symbol form) |
| M-09 `Contracts:` marker-line-only harvest | CONFIRMED — `gen_arch_map` vs `dispatch.py:72-77` continuation lines | **WI-478** |
| M-10 dead red-TC feature | CONFIRMED — and the decision already has a home: `dispatch.py`'s `_TC_NOT_RED` block records retire-or-re-arm as a judgement item at the 2026-08-15 sitting sweep | no new row; noted for the sitting; cited as OI-41 corroboration |
| M-11 pytest range retains the advisory | CONFIRMED — resolved 8.4.2 inside `~=8.3`; fix line is 9.0.3+ | **WI-480** |
| M-12 privacy off + identity metadata in history | CONFIRMED — `privacy_check = false`; domain-only census found personal-provider domains (identities deliberately not recorded) | **OI-44** (owner-only publication call) |
| M-13 "deny-by-default" vs fail-open | CONFIRMED | **WI-477** (honest labeling + corruption-vs-absence tests; posture change explicitly out of scope) |
| M-14 committed generated-HTML churn | CONFIRMED as cost; **DECLINED as work** — see below | recorded only |
| M-15 status.md over its own budget | CONFIRMED — 167 lines vs the declared 120 | **WI-477** checklist |
| M-16 performance gate vacuous | CONFIRMED — `check_perf --tier all`: no budgets to compare | **WI-481** |
| M-17 non-hermetic git fixtures | CONFIRMED — already owned | **WI-465** (context notes the corroboration) |
| L-01 stale operational comments (three) | CONFIRMED all three — incl. `check_trajectory.py:2436`, where the correction landed in the docstring one screen from the header still carrying the stale claim | **WI-477** |
| L-02 removable `assert` invariant | CONFIRMED — `gen_trajectory.py:812` | **WI-476** |
| L-03 two commit-subject conventions | CONFIRMED — recent practice uses category prefixes the skill does not describe | **WI-477** (document both, enforce nothing) |
| L-04 constrained-not-locked toolchain | CONFIRMED | **WI-480** |

Found during triage, same drift class as H-06: `docs/archive/README.md`'s
intro still named the retired `work-items.csv` as the WI registry — fixed in
place while the ledger row was added, declared here.

### The two declines, with reasons

- **M-04 (chronology and argument packed into normative cells; mega docs).**
  Real, and its remediation is spine-cell cosmetics at exactly the wrong
  moment: the amendment window closes at the imminent sitting, every spine
  amendment re-reddens the ratify brief, and the repo already holds the two
  correctives that address the cause — the one-decision doctrine (R1, which
  already split SR-140 three ways) and OI-32's generated-component direction
  (cells that cannot go stale). A cell-diet campaign is available POST-sign if
  the owner wants one; minting it now would queue re-attestation churn against
  the sitting. Declined, stated here so the review's finding resolves to a
  reasoned no rather than silence.
- **M-14 (megabyte-scale generated HTML committed repeatedly).** The cost is
  real and measured, but committed generated surfaces are a deliberate design
  this repo depends on: `gen_open_items --check` and the dashboard freshness
  gates byte-compare COMMITTED artifacts (OI-31's staged-divergence step
  hardened exactly that), and `open-items.html` is the declared owner surface.
  Reversing that is an owner-level design change with its own program, not a
  triage mint. The provenance-stamp-only churn observation is the one
  actionable kernel; it is noted inside WI-479's surface work as context, and
  the owner can raise the storage/history question as its own item if the cost
  starts to bind.

### Deferred to the owner by this session (the OI-41 ARM-2 declaration)

This session deferred two decisions, both minted as briefs: **OI-43**
(interface contract-test posture — promote at DevStg-Tests with a migration
allowlist, or soften the shipped prose) and **OI-44** (publication/identity
posture — accept, rewrite, defer-with-trigger, or fresh-history export).
`OI-41` and `OI-42` each gained an INDEPENDENT CORROBORATION paragraph;
neither recommendation changed. `OI-32` was read against the review and left
untouched (the generated-view direction is corroborated but not altered).

### Frontier hygiene (the review's triage doubled as the ordering pass)

The frontier survey found five orderings living in prose with no encoded
edge; the ones with clean semantics were encoded as soft `needs` edges, each
beside a dated note: **WI-455** gains `~WI-469` (the column drop follows
WI-469 — WI-469's own standing rule, now visible to the scheduler) and a
Context section recording that the `gen_arch_map`/MAPPING collision set grew
to four programs (WI-455/WI-390/WI-448/WI-483); **WI-390** gains `~WI-464`
(its spine amendment runs inside the re-tier window — already ruled 13q/13s,
now encoded); **WI-452** gains `~WI-455` (its "run last or scope to today"
choice, encoded soft). Deliberately NOT encoded: WI-467 → WI-464 (WI-467
feeds the same sitting that closes WI-464 — an edge either way would state
the wrong thing; the prose has it right), and WI-390's absent `priority`
(reads as 0 = most deprioritized, which matches its sitting-gated reality).
No frontier contradiction found beyond these; every open spec's citations
were left as the 2026-08-18b sweep recorded them.

### Discipline

- New WI titles are deliberately single-sentence with the argument in
  `## Context` — the registry's recent long-title practice is what M-03
  measures breaking the dashboard, and WI-479 proposes the warn; the eleven
  mints practice the form first.
- `ruff check .` on the pre-change tree: **6 errors** (WI-476's population).
  <!-- fig: cmd="python -m ruff check ." rev=0c7afad7 -->
- `check_trajectory.py --strict` on the pre-change tree: **1 error** (the
  WI-474 seam), and the interface-coverage advisory at **115 of 125** seams
  (OI-43's population).
  <!-- fig: cmd="python project-trajectory/scripts/check_trajectory.py --root . --strict" rev=0c7afad7 -->
- Watermarks risen by `trace.py --bump-ids` (WI 472 → 483, OI 42 → 44), never
  by hand; `open-items.html`, the dashboard, and the status generated block
  regenerated; commit bar (smoke + `check_docs --stale`) run green before the
  commit — outputs quoted in the commit body.
