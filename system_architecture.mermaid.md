# System Architecture Diagram

> **IMPORTANT:** This file is the authoritative source for the system diagram. After ANY changes:
> 1. Run `python3 tools/validate-diagram.py` to validate against workflow/agent files
> 2. Copy the mermaid block to README.md (validation will fail if they differ)

## Schema

<!--
  Machine-parseable tables defining the diagram structure.
  Validation script cross-references these against workflow Summary blocks.
  Run: python3 tools/validate-diagram.py
-->

### Agents

| id | style | color | label | source |
|----|-------|-------|-------|--------|
| max | maxStyle | #ff6b35 | AGENT MAX — Resume Tailoring & Feedback | agents/job-coach.md |
| scout | scoutStyle | #00b4d8 | AGENT SCOUT — Market Research & Discovery | agents/job-scout.md |
| voice | voiceStyle | #9b59b6 | VOICE — Authentic Writing Style | agents/voice.md |
| dual | dualStyle | #7b4b94 | Both Agents | — |

### Data Stores

| id | type | path | label |
|----|------|------|-------|
| corpus | central | profile/corpus.json | RESUME CORPUS |
| constraints | file | profile/constraints.yaml | constraints.yaml |
| voice_profile | file | profile/voice_profile.json | voice_profile.json |
| voice_agent | file | agents/voice.md | voice.md |
| resume_template | file | profile/resume_template.yaml | resume_template.yaml |
| linkedinmd | file | profile/linkedin.md | linkedin.md |
| market_skills | file | research/market_skills.json | market_skills.json |
| industries | directory | research/industries/ | industries/ |
| companies | directory | research/companies/ | companies/ |
| openings | directory | research/openings/ | openings/ |
| resumes | directory | applications/resumes/ | resumes/ |
| coverletters | directory | applications/cover_letters/ | cover_letters/ |

### Workflows

| id | phase | agents | lead | source |
|----|-------|--------|------|--------|
| init | setup | max, scout | max | workflows/init/workflow.md |
| scoping | setup | max, scout | max | workflows/scoping-interview/workflow.md |
| create_voice | setup | scout | — | workflows/create-voice/workflow.md |
| industry | research | scout | — | workflows/industry-research/workflow.md |
| company | research | scout | — | workflows/company-discovery/workflow.md |
| jobscan | research | scout | — | workflows/job-scan/workflow.md |
| tailor | apply | max | — | workflows/tailor-resume/workflow.md |
| cover | apply | voice, max | voice | workflows/cover-letter/workflow.md |
| corpus_rev | standalone | max, scout | max | workflows/corpus-review/workflow.md |
| linkedin | standalone | voice, max | voice | workflows/linkedin-review/workflow.md |
| audit | system | max, scout | — | workflows/audit/workflow.md |

### Data Flows

<!-- Legend: ? = optional/conditional, — = none -->

| workflow | reads | writes | updates |
|----------|-------|--------|---------|
| init | — | corpus, market_skills, resume_template? | — |
| scoping | corpus | constraints | corpus? |
| create_voice | writing_samples | voice_profile, voice_agent | — |
| industry | corpus, constraints, industries? | industries, companies | constraints? |
| company | corpus, constraints, industries, companies? | companies | — |
| jobscan | corpus, constraints, market_skills, openings?, companies? | openings | market_skills, companies? |
| tailor | corpus, constraints?, openings, resume_template?, resumes? | resumes | corpus |
| cover | corpus, constraints, voice_agent?, voice_profile?, openings, resumes? | coverletters | voice_profile?, voice_agent? |
| corpus_rev | corpus, market_skills, constraints? | — | corpus |
| linkedin | corpus, constraints?, voice_agent?, voice_profile?, linkedinmd? | linkedinmd | corpus |
| audit | — | — | — |

---

## Diagram

