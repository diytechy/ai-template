# WI-996 dispute sitting 008 (28fb8e46): finding LAND

## LAND

**What I observed at the range.**
- `kitlib.red_mark.landing_refusal` has exactly one caller: the integrator's
  refresh (`project-trajectory/scripts/integrate.py:2845`). It reads the
  staged tree of the worktree it is given and refuses any file under the
  tests root that holds the declared mark.
- Nothing else reads the mark at landing. No step in `docs/stack.ini`, no
  hook under `project-trajectory/hooks` or `.githooks`, and no line in recipes
  §3 calls it.
- Recipes §3, this repository's landing route, squashes with
  `git merge --squash <lane>`, regenerates, and runs `run_menu.py smoke` on the
  staged squash. That is the commit bar, not a refresh.
- Recipes §8's partial close calls `handback.close_partial`, keeps or discards
  each lane commit by the coordinator's own lists, then says "land the lane",
  by that same route.

The finding's facts hold.

**Is it reachable under PROCESS.md §6?** Yes. The hand squash is not a
contrived ordering of tools. It is the supported way this repository lands
every coordinator lane, written down in the skill this lane itself edited.
The lane's own procedure text now makes every lane's tests-first commit carry
strict marks (coordinator-cycle SKILL.md Intent step 2). That text says the
code commit removes them and "a refresh refused for a mark ends in the code
commit or a quarantine". PROCESS.md §4's new sentence says a marked test is
"never landed".

On this route nothing makes that true. A mark that survives to the landing
lands on trunk, and its red test reads green under the smoke bar. Two ways it
survives are both on supported routes:
- a code commit that leaves one marked test unfixed. Agent-written content,
  which §6 names as the thing the gates exist to check; `attest` admits a mark
  its set names, and nothing requires the marks gone before landing;
- a §8 partial close that keeps the attested tests-first commit.

Neither needs a compromised host, a forbidden hand act or a hand-edited
record. What follows is a fail-open: a red test lands as a pass, the exact
failure SN-008 forbids and the reason the landing arm exists. It also has the
spec's own S1 cost: every later loop lane's refresh is refused for a file it
never touched.

**Why FIX and not something else.**
- **Not DISMISS:** the path is real, reachable and in scope.
- **Not SUCCESSOR:** it is convergence-class (a fail-open path), so the brief
  forbids it.
- **Not ESCALATE:** the remedy is small and sits inside the surface this lane
  already owns. The lane wrote the coordinator-cycle procedure text whose
  promise the route does not keep, and the landing check already exists as one
  function over a staged tree. Recipes §3 already runs named checks on the
  staged squash before the landing commit (`check_complexity`, `run_menu.py
  smoke`). One more step there, running `kitlib.red_mark.landing_refusal` on
  the staged squash and resetting the squash on a refusal, closes the gap on
  this route.
- **Not the one-landing row:** that row, filed and not built, would move
  coordinator landings onto the merge slot. It is the structural answer, but it
  is not this lane's, and waiting for it leaves the lane's own new text untrue
  on every landing until it lands.
- **Not the commit hook:** a bar step on every commit would be wrong, because
  marks are legitimately present on lane commits between the tests-first and
  code commits.

Severity stands at MAJOR: a fail-open on the supported landing route, reached
by ordinary agent error or a documented partial close.

RULING: LAND FIX the red-mark landing arm runs only inside the refresh, so this repository's supported hand landing (recipes §3, and §8's partial close) can land a strictly marked red test as green; add a recipes §3 step that runs kitlib.red_mark.landing_refusal on the staged squash before the landing commit and resets the squash on a refusal, and make the coordinator-cycle text's "a refresh refused for a mark" sentence cover that landing check too
