# ADJUDICATE — WI-855 — re-sitting: the queue moved when WI-846 was released, at 75ca1b9c

This sitting re-sits one staleness question. The close refuses to enact the
`## Consolidation` block, because the queue digest recorded at the mint
(`20424540cd76`) no longer matches the live one (`83a94fde0f88`). The question:
against the queue as it stands now, does WI-846 becoming claimable change the
outcome? The first sitting (`001-ADJUDICATE-2d74139.md`) and the second
(`002-ADJUDICATE-e12a19e.md`) stand except where this file says otherwise. This
file supersedes 002 for the close, and its last line restates the complete
typed block.

Disclosure. I read both earlier verdicts and WI-855's spec in full. I also
read: `git show b2dfc1fa` (the OI-110 (b) ruling); WI-846 and WI-848 in full;
the Context and Done-when of WI-799, WI-816, WI-827, WI-828, WI-832, WI-833,
WI-849 to WI-854, and WI-834's part C (sign-in and consent); the reviewed
coordinator-cycle draft
(`docs/plans/2026-10-07-wi841-retro/drafts/coordinator-cycle/references/recipes.md`)
and `session-protocol` §2's adjudicator paragraph; `consolidate.queue_digest`,
`spine_digest`, `edged_text`, `parse_machine_line`, `reconcile_refusal` and
`_drift_refusal`; and `handback._enact_plan`. HEAD stayed at 75ca1b9c
throughout.

**1. What moved, verified.** The live digests, computed from this worktree,
are `consolidate.queue_digest(consolidate.read_rows(root)) = 83a94fde0f88` and
`consolidate.spine_digest(root) = 1237285c1cff`. The spine half is unchanged.
`git log 2d741392..HEAD -- docs/work/queued` lists one commit, b2dfc1fa. It
deletes WI-846's `needs = ["OI-110"]` line and rewrites WI-846's Done-when to
the ruling. With WI-846's `needs` patched back to `OI-110` and every other row
read live, `queue_digest` returns `20424540cd76`, the recorded value. So the
only change among the four hashed fields of the 35 queued work rows is that one
dropped wait, and the coordinator's claim holds.

**2. Where WI-846 now stands in the graph.** WI-846 waits on nothing. The seven
edges, once enacted, order after it WI-834, then WI-847 and WI-798, then WI-800,
then everything that waits on WI-800 or WI-798. In the cluster, those are
WI-801, WI-802, WI-804, WI-805, WI-807 to WI-811, WI-813 and WI-817. Nothing is
ordered before WI-846. That leaves thirteen cluster rows unordered against it:
WI-799, WI-816, WI-827, WI-828, WI-832, WI-833 and WI-848 to WI-854. I checked
each one against what WI-846 changes:

- the retained Claude launch's token authentication;
- the sign-in probe;
- dev-setup's `claude setup-token` step;
- SR-227's retire-on-failure clause;
- the coordinator procedure skill's sign-in guidance;
- a RESYNC entry.

Eleven share none of those:

- None amends SR-227 or LLR-270. The rows that do are WI-800, WI-802, WI-834
  and WI-847, and all four are ordered.
- None touches the session layer (`session_keep`, `session_service`,
  `session_adapters`), `coordinator_adjudicate.py` or dev-setup.
- The pre-filter's shared `adjudicate_brief.py` and `agent_loop.py` hints with
  WI-799 and WI-849 to WI-854 come from SR-level component maps. WI-846's
  deliverable edits neither file.
- WI-852 renders review and critique briefs and launches nothing. WI-801 owns
  launching, and it is ordered after WI-846.
- Each of the other rows hits "token" only through the
  `prompt-image-token-efficiency` knowledge pack, and "home" only as the
  archive's terminal home (WI-816) or a composition home (WI-854).
- Each RESYNC entry is its own anchored entry, so none collides.

WI-853 names the `coordinator-cycle` skill, but only for its sweep table, not
for sign-in. That leaves WI-848.

**3. The new collision: WI-846 and WI-848.** One of WI-846's Done-when bullets
reads: "The sign-in guidance in the coordinator's procedure skill
(`session-protocol` today, `coordinator-cycle` once it lands) describes the
token step, not an interactive sign-in." WI-848 lands `coordinator-cycle` from
its reviewed draft. That draft's adjudication recipe still says: "Wave 18
reports headless OAuth refresh failures pending WI-846; the owner runs `/login`
at expiry." When the first sitting judged, WI-846 was blocked on an open owner
question, so WI-848 would almost surely land first, and WI-846's "once it
lands" clause covered that order. Now both rows wait on nothing. Both can be
claimed on the same day, and WI-848 is the row the coordinator batches next
with WI-849. Two orders fail, and no gate catches either:

- WI-846 lands first. WI-848 then lands a new skill file, so nothing conflicts
  at rebase, but the file restores `/login` guidance. The handoffs now point
  at that skill for procedure. This undoes WI-846's guidance deliverable after
  it closed. WI-848's general clause, "reconciled with every row landed since
  2026-10-07", is the only thing that would catch this. Its "in particular"
  list names WI-849 and WI-851, not WI-846.
