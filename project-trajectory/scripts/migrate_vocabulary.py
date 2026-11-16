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
                                   `Attest`  ->  `Vouch`; in every row's
                                   `status` (CSV `Status`), `Approved`  ->
                                   `Accepted`
    docs/process.toml              the table `[attestation]`  ->  `[authority]`,
                                   and in it `human_approval_through`  ->
                                   `operator_accepts_through`; in `[policies]`,
                                   `push = "human"`  ->  `push = "operator"`;
                                   in `[adjudicator] retain_for`, the brief
                                   kind `"first-approval"`  ->
                                   `"first-acceptance"`
    docs/decisions/*.toml         in each `[decision.<id>]` entry, the key
                                   `owner`  ->  `operator`
    docs/work/**/*.md,             in each work item's front matter and in each
    docs/archive/work/**/*.md      row drafted in its `## Dispositions` section,
                                   the key `bar`  ->  `checks_stage`

One file is renamed rather than rewritten: the operator's scratchpad at the
root, `OWNER_SCRATCHPAD.md`  ->  `OPERATOR_SCRATCHPAD.md`. The kit's scripts
protect it by its current name, so a file left under the earlier one would
lose that protection without a word. It holds a person's private notes, so
it is moved and never opened.

One directory is moved: the acceptance record, `docs/archive/last_approved/`
->  `docs/archive/last_accepted/`. In its act ledger, `acts.toml`, each
`[[act]]` entry's keys `approved`  ->  `accepted` and `reattested`  ->
`reaccepted`. Then each registry copy in it is written equal to its live
registry, because a copy that differs from live is drift the kit would report
and a renamed directory writes every copy anyway. That absorbs whatever text
had moved since the last act, so every accepted cell that differed is named
in the output, for the operator to read. The record's README keeps its words.

