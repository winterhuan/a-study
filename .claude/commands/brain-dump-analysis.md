# Brain Dump Analysis

Extract profound insights from your stream-of-consciousness writing.

## Process:

### 1. Folder Discovery

- Check if `lifeOS/braindumps/` exists
- If not, create it and guide user to add brain dump files
- Scan for all text files (.txt, .md) in the folder

### 2. Content Reading

- Read all brain dump files from `lifeOS/braindumps/`
- Preserve original formatting and voice
- Note timestamps if available in filenames or content

### 3. Insight Extraction Phase

Launch insight-extractor subagent with:

```
Analyze these brain dumps for deep patterns:
[Provide all brain dump content]

Focus on:
- Recurring themes and obsessions
- Evolution of thinking over time
- Hidden connections between ideas
- Key questions being explored
- Breakthrough moments and realizations
- Use the author's exact words when possible
```

### 4. Analysis Phase

After receiving extracted insights, launch brain-dump-analyst subagent:

```
Create a comprehensive analysis from these insights:
[Provide extracted patterns and themes]

Generate:
1. Visual mind map of connected thoughts
2. Top 10 realizations (in author's words)
3. Thinking evolution timeline
4. Action items mentioned
5. For creators: content ideas from insights
6. Make it visual with ASCII art and emojis
```

### 5. Output Organization

- Save extracted insights to `lifeOS/braindumps/analysis/insights-YYYY-MM-DD.md`
- Save full analysis to `lifeOS/braindumps/analysis/analysis-YYYY-MM-DD.md`
- Provide summary to user with key discoveries

## Key Features:

- Pattern recognition across multiple dumps
- Thinking evolution tracking
- Hidden connection discovery
- Action item extraction
- Content idea generation (for creators)
- Visual representation of thoughts

## Important Notes:

- Preserve the author's authentic voice
- Celebrate thinking and growth
- Find patterns the author can't see
- Make insights actionable
- Show how ideas connect and evolve
