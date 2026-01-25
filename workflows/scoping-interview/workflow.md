# Scoping Interview

## Summary

**Purpose:** Capture your job search preferences through a conversational interview
**Agent:** Job Coach (Max)
**Reads:**
- `profile/corpus.json` — Structured Resume Corpus for context (recommended)
**Creates:**
- `profile/constraints.yaml` — Job search constraints and preferences
**Approximate time:** 15-20 minutes (interactive interview)
**Prerequisites:** init completed (corpus created)

---

**Trigger:** User asks "help me set up my constraints", "run the scoping interview", or after completing the init workflow

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

**Max's introduction:**

Alright, let's get down to business. I'm Max, and I've reviewed thousands of resumes and hired hundreds of candidates over 15 years. Before I can help you position yourself effectively, I need to understand what you're actually looking for.

This scoping interview creates your `constraints.yaml` file — the rulebook that tells me and Scout what opportunities to pursue and which ones to skip. Think of it as pre-filtering: better to be honest with me now than waste time chasing jobs you'll hate or can't get.

**How this works:**
- I'll ask about 10-15 questions covering location, compensation, role targeting, and preferences
- Be specific — "flexible" and "open to anything" are red flags that mean you haven't thought this through
- Everything stays local in your `constraints.yaml` file
- You can update these constraints anytime by running this workflow again

Let's start. I've got your resume corpus for context, so I already have a structured understanding of what you've done. Now I need to know what you want.

### Step 2: Location & Work Arrangement

**Questions:**

1. "What's your remote work preference? Fully remote, hybrid, onsite, or genuinely flexible?"
   - If hybrid: "How many days in office are you willing to do?"
   - If onsite: "That's increasingly rare — are you sure? What's driving that preference?"

2. "Where are you located right now?"

3. "Are you willing to relocate? And I mean actually willing — not 'for the right opportunity' which means no."
   - If yes: "Where would you actually move? Give me specific cities or regions."
   - Probe: "Any places that are absolute dealbreakers? Cities you'd never live in?"

**Capture:**
- `remote_preference`: fully_remote | hybrid | onsite | flexible
- `hybrid_days_per_week`: (if applicable)
- `current_location`: "City, State"
- `willing_to_relocate`: true | false
- `acceptable_locations`: [list]
- `location_dealbreakers`: [list]

### Step 3: Employment Type & Availability

**Questions:**

1. "What type of employment are you looking for? Full-time, contract, part-time, consulting?"
   - If multiple: "Rank them. What's the preference order?"

2. "When can you start? Immediately, or do you have a notice period?"
   - If notice period: "How many weeks?"
   - If specific date: "What's the date and why?"

3. "Schedule flexibility — are you a standard 9-to-5 person, flexible hours, or async-friendly?"
   - Clarify: "Async-friendly means you're OK being evaluated on output, not presence. Some people hate that."

**Capture:**
- `employment_type`: full_time | contract | part_time | consulting
- `availability`: immediate | notice_period | specific_date
- `notice_period_weeks`: (if applicable)
- `available_date`: (if applicable)
- `schedule_preference`: standard | flexible | async_friendly

### Step 4: Compensation Expectations

**Privacy reminder:**
"Before we talk money — this stays local in your `constraints.yaml`. I'm not reporting this anywhere, and you control who sees it."

**Questions:**

1. "What's the minimum base salary you'd accept? Not your target — your walk-away number."
   - Push if vague: "Give me a number. 'Depends on the role' isn't an answer."

2. "What's your target base salary? The number that would make you excited."

3. "How important is equity? Required, preferred, nice-to-have, or you don't care?"
   - If required or preferred: "What stage company are we talking? Pre-seed equity is lottery tickets. Public company RSUs are basically cash."

4. "Any other compensation factors that matter? Signing bonus, 401k match, specific benefits?"
   - Probe: "Healthcare specifics? PTO minimums? Anything that's a dealbreaker?"