Links into the record follow it: in every Markdown file of the repository, a
link target that names the record's earlier directory as a whole path segment
names the current one, so `check_docs` does not report it broken. The link
text and every other word of the file stay as written.

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
import os
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
# The status a row holds once accepted was `Approved`; the kit's readers fold
# its case, so each case it was written in moves.
_STATUS = {"Approved": "Accepted", "approved": "accepted", "APPROVED": "ACCEPTED"}
VALUES = {
    "toml": {"verification_method": {"Attest": "Vouch"}, "status": _STATUS},
    "csv": {"VerificationMethod": {"Attest": "Vouch"}, "Status": _STATUS},
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
# person delegated the push to. ITEMS: within a table and a key holding a list
# of strings, an earlier element and the current one. The adjudicator's
# retained sittings are named by brief kind, and the sitting that takes a row
# into acceptance was the kind `first-approval`.
POLICY_REL = "docs/process.toml"
POLICY_TABLES = {"attestation": "authority"}
POLICY_KEYS = {"authority": {"human_approval_through": "operator_accepts_through"}}
POLICY_VALUES = {"policies": {"push": {"human": "operator"}}}
POLICY_ITEMS = {"adjudicator": {"retain_for": {"first-approval": "first-acceptance"}}}

_TABLE_HEADER = re.compile(
    r"^(?P<lead>[ \t]*\[)(?P<name>[A-Za-z0-9_-]+)(?P<tail>\][ \t]*(?:#[^\r\n]*)?\r?)$"
)
_KEY_LINE = re.compile(r"^(?P<lead>[ \t]*)(?P<key>[A-Za-z0-9_-]+)(?P<rest>[ \t]*=.*)$")
# The `= value` part of a key line when the value is a one-line quoted string.
_QUOTED = re.compile(
    r"^(?P<eq>[ \t]*=[ \t]*)(?P<quote>[\"'])(?P<value>[^\"'\r\n]*)(?P=quote)(?P<tail>.*)$"
)
# One quoted element of a list.
_ITEM = re.compile(r"(?P<quote>[\"'])(?P<value>[^\"'\r\n]*)(?P=quote)")


def _policy_value(table, key, value):
    """`value` as the current vocabulary spells it, for `key` in `table`: a
    string through `POLICY_VALUES`, each string of a list through
    `POLICY_ITEMS`."""
    if isinstance(value, list):
        items = POLICY_ITEMS.get(table, {}).get(key, {})
        return [items.get(v, v) if isinstance(v, str) else v for v in value]
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


def _code_part(text):
    """Where the comment of a line of TOML starts: the index of its first `#`
    outside a quoted string, or the line's length when it has none."""
    quote = None
    for i, char in enumerate(text):
        if quote:
            quote = None if char == quote else quote
        elif char in "\"'":
            quote = char
        elif char == "#":
            return i
    return len(text)


def _array_line(text, items):
    """`(text, items)`: one line of a list whose elements `items` respells,
    each quoted element before its comment in the current vocabulary, and
    `items` again while the list stays open after it (None once a `]` before
    the comment closes it). The comment keeps its words."""
    cut = _code_part(text)
    code = _ITEM.sub(
        lambda m: "{0}{1}{0}".format(m["quote"], items.get(m["value"], m["value"])),
        text[:cut],
    )
    return code + text[cut:], (None if "]" in code else items)


def _array_opened(line, table):
    """`(line, items)` for a line of `table`: when its key holds a list that
    `POLICY_ITEMS` respells, the line with the elements on it respelled and the
    map for the lines after it while the list is open; otherwise the line as
    it is and None."""
    cell = _KEY_LINE.match(line)
    items = POLICY_ITEMS.get(table, {}).get(cell["key"]) if cell else None
    if not items or not cell["rest"].lstrip(" \t=").startswith("["):
        return line, None
    rest, items = _array_line(cell["rest"], items)
    return cell["lead"] + cell["key"] + rest, items


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
    lines, table, items = [], None, None
    for line in text.split("\n"):
        if items:
            line, items = _array_line(line, items)
        else:
            line, table = _policy_line(line, table)
            line, items = _array_opened(line, table)
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


def _parsed(text):
    """The parse of TOML `text`. Raises `Unsafe` when it does not parse."""
    try:
        return tomllib.loads(text.lstrip("﻿"))
    except tomllib.TOMLDecodeError as exc:
        raise Unsafe("it does not parse ({})".format(exc)) from None


def _moved_keys(entries, keys):
    """Each entry table of `entries` with the keys `keys` maps moved to their
    current names, in place. Raises `Unsafe` for an entry carrying both."""
    for entry in entries:
        for key, new in keys.items():
            if key not in entry:
                continue
            if new in entry:
                raise Unsafe("an entry carries both `{}` and `{}`".format(key, new))
            entry[new] = entry.pop(key)


def _rekeyed(text, entries_of, keys, step):
    """`text` with the keys `keys` maps respelled in every entry table
    `entries_of` finds in its parse, by a line edit through `step(line,
    inside)`, which says whether the lines after it belong to an entry.
    Raises `Unsafe` when the result would not parse as exactly that."""
    expected = _parsed(text)
    entries = entries_of(expected)
    if not any(key in entry for entry in entries for key in keys):
        return text
    _moved_keys(entries, keys)
    lines, inside = [], False
    for line in text.split("\n"):
        line, inside = step(line, inside)
        lines.append(line)
    new = "\n".join(lines)
    try:
        after = tomllib.loads(new.lstrip("﻿"))
    except tomllib.TOMLDecodeError:
        after = None
    if after != expected:
        raise Unsafe("a rewrite of it would change more than the vocabulary")
    return new


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
    return _rekeyed(text, _decision_entries, DECISION_KEYS, _decision_line)


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


# --- work items ------------------------------------------------------------------

# A work item is a spec file under `docs/work/` or its archive: TOML front
# matter between two `+++` lines, and, in a `## Dispositions` section, the rows
# it drafts, each in a fenced ```toml block. The stage a row pins its landing
# checks to was keyed `bar`; it is `checks_stage`.
WORK_DIRS = ("docs/work", "docs/archive/work")
WORK_ITEM_KEYS = {"bar": "checks_stage"}
_FRONT_MATTER = "+++"
_DISPOSITIONS = "## Dispositions"
_TOML_FENCE, _FENCE = "```toml", "```"
# A line that may declare one of the keys, before anything is parsed.
_WORK_ITEM_KEY = re.compile(
    r"^[ \t]*(?:{})[ \t]*=".format("|".join(map(re.escape, WORK_ITEM_KEYS))), re.M
)


def _front_matter_span(lines):
    """`[(first, end)]`: the line span of a work item's front matter, between
    the `+++` line it opens with and the next one, or `[]` when it has none."""
    if not lines or lines[0].lstrip("﻿").rstrip() != _FRONT_MATTER:
        return []
    for end in range(1, len(lines)):
        if lines[end].rstrip() == _FRONT_MATTER:
            return [(1, end)]
    return []


def _disposition_spans(lines):
    """`[(first, end)]`: the line span of each fenced ```toml block of a work
    item's `## Dispositions` section, which runs to the next `## ` heading."""
    spans, opened, inside = [], None, False
    for number, line in enumerate(lines):
        text = line.rstrip()
        if text.startswith("## "):
            inside, opened = text == _DISPOSITIONS, None
        elif inside and opened is None and text == _TOML_FENCE:
            opened = number + 1
        elif inside and opened is not None and text == _FENCE:
            spans.append((opened, number))
            opened = None
    return spans


def _top_level_line(line, in_table):
    """`(line, in_table)`: one line of a TOML segment with a top-level key
    respelled, and whether the lines after it belong to a table."""
    if line.lstrip().startswith("["):
        return line, True
    cell = _KEY_LINE.match(line)
    if not in_table and cell and cell["key"] in WORK_ITEM_KEYS:
        return cell["lead"] + WORK_ITEM_KEYS[cell["key"]] + cell["rest"], in_table
    return line, in_table


def migrate_work_item(text):
    """Work-item `text` with each top-level key of its front matter and of the
    rows its `## Dispositions` section drafts in the current vocabulary. Raises
    `Unsafe` when a segment's result would not parse as exactly that.

    Implements: SR-247, LLR-369
    """
    lines = text.split("\n")
    for first, end in _front_matter_span(lines) + _disposition_spans(lines):
        segment = "\n".join(lines[first:end]) + "\n"
        if not _WORK_ITEM_KEY.search(segment):
            continue
        new = _rekeyed(segment, lambda data: [data], WORK_ITEM_KEYS, _top_level_line)
        lines[first:end] = new[:-1].split("\n")
    return "\n".join(lines)


def _work_item_files(root):
    """Each `.md` file under the work-item folders, the archive's included."""
    for folder in (root / d for d in WORK_DIRS):
        if folder.is_dir():
            yield from sorted(folder.rglob("*.md"))


def work_items(root, check):
    """Each work item whose front matter or drafted rows carry a key by an
    earlier name, rewritten: `([repo-relative path], [problem])`. Only the key
    moves; the item's prose keeps the words it was written in.

    Implements: SR-247, LLR-369
    """
    done, problems = [], []
    for path in _work_item_files(root):
        rel = path.relative_to(root).as_posix()
        try:
            raw = path.read_bytes().decode("utf-8")
            new = migrate_work_item(raw)
        except UnicodeDecodeError:
            problems.append("{}: not UTF-8; left untouched".format(rel))
            continue
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


# --- the acceptance record -------------------------------------------------------

# The record's directory is `RECORD_DIRS` above, by its earlier and current
# name. Its act ledger holds one `[[act]]` entry per act; each named the rows
# it carried into acceptance and the rows it re-accepted under earlier keys.
LEDGER_NAME = "acts.toml"
LEDGER_KEYS = {"approved": "accepted", "reattested": "reaccepted"}
# A row the copy holds as accepted, in either spelling of the status.
_ACCEPTED_WORDS = frozenset({"approved", "accepted"})

# An array-of-tables header: `[[act]]`.
_ARRAY_HEADER = re.compile(
    r"^[ \t]*\[\[(?P<name>[A-Za-z0-9_.-]+)\]\][ \t]*(?:#[^\r\n]*)?\r?$"
)


def _ledger_entries(data):
    """Every `[[act]]` entry of a parsed act ledger."""
    acts = data.get("act")
    if not isinstance(acts, list):
        return []
    return [entry for entry in acts if isinstance(entry, dict)]


def _ledger_line(line, in_act):
    """`(line, in_act)`: one line of the act ledger with an entry's key
    respelled, and whether the lines after it belong to an `[[act]]` entry."""
    array = _ARRAY_HEADER.match(line)
    if array:
        return line, array["name"] == "act"
    if line.lstrip().startswith("["):
        return line, False
    cell = _KEY_LINE.match(line)
    if in_act and cell and cell["key"] in LEDGER_KEYS:
        return cell["lead"] + LEDGER_KEYS[cell["key"]] + cell["rest"], in_act
    return line, in_act


def migrate_ledger(text):
    """Act-ledger `text` with each entry's keys in the current vocabulary.
    Raises `Unsafe` when the result would not parse as exactly that.

    Implements: SR-247, LLR-369
    """
    return _rekeyed(text, _ledger_entries, LEDGER_KEYS, _ledger_line)


def _record_rows(text, suffix):
    """`{row id: {cell: value}}` of a registry's `text` under either carrier
    (a CSV row keyed by its first cell), `{}` when it does not parse."""
    if suffix == ".toml":
        try:
            data = tomllib.loads(text.lstrip("﻿"))
        except tomllib.TOMLDecodeError:
            return {}
        tiers = [t for t in data.values() if isinstance(t, dict)]
        return {
            rid: row for t in tiers for rid, row in t.items() if isinstance(row, dict)
        }
    offset = len(text) - len(text.lstrip("﻿"))
    offset += _csv_preamble(text[offset:])
    records = _csv_parsed(text[offset:])
    if not records:
        return {}
    return {r[0]: dict(zip(records[0], r)) for r in records[1:] if r}


def _absorbed(copy_text, live_text, suffix):
    """`[(row id, cell)]`: each cell of a row the copy holds as accepted that
    the live registry holds otherwise, the status left out; a row the live
    registry no longer holds is named once, as the whole row."""
    copy, live = _record_rows(copy_text, suffix), _record_rows(live_text, suffix)
    out = []
    for rid, row in copy.items():
        status = str(row.get("status", row.get("Status", ""))).strip().lower()
        if status not in _ACCEPTED_WORDS:
            continue
        if rid not in live:
            out.append((rid, "(the whole row)"))
            continue
        cells = (set(row) | set(live[rid])) - {"status", "Status"}
        out += [(rid, c) for c in sorted(cells) if row.get(c) != live[rid].get(c)]
    return out


def _record_copies(home):
    """`(live path, copy path)` for each registry copy in the record `home`."""
    for folder in (home / d for d in REGISTRY_DIRS):
        if not folder.is_dir():
            continue
        for path in sorted(folder.iterdir()):
            if path.is_file() and path.suffix in (".toml", ".csv"):
                yield path.relative_to(home).as_posix(), path


def _copies_owed(root, home):
    """`([(copy path, live bytes)], [report line], [problem])`: each copy in
    the record `home` that differs from its live registry, with a line for it
    and one for each accepted cell writing it would absorb, and each copy
    whose live registry is gone, which is left as it is."""
    owed, lines, problems = [], [], []
    for rel, path in _record_copies(home):
        where = "{}/{}".format(RECORD_DIRS[1], rel)
        live = root / rel
        if not live.is_file():
            problems.append(
                "{}: no live {} to write it from; left untouched".format(where, rel)
            )
            continue
        want, have = live.read_bytes(), path.read_bytes()
        if want == have:
            continue
        owed.append((path, want))
        lines.append("{} written equal to {}".format(where, rel))
        absorbed = _absorbed(have.decode("utf-8"), want.decode("utf-8"), path.suffix)
        lines += ["{} absorbs {} {}".format(rel, rid, cell) for rid, cell in absorbed]
    return owed, lines, problems


def _ledger_owed(root, home):
    """`(ledger text or None, [problem])`: the record `home`'s act ledger with
    its keys respelled, None when nothing moves, or a problem when the line
    edit cannot be proved."""
    path = home / LEDGER_NAME
    if not path.is_file():
        return None, []
    raw = path.read_bytes().decode("utf-8")
    try:
        new = migrate_ledger(raw)
    except Unsafe as exc:
        where = path.relative_to(root).as_posix()
        return None, ["{}: {}; the record is left untouched".format(where, exc)]
    return (None if new == raw else new), []


def _write_record(home, target, ledger, owed):
    """Move the record `home` to `target`, then write its ledger and copies."""
    if home != target:
        home.rename(target)
    if ledger is not None:
        (target / LEDGER_NAME).write_bytes(ledger.encode("utf-8"))
    for path, want in owed:
        (target / path.relative_to(home)).write_bytes(want)


def record(root, check):
    """The acceptance record under its earlier name moved to the current one,
    its act ledger's keys respelled, and each registry copy in it written
    equal to its live registry, naming every accepted cell that absorbs:
    `([what moved], [problem])`. Both names present, or a ledger the line
    edit cannot prove, is a problem, and nothing is touched.

    Implements: SR-247, LLR-369
    """
    old, new = (root / d for d in RECORD_DIRS)
    if old.is_dir() and new.exists():
        return [], ["{}: {} exists too; merge the two by hand".format(*RECORD_DIRS)]
    home = old if old.is_dir() else new
    if not home.is_dir():
        return [], []
    ledger, problems = _ledger_owed(root, home)
    owed, lines, missing = _copies_owed(root, home)
    if problems:
        return [], problems + missing
    done = ["{} -> {}".format(*RECORD_DIRS)] if home == old else []
    if ledger is not None:
        done.append(
            "{}/{}: keys {}".format(
                RECORD_DIRS[1],
                LEDGER_NAME,
                ", ".join("{} -> {}".format(*kv) for kv in LEDGER_KEYS.items()),
            )
        )
    if not check:
        _write_record(home, new, ledger, owed)
    return done + lines, missing


# --- links into the moved record -------------------------------------------------

# A Markdown link's target: inline, `](target)`, or a reference definition,
# `[label]: target`. Only `target` is ever rewritten.
_LINK = re.compile(
    r"(?P<lead>\]\(|^[ \t]{0,3}\[[^\]\r\n]+\]:[ \t]*)(?P<target>[^)\s]+)",
    re.M,
)
# The record's directory names, earlier and current, as one path segment.
_OLD_RECORD, _NEW_RECORD = (d.rsplit("/", 1)[1] for d in RECORD_DIRS)
_OLD_SEGMENT = re.compile(r"(?<![\w.-]){}(?![\w.-])".format(re.escape(_OLD_RECORD)))
# Folders whose Markdown is not the repository's own.
_UNWALKED = frozenset({"node_modules", "__pycache__"})


def relink_markdown(text):
    """`(text, count)`: Markdown `text` with each link target naming the
    record's earlier directory re-based onto the current one, and how many
    moved. The link text and the prose around it keep their words.

    Implements: SR-247, LLR-369
    """
    count = 0

    def rebased(match):
        nonlocal count
        target, n = _OLD_SEGMENT.subn(_NEW_RECORD, match["target"])
        count += n
        return match["lead"] + target

    return _LINK.sub(rebased, text), count


def _markdown_files(root):
    """Each `.md` file under `root`, outside hidden folders and `_UNWALKED`."""
    for folder, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d[0] != "." and d not in _UNWALKED)
        for name in sorted(files):
            if name.endswith(".md"):
                yield Path(folder) / name


