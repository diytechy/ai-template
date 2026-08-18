#!/usr/bin/env python3
"""The substance scorer — score a review verdict block by how USEFUL it is, not
how long it is (process-options.md "Unattended operation" -> the routing/
escalation subsection). Stdlib only, Python 3.11+.

Review-substance-as-a-routing-signal has no published precedent, so this stays
deliberately conservative and, above all, **advisory**: the declared
win-stay/lose-shift policy (`agent_route.escalate`) picks the next round's
routing; nothing here auto-optimizes. A verdict block is a repo file in the
log.md block format plus one machine line:

    - [MAJOR] scripts/agent_loop.py:412 -> issue -> the concrete change -> @owner
    - [MINOR] docs/process-options.md:445 -> issue -> the concrete change
    VERDICT: CHANGES-REQUESTED findings=2

Scored components (mechanical, each in [0,1]):
  - **anchored-finding precision** — every finding's anchor (`file`, `file:line`,
    or `sym:mod.name`) must resolve in the repo; capped (a reviewer cannot farm
    score by anchoring at things that do not exist — CriticGPT's dominant failure
    is confident FALSE findings, so unresolved anchors cost precision).
  - **actionability rate** — the fraction of findings carrying a concrete change
    clause (issue -> change), the change-triggering usefulness measure.
  - **cross-reviewer corroboration** — when two reviewers overlap on an anchor it
    is a strong precision signal; a **cross-family** match (a different `Family`
    — who trained the model, NOT the route it was reached by; a legacy
    `Provider` label is the fallback) weighs above a same-family one (the
    popularity-trap correction: two samples of one model share blind spots).
  - **confirmed-finding rate** — a later commit touching +/- 10 lines of a
    finding's anchor is the canonical usefulness proof; scored only when that
    follow-up diff is supplied, else left out (never faked to 0-as-signal).

**Severity hygiene and the anti-gaming tripwires are GATES, never scores; length
never scores positively.** Tripwires (each a non-scored hard stop the escalation
policy reads): a declared `findings=N` that does not match the counted finding
lines (count gaming / cap pinning), near-duplicate review text between the two
reviewers (they were not independent), an implementer diff that touched a
review/policy path (editing the referee), and mass rejection of a prior round's
findings.

The **scoreboard** is one small decayed-tally text file
(`docs/reviews/scoreboard.txt`): per-provider decayed substance plus the round
history the escalation policy consumes. It is advisory state, never a source of
truth.

Contracts: IF-046, IF-047 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
"""

import argparse
import re
import sys
from pathlib import Path

# The finding line: "- [SEVERITY] <anchor> -> issue -> change [-> @owner]".
# Arrows may be "->" or the unicode arrow; we split on either.
FINDING_RE = re.compile(r"^\s*-\s*\[(?P<sev>[A-Za-z]+)\]\s*(?P<body>.+)$")
ARROW_RE = re.compile(r"\s*(?:->|→)\s*")
VERDICT_RE = re.compile(
    r"^\s*VERDICT:\s*(?P<verdict>APPROVE|CHANGES-REQUESTED)\s*(?:findings\s*=\s*(?P<n>\d+))?",
    re.I,
)
MODEL_RE = re.compile(r"^\s*Model:\s*(?P<model>.+?)\s*$", re.I)
# An anchor of the shape file:line or file:line:col, or a bare path, or sym:...
ANCHOR_RE = re.compile(r"^(?P<path>[\w./\-]+?)(?::(?P<line>\d+))?(?::\d+)?$")

# Scoreboard decay: recent rounds weigh more (substance' = substance*DECAY + new).
SCOREBOARD_DECAY = 0.7
# Corroboration: a cross-FAMILY overlap weighs above a same-family one — two
# samples of one model line share blind spots. The label the caller supplies is
# the model's `Family` (who trained it, never the route); a legacy `Provider`
# label is the fallback, so the weighting is unchanged on a legacy registry.
CROSS_FAMILY_WEIGHT = 1.0
SAME_FAMILY_WEIGHT = 0.5
# Two anchors "match" when they name the same path within this many lines.
ANCHOR_LINE_WINDOW = 10
# Near-duplicate tripwire: token-Jaccard at or above this = not independent.
NEAR_DUP_THRESHOLD = 0.8
# Paths an implementer diff must not touch (editing the referee). The two
# routing-referee scripts are listed twice: the `scripts/` prefix is the
# downstream scaffolded layout, and `project-trajectory/scripts/` is this
# meta-repo's own kit-script home — self-adoption needs both, since a prefix
# match on one never catches the other (WI-167).
REVIEW_POLICY_PATHS = (
    "docs/reviews/",
    # SN-028 folded the reviewer dial into docs/process.toml. BOTH stay listed:
    # the new home is where an implementer would now set `review_rounds = 0` in
    # the same diff as the work it would stop reviewing, and the legacy path
    # still exists in un-migrated repos. A tripwire that follows a dial to its
    # new home a release late is a tripwire that was blind for a release.
    "docs/process.toml",
    "docs/review-policy",
    # BOTH carriers: this is a pathspec allowlist matched against a diff,
    # and a repo that has not migrated stages the `.csv` name. A tripwire
    # that names one suffix is a tripwire the migration blinded.
    "docs/agents.toml",
    "docs/agents.csv",
    "docs/agents-enabled",
    "scripts/score_reviews.py",
    "scripts/agent_route.py",
    "project-trajectory/scripts/score_reviews.py",
    "project-trajectory/scripts/agent_route.py",
)


