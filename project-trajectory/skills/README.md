# Skills — portable accelerators (opt-in, per-agent materialized)

Agent-neutral **skill** definitions the kit ships, plus the contract for adding
more. A *skill* is a small, focused capability — a repeatable procedure grounded
in this repo's actual commands and files — that an agent loads on demand to work
faster and more correctly. Skills are **opt-in accelerators, not process gates**:
the gates, the traceability spine, and the git/CI floor are the bar (see
[`../PROCESS.md`](../PROCESS.md)); a skill just helps an agent clear it. A repo
with no agent, or an agent that ignores them, loses nothing.

This is the resolution of the Thread-15 *"agent selection & auto-provisioning"*
parked follow-on (IMPROVEMENT_PLAN.md) and the scratch *"what AI skills should the
template make available"* open item: at **repo setup** the user most likely has an
agent configured, so bootstrap can ask which one and bring that agent's skills
into the repo fold — without locking the kit to any agent (the source format
below stays neutral).

## Source format (agent-neutral) → native materialization

Each skill is a directory holding a **`SKILL.md`** whose YAML frontmatter carries
both the **agent-facing fields** and this kit's **applicability metadata** for
discovery:

```
skills/
  <skill-name>/
    SKILL.md          # frontmatter + concise, imperative body
  INDEX.csv           # generated scan surface (see below)
```

`SKILL.md` frontmatter contract:

```yaml
---
name: byte-budget-guard              # required; lowercase-hyphen; == dir name
description: One sentence...          # required; when the agent should use it
stacks: [python, powershell, any]     # applicability: primary stacks it helps
domains: [any]                        # web|game|hardware|data|any
phases: [dev, gate]                   # setup|dev|gate|release
tags: [byte-budget, agents-md]        # freeform, lowercase-hyphen
scope: this-repo                      # this-repo | kit  (see split below)
---
```

- **`name` + `description`** are the fields both **Claude Code** and **Gemini
  CLI** read from `SKILL.md` frontmatter — the same
  [Agent Skills](https://code.claude.com/docs/en/skills) open-standard shape, so
  one neutral source materializes to either agent unchanged.
- **`stacks` / `domains` / `phases` / `tags`** are this kit's *applicability
  schema* — the discovery metadata the matcher (below) and `INDEX.csv` use.
  `any` in a list means "applies regardless of that axis". Closed vocabularies:
  `stacks ∈ {python, node, go, rust, powershell, any}` (`node` is the one
  JS/TS label), `domains ∈ {web, game, hardware, data, any}`,
  `phases ∈ {setup, dev, gate, release}`; `tags` is freeform.
- **`scope`** is `kit` (generic to any adopted repo — shipped and materialized on
  scaffold) or `this-repo` (maintains *this* template's own attributes — kept in
  the kit as a reference/dogfood source, **not** materialized downstream).

### Where a selected skill lands

Bootstrap materializes each **selected** skill into the chosen agent's native
skills location, copying the neutral `SKILL.md` verbatim:

| Agent | Native location | Selector |
|---|---|---|
| Claude Code | `.claude/skills/<name>/SKILL.md` | `--agents claude` |
| Gemini CLI | `.gemini/skills/<name>/SKILL.md` (workspace skill) | `--agents gemini` |
| Codex | `.agents/skills/<name>/SKILL.md` (its AGENTS.md-mirror dir) | `--agents codex` |

All three adopted the **same Agent-Skills standard**, so materialization is a
straight copy into the agent-specific directory — no per-agent rewrite. If a
future agent has *no* skills equivalent, it simply gets none (its stub +
`AGENTS.md` still stand); the neutral source stays ready for when it does.

### Checked fan-out: one source, many copies, no drift (S7)

The per-agent dirs hold **byte-identical** copies of the one neutral source —
they differ only because agent skill *locations* don't standardize (the same
reason the kit keeps separate hook configs). To stop them rotting:

- **Refresh is one command.** Materialization is write-once (never clobbers
  project content); `bootstrap.py --sync` force-overwrites **only** each
  `<agent>/skills/<name>/` subtree from source — "edit source → re-materialize".
- **Drift is gated.** `gen_skills_index.py --check-agents` byte-compares every
  per-agent copy to source and **fails** on a divergence (with the `--sync` fix),
  wired into the pre-commit floor + DevStg-Impl like the arch-map/OKF freshness gates.
  Vacuous for a repo with no neutral source or no per-agent dir; only skills a
  per-agent dir already carries are compared, so a scope-matched subset is fine.
- **Tracked + gated.** The copies are committed (a fresh clone has working skills
  before setup runs), the kit's idiom for committed generated artifacts.
- **Tenability constraint:** verbatim fan-out holds only while **skill
  frontmatter stays agent-neutral**. The day a skill needs an agent-specific
  field, materialization gains a per-agent transform and the tracking model flips
  to gitignore + regenerate-on-setup (tracking *transformed* artifacts invites
  the hand-edits the kit exists to prevent). Deferred until a real need earns it.

