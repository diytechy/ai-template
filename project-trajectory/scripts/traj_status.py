"""The --status snapshot (WI-280 split of gen_trajectory.py).

The docs/status.md GENERATED STATUS splice (WI-202) and the generated
Ready-frontier lines. The facade re-exports, so consumers are unchanged.

THE PENDING-OWNER-ACTIONS DERIVATION (WI-234) LEFT AT WI-483 SLICE 3, down to
`pending.py`, and only its re-exports remain below: it had three readers, of
which this module is one, so the dispatcher and the generated owner surface
each had to import the `gen_trajectory` facade — a render family — to reach a
state query, and the dispatcher reached in for two PRIVATE names. Those were the
2026-08-19 review's two documented bad edges (H-02, M-02).

Contracts: IF-164 — the interface seam this module declares (process.md §8; row
of record in docs/requirements/interfaces.toml).

Contract IF-164: the generated region of `docs/status.md` — the block between
    the GENERATED STATUS markers, and nothing outside them. It carries derived
    facts only: a banner naming the command that regenerates it, the derived
    stage line with its per-phase detail, one spine line (SN/SR/LLR/TC counts,
    drafts, seams, components), the pending open-item one-liners, and the
    dependency-ready frontier in build order, so a closed row drops out of the
    file on the next run. Deterministic — sorted inputs, no clock — and written
    LF on every platform, so `--check` byte-compares it and reports STALE rather
    than writing. A status.md that is absent or carries no marker pair is left
    untouched and passes vacuously; a duplicated marker is refused rather than
    spliced ambiguously.
"""

import re
import sys

import check_trajectory as ct

import traj_parse

# The stage carrier's ONE home: the rung descriptions (slice 0) and the
# `docs/stage` record format (slice 1). A RENDER LEAF NOW IMPORTS NEITHER
# `spine_rules` NOR `derive_stage` — reading the recorded file needs only the
# format, and the derivation engines stay out of a module that draws pages.
from kitlib import ladder as _ladder
from kitlib import stage as _kitstage
from traj_parse import cmp_rows, spine_stats

# --- the pending-owner-actions projection, RE-EXPORTED (WI-483 slice 3) --------
#
# The derivation moved DOWN to `pending.py`, below this module: it had three
# readers and only one of them is the dashboard, so the other two — the
# dispatcher's exit banner and the generated owner surface — each had to import
# the `gen_trajectory` FACADE to reach it, and one of them reached in for the
# two private names below. A read model with three readers belongs beneath all
# three (the `census.py` / `kitlib.station` cut, applied again).
#
# The former private names are kept as aliases rather than updated at their call
# sites: the facade re-exports them, the dashboard's own tests name them, and a
# rename would have cost this slice the byte-identical-behaviour contract it is
# held to for no layering gain. `_SR_REL`, `PAUSE_MALFORMED` and the three
# sources are all `pending`'s now.
from pending import (  # noqa: F401
    PAUSE_MALFORMED,
    blocked_pending as _blocked_pending,
    pause_pending as _pause_pending,
    pending_block,
    spine_pending as _spine_pending,
)


# --- the docs/status.md derived-snapshot block (WI-202) ------------------------
# `--status` splices a GENERATED block into the OTHERWISE hand-authored status.md
# carrying ONLY derived facts (the spine + derived gate + the open-items
# one-liners), the gen_arch_map --doc block-splice idiom. Its
# `--check` is the freshness successor to the WI-200 forward-only token guard:
# with this marker present, check_trajectory.status_forward_only_findings stands
# its token rule down (the marker is `<!-- BEGIN GENERATED ... -->`, which its
# _STATUS_GENERATED_RE matches) and THIS byte-compare becomes the invariant. The
# forward-only INTENT — Next action, the OI briefs, Scope — stays hand-authored
# OUTSIDE the markers. Opt-in: a status.md without the marker pair is left
# untouched, so `--status --check` passes vacuously downstream.
STATUS_MD = "docs/status.md"
STATUS_BEGIN = "<!-- BEGIN GENERATED STATUS -->"
STATUS_END = "<!-- END GENERATED STATUS -->"
# The `# basis:` regex retired with `docs/gate` (WI-498 slice 5): `docs/stage`
# is key=value, so the snapshot addresses a field BY NAME through
# `kitlib.stage.parse` instead of scraping a comment line.

# --- the status.md derived snapshot (WI-202) -----------------------------------


