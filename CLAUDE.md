# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a multi-technology study repository focused on big data and distributed systems learning, with integrated personal productivity tools (lifeOS system).

## Repository Structure

- **agnoStudy/**: Python-based AI model integration studies (OpenRouter examples)
- **sparkStudy/**: Apache Spark learning materials
- **flinkStudy/**: Apache Flink learning materials
- **lanceStudy/**: Lance columnar database examples (Rust)
- **kafkaStudy/**: Apache Kafka learning materials
- **lifeOS/**: Personal productivity system with daily/weekly tracking tools

## Development Commands

### Rust Development

```bash
# Build all Rust projects
cargo build

# Run tests
cargo test

# Add new dependencies
cargo add [package_name]

# Search for packages
cargo search [package_name] --registry crates-io
```

### Python Development (agnoStudy)

```bash
# Activate virtual environment
cd agnoStudy && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run examples
python simple_example.py
python advanced_example.py
```

## Configuration Notes

### Rust/Cargo China Mirror Configuration

The repository uses USTC mirrors for faster Rust/Cargo operations in China. Configuration is in `~/.cargo/config.toml`.

### Symlinks

Study materials are symlinked from external repositories:

- `agnoStudy/agno -> ../../study/agno/`
- `sparkStudy/spark -> ../../study/spark/`
- `flinkStudy/flink -> ../../study/flink/`

## lifeOS Custom Commands

The repository includes a comprehensive personal productivity system with the following commands:

## Daily Check-In Protocol

The `/daily-checkin` command provides:

- Personal reflection prompts for well-being tracking
- Mood and energy pattern analysis
- Accomplishment tracking and momentum scoring
- Visual trends and insights over time
- Gentle, encouraging feedback for continuous growth

Daily entries are saved in `lifeOS/journal/daily/` for long-term pattern recognition.

### How it works:

- Asks consistent personal development questions daily
- Tracks responses in journal format (saved to `lifeOS/journal/daily/YYYY-MM-DD.md`)
- Analyzes patterns across multiple days
- Provides visual mood/energy trends
- Offers encouraging insights and gentle suggestions
- Analysis outputs saved to `lifeOS/journal/daily/YYYY-MM-DD-reflection.md`
- Builds a long-term record of personal growth

Unlike business metrics, these personal reflection questions work universally for anyone focused on self-improvement and productivity tracking.

### Directory Structure:

- **Commands**: `.claude/commands/daily-checkin.md`
- **Subagents**: `.claude/subagents/daily-reflection.md`
- **Journal Data**: `lifeOS/journal/daily/` (all inputs and outputs)

## Newsletter Research Protocol

The `/newsletter-research` command provides:

- Automated competitor newsletter analysis
- Trend identification across multiple sources
- Content gap and opportunity discovery
- AI-powered draft creation in your unique voice
- Complete 500-800 word newsletters ready to send

### How it works:

- Fetches and analyzes competitor newsletters from URLs
- Identifies trending topics and content opportunities
- Learns your writing style from existing content
- Generates 3 compelling subject line options
- Creates value-first drafts with practical takeaways
- Organizes research and drafts in structured folders

### Key Features:

- **Smart Analysis**: Tracks trends across multiple newsletters
- **Voice Matching**: Learns and mimics your writing style
- **Complete Drafts**: Not just outlines, but ready-to-send content
- **Strategic Insights**: Identifies gaps and timing opportunities
- **Authentic Output**: Sounds human, not AI-generated

### Directory Structure:

- **Commands**: `.claude/commands/newsletter-research.md`
- **Subagents**:
    - `.claude/subagents/content-researcher.md` - Trend analysis
    - `.claude/subagents/newsletter-writer.md` - Draft creation
- **Newsletter Data**:
    - `lifeOS/newsletter/drafts/` - Completed drafts
    - `lifeOS/newsletter/research/` - Analysis reports
    - `lifeOS/newsletter/sources/` - URL sources
    - `lifeOS/metrics/` - Performance metrics

## Weekly Check-In Protocol

The `/weekly-checkin` command provides:

- Intelligent context-aware metrics discovery
- Automated identification of relevant KPIs based on your work
- Week-over-week comparison with visual indicators
- Beautiful markdown reports with progress visualization
- Actionable recommendations based on data trends

### How it works:

1. **Context Analysis**: Reads your entire project to understand what you do
2. **Smart Discovery**: Automatically identifies relevant metrics (not generic templates)
3. **Data Collection**: Asks for specific metrics that matter to YOUR work
4. **Visual Analysis**: Creates beautiful reports with growth indicators and progress bars
5. **Actionable Insights**: Provides specific recommendations based on trends

### Adaptive Metrics Examples:

- **Creators**: Followers, views, engagement, revenue
- **SaaS/Products**: MRR, users, churn, growth rate
- **Developers**: Stars, commits, PRs, downloads
- **Students**: Courses, projects, study hours, skills

### Key Features:

- **Intelligent Adaptation**: Discovers what matters for YOUR specific context
- **Visual Reports**: Beautiful tables, progress bars, and trend indicators
- **Growth Tracking**: Week-over-week comparisons with percentages
- **Encouraging Tone**: Celebrates wins and frames challenges as opportunities
- **Historical Data**: Maintains complete metrics history for trend analysis

### Directory Structure:

- **Commands**: `.claude/commands/weekly-checkin.md`
- **Subagents**: `.claude/subagents/metrics-analyst.md`
- **Metrics Data**:
    - `lifeOS/metrics/metrics-history.md` - Historical data
    - `lifeOS/metrics/weekly-report-YYYY-MM-DD.md` - Weekly reports

## Brain Dump Analysis Protocol

The `/brain-dump-analysis` command provides:

- Deep pattern recognition in stream-of-consciousness writing
- Thinking evolution tracking over time
- Hidden connection discovery between ideas
- Visual mind mapping of thought patterns
- Action item extraction and content idea generation

### How it works:

1. **Content Collection**: Reads all brain dump files from `lifeOS/braindumps/`
2. **Pattern Extraction**: Identifies recurring themes, questions, and breakthroughs
3. **Deep Analysis**: Maps connections and evolution of thinking
4. **Visual Output**: Creates mind maps and timeline visualizations
5. **Action Generation**: Transforms insights into concrete next steps

### Key Capabilities:

- **Pattern Recognition**: Finds themes you can't see yourself
- **Evolution Tracking**: Shows how your ideas develop over time
- **Connection Discovery**: Links seemingly unrelated thoughts
- **Breakthrough Detection**: Highlights moments of clarity
- **Voice Preservation**: Uses your exact words in analysis

### Output Features:

- **Visual Mind Maps**: ASCII art showing thought connections
- **Top 10 Realizations**: Your most profound insights (in your words)
- **Thinking Timeline**: Journey from questions to clarity
- **Action Items**: Concrete steps extracted from your thoughts
- **Content Ideas**: For creators - topics and angles from insights
- **Growth Celebration**: Highlights your thinking evolution

### Directory Structure:

- **Commands**: `.claude/commands/brain-dump-analysis.md`
- **Subagents**:
    - `.claude/subagents/insight-extractor.md` - Pattern mining
    - `.claude/subagents/brain-dump-analyst.md` - Visual analysis
- **Brain Dump Data**:
    - `lifeOS/braindumps/` - Your raw thoughts
    - `lifeOS/braindumps/analysis/` - Insights and analysis

## Daily Brief Protocol

The `/daily-brief` command provides:

- Personalized news based on your actual interests
- ONLY news from the last 7 days (verified dates)
- Relevance explanations for each item
- Actionable insights and suggestions
- Organized by priority and interest areas

### How it works:

1. **Interest Discovery**: Analyzes your files to identify what you care about
2. **Smart Search**: Uses web search with date filters (last 7 days only)
3. **Date Verification**: Confirms all publication dates before inclusion
4. **Relevance Filtering**: Only includes news that matters to YOU
5. **Context Addition**: Explains why each item is relevant and what to do

### Key Features:

- **Personalized**: Based on analysis of your actual projects and files
- **Current**: Strictly enforces 7-day recency requirement
- **Verified**: All dates checked, no outdated content
- **Actionable**: Includes suggested actions for each news item
- **Contextual**: Shows how news relates to your specific work

### What it tracks (examples):

- **For Developers**: Framework updates, security alerts, new tools
- **For Creators**: Platform changes, trending topics, opportunities
- **For Entrepreneurs**: Market news, competitor moves, industry trends
- **For Students**: Research developments, learning resources, deadlines

### Directory Structure:

- **Commands**: `.claude/commands/daily-brief.md`
- **Subagents**:
    - `.claude/subagents/interest-analyzer.md` - Discovers your interests
    - `.claude/subagents/news-curator.md` - Finds and verifies news
- **Brief Data**:
    - `lifeOS/daily-brief/` - Daily briefings
    - `lifeOS/daily-brief/archives/` - Historical briefings

## English Learning Protocol

The `/english-learning` command provides an intelligent vocabulary learning system that extracts technical terms directly from your project code:

- Smart vocabulary extraction from code and documentation
- Automatic filtering based on your English level (high school+)
- Context generation from real project usage
- Spaced repetition based on forgetting curve
- Visual progress tracking and gamification

### Commands:

- `/english-learning scan` - Scan project files to extract new technical vocabulary
- `/english-learning daily` - Start today's learning session (10 words with contexts)
- `/english-learning review` - Review words due for reinforcement
- `/english-learning progress` - Generate visual progress report
- `/english-learning context [word]` - View detailed contexts for a specific word

### How it works:

1. **Intelligent Extraction**: Scans your code to find valuable technical terms
2. **Smart Filtering**: Excludes simple words you already know (high school level)
3. **Context Creation**: Generates 3 types of contexts for each word:
   - Project context (actual usage in your code)
   - Technical explanation (clear definition)
   - Practical application (real-world usage)
4. **Adaptive Learning**: Prioritizes high-frequency and recently-appeared words
5. **Progress Tracking**: Visualizes learning curves and domain coverage

### Key Features:

- **Personalized Source**: Learn from YOUR actual project vocabulary
- **Difficulty Grading**: Focuses on intermediate to advanced technical terms
- **Real Contexts**: Examples from your codebase, not generic sentences
- **Mastery Levels**: Track progress from recognition to fluent usage
- **Domain Coverage**: Build vocabulary across different technical areas

### Learning Focus Areas (from your projects):

- **Distributed Systems**: executor, checkpoint, partition, consensus
- **Stream Processing**: watermark, windowing, backpressure, throughput
- **Architecture**: orchestration, scalability, resilience, idempotent
- **Concurrency**: asynchronous, mutex, semaphore, deadlock

### Directory Structure:

- **Commands**: `.claude/commands/english-learning.md`
- **Subagents**:
    - `.claude/subagents/en-vocabulary-extractor.md` - Intelligent word extraction
    - `.claude/subagents/en-context-generator.md` - Context and practice generation
    - `.claude/subagents/en-progress-analyzer.md` - Visual progress reports
- **Learning Data**:
    - `lifeOS/english/vocabulary/` - Word lists and mastery tracking
    - `lifeOS/english/contexts/` - Generated learning contexts
    - `lifeOS/english/daily/` - Daily learning records
    - `lifeOS/english/progress/` - Statistics, achievements and progress reports
    - `lifeOS/english/reports/` - Vocabulary scan reports
