#!/usr/bin/env python3
"""Need-form check: stakeholder-need cells stay in stakeholder language.

SN-033 (ratified 2026-08-13) commissions this check by its own acceptance text:
"A declared check reports the row and phrase when a need cell contains an
internal path, implementation-only identifier or process citation; a reviewed
exception list distinguishes names that are themselves user-facing interfaces."
A need written in internal engineering vocabulary can stay technically current
while becoming unreadable to the person whose intent it preserves — the failure
is an approved requirement spine no stakeholder can independently validate.

Stdlib only, like trace.py / check_vocab.py:

    python scripts/check_need_form.py [--root .] [--strict]

WHAT IT SCANS — `need` cells ONLY. SN-033 scopes itself by its own text: "the
rule applies specifically to each SN `need` cell, not to engineering
requirements or acceptance evidence". So the `why` and `acceptance` cells are
EXEMPT — measured at the ruling (2026-08-13), 16 of 27 acceptance cells carry
such tokens, correctly, because acceptance evidence legitimately names the
machinery that produces it. Example/placeholder rows (`SN-000`-style ids ending
in `-000`) are ignored, the same rule trace.py applies. The edge-case tier
carries no `need` field and so is naturally out of scope.

An ABSENT registry is a clean skip (the pre-scaffold case). A registry that is
PRESENT but yields zero scannable need cells — an empty file, or real rows
none of which carries a `need` field — is reported as VACUOUS, never clean:
zero need cells reading as a clean tier on exactly the registry this check
guards is the false green SN-008 forbids (the round-1 adversarial review drove
this: at DevBar-Reqs an emptied registry hard-fails nothing else in the
harness). A scaffold's `-000`-only registry stays clean — example rows are a
form, not a vacuous tier.

THE THREE TOKEN CLASSES, from SN-033's acceptance verbatim:

  - **internal path** — a slash-joined repo path (`docs/status.md`,
    `scripts/check.py`), including a one-level dot-free token that RESOLVES in
    the scanned tree (`docs/archive`). URLs — `scheme://` and scheme-less
    `www.` forms alike — are deliberately NOT matched: an address a need
    names is an external, stakeholder-visible reference, not repository
    internals. The exclusion is enforced by suppressing the whole URL span,
    so a path-shaped tail (`https://host/docs/status.md`) never reports —
    with the span stopping at prose delimiters (`,`/`;`) and the `www.` form
    requiring a multi-label host, so a genuine token abutting a URL and a
    local `www.assets/logo.png` both still report (review rounds 1–3). A
    sentence-final token's trailing full stop is stripped before the phrase
    is judged or reported, so its reviewed exception matches.
  - **implementation-only identifier** — a code-suffixed filename
    (`trace.py`, `stack.ini`), an underscore-joined identifier
    (`human_ratification_through`), or a `--flag` token.
  - **process citation** — a sub-stakeholder registry id (`SR-137`, `WI-454`,
    ...) or a `§`-section reference. A stakeholder should not need the process
    docs to recognize the outcome they asked for. `SN-###` is deliberately NOT
    in this class: the SN registry is the stakeholder's own document, so a need
    pointing at a sibling need keeps the reader at the stakeholder tier (the
    live case at landing: SN-025's need hands its launcher clause to SN-034 by
    id, on OI-17's 2026-08-13 ruling).

THE EXCEPTION LIST — `docs/need-form-allow`, one reviewed entry per line:

    <token> — <reason it is a user-facing interface>

`#` comments and blank lines are ignored. A line with NO ` — ` separator
declares nothing (the declared-absences fail-soft rule, in the loud direction:
a malformed entry can only ever fail to silence a finding, never silence one by
accident). The list SHIPS EMPTY — the file is not scaffolded and an absent file
declares nothing — because on the day this check landed the live registry was
measured clean (0 of 27 need cells), and the point of landing it then was to
lock that state in: the FIRST row to dirty the tier is the one that reports.

SEVERITY IS WARN-FIRST, ALWAYS, in the shipped wiring. check.py runs this step
with no `--strict` at every bar — deliberately unlike check_vocab, which
promotes from DevBar-Tests on. Promoting this check to a gate is an owner
ruling that has not been made (WI-454's scope guard): a form heuristic over
stakeholder prose must not block work on the strength of a regex. `--strict`
exists for a repo that makes that ruling for itself.

Contracts: IF-121, IF-122 — the seams this module declares (process.md §8; rows
of record in docs/requirements/interfaces.toml).
"""

import argparse
import re
import sys
from pathlib import Path

