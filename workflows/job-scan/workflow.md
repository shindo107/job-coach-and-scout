# Job Scan

## Summary

**Purpose:** Parse a job posting into structured requirements for fit analysis and tailoring
**Agent:** Job Scout
**Reads:**
- Job posting content (URL, file path, or pasted text)
- `profile/constraints.yaml` — For quick fit assessment (optional)
**Creates:**
- `research/openings/{company}-{role}.md` — Parsed job posting with categorized requirements
**Approximate time:** 5-10 minutes
**Prerequisites:** None (constraints.yaml recommended for fit assessment)

---

**Trigger:** User says "scan this job posting", "analyze this job", "help me understand this role", or provides a job posting URL/file

## Context Required

**Required:**
- Job posting content (via URL, file path, or direct paste)

**Optional:**
- `profile/constraints.yaml` — Job search constraints for quick fit assessment

## Steps

### Step 1: Obtain Job Posting Content

**Determine input method:**

Ask the user how they want to provide the job posting:

```
I'll analyze this job posting for you. How would you like to provide it?

1. **URL** — Paste the job posting URL and I'll fetch it
2. **File** — Provide a file path to a saved posting
3. **Paste** — Paste the job posting content directly

Which method works best for you?
```

**If user already provided a URL or file path in their initial request:**
Skip the prompt and proceed directly to the appropriate method below.

---

**Method A: URL Input**

1. Use WebFetch to retrieve the page content
2. Extract the job posting text from the page
3. Record the source URL for the output file
4. Proceed to Step 2

**If WebFetch fails (network error, 404, paywall, authentication required):**
```
I couldn't fetch that URL. This sometimes happens with:
- Job boards that require login (LinkedIn, some company portals)
- Pages behind paywalls or authentication
- Network issues or expired links

Would you like to:
1. Try a different URL?
2. Save the posting locally and give me the file path?
3. Paste the job posting content directly?
```

---

**Method B: File Path Input**

1. Use Read tool to load the file content
2. Record the file path as the source
3. Proceed to Step 2

**If file cannot be read:**
```
I couldn't read that file. Please check:
- The file path is correct
- The file exists and is readable

Would you like to:
1. Try a different path?
2. Paste the content directly?
```

---

**Method C: Direct Paste**

1. Accept the pasted content from the user
2. Record source as "User provided (pasted)"
3. Proceed to Step 2

### Step 2: Extract Company and Role Information

From the job posting, identify:

1. **Company name** — The employer (not the job board)
2. **Role title** — The exact job title
3. **Location** — Where the role is based (or "Remote")
4. **Employment type** — Full-time, contract, etc.

**Generate output filename:**
- Pattern: `{company}-{role}.md`
- Lowercase, hyphens for spaces
- Remove special characters
- Example: "Stripe" + "Staff Software Engineer" → `stripe-staff-software-engineer.md`

### Step 3: Parse Requirements

Analyze the job posting and extract requirements into categories:

**Technical Requirements:**
- Programming languages, frameworks, tools
- Specific technical skills mentioned
- Years of experience with technologies

**Experience Requirements:**
- Total years of experience
- Industry experience
- Role-specific experience (e.g., "led teams", "shipped products")
- Domain expertise

**Education & Certifications:**
- Degree requirements (if any)
- Certifications mentioned
- "Or equivalent experience" noted if present

**Soft Skills & Culture:**
- Communication, collaboration, leadership
- Work style expectations
- Company values alignment

**For each requirement extracted:**
- Label as **MUST-HAVE** or **NICE-TO-HAVE**
- Include the original text from the posting (quoted)
- Include brief rationale explaining the categorization

**Categorization Logic:**
- Label as **MUST-HAVE** if posting uses: "must have", "required", "minimum", "essential", "need", "mandatory"
- Label as **NICE-TO-HAVE** if posting uses: "preferred", "nice to have", "bonus", "ideally", "plus", "desired"
- When unclear, default to **MUST-HAVE** and note: "Assumed — not explicitly stated"

### Step 4: Quick Fit Assessment (if constraints available)

**If `profile/constraints.yaml` exists:**

First, validate the constraints file:
- If YAML is malformed or unreadable, note: "Could not parse constraints.yaml — skipping fit assessment. Run scoping-interview to regenerate."
- If expected fields are missing, proceed with available fields and note which comparisons were skipped.

Compare the posting against user's constraints:

| Constraint | User Preference | Posting | Match |
|------------|-----------------|---------|-------|
| Remote | {from constraints} | {from posting} | ✅/⚠️/❌ |
| Location | {from constraints} | {from posting} | ✅/⚠️/❌ |
| Seniority | {from constraints} | {from posting} | ✅/⚠️/❌ |
| Company Size | {from constraints} | {from posting} | ✅/⚠️/❌ |
| Industry | {from constraints} | {from posting} | ✅/⚠️/❌ |

**Quick verdict:**
- **Strong fit** — Meets all non-negotiables, most preferences
- **Potential fit** — Meets non-negotiables, some preference mismatches
- **Weak fit** — Misses some non-negotiables or major preferences
- **Not recommended** — Violates dealbreakers

---

**Dealbreaker Check:**

Check these constraint fields for dealbreaker violations (field paths match scoping-interview output):
- `location.dealbreakers` — Cities/regions user won't work in
- `industries.avoid` — Industries user won't work in
- `targeting.avoid_titles` — Job titles user won't accept
- `targeting.avoid_companies` — Specific companies to avoid

