# Fit Resume

## Summary

**Purpose:** Tailor your resume through interview-driven extraction and voice-matched bullet generation
**Agent:** Job Coach (Max)
**Reads:**
- `profile/resume.md` — Master resume (required)
- `research/openings/{company}-{role}.md` — Parsed job posting (required)
- `profile/constraints.yaml` — For feedback style preference (optional)
- `applications/resumes/*.md` — Previous tailored resumes for content reuse (optional)
**Creates:**
- `applications/resumes/{company}-{role}.md` — Tailored resume with alignment scores and metadata
**Approximate time:** 20-45 minutes (interactive probing for each gap)
**Prerequisites:** job-scan completed for target posting

---

> **CORE WORKFLOW**: This is the heart of Job Coach & Scout — the interview-driven extraction model that actively probes for forgotten experiences and positions them against specific job requirements.

**Trigger:** User says "help me tailor my resume for [company]", "fit my resume", or after evaluate-fit reveals gaps to address

## Session Continuity

**Claude Code conversation history automatically preserves your progress.** You can pause at any checkpoint and resume later:

- **To pause:** At any checkpoint, say "take a break" or simply close the session
- **To resume:** In the same Claude Code session, say "let's continue" or "where were we?"
- **To resume in a new session:** Say "continue fit-resume for {company}" — Claude Code will reload context and ask where you left off

**Checkpoints are provided after each gap is addressed** (see Step 3f), summarizing:
- Which gap was just addressed
- What evidence was captured
- How many gaps remain

**Note:** If starting a completely new session, you may need to re-share any experiences discussed previously, as they exist only in conversation history.

## Context Required

Before starting, load these files:
- `profile/resume.md` — Master resume (required)
- `research/openings/{company}-{role}.md` — Parsed job posting (required)

If available, also load:
- `profile/constraints.yaml` — For feedback style preference
- `applications/resumes/*.md` — Previous tailored resumes (CORPUS for content reuse)

**If resume doesn't exist:**
```
I need your resume to tailor. I couldn't find `profile/resume.md`.

Would you like to:
1. Run the init workflow to import your resume
2. Provide the path to your resume file
3. Paste your resume content
```

**If job posting doesn't exist:**
```
I need a parsed job posting to tailor against. I couldn't find a posting in `research/openings/`.

Would you like to:
1. Run job-scan first to analyze a job posting
2. Specify which posting to use (provide filename)
```

## Steps

### Step 1: Load Context and Analyze Voice

**1a. Load and validate required files:**
1. Load `profile/resume.md`
2. Load `research/openings/{company}-{role}.md`
3. Load `profile/constraints.yaml` if available for feedback style

**1b. Analyze resume writing style for voice matching:**

Study the existing resume bullets to identify:
- **Sentence structure**: Bullet length, complexity level
- **Verb patterns**: Action verbs used (led, built, drove, etc.)
- **Quantification style**: Percentages, dollar amounts, team sizes, time frames
- **Tone**: Formal vs conversational
- **Technical depth**: Jargon level, acronym usage

Store these patterns — all new bullets must match the user's voice.

**If resume has few or no existing bullets to analyze:**
```
Your resume doesn't have many bullets for me to analyze your writing style.

Before I generate new bullets, I need to understand your voice. Can you:
1. Share a writing sample or previous resume version
2. Describe your preferred style (formal/conversational, short/detailed)
3. Let me generate bullets and you'll edit them to match your voice

Which approach works for you?
```

**1c. Load feedback style preference:**
- `brutally_honest` → Maximum challenge, no sugar-coating (default)
- `balanced` → Honest with acknowledgment of strengths
- `supportive` → Encouraging delivery, same standards

### Step 2: Run Gap Identification

**2a. Extract and validate requirements:**

1. Extract requirements from the "Parsed Requirements" section of the job posting
2. Validate the posting has proper structure

