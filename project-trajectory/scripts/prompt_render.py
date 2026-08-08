#!/usr/bin/env python3
"""Every operational prompt as a reviewed asset, rendered once, strictly.

Stack-agnostic, standard-library only. The three highest-traffic prompts in this
kit — worker, reviewer, critique — were Python string constants inside
`agent_loop.py`. The prose was load-bearing (the reviewer's redaction clause is
the reason independent review finds anything; the critique rubric anchors are
the reason a critic cannot invent its own standard) and it was reviewable only
by reading source. Meanwhile the dual-plan hats had already shown the better
shape: standalone Markdown with `{{SLOT}}` placeholders and a strict fill.

This module generalises that shape to every job and adds the four things the
embedded constants could not have (contracts `docs/mechanized-loop-contracts.md`
§1; authoring rules `project-trajectory/prompts/README.md`). Each design
commitment below exists because of a specific failure:

  - **Three refusals BEFORE launch, each naming the offending slot.** An
    unknown slot key, a slot the caller did not supply, and a placeholder that
    survived the render are separate findings with separate messages, and a run
    reports all of them. A half-filled brief is a hole where evidence belongs,
    and a session started on one produces a confident answer to the wrong
    question — which costs a whole session to discover and is indistinguishable
    from a real verdict afterwards.

  - **Sources are TYPED, and checked twice.** A judging role declares the source
    classes it may be fed and the ones it may never be fed (SR-156). The first
    check reads each value's declared class — a value labelled
    `self-assessment` never reaches a reviewer. The second re-runs the same
    marker scan over the RENDERED prompt, because the interesting leak is the
    one that arrives inside an *allowed* slot: a registry excerpt that happens
    to quote the defendant's own verdict is still the defendant's own verdict. A
    live adjudication brief once opened with the judged party's verdict line
    clipped mid-word, which is what the second check is for.

  - **The content check compares marker COUNTS, not presence.** The reviewer
    template legitimately contains the words "self-assessment" (its redaction
    clause) and a literal `VERDICT:` line (its output contract). A
    presence test would refuse every reviewer render forever. What is
    diagnostic is a marker count that RISES between the template body and the
    rendered prompt: the template's own prose is the baseline, and anything
    above it arrived with a value.

  - **Provenance is hashes, never prompts.** A recorded verdict nobody can
    attribute to a prompt cannot be challenged; a tracked history full of
    rendered briefs is a privacy and size problem. `provenance` returns the
    template identity, the template hash and the rendered-prompt hash, which
    reproduce the attribution without carrying the text (SR-157).

  - **The catalog is GENERATED.** A hand-maintained table of which prompt may
    read what drifts from the templates the day after it is written; this one
    is read from the declarations and the files themselves.

  - **Prompts travel on stdin.** The `render` command writes the prompt to
    stdout and nowhere else, so a caller pipes it into the session. A
    brief-sized prompt in argv hits the OS command-line cap (the same finding
    that put `agent_loop`'s own transport on stdin), and an argv prompt is
    visible in every process listing on the box.

Line endings are folded to LF and the rendered prompt ends with exactly one
newline, so a golden fixture render is byte-identical on Windows and POSIX and
the recorded hash is a property of the CONTENT, not of the checkout.

This module changes NO existing runtime reader: `agent_loop.py` keeps its
embedded constants until the cutover slice moves the call sites. What exists
here is the reviewed asset plus the proof that it renders.

Usage — `--root` is a GLOBAL option, so it precedes the subcommand (the shape
intake.py, integrate.py, schedule.py and plan_briefs.py all use); argparse
rejects the trailing spelling with exit 2:
    python scripts/prompt_render.py [--root .] catalog   # the generated table
    python scripts/prompt_render.py [--root .] check     # declarations vs files
    python scripts/prompt_render.py [--root .] render --job JOB --slots FILE

Small helpers (`_utf8_console`, the dispatcher-block stripper, the `Finding`
shape) are duplicated from siblings per the kit's independently-copyable-script
convention (F5) — this file stays a self-contained drop-in.
"""

import argparse
import collections
import hashlib
import json
import re
import sys
from pathlib import Path

