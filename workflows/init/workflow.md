# Init Workflow

## Summary

**Purpose:** Set up your job search project with directory structure, import resume and writing samples
**Agent:** Job Coach (Max) & Job Scout
**Reads:**
- User-provided resume (file path or pasted content)
- User-provided writing samples (optional)
**Creates:**
- `profile/resume.md` — Your master resume
- `profile/writing_samples/` — Voice analysis samples
- `applications/resumes/` — Directory for tailored resumes
- `applications/cover_letters/` — Directory for cover letters
- `research/companies/` — Directory for company profiles
- `research/openings/` — Directory for job posting analyses
**Approximate time:** 5-10 minutes (interactive)
**Prerequisites:** None — this is the starting workflow

---

**Trigger:** First workflow for new projects, or user says "help me set up" or "initialize my project"

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
- [ ] Import your resume
- [ ] Import writing samples (optional)
- [ ] Schedule scoping interview (next workflow)

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
   - `profile/writing_samples/`
   - `applications/`
   - `applications/resumes/`
   - `applications/cover_letters/`
   - `research/`
   - `research/companies/`
   - `research/openings/`
2. Report what was created.

### Step 4: Create Resume Corpus

Now, we'll import your resume and transform it into a structured "Resume Corpus". This creates a powerful, searchable knowledge base of your experience that will improve over time.

**Prompt for Resume:**
"Where is your resume? You can:
1. Provide a file path to a text or markdown file
2. Paste the content directly
3. Type 'skip' to create an empty corpus"

**(Get resume content into a temporary variable based on user choice)**

**If skipped:**
1. Create an empty `profile/corpus.json` file with the base schema.
2. Skip to **Step 5**.

**Once resume content is available, proceed:**

1.  **- [ ] Parse Resume into Structured Blocks:**
    -   **Instruction:** "Analyze the provided resume text. Your goal is to convert this unstructured document into a structured JSON object. Identify the following sections: Professional Summary, Work Experience, Education, and Skills."
    -   **Instruction:** "For each job under Work Experience, extract the company, title, dates, and a list of accomplishment bullet points."
    -   **Instruction:** "For each skill, identify the skill name and try to categorize it (e.g., 'Programming Language', 'Database', 'Cloud Platform')."

2.  **- [ ] Generate JSON with Schema:**
    -   **Instruction:** "Using the parsed information, generate the content for a `corpus.json` file. Adhere strictly to the following JSON schema. Create unique IDs for each item."
    -   **Schema Definition:**
        ```json
        {
          "schema_version": "1.0",
          "last_updated": "{current_timestamp}",
          "summaries": [
            { "id": "sum_01", "content": "{parsed_summary}" }
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
              "content": "{parsed_bullet_point}",
              "skills_tags": ["{inferred_skill_1}", "{inferred_skill_2}"],
              "metrics": ["{inferred_metric_1}"]
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

3.  **- [ ] Save Corpus File:**
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

### Step 5: Writing Samples Import (Optional)

Writing samples help me match your voice when generating cover letters. This is separate from your resume corpus.

**Prompt:**
"Do you have writing samples to import? (cover letters, LinkedIn posts, etc.)
- Provide file paths separated by commas
- Type 'skip' if you don't have any right now"

**(This step's logic for copying files remains the same as before)**

### Step 6: Completion Summary

**Summarize what was created:**

```
Setup Complete!

Your resume has been converted into a structured Resume Corpus at `profile/corpus.json`.

This file is a searchable database of your skills and experiences that will improve over time. All future workflows will now use this corpus as the single source of truth.

Created directories:
- profile/, applications/, research/ and their subdirectories.

Created files:
- profile/corpus.json (Your new Resume Corpus)
- profile/writing_samples/[list of samples]
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
- `profile/writing_samples/*` (imported samples, if any)

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
