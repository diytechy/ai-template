"""A `single` row's plan records: the plan, its filed critiques and its pass
record, in one grammar with one reader (WI-913).

WHY THIS EXISTS. A row the scope critique marks `planmode = "single"` builds
only after its in-lane plan passes the coverage gate and an independent
critique. The pass is a FILE the filing step writes (`review_brief.py
plan-file --pass`) and the gate reads at the commit (`plan_gate.py`), so the
two must agree on what a record says and what it binds. This module is that
agreement, stated once: the record's grammar (`parse`, `render`), its digests
(`bytes_digest`, the plan's exact bytes; `kitlib.done_when.digest`, the
Done-when the plan was gated against), and the one reader of each input a
record binds, at a commit or the index (`blob`, `plan_digest`,
`done_when_digest`, `gate_rows`). It decides nothing about a commit; the gate
does, through these readers.

THE HOMES. Everything a plan step writes sits under `docs/plans/<WI>/`: the
plan (`plan.md`), each filed critique (`critique-1.md`, and after the one
allowed revision `critique-2.md`) and the pass record (`pass.toml`).

WHAT A RECORD BINDS. The work item id, the plan's exact bytes and the
Done-when digest, each compared by CONTENT, so a rebase keeps a binding and a
plan or Done-when edited after the record unbinds it. A tick or evidence on a
Done-when item does not move its digest (`kitlib.done_when.digest`). It also
names the critique it rests on (path, content digest, and the full commit the
critique reviewed) and, at the cap, the dispute verdict that dismissed the
critique's blocking findings.

THE PLANMODE IT GATES ON is read from the CLAIM COPY (`gate_rows`): the spec
under `docs/work/active/<branch>/` at the lane's claim base, so a lane that
edits its own `planmode` changes nothing. `single` is gated; absent, empty,
`none` and `dual` are not; any other value holds, naming it, and so does a
value that is not a string (a raw `false`, `0`, `[]` or `{}`).

Every reader fails closed: an unreadable git read or a decode failure is a
reason, never an absence.

The record's format is declared with the filing step's command line
(`review_brief.py`) and the gate's (`plan_gate.py`).
"""

import hashlib
import re
import tomllib

from . import done_when as _kdone
from .git import git_bytes, git_out
from .registry import parse_spec_frontmatter

__all__ = [
    "PLANS",
    "PLAN",
    "PASS",
    "MAX_CRITIQUES",
    "SINGLE",
    "UNGATED",
    "DELTAS",
    "PASSING_DELTAS",
    "FIELDS",
    "plan_dir",
    "plan_path",
    "record_path",
    "critique_path",
    "critique_round",
    "bytes_digest",
    "delta",
    "parse",
    "render",
    "blob",
    "plan_digest",
    "done_when_digest",
    "planmode",
    "gate_rows",
]

PLANS = "docs/plans"
PLAN = "plan.md"
PASS = "pass.toml"
# One critique, then at most one revision judged by a second, fresh critique.
MAX_CRITIQUES = 2
SINGLE = "single"
# The planmode values this gate does not hold (absent reads as "").
UNGATED = ("", "none", "dual")
DELTAS = ("none", "within", "beyond")
PASSING_DELTAS = ("none", "within")
# The pass record's keys, every one required; the dispute pair is empty unless
# the record rests on a dispute sitting at the cap.
FIELDS = (
    "wi",
    "plan",
    "done_when",
    "critique",
    "critique_digest",
    "reviewed",
    "delta",
    "dispute",
    "dispute_digest",
)
_WI_RE = re.compile(r"^WI-\d+$")
_FULL_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
_DW_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{16}$")
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
# Only the rounds the cap allows are critique paths: a third is no record.
_CRITIQUE_RE = re.compile(r"^critique-([1-{}])\.md$".format(MAX_CRITIQUES))
_DELTA_RE = re.compile(r"^\s*DELTA:(.*)$")
_HEADER = (
    "# The plan gate's pass record (written by `review_brief.py plan-file "
    "--pass`;\n# read by `plan_gate.py`). Never edit it by hand: an edit "
    "unbinds it.\n"
)


def plan_dir(wi):
    """`docs/plans/<WI>`, the one home of a row's plan records.

    Implements: SR-154, LLR-337
    """
    return "{}/{}".format(PLANS, wi)


