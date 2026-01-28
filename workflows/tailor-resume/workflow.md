# Tailor Resume

## Summary

**Purpose:** Analyze your fit against a job posting, track three distinct fit scores (corpus fit, initial resume fit, final resume fit), and interactively tailor your resume while discovering and cataloging new corpus entries.
**Agent:** Job Coach (Max)
**Reads:**
- `profile/corpus.json` — Resume Corpus (required)
- `research/openings/{company}-{role}.md` — Parsed job posting with fit score from job-scan (required)
- `profile/constraints.yaml` — For feedback style preference (optional)
**Creates:**
- `applications/resumes/{company}-{role}.md` — Tailored resume with fit score progression (initial → final).
- `profile/corpus.json` (updated) — Enriched with explicitly cataloged new accomplishments, variations, and skills discovered during tailoring.
**Key Metrics Tracked:**
- **Corpus Fit Score** — Theoretical maximum based on all corpus content
- **Initial Resume Fit Score** — Starting point of the draft resume
- **Final Resume Fit Score** — Result after tailoring
- **Corpus Discoveries** — New accomplishments, variations, and skills added
**Prerequisites:** `job-scan` completed for the target posting.

---

> **CORE WORKFLOW**: This is the heart of Job Coach & Scout. It begins with a detailed gap analysis and then uses an interview-driven model to extract forgotten experiences, close gaps, and position you as the ideal candidate.

**Trigger:** User says "help me tailor my resume for [company]", "tailor my resume", or after `job-scan` identifies a promising role.

## Persona

**Load and adopt:** `agents/job-coach.md`. Embody Max's expert, direct, and adversarial persona to guide the user through a rigorous tailoring session.

## Context Required

- `profile/corpus.json` (required)
- `research/openings/{company}-{role}.md` (required)
- `profile/constraints.yaml` (optional)

**If corpus doesn't exist:**
```
I need your Resume Corpus to tailor. I couldn't find `profile/corpus.json`.

Would you like to:
1. Run the init workflow to create your corpus
2. Provide the path to your resume file (I'll help import it)
```

**If job posting doesn't exist:**
```
I need a parsed job posting to tailor against. I couldn't find a posting in `research/openings/`.

Would you like to:
1. Run job-scan first to analyze a job posting
2. Specify which posting to use (provide filename)
```

## Session Continuity

**Claude Code conversation history automatically preserves your progress.** You can pause at any checkpoint and resume later:

- **To pause:** At any checkpoint, say "take a break" or simply close the session
- **To resume:** In the same Claude Code session, say "let's continue" or "where were we?"
- **To resume in a new session:** Say "continue tailor-resume for {company}" — Claude Code will reload context and ask where you left off

**Checkpoints are provided after each gap is addressed** (see Step 4d), summarizing:
- Which gap was just addressed
- What evidence was captured
- How many gaps remain

**Note:** If starting a completely new session, you may need to re-share any experiences discussed previously, as they exist only in conversation history.

---

## Steps

### Step 1: Detailed Gap Analysis

**Instruction:** This step replaces the deprecated `evaluate-fit` workflow. Your goal is to conduct a thorough, read-only analysis before any tailoring begins.

**1a. Load Context:**
- **Instruction:** Load `corpus.json` and the target `research/openings/{company}-{role}.md`.
- **Instruction:** Extract the MUST-HAVE and NICE-TO-HAVE requirements from the job posting file.

**1b. Score Each Requirement:**
- **Instruction:** For each requirement, search the user's corpus for evidence (in `skills` and `accomplishments`). Score each requirement as a Full Match (100%), Partial Match (50%), or No Match (0%) based on the strength of the evidence.

**1c. Calculate Overall Alignment Score:**
- **Instruction:** Calculate a weighted alignment score based on the individual requirement scores. MUST-HAVE requirements should be weighted more heavily than NICE-TO-HAVE ones.

### Step 2: Present Strategic Briefing

**Instruction:** Present the findings from Step 1 as a "Strategic Briefing" to kick off the tailoring session. This establishes the baseline scores that will be improved during tailoring.

