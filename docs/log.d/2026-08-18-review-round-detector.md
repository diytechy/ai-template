## 2026-08-18n — the citation-frame detector, corrected against two adversarial reviews

The warn-first provenance detectors that landed at `4e9a5c8a` under the
`2026-08-18m` ruling were reviewed twice, adversarially. Eight findings; every
one was re-verified against the live registries before anything was changed, and
every one held. What follows is the correction, with the measurement that decides
each call. **Provisional like its parent** — no `status` cell moved, nothing was
attested, the re-attest sitting countersigns.

The four registries this lane could touch are the SR tier, `components.toml`,
`external.toml` and `docs/provenance-allow`. Frames the corrected detector reports
in `low-level-requirements.toml`, `test-cases.toml` and `interfaces.toml` are
**left standing as a worklist for those lanes** and named in §6.

---

### 1. The review-round arm was 100% false and is GONE

`_REVIEW_CODE_RE` (`\bC-[A-Z]{2,5}-\d+\b`) shipped with the commit message
claiming a "measured false-positive rate 0 of 319". Re-measured over every live
spine and IF cell: **20 hits, 20 of them false.** Every live `C-<HAT>-<n>`
occurrence names a hat-charter CLAUSE as the standing constraint the row answers
— "C-MNT-3 gives every declared vocabulary value exactly one normative
definition", "C-PRF-1 wants a declared improvement", "…is the MAINTAINER clause
this row answers" — which is a constraint cited like a standard's clause, i.e.
the row's REASON. It is the same subject-noun hazard the module's own design
notes claim to guard, recurring in a shape nobody had measured.

