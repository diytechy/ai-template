#!/usr/bin/env python3
"""Model routing for the unattended coordinator — the enable-list + availability
selector and the fixed escalation policy (process-options.md "Unattended
operation" -> the routing/escalation subsection). Stdlib only, Python 3.11+.

This is the declared, legible half of heterogeneous implementer/reviewer
scheduling. It is **config, not a catalog**, and its registry is the
**pair-row model** ("pairs now, factor later"): identity vs access, one row
per (model x route) pair.

  - `docs/agents.toml` is the model REGISTRY (`.csv` until a repo runs
    `migrate_carrier.py`; either carrier resolves). Columns:
    `Id,Family,Model,Version,Tier,CmdTemplate,Env,Notes`.
      * IDENTITY = `Family` (who trained it — the heterogeneity + scorer
        corroboration key), `Model` (the provider's line identity, INCLUDING
        `-pro`/`-flash`-style tokens), `Version` (the *comparable* token only:
        a dotted numeric like `4.8`, a date stamp, or a maturity tag — moving
        vendor aliases never live here).
      * ACCESS = `CmdTemplate` (`{model}`/`{prompt}` slots) + `Env`
        (`KEY=value;KEY2=value2`, merged over the inherited environment at
        launch; **empty Env = the ambient environment = today's behavior**).
      * `Tier in {strong,medium,quick}` (legacy `weak` reads as `quick` —
        never-breaking). **One row = one (model x route) pair** —
        the table itself IS the allow matrix (no `Serves` patterns). A router
        service is a *second pair row* (distinct id, same Family, its own Env).
      * ACCOUNTS (WI-798) are `[account.<ID>]` tables beside the rows: `cli`
        (one of IF-245's), `notes`, an optional `env` (composed after the
        route's), an optional `token_file_variable` (the variable naming the
        account's long-lived token file, never a path) and `verified`. A
        second account is an account table and a qualified enable-list entry
        (`ROUTE@ACCOUNT`), never a duplicated row; each entry cools on its own.
    The id is a join key, **never parsed** — the columns are the machine truth;
    the id charset is uppercase + digits + hyphen + dot so dated snapshots and
    `-PREVIEW` tags are valid. `Provider` is retired: a legacy registry with a
    `Provider` column and no `Family` reads Provider as Family (never-breaking).
    No vendored catalog: richer data lives in the maintained community
    registries (models.dev `api.json`; LiteLLM's model-prices JSON) — a
    documented pointer, not a copy.
  - `docs/agents-enabled` is the ENABLE-LIST — the ids (or version-less tokens),
    each optionally qualified `@ACCOUNT`, this repo may use, in **preference
    order**, one per line (`#` comments allowed); an unqualified entry runs
    under the person's ambient login. It is the consent surface: routing selects only from this pool,
    and its **presence** is what turns on managed routing at all. Absent
    enable-list -> the loop keeps today's single `AGENT_CMD`/`AGENT_MODEL`
    behavior, so a fresh scaffold pays nothing (no silent model swap: consent =
    the enabled set + these declared rules). A token that exactly matches a row
    Id resolves to it; otherwise it resolves over rows whose normalized
    `Family`-`Model` matches (intra-line only — the `-PRO` correction), newest
    version winning (see `resolve_token`).

The recorded revisit trigger (the "factor later" half): once one route's
command/env text repeats across enough pair rows that editing it is
error-prone, factor the route definitions into a named-preset file the pair
rows reference — the rows stay the explicit allow matrix, only the text gets
deduplicated.

Selection composes the phase's tier with the heterogeneity rules: reviewers
prefer two families, at least one differing from the implementer's — *preferred
not required* (degraded availability is legal: one responding family reviews
with two independent same-family sessions; fresh context is the invariant).
A model whose session fails to start or stalls goes on **cooldown** (its limit
is probably exhausted) and is retried later; when no enabled model of the
preferred tier is available, selection walks the **next tier up — never a
weaker one**.

The escalation policy is **fixed and declared, not a learned router**
(per-project sample sizes are far too small for a bandit): win-stay/lose-shift
with a margin, an implementer-family swap after consecutive failed review
gates, a tier rise only after the swap also fails, and paging the human on the
shared-failure regime, contradictory verdicts, or any tripwire. The constants
ship as legible per-repo-overridable defaults (calibration values, not spine
facts); the scoreboard (`score_reviews.py`) stays **advisory** — the declared
policy picks, nothing auto-optimizes.

Contracts: IF-044 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-044: model routing as a PURE selection library the coordinator calls.
    `load_registry` reads the declared pair-row model registry and
    `load_enabled` / `load_enabled_entries` the enable-list (one that exists
    but cannot be read raises `EnabledUnreadable`); `resolve_enabled` turns
    those tokens into enabled entries (`ROUTE` or `ROUTE@ACCOUNT`), and
    `entry_route` / `account_of` name the row and the account an entry
    selects; `parse_env` turns a row's `Env` cell into the environment a
    launch merges over its own; `select` returns the chosen entry TOGETHER
    WITH ITS REASON as data;
    `escalate` and `failure_action` return the declared next move; `cool` and
    `available` carry the cooldown. Nothing here launches a session, writes a
    file or touches git — the coordinator owns every launch, which is what
    makes each choice auditable and testable without a model. An ABSENT
    enable-list is the off switch: managed routing does not engage and the
    caller keeps its single declared agent command, so a fresh scaffold can
    never suffer a silent model swap.
"""

import argparse
import csv
import io
import os
import re
import sys
import tomllib
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# The ONE comment-skipping CSV reader (WI-533): a registry CSV may open with a
# `#` declaration header, and a raw `csv.reader` here would read that header's
# first line as the column row — the header check below would then page over a
# missing `CmdTemplate` the registry actually declares.
from kitlib import spine as _spine

# Sibling: the registry CARRIER (repo-lock D-6 — the vocabulary gets ONE home
# and the readers import it; a re-sync copies this file with its declared
# siblings, ADOPTING.md §6). The model registry joined that carrier in the
# batch-2 sweep (repo-lock §8.1), so `agents.toml` is the destination name and
# `agents.csv` still resolves for a repo that has not migrated.
# `agent_session` is the launcher's template reader, whose parse `route_runner`
# shares; it imports the standard library only.
try:
    import agent_session
    import session_adapters
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import agent_session
    import session_adapters
    import spine_carrier

# Tier strength, ascending. Selection never picks a WEAKER tier than requested
# (a hard rule: cheap-is-not-free, so an unavailable tier escalates UP).
TIER_ORDER = ("quick", "medium", "strong")


def normalize_tier(tier):
    """Lowercase + the legacy alias: `weak` — the pre-rename bottom tier — reads
    as `quick` (owner rename 2026-07-12), so an existing registry or tier-map
    value stays valid (the Provider->Family never-breaking precedent)."""
    t = (tier or "").strip().lower()
    return "quick" if t == "weak" else t


# Registry id charset: uppercase + digits + hyphen + dot, starting alphanumeric.
# Deliberately permissive on internal structure — the id is a join key, never
# parsed for its Family/Model/Version (those are their own columns), and model
# names carry hyphens and dotted/dated version tags.
ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9.\-]*$")

REGISTRY_FIELDS = (
    "Id",
    "Family",
    "Model",
    "Version",
    "Tier",
    "CmdTemplate",
    "Env",
    "Notes",
)

# The maturity vocabulary + its DEFAULT rank (higher = preferred): GA/untagged
# beats preview beats beta beats exp (a fixed set with a per-registry override —
# a `# tag-rank: ga>preview>beta>exp` comment line in agents.toml, or the
# AGENT_TAG_RANK env knob; see load_tag_rank). `preview`/`exp` rows are SKIPPED
# in version-less resolution unless explicitly named or the only candidate.
DEFAULT_TAG_RANK = {"ga": 3, "preview": 2, "beta": 1, "exp": 0}
_SKIP_MATURITY = frozenset(("preview", "exp"))
_MATURITY_TOKENS = ("preview", "beta", "exp", "ga")

