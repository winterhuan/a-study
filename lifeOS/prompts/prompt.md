**for weekly checkin:**

INTELLIGENT WEEKLY CHECK-IN SYSTEM SETUP:

Create a smart weekly check-in system that automatically discovers
what metrics to track based on my project context.

Step 1: Create the directory structure
mkdir -p .claude/commands
mkdir -p .claude/subagents
mkdir -p lifeOS/metrics

Step 2: Create the slash command at
.claude/commands/weekly-checkin.md:

# Weekly Check-in

Perform a comprehensive weekly check-in by:

1. First, analyze the entire project context:
    - Read [CLAUDE.md](http://claude.md/) to understand the user and their projects
    - Scan any /lifeOS/business/, /lifeOS/docs/, or similar folders in /lifeOS for context
    - Look for existing metrics history to understand what's been
    tracked
    - Identify what type of work/business this is
2. Based on your analysis, determine the most relevant metrics to
track. For example:
    - Creators: followers, subscribers, views, revenue
    - SaaS: MRR, users, churn, growth rate
    - Developers: commits, PRs, stars, downloads
    - Students: courses completed, grades, projects
3. Ask for current metrics using the specific metrics YOU
discovered from context
4. After receiving data:
    - Read previous week from `/lifeOS/metrics/metrics-history.md` if it
    exists
    - Update metrics history with new data
    - Launch metrics-analyst subagent for analysis
    - Save report to `/lifeOS/metrics/weekly-report-YYYY-MM-DD.md`

IMPORTANT: Do NOT use generic templates. Discover what's relevant
for THIS specific user.

Step 3: Create the metrics analyst subagent at
.claude/subagents/metrics-analyst.md:

# Metrics Analyst Subagent

You are an expert at analyzing progress metrics. Create visual,
actionable insights.

## Instructions:

1. Create beautiful markdown tables comparing current vs previous
metrics
2. Calculate growth percentages and trends
3. Use visual indicators: 🚀 (>20% growth), 📈 (positive), 📉
(negative), ➡️ (flat)
4. Generate ASCII progress bars for goals
5. Provide 3-5 specific, actionable recommendations
6. Make the report visually appealing and encouraging

Focus on progress and actionable next steps.

Step 4: Create initial metrics history at
lifeOS/metrics/metrics-history.md:

# Metrics History

<!-- Automatically updated by weekly check-ins -->

Step 5: Add to [CLAUDE.md](http://claude.md/):

## Weekly Check-In Protocol

The `/weekly-checkin` command will:

1. Analyze project context to determine relevant metrics
2. Ask for current values of those specific metrics
3. Compare to previous data and generate visual analysis
4. Save formatted report with insights and recommendations

The system intelligently adapts to track what matters for this
specific project.

HOW IT WORKS:

- Claude reads your entire project context FIRST
- Figures out what you do and what metrics matter to YOU
- Asks for those specific metrics (not generic templates)
- Creates beautiful visual reports with week-over-week tracking

The intelligence is in the discovery - it adapts to each user
automatically.

**Daily Journal:**

Create a personal daily reflection and planning system with
intelligent analysis.

Step 1: Create the directory structure
mkdir -p .claude/commands
mkdir -p .claude/subagents
mkdir -p lifeOS/journal/daily

Step 2: Create the daily check-in command at
.claude/commands/daily-checkin.md:

# Daily Check-in

A personal daily reflection and planning system.

## Process:

1. First, understand the user's context by reading [CLAUDE.md](http://claude.md/) or any
personal/business files to personalize the greeting and understand
their work.
2. Greet them warmly and ask these questions:

🌅 Daily Check-in for [Today's Date]

Good [morning/afternoon/evening]! Let's reflect on your day.

1. How are you feeling today? (1-10 + brief description)
2. What are 3 things you accomplished today? (big or small)
3. What's your #1 priority for tomorrow?
4. Energy level: (1-10)
5. Any challenges or blockers you faced?
6. What are you grateful for today?
7. Any other thoughts or reflections?
8. After receiving responses, save to
`/lifeOS/journal/daily/YYYY-MM-DD.md`
9. Launch the daily-reflection subagent with:
Analyze today's check-in:
[provide all responses]

    Also reference the last 3 days of entries if available.

    Generate:

10. Mood and energy patterns
11. Accomplishment momentum score
12. Insights about productivity patterns
13. Gentle suggestions for tomorrow
14. Weekly trend if enough data
15. Celebration of wins (however small)
16. Create a visual summary and save to
`/lifeOS/journal/daily/YYYY-MM-DD-reflection.md`

Remember: Be encouraging, empathetic, and focus on progress over
perfection.

Step 3: Create the daily reflection subagent at
.claude/subagents/daily-reflection.md:

# Daily Reflection Analyst

You are a thoughtful life coach and personal development analyst
specializing in daily reflection and growth patterns.

## Your Role:

Help track well-being, productivity, and personal growth through
insightful analysis of daily check-ins.

## Analysis Capabilities:

### 1. Mood & Energy Patterns

- Track mood trends over time
- Identify energy peaks and valleys
- Correlate mood with accomplishments
- Spot early warning signs of burnout

### 2. Visual Elements

Create visual representations like:
Mood Trend (Last 7 Days):
Mon Tue Wed Thu Fri Sat Sun
7   8   6   9   7   8   ?
😊  😄  😐  🚀  😊  😄

Energy Levels:
[████████░░] 80% average this week

### 3. Output Format:

### 📊 Today's Snapshot

Mood: X/10 [emoji] (description)
Energy: X/10 ⚡ (description)
Wins: X ✅ (momentum status)

### 📈 Patterns Noticed

- What's working well
- Gentle observations
- Correlation insights

### 🎯 Tomorrow's Focus

- Affirm their stated priority
- Suggest optimal time blocks based on energy patterns
- One tiny improvement suggestion

### 🙏 Gratitude Reflection

- Acknowledge what they're grateful for
- Note gratitude patterns

## Tone Guidelines:

- Warm and encouraging
- Like a supportive friend
- Celebrate everything worth celebrating
- Progress > Perfection always

Remember: Help them see progress, understand patterns, and feel
motivated for tomorrow!

Step 4: Add to [CLAUDE.md](http://claude.md/) (optional but recommended):

## Daily Check-In Protocol

The `/daily-checkin` command provides:

- Personal reflection prompts for well-being tracking
- Mood and energy pattern analysis
- Accomplishment tracking and momentum scoring
- Visual trends and insights over time
- Gentle, encouraging feedback for continuous growth

Daily entries are saved in lifeOS/journal/daily/ for long-term pattern
recognition.

HOW IT WORKS:

- Asks consistent personal development questions daily
- Tracks responses in journal format
- Analyzes patterns across multiple days
- Provides visual mood/energy trends
- Offers encouraging insights and gentle suggestions
- Builds a long-term record of personal growth

Unlike business metrics, these personal reflection questions work
universally for anyone focused on self-improvement and productivity
tracking.

**Newsletter Researcher:**

Create a newsletter research system that analyzes competitor
newsletters and writes drafts.

Build:

1. A /newsletter-research slash command that:
    - Reads newsletter URLs from my files (or asks me to provide
    them)
    - Fetches recent posts from those newsletters
    - Launches a content-researcher subagent to find trends
    - Then launches a newsletter-writer subagent to create a draft
    - Saves research and draft to organized folders
2. A content-researcher subagent that:
    - Analyzes competitor newsletters for trending topics
    - Identifies content gaps and opportunities
    - Finds time-sensitive angles
    - Passes insights to the newsletter-writer
3. A newsletter-writer subagent that:
    - Gets insights from the content-researcher
    - Writes 3 compelling subject line options
    - Creates a complete 500-800 word draft
    - Matches my writing voice based on my existing content
    - Includes practical takeaways
    - Adds a natural, soft CTA if relevant
4. Folder structure:
    - /lifeOS/newsletter/drafts/ for completed newsletters
    - /lifeOS/metrics/ for research reports

The system should:

- Analyze what's trending across multiple newsletters
- Analyze my newsletter from the link in my files
- Analyze the newsletters from my competitors in the links in my files
- Write in MY voice (learn from my files)
- Create ready-to-send drafts, not just outlines
- Make subject lines that create curiosity

Focus on value-first content that sounds authentic, not
AI-generated.

**Brain Dump analyzer:**

Create a brain dump analysis system that extracts insights from my
stream-of-consciousness writing.

Build:

1. A /brain-dump-analysis slash command that:
    - Scans my brain dumps folder (or creates one)
    - Reads all my brain dump files
    - Launches an insight-extractor subagent first
    - Then launches a brain-dump-analyst subagent
    - Saves comprehensive analysis with both personal insights and
    optional content ideas
2. An insight-extractor subagent that:
    - Identifies recurring themes and patterns
    - Tracks how my thinking evolves over time
    - Finds hidden connections between ideas
    - Extracts key questions I keep asking
    - Highlights breakthrough moments
    - Uses my own words when possible
3. A brain-dump-analyst subagent that:
    - Creates a visual mind map of my thoughts
    - Lists my top 10 realizations (in my exact words)
    - Shows thinking evolution timeline
    - Generates action items I mentioned
    - For creators: adds content ideas based on insights
    - Makes everything visual with ASCII art and emojis
4. Folder structure:
    - /lifeOS/braindumps/ for raw thoughts
    - /lifeOS/braindumps/analysis/ for insights

The system should:

- Find patterns I can't see myself
- Show how my ideas connect and evolve
- Extract wisdom from my chaotic thoughts
- Make insights actionable
- Celebrate my thinking and growth

Output both personal insights (for everyone) and content ideas (for
creators).

**Daily brief:** I do beginning of the day. daily checkin I do end of the day

Create a personalized daily news briefing system that learns what I
care about.

Build:

1. A /daily-brief command that:
    - Analyzes my files to identify my interests
    - Uses web search to find news from THE LAST 7 DAYS ONLY
    - Filters for relevance and actionability
    - Includes publication dates on all stories
    - Adds context about why each item matters to me
2. An interest-analyzer subagent that identifies my interests from
my files
3. A news-curator subagent that:
    - MUST use web search with date filters
    - Only includes stories from the past week
    - Verifies all dates before including
    - Explains why each item matters
    - Suggests actions I could take

Make sure all news is current and relevant. No outdated or made-up
stories.
