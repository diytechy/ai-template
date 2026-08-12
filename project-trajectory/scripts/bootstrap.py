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
    docs/id-watermark                          <- id-watermark.template  (id high-water marks)
    docs/process.toml                          <- process.toml.template  (EVERY policy dial:
                                                  gate authority, the human-ratification level,
                                                  push, reviewer count, privacy + secrets,
                                                  guardrails, blackout, and the six
                                                  check-enablement toggles — SN-028's one home)
    prompts/*.template.md                      <- prompts/  (every brief the loop sends)
    docs/status.md                             <- STATUS.template.md  (working surface)
    docs/log.md                                <- LOG.template.md  (append-only history)
    docs/plan.md                               <- PLAN.template.md  (plan/build session blocks)
    docs/architecture.md                       <- ARCHITECTURE.template.md
    docs/interfaces.md                         <- INTERFACES.template.md
    docs/requirements/stakeholder-needs.toml   <- registries/stakeholder-needs.template.toml
    docs/requirements/system-requirements.toml <- registries/system-requirements.template.toml
    docs/requirements/low-level-requirements.toml
    docs/requirements/interfaces.csv           <- registries/interfaces.template.csv
    docs/requirements/performance-budgets.csv  <- registries/performance-budgets.template.csv
    docs/requirements/procurement.csv          <- registries/procurement.template.csv
    docs/requirements/assets.csv               <- registries/assets.template.csv
    docs/requirements/components.csv           <- registries/components.template.csv
    docs/work/queued/WI-000-example.md         <- work/WI-000.template.md  (the
                                                registry's spec-folder home; the
                                                other status dirs get .gitkeep)
    docs/orphans-allow                         <- orphans-allow.template  (declares
                                                docs/work/* an expected-live-orphan
                                                class: registry entries, not pages)
    docs/log.d/.gitkeep                        (the log's fragment drop-box: a work
                                                branch writes docs/log.d/<WI-id>-<slug>.md,
                                                the serial trunk step compiles them)
    docs/specs/README.md, docs/specs/WI-000.md <- specs/*.template.md  (spec-of-record dir)
    docs/knowledge/README.md                  <- knowledge/README.template.md
    docs/rubrics/README.md, docs/rubrics/rubric-000.md <- rubrics/*.template.md  (critique rubrics)
    docs/test/test-cases.toml                  <- registries/test-cases.template.toml
    scripts/trace.py, trace_text.py, derive_gate.py, check.py, check_flows.py, check_docs.py, check_perf.py,
    scripts/check_stubs.py, check_coverage.py, check_doc_refs.py, check_figures.py, check_privacy.py, check_vendored.py, check_trajectory.py,
    scripts/subagent_gate.py, gen_arch_map.py, gen_release_checklist.py, gen_cases.py, gen_trajectory.py, gen_open_items.py, gen_okf.py
    scripts/traj_graph.py, traj_parse.py, traj_render.py, traj_views.py, traj_panels.py, traj_status.py
                                               (the WI-280 gen_trajectory.py split — copied with it, always)
    scripts/plan_coverage.py, plan_round.py, plan_briefs.py, plan_coverage_step.py, plan_artifacts.py
                                               (the dual-plan round set, process-options.md "Dual-plan decomposition")
    scripts/wi_convert.py                      (work-item registry CSV <-> spec-folder converter)
    scripts/trunk_step.py                      (the serial trunk step: compile log
                                                fragments + regenerate the trunk artifacts)
    scripts/integrate.py                       (the local integrator: claim + serial
                                                fail-closed merge queue + RULING-6 audit)
    scripts/handback.py                        (the two lane closes that are not a merge:
                                                handback + its bar-inert quarantine; WI-387)
    scripts/spec_move.py                       (the link-aware spec-move ritual:
                                                move + relink as one operation; WI-393)
    scripts/intake.py                          (the unified trunk-side intake mint:
                                                three triggers + drafts-not-mints,
                                                the context block, the gate-policy
                                                flip arms; WI-388)
    scripts/agent_route.py, scripts/score_reviews.py   (S8 coordinator routing + review scorer)
    docs/agents.toml                           <- agents.template.toml (model registry; inert until docs/agents-enabled)
    scripts/setup.{sh,ps1}, scripts/check.{sh,ps1}   (cross-platform launchers)
    scripts/onboard.{sh,command,cmd}           <- onboard.template.*  (Stage-0 onboarder)
    scripts/dev-setup.{sh,ps1,command,cmd}     <- dev-setup.template.* (workstation setup)
    README.md                                  <- README.template.md (human front door; kept if one exists)
    OWNER_SCRATCHPAD.md                        <- OWNER_SCRATCHPAD.template.md (owner-only notes; agents ignore)
    scripts/run_menu.py                        (capability-menu reader the run.* launchers delegate to)
    run.{cmd,sh,command}                       <- run.template.*  (root product launchers)
    agent-resume.{cmd,sh,command}              <- agent-resume.template.*  (root agent launchers)
    scripts/agent_loop.py                      (worker/reviewer/critique session engine; entry point)
    scripts/dispatch.py                        (the dispatcher a plain agent-resume
                                                launch runs: tick loop, admission +
                                                spine barrier, merge slot; WI-374/WI-381)
    scripts/lane.py                            (one lane's mechanics: worktree, worker
                                                subprocess, the §A2 refresh; WI-381)
    scripts/agent_session.py, agent_common.py, plan_runner.py, adjudicate_brief.py
                                               (the WI-218 split: session launch / shared primitives / dual-plan runner)
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
    src/, tests/, docs/work/{draft,active,deferred,cancelled,complete}/
                                               (empty, with .gitkeep)

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
`secrets_scan` posture): a multi-module arch-map with no declared seams warns
"connectivity undeclared" rather than passing vacuously — silence it with
`docs/process.toml` `[checks] interfaces_check = false`, or a single-module
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
`docs/process.toml` `[checks] trajectory_check = false`. It is off-spine (like procurement / assets);
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

It also writes `docs/kit-license` — the kit's own Apache-2.0 text, prefixed by a
header stating what it does and does not cover. Adopting the kit *is* copying it,
and Apache-2.0 §4(a) asks that recipients of a copy also receive the License, so
the scaffold carries it rather than pointing at a URL. The scope is the copied
kit files only: the adopting project's own code, and the artifacts this scaffold
produces, are the adopter's under whatever license they choose. The text ships
inside the portable unit (`project-trajectory/LICENSE`) so it survives the
copy-in step.

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
from dataclasses import dataclass
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


# The one scaffold destination that is never force-overwritten: it is the only
# file whose content is HISTORY (which ids have been allocated and deleted) and
# so cannot be rebuilt from the tree. Kept as a basename so the rule holds
# wherever the MAPPING puts it.
WATERMARK_DEST_NAME = "id-watermark"


def copy_if_new(src, dst, dry_run, force):
    """The write-once scaffold copy, stated once (WI-347): True when `dst` was
    created (or would be, under `dry_run`), False when it already exists and
    `force` is off.

    Deliberately does NOT test `src`: one caller copies a kit file that must be
    there, where a missing source should raise rather than be skipped silently,
    and the caller that tolerates an absent source says so itself.

    ONE DESTINATION IGNORES `force`: `docs/id-watermark`. Every other scaffold
    target is a template to fill or is regenerable from the tree, so re-forcing
    it costs at most re-doing an edit. The watermark is the only record of which
    ids have been DELETED — nothing in the tree can rebuild it — so overwriting a
    live repo's marks with the fresh-scaffold ones frees every id above them for
    silent re-use. Write-once is the only safe rule for a file whose whole
    content is history."""
    if dst.exists() and (not force or dst.name == WATERMARK_DEST_NAME):
        return False
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    return True


def _skill_rel(spec, name_dir, rel):
    """The dest-relative POSIX path of one file inside a materialized skill — the
    identity `refresh_agent_skills` reports for BOTH a refreshed copy and a
    deleted-source removal. Stated once (WI-347): the two arms differ in what they
    do to the file, not in what they call it."""
    return (Path(spec["skills_dir"]) / name_dir.name / rel).as_posix()


def materialize_agent_layer(dest, agents, skills, dry_run, force):
    """Copy the selected skills (and the inert hook example) into each chosen
    agent's native location. Returns a list of created dest-relative paths."""
    created = []
    for agent in agents:
        spec = AGENTS[agent]
        for name, src in skills:
            dst_rel = "{}/{}/SKILL.md".format(spec["skills_dir"], name)
            if copy_if_new(src, dest / dst_rel, dry_run, force):
                created.append(dst_rel)
        # The inert hook example is optional — an agent with no shipped hook
        # config (codex) declares no `hooks_src` and simply gets its skills.
        if not spec.get("hooks_src"):
            continue
        hooks_src = KIT / spec["hooks_src"]
        if hooks_src.exists() and copy_if_new(
            hooks_src, dest / spec["hooks_dst"], dry_run, force
        ):
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
        # This caller TOLERATES an absent source (a domain with no pack file), so
        # it makes that test itself rather than folding it into copy_if_new.
        if not src.is_file() or not copy_if_new(src, dest / dst_rel, dry_run, force):
            continue
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
                refreshed.append(_skill_rel(spec, name_dir, rel))
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
                refreshed.append(_skill_rel(spec, name_dir, rel))
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


PROCESS_TOML_REL = "docs/process.toml"


def _toml_scalar(value):
    """A Python value as the TOML literal `set_process_key` writes. Bool and int
    render bare; everything else renders as a basic string. Deliberately tiny —
    stdlib has no TOML WRITER, and the only values this scaffolder sets are
    one-word policy tokens, an ordinal and a boolean."""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    text = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return '"{}"'.format(text)


def set_process_key(dest, section, key, value, dry_run=False, add_if_missing=False):
    """Set `[section] key = value` in `docs/process.toml`, IN PLACE.

    A LINE REWRITE, not a re-serialization: stdlib has no TOML writer, and the
    file's explanatory header is most of its value (the same reason the legacy
    appliers kept the template's `#` lines). The one-`key = value`-per-line
    convention this file owes the git hooks is exactly what makes a line
    rewrite exact.

    Returns `"set"` (written), `"same"` (already that value) or `"missing"`
    (no such file/section/key, nothing written). THREE states, not a bool: the
    MIGRATOR must be able to tell "already correct" from "I could not write
    it", because deleting a legacy file on the strength of a write that never
    happened destroys a declared policy and reports success. It did exactly
    that once, on a hand-trimmed process.toml.

    `add_if_missing` appends the key (creating the `[section]` header when
    needed) instead of answering `"missing"` — what the migrator passes, so a
    conversion is TOTAL. The scaffold flags leave it off: there, an absent key
    means someone deleted it deliberately.
    """
    path = Path(dest) / PROCESS_TOML_REL
    if not path.is_file():
        return "missing"
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    want = "{} = {}".format(key, _toml_scalar(value))
    header = "[{}]".format(section)
    at, append_at = _locate_process_key(lines, header, key)
    if at is not None:
        if lines[at] == want:
            return "same"
        if not dry_run:
            lines[at] = want
            _write_text_lf(path, "\n".join(lines) + "\n")
        return "set"
    if not add_if_missing:
        return "missing"
    if not dry_run:
        if header in [ln.strip() for ln in lines]:
            lines.insert(append_at if append_at is not None else len(lines), want)
        else:
            lines.extend(["", header, want])
        _write_text_lf(path, "\n".join(lines) + "\n")
    return "set"


def _locate_process_key(lines, header, key):
    """`(index_of_key, index_to_append_at)` for `key` under `header`.

    The pure SCAN half of `set_process_key`, split from the write half so
    neither sits at the C901 ceiling — and because "where is it" and "what do I
    write" are two questions. Either value is None when there is no answer."""
    in_section, append_at = False, None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_section = stripped == header
            continue
        if not in_section:
            continue
        if "=" in stripped and stripped.split("=", 1)[0].strip() == key:
            return i, None
        if stripped:
            append_at = i + 1
    return None, append_at


def apply_gate_policy(dest, level, dry_run):
    """Write a non-default gate-authority posture, as the THREE DIALS it is.

    `--gate-policy` still takes the familiar word, because that is how the
    posture is talked about — but the word is TRANSLATED here (SN-029,
    `LEGACY_RATIFICATION` above) rather than stored. Storing it was the
    defect: the template ships `human_ratification_through = 4`, and
    `ratification_level` prefers that key, so a `gate_policy = "autonomous"`
    written beside it was read by nothing and every repo that chose a
    non-default posture scaffolded as fully attended — silently, since neither
    dial is wrong on its own and `config_conflicts` had no rule against the
    pair.

    Also scaffolds the deviation-register skeleton (docs/gate-policy.md)
    pre-filled for the level — prose, and still keyed by the word. Returns the
    list of dest-relative paths written."""
    if level == "attended" or dry_run:
        return []
    for key, value in sorted(LEGACY_RATIFICATION.get(level, {}).items()):
        set_process_key(dest, "attestation", key, value)
    register = dest / "docs" / "gate-policy.md"
    written = [PROCESS_TOML_REL]
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
            "(`docs/process.toml` `[attestation] human_ratification_through` "
            "plus `keep_nondependent` and `final_review`; process.md "
            "§4). "
            "The kit-owned process doc is "
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
    """Write a non-default push policy into `[policies] push` of
    docs/process.toml (SN-028; same shape as apply_privacy_check)."""
    if policy == "human" or dry_run:
        return
    set_process_key(dest, "policies", "push", policy)


def apply_privacy_check(dest, value, dry_run):
    """Write the privacy-check toggle into `[policies] privacy_check` of
    docs/process.toml. Set at repo creation — an explicitly passed/answered
    `true` overwrites the scaffolded default (`false`). `value` arrives as the
    legacy one-word string; it is written as a TOML BOOLEAN, which is the shape
    the keyed git-hook grep matches (M-42)."""
    if dry_run:
        return
    set_process_key(
        dest, "policies", "privacy_check", str(value).strip().lower() == "true"
    )


# SN-029: the retired gate-authority enum, translated to the three dials that
# replaced it. DUPLICATED from `agent_common.LEGACY_RATIFICATION` under the F5
# rule — bootstrap imports no kit sibling, because it is the one script an
# adopter may run from a bare download before anything else exists — and pinned
# equal by tests/test_rule_sync.py, which is how this kit keeps a duplicated
# POLICY (as opposed to duplicated plumbing) from drifting.
#
# What each word meant, and why one key could not hold it: `attended` held every
# tier and drained the station at a ratification; `single-ratify` held NO tier
# (LLM-gate review ran through G1+G2) but sat ONE human at the close and kept
# non-dependent work running; `autonomous` did the same without the final read.
LEGACY_RATIFICATION = {
    "attended": {
        "human_ratification_through": 4,
        "keep_nondependent": False,
        "final_review": "always",
    },
    "single-ratify": {
        "human_ratification_through": 0,
        "keep_nondependent": True,
        "final_review": "always",
    },
    "autonomous": {
        "human_ratification_through": 0,
        "keep_nondependent": True,
        "final_review": "off",
    },
}


# --- SN-028: the legacy one-word -> docs/process.toml converter ---------------
# Ordered like process.toml's own sections so a converted file reads the way a
# scaffolded one does. Each row: legacy docs/<file> -> (section, key, how to
# turn its one word into a TOML value).
def _legacy_bool_true(word):
    return word.strip().lower() == "true"


def _legacy_not_off(word):
    return word.strip().lower() != "off"


def _legacy_int(word):
    try:
        return int(word.strip())
    except ValueError:
        return None


# `gate-policy` is DELIBERATELY ABSENT from this table: its one word expands to
# THREE dials (SN-029), so it cannot be a one-key row, and `_migrate_gate_policy`
# owns it below.
LEGACY_CONFIG = (
    ("push-policy", "policies", "push", str.strip),
    ("review-policy", "policies", "review_rounds", _legacy_int),
    ("privacy-check", "policies", "privacy_check", _legacy_bool_true),
    ("secrets-scan", "policies", "secrets_scan", _legacy_not_off),
    ("privacy-review", "policies", "privacy_review", str.strip),
    ("guardrails-policy", "policies", "guardrails", str.strip),
    ("blackout", "policies", "blackout", str.strip),
    # The six check-enablement toggles (2026-08-11 overturn of WI-423). Each
    # legacy vocabulary is preserved exactly by its coercer: the four opt-out
    # checks said `off` to disable and anything else to enable, `live-status`
    # said `true` to enable, and `subagent-gate` carried one of three words.
    # `set_process_key(add_if_missing=True)` writes the key even into a
    # process.toml predating this section, so an adopter converting an old
    # config never silently loses the declaration.
    ("trajectory-check", "checks", "trajectory_check", _legacy_not_off),
    ("interfaces-check", "checks", "interfaces_check", _legacy_not_off),
    ("components-check", "checks", "components_check", _legacy_not_off),
    ("okf-export", "checks", "okf_export", _legacy_not_off),
    ("live-status", "checks", "live_status", _legacy_bool_true),
    ("subagent-gate", "checks", "subagent_gate", str.strip),
)


def _first_declared_line(path):
    """The legacy one-word parse (first non-empty non-comment line), or None."""
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return None
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return None


def migrate_legacy_config(dest, dry_run=False):
    """Fold every legacy one-word policy file into docs/process.toml and DELETE
    it. Returns `(moved, notes)` — the dest-relative legacy paths absorbed, and
    human-readable lines for anything skipped.

    This is what makes plan §11.8's hard mixed-config refusal safe to ship: a
    downstream adopter never meets the refusal un-aided, because bootstrap runs
    this on every scaffold pass and ADOPTING.md §6's re-sync names it. Deleting
    the legacy file is the point — leaving it would BE the mixed config.

    Idempotent: a repo with no legacy files answers `([], [])`. A legacy file
    whose value does not parse (a non-integer reviewer dial) is left in place
    and named in `notes`, never silently dropped.
    """
    dest = Path(dest)
    target = dest / PROCESS_TOML_REL
    if not target.is_file():
        return [], ["{} is absent — nothing to migrate into".format(PROCESS_TOML_REL)]
    moved, notes = [], []
    _migrate_gate_policy(dest, moved, notes, dry_run)
    for legacy_name, section, key, coerce in LEGACY_CONFIG:
        path = dest / "docs" / legacy_name
        if not path.is_file():
            continue
        word = _first_declared_line(path)
        if word is None:
            # An empty/comment-only legacy file declared nothing; deleting it is
            # the whole migration.
            if not dry_run:
                path.unlink()
            moved.append("docs/" + legacy_name)
            continue
        value = coerce(word)
        if value is None:
            notes.append(
                "docs/{} holds {!r}, which is not a valid value — left in "
                "place; fix it, then re-run --migrate-config".format(legacy_name, word)
            )
            continue
        # THE WRITE DECIDES THE DELETE. `set_process_key` can answer "missing"
        # (a hand-trimmed process.toml, a renamed section, a dial this kit
        # version does not carry) — and unlinking on the strength of a write
        # that never happened is how a declared policy disappears under a
        # green `migrated:` line. `add_if_missing` makes the write total, and
        # the guard below is the belt beside that brace.
        wrote = set_process_key(
            dest, section, key, value, dry_run=dry_run, add_if_missing=True
        )
        if wrote == "missing":
            notes.append(
                "docs/{} could NOT be folded into {} [{}] {} — the legacy file "
                "is LEFT IN PLACE with its value intact. Fix the TOML, then "
                "re-run --migrate-config.".format(
                    legacy_name, PROCESS_TOML_REL, section, key
                )
            )
            continue
        if _has_comment_lines(path):
            notes.append(
                "docs/{} carried its own comment lines; the VALUE migrated and "
                "the notes went with the file. Re-state them in {} if they "
                "still matter.".format(legacy_name, PROCESS_TOML_REL)
            )
        if not dry_run:
            path.unlink()
        moved.append("docs/" + legacy_name)
    return moved, notes


def _migrate_gate_policy(dest, moved, notes, dry_run):
    """Fold a legacy `docs/gate-policy` word into the THREE dials it meant.

    Its own arm rather than a `LEGACY_CONFIG` row because it is the one legacy
    file that is not a one-key rename: `single-ratify` carried a tier hold, a
    drain policy AND an end-of-run hold at once, and folding it to a single key
    is what loses two of the three (SN-029). The translation itself lives in
    `agent_common.LEGACY_RATIFICATION`, so the migrator and the readers cannot
    disagree about what a word meant."""
    path = dest / "docs" / "gate-policy"
    if not path.is_file():
        return
    word = _first_declared_line(path)
    dials = LEGACY_RATIFICATION.get((word or "").strip().lower())
    if word is not None and dials is None:
        notes.append(
            "docs/gate-policy holds {!r}, which is not one of {} — left in "
            "place; fix it, then re-run --migrate-config.".format(
                word, " / ".join(sorted(LEGACY_RATIFICATION))
            )
        )
        return
    for key, value in sorted((dials or {}).items()):
        if (
            set_process_key(
                dest, "attestation", key, value, dry_run=dry_run, add_if_missing=True
            )
            == "missing"
        ):
            notes.append(
                "docs/gate-policy could NOT be folded into {} [attestation] {} "
                "— the legacy file is LEFT IN PLACE with its value intact. Fix "
                "the TOML, then re-run --migrate-config.".format(PROCESS_TOML_REL, key)
            )
            return
    if _has_comment_lines(path):
        notes.append(
            "docs/gate-policy carried its own comment lines; the VALUE migrated "
            "and the notes went with the file. Re-state them in {} if they "
            "still matter.".format(PROCESS_TOML_REL)
        )
    if not dry_run:
        path.unlink()
    moved.append("docs/gate-policy")


def _has_comment_lines(path):
    """Whether a legacy policy file carries `#` lines an adopter may have
    written (the kit's own templates do, so this is only interesting as a
    reminder, never as a refusal)."""
    try:
        return any(
            ln.lstrip().startswith("#")
            for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()
        )
    except OSError:
        return False


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
# The Needs-<human> OI-3 carries its decision brief in the open-items REGISTRY
# (check_docs S-3: every owner ask has its brief); the In-flight OI-4..6 are
# driver work and need none. WI-322 retired the markdown surface — briefs are
# ROWS in docs/requirements/open-items, rendered into the generated
# docs/open-items.html the owner reads — so the brief is APPENDED as a row
# instead of spliced above a marker.
#
# KEYS, not a positional tuple, since the carrier moved to TOML (repo-lock
# §8.1): a 12-cell tuple aligned to a header by position is exactly the shape
# that silently shifts when a column is inserted, and the carrier no longer has
# a header to align to. The key names duplicate `migrate_carrier.KEY`'s
# open-items half, and that duplication is DECLARED, not accidental:
# `bootstrap.py` runs BEFORE the kit is copied and can import no sibling
# (repo-lock §8.2 names this as the standing argument for standalone), so it
# carries its own two-line TOML emitter exactly as it already carries
# `_toml_scalar` for `docs/process.toml`. `tests/test_rule_sync.py` pins the key
# set against the converter so the two cannot drift apart in silence — the
# behavioural pin D-7 requires of any new duplication of POLICY.
STACK_OI3_ID = "OI-3"
STACK_OI3_ROW = (
    ("title", "Decide: the {stack} toolchain commands"),
    ("status", "pending"),
    (
        "one_line",
        "rule the {stack} format / lint / test commands - rec: mirror the "
        "existing CI commands first, then tighten",
    ),
    (
        "decision",
        "the format / lint / test commands for the {stack} stack in "
        "docs/stack.ini's [product] section (blocks: G1).",
    ),
    (
        "blast_radius",
        "every gate run and CI job shells these commands - a wrong entry "
        "green-washes the harness.",
    ),
    (
        "options",
        "the stack's conventional tools · whatever the repo already runs in CI.",
    ),
    ("recommendation", "mirror the existing CI commands first, then tighten."),
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
    # OI-3 is a Needs-<human> ask, so it owes a brief (check_docs S-3): append it
    # as a row of the open-items registry, which the generated owner surface
    # renders. Idempotent — re-running bootstrap must not file OI-3 twice.
    #
    # AN APPEND, NOT A RE-SERIALIZATION — the same discipline `set_process_key`
    # states for `docs/process.toml` and `intake._apply_flips` for a spine
    # Status flip, and for the same reason: every byte the scaffolder did not
    # write stays exactly as the template shipped it, comments and ordering
    # included. Under CSV this had to go through `csv.writer` for the quoting
    # (and `lineterminator="\n"`, because the default is CRLF and this repo
    # stores LF); under TOML there is no row-level quoting to get wrong, so the
    # emitter is `_toml_scalar` per cell and `_write_text_lf` for the file.
    open_items = dest / "docs" / "requirements" / "open-items.toml"
    if open_items.exists():
        existing = open_items.read_text(encoding="utf-8-sig")
        table = "[open_item.{}]".format(STACK_OI3_ID)
        if table not in existing:
            block = "{}\n{}\n".format(
                table,
                "\n".join(
                    "{} = {}".format(key, _toml_scalar(cell.format(stack=stack)))
                    for key, cell in STACK_OI3_ROW
                ),
            )
            if existing and not existing.endswith("\n"):
                existing += "\n"
            if existing and not existing.endswith("\n\n"):
                existing += "\n"
            _write_text_lf(open_items, existing + block)
            raise_watermark(dest, "OI", 3)
    return True


def raise_watermark(dest, space, floor):
    """Raise `space`'s id-watermark mark to at least `floor` (never lower it).

    Scaffolding a row is ALLOCATING an id, so the mark has to cover it: the
    always-on integrity pass refuses a live id standing above its mark, and a
    scaffold that ships one fails `trace.py --strict` on the adopter's very
    first run — which is precisely what SN-001 promises a fresh scaffold does
    not do. That is not hypothetical: `id-watermark.template` ships `OI = 2`
    and the non-Python profile appends OI-3, so every node/other-stack scaffold
    shipped internally inconsistent until this call existed.

    Raise-only, because the mark is a HIGH-WATER mark: it may legally stand
    above the live maximum (that headroom is what keeps a deleted id from being
    re-minted), but it must never fall."""
    path = dest / "docs" / WATERMARK_DEST_NAME
    if not path.is_file():
        return False
    out, hit = [], False
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        m = re.match(r"^([A-Z]+)\s*=\s*(-?\d+)\s*$", line.strip())
        if m and m.group(1) == space:
            hit = True
            if int(m.group(2)) < floor:
                line = "{} = {}".format(space, floor)
        out.append(line)
    if hit:
        _write_text_lf(path, "\n".join(out) + "\n")
    return hit


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
    # The id watermark (docs/id-watermark): the high-water mark per id space, so
    # a deleted row's number is never re-minted. REQUIRED, because trace.py
    # treats an absent mark as an error rather than as "no id is taken".
    # NOT all-zeros: the template covers the example rows the other templates
    # seed (OI=2), so it is generated from a real scaffold, never hand-written.
    # NEVER --force THIS ONE onto a live repo. Every other target here is a
    # template to fill or is regenerable from the tree (docs/gate <- derive_gate);
    # this file is the only record of ids that have been DELETED, so overwriting
    # it with the fresh-scaffold marks destroys information nothing can recover.
    # `copy_file` therefore exempts it from --force (see WATERMARK_DEST).
    ("id-watermark.template", "docs/id-watermark"),
    # THE ONE POLICY HOME (SN-028). Every process dial — gate authority, the
    # human-ratification level, push authority, the reviewer count, the privacy
    # toggle, the secrets floor, guardrails, the blackout window — declared once
    # here instead of in ~10 one-word files. A FRESH SCAFFOLD GETS ONLY THIS
    # FILE: shipping both homes would hand every new repo the mixed-config
    # refusal on its first run. An EXISTING repo converts with
    # `bootstrap.py --migrate-config`, which bootstrap runs for you (see
    # `migrate_legacy_config`). The three --gate-policy/--push-policy/
    # --privacy-check flags now rewrite a KEY in this file rather than writing
    # their own file.
    ("process.toml.template", "docs/process.toml"),
    # THE PROMPTS (plan §8). Every brief the loop sends is a FILE now, not a
    # Python string constant, and `scripts/prompts.py` resolves them
    # SCRIPT-RELATIVELY — in a scaffolded repo `scripts/` sits at the root, so
    # the templates must land in `prompts/` or every worker, reviewer and
    # critique session downstream loses its brief. (Before this, the three
    # dual-plan hats were the only templates here and nothing copied them: the
    # opt-in round simply PAGEd "hat template unreadable". That degrade was
    # tolerable for an opt-in layer and is not for the ordinary session path.)
    # Kit-owned: a re-sync overwrites them, and a repo that wants different
    # prose wires its own file through --prompt-map instead of editing these.
    ("prompts/README.md", "prompts/README.md"),
    ("prompts/worker.template.md", "prompts/worker.template.md"),
    ("prompts/reviewer.template.md", "prompts/reviewer.template.md"),
    ("prompts/critique.template.md", "prompts/critique.template.md"),
    (
        "prompts/adjudicate-amendment.template.md",
        "prompts/adjudicate-amendment.template.md",
    ),
    (
        "prompts/adjudicate-disposition.template.md",
        "prompts/adjudicate-disposition.template.md",
    ),
    (
        "prompts/adjudicate-conflict.template.md",
        "prompts/adjudicate-conflict.template.md",
    ),
    ("prompts/adjudicate-red-tc.template.md", "prompts/adjudicate-red-tc.template.md"),
    ("prompts/dual-plan-planner.template.md", "prompts/dual-plan-planner.template.md"),
    ("prompts/dual-plan-critic.template.md", "prompts/dual-plan-critic.template.md"),
    ("prompts/dual-plan-arbiter.template.md", "prompts/dual-plan-arbiter.template.md"),
    # The model REGISTRY the coordinator's router reads (WI-059, S8): one row per
    # usable model keyed [PROVIDER]-[MODEL_NAME]-[VERSION], with example rows for
    # the verified headless shapes. Present but INERT until docs/agents-enabled
    # (the ordered enable-list / consent surface, deliberately NOT scaffolded) is
    # created — routing then selects from that pool (process-options.md
    # "Unattended operation" -> routing/escalation). Absent both files = today's
    # single AGENT_CMD/AGENT_MODEL behavior.
    ("agents.template.toml", "docs/agents.toml"),
    # (The gate-policy / push-policy / review-policy / privacy-check / blackout
    # one-word files folded into docs/process.toml at SN-028 — see the
    # process.toml.template row above. Their `*.template` files stay in the kit
    # marked RETIRED, as a HUMAN's reference for the legacy vocabulary when
    # reading an un-migrated adoption. `migrate_legacy_config` does NOT read
    # them: it reads the adopting repo's own `docs/<file>`, so the templates
    # are documentation, not an input.)
    ("STATUS.template.md", "docs/status.md"),
    # The owner decision briefs status.md's Needs-<human> bullets link to
    # (process-options.md "Trajectory / work-items layer"): one OI-N section
    # per pending decision, deleted when the ruling lands in log.md Decisions.
    ("registries/open-items.template.toml", "docs/requirements/open-items.toml"),
    # (SN-029's separate attestation ledger was scaffolded here until it was
    # retired. The anchor it carried moves onto the artifact's own row, so
    # there is no second registry for an adopter to scaffold; the columns
    # arrive in the spine templates with the anchor half.)
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
        "registries/stakeholder-needs.template.toml",
        "docs/requirements/stakeholder-needs.toml",
    ),
    (
        "registries/system-requirements.template.toml",
        "docs/requirements/system-requirements.toml",
    ),
    (
        "registries/low-level-requirements.template.toml",
        "docs/requirements/low-level-requirements.toml",
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
    # registries/work-items.template.csv is deliberately NOT mapped: since the
    # Phase 2c authority flip the work-item registry scaffolds as the docs/work/
    # spec folder below, and the CSV template survives only as the legacy-format
    # reference wi_convert.py migrates from (ADOPTING.md §6).
    # The work-item registry's home (docs/concurrency-restructure.md §2):
    # one Markdown spec per work item, its STATUS encoded as the directory. Ships
    # ADDITIVE beside the CSV — the readers resolve to the folder only once it
    # holds a REAL spec, so a fresh scaffold's CSV stays authoritative and the
    # `-000` example is documentation, exactly like the `-000` row it mirrors.
    # The status directories themselves are created below (GITKEEP_DIRS).
    ("work/WI-000.template.md", "docs/work/queued/WI-000-example.md"),
    # ...and the declaration that makes it green: a work spec is a REGISTRY
    # ENTRY that happens to be Markdown, not a page anyone navigates to, so
    # `docs/work/*` is a declared expected-live-orphan class rather than a wall
    # of check_docs warnings (WI-228's census idiom, one glob with its reason).
    ("orphans-allow.template", "docs/orphans-allow"),
    ("registries/test-cases.template.toml", "docs/test/test-cases.toml"),
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
    # WI-329: trace.py imports its spine-row TEXT layer from this sibling, so a
    # scaffold missing it gets an ImportError on the first check. Copied
    # together, always.
    ("scripts/trace_text.py", "scripts/trace_text.py"),
    # OI-12: the spine's registry CARRIER — the one home
    # for the TOML tier tables, the key->column vocabulary and both readers.
    # Imported by trace.py and check_trajectory.py (and by the rest of the
    # spine readers as they convert), so the trace_text.py rule applies
    # verbatim: a scaffold missing it ImportErrors on the first check.
    ("scripts/spine_carrier.py", "scripts/spine_carrier.py"),
    # The one-shot CSV/markdown -> TOML converter (SR-147). Shipped because
    # EVERY adopting repo migrates too, and the round-trip proof is the
    # migration's evidence — an adopter that cannot run --check has to take the
    # conversion on faith, which is what SR-129's 140-cell lesson forbids.
    ("scripts/migrate_carrier.py", "scripts/migrate_carrier.py"),
    ("scripts/derive_gate.py", "scripts/derive_gate.py"),
    ("scripts/check.py", "scripts/check.py"),
    ("scripts/check_flows.py", "scripts/check_flows.py"),
    ("scripts/check_docs.py", "scripts/check_docs.py"),
    ("scripts/check_doc_refs.py", "scripts/check_doc_refs.py"),
    ("scripts/check_figures.py", "scripts/check_figures.py"),
    ("scripts/check_perf.py", "scripts/check_perf.py"),
    ("scripts/check_stubs.py", "scripts/check_stubs.py"),
    ("scripts/check_coverage.py", "scripts/check_coverage.py"),
    ("scripts/check_privacy.py", "scripts/check_privacy.py"),
    ("scripts/check_vendored.py", "scripts/check_vendored.py"),
    ("scripts/check_trajectory.py", "scripts/check_trajectory.py"),
    # The ready-frontier/safety-classification library (IF-053). Shipped
    # because it is a SIBLING IMPORT of the integration seam, not a nicety:
    # integrate.py's claim refusal ladder and dispatch.py's cycle both
    # `import schedule` UNGUARDED, so a scaffold without it cannot claim work
    # or run the walk-away loop at all (WI-379 — a fresh scaffold raised
    # ModuleNotFoundError from the frontier check). check_trajectory and the
    # dashboard read it too.
    ("scripts/schedule.py", "scripts/schedule.py"),
    ("scripts/subagent_gate.py", "scripts/subagent_gate.py"),
    ("scripts/gen_arch_map.py", "scripts/gen_arch_map.py"),
    ("scripts/gen_release_checklist.py", "scripts/gen_release_checklist.py"),
    ("scripts/gen_cases.py", "scripts/gen_cases.py"),
    ("scripts/gen_trajectory.py", "scripts/gen_trajectory.py"),
    # WI-280 split of gen_trajectory.py: the sibling module(s) it imports and
    # re-exports — copied together, always (the trace_text.py idiom; a scaffold
    # missing one ImportErrors on the first render).
    ("scripts/traj_graph.py", "scripts/traj_graph.py"),
    ("scripts/traj_parse.py", "scripts/traj_parse.py"),
    ("scripts/traj_render.py", "scripts/traj_render.py"),
    ("scripts/traj_views.py", "scripts/traj_views.py"),
    ("scripts/traj_status.py", "scripts/traj_status.py"),
    ("scripts/traj_panels.py", "scripts/traj_panels.py"),
    ("scripts/gen_open_items.py", "scripts/gen_open_items.py"),
    ("scripts/gen_okf.py", "scripts/gen_okf.py"),
    ("scripts/plan_coverage.py", "scripts/plan_coverage.py"),
    ("scripts/plan_round.py", "scripts/plan_round.py"),
    ("scripts/plan_briefs.py", "scripts/plan_briefs.py"),
    # The prompt-template loader + strict single-brace fill (plan §8): every
    # brief the loop sends resolves through it, so it ships wherever
    # agent_loop.py does.
    ("scripts/prompts.py", "scripts/prompts.py"),
    # The adjudicator briefs' evidence assemblers: without it an
    # ADJUDICATE session composes from the worker assignment, which is
    # the WI-424 defect this ships to close.
    ("scripts/adjudicate_brief.py", "scripts/adjudicate_brief.py"),
    ("scripts/plan_coverage_step.py", "scripts/plan_coverage_step.py"),
    ("scripts/plan_artifacts.py", "scripts/plan_artifacts.py"),
    # The work-item registry's CSV <-> spec-folder converter (§2 of
    # docs/concurrency-restructure.md). plan_artifacts imports it as a sibling
    # when the folder home is authoritative, so the two copy together — a
    # scaffold with the filer and not the converter files nothing.
    ("scripts/wi_convert.py", "scripts/wi_convert.py"),
    # The serial trunk step (docs/concurrency-restructure.md §5.1/§5.5): compiles
    # the log fragments in git-derived merge order and re-derives the generated
    # artifacts. Ships with the kit because the rule it enforces — no work branch
    # writes docs/log.md or commits a generated artifact — is the process, not
    # this repo's local habit; its drop-box scaffolds as docs/log.d/ below.
    ("scripts/trunk_step.py", "scripts/trunk_step.py"),
    # The local integrator (concurrency-restructure §1.2, Phase 4): the §2.3
    # claim, the serial fail-closed merge queue over finished claimed branches,
    # and the RULING-6 window audit. The default backend of the one integration
    # flow; the forge backend is the same flow with server-side enforcement.
    ("scripts/integrate.py", "scripts/integrate.py"),
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
    # The scheduling front end (WI-374; renamed drive.py -> dispatch.py with
    # lane.py extracted at WI-381, concurrency-v2 §A4.2): the dispatcher a
    # plain agent-resume launch runs — agent_loop.py imports it as a sibling
    # when no role flag is given. Composes schedule.py / integrate.py / the
    # lane.py worker launch; admission (the §A8 policy table + spine barrier)
    # is its scheduling decision, every other refusal stays where it lives.
    ("scripts/dispatch.py", "scripts/dispatch.py"),
    # One lane's mechanics (WI-381): ensure the lane worktree, launch the
    # worker subprocess, run the §A2 refresh as its own subprocess. dispatch.py
    # imports it unguarded, so a scaffold without it cannot run the loop.
    ("scripts/lane.py", "scripts/lane.py"),
    # The two lane closes that are NOT a merge (WI-387, concurrency-v2 §A3):
    # handback (the work so far committed as-is, the specs back in queued/) and
    # its ruled red arm, quarantine. drive.py imports it unguarded, so a
    # scaffold without it cannot run the walk-away loop at all.
    ("scripts/handback.py", "scripts/handback.py"),
    # The link-aware spec-move ritual (WI-393, rehoming WI-288/WI-353): move a
    # spec and relink the repo in ONE operation. integrate.py's claim and
    # handback.py's return import it unguarded; workers run its CLI for the
    # terminal close moves and the spec-of-record archival.
    ("scripts/spec_move.py", "scripts/spec_move.py"),
    # The unified trunk-side intake mint (WI-388, concurrency-v2 §A5.2;
    # rulings R1/R3): a WI id is created only by a human trunk commit or this
    # helper. integrate.py's post-merge arm and dispatch.py's empty-frontier
    # ladder import it unguarded, so a scaffold without it cannot merge or
    # run the walk-away loop; agent_loop.py imports it lazily (the worker
    # prompt's advisory context block).
    ("scripts/intake.py", "scripts/intake.py"),
    # The WI-218 split of the coordinator engine: the headless session layer,
    # the shared primitives, and the dual-plan runner agent_loop.py imports as
    # siblings. (The parallel dispatcher retired at concurrency-restructure
    # Phase 5; integrate.py is the serial integration seam.)
    ("scripts/agent_session.py", "scripts/agent_session.py"),
    ("scripts/agent_common.py", "scripts/agent_common.py"),
    ("scripts/plan_runner.py", "scripts/plan_runner.py"),
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

GITKEEP_DIRS = [
    "src",
    "tests",
    # The work-item registry's spec-folder home (docs/concurrency-restructure.md
    # §2.1; the six-state vocabulary is WI-384's): STATUS IS THE DIRECTORY, so
    # the directories must exist for the vocabulary to be visible — an empty
    # `deferred/` is what tells a reader parking is a first-class state rather
    # than a convention someone invented, and an empty `cancelled/` beside
    # `complete/` is what says a terminal state has two outcomes and the folder
    # names which. `draft/` must be scaffolded for a second reason beyond
    # visibility: it is a DECLARED status directory, and specs parked in an
    # undeclared one never enter the registry, so the duplicate-id guard and
    # the dashboard go blind to the id a draft holds. (The mint itself reads
    # FILENAMES through an unfiltered walk and is safe either way — measured at
    # WI-384's review.) `queued/` is not listed: the WI-000
    # example spec lands there, so git already tracks it. `active/` holds one
    # subdirectory per claiming branch.
    "docs/work/draft",
    "docs/work/active",
    "docs/work/deferred",
    "docs/work/cancelled",
    # SR-144's third terminal, scaffolded for the same visibility reason: a lane
    # that stopped early closes HERE, not back into `queued/` with a blockref,
    # and an empty `partial/` beside the other two terminals is what tells a
    # reader "stopped early" is a state the process has a name for.
    "docs/work/partial",
    "docs/work/complete",
    # SR-144's per-close reports: one immutable document per non-merged-clean
    # lane close. OUTSIDE docs/work/ deliberately — `spec_files` is an rglob for
    # `WI-*.md` filtered only on "not directly in work_dir", so a report living
    # under docs/work/ would be walked, raise on its undeclared directory, and
    # then be SILENTLY SKIPPED by the registry readers, while its id counted as
    # taken by the mint. The report is the return event's identity; it must not
    # be a half-visible spec.
    "docs/handbacks",
    # The log's fragment drop-box (docs/concurrency-restructure.md §5.1): a work
    # branch writes `docs/log.d/<WI-id>-<slug>.md` — a unique name, so the log
    # stops being a merge-conflict surface — and `scripts/trunk_step.py` compiles
    # the fragments into `docs/log.md` serially, on the trunk. Scaffolded EMPTY,
    # by the same .gitkeep convention as the status directories above: it holds no
    # exemplar because a fragment's whole life is measured in one merge, and a
    # committed example would be compiled into the log by the first trunk step.
    "docs/log.d",
]

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
        # WI-322: the owner decision surface is a fully-generated file, so a
        # MISSING one reads as stale to its freshness gate (the C9 posture its
        # siblings take). Seeding it here is what keeps a fresh scaffold green
        # on its first `check.py` — the scaffolded registry already carries the
        # example rows the status template's Needs-<human> bullets name.
        ["scripts/gen_open_items.py"],
    ):
        if not (dest / rel_cmd[0]).exists() or not (dest / "docs").exists():
            continue
        # `-B`: never write __pycache__ into a fresh scaffold. gen_open_items
        # IMPORTS its sibling generators (one derivation, two renderers), and an
        # import writes bytecode next to the source — which left a
        # scripts/__pycache__/ tree in every new project, with .pyc bytes that
        # differ run to run. Caught by the byte-for-byte scaffold comparison.
        proc = subprocess.run([sys.executable, "-B"] + rel_cmd, cwd=str(dest))
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


KIT_LICENSE_HEADER = (
    "# The license the COPIED KIT FILES carry — Apache-2.0, the full text below.\n"
    "#\n"
    "# Why this file exists: adopting the kit means COPYING it (project-trajectory/\n"
    "# into your repo, its templates scaffolded into docs/). Apache-2.0 §4(a) asks\n"
    "# that anyone who receives those files also receives the License, so bootstrap\n"
    "# drops it here rather than leaving you to fetch it — your repo is\n"
    "# redistributable as-is.\n"
    "#\n"
    "# SCOPE — this covers the kit files you copied, and nothing else. Your own\n"
    "# code, and the artifacts this scaffold produces (your filled registries,\n"
    "# requirements, architecture, log), are YOURS under whatever license your\n"
    "# project chooses. Put that one in your repo's own LICENSE; this file does not\n"
    "# compete with it. If you MODIFY a kit file, §4(b) asks you to say so in that\n"
    "# file — docs/kit-version records which kit commit you started from, which is\n"
    "# what makes the delta visible.\n"
    "#\n"
    "# ATTRIBUTION, per §4(d) — the kit's NOTICE, carried here because a scaffold\n"
    "# is a Derivative Work and this is the 'within the documentation' option:\n"
    "#\n"
    "#     The project-trajectory kit — Copyright 2026 Peter Johnson.   privacy-ok\n"
    "#\n"
    "# (That line carries the `privacy-ok` marker deliberately: a real name is a\n"
    "# LEGAL REQUIREMENT here, not a leak, so a privacy-checked adopting repo must\n"
    "# not red on it. The License text below carries no personal name — the stock\n"
    "# Apache appendix placeholder — so this is the only such line.)\n"
    "#\n"
    "# Generated, like docs/kit-version: rewritten on every scaffold/re-sync.\n"
    "# ---------------------------------------------------------------------------\n"
)


def write_kit_license(dest, dry_run, verb):
    """Write `docs/kit-license` — the kit's own LICENSE text, scoped by a header.

    The kit ships its license INSIDE the portable unit (`project-trajectory/
    LICENSE`) precisely so it survives the copy-in step; a root LICENSE in the
    kit's home repo would not travel. Reports its own outcome (like the other
    stamp writers' callers do) so `main()` stays a straight-line sequence —
    bootstrap's `main` is already the WI-280 decomposition target, and a new
    branch there is debt this step doesn't need to add. Returns True if written."""
    source = KIT / "LICENSE"
    if not source.exists():
        print(
            "WARNING: the kit has no LICENSE file, so docs/kit-license was NOT "
            "written — this scaffold carries no record of the terms the copied "
            "kit files are under. Restore project-trajectory/LICENSE and re-run.",
            file=sys.stderr,
        )
        return False
    print("  {}: docs/kit-license (Apache-2.0, kit files only)".format(verb))
    if dry_run:
        return False
    target = dest / "docs" / "kit-license"
    target.parent.mkdir(parents=True, exist_ok=True)
    _write_text_lf(target, KIT_LICENSE_HEADER + source.read_text(encoding="utf-8"))
    return True


# --- main() decomposed into phases (WI-280 slice 10, subsuming the retired
# WI-082) ------------------------------------------------------------------
#
# `main()` was a 380-line straight-line script at complexity 41 — the largest
# single function in the kit and the one every adopter's FIRST command runs.
# The phases below are the script's own paragraphs given names and a typed
# hand-off; nothing about the scaffold changes, which is the point: every print
# is byte-identical and in the same order, proven by the scaffold byte-compare
# suites (test_bootstrap / test_profile / test_stack_profile) and by a
# pre/post `--dry-run` diff. The two records carry what the paragraphs used to
# pass through a dozen locals.


@dataclass(frozen=True)
class ScaffoldPlan:
    """Everything the resolution ladders decided, before a byte is written:
    the declared profile (stack/omit), the agent layer, the three declared
    policies, and the two write modes. Frozen — a phase reads the plan, it
    never re-decides."""

    stack: str
    omit: frozenset
    agent_choice: str
    agents: list
    domain: str
    skills: list
    gate_policy: str
    push_policy: str
    privacy_check: str
    force: bool
    dry_run: bool


@dataclass
class CopyOutcome:
    """What the copy phases did, accumulated across them: `created` is the
    ordered report list (later phases append to it — the report prints it in
    that order), `skipped` the write-once hits, `missing` the absent templates
    that make the run exit 1."""

    created: list
    skipped: list
    missing: list


def build_parser():
    """The CLI surface. Its own function so `main()` reads as a sequence of
    phases and the flag set can be inspected without running a scaffold."""

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
        "--migrate-config",
        action="store_true",
        help="SN-028: fold every legacy one-word policy file (docs/gate-policy, "
        "docs/push-policy, docs/review-policy, docs/privacy-check, "
        "docs/secrets-scan, docs/privacy-review, docs/guardrails-policy, "
        "docs/blackout) into docs/process.toml and DELETE it, then exit. "
        "Idempotent. A full scaffold pass runs this for you; the flag is for a "
        "repo that wants the conversion WITHOUT a re-sync.",
    )
    ap.add_argument(
        "--gate-policy",
        choices=GATE_POLICY_CHOICES,
        default=None,
        help="declared gate authority, written to docs/process.toml "
        "[attestation] gate_policy (process.md §4): "
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
    return ap


def resolve_profile(ap, args, dest):
    """`(stack, omit)` — the scaffold profile (Thread 34): explicit flags win;
    else the destination's recorded docs/kit-profile (so a re-sync regenerates
    the same structural choices instead of silently reverting them); else ASK
    for the stack on an interactive TTY / take the do-nothing defaults."""
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
    return stack, omit


def resolve_choices(args, stack, omit):
    """The consent-first ladders — agent layer, domain/skills, and the three
    declared policies — resolved into one `ScaffoldPlan`. Each follows the same
    rule: an explicit flag wins; else ASK on an interactive TTY; else the
    do-nothing default (CI-safe, and the scaffolded file already says it)."""
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
    return ScaffoldPlan(
        stack=stack,
        omit=omit,
        agent_choice=agent_choice,
        agents=agents,
        domain=domain,
        skills=skills,
        gate_policy=gate_policy,
        push_policy=push_policy,
        privacy_check=privacy_check,
        force=args.force,
        dry_run=args.dry_run,
    )


def _write_scaffold_file(src, dst, src_rel, dst_rel, dest, plan):
    """Write ONE mapped file into the scaffold: the per-suffix generation rule,
    the template meta-prose rewrites, the README's one placeholder, and the
    POSIX executable bit. Its own function (WI-280 slice 10) so `copy_kit_files`
    is the write-once LEDGER — which file, and whether — and this is the writing."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.suffix == ".md":
        # Markdown templates are GENERATED, not copied: drop kit-only
        # regions, keep or stub profile regions per the resolved profile.
        _write_text_lf(
            dst, strip_markers(src.read_text(encoding="utf-8"), plan.omit, src_rel)
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


def copy_kit_files(dest, plan):
    """The MAPPING copy pass + the GITKEEP_DIRS placeholders, as a
    `CopyOutcome`. Write-once by default (an existing file is skipped, not
    overwritten); `--force` overwrites; `--dry-run` reports without writing."""
    created, skipped, missing = [], [], []
    for src_rel, dst_rel in MAPPING:
        src = KIT / src_rel
        dst = dest / dst_rel
        # Stack-gated artifacts (Thread 34, R7/C3): an explicitly non-Python
        # stack gets no dead Python artifacts — the rewiring checklist lands
        # in docs/status.md instead (append_stack_checklist below).
        if dst_rel == "pytest.ini" and plan.stack in NON_PYTHON_STACKS:
            continue
        if not src.exists():
            missing.append(src_rel)
            continue
        # WRITE-ONCE, and `--force` does not override it for the watermark. Every
        # other target here is a template to fill or is regenerable from the tree,
        # so re-forcing costs at most re-doing an edit. `docs/id-watermark` is the
        # only file whose content is HISTORY — which ids have been allocated and
        # DELETED — so replacing a live repo's marks with the fresh-scaffold ones
        # frees every id above them for silent re-use, and nothing in the tree can
        # rebuild what was lost.
        if dst.exists() and (
            not plan.force or Path(dst_rel).name == WATERMARK_DEST_NAME
        ):
            skipped.append(dst_rel)
            continue
        if plan.dry_run:
            created.append(dst_rel)
            continue
        _write_scaffold_file(src, dst, src_rel, dst_rel, dest, plan)
        created.append(dst_rel)

    for d in GITKEEP_DIRS:
        keep = dest / d / ".gitkeep"
        if keep.exists():
            skipped.append("{}/.gitkeep".format(d))
        elif plan.dry_run:
            created.append("{}/.gitkeep".format(d))
        else:
            keep.parent.mkdir(parents=True, exist_ok=True)
            _write_text_lf(keep, "")
            created.append("{}/.gitkeep".format(d))
    return CopyOutcome(created, skipped, missing)


def apply_stack_extras(dest, plan, outcome):
    """The declared stack's two follow-ups: the harness-rewiring checklist a
    non-Python scaffold owes, and the stack-neutral arch-map mode."""
    # A non-Python stack's remaining hand-edits become visible Open-items
    # bullets in the fresh status.md (only on the run that created it — a
    # re-sync must never re-append into a repo's own working surface).
    if (
        plan.stack in NON_PYTHON_STACKS
        and "docs/status.md" in outcome.created
        and append_stack_checklist(dest, plan.stack, plan.dry_run)
    ):
        print(
            "  appended the {} harness-rewiring checklist to docs/status.md "
            "(Open items OI-3..OI-6)".format(plan.stack)
        )
    if seed_arch_map_mode(dest, plan.stack, outcome.created, plan.dry_run):
        print(
            "  set docs/stack.ini [arch-map] mode = files (stack-neutral code "
            "map until a {} symbol-level generator is ported — "
            "ADOPTING.md §3)".format(plan.stack)
        )


def materialize_agent_layer_phase(dest, plan, outcome):
    """The chosen agent's layer: its matched skills into the native skills dir
    + the inert hook example, the curated knowledge packs, and the launcher
    seed. "none" (the non-interactive default) adds nothing, so the historical
    scaffold is byte-for-byte unchanged."""
    outcome.created.extend(
        materialize_agent_layer(
            dest, plan.agents, plan.skills, plan.dry_run, plan.force
        )
    )
    outcome.created.extend(
        materialize_knowledge_packs(dest, plan.domain, plan.dry_run, plan.force)
    )

    # Seed the fresh agent-resume launchers' AGENT_CMD slot with the chosen
    # agent's example command (never on a re-sync that skipped them).
    if seed_agent_resume(dest, plan.agents, outcome.created, plan.dry_run):
        print(
            "  seeded agent-resume launchers for {} (AGENT_CMD carries the "
            "permission-bypass flag — filling/keeping it is your consent to "
            "unattended sessions; see docs/process-options.md).".format(plan.agents[0])
        )


def apply_declared_policies(dest, plan, outcome):
    """The three declared authorities: a non-default level overwrites the key
    docs/process.toml just scaffolded (SN-028) and says so.

    Runs the LEGACY CONVERTER first. On a fresh scaffold that is a no-op; on a
    re-sync onto a repo that predates SN-028 it is what keeps the hard
    mixed-config refusal from ever reaching a human — the legacy files are
    folded in and deleted before anything reads a policy.
    """
    moved, notes = migrate_legacy_config(dest, plan.dry_run)
    for rel in moved:
        print("  migrated into docs/process.toml (SN-028): {}".format(rel))
    for note in notes:
        print("  NOTE: {}".format(note))

    # A declared non-default gate authority overwrites the scaffolded default
    # and lays down the deviation-register skeleton for the level.
    for rel in apply_gate_policy(dest, plan.gate_policy, plan.dry_run):
        if rel not in outcome.created:
            outcome.created.append(rel)
    if plan.gate_policy != "attended":
        print("  gate-authority level: {}".format(plan.gate_policy))

    # A declared non-default push authority overwrites the scaffolded default
    # (the file itself was just copied with `human` on its value line).
    if plan.push_policy != "human":
        apply_push_policy(dest, plan.push_policy, plan.dry_run)
        if PROCESS_TOML_REL not in outcome.created:
            outcome.created.append(PROCESS_TOML_REL)
        print("  push policy: {}".format(plan.push_policy))

    # A `true` privacy-check overwrites the scaffolded default (`false`) — set
    # at repo creation, the cheap moment.
    if plan.privacy_check and plan.privacy_check != "false":
        apply_privacy_check(dest, plan.privacy_check, plan.dry_run)
        if PROCESS_TOML_REL not in outcome.created:
            outcome.created.append(PROCESS_TOML_REL)
        print("  privacy-check: {}".format(plan.privacy_check))


def report_outcome(plan, outcome):
    """The per-file report + the one-line summary, in the order the phases
    appended to it."""
    verb = "would create" if plan.dry_run else "created"
    for c in outcome.created:
        print("  {}: {}".format(verb, c))
    for s in outcome.skipped:
        print("  skipped (exists): {}".format(s))
    for m in outcome.missing:
        print("  WARNING missing template: {}".format(m), file=sys.stderr)

    print(
        "\n{} file(s) {}, {} skipped.".format(
            len(outcome.created),
            "to create" if plan.dry_run else "created",
            len(outcome.skipped),
        )
    )


def write_stamps(dest, plan):
    """The generated stamps — kit-version / kit-profile / kit-license — plus
    the agent-choice note in docs/status.md."""
    verb = "would create" if plan.dry_run else "created"
    # docs/kit-version + docs/kit-profile are generated stamps, not user
    # content, so they are always (re)written — refreshed on every
    # scaffold/re-sync to record the kit state + profile this run came from.
    label, dirty, wrote = write_kit_version(dest, plan.dry_run)
    print("  {}: docs/kit-version ({})".format(verb, label))
    write_kit_profile(dest, plan.stack, plan.omit, plan.dry_run)
    print(
        "  {}: docs/kit-profile (stack={}; omit={})".format(
            verb, plan.stack, ",".join(sorted(plan.omit)) or "none"
        )
    )
    write_kit_license(dest, plan.dry_run, verb)
    if dirty:
        print(
            "WARNING: the kit working tree is DIRTY — this scaffold is stamped "
            "{} and cannot be reproduced or cleanly diffed later. Re-sync only "
            "from a committed kit state (commit the kit, then re-run).".format(label),
            file=sys.stderr,
        )

    # Record the agent choice + date + materialized skills in docs/status.md so
    # the scaffolded repo carries the setup decision (AGENTS.md stays canonical).
    if record_agent_choice(dest, plan.agent_choice, plan.skills, plan.dry_run):
        print(
            "  {}: docs/status.md agent-setup note ({})".format(verb, plan.agent_choice)
        )


def run_migrate_config(dest, dry_run):
    """The `--migrate-config` report (SN-028). Its own function so `main` keeps
    its complexity baseline — the same reason `sync_agent_skills` has one."""
    moved, notes = migrate_legacy_config(dest, dry_run)
    verb = "would migrate" if dry_run else "migrated"
    for rel in moved:
        print("  {}: {}".format(verb, rel))
    for note in notes:
        print("  NOTE: {}".format(note))
    print(
        "\n{} legacy policy file(s) {} into docs/process.toml.".format(
            len(moved), "to migrate" if dry_run else "folded"
        )
    )


def main():
    _utf8_console()
    ap = build_parser()
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

    # --migrate-config (SN-028): a FOCUSED conversion of the legacy one-word
    # policy files into docs/process.toml, nothing else — kept separate from the
    # full scaffold pass for the same reason --sync is, so an existing repo can
    # take the migration without re-stamping kit-version or re-running the
    # generators. The scaffold pass runs the same function. Extracted from
    # `main` rather than inlined: `main` sits at the C901 ratchet's edge and the
    # ratchet's standing instruction is to simplify, never to bump.
    if args.migrate_config:
        run_migrate_config(dest, args.dry_run)
        return

    stack, omit = resolve_profile(ap, args, dest)
    plan = resolve_choices(args, stack, omit)

    if not dest.exists():
        if plan.dry_run:
            print("would create destination directory:", dest)
        else:
            dest.mkdir(parents=True)

    outcome = copy_kit_files(dest, plan)
    apply_stack_extras(dest, plan, outcome)
    materialize_agent_layer_phase(dest, plan, outcome)
    apply_declared_policies(dest, plan, outcome)
    report_outcome(plan, outcome)
    write_stamps(dest, plan)

    if not plan.dry_run:
        initialize_generated_docs(dest, outcome.created)
    if not plan.dry_run and outcome.created:
        print(
            "Next: fill the PROJECT BRIEF in AGENTS.md + docs/status.md, then "
            "run gate G1 (docs/process.md)."
        )
    if outcome.missing:
        sys.exit(1)


if __name__ == "__main__":
    main()
