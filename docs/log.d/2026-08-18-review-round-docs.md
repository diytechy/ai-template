## 2026-08-18 — the docs lane of the review round: the pack's silent backlog, a repealed rule still being taught, and the WI-455 residue

Two adversarial reviews (one external, one internal) filed eight findings against
the shipped prose surfaces. All eight verified; two grew a ninth on inspection.

### 1. The RESYNC pack had gone blind in two directions at once

**The backlog (M5 / Sol-F3, proved).** Three entries landed today ending
`*(Reserved, awaiting its [since <sha>]: …)*`, against 75 anchored ones;
`git show ff03d323:…/RESYNC_PACK.md | grep -c "Reserved, awaiting"` is 0, so the
backlog ran 0 → 3 in a day. An unanchored entry is not skipped loudly — it falls
in no stamp-to-target range, so a re-syncing adopter never sees it at all.
`tests/test_resync_pack.py` exempted `### Reserved:` headings from the anchor
check, which made the one unanchored shape the pack admits also the one shape
nothing counted.

**The second blindness (found while fixing the first, not in either review).**
Two of those three, plus the already-anchored `docs/architecture.md` RETIRES
entry, had been appended **after `## 5. Promotion`** — outside the §3/§4 bodies
the anchor grammar, the landing-order rule and §1.3's operator worklist all read.
Three entries, well-formed and unreachable.

**Stamped, from the commits that actually landed them:** the `docs/work/README.md`
entry → `712ff788`; artifact-voice-at-the-need-tier → `3dd665fc`; no-provenance-
in-a-living-cell → `4e9a5c8a`. All three moved into §3, and `c7adf7dc` moved back
into §3 at its 2026-08-14 date cohort (ahead of `bd0e739a`) so landing order
holds.

**The guard, and why this shape.** The obvious options were "backlog must be
empty" and "backlog bounded and listed". Empty wins, because the pack already
ships the escape hatch that makes it always satisfiable: **anchor at the
preceding commit and say so in a parenthetical** — four entries do exactly that
(`1337`, `1445`, `1460`, `1489` before this change), it resolves, it selects a
range one commit wide of correct, and it needs no follow-up commit to become
true. A bounded-and-listed backlog would buy nothing that convention does not,
at the price of machinery deciding how stale is too stale. So:
`test_a_reserved_placeholder_stays_anchor_free` becomes
`test_no_reserved_placeholder_survives_a_commit`, asserting **both** halves (the
shape rule still bites if emptiness is ever relaxed to a bound), and a new
`test_no_entry_hides_below_the_closing_section` asserts no `###` heading follows
§5. The convention itself is now written down in §3's preamble rather than
inferable from four worked examples. Reserving a slot deliberately means editing
an assertion — which is the point: it becomes an act with a reviewer.

### 2. A repealed permission was still being taught, in two places in the pack

**M7 (proved).** The artifact-voice entry's step 4 still read "Two things need
**no** waiver … a **provenance** citation (a spec of record; a retired artifact
named as the thing this need abolished) … Neither is a carrier" — the same §1(e)
carve-out `4e9a5c8a` corrected in `spine-authoring/SKILL.md` and missed here, ten
lines above the entry that repeals it. An adopter applies entries in order, so
they learn the permission, apply it, then meet its repeal. Step 4 now keeps only
the declared-vocabulary half and routes provenance to deletion, naming the next
entry by its anchor.

**Sol-F1 (confirmed).** The same entry justified excluding `.md` from the SN
artifact vocabulary because "a document named in a spine cell is usually a
*citation*, which §3's provenance clause already sanctions" — sanctioned by a
clause that no longer exists. The exclusion is right and stays; it is now
justified on a ground that is still true (a markdown name is rarely the
*instrument* that observes a condition — it is a document under specification or
a pointer to a home), with the citation case handed to the entry that bans it.

**Owed elsewhere, not applied (detector lane owns the file).**
`tests/test_trace_rules.py` carries the same stale justification in a comment.
Suggested wording: replace the "§3's provenance clause already sanctions it"
clause with *"a markdown name is rarely the instrument that observes the
condition, and a markdown name that IS a citation is forbidden outright by the
provenance rule rather than waived"*.

### 3. WI-455 merge residue in PROCESS.md (Sol-F4, confirmed — and it was wider)

§3 still said "**Architecture is generated** (module/function map) so it cannot
drift; keep a hand-written one-page overview above it." The merge deleted
`docs/architecture.md` and the scaffold no longer creates a home for that
overview, so the rule instructed an adopter to maintain a file that does not
exist. Rewritten to what is true: the map, import graph and seams derive live
from source + registries into the dashboard, and the one authored narrative that
survives is `docs/runtime-flows.md`.

