# Corpus Review

## Summary

**Purpose:** Strengthen your Resume Corpus by analyzing it against real-world market data and closing strategic gaps.
**Agent:** Job Coach (Max) & Job Scout
**Agent Lead:** Max (Scout leads market analysis, Max leads interactive gap-closing)
**Phase:** standalone
**Reads:**
- `profile/corpus.json` — Your structured Resume Corpus (required)
- `research/market_skills.json` — The database of skills seen in jobs you have scanned (required for market analysis)
- `profile/constraints.yaml` (optional) — For feedback style preference
**Creates:** None
**Updates:**
- `profile/corpus.json` — Updated with improved and new entries
**Prerequisites:** `init` completed. `job-scan` should be run on several jobs for a meaningful market analysis

---

**Trigger:** User says "review my resume", "improve my resume", or "review my corpus".

## Persona

**Load and adopt:** `agents/job-coach.md` AND `agents/job-scout.md`

**Role assignment:**
- **Scout** leads Step 2 (Market-Aware Corpus Analysis) — analyzing `market_skills.json`, identifying demand patterns, presenting the market alignment briefing
- **Max** leads Step 3 (Interactive Gap-Closing) — probing for experiences, drafting accomplishments, challenging weak bullets

Transition naturally between personas based on the task at hand.

## Steps

### Step 1: Load Context and Set Expectations

**Instruction:**
- Load `profile/corpus.json`, `profile/constraints.yaml`, and `research/market_skills.json`.
- If `market_skills.json` is missing or empty, inform the user that you can perform a content review for weak bullets, but for a true strategic review, they should scan a few target job descriptions first using the `job-scan` workflow.
- **Instruction (as Max):** Introduce the purpose of the review: to strategically strengthen their core career story against real-world market demands, not just to polish bullet points.

### Step 2: Market-Aware Corpus Analysis

**Instruction:** This step is the core of the new, strategic review.

**2a. Analyze Market Demand:**
- **Instruction:** Analyze `research/market_skills.json` to identify the most frequently occurring "MUST-HAVE" skills. These are the "High-Demand Skills".

**2b. Analyze Corpus Coverage:**
- **Instruction:** For each "High-Demand Skill", analyze `profile/corpus.json` to determine the user's coverage. Check for the skill in the top-level `skills` array and, more importantly, in the `skills_tags` and `content` of the `accomplishments`.
- **Instruction:** Categorize the coverage for each High-Demand Skill as "Strong" (multiple, quantifiable accomplishments), "Weak" (mentioned but accomplishments are vague or unquantified), or "Missing" (no evidence in the corpus).

**2c. Present Market Alignment Briefing:**
- **Instruction:** Present a summary of the analysis to the user. This is the agenda for the review session.
- **Example Dialogue:** "I've analyzed your corpus against the data from jobs you've scanned. Here's the market alignment:
    - ✅ **High Demand, Strong Coverage:** You have great stories for 'Python' and 'AWS', which are consistently requested.
    - ⚠️ **High Demand, Weak Coverage:** The market is asking for 'Terraform', and while you list it as a skill, your accomplishments don't prove you've used it effectively.
    - 🚨 **CRITICAL GAP:** 'Go' is a MUST-HAVE in 60% of the senior roles you've scanned, but it's completely missing from your corpus. This is our top priority to fix."

### Step 3: Interactive Strategic Gap-Closing

**Instruction:** Focus the interactive session on closing the gaps identified in Step 2, starting with the most critical.

**3a. Address a Strategic Gap:**
- **Instruction:** Pick the top "CRITICAL GAP" or "Weak Coverage" skill.
- **Example Dialogue:** "Let's tackle the 'Go' gap. It's the biggest disconnect between your profile and the market. I know it's not on your resume, but think back to your time at {Company}. Were there any side projects, internal tools, or prototypes where you used Go, even briefly? Or perhaps you worked on a project that was later rewritten in Go? We need to find a story here."

**3b. Probe, Draft, and Capture:**
- **Instruction:** As the user tells a story, probe for details, quantification, and impact.
- **Instruction:** Draft a new accomplishment bullet that directly addresses the market demand. Read it back for confirmation.
- **Instruction:** Once confirmed, create the new accomplishment object in memory to be added to the corpus.

**3c. Fortify Weak Coverage:**
- **Instruction:** For skills with "Weak Coverage," review the existing accomplishments.
- **Example Dialogue:** "Let's look at this 'Terraform' bullet point: 'Responsible for infrastructure as code'. It's too vague. What kind of infrastructure? How many resources? Did you improve deployment time? Reduce costs? Let's add the proof."
- **Instruction:** Based on the user's answers, create a `variation` of the existing accomplishment with the new, stronger phrasing.

**3d. Repeat for all Major Gaps:**
- **Instruction:** Continue this process until the most significant market gaps are addressed.

### Step 4: Confirm and Update Resume Corpus

**Instruction:** This step is identical to the safe-write process in other workflows.

**4a. Confirm New Entries:**
- **Instruction:** Summarize all new and improved accomplishments and get the user's final approval.

**4b. Construct, Validate, and Write:**
- **Instruction:** Merge the new entries into the corpus object, save to a `.tmp` file, validate with `tools/validate-json.sh`, and perform the atomic write by renaming files. Report success.

### Step 5: Completion Summary

**Summary:**
```
## Strategic Corpus Review Complete!

Your Resume Corpus is now more closely aligned with market demands.

- **Strategic Gaps Closed:** {count} (e.g., Added new accomplishments for 'Go' and 'Terraform')
- **Accomplishments Strengthened:** {count}

Your core career story is now better positioned to meet what recruiters are looking for.
```

**Recommend Next:**
- **Instruction:** Suggest `tailor-resume` as the immediate next step to apply the newly strengthened corpus. "Your corpus is now much stronger. Let's put it to use immediately by running `tailor-resume` for that {Company} role."
