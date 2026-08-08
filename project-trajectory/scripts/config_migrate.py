#!/usr/bin/env python3
"""Convert the retired one-word policy files into `docs/config.toml`.

Stack-agnostic, standard-library only. Seventeen declared-policy files are
retired by the single configuration authority (contracts §1). An adopter must
not have to hand-translate them — and, more importantly, must not be *silently*
translated: the retired gate-authority values do not map one-for-one onto the
numeric ratification boundary, and a converter that guessed would move a repo to
a policy nobody chose. That is worse than an explicit question, because the
adopter would never learn a question had been answered.

So this module is built around two tables and one refusal:

  - **`LEGACY_MAP` is data.** One row per retired source: where it lived, which
    canonical key it becomes, how to read it, and how to coerce its one word.
    Because the mapping is a table, the set of things it CANNOT map is derivable
    rather than remembered — every row with no canonical key, and every value in
    `AMBIGUOUS`, lands in the report by construction.
  - **`AMBIGUOUS` names the values that carry more meaning than the target key
    can hold**, with their candidate targets. `attended` maps cleanly (a human
    ratifies every tier, so the boundary is 3); `single-ratify` also encoded a
    *cadence* — LLM review through G1+G2, one human ratification at the phase
    close — and `autonomous` permitted no early human checkpoint at all.
    Neither is a boundary number. They are reported by name with their
    candidates and left UNWRITTEN.
  - **A read-only run is the default.** `convert(root)` reports without touching
    the tree; writing is an explicit act, and it never overwrites an existing
    `docs/config.toml` (SR-141 — the adopter owns that file).

The same renderer produces the shipped blank form: `render_template()` walks
`config.SCHEMA` and emits every dial as a COMMENTED line carrying its default
and its documentation string. Commented, not set, for a reason a fresh scaffold
would otherwise discover the hard way — bootstrap still scaffolds the retired
files, so a template that SET every key would make every new repo mixed-source
on day one. A blank form declares the schema version and nothing else.

Usage:
    python scripts/config_migrate.py [--root .]            # report only
    python scripts/config_migrate.py --root . --write      # write if absent
    python scripts/config_migrate.py --template            # print the blank form
"""

import argparse
import collections
import csv
import json
import re
import sys
import textwrap
from pathlib import Path

# Deferred sibling import (contracts §6): resolved inside the functions that
# need it so an in-process caller whose sys.path lacks scripts/ still works.


COMMENT_WIDTH = 76

# One retired source. `reader` is a token, not a callable, so the table stays
# printable and a reader can audit the whole migration at a glance:
#   line             the first non-comment line of a one-word declared file
#   ini:<sec>:<key>  one key of one section of docs/stack.ini
#   agents-csv       the model registry -> [[routes]]
#   agents-enabled   the consent surface -> [routing] + the per-job pools
# `coerce` is likewise a token; see `_coerce`.
Legacy = collections.namedtuple("Legacy", "source key reader coerce")

LEGACY_MAP = (
    Legacy(
        "docs/gate-policy", "attestation.human_ratification_through", "line", "gate"
    ),
    Legacy("docs/push-policy", "policy.push", "line", "word"),
    Legacy("docs/review-policy", "policy.review_rounds", "line", "int"),
    Legacy("docs/privacy-check", "policy.privacy_check", "line", "true-exact"),
    Legacy("docs/secrets-scan", "policy.secrets_scan", "line", "off-no"),
    Legacy("docs/privacy-review", "policy.privacy_review", "line", "word-or-require"),
    Legacy("docs/guardrails-policy", "policy.guardrails", "line", "line-or-off"),
    Legacy("docs/blackout", "automation.blackout", "line", "word"),
    Legacy("docs/live-status", "policy.live_status", "line", "true-fold"),
    Legacy("docs/subagent-gate", "policy.subagent_gate", "line", "word-or-off"),
    Legacy("docs/status-lint", "policy.status_lint", "line", "int-or-off"),
    Legacy("docs/trajectory-check", "policy.trajectory_check", "line", "off-no"),
    Legacy("docs/interfaces-check", "policy.interfaces_check", "line", "off-no"),
    Legacy("docs/components-check", "policy.components_check", "line", "off-no"),
    Legacy("docs/okf-export", "policy.okf_export", "line", "off-no"),
    # Named by contracts §1 as retired, but this kit ships no template for it and
    # no script reads it, so there is no canonical key to map it onto. A row with
    # `key=None` is how the table says "retired, unmappable": present it in the
    # report if a repo actually carries one, never invent a target for it.
    Legacy("docs/critique-policy", None, "line", "unmappable"),
    Legacy("docs/agents.csv", "routes", "agents-csv", "routes"),
    Legacy("docs/agents-enabled", "routing.enabled", "agents-enabled", "routing"),
    Legacy("docs/stack.ini", "automation.lanes", "ini:agent-loop:lanes", "int"),
)