The arm is **removed, not narrowed.** The token carries no signal about which use
it is; the FRAME around it does, and a frame is what the two edit-stamp arms
already detect. Where a clause code genuinely rides inside a stamp ("REWORDED
2026-08-17 (C-PRF-1, applied)") the stamp is reported and the whole frame is what
gets stripped, so removing the arm loses no catch. Pinned by three negative tests.

### 2. The exception list is TOKEN-SCOPED

`docs/provenance-allow` suppressed at CELL granularity while every entry
justified ONE token — 15 of them read "unsigned derived-requirement label",
which is the `(Derived-requirement label, added <date> — PROVISIONAL,
unsigned.)` parenthetical and nothing else. Re-running detection with the list
ignored exposed **67 tokens over 22 rows** that no reviewed reason had ever
named, `RE-VOICED 2026-08-17` and `Minted at the owner's 2026-08-15` among them
— the banned shape itself, riding a carve-out written for a label. Meanwhile
`docs/test/report.md` asserted "None. No living spine cell carries a citation
frame."

The key is now `<ROW-ID> <Cell> <token>`, matched against the token as the
detector reports it, whitespace-collapsed and case-folded. **A two-field key
declares NOTHING**, which is what made the migration self-enforcing rather than
optional. Three entries (IF-123/127/130) turned out to justify only the
`PROVISIONAL` marker, which is not a citation token and was never reported — so
they had been suppressing other people's frames for free. They are retired, in
place, with the reason recorded. `tests/test_trace.py` now fails if any entry in
this repo's own list matches no live token.

### 3. The stamp that lost its date

The 2026-08-18 sweep used `_EDIT_STAMP_RE` (verb + ISO date within one clause) as
its definition of done and deleted the DATES, leaving the verbs: "MINTED
2026-08-17 (Sol F18, applied) out of SR-170" became "MINTED out of SR-170" and
went silent. **33 such tokens survived on 31 live rows.**

`_CAPS_EDIT_STAMP_RE` reads the corpus's own convention — an ALL-CAPS verb
opening a clause, optionally behind up to four all-caps subject words ("OWNER
RE-POINTED:", "CROSSING ATTRIBUTION EXAMINED AND CONFIRMED:"). The clause-opening
constraint is the entire separation from the participle hazard: `RATIFIED`,
`RETIRED`, `DELETED`, `RULED` and `AMENDED` are also ordinary participles
mid-sentence ("a RATIFIED SN cited by zero SRs", "a stale file is DELETED in the
same act"). **Measured over every live spine + IF cell: 36 hits, 36 genuine
stamps, 0 false.** `provisional` is excluded from this arm's verb set — it is an
adjective, never an edit, and 17 rows write it as a label's status.

A prefix word must be TWO letters or more. With `*`, the article in "A RATIFIED
SN…" read as an all-caps subject whenever the sentence opened a cell; the
negative test is what found it.

**Known and accepted under-detect**, stated so it is never implied as covered: a
mid-clause passive stamp ("the anchor is RE-BASED onto…", "it SPLIT rather than
moved whole") stays silent. Extending to copula + caps-verb was measured and
REJECTED — it buys four catches and one false accusation on TC-167's "a stale
file is DELETED in the same act", which is a normative behaviour statement and
exactly the class this rule must not touch.

### 4. CMP and EXT are guarded

`components.toml` and `external.toml` were swept in the same pass that guarded
the four spine tiers, then left unwatched — a clean state nothing was watching.
`off_spine_advisories` covers CMP `Name`/`Notes` and EXT `Name`/`Description`/
`Notes`, sharing one engine (`cite_advisories`) with the spine rule so there is
no second copy to drift. `Description` is read as NORMATIVE and `Notes` as the
reason cell, the same split the spine uses. B-## and REL-### carry no reason cell
(`Carries` and `Flow` state what crosses) and are deliberately absent. The guard
found one live frame immediately: EXT-005's `notes`.

They join the SPINE advisory list rather than taking a counter of their own —
one ruling, one worklist, and a second counter would invite a reader to clear the
spine and call the ruling discharged.

### 5. Three narrower corrections

* **The gating class-1 message named a dead carrier.** It told an author to
  "move provenance to work-items.csv / the log's Decisions". `work-items.csv` is
  retired and its presence is itself an integrity finding, so the lint was
  naming a forbidden file as the place to move provenance TO. The three
  neighbouring messages were re-pointed at the log in the same-day sweep; this
  one was missed. Now: "move provenance to the log".
* **Path suppression covered one date arm.** It was keyed on
  `rx is _ISO_DATE_RE`, so a pure pointer fired as an edit stamp whenever the
  verb landed inside the 24-character window: "restated in
  docs/plans/2026-08-16-blind-derivation.md" reported while the longer "moved to
  docs/archive/specs/parallel-wi-dispatch.2026-07-20.md" went silent — hit or
  miss decided by filename length. Both date-bearing patterns now carry a named
  `date` group and the suppression is keyed on that.
* **This repo's own ruling stamp was invisible.** `_ISO_DATE_RE` was
  `\d{4}-\d{2}-\d{2}` while rulings are letter-suffixed (`2026-08-13u`), so
  `provenance_tokens("The owner ruling 2026-08-13u settled this.")` returned
  `[]`. Twelve such tokens sat in `docs/requirements/*.toml`. The suffix must END
  the token, so `2026-08-13until` is correctly refused.

### 6. The waiver marker is renamed: `13v` → `recorded waiver:`

`13v` is a DECISION ID (log decision 2026-08-13v), and the kit mandated it into
the very reason cell §3 now bans decision ids from — a self-contradiction shipped
in four places. **Renamed rather than exempted**, on three grounds:

1. **It ships downstream.** An adopting project has no decision 2026-08-13v, so
   the kit was instructing every adopter to cite a ruling they can never read.
   That is the defect the provenance rule exists to prevent, shipped as an
   instruction. A declared exception would have entrenched it.
2. **Machinery should read as itself.** A control word an author writes to claim
   an exception is like `fan-out re-stamp:`; naming it after the meeting that
   authorized it makes a reader resolve a citation to learn what a keyword means.
3. **The colon earns its keep.** `\b13v\b` matched prose ABOUT a waiver as
   readily as a claim of one — measured, its only two live hits were SR-140 and
   SR-147, whose rationales say the waiver is SPENT. A stale sentence was
   standing as a live valve.

No live row used the marker as a working valve (neither SR-140 nor SR-147 names
a `.py` in `requirement`), so nothing needed a replacement marker; both spent
mentions were swept with the rest of §7. **`PROCESS.md`, `skills/spine-authoring/
SKILL.md` and `RESYNC_PACK.md` still carry the old token and are another lane's
to change** — the exact replacement wording was handed over with this fragment.

### 7. The sweep

31 SR rows and one EXT row re-voiced: drop the frame, KEEP the reason as standing
prose. Bare edit-verb stamps (SR-006/007/027/070/137/139/140/148/154/156/160/162/
168/169/170/171/173/174/178/179), dated stamps and bare dates no allow entry
justified (SR-024/033/052/111/112/129/144/147/149/150/167/175/176/177),
`OI-21` (SR-149), `sitting-3` (SR-175/176/177), the `13v`/`13p` decision
references (SR-140/147/148/156/160), and EXT-005's `notes`. Also fixed: the stray
leading space at `system-requirements.toml` SR-171's `rationale = """ This…`,
left where a stamp was cut out — swept for siblings, it was the only one.

Raw detector output over the live registries, exception list ignored: **82 tokens
over 49 cells → 39 over 27.** With the exception list applied, 8 findings remain,
every one of them outside this lane and left deliberately: IF-043/117/127/128/130
`Notes`, LLR-158/178 `Detail`, TC-153 `Method`.

### 8. What is NOT changed

Severity. Every arm touched here is **warn-first and stays warn-first** — the
repo is mid-program at *DevStg-Reqs* and a gate would stop the harness on a prose
campaign. `exit_code` is untouched; the gating class-1 rule keeps exactly its
current severity and only its message text moved.