If a field doesn't exist in the user's constraints, skip that check silently.

**If any dealbreaker is violated:**

```
⚠️ **DEALBREAKER CONFLICT DETECTED**

The following conflicts with your stated dealbreakers:

| Dealbreaker Type | Your Constraint | This Posting |
|------------------|-----------------|--------------|
| {type} | "{your value}" | "{posting value}" |

This role is **not recommended** based on your constraints.

Would you like to:
1. Continue anyway (save analysis for reference)
2. Skip this posting and find alternatives
```

**Wait for user confirmation before proceeding to Step 5 if dealbreakers are violated.**

---

**If constraints not available:**
Note: "Quick fit assessment skipped — run scoping-interview to establish your constraints for personalized fit analysis."

### Step 5: Save Output File

**Check for existing files:**

Before saving, scan `research/openings/` for existing files matching this company/role.

**Detection logic:**
1. Look for exact match: `{company}-{role}.md`
2. Look for versioned files: `{company}-{role}-v2.md`, `{company}-{role}-v3.md`, etc.
3. Look for date-suffixed files: `{company}-{role}-2026-01-25.md`
4. Look for revision patterns: `{company}-{role}-rev2.md`, `{company}-{role}-r2.md`

**If any matching files found:**

```
I found existing analysis for {Company} - {Role}:

| File | Modified | Notes |
|------|----------|-------|
| {filename} | {file modified date} | {original/v2/dated} |

Which file should I update or replace? Or should I create a new version?

1. **Overwrite {most recent file}** — Replace with this new scan
2. **New version** — Save as {company}-{role}-v{next}.md
3. **Custom filename** — Let me specify the filename
4. **Cancel** — Keep existing and discard this scan
```

**If user chooses option 3 (custom):**
```
Enter the filename (will be saved to research/openings/):
```
Validate the filename follows conventions (lowercase, hyphens, .md extension).

**Version number detection:**
- Parse existing filenames for version indicators: `-v2`, `-v3`, `-rev2`, `-r2`
- Extract dates from filenames: `-2026-01-25`
- Use file modification dates as secondary signal
- Suggest next version number based on highest found

**If user chooses to cancel:** End workflow gracefully without saving.

---

**Write the parsed posting to output file:**

```markdown
# {Company} - {Role}

**Source:** {URL or file path or "User provided"}
**Date Scanned:** {current date}
**Location:** {location}
**Employment Type:** {type}

## Quick Fit Assessment

{Quick fit table and verdict, or note about missing constraints}

## Parsed Requirements

### Technical Requirements

| Requirement | Priority | Rationale | Original Text |
|-------------|----------|-----------|---------------|
| {skill} | MUST-HAVE/NICE-TO-HAVE | {trigger phrase or "Assumed"} | "{quoted text}" |

### Experience Requirements

| Requirement | Priority | Rationale | Original Text |
|-------------|----------|-----------|---------------|
| {experience} | MUST-HAVE/NICE-TO-HAVE | {trigger phrase or "Assumed"} | "{quoted text}" |

### Education & Certifications

| Requirement | Priority | Rationale | Original Text |
|-------------|----------|-----------|---------------|
| {education} | MUST-HAVE/NICE-TO-HAVE | {trigger phrase or "Assumed"} | "{quoted text}" |

### Soft Skills & Culture

| Requirement | Priority | Rationale | Original Text |
|-------------|----------|-----------|---------------|
| {skill} | MUST-HAVE/NICE-TO-HAVE | {trigger phrase or "Assumed"} | "{quoted text}" |

## Original Posting

{preserved original posting text}
```

**Confirm save:**
"Saved job posting analysis to `research/openings/{filename}`."

### Step 6: Summary and Next Steps

**Display summary:**

```
Job Posting Analyzed: {Company} - {Role}

Key Requirements:
- {top 3-5 requirements summarized}

Quick Fit: {verdict}

Saved to: research/openings/{filename}
```

**Suggest next workflow based on fit:**

- **Strong/Potential fit:** "Would you like me to evaluate your fit in detail? Run **evaluate-fit** for a comprehensive gap analysis."
- **Weak fit:** "This role has some mismatches with your preferences. Want to explore it anyway, or should we look for better matches?"
- **Not recommended:** "This role conflicts with your dealbreakers. Want me to explain why, or should we find alternatives?"

## Output

Save the result to: `research/openings/{company}-{role}.md`

**Files created:**
- `research/openings/{company}-{role}.md` — Parsed job posting with requirements and fit assessment

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** evaluate-fit OR fit-resume
   **Rationale:** "Posting parsed. Want a quick fit check or ready to start tailoring?"
   **Context to pass:** `research/openings/{company}-{role}.md` (parsed requirements), `profile/resume.md`, `profile/constraints.yaml`

2. Present the suggestion conversationally:
   "I've parsed the job posting for {Company} - {Role}. Would you like to:
   - **Evaluate your fit** — Get a detailed alignment score and gap analysis (read-only)
   - **Start tailoring** — Jump straight into resume tailoring with interview-driven extraction

   Which approach? [Evaluate fit/Start tailoring/Something else]"

3. If user chooses evaluate-fit: Load `workflows/evaluate-fit/workflow.md` and execute
4. If user chooses fit-resume: Load `workflows/fit-resume/workflow.md` and execute
5. If user declines: Summarize what was accomplished and end gracefully
6. If user requests different workflow: Honor their request