# Escalation calibration — legible per-repo-overridable defaults, NOT spine
# facts. Override per repo through the environment (the coordinator passes its
# own os.environ); a bad value falls back to the default rather than crashing a
# walk-away run.
DEFAULT_CONSTANTS = {
    # win-stay/lose-shift: swap the primary feedback source only on >= this.
    # Substance scores are means of [0,1] components, so a round's margin is
    # bounded by 1.0 — the old integer default of 2 was unreachable and made
    # the whole win-stay half arithmetic fiction (repo-review 2026-07-21 M-34).
    "margin": 0.15,
    "swap_after": 2,  # consecutive failed review gates before the implementer family swaps
    "page_top_tier_fails": 2,  # top-tier failed gates before paging the human (shared-failure regime)
}
_CONST_ENV = {
    "margin": "AGENT_ROUTE_MARGIN",
    "swap_after": "AGENT_ROUTE_SWAP_AFTER",
    "page_top_tier_fails": "AGENT_ROUTE_PAGE_TOP_TIER_FAILS",
}

# Per-phase draw-weight grammar (WI-236): an agents-enabled id may carry optional
# `<PHASE>=<int>` annotations after whitespace. These are the phases a weight may
# name; `REVIEW` is the umbrella that expands to both reviewer legs. A weight of 0
# means "fallback-only" (never drawn for the phase unless it is the sole legal
# candidate); a negative or non-integer weight is a malformed line (preflight
# fails). Unannotated ids weigh 1 everywhere, so an unannotated file selects
# byte-identically to before (uniform weight == today's line-order tie-break).
# SN-026: `ADJUDICATE` joins the vocabulary. An adjudication row is
# not a build — it judges a CLAIM another session made (a lane's partial close,
# an amendment's meaning-vs-clarity, a red TC under a closed row) — so it is a
# job type in exactly the sense the phase weights exist to express, and routing
# it as an ordinary BUILD drew from the implementer pool at the implementer
# tier. Cross-family preference is ON for it, for the reviewers' reason: a judge
# that shares the family of the party it is judging corroborates rather than
# checks.
WEIGHT_PHASES = ("BUILD", "REVIEW", "CRITIQUE", "DESIGN-CHECK", "ADJUDICATE")
_WEIGHT_PHASE_ALIAS = {"REVIEW": ("REVIEW-A", "REVIEW-B")}
# A weight is an unsigned ASCII decimal integer — no sign prefix, no whitespace
# (`+3`/`-1`/` 3` all fail). Python ints are unbounded, so a very large weight is
# accepted and simply concentrates the draw (a near-pin; documented).
_WEIGHT_INT_RE = re.compile(r"[0-9]+\Z")


class Model:
    """One registry row = one (model x route) pair. The id is opaque (a join
    key); Family/Model/Version (identity) + Tier + CmdTemplate/Env (access) are
    the machine truth. `family` is the heterogeneity/corroboration key (a legacy
    `Provider` column is read into it)."""

    __slots__ = (
        "id",
        "family",
        "model",
        "version",
        "tier",
        "cmd_template",
        "env",
        "notes",
    )

    def __init__(
        self, id, family, model, version, tier, cmd_template, env="", notes=""
    ):
        self.id = id
        self.family = family
        self.model = model
        self.version = version
        self.tier = tier
        self.cmd_template = cmd_template
        self.env = env
        self.notes = notes


class Registry(dict):
    """The loaded registry: `{route id: Model}`, and its declared `accounts`
    (`{account id: Account}`), read in the same one parse (WI-798). A plain
    dict reads as a registry that declares no account.

    Implements: SR-222, LLR-336
    """

    def __init__(self, rows=(), accounts=None):
        super().__init__(rows)
        self.accounts = dict(accounts or {})


class Account:
    """One `[account.<ID>]` table (WI-798): the CLI it signs into, its notes,
    its own declared environment (an Env cell, composed after the route's),
    the environment VARIABLE naming its long-lived token file when it
    authenticates with one ("" for a login account; OI-110 (b): never a path),
    and its login-isolation reading `verified` ("<date> <cli version>", empty
    until the check passes). Its home is derived from the id alone.

    Implements: SR-222, LLR-336
    """

    __slots__ = ("id", "cli", "notes", "env", "token_file_variable", "verified")

    def __init__(self, id, cli, notes="", env="", token_file_variable="", verified=""):
        self.id = id
        self.cli = cli
        self.notes = notes
        self.env = env
        self.token_file_variable = token_file_variable
        self.verified = verified

    @property
    def unverified(self):
        """Whether this is a login-authenticated Claude account whose
        login-isolation check has not passed (an empty `verified`): it is
        printed as unverified, never refused (D-011). A token account is
        outside the question, its token outranking any login.

        Implements: SR-222, LLR-336
        """
        return (
            self.cli == "claude" and not self.token_file_variable and not self.verified
        )


ACCOUNT_KEYS = ("cli", "notes", "env", "token_file_variable", "verified")
# An environment variable name, as a token locator must be one.
_VARIABLE_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*\Z")
# `verified`: empty, or the date the check passed and the CLI version it ran.
_VERIFIED_RE = re.compile(r"\d{4}-\d{2}-\d{2} \S+\Z")
# An account id names its home directory, so it is portable: no dot (Windows
# strips a trailing one and reads `NAME.EXT` as the device NAME) and not a
# Windows device name. Upper-case only, so two ids never fold to one name.
ACCOUNT_ID_RE = re.compile(r"[A-Z0-9][A-Z0-9-]*\Z")
_WINDOWS_DEVICES = re.compile(r"(CON|PRN|AUX|NUL|COM[0-9]|LPT[0-9])\Z")


# Windows resolves environment variable names case-insensitively, POSIX does
# not (`env_name_key`, the one rule every comparison of names uses, here and
# in a launch environment).
# Implements: SR-222, LLR-336
_CASE_INSENSITIVE = os.name == "nt"


def env_name_key(name):
    """An environment variable name as the platform resolves it
    (`_CASE_INSENSITIVE`): Windows folds case, POSIX does not; the rule every
    name comparison of the registry and of a launch environment uses.

    Implements: SR-222, LLR-336
    """
    return name.upper() if _CASE_INSENSITIVE else name


def route_runner(template, model):
    """The runner a command template launches: its first token by the
    launcher's own parse (`agent_session.split_cmd`, the shell-string or
    JSON-array form) after the argv substitution (`agent_session.substitute`),
    or "" when the template is empty or that parse refuses it. The one reading
    of a template's runner: the launch resolves what it returns, and the CLI
    a route launches is read from it.

    Implements: SR-222, LLR-336
    """
    try:
        first = agent_session.split_cmd(template or "")[:1]
    except ValueError:
        return ""
    return agent_session.substitute(first[0], model, "") if first else ""


def route_cli(row):
    """The CLI a route row launches (`session_adapters.cli_named` over its
    runner, `route_runner`), or "" when it names none of IF-245's CLIs.

    Implements: SR-222, LLR-336
    """
    return session_adapters.cli_named(route_runner(row.cmd_template, row.model))


def _account_problem(aid, cells):
    """Why one account table is malformed, or "" (WI-798's Trust: a bad id
    (outside `ACCOUNT_ID_RE`, or a Windows device name), an unknown key, a
    non-string value, a missing or unknown `cli`, an env declaring its own
    CLI's home variable, a token locator that is not a variable name or that
    its CLI cannot carry, or a malformed `verified`). The schema (the id, the
    keys, every value a string) is decided first, so no later check reads a
    value of the wrong type.

    Implements: SR-222, LLR-336
    """
    if not isinstance(cells, dict):
        return "is not a table"
    unknown = sorted(set(cells) - set(ACCOUNT_KEYS))
    bad_type = [k for k in ACCOUNT_KEYS if k in cells and not isinstance(cells[k], str)]
    schema = (
        (
            not ACCOUNT_ID_RE.match(aid) or _WINDOWS_DEVICES.match(aid),
            "has an id outside [A-Z0-9][A-Z0-9-]* or is a Windows device name",
        ),
        (unknown, "has unknown key(s) {}".format(", ".join(unknown))),
        (bad_type, "has non-string value(s) for {}".format(", ".join(bad_type))),
    )
    why = next((why for bad, why in schema if bad), "")
    if why:
        return why
    cli = cells.get("cli", "")
    homes = {env_name_key(v) for v in session_adapters.HOME_VARIABLES.get(cli, ())}
    declared = parse_env(cells.get("env", ""))
    token = cells.get("token_file_variable", "")
    checks = (
        (not cli, "is missing `cli`"),
        (
            cli not in session_adapters.HOME_VARIABLES,
            "names cli {!r}, outside {}".format(
                cli, "|".join(session_adapters.HOME_VARIABLES)
            ),
        ),
        (
            [k for k in declared if env_name_key(k) in homes],
            "declares its own CLI's home variable in `env`",
        ),
        (
            token and not _VARIABLE_RE.match(token),
            "token_file_variable {!r} is not a variable name".format(token),
        ),
        (
            token and cli not in session_adapters.TOKEN_VARIABLES,
            "cli {!r} carries no long-lived token".format(cli),
        ),
        (
            cells.get("verified") and not _VERIFIED_RE.match(cells["verified"]),
            'verified {!r} is not "<YYYY-MM-DD> <cli version>"'.format(
                cells.get("verified")
            ),
        ),
    )
    return next((why for bad, why in checks if bad), "")


