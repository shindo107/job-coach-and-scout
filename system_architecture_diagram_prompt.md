Create a technical workflow diagram for an AI job search system. Match the visual style of the provided `jcas_final.jpg` exactly.

## Visual Style

- **Background:** Dark blue/black gradient with subtle texture
- **Color palette:** Orange and teal/cyan only
- **Effects:** Neon glow on boxes and central database
- **Typography:** Bold sans-serif. Title gradient orange-to-white.
- **Icons:** Simple icons in each workflow box

## Title Banner

**"AI JOB SEARCH SYSTEM WORKFLOW: AGENTS MAX & SCOUT"**
- "AGENTS MAX & SCOUT" in orange gradient
- Rest in white

## Agent Zones (Two Columns)

### Left: AGENT MAX (Orange)
**"Resume Tailoring & Feedback"**
- `init` (Setup) — "Both Agents" subtitle
- `scoping-interview` (Setup)
- `tailor-resume` (Apply)
- `cover-letter` (Apply)
- `corpus-review` (Standalone)
- `linkedin-review` (Standalone)

### Right: AGENT SCOUT (Teal)
**"Market Research & Job Discovery"**
- `industry-research` (Research)
- `company-discovery` (Research)
- `job-scan` (Research)

## Central Element: RESUME CORPUS

- Large database cylinder, glowing orange/gold
- Label: **"RESUME CORPUS"**
- All workflows connect to it

## Secondary Data Files

Position near relevant workflows:
- `constraints.yaml` — near `scoping-interview`
- `voice_profile.json` — near `cover-letter`
- `market_skills.json` — between `job-scan` and `corpus-review`
- `research/` folder — near Scout workflows (industries/, companies/, openings/)
- `applications/` folder — near `tailor-resume` and `cover-letter`

## Arrow Annotations

- **"READ >>>"** — orange arrows, corpus → workflow
- **"<<< WRITE"** — teal arrows, workflow → corpus

## Phase Labels (Bottom)

1. **(1) Setup** — init, scoping-interview
2. **(2) Research** — industry-research, company-discovery, job-scan
3. **(3) Apply** — tailor-resume, cover-letter

## Entry/Exit Points

- **"User Action"** — entry point (left edge)
- **"Job Application"** — exit point (right edge, from applications/)

## Key Data Flows

**Setup:**
- `init` → creates CORPUS, seeds `market_skills.json`
- `scoping-interview` → reads CORPUS, writes `constraints.yaml`

**Research (Scout):**
- `industry-research` → writes `research/industries/`
- `company-discovery` → writes `research/companies/`
- `job-scan` → writes `research/openings/`, updates `market_skills.json`

**Apply (Max):**
- `corpus-review` → reads `market_skills.json`, updates CORPUS
- `tailor-resume` → reads CORPUS + openings, writes `applications/resumes/`, updates CORPUS
- `cover-letter` → reads CORPUS + `voice_profile.json`, writes `applications/cover_letters/`
- `linkedin-review` → reads/writes CORPUS, writes `linkedin.md`

## Overall Impression

Technical and polished like a DevOps dashboard. Dark background with glowing elements conveys "modern AI system." Orange/teal split makes agent ownership immediately obvious.
