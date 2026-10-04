**VERDICT: NOT-READY.** The architecture can largely be designed from the recorded direction, but the spec leaves owner decisions about approval authority, trunk scope, provider identity and live-probe authorization unanswered.

References below are relative to the repo; **WI** means [WI-788](../../../docs/work/queued/WI-788-provider-homes-and-new-routes.md). No files were modified.

**OPEN ITEMS FOR THE OWNER:**

1. **Who approves spine text after the adjudicator drafts it and the adjudication reviewer edits it?**
   
   Both sessions have authored the text. Having the original adjudicator approve on its final pass conflicts with “a review or judgement never runs in a session that authored what it judges.” Separating commits does not establish session independence. The flow remains explicitly an *option*, and its approval act is unspecified. Evidence: WI:105–111, 139–143, 158–166; [current amendment brief:96](../../../project-trajectory/prompts/adjudicate-amendment.template.md).
   
   **Options:** a third, non-author adjudicator approves; the owner approves; explicitly permit the drafting adjudicator to approve independently edited text.
   
   **Recommendation:** require a non-author approving session, while preserving human-held approvals. State that the drafting adjudicator’s final pass is authoring, not approval.

2. **Does the prohibition on combining spine-text changes and snapshot updates apply on trunk too?**
   
   The lane rule is decided; trunk removal is only “may need removing.” The note cannot declare a universal guard or retain the trunk exception as owner-approved without choosing an unresolved scope. Evidence: WI:256–261; [existing allowance:1039](../../../project-trajectory/scripts/baseline_snapshot.py).
   
   **Options:** lane only; all approval paths, including trunk; a specifically defined trunk exception.
   
   **Recommendation:** apply it to lane and trunk approval paths, with text committed and independently reviewed before re-anchoring.

3. **Which exact service does “FreeAI” mean, and what substitutes are acceptable for SuperGrok?**
   
   FreeAI has no URL, provider identifier or product definition. “xAI/SuperGrok” also does not say whether an xAI API route satisfies the request if the SuperGrok account entitlement supplies no suitable headless interface. Research can establish capabilities; it cannot determine which product or replacement the owner intended. Evidence: WI:18–25, 48–52, 60–70.
   
   **Options:** name the intended services and entitlements; permit an equivalent API/gateway route; retain visibly untested or unsupported entries pending provision.
   
   **Recommendation:** identify FreeAI by URL/provider ID; treat SuperGrok entitlement and xAI API access separately. Do not assume a paid API is an authorized substitute.

4. **May half 1 run new authenticated/live probes or recordings, and under which accounts and spending limit?**
   
   Half 1 requests sources and probes; explicit recording authorization appears only in half 2. No Google, xAI/SuperGrok or FreeAI provisioning or spending authority is recorded. This blocks new live evidence, although documentation and existing-fixture research can proceed. Evidence: WI:58–73, 82–85.
   
   **Options:** documentation/code/existing recordings only, with unverified claims labelled; specified live probes using owner-provisioned accounts and a cap; owner-run recordings.
   
   **Recommendation:** authorize documentation and existing recordings for half 1; specify any additional live runs individually. Keep credentials outside tracked files and redact recordings. Actual accounts to enable in this repo can be selected at the checkpoint if half 1 does not require testing them.

**FACT CHECK:**