```mermaid
flowchart TB
    %% Styling
    classDef maxStyle fill:#ff6b35,stroke:#ff6b35,color:#fff
    classDef scoutStyle fill:#00b4d8,stroke:#00b4d8,color:#fff
    classDef voiceStyle fill:#9b59b6,stroke:#9b59b6,color:#fff
    classDef dualStyle fill:#7b4b94,stroke:#7b4b94,color:#fff
    classDef coreData fill:#ffd166,stroke:#ff6b35,color:#000
    classDef intermediateData fill:#90be6d,stroke:#43aa8b,color:#000
    classDef outputData fill:#f8961e,stroke:#f3722c,color:#000

    %% ===== ENTRY =====
    USER([User])

    %% ===== SETUP LANE (Purple) =====
    subgraph SETUP["🟣 SETUP"]
        init[init]
        init ==> scoping[scoping-interview]
        scoping -.->|optional| create_voice[create-voice]
    end

    %% ===== SYSTEM (Standalone) =====
    subgraph SYSTEM["🟣 SYSTEM"]
        audit[audit]
    end

    %% ===== CORE DATA =====
    subgraph CORE["CORE DATA"]
        CORPUS[(CORPUS)]
        constraints[constraints.yaml]
        voice_profile[voice_profile.json]
        voice_agent[voice.md]
        resume_template[resume_template.yaml]
    end

    %% ===== RESEARCH LANE (Teal) =====
    subgraph RESEARCH["🔵 SCOUT — Research"]
        industry[industry-research]
        industry ==> company[company-discovery]
        company ==> jobscan[job-scan]
    end

    %% ===== INTERMEDIATE DATA =====
    subgraph INTERMEDIATE["INTERMEDIATE DATA"]
        market_skills[market_skills.json]
        industries[industries/]
        companies[companies/]
        openings[openings/]
    end

    %% ===== APPLY LANE =====
    subgraph APPLY["APPLY"]
        subgraph MAX_APPLY["🟠 MAX"]
            tailor[tailor-resume]
        end
        subgraph VOICE_APPLY["🟣 VOICE"]
            cover[cover-letter]
        end
    end

    %% ===== OUTPUTS =====
    subgraph OUTPUTS["OUTPUTS"]
        resumes[resumes/]
        coverletters[cover_letters/]
    end

    %% ===== STANDALONE LANE =====
    subgraph STANDALONE["STANDALONE"]
        subgraph MAX_STANDALONE["🟠 MAX"]
            corpus_rev[corpus-review]
        end
        subgraph VOICE_STANDALONE["🟣 VOICE + MAX"]
            linkedin[linkedin-review]
        end
    end

    %% ===== STANDALONE OUTPUTS =====
    subgraph STANDALONE_OUT["STANDALONE OUTPUTS"]
        linkedinmd[linkedin.md]
    end

    %% ===== FINAL =====
    OUTPUT([Job Applications])

    %% ===== FLOW: Setup creates foundation =====
    USER ==> SETUP
    init -->|creates| CORPUS
    init -.->|seeds| market_skills
    init -.->|optional| resume_template
    scoping -->|writes| constraints
    scoping -.->|updates| CORPUS
    create_voice -->|writes| voice_profile
    create_voice -->|writes| voice_agent

    %% ===== FLOW: Research reads CORE, writes INTERMEDIATE =====
    CORPUS -.->|read by| industry
    constraints -.->|read by| industry
    industry -->|writes| industries
    industries -.->|read by| company
    company -->|writes| companies
    jobscan -->|writes| openings
    jobscan -.->|updates| market_skills

    %% ===== FLOW: Apply reads CORE + INTERMEDIATE, writes OUTPUTS =====
    openings -.->|read by| tailor
    openings -.->|read by| cover
    resume_template -.->|read by| tailor
    voice_agent -.->|read by| cover
    voice_profile -.->|read by| cover
    tailor -->|writes| resumes
    tailor -.->|updates| CORPUS
    cover -->|writes| coverletters

    %% ===== FLOW: Standalone reads and updates =====
    USER -.-> STANDALONE
    USER -.-> SYSTEM
    CORPUS -.->|read by| corpus_rev
    market_skills -.->|read by| corpus_rev
    corpus_rev -.->|updates| CORPUS
    CORPUS -.->|read by| linkedin
    constraints -.->|read by| linkedin
    voice_agent -.->|read by| linkedin
    linkedin -->|writes| linkedinmd
    linkedin -.->|updates| CORPUS

    %% ===== FLOW: To final output =====
    OUTPUTS ==> OUTPUT
    STANDALONE_OUT ==> OUTPUT

    %% ===== APPLY STYLES =====
    class tailor,corpus_rev maxStyle
    class init,scoping,audit dualStyle
    class industry,company,jobscan scoutStyle
    class cover,linkedin,create_voice voiceStyle
    class CORPUS,constraints,voice_profile,voice_agent,resume_template coreData
    class market_skills,industries,companies,openings intermediateData
    class resumes,coverletters,linkedinmd outputData
```

---

## Legend

| Element | Meaning |
|---------|---------|
| 🟠 Orange | MAX workflows (Resume Tailoring & Feedback) |
| 🔵 Teal | SCOUT workflows (Market Research & Discovery) |
| 🟣 Purple | VOICE workflows (Authentic Writing Style) or SETUP (Dual-agent) |
| 🟡 Yellow | Core Data — foundational profile (corpus, constraints, voice, template) |
| 🟢 Green | Intermediate Data — research artifacts (industries, companies, openings) |
| 🟧 Orange | Outputs — final deliverables (resumes, cover letters, LinkedIn) |
| **Thick arrows** | Workflow handoffs (sequence between workflows) |
| Solid arrows | Data writes (workflow creates/updates data) |
| Dashed arrows | Data reads or optional/conditional flows |

## Rendering

This diagram renders in:
- GitHub (native Mermaid support)
- VS Code (with Mermaid extension)
- Obsidian
- [Mermaid Live Editor](https://mermaid.live)
