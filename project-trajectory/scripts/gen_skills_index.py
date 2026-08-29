#!/usr/bin/env python3
"""Generate the skills applicability index from the SKILL.md frontmatter.

Stack-agnostic kit, stdlib-only (Python 3.11+). The kit's `skills/` folder holds
agent-neutral skill definitions (one dir per skill, each with a `SKILL.md` whose
YAML-ish frontmatter carries the agent-facing `name`/`description` and this kit's
applicability metadata: `stacks`, `domains`, `phases`, `tags`, `scope`). This
script scans them and writes a flat `skills/INDEX.csv` — one row per skill — so a
human or tool can read applicability cheaply without opening every SKILL.md (the
same "generated, don't hand-maintain" stance as the registries and the code map).

`SKILL.md` frontmatter is a top `---`-delimited block of `key: value` lines. List
values are `[a, b, c]`; scalars are bare. We deliberately parse only that shape
(no external YAML dependency, per the stdlib-only rule) — a SKILL.md that needs
richer YAML is out of scope for the index.

Usage:
    python scripts/gen_skills_index.py [--skills skills] [--check]

    --check   Exit nonzero (and print a diff-style note) if INDEX.csv is stale,
              like `gen_arch_map.py --check`. Use in CI / a gate.
    default   (Re)write skills/INDEX.csv from the SKILL.md files.

Contracts: IF-019 — the interface seam this module declares (process.md §8; row of record in docs/requirements/interfaces.toml).

Contract IF-019: this module is the sole writer of `skills/INDEX.csv`, and the
    file's shape is the contract: a one-line GENERATED banner comment, then a
    header row and one data row per skill under the fixed COLUMNS order —
    name, scope, stacks, domains, phases, tags, description — list values
    rendered space-joined. Rows come from the `SKILL.md` frontmatter alone, so
    the index is a pure function of the source tree and never a second place to
    author applicability. It is written as bytes with LF endings on every
    platform, keeping the committed file diff-free across checkouts.
    `--check` re-renders in memory, compares with line endings normalized —
    row content, not the checkout's newline convention — and exits 1 with a
    STALE line naming the path when they differ. An absent skills directory is
    reported and exits 0, so a repo that vendors no skills pays nothing.
"""

import argparse
import csv
import io
import re
import sys
from pathlib import Path

# The console guard's one home is the shipped package (WI-448 / D-8);
# aliased to the module-local name so no call site changes.
from kitlib.config import utf8_console as _utf8_console

# Column order of the generated index. `scope` and the applicability axes come
# first so a scan can filter on them without reading `description`.
COLUMNS = ["name", "scope", "stacks", "domains", "phases", "tags", "description"]
LIST_FIELDS = ("stacks", "domains", "phases", "tags")


# The per-agent skill dirs the kit fans the neutral source out to (S7). Mirrors
# the `skills_dir` values in bootstrap.AGENTS — kept a small duplicated constant
# (gen_skills_index must not import bootstrap; both stay single stdlib files, the
# F5 rule). `.agents/` is Codex's AGENTS.md-mirror location.
AGENT_SKILLS_DIRS = (".claude/skills", ".gemini/skills", ".agents/skills")

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def _skill_files(skill_dir):
    """Sorted POSIX-relative paths of every file under a skill dir."""
    return sorted(
        p.relative_to(skill_dir).as_posix() for p in skill_dir.rglob("*") if p.is_file()
    )


def check_agent_sync(source, root):
    """Verify every per-agent skill copy under `root` is byte-identical to its
    neutral `source` skill (S7 checked fan-out). Returns (drifts, orphans,
    checked): `drifts` a list of hard-failing drift descriptions, `orphans` a
    list of non-failing warnings (a per-agent copy whose skill no longer exists
    in source), `checked` the number of per-agent skills compared.

    Vacuous (empty) when `source` is absent or no per-agent skills dir exists.
    Only skills that EXIST in a per-agent dir are compared — a subset dir is
    legitimate (a scope-matched downstream materializes only some skills), so a
    source skill MISSING from a per-agent dir is NOT reported. Byte comparison
    reads bytes (a CRLF vs LF difference must neither false-drift nor false-pass;
    the tracked copies are byte-identical as committed)."""
    drifts, orphans, checked = [], [], 0
    if not source.is_dir():
        return drifts, orphans, checked
    for rel_dir in AGENT_SKILLS_DIRS:
        agent_skills = root / rel_dir
        if not agent_skills.is_dir():
            continue
        for name_dir in sorted(p for p in agent_skills.iterdir() if p.is_dir()):
            src_skill = source / name_dir.name
            if not (src_skill / "SKILL.md").exists():
                # A copy with no source can't be verified or fixed by --sync;
                # surface it (a removed skill left behind) but don't hard-fail —
                # the fix is a manual removal, not a re-materialize.
                orphans.append("{}/{}: no source skill".format(rel_dir, name_dir.name))
                continue
            checked += 1
            src_files, dst_files = _skill_files(src_skill), _skill_files(name_dir)
            if src_files != dst_files:
                drifts.append(
                    "{}/{}: file set differs from source (source={}, copy={})".format(
                        rel_dir, name_dir.name, src_files, dst_files
                    )
                )
                continue
            for rel in src_files:
                if (src_skill / rel).read_bytes() != (name_dir / rel).read_bytes():
                    drifts.append(
                        "{}/{}/{}: bytes differ from source".format(
                            rel_dir, name_dir.name, rel
                        )
                    )
    return drifts, orphans, checked


