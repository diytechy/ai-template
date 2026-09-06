#!/usr/bin/env python3
"""Redacted dual-plan brief assembler + the three hat prompt-map keys (DP-001
selected plan P2 / WI-195; the protocol is process-options.md "Dual-plan
decomposition").

Stack-agnostic, standard-library only (Python 3.11+, Windows/POSIX). This is the
brief-assembly half of the dual-plan round: it turns an ALLOWLIST-ONLY input set
into the planner/critic/arbiter prompts the coordinator sends to fresh sessions.
Redaction is BY CONSTRUCTION, not by review — the module can read exactly two
files under the repo root:

    docs/requirements/system-requirements.toml  (the SR surface)
    docs/requirements/interfaces.toml           (the IF registry excerpt)

plus the strings the caller passes in (the goal brief, the coverage report, the
plan texts, the rubric). It never opens docs/status.md, docs/log.md, a
docs/reviews/ verdict, or any self-assessment, so a planner/critic/arbiter can
never be handed the driver's own notes — the leak that collapses independent
finding rates (agent_loop's REVIEWER_PROMPT / CRITIQUE_PROMPT enforce the same
rule for the review/critique hats). `build_surface` keeps that two-file
allowlist; the separate hat surface reads the roster and explicit parents.

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

THE HATS ROSTER RIDES THE PLANNER BRIEF (SN-036, ruled at OI-19 2026-08-13).
The planner brief is what this repo mechanizes as *the decomposition brief*, so
it is where a declared expert perspective has to arrive if it is to constrain a
decomposition at all. `hat_surface(root, context)` fills `{{HAT_QUESTIONS}}`
from `docs/requirements/hats.toml` via the `hats` sibling; every applicable
hat's question lands in the brief, so the session faces each perspective rather
than being trusted to remember it.

Those reads are deliberately NOT inside `build_surface`: the two-file allowlist
is `build_surface`'s own contract and stays exactly as it was. The redaction
INVARIANT is unchanged either way — the roster and explicit parent carriers are
declared inputs, not the driver's notes, not `docs/status.md`, not a
self-assessment — and keeping the widening in separately named functions means
the boundary that matters is still readable in one place.

`{{HAT_QUESTIONS}}` is filled only when the (possibly operator-overridden)
template DECLARES it — `declares_slot` is the guard. A strict fill rejects an
unknown slot key, so unconditionally passing it would have broken every
operator override authored before this slot existed.

Small helpers (_utf8_console, the CSV loader) are duplicated from siblings per
the kit's independently-copyable-script convention (F5). Usage (the CLI is a
documentation aid; the module is library-first):

    python scripts/plan_briefs.py surface [--root .]   # print the SR+IF surface
    python scripts/plan_briefs.py hats                 # print the hat->template map
"""

import argparse
import re
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console
from kitlib.spine import refs as _refs

# Sibling: the spine's registry CARRIER — the one home for
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

# Sibling: the HATS ROSTER reader (SN-036 / OI-19) — the roster's parse rules,
# its applies_when grammar and the absent-vs-malformed split have ONE home, so
# a second composer that grows hats later inherits them rather than re-deciding
# what a broken roster means.
try:
    import hats as hats_roster
except ImportError:  # pragma: no cover - in-process fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import hats as hats_roster

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
SR_CSV = "docs/requirements/system-requirements.toml"
IF_CSV = "docs/requirements/interfaces.toml"

