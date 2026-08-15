# The LLM re-sync pack (bringing an adopted repo forward to a newer kit)

**Who reads this:** an LLM agent (or a human) carrying a repo that adopted this
kit at some earlier commit forward to a newer one. It is the single home for the
re-sync *rules* — the file classes, the per-change migration entries, the
concept renames. `ADOPTING.md` §6 frames the job and points here; the
`downstream-resync` skill sequences it and points here. **If a rule is wrong,
fix it here** — there is no second copy to keep in step.

<!-- check_vocab: allow-file — this pack is the DECLARED home of every concept
rename the kit has shipped, so it necessarily spells out retired vocabulary on
both sides of each arrow (§4 is literally the translation table). Exempting the
whole file is correct here and correct nowhere else: an entry that could not name
what it replaces would be useless to the reader it exists for. -->


**Where this lives, and which copy to read.** This is a kit reference doc
(`project-trajectory/RESYNC_PACK.md`), like `ADOPTING.md` and `EXAMPLE.md` — it
is **not** scaffolded into an adopting repo, deliberately. A copy frozen in your
repo at adoption time would be missing exactly the entries you need (the ones
added since), and a re-sync doc that is stale on the day it matters is worse than
no doc. So read the pack **from the kit checkout you are syncing TO** — the same
checkout you are diffing against, which this procedure already requires you to
have.

**The one anchor you have** is `docs/kit-version` in the adopting repo: the kit's
short SHA + date that bootstrap stamped there. Every entry in §3 and §4 below
carries `[since <sha>]` — the kit commit at which the change landed. That is what
makes range selection mechanical rather than a 40-entry read: your stamp's SHA to
your target SHA is a range, and an entry applies when its `since` SHA is **in**
that range. See §5 for what happens when the entries stop being prose.

---

## 1. The procedure

Bounded on purpose: this is what to read, in what order, and where the judgement
sits. Do not improvise a wider sweep — the deviation review in §2 is the sweep.

### 1.1 Establish the range

1. Read `docs/kit-version` — the kit short-SHA + date this repo was last
   scaffolded or re-synced from — and `docs/kit-profile`, the structural choices
   (stack + omitted sections) its process docs were *generated* with.
2. **If the stamp reads `unknown (kit not a git checkout)`**, the repo was
   scaffolded from a tarball and has **no anchor**. Do not guess a range.
   Reconstruct one from artifacts: which scripts and docs the repo actually has,
   which registry carriers are live, which columns its registries carry. Each §3
   entry names the artifacts its change creates or moves, so the entries
   themselves are the probe list. Treat the whole of §3 as potentially applicable
   and re-stamp honestly at the end.
3. Choose the target kit commit. **Sync only from a committed kit state**, never
   a dirty kit tree: bootstrap stamps `<sha>-dirty` and warns, and a dirty stamp
   is unreproducible and cannot be diffed later.
4. Diff the recorded SHA against the target *before touching anything*, so the
   moves below are driven by what actually changed rather than by this document's
   full length.
5. While the diff is open, recheck the **new capability surface** across the
   range — new or updated skills (`skills/INDEX.csv`), opt-in layers added to
   `process-options.md`, new vendorable packs (guardrails / efficiency /
   knowledge). An upgrade that only takes script fixes leaves accelerators on the
   table (`ADOPTING.md` §6).

### 1.2 The judgement this pack does NOT make for you

`SR-036` declares the overwrite-vs-preserve call **`verification = "Inspection"`**
— one of a handful of non-Test requirements in the kit's own spine — because it
rests on a fact no tool holds: *did the adopter edit this file, and does their
edit still mean something under the new kit?* This pack bounds what you look at
and states the default class for every kit-owned path. **It does not decide a
file you have edited.** Where §2's class and your local edit disagree, that is a
decision for the operator, recorded in the re-sync commit — not something to
resolve by taking the kit's copy because it is newer.

### 1.3 The order of moves

1. **Legacy one-word policy files first.** If the repo still carries them under
   `docs/`, fold them into `docs/process.toml` **before running anything else** —
   running with both homes live is *refused*, not resolved by precedence. §3
   entry *One policy home* has the command.
2. **Then a plain `bootstrap.py --dest .` re-run.** This is **ADD-ONLY**: it
   creates the files the repo lacks, updates **nothing** it already has, and
   never deletes a script the kit has since retired. It is the safe first move,
   not the whole move.
3. **Then the deviation review** (§2) over the changed files: overwrite,
   regenerate, re-apply dials, or preserve — per file, per its class.
4. **Then the applicable §3 entries**, oldest first. They cover what a file copy
   cannot: registry conversions, renamed or deleted scripts you must remove by
   hand, config folds, and state you must reconcile before a derived value is
   trustworthy. Where two entries touch the same artifact, the later one may
   *supersede* the earlier — each such pair says so in its text.
5. **Then the translation helper** (§4) for any concept your own prose, scripts,
   CI or registry cells still spell the old way.
6. **Re-stamp last.** Re-run bootstrap to refresh generated pieces (it re-stamps
   `docs/kit-version` + `docs/kit-profile`), refresh materialized per-agent
   skills with `bootstrap.py --dest . --sync` (scope guarantee: `--sync`
   force-overwrites ONLY the `<agent>/skills/…` subtrees, nothing else — the
   `skills-sync` gate flags a drifted copy), and commit the stamps as the
   **last** step so the record reflects the state you actually landed on.

### 1.4 Verify — and why a green can lie

Run the harness (`scripts/check.py` / `check.{sh,ps1}`) and `scripts/check_docs.py`.
A re-sync that leaves the harness red is not done.

**A green is only as new as your checkers.** If step 3 left any kit-owned script
un-updated, the repo is being judged by the OLD one — which cannot see what the
new kit refuses. This is measured, not hypothetical: on a three-week range, an
add-only re-sync leaves the spine registries under **both** carriers, a state the
current kit hard-refuses, and the surviving old `trace.py` passes it
(`tests/test_old_kit_resync.py` pins exactly this). Before believing the green,
run the **target** kit's checkers against your tree —
`python <kit>/scripts/trace.py --strict` from your repo root — and treat any
disagreement between the two as the list of moves step 3 still owes.

---

## 2. The file-by-file deviation review

### 2.1 The inventory

`bootstrap.py`'s `MAPPING` list is the authoritative inventory of every file the
kit places in an adopting repo: each row is `(source in the kit, destination in
your repo)`. Read it from the **target** kit — it is the file list for this
review, and it is generated-by-being-executable rather than a hand-kept table
that can rot. The kit checkout you are diffing against carries the reference copy
of every source in it, so "what should this file look like?" is always answerable
by reading, never by inference.

Walk the destinations, not your whole tree: a path that is not a MAPPING
destination is yours, and no re-sync rule applies to it.

### 2.2 The four classes

- **Overwrite freely (kit-owned; you don't hand-edit these).** The process
  scripts under `scripts/` (`trace.py`, `derive_gate.py`, `check_docs.py`,
  `check_flows.py`, `check_perf.py`, `check_privacy.py`, `gen_arch_map.py`,
  `gen_*`, `agent_loop.py`), the git hooks (`.githooks/pre-commit`,
  `.githooks/commit-msg`, `.githooks/pre-push`), `pytest.ini` markers, and
  **`scripts/check.py`**. `check.py` is safe to take wholesale because your whole
  toolchain lives in `docs/stack.ini` — the format/lint/test commands **and any
  project-specific gates, as `[step:<name>]` sections** — not in `check.py`. (If
  you still have a hand-added step inside a pre-`[step:]` `check.py`, move it into
  a `[step:<name>]` section once and it survives every re-sync after.) Diff before
  committing anyway, so a kit change you disagree with doesn't land unread.
- **Regenerate, never raw-copy (kit-owned but generated).** `docs/process.md` +
  `docs/process-options.md` are *generated* from the kit masters per the recorded
  `docs/kit-profile`. Raw-copying `PROCESS.md`/`PROCESS_OPTIONS.md` over them
  would ship the masters' `kit-only`/`profile` marker comments, the copy-me
  meta-prose, and any sections your repo opted out of. To take the new versions:
  **delete the two files, then re-run `bootstrap.py --dest .`** — it re-reads
  `docs/kit-profile` (explicit `--stack`/`--omit` flags override it), regenerates
  them with the same structural choices, and re-stamps `kit-version` +
  `kit-profile`.
- **Overwrite, then re-apply your dials (kit-owned, but hand-edited).**
  `docs/process.toml` — the one home for every process dial (gate authority, the
  human-ratification level, push authority, the reviewer count, the privacy and
  secrets gates, guardrails, the blackout window). Unlike `docs/stack.ini` it is
  **kit-owned**: its explanatory header and its key set come from
  `process.toml.template`, so take the kit's version on re-sync and re-apply your
  non-default values in the same commit — by hand, or by re-running the scaffold
  pass with `--gate-policy` / `--push-policy` / `--privacy-check`, which rewrite
  one key in place instead of replacing the file. `--force` **rewrites the whole
  file and resets every dial to the kit defaults**; never aim it at a live repo
  without a diff pass.
- **Preserve always (yours; the kit only seeds them).** `docs/stack.ini` (your
  declared toolchain — the kit seeds the Python reference once and never
  re-touches it; its `[generated]` section, the integrator's auto-resolution
  allowlist, is likewise project-owned), every registry — the four spine TOMLs
  (`docs/requirements/stakeholder-needs.toml`, `system-requirements.toml`,
  `low-level-requirements.toml`, `docs/test/test-cases.toml`) plus the off-spine
  registries that did not move carrier, and their legacy `.md`/`.csv` forms in a
  repo that has not run `migrate_carrier` yet — the `docs/work/` WI spec folder,
  `docs/status.md`, `docs/log.md`, `docs/plan.md` (your work plan — the kit seeds
  the block-list skeleton once), `docs/iteration/` + `docs/iteration_index.md`
  (session history), `docs/architecture.md`'s hand-written overview (regenerate
  only the marker blocks), `AGENTS.md` project content, the root launchers' EDIT
  slots, `docs/gate`, and `.gitignore`/`.gitattributes` (merge new kit lines in by
  hand). `bootstrap.py` **skips existing files**, so a plain re-run won't clobber
  these — but don't run it with `--force` against a live repo without a diff pass.

