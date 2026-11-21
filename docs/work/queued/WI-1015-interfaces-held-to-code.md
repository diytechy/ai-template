+++
id = "WI-1015"
title = "The code is held to its interface and LLR rows, and the cross-component rule's loopholes close"
workstream = "process"
sr_refs = ["SR-159", "SR-157"]
specref = "docs/reviews/2026-11-21-code-vs-interfaces/README.md"
buildtier = "strong"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed by hand on 2026-11-21 at the operator's direction. The operator wants
the code to read as the compiled decomposition of the spine, with every link
pointing up the chain and drift prevented where links are kept. A measurement
of the tree (`docs/reviews/2026-11-21-code-vs-interfaces/`) found the upward
links largely present but the interface layer loosely held:

- **The cross-component rule (LLR-067, SR-159) already scopes which seams
  need a row,** and that scope stays: an import into a kernel-allowlisted
  module (189 of the 340 imports no call row declares) or between modules of
  one component (82) needs none. Its check reports no finding today.
- **Loophole 1, cover.** Any interface row naming both modules counts as
  cover, on any channel and whoever owns it. Six cross-component imports
  pass only that way; `check_assumption_gate` imports `record_observation`
  as a call and is covered by `record_observation`'s CLI row.
- **Loophole 2, overlap.** A module tagged into several components silences
  the rule on every edge it touches: 32 such modules, 63 edges, reported
  only as an advisory.
- **Nothing compares a row with the code in the other direction:** 15
  declared requestors do not import their owner; about 9 of the 101
  `name(args)` signatures in `data` cells no longer match the owner; 7
  symbols LLR CodeSymbol cells name exist nowhere and 3 have moved; about 25
  CodeSymbol cells hold prose or CSS tokens.
- **125 of the 268 interface rows have no test case,** though PROCESS.md §8
  says every interface is backed by one; no row uses `verified_by`.

The test-file link already shows the target shape: a test's `Implements:`
tags and its test case's `Evidence` are held equal both ways, and a mismatch
fails `--strict`.

## Done-when

- [ ] A cross-component import is covered only by a row for that seam: a
      `call` row owned by the imported module that names the importer as a
      requestor. LLR-067's amendment is drafted for the operator's
      acceptance.
- [ ] A module tagged into several components no longer silences the rule.
      The scope critique chooses between re-tagging the 32 modules to one
      component each and treating an overlap as a crossing; either way the
      63 edges are covered or shown to be inside one component.
- [ ] For every `call` row, each declared requestor imports the owner,
      directly or through a re-export the owner's contract names.
- [ ] Every `name(args)` in a `data` cell names a function, class or
      re-export the owner defines, with the arguments it takes.
- [ ] Every symbol an LLR's CodeSymbol names resolves in that row's Module;
      a cell that names no code symbol says so in a form the check reads.
- [ ] Each interface row is verified by a test case's `Verifies`, or names in
      `verified_by` the parent row whose tests cover it.
- [ ] The new findings are warn-first and fail `--strict`, like their
      siblings, and today's drift is cleared in this row so the gate lands
      green.
- [ ] The kernel allowlist and the one-component exemption are unchanged.
