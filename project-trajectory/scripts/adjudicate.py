#!/usr/bin/env python3
"""adjudicate.py — the authority that confirms or overrides a worker's
judgement, and drafts the candidate that carries what is still owed.

`outcome.py` gave an attempt an identity: one immutable event saying what the
branch's worker believed. This module is the half that says whether the record
AGREES — and it is deliberately not a second verdict gate bolted onto the first.

Four commitments, each answering a specific way this has gone wrong:

  needs_adjudication  A POLICY, NOT A HABIT. Partial and Cancelled always
                      adjudicate: something was owed and did not arrive, so
                      somebody other than the party that stopped has to say what
                      happens next. Complete normally does NOT, and refusing to
                      re-judge it is the point — its authoritative judgement
                      already comes from the independent reviewer plus the
                      composed-tree bar, and rebuilding that gate under a new
                      name would be a second verdict reached from no new
                      evidence. Four triggers reopen it (plan §7) and they are
                      each a reason the first verdict is not trustworthy: the
                      review disagreed with the claim, the scope/bar evidence
                      is incomplete, the safety class is in the configured risk
                      set, or configured sampling drew it. SAMPLING IS DERIVED
                      FROM THE EVENT ID, never from a random draw — see below.

  adjudicate          THE DISPOSITION IS A RECORD, NEVER AN EDIT. It appends a
                      `disposition` event beside the worker's outcome event; the
                      worker's original claim stays visible and unaltered in its
                      own event, so "what was claimed" and "what was ruled" are
                      two readable facts rather than one overwritten one. When
                      the ruling OVERRIDES, the byte-identical spec moves to the
                      corrected terminal folder — the move is part of the
                      verdict, not an optional tidy-up, because leaving a
                      misjudged item in its original folder would contradict the
                      directory-as-status contract every reader depends on.

  draft_successor     AN ATTEMPT IS NEVER REVIVED (SR-151). The remaining scope
                      becomes a NEW candidate carrying explicit lineage — which
                      attempt, and which outcome event produced it — so both
                      histories stay readable and the remaining scope has to
                      pass admission on its own merits rather than inheriting an
                      old verdict. It refuses while the Partial attempt's
                      keep/discard/quarantine split is incomplete: the
                      2026-08-03 incident (`08e6c08a`) merged a returned branch
                      green and landed rejected code as-is precisely because
                      nothing forced that call into the open.

  draft_remediation   EXACTLY-ONCE, BY IDENTITY. One bar-failure event drafts at
                      most one candidate, keyed by the event id, so a failure
                      observed on ten cycles is one repair row rather than ten.
                      The key is a property of the failure (`outcome.py` made it
                      so) and this module simply refuses to mint a second
                      candidate against an id some candidate already names.

**Every candidate lands in `docs/work/draft/`, never in `queued/`.** Queue entry
is one trunk-side admission transaction's job (plan §8) — a producer that wrote
straight into the queue would re-implement the preconditions per producer, which
is how an unclassified or stale row reaches a worker.

**Sampling must be deterministic given the event.** A random draw would make the
same tree adjudicate on one run and not on the next, so a rerun could not
reproduce the loop's decisions and no recorded run could be replayed to check
it. The bucket is the leading hex of the event id — itself the content digest of
the payload — so the same facts always draw the same way, and observing an
outcome twice never changes the answer.

Contracts: `docs/mechanized-loop-contracts.md` §2 (the append-only envelope and
the content-derived id), §5 (the refusal form), §6 (deferred sibling imports).
The ledger helpers below are this module's own small copies per the kit's F5
independently-copyable rule; `tests/test_adjudicate.py` pins them behaviourally
equal to `outcome.py`'s, since the two modules append to ONE file.

Stdlib only; Windows + POSIX (path math is posix, every read declares its
encoding, every write declares `newline="\\n"`).
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import re
import sys
import tomllib
from pathlib import Path

SCHEMA = 1

EVENTS_DIR = "docs/events"
OUTCOMES_LEDGER = EVENTS_DIR + "/outcomes.jsonl"
FAILURES_LEDGER = EVENTS_DIR + "/failures.jsonl"
WORK = "docs/work"

# Candidates land HERE and only here. `draft/` is a declared status directory,
# so a candidate is visible to the duplicate-id guard and the dashboard while
# still being never-ready to the scheduler; `queued/` is the admission
# transaction's to write (plan §8).
DRAFT_DIR = "draft"

# The three terminal folders, keyed by the worker outcome word they encode. The
# map is the whole of "directory as status" for this module: an override moves
# the spec between two of these and changes nothing else about it.
TERMINAL_DIRS = {"complete": "complete", "cancelled": "cancelled", "partial": "partial"}

# The adjudicator's verdict vocabulary — the `disposition-v1` output contract of
# `prompts/adjudicate-disposition.md`, verbatim. Closed: a word outside it is a
# refusal, because a verdict nobody can map to an action is not a verdict.
VERDICTS = (
    "confirm",
    "override-complete",
    "override-partial",
    "override-cancelled",
    "insufficient-evidence",
)

# Verdict -> the corrected worker outcome. `confirm` and `insufficient-evidence`
# are absent on purpose: neither corrects anything, so neither moves the spec.
# `insufficient-evidence` is the honest third answer — it names what the record
# would need, and a guess in its place mints a successor for work nobody wants
# or closes a need nobody agreed to close.
CORRECTED = {
    "override-complete": "complete",
    "override-partial": "partial",
    "override-cancelled": "cancelled",
}

# Why a dedicated adjudicator runs. A closed vocabulary, because the answer
# "this needs adjudication" with no reason attached is unactionable — and
# because a trigger set that grows by string literal at call sites drifts.
TRIGGERS = (
    "outcome-partial",
    "outcome-cancelled",
    "outcome-unreadable",
    "review-disagrees",
    "evidence-incomplete",
    "safety-class",
    "sampling",
)

# The one reviewer verdict that AGREES with a completion claim
# (`prompts/reviewer.md`'s output contract is `APPROVE|CHANGES-REQUESTED`).
# Anything else — including a word this module does not recognise — reads as
# disagreement, which is the fail-closed direction: an unreadable review is not
# evidence that the claim stands.
REVIEW_APPROVES = "APPROVE"

# How much of the event id the sampling bucket reads. Eight hex is 32 bits of a
# digest that is already uniform, which resolves a rate to ~2e-10 — far finer
# than any rate an adopter will write, and short enough that the arithmetic
# stays exact in a float.
SAMPLE_HEX = 8

# The lineage keys a drafted candidate carries in its frontmatter. Neither is a
# declared registry column, so every existing reader passes over them (an
# unknown frontmatter key is ignored, not refused) while `read_lineage` and the
# admission transaction can still read them. `needs` deliberately does NOT
# carry the predecessor: a hard edge to a terminal attempt would block the
# successor forever, since a cancelled predecessor never integrates and so never
# satisfies a hard dependency (docs/work/queued/WI-000-example.md).
LINEAGE_KEYS = ("supersedes", "source_event")

SPEC_FENCE = "+++"
CONTEXT_HEADING = "\n## Context\n\n"

_DIGEST_RE = re.compile(r"^[0-9a-f]{16}$")
# A markdown ATX section heading at the start of a line. Used to REFUSE one
# inside a candidate's scope prose: `outcome.scope_regions` splits the frozen
# region on exactly this shape, so a heading smuggled into scope text would
# silently carve the obligation into pieces — and a section named `Deliverable`
# would carve a piece straight out of the frozen region altogether.
_HEADING_RE = re.compile(r"(?m)^#{1,6}\s")
_BACKTICK_RUN_RE = re.compile(r"`+")

BUILD_TIERS = ("quick", "medium", "strong")
PLAN_MODES = ("", "dual")
BARS = ("", "G1", "G2", "G3")


def _refuse(what, why):
    """One refusal in the program's declared shape (contracts §5): the module,
    the offending thing, and why it is refused. Never a bare boolean — a caller
    that has to guess the subject of a refusal cannot fix it."""
    return "adjudicate: REFUSED - {} ({})".format(what, why)


# --- the append-only ledger ---------------------------------------------------
# This module's own small helpers (F5). They matter more here than usual: the
# `outcome` and `disposition` events share ONE file, so a divergence between
# these and `outcome.py`'s would produce two id derivations over one ledger and
# make every duplicate check answer wrong. tests/test_adjudicate.py pins the
# two behaviourally rather than by extraction.


def _now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _canonical_payload(payload):
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    )


def event_id(payload):
    """The content-derived event id (contracts §2): the first 16 hex of the
    SHA-256 of the canonical payload with `id` and `ts` removed.

    `ts` is out of the digest so that observing one fact twice is not two
    events, which is what makes the duplicate check a property of the data
    rather than of a token somebody remembered to mint."""
    body = {k: v for k, v in payload.items() if k not in ("id", "ts")}
    return hashlib.sha256(_canonical_payload(body).encode("utf-8")).hexdigest()[:16]


def read_events(path):
    """Every event in one ledger, in file order; `[]` when the file is absent.

    A malformed line is a HARD error naming the file and line number, and an id
    that its own payload does not derive is the same (contracts §2). Both
    refusals exist because this reader answers "has this already been
    adjudicated?" — a reader that quietly skipped what it could not parse would
    answer "no" to that question and let a second disposition land."""
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
        if "id" in record and record["id"] != event_id(record):
            raise ValueError(
                _refuse(
                    "{} line {} carries id {!r}, which its payload does not "
                    "derive".format(path.as_posix(), number, record.get("id")),
                    "the id is the digest of the payload with `id`/`ts` removed, so "
                    "a line whose id no longer derives was edited after it was "
                    "written; the ledger is append-only and never rewritten",
                )
            )
        out.append(record)
    return out


def append_event(path, payload):
    """Stamp `payload` with its derived id and append it as one ledger line.

    A plain append, never a read-modify-write: an `os.replace` rewrite would put
    the whole history at risk of one bad write to add one line."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    event = dict(payload)
    event["id"] = event_id(event)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(_canonical_payload(event) + "\n")
    return event