**2a. Display Dual Fit Scores:**
- **Instruction:** Calculate and present TWO distinct scores:
  1. **Corpus Fit Score** — The theoretical maximum alignment if we use ALL relevant content from your corpus. This represents your full potential for this role.
  2. **Initial Resume Fit Score** — The alignment of the initial draft resume (assembled from best-matching content only). This is your starting point.
- **Instruction:** Present the scores clearly:
  ```
  ## Strategic Briefing: {Company} - {Role}

  **Corpus Fit Score: {X}%** — Your full potential based on everything in your corpus
  **Initial Resume Fit Score: {Y}%** — Where we're starting with the initial draft

  The gap between these scores ({X-Y}%) represents untapped potential we can unlock during tailoring.
  ```

**2b. Display Verdict:**
- **Instruction:** Provide a qualitative assessment based on the corpus fit score:
  - **80%+:** "Excellent Starting Point — You have strong evidence for most requirements"
  - **60-79%:** "Good Foundation — Solid match with some gaps to address"
  - **40-59%:** "Significant Gaps — We'll need to dig for experiences"
  - **<40%:** "Stretch Role — Be prepared for extensive exploration"

**2c. Summarize Strengths and Gaps:**
- **Instruction:** Create two lists:
    - **Strengths:** List the top 3-5 requirements where strong evidence was found in the corpus.
    - **Actionable Gaps:** List the top 3-5 requirements, prioritizing unmet MUST-HAVEs, where little or no evidence was found.

**2d. Set the Agenda:**
- **Example Dialogue (as Max):** "Alright, I've analyzed your corpus against this role. Your **Corpus Fit is {X}%** — that's your ceiling. The **Initial Resume scores {Y}%** — that's our starting point. You have strong evidence for {list of strengths}. But we have {N} actionable gaps: {list of gaps}. Our mission is to close these gaps and get your resume as close to that {X}% ceiling as possible. Let's start with the biggest gap: {the top gap}."

### Step 3: Assemble Initial Draft from Strengths

**Instruction:**
- Based on the "Strengths" identified in the analysis, assemble an initial draft of the resume. This draft will only contain the parts where the user is already a strong fit.
- Present this draft as the "solid foundation" that you will now build upon.

### Step 4: Interactive Gap-Closing Interview (CORE)

**Instruction:** This is the interactive interview where you address the "Actionable Gaps" from the strategic briefing. Go through them one by one.

**4a. Address a Specific Gap:**
- **Example Dialogue (as Max):** "Let's focus on the first gap: the requirement for 'Experience with multi-threaded programming'. I don't see any accomplishments in your corpus that explicitly mention this. Tell me about a time you had to work on a project involving concurrency or parallelism, even if it wasn't the main focus."

**4b. Probe and Draft:**
- **Instruction:** Based on the user's story, probe for specifics, quantification, and outcomes.
- **Instruction:** Draft a new accomplishment bullet that directly addresses the gap. Read it back to the user for confirmation. "Here's how I'd phrase that for the resume: '{drafted bullet}'. Does that accurately capture it?"

**4c. Capture as New Corpus Entry:**
- **Instruction:** Once the user confirms the new accomplishment, create a new JSON object for it in your context/memory. Assign it a new `id` and link it to the appropriate `position_id`.

**4d. Repeat for all Major Gaps:**
- **Instruction:** Continue this process until all the major gaps identified in the strategic briefing have been addressed.

**4e. Checkpoint (after each gap):**
- **Instruction:** After addressing each gap, provide a checkpoint summary:
```
✅ Gap addressed: {requirement name}
   Evidence captured: {brief summary of new accomplishment}

Progress: {N} of {M} gaps addressed.
Remaining: {list of remaining gaps}

Ready to continue, or would you like to take a break?
```
- If user wants to pause, confirm their progress is saved in conversation history and they can resume with "let's continue".

### Step 5: Final Review

**Instruction:**
- After addressing the gaps, assemble the complete, tailored resume including both the original strengths and the newly created accomplishments.
- Present this final version to the user for their approval.

### Step 6: Confirm and Update Resume Corpus

**Instruction:** This step safely writes the improvements back to the central knowledge base and explicitly documents what was discovered.

