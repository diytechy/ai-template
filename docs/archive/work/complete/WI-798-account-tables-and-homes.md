+++
id = "WI-798"
title = "Account tables and per-account homes for every CLI route"
workstream = "process"
specref = ""
sr_refs = ["SR-222"]
needs = ["WI-797", "WI-834", "WI-887"]
buildtier = "strong"
safety_class = "ordinary"
priority = 3
+++

## Deliverable

Closed at its landing on 2026-10-20, after its gate, in a headless leg:

- `docs/agents.toml` declares `[account.<ID>]` tables (`cli`, `notes`, an
  optional `env`, an optional `token_file_variable`, `verified`), and the
  enable list names a `ROUTE@ACCOUNT` entry. Malformed tables and qualifiers,
  an unreadable enable list, a route env declaring its CLI's home variable
  and a route or account declaring a competing credential source are named
  errors, never an ambient or unqualified fallback.
- Each account has its own home outside every checkout, under the user
  configuration directory; the per-family home is gone. A qualified launch
  withholds every ambient source its CLI ranks above the account's own home
  or token, and a qualified OpenCode launch composes from a declared base of
  platform variables plus the kit-owned names it inherits, never the ambient
  environment. An unqualified entry keeps today's environment.
- The enable-list entry is the identity selection, preference, cooldowns,
  planners and retained records carry; a record lacking or naming another
  account re-mints once. A route's CLI is read through the launcher's one
  template parse.
- This repository's adjudicator runs on the declared token account
  ADJUDICATOR through the qualified entry `ANTHROPIC-OPUS-STRONG@ADJUDICATOR`,
  for its sittings and its act turns alike; the sign-in probe and dev-setup
  report the account, and an unverified non-ambient Claude login is printed,
  not refused. The two-login half of the isolation check is WI-908's (OI-114).
- The spine: LLR-336 and TC-361..366 approved; LLR-044, LLR-072, LLR-266..268,
  LLR-270, LLR-305, LLR-306, LLR-321, TC-267, TC-321, TC-323, TC-324, TC-330
  and TC-344 re-attested (verdict 017). The RESYNC entry states the migration.
  Lane log: `docs/log.d/WI-798-account-tables-and-homes.md`.

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

## Deliverables and landing order

Written before the claim, answering the scope critique's S1 (coordinator
2026-10-11 D-008, for the owner to confirm or overrule). "Homes come first
among code rows" in the Context orders WI-798 against the other S788 rows; this
section orders the work inside it.

**The units that could land on their own.**

- **(b) The entry identity.** The selected enable-list entry, not the bare
  route id, becomes the identity that resolution, selection, preference and
  cooldowns carry (`agent_route`'s resolve and select functions, `available`
  and `cool`, `agent_loop`'s cooldown state, `plan_runner`'s dual-plan and
  planner-fallback pools, `coordinator_adjudicate.resolve_route`). Every
  existing entry is unqualified, so this changes no behaviour.
- **(a) Accounts and homes.** `[account.<ID>]` tables, the `ROUTE@ACCOUNT`
  qualifier, the adapter home variables (IF-245), one launch-environment rule
  for every launch site, the per-family home's retirement, and `account` in the
  retained record's identity.
- **(c) The adjudicator's authentication.** The OI-110 (b) token locator moves
  from the ANTHROPIC family to one declared account; this repo's adjudicator
  runs on that account through a qualified entry; the sign-in probe,
  dev-setup's check and its `claude setup-token` offer report on that account.

**Order and decision.** One row, two commits: (b) first, as a structural
commit (PROCESS.md §3, "A structural move is its own commit"); then (a) and
(c) together in one behaviour commit with their spine rows, template, fixtures
and RESYNC entry. (c) cannot land after (a): the token is keyed by family today
(`session_service.TOKEN_VARIABLES`), so once the family home retires either
every Claude account authenticates as the token's account, or the adjudicator
loses its token unless its entry moves to the declared account in the same
commit. (c) cannot land first, because a declared account needs (a)'s tables.
(b) could land alone but delivers nothing until (a), so it rides as the first
commit rather than paying a lane of its own. The lane lands as one squash, so
(a) and (c) reach trunk together by construction.

