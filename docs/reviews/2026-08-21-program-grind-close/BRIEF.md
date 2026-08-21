# Adversarial review brief — the 2026-08-20/21 program-grind batch

You are an ADVERSARIAL reviewer of one batch of work in c:\Projects\ai-template
(a meta-repo whose product is the process kit under project-trajectory/).
Your job is to find what is WRONG, OVERCLAIMED, or SILENTLY BROKEN — not to
summarize. Every finding needs file:line evidence and a concrete failure
scenario; rank by severity. The repo's dominant historical defect class is
FLUENT FALSE SIGNED CLAIMS and GUARDS THAT CANNOT FAIL — hunt those first.

THE RANGE: git commits b94bf58c..bd8fce68 on this branch (23 commits, the
PROGRAM frontier ground in series): (1) WI-448 slice 1 — the shipped
`kitlib/` package (config/git/registry, later station), bootstrap importing
it, four MAPPING rows, the bootstrap-imports-only-kitlib rule test, the
package-completeness manifest test, duplication measured 757→477 redundant
lines; (2) WI-455 slice 2 — IF-134/135 minted as the hook crossings' facing,
five untied `external:` rows adjudicated, 22 stale CMP-id notes swept,
migrate_carrier one-shot framing corrected, OI-49/OI-50 queued; (3) WI-469
closed — all 27 SR-owned file-as-endpoint Consumes rows re-authored (10
verified real consumer modules, 16 → `external:downstream adopter`/B-05);
(4) WI-473 slice — the derived product-regression floor (`ex-draft`) beside
the bar selector in check.py, plus the discovery that DevStg-Impl is
unreachable from the derived selector (OI-51); (5) WI-483 slice 1 — the
7-module import SCC cut to 5 via the typed read model kitlib/station.py,
guarded by tests/test_import_layers.py (sees function-body imports),
LLR-182/TC-177 minted; (6) WI-484 slice 1 — the `Hat-Refs` cell on SR/LLR,
resolution rule hard under --strict, effective sets, 17-row backfill,
LLR-183/TC-178, the "labelled derived SR" vocabulary retired; (7) WI-390
slice — IF-136/137 minted, IF-055/080/081 declared, stale process prose
corrected, LLR-056/TC-056 amendment deferred with recommendation; (8)
WI-467 closed — verified the 2026-08-16 blind re-derivation had already run
and been consumed, housekeeping close only; (9) WI-487 closed — the
Implements: back-link campaign, coverage 1/165 → 83/165 (50.3%), the
process.toml dial 0→50, every tag claimed to be code-verified, one
dishonest tag (LLR-005) caught and replaced by LLR-038; (10) WI-488 closed
— seam-TC coverage promoted to ERROR from DevStg-Tests via
if_tc_coverage_findings, migration allowlist docs/if-tc-coverage-allow
re-measured and seeded at 120 (ruling said 115 on the older tree),
allowlist-hygiene reporter; (11) WI-490 closed — OI-45 (b): the
mechanical-ratification docstrings state the ruled shape; (12) WI-491
closed — OI-46 (1a)+(2a): subagent_gate's present-but-unparseable arm
fail-closed (UNPARSEABLE→ask), banner surfaces the fail-open log count;
(13) WI-492 closed — OI-47 (e): trace.py's one-shot recorded-correction
verb (--correct-mark), the real B=8/REL=4 correction applied through it.
The per-WI record is docs/log.d/2026-08-20-program-grind.md.

PRIORITY TARGETS (where wrongness costs most):
1. THE BACKLINK CAMPAIGN (biggest claim surface of the batch): the cardinal
   rule was "a wrong Implements: tag is worse than a missing one" and every
   tag was claimed code-verified. Sample AT LEAST eight tags across
   different modules and try to refute each against the LLR row's
   requirement+detail. Does 83/165 reproduce via
   `python project-trajectory/scripts/gen_arch_map.py --backlink-coverage
   --src project-trajectory/scripts --root .`? Were any tags placed on
   symbols that only PARTIALLY realize the row, without the row or tag
   saying so? Was raising the dial 0→50 in the repo's own process.toml a
   sanctioned act or a check edited to match its own new number?
