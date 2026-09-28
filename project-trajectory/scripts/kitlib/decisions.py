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

THE REVIEW CELL IS THE OWNER'S, AND NOTHING READS IT. Each entry carries
`review = ""`; the owner reviews in place by writing any string there. Empty
means unreviewed and any string means reviewed, with semantics the owner's own.
No check here or anywhere judges the review state: a collator, if one is ever
built, skips entries whose `review` is not empty. The file is edited in place
and is not immutable.

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
    the owner writes a note in place. Other keys are the writer's and are not
    judged; an entry id ending `-000` is inert.

Contract IF-256: the delegated-decisions record, as a CALL. `MODES` is the
    dial's alphabet (`off`, `record`, `escalate-first`); `REQUIRED_KEYS` the
    entry's required keys; `record_path(run)` the file's repo-relative path;
    `record_findings(text)` one finding per defect IF-255 names, `[]` for a
    sound record, never raising; `owed(mode, outcomes)` whether a close under
    the dial `mode`, with at least one claimed row closed, owes a record;
    `session_note(mode, run)` the instruction a delegated session is handed,
    `""` under `off`. Pure functions of their arguments: no file, git or
    environment read.
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


def record_path(run):
    """The repo-relative path of one run's record: `DECISIONS_DIR/<run>.toml`,
    a `/` in the run's name becoming `-`.

    Implements: SR-225, LLR-283
    """
    return "{}/{}.toml".format(DECISIONS_DIR, str(run).replace("/", "-"))


def _inert(entry_id):
    return str(entry_id).endswith("-000")


def _entry_findings(entry_id, entry):
    if not _ENTRY_ID_RE.match(entry_id):
        return ["{}: an entry id is D-<number>".format(entry_id)]
    if not isinstance(entry, dict):
        return ["{}: an entry is a table of its fields".format(entry_id)]
    out = []
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
        "{keys} (leave review empty — it is the owner's), and a top-level "
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
