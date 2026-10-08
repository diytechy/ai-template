+++
id = "WI-798"
title = "Account tables and per-account homes for every CLI route"
workstream = "process"
specref = "docs/plans/2026-10-04-wi788-design/README.md#s788-accounts"
sr_refs = ["SR-222"]
needs = ["WI-797", "WI-834"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Context

Filed by hand by the coordinator on 2026-10-04 from WI-788's approved design note
(OI-104, ruled 2026-10-04). This is S788-accounts (ch.2 §4, §9). Today IF-045 makes
a second account a second, duplicated route row, and a retained family's home
silently overrides a route's own `CLAUDE_CONFIG_DIR` or `CODEX_HOME`. The row adds
`[account.<ID>]` tables in `docs/agents.toml` (`cli`, `notes`, optional `env`), a
`ROUTE@ACCOUNT` qualifier in the enable list, and adapter home variables (IF-245:
claude `CLAUDE_CONFIG_DIR`, codex `CODEX_HOME`, opencode `XDG_DATA_HOME` and
`OPENCODE_CONFIG`, gemini `GEMINI_CLI_HOME`). Homes live in the user config
directory, outside every checkout (README Q-2); a person provisions credentials and
the kit never reads them. The per-family home retires (README change 3, OI-69 (e1);
change 21 retires "a second account is a second row"). Homes come first among code
rows because retained homes override route environments today (README order
notes, B12). D-029 holds a non-ambient claude account unverified until the
login-isolation check passes.

## Done-when

- Two accounts of one CLI run under two homes, and a route's env is never
  overridden by a family home; the per-family home is gone.
- Unqualified enable-list entries behave as today (the person's ambient login).
- Cooldowns key on `route@account`.
- The no-spend claude login-isolation check runs: two `CLAUDE_CONFIG_DIR` homes on
  Windows show two logins (ch.2 §5). Until it passes, a claude account other than
  the ambient login stays unverified (D-029).
- Each spine row the README matrix gives this row (LLR-266/267/268, TC-262..265,
  IF-045, IF-162, IF-245, shared with WI-815; a new LLR for accounts with a TC
  verifying each arm it states) is amended or added and passes adjudication of
  that row, on whichever adjudication path is the one path when this row lands. `docs/agents.toml`, `agents.template.toml` and
  `docs/agents-enabled` are amended to match.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`,
  plus a scaffold bootstrap and the claude login-isolation check.
- The per-family home's authentication moves to the account home and is not
  retired with it (WI-846, WI-834). This repo's dedicated Claude home becomes
  a declared account. A retained Claude launch under that account still reads
  the owner's long-lived token at launch through the environment variable
  OI-110 (b) declares: nothing about the path is tracked, and the token is
  never written to a log, prompt, record or commit. An unset variable, or a
  missing or unreadable token file, is still refused before launch, naming
  dev-setup, and an authentication failure still retires no session. The
  sign-in probe and dev-setup's check and `claude setup-token` offer report on
  that account's home. The adjudicator that ran signed in before this row runs
  signed in after it. WI-846's and WI-834's tests stay green, re-pointed at
  the account home rather than deleted, and the RESYNC entry states the
  migration.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit, migrating route config to
  account tables (risk 9: the RESYNC entry is the migration).
