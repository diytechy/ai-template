"""The DELEGATED-DECISIONS RECORD: what one delegated run tells the owner about
the calls it made on the owner's behalf — its path, its format, which closes
owe one, and the note a delegated session is handed.

WHY A RECORD AND NOT AN EXIT (SR-225). A delegated session decides things the
owner would want a second look at: too settled for a pending open item, which
blocks by design, and not settled enough for the log, which records settled
decisions. Such calls had no home, and a prose "decisions for review" file
degraded within one session: the fields it asked for were left out as soon as
nothing read them. So the record is structural — one table per decision, each
carrying four REQUIRED disclosure fields — and it is a RECORD of calls already
made, never a route for work: a call the owner must make, or an act that cannot
be undone, still goes to the owner through the process's exits.

ONE FILE PER RUN (`DECISIONS_DIR/<run>.toml`), named by the lane's branch, so
two lanes never write one file and the directory is never a merge-conflict
surface, the way the log's per-branch fragments are not. A branch name's `/`
becomes `-`, so a run is always ONE file and never a directory.

THE OWNER'S VERDICT IS ONE KEY, AND AN OVERRULE IS ACTED ON (WI-818). A
decision is a direction already taken, so the owner does not approve it: the
owner CONFIRMS it or OVERRULES it (owner, 2026-10-04). Each entry may carry
`owner`, set in place to `confirmed` or `overruled`; an absent key is NOT YET
SEEN. `owner_state` is the one reading, and any other value reads as not yet
seen AND is a format finding, so a typo never hides a decision. The retired
`reviewed` key (WI-790) is a format finding wherever it appears and is never
read beside `owner`: the migrator (`migrate_text`, run by
`migrate_decisions.py`) rewrites it, and no reader keeps a legacy path. An
overrule states the direction instead in the `review` note, so an overruled
entry with a blank note is a finding. The generated owner surface lists every
entry not yet seen under "Decisions to review" and every overruled entry
under its own heading beside the work item citing it (`review_queue`).

An overrule is coupled to work at the COMMIT, the way a ruled open item is
coupled to its citing row (OI-102 Q3): the commit that sets an entry
`overruled` files or amends, in the same diff, a queued or active work item
whose spec cites the entry as `docs/decisions/<run>.toml#D-NNN` (`citation`,
`citations`, `newly_overruled`; the two-tree read is the ruling sync's, in
`acceptance_record`). Amending the queued row the decision was scoped to is
enough; nothing has to be minted. Who sets the key stays a convention: git
cannot tell the owner's commit from an agent's without a marker, which the
owner has ruled out.

WHAT IS JUDGED, AND HOW LOUDLY. The merge slot refuses a close that OWES a
record and carries none (`owed`), because a missing record is silence about
every call the run made. Every close owes one, a partial close included: a lane
the machinery closed with no session present is refused too, and the refusal is
a hold for a person to write the record. A malformed entry — a missing or blank
disclosure field, a non-text value, a hoist naming an entry the record lacks —
is REPORTED and never refused (`record_findings`): the record exists, the owner
can read what is there, and refusing the merge over one field would strand
finished work for a reporting defect. An entry numbered `-000` is the template's
example and is never judged, so the template stays copy-ready.

A kitlib module: stdlib only, importing nothing.

Contracts: IF-255, IF-256 — the seams this module declares (process.md §8; rows
of record in docs/requirements/interfaces.toml).

Contract IF-255: the delegated-decisions record, as a FILE. One TOML file per
    delegated run at `docs/decisions/<run>.toml`, a `/` in the run's name
    becoming `-`, committed on the lane's branch by the session that made the
    calls and read off that branch's tree by the merge slot. A top-level
    `high_risk` list of entry ids names the entries the writer judges deserve
    the owner's eyes first (empty when none). Each decision is a table
    `[decision.D-<digits>]` carrying `decided`, `alternative`, `reversal_cost`
    and `why_not_escalated` as non-blank text and `review` as text, empty until
    the owner writes a note in place, and may carry `owner`, the owner's
    verdict: `confirmed` or `overruled`, absent meaning not yet seen
    (`owner_state` reads it). An overruled entry's `review` note states the
    direction instead and is not blank. `reviewed` is retired: a format
    finding wherever it appears, never read. A work item cites an entry as
    `docs/decisions/<run>.toml#D-<digits>`. Other keys are the writer's and
    are not judged; an entry id ending `-000` is inert.

Contract IF-256: the delegated-decisions record, as a CALL. `MODES` is the
    dial's alphabet (`off`, `record`, `escalate-first`); `REQUIRED_KEYS` the
    entry's required keys; `record_path(run)` the file's repo-relative path;
    `record_findings(text)` one finding per defect IF-255 names, `[]` for a
    sound record, never raising; `owed(mode, outcomes)` whether a close under
    the dial `mode`, with at least one claimed row closed, owes a record;
    `session_note(mode, run)` the instruction a delegated session is handed,
    `""` under `off`; `owner_state(value)` `confirmed`, `overruled`, `""` for
    the absent key (not yet seen), or None for a value it does not recognize;
    `review_queue(text)` the entries not yet seen and the entries overruled,
    each high-risk first, and the count confirmed; `citation(rel, entry_id)`
    the token a work item cites an entry by and `citations(text)` every such
    token in a text; `newly_overruled(before, after)` the entries overruled in
    `after` and not in `before`; `migrate_text(text)` the record with the
    retired key rewritten, and the ids it could not rewrite. Pure functions of
    their arguments: no file, git or environment read.
"""