def _fmt_per_phase(value):
    """`{"4": "DevStg-Arch", "5": "DevStg-Reqs"}` back to `4=DevStg-Arch;5=DevStg-Reqs`.

    `kitlib.stage.parse` COERCES the per-phase field to a mapping (so consumers
    address a phase by key); the retired `# basis:` line handed this surface the
    raw string. Rendering it back here rather than reaching for the unparsed text
    keeps one reader of the file — and keeps the snapshot's wording stable across
    the cut-over, so `--status --check` moves for a real reason or not at all."""
    if isinstance(value, dict):
        return ";".join("{}={}".format(k, value[k]) for k in sorted(value))
    return str(value)


def _stage_facts(root):
    """The derived stage record for the status snapshot, read from `docs/stage`
    (`derive_stage.py` owns it; check.py's `derived-stage` step keeps it fresh),
    or `{}` when the file is absent or carries no readable record.

    READS THE RECORDED FILE, not the self-healing reader — the same choice
    `traj_parse._stage_value` records and for the same reason: this block is a
    GENERATED artifact whose own freshness is byte-compared by
    `gen_trajectory.py --status --check`, so it must describe the commit it is
    generated alongside rather than derive a value the file beside it does not
    carry."""
    path = root / _kitstage.STAGE_FILE
    if not path.exists():
        return {}
    try:
        record = _kitstage.parse(path.read_text(encoding="utf-8", errors="replace"))
    except ValueError:  # a hand-edited or cross-ladder value: degrade, never guess
        return {}
    return record or {}


def _spine_counts(root):
    """`{SN,SR,LLR,TC}` string counts for the snapshot, counted from the
    registries.

    THE CACHED-COUNTS FAST PATH RETIRED WITH `docs/gate` (WI-498 slice 5). That
    file's `# basis:` line carried SN/SR/LLR/TC and this function preferred them;
    `docs/stage` deliberately does not — it records the STAGE derivation, and row
    counts are not an input to it (they would have to be fingerprinted to be
    trustworthy, for a display convenience). The registry count was already the
    fallback arm here and is now the only arm, at no new cost class: this
    snapshot already loads the IF and CMP registries two lines below."""
    st = spine_stats(root)
    return {
        "SN": str(st["sn_total"]),
        "SR": str(st["sr_total"]),
        "LLR": str(st["llr_total"]),
        "TC": str(st["tc_total"]),
    }


_OI_ID_RE = re.compile(r"\bOI-\d+\b")


def _clean_oneliner(s):
    """Normalize a projected one-liner: Markdown link `[text](url)` -> its text,
    stray emphasis/backticks dropped, whitespace collapsed. Keeps the snapshot
    scannable and byte-stable regardless of the brief's inline markup."""
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"\*\*|`", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _first_sentence(s):
    """The first sentence of `s` (up to the first sentence-ending `.`/`!`/`?`),
    else all of `s`. A `;`-joined clause stays whole — only a full stop ends it."""
    m = re.search(r"^(.*?[.!?])(?:\s|$)", s)
    return (m.group(1) if m else s).strip()


def _open_item_oneliners(root):
    """`[(OI-id, one-liner)]` for every PENDING decision, id-order — the status
    snapshot's one-line-per-item projection.

    Reads the open-items registry (WI-322, OI-10 ruled option (b); TOML since
    repo-lock §8.1, either carrier resolves):
    the registry is the source and `docs/open-items.html` is the rendered owner
    surface, so a markdown section parse has nothing left to parse. The
    one-liner is the row's `OneLine` cell, else the first sentence of its
    `Recommendation` — the same fallback the markdown contract had, kept so a
    row that states only a recommendation still projects something useful.
    Empty when the registry is absent (a repo carrying no decisions)."""
    p = root / "docs" / "requirements" / "open-items.toml"
    if ct.spine_carrier.resolve(p) is None:
        return []
    out = []
    # Through the CARRIER, not `read_rows`: this projection is spliced into
    # `status.md` and an unreadable registry that came back as no rows would
    # publish "no pending decisions" — the owner's queue reporting empty because
    # it could not be parsed. `load` raises there and returns [] only when the
    # registry is genuinely absent.
    for row in ct.spine_carrier.load(p, "OI-ID"):
        oid = (row.get("OI-ID") or "").strip()
        if not _OI_ID_RE.fullmatch(oid) or oid.endswith("-000"):
            continue
        if (row.get("Status") or "").strip().lower() != "pending":
            continue  # a ruled row is history; the Decisions log holds it
        one = (row.get("OneLine") or "").strip()
        if not one:
            reco = (row.get("Recommendation") or "").strip()
            one = _first_sentence(reco) if reco else ""
        out.append((oid, _clean_oneliner(one)))
    return sorted(out, key=lambda t: int(t[0].split("-")[1]))


