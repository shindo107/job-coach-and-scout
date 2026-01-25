# Cover Letter

## Summary

**Purpose:** Generate a voice-matched cover letter through writing sample analysis and iterative refinement
**Agent:** Job Coach (Max)
**Reads:**
- `profile/resume.md` — Master resume (required)
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
- `profile/resume.md` — Master resume (required)
- Job posting or `research/openings/{company}-{role}.md` — Target job details (required)

If available, also load:
- `profile/writing_samples/*.md` — Writing samples for voice matching (recommended)
- `profile/constraints.yaml` — For name and preferences
- `applications/resumes/{company}-{role}.md` — Tailored resume for this role (preferred)

**If resume doesn't exist:**
```
I need your resume to reference achievements for your cover letter.
I couldn't find `profile/resume.md`.

Would you like to:
1. Run the init workflow to import your resume
2. Provide the path to your resume file
3. Paste your resume content
```

**If job posting doesn't exist:**
```
I need a job posting to write a targeted cover letter.
I couldn't find a posting in `research/openings/`.

Would you like to:
1. Run job-scan first to analyze a job posting
2. Paste the job posting content
3. Provide a URL to the job posting
```

## Pre-Flight Validation

**Before proceeding to Step 1, validate all required files are available:**

1. **Check resume exists:**
   - Try `profile/resume.md`
   - If missing → Display "resume doesn't exist" message above and STOP until resolved

2. **Check job posting available:**
   - Check if user provided company/role context
   - Try `research/openings/{company}-{role}.md`
   - If missing → Display "job posting doesn't exist" message above and STOP until resolved

3. **Store posting source for metadata:**
   - If loaded from `research/openings/` → Set `posting_source` = file path
   - If user will paste/URL → Set `posting_source` = "user-provided"

**Only proceed to Step 1 after resume and job posting availability are confirmed.**

## Steps

### Step 1: Check for Writing Samples

**1a. Check if writing samples exist:**

Look for files in `profile/writing_samples/`.

**If writing samples exist:**
```
Found {count} writing sample(s). I'll analyze these to match your voice.
```
Proceed to Step 2.

**If no writing samples exist:**
```
I don't see any writing samples in profile/writing_samples/.

Without samples, I can't match your personal voice, but I can still write a strong cover letter in a neutral professional tone.

Would you like to:
1. Continue with neutral professional tone
2. Add some writing samples first (old cover letters, LinkedIn posts, emails work great)
3. Describe your preferred writing style manually

Your choice?
```

**Handle user response:**

**If user chooses 1 (neutral tone):**
- Set voice_profile to "neutral_professional"
- Skip to Step 3

**If user chooses 2 (add samples):**
```
Great! Add your writing samples to `profile/writing_samples/`.
Good samples include: previous cover letters, LinkedIn posts, professional emails, or any writing that shows your natural voice.

Let me know when you've added them, and I'll analyze your style.
```
Wait for user, then proceed to Step 2.

**If user chooses 3 (describe style):**
```
Tell me about your preferred writing style:
- Formal or conversational?
- Short sentences or longer, flowing ones?
- Technical jargon or accessible language?
- Direct and confident or humble and measured?
```
Capture user's description and create a manual voice profile. Proceed to Step 3.

### Step 2: Analyze Writing Voice

**2a. Load all writing samples:**

Read all files from `profile/writing_samples/`.

**2b. Analyze samples for voice characteristics:**

For each sample, identify:

**Tone indicators:**
- Overall tone: professional, casual, enthusiastic, reserved, confident, humble
- Emotional warmth: warm and personable vs. strictly business
- Energy level: high-energy/dynamic vs. measured/calm

**Sentence patterns:**
- Average sentence length (short <15 words, medium 15-25, long >25)
- Variety in structure (simple, compound, complex)
- Use of fragments or incomplete sentences

**Vocabulary choices:**
- Technical jargon frequency
- Industry-specific terms
- Casual vs. formal word choices

**Personality signals:**
- First person usage ("I achieved" vs. "The project achieved")
- Enthusiasm markers (exclamation points, superlatives)
- Hedging language ("I believe", "perhaps", "might")
- Directness level
- **Humor usage:** Does user use wit, self-deprecation, or wordplay? Or strictly serious?

**Structural preferences:**
- Paragraph length
- Use of bullet points vs. prose
- Opening patterns (question, statement, story)

**2c. Extract specific patterns:**

Identify:
- Phrases and expressions the user tends to use
- Things the user AVOIDS (e.g., never uses "synergy", avoids clichés)
- Tone markers (confident, humble, enthusiastic, reserved)

**2d. Synthesize voice profile:**

Create a structured voice profile with:
- `tone`: e.g., "Direct and confident"
- `formality`: e.g., "Semi-formal"
- `sentence_style`: e.g., "Mix of short punchy and longer explanatory"
- `vocabulary`: e.g., "Technical when needed, accessible to non-experts"
- `personality`: e.g., "Warm but not effusive"
- `patterns_to_use`: List of observed patterns
- `patterns_to_avoid`: List of things user avoids