import re
import tomllib

# Where the records live, repo-relative.
# Implements: SR-225, LLR-283
DECISIONS_DIR = "docs/decisions"

# The `[attestation] decision_recording` alphabet, in order of how much it asks:
# no obligation; a delegated run's close owes the record; and, beyond recording,
# prefer the process's exits over deciding.
# Implements: SR-225, LLR-283
MODES = ("off", "record", "escalate-first")

# The keys every entry carries. The first four are the DISCLOSURE, and must say
# something; `review` is the owner's cell, empty until the owner writes in it.
# Implements: SR-225, LLR-283
REQUIRED_KEYS = (
    "decided",
    "alternative",
    "reversal_cost",
    "why_not_escalated",
    "review",
)
_DISCLOSURE = REQUIRED_KEYS[:4]

_ENTRY_ID_RE = re.compile(r"^D-\d+$")

# The owner's verdict (WI-818; the owner, 2026-10-04: a decision is "either
# confirmed by the user or overruled (or empty / ignored)"). Exact words: the
# vocabulary is closed and the migrator writes it, so any other value is a
# format finding and reads as not yet seen.
# Implements: SR-225, LLR-283
OWNER_KEY = "owner"
CONFIRMED = "confirmed"
OVERRULED = "overruled"
OWNER_VALUES = (CONFIRMED, OVERRULED)

# WI-790's key, retired by WI-818: a format finding wherever it appears, never
# read as a verdict. `migrate_text` is the one place its vocabulary survives.
# Implements: SR-225, LLR-283
RETIRED_KEY = "reviewed"
_RETIRED_TRUE = frozenset({"true", "yes", "y", "1", "reviewed", "done"})
_RETIRED_FALSE = frozenset({"false", "no", "n", "0", ""})

# How a work item cites one entry: the record's repo-relative path, `#`, and
# the entry id, a digit never following (so `#D-01` does not match `#D-012`).
_CITATION_RE = re.compile(r"(docs/decisions/[\w.-]+?\.toml)#(D-\d+)(?!\d)")


def record_path(run):
    """The repo-relative path of one run's record: `DECISIONS_DIR/<run>.toml`,
    a `/` in the run's name becoming `-`.

    Implements: SR-225, LLR-283
    """
    return "{}/{}.toml".format(DECISIONS_DIR, str(run).replace("/", "-"))


def _inert(entry_id):
    return str(entry_id).endswith("-000")


def owner_state(value):
    """The owner's verdict on one entry: `CONFIRMED`, `OVERRULED`, `""` for
    the absent key (`None` as the argument: not yet seen), or None for a value
    the `owner` key does not recognize (which the caller reads as not yet seen
    and reports).

    Implements: SR-225, LLR-283
    """
    if value is None:
        return ""
    if isinstance(value, str) and value in OWNER_VALUES:
        return value
    return None


def _owner_findings(entry_id, entry):
    """The verdict's findings for one entry: an unrecognized `owner`, the
    retired key, and an overrule with no stated direction.

    Implements: SR-225, LLR-283
    """
    out = []
    state = owner_state(entry.get(OWNER_KEY))
    if state is None:
        out.append(
            "{}: `{}` = {!r} is not `{}` or `{}`, so the entry reads as not "
            "yet seen".format(
                entry_id, OWNER_KEY, entry.get(OWNER_KEY), CONFIRMED, OVERRULED
            )
        )
    if RETIRED_KEY in entry:
        out.append(
            "{}: `{}` is retired and never read; the entry reads by `{}` alone "
            "(migrate_decisions.py rewrites it)".format(
                entry_id, RETIRED_KEY, OWNER_KEY
            )
        )
    if state == OVERRULED and not str(entry.get("review") or "").strip():
        out.append(
            "{}: overruled with a blank `review`: an overrule states the "
            "direction instead in the note".format(entry_id)
        )
    return out


