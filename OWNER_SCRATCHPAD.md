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

*******************************

I notice in visual code using claude code, I can complete multiple work items in a single session, but often when running agent-resume it seems only 1 work item is pulled per session, resulting in signficantly more session spin ups / context re-uploads / etc.  Is there a gap with how work-items are grouped and aggrigated for a session?  Is the method being used too concervative?

Need to adjust the process maps, specifically to show how injest occurs and interaction with open items and human.

While agent-resume is running, is it possible for each workstream to just update it's latest line on the console (so, intead of a long rolling window, each workstream continues to update it's status in a line that gets continuously updated.)

Other noticed items: The logs (in /docs/interation) and reviews don't appear to be committed with the rest of their content, it would be good for them to be part of the code commit for reference.  Should the reviews and logs include the work item key name in their label / filename for tracking?  

Do we need "hats" to be allocated to specific SRs to be spun up during related development?  Or how can we ensure test cases / and specifically critiques are triggered appropriately for the right content.  Ex: If a work-item is building UI, how does the resume-agent chain know to wear a UI hat to evaluate the UI for accessability and readability?

For gate reviews should we drop in a full review?  Should the text be verbatim: 

Can we add in the knowledge kits from 
