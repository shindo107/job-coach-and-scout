# Tailor Resume

## Summary

**Purpose:** Modify an existing resume to better fit a specific job posting, track three distinct fit scores (corpus fit, starting resume fit, final resume fit), and discover new corpus entries during the tailoring process.
**Agent:** Job Coach (Max)
**Reads:**
- **Starting resume** — An existing resume file to modify (required). Can be:
  - A previous tailored resume from `applications/resumes/`
  - A master resume from `profile/imports/`
  - Any resume file the user provides (PDF files are auto-converted to Markdown)
- `profile/corpus.json` — Resume Corpus (required)
- `research/openings/{company}-{role}.md` — Parsed job posting with fit score from job-scan (required)
- `profile/constraints.yaml` — For feedback style preference (optional)
**Creates:**
- `applications/resumes/{company}-{role}.md` — Tailored resume with fit score progression (starting → final).
- `profile/corpus.json` (updated) — Enriched with explicitly cataloged new accomplishments, variations, and skills discovered during tailoring.
**Key Metrics Tracked:**
- **Corpus Fit Score** — Theoretical maximum based on all corpus content
- **Starting Resume Fit Score** — The provided resume's alignment before modifications
- **Final Resume Fit Score** — Result after tailoring
- **Corpus Discoveries** — New accomplishments, variations, and skills added
**Prerequisites:** `job-scan` completed for the target posting; a starting resume to modify.

---

> **CORE WORKFLOW**: This is the heart of Job Coach & Scout. It begins with a detailed gap analysis and then uses an interview-driven model to extract forgotten experiences, close gaps, and position you as the ideal candidate.

**Trigger:** User says "help me tailor my resume for [company]", "tailor my resume", or after `job-scan` identifies a promising role.

## Persona

**Load and adopt:** `agents/job-coach.md`. Embody Max's expert, direct, and adversarial persona to guide the user through a rigorous tailoring session.

## Context Required

- **Starting resume file** (required) — The resume to modify
- `profile/corpus.json` (required)
- `research/openings/{company}-{role}.md` (required)
- `profile/constraints.yaml` (optional)

**If starting resume not specified:**
```
I need a starting resume to modify. Which resume should I use as the base?

**Available options:**
1. {List any files in applications/resumes/}
2. {List any files in profile/imports/}
3. Provide a path to another resume file

Which one should I start with?
```
- **Instruction:** List available resumes from `applications/resumes/*.md` and `profile/imports/*` (common formats: .md, .txt, .pdf).
- **Instruction:** If user provides a path, validate the file exists and is readable.
- **Note:** PDF files will be converted to Markdown before modification. The converted file is saved to `profile/imports/` for future use.

**If corpus doesn't exist:**
```
I need your Resume Corpus to draw from. I couldn't find `profile/corpus.json`.

Would you like to:
1. Run the init workflow to create your corpus
2. Provide the path to your resume file (I'll help import it)
```

**If job posting doesn't exist:**
```
I need a parsed job posting to tailor against. I couldn't find a posting in `research/openings/`.

Would you like to:
1. Run job-scan first to analyze a job posting
2. Specify which posting to use (provide filename)
```

## Session Continuity

**Claude Code conversation history automatically preserves your progress.** You can pause at any checkpoint and resume later:

- **To pause:** At any checkpoint, say "take a break" or simply close the session
- **To resume:** In the same Claude Code session, say "let's continue" or "where were we?"
- **To resume in a new session:** Say "continue tailor-resume for {company}" — Claude Code will reload context and ask where you left off

**Checkpoints are provided after each gap is addressed** (see Step 4d), summarizing:
- Which gap was just addressed
- What evidence was captured
- How many gaps remain

**Note:** If starting a completely new session, you may need to re-share any experiences discussed previously, as they exist only in conversation history.

---

## Steps

### Step 1: Load Starting Resume and Analyze

**Instruction:** This step loads the starting resume and conducts a thorough gap analysis before any modifications begin.

**1a. Load Starting Resume:**
- **Instruction:** Load the user-specified starting resume file.
- **Instruction:** Check the file extension to determine format.

**If the starting resume is a PDF (.pdf):**
- **Instruction:** PDFs cannot be directly modified. Convert to Markdown first:
  1. Read the PDF file using the Read tool (which supports PDF extraction)
  2. Parse the extracted content into clean Markdown format:
     - Use `#` headers for section titles (Experience, Education, Skills, etc.)
     - Use bullet points (`-`) for accomplishments
     - Preserve company names, titles, and dates
     - Format contact info at the top
  3. Save the converted Markdown to `profile/imports/{original-filename}.md`
  4. Inform the user:
     ```
     📄 Your PDF resume has been converted to Markdown for editing.

     **Original:** {path/to/resume.pdf}
     **Working copy:** profile/imports/{filename}.md

     I'll modify the Markdown version. You can review the conversion below.
     ```
  5. Show the converted Markdown for user approval before proceeding
  6. If user requests corrections to the conversion, make them before continuing
