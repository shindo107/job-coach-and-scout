---
name: tailor-resume
description: Tailor your resume for a specific job posting through interview-driven extraction. Creates a targeted resume and updates your corpus with new experiences.
argument-hint: [company-name]
---

# Tailor Resume Workflow

**Load and execute:** `workflows/tailor-resume/workflow.md`

Read the entire workflow file and execute it step by step. This workflow:

1. Loads your Resume Corpus and the parsed job posting
2. Assembles a draft resume from best-fit corpus content
3. Conducts interactive tailoring (the core interview process)
4. Probes for forgotten experiences and captures new accomplishments
5. Updates your corpus with confirmed new entries
6. Saves the tailored resume to applications/resumes/

This is the heart of Job Coach & Scout. Follow all steps exactly as written, especially the confirmation steps before saving new entries.

$ARGUMENTS
