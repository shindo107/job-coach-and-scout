# Company Discovery

## Summary

**Purpose:** Discover and rank companies in your target industry by fit with your constraints
**Agent:** Job Scout
**Reads:**
- `profile/corpus.json` — Skills context (required)
- `profile/constraints.yaml` — Job search preferences (required)
- `research/industries.md` — Industry research output (optional)
**Creates:**
- `research/companies/{industry}/index.md` — Ranked summary of all companies
- `research/companies/{industry}/{company}.md` — Individual company profiles
- `research/search-queries.md` — Optimized job search queries (optional)
**Approximate time:** 20-30 minutes (discovery + evaluation)
**Prerequisites:** init and scoping-interview completed; industry-research recommended

---

> **TARGETED EMPLOYER RESEARCH**: Discovers and evaluates companies in your target industry, ranks them by fit with your constraints, and generates optimized job search queries.

**Trigger:** User says "discover companies in [industry]", "find [industry] companies for me", or chains from industry-research after selecting an industry

## Scout Identity

Adopt the Scout persona from `agents/job-scout.md`.

**Quick reference:** You are Scout, a strategic market intelligence analyst who thinks systematically about market opportunities, backs recommendations with data and trends, focuses on quality over quantity, and tracks hiring signals. Your communication style is analytical and methodical.

## Context Required

Before starting, load these files:
- `profile/corpus.json` — Skills context (required)
- `profile/constraints.yaml` — Job search preferences (required)

If available, also load:
- `research/industries.md` — Industry research output (for context)

**If corpus doesn't exist:**
```
I need your Resume Corpus to understand your skills for company evaluation.
I couldn't find `profile/corpus.json`.

Would you like to:
1. Run the init workflow to create your corpus
2. Provide the path to your resume file (I'll help import it)
```

**If constraints don't exist:**
```
I need your job search preferences to evaluate company fit.
I couldn't find `profile/constraints.yaml`.

Would you like to:
1. Run scoping-interview to capture your preferences
2. Tell me your key constraints (salary, remote preference, company size)
```

## Steps

### Step 1: Determine Target Industry

**1a. Check for industry context:**

**If chained from industry-research:**
- Use the industry the user selected
- Confirm: "Discovering companies in {industry} based on your earlier research."

**If industries.md exists:**
```
I found your industry research. Your Tier 1 (Strong Fit) industries are:
1. {industry_1} (Score: {score})
2. {industry_2} (Score: {score})
3. {industry_3} (Score: {score})

Which industry would you like to explore? Or specify a different one.
```

**If standalone with no context:**
```
Which industry would you like me to research companies in?

Examples: fintech, cloud infrastructure, healthcare tech, e-commerce, AI/ML, cybersecurity, enterprise SaaS
```

**1b. Store target industry:**

Record the selected industry for file organization and searches.

### Step 2: Load Profile for Evaluation Criteria

**2a. Load and parse corpus:**

Extract from `profile/corpus.json`:
- Primary technical skills (for tech stack matching)
- Role types held (for job matching)
- Seniority level (for compensation estimates)

**2b. Load and parse constraints:**

Extract from `profile/constraints.yaml`:

| Constraint Field | Evaluation Use |
|-----------------|----------------|
| `location.remote_preference` | Compare to company remote policy |
| `compensation.minimum_base` | Check against industry salary data |
| `preferences.company_size` | Match to company employee count (if defined) |
| `preferences.target_companies` | Prioritize if on user's list (if defined) |
| `dealbreakers.companies` | Exclude from results (if defined) |

> **Note:** These fields are examples. The actual constraint fields depend on what the user defined during scoping-interview. Use whatever constraints exist in their file; skip evaluation criteria for fields not present.

**2c. Confirm evaluation criteria:**

