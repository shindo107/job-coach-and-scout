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
- `profile/corpus.json` — The structured Resume Corpus (required)
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
- `profile/corpus.json` — The structured Resume Corpus (required)
- `profile/constraints.yaml` — Job search constraints (required)
```

**Optional files** — Enhance workflow but not required:
```markdown
If available, also load:
- `applications/resumes/*.md` — Previously generated resumes
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
I need your Resume Corpus to continue, but I couldn't find `profile/corpus.json`.

Would you like to:
1. Run the init workflow to create your corpus from your resume
2. Point me to the correct file path if you moved it
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
│   ├── corpus.json             # Your structured Resume Corpus
│   ├── constraints.yaml        # Job search constraints
│   └── writing_samples/        # Voice analysis samples
│
├── applications/                # Generated outputs
│   ├── resumes/                # Tailored resumes (Markdown)
│   └── cover_letters/          # Generated cover letters
│
├── research/                    # Market intelligence
│   ├── ...
│
└── tools/                       # Utility scripts
    ├── validate-json.sh        # Deterministic JSON validator
    └── validate-yaml.sh        # Deterministic YAML validator
```

## Available Workflows

| Workflow | Purpose | Agent | Prerequisites |
|----------|---------|-------|---------------|
| **[init](init/workflow.md)** | Parse a resume into the structured `corpus.json`. | Both | None |
| **[scoping-interview](scoping-interview/workflow.md)** | Capture job search preferences and constraints. | Max | init |
| **[job-scan](job-scan/workflow.md)** | Parse job posting into structured requirements. | Scout | None |
| **[evaluate-fit](evaluate-fit/workflow.md)** | Assess alignment between `corpus.json` and a job. | Max | job-scan |
| **[fit-resume](fit-resume/workflow.md)** | Tailor a resume by querying and updating `corpus.json`. | Max | job-scan |
| **[cover-letter](cover-letter/workflow.md)** | Generate a voice-matched cover letter using corpus context. | Max | fit-resume |
| **[resume-review](resume-review/workflow.md)** | Adversarially review and improve the contents of `corpus.json`. | Max | init |
| **[industry-research](industry-research/workflow.md)** | Research and tier industries by fit. | Scout | init, scoping-interview |
| **[company-discovery](company-discovery/workflow.md)** | Discover and rank companies in target industry. | Scout | init, scoping-interview |
| **[audit](audit/workflow.md)** | Verify core workflows are functioning correctly. | Both | None |

## Workflow Dependency Graph

```
                    ┌─────────────────┐
                    │      init       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ scoping-interview│
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────────┐     │     ┌────────▼────────┐
     │ industry-research│     │     │    job-scan     │
     └────────┬────────┘     │     └────────┬────────┘
              │              │              │
     ┌────────▼────────┐     │     ┌────────▼────────┐
     │company-discovery│     │     │  evaluate-fit   │
     └────────┬────────┘     │     └────────┬────────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │   fit-resume    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  cover-letter   │
                    └─────────────────┘

     Standalone:
     - resume-review (improves baseline, any time)
     - audit (system verification, any time)
