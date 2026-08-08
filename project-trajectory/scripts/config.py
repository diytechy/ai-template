#!/usr/bin/env python3
"""The one editable authority for how a repo BEHAVES — `docs/config.toml`.

Stack-agnostic, standard-library only. Before this module every behaviour dial
lived in its own one-word file under `docs/` (`docs/push-policy`,
`docs/blackout`, `docs/okf-export`, …), each with a private
first-non-comment-line parse and its own idea of what an absent file meant.
Seventeen of them accumulated: nothing could enumerate the set, a typo in any of
them read as "absent" — which nearly always meant OFF — and an adopter could not
answer "what is this repo configured to do?" without grepping the scripts.

This module replaces that with ONE declared table, `SCHEMA`, and one strict
loader (contracts: `docs/mechanized-loop-contracts.md` §1). The design
commitments, and what each one refuses:

  - **The schema is DATA, not code branches.** One row per dial carries its
    dotted path, its type token, its default, its allowed values and its
    documentation string. The validator walks those rows; so does the
    documentation generator that renders `config.toml.template`
    (`config_migrate.render_template`). A dial absent from the table does not
    exist — which is precisely why an unknown key is a refusal and not a shrug.
  - **A finding names the offending key, and a run reports all of them.**
    `load_config` returns `(Config, [Finding])` instead of raising on the first
    problem, so an adopter fixing a config learns every mistake in one pass. A
    non-empty list means the CALLER refuses; the `Config` is still returned so
    the caller can print and exit rather than crash.
  - **Absent is not a finding — absent is the declared default.** An absent file
    and an absent key resolve identically, through the one table. A default
    living in a reader rather than in the schema is invisible to the adopter;
    this refuses to keep one.
  - **Values are read as typed attributes** (`cfg.policy.review_rounds`), never
    by dict-walking at a call site. A mistyped attribute raises here, naming the
    section, instead of yielding `None` three modules away.
  - **Two live sources for one behaviour is a refusal, never a precedence
    rule.** `mixed_source_findings` watches the retired declared-policy files
    beside the schema, so a newly migrated key cannot be forgotten there. A
    precedence rule would hide the divergence — the adopter reads one file and
    the loop obeys the other — rather than end it.

This module changes NO existing runtime reader: `agent_common.read_declared` and
every current caller keep working byte-for-byte until the cutover. What exists
here is the authority — declared, validated, and provably in agreement with the
files it will replace.
"""

import collections
import re
import tomllib
from pathlib import Path

# The document this module owns, as a repo-relative POSIX string for messages
# (joined with `/` parts for the filesystem, so no separator is assumed).
CONFIG_REL = "docs/config.toml"
CONFIG_PARTS = ("docs", "config.toml")

# The document formats this loader understands. An unsupported value is a
# refusal rather than a best-effort read: a schema bump exists exactly so that
# an old reader stops instead of silently misinterpreting a new document.
SUPPORTED_SCHEMAS = (1,)
SCHEMA_VERSION = SUPPORTED_SCHEMAS[-1]


class _Required:
    """Sentinel default meaning "the adopter must supply this" (route ids,
    prompt templates). Distinct from `None`, which is a legal absent value."""

    def __repr__(self):
        return "REQUIRED"


REQUIRED = _Required()


# One schema row. `type` is a token, not a Python type object, so the table
# stays printable: the documentation generator renders these rows verbatim.
#   bool | int | float | str | str[] | str{} | pool
# `choices` is a tuple of allowed values, `rng` an inclusive `(lo, hi)` with
# `None` for unbounded, `pattern` a full-match regex. All three are printable,
# which is why they are data instead of a per-key validate() callable.
Key = collections.namedtuple(
    "Key", "path type default choices rng pattern doc", defaults=(None, None, None, "")
)

# A validation refusal: the dotted path of the offending key and why it was
# refused. `key` is a path a reader can search for — `policy.review_rounds`,
# `routes[2].strength` — never a bare boolean or a line number.
Finding = collections.namedtuple("Finding", "key reason")