# The eight-rung stage ladder's descriptions, for the generated snapshot line.
# A repo is IN a stage; approval is the event that moves it (process.md §4
# "The stage ladder"). Derived by derive_stage.py and read here off the recorded
# `docs/stage`, never recomputed.
#
# THIS WAS A BYTE-IDENTICAL COPY of `spine_rules.STAGE_DESC` until WI-498 slice
# 0, and — unlike `agent_common`'s restatement — NOTHING pinned it. A renderer is
# the worst place for a silent copy: a reworded or inserted rung would have shown
# the dashboard's readers the OLD sentence, or dropped the stage bullet entirely
# (the `stage in _STAGE_LABELS` guard below degrades to bar-only wording), with
# every test still green. The table now has one home in `kitlib.ladder`, which
# this module imports DIRECTLY rather than through `spine_rules`: a render leaf
# should not have to load a 1,400-line derivation engine to read eight strings —
# the same direction WI-483 took `station` out of the merge coordinator.
_STAGE_LABELS = _ladder.STAGE_DESC


def _stage_line(record, detail):
    """The snapshot's first bullet: the rung this repo is IN.

    ONE VOCABULARY, ONE VALUE (WI-498 slice 5). This bullet used to render two —
    the stage the repo was in AND the "next bar to clear" — because two axes were
    derived side by side. The bar axis retired with `docs/gate`, and with it the
    sentence that had to keep telling readers which reading was meant. A stage is
    a STATE; approval is the EVENT that moves it, and it is reported where
    events are (the phase anchors), not folded into the state.

    A `docs/stage` that is absent, or carries a rung this ladder does not name,
    degrades to naming no stage rather than inventing one — the same
    absent-means-absent direction the derivation takes. `bar_label`'s
    "(Release: pending harness driver)" suffix retires with the bar it named:
    `DevStg-Release` is now returned by NOTHING (slice 3), so there is no withheld
    top value for a reader to mistake for a regression."""
    stage = record.get("stage")
    link = "[`derive_stage.py`](../project-trajectory/scripts/derive_stage.py)"
    if stage not in _STAGE_LABELS:
        return (
            "- **Stage:** not derived — no readable `docs/stage`. {link} writes "
            "it; `check.py`'s `derived-stage` step keeps it fresh.".format(link=link)
        )
    ord_txt = record.get("stage-ord")
    of_txt = record.get("stage-of")
    # The position rides the record; when it is absent, name the rung without a
    # position rather than guessing one.
    #
    # `stage-ord` IS 0-BASED and the sentence is 1-BASED, so it is rendered +1.
    # Without that, `DevStg-Needs` — the FIRST rung — read "stage 0 of 8", and
    # this repo at the fourth rung read "stage 3 of 8". The record keeps the
    # 0-based ordinal because that is what comparisons want (`stage_ord` is the
    # index into `STAGE_ORDER`); only the human sentence counts from one, which
    # is why the conversion belongs at the renderer and not in the field.
    where = (
        "stage {o} of {n}".format(o=ord_txt + 1, n=of_txt)
        if isinstance(ord_txt, int) and of_txt is not None
        else "stage"
    )
    # `floored` arrives as a BOOL from `kitlib.stage.parse`, not the `"yes"` the
    # file spells. Comparing against the spelling made this disclosure
    # unrenderable — and it is the one the FLOOR's own design note calls
    # mandatory: the floored value is a selection guarantee, never a claim about
    # the repo, so a reader must be told when it differs from the honest reading.
    floored = " · floored for selection" if record.get("floored") else ""
    return (
        "- **In stage:** **{s}** ({where}, {label}){floored}{detail} — the rung "
        "this repo is IN, derived over its settled spine. {link} derives it, "
        "recorded in [`docs/stage`](stage).".format(
            s=stage,
            where=where,
            label=_STAGE_LABELS[stage],
            floored=floored,
            detail=detail,
            link=link,
        )
    )


