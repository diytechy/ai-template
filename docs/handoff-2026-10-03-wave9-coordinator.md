# Handoff 2026-10-03 (wave 9, coordinator): ladder dropped, TC-279 recorded, the cadence rows settled

For the next session's **coordinator**. This replaces
[handoff-2026-10-03-wave8-coordinator.md](handoff-2026-10-03-wave8-coordinator.md)
as the resume map. That handoff still governs:

- the **roles**: Claude Opus builds at medium effort, Codex Luna (`gpt-6-luna`)
  reviews at high effort through the CLI, and an independent Opus agent
  adjudicates, arbitrates and judges;
- the **tools** in `C:/Projects/ai-template.wt/coordinator-tools/` (README there):
  `compose.py`, `toml_merge3.py`, `mkprompt.py`, `review-prompt.template.md` and
  `luna_review.sh`;
- the **recipe corrections**.

Read it after this one. This session's record is the tail of
[log.d/2026-10-03-wave8-coordinator.md](log.d/2026-10-03-wave8-coordinator.md) and
[reviews/2026-10-03-wave8/](reviews/2026-10-03-wave8/).

## State at handoff (trunk `refactor_again`, clean, nothing pushed)

Landed this session, each with the full commit bar: smoke at or under 60 s
enforced, `check_trajectory --strict`, `check_docs`, and `trace.py --strict`
showing only LLR-292's pre-existing finding.

- **WI-697:** TC-279's first judgement was recorded as a **pass** on a seeded
  five-part sample. A fresh Opus judge ruled; Luna found it SOUND.
- **Batch P (act seq 23, retaken):** Luna found SR-215's re-attested rationale
  misleading, and an independent arbiter ruled B
  ([ARBITRATION.md](reviews/2026-10-03-wave8/ARBITRATION.md)).
- **WI-778**, then **batch Q (act seq 24):** SR-215 re-attested.
- **WI-771:** the assumption evidence ladder is dropped. SR-200, LLR-237 and
  TC-232 are retired; 12 rows were amended; a test case now *falsifies* an
  assumption and never *evidences* one.
- **WI-781:** TC-309 and TC-310's test assertions.
- Approval acts run to **seq 24**. The consolidation census dry run finds no
  overlapping queued rows. Disk: about 31 GB free after the owner cleared space.

## Resume here, in order

1. **One combined sitting over WI-782 and WI-783.**
   - **WI-782:** the amendment of WI-771's 20 rows.
   - **WI-783:** the first approval of TC-309, plus TC-310, which the coordinator
     carried in; its Context explains why.
   - Use ONE act: `--approves "docs/test/test-cases.toml=WI-783" --reattests <the
     WI-782 rows ruled blessable>`. The test-case registry's first-approval copy
     is refused while WI-782's drifted TC rows are unattested.
   - Compose both briefs with `compose.py`, use a fresh Opus adjudicator in its
     own lane, then a Luna cross-review.
2. **WI-777: TC-055 re-judge.** It is ready now; WI-771 changed the rendered
   assumption view it judges.
   - Render with `scripts/dashboard-shots/shoot.mjs`, and cut tiles of at most
     1500 px with Playwright clips.
   - Run three judges, one per width. Each judge's family must differ from the
     rendering code's author's family; WI-771's view code was written by Claude
     Opus.
   - The wave-7 handoff has the judging recipe.
3. **WI-688** second to last, held by OI-99. Its sitting is WI-541's occupancy
   run, and WI-541 closes with it. **WI-625** (deferred) goes last.

## Open questions for the owner

- **S11, adjudication in the lane.** This session's return chain (WI-747 →
  766/767 → 770 → 772/773 → 774 → 775/776 → 778 → 779/780 → 781 → 783) is the
  evidence. The coordinator offered to draft a plan in which an independent
  adjudicator judges a lane's spine text before it lands, and returns become fix
  rounds inside the lane.
- **OI-98 / WI-684:** the FileBackup re-sync.
- **Need re-attestations:** SN-003, SN-008, SN-009, SN-025 and SN-043.
- **SR-006:** batch M's recommended amendment.
- **Full suite:** it can now run, with the disk freed; it has not run in three
  waves.

## Follow-ups noted, not filed

- LLR-231 and TC-227's `method` keep the "assumption evidence" group name, which
  is tied to the `assumption_evidence_rows` symbol and a rendered label. Renaming
  it is a contract change.
- `gen_arch_map.declaration_sites` harvests `Implements:` text inside test-fixture
  strings. TC-279's procedure should state its skip-a-non-part rule before a
  draw.
- `_render_drill`'s trace-bar branch has no recorded reason, a small instance of
  DA-011's obstacle.
- TC-279's result section is an input of TC-209, TC-210 and TC-211.
- `trace.py --strict` exits 1 on trunk from LLR-292's "minimal" disclaimer, which
  the lint misreads.

## Corrections learned this session

- **`.claude/agents/kit-builder.md`** (`model: opus`, `effort: medium`) loads at
  session start. A new session can dispatch `subagent_type: "kit-builder"`; this
  one used `general-purpose` with Opus and had the builder read the file.
- **A retake cannot revert an act.** A commit that writes a snapshot copy unequal
  to the live registry is itself a finding. Rebuild the lane from the commit
  before the act, retake it, and add the discarded act as an extra parent in
  `archive/lanes`.
- **Never resolve a registry conflict with `checkout --ours`.** A loop over all
  unmerged paths once took trunk's side of `test-cases.toml`. Resolve generated
  files that way, and registries with `toml_merge3.py`. Then check that both
  sides' cells are present.
- **When git line-merges registries without conflict, cross-check against
  `toml_merge3.py`.** Compare the parsed tables; they matched for WI-771.
- **A return whose follow-up is one assertion** can be fixed by the coordinator on
  the lane, in the open and recorded (WI-781). That beats a further mint-and-sit
  round.
- **Luna:**
  - Cite locations as plain `path:line` (the template says so), because absolute
    worktree links break `check_docs`.
  - A lane's regenerated views are by design (the template says so).
  - `git worktree add` and some Git-for-Windows file mappings fail inside the
    sandbox, so tests that need them fail there. Confirm them outside it.
- **Disk:** the drive filled mid-session from outside these sessions. Free space
  swung between 0 and 600 MB until the owner cleared it.
