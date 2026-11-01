# WI-977 checkpoint sitting at a7ebe2f

## amendment

Twenty-three approved rows moved against their copies (anchor 2aaf9f66f). They carry WI-977's one change: the spine batch retires, so every admission, claim, resume, worker assignment and close names exactly one work item.

What I compared, cell by cell:
- each row's live text against its anchor, and against `contract_split`'s text at 961f9e47, which the spec names as the target meaning;
- the rows' text before and after the W14 reconcile (9e1116b to a7ebe2f), and the round-2 findings that reconcile was to answer (REVIEW-B 003's two MAJORs, REVIEW-A 004's MINORs);
- the code, where a row's new text states a fact about it: the worker template, and the disposition sweep in `intake.py`.

`trace.py --strict` exits 0 at this tip. The live cells match the brief's after text byte for byte.

**The verdict.** Every row but one changed MEANING:
- **Bless (4):** SR-144, SR-148, SR-156 and TC-146. The released rung lets the act turn re-attest them.
- **CLARITY (1):** LLR-058, which changes only its title, and its detail never stated the ordering the old title named.
- **Returned (18):** I would not bless these, for two reasons that recur.

**Why 18 rows return.**

1. **Obligations deleted, or replaced by pointers.** The spec allows only the batch clause to change: "only that clause is replaced, in the same voice, and the rest of the cell waits for item 5's migration" for LLR-152, LLR-207, TC-146 and TC-205, and "H's text stays" for the rest. Yet several cells drop approved obligations, or replace them with "retain their stated assertions" / "retain their stated refusals". Those phrases point at text the same edit deleted. A TC whose method says an arm "retains its stated assertions", with that statement gone, binds the arm to nothing. A later edit could weaken the test and nothing in the spine would object.
   - D-019 says "no pointer phrase left in the 23 rows". The W14 reconcile reworded "existing" to "stated" and kept the pointers.
   - The same reconcile compressed LLR-207 and TC-205, which at 9e1116b had kept their full text with only the batch clause replaced, down to one-paragraph summaries.
   - This is the failure REVIEW-B 003's MAJORs named, and it is a Done-when gap ("The 23 rows above carry their target meaning").
2. **Corrupted text.** LLR-061, LLR-150 and LLR-152's Detail and TC-144's Method each hold a U+FFFD replacement character (bytes EF BF BD) where an apostrophe was: "branch�s", "lane�s", "row�s", "lane�s". I would not attest a cell holding a corrupted character, however small the fix.

**Per row:**

- [MEANING] LLR-061 Detail, Title -> before: explicit `--wi`/`--train`/worktree assignment replacing `--track`. The prompt is built from AGENTS.md, the WI row, SpecRef, predecessor context, train diff and rework finding, never the generated status surface, plus every assigned row's walk state on a multi-row lane. Logs and review evidence are collision-safe and per assignment, naming the exact reviewed commit. The prompt never includes docs/status.md. The worker never edits root status, others' claims, the root log or generated artifacts. The result channel is `WI:` / `Blocked-WI:` + `BlockRef:` -> after: one assignment; the multi-row block is gone; empty, malformed or multi-item assignments refuse before a session -> not the same: cardinality narrows and a refusal is added. Return:
  - The prompt's AGENTS.md input is dropped. The worker template still opens "Read AGENTS.md first".
  - "the prompt never includes docs/status.md" is dropped, while the template still says "Do not resume from docs/status.md".
  - "naming the exact reviewed commit" is dropped from the evidence clause.
  - The blocked result channel (`Blocked-WI:` + `BlockRef:`) is dropped, leaving only "committed trailer evidence".
  - The cell holds U+FFFD ("another branch�s claim").
- [MEANING] TC-061 Method -> before: a full method naming each asserted arm:
  - the composed prompt's inputs, the docs/status.md prohibition, the context block only when the registries join, the one-turn close bar, and close commands resolved at the repository's own scripts path;
  - the result channel: `WI:` ends DONE, a relaunch spends no session, `Blocked-WI:` writes no block record, no trailer runs to the budget ceiling, and done-detection defers on an open review, a pending rework or an uncommitted path;
  - no run-state, iteration-index or tracks file; concurrent tag-prefixed logs; managed review under reviews/<tag>/ naming the commit;
  - the preflight refusals (traversal tag, `--train` without `--wi`, detached HEAD, unknown/done/cancelled WI, unresolvable base), and `--track` refused as an unknown flag.

  -> after: the one-item refusal and the one-row prompt are added. Everything else becomes "retains the declared close and context behavior" and "The result, relaunch, blocked, budget, review, concurrent-worker, managed-review and preflight refusal behaviors retain their stated assertions" -> not the same: the verified set loses every named arm. Return: restore each arm's assertion in capability voice (REVIEW-B 003's second MAJOR). `contract_split`'s TC-061 shows the arms can be stated without code names.
