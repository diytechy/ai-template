# OWNER_SCRATCHPAD — the human owner's private notes

> **For the human owner only.** LLM agents: do **NOT** read, index, summarize,
> cite, or act on anything in this file. Nothing here is a requirement, ruling,
> or working surface — those are `docs/status.md`, the registries under
> `docs/requirements/`, and `docs/log.md`. Notes here may be old, contradictory,
> augmented, or not yet fully formed, so none of them is direction. The always-on
> **secrets floor still scans this file**, so it is *not* a secrets-safe zone —
> do not paste credentials or tokens here.

---

<!-- Owner notes below. Free-form; nothing here gates a commit. -->

Does the readme 
Different topic:

We should able to fall back at any point to G1 without loosing attest confirmation on certain artifacts, because it's possible new content will affect implimentation.  We don't want to force the full run through G3 just because a new phase can capture new content.  Ideally there would be a way to attest / ratify the current G2 content (SN / SRs) and then back off.  Again, it seems most of this is there, but it should be as simple as moving the gate back to 1 but keeping individual items in a confirmed state.

Only one more question - should we explore showing the phase in the when (roadmap DAG) in PROJECT_STATE.html in some way?  By color, parent grouping, or other option?  I think this needs to be clarified in the requirements, and it can be mapped out as a new work item.

The when view should start with the phase blocks if there are more than 3 phases.  They will look like a simulink flow diagram, where the user can click into the block to explode the view and would follow the lower level views: If there are more than 3 work streams, show the workstreams only and allow them to be clicked also to explode into their individual work items.  Connections should be inherited for parents based on children connections.

The how view should start with the component blocks if there are more than 3 components.  They will look like a simulink flow diagram, where the user can click into the block to explode into their individual software module items.  Connections should be inherited for parents based on children connections.

************************

My concern with both of these approaches is they assume we understand what previously gate-cleared requirements might be impacted.  Perhaps it would be better to rethink the monolithic gate approach.  There are basically approaches: Parallel and series.  In parallel, each gate is approached.  We build out the core requirements, G1, then everything proceeds to build out detailed requirements and test cases, G2, and then full implimentation and sign-off at G3.  Ironically, work-items tend to be focussed on series channelling.  Each work item is run through to completion from G1 to G3.

Ideally, the repository gate state would be derived from it's artifacts (back to SSOT), each SN has it's state indicating draft or ratified with a date, or some other form.  Each SR/LLR/TC already has a state that could represent draft indicating it hasn't been ratified yet.  Then the repository gate is derived from it's artifacts, not some other definition.

The 2 challenges I see:

1. Phase definition will become murky, but it probably be derived at each gate.  If we move forward in a gate, don't change the phase, if we move backward, get ready to rev the gate.  So we can always derive from the previous repository state and where it is going.  Fundimentally phases don't have any meaning, they just help to break things down in time, but this can then be conflated with campaign.  Campaign is night for a set of new work, but if other work leaks in phases are better.

2. When piping in content as work items, the injest should change.  All work items that are open and not deferred and moving the gate back would mean we need to start a new phase, and that can just be a special work item as [phase]-[g*] where it's g1 or g2.  That means all pre-dev gates (requirement structuring) can be done together to help prevent conflicts or see where somethign just ends up getting modified.  Once G2 on that phase passes, the work items run through their development.  This would also be compatible with attended / autonomous / single-ratify ensuring reviews for a single batch of changes are minimized.


************************

Related to agent driven loop:
How do multiple workstreams run in parallel when there appears to be a single docs/run-phase document?  Wouldn't this have to be per workstream to avoid thrashing between streams?

Can we add claude and opencode as required dev tools (setup-dev) on this repo and then add the latest openai model sol, terra, and luna as the latest strong, medium, and quick agents in the csv list to be executed through opencode? Likewise prompt the user to sign into open-code if all those models fail when called.

Similar for claude, and perhaps there needs to be better failure context.  Specifically for claude we should be setting the effort level to high or very high as a good balance, perhaps computing this could be a part of a future update and kept as a deferred work item for future reference - that is to add scripts or methods to select the proper effort level when applying a claude level agent.

######################

Now does setup-dev properly only install items that need to be installed?  I want to test it from this machine but I don't want it to try to initiate installs that are not necessary.

**

Can you verify the calls through agent-resume can properly access each model already defined in this repository?  (Claude fable, claude opus, claude sonnet, Codex / Open AI Sol, Codex / Open AI Terra, Codex / Open AI Luna)

************

Additions:

On resync, we should also stress to odopters to recheck if there are updated / newly available skills or knowledge packs that should be adopted as well.  Since resync will also result in the new gate derivation methodology, resync will require stakeholder need verification to be derived based on the stakeholder needs that were present at gate bump (from commit history)

One important distinction related to the derived gate updates, this means work items should always get processed to their G2 level before implimentation starts.  This means running be default from status.md should verify all G2 processes are met before implimenting code, and either go through those processes in autonomous mode, or tell the user to close the open items before proceeding to implimentation on work items.  If a user specifically asks for work items to be implimented of course it should be honored, but resuming from status should try to ensure G2 is passed so conflicts between implimentations are minimized.

Related to the readme:

Does the readme show the config options for the repo and the opt-in vs opt-out options?

Related now that we have the gate rederivation complete, is that readme and other documentation up-to-date?

Should we drop in open code or emphasize it's capability as a multi-model provider?

***********************************************************
Is dropping the per-commit full test already in the work-item backlog?  It looks like hundreds of test cases are still running each commit.

Instead of doing reviews each commit, should the basis just be doing 2 adversarial reviews at the end of a campaign?  If the test cases pass, that should probably protent generally against issues.

Should we flip build to be medium and review to be strong if they are delayed?

*****************************

Update the plan so that WI-122 is the first one to land, to speed up iteration.

Is there a way to restrict CLI envirments to only allow writes within the repository as a restrictive / protective measure?

******************************

Might there be times when an explicit plan stage is unecessary in agent-resume?  If the spec is documented sufficiently, it doesn't need to be replanned.  Perhaps work-items should be pinned to a teir for it's build at creation, and also contain a flag if additional planning is required.  If the plan / spec is detailed enough, no need to spin up another agent.  This could also reduce spinning up dedicated sessions for planning and building that will already hold much of the same context.

