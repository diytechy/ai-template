# Independent code review dispositions

The [Opus 5/high review](2026-09-06-redesign-independent-code-opus.md) examined
H1, the text-status import boundary and the missing scaffold catalog producer.

| Finding | Disposition and evidence |
|---|---|
| B1: Windows need-carrier alias silently missed | Fixed: serialize the canonical Markdown alias with `as_posix()` and reuse the hats reader's needs-carrier constant. A PureWindowsPath regression exercises the repository's forward-slash reference spelling even on POSIX. |
| B2: valid Markdown fixture could pass if parent ignored | Fixed: test both canonical carrier spellings and require an unknown exact SN reference to refuse. This distinguishes actual resolution from an ignored fragment. |
| B3: existing adopters need explicit catalog regeneration | Clarified the common RESYNC procedure with the exact generator command and fresh-only initialization boundary. A historical entry already named the generator, but relying on that old version range was insufficient for a newly delivered script. Preserve the deliberate fresh-only initializer. A commit-anchored entry follows the source commit. |
| Delivery inventory and broad checks | The obsolete kit-only exclusion is removed; the physical source now belongs to the bootstrap mapping. Full scaffold, mapping-purpose and suite checks remain required before the slice is called complete. |
| Ratchet annotation | The old inline delta is retained as dated history. A new adjacent dated note records 1661→1663 SLOC for one mapping entry and one initializer command; it is not a function-complexity relaxation. |

The review found the per-parent context union, opt-out-before-read behavior,
typed malformed-carrier refusal, legacy prompt override, two-file build-surface
contract and real status import-denial test sound. It did not run tests.
Subsequent verification results belong in the
[execution record](../ai-template-redesign-2026-09-05-codex/EXECUTION-RECORD.md).

The [independent closure review](2026-09-06-redesign-code-closure-opus.md)
returned **APPROVE**. The three Windows/alias test cases passed locally in
0.24 seconds; the combined H1/dual-plan/complexity run passed 80 tests in
3.92 seconds before the extra Windows-path case. The broader freeze run still
owes the scaffold and inventory checks identified by the reviewer.