def _utf8_console():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


class Finding:
    __slots__ = ("severity", "anchor", "path", "line", "issue", "change", "raw")

    def __init__(self, severity, anchor, path, line, issue, change, raw):
        self.severity = severity
        self.anchor = anchor
        self.path = path
        self.line = line
        self.issue = issue
        self.change = change
        self.raw = raw


class Verdict:
    __slots__ = ("model", "verdict", "declared_n", "findings", "text")

    def __init__(self, model, verdict, declared_n, findings, text):
        self.model = model
        self.verdict = verdict
        self.declared_n = declared_n
        self.findings = findings
        self.text = text


def _parse_anchor(token):
    """(path, line|None) from a finding anchor token, or (None, None) when it is
    not path-shaped (a bare id, prose). A `sym:mod.name` anchor keeps its whole
    token as the path so precision resolves it against the module map."""
    token = token.strip().strip("`")
    if token.startswith("sym:"):
        return token, None
    m = ANCHOR_RE.match(token)
    if not m or "/" not in token and "." not in token:
        # Require a path-ish token (a separator or an extension dot) — a bare
        # word is prose, not an anchor.
        return None, None
    line = int(m.group("line")) if m.group("line") else None
    return m.group("path"), line


def parse_verdict(text, model=None):
    """Parse one verdict block into a Verdict. `model` overrides the Model: header
    (the coordinator knows which registry id it launched)."""
    findings = []
    verdict, declared_n = None, None
    hdr_model = None
    for ln in text.splitlines():
        mv = VERDICT_RE.match(ln)
        if mv:
            verdict = mv.group("verdict").upper()
            declared_n = int(mv.group("n")) if mv.group("n") is not None else None
            continue
        mm = MODEL_RE.match(ln)
        if mm and hdr_model is None:
            hdr_model = mm.group("model")
            continue
        mf = FINDING_RE.match(ln)
        if mf:
            parts = ARROW_RE.split(mf.group("body").strip())
            anchor_tok = parts[0].strip() if parts else ""
            path, line = _parse_anchor(anchor_tok)
            issue = parts[1].strip() if len(parts) > 1 else ""
            change = parts[2].strip() if len(parts) > 2 else ""
            findings.append(
                Finding(
                    severity=mf.group("sev").upper(),
                    anchor=anchor_tok,
                    path=path,
                    line=line,
                    issue=issue,
                    change=change,
                    raw=ln.strip(),
                )
            )
    return Verdict(
        model=model or hdr_model,
        verdict=verdict,
        declared_n=declared_n,
        findings=findings,
        text=text,
    )


def _anchor_resolves(finding, root, symbols=None):
    """True when a finding's anchor points at something real: a file that exists
    (and, with a line, one within the file), or a sym: reference present in the
    supplied symbol set. A finding with no path-shaped anchor does not count
    toward precision (neither credited nor penalised)."""
    if finding.path is None:
        return None  # not an anchor — excluded from the precision base
    if finding.path.startswith("sym:"):
        if symbols is None:
            return None  # no oracle -> excluded, never a false penalty
        return finding.path[len("sym:") :] in symbols
    p = Path(root) / finding.path
    if not p.is_file():
        return False
    if finding.line is not None:
        try:
            n = len(p.read_text(encoding="utf-8", errors="replace").splitlines())
        except OSError:
            return False
        return 1 <= finding.line <= n
    return True


def anchored_precision(verdict, root, symbols=None):
    """Fraction of ANCHORED findings whose anchor resolves, in [0,1]. No anchored
    finding -> 1.0 (nothing false to punish; corroboration/actionability carry
    the signal instead)."""
    checks = [_anchor_resolves(f, root, symbols) for f in verdict.findings]
    anchored = [c for c in checks if c is not None]
    if not anchored:
        return 1.0
    return sum(1 for c in anchored if c) / len(anchored)


