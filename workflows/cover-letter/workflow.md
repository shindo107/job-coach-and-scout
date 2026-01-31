# Cover Letter

## Summary

**Purpose:** Generate a voice-matched cover letter using your personalized Voice Agent
**Agent:** Voice Agent (primary), Max (optional review)
**Phase:** apply
**Reads:**
- `agents/voice.md` — Your personalized Voice Agent (preferred)
- `profile/voice_profile.json` — Your writing voice characteristics (fallback)
- `profile/writing_samples/*` — For voice analysis if no profile exists (fallback)
- `profile/corpus.json` — Resume Corpus (required)
- `research/openings/{company}-{role}.md` — Target job details (required)
- `profile/constraints.yaml` — For user preferences
- `applications/resumes/{company}-{role}.md` (optional) — Tailored resume (preferred)
**Creates:**
- `applications/cover_letters/{company}-{role}.md` — Voice-matched cover letter
**Updates:**
- `agents/voice.md` (conditional) — Generated if voice_profile.json exists but voice.md doesn't
- `profile/voice_profile.json` (conditional) — Created if only writing samples exist
**Prerequisites:** job-scan completed; tailor-resume recommended

---

> **VOICE-MATCHED GENERATION**: Uses your personalized Voice Agent to generate a cover letter that sounds authentically like you wrote it. Max reviews from a hiring manager's perspective (optional).

**Trigger:** User says "help me write a cover letter for [company]" or after `tailor-resume`.

## Persona

**Primary:** Load and adopt `agents/voice.md` (your personalized Voice Agent)
**Review:** `agents/job-coach.md` (Max, for optional hiring manager review)

## Context Required
- `agents/voice.md` (preferred) or `profile/voice_profile.json` (fallback) or `profile/writing_samples/` (last resort)
- `profile/corpus.json`
- `research/openings/{company}-{role}.md`
- `profile/constraints.yaml`

---

## Steps

### Step 1: Load Voice Agent

**Fallback chain for voice matching:**

**1a. Check for Voice Agent (preferred):**
- Check if `agents/voice.md` exists
- **If it exists:** Load and adopt the Voice Agent persona
  ```
  Loading your Voice Agent...

  I'll write this cover letter in your authentic voice:
  - Tone: {tone summary from voice.md}
  - Style: {style summary}

  Ready to draft your cover letter.
  ```
  - Skip to Step 5

**1b. Check for Voice Profile (fallback):**
- If no `agents/voice.md`, check if `profile/voice_profile.json` exists
- **If it exists:**
  ```
  I found your voice profile but no Voice Agent. Let me generate one...
  ```
  - Read `agents/voice-template.md`
  - Generate `agents/voice.md` from template + voice_profile.json
  - Load the generated Voice Agent
  - Skip to Step 5

**1c. Check for Writing Samples (last resort):**
- If no voice profile, check for files in `profile/writing_samples/`
- **If samples exist:**
  ```
  I found writing samples but no voice profile. I'll analyze them now to create your Voice Agent.
  ```
  - Proceed to Step 2 (Analyze Writing Voice)

**1d. No Voice Data Available:**
- If no samples exist:
  ```
  I don't have any voice data to match your writing style.

  Options:
  1. Add samples — Put writing samples in `profile/writing_samples/` and I'll analyze them
  2. Proceed without — I'll write a professional cover letter without voice matching
  3. Cancel — Stop and set up voice matching first via /create-voice

  Which option? [1/2/3]
  ```
  - If add samples: Wait for confirmation, then proceed to Step 2
  - If proceed without: Skip to Step 5 (no voice matching)
  - If cancel: End workflow

### Step 2: Analyze Writing Voice (Fallback Only)

**Skip this step if:** Voice Agent was loaded in Step 1a or 1b.

**Instruction:** This step runs the full voice analysis when no profile exists.

- Read all files in `profile/writing_samples/` and analyze for:
  - Tone & Register (formality, confidence, energy)
  - Sentence Structure (length, variety, openings)
  - Vocabulary Patterns (complexity, technical density, distinctive phrases)
  - Voice & Perspective (person, active/passive, self-reference style)
  - Rhetorical Patterns (argument structure, evidence style)
  - Signature Elements (distinctive phrases, achievement patterns)

### Step 3: Present Voice Analysis for Confirmation (Fallback Only)

