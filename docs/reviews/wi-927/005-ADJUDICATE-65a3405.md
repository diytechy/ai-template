# WI-927 adjudication 005: amendment of LLR-322, TC-345 and LLR-300

I judged the three amended rows at `65a340522`. Since the anchor (`e45ed5a75`), the LLR and TC registries moved only in these rows. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**The scope:** the work item's Context records the owner's rulings.
- **D-011:** WI-834's command-level hook ownership is contrived, and is replaced by "checked by name; installed on first run when none are there; refuse when other hooks occupy the slot; no re-enable path".
- **D-019:** the first run is both the lease take and dev-setup's readiness check, and the install keeps asking consent.

**What I checked:**
- **Evidence:** all 33 of TC-345's cited tests exist, and TC-345 verifies LLR-322 and LLR-300 both, so the take's new gate is under test.
- **The "missing" report:** "reported missing" is dev-setup's `[missing]` readiness line, the vocabulary the shipped reader uses (`kitlib/guard_hooks.py` names a missing guard event the same way).

## amendment

- [MEANING+BLESS] LLR-322 Detail, Rationale and Title -> on consent, merge the guard hooks into the machine-local settings, bound to the floor interpreter, replacing only commands of the example's exact guard shape, preserving every other command and its group, dropping a group only when emptied; idempotent; a declined offer and a no-guard example change nothing -> the guard hooks' state is none, absent, on or occupied, each guard event checked by the guard's command name (a missing file or all events missing is absent, a parsed null is occupied):
  - **At absent:** dev-setup's offer and the lease take each install the example's groups only after a terminal yes, with the consent question shown before its answer is read, bound to the running interpreter and keeping every other key and event, and continue only when a re-read reads on.
  - **Without a terminal:** the take refuses and names the consent step; on Windows, a non-console character device is no terminal.
  - **At occupied:** every route writes nothing and names the file, events, commands and fix.
  - **On failure:** a failed or off-reading install refuses the take without recording a holder, and dev-setup reports it missing; a failed reader is missing, never none.
  - **No re-enable path exists.** The Rationale drops "preserves existing configuration", and the Title follows.

  -> the behaviour changed: the old command-level merge into shared groups is gone, an occupied slot is refused instead of merged, and the take becomes an install route. **Blessed.**
  - Upward, SR-032's green developer setup still holds: the readiness report names the state, and where the install is offered.
  - The owner ruled the command-shape ownership contrived. The new state machine is closed, four states plus a never-none failed read, and it fails closed: occupied writes nothing.
  - The consent and machine-local target the owner kept are kept, and no carrier is named.
- [MEANING+BLESS] TC-345 Expected and Method -> verify the consented merge (bound interpreter, guard-shape-only replacement keeping user commands and matchers, bare-python rebinding), idempotence, older Python on PATH, git-ignored file, decline and no-guard cases, and the repo's settings, example and readiness report -> verify the four states over the Trust shapes; the consented install at the dev-setup offer and the lease take (in process, through a pseudo-terminal and at a Windows console); the question shown before its answer; the no-terminal and occupied refusals; failed-install and failed-reader reporting; the no-guard, no-re-enable and older-Python cases; and the repo's settings, example and report -> the verification set was replaced. **Blessed.** It is closed over LLR-322's arms and LLR-300's take gate, and every cited test exists.
- [MEANING+BLESS] LLR-300 Detail -> the lease guard, claim admission, blackout hooks and compaction records -> it adds that, after identifying a session, the lease take reads the guard hooks' state and records no holder unless it reads none or on, or a terminal consent installs them and the re-read reads on; without a terminal at absent, or at occupied, it refuses naming the consent step or the hooks to move -> a new precondition on taking the lease. **Blessed.**
  - The lease holder is the session the guard's latch and blackout close-down instructions reach, and they reach it only through these hooks. So the take refusing to install a holder the hooks cannot reach serves both parents: SR-229's drain and SR-237's close-down.
  - It fails closed, it names its recovery, and TC-345 verifies it.
  - It states only the take's gate and leaves the state machine to LLR-322, so the decision has one home.
  - Every other clause is verbatim.

VERDICT: MEANING rows=3

**For the later act turn:** all three rows are marked `[MEANING+BLESS]` on a released rung, so the act turn re-attests LLR-322, TC-345 and LLR-300. No row is held, and no row is returned.

**On the coordinator's question about SR-229: reading (b).** SR-229's list is not exhaustive over the lease take, and SR-229 stays unchanged.
- **Where the clause sits:** "a subsequent session may take the freed lease" closes SR-229's hand-back sentence. It says the hand-back frees the lease so that it is takable, not held by the leaving holder. It does not enumerate the take's preconditions.
- **The take already has a refusal SR-229 never lists.** It refuses another holder, which lives in LLR-300 alone.
- **The hooks precondition is design detail beneath SR-229 and SR-237 as approved.** It is how the holder is kept reachable by the drain and close-down the SRs require, and a session that consents, or a repository whose example declares no guard hooks, can still take the freed lease.

**Two advisories, neither blocking:**
1. **"No re-enable path exists" (LLR-322)** states an absence without naming the act. The spec's meaning is that the deleted enable commands have no replacement, so the absent-state consent is the only install route. A later edit could say that outright.
2. **TC-345's tier** (not amended here) reads `Smoke`, while its evidence includes `test_coordinator_guard_e2e` and `test_run_devsetup`, both in `SLOW_MODULES`. By TC-205's rule it should read `Full`.

SITTING: JUDGED kinds=amendment