I notice in visual code using claude code, I can complete multiple work items in a single session, but often when running agent-resume it seems only 1 work item is pulled per session, resulting in signficantly more session spin ups / context re-uploads / etc.  Is there a gap with how work-items are grouped and aggrigated for a session?  Is the method being used too concervative?

*******************************

IMPORTANT: It is possible some of these items are already covered by some work items.  Take care not to duplicate queued work.

1) All the flow diagrams in PROJECT_STATE.html need some work.  The work-items that iterate here should have critiques around accessability, UI uniformity, and other interface usability standards.

1A)
Need to adjust the process maps, / diagrams shown in PROJECT_STATE specifically to show how injest occurs and interaction with open items and human.  This should show how the two circular processes:

[LLM_Agent] - Any AI agent recieving feedback in the repo context should follow the processes here to review user input and determine next actions.

[From LLM_Agent] -> 
A2. New items are converted to work items with spec details if necessary -> [HERE SHOW THE RESUME LOOP]->[Back to A&B_Merge]

[From LLM_Agent] -> B3. Open items list is populated, including gate ratification table, B2. Human reviews open items and gives feedback -> [Back to A&B_Merge]

1B) Architecture decomposition - columns can be much narrower, and each parent should have a horizontal arrow going to it's child.  Highlights can stay on the last item hovered over (instead of removing the highlight as soon as the cursor gets off the item, which tends to cause flashing-like behavior)

1C) Software architecture and Work-item trajectory should present like simulink diagrams, where interfaces connect to the inputs / outputs / finals.  I believe this may already exist as a work item, but it is very important that the visuals are crisp, and ideally that double-clicking on the item brings the user into a deeper layer.


2)
While agent-resume is running, is it possible for each workstream to just update it's latest line on the console (so, intead of a long rolling window, each workstream continues to update it's status in a line that gets continuously updated.)

3)
Other noticed items: The logs (in /docs/interation) and reviews don't appear to be committed with the rest of their content (instead they sometimes get bundled with a later commit), iI t would be good for them to be part of the code commit for reference.  Should the reviews and logs include the work item key name in their label / filename for tracking? 

4)
Do we need "hats" to be allocated to specific SRs to be spun up during related development?  Or how can we ensure test cases / and specifically critiques are triggered appropriately for the right content.  Ex: If a work-item is building UI, how does the resume-agent chain know to wear a UI hat to evaluate the UI for accessability and readability?

5)
Is there anything from this repository that should be considered? ==> https://github.com/PiLastDigit/TRIP-workflow
I think this flow already contains everything, but perhaps the big benifit here is stress on research.  In my mind that should be part of the plan phase.  I'm not sure of the best time to run this (before creating work items?  When actually ingesting work items?  Both?) but I think the emphasis on research and spinning up mid-tier agents to find online information would be very valuble, so long as the research findings are looped back into the knowledge kits (which I dont' even recall where those are stored).

6)
My other concern here is specs.  The intent of the specs was to actually hold specs for component and module-piece information that could point to knowledge packs and draw the what with the how with greater detail.  Right now most of the specs are just work items that get archived, and ultimately create risk of duplicating analysis through work-item iteration instead of collating the defined expectations for modules into their respective chunks, and updating those as new work items come in and act on the similar layers.

Please commit all the unstaged files, even if they were edited by me.

***********************************************

IMPORTANT: It is possible some of these items are already covered by some work items.  Take care not to duplicate queued work.

Then go through the following items:

1)
Related to open-items.md:

OI-8: I want to see the heirarchy here.  Whenever there is a G2 or G1 ratification, I want to be presented with the heirarchy / tree of each SN -> SR -> LLR so I can review the prose and the associated breakdown.  What restrictions / checks can be put in place to gaurantee that view?

OI-9: Many pieces of feedback here,  Research should probably be a strong teir that spawns off lower teir agents to actually gather information (basically, I would expect it to run as a small coordinator, deciding which context to dig further into spawning directed agents).  I would ask that knowledge packs be turned on for the meta repo as well to excercise it.  I don't recall, how does each component store / alllocate against implimentation?   Does it contain SRs / LLRs?  That is -if components are what tie the what to the knowledge which supports the how- that web needs to be robust.  I think in that case if knoweldge packs are enabled for a repository, there needs to be a check that ensures each implimentation module (again - is this an LLR and SR?  Some other way to define it?) is tied back to a component.

This actually ties in to another question I had: Should some interfaces be defined at the same time as work items to define how work items connect?  Aren't we effectively building out arcitecture changes when breaking items into work items or defining where their content should likely be implimented?  And does this influence OI-8 where the heirarchy of the software arcitecture should be containerized by components and traced / connected by their connecting interfaces?  Note I would expect interfaces to also define their start / end points if it is external to the system.  For this meta repo, that would include various files that are created / generated, and the input mainly from the user, and many of the files themselves become circular references that are both edited and are ingested.


2)
Explore: the build / research tiers also need to be optionally configurable with a preference set so it always prefers a certain designated model for certain tasks.  Ex: Research and plan should always attempt to use fable, else another teired model if not available.  Build should always attempt to use opus.

Related: Opus implimentation should be set to extra high.  Are there effort parameters for openai?

3)
When deciding on work items, always clear work items that affect the lowest gate level first, this prevents implimentation from potentially having to go through rework.  This would then prompt a "Needs Human" to ratify the relevent gates.

4)
Allow method to pause using key or other method during agent-resume, all coordinators wrap up what they are working on and pause at a clean state.

Setup a pause period where the coordinators do the same action based on a weekday pause configuration.  Default: Weekdays Noon UTC to 7:00 PM UTC are blackout times where no coordinators will start new work.  This prevents execution of work during peak hours through claude agents.  This would be always on but time gate configurable for weekdays.  If the blackout start time is the same as the end time, it would be disabled.  Default should be as described above.

5)
What would it take to convert a prompt into an image (like a black and white image with text) and feed that into the agents?  Many agents apply different tokenizers to image processing such that this might actually be more efficient.  Can this be added as an opt-it behavior?  It may require a specialized tool though to "print" a prompt to an image, and then hand that image to an LLM agent.

