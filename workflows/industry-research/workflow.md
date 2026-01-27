# Industry Research

## Summary

**Purpose:** Research industry trends and tier industries by fit with your profile
**Agent:** Job Scout
**Reads:**
- `profile/corpus.json` — Skills and experience context (required)
- `profile/constraints.yaml` — Job search preferences (required)
**Creates:**
- `research/industries.md` — Tiered industry analysis with scores and rationale
**Approximate time:** 15-25 minutes (market research + analysis)
**Prerequisites:** init and scoping-interview completed

---

> **STRATEGIC MARKET INTELLIGENCE**: Analyzes hiring trends and industry dynamics to identify where your skills are most valued, helping you focus your job search on promising sectors.

**Trigger:** User says "research industries for me", "which industries should I target", "help me find the right industries", or wants market intelligence before company-specific research

## Persona

**Load and adopt:** `agents/job-scout.md`

Read the full persona file and embody Scout for this workflow. Use Scout's analytical communication style, data-driven approach, and focus on quality over quantity.

## Context Required

Before starting, load these files:
- `profile/corpus.json` — Skills and experience context (required)
- `profile/constraints.yaml` — Job search preferences (required)

**If corpus doesn't exist:**
```
I need your Resume Corpus to understand your skills and experience, but I couldn't find `profile/corpus.json`.

The easiest way to set this up is to run the init workflow — just say "run init" and I'll help you import your resume and create your corpus. Or if you have a resume file elsewhere, let me know the path and I'll help you import it.
```

**If constraints don't exist:**
```
I need your job search preferences to filter industries, but I couldn't find `profile/constraints.yaml`.

Let's run the scoping-interview workflow to capture your preferences — just say "run scoping-interview". Or if you want to skip that, tell me your key constraints (salary expectations, remote preference, location requirements, any industry dealbreakers) and I'll work with those.
```

## Steps

### Step 1: Load Profile Context

**1a. Load and parse corpus:**

Read `profile/corpus.json` and extract:

**Primary technical skills:**
- Programming languages and frameworks
- Domains (backend, frontend, data, ML, infrastructure, etc.)
- Tools and platforms

**Experience areas:**
- B2B vs B2C experience
- Enterprise vs startup background
- Industry experience already have

**Seniority indicators:**
- Years of experience
- Leadership/management experience
- Role titles held

**1b. Load and parse constraints:**

Read `profile/constraints.yaml` and extract relevant fields:

| YAML Path | How Used |
|-----------|----------|
| `location:` → `remote_preference:` | Weight remote-friendly industries higher |
| `compensation:` → `minimum_base:` | Filter industries that typically pay below minimum |
| `preferences:` → `target_industries:` | Prioritize if specified |
| `dealbreakers:` → `industries:` | Exclude from analysis entirely |
| `preferences:` → `company_size:` | Note which industries have preferred sizes |

Example constraints.yaml structure:
```yaml
location:
  remote_preference: fully_remote
compensation:
  minimum_base: 180000
preferences:
  target_industries: [fintech, cloud]
  company_size: startup
dealbreakers:
  industries: [defense, gambling]
```

**1c. Summarize profile for research:**

```
Based on your profile:
- **Primary skills:** {skill_1}, {skill_2}, {skill_3}
- **Experience level:** {level} ({years} years)
- **Background:** {B2B/B2C/both}, {enterprise/startup/both}
- **Key constraints:** {remote_pref}, ${min_salary}+, {other constraints}
- **Dealbreakers:** {any industry dealbreakers}

I'll research industries that match this profile.
```

### Step 2: Research Current Market

**2a. Conduct skill-specific searches:**

Use WebSearch to gather current hiring intelligence:

```
Search queries:
- "{primary_skill} job market 2026"
- "{primary_skill} hiring trends by industry"
- "Best industries for {role_type} 2026"
- "{secondary_skill} demand 2026"
```

**2b. Conduct trend searches:**

```
Search queries:
- "Fastest growing tech industries 2026"
- "Industries with most remote tech jobs 2026"
- "Tech hiring outlook by sector 2026"
- "Highest paying industries for {role_type}"
```

**2c. Compile initial industry list:**

Based on search results, identify 8-12 industries where user's skills are relevant:

Consider industries like:
- Fintech / Financial Services
- Cloud Infrastructure / DevOps
- Healthcare Tech / Biotech
- E-commerce / Retail Tech
- AI/ML Platforms
- Cybersecurity
- Enterprise SaaS
- Consumer Tech
- Gaming / Entertainment
- Climate Tech / Clean Energy
- Logistics / Supply Chain Tech
- EdTech

**2d. Note search sources:**

Track URLs and publication dates for methodology section.

**IMPORTANT:** After each WebSearch, immediately record:
- The search query used
- Source URLs from results (copy the actual URLs)
- Publication dates where visible

Store these in a running list — you'll need them for the Sources section in the output file.

### Step 3: Analyze Each Industry

**ITERATE:** For EACH industry in your list from Step 2c, perform steps 3a through 3e before moving to the next industry.

**3a. Gather industry-specific data:**

For the current industry, run these WebSearch queries (replacing {industry} with the actual industry name):
```
- "{industry} tech hiring 2026"
- "{industry} remote jobs availability"
- "{industry} {role_type} salary range"
- "{industry} job growth outlook"
```

Record source URLs from each search for the Sources section.

**3b. Assess each industry on dimensions:**

| Dimension | Assessment |
|-----------|------------|
| **Hiring volume** | High / Medium / Low demand for user's skills |
| **Growth trajectory** | 📈 Expanding / ➡️ Stable / 📉 Contracting |
| **Remote prevalence** | 🏠 High / 🏢 Mixed / 🏛️ Low |
| **Salary range** | Typical range for user's level |
| **Company sizes** | Mostly startups / Mixed / Mostly enterprise |
| **Constraint alignment** | How well it fits user's preferences |

**3c. Score each industry (0-100):**

Calculate fit score based on weighted criteria:

| Criterion | Weight | Scoring |
|-----------|--------|---------|
| Skills match | 30% | How much demand exists for user's specific skills |
| Compensation alignment | 25% | Whether typical salaries meet user's minimum |
| Remote/location fit | 20% | Match with user's remote preference |
| Growth trajectory | 15% | Industry expansion = more opportunities |
| No dealbreakers | 10% | Absence of user's stated dealbreakers |

**3d. Generate pros and cons:**

For each industry:
- **2-3 Pros:** Why this industry fits the user
- **1-2 Cons:** Potential concerns or mismatches
- **Specific rationale:** Connect to user's actual profile

**3e. Identify notable companies per industry:**

For each industry being analyzed, use WebSearch to find 3-5 well-known companies:
```
Search: "top {industry} companies hiring engineers 2026"
Search: "best {industry} companies to work for tech"
```

Record notable company names for each industry to include in the tier presentation.

### Step 4: Tier Industries by Fit

**4a. Sort industries into tiers:**

Based on fit scores:

| Tier | Score Range | Meaning |
|------|-------------|---------|
| **Tier 1: Strong Fit** | 70-100 | Prioritize these industries |
| **Tier 2: Moderate Fit** | 50-69 | Worth exploring with caveats |
| **Tier 3: Watch List** | Below 50 | Monitor but don't prioritize |

**4b. Prepare tier presentation:**

For each industry in each tier, use the appropriate emoji:
- **Tier 1:** Use 🏆 (trophy)
- **Tier 2:** Use 🥈 (silver medal)
- **Tier 3:** Use 👀 (eyes/watching)

```markdown
### {emoji} {Industry Name} (Score: {XX}/100)
**Growth:** {📈/➡️/📉} {trend} | **Remote:** {🏠/🏢/🏛️} {level} | **Salary:** ${range}

**Pros:**
- {Pro 1 - connected to user's profile}
- {Pro 2}
- {Pro 3 if applicable}

**Cons:**
- {Con 1}
- {Con 2 if applicable}

**Why for you:** {Specific rationale connecting to user's skills, experience, or constraints}

**Top companies to watch:** {3-5 notable companies from Step 3e}
```

### Step 5: Present Results

**5a. Display summary:**

```markdown
## Industry Research Complete

Based on your profile as a {level} {role_type} with expertise in {skills}, I've analyzed {count} industries.

**Quick Overview:**
- **Tier 1 (Strong Fit):** {count} industries
- **Tier 2 (Moderate Fit):** {count} industries
- **Tier 3 (Watch List):** {count} industries

Your strongest opportunities are in **{top_industry_1}** and **{top_industry_2}**, both showing strong demand for your skills with compensation meeting your ${min} target.
```

