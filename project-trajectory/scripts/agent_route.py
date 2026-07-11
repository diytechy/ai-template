#!/usr/bin/env python3
"""Model routing for the unattended coordinator — the enable-list + availability
selector and the fixed escalation policy (process-options.md "Unattended
operation" -> the routing/escalation subsection). Stdlib only, Python 3.8+.

This is the declared, legible half of heterogeneous implementer/reviewer
scheduling (AGENT_ROLES R6; the S8 rulings). It is **config, not a catalog**:

  - `docs/agents.csv` is the model REGISTRY — one row per usable model, keyed
    `[PROVIDER]-[MODEL_NAME]-[VERSION]` (`ANTHROPIC-OPUS-4.8`, `OPENAI-GPT-5.2`).
    The id is a join key, **never parsed** — Provider/Model/Version stay
    separate columns (machine truth); the id charset is uppercase + digits +
    hyphen + dot so dated snapshots and `-PREVIEW` tags are valid versions.
    Columns: `Id,Provider,Model,Version,Tier,CmdTemplate,Notes` with
    `Tier in {strong,medium,weak}` and a `CmdTemplate` carrying `{model}`/
    `{prompt}` slots. No vendored catalog: richer data lives in the maintained
    community registries (models.dev `api.json`; LiteLLM's model-prices JSON) —
    a documented pointer, not a copy.
  - `docs/agents-enabled` is the ENABLE-LIST — the ids this repo may use, in
    **preference order**, one per line (`#` comments allowed). It is the
    consent surface: routing selects only from this pool, and its **presence**
    is what turns on managed routing at all. Absent enable-list -> the loop
    keeps today's single `AGENT_CMD`/`AGENT_MODEL` behavior, so a fresh
    scaffold pays nothing (no silent model swap: consent = the enabled set +
    these declared rules).

Selection composes the phase's tier with the heterogeneity rules: reviewers
prefer two providers, at least one differing from the implementer's — *preferred
not required* (degraded availability is legal: one responding provider reviews
with two independent same-provider sessions; fresh context is the invariant).
A model whose session fails to start or stalls goes on **cooldown** (its limit
is probably exhausted) and is retried later; when no enabled model of the
preferred tier is available, selection walks the **next tier up — never a
weaker one**.

The escalation policy is **fixed and declared, not a learned router**
(per-project sample sizes are far too small for a bandit): win-stay/lose-shift
with a margin, an implementer-provider swap after consecutive failed review
gates, a tier rise only after the swap also fails, and paging the human on the
shared-failure regime, contradictory verdicts, or any tripwire. The constants
ship as legible per-repo-overridable defaults (calibration values, not spine
facts); the scoreboard (`score_reviews.py`) stays **advisory** — the declared
policy picks, nothing auto-optimizes.

Contracts: IF-044, IF-045 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path

# Tier strength, ascending. Selection never picks a WEAKER tier than requested
# (a hard rule: cheap-is-not-free, so an unavailable tier escalates UP).
TIER_ORDER = ("weak", "medium", "strong")

# Registry id charset: uppercase + digits + hyphen + dot, starting alphanumeric.
# Deliberately permissive on internal structure — the id is a join key, never
# parsed for its Provider/Model/Version (those are their own columns), and model
# names carry hyphens and dotted/dated version tags.
ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9.\-]*$")

REGISTRY_FIELDS = ("Id", "Provider", "Model", "Version", "Tier", "CmdTemplate", "Notes")

# Escalation calibration — legible per-repo-overridable defaults, NOT spine
# facts. Override per repo through the environment (the coordinator passes its
# own os.environ); a bad value falls back to the default rather than crashing a
# walk-away run.
DEFAULT_CONSTANTS = {
    "margin": 2,  # win-stay/lose-shift: swap the primary feedback source only on >= this
    "swap_after": 2,  # consecutive failed review gates before the implementer provider swaps
    "page_top_tier_fails": 2,  # top-tier failed gates before paging the human (shared-failure regime)
}
_CONST_ENV = {
    "margin": "AGENT_ROUTE_MARGIN",
    "swap_after": "AGENT_ROUTE_SWAP_AFTER",
    "page_top_tier_fails": "AGENT_ROUTE_PAGE_TOP_TIER_FAILS",
}


class Model:
    """One registry row. The id is opaque (a join key); Provider/Model/Version/
    Tier/CmdTemplate are the machine truth."""

    __slots__ = ("id", "provider", "model", "version", "tier", "cmd_template", "notes")

    def __init__(self, id, provider, model, version, tier, cmd_template, notes):
        self.id = id
        self.provider = provider
        self.model = model
        self.version = version
        self.tier = tier
        self.cmd_template = cmd_template
        self.notes = notes


def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (the kit's guard); routing
    reasons and model ids echoed to stdout stay ASCII, but a Notes cell needn't."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def load_registry(path):
    """Parse docs/agents.csv into {id: Model}, plus a list of error strings for
    malformed rows (a duplicate/invalid id, an out-of-vocabulary tier, a short
    row). Absent file -> ({}, []) so the caller degrades to today's behavior.
    utf-8/errors=replace so a stray byte degrades, never crashes."""
    path = Path(path)
    if not path.exists():
        return {}, []
    models, errors = {}, []
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError as exc:
        return {}, ["cannot read {}: {}".format(path, exc)]
    rows = list(csv.reader(text.splitlines()))
    if not rows:
        return {}, []
    header = [h.strip() for h in rows[0]]
    # Map the columns we need by name so column order is not load-bearing.
    idx = {name: header.index(name) for name in REGISTRY_FIELDS if name in header}
    for need in ("Id", "Provider", "Model", "Version", "Tier", "CmdTemplate"):
        if need not in idx:
            errors.append(
                "{}: header is missing the {!r} column".format(path.name, need)
            )
    if errors:
        return {}, errors

    def cell(row, name):
        i = idx[name]
        return row[i].strip() if i < len(row) else ""

    for row in rows[1:]:
        if not any(c.strip() for c in row):
            continue  # blank line
        mid = cell(row, "Id")
        if mid.startswith("#"):
            continue  # a commented row
        # A -000-style placeholder ships inert like every other registry.
        if mid.endswith("-000") or mid == "":
            continue
        if not ID_RE.match(mid):
            errors.append(
                "{}: id {!r} is not [A-Z0-9][A-Z0-9.-]* (uppercase + digits + "
                "hyphen + dot)".format(path.name, mid)
            )
            continue
        if mid in models:
            errors.append("{}: duplicate id {!r}".format(path.name, mid))
            continue
        tier = cell(row, "Tier").lower()
        if tier not in TIER_ORDER:
            errors.append(
                "{}: id {!r} has tier {!r}; expected one of {}".format(
                    path.name, mid, tier, "|".join(TIER_ORDER)
                )
            )
            continue
        tmpl = cell(row, "CmdTemplate")
        models[mid] = Model(
            id=mid,
            provider=cell(row, "Provider"),
            model=cell(row, "Model"),
            version=cell(row, "Version"),
            tier=tier,
            cmd_template=tmpl,
            notes=cell(row, "Notes") if "Notes" in idx else "",
        )
    return models, errors


def load_enabled(path):
    """The ordered enable-list (docs/agents-enabled): every non-empty, non-#
    line, in preference order. Absent/empty -> [] (routing off). This is the
    consent surface — its presence is what turns managed routing on."""
    path = Path(path)
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []
    out = []
    for ln in lines:
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            out.append(ln)
    return out


def available(cooldowns, model_id, now):
    """True when `model_id` is not cooling down. `cooldowns` maps id -> the epoch
    it is available again (the generalized rate-limit backoff, per-model)."""
    until = (cooldowns or {}).get(model_id)
    return until is None or until <= now


def cool(cooldowns, model_id, now, seconds):
    """Put `model_id` on cooldown until now+seconds (its limit is probably
    exhausted, or its session failed to start / stalled). In-place on the dict."""
    cooldowns[model_id] = now + max(0, seconds)


def select(
    enabled,
    registry,
    tier,
    now=0.0,
    cooldowns=None,
    exclude_providers=(),
    prefer_different=False,
):
    """Pick a model id from the enabled pool, or None. Returns (id, reason) — the
    reason is the line the coordinator LOGS before launch (no silent swap).

    Rules, in order:
      - Only enabled ids that exist in the registry and are not cooling down.
      - Walk from `tier` UP to strong; never select a weaker tier than asked.
      - Within a tier the enable-list order is the preference order.
      - When prefer_different, prefer an id whose provider is not in
        exclude_providers; if none qualifies, fall back to any available one
        (degraded availability is legal — same-provider review is allowed, it
        just earns a weaker corroboration signal).
    """
    cooldowns = cooldowns or {}
    exclude = set(exclude_providers or ())
    if tier not in TIER_ORDER:
        return None, "unknown tier {!r} (expected {})".format(
            tier, "|".join(TIER_ORDER)
        )
    start = TIER_ORDER.index(tier)
    for ti in range(start, len(TIER_ORDER)):
        this_tier = TIER_ORDER[ti]
        avail = [
            mid
            for mid in enabled
            if mid in registry
            and registry[mid].tier == this_tier
            and available(cooldowns, mid, now)
        ]
        if not avail:
            continue
        bumped = " (tier bumped up from {})".format(tier) if ti != start else ""
        if prefer_different:
            different = [m for m in avail if registry[m].provider not in exclude]
            if different:
                return different[0], "selected {} [{}]{}".format(
                    different[0], this_tier, bumped
                )
            # Degraded: only same-provider models are available. Legal — fresh
            # context is the invariant, provider diversity is best-effort.
            return avail[0], (
                "selected {} [{}]{} — DEGRADED: no different-provider model "
                "available, same-provider review (weaker corroboration)".format(
                    avail[0], this_tier, bumped
                )
            )
        return avail[0], "selected {} [{}]{}".format(avail[0], this_tier, bumped)
    return None, (
        "no enabled model available at tier {} or stronger (all cooled down or "
        "none enabled) — page/wait rather than select a weaker tier".format(tier)
    )


def load_constants(env=None):
    """The escalation constants: the per-repo-overridable defaults, each read from
    its env var when set to a valid non-negative int, else the default (a bad
    value never crashes the run)."""
    env = os.environ if env is None else env
    out = dict(DEFAULT_CONSTANTS)
    for key, var in _CONST_ENV.items():
        raw = env.get(var)
        if raw is None:
            continue
        try:
            val = int(raw)
        except (TypeError, ValueError):
            continue
        if val >= 0:
            out[key] = val
    return out


def _consecutive_changes_requested(rounds):
    """How many of the most recent rounds ended CHANGES-REQUESTED, contiguously."""
    n = 0
    for rnd in reversed(rounds):
        if str(rnd.get("verdict", "")).upper() == "CHANGES-REQUESTED":
            n += 1
        else:
            break
    return n


def escalate(rounds, constants=None, swapped=False, at_top_tier=False):
    """The fixed win-stay/lose-shift decision after a review round.

    `rounds` is the chronological history, each a dict:
      verdict          -> APPROVE | CHANGES-REQUESTED  (the merged round result)
      tier             -> the implementer tier this round ran at (weak/medium/strong)
      margin           -> substance margin between the two reviewers this round
      primary          -> the higher-substance provider this round (for win-stay)
      contradiction    -> True when the two reviewers gave opposite verdicts
      tripwire         -> True when any anti-gaming tripwire fired
    `swapped`/`at_top_tier` are the coordinator's applied-so-far state.

    Returns {'action', 'reason', 'next_primary'} with action in
    {continue, swap-implementer, tier-up, page-human}.
    """
    c = constants or DEFAULT_CONSTANTS
    if not rounds:
        return {
            "action": "continue",
            "reason": "no review round yet",
            "next_primary": None,
        }
    last = rounds[-1]

    # --- page-the-human conditions (the shared-failure / distrust regime) ------
    if last.get("tripwire"):
        return {
            "action": "page-human",
            "reason": "a tripwire fired — anti-gaming stop, never absorbed silently",
            "next_primary": None,
        }
    if (
        len(rounds) >= 2
        and last.get("contradiction")
        and rounds[-2].get("contradiction")
    ):
        return {
            "action": "page-human",
            "reason": "reviewers gave opposite verdicts twice running — the spec is likely ambiguous",
            "next_primary": None,
        }
    top_tier_fails = sum(
        1
        for r in rounds
        if r.get("tier") == "strong"
        and str(r.get("verdict", "")).upper() == "CHANGES-REQUESTED"
    )
    if top_tier_fails >= c["page_top_tier_fails"]:
        return {
            "action": "page-human",
            "reason": "{} top-tier review failures — the shared-failure regime (the spec is wrong, not the model)".format(
                top_tier_fails
            ),
            "next_primary": None,
        }

    # --- win-stay / lose-shift ------------------------------------------------
    consecutive = _consecutive_changes_requested(rounds)
    if consecutive >= c["swap_after"]:
        if not swapped:
            return {
                "action": "swap-implementer",
                "reason": "{} consecutive failed review gates — swap the implementer provider (cheap test for idiosyncratic failure)".format(
                    consecutive
                ),
                "next_primary": None,
            }
        if not at_top_tier:
            return {
                "action": "tier-up",
                "reason": "the provider swap also failed — raise the tier (only now, never before the swap)",
                "next_primary": None,
            }
        return {
            "action": "page-human",
            "reason": "swap and tier-up both exhausted at the top tier — page the human",
            "next_primary": None,
        }

    # A clean approve, or a single failure still inside the streak budget: keep
    # going. The higher-substance provider becomes next round's primary feedback
    # source only when this round's margin cleared the bar (win-stay).
    next_primary = last.get("primary") if last.get("margin", 0) >= c["margin"] else None
    return {
        "action": "continue",
        "reason": (
            "margin {} >= {}: {} leads next round's feedback".format(
                last.get("margin", 0), c["margin"], next_primary
            )
            if next_primary
            else "within the streak budget — continue with the current routing"
        ),
        "next_primary": next_primary,
    }


def failure_action(gate_policy):
    """What a page-the-human escalation does, keyed to docs/gate-policy (ruled).
    In every mode the causing WI and its hard-edge dependents PAUSE; the mode
    decides what happens around that. Redesign re-enters the change-intake flow
    (process.md §5 — linked, not restated). Returns a dict the coordinator enacts
    and logs."""
    gp = (gate_policy or "attended").strip().lower()
    if gp == "single-ratify":
        return {
            "mode": "single-ratify",
            "run_state": "RUNNING",
            "pause_wi": True,
            "keep_nondependent": True,
            "design_check": False,
            "note": "single-ratify: keep working non-dependent work items to completion; surface the block for ratification",
        }
    if gp == "autonomous":
        return {
            "mode": "autonomous",
            "run_state": "RUNNING",
            "pause_wi": True,
            "keep_nondependent": True,
            "design_check": True,
            "note": "autonomous: schedule a fresh strong-tier, different-provider design-check session to rule grind-through vs redesign, document every assumption, and continue (redesign re-enters process.md 5)",
        }
    return {
        "mode": "attended",
        "run_state": "NEEDS-HUMAN",
        "pause_wi": True,
        "keep_nondependent": False,
        "design_check": False,
        "note": "attended: start nothing new, let in-flight sessions close out, then alert the user",
    }


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description="Inspect the model registry + enable-list and the routed "
        "selection (the coordinator uses these functions in-process).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--registry", default="docs/agents.csv", help="the model registry CSV"
    )
    ap.add_argument(
        "--enabled", default="docs/agents-enabled", help="the ordered enable-list"
    )
    ap.add_argument(
        "--list", action="store_true", help="print the enabled pool and exit"
    )
    ap.add_argument(
        "--select", action="store_true", help="print the routed selection for --tier"
    )
    ap.add_argument("--tier", default="strong", choices=list(TIER_ORDER))
    ap.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="a provider to prefer against (repeatable); implies --prefer-different",
    )
    args = ap.parse_args(argv)

    registry, errors = load_registry(args.registry)
    for e in errors:
        print("agent_route: {}".format(e), file=sys.stderr)
    enabled = load_enabled(args.enabled)

    if args.list:
        if not enabled:
            print(
                "(no enable-list — routing off; today's AGENT_CMD/AGENT_MODEL behavior)"
            )
        for mid in enabled:
            m = registry.get(mid)
            if m:
                print("{:32} {:7} {}".format(m.id, m.tier, m.provider))
            else:
                print("{:32} {:7} (NOT in registry)".format(mid, "?"))
        return 1 if errors else 0

    if args.select:
        chosen, reason = select(
            enabled,
            registry,
            args.tier,
            exclude_providers=args.exclude,
            prefer_different=bool(args.exclude),
        )
        print(reason)
        return 0 if chosen else 1

    # Default: a terse status line.
    print(
        "registry={} models, enabled={} (routing {})".format(
            len(registry), len(enabled), "on" if enabled else "off"
        )
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
