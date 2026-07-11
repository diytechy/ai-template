# Capability expansion — run menu · critique loop · registry robustness · OKF tab — PLAN

**Status:** 🟡 **PROPOSED — drafted 2026-07-11 from owner direction; every
section carries a working default and its open rulings.** No code written;
ingests as `WI-067…` when scheduled. The spine-touching sections bundle into
the **pending G3 re-attestation** if scheduled before the owner sitting (the
campaign ruling,
[archive/specs/working-surface-and-architecture-restructure.2026-07-11.md](../archive/specs/working-surface-and-architecture-restructure.2026-07-11.md)).

**Provenance:** owner direction 2026-07-11 (four items, verbatim intent
restated per section); two same-day web-research passes (an OKF-visualizer
survey and a multi-account/router CLI survey — key findings folded in below);
builds on the landed S8 layer (`agent_route.py`, `score_reviews.py`, reviewer
dispatch, verdict files) and the 2026-07-11 OKF audit + WI-066 banner ruling.

---

## C1 — `run.*` becomes a capability menu

**Owner intent.** The root `run` file should present the user with all major
capabilities of the system — e.g. *run the docker image and open its pages* vs
*build the ISO and launch the burner* for one project; *run a named simulation
configuration* for another. "That run capability is probably not well defined
right now."