### Step 3: Present Voice Analysis for Confirmation

**3a. Display voice profile summary:**

```markdown
## Your Writing Voice Profile

Based on your samples, here's how you write:

**Tone:** {detected_tone}
**Formality:** {formality_level}
**Sentence style:** {sentence_description}
**Vocabulary:** {vocabulary_description}
**Personality:** {personality_description}

**Things you DO:**
- {pattern_1}
- {pattern_2}
- {pattern_3}

**Things you AVOID:**
- {avoid_1}
- {avoid_2}

Does this sound like you? (Confirm / Adjust)
```

**3b. Handle user response:**

**If user confirms:**
```
Great! I'll use this voice profile for your cover letter.
```
Store voice profile.

`[CHECKPOINT: Voice Analysis]` — Voice profile confirmed and stored. Safe to pause here.

Proceed to Step 4.

**If user wants to adjust:**
```
What would you like to adjust?
Examples:
- "More formal"
- "Less verbose"
- "More enthusiastic"
- "Avoid technical jargon"
```

Parse user feedback and update voice profile:

| Feedback | Adjustment |
|----------|------------|
| "More formal" | Increase formality, reduce casual markers |
| "Less verbose" | Shorter sentences, tighter prose |
| "More enthusiastic" | Add energy markers, confident language |
| "Less technical" | Reduce jargon, use accessible alternatives |

Show updated profile and confirm again:
```markdown
## Updated Voice Profile

**Tone:** {updated_tone}
**Formality:** {updated_formality}
...

Does this work? (Confirm / Adjust again)
```

Repeat until user confirms.

### Step 4: Load Job Context

**4a. Load job posting:**

Check for job posting in this order:
1. `research/openings/{company}-{role}.md` (parsed posting)
2. User-provided file path
3. User-provided URL (use WebFetch to retrieve)
4. User-provided text

**If WebFetch fails (URL option):**
```
I couldn't retrieve the job posting from that URL. This might be due to:
- The page requires login
- The site blocks automated access
- Network issues

Would you like to:
1. Paste the job posting content directly
2. Try a different URL
3. Save the posting to a file and provide the path
```

Extract from job posting:
- Company name and role title
- Top 3-5 key requirements
- Company mission/values (if mentioned)
- Team/reporting structure (if mentioned)
- Any unique aspects worth referencing

**4b. Load resume:**

Check for tailored resume first:
1. `applications/resumes/{company}-{role}.md` (preferred)
2. `profile/resume.md` (fallback)

If using master resume instead of tailored:
```
Note: Using your master resume. For best results, consider running fit-resume first to create a tailored version specifically for this role.
```

Extract from resume:
- Top 3-5 most relevant achievements for this role
- Quantified results to highlight
- Keywords that match job requirements

**4c. Load user name:**

Check `profile/constraints.yaml` for user's name.
If not found, ask:
```
What name should I use in the cover letter?
```

### Step 5: Generate Cover Letter Draft

**5a. Generate the cover letter:**

Using the confirmed voice profile, create a cover letter with:

**Opening Hook (1-2 sentences)**
- Reference why this company/role specifically interests you
- Be specific, not generic
- Match the user's voice

**Value Proposition (1 paragraph)**
- Select 2-3 achievements from resume that directly address top job requirements
- Quantify where possible
- Connect each achievement to a specific job need
- Use the user's voice patterns

**Company Knowledge (1-2 sentences)**
- Demonstrate research about the company
- Reference recent news, product, mission, or culture if discoverable
- Show genuine interest

**Closing (2-3 sentences)**
- Clear call to action
- Express enthusiasm appropriately (matching voice profile)
- Thank them

**5b. Ensure appropriate length:**

Target 3-4 paragraphs, approximately 300-400 words.

- **If longer than 450 words:** Tighten prose while maintaining voice. Remove redundancy, combine sentences.
- **If shorter than 250 words:** Expand value proposition with additional achievement detail, or add more company-specific context.

**5c. Store draft for iteration tracking:**

Initialize tracking variables (maintain these throughout the session):
- `iteration_count`: 1
- `changes_made`: [] (array of strings describing each change, e.g., ["Made tone more formal", "Shortened opening paragraph"])

`[CHECKPOINT: Draft Ready]` — Initial draft generated. Safe to pause here.

### Step 6: Present Draft for Feedback

**6a. Display the draft:**

```markdown
## Cover Letter Draft (Iteration {iteration_count})

---

{Generated cover letter content}

---

**Word count:** {count}
**Voice profile applied:** {tone}, {formality}
```

**6b. Ask for feedback:**

```
How does this look?

You can:
- **Approve** — If you're happy with it
- **Request changes** — Tell me what to adjust

Example feedback:
- "Too formal/casual"
- "Too long/short"
- "Emphasize different achievements"
- "Change the opening hook"
- "More enthusiasm"
- "Less corporate language"

What would you like?
```

