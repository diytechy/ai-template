# Arbitration — the fourth build wave (2026-09-27)

The wave that opens with the owner's direction to consolidate the queue
([the handoff](../../handoff-2026-09-27-coordinator.md)). Builders work in
their own worktrees; codex Sol reviews each commit read-only (the `sol-*.md`
files beside this one). The coordinator rules where a builder and Sol
disagree, where it disagrees with Sol, and where a queued item asks for a
ruling that is not the owner's, citing the governing text. Rulings a Fable
arbiter makes are marked as such.

1. **WI-670's precondition: what a design row's `module` cell lists.**
   WI-670 (now absorbed into WI-656) asks for a ruling before its count is
   built: does `module` list the modules holding the row's `code_symbol`
   entries, or every module the change touched? The governing text is WI-670's
   own Context, which states what the cell is for: it "is where a reader goes
   to find the row's code". A module the change touched but that holds none of
   the row's code sends that reader to the wrong file, and LLR-180's union
   reading lets it pass silently. **Ruling: the former.** A design row's
   `module` cell lists the modules holding its `code_symbol` entries. The union
   reading stays for LLR-180's anchor verdict; the new per-module "unbound
   module" count is untraced-class, listed by `--show-untraced`, never the
   exit code, and a generic token (`main`, and any name every CLI module
   defines) does not bind for it. LLR-180's amendment is judged in the
   spine-acts batch. The owner may overturn this; it is a convention reading,
   not a rung decision, which is why the coordinator rules it rather than
   minting an open item.

2. **WI-638's carried-over blocker: declare, don't amend, where the rows
   already say so.** Wave-3 ruling 22 left two routes for the five
   observation cases a re-judge cannot finish (TC-036, TC-055, TC-209,
   TC-210, TC-211): amend SR-215, LLR-254 and TC-247 so an undeclared case
   is not due, or declare `inputs` and `max_age` on the five. The governing
   text is OI-90's ruling (a): the ten declaration advisories on exactly
   these five cases "are real work, not noise". **Ruling: declare.** The
   builder declares `inputs` and `max_age` on the five cases, and SR-215,
   LLR-254 and TC-247 stay as approved; wave-3 ruling 19's "not due"
   remedy stays withdrawn. If a declared cell is an attesting cell of an
   approved row, it is amended in place, status left `Approved`, and joins
   the spine-acts batch. For the always-on declaration failure that exceeds
   LLR-233 and TC-228: an input path that escapes the committed snapshot is
   a real defect, so the failure stays and LLR-233 and TC-228 are amended
   in place to name it, judged in the batch. The escape test resolves
   symlinks against the snapshot and does not reject a non-escaping
   `docs/../src`; the checkpoint revision is extracted once.

3. **WI-675 / WI-676 / WI-604 (spine-acts batch A) — no dispute.** Sol:
   9c116ee1 SOUND, no findings (`sol-wi675.md`). WI-604's RETURN is folded
   into WI-582, the open spine-authoring group, not filed as a new row.

4. **WI-582, first round — SOL.** IF-176 gained a covering test case but no
   owner-side `Contract IF-176:` body in `trace.py`; the builder adds it in
   the follow-up commit that also carries WI-604's disposition.