6)
What does this design system introduce that this framework doesn't currently contain?  Does it have anything that should be / could be leveraged here?  It seems to be focused on UI related design, but that might still have some relevence (most projects need a front end, and often time those front ends are lacking in style), but it's process backend might also have something to leverage ==>
https://github.com/jrpease/throughline

7)
Coordinator should have some inferencing capability to drop down to a lower teir planner if applicable.  This may have already been implimented, but it should be able ot autonomously determine if the preferred higher teir model (fable in this case) is really neccessary.  And if not - The plan and build cycle can be done with the mid-tier preferred builder.

8)
Can this template / kit provision knowledge kits for downstream adopters to consume?  There are updated knowledge definitions in "C:\Projects\ClaudeGuardChecks\skill-knowledge-library"
~~~~~~~~~~~~~~~

Some additional feedback, but again note it's possible some of these are duplicates:

1)
Can we update the cli for open ai to actually use the provider cli instead of opencode?  It seems sometimes opencode does not respond, it will be curious if openai / codex cli interfaces work better.

Related please set the builder preference to Codex Sol for now.

2)
It appears there are many times work items could be taken in parallel but are not.  Is there a setting in this repo preventing that?  If a work item's dependencies are all complete and there is no risk over overlap with another work-item already being actively worked on,  the work item should start getting processed.    Parallelization should be emphasized here for development speed.

3)
Related to speed and optomization, there should be a method to let a critique level run an "infinite" number of times until an acceptance criteria is met.  Right now is the max number of critique iterations a global definition?  If we run through the max number of iterations in general it is good to move on, but there may be some special cases where it needs to become a blocker for a human to reeview.  So, default would be to move on, but is there a provision to block?  For iterative / optomization processes themselves it would be good to do some research here so this template has a good approach to exploring problem optomization.  How to lay out solution spaces, select samples, cross-polinate, etc.  Additionally, there may be times the agent should construct a conventional optomization / minimization loop around training variables instead of iterating on the LLM itself.  It all depends on the problem.  

4)
The "Process" UI is also showing the working loops (4A and 4B) as just straight lines, but this should be rendered as two actual circular loops that intersect on the LLM Agent feedback from the user.

~~~~~~~~~~~~~~~~~~~~~~

1)
Is status.md even necessary anymore?  If work items in the csv carry their dependencies, blockers, and readiness state, can the work items to be executed be derived?  But of the key concern, how are two work-items with interdependencies handled such that they are not scheduled in parallel?  Or shouldn't that already be worked out because of the dependency relationship definition.  Multiple related work items should be able to be consumed at once.  In the most recent run, all work occured in series from agent-resume.cmd, but I really want to take advantage of parallel development where possible, what design changes can be made to this template repository to help push the automated development cycles kicked off by "agent-resume" toward more parallel development?

I further question if defined parallel tracks are even necessary.  They do help to catagorize work-streams, but the parallization likely does not need to rely on them.  Parallization can be derived, each time a work item is queued and no dependencies are open, it can start a new development branch.  If it has exactly one dependency, that next work item can be pulled into the same branch, each iterating until they get to the end of the series sequence (End of series sequence means there are 0 or more than 1 work items that depend on the current work item, or the single work item that depends on the current work item also depends on another work item that is not already in the main branch).  Once at the end of the sequence the dev branch get's merged by an integrator.

This allows multiple work items to automatically queue up in dedicated dev branches, getting merged in when needed.  The integrator would need to handle potential conflicts, but most of those should be trivial (like test case adjustments), it relies on work items being defined with correct dependencies to avoid merging conflict pain.

Or is there any other research that might indicate other ways to do this?

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Feedback:
1) Agreed, but this is what allows for faster development.
2) Agreed.
3) Agreed, this parallization will be less advantageous for this repo, it's intended for much larger adopters, like the gilbert repository.
4) Isn't the DAG computed before commit?  Is there something that needs to be done to build confidence?
5) I'm not following, can you give an example?
6) This is interseting, why can't batches of series WI be consumed into a single train?  Is it just a matter of flushing out those requirements?

Related to gaps:
docs/run-phase - Do we even need run-phase anymore?  Perhaps this makes this effort distinct.  Phases are not all that important, they help to substantiate new requirement intake and build out changes in a timeline, and that probably still can happen.  If a work item happens to bump the phase in it's iteration branch, that's fine, but then the integrator should take / prefer the biggest phase bump it sees at merge to help emphasize a phase bump occured.  Phases in that way can be completely derived from the workflow, and completely deleted from registries.  This also means multiple campaigns can run in parallel if they are isolated from one-another.

Agreed upstreem adopters will flip to parallel - it will be a good excersize of the framework.

"Material integration edit forces re-review" - Explain specifically what "Material integration" is here, any content getting merged?  How does that translate into a coin flip?

"Train-branch and integrate-branch proliferation." - Agreed, maybe that's a rolling check like the push check, see how many LLM branches exist that are older than 2 days, and recommend cleanup.  This could be automated in the future, but for now I tend to think it should be intentional from the human side.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

From work-items: Remove Workstreams, it should not be needed anywhere.  The phase groups / clusters things that occured in similar history.  An alternative is campaign, which even that might not really hold any value.

Explain Exclusive keys / new edges human-ratified?

And please re-expound on the 2 open items again.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Exclusive keys / new edges - But by then the work items are already done.  It would expose poorer planning, but I don't think it's something a human could ratify after the fact, it just means the planning / work item setup stage did not properly allocate resources.  Agreed the dispatcher can't change the allocated resources, all it can do is record the conflict and be reviewed in post to understand why the resource allocation to the WI was incorrect / underestimated.  Agreed it will continue causing conflict until it is resolved, but I don't see a better method, forcing human intervention due to some collitions would not be preferable in my opinion.

For open item 1 and 2,  let's take a step back on the iteration sequence.

1. Campaign should not be used to schedule workflow.  It should only be an attribute of a work item.

Then let's talk about the agent-resume behavior.

