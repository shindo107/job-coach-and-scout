# Create Voice

## Summary

**Purpose:** Analyze writing samples and generate your personalized Voice Agent
**Agent:** Job Scout (Scout)
**Phase:** setup
**Reads:**
- `profile/writing_samples/*` — Your writing samples (cover letters, emails, blog posts)
- `profile/constraints.yaml` (optional) — For user's name
- `agents/voice-template.md` — Template for generating the Voice Agent
**Creates:**
- `profile/voice_profile.json` — Your analyzed writing voice characteristics
- `agents/voice.md` — Your personalized Voice Agent
**Updates:** None
**Prerequisites:** init completed (corpus exists)

---

**Trigger:** User says "create my voice profile", "analyze my writing style", or runs `/create-voice`

## Persona

**Load and adopt:** `agents/job-scout.md`

Read the persona file and embody Scout for this workflow. You're analyzing the user's writing patterns to create a faithful voice profile, approaching it like competitive intelligence but focused on their unique communication style.

## Context Required

Before starting, check for:
- `profile/writing_samples/` — Directory with writing samples (required)
- `profile/constraints.yaml` — For user's name (optional, can ask)
- `agents/voice-template.md` — Template file (required)

**If writing samples directory doesn't exist or is empty:**
```
I need writing samples to analyze your voice. Please add some samples to `profile/writing_samples/`.

Good samples include:
- Cover letters you've written
- Professional emails
- LinkedIn posts or articles
- Blog posts or documentation
- Any professional writing that sounds like "you"

The more varied the samples, the better I can capture your authentic voice.
Aim for 3-5 samples totaling at least 1,000 words.

Let me know when you've added them.
```

## Steps

### Step 1: Check for Existing Voice Profile

**1a. Check current state:**
- Check if `agents/voice.md` already exists
- Check if `profile/voice_profile.json` already exists

**If Voice Agent exists:**
```
I found an existing Voice Agent at `agents/voice.md`.

Would you like to:
1. Re-analyze — Start fresh with current writing samples
2. View current — Show your current voice profile
3. Cancel — Keep the existing profile

Which option? [1/2/3]
```
- If re-analyze: Continue to Step 2
- If view current: Show summary of voice_profile.json and ask if they want to continue
- If cancel: End workflow

**If no Voice Agent but profile exists:**
```
I found a voice profile at `profile/voice_profile.json` but no Voice Agent.
I'll regenerate your Voice Agent from this profile.

Or would you prefer to re-analyze your writing samples? [Generate/Re-analyze]
```
- If generate: Skip to Step 6 (Generate Voice Agent)
- If re-analyze: Continue to Step 2

**If neither exists:** Continue to Step 2

### Step 2: Gather User's Name

**Check for name in constraints:**
- Look for user's name in `profile/constraints.yaml` under a `name` or `user.name` field
- If found, use it

**If not found:**
```
What name should I use for your Voice Agent?

This will appear in the agent file (e.g., "Alex — Voice Agent") and creates
psychological alignment when the agent writes as you.

Your name:
```
- Store the name for use in template generation

### Step 3: Analyze Writing Samples

**Instruction:** Read all files in `profile/writing_samples/` and perform comprehensive voice analysis.

**For each sample, analyze these dimensions:**

**Tone & Register:**
- Formality level: formal, professional, conversational, casual
- Confidence style: assertive, measured, humble, collaborative
- Energy: enthusiastic, calm, reserved, dynamic

**Sentence Structure:**
- Average sentence length tendency: short-punchy, medium, long-complex, varied
- Sentence variety: consistent, varied
- Preferred openings: direct statements, context-setting, questions

**Vocabulary Patterns:**
- Complexity: simple-clear, moderate, sophisticated
- Technical density: minimal, moderate, heavy
- Industry jargon usage: avoided, selective, frequent
- Distinctive words/phrases the user frequently uses
- Words they seem to avoid

**Voice & Perspective:**
- Person: first-person dominant, mixed, third-person
- Voice: active-dominant, mixed, passive-tolerant
- Self-reference style: "I achieved", "Led the team", "We delivered"

**Rhetorical Patterns:**
- Argument structure: direct-first, building, storytelling
- Evidence style: metrics-heavy, example-driven, principle-based
- Persuasion approach: logical, emotional, credibility-based

**Paragraph & Flow:**
- Paragraph length: short, medium, varied
- Transition style: explicit connectors, implicit flow, minimal
- Opening tendency: hook, context, direct statement
- Closing tendency: call-to-action, summary, forward-looking

**Signature Elements:**
- Extract 3-5 distinctive phrases or constructions
- Note consistent patterns in describing achievements
- Identify storytelling style

### Step 4: Present Analysis for Confirmation

**Instruction:** Present a summary of the analysis for user confirmation.

```
Here's what I've learned about your writing voice:

**Tone:** {formality}, {confidence}, {energy}
**Style:** {sentence_length} sentences, {complexity} vocabulary
**Voice:** {person} person, {active_passive} voice
**Rhetoric:** {argument_structure}, {evidence_style}

**Signature elements I noticed:**
- "{distinctive_phrase_1}"
- "{distinctive_phrase_2}"
- "{distinctive_phrase_3}"

**How you describe achievements:**
{achievement_pattern_summary}

**Your storytelling approach:**
{storytelling_style_summary}

Does this sound like you? [Yes / Adjust / Cancel]
```

**If user wants adjustments:**
- Ask for specific corrections (e.g., "I'm more formal than that", "I never use jargon")
- Update the analysis accordingly
- Re-present for confirmation

**If user cancels:**
- End workflow without saving

### Step 5: Save Voice Profile

**Instruction:** Generate and save the voice profile JSON.

**Generate:** Create `profile/voice_profile.json` with the analyzed characteristics:

```json
{
  "schema_version": "1.0",
  "created_at": "{ISO timestamp}",
  "samples_analyzed": ["{filename_1}", "{filename_2}"],
  "sample_count": {N},
  "total_word_count": {N},

  "tone": {
    "formality": "{formal|professional|conversational|casual}",
    "confidence": "{assertive|measured|humble|collaborative}",
    "energy": "{enthusiastic|calm|reserved|dynamic}",
    "notes": "{any nuances observed}"
  },

  "sentence_structure": {
    "length_tendency": "{short-punchy|medium|long-complex|varied}",
    "variety": "{consistent|varied}",
    "common_openings": ["{pattern_1}", "{pattern_2}"]
  },

  "vocabulary": {
    "complexity": "{simple-clear|moderate|sophisticated}",
    "technical_density": "{minimal|moderate|heavy}",
    "jargon_usage": "{avoided|selective|frequent}",
    "favorite_words": ["{word_1}", "{word_2}"],
    "avoided_words": ["{word_1}", "{word_2}"]
  },

  "voice": {
    "person": "{first-person|mixed|third-person}",
    "active_passive": "{active-dominant|mixed|passive-tolerant}",
    "self_reference_examples": ["{example_1}", "{example_2}"]
  },

  "rhetoric": {
    "argument_structure": "{direct-first|building|storytelling}",
    "evidence_style": "{metrics-heavy|example-driven|principle-based}",
    "persuasion_approach": "{logical|emotional|credibility-based}"
  },

  "flow": {
    "paragraph_length": "{short|medium|varied}",
    "transitions": "{explicit|implicit|minimal}",
    "opening_tendency": "{hook|context|direct}",
    "closing_tendency": "{call-to-action|summary|forward-looking}"
  },

  "signature_elements": {
    "distinctive_phrases": ["{phrase_1}", "{phrase_2}", "{phrase_3}"],
    "achievement_pattern": "{how they typically describe accomplishments}",
    "storytelling_style": "{brief description of narrative approach}"
  },

  "generation_guidance": {
    "do": ["{guideline_1}", "{guideline_2}", "{guideline_3}"],
    "avoid": ["{anti-pattern_1}", "{anti-pattern_2}"],
    "example_sentences": ["{representative_sentence_1}", "{representative_sentence_2}"]
  }
}
```

**Validate:** Run `cat profile/voice_profile.json | tools/validate-json.sh`
- If validation fails, fix and retry

### Step 6: Generate Voice Agent

**Instruction:** Use the template to generate the personalized Voice Agent.

1. Read `agents/voice-template.md`
2. Replace all placeholders with values from `voice_profile.json`:
   - `{name}` — User's name from Step 2
   - `{tone.formality}` — From voice_profile.json
   - `{tone.confidence}` — From voice_profile.json
   - `{tone.energy}` — From voice_profile.json
   - `{sentence_structure.length_tendency}` — From voice_profile.json
   - `{sentence_structure.variety}` — From voice_profile.json
   - `{vocabulary.complexity}` — From voice_profile.json
   - `{vocabulary.technical_density}` — From voice_profile.json
   - `{voice.person}` — From voice_profile.json
   - `{voice.active_passive}` — From voice_profile.json
   - `{rhetoric.argument_structure}` — From voice_profile.json
   - `{rhetoric.evidence_style}` — From voice_profile.json
   - `{rhetoric.persuasion_approach}` — From voice_profile.json
   - `{flow.paragraph_length}` — From voice_profile.json
   - `{flow.transitions}` — From voice_profile.json
   - `{flow.opening_tendency}` — From voice_profile.json
   - `{flow.closing_tendency}` — From voice_profile.json
   - `{generation_guidance.do}` — Format as numbered list
   - `{generation_guidance.avoid}` — Format as numbered list
   - `{generation_guidance.example_sentences}` — Format as quoted list
   - `{signature_elements.distinctive_phrases}` — Format as bulleted list
   - `{signature_elements.achievement_pattern}` — From voice_profile.json
   - `{signature_elements.storytelling_style}` — From voice_profile.json
   - `{timestamp}` — Current ISO timestamp

3. Save to `agents/voice.md`

### Step 7: Test Voice Match

**Instruction:** Generate a test sentence to verify the voice profile works.

```
Let me test your Voice Agent. Here's a sample sentence written in your voice:

"{generated_test_sentence}"

Does this sound like you? [Yes / No, adjust]
```

**If user says no:**
- Ask what felt off
- Adjust the voice profile accordingly
- Regenerate the Voice Agent
- Test again

### Step 8: Completion Summary

```
Voice Agent Created!

Your personalized Voice Agent is now ready at `agents/voice.md`.

Created files:
- `profile/voice_profile.json` — Your writing voice characteristics
- `agents/voice.md` — Your Voice Agent ({name}'s authentic style)

The Voice Agent will be used automatically by:
- `/cover-letter` — Writes cover letters in your voice
- `/linkedin-review` — Writes About section and experience narratives

Your voice profile was built from {sample_count} samples ({total_word_count} words).
You can update it anytime by adding samples to `profile/writing_samples/` and
running `/create-voice` again.
```

## Output

**Files created:**
- `profile/voice_profile.json` — Structured voice characteristics
- `agents/voice.md` — Personalized Voice Agent

## Recommend Next

After this workflow completes:

1. **If constraints don't exist:** Suggest scoping-interview
   "Now that your Voice Agent is ready, let's capture your job search preferences. Ready for the scoping interview?"

2. **If constraints exist:** Suggest cover-letter or linkedin-review
   "Your Voice Agent is ready to write! Would you like to:
   - Write a cover letter for a specific role
   - Optimize your LinkedIn profile
   - Something else?"
