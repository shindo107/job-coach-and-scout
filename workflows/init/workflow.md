# Init Workflow

## Summary

**Purpose:** Set up your job search project with directory structure and import resume(s)
**Agent:** Job Coach (Max) & Job Scout
**Agent Lead:** Max
**Phase:** setup
**Reads:**
- User-provided resumes (one or more file paths, or pasted content)
**Creates:**
- `profile/corpus.json` — Your structured Resume Corpus
- `profile/resume_template.yaml` (optional) — PDF styling template (if PDF imported)
- `profile/imports/` — Drop zone for source resumes
- `profile/writing_samples/` — Directory for voice analysis samples (populated later)
- `applications/resumes/` — Directory for tailored resumes
- `applications/cover_letters/` — Directory for cover letters
- `research/companies/` — Directory for company profiles
- `research/openings/` — Directory for job posting analyses
- `research/market_skills.json` — Market intelligence database (empty seed)
**Updates:** None
**Prerequisites:** None — this is the starting workflow

> **Note:** Voice Agent created separately via `/create-voice` workflow after adding writing samples to `profile/writing_samples/`

---

**Trigger:** First workflow for new projects, or user says "help me set up" or "initialize my project"

## Persona

**Load and adopt:** `agents/job-coach.md` AND `agents/job-scout.md`

Read both persona files. This workflow introduces both Max and Scout. Present their introductions as written in the persona files, then proceed with Max leading the setup process.

## Context Required

None — this is the starting workflow for new projects.

## Steps

### Step 1: Welcome & Agent Introductions

Welcome to Job Coach & Scout! Let's get your job search project set up.

**Meet your agents:**

**Max (Job Coach):**
I'm Max, a veteran recruiter and hiring manager with 15+ years of experience. I've reviewed thousands of resumes and conducted hundreds of interviews. I know what makes a hiring manager's eyes glaze over and what makes them reach for the phone.

I'll be your guide for resume tailoring, interview prep, and honest feedback. My default mode is adversarial — I'm the skeptical hiring manager reading your resume with one hand on the "reject" pile. This isn't about being harsh; it's about preparing you for real interviews.

**Scout (Job Scout):**
I'm Scout, your strategic market intelligence analyst. While Max helps you position yourself, I help you find the right targets. I track hiring trends, evaluate companies, and surface opportunities that match your constraints.

I approach job hunting like competitive intelligence — analyzing markets, identifying patterns, and building a picture of where your skills are valued.

**How we work together:**
- Max focuses on *your story* — making sure your resume and materials are compelling
- Scout focuses on *the market* — finding where your story resonates best
- Together, we help you target the right opportunities with the right positioning

### Step 2: Onboarding Overview & Privacy Agreement

**What we'll set up today:**

- [ ] Establish directory structure (profile/, applications/, research/)
- [ ] Import your resume(s) — you can provide multiple versions for a richer corpus
- [ ] Schedule scoping interview (next workflow)
- [ ] (Optional) Create Voice Agent via `/create-voice` after adding writing samples

---

**IMPORTANT: Privacy & Data Handling**

Before we continue, you need to understand how your data will be handled:

**What you'll be sharing:**
- Your resume (work history, skills, education)
- Writing samples (cover letters, LinkedIn posts, etc.)
- Career preferences (salary expectations, location, role types)
- Personal career history and aspirations

