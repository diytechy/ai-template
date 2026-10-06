Deferred open items: OI-98, OI-105, OI-106, OI-107

## 2026-10-06 — Wave-17 coordinator: WI-835 lands, adjudicated through its own entry point

At the owner's direction the coordinator ran WI-835's adjudications through the
entry point the lane built, `coordinator_adjudicate.py adjudicate`, and watched it
as a live trial. Roles as before: Claude Opus builds (kit-builder, medium), GPT
Terra (medium) authors spine rows, Codex 6.1 Sol (high) reviews, and the retained
Claude Opus adjudicator judges. Nothing else was claimed; `docs/work/pause` is
unchanged.

### The live run (acts 37 to 40)

All five adjudications ran on one retained session (`ce1fccc0…`, generation 1),
reaching 18% of a 1M window. The second call resumed the first, which is the
continuity WI-834 depends on. The first launch was refused (exit 2) because a
work item's first verdict names a review directory that does not exist yet.
After two calls the session read `draining` with "governing-inputs changed"
although nothing had changed: the governing hash was keyed on the call's own
brief-class template. Builder round 4 fixed both (`5ca5164d`). The verdict's
parent directories are created, and the identity covers every `retain_for`
class (owner-confirmed scope). A class switch no longer drains the session, but a
template edit or an override still does.

The verdicts: 001 returned LLR-305 and TC-321..TC-324, and 002 returned SR-227,
whose acceptance outran its Requirement. Terra's round 4 answered both: SR-231 (a
derived, dial-independent requirement) took the lane-only and current-verdict
boundary, and LLR-305's entry part became LLR-306. 003 re-attested SR-227 and
LLR-270. 004 approved LLR-305 and TC-322..TC-324 and returned SR-231, LLR-306 and
TC-321. Terra's round 6 answered those, and 005 approved all three. The owner
ruled that the adjudicators' `## Dispositions` follow-ups are answered in-lane,
so the spec records where each was answered and intake mints nothing.

### Review and the bar

Sol ran rounds 3 to 5. Round 4 found trunk-only generated artifacts committed on
the work branch; they were restored to claim-base bytes (`cddedd45`). It also
found that the coordinator recipe had not been edited; the coordinator edited it
outside the repository, as D-010 says. Round 5 claimed that the module-size
stamp is a trunk-only artifact. The coordinator disputed it with evidence: the
ratchet matches exactly, and `integrate.py` names `linecounts` as the one
hand-stamped kind that a lane carries with its reason. Sol withdrew it, giving
`3b5e0c65 SOUND`. The full suite at `3b5e0c65` (detached worktree, fixed
basetemp): 1 failed, 5282 passed, 13 skipped, in 627.6 s. The one failure was the
committed `docs/stage`, a trunk-only file this landing regenerates; after
the landing's regeneration it passes, and the smoke tier on trunk gives 2262
passed (42.9 s against the 60 s budget).

The hand landing took two commits. A single squash that also archived the spec
failed the ruling-sync step: D-007's overrule would land with no open work item
citing it. It also failed text-then-act, because the lane did not yet contain
trunk. So the lane was rebased onto `681e3280`, and only the generated
`open-items.html` conflicted (trunk's side taken). Trunk then took the squash
up to the commit before the close (`181ec900`, every hook step passing), and
then the close.

### Follow-ups (topics, unfiled)

- The first mint on a route writes no lease (`session_keep._hold` with no
  record), so two simultaneous first calls can both mint. This predates WI-835.
- PROCESS_OPTIONS.md and concurrency-restructure §5.3 say that stamps are never
  carried on work branches; the integrator's hand-stamped `linecounts` exception
  says that a lane carries them. The documentation should state the exception.
- Full-suite and review basetemps accumulate under `review-tmp`, because pytest
  keeps a literal `--basetemp`. `tmp_path_retention_policy = failed` and one dated
  run root per session would bound them. 137 stale directories (6.6 GB) were
  deleted this session.