def plan_path(wi):
    """The plan's repo-relative path.

    Implements: SR-154, LLR-337
    """
    return "{}/{}".format(plan_dir(wi), PLAN)


def record_path(wi):
    """The pass record's repo-relative path.

    Implements: SR-154, LLR-337
    """
    return "{}/{}".format(plan_dir(wi), PASS)


def critique_path(wi, n):
    """The `n`th filed critique's repo-relative path.

    Implements: SR-154, LLR-337
    """
    return "{}/critique-{}.md".format(plan_dir(wi), n)


def critique_round(wi, path):
    """The round `n` of a filed critique path under `wi`'s plan home, or None
    for any other path.

    Implements: SR-154, LLR-337
    """
    head, _sep, name = str(path).rpartition("/")
    found = _CRITIQUE_RE.match(name)
    return int(found.group(1)) if found and head == plan_dir(wi) else None


def bytes_digest(data):
    """`sha256:<64 hex>` over exact bytes: a plan's, a critique's, a verdict's.

    Implements: SR-154, LLR-337
    """
    return "sha256:" + hashlib.sha256(data).hexdigest()


def delta(text):
    """`(value, None)` for a plan carrying exactly one `DELTA:` line whose
    value is in `DELTAS`, else `(None, why)`: the architectural-delta answer
    on its typed line (Q8), never read out of prose.

    Implements: SR-154, LLR-337
    """
    found = [m.group(1).strip() for m in map(_DELTA_RE.match, text.splitlines()) if m]
    if len(found) != 1:
        return None, "the plan carries {} `DELTA:` lines, not one".format(len(found))
    if found[0] not in DELTAS:
        return None, "its `DELTA: {}` is not one of {}".format(
            found[0], "|".join(DELTAS)
        )
    return found[0], None


def _field_problem(key, value):
    """Why one record value is outside its grammar, or None."""
    rules = {
        "wi": _WI_RE,
        "plan": _FULL_DIGEST_RE,
        "done_when": _DW_DIGEST_RE,
        "critique_digest": _FULL_DIGEST_RE,
        "reviewed": _SHA_RE,
    }
    if not isinstance(value, str):
        return "{} is not a string".format(key)
    if key in rules and not rules[key].match(value):
        return "{} = {!r} is outside its grammar".format(key, value)
    if key == "delta" and value not in PASSING_DELTAS:
        return "delta = {!r} is not one of {}".format(value, "|".join(PASSING_DELTAS))
    return None


def parse(text):
    """`(fields, None)` for a pass record in the grammar, else `(None, why)`:
    exactly the `FIELDS` keys, each in its grammar; the critique a filed one
    under the record's own plan home; the dispute pair both empty or both
    set. A partial write fails here, and every reader holds on it.

    Implements: SR-154, LLR-337
    """
    try:
        data = tomllib.loads(text or "")
    except tomllib.TOMLDecodeError as exc:
        return None, "the record is not valid TOML: {}".format(exc)
    if set(data) != set(FIELDS):
        return None, "the record's keys are not exactly {}".format(", ".join(FIELDS))
    why = next(filter(None, (_field_problem(k, data[k]) for k in FIELDS)), None)
    if why is None and critique_round(data["wi"], data["critique"]) is None:
        why = "critique {!r} is not a filed critique of {}".format(
            data["critique"], data["wi"]
        )
    if why is None and bool(data["dispute"]) != bool(data["dispute_digest"]):
        why = "dispute and dispute_digest are not both set or both empty"
    if why is None and data["dispute_digest"]:
        why = _field_problem("critique_digest", data["dispute_digest"])
    return (None, why) if why else (data, None)


def render(fields):
    """The record's text for `fields`, refused (ValueError) unless it reads
    back through `parse` as the same fields: the writer goes through the
    reader's grammar.

    Implements: SR-154, LLR-337
    """
    body = "".join('{} = "{}"\n'.format(k, fields.get(k, "")) for k in FIELDS)
    data, why = parse(body)
    if why or data != {k: fields.get(k, "") for k in FIELDS}:
        raise ValueError("the pass record is not written: {}".format(why))
    return _HEADER + body