**Skip this step if:** Voice Agent was loaded in Step 1a or 1b.

**Instruction:** Present a summary for user confirmation.
```
Here's what I've learned about your writing voice:

Tone: {formality}, {confidence}, {energy}
Style: {sentence_length} sentences, {complexity} vocabulary
Voice: {person} person, {active_passive} voice

Signature elements I noticed:
- "{distinctive_phrase_1}"
- "{distinctive_phrase_2}"

Does this sound like you? [Yes / Adjust / Skip voice matching]
```

### Step 4: Generate Voice Agent (Fallback Only)

**Skip this step if:** Voice Agent was loaded in Step 1a or 1b.

**Instruction:** Save the voice profile and generate the Voice Agent.

1. Save `profile/voice_profile.json` with analyzed characteristics
2. Validate: `cat profile/voice_profile.json | tools/validate-json.sh`
3. Read `agents/voice-template.md`
4. Generate `agents/voice.md` from template + voice_profile.json
5. Load the generated Voice Agent
6. Inform user: "I've created your Voice Agent. It will be used for this and future cover letters."

### Step 5: Load Job & Resume Context

**Instruction:**
- Load the parsed job posting, the tailored resume (if it exists), the full resume corpus, and the user's name from constraints.
- Identify the top 3-5 key requirements from the job and the main accomplishments featured in the tailored resume.

### Step 6: Generate Cover Letter Draft (As Voice Agent)

**Instruction:**
- **You ARE the Voice Agent now.** Write as {name}, not as an assistant.
- Embody `agents/voice.md` fully. The cover letter should be indistinguishable from the user's own writing.

**Apply Voice Agent characteristics:**
- Follow the "do" guidelines from generation_guidance
- Avoid patterns listed in "avoid"
- Match the tone, sentence structure, and vocabulary patterns
- Incorporate signature phrases naturally where appropriate
- Use the user's self-reference style (from voice.self_reference_examples)

**Prioritize Narrative Fields:**
- When telling the story of a key accomplishment, **first** check `corpus.json` for a `narrative_description` associated with that position (from linkedin-review)
- If it exists, use it as the primary source material
- If no narrative exists, use the tailored resume's accomplishments as a guide

**Voice Consistency Check:**
- Before presenting the draft, verify it matches the Voice Agent's characteristics
- Read the draft as if you were the user: "Would I have written this?"

### Step 7: Present Draft for Feedback

**Instruction:**
- Present the draft to the user. Ask for specific feedback: "How does this sound to you? Does it capture your voice? Is there anything you'd change?"

### Step 7a: Max Review (Default, Opt-Out)

**Instruction:** By default, Max reviews the cover letter from a hiring manager's perspective.

```
Would you like Max to review this from a hiring manager's perspective?

Max will critique the positioning, not rewrite the letter. Your voice stays intact.
[Yes (recommended) / Skip Max review]
```

**If user wants Max review:**
1. Switch persona to `agents/job-coach.md` (Max)
2. Review the cover letter as a skeptical hiring manager:
   - Does it answer "why this company?"
   - Does it answer "why this candidate?"
   - Are claims specific and believable?
   - Is there anything that would make you pause?
3. Present critique (not rewrites):
   ```
   **Max's Review:**

   Strengths:
   - {what works well}

   Concerns:
   - {specific issue 1}: {why it's a problem}
   - {specific issue 2}: {why it's a problem}

   Suggestions:
   - {actionable feedback without rewriting}
   ```
4. Switch back to Voice Agent persona
5. Incorporate feedback while preserving user's voice
6. Present revised draft

**If user skips Max review:** Proceed directly to Step 8.

### Step 8: Iterative Refinement Loop

**Instruction:**
- Based on user feedback, refine the draft while staying in Voice Agent persona
- This could involve changing emphasis, swapping accomplishments, or rephrasing sentences
- Continue to iterate until the user is satisfied
- Always maintain the user's authentic voice

### Step 9: Save Cover Letter with Metadata

**Instruction:**
- Save the final, approved cover letter to `applications/cover_letters/{company}-{role}.md`.
- Include metadata in the file, including the date, the source job posting, and the tailored resume it's linked to.

### Step 10: Workflow Completion

**Instruction:**
- Inform the user that the cover letter has been saved.
- Suggest next steps, such as preparing for an interview or finding other jobs to apply for.