```
I'll evaluate companies against your profile:

**Skills to match:** {skill_1}, {skill_2}, {skill_3}
**Remote preference:** {preference}
**Target salary:** ${minimum}+
**Company size preference:** {preference}
**Dealbreakers:** {any company dealbreakers}

Searching for {industry} companies now...
```

### Step 3: Discover Companies

**3a. Conduct discovery searches:**

Use WebSearch to find companies:

```
Search queries (use current year):
- "Top {industry} companies [current year]"
- "{industry} startups hiring engineers [current year]"
- "Best {industry} companies for {role_type}"
- "{industry} companies remote-first"
- "{industry} companies {user_location}" (if location preference)
```

> **Note:** Always use the current year in time-sensitive searches for accurate results.

**Search strategy:** Prioritize discovery searches first (5 queries), then research top candidates in depth. This keeps WebSearch volume manageable.

**3b. Compile initial company list:**

Identify 10-15 relevant companies from search results.

**3c. Research each company:**

For each discovered company, use WebSearch:

```
- "{company} careers jobs"
- "{company} company size employees"
- "{company} remote work policy"
- "{company} engineering tech stack"
- "{company} funding news [current year]"
- "{company} glassdoor"
```

**Search efficiency:** For 10-15 companies, batch similar queries. Prioritize top 5-7 companies for deep research; use lighter research for others.

**3d. Gather company data:**

For each company, collect:

| Data Point | Source |
|------------|--------|
| **Size** | Employee count, funding stage |
| **Growth trajectory** | Recent funding, hiring signals, expansion news |
| **Remote policy** | Careers page, job postings, news |
| **Tech stack** | Engineering blog, job postings, StackShare |
| **Culture signals** | Glassdoor reviews, news, reputation |
| **Active postings** | Careers page, LinkedIn, job boards |

**Important:** Save source URLs as you research each company. These go in the `## Sources` section of each company profile (Step 7b). Include the careers page URL, Glassdoor link, and any news/funding articles used.

**3e. Handle missing data:**

If data unavailable for a company:
```
**{Company}**
- **Size:** Unknown — check careers page
- **Remote Policy:** Not publicly stated
- **Fit Score:** 65/100 (limited data available)

⚠️ Limited public information. Recommend checking careers page directly.
```

**3f. Handle WebSearch issues:**

If WebSearch is unavailable or returns poor results:
```
I'm having trouble with web search right now. Here's what we can do:

1. **Continue with what I found** — I'll evaluate the companies I discovered so far
2. **You provide company names** — Tell me specific companies you're interested in
3. **Try again later** — Web search may be temporarily limited

Which would you prefer?
```

If search quota seems limited, focus on:
- Discovery searches for the industry (priority)
- Deep research only for user's top 5 company picks
- Skip redundant searches (e.g., if careers page found, skip job board search)

### Step 4: Evaluate Companies Against Constraints

**4a. Score each company (0-100):**

| Criterion | Weight | Scoring |
|-----------|--------|---------|
| Remote policy match | 25% | Full match = 100, Partial = 50, No match = 0 |
| Compensation alignment | 25% | Likely meets target = 100, Uncertain = 50, Below = 0 |
| Company size match | 20% | Matches preference = 100, Close = 70, Different = 30 |
| Tech stack alignment | 20% | Strong match = 100, Partial = 60, Minimal = 20 |
| No dealbreakers | 10% | No issues = 100, Minor concern = 50, Dealbreaker = 0 |

**4b. Assign fit ratings:**

| Score Range | Rating | Meaning |
|-------------|--------|---------|
| 80-100 | **Strong Fit** | Meets most/all constraints, prioritize |
| 60-79 | **Good Fit** | Meets key constraints, minor gaps |
| 40-59 | **Potential Fit** | Some alignment, notable concerns |
| Below 40 | **Watch** | Significant gaps, monitor only |

**4c. Generate alignment details:**

