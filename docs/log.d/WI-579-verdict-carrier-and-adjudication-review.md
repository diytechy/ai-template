## 2026-09-02 — WI-579: the verdict carrier, tree identity, and the `adjudication_review` dial

The lane for the OI-76 build (ruled 2026-08-31: **B with C and the generated
rollup; governing = TREE IDENTITY**), consolidated with WI-559 DW2 and WI-560
DW1 by the 2026-09-02 backlog restructure (plan §2.2). The spec of record is
`docs/work/active/wi-579-the-verdict-carrier-and-the-ad/`, whose Done-when
quotes the absorbed rows verbatim.

### What was read before anything was written

- `integrate._verdict_gate` (`integrate.py:1279`): reads
  `docs/reviews/WI-<n>-REVIEW-A.md` per `merged` WI, parses its `VERDICT:`
  line, and compares that file's last commit time against `_last_commit_time`
  over the work tip excluding `docs/reviews` and `docs/log.d`. Nothing in the
  kit writes that file — the plan's finding (a).
- `agent_loop.review_owed_by_evidence` (`agent_loop.py:3206`): the C2
  derivation, which asks a DIFFERENT question — "does any round file name
  HEAD's short sha?" — over a DIFFERENT exclusion set (none). That is the
  double-identical-round class WI-560 DW1 names.
- `agent_loop.NON_BUILD_PHASES` contains `ADJUDICATE`, so
  `build_bookkeeping` never calls `schedule_review_round` for a committing
  adjudication; `integrate._verdict_gate` nonetheless demands its REVIEW-A.
  Every adjudication merge is therefore a supervisor stop (the plan's §0).
- Round files are `docs/reviews/<train>/<NNN>-REVIEW-<X>-<sha7>[-relaxed].md`,
  written by the reviewer session and committed by it; the loop commits the
  session log `docs/iteration/<train>-<NNN>-<stamp>.log`, whose `# phase:`
  header is the LOGGED-SESSION anchor the plan's finding K needs.

### The shape being built

1. `kitlib/verdict.py` — one home for the verdict record: the non-record tree
   identity (`docs/reviews`, `docs/log.d`, `docs/iteration` excluded), the
   `Review-Verdict:` trailer grammar, the round-file/session-log join, and the
   governing-verdict decision. Pure functions plus thin `git_out` readers, so
   both readers (the merge slot and the C2 derivation) stand on ONE definition.
2. `integrate._verdict_gate` recomputed over that evidence; the freshness
   comparison retires into identity. Migration window: a legacy hand-authored
   rollup still clears the gate, with a WARN.
3. `agent_common.adjudication_review_owed(docs, brief, drafts)` + the
   `[attestation] adjudication_review` dial, read by BOTH the round scheduler
   and the gate.
4. `gen_verdict_rollup.py` — the per-train (= per review scope, LLR-140)
   rollup as a GENERATED artifact with `--check`, declared in
   `docs/stack.ini [generated]`, never read by the gate.

Deferred open items: none — OI-76 is ruled and this row is its build.
