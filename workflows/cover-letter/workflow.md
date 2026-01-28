# Cover Letter

## Summary

**Purpose:** Generate a voice-matched cover letter using your persistent voice profile.
**Agent:** Job Scout (Scout)
**Reads:**
- `profile/corpus.json` — Resume Corpus (required).
- `research/openings/{company}-{role}.md` — Target job details (required).
- `profile/voice_profile.json` — Your writing voice characteristics (created by init or this workflow).
- `profile/writing_samples/*` — For voice analysis if no profile exists.
- `profile/constraints.yaml` — For user preferences.
- `applications/resumes/{company}-{role}.md` — Tailored resume (preferred).
**Creates:**
- `applications/cover_letters/{company}-{role}.md` — Voice-matched cover letter.
- `profile/voice_profile.json` — Created if it doesn't exist (from writing samples analysis).
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
- `profile/voice_profile.json` (or `profile/writing_samples/` if no profile exists)
- `profile/constraints.yaml`

---

## Steps

### Step 1: Establish Voice Profile

**1a. Check for Existing Voice Profile:**
- **Instruction:** Check if `profile/voice_profile.json` exists.
- **If it exists:** Load the file and present a summary to the user:
  ```
  I found your voice profile (created {created_at date}).

  Your style: {tone.formality}, {tone.confidence}, {tone.energy}
  Sentence structure: {sentence_structure.length_tendency}
  Vocabulary: {vocabulary.complexity}

  Signature elements:
  - {signature_elements.distinctive_phrases[0]}
  - {signature_elements.distinctive_phrases[1]}

  Would you like me to use this profile, or re-analyze your writing samples?
  ```
    - If user agrees, use the existing profile and skip to Step 5.
    - If user wants to re-analyze, proceed to the next step.
- **If it does not exist:** Proceed to the next step.

**1b. Check for Writing Samples:**
- **Instruction:** If no voice profile exists, check for files in `profile/writing_samples/`.
- **If no samples:** Instruct the user to add some samples (cover letters, blog posts, professional emails) and explain why they are necessary for the voice-matching feature. Wait for user to confirm they've added files.
- **If samples exist:** Proceed to Step 2.

### Step 2: Analyze Writing Voice (If Needed)

**Instruction:** This step performs comprehensive voice analysis matching the schema from the init workflow.

- **Instruction:** Read all files in `profile/writing_samples/` and analyze for the following dimensions:

    **Tone & Register:**
    - Formality level: formal, professional, conversational, casual
    - Confidence style: assertive, measured, humble, collaborative
    - Energy: enthusiastic, calm, reserved, dynamic

    **Sentence Structure:**
    - Average sentence length tendency: short-punchy, medium, long-complex
    - Sentence variety: consistent, varied
    - Preferred openings: direct statements, context-setting, questions

    **Vocabulary Patterns:**
    - Complexity: simple-clear, moderate, sophisticated
    - Technical density: minimal, moderate, heavy
    - Distinctive words/phrases the user frequently uses

    **Voice & Perspective:**
    - Person: first-person dominant, mixed, third-person
    - Voice: active-dominant, mixed, passive-tolerant
    - Self-reference style: "I achieved", "Led the team", "We delivered"

    **Rhetorical Patterns:**
    - Argument structure: direct-first, building, storytelling
    - Evidence style: metrics-heavy, example-driven, principle-based

    **Signature Elements:**
    - Extract 3-5 distinctive phrases or constructions
    - Note consistent patterns in describing achievements

### Step 3: Present Voice Analysis for Confirmation

**Instruction:**
- Present a summary of the analysis to the user for confirmation.
- **Example:**
  ```
  Here's what I've learned about your writing voice:

  Tone: Professional, confident, dynamic
  Style: Medium-length sentences, moderate vocabulary
  Voice: First-person, active voice dominant
  Rhetoric: Direct-first arguments, metrics-heavy evidence

  Signature elements I noticed:
  - "Drove X by doing Y"
  - "Partnered with stakeholders to..."
  - Frequent use of "delivered", "architected", "scaled"

  Does this sound like you? [Yes / Adjust / Skip voice matching]
  ```
- **CRITICAL:** Wait for user confirmation. If they want adjustments, ask for specifics and modify the profile.

### Step 4: Save Confirmed Voice Profile

**Instruction:**
- Once the user confirms the voice profile, save it to `profile/voice_profile.json`.
- **Generate:** Create a JSON object following the schema from init workflow:
  ```json
  {
    "schema_version": "1.0",
    "created_at": "{ISO timestamp}",
    "samples_analyzed": ["{filename_1}", "{filename_2}"],
    "sample_count": {N},
    "total_word_count": {N},
    "tone": { ... },
    "sentence_structure": { ... },
    "vocabulary": { ... },
    "voice": { ... },
    "rhetoric": { ... },
    "flow": { ... },
    "signature_elements": { ... },
    "generation_guidance": {
      "do": ["{guideline_1}", "{guideline_2}"],
      "avoid": ["{anti-pattern_1}", "{anti-pattern_2}"],
      "example_sentences": ["{representative_sentence_1}", "{representative_sentence_2}"]
    }
  }
  ```
- **Validate:** Run `cat profile/voice_profile.json | tools/validate-json.sh`
- **If validation fails:** Fix and retry.
- **Inform:** "I've saved your voice profile to `profile/voice_profile.json`. I'll use it for this and future cover letters."

### Step 5: Load Job & Resume Context

**Instruction:**
- Load the parsed job posting, the tailored resume (if it exists), the full resume corpus, and the user's name from constraints.
- Identify the top 3-5 key requirements from the job and the main accomplishments featured in the tailored resume.

### Step 6: Generate Cover Letter Draft (Corpus-Enhanced)

**Instruction:**
- Your goal is to write a compelling narrative that sounds like the user, not a generic template.
- **Apply Voice Profile:** Use the `generation_guidance` section from `profile/voice_profile.json`:
  - Follow the "do" guidelines for style and phrasing
  - Avoid patterns listed in "avoid"
  - Match the tone, sentence structure, and vocabulary patterns
  - Incorporate signature phrases naturally where appropriate
- **Prioritize Narrative Fields:** When telling the story of a key accomplishment, **first** check the `corpus.json` for a `narrative_description` associated with that position (from the `linkedin-review` workflow). If it exists, use it as the primary source material.
- **If no narrative exists:** Use the tailored resume's accomplishments as a guide. Find those accomplishments in the corpus and use their `content`, `variations`, and any other related bullets to tell the *story* behind the achievement.
- **Voice Consistency Check:** Before presenting the draft, verify it matches the voice profile's tone and style characteristics.

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
