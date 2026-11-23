+++
id = "WI-1062"
title = "WI-1061's verdict answered: SR-251's chain states its live scope, the keyless condition and an all-or-nothing write"
workstream = "process"
specref = "docs/reviews/wi-1061-adjudicate-fifth-sitting/001-ADJUDICATE-0385b75.md"
sr_refs = ["SR-251"]
needs = []
buildtier = "medium"
planmode = "none"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, to answer
the fifth automated adjudication sitting's verdict (WI-1061, Gemini Neon,
the specref). That sitting judged SR-251's chain whole, after WI-1058
answered the fourth sitting's two returns, and returned all three rows.
Its `### Dispositions` draft names this row's scope.

The findings, in short (the specref quotes them in full):

- **SR-251 and LLR-406 disagree on scope.** SR-251 rewrites "each test
  case's evidence cell", while LLR-406 rewrites "each live test case". The
  sitting asks both to say the same thing, and to say what happens to a
  case outside that scope.
- **LLR-406's keyless clause is unconditional.** "A case with no evidence
  key gains one" contradicts the identity clause for a keyless case that no
  declaration names. It gains a key only when a declaration supplies a part.
- **No all-or-nothing write.** SR-251 carries the integrity-recoverability
  concern (`hat_refs`) for a registry rewritten in place, but neither row
  says what an interrupted write leaves behind.
- **TC-483** verifies none of the three.

**What "live" means here, as the code reads it.** The regeneration reads
the cases the test-case registry holds. A retired case is deleted from the
registry, so no row stays behind for the rewrite to touch. The case outside
the scope is a test file that still declares a case the registry no longer
holds. The rewrite adds no row for it and names no such case. The rows
state it that way, and the test drives it.

**The write.** Today the writer writes the registry in place. The kit
already has one all-or-nothing file writer (`kitlib/observation.py`'s
`write_atomic`, under SR-199 and LLR-234): it writes a temporary file
beside the target, then moves it into place in one replace. The registry
writer reuses it rather than adding a second one. It keeps the file's own
line endings, which the writer reads and writes back. If reusing it would
cross a component boundary that no interface row declares, the builder
stops and reports before writing one.

**LLR-406 and WI-1057's held flip.** The fourth sitting accepted LLR-406
and the fifth returned it. Its flip, held under WI-1057's verdict, is
therefore void: no act takes it from that verdict. LLR-406 goes to the next
sitting with its chain, and its flip comes from that sitting's verdict.

**Why one row.** As at WI-1058, the sitting judges the chain whole, so the
three rows' repairs land together as one branch before the next sitting.
**Planning** is `none`: one writer swap, wording settled here, and tests
stated below.

## Done-when

- [ ] SR-251's requirement and acceptance criteria scope the rewrite to the
      test cases the registry holds. A declaration naming a case the
      registry does not hold adds nothing and is not reported as changed.
      The acceptance criteria add that an interrupted rewrite leaves the
      registry's bytes as they were before or as fully rewritten, never
      partly written. One `shall`, the event trigger kept in front.
- [ ] LLR-406 says the same about scope, gives a case with no evidence key
      a key only when its declarations supply a part (a keyless case no
      declaration names stays keyless and unchanged), and states that the
      registry is replaced whole by an all-or-nothing write.
- [ ] The registry writer writes through the kit's one all-or-nothing file
      writer, keeping the file's line endings and encoding. No second
      writer is added.
- [ ] Tests, each tagged TC-483: a declaration naming a case the registry
      does not hold changes nothing and is not named; a keyless case that no
      declaration names stays keyless and the registry's bytes are
      unchanged; a replace step that fails leaves the registry's bytes
      unchanged and no temporary file behind. A new behaviour is shown
      failing first; one that already holds is shown to bite by a mutation,
      recorded in the Deliverable and never committed.
- [ ] TC-483's method and expected name the three cases, with evidence
      regenerated from the tags. No text this row writes names a code file,
      function, symbol or flag; each child stays inside its parent. The
      Deliverable lists the rows owed to the next sitting: SR-251, LLR-406
      and TC-483 first acceptances.
