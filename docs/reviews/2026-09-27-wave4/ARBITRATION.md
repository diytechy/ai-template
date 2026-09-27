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
