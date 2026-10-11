# ADJUDICATE — WI-892 @ d0fe3e3: Done-when edit after claim

One bullet was rewritten in commit `d0fe3e32`. `kitlib.done_when.changes`
reports a rewrite as two entries, the claim-time item it no longer carries and
the item that replaced it, so both are judged below.

The two obligations are mutually exclusive. The claimed bullet asks the
module-size baseline to *record* both modules. The current one asks that
*neither* carry a baseline entry, and that both stay under the threshold. A
close that satisfied the old text, with a baseline entry for each module, fails
the new one. And the new text binds something the old did not: the new module
must itself stay under 1000 SLOC. The old text let it take a reviewed baseline
entry above that. So the scope MOVED; this is not clarity.

I bless the move. I checked one fact in the code: `tests/test_module_size_ratchet.py`
keeps an exact entry only for a module above `THRESHOLD = 1000`, and its rule
says an entry for a module that drops under the threshold is deleted. A
literal reading of the claimed bullet therefore asked for entries the ratchet
refuses. The current text is the satisfiable form of the same check, so a
reviewer still tests the item against the same ratchet. The one widening,
that the new module stays under the threshold, serves the Context's stated
purpose directly. The row exists because `acceptance_record.py` was about to
cross the ratchet, and the ratchet's own docstring names a module that "stays
under THRESHOLD" as the intended exit for moved lines. The owner would
recognise this as the same work. No part of the purpose is dropped or deferred,
so no successor is owed.

- [MOVED] claimed bullet 4, "... and the module-size baseline records both modules" -> the existing tests pass unchanged (beyond import lines) AND the size baseline holds an entry for each of `acceptance_record.py` and the new module -> (replaced by the item below) -> it is not the same: the baseline-entry obligation is gone and its opposite is now required. Blessed: under the ratchet's rule (exact entries only above THRESHOLD = 1000) the old obligation could not be met for a module under the threshold.
- [MOVED] current bullet 4, "... the module-size ratchet passes with both modules measured: ... each stay under its SLOC threshold, so neither carries a baseline entry" -> (the claimed bullet above) -> the existing tests pass unchanged (beyond import lines) AND the ratchet passes with `acceptance_record.py` and the new module each under the 1000-SLOC threshold and neither baselined -> it is not the same: it forbids the entries the old text required, and it newly binds the new module under the threshold, which the old text left open to a reviewed entry. Blessed: it is the satisfiable form of the same size check, and it serves the Context's purpose that the move must not create a new monolith.

DONE-WHEN: BLESSED changes=2 digest=sha256:2f483f24c188f277