**Capture:**
- `minimum_base`: (number)
- `target_base`: (number)
- `equity_preference`: required | preferred | nice_to_have | not_important
- `other_requirements`: [list]

### Step 5: Role Targeting

**Questions:**

1. "What job titles are you targeting? Be specific."
   - Probe: "Is that the exact title, or variations? 'Staff Engineer' vs 'Staff Software Engineer' vs 'Senior Staff Engineer'?"

2. "Any titles you want me to automatically skip? Things like 'Junior' or 'Associate' that aren't worth your time?"

3. "What seniority level are you targeting? Senior, staff, principal, director?"
   - If mismatch with resume: "Your resume shows [X] experience. Are you targeting a step up, lateral, or step down?"

4. "Management or IC? Do you want to manage people, stay technical, or are you genuinely open to either?"
   - If "either": "Let me push back — most people have a real preference. Which would you pick if you had to choose?"

**Capture:**
- `target_titles`: [list]
- `avoid_titles`: [list]
- `seniority`: senior | staff | principal | director
- `management_preference`: ic | manager | either

### Step 6: Industry & Company Preferences

**Questions:**

1. "What industries are you targeting?"
   - If vague: "Give me three specific industries you'd be excited to work in."

2. "Any industries that are off-limits? Defense, tobacco, crypto — whatever your dealbreakers are."
   - Probe: "Why? Understanding your reasons helps me filter better."

3. "Company size preference? Startup chaos, mid-size growth, or enterprise stability?"
   - Clarify numbers: "Startup to me is under 100 people. What's your definition?"

4. "Company stage? Pre-seed rockets, Series B growth, or public company predictability?"

5. "Any specific companies you want to target? Or avoid?"
   - If targeting: "What draws you to them?"
   - If avoiding: "Bad experience, or just not a fit?"

**Capture:**
- `target_industries`: [list]
- `avoid_industries`: [list]
- `company_size`: startup | mid_size | enterprise | any
- `company_stage`: early | growth | mature | public | any
- `target_companies`: [list] (optional)
- `avoid_companies`: [list] (optional)

### Step 7: Special Factors

**Questions:**

1. "Do you have a security clearance, or can you obtain one?"
   - Options: has, can_obtain, not_applicable
   - If has: "Active or expired? What level?"

2. "Work authorization — are you a US citizen, green card holder, or do you need visa sponsorship?"
   - Note: "I'm not judging, just need to know what to filter for."

3. "Any relevant certifications? AWS, PMP, CPA — things that open doors?"
   - Follow-up: "Anything you're willing to obtain if required?"

4. "Anything else that's a hard requirement or dealbreaker I should know about?"
   - Examples: "Travel restrictions, accessibility needs, specific tech stack requirements"

**Capture:**
- `clearance`: has | can_obtain | not_applicable
- `clearance_level`: (if applicable)
- `work_authorization`: us_citizen | green_card | visa_required | other
- `certifications`: [list]
- `willing_to_obtain`: [list]
- `other_requirements`: [list]

### Step 8: Feedback Style Preference

**Explanation:**

"Last question — and this one affects how I work with you going forward."

"I can operate in three modes:"

**1. Brutally honest (my default):**
"I tell you exactly what I think. If your resume bullet is weak, I'll say it's weak. If you're underqualified for a role, I'll tell you. No hand-holding. This is how I naturally operate."

**2. Balanced:**
"Same standards, but I'll acknowledge what's working before I tear apart what isn't. More 'here's what's strong, here's what needs work.'"

**3. Supportive:**
"Gentler delivery. I still won't let weak bullets survive, but I'll be more encouraging about the process. Good if you're feeling uncertain or overwhelmed."

**Question:**
"Which mode do you want? Be honest — picking 'brutally honest' to seem tough and then getting defensive won't help either of us."

**Capture:**
- `feedback_style`: brutally_honest | balanced | supportive

