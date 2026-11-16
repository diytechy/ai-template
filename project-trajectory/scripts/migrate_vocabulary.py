#!/usr/bin/env python3
"""Rewrite a repository's stored values from the kit's earlier vocabulary to
the current one, in place.

WHY A MIGRATOR AND NOT A READER. The kit's vocabulary was unified on
2026-11-11: one word for one thing, as `GLOSSARY.md` defines them. The
operator ruled out compatibility readers, so the core scripts read the current
spellings only, and a repository that still stores an earlier one reads as if
the value were absent. This script is the path from an earlier kit to the
current one. A repository runs it once, at the re-sync that brings the new
vocabulary in, and it is the one home for knowledge of the earlier spellings:
no other script names them.

WHAT IT REWRITES. Stored values that a current script still reads, and only
those. Each is a whole value in a known place (a line of a binding, a key or a
cell of a registry), never a word inside prose. Prose, comments and the text
of rows are the re-syncing session's to change, and dated records keep the
words they were written in.

    docs/reviews/**/*.requested    outcome = accepted  ->  outcome = recorded
    every registry, both carriers  the requirement field `verification`
                                   (CSV `Verification`)  ->  `verification_method`
                                   (`VerificationMethod`), and in it the method
                                   `Attest`  ->  `Vouch`
    docs/process.toml              the table `[attestation]`  ->  `[authority]`,
                                   and in it `human_approval_through`  ->
                                   `operator_accepts_through`; in `[policies]`,
                                   `push = "human"`  ->  `push = "operator"`
    docs/decisions/*.toml          in each `[decision.<id>]` entry, the key
                                   `owner`  ->  `operator`

One file is renamed rather than rewritten: the operator's scratchpad at the
root, `OWNER_SCRATCHPAD.md`  ->  `OPERATOR_SCRATCHPAD.md`. The kit's scripts
protect it by its current name, so a file left under the earlier one would
lose that protection without a word. It holds a person's private notes, so
it is moved and never opened.

A registry is a `.toml` or `.csv` file directly under `docs/requirements/` or
`docs/test/`, and the acceptance record's copy of each. A registry is rewritten
in place, byte for byte outside the values named above, then parsed again: a
file whose parse would differ in anything else is left untouched and named.

Usage:
    python scripts/migrate_vocabulary.py [--root .] [--check]

`--check` writes nothing and exits 1 when anything still owes the rewrite;
otherwise the values are rewritten and the script exits 0, or 1 when a file
could not be rewritten safely. It imports nothing from the kit, so it runs
whatever state the kit's own scripts are in. Idempotent: a second run finds
nothing to do.
"""

import argparse
import csv
import io
import re
import sys
import tomllib
from pathlib import Path

# A verdict's binding: `<verdict>.requested` beside each adjudication verdict.
REVIEWS_DIR = "docs/reviews"
BINDING_SUFFIX = ".requested"
# The outcome a route wrote once its call succeeded and the verdict parsed.
_BINDING_OUTCOME = re.compile(r"^(outcome[ \t]*=[ \t]*)accepted([ \t]*\r?)$", re.M)

# Where registries live, and the homes of the acceptance record's copies of
# them (the record's own earlier and current directory names).
REGISTRY_DIRS = ("docs/requirements", "docs/test")
RECORD_DIRS = ("docs/archive/last_approved", "docs/archive/last_accepted")

# FIELDS: an earlier field name and the current one, per carrier. A TOML
# registry names a field by its key; a CSV registry by its header cell.
# VALUES: within a field (named as it is AFTER the rename), an earlier value
# and the current one. A cell is matched on its stripped text, as the kit's
# readers match it.
FIELDS = {
    "toml": {"verification": "verification_method"},
    "csv": {"Verification": "VerificationMethod"},
}
VALUES = {
    "toml": {"verification_method": {"Attest": "Vouch"}},
    "csv": {"VerificationMethod": {"Attest": "Vouch"}},
}


class Unsafe(Exception):
    """A registry whose rewrite would change more than the values named."""