- **Instruction:** Use the converted Markdown file as the working copy for all subsequent steps.

**If the starting resume is already Markdown (.md) or plain text (.txt):**
- **Instruction:** Use the file directly as the working copy.

**After loading (all formats):**
- **Instruction:** Parse the resume content to identify:
  - Current positions and companies listed
  - Accomplishment bullets present
  - Skills section content
  - Education and certifications
- **Instruction:** Confirm the starting resume with the user:
  ```
  📄 Starting Resume: {filename}
  - Format: {PDF (converted to MD) | Markdown | Text}
  - Positions: {N} roles listed
  - Accomplishments: {M} bullets
  - Skills: {list or count}

  This is the resume I'll modify for {Company} - {Role}. Correct?
  ```

**1b. Load Supporting Context:**
- **Instruction:** Load `corpus.json` and the target `research/openings/{company}-{role}.md`.
- **Instruction:** Extract the MUST-HAVE and NICE-TO-HAVE requirements from the job posting file.

**1c. Score Starting Resume Against Requirements:**
- **Instruction:** For each job requirement, check if the **starting resume** (not the full corpus) contains evidence. Score each as:
  - Full Match (100%) — Clear, strong evidence present in the resume
  - Partial Match (50%) — Related experience but not directly stated
  - No Match (0%) — No relevant content in the resume
- **Instruction:** This produces the **Starting Resume Fit Score**.

**1d. Score Corpus Potential:**
- **Instruction:** For each requirement, also check the full `corpus.json` for additional evidence NOT currently in the starting resume.
- **Instruction:** This produces the **Corpus Fit Score** (theoretical ceiling).

**1e. Identify Improvement Opportunities:**
- **Instruction:** Compare the two scores to identify:
  - **Already covered:** Requirements met by the starting resume
  - **Corpus additions:** Requirements where corpus has evidence not in the resume (easy wins)
  - **Gaps to probe:** Requirements where neither resume nor corpus has strong evidence (need interview)

### Step 2: Present Strategic Briefing

**Instruction:** Present the findings from Step 1 as a "Strategic Briefing" to kick off the tailoring session. This establishes the baseline scores that will be improved during tailoring.

**2a. Display Dual Fit Scores:**
- **Instruction:** Present the TWO scores calculated in Step 1:
  1. **Corpus Fit Score** — The theoretical maximum alignment if we use ALL relevant content from your corpus. This represents your full potential for this role.
  2. **Starting Resume Fit Score** — The alignment of the resume you provided. This is your actual starting point.
- **Instruction:** Present the scores clearly:
  ```
  ## Strategic Briefing: {Company} - {Role}

  **Corpus Fit Score: {X}%** — Your full potential based on everything in your corpus
  **Starting Resume Fit Score: {Y}%** — Where your current resume stands

  The gap between these scores ({X-Y}%) represents improvement we can make by:
  - Adding content from your corpus that's not in this resume
  - Discovering new experiences through our interview
  ```

**2b. Display Verdict:**
- **Instruction:** Provide a qualitative assessment based on the starting resume fit score:
  - **80%+:** "Strong Starting Point — Minor tweaks needed"
  - **60-79%:** "Good Foundation — Some content to add or rephrase"
  - **40-59%:** "Significant Work Needed — We'll add corpus content and probe for more"
  - **<40%:** "Major Overhaul — This resume needs substantial modification for this role"

**2c. Summarize What's Working and What's Missing:**
- **Instruction:** Create three lists:
    - **Already Strong:** Requirements well-covered by the starting resume
    - **Easy Wins (from Corpus):** Requirements where your corpus has content not in this resume — we can add these directly
    - **Gaps to Probe:** Requirements where we need to interview you for new experiences

**2d. Set the Agenda:**
- **Example Dialogue (as Max):** "Alright, I've analyzed your starting resume against this role. It currently scores **{Y}%**. Your corpus ceiling is **{X}%**, so we have room to improve. Here's the plan: First, I'll suggest {N} additions from your corpus that will boost your score. Then we'll probe for {M} gaps where I don't have evidence yet. Let's start with the easy wins."

### Step 3: Apply Easy Wins from Corpus

**Instruction:** Before probing for new experiences, first improve the starting resume by adding relevant content that already exists in the corpus.

