## 2026-08-30 — the owner rules OI-68 (1c, a SLOC-based line ratchet / 2a / 3a / 4a) and OI-69 (a1 / b1 / c2 / d1 / e1 once the dial is on); five rows filed with their edges

Deferred open items: none — both pending rows were ruled by this entry, and
the decision surface is empty again.

Both rulings were made in session, over four exchanges, and the owner's words
are recorded verbatim; the two rows' `one_line` and `decision` cells carry
the ruling at their head, the OI-67 convention, and their `wi_refs` name the
rows this entry files.

### OI-68 — RULED: (1c) keep both sensors armed, the line ratchet re-based to SLOC · (2a) · (3a) · (4a)

The owner, on the driver's clarification that the brief's cell recommends
(1a) retire / (3a) armed, where the driver had argued (1b) / (3b) in session:
*"I was referencing open-items from this repository, which lists 1a / 2a /
3a / 4a. If there was some other context you saw it was not clear to me, but
the more I read for OI-68 I wonder if 1c is the right direction + some update
to make sure line length checks omit whole-line comments, which can obscure
what matters."* — and, on the tuple the driver then proposed, *"Sounds good."*

What is ruled. **Q1 (1c), with one change to the instrument:** both sensors
stay armed because they measure different axes — module SIZE (decomposition:
how much code sits in one file) and function COMPLEXITY (readability: how
deeply it nests) — and `tests/test_module_size_ratchet.py` is RE-BASED from
raw physical lines (`len(text.splitlines())`, which counted the prose that
made it fire six times on docstring-only growth in one sitting) to **SLOC:
non-blank, non-comment, non-docstring lines**, the prototype's own `sloc()`
definition, held in ONE place in the kit beside the sensor and imported by the
this-repo ratchet so the two instruments cannot drift. The re-base is a
one-time full re-stamp of the table with the derivation on record — an axis
change reviewed once, not a blind re-stamp to a moving tree. Nothing is
deleted: no `[generated] linecounts` row, no `OTHERWISE_ENFORCED` entry, no
WI-521 pointer move. **Q2 (2a):** the complexity sensor censuses `tests/` as
well as `project-trajectory/scripts/`; the line ratchet stays scripts-only,
so WI-521's refusal to extend a disputed axis to a second tree is honoured.
**Q3 (3a):** armed on this repo at `DevStg-Impl` as `[step:complexity]`,
`--report` only downstream, arming an opt-in layer. **Q4 (4a):** `match` is
one increment (the spec's own text), a comprehension's `if` takes the nesting
increment, threshold 15, both pinned in the docstring and by tests. The
driver's (1b)/(3b) reservations are on record in the filing entry and are
not taken.

What it changes in the plan of record
([../plans/2026-08-29-complexity-sensor-plan.md](../plans/2026-08-29-complexity-sensor-plan.md)):
phase 2 shrinks from "arm + retire" to "arm + re-base" — the smaller blast
radius; phases 1 and 3 are as planned. The plan's byte arithmetic (§0, §1.6,
§4.3) is one day stale — `PROCESS.md` 87,871, `PROCESS_OPTIONS.md` 179,258,
the guard skill 4,938 with 62 B of headroom — and the executing session
measures rather than trusts it, as the plan itself instructs; the smoke
membership stamp (1,390 against 1,384 collected) will need a deliberate
re-stamp when the sensor's test module joins the tier.

### OI-69 — RULED: (a1) · (b1) · (c2) · (d1) · (e1) once the dial is on

The owner: *"I will take all of Open-Items recommendations, of course
assuming OI-69 takes c2 as just discussed."* The discussion, recorded because
it corrected the driver twice:

- **(b)** the owner: *"the adjudicator would retain design decision and
  orientation regardless if it's an active session or picked up from
  surrounding context and previous decisions. Context available for
  continuity agreed might influence judgement around future work items, but
  the original study was around judgement of the same item ... I would think
  the context of the previous judgement would be good to have going into the
  next, but agreed it's influential, but it is not the same as judging it's
  own design or judging the same thing twice."* Ruled (b1):
  `reset_on_same_artifact = false`, the fork hardening banked. The one
  residual named for the record: a changes-requested → rework → same judge
  second look IS the same item twice with the first verdict in context — the
  continuity case itself — and the signal to watch in the telemetry is the
  rework-round flip rate. The layer's build should carry the diff since the
  first verdict in the second-round brief so continuity is spent on what
  changed.
- **(c)** the owner: *"if a ping is issued every 50 min over 7 hours, that's
  8 pings, ringing in about $0.03 I assume? It's just a ping to keep the cache
  hot ... If the agents-resume is running, that's the only time it will be in
  a blackout, and the only time it would be pinging to keep the cache ready
  for a resume from that blackout."* Ruled (c2), pinging THROUGH the
  `12:00–19:00` UTC weekday blackout, and the driver's (c1) recommendation
  was WRONG on the plan's own arithmetic: a ping is a real one-turn API call
  that re-reads the cached prefix (≈ 0.1× the input price, ≈ $0.15 on a 300k
  Opus-5 prefix — not fractions of a cent), so eight pings ≈ $1.20 against
  the ≈ $3 cold rewrite they avoid; break-even ≈ 20 pings ≈ 17 h, which the
  daily window never reaches. Anthropic only; codex and opencode caches live
  minutes and are never pinged. Sol's finding 17 (a TURN that starts just
  before the boundary) stays its own line: no turn starts within one
  worst-case turn of the boundary.
- **(e)** the owner asked what surfaced it and whether a dedicated home would
  lose the adjudicator its context; the answer on record: everything the kit
  mandates comes from the working directory (`CLAUDE.md`/`AGENTS.md`, the
  project skills, project settings, `.mcp.json`, the brief, the registries)
  and survives; what moves is the user layer — credentials (to provision),
  user settings and personal skills, and the shared transcripts and
  auto-memory that a headless adjudicator in this checkout resolves to today.
  The owner: *"Okay, so even with e1, it will pick up the agents.md, skills,
  etc"* — confirmed. Ruled (e1) **once the dial is on** (session identity and
  transcripts become load-bearing then); today's shared home stands for the
  telemetry row.
- **(a1)** and **(d1)** as recommended: the layer retains a transcript a
  bounded process replays, not an actor — the no-daemon doctrine stands; the
  dial lives in `docs/process.toml [adjudicator]`.

### Filed by this entry

Five rows queued, each with a `specref` that resolves path and anchor, the
watermark `WI` 536 → 541: the complexity sensor report-only (phase 1,
`strong`, `spine` — it mints an SR/LLR/TC chain), arm-and-re-base (phase 2,
`needs` the sensor plus a SOFT edge to WI-521, whose §3 it amends — a hard
edge on a standing debt owner would deadlock, IF-054), ship (phase 3, needs
phase 2); the retention layer (needs the telemetry row already queued) and
its on-box verification (needs the layer). Enabling the dial is the owner's
edit of one number, not a row. Rows are named in the generated frontier, not
here.

**Deviations from spec:** the phase-1 row is `safety_class = "spine"` where
the plan's draft said `ordinary` — it mints spine rows, and the spine class is
what serialises that; the phase-2 row's title says re-base, not retire, per
the ruling.

**Byte deltas on budgeted files:** none touched.

**pytest totals:** smoke tier under Git Bash **1378 passed, 6 skipped in 40.10 s** — the budget read **40.7 s vs 60 s → WITHIN**, the first reading inside the budget since the sitting's opening 23.3 s on 2026-08-29: the other sessions' processes had gone quiet (the box at 54 % at the sample), which is the condition every OVER reading of these two days lacked; one machine, one data point, the budget untouched; `gen_open_items --check`: current, zero pending
cards; `check_trajectory --strict`: exit 0 (five queued rows' `specref`
resolve, path and anchor; the DAG acyclic); `check_docs --stale`: 0 broken.