# Sibling: the spine's registry CARRIER (the check_docs.py idiom) — the needs
# registry answers through whichever of TOML/CSV-era markdown is live, and an
# unreadable registry refuses loudly instead of scanning as empty.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

# The needs registry and the reviewed exception list, repo-root-relative.
NEEDS = "docs/requirements/stakeholder-needs"
ALLOW = "docs/need-form-allow"

# The entry separator the exception list requires — an em-dash with spaces, the
# same separator docs/declared-absences uses. Requiring it is what makes every
# entry carry its reviewed reason.
ALLOW_SEP = " — "

# The three token classes, each labelled with SN-033's own vocabulary so a
# finding names the class the acceptance names. Order matters only for which
# label a doubly-matching token gets (a path is reported as a path, not as the
# identifier its basename would also match).
CLASSES = (
    (
        "internal path",
        # Slash-joined path segments. `(?<![\w:/])` refuses mid-token starts;
        # URL interiors are handled by the _URL span suppression in
        # need_findings (the lookbehind alone let a `host.tld/docs/x.md` tail
        # through — the round-1 review's driven find). The segment charset is
        # the kit's own path alphabet. A single-slash, dot-free token is then
        # judged by _looks_like_path below: "subjective/perceptual" and
        # "requirement/test" are English either/or pairs that resolve to
        # nothing on disk (both live in the ratified registry), while
        # `docs/archive` names a real directory and reports. The residual,
        # documented miss is a one-level dot-free path whose target no longer
        # exists in the scanned tree.
        re.compile(r"(?<![\w:/])[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.*{}-]+)+"),
    ),
    (
        "implementation identifier",
        re.compile(
            # a code-suffixed filename ...
            r"\b[\w-]+\.(?:py|md|toml|csv|ini|ya?ml|sh|ps1|cmd|command|html|json)\b"
            # ... or an underscore-joined identifier ...
            r"|\b[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)+\b"
            # ... or a --flag token.
            r"|(?<![\w-])--[A-Za-z][\w-]+\b"
        ),
    ),
    (
        "process citation",
        # SN deliberately absent — see the docstring's class notes.
        re.compile(
            r"\b(?:SR|LLR|TC|WI|OI|IF|CMP|PB|REPO|MOD|PART|ASSET|DP)-\d+\b"
            r"|§\s*\d+"
        ),
    ),
)


# A URL span: `scheme://` — or the scheme-less `www.` form — up to the next
# whitespace or prose delimiter. Findings inside one are suppressed whole: an
# external address is stakeholder-visible however path-shaped its tail, and
# suppressing the SPAN (not just refusing the match start) is what keeps the
# identifier class from re-matching a `status.md` inside it. Two round-3
# narrowings, both silent-miss classes the adversarial review drove: the span
# STOPS at `,`/`;` so an abutting separate token (`...status.md,docs/gate.md`)
# still reports, and the `www.` form requires a MULTI-LABEL host
# (`www.example.test`) so a local `www.assets/logo.png` is a path, not an
# address — a real scheme-less URL practically always carries a second dot
# before its first slash. (`www.` joined at round 2: a scheme-less address is
# the same external reference.)
_URL = re.compile(
    r"(?:\b[a-z][a-z0-9+.-]*://|\bwww\.(?=[^\s/,;]+\.))[^\s,;]+", re.IGNORECASE
)


def _looks_like_path(token, root=None):
    """True when a slash-joined token reads as a repo path rather than an
    English either/or pair: two or more slashes, any segment carrying a dot
    (a file suffix), or — the remaining one-level dot-free shape — a token
    that RESOLVES in the scanned tree (`docs/archive` names a real directory;
    `subjective/perceptual` names nothing). With no root to resolve against,
    the one-level dot-free shape stays exempt."""
    if token.count("/") >= 2 or any("." in seg for seg in token.split("/")):
        return True
    if root is None:
        return False
    try:
        return (Path(root) / token).exists()
    except (OSError, ValueError):  # unstattable charset member (e.g. `*`)
        return False


def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (the trace.py/check_docs.py
    guard — a non-ASCII phrase must not wedge a cp1252 console)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def load_allow(root):
    """The reviewed exception tokens from `docs/need-form-allow`, as a set.

    Absent file: empty set (the list ships empty). A line with no separator
    declares nothing — loud-direction fail-soft: the worst a malformed entry
    can do is leave a finding reported."""
    path = Path(root) / ALLOW
    if not path.is_file():
        return set()
    out = set()
    for line in path.read_text(encoding="utf-8-sig", errors="replace").split("\n"):
        line = line.strip()
        if not line or line.startswith("#") or ALLOW_SEP not in line:
            continue
        token = line.split(ALLOW_SEP, 1)[0].strip()
        if token:
            out.add(token)
    return out


