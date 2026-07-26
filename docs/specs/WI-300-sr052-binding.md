# WI-300 remainder — bind A1 / A3 / A4 so SR-052 can flip

**Status: queued.** The last step of WI-300's option (f) ruling. Written
2026-07-26 as a resumption guide: a fresh session should be able to start from
here without re-deriving anything.

**Spec of record for:** WI-300 (this file is its remaining-work half; the ruling
and the per-anchor pass are in [WI-300.md](WI-300.md)).

---

## 1. Where this sits

SR-053 flipped to `Verification=Test` on 2026-07-26 — the first SR to leave the
critique chain — after its five anchors were mechanized and bound. **SR-052 is
the same job, three anchors short.**

| SR | State | What it needs |
|---|---|---|
| **SR-053** | ✅ `Test` | done |
| **SR-052** | `Critique` | **A1, A3, A4 bound.** A2 is done (`LLR-101`/`TC-104` + `LLR-108`/`TC-113`) |
| **SR-054** | `Critique` **by design** | not this WI — see §6 |

**The rule that governs the flip** (from the ruling, and it is the one way this
fails): *an SR keeps `Verification=Critique` only while a perceptual child
remains under it* — and **land every child TC with real `Evidence` BEFORE
changing an SR's `Verification`, never the reverse.**

**A distinction that cost a false start last time:** *clearing a residue clause
is not the same as binding an anchor.* Clearing says "this part is no longer
judged by eye"; binding says "this anchor is owned by a test". A1/A3/A4 have no
residue clause to clear — they are simply **undecomposed**, still riding the
coarse `LLR-053`/`TC-053`.

## 2. The method that worked — reuse it

Four anchors were mechanized this way on 2026-07-25/26 (WI-309…312). The pattern:

1. **Measure the anchor against the shipped artifact first.** Every one of the
   four was assumed perceptual and turned out to be arithmetic or set
   membership — *and every one failed on first measurement*. Do not start by
   writing the test; start by finding out whether it passes.
2. **Declare, then assert.** Where the anchor says "uniform"/"consistent", the
   fix was almost always *"there was no declared set to be consistent with"*.
   Declare the set (with a **role per entry**), merge near-duplicates into the
   role's entry, then assert membership.
3. **Sweep every emitter**, via `_every_emitter_document()` in
   `tests/test_gen_trajectory.py`. This bit **three times**: a document walk
   judges only the emitters its fixture happens to render. That helper is now the
   single place the fixture list lives — add to it, never build a private list.
4. **Scope to paint surfaces**, via `_style_surfaces()`. The rendered dashboard
   *quotes* CSS and hexes inside prose (registry `Detail` cells explaining past
   fixes); a whole-document scan judges documentation as if it were code.
5. **Prove the guard fails** against each original defect before keeping it.
   A guard that cannot fail is not a guard (the WI-293 lesson). Use a retry loop
   on the restore path and assert the source is byte-identical afterwards — a
   Windows `OSError` in a `finally` once left `gen_trajectory.py` mid-mutation.
6. **Bind**: child LLR under SR-052 + TC with `Automated: Yes` and the pytest
   node id in `Evidence`. State the **scope and its narrowing** in the LLR — what
   is proven, and what is deliberately not.

## 3. A1 — keyboard reachability

**Anchor:** every interactive element (tab buttons, expandable blocks, each SVG
node opening a detail panel) is reachable and operable by keyboard; *"tabbing
walks every control in a sensible order"*.

**Measured 2026-07-26 (shipped artifact):**

- **0** elements carry an interaction hook (`data-node` / `data-descend` /
  `data-id`) without `tabindex="0"`. The structural half already passes.
- The page wires **12** interaction selectors — `.block`, `.block[data-node]`,
  `.block[data-wi]`, `.cell`, `.wi`, `[data-descend]`, `[role=tab]`, `.edge`,
  `.layer`, `.view, .tablescroll`, `.drill:not([data-ready])`.
- **2 `<details>` elements have no `<summary>`.** Worth a look — a `<details>`
  without a summary is not keyboard-operable in the usual way. Confirm whether
  these are real disclosure widgets before treating it as a finding.

**Existing owning tests:** `test_a1_drill_leaf_blocks_are_keyboard_focusable`,
plus WI-273's `test_tabs_are_an_aria_tablist`,
`test_tab_controller_does_keyboard_and_roving_tabindex`,
`test_tab_button_and_panel_helpers_emit_the_aria_pattern`.

**Proposed core:** *every element the page wires an interaction to is focusable
by the shared mechanism.* Derive the selector list **from the emitted JS** rather
than hard-coding it, so a new wired selector cannot be added without a matching
focusability guarantee. That is the assertion the existing tests do not make —
they check specific known elements, not the closure.

**Residue to drop, with reasoning:** the rubric's *"sensible order"*. Document
order **is** assertable (and equals emission order); *perceived* order is not.
The spec's original recommendation stands: assert document order matches emission
order and drop the perceptual half.

## 4. A3 — no information by colour alone

**Anchor:** every status / phase / type encoding pairs its colour with a
redundant text or shape cue.

**Measured 2026-07-26, with CSS tokens resolved** (this matters — the status
legend paints via `var(--done)` etc., so a raw hex scan under-reports it 1/4
when the truth is 4/4):

