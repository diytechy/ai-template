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
Then it moves into a fresh build-out plan.



C: It kicks off a work-advisor / schedular that goes through the unblocked work items that are in the queue, and creates a small table / other tracking element that scehdules "traincars" that are filled with work items.  The design of this needs to be careful, as it could include multiple small work items in parallel, multiple small work items that are acceptable to group in series.  What research is available to help design this?  It would be complex but it's apart of the vision: making sure agents can execute efficiently on a larger project.
    IMPORTANT: Work items also probably need some estimates to be made while they are being drafted.  Maybe an estimated token cost?  Model teir already exists.
    
    Traincars get assigned WIs, and their dependent traincars.
    Then if a traincar has no open dependencies and there is an open thread, it get's kicked off.

For open item 1 - This should be automatic, opt-out.  Perhaps this needs to be it's own design effort.  If you have many interdependnent work items / chained work items, those should be run on a chain.  And in fact work items could be grouped along that chain as train as well.  Thus each session along a chain becomes a traincar.  It could hold multiple unrelated mini-work-items, multiple workitems that are co-dependnent but can be reasonably executed (but then I would question why they are seperate work-items).  Perhaps this is all making the executor do more than it should.  Do we need a work-advisor to collate work-items and fold them into eachother where applicable?  That way the executor only cares about execution, and a prestep is a work-advisor that is trimming down the work-items and collating their scope into reasonable portions before the executor acts.

For open item 2 - Again, this makes me think "campaign" should die, or perhaps just not drive any work.  



