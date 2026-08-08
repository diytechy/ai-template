#!/usr/bin/env python3
"""outcome.py — an attempt's own identity: the frozen scope, the immutable
record, and the classification a partial attempt owes before it may land.

Every return-handling defect this kit has paid for shares one cause: **the
attempt had no identity of its own.** The outcome was a fact somebody derived —
from a folder, from a commit subject, from a reason string — so each consumer
derived its own and no two derivations agreed. This module removes the
derivation. An attempt writes ONE event, keyed by content, into an append-only
ledger outside `docs/work/`, and everything downstream reads that event rather
than re-inferring one (decisions D-3, SR-149).

Four things live here, and each closes a specific hole:

  scope_digest      WHAT THE BRANCH MAY NOT EDIT. A branch that can narrow its
                    own scope to whatever it managed to finish makes every
                    completion claim unfalsifiable, because the obligation and
                    the delivery have the same author. The digest covers the
                    identity, the references, the predecessors and the
                    classification cells plus the body sections that state the
                    obligation — and deliberately NOT the `## Deliverable`
                    section, which is exactly what an honest close writes.

  write_outcome     ONE EVENT PER ATTEMPT, and no second one. The id is the
                    first 16 hex of the SHA-256 of the canonical payload with
                    `id`/`ts` removed (contracts §2), so observing the same
                    facts twice is not two events and any holder of the payload
                    can re-derive the id rather than trusting the ledger. The
                    schema is CLOSED: an unknown field is a refusal, so there is
                    no free-form slot where an instruction could ride in wearing
                    a fact's clothes. A rationale is one delimited string value,
                    never prose the reader could mistake for policy.

  classify_groups   THE 2026-08-03 INCIDENT (`08e6c08a`), mechanised. A returned
                    branch merged green and landed rejected code as-is, because
                    nothing forced anyone to say which of its changes were
                    wanted. Requiring a keep/discard/quarantine label per change
                    group moves that decision into the open, before the merge,
                    where an adjudicator makes it — instead of leaving it
                    implicit in a merge nobody re-read.

  failure_event     EXACTLY-ONCE REMEDIATION. A red bar that merely stopped the
                    loop left the failure unowned; one that minted per cycle
                    would flood the queue with copies of one defect. Keying the
                    event by the tree, the failing step and a NORMALISED
                    fingerprint makes the identity a property of the FAILURE,
                    not of the observer who happened to see it.

`partial` is the third terminal word (decision D-2 — `returned/`, proposed by
`docs/handback-contract.md` §5, is superseded). This module ADDS it beside the
old mutating return rather than replacing it: `handback.py` still runs, and
retiring it is a later slice's act, not a side effect of this one.

Self-contained by the kit's F5 rule — stdlib only, no sibling import, its own
small git and append helpers — because `integrate.py` imports it on the claim
path and a module on that path must cost nothing to import. The `diff_records`
/ `_revert_ops` pair below is a deliberate verbatim-in-shape copy of
`handback.py`'s, for the same reason and with the same traps; that file stays
untouched.

Stdlib only; Windows + POSIX (path math is `posixpath`, I/O is `pathlib`, every
read declares its encoding).
"""

from __future__ import annotations

import datetime
import hashlib
import json
import posixpath
import re
import subprocess
import tomllib
import unicodedata
from pathlib import Path

SCHEMA = 1

# The ledgers this module owns (contracts §2). Outside `docs/work/` on purpose:
# `agent_common.spec_files` walks `rglob("WI-*.md")` there, so an event parked
# under the work folder would enter the work-item registry as a malformed spec.
EVENTS_DIR = "docs/events"
OUTCOMES_LEDGER = EVENTS_DIR + "/outcomes.jsonl"
FAILURES_LEDGER = EVENTS_DIR + "/failures.jsonl"

# THE THREE WORKER OUTCOMES, and the whole vocabulary. `complete` shipped it,
# `cancelled` never will, `partial` tried and stopped — and all three are
# TERMINAL, which is the half that makes SR-151 true: remaining scope re-enters
# the queue as a successor with its own id and its own admission verdict, never
# as the same row revived.
OUTCOMES = ("complete", "cancelled", "partial")

# What an adjudicator may say about one change group. There is no fourth answer
# and no default: an unlabelled group is a refusal, because "we did not decide"
# is exactly the state the 2026-08-03 incident merged.
LABELS = ("keep", "discard", "quarantine")

# Where a quarantined group's failing diff lands: bar-inert BY EXTENSION, not by
# a rule someone has to keep. The doc checkers discover `*.md`, the stub/dupes
# steps read the declared source tree, and `check.py` ignores `docs/work/*`
# outright — the same reasoning `handback.ARTEFACTS` was built on.
QUARANTINE_DIR = "docs/work/quarantine"