def _entry_findings(entry_id, entry):
    if not _ENTRY_ID_RE.match(entry_id):
        return ["{}: an entry id is D-<number>".format(entry_id)]
    if not isinstance(entry, dict):
        return ["{}: an entry is a table of its fields".format(entry_id)]
    out = _owner_findings(entry_id, entry)
    for key in REQUIRED_KEYS:
        value = entry.get(key)
        if value is None:
            out.append("{}: no `{}`".format(entry_id, key))
        elif not isinstance(value, str):
            out.append("{}: `{}` is not text".format(entry_id, key))
        elif key in _DISCLOSURE and not value.strip():
            out.append("{}: `{}` is blank".format(entry_id, key))
    return out


def record_findings(text):
    """Every defect in one record's text, as findings naming the entry and the
    field — `[]` for a sound record. Never raises.

    Implements: SR-225, LLR-283
    """
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return ["the record does not parse as TOML ({})".format(exc)]
    entries = data.get("decision", {})
    if not isinstance(entries, dict):
        return ["`decision` is not a table of entries"]
    out = []
    for entry_id, entry in entries.items():
        if not _inert(entry_id):
            out.extend(_entry_findings(entry_id, entry))
    hoist = data.get("high_risk")
    if not isinstance(hoist, list) or not all(isinstance(h, str) for h in hoist):
        out.append(
            "no top-level `high_risk` list of entry ids (empty when no entry "
            "deserves the owner's eyes first)"
        )
        return out
    out.extend(
        "`high_risk` names {}, which the record does not carry".format(h)
        for h in hoist
        if h not in entries and not _inert(h)
    )
    return out


def _entries(data):
    """`(entries, hoisted ids)` of a parsed record: `-000` and non-table
    entries dropped, `({}, set())` when it carries no table of entries.

    Implements: SR-225, LLR-283
    """
    entries = data.get("decision")
    if not isinstance(entries, dict):
        return {}, set()
    hoist = data.get("high_risk")
    # A malformed hoist is `record_findings`' to report; the queue still lists
    # every entry, so the owner page shows the finding beside them.
    hoisted = (
        {h for h in hoist if isinstance(h, str)} if isinstance(hoist, list) else set()
    )
    kept = {
        eid: e for eid, e in entries.items() if not _inert(eid) and isinstance(e, dict)
    }
    return kept, hoisted


def _parsed(text):
    """`_entries` of a record's text, `({}, set())` when it does not parse."""
    try:
        return _entries(tomllib.loads(text or ""))
    except tomllib.TOMLDecodeError:
        return {}, set()


def review_queue(text):
    """`(unseen, overruled, confirmed)` for one record's text: the entries NOT
    YET SEEN (an absent or unrecognized `owner`) and the entries OVERRULED,
    each `{"id", "high_risk", "fields", "owner"}` (`fields` the entry's table,
    `owner` the raw value), each list the record's `high_risk` entries first
    and then id order; and how many entries are confirmed. A `-000` entry is
    never listed or counted, and a text that does not parse lists nothing
    (`record_findings` reports it). Never raises.

    Implements: SR-225, LLR-283
    """
    entries, hoisted = _parsed(text)
    unseen, overruled, confirmed = [], [], 0
    for entry_id, entry in entries.items():
        state = owner_state(entry.get(OWNER_KEY))
        if state == CONFIRMED:
            confirmed += 1
            continue
        shown = {
            "id": entry_id,
            "high_risk": entry_id in hoisted,
            "fields": entry,
            "owner": entry.get(OWNER_KEY),
        }
        (overruled if state == OVERRULED else unseen).append(shown)
    for listed in (unseen, overruled):
        listed.sort(key=lambda e: (not e["high_risk"], _id_number(e["id"])))
    return unseen, overruled, confirmed


def citation(rel, entry_id):
    """The token a work item cites one entry by: `<record path>#<entry id>`,
    e.g. `docs/decisions/wi-818.toml#D-002`.

    Implements: SR-225, LLR-283
    """
    return "{}#{}".format(rel, entry_id)


def citations(text):
    """Every entry a text cites, as the set of its `citation` tokens.

    Implements: SR-225, LLR-283
    """
    return {citation(m.group(1), m.group(2)) for m in _CITATION_RE.finditer(text or "")}


def _overruled_ids(text):
    entries, _hoisted = _parsed(text)
    return {
        eid for eid, e in entries.items() if owner_state(e.get(OWNER_KEY)) == OVERRULED
    }


def newly_overruled(before, after):
    """The entry ids overruled in the record text `after` and not in `before`
    (either None or "" for a record absent on that side), in id order. A side
    that does not parse overrules nothing, so an overrule hidden behind a
    syntax error is owed by the commit that makes it readable.

    Implements: SR-225, LLR-283
    """
    return sorted(_overruled_ids(after) - _overruled_ids(before), key=_id_number)