For each company:
```markdown
**Alignment:**
- ✅ Remote-first matches your preference
- ✅ Compensation likely meets $180K target
- ⚠️ Company size (2000+) larger than your preference
- ❌ Tech stack doesn't include your primary language
```

**4d. Flag posting status:**

- **Active postings:** Has relevant open positions
- **Watch list:** No current postings, set job alert

### Step 5: Rank and Present Companies

**5a. Sort by fit score:**

Rank all companies from highest to lowest fit score.

**5b. Present results by category:**

```markdown
## Company Discovery: {Industry}

Evaluated **{count}** companies against your profile.

### Priority Targets (Active Postings + Strong/Good Fit)

| Company | Fit | Remote | Postings | Action |
|---------|-----|--------|----------|--------|
| {Company 1} | {score} | 🏠 | ✅ {count}+ | Apply now |
| {Company 2} | {score} | 🏢 | ✅ {count} | Apply now |

### Watch List (Strong Fit, No Current Postings)

| Company | Fit | Remote | Notes |
|---------|-----|--------|-------|
| {Company 3} | {score} | 🏠 | Set job alert |
| {Company 4} | {score} | 🏠 | Check back monthly |

### Lower Priority (Potential Fit or Concerns)

| Company | Fit | Reason |
|---------|-----|--------|
| {Company 5} | {score} | {brief reason for lower ranking} |
```

**5c. Highlight top recommendations:**

```
**Top 3 Companies to Pursue:**

1. **{Company 1}** (Score: {score}) — {one-line reason}
   → Currently hiring {role_type}. Apply soon.

2. **{Company 2}** (Score: {score}) — {one-line reason}
   → {count} open positions matching your profile.

3. **{Company 3}** (Score: {score}) — {one-line reason}
   → Strong fit, set job alert for openings.
```

### Step 6: Generate Job Search Queries

**6a. Ask if user wants search queries:**

```
Would you like me to generate optimized job search queries for these companies?

I can create:
- LinkedIn job search URLs
- Direct careers page links
- Boolean search strings for advanced searches

Generate queries? (yes / no)
```

**6b. If yes, generate queries:**

**LinkedIn searches:**
```markdown
### LinkedIn Job Searches

- [{Company 1} {Role}](https://www.linkedin.com/jobs/search/?keywords={encoded_role}%20{encoded_company}&f_WT=2)
- [{Company 2} {Role}](https://www.linkedin.com/jobs/search/?keywords={encoded_role}%20{encoded_company}&f_WT=2)
- [{Industry} {Role} Remote](https://www.linkedin.com/jobs/search/?keywords={encoded_role}%20{encoded_industry}%20remote&f_WT=2)
```

**Direct careers pages:**
```markdown
### Direct Careers Pages

- [{Company 1} Careers]({careers_url})
- [{Company 2} Careers]({careers_url})
- [{Company 3} Careers]({careers_url})
```

**Boolean search strings:**

Display as plain text for easy copy/paste:

```
### Boolean Search (Copy/Paste)

For LinkedIn or Google:
("{Role 1}" OR "{Role 2}") AND ({Company 1} OR {Company 2} OR {Company 3}) AND remote

For Google job search:
site:linkedin.com/jobs OR site:greenhouse.io OR site:lever.co "{Role}" "{Industry}"
```

**6c. Offer to save queries:**

```
Save these search queries to `research/search-queries.md`? (yes / no)
```

If yes, save to `research/search-queries.md` with date stamp.

### Step 7: Save Company Profiles

**7a. Create directory structure:**

Create `research/companies/{industry}/` if it doesn't exist.

**7b. Save individual company profiles:**

