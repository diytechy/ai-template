# The interface-rework exception dossier (WI-495, OI-49 ruled (b))

Prepares the seven-row exception read OI-49's ruling (b) named, so the
owner's ratifying Status-change commit reads a recommendation per item
instead of re-deriving each one cold. This dossier does not flip any
`status`/approval cell — the ratifying commit is the owner's — and it does
not pre-empt OI-60 (pending), which is coordinated against below wherever
the two rows share a cell.

## 1. The two unargued picks

### IF-013 -> SR-006 (not SR-007)

`IF-013`'s contract is `check.py`'s CLI: run the active gate's declared
steps as subprocesses, exit nonzero on any required failure, never a
silent pass. `SR-006` ("Gate/tier harness enforces required steps") states
that exact obligation almost verbatim: *"run the required steps of the gate
... fail that gate when a required tool is missing, reporting SKIP(missing)
rather than silently passing."* `SR-007` ("Declared stack profile, refused
when it is broken") governs a different observable — the stack profile's
own validity — and its own rationale draws the same line: *"a missing
declared binary fails under SR-006, which states that clause"* (recorded on
SR-007 itself, `docs/requirements/system-requirements.toml`). `req_refs`
correctly lists both parents this seam realizes/relies on; `owner` names the
one answerable for the contract's central claim.

**Recommendation: KEEP SR-006.** Reason written into `IF-013`'s `notes`
cell (traced, not ratified — the row is `Drafted`, so no re-attest window
opens).

### IF-044 -> SR-154 (not SR-155)

`IF-044`'s contract is `agent_route.py`'s module/CLI surface: seven named
call sites. Five of them (`load_registry`/`load_enabled`, `resolve_enabled`,
`parse_env`, `select`, `escalate`/`failure_action`) serve the general
cross-family review-routing capability `SR-154` states verbatim: *"obtain
each review or critique verdict ... resolved ... from the delivered agent
registry's declared ... rows ... drawn from a different model family
wherever one is configured."* Only `planner_pair()`/`planner_fallback()`
serve `SR-155`'s contested-planning round, and there as one input function
among several the round also needs (briefs, cross-critique, arbitration —
none of which this module carries); `SR-155`'s own fan-out rationale names
the round's children as "the successive phases of that single round," of
which planner selection is one step, not the round itself.

**Recommendation: KEEP SR-154** — the majority-surface owner. Reason
written into `IF-044`'s `notes` cell.

### OI-60 coordination, both rows

