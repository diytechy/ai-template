#!/usr/bin/env python3
"""Redacted dual-plan brief assembler + the three hat prompt-map keys (DP-001
selected plan P2 / WI-195; the protocol is process-options.md "Dual-plan
decomposition").

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX). This is the
brief-assembly half of the dual-plan round: it turns an ALLOWLIST-ONLY input set
into the planner/critic/arbiter prompts the coordinator sends to fresh sessions.
Redaction is BY CONSTRUCTION, not by review — the module can read exactly two
files under the repo root:

    docs/requirements/system-requirements.csv  (the SR surface)
    docs/requirements/interfaces.csv           (the IF registry excerpt)

plus the strings the caller passes in (the goal brief, the coverage report, the
plan texts, the rubric). It never opens docs/status.md, docs/log.md, a
docs/reviews/ verdict, or any self-assessment, so a planner/critic/arbiter can
never be handed the driver's own notes — the leak that collapses independent
finding rates (agent_loop's REVIEWER_PROMPT / CRITIQUE_PROMPT enforce the same
rule for the review/critique hats). THE ALLOWLIST IS THE CONSTRUCTION: the only
file reads in this module are the two registries above.

The three hats register on the existing S8 --prompt-map / AGENT_PROMPT_MAP
override (agent_loop.py; each entry names a prompt-template FILE). `HAT_KEYS`
maps each hat's override key to its shipped kit template; `load_template(hat,
override)` returns the operator's override FILE when one is wired, else the kit
template shipped under project-trajectory/prompts/ (located relative to this
script, the way bootstrap.py locates kit files).

`assemble(hat, slots, template_text)` does a STRICT slot-fill of the template's
`{{NAME}}` placeholders: an unknown slot key or an unfilled placeholder both
raise ValueError, so a half-filled brief (a hole where a redacted input should
be) can never reach a session.

Small helpers (_utf8_console, the CSV loader) are duplicated from siblings per
the kit's independently-copyable-script convention (F5). Usage (the CLI is a
documentation aid; the module is library-first):

    python scripts/plan_briefs.py surface [--root .]   # print the SR+IF surface
    python scripts/plan_briefs.py hats                 # print the hat->template map

Contracts: IF-059, IF-100, IF-108 — the interface seam this module declares (process.md §8; rows
of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import re
import sys
from pathlib import Path

# Sibling: the spine's registry CARRIER (repo-lock D-5/D-6) — the one home for
# the TOML tier tables, the key->column vocabulary and both readers. Run as a
# subprocess this script's own dir is sys.path[0] so a plain import resolves;
# the guard covers an in-process import (a test) whose sys.path does not yet
# carry scripts/ — the sanctioned-sibling idiom trace.py uses for trace_text.
try:
    import spine_carrier
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import spine_carrier

# The sanctioned-sibling import (the agent_loop / gen_trajectory idiom): the
# prompt-template LOCATION and the dispatcher-notes rule have one home now that
# the session-engine briefs are files too.
try:
    import prompts
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import prompts

# --- the three dual-plan hats and their prompt-map override keys --------------
# Each key is the phase key an operator wires on --prompt-map / AGENT_PROMPT_MAP
# (agent_loop.py); the value is the kit template shipped under prompts/.
HAT_PLANNER = "DUALPLAN-PLANNER"
HAT_CRITIC = "DUALPLAN-CRITIC"
HAT_ARBITER = "DUALPLAN-ARBITER"

HAT_KEYS = {
    HAT_PLANNER: "dual-plan-planner.template.md",
    HAT_CRITIC: "dual-plan-critic.template.md",
    HAT_ARBITER: "dual-plan-arbiter.template.md",
}

# Kit files are located relative to this script (bootstrap.py's KIT pattern).
KIT = Path(__file__).resolve().parent.parent  # the project-trajectory/ folder
PROMPTS = KIT / "prompts"

# The ONLY two files this module may read — the redaction allowlist, as paths
# relative to the caller-supplied repo root.
SR_CSV = "docs/requirements/system-requirements.csv"
IF_CSV = "docs/requirements/interfaces.csv"

# The registry columns each surface exposes (a stable, minimal excerpt — never
# the whole row, so Rationale/Notes prose never rides along into a brief).
SR_SURFACE_COLUMNS = ("SR-ID", "Title", "Requirement")
IF_SURFACE_COLUMNS = (
    "IF-ID",
    "Direction",
    "ThisProject",
    "Counterpart",
    "Status",
    "Contract",
)

# A `{{NAME}}` slot placeholder (NAME is word chars, as the shipped templates use).
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")


def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (the trace.py/check.py guard)."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# --- small self-contained CSV loader (duplicated per the F5 rule) -------------
def _load_rows(path):
    """Read a CSV registry into a list of dict rows (utf-8-sig tolerates the BOM
    some editors add), or [] when the file is absent — absence is 'nothing to
    surface', never a crash."""
    p = Path(path)
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


# --- prompt-template loading (kit template or operator override) --------------
def load_template(hat, override=None):
    """The prompt-template TEXT for a hat: the operator's --prompt-map override
    FILE when `override` is a path, else the kit template shipped under
    project-trajectory/prompts/. `hat` must be a known HAT_KEYS key."""
    if hat not in HAT_KEYS:
        raise KeyError(
            "unknown hat {!r} (expected one of {})".format(
                hat, ", ".join(sorted(HAT_KEYS))
            )
        )
    path = Path(override) if override else PROMPTS / HAT_KEYS[hat]
    return path.read_text(encoding="utf-8")