def status_block(root):
    """The GENERATED STATUS block CONTENT (between the markers) for docs/status.md:
    the derived stage + spine snapshot (projected from `docs/stage`, the
    freshness-guarded SSOT) plus the open-items one-liners (from the registry). Derived
    facts ONLY — the forward-only intent stays hand-authored outside the markers.
    Deterministic (no clocks), so the `--status --check` byte-compare is stable,
    exactly like the arch-map / dashboard freshness gates."""
    record = _stage_facts(root)
    counts = _spine_counts(root)
    seams = len(ct.load_ifs(ct.spine_carrier.load(root / ct.IF_CSV, "IF-ID")))
    comps = len(cmp_rows(root))

    stage_bits = []
    if record.get("per-phase"):
        stage_bits.append("per-phase `{}`".format(_fmt_per_phase(record["per-phase"])))
    if record.get("phase"):
        stage_bits.append("derived current **phase={}**".format(record["phase"]))
    stage_detail = " ({})".format(", ".join(stage_bits)) if stage_bits else ""

    # THE CARRIER HANDS THIS OVER TYPED (WI-498 slice 5). `docs/gate`'s
    # `# basis:` line was scraped into STRINGS, so the pluralization compared
    # `drafts == "1"`; `kitlib.stage.parse` coerces `drafted` to an INT, against
    # which that test is never true and every repo read "(1 drafts)". Caught by
    # the cut-over's own test repair, and fixed at the comparison rather than by
    # stringifying the field — a typed carrier is the improvement, and a
    # renderer reaching back for the string form would give it up.
    drafts = record.get("drafted")  # renamed with the value at D-9 step 5
    draft_bit = ""
    if drafts is not None:
        draft_bit = " ({} draft{})".format(drafts, "" if drafts == 1 else "s")

    lines = [
        "_GENERATED by `python project-trajectory/scripts/gen_trajectory.py "
        "--status` — do not hand-edit; cite the spine registries + "
        "`docs/stage`, not this rendering (the forward-only intent below is "
        "hand-authored)._",
        "",
        _stage_line(record, stage_detail),
        "- **Spine:** **SN={sn} SR={sr} LLR={llr} TC={tc}**{d} · {seams} seam{sp} · "
        "{comps} component{cp}.".format(
            sn=counts["SN"],
            sr=counts["SR"],
            llr=counts["LLR"],
            tc=counts["TC"],
            d=draft_bit,
            seams=seams,
            sp="" if seams == 1 else "s",
            comps=comps,
            cp="" if comps == 1 else "s",
        ),
    ]
    ois = _open_item_oneliners(root)
    if ois:
        # The LIVE carrier's name, never a hardcoded suffix: this block is
        # spliced into status.md, and a link at the file the repo no longer has
        # is a broken link on the working surface (check_docs's own hard
        # finding), manufactured by a generator.
        oi_rel = ct.spine_carrier.stem("requirements/open-items.toml") + (
            ct.spine_carrier.resolve(
                root / "docs" / "requirements" / "open-items.toml"
            ).suffix
        )
        lines.append(
            "- **Open items** _(pending rows of [{oi}]({oi}); each ".format(oi=oi_rel)
            + "item's blast radius, options and recommendation render in "
            "[open-items.html](open-items.html), the generated owner surface):_"
        )
        lines.extend("  - **{}** — {}".format(oid, one) for oid, one in ois)
    lines.extend(_frontier_lines(root))
    return "\n".join(lines)


# The forward-looking WI list is DERIVED here (WI-284), not hand-authored: the
# scheduler's dependency-ready frontier in build order. Because it lives inside
# the generated block (which check_trajectory.status_forward_only_findings
# exempts) AND is drawn only from ready — i.e. open, never-`done` — rows, a WI
# that integrates simply drops out on the next `--status` regen: the integrator
# runs that regen in _regenerate_disposition_artifacts, so status.md can no
# longer strand a closed id (the cascade that burned WI-276). Pure/deterministic
# (registry-derived, no reservations, no clocks), so `--status --check` stays a
# stable byte-compare. Capped so a long backlog stays one readable line-group.
_FRONTIER_CAP = 12