- Both are in flight. WI-846's builder sees no `coordinator-cycle` and edits
  `session-protocol` only. WI-848's builder reconciles against a WI-846 that
  has not landed. Whichever lands second may never see the other's text.

The direction follows the second sitting's delay comparison. WI-846 is on the
critical path: WI-834, then WI-847 and WI-798, then WI-800 and the rest of
S788. It is also the owner's operational fix for the unattended adjudicator.
Nothing in the queue waits on WI-848. Making WI-848 wait on WI-846 delays only
WI-848, and only by WI-846's medium-tier build. It also leaves WI-848's own
order intact: after WI-849, or in one batch with it, since WI-849 is unordered
against WI-846. The reverse direction is rejected because it would hold back
the critical path for a documentation row. Leaving the pair unordered is
rejected for the reason the second sitting gave: a row claimed while the other
is in flight cannot carry a deliverable that has not landed.

The close cannot enact this edge. WI-848 carries no `needs` line. So
`consolidate.edged_text` returns None, and `handback._enact_plan` would refuse
the whole verdict. WI-846 has no `needs` line either: b2dfc1fa deleted it
rather than emptying it. This is the WI-833 case from the first sitting, and
the first sitting's machinery finding applies again. So the edge is recorded
here for the coordinator, and the typed block keeps its seven edges. WI-848
lands second, so the obligation to carry the sign-in falls on WI-848 alone, and
a Done-when bullet makes it explicit rather than leaving it to the general
reconciliation clause. WI-846 builds exactly as filed: `session-protocol`
today, and `coordinator-cycle` too if it has landed.

**4. The existing edges, re-checked.** None is dropped or reversed.

- *WI-834 needs WI-846.* The first sitting gave two reasons, and one is now
  moot: built first, WI-834 would have settled the open OI-110 question in a
  lane. The others still hold:
  - both rows amend SR-227;
  - they share the sign-in step ("whichever builds first owns it");
  - the reconciliation's §8.2 asks the SR-227 amendments to run in series;
  - status says to build the token row first.

  WI-846's release makes the edge cheaper, because WI-834 now waits on a
  claimable row rather than an owner ruling. The second sitting's
  WI-798 → WI-834 edge reaches WI-846 through this one, so dropping it would
  leave WI-798 unordered against the home it migrates.
- *WI-834 against the ruling: no contradiction.* Part C reads "the configured
  token is present and readable, WI-846", and its consent step keeps the
  token "in a file at the declared location outside the repository". Both
  agree with (b), because an environment variable is what declares the
  location. WI-834 is ordered after WI-846, so it builds against WI-846's
  landed text.
- *The other five edges and the second sitting's WI-798 bullet* do not involve
  WI-846's needs. The second sitting already took WI-846 as released by OI-110
  (b). The bullet is carried forward unchanged.

- [MINOR] WI-848 / WI-846 -> WI-846's release by OI-110 (b) makes both rows
  claimable on the same day. WI-846 must make the coordinator procedure
  skill's sign-in guidance describe the token step (`coordinator-cycle` once it
  lands). WI-848's reviewed draft lands that skill saying the owner runs
  `/login` "pending WI-846". If WI-848 lands second, or alongside, it restores
  the interactive sign-in guidance WI-846 retired, with no rebase conflict and
  no gate to catch it. -> the coordinator adds the edge WI-848 needs WI-846 by
  hand (`needs = ["WI-846"]` in WI-848's frontmatter) before claiming either
  row. The close cannot write it, because WI-848 carries no `needs` line. Give
  WI-848 the Done-when bullet below.

```toml
done_when = [
  { row = "WI-798", bullet = "The per-family home's authentication moves to the account home and is not retired with it (WI-846, WI-834). This repo's dedicated Claude home becomes a declared account. A retained Claude launch under that account still reads the owner's long-lived token at launch through the environment variable OI-110 (b) declares: nothing about the path is tracked, and the token is never written to a log, prompt, record or commit. An unset variable, or a missing or unreadable token file, is still refused before launch, naming dev-setup, and an authentication failure still retires no session. The sign-in probe and dev-setup's check and `claude setup-token` offer report on that account's home. The adjudicator that ran signed in before this row runs signed in after it. WI-846's and WI-834's tests stay green, re-pointed at the account home rather than deleted, and the RESYNC entry states the migration." },
  { row = "WI-848", bullet = "The coordinator-cycle recipes carry WI-846's sign-in as landed: the adjudication recipe's sign-in step names the long-lived token read through the environment variable OI-110 (b) declares, and dev-setup's one-time `claude setup-token` step as the remedy for a home that is not signed in. The draft's 'pending WI-846; the owner runs `/login` at expiry' line does not land, and no recipe makes an interactive sign-in the procedure." },
]
```

OUTCOME: QUEUE-WITH-EDGE needs=WI-834;WI-847;WI-800;WI-851;WI-808;WI-801;WI-798 absorbs=-
