#!/usr/bin/env python3
"""OKF export — the traceability graph as a portable knowledge bundle (Thread 48).

Emits `docs/okf/`: an Open Knowledge Format (OKF v0.1) bundle generated from the
spine registries — one markdown file per concept with YAML frontmatter, the
graph reconstructed as normal markdown links, per-tier `index.md` tables and a
root `index.md` (progressive disclosure). The iron constraint: a **generated
export, never a parallel source of truth** — the reviewed truth stays the CSV
registries; a hand-edited bundle is exactly the drift the kit exists to
prevent, so `--check` regenerates in memory and compares the on-disk bundle
byte-for-byte (the `gen_arch_map` contract; extra files in `docs/okf/` count
as stale, and the write mode prunes them).

Every emitted file opens with a one-line GENERATED banner — a blockquote right
after the frontmatter (or first, in the frontmatter-less `UPSTREAM.md`) — that
names the file a reference copy, points at its source registry/doc, and gives
the regen command, so a reader who lands on a single bundle file can't mistake
it for the reviewed truth. It is source-slotted from one template and carries no
clock, so the freshness gate stays byte-stable.

Stdlib, emit-only: frontmatter is string-formatted (JSON string scalars are
valid YAML), and the kit never *parses* arbitrary OKF — consuming is the job
of OKF's own tooling. Deterministic by construction (sorted rows, no clocks —
the spec's optional `timestamp` field is deliberately omitted so the freshness
gate stays byte-stable). `docs/okf/UPSTREAM.md` pins the targeted spec version;
re-targeting is a visible, human-reviewed bump, never silent drift.

On by default, opt-out (owner ruling): `docs/process.toml` `[checks]
okf_export = false` silences everything — else, for the SN-028 migration
window, the one word `off` in the legacy `docs/okf-export`. A placeholder-only
or absent registry emits nothing and passes vacuously, so a fresh scaffold and
a non-adopter pay nothing.

Usage:  python scripts/gen_okf.py [--root .] [--check]
Exit codes: 0 clean / vacuous / opted-out, 1 stale bundle under --check.

Contracts: IF-012, IF-033, IF-106 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import json
import re
import sys
import tomllib
from pathlib import Path

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

OUT_DIR = "docs/okf"
# The enablement dial's home since the 2026-08-11 overturn of WI-423, and the
# one-word file it replaced — still read as the SN-028 migration-window
# fallback, the way check_privacy.py still reads `docs/privacy-check`.
POLICY = "docs/process.toml [checks] okf_export"
LEGACY_POLICY = "docs/okf-export"

# Layer B2 (Thread 48): the key process docs summarized as `Process Guide`
# concepts, so the WHOLE repo — process knowledge + the requirement graph — is
# one OKF bundle. (relpath, concept-id slug, friendly-title fallback). A doc
# absent in a given repo is skipped, so the shipped list can be generous; the
# meta-repo, whose process masters live under project-trajectory/, gets the
# subset it actually carries. The summary is DERIVED from each doc (never
# hand-authored), and the source doc is left untouched (that mutation is the
# opt-in Layer B1, deferred). Guides emit only alongside a real spine (added
# after emit()'s vacuity gate), so a fresh scaffold stays vacuously clean.
PROCESS_GUIDE_DOCS = [
    ("AGENTS.md", "agents", "Agent guide"),
    ("docs/process.md", "process", "Process"),
    ("docs/process-options.md", "process-options", "Process options"),
    ("docs/architecture.md", "architecture", "Architecture"),
    ("docs/status.md", "status", "Status blackboard"),
    ("docs/plan.md", "plan", "Plan"),
]

UPSTREAM = """# Upstream pin — Open Knowledge Format