def _frontier_lines(root):
    """The `- **Ready frontier**` generated bullet: dependency-ready WIs in
    scheduler order, id + one-line title. Empty when nothing is ready (a drained
    or placeholder registry) OR when schedule.py is unavailable (a scaffold that
    omits it), so the block stays byte-stable and vacuous."""
    if traj_parse.schedule is None:
        return []
    try:
        rows = traj_parse.schedule.load_registry_rows(
            root / "docs/requirements/work-items.csv"
        )
        wis = traj_parse.schedule.load_wis(rows)
        # reserved=None -> pure registry frontier
        ready = traj_parse.schedule.frontier(wis)
    except (OSError, ValueError):
        return []
    if not ready:
        return []
    titles = {w["id"]: w.get("title", "") for w in wis}
    prios = {w["id"]: w.get("priority", 0) for w in wis}
    shown = ready[:_FRONTIER_CAP]
    out = [
        "- **Ready frontier** _(dependency-ready WIs in build order — generated "
        "from the scheduler; a closed WI drops out automatically, so this list "
        "is never stale and never names a `done` id):_"
    ]
    for r in shown:
        wid = r["id"]
        p = prios.get(wid, 0)
        pri = " `P{}`".format(p) if p else ""
        title = _clip_title(titles.get(wid, ""))
        out.append("  - **{}**{} — {}".format(wid, pri, title))
    if len(ready) > _FRONTIER_CAP:
        out.append(
            "  - _(+{} more ready — see the dashboard)_".format(
                len(ready) - _FRONTIER_CAP
            )
        )
    return out


def _title_clause(title):
    """The leading clause of a WI Title — the name of the work, before the
    rationale the registry cell carries after it."""
    return title.split(" - ")[0].split(" — ")[0].strip() or "(untitled)"


def _clip_title(title, limit=90):
    """First clause of a WI Title, clipped — the registry titles are long. The
    status.md frontier line still budgets by character (one markdown line, and
    status.md carries its own line budget); the dashboard card does not — see
    `_next_work_title`."""
    head = _title_clause(title)
    if len(head) > limit:
        head = head[: limit - 1].rstrip() + "…"
    return head


def _splice_status(doc_text, content):
    """Replace the text between the STATUS markers with `content`. Returns
    `(new_text, present)`; `present` is False when the marker pair is absent — the
    opt-in posture, a status.md without markers is left untouched so `--status
    --check` passes vacuously downstream. A duplicated marker is refused (it would
    make the splice ambiguous), the gen_arch_map.splice_region rule."""
    if STATUS_BEGIN not in doc_text or STATUS_END not in doc_text:
        return doc_text, False
    if doc_text.count(STATUS_BEGIN) > 1 or doc_text.count(STATUS_END) > 1:
        raise SystemExit(
            "{}: duplicated STATUS marker; keep exactly one {} / {} pair".format(
                STATUS_MD, STATUS_BEGIN, STATUS_END
            )
        )
    pre = doc_text.split(STATUS_BEGIN)[0]
    post = doc_text.split(STATUS_END)[1]
    return "{}{}\n{}\n{}{}".format(pre, STATUS_BEGIN, content, STATUS_END, post), True


def run_status(root, check):
    """`--status` mode: splice the derived snapshot into docs/status.md (or, with
    `check`, byte-compare and fail on drift). Vacuous — exit 0 — when status.md is
    absent or carries no marker pair (the opt-in posture)."""
    path = root / STATUS_MD
    if not path.exists():
        print("gen_trajectory: no {} — nothing to splice (vacuous).".format(STATUS_MD))
        return 0
    current = path.read_text(encoding="utf-8")
    updated, present = _splice_status(current, status_block(root))
    if not present:
        print(
            "gen_trajectory: {} has no GENERATED STATUS markers — vacuous (add the "
            "{} / {} pair to opt in).".format(STATUS_MD, STATUS_BEGIN, STATUS_END)
        )
        return 0
    if check:
        if updated != current:
            print(
                "status snapshot STALE in {}: run `python "
                "scripts/gen_trajectory.py --status`".format(STATUS_MD),
                file=sys.stderr,
            )
            return 1
        print("status snapshot up to date.")
        return 0
    if updated == current:
        print(
            "gen_trajectory: {} status snapshot already up to date.".format(STATUS_MD)
        )
    else:
        # newline="\n" via open() (write_text(newline=) is 3.10+; scripts stay
        # 3.9-runnable, floor 3.11): LF on every OS so the generated block stays
        # byte-stable regardless of a downstream .gitattributes rule.
        with path.open("w", encoding="utf-8", newline="\n") as fh:
            fh.write(updated)
        print("gen_trajectory: status snapshot regenerated -> {}".format(STATUS_MD))
    return 0