Sweeping the neighbours found two more, both naming a step that retired with the
doc (`check.py:735` records the retirement): §7's process-check list credited
`gen_arch_map.py` with "architecture-map freshness" — contradicting §7's own
"The architecture views are derived from source + registries, so no map step is
owed" nine lines earlier — and the pre-commit floor and §8's `check.py` bullet
both still listed "map freshness" / "arch-map freshness". All three now say
generated-artifact freshness. `RESYNC_PACK.md` §2.2 carried the fourth: it told a
re-syncing adopter to preserve "`docs/architecture.md`'s hand-written overview
(regenerate only the marker blocks)" — now `docs/runtime-flows.md`'s authored
flows, pointing at the retirement entry.

### 4. Two registry templates never got the charter the ruling extended to them (N12, proved)

`system-requirements.template.toml:20`, `low-level-requirements.template.toml:19`
and `interfaces.template.toml:84` say the reason column takes the ARGUMENT, never
the CITATION. `stakeholder-needs.template.toml` — whose reason cell is `why`, and
whose tier is the one the ruling **added** — did not, nor did
`test-cases.template.toml`. The SN `why` charter now carries the clause in the
LLR template's wording, and notes that `why` IS the tier's reason cell (the
schema has no `Rationale`). The TC tier has no reason cell at all, so the clause
goes in its schema header over the three living cells (`method`, `expected`,
`parameters`), with the one distinction that tier needs stated: an SR/LLR id in
`expected` is a trace link, not a citation frame.

### 5. Byte budgets: the capped rows had gone stale, and one file is parked (N6, N7 — both proved)

The WI-455 merge re-stamped the *watched* rows and left the *capped* ones, so two
of three capped baselines were fiction. Re-measured and re-stamped replace-style
in all three copies (source + `.claude/` + `.agents/`, byte-identical):

```
Byte deltas, one line per touched file:
project-trajectory/AGENTS.template.md   stamped 9,994 -> actual 9,953 (cap 10,000; 47 free, 0.5%) — not edited, stamp corrected
CLAUDE.md                               stamped 6,677 -> actual 6,805 (cap 8,500; 1,695 free, 20%) — not edited, stamp corrected
project-trajectory/skills/byte-budget-guard/SKILL.md  4,206 -> 4,636 (cap 5,000; 364 free, 7%) — the re-stamp + the parked-at-the-cap note
project-trajectory/PROCESS.md           82,190 -> 82,448 (+258, watched) — the architecture residue above
project-trajectory/PROCESS_OPTIONS.md   173,374 -> 173,374 (untouched)
```

N7's finding is that nothing recorded `AGENTS.template.md` sitting 47 bytes under
its cap while every other capped file holds 7–20%. The cap is not the defect — it
reserves ≥2k under Gemini's ~12k truncation for the adopter's own section — so the
skill now states the file is parked and that an addition there must be paid for
by a cut there, in the same edit. `AGENTS.template.md` itself was not touched.

### 6. The flows lane's owed entry

`docs/log.d/2026-08-18-review-round-flows.md` proposed verbatim RESYNC text for
the `check_flows` title-shadowing fix: an adopter who followed the
architecture-retirement entry may hold a `docs/runtime-flows.md` whose only
"Runtime flows" heading is its H1, which is green-and-unfailable today and a hard
FAIL after the fix. Added to §3 as **The flows gate stops matching your document
TITLE**, anchored `[since 4e9a5c8a]` under the preceding-commit convention (the
round is not committed, so the landing SHA is not knowable) with the
parenthetical that convention requires.

### DEFERRED — the `13v` token, awaiting the detector lane's ruling

The waiver token is itself a decision id, mandated into the very cell §3 now bans
decision ids from. Left untouched, verbatim, pending the resolution. The lines
that will need it, in this lane:

- `project-trajectory/skills/spine-authoring/SKILL.md:92` — "as the same `13v`
  token the SR valve uses" (the SN artifact-naming waiver).
- `project-trajectory/RESYNC_PACK.md:1665` — step 3 of the artifact-voice entry,
  "the same `13v` token the one-`shall` and SR artifact valves already use",
  written into `Rationale` at SR / `why` at SN.
- `project-trajectory/PROCESS.md` carries no `13v` literal; its two valve
  bullets (§3 "one requirement, one `shall`" and the artifact-naming bullet)
  say "a recorded per-row waiver" without naming the token, so they need no
  edit unless the resolution renames the concept rather than the token.