# --- the declared dials -------------------------------------------------------
# Every key of contracts §1, in the section order the document uses. Editing
# this table is the ONLY way to add a dial: the loader, the query entry point,
# the template renderer and the converter all read it.
SCHEMA = (
    Key(
        "attestation.human_ratification_through",
        "int",
        1,
        rng=(0, 3),
        doc="Inclusive human checkpoints: 0=SN; 1=SN+SR; 2=SN+SR+LLR; "
        "3=SN+SR+LLR+TC. At or below the boundary a ratification needs a human "
        "decision; above it an adjudicator may enact.",
    ),
    Key(
        "attestation.final_full_spine_review",
        "str",
        "never",
        choices=("never", "always"),
        doc="Persistent policy for a whole-spine human review at stage 4. A "
        "one-off ask is a review-request event, not a config edit.",
    ),
    Key(
        "automation.lanes",
        "int",
        1,
        rng=(1, None),
        doc="The dispatcher's worker-lane ceiling. 1 is serial.",
    ),
    Key(
        "automation.session_timeout_seconds",
        "int",
        7200,
        rng=(1, None),
        doc="Wall-clock ceiling for one worker session.",
    ),
    Key(
        "automation.blackout",
        "str",
        "",
        pattern=r"(\d{2}:\d{2}-\d{2}:\d{2})?",
        doc='UTC Mon-Fri window "HH:MM-HH:MM" the coordinator starts no new '
        'session inside; "" disables it.',
    ),
    Key(
        "policy.push",
        "str",
        "human",
        choices=("human", "agent-iteration", "agent"),
        doc="Who may publish this repo: human (an agent never pushes), "
        "agent-iteration (the scrubbed iteration branch only), or agent.",
    ),
    Key(
        "policy.privacy_check",
        "bool",
        False,
        doc="Run the privacy gate: author identity and committed content are "
        "scanned for PII / identity leak classes.",
    ),
    Key(
        "policy.secrets_scan",
        "bool",
        True,
        doc="The always-on secrets floor: private-key headers and key/token "
        "shapes block a commit and a push.",
    ),
    Key(
        "policy.privacy_review",
        "str",
        "require",
        choices=("require", "warn-unwired"),
        doc="Whether an unwired reviewer command blocks a push (require) or "
        "warns and proceeds (warn-unwired). Read today by pre-push only.",
    ),
    Key(
        "policy.review_rounds",
        "int",
        1,
        choices=(0, 1, 2),
        doc="Independent fresh-context review verdicts a completed work item "
        "gets before the integrator accepts it.",
    ),
    Key(
        "policy.guardrails",
        "str",
        "off",
        doc="Which sessions get the vendored guardrails core prepended: off, "
        "all, `all except <sub>`, or a model-substring allowlist.",
    ),
    Key(
        "policy.subagent_gate",
        "str",
        "off",
        choices=("off", "ask", "deny"),
        doc="What happens when a session tries to spawn a subagent.",
    ),
    Key(
        "policy.live_status",
        "bool",
        False,
        doc="Redraw the session status line in place instead of appending to "
        "the scroll (honoured only on a TTY).",
    ),
    Key(
        "policy.status_lint",
        "int",
        120,
        rng=(0, None),
        doc="Line budget for docs/status.md; 0 disables the lint.",
    ),
    Key(
        "policy.trajectory_check",
        "bool",
        True,
        doc="Run the status.md <-> work-item registry coherence check.",
    ),
    Key(
        "policy.interfaces_check",
        "bool",
        True,
        doc="Run the declared-interface coverage check.",
    ),
    Key(
        "policy.components_check",
        "bool",
        True,
        doc="Run the component-registry coverage check.",
    ),
    Key(
        "policy.okf_export",
        "bool",
        True,
        doc="Generate and freshness-check the docs/okf/ knowledge bundle.",
    ),
    Key(
        "harness.src",
        "str",
        "src",
        doc="Product source root. Mirrors docs/stack.ini [paths] src; stack.ini "
        "stays the live source until the cutover and the two are proved equal "
        "by the parity tests.",
    ),
    Key(
        "harness.tests",
        "str",
        "tests",
        doc="Test root. Mirrors docs/stack.ini [paths] tests (see harness.src).",
    ),
    Key(
        "outcomes.complete_sampling_rate",
        "float",
        0.0,
        rng=(0.0, 1.0),
        doc="Fraction of Complete outcomes that draw a dedicated adjudicator "
        "even with no risk trigger.",
    ),
    Key(
        "outcomes.risk_safety_classes",
        "str[]",
        ("spine", "gate", "attestation", "high-risk", "adjudication"),
        doc="Safety classes whose Complete outcome always adjudicates.",
    ),
    Key(
        "admission.max_batch_size",
        "int",
        0,
        rng=(0, None),
        doc="Optional throttle on one admission batch; 0 disables it. Never "
        "the independence criterion.",
    ),
    # Default FALSE deliberately, though contracts §1's sample document shows a
    # filled `true`: docs/agents-enabled carried consent by PRESENCE, so the
    # only faithful successor is an explicit opt-in. A default of true would
    # turn managed routing on for every repo that never asked for it, which is
    # the one property D-5 says the conversion must preserve.
    Key(
        "routing.enabled",
        "bool",
        False,
        doc="Managed model routing. The explicit successor of the consent "
        "property docs/agents-enabled carried by mere presence, so it is "
        "opt-in: routing is off until this says otherwise.",
    ),
)

