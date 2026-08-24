#!/usr/bin/env python3
"""The owner decision surface, generated (WI-322, OI-10 ruled option (b)).

Replaces the hand-maintained `docs/open-items.md`. Two inputs, one output:

  docs/requirements/open-items.toml   pending decision briefs, one row per OI
  the spine registries + git         rows owing an approval or a re-attest
  -> docs/open-items.html            the ONLY surface a human reads

Why HTML and not markdown: the depth an owner needs to rule a re-attest is a
WORD-LEVEL DIFF — of a 1,500-character cell, which forty words moved — and
markdown cannot mark that. The first sitting under the retired `Modified` regime
read a POINTER ("run `trace.py --approve modified`") and could not act from it,
which is what this replaces. The CSV is a machine source: it is read raw about as often
as `work-items.csv` is, i.e. never.

WHAT IT RENDERS, in the order an owner needs it:

  1. PENDING DECISIONS — one card per `Status=pending` row of the registry:
     the one-line, what is being decided, blast radius, options, recommendation,
     and the WI rows that carry the work.
  2. APPROVAL & RE-ATTESTATION — every SR whose `Status` is `Drafted` (owes a
     first approval) or whose chain has DRIFTED from the approved snapshot
     (owes a re-attest — D-9 step 7 retired the `Modified` marker and left the
     comparison as the whole detector), with its whole chain:
     per-cell before/after, unchanged runs collapsible, additions and deletions
     marked, and THE BASELINE REVISION PRINTED ON EVERY SECTION. An empty
     section reads as *check the baseline*, never as *nothing changed* — the
     failure mode that shipped a brief missing two of six rows (log 2026-07-26).
     Clearing the toolbar box also reveals THE REST OF EACH ROW — the cells the
     diff had no reason to show, plus the SR's own text where the amendment sits
     entirely in a child. A diff says what moved; an attestation asks whether the
     evidence still verifies what the row now SAYS, and the second question needs
     the cells the first one omits (owner, 2026-07-27).
  3. PENDING OWNER ACTIONS — the pointer projection `pending.py` already
     derives (blocked rows, the spine pointers, the tracked pause), reused
     verbatim rather than recomputed.

ANTI-DUPLICATION, deliberately: the git archaeology and the cell comparison live
in `trace.reattest_model`, and the pending projection lives in
`pending.pending_block`. This module imports both and RENDERS. It owns no
second opinion about what is pending or what changed — if this view and the
`--approve` brief ever disagree, the brief is authoritative and this is the bug.

Freshness: `--check` byte-compares the regenerated view against the file — a
pure function of the committed tree since the dispatcher-era machine-local
advisory region retired (concurrency-restructure Phase 5), so it holds in any
clone.

Stdlib only, cross-platform, deterministic (sorted inputs, no clocks) so the
gated compare is byte-stable.

Contracts: IF-073, IF-074, IF-075, IF-118, IF-126 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.toml).
IF-126 is the READ-ONLY consumption of the `last_approved` baseline whose
provider row is IF-123: this is a generator, so it reads what was blessed and
never refreshes it.
"""

import argparse
import difflib
import html
import re
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pending  # noqa: E402  (path set above)
import spine_carrier  # noqa: E402
import baseline_snapshot  # noqa: E402
import trace as tr  # noqa: E402

# The registry names its DESTINATION carrier; `spine_carrier.resolve` finds
# whichever of the two is live, so a repo that has not run `migrate_carrier`
# keeps rendering from its CSV (repo-lock §8.1).
OPEN_ITEMS_REL = "docs/requirements/open-items.toml"
OUT_REL = "docs/open-items.html"

# (The `<!-- attestation-baseline: <rev> -->` stamp retired at D-9 step 4 with
# `--since`. The view used to RECORD the git revision it was rendered against so
# `--check` could reproduce that render; the baseline is now a directory of
# files, identical on every machine and in CI, so there is nothing to stamp and
# nothing a later run could accidentally re-derive differently.)

# The theme tokens the two owner surfaces must agree on. This is a NAME list,
# not a value mirror: 122-REVIEW-A refuted the value-mirror version — nine of the
# twelve emitted tokens were rewritten (dark `--text:#444444`) and the guard
# stayed green, because the mirror was a test-only dict nothing rendered from.
# The values now live in ONE place, the emitted CSS below, and the drift guard
# parses them out of it (`theme_tokens`) so it cannot pass while the page ships
# something else. Still a guard rather than an extraction: importing the
# dashboard's tokens would edit gen_trajectory and re-red `perceptual-stale`
# for a refactor (the WI-291 precedent, and the F5 ruling against _kitcommon).
THEME_TOKENS = ("--bg", "--surface", "--border", "--text", "--muted", "--accent")

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
.anchor{display:flex;flex-direction:column;gap:.6rem;}
.field .v{font-size:var(--small);}
.field .v p{margin:0 0 .5rem;}
.field .v p:last-child{margin-bottom:0;}
.field .v h4{margin:.7rem 0 .35rem;font-size:var(--small);
  text-transform:uppercase;letter-spacing:.06em;color:var(--muted);}
.field .v h4:first-child{margin-top:0;}
.field .v ul{margin:0 0 .5rem;padding-left:1.15rem;}
.field .v ul:last-child{margin-bottom:0;}
.field .v li{margin:0 0 .3rem;}
.pill{font-size:var(--tiny);border-radius:var(--r-pill);padding:.1rem .55rem;
  border:1px solid var(--border);color:var(--muted);white-space:nowrap;
  font-variant-numeric:tabular-nums;}
.pill.approve{border-color:var(--pending);color:var(--pending);}
.baseline{font-size:var(--xsmall);color:var(--muted);font-family:var(--mono);}
.empty{font-size:var(--small);border-left:3px solid var(--pending);
  padding-left:.75rem;}
.row{border-top:1px solid var(--border);padding-top:.8rem;
  display:flex;flex-direction:column;gap:.45rem;}
