# WI-550 — REVIEW-A of the disposition close (adjudication of the WI-540 partial close)

Reviewed diff: `git diff contract_split...HEAD` (docs-only): the WI-550 spec moved
`active/ -> archive/work/complete/`, `## Deliverable` + `## Dispositions` added,
`specref` cleared.

## What I verified (drove the real paths, quoted real output)

- **Close mechanics (adjudicate-disposition.template.md §50).** `## Deliverable`
  filled with the `OUTCOME:` line + verdict path, placed BEFORE `## Context`;
  `specref = ""` cleared; spec moved to `docs/archive/work/complete/`; both the
  verdict commit (`547c3505`) and the close commit (`9aa2158b`) carry the
  `WI: WI-550` trailer. All present.
- **Successor draft mints cleanly.** Drove `intake.parse_dispositions` on the
  shipped spec → `refusal=None`, 1 draft, `kind=ordinary`, `supersedes="WI-540"`.
  Title 109 chars (≤120). `safety_class="ordinary"` ∈ `schedule.SAFETY_CLASSES`;
  all keys ∈ `_DRAFT_KEYS`; no `[table]` header. `_terminal_hits` unions
  `WORK`+`ARCHIVE_WORK`, so the archived spec is scanned — the successor will be
  found and minted at merge.
- **Factual basis of the ruling holds.** `git diff 9abdb5d982 contract_split --
  project-trajectory/scripts tests` is EMPTY (trunk byte-identical to the WI-540
  base); `adjudicator_session.py` + its test absent from trunk; IF-174 reverted
  out of `interfaces.toml` while its mark stays burned. The DISCARD-all ruling
  and "no red on trunk" claim are true. Referenced `wi-540-...patch` and
  `WI-541` queued spec both exist.
- **Harness.** `check.py --jobs 0` → `RESULT: PASS`. `trace.py --strict-integrity`
  → `integrity=0`. The LLR-197 provenance FINDING and `orphans=2` are pre-existing
  trunk-side rows this docs-only diff does not touch.

Four disposition answers all covered: outcome PARTIAL upheld against commit facts;
keep/discard split ruled (DISCARD product commits — already reverted, verified;
KEEP report/patch/mark bookkeeping); one successor drafted; cost strong, no dual.

## Findings

- [MINOR] docs/archive/work/complete/WI-550-dispose-the-close-recorded-at.md:52 -> the successor's rationale prose (WI-541 blocks, re-land-don't-rebuild, resolve DESIGN-CHECK first, strong-tier justification) is placed BEFORE the ```toml block, so `parse_dispositions` captures `scope=''` and the minted successor's `## Context` will hold only the "Drafted by WI-550 … drafts-not-mints" boilerplate — the two hard boundaries the adjudication stressed do not ride into the minted row (prior dispositions WI-542/WI-544 put substantive scope prose AFTER the block, which intake carries verbatim into Context); the successor still mints and its `specref` defaults back to this archived spec, so the loss is recoverable, not silent -> move the scope/boundary prose to AFTER the ```toml block (a short "Scope of the successor: re-land the preserved patch inert at dial 0, do not rebuild; first reproduce and resolve the DESIGN-CHECK error/timeout, then get the §A2 refresh bar green" paragraph) so it rides into the minted successor's Context -> @owner

VERDICT: APPROVE findings=1