**6a. Present Corpus Discoveries Summary:**
- **Instruction:** Before saving, present a clear summary of ALL new content discovered during the tailoring session:
  ```
  ## Corpus Discoveries During This Session

  **New Accomplishments Added:** {N}
  1. **{accomplishment_id}** — "{brief summary of bullet}"
     - Position: {company} - {title}
     - Skills tagged: {skill1}, {skill2}
     - Gap addressed: {requirement this closes}

  2. **{accomplishment_id}** — "{brief summary of bullet}"
     - Position: {company} - {title}
     - Skills tagged: {skill1}, {skill2}
     - Gap addressed: {requirement this closes}

  **New Variations Added:** {M}
  - {accomplishment_id}.var_{N}: Alternative phrasing for {context}

  **New Skills Identified:** {K}
  - {skill_name} (discovered from: {accomplishment_id})

  These entries will be available for ALL future applications, not just this one.
  ```

**6b. Confirm New Entries:**
- **Instruction:** Ask the user for explicit confirmation:
  ```
  Ready to add these {N} accomplishments, {M} variations, and {K} skills to your corpus?
  1. Yes, save all
  2. Let me review/edit first
  3. Skip corpus update (resume will still be saved)
  ```

**6c. Construct and Validate:**
- **Instruction:** Merge the confirmed entries into the corpus, save to a `.tmp` file, and validate it using `tools/validate-json.sh`.

**6d. Perform Atomic Write:**
- **Instruction:** If validation passes, perform the safe rename (`.bak`, then rename `.tmp`). Report success with specifics:
  ```
  ✓ Corpus updated successfully
  - Added: {N} accomplishments, {M} variations, {K} skills
  - Backup saved: profile/corpus.json.bak
  ```

### Step 7: Save Final Tailored Resume

**Instruction:** This step is also identical to the original workflow.

- **Instruction:** Add a metadata header to the final markdown resume, including the final (improved) alignment score.
- **Instruction:** Save the file to `applications/resumes/{company}-{role}.md`.

### Step 8: Completion Summary & Recommendation

**Instruction:** Present a comprehensive summary showing the full journey from start to finish.

**Summary:**
```
## Tailoring Complete: {Company} - {Role}

### Fit Score Progression
┌─────────────────────────────────────────────────────┐
│  Corpus Fit:        {X}%  ████████████░░  (ceiling) │
│  Initial Resume:    {Y}%  ██████████░░░░  (start)   │
│  Final Resume:      {Z}%  ████████████░░  (result)  │
└─────────────────────────────────────────────────────┘

**Improvement:** +{Z-Y}% from starting point
**vs Ceiling:**  {X-Z}% potential remains (if any)

### Corpus Discoveries (Reusable for Future Applications)
{N} new accomplishments added:
  • {brief description 1} → closes gap: {requirement}
  • {brief description 2} → closes gap: {requirement}
  • ...

{M} new variations added
{K} new skills identified

### Files Updated
- **Resume saved:** `applications/resumes/{company}-{role}.md`
- **Corpus updated:** `profile/corpus.json` (+{N} accomplishments)
- **Backup created:** `profile/corpus.json.bak`
```

**Interpret the Scores:**
- **Instruction:** Provide context on what the scores mean:
  - If Final ≈ Corpus Fit: "You've maximized your potential for this role based on your current experience."
  - If Final < Corpus Fit by >10%: "There's still {X-Z}% untapped potential. Consider revisiting gaps you skipped or exploring deeper variations."
  - If Final improved significantly (>15%): "Great session! The new accomplishments we discovered significantly strengthened your positioning."

**Recommend Next:**
- **Instruction:** Suggest `cover-letter` as the logical next step: "Your tailored resume is ready at {Z}% fit. Shall we write a compelling cover letter to go with it?"
- **If corpus was significantly enriched:** Also mention: "The {N} new accomplishments we added will also strengthen your applications to similar roles."

## Output

**Files created/modified:**
- `profile/corpus.json` (updated with new experiences)
- `profile/corpus.json.bak` (backup of the previous version)
- `applications/resumes/{company}-{role}.md` (the tailored Markdown resume for this specific job)

## Recommend Next

After this workflow completes successfully, suggest **cover-letter**.