def _load_accounts(text, name):
    """`({id: Account}, errors)` from a TOML registry's `[account.<ID>]`
    tables. A malformed table is an error naming it and is dropped, so an
    Account is built only from a table whose values are all strings; so is
    every table naming a `token_file_variable` another also names, as the
    platform resolves the name (`env_name_key`). A CSV
    registry, or a TOML text with no account table, declares none.

    Implements: SR-222, LLR-336
    """
    try:
        tables = tomllib.loads(text).get("account") or {}
    except tomllib.TOMLDecodeError:
        return {}, []  # load_registry already reports the unparseable file
    accounts, errors = {}, []
    if not isinstance(tables, dict):
        return {}, ["{}: `account` is not a table of accounts".format(name)]
    for aid, cells in tables.items():
        why = _account_problem(aid, cells)
        if why:
            errors.append("{}: [account.{}] {}".format(name, aid, why))
            continue
        accounts[aid] = Account(aid, **{k: cells.get(k, "") for k in ACCOUNT_KEYS})
    named = [
        env_name_key(a.token_file_variable)
        for a in accounts.values()
        if a.token_file_variable
    ]
    for aid in [
        a.id
        for a in accounts.values()
        if named.count(env_name_key(a.token_file_variable)) > 1
    ]:
        errors.append(
            "{}: [account.{}] names token_file_variable {} another account also "
            "names".format(name, aid, accounts[aid].token_file_variable)
        )
        del accounts[aid]
    return accounts, errors


# The safe shape for a Model cell: letters/digits plus . _ : - / (router ids
# like `org/model` and `us.anthropic....` stay legal). Anything else — quotes,
# spaces, %, &, | … — is refused at load (see the check in load_registry).
MODEL_SLUG_RE = re.compile(r"^[A-Za-z0-9._:/\-]+$")


def _rows_from_csv(text, name):
    """`(rows, errors)` from the CSV carrier — each row a `{column: cell}` dict.

    The HEADER CHECK lives here and only here, because it is a property of the
    CSV carrier: that carrier declares its schema in a header, so a header
    missing `CmdTemplate` is a registry that cannot launch anything and must
    PAGE rather than degrade. TOML declares no header — an absent key IS the
    empty cell — so its analogue is "the file does not parse", which the TOML
    branch raises instead."""
    errors = []
    rows = list(csv.reader(io.StringIO(_spine.csv_body(text))))
    if not rows:
        return [], []
    header = [h.strip() for h in rows[0]]
    # Map the columns we need by name so column order is not load-bearing.
    # `Provider` is accepted as the legacy alias for `Family` (never-breaking).
    idx = {
        name_: header.index(name_)
        for name_ in REGISTRY_FIELDS + ("Provider",)
        if name_ in header
    }
    # Identity's Family key: the Family column, or a legacy Provider column.
    fam_key = (
        "Family" if "Family" in idx else ("Provider" if "Provider" in idx else None)
    )
    for need in ("Id", "Model", "Version", "Tier", "CmdTemplate"):
        if need not in idx:
            errors.append("{}: header is missing the {!r} column".format(name, need))
    if fam_key is None:
        errors.append(
            "{}: header is missing the 'Family' column (legacy 'Provider' also "
            "accepted)".format(name)
        )
    if errors:
        return [], errors
    out = []
    for row in rows[1:]:
        if not any(c.strip() for c in row):
            continue  # blank line
        cells = {
            col: (row[i].strip() if i < len(row) else "") for col, i in idx.items()
        }
        cells["Family"] = cells.get(fam_key, "")
        out.append(cells)
    return out, []


def load_registry(path):
    """Parse the model registry into a `Registry` ({id: Model} and its
    declared `accounts`), plus a list of error strings for malformed rows (a
    duplicate/invalid id, an out-of-vocabulary tier, a short row) and
    malformed account tables (`_load_accounts`, each dropped). Absent file ->
    ({}, []) so the caller degrades to today's behavior; an empty file
    declares no rows and no accounts. utf-8/errors=replace so a stray byte
    degrades, never crashes.

    `path` may name either carrier; `spine_carrier.resolve` returns whichever
    is live and REFUSES both at once, so a half-finished migration cannot leave
    the router quietly reading the stale half. An unparseable TOML registry is
    an ERROR, never an empty pool: `{}` here means "no models are enabled",
    which under managed routing reads as a consent decision rather than a
    broken file — a page the human never gets.

    Implements: SR-154, SR-222, LLR-044, LLR-336
    """
    live = spine_carrier.resolve(Path(path))
    if live is None:
        return Registry(), []
    models, errors = Registry(), []
    try:
        text = live.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return Registry(), ["cannot read {}: {}".format(live, exc)]
    if live.suffix == ".toml":
        rows = spine_carrier.rows_seq_from_text(text, "Id", ".toml")
        if rows is None:
            return Registry(), [
                "{}: does not parse as TOML — refusing to report an unreadable "
                "registry as an empty pool".format(live.name)
            ]
        models.accounts, errors = _load_accounts(text, live.name)
    else:
        rows, errors = _rows_from_csv(text, live.name)
        if errors:
            return Registry(), errors

    def cell(row, name):
        return str(row.get(name) or "").strip()

    for row in rows:
        mid = cell(row, "Id")
        if mid.startswith("#"):
            continue  # a commented row
        # A -000-style placeholder ships inert like every other registry.
        if mid.endswith("-000") or mid == "":
            continue
        if not ID_RE.match(mid):
            errors.append(
                "{}: id {!r} is not [A-Z0-9][A-Z0-9.-]* (uppercase + digits + "
                "hyphen + dot)".format(live.name, mid)
            )
            continue
        if mid in models:
            errors.append("{}: duplicate id {!r}".format(live.name, mid))
            continue
        tier = normalize_tier(cell(row, "Tier"))
        if tier not in TIER_ORDER:
            errors.append(
                "{}: id {!r} has tier {!r}; expected one of {}".format(
                    live.name, mid, tier, "|".join(TIER_ORDER)
                )
            )
            continue
        model_cell = cell(row, "Model")
        if model_cell and not MODEL_SLUG_RE.match(model_cell):
            # The Model cell rides `{model}` substitution into a session
            # argv; on Windows a `.cmd`-shim CLI re-parses that line under
            # cmd.exe, where an embedded quote re-arms `&`/`|` as live
            # operators (the BatBadBut class). A tracked registry must not be a
            # command-injection vector: refuse the row loudly (a preflight
            # failure under managed routing) — repo-review 2026-07-21 H-4.
            errors.append(
                "{}: id {!r} Model {!r} has characters outside "
                "[A-Za-z0-9._:/-]; refusing (shell-unsafe in a .cmd-shim "
                "argv)".format(live.name, mid, model_cell)
            )
            continue
        tmpl = cell(row, "CmdTemplate")
        models[mid] = Model(
            id=mid,
            family=cell(row, "Family"),
            model=cell(row, "Model"),
            version=cell(row, "Version"),
            tier=tier,
            cmd_template=tmpl,
            env=cell(row, "Env"),
            notes=cell(row, "Notes"),
        )
    return models, errors


def parse_env(spec):
    """Parse an `Env` cell (`KEY=value;KEY2=value2`) into a dict, to be merged
    over the inherited environment at launch. Lenient by construction — an entry
    without `=` or an empty key is skipped rather than crashing a walk-away run
    (a value may contain `=` but not `;`, the row separator).

    Implements: SR-154, LLR-044
    """
    out = {}
    for part in (spec or "").split(";"):
        part = part.strip()
        if not part or "=" not in part:
            continue
        key, _, val = part.partition("=")
        key = key.strip()
        if key:
            out[key] = val.strip()
    return out


