# ADJUDICATE — WI-697 — first judgement of TC-279 (DA-011) at f2bc66c1

This is the first judgement of TC-279, the observation of DA-011: whether the
sampled new-reader inspection holds. The adjudicator is Claude Opus 5.5. It
directed none of the sample, authored none of the five parts, and had read none
of them before this sitting.

What the judgement used:

- the declared inputs: the rubric `docs/rubrics/sampled-new-reader.md` at
  `1f1dc64e` (R1, R2, B1, B2) and DA-011;
- the procedure in `docs/test/inspection-procedures.md#sampled-new-reader-inspection`;
- TC-279's cells: SampleSize 5, the AcceptanceRule and the Expected;
- for each part, its code and its linked SR and LLR rows, read at `f2bc66c1`.

The coordinator took the draw and ran the five readers; this sitting judged
them. Each statement is recorded beside its rows in
[SAMPLE-f2bc66c.md](SAMPLE-f2bc66c.md).

- [BLOCKER] The draw honours the procedure: its population, its part definition and its randomness -> **Randomness: honoured.** The seed is the integer of trunk HEAD `f2bc66c1`, fixed before any reader ran and chosen by no author. `random.sample` was run over a sorted frame, and I re-ran it at `f2bc66c1` and got the same five parts. **Part definition and population: NOT honoured.** The procedure defines a part as "one function, class or module-level block with its own back-link". The frame was "a function or class whose docstring contains `Implements:`" (423 parts). The kit's own harvest of back-links (`gen_arch_map.declaration_sites`, under `[paths] src`/`tests`) finds about 516 back-linked parts. The frame left out about 101 of them, roughly a fifth, and none of them could be drawn: 8 module headers, about 82 module-level blocks back-linked by a `# Implements:` comment, and about 11 functions back-linked by a comment above the `def` (mostly `main`). The frame also included 8 functions whose docstrings only mention `Implements:` and carry no back-link, such as `trace._implementing_modules`. The excluded stratum is exactly what DA-011's Obstacle is about: a sample that systematically misses a kind of part. So no pass can be recorded on this draw.
- [MINOR] R1: each drawn part was read by a fresh non-author session, and the reader kind and statement are recorded beside the linked rows -> Holds for the five drawn parts. Every reader file names a fresh Claude Sonnet 5.5 session, told that it did not author the part, that read only the part's code and the rows its `Implements:` names. The record is now `SAMPLE-f2bc66c.md` plus the result section. Two gaps: (a) the readers' records do not say they read the rows "through the generated views", as the procedure asks, so this sitting cannot confirm it; (b) "randomly drawn" holds only within the defective frame above.
- [MINOR] Part 1, `session_keep.write_tombstone` (SR-227, LLR-270) -> **Agrees.** Reader 1's account matches the code: a lockless, whole-file `.retire` marker naming the session, the reason and the holder. Its purpose matches LLR-270's tombstone clause and SR-227's "retire it at once when a call on it fails". The inferred shape of `keep` is correct.
- [MINOR] Part 2, `session_keep.load_honoured` (SR-227, LLR-270) -> **Agrees.** Reader 2 described the behaviour exactly, including the edge it flagged. That edge, a tombstone removed unapplied when the record is not a dict, is a corner-case rationale and does not count against explaining the behaviour or purpose (not B1). `store_load` returns None only for a record that is absent, unreadable or not this route's, and its docstring says that "reads as 'no session', and the next launch mints". No retained session is left for the tombstone to retire, so deleting it is clean-up. The rows' tombstone rule concerns a live record and is not contradicted.
- [MAJOR] Part 3, `kitlib.spine.sn_all_ids` (SR-189, LLR-215) -> **Agrees on purpose and the main behaviour, with one branch misstated; I rule this short of B1. It is the sample's closest call.** Reader 3 correctly gives the part's job: the single need-id universe, narrowed under TOML to the `[need.*]` tables so that stakeholder-prose ids stay out, for both the stage derivation and the orphan listing. That is LLR-215's rule. The reader also says "TOML with no `need` table get[s] a whole-text scrape", which is wrong. I called the function at `f2bc66c1`: a parsed TOML document with only a `[stakeholder.*]` table returns `set()` both with `carrier='.toml'` and with no carrier. Only markdown, and `.toml` text that does not parse, take the whole-text scrape. On that input the reader's version would admit stakeholder prose, which LLR-215 rules out. The code keeps to the row; the reader misread one fallback. Why this is not B1: the reader explained both what the part does and why it exists, and its account of the rule the rows state agrees with them. The slip concerns a degenerate input (a needs file with no need tables) that no live registry presents. A stricter reading of "contradicts the linked rows" would make this a failing sample. If a person reads it that way, the act is `record_observation.py --tc TC-279 --outcome fail`.
- [MINOR] Part 4, `trace.triangle_findings` (SR-157, LLR-002) -> **Agrees.** Reader 4's account matches the code line for line. The call site, `integrity += triangle_findings(...)` at trace.py:5453, confirms the always-on integrity-floor placement LLR-002 gives the reason for. The inferred `refs` (`kitlib.spine.refs` splits a multi-ref cell) and `ID_PATTERNS` are correct.
- [MINOR] Part 5, `traj_render._cedge_marker` (SR-054, LLR-105) -> **Agrees.** It returns a per-ink `cedgearrow-<hex>` marker and the higher-contrast white or near-black ink for a hex fill, and the plain marker with `None` for a theme token. Its stated purpose matches LLR-105: the 3:1 floor per fill in both themes, the measured 1.06:1 and 1.99:1, and the marker that cannot inherit `--ring`. The inferred `_ring_ink` is correct: it returns one of `RING_INKS`.
- [MINOR] B1, any reader who cannot explain a part or who contradicts the rows -> Does not hold, by the ruling on part 3 above. All five readers stated both behaviour and purpose without asking the author, and on all five parts each account of what the part is for agrees with its rows. Every helper inferred from its name was inferred correctly. None of these randomly drawn parts falsifies DA-011.
- [MINOR] B2, no author-selected sample and no claim about unsampled parts -> No author chose the sample, and this verdict claims nothing about parts the sample did not reach. Even on a valid frame, a passing sample bounds discovery to the five parts read and does not show that DA-011 holds elsewhere.

