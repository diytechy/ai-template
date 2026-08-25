# The blind minimal-map derivation brief (WI-508 slice 2)

_The brief two independent agents were given, recorded here BEFORE their returns
so the question cannot be re-written to fit the answer. The returns are
[`2026-08-25-blind-minimal-map-derivation.md`](2026-08-25-blind-minimal-map-derivation.md).
The program that commissioned it: `docs/work/active/wi508-architectural-remap/`.
The requirement it produces evidence for: `SR-163`, decomposed at slice 1._

## 1. What is being asked, and why it is asked BLIND

`OI-58` was ruled (c): an agent re-derives the **minimal module map** from the
requirements alone, blind to the live layout; the live map is then diffed
against it, and each divergence is adjudicated — consolidate, or keep with a
recorded reason — and filed.

Blindness is the method's whole integrity, and the failure mode it defends
against has a name in this repo's own spine-authoring rules:
**implementation-mirroring** — a "fresh" derivation that re-describes the code
rather than the need, which produces agreement that means nothing because both
sides were copied from the same source. The precedent is `WI-467`, where two
axis-diverse teams derived a capability breakdown from the needs and the
boundary frame alone, a third pass built the alignment map, and every orphan
became a finding rather than a silent merge.

**Two teams, two axes, deliberately.** Two derivations on the SAME axis mostly
agree with each other and tell you little; two on different axes disagree
where the decomposition is genuinely underdetermined, which is exactly the
information the adjudication needs.

## 2. The objective function, in the owner's words

> serve the declared outputs while minimizing internal signal overlap and
> duplicated behavior — **calls, not lines**

"Calls, not lines" is load-bearing and is the brief's whole discriminator: the
target is minimum TOTAL BEHAVIOR, not minimum file count and not minimum
character count. A map that reaches a small module count by fusing unrelated
responsibilities into one wide module scores WORSE, not better, because the
behaviours it merged are still all there and are now harder to reach one at a
time.

## 3. The research grounding, from `OI-58`'s own row

Given to both agents as framing, not as instructions:

- **Minimum description length / DRY-as-information-theory.** A behaviour
  stated once is a smaller model of the system than the same behaviour stated
  twice. Duplication is not a tidiness problem; it is a larger model.
- **Deep modules.** Prefer a narrow interface over a large implementation to a
  wide interface over a thin one. A module earns its boundary by how much its
  callers do NOT have to know.
- **This repository's own measured findings about agent readers.**
  One-home-per-behaviour measurably improves navigation; duplicated prose
  creates retrieval collisions; and context is the scarce resource, so total
  size minimisation IS agent-performance work rather than aesthetics.

## 4. The input set — closed, and the reason each file is in or out

**IN** (a directory containing exactly these five files was the agents' whole
world):

| file | why it is an input |
| --- | --- |
| `VISION.md` | the purpose statement, verbatim; the only prose |
| `stakeholder-needs.toml` | the needs the system exists to serve |
| `system-requirements.toml` | the obligations derived from them |
| `external.toml` | the depth-0 frame — the **declared outputs** the objective names, as boundary crossings, plus who is outside and what the system is not a party to |
| `hats.toml` | the review-perspective roster: a lens absent from the blind input set cannot produce its obligations (the spine-authoring rule for blind re-derivation names the roster as an input, not an aid) |

**OUT**, each for a stated reason — this is the list that makes the exercise
blind rather than merely fresh:

- `low-level-requirements.toml` — **the design tier names modules by design.**
  Handing it over would hand over the answer; it is the very thing the
  derivation is to be diffed against.
- `components.toml` / `components.derived.toml` — the live partition, with the
  module roster written into its notes.
- `interfaces.toml` — the live seams, endpoint by endpoint.
- the source tree, `PROCESS.md`, `PROCESS_OPTIONS.md`, `README.md` beyond the
  vision tag, `docs/stack.ini`, the dashboard, the logs — every one of them
  either names the live modules or lets them be inferred.

**The one contamination that cannot be removed, and how it was handled.** Some
`acceptance_criteria` cells legitimately name a current carrier — the spine's
own rule is that an SR states the delivered capability while acceptance may
carry rewritable current-carrier evidence. Those names are inside the
requirements and cannot be stripped without falsifying the input. Both agents
were therefore told to treat a concrete artifact name in a requirement cell as
**evidence that an obligation exists**, never as a module assignment, and to
list every place they used one.

## 5. The two axes

- **Team A — outputs-backward.** Start at `external.toml`'s boundary crossings
  (what the system must hand across its edge), work backwards to the internal
  signals each output requires, and cluster the signals into modules. The
  question this axis is good at: *is anything produced twice?*
- **Team B — obligations-clustered.** Start at the SR set, group obligations
  that share an internal signal or a failure mode, and let modules fall out of
  the clusters. The question this axis is good at: *is any obligation owned by
  nobody, or by two owners?*

## 6. The required return shape

Both agents were asked for the same artifact, so the returns are comparable:

1. **The module map.** Each module: a functional NAME (never a guessed
   filename), the one-sentence responsibility it owns, the SR ids it serves,
   its inputs and outputs as signals, and the modules it depends on.
2. **Coverage, both directions.** Every SR mapped to exactly one owning module
   — nothing unserved, nothing served twice — with any SR that resisted
   single-ownership called out by id.
3. **The objective applied, per decision.** Every place two candidate modules
   were merged, or one split, with the reason in the objective's own terms
   (which duplicated behaviour it removes, or which wide interface it narrows).
4. **The overlaps found IN THE REQUIREMENTS.** Where two SRs describe behaviour
   that a minimal map would state once — a finding about the spine, produced as
   a side effect, and worth as much as the map.
5. **An honesty section.** Anything recognised from prior knowledge of this
   repository, any place a concrete artifact name in a cell was leaned on, and
   any judgement the requirements did not determine.

## 7. What the derivation is NOT

It is not a proposal to restructure anything. No module moves, no cell moves,
and no consolidation is filed off the derivation alone. The map is one half of
a diff; the adjudication is a separate pass — the only role permitted to read
both sides — and every divergence is a finding to be ruled on, never a silent
merge or a silent deletion. The legacy side's own recorded rationale is read
FIRST, before any divergence is called an accretion.
