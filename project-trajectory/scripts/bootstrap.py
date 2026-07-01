#!/usr/bin/env python3
"""Scaffold a new project from this trajectory kit.

Copies the templates into a target repo's `docs/`, `scripts/`, and root, renaming
`*.template.*` to their working names and creating the directory layout the
process expects. Idempotent and safe: it never overwrites an existing file
unless you pass `--force`, so re-running to pick up kit updates won't clobber
your filled-in registries.

Run it from inside this kit folder (it locates the templates relative to itself):

    python scripts/bootstrap.py --dest /path/to/your/repo [--force] [--dry-run]

What it creates in the destination:
    AGENTS.md                                  <- AGENTS.template.md  (full agent guide)
    CLAUDE.md                                  <- CLAUDE.stub.template.md (points to AGENTS.md)
    GEMINI.md                                  <- GEMINI.stub.template.md (points to AGENTS.md)
    docs/process.md                            <- PROCESS.md
    docs/status.md                             <- STATUS.template.md
    docs/architecture.md                       <- ARCHITECTURE.template.md
    docs/interfaces.md                         <- INTERFACES.template.md
    docs/requirements/stakeholder-needs.md     <- registries/stakeholder-needs.template.md
    docs/requirements/system-requirements.csv  <- registries/system-requirements.template.csv
    docs/requirements/low-level-requirements.csv
    docs/requirements/interfaces.csv           <- registries/interfaces.template.csv
    docs/requirements/performance-budgets.csv  <- registries/performance-budgets.template.csv
    docs/test/test-cases.csv                   <- registries/test-cases.template.csv
    scripts/trace.py, check.py, check_flows.py, check_docs.py, check_perf.py,
    scripts/check_stubs.py, gen_arch_map.py, gen_release_checklist.py, gen_cases.py
    scripts/setup.{sh,ps1}, scripts/check.{sh,ps1}   (cross-platform launchers)
    scripts/onboard.{sh,command,cmd}           <- onboard.template.*  (Stage-0 onboarder)
    scripts/dev-setup.{sh,ps1}                 <- dev-setup.template.* (workstation setup)
    .githooks/pre-commit                       <- hooks/pre-commit  (opt-in process floor)
    pytest.ini                                 (test-tier markers)
    .gitignore                                 <- gitignore.template
    .github/workflows/check.yml                <- ci/check.yml
    src/, tests/                               (empty, with .gitkeep)

The agent guide lives once, in `AGENTS.md` (the cross-tool standard). `CLAUDE.md`
and `GEMINI.md` ship as thin stubs that point back at it, because Claude Code and
Gemini prefer their own filenames. All three are copied unconditionally — they're
tiny and cost nothing (same rationale as the interface artifacts), so every
scaffold works whichever agent shows up.

The interface artifacts (`docs/interfaces.md`, `docs/requirements/interfaces.csv`)
are always scaffolded but ship **inert**: they hold only `IF-000` placeholder
rows that nothing reads (`trace.py` doesn't process interfaces), so a standalone
project can simply ignore them. Fill them in only when this repo shares a
contract with another (process.md §8). They cost nothing to leave empty, which is
why bootstrap copies them unconditionally rather than gating them behind a flag.

`docs/requirements/performance-budgets.csv` (PB-###, process.md §9) is the same
kind of optional, always-scaffolded coordination registry for quantitative
perf/resource budgets. Its `PB-000` placeholder is inert (`trace.py` ignores
`-000` rows); a project with no resource concerns leaves it untouched. Once it
carries real rows, `trace.py` keeps their SR/LLR/Module back-links honest.

This scaffolds a **single-repo** project — the default and almost-always-right
rung of the scale ladder (process.md §10). The rare multi-repo **coordinator** rung
(`MULTI_REPO.md`) is intentionally **not** produced here: a coordinator repo drops
the `src/` build and instead carries a `modules.csv` (MOD-###), the interface
catalog, and an assembly definition. A `--coordinator` scaffold mode (and the
cross-repo tooling around it) is a documented concept deferred to the cross-repo
tooling track, not built into this script — so a project climbing to that rung adds
those pieces by hand, guided by `MULTI_REPO.md`.

It then runs `gen_arch_map.py` and `trace.py` once in the new repo so the
scaffold starts green — `check.py` would otherwise fail on the template
placeholder between the architecture markers.

After running: open AGENTS.md and docs/status.md, fill the PROJECT BRIEF, then
start gate G1 (see docs/process.md).
"""

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent  # the project-trajectory/ folder