**Split out:** only the live two-login half of the Claude login-isolation
check, which needs the owner (`## Owner-dependent completion`). Its row and open
item are filed on trunk before this row's claim (scope rubric B2).

## Trust

Written before the claim, answering the scope critique's S2 (coordinator
2026-10-11 D-009 to D-013, for the owner to confirm or overrule). The registry
and the enable list choose the credential and home a launch runs under, and an
account's home or token authenticates an adjudicator that takes acts, so each
carrier, its producer, every consumer by path and a ruling per consumer are
stated here, under `project-trajectory/PROCESS.md` §3, "When a guard is owed".

**The carriers.**

1. **Account tables** in `docs/agents.toml`: `cli`, `notes`, an optional `env`
   (composed after the route's env; see the one environment rule below),
   an optional `token_file_variable` naming the environment variable that
   locates the account's token file (never a path, OI-110 (b)), and
   `verified = "<date> <cli version>"`, empty by default (D-011).
2. **`ROUTE@ACCOUNT` lines** in `docs/agents-enabled`, the consent surface
   (IF-162).
3. **The account home**, `<user config dir>/project-trajectory/accounts/<ID>/`
   (`%APPDATA%` on Windows; `$XDG_CONFIG_HOME`, else `~/.config`, on POSIX). The
   provider-owned authentication state inside it is never opened by the kit.
   The one provider-written file the kit reads there is a Codex session
   rollout (`sessions/**/rollout-*-<thread id>.jsonl`), for telemetry only.
4. **The token locator variable** a `token_file_variable` names
   (`AGENT_CLAUDE_TOKEN_FILE` for this repo), and the file it names.
5. **The login-isolation evidence:** the account's `verified` cell, citing the
   log fragment of the check that set it.
6. **Retained-session records** under `out/adjudicator/`, keyed by family,
   route and scope; this row adds `account` to their identity (IF-247).
7. **Cooldowns:** an in-process map in `agent_loop`'s loop state, keyed by
   entry. Not on disk, so it crosses no trust boundary and owes no guard. Two
   declared accounts that are one provider account cool independently, a known
   limit this row does not detect.

**Producers, write routes and failed writes.**

- **Carriers 1 and 2:** a person or the coordinator edits them and they land
  through a reviewed lane; bootstrap copies `agents.template.toml` to
  `docs/agents.toml` (`bootstrap.py`, `kitlib/bootstrap_manifest.py`), the
  template shipping one commented account example and no qualified entry; the
  RESYNC migration is a hand edit. An interrupted edit or merge leaves a file
  that does not parse or a table missing a key; a failed or interrupted
  bootstrap copy (`bootstrap.py`, `_write_scaffold_file`) exits non-zero and
  can leave the file absent, empty, truncated or as the template's bytes. The
  readers treat every such result by the rules below, whatever produced it: a
  file that does not parse is a registry error (with routing on, preflight
  fails, as today); a parseable but incomplete file reads table by table, a
  table missing a key being a registry error naming it and an account table
  that is absent leaving its account undeclared, so a qualifier naming it is
  an enable-list error; an empty `docs/agents.toml` declares no rows and no
  accounts.
- **Carrier 3:** the person provisions it (for example
  `CODEX_HOME=<home> codex login`) and the provider CLI writes it. The kit
  creates only a token account's home, empty, because it holds no credential;
  it never creates a login account's home and never moves, copies, reads or
  deletes any home (D-013). An aborted or timed-out login leaves no
  authentication file, or a partial or expired one; the status command then
  answers "not logged in" (the CLI's structured error) or something
  undocumented; an unwritable home fails the CLI at launch. The Codex CLI
  writes its rollouts as it runs: a killed or interrupted run leaves a
  rollout whose last line is truncated, or none.
- **Carrier 4:** the owner writes it: `claude setup-token` prints the token,
  the owner keeps it in a file outside every checkout and sets the variable as
  dev-setup says. The kit writes neither. Failed writes: the variable unset, or
  not visible to an already-running process; the file missing, unreadable or
  empty; the token truncated, carrying stray text, revoked or expired, which the
  first launch reveals as the CLI's authentication failure.
- **Carrier 5:** only the owner-held isolation-check row writes it, in its own
  reviewed commit after the owner's two-login check. A check not run or failed
  leaves the cell empty; a failure is recorded in that row's log fragment and
  its open item. The lane's unattended empty-home half is lane-log evidence only
  and never sets the cell.
- **Carrier 6:** `session_keep` writes whole records under `store_lock`,
  through a temporary file and a replace, with lockless markers (WI-858).
  Failed writes (`StoreBusy`, a leftover temporary file, a failed replace that
  leaves the prior record) are unchanged here (LLR-270).

**What the authority binds to.** A call's authority is the selected entry,
resolved once per call into: the route row (CLI, template, model, declared
env); the account and its declared env (no account means the person's ambient
login); the effective home,
derived from the account id and the user config directory alone (no home for
an ambient entry); the authentication source (the account's token locator if
it declares one, else the login in its own home); and, for a retained call, the
record whose identity (family, route, account, scope) equals the call's. No
consumer re-derives any of these from the family, the bare route id or the
ambient environment. An account's readiness is read only from its own source,
its token file or its status command run under its own home; a sign-in anywhere
else (the ambient login, another account's home, the retired family home) never
establishes it. A token-authenticated account is outside the isolation
question, because its token outranks any login (the precedence at
`session_service.COMPETING_CREDENTIALS`). A login-authenticated Claude account
other than the ambient login with an empty `verified` is unverified (D-029):
preflight and the sign-in probe print it as unverified, as the design prints
every untested route (chapter 2, "Untested is visible"); it is not refused.

**Absent, unreadable, failed and malformed inputs.** No case falls back to the
ambient login, the unqualified entry, the retired family home, a
checkout-local path or another account.

- **Absent:** an absent `docs/agents.toml` keeps today's rule (no rows; with
  `agents-enabled` present, preflight pages); an absent `docs/agents-enabled`
  keeps routing off (IF-162); an absent token-account home is created; an
  absent login-account home reads `missing` and is refused before launch,
  naming the provisioning command.
- **Unreadable:** an `agents-enabled` that exists but cannot be read is an
  error, never read as absent (D-012; today it reads as routing off, which
  would drop a consented run onto the single-model path); an unresolvable user
  config directory refuses every qualified launch.
- **Malformed:** an account table missing `cli`, with a `cli` outside IF-245's
  table, an unknown key, an id outside the id grammar, an `env` declaring its
  own CLI's home variable, a `token_file_variable` another account also names,
  or a malformed `verified` is a registry error naming the table, and the table
  is dropped; a qualifier with an empty side, more than one `@`, an undeclared
  account, or an account whose `cli` differs from the route's CLI is an
  enable-list error naming the line, never stripped to the unqualified entry; a
  qualified entry whose route `env` declares its CLI's home variable, or whose
  route `env` and account `env` declare the same key, is refused, so neither
  side silently wins (D-012).
- **Failed:** token problems refuse before launch, naming the variable and
  dev-setup but never the path or the value (today's wording, now per
  account); a status command that fails, times out or answers outside its
  documented pairs reads `unknown`, and `unknown` never reads as ready; an
  authentication failure at launch is a failed call that retires no session and
  cools only its own `route@account`.

**Consumers and rulings** (found by the census greps recorded with D-009).

- **The loader**, `project-trajectory/scripts/agent_route.py`
  (`load_registry`, `load_enabled_entries`, `load_enabled`, `load_tag_rank`,
  `resolve_enabled`, `available`, `cool`, `pool_context`,
  `winstay_preferred_ids`, the planner pair and fallback): the one parse of
  tables and qualifiers, with every rule above. No other module parses either.
- **The loop launcher**, `project-trajectory/scripts/agent_loop.py`
  (preflight, routing status, worker launch env, `probe_route`, cooldown
  state): under managed routing every registry or enable-list error above fails
  preflight, as registry and enable errors do today; preflight prints each
  enabled unverified account; launches take the one environment rule; cooldowns
  key on the entry.
- **The dual-plan launcher**, `project-trajectory/scripts/plan_runner.py`
  (`_dp_routes`, the planner fallback): registry errors page as today, never
  moving to the ambient template; the fallback carries the entry and refuses on
  resolution errors, where today it discards them.
- **The adjudicator's launcher and sign-in reporter**,
  `project-trajectory/scripts/coordinator_adjudicate.py` (`resolve_route`,
  `DEFAULT_ROUTE`, `signin`): the adjudicator resolves its qualified entry; an
  entry not on the list, an undeclared account, or a registry error on its row
  or account refuses before launch (today those errors are discarded);
  `signin --retained` reports the adjudicator entry's account.
- **dev-setup's sign-in check and setup offer**, `scripts/dev-setup.ps1`,
  `scripts/dev-setup.sh`, `project-trajectory/scripts/dev-setup.template.ps1`,
  `project-trajectory/scripts/dev-setup.template.sh`: they parse the account
  line, changed in the same commit as `signin`; an absent or unparseable line
  reads `unknown`, as today; the `claude setup-token` offer appears only for a
  token account reading `missing`; for a login account dev-setup names the
  provisioning command and runs nothing. Nothing signs in automatically.
- **Retained and unretained launch, token and probe**,
  `project-trajectory/scripts/session_service.py` (`prepare_launch`,
  `launch_credential`, `_read_token`, `refuse_competing`, `require_signin`,
  `signin_status`, `route_env`, `keep_warmer` and `KeepWarmer`): one
  environment rule, composed once per call: the ambient environment, then the
  route's declared env, then the account's declared env, then the account's
  home variables. A key that both the route's env and the account's env
  declare is refused before launch, naming both, so neither silently
  overrides the other. That one composed environment is the one every
  consumer of the call uses: the launch, the version and sign-in probes, and
  a keep-warm ping. The token is read only for an account
  that declares a locator, and the competing-credential refusal applies to that
  account; an ambient entry has no kit-held home and no sign-in gate; keep-warm
  pings only records whose entry is still enabled and whose account resolves.
- **The home and record store**, `project-trajectory/scripts/session_keep.py`
  (`HOME_VARIABLES`, `dedicated_home`, `dedicated_home_env`, `store_dir`,
  `store_load`, `_record_path`, `store_save`, lease preparation): homes are
  keyed by account under the user config directory; a record whose `account`
  differs from the call's, or that lacks `account` (every record written before
  this row), reads as not its own, and the next launch mints, once, as the
  RESYNC entry states. Write and lock rules are unchanged.
- **The Codex rollout reader**, `project-trajectory/scripts/session_adapters.py`
  (`_codex_home`, `_codex_rollout`, the codex adapter's `context` and
  `compaction`): telemetry only, never deciding a hold, an act or a gate. It
  reads exactly the call's thread id's newest rollout under the composed
  environment's `CODEX_HOME` (the account home for a qualified entry, codex's
  own default for an ambient one), so one account's rollouts are never read
  for another's thread. An absent home, rollout or thread id, or an
  unreadable file, leaves occupancy blank and records no compaction
  observation; a malformed or truncated line is skipped. These rules are
  today's and stay unchanged; the row changes only the home it receives.