def links(root, check):
    """Markdown links into the acceptance record re-based from its earlier
    directory to the current one: `([what moved], [problem])`. A file that is
    not UTF-8 is named and left untouched.

    Implements: SR-247, LLR-369
    """
    done, problems = [], []
    needle = _OLD_RECORD.encode("ascii")
    for path in _markdown_files(root):
        raw = path.read_bytes()
        if needle not in raw:
            continue
        where = path.relative_to(root).as_posix()
        try:
            text, count = relink_markdown(raw.decode("utf-8"))
        except UnicodeDecodeError:
            problems.append("{}: not UTF-8; left untouched".format(where))
            continue
        if not count:
            continue
        done.append("{}: {} link(s) into {}".format(where, count, RECORD_DIRS[1]))
        if not check:
            path.write_bytes(text.encode("utf-8"))
    return done, problems


# Each step: what it is called in the report, and the function that takes it.
# The record comes after the registries, so that the copies it writes equal
# live registries the registry step has already respelled; the links into it
# come last.
STEPS = (
    ("verdict binding", bindings),
    ("registry", registries),
    ("policy file", policy),
    ("decisions record", decisions),
    ("work item", work_items),
    ("scratchpad", scratchpad),
    ("acceptance record", record),
    ("acceptance-record link", links),
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