```

## Common User Journeys

### First-Time Setup
```
init → scoping-interview
```
Get your project set up and capture your job search preferences.

### Apply to a Specific Job
```
job-scan → evaluate-fit → fit-resume → cover-letter
```
The complete application workflow: parse the posting, assess your fit, tailor your resume, generate a cover letter.

### Quick Application (Skip Fit Evaluation)
```
job-scan → fit-resume → cover-letter
```
If you're confident about the role, skip the read-only assessment and go straight to tailoring.

### Research Mode (Exploring Options)
```
industry-research → company-discovery → job-scan
```
Start broad: research industries, discover companies, then target specific postings.

### Improve Your Baseline
```
resume-review (standalone)
```
Strengthen your master resume before any applications. Can be done anytime.

## Multi-Workflow Requests (Batch Execution)

You can request multiple workflows in a single conversation. Claude Code will execute them in sequence, passing context forward.

### Example Patterns

**"Scan this posting and tailor my resume"**
```
1. job-scan (parses requirements)
2. fit-resume (uses parsed requirements as input)
```

**"Full application for this posting"**
```
1. job-scan (parses requirements)
2. fit-resume (tailors resume against requirements)
3. cover-letter (generates letter using tailored resume)
```

**"Research fintech and find companies"**
```
1. industry-research (tiers industries, identifies fintech fit)
2. company-discovery (discovers companies in fintech)
```

### Context Passing

Each workflow automatically passes its outputs to the next:
- **job-scan** → `research/openings/{company}-{role}.md` → **fit-resume**
- **fit-resume** → `applications/resumes/{company}-{role}.md` → **cover-letter**
- **industry-research** → `research/industries.md` → **company-discovery**

### Partial Failure Handling

If a workflow in a sequence fails:
- The sequence stops at that point
- Claude Code reports what failed and why
- Previous outputs are preserved
- You can fix the issue and continue from the failure point

## Cross-Session Continuity

### All State is in Files

Your progress persists in the filesystem — no database, no session storage. This means:
- You can close Claude Code and resume later
- A new session can read all previous outputs
- Multiple sessions can work on the same project

### Resuming Previous Work

When you start a new Claude Code session:

**Your profile is in `profile/`:**
- `corpus.json` — Your structured Resume Corpus.
- `constraints.yaml` — Your job search preferences.
- `writing_samples/` — Your voice analysis samples.

**Previous applications are in `applications/`:**
- `resumes/` — Tailored resumes by company.
- `cover_letters/` — Generated cover letters.

**Research is in `research/`:**
- `industries.md` — Industry tier analysis.
- `companies/{industry}/` — Company profiles.
- `openings/` — Parsed job postings.

### Common Resume Commands

```
"Continue tailoring for Stripe"
→ Loads existing work from applications/resumes/stripe-*.md

"What have I done so far?"
→ Summarizes all output directories and files

"Start a new application for Netflix"
→ Begins fresh job-scan for Netflix posting
```

### Status Check Capability

Ask "What have I done so far?" and Claude Code will:

1. **Check `profile/` directory:**
   - corpus.json exists? "✓ Resume Corpus created"
   - constraints.yaml exists? "✓ Preferences captured"
   - writing_samples/ has files? "✓ Voice samples collected"

2. **Check `applications/` directory:**
   - List all resumes in `applications/resumes/`
   - List all cover letters in `applications/cover_letters/`

3. **Check `research/` directory:**
   - industries.md exists? "✓ Industry research done"
   - companies/ has subdirectories? "✓ Company profiles created"

4. **Present summary:**
   ```
   Here's what you've done so far:
   - Profile: Complete (resume, constraints, 3 writing samples)
   - Applications: 2 tailored resumes (Stripe, Acme), 1 cover letter (Stripe)
   - Research: Industry analysis complete, 8 fintech companies profiled

   What would you like to work on next?
   ```

## How to Run Workflows

Just ask Claude Code naturally:

| What You Say | Workflow Triggered |
|--------------|-------------------|
| "Help me get started" | init |
| "Set up my constraints" | scoping-interview |
| "Scan this job posting" | job-scan |
| "How well do I match?" | evaluate-fit |
| "Tailor my resume for Stripe" | fit-resume |
| "Write a cover letter" | cover-letter |
| "Review my resume" | resume-review |
| "Research industries for me" | industry-research |
| "Find fintech companies" | company-discovery |

## Workflow Explanation

To understand what a workflow does before running it, ask:

```
"What does fit-resume do?"
"Explain the cover-letter workflow"
"What files does job-scan create?"
```

Claude Code will read the workflow's Summary section and explain:
- What the workflow does
- What files it reads
- What files it creates
- Approximate time required
- Prerequisites needed