# Every dial's default in one place — the projection of the ONE table above, so
# an absent file and an absent key cannot resolve differently (LLR-156). The
# array-valued tables (routes/jobs/prompts) default to empty and live on the
# Config, not here: they have no scalar default to state.
DEFAULTS = {k.path: k.default for k in SCHEMA}

# Section order, derived from the table rather than restated.
SECTIONS = tuple(dict.fromkeys(k.path.split(".", 1)[0] for k in SCHEMA))

# The declared roles a model is drawn for, and the reviewed prompt templates.
# Both are closed vocabularies: an undeclared job or prompt name is a finding,
# because a typo'd `[jobs.reviewr]` would otherwise silently never be drawn.
JOBS = ("planner", "critic", "arbiter", "implementer", "reviewer", "adjudicator")
PROMPTS = JOBS + (
    "adjudicate-amendment",
    "adjudicate-disposition",
    "adjudicate-conflict",
    "adjudicate-red-test",
)

ROUTE_FIELDS = (
    Key("id", "str", REQUIRED, doc="Stable route id, e.g. ANTHROPIC-OPUS-STRONG."),
    Key("family", "str", REQUIRED, doc="Provider family; drives cross-family draws."),
    Key("model", "str", REQUIRED, doc="Model slug substituted into {model}."),
    Key("strength", "int", 2, rng=(1, 3), doc="1=quick 2=medium 3=strong."),
    Key("argv", "str[]", (), doc="Invocation argv; {model} is substituted."),
    Key("env", "str{}", {}, doc="Environment merged over the inherited one."),
    Key("capabilities", "str[]", (), doc="What this route may be drawn for."),
    Key("notes", "str", "", doc="Failure-context hint echoed at preflight."),
)

POOL_FIELDS = (
    Key("route", "str", REQUIRED, doc="A declared route id."),
    Key("weight", "int", 1, rng=(0, None), doc="Draw weight; 0 = fallback-only."),
)

JOB_FIELDS = (
    Key("minimum_strength", "int", 1, rng=(1, 3), doc="Weakest drawable route."),
    Key("fallback", "str", "same-or-higher", doc="What to draw when the pool is out."),
    Key("prefer_cross_family", "bool", False, doc="Prefer a different family."),
    Key("pool", "pool", (), doc="Weighted route entries: {route=..., weight=...}."),
)

PROMPT_FIELDS = (
    Key("template", "str", REQUIRED, doc="Repo-relative Markdown template path."),
    Key("required_slots", "str[]", (), doc="Slots the render must fill."),
    Key("allowed_sources", "str[]", (), doc="Evidence sources the prompt may cite."),
    Key("prohibited_sources", "str[]", (), doc="Sources it may never cite."),
    Key("output_schema", "str", REQUIRED, doc="Declared output contract name."),
)


