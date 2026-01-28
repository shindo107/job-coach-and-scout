---
name: init
description: Initialize your job search project. Imports your resume(s), creates the Resume Corpus, and sets up directory structure.
disable-model-invocation: true
argument-hint: [resume-file-path]
---

# Init Workflow

**Load and execute:** `workflows/init/workflow.md`

Read the entire workflow file and execute it step by step. This workflow:

1. Introduces both agents (Max and Scout)
2. Obtains privacy agreement before processing personal data
3. Sets up directory structure (profile/, applications/, research/)
4. Imports resume(s) and creates the structured Resume Corpus
5. Optionally imports writing samples for voice matching
6. Suggests running scoping-interview next

Follow all steps exactly as written. Wait for user input where the workflow specifies interaction points.

$ARGUMENTS