A: When it starts, it should make sure all /llm branches are at a merged state, if not it means it needs to get things to a clean state.
    a: To get to a clean start, it should only execute open llm branches until they are merged into the current main development branch.
    b: Any traincar scehdule is deleted after this, it might be out of date now if new work items were added.

B1: Next, any work items that affect G1 are completed as a single large item.  These need the scope of the whole project anyways, no reason to complete these as a single work item.
B2: If ratification is required, the process exits because ratification is required.
B3: Next, any work items that affect G2 are completed as a single large item.  These need the scope of the whole project anyways, no reason to complete these as a single work item.
B4: If ratification is required, the process exits because ratification is required.

Then it moves into a fresh build-out plan.

C: It kicks off a work-advisor / schedular that goes through the unblocked work items that are in the queue, and creates a small table / other tracking element that scehdules "traincars" that are filled with work items.  The design of this needs to be careful, as it could include multiple small work items in parallel, multiple small work items that are acceptable to group in series.  What research is available to help design this?  It would be complex but it's apart of the vision: making sure agents can execute efficiently on a larger project.
    IMPORTANT: Work items also probably need some estimates to be made while they are being drafted.  Maybe an estimated token cost?  Model teir already exists.
    
    Traincars get assigned WIs, and their dependent traincars.
    Then if a traincar has no open dependencies and there is an open thread, it get's kicked off.

I believe this addresses your parallel campaign open item and independent-batch train mode open item.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It appears the language "campaign" is still persisting when breaking down items.  Can you please make sure that "campaign" language is removed from all sources in this repo (ignoring logs and archive documents) and in your memory.  Instead SN/SR/LLR/TC workflow should have a phase property tied to them when indicating what phase they were ratified in, to make it clear when changes in scope (SN/SR/LLR) were introduced.  You can look at git history to back-date the current SN/SR/LLR/TCs, and then design a test to ensure a ratified SN/SR/LLR/TCs is populated with a non-empty phase.  Note in this way the phase also becomes derived (it is always the highest phase number of the last ratified item)

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

My main concern remaining is around the planning / research / build station and the way the current html is rendered.  (Can be broken into 3 issues / concerns) 1. What tools will allow you to see the rendered html and make better critiques of the current implimentation?  2. In relation to palnning itself, how can we better select deep planning and test case generation?  For example, if I'm building something that needs to optomize for a certain variable, I probably want that to be developed all within the same plan / develop station, but if the loop will be that complex, I probably want an adversarial review from another agent, and then I want those 2 agents to continue to iterate back and forth until they are agreed on the plan and optomization method.
3. Note this should also likely happen when constructing work items, and work items should generally always act on either defined software modules / LLRs or interfaces that bind them together.  When work items are constructed, the interfaces they expect to use for intercommunication should also be built out.  How can that be better encouraged, or should there be some dedicated engine / script that formally takes in a prompt and structurally asks one agent to build a plan, and another agent to give feedback, and then ask the first agent to await feedback / ping back and forth until the plan of work item decomposition and interfaces are agreed?

Feedback, please be critical of this and push back with evidence where reasonble:

1. Okay so this only tooling to support the development (something to be installed in dev-setup, not something downstream adopters would take).

2. Agreed the ping-pong rounds can be hazardous, but I don't see a good alternative.  Reviews are easy to merge, a planned bulk of potential work items - not so much.  If I surface a problem that Agent 1 breaks into 4 WI but another agent breaks into 3 WI, how do they get rectified?  A critique at the spec is already constrained to the interfaces of the spec itself, I'd like it to be able to be broader.  Almost a method to have a work_item_propsoal_nnn related to a user goal / and then let some arbiter talk to both, but it all seems hazardous.  Or can they both review eachothers plans, iterate their own plans, and then review again?  Maybe duel iteration of 2 independent plans n number of times, and then spawn a fresh arbiter to pick one given the users initial prompt?  Any research that exposes agent coplanning?  Can you spawn opus agents to gather evidence?

3. Agreed can propose IF at filing, but I think it's imperative specs act on defined interface boundaries, or else they can very quickly start constructing specific interfaces that just result in duplication as each spec wants it's own slightly unique variant.

~~~~~~~~~~~~~~~~~~~~~

For the recent hybrid work item constructor that uses multiple agents to build out a work plan, how is that initiated?  Is this in the form of a skill?  Or should a command script be constructed that takes in a string prompt and routes it to the corresponding agents and independent arbiter(s)?

Does the reseach methods that are included here correctly spin up lower tier agents? Or is it at least encouraged?

IMPORTANT: WI-190 is NOT complete, it is outfitted.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a gate is running adversarial reviews, is it an independent agent wearing different "hats"?  If so, would there be benifit in the reviewer also being from a different provider than the model that drafted the SN/SR/LRs?

Finally verify there is nothing here missing that would make all these template updates incompatible or struggle when I push it to upstream repositories, specifically gilbert (repository folder "core") which is quite complex.  My main concern is if the modules there will create any changes with some of the template's new capabilities.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consider integrating the latest think like fable for mid and low teir models to adopt when processing, this is simlar to another appproach that was already used in this template to pull in an external package to augment the environment of a non-strong-tier llm agent model.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

4 items of query / verification:

1.
Make sure for strong models the planner is strong (where the test cases should also get created), implimenter and reviewers can stay medium.  Which judgement determines if it should be duel planned or not?

2.
Can I add a 3rd model to act another reviewer?  How can I setup the configurations such that there are more degrees of preference?  In my case, I'd like to configure it as:
Primary planner: Claude
Primary builder: Claude
Reviewers: OpenAI and Kimi (OpenCode Go) and Grok (OpenCode Go)

Maybe prefer OpenAI for every 2 of every 3 reviews?  Or just reserve kimi or grok for judging?

3.
Verify / fix the project_state.html, this should have already landed (WI-231) but how does the integrator know which artifacts are generated?  How does it discover this?

4.
Verify incorperation of new merge method for parallel builds (should already be a WI by the time this hits.)

5.
iS THERE ANYTHING THAT WOULD HAVE PREVENTED THE complexity of the software (mainly thinking of the main funcitons) from growing?  Should the complexity check surface as an error instead of a warning?

6.
If there is attestation work or other work, even from parallel branches, it should all be piped into the open items at the root project for central review, just as all others are.

