56f374f6 NOT YET SOUND

## BLOCKER

- docs/plans/2026-10-04-wi788-design/README.md:352 — A1 explicitly leaves chapter 2’s exclusion table “unchanged,” but its family assignments make two draws empty:
  - `plan-critique` is OPENAI-only (README.md:380), while 2-sessions-routing-accounts.md:121 excludes the critiqued drafter’s **family**. Critiquing the OpenAI half of a dual round has no eligible family.
  - `author` is ANTHROPIC-only (README.md:379), while 2-sessions-routing-accounts.md:123 excludes builder **families**. An author call adopting Anthropic-built text likewise has no eligible family.
  
  Fresh sessions cannot satisfy these family exclusions. The amendment must explicitly reconcile them; “README wins” does not resolve a table the README declares unchanged.

- docs/plans/2026-10-04-wi788-design/README.md:379 — Anthropic-only `build` and `plan` cannot execute the retained **family swap**. Chapter 3 still requires the incoming family to replan and build after two consecutive CHANGES-REQUESTED (3-planning-tiering.md:300, :304), and its successor acceptance requires that behavior (:409). Starting with Anthropic leaves no eligible incoming family. The owner’s restriction and the approved Q-6 trial need an explicit reconciliation.

## MAJOR

- docs/plans/2026-10-04-wi788-design/README.md:301 — The successor contracts do not allocate and verify the complete A1 replacement. S788-ask’s detailed scope still says today’s phases move “unchanged, except author-derived exclusion” (2-sessions-routing-accounts.md:559); its acceptance names neither the routing table, zero-weight ineligibility nor removal of `DEFAULT_PHASE_TIER`. S788-plan-kinds still names only `plan` and `plan-critique` (3-planning-tiering.md:407). SR-154’s matrix assigns three amendments to ask/single-plan/resolve (README.md:212), while A1 assigns its new amendment to session-families (:369). Builders can satisfy the listed contracts without implementing the amendment. Additionally, A1 requires pacing for every new session (:359), but the row providing pacing depends on ask (:314). The drawn graph is acyclic; the behavioral allocation does not establish that ask is landable from its needs alone.

- docs/plans/2026-10-04-wi788-design/README.md:411 — A2 excludes an exhausted **5-hour** window but does not exclude an exhausted **weekly** budget. With fresh readings and available short windows, account A at 0% remaining and one hour until weekly reset has headroom approximately −0.6; account B at 10% remaining and 100 hours until reset has headroom approximately −49.5. The stated maximum-headroom rule selects exhausted A although B can run. The rule also leaves the freshness cutoff and calculation of elapsed weekly fraction unspecified, despite requiring stale-reading fixtures. These need concrete definitions in the pacing contract.

## MINOR

- docs/plans/2026-10-04-wi788-design/README.md:373 — The owner-attributed values table includes coordinator interpretations: introducing `plan-dual`, assigning `author` to Anthropic, and assigning unnamed review kinds to OpenAI. OI-104 explicitly labels this mapping **“The coordinator’s reading”**; D-032 and D-033 likewise disclose delegated decisions. Preserve that distinction on the ruling page, particularly where “Codex for authoring” is interpreted as author-review editing only.

- docs/decisions/wi-788.toml:235 — D-032 says “every other plan kind is ANTHROPIC only,” but README.md:380 assigns `plan-critique` to OPENAI. Restrict the statement to the intended drafting kinds.

## Verified

The Q answers, Q-4’s move to OI-105, A3’s optional third agent, and A4’s approval with iteration are carried through. Changes 26–27 preserve the lane guard against each commit’s parent and exempt the landing squash. All seven `reviewed = true` entries have support in OI-104, including its explicitly disclosed D-012→D-010 reading. The decisions TOML parses, contains 34 complete entries, and leaves D-032–D-034 unreviewed. A1’s code claims are correct: existing weights are per resolved row and phase; the family filter precedes pins and weights; zero remains fallback-only; phase defaults reside in code with overrides. The graph has 21 successor rows and is acyclic. No remaining “twenty rows” wording appeared in the reviewed paths. The worktree remained clean.

## Commands

Repeated reads and line-number display loops are grouped below; all commands were read-only.

- `git status --short` — clean throughout and at completion.
- `git diff c5e0a154 56f374f6 -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml docs/work/active/wi-788` — inspected the scoped fold.
- `git show 68fda4fe:docs/log.d/2026-10-04-owner-rulings-oi104.md` — read the trunk ruling summary.
- `git show 68fda4fe:docs/requirements/open-items.toml`, followed by PowerShell extraction of OI-104/OI-105 — compared owner words, coordinator reading and provisioning hold.
- `Get-Content` commands for `CLAUDE.md`, `.agents/skills/antidote/SKILL.md`, the amended README, chapters 2–4, `docs/decisions/wi-788.toml`, `project-trajectory/PROCESS.md`, `project-trajectory/decisions.template.toml`, routing code, brief code, `docs/agents-enabled` and SR-154 — inspected rules, exclusions, successor contracts and decision fields.
- `rg -n` searches across those sources for routing functions, weights, pins, tiers, families, planning kinds, swaps, successors, independence, pacing, reset windows, counts and effort settings — located and cross-checked the cited claims.
- `git log --oneline c5e0a154..56f374f6 -- docs/work/active/wi-788` — confirmed the retitle was its own commit.
- `git rev-parse --short HEAD` — confirmed `56f374f6`.
- `git diff --check c5e0a154 56f374f6 -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml docs/work/active/wi-788` — no whitespace errors.
- PowerShell in-memory graph traversal and successor-table count — 23 graph nodes, 34 edges, all nodes topologically visited; 21 successor rows.
- `git diff --name-only c5e0a154 56f374f6 -- docs/plans/2026-10-04-wi788-design docs/decisions/wi-788.toml docs/work/active/wi-788` — confirmed six changed files in scope.
- `C:/Projects/ai-template/.venv/Scripts/python.exe -B -c` with in-memory `tomllib` parsing and field checks — 34 decisions, no malformed required fields; verified reviewed marks. No pytest or trajectory check ran.