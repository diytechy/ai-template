# 094-DESIGN-CHECK — stale shared-failure tally: the page now fires on every review round, including clean APPROVEs

The autonomous page-the-human path (PROCESS_OPTIONS.md "Unattended operation",
failure semantics): review round 36 (session 093, REVIEW-A of WI-152, built
session 092 by gpt-5.6-sol) came back **APPROVE (1 MINOR) at the strong tier**
with the full G3 harness observed green — and `escalate` still returned
**page-human**, so `docs/gate-policy: autonomous` scheduled this design-check
session (Claude Fable, strong tier, a different family from the implementer)
to rule grind-through vs. redesign. This is that ruling.

## What fired, exactly (traced, not assumed)

- Scoreboard round 36: `verdict=APPROVE tier=strong tripwire=0 contradiction=0`
  ([scoreboard.txt](scoreboard.txt)) — so neither the tripwire page nor the
  twice-contradiction page can have fired. The only remaining page condition is
  `page_top_tier_fails` (default **2**, `agent_route.escalate` — the
  `top_tier_fails` sum at `agent_route.py:584-597`), counted over the
  coordinator run's **entire in-memory round history** (`rounds = []` is
  initialized once per coordinator process, `agent_loop.py:2104`; nothing ever
  removes a counted round).
- The in-run strong-tier CHANGES-REQUESTED rounds are **31** (WI-166) and
  **33** (WI-165) — exactly the two [085-DESIGN-CHECK](085-DESIGN-CHECK.md)
  already traced, ruled **GRIND-THROUGH**, and remediated: the WI-168 rework
  landed and drew a zero-finding APPROVE ([087-REVIEW-A](087-REVIEW-A.md)), and
  the WI-169 rework landed (session 088). Nothing new has failed since; rounds
  34, 35, and 36 are all APPROVEs.
- Consistency check across the run: once the tally reached 2 at round 33, a page
  fired after **every** subsequent round regardless of verdict — round 33 →
  design-check 085, round 34 → 088, round 35 → 091, round 36 → this session —
  and will keep firing for the life of this coordinator process. A clean APPROVE
  cannot coherently be a page cause; the page is firing on stale, already-ruled,
  already-remediated evidence.

## Ruling: **GRIND-THROUGH** (no redesign)

There is no shared failure: the round that triggered this page **approved** the
artifact under review with the whole G3 harness green. Nothing indicts a spec or
a design; redesign re-entering process.md §5 is not indicated. Resume BUILD.

**Standing fast path for successor design-checks (assumption documented, per
the autonomous failure semantics):** the rearm fix (WI-171) only takes effect
when it lands **and the coordinator restarts** (the routing referees are
imported at process start), so until then every review round in this run will
page again on the same stale tally. A successor design-check fired with **no
new strong-tier CHANGES-REQUESTED round after round 33** on the scoreboard may
cite this ruling, verify that precondition, and immediately reset
`docs/run-phase` to BUILD — no fresh trace required. Any new evidence (a new
strong-tier fail, a tripwire, a contradiction pair) voids the fast path and
demands its own ruling.

## The defects the trace exposed (filed, the 085 idiom — remediation ahead of backlog)

1. **WI-171** (`BuildTier=medium`, `unattended`): the shared-failure page never
   **rearms**. `top_tier_fails` sums strong-tier fails over the whole run, so
   after a design-check ruling the same two rounds re-page forever, burning one
   strong-tier session per review round. Fix direction (design settled here, the
   build is mechanical): when the page dispatches (a design-check is scheduled
   or NEEDS-HUMAN is written), the coordinator resets the tally so only **new**
   top-tier fails can re-page — e.g. mark the dispatch index and count fails
   after it. Keep the intended semantics "2 fresh top-tier fails ⇒ the
   shared-failure regime"; the last-round tripwire and two-round contradiction
   pages already have bounded windows and need no change. Note: WI-171's own
   commit touches `agent_route.py`, a listed review path, so its review round
   fires the `implementer-touched-review-path` tripwire once — anticipated, the
   WI-167 precedent, not a defect.
2. **WI-172** (`BuildTier=medium`, `unattended`): collateral already incurred.
   DESIGN-CHECK is a **review-exempt** phase (`REVIEW_EXEMPT_PHASES`,
   `agent_loop.py`), and the two spurious design-check sessions ground through
   by **building the next WI inside the exempt session**: commit `e544ae1`
   (WI-169 — spine-touching: TC-056 / `docs/test/test-cases.csv`) in session
   088 and commit `cef63a1` (WI-170 — `agent_loop.py` + PROCESS_OPTIONS) in
   session 091 have **no REVIEW-A round**, so the declared `review-policy: 1`
   was never satisfied for either. WI-172 is the retrospective independent
   fresh-context review of both commits, verdicts recorded in `docs/reviews/`,
   findings filed as WIs. Discipline note for the record: a design-check session
   **rules and files**; it must not fold build work into a review-exempt phase —
   with WI-171 in place those sessions would have been ordinary reviewed BUILDs.
3. **WI-173** (`BuildTier=quick`, `scripts`): [093-REVIEW-A](093-REVIEW-A.md)'s
   MINOR has no mechanized carrier — the `docs/rework-wi` pointer is
   CHANGES-REQUESTED-only by design, so APPROVE-round findings are the driver's
   to file (the WI-139/WI-140 idiom). The scaffolded knowledge index's example
   row labels the pack with a code-span, so a copied row leaves the pack an
   orphan; render the example Label as a markdown link
   (`` [`example`](example.md) ``) so the index actually delivers spec §3a's
   "indexes them, so packs aren't orphans".

Order: **WI-171 → WI-172;WI-173 → WI-153** — stop the per-round page bleed
first, then the incurred-review debt and the one-line template fix as one
dev-slice batch (WI-133: both off-spine, independent, no intra-batch edge;
strongest-member pin = medium), then the owner-greenlit research-knowledge
campaign resumes at WI-153 exactly as queued.

RULING: GRIND-THROUGH — resume BUILD on WI-171 (then WI-172;WI-173 → WI-153);
redesign not indicated.