# The one gate-authority value that maps losslessly: `attended` means a human
# ratifies every batch, at every tier, which IS the top of the inclusive
# boundary (0=SN … 3=SN+SR+LLR+TC).
GATE_AUTHORITY = {"attended": 3}

# What each value refuses to become, and what a human might reasonably choose
# instead. Reported verbatim; never applied.
AMBIGUOUS = {
    ("docs/gate-policy", "single-ratify"): (
        (
            "attestation.human_ratification_through = 1",
            "attestation.human_ratification_through = 2",
            'attestation.final_full_spine_review = "always"',
        ),
        "single-ratify also encoded a CADENCE (LLM-gate review through G1+G2, "
        "one human ratification at the phase's [g2] close). The boundary dial "
        "carries a tier, not a cadence, so the tier the human keeps is a choice",
    ),
    ("docs/gate-policy", "autonomous"): (
        (
            "attestation.human_ratification_through = 0",
            'attestation.final_full_spine_review = "never"',
        ),
        "autonomous permitted NO early human checkpoint, while the boundary is "
        "inclusive and its lowest value (0) still keeps stakeholder needs with "
        "the human — so there is no value that means what autonomous meant",
    ),
}

# docs/agents.csv Tier -> the numeric strength a route declares. `weak` is the
# pre-rename bottom tier and reads as quick, exactly as agent_route does.
TIER_STRENGTH = {"quick": 1, "weak": 1, "medium": 2, "strong": 3}

# The per-phase draw-weight grammar docs/agents-enabled carried (`<ID> BUILD=3`),
# and the job each phase becomes. `REVIEW` is the umbrella over both reviewer
# legs, and both legs are the same job, so it needs no expansion here.
WEIGHT_PHASES = ("BUILD", "REVIEW", "CRITIQUE", "DESIGN-CHECK")
PHASE_JOB = {"BUILD": "implementer", "REVIEW": "reviewer", "CRITIQUE": "critic"}
# DESIGN-CHECK named a run phase, not one of the six declared jobs. A repo that
# weighted it gets a report entry rather than a job picked on its behalf.
PHASE_UNMAPPED = {"DESIGN-CHECK": ("jobs.planner", "jobs.arbiter")}

_WEIGHT_INT_RE = re.compile(r"[0-9]+\Z")

# One thing the converter could not carry across, with the candidate targets a
# human should choose between. `targets` is empty when there is nothing to
# choose — the value is simply gone and the report says so.
Unmapped = collections.namedtuple("Unmapped", "source value targets why")


# --- readers (duplicated per the kit's F5 rule, never imported) ---------------
def declared_line(path):
    """The first non-empty, non-comment line of a declared-policy file, or None.

    The same rule `agent_common.read_declared`, the git hooks and check_privacy
    apply — restated here rather than imported so this converter stays a
    self-contained drop-in (F5). `tests/test_config_migrate.py` pins it equal to
    `agent_common.read_declared`'s answer over the same inputs.
    """
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return None
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None


def ini_value(path, section, key):
    """One `key = value` of one `[section]` of an INI-ish file, or None."""
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return None
    inside = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            inside = stripped[1:-1].strip() == section
            continue
        if not inside or not stripped or stripped.startswith(("#", ";")):
            continue
        name, sep, value = stripped.partition("=")
        if sep and name.strip() == key:
            return value.strip()
    return None


