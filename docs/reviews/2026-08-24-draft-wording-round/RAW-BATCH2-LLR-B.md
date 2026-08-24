# Raw return - batch 2 (LLR-201, LLR-200, LLR-196, LLR-194)

Unedited final message from `OPENAI-TERRA` (`gpt-5.6-terra`, `codex exec`),
captured with `--output-last-message`. Adjudicated in `RESUME.md`.

```
=== LLR-201 Title
SUGGEST: Checker cross-row coherence module below its engine
CUT-REDUNDANT: none
CUT-KEPT: Checker, cross-row coherence, and below-engine placement remain because they identify the mechanism and its location.
RISK: None; the Detail retains the concrete rule and emission behavior.

=== LLR-201 Detail
SUGGEST: Module beneath the engine composes every checker rule needing two or more rows. Orphan checks require SR -> LLR, TC, SN children and every cited id to resolve; LLR -> SR parent and TC; TC -> real spine id (seam ids supplement, never replace, a spine citation); SN -> one or more citing SRs. Each tier returns the same at-fault-id-and-finding pair, collecting ids flagged by rendered views here rather than at eight append sites. It resolves PB Refs to SR ids, LLR ids, and LLR Module paths; REPO DelegatedSRs to SR ids; CMP PartOf, SupersededBy, and Component tags on LLR, IF, PART, and ASSET rows to the component registry; and the docs/knowledge prefix in a CMP Knowledge cell to a real pack file. This is its only filesystem read. PhaseScope resolves requested labels plus the foundation phase in every filter once and scopes the require-verified status criterion. Results retain declared strict/advisory status: the declared strict failure set gates at its declared gate; advisory findings are reported and never change exit code. Emission order SR, LLR, TC, SN is used by report and console.
CUT-REDUNDANT: none
CUT-KEPT: The four-tier orphan cases, seam-id restriction, single filesystem read, PhaseScope scoping, strict/advisory split, and emission order remain because they define behavior and exit effects.
RISK: The compact orphan notation could be misread as allowing unresolved citations; every cited id still resolves.

=== LLR-200 Title
SUGGEST: State view depth-0 frame renderer
CUT-REDUNDANT: none
CUT-KEPT: State view, depth-0 frame, and renderer remain because they identify the generated mechanism.
RISK: None; the Detail retains placement and rendering constraints.

=== LLR-200 Detail
SUGGEST: traj_parse.frame_context inserts the declared external frame above derived structure in the state view's architecture tab. The block shows entities outside the system, boundary crossings, and external-to-external relationships to which the system is not a party. There is one lane per crossing; a party with several crossings has one card spanning its lanes, with the system opposite. Each crossing is a directed wire with a heading from the system's point of view. External relationships bow clear of the system card and carry no interface vocabulary. Realizing IF-### rows are joined from the interface registry, not repeated on the frame row: a crossing that nothing realizes is dashed and explicitly marked, and an interface whose endpoint is outside the tree but ties to no crossing is listed with its row's recorded reason. Three tables carry every cell truncated by the diagram. Vacuous when the repository declares no frame or contains only blank-form -000 example rows: the block is omitted and the artifact is byte-identical to the version before this view. Fixed geometry, id-sorted inputs, and no clocks keep freshness byte comparison stable.
CUT-REDUNDANT: none
CUT-KEPT: The no-interface-vocabulary rule, no-realizer and unpaired-interface behavior, vacuity clause, and deterministic-byte conditions remain because they are observable output constraints.
RISK: "Explicitly marked" needs to remain a clear no-realizer message, not a dashed wire alone.

=== LLR-196 Title
SUGGEST: Per-session fan-out utilisation telemetry, unaggregated
CUT-REDUNDANT: none
CUT-KEPT: Per-session, fan-out utilisation, and unaggregated status remain because they distinguish existing telemetry from the missing report.
RISK: None; the Detail states both the available data and build gap.

=== LLR-196 Detail
SUGGEST: write_session_log writes # wall-secs:, # api-secs:, # turns:, # tokens:, # cache-read:, and # cache-create: to each docs/iteration/*.log. The coordinator clock supplies wall time; agent_loop.parse_json_result reads the rest from the CLI type: result JSON event into the meta dict at its session-close path. regenerate_index folds these headers into one row per session in docs/iteration_index.md; per_turn_pace and per_turn_context already derive the like-for-like speed and context-volume values SR-177 identifies as source telemetry. NOT DISCHARGED: docs/iteration_index.md is a flat session table with no RUN or LANE grouping. Nothing joins the lanes value agent_loop resolves at boot from CLI --lanes, AGENT_LANES, or docs/stack.ini [agent-loop] lanes to concurrent trains. Configured lanes, occupied lanes, and work items integrated per wall-hour are therefore unmeasured. The missing aggregation is the stated build gap; no aggregator exists. When built, the per-run report is informational: reported and never gated, with no declared improvement target, threshold, or exit-code change, and a serial run reports one configured lane rather than omitting the line.
CUT-REDUNDANT: none
CUT-KEPT: Every telemetry header, its source, the missing RUN/LANE grouping and join, the build gap, and the informational no-target condition remain because they define both evidence and absence.
RISK: Treating session count as concurrent trains would overstate occupied lanes.

=== LLR-194 Title
SUGGEST: SN scope schema-tier validation seam
CUT-REDUNDANT: none
CUT-KEPT: SN, scope, schema tier, and validation seam remain because they identify the intended mechanism without claiming it exists.
RISK: None; the Detail keeps the non-discharge status explicit.

=== LLR-194 Detail
SUGGEST: schema_findings scans real, non-placeholder rows in a labeled table. An empty REQUIRED_FIELDS[label] column reports its row and column; an ENUM_FIELDS[label] value outside the closed set reports its row, value, and allowed set. SN-039 identifies this mechanism as scope's home, not a one-off column check. The intended SN entries require scope and limit it to template, this repository, or both; the extension skips -000 example rows and scans the shipped and this repository's filled needs registries. NOT DISCHARGED: SN has no REQUIRED_FIELDS or ENUM_FIELDS entry; no dict, checker branch, or test in shipped scripts names scope; and the whole-registry schema tier does not scan the needs registry. This is a seam for scope checking, not scope-checking machinery; no implementing module or symbol exists.
CUT-REDUNDANT: none
CUT-KEPT: Both failure classes, the closed vocabulary, -000 exemption, required registry coverage, and every negative implementation-status clause remain because they define the future check and current build gap.
RISK: The seam could be mistaken for a live SN check unless NOT DISCHARGED remains explicit.
```