def parse_tag_rank(spec):
    """Parse a `ga>preview>beta>exp` ordering into {tag: rank} (higher = earlier
    = preferred). Empty/unparseable -> DEFAULT_TAG_RANK."""
    toks = [t for t in re.split(r"[>,\s]+", (spec or "").strip().lower()) if t]
    if not toks:
        return dict(DEFAULT_TAG_RANK)
    return {tok: len(toks) - 1 - i for i, tok in enumerate(toks)}


def load_tag_rank(path, env=None):
    """The maturity rank vocabulary for version-less resolution: the
    AGENT_TAG_RANK env knob wins, else a `# tag-rank: ...` comment line in the
    registry file, else DEFAULT_TAG_RANK. Deterministic and offline.

    THE LINE SCAN SURVIVED THE CARRIER CHANGE UNCHANGED, and that is not a
    coincidence: TOML's comment syntax is the `#` line this convention already
    used, so `migrate_carrier` carries every comment across BYTE-FOR-BYTE and in
    place. What did have to change is finding the file — `resolve` picks the
    live carrier, and without it a migrated repo silently fell back to
    DEFAULT_TAG_RANK, resetting the maturity vocabulary that decides which row a
    version-less enable-list token resolves to."""
    env = os.environ if env is None else env
    if env.get("AGENT_TAG_RANK"):
        return parse_tag_rank(env["AGENT_TAG_RANK"])
    live = spine_carrier.resolve(Path(path))
    if live is None:
        return dict(DEFAULT_TAG_RANK)
    try:
        text = live.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return dict(DEFAULT_TAG_RANK)
    for ln in text.splitlines():
        m = re.match(r"\s*#\s*tag-rank\s*:\s*(.+)$", ln, re.I)
        if m:
            return parse_tag_rank(m.group(1))
    return dict(DEFAULT_TAG_RANK)


def _maturity_of(model):
    """The maturity tag of a registry row (`preview`/`beta`/`exp`/`ga`), read
    from its Version (the ruled home) or Model line — GA/untagged is the
    default. Tokenized so a numeric/date version reads GA, never a substring
    hit."""
    toks = set(
        re.split(r"[^a-z0-9]+", "{} {}".format(model.version, model.model).lower())
    )
    for tag in _MATURITY_TOKENS:
        if tag in toks:
            return tag
    return "ga"


_DATE_RE = re.compile(r"(?:^|[^0-9])(\d{8}|\d{4}-\d{2}-\d{2})(?:[^0-9]|$)")


def _version_key(model, tag_rank):
    """The comparison key for version-less resolution: (dotted-numeric tuple,
    maturity rank, date stamp) — numeric dominates, maturity breaks a numeric
    tie, the date stamp is the final tiebreak. A pure date carries no numeric
    (so numeric always dominates a date-kind mix), and a maturity tag alone
    sorts by rank."""
    v = (model.version or "").strip()
    dm = _DATE_RE.search(" " + v + " ")
    date = int(dm.group(1).replace("-", "")) if dm else 0
    numeric = ()
    if not (dm and dm.group(1).replace("-", "") == re.sub(r"[^0-9]", "", v)):
        nm = re.match(r"(\d+(?:\.\d+)*)", v)
        if nm:
            numeric = tuple(int(p) for p in nm.group(1).split("."))
    rank = tag_rank.get(_maturity_of(model), tag_rank.get("ga", 3))
    return (numeric, rank, date)


def resolve_token(token, registry, tag_rank=None):
    """Resolve one enable-list token to a registry id, or (None, reason).

    An exact id wins outright. Otherwise the token resolves over rows whose
    normalized `Family`-`Model` (column-keyed, uppercased — the id is NEVER
    parsed) equals it: this stays INTRA-line (the `-PRO` correction — resolution
    never crosses a model line). `preview`/`exp` rows are skipped unless named
    or the only candidates; the survivor is the newest by `_version_key`, and
    among equal-key pairs (one model line, several routes) REGISTRY ROW ORDER
    decides. "Newest" is computed only over rows present in the registry —
    deterministic and offline."""
    tag_rank = tag_rank or DEFAULT_TAG_RANK
    t = (token or "").strip()
    if t in registry:
        return t, "exact id"
    tu = t.upper()
    cands = [
        mid
        for mid, m in registry.items()
        if "{}-{}".format(m.family, m.model).upper() == tu
    ]
    if not cands:
        return None, "no exact id and no Family-Model match"
    non_skipped = [
        mid for mid in cands if _maturity_of(registry[mid]) not in _SKIP_MATURITY
    ]
    pool = set(non_skipped or cands)
    best, best_key = None, None
    for mid in registry:  # registry insertion order breaks equal-key ties (first wins)
        if mid not in pool:
            continue
        key = _version_key(registry[mid], tag_rank)
        if best is None or key > best_key:
            best, best_key = mid, key
    return best, "resolved {!r} -> {} (newest of {})".format(t, best, "|".join(cands))


def resolve_enabled(enabled, registry, tag_rank=None):
    """Resolve the ordered enable-list to its ENTRIES, preserving preference
    order and de-duplicating. Returns (entries, errors); an unresolvable token
    or a malformed qualifier becomes an error string naming the line
    (surfaced in the managed preflight), never stripped to the unqualified
    entry. An entry is the identity every consumer carries from here (see
    `entry_route`): an unqualified entry's key is the concrete registry id
    its token resolves to, a qualified one's is `ROUTE@ACCOUNT`
    (`resolve_entry`).

    Implements: SR-154, SR-222, LLR-044, LLR-336
    """
    resolved, errors, seen = [], [], set()
    for tok in enabled:
        entry, error = resolve_entry(tok, registry, tag_rank)
        if error:
            errors.append(error)
            continue
        if entry not in seen:
            seen.add(entry)
            resolved.append(entry)
    return resolved, errors


def resolve_entry(token, registry, tag_rank=None):
    """`(entry, None)` for one enable-list token, else `(None, why)` naming
    the token. `ROUTE` resolves as `resolve_token` does; `ROUTE@ACCOUNT`
    resolves its route the same way and is refused (WI-798's Trust) when a
    side is empty, the line holds more than one `@`, the account is not
    declared, its `cli` is not the route's CLI, the route's env declares that
    CLI's home variable, or the route's env and the account's declare one
    name, so neither side silently wins.

    Implements: SR-222, LLR-336
    """
    route_tok, at, aid = (token or "").strip().partition("@")
    if at and (not route_tok or not aid or "@" in aid):
        return (
            None,
            "{!r}: a qualifier is ROUTE@ACCOUNT, one `@`, both sides set".format(token),
        )
    rid, reason = resolve_token(route_tok, registry, tag_rank)
    if rid is None:
        return None, (
            "{!r} is not a row in docs/agents.toml and does not resolve "
            "to one ({})".format(token, reason)
        )
    if not at:
        return rid, None
    why = qualifier_problem(
        registry[rid], getattr(registry, "accounts", {}).get(aid), aid
    )
    return (None, "{!r}: {}".format(token, why)) if why else (entry_of(rid, aid), None)


def qualifier_problem(row, account, aid):
    """Why `row` cannot run under the account `aid` (`account`, None when it
    is not declared), or "": the qualifier and conflict rules of
    `resolve_entry`, also re-checked by the launch environment.

    Implements: SR-222, LLR-336
    """
    if account is None:
        return "account {} is not declared in docs/agents.toml".format(aid)
    cli = route_cli(row)
    if account.cli != cli:
        return "account {} signs into {}, but route {} launches {}".format(
            aid, account.cli, row.id, cli or "no known CLI"
        )
    route_env = {env_name_key(k): k for k in parse_env(row.env)}
    homes = [
        v for v in session_adapters.HOME_VARIABLES[cli] if env_name_key(v) in route_env
    ]
    if homes:
        return "route {} declares {} in its env, which account {}'s home sets".format(
            row.id, ", ".join(homes), aid
        )
    both = [
        route_env[k]
        for k in map(env_name_key, parse_env(account.env))
        if k in route_env
    ]
    if both:
        return "route {} and account {} both declare {} in their env".format(
            row.id, aid, ", ".join(both)
        )
    return ""


