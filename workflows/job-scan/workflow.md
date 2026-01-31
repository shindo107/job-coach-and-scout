# Job Scan

## Summary

**Purpose:** Search for jobs at a company OR parse a specific job posting into structured requirements. Identifies skill gaps and updates the market skills database. Intelligently detects duplicate postings and re-validates existing analyses.
**Agent:** Job Scout
**Phase:** research
**Reads:**
- Job posting content (URL, file path, pasted text, OR company name for search mode)
- `profile/corpus.json` — For skill gap analysis
- `profile/constraints.yaml` — For dealbreaker and preference checks
- `research/market_skills.json` — The central database of all skills seen in the market
- `research/openings/*.md` (optional) — Existing analyses for duplicate detection
- `research/companies/{industry}/{company}.md` (optional) — Company profile for cross-referencing openings
**Creates:**
- `research/openings/{company}-{role}.md` — Parsed job posting with categorized requirements
**Updates:**
- `research/market_skills.json` — Enriched with the skills from this job posting
- `research/companies/{industry}/{company}.md` (conditional) — Tracked Openings section
**Prerequisites:** `corpus.json` and `constraints.yaml` are highly recommended for full functionality

---

**Trigger:** User says "scan this job posting", "analyze this job", "find jobs at [company]", "scan jobs at [company]", or provides a job posting URL/file. Also triggers on "re-scan" or "re-validate" requests for previously analyzed roles.

## Persona

**Load and adopt:** `agents/job-scout.md`. Embody Scout's analytical, data-driven approach.

## Steps

### Step 0: Detect Input Mode

**Instruction:** Determine whether the user is providing a specific job posting OR wants to search for jobs at a company.

**Indicators of Search Mode (company name):**
- Input is a company name without a URL or file path (e.g., "Stripe", "Google", "Acme Corp")
- User says "find jobs at...", "search jobs at...", "scan jobs at...", "what's open at..."
- Input doesn't contain `/`, `.com`, `.html`, `.md`, `.txt`, or other URL/file indicators

