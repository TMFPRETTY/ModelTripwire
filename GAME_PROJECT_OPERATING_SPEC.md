# GAME_PROJECT_OPERATING_SPEC.md

## Purpose
This file defines the initial operating model for the 2D isometric RPG project.

## Project
- Project type: 2D isometric RPG
- Primary codebase: `/Users/tmfprettybot/Documents/Game/Untitled-2d-Isometric-RPG`
- Initial Discord room: `1485801109087060018`

## Initial Room Model

### game-dev
- Purpose: main game project room
- Discord channel id: `1485801109087060018`
- Role: intake, planning, systems direction, implementation requests, coordination
- Owning agent: `game-dev`

## Relationship To Engineering And QA
The game room is the domain room.
Engineering is the implementation lane when work becomes code/debugging/integration/tooling work.
QA is the validation gate for engineering-impact work.

Default loop:
- game-dev defines the need
- engineering implements when implementation work is required
- QA reviews the result
- engineering reworks if needed
- approved result returns to the game room

## What Belongs In game-dev
- feature ideas
- mechanic/system prompts
- gameplay loops
- narrative/world requests
- content pipeline requests
- bug reports
- implementation requests
- prioritization and scope decisions
- requests to inspect the game repo and propose changes

## What Does Not Need To Start Here
These can exist later as separate rooms if the project grows:
- game-design
- game-writing
- game-art
- game-audio
- game-engineering
- game-qa
- game-production

For now, keep the project simple and centralize work in `game-dev` unless specialization becomes useful.

## Repo Context Rule
If a request is clearly about the game, default working context should be:
- `/Users/tmfprettybot/Documents/Game/Untitled-2d-Isometric-RPG`

## Practical Operating Rule
- Use `game-dev` as the source-of-truth room for the game.
- When implementation is needed, route the work into engineering behavior with the game repo as context.
- Do not treat implementation as complete until QA has passed it, explicit approval is given, or the work is intentionally stopped.

## Initial Studio Agent Roster

### Chief of Staff
- Department: Studio Operations
- Role: coordination, synthesis, prioritization, conflict resolution, decision continuity
- Canonical spec: `game-agents/CHIEF_OF_STAFF.md`
- Notes:
  - coordinates specialists without replacing them
  - protects alignment, focus, and clear next actions
  - should be the first escalation point when game-agent recommendations conflict

### Game Director
- Department: Creative Leadership
- Role: protects game vision, fun, cohesion, and player experience quality
- Canonical spec: `game-agents/GAME_DIRECTOR.md`
- Notes:
  - evaluates whether features strengthen or dilute the game
  - should challenge feature creep and weak-fit mechanics directly
  - acts as a guardian of the core fantasy and overall game feel

### Executive Producer
- Department: Production
- Role: protects scope discipline, milestone realism, sequencing, and ship viability
- Canonical spec: `game-agents/EXECUTIVE_PRODUCER.md`
- Notes:
  - pressures work against schedule and scope reality
  - should challenge undefined work, perfectionism, and non-essential additions
  - should help force clarity on what must happen now versus later

### Technical Director
- Department: Engineering Leadership
- Role: protects architecture, maintainability, performance, integration quality, and technical debt control
- Canonical spec: `game-agents/TECHNICAL_DIRECTOR.md`
- Notes:
  - should challenge fragile systems, tight coupling, and weak abstractions
  - should be conservative with complexity unless value is clear
  - should protect long-term development speed, not just short-term implementation success

### Art Director
- Department: Visual Development
- Role: protects visual identity, readability, tonal consistency, and stylistic cohesion
- Canonical spec: `game-agents/ART_DIRECTOR.md`
- Notes:
  - should challenge mismatched assets, style drift, unclear silhouettes, and interface clutter
  - should prioritize readability and emotional fit, not just effort or detail level
  - acts as the visual consistency guardrail for the project

### Narrative Director
- Department: Narrative and Worldbuilding
- Role: protects story logic, lore coherence, dialogue quality, tone, and emotional arcs
- Canonical spec: `game-agents/NARRATIVE_DIRECTOR.md`
- Notes:
  - should challenge lore contradictions, flat dialogue, narrative bloat, and story/gameplay mismatch
  - should protect pacing as well as depth
  - acts as the narrative consistency and tone guardrail for the project

### Audio Director
- Department: Audio
- Role: protects sonic identity, audio readability, emotional pacing, and gameplay feedback through sound
- Canonical spec: `game-agents/AUDIO_DIRECTOR.md`
- Notes:
  - should challenge weak feedback, generic audio direction, and noisy/overlapping mixes
  - should prioritize clarity and mood, not just added sound density
  - acts as the audio identity and feedback guardrail for the project

## Future Expansion Path
As the game project grows, likely additional rooms are:
- `game-design`
- `game-writing`
- `game-art`
- `game-engineering`
- `game-qa`
- `game-production`

Do not create these just because they sound nice. Create them when they solve a real coordination problem.