.row-head{display:flex;gap:.6rem;align-items:center;flex-wrap:wrap;}
.row-head .rid{font-family:var(--mono);font-size:var(--xsmall);font-weight:700;}
.cellname{font-family:var(--mono);font-size:var(--xsmall);font-weight:700;
  color:var(--muted);}
/* The §A5.1 group label above a run of cells (D-9 step 4) — approved cells owe
   an attestation, traced ones route to adjudication. Set apart from .cellname
   by weight and a rule rather than by colour alone, so the grouping survives a
   monochrome print and a low-contrast display. */
.cellgroup{font-size:var(--xsmall);font-weight:600;letter-spacing:.04em;
  text-transform:uppercase;color:var(--muted);border-top:1px solid var(--border);
  padding-top:.5rem;margin-top:.35rem;}
.diff{font-size:var(--small);line-height:1.7;overflow-wrap:anywhere;}
.diff ins{background:var(--ins-bg);color:var(--ins-ink);text-decoration:none;
  box-shadow:inset 0 -2px 0 var(--ins-rule);border-radius:2px;padding:0 .05em;}
.diff del{background:var(--del-bg);color:var(--del-ink);
  text-decoration:line-through;border-radius:2px;padding:0 .05em;}
/* The row's remaining cells. Hidden while the toolbar box is CHECKED (the
   focus default), shown when it is cleared — one control, two collapses: the
   long unchanged runs INSIDE a diff, and the fields that never changed at all.
   A reader blessing a rewritten `Rationale` needs the `Requirement` it argues
   for, and before this the surface rendered the changed cells alone. */
.ctx{display:none;flex-direction:column;gap:.5rem;margin-top:.15rem;
  border-top:1px dashed var(--border);padding-top:.6rem;}
body.ctx-open .ctx{display:flex;}
/* Label beside value, not above it: a row carries a dozen cells and most hold
   one word, so the stacked `.field` shape used elsewhere pushed the NEXT diff a
   screen down — context that buries what it was added to support. */
.ctx .field{display:grid;grid-template-columns:minmax(5rem,10.5rem) 1fr;
  gap:.15rem .9rem;align-items:baseline;}
.ctx .field .k{overflow-wrap:anywhere;}
@media (max-width:34rem){.ctx .field{grid-template-columns:1fr;}}
.ctxhead{font-size:var(--tiny);text-transform:uppercase;letter-spacing:.08em;
  color:var(--muted);font-weight:600;}
.hint{color:var(--muted);font-size:var(--xsmall);}
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
    // The SAME control governs both halves of "focus": the middles of long
    // unchanged runs, and the cells that did not change at all.
    document.body.classList.toggle('ctx-open',!box.checked);
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


def theme_tokens(css=None):
    """`{"light": {token: value}, "dark": {...}}` parsed out of the EMITTED CSS —
    the single source the page actually ships. The drift guard compares this
    against the dashboard's own emitted values; a value that exists only in a
    test fixture would prove nothing (122-REVIEW-A)."""
    css = CSS if css is None else css
    root = re.search(r":root\{([^}]*)\}", css, re.S)
    dark = re.search(
        r"@media \(prefers-color-scheme:dark\)\{\s*:root\{([^}]*)\}", css, re.S
    )
    out = {}
    for name, block in (("light", root), ("dark", dark)):
        found = dict(
            re.findall(
                r"(--[\w-]+):\s*(#[0-9a-fA-F]{3,8})",
                block.group(1) if block else "",
            )
        )
        out[name] = {t: found[t] for t in THEME_TOKENS if t in found}
    return out


def read_view(path):
    """The view as written, without universal-newline translation."""
    with path.open(encoding="utf-8", newline="") as fh:
        return fh.read()


def normalize(text):
    """Line endings folded to LF for COMPARISON only.

    Two failure modes pull in opposite directions and this is the seam that
    satisfies both. A registry cell can hold a CRLF (what a Windows-authored
    multi-line CSV cell carries): `write_text` turned that into CR CR LF and read
    it back as two LFs, so the view failed `--check` the moment it was generated
    (122-REVIEW-A). But a *checkout* can also carry CRLF line endings by local
    git convention, and a byte-exact compare would then red every fresh worktree
    — which the WI-322 rework caught when the integrate suite's detached view
    worktree went STALE. So: emitted cell text is stripped of CR at the source
    (`esc`), the file is written LF-only, and the compare normalizes both sides —
    the artifact is line-ending-clean and the gate is line-ending-agnostic."""
    return text.replace(chr(13) + chr(10), chr(10)).replace(chr(13), chr(10))


def esc(text):
    # CR is stripped HERE, at the single choke point every registry value passes
    # through: a CR inside a CSV cell is an authoring artifact of the editor that
    # wrote it, and carrying it into the emitted HTML makes the artifact's line
    # endings depend on who last touched the registry (WI-322 rework).
    return html.escape(normalize(text or ""), quote=True)


def load_open_items(root):
    """Rows of the open-items registry, `-000` example rows dropped (the
    copy-ready placeholder convention every other registry uses). Missing file
    -> [] : a repo that carries no decisions yet still renders a view.

    Through `spine_carrier.load`, which is what makes the missing-file arm safe.
    Reading the registry directly, an UNPARSEABLE carrier came back as no rows
    and this view rendered "no open items" — the owner's decision queue
    reporting empty because it could not be read, which is the false green D-5
    built the None-not-`{}` rule for. `load` raises on that and returns `[]`
    only when the registry genuinely is not there."""
    return [
        r
        for r in spine_carrier.load(Path(root) / OPEN_ITEMS_REL, "OI-ID")
        if (r.get("OI-ID") or "").startswith("OI-") and not r["OI-ID"].endswith("-000")
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
        elif came:
            # A whitespace-only insertion is not worth MARKING, but dropping it
            # fused the neighbours — "a  b" → "a b" rendered as "ab". The
            # reconstructed "after" must be the cell the owner is blessing, so
            # the run is emitted unmarked (122-REVIEW-A).
            out.append('<span class="eq">{}</span>'.format(esc(came)))
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
    out = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _safe_link, out)
    return out


