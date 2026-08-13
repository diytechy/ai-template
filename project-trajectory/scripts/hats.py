#!/usr/bin/env python3
"""hats.py — the HATS ROSTER reader: which declared expert perspectives apply to
a decomposition, and the block a brief embeds so the session has to face them.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX).

WHY THIS MODULE EXISTS (SN-036, ruled at OI-19 on 2026-08-13). SN-036 requires
that a need turned into detailed requirements is examined from every relevant
expert and downstream-user perspective. Before this module those roles lived in
prose and column headers and had NO mechanical existence at all: nothing put a
perspective to a decomposition, and nothing could say whether one had ever been
applied. The roster (`docs/requirements/hats.toml`) declares the perspectives;
this module decides which of them a given decomposition must face; the brief
composer embeds their questions. That is the INJECTION half. The per-decomposition
RECORD half of SN-036's acceptance — which hats were applied and what each
produced — is DELIBERATELY NOT BUILT HERE: injection alone already changes what
a decomposition produces, while a record built first would be a form to fill in
with nothing behind it (OI-19's sequencing). Nothing gates on a hat today.

ABSENT IS OPT-OUT, MALFORMED IS A REFUSAL. An adopter who deletes the roster
gets composers that proceed without hats — the roster is a layer, not a floor.
A roster that EXISTS and does not parse, or carries a row missing a required
key, or an `applies_when` this module cannot evaluate, raises `HatsError`: a
broken roster reported as an empty one is a decomposition that silently faced
no perspective at all, which is the most expensive way for this machinery to be
wrong. (The same absent-vs-malformed split `spine_carrier.load` draws for the
spine registries.)

`applies_when` IS A CLOSED GRAMMAR, NOT PROSE — because a condition a composer
cannot evaluate is a comment:

    always
    scope == "template"          scope != "this-repo"
    kind == "core"               kind != "draft"
    tags contains "unattended"

Clauses join with `or` OR with `and`; MIXING THEM IN ONE EXPRESSION IS REFUSED,
so no reader ever has to guess a precedence the author did not write. The split
is on the bare keywords, so a VALUE containing ` or ` / ` and ` breaks its
clause and the roster refuses — loudly, naming the clause, which is the right
trade for not carrying a quote-aware tokenizer for values that are tags and
enum words. Scalar
fields (`scope`, `kind`) take `==` / `!=` only; the list field (`tags`) takes
`contains` only — an operator that would need a defined answer for "a list
equals a word" never parses. And the rule that keeps the roster honest as it
ships to projects whose registries carry different facts:

    A FIELD THE COMPOSER DID NOT DECLARE SATISFIES NO CONDITION.

An undeclared fact is not a true one, and it is not a false one either — so
`scope != "template"` over a context with no `scope` is FALSE, not true. A hat
keyed on a fact this project does not yet record stays silent rather than
firing on every decomposition; the fix is to declare the fact (or edit the
roster), never to let the absence read as a match.

WHY tomllib DIRECTLY AND NOT `spine_carrier`. The carrier owns the SPINE's
vocabulary — a stated key->column map, the id-column tier table, and the
migrate_carrier inverse that `tests/test_rule_sync.py` pins. The roster shares
none of it: its rows are keyed by NAME rather than by a numeric id space, it
has three keys of its own, and it is not a tier anything traces through.
Registering it there would grow the map every spine reader consults for a
registry none of them read. Forty lines of `tomllib` here is the smaller change.

Usage (the CLI is a documentation aid; the module is library-first):

    python scripts/hats.py list [--root .]
    python scripts/hats.py applicable [--root .] [--scope S] [--kind K] [--tag T]...
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

# The roster's home, relative to the repo root.
ROSTER_REL = "docs/requirements/hats.toml"

# The one top-level table; a roster declaring anything else is malformed.
TABLE = "hat"

# Every key a hat row must carry. `listens_for` is required for a reason worth
# stating: a hat that names no FAILURE CLASS is ceremony, and the cheapest way
# to refuse ceremony is to make its absence unparseable.
REQUIRED_KEYS = ("applies_when", "asks", "listens_for")

# The context fields `applies_when` may name, split by the operators they admit.
SCALAR_FIELDS = ("scope", "kind")
LIST_FIELDS = ("tags",)
FIELDS = SCALAR_FIELDS + LIST_FIELDS

ALWAYS = "always"

# `<field> <op> <value>`; the value is quoted (either quote) or a bare token.
_CLAUSE_RE = re.compile(
    r"""^(?P<field>[a-z_]+)\s+(?P<op>==|!=|contains)\s+"""
    r"""(?:"(?P<dq>[^"]*)"|'(?P<sq>[^']*)'|(?P<bare>\S+))$"""
)
# The join keywords, as whole words between clauses.
_JOIN_RE = re.compile(r"\s+(or|and)\s+")


