# Rolling review — 2026-11-05 — maintenance & sustainability

**Scope (owner request):** a deep review of the kit with maintenance and
sustainability as the lens. Four questions drive every finding:

1. Where does code duplicate behaviour that could be consolidated?
2. Where can the architecture-related skills and prose be improved?
3. Where can the requirement → implementation spine be improved, so that
   requirements and tests sit as close to the end user as possible — not at
   implementation altitude, and not testing other test infrastructure?
4. Where does the kit guard against contrived cases that should just warn?

**Method:** findings are appended as the investigation proceeds and committed
to `rolling_review` after each pass, so partial progress survives a usage
limit. Each finding carries a severity (`[HIGH]`/`[MED]`/`[LOW]`), an anchor
(file or rule), the issue, and a concrete change. Measurements are reproduced
with the command that produced them.

**Status:** IN PROGRESS. Sections marked `(pending)` have not been reviewed yet.

---

## 0. Orientation measurements (reproduced 2026-11-05)

```
wc -l project-trajectory/scripts/*.py            ->  98,627 lines, 116 files
wc -l project-trajectory/scripts/kitlib/*.py     ->  12,747 lines,  25 files
wc -l tests/*.py                                 -> 157,218 lines, 281 files
wc -c project-trajectory/PROCESS.md              ->  98,912 bytes
wc -c project-trajectory/PROCESS_OPTIONS.md      -> 199,478 bytes
wc -c project-trajectory/README.md               ->  93,389 bytes
wc -c project-trajectory/RESYNC_PACK.md          -> 643,982 bytes
wc -c project-trajectory/skills/*/SKILL.md       -> 144,330 bytes, 33 skills
registries: SN 35 rows, SR 138, LLR 331, TC 363, IF 255, OI 120
```

These numbers are the headline finding on their own (see §1).

---

## 1. Findings — size and surface area (pending)

## 2. Findings — code duplication / consolidation candidates (pending)

## 3. Findings — architecture skills and prose (pending)

## 4. Findings — the spine: altitude of SN/SR/LLR/TC (pending)

## 5. Findings — tests testing test infrastructure (pending)

## 6. Findings — guards vs warnings (contrived cases) (pending)

## 7. Recommendations, ordered by leverage (pending)
