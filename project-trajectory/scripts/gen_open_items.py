#!/usr/bin/env python3
"""The owner decision surface, generated (WI-322, OI-10 ruled option (b)).

Replaces the hand-maintained `docs/open-items.md`. Two inputs, one output:

  docs/requirements/open-items.csv   pending decision briefs, one row per OI
  the spine registries + git         rows owing a ratification or a re-attest
  -> docs/open-items.html            the ONLY surface a human reads

Why HTML and not markdown: the depth an owner needs to rule a re-attest is a
WORD-LEVEL DIFF — of a 1,500-character cell, which forty words moved — and
markdown cannot mark that. The first sitting under the `Modified` regime read a
POINTER ("run `trace.py --ratify modified`") and could not act from it, which is
what this replaces. The CSV is a machine source: it is read raw about as often
as `work-items.csv` is, i.e. never.

WHAT IT RENDERS, in the order an owner needs it:

  1. PENDING DECISIONS — one card per `Status=pending` row of the registry:
     the one-line, what is being decided, blast radius, options, recommendation,
     and the WI rows that carry the work.
  2. RATIFICATION & RE-ATTESTATION — every SR whose `Status` is `Draft` (owes a
     first ratification) or `Modified` (owes a re-attest), with its whole chain:
     per-cell before/after, unchanged runs collapsible, additions and deletions
     marked, and THE BASELINE REVISION PRINTED ON EVERY SECTION. An empty
     section reads as *check the baseline*, never as *nothing changed* — the
     failure mode that shipped a brief missing two of six rows (log 2026-07-26).
  3. PENDING OWNER ACTIONS — the pointer projection `gen_trajectory` already
     derives (blocked rows, the spine pointers, the NEEDS-HUMAN ask) plus its
     machine-local advisory, reused verbatim rather than recomputed.

ANTI-DUPLICATION, deliberately: the git archaeology and the cell comparison live
in `trace.reattest_model`, and the pending projection lives in
`gen_trajectory.pending_block`. This module imports both and RENDERS. It owns no
second opinion about what is pending or what changed — if this view and the
`--ratify` brief ever disagree, the brief is authoritative and this is the bug.

Freshness: `--check` byte-compares the regenerated view against the file, with
the machine-local advisory region MASKED — those `refs/llm/*` facts do not
transport with clone/push, so gating on them would red a second clone (the
M-10/WI-266 rule the markdown block already followed).

Stdlib only, cross-platform, deterministic (sorted inputs, no clocks) so the
gated compare is byte-stable.

Contracts: IF-073, IF-074 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import difflib
import html
import io
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import gen_trajectory as gt  # noqa: E402  (path set above)
import trace as tr  # noqa: E402

OPEN_ITEMS_CSV = "docs/requirements/open-items.csv"
OUT_REL = "docs/open-items.html"

# The advisory region is regenerated per machine and excluded from --check, the
# same split (and the same reason) as the markdown block's PENDING_LOCAL_LABEL.
LOCAL_BEGIN = "<!-- BEGIN MACHINE-LOCAL -->"
LOCAL_END = "<!-- END MACHINE-LOCAL -->"
# The view RECORDS the baseline it was rendered against, so `--check` re-renders
# with the same one instead of silently comparing against a different history.
# Without this, `--since` would be a write-only flag whose output the freshness
# gate could never reproduce — a generated file nobody could keep green.
BASELINE_MARK = "<!-- attestation-baseline: {} -->"
BASELINE_RE = re.compile(r"<!-- attestation-baseline: ([^\s>]*) -->")

# Mirrors the dashboard's theme tokens so the two owner surfaces read as one
# system. NOT imported: they live inside gen_trajectory's HTML_TEMPLATE string,
# and extracting them would edit that module — which re-reds `perceptual-stale`
# and costs a critique dispatch for a refactor. Kept honest by
# test_open_items_theme_tokens_match_the_dashboard, the WI-291 drift-guard
# pattern (a guard, not an extraction) rather than a shared-module dedup the
# F5 ruling already rejected.
THEME = {
    "light": {
        "--bg": "#f8fafc",
        "--surface": "#ffffff",
        "--border": "#e2e8f0",
        "--text": "#0f172a",
        "--muted": "#64748b",
        "--accent": "#4f46e5",
    },
    "dark": {
        "--bg": "#0b1120",
        "--surface": "#0f172a",
        "--border": "#1e293b",
        "--text": "#e2e8f0",
        "--muted": "#94a3b8",
        "--accent": "#818cf8",
    },
}

CSS = """
:root{
  --bg:#f8fafc; --surface:#ffffff; --border:#e2e8f0; --text:#0f172a;
  --muted:#64748b; --accent:#4f46e5; --pending:#b45309;
  --ins-ink:#065f46; --ins-bg:rgba(4,120,87,.13); --ins-rule:#047857;
  --del-ink:#9f1239; --del-bg:rgba(190,18,60,.11); --del-rule:#be123c;
  --tiny:.75rem; --xsmall:.8rem; --small:.85rem; --body:.94rem;
  --lead:1.05rem; --display:1.3rem; --hero:1.7rem;
  --r-ctl:6px; --r-card:12px; --r-pill:999px;
  --mono:ui-monospace,"Cascadia Code","Segoe UI Mono",Consolas,monospace;
  color-scheme: light dark;
}
@media (prefers-color-scheme:dark){
  :root{
    --bg:#0b1120; --surface:#0f172a; --border:#1e293b; --text:#e2e8f0;
    --muted:#94a3b8; --accent:#818cf8; --pending:#fbbf24;
    --ins-ink:#6ee7b7; --ins-bg:rgba(16,185,129,.16); --ins-rule:#34d399;
    --del-ink:#fda4af; --del-bg:rgba(244,63,94,.15); --del-rule:#fb7185;
  }
}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--text);
  font:var(--body)/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",system-ui,sans-serif;}