def entry_of(route_id, account=""):
    """The entry key of `route_id` under `account`: the route id itself for
    the person's ambient login (no account), else `ROUTE@ACCOUNT`.

    Implements: SR-222, LLR-336
    """
    return "{}@{}".format(route_id, account) if account else route_id


def entry_route(entry):
    """The registry route id an enabled ENTRY selects. The entry, not the
    bare route id, is the identity that selection, preference and cooldowns
    carry: `resolve_enabled` produces the entries once, `select`,
    `winstay_preferred_ids` and the planner pair return them, and
    `available`/`cool` key cooldowns on them. A registry row is read only
    through this function, never by taking an entry for its route id. An
    unqualified entry's key is its route id; `ROUTE@ACCOUNT` selects ROUTE.

    Implements: SR-154, SR-222, LLR-044, LLR-336
    """
    return entry.partition("@")[0]


def entry_account(entry):
    """The account an enabled entry runs under, "" for the ambient login.

    Implements: SR-222, LLR-336
    """
    return entry.partition("@")[2]


def account_of(registry, entry):
    """The declared `Account` an entry runs under, or None for an ambient
    (unqualified) entry. A qualified entry resolved by `resolve_entry` always
    names a declared account; one that does not raises LookupError, never
    reading as the ambient login.

    Implements: SR-222, LLR-336
    """
    aid = entry_account(entry)
    if not aid:
        return None
    found = getattr(registry, "accounts", {}).get(aid)
    if found is None:
        raise LookupError("{}: account {} is not declared".format(entry, aid))
    return found


# The grammar of an enable-list entry as a preference may name it: a registry
# id, optionally qualified `@ACCOUNT` (both sides the id charset).
ENTRY_RE = re.compile(r"^[A-Z0-9][A-Z0-9.\-]*(@[A-Z0-9][A-Z0-9.\-]*)?$")


def unverified_lines(registry, enabled):
    """One line per enabled entry whose account is unverified
    (`Account.unverified`): what preflight prints, never a refusal (D-011).

    Implements: SR-222, LLR-336
    """
    lines = []
    for entry in enabled:
        account = account_of(registry, entry)
        if account is not None and account.unverified:
            lines.append(
                "{}: account {} is UNVERIFIED — a Claude login other than the "
                "ambient one whose login-isolation check has not passed "
                "(`verified` is empty)".format(entry, account.id)
            )
    return lines


def _row_of(registry, entry):
    """The registry row `entry` selects, or None when it names none.

    Implements: SR-154, LLR-044
    """
    return registry.get(entry_route(entry))


def _parse_enabled_line(line):
    """Split one non-comment agents-enabled line into (token, {phase: weight},
    error). `token` is the first whitespace field (the id, resolved elsewhere);
    the rest are optional `<PHASE>=<int>` draw-weight annotations (WI-236). The
    weight dict is keyed by CONCRETE phase (the `REVIEW` umbrella expands to
    REVIEW-A/REVIEW-B). `error` is None on success, else a human string naming
    the malformed field — the caller surfaces it as a preflight failure, since
    the file is the consent surface (never a silent drop)."""
    fields = line.split()
    token = fields[0]
    # An annotation-only line (weights with no id in front) is a common slip —
    # name it precisely rather than failing later as an unresolvable id.
    if "=" in token:
        return (
            token,
            {},
            "missing id before annotations (line starts with {!r})".format(token),
        )
    weights = {}
    for field in fields[1:]:
        raw_phase, sep, raw_val = field.partition("=")
        if not sep:
            return (
                token,
                {},
                "malformed annotation {!r} (expected PHASE=int)".format(field),
            )
        # Strict, case-SENSITIVE match to the documented grammar — the file is a
        # consent surface, so a lowercase or misspelled phase is a hard error.
        if raw_phase not in WEIGHT_PHASES:
            return (
                token,
                {},
                "unknown phase {!r} (expected one of {})".format(
                    raw_phase, "|".join(WEIGHT_PHASES)
                ),
            )
        if not _WEIGHT_INT_RE.match(raw_val):
            return (
                token,
                {},
                "weight {!r} for {} is not a non-negative integer".format(
                    raw_val, raw_phase
                ),
            )
        weight = int(raw_val)
        for key in _WEIGHT_PHASE_ALIAS.get(raw_phase, (raw_phase,)):
            if key in weights:
                return token, {}, "duplicate phase {} on one line".format(raw_phase)
            weights[key] = weight
    return token, weights, None


class EnabledUnreadable(OSError):
    """docs/agents-enabled exists but cannot be read. Never read as absent
    (WI-798, D-012): absent means routing off, and reading an unreadable
    consent surface that way would drop a consented run onto the
    single-model path. Every caller refuses on it.

    Implements: SR-222, LLR-336
    """


def load_enabled_entries(path):
    """Parse docs/agents-enabled into ordered (token, {phase: weight}) entries
    plus a list of malformed-annotation errors, each naming the offending line
    (WI-236). Absent/empty file -> ([], []); a file that exists but cannot be
    read raises EnabledUnreadable. This is the annotation-aware read;
    `load_enabled` wraps it for callers that only need the ids.

    Implements: SR-222, LLR-336
    """
    path = Path(path)
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except FileNotFoundError:
        return [], []
    except OSError as exc:
        raise EnabledUnreadable(
            "{} exists but cannot be read ({}); it is the consent surface, so "
            "routing is neither on nor off until it reads".format(path, exc)
        ) from exc
    entries, errors = [], []
    for ln in lines:
        stripped = ln.strip()
        if not stripped or stripped.startswith("#"):
            continue
        token, weights, err = _parse_enabled_line(stripped)
        entries.append((token, weights))
        if err:
            errors.append("{!r}: {}".format(stripped, err))
    return entries, errors


def load_enabled(path):
    """The ordered enable-list ids (docs/agents-enabled): the first field of
    every non-empty, non-# line, in preference order. Absent/empty -> [] (routing
    off). This is the consent surface — its presence is what turns managed routing
    on; per-phase draw-weight annotations (WI-236) are stripped here and read via
    `load_enabled_entries`."""
    entries, _errors = load_enabled_entries(path)
    return [token for token, _weights in entries]


def resolved_weights(entries, registry, tag_rank=None):
    """Map each resolved entry (`resolve_enabled`'s key) to its {phase: weight} from parsed enable-list
    `entries` [(token, weights)] (WI-236). Returns (weight_map, errors). An
    unannotated or unresolvable token contributes nothing (unresolvable tokens are
    already reported by resolve_enabled). A CONFLICTING redeclaration of the same
    id (two lines resolving to one id with different weights) is a preflight error
    naming the id — the consent surface must not silently keep one; an IDENTICAL
    redeclaration is a benign dedup. Only ids that carry a declared weight appear
    — an absent id weighs 1 (uniform) at select time."""
    out, errors = {}, []
    for _token, weights in entries:
        if not weights:
            continue
        rid, _error = resolve_entry(_token, registry, tag_rank)
        if rid is None:
            continue
        if rid in out:
            if out[rid] != weights:
                errors.append(
                    "id {} redeclared with conflicting weights ({} vs {})".format(
                        rid, out[rid], weights
                    )
                )
            continue  # identical redeclaration -> benign dedup
        out[rid] = weights
    return out, errors


def phase_weights(weight_map, phase):
    """The per-id draw weights for `phase` from the resolved weight map
    ({id: {phase: int}}), keyed by concrete phase. Absent -> {} (uniform, i.e.
    today's line-order tie-break). BUILD covers the legacy/interactive '' phase."""
    key = "BUILD" if phase in ("BUILD", "") else phase
    return {rid: wm[key] for rid, wm in (weight_map or {}).items() if key in wm}


def available(cooldowns, entry, now):
    """True when `entry` is not cooling down. `cooldowns` maps an enabled entry
    -> the epoch it is available again (the generalized rate-limit backoff,
    per entry, so two entries of one route cool independently)."""
    until = (cooldowns or {}).get(entry)
    return until is None or until <= now


def cool(cooldowns, entry, now, seconds):
    """Put `entry` on cooldown until now+seconds (its limit is probably
    exhausted, or its session failed to start / stalled). In-place on the dict."""
    cooldowns[entry] = now + max(0, seconds)


