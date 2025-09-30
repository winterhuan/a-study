# 📚 Today's Learning - 2025-09-29

## 🎯 今日学习目标：掌握10个高频技术词汇

---

### Word 1: **executor**
📊 Frequency: 22 times | 📁 Category: Distributed Systems

**📝 Contexts:**
1. *Project Context:* "CoarseGrainedExecutorBackend is Spark's standard Executor backend implementation"
2. *Technical Meaning:* An executor is a distributed computing unit that runs tasks in parallel processing frameworks. It manages resources and executes the actual computation on worker nodes.
3. *Practical Use:* "We need to configure 10 executors with 4GB memory each for this Spark job"

**🧠 Memory Tip:**
Execute + -or (one who does) = Executor (执行者)
Think of it as "the one who executes tasks" in a distributed system

**✍️ Practice:**
- Fill in: "Each _______ in Spark is responsible for running tasks and storing data partitions."
- Choice: What does an executor primarily do?
  A) Compile code B) Execute tasks on worker nodes ✓ C) Design architecture D) Write logs

---

### Word 2: **streaming**
📊 Frequency: 18 times | 📁 Category: Stream Processing

**📝 Contexts:**
1. *Project Context:* "StreamExecutionEnvironment - the stream processing execution environment"
2. *Technical Meaning:* Streaming refers to continuous data processing where data is processed as it arrives, rather than in batches. It enables real-time analytics and event processing.
3. *Practical Use:* "Our streaming pipeline processes 100,000 events per second in real-time"

**🧠 Memory Tip:**
Stream + -ing = Streaming (流式处理)
Like a river stream that flows continuously, data streams flow continuously

**✍️ Practice:**
- Fill in: "Apache Flink is designed for _______ processing with low latency."
- Choice: Which is a characteristic of streaming?
  A) Batch processing B) Real-time processing ✓ C) Offline analysis D) Static data

---

### Word 3: **checkpoint**
📊 Frequency: 15 times | 📁 Category: Distributed Systems

**📝 Contexts:**
1. *Project Context:* "Checkpoint is the core feature of Flink's fault tolerance mechanism"
2. *Technical Meaning:* A checkpoint is a snapshot of the application state at a specific point in time. It enables recovery from failures by restoring the system to a previous consistent state.
3. *Practical Use:* "Enable checkpointing every 5 minutes to ensure job recovery in case of failure"

**🧠 Memory Tip:**
Check + point = Checkpoint (检查点)
Like a save point in a video game - you can restart from there if something goes wrong

**✍️ Practice:**
- Fill in: "The _______ mechanism ensures our streaming job can recover from failures."
- Choice: What is the primary purpose of checkpoints?
  A) Performance optimization B) Fault tolerance ✓ C) Data validation D) Code compilation

---

### Word 4: **schema**
📊 Frequency: 12 times | 📁 Category: Data Structures

**📝 Contexts:**
1. *Project Context:* "let schema = Arc::new(Schema::new(vec![Field::new(...)]))"
2. *Technical Meaning:* A schema defines the structure of data, including field names, data types, and constraints. It's the blueprint for how data is organized.
3. *Practical Use:* "Define a schema with user_id (long), name (string), and timestamp (datetime)"

**🧠 Memory Tip:**
Schema comes from Greek "skhēma" meaning "form" or "shape"
Think of it as the shape/structure of your data

**✍️ Practice:**
- Fill in: "Before loading data, we need to define the _______ to specify column types."
- Choice: What does a schema contain?
  A) Data values B) Field definitions and types ✓ C) Actual records D) Query results

---

### Word 5: **backend**
📊 Frequency: 9 times | 📁 Category: Architecture

**📝 Contexts:**
1. *Project Context:* "HashMapStateBackend - the in-memory state backend implementation"
2. *Technical Meaning:* A backend is the server-side component that handles data processing, storage, and business logic. It operates behind the scenes to support frontend operations.
3. *Practical Use:* "Switch from RocksDB backend to in-memory backend for faster state access"

**🧠 Memory Tip:**
Back + end = Backend (后端)
The "back end" that users don't see, working behind the scenes

**✍️ Practice:**
- Fill in: "The state _______ determines how Flink stores and manages state data."
- Choice: Which is typically a backend responsibility?
  A) UI rendering B) Data persistence ✓ C) User interaction D) CSS styling

---

### Word 6: **asynchronous**
📊 Frequency: 8 times | 📁 Category: Concurrency

**📝 Contexts:**
1. *Project Context:* "#[tokio::main] async fn main() -> Result<()>"
2. *Technical Meaning:* Asynchronous operations don't block execution while waiting for results. They allow multiple operations to proceed concurrently without waiting for each other.
3. *Practical Use:* "Use asynchronous I/O to improve throughput when calling external services"

