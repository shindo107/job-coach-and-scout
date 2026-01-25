# Evaluate Fit

## Summary

**Purpose:** Assess alignment between your resume and job requirements (read-only analysis)
**Agent:** Job Coach (Max)
**Reads:**
- `profile/resume.md` — Your master resume (required)
- `research/openings/{company}-{role}.md` — Parsed job posting (required)
- `profile/constraints.yaml` — For feedback style preference (optional)
**Creates:**
- None — displays assessment in conversation only
**Approximate time:** 5-10 minutes
**Prerequisites:** job-scan completed for target posting

---

**Trigger:** User says "evaluate my fit", "how well do I match", "assess this role for me", or after completing job-scan

## Context Required

Before starting, load these files:
- `profile/resume.md` — Your master resume (required)
- `research/openings/{company}-{role}.md` — Parsed job posting (required)

If available, also load:
- `profile/constraints.yaml` — For feedback style preference

**If resume doesn't exist:**
```
I need your resume to evaluate fit. I couldn't find `profile/resume.md`.

Would you like to:
1. Run the init workflow to import your resume
2. Provide the path to your resume file
3. Paste your resume content
```

**If job posting doesn't exist:**
```
I need a parsed job posting to evaluate against. I couldn't find a posting in `research/openings/`.

Would you like to:
1. Run job-scan first to analyze a job posting
2. Specify which posting to evaluate (provide filename)
```

## Steps

### Step 1: Load Context and Identify Posting

**If user specified a company/role:**
Load `research/openings/{company}-{role}.md`

**If user didn't specify:**
```
Which job posting would you like me to evaluate your fit against?

Available postings in research/openings/:
{list available .md files}

Enter the company-role name, or provide a new posting to scan first.
```

**Once posting is identified:**
1. Load the parsed job posting file
2. Extract the requirements from the "Parsed Requirements" section
3. Note the company and role for the assessment header

**If "Parsed Requirements" section is missing or malformed:**
```
The job posting file exists but doesn't have a properly structured "Parsed Requirements" section.

This can happen if:
- The posting was manually created without using job-scan
- The job-scan workflow didn't complete successfully

Would you like to:
1. Run **job-scan** to properly parse this posting
2. Tell me the requirements and I'll assess against those
3. Paste the original job posting and I'll extract requirements now
```

**If no requirements can be extracted:**
```
I couldn't find any requirements to evaluate against.

A job posting needs at least one requirement (skill, experience, qualification) for alignment scoring.

Would you like to:
1. Run **job-scan** on the original posting URL
2. Manually list the key requirements for this role
```

### Step 2: Load Feedback Style Preference

**If `profile/constraints.yaml` exists:**
1. Load the file
2. Extract `preferences.feedback_style` value
3. Store for use in Max's assessment

**Feedback style mapping:**
- `brutally_honest` → Maximum challenge, no sugar-coating
- `balanced` → Honest with acknowledgment of strengths
- `supportive` → Encouraging delivery, same standards