def blob(root, rev, rel):
    """`(bytes, None)` for `rel` at the commit `rev` (None: the index);
    `(None, None)` when the tree does not hold it (ABSENT); `(None, why)` when
    git cannot read it or its listing (UNREADABLE).

    Implements: SR-154, LLR-337
    """
    at = "" if rev is None else rev
    data = git_bytes(root, ["show", "{}:{}".format(at, rel)])
    if data is not None:
        return data, None
    args = ["ls-files", "--"] if rev is None else ["ls-tree", "--name-only", rev, "--"]
    listed = git_out(root, args + [rel])
    if listed is None or listed.strip():
        return None, "{} cannot be read at {}".format(rel, str(rev or "the index")[:10])
    return None, None


def plan_digest(root, rev, wi):
    """`(digest, delta, None)` for `wi`'s plan at `rev` (None: the index), or
    `(None, None, why)`: no plan, an unreadable one, or one whose `DELTA:`
    line is missing or outside its set.

    Implements: SR-154, LLR-337
    """
    data, why = blob(root, rev, plan_path(wi))
    if data is None:
        return None, None, why or "no plan at {}".format(plan_path(wi))
    try:
        value, why = delta(data.decode("utf-8"))
    except UnicodeDecodeError:
        return None, None, "{} is not UTF-8".format(plan_path(wi))
    return bytes_digest(data), value, why


def done_when_digest(root, rev, branch, wi, claimed):
    """`(digest, None)` for `wi`'s Done-when in the lane's tree at `rev`
    (None: the index) against its claimed text, or `(None, why)`.

    Implements: SR-154, LLR-337
    """
    _path, text, why = _kdone.spec_at(root, rev, branch, wi)
    if text is None:
        return None, why or "no copy of {}'s spec in the lane".format(wi)
    return _kdone.digest(wi, claimed, text), None


def planmode(text, where):
    """`(mode, None)`: a spec's `planmode`, stripped and lowercased ("" when
    the key is absent), or `(None, why)` when its frontmatter cannot be read
    or the value is not a string. The raw TOML value is judged here, at its
    one reader, so a `false`, `0`, `[]` or `{}` is outside the set by name and
    never collapses into the ungated empty value.

    Implements: SR-154, LLR-337
    """
    try:
        meta, _body = parse_spec_frontmatter(text, where)
    except ValueError as exc:
        return None, "its claim copy cannot be read ({})".format(exc)
    raw = meta.get("planmode", "")
    if not isinstance(raw, str):
        return (
            None,
            "planmode {!r} is not a string, so it is outside the set "
            "(none, single, dual)".format(raw),
        )
    return raw.strip().lower(), None


def gate_rows(root, claim_rev, branch):
    """`(rows, claimed, holds)` for the lane `branch`, read off its claim
    copies under `docs/work/active/<branch>/` at `claim_rev`: `rows` the
    `[(wi, claim text)]` whose `planmode` is `single`; `claimed` every claimed
    row's id (whose plan home and spec are record homes); `holds` one reason
    per claim copy that cannot be read or declares a value outside the set.
    No claim copies (trunk, or a lane cut by hand) gates nothing.

    Implements: SR-154, LLR-337
    """
    folder = "docs/work/active/{}/".format(branch)
    if not claim_rev:
        return [], [], ["the claim copies under {} cannot be read".format(folder)]
    listing = git_out(root, ["ls-tree", "-r", "--name-only", claim_rev, "--", folder])
    if listing is None:
        return [], [], ["{} cannot be read at {}".format(folder, claim_rev[:10])]
    rows, claimed, holds = [], [], []
    for rel in sorted(listing.splitlines()):
        wi = re.match(r"^(WI-\d+)-[^/]*\.md$", rel[len(folder) :])
        if not wi:
            continue
        claimed.append(wi.group(1))
        text = git_out(root, ["show", "{}:{}".format(claim_rev, rel)])
        mode, why = (
            planmode(text, rel)
            if text is not None
            else (None, "its claim copy cannot be read ({})".format(rel))
        )
        if mode is None:
            holds.append("{}: {}".format(wi.group(1), why))
        elif mode == SINGLE:
            rows.append((wi.group(1), text))
        elif mode not in UNGATED:
            holds.append(
                "{}: planmode {!r} is outside the set (none, single, dual)".format(
                    wi.group(1), mode
                )
            )
    return rows, claimed, holds