**How your data is handled:**
- All data is stored **locally** in your project directory
- Files are **unencrypted** — secure your machine accordingly
- **No telemetry** or analytics are collected by this tool
- Data you share with Claude is subject to [Anthropic's usage policies](https://www.anthropic.com/policies)
- Claude may use your conversations for model training unless you opt out via Anthropic's settings

**Your responsibilities:**
- Secure your local machine and project directory
- Understand that frontier LLMs process your personal information
- Review and understand Anthropic's data handling policies

---

**Do you agree to continue?**

Type `yes` to proceed or `no` to exit.

**If user responds `no` or declines:**
1. Acknowledge their decision respectfully
2. Say: "No problem. Your privacy matters. When you're ready to proceed, just ask me to run the init workflow again."
3. **STOP HERE** — Do not proceed to Step 3 or any subsequent steps
4. End the workflow immediately

### Step 3: Directory Structure Setup

First, I'll set up the required directories for your project.

**Actions:**
1. Check for and create the following directories if they don't exist:
   - `profile/`
   - `profile/imports/` — where users drop source resume files
   - `profile/writing_samples/`
   - `applications/`
   - `applications/resumes/`
   - `applications/cover_letters/`
   - `research/`
   - `research/companies/`
   - `research/openings/`
2. Initialize `research/market_skills.json` if it doesn't exist:
   - Create the file with an empty JSON object: `{}`
   - This file will be populated by the `job-scan` workflow as you analyze job postings
3. Report what was created.

### Step 4: Create Resume Corpus

Now, we'll import your resume(s) and transform them into a structured "Resume Corpus". This creates a powerful, searchable knowledge base of your experience that will improve over time.

> **Why multiple resumes?** If you have different versions of your resume (tailored for different roles, older versions with experiences you trimmed, a master resume and a shorter one), providing all of them helps build a more comprehensive corpus. I'll intelligently merge them, keeping unique accomplishments and the best phrasing from each.

**Prompt for Resumes:**
```
Where are your resumes? You can provide multiple files to build a richer corpus.

Options:
A) Drop them in `profile/imports/` (Recommended)
   Just copy your resume files there and I'll import them all.
   Supported formats: .md, .txt, .pdf, .docx

B) Point me to a different folder
   I'll scan that directory for resume files.

C) Other (specify)
   Paste content, provide specific file paths, or skip.

Which option? [A/B/C]
```

**(Handle user's choice)**

**Option A — Import from `profile/imports/` (Recommended):**
1. Check if `profile/imports/` contains any files
2. **If empty:**
   ```
   The `profile/imports/` folder is empty.

   Please copy your resume file(s) there now. You can add:
   - Your current resume
   - Older versions with experiences you may have trimmed
   - Role-specific variants (e.g., technical vs. management focused)

   Let me know when you've added them, or choose another option.
   ```
   Wait for user confirmation, then re-scan.
3. **If files found:**
   ```
   Found {N} file(s) in profile/imports/:
   - {filename_1}
   - {filename_2}
   - ...

   Import all of these? [Yes / No, let me adjust]
   ```
4. Read each supported file and store contents with source filename
5. Unsupported file types: warn and skip

**Option B — Different directory:**
```
What's the path to the folder containing your resumes?
Example: ~/Documents/resumes or /Users/you/job-search/
```
1. Validate the directory exists
2. List files found and confirm with user (same as Option A step 3)
3. Read each supported file

**Option C — Other:**
```
How would you like to provide your resume(s)?
1. Paste content directly — I'll prompt you for each resume
2. Specific file path(s) — comma-separated list
3. Skip — create an empty corpus to populate later
```

**If pasting:**
```
Great! Let's collect your resumes one at a time.

Paste your first resume content below. When you're done, type 'DONE' on a new line.
```
After each paste:
```
Got it! Do you have another resume version to add?
- Paste the next one
- Type 'no more' when you've added all your resumes
```

**If specific paths:**
1. Parse the comma-separated list of paths
2. Read each file and store contents with source filename
3. If any file fails to read, report which one and ask if they want to continue with the others

**If skipped:**
1. Create an empty `profile/corpus.json` file with the base schema.
2. Skip to **Step 5**.

**Once resume content is collected, proceed:**

1.  **- [ ] Parse Each Resume into Structured Blocks:**
    -   **Instruction:** "For EACH provided resume, analyze the text and extract: Professional Summary, Work Experience (company, title, dates, accomplishment bullets), Education, and Skills."
    -   **Instruction:** "Track which resume each piece of content came from (for deduplication decisions)."
    -   **Instruction:** "For each skill, identify the skill name and try to categorize it (e.g., 'Programming Language', 'Database', 'Cloud Platform')."

2.  **- [ ] Merge and Deduplicate:**
    -   **Positions:** Match positions by company + title + overlapping dates. If the same position appears in multiple resumes, merge their accomplishments.
    -   **Accomplishments:** For semantically similar bullets (same achievement, different wording), keep the version with:
        - More specific metrics/numbers
        - Stronger action verbs
        - More detail
        - Note: Store alternate phrasings as `variations` for future use
    -   **Skills:** Union all skills across resumes, deduplicate by name (case-insensitive).
    -   **Summaries:** Keep all unique summaries (they may be tailored for different audiences).

3.  **- [ ] Generate JSON with Schema:**
    -   **Instruction:** "Using the merged information, generate the content for a `corpus.json` file. Adhere strictly to the following JSON schema. Create unique IDs for each item."
    -   **Schema Definition:**
        ```json
        {
          "schema_version": "1.0",
          "last_updated": "{current_timestamp}",
          "sources": ["{filename_1}", "{filename_2}"],
          "summaries": [
            { "id": "sum_01", "content": "{parsed_summary}", "source": "{filename}" }
          ],
          "positions": [
            {
              "id": "pos_01",
              "company": "{parsed_company}",
              "title": "{parsed_title}",
              "start_date": "{parsed_start}",
              "end_date": "{parsed_end}"
            }
          ],
          "accomplishments": [
            {
              "id": "acc_01",
              "position_id": "pos_01",
              "content": "{best_bullet_point}",
              "skills_tags": ["{inferred_skill_1}", "{inferred_skill_2}"],
              "metrics": ["{inferred_metric_1}"],
              "variations": [
                { "id": "var_01", "content": "{alternate_phrasing}", "source": "{filename}" }
              ]
            }
          ],
          "skills": [
            {
              "id": "skill_01",
              "name": "{parsed_skill}",
              "category": "{inferred_category}"
            }
          ]
        }
        ```
    -   **PII Handling:** "During this process, identify any PII (email, phone, address) and replace it with placeholders like `[REDACTED_EMAIL]` in the `content` fields."

4.  **- [ ] Report Merge Results:**
    -   Tell the user what was merged:
    ```
    Corpus built from {N} resume(s):
    - {X} positions identified
    - {Y} unique accomplishments extracted
    - {Z} alternate phrasings saved as variations
    - {W} skills catalogued

    Notable merges:
    - Position "{title} at {company}": Combined {N} bullets from multiple sources
    - Accomplishment about "{topic}": Kept version with metrics, saved alternate as variation
    ```

5.  **- [ ] Confirm Accuracy:**
    -   **IMPORTANT:** Before saving, confirm the extraction is accurate.
    -   Show the user a summary of positions and key accomplishments extracted.
    -   **Max:** "I've parsed your resume(s) and built your corpus. Here's what I captured — does this look accurate? Any positions, accomplishments, or skills I missed or got wrong?"
    -   **CRITICAL:** I only extract what's in your documents — I never fabricate experiences, skills, or details. If something looks wrong, it may be a parsing error that we should fix.
    -   Wait for user confirmation before proceeding.

6.  **- [ ] Save Corpus File:**
    -   Save the generated JSON to `profile/corpus.json`.

### Step 4a: Validate Corpus File

This is a critical safety check to ensure the Resume Corpus is not corrupted.

**Actions:**
1.  **- [ ] Execute validation script:**
    -   Run the command: `cat profile/corpus.json | tools/validate-json.sh`
2.  **- [ ] Handle result:**
    -   **If the command succeeds (exit code 0):** The file is valid. Inform the user: "Resume Corpus created and validated successfully." Proceed to the next step.
    -   **If the command fails (non-zero exit code):** The file is invalid.
        -   Report the error to the user: "I detected a formatting error in the `profile/corpus.json` file I just saved. The error is: [show stderr from the command]."
        -   "I will attempt to fix this automatically."
        -   Re-run the parsing and generation steps from Step 4 to create a corrected version.
        -   If it fails a second time, stop the workflow and report the critical failure.

### Step 4b: Analyze Resume Template (PDF imports only)

**Skip this step if:** No PDF was imported OR user opts out of PDF generation.

**Purpose:** When you import a PDF resume, this step analyzes its visual structure and creates a matching template so future tailored resumes maintain the same look and feel.

**Actions:**

1.  **- [ ] Check PDF tool availability:**
    -   Run: `./tools/check-pdf-tools.sh`
    -   Parse the JSON output to determine if any PDF engine is available.
    -   **If no tools available:** Inform user and offer to skip:
        ```
        PDF generation tools are not currently installed.

        I can still analyze your resume's layout and save a template for later.
        When you install a PDF tool, tailored resumes will automatically
        generate matching PDFs.

        Install options:
        - WeasyPrint (recommended): pip install weasyprint
        - Typst: https://typst.app/

        Continue with template analysis? [Yes/Skip]
        ```

2.  **- [ ] Analyze imported PDF structure:**
    -   If a PDF file was imported in Step 4, analyze its visual structure:

    **Layout detection:**
    - Column structure: single-column, two-column-sidebar, two-column-equal
    - Page margins (estimate from content positioning)
    - Page size (letter vs A4)

    **Header analysis:**
    - Name position: left, center, or right aligned
    - Name size: medium, large, or xlarge relative to body text
    - Contact info layout: single-line, multi-line, or sidebar
    - Contact separator character: |, bullet, or space

    **Section analysis:**
    - Order of sections (summary, experience, skills, education, etc.)
    - Section heading style (uppercase, bold, underlined)
    - Presence of dividing lines between sections

    **Experience formatting:**
    - Company vs title ordering (which appears first)
    - Date position (right-aligned vs inline)
    - Date format (MMM YYYY, MM/YYYY, YYYY)
    - Bullet style (bullet, dash, arrow)

    **Typography:**
    - Font style: modern (sans-serif) or traditional (serif)
    - Approximate body text size
    - Heading weight

    **Colors:**
    - Primary accent color (headings, name)
    - Secondary color (dates, subtle text)
    - Body text color

3.  **- [ ] Generate template file:**
    -   Create `profile/resume_template.yaml` with detected settings:
    ```yaml
    schema_version: "1.0"
    created_from: "profile/imports/{original_pdf_filename}"
    created_at: "{ISO timestamp}"

    layout:
      type: "{detected_layout}"
      page_size: "{letter|a4}"
      margins:
        top: "{value}"
        bottom: "{value}"
        left: "{value}"
        right: "{value}"

    header:
      name_position: "{left|center|right}"
      name_size: "{medium|large|xlarge}"
      contact_layout: "{single-line|multi-line|sidebar}"
      contact_separator: "{|, bullet, space}"

    sections:
      order: [{list of detected sections}]
      experience:
        company_title_order: "{title-first|company-first}"
        date_position: "{right|inline}"
        date_format: "{MMM YYYY|MM/YYYY|YYYY}"
        bullet_style: "{bullet|dash|arrow}"

    typography:
      style: "{modern|traditional|minimal}"
      font_family: "{sans-serif|serif}"
      heading_weight: "{bold|semibold}"
      body_size: "{10pt|11pt|12pt}"

    colors:
      primary: "#{hex_color}"
      secondary: "#{hex_color}"
      body: "#{hex_color}"

    special_features:
      has_dividers: {true|false}
      has_icons: {true|false}
      skills_format: "{tags|list|inline}"
    ```

4.  **- [ ] Validate template:**
    -   Run: `cat profile/resume_template.yaml | tools/validate-yaml.sh`
    -   If validation fails, fix the YAML and retry.

5.  **- [ ] Confirm with user:**
    -   Display a summary of detected settings:
    ```
    Resume Template Detected:

    Layout: {type} with {page_size} page
    Header: Name {position}, contact on {layout}
    Sections: {comma-separated list}
    Style: {modern/traditional}, {sans-serif/serif}
    Colors: Primary #{hex}, Secondary #{hex}

    This template will be used when generating PDF versions of
    your tailored resumes. You can edit profile/resume_template.yaml
    to adjust any settings.

    Does this look correct? [Yes / Let me adjust / Skip PDF features]
    ```
    -   If user wants adjustments, allow inline edits or note they can edit the YAML file later.
    -   If user skips, delete the template file and proceed without PDF support.

### Step 5: Voice Agent Setup (Optional)

Your Voice Agent writes cover letters and LinkedIn content in your authentic style. It's created from writing samples you provide.

**Prompt:**
```
Would you like to set up voice matching for cover letters?

This creates a Voice Agent that writes in your authentic style, based on
samples of your writing (cover letters, emails, blog posts, etc.).

Options:
1. Yes, I have samples ready — I'll guide you to add them now
2. Later — I'll set up the directory, you can run /create-voice anytime
3. Skip — I don't need voice matching

Which option? [1/2/3]
```

**Option 1 — Set up now:**
```
Great! Add your writing samples to `profile/writing_samples/`.

Good samples include:
- Cover letters you've written
- Professional emails
- LinkedIn posts or articles
- Any professional writing that sounds like "you"

Let me know when you've added them, and I'll run /create-voice to analyze
your writing style and generate your Voice Agent.
```
- Wait for user to add files
- Once confirmed, suggest running `/create-voice` as the next step after scoping

**Option 2 — Later:**
```
No problem! The `profile/writing_samples/` directory is ready for you.

When you're ready:
1. Add writing samples to `profile/writing_samples/`
2. Run `/create-voice` to generate your Voice Agent

Your Voice Agent will be used automatically by /cover-letter and /linkedin-review.
```

**Option 3 — Skip:**
```
Got it. Cover letters will be generated without voice matching.

You can always add voice matching later by:
1. Adding samples to `profile/writing_samples/`
2. Running `/create-voice`
```

### Step 6: Completion Summary

**Summarize what was created:**

```
Setup Complete!

Your resume(s) have been converted into a structured Resume Corpus at `profile/corpus.json`.

{If multiple resumes were provided:}
I merged content from {N} resume sources, extracting {X} positions, {Y} accomplishments, and {Z} skills. Alternate phrasings were saved as variations for future tailoring.

This file is a searchable database of your skills and experiences that will improve over time. All future workflows will now use this corpus as the single source of truth.

Created directories:
- profile/, applications/, research/ and their subdirectories.

Created files:
- profile/corpus.json (Your Resume Corpus — built from {N} source(s))
{If PDF imported:}
- profile/resume_template.yaml (PDF styling template)

Voice Agent:
{If user chose to set up voice later or skipped:}
- Run `/create-voice` after adding samples to `profile/writing_samples/`
{If user added samples and wants to proceed:}
- Ready to run `/create-voice` to generate your Voice Agent
```

**Next step:**

The scoping interview is where we establish your job search constraints. This creates your `constraints.yaml` file that guides all future workflows.

**Would you like to start the scoping interview now?**
- Type `yes` to start the scoping-interview workflow
- Type `no` to finish here (you can run it later by asking)

## Output

**Directories created:**
- `profile/`, `applications/`, `research/` and their subdirectories.

**Files created:**
- `profile/corpus.json` (The user's structured resume knowledge base)
- `profile/resume_template.yaml` (PDF styling template, if PDF imported)
- `research/market_skills.json` (empty seed for market intelligence)

> **Note:** Voice Agent (`agents/voice.md`) and voice profile (`profile/voice_profile.json`) are created separately via the `/create-voice` workflow.

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** scoping-interview
   **Rationale:** "Let's capture your job search preferences next"
   **Context to pass:** `profile/corpus.json` (the newly created corpus)

2. Present the suggestion conversationally:
   "Great, your Resume Corpus is set up! Let's capture your job search preferences next — salary expectations, location, remote preferences, and dealbreakers. Ready to start the scoping interview? [Yes/No/Something else]"

3. If user agrees: Load `workflows/scoping-interview/workflow.md` and execute
4. If user declines: Summarize what was accomplished and end gracefully
5. If user requests different workflow: Honor their request