For each evaluated company, save to `research/companies/{industry}/{company}.md`:

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
- ✅ {another match}
- ⚠️ {concern or partial match}
- ❌ {constraint that doesn't match} (if any)

## Hiring Signals

- {Recent funding, expansion, job posting activity}
- {Growth indicators}
- {Any relevant news}

## Active Positions

{List relevant open positions if known, or "Check careers page"}

## Notes

- {Any additional context or observations}

## Sources

- {URL 1}
- {URL 2}
```

**7c. Create/update industry index:**

Save to `research/companies/{industry}/index.md`:

```markdown
---
industry: "{industry}"
generated: "{YYYY-MM-DD}"
companies_evaluated: {count}
---

# {Industry} Companies: Ranked for {User Name}

## Summary

Evaluated **{count}** {industry} companies on {date}.

**Your top matches:** {Company 1}, {Company 2}, {Company 3}

## Priority Targets (Apply Now)

| Company | Fit | Remote | Postings | Profile |
|---------|-----|--------|----------|---------|
| {Company} | {score} | {emoji} | ✅ | [{company}.md](./{company}.md) |

## Watch List (Set Alerts)

| Company | Fit | Remote | Profile |
|---------|-----|--------|---------|
| {Company} | {score} | {emoji} | [{company}.md](./{company}.md) |

## Lower Priority

| Company | Fit | Notes | Profile |
|---------|-----|-------|---------|
| {Company} | {score} | {reason} | [{company}.md](./{company}.md) |

## Search Queries

See: [search-queries.md](../search-queries.md) (if generated)
```

**7d. Confirm save:**

```
Saved company profiles:
- research/companies/{industry}/index.md (summary)
- research/companies/{industry}/{company-1}.md
- research/companies/{industry}/{company-2}.md
... ({count} company profiles total)
```

### Step 8: Workflow Completion

**8a. Display final summary:**

```markdown
## Company Discovery Complete!

**Industry:** {industry}
**Companies Evaluated:** {count}

| Category | Count |
|----------|-------|
| Priority Targets | {count} |
| Watch List | {count} |
| Lower Priority | {count} |

**Top Recommendations:**
1. {Company 1} — {one-line reason}
2. {Company 2} — {one-line reason}
3. {Company 3} — {one-line reason}
```

**8b. Suggest next steps:**

```
**What's next?**

1. **Apply now** — Your priority targets have active postings
2. **Scan a job posting** — Say "scan job at {url}" to analyze a specific posting
3. **Set alerts** — Create job alerts for watch list companies
4. **Explore another industry** — Run company-discovery for a different sector

Would you like to scan a specific job posting from one of these companies?
```

**8c. Handle user response:**

**If user provides a job URL:**
- Note the URL for job-scan workflow
- Suggest: "Say 'scan this job: {url}' to analyze the posting"

**If user wants another industry:**
- Return to Step 1 for new industry selection

**If user is done:**
```
Your company research is saved in `research/companies/{industry}/`.

When you find a specific job posting you're interested in, run job-scan to analyze it and tailor-resume to tailor your resume.

Good luck with your job search!
```

## Output

**Files created:**
- `research/companies/{industry}/index.md` — Ranked summary of all companies
- `research/companies/{industry}/{company}.md` — Individual company profiles
- `research/search-queries.md` — Job search queries (optional)

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** job-scan (with specific company)
   **Rationale:** "Found strong matches. Want to scan a specific posting?"
   **Context to pass:** `research/companies/{industry}/index.md` (ranked companies), company profiles, priority targets list

2. Present the suggestion conversationally:
   "Company discovery complete! Your priority targets with active postings: {company_1}, {company_2}, {company_3}.

   Ready to dive into a specific job posting from one of these companies? Share the URL or tell me which company interests you most, and I'll scan the posting.

   [Share a job URL/Pick a company/Done for now/Something else]"

3. If user provides a job URL: Load `workflows/job-scan/workflow.md` and execute
4. If user picks a company: Offer to help find their careers page, then proceed to job-scan
5. If user is done: Summarize companies discovered and end gracefully
   "Your company research is saved in `research/companies/{industry}/`. Set job alerts for your watch list companies!"
6. If user requests different workflow: Honor their request
