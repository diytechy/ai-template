# WI-468 — intake proposals for the four hat-exposed obligation candidates

**Date:** 2026-08-17 · **WI:** `WI-468` (intake only — **this session minted
nothing**; every disposition below is the owner's ruling at the sitting) ·
**Origin:** the hat-aware blind re-derivation, team C
(`2026-08-16-derivation-alignment.md` §4.3; clause texts in
`2026-08-16-blind-derivation-c-hats.md`) · **Desk:** sitting-3 §0.4 item 8.

**This document proposes; it rules nothing.** One section per candidate:
what the kit measurably does today (named files and functions), the option
set — amendment / hat-derived SR under an existing need / new SN / refuse —
each with what it would say and cost, the honest case for refusal, and a
recommendation. A recommendation is a starting position, never a ruling
taken in advance.

## 0. The owner steer, and what the record says

The owner, dispatching this WI: *"I wouldn't really anticipate new SNs (Hats
themselves should no longer result in edge SNs, that method has been
retired), but it might result in new SRs when interpreting SNs through that
hat lens."*

The record supports the steer, twice over:

- **OI-18, ruled 2026-08-13 (owner):** *dissolve all ten edge-case needs* —
  edge coverage is *"REGENERATED per-need by the hats mechanism … rather
  than standing as a separate tier"*
  (`docs/requirements/open-items.toml` OI-18). Today all 28 SN rows read
  `kind = "core"`; no `edge` row survives. A hat producing a new SN would
  re-open the tier that ruling closed.
- **2026-08-16l (owner, option (b)):** *hat-derived labels over SN
  amendment* for the SR-052/053/054 quality family — the standing precedent
  that an obligation arriving through a lens lands as a **labelled derived
  requirement** (the DO-178C derived-requirement class the alignment map
  invokes: legitimate because the deriving lens is named and the need owner
  sees it fed back), not as new need text.

So the structurally favored form throughout is the **hat-derived SR under an
existing need** — and where a candidate genuinely cannot be carried without
new *need* text, this document says so explicitly rather than bending the
option to fit the steer. The alignment map classes C-DPR-3 and C-PRF-1 as
**needs defects** (the kit does the thing and no need says so), so those two
sections carry that tension honestly.

One vocabulary note, to keep the options crisp: an **amendment** to an
existing SN puts the obligation in *normative need text* (the SR that
follows derives plainly, no label needed, but the SN re-opens for
re-attestation — cheap while the 2026-08 window is still open, a real cost
after it closes); a **hat-derived SR** leaves the need untouched and carries
the deriving charter in its `Rationale` (the 2026-08-16l form); a **new SN**
is the option the record stands against; **refuse** records the candidate
and the reason on the log, minting nothing.

---

## 1. C-DPR-3 — provider egress of commit authorship

**Deriving charter:** hat.DATA-PROTECTION (*"personal data crossing a
boundary with no stated basis, retention limit or access rule"*), with
hat.SECURITY's **C-SEC-5** (a brief is an unreviewed egress path — the
inclusion rule shall be *declared rather than implicit*) and hat.LEGAL's
**C-LEG-3** (transmission terms per declared provider) arriving at the same
boundary control. Classed a **needs defect** by the alignment map §4.3. The
crossing is already drawn: `REL-003` (`docs/requirements/external.toml`) —
EXT-005 model runners *"touch the SESSION, never the system"*.

### Grounding — what actually crosses today

Two channels, and they have opposite characters.

**The push channel (what the kit assembles) is narrow and disciplined —
but the discipline is an undeclared convention.** The prompt builders are
`agent_loop.worker_prompt` (WI row + predecessor Deliverables clipped to
200 chars + `git log --oneline --no-decorate` clipped to 30 lines +
`git diff --name-status` clipped to 60), `agent_loop.critique_brief` (SR
intent + TC `Parameters` + full rubric files), `adjudicate_brief.compose`
(full closed spec + close report + oneline/name-status logs, "no commit
BODIES" stated in-module), and `plan_briefs.build_surface` (a hard
two-file allowlist plus `hats.toml`). A sweep of the prompt path for
`%an|%ae|%ad|--author|blame|git show` finds **zero** hits — no authorship
field is ever formatted into a brief — and `docs/log.md` is excluded *by
name* in three modules (`plan_briefs.py`, `adjudicate_brief.py`,
`intake.context_block`). So the C-SEC-5 observable is nearly met in
behaviour; what is missing is exactly what the clause asks for: the
inclusion rule as a *declared set* rather than a convention living in five
functions.