~~~~~~~~~~~~~~~~~~~~~~~~

Do we need to do anything to stress adversarial reviews?  Or to follow a specific review template?  Can you show me what is there currently?  This may be related to structured prompts as well when running agent-resume, if you refer to this reddit post, how does it compare to the prose that is currently being used to activate planners, implimenters, and reviewers ==>

    Most prompt “improvers” seem to do the same thing:

    Take a two-line request and turn it into a 500-word operating manual full of roles, headings, micro-steps, “think step by step,” “be thorough,” and twenty negative instructions.

    That approach makes less sense after reading Anthropic’s model-specific prompting guides.

    Fable 5 often benefits from less prescription, not more. Anthropic explicitly warns that prompts and skills written for earlier models can be too prescriptive and may degrade output quality.

    Opus 4.8 has a different failure mode: it follows instructions very literally, so implied scope can become a bug.

    The same generic “improvement” can therefore help one model and hurt another.

    I built prompt-polish around that problem.

    It is a free, open-source Claude/agent skill that rewrites rough prompts using the official prompting guide for the specific target model rather than applying one universal prompt-engineering template.

    Install:

    npx skills add mfarzanansari/prompt-polish

    Repo:

    https://github.com/mfarzanansari/prompt-polish

    Example invocation:

    prompt-polish/FABLE 5/review my API code and fix whatever is broken

    A simplified example of the output:

    Review [API scope] for defects that could cause incorrect behavior or failures, and fix the issues you can verify.

    Do not add features, refactor surrounding code, or introduce abstractions beyond what each fix requires. Run [relevant existing checks] after the changes. Report what changed, which checks passed, and anything you could not verify.

    Done means the verified defects are fixed and [relevant existing checks] pass.

    Fill in: [API scope], [relevant existing checks]

    The important part is not that it made the prompt longer. It added only the information that materially changes the model’s behavior and left unknown information as placeholders rather than inventing it.

    Internally, the skill:

    Routes the request to the correct model guide.

    Classifies it as an ask, build, agent, review, design, or pipeline task.

    Detects missing intent, deliverables, completion conditions, and instruction noise.

    Chooses the smallest useful rewrite tier.

    Runs a hard gate before returning the prompt.

    The hard gate rejects:

    - Task drift
    - Invented facts, files, tools, deadlines, or requirements
    - Unnecessary prompt inflation
    - Chain-of-thought extraction instructions
    - Boilerplate that the target model already handles by default

    The output is just the copy-ready prompt. It does not give you a lecture about every edit unless you ask.

    Current support:

    - Claude Fable 5
    - Claude Opus 4.8
    - Opus 4.7 routes to the 4.8 guidance

    Unsupported models are declined rather than receiving fake “model-specific” advice.

    It is MIT licensed and currently at v1.0.2.

    I want to test it against prompts that are genuinely difficult to polish without changing the task.

    Reply with a rough prompt and either Fable 5 or Opus 4.8. I’ll run it through the current version and report honestly where the skill helps, over-compresses, inflates, or drifts.

Do we need to make sure we dogfood the templates functions to prevent this repo from getting out of sync with it's own template?

I need help with the generator of PROJECT_STATE.html.  Most of the tabs of PROJECT_STATE.html have some deficiencies.  "When" and "How" tab content do  not have arrow heads, and the lines overlap / crisscross haphazardously.  In the process tab, the working loops should show two intersecting hoops, the current UI is just two circles around various blocks without clear flow or where that flow intersects with the AI terminal / resume script where the user would interact with / launch content.  Please clean up this generator for more professional looking flow diagrams that are human ledgible.  Install dependencies if needed.

~~~~~~~~~~~~~~~~
My main remaining concern is that the reviewer "hats" are getting applied at gates, but sometimes I still see output quality below where I would expect.  For instance, the html output still has multiple tabs that are hard to read, things a UI reviewer should have caught and flagged. Perhaps it's because the test cases were made earlier, but I'm wondering what can be done to ensure better quality moving forward.

It makes me think there are numerous skills and addons that could be referred to (both claude specific and for other vendor models) which could be indexed here as a reference to pull if relevent to down-stream users, for instance, the following (please spawn opus agents as needed to evaluate):

https://github.com/rebelytics/one-skill-to-rule-them-all 

https://claude.com/plugins/legal

https://claude.com/plugins/small-business

https://claude.com/plugins/finance

https://github.com/charlie947/social-media-skills

https://github.com/coreyhaines31/marketingskills

https://github.com/Jakubantalik/transitions.dev

https://github.com/Leonxlnx/taste-skill

https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

https://github.com/anthropics/skills

https://github.com/upstash/context7

https://github.com/obra/superpowers

https://github.com/rebelytics/one-skill-to-rule-them-all

~~~~~

Now, how can I ensure future critiques do not fail in this same way?  There could be many cases here, critiques / design iteration potentially needs to be rerun when the design is touched in a way it would be impacted, or do you htink the just-implimented work items covers these cases?

Unrelated, which test cases are actually carried through to a downstream user of the template?  Ideally only ones to validate the structure and relationships of the regiesteries themselves, omitting the test cases that are validating the various runner scripts that would have already have been tested here and need not be duplicated into downstream users.

~~~~~~~~~~~~~~~~

Specs are getting stored as WI labels, instead of getting integrated with the module they go with.  This will likely cause specs to rot over time.  Wasn't this addressed earlier in some form?  I thought work item specs were to get absorved into their respective work item when complete to keep all relevent content in a single location.

Related to the fix to ensure specs are properly archived for WIs and consumed into their relevent holders, that must be a core kit component, not something to opt in / opt out of.  It is critical the flow of information is in the appropriate location to help prevent rot and ensure relevent information is always discoverable for other LLM agents, can you confirm this is the case?

~~~~~~~~~~~~~~~~

Related to WI-254, you indicated "the shipped kit hook is untouched, so downstream sees no change.", I assume because the .coverage files are getting created by the test cases specific to this repo?  Just want to confirm.

Is WI-253 the only open work item?  Grind through WI-253

Finally, should we remove completed work items from the work-items table?  

~~~~~~~~~~~~~~~~~~~~~~