# A `{{NAME}}` slot, exactly the shape the shipped dual-plan templates use.
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")

# A validation refusal: the offending thing and why. Same two-field shape as
# `config.Finding` (duplicated, not imported — F5), so a caller can print the
# two lists through one formatter.
Finding = collections.namedtuple("Finding", "key reason")

# What a slot value is: its declared source class plus its text. A bare string
# is accepted and read as UNLABELLED — which is a refusal for any role that
# declares an allowed-source list, because a value that will not name itself
# cannot be allowlisted.
Evidence = collections.namedtuple("Evidence", "source text")

UNLABELLED = "(unlabelled)"

# One prompt's declared contract, resolved: the config row plus the template
# path it names, anchored to the repo root.
Declaration = collections.namedtuple(
    "Declaration",
    "job template path required_slots allowed_sources prohibited_sources output_schema",
)

# One render. `body` (the template with its dispatcher block removed) is carried
# beside `text` because the source check needs the baseline it was rendered
# from; `template_text` is the whole reviewed asset, which is what gets hashed.
Rendered = collections.namedtuple("Rendered", "job template text body template_text")

# The session record's prompt half (SR-157). The route identity and the model
# are the routing slice's to add beside it.
Provenance = collections.namedtuple(
    "Provenance", "job template template_sha256 prompt_sha256"
)

CatalogRow = collections.namedtuple(
    "CatalogRow", "job template allowed prohibited output_schema template_sha256"
)


# --- the declared source classes ---------------------------------------------
# `markers` are the shapes that identify text OF this class when it arrives
# inside some OTHER slot. A class with no markers is enforced by its LABEL only:
# a role may still prohibit it, and a value declaring it is still refused, but
# the same content pasted into an allowed slot is invisible. That limitation is
# stated here and in prompts/README.md rather than papered over — a marker set
# loose enough to catch everything would refuse honest registry prose, and a
# check that cries wolf gets switched off.
SourceClass = collections.namedtuple("SourceClass", "name what markers")


def _markers(*pairs):
    """`(label, compiled regex)` pairs. The label is what a finding prints, so
    it reads as a description of the offending shape, not as a regex."""
    return tuple((label, re.compile(pattern)) for label, pattern in pairs)


SOURCE_CLASSES = (
    SourceClass(
        "registry",
        "SN/SR/LLR/TC rows and work-item rows, as filed.",
        (),
    ),
    SourceClass(
        "spec",
        "A work item's spec-of-record body: the obligation, as written.",
        (),
    ),
    SourceClass(
        "diff",
        "Committed changes: `git log` / `git diff` output over a named range.",
        (),
    ),
    SourceClass(
        "harness",
        "Real output of a declared harness step, quoted verbatim.",
        (),
    ),
    SourceClass(
        "ledger",
        "docs/events/ records: attestation, outcome, admission, failure.",
        (),
    ),
    SourceClass(
        "graph",
        "Computed structure: the overlap graph, the work-item DAG, a coverage "
        "report. Arithmetic, not opinion.",
        (),
    ),
    SourceClass(
        "rubric",
        "A written rubric with numbered anchors.",
        (),
    ),
    SourceClass(
        "owner-prompt",
        "The owner's own words, verbatim.",
        (),
    ),
    SourceClass(
        "self-assessment",
        "The judged party's own account of its work: session notes, a status "
        "or log entry it wrote, a verdict or outcome line it declared.",
        _markers(
            ("a machine verdict line", r"(?m)^[ \t>*\-]*VERDICT\s*:"),
            ("a machine outcome line", r"(?m)^[ \t>*\-]*OUTCOME\s*:"),
            ("a handback self-report heading", r"(?mi)^#{1,6}\s*handback\b"),
            ("the words 'self-assessment'", r"(?i)\bself[ \-]assessment\b"),
        ),
    ),
    SourceClass(
        "worker-rationale",
        "The `rationale` field of a worker's outcome event — why IT says the "
        "attempt ended as it did. Facts from the same event are a different "
        "class; this is the claim under judgement.",
        _markers(
            ("a rationale field", r"(?mi)^[ \t>*\-]*rationale\s*[:=]"),
            ("a serialized rationale field", r'(?i)"rationale"\s*:'),
        ),
    ),
    SourceClass(
        "rival-plan",
        "The competing plan's text in a dual-plan round. The critic gets the "
        "computed coverage diff instead.",
        _markers(
            ("a plan table header", r"(?m)^\s*\|\s*Plan-WI\s*\|"),
            ("a plan-local work-item row", r"(?m)^\s*\|\s*P\d+\s*\|"),
        ),
    ),
    SourceClass(
        "provenance",
        "Who produced an artifact: model, route, family, session id. The "
        "arbiter judges anonymized plans, so this is what anonymization removes.",
        _markers(
            (
                "a model/route identity line",
                r"(?mi)^[ \t>*\-]*(model|route|family|provider)\s*[:=]",
            ),
            ("a session id", r"(?i)\bsession[ \-]id\b"),
        ),
    ),
)

