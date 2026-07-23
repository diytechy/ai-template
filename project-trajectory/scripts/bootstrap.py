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
    docs/gate-policy                           <- gate-policy.template  (authority: attended)
    docs/privacy-check                         <- privacy-check.template  (privacy: off)
    docs/push-policy                           <- push-policy.template  (policy: human)
    docs/blackout                              <- blackout.template  (window: 12:00-19:00 UTC)
    docs/review-policy                         <- review-policy.template  (reviewers: 1)
    docs/status.md                             <- STATUS.template.md  (working surface)
    docs/log.md                                <- LOG.template.md  (append-only history)
    docs/plan.md                               <- PLAN.template.md  (plan/build session blocks)
    docs/architecture.md                       <- ARCHITECTURE.template.md
    docs/interfaces.md                         <- INTERFACES.template.md
    docs/requirements/stakeholder-needs.md     <- registries/stakeholder-needs.template.md
    docs/requirements/system-requirements.csv  <- registries/system-requirements.template.csv
    docs/requirements/low-level-requirements.csv
    docs/requirements/interfaces.csv           <- registries/interfaces.template.csv
    docs/requirements/performance-budgets.csv  <- registries/performance-budgets.template.csv
    docs/requirements/procurement.csv          <- registries/procurement.template.csv
    docs/requirements/assets.csv               <- registries/assets.template.csv
    docs/requirements/components.csv           <- registries/components.template.csv
    docs/requirements/work-items.csv           <- registries/work-items.template.csv
    docs/specs/README.md, docs/specs/WI-000.md <- specs/*.template.md  (spec-of-record dir)
    docs/knowledge/README.md                  <- knowledge/README.template.md
    docs/rubrics/README.md, docs/rubrics/rubric-000.md <- rubrics/*.template.md  (critique rubrics)
    docs/test/test-cases.csv                   <- registries/test-cases.template.csv
    scripts/trace.py, derive_gate.py, check.py, check_flows.py, check_docs.py, check_perf.py,
    scripts/check_stubs.py, check_dupes.py, check_coverage.py, check_doc_refs.py, check_privacy.py, check_vendored.py, check_trajectory.py,
    scripts/subagent_gate.py, gen_arch_map.py, gen_release_checklist.py, gen_cases.py, gen_trajectory.py, gen_okf.py
    scripts/plan_coverage.py, plan_round.py, plan_briefs.py, plan_coverage_step.py, plan_artifacts.py
                                               (the dual-plan round set, process-options.md "Dual-plan decomposition")
    scripts/agent_route.py, scripts/score_reviews.py   (S8 coordinator routing + review scorer)
    docs/agents.csv                            <- agents.template.csv (model registry; inert until docs/agents-enabled)
    scripts/setup.{sh,ps1}, scripts/check.{sh,ps1}   (cross-platform launchers)
    scripts/onboard.{sh,command,cmd}           <- onboard.template.*  (Stage-0 onboarder)
    scripts/dev-setup.{sh,ps1,command,cmd}     <- dev-setup.template.* (workstation setup)
    README.md                                  <- README.template.md (human front door; kept if one exists)
    OWNER_SCRATCHPAD.md                        <- OWNER_SCRATCHPAD.template.md (owner-only notes; agents ignore)
    scripts/run_menu.py                        (capability-menu reader the run.* launchers delegate to)
    run.{cmd,sh,command}                       <- run.template.*  (root product launchers)
    agent-resume.{cmd,sh,command}              <- agent-resume.template.*  (root agent launchers)
    scripts/agent_loop.py                      (unattended coordinator engine; entry point)
    scripts/agent_session.py, agent_common.py, plan_runner.py, agent_dispatch.py
                                               (the WI-218 split: session launch / shared primitives / dual-plan runner / dispatcher+integrator)
    .githooks/pre-commit                       <- hooks/pre-commit  (opt-in process floor)
    .githooks/commit-msg                       <- hooks/commit-msg  (commit-message privacy scan)
    .githooks/pre-push                         <- hooks/pre-push  (privacy-review backstop)
    docs/stack.ini                             <- stack.ini.template  (declared product toolchain)
    pytest.ini                                 (test-tier markers; skipped when
                                                --stack is explicitly non-Python)
    docs/kit-profile                           (generated stamp: stack + omitted axes)
    .gitignore                                 <- gitignore.template
    .gitattributes                             <- gitattributes.template (eol=lf hook pin)
    .github/workflows/check.yml                <- ci/check.yml
    src/, tests/                               (empty, with .gitkeep)

The agent guide lives once, in `AGENTS.md` (the cross-tool standard). `CLAUDE.md`
and `GEMINI.md` ship as thin stubs that point back at it, because Claude Code and
Gemini prefer their own filenames. All three are copied unconditionally — they're
tiny and cost nothing (same rationale as the interface artifacts), so every
scaffold works whichever agent shows up.

Agent selection (`--agents claude|gemini|codex|both|none`, WI-1.9 + S7): at repo
setup the user most likely has an agent configured, so bootstrap can bring that
agent's **skills** (from the neutral `skills/` source) into the repo fold. The
flag drives what's *materialized* beyond the always-copied stubs: the matched
skills into the agent's native dir (`.claude/skills/<name>/SKILL.md`,
`.gemini/skills/...`, `.agents/skills/...` for codex), the
agent's optional hook config copied **inert** as `settings.json.example` (never a
silently-installed Stop hook), and a setup note in `docs/status.md`. Run
interactively without the flag and it ASKS (agent, then up to two scope questions
— stack? domain? — that drive a trivial tag-intersection skill match). Run
non-interactively (CI) without the flag and it defaults to `none`: zero prompts,
nothing materialized, the historical agent-neutral scaffold unchanged. AGENTS.md
stays the canonical guide whatever the choice; skills are opt-in accelerators, not
process gates (skills/README.md).

The per-agent skill copies are a **checked fan-out of the one neutral source**
(S7): materialization is write-once (never clobbers project content), and
`--sync` is the deliberate refresh that force-overwrites each existing per-agent
skills subtree from `skills/` so "edit source → re-materialize" is one command.
`gen_skills_index.py --check-agents` is the drift gate (byte-identity of every
per-agent copy to source), wired into the pre-commit floor + G3 like the arch-map
/ OKF freshness steps and vacuous when a repo has no per-agent skills dir.

The README and the root `run.{cmd,sh,command}` launchers (WI-1.12) are the
**evaluator's rungs** of the §7 onboarding ladder: the README is the human front
door (bootstrap fills `{{PROJECT_NAME}}` from the destination folder name; the
kickoff agent builds the rest out from the project brief; an existing README is
never overwritten), and the launchers give every launchable project a
double-clickable start per platform so running it never requires recalling a
command — presenting the capabilities declared in `docs/stack.ini`'s `[run]`
section (via `scripts/run_menu.py`), so the launch commands live once. They ship
inert — an absent/empty `[run]` section prints guidance and exits nonzero — and
a pure library simply deletes them.

The root `agent-resume.{cmd,sh,command}` launchers + `scripts/agent_loop.py`
(Thread 33, process-options.md "Unattended operation") are the *work-resume*
counterpart of the evaluator's rungs: one double-clickable entry that boots the
right agent session at the right tier under the declared gate policy — or the
walk-away coordinator loop. Like `run.*` they ship **inert** (an unfilled
`AGENT_CMD` prints guidance and exits nonzero) and a repo without agent-driven
work deletes them. When `--agents` picked an agent, bootstrap **seeds** the
launcher's `AGENT_CMD`/`AGENT_MODEL` slots with that agent's example command
(including its permission-bypass flag — the launchers and the loop banner state
the consent plainly); the slots stay an EDIT block the repo owns.

The interface artifacts (`docs/interfaces.md`, `docs/requirements/interfaces.csv`)
are always scaffolded but ship **inert**: they hold only the `IF-000` placeholder
row (ignored, like every `-000`), so a single-module project can simply leave
them empty. Fill in `IF-###` rows when this repo declares a contract — with
another repo **or between its own modules** (process.md §8). `trace.py`
integrity-checks the seam registry (id shape, SR-Refs back-link, WI-056) and
`check_trajectory.py` runs the **architecture-connectivity coverage** over the
arch-map inventory. That coverage is **opt-out, default-on** (the
`docs/secrets-scan` / `docs/trajectory-check` posture — absence reads on): a
multi-module arch-map with no declared seams warns "connectivity undeclared"
rather than passing vacuously, so like those layers there is no file to scaffold —
silence it with the one word `off` in `docs/interfaces-check`, or a single-module
inventory. They cost nothing to leave empty, which is why bootstrap copies them
unconditionally rather than gating them behind a flag.

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

`docs/requirements/work-items.csv` (WI-###, process-options.md "Trajectory /
work-items layer") is the machine-readable execution registry that complements
the SN->SR->LLR->TC spine: each row is a work item decomposing *how* work runs —
it delivers SR(s), sits on a track, and depends on predecessor WIs (the DAG
edges), moving `queued->active->done`. `scripts/check_trajectory.py` validates it
(id integrity, resolvable predecessors, an acyclic graph, SR refs that exist)
as the `trajectory` gate step from G2 on. Like the always-on secrets floor it is
OPT-OUT and vacuous by default: the shipped inert `WI-000` placeholder makes a
fresh scaffold pass for free, and a repo that never wants the layer sets
`docs/trajectory-check: off`. It is off-spine (like procurement / assets);
`trace.py` does not read WI ids — `check_trajectory.py` owns them.
`scripts/gen_trajectory.py` renders the registry + spine into a self-contained,
fully-offline root `PROJECT_STATE.html` dashboard — an SVG icicle of the spine and a
plain-SVG layered DAG of the work items, no CDN; its `--check` is the
`trajectory-map` freshness gate at G3 (regenerate + byte-compare, like `arch-map`).
Both are generated *views*, never a source of truth.

`docs/privacy-check` (process-options.md "Commit identity & privacy") toggles
the privacy gate: `false` (the scaffolded default — off) or `true` to scan the
commit author email and committed content for PII / identity leaks. Identity
(which account authors) is the user's own git config, not pinned here; the gate
defends *privacy*. `--privacy-check <true|false>` sets it at scaffold time; run
interactively without the flag and bootstrap ASKS (the same consent-first shape
as --agents; non-interactive runs keep `false`). The always-on secrets floor
(docs/secrets-scan) runs regardless. Enforcement lives in .githooks/pre-commit
(author + staged content), .githooks/commit-msg (the message), and
.githooks/pre-push (the outgoing range + LLM review).

`docs/push-policy` (process-options.md "Agent iteration branch & sync")
declares who may publish (`git push`): `human` (the scaffolded default — an
agent never pushes, even if asked mid-session; it prepares the branch and
requests), `agent-iteration` (only the scrubbed llm/<branch> iteration
branch), or `agent` (the development branch after a landed sync).
`--push-policy` sets it at scaffold time; run interactively without the flag
and bootstrap ASKS (the same consent-first shape as --gate-policy;
non-interactive runs keep `human`). It is a process rule honored by agent
drivers and coordinators, not a hook guarantee — hooks are per-clone and can
only assist, which is why the authority is declared rather than enforced at
push time.

`docs/stack.ini` (Thread 30, process.md §7) declares the product toolchain
**once** — the format/lint/test commands, the `src`/`tests` paths, the test-tier
expressions, and the coverage threshold. `scripts/check.py` reads it; CI, the
pre-commit hook, and `scripts/setup.*` delegate to it instead of each restating
a command, so a stack swap edits one file. It is scaffolded unconditionally with
the Python-reference values (identical to check.py's built-in fallback, so a
fresh scaffold's behavior is unchanged); a non-Python scaffold's rewiring
checklist points here. Deleting the file falls back to the built-ins.

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

**Conditional scaffold generation (Thread 34).** The Markdown templates are
masters holding *all* permutations; bootstrap *generates* each repo's copy by
stripping `<!-- kit-only -->` regions (the "copy me" meta-prose no scaffold
keeps) and keeping or stubbing `<!-- profile: axis -->` regions per the
resolved profile (`--stack`, `--omit`; see PROFILE_AXES). Omission never
renumbers: § headings stay outside the markers, an omitted section keeps its
heading plus a one-line resolvable stub, so a finding citing §9 means the same
thing in every adopted repo. The resolved profile is recorded in
`docs/kit-profile` (beside the kit-version stamp) and a re-sync **regenerates
from that record** — re-running bootstrap without `--stack`/`--omit` re-reads
it, so an upgrade never silently reverts a structural choice (ADOPTING.md §6).
An explicitly non-Python `--stack` (node|go|rust|powershell) also skips
`pytest.ini`, seeds the fresh docs/stack.ini's `[arch-map] mode = files`
(the stack-neutral map — a Python-AST scan would pass vacuously), and
appends the harness-rewiring checklist to the fresh status.md's Open items,
so the remaining hand-edits are visible work items.

It then runs `gen_arch_map.py` and `trace.py` once in the new repo so the
scaffold starts green — `check.py` would otherwise fail on the template
placeholder between the architecture markers.

After running: open AGENTS.md and docs/status.md, fill the PROJECT BRIEF, then
start gate G1 (see docs/process.md).

Contracts: IF-014, IF-039 — the interface seams this module declares (process.md §8; rows of record in docs/requirements/interfaces.csv).
"""

import argparse
import configparser
import re
import shutil
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parent.parent  # the project-trajectory/ folder


def _write_text_lf(path, text):
    """Write scaffold text with LF endings on every platform.

    `Path.write_text` translates "\\n" to os.linesep, so a Windows bootstrap
    would emit CRLF scaffolds — including the seeded `agent-resume.sh`, whose
    CRLF shebang breaks `#!/bin/sh` (the exact trap gitattributes.template
    documents). Same explicit-newline pattern the other generators use
    (gen_arch_map/gen_okf); stays 3.9-runnable. Every scaffold/policy TEXT write routes
    through here; the `.py` copy branch stays write_bytes (byte-for-byte)."""
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# --- Agent selection & the skills layer (WI-1.9) -----------------------------
# At repo setup the user most likely already has an agent configured, so the
# scaffold can materialize that agent's stub, its optional hook config, and the
# skills relevant to the project — without locking the kit to any agent (the
# `skills/` source stays neutral). See skills/README.md for the full contract.
AGENT_CHOICES = ("claude", "gemini", "codex", "both", "none")

# Per-agent native skill locations. Claude Code, Gemini CLI, and Codex all read
# the same Agent-Skills `SKILL.md` shape (Codex mirrors the AGENTS.md convention
# under `.agents/`), so materializing a skill is a straight copy into the agent's
# skills dir — the locations differ only because agent skill *dirs* don't
# standardize (S7). The optional hook config is copied *inert* (as a
# `settings.json.example`) so the scaffold never silently installs a Stop hook
# that runs commands — activation stays the user's explicit choice (the
# agent-hooks/README.md "not wired by bootstrap" stance). `hooks_src`/`hooks_dst`
# are OPTIONAL: an agent with no shipped hook config (codex today) just gets its
# skills fanned out.
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
    "codex": {
        "skills_dir": ".agents/skills",
    },
}

# The closed applicability vocabularies used by the trivial scope matcher. `any`
# in a skill's list always matches; an answer of "" (skipped question) also
# matches everything (no filter on that axis). `node` is the one JS/TS label —
# a js/ts split would fragment the vocabulary (Thread 34, D2/R6).
STACK_CHOICES = ("python", "node", "go", "rust", "powershell", "any")
DOMAIN_CHOICES = ("web", "game", "hardware", "data", "any")

# Curated knowledge packs are an explicit domain opt-in.  Unlike skills, an
# unspecified/"any" domain must not install the superset: packs become authored
# project context once materialized, so irrelevant packs would be durable noise.
KNOWLEDGE_PACKS = {
    "web": (
        ("ui-design-systems", "UI & design systems", "web"),
        ("web-rendering", "Web rendering", "web"),
        ("model-inference", "Model inference", "web"),
    ),
    "hardware": (
        ("perception", "Perception", "hardware"),
        ("kinematics", "Kinematics", "hardware"),
        ("simulation-robot-learning", "Simulation & robot learning", "hardware"),
    ),
}

# Stacks that are *explicitly* not Python: their scaffold skips the dead Python
# artifacts (pytest.ini) and gets the harness-rewiring checklist appended to
# docs/status.md as Open-items bullets instead (Thread 34, R7/C3). Blank/`any`
# keeps today's Python-reference scaffold byte-for-byte.
NON_PYTHON_STACKS = ("node", "go", "rust", "powershell")


def selected_agents(choice):
    """Expand an --agents choice into the concrete agent keys to materialize.

    `both` stays claude+gemini (its historical meaning — an explicit `codex`
    selection is how a repo populates `.agents/skills`); `none` materializes
    nothing."""
    if choice == "both":
        return ["claude", "gemini"]
    if choice in AGENTS:
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
    An unspecified domain resolves to `any`, which selects universal skills but
    not domain-specific ones; those require an explicit domain opt-in."""
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
        # The inert hook example is optional — an agent with no shipped hook
        # config (codex) declares no `hooks_src` and simply gets its skills.
        if not spec.get("hooks_src"):
            continue
        hooks_src = KIT / spec["hooks_src"]
        if hooks_src.exists():
            hooks_dst = dest / spec["hooks_dst"]
            if not hooks_dst.exists() or force:
                if not dry_run:
                    hooks_dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(hooks_src, hooks_dst)
                created.append(spec["hooks_dst"])
    return created


def materialize_knowledge_packs(dest, domain, dry_run, force):
    """Install the curated packs for one explicitly declared domain.

    Pack files are write-once like the rest of the scaffold.  The index is
    extended only for files this invocation creates/overwrites, and only when
    their row is absent, so a re-run cannot duplicate rows or silently adopt a
    pre-existing project-owned pack into the kit's index.
    """
    selected = KNOWLEDGE_PACKS.get(domain, ())
    created = []
    indexed = []
    for label, topic, pack_domain in selected:
        src = KIT / "knowledge" / (label + ".md")
        dst_rel = "docs/knowledge/" + label + ".md"
        dst = dest / dst_rel
        if not src.is_file() or (dst.exists() and not force):
            continue
        if not dry_run:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)
        created.append(dst_rel)
        indexed.append((label, topic, pack_domain))

    index = dest / "docs" / "knowledge" / "README.md"
    if indexed and index.is_file() and not dry_run:
        text = index.read_text(encoding="utf-8")
        rows = []
        for label, topic, _pack_domain in indexed:
            marker = "[{}]({}.md)".format(label, label)
            if marker not in text:
                # Cells follow the index header `| Label | Topic | Components |
                # Last reviewed |` (knowledge/README.template.md): the kit knows
                # no Components mapping and stamps no date (deterministic — the
                # adopter fills both when they first review the pack).
                rows.append("| [{}]({}.md) | {} | — | — |".format(label, label, topic))
        if rows:
            _write_text_lf(index, text.rstrip() + "\n" + "\n".join(rows) + "\n")
    return created


def sync_agent_skills(dest, dry_run):
    """Force-refresh each per-agent skill copy from the ONE neutral source, so a
    "edit source → re-materialize" is one command (`bootstrap.py --sync`).

    The kit fans `project-trajectory/skills/<name>/` out to `.claude/skills/`,
    `.gemini/skills/`, and `.agents/skills/` as byte-identical copies (S7,
    tracked + drift-checked). Materialization is otherwise write-once so it never
    clobbers project content; this refresh is the deliberate exception — but it
    touches ONLY the `<agent>/skills/<name>/` subtree of a per-agent dir that
    ALREADY exists (a subset dir stays a subset; creating a per-agent dir is
    `--agents`' job), and only the skills that dir already carries. A file
    outside `<agent>/skills/<name>/` is never read or written, so a project's own
    settings/hook files are safe. Byte-exact (read/write bytes — CRLF must not
    false-refresh). Within a synced `<agent>/skills/<name>/` subtree — which is
    kit-owned by contract — a dest file with no source counterpart is DELETED
    (and emptied subdirs removed): when a kit skill drops a file, the
    `--check-agents` floor goes red on the stray and prescribes `--sync`, so
    `--sync` must actually be able to fix it (M-14). Returns the list of
    refreshed/removed dest-relative file paths."""
    source = KIT / "skills"
    refreshed = []
    if not source.is_dir():
        return refreshed
    for spec in AGENTS.values():
        agent_skills = dest / spec["skills_dir"]
        if not agent_skills.is_dir():
            continue
        for name_dir in sorted(p for p in agent_skills.iterdir() if p.is_dir()):
            src_skill = source / name_dir.name
            if not (src_skill / "SKILL.md").exists():
                continue  # a copy with no source (orphan) — the drift check flags it
            src_rels = set()
            for src_file in sorted(f for f in src_skill.rglob("*") if f.is_file()):
                rel = src_file.relative_to(src_skill)
                src_rels.add(rel)
                dst_file = name_dir / rel
                data = src_file.read_bytes()
                if dst_file.exists() and dst_file.read_bytes() == data:
                    continue
                refreshed.append(
                    (Path(spec["skills_dir"]) / name_dir.name / rel).as_posix()
                )
                if not dry_run:
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    dst_file.write_bytes(data)
            # Deleted-source drift: files under this dest skill dir with no
            # source counterpart (see docstring). Deepest-first so emptied
            # subdirs can be pruned after their files go.
            for dst_file in sorted(
                (f for f in name_dir.rglob("*") if f.is_file()),
                key=lambda p: len(p.parts),
                reverse=True,
            ):
                rel = dst_file.relative_to(name_dir)
                if rel in src_rels:
                    continue
                refreshed.append(
                    (Path(spec["skills_dir"]) / name_dir.name / rel).as_posix()
                )
                if not dry_run:
                    dst_file.unlink()
                    parent = dst_file.parent
                    while parent != name_dir and not any(parent.iterdir()):
                        parent.rmdir()
                        parent = parent.parent
    return refreshed


# Per-agent example commands seeded into the agent-resume launchers' AGENT_CMD
# EDIT slot when --agents chose that agent (Thread 33; "both" seeds the first).
# They stay examples the repo owns — including the permission-bypass flag,
# which the launcher header and the loop banner call out as the consent line.
AGENT_RESUME_SEEDS = {
    "claude": {
        # No {prompt}: the loop pipes the prompt to the CLI's stdin (WI-216),
        # immune to the OS command-line caps a brief-sized prompt-in-argv hits.
        "cmd": "claude -p --model {model} --output-format json "
        "--dangerously-skip-permissions",
        "interactive": "claude --model {model} {prompt}",
        # Strong tier by default: driver sessions carry gate-bearing judgment
        # (process.md §6 tiering) — step phases down via AGENT_MODEL_MAP, not
        # by seeding the whole loop cheap.
        "model": "opus",
    },
    "gemini": {
        "cmd": "gemini --prompt {prompt} --model {model} --yolo",
        "interactive": "gemini --model {model} --prompt-interactive {prompt}",
        "model": "gemini-2.5-pro",
    },
}


def seed_agent_resume(dest, agents, created, dry_run):
    """Fill the freshly scaffolded agent-resume launchers' AGENT_CMD/AGENT_MODEL
    slots with the chosen agent's example command (the RUN_CMD stance: the slot
    is an EDIT block the repo owns — bootstrap only seeds it, and only on the
    run that created the file, so a re-sync never clobbers a repo's own slot).
    Returns True when the slots were seeded."""
    if dry_run or not agents or agents[0] not in AGENT_RESUME_SEEDS:
        return False
    seed = AGENT_RESUME_SEEDS[agents[0]]
    seeded = False
    for rel, empty, fmt in (
        ("agent-resume.cmd", 'set "{}="', 'set "{}={}"'),
        ("agent-resume.sh", '{}=""', '{}="{}"'),
    ):
        if rel not in created:
            continue
        path = dest / rel
        text = path.read_text(encoding="utf-8")
        for var, value in (
            ("AGENT_CMD", seed["cmd"]),
            ("AGENT_MODEL", seed["model"]),
            ("AGENT_CMD_INTERACTIVE", seed["interactive"]),
        ):
            text = text.replace(empty.format(var), fmt.format(var, value), 1)
        # LF for both files: agent-resume.sh MUST stay LF (CRLF breaks its
        # shebang); the .cmd tolerates LF (no labels/goto) and the scaffolded
        # .gitattributes re-normalizes it to CRLF at the first commit.
        _write_text_lf(path, text)
        seeded = True
    return seeded


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
    _write_text_lf(status, text + note)
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


# The three gate-authority levels (Thread 32, process.md §4). The level is
# chosen before the kit is ported — a one-word docs/gate-policy value; a
# non-default level also gets the repo-local deviation register that amends
# the untouched, kit-owned process.md (process-options.md "Gate authority
# levels" — the NotHomeWrecker-proven pattern).
GATE_POLICY_CHOICES = ("attended", "single-ratify", "autonomous")

# Per-level deviation rows for the register skeleton: (process.md clause,
# standard behavior, this repo). The fixed points are appended for every level.
GATE_POLICY_DEVIATIONS = {
    "single-ratify": [
        (
            "§4 acceptor, G1+G2",
            "a human approves each gate",
            "LLM-gate review; every human call queued as a `Needs <human>` "
            "Open item (+ provisional decision where the driver proceeded)",
        ),
        (
            "§4 ratification point",
            "per-gate approval",
            "one human sitting at **G2 close** ratifies/amends the queue; "
            "ratified decisions move to docs/log.md (relocating the point = "
            "amending this register)",
        ),
        (
            "§4 acceptor, G3→G-Release",
            "a human approves each gate",
            "autonomous rules after ratification (LLM-gate verdicts)",
        ),
        (
            "§4 consistency review 'pause and ask'",
            "solicit the human",
            "route by revert-cost: LOW → decide + record (log.md Decisions "
            "log); MEDIUM/HIGH → the Blocked register; never a mid-run pause",
        ),
    ],
    "autonomous": [
        (
            "§4 acceptor, G1→G-Release",
            "a human approves each gate",
            "LLM-gate: an independent fresh-context reviewer runs the harness "
            "itself; verdict recorded in docs/log.md with `Model:` + "
            "`Role: LLM-GATE`; the driver makes the ratifying Status-change "
            "commit + regenerates docs/gate (derive_gate.py) citing it",
        ),
        (
            "mid-run escalation to the human",
            "escalate and wait",
            "Blocked register in status.md; continue independent work; all "
            "blocks surface in the end-of-run report",
        ),
        (
            "ask-the-human / solicit clarification",
            "pause and ask",
            "decide + record in the log.md Decisions log; HIGH revert-cost "
            "gets an independent peer-tier second opinion before execution",
        ),
        (
            "§4 `Attest` (named human judgment)",
            "a human attests",
            "LLM-Attest: named *model* judgment, reported honestly as machine "
            "attestation in the trace report's attested-vs-mechanized split",
        ),
    ],
}

GATE_POLICY_FIXED_POINTS = """## Fixed points (nothing in this file overrides these)

- **G-Final is the human's.**
- **No un-run greens** — a verdict or test result that wasn't actually
  executed is a process violation regardless of tier.
- **The harness is still the bar** — LLM judgment supplements the checks; it
  never waives a red one.
- **Ratified owner decisions are never re-decided by an agent** — flag a
  problematic one as Blocked instead.
"""


def apply_gate_policy(dest, level, dry_run):
    """Write a non-default gate-authority level: set docs/gate-policy (keeping
    the template's explanatory header) and scaffold the deviation-register
    skeleton (docs/gate-policy.md) pre-filled for the level. Returns the list
    of dest-relative paths written."""
    if level == "attended" or dry_run:
        return []
    header = [
        ln
        for ln in (KIT / "gate-policy.template")
        .read_text(encoding="utf-8")
        .splitlines()
        if ln.startswith("#")
    ]
    policy = dest / "docs" / "gate-policy"
    policy.parent.mkdir(parents=True, exist_ok=True)
    _write_text_lf(policy, "\n".join(header + [level]) + "\n")
    register = dest / "docs" / "gate-policy.md"
    written = ["docs/gate-policy"]
    if not register.exists():
        rows = "\n".join(
            "| {} | {} | {} |".format(*row) for row in GATE_POLICY_DEVIATIONS[level]
        )
        _write_text_lf(
            register,
            "# Gate-authority deviation register — `{level}`\n\n"
            "**Status:** DRAFT — ratify with the owner, then keep in version "
            "control.\n"
            "**What this is:** this repo declares the `{level}` gate authority "
            "(`docs/gate-policy`; process.md §4). The kit-owned process doc is "
            "never edited per-repo (a re-sync overwrites it); this register "
            'amends it (process-options.md "Gate authority levels"). Where '
            "the two disagree, this file wins — except the fixed points at "
            "the bottom, which nothing overrides.\n\n"
            "## Deviation register\n\n"
            "| process.md clause | Standard behavior | This repo |\n"
            "|---|---|---|\n"
            "{rows}\n\n"
            "{fixed}".format(level=level, rows=rows, fixed=GATE_POLICY_FIXED_POINTS),
        )
        written.append("docs/gate-policy.md")
    return written


# Who may publish (Thread 40, process-options.md "Agent iteration branch &
# sync"). Declared once at scaffold time like the gate authority; the value is
# honored by agent drivers/coordinators as a process rule (hooks are per-clone
# and can only assist).
PUSH_POLICY_CHOICES = ("human", "agent-iteration", "agent")


def apply_push_policy(dest, policy, dry_run):
    """Write a non-default push policy into docs/push-policy, keeping the
    template's explanatory header (same shape as apply_privacy_check)."""
    if policy == "human" or dry_run:
        return
    header = [
        ln
        for ln in (KIT / "push-policy.template")
        .read_text(encoding="utf-8")
        .splitlines()
        if ln.startswith("#")
    ]
    target = dest / "docs" / "push-policy"
    target.parent.mkdir(parents=True, exist_ok=True)
    _write_text_lf(target, "\n".join(header + [policy]) + "\n")


def apply_privacy_check(dest, value, dry_run):
    """Write the privacy-check toggle into docs/privacy-check, keeping the
    template's explanatory header. Set at repo creation — an explicitly
    passed/answered `true` overwrites the scaffolded default (`false`)."""
    if dry_run:
        return
    header = [
        ln
        for ln in (KIT / "privacy-check.template")
        .read_text(encoding="utf-8")
        .splitlines()
        if ln.startswith("#")
    ]
    target = dest / "docs" / "privacy-check"
    target.parent.mkdir(parents=True, exist_ok=True)
    _write_text_lf(target, "\n".join(header + [value]) + "\n")


# (The opt-in parallel-tracks layer is retired outright, WI-210: the
# dispatcher's --wi/--train worker assignment is the only lane concept, so
# --tracks, tracks-README.template.md, and the per-track ID-block scaffold
# are gone. An adopted repo's existing docs/tracks/ notes are its own files;
# ADOPTING.md §6 carries the migration recipe.)


# --- Conditional scaffold generation (Thread 34, Q8 ruling) -------------------
# The kit's master templates contain ALL permutations; bootstrap *generates*
# each repo's docs by omitting the marked regions its declared profile doesn't
# use. The grammar is deliberately dumb — exact full-line HTML-comment markers,
# no nesting — and § headings stay OUTSIDE the markers, so section labels are
# literal text that never renumbers and every anchor resolves in every
# permutation (a finding citing §9 means the same thing in every adopted repo).
#
#   <!-- kit-only -->  ...  <!-- /kit-only -->     dropped from every scaffold
#       (the degenerate profile no repo selects: "copy me" meta-prose).
#   <!-- profile: axis -->  ...  <!-- /profile -->  kept unless the axis is
#       omitted; an omitted region is replaced by a one-line resolvable stub.
#
# Axes are FEW AND BOOLEAN by design (the per-permutation test matrix is what
# holds the scaffold-green line; every new axis doubles it):
#   nfr           — §9 non-functional/perf budgets + its process-options
#                   expansions (the registries stay: referenced config).
#   multi-module  — the §10 scale ladder + its rung-2 expansion.
PROFILE_AXES = ("nfr", "multi-module")

KIT_ONLY_OPEN = "<!-- kit-only -->"
KIT_ONLY_CLOSE = "<!-- /kit-only -->"
PROFILE_CLOSE = "<!-- /profile -->"
PROFILE_OPEN_RE = re.compile(r"^<!--\s*profile:\s*([\w-]+)\s*-->$")


def _profile_open(line):
    return PROFILE_OPEN_RE.match(line)


def profile_stub(axis):
    """The resolvable one-liner an omitted profile region leaves behind: the
    section heading above it stays (stable §N label, resolvable anchor); this
    line says why the body is gone and where it lives."""
    return (
        "_Omitted by this repo's profile (`{}=off` in `docs/kit-profile`); the "
        "kit master retains this section — flip the axis and regenerate "
        "(ADOPTING.md §6) to opt back in._".format(axis)
    )


def strip_markers(text, omit, where="template"):
    """Generate a scaffold doc from a master: drop kit-only regions, keep or
    stub profile regions per `omit`. Raises ValueError on unbalanced or nested
    markers — the kit's own tests lint every template, so a downstream run
    should never see that."""
    out = []
    mode, axis = "copy", None  # copy | keep-prof | skip-kit | skip-prof
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        opened = _profile_open(s)
        if mode == "copy":
            if s == KIT_ONLY_OPEN:
                mode = "skip-kit"
            elif opened:
                axis = opened.group(1)
                if axis in omit:
                    out.append(profile_stub(axis))
                    mode = "skip-prof"
                else:
                    mode = "keep-prof"
            elif s in (KIT_ONLY_CLOSE, PROFILE_CLOSE):
                raise ValueError("{}:{}: close marker without an open".format(where, n))
            else:
                out.append(line)
        elif s == KIT_ONLY_OPEN or opened:
            raise ValueError("{}:{}: nested marker".format(where, n))
        elif mode == "keep-prof":
            if s == PROFILE_CLOSE:
                mode = "copy"
            elif s == KIT_ONLY_CLOSE:
                raise ValueError("{}:{}: mismatched close marker".format(where, n))
            else:
                out.append(line)
        elif mode == "skip-kit" and s == KIT_ONLY_CLOSE:
            mode = "copy"
        elif mode == "skip-prof" and s == PROFILE_CLOSE:
            mode = "copy"
    if mode != "copy":
        raise ValueError("{}: unclosed {} region".format(where, mode))
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def read_kit_profile(dest):
    """The recorded profile of an existing adoption (docs/kit-profile), or None.

    Re-sync regenerates from THIS record: when --stack/--omit aren't passed and
    the destination carries a profile, bootstrap re-reads it instead of
    defaulting — so a re-run never silently reverts a structural choice."""
    path = dest / "docs" / "kit-profile"
    if not path.exists():
        return None
    profile = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        profile[key.strip()] = value.strip()
    return profile


def write_kit_profile(dest, stack, omit, dry_run):
    """Record the resolved profile in docs/kit-profile (beside the kit-version
    stamp). Like kit-version it is a generated record, rewritten every run
    from the resolved choices — never hand-maintained."""
    body = (
        "# Kit profile — the structural scaffold choices this repo was generated\n"
        "# with. docs/process.md + docs/process-options.md are GENERATED from the\n"
        "# kit masters by omitting the sections this profile turns off (omitted\n"
        "# sections keep their heading + a one-line stub; § labels never\n"
        "# renumber). A re-sync REGENERATES from this file: bootstrap re-reads it\n"
        "# when --stack/--omit aren't passed. See ADOPTING.md §6.\n"
        "stack={}\n"
        "omit={}\n".format(stack, ",".join(sorted(omit)))
    )
    if dry_run:
        return
    target = dest / "docs" / "kit-profile"
    target.parent.mkdir(parents=True, exist_ok=True)
    _write_text_lf(target, body)


# The harness-rewiring checklist appended to a non-Python scaffold's status.md
# Open items (WI-1.17 bullet shape: stable OI ids, the decision stated, a
# blocks: clause where something waits, a trailing artifact link). These are
# the hand-edits a non-Python stack still owes (ADOPTING.md §2); making them
# visible work items keeps them from becoming folklore. OI-1/OI-2 are the
# template's seeded examples, so the checklist starts at OI-3.
STACK_NEEDS_HUMAN = (
    "    - OI-3 — decide: the {stack} toolchain commands (format / lint / "
    "test) in docs/stack.ini's [product] section (blocks: G1) → "
    "[stack.ini](stack.ini)\n"
)
STACK_IN_FLIGHT = (
    "    - OI-4 — rewire scripts/setup.* dependency installs for {stack} → "
    "[setup.sh](../scripts/setup.sh)\n"
    "    - OI-5 — rewire the CI install step for {stack} → "
    "[check.yml](../.github/workflows/check.yml)\n"
    "    - OI-6 — map the Smoke/Full/Release test tiers onto the {stack} "
    "runner in docs/stack.ini's [tiers] (pytest.ini deliberately not "
    "scaffolded) → [stack.ini](stack.ini)\n"
)
# The Needs-<human> OI-3 carries its decision brief in docs/open-items.md
# (check_docs S-3: every owner ask has its brief); the In-flight OI-4..6 are
# driver work and need none.
# The scaffolded open-items.md ends with the generated pending-owner-actions
# block (WI-234), separated from the hand-authored briefs by a `---` + lead-in
# comment; a stack brief is inserted ABOVE that separator so it never lands
# below the marker. Kept byte-exact with OPEN_ITEMS.template.md's tail.
OI_PENDING_ANCHOR = "---\n\n<!-- Generated pending-owner-actions projection"

STACK_OI3_BRIEF = (
    "\n## OI-3 — Decide: the {stack} toolchain commands\n\n"
    "- **Decision:** the format / lint / test commands for the {stack} stack "
    "in docs/stack.ini's `[product]` section (blocks: G1).\n"
    "- **Blast radius:** every gate run and CI job shells these commands — a "
    "wrong entry green-washes the harness.\n"
    "- **Options:** the stack's conventional tools · whatever the repo "
    "already runs in CI.\n"
    "- **Recommendation:** mirror the existing CI commands first, then "
    "tighten.\n"
)


def seed_arch_map_mode(dest, stack, created, dry_run):
    """A non-Python stack starts on the stack-neutral file-level arch map:
    flip the fresh docs/stack.ini's [arch-map] mode to `files` (only on the
    run that created the profile — a re-sync never rewrites a repo's own).
    The Python-AST symbol map would scan nothing and pass vacuously; the
    files fallback keeps the freshness gate real until a symbol-level
    generator is ported (ADOPTING.md §3)."""
    if dry_run or stack not in NON_PYTHON_STACKS or "docs/stack.ini" not in created:
        return False
    ini = dest / "docs" / "stack.ini"
    text = ini.read_text(encoding="utf-8")
    if "mode = symbols" not in text:
        return False
    _write_text_lf(ini, text.replace("mode = symbols", "mode = files", 1))
    return True


def append_stack_checklist(dest, stack, dry_run):
    """Insert the rewiring checklist into the freshly scaffolded status.md's
    Open-items sub-lists (Needs <human> / In flight). Only called when this
    run created status.md and the declared stack is explicitly non-Python."""
    status = dest / "docs" / "status.md"
    if dry_run or not status.exists():
        return False
    text = status.read_text(encoding="utf-8")
    # Anchor on the template's seeded sub-list heads; insert after each head's
    # example bullet (the next "  - " line at the outer level closes it).
    human_anchor = "  - **In flight** _(driver; no approval needed)_:\n"
    flight_anchor = "- **Assumptions (unattended):**"
    if human_anchor not in text or flight_anchor not in text:
        return False
    text = text.replace(
        human_anchor, STACK_NEEDS_HUMAN.format(stack=stack) + human_anchor, 1
    )
    text = text.replace(
        flight_anchor,
        STACK_IN_FLIGHT.format(stack=stack) + flight_anchor,
        1,
    )
    _write_text_lf(status, text)
    # OI-3 is a Needs-<human> ask, so it owes a brief (check_docs S-3). Insert it
    # ABOVE the generated pending-owner-actions block (WI-234) so hand-authored
    # briefs stay above the marker, never below it.
    open_items = dest / "docs" / "open-items.md"
    if open_items.exists():
        oi_text = open_items.read_text(encoding="utf-8")
        brief = STACK_OI3_BRIEF.format(stack=stack)
        if OI_PENDING_ANCHOR in oi_text:
            oi_text = oi_text.replace(
                OI_PENDING_ANCHOR,
                brief.strip("\n") + "\n\n" + OI_PENDING_ANCHOR,
                1,
            )
        else:
            oi_text = oi_text + brief
        _write_text_lf(open_items, oi_text)
    return True


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
    # The machine-readable active gate (first non-comment line: G1|G2|G3).
    # check.py and CI read it, so a young project's CI enforces the bar it is
    # actually at. It is DERIVED from the artifact states by derive_gate.py (not
    # hand-set); closing a gate = ratifying artifacts in a reviewed commit +
    # regenerating. The scaffold ships a legacy one-liner (accepted value-only);
    # `python scripts/derive_gate.py` migrates it to the generated form.
    ("gate.template", "docs/gate"),
    # The declared gate authority (Thread 32, process.md §4): who accepts a
    # gate advance. Scaffolds `attended`; --gate-policy sets a non-default
    # level and pre-fills the deviation-register skeleton for it.
    ("gate-policy.template", "docs/gate-policy"),
    # The reviewer dial (process-options.md "Unattended
    # operation"): how many independent fresh-context review verdicts a WI
    # gets (0|1|2). Default `1`; floors above the dial live in the file.
    ("review-policy.template", "docs/review-policy"),
    # The model REGISTRY the coordinator's router reads (WI-059, S8): one row per
    # usable model keyed [PROVIDER]-[MODEL_NAME]-[VERSION], with example rows for
    # the verified headless shapes. Present but INERT until docs/agents-enabled
    # (the ordered enable-list / consent surface, deliberately NOT scaffolded) is
    # created — routing then selects from that pool (process-options.md
    # "Unattended operation" -> routing/escalation). Absent both files = today's
    # single AGENT_CMD/AGENT_MODEL behavior.
    ("agents.template.csv", "docs/agents.csv"),
    # The privacy-check toggle (Thread 38 -> identity/privacy reframe,
    # process-options.md "Commit identity & privacy"): `false` by default;
    # --privacy-check overrides.
    ("privacy-check.template", "docs/privacy-check"),
    # The declared push authority (Thread 40, process-options.md "Agent
    # iteration branch & sync"): who may publish. `human` by default — an
    # agent never pushes; --push-policy overrides.
    ("push-policy.template", "docs/push-policy"),
    # The weekday blackout window (WI-148, process-options.md "Unattended
    # operation"): a `HH:MM-HH:MM` UTC Mon–Fri window the coordinator starts no
    # new session inside (it waits the window out, then resumes). Ships the
    # 12:00–19:00 default so a fresh scaffold gets it; delete the file or set
    # start==end to disable (absent = disabled, byte-identical to before).
    ("blackout.template", "docs/blackout"),
    ("STATUS.template.md", "docs/status.md"),
    # The owner decision briefs status.md's Needs-<human> bullets link to
    # (process-options.md "Trajectory / work-items layer"): one OI-N section
    # per pending decision, deleted when the ruling lands in log.md Decisions.
    ("OPEN_ITEMS.template.md", "docs/open-items.md"),
    # The append-only history status.md points at (Thread 36, process.md §5):
    # sign-offs, verdicts, and ratified decisions append here, keeping the
    # per-session status.md reload cheap.
    ("LOG.template.md", "docs/log.md"),
    # The sequenced work-plan the plan/build cadence runs on (WI-1.29,
    # process-options.md "Unattended operation" → Plan/build cadence): PLAN
    # sessions write blocks here, BUILD sessions execute them; status.md stays
    # the lean resume surface and points at it.
    ("PLAN.template.md", "docs/plan.md"),
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
    (
        "registries/components.template.csv",
        "docs/requirements/components.csv",
    ),
    (
        "registries/work-items.template.csv",
        "docs/requirements/work-items.csv",
    ),
    ("registries/test-cases.template.csv", "docs/test/test-cases.csv"),
    # Specs-of-record (process-options.md "Trajectory / work-items layer"): the
    # per-WI spec directory the work-items.csv `SpecRef` column points at (rule
    # R-E). A README explaining the layer + an inert WI-000 example carrying the
    # Done-when checklist. Nothing gates on the -000 file (check_trajectory
    # ignores the WI-000 row), so a fresh scaffold stays vacuously clean.
    ("specs/README.template.md", "docs/specs/README.md"),
    ("specs/WI-000.template.md", "docs/specs/WI-000.md"),
    # Durable, hand-owned project knowledge: one topic per pack, indexed by this
    # README so documentation checks discover every pack. Packs are advisory;
    # requirements remain authoritative in the spine.
    ("knowledge/README.template.md", "docs/knowledge/README.md"),
    # Critique rubrics (process-options.md "Critique verification & the critique
    # loop", WI-068): the judgment reference a Verification=Critique requirement is
    # scored against — written from the SN/SR intent (not the possibly-lax TC),
    # carrying numbered good/bad anchors that accumulate at rework. A README
    # explaining the convention + an inert rubric-000 example. Nothing gates on the
    # -000 file, so a fresh scaffold that never uses Critique carries it for free.
    ("rubrics/README.template.md", "docs/rubrics/README.md"),
    ("rubrics/rubric-000.template.md", "docs/rubrics/rubric-000.md"),
    ("scripts/trace.py", "scripts/trace.py"),
    ("scripts/derive_gate.py", "scripts/derive_gate.py"),
    ("scripts/check.py", "scripts/check.py"),
    ("scripts/check_flows.py", "scripts/check_flows.py"),
    ("scripts/check_docs.py", "scripts/check_docs.py"),
    ("scripts/check_doc_refs.py", "scripts/check_doc_refs.py"),
    ("scripts/check_perf.py", "scripts/check_perf.py"),
    ("scripts/check_stubs.py", "scripts/check_stubs.py"),
    ("scripts/check_dupes.py", "scripts/check_dupes.py"),
    ("scripts/check_coverage.py", "scripts/check_coverage.py"),
    ("scripts/check_privacy.py", "scripts/check_privacy.py"),
    ("scripts/check_vendored.py", "scripts/check_vendored.py"),
    ("scripts/check_trajectory.py", "scripts/check_trajectory.py"),
    ("scripts/subagent_gate.py", "scripts/subagent_gate.py"),
    ("scripts/gen_arch_map.py", "scripts/gen_arch_map.py"),
    ("scripts/gen_release_checklist.py", "scripts/gen_release_checklist.py"),
    ("scripts/gen_cases.py", "scripts/gen_cases.py"),
    ("scripts/gen_trajectory.py", "scripts/gen_trajectory.py"),
    ("scripts/gen_okf.py", "scripts/gen_okf.py"),
    ("scripts/plan_coverage.py", "scripts/plan_coverage.py"),
    ("scripts/plan_round.py", "scripts/plan_round.py"),
    ("scripts/plan_briefs.py", "scripts/plan_briefs.py"),
    ("scripts/plan_coverage_step.py", "scripts/plan_coverage_step.py"),
    ("scripts/plan_artifacts.py", "scripts/plan_artifacts.py"),
    # The S8 routing/scoring half of the unattended coordinator (WI-059): the
    # model-registry router + fixed escalation policy, and the substance scorer.
    # agent_loop imports them as siblings when the docs/agents-enabled enable-list
    # opts routing in; absent, they are inert (process-options.md "Unattended
    # operation" -> routing/escalation).
    ("scripts/agent_route.py", "scripts/agent_route.py"),
    ("scripts/score_reviews.py", "scripts/score_reviews.py"),
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
    ("scripts/dev-setup.template.command", "scripts/dev-setup.command"),
    ("scripts/dev-setup.template.cmd", "scripts/dev-setup.cmd"),
    # The evaluator's rungs (WI-1.12): a README skeleton the kickoff agent
    # builds out from the project brief (never overwritten — an adopted repo
    # keeps its own README), and root double-clickable product launchers, one
    # per platform, so running the product never requires recalling a command.
    # They delegate to scripts/run_menu.py (capabilities declared in the
    # docs/stack.ini [run] section) and ship inert (an absent/empty [run] section
    # prints guidance); a pure library deletes
    # them. Root, not scripts/: the double-click use case is "open the checkout
    # folder and click" — one hop shallower matters for a non-code evaluator.
    ("README.template.md", "README.md"),
    # The owner's private scratchpad (FB3, owner-feedback-2026-07-11): a root
    # file for the human owner to keep free-form notes. Its loud header tells LLM
    # agents not to read/cite/act on it, and check_docs.py exempts it entirely
    # (links, orphans, stale hints) — owner notes never gate. Always scaffolded
    # like the README front door; a repo that doesn't want it just deletes it.
    ("OWNER_SCRATCHPAD.template.md", "OWNER_SCRATCHPAD.md"),
    # The capability-menu reader the launchers delegate to (WI-067): reads the
    # docs/stack.ini [run] section and presents a menu / launches by name /
    # lists for an agent, so the launch commands live once in stack.ini instead
    # of duplicated across the platform launchers.
    ("scripts/run_menu.py", "scripts/run_menu.py"),
    ("scripts/run.template.cmd", "run.cmd"),
    ("scripts/run.template.sh", "run.sh"),
    ("scripts/run.template.command", "run.command"),
    # The work-resume counterpart (Thread 33): root agent launchers over the
    # unattended-coordinator engine. Inert until AGENT_CMD is filled (seeded
    # when --agents chose an agent); deletable like run.* — see the module
    # docstring and process-options.md "Unattended operation".
    ("scripts/agent_loop.py", "scripts/agent_loop.py"),
    # The WI-218 split of the coordinator engine: the headless session layer,
    # the shared primitives, the dual-plan runner, and the parallel
    # dispatcher/integrator agent_loop.py imports as siblings.
    ("scripts/agent_session.py", "scripts/agent_session.py"),
    ("scripts/agent_common.py", "scripts/agent_common.py"),
    ("scripts/plan_runner.py", "scripts/plan_runner.py"),
    ("scripts/agent_dispatch.py", "scripts/agent_dispatch.py"),
    ("scripts/agent-resume.template.cmd", "agent-resume.cmd"),
    ("scripts/agent-resume.template.sh", "agent-resume.sh"),
    ("scripts/agent-resume.template.command", "agent-resume.command"),
    # Agent-neutral enforcement: POSIX hooks (opt-in via
    # `git config core.hooksPath .githooks`, which setup.sh/ps1 set). commit-msg
    # scans the message; pre-push is the privacy-review backstop (Thread 39) —
    # the identity review is inert under the default `false` privacy-check (the
    # always-on secrets floor still runs), like the policy files.
    ("hooks/pre-commit", ".githooks/pre-commit"),
    ("hooks/commit-msg", ".githooks/commit-msg"),
    ("hooks/pre-push", ".githooks/pre-push"),
    # The declared product toolchain (Thread 30, process.md §7): the single home
    # for the format/lint/test commands, src/tests paths, tiers, and coverage
    # threshold. check.py/CI/hook/setup.* read it. Copied UNCONDITIONALLY (unlike
    # pytest.ini) with the Python-reference values — it's the one file a stack
    # swap edits, so every scaffold gets it (a non-Python scaffold's OI checklist
    # points here). Deleting it falls back to check.py's identical built-ins.
    ("stack.ini.template", "docs/stack.ini"),
    ("pytest.ini", "pytest.ini"),
    ("gitignore.template", ".gitignore"),
    # eol=lf pin for the sh-based git hook (a CRLF shebang breaks it under
    # Windows autocrlf). Skipped if the repo already has a .gitattributes —
    # merge the .githooks/pre-commit rule in by hand (ADOPTING.md §1).
    ("gitattributes.template", ".gitattributes"),
    ("ci/check.yml", ".github/workflows/check.yml"),
]

GITKEEP_DIRS = ["src", "tests"]

# Per-destination text fixups applied right after a template is generated: the
# in-line rewrites a marker strip can't express (a phrase inside a line that
# must otherwise survive). Whole-region copy-me prose belongs in kit-only
# markers instead (Thread 34). Keyed by destination rel-path; each entry is
# (old, new). Kept to exact, unique strings so a missed match is a no-op,
# never a wrong edit.
TEMPLATE_REWRITES = {
    "docs/process.md": [
        ("# Development Process (template)", "# Development Process"),
    ],
}


# Archive-anchor provenance citations — comment/docstring pointers into this
# meta-repo's docs/archive/ review docs (THREAD_<n>_REVIEW.md, REVIEW_GRIND_A/B/
# FULL.md) tagged with a finding code (A5, C7, F4). They resolve HERE but dangle
# for a downstream reader, whose scaffold copies the scripts WITHOUT docs/archive/
# — so bootstrap drops them as it copies, keeping the copy-ready *why* and leaving
# the provenance in the kit (deep-review-2026-07-12 M7 / WI-079). The anchors are
# doc names that never appear in code (REVIEW_GRIND_[A-Z]+ excludes the
# REVIEW_PHASES identifier), so these subs can only ever touch a real citation,
# never a `foo()` call. Design-doc references (AGENT_ROLES, IMPROVEMENT_PLAN) are
# a different, out-of-scope class — see the WI-079 note in docs/log.md.
_PROV_ANCHOR = r"(?:THREAD_\d+_REVIEW(?:\.md)?|REVIEW_GRIND_[A-Z]+)"
# A citation can wrap across one comment-continuation line ("REVIEW_GRIND_FULL\n
# # C6"), so allow at most one newline + optional "#" between the pieces.
_PROV_WRAP = r"[ \t]*(?:\r?\n[ \t]*#?)?[ \t]*"
_PROV_CITE = _PROV_ANCHOR + _PROV_WRAP + r"[A-Z]\d+"
# Order matters: the two in-paren clause forms run before the whole-paren form so
# a citation sharing a paren with real prose keeps the prose; the bare form last.
_PROVENANCE_SUBS = (
    # Leading clause inside a paren — drop the "ANCHOR CODE; "/" — " head, keep
    # the prose: "(C5; verbatim across the kit)" -> "(verbatim across the kit)".
    (re.compile(r"\(" + _PROV_WRAP + _PROV_CITE + r"[ \t]*[;—][ \t]*"), "("),
    # Trailing clause inside a paren — drop the "; ANCHOR CODE"/" — " tail, keep
    # the prose and the ")": "(...second block; A6)" -> "(...second block)".
    (
        re.compile(
            r"[ \t]*[;—][ \t]*(?:#[ \t]*)?" + _PROV_CITE + r"(?=" + _PROV_WRAP + r"\))"
        ),
        "",
    ),
    # Whole-parenthetical citation that IS a whole comment line ("# (A7).") —
    # drop the line entirely so nothing dangles; the sentence it tailed sits on
    # the line above.
    (
        re.compile(
            r"\r?\n[ \t]*#[ \t]*\("
            + _PROV_WRAP
            + _PROV_CITE
            + _PROV_WRAP
            + r"\)[ \t]*\.?[ \t]*(?=\r?\n)"
        ),
        "",
    ),
    # Whole-parenthetical citation that OPENS a comment line before real prose
    # ("# (F4). Kept…") — keep the "# " and the prose, drop the citation.
    (
        re.compile(
            r"(\r?\n[ \t]*#[ \t]*)\("
            + _PROV_WRAP
            + _PROV_CITE
            + _PROV_WRAP
            + r"\)[ \t]*\.?[ \t]*"
        ),
        r"\1",
    ),
    # Whole-parenthetical citation (the paren holds nothing but the citation) —
    # drop it and the space (or wrapped-onto-its-own-line break) before it:
    # "posture (C9): ..." -> "posture: ...".
    (
        re.compile(
            r"[ \t]*(?:\r?\n[ \t]*)?\(" + _PROV_WRAP + _PROV_CITE + _PROV_WRAP + r"\)"
        ),
        "",
    ),
    # Bare trailing citation, optionally introduced by "See" and wrapped onto its
    # own comment line: "...explicitly. See\n# THREAD_52_REVIEW.md F5." -> "...".
    (
        re.compile(
            r"[ \t]*(?:[Ss]ee[ \t]*)?(?:\r?\n[ \t]*#[ \t]*)?" + _PROV_CITE + r"\.?"
        ),
        "",
    ),
)


def strip_provenance(text):
    """Remove archive-anchor review-doc provenance citations from a kit script so
    its scaffolded copy carries no pointer into docs/archive/ (which does not ship
    downstream). See _PROVENANCE_SUBS for the citation shapes handled."""
    for pat, repl in _PROVENANCE_SUBS:
        text = pat.sub(repl, text)
    return text


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
        _write_text_lf(dst, text)
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
    # Honor the scaffolded profile's arch-map mode: a non-Python scaffold is
    # seeded `[arch-map] mode = files` (see seed_arch_map_mode), and check.py
    # will verify freshness in that mode — initializing in symbols mode would
    # leave the fresh repo stale on day one.
    arch_cmd = [
        "scripts/gen_arch_map.py",
        "--src",
        "src",
        "--doc",
        "docs/architecture.md",
    ]
    ini = dest / "docs" / "stack.ini"
    if ini.exists():
        cp = configparser.ConfigParser(interpolation=None)
        try:
            cp.read_string(ini.read_text(encoding="utf-8"))
        except configparser.Error:
            pass  # check.py reports a malformed profile loudly; init stays reference-mode
        else:
            if (
                cp.has_option("arch-map", "mode")
                and cp.get("arch-map", "mode") == "files"
            ):
                arch_cmd += ["--mode", "files"]
    for rel_cmd in (
        arch_cmd,
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
            encoding="utf-8",
            errors="replace",
        )
        if sha.returncode != 0 or not sha.stdout.strip():
            return "unknown (kit not a git checkout)", False
        short = sha.stdout.strip()
        date = subprocess.run(
            ["git", "-C", str(KIT), "show", "-s", "--format=%cs", "HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        # Dirty = any staged/unstaged change anywhere in the kit checkout. We
        # stamp a real SHA either way (so the scaffold is never blocked), but
        # mark it `-dirty` and warn: the honest signal is "unreproducible".
        status = subprocess.run(
            ["git", "-C", str(KIT), "status", "--porcelain"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
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
    _write_text_lf(target, body)
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
        "--sync",
        action="store_true",
        help="refresh mode (S7): force-overwrite each existing per-agent skills "
        "subtree (.claude/.gemini/.agents) from the neutral project-trajectory/"
        "skills/ source so the copies are byte-identical again — 'edit source → "
        "re-materialize' in one command. Touches ONLY <agent>/skills/<name>/; "
        "every other scaffolded file stays write-once. Does not run the full "
        "scaffold. Vacuous when a repo has no per-agent skills dir.",
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
        help="declared primary stack (python|node|go|rust|powershell|any). "
        "Drives skill matching AND the scaffold profile: an explicitly "
        "non-Python stack skips pytest.ini and appends the harness-rewiring "
        "checklist to docs/status.md. Omitted + interactive -> ASK; "
        "non-interactive -> the recorded docs/kit-profile, else 'any' "
        "(today's Python-reference scaffold, unchanged).",
    )
    ap.add_argument(
        "--omit",
        default=None,
        metavar="AXIS[,AXIS...]",
        help="profile axes to omit from the generated process docs ({}). An "
        "omitted section keeps its § heading + a one-line stub, so labels "
        "never renumber and links never dangle. Omitted flag -> the recorded "
        "docs/kit-profile, else omit nothing.".format("|".join(PROFILE_AXES)),
    )
    ap.add_argument(
        "--domain",
        choices=DOMAIN_CHOICES,
        default=None,
        help="declared primary domain, for skill matching and curated knowledge-"
        "pack opt-in (web|game|hardware|data|any). web/hardware materialize their "
        "pack sets; any/omitted materializes no packs. Omitted + interactive "
        "agent setup -> ASK; non-interactive -> no filter.",
    )
    ap.add_argument(
        "--gate-policy",
        choices=GATE_POLICY_CHOICES,
        default=None,
        help="declared gate authority for docs/gate-policy (process.md §4): "
        "attended|single-ratify|autonomous. Omitted + interactive TTY -> ASK; "
        "non-interactive -> 'attended' (the default level; zero change). A "
        "non-default level also scaffolds the deviation-register skeleton "
        "(docs/gate-policy.md) pre-filled for it.",
    )
    ap.add_argument(
        "--push-policy",
        choices=PUSH_POLICY_CHOICES,
        default=None,
        help="declared push authority for docs/push-policy (process-options.md "
        '"Agent iteration branch & sync"): human|agent-iteration|agent. '
        "Omitted + interactive TTY -> ASK; non-interactive -> 'human' (the "
        "default: an agent never pushes; it prepares the branch and requests).",
    )
    ap.add_argument(
        "--privacy-check",
        choices=("true", "false"),
        default=None,
        help="privacy gate for docs/privacy-check: 'true' runs the PII/identity "
        "leak scan (author email + content must be non-private), 'false' (the "
        "default) leaves it off. The always-on secrets floor runs regardless. "
        "Omitted + interactive TTY -> ASK; non-interactive -> 'false' "
        '(process-options.md "Commit identity & privacy").',
    )
    args = ap.parse_args()

    dest = Path(args.dest).resolve()

    # --sync (S7): a FOCUSED refresh of the per-agent skill copies, nothing else.
    # Kept separate from the full scaffold pass so re-materializing the skills in
    # an existing repo (e.g. this kit's own .claude/.agents) doesn't re-stamp
    # kit-version, re-run the generators, or touch any other file.
    if args.sync:
        refreshed = sync_agent_skills(dest, args.dry_run)
        verb = "would refresh" if args.dry_run else "refreshed"
        for rel in refreshed:
            print("  {}: {}".format(verb, rel))
        print(
            "\n{} per-agent skill file(s) {} from the neutral source.".format(
                len(refreshed), "to refresh" if args.dry_run else "refreshed"
            )
        )
        return

    # Resolve the scaffold profile (Thread 34): explicit flags win; else the
    # destination's recorded docs/kit-profile (so a re-sync regenerates the
    # same structural choices instead of silently reverting them); else ASK
    # for the stack on an interactive TTY / take the do-nothing defaults.
    recorded = read_kit_profile(dest) or {}
    stack = args.stack
    if stack is None:
        stack = recorded.get("stack") or None
        if stack not in STACK_CHOICES:
            stack = None
    if stack is None:
        stack = prompt_choice("Primary stack?", STACK_CHOICES, "any")
    omit_raw = args.omit if args.omit is not None else recorded.get("omit", "")
    omit = frozenset(a.strip() for a in omit_raw.split(",") if a.strip())
    unknown = omit - set(PROFILE_AXES)
    if unknown:
        ap.error(
            "--omit: unknown profile axis {} (choose from {})".format(
                ", ".join(sorted(unknown)), "|".join(PROFILE_AXES)
            )
        )

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
    # Only ask the remaining scope question when an agent was chosen and the
    # answer wasn't passed as a flag — it only drives skill matching. A
    # non-interactive run never prompts (prompt_choice returns the default).
    domain = args.domain
    if agents:
        if domain is None:
            domain = prompt_choice("Primary domain?", DOMAIN_CHOICES, "any")
        binary_assets = (
            prompt_choice("Binary assets or hardware involved?", ("yes", "no"), "no")
            == "yes"
        )
        skills = select_skills("" if stack == "any" else stack, domain, binary_assets)
    else:
        skills = []

    # Resolve the gate-authority level the same consent-first way: explicit
    # flag wins; else ASK on an interactive TTY; else 'attended' (CI-safe —
    # the scaffolded default file already says attended). Selection belongs
    # before the port: the level shapes how every later gate is run.
    gate_policy = (
        args.gate_policy
        if args.gate_policy is not None
        else prompt_choice(
            "Gate authority for this repo? (who accepts a gate advance — "
            "process.md §4)",
            GATE_POLICY_CHOICES,
            "attended",
        )
    )

    # Resolve the push authority the same consent-first way: explicit flag
    # wins; else ASK on an interactive TTY; else 'human' (CI-safe — the
    # scaffolded default file already says human, so nothing extra happens).
    push_policy = (
        args.push_policy
        if args.push_policy is not None
        else prompt_choice(
            "Push policy for this repo? (who may `git push` — "
            'process-options.md "Agent iteration branch & sync")',
            PUSH_POLICY_CHOICES,
            "human",
        )
    )

    # Resolve the privacy-check toggle the same consent-first way: explicit flag
    # wins; else ASK on an interactive TTY; else 'false' (CI-safe — the
    # scaffolded default file already says false, so nothing extra happens).
    privacy_check = (
        args.privacy_check
        if args.privacy_check is not None
        else prompt_choice(
            "Enable the privacy gate for this repo? (scan author + content for "
            'PII / identity leaks — process-options.md "Commit identity & '
            'privacy")',
            ("false", "true"),
            "false",
        )
    )

    if not dest.exists():
        if args.dry_run:
            print("would create destination directory:", dest)
        else:
            dest.mkdir(parents=True)

    created, skipped, missing = [], [], []
    for src_rel, dst_rel in MAPPING:
        src = KIT / src_rel
        dst = dest / dst_rel
        # Stack-gated artifacts (Thread 34, R7/C3): an explicitly non-Python
        # stack gets no dead Python artifacts — the rewiring checklist lands
        # in docs/status.md instead (append_stack_checklist below).
        if dst_rel == "pytest.ini" and stack in NON_PYTHON_STACKS:
            continue
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
        if dst.suffix == ".md":
            # Markdown templates are GENERATED, not copied: drop kit-only
            # regions, keep or stub profile regions per the resolved profile.
            _write_text_lf(
                dst, strip_markers(src.read_text(encoding="utf-8"), omit, src_rel)
            )
        elif dst.suffix == ".py":
            # Kit scripts copy verbatim EXCEPT for the archive-anchor provenance
            # citations, which would dangle downstream (see strip_provenance).
            # write_bytes keeps the source's LF endings byte-for-byte (unlike
            # write_text, which would translate to os.linesep on Windows).
            dst.write_bytes(
                strip_provenance(src.read_text(encoding="utf-8")).encode("utf-8")
            )
        else:
            shutil.copyfile(src, dst)
        # Strip the in-line template meta-prose a marker can't express (the
        # process doc's "(template)" title) now that the file *is* the doc.
        apply_template_rewrites(dst_rel, dst)
        # The README skeleton carries the one dynamic placeholder: the project's
        # name, taken from the destination folder (the kickoff agent fills in
        # the rest from the project brief).
        if dst_rel == "README.md":
            text = dst.read_text(encoding="utf-8")
            _write_text_lf(dst, text.replace("{{PROJECT_NAME}}", dest.name))
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
            _write_text_lf(keep, "")
            created.append("{}/.gitkeep".format(d))

    # A non-Python stack's remaining hand-edits become visible Open-items
    # bullets in the fresh status.md (only on the run that created it — a
    # re-sync must never re-append into a repo's own working surface).
    if (
        stack in NON_PYTHON_STACKS
        and "docs/status.md" in created
        and append_stack_checklist(dest, stack, args.dry_run)
    ):
        print(
            "  appended the {} harness-rewiring checklist to docs/status.md "
            "(Open items OI-3..OI-6)".format(stack)
        )
    if seed_arch_map_mode(dest, stack, created, args.dry_run):
        print(
            "  set docs/stack.ini [arch-map] mode = files (stack-neutral code "
            "map until a {} symbol-level generator is ported — "
            "ADOPTING.md §3)".format(stack)
        )

    # Materialize the chosen agent's layer: its matched skills into the native
    # skills dir + the inert hook example. "none" (the non-interactive default)
    # adds nothing, so the historical scaffold is byte-for-byte unchanged.
    created.extend(
        materialize_agent_layer(dest, agents, skills, args.dry_run, args.force)
    )
    created.extend(materialize_knowledge_packs(dest, domain, args.dry_run, args.force))

    # Seed the fresh agent-resume launchers' AGENT_CMD slot with the chosen
    # agent's example command (never on a re-sync that skipped them).
    if seed_agent_resume(dest, agents, created, args.dry_run):
        print(
            "  seeded agent-resume launchers for {} (AGENT_CMD carries the "
            "permission-bypass flag — filling/keeping it is your consent to "
            "unattended sessions; see docs/process-options.md).".format(agents[0])
        )

    # A declared non-default gate authority overwrites the scaffolded default
    # and lays down the deviation-register skeleton for the level.
    for rel in apply_gate_policy(dest, gate_policy, args.dry_run):
        if rel not in created:
            created.append(rel)
    if gate_policy != "attended":
        print("  gate-authority level: {}".format(gate_policy))

    # A declared non-default push authority overwrites the scaffolded default
    # (the file itself was just copied with `human` on its value line).
    if push_policy != "human":
        apply_push_policy(dest, push_policy, args.dry_run)
        if "docs/push-policy" not in created:
            created.append("docs/push-policy")
        print("  push policy: {}".format(push_policy))

    # A `true` privacy-check overwrites the scaffolded default (`false`) — set
    # at repo creation, the cheap moment.
    if privacy_check and privacy_check != "false":
        apply_privacy_check(dest, privacy_check, args.dry_run)
        if "docs/privacy-check" not in created:
            created.append("docs/privacy-check")
        print("  privacy-check: {}".format(privacy_check))

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

    # docs/kit-version + docs/kit-profile are generated stamps, not user
    # content, so they are always (re)written — refreshed on every
    # scaffold/re-sync to record the kit state + profile this run came from.
    label, dirty, wrote = write_kit_version(dest, args.dry_run)
    print("  {}: docs/kit-version ({})".format(verb, label))
    write_kit_profile(dest, stack, omit, args.dry_run)
    print(
        "  {}: docs/kit-profile (stack={}; omit={})".format(
            verb, stack, ",".join(sorted(omit)) or "none"
        )
    )
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
