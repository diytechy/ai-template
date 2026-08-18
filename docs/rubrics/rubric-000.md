# rubric-000 — EXAMPLE (delete or copy on first real entry)

> Inert placeholder (`-000`) — names no real requirement, so it never gates and a
> fresh scaffold carries it for free. Copy it to `rubric-<name>.md` and fill it in
> when a requirement declares `Verification=Critique`. See
> [`README.md`](README.md).

**Judges:** SR-000 (`Verification=Critique`) · **Artifact recipe:** the TC's
`Parameters` cell (the command/steps that produce what's judged).

## Intent

Derived from **SN-000 / SR-000**, in the stakeholder's terms: state in one
paragraph what "good enough" *means* for this subjective slice — e.g. *the rendered
scene reads as a plausible physical space to a first-time viewer; nothing in it
announces "a machine made this"*. Written from the need's intent, **not** from the
test case, so a lax TC is caught here instead of inherited.

## Good anchors (what "good enough" looks like)

- **DevStg-Reqs** — <a definite, citable thing that must be true; e.g. surfaces meet the
  ground plane with contact shadows consistent with one light source>.
- **DevStg-Tests** — <another; e.g. materials read as their intended substance (metal vs
  matte) under the scene's lighting>.

## Bad anchors (known failure modes — accumulate at rework)

- **B1** — <a definite known-bad pattern; e.g. seam artifacts where two meshes
  meet>.
- **B2** — <another; e.g. impossible/contradictory shadows, or geometry floating
  off its support>.

_When a critique round names a **new** failure mode, add it here as the next `B#`
at rework, so later rounds judge against the accumulated reference (the accumulation
rule — see [`README.md`](README.md)). A verdict cites anchor ids (`B1`, `DevStg-Tests`, …)._