# --- the adjudication policy (plan §7) ----------------------------------------


def _dial(cfg, dotted):
    """One declared config dial, whatever shape the caller holds it in.

    Accepts a `config.Config`, a plain mapping of dotted keys (what a test or a
    projection carries), or None for "the declared defaults". `config` is
    imported lazily so an unbuilt sibling never breaks this module's import
    chain (contracts §6)."""
    if cfg is not None:
        try:
            value = cfg.get(dotted)
        except (AttributeError, KeyError, TypeError):
            value = None
        # `None` means "this holder does not carry the dial", not "the dial is
        # None": no declared dial defaults to None, and a plain mapping's `get`
        # answers None for an absent key rather than raising. A dial genuinely
        # set to `0`, `0.0` or `""` therefore still comes back as itself.
        if value is not None:
            return value
    import config

    return config.DEFAULTS[dotted]


def sampling_bucket(event):
    """The event's position in `[0, 1)` — the deterministic sampling draw.

    Read off the event ID, which is itself the digest of the payload, so the
    bucket is a function of the FACTS. That is the whole requirement: a random
    draw would adjudicate a tree on one run and not on the next, so no run could
    be reproduced and no recorded decision could be replayed to check it. An
    event with no stamped id gets one derived here rather than a fallback draw —
    the id is computable from the payload by anyone holding it."""
    ident = str((event or {}).get("id") or "") or event_id(event or {})
    digits = re.sub(r"[^0-9a-f]", "", ident.lower())[:SAMPLE_HEX]
    if not digits:
        return None
    return int(digits, 16) / float(16 ** len(digits))