- [MEANING+BLESS] SR-144 Requirement, AcceptanceCriteria -> before: a terminal partial close with one immutable report, refusing an undeclared split and a second close; a multi-spec close that refuses restores every report it wrote -> after: the same, also refusing a close whose claim is other than one work item. A refused single-item close restores its one report and leaves claim and terminal state unchanged, and a non-single claim refuses before any report or state change -> not the same: the close gains a cardinality refusal, and the restore narrows to one report. Ready to bless:
  - It is the spec's target (`contract_split`'s meaning).
  - The acceptance is observable at "before any report or state change".
  - It names no carrier.
  - It stays apart from SR-156: SR-156 owns the claim, assignment and resume inputs, and this row owns the close.
- [MEANING] LLR-144 Detail -> before: the partial close moves each spec to terminal partial/ and writes one immutable report under docs/handbacks/; any refusal restores every report; quarantine as stated. The outcome is read off the spec's directory: complete/ = merged, cancelled/ = cancelled, any open folder = handback. Every lane ends in a merge -> after: a non-single claim refuses first; one spec moves, and one report is restored on refusal; quarantine is kept -> not the same: cardinality narrows. Return:
  - The directory-to-outcome mapping is dropped. No other LLR states it; I searched the design registry. The unchanged rationale still argues for it: "Making the outcome the directory leaves no fourth answer".
  - The report's home (docs/handbacks/) and the patch's home (docs/work/handback/) are dropped. Other readers find the record at those paths, and the LLR tier may name them.
- [MEANING] LLR-161 Detail -> before:
  - the report is written first; a second report is refused; every report is restored on refusal;
  - the disposition is titled on the report PATH and nothing else;
  - the sweep says so LOUDLY when a terminal spec has no report, rather than minting zero rows quietly;
  - one disposition per close; a disposition never mints for itself ("refused at both ends");
  - a successor carries lineage "that survives the id change";
  - a successor is adopted or drafted.

  -> after: the single report is restored on refusal, leaving claim and terminal state unchanged; the rest is condensed -> not the same: the restore narrows. Return:
  - The report-path key is dropped, while the unchanged rationale still argues it: "The path is the only token in the event's identity that cannot move".
  - "A terminal specification without a report refuses loudly" misstates the code. `intake.py`'s sweep prints the missing report to stderr and continues with the next spec; it refuses nothing. Restore "says so loudly rather than minting zero rows quietly".
  - "refused at both ends" and "survives the id change" are dropped.
- [MEANING] TC-138 Method -> before: the handback suite's close and quarantine arms, the report written under docs/handbacks/, and the failing diff kept as a bar-inert .patch, with the rename read "mutation-proven" -> after: the empty and multi-spec refusal is added, and the arms are condensed -> not the same: a refusal arm is added. Return:
  - "bar-inert" is dropped from the kept patch, so TC-138 no longer verifies LLR-144's own "bar-inert patch" clause.
  - The report's location is dropped.
  - "mutation-proven" is dropped. That was a statement of how strongly the rename arm is verified.
- [MEANING] TC-156 Method -> before: the close is clean under the real check, loud with no report, and a second close leaves no residue. The disposition is keyed on the report path, so a re-sweep mints nothing, and an owed successor is drafted or an already-filed superseding row adopted -> after: the single-report restore arm is added, and "disposition, re-sweep, drafting and adoption retain their stated assertions" -> not the same: a pointer replaces the keyed-on-path and adoption assertions, which the W14 reconcile removed. Return: restore those two assertions.
- [MEANING+BLESS] SR-148 Requirement, AcceptanceCriteria -> before: select the work an unattended run does next, in the stated order -> after: select exactly one work item for each admitted assignment, spine admission included; an ordinary frontier fills several lanes through separate single-item assignments; every other clause is kept verbatim -> not the same: admission cardinality is bounded. Ready to bless:
  - It is `contract_split`'s meaning.
  - It is observable per assignment, and the adjudicated-successor clause is kept.
  - Note, not a finding: the spec also asks the rationale to say that admission cardinality here and claim cardinality in SR-156 bound one contract at two boundaries. The rationale was not amended. The two rows' decisions stay distinct (what admission yields, what a lane accepts), so this does not stop the blessing. The sentence is still owed under the Done-when.
