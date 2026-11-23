+++
id = "WI-1058"
title = "WI-1057's verdict answered: SR-251's trigger fronted, and TC-483 covers LLR-406's key insertion and sorted append"
workstream = "process"
specref = "docs/reviews/wi-1057-adjudicate-fourth-sitting/001-ADJUDICATE-ca5a7d9.md"
sr_refs = ["SR-251"]
needs = []
buildtier = "medium"
safety_class = "ordinary"
priority = 2
+++

## Context

Filed on trunk on 2026-11-23 by the queue drill's coordinator, to answer
the fourth automated adjudication sitting's verdict (WI-1057, Gemini Neon,
the specref). That sitting blessed all nine amendments and accepted 16 of
18 rows. It returned two, both on SR-251's chain, and its `## Dispositions`
draft names this row's scope.

The findings, quoted from the verdict:

- **SR-251** (RETURN): "`Requirement` buries its event trigger between
  `shall` and the verb (`shall, on request, rewrite…`), which is the exact
  buried-condition trap §2(b2) forbids; because regeneration runs only on
  explicit request rather than ubiquitously during checks, front the
  trigger in event-driven EARS form (e.g., `When requested, the delivered
  harness shall rewrite…`)."
- **TC-483** (RETURN): it "leaves two explicit clauses of LLR-406
  unverified — (1) 'a case with no evidence key gains one' is exercised
  only in pure cell generation ('an empty cell with one declaration') and
  never through the TOML registry file writer inserting a new evidence key
  into a row that lacks one while preserving every other byte, and (2) 'a
  declared node the cell lacks is appended, joined by a semicolon and a
  space, in sorted order' is exercised with only a single missing declared
  node, leaving multi-node `; ` joining and sorted ordering unverified."

**LLR-406 is held.** The sitting ruled LLR-406 ACCEPT, and WI-1057's
derived act listed its flip. The commit hook's parent-first step refused
it under SR-251, which stays `Drafted`, so the act was taken without it.
Its flip stays owed under WI-1057's verdict. Once a later sitting accepts
SR-251, `compose_act` over that verdict lists it again, provided LLR-406's
text has not changed. So this row leaves LLR-406's text alone unless a fix
here needs it changed. If it does, LLR-406 goes back to a sitting with the
other rows.

Both rows are `Drafted`, so their text may change freely; neither is an
amendment.

## Done-when

- [ ] SR-251's requirement opens with its event trigger ("When requested,
      the delivered harness shall ..."), with one `shall` and nothing
      between it and its verb. Its acceptance criteria, rationale and
      coincident still agree with it.
- [ ] A test drives the regeneration through the registry writer over a
      test-case registry with a live case that has no evidence key. The
      case gains the key, and every other byte of the registry stays as
      written. It is tagged TC-483.
- [ ] A test appends two or more missing declared tests, declared out of
      sorted order, to one case. They land joined by a semicolon and a
      space, in sorted order. It is tagged TC-483.
- [ ] TC-483's method and expected name both cases, with evidence
      regenerated from the tags. No text this row writes names a code file,
      function, symbol or flag.
- [ ] Each test is shown failing first, or, where the behaviour already
      exists, shown to bite by a mutation of the code it drives, recorded
      in the Deliverable and never committed. The Deliverable lists the
      rows owed to the next sitting: SR-251 and TC-483 first acceptances,
      LLR-406 only if its text changed.
