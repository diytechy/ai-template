# ADJUDICATE — WI-702 — first approval at 1d84d77c

Independent adjudication of the eight spine rows WI-615 authored `Drafted`
that the `human_approval_through = "DevStg-Boundary"` dial releases to an
adjudication session: two labelled derived requirements (SR-223, SR-224),
three design rows (LLR-279, LLR-280, LLR-281) and three test cases (TC-289,
TC-290, TC-291). The one question: is each row ready to be APPROVED as it
stands, or does it go back with findings. `Approved` blesses the row's TEXT;
I ran the tests anyway, because a cell describing a test the suite does not
run, or a mechanism no module holds, is not blessable text.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chains of SR-112, SR-223 and SR-224 in full;
anchor `docs/archive/last_approved` copied at 464dc7ac). Every row was read
upward, sideways and downward; every evidence pointer resolved by file and
function name; every named code symbol located in its module. Disclosure: I
read WI-702's queued spec for its Context and the spine-authoring skill for
rule (c); nothing rests on any session's account of its own intent. HEAD
stayed at 1d84d77c throughout; the worktree was clean before this file was
written.

- [APPROVE] LLR-279 -> `skill_copies(skill_dir, name, spec)` names every file under a skill's directory paired with its destination at the same relative path under the agent's skills directory, so the unit a skill materializes as is its directory; `materialize_agent_layer` copies those pairs write-once for the chosen agents; `delivery_inventory` lists the same pairs as the skill's conditional deliveries -> SR-112 asks for a checked, generated fan-out of the one neutral source, and LLR-043's drift check compares the whole file set, so a SKILL.md-only first copy is drifted from its first write — the row's rationale says exactly that and names the alternative that lost (a directory walk per caller); every clause is true of `bootstrap.skill_copies` (an `rglob` over files, destinations under `spec["skills_dir"]`), `materialize_agent_layer` and `delivery_inventory` (which calls `skill_copies` per agent); Component CMP-009 is bootstrap's; no sibling (LLR-025, LLR-043) decides the unit -> ready.
- [APPROVE] TC-289 -> a planted one-skill kit: (a) THE COPY, `materialize_agent_layer` for one agent creating both files, the companion byte-identical, and `check_agent_sync` reporting no drift over one skill; (b) THE INVENTORY, `delivery_inventory` listing the companion as a physical source and both files as conditional deliveries for every agent skills directory -> two named pointers in `tests/test_skill_materialization.py`, resolving and green (fast batch); Tier Smoke is true, the module is not in `SLOW_MODULES`; the Expected honestly scopes to SR-112's acceptance for a multi-file skill; IF-035 exists -> ready.
- [RETURN] SR-223 -> where a repository vendors a guardrails payload for a model-name substring, the delivered loop content injects that payload in place of the default core into a guarded session whose model name contains that substring; acceptance: the longest matching substring wins, a model matching none gets the default core, an unguarded session gets nothing whatever is vendored, and the kit ships no payload and names no model -> a labelled DERIVED requirement under SN-026, judged by rule (c): (i) `Hat-Refs` UNATTENDED-OPS, a roster name whose `listens_for` names "a silent degrade", the failure the rationale argues (one core for every guarded model), and SN-026 carries the `unattended`/`loop` tags that reach that hat; (ii) the rationale argues the lens rather than the need's text and names the alternative that lost (a per-model key in the policy dial); (iii) fed back: the rationale states what SN-026's acceptance could name, carried to the owner below. Sideways, no other SR decides what a guarded session is told; downward, LLR-280 decomposes the selector and TC-290 drives the selector and the session both ways -> not ready as it stands (second sitting, ruling 38): the last acceptance clause, "the kit ships no payload and names no model", is an acceptance condition with no detector in the row's chain — TC-290 plants its payloads under a temporary directory and never inspects the kit tree — so the chain is not closed over the clauses (the skill's "the chain, passing, closed over the clauses"). The first sitting noted the gap and approved anyway; that was wrong, since an approved acceptance clause nothing checks is a claim the record carries forward. The derivation, the `Where` pattern, the one `shall` and the other three clauses stand; the remedy is an inventory assertion over `docs/guardrails/` in TC-290 (true of the tree today) or narrowing the clause, returned with TC-290.
- [APPROVE] LLR-280 -> `guardrails_core(root, model)` lists the vendored `core.<substring>.md` payloads beside `docs/guardrails/core.md`, orders their substrings longest first then by name, reads the first one `guardrails_apply` matches against the model, `core.md` when none matches or no model is named; the KIT CORE block is extracted as from the core; an unreadable chosen file returns None; whether a session is guarded stays `compose_session_prompt`'s call, made before the payload is read -> every clause is true of `agent_loop.guardrails_core` (the `(-len(sub), sub)` sort key, `next(... guardrails_apply(sub, model))`, the `OSError` -> None, `KIT_CORE_RE`) and `compose_session_prompt` tests `guardrails_apply(guardrails_policy, model)` two lines before calling `guardrails_core`; the rationale states one grammar for both decisions and why the file names carry the mapping; Component CMP-008 is agent_loop's -> ready.
- [RETURN] TC-290 -> a planted vendored set (a default core, a broad-substring payload, a narrower one wrapped in a KIT CORE block with text outside it): (a) THE SELECTOR returning the narrower block without the text outside it, the broader payload, the default core for neither and for no model; (b) THE SESSION under an all policy prepending the narrower payload and not the core, and under a policy excepting the model injecting nothing -> two named pointers in `tests/test_guardrails_payload.py`, resolving and green (fast batch); Tier Smoke is true; IF-253 exists -> not ready as it stands (second sitting): its Expected claims "Satisfies SR-223 AcceptanceCriteria" while neither arm tests the clause "the kit ships no payload and names no model"; a case whose Expected claims a whole acceptance must reach every clause of it. Remedy: a third arm asserting the kit tree's `docs/guardrails/` holds no `core.<substring>.md`, or an Expected that names the clause it does not cover; returned with SR-223.
- [RETURN] SR-224 -> if a skill's description is shorter than the declared description floor, then the kit's skills-index check fails naming that skill; acceptance: a description under the floor fails naming that skill and not one at the floor, one at the floor passes, the kit's shipped skills clear it -> a labelled DERIVED requirement under SN-005, judged by rule (c): (i) `Hat-Refs` FIRST-RUN-ADOPTER, a roster name whose `listens_for` names "a requirement satisfiable only with undocumented project knowledge", the failure the rationale argues (a skill that works only for someone who already knows it exists); (ii) the rationale argues the lens, calls the floor a lexical proxy and names the alternative that lost (a reviewer's judgement as the only guard); (iii) fed back: the rationale states what SN-005's acceptance could name, carried to the owner below. Sideways, SR-112 owns the fan-out and no other SR the description; downward, LLR-281 fixes the floor and TC-291 drives the refusal and the shipped set -> not ready as it stands (second sitting, ruling 38): rule (c)(i) asks that the derivation be recorded where something reads it, and the hats machinery reads a hat's `when` predicate against the need's tags; SN-005 carries `shell` alone while FIRST-RUN-ADOPTER fires on `scripts`, `templates` or `process`, so the recorded lens cannot reach the need it claims to derive from (`hats.py applicable` over SN-005's tags never lists it). A derivation the audit cannot see is the skill's "untagged need / blind hat" defect, and the first sitting wrongly approved past it. Fixing SN-005's tags is a needs-tier act for the owner; until it lands and the audit shows the hat reaching SN-005, the row is not an honest rule-(c) derived requirement. The `If ... then` pattern, the one `shall` and the acceptance stand.
- [APPROVE] LLR-281 -> `DESCRIPTION_FLOOR` is the shortest description `--check` accepts, 100 characters; `short_descriptions(rows)` returns the name and length of the rows under it; `refuse_short_descriptions(rows)`, called first by `--check`, prints one SHORT line per such skill naming it, its length and the floor, then exits 1; the regenerating path applies no floor -> every clause is true of `gen_skills_index.py` (the constant at 100, the comprehension, the `SHORT - <name>: description is N characters, under the 100-character floor` line to stderr, `sys.exit(1)`, and `main()` calling `refuse_short_descriptions(rows)` as the first statement under `if args.check` while the write path never calls it); the rationale states one declared number read by one function and why the check rather than the generator refuses; Component CMP-009 -> ready.
- [APPROVE] TC-291 -> (a) THE REFUSAL, a planted skills directory with one description under the floor and one exactly at it: after the index is written `--check` exits 1, names the short skill and the floor and not the skill at the floor; (b) THE SHIPPED SET, `short_descriptions` over the kit's own skills returning nothing -> two named pointers in `tests/test_skills_index.py`, resolving and green (fast batch); Tier Smoke is true; IF-254 exists -> ready.

