70146dd3 NOT YET SOUND

## Round-1 findings

- **BLOCKER 1 — resolved:** README.md:352 explicitly converts every table family exclusion, including `plan-critique` and `author`, into a preference; 2-sessions-routing-accounts.md:113 acknowledges the amendment.
- **BLOCKER 2 — resolved:** README.md:366 defines the swap as a fresh session when only one family is eligible; 3-planning-tiering.md:303 carries that reconciliation.
- **MAJOR 1 — resolved:** README.md:382 allocates A1’s implementation and fixtures, including `plan-dual` and SR-154; :394 makes pacing a later replacement, allowing ask to land independently.
- **MAJOR 2 — partly resolved:** README.md:442–456 defines window arithmetic, weekly exhaustion and freshness, but its new model-scoped rule still permits an exhausted account-wide weekly budget.
- **MINOR 1 — resolved:** README.md:405 labels the coordinator’s mappings separately from the owner’s choices.
- **MINOR 2 — resolved:** docs/decisions/wi-788.toml:235 restricts Anthropic-only routing to the other drafting kinds and explicitly assigns `plan-critique` to OpenAI.

README and chapter locations above are under docs/plans/2026-10-04-wi788-design/.

## BLOCKER

none

## MAJOR

- **docs/plans/2026-10-04-wi788-design/README.md:442 — Model-scoped pacing discards the account-wide weekly constraint.** The scoped window replaces the account window, and :450 checks exhaustion only for that selected window and the short window. The referenced Claude feeder reads both the all-model and scoped weekly limits independently. Concrete scenario: halfway through both windows, account A has 0% all-model budget remaining and 90% scoped budget; B has 90% all-model and 10% scoped remaining. Both short windows are available. The stated rule assigns headrooms +40 and −40 and draws exhausted A. Exhaustion must consider every applicable limit, even if pacing uses one selected window.

- **docs/plans/2026-10-04-wi788-design/README.md:388 — The new unchanged-selections fixture contradicts family shares.** A1 requires weights to set family shares (:361), while the shipped table assigns every family weight 1 (:398). Today’s `_weighted_rotation` deliberately selects the first candidate whenever positive weights are equal (project-trajectory/scripts/agent_route.py:683). With Anthropic first and OpenAI second, unrestricted build draws therefore all select Anthropic. Requiring those selections to remain unchanged cannot also verify the declared equal family shares. The fixture must distinguish preserved behavior from the weighting behavior A1 replaces.

## MINOR

none

## Verified

D-035 accurately records the delegated extension, has all required disclosure fields, is high-risk, and remains unreviewed. D-032 agrees with the README. The graph has 21 successor rows, 23 nodes and 34 edges; it is acyclic and matches the table’s `needs`. The amended exclusions preserve independent sessions without introducing a fallback path. The worktree stayed clean; no files were written and no pytest ran.

## Commands

Repeated read and search variants are grouped.

- `git status --short` — clean throughout and at completion.
- `git rev-parse --short HEAD` — `70146dd3`.
- `git diff 56f374f6 70146dd3 -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml` — inspected the fixes.
- `git show 68fda4fe:docs/log.d/2026-10-04-owner-rulings-oi104.md` — read the ruling summary.
- `git show 68fda4fe:docs/requirements/open-items.toml`, with PowerShell extraction — read OI-104/OI-105 and distinguished owner words from coordinator interpretation.
- `Get-Content`, including line-number loops — read CLAUDE.md, the antidote skill, both round-1 review files, README, chapters 2–4, decisions record/template, routing code, and registry/template.
- `rg -n` across those sources — checked routing, weights, tiers, exclusions, swaps, successor allocation and counts.
- `Get-Content project-trajectory/agents-enabled.template` — path absent; `rg --files project-trajectory | rg 'agents-enabled|agents.template'` confirmed the available registry template.
- `rg --files`, `rg -n` and `Get-Content` for the referenced MiniPC-Deployer feeder, timer, tests and NagLight gauge — confirmed simultaneous weekly limits and polling cadence; read tests without running them.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -B -` — in-memory TOML checks passed; corrected an overbroad graph-row extractor, then verified graph/table agreement and reproduced the scoped-window failure.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -B -` — extracted today’s weighting function; counters 0–5 all selected Anthropic at equal weights.
- `git diff --name-only 56f374f6 70146dd3 -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml` — four changed files.
- `git diff --check 56f374f6 70146dd3 -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml` — no whitespace errors.