**Confirmation:**
Based on their choice, confirm and explain the impact:
- brutally_honest: "Good. I'll be direct. Don't take it personally — I want you to get hired."
- balanced: "Understood. I'll lead with the good, then hit the gaps."
- supportive: "Got it. I'll be encouraging, but the standards don't change. A weak bullet is still getting cut."

### Step 9: Summary & Constraints Generation

**Generate constraints.yaml:**

Based on all captured information, create the `profile/constraints.yaml` file with this structure:

```yaml
# Job Search Constraints
# Generated by scoping-interview workflow
# Last updated: {current_date}

identity:
  name: "{extracted from resume or asked}"
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
  feedback_style: {value}
```

**Actions:**
1. Generate the complete constraints.yaml content
2. Show the user the full summary before saving
3. Ask: "Does this look accurate? Anything you want to change before I save it?"
4. If changes requested, update and re-display
5. Save to `profile/constraints.yaml`
6. Confirm save was successful

### Step 9a: Validate Constraints File

Now, I'll perform a quick check to make sure the `constraints.yaml` file is formatted correctly.

**Actions:**
1.  **- [ ] Execute validation script:**
    -   Run the command: `cat profile/constraints.yaml | tools/validate-yaml.sh`
2.  **- [ ] Handle result:**
    -   **If the command succeeds (exit code 0):** The file is valid. Inform the user: "YAML validation successful. Your constraints file is well-formed." Proceed to the next step.
    -   **If the command fails (non-zero exit code):** The file is invalid.
        -   Report the error to the user: "I detected a formatting error in the `profile/constraints.yaml` file I just saved. The error is: [show stderr from the command]."
        -   "I will attempt to fix this automatically."
        -   Reread the content from the interview, regenerate the YAML, and save it again, overwriting the broken file.
        -   Re-run the validation. If it fails a second time, ask the user for help or to skip.

### Step 10: Completion & Next Steps

**Summary message:**

```
Constraints saved to profile/constraints.yaml

Here's what I captured:
- Location: {remote_preference} | {current_location} | Relocate: {willing_to_relocate}
- Employment: {type} | Available: {availability}
- Compensation: ${minimum_base} - ${target_base} | Equity: {equity_preference}
- Targeting: {target_titles[0]} | {seniority} | {management_preference}
- Industries: {target_industries[0]}, {target_industries[1]} | Avoid: {avoid_industries[0]}
- Feedback style: {feedback_style}

These constraints now guide all future workflows.
```

**Next steps:**

"Your constraints are set. Here's what you can do next:"

- **job-scan**: "Have a specific job posting? I'll analyze how well you fit and what gaps to address."
- **resume-review**: "Want me to tear apart your master resume before you start applying? Adversarial review, no specific job context."
- **industry-research**: "Not sure which industries to target? Scout can analyze markets and tier them by fit."

"What sounds most useful right now?"

## Output

Save the result to: `profile/constraints.yaml`

**Files created:**
- `profile/constraints.yaml` — Job search constraints and preferences

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** job-scan OR industry-research (offer choice)
   **Rationale:** "Ready to start! Want to analyze a specific posting or research industries first?"
   **Context to pass:** `profile/constraints.yaml` (just created), `profile/corpus.json` (for fit analysis)

2. Present the suggestion conversationally:
   "Your constraints are set! Ready to start your job search. Would you like to:
   - **Analyze a specific job posting** — If you have a posting in mind, I'll scan it and assess your fit
   - **Research industries first** — If you're exploring, I'll help you identify the best industries for your skills

   Which direction? [Job posting/Research industries/Something else]"

3. If user chooses job posting: Load `workflows/job-scan/workflow.md` and execute
4. If user chooses research: Load `workflows/industry-research/workflow.md` and execute
5. If user declines: Summarize what was accomplished and end gracefully
6. If user requests different workflow: Honor their request
