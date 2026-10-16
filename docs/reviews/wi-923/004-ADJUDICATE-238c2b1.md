# WI-923 adjudication 004: amendment checkpoint at 238c2b167

I judged the three amended rows at `238c2b167`. Since the anchors, one LLR line moved (LLR-270's `detail`) and the TC-267 and TC-329 cells shown moved. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`).

**What I checked:**
- **The code matches LLR-270's new sentence.** `session_keep.dir_lock` and `_try_lock`: a create that meets an existing lock, or a `PermissionError` (access denied), reads as held and is retried until the wait ends. A lock still held at the deadline raises `StoreBusy` with the lock path, plus the access refusal when the last attempt met one. Any other create refusal propagates on the first attempt.
- **The four new evidence tests exist:**
  - TC-267: `test_a_lock_create_refused_once_as_access_denied_is_retried_and_taken`, `test_a_lock_create_refused_as_access_denied_past_the_wait_is_busy_and_named` and `test_any_other_lock_create_refusal_is_raised_at_once`.
  - TC-329: `test_a_first_call_whose_lock_create_is_refused_as_access_denied_runs_unretained`.
- **No evidence was removed.**

## amendment

- [MEANING] LLR-270 Detail -> every retained-session record write holds the store lock, an exclusively created file that goes stale after two minutes -> the same, plus: a create refused as access denied is read as the lock held and retried within the wait; a lock still held when the wait ends is refused as busy, naming the access refusal when that was the last; any other create refusal is raised after one attempt -> new failure handling. An implementation correct under the old text could raise on the first access-denied create, or report busy without naming the refusal, and fail the new one. **Blessed.**
  - Upward, SR-227's retained-session store, written whole by one holder at a time, needs a lock that does not misread a holder mid-delete (Windows' access-denied window) as a hard failure, and that names why it gave up.
  - It is closed: three readings of the create, each with a fixed outcome.
  - The sentence names no new carrier ("store_lock" was already in the approved cell).
  - Downward, TC-267 and TC-329 verify each reading.
- [MEANING] TC-267 Expected and Method -> verify LLR-270's store, reset, contention and blackout rules -> it adds: an access-denied lock create is retried and the lock taken; one refused that way through the wait is refused as busy, naming the lock and the refusal; any other refusal is raised after one attempt -> new verification obligations. **Blessed.** It is closed over LLR-270's three new readings, with one named test each. Its `Verifies` gains IF-273, the interface whose readings the docstring cites.
- [MEANING] TC-329 Method -> two concurrent first calls mint one session, plus the lease-expiry, late-call and launch-raise cases -> it adds: a second first call whose first store-lock create is refused as access denied, with no lease wait, runs unretained naming why, and the store keeps only the first call's lease -> a new case. **Blessed.** It drives the access-denied reading through the first-mint race this TC owns, so a refused create neither takes nor disturbs the first call's lease. Its named test exists.

VERDICT: MEANING rows=3

**Aftermath:** this session re-attests all three rows on the released rung, in their own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests LLR-270,TC-267,TC-329`

SITTING: JUDGED kinds=amendment
