# JOB_OPERATING_GUIDE.md

## Purpose
This file is the practical operating guide for the current recurring non-gaming automations.

It exists to answer, for each live job:
- what room it serves
- what it is supposed to do
- what good output looks like
- what failure looks like
- when it should be tuned, paused, or escalated
- what approval boundary applies

This is the operational companion to `JOB_CATALOG.md`, which is more planning-oriented.

## Shared Rules

### General Output Standard
A good recurring job should be:
- specific
- low-noise
- clearly owned by one room
- easy to skim
- easy to act on
- honest about uncertainty

### Pause / Tune / Escalate Rules
Pause or rework a job if it:
- repeatedly fails
- repeatedly posts low-value noise
- duplicates another room’s work
- invents evidence it does not actually have
- creates review burden without driving action

Escalate to `ops-desk` if a job:
- stops delivering
- starts drifting or hallucinating
- loses required auth or data access
- repeatedly creates operator confusion

Escalate to `command-center` if a job failure:
- blocks meaningful daily operation
- hides urgent work
- affects multiple rooms

---

## 1. morning-command-center-digest-weekdays-830am
- **Room:** `command-center`
- **Destination:** Discord `1484651751108775946`
- **Schedule:** weekdays 8:30 AM America/Chicago
- **Purpose:** give a concise top-level operating digest
- **Current prompt focus:** email queue, automation status, things waiting on the user, recommended focus
- **Good output looks like:**
  - clear top-of-day priorities
  - visible pending items
  - brief but useful recommendations
  - no fake precision
- **Common failure modes:**
  - stale status assumptions
  - delivery failure even after run success
  - weak prioritization
- **Escalate when:**
  - the digest stops delivering
  - it repeatedly misses pending items
  - it becomes too verbose/noisy to skim
- **Approval boundary:** internal summary only
- **Current audit note:** latest run status was `ok` but delivery was `not-delivered`; this should be watched immediately

## 2. ops-desk-midday-status-weekdays-1pm
- **Room:** `ops-desk`
- **Destination:** Discord `1484651772193673349`
- **Schedule:** weekdays 1:00 PM
- **Purpose:** summarize workflow health, drift, blockers, and next actions
- **Good output looks like:**
  - healthy vs needs-attention split
  - real blockers only
  - concrete next actions
- **Common failure modes:**
  - generic “everything looks fine” filler
  - invented blockers
  - unclear ownership of next steps
- **Escalate when:**
  - repeated failures are not reflected
  - auth/runtime drift is being missed
  - the room becomes a duplicate of command-center
- **Approval boundary:** internal operational coordination only

## 3. security-infra-daily-healthcheck-weekdays-845am
- **Room:** `security-infra`
- **Destination:** Discord `1484651900812001491`
- **Schedule:** weekdays 8:45 AM
- **Purpose:** summarize runtime/security/infra health and meaningful risks
- **Good output looks like:**
  - evidence-based status
  - clear urgency
  - practical remediation suggestions
- **Common failure modes:**
  - alarmist noise
  - shallow checks with fake confidence
  - missing repeated runtime/service issues
- **Escalate when:**
  - runtime health is unclear
  - important service failures are omitted
  - the job starts overstating severity without evidence
- **Approval boundary:** can inspect and recommend; not for disruptive remediation

## 4. engineering-midday-intake-status-weekdays-2pm
- **Room:** `engineering`
- **Destination:** Discord `1484988049229086850`
- **Schedule:** weekdays 2:00 PM
- **Purpose:** summarize likely engineering work lanes, blockers, and next actions
- **Good output looks like:**
  - clear implementation lanes
  - likely QA needs
  - practical next actions
- **Common failure modes:**
  - pretending there is concrete work when there is only weak inference
  - duplicating ops-desk reporting
  - no clear separation between implementation and QA
- **Escalate when:**
  - it repeatedly guesses at nonexistent work
  - it misses obvious implementation queues
- **Approval boundary:** internal coordination only

## 5. engineering-qa-review-check-weekdays-215pm
- **Room:** `engineering` / `qa-review`
- **Destination:** Discord `1484988049229086850`
- **Schedule:** weekdays 2:15 PM
- **Purpose:** keep QA expectations visible for engineering-impact work
- **Good output looks like:**
  - concrete QA-needed items when they exist
  - otherwise clear risk categories to watch
- **Common failure modes:**
  - boilerplate QA text with no decision value
  - verdict language used without evidence
- **Escalate when:**
  - risky work repeatedly bypasses QA
  - the post becomes empty ritual instead of useful review readiness
- **Approval boundary:** internal review guidance only

## 6. caruso-marketing-opportunity-scan-daily-1115am
- **Room:** `caruso-growth`
- **Destination:** Discord `1484651836966436934`
- **Schedule:** daily 11:15 AM
- **Purpose:** surface actionable Caruso marketing opportunities
- **Good output looks like:**
  - 3 to 5 credible opportunities
  - pain-first framing
  - useful draft angle
  - medium-fit items only when still believable
- **Common failure modes:**
  - SEO sludge
  - weak-fit communities
  - spammy suggested copy
- **Escalate when:**
  - the job repeatedly returns junk
  - source quality drops
  - the output is not actionable enough to justify review time
- **Approval boundary:** internal opportunity packaging only

## 7. caruso-weekly-marketing-pack-mondays-9am
- **Room:** `caruso-growth`
- **Destination:** Discord `1484651836966436934`
- **Schedule:** Mondays 9:00 AM
- **Purpose:** produce a weekly content/experiment pack
- **Good output looks like:**
  - specific ideas
  - credible voice
  - a clear “try these first” recommendation
