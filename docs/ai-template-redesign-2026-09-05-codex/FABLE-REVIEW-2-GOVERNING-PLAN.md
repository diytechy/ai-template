# Second Fable review — which plan governs, and the Worktrunk ruling

**Date:** 2026-09-05. **Reviewer:** Claude Fable 5.1 through Claude Code, in a fresh session with no memory of authoring either plan, at repository revision `148ddc08` on branch `contract_split`. **Scope:** read both redesign folders and their review rounds, verify selected claims against the repository and against Worktrunk's published documentation, recommend which plan to implement, and rule on Worktrunk. No implementation, requirement approval, stage change, dial change, or test run was performed. The owner adopted the recommendation and asked that it be integrated here; the edits are listed in §6.

## 1. Verdict

**This folder's plan governs implementation.** The Claude plan at `docs/ai-template-redesign-2026-09-05 - claude/` supplies the evidence base (appendices A–C), the Phase 0 correctness fixes, several independently justified cuts, and the owner-decision agenda. It is kept as a record surface and is not edited by this review.

After the two cross-reference rounds the plans agree on the loop shape, one WI per lane, intake before eligibility, the scheduler as the sole admission authority, the LLR replacement route, rendering isolation, the stage ladder kept during migration, and one mutating runner at a time. Two independently built plans converging on that much is the strongest evidence either has that the diagnosis is right. What still separates them is discipline, and this plan has more of it where it matters:

- **It refuses to set the target before the manifest exists.** The Claude plan names numbers first (about a fifth of the code, about 70 LLRs, 60 IF rows, 8 modules, 3 ratchets). Its own round-1 reviewer then found five of ten sampled "self-description" rows carrying adopter-visible contracts. A number chosen before the clause-level disposition map is pressure to fit the spine to the number, the exact failure the kit's honesty doctrine exists to stop. §4 of the README says in so many words: do not set a count and fit the product to it.
- **P1A is the gate that makes the rebuild legal under this repository's own process.** SR-148 approves the current admission partition and LLR-149 the multi-WI batch; a new runner enabled against those rows either fails the gates or runs outside them. The Claude plan and its reviewer both missed this; it was adopted there only after the cross-reference.
- **P0 forbids operating the loop as part of the measurement task and demands predeclared thresholds.** The Claude plan's control period is the same idea with less fencing.
- **The completion criterion is structural, not numeric**: one WI per assignment, one intake boundary, one scheduler answer, one review subject, one terminal outcome, preserved stakeholder evidence, and a demonstrated reduction in what it takes to understand and operate the kit.

## 2. What is taken from the Claude plan

Folded into this plan's packages by the edits in §6:

1. **Four correctness fixes that are wrong today regardless of any redesign**, landed before the control window opens and recorded as part of the observed configuration, not as the treatment: the stage bar runs no tests below DevStg-Impl (the merge slot's `Bar-Green` attests a suite that never ran); the coordinator executes the modules it imported at launch and does not exit on script drift (OI-83); a resumed claim recomputes its base and can scan an empty range (OI-84); telemetry lacks the routed tier and row id.
2. **Appendices A, B and C as P0's starting census** — every LLR/TC/IF classified, all 82 modules mapped with SLOC and import closure, about fifty external tools against five objectives. Every single-source figure in them is a claim to re-derive before it drives a decision: the first draft carried two figures wrong in the plan's favor (batch SLOC counted with docstrings; a category count read as an effort share), corrected in its round 1, and this review found a third (§3).
3. **The independently justified cuts** of its §4.5 and §4.8 — ratchets reduced to those that protect a guarantee an adopter can name, generated artifacts cut to what the ladder needs, the sixteen domain skills moved out of a process kit, `RESYNC_PACK.md` replaced by a changelog plus a mechanical sync — each as its own argued WI on its own evidence, never as part of the kernel migration.
4. **Its §7 owner decisions** as the ruling agenda for the P0 decision gate.
5. **Its package layout** (`spine/`, `queue/`, `loop/`, `surfaces/`, `scaffold/`, one-way downward imports) as the directory shape this plan's responsibilities land in; `tests/test_import_layers.py` already exists to enforce a layering.

## 3. Verified facts and two defects in the Claude plan

Checked in this session against the working tree:

- The module count (82), the AST test-function count (about 3,254) and the sizes of the loop modules reproduce. The diagnosis stands.
- **Defect 1.** The Claude plan's §2.9 states the three wire-routing geometry tests run on every commit and that `test_traj_graph` is not in the smoke tier's exclusion. It is: the module sits in `SLOW_MODULES` in [tests/conftest.py](../../tests/conftest.py) alongside the whole `test_traj_*` family, which [LLR-AND-RENDERING.md §3](LLR-AND-RENDERING.md#3-cross-reference-qualification) had already pointed out. Rendering isolation (P9R) remains justified as a coupling and import-boundary fix; the per-commit smoke-budget urgency attached to it is false.
- **Defect 2.** The Claude plan's Phase 4 still reads "auto re-baseline on untouched commits", which its own §4.5 withdrew after round 1 as a laundering path. The plan contradicts itself on a gate rule. This plan's position (a ratchet baseline moves only by a reviewed commit with a reason) is the one to keep.

Neither defect is corrected in the Claude folder by this review; that folder is a record surface and the defects are recorded here.

## 4. Worktrunk ruling

**Not adopted as a replacement for the station or the lane mechanics inside the loop. Offered as an optional operator tool for hand-driven lanes, and used as a design reference.**

Compared from [integrate.py](../../project-trajectory/scripts/integrate.py) against Worktrunk's published merge and configuration documentation (worktrunk.dev, read 2026-09-05; the tool was not installed or executed):

| Concern | Kit station | Worktrunk `wt merge` |
|---|---|---|
| Invariant | trunk must already be an ancestor of the branch; trunk is merged IN, branch commits never move | rebase the branch onto the target, then fast-forward; branch commits are rewritten |
| Evidence binding | the refresh commit's `Bar-Green: tree=<sha> work=<sha>` trailer; verdict freshness and review rounds bind to commits | default squash and rebase destroy that binding |
| Residual with `--no-commit --no-squash --no-rebase --no-ff` | the closing lines of `integrate_one` | run blocking pre-merge hooks, require the target to fast-forward to the tip, create a merge commit, remove the worktree |
| Refresh, declared-generated conflict resolution, trunk-step ordering, the bar, the trailer | inside the station | outside its model; would run as a hook or before it is called |
| Claim protocol, outcome read from the tree, minted-id refusal, approval-act refusal, verdict gate, in-slot intake | inside the station | not modeled |
| Concurrency | the coordinator lock taken once in `_slot` | no documented locking between concurrent merges |
| Unattended operation | none needed | project hooks prompt for trust on first run |
| Adopter cost | stdlib Python | a Rust binary (Homebrew, Winget as `git-wt`, cargo), a system-tier ledger row, no documented library API |

With every history-preserving flag set, Worktrunk reduces to a hooks runner plus a merge commit plus worktree removal — a few hundred lines of a three-thousand-line module, and the kit's worktree unload carries measured macOS behaviors (dirty-tree refusal, ignored files, the primary checkout) it would not reproduce. This plan's target design moves further away still: same-tree receipt commits on retained candidate branches (P5) are exactly what squash and rebase erase, and the candidate is composed by the coordinator on trunk, not merged from the worker's worktree. The Claude plan's decision 7 asked for a prototype before claiming a saving; this review goes further and rules the prototype unnecessary, because the upper bound is visible from the flag semantics. The decision is recorded in the evidence table and in README §5.

Two things Worktrunk does confirm. Its `--no-rebase` mode requires the target to fast-forward to the tip, which is the station's §A2 constraint stated by a popular independent tool: the kit's design is not exotic. And its project hook file (`.config/wt.toml`, templated `{{ branch }}` / `{{ worktree_path }}`) plus `--format json` output are a good shape to copy when the station's own CLI is rebuilt (P6/P10). Where it earns a place is `wt switch -c <branch> -x claude` for an operator opening a hand lane beside the loop and `wt list --full` for glancing at lane state; document it in the operator notes as optional.

## 5. One conflict between the plans, resolved

The Claude plan's Phase 0 freezes self-minting during the rebuild (`complete_review = "off"`, the consolidation census paused). This plan's P0 observes the loop under **unchanged** authority and review settings. Both are right about different periods: the control window measures the churn fixes already landed on 2026-09-04/05 and must run under unchanged dials, with the four correctness fixes of §2 recorded as part of the observed configuration; a self-minting freeze is a treatment, and it applies only if the decision gate selects the rebuild option, for the duration of P3–P8, recorded as a dial change.

## 6. Edits applied to this folder

- `README.md` — recommendation paragraph names this review; §5 gains the Worktrunk ruling; §6 gains decisions 9–12 (Phase 0 fixes before the window, the package layout, Worktrunk as optional, independently argued cuts) and points the ruling session at the Claude plan's §7 agenda.
- `IMPLEMENTATION.md` — §1 adopts the directory shape; P0 gains the four correctness fixes, the appendices as starting census with the re-derivation rule, the decision agenda, and the §5 resolution; P9R states that the render family is already outside the smoke tier; P9 lists the independently justified cuts as separately argued WIs.
- `EVIDENCE-AND-TOOLS.md` — a Worktrunk row in the external-tools table; this review indexed beside the first.

## 7. Limits of this review

No tests or timing runs were executed. Worktrunk was read, not installed; its Windows behavior and concurrency under two simultaneous merges were not exercised. The appendices' row classifications were sampled through the round-1 findings, not reconstructed. The owner intends a further check before implementation begins; nothing here authorizes P1 or later.

## 8. Addendum, 2026-09-05 — corrections accepted

Codex's expansion corrected two claims above, and both corrections stand. (a) §2 item 1 called the DevStg-Tests bar an attestation of "a suite that never ran"; the bar names the steps it ran, so it is honest labeling, and the gap is what it does not run — treated in the [third review](FABLE-REVIEW-3-CROSSCHECK.md), finding C1, with a one-step fix. (b) §4 called Worktrunk "the first non-Python binary dependency"; git is already required, so "the first binary beyond git" is accurate, and its `--yes` and `--no-hooks` flags make unattended use feasible. The ruling is unchanged.