def _true_word(token, raw, source, key, report):
    """A retired on/off file's word -> a boolean, or None to write nothing.

    Two tokens for one idiom, split by FIDELITY rather than style: the retired
    files are parsed differently in production, so "what did this repo actually
    do?" has a different answer per file.

      true-fold   `docs/live-status`, whose ONE reader is
                  `read_declared(...).lower() == "true"`. Folding is faithful.
      true-exact  `docs/privacy-check`, whose readers DISAGREE: the three git
                  hooks test `[ "$p" = "true" ]` (exact) while `agent_loop` and
                  `agent_common` fold. For a file spelling `TRUE` the commit
                  gates were off and the loop's identity check was on, so no
                  canonical value is faithful — it is reported, never picked.
                  Picking either way would hand the repo a privacy policy nobody
                  chose, and the adopter would never learn a question was asked.
    """
    if token == "true-fold":
        return raw.lower() == "true"
    if raw != "true" and raw.lower() == "true":
        report.append(
            Unmapped(
                source,
                raw,
                ("{} = true".format(key), "{} = false".format(key)) if key else (),
                "reads ON to the loop's Python readers (which fold case) and OFF "
                'to the git hooks (which test `= "true"` exactly), so the retired '
                "sources disagree with each other and no canonical value is "
                "faithful — choose one deliberately",
            )
        )
        return None
    return raw == "true"


def _coerce(token, raw, source, report, key=None):
    """The canonical value for one declared word, or `None` to write nothing.

    Every token is one of the idioms the retired files actually used, named so
    the table says which idiom a source followed:
      word          the word itself
      line-or-off   the whole line (a guardrails allowlist is several words)
      word-or-off   the word, with an empty file meaning `off`
      word-or-require  the word, with an empty file meaning `require` — the
                    opt-DOWN idiom: absence is the strict answer, not the lax
                    one, so a deleted file can never quietly soften a gate
      int           a decimal integer
      int-or-off    an integer, with `off` meaning 0 (the budget's disable)
      true-exact    BYTE-exactly `true` is on; a case variant is REPORTED
      true-fold     `true` in any case is on; anything else is off
      off-no        `off` in any case is off; anything else (incl. absent) is on
      gate          the gate-authority enum, mostly ambiguous (see AMBIGUOUS)

    The two `true-*` tokens are one idiom split by FIDELITY; see `_true_word`.
    """
    if token in ("word", "line-or-off"):
        return raw
    if token == "word-or-off":
        return raw or "off"
    if token == "word-or-require":
        return raw or "require"
    if token in ("int", "int-or-off"):
        if token == "int-or-off" and raw.lower() == "off":
            return 0
        try:
            return int(raw)
        except ValueError:
            report.append(
                Unmapped(source, raw, (), "is not an integer, so it has no target")
            )
            return None
    if token in ("true-exact", "true-fold"):
        return _true_word(token, raw, source, key, report)
    if token == "off-no":
        return raw.lower() != "off"
    if token == "gate":
        if raw in GATE_AUTHORITY:
            return GATE_AUTHORITY[raw]
        targets, why = AMBIGUOUS.get(
            (source, raw), ((), "is not a declared gate-authority level")
        )
        report.append(Unmapped(source, raw, targets, why))
        return None
    report.append(Unmapped(source, raw, (), "has no conversion rule"))
    return None


def _row_env(row):
    """One registry row's `Env` cell (`KEY=value;KEY2=value2`) as a dict.

    Lenient exactly like `agent_route.parse_env`: an entry with no `=` or an
    empty key is skipped rather than failing the row, because a stray separator
    is not a routing decision.
    """
    env = {}
    for pair in (row.get("Env") or "").replace(";", ",").split(","):
        name, sep, value = pair.strip().partition("=")
        if sep and name.strip():
            env[name.strip()] = value.strip()
    return env


def _route_schema_refusal(route, report):
    """True when the SCHEMA would refuse this converted route — reported, skipped.

    Asks `config.ROUTE_FIELDS` rather than restating `agents.csv`'s row rules,
    which is what makes the parity hold BY CONSTRUCTION: the id shape and the
    shell-safe model slug that `agent_route.load_registry` refuses on the way IN
    are declared patterns on the way OUT, so a rung added to the schema binds
    here without anyone remembering to mirror it.

    Mirroring matters most for the model slug. `load_registry` refuses a Model
    cell with characters outside `[A-Za-z0-9._:/-]` because that cell rides
    `{model}` into a session argv (repo-review 2026-07-21 H-4); a converter that
    carried the same cell into `docs/config.toml` would launder a row the old
    reader rejected into a canonical route nothing rejects.
    """
    config = _load_config_module()
    for spec in config.ROUTE_FIELDS:
        value = route.get(spec.path)
        reason = config._type_reason(spec.type, value) or config._constraint_reason(
            spec, value
        )
        if reason is None:
            continue
        report.append(
            Unmapped(
                "docs/agents.csv",
                "{} {}={!r}".format(route.get("id"), spec.path, value),
                ("routes.{}".format(spec.path),),
                "{} — the schema refuses it, so the row is not converted".format(
                    reason
                ),
            )
        )
        return True
    return False


