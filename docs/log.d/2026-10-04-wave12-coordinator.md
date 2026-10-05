Deferred open items: none

## 2026-10-04 — Wave-12 coordinator (owner present): OI-104 ruled, WI-788 landed, the S788 rows filed

- **Owner answers.** The owner answered WI-788's checkpoint questions Q-1 and Q-3
  to Q-12 over the session and confirmed the Q-8 reading. Q-4 moved to its own
  item, **OI-105** (FreeLLMAPI provisioning, pending), with placeholder WI-795.
- **OI-104 ruled**: approved with amendments A1 (routing per kind: family weights
  as literal shares, 0 = not eligible, the kind's tier; every family exclusion a
  ranked preference; this repo builds, plans and adjudicates on Anthropic and
  reviews and judges on OpenAI), A2 (weekly-pace account selection within a
  family, modelled on the owner's HomeHub gauges), A3 (a third-agent option on a
  dual-round disagreement) and A4 (the station authority stands; its landing hold
  time is an iteration point).
- **Independent review of the fold**: Codex 6.1 Sol, four rounds on lane
  `wi-788`. Every finding was confirmed against the note before fixing: round 1
  (2 BLOCKER: empty draws and the swap under a one-family table; 2 MAJOR:
  allocation and pacing arithmetic; 2 MINOR), round 2 (2 MAJOR: an exhausted
  account-wide window, the template fixture), round 3 (1 MAJOR: equal weights must
  be literal shares, as ruled), round 4 SOUND with two wording MINORs, fixed.
  Reviews under `docs/reviews/2026-10-04-wi788-ruling/`.
- **WI-788 landed** by squash (`2e7cd53f`), tip archived (`8642f1e8`), closed on
  the note. The sweep minted **WI-796** (re-judge TC-055, routine after a
  landing that touches CMP-009).
- **Filed** the twenty-one successor rows **WI-797 to WI-817** in the graph's
  order (drafted by an Opus agent from the note, checked against the README table
  for needs, tier and review bar, and against the SR registry). WI-794 closed.
- **For the owner**: D-032 (a plan-dual kind keeps dual rounds two-family), D-035
  (family exclusions and the swap become ranked preferences), D-036 (literal
  family shares change adopters' equal-weight draws) in `docs/decisions/wi-788.toml`;
  D-006 and D-007 in `docs/decisions/coordinator-2026-10-04.toml`.
- **The Anthropic lineup** (owner, 2026-10-04): strong = Opus 5.5 at high
  (`ANTHROPIC-OPUS-STRONG`, whose env had drifted to `xhigh`), medium = Sonnet 5.5
  at medium (`ANTHROPIC-SONNET-MEDIUM`), quick = Sonnet 5.5 at low
  (`ANTHROPIC-SONNET-QUICK`, replacing the bare `sonnet` alias at high); the Opus
  medium row is catalog-only. `claude-sonnet-5-5` was probed live. `OPENAI-SOL`
  stays at medium in the router: the owner ran this session's hand reviews at high
  for depth.
- **Later in the session.** The owner signed SN-003, SN-008, SN-025 (exclusions
  restored) and SN-043 with SN-009 (act seq 31). The owner confirmed eleven
  high-risk decisions and directed WI-818: a decision is confirmed or overruled,
  never approved, and an overrule may amend the queued row the decision is
  scoped to. The `thebpandey/lanes` evaluation
  (`docs/plans/2026-10-04-lanes-evaluation.md`) was not adopted; two methods are
  filed deferred: WI-819 (declared file ownership) and WI-820 (provider trust
  and secrets). The owner ruled on WI-820: listing a route trusts it with standard
  repo content, stated plainly; secrets get structure plus detection for every
  route, plus an opt-in per-route `deny_reads`. The program runs by coordinator
  session. The next resume map is `docs/handoff-2026-10-04-wave13-coordinator.md`.
- **The full unfiltered suite** at `6613ddd0`: 5050 passed, 13 skipped, 0 failed, in
  595.7 s (detached worktree, fixed basetemp).
