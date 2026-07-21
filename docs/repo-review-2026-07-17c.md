# Deep repository review (third sitting) — 2026-07-17c

Scope: the full active repository as of `36d945e` (branch `dualplan-routing-fix`)
— kit scripts and templates, the meta-repo's self-adopted requirements spine,
tests, launchers, hooks, CI, dependencies, configuration, security posture, and
Git history. Excluded as historical working memory per the review brief:
`docs/log.md`, `docs/archive/**`, `docs/iteration/**`, and the owner-only
`OWNER_SCRATCHPAD.md`.

Context that shaped this pass: **two full review passes were completed earlier
today** ([repo-review-2026-07-17.md](repo-review-2026-07-17.md), commits
`6ceb172`/`3ee0a3b`; [repo-review-2026-07-17b.md](repo-review-2026-07-17b.md),
commits `da772c2`/`42a30bc`). Only five commits have landed since — the
WI-215/216/217 prompt-delivery fixes plus a merge. This report is a genuine
fresh pass over the whole active tree, but its **deepest scrutiny went to the
post-`42a30bc` delta** (the code with the least review history) and to the
cross-file consistency that delta could have broken. Items the prior reports
already dispositioned and that remain unchanged are carried forward by
reference, not re-litigated.

## 0. Unfixed items and why

Filled after the fix pass. Confident fixes were applied and verified; the
following remain open deliberately.

| Item | Final state | Why it remains unfixed |
|---|---|---|
| L1 — codex detection is a name heuristic | Left as-is; trade-off documented in the helper's docstring | Any stronger detection (probing `--help`, a registry column) is speculative design for a failure nobody has hit; the heuristic is bounded (basename prefix) and its worst case is one unknown flag on a lookalike CLI. Needs an owner call on whether a `ResultCapture`-style registry column is worth a schema change. |
| L2 — `datetime.utcnow()` ×5 (Py 3.12 deprecation) | Deferred | Replacing with aware datetimes changes naive/aware comparison semantics in `blackout_wake` and its callers; it needs its own small WI with focused tests, not a drive-by inside a review commit. No behavior change today on any supported Python. |
| C1 (carried, 17/17b §0) — `agent_loop.py` monolith, now 6,313 lines; `dispatch_run` C901 | **Now filed as [WI-218](archive/specs/WI-218.2026-07-20.md)** (2026-07-18 correction) | Same reasoning as their H3: high-risk architectural work needing characterization tests and its own review. *Correction:* this report originally said the prior reports had "filed" a decomposition campaign — they had only **recommended** one; no WI existed. Note the prior campaign that did land (WI-080/081, 2026-07-16) decomposed the `main()` *functions*, not the files. WI-218 (verbatim-move file split, no compaction) now tracks the file-level work. |
| C2 (carried) — no LICENSE file (WI-097/OI-4) | Blocked on the owner's public/private intent | No safe default exists. The only carried item a downstream copy could be legally blocked on. |
| C3 (carried) — 51 orphan-doc warnings (52 with this report) | Deferred to the documentation-policy WI from the first report | Retention-policy question, not a mechanical fix. |
| M6 — WI-216's Deliverable cell states "claude keeps {prompt}", reversed by WI-217 | Left as-is | Deliverable cells are point-in-time closure records (log-like); WI-217's own cell records the reversal. Rewriting history cells to match later state would violate the registry's evidence discipline. |
| M7 — `agents.template.csv` GOOGLE row still uses `{prompt}` | Left as-is, deliberate | The gemini CLI's stdin-prompt behavior is **unverified**; the template comment explicitly says "keep `{prompt}` only for a CLI with no stdin prompt path". Changing it without live verification would ship an untested claim downstream — the exact failure shape WI-216 exists to prevent. |

Confident fixes completed in this pass (details in the findings below):