# Surfaces a revert must never touch: the spec move, the log fragments and the
# event ledgers ARE the record being kept, so reverting them would revert the
# classification itself.
BOOKKEEPING = ("docs/work/", "docs/log.d/", EVENTS_DIR + "/")

# --- the frozen scope region --------------------------------------------------
# The frontmatter keys that carry OBLIGATION. Read against agent_common's
# SPEC_SCALARS/SPEC_LISTS: everything omitted here is either mutable bookkeeping
# (`workstream`, `order`, `est_tokens`), a scheduler dial a station may retune
# (`priority`, `critique_budget`, `critique_exhaustion`) or the park marker a
# return legitimately writes (`blockref`). What is left is the obligation a
# reviewer compares delivered work against — and the branch did not write it.
SCOPE_KEYS = (
    "id",
    "title",
    "specref",
    "sr_refs",
    "needs",
    "safety_class",
    "buildtier",
    "planmode",
    "bar",
    "exclusive",
)

# The body sections a TERMINAL MOVE legitimately writes, and therefore the ones
# outside the frozen region. `## Deliverable` is the close's own record of what
# shipped (rule R-A); `## Handback` is the old mutating return's note, excluded
# so this rung does not refuse the machinery it is replacing before the later
# slice retires it. Every other section — the mint's `## Context` block and any
# prose a spec carries — states the obligation and is frozen.
CLOSE_SECTIONS = ("Deliverable", "Handback")

# The digest's schema version, carried IN the digest input. Changing the rule
# changes the prefix, so a digest computed under the old rule is recognisably
# old rather than silently wrong (the `attest-v1` idea, contracts §4).
SCOPE_PREFIX = "scope-v1"
FAILURE_PREFIX = "failure-v1"

SPEC_FENCE = "+++"

# Inline markdown link target — `handback`/`spec_move`'s shape, copied for the
# same F5 reason. Kept identical to `spec_move._MD_LINK_TARGET_RE` because the
# normalisation below has to excuse exactly what that module's rebase writes.
_MD_LINK_TARGET_RE = re.compile(r"(\]\()([^)\s]+)(\))")
_URL_SCHEME_RE = re.compile(r"^(?:[a-z][a-z0-9+.-]*:|//)", re.I)
_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)

_WI_RE = re.compile(r"^WI-\d+$")
_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
_DIGEST_RE = re.compile(r"^[0-9a-f]{16}$")


def _refuse(what, why):
    """One refusal in the program's declared shape (contracts §5): the module,
    the offending thing, and the reason it is refused — never a bare boolean and
    never a message a caller has to guess the subject of."""
    return "outcome: REFUSED - {} ({})".format(what, why)


# --- canonicalisation ---------------------------------------------------------


def _canonical_text(text):
    """A spec's text with the two differences a legitimate CHECKOUT introduces
    removed: Unicode normalisation form and line endings.

    Nothing else is folded. SR-148 says byte-identical, so a re-indent, a
    re-wrap or a trailing-space edit MUST still read as a scope change — this is
    deliberately not `attest.py`'s whitespace-collapsing canonicalisation, whose
    job is the opposite (a re-wrap of a requirement is not a meaning change).
    Line endings are excluded because they are a property of the checkout, not
    of the text (the WI-234/WI-337 lesson)."""
    text = unicodedata.normalize("NFC", text)
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _depth_free_links(text):
    """`text` with every relative markdown link target's parent hops stripped.

    THE MOVE IS NOT AN EDIT. A terminal close is `spec_move.move_spec`, which
    rebases the moved spec's own link targets against its new directory — so
    `active/<branch>/` -> `complete/` turns `../../specs/x.md` into
    `../specs/x.md` in the body, with nobody having typed anything. Freezing the
    raw text would refuse every honest close on the ritual's own write.

    Stripping the leading `../` run normalises exactly that difference and
    nothing more: a link RETARGETED to a different file still differs, because
    only the depth prefix is removed. Scheme-ish, protocol-relative and bare
    `#fragment` targets are left alone, the same three exemptions the ritual
    itself applies."""

    def rewrite(match):
        target = match.group(2)
        if target.startswith("#") or _URL_SCHEME_RE.match(target):
            return match.group(0)
        base, sep, frag = target.partition("#")
        while base.startswith("../"):
            base = base[3:]
        if base.startswith("./"):
            base = base[2:]
        return match.group(1) + base + sep + frag + match.group(3)

    return _MD_LINK_TARGET_RE.sub(rewrite, text)