def routes_from_csv(path, report):
    """`docs/agents.csv` rows -> `[[routes]]` tables.

    The registry carries no capability column, so `capabilities` converts to an
    empty array and the report says so ONCE: an invented capability list would
    be a routing decision made by a script.

    Every row rung `agent_route.load_registry` applies to the SAME file applies
    here too — the placeholder skip, the id shape, uniqueness, the tier
    vocabulary and the shell-safe model slug. A converter that mirrored only some
    of them would be a hole rather than a migration: the rows the live reader
    refuses would arrive in the canonical document as ordinary routes.
    """
    try:
        with path.open(newline="", encoding="utf-8-sig", errors="replace") as fh:
            rows = list(csv.DictReader(fh))
    except OSError as exc:
        report.append(Unmapped(str(path), "", (), "cannot be read: {}".format(exc)))
        return []
    routes, seen = [], set()
    for row in rows:
        rid = (row.get("Id") or "").strip()
        if not rid or rid.startswith("#"):
            continue
        # The kit's inert-placeholder convention: a `-000` id ships as an example
        # and is skipped by every registry reader. Converting it would mint a
        # live [[routes]] table for the example row in every adopter's config.
        if rid.endswith("-000"):
            continue
        if rid in seen:
            report.append(
                Unmapped(
                    "docs/agents.csv",
                    rid,
                    (),
                    "is a duplicate id; the registry reader refuses the second "
                    "row rather than choosing between them",
                )
            )
            continue
        tier = (row.get("Tier") or "").strip().lower()
        strength = TIER_STRENGTH.get(tier)
        if strength is None:
            report.append(
                Unmapped(
                    "docs/agents.csv",
                    "{} tier={!r}".format(rid, tier),
                    ("routes.strength = 1|2|3",),
                    "is not one of {}, so no strength follows from it".format(
                        "|".join(sorted(set(TIER_STRENGTH)))
                    ),
                )
            )
            continue
        route = {
            "id": rid,
            "family": (row.get("Family") or "").strip(),
            "model": (row.get("Model") or "").strip(),
            "strength": strength,
            "argv": (row.get("CmdTemplate") or "").split(),
            "env": _row_env(row),
            "capabilities": [],
            "notes": (row.get("Notes") or "").strip(),
        }
        if _route_schema_refusal(route, report):
            continue
        seen.add(rid)
        routes.append(route)
    if routes:
        report.append(
            Unmapped(
                "docs/agents.csv",
                "capabilities",
                ("routes.capabilities",),
                "the registry has no capability column, so every converted "
                "route carries an empty list — fill it before routing binds",
            )
        )
    return routes


def enabled_pools(path, report):
    """`docs/agents-enabled` -> the per-job weighted pools.

    Presence of the file was the CONSENT surface; that property becomes an
    explicit `[routing] enabled = true`. The per-phase weight grammar
    (`<ID> BUILD=3 REVIEW=0`) is preserved by mapping each phase onto the job it
    names; an unannotated id is weight 1 everywhere, exactly as before.
    """
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        report.append(Unmapped(str(path), "", (), "cannot be read: {}".format(exc)))
        return {}
    entries = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        fields = stripped.split()
        token, annotations = fields[0], fields[1:]
        if "=" in token:
            report.append(
                Unmapped(
                    "docs/agents-enabled",
                    stripped,
                    (),
                    "is a weight annotation with no route id in front of it",
                )
            )
            continue
        weights = {}
        for annotation in annotations:
            phase, sep, value = annotation.partition("=")
            if not sep or phase not in WEIGHT_PHASES or not _WEIGHT_INT_RE.match(value):
                report.append(
                    Unmapped(
                        "docs/agents-enabled",
                        annotation,
                        (),
                        "is not `<PHASE>=<non-negative int>` with PHASE in {}".format(
                            "|".join(WEIGHT_PHASES)
                        ),
                    )
                )
                continue
            if phase in PHASE_UNMAPPED:
                report.append(
                    Unmapped(
                        "docs/agents-enabled",
                        "{} {}".format(token, annotation),
                        PHASE_UNMAPPED[phase],
                        "names a run phase, not one of the declared jobs, so the "
                        "job the weight belongs to is a choice",
                    )
                )
                continue
            weights[phase] = int(value)
        entries.append((token, weights))
    if not entries:
        return {}
    config = _load_config_module()
    pools = {}
    for job in config.JOBS:
        phase = next((p for p, j in PHASE_JOB.items() if j == job), None)
        pools[job] = [
            {"route": token, "weight": weights.get(phase, 1) if phase else 1}
            for token, weights in entries
        ]
    return pools