**The pull channel is unbounded by construction.** Every row in
`docs/agents.toml` launches the runner with permission bypass flags
(`claude -p --dangerously-skip-permissions` / `codex exec
--dangerously-bypass-approvals-and-sandbox`), `cwd` at the repo root. The
runner can read the whole tree and run `git log` with full authorship
itself; nothing strips or filters an outbound prompt anywhere in the kit
(the only content-stripping that exists, `agent_common.redact_secrets`,
matches four credential shapes on the **inbound** transcript). The privacy
gate (`privacy_check = false` here; `docs/process.toml`) would, when on,
refuse an unattended run under a non-exempt author identity at preflight —
it never redacts egress. So the boundary control the kit actually has is
**consent-shaped, not filter-shaped**: `docs/agents-enabled` is already
"the consent surface" in SN-026's own acceptance, and the launcher carries
a CONSENT banner.

**Is authorship personal data here?** In this repo the commit identity is
deliberately a public noreply address, and the one human name in the record
(the sittings table in `docs/log.md`) belongs to the owner who put it
there. For an *adopter*, history carries every contributor's name, email
and timestamp — and the kit briefs their repo to a provider with no stated
basis. The candidate is about the kit's delivered posture, not this repo's
particular hygiene.

### Option set

- **(a) Amend SN-026.** Its acceptance already declares the consent
  surface and *"logs every selection — never a silent model swap"*; a
  clause would extend the same pattern to content: *the basis on which
  repository content crosses to a declared provider is declared per
  provider, with what is excluded*. Blind-reader check: SN-026's current
  text governs **which model runs**, not **what it is shown** — a stranger
  deriving from need + acceptance would not produce the egress rule, so
  today this obligation is genuinely beyond the parent's text. Cost:
  SN-026 is already `attestation = "pending"` (amended 2026-08-16), so the
  re-open is marginal while the window holds.
- **(b) Hat-derived SR under SN-026** *(the 2026-08-16l form)*: the
  delivered loop declares the inclusion rule for content composed for
  dispatch to an external model runner, and the basis/exclusion for
  repository content crossing to a declared provider — `Rationale` naming
  DATA-PROTECTION with C-SEC-5 and C-LEG-3 converging (three charters,
  three reasons, one boundary control — team C §2.3 item 8). Observable: the
  eligibility rule is readable as a declared set (a per-row field in
  `docs/agents.toml` or a `process.toml` dial is LLR-tier detail); a
  planted credential inside brief-eligible content blocks dispatch
  (C-SEC-5's fit criterion — the secrets scanner exists and the brief
  assembly points are enumerable). The honest limit must be stated in the
  row: the declared rule can bound the **push** channel and *scope the
  consent* for the pull channel; it cannot technically bound what a
  bypass-flagged runner reads — the same design-control honesty B-04's
  notes already record for the hosted runner.
