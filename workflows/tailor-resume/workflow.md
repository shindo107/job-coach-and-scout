# Tailor Resume

## Summary

**Purpose:** Analyze your fit against a job posting and interactively tailor your resume to address gaps and highlight strengths.
**Agent:** Job Coach (Max)
**Reads:**
- `profile/corpus.json` — Resume Corpus (required)
- `research/openings/{company}-{role}.md` — Parsed job posting (required)
- `profile/constraints.yaml` — For feedback style preference (optional)
**Creates:**
- `applications/resumes/{company}-{role}.md` — Tailored resume with alignment scores and metadata.
- `profile/corpus.json` (updated) — Enriched with new accomplishments or variations discovered during tailoring.
**Approximate time:** 25-50 minutes
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

**Instruction:** Present the findings from Step 1 as a "Strategic Briefing" to kick off the tailoring session.

**2a. Display Score and Verdict:**
- **Instruction:** State the overall alignment score and a qualitative verdict (e.g., "Excellent Starting Point", "Significant Gaps to Address").

**2b. Summarize Strengths and Gaps:**
- **Instruction:** Create two lists:
    - **Strengths:** List the top 3-5 requirements where strong evidence was found in the corpus.
    - **Actionable Gaps:** List the top 3-5 requirements, prioritizing unmet MUST-HAVEs, where little or no evidence was found.

**2c. Set the Agenda:**
- **Example Dialogue (as Max):** "Alright, I've analyzed your current resume corpus against this role. Your starting alignment is {X}%. You have strong, quantifiable evidence for {list of strengths}. However, we have actionable gaps in {list of gaps}. Our mission now is to go through these gaps one by one and find the experiences in your history to close them. Let's start with the biggest gap: {the top gap}."

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

**Instruction:** This step safely writes the improvements back to the central knowledge base. It is identical to the corresponding step in the original workflow.

**6a. Confirm New Entries:**
- **Instruction:** Summarize all new accomplishments and variations drafted during the session and ask the user for final confirmation before saving.

**6b. Construct and Validate:**
- **Instruction:** Merge the new entries into the corpus, save to a `.tmp` file, and validate it using `tools/validate-json.sh`.

**6c. Perform Atomic Write:**
- **Instruction:** If validation passes, perform the safe rename (`.bak`, then rename `.tmp`). Report success to the user.

### Step 7: Save Final Tailored Resume

**Instruction:** This step is also identical to the original workflow.

- **Instruction:** Add a metadata header to the final markdown resume, including the final (improved) alignment score.
- **Instruction:** Save the file to `applications/resumes/{company}-{role}.md`.

### Step 8: Completion Summary & Recommendation

**Summary:**
```
## Tailoring Complete!

We've significantly improved your alignment for this role.
- **Initial Score:** {X}%
- **Final Score:** {Y}%

Your resume has been tailored for {Company} and saved.

More importantly, your central Resume Corpus has been updated with {N} new accomplishments, making you a stronger candidate for future roles requiring these skills.

**File saved:** `applications/resumes/{company}-{role}.md`
**Corpus updated:** `profile/corpus.json`
```

**Recommend Next:**
- **Instruction:** Suggest `cover-letter` as the logical next step. "Your tailored resume is ready. Shall we write a compelling cover letter to go with it?"

## Output

**Files created/modified:**
- `profile/corpus.json` (updated with new experiences)
- `profile/corpus.json.bak` (backup of the previous version)
- `applications/resumes/{company}-{role}.md` (the tailored Markdown resume for this specific job)

## Recommend Next

After this workflow completes successfully, suggest **cover-letter**.