def _load_config_module():
    """The sibling schema module, imported lazily (contracts §6)."""
    try:
        import config
    except ImportError:  # pragma: no cover - in-process fallback
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import config
    return config


# --- TOML rendering -----------------------------------------------------------
def _fmt(value):
    """One TOML value. Strings go through `json.dumps`, whose escaping is a
    subset of TOML's basic-string escaping, so quotes and newlines round-trip
    without a hand-rolled escaper."""
    if value is True or value is False:
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, (list, tuple)):
        inline = "[" + ", ".join(_fmt(v) for v in value) + "]"
        if len(inline) <= COMMENT_WIDTH:
            return inline
        body = ",\n".join("    " + _fmt(v) for v in value)
        return "[\n" + body + ",\n]"
    if isinstance(value, dict):
        if not value:
            return "{}"
        return (
            "{ "
            + ", ".join("{} = {}".format(k, _fmt(v)) for k, v in value.items())
            + " }"
        )
    raise TypeError("config_migrate: no TOML form for {!r}".format(value))


def _comment(text, prefix="# "):
    """`text` wrapped to the comment width, as TOML comment lines."""
    return [
        prefix + line
        for line in textwrap.wrap(text, width=COMMENT_WIDTH - len(prefix)) or [""]
    ]


def _section_of(path):
    return path.split(".", 1)[0]


def _leaf_of(path):
    return path.split(".", 1)[1]


def render_template():
    """The shipped blank form: the schema version, then every declared dial as a
    COMMENTED line carrying its default and its documentation string.

    Walking `config.SCHEMA` is what keeps the form and the validator from
    drifting: a dial added to the table appears here without anyone remembering
    to add it, and `tests/test_config.py` pins the shipped file equal to this
    rendering.
    """
    config = _load_config_module()
    out = [
        "# docs/config.toml — the single configuration authority (blank form).",
        "#",
        "# Every dial this repo understands is listed below, COMMENTED OUT and",
        "# showing its default. Uncomment only what you actually want to declare:",
        "# an unset key resolves to the default shown, and a key you set while its",
        "# retired one-word file is still present is REFUSED as a mixed source.",
        "#",
        "# Generated by scripts/config_migrate.py --template from the declared",
        "# schema (scripts/config.py SCHEMA). Adopter-owned once written: a kit",
        "# re-sync never overwrites it.",
        "",
        "schema = {}".format(config.SCHEMA_VERSION),
    ]
    for section in config.SECTIONS:
        out.append("")
        out.append("[{}]".format(section))
        for spec in config.SCHEMA:
            if _section_of(spec.path) != section:
                continue
            out.extend(_comment(spec.doc))
            out.append("# {} = {}".format(_leaf_of(spec.path), _fmt(spec.default)))
    out.append("")
    out.extend(
        _comment(
            "Model routes, one [[routes]] table each. Convert an existing "
            "docs/agents.csv with `python scripts/config_migrate.py --write` "
            "rather than writing these by hand."
        )
    )
    for spec in config.ROUTE_FIELDS:
        out.append("#   {} — {}".format(spec.path, spec.doc))
    out.append("")
    out.extend(
        _comment(
            "Per-job weighted pools, one [jobs.<name>] table each. Declared "
            "jobs: {}.".format(", ".join(config.JOBS))
        )
    )
    for spec in config.JOB_FIELDS:
        out.append("#   {} — {}".format(spec.path, spec.doc))
    out.append("")
    out.extend(
        _comment(
            "Reviewed prompt templates, one [prompts.<name>] table each. "
            "Declared prompts: {}.".format(", ".join(config.PROMPTS))
        )
    )
    for spec in config.PROMPT_FIELDS:
        out.append("#   {} — {}".format(spec.path, spec.doc))
    return "\n".join(out) + "\n"


