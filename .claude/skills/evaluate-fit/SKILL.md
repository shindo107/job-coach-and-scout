---
name: evaluate-fit
description: Assess alignment between your Resume Corpus and a job posting. Provides honest scoring and gap analysis without modifying any files.
disable-model-invocation: true
argument-hint: [company-name]
---

# Evaluate Fit Workflow

**Load and execute:** `workflows/evaluate-fit/workflow.md`

Read the entire workflow file and execute it step by step. This workflow:

1. Loads your Resume Corpus and the parsed job posting
2. Queries corpus for evidence against each requirement
3. Scores requirements (full match, partial match, no match)
4. Calculates overall alignment score
5. Generates gap analysis with strengths and critical gaps
6. Delivers Max's adversarial assessment and recommendation

This is a read-only assessment displayed in conversation only. No files are created or modified.

$ARGUMENTS