def _rewrite(path, pattern, repl, check):
    """True when `path` held the earlier spelling `pattern` finds (and, unless
    `check`, was rewritten with `repl`). Bytes outside the match are kept, the
    file's own line endings included."""
    raw = path.read_bytes().decode("utf-8")
    new = pattern.sub(repl, raw)
    if new == raw:
        return False
    if not check:
        path.write_bytes(new.encode("utf-8"))
    return True


def bindings(root, check):
    """The bindings whose outcome reads `accepted`, each rewritten to
    `recorded`: `([repo-relative path], [])`. A binding is read long after its
    sitting, by every reader looking for the verdict that covers a row or a
    Done-when, so each one moves.

    Implements: SR-247, LLR-369
    """
    folder = root / REVIEWS_DIR
    if not folder.is_dir():
        return [], []
    done = [
        path.relative_to(root).as_posix()
        for path in sorted(folder.rglob("*" + BINDING_SUFFIX))
        if _rewrite(path, _BINDING_OUTCOME, r"\1recorded\2", check)
    ]
    return done, []


def registry_paths(root):
    """Every registry file under `root`: the live ones, then the acceptance
    record's copy of each, in a stable order."""
    for home in (root, *(root / d for d in RECORD_DIRS)):
        for folder in (home / d for d in REGISTRY_DIRS):
            if not folder.is_dir():
                continue
            for path in sorted(folder.iterdir()):
                if path.is_file() and path.suffix in (".toml", ".csv"):
                    yield path


def _current(carrier, field, value):
    """`(field, value)` as the current vocabulary spells them: the field's
    name after `FIELDS`, and, when `value` is a string whose stripped text is
    an earlier value of that field, the same string with the current word."""
    field = FIELDS[carrier].get(field, field)
    if isinstance(value, str):
        word = VALUES[carrier].get(field, {}).get(value.strip())
        if word is not None:
            value = value.replace(value.strip(), word, 1)
    return field, value


# --- the TOML carrier ----------------------------------------------------------

# One row field on one line: `key = "value"` or `key = 'value'`, as every
# registry row writes a short cell. A field written any other way is caught by
# the re-parse below, never guessed at.
_TOML_CELL = re.compile(
    r"^(?P<lead>[ \t]*)(?P<key>[A-Za-z0-9_-]+)(?P<eq>[ \t]*=[ \t]*)"
    r"(?P<quote>[\"'])(?P<value>[^\"'\r\n]*)(?P=quote)(?P<tail>[ \t]*(?:#[^\r\n]*)?\r?)$",
    re.M,
)


def _toml_rows(data):
    """Every row of a parsed registry: the tables two levels down, `[tier.ID]`."""
    for tier in data.values():
        for row in tier.values() if isinstance(tier, dict) else ():
            if isinstance(row, dict):
                yield row


def _toml_expected(data):
    """`data` as it must parse after the rewrite: each row's fields and values
    moved to the current vocabulary, and nothing else."""
    for row in list(_toml_rows(data)):
        for key in list(row):
            new_key, new_value = _current("toml", key, row[key])
            if new_key != key and new_key in row:
                raise Unsafe("a row carries both `{}` and `{}`".format(key, new_key))
            del row[key]
            row[new_key] = new_value
    return data


def _toml_cell(match):
    key, value = _current("toml", match["key"], match["value"])
    return "{}{}{}{}{}{}{}".format(
        match["lead"],
        key,
        match["eq"],
        match["quote"],
        value,
        match["quote"],
        match["tail"],
    )


def migrate_toml(text):
    """`text` with every row field and value in the current vocabulary. Raises
    `Unsafe` when the result would not parse as exactly that.

    Implements: SR-247, LLR-369
    """
    try:
        before = tomllib.loads(text.lstrip("\ufeff"))
    except tomllib.TOMLDecodeError as exc:
        raise Unsafe("it does not parse ({})".format(exc)) from None
    earlier = set(FIELDS["toml"]) | set(VALUES["toml"])
    if not any(key in earlier for row in _toml_rows(before) for key in row):
        return text
    expected = _toml_expected(before)
    new = _TOML_CELL.sub(_toml_cell, text)
    if new == text:
        return text
    try:
        after = tomllib.loads(new.lstrip("\ufeff"))
    except tomllib.TOMLDecodeError:
        after = None
    if after != expected:
        raise Unsafe("a rewrite of it would change more than the vocabulary")
    return new


