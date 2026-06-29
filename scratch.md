Other scratch notes:

How can AI tools handle multiple repositories?  How can they create new repositories for new modules?

Best ways to handle end-to-end testing?

AI tools can handle multiple repositories by implementing a centralized management system that allows for easy navigation and integration between different codebases. This can include features such as repository linking, dependency management, and automated updates across repositories. Additionally, AI tools can utilize version control systems to track changes and ensure consistency across multiple repositories.

Other AI skills to utilize?  Other guardrails to contain in claude.

What about documentation gaps / requirement clarity?  Ideally a mind map or other diagram would break user needs into individual components.  Ex User need - SR - LLR.  Could that be HTML for easy browsability?  Other alternatives?  Ideally that would be generated.  Can this be regenerated at each gate?

How to emphasize infrastructure needs?  Ideally documentation / traceability is all done with the same toolset (probably python since it's already done here), but other testing for the actual deliverables is dependent on the language it is developed in to an extent.  How can that segmentation be better clarified?

How to encode general directives into the claude.md file, the items below would likely beneficial in all general cases:

1. Ask, don't assume. If something is unclear, ask before writing a single line. Never make silent assumptions about intent, architecture, or requirements. When running unattended, pick the most reasonable interpretation, proceed, and record the assumption rather than blocking.

2. In general: Implement the simplest solution for simple problems, better solutions for harder problems. Do not over-engineer or add flexibility that isn't needed yet. However, the simple solution should always be viewed in terms of the overall scope, care should be taken not to shoehorn in a reusable / simple method if it will actually produce complex architecture to work it in.

3. Don't touch unrelated code but please do surface bad code or design smells you discover with me so we can address them as a separate issue.

4. Flag uncertainty explicitly. If you're unsure about something, see point 1 above. If it makes sense to do so, conduct a small, localized and low-risk experiment and bring the hypothesis and results to me to discuss. Confidence without certainty causes more damage than admitting a gap.

5. I'm always open to ideas on better ways to do things. Please don't hesitate to suggest a better way, or one that has long lasting impact over a tactical change. (as a few examples)

Finally, are there places where hooks would be more appropriate than claud.md directives to ensure execution?