## How the chain and the anchor were read

- Upward: SR-112, SR-223 and SR-224 as the brief printed them; SN-005,
  SN-012 and SN-026 from the needs registry with their tags; the roster
  through `python scripts/hats.py list` for UNATTENDED-OPS and
  FIRST-RUN-ADOPTER. Sideways: LLR-025, LLR-043, TC-025 and TC-045 as
  approved siblings under SR-112. Downward: every evidence pointer resolved
  by test function; every code symbol located.
- Anchor: the record at 464dc7ac holds none of the eight rows, so nothing
  here is a re-attest; the act names the three registries.
- The flipped tree was driven through `trace.py --root . --strict` and
  `--strict-integrity`: no form or provenance finding on any of the eight;
  SR-223 and SR-224 are reported "unclassified" (no `DA-Refs`, no
  `Coincident`), an advisory today and a gate case at DevStg-Boundary, which
  is above this repository's derived stage (`docs/stage`: DevStg-LLReqs) and
  which the gate would ask of the Drafted rows too, so approval changes
  nothing there; surfaced below.

Bar I produced (not claimed), on this tree with `python -m pytest -q -n 4 -p
no:cacheprovider`: the fast batch (`tests/test_skill_materialization.py`,
`tests/test_guardrails_payload.py`, `tests/test_skills_index.py` among
fourteen modules): **448 passed, 1 skipped in 16.80s** (the skip is
`test_kitlib_secret_classes.py:214`, by design); `tests/test_skills_sync.py`
in the slow batch (eight modules): **372 passed, 1 skipped in 195.57s**. No
failures, no errors.

