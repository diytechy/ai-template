## 2026-08-30 — WI-549: spot-check the clean close of WI-548

Adjudication spot-check (`docs/process.toml [attestation] complete_review = 'sample'`)
of the GREEN close of WI-548 (stall-guard C1–C7,
`docs/archive/work/complete/WI-548-stall-guard-route-aware.md`). One question:
does what shipped answer what the row asked for? A finding is a successor row,
never a reversal — the close stands.

### Method

Read the WI-548 spec `## Deliverable` (C1–C7 + adopter-compat per the plan §6)
and the plan of record `docs/plans/2026-08-30-stall-guard-plan.md`, then
spot-checked each claimed deliverable against the shipped tree at the claim base.

### What was verified present (sampled, not a re-review)

- **C1** route-aware stall: `agent_loop.RoutingState.note_session(judging=)`,
  `note_review_draw_failure` (agent_loop.py:1235/1261, called at 2390/2399/3062).
- **C2** `EXIT_REVIEW_OWED = 9` (agent_common.py:147, re-exported agent_loop.py:210);
  `dispatch.py:529` special-cases it (not a decided handback outcome).
- **C3** `idle_timeout` slot in agent_session + `AGENT_SESSION_IDLE_TIMEOUT` /
  `--session-idle-timeout` in lane.py, both `agent-resume.template.{sh,cmd}`.
- **C4** `probe_route` / `select_with_probe` (agent_loop.py:2976/2997).
- **C5** relaxed same-family rung: `round_relaxed`, `note_review_family`,
  `-relaxed` verdict suffix, `# heterogeneity: relaxed` header (agent_loop.py
  1034/1200/1257/2216/2808).
- **C6** integrate.unload sheds `out/run-logs/` streams + `out/review-owed`
  marker as declared residue (integrate.py:1742-1744, with prose 1729-1730).
- Adopter-compat surfaces present in RESYNC_PACK.md and PROCESS_OPTIONS.md.

- **C7** reviewer brief renders `{trunk}` / `{process_doc}` as slots
  (reviewer.template.md:15-16), the three-dot diff with generated/telemetry
  exclusions carried.
- **Adopter-compat (plan §6):** exit 9 / `EXIT_REVIEW_OWED` documented at the
  end of the alphabet in PROCESS_OPTIONS.md:706, relaxed rung 714, probe 718,
  idle deadline 1113. RESYNC_PACK.md carries the stall-guard change-set entry
  (line 2376, `[since 959c5996]`) PLUS the two entries the previous run owed:
  the check_docs HTML-comment fix (2355, `[since 59f52549]`) and the opencode
  `--dir .` fix (2365, `[since 59ab2951]`).
- **C6 close rituals** shipped verbatim in both briefs: worker.template.md:36
  (Deliverable-before-Context, specref cleared, trace.py --approve when spine
  rows minted, spec_move to terminal folder) and adjudicate-disposition.template.md
  (draft in this spec's `## Dispositions` as top-level keys, title ≤ 120,
  adjudicator closes its OWN row — lines 42/50).

### One probe resolved, not a finding

The C3 deliverable says the idle slot lands in "all four launchers." Six
launcher files exist (`agent-resume.{cmd,sh,command}` live + `.template.`
each), and `AGENT_SESSION_IDLE_TIMEOUT` is present in only four — both
`.command` files lack it. That is CORRECT, not a gap: the `.command` (macOS
Finder) wrapper is a thin `exec ./agent-resume.sh "$@"` that declares **no**
slots of its own by design (WI-274 — the dials live once; it inherits every
slot from its twin by exec, proven by tests/test_launcher_interpreter.py).
"Four launchers" = the four slot-carrying launchers (`.sh`/`.cmd`, live +
template); the slot is in all four. Template/live parity is separately
enforced by test_dogfood_sync, green at the close.

### Verdict

The shipped work answers what the WI-548 row asked for. Every C1–C7 deliverable
and every adopter-compatibility surface named in the row (and the plan §6) is
present in the shipped tree and matches the ask; the close was GREEN and
cross-family reviewed. **No successor row, no open item, no reversal — the close
stands.** This is the `sample` attestation (`docs/process.toml [attestation]
complete_review`) doing its intended job: a spot-check of a success that finds
the success genuine.

Full suite not re-run: the close already recorded it green (3175 passed, 16
skipped, 861.84 s at 777bbbfe) and this spot-check is read-only — it added no
product code, only this log fragment and the spec close, so there is no new
runtime surface to exercise.