# --- the retired sources ------------------------------------------------------
# Where each canonical key USED to live. Declared beside the schema (LLR-157) so
# a newly migrated dial cannot be added above and forgotten here — which is the
# one way the mixed-source refusal could quietly stop covering a key.
#
# `section`/`key` are set only for the one retired source that is a SECTION of a
# surviving file rather than a file of its own: docs/stack.ini keeps living (it
# is the declared toolchain), so its mere presence proves nothing — the pair is
# live only when that section actually declares the dial.
#
# Deliberately NOT here: docs/stack.ini's [paths], mirrored by harness.src /
# harness.tests. That mirror is a declared parity, not a divergence — stack.ini
# stays the live source until the cutover and the parity tests hold the two
# equal, so refusing on it would refuse the transition itself.
LegacySource = collections.namedtuple("LegacySource", "path section key")

LEGACY_SOURCES = {
    "attestation.human_ratification_through": LegacySource(
        "docs/gate-policy", None, None
    ),
    "automation.blackout": LegacySource("docs/blackout", None, None),
    "automation.lanes": LegacySource("docs/stack.ini", "agent-loop", "lanes"),
    "policy.push": LegacySource("docs/push-policy", None, None),
    "policy.privacy_check": LegacySource("docs/privacy-check", None, None),
    "policy.privacy_review": LegacySource("docs/privacy-review", None, None),
    "policy.secrets_scan": LegacySource("docs/secrets-scan", None, None),
    "policy.review_rounds": LegacySource("docs/review-policy", None, None),
    "policy.guardrails": LegacySource("docs/guardrails-policy", None, None),
    "policy.subagent_gate": LegacySource("docs/subagent-gate", None, None),
    "policy.live_status": LegacySource("docs/live-status", None, None),
    "policy.status_lint": LegacySource("docs/status-lint", None, None),
    "policy.trajectory_check": LegacySource("docs/trajectory-check", None, None),
    "policy.interfaces_check": LegacySource("docs/interfaces-check", None, None),
    "policy.components_check": LegacySource("docs/components-check", None, None),
    "policy.okf_export": LegacySource("docs/okf-export", None, None),
    "routes": LegacySource("docs/agents.csv", None, None),
    "routing.enabled": LegacySource("docs/agents-enabled", None, None),
}


# --- typed access -------------------------------------------------------------
class Section:
    """One config table read as attributes.

    Read-only on purpose: a config that a caller can mutate is a second source
    of truth with no file behind it. An undeclared attribute raises naming the
    section, so `cfg.policy.review_round` fails HERE rather than returning None
    three modules downstream.
    """

    __slots__ = ("_name", "_values")

    def __init__(self, name, values):
        object.__setattr__(self, "_name", name)
        object.__setattr__(self, "_values", dict(values))

    def __getattr__(self, attr):
        try:
            return object.__getattribute__(self, "_values")[attr]
        except KeyError:
            raise AttributeError(
                "config: {}.{} is not a declared key".format(self._name, attr)
            ) from None

    def __setattr__(self, attr, value):
        raise AttributeError("config: {} is read-only".format(self._name))

    def __contains__(self, attr):
        return attr in self._values

    def __repr__(self):
        return "Section({!r}, {!r})".format(self._name, self._values)


class Config:
    """The typed model of one `docs/config.toml`.

    Sections are attributes (`cfg.policy.push`); `routes` is an ordered tuple,
    `jobs` and `prompts` are name-keyed dicts, each entry a `Section`. `get`
    exists for the one caller that legitimately holds a dotted path as data —
    the query entry point the shell hooks use — not as a dict-walking escape
    hatch for ordinary call sites.
    """

    __slots__ = ("schema", "routes", "jobs", "prompts", "path", "_values") + SECTIONS

    def __init__(
        self, values, routes=(), jobs=None, prompts=None, schema=None, path=None
    ):
        object.__setattr__(self, "_values", dict(values))
        object.__setattr__(self, "schema", SCHEMA_VERSION if schema is None else schema)
        object.__setattr__(self, "routes", tuple(routes))
        object.__setattr__(self, "jobs", dict(jobs or {}))
        object.__setattr__(self, "prompts", dict(prompts or {}))
        object.__setattr__(self, "path", path)
        for section in SECTIONS:
            prefix = section + "."
            object.__setattr__(
                self,
                section,
                Section(
                    section,
                    {
                        p[len(prefix) :]: v
                        for p, v in self._values.items()
                        if p.startswith(prefix)
                    },
                ),
            )

    def __setattr__(self, attr, value):
        raise AttributeError("config: Config is read-only")

    def get(self, dotted):
        """The resolved value of one declared dotted key. `KeyError` — naming
        the key — when it is not in the schema."""
        try:
            return self._values[dotted]
        except KeyError:
            raise KeyError(dotted) from None

    def as_dict(self):
        """A copy of the resolved scalar dials, for reporting and tests. Not a
        call-site accessor: production reads go through the attributes."""
        return dict(self._values)

    def __repr__(self):
        return "Config(schema={}, path={!r}, dials={})".format(
            self.schema, str(self.path) if self.path else None, len(self._values)
        )


