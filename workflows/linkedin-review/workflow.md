# LinkedIn Profile Review

## Summary

**Purpose:** Craft a compelling LinkedIn profile through collaborative revision, enriching your core Resume Corpus.
**Agent:** Voice Agent (About, narratives), Max (headline, skills, positioning review)
**Phase:** standalone
**Reads:**
- `profile/corpus.json` — Your structured Resume Corpus (required)
- `profile/constraints.yaml` (optional) — For target roles and feedback style
- `profile/linkedin.md` (optional) — Existing LinkedIn profile if available
- `agents/voice.md` (optional) — Your Voice Agent for About/narratives
- `profile/voice_profile.json` (optional) — Fallback for voice matching
**Creates:**
- `profile/linkedin.md` — Your optimized LinkedIn profile content
**Updates:**
- `profile/corpus.json` — Updated with new narrative content (headline, about, experience)
**Prerequisites:** init completed (corpus created)

---

**Trigger:** User says "review my linkedin", "help with my linkedin profile", or "optimize my linkedin"

## Persona

**Primary agents:**
- `agents/job-coach.md` (Max) — Headline, skills selection, positioning review
- `agents/voice.md` (Voice Agent) — About section, experience narratives

**Agent responsibilities:**
| Section | Agent | Rationale |
|---------|-------|-----------|
| Headline | Max | Positioning and keyword strategy |
| About | Voice Agent | First-person writing in user's authentic voice |
| Experience Narratives | Voice Agent | Storytelling in user's authentic voice |
| Skills Selection | Max | Strategic keyword optimization |
| Industry Selection | Max | Positioning strategy |
| Final Review | Max | Hiring manager perspective |

Read both persona files. Start with Max for the introduction and headline work, then switch to the Voice Agent for About and experience narratives.

## Context Required

Before starting, load these files:
- `profile/corpus.json` — Your Resume Corpus (required)
- `profile/constraints.yaml` — For target roles and preferences (optional)
- `agents/voice.md` — Your Voice Agent (for About and narratives)
- `profile/voice_profile.json` — Fallback if Voice Agent doesn't exist

If available, also load:
- `profile/linkedin.md` — Existing LinkedIn profile to review, or the `profile.headline` and `profile.about` fields from the corpus itself.

**If corpus doesn't exist:**
```
I need your Resume Corpus to build your LinkedIn profile. I couldn't find `profile/corpus.json`.

Would you like to run the init workflow to create it?
```

**If no Voice Agent or voice profile:**
```
I don't have a Voice Agent to write your About section and experience narratives.

Options:
1. Create Voice Agent first — Run /create-voice to analyze your writing samples
2. Proceed without — Max will write everything (may not match your personal voice)

Which option? [1/2]
```
- If option 1: End workflow, suggest /create-voice
- If option 2: Continue with Max only (note this in output)

**If no existing profile:**
```
I don't see an existing LinkedIn profile at `profile/linkedin.md`. That's fine — we'll build one from scratch using your Resume Corpus.

Do you want to:
1. Start fresh (I'll draft everything based on your corpus)
2. Paste your current LinkedIn content so I can review it
```

## LinkedIn Character Limits

These limits are enforced by LinkedIn — exceeding them will truncate your content:
- **Headline:** 220 characters (aim for under 120 for mobile readability)
- **About:** 2,600 characters
- **Position Title:** 100 characters
- **Position Description:** 2,000 characters per role

## Steps

### Step 1: Load Context and Adopt Persona

1.  **- [ ] Load files:**
    -   Load `profile/corpus.json` and optionally `profile/constraints.yaml` and `profile/linkedin.md`.
2.  **- [ ] Extract target positioning:**
    -   From constraints, identify target roles, industries, and keywords.
    -   From corpus, identify strongest themes, quantified achievements, and differentiators.
3.  **- [ ] Introduce the review:**
    -   **Instruction:** Introduce the purpose of the review. Explain that a strong LinkedIn profile is a 24/7 recruiter pitch and that you'll be reviewing it section-by-section to ensure it stands out. Start with the headline.

### Step 2: Headline Review

The headline appears everywhere. It must instantly communicate value.

1.  **- [ ] Analyze current headline (if exists):**
    -   **Instruction:** Critique the current headline from the perspective of a recruiter. Evaluate if it includes the target role, quantified credibility, and key differentiators.
2.  **- [ ] Draft headline options:**
    -   **Instruction:** Based on the corpus and constraints, draft 3 distinct headline options that are keyword-rich, credible, and differentiate the user from generic titles. Present them with a brief explanation of the strategic angle for each.
