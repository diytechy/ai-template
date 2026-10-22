"""A disposition's ADOPTION of an already-filed successor: its block, the row it
disposes, whether a listing accepts it, and the record the close writes.

WHY THIS EXISTS (WI-969, carrying WI-902's spec of record). An early close
(partial or cancelled) must queue at least one successor (OI-70/OI-73). When
the successor was already filed, with `supersedes` naming the closed row, a
drafted one would mint a duplicate, so the disposition row ADOPTS it instead:
a fenced TOML block in its own `## Dispositions` section holding exactly one
key, `adopts = "WI-NNN"`. The adoption is the successor exit, not a third one.
The close validates it once, in the tree its closing commit is made on, and
writes the validated ids into the closed spec's `adopted` cell (the record);
the commit check and the sweep then judge that record. All three read the
request and the record through this module, so they cannot disagree about a
block, a title, a row or a record.

What the adjudicator's text may say is only WHICH row: the row the disposition
disposes is read from the disposition row's own title (`disposed_id`), the
immutable event token the mint writes and dedups on, and the adopted row is
accepted only while the listing it is judged in holds it open with
`supersedes` naming that row (`row_refusal`). Pure: the caller supplies the
listing, and nothing here reads git or a working tree or writes anything.

Contracts: IF-294 - adoption request, record and listing calls from intake,
handback and adoption_record (process.md §8; row of record in
docs/requirements/interfaces.toml).

Contract IF-294: `parse_block(data, at)`, `disposed_id(title,
    disposition=True)` and `record_ids(data, where)` return `(value,
    refusal)`; `row_refusal(specs, adopted, disposed)` judges a
    caller-supplied listing of `(relpath, read)` entries and returns a
    refusal string or None; `record_change(parents, record, request, moved,
    close, invalid)`, `parents` one `(record, request)` pair per parent,
    returns a refusal string or None for one spec's record across one
    commit. These calls parse the adoption block, the event identity and the
    record, and judge caller-supplied open specifications. They write no state and invoke no git; LLR-335 owns the
    eligibility rule and LLR-345 the commit rule they serve.
"""

import re

from .registry import parse_spec_row

__all__ = [
    "KEY",
    "RECORD_KEY",
    "OPEN_STATES",
    "parse_block",
    "disposed_id",
    "row_refusal",
    "record_ids",
    "record_change",
]

#: The one key an adoption block holds. Never a draft key: a draft mints a row,
#: and an adoption names one that already exists.
KEY = "adopts"
#: The closed spec's front-matter key the close writes the validated ids into.
RECORD_KEY = "adopted"
#: The open folders an adopted row may stand in.
OPEN_STATES = ("draft", "queued", "active")
_ID_RE = re.compile(r"WI-\d+")
#: The event token a disposition title carries: the close report
#: `<wi>-<branch>` or, for a report-less cancellation, the cancelled spec
#: `WI-NNN-<slug>.md`. Either file name leads with the disposed row's id.
_EVENT_TOKEN_RE = re.compile(r"\brecorded at (\S+)")
_LEADING_ID_RE = re.compile(r"(WI-\d+)-")


def parse_block(data, at):
    """`(adopted id, refusal)` for one parsed adoption block: exactly the one
    key, naming exactly one well-formed WI id. Shape only.

    Implements: SR-148, LLR-335"""
    extra = sorted(set(data) - {KEY})
    if extra:
        return None, (
            "{} adopts a successor beside other key(s) {} - an adoption block "
            "holds exactly one key, `{}`; nothing minted".format(at, extra, KEY)
        )
    value = data.get(KEY)
    if not isinstance(value, str) or not _ID_RE.fullmatch(value):
        return None, (
            "{} adopts {!r} - the value must be exactly one WI-### id; nothing "
            "minted".format(at, value)
        )
    return value, None


def disposed_id(title, disposition=True):
    """`(id, refusal)`: the row a disposition row disposes, read from its
    title's one event token. `disposition` is whether the title is a
    disposition row's at all; a title that is not, or whose token is absent or
    does not lead with exactly one WI id, refuses and is never guessed.

    Implements: SR-148, LLR-335"""
    title = str(title or "")
    tokens = _EVENT_TOKEN_RE.findall(title) if disposition else []
    leads = [_LEADING_ID_RE.match(tok.rsplit("/", 1)[-1]) for tok in tokens]
    ids = [m.group(1) for m in leads if m]
    if len(tokens) == 1 and len(ids) == 1:
        return ids[0], None
    return None, (
        "the title {!r} carries no single disposition event token naming one "
        "WI id, so the row an adoption continues cannot be read".format(title)
    )