| Claim checked | Result and evidence |
|---|---|
| Route `env` merges over launch environment; comment names `CLAUDE_CONFIG_DIR`, `CODEX_HOME`, `GEMINI_API_KEY` | **CONFIRMED.** [agent_loop.py:1621](../../../project-trajectory/scripts/agent_loop.py), [1674](../../../project-trajectory/scripts/agent_loop.py). |
| Per-route homes are “already ruled” by OI-69 | **CONFIRMED WITH A SCOPE CORRECTION.** OI-69 rules dedicated homes **once retention is on**, originally per family—not a completed general multi-account routing design. [open-items.toml:2939](../../../docs/requirements/open-items.toml). |
| Route-selected homes survive retained launches | **WRONG if inferred from the preceding claims.** Retention overlays its own home over the route environment; that home is keyed by family. Two retained accounts of one provider would currently receive the same dedicated home. [session_service.py:164](../../../project-trajectory/scripts/session_service.py), [session_keep.py:316](../../../project-trajectory/scripts/session_keep.py). |
| This repo’s Anthropic rows set only effort; OpenAI rows set no home/env | **CONFIRMED.** [agents.toml:28](../../../docs/agents.toml), :37, :46, :55; OpenAI rows begin at [:58](../../../docs/agents.toml). |
| Plain, Claude, Codex and Opencode adapters; no Google adapter | **CONFIRMED.** Prefix registration and plain fallback: [session_adapters.py:798](../../../project-trajectory/scripts/session_adapters.py). |
| Grok route exists through opencode; FreeAI has no route | **CONFIRMED for this registry.** `OPENCODE-GROK` uses `opencode-go/grok-4.6`: [agents.toml:92](../../../docs/agents.toml). The registry contains no FreeAI or direct Grok route. |
| No `gemini`/`grok` CLI installed; opencode installed | **CONFIRMED for current PATH visibility**, not every possible installation directory. `Get-Command` found opencode, codex and claude; no gemini/grok. Recorded opencode installation evidence: [agents.toml:82](../../../docs/agents.toml). |
| `retain_for = ["disposition", "amendment", "red-tc"]`, and where it lives | **CONFIRMED.** Runtime config [docs/process.toml:291](../../../docs/process.toml); shipped template [:395](../../../project-trajectory/process.toml.template); Python default [session_keep.py:120](../../../project-trajectory/scripts/session_keep.py). Only `ADJUDICATE` calls qualify at [:516](../../../project-trajectory/scripts/session_keep.py). |
| The list originated on 2026-08-30 and later kinds were omitted | **CONFIRMED, with provenance qualification.** It originated in the filed **plan**, [retention plan:52](../../../docs/plans/2026-08-29-adjudicator-session-retention-plan.md), commit `232018f2`; executable/config implementation arrived in `b90e84b6` on September 28. Git history confirms first-approval on September 1 and consolidate on September 4. “Drift, not a decision” is the recorded direction; code history alone cannot prove owner intent. |
| `lease_wait = 120` | **CONFIRMED:** `120.0` seconds, [session_keep.py:544](../../../project-trajectory/scripts/session_keep.py). |
| `keep_for` returns `None`, rather than replacing the retained session under contention | **CONFIRMED.** Covers lease contention and store-lock contention: [session_keep.py:570](../../../project-trajectory/scripts/session_keep.py), :589–598. |
| `context_reset_pct = 0` means reset every call | **CONFIRMED behaviorally.** More precisely, retention is entirely inert; it does not retire/re-mint a stored session each time. [session_keep.py:15](../../../project-trajectory/scripts/session_keep.py), :125–126, :566–567. |
| Declared occupancy/template/version reset rules, same-artifact guard and clear-point retirement exist | **CONFIRMED.** [session_keep.py:365](../../../project-trajectory/scripts/session_keep.py), [:503](../../../project-trajectory/scripts/session_keep.py). Keep-warm orchestration exists at [session_service.py:451](../../../project-trajectory/scripts/session_service.py). |
| Claude fixture gives 48,267 / 1,000,000 = 5% through `ClaudeAdapter.context` | **CONFIRMED by executing the parser read-only.** Returned `(session_id, 48267, 1000000, 5)`. Version is in [fixture:1](../../../tests/golden/sessions/claude-stream-json.jsonl); result/model window in :5; algorithm [session_adapters.py:393](../../../project-trajectory/scripts/session_adapters.py). |
| Codex occupancy now works without explicit `CODEX_HOME`; opencode reports no window | **CONFIRMED.** [session_adapters.py:511](../../../project-trajectory/scripts/session_adapters.py), [:571](../../../project-trajectory/scripts/session_adapters.py), [:728](../../../project-trajectory/scripts/session_adapters.py). WI-787 is complete: [WI-787:14](../../../docs/archive/work/complete/WI-787-codex-occupancy-default-home.md). |
| Every kit session log carries usable role/provider/roster-row/commit-range evidence | **WRONG as a universal claim.** The cited WI-688 log has those values at [:11](../../../docs/iteration/wi-688-001-20261003-160206.log) and :39–42, but it is an **ADJUDICATE** example. Standard `call` rows do not derive commits: [session_service.py:342](../../../project-trajectory/scripts/session_service.py), :383–389. Existing standard logs also have blank commits/roster-row: [example:11](../../../docs/iteration/call_f97a5e23343d4d29a7ac020bd5af44ad-20260906-112054.log), :40. The proposed hand-path closure must provide complete attribution, not merely use `call`. |
| Snapshot refusal allows “amend-plus-flip is approval” | **CONFIRMED**, and this is executable semantics, not merely wording. [baseline_snapshot.py:1039](../../../project-trajectory/scripts/baseline_snapshot.py), [:833](../../../project-trajectory/scripts/baseline_snapshot.py). |
| `route_intent` uses `last_impl_family` | **CONFIRMED**, but “only loop memory” is incomplete: resumption can populate it from recorded BUILD logs. [agent_loop.py:506](../../../project-trajectory/scripts/agent_loop.py), [:3126](../../../project-trajectory/scripts/agent_loop.py), [:3049](../../../project-trajectory/scripts/agent_loop.py). This is still not attribution over all authors in `base..HEAD`. |
| `agent_route.select` handles tier, heterogeneity, cooldown, weights and preferences | **CONFIRMED.** [agent_route.py:719](../../../project-trajectory/scripts/agent_route.py). Heterogeneity is a preference with documented same-family degradation. Weight grammar exists in [agents-enabled:17](../../../docs/agents-enabled); current entries :39–46 are unweighted. |
| Composition is around `agent_loop.py:2580–2850` | **STALE/INCOMPLETE LOCATOR.** That range contains keep/launch/metadata/probe selection. Main route/prompt preparation begins at [:1620](../../../project-trajectory/scripts/agent_loop.py); execution/commit-range recording continues around [:3334](../../../project-trajectory/scripts/agent_loop.py). |
| `plan_runner` calls with a fixed template | **CONFIRMED per call, misleading if read as globally fixed.** It already selects planner routes from the enabled registry before supplying template/model to the service. [plan_runner.py:111](../../../project-trajectory/scripts/plan_runner.py), :147–153, [:173](../../../project-trajectory/scripts/plan_runner.py). |
| Risk 7’s three named dual paths exist | **CONFIRMED.** One-word fallback: [agent_policy.py:374](../../../project-trajectory/scripts/agent_policy.py), :391. TOML/CSV support: [spine_carrier.py:541](../../../project-trajectory/scripts/spine_carrier.py), [:708](../../../project-trajectory/scripts/spine_carrier.py), [:785](../../../project-trajectory/scripts/spine_carrier.py). Legacy OI `needs` reader: [kitlib/spine.py:204](../../../project-trajectory/scripts/kitlib/spine.py), [schedule.py:488](../../../project-trajectory/scripts/schedule.py); approved contract [TC-253:2629](../../../docs/test/test-cases.toml). |
| Prior classifier refusal of codex bypass flag, followed by successful bypass use | **CONFIRMED as recorded history.** [WI-541:105](../../../docs/archive/work/complete/WI-541-verify-retention-layer.md), :113–118; October 3 session [WI-688 log:39](../../../docs/iteration/wi-688-001-20261003-160206.log) and route command [agents.toml:71](../../../docs/agents.toml). This does not guarantee future classifier acceptance. |

