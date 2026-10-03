# Sonnet cross-review — spine-acts batch N, round 1 (build/wi-766 at eb709653)

Reviewer: Claude Sonnet 5.5 (read-only). Verdicts by an independent Claude Opus 5.5
adjudicator: WI-766 (amendment) `MEANING rows=9`, re-attesting nothing (SR-215,
LLR-254, TC-248 not blessable); WI-767 (first approval) `RETURN rows=4`.

eb709653 NOT YET SOUND

The verdicts and findings hold; the Dispositions drafts are not actionable as written.

**MAJOR**
1. The WI-766 draft's re-adjudication cannot re-anchor the six blessable TC rows:
   the successor's merge mints amendment scope only for the rows it changes, and a
   scratch `snapshot --reattests TC-248` refuses naming TC-036/055/209/210/211/247.
   Nothing orders the WI-767 successor after the WI-766 one (LLR-254's drift blocks
   the LLR registry's first-approval copy too).
2. The stage-gate question is deferred in a circle: WI-766's draft hands it to
   WI-767's successor, which hands any SR-215 narrowing back; the WI-767 bullet is a
   three-way fork naming no surface.
3. The WI-766 draft keeps "rubric" in SR-215's acceptance and Rationale, so the trace
   finding it cites (`_CRITIQUE_INSTRUMENT_RE`) would not clear; LLR-294 rests on that
   clause unstated.
4. The WI-766 verdict records TC-247's dropped naming check yet would bless it; TC-247
   is LLR-254's only verifier for "names the case, reason, rubric and changed inputs".

**MINOR**: "label it derived" not actionable, no replacement Title; LLR-254 dropped
"its title carries the case id and the digest prefix"; "no gate surface names that
command" overstates (PROCESS.md:807 and RESYNC_PACK.md name it; nothing prompts it at
the gate); TC-307 is the weakest return (cost-free, same lane reworks LLR-294).

**Verified:** only review files and specs changed (`git diff 30ee386b..eb709653
--stat`); both `WI:` trailers parse; both verdicts in the brief's format; both
Dispositions parse; every RETURN/would-not-bless finding confirmed against the
registries and code; TC-279's handling correct; the snapshot refusal reproduced on
a scratch copy. Coordinator note: M1's "the brief will not show them" holds for the
merge-minted scope only — `amendment_values` renders the row's `adjudicates` cell
intersected with the drifted model, so the coordinator carries the six rows in.