def md_block(text):
    """The same inline forms, plus the three BLOCK forms a decision brief needs:
    blank-line-separated paragraphs, `- ` bullet lists, and `### ` sub-headings.

    Why this exists: `md_inline` renders a cell as ONE run of text, so a brief
    written as four paragraphs and a bulleted option list arrived on the owner's
    screen as a single wall — the owner's words, 2026-08-12: "huge blocks of
    single bloated paragraphs". The prose was structured; the renderer flattened
    it. That is a rendering defect, not an authoring one, and fixing it in the
    author (shorter cells) would have traded away the reasoning a ruler needs.

    Still deliberately NOT a markdown parser, for the reason `md_inline` gives —
    three block forms, recognized line-wise, everything else passed through as
    paragraph text. Unknown syntax degrades to visible literal text rather than
    disappearing, which is the same failure direction `_safe_link` chose."""
    blocks, para, bullets = [], [], []

    def flush():
        if bullets:
            blocks.append(
                "<ul>" + "".join("<li>{}</li>".format(b) for b in bullets) + "</ul>"
            )
            bullets.clear()
        if para:
            blocks.append("<p>{}</p>".format(" ".join(para)))
            para.clear()

    for raw in (text or "").split("\n"):
        line = raw.strip()
        if not line:
            flush()
        elif line.startswith("### "):
            flush()
            blocks.append("<h4>{}</h4>".format(md_inline(line[4:].strip())))
        elif line.startswith("- "):
            if para:
                flush()
            bullets.append(md_inline(line[2:].strip()))
        else:
            if bullets:
                flush()
            para.append(md_inline(line))
    flush()
    return "".join(blocks)


# A link target is emitted as an anchor ONLY when it is a fragment, a relative
# path, or http(s). These cells are agent-authored prose landing on the one
# document a human reads, so an unrestricted target ships a clickable
# `javascript:` URL onto the owner's decision surface (122-REVIEW-A). An unsafe
# target is not silently dropped — it degrades to visible literal text, so the
# reader still sees what the brief said.
_SAFE_TARGET = re.compile(r"(?:#|\.{0,2}/|[\w.-]+/|https?:)")


def _safe_link(match):
    text, target = match.group(1), match.group(2)
    if _SAFE_TARGET.match(target):
        return '<a href="{}">{}</a>'.format(target, text)
    return "{} ({})".format(text, target)


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
                    '<div class="v">{}</div></div>'.format(esc(label), md_block(val))
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


def _context_block(full, skip=(), heading="the rest of this row"):
    """The row's remaining cells as labelled fields — the CONTEXT a diff omits.

    A per-cell diff answers *what moved*; it cannot answer *what the row now
    says*, and those are different questions to someone deciding whether the
    existing evidence still verifies an amended requirement. The first sitting
    under this surface hit exactly that: a `Rationale` rewritten in full, with
    the `Requirement` it justifies nowhere on the page. Rendered always, revealed
    by clearing the toolbar box (hence hidden markup rather than a second
    generator mode — the owner is one click from full context, not one re-run).

    `skip` drops the cells the diff already showed, so the block is a complement
    and never a second, unmarked copy of the changed text. Empty cells are
    dropped for the same reason the whole-row states drop them: a column with no
    value is not context, it is noise between the ones that carry it."""
    fields = []
    for key, val in (full or {}).items():
        if key in skip or not (val or "").strip():
            continue
        fields.append(
            '<div class="field"><span class="k">{}</span>'
            '<span class="v">{}</span></div>'.format(
                esc(key), esc(tr.truncate_cell(val.strip()))
            )
        )
    if not fields:
        return ""
    return '<div class="ctx"><div class="ctxhead">{}</div>{}</div>'.format(
        esc(heading), "".join(fields)
    )


# The two cells the anchor block below renders on its own — excluded from
# `_context_block`'s collapsed "rest of this row" so the owner never sees the
# same Requirement/Rationale twice, once visible and once behind the toggle.
_ANCHOR_CELLS = ("Requirement", "Rationale")


def _anchor_block(sr_row):
    """The anchor SR's OWN reviewable text — Requirement verbatim, Rationale
    truncated the same way — rendered UNCONDITIONALLY for every card, never
    inside `.ctx`.

    THE OWNER'S REPORT, VERBATIM (2026-08-24): opening `open-items.html` and
    looking at an owing SR, the Requirement text was nowhere on the page. It
    was, in fact, on the page — `_context_block` already rendered it, for the
    SR-unchanged-chain-amended case — but only inside `.ctx`, which is
    `display:none` until a reader clears the "Collapse unchanged text" toolbar
    box (checked by default). A card that renders only ids and pills above the
    fold reads as having no requirement text at all, which is exactly the
    complaint. This block sits OUTSIDE that toggle so the anchor requirement is
    always the first thing under the card's heading — for every entry, not
    only the ones where the SR row itself carries no diff."""
    if not sr_row:
        return ""
    parts = []
    for key in _ANCHOR_CELLS:
        val = (sr_row.get(key) or "").strip()
        if val:
            parts.append(
                '<div class="field"><span class="k">{}</span>'
                '<div class="v"><p>{}</p></div></div>'.format(
                    esc(key), esc(tr.truncate_cell(val))
                )
            )
    if not parts:
        return ""
    return '<div class="anchor">{}</div>'.format("".join(parts))


ROW_STATE_TAGS = {
    "changed": "changed",
    "added": "ADDED since the snapshot",
    "removed": "REMOVED since the snapshot",
    "current": "current content",
    # WIDENED (the OI-61-sitting gap): a `Drafted` row present in the snapshot
    # byte-identical to its current text still owes a first approval — it just
    # never moved since being copied wholesale by `intake.py snapshot`, which
    # copies every registry, not only approved rows.
    "drafted": "Drafted — never approved",
}


