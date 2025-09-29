# Newsletter Research

Comprehensive newsletter research and draft creation system.

## Process:

1. **Source Discovery**
   - Check `lifeOS/newsletter/sources/` for newsletter URLs
   - If not found, ask user for competitor newsletter URLs
   - Also look for user's own newsletter URL for voice analysis

2. **Content Fetching**
   - Fetch recent posts from all provided newsletter URLs
   - Extract key content, themes, and writing styles

3. **Research Phase**
   - Launch content-researcher subagent with:

     ```text
     Analyze these newsletters for trends and opportunities:
     [Provide all fetched content]

     Focus on:
     - Trending topics across multiple newsletters
     - Content gaps and opportunities
     - Time-sensitive angles
     - Writing style patterns
     ```

4. **Writing Phase**
   - After receiving research insights, launch newsletter-writer subagent:

     ```
     Create a newsletter draft based on these insights:
     [Provide research findings]

     Also analyze writing voice from:
     [User's existing content in lifeOS/]

     Requirements:
     - 3 compelling subject lines
     - 500-800 word draft
     - Match user's voice
     - Include practical takeaways
     ```

5. **Output Organization**
   - Save research report to `lifeOS/newsletter/research/YYYY-MM-DD-analysis.md`
   - Save draft to `lifeOS/newsletter/drafts/YYYY-MM-DD-draft.md`
   - Save metrics to `lifeOS/metrics/newsletter-metrics.md`

## Key Features:

- Trend analysis across multiple sources
- Voice matching from user's content
- Complete drafts, not outlines
- Value-first, authentic content
- Curiosity-driven subject lines