# --- the CSV carrier -----------------------------------------------------------


def _csv_bare(text, i):
    """The index of the delimiter or line break that ends the cell at `i`."""
    while i < len(text) and text[i] not in ",\r\n":
        i += 1
    return i


def _csv_quoted(text, i):
    """`(value, end)` for the quoted cell opening at `text[i]`: its text with
    doubled quotes folded, and the index just past the cell. Whatever sits
    between the closing quote and the next delimiter stays in the value, as
    the csv module keeps it."""
    i, buf = i + 1, []
    while i < len(text):
        if text[i] != '"':
            buf.append(text[i])
            i += 1
        elif text[i + 1 : i + 2] == '"':
            buf.append('"')
            i += 2
        else:
            i += 1
            break
    end = _csv_bare(text, i)
    return "".join(buf) + text[i:end], end


def _csv_records(text):
    """The records of CSV `text`, each a list of `(start, end, value)`: a
    cell's span in `text`, quotes included, and its unquoted value. Quoted
    cells may hold commas, doubled quotes and line breaks."""
    records, row, i, n = [], [], 0, len(text)
    while i < n:
        start = i
        if text[i] == '"':
            value, i = _csv_quoted(text, i)
        else:
            i = _csv_bare(text, i)
            value = text[start:i]
        row.append((start, i, value))
        if text[i : i + 1] == ",":
            i += 1
            if i == n:
                row.append((i, i, ""))
            continue
        records.append(row)
        row = []
        i += 2 if text[i : i + 2] == "\r\n" else 1
    if row:
        records.append(row)
    return records


def _csv_parsed(text):
    """The records of CSV `text` as the csv module reads them. A raw reader
    on purpose, named in tests/test_csv_header.py: this script imports
    nothing from the kit, and `_csv_preamble` has already cut off the
    comment preamble the kit's reader would drop."""
    return list(csv.reader(io.StringIO(text, newline="")))


def _csv_expected(rows):
    """Parsed CSV `rows` as they must read after the rewrite."""
    if not rows:
        return rows
    header = [
        cell.replace(cell.strip(), FIELDS["csv"].get(cell.strip(), cell.strip()), 1)
        for cell in rows[0]
    ]
    out = [header]
    for row in rows[1:]:
        out.append(
            [
                _current("csv", header[n].strip(), cell)[1] if n < len(header) else cell
                for n, cell in enumerate(row)
            ]
        )
    return out


def _csv_edits(body, records):
    """`[(start, end, cell)]`: each cell of `records` whose text moves, with
    the text that replaces its span in `body`. A header cell moves when it
    names a field by an earlier name; a cell below it when it holds an earlier
    value of that field. Quotes and padding inside the span are kept."""
    edits, header = [], []
    for start, end, value in records[0]:
        name = FIELDS["csv"].get(value.strip(), value.strip())
        header.append(name)
        if name != value.strip():
            edits.append((start, end, body[start:end].replace(value.strip(), name, 1)))
    for record in records[1:]:
        for name, (start, end, value) in zip(header, record):
            new = _current("csv", name, value)[1]
            if new != value:
                cell = body[start:end].replace(value.strip(), new.strip(), 1)
                edits.append((start, end, cell))
    return edits


def _csv_preamble(text):
    """The length of the leading run of blank and `#` comment lines in
    `text`: the preamble the kit's CSV reader drops before the header row.
    Only the leading run counts; a `#` opening a data line, or one inside a
    quoted cell, is data."""
    end = 0
    for line in text.splitlines(keepends=True):
        if line.strip() and not line.lstrip().startswith("#"):
            break
        end += len(line)
    return end