5. **WI-672, first round — SOL on all three.**
   - *The blocker.* The builder shipped `trace.py --tests-for` (IF-233)
     with no design row, because it held no LLR or TC ids. Its reason is
     honest, but a shipped CLI arm no row claims is exactly the untraced
     code the kit exists to prevent (the builder brief's seam convention).
     The coordinator grants LLR-260 and TC-255, authored Drafted, for the
     next spine-acts batch.
   - *The Full advisory.* It follows the spec's wording: every approved
     Full case with no slow evidence is advised.
   - *TC-153.* It is split, not re-tiered. Its four in-memory clauses move
     to a fast module and the case stays Smoke; a wholesale amendment to
     Full is the remedy only where no honest split exists.

6. **WI-656, first round — SOL on all three; the builder's WI-658 choice
   stands.** The builder shipped a template `[generated]` list held equal to
   the regeneration's writes, not readers derived from it, because approved
   LLR-140 defines audit's allowed set as "the stack.ini [generated] set".
   That is the honest option under an approved row. Sol's findings: the
   resync pack omits `kitlib/registry.py`, which `check_trajectory.py` now
   calls; the reader test drives neither real reader; the unbound count is
   a substring match. All three are fixed in one follow-up commit.

7. **WI-638 (af6e9278) — BUILDER on the blocker, SOL on the three majors.**
   - *The Boundary arm's population.* Sol reads OI-88's "each
     boundary-referencing requirement" as widening SR-212 to every form. The
     governing text is approved SR-212's own acceptance: "requirements of the
     other two forms are out of scope". The owner's question (OI-88, spine map
     D8) was at which rung SR-212's gate runs, and its ruling added a rung.
     It did not widen SR-212's population. The phrase Sol quotes is the
     driver's gloss in the ruling's one-line summary, written by this
     coordinator, and it is imprecise. An assumption-form requirement is
     itself the premise, so demanding that it be bridged by an assumption
     would be circular. **Ruling: interface-form only, at both arms.** The
     one-line summary is corrected to say so.
   - *The Release arm's no-frame vacuity.* SOL. SR-206 has no frame
     exemption. The tier's adoption rule (OI-94) keys on a real assumption
     being declared, and a relied-on assumption is one. The early return
     goes.
   - *Internal committed symlinks.* SOL, proportionately. Wave-4 ruling 2
     said the escape test resolves symlinks against the snapshot, so a
     committed link whose target is inside the repository is resolved within
     the revision, and its target's bytes are what gets digested.
   - *SR-198.* SOL. The coordinator grants amendment authority over SR-198
     so it names the repository-escaping input path; it joins the batch with
     LLR-233 and TC-228.

8. **WI-582, second round (1803458b) — SOL on all three.** The IF-176 fix
   is confirmed. The WI-604 disposition's rows go to a first approval next,
   so they must be complete: LLR-210's seven symbols get their
   `Implements:` back-links, TC-208 (or TC-254) cites IF-177 and IF-178,
   whose allowlist entries named this successor, and the scope-unchanged
   assertions compare whole specs rather than one sentinel. SR-220 is judged
   honest as a labelled derived requirement under SN-025 (hat_refs lenses
   and the rationale's argument, the SR-175 / OI-89 precedent); the owner
   may prefer to widen SN-025's acceptance, which the rationale feeds back.

9. **WI-672, second round (7191fd08, ecbe72eb) — SOL on all three.** The
   first round's findings are fixed. The new design row, though, parents
   two behaviours under SR-157, which obliges REPORTING rule violations.
   The tier rule is such a report; the module-to-test listing is not. It is
   split: the listing gets its own design row and test case under an SR
   that honestly obliges a query of the joined spine, or a labelled derived
   SR if none does (the S5 ruling is its origin). Also fixed: the evidence
   parser splitting a spaced parametrized id, and `--tests-for` ignoring
   `--docs`. TC-068's `expected` is amended to drop the retired
   "unjustified seam" arm, under a coordinator grant.

10. **WI-582, third round (ffb2c143) — SOL on the vacuous seam citations,
    COORDINATOR on CRLF.** The back-links and the byte-for-byte tests are
    fixed. TC-208 cites IF-177 and IF-178, but its evidence would stay green
    with either seam removed, so each gets a test only that seam can pass.
    Sol also finds that the byte-for-byte invariant fails for a CRLF spec.
    The governing text is IF-159, the spec registry's write contract: UTF-8
    with LF endings on every platform. A CRLF spec is outside the format, so
    the test cases state the invariant for the registry's LF format and the
    code is left alone.
