# Job Coach and Scout

![Job Coach and Scout](jcas_final.jpg)

A **Claude Code workflow library** for job search preparation. Two AI personas guide you through resume tailoring, cover letter generation, and market research via interview-driven conversations.

## What This Is

This is **NOT** a standalone application. There is no CLI, no Python code, no installation required.

This is a collection of **workflow files** that Claude Code reads and executes directly. You talk to Claude Code in natural language, and it follows the workflow instructions.

**Requirements:**
- Claude Code (Claude Pro subscription)
- That's it. No dependencies, no API keys, no installation.

## How to Use

1. Open this project directory in Claude Code
2. Ask Claude Code to run a workflow using natural language

**Example invocations:**

| What you say | What happens |
|--------------|--------------|
| "Help me get started" | Runs the init workflow |
| "Run the scoping interview" | Captures your job search constraints |
| "Scan this job posting" | Parses and evaluates a job posting |
| "Tailor my resume for this job" | Interview-driven resume tailoring |
| "Review my resume" | Adversarial feedback on your master resume |
| "Write a cover letter" | Voice-matched cover letter generation |
| "Research fintech companies" | Market intelligence and company discovery |

## Available Workflows

### Setup & Onboarding

| Workflow | Purpose |
|----------|---------|
| **init** | Initialize project, import resume, collect writing samples |
| **scoping-interview** | Establish job search constraints and preferences |

### Resume Preparation

| Workflow | Purpose |
|----------|---------|
| **job-scan** | Parse job posting, extract requirements, quick-fit assessment |
| **evaluate-fit** | Cold, adversarial alignment scoring (read-only) |
| **fit-resume** | Interview-driven resume tailoring for specific job |
| **resume-review** | Adversarial review of master resume (no job context) |

### Application Materials

| Workflow | Purpose |
|----------|---------|
| **cover-letter** | Generate voice-matched cover letter |

### Research & Discovery

| Workflow | Purpose |
|----------|---------|
| **industry-research** | Analyze industries and verticals for your profile |
| **company-discovery** | Find and evaluate target companies |

## Agent Personas

### Max — Job Coach

A veteran recruiter with 15+ years experience. Adversarial by default, Max challenges vague claims, probes for forgotten experiences, and ensures every resume bullet can survive "tell me more about that."

### Scout — Job Scout

A strategic market intelligence analyst. Scout tracks hiring trends, evaluates companies, and surfaces opportunities that match your constraints.

## Directory Structure

```
job-coach-and-scout/
├── README.md                    # This file
├── .gitignore                   # Git ignore patterns
├── agents/                      # Agent persona definitions
│   ├── job-coach.md            # Max persona
│   └── job-scout.md            # Scout persona
│
├── workflows/                   # Workflow definitions
│   ├── init/                   # Project initialization
│   ├── scoping-interview/      # Constraint gathering
│   ├── job-scan/               # Job posting parsing
│   ├── evaluate-fit/           # Alignment scoring
│   ├── fit-resume/             # Resume tailoring
│   ├── resume-review/          # Master resume review
│   ├── cover-letter/           # Cover letter generation
│   ├── industry-research/      # Industry analysis
│   └── company-discovery/      # Company evaluation
│
├── profile/                     # Your data (created by init)
│   ├── resume.md               # Master resume
│   ├── constraints.yaml        # Job search constraints
│   └── writing_samples/        # Voice analysis samples
│
├── applications/                # Generated outputs
│   ├── resumes/                # Tailored resumes
│   └── cover_letters/          # Generated cover letters
│
└── research/                    # Market intelligence
    ├── industries.md           # Industry analysis
    ├── companies/              # Company profiles by industry
    └── openings/               # Parsed job postings
```

## Getting Started

1. **Initialize your project:**
   Ask Claude Code: "Help me set up my job search project"

2. **Complete the scoping interview:**
   Ask Claude Code: "Run the scoping interview"

3. **Start applying:**
   - Provide a job posting and ask Claude Code to tailor your resume
   - Or ask for a resume review to strengthen your baseline

## Privacy

- All data is stored locally in this project directory
- No telemetry, analytics, or external calls
- Data processed in Claude Code sessions is subject to Anthropic's data handling policies

## File Formats

| Data | Format | Location |
|------|--------|----------|
| Resume | Markdown | `profile/resume.md` |
| Constraints | YAML | `profile/constraints.yaml` |
| Tailored resumes | Markdown | `applications/resumes/{company}-{role}.md` |
| Cover letters | Markdown | `applications/cover_letters/{company}-{role}.md` |
| Research | Markdown | `research/` subdirectories |