def migrate_csv(text):
    """`text` with its header cells and its cells' values in the current
    vocabulary. A byte-order mark and a leading comment preamble are kept as
    they are, and the header row is the first line after them. Raises
    `Unsafe` when the result would not parse as exactly that.

    Implements: SR-247, LLR-369
    """
    offset = len(text) - len(text.lstrip("\ufeff"))
    offset += _csv_preamble(text[offset:])
    body = text[offset:]
    records = _csv_records(body)
    edits = _csv_edits(body, records) if records else []
    if not edits:
        return text
    new_body = body
    for start, end, cell in sorted(edits, reverse=True):
        new_body = new_body[:start] + cell + new_body[end:]
    if _csv_parsed(new_body) != _csv_expected(_csv_parsed(body)):
        raise Unsafe("a rewrite of it would change more than the vocabulary")
    return text[:offset] + new_body


_CARRIERS = {".toml": migrate_toml, ".csv": migrate_csv}


def registries(root, check):
    """The registries holding a field or a value in an earlier spelling, each
    rewritten: `([repo-relative path], [problem])`. A registry that cannot be
    rewritten safely is left untouched and named in the problems.

    Implements: SR-247, LLR-369
    """
    done, problems = [], []
    for path in registry_paths(root):
        rel = path.relative_to(root).as_posix()
        raw = path.read_bytes().decode("utf-8")
        try:
            new = _CARRIERS[path.suffix](raw)
        except Unsafe as exc:
            problems.append("{}: {}; left untouched".format(rel, exc))
            continue
        if new == raw:
            continue
        if not check:
            path.write_bytes(new.encode("utf-8"))
        done.append(rel)
    return done, problems


# --- the policy file -----------------------------------------------------------

# TABLES: an earlier table name and the current one. KEYS: within a table
# (named as it is AFTER the rename), an earlier key and the current one.
# VALUES: within a table and key (both named as they are after the rename), an
# earlier string value and the current one. The push authority's default was
# spelled `human`; the role is now the operator, a person or a session that
# person delegated the push to.
POLICY_REL = "docs/process.toml"
POLICY_TABLES = {"attestation": "authority"}
POLICY_KEYS = {"authority": {"human_approval_through": "operator_accepts_through"}}
POLICY_VALUES = {"policies": {"push": {"human": "operator"}}}

_TABLE_HEADER = re.compile(
    r"^(?P<lead>[ \t]*\[)(?P<name>[A-Za-z0-9_-]+)(?P<tail>\][ \t]*(?:#[^\r\n]*)?\r?)$"
)
_KEY_LINE = re.compile(r"^(?P<lead>[ \t]*)(?P<key>[A-Za-z0-9_-]+)(?P<rest>[ \t]*=.*)$")
# The `= value` part of a key line when the value is a one-line quoted string.
_QUOTED = re.compile(
    r"^(?P<eq>[ \t]*=[ \t]*)(?P<quote>[\"'])(?P<value>[^\"'\r\n]*)(?P=quote)(?P<tail>.*)$"
)


def _policy_value(table, key, value):
    """`value` as the current vocabulary spells it, for `key` in `table`."""
    if not isinstance(value, str):
        return value
    return POLICY_VALUES.get(table, {}).get(key, {}).get(value, value)


def _policy_rest(table, key, rest):
    """The `= value` part of a key line with its quoted value respelled. A value
    written any other way is left as it is, and the re-parse refuses it."""
    match = _QUOTED.match(rest)
    if not match:
        return rest
    value = _policy_value(table, key, match["value"])
    return "{}{}{}{}{}".format(
        match["eq"], match["quote"], value, match["quote"], match["tail"]
    )


def _policy_table(name, table, declared):
    """`(name, table)` as the current vocabulary spells one top-level table of
    a parsed policy file. Raises `Unsafe` when the file `declared` both
    spellings of the table, or the table carries both spellings of a key."""
    new_name = POLICY_TABLES.get(name, name)
    if new_name != name and new_name in declared:
        raise Unsafe("it declares both `[{}]` and `[{}]`".format(name, new_name))
    if not isinstance(table, dict):
        return new_name, table
    keys, renamed = POLICY_KEYS.get(new_name, {}), {}
    for key, value in table.items():
        new_key = keys.get(key, key)
        if new_key != key and new_key in table:
            raise Unsafe("`[{}]` carries both `{}` and `{}`".format(name, key, new_key))
        renamed[new_key] = _policy_value(new_name, new_key, value)
    return new_name, renamed