3.  **- [ ] Get user input and refine:**
    -   **Instruction:** Ask the user which direction resonates most or what they'd like to change. Iterate on the drafts based on their feedback.
4.  **- [ ] Finalize headline:**
    -   **Instruction:** Once the user agrees on a headline, confirm the character count and state the final version. Keep this finalized headline in memory for the corpus update.

### Step 3: About Section Review (Voice Agent)

The About section is the elevator pitch. It should hook the reader, establish credibility, and be keyword-rich — all in the user's authentic voice.

**Switch to Voice Agent persona:** Load and adopt `agents/voice.md` for this step.

1.  **- [ ] Analyze current About (if exists):**
    -   **Instruction:** Review the current About section. Evaluate its hook, career narrative, use of quantified achievements, and whether it sounds like the user.
2.  **- [ ] Draft About section as Voice Agent:**
    -   **Instruction:** You ARE the Voice Agent now. Write the About section as the user would write it.
    -   Apply voice characteristics from `agents/voice.md`:
      - Match tone (formality, confidence, energy)
      - Use signature phrases naturally
      - Follow the user's typical sentence structure
      - Apply their storytelling approach
    -   Content should: open with a strong hook, tell a coherent career story with quantified achievements, include key skills/keywords, and stay within 2,600 characters.
3.  **- [ ] Interactive refinement:**
    -   **Instruction:** Present the draft and ask: "Does this sound like you? What would you change?"
    -   Be prepared to adjust while staying true to the Voice Agent characteristics.
    -   Iterate until the user confirms it sounds authentically like them.
4.  **- [ ] Max positioning review (optional):**
    -   **Instruction:** Ask if user wants Max to review positioning:
    ```
    Would you like Max to review the positioning from a recruiter's perspective?
    (Your voice stays intact — Max will critique strategy, not rewrite.) [Yes/No]
    ```
    -   If yes: Switch to Max, provide positioning feedback, switch back to Voice Agent for revisions.
5.  **- [ ] Finalize About:**
    -   **Instruction:** Confirm the character count and state that the section is finalized. Keep this final version in memory for the corpus update.

### Step 4: Experience Sections Review (Voice Agent)

LinkedIn experience sections are for narrative storytelling, not just resume bullets. These narratives should sound like the user telling their own career story.

**Continue as Voice Agent:** Stay in `agents/voice.md` persona for this step.

1.  **- [ ] Draft narrative descriptions for each position:**
    -   **Instruction:** You ARE the Voice Agent. For each relevant position in the corpus, draft a 2-4 paragraph narrative description in the user's authentic voice.
    -   Apply `signature_elements.achievement_pattern` from the voice profile
    -   Use the user's storytelling style
    -   Match their sentence structure and vocabulary patterns
    -   This should tell the story of the role, not just list bullets.
2.  **- [ ] Review each position with the user:**
    -   **Instruction:** Present the drafted narrative for each role. Ask: "Does this capture your story at {company}? Does it sound like you?"
    -   Probe for missing details or achievements, especially for underdeveloped roles.
    -   **CRITICAL:** Only add details the user confirms. Never fabricate.
3.  **- [ ] Finalize each position's narrative:**
    -   **Instruction:** Once the user approves the narrative, confirm its character count. Keep the finalized narrative in memory, mapping it to the corresponding `position_id` from the corpus.

### Step 5: Skills Selection (Max)

LinkedIn Top Skills are critical for search rankings.

**Switch to Max persona:** Load and adopt `agents/job-coach.md` for this step.

1.  **- [ ] Recommend Top 5 Skills:**
    -   **Instruction:** Analyze the skills from the corpus and cross-reference them with target role requirements. Recommend the 5 most impactful skills for search visibility, explaining your reasoning for each.
2.  **- [ ] Finalize Top 5:**
    -   **Instruction:** Ask the user to confirm or suggest alternatives. Finalize the list based on their feedback.

### Step 6: Industry Selection (Max)

The Industry field impacts discovery.

**Continue as Max:** Stay in `agents/job-coach.md` persona for this step.

1.  **- [ ] Recommend Industry:**
    -   **Instruction:** Based on the user's target roles, recommend an industry from LinkedIn's official taxonomy. Explain that it should align with where they want to *go*, not necessarily where they've *been*.
2.  **- [ ] Finalize Industry:**
    -   **Instruction:** Wait for user confirmation.

### Step 7: Confirm and Update Resume Corpus

This is the most critical step: saving the new narrative assets back to the central knowledge base.

