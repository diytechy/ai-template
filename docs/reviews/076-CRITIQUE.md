# 076 — CRITIQUE (post-WI-159 render; the Knowledge-tab fix confirmed, remaining nits tracked)

**Scope:** SR-052/053/054 (T1–T7), the dashboard render **after WI-159** (commit
`729e867`). Judged against `docs/rubrics/dashboard-{usability,accessibility,uniformity}.md`.
**Artifact:** the `scripts/dashboard-shots/shoot.mjs` PNG matrix re-shot on the
WI-159 build (the collapsed Knowledge render), read by the builder, the independent
reviewer, and this critic.
**Critic:** Claude (agent), via the `render-dashboard-critique` loop. Honest
caveat: an agent critique is weaker than an independent family-heterogeneous critic
or the owner's own eye (SR-047) — the strongest attestation is a human pass, which
the owner can do anytime. This verdict re-dates the perceptual evidence past the
WI-159 render change (clearing the WI-243 staleness warn).

VERDICT: CHANGES-REQUESTED findings=3

## Resolved since 075

- **[T2 default-density] Knowledge (OKF) tab — FIXED.** The tab now opens
  **start-collapsed**: 6 OKF type-blocks (IF · SN→SR→LLR→TC · PG) instead of the
  ~200-node exploded hairball; double-click descends to the per-type concepts.
  The load-bearing 075 finding 1 is resolved (WI-159). *Shots:*
  `1280px-{light,dark}-know-full.png`.
- **[T4 label legibility — clipping] Knowledge TC labels — FIXED.** The collapsed
  root layer (600px) sits inside its container; no node label clips in either
  theme. 075 finding 2 resolved.

## Remaining (minor; tracked as WIs, per the OI-8 "amendments arrive as future WIs" posture)

1. **[T4, MINOR] How (SW) component-block labels truncate** with an ellipsis
   ("CMP-003 — Quality ch…"). → **WI-246** (queued).
2. **[T5 / uniformity, MINOR] When (roadmap DAG) phase-accent palette low hue
   separation** — adjacent phases near-identical maroon. → **WI-247** (queued).
3. **[T7, MINOR] What (SR breakdown) icicle overflows at 390px** — LLR/TC need
   horizontal scroll. → **WI-248** (queued).

## Disposition

The **load-bearing** perceptual defect — the owner's "hard to read" Knowledge tab
— is fixed and triple-verified. The three remaining findings are minor polish,
each filed as a queued WI (not gate blockers, the standing OI-8 posture). The
`CHANGES-REQUESTED` verdict honestly reflects that three open render items remain;
it is warn-tier only (the WI-243 re-fire never joins the exit code). A human/
heterogeneous re-pass would be the stronger attestation once WI-246/247/248 land.
