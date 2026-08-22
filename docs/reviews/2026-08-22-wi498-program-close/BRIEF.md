# Adversarial review brief — the WI-498 stage-unification program close

You are an ADVERSARIAL reviewer of the stage unification program in
c:\Projects\ai-template (a meta-repo whose product is the process kit under
project-trajectory/). Your job is to find what is WRONG, OVERCLAIMED, or
SILENTLY BROKEN — not to summarize. Every finding needs file:line evidence
and a concrete failure scenario; rank CRITICAL/MAJOR/MINOR. The repo's
dominant historical defect class is FLUENT FALSE SIGNED CLAIMS and GUARDS
THAT CANNOT FAIL — hunt those first.

THE RANGE: git commits f23e6002..d3f119ea on this branch (~20 commits):
the ruled plan going FINAL (docs/plans/2026-08-21-stage-unification-plan.md
+ its §6 owner answers); six slices — kitlib/ladder.py (one enum home),
kitlib/stage.py + derive_stage.py + docs/stage (fingerprint + self-healing
common reader), selection re-keyed at-or-above with the bar axis deleted
from check.py, the ladder re-discriminated (all-Founded → DevStg-Impl,
Release evidence-gated with no producer), the detectors re-keyed to stage
history (tier signal fixed — WI-497 folded), and the vocabulary/migration
sweep (docs/gate DELETED, derive_gate DELETED, WI-493 dial re-key folded)
— the LAST slice recovered from an interrupted session (121-file residue
reconciled: 3 hunks reverted, 9 defects fixed; commits c170da9f/73663c3d);
then the owner sessions: process.toml dropped from DECLARED_INPUTS, PB-002
re-measured, WI-473 closed complete-with-supersession, the approval dial
dropped to DevStg-Needs with its staleness sweep, OI-53/54 ruled, the
SPINE APPROVAL ACT (ac121647 — 15 Drafted rows flipped, 4 amendments
blessed, baseline re-seeded), and five owner briefs minted. The per-slice
record is docs/log.d/2026-08-21-wi498-stage-unification.md; the owner
sessions are docs/log.d/2026-08-21-owner-session-dial-and-folds.md and
docs/log.d/2026-08-22-*.md.

PRIORITY TARGETS (where wrongness costs most):
1. THE READER CONTRACT — "no consumer can read a stale stage, on any
   lane." Attack it: does every consumer actually go through the common
   reader (grep by VALUE for docs/stage readers and DevStg- comparisons —
   the program's own censuses were blind by NAME three times); does the
   fingerprint fast-path genuinely detect every input edit (the declared
   input list vs what spine_stage actually reads — process.toml was
   REMOVED from the list: is anything else read but undeclared, the
   inverse defect?); can a reader write, or a stale committed docs/stage
   survive a commit (the --check wiring at the hook + gates + CI)?
2. THE DISCRIMINATOR AND THE PHASE RULE — is DevStg-Release truly
   unreachable (both pins: exhaustive + structural — can a refactor evade
   the source-text pin?); does a fully-Founded spine read Impl on a REAL
   scaffold; the phase rule's four driven directions and the exact
   LLReqs→Arch-pair exemption (owner §6.2: the PAIR, not the rung) — can
   a multi-rung drop ending at Arch slip through any path the tests
   don't drive? The rule ships warn-first and DELIBERATELY UNWIRED
   (--phase-rule) — is that honestly recorded everywhere it is described?
3. THE SELECTION RE-KEY — sample at least six rows of the 25-row
   re-derivation table (slice 2's fragment section) and verify each
   threshold against the artifact-existence rule it claims; the
   registry-integrity widening; --stage/--gate/--stage-cleared flag
   behavior incl. the warn path; the C-01-at-selection acceptance (drive
   it if cheap: mature scaffold + one draft → plan unchanged).
4. THE DELETION'S COMPLETENESS AND THE SWEEP'S RESTRAINT — bar-axis
   remnants on LIVE surfaces (by value, not constant name); docs/gate
   references outside docstrings/records; conversely, RECORDS that the
   sweep should NOT have touched but did (the recovery reverted three
   such hunks — find any fourth: fig: markers, ruled OI text, closed
   specs, log.d history with rewritten vocabulary); the check_vocab
   alias tables' by-MEANING correctness ([g1]→LLReqs, [g2]→Impl — the
   shared-spelling inversion) and the crash class the recovery fixed.
5. THE SPINE APPROVAL ACT — were the 15 flips status-cells-only (diff
   ac121647); were the 4 blessed amendments genuinely the mechanical
   re-point class; is the re-seeded baseline byte-consistent with live
   (drive the drift check); did the act bypass any authority gate
   (intake snapshot's --approves path)? The dial at DevStg-Needs makes
   this agent-performable — but the RECORD must show the owner's written
   approval as its warrant; does it?
6. CROSS-CUTTING — new tests that cannot fail (mutation-test the
   cheapest suspicious ones: the structural no-return-STAGE_RELEASE pin,
   the process-toml-not-an-input pin, the dial rung-string pin's
   structural arm); ratchet/baseline re-stamps with reasons (module
   size, smoke membership, byte baselines — the CLAUDE.md 7,238 and
   guard-skill 4,925 stamps); every full-suite figure in the fragments
   (do the commits' claimed totals reproduce at their revisions?); the
   smoke tier's over-budget readings reported-not-absorbed everywhere.
Also read docs/log.d/2026-08-21-wi498-stage-unification.md's "Adjacent
findings" section and the slice sections' banked items — CONFIRM or
REFUTE each.

DELIBERATELY OUT OF SCOPE: the queued execution rows (WI-494/495/496/499/
500/501/502 — not yet run); the five new owner briefs OI-55..59 (owner's
to rule; flag only if a brief misstates the code); the four Drafted CMP
rows (flagged to the owner already); records/archives' historical
vocabulary (deliberately untouched); OWNER_SCRATCHPAD.md (never read it).

FORMAT: numbered findings, each with severity, file:line evidence, the
failure scenario, and a one-line suggested fix. End with: the three claims
you tried hardest to refute and could not.
