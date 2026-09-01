## 2026-09-01 — WI-563: spot-check the clean close of WI-552 (sample attestation)

Session claimed `WI-563` on branch `wi-563-spot-check-the-clean-close-of`.
SpecRef `docs/archive/work/complete/WI-552-adjudicator-two-exit-close.md`. This
is a `complete_review = 'sample'` spot-check (`docs/process.toml [attestation]`):
the WI-552 close was GREEN and nothing is alleged; the one question is whether
what shipped answers what the row asked for. A finding is a successor row, never
a reversal — the close stands.

### Method

Read the WI-552 spec (seven Done-when arms, OI-70 as refined by OI-73), its log
fragment, and the REVIEW-A rollup (4 rounds, governing APPROVE findings=2).
Verified each Done-when arm against the merged tree at HEAD, not against the
claim prose.

### Each arm located in the merged tree and matched the ask

- **Arm 1 (mechanical adjudication close)** — `handback.close_adjudication`
  (handback.py:464) wired via `dispatch._close_done_adjudication`
  (dispatch.py:624). Present.
- **Arm 2 (OI-mint, exit B)** — `intake._mint_open_item` (intake.py:317) +
  `intake._inject_open_item` (intake.py:1476). Present.
- **Arm 3 (refusal invariant)** — enforced at both `close_adjudication` and
  `intake._disposition_drafts`, and (per REVIEW-A round 1→2) extended to the
  cancelled-brief-less arm. Present.
- **Arm 4 (inbound-edge replacement)** — `intake._replace_inbound_edges`
  (intake.py:1347). Present — see the one residual below.
- **Arm 5 (typed OI edges)** — `kitlib.spine.split_pred_edges`
  (spine.py:190); scheduler `waiting:open-item-pending`; validator
  `check_trajectory.validate(..., known_ois)` + `load_known_ois`. Present.
- **Arm 6 (validator net → partial)** — `dead_dependency_findings` fires on
  `partial` predecessors (`TERMINAL_STATUSES` includes `partial`,
  check_trajectory.py:344). Present.
- **Arm 7 (contract text)** — brief + PROCESS_OPTIONS prose widened; verified
  in the WI-552 diff (arm-7 commit 442715cd).

### Verdict: the close STANDS — it answers what the row asked. No successor minted.

All seven Done-when arms are present in the merged tree with covering tests; the
merge slot ran the full bar green and REVIEW-A APPROVEd after driving each arm.
This is a read-only attestation — no product code changed.

### One residual surfaced (already on the REVIEW-A record, latent — not a reversal)

`intake._SPEC_NEEDS_RE` (intake.py:1344) is
`re.compile(r"(?m)^needs\s*=\s*\[.*?\]\s*$")` — multiline-anchored but WITHOUT
`re.DOTALL`, so `.*?` cannot cross a newline. A dependent whose `needs` is
written as a MULTI-LINE TOML list therefore fails `_SPEC_NEEDS_RE.subn`, `n==0`,
and `_replace_inbound_edges` silently skips it (no `changed` entry, no error).
Arm 4's stated guarantee — the WI-541 strand class "becomes unrepresentable,
not merely visible" — thus holds only under the invariant that every dependent's
`needs` is single-line.

Assessment: **latent, does not bite today.** `wi_convert.toml_value` emits
single-line `needs`, and a tree-wide scan (`docs/work`, `docs/archive/work`)
finds NO multi-line `needs` list, so no live row can currently escape the
re-point. It was already caught as REVIEW-A round-2 MINOR
(`intake.py:1364 … _SPEC_NEEDS_RE is single-line … the rewrite can miss a
multi-line edge`) and shipped routed `@owner`. Recording it here as the
spot-check's independent confirmation; it does not warrant a spine mint from
this branch — the guarantee is correct for every row the machine writers
produce, and a hand-authored multi-line `needs` is the only exposure.

The two other round-4 APPROVE MINORs are cosmetic and confirmed present:
`intake._OI_ID_RE` (intake.py:304) is defined and unreferenced (dead), and
`check_trajectory.validate`'s docstring (check_trajectory.py:804) still says a
non-adopter's `known_ois=None` edge is left to the scheduler while line 812
coerces `None → frozenset()` so every OI edge errors. Both are on the REVIEW-A
record; neither narrows a shipped guarantee.

### Bar

Read-only docs-only close (log fragment + spec Deliverable + spec move). No
spine rows minted or re-statused (adjudication row, no SR-Refs) — no
approval-brief regeneration owed. The environment here has no pytest toolchain;
the spot-check is a read-level attestation over the merged tree, and the merge
slot already ran the declared bar green (the WI's own premise).

### Outcome

Close STANDS; all seven arms verified; one latent residual surfaced (already on
record). Closing COMPLETE, no successor.
