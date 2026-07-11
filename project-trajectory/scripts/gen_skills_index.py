#!/usr/bin/env python3
"""Generate the skills applicability index from the SKILL.md frontmatter.

Stack-agnostic kit, stdlib-only (Python 3.8+). The kit's `skills/` folder holds
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

Contracts: IF-019, IF-035 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import csv
import io
import re
import sys
from pathlib import Path

# Column order of the generated index. `scope` and the applicability axes come
# first so a scan can filter on them without reading `description`.
COLUMNS = ["name", "scope", "stacks", "domains", "phases", "tags", "description"]
LIST_FIELDS = ("stacks", "domains", "phases", "tags")


def _utf8_console():
    """Emit UTF-8 whatever the console codepage is (a non-ASCII description or
    path in a finding must not raise UnicodeEncodeError on a legacy Windows
    cp1252 console). Python 3.7+ streams expose `.reconfigure`; guard the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


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


def render_index(rows):
    """Render the rows as CSV text (LF-terminated, stable column order)."""
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    return buf.getvalue()


def main():
    _utf8_console()
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--skills", default="skills", help="skills dir (default: skills)")
    ap.add_argument(
        "--check",
        action="store_true",
        help="exit nonzero if INDEX.csv is stale (for CI/gates)",
    )
    args = ap.parse_args()

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