def _weighted_rotation(candidates, weights, counter):
    """Deterministic weighted pick from an ORDERED legal candidate list (WI-236).

    `weights` maps id -> a non-negative draw weight for THIS phase (absent == 1);
    `counter` is the durable per-train session counter (never randomness). The
    pick is a stateless weighted rotation: `counter mod (sum of positive weights)`
    indexes the cumulative weight ranges, so over N draws each id lands its share
    and the sequence is exactly reproducible from history.

      - Zero weight is FALLBACK-ONLY: an id weighing 0 is held out of the draw
        while any positive-weight candidate exists, but is taken when it is the
        sole legal candidate (routing never dead-ends on a 0).
      - Uniform positive weights (the unannotated file, or an all-equal
        annotation) collapse to the first candidate — line order is the tie-break
        among equal weights, byte-identical to before weights existed.
      - Renormalization is implicit: a cooled model is simply absent from
        `candidates`, so the remaining shares recompute over the survivors.
    """
    if not candidates:
        return None
    weights = weights or {}
    positives = [
        (cid, weights.get(cid, 1)) for cid in candidates if weights.get(cid, 1) > 0
    ]
    if not positives:
        return candidates[0]  # every legal candidate is fallback-only: order decides
    pos_weights = [w for _cid, w in positives]
    if len(set(pos_weights)) == 1:
        return positives[0][0]  # uniform weights -> line-order tie-break (today)
    slot = counter % sum(pos_weights)
    accumulated = 0
    for cid, weight in positives:
        accumulated += weight
        if slot < accumulated:
            return cid
    return positives[-1][0]


def _pick(avail, registry, exclude, prefer_different, preferred_ids, weights, counter):
    """From the same-tier available ids (in enable-list order), apply the
    AGENT_PREFER_MAP pin, the prefer-different heterogeneity filter, and the
    weighted rotation. Returns (chosen_id, note_suffix) — a pin wins its phase
    outright over weights; weights govern the unpinned remainder. `note_suffix`
    carries the DEGRADED banner when only same-family models remain."""
    pool = avail
    suffix = ""
    if prefer_different:
        different = [e for e in avail if _row_of(registry, e).family not in exclude]
        if different:
            pool = different
        else:
            # Degraded: only same-family models are available. Legal — fresh
            # context is the invariant, family diversity is best-effort.
            suffix = (
                " — DEGRADED: no different-family model available, same-family "
                "review (weaker corroboration)"
            )
    pin = next((mid for mid in (preferred_ids or ()) if mid in pool), None)
    if pin is not None:
        return pin, suffix  # the pin wins its phase outright, over any weight
    return _weighted_rotation(pool, weights, counter), suffix


def select(
    enabled,
    registry,
    tier,
    now=0.0,
    cooldowns=None,
    exclude_families=(),
    prefer_different=False,
    preferred_ids=(),
    weights=None,
    counter=0,
):
    """Pick an enabled entry from the pool, or None. Returns (entry, reason) —
    the reason is the line the coordinator LOGS before launch (no silent swap).

    Rules, in order:
      - Only enabled entries whose route is a registry row and that are not
        cooling down.
      - Walk from `tier` UP to strong; never select a weaker tier than asked.
      - A `preferred_ids` pin (AGENT_PREFER_MAP) wins its phase outright when it
        is legal; unknown, disabled, wrong-tier, cooling, or heterogeneity-barred
        pins simply fall through (a preference never changes the requested tier).
      - When prefer_different, prefer an id whose FAMILY (who trained it — never
        the route it is reached by) is not in exclude_families; if none
        qualifies, fall back to any available one (degraded availability is
        legal — same-family review is allowed, it just earns a weaker
        corroboration signal). A router-fronted row shares its native sibling's
        Family, so it is NOT diverse from it.
      - Among the unpinned legal remainder, `weights`/`counter` drive a
        deterministic weighted rotation (WI-236); absent weights == uniform ==
        the historical line-order pick, byte-identical to before.

    Implements: SR-154, LLR-044
    """
    cooldowns = cooldowns or {}
    exclude = set(exclude_families or ())
    tier = normalize_tier(tier)  # legacy `weak` selects the `quick` tier
    if tier not in TIER_ORDER:
        return None, "unknown tier {!r} (expected {})".format(
            tier, "|".join(TIER_ORDER)
        )
    start = TIER_ORDER.index(tier)
    for ti in range(start, len(TIER_ORDER)):
        this_tier = TIER_ORDER[ti]
        avail = [
            e
            for e in enabled
            if (m := _row_of(registry, e)) is not None
            and m.tier == this_tier
            and available(cooldowns, e, now)
        ]
        if not avail:
            continue
        bumped = " (tier bumped up from {})".format(tier) if ti != start else ""
        chosen, suffix = _pick(
            avail, registry, exclude, prefer_different, preferred_ids, weights, counter
        )
        return chosen, "selected {} [{}]{}{}".format(chosen, this_tier, bumped, suffix)
    return None, (
        "no enabled model available at tier {} or stronger (all cooled down or "
        "none enabled) — page/wait rather than select a weaker tier".format(tier)
    )


def winstay_preferred_ids(next_primary, enabled, registry, cooldowns=None, now=0.0):
    """Resolve a win-stay `next_primary` (the reviewer FAMILY `escalate` returns
    when the last round's margin cleared the bar) into the enabled model ids of
    that family's entries, for use as `select()`'s `preferred_ids` — this is how the
    documented win-stay policy actually biases the next draw (WI-264, M-34).

    Fail-open by contract (the 2026-07-21 author-identity lesson — dormant policy
    is being wired into the LIVE routing path, so it must never wedge a session):
    a None/blank `next_primary`, or a family with no enabled + registered +
    currently-available (non-cooling) member, yields () — the caller then draws
    the ordinary WI-263 weighted baseline, unchanged. A returned id still only
    PINS if `select()` also finds it in the tier-filtered pool, so an off-tier
    win-stay family degrades there too (a preference never changes the tier).
    Enable-list order is preserved, so a multi-model family pins its top row."""
    if not next_primary:
        return ()
    fam = str(next_primary).strip()
    if not fam:
        return ()
    cooldowns = cooldowns or {}
    return tuple(
        e
        for e in enabled
        if (m := _row_of(registry, e)) is not None
        and m.family == fam
        and available(cooldowns, e, now)
    )


def pool_context(enabled, registry, cooldowns=None, now=0.0):
    """The enabled pool, one line per entry, for a page-human/failure banner:
    the entry, its row's tier + Family, the entry's cooling-vs-available
    state, and the row's `Notes` cell.
    Notes is the declared home for the provider's install/sign-in hint (e.g.
    `sign in: opencode auth login`), so an exhausted pool tells the human what
    to actually DO — the kit itself stays provider-neutral. Lenient: an enabled
    id missing from the registry (can't happen past preflight) still renders."""
    cooldowns = cooldowns or {}
    lines = ["enabled pool (docs/agents-enabled x docs/agents.toml):"]
    for entry in enabled:
        m = _row_of(registry, entry)
        if m is None:
            lines.append("  - {} (not in docs/agents.toml)".format(entry))
            continue
        wait = cooldowns.get(entry, 0.0) - now
        state = "cooling ~{}s".format(int(wait)) if wait > 0 else "available"
        note = " — {}".format(m.notes) if m.notes else ""
        lines.append(
            "  - {} [{}, {}] {}{}".format(entry, m.tier, m.family, state, note)
        )
    return "\n".join(lines)


def load_constants(env=None):
    """The escalation constants: the per-repo-overridable defaults, each read from
    its env var when set to a valid non-negative number — `margin` parses as a
    float (substance margins live in [0, 1]; the old int()-only parse made 0
    and the impossible 1 the only reachable overrides, M-34), the counters as
    ints — else the default (a bad value never crashes the run)."""
    env = os.environ if env is None else env
    out = dict(DEFAULT_CONSTANTS)
    for key, var in _CONST_ENV.items():
        raw = env.get(var)
        if raw is None:
            continue
        try:
            val = float(raw) if key == "margin" else int(raw)
        except (TypeError, ValueError):
            continue
        if val >= 0:
            out[key] = val
    return out