def _chain_row(row):
    """One chain row of a section: its per-cell diff where the baseline has a
    before, its whole current content where it does not.

    Split out of `_attestation_cards` when the context block pushed that
    function over the complexity ratchet — decomposition rather than a baseline
    bump, which is the escape the ratchet exists to force."""
    inner = []
    if row["state"] == "changed":
        # TWO GROUPS, §A5.1 (D-9 step 4). An APPROVED cell that moved owes an
        # attestation; a TRACED one routes to adjudication and arms no window
        # (the WI-388 ruling). Rendering them in one undifferentiated list asked
        # the owner to make that judgement per cell, from memory, mid-sitting —
        # and the snapshot comparison hands the split over for free. The heading
        # appears only when both groups are present; a lone heading over the
        # only group is noise.
        approved = row.get("approved") or frozenset()
        groups = [
            (
                "approved — re-attestation owed",
                [c for c in row["cells"] if c[0] in approved],
            ),
            (
                "traced — routes to adjudication",
                [c for c in row["cells"] if c[0] not in approved],
            ),
        ]
        both = all(cells for _label, cells in groups)
        for label, cells in groups:
            if not cells:
                continue
            if both:
                inner.append('<div class="cellgroup">{}</div>'.format(esc(label)))
            for name, before, after in cells:
                inner.append(
                    '<div class="cellname">{n} <span class="pill">{p}% of the '
                    'words changed</span></div><div class="diff">{d}</div>'.format(
                        n=esc(name),
                        p=changed_percent(before, after),
                        d=word_diff(before, after),
                    )
                )
        inner.append(
            _context_block(
                row["full"],
                skip={name for name, _, _ in row["cells"]},
                heading="the rest of this {} — unchanged since the snapshot".format(
                    row["kind"]
                ),
            )
        )
    else:
        if row["state"] == "drafted":
            # Same wording the pre-widening EMPTY-entry branch used for this
            # exact case (a row whose only claim on the brief is its own
            # `Status`, not a diff) — this row used to be silently dropped
            # instead of rendered, and the entry-level empty message covered
            # for it; now it renders itself, with the reason kept identical
            # so a reader who saw the old wording sees the same words.
            inner.append(
                '<p class="empty">No cell differs from the approved snapshot. '
                "This row is here because its own <code>Status</code> asks for "
                "a human, not because its text moved.</p>"
            )
        for key, val in (row["full"] or {}).items():
            if (val or "").strip():
                inner.append(
                    '<div class="cellname">{k}</div><div class="diff">{v}</div>'.format(
                        k=esc(key), v=esc(tr.truncate_cell(val.strip()))
                    )
                )
    # WIDENED: WHY does this row owe — drift (its state already says so) or a
    # first approval it never received (its own `Drafted` Status, independent
    # of whether its text also moved)? A row whose state is already "drafted"
    # carries the reason in the base tag; anything else states it as an add-on
    # so "ADDED since the snapshot" and "Drafted, never approved" both show
    # rather than one silently standing in for the other.
    tag = ROW_STATE_TAGS[row["state"]]
    if row.get("drafted") and row["state"] != "drafted":
        tag = "{}, Drafted — never approved".format(tag)
    return (
        '<div class="row"><div class="row-head">'
        '<span class="rid">{k} {i}</span>'
        '<span class="pill">{s}</span></div>{b}</div>'.format(
            k=esc(row["kind"]),
            i=esc(row["id"]),
            s=esc(tag),
            b="".join(inner),
        )
    )


# `trace._entry_kind`'s values -> the pill each card wears. Held as a table
# rather than a chain of ternaries so a new kind is a row here and a KeyError
# anywhere it was forgotten, which is the loud direction: a card that silently
# fell back to "re-attest owed" would misdescribe what the owner owes.
#
# BACK TO TWO AT D-9 STEP 5: `plan` ("evidence owed") went out with `Planned`,
# which OI-30 D1 folded into `Approved`. The KeyError-if-forgotten property is
# what makes the removal safe in this direction too — a model still emitting the
# retired kind would fail loudly here rather than render a wrong pill.
_KIND_LABELS = {
    "approve": "approval owed",
    "reattest": "re-attest owed",
}


