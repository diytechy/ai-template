# --- the delegated-decisions records -------------------------------------------

# A delegated run's record: `docs/decisions/<run>.toml`, one `[decision.<id>]`
# table per entry. The operator's verdict on an entry was keyed `owner`.
DECISIONS_DIR = "docs/decisions"
DECISION_KEYS = {"owner": "operator"}

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
        before = tomllib.loads(text.lstrip("﻿"))
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
        after = tomllib.loads(new.lstrip("﻿"))
    except tomllib.TOMLDecodeError:
        after = None
    if after != expected:
        raise Unsafe("a rewrite of it would change more than the vocabulary")
    return new


def decisions(root, check):
    """Each delegated-decisions record whose entries carry a key by an earlier
    name, rewritten: `([repo-relative path], [problem])`.

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


# --- the operator's scratchpad ---------------------------------------------------

# The root notes file of the person in charge, by its earlier and current name.
# Seven scripts protect it by its current name, so a file left under the
# earlier one would lose that protection without a word. It is renamed, never
# opened: it holds a person's private notes.
SCRATCHPAD_NAMES = ("OWNER_SCRATCHPAD.md", "OPERATOR_SCRATCHPAD.md")


def scratchpad(root, check):
    """The scratchpad under its earlier name, renamed to the current one:
    `([repo-relative path], [problem])`. Both names present is a problem,
    left for the operator to merge.

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
    return [SCRATCHPAD_NAMES[0]], []
