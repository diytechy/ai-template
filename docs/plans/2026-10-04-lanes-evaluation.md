# Evaluation: `thebpandey/lanes` (2026-10-04)

The owner asked whether [thebpandey/lanes](https://github.com/thebpandey/lanes)
could be adopted, in whole or in part, instead of WI-788's own lane-lifecycle
design. The coordinator read the whole repository at `0f82a46` (v0.2.0, released
2026-10-02, 14 commits, MIT): a Claude Code / Codex orchestration skill of about
350 lines of bash. An orchestrator writes a brief per task and a git worktree;
workers build there (cheap tasks go to DeepSeek or GLM through Claude Code pointed
at their Anthropic-compatible APIs); an independent reviewer writes a `review.md`
verdict bound to the exact head commit; `lane/integrate.sh` is the only merge path
and merges `--no-ff` in the main checkout after a CLEAN verdict for that revision.

## Verdict: not adopted

- **Platform and language.** Bash on Linux/macOS (`sha256sum`, `/proc`, systemd).
  The kit's scripts are stdlib Python on Windows and POSIX.
- **A second lane system.** `integrate.py`, the dispatcher and the lane state
  already cover its core; running both is the dual path the owner has ruled out.
- **Not WI-788's problem.** WI-788's weight is acts inside the lane, adjudication
  with a final pass, one id allocator, trunk exclusion for concurrent writers and
  recovery; `lanes` has none of these, and its `--no-ff` merge contradicts the
  owner's squash ruling (OI-103 Q4).
- **Immature.** Two days old.

Already in the kit: a verdict bound to one revision (the `Review-Verdict` trailer
pins the tree; the merge refuses a stale APPROVE), the orchestrator never
reviewing, model identity from usage data rather than self-report, tier
escalation, and a secret scan before push (`check_privacy`).

## Taken, deferred: declared file ownership per lane

`lanes` has each brief name the paths it may change (`owned.txt`).
`lane/scope-check.sh` then fails a lane with any changed path outside them, or with
uncommitted work, at review and again at merge. The kit has no such check. It
would catch scope creep mechanically and make parallel lanes safer (SN-027), since
overlapping ownership is visible before dispatch. Filed as WI-819, deferred by the
owner ("Please add #1 but in deferred").

## Taken, deferred: route listing and the repository content

`lanes`' `model-relay` refuses to run a third-party model in the main checkout or
in a worktree holding `.env`-style files. The owner rejected the premise of a trust
tier: "if a model should not be trusted it should not be in agents.toml". Trust is
therefore binary, by inclusion. What remains open is narrower: whether listing a
route records that its provider's terms are acceptable for the repository's content
(free tiers can retain or train on input), and whether secret-bearing files in a
worktree need a guard for every launch, whatever the provider. Filed as WI-820,
deferred by the owner ("Add 3 as WI but also deferred").

## Not taken

- **Skipping review for prose-only changes.** In this repository the prose is the
  spine, so a "prose-only" exemption would waive review exactly where it matters
  most. The kit's existing no-bar path (`integrate.py`, WI-388) skips only the
  product test bar, and only for a lane whose delta no test can judge (the work
  folder, registries, logs, reviews, decisions). Review and adjudication still
  run. That path, extended by change class, is the candidate for README A4's
  landing-cost iteration point; nothing from `lanes` is needed for it.
- **Cheap workers through Claude Code.** `bin/claude-via` runs the `claude` CLI
  with `ANTHROPIC_BASE_URL` and `ANTHROPIC_AUTH_TOKEN` pointed at a provider's
  Anthropic-compatible API (DeepSeek, or GLM through OpenRouter). In the kit that
  is an ordinary route row (`cmd_template` plus `env`, family = the trainer, e.g.
  DEEPSEEK, not ANTHROPIC), selected by tier and by README A1's per-kind table. No
  new mechanism is needed; adding such a row is the owner's choice.
- **Per-brief token caps with stop-and-rebrief.** Lower value beside the usage
  ledger (WI-800); not taken.