- [CLARITY] LLR-058 Title -> before: "WI-DAG frontier + deterministic traincar ordering" -> after: "WI-DAG dependency-ready frontier" -> the same: the detail, which is unchanged, states only the frontier. Ordering was never this row's obligation; it is LLR-123's. A reader acting on the old row acts identically on the new one.
- [MEANING] LLR-123 Detail, Title -> before: orders traincars, the tiebreak is the first WI id, and the order is identical across ready --explain, ready --format json and simulate --jobs 1's serial schedule -> after: orders work items, the tiebreak is the work-item id, and the order is identical "across the declared scheduling views" -> not the same: the ordered unit changes. Return:
  - The closed set of three views becomes "the declared scheduling views", and nothing declares them, so the identity property's domain is open.
  - The spec asked only for "traincar" to become "work item". LLR-058's approved detail names these same views, and `contract_split` keeps them. Name them, or describe them by role (the ready report in its explained and machine-readable forms, the serial simulation).
- [MEANING] LLR-149 Detail -> before: the §A8 table verbatim per kind × held answer, consuming the kind classification; all spine rows admit as one batch; attended attestation/gate rows drain with exit 0, naming the open-items cards; the lane ladder; the gap census -> after: the first spine row admits alone and the rest wait for later exclusive turns; held rows surface even under keep-nondependent; delegated-tier rows go one at a time, exclusive; the ladder and census are kept -> not the same: the batch arm retires and the stale single-approve sentence is corrected to the code. Return:
  - The drained stop's "exit 0, naming the open-items cards" is dropped. It is the observable a caller acts on, and `contract_split` keeps the cards.
  - The row no longer says that it consumes the kind classification, which TC-143's agreement arm verifies.
- [MEANING] LLR-152 Detail -> before: the adjudication kind is exclusive at rank 1; its lane runs no product bar, but the refresh still commits a verified no-bar attestation; a mixed batch or unreadable frontmatter fails toward the bar; the batch's strictest bar value goes to the gate check -> after: a lane whose one row is any other kind, or whose frontmatter is unreadable, runs the bar; that one row's key is forwarded; absent keys forward none; malformed values refuse -> not the same: the batch arms become one-row arms. Return for one reason only: the cell holds U+FFFD ("that one row�s key"). Otherwise I would bless it, because the obligations survive.
- [MEANING] TC-058 Method -> before: frontier, exclusions and traincar order match across ready --explain, ready --format json, simulate and the dispatcher -> after: work-item order matches "across its declared views and the dispatcher" -> not the same: the ordered unit changes. Return: the same open domain as LLR-123. The named views are dropped, though the spec asked only for the unit to change and `contract_split` keeps them.
- [MEANING] TC-143 Method -> before: the admission suite, including the §A8 table verbatim per kind × level -> after: the first spine row alone, and the table reduced to "surfaces held rows, preserves non-dependent work only where declared, and dispatches autonomous held rows exclusively" -> not the same: the batch arm retires. Return:
  - The new method never asserts LLR-149's key corrected clause: a held attestation or gate row still surfaces at the keep-nondependent close, and its hold is never released. `contract_split`'s TC-143 asserts both.
  - "preserves non-dependent work only where declared" names no observable.
- [MEANING+BLESS] TC-146 Method -> before: the adjudication cases with a mixed-batch bar arm -> after: a lane whose one row is any other kind runs the bar; the declared, undeclared and malformed bar arms are kept -> not the same: the batch arm becomes a one-row arm. Ready to bless:
  - Every assertion its LLR-152 obligations need is stated, including the gate value observed off the recording stub.
  - Note, not a finding: "the reserved slot, pinned by name" is dropped, a detail of how the rank is pinned; the rank itself is still asserted.