SOURCE_CLASS_NAMES = tuple(c.name for c in SOURCE_CLASSES)
_BY_CLASS = {c.name: c for c in SOURCE_CLASSES}


# --- text canonicalisation ----------------------------------------------------
def fold_newlines(text):
    """CRLF and CR folded to LF.

    Applied to the template and to every slot value, so a Windows checkout and a
    POSIX one render the same bytes — which is what makes a golden fixture and a
    recorded hash comparable across machines at all."""
    return text.replace("\r\n", "\n").replace("\r", "\n")


def canonical_text(text):
    """`fold_newlines` plus exactly one trailing newline.

    The trailing-newline rule is the hashing rule: an editor that adds or eats a
    final blank line must not change the recorded template hash, or every
    provenance record would disagree with the next one for a reason no reader
    could see."""
    return fold_newlines(text).rstrip("\n") + "\n"


def sha256_of(text):
    """The SHA-256 of `text` as canonical UTF-8 — a property of the content, not
    of the checkout that holds it."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def strip_dispatcher_block(text):
    """The prompt body with a leading `<!-- DISPATCHER NOTES ... -->` block
    removed (duplicated from plan_briefs.py per F5).

    Stripped BEFORE the slot set is computed, which is what lets the notes name
    every `{{SLOT}}` in prose without those mentions becoming slots."""
    body = text.lstrip()
    if body.startswith("<!--"):
        end = body.find("-->")
        if end != -1:
            return body[end + len("-->") :].lstrip()
    return body


def template_slots(body):
    """The `{{NAME}}` slot names present in a template body."""
    return set(PLACEHOLDER_RE.findall(body))


def evidence(value):
    """One slot value as `Evidence`.

    Accepts an `Evidence`, a `{"source": ..., "text": ...}` mapping (the JSON
    slots-file shape) or a bare string, which reads as UNLABELLED. Text is
    newline-folded here, once, so no caller has to remember to."""
    if isinstance(value, Evidence):
        return Evidence(value.source, fold_newlines(str(value.text)))
    if isinstance(value, dict):
        return Evidence(
            str(value.get("source", UNLABELLED)),
            fold_newlines(str(value.get("text", ""))),
        )
    return Evidence(UNLABELLED, fold_newlines(str(value)))


def _as_evidence(slots):
    return {name: evidence(value) for name, value in slots.items()}


# --- declarations -------------------------------------------------------------
def declarations(root, cfg=None):
    """`({job: Declaration}, [Finding])` for every `[prompts.*]` the repo at
    `root` declares, in the closed vocabulary's order.

    An UNDECLARED job yields no row rather than a default path: a prompt this
    repo never declared is not a prompt with a guessable home, and inventing one
    would launch a session on a file nobody reviewed.

    `config` is imported lazily so an unbuilt sibling can never break this
    module's import chain (contracts §6)."""
    import config

    root = Path(root)
    findings = []
    if cfg is None:
        cfg, cfg_findings = config.load_config(root)
        findings.extend(Finding(f.key, f.reason) for f in cfg_findings)
    out = {}
    for job in config.PROMPTS:
        entry = cfg.prompts.get(job)
        if entry is None:
            continue
        rel = entry.template or ""
        out[job] = Declaration(
            job=job,
            template=rel,
            path=root.joinpath(*rel.split("/")) if rel else None,
            required_slots=tuple(entry.required_slots),
            allowed_sources=tuple(entry.allowed_sources),
            prohibited_sources=tuple(entry.prohibited_sources),
            output_schema=entry.output_schema or "",
        )
    return out, findings