def parse_frontmatter(text):
    """Parse the leading `---`-delimited frontmatter into a dict.

    List values (`[a, b, c]`) become Python lists; everything else is a stripped
    string. Returns {} when there is no frontmatter block.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            fields[key] = [v.strip() for v in inner.split(",") if v.strip()]
        else:
            fields[key] = value
    return fields


def collect_skills(skills_dir):
    """Return the parsed frontmatter of every `<skill>/SKILL.md`, sorted by name.

    Each entry is a dict with the COLUMNS keys; list fields are rendered as
    space-joined strings for the flat CSV. A SKILL.md missing `name`/`description`
    is a hard error (the two agent-required fields)."""
    rows = []
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        name = fm.get("name", "").strip()
        if not name:
            raise ValueError(
                "{}: missing required 'name' in frontmatter".format(skill_md)
            )
        if name != skill_md.parent.name:
            raise ValueError(
                "{}: name '{}' != directory '{}'".format(
                    skill_md, name, skill_md.parent.name
                )
            )
        if not fm.get("description", "").strip():
            raise ValueError("{}: missing required 'description'".format(skill_md))
        row = {"name": name}
        row["scope"] = (fm.get("scope") or "kit").strip()
        for f in LIST_FIELDS:
            val = fm.get(f, [])
            if isinstance(val, str):
                val = [val] if val else []
            row[f] = " ".join(val) if val else "any" if f != "tags" else ""
        row["description"] = fm.get("description", "").strip()
        rows.append(row)
    return rows


# The leading comment row every emitted INDEX.csv carries — the ruled
# generated-but-LIVE form (OI-56 (a), WI-505): a plain `#`-prefixed line, since
# no consumer of this file parses it with `csv.reader`/`DictReader` (each reads
# the SKILL.md frontmatter directly and regenerates; the row-count/applicability
# consumers only check the file's existence or byte-compare it whole), so a
# non-data first line cannot desync a column reader that does not exist.
GENERATED_BANNER = (
    "# GENERATED by scripts/gen_skills_index.py — do not hand-edit; cite the "
    "SKILL.md frontmatter, not this rendering; regenerate: python "
    "scripts/gen_skills_index.py\n"
)


def render_index(rows):
    """Render the rows as CSV text (LF-terminated, stable column order), led by
    `GENERATED_BANNER`."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return GENERATED_BANNER + buf.getvalue()


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skills", default="skills", help="skills dir (default: skills)")
    ap.add_argument(
        "--check",
        action="store_true",
        help="exit nonzero if INDEX.csv is stale (for CI/gates)",
    )
    ap.add_argument(
        "--check-agents",
        action="store_true",
        help="S7 drift gate: exit nonzero if any per-agent skill copy "
        "(.claude/.gemini/.agents) has drifted from the neutral source. Vacuous "
        "when there is no source or no per-agent dir; fix drift with "
        "`bootstrap.py --sync`. Wired into the pre-commit floor + DevStg-Impl like "
        "gen_arch_map --check.",
    )
    ap.add_argument(
        "--source",
        default=None,
        help="neutral skills source for --check-agents (default: the kit's "
        "skills/ beside this script, e.g. project-trajectory/skills)",
    )
    ap.add_argument(
        "--root",
        default=".",
        help="repo root scanned for per-agent skill dirs by --check-agents "
        "(default: the current directory)",
    )
    args = ap.parse_args()

    if args.check_agents:
        source = (
            Path(args.source)
            if args.source
            else Path(__file__).resolve().parent.parent / "skills"
        )
        drifts, orphans, checked = check_agent_sync(source, Path(args.root))
        for o in orphans:
            print("gen_skills_index: WARN orphan copy - {}".format(o), file=sys.stderr)
        if drifts:
            print(
                "gen_skills_index: STALE - per-agent skill copy(ies) drifted from "
                "{}:".format(source),
                file=sys.stderr,
            )
            for d in drifts:
                print("  - {}".format(d), file=sys.stderr)
            print(
                "  run `python project-trajectory/scripts/bootstrap.py "
                "--dest . --sync` to refresh the copies from source.",
                file=sys.stderr,
            )
            sys.exit(1)
        print(
            "gen_skills_index: OK - {} per-agent skill copy(ies) match source.".format(
                checked
            )
        )
        return

    skills_dir = Path(args.skills)
    if not skills_dir.is_dir():
        print("gen_skills_index: no skills dir at {}".format(skills_dir))
        return
    rows = collect_skills(skills_dir)
    index_path = skills_dir / "INDEX.csv"
    new_text = render_index(rows)

    if args.check:
        # Read as bytes and normalize newlines so the freshness check is stable
        # across platforms (a Windows checkout may hold CRLF; the generated text
        # is LF) — the row *content*, not the line ending, is what must match.
        old = (
            index_path.read_bytes().decode("utf-8").replace("\r\n", "\n")
            if index_path.exists()
            else ""
        )
        if old != new_text:
            print(
                "gen_skills_index: STALE - {} does not match the SKILL.md files; "
                "run `python scripts/gen_skills_index.py`.".format(index_path),
                file=sys.stderr,
            )
            sys.exit(1)
        print("gen_skills_index: OK - {} skill(s), index fresh.".format(len(rows)))
        return

    # Write bytes so the file is LF on every platform (write_text would translate
    # to CRLF on Windows), keeping the committed index stable and diff-free.
    index_path.write_bytes(new_text.encode("utf-8"))
    print("gen_skills_index: wrote {} ({} skill(s)).".format(index_path, len(rows)))


if __name__ == "__main__":
    main()