def safety_class_of(spec_row):
    """The safety class a work item declares, read from either shape this tree
    carries: the parsed 18-column registry row (`SafetyClass`) or the raw spec
    frontmatter (`safety_class`).

    FAILS CLOSED, exactly like the scheduler's own rule: an absent or blank
    class reads as `unclassified`, which is not in any risk set an adopter would
    write, so `needs_adjudication` treats it as a trigger rather than as
    permission. A row nobody classified is the one whose completion claim
    deserves a second reader."""
    row = spec_row or {}
    for key in ("SafetyClass", "safety_class"):
        value = row.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().lower()
    return "unclassified"


def evidence_gaps(outcome_event):
    """The named gaps in one outcome event's scope/bar evidence, sorted.

    Each entry is a thing a judge would have to ASK for, which is why they are
    named rather than counted. The list is deliberately about the record being
    incomplete, not about the work being bad: a red check result is evidence (a
    clear one), while no check result at all is the absence of it.

      no-scope-digest   nothing says which obligation the branch was measured
                        against, so "did the scope arrive?" has no referent.
      no-checks         nothing records that the declared bar ran. "The bar ran"
                        and "the bar passed" reading alike in a record is the
                        original defect `outcome._checks` was built against.
      no-commits        a claim with no commits delivered nothing observable;
                        the branch tip is not evidence of what is IN it.
      unmet-criteria    the event's own `unmet` list is non-empty. The record
                        contradicts the claim, which is the cheapest possible
                        signal that the claim needs a second reader.
    """
    event = outcome_event or {}
    gaps = []
    if not _DIGEST_RE.match(str(event.get("scope") or "")):
        gaps.append("no-scope-digest")
    if not event.get("checks"):
        gaps.append("no-checks")
    if not event.get("commits"):
        gaps.append("no-commits")
    if event.get("unmet"):
        gaps.append("unmet-criteria")
    return sorted(gaps)


def _review_verdict(review):
    """The verdict word out of whatever the caller holds: a bare string, or a
    mapping carrying `verdict`. `None` means no review verdict was supplied.

    The review lives outside the outcome event on purpose — `outcome.py`'s event
    schema is CLOSED and carries no reviewer field — so the caller that holds
    the reviewer's answer passes it in rather than this module inventing a place
    to look for it."""
    if review is None:
        return None
    if isinstance(review, dict):
        review = review.get("verdict")
    text = str(review or "").strip()
    return text or None


def needs_adjudication(outcome_event, spec_row, config, *, review=None):
    """Which triggers, if any, put this outcome in front of a dedicated
    adjudicator — a tuple of `TRIGGERS` names, empty when none do.

    Truthy IS the answer, and the names are the reason: a caller can branch on
    the tuple and print it, and a reader of the printed line learns why without
    re-deriving the policy.

    The rule (plan §7):

    * **Partial and Cancelled always adjudicate**, and short-circuit. Something
      was owed and did not arrive; the party that stopped does not get to be the
      one who decides what happens to the rest.
    * **Complete normally does not.** Its authoritative judgement already comes
      from the independent reviewer plus the composed-tree bar. Running a
      dedicated adjudicator over every completion would be a second verdict
      reached from no new evidence — the existing gate rebuilt under a new name.
      Four things reopen it, and each is a reason the first verdict is not
      trustworthy on its own:
        - `review-disagrees` — a supplied verdict that is not `APPROVE`, or a
          declared review round (`policy.review_rounds > 0`) that produced no
          verdict at all. The second half matters: "Complete needs no
          adjudicator" is an argument FROM the review, so with the declared
          review missing the argument is missing too. A repo that declared zero
          review rounds is not missing anything and does not trip this.
        - `evidence-incomplete` — `evidence_gaps` found something.
        - `safety-class` — the row's class is in `outcomes.risk_safety_classes`;
          an unclassified row fails closed into this arm.
        - `sampling` — the deterministic bucket falls under
          `outcomes.complete_sampling_rate`.
    * An `outcome` word outside the declared vocabulary is `outcome-unreadable`
      and adjudicates. Only a hand-edited ledger can produce one (`write_outcome`
      validates), and the safe reading of a record nobody can parse is that
      somebody has to look at it.

    Pure: it reads its three arguments and nothing else — no clock, no ledger,
    no filesystem — so the same inputs give the same answer on every run.
    """
    event = outcome_event or {}
    declared = event.get("outcome")
    if declared == "partial":
        return ("outcome-partial",)
    if declared == "cancelled":
        return ("outcome-cancelled",)
    if declared != "complete":
        return ("outcome-unreadable",)

    triggers = []
    verdict = _review_verdict(review)
    rounds = _dial(config, "policy.review_rounds")
    if verdict is not None:
        if verdict.upper() != REVIEW_APPROVES:
            triggers.append("review-disagrees")
    elif isinstance(rounds, int) and rounds > 0:
        triggers.append("review-disagrees")
    if evidence_gaps(event):
        triggers.append("evidence-incomplete")
    declared_classes = _dial(config, "outcomes.risk_safety_classes") or ()
    risky = {str(name).strip().lower() for name in declared_classes}
    safety = safety_class_of(spec_row)
    if safety in risky or safety == "unclassified":
        triggers.append("safety-class")
    rate = _dial(config, "outcomes.complete_sampling_rate")
    bucket = sampling_bucket(event)
    if bucket is not None and isinstance(rate, (int, float)) and bucket < float(rate):
        triggers.append("sampling")
    # Declared order, never discovery order: two runs that found the same
    # triggers must print the same line.
    return tuple(name for name in TRIGGERS if name in triggers)


# --- reading the ledgers ------------------------------------------------------


