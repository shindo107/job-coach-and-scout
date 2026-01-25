# Workflow Conventions

> Standard patterns for all workflow files in Job Coach & Scout.

This document defines the conventions that all workflow files must follow to ensure Claude Code interprets them consistently and users have predictable experiences.

## Standard Workflow Structure

Every workflow file follows this structure:

```markdown
# {Workflow Name}

**Agent:** Job Coach (Max) | Job Scout
**Purpose:** {One-line description}
**Trigger:** {When/how this workflow is invoked}

## Context Required

Before starting, load these files:
- `profile/resume.md` — Master resume (required)
- `profile/constraints.yaml` — Job search constraints (required)

If available, also load:
- `applications/resumes/*.md` — Previous tailored resumes

## Steps

### Step 1: {Step Name}

{Instructions for Claude Code to follow}

### Step 2: {Step Name}

{More instructions}

## Output

Save the result to: `{output path pattern}`

**Files created:**
- `{path}` — {description}

## Recommend Next

After completing this workflow, suggest: **{next workflow name}**

{Brief explanation of why this is the logical next step}
```

## Header Format

Every workflow begins with three required header fields:

| Field | Format | Example |
|-------|--------|---------|
| Agent | `**Agent:** {agent name(s)}` | `**Agent:** Job Coach (Max)` |
| Purpose | `**Purpose:** {one-line description}` | `**Purpose:** Tailor resume for a specific job posting` |
| Trigger | `**Trigger:** {invocation method}` | `**Trigger:** User says "help me tailor my resume"` |

**Agent options:**
- `Job Coach (Max)` — Resume tailoring, interview prep, feedback
- `Job Scout` — Market research, company discovery
- `Job Coach (Max) & Job Scout` — Combined workflows

**Trigger examples:**
- `User says "help me tailor my resume for [company]"`
- `User asks to evaluate a job posting`
- `First workflow for new projects`
- `Automatically suggested after completing fit-resume`

## Context Required Section

Lists files the workflow needs to function. Use two categories:

**Required files** — Workflow cannot proceed without these:
```markdown
Before starting, load these files:
- `profile/resume.md` — Master resume (required)
- `profile/constraints.yaml` — Job search constraints (required)
```

**Optional files** — Enhance workflow but not required:
```markdown
If available, also load:
- `applications/resumes/*.md` — Previous tailored resumes
- `research/companies/{company}.md` — Existing company research
```

**Special case — no context required:**
```markdown
## Context Required

None — this is the starting workflow for new projects.
```

## Steps Section

Steps are numbered sequentially with descriptive names:

```markdown
## Steps

### Step 1: Parse Job Posting

Read the job posting and extract:
- Required qualifications
- Preferred qualifications
- Key responsibilities
- Company information

### Step 2: Identify Alignment

Compare extracted requirements against resume...
```

**Step conventions:**
- Use `### Step N: {Descriptive Name}` format
- Instructions are written as commands to Claude Code
- Include checkboxes `- [ ]` for multi-part steps users track
- Keep instructions clear and actionable

## Output Section

Specifies where results are saved:

```markdown
## Output

Save the result to: `applications/resumes/{company}-{role}.md`

**Files created:**
- `applications/resumes/{company}-{role}.md` — Tailored resume
- `research/openings/{company}-{role}.md` — Job posting analysis
```

**Path patterns use placeholders:**
- `{company}` — Normalized company name (lowercase, hyphens)
- `{role}` — Normalized role title (lowercase, hyphens)
- `{industry}` — Industry category (lowercase, hyphens)

## Recommend Next Section

Suggests the logical next workflow:

```markdown
## Recommend Next

After completing this workflow, suggest: **cover-letter**

Now that your resume is tailored, you can generate a voice-matched cover letter that complements it.
```

**Pattern:**
1. Bold the workflow name
2. Provide brief rationale (1-2 sentences)
3. Can suggest multiple options if appropriate

## Error Handling

Errors are conversational, not programmatic. When something goes wrong:

```
I tried to [action] but [problem].

Would you like to:
1. [Alternative 1]
2. [Alternative 2]
3. [Alternative 3 - often "skip and continue"]
```

### Missing Required File

```
I need your resume to continue, but I couldn't find `profile/resume.md`.

Would you like to:
1. Provide a file path to your resume
2. Paste your resume content directly
3. Run the init workflow first to set up your project
```

### Missing Optional File

```
I looked for your constraints file at `profile/constraints.yaml` but it doesn't exist yet.

This file captures your job search preferences (salary, location, role types).

Would you like to:
1. Run the scoping-interview workflow to create it
2. Continue without constraints (some features will be limited)
```

### Invalid File Format

```
I found `profile/resume.md` but it appears to be empty or corrupted.

Would you like to:
1. Re-import your resume from another file
2. Paste your resume content directly
3. Check the file manually and try again
```

### User Cancellation

When a user declines to continue at any step:
1. Acknowledge their decision respectfully
2. Explain how to resume later
3. Stop immediately — do not proceed to subsequent steps

```
No problem. When you're ready to continue, just ask me to run the [workflow name] workflow again.
```

## Output Conventions

### Naming Patterns

All output files use lowercase with hyphens:

| Output Type | Path Pattern | Example |
|-------------|--------------|---------|
| Tailored resumes | `applications/resumes/{company}-{role}.md` | `applications/resumes/stripe-staff-engineer.md` |
| Cover letters | `applications/cover_letters/{company}-{role}.md` | `applications/cover_letters/stripe-staff-engineer.md` |
| Job postings | `research/openings/{company}-{role}.md` | `research/openings/netflix-principal-engineer.md` |
| Company profiles | `research/companies/{industry}/{company}.md` | `research/companies/fintech/stripe.md` |
| Industry research | `research/industries.md` | Single file, updated in place |

### Path Normalization Rules

Transform user input to valid file paths:

| Input | Normalized |
|-------|------------|
| `Stripe` | `stripe` |
| `Senior Staff Engineer` | `senior-staff-engineer` |
| `McKinsey & Company` | `mckinsey-company` |
| `AI/ML Engineer` | `ai-ml-engineer` |

**Rules:**
1. Lowercase everything
2. Replace spaces with hyphens
3. Remove special characters (except hyphens)
4. Replace slashes with hyphens
5. Collapse multiple hyphens to single hyphen

### Directory Structure

```
job-coach-and-scout/
├── profile/                     # User data
│   ├── resume.md               # Master resume
│   ├── constraints.yaml        # Job search constraints
│   └── writing_samples/        # Voice analysis samples
├── applications/                # Generated outputs
│   ├── resumes/                # Tailored resumes
│   └── cover_letters/          # Generated cover letters
└── research/                    # Market intelligence
    ├── companies/              # Company profiles by industry
    │   └── {industry}/         # Industry subdirectory
    ├── openings/               # Job posting analyses
    └── industries.md           # Industry research summary
```

## Available Workflows

| # | Workflow | Agent | Purpose | Trigger |
|---|----------|-------|---------|---------|
| 1 | [init](init/workflow.md) | Max & Scout | Set up project structure, import resume and writing samples | First workflow for new projects |
| 2 | scoping-interview | Max | Establish job search constraints and preferences | User wants to define job search criteria |
| 3 | job-scan | Max | Parse job posting into structured requirements | User provides a job posting to analyze |
| 4 | evaluate-fit | Max | Calculate alignment score (read-only assessment) | User asks "how well do I fit this job?" |
| 5 | fit-resume | Max | Tailor resume through interview-driven probing | User wants to tailor resume for a specific job |
| 6 | cover-letter | Max | Generate voice-matched cover letter | User needs a cover letter for an application |
| 7 | resume-review | Max | Adversarial review of master resume | User wants feedback on their resume |
| 8 | industry-research | Scout | Analyze industries and tier by fit | User exploring which industries to target |
| 9 | company-discovery | Scout | Discover and evaluate target companies | User looking for companies to apply to |

To see what workflows are available, ask Claude Code: "What workflows are available?" and it will list these with their purposes.
