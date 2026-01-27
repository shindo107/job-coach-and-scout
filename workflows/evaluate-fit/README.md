# Evaluate Fit Workflow

Provides alignment scoring between a user's resume and job posting requirements.

## Alignment Score Thresholds

This workflow uses **evidence-based thresholds** derived from recruiting industry research. The thresholds reflect real-world hiring outcomes rather than arbitrary cutoffs.

### 5-Tier Scoring Scale

| Score | Verdict | Recommendation | Expected Outcome |
|-------|---------|----------------|------------------|
| **80-100%** | Excellent Fit | PROCEED | 2-3x higher interview callback rate |
| **70-79%** | Good Fit | PROCEED | Reliably passes ATS, reaches hiring managers |
| **60-69%** | Moderate Fit | PROCEED WITH CAUTION | Minimum competitive threshold |
| **50-59%** | Weak Fit | STRETCH | Possible but requires extra effort |
| **Below 50%** | Poor Fit | RECONSIDER | ~90% rejection rate |

### Research Sources

The thresholds above are based on the following industry research:

#### 80%+ Threshold (Excellent Fit)

> "For most clients, a job fit score of 80 percent reveals a candidate with a high probability of success."
> — [ERE: Why Good Candidates Fail](https://www.ere.net/articles/why-good-candidates-fail-beware-the-90-percent-job-fit)

> "Candidates whose resumes score 80% or higher on a job-match analysis receive 2-3x more interview callbacks than those below the threshold."
> — [Jobscan](https://www.jobscan.co/blog/what-jobscan-match-rate-should-i-aim-for/)

#### 70%+ Threshold (Good Fit)

> "Experts suggest aiming for a match rate of 70% or higher. Research indicates that resumes achieving this threshold are more likely to bypass ATS filters and reach hiring managers."
> — [Parkes Career Services](https://www.parkescareerservices.com/post/decoding-ats-what-percentage-must-your-resume-match-to-get-noticed)

#### 60% Threshold (Moderate Fit)

> "Many employers would prefer to hire a candidate who is 60 percent qualified and accompanied by a solid recommendation rather than a 'perfect' candidate with no one to vouch for them."
> — [InHerSight: Why 60% Qualified Is Enough](https://www.inhersight.com/blog/insight-commentary/why-60-percent-qualified-is-enough)

#### 50% Threshold (Weak Fit / Stretch)

> "The jobs search site TalentWorks found candidates were 'just as likely to get an interview matching 50 percent of requirements as you are 90 percent or more.'"
> — [CNBC](https://www.cnbc.com/2018/12/12/matching-half-of-a-jobs-requirements-might-still-get-you-an-interview.html)

This surprising finding suggests that once candidates cross a minimum threshold, soft factors (referrals, cover letters, interview skills) become more important than incremental match percentage. This is why we include a "STRETCH" tier rather than immediately discouraging candidates at 50%.

#### Below 50% Threshold (Poor Fit)

> "Below 60 percent indicates a high rate of failure."
> — [ERE](https://www.ere.net/articles/why-good-candidates-fail-beware-the-90-percent-job-fit)

> "Resumes with Job Match Score below 60 are rejected by human reviewers about 90% of the time."
> — [Jobscan](https://www.jobscan.co/blog/what-jobscan-match-rate-should-i-aim-for/)

### Why These Thresholds Matter

1. **ATS Reality**: ~70% of resumes are rejected by Applicant Tracking Systems before human review. Optimizing for keyword match is crucial.

2. **Human Review**: Even after passing ATS, human reviewers quickly screen for qualification fit. Sub-60% match rates have ~90% rejection.

3. **Soft Factors**: The 50% TalentWorks finding reveals that referrals, cover letters, and interview performance can offset qualification gaps — but only above a minimum threshold.

4. **Honesty Over Encouragement**: This workflow uses Max (Job Coach) persona, which prioritizes honest assessment over false encouragement. The thresholds reflect real hiring outcomes, not aspirational targets.

### Threshold Adjustments

The MUST-HAVE gap count adjusts recommendations within tiers:

| MUST-HAVE Gaps | Effect |
|----------------|--------|
| 0-1 gaps | Recommendation stays at score-based tier |
| 2 gaps | Drops to PROCEED WITH CAUTION |
| 3 gaps | Drops to STRETCH |
| 4+ gaps | Drops to RECONSIDER |

This reflects that missing critical requirements has outsized impact on candidacy, regardless of overall percentage match.

## Related Workflows

- **job-scan** (upstream): Creates the parsed job posting this workflow evaluates against
- **tailor-resume** (downstream): Uses evaluate-fit scoring during iterative resume tailoring