def declaration(root, job, cfg=None):
    """`(Declaration, [Finding])` for one job; `(None, [Finding])` when the repo
    declares no prompt for it."""
    decls, findings = declarations(root, cfg=cfg)
    decl = decls.get(job)
    if decl is None:
        findings.append(
            Finding(
                "prompts.{}".format(job),
                "is not declared in docs/config.toml; a prompt with no declared "
                "template has no reviewed prose to render",
            )
        )
    return decl, findings


def read_template(declaration):
    """`(canonical template text, [Finding])` for a declaration's template file.

    An absent or unreadable template is a finding naming the path, never an
    empty prompt: an empty brief launches just as happily as a full one."""
    if declaration.path is None:
        return None, [
            Finding(
                "prompts.{}.template".format(declaration.job),
                "declares no template path",
            )
        ]
    try:
        raw = declaration.path.read_bytes()
    except OSError as exc:
        return None, [
            Finding(
                declaration.template,
                "cannot be read: {}".format(exc),
            )
        ]
    try:
        return canonical_text(raw.decode("utf-8-sig")), []
    except UnicodeDecodeError as exc:
        return None, [
            Finding(declaration.template, "is not valid UTF-8: {}".format(exc))
        ]


# --- the strict render --------------------------------------------------------
def render(declaration, slots):
    """`(Rendered, [])` for a complete, clean fill; `(None, [Finding])` for any
    refusal — and EVERY refusal in the list, never the first.

    The rungs, in order, each naming the offending slot:

      1. a supplied key the template has no slot for (a caller filling a brief
         that moved on without it);
      2. a declared required slot the template does not contain (the config row
         and the reviewed prose have drifted apart);
      3. a template slot nobody supplied — a hole where evidence belongs, the
         message saying whether the declaration called it required;
      4. a `{{...}}` that SURVIVED the fill, which can only have arrived inside
         a slot value, so the message names the carrier;
      5. `check_sources`, over the values and over the rendered prompt.

    Rungs 1-3 are computed together and refuse as a set, because a caller
    fixing a brief should learn everything wrong with it in one run. Nothing is
    substituted until they pass: a partially filled prompt must not exist even
    as a local variable that a later edit could return."""
    text, findings = read_template(declaration)
    if text is None:
        return None, findings

    body = strip_dispatcher_block(text)
    present = template_slots(body)
    supplied = _as_evidence(slots)
    job = declaration.job
    known = ", ".join(sorted(present)) or "(none)"

    for name in sorted(set(supplied) - present):
        findings.append(
            Finding(
                "{}.{}".format(job, name),
                "is not a slot of {} (its slots are {})".format(
                    declaration.template, known
                ),
            )
        )
    for name in sorted(set(declaration.required_slots) - present):
        findings.append(
            Finding(
                "{}.{}".format(job, name),
                "is declared required but {} has no such slot (the declaration "
                "and the template have drifted)".format(declaration.template),
            )
        )
    for name in sorted(present - set(supplied)):
        findings.append(
            Finding(
                "{}.{}".format(job, name),
                "is a {} slot of {} and was not supplied (a render leaves no "
                "hole)".format(
                    "REQUIRED" if name in declaration.required_slots else "declared",
                    declaration.template,
                ),
            )
        )
    if findings:
        return None, findings

    # A FUNCTION replacement, never a string one: `re.sub` expands `\1` and
    # `\g<0>` in a string replacement, so a diff or a harness log containing a
    # backslash escape would be rewritten on its way into the prompt.
    out = canonical_text(PLACEHOLDER_RE.sub(lambda m: supplied[m.group(1)].text, body))

    for name in sorted(set(PLACEHOLDER_RE.findall(out))):
        carriers = sorted(
            slot for slot, ev in supplied.items() if "{{" + name + "}}" in ev.text
        )
        findings.append(
            Finding(
                "{}.{}".format(job, name),
                "survived the render, carried in by {} - a launched prompt holds "
                "no placeholder".format(
                    "slot " + "/".join(carriers) if carriers else "a slot value"
                ),
            )
        )

    provisional = Rendered(
        job=job,
        template=declaration.template,
        text=out,
        body=body,
        template_text=text,
    )
    findings.extend(check_sources(declaration, supplied, rendered=provisional))
    if findings:
        return None, findings
    return provisional, []