def _render_value(value):
    """One frontmatter value as a canonical string, TYPE INCLUDED.

    A list and the string that happens to join to the same characters must not
    digest alike — `needs = ["WI-1", "WI-2"]` and `needs = "WI-1,WI-2"` are
    different declarations — so the separator is a control character no TOML
    value carries and booleans render as words rather than as `1`/`0`."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (list, tuple)):
        return "\x1d".join(_render_value(v) for v in value)
    if isinstance(value, (int, float)):
        return repr(value)
    return str(value)


def parse_spec(spec_text):
    """`(frontmatter dict, body)` for one spec's text.

    A copy of `agent_common.parse_spec_frontmatter`'s shape rather than an
    import (F5): this module sits on `integrate.py`'s claim path and must not
    pull the coordinator library in to hash a file."""
    text = _canonical_text(spec_text)
    lines = text.split("\n")
    if not lines or lines[0] != SPEC_FENCE or SPEC_FENCE not in lines[1:]:
        raise ValueError(
            _refuse(
                "the spec text carries no closed `{}` frontmatter fence".format(
                    SPEC_FENCE
                ),
                "a spec with no frontmatter declares no scope to freeze",
            )
        )
    close = lines.index(SPEC_FENCE, 1)
    try:
        data = tomllib.loads("\n".join(lines[1:close]))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(
            _refuse("the spec frontmatter is not valid TOML", str(exc))
        ) from None
    return data, "\n".join(lines[close + 1 :])


def _body_sections(body):
    """`{heading: text}` for a spec body; the pre-heading preamble keys on `""`.

    A repeated heading ACCUMULATES rather than overwriting: two `## Context`
    blocks are two pieces of one obligation, and letting the later one win would
    quietly drop the earlier from the frozen region."""
    marks = [(m.start(), m.end(), m.group(1)) for m in _HEADING_RE.finditer(body)]
    out = {}
    preamble = body[: marks[0][0]] if marks else body
    if preamble.strip():
        out[""] = preamble
    for i, (_start, end, name) in enumerate(marks):
        stop = marks[i + 1][0] if i + 1 < len(marks) else len(body)
        out[name] = out.get(name, "") + body[end:stop]
    return out


def scope_regions(spec_text):
    """The frozen region of one spec, as `{region name: canonical value}`.

    Named regions rather than one blob, because the refusal has to say WHICH
    part moved: "the scope changed" sends a reader to diff the whole file, while
    "front:needs" and "body:Context" send them to the line. `scope_digest`
    hashes exactly this mapping, so the digest and the diff can never disagree
    about what the frozen region is."""
    data, body = parse_spec(spec_text)
    regions = {}
    for key in SCOPE_KEYS:
        if key in data:
            regions["front:" + key] = _canonical_text(_render_value(data[key]))
    for heading, text in _body_sections(body).items():
        if heading in CLOSE_SECTIONS:
            continue
        # Stripped at the ENDS, and only there. A section's blank-line opener
        # and its terminator are functions of the document around it — appending
        # `## Deliverable` at close puts a blank line on the end of whatever
        # section preceded it — so freezing them would make the close rewrite a
        # region nobody edited. Interior whitespace is untouched: a re-indent or
        # a re-wrap inside an obligation section is a text edit and still reads
        # as one (SR-148 says byte-identical, and this is the whole of the
        # exception).
        regions["body:" + (heading or "(preamble)")] = _depth_free_links(text).strip()
    return regions


def scope_digest(spec_text):
    """The 16-hex digest of a spec's frozen scope region (LLR-172).

    Region names sort, so the digest is a function of the CONTENT and not of the
    order a TOML parser happened to yield keys in. Sixteen hex is the same width
    the event ids use (contracts §2): the threat model here is drift and
    accident — a branch editing its own obligation — not a collision an attacker
    mines, and one width across the program keeps the two readable side by side.
    """
    regions = scope_regions(spec_text)
    payload = SCOPE_PREFIX + "\n"
    for name in sorted(regions):
        payload += name + "\x1f" + regions[name] + "\x1e"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def scope_diff(claim_text, terminal_text):
    """The frozen regions that differ between two versions of one spec, sorted.

    A region present in only one side counts as differing — a DELETED `##
    Context` block narrows the obligation exactly as an edited one does, and a
    comparison that walked only the shared keys would call that identical."""
    before, after = scope_regions(claim_text), scope_regions(terminal_text)
    return sorted(
        name for name in set(before) | set(after) if before.get(name) != after.get(name)
    )


# The ONE frozen cell a terminal close is REQUIRED to change, and the only
# direction it may change in: CLEARED, never repointed.
#
# THIS IS A COLLISION BETWEEN TWO SHIPPED RULES, resolved rather than papered
# over. SR-148 freezes the references, `specref` among them; the spec-lifecycle
# rule R-F (`check_trajectory.spec_lifecycle_findings`) says a TERMINAL work
# item clears its `SpecRef` and archives the spec — and the kit's own close
# ritual does exactly that. Freeze it flatly and every honest close refuses;
# drop it from the frozen set and a branch may repoint its own acceptance
# document at whatever it happened to build, which is the unfalsifiable
# completion claim SR-148 exists to stop. Allowing only the CLEARING satisfies
# both: the pointer may be retired at close, and it may not be swapped.
#
# In the DIGEST the cell stays frozen whole — the claim-time record has to be a
# complete statement of the obligation — so the allowance lives here, in the
# comparison, where its direction can be expressed.
CLOSE_CLEARED_KEYS = ("specref",)


def scope_change(claim_text, terminal_text):
    """The frozen regions a terminal move actually changed: `scope_diff` with
    the close ritual's one mandated edit excused. Empty means the move is
    honest; anything in it is a scope the branch wrote and may not have."""
    before, after = scope_regions(claim_text), scope_regions(terminal_text)
    changed = []
    for name in sorted(set(before) | set(after)):
        if before.get(name) == after.get(name):
            continue
        cleared_at_close = (
            name.partition(":")[0] == "front"
            and name.partition(":")[2] in CLOSE_CLEARED_KEYS
            and name in before
            and name not in after
        )
        if not cleared_at_close:
            changed.append(name)
    return changed


# --- the append-only ledgers --------------------------------------------------


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canonical_payload(payload):
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def event_id(payload):
    """The content-derived event id (contracts §2): the first 16 hex of the
    SHA-256 of the canonical payload with `id` and `ts` removed.

    `ts` is excluded PRECISELY so that observing the same fact twice is not two
    events — which is what makes duplicate detection and exactly-once
    remediation properties of the data rather than of a token somebody mints."""
    body = {k: v for k, v in payload.items() if k not in ("id", "ts")}
    return hashlib.sha256(_canonical_payload(body).encode("utf-8")).hexdigest()[:16]


def read_events(path):
    """Every event in one ledger, in file order; `[]` when the file is absent.

    A malformed line is a HARD read error naming the file and the line number,
    never a silently skipped record (contracts §2): a ledger that quietly drops
    what it cannot parse would answer "no such event" to the duplicate check,
    which is the one question it exists to answer correctly."""
    path = Path(path)
    if not path.is_file():
        return []
    out = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(
                _refuse(
                    "{} line {} is not valid JSON".format(path.as_posix(), number),
                    str(exc),
                )
            ) from None
        if not isinstance(record, dict):
            raise ValueError(
                _refuse(
                    "{} line {} is not a JSON object".format(path.as_posix(), number),
                    "one ledger line is one event",
                )
            )
        out.append(record)
    return out


def append_event(path, payload):
    """Stamp `payload` with its derived id and append it as one ledger line.

    A plain append, never a read-modify-write: the ledger is append-only, so an
    `os.replace` rewrite would put the whole history at risk of one bad write to
    add one line. `newline="\\n"` and UTF-8 explicitly, so a Windows checkout
    writes the same bytes a POSIX one does."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    event = dict(payload)
    event["id"] = event_id(event)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(_canonical_payload(event) + "\n")
    return event


