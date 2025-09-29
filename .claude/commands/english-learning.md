# English Learning from Code

智能英语学习系统 - 从您的项目代码中学习专业技术词汇

## Process:

### 1. 词汇扫描与提取

根据用户的具体命令执行相应操作：

#### `/english-learning scan` - 扫描项目提取新词汇

- 扫描项目中的所有代码文件（.py, .java, .rs, .md等）
- 提取技术词汇、专业术语、复合词
- 过滤掉简单常见词（如: get, set, data, run等）
- 识别最近修改文件中的新词汇
- 将词汇按难度和领域分类存储

#### `/english-learning daily` - 开始今日学习

- 从词汇库中选择10个待学习词汇
- 优先选择：
    - 项目中高频出现的词汇
    - 最近代码中新出现的词汇
    - 到期需要复习的词汇
- 为每个词汇生成学习材料：
    - 原始代码语境（词汇在项目中的实际使用）
    - 技术解释（简明的技术含义）
    - 应用场景（实际工作中的使用例子）
- 进行互动练习：
    - 语境填空
    - 造句练习
    - 场景应用选择
- 记录学习结果和掌握度

#### `/english-learning review` - 复习到期词汇

- 基于艾宾浩斯遗忘曲线计算复习时间
- 复习间隔：1天、3天、7天、15天、30天
- 展示需要复习的词汇列表
- 进行复习测试
- 根据测试结果调整下次复习时间

#### `/english-learning progress` - 查看学习进度

- 启动进度分析器子代理生成可视化报告
- 显示学习统计：
    - 总词汇量和各级别分布
    - 学习连续天数和效率
    - 领域覆盖情况
    - 本周/本月进度对比

#### `/english-learning context [word]` - 查看特定词汇语境

- 显示该词汇的所有语境句子
- 展示在项目中的实际使用位置
- 提供相关词汇推荐

### 2. 子代理调用

根据不同命令调用相应子代理：

**词汇提取器 (vocabulary-extractor):**

```
扫描以下文件类型：[提供文件列表]
提取技术词汇，过滤基础词汇（高中水平）
返回JSON格式的词汇列表，包含：
- 词汇
- 出现频率
- 所在文件
- 代码上下文
```

**语境生成器 (context-generator):**

```
为以下词汇生成学习材料：[词汇列表]
每个词汇生成：
1. 原始代码语境（基于项目代码）
2. 技术解释（简洁专业）
3. 应用场景句子
确保句子自然、实用、专业
```

**进度分析器 (progress-analyzer):**

```
分析学习数据：
- 当前掌握词汇：[数据]
- 学习历史：[数据]
- 复习记录：[数据]

生成可视化报告，包含：
- 学习曲线图
- 掌握度分布
- 领域覆盖雷达图
- 本周亮点和建议
```

### 3. 数据存储结构

```
lifeOS/english/
├── vocabulary/
│   ├── tech-terms.json      # 所有提取的技术词汇
│   ├── learning.json         # 正在学习的词汇
│   ├── mastered.json         # 已掌握词汇
│   └── review-schedule.json  # 复习计划
├── contexts/
│   └── [word].json           # 每个词汇的语境句子
├── progress/
│   ├── daily-records.json    # 每日学习记录
│   └── statistics.json       # 统计数据
└── reports/
    └── weekly-report-YYYY-MM-DD.md  # 周报
```

### 4. 智能特性

**词汇难度判断：**

- 排除列表：常见动词、基础名词、简单形容词
- 保留规则：
    - 技术专有名词（如：serialization, polymorphism）
    - 复合词（如：checkpoint, lifecycle）
    - 缩写词（如：RPC, JVM, API）
    - 领域术语（如：executor, orchestration）

**学习优先级：**

1. 项目高频词汇（出现>5次）
2. 最近新增词汇（最近7天）
3. 复习到期词汇
4. 相关领域扩展词汇

**掌握度分级：**

- 🌱 初识（刚接触）
- 📖 理解（知道含义）
- 💡 应用（能够使用）
- 🎯 精通（熟练运用）

### 5. 输出格式

学习材料展示格式：

```markdown
### 📚 Today's Learning - [Date]

#### Word 1: **checkpoint**
📊 Frequency: 23 times in project
📁 Found in: flink_source_code_analysis.md

**📝 Contexts:**
1. *Project Context:* "The checkpoint mechanism ensures fault tolerance in streaming applications"
2. *Technical Meaning:* "A checkpoint is a snapshot of the application state at a specific point in time"
3. *Practical Use:* "Configure checkpoint intervals based on your latency requirements"

**✍️ Practice:**
Fill in: "We need to enable _______ to ensure our streaming job can recover from failures."
```

## Important Notes:

- 始终基于用户的实际项目内容生成学习材料
- 过滤掉过于简单的词汇，聚焦技术术语
- 语境句子要自然、专业、实用
- 定期分析学习效果，调整学习策略
- 保持学习的连续性和趣味性