**If "Parsed Requirements" section is missing or malformed:**
```
The job posting file exists but doesn't have a properly structured "Parsed Requirements" section.

This can happen if:
- The posting was manually created without using job-scan
- The job-scan workflow didn't complete successfully

Would you like to:
1. Run **job-scan** to properly parse this posting
2. Tell me the requirements and I'll tailor against those
3. Paste the original job posting and I'll extract requirements now
```

**If no requirements can be extracted:**
```
I couldn't find any requirements to tailor against.

A job posting needs at least one requirement for me to help you tailor your resume.

Would you like to:
1. Run **job-scan** on the original posting URL
2. Manually list the key requirements for this role
```

**2b. Score current alignment (invoke evaluate-fit logic):**

For each requirement from the parsed job posting:
1. Search resume for direct or indirect evidence
2. Score as Full Match (100%), Partial Match (50%), or No Match (0%)
3. Note specific evidence or what's missing

**Note:** This uses the same scoring logic as the evaluate-fit workflow. You can run `evaluate-fit` separately first for a detailed assessment, or this workflow will perform the gap analysis inline.

**2c. Prioritize gaps for interview:**

Create an interview plan ordered by priority:

**MUST-HAVE gaps first (critical to address):**
```
1. {Requirement} — MUST-HAVE, No Match
   Why it matters: {reason from posting}
   What's missing: {specific gap}

2. {Requirement} — MUST-HAVE, Partial Match
   Current evidence: {what resume shows}
   Gap: {what's missing - quantification, specifics, etc.}
```

**NICE-TO-HAVE gaps second (if time permits):**
```
3. {Requirement} — NICE-TO-HAVE, No Match
   ...
```

**2d. Calculate baseline score and set iteration counter:**

Initialize `iteration_count = 1` for tracking multiple improvement passes.

Record the current alignment score before tailoring — we'll compare after.

### Step 2.5: Corpus Analysis & Content Reuse

**This step accelerates tailoring by reusing approved content from previous applications.**

**2.5a. Scan corpus for existing content:**

Load all files from `applications/resumes/` (excluding the current target if it exists).

For each previous tailored resume:
- Extract all bullet points with their section context
- Note which requirements they were written to address (from metadata `gaps_addressed`)
- Note the date generated (for freshness assessment)

**If a corpus file is malformed or empty:**
```
⚠️ Skipping {filename}: Unable to parse (empty or invalid format).
```
Continue processing remaining files — don't fail the entire corpus scan.

**If no previous resumes exist:**
```
This is your first tailored resume — no corpus to draw from yet.
After this session, your content will be available for future applications.
```
Skip to Step 3 (Interview).

**2.5b. Match corpus content to current requirements:**

For each requirement in the new job posting:
1. Search previous resume bullets for relevant content
2. Use semantic matching to identify bullets addressing similar skills/experiences
3. Score relevance:
   - **High:** Direct match — bullet addresses same requirement
   - **Medium:** Related — bullet demonstrates transferable skill
   - **Low:** Tangential — weak connection

**2.5c. Calculate corpus coverage:**

```
📊 **Corpus Analysis:** {X}% requirement coverage from previous applications

Found {count} previous tailored resumes.
Matching content for {matched_count} of {total_count} requirements.
```

**If corpus contains more than 20 files:**
```
ℹ️ **Large Corpus Notice:** You have {count} previous applications.
Scanning may take a moment. Consider archiving older applications you no longer reference.
```

**2.5c-2. Aggregate corpus freshness check (runs BEFORE individual matches):**

Assess overall corpus health using the freshness threshold:

```
{If >50% of matched bullets exceed the freshness threshold:}

⚠️ **Corpus Health Notice:** {X}% of your reusable content exceeds your freshness threshold.

Consider running a **corpus refresh session** after this application to:
- Validate aging bullets are still accurate
- Update quantifications with recent data
- Remove outdated experiences

[Acknowledge and continue] [Schedule reminder]
```

**2.5d. Present matches for user decision:**

For each requirement with High or Medium relevance match:

```
**Requirement: "{requirement_text}"**

From your {company} application ({age}):
> "{matched_bullet_text}"

Source: applications/resumes/{source_file}
Relevance: {High/Medium}

[Reuse] [Modify] [Skip — probe for new content]
```

