## 2026-08-14 — WI-451 slice 2, act 6: the re-iteration pass — two owed calls closed, the Aspect conversion finished in the docs, and the layer read top-down

The method's `re-iterate — top-down again` step (`2026-08-14g`), plus the two
calls the ledger carried as owed. Full detail:
[plans/2026-08-14-wi451-slice2-ledger.md](../plans/2026-08-14-wi451-slice2-ledger.md).

**The two owed calls, closed on evidence rather than judgement.**

- **SR-043's migration window: KEEP.** Driven, not assessed —
  `subagent_gate.py` declares `LEGACY_POLICY = "docs/subagent-gate"` and
  `read_process_policy` falls through to it, and both `agent_common.PROCESS_KEYS`
  and `bootstrap.py --migrate-config` still carry the legacy key. Same standard
  as SR-067's and SR-042's keeps — and SR-131's window was CLOSED on that same
  standard, which is what makes these keeps a finding rather than a default.
- **The child/parent phase spread (38 vs a base of 19): RECORDED AS INTENDED**,
  with the analysis rather than a shrug. All 38 sit under six parents, and
  **three of those six are already in the base 19** — the campaign concentrated
  a pre-existing phenomenon rather than inventing it. Aligning them would either
  falsify when work shipped or split parents per phase, re-fragmenting the layer
  this campaign consolidated. Failure direction checked: a draft child drops
  *its own* phase's gate, i.e. toward more scrutiny.

**Act 5's conversion was half-done, and this act finished it.** The registry,
carrier schema and shipped template had moved to `Aspect` while
`PROCESS.md`, `PROCESS_OPTIONS.md`, `EXAMPLE.md`, `MULTI_REPO.md` and
`KICKOFF_PROMPT.md` all still TAUGHT `Area` — an adopter following the worked
example would have authored a column the carrier no longer declares. **Two
traps in that sweep, both the opposite of a mechanical rename:**

1. `Lifecycle` was documented as *"mirroring `Area`"* — an **OPEN**
   project-named vocabulary. Re-pointing that analogy at `Aspect` would teach
   the exact opposite of the new rule, since `Aspect` is **CLOSED**. Struck,
   not re-pointed.
2. `Area` was an **ownership** tag and `Aspect` explicitly is not one. Every
   domain-hat and module-partition passage re-anchors on the LLR
   `Module`/component — decision 10's own reasoning (25 of 31 values were a
   component by another name) applied to the prose.

**Surfaced rather than buried:** retiring `Area` from the shipped template
removes an adopter capability — a free-text owner/domain tag — that `Aspect`
does not replace. The dogfood rule forces it (`test_dogfood_sync` pins template
structure to the live registry), so it follows from the ruling; it is named
here and in the `RESYNC_PACK` entry because adopters will notice.

**Byte deltas:** `AGENTS.template.md` 9,994 → 9,994 (unchanged; 6 bytes of
headroom under 10,000). `PROCESS.md` 73,617 → **73,819 (+202)** — §1's
domain-hat paragraph re-anchors on `Module`/component and NAMES `Aspect` while
stating what it is not; that distinction is the whole +202, and without it a
reader finds the old tag gone and reasonably assumes the new one replaces it,
which is the confusion the ruling's *"REVIEW grouping, not an ownership claim"*
wording exists to prevent. `PROCESS_OPTIONS.md` 171,916 → **171,869 (−47)**.
Both baselines re-stamped in all three tracked skill copies, same commit.

**The top-down read (independent, fresh context) produced a RANKED FINDINGS
LIST — a deliverable per 13s, not a failure.** Two were fixed here:

- **SR-152 carried a FALSE acceptance criterion**, self-inflicted in act 2: it
  asserted the B-04 pairing was *"cross-referenced from theirs"* when no B-04
  row cited SR-152 at all — and asserting registry prose is not testable
  anyway. Removed.
- **§1R.6's explicit instruction was unexecuted:** the honest limit belongs IN
  the B-04 crossing's SR, and `--no-verify` appeared only in a B-07 row's
  rationale. **SR-019 now states it** — a local floor, bypassable by the
  session, discharging its claim only as a PAIR with the hosted re-run. (The
  first two wordings tripped the form checker's `can`/`will` rule; the third
  passes, and `form-findings` is back to the two recorded waivers.)

Nine findings remain OPEN and ranked in the ledger — the frame's own named
B-05 observable (the package/MAPPING manifest) has no row; three (SN-025,
loop-selection) duplications of the SR-141 class; SR-031/SR-137 stating one
observable twice and already diverging; four rows that escaped demotion against
the campaign's own criterion; three needs with zero textual coverage despite
`orphans=0`; and the fast-authored mints' placeholder/dead-clause issues. None
is a regression: each names a state the pre-campaign registry also had, or a
gap this campaign's own mints introduced and this pass caught **before** the
owner's sitting rather than after it.

Bar: `pytest -q -n auto -m smoke` → 1134 passed, 7 skipped;
`trace.py --strict --strict-schema` → `orphans=0 integrity=0 schema-findings=0
form-findings=2`; `check_docs` OK.