def render_document(values, routes, pools, converted, report):
    """The converted document: only what a retired source actually declared,
    plus the conversion notes as comments so the open questions travel with the
    file instead of scrolling past in a terminal."""
    config = _load_config_module()
    out = [
        "# docs/config.toml — the single configuration authority.",
        "#",
        "# CONVERTED from this repo's retired declared-policy files by",
        "# scripts/config_migrate.py. Only keys a retired source actually",
        "# declared appear below; every other dial resolves to its schema",
        "# default (scripts/config.py SCHEMA — see config.toml.template for the",
        "# full commented list). Adopter-owned: a kit re-sync never overwrites",
        "# this file.",
        "#",
    ]
    out.append("# Converted sources — each of these is STILL PRESENT in the tree,")
    out.append("# so `config.mixed_source_findings` reports every key below as")
    out.append("# double-declared until the retired file is deleted. That is the")
    out.append("# expected transitional state, and the refusal binds at the cutover:")
    out.append("# no runtime reader consults this file yet.")
    for source in converted:
        out.append("#   {}".format(source))
    if report:
        out.append("#")
        out.append("# NOT CONVERTED — each of these needs a human decision. Nothing")
        out.append("# below was guessed; the values are simply absent until chosen:")
        for item in report:
            out.extend(
                _comment(
                    "{}: {!r} {}".format(item.source, item.value, item.why),
                    prefix="#   ",
                )
            )
            if item.targets:
                out.append("#     candidates: {}".format("; ".join(item.targets)))
    out.append("")
    out.append("schema = {}".format(config.SCHEMA_VERSION))

    for section in config.SECTIONS:
        leaves = [
            spec
            for spec in config.SCHEMA
            if _section_of(spec.path) == section and spec.path in values
        ]
        if not leaves:
            continue
        out.append("")
        out.append("[{}]".format(section))
        for spec in leaves:
            out.extend(_comment(spec.doc))
            out.append("{} = {}".format(_leaf_of(spec.path), _fmt(values[spec.path])))

    for route in routes:
        out.append("")
        out.append("[[routes]]")
        for spec in config.ROUTE_FIELDS:
            out.append("{} = {}".format(spec.path, _fmt(route[spec.path])))

    for job in config.JOBS:
        if job not in pools:
            continue
        out.append("")
        out.append("[jobs.{}]".format(job))
        entries = ",\n".join(
            "    {{ route = {}, weight = {} }}".format(_fmt(e["route"]), e["weight"])
            for e in pools[job]
        )
        out.append("pool = [\n" + entries + ",\n]")
    return "\n".join(out) + "\n"


def _schema_refusal(key, value, source, raw, report):
    """True when `value` is one the SCHEMA would refuse — reported, never written.

    A converter that writes a document its own loader rejects has produced the
    worst of both worlds: the adopter's tree now carries a canonical file that
    refuses at preflight, and the retired file that would have worked is still
    the only honest record. SR-140 is explicit that an unmappable value is
    *reported*, and a value the schema refuses is unmappable — a junk word in a
    retired file was tolerated by a `grep` that only ever asked "is it exactly
    this word?", and there is no faithful canonical form for it.

    Validating HERE rather than trusting the coercion table is deliberate: the
    coercions know the retired *idioms* (`true-yes`, `off-no`), while only the
    schema knows the declared *vocabulary*. Asking the schema keeps one authority
    for what a value may be.
    """
    import config

    spec = {k.path: k for k in config.SCHEMA}.get(key)
    if spec is None:
        return False
    reason = config._type_reason(spec.type, value) or config._constraint_reason(
        spec, value
    )
    if reason is None:
        return False
    report.append(
        Unmapped(
            source,
            raw,
            (key,),
            "{} — the schema refuses it, so no canonical value is written".format(
                reason
            ),
        )
    )
    return True


