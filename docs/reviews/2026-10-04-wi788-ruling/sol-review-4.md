486c126a SOUND

## Round-3 findings

- **MAJOR — resolved:** docs/decisions/wi-788.toml:263–266 rejects the first-candidate collapse; docs/plans/2026-10-04-wi788-design/README.md:361–366 now makes positive family weights literal shares, faithfully implementing option (a).
- **Round-2 MAJOR 2 — resolved:** docs/plans/2026-10-04-wi788-design/README.md:393 requires equal-share and 2:1 fixtures. The unchanged-selections requirement is gone; the remaining compatibility wording is a minor issue below.

## BLOCKER

none

## MAJOR

none

## MINOR

- **docs/plans/2026-10-04-wi788-design/README.md:404 — The template still promises “today’s behaviour.”** With Anthropic first, OpenAI second and both build weights 1, today’s function selects Anthropic every time; the revised rule splits draws evenly. This contradicts :364 and D-036’s migration disclosure. Replace the compatibility promise with the declared change.
- **docs/decisions/wi-788.toml:263 — The alternation claim needs a preference qualifier.** Two families eligible for a kind do not necessarily alternate: repeated fresh `judge` calls on Anthropic-authored work prefer OpenAI under README.md:358–360, even when both declared weights are 1. State that alternation applies when both families remain in the weighted draw after preferences and availability.

## Verified

D-036’s selection rule is accurate and faithful to the owner’s option (a); its required fields are valid, it remains unreviewed, and it is listed as high risk. The two minor findings concern migration wording, not the routing rule. I found no new empty draw, fallback path, dependency regression or owner-attribution error. The graph is acyclic: 21 successor rows, 23 nodes and 34 edges, matching the table’s `needs`. The worktree remained clean. No files were written and no pytest ran.

## Commands

Repeated read and search variants are grouped.

- `git status --short`; `git rev-parse HEAD` — clean initially and finally; confirmed `486c126a88a4715828438f4e4943a35449b3cd51`.
- `Get-Content CLAUDE.md` — read governing instructions.
- `Get-Content .agents/skills/antidote/SKILL.md`; `Get-Content .agents/skills/session-protocol/SKILL.md` — read applicable review and standing rules.
- `rg --files docs/reviews/2026-10-04-wi788-ruling docs/plans/2026-10-04-wi788-design` — located reviews, briefs and chapters.
- `Get-Content` for all three prior reviews and their briefs; repeated round-3 read — checked the instruction set and outstanding findings.
- `Get-Content docs/status.md`; `rg --files docs/work | rg '788'`; `git show --stat 68fda4fe` — read session context and located the scoped spec and ruling commit.
- `git diff f3003bf1 486c126a -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml` — inspected the fix.
- `git show 68fda4fe:docs/log.d/2026-10-04-owner-rulings-oi104.md` — read the ruling summary.
- `git show 68fda4fe:docs/requirements/open-items.toml | Select-String ... -Context 0,22` — compared OI-104/OI-105’s owner words and coordinator readings.
- `Get-Content`, including numbered display loops, for README, chapters 2–4, WI-788’s spec, decisions record/template, routing code, brief defaults and registry template — checked routing, exclusions, contracts and disclosures.
- `Get-Content docs/agents-enabled` — confirmed current ordering and unannotated weights.
- `rg -n` across PROCESS, PROCESS_OPTIONS, routing code, registries and design files — cross-checked owner authority, weighting, compatibility claims and successor allocation.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -B -` — in-memory TOML and graph checks passed; six existing equal-weight draws all selected Anthropic, while 2:1 produced four Anthropic and two OpenAI draws.
- `git diff --check f3003bf1 486c126a -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml` — no whitespace errors.
- `git diff --name-only f3003bf1 486c126a` — changes comprise README, the decisions record and round-3 review records.