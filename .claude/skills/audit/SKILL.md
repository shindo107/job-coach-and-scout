---
name: audit
description: Run a system audit to verify core workflows are functioning correctly. Uses sample data to test the `init` -> `job-scan` -> `tailor-resume` pipeline.
---

# Audit Workflow

**Load and execute:** `workflows/audit/workflow.md`

Read the entire workflow file and execute it step by step. This workflow:

1. Loads sample resume and job description.
2. Creates a temporary corpus to test parsing logic.
3. Runs `job-scan` on the sample job description.
4. Runs `tailor-resume` to test the gap analysis and tailoring kickoff.
5. Reports results and guides cleanup of temporary files.

This is a diagnostic workflow. Follow all steps exactly as written and report any failures clearly.