**3a. Present Corpus Additions:**
- **Instruction:** For each "Easy Win" identified in Step 2c, propose specific additions:
  ```
  ## Easy Wins: Content from Your Corpus

  I found {N} items in your corpus that would strengthen this resume:

  **1. Add to {Position} section:**
  Current: {existing bullet or "[no relevant bullet]"}
  Suggested: "{accomplishment from corpus}"
  Addresses: {requirement}

  **2. Add to Skills section:**
  Missing skill: {skill from corpus}
  Addresses: {requirement}

  ...

  Should I apply these additions? (Yes to all / Review one by one / Skip)
  ```

**3b. Apply Confirmed Additions:**
- **Instruction:** For each confirmed addition, modify the working copy of the resume.
- **Instruction:** Track what was added for the final summary.

**3c. Show Updated Score:**
- **Instruction:** After applying corpus additions, recalculate the fit score:
  ```
  ✓ Applied {N} additions from your corpus.

  **Updated Resume Fit Score: {Z}%** (was {Y}%, +{Z-Y}%)
  **Remaining gap to ceiling: {X-Z}%**

  Now let's probe for experiences to close the remaining gaps.
  ```

### Step 4: Interactive Gap-Closing Interview (CORE)

**Instruction:** This is the interactive interview where you address the "Gaps to Probe" — requirements where neither the starting resume nor corpus has strong evidence.

**4a. Address a Specific Gap:**
- **Example Dialogue (as Max):** "Let's focus on the first gap: the requirement for 'Experience with multi-threaded programming'. I don't see any accomplishments in your corpus that explicitly mention this. Tell me about a time you had to work on a project involving concurrency or parallelism, even if it wasn't the main focus."

**4b. Probe and Draft:**
- **Instruction:** Based on the user's story, probe for specifics, quantification, and outcomes.
- **Instruction:** Draft a new accomplishment bullet that directly addresses the gap. Read it back to the user for confirmation. "Here's how I'd phrase that for the resume: '{drafted bullet}'. Does that accurately capture it?"

**4c. Capture as New Corpus Entry:**
- **Instruction:** Once the user confirms the new accomplishment, create a new JSON object for it in your context/memory. Assign it a new `id` and link it to the appropriate `position_id`.

**4d. Repeat for all Major Gaps:**
- **Instruction:** Continue this process until all the major gaps identified in the strategic briefing have been addressed.

**4e. Checkpoint (after each gap):**
- **Instruction:** After addressing each gap, provide a checkpoint summary:
```
✅ Gap addressed: {requirement name}
   Evidence captured: {brief summary of new accomplishment}

Progress: {N} of {M} gaps addressed.
Remaining: {list of remaining gaps}

Ready to continue, or would you like to take a break?
```
- If user wants to pause, confirm their progress is saved in conversation history and they can resume with "let's continue".

### Step 5: Final Review

**Instruction:**
- After addressing the gaps, assemble the complete, tailored resume including both the original strengths and the newly created accomplishments.
- Present this final version to the user for their approval.

### Step 6: Confirm and Update Resume Corpus

**Instruction:** This step safely writes the improvements back to the central knowledge base and explicitly documents what was discovered.

**6a. Present Corpus Discoveries Summary:**
- **Instruction:** Before saving, present a clear summary of ALL new content discovered during the tailoring session:
  ```
  ## Corpus Discoveries During This Session

  **New Accomplishments Added:** {N}
  1. **{accomplishment_id}** — "{brief summary of bullet}"
     - Position: {company} - {title}
     - Skills tagged: {skill1}, {skill2}
     - Gap addressed: {requirement this closes}

  2. **{accomplishment_id}** — "{brief summary of bullet}"
     - Position: {company} - {title}
     - Skills tagged: {skill1}, {skill2}
     - Gap addressed: {requirement this closes}

  **New Variations Added:** {M}
  - {accomplishment_id}.var_{N}: Alternative phrasing for {context}

  **New Skills Identified:** {K}
  - {skill_name} (discovered from: {accomplishment_id})

  These entries will be available for ALL future applications, not just this one.
  ```

**6b. Confirm New Entries:**
- **Instruction:** Ask the user for explicit confirmation:
  ```
  Ready to add these {N} accomplishments, {M} variations, and {K} skills to your corpus?
  1. Yes, save all
  2. Let me review/edit first
  3. Skip corpus update (resume will still be saved)
  ```

**6c. Construct and Validate:**
- **Instruction:** Merge the confirmed entries into the corpus, save to a `.tmp` file, and validate it using `tools/validate-json.sh`.

**6d. Perform Atomic Write:**
- **Instruction:** If validation passes, perform the safe rename (`.bak`, then rename `.tmp`). Report success with specifics:
  ```
  ✓ Corpus updated successfully
  - Added: {N} accomplishments, {M} variations, {K} skills
  - Backup saved: profile/corpus.json.bak
  ```

