Create a technical workflow diagram for an AI job search system. Match the visual style of the provided `jcas_final.jpg` exactly.

## Visual Style (CRITICAL)

- **Background:** Dark blue/black gradient with subtle texture
- **Color palette:** Orange and teal/cyan — NO other colors for primary elements
- **Effects:** Neon glow/border effect on boxes and the central database
- **Typography:** Bold, clean sans-serif. Title in gradient orange-to-white.
- **Icons:** Small, simple icons inside each workflow box (wrench, magnifying glass, document, etc.)

## Title Banner

Top of diagram:
**"AI JOB SEARCH SYSTEM WORKFLOW: AGENTS MAX & SCOUT"**
- "AGENTS MAX & SCOUT" in orange gradient
- Rest in white

## Agent Zones (Two Columns)

### Left Zone: AGENT MAX (Orange theme)
- Header: **"AGENT: MAX (Resume Tailoring & Feedback)"**
- Border/accent color: Orange
- Workflows in this zone:
  - `init` (Setup) — "Both Agents" subtitle
  - `scoping-interview` (Setup)
  - `tailor-resume` (Apply) — formerly "fit-resume"
  - `cover-letter` (Apply)
  - `corpus-review` (Standalone)

### Right Zone: AGENT SCOUT (Teal theme)
- Header: **"AGENT: SCOUT (Market Research & Job Discovery)"**
- Border/accent color: Teal/cyan
- Workflows in this zone:
  - `industry-research` (Research)
  - `company-discovery` (Research)
  - `job-scan` (Research)

## Central Element: RESUME CORPUS

- Large database cylinder icon in the center
- Glowing orange/gold effect
- Label: **"RESUME CORPUS"**
- This is the visual anchor — all workflows connect to it

## Secondary Data Files

Show smaller elements near relevant workflows:
- `constraints.yaml` — near `scoping-interview`, with "WRITE" arrow going to it
- `research/openings/` — near `job-scan`, receiving parsed job files
- `applications/` folder — near `tailor-resume` and `cover-letter`, receiving output files
- `market_skills.json` — near `job-scan`, with bidirectional arrows

## Arrow Annotations

Use labeled arrows showing data flow:
- **"READ >>>"** — orange arrows, pointing FROM corpus TO workflow
- **"<<< WRITE"** — teal arrows, pointing FROM workflow TO corpus
- Arrows should have slight glow effect matching their color

## Numbered Phases (Bottom labels)

Three phase indicators along the bottom or integrated into the flow:
1. **(1) Setup** — pointing to init/scoping-interview area
2. **(2) Apply to Job** — pointing to tailor-resume/cover-letter area
3. **(3) Research Market** — pointing to Scout's workflow area

## Entry/Exit Points (Left edge)

- **"User Action"** — entry point showing user initiating workflows
- **"Job Application"** — exit point showing final deliverable going out

## Key Data Flows to Show

1. `init` → WRITES → RESUME CORPUS (creates corpus)
2. `init` → WRITES → `market_skills.json` (creates empty seed)
3. `scoping-interview` → READS → RESUME CORPUS
4. `scoping-interview` → WRITES → `constraints.yaml`
5. `job-scan` → WRITES → `market_skills.json`
6. `job-scan` → WRITES → `research/openings/`
7. `corpus-review` → READS → `market_skills.json` + RESUME CORPUS
8. `corpus-review` → WRITES → RESUME CORPUS
9. `tailor-resume` → READS → RESUME CORPUS + `constraints.yaml` + `research/openings/`
10. `tailor-resume` → WRITES → RESUME CORPUS (new accomplishments)
11. `tailor-resume` → WRITES → `applications/resumes/`
12. `cover-letter` → READS → RESUME CORPUS + `constraints.yaml`
13. `cover-letter` → WRITES → `applications/cover_letters/`
14. `linkedin-review` → READS/WRITES → RESUME CORPUS

## Overall Impression

Technical and polished, like a well-designed DevOps dashboard or system architecture poster. The dark background with glowing elements should convey "modern AI system" while remaining clear and readable. The orange/teal split should make it immediately obvious which agent owns which workflows.
