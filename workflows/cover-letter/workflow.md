# Cover Letter

## Summary

**Purpose:** Generate a voice-matched cover letter through writing sample analysis and iterative refinement
**Agent:** Job Coach (Max)
**Reads:**
- `profile/corpus.json` — Resume Corpus (required)
- `research/openings/{company}-{role}.md` — Target job details (required)
- `profile/writing_samples/*.md` — For voice matching (recommended)
- `profile/constraints.yaml` — For name and preferences (optional)
- `applications/resumes/{company}-{role}.md` — Tailored resume (preferred)
**Creates:**
- `applications/cover_letters/{company}-{role}.md` — Voice-matched cover letter with metadata
**Approximate time:** 15-25 minutes (voice analysis + iterative refinement)
**Prerequisites:** job-scan completed; fit-resume recommended

---

> **VOICE-MATCHED GENERATION**: Analyzes your writing samples to capture your authentic voice, then generates a personalized cover letter that sounds like you wrote it.

**Trigger:** User says "help me write a cover letter for [company]", "cover letter for [role]", or after fit-resume suggests generating a cover letter

## Session Continuity

**Claude Code conversation history automatically preserves your progress.** You can pause at any checkpoint and resume later:

- **To pause:** At any `[CHECKPOINT]`, say "take a break" or simply close the session
- **To resume:** In the same Claude Code session, say "let's continue" or "where were we?"
- **To resume in a new session:** Say "continue cover letter for {company}" — Claude Code will reload context and ask where you left off

**Checkpoints in this workflow:**
- `[CHECKPOINT: Voice Analysis]` — After voice profile confirmed
- `[CHECKPOINT: Draft Ready]` — After initial draft generated
- `[CHECKPOINT: Iteration]` — After each refinement round

## Context Required

Before starting, load these files:
- `profile/corpus.json` — The user's full resume knowledge base (required).
- `research/openings/{company}-{role}.md` — Target job details (required).

If available, also load:
- `applications/resumes/{company}-{role}.md` — The tailored resume for this role (highly recommended, as it indicates which experiences to focus on).
- `profile/writing_samples/*.md` — For voice matching.
- `profile/constraints.yaml` — For user's name and preferences.

**If corpus doesn't exist:**
```
I need your Resume Corpus to write a cover letter. I couldn't find `profile/corpus.json`.

Would you like to run the init workflow to create your resume corpus?
```

**If job posting doesn't exist:**
```
I need a parsed job posting to write a targeted cover letter. I couldn't find a posting in `research/openings/`.

Would you like to run job-scan first to analyze a job posting?
```

## Pre-Flight Validation
**(This section remains the same)**

## Steps

### Step 1: Check for Writing Samples
**(This section remains the same)**

### Step 2: Analyze Writing Voice
**(This section remains the same)**

### Step 3: Present Voice Analysis for Confirmation
**(This section remains the same)**

### Step 4: Load Job & Resume Context

1.  **- [ ] Load Files:**
    -   Load the parsed job posting (`research/openings/{...}.md`).
    -   Load the tailored resume (`applications/resumes/{...}.md`). If it doesn't exist, inform the user you'll use the main corpus but results may be less targeted.
    -   Load the resume corpus (`profile/corpus.json`).
    -   Load user's name from `constraints.yaml`.

2.  **- [ ] Identify Key Themes:**
    -   From the job posting, extract the top 3-5 key requirements.
    -   From the tailored resume (if it exists), identify the main accomplishments the user chose to feature for this role.

### Step 5: Generate Cover Letter Draft (Corpus-Enhanced)

1.  **- [ ] Synthesize a Narrative:**
    -   **Instruction:** "Your goal is to write a compelling narrative, not just repeat the resume. Use the key themes from the job posting and the tailored resume as your guide."
    -   **Instruction:** "For the 1-2 most important accomplishments featured in the tailored resume, find those entries in the `corpus.json`. Read their `content`, any `variations`, and any other related `accomplishments` under the same `position_id`. Use this rich context to tell the *story* behind the bullet point. For example, instead of 'Reduced latency by 40%', you could write 'When my team was tasked with improving a sluggish API, I dug in and discovered a caching bottleneck. By implementing a new strategy, I was able to reduce p95 latency by 40%...'."
    -   **Instruction:** "Combine this deep context with the user's voice profile to generate a draft cover letter."

2.  **- [ ] Structure the Draft:**
    -   **Opening Hook:** Connect to the company's mission or a specific challenge mentioned in the posting.
    -   **Value Proposition (Body):** Build the narrative around the 1-2 key accomplishments, using the deep context from the corpus.
    -   **Closing:** Reiterate enthusiasm with a clear call to action.

3.  **- [ ] Store draft for iteration tracking.**

### Step 6: Present Draft for Feedback
**(This section remains the same)**

### Step 7: Iterative Refinement Loop
**(This section remains the same)**

### Step 8: Save Cover Letter with Metadata

**(This section remains the same, but the `linked_resume` metadata field should point to the tailored resume used for context).**

### Step 9: Workflow Completion
**(This section remains the same).**

## Output
**(This section remains the same).**

## Recommend Next
**(This section remains the same).**
