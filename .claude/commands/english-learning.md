# English Learning from Code

智能英语学习系统 - 从您的项目代码中学习专业技术词汇

## Process:

### 1. 词汇扫描与提取

根据用户的具体命令执行相应操作：

#### `/english-learning scan` - 扫描项目提取新词汇

- 分析项目结构，扫描所有代码文件（.py, .java, .rs, .md, .toml, .json）
- 启动 en-vocabulary-extractor 子代理：提取所有技术词汇（包括低频生词），过滤基础词汇
- 保存词汇到 `lifeOS/english/vocabulary/tech-terms.json`
- 生成扫描报告到 `lifeOS/english/reports/scan-report-YYYY-MM-DD.md`

#### `/english-learning daily` - 开始今日学习

- 读取词汇库，选择10个待学习词汇，优先级：
  1. 未学习的生词（优先低频专业术语）
  2. 复习到期词汇
  3. 最近新增词汇
  4. 项目高频词汇
- 启动 en-context-generator 子代理：为每个词汇生成项目语境、技术解释、应用场景、记忆技巧、练习题
- 保存语境到 `lifeOS/english/contexts/[word].json`
- 保存学习记录到 `lifeOS/english/daily/daily-learning-YYYY-MM-DD.md`
- 更新进度数据 `lifeOS/english/progress/daily-records.json`

#### `/english-learning review` - 复习到期词汇

- 读取复习计划，计算基于遗忘曲线的到期词汇
- 读取已有的 contexts 文件进行复习测试
- 根据测试结果更新复习计划，调整下次复习时间（1天/3天/7天/15天/30天）

#### `/english-learning progress` - 查看学习进度

- 读取所有学习数据文件（词汇库、学习记录、统计数据）
- 启动 en-progress-analyzer 子代理：生成可视化报告（学习曲线、掌握度分布、领域覆盖、连续天数、亮点和建议）
- 保存报告到 `lifeOS/english/progress/progress-report-YYYY-MM-DD.md`

#### `/english-learning context [word]` - 查看特定词汇语境

- 读取 `lifeOS/english/contexts/[word].json`（如不存在则调用 en-context-generator 即时生成）
- 显示完整语境：项目语境、技术解释、应用场景、记忆技巧、练习题
- 展示在项目中的实际使用位置和相关词汇推荐

### 2. 数据存储结构

```
lifeOS/english/
├── vocabulary/
│   ├── tech-terms.json      # 所有提取的技术词汇
│   ├── learning.json         # 正在学习的词汇
│   ├── mastered.json         # 已掌握词汇
│   └── review-schedule.json  # 复习计划
├── contexts/
│   └── [word].json           # 每个词汇的语境句子
├── daily/
│   └── daily-learning-YYYY-MM-DD.md  # 每日学习记录
├── progress/
│   ├── daily-records.json            # 每日学习汇总数据
│   ├── statistics.json               # 统计数据
│   └── progress-report-YYYY-MM-DD.md # 学习进度报告
└── reports/
    └── scan-report-YYYY-MM-DD.md     # 词汇扫描报告
```

### 3. 学习策略

**词汇提取规则：**

- 提取：技术专有名词、复合词、缩写词、领域术语
- **重点：所有专业术语都提取，包括低频生词**

**学习优先级：**

1. 未学习的生词（优先低频专业术语）
2. 复习到期词汇
3. 最近新增词汇
4. 项目高频词汇

**掌握度分级：**

- 🌱 初识 → 📖 理解 → 💡 应用 → 🎯 精通

### 4. 文件路径规范

- **每日学习记录**：`lifeOS/english/daily/daily-learning-YYYY-MM-DD.md`
- **词汇扫描报告**：`lifeOS/english/reports/scan-report-YYYY-MM-DD.md`
- **学习进度报告**：`lifeOS/english/progress/progress-report-YYYY-MM-DD.md`
- **词汇库数据**：`lifeOS/english/vocabulary/tech-terms.json`
- **语境数据**：`lifeOS/english/contexts/[word].json`
- **学习记录**：`lifeOS/english/progress/daily-records.json`

## Important Notes:

- 始终基于用户的实际项目内容生成学习材料
- **确保所有技术生词都被提取，包括低频词**
- 语境句子要自然、专业、实用
- 学习优先级：生词 > 复习 > 高频词
- 保持学习的连续性和趣味性