# --- validation ---------------------------------------------------------------
def _type_reason(token, value):
    """Why `value` does not match the declared type token, or None.

    `bool` is matched by identity rather than `isinstance`: in Python `True` IS
    an `int`, so an isinstance check would quietly accept `lanes = true`.
    """
    if token == "bool":
        return None if value is True or value is False else "expected a boolean"
    if token == "int":
        if value is True or value is False or not isinstance(value, int):
            return "expected an integer"
        return None
    if token == "float":
        # A TOML `0` is an int and a TOML `0.0` is a float; both are honest ways
        # to write a rate, so an int is accepted and coerced at read time.
        if value is True or value is False or not isinstance(value, (int, float)):
            return "expected a number"
        return None
    if token == "str":
        return None if isinstance(value, str) else "expected a string"
    if token == "str[]":
        if not isinstance(value, list) or any(not isinstance(x, str) for x in value):
            return "expected an array of strings"
        return None
    if token == "str{}":
        if not isinstance(value, dict) or any(
            not isinstance(k, str) or not isinstance(v, str) for k, v in value.items()
        ):
            return "expected a table of string values"
        return None
    if token == "pool":
        return None if isinstance(value, list) else "expected an array of tables"
    return "unknown type token {!r}".format(token)


def _coerce(token, value):
    """The stored form of an accepted value: floats normalized, arrays and
    tables copied so a caller cannot mutate the loaded document."""
    if token == "float":
        return float(value)
    if token == "str[]":
        return tuple(value)
    if token == "str{}":
        return dict(value)
    return value


def _constraint_reason(spec, value):
    """Why an accepted-type `value` is out of the declared range, choice set or
    pattern, or None."""
    if spec.choices is not None and value not in spec.choices:
        return "expected one of {}".format("|".join(str(c) for c in spec.choices))
    if spec.rng is not None:
        lo, hi = spec.rng
        if lo is not None and value < lo:
            return "expected >= {}".format(lo)
        if hi is not None and value > hi:
            return "expected <= {}".format(hi)
    if spec.pattern is not None and not re.fullmatch(spec.pattern, value):
        return "expected to match {}".format(spec.pattern)
    return None


def _check_scalar(path, spec, value, findings):
    """Validate one scalar against its schema row; append at most one finding
    and return the value to store (the default when it was refused)."""
    reason = _type_reason(spec.type, value)
    if reason is None:
        reason = _constraint_reason(spec, value)
    if reason is not None:
        findings.append(Finding(path, "{}, got {!r}".format(reason, value)))
        return spec.default
    return _coerce(spec.type, value)


def _check_table(label, fields, table, findings):
    """Validate one declared sub-table (a route, a job, a prompt, a pool entry)
    against its field list. Returns a `Section`; unknown fields, wrong types and
    missing required fields are each their own finding, so one malformed route
    reports everything wrong with it in a single run."""
    by_name = {f.path: f for f in fields}
    values = {}
    for name, value in table.items():
        spec = by_name.get(name)
        if spec is None:
            findings.append(
                Finding("{}.{}".format(label, name), "unknown key for this table")
            )
            continue
        if spec.type == "pool":
            values[name] = _check_pool("{}.{}".format(label, name), value, findings)
            continue
        values[name] = _check_scalar("{}.{}".format(label, name), spec, value, findings)
    for spec in fields:
        if spec.path in values:
            continue
        if spec.default is REQUIRED:
            findings.append(
                Finding("{}.{}".format(label, spec.path), "required key is missing")
            )
            values[spec.path] = None
        else:
            values[spec.path] = _coerce(spec.type, spec.default)
    return Section(label, values)