def _policy_line(line, table):
    """`(line, table)`: one line of a policy file in the current vocabulary,
    and the table the lines after it belong to. A header names its table; a
    header this cannot read (a dotted or an array table) names none."""
    header = _TABLE_HEADER.match(line)
    if header:
        table = POLICY_TABLES.get(header["name"], header["name"])
        return header["lead"] + table + header["tail"], table
    if line.lstrip().startswith("["):
        return line, None
    cell = _KEY_LINE.match(line)
    if cell and (table in POLICY_KEYS or table in POLICY_VALUES):
        key = POLICY_KEYS.get(table, {}).get(cell["key"], cell["key"])
        return cell["lead"] + key + _policy_rest(table, key, cell["rest"]), table
    return line, table


def migrate_policy(text):
    """Policy-file `text` with its tables, keys and values in the current
    vocabulary.
    Raises `Unsafe` when the result would not parse as exactly that.

    Implements: SR-247, LLR-369
    """
    try:
        before = tomllib.loads(text.lstrip("\ufeff"))
    except tomllib.TOMLDecodeError as exc:
        raise Unsafe("it does not parse ({})".format(exc)) from None
    expected = dict(
        _policy_table(name, table, before) for name, table in before.items()
    )
    if expected == before:
        return text
    lines, table = [], None
    for line in text.split("\n"):
        line, table = _policy_line(line, table)
        lines.append(line)
    new = "\n".join(lines)
    try:
        after = tomllib.loads(new.lstrip("\ufeff"))
    except tomllib.TOMLDecodeError:
        after = None
    if after != expected:
        raise Unsafe("a rewrite of it would change more than the vocabulary")
    return new


def policy(root, check):
    """The policy file, when it names a table, a key or a value by an earlier
    name, rewritten: `([repo-relative path], [problem])`.

    Implements: SR-247, LLR-369
    """
    path = root / POLICY_REL
    if not path.is_file():
        return [], []
    raw = path.read_bytes().decode("utf-8")
    try:
        new = migrate_policy(raw)
    except Unsafe as exc:
        return [], ["{}: {}; left untouched".format(POLICY_REL, exc)]
    if new == raw:
        return [], []
    if not check:
        path.write_bytes(new.encode("utf-8"))
    return [POLICY_REL], []


# --- the delegated-decisions records ------------------------------------------

# A delegated run's record: `docs/decisions/<run>.toml`, one `[decision.<id>]`
# table per entry. The operator's verdict on an entry was keyed `owner`.
DECISIONS_DIR = "docs/decisions"
DECISION_KEYS = {"owner": "operator"}

# Any table header, dotted names included: `[decision.D-001]`.
_ANY_HEADER = re.compile(
    r"^[ \t]*\[(?P<name>[A-Za-z0-9_.-]+)\][ \t]*(?:#[^\r\n]*)?\r?$"
)


def _decision_entries(data):
    """Every entry table of a parsed decisions record: `[decision.<id>]`."""
    tier = data.get("decision")
    if not isinstance(tier, dict):
        return []
    return [entry for entry in tier.values() if isinstance(entry, dict)]


def _decisions_expected(data):
    """`data` as it must parse after the rewrite: each entry's keys moved to
    the current vocabulary. Raises `Unsafe` for an entry carrying both."""
    for entry in _decision_entries(data):
        for key, new in DECISION_KEYS.items():
            if key not in entry:
                continue
            if new in entry:
                raise Unsafe("an entry carries both `{}` and `{}`".format(key, new))
            entry[new] = entry.pop(key)
    return data


def _decision_line(line, in_entry):
    """`(line, in_entry)`: one line of a decisions record with an entry's key
    respelled, and whether the lines after it belong to an entry."""
    header = _ANY_HEADER.match(line)
    if header:
        return line, header["name"].startswith("decision.")
    if line.lstrip().startswith("["):
        return line, False
    cell = _KEY_LINE.match(line)
    if in_entry and cell and cell["key"] in DECISION_KEYS:
        return cell["lead"] + DECISION_KEYS[cell["key"]] + cell["rest"], in_entry
    return line, in_entry


