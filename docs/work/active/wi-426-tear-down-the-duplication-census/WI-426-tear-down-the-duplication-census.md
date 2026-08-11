+++
id = "WI-426"
title = "Tear down the duplication census (repo-lock D-7, owner-ruled 2026-08-10) and execute its six-item consequence inventory, none of it optional. (1) check_dupes.py retires from the kit: the script, its bootstrap.py MAPPING row, the README kit-contents row, docs/stack.ini [step:dupes] and its [generated] row, and check.py's advisory-step references. (2) docs/dupes-allow is DELETED, not archived - a registry states what IS, and git is the history (the D-1/D-4 doctrine). (3) tests/test_check_dupes.py (18 tests) and tests/test_dupes_census_audit.py (12) are deleted with their subject. (4) the spine chain SR-039 -> LLR-036 -> TC-039 is SUPERSEDED, which under D-4 means the rows are DELETED from the three registries, ids retired against docs/id-watermark, the act recorded in log.md's Decisions - the log entry IS the forwarding pointer home for the retired ids. This is the FIRST REAL SUPERSESSION D-4 performs, so the row doubles as D-4's proving case. The seam rows IF-007/IF-027 go with the module they describe: an IF row citing a deleted SR is a trace.py --strict FINDING, not a warn. (5) F5 becomes unbounded again and the mitigation is NAMED rather than implied - test_rule_sync is the anti-drift tool of record, new F5 duplication of POLICY requires a behavioral pin there, plumbing duplication is accepted unbounded (which the evidence ledger shows was its de-facto state anyway). Record that where the census's role was documented. (6) ADOPTING.md notes the removal; an adopter's copy is their file after copy-in. THE HEDGE, recorded as an instruction: if a genuinely cheaper form of the census turns up mid-execution, bring it to the owner rather than building it."
workstream = "scripts"
specref = "docs/repo-lock.md"
buildtier = "strong"
safety_class = "spine"
+++

## Context

**This is faithful execution of a ruled decision, not a re-litigation.** The
owner ruled on the evidence ledger in [`repo-lock.md`](../../../repo-lock.md) §2
D-7: *"unless there is a better alternative it seems to be creating more
maintenance structure than it really solves, so it should probably just be torn
down."* The member-list improvement was on the table and was judged not worth
keeping the apparatus for.

**Why (the ledger, repo-lock §"Is the census earning its keep"):** one real
catch at the one-time triage and zero recorded since; structurally blind to both
real drift incidents this repo suffered (a diverged copy is no longer an
identical token block, so the tool goes silent exactly when duplication becomes
dangerous); 93% of its 253 census lines register accepted idioms; and it carried
its own defect chain, a 12-test meta-audit over its own prose, and three churn
cycles in one session.

**Why it lands HERE, in step 7.** repo-lock §5 step 7 is the batch that builds
the D-3/D-4 schema changes once, on the D-5 carrier. D-4 says supersession is
deletion; nothing in this repo had yet performed one. This row is the proving
case, which is why `safety_class = "spine"`: it deletes three ratified spine
rows and must leave the watermark's two rules intact — *the mark never
decreases*, and *no live id exceeds it*.

**The care point that makes this more than a `git rm`.** A deleted id is a join
key that other rows and documents cite. Every inbound reference must be
dispositioned before the delete, on the line the `check_doc_refs` docstring
already draws: a HISTORICAL document naming a retired id is accurate history and
keeps its citation (`docs/log.md`, `docs/archive/`, the reviews, the handoffs,
repo-lock itself); a LIVE typed join field pointing at a row that no longer
exists is a dangling pointer and must be re-grounded or cleared.
