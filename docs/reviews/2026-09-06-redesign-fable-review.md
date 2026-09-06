# Redesign implementation review — Fable 5.1, 2026-09-06

**Scope:** commits `22b21b06` (P0b runtime repairs), `77612fb2` (continuation)
and `875a64b7` (source stamp) on `contract_split`, reviewed at tip `875a64b7`
after the Opus rounds recorded beside this file. Three independent reviewers
(runtime, continuation code, spine/docs) plus the supervising session's own
verification. Ranked most severe first; dispositions are recorded in the
companion [dispositions file](2026-09-06-redesign-fable-dispositions.md).

## Verification the reviewer produced

- Smoke tier at `875a64b7`: `1670 passed, 4 skipped`; enforced wall `52.2s vs
  60s budget -> within` on a quiet box. A run taken while three reviewers
  loaded the box read `79.2s -> OVER`; that reading is retained as the same
  contention shape the execution record already reports, not as a breach.
- `trace.py --strict --no-placeholders` and `--strict-schema`: `orphans=0
  integrity=0 schema-findings=0`; one advisory new to `77612fb2` (SR-184
  Critique wording under Inspection).
- `derive_stage.py --check`: `docs/stage up to date (DevStg-Tests)`, 17 drafts.
- Byte caps and skill mirrors: match the execution record.
- The record's cited `out/run-logs` files exist and match its figures.

## Findings

### 22b21b06 — runtime

1. **HIGH — durable base pollutes evidence after a trunk merge into a lane.**
   `default_base` preferred the claim commit unconditionally while
   `train_evidence` and every other `base..HEAD` reader walk the range without
   `--first-parent`. Reproduced with real Git: after `git merge main` into a
   lane, a trunk commit's `WI:` trailer reads as the lane's own; the
   stale-assignment preflight returned False where the pre-repair rule returned
   True. The regression test merged a trailer-free trunk commit, which is why
   it stayed green. The single-checkout case the repair targeted is real
   (`trunk_name` reads the primary checkout's branch, so merge-base collapses
   to HEAD once the primary sits on the lane); the fix is to use the claim only
   there.
2. **MEDIUM — `scripts_fingerprint` crashes at import.** No regular-file guard
   on `rglob("*.py")`; a dangling editor lock file (`.#a.py`) raised
   `FileNotFoundError` at import of twelve kit entry points (reproduced). The
   dispatcher re-scans every 0.5 s, so the same class ended a run mid-save.
3. **MEDIUM (design) — every integration ends the dispatcher in this repo.**
   40 of the last 40 trunk merges touch the hashed directory. Correctness and
   the one-lane-at-a-time integration invariant are unaffected; the run simply
   stopped being unattended. Ruled in
   [CONTROL-DECISION.md](../ai-template-redesign-2026-09-05-codex/CONTROL-DECISION.md#owner-ruling-2026-09-06).
4. **MEDIUM — Ctrl-C in an attached sitting** persisted a `call_` log with blank
   `wall-secs`, `ended-at` and `usage-status`, and committed telemetry on the
   branch the human was sitting on.
5. **LOW/MEDIUM — restart drain swallowed real outcomes.** With the restart
   armed, every child exit returned "preserved", so NEEDS-HUMAN and BLOCKED
   workers got no handback or page, and a green refresh was redone by the
   fresh process.
6. **LOW —** `_is_claim_move` reads `diff-tree --name-status` without `-z`, so
   a quoted non-ASCII spec name degrades silently to the merge-base fallback.
7. **LOW —** one assertion in `test_agent_loop.py` passes with or without the
   `call_` exclusion; the load-bearing check lives in `test_dual_plan_routing`.

Verified as claimed: exit 11 collides with nothing; the hash is content-only
and LF-normalised; the accounting round-trip (escaped CR/LF, full header read,
`?` not `0`, `call_` names outside numbering and draw rotation) holds.

### 77612fb2 — continuation code

8. **MEDIUM — H1 and R-E disagree on canonical-carrier SpecRef fragments.** The
   composer refuses any fragment on the need TOML that is not exactly `SN-n`;
   the validator passes every fragment on a `.toml` target. A validator-clean
   `#need.SN-12` pages the dual-plan round at draw time; a leading `./` resolves
   to nothing silently.
9. **LOW —** P2a drops comments inside a multiline `needs` array; the record's
   "comments outside the value" wording is accurate but unannounced. `_open_specs`
   skips a dependent whose frontmatter does not parse in both the prevalidation
   and apply passes, so "prevalidates every existing dependent edit" over-claims.
10. **LOW —** `test_old_kit_resync.py` skips its kit-only assertions when node
    is absent; the `--force` leg's name claims a preservation the test itself
    supplies by byte-restore.

Verified: P2a span surgery on every adversarial fixture (CRLF, comments with
`]`, trailing comma, `WI-10` vs `WI-100`, refusals); P9R's `sys.modules` probe
loads no renderer; CLI contract unchanged; catalog fresh; template/live hat
structure sync; skill mirrors identical; resync anchors correct.

### 77612fb2 — spine and docs

11. **MAJOR — need-tier re-attestation debt has no mechanized consumer.** SN-007
    and SN-026 changed while Approved; `SNAPSHOT_TIERS` covers SR/LLR/TC only,
    `--approve modified` renders no SN section, and no OI or WI named the debt.
12. **MAJOR — SR-184 contradicted SN-024.** The parent's acceptance requires a
    family-heterogeneous critique session unconditionally; the Drafted child's
    rationale disclaimed it for the attended case.
13. **MEDIUM —** SN-007's amended acceptance states no observable for the full
    suite; "the declared bar" names no home in PROCESS.md.
14. **MINOR —** Inspection carriers keyed to the packet's H2/H3/H5 numbering, with
    state encoded in the evidence anchors.
15. **MINOR —** the design-replacement rule now has four homes (PROCESS §5, the
    spine-authoring skill, both prompt templates), with the fuller statement in
    the skill.
16. **MINOR —** SR-184's acceptance re-declares its own Verification, which is
    what trips the retained advisory. `hats.toml` charters are outside the
    snapshot, so a charter rewording is never seen by any drift arm.

Clean: no WI/OI ids in cells; every new SR carries its refs and phase; TCs are
honest about not having run; SR-162's stale NOT-DISCHARGED clause correctly
dropped; status.md hand-authored prose names no done id; stage derived.