def find_event(root, ident, *, kind="outcome", ledger=None):
    """`(event, refusal)` for one event id in the ledger that owns `kind`.

    Refuses BY NAME rather than returning None-and-nothing: "no such event" and
    "that event is a bar-failure, not an outcome" send a caller to two different
    fixes, and a bare None says neither."""
    default = FAILURES_LEDGER if kind == "bar-failure" else OUTCOMES_LEDGER
    path = Path(ledger) if ledger else Path(root) / default
    try:
        events = read_events(path)
    except ValueError as exc:
        return None, str(exc)
    for event in events:
        if event.get("id") == ident:
            if event.get("kind") != kind:
                return None, _refuse(
                    "event {} is a {!r} event".format(ident, event.get("kind")),
                    "this call adjudicates a {!r} event".format(kind),
                )
            return event, None
    return None, _refuse(
        "no {!r} event {!r} in {}".format(kind, ident, path.as_posix()),
        "the disposition names the event it rules on; an id nothing derives is "
        "not a record",
    )


def dispositions_for(root, ident, *, ledger=None):
    """Every disposition already recorded against one outcome event."""
    path = Path(ledger) if ledger else Path(root) / OUTCOMES_LEDGER
    return [
        e
        for e in read_events(path)
        if e.get("kind") == "disposition" and e.get("outcome_event") == ident
    ]


def effective_outcome(root, ident, *, ledger=None):
    """`(outcome word, refusal)` — what the attempt's outcome IS, after
    adjudication.

    The worker's declared word until a disposition overrides it, and the
    corrected word after. This is the single place that join lives: a caller
    that read the outcome event alone would act on a claim that has since been
    overruled, and one that read the disposition alone would find nothing for
    every confirmed attempt."""
    event, refusal = find_event(root, ident, ledger=ledger)
    if refusal:
        return None, refusal
    outcome = event.get("outcome")
    for disposition in dispositions_for(root, ident, ledger=ledger):
        corrected = disposition.get("corrected")
        if corrected:
            outcome = corrected
    return outcome, None


# --- the disposition ----------------------------------------------------------


def _spec_hits(root, wi_id, work=WORK):
    """Every spec file the work registry holds for one id, sorted."""
    work_dir = Path(root) / work
    if not work_dir.is_dir():
        return []
    return sorted(work_dir.rglob(wi_id + "-*.md"))


def _spec_location(root, wi_id, work=WORK):
    """`(relpath under work, status directory, refusal)` for one id's spec.

    Zero hits and two hits are both refusals: an id with no file has no spec to
    move, and an id with two has no ONE spec to move — picking either would make
    the disposition rule on a file the reader might not be looking at."""
    hits = _spec_hits(root, wi_id, work)
    if not hits:
        return (
            None,
            None,
            _refuse(
                "{} has no spec under {}".format(wi_id, work),
                "the disposition moves the byte-identical spec, so there has to be "
                "one to move",
            ),
        )
    if len(hits) > 1:
        rels = ", ".join(p.relative_to(Path(root) / work).as_posix() for p in hits)
        return (
            None,
            None,
            _refuse(
                "{} has {} specs ({})".format(wi_id, len(hits), rels),
                "one work item is one file; a duplicate id makes every folder-as-"
                "status answer ambiguous",
            ),
        )
    rel = hits[0].relative_to(Path(root) / work).as_posix()
    return rel, rel.split("/")[0], None


def adjudicate(
    root,
    event_id,
    verdict,
    *,
    by,
    rationale="",
    ts=None,
    ledger=None,
    work=WORK,
):
    """Record the disposition of one attempt: `(event, [refusals])`.

    The verdict CONFIRMS or OVERRIDES the worker's outcome. It is appended to
    the ledger and it never edits the outcome event — two records, two authors,
    both readable. When it overrides, the byte-identical spec moves to the
    corrected terminal folder through `spec_move.move_spec`, so the ritual's
    inbound-link relinking runs too; the move is part of the verdict, because a
    misjudged item left in its original folder makes the directory lie about its
    status and every reader of the directory is then wrong.

    The move is pre-flighted BEFORE the event is appended and performed after.
    If the move then fails, the refusal says so explicitly: the ledger is the
    authority and it now runs ahead of the tree, which a reader can complete —
    where a move with no record behind it is a change nobody can attribute.

    A second disposition against one outcome event is refused by name. Two live
    rulings on one attempt hand every reader the same "which one is it?"
    question this whole layer exists to delete; a later change of mind is a
    human override recorded through `attest.py`, not a second verdict here.
    """
    findings = []
    if verdict not in VERDICTS:
        findings.append(
            _refuse(
                "{!r} is not an adjudication verdict".format(verdict),
                "the vocabulary is " + " | ".join(VERDICTS),
            )
        )
    if not isinstance(by, str) or not by.strip():
        findings.append(
            _refuse(
                "the disposition names no adjudicator",
                "`by` is who ruled; an unattributed ruling cannot be challenged",
            )
        )
    if not isinstance(rationale, str):
        findings.append(
            _refuse(
                "the rationale is not a string",
                "it is one delimited value a reader renders as quoted evidence, "
                "never a structure a reader walks",
            )
        )
        rationale = ""

    event, refusal = find_event(root, event_id, ledger=ledger)
    if refusal:
        return None, findings + [refusal]

    existing = dispositions_for(root, event_id, ledger=ledger)
    if existing:
        findings.append(
            _refuse(
                "outcome event {} already has disposition {}".format(
                    event_id, existing[-1].get("id")
                ),
                "one attempt gets one ruling; a changed mind is a recorded human "
                "override, not a second verdict wearing the same name",
            )
        )

    declared = event.get("outcome")
    corrected = CORRECTED.get(verdict, "")
    if corrected and corrected == declared:
        findings.append(
            _refuse(
                "{} overrides {} to the outcome it already declared".format(
                    verdict, declared
                ),
                "an override to the declared outcome is a confirm; recording it "
                "as an override would put a correction in the history that never "
                "happened",
            )
        )

    wi_id = event.get("wi") or ""
    src_rel, status_dir, refusal = _spec_location(root, wi_id, work)
    if refusal:
        findings.append(refusal)
    elif status_dir != TERMINAL_DIRS.get(declared):
        findings.append(
            _refuse(
                "{}'s spec sits in {}/ while its outcome event declares {!r}".format(
                    wi_id, status_dir, declared
                ),
                "the folder and the ledger already disagree about this attempt; "
                "an adjudicator rules on a record, and this one has two",
            )
        )

    # A destination that is already occupied needs NO rung of its own, and the
    # missing rung is the interesting part: the move keeps the spec's filename,
    # so anything sitting at the corrected home carries this id too — and
    # `_spec_location`'s one-item-one-file rung has already refused, before
    # anything was recorded. `spec_move.move_spec` refuses an existing
    # destination as well, which leaves this a backstop rather than the guard.
    dest_rel = ""
    if corrected and not findings:
        dest_rel = "{}/{}".format(TERMINAL_DIRS[corrected], src_rel.split("/", 1)[1])
    if findings:
        return None, findings

    payload = {
        "schema": SCHEMA,
        "kind": "disposition",
        "wi": wi_id,
        "outcome_event": event_id,
        "declared": declared,
        "verdict": verdict,
        "corrected": corrected,
        "moved": ("{}/{}".format(work, dest_rel) if dest_rel else ""),
        "by": by.strip(),
        # NOT named `rationale`, and the difference is load-bearing rather than
        # stylistic: `prompt_render`'s `worker-rationale` source class matches a
        # serialized `"rationale":` key, so a disposition line fed to a later
        # judge as `ledger` evidence would trip the SR-156 marker and refuse an
        # honest render. This field is the JUDGE's reasoning, a different party
        # from the one under judgement, and the template's own output contract
        # already calls it REASON.
        "reason": rationale,
        "ts": ts or _now(),
    }
    path = Path(ledger) if ledger else Path(root) / OUTCOMES_LEDGER
    written = append_event(path, payload)
    if dest_rel:
        import spec_move

        _touched, refusal = spec_move.move_spec(
            root, "{}/{}".format(work, src_rel), "{}/{}".format(work, dest_rel)
        )
        if refusal:
            return written, [
                _refuse(
                    "disposition {} is recorded but the spec did not move: {}".format(
                        written.get("id"), refusal
                    ),
                    "the ledger is the authority and now runs ahead of the tree; "
                    "complete the move to {}".format(dest_rel),
                )
            ]
    return written, []


