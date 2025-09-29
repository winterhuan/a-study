# Daily Brief

Personalized daily news briefing based on your interests and current relevance.

## Process:

### 1. Interest Discovery

Launch interest-analyzer subagent to identify user's interests:

```text
Analyze all files in / to identify:
- Current projects and focus areas
- Technologies and tools being used
- Topics frequently mentioned
- Industries or domains of interest
- Personal goals and objectives

Return a structured list of interests with priority levels.
```

### 2. News Collection

Launch news-curator subagent with discovered interests:

```text
Search for news on these topics: [List of interests]

CRITICAL REQUIREMENTS:
- Only include news from THE LAST 7 DAYS
- Use date filters in all searches (e.g., "after:YYYY-MM-DD")
- Verify publication dates before including
- Filter for high relevance and actionability
- Include original publication dates
- Explain why each item matters to the user
```

### 3. Briefing Generation

Format the curated news into a daily brief:

- Group by relevance and priority
- Include publication dates prominently
- Add personal context for each item
- Suggest potential actions
- Highlight urgent/time-sensitive items

### 4. Output Organization

Save the briefing to `lifeOS/daily-brief/YYYY-MM-DD-brief.md` with:

- Clear sections by topic
- Publication dates for all items
- Why it matters to you
- Suggested actions
- Quick summary at the top

## Key Features:

- **Personalized**: Based on YOUR actual interests from your files
- **Current**: Only news from the last 7 days
- **Verified**: All dates checked before inclusion
- **Actionable**: Includes what you can do with the information
- **Contextual**: Explains relevance to your specific work/interests

## Important Notes:

- NEVER include outdated news (older than 7 days)
- ALWAYS verify publication dates
- ALWAYS use web search with date filters
- ALWAYS explain personal relevance
- FOCUS on actionable information