# --- the outcome event --------------------------------------------------------

# The CLOSED schema. `write_outcome` builds the payload from this list alone and
# refuses any other keyword, which is the mechanical half of "the event carries
# facts, never instructions": there is no extension point for a field a reader
# might act on, so a would-be instruction has to arrive as `rationale` — one
# delimited string, in a slot every consumer renders as quoted evidence.
OUTCOME_FACTS = ("files", "commits", "checks", "blockers", "unmet", "rationale")


def _string_list(name, value, findings, pattern=None):
    if not isinstance(value, (list, tuple)):
        findings.append(
            _refuse("{} is not a list".format(name), "got {!r}".format(value))
        )
        return []
    out = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            findings.append(
                _refuse(
                    "{} carries a non-string or empty entry".format(name),
                    "got {!r}".format(item),
                )
            )
            continue
        if pattern is not None and not pattern.match(item):
            findings.append(
                _refuse(
                    "{} entry {!r} is not the declared shape".format(name, item),
                    pattern.pattern,
                )
            )
            continue
        out.append(item)
    return out


def _checks(value, findings):
    """The checks run, as `[{"step":..., "result":...}]` — the EXACT result the
    harness reported, never a boolean somebody derived from it. A pass/fail bit
    is what let "the bar ran" and "the bar passed" read alike in a record; the
    verbatim result string cannot be read two ways."""
    if not isinstance(value, (list, tuple)):
        findings.append(_refuse("checks is not a list", "got {!r}".format(value)))
        return []
    out = []
    for item in value:
        if isinstance(item, dict):
            step, result = item.get("step"), item.get("result")
            extra = sorted(set(item) - {"step", "result"})
            if extra:
                findings.append(
                    _refuse(
                        "check {!r} carries undeclared field(s) {}".format(
                            step, ", ".join(extra)
                        ),
                        "a check is a step and its exact result, nothing else",
                    )
                )
                continue
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            step, result = item
        else:
            findings.append(
                _refuse(
                    "check entry {!r} is not (step, result)".format(item),
                    "each check names its step and the result verbatim",
                )
            )
            continue
        if not isinstance(step, str) or not step.strip():
            findings.append(_refuse("a check names no step", "got {!r}".format(step)))
            continue
        if not isinstance(result, str) or not result.strip():
            findings.append(
                _refuse(
                    "check {!r} records no result".format(step),
                    "an unrecorded result is the dishonest green this event exists "
                    "to make impossible",
                )
            )
            continue
        out.append({"step": step, "result": result})
    return out