Both `IF-013` and `IF-044` are named in `OI-60`'s census
(`docs/log.d/2026-08-22-wi455-consumers-transform.md`) as 2 of the 12
requirement-owned `Provides` rows whose `this_project` is underivable — no
`LLR` row owns `scripts/check` or `scripts/agent_route` outright (verified:
zero `module = "project-trajectory/scripts/check.py"` / `"...agent_route.py"`
hits carry those as an LLR's *sole* identity — every LLR citing either
module decomposes a narrower slice, e.g. `LLR-008`, not the module's owner
role `IF-013`/`IF-044` need). That absence is exactly why these two rows
fell back to an `SR` owner in the first place (the schema's own stated
preference is "design tier wherever a design row exists for the owner-side
endpoint").

**What each OI-60 option does to this pick, without pre-empting it:**
- **(a) shed `direction` only, keep an endpoint cell** — touches
  `this_project`/`counterpart`/`direction`, not `owner`. This pick stands.
- **(b) re-point the 12 first, then shed both** — would extend the owner
  re-point pass to these 12 rows, minting or finding the design row that
  implements each. If ruled, it supersedes this pick: `IF-013`/`IF-044`'s
  `owner` would move from `SR-006`/`SR-154` to whatever `LLR` is minted or
  found, per the schema's own design-tier preference. This dossier's
  recommendation is the right SR-tier answer *until or unless* (b) lands.
- **(c) shed both now, record the 12 modules in `notes`** — touches
  `this_project`, not `owner`. This pick stands.
- **(d) hold the shed, take the two free corrections** — touches nothing on
  these two rows. This pick stands.

So the recommendation is safe under three of OI-60's four options and is
explicitly provisional under the fourth. Written into both `notes` cells so
the coordination is visible on the row itself, not only here.

## 2. The five-row loaders-vs-decision split

| Row | `this_project` | `counterpart` | Contract states it CROSSES | `owner` |
|---|---|---|---|---|
| IF-056 | scripts/gen_trajectory | scripts/check_trajectory | the validator's **loaders/joins** (`read_rows`/`load_wis`/`_split_refs`/`_norm_module`/`load_ifs`/`component_top_view`/`_cycles`) — the DERIVATION seam | LLR-049 |
| IF-082 | scripts/traj_parse | scripts/check_trajectory | "IF-056's derivation-loader seam, as HELD by the split sibling" — same loaders | LLR-049 |
| IF-084 | scripts/traj_status | scripts/check_trajectory | "IF-056's derivation-loader seam, as HELD by the split sibling" — same loaders | LLR-049 |
| IF-071 | scripts/gen_trajectory | scripts/schedule | the scheduler's **ready-frontier** (`schedule.load_registry_rows`/`load_wis`/`frontier`/`evaluate`) — the DECISION seam | LLR-058 |
| IF-085 | scripts/traj_parse | scripts/schedule | "IF-071's frontier DECISION seam, as HELD by the split sibling" — same frontier | LLR-058 |

Read against the two candidate owners' own rows:

- `LLR-049` ("Bounded software top view") — `module =
  project-trajectory/scripts/check_trajectory.py`, `code_symbol =
  component_top_view/component_findings/module_components/load_cmps/
  _cmp_roots`. This is precisely the loaders/joins surface IF-056/082/084's
  contracts name.
- `LLR-058` ("WI-DAG frontier + deterministic traincar ordering") —
  `module = project-trajectory/scripts/schedule.py`, `code_symbol =
  ready/frontier/evaluate`. This is precisely the ready-frontier surface
  IF-071/085's contracts name.

The split is not arbitrary — it is the WI-280 facade decomposition read
straight off each contract's own "Contract: IF-056's" / "Contract:
IF-071's" cross-reference, and each owner's `code_symbol` cell matches its
claimed side with no overlap or ambiguity.

**Recommendation: KEEP all five as recorded.** No re-pick, and no cell
edit — the grounding already lives in the contract prose (IF-082/084 state
"Contract: IF-056's" / IF-085 states "Contract: IF-071's" explicitly), so
adding a `notes` reason would restate what the row already says rather than
supply a missing one. This is the opposite shape from item 1: there the
reason was absent; here it is present and correct, just never checked
against the two candidate LLRs' own text before now.

## 3. IF-131's single-constituent bundle

`IF-131` (owner `LLR-080`, component `CMP-006`) is the sole seam declared
as the carrier of a `carried_by` chain with exactly **one** constituent —
`IF-132` (`carried_by = "IF-131"`, component `CMP-009`). Compare the
carriage field's declared purpose: *"Several seams riding one larger seam
name the same carrier id, so granularity stops being a forced choice"* — a
bundle exists to let one owner's contract answer for several distinct
crossings at once (`IF-102`: 16 constituents; `IF-123`: 3). A carrier with
exactly one constituent is not doing that work.

The closer precedent is the `IF-056` family, which faces the **identical**
shape — one underlying seam (`check_trajectory`'s loaders), declared
separately in each of three cross-component consuming modules because "the
rule covers PAIRS" — and that family does **not** use `carried_by` at all;
it states "Contract: IF-056's" in prose (§2 above). `IF-131`/`IF-132` are
the same situation (one underlying seam — `gen_arch_map.scan_inventory` —
declared twice because `gen_arch_map` straddles `CMP-006`/`CMP-009`) wearing
a different mechanism. `IF-132`'s own contract text already carries the
equivalent prose sentence: *"Same `scan_inventory` seam as IF-131; declared
separately because the two consumers sit in different components and the
rule covers PAIRS."* The `carried_by = "IF-131"` cell is therefore
redundant with prose the row already states, and it is the one place in the
registry that answers the same shape of question two different ways.

**Recommendation: the plain re-point** — drop `carried_by = "IF-131"` from
`IF-132` and let its existing prose carry the cross-reference, matching the
`IF-056`/`082`/`083`/`084` precedent exactly. **Not executed by this WI**:
`carried_by` is the field OI-49 flagged as part of the judgement under
ratification, and the two-row edit (dropping one carrier's only
constituent link) is exactly the kind of call this dossier exists to
recommend rather than pre-empt. Left for the owner's ratifying commit,
should it accept the recommendation — a one-line `carried_by` deletion,
already prose-safe.

## 4. The `carried_by` depth bound of 2

`IF_CARRIAGE_MAX_DEPTH = 2` (`project-trajectory/scripts/trace.py:2498`),
provisional since the ruling that created the obligation (Q3, 2026-08-15a)
fixed a number without fixing the evidence for it — the module comment
says as much: *"Two is the depth the ruling's own worked shape needs ...
so a third level is a bundle inside a bundle, which may be right and
should be looked at."*

**Evidence gathered by direct measurement** (`grep carried_by
docs/requirements/interfaces.toml`, 20 hits, all constituent-side cells):
the three carrier ids — `IF-102`, `IF-123`, `IF-131` — were each read in
full (§3 above, and IF-102/IF-123's own rows). **None of the three carries
a `carried_by` cell of its own.** Every live carriage relationship in the
registry today is exactly **one hop deep** (a constituent naming a carrier
that is not itself anyone's constituent) — there is no live bundle-inside-
a-bundle, and therefore no row has ever come within one hop of testing the
bound the depth-2 warn was set to catch.

That is weaker evidence than "the bound is right" and stronger evidence
than "the bound has been examined" — it is the same reading OI-49's own
pre-ruling recommendation gave it *("nothing has yet wanted a third level,
which is weak evidence that 2 is right and good evidence that nobody has
tested it")*, now confirmed against the live registry rather than
recalled.

**Recommendation: KEEP PROVISIONAL.** The bound costs nothing today (it
warns, never gates, per `if_carriage_advisories`) and no population exists
yet to ratify a specific number against. Ratifying "2" now would bless a
figure with no worked example past depth 1 to test it; leaving it
provisional costs nothing and is honest about what has and has not been
tried. Re-open only if a real depth-2 chain is proposed.

## 5. IF-097 and IF-080 — verify-and-state, not re-derived

**IF-097.** OI-49's own ruling record
(`docs/log.d/2026-08-21-owner-rulings-oi48-52.md`, quoted verbatim in
`docs/requirements/open-items.toml#OI-49`) states the `;` multi-endpoint
form on `IF-097` (`counterpart =
"scripts/agent_loop;scripts/plan_briefs;scripts/plan_runner"`) is CORRECT
as authored (three consumers, one shared contract — three rows would be
three copies of it) and names one residue: `check_trajectory.
_declared_seam_pairs` did not split on `;`, so the row silently
contributed no coverage pair. **Verified fixed**: the 2026-08-21 review's
`WORKLIST.md` item **W-12** ("Two seam readers disagree on `;`-joined
endpoint cells (7 rows)") names the identical defect and lands the fix —
confirmed live in `project-trajectory/scripts/check_trajectory.py`, whose
`_declared_seam_pairs` docstring today reads *"`trace.py` has split on `;`
since IF-097 ... this reader did not, so the two readers of the same cells
disagreed — 14 of 249 pairs ..."* (past tense; the function now calls
`_seam_endpoints` on both `this`/`counterpart` before pairing) and which
landed at commit `3c27291c` ("review: the MINOR sweep"). **No further work
owed on IF-097.**

**IF-080.** The ruling record states `IF-080`'s `this_project =
"scripts/integrate"` is correct as written — `handback.py` declines a
`Contracts:` line precisely because the integrator seam is `IF-080`'s, and
the plan was amended to say so. Read directly (`docs/requirements/
interfaces.toml:1034-1046`): the row is intact, `this_project =
"scripts/integrate"`, `owner = "LLR-140"`, unremarkable and unchanged.
**No further work owed on IF-080.**

## Summary — recommendation per item

| Item | Recommendation | Cell touched |
|---|---|---|
| 1a. IF-013 -> SR-006 | KEEP | `notes` (reason written) |
| 1b. IF-044 -> SR-154 | KEEP | `notes` (reason written) |
| 2. IF-056/082/084 (loaders) vs IF-071/085 (decision) | KEEP all five | none — already self-grounded |
| 3. IF-131/IF-132 carriage | RE-POINT — drop `carried_by` from IF-132 | none by this WI — recommendation only |
| 4. carried_by depth bound = 2 | KEEP PROVISIONAL | none |
| 5. IF-097, IF-080 | verified closed, no action | none |

No `status`/approval cell was touched anywhere in this dossier or its
registry edits. The ratifying Status-change commit — accepting or
overriding the five recommendations above — is the owner's.