class HatsError(Exception):
    """A roster that exists and cannot be trusted — the loud half of
    absent-is-opt-out. Never raised for an absent file."""


# --- reading ------------------------------------------------------------------
def roster_path(root, rel=ROSTER_REL):
    """The roster file for a repo root."""
    return Path(root) / rel


def load(root, rel=ROSTER_REL):
    """The roster as a list of hat dicts in DECLARED ORDER — each
    `{"name", "applies_when", "asks", "listens_for"}` with `applies_when`
    already parsed (so a condition nobody can evaluate fails at load, where
    there is a file to fix, rather than at the composition it would have
    silently skipped).

    `[]` when the file is absent — the adopter opted out. `HatsError` when it
    exists and is not a usable roster."""
    path = roster_path(root, rel)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return []
    except OSError as exc:
        raise HatsError("{}: cannot be read ({})".format(path, exc)) from exc
    try:
        data = tomllib.loads(raw.decode("utf-8-sig"))
    except (tomllib.TOMLDecodeError, UnicodeDecodeError) as exc:
        raise HatsError(
            "{} does not parse as TOML ({}) — refusing to report an unreadable "
            "roster as an empty one".format(path, exc)
        ) from exc

    extra = sorted(k for k in data if k != TABLE)
    if extra:
        raise HatsError(
            "{}: unknown top-level table(s) {} — a roster declares only "
            "[{}.<NAME>]".format(path, ", ".join(extra), TABLE)
        )
    # `.get(TABLE, {})`, never `or {}`: a falsey non-table (`hat = ""`,
    # `hat = false`, `hat = []`) is a MALFORMED roster and must refuse loudly —
    # coercing it to an empty roster is the silent opt-out this loader exists
    # to forbid (review finding). Only true ABSENCE reads as opt-out.
    table = data.get(TABLE, {})
    if not isinstance(table, dict):
        raise HatsError("{}: [{}] is not a table of hats".format(path, TABLE))

    return [
        _hat_from_row(name, row, "{}: [{}.{}]".format(path, TABLE, name))
        for name, row in table.items()
    ]


def _hat_from_row(name, row, where):
    """One validated hat, or HatsError naming exactly which key is wrong.

    Split out of `load` so the file-level rules (does it exist, does it parse,
    does it declare only `[hat.*]`) and the row-level ones (three keys, all
    present, all non-empty, a condition that parses) read as two jobs rather
    than one nested loop."""
    if not isinstance(row, dict):
        raise HatsError("{} is not a table".format(where))
    unknown = sorted(k for k in row if k not in REQUIRED_KEYS)
    if unknown:
        raise HatsError(
            "{} declares unknown key(s) {} — a hat carries {}".format(
                where, ", ".join(unknown), ", ".join(REQUIRED_KEYS)
            )
        )
    hat = {"name": name}
    for key in REQUIRED_KEYS:
        value = row.get(key)
        if not isinstance(value, str) or not value.strip():
            raise HatsError(
                "{} has no `{}` — every hat must name its condition, its "
                "question and the FAILURE CLASS it catches (a hat naming "
                "no failure is ceremony)".format(where, key)
            )
        # Whitespace is COLLAPSED at load: `asks`/`listens_for` render inside
        # a one-line markdown bullet in the composed brief, and a multi-line
        # value would put its later lines at column 0 — where `## ...` becomes
        # a top-level heading that can override the brief's own structure
        # (review finding). Inline text cannot mint a heading.
        hat[key] = " ".join(value.split())
    hat["condition"] = parse_condition(hat["applies_when"], where)
    return hat