**Indicators of Direct Mode (URL/file/paste):**
- Input contains a URL (http://, https://, or recognizable domain)
- Input is a file path (contains `/` or file extension like `.md`, `.txt`)
- User explicitly says "scan this posting" or "analyze this job"
- User pastes job posting content directly

**If Search Mode detected:** Proceed to **Step 0a: Company Job Search**
**If Direct Mode detected:** Proceed to **Step 1: Obtain Job Posting Content**

### Step 0a: Company Job Search

**Instruction:** Search for current job openings at the specified company and let the user select which to scan.

**0a-i. Load User Context:**
- **Instruction:** Load `profile/corpus.json` and `profile/constraints.yaml` to understand what roles to prioritize.
- **Instruction:** Extract the user's target role types, seniority level, and location preferences.

**0a-ii. Search for Openings:**
- **Instruction:** Use WebSearch to find current job openings at the company.
- **Example queries:**
  - `"{company}" careers {role_type} jobs 2026`
  - `"{company}" hiring {seniority} engineer`
  - `site:linkedin.com/jobs "{company}" {role_type}`
  - `site:greenhouse.io "{company}"` or `site:lever.co "{company}"`
- **Instruction:** Also attempt to find the company's careers page directly:
  - `"{company}" careers page`
  - Try common patterns: `{company}.com/careers`, `careers.{company}.com`, `jobs.lever.co/{company}`

**0a-iii. Compile and Filter Results:**
- **Instruction:** From the search results, compile a list of current openings.
- **Instruction:** For each opening, extract:
  - Role title
  - Location (or "Remote" if applicable)
  - URL to the job posting
  - Brief description if available
- **Instruction:** Filter and prioritize based on user's constraints:
  - Roles matching their target role type appear first
  - Roles matching their seniority level are highlighted
  - Roles violating dealbreakers (e.g., wrong location) are flagged with ⚠️
- **Instruction:** Limit to 10 most relevant openings.

**0a-iv. Present Openings to User:**
- **Instruction:** Present the list for user selection:
  ```
  📋 Found {N} openings at {Company}:

  1. Staff Software Engineer, Infrastructure — San Francisco (Remote eligible)
     https://boards.greenhouse.io/stripe/jobs/12345
  2. Senior Backend Engineer, Payments — Seattle
     https://boards.greenhouse.io/stripe/jobs/12346
  3. ⚠️ Engineering Manager, Platform — NYC (on-site only)
     https://boards.greenhouse.io/stripe/jobs/12347
  4. Software Engineer, Connect — Remote
     https://boards.greenhouse.io/stripe/jobs/12348

  ⚠️ = May conflict with your location preferences

  Which would you like me to scan?
  - Enter a number (e.g., "1")
  - Enter multiple numbers (e.g., "1, 3, 4")
  - Enter "all" to scan all of them
  - Enter "none" to cancel
  ```

**0a-v. Handle User Selection:**
- **If user selects one posting:** Set the URL as the source and proceed to **Step 1**.
- **If user selects multiple postings:**
  - Process each posting sequentially through Steps 1-7.
  - Between postings, show brief progress: "Completed {N} of {M} scans. Continuing with {next role}..."
  - At the end, show a summary table of all scans with fit scores.
- **If user selects "all":** Process all postings as above.
- **If user selects "none":** End the workflow gracefully.

**0a-vi. If No Openings Found:**
- **Instruction:** If the search yields no results:
  ```
  I couldn't find current openings at {Company} matching your profile.

  This could mean:
  - They're not actively hiring for your role type
  - Their jobs are posted on a platform I couldn't search
  - The company name might be spelled differently

  Would you like to:
  1. Try a different spelling or company name?
  2. Provide a direct URL to a job posting?
  3. Search for jobs at a different company?
  ```

### Step 1: Obtain Job Posting Content

**Instruction:** Determine the user's preferred input method and retrieve the job posting content.

**Note:** If coming from Step 0a, the URL has already been determined. Proceed directly to fetching.

**If user provides a URL:**
1. Use WebFetch to retrieve the page content.
2. Extract the job posting text from the page.
3. Record the source URL for the output file.

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

**If user provides a file path:**
1. Use Read tool to load the file content.
2. Record the file path as the source.

**If file cannot be read:**
```
I couldn't read that file. Please check:
- The file path is correct
- The file exists and is readable

Would you like to:
1. Try a different path?
2. Paste the content directly?
```

**If user pastes content directly:**
1. Accept the pasted content from the user.
2. Record source as "User provided (pasted)".

### Step 2: Extract Company and Role Information

**Instruction:**
- From the content, identify the company name, role title, location, and employment type.
- Generate a standardized filename for the output, e.g., `stripe-staff-software-engineer.md`.

### Step 2b: Intelligent Duplicate Detection

**Instruction:** Before proceeding with full analysis, check if this job has already been scanned to avoid duplicate entries and wasted effort. Use a two-phase approach: exact URL match first, then fuzzy matching.

**2b-i. Exact URL Search (if source is a URL):**
- **Instruction:** If the job posting was provided via URL, search for that exact URL in existing opening files.
- **Instruction:** Use Grep to search file contents: `grep -l "{exact-url}" research/openings/*.md`
- **Instruction:** If a match is found:
  ```
  ✓ Found exact URL match in: `research/openings/{filename}`

  This job posting has already been scanned.
  ```
  - Read the existing file and extract: date scanned, fit score, and verdict.
  - Present options:
    1. **Re-validate** — Check if the posting has changed since last scan
    2. **View existing analysis** — Open the file without re-scanning
    3. **Cancel** — Stop here
  - If user chooses "Re-validate", proceed to **2b-v. Re-validation Flow**.
  - If user chooses "View existing" or "Cancel", skip to Step 7 (summary only) or end.
- **Instruction:** If no URL match is found, proceed to **2b-ii**.

**2b-ii. Scan Existing Openings (for fuzzy matching):**
- **Instruction:** List all files in `research/openings/` using Glob pattern `research/openings/*.md`.
- **Instruction:** If the directory is empty, skip to Step 3.

**2b-iii. Fuzzy Match Detection:**
- **Instruction:** Only perform this step if the exact URL search (2b-i) did not find a match.
- **Instruction:** For each existing file, extract the company and role from the filename (format: `{company}-{role}.md`).
- **Instruction:** Compare against the current job posting using these matching criteria:
  - **Company match:** Case-insensitive comparison, ignoring common suffixes (Inc, Corp, LLC, Ltd). Also check for common abbreviations (e.g., "IBM" vs "International Business Machines").
  - **Role match:** Check for semantic similarity—treat these as equivalent:
    - "Senior" / "Sr." / "Sr"
    - "Staff" / "Principal" / "Lead" (similar seniority)
    - "Software Engineer" / "Software Developer" / "SWE"
    - "Frontend" / "Front-end" / "Front End"
    - "Backend" / "Back-end" / "Back End"
    - "Full Stack" / "Fullstack" / "Full-Stack"
- **Instruction:** A potential duplicate exists if the company matches AND the role is semantically similar.

**2b-iv. If Potential Fuzzy Match Found:**
- **Instruction:** Read the existing file and extract key details: date scanned, source URL, and the Fit Score/Verdict.
- **Instruction:** Present the finding to the user:
  ```
  📋 I found an existing analysis that may be for this same role:

  **Existing:** `research/openings/{existing-filename}`
  - Scanned: {date}
  - Source: {original URL or source}
  - Fit Score: {X}% ({verdict})

  **Current posting:**
  - Company: {company}
  - Role: {role}
  - Source: {current URL or source}

  Is this the same job posting?
  ```
- **Instruction:** Offer these options:
  1. **Yes, re-validate existing** — Compare the new posting against the stored analysis, update any changed requirements, and refresh the fit assessment.
  2. **No, this is a different role** — Proceed to create a new analysis (may prompt for a disambiguated filename like `{company}-{role}-remote.md` or `{company}-{role}-v2.md`).
  3. **Skip** — Cancel the scan entirely.

**2b-v. Re-validation Flow (if user chooses re-validate):**
- **Instruction:** This flow updates an existing analysis rather than creating from scratch.
- **Instruction:** Parse the new posting content and compare against the stored requirements:
  - Identify **added requirements** (in new but not in old)
  - Identify **removed requirements** (in old but not in new)
  - Identify **changed priority** (MUST-HAVE ↔ NICE-TO-HAVE)
  - Identify **wording changes** (same requirement, different phrasing)
- **Instruction:** Present a diff summary to the user:
  ```
  📊 Re-validation Results for {company} - {role}

  **Changes detected:**
  ➕ Added:
    - {new requirement} (MUST-HAVE)
  ➖ Removed:
    - {old requirement that's no longer listed}
  🔄 Priority Changed:
    - "Python" upgraded from NICE-TO-HAVE → MUST-HAVE
  📝 Wording Updated:
    - "3+ years experience" → "5+ years experience"

  **No changes:** {list of requirements that are identical}
  ```
- **Instruction:** If changes are detected:
  - Update the stored file with the new requirements
  - Update the "Date Scanned" to today
  - Preserve the original source URL but add the new source as "Re-validated from: {new source}"
  - Re-run the Corpus Skill Gap Analysis (Step 4a) with the updated requirements
  - Re-run the Constraints Check (Step 4b) if requirements changed
- **Instruction:** If no changes are detected:
  ```
  ✅ No changes detected. The existing analysis is still current.
  Last scanned: {date} | Verdict: {fit verdict}
  ```
  - Ask if the user wants to re-run the fit assessment anyway (useful if their corpus has changed).
- **Instruction:** After re-validation, skip to Step 6 (Update Market Skills) and Step 7 (Summary).

**2b-vi. If No Duplicates Found:**
- **Instruction:** If neither the exact URL search (2b-i) nor the fuzzy match (2b-iii) found duplicates, proceed to Step 3 for full analysis.

### Step 3: Parse Requirements

**Instruction:**
- Analyze the job posting and extract all requirements.
- Categorize each requirement into: `Technical`, `Experience`, `Education & Certifications`, and `Soft Skills & Culture`.
- Label each requirement as **MUST-HAVE** or **NICE-TO-HAVE** based on trigger words ("required", "preferred", etc.). If unclear, default to MUST-HAVE.
- For each requirement, include the original quoted text and the rationale for the priority.
- **Empowered Analysis:** If a requirement is notably vague ("synergy"), rare, or stringent ("PhD required"), add a `Note:` with your analytical commentary.

### Step 4: Quick Fit Assessment

**Instruction:** This is a multi-part assessment. Perform all parts if the necessary files are available.

**4a. Corpus Skill Gap Analysis (CRITICAL):**
- **Instruction:** Compare the list of parsed **MUST-HAVE Technical Requirements** against the skills present in `profile/corpus.json`.
- **Instruction:** If there are any MUST-HAVE skills from the job posting that are NOT in the user's corpus, this is a **Critical Gap**.
- **Instruction:** The primary output of this step is a clear warning to the user.
- **Example Output:**
    ```
    ### 🚨 Critical Skill Gaps Detected
    This role lists the following as MUST-HAVE skills, but they are missing from your resume corpus:
    - **Kubernetes**
    - **Go**
    - **Terraform**

    Addressing these gaps in the `tailor-resume` workflow will be essential.
    ```
- If no gaps are found, state that explicitly: "✅ No critical skill gaps found between the job's must-have requirements and your corpus."

**4b. Constraints & Dealbreaker Check:**
- **Instruction:** If `profile/constraints.yaml` exists, compare the posting's details (location, seniority, etc.) against the user's preferences.
- **Instruction:** Explicitly check for any dealbreaker violations (e.g., role is in a city on the `location_dealbreakers` list).
- **Instruction:** If a dealbreaker is found, present a strong warning and ask the user if they wish to proceed.

**4c. Calculate Numerical Fit Score:**
- **Instruction:** Calculate a numerical fit score (0-100%) based on requirement coverage and constraint alignment.
- **Scoring methodology:**
  1. **Requirement Coverage (70% of score):**
     - For each requirement, check if evidence exists in the corpus (skills, accomplishments, positions)
     - MUST-HAVE requirements: 10 points each (full match) or 5 points (partial match)
     - NICE-TO-HAVE requirements: 5 points each (full match) or 2 points (partial match)
     - Normalize to percentage: (points earned / max possible points) × 70
  2. **Constraint Alignment (30% of score):**
     - Location match: +10 points (or 0 if mismatch, -30 if dealbreaker)
     - Salary range match: +10 points (or 0 if below minimum)
     - Role type match: +5 points
     - Remote policy match: +5 points
     - Normalize to percentage of 30 points
  3. **Dealbreaker override:** If any dealbreaker is triggered, cap the score at 25% maximum regardless of other factors.
- **Instruction:** Present the score prominently:
  ```
  ## Fit Score: {X}%

  **Breakdown:**
  - Requirement Coverage: {Y}% (matched {N} of {M} requirements)
  - Constraint Alignment: {Z}% ({summary of matches/mismatches})

  **Verdict:** {Strong Fit (80%+) | Good Fit (60-79%) | Potential Fit (40-59%) | Stretch (20-39%) | Not Recommended (<20%)}
  ```
- **Instruction:** This score will be used as the baseline "Corpus Fit Score" in the `tailor-resume` workflow.

### Step 5: Save Parsed Job File

**5a. Final Filename Confirmation:**
- **Instruction:** If Step 2b already handled duplicate detection and re-validation, skip to 5b.
- **Instruction:** If this is a new analysis, confirm the target filename: `research/openings/{company}-{role}.md`.
- **Instruction:** If an exact filename collision exists (rare edge case—Step 2b should have caught this), offer:
  1. Overwrite the existing file
  2. Create a versioned file (`{company}-{role}-v2.md`)
  3. Cancel

**5b. Write the Output File:**
- **Instruction:** Save the complete analysis to `research/openings/{filename}`.
- **Instruction:** The file must include the new "Corpus Skill Gap Analysis" section at the top of the "Quick Fit Assessment".

### Step 5c: Update Company Profile (if exists)

**Instruction:** After saving the job analysis, update the company's profile to track this opening.

**5c-i. Locate Company Profile:**
- **Instruction:** Search for an existing company profile using Glob: `research/companies/*/{company-slug}.md`
- **Instruction:** The company slug should be derived from the company name (lowercase, hyphens for spaces).
- **Example:** For "BAE Systems", search for `research/companies/*/bae-systems.md`.

**5c-ii. If Company Profile Found:**
- **Instruction:** Read the company profile file.
- **Instruction:** Locate the `## Tracked Openings` section.
- **Instruction:** Check if this role is already listed (by matching the analysis file path).
- **If not already listed:** Add a new row to the table:
  ```markdown
  | {Role Title} | {Fit Score}% | {YYYY-MM-DD} | [View](../../openings/{company}-{role}.md) |
  ```
- **If already listed (re-validation):** Update the existing row with the new fit score and date.
- **Instruction:** Save the updated company profile.
- **Instruction:** Inform the user: "Updated company profile: `research/companies/{industry}/{company}.md`"

**5c-iii. If No Company Profile Found:**
- **Instruction:** Note this for the user but don't block the workflow:
  ```
  Note: No company profile found for {Company}. Run `company-discovery` to create
  a profile and track this opening alongside company research.
  ```
- **Instruction:** Proceed to Step 6.

### Step 6: Update Market Skills Database

**Instruction:** This step updates the central `research/market_skills.json` file to improve market intelligence over time. User confirmation is required before adding skills.

**6a. Read the Market Skills DB:**
- **Instruction:** Read the contents of `research/market_skills.json`. If the file doesn't exist, initialize an empty JSON object `{}`.

**6b. Present Skills for Confirmation:**
- **Instruction:** Extract the list of technical skills parsed from this job posting (from Step 3).
- **Instruction:** Categorize them for the user:
  - **New skills** — Skills not currently in the market database
  - **Existing skills** — Skills already tracked (will increment counts)
- **Instruction:** Present the skills to the user for review:
  ```
  📊 I extracted the following technical skills from this posting:

  **New to your market database:**
  - Kubernetes (MUST-HAVE)
  - Terraform (NICE-TO-HAVE)

  **Already tracked (will update counts):**
  - Python (MUST-HAVE) — currently seen in 14 postings
  - Go (MUST-HAVE) — currently seen in 7 postings

  Would you like me to add these to your market skills database?
  1. Yes, add all
  2. Let me edit the list first
  3. Skip — don't update the database
  ```

**6c. Handle User Response:**
- **If user chooses "Yes, add all":** Proceed to 6d with all extracted skills.
- **If user chooses "Let me edit the list":**
  - **Instruction:** Ask the user which skills to remove or modify.
  - **Instruction:** Common reasons to edit:
    - Remove overly generic terms (e.g., "Communication", "Problem Solving")
    - Correct skill names (e.g., "JS" → "JavaScript")
    - Remove duplicates or variations (e.g., keep "React" but remove "React.js")
  - **Instruction:** After edits, confirm the final list before proceeding.
- **If user chooses "Skip":** Skip to Step 7 without updating the database.

**6d. Update Skill Counts:**
- **Instruction:** For each confirmed technical skill:
    - If the skill already exists in the database, increment its `count` and its `must_have_count` or `nice_to_have_count`.
    - If the skill is new, add it to the database with an initial `count: 1`.
- **Example Structure:**
    ```json
    {
      "Python": { "count": 15, "must_have_count": 10, "nice_to_have_count": 5 },
      "Go": { "count": 8, "must_have_count": 8, "nice_to_have_count": 0 },
      "Kubernetes": { "count": 1, "must_have_count": 1, "nice_to_have_count": 0 }
    }
    ```

**6e. Safe Write-Back:**
- **Instruction:** Save the updated JSON object to a temporary file, `research/market_skills.json.tmp`.
- **Instruction:** Validate the file using `cat research/market_skills.json.tmp | tools/validate-json.sh`.
- **Instruction:** If valid, perform an atomic write (rename original to `.bak`, rename `.tmp` to original). If invalid, report the error and discard the changes to this file to prevent corruption.
- **Instruction:** Confirm to the user: "✓ Added {N} skills to your market database ({X} new, {Y} updated)."

### Step 7: Summary and Next Steps

**Instruction:**
- Display a summary of the analysis, leading with the fit score and most critical information.
- **For new scans:**
  - **Example:**
    ```
    Job scan complete for {Role}.

    **Fit Score: {X}%** ({Verdict})
    - {N} critical skill gaps detected
    - {M} of {T} requirements matched
    - Constraints: {summary}

    Full analysis saved to `research/openings/{filename}`.
    ```
- **For re-validations:**
  - **Example (with changes):** "Re-validation complete for {Role}. **Fit Score: {X}%** (changed from {Y}%). The posting has changed—2 new requirements added, 1 priority upgraded."
  - **Example (no changes):** "Re-validation complete for {Role}. **Fit Score: {X}%** — No changes detected since {date}."
- **Instruction:** Suggest `tailor-resume` as the next logical step. Frame based on score:
  - **High score (70%+):** "You're already a strong match. `tailor-resume` will help you highlight your best evidence and polish the presentation."
  - **Medium score (40-69%):** "There are gaps to address. `tailor-resume` will help you find experiences to close them."
  - **Low score (<40%):** "This is a stretch role. `tailor-resume` can help, but be prepared for a longer session to find relevant experiences."

## Output

**For new scans:**
- `research/openings/{company}-{role}.md` — New parsed job posting with categorized requirements.
- `research/companies/{industry}/{company}.md` — Updated "Tracked Openings" section (if company profile exists).
- `research/market_skills.json` — Updated with user-confirmed skills from this posting (optional).

**For re-validations:**
- `research/openings/{company}-{role}.md` — Updated with any changed requirements, new scan date, and refreshed fit assessment.
- `research/companies/{industry}/{company}.md` — Updated "Tracked Openings" with new fit score and date (if company profile exists).
- `research/market_skills.json` — Updated with user-confirmed new skills if any were added to the posting (optional).
