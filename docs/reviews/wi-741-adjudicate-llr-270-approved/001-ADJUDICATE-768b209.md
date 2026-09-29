# ADJUDICATE — WI-741 — amendment of LLR-270 at 768b209

Independent adjudication, spine-acts batch K. The question is whether
LLR-270's amendment changed meaning or only clarity. I read the brief
(`adjudicate_brief`, amendment form) in full, and I directed none of the
amendments judged here.

The anchor is `docs/archive/last_approved/docs/requirements/low-level-requirements.toml`,
copied 2026-09-29 at 7a6536f9. Two cells of LLR-270 differ from it:

- `Detail`, the one the brief routes;
- `CodeSymbol`, a trace pointer that now also lists `PlainAdapter.bounds_one_turn`.

Context, not authority:

- the lane that made the change (WI-740, `git show 3ecef627`) and its review
  (`docs/reviews/2026-09-28-wave6/sonnet-wi740.md`);
- the draft it answered (WI-737 `## Dispositions`) and that sitting's verdict.

- [MEANING] LLR-270 Detail -> before: with the dial and `keepwarm_minutes` on, the keep-warm pinged every active ANTHROPIC session idle `keepwarm_minutes` while lanes were out, whatever runner served its route. Its one-turn bound was stated as `one_turn`'s `--max-turns 1`, which only the claude adapter adds -> after: the same session is pinged only when its route's runner's adapter bounds a call to one turn (today claude's), and a route served through any other runner is never pinged -> not the same. The eligible set is narrower. A correct build of the old text pings an ANTHROPIC route served through opencode, and the new text forbids that ping, so the obligation moved. Every other clause of the cell is byte-identical.

Re-attestation: the LLR tier is released to the loop, so this sitting owes the
re-attestation, and I would bless the new text. My reasons:

- **The claim holds in the code at HEAD.**
  - `KeepWarmer.__init__` builds each registry row's argv the way `act` does
    (the same template, model and `KEEPWARM_PROMPT`), resolves the adapter
    through `adapter_for`, and keeps only the routes whose
    `bounds_one_turn()` is true.
  - `take_warm_lease` filters the due routes by that set before it takes the
    lock or writes a lease, so a non-bounding route takes no lease and starts
    no ping. Its retention, resume, drain and retirement are untouched.
  - `act` applies the same adapter's `one_turn` to the ping, so the route
    judged bounding is the route that gets bounded.
  - `test_keep_warm_pings_only_a_route_whose_adapter_bounds_one_turn` pins
    this: the opencode twin takes no lease and launches nothing, and the
    claude twin launches with `--max-turns 1`. It passed, and so did the
    three session modules (106 passed).
- **The coordinator's chain evidence (the review's accepted MAJOR).**
  `bounds_one_turn` infers the capability from method identity
  (`type(self).one_turn is not PlainAdapter.one_turn`); it does not declare
  it. Ruled: this makes no stated claim untrue.
  - The base method's own contract is "the argv bounded to one model turn;
    unchanged where the CLI has no such bound". So overriding `one_turn` is,
    by that contract, the declaration that the runner has a bound.
  - The inference and "bounds a call to one turn" can differ only for an
    override that does not bound. Such an override breaks `one_turn`'s own
    contract. It also needs a kit edit to `session_adapters` (the adapter
    table is kit code, not adopter configuration), and that edit is
    reviewed against this row.
  - Every shipped adapter classifies correctly, and the parenthetical
    "(claude's)" is true today.
  - A declared attribute would state the same decision more directly. That
    is a design preference, not a return. It would also cost the second
    edit that the draft this lane answered ruled out.
- **The new clause answers SR-227's approved "one bounded turn" clause.**
  Before, the LLR claimed `--max-turns 1` for a ping it did not bound.
  WI-737's sitting found that gap and confirmed it.
- **The CodeSymbol pointer holds.** `PlainAdapter.bounds_one_turn` exists
  in the `session_adapters.py` group and carries `Implements: SR-227,
  LLR-270`. The other pointer cells (SR-Refs SR-227, Component CMP-008,
  Module, TestRefs TC-266/267/268) are unchanged and still hold.

One real code defect sits under this text, not in it. WI-740 moved argv
building for EVERY registry row, of every family, into
`KeepWarmer.__init__`:

- `agent_session.build_argv` raises `ValueError` for a `{prompt}`-in-argv
  row behind a Windows batch shim. The kit's own template row
  `gemini -p {prompt}` is one, where `gemini` is an npm `.cmd` shim.
- So with the dial and `keepwarm_minutes` on, `keep_warmer` raises. I
  reproduced this at HEAD with a `gemini.cmd -p {prompt}` row:
  `ValueError: unsafe prompt delivery refused`.
- `dispatch.run` then stops before its first poll, where before only that
  one route's launch was refused.
- That breaks this row's own approved "built by keep_warmer when
  keepwarm_minutes is also on, ticked once per dispatcher poll by run". It
  does not change the shipped dial-0 behaviour.

The text is right. A sound requirement violated by code needs a code fix,
not a return. The fix is drafted as the one successor in WI-741's
`## Dispositions`. The act re-anchors LLR-270 by `--reattests LLR-270` in
batch K's act commit, with its `Status` left at `Approved`.

VERDICT: MEANING rows=1
