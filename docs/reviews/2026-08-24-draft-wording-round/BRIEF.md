# Review brief - simplify the approval-pending Drafted spine text

Provider: OPENAI family, `OPENAI-TERRA` (`gpt-5.6-terra`) via `codex exec`,
the row `docs/agents.toml` declares and `docs/agents-enabled` consents to.
Probed live before dispatch (trivial PONG prompt, returned clean).

Four batches, prompt on stdin, result captured with `-o`:

| batch | rows | raw return |
|---|---|---|
| 1 | LLR-187, LLR-199, LLR-202, LLR-193, LLR-198 | `RAW-BATCH1-LLR-A.md` |
| 2 | LLR-201, LLR-200, LLR-196, LLR-194 | `RAW-BATCH2-LLR-B.md` |
| 3 | TC-196, TC-195, TC-197, TC-182, TC-188 | `RAW-BATCH3-TC-A.md` |
| 4 | TC-194, TC-198, TC-192, TC-191, TC-189 | `RAW-BATCH4-TC-B.md` |

Each row was sent with its ANCHOR SR's `Requirement` and `AcceptanceCriteria`
as the intent anchor. The instruction head, identical in all four batches:

```
You are a cross-family REVIEWER (OpenAI family) working for the owner of a
requirements-traced software process kit. The owner must personally APPROVE the
rows below and has said, verbatim:

  "The text on these items that need approval still seems pretty heavy. Can you
   spin up an openai terra review to suggest more simplified wording and accept
   suggestions that still fit the intent of the SR?"

YOUR JOB, per row and per cell: suggest SIMPLER WORDING that preserves the FULL
normative intent. Then flag anything you would CUT as either
(a) REDUNDANT-WITH-PARENT (already stated by the anchor SR shown with the row),
or (b) GENUINELY LOAD-BEARING (must survive any rewrite, say why).
Do NOT weaken obligations. Do NOT delete a guard clause, a negative claim
("reported and never gated", "no declared improvement target", "not discharged",
"vacuous when ..."), a stated residual/build-gap, or a severity split. Those are
the reason the row exists.

TIER DISCIPLINE the rewrite must still satisfy:
- LLR `Title` names the module/mechanism the row is about (not the obligation).
- LLR `Detail` states the DESIGN — module, mechanism, the decisions it makes.
  It must NOT contain the word "shall" (that is the requirement tier's voice).
- TC `Method` states CONCRETE verification method: what is driven and what is
  asserted. TC `Expected` states the concrete expected outcome.

HARD PROSE RULES — a suggestion that breaks one of these is unusable:
1. NO work-item / open-item / decision ids (WI-nnn, OI-nnn, D-nn), NO dates,
   NO references to reviews, sittings, rulings, or to the process documents.
   A row states the system and its standing reason, never its own history.
2. NO vague/unfalsifiable terms: etc., as appropriate, as needed, if possible,
   minimal, optimal, appropriate, robust, efficient, flexible, sufficient,
   adequate, reasonable, seamless, intuitive, easy to use, user-friendly,
   and so on, TBD, TBC.
3. NO open-ended clauses: "including but not limited to", "at a minimum",
   "among others", "such as".
4. Keep every concrete identifier (module paths, function names, registry
   filenames, id references like SR-nnn/LLR-nnn/IF-nnn) that the current text
   carries — those are evidence a reader checks, not decoration.
5. Plain ASCII. No markdown headings inside a cell. One paragraph per cell.

OUTPUT FORMAT — exactly this, per cell, nothing else:

=== <ROW-ID> <CELL>
SUGGEST: <the full replacement text, or the single word KEEP if you cannot
          simplify it without losing intent>
CUT-REDUNDANT: <clauses you dropped that the anchor SR already states; or none>
CUT-KEPT: <clauses you deliberately did NOT touch and why; or none>
RISK: <what intent could be lost if this is accepted; or none>

Be aggressive about length where the text merely restates itself, and
conservative where it carries a guard. Aim to cut 30-50% of characters on the
worst offenders and 0% where the text is already tight.
```

Adjudication (every suggestion confirmed or refuted, per cell): `RESUME.md`.