def row_refusal(specs, adopted, disposed):
    """Why the listing `specs` (`[(relpath, read)]`, `relpath` from the work
    root, `read()` the spec's text) does not accept `adopted` as the
    successor of `disposed`, else None: the id names no open row, its spec
    cannot be read (or several specs carry it), or it does not supersede
    `disposed`. Distinct reasons, none of them a fallback; the rule is the same
    whichever tree the caller listed.

    Implements: SR-148, LLR-335"""
    hits = _hits(specs, adopted)
    if not hits:
        return "adopts {}, which names no open row ({})".format(
            adopted, "/".join(OPEN_STATES)
        )
    rel, read = hits[0]
    try:
        if len(hits) > 1:
            raise ValueError("{} specs carry the id".format(len(hits)))
        row, _order = parse_spec_row(read(), rel)
    except (OSError, ValueError, UnicodeDecodeError) as exc:
        return "adopts {} but cannot read its spec {} ({})".format(adopted, rel, exc)
    cell = row.get("Supersedes") or ""
    if disposed not in [tok.strip() for tok in cell.split(";")]:
        return "adopts {}, which does not supersede {} (its supersedes is {!r})".format(
            adopted, disposed, cell
        )
    return None


def _hits(specs, adopted):
    """The `(relpath, read)` entries of `specs` that carry `adopted` in an open
    state.

    Implements: SR-148, LLR-335"""
    return [
        (rel, read)
        for rel, read in specs
        if rel.split("/", 1)[0] in OPEN_STATES
        and rel.rsplit("/", 1)[-1].startswith(adopted + "-")
    ]


def record_ids(data, where):
    """`(ids, refusal)` for the `adopted` record in the parsed front matter
    `data`: `(None, None)` when the key is absent, the ids as a tuple when it
    is a non-empty list of distinct well-formed WI ids, else a refusal. The
    registry readers carry the cell as data and grant it nothing; every
    consumer that acts on the record reads it here.

    Implements: SR-148, LLR-335"""
    if RECORD_KEY not in data:
        return None, None
    value = data[RECORD_KEY]
    ids = value if isinstance(value, list) else []
    well_formed = all(isinstance(i, str) and _ID_RE.fullmatch(i) for i in ids)
    if not (ids and well_formed and len(set(ids)) == len(ids)):
        return None, (
            "{}: `{}` is {!r}, not a non-empty TOML list of distinct WI-### ids".format(
                where, RECORD_KEY, value
            )
        )
    return tuple(ids), None


def record_change(parents, record, request, moved, close, invalid):
    """The refusal for one spec's record across one commit, or None: the
    `(record, request)` pair each parent holds (`parents`), the commit's
    `record` and `request`, whether the spec `moved` into a `complete/`
    folder, whether the commit is the machinery's `close`, and the
    validation's refusal (`invalid`, None when the adoption validated).

    A record is admitted in two ways only: carried unchanged with its request
    (some parent holds the same record and the same request; a spec that
    records nothing, in a commit no parent of which recorded anything, is
    unchanged too), or written by the close's own commit onto a spec no parent
    recorded, equal to the request and validated. A spec that requests an
    adoption never moves into `complete/` without its record. Every other
    change refuses, a carried record whose request changed included.

    Implements: SR-148, LLR-345"""
    pairs = [(_ids(r), _ids(q)) for r, q in parents]
    records = [r for r, _q in pairs]
    record, request = _ids(record), _ids(request)
    if moved and request and record is None:
        return (
            "requests adoption of {} but moved into complete/ with no `{}` "
            "record".format(";".join(request), RECORD_KEY)
        )
    unrecorded = all(r is None for r in records)
    if record is None and (unrecorded or record in records):
        return None
    if record in records:
        if request and (record, request) in pairs:
            return None
        return "the `{}` record {} is carried but its request is now {}".format(
            RECORD_KEY, _shown(record), _shown(request)
        )
    if not close or record is None or not unrecorded:
        return "the `{}` record {} changed outside the machinery's close".format(
            RECORD_KEY, _shown(record)
        )
    if record != request:
        return "the `{}` record {} differs from the request {}".format(
            RECORD_KEY, _shown(record), _shown(request)
        )
    if invalid:
        return "the `{}` record {} does not validate ({})".format(
            RECORD_KEY, _shown(record), invalid
        )
    return None


def _ids(value):
    """A record or request as a tuple of ids, None for none.

    Implements: SR-148, LLR-345"""
    return tuple(value) if value else None


def _shown(ids):
    """A record or request as the text a refusal names.

    Implements: SR-148, LLR-345"""
    return ";".join(ids) if ids else "(none)"