def _check_pool(label, value, findings):
    """A job's weighted route pool: an array of `{route, weight}` tables."""
    reason = _type_reason("pool", value)
    if reason is not None:
        findings.append(Finding(label, "{}, got {!r}".format(reason, value)))
        return ()
    entries = []
    for n, item in enumerate(value):
        if not isinstance(item, dict):
            findings.append(
                Finding(
                    "{}[{}]".format(label, n), "expected a table, got {!r}".format(item)
                )
            )
            continue
        entries.append(
            _check_table("{}[{}]".format(label, n), POOL_FIELDS, item, findings)
        )
    return tuple(entries)


def _check_named_tables(label, declared, fields, table, findings):
    """`[jobs.*]` / `[prompts.*]`: a closed name vocabulary whose entries share
    one field list. An undeclared name is a finding — a typo'd role would
    otherwise sit in the file looking configured and never be drawn."""
    if not isinstance(table, dict):
        findings.append(Finding(label, "expected a table, got {!r}".format(table)))
        return {}
    out = {}
    for name, entry in table.items():
        path = "{}.{}".format(label, name)
        if name not in declared:
            findings.append(
                Finding(
                    path,
                    "undeclared name; expected one of {}".format("|".join(declared)),
                )
            )
            continue
        if not isinstance(entry, dict):
            findings.append(Finding(path, "expected a table, got {!r}".format(entry)))
            continue
        out[name] = _check_table(path, fields, entry, findings)
    return out


def _check_routes(value, findings):
    if not isinstance(value, list):
        findings.append(Finding("routes", "expected an array of tables"))
        return ()
    routes = []
    for n, entry in enumerate(value):
        label = "routes[{}]".format(n)
        if not isinstance(entry, dict):
            findings.append(Finding(label, "expected a table, got {!r}".format(entry)))
            continue
        routes.append(_check_table(label, ROUTE_FIELDS, entry, findings))
    return tuple(routes)


def validate(document, path=None):
    """`(Config, [Finding])` for an already-parsed TOML mapping.

    Split out from `load_config` so the converter can prove its own output
    loads clean without writing a file first.
    """
    findings = []
    values = dict(DEFAULTS)
    by_path = {k.path: k for k in SCHEMA}

    schema = document.get("schema")
    if schema is None:
        findings.append(
            Finding(
                "schema",
                "the document does not declare `schema`; a reader cannot know "
                "which rules apply to it",
            )
        )
        schema = SCHEMA_VERSION
    elif _type_reason("int", schema) is not None or schema not in SUPPORTED_SCHEMAS:
        findings.append(
            Finding(
                "schema",
                "unsupported schema version {!r}; this reader understands {}".format(
                    schema, "|".join(str(s) for s in SUPPORTED_SCHEMAS)
                ),
            )
        )

    routes, jobs, prompts = (), {}, {}
    for name, value in document.items():
        if name == "schema":
            continue
        if name == "routes":
            routes = _check_routes(value, findings)
            continue
        if name == "jobs":
            jobs = _check_named_tables("jobs", JOBS, JOB_FIELDS, value, findings)
            continue
        if name == "prompts":
            prompts = _check_named_tables(
                "prompts", PROMPTS, PROMPT_FIELDS, value, findings
            )
            continue
        if name not in SECTIONS:
            findings.append(Finding(name, "unknown section"))
            continue
        if not isinstance(value, dict):
            findings.append(Finding(name, "expected a table, got {!r}".format(value)))
            continue
        for leaf, raw in value.items():
            dotted = "{}.{}".format(name, leaf)
            spec = by_path.get(dotted)
            if spec is None:
                findings.append(Finding(dotted, "unknown key"))
                continue
            values[dotted] = _check_scalar(dotted, spec, raw, findings)

    return (
        Config(
            values, routes=routes, jobs=jobs, prompts=prompts, schema=schema, path=path
        ),
        findings,
    )


