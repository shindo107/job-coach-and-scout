# Industry Research

## Summary

**Purpose:** Research, score, and tier industries by fit, creating a durable and structured knowledge base.
**Agent:** Job Scout
**Phase:** research
**Reads:**
- `profile/corpus.json` — Skills and experience context (required)
- `profile/constraints.yaml` — Job search preferences (required)
- `research/industries/index.md` (optional) — Previously researched industries
**Creates:**
- `research/industries/index.md` — Tiered summary of all researched industries
- `research/industries/{industry}.md` — A detailed analysis file for each industry
- `research/companies/{industry}/{company}.md` (stubs) — Placeholder files for notable companies
**Updates:**
- `profile/constraints.yaml` (conditional) — If user wants to add avoid_industries
**Prerequisites:** init and scoping-interview completed

---

> **STRATEGIC MARKET INTELLIGENCE**: Analyzes hiring trends and industry dynamics to identify where your skills are most valued, creating an actionable and auditable knowledge base.

**Trigger:** User says "research industries for me", "which industries should I target", or "help me find the right industries".

## Persona

**Load and adopt:** `agents/job-scout.md`

Read the full persona file and embody Scout for this workflow. Use Scout's analytical, data-driven approach.

## Context Required

Before starting, load these files:
- `profile/corpus.json` — Skills and experience context (required)
- `profile/constraints.yaml` — Job search preferences (required)
- If `research/industries/index.md` exists, load it to see what was previously researched.

## Steps

### Step 1: Load Profile and Define Research Vector

**1a. Load and parse profile:**
- **Instruction:** Load `corpus.json` and `constraints.yaml`. Synthesize the user's skills, experience level, and key constraints (remote preference, salary, dealbreakers) into a research vector.
- **Instruction:** Present this summary to the user for confirmation before starting the research. "Based on your profile, I'm researching industries for a {level} {role_type} with expertise in {skills}, targeting roles that are {remote_pref} and pay at least ${min_salary}. Correct?"

### Step 2: Initial Market Research

**2a. Create directories:**
- **Instruction:** Ensure the output directories exist. Run `mkdir -p research/industries`.

**2b. Conduct broad market searches:**
- **Instruction:** Use WebSearch to understand the current landscape.
- **Example Queries:** `"{primary_skill} job market 2026"`, `"fastest growing tech industries 2026"`, `"highest paying industries for {role_type}"`.

**2c. Compile initial industry list:**
- **Instruction:** From the search results, identify a list of 8-12 promising industries to analyze further.

### Step 3: Deep Dive Analysis and Modular Output Generation

**Instruction:** For EACH industry in the list from Step 2c, perform the following steps and create its dedicated analysis file.

**3a. Gather industry-specific data:**
- **Instruction:** For the current industry (e.g., "Fintech"), run focused WebSearch queries.
- **Example Queries:** `"{industry} tech hiring trends 2026"`, `"{industry} remote work policy trends"`, `"{industry} {role_type} salary ranges"`.
- **CRITICAL:** For each piece of data, keep track of the source URL.

**3b. Assess and score the industry:**
- **Instruction:** Score the industry from 0-100 based on weighted criteria: Skills match (30%), compensation alignment (25%), remote fit (20%), growth trajectory (15%), and constraint compliance (10%).

**3c. Generate pros, cons, and rationale:**
- **Instruction:** Write 2-3 pros and 1-2 cons for the user considering this industry. Provide a specific "Why it's for you" rationale connecting the analysis to the user's unique profile.

**3d. Identify notable companies:**
- **Instruction:** Find 3-5 notable companies in the industry that appear to be hiring or are market leaders.

**3e. Save individual industry file:**
- **Instruction:** Create a new file at `research/industries/{industry-name}.md`. The industry name should be lower-case with spaces replaced by hyphens (e.g., `healthcare-tech.md`).
- **Instruction:** The file must contain the score, tier, pros/cons, rationale, and a `## Sources` section with all URLs used for *this specific industry's analysis*.

**3f. Create company stubs:**
- **Instruction:** For each notable company found in step 3d, create the necessary directory `mkdir -p research/companies/{industry-name}/`.
- **Instruction:** Then, create an empty placeholder file: `touch research/companies/{industry-name}/{company-name}.md`.
- **Instruction:** This creates an actionable handoff to the `company-discovery` workflow.

### Step 4: Tier and Generate Index File

**4a. Tier all researched industries:**
- **Instruction:** Once the loop in Step 3 is complete, sort all the analyzed industries into Tiers based on their scores (e.g., Tier 1: 70-100, Tier 2: 50-69, Tier 3: <50).

**4b. Create the index file:**
- **Instruction:** Save a new file to `research/industries/index.md`.
- **Instruction:** This file should contain a summary of the research and then list the industries by tier, with a brief summary and a direct link to the detailed analysis file for each one.
- **Example Entry:** `### 🏆 Fintech (Score: 88/100)`\n`Strong demand for your backend skills and aligns with your salary expectations. [Read the full analysis](./fintech.md).`

### Step 5: Present Results

**5a. Display summary from `index.md`:**
- **Instruction:** Announce completion and present the tiered summary from the generated `index.md` file. Highlight the Tier 1 industries. "Research complete. I've analyzed {X} industries and tiered them based on fit with your profile. Your strongest opportunities appear to be in {Tier 1 industries}."

**5b. Present Tier 1 in detail:**
- **Instruction:** Briefly summarize the pros for each Tier 1 industry and point the user to the detailed files. "Both Fintech and Cloud Infrastructure are strong fits. Fintech offers higher salary potential, while Cloud has more remote-friendly roles. You can read the full deep-dive in the `research/industries/` directory."

### Step 6: User Feedback and Constraint Update

**6a. Ask for feedback:**
- **Instruction:** Actively solicit the user's input on the results. "Here are the tiers I've identified. Does this list align with your own interests and expectations? Are there any here that you'd like to deprioritize, regardless of the score?"

**6b. Offer to update constraints:**
- **Instruction:** If the user expresses a strong negative preference for a high-ranking industry (e.g., "I'd never work in E-commerce"), offer to make that preference permanent. "That's useful feedback. Would you like me to add 'E-commerce' to your `avoid_industries` list in `profile/constraints.yaml` so I don't suggest it again in the future?"
- **Instruction:** If the user agrees, perform a safe, validated write to update their `constraints.yaml` file.

### Step 7: Complete and Suggest Next Steps

**Instruction:**
- Summarize the outcome: a new, structured knowledge base in the `research/` directory.
- Propose an intelligent next step based on the new artifacts.
- **Example:** "Your industry analysis is saved. I've also created placeholder files for top companies in your Tier 1 industries. We can now run `company-discovery` on 'Fintech' to find more companies, or we can do a deep-dive on one of the specific companies I already identified, like 'Stripe' or 'Brex'. What's your preference?"

## Output

**Files created:**
- `research/industries/index.md` — The summary file.
- `research/industries/{industry-name}.md` — One file per industry.
- `research/companies/{industry-name}/{company-name}.md` — Empty placeholder stubs.
- `profile/constraints.yaml` (potentially updated).

## Recommend Next

After this workflow completes successfully, suggest **company-discovery**, framed around the new artifacts. "Ready to explore specific companies? We can either run a broad discovery in a Tier 1 industry like '{industry_1}', or we can start with the notable companies I've already stubbed out, like '{company_1}'."
