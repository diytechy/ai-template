f3003bf1 NOT YET SOUND

## Round-2 findings

- **MAJOR 1 — resolved:** docs/plans/2026-10-04-wi788-design/README.md:444 includes every applicable window; :453 uses the smallest weekly headroom; :455 excludes exhaustion in ANY window; :470 adds the account-wide exhaustion fixture.
- **MAJOR 2 — partly:** docs/plans/2026-10-04-wi788-design/README.md:391 clarifies the fixture, but :364 preserves an equal-weight exception that still contradicts the owner’s family-share ruling.
- **Round-1 MAJOR 2 — resolved:** docs/plans/2026-10-04-wi788-design/README.md:447–461 supplies window arithmetic, freshness and exhaustion rules; the new account-wide check closes the remaining exhausted-account case.

## BLOCKER

none

## MAJOR

- **docs/decisions/wi-788.toml:263 — D-036 substitutes priority for equal family shares without an owner amendment.** README.md:362 still states the owner’s answer: “weights set the family share,” but :364 makes equal weights select by enable-list order. Concrete scenario: an adopter enables Anthropic first and OpenAI second, assigns both build weight 1, and starts fresh build sessions. Every draw selects Anthropic; OpenAI’s share is zero. I reproduced six consecutive Anthropic draws from today’s `_weighted_rotation`, while weights 2:1 produced four Anthropic and two OpenAI draws. D-036 accurately describes that shortcut, but its :266 justification does not establish fidelity to the owner’s ruling. Recording it as high risk cannot amend the ruled instruction: project-trajectory/PROCESS.md:455 says approved owner decisions are never re-decided by an agent.

## MINOR

none

## Verified

The pacing counterexample now selects live account B and excludes exhausted A. D-036 is structurally well formed, high-risk and unreviewed; its equal-weight shortcut and consecutive 2:1 example match today’s function. Its substantive justification fails as described above. The graph remains acyclic: 21 successor rows, 23 nodes, 34 edges, matching the table’s `needs`. I found no new empty-draw, fallback-path or dependency regression from these edits. Coordinator mappings remain labelled separately. The worktree stayed clean; no files were written and no pytest ran.

## Commands

Repeated read and search variants are grouped.

- `git status --short` — clean initially and at completion.
- `git rev-parse HEAD` — confirmed `f3003bf1484798f892cb86cbe14f0e7a135e3d62`.
- `git diff 70146dd3 f3003bf1 -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml` — inspected the fixes.
- `Get-Content CLAUDE.md` and both applicable skill files — read governing rules and review guidance.
- `Get-Content` for both prior reviews and both briefs — read outstanding findings and standing instructions.
- `rg --files docs/plans/2026-10-04-wi788-design`; `rg --files docs/work | rg 'WI-788'`; `Get-Content docs/status.md` — located the note, scoped spec and current context.
- `git show 68fda4fe:docs/log.d/2026-10-04-owner-rulings-oi104.md` — read the ruling summary.
- `git show 68fda4fe:docs/requirements/open-items.toml`, with PowerShell extraction — read OI-104/OI-105, including owner words and coordinator interpretation.
- `Get-Content`, including line-number loops, for README, chapters 2–4, decisions record/template and WI-788’s spec — compared amendments, matrices, contracts and decision fields.
- `Get-Content` and `rg -n` for routing code, brief defaults, registry/template and enable-list — checked weighting, exclusions, tiers and enabled families.
- `Get-Content` and `rg -n` for PROCESS and PROCESS_OPTIONS — checked consolidation, delegated decisions and owner authority.
- `rg --files`, `rg -n` and targeted `Get-Content` for MiniPC-Deployer’s feeder and NagLight’s gauge — confirmed independent limits and linear pacing.
- `rg -n ... ai-usage-feeder.timer` — guessed filename absent; directory discovery located `homehub-ai-usage.timer`, whose interval is 10 minutes.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -B -` — in-memory TOML, graph/table, weighted-rotation and pacing checks produced the results reported above.
- `git diff --check 70146dd3 f3003bf1 -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml` — no whitespace errors.
- `git diff --name-only 70146dd3 f3003bf1 -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml` — only README and the decisions record changed.