def _outcome_payload(wi, outcome, claim_base, branch_tip, scope, facts, findings):
    """The validated `outcome` event body, and every problem with it.

    EVERY finding, not the first: a caller fixing a malformed record learns all
    of them in one run rather than one per attempt (contracts §5)."""
    if not isinstance(wi, str) or not _WI_RE.match(wi or ""):
        findings.append(
            _refuse("{!r} is not a WI-### id".format(wi), "the event is keyed by it")
        )
    if outcome not in OUTCOMES:
        findings.append(
            _refuse(
                "{!r} is not a worker outcome".format(outcome),
                "the vocabulary is " + " | ".join(OUTCOMES),
            )
        )
    for name, value in (("claim_base", claim_base), ("branch_tip", branch_tip)):
        if not isinstance(value, str) or not _SHA_RE.match(value or ""):
            findings.append(
                _refuse(
                    "{} {!r} is not a full 40-hex commit".format(name, value),
                    "an abbreviated sha means different things in different repos",
                )
            )
    if not isinstance(scope, str) or not _DIGEST_RE.match(scope or ""):
        findings.append(
            _refuse(
                "scope digest {!r} is not 16 hex".format(scope),
                "it is `scope_digest`'s output or it is not a scope digest",
            )
        )
    undeclared = sorted(set(facts) - set(OUTCOME_FACTS))
    if undeclared:
        findings.append(
            _refuse(
                "undeclared event field(s): " + ", ".join(undeclared),
                "the outcome schema is closed so no field can arrive as an "
                "instruction; the declared facts are " + ", ".join(OUTCOME_FACTS),
            )
        )
    rationale = facts.get("rationale", "")
    if not isinstance(rationale, str):
        findings.append(
            _refuse(
                "rationale is not a string",
                "it is one delimited value a reader renders as quoted evidence, "
                "never a structure a reader walks",
            )
        )
        rationale = ""
    return {
        "schema": SCHEMA,
        "kind": "outcome",
        "wi": wi,
        "outcome": outcome,
        "claim_base": claim_base,
        "branch_tip": branch_tip,
        "scope": scope,
        "files": _string_list("files", facts.get("files", ()), findings),
        "commits": _string_list(
            "commits", facts.get("commits", ()), findings, pattern=_SHA_RE
        ),
        "checks": _checks(facts.get("checks", ()), findings),
        "blockers": _string_list("blockers", facts.get("blockers", ()), findings),
        "unmet": _string_list("unmet", facts.get("unmet", ()), findings),
        "rationale": rationale,
    }


def write_outcome(
    root, wi, outcome, claim_base, branch_tip, scope, ts=None, ledger=None, **facts
):
    """Append the ONE outcome event for one attempt: `(event, [refusals])`.

    THE ATTEMPT KEY IS `(wi, claim_base)`, not the payload. Content-derived ids
    already make a byte-identical re-write free to detect, but the write worth
    refusing is the SECOND one that disagrees — a lane that recorded `partial`,
    thought better of it and recorded `complete` would otherwise leave two live
    events and hand every reader the same "which one is it" question this module
    exists to delete. One claim is one attempt (SR-151: an attempted item never
    returns to the frontier), so the claim base names it exactly.
    """
    findings = []
    payload = _outcome_payload(
        wi, outcome, claim_base, branch_tip, scope, facts, findings
    )
    path = Path(ledger) if ledger else Path(root) / OUTCOMES_LEDGER
    try:
        existing = read_events(path)
    except ValueError as exc:
        return None, findings + [str(exc)]
    for event in existing:
        if event.get("kind") != "outcome":
            continue
        if event.get("wi") == wi and event.get("claim_base") == claim_base:
            findings.append(
                _refuse(
                    "{} already has an outcome event for claim {} (id {})".format(
                        wi, (claim_base or "")[:10], event.get("id")
                    ),
                    "one attempt writes one immutable event; a changed verdict is "
                    "a disposition event, which never edits this one",
                )
            )
            break
    if findings:
        return None, findings
    payload["ts"] = ts or _now()
    return append_event(path, payload), []


# --- the bar-failure event ----------------------------------------------------

_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")
_TIMESTAMP_RE = re.compile(r"\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(?:\.\d+)?Z?")
_DURATION_RE = re.compile(r"\b\d+(?:\.\d+)?\s?(?:s|ms|sec|secs|seconds)\b")
_HEX_RE = re.compile(r"\b(?:0x)?[0-9a-f]{7,}\b", re.I)