This bundle targets **OKF v0.1** (`GoogleCloudPlatform/knowledge-catalog`,
`okf/`). OKF is "a starting point, not a finished standard": when the spec
moves, re-targeting this generator is a **visible, human-reviewed bump** of
this note plus a regeneration — never silent drift (the `check_vendored.py`
posture applied to a spec instead of a doc set).
"""

# ---- small local loaders (duplicated, not imported: the F5 rule keeps small,
# stable helpers inline — gen_trajectory's guarded sibling import stays the
# kit's one sanctioned exception, reserved for the large evolving graph core).


def read_rows(path):
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def split_refs(cell):
    return [t for t in re.split(r"[;,\s]+", (cell or "").strip()) if t]


ID_RE = re.compile(r"^[A-Z]+-\d+$")  # PREFIX-<digits>, the kit-wide id shape


def real_rows(rows, key, prefix):
    """Real (non-placeholder) rows whose id is well-formed. The id becomes a
    path component in emit(), so it must match the kit's `PREFIX-<digits>`
    shape (trace.py's integrity rule) — a crafted id with `/`..`..` would
    otherwise escape docs/okf/ on write. trace.py --strict-integrity is the
    floor that blocks such an id from committing; this is defense-in-depth for
    the standalone run."""
    out = []
    for r in rows:
        rid = (r.get(key) or "").strip()
        if rid.startswith(prefix) and not rid.endswith("-000") and ID_RE.match(rid):
            out.append(r)
    return sorted(out, key=lambda r: r[key].strip())


def sn_rows(root):
    """Every need as the core four — `spine_carrier.folded_needs`, the ONE home
    this rule now has. Was a copy of traj_parse._sn_rows and trace._sn_prose
    kept in sync by a docstring; they drifted."""
    return spine_carrier.folded_needs(root / "docs/requirements/stakeholder-needs.toml")


def _process_check(root, key):
    """One `[checks]` toggle out of `docs/process.toml`, or None when this file
    has nothing to say (fall through to the legacy one-word file).

    A LOCAL reader, per the F5 independently-copyable-script rule — the cost the
    2026-08-11 overturn of WI-423 priced and accepted. Unparseable-but-present,
    or a non-bool value, reads ON: a check that silently stops running is the
    failure worth avoiding. `tests/test_rule_sync.py` pins this copy against
    `check_trajectory.py`'s and `subagent_gate.py`'s by value (D-7)."""
    path = root / "docs" / "process.toml"
    if not path.is_file():
        return None
    try:
        # utf-8-sig: a BOM is not legal TOML but is invisible to a shell read.
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError):
        return True  # unparseable but present: fail loud, never a quiet opt-out
    table = data.get("checks")
    value = table.get(key) if isinstance(table, dict) else None
    if value is None:
        return None
    return value if isinstance(value, bool) else True


def read_enabled(root):
    """Whether the OKF export layer is on. `docs/process.toml` `[checks]
    okf_export = false` opts out; else (migration window) the one word `off` in
    the legacy `docs/okf-export`; absent or any other value reads on (the
    owner-ruled default-on posture)."""
    declared = _process_check(root, "okf_export")
    if declared is not None:
        return declared
    p = root / LEGACY_POLICY
    if not p.exists():
        return True  # absent = on (the owner-ruled default-on posture)
    for ln in p.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if ln and not ln.startswith("#"):
            return ln.lower() != "off"
    return True


# ---- emit ---------------------------------------------------------------------


def fm(pairs):
    """A YAML frontmatter block; JSON string scalars are valid YAML, so quoting
    is safe without a YAML library (emit-only, per the iron constraint)."""
    lines = ["---"]
    for key, val in pairs:
        if isinstance(val, list):
            lines.append("{}: [{}]".format(key, ", ".join(json.dumps(v) for v in val)))
        else:
            lines.append("{}: {}".format(key, json.dumps(val)))
    lines.append("---")
    return "\n".join(lines) + "\n"


def banner(source):
    """The one-line GENERATED provenance blockquote every emitted file carries,
    immediately after the frontmatter (or first, in the frontmatter-less
    UPSTREAM.md): a reader who lands on a single bundle file learns it is a
    reference copy, where the reviewed truth lives, and how to regenerate. One
    template, source-slotted; no clock, so the freshness gate stays byte-stable."""
    return (
        "> **GENERATED — a reference copy, not the source of truth.** Derived "
        "from {} by scripts/gen_okf.py; edit the registry/doc, then rerun it "
        "({} = false silences the layer).".format(source, POLICY)
    )


def concept(rel_dir, cid, ctype, title, description, tags, resource, body_lines):
    head = fm(
        [
            ("type", ctype),
            ("title", title or cid),
            ("description", description),
            ("tags", [t for t in tags if t]),
            ("resource", resource),
        ]
    )
    return (
        head
        + banner(resource)
        + "\n\n# {} — {}\n\n{}\n".format(cid, title or ctype, "\n".join(body_lines))
    )


def links(label, ids, target_dir):
    if not ids:
        return []
    return [
        "- {}: ".format(label)
        + " · ".join(
            "[{0}](../{1}/{0}.md)".format(i, target_dir) for i in sorted(set(ids))
        )
    ]


def field(label, value, fmt="{}"):
    """One optional labelled body section, or nothing when the cell is empty.

    The `links` sibling above for plain cells. Extracted when the LLR gained its
    `Rationale` column and made this the fifth copy of `if cell: body.append(...)`
    inside `emit` — the complexity ratchet caught the fifth and was right to: the
    branch was never the point, the label was."""
    value = (value or "").strip()
    return ["\n**{}.** {}".format(label, fmt.format(value))] if value else []


def _strip_md_links(text):
    """Reduce inline markdown links/images to their visible text. A derived
    summary is prose, not navigation — and a relative link valid in the source
    doc would dangle once transplanted into docs/okf/ (check_docs would flag
    it), so links must not survive into a Process Guide."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # inline [t](u)/![a](u)
    text = re.sub(r"!?\[([^\]]*)\]\[[^\]]*\]", r"\1", text)  # reference [t][ref]
    return text


def _doc_title_and_summary(path):
    """(title, one-line summary) DERIVED from a markdown doc — its first heading
    and its first prose paragraph — so a Process Guide concept regenerates from
    the source and can't drift (Layer B2; never hand-authored). Frontmatter,
    HTML comments, tables, quotes, fences and list markers are skipped; inline
    links are reduced to their text so nothing dangles in the bundle."""
    title, para, started, in_fm = "", [], False, False
    for i, raw in enumerate(
        path.read_text(encoding="utf-8", errors="replace").splitlines()
    ):
        ln = raw.strip()
        if i == 0 and ln == "---":
            in_fm = True
            continue
        if in_fm:
            if ln == "---":
                in_fm = False
            continue
        if not ln or ln.startswith("<!--"):
            if started:
                break
            continue
        if ln.startswith("#"):
            if not title:
                title = ln.lstrip("# ").strip()
            if started:
                break
            continue
        if ln.startswith(("|", ">", "```", "- ", "* ", "1.")):
            if started:
                break
            continue
        para.append(ln)
        started = True
    title = _strip_md_links(title)
    summary = _strip_md_links(" ".join(" ".join(para).split()))
    if len(summary) > 240:
        summary = summary[:239].rstrip() + "…"
    return title, summary


def source_path(root, rel, needs=False):
    """The registry path to CITE, resolved to the carrier that is actually
    live. The bundle's whole promise is that every generated page
    names the file its content came from, so a hardcoded suffix would print a
    path the reader cannot open — in the one line that exists to send them back
    to the source of truth."""
    live = spine_carrier.resolve(
        root / rel, spine_carrier.NEED_CARRIERS if needs else spine_carrier.CARRIERS
    )
    return spine_carrier.stem(rel) + (live.suffix if live is not None else ".toml")


def emit(root):
    """{relpath-under-docs/okf: content} for the whole bundle, or {} when the
    registries are placeholder-only/absent (the vacuous case)."""
    req = root / "docs" / "requirements"
    sns = sn_rows(root)
    # The spine tiers read through the CARRIER so the bundle
    # exports the same cells whether the registries are CSV or TOML.
    srs = real_rows(
        spine_carrier.load(req / "system-requirements.toml", "SR-ID"), "SR-ID", "SR-"
    )
    llrs = real_rows(
        spine_carrier.load(req / "low-level-requirements.toml", "LLR-ID"),
        "LLR-ID",
        "LLR-",
    )
    tcs = real_rows(
        spine_carrier.load(root / "docs/test/test-cases.toml", "TC-ID"), "TC-ID", "TC-"
    )

    sn_src = source_path(root, "docs/requirements/stakeholder-needs.toml", needs=True)
    sr_src = source_path(root, "docs/requirements/system-requirements.toml")
    llr_src = source_path(root, "docs/requirements/low-level-requirements.toml")
    tc_src = source_path(root, "docs/test/test-cases.toml")
    if_src = source_path(root, "docs/requirements/interfaces.toml")
    ifs = real_rows(
        spine_carrier.load(req / "interfaces.toml", "IF-ID"), "IF-ID", "IF-"
    )
    if not (sns or srs or llrs or tcs):
        return {}

    sr_of_sn, llr_of_sr, tc_of = {}, {}, {}
    for r in srs:
        for sn in split_refs(r.get("SN-Refs", "")):
            sr_of_sn.setdefault(sn, []).append(r["SR-ID"].strip())
    for r in llrs:
        for sr in split_refs(r.get("SR-Refs", "")):
            llr_of_sr.setdefault(sr, []).append(r["LLR-ID"].strip())
    for r in tcs:
        for v in split_refs(r.get("Verifies", "")):
            tc_of.setdefault(v, []).append(r["TC-ID"].strip())

    out = {"UPSTREAM.md": banner("the OKF spec pin") + "\n\n" + UPSTREAM}
    tiers = []  # (dirname, [(id, one-liner)], source registry/doc for the banner)

    def add_tier(dirname, entries, source):
        tiers.append((dirname, entries, source))

    entries = []
    for r in sns:
        cid = r["id"]
        body = ["**Need.** {}".format(r["need"])]
        if r["why"]:
            body.append("\n**Why it matters.** {}".format(r["why"]))
        if r["acceptance"]:
            body.append("\n**Acceptance intent.** {}".format(r["acceptance"]))
        body += links("Realized by", sr_of_sn.get(cid, []), "system-requirements")
        out["stakeholder-needs/{}.md".format(cid)] = concept(
            "stakeholder-needs",
            cid,
            "Stakeholder Need",
            r["need"][:80],
            r["need"],
            [],
            "{} ({})".format(sn_src, cid),
            body,
        )
        entries.append((cid, r["need"]))
    add_tier("stakeholder-needs", entries, sn_src)

    entries = []
    for r in srs:
        cid = r["SR-ID"].strip()
        body = ["**Requirement.** {}".format((r.get("Requirement") or "").strip())]
        body += field("Acceptance criteria", r.get("AcceptanceCriteria"))
        body += field("Rationale", r.get("Rationale"))
        body += links("Realizes", split_refs(r.get("SN-Refs", "")), "stakeholder-needs")
        body += links("Decomposed by", llr_of_sr.get(cid, []), "low-level-requirements")
        body += links("Verified by", tc_of.get(cid, []), "test-cases")
        out["system-requirements/{}.md".format(cid)] = concept(
            "system-requirements",
            cid,
            "System Requirement",
            (r.get("Title") or "").strip(),
            (r.get("Requirement") or "").strip(),
            [
                (r.get("Priority") or "").strip(),
                (r.get("Verification") or "").strip(),
                (r.get("Status") or "").strip(),
                (r.get("Aspect") or "").strip(),
            ],
            "{} ({})".format(sr_src, cid),
            body,
        )
        entries.append((cid, (r.get("Title") or "").strip()))
    add_tier("system-requirements", entries, sr_src)

    entries = []
    for r in llrs:
        cid = r["LLR-ID"].strip()
        body = ["**Detail.** {}".format((r.get("Detail") or "").strip())]
        body += field("Rationale", r.get("Rationale"))
        mod = (r.get("Module") or "").strip()
        sym = (r.get("CodeSymbol") or "").strip()
        if mod or sym:
            body.append("\n**Code.** `{}` — `{}`".format(mod, sym))
        body += links(
            "Decomposes", split_refs(r.get("SR-Refs", "")), "system-requirements"
        )
        body += links("Verified by", tc_of.get(cid, []), "test-cases")
        out["low-level-requirements/{}.md".format(cid)] = concept(
            "low-level-requirements",
            cid,
            "Low-Level Requirement",
            (r.get("Title") or "").strip(),
            (r.get("Detail") or "").strip(),
            [(r.get("Status") or "").strip()],
            "{} ({})".format(llr_src, cid),
            body,
        )
        entries.append((cid, (r.get("Title") or "").strip()))
    add_tier(
        "low-level-requirements",
        entries,
        llr_src,
    )

    entries = []
    for r in tcs:
        cid = r["TC-ID"].strip()
        body = ["**Method.** {}".format((r.get("Method") or "").strip())]
        body += field("Expected", r.get("Expected"))
        body += field("Evidence", r.get("Evidence"), "`{}`")
        ups = split_refs(r.get("Verifies", ""))
        body += links(
            "Verifies (SR)",
            [u for u in ups if u.startswith("SR-")],
            "system-requirements",
        )
        body += links(
            "Verifies (LLR)",
            [u for u in ups if u.startswith("LLR-")],
            "low-level-requirements",
        )
        out["test-cases/{}.md".format(cid)] = concept(
            "test-cases",
            cid,
            "Test Case",
            "verifies {}".format((r.get("Verifies") or "").strip()),
            (r.get("Method") or "").strip(),
            [
                (r.get("Tier") or "").strip(),
                (r.get("Level") or "").strip(),
                "Automated={}".format((r.get("Automated") or "").strip() or "?"),
                (r.get("Status") or "").strip(),
            ],
            "{} ({})".format(tc_src, cid),
            body,
        )
        entries.append((cid, (r.get("Method") or "").strip()))
    add_tier("test-cases", entries, tc_src)

    if ifs:
        entries = []
        for r in ifs:
            cid = r["IF-ID"].strip()
            desc = (r.get("Contract") or r.get("Description") or "").strip()
            out["interfaces/{}.md".format(cid)] = concept(
                "interfaces",
                cid,
                "Interface",
                (r.get("Name") or "").strip(),
                desc,
                # `Approval`, not `Status` or `Stability`: the IF `Status`
                # column retired at WI-443 (OI-14 part B), and `Stability`
                # retired for `Approval` at WI-442 — the tier's one maturity
                # field. Reading the retired column shipped `tags: []` on all
                # 113 one-pagers while the live value went nowhere (REVIEW-A).
                [(r.get("Status") or "").strip()],
                "{} ({})".format(if_src, cid),
                ["**Contract.** {}".format(desc)],
            )
            entries.append((cid, (r.get("Name") or "").strip()))
        add_tier("interfaces", entries, if_src)

    # Layer B2: the process docs as `Process Guide` concepts (derived summary +
    # a resource pointer back to the untouched source). From a concept file at
    # docs/okf/process-guides/, three `../` reach the repo root, then the doc.
    guides = []
    for rel, slug, friendly in PROCESS_GUIDE_DOCS:
        doc = root / rel
        if not doc.exists():
            continue
        title, summary = _doc_title_and_summary(doc)
        title = title or friendly
        desc = summary or title
        out["process-guides/{}.md".format(slug)] = concept(
            "process-guides",
            slug,
            "Process Guide",
            title,
            desc,
            [],
            rel,
            [
                "**Summary.** {}".format(desc),
                "",
                "**Source (unmodified).** [{0}](../../../{0}).".format(rel),
            ],
        )
        guides.append((slug, title))
    if guides:
        add_tier("process-guides", guides, "the repo's process docs")

    for dirname, tier_entries, source in tiers:
        lines = [
            "# {} — index".format(dirname),
            "",
            "| id | summary |",
            "|---|---|",
        ]
        for cid, summary in tier_entries:
            one = " ".join(summary.split())
            if len(one) > 90:
                one = one[:89] + "…"
            lines.append("| [{0}]({0}.md) | {1} |".format(cid, one.replace("|", "\\|")))
        out["{}/index.md".format(dirname)] = (
            fm(
                [
                    ("type", "Index"),
                    ("title", dirname),
                    ("description", "tier index"),
                    ("tags", []),
                    ("resource", "generated"),
                ]
            )
            + banner(source)
            + "\n\n"
            + "\n".join(lines)
            + "\n"
        )

    root_lines = [
        "# Knowledge bundle — the traceability graph + process guides",
        "",
        "Spec pin: [UPSTREAM.md](UPSTREAM.md).",
        "",
    ]
    for dirname, tier_entries, _source in tiers:
        root_lines.append(
            "- [{0}]({0}/index.md) — {1} concept(s)".format(dirname, len(tier_entries))
        )
    out["index.md"] = (
        fm(
            [
                ("type", "Index"),
                ("title", "traceability bundle"),
                ("description", "the SN->SR->LLR->TC graph as OKF concepts"),
                ("tags", []),
                ("resource", "generated"),
            ]
        )
        + banner("the spine registries and the process docs")
        + "\n\n"
        + "\n".join(root_lines)
        + "\n"
    )
    return out


def on_disk(out_root):
    if not out_root.exists():
        return {}
    return {
        p.relative_to(out_root).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(out_root.rglob("*"))
        if p.is_file()
    }


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so a
    non-ASCII path / title / registry cell can't raise UnicodeEncodeError on a
    legacy Windows cp1252 console (verbatim across the
    kit). Python 3.7+ streams expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--root", default=".", help="repo root (default: cwd)")
    ap.add_argument(
        "--check",
        action="store_true",
        help="regenerate in memory and compare the on-disk bundle (nonzero on "
        "stale/extra/missing files); never writes. Missing-target posture "
        "(C9): a fully-generated output, so a missing bundle reads as "
        "stale/vacuous — unlike arch-map, whose hand-authored target must exist",
    )
    args = ap.parse_args()
    root = Path(args.root).resolve()
    if not read_enabled(root):
        print("gen_okf: off ({}) — nothing to export.".format(POLICY))
        return 0
    expected = emit(root)
    out_root = root / OUT_DIR
    if not expected and not out_root.exists():
        print("gen_okf: no real registry rows — nothing to export; vacuously clean.")
        return 0
    current = on_disk(out_root)
    stale = sorted(
        set(k for k in expected if expected.get(k) != current.get(k))
        | (set(current) - set(expected))
    )
    if args.check:
        if stale:
            for k in stale[:20]:
                print("gen_okf: STALE - {}/{}".format(OUT_DIR, k), file=sys.stderr)
            print(
                "gen_okf: OKF bundle STALE ({} file(s)): run `python "
                "scripts/gen_okf.py`".format(len(stale)),
                file=sys.stderr,
            )
            return 1
        print("gen_okf: OKF bundle up to date ({} file(s)).".format(len(expected)))
        return 0
    wrote = pruned = 0
    for rel, content in expected.items():
        p = out_root / rel
        if current.get(rel) != content:
            p.parent.mkdir(parents=True, exist_ok=True)
            # open(newline=...) rather than write_text(newline=...): the latter
            # is Python 3.10+; the scripts stay 3.9-runnable (declared floor 3.11).
            with p.open("w", encoding="utf-8", newline="\n") as fh:
                fh.write(content)
            wrote += 1
    for rel in set(current) - set(expected):
        (out_root / rel).unlink()
        pruned += 1
    # Remove now-empty tier directories left by the prune (e.g. interfaces/
    # after the last IF row goes), so a deleted tier leaves no cruft behind.
    if pruned:
        for d in sorted(out_root.rglob("*"), key=lambda p: len(p.parts), reverse=True):
            if d.is_dir() and not any(d.iterdir()):
                d.rmdir()
    if wrote or pruned:
        print(
            "gen_okf: wrote {} / pruned {} -> {} ({} file(s) total).".format(
                wrote, pruned, OUT_DIR, len(expected)
            )
        )
    else:
        print("gen_okf: already up to date -> {}".format(OUT_DIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
