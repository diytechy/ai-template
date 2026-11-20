## 2026-11-19 — WI-1004: ten diverged policy duplicates each get one home, with the disputed inputs pinned; §13.14 leaves scope

Deferred open items: none.

Built on the maintenance branch `maint/wi-1004`, cut from `refactor_again` at
`426f88f60`, outside the lane workflow at the operator's direction: no claim,
no lane review rounds, commit hooks on. The parent session reviews and merges.

- **The critique and the ruling.** Gemini Argon's scope critique raised two
  BLOCKERs and three MAJORs; all five were adopted. The operator ruled on S1
  (2026-11-19) that the row stays one work item, walked in series, so the spec
  now names each behaviour's copies, home, requirement, landing order and kept
  answer on every disputed input before any code, with a Trust and an
  architectural-delta section (`b09b33fed`). The plan followed (`40a74a817`).
- **The rule for a kept answer:** correct for the inputs a supported route
  produces, then the one an accepted test pins, then the stricter; a strict
  check is never loosened. Where it applied twice over (B8b, §13.16), the
  stricter answer won and the tightening is named in a RESYNC entry.
- **Ten behaviours, ten commits,** each with its pins seen red for the
  disputed input first: B3 `value_to_cell` (`47438070f`), B12 module key
  (`956377922`), id number (`24e9ae0d7`), B5 SN-id universe (`0aabe35c0`), B10
  ref split (`35336c150`), B8b spec parse (`eab83e5cd`), the queued-spec
  lookup (`07fc4f676`), §13.13 spec precedence (`4a4e66432`), §13.22 command
  tokenizer (`c81c86f14`), §13.16 declared-file grammar (`4e0bcf9e0`). The
  homes are all in `kitlib/spine.py`, `kitlib/registry.py` and
  `kitlib/config.py`, each on `docs/kernel-modules-allow`, so no boundary or
  interface row moved; `handback` gained the one new edge, into
  `kitlib.registry`.
- **§13.14 left scope.** Its four arms agree on every verdict. They differ on
  a missing output, by postures each generator documents as deliberate, and on
  the STALE line's stream, which `check.py` merges. That is duplicated
  plumbing, not a disagreeing policy duplicate.
- **Files other builders hold.** `kitlib/decisions.py` (WI-1009) changed by an
  import and two call sites. `trajectory_arch.py` (WI-1007) changed in
  `_parse_kernel_allow`'s loop and the `KERNEL_ALLOW_SEP` binding. After
  trunk (`96689d3be`) was merged in, that edit lives in `arch_seams.py`,
  where WI-1007 moved the function, and the composer is trunk's unchanged;
  WI-1009's `kitlib/decisions.py` change merged beside this row's without
  conflict. `check_trajectory.py`, `gen_open_items.py`, `pending.py` and
  `traj_status.py` were not touched.
- **At review (Sol).** A list element carrying `;` was refused only for
  `adjudicates`; for `sr_refs`, `needs`, `adopted`, `authoring_tags` and a
  list-form `supersedes` both parses joined it into the cell, one element read
  as two references. The stricter answer now holds for every list key
  (`kitlib.registry.spec_list_element`), pinned per key. No spec on
  `docs/work` or `docs/archive/work` writes one, so no key kept the old
  reading.
- **The census.** `[dupes-census]` reads 2/2/32 before and after: the deleted
  copies' bodies differed from their homes', which the body census does not
  count. The OI-130 re-score's `policy.json` drops each folded copy, as its
  README asks.
- **Found, not fixed:** a bare string in a spec's list key (`sr_refs =
  "SR-1"`) is read character by character by the one spec parse, as both
  copies read it before; and `check_docs.declared_lines` is a sixth reader of
  a declared file (`orphans-allow`, `status-lint`), with a grammar of its own
  (no separator), which also reads `utf-8` without stripping a byte-order
  mark.