| Finding | Disposition |
|---|---|
| H1 | `run_interactive` now pipes a no-`{prompt}` prompt with `text=True` (was a guaranteed `TypeError`); regression test added. |
| H2 | This repo's own `agent-resume.cmd`/`.sh` `AGENT_CMD` drops `{prompt}` — the ambient-template path (routing-off hats and the dual-plan **arbiter** even under routing-ON) now delivers via stdin and is immune to the Windows argv caps. |
| M1 | The retired "no `{prompt}` = the resume prompt is appended as its final argument" contract corrected to the stdin contract in the module docstring, both live launchers, and both shipped launcher templates (+ `test_bootstrap` example asserts updated with them). |
| M2 | README's unattended-operation bullets no longer describe the retired resume-from-`status.md` serial driver; the "(in development, phase v4)" marker corrected to reflect the landed dispatcher. |
| M3 | `PROCESS_OPTIONS.md`'s pair-row *Access* bullet now documents the stdin prompt-delivery contract (one sentence; byte budget re-checked with the guard). |
| M4 | `_dp_routes` and the dual-plan runtime fallback now pass the registry's `tag-rank` override into `resolve_enabled`, matching `main()`; regression test added. |
| M5 | `preflight`'s guidance example and `--agent-cmd`'s help text recommend the stdin (no-`{prompt}`) form. |
| L3 | `map_preflight`'s `build_argv(...)[0][0]` double-index unpacked to match the sibling call site. |

Final verification after remediation is recorded in §4.

## 1. Executive summary

**Strengths.** The repository remains in unusually strong shape, and the
verification culture is real, not performative: the full suite green at
baseline (**1,059 passed / 3 skipped**, cross-platform CI including the Python
3.8 floor plus a floating-latest canary), the **full G3 gate PASS on all 16
steps** (format · lint · tests+coverage · dupes · derived-gate · traceability ·
privacy · doc-navigability · perf-budgets · design-flows · trajectory ·
arch-map · trajectory-map · status-map · okf · skills-sync), strict
traceability clean (SN=25 SR=66 LLR=76 TC=76, zero orphans, 61 seams, 5
components), an acyclic 215-WI trajectory, 0 broken doc links, a pinned dev
toolchain with written rationale for every pin, and no security smells. The
WI-215/216/217 work itself is a model of downstream-feedback discipline: each
gilbert-surfaced defect landed with a failing-first test, a spine amendment
(LLR-026/TC-026), and an honest "why our own tests missed it" note.

**The critical theme of this pass: the WI-216/217 contract change is only
half-propagated.** The stdin prompt-delivery fix was applied to the registry
rows and the headless engine, but:

1. The **interactive entry crashes outright** on the new template form
   (`subprocess.run(input=<str>)` without `text=True` — a guaranteed
   `TypeError`, verified by probe). The one path meant for a human to debug a
   broken run is the one path the new contract breaks.
2. The **ambient `AGENT_CMD` path still delivers via argv** — this repo's own
   launchers kept `{prompt}`, and the dual-plan **arbiter** rides the ambient
   template even when routing is ON. WI-217's own evidence (~70K critic briefs
   exceed the 32,767-char CreateProcess cap) applies verbatim to the arbiter
   prompt, which embeds *both* plans plus rubric plus coverage report. The
   defect class WI-216 fixed was still reachable through the front door.
3. **Five separate pieces of shipped documentation still teach the retired
   contract** ("no `{prompt}` = the prompt is appended as the final
   argument") — the module docstring, both live launchers, and both shipped
   launcher templates — and the canonical routing spec (`PROCESS_OPTIONS.md`)
   never mentions stdin delivery at all. An adopter reading the normal entry
   points learns behavior that stopped being true two commits ago, and the
   difference is exactly the crash-vs-works line on Windows.

All of the above were fixed in this pass. The remaining open items are the
prior reports' structural carries (the 6,313-line coordinator, the missing
license, orphan-doc policy) plus two deliberate deferrals with reasons in §0.

## 2. Findings

Severity reflects impact on the kit's stated goals (maintainable, trustworthy,
copy-ready downstream): **Critical** = breaks a core promise now; **High** =
real defect or trap an adopter will plausibly hit; **Medium** = correctness of
record / consistency debt; **Low** = polish.