Remaining pieces: please spin up other agents where appropriate (opus level where appropriate as well).  Use the openai agent as well for critical cross-review as well where appropriate.

Note I want this session to be fully autonomous, attestation can be performed by a new agent or a different family agent.  I will not be present, I can review the requirement document changes later, but this is restructuring a deliverable that already exists, it is a rearchitecture, so I do not expect any SNs to change.

1. What can be done to ensure while agent-resume is running, that any new work that was created since it's start, is appropriately acted on (without requiring the train to come to a stop and "agent-resume" to be retriggered).  Or is that already working today?  So if I start agent-resume, a work item or review determines another work-item is created, will that newly created work-item be properly injested during the same agent-resume cycle?

2. What is causing the test cases here to take so long to run?  Ex: "The full gate bar on the composed tree takes a while."  I think the last metric I saw was 40 min?

3. A very old version of this ai-template was used in a multi-repo setup (multiple repos referenced throughout C:\Projects\Personal\homelab) and at one point there I saw a comment about interfering / conflicting IF- designations between repos (since they are all indepenent)  Perhaps it is already laid out, but if multi-repo connections are in use, the IF- layer can't just connect to a bare external IF-, it would have to prepeend it or otherwise specify a repo specific IF first.  I'm not sure if that neesd to be better clarified in the docs somewhere to prevent conflict.

4. Now that this ai-template is up-to-date, do you see any issues / blockers with getting it down-stream into the large gilbert project (C:\Projects\gilbert), this is probably the most complex project right now.  Obviously many registries will need to be updated to some of the new conventions / columns, that's fine, I just want to make sure there are not any other sticking points that will come back to this template and force iteration for compatability.

5. Finally, queue and churn through WI-374, WI-280, WI-277 and WI-375 at the end.

Consider done when:
- All questions above are answered
- Work items noted above are complete
- Any new work items that are constructed as a reaction to reviews both in work items and in downstream repo compatability that are critically / confidently needed are also completed.
- After all work is complete, perform migration on the gilbert project, such that it is moved over to the new template, and it's open items are waiting for the user to re-attest it's spine changes that are necessary to adopt the new ai-template.  Again, any new learnings from migrating the new template updates to gilbert should also be applied here if confident.

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Work item state:

Add draft, or keep in draft folder?  Or is state derived from the folder it's in?  It seems like the state of the work item attribute in the table perhaps duplciates the state that can be derived from where that WI exists in the repo.

Instead of going to "specs" in archive, they should go to a corresponding folder "Complted" or "Cancelled".  Note the retired term used earlier is also a bit ambiguous, which I think "Cancelled" firmly describes.

So before: queued, active, deferred, archive
After: draft, queued, active, deferred, cancelled, complete

Yes let's bake all this into corresponding work items and an overarching design document pointing to those work itmes to make sure this concurrency problem is attacked with the right level of complexity so it does not grow out of hand.  It seems a lot of the previous moth-balling was due to constraining the overall system and building checks instead of building constraints that would have prevented the bad behavior in the first place (it's not clear to me if that was due to assumptions or adversity to arcitectural change)

 ## Feedback about function calls:

To be precise about which is which: drive.py has no CLI at all — it's a library agent_loop.py calls when no role flag is given, and it reads fields off the shared namespace. The multi-WI batching you're remembering is agent_loop.py --wi.

drive.py — what it actually takes
Two parameters of its own: worker=None (a test injection seam) and tier="all" (the composed-tree bar tier). Plus 14 fields read off args:

Group	Fields
Agent invocation	agent_cmd
Routing	model, model_map, cmd_map, prompt_map, tier_map, prefer_map
Loop control	max_iterations, stall_limit, session_timeout, wait_on_limit, limit_retry_fallback
Console	no_session_echo, live_status
There is no lanes/jobs input, and no way to hand it multiple WIs. It always claims ready[0] and passes wi_ids = [wid] — exactly one. So a dispatcher needs a genuinely new input; nothing existing can be repurposed.

Two flag-collisions worth knowing before you design around them:

--max-iterations means two different things. drive uses it as its cycle ceiling (how many WIs), and does not forward it — so the worker independently uses its own default of 40 sessions. Set --max-iterations 5 meaning "five WIs" and each worker still gets 40 sessions.
--stall-limit also doubles: drive counts cycles that left the trunk unmoved, the worker counts consecutive no-commit sessions. This one at least is forwarded, so the number is consistent even though the unit isn't.
agent_loop.py — 24 flags, four roles
Role is selected by which flags appear: none → drive mode; --wi → worker; --interactive → one attached session; --dual-plan WI-### → one decomposition round.

The batching cluster is the worker one:

Flag	Meaning
--wi 'WI-201;WI-204'	the ordered constituent list — this is the batch
--train	session tag scoping logs and review evidence (defaults to branch name)
--worktree	becomes the effective root
--base	the integration base commit the branch was cut from
--rework	a findings file embedded as the rework scope
The rest are routing (--model, the five maps, --agent-cmd, --interactive-cmd), loop control (--max-iterations, --stall-limit, --pause, --session-timeout, --wait-on-limit, --limit-retry-fallback), and console (--no-session-echo, --live-status).

~~~~~~~~~~~~~~~~~~~~~~~

Using status.md and docs\concurrency-v2.md, I want to work through a deep redesign of some of the implimentation this ai-template has mutated into. Speciifcally around how work items are getting injested and what functionality lives where.

In general always plan to prevent bad behavior, instead of making checks around bad outcomes.  The flowchart today (Workstream A — concurrency and spine authority) appears to have a signficiant number of checks which I think have grown from individual failure modes, instead of prevention.

Open questions, collected and responded to.
A. Driver and dispatcher — one module or two?
	My initial thought is that this needs to be 2, but it needs to be carefully crafted.  It looks like drive is already doing a lot of what a dispatcher would need to do, and reintegrating into main needs to be done per workstream.  I would actually propose to take drive, rename it dispatch, and then extract the parts that are only really about driving.  The driving needs to move the work items into the in-work state in the trunk, then it needs to make that branch, and intiaite the drive for that work to be completed.  The main concern I have is that the drive then needs to wait for the dispatcher again to say it's okay to merge into trunk (since only one merge can happen at a time).  So ultimately, if it's easier to carry it in a single module that's okay, it just needs to have a definable number to define how many workstreams can be active, and whatever is doing the dispatching must follow the stateflow that was just setup.  The agent_loop.py may already be well poised for dispatching, it may just need some adjustment.