2. THE NEW GATES — can they actually fail, and do they fail closed?
   - if_tc_coverage_findings: plant (mentally) an uncovered seam not on the
     allowlist at DevStg-Tests — trace the code path to a hard FAIL. Is the
     allowlist's 120 an honest measurement on the seeding tree? Can an
     entry be added silently (what reads/reports allowlist growth)?
   - the product floor: does max(derived-bar, ex-draft) actually change any
     selected step on a real mature scaffold, or only in the fixture? Is
     the DevStg-Impl-unreachable pin test real?
   - test_import_layers.py: would a NEW function-body import inside the
     5-module SCC actually red it, or only topology changes?
   - the recorded-correction verb: can --correct-mark be replayed? Can the
     header line be hand-forged to sanction an arbitrary raise? Does an
     ordinary --bump-ids preserve or clobber the correction record?
   - subagent_gate UNPARSEABLE: does the REAL hook (as wired in a scaffold,
     not the unit test) return ask on a corrupt process.toml? Does genuine
     absence still allow (opt-in posture preserved)?
3. THE REGISTRY EDITS: WI-469's 27 Consumes rows — sample at least five
   low-fan-out rows and verify the named consumer module actually reads
   the file today; sample three B-05 conversions for whether an internal
   consumer ALSO exists that the row now hides. WI-455's IF-134/135 — do
   the rows realize the crossings they claim (B-01, B-04) and was IF-135's
   B-04-only choice recorded honestly? The Hat-Refs backfill (17 Approved
   SR rows edited under a "traced-cell" classification) — is that
   classification defensible against the snapshot/drift machinery, i.e.
   does docs/archive/last_approved comparison stay green for the RIGHT
   reason and would a requirement-text edit still red?
4. THE GRIND CLOSES: pick at least four Deliverable claims at random and
   verify against the tree — do the cited tests exist and assert what the
   claim says? Any "verified/green/measured" without the artifact? The
   duplication figures (757→477) — does the declared fig: command
   reproduce? The WI-467 close leaned entirely on prior artifacts — is the
   ancestry claim true (cda29c42/dea8364e ancestors of HEAD)?
5. CROSS-CUTTING: the batch added ~25 new tests — any that cannot fail?
   Ratchet re-stamps (module-size in BOTH directions, complexity, smoke
   membership 1258→1269→1284, byte-budget SKILL.md tightenings ×5) — any
   bound quietly raised without a recorded reason? The smoke tier measured
   64–116s across workers against the declared 60s budget — is the stamp
   now dishonest? The fragment top-matter deferral union (OI-48, OI-49,
   OI-50, OI-51) — does it match the per-section declarations, and are the
   OLDER fragments' declarations (frontier-grind: OI-45/46) now stale
   against open-items state?
Also read docs/log.d/2026-08-20-program-grind.md's "Adjacent findings"
section — CONFIRM or REFUTE each banked finding while you are in there.

DELIBERATELY OUT OF SCOPE: the recorded program remainders (wi448 items
1–5, wi455 items 1–3, wi483's four owed items, wi484 phases 2–5, wi390's
window question — each is recorded debt, not hidden debt; flag only if the
RECORD is dishonest); the owner-held recommendations (OI-48..51, the
LLR-056/TC-056 and SR-159 amendment recommendations — flag only if a
recommendation misstates the code); docs/log.md history; and
OWNER_SCRATCHPAD.md (never read it).

FORMAT: numbered findings, each with severity (CRITICAL/MAJOR/MINOR),
file:line evidence, the failure scenario, and a one-line suggested fix.
End with: the three claims you tried hardest to refute and could not.