def actionability(verdict):
    """Fraction of findings with a concrete change clause (issue -> change), the
    change-triggering usefulness measure. No findings -> 1.0 (an APPROVE with no
    findings is maximally actionable: nothing to do)."""
    if not verdict.findings:
        return 1.0
    return sum(1 for f in verdict.findings if f.change) / len(verdict.findings)


def corroboration(v_a, v_b, providers=None):
    """Cross-reviewer overlap in [0,1]: the fraction of reviewer A's anchored
    findings that reviewer B also raises (same path within ANCHOR_LINE_WINDOW
    lines), weighted UP when the two are a different FAMILY (cross-family). One
    reviewer -> 0.0 (no corroboration signal available). `providers` is the pair
    of Family labels (who trained each model — a router-fronted row shares its
    native sibling's Family, so it is NOT cross-family; a legacy Provider label
    is the fallback)."""
    if v_b is None:
        return 0.0
    a_anchored = [f for f in v_a.findings if f.path is not None]
    if not a_anchored:
        return 0.0
    b_anchored = [f for f in v_b.findings if f.path is not None]
    weight = SAME_FAMILY_WEIGHT
    if providers and providers[0] and providers[1] and providers[0] != providers[1]:
        weight = CROSS_FAMILY_WEIGHT
    matched = 0
    for fa in a_anchored:
        for fb in b_anchored:
            if fa.path == fb.path and (
                fa.line is None
                or fb.line is None
                or abs(fa.line - fb.line) <= ANCHOR_LINE_WINDOW
            ):
                matched += 1
                break
    return weight * matched / len(a_anchored)


def confirmed_rate(verdict, confirmed_lines):
    """Fraction of anchored findings a later commit confirmed (touched +/- 10
    lines of the anchor). `confirmed_lines` maps path -> set/iterable of touched
    line numbers. None -> unavailable (returns None, excluded from substance)."""
    if confirmed_lines is None:
        return None
    anchored = [f for f in verdict.findings if f.path is not None]
    if not anchored:
        return None
    hits = 0
    for f in anchored:
        touched = confirmed_lines.get(f.path)
        if not touched:
            continue
        if f.line is None:
            hits += 1
        elif any(abs(f.line - t) <= ANCHOR_LINE_WINDOW for t in touched):
            hits += 1
    return hits / len(anchored)


def substance(
    verdict, root, other=None, providers=None, symbols=None, confirmed_lines=None
):
    """The conservative composite in [0,1]: the mean of the AVAILABLE components
    (anchored precision, actionability, corroboration, and — when a follow-up
    diff is supplied — confirmed rate). Length is never a positive term."""
    comps = [
        anchored_precision(verdict, root, symbols),
        actionability(verdict),
        corroboration(verdict, other, providers),
    ]
    cr = confirmed_rate(verdict, confirmed_lines)
    if cr is not None:
        comps.append(cr)
    return sum(comps) / len(comps)


# --------------------------------------------------------------------------- #
# Tripwires — GATES, never scores. Each returns True when it FIRED.
# --------------------------------------------------------------------------- #
def tripwire_count_mismatch(verdict):
    """A declared findings=N that does not equal the counted finding lines —
    count gaming / cap pinning."""
    return verdict.declared_n is not None and verdict.declared_n != len(
        verdict.findings
    )


def _tokens(text):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def tripwire_near_duplicate(text_a, text_b):
    """Two reviewers' text is near-identical (token Jaccard >= threshold) — they
    were not independent draws."""
    ta, tb = _tokens(text_a), _tokens(text_b)
    if not ta or not tb:
        return False
    jaccard = len(ta & tb) / len(ta | tb)
    return jaccard >= NEAR_DUP_THRESHOLD


def tripwire_implementer_touched_review(changed_paths):
    """The implementer's diff touched a review/policy path (editing the referee)."""
    for p in changed_paths or ():
        norm = str(p).replace("\\", "/")
        if any(norm == rp or norm.startswith(rp) for rp in REVIEW_POLICY_PATHS):
            return True
    return False


def tripwire_mass_rejection(rejected, total, threshold=0.5):
    """A prior round's findings were mostly rejected/unaddressed (> threshold) —
    the implementer is dismissing review en masse."""
    if not total:
        return False
    return (rejected / total) > threshold


