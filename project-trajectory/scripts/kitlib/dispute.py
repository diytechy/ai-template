"""A DISPUTE sitting: the findings file it rules, and its verdict grammar.

WHY THIS EXISTS (WI-865). A review finding the lane's builder or its
coordinator contests, or one that keeps coming back round after round, is the
adjudicator's call, not the coordinator's by sending every finding back to the
builder (the owner's ruling of 2026-10-08, rule 2); its call is final, and a
high-risk finding goes to the owner. That sitting's input is a findings file
the coordinator writes by hand, and its output a verdict ruling each finding.
Both shapes have one home, here, below the routes that use them: the
coordinator's adjudication entry point today, the loop's in-lane sitting
(WI-811) later. Pure functions over text.

Contracts: IF-290 — the seam this module declares (process.md §8; row of record
in docs/requirements/interfaces.toml).

Contract IF-290: the dispute grammar `adjudicate_brief` calls. Text in,
    values or a refusal out: no file read, no git, no process. `read_findings(
    text, where)` returns `({"range": str, "findings": [{id, held_by, finding,
    position}]}, None)` for a findings file in the shape below, else `(None,
    why)` naming `where` and the cause. `request_line(ids)` returns the brief's
    `DISPUTE: findings=<ids>` line, and `requested_ids(brief_text)` reads the
    ids back off the first such line, `()` when there is none, so the request a
    brief renders is the request its verdict is judged against. `parse(text,
    requested, where)` returns `({id: (ruling, reason class or None, reason)},
    None)` for a verdict ruling every requested finding exactly once and
    nothing else, else `(None, why)`.

THE FINDINGS FILE (TOML, every key required, no other key accepted):

    range = "<base>..<head>"     # the lane range the findings concern

    [[finding]]                  # one table per finding, in the order to rule
    id = "F1"                    # the finding's id: a letter, then letters,
                                 # digits, `.`, `_` or `-`; unique in the file
    held_by = "builder"          # whose position follows: builder | coordinator
    finding = '''
    <the finding exactly as the reviewer wrote it>
    '''
    position = '''
    <the builder's or coordinator's position on it>
    '''

THE VERDICT: exactly one `RULING:` line per requested finding, each on its own
physical line (leading indentation aside), and no other `RULING:` line:

    RULING: <id> FIX <why, on the same line>
    RULING: <id> DISMISS out-of-scope|refuted|not-worth-cost <why>
    RULING: <id> ESCALATE <why it is high risk>

`parse` is the ONE parser of that verdict. It is judged against the finding
ids the composed brief REQUESTED (its `DISPUTE: findings=<ids>` line, read by
`requested_ids`), which the entry point binds beside the verdict before the
call, so a verdict cannot choose what it rules. A missing, duplicated,
unrequested or malformed ruling refuses the whole verdict; nothing is
defaulted.
"""

import re
import tomllib

__all__ = [
    "BRIEF",
    "RULINGS",
    "DISMISS_REASONS",
    "HELD_BY",
    "read_findings",
    "request_line",
    "requested_ids",
    "parse",
]

BRIEF = "dispute"
RULINGS = ("FIX", "DISMISS", "ESCALATE")
DISMISS_REASONS = ("out-of-scope", "refuted", "not-worth-cost")
HELD_BY = ("builder", "coordinator")
# The verdict's per-finding keyword, and the composed brief's request line.
_RULING = "RULING"
_REQUEST = "DISPUTE"
_ID_RE = re.compile(r"[A-Za-z][A-Za-z0-9._-]*")
_FILE_KEYS = ("range", "finding")
_FINDING_KEYS = ("id", "held_by", "finding", "position")


def read_findings(text, where):
    """`({"range": str, "findings": [{id, held_by, finding, position}]}, None)`
    for a findings file in the declared shape, else `(None, why)`. The texts
    are kept as written, apart from the newline TOML drops after an opening
    `'''` and the blank lines around them.

    Implements: SR-234, LLR-314
    """
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return None, "{} is not TOML: {}".format(where, exc)
    why = _file_refusal(data, where)
    if why:
        return None, why
    findings = []
    for index, table in enumerate(data["finding"]):
        finding, why = _finding(table, "{} finding {}".format(where, index + 1))
        if why is None and finding["id"] in {f["id"] for f in findings}:
            why = "{} names the finding {} twice".format(where, finding["id"])
        if why:
            return None, why
        findings.append(finding)
    return {"range": data["range"].strip(), "findings": findings}, None


def _file_refusal(data, where):
    """Why the file's top level is not `range` and a non-empty `[[finding]]`
    list, or None."""
    unknown = sorted(set(data) - set(_FILE_KEYS))
    if unknown:
        return "{} carries unknown key(s) {}; the shape takes {}".format(
            where, ", ".join(unknown), ", ".join(_FILE_KEYS)
        )
    span = data.get("range")
    if not isinstance(span, str) or not span.strip():
        return "{} declares no `range`".format(where)
    tables = data.get("finding")
    if not isinstance(tables, list) or not tables:
        return "{} declares no finding".format(where)
    return None


