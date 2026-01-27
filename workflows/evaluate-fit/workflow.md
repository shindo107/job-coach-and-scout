# Evaluate Fit

## Summary

**Purpose:** Assess alignment between your resume corpus and job requirements (read-only analysis)
**Agent:** Job Coach (Max)
**Reads:**
- `profile/corpus.json` — Your structured Resume Corpus (required)
- `research/openings/{company}-{role}.md` — Parsed job posting (required)
- `profile/constraints.yaml` — For feedback style preference (optional)
**Creates:**
- None — displays assessment in conversation only
**Approximate time:** 5-10 minutes
**Prerequisites:** `init` and `job-scan` completed.

---

**Trigger:** User says "evaluate my fit", "how well do I match", or after completing job-scan

## Persona

**Load and adopt:** `agents/job-coach.md`

Read the full persona file and embody Max for this workflow. Deliver honest, evidence-based assessment using Max's adversarial approach.

## Context Required

Before starting, load these files:
- `profile/corpus.json` — Your Resume Corpus (required)
- `research/openings/{company}-{role}.md` — Parsed job posting (required)

If available, also load:
- `profile/constraints.yaml` — For feedback style preference

**If corpus doesn't exist:**
```
I need your Resume Corpus to evaluate fit. I couldn't find `profile/corpus.json`.

Would you like to:
1. Run the init workflow to create your resume corpus
2. Continue without a resume (assessment will not be possible)
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

**(This step remains the same: identify and load the parsed job posting file and extract requirements.)**

### Step 2: Load Corpus and Feedback Style

1.  **- [ ] Load Resume Corpus:**
    -   Load `profile/corpus.json`.
    -   If the file is missing or invalid, stop and guide the user to run the `init` workflow.
2.  **- [ ] Load Feedback Style Preference:**
    -   Load `profile/constraints.yaml` if it exists.
    -   Extract `preferences.feedback_style` value.
    -   Default to `brutally_honest` if not set.

### Step 3: Query Corpus for Evidence (Requirement-by-Requirement)

This is the new core of the analysis. For each requirement extracted from the job posting:

1.  **- [ ] Search Corpus for Evidence:**
    -   **Instruction:** "For the requirement '[requirement text]', search the `profile/corpus.json` file for evidence. Your search should cover:"
        -   "The `skills` array: Look for an exact or closely related skill `name`."
        -   "The `accomplishments` array: Look for matches in the `skills_tags` for each accomplishment."
        -   "The `accomplishments` array: Perform a semantic search on the `content` of each accomplishment to find phrases that demonstrate the required skill, even if not explicitly tagged."

2.  **- [ ] Score Each Requirement:**
    -   **Instruction:** "Based on the evidence found, score the requirement."
    -   **Full Match (100%):** An `accomplishment` is found with a matching `skills_tag`, AND its `content` provides strong, quantifiable proof. OR, a skill is listed in the `skills` array with a high proficiency.
    -   **Partial Match (50%):** An `accomplishment` `content` is semantically related but lacks quantification or a direct skill tag. OR, a related but not identical skill is found.
    -   **No Match (0%):** No relevant skills or accomplishments can be found in the entire corpus.

3.  **- [ ] Record Evidence or Gap:**
    -   For each requirement, note:
        -   The `content` of the best matching `accomplishment` block(s).
        -   The `id` of the matching block for reference.
        -   Why it was scored as a full, partial, or no match.

### Step 4: Calculate Alignment Score

**(This step remains the same, as it operates on the scores generated in the previous step.)**

### Step 5: Generate Gap Analysis

**(This step's logic remains the same, but its input is now the structured evidence from Step 3.)**

-   **Critical Gaps:** List unmet MUST-HAVE requirements, explaining that no evidence was found in the resume corpus.
-   **Strengths:** List strong matches, citing the specific `content` from the `accomplishment` block in the corpus.

### Step 6: Max's Adversarial Assessment

**(This step remains the same, delivering the verdict based on the calculated score and gaps.)**

### Step 7: Provide Recommendation

**(This step remains the same, providing a recommendation based on the score.)**

### Step 8: Display Complete Assessment

**Do NOT save to file — this is a read-only assessment displayed in conversation.**

The structure of the output table is updated to reflect the new evidence source.

```
# Alignment Assessment: {Company} - {Role}

**Date:** {current date}
**Alignment Score:** {X}%
**Verdict:** {Excellent Fit / Good Fit / Moderate Fit / Weak Fit / Poor Fit}

---

## Score Breakdown

| Requirement | Priority | Resume Evidence (from Corpus) | Score |
|-------------|----------|-------------------------------|-------|
| {requirement} | MUST-HAVE | "acc_01: Reduced latency by 40%..." | 100% |
| {requirement} | NICE-TO-HAVE| "Not found in corpus." | 0% |
...

---

## Gap Analysis
...
```

## Output

**(This section remains the same.)**

## Recommend Next

After this workflow completes successfully, the logic for recommending the next step remains the same, but the context passed to the `tailor-resume` workflow is now the full corpus.

1.  **Suggest:** tailor-resume (if fit is reasonable, score >= 50%)
    **Rationale:** "You're at {X}% alignment. Want to improve it by tailoring your resume from the corpus?"
    **Context to pass:** `research/openings/{company}-{role}.md` (parsed requirements), `profile/corpus.json`, alignment score, gap analysis.

**(The rest of the conversational suggestions remain the same.)**
