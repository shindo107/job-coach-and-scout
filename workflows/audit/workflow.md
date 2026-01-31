# System Audit

## Summary

**Purpose:** Verify that the core `init` -> `job-scan` -> `tailor-resume` pipeline is functioning as expected after any changes.
**Agent:** Job Coach (Max) & Job Scout
**Phase:** system
**Reads:**
- `workflows/audit/sample_data/sample_resume.md` — Sample resume for testing
- `workflows/audit/sample_data/sample_job_description.txt` — Sample job posting for testing
**Creates:** None (temporary files are cleaned up)
**Updates:** None
**Prerequisites:** None

---

**Trigger:** User says "run a system audit" or "verify the workflows".

## Persona

**Load and adopt:** `agents/job-coach.md` AND `agents/job-scout.md`.

---

## Details

This workflow provides a consistent way to test the core functionality of the Job Coach & Scout system. It uses a predefined sample resume and job description to run through the main pipeline and asks for confirmation that the output is correct.

**This is a read-only, diagnostic workflow.** It will create temporary files but will guide you to clean them up at the end.

---

## Steps

### Step 1: Introduction

**Instruction:** Explain the purpose of the audit: "I'm going to run a system audit to make sure the core workflows are behaving as expected. This will test the resume parsing (`init`), job scanning (`job-scan`), and the gap-analysis portion of the resume tailoring (`tailor-resume`) workflows. I'll need your help to confirm the results at the end."

### Step 2: Setup and Corpus Creation

**Instruction:** This step is unchanged. It creates a temporary corpus from sample data to test the parsing logic of the `init` workflow.

1.  **- [ ] Load sample data:**
    -   Read `workflows/audit/sample_data/sample_resume.md`.
    -   Read `workflows/audit/sample_data/sample_job_description.txt`.

2.  **- [ ] Create temporary Resume Corpus:**
    -   **Instruction:** Using the logic from the `init` workflow, parse the sample resume into a structured JSON and save it to `profile/audit_corpus.json`.
    -   Inform the user about the temporary file creation.

3.  **- [ ] Validate Temporary Corpus:**
    -   **Instruction:** Run `cat profile/audit_corpus.json | tools/validate-json.sh`.
    -   If validation fails, report "AUDIT FAILED at corpus creation" and STOP.
    -   If it succeeds, report success and continue.

### Step 3: Run `job-scan`

**Instruction:** This step is unchanged. It tests if `job-scan` can correctly parse the sample job description.

1.  **- [ ] Execute `job-scan`:**
    -   Use the sample job description as input.
    -   Save the output to `research/openings/audit-innovate-senior-engineer.md`.
2.  **- [ ] Verify `job-scan` output:**
    -   Confirm the analysis file was created. If not, report failure and STOP.

### Step 4: Run Gap Analysis (from `tailor-resume`)

**Instruction:** This step tests the gap-analysis portion of the `tailor-resume` workflow. We execute Steps 1-2 of `tailor-resume` only, not the full interactive session.

1.  **- [ ] Execute gap analysis:**
    -   Load the temporary corpus (`profile/audit_corpus.json`) and the scanned job file (`research/openings/audit-innovate-senior-engineer.md`).
    -   Perform the "Detailed Gap Analysis" (Step 1 of `tailor-resume`): score each requirement against the corpus.
    -   Present the "Strategic Briefing" (Step 2 of `tailor-resume`): display the alignment score, strengths, and gaps.

2.  **- [ ] Stop and request verification:**
    -   After presenting the Strategic Briefing, **DO NOT** proceed to Step 3 (Assemble Draft) or Step 4 (Interactive Gap-Closing).
    -   Instead, explicitly ask the user to verify the analysis:
    ```
    --- AUDIT CHECKPOINT ---
    I've completed the gap analysis. Before continuing, please verify the results above.

    Press Enter to continue to verification questions, or type 'abort' to stop the audit.
    ```
    -   Wait for user input before proceeding to Step 5.

### Step 5: User Verification (New)

**Instruction:** Ask the user to review the "Strategic Briefing" from Step 4 and confirm its correctness.

**Ask these specific questions:**

1.  **"Did the 'Strategic Briefing' from the `tailor-resume` workflow run correctly?"**
2.  **"Does the initial Alignment Score seem correct?** The sample resume is a very strong match for the job description, so the score should be high (likely 80%+)."
3.  **"Was the Gap Analysis correct?** The briefing should have correctly identified that there are NO critical skill gaps."

If the user reports that the briefing was incorrect or did not run, this may indicate a problem with the `tailor-resume` workflow's initial analysis logic.

### Step 6: Cleanup

**Instruction:** This step is unchanged.

1.  **- [ ] Delete temporary files:**
    -   `rm profile/audit_corpus.json`
    -   `rm research/openings/audit-innovate-senior-engineer.md`
2.  **- [ ] Confirm cleanup:**
    -   "I have removed the temporary files created during the audit."

### Step 7: Report Final Result

**Instruction:** This step is unchanged. Based on the user's feedback, report the final pass/fail status of the audit.

-   **If user confirms everything looks good:** "Audit complete. The core `init` -> `job-scan` -> `tailor-resume` pipeline appears to be functioning correctly."
-   **If user reports issues:** "Audit complete. It seems there are some deviations in the workflow outputs."

---

## Output

This workflow creates temporary files for diagnostics and then cleans them up.

- `profile/audit_corpus.json` (deleted)
- `research/openings/audit-innovate-senior-engineer.md` (deleted)

## Recommend Next

After completing this workflow, suggest: **No recommendation.** This is a terminal, diagnostic workflow.