.wrap{max-width:60rem;margin-inline:auto;padding:2rem 1.25rem 4rem;
  display:flex;flex-direction:column;gap:2rem;}
h1{font-size:var(--hero);margin:0 0 .35rem;letter-spacing:-.02em;}
h2{font-size:var(--display);margin:0;letter-spacing:-.01em;}
.sub{color:var(--muted);font-size:var(--small);margin:0;}
.eyebrow{font-size:var(--tiny);text-transform:uppercase;letter-spacing:.1em;
  color:var(--muted);font-weight:600;margin:0 0 .6rem;}
section.band{display:flex;flex-direction:column;gap:1rem;}
.card{background:var(--surface);border:1px solid var(--border);
  border-radius:var(--r-card);padding:1.2rem 1.35rem;
  display:flex;flex-direction:column;gap:.75rem;scroll-margin-top:1rem;}
.card h3{margin:0;font-size:var(--lead);display:flex;gap:.6rem;
  align-items:baseline;flex-wrap:wrap;}
.card h3 .rid{font-family:var(--mono);color:var(--accent);}
.field{display:flex;flex-direction:column;gap:.2rem;}
.field .k{font-size:var(--tiny);text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted);font-weight:600;}
.field .v{font-size:var(--small);}
.pill{font-size:var(--tiny);border-radius:var(--r-pill);padding:.1rem .55rem;
  border:1px solid var(--border);color:var(--muted);white-space:nowrap;
  font-variant-numeric:tabular-nums;}
.pill.ratify{border-color:var(--pending);color:var(--pending);}
.baseline{font-size:var(--xsmall);color:var(--muted);font-family:var(--mono);}
.empty{font-size:var(--small);border-left:3px solid var(--pending);
  padding-left:.75rem;}
.row{border-top:1px solid var(--border);padding-top:.8rem;
  display:flex;flex-direction:column;gap:.45rem;}
.row-head{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;}
.row-head .rid{font-family:var(--mono);font-size:var(--xsmall);font-weight:700;}
.cellname{font-family:var(--mono);font-size:var(--xsmall);font-weight:700;
  color:var(--muted);}