- [MEANING] TC-154 Method -> before: adjudication ahead of a spine batch; a stable partition; a red TC named only under a `done` citer, with the three exempt statuses and the mixed-target case driven; the census grammar round-trips and matches nothing else -> after: adjudication ahead of a spine work item; "the completion and census grammar assertions retain their stated cases" -> not the same: the unit changes. Return: the pointer replaces the red-TC citer and census-grammar assertions. The spec asked only for "a ready spine batch" to become "a ready spine work item".
- [MEANING] TC-205 Method -> before: the full verdict-record method:
  - identity and encoding;
  - trailer grammar and name parse;
  - the gate's phase, log and attestation arms;
  - the verified carrier and the writer driven end to end;
  - the resume's owed set;
  - both peels and their refusal arms;
  - the dial, scope and filing boundary;
  - the bar attestation;
  - and its tier argument.

  The spec's change was one clause: the two-row batch arm. -> after: one paragraph: "Drive verdict identity, evidence, phase, scope and attestation behavior beside their refusal cases", the one-row peel, and "retain their stated refusals" -> not the same: it is the spec's batch-clause change plus the loss of nearly every named arm. Return: restore the method from its 9e1116b text and replace only the batch-shape clause. That clause becomes: a close moving two rows does not peel, under the historical joined subject and under the current one-id subject. Also carry REVIEW-A 004's note: the empty close's refusal comes from cardinality, and one source branch follows from one deletion.
- [MEANING+BLESS] SR-156 Requirement, AcceptanceCriteria -> before: bounded isolated lanes narrowing through one serial seam -> after: exactly one work item per lane. Empty or multi-item claim, assignment and resume inputs refuse before changing state, and historical multi-item records stay readable as evidence and never run as claims. Every other clause is kept verbatim -> not the same: lane cardinality is bounded, with a refusal and a history clause. Ready to bless:
  - It is `contract_split`'s meaning.
  - The refusal is observable.
  - The history clause is the fit criterion of the Requirement's existing "reconstructing claim and queue state from version-control history alone", so it mints nothing the Requirement lacks.
- [MEANING] LLR-150 Detail -> before: ensure the lane worktree (the one home both the worker and the refresh agree on); forward the session dials; launch the worker non-blocking, with a blocking form kept as a declared seam; run the refresh as the lane's own subprocess; tree signal plus exit codes, no state file and no back-channel -> after: hand the worker one item; a parked resume refuses a non-single assignment before mutation or launch -> not the same: cardinality narrows and a refusal is added. Return:
  - The cell holds U+FFFD ("the lane�s own").
  - "the one home both the worker and the refresh agree on" is dropped.
  - The non-blocking launch and its declared blocking seam are dropped, though the seam still sits in the row's traced symbols.
- [MEANING] LLR-151 Detail, Rationale, Title -> before:
  - the safety-class refusal is deleted, and admission is the dispatcher's decision;
  - the claim requires the dispatch lock at one site, with the ladder run first;
  - the claim commits through the bookkeeping helper, which refuses by name a dirty path the claim must write and never stages the lock's own file;
  - batch-aware claims;
  - the integration takes an optional branch restriction, so each lane merges as its own refresh completes.

  -> after: one spec per claim commit; empty or multi-item input refuses before the lock and any write; historical multi-item commits are neither split nor re-claimed; the rationale states the window trade -> not the same: cardinality narrows. Return:
  - The by-name dirty-path refusal and the lock file never being staged are dropped, though the bookkeeping commit is still in this row's traced symbols.
  - "each branch refresh remains independently restricted" does not state the old obligation (merge can be restricted to named branches, so each lane merges as its refresh completes). A reader cannot recover it.
  - The rationale's "the state the old refusal guarded against" now has no referent, because the detail no longer names the deleted safety-class refusal.
