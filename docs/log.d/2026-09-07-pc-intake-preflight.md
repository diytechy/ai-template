## 2026-09-07 — PC intake exposes a scoped-publication composition conflict

Continued the owner's PC instruction from `14ac5251`. The
[preflight](../reviews/pc-intake/preflight.md) reproduces an actual conflict:
the LLR whole-file census requires accepted decisions outside WI-601, while
its immutable scope forbids those decisions. Even assuming valid evidence
references, the real helpers reject that combination. A zero-effect RETURN
can still close; accepted snapshot publication cannot satisfy PC on this
baseline. No primary selection was started.

The actual independent ANTHROPIC-FABLE review approved bounded reversible
intake only, not a repair design or registry acceptance. Its frozen input,
provider metadata and verbatim response are preserved. The record corrects
two unsupported reviewer assumptions using current source: WI-605 already owns
LLR-183, and amendment intake derives one grouped draft per merge. Missing
queued ownership is not proof that historical judgments are absent.

Canonical `intake.stage_mint` in a pristine disposable checkout produced
WI-608 (exact PC spine authoring) and WI-609 (separate scoped-publication
resolution). Copied only the minted specs and watermark under the existing
station locks, then ran the normal regeneration step. Existing adjudication
specs, live registries, snapshots, runtime, tests and pause are unchanged.
The derived stage changed only its provenance line. The two new WIs share
parent SRs but have distinct scopes: singleton authoring versus approval
composition; the trajectory advisory is retained, not suppressed.

Smoke: **1695 passed, 4 skipped in 46.79 s**, **47.1 s** measured wall within
the enforced **90 s** budget. <!-- fig: `.venv/bin/python -m pytest -q -n auto -m smoke`, time.monotonic wall checked by `scripts/check_smoke_budget.py --mode enforce --elapsed`; runtime/test tree at 14ac5251 plus this intake candidate; out/run-logs/pc-continuation/smoke.txt -->
Strict trajectory and documentation checks passed with existing warnings;
normal regeneration passed. No broad code change or phase close, so no
unfiltered implementation-suite result is claimed. No byte-capped guide
changed. Deviation: successful primary acceptance is blocked by the demonstrated
composition constraint, so this continuation completes reviewed intake and
records its resolution scope rather than launching a known-unacceptable turn.
No control window, push, merge to main, code deletion or snapshot write.

Deferred open items: none — the concrete publication issue is now scoped in
WI-609, and the oldest supported upgrade revision remains the already-recorded
owner input for legacy expiry. No new owner ruling is inferred from this intake.
