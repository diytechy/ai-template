## 2026-08-20 — The frontier grind, in series (owner directive): per-WI record

The owner's 2026-08-20 directive: grind the open frontier in series with
opus/sonnet workers, one large adversarial review (internal Opus +
cross-family Sol via codex) at the end, consolidated and iterated in one
action. One entry per WI as it closes; adjacent findings accumulate at the
bottom for the closing review.

### WI-474 — the hats→spine_carrier seam (opus worker) — CLOSED complete

IF-133 minted (carrier-consumption shape per IF-118/119/120/122; owner
LLR-166, carried_by IF-102, req_refs SR-147, CMP-008, Drafted); two
consumer-side contract tests added and driven negative; `Contracts: IF-133`
docstring line; watermark IF 132→133; snapshot re-taken byte-identical.
`check_trajectory --strict` EXITS 0 — the first all-green strict trajectory
run on record. Worker's full suite: 2592 passed / 13 skipped in 492.66s
(one environmental posix-shell gate re-run gated).
<!-- fig: cmd="python -m pytest -q -n auto" rev=6a6d866d -->

### WI-476 — harness hygiene batch (sonnet worker) — CLOSED complete

`ruff check .` ALL CHECKS PASSED (was 6 errors; the trace.py dead unpacking
deleted with its ratchet entry re-stamped DOWN); the duplicate
`"bootstrap.py"` baseline entry merged (effective bound preserved) and the
baseline made duplicate-key-PROOF via an AST parse of the file's own source;
the nested smoke-budget child runs forced-UTF8 with a planted cp1252-byte
regression test; the gen_trajectory panel assert is an explicit raise with a
test. Touched modules 98 passed; smoke 1209/5 (two new tests joined the
tier). The worker's final report arrived AFTER the close (it had stalled on
its own background full run; the work was verified from the diff first) and
confirms: full unfiltered suite 2596 passed / 13 skipped in 453.88s; the
M-01 crash was REPRODUCED live before fixing (the cp1252 em dash killing
subprocess's reader thread); the spec's "malformed noqa" finding no longer
existed on the moved tree — the real sixth was a second F841. Two declared
deviations, both accepted: M-05 deliberately narrowed to the duplicate
merge + AST guard (stripping ~1,700 lines of per-entry history judged
disproportionate for a quick batch — if wanted it is its own WI), and no
RESYNC entry (no adopter-facing behavior moved).
<!-- fig: cmd="python -m pytest -q -n auto" rev=34a42f7e -->

### WI-475 — launcher interpreter selection (opus worker) — CLOSED complete

One selection policy in every probing launcher (.venv first, runnability
then version probe, refusal NAMES every rejected candidate), the `.command`
wrapper documented as the honest inherited exception, `call`-prefixed cmd
invocations (the shim trap: the old launcher exited 0 having run nothing),
and 27 executable selection tests replacing text inspection. Two live bugs
found by execution: PowerShell's empty-string argument drop and 7.4+'s
Stop-preference native-exit behavior. Scaffold-verified; RESYNC entry.
Worker full suite 2621/13 green.
<!-- fig: cmd="python -m pytest -q -n auto" rev=27a65c19 -->

### WI-478 — Contracts marker-line grammar (sonnet worker) — CLOSED complete

Marker-line-only grammar with `ContractsGrammarError` on an ambiguous
continuation (the alternative rejected on measurement: eight modules
legitimately re-mention foreign IF ids in flush-left prose); dispatch.py's
wrap fixed; the two false undeclared warnings gone, proven by a
before/after strict diff whose only delta is those two lines; two
regression tests. 117 arch/dispatch tests + smoke 1209/5 green.

### WI-482 — the three stale anchors (sonnet worker) — CLOSED complete

LLR-087/088 re-pointed to `traj_render._drill_layer_svg/_render_drill` and
`DRILL_SCRIPT` (module cells corrected; each target READ before citing),
LLR-112 to `gen_trajectory.HTML_TEMPLATE`; traced-cell moves only, snapshot
refreshed byte-identical, `check_doc_refs` clean on all three ids,
integrity 0, smoke 1209/5. The planned-symbol declared form deferred behind
WI-472's obligation SR, with reasoning on the row.

### WI-466 — the verified-triple display fix (sonnet worker) — CLOSED complete

The summary guard widened to any-leg-nonzero (was demonstrated-or-attested
only, hiding the common mechanized-only shape); regression test added;
goldens verified unaffected; ratchet re-stamped 4510→4515 with reason. The
attested-vs-mechanized split is visible again on the repo's own run
(69/3/0). test_trace.py 82 passed; smoke 1209/5.

### WI-480 — dev-toolchain currency (sonnet worker) — CLOSED complete

pytest moved to `>=9.0.3,<10` after a throwaway-venv full-suite
qualification produced the identical pass/fail set as 8.4.2 (the shared
two failures were WI-466's golden gap — see below); weekly `pip-audit` SCA
workflow (verified catching then clearing the pytest advisory);
`uv`-generated hash-pinned locks for both Pythons with a loud staleness
check instead of auto-commit (refused under push=human, reasoning in the
workflow); pip-audit + uv ledgered in docs/dependencies.md.

Post-close confirmation from the worker's finishing run: the FULL suite is
fully green under pytest 9.1.1 with the golden fix in — 2626 passed / 13
skipped in 483.65s, exit 0 — and the committed content matches the
worker's authored files byte-for-byte.
<!-- fig: cmd="python -m pytest -q -n auto" rev=94489f7a -->

**The golden episode, recorded for the closing review:** WI-466's widened
guard added the triple line to mechanized-only output; the clean/orphan
goldens (slow-tiered, invisible to the commit-bar smoke) went red at
8d7ff553 and stayed red for one commit until WI-480's qualification run
surfaced them — regenerated deliberately at 74c20704. Two lessons: a
smoke-invisible module can carry a red across a close, and a worker's
"goldens verified unaffected" claim was wrong where the orchestrator's
verification (smoke only) could not catch it.

### WI-481 — live performance budgets (sonnet worker) — CLOSED complete

Four PB rows seeded with warm-run measured bases + fig: markers (trace
0.97s/5s, regen pair 6.46s/20s, check_docs 1.94s/8s, whole hook 7.7s/30s),
declared-absence line retired with its three readers checked, PB watermark
0→4. check_perf moved from vacuous OK to an honest 4-budgets SKIP naming
the unwired metrics emitter — that emitter is the named residue for a
future WI.

### Adjacent findings accumulating for the closing review

- (WI-475 worker) `run.template.{sh,cmd}` carry the IDENTICAL pre-WI-475
  runnability-only pattern — same defect class, product-launcher surface,
  worth its own WI.
- (WI-475 worker) the smoke tier measures ~56s against the declared 60s
  budget on this box — the stamp's headroom is gone; and smoke membership
  is 1214/1216 — the next new smoke module trips the membership ratchet.

- (WI-474 worker) `check_vocab.py:71` declares `Contracts: IF-118`, which is
  NOT its row (IF-118 is gen_open_items→spine_carrier) — and the checker
  verifies only that a cited id EXISTS, never that the row names the citing
  module: a `Contracts:` line can cite any live IF id and be believed. Real
  checker hole.
- (WI-474 worker) LLR-168's detail/code_symbol omit hats.py's entire `audit`
  subcommand (~170 lines incl. the newly declared seam) — Approved row, so
  the coverage amendment is owner-adjacent.
- (WI-474 worker) IF-118/119/120 `notes` cite a retired CMP numbering
  ("this module is CMP-002...") — stale, reads authoritative.
- (step-7 worker) `intake._apply_flips` now writes nothing — whether any
  mechanical ratification authority returns is an owner policy call
  (docstring carries both candidates).
