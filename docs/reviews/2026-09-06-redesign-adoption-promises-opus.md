# redesign-adoption-promises — adversarial review

Requested route: Opus 5, high; declared CLI stream-json pattern.

Subject SHA256: `370d932df3ae56396204bf450d2e9a6de094b28dee9f87cd4f45a4a55d1078a4`

Tracked invocation: [session log](../iteration/call_3ce5bf5dfbe146cb8c045170c292e405-20260906-094934.log).

Review uses supplied source with tools disabled. It is an independent
assessment, not a requirement approval or a test execution.

# Adversarial review — adopter revalidation + objectives + charter edits

**Verdict: CHANGES_REQUESTED** (four findings, all small edits; no new framework, registry, blanket review or string tests required)

## Findings — defects of this diff

**F1 — §1(a) is a net deletion, not a consolidation.** `project-trajectory/skills/spine-authoring/SKILL.md`, §1(a). The rewrite drops (i) the only mention of the roster's location (`docs/requirements/hats.toml`) anywhere in the skill, and (ii) the description of what `hats.py audit` actually prints — the SN × conditional-hat matrix, the needs waking no conditional hat, and **each hat's reach count**. The new section calls the audit "a worksheet" but never says what is on it. The reach count is the mechanism for case (7); deleting it while adding prose telling the reader to "check the real brief" removes the instrument and keeps the exhortation. Restore the roster path and one clause naming the audit's three outputs; the rest of the compression is fine.

**F2 — CONSISTENCY broadens while its justification and its instance clause go stale.** `docs/requirements/hats.toml` and `registries/hats.template.toml`, CONSISTENCY. (a) The instance drops *"a rule the template states one way and the instance another"* — the template-vs-instance axis (the lens over `test_dogfood_sync`'s subject). The replacement list — requirements, interfaces, policy readers, user surfaces — does not name that axis, so this repo loses a lens nothing else carries. Restore it as a fifth item in the instance's `listens_for`. (b) The comment immediately above both charters still argues CONSISTENCY as the *surfaces* hat ("Nothing else here asks whether two surfaces agree… the UX pair asks about ONE surface's…"). The charter now reaches contracts and readers. This is the skill's own method-flip sweep failure (§4, §5 "acceptance rot"): the cell changed, its neighbour did not. Same check owed on PERFORMANCE, whose comment still frames the collision as SN-012 right-sizing while the charter now reaches operating cost.

**F3 — FIRST-RUN-ADOPTER now carries two audiences, five questions and an unsupported obligation.** Both `hats.toml` files. `asks` bundles the stranger test with customizations, policy meanings, accepted evidence, unfinished work and *"how is the upgrade completed or reversed"*. Three problems: the hat's name no longer matches its content (an existing adopter is not a first run — CONSISTENCY's own charge); a charter answering five questions cannot be answered per row; and **reversal/rollback is a new obligation no need in view demands**, which will mint derived rows with no parent (§2(c), §5 "underivable-from-any-input"). Also, the predicate still fires only on `scripts`/`templates`/`process` — an upgrade that changes a *policy meaning* on a registry-tagged row never faces the question, so case (2) escapes the very lens this edit adds. Recommended: keep the stranger question; carry preservation-of-project-owned-content and accepted-evidence as the second clause only; drop "or reversed" unless a need states it; widen the predicate or accept the gap explicitly.

**F4 — O1–O6 are unwired, and may duplicate the vision's one home.** `README.md`. Six anchors are minted and nothing cites them; the skill's own §5 "unwired marker" asks *which checker, gate or brief changes behaviour because of this*. Either cite at least one anchor from where a reader acts on it (the new SKILL section, or ADOPTING's revalidation entry), or keep the prose and drop the `<a id>`s. Separately, verify against the `PROJECT-VISION:` tag above them: O1/O3/O4 read close to the tag's maintainable/trustworthy/approval-gated phrasing, and a decomposition that restates its parent is the paraphrase this repo forbids. Not blocking if the tag is genuinely broader — but check before merge.

**TEST-ENGINEER** is the one charter I would take as-is: mechanical→four-method is alignment with `docs/process.md` §4 and §3's `Attest` rule, and "hides its limits" is a real, previously unowned failure. Minor: it now overlaps PERFORMANCE's new "reported as a reliable total". Keep one home — I'd leave honest-limits with TEST-ENGINEER.

## Cases

| # | Disposition guidance gives | OK? |
|---|---|---|
| 1 | New hat only if no suitable owner; seed roster proves nothing; item 4 forbids copying the kit's own hats/needs/objectives into the product | ✅ |
| 2 | New-SN proposal → §1(a)–(e) intake → affected SRs | ✅ except F3's predicate gap |
| 3 | SR amendment, not a new need; label derived + `Hat-Refs`/`Rationale`; anchor the interface by registry **id** (frame §), re-attest the amended row only | ✅ |
| 4 | "A sound requirement violated by code needs a fix, not another need" — explicit; new LLR bullet separates mechanism-caused from code-caused | ✅ |
| 5 | Resolve inbound Hat-Refs before removal; re-point or empty the cell (§2(c2) "subject is gone"), same commit. **Gap:** item 1 covers *removal* only — extend the clause to refine/condition, since this diff itself broadens four charters that existing rows already cite | ⚠️ one clause |
| 6 | Scoped "no semantic impact" with a reason; no whole-spine rederivation. Proportionate. Name the existing home for that conclusion (the re-sync commit, per §1.2) so it isn't itself an unwired claim | ⚠️ one phrase |
| 7 | Repair predicate or declare the tag via ordinary review; no prose inference. Weakened by F1's deletion of reach counts | ⚠️ see F1 |
| 8 | "Rejected proposals leave authoritative content intact" — clean | ✅ |

**Authority:** preserved. Nothing here lets a lane flip `Status`, re-seed snapshots or cancel work; "preserve previous approvals as history" should cross-ref §5's last bullet so no lane reads it as licence to write `docs/archive/last_approved/`.

**Scope:** the SKILL section and ADOPTING/RESYNC entries are proportionate one-home pointers, not a migration engine. The smuggling is in the charters (F3, F2) and the unwired objectives (F4), not in the procedure.