**INCONSISTENCIES:**

- **Spine approval:** the proposed two-session author/edit/final-pass flow does not identify a non-author approver. Risk 6’s commit separation addresses chronology, not authorship independence. Owner item 1.
- **S10 “reviewers never”:** the owner explicitly describes a “dedicated retained reviewer” at WI:109–111, so permission to *design the narrowing* is present; it is not merely the coordinator’s inference. The note must distinguish an editing **author-review** role from ordinary reviewers, whose current commits may contain only their verdict. [agent_loop.py:2442](../../../project-trajectory/scripts/agent_loop.py). Final policy wording belongs at the checkpoint.
- **Families versus call kinds:** they do **not** map 1:1. WI:158–161 lists five retention families; WI:212–215 supplies example request kinds. `judge` is specifically an observation re-judge at WI:153, so it cannot silently stand for every `ADJUDICATE` call. REVIEW-A/B, CRITIQUE, DESIGN-CHECK and planner author/critic calls need an explicit mapping. This is **R**, because “such as” does not impose a closed five-kind interface.
- **Builder default:** the second pass settles it: capability built, shipped default **reset every call** (WI:171–179). The earlier “retained by default” must not be repeated as a universal shipped setting.
- **Risk 5 versus risk 7:** no necessary contradiction. Risk 5 explicitly permits a fresh, non-replacing session after waiting; risk 7 rejects additional robustness/legacy paths. Implement the timeout outcome through the same entry point. This also matches [SR-227:1710](../../../docs/requirements/system-requirements.toml).
- **This repo’s dial:** answered sufficiently for half 1: it may remain unchanged, and status explicitly says it stays off. WI:179; [status.md:70](../../../docs/status.md).
- **S11 overlap:** the approval flow cannot be described as settled S11 policy. That plan still lists seven owner questions, including approval in the authoring lane, resumed judging and final review. [S11 plan:317](../../../docs/plans/2026-10-03-s11-in-lane-adjudication.md). Reference those pending decisions; do not import its proposals as rulings.
- **“Nothing new is built” for attribution:** existing records can remain the source, but risk 2 overstates their completeness. The note must identify how the unified hand path obtains commit attribution, particularly when the coordinator commits returned work.