# --- the conversion -----------------------------------------------------------
# `convert` reads one source per LEGACY_MAP row and each reader kind owns its own
# rung below. Extracted rather than left inline because the loop crossed this
# repo's C901 ratchet, and the repo's rule is to answer a crossing by decomposing
# rather than by stamping a larger number.
def _convert_line(row, path, values, converted, report):
    """One retired one-value file -> its canonical key, or a report entry."""
    raw = declared_line(path)
    if raw is None and row.coerce != "word-or-off":
        return
    if row.key is None:
        report.append(
            Unmapped(
                row.source,
                raw or "",
                (),
                "is retired but has no canonical key in the schema",
            )
        )
        return
    value = _coerce(row.coerce, raw or "", row.source, report, key=row.key)
    if value is None:
        return
    if _schema_refusal(row.key, value, row.source, raw or "", report):
        return
    values[row.key] = value
    converted.append(row.source)


def _convert_ini(row, path, values, converted, report):
    """One `[section] key` of a retired ini file -> its canonical key."""
    _, section, key = row.reader.split(":", 2)
    raw = ini_value(path, section, key)
    if raw is None:
        return
    value = _coerce(row.coerce, raw, row.source, report)
    if value is None:
        return
    values[row.key] = value
    converted.append("{} [{}] {}".format(row.source, section, key))


def _report_unkeyed_dials(root, report):
    """The `[agent-loop]` dials no canonical key answers.

    Reported rather than dropped: they are live behaviour today, and an adopter
    who converts and then finds their model map silently gone would rightly
    distrust every other row the converter wrote.
    """
    stack = root / "docs" / "stack.ini"
    if not stack.is_file():
        return
    for dial in ("model", "model-map", "jobs"):
        raw = ini_value(stack, "agent-loop", dial)
        if raw:
            report.append(
                Unmapped(
                    "docs/stack.ini [agent-loop]",
                    "{} = {}".format(dial, raw),
                    (),
                    "has no canonical key: the fallback model dials stay an "
                    "AGENT_* / stack.ini concern until routing binds",
                )
            )


def convert(root, *, write=False):
    """`(document, unmapped_report)` for the repo at `root`.

    Read-only by default (TC-154's read-only permutation): nothing in the tree
    is touched unless `write` is true, and even then the target is written ONLY
    when absent — `docs/config.toml` is adopter-owned, so overwriting it is the
    one thing this converter must never do.
    """
    root = Path(root)
    report = []
    values, converted = {}, []
    routes, pools = [], {}

    for row in LEGACY_MAP:
        path = root.joinpath(*row.source.split("/"))
        if not path.is_file():
            continue
        if row.reader == "line":
            _convert_line(row, path, values, converted, report)
        elif row.reader.startswith("ini:"):
            _convert_ini(row, path, values, converted, report)
        elif row.reader == "agents-csv":
            routes = routes_from_csv(path, report)
            if routes:
                converted.append(row.source)
        elif row.reader == "agents-enabled":
            pools = enabled_pools(path, report)
            # Presence IS the consent (D-5), so the key is set from the file's
            # existence, not from anything inside it.
            values[row.key] = True
            converted.append(row.source)

    _report_unkeyed_dials(root, report)
    document = render_document(values, routes, pools, converted, report)
    if write:
        target = root / "docs" / "config.toml"
        if not target.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(document, encoding="utf-8", newline="\n")
    return document, report


def main(argv=None):
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--write",
        action="store_true",
        help="write docs/config.toml when it is ABSENT (never overwrites)",
    )
    ap.add_argument(
        "--template",
        action="store_true",
        help="print the blank form rendered from the declared schema",
    )
    args = ap.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass

    if args.template:
        sys.stdout.write(render_template())
        return 0

    root = Path(args.root)
    target = root / "docs" / "config.toml"
    if args.write and target.exists():
        print(
            "config_migrate: REFUSED - docs/config.toml (already exists; it is "
            "adopter-owned and this converter never overwrites it)",
            file=sys.stderr,
        )
        return 1

    document, report = convert(root, write=args.write)
    if not args.write:
        sys.stdout.write(document)
    else:
        print("config_migrate: wrote docs/config.toml")
    for item in report:
        print(
            "config_migrate: NOT CONVERTED - {} {!r} ({}){}".format(
                item.source,
                item.value,
                item.why,
                "; candidates: " + "; ".join(item.targets) if item.targets else "",
            ),
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
