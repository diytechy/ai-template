# ADJUDICATE — WI-709 — first approval at 126cf5f2

Independent adjudication of the four spine rows batch C returned and WI-707
re-authored `Drafted` on merged trunk, which the `human_approval_through =
"DevStg-Boundary"` dial releases to an adjudication session: SR-223 (a
labelled derived requirement, its last clause pinned), TC-272 (split: the
in-memory readers), TC-297 (new: the readers over git history and the recorded
copy) and TC-290 (its method now driving SR-223's last clause). The one
question: is each row ready to be APPROVED as it stands, or does it go back
with findings. `Approved` blesses the row's TEXT; the harness answers whether
its tests pass, and I ran them anyway, because a cell describing a test the
suite does not run, or a mechanism no module holds, is not blessable text.

Brief: the kit's first-approval brief rendered for this row
(`adjudicate_brief.compose`, the chains of SR-147 and SR-223 in full; anchor
`docs/archive/last_approved` copied at 464dc7ac for the SR registry and
eecd656d for the TC registry). Every row was read upward (its parent and the
need the parent cites), sideways (the approved siblings in the brief) and
downward (every evidence pointer resolved by file and function name; every
named code symbol located in its module). Disclosure: I read WI-709's queued
spec for its Context and the spine-authoring skill for rule (c); the
arbitration file (rulings 38, 47) was context for why, never evidence. HEAD
stayed at 126cf5f2; the worktree was clean before this file was written.

- [APPROVE] SR-223 -> where a repository vendors a guardrails payload for a model-name substring, the delivered loop content injects that payload, in place of the default guardrails core, into a guarded session whose model name contains the substring; the acceptance fixes: the payload and not the core for a matching model, the longest substring winning among several, the default core for a model matching none, nothing for a session the policy leaves unguarded whatever is vendored, and the kit shipping no payload of its own so that with only the default core present every model receives the default core -> a labelled DERIVED requirement under SN-026, judged by the skill's rule (c): (i) recorded where something reads it — `Hat-Refs` UNATTENDED-OPS, a roster name whose `listens_for` ("a silent degrade ... a green that is green because nothing looked") names the failure this row prevents (one posture for every guarded model, drifting unwatched), and SN-026 carries the `unattended`/`loop` tags that reach that hat; (ii) the rationale argues the lens and says why SN-026's text (models selected per job and capability level) does not itself say what a session on a model is told, and names the alternative that lost (a per-model key in the policy dial: a model name in shared configuration rots as models turn over); (iii) fed back upward in the rationale's last sentence. Voice: the SR names no file — the vendoring rule lives at LLR-280's Detail and IF-253. EARS: a `Where` opening on a declared feature, one `shall`. The rationale carries no citation frame. Upward, SN-026 asks for selection per job; sideways, SR-040 routes the phase and SR-043 guards the spawn, neither deciding what a guarded session is handed; downward, LLR-280 (approved, act seq 5) holds the longest-first matcher in `agent_loop.guardrails_core` (read at HEAD: `core.?*.md` stems sorted `(-len, name)`, `guardrails_apply` as the matcher, `core.md` when none matches or no model is named, `KIT_CORE_RE` extraction, `None` on an unreadable file), and TC-290 now drives every acceptance clause including the last -> ready. No `Coincident` waiver and no `da_refs`: the row is honestly unclassified under SR-193's third state (ruling 47), which the SR rung's gate reports without failing.
- [APPROVE] TC-272 -> in memory, `spine_carrier.needs_from_text` under the TOML carrier yields no need from a comment-only text, from a text whose only table row sits in a stakeholder's description string, and from an empty text, while the markdown carrier reads that string text's row; an unparseable TOML text and a carrier the need tier lacks raise, `needs_or_refuse` refuses naming the file; the README floor (`check_docs._registry_needs`) and the approval view's need prose (`trace._sn_prose`) read no need from a TOML file declaring none, and the README floor refuses an unparseable one by name -> three named pointers in `tests/test_spine_carrier.py`, each resolving by function name and asserting exactly what the Method says (read at HEAD: `_COMMENT_ONLY_TOML`, `_TABLE_IN_A_STRING`, `""`, `_UNPARSEABLE`, the `.csv` carrier, `SystemExit` matching the file name); Verifies SR-147, LLR-277 (approved, act seq 5, whose Detail names these readers) and IF-112 (the `spine_carrier -> check_docs` call seam, `needs_or_refuse` in its data cell); Tier Smoke is honest — `test_spine_carrier` is not in `tests/conftest.py` `SLOW_MODULES`, and the case runs in memory with no git; Level Unit true; Expected states the condition (no reader chooses its carrier by guessing) not the instrument -> ready. The split from the old TC-272 is the right stopping boundary: the in-memory readers and the git-history reader are two verification purposes, and TC-297 carries the second.
- [APPROVE] TC-290 -> a planted vendored set under a temporary directory (default core, a broad-substring payload, a narrower payload wrapped in a KIT CORE block with text outside it): (a) the selector returns the narrower block without its outside text for a model containing both substrings, the broader payload for one containing only the broader, the default core for neither and for no model; (b) `compose_session_prompt` under an `all` policy prepends the narrower payload and not the core, and under a policy excepting that model guards nothing and injects no payload; (c) no physical kit source, no MAPPING, conditional or generated destination of the delivery inventory, and this repository's own guardrails directory, is a `core.<substring>.md` payload, and with only a default core present the selector returns it for every model the shipped roster template names, bare and with version -> three named pointers in `tests/test_guardrails_payload.py`, each read at HEAD and asserting exactly the Method's three arms — (c) is the arm ruling 38 found missing, and it is now driven over `bootstrap.delivery_inventory()`, `bootstrap.mapping_entries()`, `ROOT/docs/guardrails` and `agents.template.toml`'s roster; Expected restates SR-223's acceptance including the pinned last clause, and every clause of that acceptance has an arm; Verifies SR-223, LLR-280, IF-253 (exists: the `core.<substring>.md` file seam owned by `scripts/agent_loop`, tied to B-05); Tier Smoke honest — `test_guardrails_payload` is not in `SLOW_MODULES` and the module runs in-process on tmp_path (3 cases); Level Unit true -> ready.
- [APPROVE] TC-297 -> over real git repositories and a scaffold: the record's history reader (`baseline_snapshot._needs_at`) reads no need at a commit whose needs file is TOML declaring none, and refuses one at a commit whose needs file does not parse, naming the commit and the file; a scaffold whose needs file is markdown records its approved need at the seed, reports it drifted naming the cell once amended, refuses `intake.py snapshot --approves` until the need is named in `--reattests`, then copies it byte-exact and reports nothing owing -> two named pointers in `tests/test_snapshot_readers.py`, each resolving and asserting exactly the Method's two arms (read at HEAD: the `STK-01` description holding a table row, the unterminated `[need.SN-007]`, `re.escape(broken) + ".*stakeholder-needs"`; the `_MD_NEEDS` scaffold, `("SN-001", "DRIFTED", ["Need"])`, the refusal then the `--reattests SN-001` copy); `_needs_at` at HEAD reads through `spine_carrier.carriers` + `needs_or_refuse("<sha>:<path>", text)` as LLR-277's Detail says; Verifies SR-147 and LLR-277; Tier Full is honest for a case that commits to real repositories and drives a scaffold; Level Integration true; Expected names the condition -> ready.

## How the chain and the anchor were read

- Upward: SR-147 and SR-223 as the brief printed them and as the live file
  holds them; SN-002 and SN-026 from `docs/requirements/stakeholder-needs.toml`;
  the hats roster from `docs/requirements/hats.toml` for UNATTENDED-OPS
  (`applies_when`, `asks`, `listens_for`). Sideways: LLR-165, LLR-166, LLR-277,
  TC-159, TC-160 (SR-147's approved chain) and LLR-280 (SR-223's approved
  child). Downward: every evidence pointer of TC-272, TC-290 and TC-297
  resolved by file and test function and read; `guardrails_core`,
  `needs_from_text`, `needs_or_refuse`, `load_need_tier` and `_needs_at`
  located and read in their modules.
- Anchor: the SR copy at 464dc7ac and the TC copy at eecd656d hold none of the
  four rows as `Approved` (SR-223 at `Drafted`; TC-272 at `Drafted`; TC-290 at
  `Drafted`; TC-297 absent), so nothing here is a re-attest of this row's
  rows. The act names both registries.
- Smoke-tier check (batch D's standing rule): TC-272 and TC-290 are `Smoke`
  and neither cites a `SLOW_MODULES` module. TC-297 is `Full`.
- Method and Rationale cells state the standing system: no history, status or
  citation frame in any of the four rows.

## Bar I produced (not claimed)

On this tree, `python -m pytest -q -n 4 -p no:cacheprovider` over the six
modules batch D's rows cite (`tests/test_guardrails_payload.py`
`tests/test_decision_record.py` `tests/test_decision_record_merge.py`
`tests/test_spine_carrier.py` `tests/test_snapshot_readers.py`
`tests/test_traj_render_sweeps.py`): **166 passed in 51.26s**; collected per
module 3 / 89 / 16 / 25 / 20 / 13. No failures, no errors. The flipped tree
was driven through `trace.py --root . --strict` before the act; the findings
are recorded in the act's commit and the coordinator's report.

## The derived requirement: recommendation to the owner

SR-223 passes rule (c) as written, and the recommendation does not change
the verdict. Keep it derived; SN-026's acceptance could carry "a session on a
routed model receives the guardrails posture the repository vendors for that
model, or the default one", at which point the row reads as realized rather
than derived. Until the owner writes that sentence, the row says so itself.

OUTCOME: APPROVE rows=4