def need_findings(needs, allow, root=None):
    """`[(row_id, class_label, phrase)]` over the `need` cells of `needs`.

    One finding per distinct (row, phrase): a token repeated inside one cell is
    one phrase to rewrite. A phrase on the reviewed exception list is skipped —
    that is the list's whole job (SN-033: a name that IS the user-facing
    interface belongs in the need). `root`, when given, lets the path class
    resolve one-level dot-free tokens against the scanned tree."""
    out = []
    for row in needs:
        rid = row.get("id", "")
        if not rid or rid.endswith("-000"):  # example/placeholder rows
            continue
        cell = row.get("need") or ""
        if not cell:
            continue
        # URL spans are pre-suppressed: every class match inside one is the
        # tail of an external address, not repository internals.
        seen = set()
        spans = [(m.start(), m.end()) for m in _URL.finditer(cell)]
        for label, rx in CLASSES:
            for m in rx.finditer(cell):
                phrase = m.group(0)
                if label == "internal path":
                    # A sentence-final token drags its full stop into the
                    # match (the segment charset allows dots). Strip it BEFORE
                    # judging and reporting: `docs/status.md.` must name — and
                    # allow-list as — `docs/status.md`, and a sentence-final
                    # English pair (`requirement/test.`) must not read its
                    # punctuation as a file suffix (review round 2).
                    phrase = phrase.rstrip(".")
                    if not _looks_like_path(phrase, root):
                        continue
                # One token, one finding: a later class re-matching INSIDE an
                # already-reported span (`status.md` inside `docs/status.md`)
                # is the same phrase to rewrite, not a second one.
                if any(a <= m.start() and m.end() <= b for a, b in spans):
                    continue
                spans.append((m.start(), m.end()))
                if phrase in allow or phrase in seen:
                    # An allow'd span still suppresses its inner tokens — the
                    # reviewed exception covers the whole name, not just the
                    # exact charspan a later class would re-match inside it.
                    continue
                seen.add(phrase)
                out.append((rid, label, phrase))
    return out


def scan(root):
    """`(findings, scanned_count, vacuous)` for the repo at `root`.

    `vacuous` is True when the registry file is PRESENT but yields zero
    scannable need cells — an empty file, or real (non-`-000`) rows none of
    which carries a `need` cell. An absent registry is not vacuous (the
    pre-scaffold clean skip), and neither is a `-000`-only scaffold registry:
    example rows are a blank form, not an emptied tier."""
    base = Path(root) / NEEDS
    needs = spine_carrier.load_needs(base)
    allow = load_allow(root)
    scanned = [n for n in needs if (n.get("need") and not n["id"].endswith("-000"))]
    real = [n for n in needs if n.get("id") and not n["id"].endswith("-000")]
    present = spine_carrier.resolve(base, spine_carrier.NEED_CARRIERS) is not None
    vacuous = present and (not needs or bool(real and not scanned))
    return need_findings(needs, allow, root), len(scanned), vacuous


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".", help="repo root (default: .)")
    ap.add_argument(
        "--strict",
        action="store_true",
        help="promote findings from WARN to ERROR (exit 1). NOT wired by "
        "check.py at any bar — gating on this check needs an owner ruling "
        "(WI-454's scope guard).",
    )
    args = ap.parse_args()

    findings, scanned, vacuous = scan(args.root)
    label = "check_need_form: ERROR" if args.strict else "check_need_form: WARN"
    if vacuous:
        print(
            "{} - the needs registry is present but yields no scannable need "
            "cell (empty file, or rows with no need field) — a vacuous read "
            "is not a clean tier: the registry this check guards has been "
            "emptied or lost its schema (SN-008; round-1 review find)".format(label)
        )
    for rid, cls, phrase in findings:
        article = "an" if cls[0] in "aeiou" else "a"
        print(
            "{} - {} need cell carries {} {}: '{}' — a stakeholder need names "
            "the outcome in the reader's language (SN-033); if this token IS a "
            "user-facing interface name, add it to {} with its reason".format(
                label, rid, article, cls, phrase, ALLOW
            )
        )
    total = len(findings) + (1 if vacuous else 0)
    if not total:
        print(
            "check_need_form: clean ({} need cell(s); no internal path, "
            "implementation identifier or process citation).".format(scanned)
        )
        return 0
    print(
        "check_need_form: {} finding(s) across {} need cell(s){}".format(
            total, scanned, "" if args.strict else " (warn-first)"
        )
    )
    return 1 if args.strict else 0


if __name__ == "__main__":
    sys.exit(main())
