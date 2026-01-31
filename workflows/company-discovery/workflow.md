# Company Discovery & Enrichment

## Summary

**Purpose:** Discover new companies or enrich known targets in a specific industry, creating detailed, structured profiles.
**Agent:** Job Scout
**Phase:** research
**Reads:**
- `profile/corpus.json` — Skills context (required)
- `profile/constraints.yaml` — Job search preferences (required)
- `research/industries/index.md` — To identify Tier 1 industries
- `research/companies/{industry}/` — To find existing company stubs
**Creates:**
- `research/companies/{industry}/index.md` — Ranked summary of all companies
- `research/companies/{industry}/{company}.md` — Individual company profiles (new or enriched)
**Updates:** None
**Prerequisites:** init and scoping-interview completed; industry-research recommended

---

> **TARGETED EMPLOYER RESEARCH**: Fills out detailed intelligence reports on specific companies or discovers new ones in a target industry, populating a durable knowledge base.

**Trigger:** User wants to find companies in an industry ("discover companies in fintech") or learn more about a specific one ("tell me more about Stripe").

## Persona

**Load and adopt:** `agents/job-scout.md`. Use Scout's analytical, data-driven approach.

## Step 1: Determine Mode (Discover vs. Enrich)

**Instruction:**
- Analyze the user's request. Are they targeting a broad industry ("fintech") or a specific company ("Stripe")?
- **If specific company:** Go to **Enrichment Mode (Step 2)**.
- **If broad industry:** Go to **Discovery Mode (Step 3)**.
- **If no target:** Prompt the user. Check `research/industries/index.md` for Tier 1 industries and suggest them. "Your top industries from previous research are {list}. Which would you like to explore, or do you have a new target in mind?"

---

## Enrichment Mode

### Step 2: Enrich a Known Company Target

**Instruction:** This mode is for filling in the details for a single, known company.

**2a. Identify Target File:**
- Locate the company's file, which may be an empty stub from `industry-research`. E.g., `research/companies/{industry}/{company-name}.md`. If it doesn't exist, create it.

**2b. Conduct Focused Research:**
- **Instruction:** Your goal is to populate all the fields in the company's profile file. Run targeted WebSearch queries to find the necessary data.
- **Example Queries:** `"{company} remote work policy"`, `"{company} engineering tech stack blog"`, `"{company} glassdoor salary {role_type}"`, `"{company} recent funding news"`.

**2c. Gather and Synthesize Data:**
- **Instruction:** Collect the data points required for the profile: Size, Stage, Founded, Remote Policy, Tech Stack, Headquarters, Hiring Signals, Active Positions, etc.
- **CRITICAL:** For each data point, record the source URL.

**2d. Score and Rate:**
- **Instruction:** Score the company from 0-100 against the user's `constraints.yaml`, just as in the original workflow. Assign a fit rating (Strong Fit, Good Fit, etc.).

**2e. Generate Search Links:**
- **Instruction:** Create direct search links for finding jobs at this company.
- **Example:** `[Search for {Role} jobs at {Company} on LinkedIn]({linkedin_url})`.

**2f. Populate and Save Profile:**
- **Instruction:** Overwrite the stub file with a complete profile containing all the researched data, the fit score, alignment details, hiring signals, and the new `## Search Links` section.
- Go to **Step 5: Completion**.

---

## Discovery Mode

### Step 3: Discover Companies in an Industry

**Instruction:** This mode is for a broad search within a single industry.

**3a. Check for Existing Stubs:**
- **Instruction:** Before any web searches, check the `research/companies/{industry}/` directory for existing stub files created by `industry-research`.
- **Instruction:** If stubs exist, present them to the user as a prioritized work queue. "I've found some notable companies from the initial industry research: {list of companies}. Would you like to start by doing a deep dive on one of these, or should I search for new companies?"
- **If user selects a company:** Switch to **Enrichment Mode (Step 2)** for that company.
- **If user wants new discovery:** Proceed to the next step.

**3b. Conduct Broad Discovery Searches:**
- **Instruction:** Use WebSearch to find a list of new, relevant companies in the target industry that were not previously identified.
- **Example Queries:** `"top {industry} companies hiring {role_type}"`, `"{industry} startups 2026"`.

**3c. Create a Work Queue:**
- **Instruction:** From the search results, compile a list of 5-10 promising new companies to investigate. Present this list to the user for approval before proceeding with deep-dive research on each one.

