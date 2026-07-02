# Optional per-agent hook configs

**These are convenience extras, not the source of truth.** Enforcement of the
process floor lives in the agent-neutral substrate — the git `pre-commit` hook
(`hooks/pre-commit`, enabled by `setup.sh`/`setup.ps1`) and CI (`ci/check.yml`).
Those run the same checks for every agent *and* for bare `git`, so the bar holds
no matter who (or what) commits.

Agent hook systems do **not** standardize: Claude Code uses
`.claude/settings.json` (~12 events), Gemini CLI uses `.gemini/settings.json`
(~10 events), and Codex has no hook system at all (it relies on policy + an OS
sandbox). That fragmentation is exactly why enforcement belongs in git + CI, not
in any one agent's config.

The files here let an agent give you *earlier* feedback (e.g. on the agent's
`Stop` event) by running the same stdlib process checks the git hook runs:

- `claude.settings.json` → copy/merge into the repo's `.claude/settings.json`.
- `gemini.settings.json` → copy/merge into the repo's `.gemini/settings.json`.

They are intentionally **never wired live** by `bootstrap.py`. When you scaffold
with `--agents claude|gemini|both`, the chosen agent's config is copied **inert**
as `.claude/settings.json.example` / `.gemini/settings.json.example` — so the
scaffold never silently installs a `Stop` hook that runs commands. Adopt one only
if you want the extra signal: rename the example to `settings.json` (merging into
any existing one), and **verify the schema against your agent's current version** —
these mirror the git hook for convenience; they don't replace it.