- **(c) New SN.** What it would have to say: *a team's repository content,
  personal data included, crosses to an external model provider only on a
  declared basis with a declared exclusion.* The record stands against the
  form (§0), and the subject has two live parents (SN-026's provider
  registry and consent surface; SN-009's protection instinct) — a third
  need would split one boundary control across three homes.
- **(d) Refuse.** See below.

### The honest case for refusing

The runner *is* the developer: the session's entire function is reading
this repository, so "a declared basis for the development session to read
the repo it is developing" is a compliance document that changes no
behaviour. The kit already holds the two honest controls it can hold —
explicit consent (`docs/agents-enabled`, the CONSENT banner, the bypass
flags argued in `agents.toml`'s own header) and an author-identity
preflight under the privacy gate — and the design-control ruling the frame
applied twice (`REL-003`, the `B-06`/`B-07` cut) says this system holds no
authority over what an external runner does once invoked. A declared
exclusion rule the kit cannot enforce risks being read as a guarantee it is
not. **What refusal costs:** an adopter who turns `privacy_check` on gets
identity protection at the *commit* boundary and nothing that even names
the *model* boundary — the gate scans what publishes, not what is briefed —
and the push-channel discipline that really exists stays unfalsifiable
because no requirement states it (the same shape as the no-stub detector,
desk finding #1).

### Recommendation

**(b) — one hat-derived SR under SN-026**, labelled with the three
converging charters, scoped honestly: declare the brief-inclusion rule
(mechanically checkable today), declare the per-provider basis/exclusion as
the *scope of the consent* `docs/agents-enabled` grants (not as a technical
filter), and state the pull-channel limit in the rationale. This follows
the steer and the 2026-08-16l precedent, and it converts an existing,
real, undeclared discipline into a falsifiable one. The needs-defect
classification is answered rather than suppressed: option (a) is the
need-tier form of the same obligation and is cheap while SN-026's window
is open — take it *instead of* (b), not alongside, if the owner wants the
need to own egress; carrying both would state one rule in two homes.

---

## 2. C-DPR-2 — the privacy finding record's retention

**Deriving charter:** hat.DATA-PROTECTION. Classed a **new
derived-obligation candidate** (§4.3): the finding record is the one
artifact guaranteed to contain the personal data it reports, created by
the control itself.

### Grounding — what the finding record actually is

**The scanner mints no record of its own.** `check_privacy.report()`
prints `(location, label, excerpt)` to stdout and returns an exit code;
the module contains no file-write at all. But the `excerpt` is
`m.group(0)` — **the matched value itself**: the email, the token, the
identity term. The finding *is* the personal data, on stdout.

**The durable copy is the session transcript, and it is tracked.** An
unattended session that runs the bar has the finding text in its output;
`agent_common.write_session_log` writes that transcript to
`docs/iteration/NNN-<stamp>.log` — committed bookkeeping (212 files today
<!-- fig: cmd="ls docs/iteration/ | wc -l" rev=8537b205 -->) — after
`redact_secrets`, which strips **credential shapes only and does not touch
the PII classes**. The unredacted raw stream additionally lands in
`out/run-logs/` (gitignored, never pruned by any script). No retention
bound, no access rule, no artifact *designated* as the finding record
anywhere.

**The premise is dormant in this repo but live in the shipped kit.** With
`privacy_check = false` here, only the secrets floor fires — and secrets
are the one class the transcript path redacts, so today's meta-repo
exposure is nearly closed *by accident*. For an adopter with the gate on,
the chain is exactly as the charter fears: a PII finding echoes the value,
the transcript persists it in a tracked, committable file, and git history
makes the retention effectively infinite.

### Option set

- **(a) Amend SN-009** — acceptance gains *"a finding never persists the
  matched value beyond the session"*. Need-tier ownership; SN-009 is
  already `attestation = "pending"`, so the window cost is marginal.
- **(b) Hat-derived SR under SN-009** *(recommended form)*: any durable
  record the delivered kit produces of a privacy finding identifies the
  finding by **class and location, never by the matched value**.
  Observable (the same fit-criterion shape C-SEC-4 already uses for
  secrets): a planted personal-data value caught by the gate appears **0
  times** in any tracked artifact after the run. Implementation is cheap
  because the seam exists — `redact_secrets` already sits on the exact
  path and needs the privacy classes added when the gate is on. Note this
  is a deliberate **narrowing of the charter's ask**: the charter asks
  basis/retention/access; a kit cannot honestly promise a retention limit
  or an access rule over an adopter's git history (committed content is
  forever, access is the host's) — but it *can* promise the value never
  reaches durable storage, which moots both.
- **(c) New SN.** No case: the subject is SN-009's own ("a team is
  protected from publishing a secret or private identity" — a finding
  record that republishes the identity is SN-009 defeating itself).
- **(d) Refuse.** See below.

### The honest case for refusing

No designated finding record exists; the scanner persists nothing; the
exposure is a transcript side-channel, in a repo where the PII classes are
switched off. The candidate asks the kit to bound an artifact it never
deliberately created, and this repo cannot itself exercise the guarded
path without turning a gate on that its owner turned off. **What refusal
costs:** the control's own output remains the one guaranteed carrier of
what it catches — for every downstream adopter the privacy gate is
marketed to — and the defect is invisible precisely when the gate works
(a finding that blocks a commit still lands in the committed session log
of the run that found it).

### Recommendation

**(b)** — the non-persistence form, labelled DATA-PROTECTION (C-DPR-2),
under SN-009, with the narrowing from retention-bound to
value-never-persisted stated in the rationale. It is testable with a
planted value, implementable on an existing seam, and honest about what a
kit can and cannot promise about retention. Refusal is defensible for
*this repo* but not for the shipped kit, and the kit is the product.

---

## 3. C-PRF-1 — SN-027's undeclared throughput budget

**Deriving charter:** hat.PERFORMANCE (*"a declared budget with no
measurement behind it"* — here inverted: machinery with no declared
budget). Classed a **needs defect**: SN-027's entire justification is
throughput and it declares no measurement. The desk's own note (§0.4
item 8): this is the candidate needing the most judgement, because a
declared throughput measure commits the repo to measuring it.

### Grounding — what is measured today

**Nothing measures it, and the finding holds without qualification.**
SN-027's `why` is the word "Throughput:" plus the idling argument; its
acceptance is wholly structural (worker ceiling, isolated worktrees, one
serial integrator, `--jobs 1` semantics, crash recovery) — no number, no
comparison to serial, no measurement obligation. In the machinery itself
(`dispatch.py`, `schedule.py`, `trunk_step.py`, `integrate.py`) the only
occurrence of "throughput" is one prose comment (`integrate.py`, "extra
lanes buy throughput instead"). What *does* exist: per-session telemetry
(WI-124 — wall s, api s, turns, s/turn, rendered as columns of
`docs/iteration_index.md`) that nothing aggregates by lane or compares to
anything; and `check_perf.py`, a generic budget comparator that is
**unwired** here (no `[step:perf]` in `docs/stack.ini`, no
`performance-budgets.csv`, no `perf-metrics.json`).

**The sharpest fact:** `dispatch.lanes_dial` reads
`[agent-loop] lanes` from `docs/stack.ini`, and the key **is not
declared** — the dial defaults to 1. **The meta-repo runs SN-027's
machinery serial**, and owns no instrument that would tell it so. The
unfalsifiability is not hypothetical; it is the current state, measured.

**The house already has the idiom a measurement would use:**
`[smoke-budget]` in `docs/stack.ini` declares seconds + membership with a
ratchet test (`tests/test_smoke_budget.py`) — a declared figure, a
deterministic check, deliberate re-stamps. A throughput measure would not
be a new kind of thing here.

### Option set

- **(a) Amend SN-027** — acceptance gains a measurement clause: *the
  improvement over `--jobs 1` on a declared workload is measured,
  repeatable, and a miss is reported rather than silently accepted* (the
  C-PRF-1 text). This is the full form, and it commits the repo to a
  benchmark harness: a declared workload, a serial baseline run, and a
  place the comparison lives. Real cost, stated plainly — and wall-clock
  throughput of an LLM loop is dominated by provider latency and model
  choice, so a numeric improvement target pins machine + provider + model
  conditions ("one machine is one data point", `docs/status.md` standing
  rules).
- **(b) Hat-derived SR under SN-027, the modest form** *(recommended)*:
  the delivered loop **reports the utilisation of the fan-out it
  commissions** — per run: lanes configured, lanes actually occupied, WIs
  integrated per wall-hour — from the telemetry seams that already exist
  (the iteration log header / index), reported never gated, no declared
  improvement target. This is deliberately less than C-PRF-1 asks: it
  makes the throughput claim *observable* rather than *budgeted*. It
  would, today, print `lanes=1` — i.e. it would have surfaced the
  sharpest-fact discrepancy on its first run, which is the concrete
  argument that some instrument earns its keep.
- **(c) New SN.** No case: SN-027 is the need; the defect is in its own
  text.
- **(d) Refuse, and narrow the need instead.** Reword SN-027's `why` at
  the re-attest it already owes (`attestation = "pending"`): the honest
  justification is structural — *the WI DAG already encodes what may
  proceed; a frontier bounded to one lane idles ready work for no reason;
  fan-out is admitted only because the serial gated seam makes it safe* —
  a claim about admitted concurrency, not a quantified speedup. That
  removes the unfalsifiable speed claim rather than building machinery to
  falsify it, at zero ongoing cost. SN-012's right-sizing supports this:
  perf is named there as an opt-in layer that must cost non-users nothing.

### The honest case for refusing

Option (d) *is* the refusal case, and it is respectable: a benchmark
harness for a loop whose wall time is provider-dominated measures mostly
the provider; the repo runs one lane in practice; and the kit's own
proportionality doctrine warns against machinery whose keep exceeds its
earnings. What refusal-without-narrowing costs: the need keeps justifying
the system's most complex machinery with a claim no instrument can
check — three independent derivations flagged it, and "unfalsifiable as
written" stays true in the registry the owner signs.

### Recommendation

**(b) as the floor, (d)'s rewording alongside it** — they compose: narrow
the need's justification to the structural claim *and* have the loop
report the utilisation it actually achieves. Both are cheap; neither
commits to a benchmark. Recommend **against** (a)'s declared numeric
improvement target at need tier — it is the one option that commits the
repo to a measurement whose dominant variable it does not control. If the
owner takes only one: (b), because it is the only option that would have
caught the lanes=1 fact this session had to find by reading the dial code.

---

## 4. C-ACC-2 — the colour-only signal

**Deriving charter:** hat.ACCESSIBILITY (ruled `always` 2026-08-16).
Classed a **new derived-obligation candidate**. The desk's note: cheapest
as an SN-008 wording amendment.

### Grounding — where colour actually carries signal today

**The candidate's premise is measurably overstated against legacy: the
core obligation already exists in the registry.** `SR-052`
("Dashboard accessibility", `Approved`, hat-derived label ACCESSIBILITY
added 2026-08-16) states verbatim: *"no information is encoded by color
alone (status/phase/type encodings carry a text or shape cue)"* — and it
is mechanized: `LLR-113` ("No information by colour alone (A3 core)",
under rubric anchor A3 of `docs/rubrics/dashboard-accessibility.md`) →
`TC-118` → `test_a3_every_painted_vocabulary_member_is_explained_in_words`
plus three drift guards. The dashboard renders a **shape glyph per status
inside the node label** (`traj_render.STATUS_GLYPH`: ✓ ● ○ ✎ ◌ ⊗), pairs
every swatch with glyph + word in the legend, and emits `data-status` +
tooltips. Team C derived C-ACC-2 blind — correctly, since the lens could
not read the registries — but the alignment claim "carried by neither
A/B nor the legacy layer" does not survive contact with SR-052's text.
What C-ACC-2 adds beyond SR-052 is scope: *any* surface carrying a
verdict/gate/status, console and rendered alike.

**On the wider scope, the measured reality is already conformant:**
console verdicts are words (`check.py` prints `PASS`/`FAIL`/`RESULT:
PASS`; a repo-wide sweep for ANSI colour finds a single escape sequence,
a line-clear in `agent_session.py` — the kit's console output uses **no
colour at all**); `docs/gate` is plain text; the README carries no badge.
The "green" SN-008 names is, in delivered fact, the word `PASS`.

**The real, named gaps are narrower than the candidate:** (i) `LLR-113`'s
own recorded narrowing — the worded cue must exist in the *same document*,
not within eyeshot; (ii) the JS detail badge is excluded from the legend
rule (its own text carries the concept); (iii) **`gen_open_items.py` is
outside the mechanized A3 sweep** — its idioms are good (ins/del carries
line-through + box-shadow "so the grouping survives a monochrome print";
pills carry words) but held by comment discipline, not by the closure;
(iv) the rubric is scoped to `PROJECT_STATE.html` alone. Plus two thin
spots: the process-flow "you are here" tier (accent border, no word — one
panel away from a plain-text "Next gate" sentence) and the two hero meters
(which-meter-is-which rides fill colour; the values are texted).

### Option set

- **(a) Amend SN-008's wording** *(the desk's own recommendation)*: state
  the channel, not the hue — e.g. *"a reader can believe a **pass
  verdict**"* with the honesty clause unchanged. This is the spine-authoring
  skill's own named failure mode ("colour-only signals — state the channel,
  not the hue") fixed at its source. Cost: SN-008 is one of the few SNs
  *not* already re-opened (no `attestation` field, no 2026-08-16
  amendment) — this amendment is what re-opens it, though the window is
  open anyway until the sitting. It changes no obligation by itself.
- **(b) Hat-derived SR** stating C-ACC-2 in full (*no verdict, gate
  outcome or status conveyed by colour alone, on any surface that carries
  one, console and rendered alike*). Honest problem: **it would share its
  subject with SR-052's existing clause** — one meaning, two rows, the
  anti-duplication defect — unless SR-052 is simultaneously narrowed to
  its other clauses, which is re-tier churn on an `Approved` row for no
  behavioural delta (the beyond-dashboard surfaces are word-only today).
- **(c) New SN.** No case whatsoever: SN-008 exists and is exactly on
  subject.
- **(d) Refuse the mint; disposition as *matched-to-legacy* instead** —
  feed C-ACC-2 back to the alignment record as matched to SR-052 (the
  DO-178C feedback half: the need owner sees what the lens produced and
  where it already lives), and file the real remainder as **coverage work
  under SR-052**: extend the A3 sweep to `gen_open_items.py` (gap iii)
  and word the process-flow "now" marker — a WI, not a spine row.

### The honest case for refusing

Refusal here is not "the obligation is unwanted" — it is that the
obligation is **already wanted, stated, and enforced** at SR-052/LLR-113,
and a second row would give one meaning two treatments (the exact failure
the CONSISTENCY charter names). The only substantive loss in refusing the
mint is need-tier ownership of the channel-not-hue principle — which
option (a) supplies for one wording change.

### Recommendation

**(a) + (d) together, no new spine row:** amend SN-008's metonym (the
desk's own call — cheapest, and it is the need-tier fix), record C-ACC-2
as matched to SR-052 in the alignment record, and file the open-items A3
sweep + the two thin spots as coverage work under SR-052. This delivers
everything the candidate honestly adds, at the cost of one wording change
and one WI, and mints nothing that duplicates an Approved row.

---

## 5. Summary table

| Candidate | Class (map §4.3) | Measured premise | Recommendation |
|---|---|---|---|
| C-DPR-3 egress basis | needs defect | Push channel disciplined but undeclared; pull channel unbounded by construction; no outbound redaction exists | **Hat-derived SR under SN-026** (3 charters converge); SN-026 amendment the alternative, not a companion |
| C-DPR-2 finding record | derived candidate | No designated record; the durable copy is the committed session transcript; `redact_secrets` skips PII; dormant here (`privacy_check=false`), live for adopters | **Hat-derived SR under SN-009**, narrowed to value-never-persists (testable on an existing seam) |
| C-PRF-1 throughput | needs defect | Nothing measures; `check_perf.py` unwired; repo runs `lanes=1` with no instrument to notice | **Modest derived SR under SN-027** (report utilisation, no target) + reword the `why` at its pending re-attest; against a numeric target |
| C-ACC-2 colour-only | derived candidate | **Overstated vs legacy**: SR-052/LLR-113/TC-118 already state and mechanize no-colour-alone for the dashboard; console is word-only, zero ANSI colour | **No new row**: amend SN-008's metonym + record matched-to-SR-052 + file the open-items sweep as coverage work |

Every recommendation is a starting position for the sitting; the session
minted nothing.
