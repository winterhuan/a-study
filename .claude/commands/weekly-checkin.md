# Weekly Check-in

Perform a comprehensive weekly check-in by intelligently discovering and tracking relevant metrics.

## Process:

### 1. Context Discovery

Analyze the entire project context to understand what matters:

- Read `CLAUDE.md` to understand the user and their projects
- Scan `lifeOS/business/`, `lifeOS/docs/`, or similar folders for context
- Look for existing metrics in `lifeOS/metrics/metrics-history.md`
- Identify the type of work/business

### 2. Metric Identification

Based on context analysis, determine relevant metrics. Examples:

**For Creators:**

- Followers/Subscribers
- Views/Impressions
- Engagement rate
- Revenue/Sponsorships

**For SaaS/Products:**

- MRR/ARR
- User count
- Churn rate
- Growth rate

**For Developers:**

- GitHub stars
- Commits/PRs
- Downloads
- Active projects

**For Students/Learners:**

- Courses completed
- Study hours
- Projects finished
- Skills acquired

### 3. Data Collection

Ask the user for current values of the discovered metrics:

```text
Based on your [type] work, let's track this week's progress:
1. [Specific metric 1]:
2. [Specific metric 2]:
3. [Specific metric 3]:
...
```

### 4. Analysis & Reporting

- Read previous data from `lifeOS/metrics/metrics-history.md`
- Update the metrics history with new data
- Launch metrics-analyst subagent with:

  ```text
  Analyze this week's metrics:
  Current: [provide current metrics]
  Previous: [provide last week's metrics]
  Historical: [provide trend data if available]

  Generate visual analysis with growth rates, trends, and recommendations.
  ```

### 5. Output Organization

- Update `lifeOS/metrics/metrics-history.md` with new data
- Save detailed report to `lifeOS/metrics/weekly-report-YYYY-MM-DD.md`
- Provide summary with key insights to user

## Important Notes:

- DO NOT use generic templates - discover what's relevant for THIS user
- Adapt metrics based on actual project context
- Focus on actionable insights, not just data collection
- Make reports visual and encouraging
