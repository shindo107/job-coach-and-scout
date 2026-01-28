---
name: job-scan
description: Parse a job posting into structured requirements. Extracts must-haves, nice-to-haves, and company signals for fit analysis.
disable-model-invocation: true
argument-hint: [job-url-or-file]
---

# Job Scan Workflow

**Load and execute:** `workflows/job-scan/workflow.md`

Read the entire workflow file and execute it step by step. This workflow:

1. Obtains job posting content (URL, file, or pasted text)
2. Extracts company information and role details
3. Categorizes requirements into MUST-HAVE and NICE-TO-HAVE
4. Identifies hidden requirements and company signals
5. Saves parsed posting to research/openings/

Follow all steps exactly as written. Embody Scout's analytical approach throughout.

$ARGUMENTS