def strip_dispatcher_block(text):
    """Return the prompt body with a leading HTML-comment dispatcher block
    (`<!-- ... -->`, the operator notes at the top of each kit template)
    removed. Text without a leading comment block is returned left-stripped and
    otherwise unchanged.

    DELEGATES to `prompts.strip_dispatcher_block` (plan §8): once the worker /
    reviewer / critique briefs became files too, two copies of this three-line
    rule would have been an intra-repo duplicate of the one thing every kit
    template's header depends on. The name stays here because `plan_runner`
    and the hat tests call it through this module."""
    return prompts.strip_dispatcher_block(text)


# --- the allowlist-only registry surface --------------------------------------
def _cell(row, key):
    return (row.get(key) or "").strip()


def _skip(row_id):
    """A blank id or an inert `-000` example row contributes nothing."""
    return not row_id or row_id.endswith("-000")


def _sr_surface(rows):
    """The SR surface: one entry per real SR row — `- SR-### — <Title>` plus the
    Requirement text, id + text only."""
    out = []
    for r in rows:
        sid = _cell(r, "SR-ID")
        if _skip(sid):
            continue
        out.append("- {} — {}".format(sid, _cell(r, "Title")))
        req = _cell(r, "Requirement")
        if req:
            out.append("  {}".format(req))
    return "\n".join(out)


def _if_registry(rows):
    """The IF registry excerpt as a markdown table over IF_SURFACE_COLUMNS."""
    out = ["| " + " | ".join(IF_SURFACE_COLUMNS) + " |"]
    out.append("|" + "|".join(["---"] * len(IF_SURFACE_COLUMNS)) + "|")
    for r in rows:
        iid = _cell(r, "IF-ID")
        if _skip(iid):
            continue
        cells = [
            _cell(r, c).replace("|", r"\|").replace("\n", " ")
            for c in IF_SURFACE_COLUMNS
        ]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def build_surface(root):
    """The allowlist-only registry surface the briefs embed, as `{slot: text}`
    keyed by the planner/critic slot names: `SR_SURFACE` (the SR rows — id,
    title, requirement) and `IF_REGISTRY` (the interfaces.csv excerpt — id,
    direction, endpoints, status, contract).

    Reads ONLY system-requirements.csv and interfaces.csv under `root`. That
    two-file read IS the redaction boundary: status.md, log.md, and every
    self-assessment are unreachable because this function never names them."""
    root = Path(root)
    return {
        "SR_SURFACE": _sr_surface(spine_carrier.load(root / SR_CSV, "SR-ID")),
        "IF_REGISTRY": _if_registry(_load_rows(root / IF_CSV)),
    }


# --- strict slot fill ---------------------------------------------------------
def _placeholders(text):
    """The set of `{{NAME}}` placeholder names present in `text`."""
    return set(PLACEHOLDER_RE.findall(text))


def assemble(hat, slots, template_text):
    """Strict slot-fill of the `{{NAME}}` placeholders in `template_text`.

    Every provided slot key must name a placeholder present in the template
    (unknown keys raise ValueError); after the fill, ANY placeholder left
    unprovided raises ValueError naming it — a half-filled brief (a hole where a
    redacted input belongs) never reaches a session. `hat` labels the error
    context. Returns the filled text.

    Note the unfilled check is computed from the template's own placeholder set,
    not by re-scanning the output, so a slot VALUE that happens to contain a
    `{{...}}`-looking string is passed through verbatim rather than mis-flagged."""
    # The strictness itself lives ONCE, in prompts.strict_check — the two slot
    # syntaxes differ, the rule they enforce does not. `ValueError` is passed
    # through so this function's exception contract (and the tests that assert
    # it) are unchanged by the extraction.
    prompts.strict_check(
        hat,
        present=_placeholders(template_text),
        provided=set(slots),
        form="{{NAME}}",
        error=ValueError,
    )
    return PLACEHOLDER_RE.sub(lambda m: str(slots[m.group(1)]), template_text)


# --- CLI (documentation aid; the module is library-first) ---------------------
def _cmd_surface(args):
    surface = build_surface(args.root)
    print("## Requirement surface (system-requirements.csv)\n")
    print(surface["SR_SURFACE"] or "(no SR rows)")
    print("\n## Declared interface seams (interfaces.csv)\n")
    print(surface["IF_REGISTRY"])
    return 0


def _cmd_hats(args):
    for k in sorted(HAT_KEYS):
        print("{:18s} {}".format(k, HAT_KEYS[k]))
    return 0


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument(
        "--root", default=".", help="repo root holding docs/requirements/ (default: .)"
    )
    sub = ap.add_subparsers(dest="cmd")

    surf = sub.add_parser("surface", help="print the allowlist-only SR + IF surface")
    surf.set_defaults(func=_cmd_surface)

    hats = sub.add_parser("hats", help="print the hat -> kit template map")
    hats.set_defaults(func=_cmd_hats)

    args = ap.parse_args(argv)
    if not getattr(args, "cmd", None):
        ap.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