# --- the applies_when grammar -------------------------------------------------
def parse_condition(expr, where="applies_when"):
    """`(join, [(field, op, value), ...])` for a condition, or `("always", [])`.

    Raises HatsError on anything outside the closed grammar — including a mixed
    `or`/`and` expression, an operator a field does not admit, and a field name
    no context can carry."""
    text = (expr or "").strip()
    if text == ALWAYS:
        return (ALWAYS, [])
    # A capturing split interleaves clause, join, clause, join, ... — the even
    # slots are the clauses and the odd ones the joins.
    parts = _JOIN_RE.split(text)
    clauses, joins = parts[0::2], parts[1::2]
    if len(set(joins)) > 1:
        raise HatsError(
            "{}: {!r} mixes `or` and `and` — write one or the other, so no "
            "reader has to guess a precedence you did not state".format(where, expr)
        )
    join = joins[0] if joins else "or"
    parsed = []
    for clause in clauses:
        matched = _CLAUSE_RE.match(clause.strip())
        if matched is None:
            raise HatsError(
                "{}: {!r} is not an evaluable clause — expected `always` or "
                "`<field> <op> <value>` with field in {} and op in "
                "==/!=/contains".format(where, clause.strip(), "/".join(FIELDS))
            )
        field, op = matched.group("field"), matched.group("op")
        value = matched.group("dq")
        if value is None:
            value = matched.group("sq")
        if value is None:
            value = matched.group("bare")
        if field not in FIELDS:
            raise HatsError(
                "{}: unknown field {!r} — a composer can declare {}".format(
                    where, field, ", ".join(FIELDS)
                )
            )
        if field in LIST_FIELDS and op != "contains":
            raise HatsError(
                "{}: `{}` is a list, so it takes `contains` only (got {!r})".format(
                    where, field, op
                )
            )
        if field in SCALAR_FIELDS and op == "contains":
            raise HatsError(
                "{}: `{}` is a single value, so it takes == / != only".format(
                    where, field
                )
            )
        parsed.append((field, op, value))
    return (join, parsed)


def evaluate(condition, context):
    """Whether a parsed condition holds for `context` — a dict that may carry
    `scope`, `kind` (strings) and `tags` (an iterable of strings).

    A FIELD THE CONTEXT DOES NOT DECLARE SATISFIES NO CLAUSE, `!=` included:
    an undeclared fact is not a true one, and reading its absence as a match
    would fire a hat on every decomposition in a project that never records
    that fact."""
    join, clauses = condition
    if join == ALWAYS:
        return True
    results = [_clause_holds(c, context) for c in clauses]
    return all(results) if join == "and" else any(results)


def _clause_holds(clause, context):
    field, op, value = clause
    have = (context or {}).get(field)
    if have is None:
        return False  # an undeclared fact satisfies nothing
    if field in LIST_FIELDS:
        tags = [str(t).strip() for t in have if str(t).strip()]
        return value in tags
    have = str(have).strip()
    if not have:
        return False
    return have == value if op == "==" else have != value


def applicable(roster, context):
    """The hats whose `applies_when` holds for `context`, in declared order."""
    return [h for h in roster if evaluate(h["condition"], context)]


# --- the contexts a composer builds -------------------------------------------
def context_from_need(row):
    """The decomposition context for ONE stakeholder-need row: its declared
    `scope` and `kind`, plus any declared `tags`.

    Reads only TYPED cells, under either the TOML key or the column name the
    carrier reports. A cell the row does not carry is simply absent from the
    context, which (see `evaluate`) means no clause keyed on it fires — the
    honest reading of a fact the registry has not recorded yet."""
    ctx = {}
    for field in SCALAR_FIELDS:
        value = _first(row, field, field.capitalize())
        if isinstance(value, str) and value.strip():
            ctx[field] = value.strip()
    tags = _first(row, "tags", "Tags")
    tags = _as_tags(tags)
    if tags:
        ctx["tags"] = tags
    return ctx


