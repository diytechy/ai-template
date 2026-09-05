# Adversarial review brief — round 1 (codex, gpt-6-astra, effort high)

You are a hostile reviewer. Your job is to REFUTE, not admire. The document under
review is a redesign plan for this repository's process kit, written by a
Claude agent on 2026-09-05. The repository owner suspects the kit has grown
overly complex and asked for a redesign; the plan's author had every incentive
to make the case for a rebuild look clean. Find where it is wrong, overclaims,
under-evidences, or would make things worse.

## Files under review (read all four, in this order)

- `docs/ai-template-redesign-2026-09-05 - claude/PLAN.md` — the plan (about 690 lines)
- `docs/ai-template-redesign-2026-09-05 - claude/A-spine-census.md` — spine classification
- `docs/ai-template-redesign-2026-09-05 - claude/B-module-map.md` — module map, batch-lane sizing, duplication signals
- `docs/ai-template-redesign-2026-09-05 - claude/C-external-tools.md` — external tool landscape

Repository context you may read: `CLAUDE.md`, root `README.md` (the
`PROJECT-VISION:` tag), `project-trajectory/PROCESS.md`,
`docs/requirements/*.toml`, `docs/test/test-cases.toml`,
`project-trajectory/scripts/**/*.py`, `tests/`, `docs/handoff-2026-09-04.md`,
`docs/handoff-2026-09-03.md`, `docs/concurrency-v2.md`,
`docs/plans/2026-09-02-backlog-restructure-and-consolidation.md`,
`docs/decisions-for-review-2026-09-05.md`. Do NOT read `OWNER_SCRATCHPAD.md`
(owner-only). Do not read the sibling folder
`docs/ai-template-redesign-2026-09-05-codex/` — your review must be
independent of it.

## Budget rule

The owner's remaining usage on your model is low. Spend your own reasoning on
JUDGEMENT. For bulk fact extraction (counting lines, grepping for a symbol,
listing which modules import what, sampling LLR rows), delegate to a cheaper
model where feasible:

    codex exec --ephemeral -s read-only -m gpt-6-luna -c model_reasoning_effort="low" -C <repo> "<narrow question>"

(fall back to `-m gpt-5.6-luna` if that model id is rejected). Or run the
stdlib Python / grep yourself — that is cheaper still. Do not re-derive the
whole census; sample it.

## What to attack, specifically

1. **Measured claims.** The plan rests on numbers: 38,995 SLOC in 82 modules;
   3,255 tests; 27 of 48 merges since 2026-08-15 were process-about-process;
   batch-lane code is about 383 SLOC and caused four of six stranding defects;
   96 of 167 IF rows are intra-kit; 44 LLRs are self-description; the loop's
   import closure is 65% of the kit; the `+++` fence is parsed seven ways;
   `process.toml` four ways. Spot-check at least five of these against the
   repo. Where a number is wrong or its definition is slippery (SLOC with vs
   without docstrings, "process-about-process"), say so with the correct
   figure.
2. **Classification honesty.** Appendix A classes 44 LLRs as
   "self-description / accident" and recommends deleting them. Sample ten of
   the 44 by reading their `detail` cells in
   `docs/requirements/low-level-requirements.toml`. For each, is the class
   defensible, or is the row carrying a behaviour an adopter would miss?
   Do the same for five of the 96 "intra-kit" IF rows.
3. **The target design.** Attack each of these on its merits, with the
   failure scenario it would produce in THIS repo:
   - one WI per lane, batch admission deleted (the plan admits the batch
     bought atomicity of the human re-attest window — is the loss really
     "worth less" than the defects, and does the `exclusive` key plus a class
     barrier actually recover serialisation?);
   - intake judgement at proposal time (`proposed/` directory) replacing the
     post-merge amendment adjudication for non-promise rows and the idle-tick
     consolidation census — what does a proposal-time judge NOT see that the
     post-merge one does?
   - "an LLR amendment does not drop the derived stage below DevStg-Tests" —
     does this contradict SN-029's acceptance text or the D-9 attestation
     model? Read SN-029 in `docs/requirements/stakeholder-needs.toml`.
   - close-before-final-round ordering removing the verdict peel — is that
     actually implementable given how the merge slot verifies the round
     names the tip?
   - ratchets cut to three with automatic re-baselining on untouched
     commits — is auto-re-baseline a laundering path the kit's own doctrine
     forbids?
   - retiring the daily handoff in favour of a derived dashboard panel;
     making `status.md` generated.
4. **Effort and sequencing.** The plan estimates about 27 supervised days
   plus two two-week soaks. Is the Phase 1 spine prune (4 days) credible for
   deleting ~120 LLRs, ~117 IF rows and ~100 TCs and re-snapshotting the
   baseline, given the kit's own amendment/approval machinery? Is the phase
   order right (spine prune BEFORE the loop rebuild)? What is missing from
   every phase's Done-when?
5. **The external-tool claims.** Pick three from appendix C (e.g. Worktrunk's
   `wt merge` behaviour, Beads storing state in Dolt, Bernstein's
   deterministic coordination) and check them against the cited URLs if you
   have network, or flag them as unverifiable if you do not. Note the
   appendix's own caveats before repeating them as findings.
6. **What the plan does not say.** Missing gaps, missing risks, an option the
   plan should have considered and did not (for example: a much smaller
   refactor that gets most of the benefit; or keeping the loop as-is and
   changing only the review threshold; or dropping the loop from the shipped
   kit entirely).

## Output contract

Write your findings as Markdown to the file named by `-o`. Structure:

1. A one-paragraph verdict: is the plan's diagnosis sound, is the target
   shape sound, is the breakdown executable — each answered yes / partly / no.
2. A findings table: `| # | Severity | Where (file:line or §) | Claim under attack | Finding | Evidence |`
   Severity is BLOCKER (the plan would mislead the owner or make the repo
   worse if followed), MAJOR (a material error or omission), or MINOR.
   Every finding cites a file and line or section in the plan AND the
   evidence you checked (repo file:line, a command you ran and its output,
   or a URL). No finding without evidence.
3. For each BLOCKER and MAJOR: two to six sentences of detail and the
   concrete correction you would make to the plan.
4. A short list of things you could not verify and why.
5. Do not restate what the plan gets right beyond one sentence in the
   verdict. Do not soften. If the plan is wrong, say it is wrong.

Cap the whole output at roughly 3,000 words.