- **Readers left unchanged:** `project-trajectory/scripts/coordinator_guard.py`
  (command templates only; an account carries none);
  `project-trajectory/scripts/dispatch.py` (the enable list's presence only; an
  unreadable file still raises and launches nothing); the launcher slots in
  `agent-resume.template.sh` and `.cmd` (`AGENT_PREFER_MAP`: a preference names
  an entry exactly, and an unknown one keeps today's fall-through, because it is
  a preference, not consent).
- **Producers:** `project-trajectory/scripts/bootstrap.py` and
  `project-trajectory/scripts/kitlib/bootstrap_manifest.py`, under the template
  rule above.
- **Wording only, no ruling owed:** `score_reviews.py`, `agent_policy.py`,
  `agent_brief.py` and `trace_text.py` under `project-trajectory/scripts/`,
  `docs/interface-reference.md`, `project-trajectory/PROCESS_OPTIONS.md`,
  `project-trajectory/GLOSSARY.md`, `project-trajectory/RESYNC_PACK.md`, and
  both copies of the coordinator-cycle `references/recipes.md`.
- **Outside the kit:** the provider CLIs (`claude`, `codex`, `opencode`,
  `gemini`) consume their home variables and their own authentication state,
  which the kit never opens.

## Owner-dependent completion

Written before the claim, answering the scope critique's proposed B3
(coordinator 2026-10-11 D-014, for the owner to confirm or overrule).