def _attestation_cards(model, srs_by_id=None):
    """One card per SR owing an approval or a re-attest, its chain beneath.

    `srs_by_id` supplies the SR row's own cells for two things now: the
    UNCONDITIONAL anchor block (`_anchor_block` — the SR's Requirement and
    Rationale, rendered visibly above the fold for every card) and the
    collapsed `sr_ctx` remainder for the case where the SR does NOT appear
    among its chain rows — which happens whenever the SR's own cells did not
    move and an LLR or TC carries the whole amendment. Without the anchor
    block a reader saw ids and pills with no requirement text on the page at
    all (the owner's report, 2026-08-24); without `sr_ctx` a reader diffing a
    child row still had no statement of the requirement it hangs from."""
    srs_by_id = srs_by_id or {}
    if not model:
        return (
            '<p class="empty">No <code>Drafted</code> <strong>SR</strong>, '
            "<strong>LLR</strong>, or <strong>TC</strong> anywhere in the "
            "spine, and no drifted chain — no SR owes an approval or a "
            "re-attest. Say only what was checked: an amended row's own "
            "<code>Status</code> answers for its own cells (owner ruling "
            "2026-08-17m), so a chain row's TEXT moving under an "
            "<code>Approved</code> SR reaches this view through the "
            "snapshot-drift arm — which compares against "
            "<code>docs/archive/last_approved/</code>, the "
            "<code>Modified</code> marker having retired at D-9 step 7 — "
            "but a chain row's <code>Drafted</code> Status reaches this view "
            "DIRECTLY (the OI-61-sitting widening: it used to be checked on "
            "the SR row alone, `docs/log.d/2026-08-23-oi61-rule-and-spine-"
            "approval.md`), not only through drift.</p>"
        )
    cards = []
    for entry in model:
        # KeyError on an unknown kind, deliberately (see `_KIND_LABELS`).
        label = _KIND_LABELS[entry["kind"]]
        head = (
            '<h3><span class="rid">{i}</span><span>{t}</span>'
            '<span class="pill{cls}">{label}</span></h3>'.format(
                i=esc(entry["id"]),
                t=esc(entry["title"] or "(untitled)"),
                cls="" if entry["kind"] == "reattest" else " approve",
                label=label,
            )
        )
        # THE BASELINE IS HOISTED (D-9 step 4). It used to be per-card because
        # every SR carried its OWN git-derived revision; under the snapshot
        # there is exactly one baseline for the whole page, stated once in the
        # section header. What stays per-card is the only thing still per-row:
        # WHY this row has no baseline at all.
        base = (
            ""
            if not entry["no_baseline_reason"]
            else '<p class="baseline">no baseline — {}</p>'.format(
                esc(entry["no_baseline_reason"])
            )
        )
        # UNCONDITIONAL and never hidden — see `_anchor_block`'s docstring for
        # the gap this closes (the owner's report, verbatim).
        anchor = _anchor_block(srs_by_id.get(entry["id"]))
        # The SR's own REMAINING text (SN-Refs, Boundary-Refs, … — Requirement
        # and Rationale are excluded: `anchor` above already showed them,
        # unconditionally), for the section where the SR row itself does not
        # render: nothing but the Status flip touched it, so the amendment sits
        # entirely in a child LLR/TC.
        sr_ctx = ""
        if not any(r["kind"] == "SR" and r["id"] == entry["id"] for r in entry["rows"]):
            sr_ctx = _context_block(
                srs_by_id.get(entry["id"]),
                skip=_ANCHOR_CELLS,
                # The heading named "beyond the Status flip" until D-9 step 7,
                # when the flip retired: an amended row's Status does not move at
                # all now, so the honest statement is about the SR's OWN cells.
                heading="{} itself — no cell of this row changed".format(entry["id"]),
            )
        body = [_chain_row(row) for row in entry["rows"]]
        if not entry["rows"]:
            # The "check the baseline" advice this used to give was about a
            # failure mode that no longer exists: an auto-derived baseline could
            # sit AFTER the amendment, so an empty section meant "the baseline
            # is wrong", and `--since` was the escape. A snapshot cannot sit
            # after the amendment it precedes, so an empty section now means
            # exactly what it says.
            body.append(
                '<p class="empty">No cell differs from the approved snapshot. '
                "This row is here because its own <code>Status</code> asks for a "
                "human, not because its text moved.</p>"
            )
        cards.append(
            '<article class="card" id="{i}">{h}{a}{b}{c}{rows}</article>'.format(
                i=esc(entry["id"] + "-attest"),
                h=head,
                a=anchor,
                b=base,
                c=sr_ctx,
                rows="".join(body),
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


def live_registry_rel(root):
    """The open-items registry's path under whichever carrier is live, for the
    pointers this view renders. Falls back to the destination carrier's name
    when neither exists, so a vacuous render still points somewhere sane."""
    live = spine_carrier.resolve(Path(root) / OPEN_ITEMS_REL)
    return spine_carrier.stem(OPEN_ITEMS_REL) + (live.suffix if live else ".toml")


def render(root):
    """The whole page. Deterministic: every input is sorted upstream.

    NO `since` PARAMETER SINCE D-9 STEP 4. It existed to override a git-derived
    baseline that could sit AFTER the amendment it was supposed to precede — the
    pre-regime-streak case. A snapshot is a directory of files copied at an
    approval, so it cannot sit after anything; there is nothing to override, and
    with it goes the baseline stamp `--check` needed in order to reproduce an
    earlier render."""
    root = Path(root)
    reg = tr.load_registries(root / "docs")
    # The model selects on STATE, not on a status literal (D-9 step 4):
    # `Drafted`, or a chain that has DRIFTED from the approved snapshot. Drift
    # is the arm no cell can carry, and the reason this page survived both the
    # rename and step 7's retirement with nothing to re-key.
    model = tr.reattest_model(root, reg.srs, reg.llrs, reg.tcs)
    items = load_open_items(root)
    pure = pending_block_text(root)
    stamp_rev, stamp_date = baseline_snapshot.stamp(root)
    counts = {
        "pending": sum(
            1 for r in items if (r.get("Status") or "").strip().lower() == "pending"
        ),
        "attest": len(model),
        "rows": sum(len(e["rows"]) for e in model),
        # The drifted count is the one number that cannot be read off a Status
        # cell: a row whose text moved away from what was approved, while its
        # own Status still claims approval.
        "drifted": sum(1 for e in model if not e["no_baseline_reason"]),
        "baseline": (
            "<code>{}</code> — copied {} ({}), the reviewed commit that last "
            "moved an approval".format(
                esc(baseline_snapshot.SNAPSHOT_DIR), esc(stamp_date), esc(stamp_rev)
            )
            if stamp_rev
            else "<code>{}</code> — no snapshot exists yet, so every row below "
            "awaits a FIRST approval and shows its current text in "
            "full".format(esc(baseline_snapshot.SNAPSHOT_DIR))
        ),
    }
    return (
        "<!doctype html>\n"
        '<html lang="en"><head><meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        "<title>Open items — owner decision surface</title>\n"
        "<style>{css}</style>\n"
        # Without scripting the checkbox governs nothing, so the honest default
        # is the FULLER page: context visible rather than a control that lies.
        "<noscript><style>.ctx{{display:flex;}}</style></noscript>\n"
        "</head><body>\n"
        '<div class="wrap">\n'
        "<header>\n"
        '<p class="eyebrow">generated — do not hand-edit · '
        "<code>python project-trajectory/scripts/gen_open_items.py</code></p>\n"
        "<h1>Open items — owner decision surface</h1>\n"
        '<p class="sub">{pending} pending decision(s) · {attest} spine row(s) owing a '
        "approval or a re-attest, across {rows} chain row change(s); "
        "{drifted} row(s) drifted from the approved snapshot. Briefs are rows "
        "in <code>{registry}</code>; the attestation depth is "
        "computed by <code>trace.reattest_model</code>, the same code behind "
        "<code>trace.py --approve</code>. If the two ever disagree, the brief is "
        "authoritative and this view is the bug.</p>\n"
        '<p class="baseline">Baseline: {baseline}</p>\n'
        "</header>\n"
        '<section class="band"><p class="eyebrow">1 · Pending decisions</p>{briefs}</section>\n'
        '<div class="toolbar"><label><input type="checkbox" id="focus" checked> '
        "Collapse unchanged text and the cells that did not change</label>"
        '<span class="hint">clear it to read every row in full — each amended '
        "row's remaining cells, and the SR text a chain-only amendment hangs "
        "from</span></div>\n"
        '<section class="band"><p class="eyebrow">2 · Approval &amp; '
        "re-attestation</p>{attestations}</section>\n"
        '<section class="band"><p class="eyebrow">3 · Pending owner actions '
        "(derived)</p>{pointers}</section>\n"
        "<footer>Source: <code>{registry}</code> + the spine "
        "registries. Rule a decision by appending to <code>docs/log.md</code>'s "
        "Decisions log and setting the row's <code>Status</code>; bless an amendment "
        "by re-reading the drifted cells and running "
        "<code>intake.py snapshot</code> in a reviewed commit — the copy IS the "
        "blessing now that no <code>Status</code> cell records one, so without it "
        "the record of what was blessed does not move. The gate re-derives on its own.</footer>\n"
        "</div>\n<script>{js}</script>\n</body></html>\n"
    ).format(
        css=CSS,
        js=JS,
        briefs=_brief_cards(items),
        attestations=_attestation_cards(
            model, {r.get("SR-ID"): r for r in reg.srs if r.get("SR-ID")}
        ),
        pointers=_pointer_list(pure),
        # The LIVE carrier, never a hardcoded suffix: this view is the surface
        # an owner rules from, and a pointer at the file the repo no longer has
        # (or has not migrated to yet) sends them to edit nothing.
        registry=live_registry_rel(root),
        **counts,
    )


def pending_block_text(root):
    """The pending-projection markdown item text, reused from the `pending.py`
    read model rather than recomputed — one home for "what is pending".

    THE IMPORT SHRANK AT WI-483 SLICE 3 without the seam moving: this used to
    reach the same derivation through `gen_trajectory`, the ~1,000-line render
    facade, which is the 2026-08-19 review's "imports the large facade for a
    state query" (H-02). A view asking another view's family for state was the
    edge; the derivation now sits below both."""
    return pending.pending_block(root)


# --- The deferral arms (OI-41, ruled 2026-08-20) ------------------------------
# A generated view can be perfectly FRESH and carry nothing: before 2026-08-18
# this check reported UP TO DATE — truthfully, the bytes matched — over a
# registry holding one pending row, the inert `-000` example, while about TEN
# genuine owner decisions were live in log fragments, allow entries and session
# reports. Every freshness gate here asks *does the artifact match its
# regeneration*; none of them asked whether the SOURCE was populated, and the
# reassuring word is the same in both cases.
#
# The two arms below are the count half of the answer (the field half is
# `trace.provenance_allow_findings`). Both are WARN-FIRST by the ruling: they
# print, they never move this step's exit code, which stays the freshness verdict.

LOG_D_REL = "docs/log.d"

# ARM 2's grammar. The marker is the KEY `deferred:` — a declaration position,
# never a vocabulary of defer-PHRASES, which is what OI-41 refused: a phrase
# matcher's precision is a property of the wording it meets, so its false-positive
# rate cannot be bounded before it ships. What follows the key on that line is the
# declaration: `OI-###` ids, or an explicit none-word.
#
# Canonical form, and the whole tax on a session close:
#     Deferred open items: OI-45, OI-46
#     Deferred open items: none — every question this session raised was ruled.
# Prose that states it inline satisfies the same key (measured on the live
# fragment `2026-08-20-owner-rulings-review-ois.md`, whose sentence reads
# "…declaring what was deferred: **nothing new was deferred by this session**").
DEFERRED_DECL_RE = re.compile(
    r"\bdeferred(?:\s+open\s+items?)?\s*:[ \t]*([^\n]*)", re.I
)
# The explicit NONE declaration — the ruled answer to the objection that a
# zero-pending queue is a legitimate state which now needs a way to be SAID, or
# the vacuity arm becomes a permanent warning that gets silenced.
NONE_WORDS = frozenset({"none", "nothing", "no", "n/a", "nil"})
_OI_IN_TEXT_RE = re.compile(r"\bOI-\d+\b")

# A fragment SECTION. `### ` because that is the level a multi-entry fragment
# uses for its per-item records (the grind fragment's twenty per-WI entries);
# `## ` is the fragment's own title.
_SECTION_RE = re.compile(r"^###\s+(.*)$", re.M)


def fragment_declarations(root):
    """What each `docs/log.d/` fragment DECLARES it deferred: a list of
    `{file, line, ids, none, scope}`, sorted by file.

    **POSITION IS SCOPE** (2026-08-20, the batch review's MAJOR-7). A declaration
    standing inside a `### ` section speaks for THAT SECTION (`scope` is the
    heading); one standing in the fragment's top matter, above the first section,
    speaks for the whole fragment (`scope` is None). The rule was forced by
    measurement: the day's grind fragment carried twenty per-WI sections and ONE
    declaration — `Deferred open items: none`, inside the WI-485 entry, true of
    that entry — and it read as the file's answer while two decisions announced
    in other sections had no rows at all. That is OI-41's founding class
    reproduced inside the very artifact built to catch it.

    The cheaper of the two candidate rules, deliberately: the alternative (one
    declaration per FILE, the fragment defined as one session's record) needs a
    definition of "session" the log does not carry — several fragments on one day
    are one session, and one fragment can span two. Position is already in the
    text, costs one regex, and is what a reader is doing anyway.

    ARM 2, and it is the DECLARED-WEAK arm — ruled with its weakness on the
    record rather than discovered later. It reaches the class ARM 1 cannot: a
    deferral that suppresses no mechanized rule at all (the `B-08`/`REL-004`
    watermark ruling was exactly that shape — announced twice on two surfaces,
    queued nowhere), because no allow entry would ever exist to carry the field.
    Its weakness is the opposite of a matcher's: a session that defers silently
    and says nothing passes clean, and no mechanism here reaches that.

    FAIL-SOFT, so the arm cannot false-positive: a marker line carrying neither
    an id nor a none-word declares NOTHING and is dropped — the same rule
    `docs/provenance-allow` applies to a malformed entry, in the same direction
    (the worst it can do is leave a deferral unrecorded, never invent one)."""
    out = []
    for path in sorted(Path(root).joinpath(LOG_D_REL).glob("*.md")):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        sections = [(m.start(), m.group(1).strip()) for m in _SECTION_RE.finditer(text)]
        for match in DEFERRED_DECL_RE.finditer(text):
            payload = match.group(1)
            ids = _OI_IN_TEXT_RE.findall(payload)
            first = payload.replace("*", "").replace("_", "").split()
            none = bool(first) and first[0].strip(":;,.").lower() in NONE_WORDS
            if not ids and not none:
                continue
            above = [head for start, head in sections if start < match.start()]
            out.append(
                {
                    "file": "{}/{}".format(LOG_D_REL, path.name),
                    "line": text.count("\n", 0, match.start()) + 1,
                    "ids": ids,
                    "none": none and not ids,
                    "scope": above[-1] if above else None,
                }
            )
    return out


def fragment_scope_findings(root):
    """ARM 2's SCOPE rule as printable lines: a sectioned fragment whose only
    declarations are section-scoped leaves its other sections undeclared, and a
    reader generalises the one answer they can see.

    Warn-first like the rest of ARM 2, and narrow in three ways so it cannot
    become the noise that gets the arm ignored: it fires only on a fragment with
    at least TWO sections, only when that fragment already carries at least one
    declaration (a fragment that declares nothing is the arm's ruled weakness,
    not this rule's business), and it prints ONE line per fragment naming the
    count rather than one per undeclared section. The fix is one line of top
    matter: a file-level declaration speaks for the whole fragment."""
    out = []
    for path in sorted(Path(root).joinpath(LOG_D_REL).glob("*.md")):
        rel = "{}/{}".format(LOG_D_REL, path.name)
        decls = [d for d in fragment_declarations(root) if d["file"] == rel]
        if not decls:
            continue
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        heads = [m.group(1).strip() for m in _SECTION_RE.finditer(text)]
        if len(heads) < 2 or any(d["scope"] is None for d in decls):
            continue
        declared = {d["scope"] for d in decls}
        missing = [h for h in heads if h not in declared]
        if not missing:
            continue
        out.append(
            "{}: {} of {} sections carry no deferral declaration, and the {} "
            "that do speak only for their own section (first: `{}`). A reader "
            "takes the one answer they can see for the file's. Add a "
            "FILE-LEVEL `Deferred open items:` line to the fragment's top "
            "matter, above the first `### ` heading — that one speaks for the "
            "whole fragment".format(
                rel,
                len(missing),
                len(heads),
                len(decls),
                decls[0]["scope"],
            )
        )
    return out


def _entry_groups(entries):
    """Allow entries grouped by the `OI-###` they name, for a finding that NAMES
    them without printing one line per entry (16 of this repo's 17 name one row).
    An entry with no id is grouped under `None` — ARM 1 reports it as an error,
    and this arm still counts it rather than pretending the surface is empty."""
    groups = {}
    for e in entries:
        groups.setdefault(e["oi"], []).append(e)
    return groups


def deferral_findings(root, states=None):
    """ARM 2 + ARM 3 of OI-41 as printable lines — warn-first, never the exit code.

    ARM 2: every id a fragment declares deferred must name a PENDING row (an id
    with no row, or a row already ruled, is a declaration that resolves to
    nothing).

    ARM 3, the vacuity check RE-AIMED so it names something: a pending count of
    ZERO while the declared-exception surface still carries entries is a
    contradiction between two artifacts, and the finding NAMES the entries. Not
    "0 pending is a finding" — that is the unactionable form the ruling refused,
    because *something, somewhere, defers* cannot be discharged without doing the
    search by hand. It compares COUNTS, so it fires for a deferral whose wording
    no vocabulary knows.

    **REGISTRY-ABSENT NO LONGER DISARMS IN SILENCE** (2026-08-20, the batch
    review's MAJOR-6). `states is None` means the repo carries no open-items
    registry, and the vacuum is still real — there is no count to contradict, so
    the count arms cannot run. What was wrong was the SILENCE: a repo with an
    exception surface that defers and no queue to defer INTO is the strongest
    form of the founding class, not the weakest, and it was the one state that
    produced nothing at all. It now says so, once, naming how many entries stand.
    Still warn-first, and still no count comparison — an absent registry is a
    migration, and the finding says which one is owed."""
    if states is None:
        entries = tr.parse_provenance_allow(root)
        if not entries:
            return []
        return [
            "{} carries {} exception entr{} while this repo has no {} at all — "
            "every one of them defers a decision into a queue that does not "
            "exist. The layer is always-on: scaffold the registry (the deferrals "
            "already have somewhere to point) or retire the entries".format(
                tr.PROVENANCE_ALLOW,
                len(entries),
                "y" if len(entries) == 1 else "ies",
                OPEN_ITEMS_REL,
            )
        ]
    pending = sorted(k for k, v in states.items() if v == "pending")
    decls = fragment_declarations(root)
    out = fragment_scope_findings(root)
    for d in decls:
        for oid in d["ids"]:
            if oid not in states:
                out.append(
                    "{}:{} declares {} deferred, which has no row in {} — a "
                    "declared deferral names the row that carries it".format(
                        d["file"], d["line"], oid, OPEN_ITEMS_REL
                    )
                )
            elif states[oid] != "pending":
                out.append(
                    "{}:{} declares {} deferred, but that row reads `{}` — a "
                    "deferral names a row the owner has still to rule".format(
                        d["file"], d["line"], oid, states[oid] or "(no status)"
                    )
                )
    if pending:
        return out
    entries = tr.parse_provenance_allow(root)
    for oid, group in sorted(_entry_groups(entries).items(), key=lambda kv: str(kv[0])):
        named = ", ".join("{} {}".format(e["rid"], e["cell"]) for e in group[:3])
        more = "" if len(group) <= 3 else " (+{} more)".format(len(group) - 3)
        out.append(
            "VACUITY — 0 pending rows, yet {} carries {} entr{} naming {}: "
            "{}{}. The queue reports empty while the exception surface still "
            "defers; retire each entry with its ruling's execution, or the row "
            "belongs back in `pending`.".format(
                tr.PROVENANCE_ALLOW,
                len(group),
                "y" if len(group) == 1 else "ies",
                oid or "NO open-items row",
                named,
                more,
            )
        )
    return out


def report_deferrals(root):
    """Print the ARM 2 / ARM 3 findings, and — when there are none — say what was
    CHECKED rather than nothing at all. An empty queue that no surface
    contradicts is a real state and the reader is entitled to see it asserted;
    silence here would read exactly like the "up to date" this row was raised
    over. Returns the finding count (never an exit code).

    **THE ALL-CLEAR IS MEASURED, NOT WORDED** (2026-08-20, the batch review's
    MAJOR-6). It used to print the literal "no allow entry defers" whenever the
    findings list was empty — a sentence, not a reading. Every way the arms can
    be disarmed (a malformed entry the grammar drops, a fragment whose marker
    line declares neither an id nor a none-word) produces exactly that empty
    list, so the reassurance was strongest precisely where the measurement had
    failed. It now prints the COUNTS it actually took: how many entries parsed,
    how many fragment declarations were read, and — the number that matters —
    how many declaring lines the grammar could not read at all."""
    states = tr.open_item_states(root)
    findings = deferral_findings(root, states)
    for line in findings:
        print("gen_open_items: {}".format(line))
    if (
        not findings
        and states is not None
        and not any(v == "pending" for v in states.values())
    ):
        entries, unparsed = tr.read_provenance_allow(root)
        decls = fragment_declarations(root)
        print(
            "gen_open_items: 0 pending rows — and nothing contradicts it: "
            "{} parsed entr{} in {} ({} unreadable declaring line(s)); "
            "{} fragment declaration(s) read, {} of them `none`.".format(
                len(entries),
                "y" if len(entries) == 1 else "ies",
                tr.PROVENANCE_ALLOW,
                len(unparsed),
                len(decls),
                sum(1 for d in decls if d["none"]),
            )
        )
    return len(findings)


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
        "--check",
        action="store_true",
        help="exit 1 when the file is stale, writing nothing (the freshness gate; "
        "a pure function of the committed tree)",
    )
    args = ap.parse_args(argv)
    root = Path(args.root).resolve()
    out = Path(args.out) if args.out else root / OUT_REL
    # Vacuous for a repo that carries neither the registry nor the view: the
    # surface is opt-in, exactly like the markdown block it replaces, so a
    # non-adopter (and a fresh scaffold before its first decision) pays nothing.
    if spine_carrier.resolve(root / OPEN_ITEMS_REL) is None and not out.is_file():
        print(
            "gen_open_items: no {} and no {} — nothing to render (vacuous).".format(
                OPEN_ITEMS_REL, OUT_REL
            )
        )
        return 0
    # The migration has a detector, on BOTH paths. A resynced adopter keeps the
    # retired docs/open-items.md, whose GENERATED PENDING block nothing writes
    # any more — it can sit there asserting a stale owner action, with their
    # status.md still pointing at it, while every gate stays green (122-REVIEW-A
    # planted a fabricated "WI-999 blocked" line and nothing noticed). Warn-only:
    # the migration is the owner's, and failing here would red a repo midway
    # through it.
    if (root / "docs" / "open-items.md").is_file() and spine_carrier.resolve(
        root / OPEN_ITEMS_REL
    ):
        print(
            "gen_open_items: WARN - docs/open-items.md is still present beside "
            "the registry. It was RETIRED by WI-322 and nothing regenerates its "
            "pending block, so anything it claims is now unmaintained. Migrate "
            "any remaining briefs to rows and delete it (the migration recipe is "
            "in the kit's RESYNC_PACK.md)."
        )
    # The DEFERRAL arms run on both paths — the check a commit passes and the
    # regeneration a human runs — because the misreading they exist to stop
    # ("up to date" read as "the queue is empty") happens on both.
    report_deferrals(root)
    if args.check:
        if not out.is_file():
            print(
                "gen_open_items: {} missing — run "
                "`python scripts/gen_open_items.py`".format(OUT_REL)
            )
            return 1
        current = read_view(out)
        fresh = render(root)
        if normalize(current) != normalize(fresh):
            print(
                "gen_open_items: {} STALE — run "
                "`python scripts/gen_open_items.py`".format(OUT_REL)
            )
            return 1
        print("gen_open_items: open-items view up to date.")
        return 0
    # THE BASELINE-REUSE RULE RETIRED WITH `--since` (D-9 step 4). It existed
    # because a regeneration could silently pick a DIFFERENT git-derived
    # baseline and destroy the depth an owner was about to attest from — driven
    # at 122-REVIEW-A, it collapsed 43 chain-row diffs to 18 and `--check` then
    # certified the loss. The snapshot is the same directory on every machine
    # and in CI, so a regeneration cannot move it and there is nothing to reuse.
    fresh = render(root)
    if out.is_file() and normalize(read_view(out)) == normalize(fresh):
        print("gen_open_items: already up to date -> {}".format(out))
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    # Write with an explicit LF newline: write_text NEWLINE-TRANSLATES, so a
    # registry cell holding a CRLF (what a Windows-authored multi-line CSV cell
    # carries) went to disk as CR CR LF and read back as two LFs - the view
    # failed --check IMMEDIATELY after being generated, permanently, with no
    # clean remedy. The sibling generator carries the same fix for the same
    # reason (122-REVIEW-A).
    with out.open("w", encoding="utf-8", newline=chr(10)) as fh:
        fh.write(fresh)
    print("gen_open_items: wrote {}".format(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
