# Cover Letter

## Summary

**Purpose:** Generate a voice-matched cover letter by creating and using a persistent, structured voice profile.
**Agent:** Job Coach (Max)
**Reads:**
- `profile/corpus.json` — Resume Corpus (required).
- `research/openings/{company}-{role}.md` — Target job details (required).
- `profile/constraints.yaml` — For user preferences and existing voice profile.
- `profile/writing_samples/*.md` — For initial voice analysis.
- `applications/resumes/{company}-{role}.md` — Tailored resume (preferred).
**Creates:**
- `applications/cover_letters/{company}-{role}.md` — Voice-matched cover letter.
- `profile/constraints.yaml` (updated) — With the user's confirmed `voice_profile`.
**Approximate time:** 15-25 minutes
**Prerequisites:** job-scan completed; tailor-resume recommended.

---

> **VOICE-MATCHED GENERATION**: Analyzes your writing samples to create a persistent, structured profile of your authentic voice, then uses it to generate a cover letter that sounds like you wrote it.

**Trigger:** User says "help me write a cover letter for [company]" or after `tailor-resume`.

## Persona

**Load and adopt:** `agents/job-scout.md`.

## Context Required
- `profile/corpus.json`
- `research/openings/{company}-{role}.md`
- `profile/writing_samples/`
- `profile/constraints.yaml`

---

## Steps

### Step 1: Establish Voice Profile

**1a. Check for Existing Voice Profile:**
- **Instruction:** Check if `profile/constraints.yaml` contains a `voice_profile` block.
- **If it exists:** "I've found your previously saved voice profile. It describes your style as {summary of profile: e.g., 'Informal, Concise, and Direct'}. Would you like me to use this profile, or should I re-analyze your writing samples?"
    - If user agrees, use the existing profile and skip to Step 5.
    - If user wants to re-analyze, proceed to the next step.
- **If it does not exist:** Proceed to the next step.

**1b. Check for Writing Samples:**
- **Instruction:** If no voice profile exists, check for files in `profile/writing_samples/`.
- **If no samples:** Instruct the user to add some samples (cover letters, blog posts, professional emails) and explain why they are necessary for the voice-matching feature. Wait for user to confirm they've added files.

### Step 2: Analyze Writing Voice (If Needed)

**Instruction:** This step defines the structure of the voice analysis.

- **Instruction:** "Analyze the writing samples for the following specific attributes:
    - **Formality:** (Formal, Semi-formal, Informal) - e.g., "I am writing to express my interest" vs. "I'm excited to apply".
    - **Verbosity:** (Concise, Descriptive) - Are sentences short and to the point, or longer and more detailed?
    - **Tone:** (e.g., 'Confident and direct', 'Collaborative and team-oriented', 'Enthusiastic and passionate').
    - **Keywords:** A list of commonly used positive adjectives or verbs (e.g., 'drove', 'led', 'strategic', 'impactful')."

### Step 3: Present Voice Analysis for Confirmation

**Instruction:**
- Present the structured analysis from Step 2 to the user for confirmation.
- **Example:** "Here's what I've learned about your writing style: You tend to be **Semi-formal** and **Descriptive**. Your tone is **Confident and direct**, and you often use action words like **'architected'** and **'delivered'**. Does this sound right?"
- **CRITICAL:** Wait for user confirmation. If they disagree, ask for clarification and adjust the profile before proceeding.

### Step 4: Save Confirmed Voice Profile

**Instruction:**
- Once the user confirms the voice profile, save it to `profile/constraints.yaml`.
- **Read:** Load the current `profile/constraints.yaml`.
- **Modify:** Add a new top-level block named `voice_profile` with the confirmed, structured attributes.
- **Safe Write:** Perform a safe, validated write to update the `constraints.yaml` file.
- **Inform:** "Great. I've saved this voice profile to your `constraints.yaml`. I'll use it for future writing tasks."

### Step 5: Load Job & Resume Context

**Instruction:**
- Load the parsed job posting, the tailored resume (if it exists), the full resume corpus, and the user's name from constraints.
- Identify the top 3-5 key requirements from the job and the main accomplishments featured in the tailored resume.

### Step 6: Generate Cover Letter Draft (Corpus-Enhanced)

**Instruction:**
- Your goal is to write a compelling narrative that sounds like the user, not a generic template.
- **Prioritize Narrative Fields:** When telling the story of a key accomplishment, **first** check the `corpus.json` for a `narrative_description` associated with that position (from the `linkedin-review` workflow). If it exists, use it as the primary source material.
- **If no narrative exists:** Use the tailored resume's accomplishments as a guide. Find those accomplishments in the corpus and use their `content`, `variations`, and any other related bullets to tell the *story* behind the achievement.
- **Apply Voice:** Combine this deep context with the confirmed `voice_profile` to generate the draft.

### Step 7: Present Draft for Feedback

**Instruction:**
- Present the draft to the user. Ask for specific feedback: "How does this sound to you? Does it capture your voice? Is there anything you'd change?"

### Step 8: Iterative Refinement Loop

**Instruction:**
- Based on user feedback, refine the draft. This could involve changing the tone, swapping out accomplishments, or rephrasing sentences.
- Continue to iterate until the user is satisfied.

### Step 9: Save Cover Letter with Metadata

**Instruction:**
- Save the final, approved cover letter to `applications/cover_letters/{company}-{role}.md`.
- Include metadata in the file, including the date, the source job posting, and the tailored resume it's linked to.

### Step 10: Workflow Completion

**Instruction:**
- Inform the user that the cover letter has been saved.
- Suggest next steps, such as preparing for an interview or finding other jobs to apply for.