**Confirmed.** `run.template.{cmd,sh,command}` today hard-wires ONE `RUN_CMD`,
deliberately duplicated between `.cmd` and `.sh` ("the command lives exactly
twice"), and **no SR covers the launcher surface** — it rides PROCESS.md §7
prose only.

**Model.** Capabilities are **declared once** and the launchers become thin
readers (the `stack.ini` idiom):

- `stack.ini` gains a **`[run]` section**: one `<name> = <command>` line per
  capability, optional `<name>.desc = <one line>` rows.
- A new stdlib **`scripts/run_menu.py`**: no-arg = numbered interactive menu
  (name + desc, pick one); `run_menu.py <name>` = direct launch;
  `--list` = stable machine-readable listing (the agent surface). Missing
  `[run]` section → the same "no launch command wired yet" guidance today's
  launcher prints, exit 1.
- `run.template.{cmd,sh,command}` become 3-line delegates to `run_menu.py` —
  the duplication dies; multi-step capabilities stay one command each (a
  project script owns the steps).

**Never-breaking.** Existing repos with a wired `RUN_CMD` keep their files
(resync never clobbers project-edited launchers); new scaffolds ship the
delegates; a `[run]`-less stack.ini degrades to guidance.

**Steps.** `run_menu.py` + rewritten templates + `stack.ini` template `[run]`
examples + ADOPTING §6 migration note + the §7 rung prose updated
(PROCESS.md is byte-budgeted — keep the delta minimal, flag it).

**Tests.** Declared capabilities listed; direct launch runs the command;
`--list` format stable; absent section = guidance + exit 1; Windows/POSIX
quoting; scaffold ships the delegates.

**Spine impact.** One new SR formalizing the launcher surface (the evaluator
runs any major capability without recalling commands) → re-attestation rider.

**Open rulings.**
1. Capability home: `stack.ini [run]` *(default)* vs a separate `docs/run.ini`.
2. New SR *(default — a different need than dev-setup's SR-032)* vs extending
   SR-032.
3. All three launchers delegate to Python *(default — Python ≥3.8 is already
   the kit floor; an interactive menu in raw `.cmd` batch is not worth owning)*
   vs shell-native menus.

## C2 — subjective-quality critique loop (the perceptual arbiter)

**Owner intent.** Some acceptance is subjective — "a realistic looking
rendered scene", artifact comparisons with no crisp measurable interface. The
implementer session cannot judge its own output (a real project shipped
awkward render artifacts because "the LLM-agent didn't know how to judge it,
it just shipped it"), and the original TCs may have been lax. Another LLM
agent with **a different hat** must give the critical eye — say *where and
why* something isn't good enough, ideally drive a better TC restructure, and
most importantly **drive rework and deeper exploration**. Who is the arbiter
of "good enough"?

**Model** — built on the S8 chassis (fresh independent sessions, redacted
prompts, verdict files, escalation keyed to `docs/gate-policy`):

- **Perceptual TCs.** A TC whose acceptance is subjective declares it: its
  `Method` names the critique procedure and its `Parameters` name a **rubric**
  (`docs/rubrics/<name>.md`) plus the **artifact recipe** (the command/steps
  that produce the screenshot/render/output under judgment). The rubric
  derives from the **SN/SR intent, not the TC** — that inversion is what
  catches a lax TC instead of inheriting it.
- **The CRITIQUE run-phase.** A fresh session, provider-heterogeneous from the
  implementer when available (`agent_route` reused), receives: the rubric, the
  artifact paths (agent CLIs read local images natively; capability varies per
  model — note it in the registry `Notes`, degraded = text-proxy critique),
  and the SN/SR intent text — **never the implementer's self-assessment** (the
  S8 redaction rule). Output = a verdict file in the `docs/reviews/` format:
  the machine line plus **located findings** ("where and why", anchored to
  regions/aspects of the artifact), plus optional **TC-hardening findings**
  (proposed measurable sub-criteria). The critic never edits the spine —
  hardening proposals route through the change-intake flow (process.md §5).
- **The loop.** BUILD → CRITIQUE → rework, iterating until APPROVE or the
  iteration budget (default **3**) trips the S8 escalation semantics
  (page-the-human per the declared `gate-policy` mode). This is the
  "optimization loop": bounded iteration toward a written rubric, not a
  single-shot pass/fail.
- **The lax-TC ratchet.** A CRITIQUE round that returned CHANGES-REQUESTED
  findings and then closes with **no change to the validation chain** (TC
  prose or test logic) trips the existing no-validation-delta warn (WI-053
  machinery): the fix must land in the chain, not just the artifact. This is
  the specific mechanism that prevents "shipped it because nothing judged it"
  from recurring.
- **The arbiter (the ruling that matters).** Working default: **the critic
  gates iteration; the human owns acceptance.** A critic APPROVE ends rework;
  gate closure still carries the human `Attest` (the gate-closure strong-model
  floor and the attested-vs-mechanized split stand unchanged). Under
  `gate-policy: autonomous`, the critic verdict closes iteration-level
  acceptance and the recorded-verdict rules govern the gate as they do today.
  *(This does not contradict the S8 "no LLM-judge tiebreaker" ruling — that
  ruled out an LLM arbitrating between reviewers' scores; here the quality
  itself is perceptual and an LLM eye is the only mechanizable instrument.)*

**Spine impact.** One new SN (*subjective/perceptual acceptance is adjudicated
by an independent critical eye against a written rubric — never by the
authoring session*) + one new SR (the critique loop) → re-attestation rider.

**Risks.** The rubric becomes the quality ceiling (a vague rubric yields a
vague critic — the TC-hardening channel is the repair path); critic sycophancy
(defended by fresh context + provider heterogeneity + no self-assessment);
multimodal support varies per CLI (declared per-model, degraded honestly).

**Open rulings.**
4. Verification vocabulary: **no new value** *(default — the critic is an
   instrument under `Attest`; Evidence = verdict file + artifact path)* vs a
   first-class `Critique` method (touches trace's vocabulary + byte-budgeted
   PROCESS.md text).
5. Trigger: the CRITIQUE leg fires when a WI touches a perceptual TC
   *(default)* vs riding the `docs/review-policy` dial.
6. Iteration budget default (3) and where it's declared (env-overridable
   constant like the S8 escalation knobs — default).
7. Rubric home: `docs/rubrics/` files *(default — reusable across TCs)* vs
   inline TC cells.

## C3 — agent registry robustness: version-less ids, multi-login, routers

**Owner intent.** (a) An enable-list entry without a version should resolve to
the **newest** registry version, preferring a final tag designation (like
`-PRO`). (b) A user may hold **multiple paid plans with one provider** (Claude
and Codex both allow it) — how does the registry express that, or does it push
into a third-party router? (c) If a router is used, does it become a
**provider row** itself?

**Research findings (2026-07-11 pass, verified against live provider/CLI
docs; sources in the session record).** One correction and four structural
facts:

- **The `-PRO` correction.** Across vendors, `-pro`/`-mini`/`-flash`/`-codex`
  are **model identity** (a different, separately-billed model line), never a
  maturity/finality tag. Maturity lives in a different tag set: GA =
  *untagged*, vs `-preview`/`-exp`/`-beta` (Google formalized exactly this).
  The owner's intent maps safely to: **prefer GA/untagged over
  preview/exp/beta** — and `-PRO`-style tokens belong in `MODEL_NAME`, so
  version-less resolution must be **intra-`(Provider, Model)` only** (it never
  crosses model lines — that keeps the "different model vs version" trap
  closed).
- **The template's own column contract is muddy today** — a prerequisite fix:
  the shipped example rows leak line-names into `Version` (`3-pro`) and
  duplicate the version into `Model` (`gpt-5.2`). Pin the contract:
  `MODEL_NAME` = the provider's line identity (incl. `-pro`/`-flash`);
  `VERSION` = the *comparable* token only (dotted numeric, date stamp, or
  maturity tag). Moving vendor aliases (`chat-latest`, tier aliases like bare
  `opus`) should not be stored as `Version` — the kit's own newest-rule is the
  only mover.
- **Env-only selectors don't fit today's `CmdTemplate`.** The loop launches
  `subprocess.run(argv)` — no shell, no `env=` — so `CLAUDE_CONFIG_DIR=… claude
  -p` in a CmdTemplate would fail (the assignment parses as the executable).
  And the *only* account selectors for Claude (`CLAUDE_CONFIG_DIR`) and Codex
  (`CODEX_HOME` — `--profile` alone shares one `auth.json`, NOT two accounts)
  are env vars, as is Claude's router path (`ANTHROPIC_BASE_URL`).
- **Concurrency:** distinct Claude/Codex config dirs are token-isolated —
  concurrent account rows are safe; **Gemini OAuth accounts share one creds
  file and race on refresh** — multi-account Gemini must use API keys or be
  serialized.

**Model (working defaults, shaped by the findings):**

- **Version-less resolution:** an enable-list token naming `PROVIDER-MODEL`
  with no version resolves over the registry rows whose **`Provider`+`Model`
  columns** match (column-keyed — the id stays a never-parsed join key):
  primary = dotted-numeric tuple compare, tiebreak = maturity rank
  (GA/untagged > `preview` > `beta` > `exp`, a fixed vocabulary with a
  per-registry override), final tiebreak = date stamp. Preview/exp rows are
  skipped unless explicitly named or the only candidate. "Newest" is computed
  **only over rows present in `agents.csv`** — deterministic and offline.
- **Multi-login:** a second account = a second registry row with a distinct id
  and its own `CmdTemplate`, enabled by a new **optional `Env` column**
  (`KEY=value;KEY2=value2`, merged over the inherited environment at launch) —
  the declarative fix for every env-only selector (accounts AND router base
  URLs). Per-id cooldown already gives each account its own quota pool
  (correct by construction). Flag-based selection (Codex `--profile` for
  *config*, `-c` overrides) keeps working inline with zero change.
- **Routers as providers:** confirmed — one router = one `Provider` row set
  (`OPENROUTER-…`), its CmdTemplate carrying the base-url selection (via `Env`
  for Claude; via `-c model_provider=…` + `wire_api="responses"` for Codex;
  Gemini-through-router is fragile — treat unsupported). **False-diversity
  fix:** a new optional **`Family` column** (training lineage: `ANTHROPIC`,
  `OPENAI`, `GOOGLE`, …; **absent/blank = `Provider`**, so today's registries
  behave identically). Reviewer heterogeneity and the scorer's cross-family
  corroboration re-key on `Family`; `Provider` stays the invocation truth
  (cooldown, launch, accounts).

**Steps.** Column-keyed resolver in `agent_route.py` + the `Env` merge in the
loop's launch path + `Family` re-key of `select()`/scorer + template column
contract fix + example rows + PROCESS_OPTIONS routing subsection update +
tests (resolution ordering incl. mixed version kinds; env merge; family
heterogeneity; absent-columns = byte-identical legacy behavior). Security
note carried into the docs: pin LiteLLM away from the known-malicious PyPI
versions (`1.82.7`/`1.82.8`); Gemini OAuth concurrency caveat stated.

**Spine impact.** Extends SR-045's text (routing gains resolution/account/
router semantics) → re-attestation rider. All additive, never-breaking (new
columns optional; absent files/columns = today's behavior).

**Open rulings.**
8. Pin the `Model`/`Version` column contract as above *(prerequisite to all
   of C3 — the shipped example rows violate it today)*.
9. Ordering direction when numeric and maturity conflict: numeric-newest-wins
   with preview demoted on ties *(default)* vs stable-always-wins (is
   `3.1-preview` newer than `3-GA`?); confirm the tag vocabulary + override.
10. Confirm resolution is intra-`(Provider, Model)` only — the `-PRO`
    correction (preference for "final designations" = GA-over-preview, not
    pro-over-plain).
11. The **`Env` column** *(default — declarative, resync-friendly)* vs
    wrapper executables for env-only selectors.
12. Second-account id convention: an `Account` column with an id suffix
    (e.g. `…-ACCT2`) *(default)* vs a provider-suffix (`ANTHROPIC2-…`) —
    either way `Provider`/`Family` stay identical across the account rows and
    ids stay distinct (independent cooldown).
13. The **`Family` column** + re-keying heterogeneity/scorer from provider to
    family *(default: yes, with absent = Provider fallback)*.

## C4 — PROJECT_STATE.html gains an OKF knowledge tab (the first real consumer)

**Owner intent.** The main HTML output should also consume the OKF artifacts
and show a visualizer on a separate tab — reusing an existing source if one
fits — while the HTML stays offline-buildable.

**Research verdict (2026-07-11 pass, sources in the session log).** The
`GoogleCloudPlatform/knowledge-catalog` OKF visualizer is real (Apache-2.0, a
single `viz.html` with the bundle embedded as JSON) **but disqualified as-is**:
it loads cytoscape.js and marked.js **from a CDN** (violates the offline/
self-contained rule) and uses a non-deterministic force layout (violates the
`--check` byte-stability contract). Vendored graph libraries were surveyed
(sigma ~97 KB, force-graph ~176 KB, cytoscape ~370 KB minified) — all carry a
second problem: `check_vendored.py` can't verify a lib inlined inside a
generated file, so a vendored lib forces a second committed file, breaking the
one-self-contained-artifact guarantee.

**Model (the research recommendation, adopted as the working default).**
Extend the kit's **own deterministic machinery** — no vendored library:

- A new **Knowledge tab** in `PROJECT_STATE.html`: the typed concept graph
  (SN/SR/LLR/TC/IF + process guides, node fill keyed by `type`), laid out
  server-side in Python by the existing `_dag_ranks` + barycentre layouter
  (the `sw_graph()` pattern pointed at the knowledge join), with the existing
  ~70-line vanilla-JS idiom for hover-highlight + click-to-detail. Layout is
  computed at generation time, so **no new `--check` exclusions** — the as-of
  stamp stays the only excluded line.
- **gen_trajectory consumes `docs/okf/`** (parse frontmatter + link lists;
  duplicate the small loader per the established small-loader rule rather than
  importing gen_okf) — making the dashboard the bundle's **first real
  consumer**, which is what the 2026-07-11 OKF audit found missing. Vacuity:
  no bundle (opt-out, or empty spine) → the tab is omitted; regen order is
  arch-map → okf → trajectory (document it where the regen recipe lives).
- **Size lever = body embedding.** Default: the **middle path** — embed each
  concept's one-line `description` in the detail panel and **link out** to the
  committed `docs/okf/<tier>/<id>.md` for the full body (~+50–80 KB on today's
  ~199 KB file). Embed-all-bodies (~+250 KB) and link-only are the
  alternatives.

**Spine impact.** Extends **SR-038** (the dashboard SR gains the knowledge-tab
clause) and touches SR-042's Rationale (the bundle gains a consumer) → both
ride the re-attestation.

**Steps.** Stdlib okf loader + knowledge join; tab render + detail panel;
regen-order note; tests (tab renders from a real bundle, omitted without one,
byte-deterministic, link-out targets exist, mobile shell holds); docs.

**Open rulings.**
14. Consume `docs/okf/` as the tab's input *(default — the owner's stated
    intent, and it makes the bundle load-bearing)* vs re-deriving from the
    CSVs and merely linking the bundle (weaker consumer story, one less
    coupling).
15. Body embedding: middle path *(default)* vs embed-all vs link-only.
16. If the owner wants the organic "graph-view feel" later: a fixed-seed
    force layout **computed in Python** stays deterministic and lib-free — a
    follow-up, not this WI *(default: layered layout now)*.

---

## Sequencing & bundling

```
C1 run menu            (standalone)
C2 critique loop       (builds on the S8 chassis)
C3 registry robustness (extends agent_route/SR-045; research pending)
C4 OKF knowledge tab   (consumes docs/okf; extends SR-038)
```

All four touch the spine (C1 new SR · C2 new SN+SR · C3 SR-045 text · C4
SR-038/042 text) — per the campaign ruling they should land as **one campaign
riding the pending G3 re-attestation sitting**, so the owner still signs once.

## Consolidated open rulings

Rulings 1–16 above (C1: 1–3 · C2: 4–7 · C3: 8–13 · C4: 14–16), plus:

17. **Schedule as one campaign now** (bundling with the pending
    re-attestation sitting) vs after the owner sitting closes the current
    batch. Every section carries a working default, so an unruled item does
    not block scheduling — rulings can land per-section like the S0–S8
    precedent.