# The registry columns the IF surface exposes (a stable, minimal excerpt — never
# the whole row, so Rationale/Notes prose never rides along into a brief). The SR
# surface is a bullet list rather than a table, so it names its own cells in
# `_sr_surface` instead of reading a column tuple.
#
# `Status` LEFT THIS TUPLE AT WI-443 and its departure is the reason OI-14 part B
# was urgent rather than tidy. Every cell here is handed to a planning model as
# authority (process.md §8), and `Status` was an UNDECLARED column — absent from
# §8's field list, validated by no check, and carrying `Stable` while the row's
# `Stability` cell said something different with the same word. The column
# retired; `Signal` is deliberately NOT promoted in its place, because a brief
# needs the surface, not the schema. What a planner sees is the seam and its
# contract.
#
# `Owner` JOINED at the 2026-08-15 rework, and it is the one addition that
# answers the complaint this surface caused: reading who serves a seam took
# three cells (`Direction` + `ThisProject` + `Counterpart`) whose meanings swap
# on the first, and a planning model was being handed that puzzle as fact. One
# id-typed cell says it instead (Q1, 2026-08-15a). WI-455 then removed the
# puzzle at the source: the three cells became `Provider` + `Consumers`, which
# read the same way on every row. The endpoint cells still name the surface,
# which is the only place it is named — and `Provider` is EMPTY on a row whose
# owner derives it, which is honest for a brief: the `Owner` column beside it is
# where that seam's provider is stated.
IF_SURFACE_COLUMNS = (
    "IF-ID",
    "Owner",
    "Requestors",
    "Consumers",
    "Channel",
    "Data",
)

# A `{{NAME}}` slot placeholder (NAME is word chars, as the shipped templates use).
PLACEHOLDER_RE = re.compile(r"\{\{(\w+)\}\}")


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
    Requirement text, id + text only.

    The three cells named here ARE the redaction contract: a stable, minimal
    excerpt, never the whole row, so Rationale/Notes prose never rides along
    into a brief. Widening it is a deliberate act, not a convenience."""
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
    title, requirement) and `IF_REGISTRY` (the interfaces registry excerpt — id,
    owner, endpoints, contract).

    Reads ONLY the SR and IF registries under `root`. That
    two-file read IS the redaction boundary: status.md, log.md, and every
    self-assessment are unreachable because this function never names them."""
    root = Path(root)
    return {
        "SR_SURFACE": _sr_surface(spine_carrier.load(root / SR_CSV, "SR-ID")),
        "IF_REGISTRY": _if_registry(spine_carrier.load(root / IF_CSV, "IF-ID")),
    }


# --- the hats roster surface (SN-036) -----------------------------------------
# The planner-brief slot the applicable perspectives land in.
HAT_QUESTIONS_SLOT = "HAT_QUESTIONS"
NEEDS_REL = hats_roster.NEEDS_REL

# Re-exported so a composer needs one seam, not two, to put hats in a brief.
HatsError = hats_roster.HatsError
hat_context_for_work_item = hats_roster.context_from_work_item
hat_context_for_need = hats_roster.context_from_need


def hat_surface(root, context):
    """`{HAT_QUESTIONS: <block>}` — the declared perspectives this decomposition
    must face, as the markdown block the planner template embeds.

    ABSENT IS OPT-OUT: with no `docs/requirements/hats.toml` the block is the
    roster module's stated no-hats line and the brief goes out without hats — a
    layer, not a floor. A roster that EXISTS and does not parse raises
    `HatsError`, which the caller turns into a page: silently briefing a
    decomposition with no perspective, because the file listing them was
    broken, is the failure this refusal exists for."""
    chosen = hats_roster.applicable(hats_roster.load(root), context)
    return {HAT_QUESTIONS_SLOT: hats_roster.brief_block(chosen)}


def _canonical_need_ref(spec):
    """Return an exact SN id from a canonical needs-carrier SpecRef, or None."""
    pathpart, separator, fragment = spec.partition("#")
    canonical = {NEEDS_REL, Path(NEEDS_REL).with_suffix(".md").as_posix()}
    if pathpart not in canonical or not separator or not fragment.strip():
        return None
    fragment = fragment.strip()
    if not re.fullmatch(r"SN-\d+", fragment):
        raise HatsError("need SpecRef requires an exact SN-ID fragment: " + repr(spec))
    return fragment