def _consecutive_changes_requested(rounds):
    """How many of the most recent rounds ended CHANGES-REQUESTED, contiguously."""
    n = 0
    for rnd in reversed(rounds):
        if str(rnd.get("verdict", "")).upper() == "CHANGES-REQUESTED":
            n += 1
        else:
            break
    return n


def escalate(rounds, constants=None, swapped=False, at_top_tier=False, fails_since=0):
    """The fixed win-stay/lose-shift decision after a review round.

    `rounds` is the chronological history, each a dict:
      verdict          -> APPROVE | CHANGES-REQUESTED  (the merged round result)
      tier             -> the implementer tier this round ran at (quick/medium/strong)
      margin           -> substance margin between the two reviewers this round
      primary          -> the higher-substance family this round (for win-stay)
      contradiction    -> True when the two reviewers gave opposite verdicts
      tripwire         -> True when any anti-gaming tripwire fired
    `swapped`/`at_top_tier` are the coordinator's applied-so-far state.

    `fails_since` (WI-171) is the round index the shared-failure tally counts
    from: the coordinator advances it to len(rounds) each time a page dispatches,
    so an already-paged (and, under autonomous policy, already-ruled) strong-tier
    failure cannot re-page forever — only NEW strong-tier failures recorded after
    the last dispatch accumulate toward the shared-failure regime. The last-round
    tripwire and two-round contradiction pages carry their own bounded windows and
    are unaffected (the default 0 preserves the whole-run count for callers that
    pass no index).

    Returns {'action', 'reason', 'next_primary'} with action in
    {continue, swap-implementer, tier-up, page-human}.

    Implements: SR-154, LLR-081
    """
    c = constants or DEFAULT_CONSTANTS
    if not rounds:
        return {
            "action": "continue",
            "reason": "no review round yet",
            "next_primary": None,
        }
    last = rounds[-1]

    # --- page-the-human conditions (the shared-failure / distrust regime) ------
    if last.get("tripwire"):
        return {
            "action": "page-human",
            "reason": "a tripwire fired — anti-gaming stop, never absorbed silently",
            "next_primary": None,
        }
    if (
        len(rounds) >= 2
        and last.get("contradiction")
        and rounds[-2].get("contradiction")
    ):
        return {
            "action": "page-human",
            "reason": "reviewers gave opposite verdicts twice running — the spec is likely ambiguous",
            "next_primary": None,
        }
    top_tier_fails = sum(
        1
        for r in rounds[max(0, fails_since) :]
        if r.get("tier") == "strong"
        and str(r.get("verdict", "")).upper() == "CHANGES-REQUESTED"
    )
    if top_tier_fails >= c["page_top_tier_fails"]:
        return {
            "action": "page-human",
            "reason": "{} top-tier review failures — the shared-failure regime (the spec is wrong, not the model)".format(
                top_tier_fails
            ),
            "next_primary": None,
        }

    # --- win-stay / lose-shift ------------------------------------------------
    consecutive = _consecutive_changes_requested(rounds)
    if consecutive >= c["swap_after"]:
        if not swapped:
            return {
                "action": "swap-implementer",
                "reason": "{} consecutive failed review gates — swap the implementer family (cheap test for idiosyncratic failure)".format(
                    consecutive
                ),
                "next_primary": None,
            }
        if not at_top_tier:
            return {
                "action": "tier-up",
                "reason": "the family swap also failed — raise the tier (only now, never before the swap)",
                "next_primary": None,
            }
        return {
            "action": "page-human",
            "reason": "swap and tier-up both exhausted at the top tier — page the human",
            "next_primary": None,
        }

    # A clean approve, or a single failure still inside the streak budget: keep
    # going. The higher-substance family becomes next round's primary feedback
    # source only when this round's margin cleared the bar (win-stay).
    next_primary = last.get("primary") if last.get("margin", 0) >= c["margin"] else None
    return {
        "action": "continue",
        "reason": (
            "margin {} >= {}: {} leads next round's feedback".format(
                last.get("margin", 0), c["margin"], next_primary
            )
            if next_primary
            else "within the streak budget — continue with the current routing"
        ),
        "next_primary": next_primary,
    }


def failure_action(human_held, keep_nondependent=False):
    """What a page-the-human escalation does, keyed to SN-029's ordinal
    comparison rather than the retired three-value enum.

    In every mode the causing WI and its hard-edge dependents PAUSE; what
    differs is what happens AROUND that — and those are two genuinely separate
    questions, which is why the enum needed three values to express two bits.
    Is the tier in process still the human's to approve (`human_held`), and may
    other work keep running meanwhile (`keep_nondependent`)? The old
    `single-approve` and `autonomous` differed only in the design-check leg while
    sharing the second answer; splitting them makes each dial mean one thing.

    Redesign re-enters the change-intake flow (process.md §5 — linked, not
    restated). Returns a dict the coordinator enacts and logs.

    Implements: SR-154, LLR-081
    """
    if human_held:
        return {
            "mode": "human-held",
            "pause_wi": True,
            "keep_nondependent": bool(keep_nondependent),
            "design_check": False,
            "note": (
                "human-held tier: surface the block for approval"
                + (
                    "; keep working non-dependent work items to completion"
                    if keep_nondependent
                    else "; start nothing new, let in-flight sessions close "
                    "out, then alert the user"
                )
            ),
        }
    return {
        "mode": "loop-held",
        "pause_wi": True,
        # The DECLARED dial, not a hardcoded True. The two questions are
        # independent — that is the entire reason the enum's three words became
        # two dials — so a loop-held tier that was told to drain must drain.
        # Hardcoding it here made the returned dict, documented as "what the
        # coordinator enacts and logs", report the opposite of the owner's
        # explicit setting.
        "keep_nondependent": bool(keep_nondependent),
        "design_check": True,
        "note": "loop-held tier: schedule a fresh strong-tier, different-family design-check session to rule grind-through vs redesign, document every assumption, and continue (redesign re-enters process.md 5)",
    }


# --- the two-hat planner pair (dual-plan decomposition, DP-001 plan P3) ----- #
# A PURE selection/fallback library: it composes `select()` for the two planner
# hats and never launches a session (the coordinator, P6, owns launch-and-feed-
# back). Its seams stay IF-044/IF-045 — no file I/O beyond what agent_route
# already reads. The machine-readable reason codes below are the round-artifact /
# telemetry key for WHY a pair is diverse or degraded.
PAIR_TWO_FAMILY = "two-family"  # happy path: the two hats got different Family lines
PAIR_SINGLE_FAMILY = (
    "single-family-pool"  # degraded at SELECTION: only one family enabled
)
PAIR_RUNTIME_FALLBACK = (
    "runtime-nonresponse-fallback"  # degraded at LAUNCH: a routed family went dark
)
PAIR_NO_MODEL = "no-model-available"  # the pool has nothing routable at/above tier
PAIR_NO_RESPONDER = (
    "no-responding-family"  # every non-failed family is also unavailable
)


class PlannerSession:
    """One planner-hat session selection — the enabled entry routed to a hat,
    with `model_id` the registry route that entry selects. FRESHNESS is object
    identity: the coordinator relies on each returned session being a NEW
    instance (never the failed one reused) so a relaunch starts from clean
    context. Two same-family sessions are two DISTINCT objects that may share
    an entry — independent runs, weaker corroboration."""

    __slots__ = ("hat", "entry", "family", "tier")

    def __init__(self, hat, entry, family, tier):
        self.hat = hat
        self.entry = entry
        self.family = family
        self.tier = tier

    @property
    def model_id(self):
        """The registry route this session's entry selects.

        Implements: SR-155, LLR-072
        """
        return entry_route(self.entry)

    def __repr__(self):  # for round-artifact / test readability
        return "PlannerSession(hat={!r}, entry={!r}, family={!r}, tier={!r})".format(
            self.hat, self.entry, self.family, self.tier
        )


class PlannerPair:
    """The result of routing the two planner hats: the two `PlannerSession`s (or
    `(None, None)` when nothing is routable), the machine-readable `reason` code
    (one of the PAIR_* constants — the telemetry key), `degraded` (True when
    family diversity was not achieved), and a human `detail` line to log."""

    __slots__ = ("sessions", "reason", "degraded", "detail")

    def __init__(self, sessions, reason, degraded, detail):
        self.sessions = sessions
        self.reason = reason
        self.degraded = degraded
        self.detail = detail

    def __repr__(self):
        return "PlannerPair(sessions={!r}, reason={!r}, degraded={!r})".format(
            self.sessions, self.reason, self.degraded
        )


