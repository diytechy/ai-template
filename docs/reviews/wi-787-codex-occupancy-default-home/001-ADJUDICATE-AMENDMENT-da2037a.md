# ADJUDICATE (amendment): WI-787, LLR-267 and LLR-290 `detail` at da2037a7

An independent spine adjudicator (Claude Opus) judged this amendment. It made none of the
changes it judges. The judgement used the kit brief composed for this lane's merge, read in the
lane as the owner directed on 2026-10-03 (S11). The anchor is
`docs/archive/last_approved/docs/requirements/low-level-requirements.toml` (copied 2026-10-03,
commit a9791303). A row-by-row comparison of that copy with the live registry finds exactly two
moved cells: LLR-267 `detail` and LLR-290 `detail`. In each, only the clause that says where the
codex rollout is read moved:

- LLR-267 before: "...under the launch environment's CODEX_HOME, and blank with no CODEX_HOME."
- LLR-267 after: "...under the launch environment's CODEX_HOME or, when that is unset, under
  codex's own default home, and blank when no rollout for that thread id exists there."
- LLR-290 before: "...from the exact thread rollout under the launch CODEX_HOME, and..."
- LLR-290 after: "...from the exact thread rollout under the launch CODEX_HOME, or codex's own
  default home when that is unset, and..."

- [MEANING] LLR-267 detail -> before: codex occupancy (used, window, pct) is read from the rollout
  for exactly this thread id under the launch environment's CODEX_HOME, and when the launch sets
  no CODEX_HOME all three are blank: no home is looked up -> after: with CODEX_HOME set, the same
  read; with it unset, the rollout for exactly this thread id is looked up under codex's own
  default home and occupancy is filled from it; blank only when no rollout for that thread id
  exists under the resolved home -> not the same: the unset case moved from "always blank" to
  "read from the default home". The old text's correct implementation (blank with no CODEX_HOME)
  fails the new text whenever a default-home rollout exists, and the new behaviour reads a
  location the old text kept out of scope. The CODEX_HOME-set case and every claude, opencode and
  pct clause are unchanged.
- [MEANING] LLR-290 detail -> before: compacted entries and per-request input counts come only
  from the exact thread rollout under the launch CODEX_HOME, so with none set there is no
  readable rollout and no new compaction inference -> after: the same read under the launch
  CODEX_HOME, else under codex's own default home, so an unset launch now yields rollout prompts,
  reported compacted entries and inferred drops -> not the same: the unset case moved from "no
  rollout, no inference" to "rollout read from the default home". The old text's correct
  implementation records nothing where the new text requires compaction evidence. Every clause
  after the first sentence is unchanged.

## Would this adjudicator bless the new text? Yes, both rows.

Checked against the code (`session_adapters.py` at da2037a7):

- `_codex_home(env)` returns `Path(env["CODEX_HOME"])` when that is set and non-empty, else
  `Path.home() / ".codex"`, or None when no user home resolves. `_codex_rollout(env, thread_id)`
  globs `sessions/**/rollout-*-<thread_id>.jsonl` under it and returns "" with no match, no home
  or no thread id. Both `CodexAdapter.context` and `CodexAdapter.compaction` read through it.
  This is what both cells now say.
- `session_service.act` passes the launch environment (`os.environ` when the call has no own
  `env`; a retained call's dedicated home merged over it), so "the launch environment's
  CODEX_HOME" names what the code reads. A retained route's dedicated home and a roster `Env`
  CODEX_HOME still win, as PROCESS_OPTIONS.md's "`Env` merged over the inherited environment"
  and OI-69 (e1) require.
- The rationale that justified the old blank was "an ambient home could hold another route's
  thread". The new text still keys the lookup on exactly this thread id, which codex minted for
  this launch, so no other session's file can be read. LLR-267's own rationale (blank rather
  than guessed) still holds: a value read from the thread's own rollout is not a guess. Nothing
  in SR-222 or SR-227 is contradicted. SR-222 leaves blank only "what the loop cannot read from
  the runner's output", and SR-227's drain needs this occupancy.

Mutation probes, on a scratch export of the lane (tests/test_session_adapters.py,
test_session_keep.py and test_session_service.py; 128 pass unmutated). Each probe was killed:

| Probe on `session_adapters.py` | Failing test(s) |
|---|---|
| M1 unset CODEX_HOME resolves to no home (the old rule) | `test_codex_occupancy_falls_back_to_codexs_default_home` |
| M2 the default home beats an explicit CODEX_HOME | `test_an_explicit_codex_home_wins_over_the_default` and 11 others |
| M3 the glob matches any thread's rollout | `test_codex_occupancy_stays_blank_without_this_threads_rollout`, `test_codex_unrelated_rollout_cannot_report_compaction` |
| M4 `compaction` keeps the old explicit-only read | `test_codex_occupancy_falls_back_to_codexs_default_home` (its compaction assertion) |
| M5 `context` ignores the launch env | `test_an_explicit_codex_home_wins_over_the_default` and 3 others |

Observations that do not block the blessing:

- "When that is unset": the code also treats a set-but-empty CODEX_HOME as unset. That is the
  only sensible reading of an empty value, and the old code (`if not home`) treated it the same
  way, so it is not a divergence.
- "codex's own default home" is resolved from the kit process's user home, not from a HOME or
  USERPROFILE that a route's `Env` might override. No shipped route does that, and the cell's
  wording is right at its level. A route overriding the user home without setting CODEX_HOME
  would be read from the wrong place; this is noted for WI-788 (per-route homes), not owed here.

VERDICT: MEANING rows=2