# A table header, the one shape `migrate_text` reads entry ids from; any
# other header ends the entry.
_TABLE_RE = re.compile(r"^\s*\[\s*decision\.([^\]\s]+)\s*\]")
_HEADER_RE = re.compile(r"^\s*\[")
_RETIRED_LINE_RE = re.compile(r"^(\s*)reviewed\s*=")


def _retired_verdict(value):
    """The retired key's reading, kept for the migrator alone: True, False, or
    None for a value outside its vocabulary.

    Implements: SR-225, LLR-304
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    word = value.strip().lower() if isinstance(value, str) else None
    if word in _RETIRED_TRUE:
        return True
    if word in _RETIRED_FALSE:
        return False
    return None


def _migrated_line(entry, line):
    """What one `reviewed = ...` line becomes: `owner = "confirmed"` for a
    reviewed value, "" (dropped) for a not-reviewed one or beside an `owner`
    key already set, and None (kept) for a value outside the retired
    vocabulary.

    Implements: SR-225, LLR-304
    """
    if OWNER_KEY in entry:
        return ""
    verdict = _retired_verdict(entry.get(RETIRED_KEY))
    if verdict is None:
        return None
    if not verdict:
        return ""
    ending = line[len(line.rstrip("\r\n")) :]
    indent = _RETIRED_LINE_RE.match(line).group(1)
    return '{}{} = "{}"{}'.format(indent, OWNER_KEY, CONFIRMED, ending)


def migrate_text(text):
    """`(new_text, left)`: one record with the retired key rewritten in place —
    `reviewed = true` (or any word that read as reviewed) becomes
    `owner = "confirmed"`, a not-reviewed value is dropped, and every other
    line, each `review` note and every comment included, is kept byte for
    byte — and the ids whose value is outside the retired vocabulary, left as
    they are (still a format finding). Idempotent. Raises `ValueError` for a
    text that does not parse as TOML.

    Implements: SR-225, LLR-304
    """
    try:
        entries, _hoisted = _entries(tomllib.loads(text))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError("the record does not parse as TOML ({})".format(exc))
    out, left, current = [], [], None
    for line in text.splitlines(keepends=True):
        table = _TABLE_RE.match(line)
        if table or _HEADER_RE.match(line):
            current = table.group(1) if table else None
        elif current in entries and _RETIRED_LINE_RE.match(line):
            new = _migrated_line(entries[current], line)
            if new is None:
                left.append(current)
            else:
                line = new
        out.append(line)
    return "".join(out), left


def _id_number(entry_id):
    tail = str(entry_id).rsplit("-", 1)[-1]
    return int(tail) if tail.isdigit() else 0


def owed(mode, outcomes):
    """Does a close owe a record — the dial at `record` or `escalate-first`,
    and at least one claimed row closed. EVERY close owes one, a partial close
    included: every delegated run closes with its record. A lane the machinery
    closed partial with no session present is therefore refused too, and that
    refusal is a hold for a person to write the record, never a strand.

    Implements: SR-225, LLR-283
    """
    return str(mode) in MODES[1:] and bool(list(outcomes or ()))


def session_note(mode, run):
    """The instruction a delegated session is handed under a recording dial, or
    `""` under `off`. It names the exact path, so the session is told where its
    record belongs rather than asked to derive it.

    Implements: SR-225, LLR-283
    """
    if str(mode) not in MODES[1:]:
        return ""
    note = (
        "\n\nDECISIONS RECORD (docs/process.toml [attestation] "
        'decision_recording = "{mode}"): this run owes one record of the calls '
        "it made on the owner's behalf, at {path} — the format and the routing "
        'rules are the process options\' "Delegated decisions record" layer. '
        "Write one [decision.D-<n>] table per call that touched a registry, the "
        "spine or a kit file, or that you are unsure of, each carrying "
        "{keys} (leave review empty and set no owner key — the owner "
        'confirms or overrules each entry in place: owner = "confirmed" or '
        '"overruled"), and a top-level '
        "high_risk list naming the entries the owner should read first (empty "
        "when none). The record is not an exit: a call that is the owner's to "
        "make, or an act that cannot be undone, still goes to the owner through "
        "the process's exits, never only into this file. Commit it on this "
        "branch before your close commit, even with no entries: a lane that "
        "closes its work without it is refused at the merge."
    ).format(mode=mode, path=record_path(run), keys=", ".join(REQUIRED_KEYS))
    if str(mode) == "escalate-first":
        note += (
            " The dial is at escalate-first: where a call could go either way, "
            "prefer the exits over deciding it yourself."
        )
    return note