def normalise_failure(root, output):
    """A harness failure's OBSERVER-INVARIANT form — the fingerprint's input.

    Every substitution below removes something that varies with WHO ran the bar
    rather than with WHAT failed, and each is declared so a reader can predict
    the fingerprint instead of measuring it:

      1. Unicode NFC, CRLF/CR -> LF (the checkout, again).
      2. ANSI colour escapes — present or absent depending on the terminal.
      3. The repo root, in both its native and posix spellings, -> `<root>`;
         then remaining backslashes inside path-ish tokens -> `/`, so the same
         failure fingerprints alike on Windows and POSIX.
      4. Timestamps, durations and long hex runs (shas, addresses, temp-dir
         suffixes) -> typed placeholders.
      5. Runs of spaces/tabs collapsed and every line stripped; blank lines
         dropped.

    What is NOT removed: counts, ids, assertion text and file/line references.
    Those are the failure. Collapsing them would fold two different defects into
    one event, which is the failure direction that silently loses a bug — where
    the direction this errs toward, a second event for one defect, is merely
    noisy and visible.

    THE SCOPE OF (3), STATED HONESTLY: only the root the caller DECLARES is
    erased, so dedup holds across cycles of one checkout — which is what "the
    same failure on ten cycles" means — and not across two unrelated checkout
    roots. Collapsing an arbitrary absolute prefix would need a guess about
    where somebody else's root ends, and a wrong guess folds two failures into
    one. A second event for one defect is the acceptable error here."""
    text = _canonical_text(output or "")
    text = _ANSI_RE.sub("", text)
    root_text = str(root)
    for spelling in (root_text, root_text.replace("\\", "/")):
        if spelling:
            text = text.replace(spelling, "<root>")
    text = re.sub(r"(?<=[\w>])\\(?=[\w.])", "/", text)
    text = _TIMESTAMP_RE.sub("<ts>", text)
    text = _DURATION_RE.sub("<dur>", text)
    text = _HEX_RE.sub("<hex>", text)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    return "\n".join(line for line in lines if line)


def failure_fingerprint(root, output):
    """The 16-hex fingerprint of a normalised failure."""
    payload = FAILURE_PREFIX + "\n" + normalise_failure(root, output)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


# How much of the normalised failure the event carries. Normalised, so it does
# not vary per cycle and cannot perturb the content-derived id; capped, so one
# pathological bar cannot make the ledger unreadable.
EXCERPT_LINES = 40


def failure_event(root, tree, step, output, gate=None, ts=None, ledger=None):
    """Mint the ONE remediation event for one red bar: `(event, [refusals])`.

    Keyed by `(tree, step, fingerprint)` — the tree says WHICH code, the step
    says WHERE it failed, the fingerprint says WHAT failed — so the same failure
    seen on ten cycles is one event and one remediation draft, while a different
    step or a different failure on the same tree is a second. The key is checked
    against the ledger explicitly rather than left to the derived id: the id
    covers the whole payload, and a second mint that differed only in `gate`
    would otherwise slip through as a "new" failure.
    """
    findings = []
    if not isinstance(tree, str) or not _SHA_RE.match(tree or ""):
        findings.append(
            _refuse(
                "tree {!r} is not a full 40-hex tree id".format(tree),
                "the tree is what makes the failure attributable to code",
            )
        )
    if not isinstance(step, str) or not step.strip():
        findings.append(
            _refuse(
                "the failing step is unnamed",
                "a failure nobody can name a step for is not a bar failure",
            )
        )
    if not (output or "").strip():
        findings.append(
            _refuse(
                "the failure output is empty",
                "the fingerprint is derived from it, so an empty one would key "
                "every silent failure to the same event",
            )
        )
    if findings:
        return None, findings
    normalised = normalise_failure(root, output)
    fingerprint = failure_fingerprint(root, output)
    path = Path(ledger) if ledger else Path(root) / FAILURES_LEDGER
    try:
        existing = read_events(path)
    except ValueError as exc:
        return None, [str(exc)]
    for event in existing:
        if (
            event.get("kind") == "bar-failure"
            and event.get("tree") == tree
            and event.get("step") == step
            and event.get("fingerprint") == fingerprint
        ):
            return None, [
                _refuse(
                    "this failure is already event {} (tree {}, step {})".format(
                        event.get("id"), tree[:10], step
                    ),
                    "exactly-once remediation: the key is the failure, not the "
                    "cycle that observed it",
                )
            ]
    payload = {
        "schema": SCHEMA,
        "kind": "bar-failure",
        "tree": tree,
        "step": step,
        "gate": gate or "",
        "fingerprint": fingerprint,
        "excerpt": "\n".join(normalised.split("\n")[-EXCERPT_LINES:]),
        "ts": ts or _now(),
    }
    return append_event(path, payload), []


# --- the change-group classification ------------------------------------------