**5b. Present Tier 1 in detail:**

Show full analysis for each Tier 1 industry.

**5c. Present Tier 2 summary:**

Show condensed view with key points for moderate fits.

**5d. Present Tier 3 briefly:**

List watch-list industries with one-line rationale.

### Step 6: Save Output File

**6a. Create research directory if needed:**

Use Bash to run: `mkdir -p research/`

**6b. Check for existing file:**

If `research/industries.md` already exists, inform the user:
```
Note: research/industries.md already exists and will be overwritten with fresh analysis.
If you want to preserve the previous version, let me know and I'll rename it first.
```

Wait for user acknowledgment before proceeding.

**6d. Save to research/industries.md:**

Replace all `{placeholder}` values with actual data. For the date, use today's date in YYYY-MM-DD format.

```markdown
---
generated: "YYYY-MM-DD"  <!-- Replace with today's actual date -->
based_on_profile: "profile/corpus.json"
constraints_used: "profile/constraints.yaml"
industries_analyzed: {count}
---

# Industry Research: {User Name}'s Job Search

## Summary

{Overview paragraph summarizing findings}

**Profile Used:**
- Skills: {key skills}
- Level: {seniority}
- Constraints: {key constraints}

**Results:**
- Tier 1 (Strong Fit): {count} industries
- Tier 2 (Moderate Fit): {count} industries
- Tier 3 (Watch List): {count} industries

## Tier 1: Strong Fit

{Full analysis for each Tier 1 industry}

---

## Tier 2: Moderate Fit

{Analysis for each Tier 2 industry}

---

## Tier 3: Watch List

{Brief notes on Tier 3 industries}

---

## Methodology

This analysis was conducted on {date} using:
- Your resume and stated constraints
- Current market research via web search
- Scoring based on skills match (30%), compensation alignment (25%), remote fit (20%), growth trajectory (15%), and constraint compliance (10%)

**Note:** Industry conditions change. Consider re-running this analysis quarterly or when your constraints change.

## Sources

{List of web sources referenced with URLs and dates}
```

**6e. Confirm save:**

```
Saved: research/industries.md
```

### Step 7: Complete and Suggest Next Steps

**7a. Display completion summary and ask about next steps:**

```
Research complete! Your results are saved at `research/industries.md`.

**Top recommendations for your profile:**
1. {Top industry 1} — {one-line reason}
2. {Top industry 2} — {one-line reason}
3. {Top industry 3} — {one-line reason}

**What would you like to do next?**

The natural next step is to pick a Tier 1 industry and run `company-discovery` to find specific companies that are hiring. I can also re-run this analysis with different constraints if the results don't feel right.

Which industry interests you most?
```

**7b. Handle user selection:**

**If user selects an industry:**
```
Great choice! {Industry} has strong demand for your skills.

Want me to run company-discovery for {Industry}? I'll find specific companies hiring in this space that match your constraints.
```

If user confirms, suggest: "Say 'discover companies in {industry}' to start company-discovery"

**If user declines or wants to review later:**
```
No problem! Your industry research is saved at `research/industries.md`.

When you're ready to explore specific companies, just say "discover companies in {industry}" and I'll help you find opportunities.
```

## Output

Save the research to: `research/industries.md`

**Files created:**
- `research/industries.md` — Industry analysis with tiers, scores, and rationale (overwrites on re-run)

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** company-discovery
   **Rationale:** "Which industry do you want to explore? I'll find target companies"
   **Context to pass:** `research/industries.md` (tiered industry analysis), selected Tier 1 industry

2. Present the suggestion conversationally:
   "Industry research complete! Your Tier 1 (Strong Fit) industries are: {industry_1}, {industry_2}, {industry_3}.

   Which industry would you like to explore further? I'll discover specific companies that are hiring and match your constraints.

   [Pick an industry name/Something else]"

3. If user selects an industry: Load `workflows/company-discovery/workflow.md` and execute with that industry
4. If user declines: Summarize research and end gracefully
   "Your industry research is saved at `research/industries.md`. Come back anytime to explore specific companies."
5. If user requests different workflow: Honor their request