def fired_tripwires(verdicts, changed_paths=None, rejected=0, total_prior=0):
    """Every tripwire that fired over a round's verdict list, as a name list."""
    fired = []
    for v in verdicts:
        if tripwire_count_mismatch(v):
            fired.append("finding-count-mismatch")
            break
    if len(verdicts) >= 2 and tripwire_near_duplicate(
        verdicts[0].text, verdicts[1].text
    ):
        fired.append("near-duplicate-review")
    if tripwire_implementer_touched_review(changed_paths or ()):
        fired.append("implementer-touched-review-path")
    if tripwire_mass_rejection(rejected, total_prior):
        fired.append("mass-finding-rejection")
    return fired


def merge_verdict(verdicts):
    """Mechanical merge, no debate: CHANGES-REQUESTED if any reviewer requests
    changes, else APPROVE (independent parallel review beats a debate round at
    equal compute). Returns (verdict, contradiction) where contradiction = the
    reviewers disagreed."""
    seen = [v.verdict for v in verdicts if v.verdict]
    if not seen:
        return None, False
    merged = "CHANGES-REQUESTED" if "CHANGES-REQUESTED" in seen else "APPROVE"
    contradiction = "CHANGES-REQUESTED" in seen and "APPROVE" in seen
    return merged, contradiction


def latest_phase_verdicts(entries):
    """The deterministic latest-file-per-phase rule the integrator gate reads —
    extending merge_verdict's any-dissent-blocks discipline (LLR-140) from one
    parallel round to the reroll dimension. `entries` is [(phase, ordinal,
    verdict), ...] parsed from the verdict files at ONE reviewed head; the
    highest ordinal is a phase's LATEST word, so "latest" is well-defined even
    when a phase was re-run at the same commit. Returns ({phase: latest_verdict},
    {flipped phases}). Rules: a flipped phase is one whose latest APPROVE
    overwrites an earlier same-head CHANGES-REQUESTED — a reroll-until-green the
    gate must escalate rather than silently honor (repo-review 2026-07-21 L-28
    kin). The reverse (APPROVE then a later CHANGES-REQUESTED) is a plain latest
    dissent, not a flip — the last word still blocks. And the last word governs
    even when it is UNPARSEABLE: a higher-ordinal blank/mangled verdict file
    leaves the phase with NO latest verdict (omitted from the map) rather than
    falling back to an older parseable APPROVE — a mangled meant-to-dissent
    re-review must page, not silently clear (WI-260 review fix 2)."""
    by_phase = {}
    for phase, ordinal, verdict in entries:
        by_phase.setdefault(phase, []).append((ordinal, verdict))
    latest, flipped = {}, set()
    for phase, seq in by_phase.items():
        seq.sort()  # by ordinal ascending; the highest ordinal is the last word
        top = seq[-1][1]
        if not top:
            continue  # ambiguous last word -> no clear latest verdict for the phase
        latest[phase] = top
        earlier = [v for _o, v in seq[:-1]]
        if top == "APPROVE" and "CHANGES-REQUESTED" in earlier:
            flipped.add(phase)
    return latest, flipped


# --------------------------------------------------------------------------- #
# The scoreboard — one small decayed-tally text file.
# --------------------------------------------------------------------------- #
def read_scoreboard(path):
    """Parse the scoreboard: ({provider: (substance, rounds)}, [round dict, ...]).
    Absent -> ({}, [])."""
    path = Path(path)
    providers, rounds = {}, []
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return providers, rounds
    for ln in lines:
        ln = ln.strip()
        if not ln or ln.startswith("#"):
            continue
        parts = ln.split()
        if parts[0] == "provider" and len(parts) >= 2:
            kv = _kv(parts[2:])
            providers[parts[1]] = (
                _f(kv.get("substance", "0")),
                int(_f(kv.get("rounds", "0"))),
            )
        elif parts[0] == "round":
            kv = _kv(parts[1:])
            rounds.append(
                {
                    "verdict": kv.get("verdict", ""),
                    "tier": kv.get("tier", ""),
                    "margin": _f(kv.get("margin", "0")),
                    "primary": kv.get("primary", "") or None,
                    "tripwire": kv.get("tripwire", "0") not in ("0", ""),
                    "contradiction": kv.get("contradiction", "0") not in ("0", ""),
                }
            )
    return providers, rounds


def _kv(tokens):
    out = {}
    for t in tokens:
        if "=" in t:
            k, _, v = t.partition("=")
            out[k] = v
    return out