**2.5e. Handle user decisions:**

**If user chooses "Reuse":**
- Mark bullet for inclusion in new resume
- Track source for metadata: `reused_from: {source_file}`
- Mark requirement as COVERED (skip probing)

**If user chooses "Modify":**
```
How would you like to modify this bullet?

Current: "{original_bullet}"

Your changes:
```
- Save modified version for new resume
- Track as `modified_from: {source_file}`
- Mark requirement as COVERED (skip probing)
- **Persist improvement:** Ask user if they want to update the source file with this improved version:
  ```
  This improved bullet could benefit future applications too.
  Update the source file ({source_file}) with this version? [Yes/No]
  ```
  If yes:
  1. Verify source file still exists (it may have been deleted/renamed)
  2. If file exists: edit to replace original bullet with improved version
  3. If file missing: warn user and skip update
     ```
     ⚠️ Source file {source_file} no longer exists. Skipping update.
     The improved bullet will still be used in your new resume.
     ```

**If user chooses "Skip":**
- Mark requirement for probing in Step 3
- Content will be freshly extracted via interview

**2.5f. Handle content freshness:**

Check `profile/constraints.yaml` for `corpus_freshness_months` setting.
- If constraints.yaml doesn't exist: use default of 6 months
- If constraints.yaml exists but key is missing: use default of 6 months
- If key exists: use configured value

For content older than the freshness threshold, add freshness warning:

```
⚠️ This bullet is from your {company} application ({X} months ago).

Still accurate? [Reuse as-is] [Update] [Skip]
```

**Track validation:** When user approves old content (Reuse as-is or Update), record today's date as `last_validated` for that bullet in session context. This validation date will be saved in the output metadata.

**2.5g. Summarize corpus decisions:**

```
## Corpus Decisions Summary

| Requirement | Decision | Source |
|-------------|----------|--------|
| {req 1} | ✓ Reused | stripe-staff-engineer.md |
| {req 2} | ✓ Modified | acme-senior-engineer.md |
| {req 3} | → Probe | (no match / skipped) |
| {req 4} | → Probe | (no match) |

**Content reused:** {count} bullets
**Content modified:** {count} bullets
**Requires probing:** {count} requirements

{If all requirements covered:}
All requirements have existing content! Proceeding to generate your tailored resume.

{If gaps remain:}
Let me probe for the {count} remaining requirements...
```

**2.5h. Skip to Step 4 if all requirements covered:**

If user approved/modified content for ALL requirements:

```
✅ All {count} requirements have content from your corpus!

Corpus content selected:
- {count} bullets reused as-is
- {count} bullets modified

No probing interview needed. Ready to generate your tailored resume?
[Yes - proceed to generation] [Review selections first]
```

If user chooses "Review selections first", re-display the corpus decisions summary from 2.5g.

If user confirms, skip Step 3 entirely and proceed to Step 4 (Generate Voice-Matched Bullets).

### Step 3: Interview for Each Gap (CORE INNOVATION)

**Note:** Only probe requirements NOT covered by corpus reuse (Step 2.5). If all requirements were addressed via corpus, skip to Step 4.

**Adopt Max's full adversarial persona for the interview.**

For each gap in priority order (excluding requirements covered by corpus):

**3a. State the requirement and why it matters:**
```
The posting emphasizes {requirement}. Here's why they care:
{Context from job posting — what this enables, what problem it solves}

Your resume currently {shows partial evidence / doesn't address this}.
```

**3b. Probe with memory triggers:**
```
Think back to your time at {previous company from resume}.
- Was there ever a time when you dealt with {requirement}?
- Around {date range}, what projects were you focused on?
- Did you ever support or collaborate with someone handling {function}?
- Even if it wasn't your main responsibility, did you ever touch {area}?
```

**3c. If user shares experience — challenge for specifics:**
```
You said you "{user's vague statement}."

That's a start, but tell me more:
- WHO was involved? How many people?
- WHAT specifically did you do vs. the team?
- WHEN was this? How long did it take?
- WHAT was the outcome? What changed?
- HOW would someone verify this in a reference call?
```