def _finding(table, where):
    """`(finding, None)` for one `[[finding]]` table, else `(None, why)`."""
    if not isinstance(table, dict) or sorted(table) != sorted(_FINDING_KEYS):
        keys = sorted(table) if isinstance(table, dict) else table
        return None, "{} carries {}; a finding takes exactly {}".format(
            where, keys, ", ".join(_FINDING_KEYS)
        )
    fid = table["id"]
    if not isinstance(fid, str) or not _ID_RE.fullmatch(fid):
        return None, (
            "{}: id {!r} is not a letter followed by letters, digits, "
            "`.`, `_` or `-`".format(where, fid)
        )
    if table["held_by"] not in HELD_BY:
        return None, "{} ({}): held_by {!r} is not one of {}".format(
            where, fid, table["held_by"], "|".join(HELD_BY)
        )
    texts = {key: table[key] for key in ("finding", "position")}
    for key, value in texts.items():
        if not isinstance(value, str) or not value.strip():
            return None, "{} ({}): empty `{}`".format(where, fid, key)
    found = {key: value.strip("\n") for key, value in texts.items()}
    return dict(found, id=fid, held_by=table["held_by"]), None


def request_line(ids):
    """The composed brief's line naming the findings it asks ruled.

    Implements: SR-234, LLR-314
    """
    return "{}: findings={}".format(_REQUEST, ";".join(ids))


def _keyword_rests(text, keyword):
    """The text after `keyword:` on every physical line of `text` whose first
    token, leading whitespace aside, is `keyword:`. One line at a time, as
    `kitlib.sitting` reads its machine lines: nothing spans a newline."""
    out = []
    for line in (text or "").splitlines():
        head, sep, rest = line.strip().partition(":")
        if sep and head == keyword:
            out.append(rest.strip())
    return out


def requested_ids(brief_text):
    """The finding ids a composed dispute brief requested, read off its FIRST
    `DISPUTE: findings=<ids>` line (the template puts it before any finding's
    text); () when it carries none.

    Implements: SR-234, LLR-314
    """
    for rest in _keyword_rests(brief_text, _REQUEST)[:1]:
        key, sep, value = rest.partition("=")
        if sep and key.strip() == "findings":
            return tuple(i for i in value.strip().split(";") if i)
    return ()


def _one_ruling(rest, where):
    """`((id, ruling, reason class or None, reason), None)` for one
    `RULING:` line's text after the keyword, else `(None, why)`."""
    tokens = rest.split()
    if len(tokens) < 2:
        return (
            None,
            "{}: a `RULING:` line names a finding id and a ruling; "
            "this one reads {!r}".format(where, rest),
        )
    fid, ruling, words = tokens[0], tokens[1], tokens[2:]
    if ruling not in RULINGS:
        return None, "{}: `RULING: {} {}` - the ruling is not one of {}".format(
            where, fid, ruling, "|".join(RULINGS)
        )
    reason = None
    if ruling == "DISMISS":
        if not words or words[0] not in DISMISS_REASONS:
            return None, "{}: `RULING: {} DISMISS` names no reason class ({})".format(
                where, fid, "|".join(DISMISS_REASONS)
            )
        reason, words = words[0], words[1:]
    if not words:
        return None, "{}: `RULING: {} {}` gives no reason on its line".format(
            where, fid, ruling
        )
    return (fid, ruling, reason, " ".join(words)), None


def parse(text, requested, where=""):
    """THE ONE PARSER: `({id: (ruling, reason class or None, reason)}, None)`
    for a verdict ruling every `requested` finding exactly once and nothing
    else, else `(None, why)`.

    Implements: SR-234, LLR-314
    """
    if not requested:
        return (
            None,
            "{}: a dispute verdict is judged against the findings its "
            "brief requested, and none were given".format(where),
        )
    rulings = {}
    for rest in _keyword_rests(text, _RULING):
        ruled, why = _one_ruling(rest, where)
        if why is None and ruled[0] in rulings:
            why = "{}: rules the finding {} twice".format(where, ruled[0])
        if why is None and ruled[0] not in requested:
            why = "{}: rules {}, which the brief did not request ({})".format(
                where, ruled[0], ";".join(requested)
            )
        if why:
            return None, why
        rulings[ruled[0]] = ruled[1:]
    unruled = [fid for fid in requested if fid not in rulings]
    if unruled:
        return None, "{}: leaves unruled {} (one `RULING:` line per finding)".format(
            where, ";".join(unruled)
        )
    return rulings, None