Two classes have **exceptions that an entry states**, and the entry wins: a §3
entry may invert a standing rule for one file (the clearest case is a migration
that requires `docs/gate` to be **regenerated** rather than preserved). Read the
applicable entries before applying the classes, not after.

### 2.3 Set-together files

Some kit-owned files only work as a **set** — take a newer hook with an older
`check.py` and every commit fails on a step that doesn't exist
(`check: no step named '<x>'`). Never re-sync one half of a set:

- `.githooks/pre-commit` + `scripts/check.py` — every entry that adds a harness
  step (`skills-sync`, `okf`, `trajectory-map`, `derived-gate`) names this.
- `scripts/trace.py` + `scripts/trace_text.py` — an `ImportError` on first check
  otherwise, not a quiet degradation.
- `scripts/spine_carrier.py` with `trace.py`, `check_trajectory.py`,
  `check_docs.py`, `trunk_step.py` and `agent_route.py`.
- `scripts/gen_trajectory.py` + the six `traj_*` renderers.
- The work-item vocabulary set: `check_trajectory.py`, `schedule.py`,
  `agent_common.py`, `wi_convert.py`, `gen_trajectory.py` + `traj_*`,
  `bootstrap.py` — the loaders, scheduler, converter and dashboard must share one
  status vocabulary.

`bootstrap.py` copies each set together; a hand-managed re-sync must too.

### 2.4 The per-file walk

For each MAPPING destination that the range changed:

1. Does the file exist in your repo? If not, the add-only re-run already created
   it — read it and move on.
2. Which class (§2.2) is it in, and does an applicable §3 entry override that
   class for this file?
3. Does your copy differ from the kit's copy at your **recorded** SHA? If it does
   **not**, you never edited it — take the kit's new version outright.
4. If it does differ, that difference is your edit. Re-apply it on top of the new
   version, or record why you are dropping it. This is the SR-036 judgement
   (§1.2); it is the only step of this review that is not mechanical.
5. Is it in a set (§2.3)? Then move the whole set in the same commit.

---

## 3. What changed over time

Every entry is anchored: `[since <sha>]` is the kit commit at which the change
landed, so an entry applies when that SHA falls inside your stamp-to-target
range. Entries are ordered **oldest first** — apply them in that order.

### The TC `Tier` column [since af852db7]

Adoptions created `docs/test/test-cases.csv` before the `Tier` column existed.
`trace.py --strict-schema` requires `Tier` as a non-empty field (it validates the
full TC schema at DevBar-Release). Migration is mechanical: add a `Tier` column and set a
default of `Full`; mark hardware/network/interactive cases `Release` so they
don't run on unattended CI. Once the column is present, `--strict-schema` also
validates that values are in `{Smoke, Full, Release}`, so tighten any free-text
entries at the same time.

### UN → SN id-tier rename (User Need → Stakeholder Need) [since 3ea00aa5]

The top tier was renamed. **Keep the id *numbers* — only the prefix changes**
(`UN-014` → `SN-014`); renumbering would break every back-link. Recipe: rename
the file reference and the prefix in the stakeholder-needs registry and every
`SN-Refs`/`UN-Refs` cell across the SR registry, then rerun `trace.py --strict`
(it validates the SN↔SR join and will flag any missed `UN-###`). **Do *not*
rewrite audit-log / status.md evidence quotes** that say "UN-014" — those are a
historical record of what was decided at the time; rewriting history to match a
later rename is dishonest. Leave them, optionally with a one-line
"(UN-### = today's SN-### after the rename)" note where confusion is likely.

- *Tooling latitude:* `trace.py` intentionally does **not** accept legacy
  `UN-Refs` — a lingering `UN-` after you claim the rename is done is a real
  orphan you want surfaced, not silently bridged, and the migration is a one-time
  find-replace, not an ongoing compatibility burden. If your repo is mid-rename
  and wants a transitional deprecation warning, that's a *local* patch to your
  copy of `trace.py`, not something the kit ships.
- *Downstream test import:* overwriting `scripts/gen_release_checklist.py` from
  the kit renames its public function `read_user_needs` →
  `read_stakeholder_needs`. Any downstream test or script that imports
  `gen_release_checklist.read_user_needs` by the old name will break (a real
  adopter was bitten by this). Grep for `read_user_needs` in your tests and
  scripts as part of this recipe.

### `process.md` splits into `process.md` + `process-options.md` [since cdb64dc2]

The opt-in layers (phased delivery, lifecycle tags, the §8/§9 boundary notes, the
multi-repo rung) moved out of `process.md` into a companion
`process-options.md`, keeping `§`-numbering stable. To migrate: drop in **both**
new files; anything your repo added *inside* the old monolith (rare — it's
kit-owned) moves to whichever file now owns that section. Fix references: a link
to `process.md#section-9` may now point into `process-options.md`. Run
`check_docs.py` — it fails on exactly these broken intra-repo links.

### `Attest` verification kind + the binary-asset registry [since 31f43343]