# --- the source check ---------------------------------------------------------
def _declaration_findings(declaration):
    """`[Finding]` about the DECLARATION itself, before any value is looked at.

    Extracted from `check_sources` because it answers a different question at a
    different time: these two rungs are wrong about the config file, not about a
    render, and they give the same answer for every render of that job. Keeping
    them here also means a caller can validate a whole catalog without assembling
    evidence for it — which is exactly what the `check` CLI arm does.
    """
    job = declaration.job
    allowed = set(declaration.allowed_sources)
    prohibited = set(declaration.prohibited_sources)
    findings = []
    for name in sorted(allowed | prohibited):
        if name not in _BY_CLASS:
            findings.append(
                Finding(
                    "prompts.{}".format(job),
                    "names the undeclared source class {!r}; the declared "
                    "classes are {}".format(name, ", ".join(SOURCE_CLASS_NAMES)),
                )
            )
    for name in sorted(allowed & prohibited):
        findings.append(
            Finding(
                "prompts.{}".format(job),
                "both allows and prohibits the source class {!r}; a class "
                "cannot be evidence and contraband at once".format(name),
            )
        )
    return findings


def check_sources(declaration, slots, rendered=None):
    """`[Finding]` for one render's sources: the label rung, the per-value
    content rung, and — when `rendered` is given — the residue rung over the
    prompt as it will be launched.

    Called without `rendered` it checks the inputs alone, which is what a caller
    assembling evidence wants before it has a template. `render` always passes
    the render, because the class of leak this requirement exists for is the one
    that arrives inside an ALLOWED slot and is therefore invisible to a label
    check (SR-156).

    The residue rung compares marker COUNTS between the template body and the
    rendered prompt. Presence would be wrong: the reviewer template contains the
    literal word "self-assessment" in the clause forbidding it, so a presence
    test would refuse every reviewer render ever launched. A count that rises
    above the template's own baseline is what a value brought with it — and it
    also catches the marker formed at a JOIN, where template prose and a value
    are individually clean and their concatenation is not."""
    findings = list(_declaration_findings(declaration))
    supplied = _as_evidence(slots)
    job = declaration.job
    allowed = tuple(declaration.allowed_sources)
    prohibited = tuple(declaration.prohibited_sources)

    # Rung 1 - the LABEL each value carries.
    for name in sorted(supplied):
        source = supplied[name].source
        if source == UNLABELLED:
            if allowed:
                findings.append(
                    Finding(
                        "{}.{}".format(job, name),
                        "carries no source label and {} declares an "
                        "allowed-source list ({}); a value that will not name "
                        "itself cannot be allowlisted".format(job, ", ".join(allowed)),
                    )
                )
            continue
        if source not in _BY_CLASS:
            findings.append(
                Finding(
                    "{}.{}".format(job, name),
                    "declares the undeclared source class {!r}; the declared "
                    "classes are {}".format(source, ", ".join(SOURCE_CLASS_NAMES)),
                )
            )
            continue
        if source in prohibited:
            findings.append(
                Finding(
                    "{}.{}".format(job, name),
                    "carries the PROHIBITED source class {!r} ({})".format(
                        source, _BY_CLASS[source].what
                    ),
                )
            )
        elif allowed and source not in allowed:
            findings.append(
                Finding(
                    "{}.{}".format(job, name),
                    "carries the source class {!r}, which {} does not allow "
                    "(allowed: {})".format(source, job, ", ".join(allowed)),
                )
            )

    # Rung 2 - the CONTENT of each value, whatever label it wore. This is the
    # rung that names an actionable slot, so it runs first and the residue rung
    # below reports only what it did not already attribute.
    attributed = set()
    for cls_name in prohibited:
        cls = _BY_CLASS.get(cls_name)
        if cls is None:
            continue
        for name in sorted(supplied):
            for label, rx in cls.markers:
                if rx.search(supplied[name].text):
                    attributed.add((cls_name, label))
                    findings.append(
                        Finding(
                            "{}.{}".format(job, name),
                            "carries {}, a marker of the PROHIBITED source "
                            "class {!r}, whatever label the slot wore".format(
                                label, cls_name
                            ),
                        )
                    )

    # Rung 3 - the residue, over the prompt as launched.
    if rendered is not None:
        findings.extend(_residue_findings(job, prohibited, rendered, attributed))
    return findings