**3d. Push for quantification:**
```
"Improved the process" doesn't cut it.
- By how much?
- Compared to what baseline?
- What's the number someone would remember?

If you can't quantify it, we need a different angle.
```

**3e. Confirm no experience or capture details:**

**If user confirms no relevant experience:**
```
Understood. Let's move on to the next gap.
{Move to next requirement}
```

**If user provides substantive experience:**
```
Good. I have what I need to draft a bullet. Let's continue and I'll show you the new content at the end.
{Capture: requirement addressed, specific experience, quantification, outcome}
```

**3f. Checkpoint after each major gap:**
```
--- CHECKPOINT ---
Gap addressed: {requirement}
Evidence captured: {summary}
Gaps remaining: {count}
Next gap: {next requirement to probe}

Ready to continue?
- "yes" or "continue" → proceed to next gap
- "take a break" → pause here, resume anytime with "let's continue"
- "review" → show all evidence captured so far
```

**If user says "review", display cumulative evidence:**
```
## Evidence Captured So Far

| # | Requirement | Status | Evidence Summary |
|---|-------------|--------|------------------|
| 1 | {req 1} | ✓ Captured | {brief summary of experience shared} |
| 2 | {req 2} | ✓ Captured | {brief summary} |
| 3 | {req 3} | ✗ No experience | User confirmed none |
| 4 | {req 4} | ⏳ Pending | Not yet probed |

**Bullets to generate:** {count based on captured evidence}
**Gaps remaining:** {count}

Continue probing? (yes / take a break)
```

### Step 4: Generate Voice-Matched Bullets

For each captured experience:

**4a. Draft bullet matching user's voice:**

Apply the voice patterns identified in Step 1:
- Match sentence structure and length
- Use similar action verbs
- Match quantification style
- Maintain consistent tone

**4b. Ensure bullet addresses the requirement:**

Each bullet must:
- Directly relate to a specific job requirement
- Include the evidence captured in the interview
- Contain quantification or specific outcomes
- Survive the "tell me more about that" test

**4c. Present bullets for approval:**
```
Here's what I've drafted based on our conversation:

**For {requirement}:**
> {New bullet}

This addresses: {which requirement from posting}
Based on: {what you told me}

Does this accurately represent your experience? (approve / edit / cut)
```

Iterate until user approves each bullet.

### Step 5: Display Diff View

**Show the user exactly what changed between their original resume and the tailored version.**

**5a. Generate diff by resume section:**

```markdown
## Changes Made to Your Resume

### {Section Name} (e.g., Experience)

**Reused from corpus:** (from previous applications)
♻️ {Bullet reused from stripe-staff-engineer.md}
♻️ {Another reused bullet from acme-senior-engineer.md}

**Modified from corpus:**
🔄 "{Original from corpus}" →
   "{Updated version for this application}"

**Added:** (new content from this session)
+ {New bullet addressing requirement}
+ {Another new bullet}

**Modified:**
~ "{Original bullet}" →
  "{Enhanced bullet with quantification}"

**Removed:**
- {Weak or irrelevant bullet that was cut}
- {Generic bullet replaced by stronger version}

**Repositioned:**
↑ Moved "{bullet}" higher to emphasize {skill}

### {Another Section} (e.g., Skills)

**Added:**
+ {New skill relevant to posting}
```

**Note:** Only show sections with changes. Reused content is marked with ♻️ to show corpus origin. If Max recommends removing weak bullets, they appear in the "Removed" section so user can review before finalizing.

**5b. Summarize changes:**
```
**Change Summary:**
- Bullets reused from corpus: {count}
- Bullets modified from corpus: {count}
- Bullets added (new): {count}
- Bullets modified: {count}
- Bullets removed: {count}
- Bullets repositioned: {count}
- Sections affected: {list}
```

### Step 6: Calculate and Display Alignment Score

**6a. Re-run alignment scoring:**

With the new bullets integrated, recalculate alignment score using evaluate-fit logic.

