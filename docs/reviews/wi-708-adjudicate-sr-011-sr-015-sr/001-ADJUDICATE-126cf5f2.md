# ADJUDICATE — WI-708 — amendment at 126cf5f2

Independent adjudication of the thirteen approved system requirements WI-707
amended on merged trunk (batch C's returns, wave-5 rulings 44, 46 and 47).
Brief: the kit's amendment brief rendered for this row
(`adjudicate_brief.compose`, anchor `docs/archive/last_approved` copied at
464dc7ac for the SR registry). The brief shows EIGHT rows, because it diffs
live text against the anchor: the five rows whose waiver WI-707 removed
(SR-015, SR-024, SR-033, SR-129, SR-177) read byte-identical to the anchor in
every approved cell, and the `SN-Refs` re-points are traced cells, silent by
ruling (WI-388). All thirteen are ruled below so the row's `Adjudicates` list
is answered whole. I directed none of the amendments and read no session's
account of them; the arbitration file (rulings 38 to 47) was context for why,
never evidence. HEAD stayed at 126cf5f2; the worktree was clean before this
file was written.

The dial: `human_approval_through = "DevStg-Boundary"`, so the SR rung is
released and a MEANING verdict is re-attested by this session, in the one act
batch D takes (its own commit after this verdict).

THE TEST every waiver was held to is approved SR-193's own: a `coincident`
waiver "states why its own specification alone delivers its needs" — the
requirement's stated effect, with no party and no premise between it and the
outcome the cited need actually states. SR-193 also names the honest third
state: a requirement with neither a citation nor a waiver "is reported as
unclassified without failing the check". No row at HEAD carries both a
citation and a waiver.

Why a filled `Coincident` is MEANING rather than CLARITY (unchanged from the
WI-695 ruling): an empty cell claims nothing and the assumption gates read it
as unclassified; a filled cell is the recorded waiver those gates pass on, so
the same requirement text is admitted by a gate that refused it before — an
acceptance condition on the row moved. A `Rationale` re-parented from a need
the row no longer cites to the one it does, with the argument otherwise kept,
changes no obligation: a builder and a test act identically on both texts.

- [MEANING] SR-011 Coincident (and Rationale) -> skip an existing file on a re-run unless an explicit overwrite is requested, with no recorded waiver; rationale realizes SN-001 and SN-007 -> the same obligation, now carrying the waiver that a re-run leaving every existing file byte-unchanged IS SN-001's "a re-sync onto an existing repo never clobbers the repo's own files", delivered by the generator with no party between; rationale realizes SN-001 by that clause -> the waiver moved the row's classification (meaning); it is TRUE under SR-193's test — the clause it names is in SN-001's acceptance verbatim and the generator's own behaviour is that clause, nothing outside the system needed. The rationale change is clarity: the argument (edits lost, overwrite-with-backup rejected, merge is SR-036's) is unchanged and now names the need the row cites. BLESSED.
- [CLARITY] SR-015 Coincident -> (empty at the anchor: unclassified) -> (empty at HEAD: unclassified) -> no approved cell differs from the anchor; the waiver WI-695 wrote and WI-707 removed was never blessed, so nothing moved. The row stands approved and unclassified under SR-193's third state (its PB-reference invariant is one link of SN-002's verified chain, not that chain's outcome alone), pending the owner's vocabulary ruling (OI-97). Nothing to re-attest.
- [CLARITY] SR-024 Coincident -> (empty at the anchor) -> (empty at HEAD) -> as SR-015: no approved cell differs from the anchor; approved and honestly unclassified (generated permutation cases serve SN-002's coverage jointly with the negative tests the rationale names). Nothing to re-attest.
- [MEANING] SR-031 Coincident (and Rationale) -> every enforcer reads the same value for a dial and the two reader grammars agree over the adversarial table, with no recorded waiver; rationale realizes SN-004 and SN-005 -> the same obligation, now carrying the waiver that every enforcer reading one value and the two delivered grammars agreeing over the adversarial table, decoy included, IS SN-028's "the two readings are pinned equal over a table of adversarial files", a property of the delivered code; rationale realizes SN-028 by that clause -> the waiver moved the classification (meaning); it is TRUE — SN-028's acceptance states that pinned equality in those words, and the row's own effect is the equality; the one-home surface and the double-declaration refusal are SR-137's and the waiver says so. Rationale change is clarity (the SR-137 partition and the ONE HOME argument are byte-kept). BLESSED.
- [CLARITY] SR-033 Coincident -> (empty at the anchor) -> (empty at HEAD) -> as SR-015; approved and honestly unclassified (the emitted checklist puts warn-tier budgets in front of a reader, a step of SN-004's gate that a human tick-off completes, so the row's effect alone is not the outcome). Nothing to re-attest.
- [MEANING] SR-040 Coincident (and Rationale) -> route each in-process session phase through its declared per-phase command template, fall back to the single declared command, surface the reviewer dial at run start, fail a broken map entry at preflight, with no recorded waiver; rationale realizes SN-006 -> the same obligation, now carrying the waiver that each phase routed through its own declared command, falling back to the single one, IS SN-026's per-job selection carried out — a review phase declared on another family's command runs on that family, the dial surfaced shows the choice, a broken entry is refused before iteration 1 — and that what the invoked runner then does is the routed session's own requirement; rationale realizes SN-026 by that clause -> the waiver moved the classification (meaning); it is TRUE against SN-026's stated outcome (work routed to a different family wherever that is configured — the routing is the coordinator's own act) and it scopes out, in words, the one thing outside the row (the runner's behaviour, DA-006's premise, cited by the rows that rely on it). Rationale change is clarity: the two-lenses answer on the retired tripwire is byte-kept and the opening names the cited need. BLESSED.
- [CLARITY] SR-111 Rationale -> record the kit commit a scaffold came from (unchanged Requirement and Acceptance); rationale "Realizes SN-007 — without a recorded origin an adopter cannot tell which kit version they are on ..." -> the same obligation; rationale "Contributes to SN-001's re-sync clause ... by supplying the kit base that re-sync diffs from — without a recorded origin ..." -> the obligation is identical: a builder writes the same stamp and a test reads the same cell. The re-parent is honest — the stamp is the baseline a never-clobbering re-sync diffs against, a prerequisite of SN-001's clause rather than the clause itself, which is exactly why the row carries no waiver and stays unclassified (ruling 47's reading, OI-97 for the vocabulary). The drifted cell is named in the act's `--reattests` so the SR registry can be copied; this verdict blesses its text.
- [MEANING] SR-112 Coincident -> per-agent skill copies are a checked, generated fan-out of one neutral source, with no recorded waiver -> the same obligation, now carrying the waiver that each copy generated from the one neutral source, a divergent copy detected and refreshed by one command, IS SN-005's "AI agents and humans work from the same playbook" for the skills — every agent loads the text the source holds — with the need's agent-neutral enforcement clause left to other rows -> the waiver moved the classification (meaning); it is TRUE: the sameness is the generator's and its check's own effect, and the waiver names the half of SN-005 it does not carry. The `SN-Refs` re-point (SN-012 -> SN-005) is a traced cell, silent by ruling. BLESSED.
- [CLARITY] SR-129 Coincident -> (empty at the anchor) -> (empty at HEAD) -> as SR-015: no approved cell differs from the anchor. The `SN-Refs` re-point (SN-002;SN-012 -> SN-025) is a traced cell, silent by ruling; noted without judging it that SN-025 asks for next work derived from the tracked work-item registry, which is the registry this row's converter migrates. Approved and honestly unclassified. Nothing to re-attest.
- [MEANING] SR-147 Coincident -> hold every spine tier in one machine-parseable representation, reached by a migration proven cell-for-cell, with no recorded waiver -> the same obligation, now carrying the waiver that the one representation is what SN-002's strict check reads AND carries part of SN-002's stated outcome itself — a duplicate id is a decode error of the parse, a reference list is a typed array so no prose word reads as a reference, and the cell-for-cell migration means the chain verified is the one the registries held -> the waiver moved the classification (meaning); it is TRUE, and this is the one of the six that needed the re-wording ruling 44 asked for: SN-002's acceptance says "a malformed/duplicate id fails at any stage", and the representation's parse is that failure at the earliest stage, the row's own effect and nobody else's. The rest of SN-002 (zero orphans) is the checker's, and the waiver does not claim it. The `SN-Refs` re-point (drops SN-012) is traced. BLESSED.
- [MEANING] SR-149 Coincident (and Rationale) -> report every retired process tag in a live authored surface, carve-outs for history, generated and attestation-quoting surfaces, warn by default and fail under --strict, with no recorded waiver; rationale realizes SN-004 and SN-010 -> the same obligation, now carrying the waiver that a retired tag surviving in a live surface is a second, contradictory definition of a process word and that reporting each one, carve-outs kept, IS SN-010's "trust the documentation: navigable and honest" held by the harness rather than by attention; rationale realizes SN-010 by that clause -> the waiver moved the classification (meaning); it is TRUE against SN-010's stated outcome, the honesty half, and it is the check's own verdict. Rationale change is clarity: the measured-regeneration argument and the carve-out argument are byte-kept. BLESSED.
- [CLARITY] SR-174 Rationale -> allocate work-item identity once and never re-issue it (unchanged Requirement and Acceptance); rationale ends "Realizes SN-008 and SN-025." -> the same obligation; rationale ends "Contributes to SN-025 (the ready frontier ordered deterministically, so two readers of the same registry dispatch the same work) by supplying a work-item identity that names one record for every reader, before and after a deletion." -> the obligation is identical: same allocator, same non-reuse test. The re-parent is honest and argued in the row's own words (an identity that names one record for every reader is what makes "two readers dispatch the same work" mean one thing), a contribution rather than the outcome, so the row stays unclassified. The drifted cell is named in the act's `--reattests`; this verdict blesses its text.
- [CLARITY] SR-177 Coincident -> (empty at the anchor) -> (empty at HEAD) -> as SR-015: no approved cell differs from the anchor. Approved and honestly unclassified (the utilisation report is SN-027's measurement, read by the team; its rationale already says the aggregation is the row's stated build gap). Nothing to re-attest.

## The carried rulings, confirmed by git

Batch C judged three sets of SR rows but its act copied the LLR and TC
registries only (ruling 38), so each is relied on here only after confirming
that every cell it judged is byte-identical at HEAD to what it judged at
1d84d77c. The 66 blessed rows are the 79 `- [MEANING] SR-nnn Coincident`
lines of `docs/reviews/wi-695-adjudicate-sr-006-sr-007-sr/001-ADJUDICATE-1d84d77c.md`
minus the thirteen that verdict withheld (this row's `Adjudicates` list).
The comparison parsed the registry at both commits and diffed EVERY cell of
each row (not the approved half only):

```
$ python - <<'EOF'   # in C:\Projects\ai-template-wt\batch-d, HEAD = 126cf5f2
import tomllib, subprocess, re
def load(rev):
    t = subprocess.run(['git','show',f'{rev}:docs/requirements/system-requirements.toml'],capture_output=True).stdout.decode('utf-8')
    return tomllib.loads(t)['requirement']
head, c = load('HEAD'), load('1d84d77c')
verdict = open('docs/reviews/wi-695-adjudicate-sr-006-sr-007-sr/001-ADJUDICATE-1d84d77c.md', encoding='utf-8').read()
withheld = "SR-011 SR-015 SR-024 SR-031 SR-033 SR-040 SR-111 SR-112 SR-129 SR-147 SR-149 SR-174 SR-177".split()
blessed = [r for r in re.findall(r'^- \[MEANING\] (SR-\d+) Coincident', verdict, re.M) if r not in withheld]
print('blessed count:', len(blessed))
moved = []
for rid in blessed + ['SR-178', 'SR-220']:
    a, b = c[rid], head[rid]
    diff = [k for k in set(a) | set(b) if a.get(k) != b.get(k)]
    if diff: moved.append((rid, diff))
print('MOVED since 1d84d77c:', moved)
EOF
blessed count: 66
MOVED since 1d84d77c: []
```

- The 66 WI-695 waivers (SR-006, SR-007, SR-009, SR-022, SR-027, SR-035,
  SR-043, SR-049, SR-070, SR-113, SR-137, SR-144, SR-146, SR-150, SR-157,
  SR-158, SR-159, SR-161, SR-162, SR-164, SR-165, SR-166, SR-167, SR-168,
  SR-169, SR-173, SR-175, SR-176, SR-180, SR-181, SR-182, SR-183, SR-185,
  SR-186, SR-187, SR-188, SR-189, SR-190, SR-191, SR-192, SR-193, SR-194,
  SR-195, SR-196, SR-197, SR-198, SR-199, SR-200, SR-201, SR-202, SR-203,
  SR-204, SR-205, SR-206, SR-207, SR-208, SR-210, SR-211, SR-212, SR-213,
  SR-214, SR-215, SR-217, SR-218, SR-219, SR-221): every cell byte-identical
  to 1d84d77c. The BLESSED ruling is relied on; they are named in the act's
  `--reattests`.
- SR-178, blessed MEANING in `docs/reviews/wi-693-adjudicate-llr-158-llr-173/001-ADJUDICATE-1d84d77c.md`
  (Requirement, Rationale and Acceptance re-worded when the need tier gained
  its status cell): every cell byte-identical to 1d84d77c. Relied on; named in
  `--reattests`.
- SR-220, APPROVED in `docs/reviews/wi-683-adjudicate-llr-264-llr-265/001-ADJUDICATE-1d84d77c.md`
  and `docs/reviews/wi-696-adjudicate-sr-220-tc-279-s/001-ADJUDICATE-1d84d77c.md`
  but never flipped (the act did not copy the SR registry): every cell
  byte-identical to 1d84d77c, `Status` still `Drafted`. The APPROVE is relied
  on; this batch's act flips it to `Approved` and the SR copy carries it.

## What the act carries for this row

Re-attested (drifted approved text this verdict blesses): SR-011, SR-031,
SR-040, SR-111, SR-112, SR-147, SR-149, SR-174 — eight rows. Not re-attested
because not drifted: SR-015, SR-024, SR-033, SR-129, SR-177. Withheld: none.
No `## Dispositions` draft is owed. Nothing here edits a registry cell.

The six re-worded waivers were also driven through `trace.py --root . --strict`
on the flipped tree: rc 1, carrying only the thirteen "reads Status=Approved
but its copy reads Drafted / is ABSENT" approval-record findings the act's
copy clears; the assumption-gate arms report no row carrying both a citation
and a waiver, no waiver-form finding on any of the six, and the seven
unclassified rows as the warn-only advisory SR-193 specifies.

## Second sitting (2026-09-28): routed pointers

Wave-5 ruling 49 (Codex Sol's two blockers on 86aa7b0f, both upheld):
`SN-Refs` and `Boundary-Refs` are ROUTED traced cells
(`intake.ROUTED_TRACED_CELLS`; `acceptance_record.py`'s §A5.1 table) — a
re-pointed parent or crossing can move scope, so an amendment adjudication
rules them, and the first sitting wrongly called them silent. Act seq 6
copied the SR registry over 81 such pointers nobody had ruled: WI-707's nine
`sn_refs` re-points and C2's 72 `boundary_refs` moves (WI-655). Each is
ruled here. The tests, from the ruling: for an `sn_refs` re-point, is the new
parent's stated outcome, in the need's own words, the one the requirement's
approved text serves, and does dropping the old parent lose an obligation;
for a `boundary_refs` move, is each listed crossing one the approved
requirement text (Requirement and Acceptance) actually names or acts across,
read against `docs/requirements/external.toml`'s crossings: B-01 governed
writes admitted through the hook floor; B-05 THE TEMPLATE, the packaged
deliverable; B-09 what the operator reads — the spine, the generated views,
the derived stage and the console reports; B-10 the loop invoking a model
runner (brief out; output, exit code, commits and the runner's limits back);
B-02, B-04, B-11 the authority, in-session verdict and hosted-CI crossings.
The population was computed by parsing the SR registry at 464dc7ac (the SR
copy's last write, before C2 and before WI-707) and at HEAD and diffing the
two cells row by row: 9 `sn_refs` rows and 72 `boundary_refs` rows, four in
both sets, 81 pointer changes in all. Where a row's crossing set was itself
set by arbitration (SR-146, SR-156, SR-170, SR-215 at ruling 27; SR-174 at
ruling 32) it is still read here against the text, not carried.

The C2 rule, stated in WI-655's Deliverable and bounded by rulings 27 and
32, is the reading of the frame applied below: a requirement on what the
delivered harness or loop DOES at run time acts across the operation
crossings its effect lands on — B-09 where a person reads the report, view,
verdict or exit code; B-10 where a model runner is invoked; B-01 where
governed state is written — and keeps B-05 only where its text constrains the
package's own content (a shipped file, a shipped scaffold).

### The nine `sn_refs` re-points

- HOLDS SR-011 `SN-Refs` SN-001;SN-007 -> SN-001: SN-001's acceptance says "a re-sync onto an existing repo never clobbers the repo's own files", which is the row's skip-existing-unless-overwrite obligation in the need's words. SN-007 (the kit's maintainers hold it to its own standard through every change) states nothing an idempotent scaffold delivers; dropping it loses no obligation.
- HOLDS SR-031 `SN-Refs` SN-004;SN-005 -> SN-028: SN-028's acceptance says "two grammars read the file ... the two readings are pinned equal over a table of adversarial files", the row's acceptance in the need's words. SN-004 (gates pass on their mechanical bar) and SN-005 (one definition of passing, agent-neutral by hooks and CI) are served by the gate and CI rows (SR-006, SR-151, SR-152); the readers-agree property was parented there only because SN-028 did not yet exist. Nothing lost.
- HOLDS SR-040 `SN-Refs` SN-006 -> SN-026: SN-026's acceptance says "the coordinator resolves a row per in-process phase and tier ... logs every selection before launch"; routing each phase through its declared command template, with the reviewer dial surfaced at run start, is that per-phase selection. SN-006's preflight clause ("a preflight refuses a broken footing") is SR-027's home; the row's broken-map-entry arm stays in its own acceptance whatever its parent, so dropping SN-006 loses no obligation.
- HOLDS SR-111 `SN-Refs` SN-001;SN-007 -> SN-001: the kit-version stamp is the base SN-001's never-clobbering re-sync diffs from, which the rationale now argues in those words; the row contributes to that clause rather than delivering it, which is why it carries no waiver. SN-007 says nothing a scaffold's stamp delivers. Nothing lost.
- HOLDS SR-112 `SN-Refs` SN-012 -> SN-005: SN-005's acceptance says "per-agent configs only mirror the floor, never replace it" and the need asks that agents and humans work from the same playbook; a checked, generated fan-out of one neutral skill source is exactly a per-agent copy that mirrors and cannot diverge. SN-012 (small changes stay cheap; opt-in layers cost nothing) was the strained reading ruling 38 flagged — the row makes no cost claim. Nothing lost.
- HOLDS SR-129 `SN-Refs` SN-002;SN-012 -> SN-025: SN-025's acceptance says the next work "derives ... from the tracked WI DAG plus Git alone"; the work-item registry is that tracked state, and a cell-exact migration that refuses to convert while a claim is in flight is what keeps the DAG the dispatcher reads intact across a representation change — a contribution, which is why the row is unclassified. SN-002 names the SN->SR->LLR->TC spine, which the work-item registry is not, and SN-012 is a cost claim the row never made; dropping both loses no obligation.
- HOLDS SR-147 `SN-Refs` SN-002;SN-012 -> SN-002: SN-002 asks that the chain be mechanically verified with a malformed or duplicate id failing at any stage, which one machine-parseable carrier reached by a proven migration serves (the waiver, blessed above, argues it). SN-012's right-sizing is not what the row's rationale argues — its cost figures are about the kit's own reading code, not an adopter's opt-in layers. Nothing lost.
- HOLDS SR-149 `SN-Refs` SN-004;SN-010 -> SN-010: SN-010 asks for documentation a reader can "trust: navigable and honest"; a retired process tag reported in a live authored surface is that honesty held by the harness. SN-004's acceptance is a harness run enforcing a gate's steps, which a vocabulary check is not; the old link reached SN-004 only as the ladder vocabulary's home. Nothing lost.
- HOLDS SR-174 `SN-Refs` SN-008;SN-025 -> SN-025: SN-025's acceptance says "two readers of the same registry dispatch the same work", which an identity allocated once and never re-issued underwrites (the rationale argues it in those words). SN-008 is about a pass verdict hiding no skipped check; id re-use hides no check. Nothing lost.

### The 72 `boundary_refs` moves

- HOLDS SR-006 B-05 -> B-09: the harness's gate verdict, the SKIP(missing) report and the stated trunk-lane skip reason are console reports the operator reads.
- HOLDS SR-007 B-05 -> B-09: a loud nonzero failure on a malformed profile, and each step's resolved command, are the harness's reported verdict.
- HOLDS SR-015 B-05 -> B-09: the observable is the finding on an unresolvable Refs, a console report; the registry rows are the adopter's data, not package content.
- HOLDS SR-022 B-05 -> B-09: a drifted vendored copy reported as a finding.
- HOLDS SR-024 B-05 -> B-09: the expanded case set is generated output the author reads.
- HOLDS SR-026 B-05 -> B-10: a worker resuming from its claimed assignment and its committed trailer evidence is the brief-out / commits-back exchange with the runner, and "never blocking on a prompt" is the property of that exchange; the generated status surface is excluded as a session input, the same crossing named negatively.
- HOLDS SR-027 B-05 -> B-09: a typed nonzero exit at preflight is the verdict the operator reads.
- HOLDS SR-028 B-05 -> B-09, B-10: the typed outcome code and the all-ERROR stall report are read by the operator (B-09); the agent-CLI error it classifies arrives as the runner's exit and output (B-10).
- HOLDS SR-033 B-05 -> B-09: the emitted release checklist is a generated surface a person reads.
- HOLDS SR-040 B-05 -> B-09, B-10: each phase invoked through its command template is the runner invocation (B-10); the reviewer dial surfaced at run start and the preflight refusal are console reports (B-09).
- HOLDS SR-049 B-05 -> B-09: B-09 names "the derived stage" by name.
- HOLDS SR-052 B-05 -> B-09: the produced state view, read and operated by the reviewer.
- HOLDS SR-053 B-05 -> B-09: the produced state view.
- HOLDS SR-054 B-05 -> B-09: the produced state view.
- HOLDS SR-070 B-05 -> B-09: every artifact the generator set produces is a generated view; its freshness contract is a reported verdict.
- HOLDS SR-129 B-05 -> B-01, B-09: converting the work-item registry between representations rewrites governed state (B-01); the verification pass's exit and its refusals naming the row are reports (B-09).
- HOLDS SR-144 B-05 -> B-01, B-09: closing a lane into a terminal state with an immutable per-close report writes governed records that merge like any branch (B-01); a spec with no report being LOUD and a refused second close are reports (B-09).
- HOLDS SR-146 B-05 -> B-05, B-10: "a shipped, reviewable file" and the shipped catalogue are package content (B-05 kept, ruling 27); each session recording the template it launched with is the brief-out exchange (B-10).
- HOLDS SR-148 B-05 -> B-05, B-09, B-10: "no hand-curated next-work or run-phase pointer surface shipped" and "a fresh scaffold ships no next-wi/run-phase pointer" constrain package content (B-05 kept); `--explain`'s report, the recorded selection and the freshness-gated status surface are read (B-09); the status surface a session reads and the work it is handed cross to the runner (B-10).
- HOLDS SR-149 B-05 -> B-09: each retired tag reported with file, line and replacement, at its declared severity.
- HOLDS SR-150 B-05 -> B-09: each offending phrase reported naming the row.
- HOLDS SR-154 B-05 -> B-09, B-10: each review session obtained from a different family is a runner invocation (B-10); every selection logged before launch and the escalation through the approval level are read (B-09).
- HOLDS SR-155 B-05 -> B-01, B-09, B-10: the planner pair, critiques and arbitration are fresh sessions (B-10); the selected outcome committed atomically as registry-valid queued rows is a governed write (B-01); PAGE surfacing the round through the approval level is read (B-09).
- FAILS SR-156 B-05 -> B-01, B-10 (corrected at the third sitting, ruling 51): B-01 and B-10 are crossings the text acts across — every lane narrows to the integration branch through the serial seam that runs the bar on the composed tree (governed writes), and the lanes run sessions — but the list is INCOMPLETE: "stopping the queue loudly" is a report the operator reads, B-09, and ruling 27 requires every crossing the approved text names to be listed. Failed as incomplete before its completion (below).
- HOLDS SR-157 B-05 -> B-09: every rule violation reported with row-level attribution, gating the declared set.
- HOLDS SR-158 B-05 -> B-09: each documentation-drift class reported at its declared severity.
- HOLDS SR-159 B-05 -> B-09: each connectivity gap reported, warn-first with --strict gating.
- HOLDS SR-162 B-05 -> B-09: each unresolvable boundary reference failing the strict trace naming the row, and each advisory line.
- FAILS SR-164 B-05 -> B-09 (corrected at the third sitting, ruling 51): B-09 is a crossing the text acts across — a missing or out-of-vocabulary scope value reported by the harness naming the row — but the list is INCOMPLETE: the acceptance's "the SN carrier schema declares the scope field" and "every non-example row in the shipped registry ... carries a valid value" constrain the package's own content, B-05, and dropping it lost a crossing the approved text names. Failed as incomplete before its completion (below).
- HOLDS SR-167 B-05 -> B-09: the perf step exiting nonzero naming the breached row, the warn, and the per-row reported skip.
- HOLDS SR-168 B-05 -> B-09: the one state view a reviewer reads.
- HOLDS SR-169 B-05 -> B-09: the navigable component and interface graph.
- HOLDS SR-170 B-05 -> B-01, B-09: the compiled activity log and the generated project-state artifacts are written only from the serial merge step (B-01, governed writes; ruling 27) and are the surfaces a person reads (B-09).
- HOLDS SR-171 B-05 -> B-09, B-10: a declared transient provider limit is the runner's limit coming back (B-10); the wait surfaced so a throttled run is distinguishable from a wedged one is read (B-09).
- HOLDS SR-172 B-05 -> B-09, B-10: a session's declared progress, or its absence, is the runner's output (B-10); the stall reported as its own outcome is read (B-09).
- HOLDS SR-173 B-05 -> B-01, B-09: regenerating the shared derived artifacts and committing no partial set is a governed write (B-01); the failure reported at the stopping point, and the artifacts themselves, are read (B-09).
- HOLDS SR-174 B-05 -> B-01: allocating and permanently reserving a work-item identity is a trunk-side registry mint, a governed write (ruling 32); the row states no report.
- HOLDS SR-175 B-05 -> B-10: what the loop composes and dispatches to an external model runner, under a declared inclusion rule, is the brief-out half of B-10.
- FAILS SR-176 B-05 -> B-09 (corrected at the third sitting, ruling 51): B-09 is a crossing the text acts across — the durable record of a finding is what a reader of the repository's records meets — but the list is INCOMPLETE: "any tracked artifact after the run that caught it" and the transcript's redaction seam are a durable record written into governed state, B-01. Failed as incomplete before its completion (below).
- HOLDS SR-177 B-05 -> B-09: the per-run utilisation report, informational, read by the team.
- HOLDS SR-180 B-05 -> B-09: an undischarged design row reported, gating at the declared release bar.
- HOLDS SR-181 B-05 -> B-09: the phase-tag finding naming the row and the cause.
- HOLDS SR-182 B-05 -> B-09: the duplicated-body count reported against its stamped baseline, warn-only.
- HOLDS SR-183 B-05 -> B-09: each over-threshold function reported, gated only where the repo opts in.
- HOLDS SR-187 B-05 -> B-09: a crossing declaring no system reported.
- HOLDS SR-188 B-05 -> B-09: the unreached need reported naming the need and its stakeholder.
- HOLDS SR-189 B-05 -> B-09: an undeclared stakeholder failing the check naming the row; a need naming none reported.
- HOLDS SR-190 B-05 -> B-09: an unresolvable source pointer failing the check naming the need.
- HOLDS SR-193 B-05 -> B-09: each unclassified requirement reported; an undeclared assumption failing the check.
- HOLDS SR-194 B-05 -> B-09: each requirement declaring no form reported.
- HOLDS SR-195 B-05 -> B-09: each unreached need and idle landing reported naming the assumption.
- HOLDS SR-196 B-05 -> B-09: an uncited or unfalsifiable assumption reported.
- HOLDS SR-197 B-05 -> B-09: an assumption-only test case accepted, or an undeclared reference failing, in the harness's verdict; evidence counted apart wherever evidence is counted, which is a reported view.
- HOLDS SR-198 B-05 -> B-09: an observation test case's omission reported and a malformed declaration refused, naming it.
- HOLDS SR-200 B-05 -> B-09: the evidence level derived from current results is a derived value the views and reports show.
- HOLDS SR-201 B-05 -> B-09: the falsified assumption reported with every requirement and test case relying on it.
- HOLDS SR-202 B-05 -> B-09: the assumption read as unproven and reported naming the trigger.
- HOLDS SR-203 B-05 -> B-09: the approval brief is a generated view the approver reads.
- HOLDS SR-204 B-05 -> B-09: the derived stage, named by B-09.
- HOLDS SR-205 B-05 -> B-09: the boundary gate's failure naming the requirement, the assumption and the unmet condition.
- HOLDS SR-206 B-05 -> B-09: the release gate's failure naming the assumption and what is missing.
- HOLDS SR-211 B-05 -> B-09: each unbridged boundary interface reported; an undeclared assumption failing the check.
- HOLDS SR-212 B-05 -> B-09: the boundary and architecture gates' failures naming the requirement and the crossing or interface.
- HOLDS SR-213 B-05 -> B-09: an undeclared stakeholder on a perspective failing the check naming both.
- HOLDS SR-214 B-05 -> B-09: an undeclared perspective failing the check naming the assumption and the perspective.
- HOLDS SR-215 B-05 -> B-01: filing one re-judge work item at a merge or release checkpoint is a registry mint, a governed write (ruling 27); the row runs no model and states no report of its own.
- HOLDS SR-216 B-05 -> B-09: every worsening reported together naming measure, part and size; the change under acceptance arrives through B-01 but the row's obligation is the report.
- HOLDS SR-217 B-05 -> B-09: each requirement implemented ahead of an approved test case reported from the committed history.
- HOLDS SR-218 B-05 -> B-09: the state view's per-need assumption listing.
- HOLDS SR-219 B-05 -> B-09: a requirement spanning both systems reported naming it and a crossing from each.
- FAILS SR-220 B-05 -> B-01, B-10 (corrected at the third sitting, ruling 51): B-01 and B-10 are crossings the text acts across — the judgement is a strong-tier session, and its outcome takes effect only as a recorded restructuring of governed state — but the list is INCOMPLETE: "each refusal naming that judgement" is a report the operator reads, B-09. Failed as incomplete before its completion (below).
- HOLDS SR-221 B-05 -> B-09: the listing of a module's linked test files, and the two distinct refusals, are console reports.

### Tally and consequence

81 pointers ruled: 77 HOLD, 4 FAIL (9 of 9 `sn_refs` hold; 68 of 72
`boundary_refs` hold, and SR-156, SR-164, SR-176 and SR-220 FAIL as
INCOMPLETE — corrected here from the HOLD this sitting first recorded, under
wave-5 ruling 51: ruling 27 requires each multi-valued cell to list every
crossing its approved text names, so a list that omits one the text names
fails, however sound the crossings it does list). No pointer moved scope in
the other direction: every new parent states, in the need's own words, the
outcome the requirement's approved text serves; every dropped parent loses
no obligation; every listed crossing is one the text names or acts across.
The consequence this sitting first drew — that act seq 6 (86aa7b0f) stood as
taken — was WRONG under ruling 49: a failed pointer means the act is
reverted in the lane; the third sitting below records the revert, the
completion of the four cells and the re-taken act.

Kit gap, for the owner (ruling 49 records it): the amendment brief renders
the attesting cells and not the routed pointer cells, so an adjudicator can
bless a row without seeing its routed re-points — WI-695's and this row's
first sittings both did.

## Third sitting (2026-09-28): the four completed cells

Wave-5 ruling 51 (Codex Sol on 40e9ee16, upheld): the second sitting's four
"omission candidates" are FAILs — ruling 27 requires each `boundary_refs`
cell to list every crossing its approved text names — and the four lines
above are corrected to say so. Under ruling 49 the act is therefore reverted
in the lane (46cb87ea reverts 86aa7b0f: the 13 flips and the seq 6 copy are
undone, the SR copy back at 464dc7ac's bytes and the LLR/TC copies at
eecd656d's). The coordinator then completed the four cells in place
(9f38b6d3), each a traced pointer addition and nothing else; SR-220 is
`Drafted` there. Each completed cell is ruled here against the text, as the
second sitting's test asks: does the list NOW name every crossing the
approved text acts across, and is every listed crossing one it acts across.

- HOLDS SR-156 `Boundary-Refs` B-01;B-10 -> B-01;B-09;B-10: the serial seam's merges into the integration branch (B-01), the lanes' sessions (B-10), and "stopping the queue loudly" plus the drain to a merged stop under a declared pause, which the operator reads at the run surface (B-09). No other crossing is named: no shipped content, no authority, no hosted run.
- HOLDS SR-164 `Boundary-Refs` B-09 -> B-05;B-09: the harness's report naming the row (B-09), and the package's own content the acceptance constrains — the SN carrier schema declaring the field and the shipped registry's non-example rows carrying a valid value (B-05). No other crossing is named.
- HOLDS SR-176 `Boundary-Refs` B-09 -> B-01;B-09: the durable record a reader meets (B-09) and that same record as a tracked artifact written into governed state through the transcript's redaction seam (B-01). No other crossing is named; the unredacted raw stream stays in untracked scratch space, which crosses nothing.
- HOLDS SR-220 `Boundary-Refs` B-01;B-10 -> B-01;B-09;B-10: the judgement session (B-10), the recorded restructuring of the queue — terminal closes naming a successor, the successor's record (B-01) — and each refusal naming the judgement it waits on, read at the run surface (B-09). No other crossing is named.

Tally after the third sitting: 81 pointers, 81 HOLD as completed (9
`sn_refs`; 68 `boundary_refs` unchanged from the second sitting; 4
`boundary_refs` completed here), 0 outstanding. The same one act is re-taken
after this verdict: the same 13 flips, and the same snapshot with SR-156
added to `--reattests` beside the 75, which already held SR-164 and SR-176:
76 re-attested in all (corrected by the coordinator at integration, wave-5
ruling 52). Their live rows now differ from the SR copy in a routed pointer
this sitting has ruled, and the copy must carry the completed cells. SR-220 is flipped by the act itself.
No `## Dispositions` draft is owed.

VERDICT: MEANING rows=13