**The lane builds and checks unattended:** the schema and the qualifier; the
homes and the one environment rule, shown with fixture CLIs that report their
environment for each IF-245 adapter (two accounts of one CLI get two homes);
the entry-keyed cooldowns; the record identity and its one re-mint; the
sign-in probe and dev-setup readings, from fixtures; a scaffold bootstrap;
WI-834's and WI-846's tests, re-pointed; the no-spend empty-home half of the
Claude isolation check (a fresh, empty account home reads not logged in to
Claude's status command while the ambient login reads logged in, recorded in
the lane log); and the adjudicator continuing to authenticate: the token and
its variable are already provisioned on this box, so the lane's own in-lane
sitting launching on the declared account, with `signin --retained` reading
signed-in, is the evidence.

**What needs the owner:** provisioning a second Claude login under a second
account home on Windows, and running the two-login half (two homes show two
different logins, and signing in under one leaves the other and the ambient
login unchanged).

**A missing isolation result does not hold this row.** WI-798 lands with every
login-authenticated non-ambient Claude account unverified and printed as such
(D-029). The live check is WI-908, filed on trunk before this row's claim, held
by the pending open item OI-114.

## Done-when

- Two accounts of one CLI compose two launch environments with two homes,
  shown by fixture CLIs for each IF-245 adapter. A route's declared env is
  never overridden, and a qualified entry whose route env declares its CLI's
  home variable is refused. The per-family home is gone.