The **`Attest`** `Verification` method (a named human's recorded judgment —
playtest, creative review, physical action — for what can't be mechanized) and an
optional **`assets`** registry (`ASSET-###`) for unavoidably-binary deliverables.
To adopt: overwrite `scripts/trace.py` (it now accepts `Attest` in the vocabulary
and reports the "attested vs mechanized" split) and drop in the assets registry
template. Retag any SR you were faking as `Test`/`Manual` but that really rests on
human judgment to `Verification=Attest`, and record **who/when** in its TC cell.
For binary deliverables (art, music, voice, video): manage them as **git-LFS or
out-of-repo pointers** and record provenance (human/AI — for Steam-style
AI-content disclosure), license, attribution, and the contract/release link as
`ASSET-###` rows — track *about* the asset in text even though the asset itself
can't be diffed. Both are opt-in; a scope with no subjective or binary work
ignores them (process-options.md "Proportionality doctrine" + "Binary assets").

### The skills layer [since 1bafeb11]

Newer kits ship `skills/`. To bring an agent's skills into an already-adopted
repo, re-run `bootstrap.py --agents claude|gemini|codex|both` against it: it
materializes the matched `kit`-scope skills into the agent dir
(`.claude/skills/…` / `.gemini/skills/…` / `.agents/skills/…` for Codex) and
copies the inert hook example, **skipping any skill file that already exists**
(your edits are safe; use `--force` only after a diff pass). The `SKILL.md`
sources are kit-owned — overwrite freely on re-sync; a skill you customized
locally, treat like `check.py` (take the new version, re-apply your delta). To
refresh the per-agent copies from source after a kit skill changes, run
`bootstrap.py --dest . --sync`. Skills are opt-in accelerators, never a gate
(process-options.md "Skills layer").

### The unattended coordinator (`scripts/agent_loop.py` + root `agent-resume.*`) [since 0386838a]

A walk-away entry point (process-options.md "Unattended operation"): a plain
launch drives the claim→build→integrate loop, and the launchers ship **inert**
until their `AGENT_CMD` slot is wired. To adopt: copy the engine (kit-owned,
overwrite freely on later re-syncs) + the three launchers (yours after seeding —
like `run.*`), and merge the `out/run-logs/` line into `.gitignore`. The tracked
`docs/iteration/` logs + `iteration_index.md` appear on first run; preserve them
like `docs/log.md` — they are history. A repo without agent-driven work skips all
of it.

### Conditional scaffold generation (`docs/kit-profile`) [since c0bd5207]

Newer kits *generate* `docs/process.md` + `docs/process-options.md` from
marker-carrying masters per a recorded profile (`docs/kit-profile`: `stack=` +
`omit=nfr,multi-module` axes; omitted sections keep their § heading plus a
one-line stub, so labels never renumber and links never dangle). An older
adoption has no profile record; its first re-sync is a **one-time regeneration**:
delete the two process docs, re-run `bootstrap.py --dest . [--stack …] [--omit …]`,
and commit the two regenerated docs plus the new `docs/kit-profile`. With no
`--omit` the regenerated docs match the old full copies (minus the copy-me
meta-prose the markers now strip); declaring omissions is opt-in and can happen
at any later re-sync.

### Push policy + the agent iteration branch [since 5aae786e]

Newer kits declare who may publish (process-options.md "Agent iteration branch &
sync"): one word — `human` (default: an agent never pushes, even if asked
mid-session; it prepares the branch and requests), `agent-iteration` (only the
scrubbed `llm/<branch>` iteration branch), or `agent`. To adopt: set the push
dial in a reviewed commit (it lives in `docs/process.toml` since the one-policy-home
entry below; it was its own one-word file before). The full iteration-branch
discipline (agent work on `llm/<branch>`, history scrubbed and collated into
categorical commits before landing on the dev branch) is an **opt-in layer** for
agent-driven repos — a repo without agent-driven work keeps the default and pays
nothing. If you adopt the layer, add `"llm/**"` to your CI push triggers (the
newer shipped `check.yml` already carries it) so the floor runs on agent legs too.

### The `Area` column on the SR registry (owner-hat coverage) [since 5e743dda]

Newer kit templates end the SR schema with an optional `Area` field (owner-hat /
domain tag, process.md §1); `trace.py` reports per-Area SR counts when it carries
values. Adding it to an existing registry is **optional, not a migration** — the
field is outside the required schema, so a legacy registry without it stays green
even under `--strict-schema`.

### status/log split (`docs/status.md` → `status.md` + `docs/log.md`) [since 6a74684c]

The blackboard splits: `status.md` is the **working surface** — only what the
agent or human must perform next — and `docs/log.md` is the **append-only
history** it points at (the Sittings table, verdict blocks, ratified
decisions, session notes; process.md §5). Migration is **optional and
proportionate — never forced**: an adopted repo may keep its merged file. To
adopt: copy `LOG.template.md` → `docs/log.md`, cut the accreted history sections
over **with their headings preserved verbatim** (downstream greps and the §5
wording rely on them), and leave the `History: docs/log.md` pointer in
status.md's header. Don't rewrite the moved entries — they are the historical
record.

### The secrets floor runs in every repo [since 24a8bab1]

The deterministic secrets floor (private-key headers + GitHub/Slack/AWS/`sk-…`
shapes) runs in **all** repos, not just privacy-checked ones (process-options.md
"Secrets floor (every repo)"). Overwriting the hooks + `check_privacy.py` on
re-sync therefore starts scanning a privacy-off repo that previously had none:
the pre-commit hook blocks a staged commit carrying a credential shape,
`check.py` flags a tracked one at every gate, and the pre-push hook scans the
outgoing range. **That is the point** — but if the repo legitimately holds
secret-shaped content (test fixtures, sample keys), mark those lines with the
inline `privacy-ok` marker, and only as a last resort disable the floor repo-wide
(`secrets_scan = false` in `docs/process.toml` today; a reviewed, recorded
decision). No new scaffolded file is required; the default is on, and a repo
migrating from the one-word file's *absent = on* convention lands on the same
value.

### Privacy-check toggle — replaces the old `docs/commit-identity` glob [since 914f9b10]

Newer kits split *identity* from *privacy* (process-options.md "Commit identity &
privacy"): which account authors is the user's own git config (no longer pinned
by a repo file), and a boolean dial runs the privacy gate — the commit author
email and committed content/messages are scanned for PII, with the exempt-email
allowlist (`EXEMPT_EMAILS`, default `*noreply*`) in `check_privacy.py`. To adopt:
overwrite the hooks (`pre-commit`, the new `commit-msg`, `pre-push`) +
`check_privacy.py` + `setup.*` from the kit, delete `docs/commit-identity`, and
set the privacy dial (`true` if you had a non-`inherit` glob, else `false`; the
dial lives in `docs/process.toml` since the one-policy-home entry below). Note
that the pre-commit author check is now a Python `--author` step, so a
Python-less machine no longer enforces identity — deliberate, that pin moved to
git config. The guard covers **future commits in clones that ran setup** only —
history already committed with a private identity needs a git history rewrite,
out of the kit's scope; decide that deliberately before publishing.

### The TC `Evidence` column [since 328f141e]

The test-case registry gains an **`Evidence`** field (between `Automated` and
`Status`) naming the concrete test — a pytest node, a script path, or a
procedure-doc link (inspection-only text, never mechanically resolved). Optional
in general, but from DevBar-Release `--strict-schema` **requires it non-empty on
`Automated=Yes` rows** — a claimed-automated test with no cited location is a soft
false-green; a legacy registry without the column reads as empty and is flagged
the same way. Migration: add the field, then move any test pointers you had
squeezed into `Parameters` (the old `node=…` workaround) into `Evidence`,
restoring `Parameters` to dimensional inputs only. Below DevBar-Release a legacy file keeps
passing untouched.

### The component / workstream schema bundle [since 73313e69]

Four coupled, **never breaking** registry changes land together (the bundle spans
`73313e69`…`7f8cdc56`):

**(a)** the work-items `Track` column is renamed **`Workstream`** (a mutable
grouping category — "track" now means only the parallel-execution lane); the
legacy header is still read, so migration is renaming one header cell whenever
convenient. **(b)** `Predecessors` gains an edge kind: a bare id is a **hard**
(blocking) edge, a `~`-prefixed id (`~WI-013`) a **soft** advisory-ordering edge —
audit your DAG and demote narrative "reads-well-after" edges to `~`. **(c)** A new
optional **`components`** registry (`CMP-###`, process-options.md "Component
layer") is scaffolded, and the LLR/IF/ASSET/PART templates gain an optional
`Component` tag column; existing files without it stay valid (header-driven) —
adopt by adding it where you name components. **(d)** The multi-repo registry is
renamed **`repos.csv` / `REPO-###`** (formerly `modules.csv`/`MOD-###`); the
legacy file + ids are still read, and both may coexist mid-migration.

### The OKF knowledge bundle [since 27ebc29d]

Newer kits export the spine registries as a generated `docs/okf/` bundle, **on by
default** with a pre-commit + DevBar-Release freshness gate. After a re-sync, either run
`python scripts/gen_okf.py` once and commit the bundle (it stays fresh via the
hook from then on), or opt out with `okf_export = false` under `[checks]` in
`docs/process.toml` — a repo with placeholder-only registries needs neither
(vacuous). **Re-sync `check.py` together with the hook:** the hook's step 1b runs
`check.py --run-step okf`, so an older `check.py` with no `okf` step fails every
commit with `check: no step named 'okf'`. The okf step runs **before** the
dashboard step on purpose: the dashboard consumes the bundle (its Knowledge tab),
so the regen order is arch-map → okf → trajectory.

### `docs/trajectory.html` → root `PROJECT_STATE.html` [since 3e56f7ce]

The trajectory dashboard evolved into the unified project-state artifact at the
repo **root** (adds the How-SW module-map view, the optional CMP table, and a
git-derived as-of stamp that `--check` ignores). Migration: after the re-sync,
delete your committed `docs/trajectory.html`, run
`python scripts/gen_trajectory.py`, and commit the new root file — the
`trajectory-map` gate/hook step name is unchanged and now checks the new path
automatically.

### Architecture-connectivity coverage (the `IF-###` tier) [since 05b1b73b]

`trace.py` now reads the `IF-###` interface tier (id/SR-Refs integrity, closing
the SR-002-era gap), the interfaces template gains a `Notes` column (legacy rows
read it empty), and `check_trajectory.py` runs a warn-first **connectivity
coverage** over the arch-map inventory. It is **opt-out, default-on**, so after a
re-sync a **multi-module** repo with no declared seams starts warning
"connectivity undeclared" at the hook and DevBar-Release. That never fails a gate — the warns
only nudge. To act on them, declare `IF-###` rows (process.md §8; use a
`source`/`sink` first-word `Notes` marker for a deliberate pure source/sink) and
regenerate the arch-map + `PROJECT_STATE.html`; to silence the whole layer, set
`interfaces_check = false` under `[checks]` in `docs/process.toml`. A
single-module repo is vacuous and needs nothing.

### Cross-agent skill sync (the `skills-sync` harness step) [since 2b0c013f]

The hook gains a `check.py --run-step skills-sync` step, so **re-sync `check.py`
together with the hook** — an older `check.py` with no `skills-sync` step fails
every commit with `check: no step named 'skills-sync'`. The step is vacuous
unless the repo hosts the neutral `skills/` source and per-agent skill dirs; if
you keep per-agent copies (`.claude`/`.gemini`/`.agents` `skills/`), refresh them
from source with `bootstrap.py --dest . --sync` and commit — a drifted copy is a
gate finding.

### Run launchers become a capability menu (`scripts/run_menu.py` + `[run]`) [since 3ca5e42b]

Newer kits retire the hard-wired, duplicated `RUN_CMD` in `run.cmd`/`run.sh`: the
launchers are thin delegates to `scripts/run_menu.py`, which reads a **`[run]`
section** in `docs/stack.ini` (one `<name> = <command>` line per capability +
optional `<name>.desc`) and presents a menu / launches by name / `--list`s for an
agent. **Never forced — your edited launchers keep working:** a re-sync never
clobbers a `run.cmd`/`run.sh` you filled with a `RUN_CMD` (bootstrap skips
existing files; only *new* scaffolds get the delegates). To adopt: copy
`scripts/run_menu.py` from the kit, overwrite the three `run.*` launchers with
the delegate versions, and move your old `RUN_CMD` value into a `[run]` line
(e.g. `serve = <your old command>`). A pure library still just deletes them.

### The derived gate (`docs/gate` becomes generated) [since 03b27c44]

The re-sync ships `derive_gate.py` and a `check.py --run-step derived-gate` step
(so re-sync `check.py` + the hook together). `docs/gate` is now **generated** from
the artifact states — run `python scripts/derive_gate.py` **once** to migrate your
legacy hand-set `docs/gate` to the derived form (until you do, the
`derived-gate --check` step accepts the old one-line value **value-only**, so an
un-migrated repo is never broken). After migrating you stop bumping the line — you
ratify artifacts (`Status` `Draft`→`Planned`, or an SN section move) in a reviewed
commit and regenerate (process-options.md "Derived gate model").

**Reconcile states against your ratification history before trusting the migrated
value.** The derived gate believes your recorded `Status` values and SN sections —
but a legacy repo's registries usually contain artifacts added *after* the commit
that last set `docs/gate`, states no reviewer ever ratified. Find that commit
(`git log --oneline -- docs/gate`), diff the requirement surfaces since
(`git diff <sha>..HEAD -- docs/requirements docs/test`), and stage everything
added or materially changed since per the new model — new stakeholder needs into a
`## Draft needs (unratified)` section, not-yet-re-reviewed SRs to `Status=Draft` —
so `derive_gate.py` reproduces the gate your history actually attests instead of
laundering post-attestation additions into it. If the derived value still
disagrees with your old hand-set line after that, **the disagreement is the
finding**: ratify (or demote) deliberately before relying on the derived gate.

### The phase model, and the retired grouping column [since 6daee92f]

The delivery `Phase` is now a field on the LLR and TC registries too (it was
SR-only), and the work-item registry **drops** its old per-WI grouping column (the
one the dashboard used to bin the roadmap by — it now tiers
`phase ⊃ workstream ⊃ work-item`). Both changes are **vacuous-until-armed**, so a
re-sync is diffable and never breaks: a registry with no phased row keeps
`trace.py`'s ratified-Phase schema rule dormant (blank = in scope for every
phase), and any leftover grouping column is simply ignored (read by name, no
vocabulary rule).

### `--require-verified` widened to method-blind [since a686bcc8]

The DevBar-Release traceability floor `trace.py --require-verified` now demands
`Status=Verified` for **every** ratified, in-phase SR regardless of its
`Verification` method (was `Verification=Test` only), matching
`derive_gate.sr_gate` — which already blocked DevBar-Release for any unverified decomposed SR.
**Downstream impact:** a repo passing `--require-verified` today with a non-Test SR
(Demonstration / Manual / Analysis / Inspection / Attest / Critique) still below
`Verified` will now fail — it was never actually at the derived gate, only
reporting so. To re-sync: set those SRs to `Verified` once acceptance is met
(attach the TC evidence / recorded attestation), or mark them `Draft` if not yet
ratified. The verification-basis report is now three-way (mechanized /
demonstrated-observed / attested); no registry schema change.

### Integrator verdict-gate unanimity + reviewer-dial redefinition [since 15015bd9]

The integrator no longer clears on a *count* of approving phases: **every
scheduled verdict phase's latest verdict at the reviewed head must be APPROVE**
(REVIEW-A, REVIEW-B, and CRITIQUE on a render-surface train). The reviewer dial
(`review_rounds`) now counts **reviewer** phases scheduled (0/1/2); CRITIQUE is
orthogonal — required on every render-surface train regardless of dial. A
same-head CHANGES-REQUESTED→APPROVE flip escalates NEEDS-HUMAN rather than
silently winning; a never-filed required phase pages instead of stalling.
**Downstream impact** *(historical — the v4 dispatcher retired at the Phase 5
restructure below; `integrate.py`'s serial verdict gate keeps the same
every-scheduled-phase-APPROVE rule)*: a train that previously integrated on an
extra approval covering a missing phase will now block — ensure each scheduled
phase actually files its verdict. No registry schema change.

### Status-map freshness gate made machine-pure [since 1282f52c]

*(Superseded by the open-items registry entry below, which retires
`docs/open-items.md` entirely — if you are syncing past that commit, do that
migration instead of this one.)* The `docs/open-items.md` PENDING block is split
into a committed-tree-pure gated region (blocked WI rows + the run-state ask) and
a **machine-local advisory** region (the `refs/llm/*`-derived source conflicts,
reservations, quarantines and stranded-train notes that don't transport with
clone/push), separated by a labeled boundary; only the pure region is
byte-compared by `--status --check`. **Downstream impact:** an adopter who seeded
`docs/open-items.md` from the old template gets one STALE nudge on the next
`status-map` gate — run `gen_trajectory.py --status` to regenerate the labeled
block (your hand-authored `## OI-N` briefs above the markers stay byte-untouched).
Overwrite the kit-owned open-items template on re-sync.

### The terminal `retired` work-item status [since baed9159]

*(Superseded by the six-state entry below, which respells this `cancelled` and
gives it its own directory; an adopter re-syncing past both applies them in
order.)* The work-item lifecycle gains a sixth `Status`, **`retired`** — a
terminal WON'T-BUILD row that stays in the registry forever with its reason in the
`Deliverable` column (never a `done` overload). Never breaking, vacuous until
used: no schema/header change, and a registry with no retired rows behaves exactly
as before. After re-sync, `check_trajectory.py` accepts `retired` (the
unknown-status lint no longer fires) and validates it as terminal — **R-A**
requires a non-empty `Deliverable` (the reason) and **R-F** requires an **empty**
`SpecRef`; the scheduler never schedules it or counts it as open;
`gen_trajectory.py` renders it in its own dashboard bucket (a separate count,
never folded into `done`). One behavior to know: **a retired predecessor does NOT
satisfy a successor's hard dependency** the way `done` does — a live WI hard-blocked
on a retired one stays `waiting` and is surfaced (a `dead-dep` finding; warn plain,
ERROR under `--strict`), so re-home that edge or retire the successor too.

### Python floor 3.8 → 3.11 [since 8cd569ae]

The kit's stdlib-only scripts declare a **Python 3.11+** floor (was 3.8). Why 3.11
and not 3.9/3.10: those are EOL or nearly so (3.10's security EOL is Oct 2026),
while 3.11 is supported to Oct 2027 and enables the queued `trace.py` refactor —
`dataclass` `slots=True`, finer "did-you-mean" tracebacks, and the interpreter
speedup. The `pytest-cov` Python-gated split dissolves with it: the old
`5.x`-on-3.8 / `7.x`-on-3.9+ marker in `requirements-dev.txt` collapses to a single
`pytest-cov~=7.0`, and `conftest.py` keeps only the 7.x coverage-wiring path.
**Downstream impact:** on a re-sync onto a repo whose contributors or CI still run
3.8–3.10, provision 3.11+ first, then overwrite `requirements-dev.txt`, bump the
`check.yml` / `test.yml` matrix cells from 3.8 to 3.11 (the macOS-arm64 3.8
exclusion was a runner-availability workaround — 3.11 has arm64 builds, so drop it
or keep it as a deliberate coverage call), and update the `dev-setup.*` "install
Python 3.x+" hints. The scripts stay de-facto runnable on 3.9 for now, so the bump
is a promise you enforce in CI immediately, not a same-day code break.

### The owner decision surface becomes a registry + a generated view [since 41b228a5]

`docs/open-items.md` is **retired**. Decision briefs are now ROWS in
`docs/requirements/open-items.toml`, and `scripts/gen_open_items.py` renders them —
together with every `Draft`/`Modified` spine row's per-cell before/after — into
`docs/open-items.html`, the surface the owner reads. The driver was a real sitting:
the old pending block was a POINTER ("run `trace.py --ratify modified`"), and the
depth that makes a re-attest readable is a word-level diff, which markdown cannot
mark.

**Downstream impact — a one-time migration, and it is manual by design because
only you can classify your briefs:**

1. copy the open-items registry template to `docs/requirements/open-items.toml`;
2. move each **pending** `## OI-N` section of your `docs/open-items.md` into a row
   (the section's fields map 1:1 onto the columns: one-line, decision, blast
   radius, options, recommendation). **Do not backfill ruled items** — their
   record is the log's Decisions, and OI ids have historically been reused after a
   section was deleted, so a backfill can collide;
3. delete `docs/open-items.md`;
4. run `python scripts/gen_open_items.py` and commit `docs/open-items.html`.

The `open-items` harness step gates its freshness (machine-local advisory region
masked, like the block it replaces). If you skip the migration entirely, the step
is **vacuous** — no registry and no view means nothing to render — so an adopter
who never used the surface pays nothing.

### The `Modified` re-attest marker + the basis-line format [since 4cc61fa3]

Spine `Status` gains a third recognized value, **`Modified`** — a
post-attestation amendment owing a re-attest (canonical semantics: process.md
§7): the derived gate reads DevBar-Tests for its phase until the sitting flips it back
(`Modified`→`Verified`, or →`Planned` when the amendment invalidated the
evidence), the pending-owner-actions projection carries one line per
Draft/Modified SR, a warn-first `--staged` check flags an amendment without the
flip, and `trace.py --ratify modified` emits a per-cell before/after brief against
the git-derived attested baseline. Never breaking for a registry that never writes
the value — with one **flagged migration**: the `docs/gate` `# basis:` line now
carries `modified=N` beside `drafts=N`, so the first `check.py`/pre-commit run
after re-sync reds the `derived-gate` freshness step once. Fix:
`python scripts/derive_gate.py` and commit the regenerated `docs/gate` (the
first-non-comment-line gate value and its consumers are unchanged).

### The LLR `Rationale` column [since c1bcc389]

The LLR registry gains an optional **`Rationale`** field after `Detail`.
Non-breaking and header-driven: a registry without it reads as blank and stays
valid, so migration is adding one field whenever convenient. *Why it exists:*
`Detail` was the LLR's only prose cell, so the *what*, the *why*, the ruled-out
alternatives and the authoring history were structurally forced into one field —
and a cell asked to hold four things holds none of them legibly. `Rationale` is a
requirement attribute at **every** level (ISO/IEC/IEEE 29148); the SR had one and
the LLR did not, and that asymmetry was the bug. It stays **optional** on purpose:
a short mechanical decomposition row's why *is* its parent SR's, and requiring one
everywhere would manufacture exactly the restatement the process forbids. Fill it
where the decomposition was itself a decision. It is normative text, so the
stand-alone rule applies — no work-item ids, no process-doc citations (`trace.py`
gates it under `--strict`).

### `trace.py` splits into two files [since f18672e5]

`scripts/trace_text.py` joins `scripts/trace.py`, and **a re-sync must copy both**
— `trace.py` imports its spine-row text layer from the sibling, so a repo that
picks up one and not the other gets an `ImportError` on its first check rather
than a quiet degradation. `bootstrap.py` copies them together; a hand-managed
re-sync must too. No behaviour changes: the split is pure decomposition, and the
kit's three golden report files stay byte-identical across it. *Why:* the four
text predicates (`provenance_findings`, `form_findings`, `paraphrase_advisories`,
`ac_advisories`) and the row primitives they share are one concern — *is this row
readable and decidable on its own?* — and pure (rows in, findings out), so they
separate cleanly from the join that owns I/O and reporting.

### Parallel dispatch (v4) is deleted; the integration seam replaces it [since 31ad569d]

The v4 dispatcher/integrator — durable Git reservations, `--jobs`/`AGENT_JOBS`,
worktree pools, `docs/run-state`, train branches — is **deleted**: its lifetime
record (19 reservations → 8 integrations → 0 gate-verified, 11 hand-rescues) did
not justify its 4,042 lines. What replaces it is composition (process-options.md
"Unattended operation" / "Parallel work — the integration seam"): claims are
`integrate.py claim` (queued spec → `docs/work/active/<branch>/`, branch cut from
the claim commit), merging is `integrate.py integrate` (the serial fail-closed
queue — full bar on the composed tree, verdict gate), and a plain `agent-resume`
launch **drives** the loop: frontier → claim → worker session → merge, the
frontier re-derived every cycle so mid-run-filed WIs are picked up in the same
run.

**The upgrade recipe:** re-sync the kit, convert the WI registry CSV to the spec
folder (`wi_convert.py --verify` → `--to-specs` → delete the CSV — and DELETE
it, not keep it beside the folder: the dual-read grace window is over, the
folder wins when it holds real specs, and a repo carrying BOTH homes is an
integrity ERROR on the current kit, not a fallback), drain or
hand-finish any live train worktrees/branches from the old scheme, seed
`docs/stack.ini [generated]`, then delete local reliance on the retired surfaces —
`AGENT_JOBS`, `docs/run-state`, `docs/rework-wi`, `--track`/`docs/tracks/*`,
`docs/next-wi`/`docs/run-phase`, `refs/llm/*`, `docs/parallel-ready`. The WI DAG +
`Priority` are the whole ordering contract; no former content translates to
scheduling state.

### An LLR grounding on a superseded SR is an integrity ERROR [since 871625ec]

*(Superseded by the SR-tier `SupersededBy` retirement below — the validator this
entry describes no longer ships.)*

If your SR registry uses the optional `SupersededBy` field, an LLR whose `SR-Refs`
cites a superseded SR reds `trace.py` at every gate after this re-sync (`--strict`
and `--strict-integrity`) — re-ground each such LLR on the successor SR, or delete
it, before re-syncing `trace.py`. TC citations of superseded SRs stay legal (they
are the retained evidence record). A registry without the field is unaffected.

### The six-state work-item model; `docs/work/archive/` splits and `disposition` is deleted [since 88db58af]

*A flagged migration — the one kit change so far that MOVES files in your
registry.* The status vocabulary becomes
`draft | queued | active | deferred | cancelled | complete`, and status stays what
it always was, the directory — only now the directory is the **whole** statement.
`archive/` held both terminal states, so it needed a `disposition = "retired"`
frontmatter key plus a validator to keep folder and attribute honest; splitting it
into `complete/` and `cancelled/` deletes the key, the validator and both of its
raise paths, because the inconsistent state it checked for is no longer
representable. Two words change with it: `retired` becomes `cancelled` (it could
be read as *finished and put out to pasture*; `cancelled` cannot), and `draft/` is
new — thinking-in-progress, which previously had to sit in `deferred/` and so read
as *a decision* rather than *the absence of one*.

Migrate in one commit:

1. `git mv` each `docs/work/archive/WI-*.md` carrying `disposition = "retired"` to
   `docs/work/cancelled/`, and every other `docs/work/archive/WI-*.md` to
   `docs/work/complete/`;
2. delete the `disposition = "retired"` line from the moved cancelled specs — the
   folder is now the whole statement;
3. `mkdir docs/work/draft` (add a `.gitkeep`; a fresh scaffold ships it), and
   remove the emptied `docs/work/archive/`;
4. rerun `check_trajectory.py --strict`: the loaders REFUSE an undeclared status
   directory, so a spec left behind in `archive/` is a loud, named error, never a
   silent skip.

Use `git mv` rather than delete+add: the backlog-staleness clock reads
`git log --follow --diff-filter=AM`, and it needs BOTH flags — driven on this
kit's own migration, `--follow` alone and `--diff-filter=AM` alone each answer the
rename commit (today), while the pair answers the row's true pre-migration date. A
rewritten history re-dates every row.

*Why `draft/` had to be a DECLARED directory rather than a scratch folder:*
because there is nowhere else safe to put a draft, and the two wrong places fail
differently. Both were driven on a fresh scaffold with the same spec. **An
undeclared directory UNDER `docs/work/`** (say `docs/work/thinking/`): the readers
walk `<status>/WI-*.md` and skip anything under a directory they do not know, so
the spec never enters the registry at all — the duplicate-id guard and the
dashboard go blind, `schedule ready` prints nothing and `gen_trajectory` renders
no document. The id mint alone survives, because it reads FILENAMES through an
unfiltered walk, so the id is held by accident rather than by design; and
`check_trajectory --strict` exits 1 naming the directory, so at least the state is
LOUD. **A folder outside `docs/work/`** (say `docs/drafts/`) is worse in the way
that matters: the mint does not see it either — so the next mint really would
reissue the held id — and **nothing reds**; `check_trajectory --strict` reads
`clean (no work items …)` and exits 0.

### The dispatcher split: `drive.py` → `dispatch.py` + `lane.py` [since 81cac0e1]

`scripts/drive.py` is renamed `scripts/dispatch.py` with `scripts/lane.py`
extracted (one lane's mechanics: worktree, worker subprocess, the refresh). On
re-sync, copy both new scripts and **delete your old `scripts/drive.py`** — a
stale copy would shadow nothing (`agent_loop` imports `dispatch`) but would drift
silently. The dispatcher now admits by the session-hold table: spine-class WIs
wait for the lanes to drain and then admit **together as one batch**, and a
pending ratification drains the lanes and exits 0 naming the cards in
`open-items.html` instead of refusing nonzero. The worker-lane count is a new
declared dial — `lanes` in `docs/stack.ini [agent-loop]` (CLI `--lanes` >
`AGENT_LANES` > stack.ini > default). **An absent key means 1**: your repo stays
exactly as serial as it was until you add the line (fresh scaffolds seed
`lanes = 2`); no re-sync ever changes your lane count, because `docs/stack.ini` is
yours.

### `Phase` is numeric-only once armed [since e0623526]

Once any row is phased, a *ratified* SR/LLR/TC `Phase` must be a **full-cell bare
integer** (`1`, `2`, …) — a prefixed label (`v2`, `P1`) is now a `--strict-schema`
finding, because the `--phase`/`--ratify` filters and the phase-drop detector match
the cell literally and a prefixed cell disarms them silently. A `vN` label still
digit-parses in those filters and the derived current phase (grandfathering), so a
`vN` registry **arms the rule and now fails it**: strip prefixes (`v2` → `2`)
across ratified rows when you take this kit version — a mechanical, diffable edit
(`Phase` is a *traced* cell, so no re-attest window opens). Once you phase any row,
phase every *ratified* SR/LLR/TC — blank stays legal on `Draft` rows only — and the
foundation (minimum) phase stays in scope under `--phase`.
`derive_gate.py --next-phase` prints the number a newly confirmed phase takes.

### One policy home (`docs/process.toml`) [since c560f928]

The ~10 one-word policy files under `docs/` — the gate-authority word, the push
policy, the reviewer count, the privacy toggle, the secrets floor, the
privacy-review posture, guardrails, the blackout window — collapse into a single
hand-edited, machine-read TOML. The old idiom was never a ruling: it accreted
around the git hooks' pure-sh parse (a Python-less box must still fail closed on a
declared privacy policy), and a `head -n 1` read is the only thing that format
buys. The hooks now do a **keyed** match instead, so the file's shape is
load-bearing: one `key = value` per line under a bare `[section]` header, no dotted
keys, no inline tables, no multi-line strings — checked, not merely conventional.

To adopt: re-sync the three hooks + the scripts, take `process.toml.template` →
`docs/process.toml`, then run
**`python scripts/bootstrap.py --migrate-config --dest .`**. It folds every legacy
file it finds into the matching key, **deletes that file**, and is idempotent — and
a full `bootstrap.py --dest .` scaffold pass runs it for you. Two dials change
*type*, not meaning: the reviewer count becomes an integer (`review_rounds = 1`)
and the toggles become booleans (`privacy_check = false`, `secrets_scan = true` —
the legacy `off` word reads as `false`). **Running with both homes live is REFUSED,
not resolved by precedence**, so land the conversion in one commit rather than
half-way.

What deliberately stays a file, each for its own reason: `docs/stack.ini`
(adopter-owned product toolchain, never under a kit-owned template), the
presence-as-semantics markers `docs/work/pause` and `docs/agents-enabled` (a key
cannot express deletion-as-an-act), and the generated cache `docs/gate`.

### `docs/id-watermark` becomes REQUIRED [since e36f5661]

A new one-line-per-space file records the highest id ever allocated in each space,
so that a deleted row's number is never handed out again — the live tree cannot
answer that, because `max(live) + 1` re-issues whatever was removed. `trace.py`'s
always-on integrity pass now refuses an **absent** mark rather than reading it as
"no id is taken", so a re-sync that copies the file but not your history goes red
on the first commit, naming every live id above the scaffold's marks.

**Do this once, immediately after the re-sync:**

```
python scripts/trace.py --bump-ids     # records your existing ids
git add docs/id-watermark && git commit -m "record the id watermark"
```

That is the whole migration: the marks rise to your live maxima and the check goes
quiet. Two cautions. **Never `--force` this file** — `bootstrap.py` exempts it
deliberately, because every other scaffold target is a template to fill or is
regenerable from the tree, while this one is the only record of ids that have been
*deleted*, and overwriting it frees them for silent re-use. And **commit it before
the second commit**: until the file is in git the "a mark only ever rises" rule has
no baseline and reports itself as skipped (it says so out loud rather than passing
quietly). Thereafter a new hand-authored id — the spine tiers have no minter — is a
finding until you re-run `--bump-ids`, which is the intended rhythm: allocate, then
record.

### The spine gains a sibling: `scripts/spine_carrier.py` [since 82d5b818]

The same rule as `trace_text.py` above, and a re-sync must copy it: `trace.py`,
`check_trajectory.py`, `check_docs.py`, `trunk_step.py` and (since the batch-2
entry below) `agent_route.py` import it, so a repo that picks up one and not the
other gets an `ImportError` on its first check. `scripts/migrate_carrier.py` ships
beside it. `bootstrap.py` copies all of them together; a hand-managed re-sync must
too.

*Why a shared module at all,* given the kit's own rule that each script stays an
independently-copyable drop-in: this one holds a **vocabulary** (the carrier key →
column-name map), not plumbing, and a divergence between copies of a vocabulary
does not fail loudly — the copy that has not learned a column returns a row with
that cell **missing**, which every consumer reads as "the cell is empty". Owner
ruling: "independently copyable" means **copyable with its declared siblings**,
which is what the kit already practised (`trace.py` + `trace_text.py`,
`gen_trajectory.py` + six `traj_*` modules) and had not written down.

### The spine's four registries become ONE TOML CARRIER [since bb69a622]

The biggest change the kit has shipped to an existing adoption, and it has a
converter (`scripts/migrate_carrier.py`, which arrived at `a9b6ced3`):
`stakeholder-needs.md` (prose tables) and the SR/LLR/TC CSVs become
`stakeholder-needs.toml` · `system-requirements.toml` ·
`low-level-requirements.toml` · `test-cases.toml`, id-keyed with the prefix
retained and the key bare — `[requirement.SR-137]` under the tier tables `need` ·
`requirement` · `design` · `test`.

**Run it, check it, then stage BOTH sides in the SAME commit:**

```
python scripts/migrate_carrier.py --root . --check   # converts in memory, writes nothing
python scripts/migrate_carrier.py --root .           # writes each .toml beside its source

# STAGE THE NEW FILES FIRST. They are untracked until you do, and the `git rm`
# below stages four deletions: commit without this line and you have deleted
# your registries. (If your scaffold left the shipped `-000` templates staged
# at these paths, this is also what replaces them with your converted rows.)
git add docs/requirements/stakeholder-needs.toml \
        docs/requirements/system-requirements.toml \
        docs/requirements/low-level-requirements.toml \
        docs/test/test-cases.toml

git rm docs/requirements/stakeholder-needs.md \
       docs/requirements/system-requirements.csv \
       docs/requirements/low-level-requirements.csv \
       docs/test/test-cases.csv

git status --short          # expect four A/M and four D — nothing else
```

`--check` converts and re-reads what it emitted, cell for cell, and exits 1 naming
the registry, row id and field for anything that did not survive; the write path
refuses a lossy conversion too. **Both homes at once is REFUSED, not resolved by
precedence** — the readers raise rather than pick — so the delete belongs in the
conversion commit, not a follow-up.

*What you gain, and it is not tidiness.* Three integrity rules stop being code and
become properties of the parse: a **duplicate id** is a decode error (the id is the
table key, and TOML forbids declaring one twice); a **ref list** is a typed array,
retiring the split-on-whitespace rule that read `SN-001 and SN-002` as citing an
orphan called `and`; an **empty cell** is an *absent key*, so "unset" and "set to
empty" stop being the same value. On the need tier, draft-ness becomes a field
(`kind = "draft"`) instead of "appears under a heading containing the word draft" —
a rule a passing prose mention of an id could trip, silently un-ratifying a need.

*Three things to know before you run it.*

1. **The template's `-000` row is now your schema.** TOML has no header line, so
   the shipped example row is the only place the column vocabulary is written
   down. Keep it until you have real rows to read the key names off.
2. **Prose around the tables is not a row, and the converter does not carry it.**
   If your `stakeholder-needs.md` holds guidance, a vision link, or a non-goals
   section, move it into `#` comments yourself — comments survive every tool that
   edits these files, because the one writer that does (`intake`'s `Modified` →
   `Verified` flip) rewrites a single line rather than re-serializing.
3. **Your own scripts may read these paths.** Anything of yours that opens
   `system-requirements.csv` by name gets a `FileNotFoundError` (loud, fine) — but
   anything that CSV-parses the new file gets zero rows, silently. Read through
   `spine_carrier.load(path, id_col)`, which resolves whichever carrier is live and
   hands rows back under today's column names.

The legacy carriers stay readable for now: every kit reader resolves TOML first and
falls back, so a repo that has not migrated keeps working. That fallback is
**deliberate dead weight with an expiry** and will be dropped once no supported
baseline predates the migration — `migrate_carrier.py` is marked `Provisional` for
the same reason.

### Carrier batch 2: `open-items` and `agents` move too [since 955cddec]

`migrate_carrier.py` converts `docs/requirements/open-items.csv` and
`docs/agents.csv` alongside the spine, so there is nothing extra to run — but there
are two things to delete and one to check:

```
git rm docs/requirements/open-items.csv docs/agents.csv
python scripts/agent_route.py --list      # the pool must still resolve
python scripts/gen_open_items.py          # regenerate the owner surface
```

- **Comments survive, and one of them is executable.** TOML's comment is the same
  `#` line the CSV convention used, so the converter carries every one across
  byte-for-byte and *in place*. That matters most for the
  `# tag-rank: ga>preview>beta>exp` line in `agents.csv`, which
  `agent_route.load_tag_rank` **parses** — dropped, it would silently reset the
  maturity vocabulary that resolves a version-less enable-list token.
- **A model id containing a `.` must be QUOTED** — `[agent."OPENAI-GPT-5.2"]`.
  Written bare it is still valid TOML, declaring a table called `5` under a row
  called `OPENAI-GPT-`, so the file parses and the model row is simply gone. The
  converter quotes what needs it; a HAND edit is where this bites, and
  `spine_carrier` refuses such a row at load rather than reading it.
- **Your `docs/open-items.html` must be regenerated**, and any prose linking the
  old paths retargeted — `check_docs` reports those as broken links.

`interfaces.csv` and `components.csv` are deliberately NOT in this batch: they move
with the schema rulings that change what their rows *are*, so converting them first
would mean converting them twice.

### The six check-enablement toggles fold into `[checks]` [since 6562239f]

`docs/trajectory-check`, `docs/interfaces-check`, `docs/components-check`,
`docs/subagent-gate`, `docs/live-status` and `docs/okf-export` become the
`[checks]` section of `docs/process.toml`. `bootstrap.py --migrate-config` converts
and deletes each one, and every checker keeps reading its old file for the same
migration window — so an un-converted adoption is not broken, only un-migrated. The
independently copyable checkers each pay for it with their own small local TOML
reader, which is the cost the ruling weighed and accepted.

### `scripts/check_dupes.py` is REMOVED from the kit [since 704ffd0d]

The duplicate-code lint and the fingerprinted census file it read
(`docs/dupes-allow`) were torn down by owner ruling: over its life it caught
duplication once, at the one-time triage, and never again; it is structurally blind
to a *diverged* copy, which is the case that actually hurts (an edited copy is no
longer an identical token block, so the tool goes quiet exactly when the
duplication becomes dangerous); and 93% of its census lines were registering
deliberate, accepted idioms rather than restraining anything.

**A re-sync will delete the script**, because the re-sync overwrites kit-owned
files and `check_dupes.py` is no longer among them. **Your census file is YOURS** —
it lives under `docs/`, was never kit-owned, and the re-sync will not touch it.
Keeping the check is a legitimate choice: nothing about the ruling says the tool
cannot pay for itself in a repo with different duplication pressure. If you keep
it, pin the last shipped copy in your own tree
(`git show <recorded-kit-commit>:project-trajectory/scripts/check_dupes.py`) and
keep your `[step:dupes]` section pointing at it. If you drop it, delete three
things together or the harness reds: the `[step:dupes]` section in
`docs/stack.ini`, its `docs/dupes-allow = dupes` row in that file's `[generated]`
section, and any spine chain you traced the check with — under the kit's
supersession rule those rows are **deleted**, not marked, with the act recorded in
your log (the ids stay spent).

**What the kit offers instead**, and it is deliberately narrower: duplicated
*policy* — two modules each deciding what "Draft" means, or which methods are
exempt — needs a behavioural test that imports both and asserts they agree by
VALUE. Duplicated *plumbing* is accepted without a bound.

### Carrier batch 3 — `interfaces.csv` + `components.csv` to TOML; the IF tier changes SHAPE [since 2eb1c0c8]

The last two registries join the TOML carrier (`[interface.IF-###]` and
`[component.CMP-###]` tables), held back deliberately until the rulings that
change what their rows *are* landed, so each converts once. Same command
family as the earlier batches (`python scripts/migrate_carrier.py --check`,
then without `--check`, then `git rm` the CSV — a repo carrying BOTH carriers
is a hard refusal). **The IF tier also changes shape — read before running:**

- **`Status` RETIRES.** It was never one of the fields process.md §8 declared,
  nothing validated it, and it overlapped `Stability` — `Stable` appeared in
  both columns of one row meaning different things. `Stability`
  (`Experimental` · `Stable` · `Deprecated`) is now the row's one maturity
  field. Map your values onto it before converting; a surviving
  `status = ...` key is a column nothing reads.
- **`Signal` is NEW and required**: `discrete` (a finite enumerable alphabet)
  or `variable` (unbounded content). If both cross, the row is `variable`.
- **`Rationale` is NEW and optional** — the home for the *why* that used to
  have nowhere in the row to go except `Contract`.
- **A warn-first schema tier arrives with them** (`trace.py`): required
  fields, those closed vocabularies, `CMP.State`, four negative rules on
  `Contract` (no work-item id, no decision citation, no rationale connective,
  a 500-character ceiling), and an advisory classifying every endpoint that
  is not an arch-map module. All ADVISORY — none of it changes an exit code
  at any gate — so an unmigrated repo goes noisy, never red.

### The `G*` gate tags retire for the eight-rung stage ladder [since 08c985cb]

**The biggest vocabulary change the kit has shipped, and it reaches your own
files.** `G0`/`G1`/`G2`/`G3`/`G-Release`/`G-Final` are gone as tags. In their
place:

- **Eight stage rungs** — `DevStg-Needs` · `Boundary` · `Reqs` · `Arch` ·
  `LLReqs` · `Tests` · `Impl` · `Release`. A repo is **IN** a stage. The label is
  the identifier; the position is DERIVED (`stage-ord=`/`stage-of=` on the basis
  line), so an inserted rung re-numbers everything and moves no citation.
- **Three bars** — `DevBar-Reqs` · `DevBar-Tests` · `DevBar-Release`, each named
  for the top rung it certifies (Needs…Reqs, Arch…Tests, Impl…Release). You
  **CLEAR** a bar. `DevBar-Below` is an internal sentinel, not a bar.

**The word "gate" survives** wherever it means a check that can fail — the
`docs/gate` path, `derive_gate.py`, `check.py --gate`, "the freshness gate". Only
the TAGS retired. Do **not** run a blanket find-replace on the word; the
conversion is tag-scoped, and `scripts/check_vocab.py` (new, shipped) tells you
which of your own lines still carry a tag.

**Nothing breaks on day one.** Every reader that could receive a retired tag
translates it: `check.py --gate G2` runs `DevBar-Tests` and warns once;
`docs/stack.ini` `gates = G2 G3` translates silently; a WI's `bar: G3`
translates silently. So your pipeline stays green through the re-sync and you
convert at your own pace.

**The recipe — six moves, in this order:**

1. **REGENERATE `docs/gate`. This OVERRIDES §1's preserve-classes rule and
   ADOPTING §6's "preserve always" classification for that one file.** The cache
   is *field*-compatible but not *value*-compatible: your committed file carries
   `G1` on its value line and `computed=G0 … stage=4` in its basis, and `stage=4`
   means something DIFFERENT under the eight-rung ladder than it did under the
   six-integer one. Run `python scripts/derive_gate.py` once and commit the
   result. There is **no compat shim** — `--check` reports the old cache STALE on
   the first recompute, deliberately, because a reader that accepted both
   vocabularies is how the retired tags grow back. The failure direction is safe:
   a stale cache makes the stage unreadable, and an unreadable stage is treated
   as **human-held**, so the one state it can produce is *more* human
   involvement.
2. **Re-apply your `docs/process.toml` dials.** `human_ratification_through`
   keeps its 0–4 meaning — it was **mapped** onto the ladder, not re-keyed — so
   your declared value still means what it meant. Confirm it survived the
   re-sync; every pre-existing answer for the four spine tiers is unchanged.
3. **Hand-check anything of yours that passes `--gate` LITERALLY** — your own
   git hooks, CI workflow steps, Makefile targets, editor tasks. They keep
   working via the alias, but each will print a deprecation line every run until
   you update it. This is the one class the re-sync cannot fix for you.
4. **Convert your own WI rows' `Bar` values** and your `docs/stack.ini`
   `[step:*] gates =` keys to the new spelling. Both translate on read, so this
   is cleanup, not a break — but `check_vocab.py` will name each line.
5. **Your own log sign-offs stay VERBATIM.** The attestation carve-out applies to
   adopters too: a row recording a named human certifying `G1` recorded exactly
   that, and re-wording it makes the record claim something was signed that was
   not. Add a one-line header note naming the retired vocabulary instead —
   `check_vocab.py` already exempts `docs/log.md`, `docs/ratify/`,
   `docs/archive/` and the closed-WI specs. **Do rename the heading**
   `## Gate Sign-offs` → `## Sittings` (it is code-pinned in
   `trunk_step.RESERVED_HEADINGS`); the rows underneath do not change, and each
   new row names the **rung range** it certifies.
6. **`--sync` any materialized per-agent skills** — `gate-advance` is a full
   rewrite onto the ladder, and `registry-hygiene` / `session-protocol` took
   passes. `python scripts/bootstrap.py --dest . --sync`.

**Then run `python scripts/check_vocab.py --root .`** and work the list. It is
**warn-first** at the requirements bar and promotes to ERROR from `DevBar-Tests`
on, so a repo mid-conversion sees every site without being blocked.

**Also converted, for reference:** the `[phase]-[g1|g2]` WI-title archetype
becomes `[phase]-[reqs|tests]` for NEW titles — your committed anchors keep their
spelling and still parse forever (a title is a citation).

### The depth-0 FRAME registry; IF `Stability` → `Approval`; rung 1 re-keys [since 0ff33a95]

Four migrations in one commit, and the third one **changes what your reported
stage means** — read that item before re-syncing scripts.

- **NEW: `docs/requirements/external.toml`**, scaffolded by `bootstrap.py` from
  `registries/external.template.toml`. It holds your **depth-0 frame** in three
  tiers on one path: `[entity.EXT-###]` (who is outside), `[boundary.B-##]`
  (what crosses your system boundary), `[relationship.REL-###]` (external-to-
  external flows you are not a party to). This is the tier your **system
  requirements form around**. An `IF-###` row is a concrete interface
  definition and ties BACK to a crossing only when it realizes one.
- **RUNG 1's APPLIES-WHEN MOVED, and your stage may RISE silently.**
  `derive_gate.boundary_incomplete` used to read `interfaces.toml` and cap you
  at `DevStg-Boundary` while any IF row read `Stability = Experimental`. It now
  reads `external.toml`'s crossing `Approval`. **A repo that carries
  `interfaces.toml` and no `external.toml` therefore SKIPS rung 1 entirely**
  where it was previously held. That is the correction — internal seam
  definitions never typed a boundary — but it is not a no-op: if you want the
  rung, scaffold `external.toml` and declare your crossings. If you never
  declared a boundary, the rung is now correctly free.
- **IF `Stability` RETIRES for `Approval`** (`draft` · `approved`), the tier's
  one maturity field, shared with the new boundary tier. Map your values before
  or during the re-sync — `Experimental` → `draft` is the direct reading;
  `Stable`/`Deprecated` → `approved` **only if you mean it**, because `Stable`
  was a MATURITY claim (the contract has settled) and `approved` is a
  RATIFICATION one. The kit's own registry mapped all 113 rows to `draft`
  rather than manufacture approvals nobody signed. A surviving `stability = ...`
  key is a column nothing reads.
- **NEW optional IF keys:** `interface_from_external` / `interface_to_external`,
  the directional tie-back naming a `B-##` crossing. Present ONLY on a row that
  realizes one; a row with neither is an internal seam.
- **NEW optional SR key: `boundary_refs`** (`Boundary-Refs`), the crossing(s) a
  requirement states an observable AT. An id that does not resolve is a HARD
  finding under `--strict`; leaving the cell blank is a warn-first coverage
  count, so an unmigrated spine goes noisy, never red.
- **Two checks changed arming, both warn-first, neither newly red.** The
  seam-TC citation rule now arms on every IF row instead of on a maturity
  value, so your uncited-seam count may RISE. WI-191's "a cited `Experimental`
  seam needs a rationale" arm is GONE — its input no longer exists, and
  re-keying it onto `draft` would have armed it on every row.

### The SR tier's `SupersededBy` column RETIRES; supersession is deletion [since fd26a966]

The optional SR `superseded_by` key, its ~110-line `trace.py` validator
(semicolon-list shape, unknown target, self-link, cycle, the LLR re-grounding
error above) and its ratified-cell classification are all GONE, on the ruling
that a supersession row is history wearing a row id: **a registry states what
IS; git and the log are the history.** A retired row is *deleted*, its id spent
forever (the id watermark's committed mark keeps the headroom), and one log
entry is the forwarding home naming the replacement rows.

- **If your SR registry carries `superseded_by` keys:** the carrier now REFUSES
  the key on an SR row (it is no longer in the tier's declared key set). Before
  re-syncing scripts, delete each tombstone row, re-point any citing IF rows at
  the replacement rows, re-check `sn_refs` coverage against the replacements,
  and record one forwarding log entry for the batch.
- **TC rows whose `verifies` cite only superseded SRs** must retire with them —
  a test case verifying nothing is not evidence.
- The **CMP registry's own `PartOf`/`SupersededBy`** is a different rule and is
  unchanged.

### `SR.Area` retires for a closed `Aspect` vocabulary [since 9861e957]

The free-text `Area` column is GONE from the SR tier, replaced by `Aspect` —
a **closed** six-value vocabulary: `process`, `trajectory`, `unattended-loop`,
`connectivity`, `perf`, `portability`.

**Why it is not a rename, and what that costs you.** The measurement behind
the ruling: of the kit's own 31 `Area` values, **25 were a component by
another name** — derivable from your decomposition and therefore redundant —
while only **6 spanned components**, which is what an aspect IS: a
cross-cutting concern no partition can express. So the conversion **DROPS**
the derivable values rather than remapping them. In the kit's own registry
that took 63 tagged rows down to 21; the other 42 now carry no aspect at all,
and that is the intended end state, not data loss.

- **Migrating:** for each SR, keep the value only if it names a cross-cutting
  concern that maps to one of the six; otherwise delete the cell. Do not
  invent a seventh value to preserve a tag — if your value names a component,
  your component registry already says it.
- **A blank cell is NORMAL and never a finding.** A requirement that is not
  cross-cutting carries no aspect. (In the kit's own spine, `portability`'s
  three rows have no owning module at all, and that was ruled *not* a defect.)
- **A non-empty out-of-vocabulary value IS a `--strict-schema` finding**
  naming the row and the allowed set — reported at the schema tier, gating
  under `--strict`, exactly like the `Verification`/`Tier` vocabularies.
- **A surviving `area = ...` key is a column nothing reads.** The carrier's
  SR-tier key set declares `aspect`; `Area` is absent from the traced-cell
  table, the OKF fact row, and `trace.py`'s per-tag count (now "SRs by
  aspect").
- Nothing else moves: `Aspect` stays REPORT-ONLY for counts, and no gate reads
  the distribution.

### `docs/handbacks/*` in `orphans-allow` [since bd0e739a]

**Applies to every adoption that scaffolded `docs/orphans-allow` before this
commit — which is all of them.** The partial-close contract shipped without its
navigability entry, and the defect is invisible until the first lane closes
early: `handback.close_partial` writes an immutable per-close report under
`docs/handbacks/`, nothing links to it *by design* (its path is the close
event's identity, and the disposition row intake mints is what makes it
reachable as work), so `check_docs` reports `orphan doc (no path from an entry
root)` and the full suite goes red on a repo that did nothing wrong.

Found by dogfooding: the kit's own first partial close, 2026-08-15.

Migration is one line appended to `docs/orphans-allow`:

```
docs/handbacks/*
```

Do it **before** your first early close, not after — the failure arrives
attached to an unrelated merge, which is the worst moment to diagnose it. If
your `orphans-allow` is unmodified from the template you can simply overwrite it
with the kit's copy.

---

## 4. Translation helper — concept renames

A rename reads to a diff as an unrelated deletion plus an unrelated addition, which
is exactly the class that bit a real adopter (a silently renamed public function
broke their imports). These are the renames the kit has shipped, each anchored the
same way. Grep your **own** prose, scripts, CI, hooks and registry cells for the
left-hand spelling.

### `UN-###` → `SN-###`; `read_user_needs` → `read_stakeholder_needs` [since 3ea00aa5]

User Need → Stakeholder Need, prefix only (numbers preserved). The function rename
is the import-breaking half — see the UN → SN entry in §3.

### `Track` → `Workstream` (work-item grouping) [since 73313e69]

"Track" now means only the parallel-execution lane. The legacy header is still
read, so this is a rename-when-convenient, not a break.

### `modules.csv` / `MOD-###` → `repos.csv` / `REPO-###` [since 7f8cdc56]

The multi-repo delegation registry names repos, not components. Legacy file + ids
still read; both may coexist mid-migration.

### `Campaign` (the per-WI grouping column) → deleted [since 1cc8d636]

The roadmap is binned `phase ⊃ workstream ⊃ work-item`. A leftover column is
ignored (read by name, no vocabulary rule), so nothing breaks — but your prose and
dashboards should stop saying it.

### `docs/trajectory.html` → `PROJECT_STATE.html` (repo root) [since 3e56f7ce]

Step name (`trajectory-map`) unchanged; the path it checks moved.

### `docs/open-items.md` → `docs/requirements/open-items.toml` + `docs/open-items.html` [since 41b228a5]

Source and view split: one is the registry you edit, the other is generated.

### `agent_dispatch.py` → `integrate.py` (+ the drive loop) [since 31ad569d]

The v4 dispatcher's job splits into claim/integrate on one side and the drive loop
on the other; the module name does not survive.

### `retired` → `cancelled`; `disposition = "retired"` → the directory [since 88db58af]

The work-item terminal state is respelled and moves into its own directory; the
frontmatter key is deleted, not renamed.

### `scripts/drive.py` → `scripts/dispatch.py` (+ `scripts/lane.py`) [since 81cac0e1]

Delete your old `drive.py`: `agent_loop` imports `dispatch`, so the stale file
shadows nothing and drifts silently.

### `G0|G1|G2|G3|G-Release|G-Final` → the stage ladder [since 08c985cb]

The tags retire; the traceability survives. Grep your own prose, scripts, CI,
hooks and registry cells for the left-hand spelling — **as a whole-word TAG, not
as the word "gate"**, which survives wherever it means a check that can fail
(`docs/gate`, `derive_gate.py`, `--gate`, "the freshness gate" all stay).

| retired tag | now | what it names |
|---|---|---|
| `G1` | `DevBar-Reqs` | the bar certifying `DevStg-Needs` … `DevStg-Reqs` |
| `G2` | `DevBar-Tests` | the bar certifying `DevStg-Arch` … `DevStg-Tests` |
| `G3` | `DevBar-Release` | the bar certifying `DevStg-Impl` |
| `G0` | `DevBar-Below` | the internal below-the-floor sentinel — never a bar |
| `G-Release` | `DevStg-Release` | the release-readiness **rung** (never a mechanized bar) |
| `G-Final` | the owner's final read | the `final_review` dial, which is its own axis |
| `[phase]-[g1]` / `-[g2]` | `[phase]-[reqs]` / `-[tests]` | the phase-anchor archetype for NEW titles only |
| `## Gate Sign-offs` | `## Sittings` | code-pinned; each row now names a rung RANGE |

Every reader accepts the left-hand column as an alias, so this is a
convert-at-your-pace rename — with two exceptions that are **not** aliased:
`docs/gate`'s own contents (regenerate it) and a stage value in a basis line
(same regenerate). Full recipe: the §3 entry above.

---

## 5. Promotion: when this pack stops being prose

This pack is deliberately **not** mechanized. Re-syncs are rare, every adopter is
inside the owner's own development sphere, and the LLM does the judgement work
under every design — so investing in what it reads beats investing in selectors
(the proportionality doctrine, SN-012). The honest cost is that nothing enforces
"a kit change that needed an entry got one": the obligation holds by attention.

**The promotion trigger, named so it is a decision rather than a drift:**

- the **first out-of-sphere adopter**, OR
- the **second observed drift incident** in this pack (the first, in the prose
  regime, was the `downstream-resync` skill's hand-maintained recipe copy going
  stale within weeks at zero re-sync traffic — caught by an audit, not by use).

Either event is evidence that attention has stopped being a sufficient enforcer.

**What promotion means.** Each entry lifts into a row of a shipped **migration
registry**: `since` SHA, a **detect probe** where one exists, the action, and a
pointer to the prose. Detection selects where it can; the SHA range selects the
rest. That lift is mechanical *precisely because* every entry here already carries
its `[since <sha>]` — the anchor is the column, so promotion is a transcription
rather than a re-derivation. The registry is only better than this document if its
**enforcer lands with it**; a registry no check enforces rots exactly like the
prose it replaced.

**If a detector ships early**, on its own, because some migration warrants one
anyway: record it in that migration's entry here. The kit already ships thirteen
detector-style migrations under a settled four-way taxonomy (auto-migrate,
degrade-gracefully, warn-only, hard-refuse), and none of them consults
`docs/kit-version` — each infers the repo's actual state from its artifacts, which
is why version-blind re-syncs have mostly survived. The two mechanisms compose
rather than compete.
