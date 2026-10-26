# WI-976 dispute sitting at 095bb79

DISPUTE: findings=F1

## F1: the sample review record gives no reason why further splitting stops

**A disclosure first.** This session wrote the record under judgement, sitting 016's verdict, and the earlier verdicts the finding cites (011, 012, 015). I agree with the finding against that record, so the ruling serves no interest of its author. The coordinator may still prefer a different hand for any re-inspection the successor brings.

**The finding holds at this range.** I checked both sides:
- The sample brief (`016-ADJUDICATE-9d6ad4c.brief.md`, lines 644 to 649) asks the sitting to "record the stopping boundary in the existing scoped review ... when further splitting would only paraphrase or duplicate, record why the decomposition stops there".
- The sample verdict (`016-ADJUDICATE-9d6ad4c.md`) has no such sentence. The only matches for "split" or "stop" are in a quoted row cell. The verdicts it carries forward (011, 012, 015) have none either.

The reasons the reviewer found are about other things: a carrier (LLR-183's "would duplicate review facts"), a retirement (LLR-297) and a duplicate successor row (sitting 010). None is a stopping decision for the retained chain. The finding is TC-211's Inspection result, recorded as a fail (`docs/test/observations/TC-211.2026-10-26T071924Z.toml`), and it found no purposeless child. What is missing is the recorded reason, not a sound decomposition.

**It is not convergence-class, so SUCCESSOR is open:**
- *Not a fail-open:* nothing gates on the record's content.
- *No data loss:* nothing is lost.
- *Not a Done-when gap:* every TC-211 item holds. The sample was composed with the hat block, its brief is committed beside its verdict, the verdict names each applicable hat's outcome, and a fresh session inspected it after the acts and recorded the result through the observation writer and in the procedure. The Done-when asks for that inspection and its record, not for a pass.
- *Not this lane's change:* the clause the sample fails is SR-186's stopping-boundary criterion, which WI-976 does not change. SR-161's part, every applicable perspective's outcome named, passes.

**Why SUCCESSOR and not FIX.** The omission is systemic, not a slip in one record. Four whole-set verdicts in this lane, all written by this session against briefs carrying the same instruction, left it out. The cause is that the verdict's stated form, one line per row plus the machine line (and now one line per hat), has no place for a chain's stopping reason, so a sitting answering the form exactly drops it.

A FIX here would be one more re-sit over SN-036 with a stopping paragraph added, which would move TC-211's Inputs again and need another act and inspection. That would turn this sample green while leaving the next decomposition round free to drop the reason the same way.

The remedy that removes the defect gives the stopping boundary a named place in the decomposition-round brief, as the hat outcomes now have, and then re-inspects TC-211 on the first record that carries it. That touches the shipped sitting templates and their composer's round block, a change to every adopter's briefs. It belongs in its own row, not in a lane whose Done-when is met and whose landing already waits on SN-036's owner act.

Until then, TC-211's fail stands honestly as the observation of record. That is what an inspection result is for, and its release trigger will ask for a passing sample before any release.

RULING: F1 SUCCESSOR give a decomposition round's sitting brief a named stopping-boundary line, beside the hat outcome lines, that asks the verdict to state for each retained chain why further splitting would only paraphrase or duplicate, test that the shipped templates carry it, and re-inspect TC-211 against the first completed round whose record carries it, recording the observation