def _f(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return 0.0


def write_scoreboard(path, providers, rounds):
    """Write the scoreboard deterministically (LF, providers sorted)."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    out = [
        "# agent-review scoreboard (advisory; the declared win-stay/lose-shift",
        "# policy picks the next routing - nothing here auto-optimizes). Written",
        "# by score_reviews.py. Per-provider decayed substance + the round history",
        "# the escalation policy (agent_route.escalate) reads.",
    ]
    for prov in sorted(providers):
        sub, rnds = providers[prov]
        out.append("provider {} substance={:.4f} rounds={}".format(prov, sub, rnds))
    for i, r in enumerate(rounds, 1):
        out.append(
            "round {} verdict={} tier={} margin={:g} primary={} tripwire={} contradiction={}".format(
                i,
                r.get("verdict", ""),
                r.get("tier", ""),
                r.get("margin", 0),
                r.get("primary", "") or "",
                1 if r.get("tripwire") else 0,
                1 if r.get("contradiction") else 0,
            )
        )
    with open(str(path), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(out) + "\n")


def record_round(path, round_info, provider_substance):
    """Append a round to the scoreboard and decay the provider tallies.
    `provider_substance` maps provider -> this round's substance for that
    provider (usually one or two entries)."""
    providers, rounds = read_scoreboard(path)
    for prov, sub in provider_substance.items():
        old_sub, old_rounds = providers.get(prov, (0.0, 0))
        providers[prov] = (old_sub * SCOREBOARD_DECAY + sub, old_rounds + 1)
    rounds.append(round_info)
    write_scoreboard(path, providers, rounds)
    return providers, rounds


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description="Score one or two review verdict files and (optionally) "
        "record the round on the advisory scoreboard.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument(
        "--verdict", action="append", default=[], help="a verdict file (repeat for two)"
    )
    ap.add_argument("--root", default=".", help="repo root for anchor resolution")
    ap.add_argument(
        "--family",
        action="append",
        default=[],
        help="the Family (who trained the model — the corroboration key) per "
        "--verdict; preferred over --provider",
    )
    ap.add_argument(
        "--provider",
        action="append",
        default=[],
        help="legacy alias for --family (the corroboration key falls back to it)",
    )
    ap.add_argument("--tier", default="", help="the implementer tier this round ran at")
    ap.add_argument(
        "--scoreboard", default="docs/reviews/scoreboard.txt", help="scoreboard file"
    )
    ap.add_argument(
        "--record", action="store_true", help="record the round on the scoreboard"
    )
    args = ap.parse_args(argv)

    if not args.verdict:
        ap.error("at least one --verdict is required")
    # The corroboration key is Family; --provider is the legacy fallback.
    labels = args.family or args.provider
    verdicts = []
    for i, vp in enumerate(args.verdict):
        try:
            text = Path(vp).read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            print("score_reviews: cannot read {}: {}".format(vp, exc), file=sys.stderr)
            return 2
        fam = labels[i] if i < len(labels) else None
        verdicts.append(parse_verdict(text, model=fam))

    # Pad to the verdict count: two --verdict with one --family used to
    # IndexError on providers[1 - i] (repo-review 2026-07-21 L-27).
    providers = (list(labels) + [None] * len(verdicts))[: max(len(verdicts), 2)]
    subs = {}
    for i, v in enumerate(verdicts):
        peer = verdicts[1 - i] if len(verdicts) > 1 else None
        s = substance(
            v,
            args.root,
            other=peer,
            providers=(providers[i], providers[1 - i]) if len(verdicts) > 1 else None,
        )
        fam = labels[i] if i < len(labels) else "?{}".format(i)
        subs[fam] = s
        print(
            "verdict[{}] {} substance={:.3f} findings={} (precision={:.2f} action={:.2f})".format(
                i,
                v.verdict,
                s,
                len(v.findings),
                anchored_precision(v, args.root),
                actionability(v),
            )
        )
    merged, contradiction = merge_verdict(verdicts)
    fired = fired_tripwires(verdicts)
    print(
        "merged={} contradiction={} tripwires={}".format(
            merged, contradiction, fired or "none"
        )
    )

    if args.record:
        # Unlabeled verdicts tally under synthetic "?N" keys; recording those
        # pollutes the durable scoreboard with placeholder families (L-27).
        subs = {k: v for k, v in subs.items() if not str(k).startswith("?")}
        margin = 0.0
        primary = None
        if len(subs) == 2:
            (p1, s1), (p2, s2) = list(subs.items())
            margin = abs(s1 - s2)
            primary = p1 if s1 >= s2 else p2
        record_round(
            args.scoreboard,
            {
                "verdict": merged or "",
                "tier": args.tier,
                "margin": margin,
                "primary": primary,
                "tripwire": bool(fired),
                "contradiction": contradiction,
            },
            subs,
        )
        print("recorded round on {}".format(args.scoreboard))
    return 1 if fired else 0


if __name__ == "__main__":
    sys.exit(main())
