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

`claude.settings.json` also carries a **`PreToolUse` subagent-spawn gate**
(`scripts/subagent_gate.py`) for unattended runs — deny-by-default fan-out with
the override held by the launcher, not the model (process-options.md
"Tier-conditional guardrails" neighbours it; policy in `docs/process.toml`
`[checks] subagent_gate`, shipped `"off"`, so it is a vacuous allow until you
opt in). It is **Claude-only**
here: Gemini's hook model differs and Codex has none, so the gemini config omits
it. Like every hook, it is *supervision, not security* — a model that can edit
files can remove it.

`claude.settings.json` also registers **the coordinator guard's hooks**
(`scripts/coordinator_guard.py hook`, on every event the guard reads). Two
things act through them: the context guard (`[coordinator]
context_guard_pct`, shipped `0`, off) and the blackout window (`[policies]
blackout`), inside which the guard denies a coordinator session's new
subagents and model-CLI launches and tells it to close down, whatever the
guard's dial says. dev-setup offers, with consent, to switch **only these**
on: they are merged into the machine-local `.claude/settings.local.json`
beside any hooks already there, each command bound to the absolute path of the
Python 3.11+ interpreter dev-setup resolved (so an older `python` first on
PATH cannot run them), and declining changes nothing. That file is this
machine's, so the scaffold's `.gitignore` keeps it out of git; the committed
`.claude/settings.json` is never written. The other entries stay inert until you
copy them yourself.