**🧠 Memory Tip:**
A- (not) + synchronous (同时的) = Asynchronous (异步的)
"Not synchronized" - things happen independently

**✍️ Practice:**
- Fill in: "_______ programming allows handling multiple requests without blocking."
- Choice: What's the main advantage of asynchronous operations?
  A) Simplicity B) Non-blocking execution ✓ C) Less code D) Synchronization

---

### Word 7: **windowing**
📊 Frequency: 7 times | 📁 Category: Stream Processing

**📝 Contexts:**
1. *Project Context:* "TumblingProcessingTimeWindows.of(Duration.ofSeconds(5))"
2. *Technical Meaning:* Windowing divides infinite data streams into finite chunks for processing. Common types include tumbling (non-overlapping) and sliding (overlapping) windows.
3. *Practical Use:* "Apply a 10-minute tumbling window to calculate average temperature"

**🧠 Memory Tip:**
Window + -ing = Windowing (窗口化)
Like looking through windows of time to see data in chunks

**✍️ Practice:**
- Fill in: "_______ allows us to aggregate streaming data over time intervals."
- Choice: What is a tumbling window?
  A) Overlapping windows B) Non-overlapping fixed windows ✓ C) Session windows D) Global windows

---

### Word 8: **tokenizer**
📊 Frequency: 6 times | 📁 Category: Algorithms

**📝 Contexts:**
1. *Project Context:* ".flatMap(new Tokenizer()) // splits sentences into words"
2. *Technical Meaning:* A tokenizer breaks text into smaller units (tokens) like words or subwords. It's essential for text processing and natural language processing tasks.
3. *Practical Use:* "The tokenizer splits 'Hello World' into ['Hello', 'World']"

**🧠 Memory Tip:**
Token + -izer (maker of) = Tokenizer (分词器)
It makes tokens (small pieces) from larger text

**✍️ Practice:**
- Fill in: "The _______ splits input text into individual words for processing."
- Choice: What does a tokenizer produce?
  A) Sentences B) Tokens/words ✓ C) Characters D) Paragraphs

---

### Word 9: **watermark**
📊 Frequency: 6 times | 📁 Category: Stream Processing

**📝 Contexts:**
1. *Project Context:* "Structured Streaming's watermark implementation for handling late data"
2. *Technical Meaning:* A watermark is a timestamp that indicates the progress of event time in stream processing. It helps handle late-arriving data by defining when a window can be considered complete.
3. *Practical Use:* "Set watermark to 10 minutes to allow late data within that threshold"

**🧠 Memory Tip:**
Water + mark = Watermark (水位线)
Like a water level mark showing how far time has progressed

**✍️ Practice:**
- Fill in: "The _______ helps determine when to trigger window computations despite late data."
- Choice: What problem do watermarks solve?
  A) Data compression B) Late data handling ✓ C) Data encryption D) Load balancing

---

### Word 10: **parallelism**
📊 Frequency: 5 times | 📁 Category: Concurrency

**📝 Contexts:**
1. *Project Context:* "windowCounts.print().setParallelism(1)"
2. *Technical Meaning:* Parallelism is the simultaneous execution of multiple tasks. It determines how many parallel instances of an operator run concurrently.
3. *Practical Use:* "Increase parallelism to 10 for better throughput on this 10-core machine"

**🧠 Memory Tip:**
Parallel + -ism = Parallelism (并行性)
Think of parallel train tracks - multiple trains running side by side

**✍️ Practice:**
- Fill in: "Setting _______ to 4 means the operator will have 4 parallel instances."
- Choice: What does parallelism affect?
  A) Code quality B) Concurrent execution capacity ✓ C) Memory type D) Network protocol

---

## 📊 Today's Summary

### 掌握情况自评
- [ ] executor - 理解程度: ___/5
- [ ] streaming - 理解程度: ___/5
- [ ] checkpoint - 理解程度: ___/5
- [ ] schema - 理解程度: ___/5
- [ ] backend - 理解程度: ___/5
- [ ] asynchronous - 理解程度: ___/5
- [ ] windowing - 理解程度: ___/5
- [ ] tokenizer - 理解程度: ___/5
- [ ] watermark - 理解程度: ___/5
- [ ] parallelism - 理解程度: ___/5

### 🎯 应用练习
Try to write a sentence using at least 3 of today's words:
Example: "The streaming job uses asynchronous executors with parallelism set to 8."

Your sentence: _______________________________________

### 📅 复习计划
- Tomorrow: Quick review of all 10 words
- Day 3: Focus on words scored < 4
- Day 7: Complete review with new contexts
- Day 15: Final reinforcement

Keep learning! 🚀 Tomorrow we'll explore the next set of technical vocabulary.