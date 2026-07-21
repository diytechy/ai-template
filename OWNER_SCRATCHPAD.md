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