| Vocabulary | Fills explained by a legend swatch |
|---|---|
| status | **4/4** (plus a distinct glyph per status — `STATUS_GLYPH` covers `STATUS_BUCKET` exactly) |
| tier | **4/4** |
| okf-type | **6/6** |
| phase | **8/8** |
| sw-node | **3/4** — `component` `#44403c` has no legend entry |

**The one open question:** `#44403c` is *not painted as a node fill* — it appears
only in a `style` attribute on the How-SW detail-panel badge. So it may not be a
"status/phase/type encoding" the anchor governs at all. **Decide that before
"fixing" it** — the A2 lesson from WI-312 was that measuring the wrong set
manufactures findings the standard does not make.

**Existing owning tests:** `test_a3_status_glyph_pairs_every_status_fill`,
`test_a3_flat_dag_fallback_also_prefixes_the_status_glyph`,
`test_every_multifill_panel_emits_a_palette_bijection_legend`.

**Proposed core:** *for every declared colour vocabulary, every member resolves
to either a legend swatch labelled in words or a shape/text cue on the element
itself* — with token resolution built in. Enumerating the vocabularies from the
module (as `_palette_vocabularies()` already does for U5) makes this closed: a
new vocabulary cannot be added without a redundant cue.

## 5. A4 — text contrast

**Anchor:** WCAG 2.1 AA — 4.5:1 normal text, 3:1 large text and graphical/UI
boundaries.

**Existing owning tests (six, already substantial):**

| Test | Covers |
|---|---|
| `test_a4_node_fills_meet_the_wcag_floor` | every node fill vs its label |
| `test_a4_every_emitted_dashboard_contrast_pair_meets_floor` | computed badge/boundary/focus pairs |
| `test_a4_no_sub_label_opacity_discount` | opacity must not erode sub-label contrast |
| `test_a4_theme_token_fills_behind_white_text_meet_the_floor` | theme-token fills |
| `test_a4_hub_fill_is_not_the_page_accent` | the WI-293 regression |
| `test_a4_ring_ink_clears_the_3to1_floor_against_every_node_fill` | the focus ring (bound under SR-054 as `LLR-105`) |

**This is the cheapest of the three** — the arithmetic is done. The work is
almost entirely **binding**: write the child LLR/TC citing these node ids, and
check whether the set is *closed* (does a newly added fill automatically enter
`test_a4_every_emitted_dashboard_contrast_pair_meets_floor`, or is its pair list
hand-maintained?). If hand-maintained, close it the way U5's sweep is closed.

**Note the split:** `LLR-105`/`TC-108` binds the ring under **SR-054** (T5), not
SR-052. A4's broader arithmetic still has no child LLR under SR-052.

## 6. After the flip — what is NOT in scope here

Once A1/A3/A4 are bound and SR-052 flips, **`perceptual-stale` still fires**,
because SR-054 keeps `Verification=Critique` by design. Retiring critiques
*outright* then rests on two clauses:

- **T1** "the entry point is *obvious*"
- **T3** "the reader stays *oriented*"

Both describe a **reader's experience**, not a property of the artifact, and
cannot be asserted without redefining them as proxies. **T4** (truncation
affordance) and **T7** (viewport fit) *are* mechanizable with a browser harness
measuring bounding boxes and `scrollWidth`.

**That is an owner decision, not buildable work**, and it is deliberately not
filed as a WI. Do not quietly mechanize T1/T3 into proxies to make the gate
green.

## 7. Done-when

- [ ] A1, A3 and A4 each have a child LLR under SR-052 + a TC with
      `Automated: Yes` and real pytest node ids in `Evidence`.
- [ ] Each new LLR states its **scope and narrowing** — what is proven and what
      is deliberately not.
- [ ] Every new guard is verified to **fail** against the defect it claims to
      catch, and the source is byte-identical afterwards.
- [ ] Only then: `SR-052.Verification` → `Test`; supersede `LLR-053`/`TC-053`;
      retire [rubrics/dashboard-accessibility.md](../rubrics/dashboard-accessibility.md)
      to a record with an anchor→LLR/TC map, as
      [dashboard-uniformity.md](../rubrics/dashboard-uniformity.md) now is.
- [ ] `check_trajectory --strict` shows `perceptual-stale` naming **SR-054 only**.
- [ ] Full suite + `check.py` at the derived gate; spine change ⇒ log it as
      **RE-ATTESTATION PENDING**.

## 8. Standing hazards (the ones that actually bit)

- **`./.venv/Scripts/python.exe`** on Windows — bare `python` is not on PATH.
- **Editing `gen_trajectory.py` re-reds `perceptual-stale`.** Path-triggered,
  independent of what changed. Currently parked by owner direction.
- **A scripted `.py` rewrite on Windows produces CRLF**, and `check_dupes`
  fingerprints *tokens* — a CRLF working copy voids every census entry for that
  file (22 phantom findings, none in any commit). If `dupes` reds after a
  scripted edit, check line endings before believing it.
- **A regex rewrite over CSS can match its own comment.** `/* opacity: … */`
  was matched by the `opacity:` pass and mangled the token block.
- **Splicing a constant into an emitter template with `+` rebinds `.format`**
  to the last fragment of an implicitly-concatenated string. Declare-and-assert
  instead (`SVG_RX` is the worked example).
- **status.md is forward-only and enforced** — a `done` WI id in its
  hand-authored prose errors under `--strict`. It caught one this session.
- **R-F**: a live spec cited by no open WI errors. When the last WI citing this
  file closes, archive it to `docs/archive/specs/` with the close date.