# --- candidates ---------------------------------------------------------------


def read_lineage(spec_text):
    """The lineage a candidate's frontmatter carries: `{supersedes, source_event}`
    with `""` for anything absent.

    Its own reader because it is the other half of `_write_candidate`: a lineage
    written by one shape and read by another is a lineage that goes missing the
    first time either changes."""
    lines = str(spec_text).replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if not lines or lines[0] != SPEC_FENCE or SPEC_FENCE not in lines[1:]:
        raise ValueError(
            _refuse(
                "the spec text carries no closed `{}` frontmatter fence".format(
                    SPEC_FENCE
                ),
                "a spec with no frontmatter declares no lineage",
            )
        )
    close = lines.index(SPEC_FENCE, 1)
    try:
        data = tomllib.loads("\n".join(lines[1:close]))
    except tomllib.TOMLDecodeError as exc:
        raise ValueError(
            _refuse("the spec frontmatter is not valid TOML", str(exc))
        ) from None
    return {key: str(data.get(key) or "") for key in LINEAGE_KEYS}


def candidate_for_event(root, source_event, work=WORK):
    """The relpath of the candidate already drafted for one source event, or
    None.

    Scanned over the WHOLE work registry, not just `draft/`: a remediation that
    was drafted, admitted and shipped must not draft again, and it no longer
    lives in `draft/` by then. Exactly the reason `intake.next_wi_id` reads
    every folder — an id (or here, a source event) claimed anywhere is claimed.
    """
    work_dir = Path(root) / work
    if not work_dir.is_dir():
        return None
    for path in sorted(work_dir.rglob("WI-*.md")):
        if path.parent == work_dir:
            continue
        try:
            lineage = read_lineage(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            # A malformed spec is the registry validator's finding to report,
            # not this scan's to crash on (the kit's read_spec_rows split).
            continue
        if lineage.get("source_event") == source_event:
            return path.relative_to(work_dir).as_posix()
    return None


def _cell_findings(cells):
    """Every declared-vocabulary problem with a candidate's scheduler cells.

    Mirrors `intake._draft_refusal`'s rungs rather than inventing softer ones:
    the same cells minted with nobody watching get the same bar, whichever
    producer wrote them."""
    import config

    findings = []
    tier = str(cells.get("buildtier") or "").strip().lower()
    if tier and tier not in BUILD_TIERS:
        findings.append(
            _refuse(
                "buildtier {!r}".format(cells.get("buildtier")),
                "the vocabulary is " + " | ".join(BUILD_TIERS),
            )
        )
    mode = str(cells.get("planmode") or "").strip().lower()
    if mode not in PLAN_MODES:
        findings.append(
            _refuse(
                "planmode {!r}".format(cells.get("planmode")),
                "the vocabulary is dual, or empty for ordinary decomposition",
            )
        )
    safety = str(cells.get("safety_class") or "").strip().lower()
    if safety and safety not in config.SAFETY_CLASSES:
        findings.append(
            _refuse(
                "safety_class {!r}".format(cells.get("safety_class")),
                "the vocabulary is " + " | ".join(config.SAFETY_CLASSES),
            )
        )
    bar = str(cells.get("bar") or "").strip().upper()
    if bar not in BARS:
        findings.append(
            _refuse(
                "bar {!r}".format(cells.get("bar")),
                "the vocabulary is G1 | G2 | G3, or empty for the derived gate",
            )
        )
    return findings


def _scope_findings(what, text, *, headings=True):
    """Refuse scope prose that would break the frozen region it lands in.

    A `##` heading inside CALLER-SUPPLIED text is not decoration:
    `outcome.scope_regions` splits the frozen scope on exactly that shape, so a
    heading here would carve the obligation into pieces — and one spelled
    `## Deliverable` would carve a piece OUT of the frozen region entirely,
    which is a branch editing its own obligation with no edit visible anywhere.

    `headings=False` is for text this module ASSEMBLED, whose only unchecked
    part is a harness excerpt already inside a code fence longer than any
    backtick run in it. A `#` line there is inert — `outcome._body_sections`
    skips fenced spans — and refusing it would refuse honest repair rows for a
    hash in a stack trace."""
    findings = []
    if not isinstance(text, str) or not text.strip():
        findings.append(
            _refuse(
                "the candidate states no {}".format(what),
                "a candidate with nothing owed costs a whole session to discover "
                "and close",
            )
        )
        return findings
    if headings and _HEADING_RE.search(text):
        findings.append(
            _refuse(
                "the {} carries a markdown heading".format(what),
                "the scope freeze splits a spec body on `##`, so a heading here "
                "would silently carve the obligation into pieces",
            )
        )
    return findings


def _fence_for(text):
    """A code fence longer than any backtick run inside `text`, so an excerpt
    cannot escape the block it is quoted in (CommonMark 4.5's rule, used the way
    it is meant to be)."""
    longest = max((len(m.group(0)) for m in _BACKTICK_RUN_RE.finditer(text)), default=0)
    return "`" * max(3, longest + 1)


def _write_candidate(root, title, context, lineage, cells, work=WORK):
    """Write one `draft/` candidate: `(relpath under work, [refusals])`.

    The frontmatter is `wi_convert`'s — the single spec writer's own renderer —
    plus the two lineage keys, and the file is re-parsed before it is returned
    so a candidate cannot be produced by a path that skips the check
    (`wi_convert._self_verify`'s discipline, applied to the one shape that
    writer does not know about).
    """
    import intake
    import wi_convert

    findings = _cell_findings(cells)
    if not isinstance(title, str) or not title.strip():
        findings.append(
            _refuse(
                "the candidate has no title",
                "the title is what a reader sees in the queue; an untitled row "
                "is a row nobody can rule on",
            )
        )
    findings.extend(_scope_findings("scope", context, headings=False))
    if findings:
        return None, findings

    # The id mint is `intake.next_wi_id`, not a second implementation: a mint
    # that scanned a different set of folders would hand out a colliding id, and
    # the R1 invariant (a work branch never mints) is a property of WHERE this
    # runs — trunk-side — not of who calls it.
    row = {column: "" for column in wi_convert.COLUMNS}
    row["WI-ID"] = intake.next_wi_id(root)
    row["Title"] = title.strip()
    row["Status"] = "draft"
    row["Workstream"] = str(cells.get("workstream") or "")
    row["BuildTier"] = str(cells.get("buildtier") or "")
    row["PlanMode"] = str(cells.get("planmode") or "")
    row["SafetyClass"] = str(cells.get("safety_class") or "")
    row["Bar"] = str(cells.get("bar") or "").upper()
    row["EstTokens"] = str(cells.get("est_tokens") or "")
    row["SpecRef"] = str(cells.get("specref") or "")
    row["SR-Refs"] = ";".join(str(r) for r in (cells.get("sr_refs") or ()))

    pairs = list(wi_convert.frontmatter_pairs(row, None))
    pairs.extend((key, lineage[key]) for key in LINEAGE_KEYS if lineage.get(key))
    text = SPEC_FENCE + "\n" + wi_convert.render_frontmatter(pairs) + SPEC_FENCE + "\n"
    text += CONTEXT_HEADING + context.strip("\n") + "\n"
    relpath = "{}/{}".format(DRAFT_DIR, wi_convert.spec_filename(row))

    back, order = wi_convert.parse_spec(text, relpath)
    mismatched = [
        column
        for column in wi_convert.COLUMNS
        if (row.get(column) or "") != (back.get(column) or "")
    ]
    written_lineage = read_lineage(text)
    if mismatched or order is not None:
        return None, [
            _refuse(
                "the candidate does not read back as its own row ({})".format(
                    ", ".join(mismatched) or "order"
                ),
                "a writer whose output it cannot re-read is a writer whose "
                "defects are found later, by whoever trusted it",
            )
        ]
    for key in LINEAGE_KEYS:
        if written_lineage.get(key) != str(lineage.get(key) or ""):
            return None, [
                _refuse(
                    "the candidate's {} does not read back".format(key),
                    "lineage that cannot be read back is lineage that is not there",
                )
            ]

    dest = Path(root) / work / relpath
    if dest.exists():
        return None, [
            _refuse(
                "{} already exists".format(relpath),
                "the id mint handed out a taken id; nothing is overwritten",
            )
        ]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8", newline="\n")
    return relpath, []


def draft_successor(
    root,
    event_id,
    *,
    title,
    remaining,
    branch,
    labels,
    base=None,
    ledger=None,
    work=WORK,
    **cells,
):
    """LLR-177 — draft the candidate carrying a Partial attempt's REMAINING
    scope: `(relpath under docs/work, [refusals])`.

    It never edits and never requeues the original. The attempt stays terminal
    and this is a NEW row, minted with explicit lineage — which attempt, and
    which outcome event produced it — so the record of what was tried and
    rejected survives beside the record of what is still owed, and the remaining
    scope has to pass admission on its own merits instead of inheriting a
    verdict given to different work (SR-151).

    It REFUSES while the attempt's keep/discard/quarantine split is incomplete.
    `outcome.classify_groups` names every unlabelled change group, and every one
    of them is a change nobody has said they want: the 2026-08-03 incident
    (`08e6c08a`) merged exactly that state green and landed rejected code as-is.
    Drafting the successor first would put the incident's precondition back —
    a successor in the queue reads as "the attempt is dealt with".

    The effective outcome must be `partial` — the worker's word, or the
    adjudicator's correction where one exists. A Cancelled attempt overridden to
    Partial therefore drafts, and a Partial overridden to Complete does not.
    """
    import outcome

    findings = []
    event, refusal = find_event(root, event_id, ledger=ledger)
    if refusal:
        return None, [refusal]

    effective, refusal = effective_outcome(root, event_id, ledger=ledger)
    if refusal:
        return None, [refusal]
    if effective != "partial":
        findings.append(
            _refuse(
                "the effective outcome of {} is {!r}".format(event_id, effective),
                "a successor carries the REMAINING scope of a partial attempt; "
                "there is no remainder to carry from any other outcome",
            )
        )

    already = candidate_for_event(root, event_id, work)
    if already:
        findings.append(
            _refuse(
                "outcome event {} already produced {}".format(event_id, already),
                "one attempt, one successor: a second would put the same "
                "remaining scope in the queue twice under two ids",
            )
        )

    _groups, class_findings = outcome.classify_groups(root, branch, labels, base=base)
    findings.extend(class_findings)
    findings.extend(_scope_findings("remaining scope", remaining))
    if findings:
        return None, findings

    wi_id = event.get("wi") or ""
    context = (
        "Successor to {wi}, drafted from its PARTIAL attempt (outcome event "
        "`{event}`). The attempt stays terminal and its record is unchanged; "
        "this row carries only what was still owed when it stopped, and enters "
        "the queue through admission like any other candidate.\n\n"
        "Remaining scope:\n\n{remaining}".format(
            wi=wi_id, event=event_id, remaining=remaining.strip("\n")
        )
    )
    relpath, write_findings = _write_candidate(
        root,
        title,
        context,
        {"supersedes": wi_id, "source_event": event_id},
        cells,
        work=work,
    )
    if relpath is None:
        return None, write_findings
    return relpath, []


def draft_remediation(
    root,
    failure_event_id,
    *,
    title=None,
    effort="",
    ledger=None,
    work=WORK,
    **cells,
):
    """LLR-186 — draft the one repair candidate for one bar-failure event:
    `(relpath under docs/work, [refusals])`.

    Keyed by the failure event id, so exactly-once is a property of the
    IDENTITY rather than of a dedup pass somebody has to remember to run. The
    same failure observed on ten cycles carries one id (`outcome.failure_event`
    made it so), one id names one candidate, and the second call refuses by name
    with `None` for the path — "nothing drafted" is the answer, and the refusal
    says which row already carries it. A different failing step or a different
    fingerprint is a different id and drafts its own.

    `effort`, `buildtier` and `planmode` are the ADJUDICATED estimate, passed in
    by whoever ruled on the failure. Nothing here judges: a module that guessed
    an effort from a failure excerpt would be inventing the one number the
    adjudicator exists to supply.
    """
    event, refusal = find_event(
        root, failure_event_id, kind="bar-failure", ledger=ledger
    )
    if refusal:
        return None, [refusal]

    already = candidate_for_event(root, failure_event_id, work)
    if already:
        return None, [
            _refuse(
                "bar-failure {} already produced {}".format(failure_event_id, already),
                "exactly-once remediation: the key is the failure, not the cycle "
                "that observed it",
            )
        ]

    step = str(event.get("step") or "")
    fingerprint = str(event.get("fingerprint") or "")
    # DERIVED and deterministic, so a recovery re-run produces the same row
    # rather than a near-duplicate with a different name (intake's idempotence
    # rule, which is exact-title dedup).
    derived_title = "Repair the red {} bar ({})".format(step, fingerprint[:10])
    excerpt = str(event.get("excerpt") or "")
    fence = _fence_for(excerpt)
    context = (
        "Remediation for the red declared bar recorded as failure event "
        "`{event}` (SR-147). Failing step: `{step}`. Gate: {gate}. Failure "
        "fingerprint: `{fp}`.\n\n"
        "Adjudicated estimate: effort {effort}; build tier {tier}; plan mode "
        "{mode}.\n\n"
        "The failure as the harness reported it, normalised:\n\n"
        "{fence}text\n{excerpt}\n{fence}".format(
            event=failure_event_id,
            step=step or "(unnamed)",
            gate=event.get("gate") or "(unstated)",
            fp=fingerprint or "(none)",
            effort=effort or "(unstated)",
            tier=cells.get("buildtier") or "(phase default)",
            mode=cells.get("planmode") or "ordinary",
            fence=fence,
            excerpt=excerpt or "(no excerpt recorded)",
        )
    )
    cells = dict(cells)
    cells["est_tokens"] = effort
    relpath, write_findings = _write_candidate(
        root,
        title if title else derived_title,
        context,
        {"source_event": failure_event_id},
        cells,
        work=work,
    )
    if relpath is None:
        return None, write_findings
    return relpath, []


# --- the adjudication brief ---------------------------------------------------

# The slots this module sources itself, and the class each is declared under.
# `rationale` IS NOT HERE AND MUST NOT BE: it is the judged party's own account
# of its work, `prompt_render`'s `worker-rationale` class, and the
# adjudicate-disposition template prohibits it (SR-156). The brief is built from
# an allowlist rather than by copying the event, so adding the field would take
# an edit to this tuple — which is a reviewable act, not an oversight.
BRIEF_SOURCED = (
    ("WI_ID", "registry"),
    ("WI_TITLE", "registry"),
    ("SCOPE_AT_CLAIM", "spec"),
    ("SCOPE_DIGEST", "ledger"),
    ("DECLARED_OUTCOME", "ledger"),
)


def disposition_brief(root, event_id, evidence, *, ledger=None, work=WORK, cfg=None):
    """Render the `adjudicate-disposition` brief for one outcome event:
    `(Rendered, [findings])`.

    This module fills the slots it can source from the ledger and the spec; the
    caller supplies the rest (`BRANCH_COMMITS`, `BRANCH_CHANGES`,
    `CLASSIFICATION`, `HARNESS_RESULT`, `DOWNSTREAM`), because those come from
    git, the classification and the registry rather than from an event.

    A caller-supplied value for a slot this module sources is REFUSED. Those
    five are facts of record — the id, the title, the frozen scope, its digest
    and the declared outcome enum — and a caller that could restate them could
    launder a different claim into the brief under the ledger's authority.
    """
    import prompt_render

    findings = []
    event, refusal = find_event(root, event_id, ledger=ledger)
    if refusal:
        return None, [prompt_render.Finding("adjudicate-disposition", refusal)]

    wi_id = event.get("wi") or ""
    rel, _status, refusal = _spec_location(root, wi_id, work)
    if refusal:
        return None, [prompt_render.Finding(wi_id, refusal)]
    spec_text = (Path(root) / work / rel).read_text(encoding="utf-8")
    data, body = _split_frontmatter(spec_text)
    sourced = {
        "WI_ID": wi_id,
        "WI_TITLE": str(data.get("title") or ""),
        "SCOPE_AT_CLAIM": body,
        "SCOPE_DIGEST": str(event.get("scope") or ""),
        "DECLARED_OUTCOME": str(event.get("outcome") or ""),
    }
    supplied = dict(evidence or {})
    for name, _cls in BRIEF_SOURCED:
        if name in supplied:
            findings.append(
                prompt_render.Finding(
                    "adjudicate-disposition.{}".format(name),
                    "is sourced from the record and may not be supplied by the "
                    "caller; a restated fact of record is a claim wearing the "
                    "ledger's authority",
                )
            )
    if findings:
        return None, findings

    slots = {
        name: prompt_render.Evidence(cls, sourced[name]) for name, cls in BRIEF_SOURCED
    }
    slots.update(supplied)
    decl, decl_findings = prompt_render.declaration(
        root, "adjudicate-disposition", cfg=cfg
    )
    findings.extend(decl_findings)
    if decl is None:
        return None, findings
    rendered, render_findings = prompt_render.render(decl, slots)
    findings.extend(render_findings)
    if rendered is None:
        return None, findings
    return rendered, findings


def _split_frontmatter(spec_text):
    """`(frontmatter dict, body)` for one spec's text — the brief's reader for
    the two halves `read_lineage` does not return."""
    lines = str(spec_text).replace("\r\n", "\n").replace("\r", "\n").split("\n")
    if not lines or lines[0] != SPEC_FENCE or SPEC_FENCE not in lines[1:]:
        raise ValueError(
            _refuse(
                "the spec text carries no closed `{}` frontmatter fence".format(
                    SPEC_FENCE
                ),
                "a spec with no frontmatter declares no scope",
            )
        )
    close = lines.index(SPEC_FENCE, 1)
    data = tomllib.loads("\n".join(lines[1:close]))
    return data, "\n".join(lines[close + 1 :]).strip("\n")


# --- CLI ----------------------------------------------------------------------
def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (the trace.py/check.py
    guard) — a refusal naming a non-ASCII path must not wedge a cp1252 console
    on its way out."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass


def _report(findings):
    """Print EVERY finding, one per line, before the caller exits non-zero
    (contracts §5): a caller fixing a call learns all of its problems in one
    run rather than one per attempt."""
    for line in findings:
        print(line, file=sys.stderr)
    return 1


def _cmd_disposition(args):
    event, findings = adjudicate(
        args.root,
        args.event,
        args.verdict,
        by=args.by,
        rationale=args.reason,
    )
    if findings:
        return _report(findings)
    print(
        "adjudicate: {} -> {} (disposition {})".format(
            event.get("wi"), event.get("verdict"), event.get("id")
        )
    )
    return 0


def _cmd_successor(args):
    relpath, findings = draft_successor(
        args.root,
        args.event,
        title=args.title,
        remaining=Path(args.remaining).read_text(encoding="utf-8"),
        branch=args.branch,
        labels=dict(pair.split("=", 1) for pair in args.label or ()),
        buildtier=args.buildtier or "",
    )
    if findings:
        return _report(findings)
    print("adjudicate: drafted {}".format(relpath))
    return 0


def _cmd_remediation(args):
    relpath, findings = draft_remediation(
        args.root,
        args.event,
        title=args.title,
        effort=args.effort or "",
        buildtier=args.buildtier or "",
        planmode=args.planmode or "",
    )
    if findings:
        return _report(findings)
    print("adjudicate: drafted {}".format(relpath))
    return 0


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    sub = ap.add_subparsers(dest="cmd")

    dis = sub.add_parser("disposition", help="record one attempt's disposition")
    dis.add_argument("--event", required=True, help="the outcome event id")
    dis.add_argument("--verdict", required=True, choices=list(VERDICTS))
    dis.add_argument("--by", required=True, help="who ruled")
    dis.add_argument("--reason", default="", help="the ruling's own reasoning")
    dis.set_defaults(func=_cmd_disposition)

    suc = sub.add_parser("successor", help="draft a partial attempt's successor")
    suc.add_argument("--event", required=True, help="the outcome event id")
    suc.add_argument("--title", required=True)
    suc.add_argument(
        "--remaining", required=True, help="file holding the remaining scope"
    )
    suc.add_argument("--branch", required=True, help="the attempt's branch")
    suc.add_argument(
        "--label",
        action="append",
        metavar="GROUP=LABEL",
        help="one keep/discard/quarantine label; repeatable",
    )
    suc.add_argument("--buildtier", choices=list(BUILD_TIERS))
    suc.set_defaults(func=_cmd_successor)

    rem = sub.add_parser("remediation", help="draft one bar failure's repair row")
    rem.add_argument("--event", required=True, help="the bar-failure event id")
    rem.add_argument("--title", default=None)
    rem.add_argument("--effort", default="", help="the adjudicated effort estimate")
    rem.add_argument("--buildtier", choices=list(BUILD_TIERS))
    rem.add_argument("--planmode", choices=[m for m in PLAN_MODES if m])
    rem.set_defaults(func=_cmd_remediation)

    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