def _residue_findings(job, prohibited, rendered, attributed):
    """`[Finding]` for prohibited markers present in the LAUNCHED prompt that no
    individual value accounted for.

    Its own function because it is the only rung that reads the render rather
    than the inputs, and the only one whose arithmetic is a count DELTA against
    the template's own body — the subtlety that lets the reviewer template
    contain the literal word it forbids without refusing every reviewer render.
    It also catches the marker formed at a JOIN, where template prose and a value
    are each clean and their concatenation is not; `attributed` is what keeps it
    from reporting a second time what rung 2 already pinned on a named slot.
    """
    findings = []
    for cls_name in prohibited:
        cls = _BY_CLASS.get(cls_name)
        if cls is None:
            continue
        for label, rx in cls.markers:
            if (cls_name, label) in attributed:
                continue
            baseline = len(rx.findall(rendered.body))
            landed = len(rx.findall(rendered.text))
            if landed > baseline:
                findings.append(
                    Finding(
                        "prompts.{}".format(job),
                        "the rendered prompt carries {} occurrence(s) of {} "
                        "that {} does not, a marker of the PROHIBITED source "
                        "class {!r}".format(
                            landed - baseline, label, rendered.template, cls_name
                        ),
                    )
                )
    return findings


# --- provenance ---------------------------------------------------------------
def provenance(rendered):
    """The prompt half of one session record: the job, the template path, the
    template hash and the rendered-prompt hash (SR-157).

    Returned from the renderer rather than assembled by the caller, so the
    record cannot describe a different render than the one that launched. The
    template hash covers the WHOLE asset including its dispatcher notes — those
    notes are reviewed prose too, and an edit to them is an edit to the
    reviewed artifact."""
    return Provenance(
        job=rendered.job,
        template=rendered.template,
        template_sha256=sha256_of(rendered.template_text),
        prompt_sha256=sha256_of(rendered.text),
    )


# --- the generated catalog ----------------------------------------------------
MISSING_HASH = "(template missing)"


def catalog(root, cfg=None):
    """`([CatalogRow], [Finding])` — one row per declared prompt, in the closed
    vocabulary's order: job, template, allowed and prohibited source classes,
    output parser, template hash.

    A missing template is a ROW with `(template missing)` for its hash plus a
    finding, not an omission: a catalog that silently drops the entry nobody can
    find is the worst possible answer to "which prompt is broken?"."""
    decls, findings = declarations(root, cfg=cfg)
    rows = []
    for job, decl in decls.items():
        text, read_findings = read_template(decl)
        findings.extend(read_findings)
        rows.append(
            CatalogRow(
                job=job,
                template=decl.template,
                allowed=tuple(decl.allowed_sources),
                prohibited=tuple(decl.prohibited_sources),
                output_schema=decl.output_schema,
                template_sha256=MISSING_HASH if text is None else sha256_of(text),
            )
        )
    return rows, findings


CATALOG_COLUMNS = (
    "Job",
    "Template",
    "Allowed sources",
    "Prohibited sources",
    "Output parser",
    "Template SHA-256",
)