**RESEARCH ITEMS (R):**

- Provider CLI/version/auth/home/free-plan/stream research; FreeAI configuration once its identity is supplied; tested/untested presentation.
- Account declaration without duplicated model rows; home precedence; retention identity and reset behavior when accounts change.
- Complete phase/kind/family mapping, including PLAN, REVIEW-A/B, CRITIQUE, DESIGN-CHECK, all adjudication briefs and observation re-judges. Keep provider/model family distinct from session-role family.
- Reset thresholds, occupancy-unavailable rules, adjudication-kind inclusion and session-store format/location.
- Unified routing, retained-route priority over ratios, bounded lease waiting, coordinator communication and complete recording.
- Consolidation candidates and migration proposals. Retiring TC-253 behavior requires a proposed spine amendment, not silent deletion.
- Spine inventory: SR-222 covers recording; [SR-227:1705](../../../docs/requirements/system-requirements.toml) covers retention; [SR-154:706](../../../docs/requirements/system-requirements.toml) covers routing/independence. `sr_refs = ["SR-222"]` alone understates the expanded scope.
- Build slicing is **R**; no new owner decision is required merely to recommend slices. The recorded scope puts everything into WI-788, “with no new row.” [wave-9 log:294](../../../docs/log.d/2026-10-03-wave9-coordinator.md).
- Glossary wording/reference deployment. Keep proposed policy changes visibly pending checkpoint approval.
- Pause effects are already decided: retain the pause; half 1 proceeds through a coordinator, not an unattended claim. [status.md:42](../../../docs/status.md), [:73](../../../docs/status.md). Live loop validation would need separate authorization to lift it.

**SPEC HYGIENE:**

- **The machine-readable Deliverable is empty.** `## Context` comes first at WI:13. The parser clips everything from that heading onward, so Done-when and every subsequent ruling disappear from the registry cell. [registry.py:374](../../../project-trajectory/scripts/kitlib/registry.py). Read-only parsing returned `Status="queued"`, `BuildTier="strong"`, `Deliverable=""`.
- **The trailing `## Deliverable` at WI:284 is empty and ineffective.** The structural correction is Deliverable first, containing operative acceptance criteria; Context afterward.
- **Expanded acceptance criteria sit outside Done-when.** Its same-level successor heading at WI:90 ends that section. The reader stops at same-or-higher headings: [registry.py:252](../../../project-trajectory/scripts/kitlib/registry.py). Direct extraction found 35 Done-when lines; the later glossary, family, entry-point and risk requirements are excluded.
- Queued status and strong buildtier are correct. WI-787 is complete. The remaining parser and acceptance-placement issues are mechanical corrections, **R**, not reasons to ask the owner for permission.