1.  **- [ ] Confirm New Entries:**
    -   **Instruction:** Before saving, explicitly summarize what will be saved back to the corpus.
    -   **Example Dialogue:** "Before we finish, let's confirm what I'm saving to your Resume Corpus:
        -   **New Headline:** '{finalized headline}'
        -   **New About Section:** '{summary of the about section}'
        -   **Narrative for {Company Name}:** '{summary of the narrative description}'
        -   ... (repeat for each updated position)
      Is everything here accurate and ready to save?"
    -   **CRITICAL:** Wait for explicit user confirmation. Do not proceed if the user identifies inaccuracies.

2.  **- [ ] Construct New Corpus:**
    -   **Instruction:** Load the original `profile/corpus.json`.
    -   Create or update a top-level `profile` object to store the `headline` and `about` section.
    -   For each position that was updated, add or update the `narrative_description` field with the finalized text.
    -   Update the `schema_version` to "1.1".
    -   Update the `last_updated` timestamp.

3.  **- [ ] Save to Temporary File and Validate:**
    -   **Instruction:** Save the complete new JSON structure to `profile/corpus.json.tmp`.
    -   **Instruction:** Run the validator: `cat profile/corpus.json.tmp | tools/validate-json.sh`.
    -   **If validation fails:** Report the error and abort the save to prevent corruption. "I've encountered a formatting issue while trying to save your new LinkedIn content to the corpus. To prevent corruption, I've aborted the save. Your tailored `linkedin.md` file will still be saved." Then proceed to Step 8.
    -   **If validation succeeds:** Proceed to the next step.

4.  **- [ ] Perform Atomic Write:**
    -   **Instruction:** Rename `profile/corpus.json` to `profile/corpus.json.bak`.
    -   **Instruction:** Rename `profile/corpus.json.tmp` to `profile/corpus.json`.
    -   **Instruction:** Report success: "Your Resume Corpus has been successfully updated with your new LinkedIn narrative content."

### Step 8: Compile and Save LinkedIn Profile Markdown

1.  **- [ ] Compile and Save:**
    -   **Instruction:** Assemble all confirmed sections (headline, about, experience narratives, etc.) into the Markdown format defined below.
    -   **Instruction:** Save to `profile/linkedin.md`.
    -   Report success: "For your convenience, I've also saved a human-readable version of your profile to `profile/linkedin.md`."

### Step 9: Completion Summary

**Summary:**
```
## LinkedIn Profile and Corpus Updated!

Your profile is now optimized, and more importantly, your core Resume Corpus has been enriched with valuable narrative content.

Key improvements:
- Headline: Now targets '{keywords_in_headline}'
- About Section: Tells a compelling career story.
- Experience: Narrative descriptions added for {count} positions.
- Corpus Updated: Your new headline, about section, and experience narratives are now saved in `profile/corpus.json` for future use.
```

**Recommend Next:**
- **Instruction:** Based on the new keywords and positioning identified during the review (e.g., a new focus on a specific technology or industry), propose a relevant next step.
- **Example (if 'Cybersecurity' became a key theme):** "We've really strengthened your positioning around 'Cybersecurity'. Would you like me to use this new focus to run a `company-discovery` search for top cybersecurity firms, or would you prefer to `tailor-resume` for a specific role?"

## Output Format

The primary output is the updated `profile/corpus.json`. A secondary, human-readable file is saved to `profile/linkedin.md`.

Use this exact format for `profile/linkedin.md`:
```markdown
# LinkedIn Profile

**Last updated:** {YYYY-MM-DD}
**Source:** `profile/corpus.json`

---

## Headline

```
{headline text}
```

---

## Industry

{Industry name from LinkedIn taxonomy}

---

## About

```
{About section text}
```

---

## Profile URL

{URL if known, otherwise "https://www.linkedin.com/in/YOUR-URL/"}

---

## Top 5 Skills

1. {Skill 1}
2. {Skill 2}
3. {Skill 3}
4. {Skill 4}
5. {Skill 5}

---

## Experience

### {Company Name}
**{Title}** | {Start Month Year} – {End Month Year or "Present"}

{Narrative description paragraph 1}

{Narrative description paragraph 2}

{Narrative description paragraph 3 if needed}

**Skills:** {Skill 1}, {Skill 2}, {Skill 3}, {Skill 4}, {Skill 5}, {Skill 6}

---

{Repeat for each position}

## Notes

- Headline: {count} characters (max 220)
- About: ~{count} characters (max 2,600)
- Industry selected from LinkedIn's official taxonomy
```

## Recommend Next

After completing this workflow, suggest an intelligent next step like **company-discovery** or **tailor-resume**, using the new context from the review to frame the recommendation.
