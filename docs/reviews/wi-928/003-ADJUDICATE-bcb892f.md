# WI-928 adjudication 003: amendment of LLR-300 and TC-339

I judged the two amended rows at `bcb892fc4`. Since the anchor (`87ceeafea`), the LLR and TC registries moved only in these rows. The LLR and TC rungs are released (`human_approval_through = "DevStg-Boundary"`). Every test TC-339 cites exists.

**The scope the change rests on:** the work item's Context records the owner's ruling (D-011) that the blackout hook grew forms for findings no agent or supported route produces.
- **The forms dropped:** a model call in a here-document's or here-string's substitution; a PowerShell assignment to a property, index or typed-array target; dot-sourcing; `time -p`; `coproc`.
- **What the ruling keeps:** the quote-aware reading and the ordinary `$r = claude -p x` capture.
- **Why removal reopens no kit route:** every kit-owned launch point already refuses inside an armed window, by construction (session-service admission, claim routes, keep-warm, `window-check` in coordinator launch scripts). The hook covers only a CLI an agent types straight into its shell tool, a stop that WI-834's ruling (f) made encouraged, not enforced.

## amendment

- [MEANING] LLR-300 Detail (the shell-reading sentences; every other clause verbatim) -> the hook denies a model CLI as read by a quote-aware reading that also:
  - treats a PowerShell assignment to any target (property, index, array type, scope, chained) as running its right-hand command;
  - reads substitutions inside unquoted here-document and double-quoted here-string bodies;

  and `window_check` exits nonzero "inside it" -> the reading keeps quoted values, separators, comments, and here-document and here-string bodies as data. It finds the command word only after leading assignments, the timeout and env prefixes, reserved words, chain operators and the call operator, and in substitutions written in the line or inside double quotes. It reads only a PowerShell assignment to a variable as running its right-hand command. It states that a form outside this list has no dedicated recognition and carries no guarantee either way. `window_check` exits nonzero inside an armed window ->

  denial narrowed: a model call in an expandable here body, or assigned to a non-variable target, was denied before and is not guaranteed now. An implementation correct under the new text could fail the old one. **Blessed.**
  - **Upward:** SR-229 and SR-237's blackout close-down is met by construction at every kit launch point. The hook's remaining duty is the forms an agent actually writes, which the kept list covers, and the owner ruled the dropped forms contrived.
  - **The bound is now closed and honest:** an enumerated set of positions, plus an explicit statement that anything else carries no guarantee. That replaces the open-world "any command word" promise that produced the churn.
  - **The kept denials are unchanged:** unreadable lines, and Agent and SendMessage calls.
  - **"inside it" became "inside an armed window":** a clarification of the referent, and no carrier is added.
- [MEANING] TC-339 Expected and Method -> verify denial of PowerShell assignments whose right-hand side runs a model for any target form (property, index, array type, scoped, comma list, chained, operator spacing), and of expandable here bodies that launch a model, with literal bodies allowed -> verify assignments to a variable only (plain, typed, scoped, comma list, compound operator), with here-document and here-string bodies allowed as data -> the verification set matches LLR-300's narrowed reading. **Blessed.** It drops exactly the forms LLR-300 drops and keeps the quote-aware, variable-assignment, quoted or variable right-hand, unreadable-line, close-down and route-registry assertions. Its cited tests all exist.

VERDICT: MEANING rows=2

**Aftermath:** this session re-attests both rows on the released rung, in their own act commit:

`python project-trajectory/scripts/intake.py snapshot --reattests LLR-300,TC-339`

SITTING: JUDGED kinds=amendment