**3d. Loop for Enrichment:**
- **Instruction:** For each approved company in the work queue, perform the full enrichment process described in **Enrichment Mode (Step 2)**, creating a complete, scored profile file for each one.

**3e. Generate/Update the Industry Index:**
- **Instruction:** After all companies in the queue have been researched, create or update the `research/companies/{industry}/index.md` file.
- **Instruction:** This file should contain a ranked summary table of all companies evaluated in that industry, including their fit score, key attributes, and a link to their detailed profile file.

### Step 4: Present Discovery Results

**Instruction:**
- Announce completion and present the ranked table from the `index.md` file.
- Highlight the top 3 recommendations and provide a one-line reason for each.

---

### Step 5: Completion and Next Steps

**Instruction:**
- Summarize what was created (e.g., "I've enriched the profile for Stripe and saved it.") or ("I've discovered and profiled 7 new companies in Fintech. The summary is in the index file.").
- Suggest a relevant next step.
- **Example after Enrichment:** "The profile for Stripe is now complete. Based on their 'Strong Fit' rating and active job postings, the next logical step is to `job-scan` a specific role there. Shall I look for their careers page?"
- **Example after Discovery:** "My discovery for the Fintech industry is complete. Your top matches are {list companies}. Would you like to `job-scan` a role at one of these, or `discover` companies in another industry?"

## Output File Structure

### Company Profile (`research/companies/{industry}/{company}.md`)
```markdown
---
company: "{Company Name}"
industry: "{industry}"
evaluated: "{YYYY-MM-DD}"
fit_score: {score}
fit_rating: "{Strong Fit|Good Fit|Potential Fit|Watch}"
has_active_postings: {true|false}
---

# {Company Name}

## Overview
- **Size:** {employees} employees
- **Stage:** {startup/growth/enterprise}
- **Founded:** {year if known}
- **Remote Policy:** {remote-first/hybrid/in-office}
- **Tech Stack:** {known technologies}
- **Headquarters:** {location}

## Fit Assessment
**Score:** {score}/100 — {rating}

**Alignment:**
- ✅ {constraint that matches}
- ⚠️ {concern or partial match}

## Hiring Signals
- {Recent funding, expansion, job posting activity}

## Active Positions
{List relevant open positions if known, or "Check careers page"}

## Tracked Openings
<!-- This section is auto-updated by job-scan workflow -->
| Role | Fit Score | Date Scanned | Analysis |
|------|-----------|--------------|----------|
<!-- Openings will be added here as you scan them -->

## Search Links
- [Search for {Role} jobs at {Company} on LinkedIn]({url})
- [{Company} Careers Page]({url})

## Sources
- {URL 1 used for this company's research}
- {URL 2 used for this company's research}
```

### Industry Index (`research/companies/{industry}/index.md`)
```markdown
---
industry: "{industry}"
generated: "{YYYY-MM-DD}"
companies_evaluated: {count}
---

# {Industry} Companies: Ranked for {User Name}

## Summary
Evaluated **{count}** {industry} companies on {date}. Your top matches are {Company 1}, {Company 2}.

## Company Rankings
| Company | Fit Score | Remote | Postings | Profile Link |
|---|---|---|---|---|
| {Company 1} | {score} | 🏠 | ✅ | [{company}.md](./{company}.md) |
| {Company 2} | {score} | 🏢 | ✅ | [{company}.md](./{company}.md) |
```

## Cross-Workflow Integration

### Tracked Openings

The `## Tracked Openings` section in each company profile is automatically populated by the `job-scan` workflow. When you scan a job posting:

1. `job-scan` saves the analysis to `research/openings/{company}-{role}.md`
2. `job-scan` searches for a matching company profile in `research/companies/{industry}/`
3. If found, the company profile's "Tracked Openings" table is updated with:
   - Role title
   - Fit score (%)
   - Date scanned
   - Link to the full analysis

This creates a per-company view of all openings you've analyzed, making it easy to:
- See all opportunities at a target company in one place
- Track how your fit score varies across different roles
- Quickly navigate to detailed analyses

**To populate Tracked Openings:** Run `job-scan` on job postings from companies you've profiled.

## Recommend Next
After this workflow completes, suggest **job-scan** for a high-fit company with active postings.