**6b. Display score comparison table:**

```markdown
## Alignment Score

| Stage | Score | Change |
|-------|-------|--------|
| Before tailoring | {X}% | — |
| After this iteration | {Y}% | +{diff}% |

**Gaps Closed:**
- {requirement 1}: No Match → Full Match ✓
- {requirement 2}: Partial → Full Match ✓

**Remaining Gaps:**
- {requirement 3}: Still unaddressed (no evidence surfaced)
- {requirement 4}: Partial match (could be stronger)
```

**6c. Indicate alignment tier (evidence-based thresholds — see evaluate-fit/README.md):**

**If score >= 80%:**
```
✅ **Excellent Fit!** You're at {Y}% alignment — strong candidate with high interview callback probability.
```

**If score 70-79%:**
```
✅ **Good Fit!** You're at {Y}% alignment — competitive positioning that reliably passes ATS screening.
```

**If score 60-69%:**
```
⚠️ **Moderate Fit:** You're at {Y}% alignment. Worth applying, but continued tailoring recommended.
```

**If score 50-59%:**
```
⚠️ **Weak Fit:** You're at {Y}% alignment. This is a stretch — consider probing for more experiences.
```

**If score < 50%:**
```
🔴 **Poor Fit:** You're at {Y}% alignment. Research shows ~90% rejection at this level. Significant gaps remain.
```

### Step 7: Iteration Decision

**Ask the user whether to continue improving or finalize.**

**7a. Present iteration choice (based on evidence-based tiers):**

**If score >= 70% (Good/Excellent fit):**
```
Great progress! You've reached {Y}% alignment — {Excellent/Good} fit territory.

What would you like to do?
1. **Save & finish** — Lock in these improvements
2. **Push higher** — Continue probing for more experiences
3. **Review changes** — See the diff again before deciding
```

**If score 50-69% (Moderate/Weak fit):**
```
You're at {Y}% alignment — {Moderate/Weak} fit.

What would you like to do?
1. **Continue improving** — Probe remaining gaps for more experiences (recommended)
2. **Good enough** — Save current version and move on
3. **Review changes** — See what we've done so far
```

**If score < 50% (Poor fit):**
```
You're at {Y}% alignment — still in Poor fit territory with high rejection risk.

What would you like to do?
1. **Keep going** — We need to surface more experiences (strongly recommended)
2. **Save anyway** — Accept current state, but consider finding better-fit roles
3. **Review changes** — See what we've captured so far
```

**7b. Handle iteration:**

**If user chooses to continue:**
1. Identify remaining unaddressed gaps (track which gaps have been probed)
2. Return to Step 3 to probe for additional experiences
3. Increment iteration counter for score tracking

**If user chooses to review:**
1. Re-display the diff from Step 5
2. Return to iteration choice

**If user chooses to save/finish:**
1. Proceed to Step 8 (Final Save)

**7c. Track iteration history:**

For multiple iterations, maintain cumulative score tracking:
```markdown
| Stage | Score | Change |
|-------|-------|--------|
| Before tailoring | 52% | — |
| After iteration 1 | 68% | +16% |
| After iteration 2 | 79% | +11% |
| After iteration 3 (final) | 85% | +6% |
| **Total improvement** | | **+33%** |
```

**7d. Handle exhausted experiences:**

If user has no more experiences to share for remaining gaps:
```
We've addressed what we can. Some gaps remain, but your resume is now much stronger for this role.

Ready to save the tailored version?
```

### Step 8: Final Save with Metadata

**8a. Create the tailored resume:**

Integrate all new and modified bullets into the master resume:
- Position new bullets appropriately in relevant sections
- Prioritize requirements that matter most to this role
- Maintain overall resume structure and flow

**8a-2. Apply inline reuse markers (configurable):**

Check `profile/constraints.yaml` for `include_reuse_markers` setting:
- If `true`: Add inline HTML comments after each reused/modified bullet
- If `false` or not set: Omit inline markers (metadata-only tracking)