- Unqualified entries run as unretained launches do today: the person's
  ambient login and the route's own env, with no kit-held home. A retained
  launch on one no longer moves to a family home.
- Cooldowns key on the selected entry (`route@account`; an unqualified entry
  is its own key), landed first as a behaviour-preserving commit.
- A login-authenticated claude account other than the ambient login carries
  an empty `verified` cell and is printed as unverified at preflight and by
  the sign-in probe (D-029). The lane records the no-spend empty-home half of
  the isolation check; the two-login half (ch.2 §5) is WI-908's, held by
  OI-114. A token-authenticated account is outside the isolation question.
- Each spine row the README matrix gives this row (LLR-266/267/268, TC-262..265,
  IF-045, IF-162, IF-245, shared with WI-815; LLR-270, LLR-305 and IF-247, the
  family home, family-keyed token and record identity this row makes untrue; a new LLR for accounts with a TC
  verifying each arm it states) is amended or added and passes adjudication of
  that row, on whichever adjudication path is the one path when this row lands. `docs/agents.toml`, `agents.template.toml` and
  `docs/agents-enabled` are amended to match.
- The row's test bar: its affected modules' tests plus the smoke tier at `-n 2`,
  plus a scaffold bootstrap and the empty-home half of the claude
  login-isolation check; the two-login half is WI-908's.
- The per-family home's authentication moves to the account home and is not
  retired with it (WI-846, WI-834). This repo's adjudicator runs on a
  declared token account (its table names the OI-110 (b) variable) through a
  qualified entry, and the token binds to that account only; the retired
  home's directory is left in place and never read, moved or deleted by the
  kit, and the retained record re-mints once. A retained Claude launch under that account still reads
  the owner's long-lived token at launch through the environment variable
  OI-110 (b) declares: nothing about the path is tracked, and the token is
  never written to a log, prompt, record or commit. An unset variable, or a
  missing or unreadable token file, is still refused before launch, naming
  dev-setup, and an authentication failure still retires no session. The
  sign-in probe and dev-setup's check and offer report on that account (its
  token file, or its own home for a login account), shown by the lane's
  in-lane sitting launching on the declared account and `signin --retained`
  reading signed-in. The adjudicator that ran signed in before this row runs
  signed in after it. WI-846's and WI-834's tests stay green, re-pointed at
  the account home rather than deleted, and the RESYNC entry states the
  migration.
- Each ruling in `## Trust` holds, with a test for each consumer's absent,
  unreadable and malformed arms.
- Review bar: A (one cross-family REVIEW-A).
- RESYNC_PACK: an entry anchored at a trunk commit, migrating route config to
  account tables (risk 9: the RESYNC entry is the migration).