## The generated index

`INDEX.csv` is a flat scan surface (one row per skill: `name, scope, stacks,
domains, phases, tags, description`) so humans and tools read applicability
cheaply without opening every `SKILL.md` — the same "generated, don't
hand-maintain" stance as the registries and the code map. Regenerate it with:

```
python scripts/gen_skills_index.py            # in the kit root
```

The generator is the source of truth for the index; a stale `INDEX.csv` is a
finding (`--check` exits nonzero), like `gen_arch_map.py --check`.

## The matcher (deliberately trivial)

At scaffold time `bootstrap.py` asks up to three scope questions (primary stack?
domain? binary-assets/hardware involved?) and selects the **`kit`-scope** skills
whose applicability **intersects** the answers — plain tag intersection, no
ranking, no engine. `any` matches everything. The **metadata convention is the
deliverable, not the matcher**: the schema + index are what let a *later* tool do
something smarter; the built-in matcher stays a one-function set-intersection.

Non-interactive/CI runs never prompt: with `--agents none` (the default) nothing
is materialized. With an explicit agent flag and no domain choice, only
`domains: [any]` kit skills materialize; domain-specific skills and knowledge
packs require an explicit matching `--domain` opt-in.

## Future external skill sources (the plug-in contract)

So a later tool can fetch remote/community skills without a redesign, any
external source must honor this contract:

1. **Shape.** A fetched skill is a directory named `<skill-name>/` containing a
   `SKILL.md` with the frontmatter above (`name` == dir name; `name` +
   `description` required; the applicability keys present, using the closed
   vocabularies or `any`). A skill missing the applicability keys is treated as
   `stacks:[any], domains:[any], phases:[dev]` — usable, but it won't be
   auto-selected by a specific-scope match.
2. **Naming.** `name` is lowercase-hyphen and unique within the destination;
   a fetched skill whose name collides with a shipped one is renamed
   `<source>-<name>`, never silently overwritten.
3. **Landing zone.** Fetched skills land in the **same kit `skills/` source
   layout first** (neutral), then materialize to the agent dir via the same
   bootstrap path — so a remote skill is indexed and matchable exactly like a
   shipped one. They are **never** written straight into `.claude`/`.gemini`
   bypassing the index.
4. **Trust.** A skill is instructions an agent will follow — treat a fetched one
   as untrusted input: it is materialized only on explicit selection, never
   auto-run, and its body is reviewable text in the repo (diffable in the PR that
   adds it).

The kit ships both universal process skills and curated domain skills. Domain
skills materialize only when their `domains` metadata intersects the adopter's
explicit `--domain` choice; `--domain any` keeps them out. The generated
[`INDEX.csv`](INDEX.csv) is the complete shipped inventory. The fetch mechanism
itself is a future tool that plugs in here — the convention is what makes it
possible now.

A **curated, evaluated starting list** of real external sources — each with its
license, format, and trust caveats spelled out, under a *mine-don't-install*
posture — lives in [`EXTERNAL_SKILLS.md`](../EXTERNAL_SKILLS.md).

## Shipped skills

| Skill | Scope | Purpose |
|---|---|---|
| `byte-budget-guard` | this-repo | Check `AGENTS.template.md` / `PROCESS.md` sizes against their budgets before and after an edit. |
| `session-protocol` | this-repo | Run a WI/thread session by this repo's conventions: read plan → execute → gates → session log → commit style. |
| `registry-hygiene` | kit | Run `trace.py`/`check.py` with the right flags; read orphan/schema findings and fix them. |
| `downstream-resync` | kit | Walk `ADOPTING.md` §6 to upgrade an adopted repo to kit HEAD. |
| `gate-advance` | kit | Move DevStg-Reqs→DevStg-Tests→DevStg-Impl honestly — including `Attest` usage and attested-vs-mechanized reporting. |
| `antidote` | kit | Root-cause-vs-patch review at the single fix in front of you — the per-fix companion to `PROCESS.md` §3's consolidation doctrine. Vendored (OI-58, WI-507; source + ledger row in `docs/dependencies.md`), not authored here. |

The curated domain library adds web/rendering/model-inference skills for `web`,
robotics/perception/simulation skills for `hardware`, and cross-domain skills
where the applicability metadata names more than one domain. Skills tagged
`domains: [any]` are intentionally universal and remain part of the safe base
set. Read `INDEX.csv` rather than duplicating that evolving inventory here.

**Split rationale.** `registry-hygiene`, `downstream-resync`, and `gate-advance`
are **`kit`-scope**: every adopted repo runs the same registries, gates, and
re-sync path, so they help any downstream project and ship + materialize. The
`byte-budget-guard` and `session-protocol` are **`this-repo`-scope**: the specific
byte budgets and the IMPROVEMENT_PLAN WI/thread session ritual are *this*
template's own maintenance attributes, meaningless in an adopted product repo —
so they are dogfooded into this repo's `.claude/skills/` and kept as reference
sources here, but **not** materialized by a downstream scaffold.