.diff{font-size:var(--small);line-height:1.7;overflow-wrap:anywhere;}
.diff ins{background:var(--ins-bg);color:var(--ins-ink);text-decoration:none;
  box-shadow:inset 0 -2px 0 var(--ins-rule);border-radius:2px;padding:0 .05em;}
.diff del{background:var(--del-bg);color:var(--del-ink);
  text-decoration:line-through;border-radius:2px;padding:0 .05em;}
ul.pointers{margin:0;padding-left:1.1rem;font-size:var(--small);}
ul.pointers li{margin:.3rem 0;}
code{font-family:var(--mono);font-size:.92em;}
.toolbar{display:flex;gap:.75rem;align-items:center;flex-wrap:wrap;
  font-size:var(--small);}
.toolbar label{display:flex;gap:.45rem;align-items:center;cursor:pointer;
  border:1px solid var(--border);background:var(--surface);
  border-radius:var(--r-ctl);padding:.35rem .7rem;}
.toolbar label:focus-within{outline:2px solid var(--accent);outline-offset:2px;}
footer{color:var(--muted);font-size:var(--tiny);
  border-top:1px solid var(--border);padding-top:1rem;}
a{color:var(--accent);}
:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}
@media (max-width:34rem){.wrap{padding:1.25rem .9rem 3rem;}}
"""

JS = """
(function(){
  var box=document.getElementById('focus');
  if(!box) return;
  var LIMIT=170,HEAD=55,TAIL=55;
  var spans=[].slice.call(document.querySelectorAll('.diff .eq'));
  spans.forEach(function(s){s.setAttribute('data-full',s.textContent);});
  function apply(){
    spans.forEach(function(s){
      var full=s.getAttribute('data-full');
      s.textContent=(box.checked&&full.length>LIMIT)
        ? full.slice(0,HEAD)+' [\\u2026] '+full.slice(-TAIL) : full;
    });
  }
  box.addEventListener('change',apply);
  apply();
})();
"""


def _utf8_console():
    """Emit UTF-8 whatever the OS console codepage is: this module prints em
    dashes and arrows in its own messages, and a legacy Windows cp1252 console
    would raise UnicodeEncodeError (or hand a caller undecodable bytes) on a
    plain `print`. Same guard the sibling kit scripts carry."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def esc(text):
    return html.escape(text or "", quote=True)


def load_open_items(root):
    """Rows of the open-items registry, `-000` example rows dropped (the
    copy-ready placeholder convention every other registry uses). Missing file
    -> [] : a repo that carries no decisions yet still renders a view."""
    path = Path(root) / OPEN_ITEMS_CSV
    if not path.is_file():
        return []
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return [
            r
            for r in csv.DictReader(fh)
            if (r.get("OI-ID") or "").startswith("OI-")
            and not r["OI-ID"].endswith("-000")
        ]


def _tokens(text):
    return re.findall(r"\s+|[^\s]+", text or "")


def word_diff(before, after):
    """A unified word-level diff as HTML: unchanged runs wrapped `.eq` (so the
    view can collapse them), removals in `<del>`, additions in `<ins>`.

    One flow rather than two columns, because these cells are PROSE: the eye
    follows the sentence and the change sits inside it, where a side-by-side of
    two 1,500-character paragraphs is two walls instead of one."""
    a, b = _tokens(before), _tokens(after)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        None, a, b, autojunk=False
    ).get_opcodes():
        if tag == "equal":
            out.append('<span class="eq">{}</span>'.format(esc("".join(a[i1:i2]))))
            continue
        gone, came = "".join(a[i1:i2]), "".join(b[j1:j2])
        if gone.strip():
            out.append("<del>{}</del>".format(esc(gone)))
        if came.strip():
            out.append("<ins>{}</ins>".format(esc(came)))
    return "".join(out)