### Step 7: Save Final Tailored Resume

**Instruction:** Save the tailored resume in both Markdown and PDF formats.

**7a. Save Markdown (required):**
- **Instruction:** Add a metadata header to the final markdown resume, including the final (improved) alignment score.
- **Instruction:** Save the file to `applications/resumes/{company}-{role}.md`.

**7b. Generate PDF (if tools available):**

1. **- [ ] Check PDF tool availability:**
   - Run: `./tools/check-pdf-tools.sh`
   - Parse the JSON output.

2. **- [ ] If PDF tools are available:**
   - Check if `profile/resume_template.yaml` exists.
   - Run the PDF generation command:
     ```bash
     python3 tools/generate-pdf.py \
       "applications/resumes/{company}-{role}.md" \
       "applications/resumes/{company}-{role}.pdf" \
       --template profile/resume_template.yaml
     ```
   - **If generation succeeds (exit code 0):**
     ```
     PDF resume generated: applications/resumes/{company}-{role}.pdf
     ```
   - **If generation fails (non-zero exit code):**
     ```
     PDF generation encountered an issue. Your Markdown resume was saved successfully.
     Error: {error message from command}

     You can retry manually:
     python3 tools/generate-pdf.py "applications/resumes/{company}-{role}.md" "applications/resumes/{company}-{role}.pdf"
     ```

3. **- [ ] If PDF tools are NOT available:**
   - Display graceful fallback message:
     ```
     Markdown resume saved. PDF generation skipped (no PDF tools installed).

     To enable PDF generation, install one of:
     - WeasyPrint (recommended): pip install weasyprint
     - Typst: https://typst.app/

     Then run manually:
     python3 tools/generate-pdf.py "applications/resumes/{company}-{role}.md" "applications/resumes/{company}-{role}.pdf"
     ```

4. **- [ ] If no template file exists:**
   - Use default template settings (built into generate-pdf.py).
   - Note in output:
     ```
     Note: Using default PDF template. Run /init with a PDF resume to create
     a custom template matching your resume's original styling.
     ```

### Step 8: Completion Summary & Recommendation

**Instruction:** Present a comprehensive summary showing the full journey from start to finish.

**Summary:**
```
## Tailoring Complete: {Company} - {Role}

### Starting Point
**Base resume:** {starting_resume_filename}

### Fit Score Progression
┌─────────────────────────────────────────────────────┐
│  Corpus Fit:        {X}%  ████████████░░  (ceiling) │
│  Starting Resume:   {Y}%  ██████████░░░░  (start)   │
│  Final Resume:      {Z}%  ████████████░░  (result)  │
└─────────────────────────────────────────────────────┘

**Improvement:** +{Z-Y}% from starting point
**vs Ceiling:**  {X-Z}% potential remains (if any)

### Changes Made to Starting Resume
**From corpus (easy wins):** {P} additions
**From interview (new discoveries):** {Q} additions
**Total modifications:** {P+Q}

### Corpus Discoveries (Reusable for Future Applications)
{N} new accomplishments added:
  • {brief description 1} → closes gap: {requirement}
  • {brief description 2} → closes gap: {requirement}
  • ...

{M} new variations added
{K} new skills identified

### Files Updated
- **Resume saved:** `applications/resumes/{company}-{role}.md`
- **PDF generated:** `applications/resumes/{company}-{role}.pdf` (if PDF tools available)
- **Corpus updated:** `profile/corpus.json` (+{N} accomplishments)
- **Backup created:** `profile/corpus.json.bak`
```

**Interpret the Scores:**
- **Instruction:** Provide context on what the scores mean:
  - If Final ≈ Corpus Fit: "You've maximized your potential for this role based on your current experience."
  - If Final < Corpus Fit by >10%: "There's still {X-Z}% untapped potential. Consider revisiting gaps you skipped or exploring deeper variations."
  - If Final improved significantly (>15%): "Great session! The new accomplishments we discovered significantly strengthened your positioning."

**Recommend Next:**
- **Instruction:** Suggest `cover-letter` as the logical next step: "Your tailored resume is ready at {Z}% fit. Shall we write a compelling cover letter to go with it?"
- **If corpus was significantly enriched:** Also mention: "The {N} new accomplishments we added will also strengthen your applications to similar roles."

## Output

**Files created/modified:**
- `profile/corpus.json` (updated with new experiences)
- `profile/corpus.json.bak` (backup of the previous version)
- `applications/resumes/{company}-{role}.md` (the tailored Markdown resume for this specific job)
- `applications/resumes/{company}-{role}.pdf` (PDF version, if PDF tools are available)

## Recommend Next

After this workflow completes successfully, suggest **cover-letter**.
