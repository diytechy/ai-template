ca27479b NOT YET SOUND

**BLOCKER**

none

**MAJOR**

1. project-trajectory/scripts/kitlib/done_when.py:229 — The staged-close matcher excludes `docs/archive/work/complete`, `partial`, and `cancelled`, the required terminal destinations. Moving an unblessed edited spec into the archive returned `staged_closes=[]` and no staged refusal, although directly evaluating the same index returned a hold. tests/test_done_when_blessing.py:144 uses the legacy destination and misses this bypass. This contradicts LLR-309 and TC-325’s close guarantees.

2. project-trajectory/scripts/adjudicate_brief.py:1517 — Combined composition does not integrate its constituent act scopes with authorization. For a `combined` adjudication naming `first-approval:TC-001` and `amendment:LLR-001`, project-trajectory/scripts/acceptance_record.py:801 returns no first-approval scope, and project-trajectory/scripts/acceptance_record.py:894 returns an empty amendment scope. Following the composed approval instructions therefore produces an EMPTY-scope refusal; re-attestation likewise has no authorized scope. The new tests exercise only the Done-when section’s effect, leaving the spec’s requirement that each section be acted on unverified.

3. project-trajectory/scripts/intake.py:1290 — SUCCESSOR intake parses the whole combined verdict using a parser that selects its first `## Dispositions` section. A valid combined verdict with an earlier first-approval RETURN draft and a later Done-when SUCCESSOR draft minted only the RETURN draft; the dropped-scope successor disappeared without refusal. This contradicts LLR-262 and TC-328.

4. project-trajectory/scripts/adjudicate_brief.py:1479 — The Done-when brief omits Context, although project-trajectory/prompts/adjudicate-done-when.template.md:62 requires the adjudicator to decide whether the change preserves the purpose stated there. Two specs with opposite purposes—60 fps mandatory versus an adjustable frame-rate target—produced identical briefs for a 60-to-30 fps change. The judge lacks the evidence needed to choose BLESSED versus SUCCESSOR.

5. project-trajectory/scripts/adjudicate_brief.py:296 — `SITTING: JUDGED kinds=;` with no sections passes combined verdict validation. Both the declared-kind list and heading list become empty, so the comparison succeeds vacuously. A successful adjudicator call can therefore report a valid combined verdict without judging any requested section.

**MINOR**

1. project-trajectory/PROCESS.md:456 — “the owner’s ruling bound to that exact text, which holds the lane’s next build and its close” states the release condition backwards. With a covering ruling, the code releases both transitions. The text should say that absence of a covering blessing holds them.

**Verified**

The requested tests passed: 191 in 75.66 seconds. The trajectory check passed with warnings. Two behavior tests were red against `8c941ab2`. Exact-digest release and subsequent-edit re-holding work in the tested paths. No existing Status cells flipped; the SR Requirement cell remains unchanged, satisfying R2. New back-links produced no new trajectory warnings. The RESYNC entry exists, and its anchor is an ancestor of the supplied trunk base. The worktree remains clean.

**Commands**

All Python runs disabled bytecode writes; no full suite or smoke tier ran.

- `Get-Content` and `rg -n` over the spec, builder notes, rules, changed files, and downstream consumers — inspected requirements, implementation, tests, and act routing. One brace-list search failed PowerShell parsing and was rerun with explicit paths.
- `git diff 8c941ab2..ca27479b` and scoped variants, `--stat`, `--name-only` — reviewed all 29 changed files.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -m pytest -q -p no:cacheprovider -n 2 --basetemp C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/bt-wi-841-sol tests/test_done_when_blessing.py tests/test_adjudicate_brief.py tests/test_intake.py` — 191 passed.
- `C:/Projects/ai-template/.venv/Scripts/python.exe project-trajectory/scripts/check_trajectory.py --strict` — exit 0; clean with warnings.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-sol-probes.py` — confirmed the five MAJOR scenarios.
- `C:/Projects/ai-template/.venv/Scripts/python.exe C:/Projects/ai-template.wt/review-tmp/2026-10-06-wave18/wi841-sol-red.py` — two behavior tests red against baseline scripts.
- Inline TOML comparison using `python.exe -B -` — confirmed changed cells and no Status flips; initial table-name error corrected.
- `git log -1 --format="%h %s" dd595b62`; `git merge-base --is-ancestor dd595b62 8c941ab2` — anchor identified; ancestry exit 0.
- `git diff --check 8c941ab2..ca27479b`; `git status --short` — no whitespace errors; clean worktree.