def context_from_work_item(row):
    """The decomposition context for a WORK-ITEM row — the shape the dual-plan
    decomposition round actually has in hand.

    `tags` are the row's two typed classification cells, `Workstream` and
    `SafetyClass`; `scope` and `kind` are left UNDECLARED because a work item
    carries neither, so a roster clause keyed on them stays silent here instead
    of matching by accident. A need-level composer supplies those two through
    `context_from_need` once the need registry carries them as fields."""
    # The scope FIELD that would make the scope-keyed hats fire is the subject
    # of stakeholder need SN-039 (a declared scope value, not prose to infer).
    # Named in a comment rather than the docstring so the arch-map harvest does
    # not read a POINTER to a need as a claim to implement one.
    tags = []
    for key in ("Workstream", "workstream", "SafetyClass", "safety_class"):
        value = (row or {}).get(key)
        if isinstance(value, str) and value.strip() and value.strip() not in tags:
            tags.append(value.strip())
    return {"tags": tags} if tags else {}


def _first(row, *keys):
    for key in keys:
        if key in (row or {}):
            return row[key]
    return None


def _as_tags(value):
    if isinstance(value, str):
        return [t.strip() for t in value.replace(",", ";").split(";") if t.strip()]
    if isinstance(value, (list, tuple)):
        return [str(t).strip() for t in value if str(t).strip()]
    return []


# --- what a brief embeds ------------------------------------------------------
# The line a brief carries when no hat applies (or the roster is absent). It is
# a STATED opt-out, not a placeholder: the reader can tell "no perspective was
# declared for this" from "the section did not get filled".
NO_HATS = (
    "_(no declared perspective applies to this decomposition — "
    "docs/requirements/hats.toml is absent, or no hat's `applies_when` "
    "matched.)_"
)


def brief_block(hats):
    """The markdown block a decomposition brief embeds: one entry per applicable
    hat carrying its NAME, its question, and the failure class it listens for.

    The question is what the session must answer; `listens_for` rides along
    because a perspective stated without its failure class is an invitation to
    write a paragraph of reassurance."""
    if not hats:
        return NO_HATS
    out = []
    for hat in hats:
        out.append("- **{}** — {}".format(hat["name"], hat["asks"]))
        out.append("  - listens for: {}".format(hat["listens_for"]))
    return "\n".join(out)


def questions(hats):
    """Just the `asks` texts, in order — for a caller that lays out its own
    block (and for tests that assert a brief faced every applicable hat)."""
    return [h["asks"] for h in hats]


# --- CLI (documentation aid; the module is library-first) ---------------------
def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (the trace.py/check.py guard)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def _context_from_args(args):
    ctx = {}
    if args.scope:
        ctx["scope"] = args.scope
    if args.kind:
        ctx["kind"] = args.kind
    if args.tag:
        ctx["tags"] = list(args.tag)
    return ctx


def _cmd_list(args):
    roster = load(args.root)
    if not roster:
        print("(no roster at {})".format(roster_path(args.root)))
        return 0
    for hat in roster:
        print(
            "{}\n  when: {}\n  asks: {}\n  listens for: {}".format(
                hat["name"], hat["applies_when"], hat["asks"], hat["listens_for"]
            )
        )
    return 0


def _cmd_applicable(args):
    chosen = applicable(load(args.root), _context_from_args(args))
    print(brief_block(chosen))
    return 0


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root holding docs/ (default: .)")
    sub = ap.add_subparsers(dest="cmd")

    lst = sub.add_parser("list", help="print the declared roster")
    lst.set_defaults(func=_cmd_list)

    app = sub.add_parser("applicable", help="print the hats a context must face")
    app.add_argument("--scope", default="", help="the decomposition's declared scope")
    app.add_argument("--kind", default="", help="the decomposition's declared kind")
    app.add_argument(
        "--tag", action="append", default=[], help="a declared tag (repeatable)"
    )
    app.set_defaults(func=_cmd_applicable)

    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    try:
        return args.func(args)
    except HatsError as exc:
        print("hats: {}".format(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
