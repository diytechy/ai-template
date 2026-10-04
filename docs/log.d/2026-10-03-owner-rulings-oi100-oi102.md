Deferred open items: none

## 2026-10-03 — The owner rules OI-100, OI-101 and OI-102

The owner's words are quoted in each row's `decision` cell in
[../requirements/open-items.toml](../requirements/open-items.toml).

### OI-100 (a): amended needs reach the meaning-or-clarity adjudication

"Agreed with recommendation."
- Need, assumption and surrogate amendments route to WI-388's amendment
  adjudication.
- On a held rung, the adjudicator re-attests the rows it rules CLARITY and
  recommends the MEANING rows.
- The brief's CLARITY aftermath names its rows in the act.
- Gap 3's coupling stays.
- **WI-791** carries the build.

### OI-101: WI-788's six questions

- **Q1 (a).** In the spine-authoring flow, the adjudicator's final pass is the
  approval act only if it changes nothing. Any change goes back to the adjudication
  reviewer, bounded at 3 rounds.
- **Q2 (a).** Risk 6 applies on lane and trunk: no commit changes spine text together
  with a snapshot update. "Amend-plus-flip is approval" retires everywhere.
- **Q3.** Grok and FreeAI route through OpenCode. The owner asked whether the
  coordinator can work with that CLI. Yes: the kit already has an Opencode adapter, a
  recorded `run --format json` fixture, and live Kimi and Grok routes. On 1.18.30:
  - `opencode models` lists free `opencode/*-free` models;
  - `opencode/big-pickle` answered PONG;
  - `mimo-v2.5-free` returned a server error;
  - a JSON-format run timed out.

  FreeAI is read as those free models, to be confirmed at WI-788's checkpoint.
- **Q4.** Live probing is authorized, and only OpenCode needs it. Google's CLI is
  researched from its documentation and marked untested.
- **Q5 (a).** The glossary is kit-shipped: `project-trajectory/GLOSSARY.md`.
- **Q6.** The owner said the S11 §6 questions "were already ruled ... perhaps some
  documentation was missed".
  - **What the record shows:** the wave-9 log holds the direction "adjudication in
    the lane: yes". The plan written after it still listed seven questions, and
    status.md and the wave-10 handoff carried them as owed, which is why OI-101
    raised them again.
  - **What changed:** they are now recorded as ruled, as their recommendations
    stand, in the plan's §6. Q7's "fallback" is read as the one existing path
    (exhausted rounds land, and today's mint takes the rows), not a second code path.

WI-788's Done-when now carries these.

### OI-102: WI-790's three questions

- **Q1 (a).** Ruling an open item adds a confirmation criterion to each row citing it,
  even for a gate on a person's act.
- **Q2 (a).** While a pending item has no queued citer, open-items.html shows an
  integrity notice naming it.
- **Q3 is neither option.** In the owner's words: "Why does this need git history? A
  commit should happen at the end of a session iteration. If that session ... touches
  an OI status to close it without removing or updating the "Done When" section of
  the corresponding WI, the commit should block."
  - The rule reads one diff, a commit against its parent. That is HEAD against the
    staged tree at the pre-commit hook, and each lane commit against its first parent
    at the merge slot.
  - Each item leaving `pending` must be matched by an update to, or removal of, the
    Done-when of each row that cites it in the parent tree, or by the row being
    removed or closed.
  - No deep history is needed.

WI-790's design 6, A1, A2 and Done-when now carry these.

### Applying the owner's new rule to these rulings

The rule is not built yet. The rows these rulings touch still had their Done-when
updated in the same commit:
- WI-788 for OI-101;
- WI-790 for OI-102;
- the new WI-791 for OI-100.
