# Arbitration — the third build wave (2026-09-26/27)

The wave that carries out the owner's 2026-09-26 rulings (OI-82, OI-86 to
OI-94) and the second wave's filed drafts. Builders work in their own
worktrees; codex Sol reviews each commit read-only (the `sol-*.md` files
beside this one, prompts reproducible from
[the wave-2 record](../2026-09-26-assumption-tier-wave2/ARBITRATION.md)'s
form). The coordinator rules where a builder and Sol disagree, or where it
disagrees with Sol, citing the governing text. Rulings a Fable arbiter makes
are marked as such.

1. **WI-653 — no dispute.** Sol: SOUND, no findings.

2. **WI-665 — SOL, both findings.** The Done-when asks only that the seven
   modules collect alone, but the defect is collection-order dependent, so
   nothing in the suite would notice it coming back. The ruling is a subprocess
   regression that collects one affected module alone, in a slow module, and
   shown red. It runs serially, which reproduces the defect as `-n 2` does at
   less cost. The builder brief's own rule is that position 0 matters (`import
   trace` must bind the kit's `trace.py`), so the helper has to guarantee it
   rather than only test membership. Both are fixed in one follow-up commit.

   **Correction, by the builder's evidence.** The coordinator's instruction
   to run the regression serially was wrong. A serial run does not reproduce
   the defect: `pytest_sessionstart` calls `load_script("agent_common")` on
   the controller before collection, and xdist workers skip that hook. The
   builder showed `4 passed` serially and `1 error` at `-n 2` on the unfixed
   conftest, and wrote the test at `-n 1`. Sol's fix round (`sol-wi665-fix.md`)
   confirmed the claim and judged 614b0ac1 SOUND.

3. **WI-654's pre-adoption failure — SOL.** The builder made only the
   neither-cell advisory wait for adoption, and kept a `bridged_by` naming an
   undeclared assumption failing before it. Its reason: a pointer into
   nothing is wrong wherever it is written. The governing text is OI-94's
   ruled option (b), "one adoption rule across the tier", with the
   recommendation "one adoption rule for the whole tier". SR-193 and SR-194
   make their undeclared-citation failure vacuous before adoption, and before
   adoption every named assumption is necessarily undeclared. Keeping the
   failure would therefore keep the rule live, which is not the ruled
   vacuity. Ruling: the whole bridging rule is vacuous until the first real
   assumption row, and the exception comes out of the three amended cells.
   The builder's LLR-224 finding, which Sol confirmed, is folded into the same
   follow-up: its `detail` says "absent" where the shared predicate reads "no
   real row". It is amended in place so WI-664's joint adjudication judges it
   with the rest.