B. What admits the spine batch — dispatcher (waits) or claim rung (refuses)?
	I'm not sure what this is asking, a dispatcher is the only one who should kick off spine work. If a WI discovers spine work is necessary, it should clean up what it can and clarify it's scope has changed, along with what would likely be a new draft work item.
C. The ratified-vs-traced cell split, incl. SN-Refs and Verifies.
	Omit SN-Refs and Verifies as a ratified item to verify against.  Instead, if these change
D. Session grouping once drain grouping exists — keep, or remove the plumbing?
	I think this will clear up based on the flow I describe below.  We can discuss.
E. Default lane count. (The bar is CPU-capped at 50%, so two concurrent bars contend — lanes and bar cost are coupled.)
	I think in reality they would not contend.  One will usually be develop or review, while test bar costs only occurs right before merging and right after.
F. Does draft/ earn the schema change?
	In the TOML?  I think it must, if the TOML registry is the baseline for new WIs, all WIs must exist there in the form they are in, or else the registry could try to take that ID for something else.  Perhaps I misunderstand, but it makes me question how we keep the TOML status in sync with the actual folder state, or is that already a check?
	

WIs must always land back into trunk.  Branches never get to hang.  They must be closed.  If there is an issue, a adjudicator needs to run and decide how to take that work in and create follow-up work items, or it must throw away the work (which hopefully is rare), or it must find a way to quarantine the work in a way that it is accessible in the trunk so it can be picked up from a future work item.

~~~~~~~~~~~~~~~~~~~~~~~

This session will relate to some of the open items that surfaced from docs\rulings-context-2026-08-01.md, but I think expose some larger misalignments between the current scope of this repository and my expectations. In regard to R3, this really highlights how a work item needs to close out when it's scope has changed.  This might mean it thought a new WI was required (wi-397) or it relates to how a work item exits out (cancel, partial completion, handback).  In either case, I believe this really goes back to scope work.  For that, it needs to be addressed in a single lane, and perhaps that will cause some additional rework.  I don't think it changes much but now I would propose the total design to look like this.  Note this would then be a work item, which contradicts my last statement about no work items, but that is because I was misunderstanding the when (I didn't want a WI in process to create another WI).  Before we proceed, please review this plan, update the process diagram (which - maybe that's missing somewhere to, there should be both a mermaid diagram in the readme files and a html generated flow chart, how do those stay in sync?)  I want you to review my flow, critisize where you think it won't work, and lay out your own flow diagram with the corresponding funciton names and interface definitions along the flow path.

For reference, the gates, which also play into how the dispatcher needs to select work.

- **G0 - Any time a SN is in draft.
- **G1 — Requirements/UX/Constraints.** Needs + requirements are complete,
  measurable, and consistent with the vision; every requirement links a need;
  usability/doc needs, constraints, and non-goals are captured. (At G1 when: SRs point to SNs)
- **G2 — Decomposition & test coverage.** Every requirement decomposes to design
  (LLR) and a test (TC), each TC written **failing-first**; zero trace orphans;
  no placeholder rows; key runtime flows diagrammed. (At G2 when: TCs / LLRs all tie up into SRs, no orphans)
- **G3 — Implementation.** Code is written **test-first** and passes the full
  harness: format/lint, full test tier, coverage ≥ threshold, schema, every
  in-scope requirement `Verified`, no stubs. (At G3 when: All TCs pass.)
- **G-Release — Release readiness** *(per release)*. The release test tier
  passes; the generated release checklist is completed and signed; version
  bumped; changelog + interface versions updated.
- **G-Final — Acceptance.** A human exercises the real product (including
  manual/demonstration items) and approves.

Open questions on registry-machinery-breakdown:

What are permutations used for?  Why would it be listed in a system requirement?
Phase: Must always be NUMERIC ONLY, no prepended value.

Gate change detected ->
	If gate level prose are ratified, create a work item to create the breakdown to reach the next gate.
	If not ratified but autonomous, or gate level is NOT G2 and single attest, create a work item to perform ratification.
	Else derive the open-items that the gate is waiting for ratification or reattestation on the project owner.  PROJECT_STATE.html should automate surfacing of these items.