def catalog_table(rows):
    """The catalog as one Markdown table. Generated on demand and never stored:
    a checked-in copy would be wrong the first time a template changed."""
    out = ["| " + " | ".join(CATALOG_COLUMNS) + " |"]
    out.append("|" + "|".join(["---"] * len(CATALOG_COLUMNS)) + "|")
    for r in rows:
        out.append(
            "| {} | `{}` | {} | {} | `{}` | `{}` |".format(
                r.job,
                r.template,
                ", ".join(r.allowed) or "-",
                ", ".join(r.prohibited) or "-",
                r.output_schema or "-",
                r.template_sha256,
            )
        )
    return "\n".join(out)


def refusal_lines(findings, module="prompt_render"):
    """The printable refusal for each finding, in the kit's one refusal shape:
    `<module>: REFUSED - <what> (<why>)` (contracts §5). Every finding is
    printed, never the first."""
    return ["{}: REFUSED - {} ({})".format(module, f.key, f.reason) for f in findings]


# --- CLI ----------------------------------------------------------------------
def _utf8_console():
    """Emit UTF-8 with LF line endings whatever the console does (the
    trace.py/check.py guard, plus the newline half).

    The newline half is this module's: a rendered prompt piped from stdout must
    be the bytes the golden fixture pins, and a Windows console that translates
    LF to CRLF on the way out would make the piped prompt differ from the
    hashed one."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", newline="\n")
        except (AttributeError, ValueError):
            pass


def _report(findings):
    for line in refusal_lines(findings):
        print(line, file=sys.stderr)


def _cmd_catalog(args):
    rows, findings = catalog(args.root)
    print(catalog_table(rows))
    if findings:
        _report(findings)
        return 1
    return 0


def _cmd_check(args):
    """Every declared prompt's template exists, parses, and declares source
    classes this module knows. The preflight a coordinator wants BEFORE it draws
    a model, not after."""
    decls, findings = declarations(args.root)
    for job, decl in decls.items():
        text, read_findings = read_template(decl)
        findings.extend(read_findings)
        if text is None:
            continue
        body = strip_dispatcher_block(text)
        present = template_slots(body)
        for name in sorted(set(decl.required_slots) - present):
            findings.append(
                Finding(
                    "{}.{}".format(job, name),
                    "is declared required but {} has no such slot".format(
                        decl.template
                    ),
                )
            )
        findings.extend(check_sources(decl, {}))
    if findings:
        _report(findings)
        return 1
    print("prompt_render: OK, {} declared prompt(s)".format(len(decls)))
    return 0


def _cmd_render(args):
    """Render one job's prompt to STDOUT and nowhere else — the stdin transport
    (`prompt_render.py render ... | <agent cli>`). Slots arrive in a FILE, never
    in argv: a brief-sized value would blow the command-line cap and would be
    visible to every process listing on the box."""
    decl, findings = declaration(args.root, args.job)
    if decl is None:
        _report(findings)
        return 1
    try:
        slots = json.loads(Path(args.slots).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as exc:
        _report(
            [Finding(args.slots, "is not a readable JSON slots file: {}".format(exc))]
        )
        return 1
    if not isinstance(slots, dict):
        _report([Finding(args.slots, "is not a JSON object of slot -> value")])
        return 1
    rendered, render_findings = render(decl, slots)
    findings.extend(render_findings)
    if rendered is None:
        _report(findings)
        return 1
    sys.stdout.write(rendered.text)
    if args.provenance:
        print(
            json.dumps(provenance(rendered)._asdict(), sort_keys=True), file=sys.stderr
        )
    return 0


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    sub = ap.add_subparsers(dest="cmd")

    cat = sub.add_parser("catalog", help="print the generated prompt catalog")
    cat.set_defaults(func=_cmd_catalog)

    chk = sub.add_parser("check", help="declared prompts vs the template files")
    chk.set_defaults(func=_cmd_check)

    ren = sub.add_parser("render", help="render one job's prompt to stdout")
    ren.add_argument("--job", required=True, help="a declared prompt/job name")
    ren.add_argument(
        "--slots", required=True, help="JSON file of slot -> value (never argv)"
    )
    ren.add_argument(
        "--provenance",
        action="store_true",
        help="also print the provenance record to stderr",
    )
    ren.set_defaults(func=_cmd_render)

    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
