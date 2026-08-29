#!/usr/bin/env python3
"""prompts.py — the kit's prompt templates as FILES, and their strict fill.

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX).

WHY THIS MODULE EXISTS (SN-028's sibling problem, plan §8). The three
highest-traffic prompts the loop sends — the worker assignment, the reviewer
brief and the critique brief — were Python string constants inside
`agent_loop.py`, reviewable only by reading source. The three dual-plan hats,
by contrast, have always been standalone files under `project-trajectory/
prompts/` with a strict slot fill. The hats are the good pattern, and this
module generalizes it to every prompt the kit ships: **prompt prose becomes
diffable, reviewable text with a regression net.**

That is not cosmetic. Three measured cases say prose in this repo already
steers automation, and each one is a rule the templates now carry:

  * WI-418 — derived prose injected at claim ANCHORED the agent it briefed: a
    judge's brief opened with the defendant's clipped verdict. So: **a judge's
    brief never contains the judged party's self-assessment.**
  * The reviewer brief's redaction-by-construction (diff + requirements only)
    exists because a leaked self-assessment collapses review finding rates
    several-fold — and a test pins the exact clause that says so.
  * WI-417 — `NEEDS-HUMAN`, a prose token, silently selected the review tier,
    and a typo downgraded it. So: **prose that carries control flow must be a
    typed field, never a magic substring.**

TWO SLOT SYNTAXES, DELIBERATELY. `{{NAME}}` with `assemble()`'s strict fill is
the DUAL-PLAN hats' contract (`plan_briefs.py`, which delegates its loading
here). Single-brace `{name}` with `str.format`/`str.replace` is the contract of
the three prompts above AND of every operator override file wired through
`--prompt-map`, which is why it is preserved rather than unified: a strict
`{{NAME}}` fill would REFUSE an operator's existing single-brace template.
`fill()` below gives the single-brace family the same strictness the hats have —
an unknown key or an unfilled slot raises — so the honesty is equal even though
the syntax is not.

RESOLUTION IS SCRIPT-RELATIVE (`KIT/prompts/`, the `bootstrap.py` idiom): in
this meta-repo that is `project-trajectory/prompts/`, and in a scaffolded repo —
where `scripts/` sits at the root — it is `<repo>/prompts/`, which
`bootstrap.py` copies. An in-process caller passing an unrelated temp root
therefore still resolves the shipped template.

Contracts: IF-097, IF-098, IF-099, IF-100, IF-113 — the interface seams this
module declares (process.md §8; rows of record in
docs/requirements/interfaces.toml).

Contract IF-097: the prompt LOADER. `KIT_PROMPTS` is the declared key-to-file map
    and the only vocabulary a caller may name. `load(key, override)` returns one
    template's text with its operator-notes block stripped and its trailing
    newline dropped, or raises `PromptError` naming the path — an unreadable or
    empty template is never an empty brief. `fill(key, text, values)` refuses
    both an unknown slot and a declared slot left unfilled. `preflight(keys,
    overrides)` turns a missing template into a launch-time refusal string
    instead of a first-session crash. `digest(text)` fingerprints over
    normalized line endings, so a CRLF checkout is not a change. Resolution is
    script-relative (`KIT/prompts/`), so an unrelated caller root still finds the
    shipped template.
Contract IF-098: the generated prompt catalogue's row source. `catalog_rows()`
    returns `(key, file, slots, digest)` for every shipped prompt whose file is
    present, sorted by key, and the catalogue reads nothing else — so the
    document cannot disagree with the loader about what ships or with what
    slots. A key whose file is absent is omitted from the rows and reported by
    `preflight`, not rendered as a blank entry.
Contract IF-099: the session engine's side of the loader. `WORKER`, `REVIEWER` and
    `CRITIQUE` are resolved by CALL, never at import, so a missing shipped
    template is a named `PromptError` the coordinator's preflight reports rather
    than an ImportError every consumer of the module pays. `WORKER` is
    deliberately absent from the `--prompt-map` override vocabulary: changing
    the worker brief is a reviewed edit to the template file.
Contract IF-100: the dual-plan hats' side of the loader. `plan_briefs` delegates
    `strip_dispatcher_block` here and calls `strict_check` for its `{{NAME}}`
    fill, passing its own historical exception type, so both slot syntaxes get
    one implementation of "an unknown slot and an unfilled slot are both
    refusals". The hat templates themselves are not in `KIT_PROMPTS`, so they
    are absent from the catalogue and from the per-session digest telemetry.
Contract IF-113: the adjudicator's side of the loader. The four `ADJUDICATE-*`
    keys resolve through `load`, an operator `--prompt-map` override under the
    same key winning, and fill through `fill`; a `PromptError` from either is
    the caller's cue to REFUSE to dispatch rather than to send a brief with a
    hole where the evidence belongs.
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# Kit files are located relative to this script (bootstrap.py's KIT pattern).
KIT = Path(__file__).resolve().parent.parent  # the project-trajectory/ folder
PROMPTS = KIT / "prompts"

# The kit prompts that are NOT dual-plan hats: the session-engine briefs, and
# the four adjudicator briefs the mechanized loop routes. Key -> filename.
#
# A key is also a `--prompt-map` phase key wherever the loop honours an
# override. `WORKER` deliberately is NOT honoured there (`route_session`: "the
# assignment is the whole scope") — editing the template file IS how a repo
# changes the worker brief, and that is a reviewed diff rather than an env var.
WORKER = "WORKER"
REVIEWER = "REVIEWER"
CRITIQUE = "CRITIQUE"
ADJUDICATE_AMENDMENT = "ADJUDICATE-AMENDMENT"
ADJUDICATE_DISPOSITION = "ADJUDICATE-DISPOSITION"
ADJUDICATE_CONFLICT = "ADJUDICATE-CONFLICT"
ADJUDICATE_RED_TC = "ADJUDICATE-RED-TC"

KIT_PROMPTS = {
    WORKER: "worker.template.md",
    REVIEWER: "reviewer.template.md",
    CRITIQUE: "critique.template.md",
    ADJUDICATE_AMENDMENT: "adjudicate-amendment.template.md",
    ADJUDICATE_DISPOSITION: "adjudicate-disposition.template.md",
    ADJUDICATE_CONFLICT: "adjudicate-conflict.template.md",
    ADJUDICATE_RED_TC: "adjudicate-red-tc.template.md",
}

# A single-brace `{name}` slot. Lower-case + underscore only, so a `{}` that is
# part of prose (or a doubled `{{`) is not mistaken for a slot.
SLOT_RE = re.compile(r"(?<!\{)\{([a-z][a-z0-9_]*)\}(?!\})")


class PromptError(Exception):
    """A template could not be loaded or filled. Raised, not returned: every
    caller either preflights (and reports) or is composing a session that must
    not launch with a hole where a brief belongs."""


def strip_dispatcher_block(text):
    """The prompt body with a leading `<!-- ... -->` operator-notes block
    removed. Text without one is returned left-stripped and otherwise
    unchanged. (`plan_briefs.strip_dispatcher_block` delegates here — one
    implementation, two vocabularies.)"""
    body = text.lstrip()
    if body.startswith("<!--"):
        end = body.find("-->")
        if end != -1:
            return body[end + len("-->") :].lstrip()
    return body


def template_path(key, override=None):
    """The FILE a prompt key resolves to: the operator's `--prompt-map` override
    when given, else the shipped kit template."""
    if override:
        return Path(override)
    if key not in KIT_PROMPTS:
        raise PromptError(
            "unknown prompt key {!r} (expected one of {})".format(
                key, ", ".join(sorted(KIT_PROMPTS))
            )
        )
    return PROMPTS / KIT_PROMPTS[key]


def load(key, override=None):
    """The prompt TEXT for `key`, dispatcher notes stripped and the trailing
    newline the file carries removed, so the value is byte-identical to the
    string constant it replaced.

    Raises `PromptError` naming the path on any read failure — a template the
    kit ships is not optional, and the alternative (an empty brief) is the
    silent-wrong-content failure this whole layer exists to prevent."""
    path = template_path(key, override)
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise PromptError(
            "prompt [{}]: cannot read {}: {}".format(key, path, exc)
        ) from exc
    body = strip_dispatcher_block(text)
    if not body.strip():
        raise PromptError("prompt [{}]: {} is empty after the notes".format(key, path))
    return body.rstrip("\n")


def slots(text):
    """The set of single-brace slot names present in `text`."""
    return set(SLOT_RE.findall(text))


def fill(key, text, values):
    """STRICT single-brace fill — the `{{NAME}}` hats' guarantee, in the
    `{name}` vocabulary the session engine and every operator override already
    speak.

    Every provided key must name a slot the template declares, and every slot
    the template declares must be provided; either violation raises
    `PromptError` naming it. A half-filled brief — a hole where a redacted
    input belongs, or a value silently dropped because a template was edited —
    can never reach a session.

    The unfilled check reads the TEMPLATE's slot set, not the output, so a
    slot VALUE containing `{something}` passes through verbatim."""
    strict_check(key, present=slots(text), provided=set(values), form="{name}")
    return SLOT_RE.sub(lambda m: str(values[m.group(1)]), text)


def strict_check(label, present, provided, form, error=None):
    """THE strictness both slot syntaxes share, stated once.

    Raises when a provided key names no slot, or a declared slot has no value —
    the two halves of "a brief never ships with a hole, and a template edit
    that drops a slot fails loudly". `plan_briefs.assemble` calls this for the
    `{{NAME}}` hats (passing `ValueError`, its historical exception, so its own
    callers and tests are unchanged); `fill` calls it for `{name}`.

    Extracted rather than copied because F5 sanctions duplication between
    INDEPENDENTLY COPYABLE scripts, and `plan_briefs` already imports this
    module — a second copy of the one rule that decides whether a session gets
    a complete brief would be duplication with no copy-ability to buy."""
    error = error or PromptError
    unknown = sorted(provided - present)
    if unknown:
        raise error(
            "{}: unknown slot(s) {} — the template declares {}".format(
                label, ", ".join(unknown), ", ".join(sorted(present)) or "(none)"
            )
        )
    unfilled = sorted(present - provided)
    if unfilled:
        raise error(
            "{}: unfilled slot(s) {} — every {} must be provided "
            "(a brief never ships with a hole)".format(label, ", ".join(unfilled), form)
        )


def digest(text):
    """`sha256:<12 hex>` of the NORMALIZED text — line endings folded to `\\n`
    and the trailing newline dropped.

    Normalized, not raw, on purpose: the same template checked out CRLF on
    Windows and LF on POSIX is the same prompt, and a telemetry field that says
    otherwise would report a model change on every clone. Truncated to 12 hex
    (48 bits) because this identifies a template within one repo's catalogue,
    never across an adversary — the same posture the WI id scheme takes."""
    normal = text.replace("\r\n", "\n").replace("\r", "\n").rstrip("\n")
    return "sha256:" + hashlib.sha256(normal.encode("utf-8")).hexdigest()[:12]


def preflight(keys=None, overrides=None):
    """Refusal strings for every kit prompt that cannot be loaded — the
    launchability rung, so a missing shipped template fails BEFORE iteration 1
    rather than at the first session that needs it. `[]` when all resolve."""
    overrides = overrides or {}
    out = []
    for key in sorted(keys or KIT_PROMPTS):
        try:
            load(key, overrides.get(key))
        except PromptError as exc:
            out.append(str(exc))
    return out


def catalog_rows():
    """`[(key, file, slots, digest)]` over every shipped kit prompt, sorted by
    key — the generated prompt catalogue's rows (`gen_prompt_catalog.py`)."""
    rows = []
    for key in sorted(KIT_PROMPTS):
        path = template_path(key)
        if not path.is_file():
            continue
        text = load(key)
        rows.append(
            (key, KIT_PROMPTS[key], ";".join(sorted(slots(text))), digest(text))
        )
    return rows


def _cmd_list(_args):
    for key, filename, slot_names, dig in catalog_rows():
        print("{:24} {:36} {:10} {}".format(key, filename, dig, slot_names or "(none)"))
    return 0


def _cmd_check(_args):
    refusals = preflight()
    for line in refusals:
        print("prompts: " + line, file=sys.stderr)
    return 1 if refusals else 0


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("list", help="print the shipped prompt catalogue")
    sub.add_parser("check", help="exit 1 if any shipped prompt cannot be loaded")
    args = ap.parse_args(argv)
    return {"list": _cmd_list, "check": _cmd_check}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