- **Common failure modes:**
  - generic content ideas
  - repetitive themes with no freshness
  - hypey voice
- **Escalate when:**
  - weekly packs become repetitive or low-value
- **Approval boundary:** internal draft generation only

## 8. caruso-daily-reply-pack-weekdays-930am
- **Room:** `caruso-growth`
- **Destination:** Discord `1484651836966436934`
- **Schedule:** weekdays 9:30 AM
- **Purpose:** generate reusable draft replies for outreach/community opportunities
- **Good output looks like:**
  - natural replies
  - clear situations for use
  - helpful, non-ad-like framing
- **Common failure modes:**
  - overly promotional tone
  - repetitive replies
  - hard claims that cannot be supported
- **Escalate when:**
  - voice quality degrades
  - replies stop being adaptable/human
- **Approval boundary:** drafts only; no auto-posting

## 9. caruso-reddit-draft-queue-weekdays-10am
- **Room:** `caruso-growth`
- **Destination:** Discord `1484651836966436934`
- **Schedule:** weekdays 10:00 AM
- **Purpose:** prepare a queue of Reddit-ready draft candidates
- **Good output looks like:**
  - good subreddit fit
  - believable draft comments/posts
  - clear approval/reject/revise workflow
- **Common failure modes:**
  - weak subreddit fit
  - spammy tone
  - overconfident live-thread assumptions
- **Escalate when:**
  - draft quality falls below manual-posting usefulness
- **Approval boundary:** drafts only; explicitly not auto-posted

## 10. caruso-product-signal-digest-weekdays-1230pm
- **Room:** `caruso-product`
- **Destination:** Discord `1484651869593669762`
- **Schedule:** weekdays 12:30 PM
- **Purpose:** turn current signals into cautious product recommendations
- **Good output looks like:**
  - observed signals separated from interpretation
  - 1 to 3 sane recommendations
  - clear confidence level
- **Common failure modes:**
  - pretending there is customer evidence when there is not
  - vague recommendations with no decision value
- **Escalate when:**
  - the job becomes speculative filler
  - weak evidence is routinely overstated
- **Approval boundary:** internal recommendation only

## 11. caruso-competitor-watch-daily-530pm
- **Room:** `caruso-growth`
- **Destination:** Discord `1484651836966436934`
- **Schedule:** daily 5:30 PM
- **Purpose:** monitor competitor/market changes that affect messaging and positioning
- **Good output looks like:**
  - strong-signal items only
  - clear Caruso angle
  - practical importance
- **Common failure modes:**
  - low-value news churn
  - weak relevance to Caruso positioning
- **Escalate when:**
  - it becomes a generic news feed instead of a positioning tool
- **Approval boundary:** internal watch/reporting only

## 12. research-lab-weekly-idea-scan-mondays-11am
- **Room:** `research-lab`
- **Destination:** Discord `1484655635336265758`
- **Schedule:** Mondays 11:00 AM
- **Purpose:** generate ranked opportunity ideas worth deeper attention
- **Good output looks like:**
  - selective shortlist
  - clear wedge and downside
  - next research step
- **Common failure modes:**
  - generic SaaS sludge
  - too many weak ideas
  - fake confidence
- **Escalate when:**
  - the job stops being selective
  - it creates more reading burden than insight
- **Approval boundary:** internal research only

## 13. signalandcircuit-reddit-draft-queue-weekdays-10am
- **Room:** `signal-and-circuit`
- **Destination:** Discord `1484556120025727127`
- **Schedule:** weekdays 10:00 AM
- **Purpose:** prepare Reddit-oriented draft candidates for Signal and Circuit
- **Good output looks like:**
  - editorially credible drafts
  - relevant subreddit/topic fit
  - data-driven angle rather than promotion
- **Common failure modes:**
  - promotional tone
  - weak data grounding
  - room confusion with gaming/news scope
- **Escalate when:**
  - the room's identity becomes muddled
  - the drafts stop feeling editorially credible
- **Approval boundary:** drafts only; not auto-posted
- **Current audit note:** this job had an inconsistent sessionKey and was normalized to `agent:codex:main` during the 2026-03-24 audit/fix pass

## 14. daily-cross-room-standup
- **Room:** `command-center`
- **Destination:** planned for `command-center`
- **Schedule:** planned weekday morning cadence
- **Purpose:** synthesize cross room updates into one daily operating picture
- **Good output looks like:**
  - meaningful changes only
  - visible blockers and handoffs
  - a strong picture of what matters today
  - low noise and no fake alignment theater
- **Common failure modes:**
  - generic filler
  - repeating room local noise
  - missing important changes from the prior day
  - becoming too verbose to scan
- **Escalate when:**
  - important changes are still being missed by affected rooms
  - the standup becomes a ritual instead of a real synthesis layer
- **Approval boundary:** internal communication only
- **Current audit note:** planned communication infrastructure job, not yet confirmed live

## 15. engineering-context-sync
- **Room:** `engineering`
- **Destination:** planned for `engineering`
- **Schedule:** planned weekday cadence after morning state is known
- **Purpose:** ensure engineering sees recent changes that affect implementation reality
- **Good output looks like:**
  - major engineering relevant changes since yesterday
  - clean separation between context, blockers, and requested work
  - source docs that engineering can trust
- **Common failure modes:**
  - flooding engineering with non implementation chatter
  - missing cutovers, resets, or routing changes
  - stale or vague context
- **Escalate when:**
  - engineering still misses major recent work
  - the sync becomes either too noisy or too shallow to be useful
- **Approval boundary:** internal communication only
- **Current audit note:** planned communication infrastructure job, not yet confirmed live
