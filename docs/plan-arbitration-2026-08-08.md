# Plan arbitration and composite — 2026-08-08

**Status:** proposed for owner review at the P0 sitting; nothing here executes
until ratified. **Update (2026-08-08):** at the owner's direction, §5's six
amendments are now applied in the build plan, making it the self-contained plan
of record; this memo remains the ruling's rationale and fact-check record. Arbitrates between
[stakeholder-needs-build-plan-2026-08-08.md](stakeholder-needs-build-plan-2026-08-08.md)
("the build plan") and
[plan-2026-08-08-mechanized-loop.md](plan-2026-08-08-mechanized-loop.md)
("the loop plan"). Every load-bearing claim in both plans was re-measured
against the repo on 2026-08-08 (§2).

## 1. Verdict

**Adopt the build plan as the base; amend it with the six items in §5.**

- The loop plan's own addendum already concedes the core architecture to the
  build plan (nine adopted points: ledger, two-axis model, naming, admission
  transaction, override-moves-spec, argv arrays, prompt hashes, hard
  mixed-config refusal, WI dispositions). Its main body (§2 dual-read, §3
  git-derived baseline, §5 never-reverse, §6 warn-first) is superseded by that
  addendum, so it no longer reads standalone; the build plan is internally
  consistent as written.
- The build plan specifies the agreed mechanisms in executable detail (two-axis
  spine model §3, ledger schema §6, admission transaction §8, resume precedence
  §9, prompt provenance §10) and carries the stronger implementation apparatus:
  a dependency DAG with edges, checkpoints with exit evidence, a closure test
  matrix (§12), and a cutover/rollback path (§14).
- It diagnosed the amend+flip detection gap correctly *before* cross-review
  (its §2 row B, §6) — the gap the loop plan had to concede in its addendum
  after claiming detection was "built end-to-end".

The loop plan's genuine unique contributions are absorbed in §5, not lost.

## 2. Fact-check against the repo

Both plans are honestly grounded. The load-bearing measurements:

| Claim | Measured at | Result |
|---|---|---|
| Spine SN=27 SR=136 LLR=137 TC=135, 21 Modified, G2 | `docs/gate` basis line | exact |
| Hooks parse `privacy-check`/`review-policy` in pure sh, first non-comment line (M-42) | `project-trajectory/hooks/` pre-commit:46, commit-msg:36, pre-push:73,142 | exact line numbers |
| Worker/reviewer/critique prompts are Python constants | `agent_loop.py:259/299/347` | exact |
| `NEEDS-HUMAN` magic substring selects strong tier | `intake.py:152` (loop plan said :151) | confirmed, one line off |
| Amend+flip rows deliberately skipped by `staged_spine_amendments` | `check_trajectory.py:2884-2886` docstring | confirmed — validates build plan §6 case 2 / addendum point 1 |
| No routed adjudicator phase; arbiter only a dual-plan hat | no `ADJUDICATE` anywhere; `DEFAULT_PHASE_TIER` at `agent_loop.py:386`; `HAT_ARBITER` at `plan_briefs.py:57` | confirmed (tier table lives in `agent_loop.py`, not `agent_route.py` as loop plan §7 implies) |
| Queue = WI-000/390/413/415/416/417/418; no unused-function sweep WI | `docs/work/queued/` | exact |
| `read_declared` reads first non-comment line, same rule as hooks | `agent_common.py:112-124` + docstring | exact |
| `SPEC_STATUS_DIRS` triplicated (F5) | `agent_common.py:676`, `check_trajectory.py:379`, `schedule.py:252` | exact |
| Handback contract: `returned/` recommendation (§5), rglob trap (§8), five ruling questions (§10), one-file migration (§9) | `docs/handback-contract.md` | exact |
| No `returned/` or `partial/` status dir today | `docs/work/` = cancelled, complete, deferred, draft, queued | confirmed |
| `tomllib` already stdlib-used | 7 script files, incl. the 4 the loop plan named | confirmed |
| Five one-value policy files; `secrets-scan`/`blackout` absent | `docs/{gate-policy,push-policy,privacy-check,review-policy,guardrails-policy}` | confirmed |
| Build plan never states the resync/never-clobber contract | grep of the build plan for resync/adopter-owned/never-clobber | **confirmed gap** |
| Loop plan addendum: M-42 "unaddressed" in the build plan | build plan §5 addresses it (Python entry point, fail-closed, agreement tests) | **claim inaccurate** |

## 3. The converged core (not re-litigated)