def migrate_decisions_record(text):
    """Decisions-record `text` with each entry's keys in the current
    vocabulary. Raises `Unsafe` when the result would not parse as exactly
    that.

    Implements: SR-247, LLR-369
    """
    try:
        before = tomllib.loads(text.lstrip("\ufeff"))
    except tomllib.TOMLDecodeError as exc:
        raise Unsafe("it does not parse ({})".format(exc)) from None
    entries = _decision_entries(before)
    if not any(key in entry for entry in entries for key in DECISION_KEYS):
        return text
    expected = _decisions_expected(before)
    lines, in_entry = [], False
    for line in text.split("\n"):
        line, in_entry = _decision_line(line, in_entry)
        lines.append(line)
    new = "\n".join(lines)
    try:
        after = tomllib.loads(new.lstrip("\ufeff"))
    except tomllib.TOMLDecodeError:
        after = None
    if after != expected:
        raise Unsafe("a rewrite of it would change more than the vocabulary")
    return new


def decisions(root, check):
    """Each delegated-decisions record whose entries carry a key by an earlier
    name, rewritten: `([repo-relative path], [problem])`. Only the key moves;
    the record's prose keeps the words it was written in.

    Implements: SR-247, LLR-369
    """
    folder = root / DECISIONS_DIR
    if not folder.is_dir():
        return [], []
    done, problems = [], []
    for path in sorted(folder.glob("*.toml")):
        rel = path.relative_to(root).as_posix()
        raw = path.read_bytes().decode("utf-8")
        try:
            new = migrate_decisions_record(raw)
        except Unsafe as exc:
            problems.append("{}: {}; left untouched".format(rel, exc))
            continue
        if new == raw:
            continue
        if not check:
            path.write_bytes(new.encode("utf-8"))
        done.append(rel)
    return done, problems


# --- the operator's scratchpad --------------------------------------------------

# The root notes file, by its earlier and its current name.
SCRATCHPAD_NAMES = ("OWNER_SCRATCHPAD.md", "OPERATOR_SCRATCHPAD.md")


def scratchpad(root, check):
    """The scratchpad under its earlier name, renamed to the current one and
    never opened: `([what moved], [problem])`. Both names present is a
    problem, left for the operator to merge.

    Implements: SR-247, LLR-369
    """
    old, new = (root / name for name in SCRATCHPAD_NAMES)
    if not old.is_file():
        return [], []
    if new.exists():
        return [], [
            "{}: {} exists too; merge the two by hand".format(*SCRATCHPAD_NAMES)
        ]
    if not check:
        old.rename(new)
    return ["{} -> {}".format(*SCRATCHPAD_NAMES)], []


# Each step: what it is called in the report, and the function that takes it.
STEPS = (
    ("verdict binding", bindings),
    ("registry", registries),
    ("policy file", policy),
    ("decisions record", decisions),
    ("scratchpad", scratchpad),
)


def main(argv=None):
    """Rewrite (or, with `--check`, report) every stored value in an earlier
    spelling; exit 0 when nothing is left to do, else 1.

    Implements: SR-247, LLR-369
    """
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n", 1)[0])
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument("--check", action="store_true", help="report what owes the rewrite")
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    verb = "owes the rewrite" if args.check else "rewritten"
    owed, unsafe = 0, 0
    for name, step in STEPS:
        done, problems = step(root, args.check)
        owed += len(done)
        unsafe += len(problems)
        for item in done:
            print("migrate_vocabulary: {} {}: {}".format(name, verb, item))
        for line in problems:
            print("migrate_vocabulary: {} NOT rewritten: {}".format(name, line))
    if not owed and not unsafe:
        print("migrate_vocabulary: nothing stored in an earlier spelling")
    return 1 if unsafe or (args.check and owed) else 0


if __name__ == "__main__":
    sys.exit(main())