def config_path(root):
    """`<root>/docs/config.toml` as a Path, built from parts so no separator is
    assumed."""
    return Path(root).joinpath(*CONFIG_PARTS)


def load_config(root):
    """`(Config, [Finding])` for the repo at `root`.

    An absent file is NOT a finding: it yields the declared defaults, which is
    what makes adopting the kit a no-op until an adopter has an opinion. Every
    other problem — unreadable bytes, malformed TOML, an unknown key, a wrong
    type, an out-of-range value, an unsupported schema — is a finding naming
    the key, and the caller refuses on a non-empty list.
    """
    path = config_path(root)
    if not path.is_file():
        return Config(dict(DEFAULTS)), []
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return (
            Config(dict(DEFAULTS), path=path),
            [Finding(CONFIG_REL, "cannot be read: {}".format(exc))],
        )
    try:
        # utf-8-sig: an editor-written BOM must not become part of the first key
        # name (the kit's declared-reader idiom).
        document = tomllib.loads(raw.decode("utf-8-sig"))
    except (UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        return (
            Config(dict(DEFAULTS), path=path),
            [Finding(CONFIG_REL, "is not valid TOML: {}".format(exc))],
        )
    return validate(document, path=path)


# --- mixed-source detection ---------------------------------------------------
def _ini_section_keys(path, section):
    """The key names declared in one `[section]` of an INI-ish file.

    Ten lines rather than `configparser` because the answer needed is "which
    names appear", and configparser's `%` interpolation would raise on the
    command templates docs/stack.ini legitimately carries. Absent or unreadable
    reads as "declares nothing" — the same fail-soft posture every declared
    reader in the kit takes.
    """
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return set()
    keys, inside = set(), False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            inside = stripped[1:-1].strip() == section
            continue
        if not inside or not stripped or stripped.startswith(("#", ";")):
            continue
        name, sep, _ = stripped.partition("=")
        if sep:
            keys.add(name.strip())
    return keys


def explicit_keys(root):
    """The dotted paths a repo's `docs/config.toml` actually SETS.

    Distinct from the resolved values: a key left to its default is not a
    second source of truth, so it can never conflict with a surviving legacy
    file. A malformed or absent document sets nothing.
    """
    path = config_path(root)
    if not path.is_file():
        return set()
    try:
        document = tomllib.loads(path.read_bytes().decode("utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return set()
    present = set()
    for name, value in document.items():
        if name in ("routes", "jobs", "prompts"):
            present.add(name)
            continue
        if isinstance(value, dict):
            present.update("{}.{}".format(name, leaf) for leaf in value)
    return present


def mixed_source_findings(root):
    """One finding per canonical key whose retired declared-policy source is
    still present AND whose canonical key is set (SR-138).

    A precedence rule was the obvious alternative and is the wrong one: it
    resolves the ambiguity silently, so the adopter reads one file while the
    loop obeys the other. Refusing converts a permanent silent divergence into
    a one-time migration step — delete the retired file, or unset the key.
    """
    root = Path(root)
    present = explicit_keys(root)
    findings = []
    for key in sorted(LEGACY_SOURCES):
        if key not in present:
            continue
        legacy = LEGACY_SOURCES[key]
        path = root.joinpath(*legacy.path.split("/"))
        if not path.is_file():
            continue
        if legacy.section is not None:
            if legacy.key not in _ini_section_keys(path, legacy.section):
                continue
            where = "{} [{}] {}".format(legacy.path, legacy.section, legacy.key)
        else:
            where = legacy.path
        findings.append(
            Finding(
                key,
                "is set in {} while its retired source {} is still live; delete "
                "the retired source or unset the key".format(CONFIG_REL, where),
            )
        )
    return findings


def refusal_lines(findings, module="config"):
    """The printable refusal for each finding, in the kit's one refusal shape:
    `<module>: REFUSED - <what> (<why>)`. Every finding is printed, never the
    first — a caller fixing a config learns all of it in one run."""
    return ["{}: REFUSED - {} ({})".format(module, f.key, f.reason) for f in findings]