**When `include_reuse_markers: true`:**
```markdown
- Architected event-driven payment system handling 2M transactions <!-- reused-from: stripe-staff-engineer.md -->
- Mentored 4 engineers on distributed systems <!-- modified-from: acme-senior-engineer.md -->
- Designed ML feature pipeline with 50ms latency <!-- new: probed 2026-01-25 -->
```

These markers are invisible when rendered but provide provenance tracking in the source file.

**8b. Save to output location with full metadata:**

Save to: `applications/resumes/{company}-{role}.md`

**If `applications/resumes/` directory doesn't exist:**
Create it first. This can happen if user skipped the init workflow.
```
Creating applications/resumes/ directory for your tailored resumes...
```

Include comprehensive metadata header:
```markdown
---
source_posting: research/openings/{company}-{role}.md
initial_score: {X}%
final_score: {Y}%
score_improvement: +{total_diff}%
iterations: {count}
date_generated: {current date}
bullets_added: {count}
bullets_modified: {count}
gaps_addressed:
  - {requirement 1}
  - {requirement 2}
gaps_remaining:
  - {requirement 3}
content_sources:
  reused_bullets: {count}
  modified_bullets: {count}
  new_bullets: {count}
  sources:
    - {source-file-1}.md ({count} bullets)
    - {source-file-2}.md ({count} bullets)
  validations:
    - bullet: "{bullet text snippet...}"
      original_date: {date from source file}
      last_validated: {today's date when user approved reuse}
---

# {User Name} - Resume

## Tailored for: {Company} - {Role}

{Full tailored resume content...}
```

**8c. Confirm save:**
```
✅ **Resume saved:** applications/resumes/{company}-{role}.md

**Final Statistics:**
- Initial alignment: {X}%
- Final alignment: {Y}%
- Total improvement: +{diff}%
- Bullets added: {count}
- Bullets modified: {count}
- Iterations: {count}

**Corpus Usage:**
- Bullets reused from previous applications: {reused_count}
- Bullets modified from previous: {modified_count}
- New bullets from this session: {new_count}
```

### Step 9: Workflow Completion

**9a. Display final summary:**

```markdown
## Tailoring Complete!

**{Company} - {Role}**

| Metric | Value |
|--------|-------|
| Initial Score | {X}% |
| Final Score | {Y}% |
| Improvement | +{diff}% |
| New Bullets | {count} |
| Modified Bullets | {count} |

**File saved:** `applications/resumes/{company}-{role}.md`
```

**9b. Suggest next workflow:**

```
Your resume is now tailored for {Company}. What's next?

**Recommended:** Run **cover-letter** to generate a voice-matched cover letter
that complements this resume — telling the story your bullets can't.

Would you like to start the cover-letter workflow now? (yes / no / later)
```

**9c. Handle user response:**

**If yes:** Begin cover-letter workflow with context:
- Load the tailored resume just created
- Load the same job posting
- Carry forward voice patterns and key achievements

**If no/later:**
```
No problem! Your tailored resume is saved and ready.

When you're ready for a cover letter, just say "cover letter for {company}"
and I'll pick up where we left off.
```

## Output

Save the tailored resume to: `applications/resumes/{company}-{role}.md`

**Files created:**
- `applications/resumes/{company}-{role}.md` — Tailored resume with new bullets, comprehensive metadata, and alignment scores

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** cover-letter
   **Rationale:** "Resume tailored! Generate a matching cover letter?"
   **Context to pass:** `applications/resumes/{company}-{role}.md` (tailored resume), `research/openings/{company}-{role}.md` (requirements), voice patterns from resume

2. Present the suggestion conversationally:
   "Your resume is now tailored for {Company} — alignment improved from {initial}% to {final}%! A voice-matched cover letter will complete your application package by telling the story your resume can't. Ready to generate one? [Yes/No/Something else]"

3. If user agrees: Load `workflows/cover-letter/workflow.md` and execute
4. If user declines: Summarize what was accomplished and end gracefully
   "Your tailored resume is saved at `applications/resumes/{company}-{role}.md`. When you're ready for a cover letter, just ask."
5. If user requests different workflow: Honor their request
