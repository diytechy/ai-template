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
    docs/process.md                            <- PROCESS.md  (load-bearing core)
    docs/process-options.md                    <- PROCESS_OPTIONS.md  (opt-in layers)
    docs/gate                                  <- gate.template  (active gate: G1)
    docs/commit-identity                       <- commit-identity.template  (policy: inherit)
    docs/status.md                             <- STATUS.template.md
    docs/architecture.md                       <- ARCHITECTURE.template.md
    docs/interfaces.md                         <- INTERFACES.template.md
    docs/requirements/stakeholder-needs.md     <- registries/stakeholder-needs.template.md
    docs/requirements/system-requirements.csv  <- registries/system-requirements.template.csv
    docs/requirements/low-level-requirements.csv
    docs/requirements/interfaces.csv           <- registries/interfaces.template.csv
    docs/requirements/performance-budgets.csv  <- registries/performance-budgets.template.csv
    docs/requirements/procurement.csv          <- registries/procurement.template.csv
    docs/requirements/assets.csv               <- registries/assets.template.csv
    docs/test/test-cases.csv                   <- registries/test-cases.template.csv
    scripts/trace.py, check.py, check_flows.py, check_docs.py, check_perf.py,
    scripts/check_stubs.py, gen_arch_map.py, gen_release_checklist.py, gen_cases.py
    scripts/setup.{sh,ps1}, scripts/check.{sh,ps1}   (cross-platform launchers)
    scripts/onboard.{sh,command,cmd}           <- onboard.template.*  (Stage-0 onboarder)
    scripts/dev-setup.{sh,ps1}                 <- dev-setup.template.* (workstation setup)
    README.md                                  <- README.template.md (human front door; kept if one exists)
    run.{cmd,sh,command}                       <- run.template.*  (root product launchers)
    .githooks/pre-commit                       <- hooks/pre-commit  (opt-in process floor)
    pytest.ini                                 (test-tier markers)
    .gitignore                                 <- gitignore.template
    .gitattributes                             <- gitattributes.template (eol=lf hook pin)
    .github/workflows/check.yml                <- ci/check.yml
    src/, tests/                               (empty, with .gitkeep)

The agent guide lives once, in `AGENTS.md` (the cross-tool standard). `CLAUDE.md`
and `GEMINI.md` ship as thin stubs that point back at it, because Claude Code and
Gemini prefer their own filenames. All three are copied unconditionally — they're
tiny and cost nothing (same rationale as the interface artifacts), so every
scaffold works whichever agent shows up.

Agent selection (`--agents claude|gemini|both|none`, WI-1.9): at repo setup the
user most likely has an agent configured, so bootstrap can bring that agent's
**skills** (from the neutral `skills/` source) into the repo fold. The flag drives
what's *materialized* beyond the always-copied stubs: the matched skills into the
agent's native dir (`.claude/skills/<name>/SKILL.md`, `.gemini/skills/...`), the
agent's optional hook config copied **inert** as `settings.json.example` (never a
silently-installed Stop hook), and a setup note in `docs/status.md`. Run
interactively without the flag and it ASKS (agent, then up to two scope questions
— stack? domain? — that drive a trivial tag-intersection skill match). Run
non-interactively (CI) without the flag and it defaults to `none`: zero prompts,
nothing materialized, the historical agent-neutral scaffold unchanged. AGENTS.md
stays the canonical guide whatever the choice; skills are opt-in accelerators, not
process gates (skills/README.md).

The README and the root `run.{cmd,sh,command}` launchers (WI-1.12) are the
**evaluator's rungs** of the §7 onboarding ladder: the README is the human front
door (bootstrap fills `{{PROJECT_NAME}}` from the destination folder name; the
kickoff agent builds the rest out from the project brief; an existing README is
never overwritten), and the launchers give every launchable project a
double-clickable start per platform so running it never requires recalling a
command. They ship inert — an unfilled `RUN_CMD` prints guidance and exits
nonzero — and a pure library simply deletes them.

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

