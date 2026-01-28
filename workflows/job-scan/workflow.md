# Job Scan

## Summary

**Purpose:** Parse a job posting into structured requirements, identify skill gaps, and update a central market skills database.
**Agent:** Job Scout
**Reads:**
- Job posting content (URL, file path, or pasted text)
- `profile/corpus.json` — For skill gap analysis.
- `profile/constraints.yaml` — For dealbreaker and preference checks.
- `research/market_skills.json` — The central database of all skills seen in the market.
**Creates:**
- `research/openings/{company}-{role}.md` — Parsed job posting with categorized requirements.
- `research/market_skills.json` (updated) — Enriched with the skills from this job posting.
**Approximate time:** 5-10 minutes
**Prerequisites:** `corpus.json` and `constraints.yaml` are highly recommended for full functionality.

---

**Trigger:** User says "scan this job posting", "analyze this job", or provides a job posting URL/file.

## Persona

**Load and adopt:** `agents/job-scout.md`. Embody Scout's analytical, data-driven approach.

## Steps

### Step 1: Obtain Job Posting Content

**Instruction:** Determine the user's preferred input method and retrieve the job posting content.

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
- **Instruction:** Generate a summary verdict (e.g., Strong Fit, Potential Fit, Not Recommended).

### Step 5: Save Parsed Job File

**5a. Check for Existing Files & Offer Diff:**
- **Instruction:** Before saving, check for existing analysis files for this role in `research/openings/`.
- **Instruction:** If a previous version is found, present the user with options, including a new **"Compare with new version"** option.
- **If user chooses to compare:**
    - **Instruction:** Perform a diff between the requirements of the old and new versions.
    - **Instruction:** Summarize the key changes for the user. Example: "The new version has added 'AWS Certification' as a NICE-TO-HAVE and upgraded 'Python' from a NICE-TO-HAVE to a MUST-HAVE."
    - **Instruction:** After showing the diff, ask the user again if they want to overwrite, create a new version, or cancel.

**5b. Write the Output File:**
- **Instruction:** Save the complete analysis to `research/openings/{filename}`.
- **Instruction:** The file must include the new "Corpus Skill Gap Analysis" section at the top of the "Quick Fit Assessment".

### Step 6: Update Market Skills Database

**Instruction:** This step updates the central `research/market_skills.json` file to improve market intelligence over time.

**6a. Read the Market Skills DB:**
- **Instruction:** Read the contents of `research/market_skills.json`. If the file doesn't exist, initialize an empty JSON object `{}`.

**6b. Update Skill Counts:**
- **Instruction:** For each technical skill parsed from the current job posting:
    - If the skill already exists in the database, increment its `count` and its `must_have_count` or `nice_to_have_count`.
    - If the skill is new, add it to the database with an initial `count: 1`.
- **Example Structure:**
    ```json
    {
      "Python": { "count": 15, "must_have_count": 10, "nice_to_have_count": 5 },
      "Go": { "count": 8, "must_have_count": 8, "nice_to_have_count": 0 },
      "Chrony": { "count": 1, "must_have_count": 1, "nice_to_have_count": 0 }
    }
    ```

**6c. Safe Write-Back:**
- **Instruction:** Save the updated JSON object to a temporary file, `research/market_skills.json.tmp`.
- **Instruction:** Validate the file using `cat research/market_skills.json.tmp | tools/validate-json.sh`.
- **Instruction:** If valid, perform an atomic write (rename original to `.bak`, rename `.tmp` to original). If invalid, report the error and discard the changes to this file to prevent corruption.

### Step 7: Summary and Next Steps

**Instruction:**
- Display a summary of the analysis, leading with the most critical information.
- **Example:** "Job scan complete for {Role}. **🚨 I found 3 critical skill gaps** between the job's must-haves and your resume. The full analysis, including a dealbreaker check, is saved to `research/openings/{filename}`."
- **Instruction:** Suggest `tailor-resume` as the next logical step to address the identified gaps. Frame the suggestion around the gap analysis. "The next step is to run `tailor-resume` to address these gaps directly. Ready to start tailoring?"

## Output

**Files created/updated:**
- `research/openings/{company}-{role}.md` — Parsed job posting.
- `research/market_skills.json` — Updated with skills from this posting.
