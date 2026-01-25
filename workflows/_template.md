# {Workflow Name}

<!--
  TEMPLATE: Copy this file to create new workflows.
  Replace all {placeholders} with actual content.
  Delete these comment blocks when done.
-->

**Agent:** Job Coach (Max)
<!-- Options: "Job Coach (Max)", "Job Scout", "Job Coach (Max) & Job Scout" -->

**Purpose:** {One-line description of what this workflow does}
<!-- Keep it brief - this appears in workflow listings -->

**Trigger:** {When/how users invoke this workflow}
<!-- Examples:
  - "User says 'help me tailor my resume for [company]'"
  - "User asks to evaluate a job posting"
  - "Automatically suggested after completing fit-resume"
-->

## Context Required

<!--
  List files this workflow needs. Use two categories:
  1. Required files (workflow cannot proceed without)
  2. Optional files (enhance workflow but not required)

  If no context needed, write: "None — this is the starting workflow for new projects."
-->

Before starting, load these files:
- `profile/corpus.json` — Resume Corpus (required)
- `profile/constraints.yaml` — Job search constraints (required)

If available, also load:
- `{path/to/optional/file}` — {description}

## Steps

<!--
  Number steps sequentially with descriptive names.
  Write instructions as commands to Claude Code.
  Use checkboxes for multi-part steps users can track.
-->

### Step 1: {Step Name}

{Instructions for Claude Code to follow}

<!-- Example step content:
Read the job posting and extract:
- Required qualifications
- Preferred qualifications
- Key responsibilities
- Company information
-->

### Step 2: {Step Name}

{More instructions}

### Step 3: {Step Name}

{Continue as needed}

<!--
  ERROR HANDLING: Include error handling within steps where failures are likely.
  Use the conversational error pattern:

  **If [error condition]:**
  ```
  I tried to [action] but [problem].

  Would you like to:
  1. [Alternative 1]
  2. [Alternative 2]
  3. [Alternative 3]
  ```
-->

## Output

<!--
  Specify where results are saved.
  Use path patterns with {placeholders} for dynamic values.
  Normalize names: lowercase, hyphens, no special chars.
-->

Save the result to: `{output/path/{company}-{role}.md}`

**Files created:**
- `{path}` — {description}

## Recommend Next

<!--
  Suggest the logical next workflow.
  Bold the workflow name.
  Provide 1-2 sentence rationale.
-->

After completing this workflow, suggest: **{next-workflow-name}**

{Brief explanation of why this is the logical next step}

<!--
================================================================================
WORKFLOW TYPE EXAMPLES
================================================================================

EXAMPLE 1: Resume Tailoring Workflow
================================================================================

# Fit Resume

**Agent:** Job Coach (Max)

**Purpose:** Tailor your master resume for a specific job posting through interview-driven probing.

**Trigger:** User says "help me tailor my resume for [company]" or "fit my resume to this job"

## Context Required

Before starting, load these files:
- `profile/corpus.json` — Resume Corpus (required)
- `profile/constraints.yaml` — Job search constraints (required)
- `research/openings/{company}-{role}.md` — Job posting analysis (required)

If available, also load:
- `applications/resumes/*.md` — Previous tailored resumes for reference

## Steps

### Step 1: Review Job Requirements

Load and analyze the job posting from `research/openings/{company}-{role}.md`.
Identify the top 5 requirements the employer cares most about.

### Step 2: Identify Gaps

Compare requirements against the master resume.
For each requirement:
- Mark as "strong match", "partial match", or "gap"
- Note specific evidence from resume

### Step 3: Interview for Missing Evidence

For each gap or partial match, ask the user:
"The job emphasizes {requirement}. Your resume mentions {related experience} but doesn't explicitly demonstrate {specific skill}. Can you tell me about a time when you {probing question}?"

### Step 4: Tailor Resume

Rewrite relevant sections incorporating the new evidence.
Prioritize the top requirements in bullet ordering.
Maintain the user's voice from writing samples.

### Step 5: Review Changes

Show a diff of changes made.
Ask: "Does this accurately represent your experience? Any changes?"
Iterate until approved.

## Output

Save the result to: `applications/resumes/{company}-{role}.md`

**Files created:**
- `applications/resumes/{company}-{role}.md` — Tailored resume for this application

## Recommend Next

After completing this workflow, suggest: **cover-letter**

Now that your resume is tailored for this role, you can generate a voice-matched cover letter that complements it.

================================================================================

EXAMPLE 2: Research Workflow (Job Scout)
================================================================================

# Industry Research

**Agent:** Job Scout

**Purpose:** Analyze target industries and tier them by fit with your background and constraints.

**Trigger:** User asks "what industries should I target?" or "help me research industries"

## Context Required

Before starting, load these files:
- `profile/corpus.json` — Resume Corpus (required)
- `profile/constraints.yaml` — Job search constraints (required)

If available, also load:
- `research/industries.md` — Previous industry research to update

## Steps

### Step 1: Extract Profile Signals

From the resume, identify:
- Industries user has worked in
- Transferable skills
- Domain expertise
- Role types held

### Step 2: Apply Constraints

From constraints.yaml, note:
- Location preferences (affects industry availability)
- Salary expectations (affects which industries are viable)
- Role type preferences
- Any industry preferences or exclusions

### Step 3: Research Industries

For each potentially relevant industry:
- Current hiring trends
- Typical compensation ranges
- Remote work prevalence
- Growth trajectory
- Fit with user's background

### Step 4: Tier Industries

Categorize into:
- **Tier 1 (Strong Fit):** Direct experience + meets constraints + hiring
- **Tier 2 (Good Fit):** Transferable skills + mostly meets constraints
- **Tier 3 (Stretch):** Requires positioning but possible
- **Not Recommended:** Poor fit or doesn't meet constraints

### Step 5: Present Findings

For each tiered industry, provide:
- Fit assessment (1-2 sentences)
- Key companies to consider
- Positioning recommendations

## Output

Save the result to: `research/industries.md`

**Files created:**
- `research/industries.md` — Industry analysis with tiered recommendations

## Recommend Next

After completing this workflow, suggest: **company-discovery**

Now that we've identified promising industries, let's find specific companies worth targeting.

================================================================================

EXAMPLE 3: No Context Required (Init Workflow)
================================================================================

# Init

**Agent:** Job Coach (Max) & Job Scout

**Purpose:** Set up your job search project with the correct directory structure.

**Trigger:** First workflow for new projects

## Context Required

None — this is the starting workflow for new projects.

## Steps

### Step 1: Welcome

Welcome to Job Coach & Scout! Let's get your project set up.

[... rest of steps ...]

================================================================================
-->
