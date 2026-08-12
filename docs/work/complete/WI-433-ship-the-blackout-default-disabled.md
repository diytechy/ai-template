+++
id = "WI-433"
title = "Ship the blackout window DISABLED to every adopter, keeping its SHAPE visible (owner ruling 2026-08-11, repo-lock 8.5, settling the tabled question `should the kit ship YOUR blackout window to every adopter?`). project-trajectory/process.toml.template ships `blackout = \"12:00-12:00\"` instead of `\"12:00-19:00\"` - `start == end` disables, verified mechanically across a full week of injected clocks - with a comment naming a window an adopter might want, so the FORM is still legible without the value being inherited. THE ASYMMETRY THE RULING TURNS ON: a shipped-empty dial an adopter forgets costs odd-hours activity; a shipped-populated dial an adopter does not notice costs seven hours a day of a loop that looks broken, and it already silently disabled ten of the kit's own tests for seven hours of every weekday (WI-428). WORDING CONSTRAINT, NON-NEGOTIABLE: the rationale offered was that Claude models see heavier usage 12:00-19:00 UTC. That is UNVALIDATED - there is no source for Anthropic's aggregate load and one must not be manufactured - so the shipped comment must read as the KIT AUTHOR'S OPERATING OBSERVATION, never as an asserted fact about the vendor. docs/process.toml is EXPLICITLY OUT OF SCOPE: this repo's own dial is the owner's and they are editing it themselves. THE PINNING TEST MOVES WITH THE DIAL AND MUST NOT GO VACUOUS: tests/test_blackout_isolation.py currently pins that the template ships \"12:00-19:00\" AND really blocks - WI-428 added the second half precisely so the guard could not decay into watching an empty dial. Re-aim it, never delete it: assert the template ships DISABLED, that the disabling is REAL (probe blackout_wake across a full week and assert no wait at any hour), that the shape still parses as a window so an adopter can see the form, and that a POPULATED window still blocks - so the machinery stays proven live rather than merely unexercised. Prove the re-aimed test can go red."
workstream = "unattended"
specref = ""
buildtier = "medium"
safety_class = "ordinary"
+++

## Deliverable

**DONE 2026-08-11.** `project-trajectory/process.toml.template` ships
`blackout = "12:00-12:00"`. `docs/process.toml` was **not touched** — this
repo's dial is still the owner's `"12:00-19:00"`.

### Disabled, but still shaped

`start == end` is the dial's own documented disable form, and it is written as a
window rather than as `""` so an adopter reads the format off the line they are
about to edit. Driven in a **real fresh scaffold** (`bootstrap.py --dest <tmp>`),
not only in the template: the scaffolded value parses to `(720, 720)` and
`blackout_wake` returns no wait at **0 of 504** probed clock times (7 days ×
24 hours × 3 minutes each); the same probe against a populated `12:00-19:00`
returns **105**.
<!-- fig: cmd="bootstrap.py --dest <tmp>; probe agent_common.blackout_wake over a 504-sample week" rev=6562239f -->

### The comment, and the claim it does not make

The offered window is framed as **one person's operating observation** and the
comment says outright that it is *"NOT a measurement of any vendor's load"*.
The 12:00–19:00 UTC hours are still offered — with the checkable part, the
timezone mapping (08:00–15:00 US Eastern, 05:00–12:00 US Pacific) — because they
are useful as a starting point; what is refused is asserting them as a fact
about Anthropic's aggregate load, for which the kit has no source. The comment
closes by pointing the adopter at their own contention as the thing worth
measuring.

**That constraint is mechanized, not merely honoured.**
`test_the_shipped_comment_offers_the_window_without_claiming_a_vendor_fact`
requires the phrase "the kit's author observes" and the explicit disclaimer, and
refuses the strings `Anthropic`, `Claude models see` and `usage peaks` in the
shipped `[policies]` block. It reds when the framing erodes.

### The pin re-aimed, and where its non-vacuity moved

`test_the_kit_still_ships_the_owners_live_window` was **one** test carrying two
claims: the template ships the owner's window, and that window really blocks.
The first claim is now false by ruling, and deleting the test would have left
the module guarding an empty dial — the exact vacuity trap WI-428's own docstring
names. It is split into four:

| test | what it holds |
|---|---|
| `..._ships_the_dial_disabled_and_the_disabling_is_real` | the shipped string **and** 0 waits across 504 injected clocks, **and** that it still parses as a window `(720, 720)` |
| `..._a_populated_window_still_blocks_so_the_machinery_is_proven_live` | `12:00-19:00` still blocks — 105 sampled waits, max 7 h, Mon–Fri only. **This is where the non-vacuity went.** |
| `..._this_repos_own_dial_is_deliberately_not_pinned_to_a_value` | the key exists and parses; the VALUE is the owner's, explicitly not pinned |
| `..._the_shipped_comment_offers_the_window_without_claiming_a_vendor_fact` | the wording constraint |

`test_every_loop_launching_module_that_bootstraps_disables_the_window` and the
autouse sweep are **kept, with their rationale rewritten**: they are now the
second line of defence, and they are the rule that holds if the shipped default
is ever repopulated — which is exactly the day nobody will be reading this file.

**Red-proof — four independent breaks, each caught:**

| break | failed |
|---|---|
| template regressed to `"12:00-19:00"` | 1 (`..._disabling_is_real`) |
| `blackout_wake`'s `start == end` rule neutered | 3 (`..._disabling_is_real` + both documented-disable-form params) |
| `blackout_wake`'s inside-window test forced `False` | 2 (`..._machinery_is_proven_live`, `..._guard_reds_on_a_planted_live_window`) |
| comment reworded to assert a vendor fact | 1 (`..._without_claiming_a_vendor_fact`) |

Each restored to **14 passed**.

### Everything that stated the old shipped default

`tests/conftest.py`'s WI-428 rationale block (which said the value "is CORRECT
and stays untouched"), `tests/test_bootstrap.py`'s dial assertion and its
folding-is-a-MOVE comment, `agent_loop.py`'s and `agent_common.py`'s docstring
sentences, `PROCESS_OPTIONS.md` "Unattended operation", and the root README's
dial row — which now distinguishes what a scaffold receives (disabled) from what
this repo runs (the owner's window).

**Left alone deliberately:** `project-trajectory/blackout.template` still ends
`12:00-19:00`. It is a RETIRED scaffold source that documents the *legacy*
one-word vocabulary for `--migrate-config`; its default line describes the home
that no longer ships, not today's.

## Context

### Why the guard is the delicate part

`WI-428` exists because the suite stopped running rather than failing: a
session-driving fixture seeded from this template inherited a LIVE window and
`agent_loop` correctly honoured it by sleeping, so "full bar green" was a
function of the wall clock. The fix was to the SUITE, and the guard it left
behind is anchored on the template still shipping a live window.

Flipping the template to a disabled window removes that anchor. The failure to
avoid is a guard that still passes because there is nothing left to guard —
which is the exact vacuity trap WI-428's own docstring names. So the re-aim has
to move the non-vacuity somewhere real: to an explicit probe that a POPULATED
window blocks (the machinery), and to the planted-window test that already
reds on demand.