def _session(hat, entry, registry, requested_tier):
    """Build a fresh PlannerSession for `entry`, reading its Family + the
    row's actual tier from the registry (a tier bump means the row's tier, not
    the requested one). A missing row degrades to the requested tier / empty
    family rather than crashing a walk-away run."""
    m = _row_of(registry, entry)
    fam = m.family if m is not None else ""
    tier = m.tier if m is not None else requested_tier
    return PlannerSession(hat, entry, fam, tier)


def planner_pair(
    enabled,
    registry,
    tier,
    now=0.0,
    cooldowns=None,
    preferred_ids=(),
    hats=("A", "B"),
):
    """Route the two planner hats to two FRESH sessions (DP-001 plan P3, case a/b).

    Prefer two DIFFERENT Family lines where the enabled pool allows; when the
    pool holds only one family (or every different-family row is cooling), the
    degraded rule applies AT SELECTION TIME: two fresh same-family sessions plus
    the recorded reason `PAIR_SINGLE_FAMILY`. Pure — this selects, it never
    launches (see IF-044/IF-045). Returns a `PlannerPair`.

    The first hat routes by the ordinary policy (enable-list order, cooldowns,
    tier-up-never-down); the second hat routes prefer-different against the
    first's family. If the second lands a different family it is the happy path
    (`PAIR_TWO_FAMILY`, not degraded); if it can only land the same family it is
    the pool-degraded pair. Both sessions are distinct objects even when they
    share a `model_id` — freshness is object identity, not id difference.

    Implements: SR-155, LLR-072
    """
    cooldowns = cooldowns or {}
    first_id, first_reason = select(
        enabled,
        registry,
        tier,
        now=now,
        cooldowns=cooldowns,
        preferred_ids=preferred_ids,
    )
    if first_id is None:
        return PlannerPair((None, None), PAIR_NO_MODEL, True, first_reason)
    a = _session(hats[0], first_id, registry, tier)

    second_id, second_reason = select(
        enabled,
        registry,
        tier,
        now=now,
        cooldowns=cooldowns,
        exclude_families=[a.family],
        prefer_different=True,
        preferred_ids=preferred_ids,
    )
    if second_id is None:
        # Nothing at all for the second hat (all cooled): degrade to a second
        # fresh same-family session — fresh context is the invariant.
        b = _session(hats[1], first_id, registry, tier)
        detail = "single-family pool (second hat exhausted): {} + a fresh same-family {}".format(
            a.model_id, b.model_id
        )
        return PlannerPair((a, b), PAIR_SINGLE_FAMILY, True, detail)
    b = _session(hats[1], second_id, registry, tier)
    if b.family != a.family:
        detail = "two families: {} [{}] + {} [{}]".format(
            a.model_id, a.family, b.model_id, b.family
        )
        return PlannerPair((a, b), PAIR_TWO_FAMILY, False, detail)
    detail = "single-family pool: {} + a fresh same-family {} ({})".format(
        a.model_id, b.model_id, second_reason
    )
    return PlannerPair((a, b), PAIR_SINGLE_FAMILY, True, detail)


def planner_fallback(
    failed,
    enabled,
    registry,
    tier,
    now=0.0,
    cooldowns=None,
    preferred_ids=(),
    hats=("A", "B"),
):
    """The runtime-nonresponse fallback (DP-001 plan P3, case c) — the entry the
    coordinator calls when a routed family proves NONRESPONSIVE at launch, AFTER
    `failure_action()`'s retry policy is exhausted.

    `failed` is the typed session outcome for the dead hat (a `PlannerSession`,
    or any object exposing a `.family`); its family is the one that went dark.
    We route the RESPONDING family — the pool excluding the failed family — and
    return two FRESH same-family sessions from it, recording the degraded-
    availability reason `PAIR_RUNTIME_FALLBACK`. The returned sessions are NEW
    objects: neither is the `failed` object reused, and the two are distinct from
    each other (fresh context is the invariant). Pure — it selects, the
    coordinator relaunches (IF-044/IF-045).

    When no non-failed family is routable either, returns a `PAIR_NO_RESPONDER`
    pair with `(None, None)` for the coordinator to page on.

    Implements: SR-155, LLR-072
    """
    cooldowns = cooldowns or {}
    failed_family = getattr(failed, "family", "") or ""
    # HARD-exclude the nonresponsive family: it went dark at launch, so it is off
    # the pool entirely this round (select()'s exclude_families only DEPRIORITIZES
    # a family — it would still degrade back to it, which is exactly wrong here).
    responding = [
        e
        for e in enabled
        if (m := _row_of(registry, e)) is not None and m.family != failed_family
    ]
    resp_id, resp_reason = select(
        responding,
        registry,
        tier,
        now=now,
        cooldowns=cooldowns,
        preferred_ids=preferred_ids,
    )
    if resp_id is None:
        detail = "no responding family after {} went nonresponsive ({})".format(
            failed_family or "the failed hat", resp_reason
        )
        return PlannerPair((None, None), PAIR_NO_RESPONDER, True, detail)
    # Two FRESH same-family sessions from the responding family (distinct objects,
    # neither is `failed`). Family diversity is off the table this round — the
    # other family is dark — so this is a recorded degraded-availability pair.
    a = _session(hats[0], resp_id, registry, tier)
    b = _session(hats[1], resp_id, registry, tier)
    detail = (
        "{} nonresponsive at launch -> two fresh {} [{}] sessions "
        "(degraded availability)".format(
            failed_family or "the failed hat", resp_id, a.family
        )
    )
    return PlannerPair((a, b), PAIR_RUNTIME_FALLBACK, True, detail)


def _print_pool(raw_enabled, enabled, registry):
    """`--list`: the enabled pool, one entry per line, then each unverified
    account's line (printed, never refused; WI-798).

    Implements: SR-222, LLR-336
    """
    if not raw_enabled:
        print("(no enable-list — routing off; today's AGENT_CMD/AGENT_MODEL behavior)")
    for entry in enabled:
        m = registry[entry_route(entry)]
        print("{:40} {:7} {}".format(entry, m.tier, m.family))
    for line in unverified_lines(registry, enabled):
        print("agent_route: {}".format(line))


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description="Inspect the model registry + enable-list and the routed "
        "selection (the coordinator uses these functions in-process).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--registry",
        default="docs/agents.toml",
        help="the model registry (either carrier)",
    )
    ap.add_argument(
        "--enabled", default="docs/agents-enabled", help="the ordered enable-list"
    )
    ap.add_argument(
        "--list", action="store_true", help="print the enabled pool and exit"
    )
    ap.add_argument(
        "--select", action="store_true", help="print the routed selection for --tier"
    )
    ap.add_argument("--tier", default="strong", choices=list(TIER_ORDER))
    ap.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="a family to prefer against (repeatable); implies --prefer-different",
    )
    args = ap.parse_args(argv)

    registry, errors = load_registry(args.registry)
    for e in errors:
        print("agent_route: {}".format(e), file=sys.stderr)
    tag_rank = load_tag_rank(args.registry)
    try:
        raw_enabled = load_enabled(args.enabled)
    except EnabledUnreadable as exc:
        print("agent_route: agents-enabled: {}".format(exc), file=sys.stderr)
        return 1
    # Resolve version-less tokens to concrete ids (exact-id/newest-in-line).
    enabled, enable_errors = resolve_enabled(raw_enabled, registry, tag_rank)
    for e in enable_errors:
        print("agent_route: agents-enabled: {}".format(e), file=sys.stderr)

    if args.list:
        _print_pool(raw_enabled, enabled, registry)
        return 1 if (errors or enable_errors) else 0

    if args.select:
        chosen, reason = select(
            enabled,
            registry,
            args.tier,
            exclude_families=args.exclude,
            prefer_different=bool(args.exclude),
        )
        print(reason)
        return 0 if chosen else 1

    # Default: a terse status line.
    print(
        "registry={} models, enabled={} (routing {})".format(
            len(registry), len(enabled), "on" if raw_enabled else "off"
        )
    )
    return 1 if (errors or enable_errors) else 0


if __name__ == "__main__":
    sys.exit(main())
