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

First, let me check if you already have a project set up.

**Check for existing structure:**
1. Look for `profile/` directory
2. If found, warn: "It looks like you've already initialized a project. Continuing may overwrite existing files. Do you want to proceed? (yes/no)"
3. If user declines, exit gracefully

**Create missing directories:**

```
profile/
├── resume.md           # Your master resume (imported in Step 4)
└── writing_samples/    # Voice analysis samples
    └── README.md       # Placeholder with instructions

applications/
├── resumes/            # Tailored resumes (created by fit-resume workflow)
└── cover_letters/      # Generated cover letters

research/
├── companies/          # Company profiles (created by Scout)
└── openings/           # Job posting analyses
```

**For each directory:**
1. Check if it exists
2. Create if missing
3. Report what was created

**Create placeholder files:**

`profile/writing_samples/README.md`:
```markdown
# Writing Samples

Place your writing samples here for voice analysis. Good samples include:
- Cover letters you've written
- LinkedIn posts or articles
- Professional emails or proposals
- Any writing that represents your voice

The more samples you provide, the better Max can match your voice when generating cover letters.
```

`applications/resumes/README.md`:
```markdown
# Tailored Resumes

This folder contains resumes tailored for specific job applications.

Files are created by the fit-resume workflow and named: `{company}-{role}.md`

Example: `acme-senior-engineer.md`
```

`applications/cover_letters/README.md`:
```markdown
# Cover Letters

This folder contains cover letters generated for specific job applications.

Files are created by the cover-letter workflow and named: `{company}-{role}.md`

Example: `stripe-staff-engineer.md`
```

`research/companies/README.md`:
```markdown
# Company Research

This folder contains company profiles and research created by Scout.

Files are organized by industry and named: `{industry}/{company}.md`

Example: `fintech/stripe.md`
```

`research/openings/README.md`:
```markdown
# Job Opening Analyses

This folder contains analyzed job postings and opportunity assessments.

Files are named: `{company}-{role}.md`

Example: `netflix-principal-engineer.md`
```

### Step 4: Resume Import

Now let's import your resume.

**Prompt:**
"Where is your resume? You can:
1. Provide a file path to a markdown file
2. Paste the content directly (useful if you have a PDF/DOCX)
3. Type 'skip' to add it later"

**If file path provided:**
1. Read the file
2. Copy contents to `profile/resume.md`
3. Show a preview (first 20 lines)
4. Ask: "Does this look correct? (yes/no)"
5. If no, offer to try again or paste content

**If content pasted:**
1. Write content to `profile/resume.md`
2. Show a preview
3. Confirm with user

**If skipped:**
1. Note that resume will need to be added before using fit-resume workflow
2. Create empty `profile/resume.md` with placeholder text:
   ```markdown
   # Resume

   Add your resume content here before using the fit-resume workflow.
   ```

**Error handling:**
If file can't be read or is in an unsupported format (PDF, DOCX, binary):
```
I tried to read your resume but couldn't access it. This could be because:
- The file doesn't exist at that path
- The file is in a format I can't read directly (PDF, DOCX, etc.)

I need your resume in markdown or plain text format.

Would you like to:
1. Try a different path?
2. Paste the content directly? (recommended for PDF/DOCX)
3. Help me create a resume from scratch?
4. Skip and add it later?
```

**If user chooses "create from scratch":**
Walk through basic resume sections interactively:
- Contact information
- Professional summary
- Work experience (ask for each role)
- Education
- Skills
Save to `profile/resume.md` and show preview for confirmation.

### Step 5: Writing Samples Import (Optional)

Writing samples help me match your voice when generating cover letters.

**Prompt:**
"Do you have writing samples to import? (cover letters, LinkedIn posts, etc.)
- Provide file paths separated by commas
- Type 'skip' if you don't have any right now"

**If paths provided:**
1. For each path:
   - Read the file
   - Generate descriptive name (e.g., `sample-1-cover-letter.md`)
   - Copy to `profile/writing_samples/`
   - Report success or failure
2. Show summary of imported samples

**If skipped:**
1. Note that writing samples can be added later
2. Cover letter generation will still work, but voice matching will be limited

**Naming convention:**
- `sample-1-cover-letter.md`
- `sample-2-linkedin-post.md`
- `sample-3-proposal.md`
- Ask user to describe each sample briefly for better naming

### Step 6: Completion Summary

**Summarize what was created:**

```
Setup Complete!

Created directories:
- profile/
- profile/writing_samples/
- applications/
- applications/resumes/
- applications/cover_letters/
- research/
- research/companies/
- research/openings/

Created placeholder READMEs:
- profile/writing_samples/README.md
- applications/resumes/README.md
- applications/cover_letters/README.md
- research/companies/README.md
- research/openings/README.md

Imported files:
- profile/resume.md [or "Not imported - add before using fit-resume"]
- profile/writing_samples/[list of samples] [or "None imported"]
```

**Next step:**

The scoping interview is where we establish your job search constraints — what you're looking for, your dealbreakers, compensation requirements, and preferences. This creates your `constraints.yaml` file that guides all future workflows.

**Would you like to start the scoping interview now?**
- Type `yes` to start the scoping-interview workflow
- Type `no` to finish here (you can run it later with "help me run the scoping interview")

*If user declines:*
"No problem! When you're ready, just ask me to run the scoping interview. In the meantime, make sure your resume is in `profile/resume.md` — you'll need it for the scoping interview."

## Output

**Directories created:**
- `profile/`
- `profile/writing_samples/`
- `applications/`
- `applications/resumes/`
- `applications/cover_letters/`
- `research/`
- `research/companies/`
- `research/openings/`

**Files created:**
- `profile/resume.md` (user's master resume)
- `profile/writing_samples/README.md` (placeholder with instructions)
- `profile/writing_samples/*` (imported samples, if any)
- `applications/resumes/README.md` (placeholder with instructions)
- `applications/cover_letters/README.md` (placeholder with instructions)
- `research/companies/README.md` (placeholder with instructions)
- `research/openings/README.md` (placeholder with instructions)

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** scoping-interview
   **Rationale:** "Let's capture your job search preferences next"
   **Context to pass:** `profile/resume.md` (imported resume), `profile/writing_samples/` (if any)

2. Present the suggestion conversationally:
   "Great, your project is set up! Let's capture your job search preferences next — salary expectations, location, remote preferences, and dealbreakers. This creates your `constraints.yaml` file that guides all future workflows. Ready to start the scoping interview? [Yes/No/Something else]"

3. If user agrees: Load `workflows/scoping-interview/workflow.md` and execute
4. If user declines: Summarize what was accomplished and end gracefully
5. If user requests different workflow: Honor their request
