## 2026-08-18 — shipped-docs prose pass (six owner-authorized audit fixes)

Doc-only. No script, registry or test behaviour changed; the corrections all run
the other way — prose that had drifted off what the code already does.

1. **PROCESS.md navigation.** 27 bolded sub-topic lead-ins in §3 and §4 became
   `###` headings. No renumbering, no rewording (two colon lead-ins —
   *Constants*, *Verification methods* — lost their colon and gained a capital).
   Byte-neutral by construction: `**Title.** ` and `### Title` + a blank line are
   the same width. §-numbering untouched.
2. **Retired `G*` vocabulary archived.** The §4 block moved to
   [`docs/archive/retired-vocabulary.md`](../archive/retired-vocabulary.md);
   PROCESS.md keeps a one-line pointer. The read-side aliases are `check.py`'s
   and `check_vocab.py`'s behaviour, so the core was carrying a retirement's
   paperwork rather than a rule. `check_vocab.py` still passes (13 pre-existing
   warn-only findings, all in the generated `docs/test/report.html`).
3. **Section-as-state retired in prose.** The registries carry `status` as ONE
   field at every tier (`trace.STATUS_VALUES`;
   `stakeholder-needs.template.toml` "MATURITY IS A FIELD, NOT A SECTION"), so
   PROCESS.md §4, ADOPTING.md and PROCESS_OPTIONS.md's "Artifact states" bullet
   stopped naming "an SN out of its draft section" as a live ratification path,
   and `docs/registry-machinery-reference.md` §2 was rewritten against the TOML
   registry. Two findings surfaced while verifying §2 against the code:
   - `trace.ENUM_FIELDS["SN"]["Status"]` declares the closed vocabulary but the
     integrity sweep folds `enum_integrity_findings` over
     `raw = {"SR", "LLR", "TC"}` only — SN is not in that dict, so
     `status = "Bananas"` on a need produces **no finding at any bar** and reads
     as ratified. Verified on a planted single-need registry. Recorded in §2.3
     and §12.5 as a live hole, not fixed here (out of a prose lane's scope).
   - `spine_carrier.is_draft_need` matches `"Drafted"` **exactly and
     case-sensitively**, unlike the case-insensitive SR/LLR/TC `Status` reads.
     Recorded in §2.1.
4. **`partial/` documented.** `agent_common.SPEC_STATUS_DIRS` declares seven
   status folders and `check_trajectory.TERMINAL_STATUSES` declares THREE
   terminals; PROCESS_OPTIONS.md declared six and two. `partial` (SR-144 — could
   not finish, scope ends here, remainder carried by a successor WI) joined the
   folder list, the `Status ∈ {…}` enum, the lifecycle bullet, R-A (with its
   exemption from the non-empty-`Deliverable` half — the record is the
   `docs/handbacks/` report) and R-F (a `partial` row's `SpecRef` **stays** and
   counts as a live citation).
5. **One reporting rule, one wording.** *Paste the real output; never report a
   green you didn't produce.* Aligned at `KICKOFF_PROMPT.md`, both places in
   `gate-advance/SKILL.md`, and `session-protocol/SKILL.md`; all three
   materialized copies of each skill re-synced byte-identical. Placements kept —
   repetition at boundaries is fine, divergent wording is the hazard.
6. **Archive boundary, stated once each side.** `docs/archive/README.md` gained
   the rule (records a historical decision, no longer read by a script) and the
   counter-rule (a generated or script-read surface is machinery, not history —
   `docs/ratify/`, `docs/iteration/`, `archive/last_approved/`); PROCESS.md §5's
   now/history split gained one sentence naming the third tier and pointing at
   that README.

**Byte deltas.** `AGENTS.template.md` 9,994 → 9,994 (untouched; 6 bytes of
headroom under 10,000). `PROCESS.md` **81,763 → 81,499 (-264)** — the headings
are neutral, the archived block is the whole delta; net negative, so nothing is
owed beyond the re-stamp. `PROCESS_OPTIONS.md` **172,047 → 173,375 (+1,328)** —
the SN field rewrite plus `partial/` across five passages; load-bearing on the
kit's own single-source rule, since a layer doc that omits a declared value
teaches a schema the checker refuses. Both baselines re-stamped in all three
`byte-budget-guard/SKILL.md` copies in this change.