def changed_percent(before, after):
    """How much of the cell moved, counting WORDS — whitespace runs are dropped
    first. Including them dilutes the figure toward nothing (four words replaced
    by four different words reads as 57% when the spaces are counted as
    unchanged), and the label the reader sees says "of the words"."""
    a = [t for t in _tokens(before) if t.strip()]
    b = [t for t in _tokens(after) if t.strip()]
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    same = sum(n for _, _, n in sm.get_matching_blocks())
    return round((1 - same / max(len(b), 1)) * 100)


def md_inline(text):
    """The few markdown inline forms the reused pointer lines actually use —
    `code`, **bold**, and [text](target). Deliberately not a markdown parser:
    the input is one generator's own output, not arbitrary prose, and a real
    parser here would be a dependency the kit's install-nothing rule forbids."""
    out = esc(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', out)
    return out


def _brief_cards(items):
    cards = []
    for row in items:
        if (row.get("Status") or "").strip().lower() != "pending":
            continue
        fields = []
        for key, label in (
            ("OneLine", "One line"),
            ("Decision", "What is being decided"),
            ("BlastRadius", "Blast radius"),
            ("Options", "Options"),
            ("Recommendation", "Recommendation"),
            ("WI-Refs", "Work items"),
        ):
            val = (row.get(key) or "").strip()
            if val:
                fields.append(
                    '<div class="field"><span class="k">{}</span>'
                    '<span class="v">{}</span></div>'.format(esc(label), md_inline(val))
                )
        cards.append(
            '<article class="card" id="{i}"><h3><span class="rid">{i}</span>'
            "<span>{t}</span></h3>{f}</article>".format(
                i=esc(row["OI-ID"]),
                t=esc((row.get("Title") or "").strip()),
                f="".join(fields),
            )
        )
    if not cards:
        return '<p class="empty">No pending decision — the owner queue is empty.</p>'
    return "".join(cards)


def _attestation_cards(model):
    """One card per SR owing a ratification or re-attest, its chain beneath."""
    if not model:
        return (
            '<p class="empty">No <code>Draft</code> or <code>Modified</code> spine '
            "row — nothing owes a ratification or a re-attest.</p>"
        )
    cards = []
    for entry in model:
        ratify = entry["kind"] == "ratify"
        head = (
            '<h3><span class="rid">{i}</span><span>{t}</span>'
            '<span class="pill{cls}">{label}</span></h3>'.format(
                i=esc(entry["id"]),
                t=esc(entry["title"] or "(untitled)"),
                cls=" ratify" if ratify else "",
                label="ratification owed" if ratify else "re-attest owed",
            )
        )
        if entry["baseline"]:
            base = '<p class="baseline">baseline {b}{d} — {why}</p>'.format(
                b=esc(entry["baseline"][:9]),
                d=" ({})".format(esc(entry["baseline_date"]))
                if entry["baseline_date"]
                else "",
                why="from --since"
                if entry["from_since"]
                else "newest revision where {} read Verified".format(esc(entry["id"])),
            )
        else:
            base = '<p class="baseline">no baseline — {}</p>'.format(
                esc(entry["no_baseline_reason"])
            )
        body = []
        for row in entry["rows"]:
            state = row["state"]
            tag = {
                "changed": "changed",
                "added": "ADDED since baseline",
                "removed": "REMOVED since baseline",
                "current": "current content",
            }[state]
            inner = []
            if state == "changed":
                for name, before, after in row["cells"]:
                    inner.append(
                        '<div class="cellname">{n} <span class="pill">{p}% of the '
                        'words changed</span></div><div class="diff">{d}</div>'.format(
                            n=esc(name),
                            p=changed_percent(before, after),
                            d=word_diff(before, after),
                        )
                    )
            else:
                for key, val in (row["full"] or {}).items():
                    if (val or "").strip():
                        inner.append(
                            '<div class="cellname">{k}</div>'
                            '<div class="diff">{v}</div>'.format(
                                k=esc(key), v=esc(val.strip())
                            )
                        )
            body.append(
                '<div class="row"><div class="row-head">'
                '<span class="rid">{k} {i}</span>'
                '<span class="pill">{s}</span></div>{b}</div>'.format(
                    k=esc(row["kind"]), i=esc(row["id"]), s=esc(tag), b="".join(inner)
                )
            )
        if not entry["rows"]:
            # Never a confident blank: an empty section under an auto-derived
            # baseline usually means the amendment PREDATES it (a pre-regime
            # streak), which is a baseline problem, not a no-change finding.
            body.append(
                '<p class="empty">No cell differs from this baseline beyond the '
                "Status flip. That is a signal to <strong>check the baseline</strong>, "
                "not a row that is free to bless — an amendment that landed while the "
                "row still read <code>Verified</code> sits BEFORE an auto-derived "
                "baseline. Re-run with <code>--since &lt;rev&gt;</code>.</p>"
            )
        cards.append(
            '<article class="card" id="{i}">{h}{b}{rows}</article>'.format(
                i=esc(entry["id"] + "-attest"), h=head, b=base, rows="".join(body)
            )
        )
    return "".join(cards)


def _pointer_list(markdown_items):
    lines = [
        ln.strip()[2:].strip()
        for ln in markdown_items.splitlines()
        if ln.strip().startswith("- ")
    ]
    if not lines:
        body = [ln.strip() for ln in markdown_items.splitlines() if ln.strip()]
        return '<p class="sub">{}</p>'.format(
            md_inline(" ".join(body).strip("_")) if body else "None."
        )
    return '<ul class="pointers">{}</ul>'.format(
        "".join("<li>{}</li>".format(md_inline(ln)) for ln in lines)
    )


def render(root, since=None):
    """The whole page. Deterministic: every input is sorted upstream.

    `since` overrides the git-derived attestation baseline for the whole view —
    needed for a PRE-REGIME streak, where the amendment landed while the row
    still read `Verified` so the auto-baseline sits AFTER it and the section
    renders empty. The chosen baseline is stamped into the output so `--check`
    reproduces it."""
    root = Path(root)
    reg = tr.load_registries(root / "docs")
    model = tr.reattest_model(
        root, reg.srs, reg.llrs, reg.tcs, since=since, statuses=("modified", "draft")
    )
    items = load_open_items(root)
    pure, local = pending_regions(root)
    counts = {
        "pending": sum(
            1 for r in items if (r.get("Status") or "").strip().lower() == "pending"
        ),
        "attest": len(model),
        "rows": sum(len(e["rows"]) for e in model),
    }
    return (
        "<!doctype html>\n"
        "{basemark}\n"
        '<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Open items — owner decision surface</title>\n"
        "<style>{css}</style></head><body>\n"
        '<div class="wrap">\n'
        "<header>\n"
        '<p class="eyebrow">generated — do not hand-edit · '
        "<code>python project-trajectory/scripts/gen_open_items.py</code></p>\n"
        "<h1>Open items — owner decision surface</h1>\n"
        '<p class="sub">{pending} pending decision(s) · {attest} spine row(s) owing a '
        "ratification or re-attest, across {rows} chain row change(s). Briefs are rows "
        "in <code>docs/requirements/open-items.csv</code>; the attestation depth is "
        "computed by <code>trace.reattest_model</code>, the same code behind "
        "<code>trace.py --ratify</code>. If the two ever disagree, the brief is "
        "authoritative and this view is the bug.</p>\n"
        "</header>\n"
        '<section class="band"><p class="eyebrow">1 · Pending decisions</p>{briefs}</section>\n'
        '<div class="toolbar"><label><input type="checkbox" id="focus" checked> '
        "Collapse unchanged text</label></div>\n"
        '<section class="band"><p class="eyebrow">2 · Ratification &amp; '
        "re-attestation</p>{attestations}</section>\n"
        '<section class="band"><p class="eyebrow">3 · Pending owner actions '
        "(derived)</p>{pointers}</section>\n"
        "{lb}\n"
        '<section class="band"><p class="eyebrow">Machine-local advisory</p>'
        '<p class="sub">Re-derived from this machine\'s <code>refs/llm/*</code>; these '
        "do not transport with clone or push, so this region is excluded from the "
        "freshness compare and may read empty in another clone.</p>{local}</section>\n"
        "{le}\n"
        "<footer>Source: <code>docs/requirements/open-items.csv</code> + the spine "
        "registries. Rule a decision by appending to <code>docs/log.md</code>'s "
        "Decisions log and setting the row's <code>Status</code>; bless an amendment "
        "by moving the spine row's <code>Status</code> "
        "<code>Modified</code>→<code>Verified</code> (or →<code>Planned</code> when "
        "the evidence no longer verifies it). The gate re-derives on its own.</footer>\n"
        "</div>\n<script>{js}</script>\n</body></html>\n"
    ).format(
        css=CSS,
        js=JS,
        basemark=BASELINE_MARK.format(since or ""),
        briefs=_brief_cards(items),
        attestations=_attestation_cards(model),
        pointers=_pointer_list(pure),
        local=_pointer_list(local),
        lb=LOCAL_BEGIN,
        le=LOCAL_END,
        **counts,
    )


def pending_regions(root):
    """`(pure, machine_local)` markdown item text, reused from gen_trajectory's
    pending projection rather than recomputed — one home for "what is pending"."""
    block = gt.pending_block(root)
    label = gt.PENDING_LOCAL_LABEL
    if label in block:
        pure, local = block.split(label, 1)
    else:  # pragma: no cover - the label is emitted unconditionally today
        pure, local = block, ""
    return pure, local


def mask_local(text):
    """`text` with the machine-local region blanked, for the freshness compare."""
    start = text.find(LOCAL_BEGIN)
    end = text.find(LOCAL_END)
    if start == -1 or end == -1 or end < start:
        return text
    return text[: start + len(LOCAL_BEGIN)] + text[end:]


def main(argv=None):
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--out", default=None, help="output path (default {})".format(OUT_REL)
    )
    ap.add_argument(
        "--since",
        default=None,
        help="attestation baseline revision for the whole view — use for a "
        "PRE-REGIME streak, where an amendment landed while the row still read "
        "Verified so the auto-derived baseline sits after it and the section "
        "renders empty. Stamped into the output so --check reproduces it.",
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="exit 1 when the file is stale, writing nothing (the freshness gate; "
        "the machine-local region is masked before comparing)",
    )
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    out = Path(args.out) if args.out else root / OUT_REL
    # Vacuous for a repo that carries neither the registry nor the view: the
    # surface is opt-in, exactly like the markdown block it replaces, so a
    # non-adopter (and a fresh scaffold before its first decision) pays nothing.
    if not (root / OPEN_ITEMS_CSV).is_file() and not out.is_file():
        print(
            "gen_open_items: no {} and no {} — nothing to render (vacuous).".format(
                OPEN_ITEMS_CSV, OUT_REL
            )
        )
        return 0
    if args.check:
        if not out.is_file():
            print(
                "gen_open_items: {} missing — run "
                "`python scripts/gen_open_items.py`".format(OUT_REL)
            )
            return 1
        current = out.read_text(encoding="utf-8")
        # Re-render against the baseline the FILE declares (not this run's flag),
        # so the gate compares like with like on every machine and in CI.
        stamped = BASELINE_RE.search(current)
        since = (stamped.group(1) if stamped else "") or None
        fresh = render(root, since=since)
        if mask_local(current) != mask_local(fresh):
            print(
                "gen_open_items: {} STALE — run "
                "`python scripts/gen_open_items.py`".format(OUT_REL)
            )
            return 1
        print("gen_open_items: open-items view up to date.")
        return 0
    fresh = render(root, since=args.since)
    if out.is_file() and out.read_text(encoding="utf-8") == fresh:
        print("gen_open_items: already up to date -> {}".format(out))
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(fresh, encoding="utf-8")
    print("gen_open_items: wrote {}".format(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
