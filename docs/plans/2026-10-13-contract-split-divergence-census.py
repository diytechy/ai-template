#!/usr/bin/env python3
"""Census of what `contract_split` holds that this branch never received.

Read-only: it reads three revisions through `git show` / `git rev-list` and
writes nothing. It produces the figures in the sibling report
`2026-10-13-contract-split-divergence.md`. Like the other measuring scripts in
docs/plans/, it sits outside project-trajectory/scripts/ and tests/, so no gate
runs it.

    python docs/plans/2026-10-13-contract-split-divergence-census.py \
        [--base 607cf609] [--lost contract_split] [--here HEAD]
"""

from __future__ import annotations

import argparse
import subprocess
import tomllib

SPINE = (
    "docs/requirements/stakeholder-needs.toml",
    "docs/requirements/system-requirements.toml",
    "docs/requirements/low-level-requirements.toml",
    "docs/requirements/interfaces.toml",
    "docs/requirements/open-items.toml",
    "docs/test/test-cases.toml",
)


def git(*args: str) -> str:
    return subprocess.run(
        ("git", *args), check=True, capture_output=True, text=True
    ).stdout


def rows(rev: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in SPINE:
        for table in tomllib.loads(git("show", f"{rev}:{path}")).values():
            if isinstance(table, dict):
                out.update((k, v) for k, v in table.items() if isinstance(v, dict))
    return out


def sort_key(row_id: str) -> tuple[str, int]:
    prefix, _, num = row_id.partition("-")
    return prefix, int(num)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="607cf609")
    ap.add_argument("--lost", default="contract_split")
    ap.add_argument("--here", default="HEAD")
    a = ap.parse_args()

    lost_commits = git("rev-list", f"{a.here}..{a.lost}").split()
    cherry = git("cherry", a.here, a.lost).split("\n")
    print(f"commits on {a.lost} not on {a.here}: {len(lost_commits)}")
    print(
        f"of those, patch-equivalent on {a.here}: "
        f"{sum(1 for line in cherry if line.startswith('-'))}"
    )
    print(git("diff", "--shortstat", a.base, a.lost).strip())

    print("\n## files added on the lost side and absent here (lines)")
    added = git(
        "diff",
        "--name-only",
        "--diff-filter=A",
        a.base,
        a.lost,
        "--",
        "project-trajectory",
        "tests",
    ).split()
    for path in added:
        if subprocess.run(
            ("git", "cat-file", "-e", f"{a.here}:{path}"), capture_output=True
        ).returncode:
            print(f"{git('show', f'{a.lost}:{path}').count(chr(10)):6} {path}")

    base, lost, here = rows(a.base), rows(a.lost), rows(a.here)
    print("\n## spine rows minted on the lost side")
    for k in sorted(set(lost) - set(base), key=sort_key):
        clash = "same id, different row" if k in here else "absent"
        print(f"{k}: {lost[k].get('title', '')[:90]} | here: {clash}")
    print(f"rows removed on the lost side: {len(set(base) - set(lost))}")

    print("\n## rows amended on the lost side (field: state here)")
    for k in sorted(set(base) & set(lost), key=sort_key):
        changed = sorted(
            f for f in set(base[k]) | set(lost[k]) if base[k].get(f) != lost[k].get(f)
        )
        if not changed or k.startswith("OI-"):
            continue
        cells = []
        for f in changed:
            mine = here.get(k, {}).get(f)
            state = (
                "already matches"
                if mine == lost[k].get(f)
                else "unchanged here"
                if mine == base[k].get(f)
                else "rewritten here"
            )
            cells.append(f"`{f}` {state}")
        print(f"| {k} | {base[k].get('status')} | {'; '.join(cells)} |")


if __name__ == "__main__":
    main()
