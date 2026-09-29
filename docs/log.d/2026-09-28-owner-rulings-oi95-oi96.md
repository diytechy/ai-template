## 2026-09-28 — The owner rules OI-95 and OI-96; OI-97 stays open for a breakdown

The owner answered the three pending open items in one message. Their words
are quoted in each row's `decision` cell in
[../requirements/open-items.toml](../requirements/open-items.toml); this entry
records what each ruling sets in motion.

**OI-95 — (a).** "Agree with recommendation." OI-76's record gains a dated
correction: the `Review-Verdict` trailer rides the commit that records the
round, written by the coordinator, which is where the build already puts it.
`kitlib/verdict.py`'s header cites the corrected ruling. No code, test or
adopter file moves, so no RESYNC entry is owed.

**OI-96 — (a), with a sequencing condition.** The shrink floor becomes a
rendered-pixel minimum for node labels. The owner's condition: "I would prefer
for other work items to be completed (unless there are dependencies) until
perception judgement happens again just so more churn waits till the queue is
mostly free." **WI-722** amends LLR-116 and TC-121, builds the floor and
settles TC-055's T5 finding at 1280 px. It is filed deferred at priority 0.
WI-713, TC-055's re-judge, now needs WI-722 rather than OI-96, so both wait.
No other row depends on them. The coordinator moves WI-722 to `queued/` once
the ordinary frontier has largely drained, and TC-055 keeps its recorded FAIL
until then.

**OI-97 — pending.** Before ruling, the owner asked for a breakdown of the
nine requirements, with a diagram of how each one's information flows, to
judge the scope and impact. The breakdown was given in the session. The row
is unchanged.

Deferred open items: OI-97, pending the owner's reading of the breakdown.
