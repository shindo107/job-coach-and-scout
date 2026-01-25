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

### Step 1: Load Context

1.  **- [ ] Load files:**
    -   Load `profile/corpus.json`. If it's missing or invalid, stop and guide the user to run `init`.
    -   Load `research/openings/{company}-{role}.md` (the parsed job posting).
    -   Load `profile/constraints.yaml` if available for feedback style.
2.  **- [ ] Extract requirements:**
    -   Extract the MUST-HAVE and NICE-TO-HAVE requirements from the job posting file.

### Step 2: Assemble Draft Resume from Corpus

1.  **- [ ] Query Corpus for Best-Fit Content:**
    -   **Instruction:** "Based on the job requirements, find the best content in `profile/corpus.json` to create a draft resume. For each requirement, search the `accomplishments` and `skills` arrays."
    -   **Instruction:** "Prioritize `accomplishments` that have matching `skills_tags` or where the `content` semantically matches the requirement. Select the strongest, most relevant accomplishments for each past `position`."

2.  **- [ ] Assemble Draft:**
    -   **Instruction:** "Assemble a draft resume in Markdown format. Use the selected skills and accomplishments, grouped under their respective job positions. This draft is our starting point for tailoring."

### Step 3: Interactive Tailoring & Corpus Expansion (CORE)

This is the interactive interview where you and Max refine the resume and expand the corpus.

**Instruction for the LLM (Max):**
"You will now guide the user through the draft resume, section by section. Your goal is to tailor the content for the specific job and capture any new experiences or improved phrasing back into the corpus."

1.  **- [ ] Review and Refine Accomplishments:**
    -   **Max:** "Here are the experiences I've pulled from your corpus for your time at [Company]. Which of these are most relevant for this role?"
    -   **(Present selected accomplishments for a position.)**
    -   **Max:** "Is the wording on this strong enough? How could we make it better?"
    -   **If user rephrases an accomplishment:**
        -   **Instruction:** "The user has rephrased an accomplishment. Treat this as a `variation`. Create a new variation object for the corresponding accomplishment in the corpus. Give it a new unique ID (e.g., `var_...`)."
        -   **(Keep the new JSON object in your context/memory.)**
    -   **If user wants to add a new accomplishment:**
        -   **Max:** "It sounds like you have an experience that's not in your corpus yet. Let's capture it. Tell me more about that."
        -   **(Probe for specifics, quantification, and outcome, just like the old workflow).**
        -   **Instruction:** "Once you have the details, create a brand new `accomplishment` JSON object. Give it a unique ID, link it to the correct `position_id`, and infer the `skills_tags` and `metrics` from the conversation."
        -   **(Keep the new JSON object in your context/memory.)**

2.  **- [ ] Repeat for all relevant positions and sections.**

3.  **- [ ] Final Review:**
    -   **Max:** "Okay, I've integrated your changes. Here is the final tailored resume for this role. Does this look right?"
    -   **(Display the complete, tailored Markdown resume.)**

### Step 4: Update and Validate Resume Corpus

This step safely writes the improvements back to your central knowledge base.

1.  **- [ ] Construct New Corpus:**
    -   **Instruction:** "Load the original `profile/corpus.json` again. Merge the new `accomplishment` and `variation` objects you created during Step 3 into the appropriate arrays in the JSON structure."

2.  **- [ ] Save to Temporary File:**
    -   Save the complete, new JSON structure to a temporary file: `profile/corpus.json.tmp`.

3.  **- [ ] Validate New Corpus:**
    -   **Instruction:** "Run the validator script: `cat profile/corpus.json.tmp | tools/validate-json.sh`."
    -   **If validation fails:**
        -   Report the error. "I've encountered an issue trying to save your new experiences to the corpus. The error is: [stderr]. I will abort the save to prevent corruption, but your tailored resume for this application will still be saved."
        -   **STOP** the corpus update process but proceed to Step 5.
    -   **If validation succeeds:** Proceed to the next step.

4.  **- [ ] Perform Atomic Write:**
    -   **Instruction:** "The new corpus is valid. Now, perform a safe replacement."
    -   1. Rename `profile/corpus.json` to `profile/corpus.json.bak` (create a backup).
    -   2. Rename `profile/corpus.json.tmp` to `profile/corpus.json`.
    -   Report success: "Your Resume Corpus has been successfully updated with the new experiences from this session."

### Step 5: Save Final Tailored Resume

1.  **- [ ] Save Markdown Resume:**
    -   Take the final, tailored Markdown resume from the end of Step 3.
    -   Add a metadata header to it (similar to the old workflow, noting the final score if `evaluate-fit` logic was used).
    -   Save the file to `applications/resumes/{company}-{role}.md`.
    -   Confirm: "Your tailored resume for this role has been saved to `applications/resumes/{company}-{role}.md`."

### Step 6: Completion Summary & Recommendation

**(This section is similar to the old workflow, but focuses on the dual success: tailoring the resume AND improving the corpus.)**

**Summary:**
```
## Tailoring Complete!

Your resume has been tailored for {Company} and saved.

More importantly, your central Resume Corpus has been updated with {X} new accomplishments and {Y} improved variations, making your knowledge base even stronger for future applications.

**File saved:** `applications/resumes/{company}-{role}.md`
**Corpus updated:** `profile/corpus.json`
```

**Recommend Next:**
"Your resume is now tailored for {Company}. The logical next step is to generate a cover letter that complements it. Would you like to start the cover-letter workflow now?"

**(Handle user response as before.)**

## Output

**Files created/modified:**
- `profile/corpus.json` (updated with new experiences)
- `profile/corpus.json.bak` (backup of the previous version)
- `applications/resumes/{company}-{role}.md` (the tailored Markdown resume for this specific job)

## Recommend Next

After this workflow completes successfully:

1. **Suggest:** cover-letter
   **Rationale:** "Resume tailored! Let's write a matching cover letter."
   **Context to pass:** `applications/resumes/{company}-{role}.md` (the tailored resume), `research/openings/{company}-{role}.md` (job posting).