One TOML config; two derived axes (`spine_stage` 0–4 for workflow/admission,
`verification_gate` G1–G3 for the harness); `human_ratification_through`;
append-only attestation ledger keyed by artifact id + normative-text digest;
per-attempt immutable outcome event outside `docs/work/`; worker claims
Complete/Cancelled/Partial into terminal folders, adjudicator
override-by-minting with the byte-identical spec moved to the corrected folder;
successors with explicit lineage, attempted WIs never revived; one trunk-side
admission transaction with digest-fresh conflict verdicts; four adjudicator
templates on the dual-plan pattern with strict slots; template/rendered-prompt
hashes recorded per session; SN-E/F stay unminted; one combined
drafting-plus-re-attest sitting; dedicated infra branch with the full suite as
the phase bar; one measured dead-function sweep at the end.

## 4. The loop plan's three "retained" points, re-examined

1. **M-42 hook constraint — dissolves as stated.** The build plan §5 addresses
   it explicitly (Python config-query entry point; missing/below-floor
   interpreter refuses clearly, preserving fail-closed; old-shell/new-Python
   agreement tests during migration). The plans merely *prefer different
   options* — and the loop plan itself rates the build plan's option "stricter
   than today, and acceptable now that the floor is enforced by dev-setup."
   Ruling: §5 item 2.
2. **Adjudicating every Complete close — not a disagreement.** The build plan
   §1.5/§7 already says what the loop plan recommends: the independent review +
   composed-tree bar is authoritative for Complete; a dedicated adjudicator
   runs on disagreement, incomplete evidence, safety class, or configured
   sampling. Record the tier/sampling dial in SN-031's acceptance text.
3. **`stack.ini`'s never-clobber resync contract — stands.** Genuine gap: the
   build plan folds stack.ini into `config.toml` without stating the
   adopter-owned, preserve-on-resync property (the SR-036/TC-036 contract).
   Fixed by §5 item 1.

## 5. The composite: the build plan plus these six amendments

1. **Resync contract (from the loop plan).** SN-028's acceptance and P2/P13
   must state: `docs/config.toml` inherits stack.ini's adopter-owned,
   never-clobber-on-resync property; the kit ships `config.toml.template` plus
   the legacy converter; bootstrap/resync runs the converter automatically, so
   no downstream adopter meets the hard mixed-config refusal unaided (the
   addendum's proviso to its own point 8 — kept).
2. **Hook strategy (decision recorded, both options documented).** Target: the
   build plan §5's Python config-query entry point, failing closed on a
   missing/below-floor interpreter. Document the loop plan's keyed-grep
   alternative (`grep -E '^privacy-check *= *true'` + cross-parser agreement
   test, the WI-1.21 pattern) as the fallback if the owner rules hooks must
   stay Python-less. Either way the migration agreement-test matrix both plans
   specify is the bar, and M-42 fail-closed holds by construction in both.
3. **File name and scope.** `docs/config.toml` (build plan), not
   `process.toml`: SN-028's acceptance is one validated file for harness +
   automation + routing + prompt selection; `process.toml` named the narrower
   scope the composite no longer has. Routes move into `[[routes]]` argv tables
   per build plan §5, carrying the agents.csv Notes culture into per-route
   notes keys; `docs/agents-enabled` stays a presence-consent file (both plans
   agree — loop plan §2 exception 2).
4. **Drafting mechanics (from loop plan §1).** P1 drafts SN-028..032 under a
   `## Draft needs` heading in `stakeholder-needs.md`, so derive_gate's
   section-as-state rule holds the gate down honestly during the sitting
   (`sn_draft_ids`; `ex-draft=` keeps the window arithmetic honest; expect
   G0/G1 — the design working, not a regression).
5. **Component spine batching.** The build plan §8's connected-components
   partition rule is the *safety* contract (independence = no trace/interface
   edge crosses the partition; missing ownership collapses to one project-wide
   batch). The loop plan's size-threshold dial may ride along as an optional,
   default-off config knob in P11.
6. **WI-390 absorption timing.** Keep the build plan's P1/P13 mapping over the
   addendum's "P0 sitting": P0 *declares* the combined sitting, P1 *is* the
   sitting — and handback-contract §11 puts WI-390's spine close in that same
   window per §A4's one-sitting rule.

The composite also inherits the loop plan's evidence discipline: §2's table
above preserves its file:line measurements for the P0 brief.

## 6. Proposed disposition of the two source docs (owner call at P0)

- **Build plan:** stands as the plan of record, amended by §5.
- **Loop plan:** superseded as a plan; retained as the measured current-state
  survey and the reconciliation record (its addendum). Both source docs stay
  untouched until the owner rules.