# (source relative to KIT, destination relative to --dest)
MAPPING = [
    # Agent guide: full content in AGENTS.md, thin stubs for tools that prefer
    # their own filename. All three copied unconditionally (see module docstring).
    ("AGENTS.template.md", "AGENTS.md"),
    ("CLAUDE.stub.template.md", "CLAUDE.md"),
    ("GEMINI.stub.template.md", "GEMINI.md"),
    ("PROCESS.md", "docs/process.md"),
    ("STATUS.template.md", "docs/status.md"),
    ("ARCHITECTURE.template.md", "docs/architecture.md"),
    ("INTERFACES.template.md", "docs/interfaces.md"),
    (
        "registries/stakeholder-needs.template.md",
        "docs/requirements/stakeholder-needs.md",
    ),
    (
        "registries/system-requirements.template.csv",
        "docs/requirements/system-requirements.csv",
    ),
    (
        "registries/low-level-requirements.template.csv",
        "docs/requirements/low-level-requirements.csv",
    ),
    ("registries/interfaces.template.csv", "docs/requirements/interfaces.csv"),
    (
        "registries/performance-budgets.template.csv",
        "docs/requirements/performance-budgets.csv",
    ),
    ("registries/test-cases.template.csv", "docs/test/test-cases.csv"),
    ("scripts/trace.py", "scripts/trace.py"),
    ("scripts/check.py", "scripts/check.py"),
    ("scripts/check_flows.py", "scripts/check_flows.py"),
    ("scripts/check_docs.py", "scripts/check_docs.py"),
    ("scripts/check_perf.py", "scripts/check_perf.py"),
    ("scripts/check_stubs.py", "scripts/check_stubs.py"),
    ("scripts/gen_arch_map.py", "scripts/gen_arch_map.py"),
    ("scripts/gen_release_checklist.py", "scripts/gen_release_checklist.py"),
    ("scripts/gen_cases.py", "scripts/gen_cases.py"),
    ("scripts/setup.sh", "scripts/setup.sh"),
    ("scripts/setup.ps1", "scripts/setup.ps1"),
    ("scripts/check.sh", "scripts/check.sh"),
    ("scripts/check.ps1", "scripts/check.ps1"),
    # Onboarding-ladder helpers (Thread 15, process.md §7): a Stage-0 onboarder
    # (one readable entry point per platform) and the developer-workstation
    # dev-setup. Optional + consent-first; a project fills the onboarder's clone
    # URL and dev-setup's EDIT-FOR-YOUR-STACK block, and may serve the onboarder
    # as a Release asset.
    ("scripts/onboard.template.sh", "scripts/onboard.sh"),
    ("scripts/onboard.template.command", "scripts/onboard.command"),
    ("scripts/onboard.template.cmd", "scripts/onboard.cmd"),
    ("scripts/dev-setup.template.sh", "scripts/dev-setup.sh"),
    ("scripts/dev-setup.template.ps1", "scripts/dev-setup.ps1"),
    # Agent-neutral enforcement: one POSIX pre-commit hook (opt-in via
    # `git config core.hooksPath .githooks`, which setup.sh/ps1 set).
    ("hooks/pre-commit", ".githooks/pre-commit"),
    ("pytest.ini", "pytest.ini"),
    ("gitignore.template", ".gitignore"),
    ("ci/check.yml", ".github/workflows/check.yml"),
]

GITKEEP_DIRS = ["src", "tests"]


def initialize_generated_docs(dest):
    """Run the generators once so the fresh scaffold starts green: the arch-map
    placeholder would otherwise fail `gen_arch_map.py --check` (and so the
    harness) until the first manual run."""
    for rel_cmd in (
        ["scripts/gen_arch_map.py", "--src", "src", "--doc", "docs/architecture.md"],
        ["scripts/trace.py"],
    ):
        if not (dest / rel_cmd[0]).exists() or not (dest / "docs").exists():
            continue
        proc = subprocess.run([sys.executable] + rel_cmd, cwd=str(dest))
        if proc.returncode != 0:
            print(
                "WARNING: {} exited {}".format(rel_cmd[0], proc.returncode),
                file=sys.stderr,
            )


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--dest", required=True, help="target repo root")
    ap.add_argument(
        "--force",
        action="store_true",
        help="overwrite existing files (default: skip them)",
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="print what would happen; write nothing"
    )
    args = ap.parse_args()

    dest = Path(args.dest).resolve()
    if not dest.exists():
        if args.dry_run:
            print("would create destination directory:", dest)
        else:
            dest.mkdir(parents=True)

    created, skipped, missing = [], [], []
    for src_rel, dst_rel in MAPPING:
        src = KIT / src_rel
        dst = dest / dst_rel
        if not src.exists():
            missing.append(src_rel)
            continue
        if dst.exists() and not args.force:
            skipped.append(dst_rel)
            continue
        if args.dry_run:
            created.append(dst_rel)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        # Keep the .sh/.command launchers and the git hook executable on POSIX
        # (the hook has no extension; git and Finder only run these if the
        # executable bit is set — .command is macOS's double-clickable shell).
        if dst.suffix in (".sh", ".command") or dst.parent.name == ".githooks":
            dst.chmod(dst.stat().st_mode | 0o111)
        created.append(dst_rel)

    for d in GITKEEP_DIRS:
        keep = dest / d / ".gitkeep"
        if keep.exists():
            skipped.append("{}/.gitkeep".format(d))
        elif args.dry_run:
            created.append("{}/.gitkeep".format(d))
        else:
            keep.parent.mkdir(parents=True, exist_ok=True)
            keep.write_text("", encoding="utf-8")
            created.append("{}/.gitkeep".format(d))

    verb = "would create" if args.dry_run else "created"
    for c in created:
        print("  {}: {}".format(verb, c))
    for s in skipped:
        print("  skipped (exists): {}".format(s))
    for m in missing:
        print("  WARNING missing template: {}".format(m), file=sys.stderr)

    print(
        "\n{} file(s) {}, {} skipped.".format(
            len(created), "to create" if args.dry_run else "created", len(skipped)
        )
    )
    if not args.dry_run:
        initialize_generated_docs(dest)
    if not args.dry_run and created:
        print(
            "Next: fill the PROJECT BRIEF in AGENTS.md + docs/status.md, then "
            "run gate G1 (docs/process.md)."
        )
    if missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