**Outcome.** No B anchor holds, so no `fail` is recorded. The frame does not
match the procedure's definition of a part, so no `pass` is recorded either.
Nothing was written to `docs/test/observations/`.

**What is owed, against TC-279's Expected.**

- Redraw five parts from the full part population: every function, class and
  module-level block with its own back-link, as `gen_arch_map.declaration_sites`
  encloses each `Implements:` line under the declared roots. Use a seed fixed
  before reading, such as the trunk HEAD at the redraw.
- Give each part to a fresh non-author reader that reads the rows through the
  generated views, and record that in each reader's record.
- Record the result with `python project-trajectory/scripts/record_observation.py --tc TC-279 --outcome pass|fail --by "<adjudicator; readers>"`.

Separately, a person may overrule this sitting's part-3 ruling and record
`fail` on this sample.

## Non-blocking findings (surfaced, not acted on)

1. The procedure says what a part is, but not how to enumerate the population.
   That left the drawer to write its own frame, and the frame drifted. Naming
   the enumeration would make the draw reproducible by construction: a function,
   class or module-level block enclosing an `Implements:` line, as
   `gen_arch_map.declaration_sites` reads it.
2. This result section sits inside `docs/test/inspection-procedures.md`, which
   TC-209, TC-210 and TC-211 declare as an input. Every TC-279 result written
   there therefore moves their inputs digest. Their records were already stale
   at `f2bc66c1`, after WI-747's edit, so this sitting costs nothing new; this
   is the same smell WI-686 and WI-688 surfaced.

OUTCOME: NEEDS-JUDGEMENT result=-