## The two derived requirements: recommendation to the owner

Both pass rule (c) as written; the advice changes neither verdict.

- **SR-223: keep it derived; do not widen SN-026.** SN-026 is about which
  family and tier a job is routed to; what a guarded session is told is an
  operating posture the kit chose, and writing "a per-model posture" into the
  need's acceptance would fix a stakeholder outcome to one mechanism (payload
  injection by file name). The label does its job: a later reader sees this is
  the kit's choice under the unattended lens and can retire it without a needs
  change if the posture argument stops holding.
- **SR-224: widen SN-005 by reaching it, not by rewording it.** The obligation
  is real (an agent loads a skill by its description alone), but the deriving
  hat cannot see the need: SN-005 carries only the `shell` tag, and
  FIRST-RUN-ADOPTER fires on `scripts`, `templates` or `process`. Tagging
  SN-005 `process` (it is the playbook need) makes the derivation reachable by
  the hats audit without adding an instrument-shaped clause to the acceptance;
  I would leave the label on until then, and I would not add "skills'
  descriptions" to the need's text, which would name a carrier at the tier the
  skill's rule 1(e) keeps carrier-free.

## Dispositions

At the first sitting none were owed. At the second sitting (below) SR-223,
TC-290 and SR-224 are returned with every cell byte-exact; the follow-up is
drafted in `docs/work/queued/WI-702-adjudicate-llr-279-llr-280.md` under
`## Dispositions` as one fenced TOML block, and intake mints it at this row's
merge or the coordinator folds it into an open item.

## Non-blocking findings (surfaced, not acted on)

1. **SR-223 and SR-224 carry neither `DA-Refs` nor `Coincident`** and are
   reported unclassified; WI-655 filled that cell for seventy-nine other
   requirements (WI-695). One cell each, an amendment the next lane on these
   rows can take with the SN-005 tag.
2. **SR-223's "the kit ships no payload and names no model"** has no test of
   its own; a one-line assertion over `docs/guardrails/` in
   `tests/test_guardrails_payload.py` would close it.
3. **IF-253 (the guardrails payload seam) records no `Coincident` and no
   `BridgedBy`** (`trace.py` advisory), the interface-tier twin of finding 1.

## Second sitting, 2026-09-28 — after wave-5 ruling 38

Codex Sol's review of the first act (edaf0fa9) found SR-224 not yet an
honest rule-(c) derived requirement (its hat cannot reach SN-005) and TC-290
short of SR-223's last acceptance clause; the coordinator upheld both. The
first sitting had noticed each defect and approved past it, which the
brief's "fail toward RETURN" does not allow. The act was reverted (6498d2fa)
and the three rows are re-ruled above:

- SR-224: RETURN. The remedy is the owner's (tag SN-005 so
  FIRST-RUN-ADOPTER reaches it, then re-run the hats audit), after which the
  row is re-judged on an unchanged text.
- SR-223 and TC-290: RETURN together. One inventory assertion over
  `docs/guardrails/` closes the clause, or the clause is narrowed.
- LLR-279, LLR-280, LLR-281, TC-289 and TC-291 stay APPROVED on their own
  text: each states a mechanism or a test that is true of the tree and
  complete over what its own cell claims, and a design row may stand
  approved under a returned parent (LLR-210 under SR-220, batch B). Their
  chains read incomplete until the parents land, which the derived stage
  carries.
- The act is narrowed to the LLR and TC registries (ruling 38): the five
  approved rows are flipped and copied; SR-223 and SR-224 stay Drafted in an
  SR registry the act does not touch.

Counts after this sitting: 5 APPROVE (LLR-279, LLR-280, LLR-281, TC-289,
TC-291), 3 RETURN (SR-223, SR-224, TC-290).

OUTCOME: RETURN rows=8