- [MEANING] LLR-207 Detail -> before: the full verdict-record contract:
  - the identity fold;
  - the Bar-Green line's grammar and verifier;
  - the tests digest;
  - the one attestation producer, and the attest route's refusals;
  - the read-only walk and the two disposable classes, with the mechanical close's move-pairing rules;
  - scope, the gating span, the logged-round phase join, the filing check, the owed phases, the round count, and the trailer grammar.

  The batch clause was the shared multi-row ordering. -> after: seven sentences: one identity; verified attestations; a one-row mechanical close; cardinality refusing empty and multi-row closes; a walk; and evidence "bound to the governing identity, declared phase span and admissible scope" -> not the same: the batch clause changes and nearly every other obligation goes. The 9e1116b text had kept them; the W14 reconcile removed them. Return: restore the 9e1116b detail and replace only its ordering sentence and the empty-close explanation (REVIEW-A 004's MINOR). The row's traced symbols list some thirty functions whose contracts the new text no longer states.
- [MEANING] TC-144 Method -> before: the dispatch-loop suite on real repositories with the real bar. A spine batch is one commit; a needs-human handback; the refresh runs as its own subprocess. A red refresh quarantines a merges-nothing branch once and stops the run for a done-asserting one. An attended gate drains and exits 0 with the approvals banner. The gap census reaches the intake mint in one bookkeeping commit, deduped on the next idle pass, with rung-2 cards counted off the shared pending read. Pause, dirty-trunk, stall and crash-resume keep their contracts at lanes=1 -> after: one item per spine claim; a one-item parked resume, with non-single refused before mutation or launch -> not the same: cardinality narrows. Return:
  - The cell holds U+FFFD ("the exclusive lane�s return").
  - "a red refresh quarantines and stops the run" merges two different outcomes into one, both wrongly stated.
  - "exits 0" is dropped.
  - The census's one-commit and dedupe assertions and the rung-2 count are dropped.
  - "at lanes=1" and "with the real bar" are dropped.
- [MEANING] TC-145 Method -> before: the claim suite. The safety-class arm is red-then-green; the lock refusal names the lock; the claim commits through the shared bookkeeping helper and refuses by name a dirty path it must write. The pre-existing claim contracts are kept, and the scratch-worktree isolation arms are stated one by one: planned over HEAD, concurrent owner drift refused and preserved, out-of-scope generator input not shaping the commit, cleanup on every exit, and a compare-and-swap install whose refusal restores -> after: one-item claims; empty and multi-item input refuse; historical records are untouched; and "The abandoned-claim re-cut, relink, minted-id, bookkeeping audit and scratch-worktree isolation arms retain their stated assertions", keeping only drift and cleanup -> not the same: a pointer replaces the named arms. Return:
  - The by-name dirty-path refusal is dropped.
  - Planned-over-HEAD, the out-of-scope generator input, and the compare-and-swap install with its restore are dropped (REVIEW-B 003's second MAJOR).

**What the act needs.**
- The released rung lets the later act turn re-attest SR-144, SR-148, SR-156 and TC-146, and re-anchor LLR-058 as CLARITY.
- The eighteen returned rows are not re-anchored.
- No row here is on a held rung, so nothing waits on the owner.

**Parent-first.** The three SRs are blessed while their LLR and TC children are returned; that is the parent-first order. TC-146 is blessed while its parent LLR-152 is returned, and LLR-152's only defect is the corrupted character. If the act's parent-first rule refuses a child approved ahead of its parent, the act should hold TC-146 until LLR-152 re-sits. I judge its text ready either way.

### Dispositions (draft, for WI-977's own spec: returns answered in the lane before it re-sits)

These are Done-when gaps on this row ("The 23 rows above carry their target meaning"), so they are answered in this lane, not deferred to a successor:

- Re-author LLR-061, LLR-144, LLR-149, LLR-150, LLR-151, LLR-161 and LLR-207 from their 9e1116b-or-anchor text, replacing only the batch clause as the spec directs. Keep every other obligation in capability voice, with no "retain"/"existing"/"stated" pointer. Each row line above names the obligations to restore.
- Re-author LLR-123 and TC-058 with the scheduling views named or described by role, not "declared".
- Re-author TC-061, TC-138, TC-143, TC-144, TC-145, TC-154, TC-156 and TC-205 so each arm's assertion is stated. TC-205 goes back to its 9e1116b text with only the batch-shape clause replaced.
- Fix the four U+FFFD characters (LLR-061, LLR-150 and LLR-152 Detail, TC-144 Method), and check the registries hold no other non-ASCII replacement byte.
- Correct LLR-161's "refuses loudly" to what the sweep does: it says so loudly and mints nothing.
- Add SR-148's rationale sentence the spec names. It is not normative and does not hold this verdict.

VERDICT: MEANING rows=23

SITTING: JUDGED kinds=amendment