def _git(cwd, *args):
    """One git call whose STDOUT survives BYTE FOR BYTE: `(code, stdout)`.

    Not a stripping helper, and the reason is `handback._git_stdout`'s exactly:
    the `--name-status -z` walk below depends on its NUL delimiters, and a diff
    destined for a `.patch` can legitimately end in a single space — the context
    line for a blank line — which stripping turns into an unappliable patch."""
    proc = subprocess.run(
        ["git", "-C", str(cwd), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdin=subprocess.DEVNULL,
    )
    return proc.returncode, proc.stdout or ""


def diff_records(fields):
    """`--name-status -z` fields as `[(status, [paths])]`, or None if truncated.

    RECORDS, NOT PAIRS — `handback.diff_records`'s lesson, copied whole because
    the trap is the same one and a second parser that "simplified" it would
    rediscover it. `diff.renames` has defaulted true since Git 2.9, so `R<score>`
    and `C<score>` are ordinary output and each emits THREE fields: status, old
    path, new path. Reading two at a time desynchronises at the first rename and
    every field after it lands in the wrong slot — paths read as statuses, the
    bookkeeping filter stops matching, and the last record falls off the loop
    bound. That is how a quarantine once printed a confident "4 path(s)
    reverted" over a branch whose failing file was untouched.

    A stream ending mid-record is a TRUNCATED READ, not an empty diff, and
    returns None so the caller refuses instead of classifying a partial list."""
    records, i = [], 0
    while i < len(fields):
        status = fields[i]
        wanted = 2 if status[:1] in ("R", "C") else 1
        if i + wanted >= len(fields):
            return None
        records.append((status, fields[i + 1 : i + 1 + wanted]))
        i += 1 + wanted
    return records


def _revert_ops(status, paths):
    """The git operations that undo one diff record: `[(op, path)]`.

    A rename or copy is TWO undo steps — the NEW path is an addition this branch
    made and has to go, the OLD path is what the base had and has to come back.
    (For a copy the old path is unchanged at the base, so restoring it is a
    harmless no-op; uniform beats a special case nobody remembers.) The `C` arm
    is defensive rather than dead for the reason `handback._revert_ops` records:
    plain `--name-status` reports a copy as `A` unless `--find-copies-harder` is
    passed, and the parser and the undo have to agree about the three-field
    forms AS A PAIR or a caller that adds the flag gets a parse that reads
    copies and an undo that mishandles them."""
    if status[:1] in ("R", "C"):
        return [("rm", paths[1]), ("checkout", paths[0])]
    if status[:1] == "A":
        return [("rm", paths[0])]
    return [("checkout", paths[0])]


def group_key(paths):
    """The change group one diff record belongs to: its directory, posix, `"."`
    at the repo root.

    THE DIRECTORY IS THE GROUP, and the choice is deliberate rather than
    convenient. It is mechanical (no judgement about what "coherent" means), it
    partitions (every record lands in exactly one group, so two labels can never
    contend for one change), and it is the granularity a reviewer already reads
    a diff at. A rename groups by its NEW path — that is where the branch's
    change lives — and its undo restores the old path even when that sits in
    another group, which is what undoing a rename means and is stated here so
    nobody reads it as leakage."""
    return posixpath.dirname(paths[-1]) or "."


def branch_groups(root, branch, base=None):
    """`(groups, refusal)` — the branch's changes against `base`, grouped.

    `groups` is `{group: [(status, paths)]}` in sorted order. Bookkeeping
    records are exempt WHOLE (a rename with one foot in `docs/work/` is not
    something to half-classify) and never appear, because they are the record
    being kept rather than work anyone chose to do."""
    if base is None:
        code, out = _git(root, "merge-base", branch, "HEAD")
        if code != 0 or not out.strip():
            return None, _refuse(
                "cannot name {}'s merge base against HEAD".format(branch),
                "there is no baseline to classify the branch's changes against",
            )
        base = out.strip()
    code, raw = _git(root, "diff", "--name-status", "-z", base, branch)
    if code != 0:
        return None, _refuse(
            "cannot read {}'s diff against {}".format(branch, base[:10]),
            "git refused the read",
        )
    records = diff_records([f for f in raw.split("\0") if f])
    if records is None:
        return None, _refuse(
            "{}'s --name-status stream against {} ends mid-record".format(
                branch, base[:10]
            ),
            "the diff was read short, and classifying a partial file list would "
            "rule on some of the branch and leave the rest unruled",
        )
    groups = {}
    for status, paths in records:
        if any(p.startswith(BOOKKEEPING) for p in paths):
            continue
        groups.setdefault(group_key(paths), []).append((status, paths))
    return {k: groups[k] for k in sorted(groups)}, None


def classify_groups(root, branch, labels, base=None):
    """LLR-175: group the branch's changes and demand a label for each.

    `(groups, [refusals])`. A group nobody labelled is named in the refusals —
    naming is the whole point, because "something is unclassified" is exactly
    the state that merged in the 2026-08-03 incident and a reader could not act
    on it. A label for a group that does not exist is also a refusal: it means
    the adjudicator ruled on a diff that is not this one, and accepting it would
    let a stale classification wave a changed branch through.
    """
    groups, refusal = branch_groups(root, branch, base)
    if refusal:
        return None, [refusal]
    labels = dict(labels or {})
    findings = []
    for group in groups:
        label = labels.get(group)
        if label is None:
            findings.append(
                _refuse(
                    "change group {!r} on {} carries no keep/discard/quarantine "
                    "label".format(group, branch),
                    "a partial attempt states which of its changes are wanted "
                    "before the integrator accepts it, never after",
                )
            )
        elif label not in LABELS:
            findings.append(
                _refuse(
                    "change group {!r} is labelled {!r}".format(group, label),
                    "the vocabulary is " + " | ".join(LABELS),
                )
            )
    for group in sorted(set(labels) - set(groups)):
        findings.append(
            _refuse(
                "label {!r} names change group {!r}, which {} does not have".format(
                    labels[group], group, branch
                ),
                "a classification of a different diff is not a classification of "
                "this one",
            )
        )
    return groups, findings


def _write_patch(wt, base, branch, group, records, artefacts):
    """A quarantined group's failing diff, as a bar-inert `.patch`. A refusal,
    or the repo-relative path it landed at.

    Every path of every record, renames included, so the patch carries the
    rename rather than half of it — the convenience copy a successor applies
    without archaeology, while the reverted commits stay reachable in trunk
    history once the branch merges."""
    paths = [p for _status, record_paths in records for p in record_paths]
    code, patch = _git(wt, "diff", base, branch, "--", *paths)
    if code != 0:
        return None, _refuse(
            "cannot render {}'s group {!r} as a patch".format(branch, group),
            "quarantine keeps the record; a group with no record is a discard "
            "wearing the wrong label",
        )
    rel = "{}/{}-{}.patch".format(
        artefacts, branch, re.sub(r"[^A-Za-z0-9._-]", "-", group)
    )
    dest = Path(wt) / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(patch, encoding="utf-8", newline="")
    return rel, None


def _revert(wt, base, branch, group, records):
    """Undo one group's records in `wt`, back to `base`. A refusal, or None.

    EVERY return code is read. A revert that half-happened is worse than not
    reverting at all, so a failing step resets the worktree to its tip and
    refuses by name — a discarded code here is exactly how `handback`'s
    pair-parse defect stayed silent while four no-match git calls ran and the
    run printed a confident success."""
    for status, paths in records:
        for op, path in _revert_ops(status, paths):
            if op == "rm":
                code, out = _git(wt, "rm", "-q", "-f", "--", path)
            else:
                code, out = _git(wt, "checkout", base, "--", path)
            if code != 0:
                _git(wt, "reset", "--hard", "HEAD")
                tail = out.strip().splitlines()
                return _refuse(
                    "the revert of group {!r} on {} failed at {} ({} {})".format(
                        group, branch, path, op, status
                    ),
                    "the worktree is reset to its tip and nothing was reverted; "
                    "git said: {}".format(tail[-1] if tail else "nothing"),
                )
    return None


def apply_classification(wt, base, branch, groups, labels, artefacts=QUARANTINE_DIR):
    """Enact a complete classification in worktree `wt`: `(actions, [refusals])`.

    `keep` leaves the group alone. `discard` reverts it, so it leaves no code
    behind. `quarantine` reverts it too and first writes the group's diff as a
    bar-inert `.patch` — the RULED red arm (owner decision 1, 2026-07-31)
    generalised from whole-branch to per-group: revert the code, keep the
    record. Nothing here decides a label; it enacts one, and an incomplete
    classification never reaches it (`classify_groups` refuses first).

    Deliberately NOT a commit. The caller owns the commit that carries the
    classification, its reasons and the outcome event together — splitting the
    write from the record is how a revert once landed with nothing saying why.
    """
    findings, actions = [], {}
    for group in sorted(groups):
        label = labels.get(group)
        if label not in LABELS:
            findings.append(
                _refuse(
                    "group {!r} reached the enactment unlabelled".format(group),
                    "apply_classification enacts a COMPLETE classification; "
                    "classify_groups is what proves one",
                )
            )
            continue
        if label == "keep":
            actions[group] = "keep"
            continue
        rel = None
        if label == "quarantine":
            rel, refusal = _write_patch(
                wt, base, branch, group, groups[group], artefacts
            )
            if refusal:
                findings.append(refusal)
                continue
        refusal = _revert(wt, base, branch, group, groups[group])
        if refusal:
            findings.append(refusal)
            continue
        actions[group] = "quarantine:" + rel if rel else "discard"
    return actions, findings