### Critical

None new. (The prior passes' Critical/High-class items were remediated in
`3ee0a3b`/`42a30bc` and spot-verified still-fixed in this pass — the
exclusive-key starvation fix, the PlanMode schema pin, and the `blocked`
lifecycle state all hold under the current suite.)

### High

**H1. `run_interactive` crashes with `TypeError` on any no-`{prompt}` template.**
- **Location:** [agent_loop.py:5063](../project-trajectory/scripts/agent_loop.py#L5063)
  (pre-fix): `proc = subprocess.run(argv, cwd=str(root), input=stdin_input)`.
- **Problem:** WI-216 made `build_argv` return `(argv, stdin_input)` and every
  headless call site pipes correctly through `run_session`. The interactive
  path instead hands the str to `subprocess.run(input=…)` **without
  `text=True`**, which raises `TypeError: a bytes-like object is required, not
  'str'` (verified by direct probe on this machine's Python 3.8). The path
  fires whenever `--interactive` resolves to a template without `{prompt}` —
  which, after WI-217, is every registry row and (post-H2) the recommended
  `AGENT_CMD` form, reached via the documented fallback chain
  `--interactive-cmd → AGENT_CMD_INTERACTIVE → AGENT_CMD`.
- **Why it matters:** `--interactive` is the "grind from a single point" entry
  a human uses precisely when the unattended run is misbehaving. A crash here
  is a trap at the worst moment, and none of the 1,059 tests covered it (the
  new stdin tests exercise `run_session`, not `run_interactive`).
- **Fix applied:** branch on `stdin_input`: `None` keeps the exact historical
  call (terminal inherited); a str pipes with `text=True`. Regression test
  added to `tests/test_session_stdin.py` driving `run_interactive` end-to-end
  with a no-`{prompt}` template.

**H2. The ambient-template path still delivers prompts via argv — including the
dual-plan arbiter under routing-ON.**
- **Location:** [agent-resume.cmd:25](../agent-resume.cmd#L25) /
  [agent-resume.sh:24](../agent-resume.sh#L24) (`AGENT_CMD=claude -p {prompt} …`),
  reaching [agent_loop.py:1420](../project-trajectory/scripts/agent_loop.py#L1420)
  (`_dp_session(template, model, prompt, …)` — the arbiter always rides the
  ambient template) and every routing-off session.
- **Problem:** WI-217's registry change moved claude/codex rows to stdin, but
  the meta-repo's own launcher template — the ambient `AGENT_CMD` used by
  routing-off mode and by the dual-plan arbiter even when routing is ON —
  kept `{prompt}`. WI-217's own recorded evidence is that critic-class briefs
  (~70K chars) exceed even the 32,767-char CreateProcess cap; the arbiter
  brief embeds both plans + rubric + coverage report and is the same size
  class. On Windows that session dies at launch as apparent nonresponse — the
  exact gilbert failure shape, still reachable.
- **Why it matters:** the fix that closed WI-216/217 is silently incomplete on
  the very machine that dogfoods it. A future dual-plan round on this repo
  (routing-ON) would page with "session failed at ARBITER run 1" and no
  indication why.
- **Fix applied:** dropped `{prompt}` from both live launchers' `AGENT_CMD`
  (stdin delivery for `claude -p` was verified live during WI-217 per the WI
  record, and `run_session`'s pipe path is test-covered); comments corrected
  (see M1). `AGENT_CMD_INTERACTIVE` deliberately keeps `{prompt}` — an
  interactive session wants the terminal attached, and H1's fix makes the
  fallback safe regardless.

### Medium

**M1. Five shipped surfaces still document the retired append-to-argv
contract.**
- **Location:** [agent_loop.py:14-16](../project-trajectory/scripts/agent_loop.py#L14)
  ("a template without `{prompt}` gets the resume prompt appended as its final
  argument"), [agent-resume.cmd:18-19](../agent-resume.cmd#L18),
  [agent-resume.sh:18-19](../agent-resume.sh#L18),
  `project-trajectory/scripts/agent-resume.template.cmd:17-18`,
  `agent-resume.template.sh:17-18` ("no `{prompt}` = the resume prompt is
  appended").
- **Problem:** doubly stale — the *append* mechanics were replaced by stdin
  delivery (WI-216), and the *resume prompt* concept was retired with the
  serial driver (WI-210). The launcher comment is the first thing an adopter
  reads when wiring `AGENT_CMD`, and the difference between "appended to argv"
  and "piped to stdin" is precisely the works-vs-dies-at-8191-chars line the
  whole WI-216 episode was about.
- **Why it matters:** the kit's own core principle is single-source-of-truth,
  decompose-don't-paraphrase; these are five paraphrases of a contract that
  changed, all now wrong. This is the recurring failure mode the
  enforcement audit names: prose restating code is the weakest enforcer.
- **Fix applied:** all five corrected to state the real contract (`{prompt}`
  in the template = argv; omitted = piped to stdin, immune to the OS
  command-line caps). The shipped template examples updated to the
  no-`{prompt}` form and `tests/test_bootstrap.py`'s two example asserts
  updated with them.

**M2. README describes the retired serial resume model as the current
unattended layer.**
- **Location:** [README.md](../README.md) lines 53–58 — "Fresh headless sessions
  resume from `docs/status.md` until `docs/run-state` reaches an end state";
  "Parallel-by-default execution *(in development, phase `v4` …)*".
- **Problem:** WI-210 deleted the resume-from-status driver: session scope is
  now a worker assignment, reviewer brief, or critique brief, and
  `docs/run-state` is dispatcher-*generated*, not read. Phase 4 is at derived
  G3 with the dispatcher landed as the plain-launch default, so "in
  development" undersells shipped, gate-passed behavior.
- **Why it matters:** the root README is the kit's storefront and the one
  place a prospective adopter forms their mental model. It currently teaches
  an architecture that no longer exists. (The 17b pass fixed this README's
  *configuration table*; these two bullets sit forty lines above it and were
  missed.)
- **Fix applied:** both bullets reworded to the dispatcher/worker model
  (plain launch = the dispatcher; sessions are explicit assignments;
  run-state is generated).

**M3. The canonical routing spec never mentions the stdin delivery contract.**
- **Location:** `PROCESS_OPTIONS.md` "Unattended operation" → the pair-row
  *Access* bullet ("**`CmdTemplate`** (`{model}`/`{prompt}` slots) + `Env` …").
- **Problem:** after WI-216/217 the load-bearing downstream-facing behavior —
  omit `{prompt}` and the kit pipes the prompt to the CLI's stdin, immune to
  the Windows 8191/32767 caps; codex sessions additionally get
  `--output-last-message` read back as the result — is documented only in a
  CSV comment and code docstrings. `PROCESS_OPTIONS.md` is the spec of record
  the kit's own docs tell adopters to read.
- **Why it matters:** an adopter designing a registry row for a new provider
  CLI has no normative statement of when to include `{prompt}`; the CSV
  comment is guidance-adjacent, not spec.
- **Fix applied:** one sentence added to the Access bullet; the file's byte
  budget re-verified with the `byte-budget-guard` skill.

**M4. Dual-plan routing ignores the registry's declared `tag-rank` override.**
- **Location:** [agent_loop.py:1167](../project-trajectory/scripts/agent_loop.py#L1167)
  (`_dp_routes`) and [agent_loop.py:1331](../project-trajectory/scripts/agent_loop.py#L1331)
  (the mid-round fallback): `agent_route.resolve_enabled(enabled, registry)` —
  no third argument — while [agent_loop.py:6043-6046](../project-trajectory/scripts/agent_loop.py#L6043)
  passes `load_tag_rank(docs / "agents.csv")`.
- **Problem:** a registry that overrides the maturity ranking (`# tag-rank: …`
  or `AGENT_TAG_RANK`) gets **different version-less token resolution** in
  dual-plan rounds than in every ordinary session — the same enable-list can
  route a different concrete row depending on which engine path asks.
- **Why it matters:** silent, config-dependent divergence between two paths
  the docs describe as one selection policy; exactly the class of latent
  routing-ON defect WI-215 just fixed two instances of, in the same two
  helpers.
- **Fix applied:** both call sites now load and pass the tag rank; covered by
  a regression test in `tests/test_dual_plan_routing.py`.

**M5. The kit's own guidance examples still recommend the argv form.**
- **Location:** [agent_loop.py:2231](../project-trajectory/scripts/agent_loop.py#L2231)
  (preflight's "fill the AGENT_CMD slot" example: `claude -p {prompt} …`),
  [agent_loop.py:4656](../project-trajectory/scripts/agent_loop.py#L4656)
  (`--agent-cmd` help: "({model}/{prompt} placeholders)").
- **Problem / why it matters:** the error message an operator sees at the
  exact moment they are wiring `AGENT_CMD` recommends the form the kit itself
  just migrated away from for cap-safety.
- **Fix applied:** example and help text updated to the no-`{prompt}` form
  with a one-clause explanation.

### Low

**L1. Codex detection in `run_session` is a name heuristic.**
[`_codex_lastmsg_setup`](../project-trajectory/scripts/agent_loop.py#L2455)
appends `--output-last-message <tmpfile>` to any argv whose basename starts
with `codex` (case-insensitive). A lookalike CLI (`codex-proxy`) would receive
an unknown flag; a template that already declares its own
`-o/--output-last-message` gets a second one (codex last-wins, so the
operator's declared file silently stops receiving the result — the kit reads
its temp file instead). Bounded blast radius, no known real-world hit; left
as-is with the trade-off noted (reason in §0).

**L2. `datetime.datetime.utcnow()` ×5 in `agent_loop.py`.** Deprecated since
Python 3.12 (warns; still correct). Migration to aware UTC datetimes touches
`blackout_wake`'s naive-datetime contract and deserves its own scoped change.
Deferred with reason in §0.

**L3. `map_preflight` indexes `build_argv(...)[0][0]`.**
[agent_loop.py:4907](../project-trajectory/scripts/agent_loop.py#L4907) — correct
but obscure beside the destructured `argv, _ = build_argv(…)` 35 lines above.
Fixed to match the sibling.

**L4. WI-216's Deliverable cell asserts "claude keeps {prompt}", which WI-217
reversed a commit later.** Registry closure cells are point-in-time records,
so this is history, not error — noted so a future reader of WI-216 alone
doesn't take the claim as current. No change (reason in §0).

### Positive / good practices worth naming

- **Downstream-defect discipline.** WI-215/216/217 each carry: the gilbert
  commit that surfaced the gap, a failing-first regression test, the honest
  "why our own tests missed it" note (TC-076's plain-text fixture), and a
  spine amendment (LLR-026/TC-026 updated in the same commits).
- **The stdin implementation itself is careful.** The daemon feeder thread
  preserves the SN-016 no-wedge invariant under a non-draining child; the
  stdout pump prevents the reverse deadlock; the timeout path cleans up the
  codex temp file; `test_session_stdin.py` proves the 20,044-char case
  end-to-end through a real `.cmd` shim on Windows.
- **Mechanical honesty end to end**: strict trace (zero orphans over 243
  rows), acyclic 215-WI graph, freshness-gated generated artifacts, a derived
  (not hand-set) gate, and a CI matrix that actually runs the 3.8 floor plus a
  scheduled unpinned canary so pins can't rot silently.
- **Security posture is deliberate**: permission-bypass flags are confined to
  the consent-bannered unattended layer and documented as consent; the privacy
  gate + pre-push backstop exist; sweeps found no bare `except:`, no
  eval/exec/os.system, no credential material, and the one `shell=True`
  (`run_menu.py`) runs the user's own declared `[run]` command with the
  rationale written where the risk lives.
- **The test suite is organized by contract, not by convenience** — 60+ files
  named per module/behavior, hermeticity guards (the `AGENT_*` scrub in
  `conftest.py` with the live incident that motivated it recorded in place),
  and cross-platform fixtures that build real scaffolds.
- **`agent_route.py`, `schedule.py`, and the `plan_*` modules** read as
  genuinely pure libraries with single responsibilities, machine-readable
  reason codes, and cap enforcement that raises on caller bugs
  (`RoundCapError`) instead of absorbing them.

## 3. Recommendations and next steps

1. **Schedule the coordinator decomposition now.** `agent_loop.py` crossed
   6,300 lines and every recent defect (WI-215's tuple bug, H1 and M4 here)
   lived in the seams between its embedded subsystems (routing, dual-plan,
   dispatcher, session I/O). Both prior reports deferred decomposition to a
   campaign; this pass adds the observation that the file grew again in the
   meantime. Suggested first cut: extract the session-launch layer
   (`build_argv`/`run_session`/codex capture — a clean seam already covered by
   `test_session_stdin.py`), then the dual-plan runner, each behind its
   existing IF row.
2. **Adopt a "contract-change checklist" for retired behaviors.** WI-216/217
   changed a contract that five documents restated. The enforcement audit
   already names prose-restatement as the weakest enforcer; a one-line rule in
   the session protocol ("grep the repo for the old contract's phrases before
   closing a WI that changes one") would have caught M1/M2/M3/M5 mechanically.
3. **Verify the gemini stdin path** (or record that it must keep `{prompt}`)
   the next time that CLI is exercised live, so the template's third example
   carries the same verified status as the other two.
4. **Close the carried owner decisions**: OI-4 (license — C2) is the only item
   in this report a downstream copy could be legally blocked on.
5. **Keep the dual-plan round's routing-ON path in the regression net.** It
   was dark until gilbert lit it; `test_dual_plan_routing.py` now covers the
   selection layer, but an end-to-end routing-ON round with a stream-json fake
   CLI would close the last fixture gap TC-076's history exposed.

## 4. Verification record

Baseline (before fixes, at `36d945e`): full suite **1,059 passed / 3 skipped**
(109.6 s, `-n auto`); **full G3 gate PASS on all 16 steps** (tests+coverage
290.7 s within it); `trace.py --strict` clean (SN=25 SR=66 LLR=76 TC=76,
0 orphans, 61 interfaces, 5 components, 0 findings); `check_trajectory.py
--strict` clean (215 WIs, 203 done, acyclic); `check_docs.py` 0 broken links /
51 orphan warnings.

After fixes (this working tree):

- Full suite **1,061 passed / 3 skipped** (120.7 s, `-n auto`) — the +2 are the
  H1 and M4 regression tests, both **proven to fail against the pre-fix
  engine** (stash-run: 2 failed) before passing with the fix.
- Smoke tier (the per-commit bar): **841 passed / 2 skipped** (62.1 s).
- Ruff format + lint: clean (93 files).
- `check_docs.py --stale`: **0 broken links** / 52 orphan warnings (the +1 is
  this report, counted under carried item C3); `gen_skills_index
  --check-agents`: all 12 per-agent skill copies match source.
- Spine untouched: no registry or trace-surface edits in this pass (the fixes
  live under the existing SR-026/LLR-026 and SR-066/LLR-076 umbrellas, whose
  Detail text already describes the stdin/routing contracts being repaired).
- Byte deltas (the budget-guard report shape): `AGENTS.template.md`
  **9,978 → 9,978** (untouched, 22 B headroom); `PROCESS.md` **60,169 →
  60,169** (unchanged); `PROCESS_OPTIONS.md` **155,536 → 156,059** (+523 this
  edit: the stdin prompt-delivery contract added to the pair-row Access
  bullet — M3; baseline re-stamped **155,819 → 156,059** in the
  byte-budget-guard skill, source + both tracked copies, this commit).
