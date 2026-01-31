# Scoping Interview

## Summary

**Purpose:** Capture your job search preferences through a dynamic, conversational interview that enriches your profile.
**Agent:** Job Coach (Max) & Job Scout
**Agent Lead:** Max
**Phase:** setup
**Reads:**
- `profile/corpus.json` — Structured Resume Corpus for context (recommended)
**Creates:**
- `profile/constraints.yaml` — Your job search constraints and preferences
**Updates:**
- `profile/corpus.json` (conditional) — If new persistent info like certifications is discovered
**Prerequisites:** init completed (corpus created)

---

**Trigger:** User asks "help me set up my constraints", "run the scoping interview", or after completing the init workflow

## Persona

**Load and adopt:** `agents/job-coach.md` AND `agents/job-scout.md`

**Role assignment:**
- **Max** leads Steps 1-6: Introduction, archetype definition, location, employment, compensation, and role targeting
- **Scout** leads Step 7: Industry & company preferences (Scout's domain expertise)
- **Max** leads Steps 8-12: Special factors, summary generation, corpus updates, and completion

Use Max's direct communication style for most of the interview. Transition to Scout's analytical approach when discussing industries and companies. The goal is to create a robust "rulebook" for the job search.

## Context Required

Before starting, load these files:
- `profile/corpus.json` — Resume Corpus for context (recommended but not required)

**If corpus doesn't exist:**
```
I'd like to review your resume corpus to understand your background better, but I couldn't find `profile/corpus.json`.

Would you like to:
1. Continue without resume context (I'll ask more background questions)
2. Run the init workflow first to create your resume corpus
```

## Steps

### Step 1: Introduction & Purpose

**Instruction:**
- Embodying Max, introduce the purpose of the scoping interview: to create the `constraints.yaml` file, which acts as the rulebook for all subsequent agent activity.
- Explain that specific, honest answers now will save time later by avoiding mismatched opportunities.
- Inform the user that you will be asking a series of questions about their preferences, and that you have loaded their `corpus.json` for context.

### Step 2: Analyze Corpus and Define Archetype

**Instruction:**
- Before the interview begins, perform a high-level analysis of the `profile/corpus.json`.
- Synthesize the user's career trajectory, key skills, and experience level into a professional summary or "archetype".
- **Example Archetype:** "A 10-year senior software engineer transitioning into engineering management, with a deep focus on fintech and distributed systems."
- Present this archetype to the user for confirmation: "Based on your corpus, I'm summarizing your professional brand as: '{archetype}'. Does that sound right to you as a starting point?"
- Keep this confirmed archetype in memory for the final YAML file.

### Step 3: Location & Work Arrangement

**Instruction:**
- Ask the user about their preferences for remote work, current location, and relocation willingness.
- Probe for specifics. If they say "flexible," ask them to define what that means to them. If they are willing to relocate, ask for specific target cities or regions, and any dealbreakers.
- **Capture:** `remote_preference`, `hybrid_days_per_week` (if applicable), `current_location`, `willing_to_relocate`, `acceptable_locations`, `location_dealbreakers`.

### Step 4: Employment Type & Availability

**Instruction:**
- Inquire about their desired employment type (full-time, contract, etc.), start date availability, and schedule preferences (e.g., standard 9-to-5 vs. async-friendly).
- **Capture:** `employment_type`, `availability`, `notice_period_weeks` (if applicable), `available_date` (if applicable), `schedule_preference`.

### Step 5: Compensation Expectations

**Instruction:**
- Remind the user that this information is stored locally and is for filtering purposes only.
- Ask for their **minimum walk-away base salary** and their **target base salary**. Insist on specific numbers.
- Inquire about the importance of equity and any other dealbreaker compensation factors (e.g., 401k match, specific benefits).
- **Capture:** `minimum_base`, `target_base`, `equity_preference`, `other_requirements`.

### Step 6: Role Targeting (Corpus-Aware)

**Instruction:**
- **This step must be corpus-aware.**
- **Propose Titles:** Analyze the `positions` in `corpus.json`. Based on the career progression, suggest 3-5 logical `target_titles` for their next role. Ask if these suggestions are on the right track or what they would change.
- Inquire about titles to avoid (e.g., 'Junior').
- Discuss seniority level, noting any mismatch between their resume and their target.
- Ask about their IC vs. Management preference, pushing for a primary choice if they say "either".
- **Capture:** `target_titles`, `avoid_titles`, `seniority`, `management_preference`.

### Step 7: Industry & Company Preferences (Scout Leads)

**Instruction:**
- **Transition to Scout:** "I'm going to hand this over to Scout for a moment — industry and company targeting is their specialty."
- Ask about target industries, dealbreaker industries, and preferences for company size and stage.
- Use Scout's analytical approach: present data-driven reasoning about industry trends if relevant to the user's skills.
- Inquire if they have a "dream list" of target companies or a "blocklist" of companies to avoid.
- **Capture:** `target_industries`, `avoid_industries`, `company_size`, `company_stage`, `target_companies`, `avoid_companies`.
- **Transition back to Max:** After capturing preferences, hand back to Max for the remaining steps.

### Step 8: Special Factors (Corpus-Aware)

**Instruction:**
- **This step must be corpus-aware.**
- **Confirm Certifications:** Scan the `corpus.json` for existing skills or certifications. State what you've found: "Your corpus already lists certifications like {list from corpus}. Are there any new ones you've earned, or any others I should know about?"
- Inquire about security clearance and work authorization status.
- Ask about any other hard requirements or dealbreakers not yet discussed.
- **Capture:** `clearance`, `clearance_level`, `work_authorization`, `certifications`, `willing_to_obtain`, `other_requirements`.
- **Note any new certifications or skills mentioned by the user for the corpus update step.**

### Step 9: Summary & Constraints Generation

**Instruction:**
- Based on all captured information, including the `archetype` from Step 2, generate the content for `profile/constraints.yaml`.
- Present the full YAML content to the user for a final review.
- Ask for confirmation: "Does this look accurate? Any changes before I save it?"
- If changes are requested, update the content and re-display.
- Once confirmed, save the content to `profile/constraints.yaml`.
- Confirm the save was successful.

### Step 10: Confirm and Update Resume Corpus (If Needed)

**Instruction:**
- This is a conditional step. Analyze the interview conversation. Did the user reveal any new, *permanent* information that should be in their corpus (e.g., a new certification, a key skill they had forgotten)?
- **If no new info was found, skip this step.**
- **If new info was found:**
    1.  **Confirm New Entries:** Summarize the new facts. "During our conversation, you mentioned you recently earned your {PMP Certification}. This is a valuable fact not in your corpus. Can I add it for you so we don't forget it?"
    2.  **CRITICAL:** Wait for explicit user confirmation before proceeding.
    3.  **Construct New Corpus:** If confirmed, load `profile/corpus.json`, add the new information to the appropriate array (e.g., `skills`), and update the `last_updated` timestamp.
    4.  **Save & Validate:** Save the updated object to `profile/corpus.json.tmp` and validate it with `cat profile/corpus.json.tmp | tools/validate-json.sh`.
    5.  **Atomic Write:** If valid, perform the safe write (`.bak` and rename). Report success to the user: "I've updated your Resume Corpus with the new information." If validation fails, report the error and delete the `.tmp` file.

### Step 11: Validate Constraints File

**Instruction:**
- Perform a quick check to ensure the `constraints.yaml` file is well-formed.
- Execute `cat profile/constraints.yaml | tools/validate-yaml.sh`.
- If it succeeds, report success.
- If it fails, report the error, attempt to fix it by regenerating and re-saving, and re-validate. If it fails a second time, notify the user of the critical failure.

### Step 12: Completion & Next Steps

**Instruction:**
- Provide a concise summary of the key constraints that were saved.
- Propose intelligent next steps based on the user's stated goals.
- **Example:** "Your constraints are set. You're targeting senior roles in FinTech. We can either start by having Scout `research-industries` to see who's hiring, or if you have a specific job in mind, we can `job-scan` the posting right away. What's your preference?"

## Output YAML Structure

The generated `profile/constraints.yaml` should follow this structure.

```yaml
# Job Search Constraints
# Generated by scoping-interview workflow
# Last updated: {current_date}

identity:
  name: "{extracted from resume or asked}"
  archetype: "{Generated professional summary from Step 2}"
  current_role: "{extracted from resume or asked}"

location:
  remote_preference: {value}
  hybrid_days_per_week: {if applicable}
  current_location: "{value}"
  willing_to_relocate: {true|false}
  acceptable_locations:
    - "{location 1}"
  location_dealbreakers:
    - "{location 1}"

employment:
  type: {value}
  availability: {value}
  notice_period_weeks: {if applicable}
  available_date: {if applicable}
  schedule_preference: {value}

compensation:
  minimum_base: {number}
  target_base: {number}
  equity_preference: {value}
  other_requirements:
    - "{requirement 1}"

targeting:
  target_titles:
    - "{title 1}"
  avoid_titles:
    - "{title 1}"
  seniority: {value}
  management_preference: {value}

industries:
  target:
    - "{industry 1}"
  avoid:
    - "{industry 1}"
  company_size: {value}
  company_stage: {value}
  target_companies:
    - "{company 1}"
  avoid_companies:
    - "{company 1}"

special_factors:
  clearance: {value}
  clearance_level: {if applicable}
  work_authorization: {value}
  certifications:
    - "{cert 1}"
  willing_to_obtain:
    - "{cert 1}"
  other_requirements:
    - "{requirement 1}"

preferences:
  feedback_style: brutally_honest
```
