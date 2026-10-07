37217b47 NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/agent_loop.py:2431 — A structured call failure can still be recorded as accepted. Confirmed with exit 0, `is_error=true`, and a committed valid BLESSED verdict: `classify_outcome` returned `COMMITTED` with `errored=True`, but bookkeeping recorded `accepted` and dispatch released. Acceptance must consume the actual failure signal; the displayed outcome can mask it behind a commit.

2. project-trajectory/scripts/coordinator_adjudicate.py:209 — Reservation cleanup deletes a binding the call does not own. Confirmed through `_inputs`: with `<verdict>.requested` already present and the verdict path absent, reservation succeeds, exclusive binding creation refuses, and `_release` deletes both files. A refused invocation destroys the pre-existing binding. Cleanup must distinguish files this call created.

**MINOR**

1. docs/test/test-cases.toml:2830 — TC-278 places the released-tier rejection cases inside its “With the rung held” clause and promises refusal by row. Both cited tests explicitly release the rung; the new refusal names the verdict and rejects the whole act. The Method must state those cases separately with their actual conditions and result.

2. docs/requirements/low-level-requirements.toml:3236 — LLR-306 says a failed or timed-out coordinator call returns without reading its verdict. Confirmed with a read spy on an exit-1 call: `_report` printed that the verdict was not read, then `record_outcome` read it during validation. The design text and narration do not describe the implemented behavior.

**Verified**

The fourth gate’s ordinary nonzero-exit and timeout cases now record failed, and released-tier acts naming unaccepted verdicts refuse, including mixed approval acts. LLR-310 now distinguishes validation from accepted-verdict consumption. Reviewed the fixed lane, spec, D-001–D-023, changed cells, parser, holds, carrier handling and successor minting. Changed SR requirement cells satisfy R2; existing Status values remain unchanged; 60 changed-function back-links resolve. The RESYNC anchor is a trunk ancestor. All **378 targeted tests passed in 184.66 seconds**; strict trajectory checking passed with warnings. Two representative tests were red against the base. No worktree files were written.

**Commands**

Python runs disabled bytecode writes and used the requested Git ceiling. No full suite or smoke tier ran.

- `Get-Content`, `Select-Object`, `Select-String`, `Where-Object`, `rg -n`, `rg --files` — inspected rules, spec, decisions, earlier review, changed cells, implementation and tests.
- `git diff 76b1d212..37217b47`, scoped and `--stat` variants; `git diff 327adae4..37217b47` — reviewed the full lane and fourth-gate fixes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-final5 tests/test_done_when_blessing.py tests/test_adjudicate_brief.py tests/test_intake.py tests/test_coordinator_adjudicate.py tests/test_snapshot_readers.py tests/test_agent_loop_worker.py` — **378 passed**.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; warnings.
- `python.exe -B C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-final5-probe.py` — confirmed both major findings and the failed-call verdict read.
- `python.exe -B C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-final-red.py` — two representative tests red against `76b1d212`.
- Inline `python.exe -B -`, adapting `wi841-final4-audit.py` to `37217b47` — checked changed cells, Status values, 60 back-links and byte deltas.
- `git merge-base --is-ancestor dd595b62 76b1d212`; `git log -1 --format='%h %s' dd595b62` — verified RESYNC anchor.
- `git diff --check 76b1d212..37217b47` — trailing whitespace in recorded telemetry.
- `git ls-files --eol`, `git status --short`, `git rev-parse HEAD`, and revision comparisons with `HEAD` — checked LF endings and concurrent commits; reviewed code, tests and live registries remained unchanged from the fixed tip.
- Scratch-only `apply_patch` — prepared the reproduction script.