**If constraints not available or feedback_style not set:**
Default to `brutally_honest` (Max's natural mode)

### Step 3: Requirement-by-Requirement Analysis

For each requirement extracted from the job posting:

**3a. Search Resume for Evidence**

Look for direct or indirect evidence that addresses the requirement:
- Exact skill/technology mentions
- Related experience descriptions
- Quantified achievements that demonstrate capability
- Transferable skills that could apply

**3b. Score Each Requirement**

| Coverage Level | Score | Criteria |
|----------------|-------|----------|
| **Full Match** | 100% | Resume explicitly addresses this with specific evidence |
| **Partial Match** | 50% | Resume suggests relevant experience but lacks specifics or quantification |
| **No Match** | 0% | Resume doesn't address this requirement at all |

**3c. Record Evidence or Gap**

For each requirement, note:
- The matching resume content (if any)
- Why it's a full/partial/no match
- What's missing (for gaps)

### Step 4: Calculate Alignment Score

**Weighting:**
- MUST-HAVE (Required) requirements: **2x weight**
- NICE-TO-HAVE (Preferred) requirements: **1x weight**

**Calculation:**
```
For each requirement:
  weighted_score = (match_percentage / 100) × weight
  weighted_max = 1.0 × weight

Total Score = (Σ weighted_scores / Σ weighted_max) × 100
```

**Score Interpretation (evidence-based thresholds — see README.md):**
- **80-100%**: Excellent fit — strong candidate, high interview callback probability
- **70-79%**: Good fit — competitive, reliably passes ATS screening
- **60-69%**: Moderate fit — worth applying, but tailoring essential
- **50-59%**: Weak fit — stretch role, possible but high effort required
- **Below 50%**: Poor fit — high rejection probability, consider better matches

### Step 5: Generate Gap Analysis

**Critical Gaps (MUST-HAVE requirements not met):**
List each unmet MUST-HAVE requirement with:
- The specific requirement
- What the posting is looking for
- What's missing from the resume
- Impact on candidacy

**Minor Gaps (NICE-TO-HAVE requirements not met):**
List each unmet NICE-TO-HAVE requirement with:
- The specific requirement
- Potential ways to address in tailoring

**Strengths (Requirements fully met):**
List strong matches to acknowledge:
- Requirements where resume excels
- Evidence that differentiates the candidate

### Step 6: Max's Adversarial Assessment

**Adopt Max's persona and deliver assessment based on feedback_style:**

**If brutally_honest:**
```
Here's the reality: {blunt assessment}

Your resume {strength or weakness statement}. The hiring manager is going to see {specific concern}.

{If gaps exist}: You're missing {critical gaps}. That's going to be a problem because {reason}.

{If strengths exist}: What's working: {strengths}. Lead with these.
```

**If balanced:**
```
Let me give you the honest picture with some context.

Strengths: {what's working}
Concerns: {what's missing}

The gaps in {areas} will need attention, but {positive framing if applicable}.
```

**If supportive:**
```
Here's where you stand — and it's workable.

You're solid on: {strengths}
Areas to strengthen: {gaps}

With some tailoring, {encouraging but realistic assessment}.
```

### Step 7: Provide Recommendation

**Based on alignment score and gap severity (evidence-based thresholds — see README.md):**

**If score >= 80% and no critical MUST-HAVE gaps:**
```
**Recommendation: PROCEED — Excellent Fit**

You're a strong candidate. Your resume addresses the core requirements well.
Run **fit-resume** to optimize positioning and maximize interview callback rate.
```

**If score 70-79% and <= 1 MUST-HAVE gap:**
```
**Recommendation: PROCEED — Good Fit**

You're competitive for this role. Your resume passes the threshold that reliably reaches hiring managers.
Run **fit-resume** to close the remaining gaps and strengthen your positioning.
```

**If score 60-69% OR has 2 MUST-HAVE gaps:**
```
**Recommendation: PROCEED WITH CAUTION — Moderate Fit**

You meet the minimum threshold recruiters consider "worth applying."
{List critical gaps}

Tailoring is essential. Run **fit-resume** to address gaps before applying.
Consider: Do you have experience not yet on your resume that addresses these gaps?
```

**If score 50-59% OR has 3 MUST-HAVE gaps:**
```
**Recommendation: STRETCH — Weak Fit**

This is a stretch role. Research shows 50%+ candidates can still land interviews, but it requires extra effort.
{List critical gaps}

Options:
1. **Tailor aggressively** — Run **fit-resume** and surface any hidden relevant experience
2. **Strengthen with referrals** — A recommendation can offset qualification gaps
3. **Apply but hedge** — Continue searching for better-fit roles in parallel

What would you like to do?
```

**If score < 50% OR has 4+ MUST-HAVE gaps:**
```
**Recommendation: RECONSIDER — Poor Fit**

I'm going to be direct: this role has significant mismatches with your current resume.
Research shows 90% rejection rate at this match level.

Critical gaps: {list}

Options:
1. **Proceed anyway** — If you have hidden experience not on your resume, we can try to surface it
2. **Find a better fit** — Run **job-scan** on roles that better match your background
3. **Use as a target** — Treat this as a future goal and identify what skills to develop

What would you like to do?
```

### Step 8: Display Complete Assessment

**Do NOT save to file — this is a read-only assessment displayed in conversation.**

```
# Alignment Assessment: {Company} - {Role}

**Date:** {current date}
**Alignment Score:** {X}%
**Verdict:** {Excellent Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit}

---

## Score Breakdown

| Requirement | Category | Priority | Resume Evidence | Score |
|-------------|----------|----------|-----------------|-------|
| {requirement} | Technical | MUST-HAVE | "{evidence}" or "Not found" | {%} |
| {requirement} | Experience | NICE-TO-HAVE | "{evidence}" or "Not found" | {%} |
...

---

## Gap Analysis

### Critical Gaps (MUST-HAVE)
{List or "None — all critical requirements addressed"}

### Minor Gaps (NICE-TO-HAVE)
{List or "None"}

### Strengths
{List top 3-5 strong matches}

---

## Max's Assessment

{Adversarial feedback in appropriate style}

---

## Recommendation

{Recommendation with next steps}

---

*This is a read-only assessment. Run **fit-resume** to tailor your resume for this role.*
```

## Output

**This workflow does NOT save files.** It provides a real-time assessment displayed in the conversation.

The assessment can be used by:
- The user to decide whether to pursue the role
- The fit-resume workflow internally for iterative scoring

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** fit-resume (if fit is reasonable, score >= 50%)
   **Rationale:** "You're at {X}% alignment. Want to improve it with tailoring?"
   **Context to pass:** `research/openings/{company}-{role}.md` (parsed requirements), alignment score, gap analysis

2. Present the suggestion conversationally based on fit level:

   **If Excellent/Good Fit (70%+):**
   "You're at {X}% alignment — strong fit! Ready to lock in your positioning with a tailored resume? [Yes/No/Something else]"

   **If Moderate Fit (60-69%):**
   "You're at {X}% alignment — worth pursuing. Tailoring is essential to close the gaps. Want to start? [Yes/No/Something else]"

   **If Weak Fit (50-59%):**
   "You're at {X}% alignment — this is a stretch, but possible with strong tailoring. Want to try? [Yes/Find better matches/Something else]"

   **If Poor Fit (<50%):**
   "You're at {X}% alignment — significant gaps. I'd recommend finding a better-fit role. Want to scan another posting instead? [Scan another/Try anyway/Something else]"

3. If user agrees to tailor: Load `workflows/fit-resume/workflow.md` and execute
4. If user wants alternatives: Load `workflows/job-scan/workflow.md` for a new posting
5. If user declines: Summarize alignment assessment and end gracefully
6. If user requests different workflow: Honor their request
