d5f243bb NOT YET SOUND

## BLOCKER

none

## MAJOR

- project-trajectory/scripts/coordinator_guard.py:743 — **The Windows successor inherits unusable console streams.** The launcher redirects stdin, stdout and stderr to `NUL`. A Windows child probe retaining the declared creation flags confirmed EOF on stdin and failed `GetConsoleMode` checks for all three handles. The new console therefore does not provide the intended interactive coordinator input or output.

- project-trajectory/scripts/coordinator_guard.py:684 — **Launch failures can strand the consumed request.** A prompt-file write failure occurs outside the restoration handler. A simulated disk-full error left the request consumed and the successor token installed. Separately, a launcher exiting 42 was reported as successfully launched, with no request restored: `launch_detached` checks process creation, not launcher success. Both violate the required failed-launch recovery.

- project-trajectory/scripts/coordinator_guard.py:583 — **Markdown headings inside the fenced prompt break extraction.** A valid handoff containing `# Coordinator role` inside its session-prompt fence returns `None`, causing `request_relaunch` to reject it. Heading detection runs before fenced-content handling and changes the section state while inside the prompt.

- tests/test_coordinator_guard.py:7 — **The required compaction fixture evidence is missing.** The test header explicitly says the boundary shape was neither documented nor observed locally; `Transcript.boundary` manufactures the exact shape the reader recognizes. TC-315 nevertheless describes “recorded transcript fixtures.” Passing this synthetic compaction case does not establish the required version-specific selection across a real compaction boundary. This is an unfinished Done-when item, not a claim that the guessed shape necessarily differs from production.

- docs/requirements/system-requirements.toml:1739 — **SR-229 omits the authorized dispatcher exception.** Its requirement and acceptance criteria promise refusal for non-holders and draining holders without qualification. `integrate.claim(..., dispatch_lock_held=True)` deliberately bypasses those refusals, as D-001 permits. A dispatcher claim during drain contradicts the SR even though it follows the recorded implementation decision. Scope the capability text to the guarded admission route.

- docs/reviews/wi-822-context-guard/terra-spine-r1.md:17 — **The new module’s interface obligation was incorrectly dismissed.** The guard provides a call surface to the integrator and consumes shared runtime-store helpers, yet no interface rows or contract declarations were added. PROCESS.md §8 requires new modules to mint those seams and headers before implementation. Absence of a `Contracts:` declaration is the missing work, not evidence that no contract exists; the resulting connectivity warning confirms that these crossings remain undeclared.

## MINOR

- project-trajectory/scripts/coordinator_guard.py:244 — **Rounding changes admission.** With a 1,000,000-token window, 499,600 tokens is 49.96%, but the reader returns 50.0% and permanently latches the 50% guard. Compare unrounded occupancy for admission.

- tests/test_coordinator_guard.py:453 — **The pre-tool claim assertion passes without the admission guard.** Its fixture contains no queued WI. Running the pre-change integrator against that fixture also returns 1, for “0 queued spec(s).” Assert the guard refusal reason or provide an otherwise admissible claim.

- docs/requirements/low-level-requirements.toml:3175 — **LLR-301 assigns the wrong behavior to `exec_claude`.** It says that function invokes the guard’s command-line operations; the function actually invokes `claude` with the extracted prompt. `main` dispatches the guard operations.

- docs/test/test-cases.toml:3204 — **TC-317 and TC-318 overstate their Smoke coverage.** Their required evidence includes CLI, wrapper, real-Git and platform-launcher tests in `test_coordinator_guard_e2e`, which the change explicitly excludes from Smoke. A Smoke run cannot execute the complete methods these rows declare.

## Verified

The tested lease identity, silent-holder retention, recorded release, successor-token transfer, persistent latch, event reminders, ownership checks and concurrent request acquisition behave as intended. Threshold-zero behavior is inert. Hook registration matches the [official hook reference](https://code.claude.com/docs/en/hooks). The new SR requirement cells comply with R2. Existing registry changes are limited to LLR-140’s detail and LLR-270’s symbols/detail; no Status flips occurred. Shipping inventory and a RESYNC entry anchored at trunk commit `176b6aef` exist. The worktree and index remained unchanged. Actual Claude exit-survival behavior remains unverified.

## Commands

Repeated read/search commands are grouped below.

- `Get-Content` on `CLAUDE.md`, session-protocol, antidote and deep-module-design skills, and relevant PROCESS.md sections — read contributor, review, traceability, tier and interface rules.
- `Get-Content` on the complete WI, spec of record, decisions, Terra report, three scope reviews and their briefs, status, coordinator log and handoff — checked scope, rulings and prior findings.
- Numbered/ranged `Get-Content` reads of the guard, integrator, session-store code, tests, settings, launchers and amended registries — checked implementation and evidence.
- `git status --short`; repeated `git status --porcelain`, `git diff --quiet`, `git diff --cached --quiet` — clean; final worktree/index checks exited 0.
- `git diff --stat`, `--name-only`, `--numstat`, and scoped diffs for `883b3edf..d5f243bb` — inspected the change inventory and authored changes; large generated HTML output was truncated.
- `git diff --check 883b3edf..d5f243bb` — no whitespace findings.
- `git log --oneline --first-parent 883b3edf -12`; `git show --format=fuller --no-patch 74b0fc96`; `git rev-parse HEAD`; `git merge-base --is-ancestor 176b6aef 883b3edf` — confirmed reviewed tip, build record and trunk anchor.
- `rg` searches for scope, symbols, backlinks, tiers and seams; `Get-ChildItem` on the scope-review directory — located relevant rules and evidence. One malformed bracket regex failed and was corrected using `rg -F`.
- `Get-Command claude` — resolved the installed native `claude.exe`.
- Official hooks-reference `open`/`find` calls — checked event and output contracts.
- `$env:GIT_CEILING_DIRECTORIES = "C:/Projects/ai-template.wt"`; `$env:PYTHONDONTWRITEBYTECODE = "1"`; `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/wi-822 tests/test_coordinator_guard.py tests/test_coordinator_guard_e2e.py tests/test_session_keep.py tests/test_integrate.py tests/test_dogfood_sync.py` — **217 passed, 1 skipped, 1 failed in 48.14s**. The failure was Git Bash startup’s `CreateFileMapping` access error, before launcher assertions.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0: **clean (820 work items, 723 done, 26 cancelled, graph acyclic)**; advisory warnings remain.
- PowerShell Python-stdin probes, confined to `review-tmp` — reproduced premature rounding, fenced-heading rejection, failed-child consumption, prompt-write recovery failure and Windows `NUL` handles.
- Python-stdin pre-change integrator probe — confirmed the claim assertion returns 1 before this change.
- Python-stdin TOML comparison of both committed revisions — confirmed the exact existing-row amendments and absence of Status flips; final comparison used explicit UTF-8 decoding.