def _hat_parent_context(work_context, need):
    """Combine WI tags with one need, without combining sibling needs."""
    context = hats_roster.context_from_need(need)
    tags = list(
        dict.fromkeys((*work_context.get("tags", ()), *context.get("tags", ())))
    )
    if tags:
        context["tags"] = tags
    return context


def _parent_need_ids(root, row):
    """Exact SN parents reached from explicit SR-Refs and canonical SpecRef."""
    sr_refs = _refs(row.get("SR-Refs"))
    need_ids = {}
    if sr_refs:
        if spine_carrier.resolve(root / SR_CSV) is None:
            raise HatsError(
                "cannot resolve declared SR-Refs {}: system-requirements carrier "
                "is absent".format(", ".join(sr_refs))
            )
        sr_rows = {
            str(sr.get("SR-ID") or ""): sr
            for sr in spine_carrier.load(root / SR_CSV, "SR-ID", keep_examples=False)
        }
        missing_srs = [ref for ref in sr_refs if ref not in sr_rows]
        if missing_srs:
            raise HatsError(
                "cannot resolve declared SR-Refs: unknown SR id(s) "
                + ", ".join(missing_srs)
            )
        for sr_id in sr_refs:
            for need_id in _refs(sr_rows[sr_id].get("SN-Refs")):
                need_ids.setdefault(need_id, None)

    spec = str(row.get("SpecRef") or "").strip()
    spec_need = _canonical_need_ref(spec)
    if spec_need:
        need_ids.setdefault(spec_need, None)
    return need_ids


def _parent_need_contexts(root, row, work_context):
    """One WI+SN context per parent; declared missing inputs refuse."""
    need_ids = _parent_need_ids(root, row)
    if not need_ids:
        return []
    if spine_carrier.resolve(root / NEEDS_REL, spine_carrier.NEED_CARRIERS) is None:
        raise HatsError(
            "cannot resolve declared stakeholder-need references {}: "
            "stakeholder-needs carrier is absent".format(", ".join(need_ids))
        )
    needs = {
        str(need.get("id") or ""): need
        for need in spine_carrier.load_needs(root / NEEDS_REL)
    }
    missing_needs = [need_id for need_id in need_ids if need_id not in needs]
    if missing_needs:
        raise HatsError(
            "cannot resolve declared stakeholder-need reference(s): unknown "
            "SN id(s) {}".format(", ".join(missing_needs))
        )
    return [_hat_parent_context(work_context, needs[need_id]) for need_id in need_ids]


def hat_surface_for_work_item(root, row):
    """Hat surface for a WI and each exact parent, without merging parents."""
    root = Path(root)
    roster = hats_roster.load(root)
    if not roster:  # absent/empty roster is the declared opt-out
        return {HAT_QUESTIONS_SLOT: hats_roster.brief_block(roster)}
    work_context = hats_roster.context_from_work_item(row)
    contexts = [work_context] + _parent_need_contexts(root, row, work_context)
    selected = {
        hat["name"]
        for context in contexts
        for hat in hats_roster.applicable(roster, context)
    }

    chosen = [hat for hat in roster if hat["name"] in selected]
    return {HAT_QUESTIONS_SLOT: hats_roster.brief_block(chosen)}


# --- strict slot fill ---------------------------------------------------------
def _placeholders(text):
    """The set of `{{NAME}}` placeholder names present in `text`."""
    return set(PLACEHOLDER_RE.findall(text))


def declares_slot(template_text, name):
    """Whether `template_text` declares the `{{name}}` placeholder.

    The guard for an OPTIONAL slot. `assemble` rejects a slot key the template
    does not declare, so a caller adding a slot to the shipped template must
    ask before filling it — otherwise every operator override written against
    the older template stops composing at all."""
    return name in _placeholders(template_text)


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
    print("## Requirement surface (system-requirements.toml)\n")
    print(surface["SR_SURFACE"] or "(no SR rows)")
    print("\n## Declared interface seams (interfaces.toml)\n")
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