### Step 7: Iterative Refinement Loop

**7a. Handle user response:**

**If user approves:**
Proceed to Step 8 (Save).

**If user requests changes:**

**7b. Parse feedback and regenerate:**

| Feedback | Action |
|----------|--------|
| "Too formal" | Relax language, shorter sentences, more personality |
| "Too casual" | Add professionalism, reduce contractions |
| "Too long" | Cut to 3 paragraphs, tighten prose |
| "Too short" | Add more detail, expand value proposition |
| "Emphasize leadership" | Swap achievement examples, lead with management wins |
| "Opening is weak" | Rewrite hook with company-specific angle |
| "Sounds generic" | Add more company research, specific role requirements |
| "More enthusiasm" | Add energy markers while maintaining voice |

**7c. Regenerate affected sections:**

Only regenerate sections that need changes, maintaining consistency with unchanged parts.

**7d. Update tracking:**

- Increment `iteration_count`
- Add change description to `changes_made`

**7e. Present updated draft:**

```markdown
## Cover Letter Draft (Iteration {iteration_count})

**Changes made:**
- {change_1}
- {change_2}

---

{Updated cover letter content}

---

**Word count:** {count}

How does this look now? (Approve / More changes)
```

**7f. Continue loop:**

`[CHECKPOINT: Iteration]` — Refinement round complete. Safe to pause here.

Return to Step 6b until user approves.

### Step 8: Save Cover Letter with Metadata

**8a. Create output directory if needed:**

Ensure `applications/cover_letters/` exists.

**8b. Determine linked resume path:**

Use the resume that was loaded:
- `applications/resumes/{company}-{role}.md` if tailored exists
- `profile/resume.md` otherwise

**8c. Save to output location:**

Save to: `applications/cover_letters/{company}-{role}.md`

```markdown
---
company: "{company}"
role: "{role}"
linked_resume: "{resume_path}"
source_posting: "{posting_source}"  # Use value from Pre-Flight Validation
date_generated: "{YYYY-MM-DD}"
voice_profile:
  tone: "{tone}"
  formality: "{formality}"
  sentence_style: "{sentence_style}"
  vocabulary: "{vocabulary}"
  personality: "{personality}"
  patterns_used:
    - "{pattern_1}"
    - "{pattern_2}"
  patterns_avoided:
    - "{avoid_1}"
  adjustments_made: "{any adjustments from Step 3}"
iterations: {count}
changes_log:
  - "{change_1}"
  - "{change_2}"
---

{Final cover letter content}
```

**Note:** `source_posting` should reflect how the posting was obtained:
- If from file: `"research/openings/{company}-{role}.md"`
- If user pasted: `"user-provided (pasted)"`
- If from URL: `"user-provided (URL: {url})"`

**8d. Confirm save:**

```
Saved: applications/cover_letters/{company}-{role}.md
```

### Step 9: Workflow Completion

**9a. Display summary:**

```markdown
## Cover Letter Complete!

**{Company} - {Role}**

| Metric | Value |
|--------|-------|
| Voice Profile | {tone}, {formality} |
| Iterations | {count} |
| Word Count | {words} |

**File saved:** `applications/cover_letters/{company}-{role}.md`
**Linked resume:** `{resume_path}`
```

**9b. Provide guidance:**

```
Your cover letter is ready to submit alongside your tailored resume.

**Files for this application:**
- Resume: `{resume_path}`
- Cover Letter: `applications/cover_letters/{company}-{role}.md`
```

**9c. Suggest next steps if applicable:**

**If no tailored resume exists for this role:**
```
Tip: For future applications, consider running fit-resume first to create a tailored resume. The cover letter can then reference your strongest, most relevant achievements.
```

**If all set:**
```
Good luck with your application to {Company}!

When you're ready for your next application, just let me know.
```

## Output

Save the cover letter to: `applications/cover_letters/{company}-{role}.md`

**Files created:**
- `applications/cover_letters/{company}-{role}.md` — Voice-matched cover letter with metadata

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** None (application complete) OR another posting
   **Rationale:** "Application complete! Ready to apply or tackle another posting?"
   **Context to pass:** Application files ready: `applications/resumes/{company}-{role}.md`, `applications/cover_letters/{company}-{role}.md`

2. Present the suggestion conversationally:
   "Your application for {Company} - {Role} is complete!

   **Application files ready:**
   - Resume: `applications/resumes/{company}-{role}.md`
   - Cover Letter: `applications/cover_letters/{company}-{role}.md`

   Good luck with your application! Would you like to:
   - **Tackle another posting** — Scan a new job and build another application
   - **Done for now** — End here

   [Another posting/Done/Something else]"

3. If user wants another posting: Load `workflows/job-scan/workflow.md` and execute
4. If user is done: End gracefully with well-wishes
5. If user requests different workflow: Honor their request