`docs/requirements/procurement.csv` (PART-###, process-options.md "purchased
parts") is the same kind of optional, always-scaffolded registry, for
purchased/external parts the project buys rather than builds. Each row's `IF-Ref`
names the interface row that is its owner-of-record (MULTI_REPO.md §3.3). Its
`PART-000` placeholder is inert; a project that buys nothing leaves it untouched.
`trace.py` integrity-checks the `PART-` ids (it does not resolve `IF-Ref`, which
points at the off-spine `IF-###` tier trace.py never reads). Full BOM tracking is
a deferred extension.

`docs/requirements/assets.csv` (ASSET-###, process-options.md "Binary assets")
is the same kind of optional, always-scaffolded registry, for unavoidably-binary
assets (art, music, voice, video) whose provenance/license/attribution/contract
and a pointer+hash are tracked in text even though the asset itself can't be
diffed. Its `ASSET-000` placeholder is inert; a project with no binary assets
leaves it untouched. `trace.py` integrity-checks the `ASSET-` ids only.

`docs/commit-identity` (process-options.md "Commit identity & anonymity")
declares whether this repo's commits are anonymous or identified: `inherit`
(the scaffolded default — no constraint) or an email glob the author identity
must match. `--commit-identity <pattern|inherit>` sets it at scaffold time —
identity belongs at repo creation, **before the first commit**, the only moment
it is free to fix; run interactively without the flag and bootstrap ASKS (the
same consent-first shape as --agents; non-interactive runs keep `inherit`).
Enforcement lives in scripts/setup.{sh,ps1} (applies a repo-local identity per
clone) and .githooks/pre-commit (blocks a mismatched commit).

This scaffolds a **single-repo** project — the default and almost-always-right
rung of the scale ladder (process.md §10). The rare multi-repo **coordinator** rung
(`MULTI_REPO.md`) is intentionally **not** produced here: a coordinator repo drops
the `src/` build and instead carries a `modules.csv` (MOD-###), the interface
catalog, and an assembly definition. A `--coordinator` scaffold mode (and the
cross-repo tooling around it) is a documented concept deferred to the cross-repo
tooling track, not built into this script — so a project climbing to that rung adds
those pieces by hand, guided by `MULTI_REPO.md`.

It also writes `docs/kit-version` — the kit commit the scaffold was produced
from (short SHA + ISO date, or `unknown` when the kit isn't a git checkout). That
stamp makes staleness *detectable*: a later "re-sync from kit HEAD" is a diff
between the recorded commit and HEAD, not a guess (ADOPTING.md "Re-syncing an
existing adoption"). **Sync only from a committed kit state**, never a dirty
working tree — bootstrap refuses to stamp a real SHA when the kit tree is dirty
(it writes `<sha>-dirty` and warns) so an adoption can't be pinned to an
unreproducible mid-edit state.

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

# --- Agent selection & the skills layer (WI-1.9) -----------------------------
# At repo setup the user most likely already has an agent configured, so the
# scaffold can materialize that agent's stub, its optional hook config, and the
# skills relevant to the project — without locking the kit to any agent (the
# `skills/` source stays neutral). See skills/README.md for the full contract.
AGENT_CHOICES = ("claude", "gemini", "both", "none")

# Per-agent native locations. Both Claude Code and Gemini CLI read the same
# Agent-Skills `SKILL.md` shape, so materializing a skill is a straight copy into
# the agent's skills dir; the optional hook config is copied *inert* (as a
# `settings.json.example`) so the scaffold never silently installs a Stop hook
# that runs commands — activation stays the user's explicit choice (the
# agent-hooks/README.md "not wired by bootstrap" stance).
AGENTS = {
    "claude": {
        "skills_dir": ".claude/skills",
        "hooks_src": "agent-hooks/claude.settings.json",
        "hooks_dst": ".claude/settings.json.example",
    },
    "gemini": {
        "skills_dir": ".gemini/skills",
        "hooks_src": "agent-hooks/gemini.settings.json",
        "hooks_dst": ".gemini/settings.json.example",
    },
}

# The closed applicability vocabularies used by the trivial scope matcher. `any`
# in a skill's list always matches; an answer of "" (skipped question) also
# matches everything (no filter on that axis).
STACK_CHOICES = ("python", "go", "rust", "powershell", "any")
DOMAIN_CHOICES = ("web", "game", "hardware", "data", "any")


def selected_agents(choice):
    """Expand an --agents choice into the concrete agent keys to materialize."""
    if choice == "both":
        return ["claude", "gemini"]
    if choice in ("claude", "gemini"):
        return [choice]
    return []  # "none"


def parse_skill_frontmatter(text):
    """Minimal frontmatter parse (name/scope + list fields) for a SKILL.md.

    Kept in sync with gen_skills_index.parse_frontmatter but inlined so bootstrap
    stays a single stdlib file. Returns a dict; list fields are Python lists."""
    import re

    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    fields = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        if value.startswith("[") and value.endswith("]"):
            fields[key] = [v.strip() for v in value[1:-1].split(",") if v.strip()]
        else:
            fields[key] = value
    return fields


def matches_scope(fm, stack, domain, binary_assets):
    """Trivial tag-intersection matcher: does a skill's applicability fit the
    declared project scope? `any` in the skill (or a skipped/"" answer) always
    matches. Deliberately dumb — the metadata convention is the deliverable, not
    an engine (skills/README.md)."""

    def axis_ok(skill_vals, answer):
        skill_vals = skill_vals or ["any"]
        if not answer or "any" in skill_vals:
            return True
        return answer in skill_vals

    if not axis_ok(fm.get("stacks"), stack):
        return False
    if not axis_ok(fm.get("domains"), domain):
        return False
    # A "binary assets / hardware involved?" yes only *adds* the hardware/game
    # domains to the match; it never filters a skill out, so leave it advisory.
    return True


def select_skills(stack, domain, binary_assets):
    """The kit-scope skills whose applicability intersects the declared scope.

    Only `scope: kit` skills are materialized downstream — `this-repo` skills
    maintain *this* template and are meaningless in an adopted product repo
    (skills/README.md "split rationale"). Returns a list of (name, SKILL.md path).
    When no scope was declared (all answers blank), every kit skill matches (the
    safe superset)."""
    chosen = []
    skills_dir = KIT / "skills"
    if not skills_dir.is_dir():
        return chosen
    for skill_md in sorted(skills_dir.glob("*/SKILL.md")):
        fm = parse_skill_frontmatter(skill_md.read_text(encoding="utf-8"))
        if (fm.get("scope") or "kit").strip() != "kit":
            continue
        if matches_scope(fm, stack, domain, binary_assets):
            chosen.append((skill_md.parent.name, skill_md))
    return chosen


def materialize_agent_layer(dest, agents, skills, dry_run, force):
    """Copy the selected skills (and the inert hook example) into each chosen
    agent's native location. Returns a list of created dest-relative paths."""
    created = []
    for agent in agents:
        spec = AGENTS[agent]
        for name, src in skills:
            dst_rel = "{}/{}/SKILL.md".format(spec["skills_dir"], name)
            dst = dest / dst_rel
            if dst.exists() and not force:
                continue
            if not dry_run:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dst)
            created.append(dst_rel)
        hooks_src = KIT / spec["hooks_src"]
        if hooks_src.exists():
            hooks_dst = dest / spec["hooks_dst"]
            if not hooks_dst.exists() or force:
                if not dry_run:
                    hooks_dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(hooks_src, hooks_dst)
                created.append(spec["hooks_dst"])
    return created


def record_agent_choice(dest, choice, skills, dry_run):
    """Append a one-line setup note to docs/status.md recording the agent choice
    + date + materialized skills, so the scaffolded repo carries the decision
    (idempotent: skipped if a note already exists)."""
    import datetime

    # "none" is the historical, agent-neutral default — it materializes nothing,
    # so it records nothing either: the scaffold stays byte-for-byte unchanged.
    if choice == "none":
        return False
    status = dest / "docs" / "status.md"
    if not status.exists() or dry_run:
        return False
    text = status.read_text(encoding="utf-8")
    marker = "<!-- agent-setup -->"
    if marker in text:
        return False
    names = ", ".join(n for n, _ in skills) if skills else "none"
    note = (
        "\n{} Agent setup ({}): agents=`{}`; skills materialized: {}. "
        "AGENTS.md remains the canonical, agent-neutral guide "
        "(skills are opt-in accelerators, not a process gate).\n".format(
            marker, datetime.date.today().isoformat(), choice, names
        )
    )
    status.write_text(text + note, encoding="utf-8")
    return True


def prompt_choice(prompt, choices, default):
    """Ask on a TTY; return `default` immediately when stdin isn't interactive
    (CI-safe: a non-interactive run never blocks and never prompts)."""
    if not sys.stdin.isatty():
        return default
    labels = "/".join(choices)
    try:
        ans = (
            input("{} [{}] (default {}): ".format(prompt, labels, default))
            .strip()
            .lower()
        )
    except EOFError:
        return default
    return ans if ans in choices else default


def prompt_text(prompt, default):
    """Free-text prompt on a TTY; `default` when stdin isn't interactive
    (same CI-safe contract as prompt_choice, for open-ended answers)."""
    if not sys.stdin.isatty():
        return default
    try:
        ans = input("{} (default {}): ".format(prompt, default)).strip()
    except EOFError:
        return default
    return ans or default


def apply_commit_identity(dest, policy, dry_run):
    """Write a declared (non-`inherit`) policy into docs/commit-identity,
    keeping the template's explanatory header. Identity belongs at repo
    creation, before the first commit — the only moment it is free to fix —
    so an explicitly passed/answered policy overwrites the scaffolded default."""
    if dry_run:
        return
    header = [
        ln
        for ln in (KIT / "commit-identity.template")
        .read_text(encoding="utf-8")
        .splitlines()
        if ln.startswith("#")
    ]
    target = dest / "docs" / "commit-identity"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(header + [policy]) + "\n", encoding="utf-8")


def _utf8_console():
    """Emit UTF-8 to stdout/stderr whatever the OS console codepage is, so the
    non-ASCII characters in the created-file list / dirty-tree WARNING can't
    raise UnicodeEncodeError on a legacy Windows cp1252 console. Python 3.7+
    streams expose `.reconfigure`; guard for the rest."""
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


# (source relative to KIT, destination relative to --dest)
MAPPING = [
    # Agent guide: full content in AGENTS.md, thin stubs for tools that prefer
    # their own filename. All three copied unconditionally (see module docstring).
    ("AGENTS.template.md", "AGENTS.md"),
    ("CLAUDE.stub.template.md", "CLAUDE.md"),
    ("GEMINI.stub.template.md", "GEMINI.md"),
    ("PROCESS.md", "docs/process.md"),
    ("PROCESS_OPTIONS.md", "docs/process-options.md"),
    # The machine-readable active gate (one line: G1|G2|G3|all). check.py and CI
    # read it, so a young project's CI enforces the bar it is actually at;
    # closing a gate = the human bumps this file in a reviewed commit.
    ("gate.template", "docs/gate"),
    # The declared commit-identity policy (Thread 38, process-options.md "Commit
    # identity & anonymity"): `inherit` by default; --commit-identity overrides.
    ("commit-identity.template", "docs/commit-identity"),
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
    (
        "registries/procurement.template.csv",
        "docs/requirements/procurement.csv",
    ),
    (
        "registries/assets.template.csv",
        "docs/requirements/assets.csv",
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
    # The evaluator's rungs (WI-1.12): a README skeleton the kickoff agent
    # builds out from the project brief (never overwritten — an adopted repo
    # keeps its own README), and root double-clickable product launchers, one
    # per platform, so running the product never requires recalling a command.
    # They ship inert (empty RUN_CMD prints guidance); a pure library deletes
    # them. Root, not scripts/: the double-click use case is "open the checkout
    # folder and click" — one hop shallower matters for a non-code evaluator.
    ("README.template.md", "README.md"),
    ("scripts/run.template.cmd", "run.cmd"),
    ("scripts/run.template.sh", "run.sh"),
    ("scripts/run.template.command", "run.command"),
    # Agent-neutral enforcement: one POSIX pre-commit hook (opt-in via
    # `git config core.hooksPath .githooks`, which setup.sh/ps1 set).
    ("hooks/pre-commit", ".githooks/pre-commit"),
    ("pytest.ini", "pytest.ini"),
    ("gitignore.template", ".gitignore"),
    # eol=lf pin for the sh-based git hook (a CRLF shebang breaks it under
    # Windows autocrlf). Skipped if the repo already has a .gitattributes —
    # merge the .githooks/pre-commit rule in by hand (ADOPTING.md §1).
    ("gitattributes.template", ".gitattributes"),
    ("ci/check.yml", ".github/workflows/check.yml"),
]

GITKEEP_DIRS = ["src", "tests"]

# Per-destination text fixups applied right after a template is copied: strip the
# "this is a template, copy me" meta-prose that reads wrong once the file *is* the
# scaffolded doc. Keyed by destination rel-path; each entry is (old, new). Kept to
# exact, unique strings so a missed match is a no-op, never a wrong edit.
TEMPLATE_REWRITES = {
    "docs/process.md": [
        ("# Development Process (template)", "# Development Process"),
        (
            "Canonical method for a gated, requirement-traced project. Copy this "
            "into a new\nrepo as `docs/process.md`. It is **stack-agnostic**",
            "Canonical method for a gated, requirement-traced project. It is "
            "**stack-agnostic**",
        ),
    ],
}


def apply_template_rewrites(dst_rel, dst):
    """Strip copy-me meta-prose from a freshly written scaffold file (see
    TEMPLATE_REWRITES). Returns the count of substitutions applied."""
    edits = TEMPLATE_REWRITES.get(dst_rel)
    if not edits:
        return 0
    text = dst.read_text(encoding="utf-8")
    applied = 0
    for old, new in edits:
        if old in text:
            text = text.replace(old, new, 1)
            applied += 1
    if applied:
        dst.write_text(text, encoding="utf-8")
    return applied


def initialize_generated_docs(dest, created):
    """Run the generators once so the fresh scaffold starts green: the arch-map
    placeholder would otherwise fail `gen_arch_map.py --check` (and so the
    harness) until the first manual run.

    Gated on this run having *created* docs/architecture.md: a re-sync against
    an adopted repo must never regenerate an artifact another generator owns —
    a PowerShell repo's map is written by the gen_arch_map .ps1 port, and
    running the Python generator over it clobbers the generated block (the
    FileBackup re-sync hit exactly this)."""
    if "docs/architecture.md" not in created:
        return
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


def kit_version():
    """The kit's committed identity for the version stamp: (label, dirty).

    `label` is `<short-sha> <ISO-date>` from the kit's git checkout, or
    `"unknown (kit not a git checkout)"` when git or the kit's history isn't
    available (a tarball copy). `dirty` is True when the kit working tree has
    uncommitted changes — the caller warns, because an adoption pinned to a
    dirty tree can't be reproduced or diffed against later (see module docstring
    / ADOPTING.md 're-sync only from a committed kit state')."""
    try:
        sha = subprocess.run(
            ["git", "-C", str(KIT), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
        )
        if sha.returncode != 0 or not sha.stdout.strip():
            return "unknown (kit not a git checkout)", False
        short = sha.stdout.strip()
        date = subprocess.run(
            ["git", "-C", str(KIT), "show", "-s", "--format=%cs", "HEAD"],
            capture_output=True,
            text=True,
        )
        # Dirty = any staged/unstaged change anywhere in the kit checkout. We
        # stamp a real SHA either way (so the scaffold is never blocked), but
        # mark it `-dirty` and warn: the honest signal is "unreproducible".
        status = subprocess.run(
            ["git", "-C", str(KIT), "status", "--porcelain"],
            capture_output=True,
            text=True,
        )
        dirty = bool(status.stdout.strip())
        label = "{}{} {}".format(
            short, "-dirty" if dirty else "", date.stdout.strip()
        ).strip()
        return label, dirty
    except (OSError, ValueError):
        return "unknown (kit not a git checkout)", False


def write_kit_version(dest, dry_run):
    """Stamp docs/kit-version with the kit commit the scaffold came from, so a
    later re-sync is diffable against kit HEAD. Returns (label, dirty, wrote)."""
    label, dirty = kit_version()
    body = (
        "# Kit version stamp — the project-trajectory kit commit this repo was\n"
        "# scaffolded/re-synced from. Bump it when you re-sync from a *committed*\n"
        "# kit state (never a dirty tree); the delta to kit HEAD is your re-sync\n"
        "# diff. See ADOPTING.md 'Re-syncing an existing adoption'.\n"
        "{}\n".format(label)
    )
    target = dest / "docs" / "kit-version"
    if dry_run:
        return label, dirty, False
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")
    return label, dirty, True


def main():
    _utf8_console()
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
    ap.add_argument(
        "--agents",
        choices=AGENT_CHOICES,
        default=None,
        help="which agent to set up (materialize its skills + inert hook example): "
        "claude|gemini|both|none. Omitted + interactive TTY -> ASK; omitted + "
        "non-interactive -> 'none' (CI-safe: preserves the agent-neutral default, "
        "zero prompts, no skills materialized).",
    )
    ap.add_argument(
        "--stack",
        choices=STACK_CHOICES,
        default=None,
        help="declared primary stack, for skill matching (python|go|rust|"
        "powershell|any). Omitted + interactive -> ASK; non-interactive -> no "
        "filter (all kit skills match).",
    )
    ap.add_argument(
        "--domain",
        choices=DOMAIN_CHOICES,
        default=None,
        help="declared primary domain, for skill matching (web|game|hardware|"
        "data|any). Omitted + interactive -> ASK; non-interactive -> no filter.",
    )
    ap.add_argument(
        "--commit-identity",
        default=None,
        metavar="PATTERN",
        help="commit-identity policy for docs/commit-identity: 'inherit' (no "
        "constraint) or an email glob the author identity must match, e.g. "
        "'*@users.noreply.github.com' for an anonymous repo. Omitted + "
        "interactive TTY -> ASK; non-interactive -> 'inherit'. Set it at repo "
        'creation, before the first commit (process-options.md "Commit '
        'identity & anonymity").',
    )
    args = ap.parse_args()

    # Resolve the agent choice: explicit flag wins; else ASK on an interactive
    # TTY; else default to "none" — which materializes no skills/hooks and so
    # preserves the historical (agent-neutral) scaffold exactly (CI-safe).
    agent_choice = (
        args.agents
        if args.agents is not None
        else prompt_choice(
            "Preferred agent to set up for this repo?", AGENT_CHOICES, "none"
        )
    )
    agents = selected_agents(agent_choice)
    # Only ask the (up to) two scope questions when an agent was chosen and the
    # answers weren't passed as flags — they only drive skill matching. A
    # non-interactive run never prompts (prompt_choice returns the default).
    stack = args.stack
    domain = args.domain
    if agents:
        if stack is None:
            stack = prompt_choice("Primary stack?", STACK_CHOICES, "any")
        if domain is None:
            domain = prompt_choice("Primary domain?", DOMAIN_CHOICES, "any")
        binary_assets = (
            prompt_choice("Binary assets or hardware involved?", ("yes", "no"), "no")
            == "yes"
        )
        skills = select_skills(stack, domain, binary_assets)
    else:
        skills = []

    # Resolve the commit-identity policy the same consent-first way: explicit
    # flag wins; else ASK on an interactive TTY; else 'inherit' (CI-safe — the
    # scaffolded default file already says inherit, so nothing extra happens).
    identity = (
        args.commit_identity
        if args.commit_identity is not None
        else prompt_text(
            "Commit-identity policy? ('inherit' = no constraint, or an email "
            "glob like *@users.noreply.github.com for an anonymous repo)",
            "inherit",
        )
    )

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
        # Strip copy-me template meta-prose (e.g. process.md's "(template)" title
        # and "Copy this into a new repo as docs/process.md") now that the file
        # *is* the scaffolded doc.
        apply_template_rewrites(dst_rel, dst)
        # The README skeleton carries the one dynamic placeholder: the project's
        # name, taken from the destination folder (the kickoff agent fills in
        # the rest from the project brief).
        if dst_rel == "README.md":
            text = dst.read_text(encoding="utf-8")
            dst.write_text(
                text.replace("{{PROJECT_NAME}}", dest.name), encoding="utf-8"
            )
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

    # Materialize the chosen agent's layer: its matched skills into the native
    # skills dir + the inert hook example. "none" (the non-interactive default)
    # adds nothing, so the historical scaffold is byte-for-byte unchanged.
    created.extend(
        materialize_agent_layer(dest, agents, skills, args.dry_run, args.force)
    )

    # A declared (non-inherit) identity policy overwrites the scaffolded
    # default — this is the one moment identity is free to fix (pre-commit).
    if identity and identity != "inherit":
        apply_commit_identity(dest, identity, args.dry_run)
        if "docs/commit-identity" not in created:
            created.append("docs/commit-identity")
        print("  commit-identity policy: {}".format(identity))

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

    # docs/kit-version is a generated stamp, not user content, so it is always
    # (re)written — unlike the copied templates it is meant to be refreshed on
    # every scaffold/re-sync to record the kit state this run came from.
    label, dirty, wrote = write_kit_version(dest, args.dry_run)
    print("  {}: docs/kit-version ({})".format(verb, label))
    if dirty:
        print(
            "WARNING: the kit working tree is DIRTY — this scaffold is stamped "
            "{} and cannot be reproduced or cleanly diffed later. Re-sync only "
            "from a committed kit state (commit the kit, then re-run).".format(label),
            file=sys.stderr,
        )

    # Record the agent choice + date + materialized skills in docs/status.md so
    # the scaffolded repo carries the setup decision (AGENTS.md stays canonical).
    if record_agent_choice(dest, agent_choice, skills, args.dry_run):
        print("  {}: docs/status.md agent-setup note ({})".format(verb, agent_choice))

    if not args.dry_run:
        initialize_generated_docs(dest, created)
    if not args.dry_run and created:
        print(
            "Next: fill the PROJECT BRIEF in AGENTS.md + docs/status.md, then "
            "run gate G1 (docs/process.md)."
        )
    if missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