Continuous loop the dispatcher runs, performed each time a commit lands?:

	1. Detect the current gate, because that determines what work can be consumed.
	
		Gate advancement and level automation (which also sets the current phase).  A gate going DOWN always incriments the phase, and phase is always derived from the phase of all items, + 1 (to get to the next phase if the gate is getting reduced).  Therefore, getting the current phase for requirement phase creation must be a method that other LLMs can use.  THIS IS DETECTED BASED ON THE CHANGE IN THE REQUIREMENT DOCUMENTATION ITSELF.  (??? Alternative - Rely on handback document?  What if these don't align?  Realistically, I should rely on mechanization.)  This means the bar should automatically run based on the detected level.  This means gate level must be mechanized:
		
		SN does not have an SR, or SR does not have SN -> Gate is at 0
		TC / LLR do not have an SR or vice-versa -> Gate is at 1
		TCs (Full) do not pass -> Gate is at 2
		TCs (Release) do not pass -> Gate is at 3
		
		The tests on a repo must only pass for the current gate level OR if a work item calls for a certain gate to be met.  How can that be mechanized from the test standpoint?  This means the test call needs a single input that allows it to auto-detect the gate level?  Should precommits work the same way?  Or should precommits just warn the gate has dropped instead of failing?
		
		Why: Gate level determines what work can be done and if / when project owner input is required.
	2. Detect if spine-adjuncation needs to run (based on prose field items changing), which will seperately change the status for each corresponding document to modified if the ratified fields changed prose between the last trunk commit (what a worker committed) and the previous trunk commit.  Note this mechanism assumes a trunk is committed to only once from a branch, which is how it should operate.  When this happens a function mints a new work item with "spine-adjucation" noting which commit needs adjucation.  (That is - it should point to the last commit on trunk, which itself should differ in prose from the previous commit)
	3. Detect if any work items had a handback that needs to be addressed (did the last commit include a handback item).  If there is a handback item, create an arbiter work item detailing what was there, so that an LLM can digest that handback item compared to the larger project vision, and determine what sort of workitems are really required.  That is run in series, and done-when new workitems are minted or verifying nothing needs to be done.  The arbiter work item is considered rectified when the branch commits to trunk and removes the handback item into the archives.
	4. If spine-adjuncation wasn't necessary (no WI created) proceed to create ratification / reattestation WIs depending on repo configuraiton.  Note if reattestation / ratification IS required but it requires the project owner, this is the point the loop exits with a loud banner, no more work can be done, the reattest / ratification should automatically populate in the open-items.html for the user to review.
	5. Else move into the schedule and pop off the relevent work items unless a pause is active (In which case, another loud banner)
	6. If no work items in the queue, but gate is less than G-Release, create a work item to understand what needs to be done next to mint new work items for the queue to fully close out the repository.
	
	
OTHER SCRATCH NOTES RELATED TO THIS BREAKDOWN:

IMPORTANT: In order to keep all of this chained mechanically, I propose a work item can exit with a single work item proposal in it's repos folder with a draft name that can be mechanically picked up by the dispatcher and renamed accordingly.  It should be sent in as a queued work item with a definition of "handback", and run as a "no-parallel" item.  It can just be named as the "WI-XXX-handback.md", and that can be the single mechanism a work item uses to communicate back to the dispatcher to open up an arbiter and resolve open items in a mechanical way.

	Priority for the scheduler / dispatcher:
        -1: Assumption: when requirement documents are adjusted, they may or may not have their field properties updated correctly.  A work item should configure it's status if necessary (change back to modified or draft), but that may not happen, that is what the mechanisms below are for.
        0. Detection and creation of work items that occurs mechanically:
            0A. Detect if requirement fields have been modified.
		1. Work items that change scope first. (spine-g0; no-parallel) <- Detection mechanism is work items that declare they are for the spine, those work items are always taken on priority.
		2. Then work items that need adjucation (spine-adjucation; no-parallel), which will determine if the prose that changed actually changed scope and what level of risk is possible, or if it is just grammer /semantic clarification.  The outcome here is only changing modified boxes back to attest, or a new work item for deeper investigation, which may need to be a duel-plan work item. <- Detection mechanism is based on detecting the requirement doc registry fields have changed (those fields have already been determined previously) and the mode of the repository is autonomous or single-ratify.  If attended, the entire chain cannot move on because it requires user review of any prose.  How should this get filed as an open item so it is apparent on opening the PROJECT_STATE.html?  Or is this documented and realized in the PROJECT_STATE.html in some other way?  Maybe it doesn't matter because it surfaces as a block on agent-resume anyways, but ideally trajectory generation and html generation would use the same method as agent-resume to detect the block and surface it.
        3. Now all ambiguous information can be combined to flush out any scope rework.  the intended scope is clear, but the scheduler / dispatcher must make sure there are no loose ends open.  That's where the new mechanical check comes in and scans for all "WI-XXX-handback.md" items, converts them to the next available 
		4. Then if in autonomous mode, perform ratification (spine-attestation; no-parallel).  Same issue here, if we're in single attest and ready for gate 3, we need to stop and wait for owner ratification.
		5. Then work from the DAG (schedule.py):
		A. Then work high-risk items (high-risk; no-parallel)
		B. Then work critiques (critique, parallel)
		C. Then work ordinary work items (ordinary;  parallel)
		
		
		Note spine-adjucation to ratify scope change, plan new work items, and verify if current work items in queue need adjustment / cancellation (dual-plan method). (attestation; spine-serial)  Note something mechanical can build this.  A detected scope change is mechanical, the WI can be created with a derived description so it does not require an LLM at all to create the initial structure and force in a WI that must be attended to.
		Then work per the work queue DAG.  Spine-adjucation does NOT ever run a bar, it's a judgement from the LLM to verify the scope hasn't changed, and if it hasn't it just changes the rows from modified back to attested.
		
	The dispatcher does the same action every time it queues work:
		1. Changes the work item toml to indicate the work items are now in work while simultaneously moving those work items into a different folder to clarify they are running.  Right after this it commits and spins up the worker to create a branch of the current state.  This all happens in a single go.
		2. The dispatcher then maintains how ever many workstreams / trains can be dispatched at once.  If spine work is waiting, the dispatcher does NOT kick off more workstreams.  It waits for any active workstreams / trains to return to the station so they can be completely closed out.
		3. When a workstream / train returns to the station, there must be a method for it to indicate it is ready for integration into the trunk.  The dispatcher must allow only a single branch into the trunch at once, so it will have a single queue for integration.
		4. The branch sees that it is queued for integration, it pulls the current main into it's branch (if it's changed), runs the full bar, and at this point normally everything would work well and it would merge into trunk.
		5. If it CANNOT merge for some reason (which should never be the case, since when it was queued the dispatcher will not merge in any other work, and the branch should merge main into itself), it must immediately issue a repair block to determine how to close out the branch, related to the comments above.  Again, a branch should never sit hanging.  It looks like Workstream A — concurrency and spine authority shows a signficiant amount of complexity around corner cases that should never occur or should be handled in a more standardized way.  Even human input is needed, it should usually result in a new work request that touches the spine (because if something isn't clear it means scope is ambiguous).

Outcomes I want:
 - A review from your side on this flow, and to align on this entire repository template workflow from a high level.  What new questions surface when you look at this vs how the flow currently works?  Show me in a mermaid diagram what flow differences you would recommend, this may require multiple diagrams, but I want to see the circular flow at different levels to ensure we are aligned.

 - From there, I am hoping we can attack multiple loose ends in this repository, removing dead / duplicate code, cleaning up where tests / guards have become numerous and instead should have been handled at validation from the output side (instead of testing and or sanatizing on the input side).

 - This analysis does NOT need to follow the rubric of this repo itself, which I beleive is part of what's hampering the current development effort.  Until the mechanized development flow is solidified, there is no reason to constrain yourself to a ruleset that may actually limit / slow down the solution space.