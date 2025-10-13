# Apache Flink 测试文件索引

> **更新日期**: 2025-01-11
> **用途**: 快速定位 Flink 源码中的测试文件
> **目标**: 通过测试代码理解 Flink 核心机制

## 📖 文档说明

本文档提供了 Flink 源码中重要测试文件的索引和说明,帮助你:

- ✅ 快速找到相关功能的测试
- ✅ 理解测试的组织结构
- ✅ 选择合适的学习起点
- ✅ 按照推荐顺序阅读

---

## 🗂️ 测试文件组织结构

### 按模块分类

```
flink-streaming-java/src/test/java/
├── org/apache/flink/streaming/
│   ├── api/
│   │   ├── environment/       # 执行环境测试
│   │   ├── datastream/         # DataStream API 测试
│   │   ├── operators/          # 算子测试
│   │   ├── windowing/          # 窗口测试
│   │   └── functions/          # 函数测试
│   ├── runtime/
│   │   ├── tasks/              # StreamTask 测试
│   │   ├── io/                 # 网络 IO 测试
│   │   └── operators/          # 运行时算子测试
│   └── util/                   # 测试工具类 (Test Harness)

flink-runtime/src/test/java/
├── org/apache/flink/runtime/
│   ├── checkpoint/             # Checkpoint 测试
│   ├── state/                  # 状态管理测试
│   ├── scheduler/              # 调度器测试
│   ├── jobgraph/               # JobGraph 测试
│   ├── executiongraph/         # ExecutionGraph 测试
│   ├── io/network/             # 网络栈测试
│   └── taskexecutor/           # TaskExecutor 测试

flink-tests/src/test/java/
└── org/apache/flink/test/      # 集成测试

flink-end-to-end-tests/
└── test-scripts/               # 端到端测试脚本
```

---

## 🎯 按学习阶段分类

### 第 1-2 周: 基础入门

#### 1. 执行环境测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **StreamExecutionEnvironmentTest** | `flink-streaming-java/.../api/environment/` | ⭐ | ⭐⭐⭐⭐⭐ | 理解环境创建和配置 |
| **StreamExecutionEnvironmentComplexConfigurationTest** | 同上 | ⭐⭐ | ⭐⭐⭐ | 复杂配置场景 |

**推荐测试用例**:

```java
// StreamExecutionEnvironmentTest.java

// 1. 理解类型推断
testFromElementsDeducedType()

// 2. 理解并行度设置
testParallelismBounds()

// 3. 理解 StreamGraph 生成
testGetStreamGraph()

// 4. 理解执行模式
testRuntimeMode()
```

**对应源码**:

- `StreamExecutionEnvironment.java` (flink-runtime)
- `StreamGraph.java`
- `StreamGraphGenerator.java`

#### 2. DataStream API 测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **DataStreamTest** | `flink-streaming-java/.../api/datastream/` | ⭐ | ⭐⭐⭐⭐ | DataStream 基本操作 |
| **KeyedStreamTest** | 同上 | ⭐⭐ | ⭐⭐⭐⭐ | KeyBy 和分区 |
| **DataStreamSinkTest** | 同上 | ⭐⭐ | ⭐⭐⭐ | Sink 操作 |

#### 3. 测试工具类 (必读!)

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **OneInputStreamOperatorTestHarness** | `flink-streaming-java/.../util/` | ⭐⭐ | ⭐⭐⭐⭐⭐ | 单输入算子测试框架 |
| **TwoInputStreamOperatorTestHarness** | 同上 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 双输入算子测试框架 |
| **KeyedOneInputStreamOperatorTestHarness** | 同上 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 键控算子测试框架 |
| **AbstractStreamOperatorTestHarness** | 同上 | ⭐⭐⭐ | ⭐⭐⭐ | 算子测试基类 |

---

### 第 3-4 周: 算子实现

#### 4. 基础算子测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **StreamMapTest** | `flink-streaming-java/.../operators/` | ⭐ | ⭐⭐⭐⭐⭐ | Map 算子测试 |
| **StreamFilterTest** | 同上 | ⭐ | ⭐⭐⭐⭐⭐ | Filter 算子测试 |
| **StreamFlatMapTest** | 同上 | ⭐ | ⭐⭐⭐⭐⭐ | FlatMap 算子测试 |
| **StreamGroupedReduceTest** | 同上 | ⭐⭐ | ⭐⭐⭐⭐ | Reduce 算子测试 |

**学习要点**:

- 如何使用 `OneInputStreamOperatorTestHarness`
- 如何构造测试数据
- 如何验证输出结果
- 如何测试时间戳和 Watermark

#### 5. 有状态算子测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **StreamingOperatorStateTest** | `flink-streaming-java/.../operators/` | ⭐⭐⭐ | ⭐⭐⭐⭐ | OperatorState 测试 |
| **AbstractStreamOperatorTest** | 同上 | ⭐⭐ | ⭐⭐⭐⭐ | 算子基类测试 |
| **StreamSourceOperatorLatencyMetricsTest** | 同上 | ⭐⭐⭐ | ⭐⭐⭐ | 延迟 Metrics |

#### 6. 窗口算子测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **WindowOperatorTest** | `flink-streaming-java/.../windowing/` | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 窗口算子核心测试 |
| **TimeWindowTest** | 同上 | ⭐⭐ | ⭐⭐⭐⭐ | 时间窗口测试 |
| **SessionWindowTest** | 同上 | ⭐⭐⭐ | ⭐⭐⭐ | 会话窗口测试 |
| **WindowAssignerTest** | 同上 | ⭐⭐ | ⭐⭐⭐⭐ | 窗口分配器测试 |

---

### 第 5-6 周: 图转换

#### 7. StreamGraph 测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **StreamGraphGeneratorTest** | `flink-streaming-java/.../graph/` | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | StreamGraph 生成测试 |
| **StreamGraphTest** | 同上 | ⭐⭐ | ⭐⭐⭐⭐ | StreamGraph 属性测试 |
| **StreamingJobGraphGeneratorTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | JobGraph 生成测试 |

**推荐测试用例**:

```java
// StreamGraphGeneratorTest.java

// 1. 理解基本图生成
testSimpleGraph()

// 2. 理解算子链
testOperatorChaining()

// 3. 理解分区策略
testPartitioning()

// 4. 理解并行度设置
testParallelism()
```

#### 8. JobGraph 测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **JobGraphTest** | `flink-runtime/.../jobgraph/` | ⭐⭐ | ⭐⭐⭐⭐ | JobGraph 基本测试 |
| **JobGraphGeneratorTestBase** | `flink-streaming-java/.../graph/` | ⭐⭐⭐ | ⭐⭐⭐⭐ | JobGraph 生成基类 |

#### 9. ExecutionGraph 测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **ExecutionGraphTest** | `flink-runtime/.../executiongraph/` | ⭐⭐⭐ | ⭐⭐⭐⭐ | 执行图测试 |
| **ExecutionVertexTest** | 同上 | ⭐⭐⭐ | ⭐⭐⭐ | 执行顶点测试 |

---

### 第 7-8 周: 任务执行

#### 10. StreamTask 测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **StreamTaskTest** | `flink-streaming-java/.../tasks/` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 任务核心测试 |
| **StreamTaskTestHarness** | 同上 | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 任务测试框架(已废弃) |
| **StreamTaskMailboxTestHarness** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 新版任务测试框架 |
| **StreamTaskMailboxTestHarnessBuilder** | 同上 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 测试框架构建器 |

**推荐测试用例**:

```java
// StreamTaskTest.java

// 1. 理解任务启动
testTaskStartup()

// 2. 理解数据处理
testProcessing()

// 3. 理解任务取消
testCancel()

// 4. 理解异常处理
testExceptionHandling()
```

#### 11. 任务执行相关测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **OneInputStreamTaskTest** | `flink-streaming-java/.../tasks/` | ⭐⭐⭐ | ⭐⭐⭐⭐ | 单输入任务测试 |
| **TwoInputStreamTaskTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 双输入任务测试 |
| **StreamTaskCancellationTest** | 同上 | ⭐⭐⭐ | ⭐⭐⭐ | 任务取消测试 |
| **StreamTaskITCase** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 任务集成测试 |

#### 12. 网络栈测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **InputGateTest** | `flink-runtime/.../io/network/partition/consumer/` | ⭐⭐⭐ | ⭐⭐⭐ | 输入网关测试 |
| **ResultPartitionTest** | `flink-runtime/.../io/network/partition/` | ⭐⭐⭐ | ⭐⭐⭐ | 结果分区测试 |
| **NetworkBufferPoolTest** | `flink-runtime/.../io/network/buffer/` | ⭐⭐⭐ | ⭐⭐⭐ | 缓冲池测试 |
| **CreditBasedPartitionRequestClientHandlerTest** | `flink-runtime/.../io/network/` | ⭐⭐⭐⭐ | ⭐⭐⭐ | Credit-based 流控测试 |

---

### 第 9-10 周: 容错机制

#### 13. Checkpoint 核心测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **CheckpointCoordinatorTest** | `flink-runtime/.../checkpoint/` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 核心协调器测试 |
| **CheckpointCoordinatorTriggeringTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 触发机制测试 |
| **CheckpointCoordinatorRestoringTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 恢复机制测试 |
| **CheckpointCoordinatorFailureTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 失败处理测试 |

**推荐测试用例**:

```java
// CheckpointCoordinatorTest.java

// 1. 理解 Checkpoint 触发
testTriggerCheckpoint()

// 2. 理解 Checkpoint 完成
testCompleteCheckpoint()

// 3. 理解 Checkpoint 失败
testCheckpointFailure()

// 4. 理解 Checkpoint 超时
testCheckpointTimeout()

// 5. 理解状态恢复
testRestoreFromCheckpoint()
```

#### 14. Checkpoint 相关测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **PendingCheckpointTest** | `flink-runtime/.../checkpoint/` | ⭐⭐⭐ | ⭐⭐⭐⭐ | 待完成检查点测试 |
| **CompletedCheckpointTest** | 同上 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 已完成检查点测试 |
| **CheckpointFailureManagerTest** | 同上 | ⭐⭐⭐ | ⭐⭐⭐ | 失败管理器测试 |
| **DefaultCheckpointPlanCalculatorTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 检查点计划计算 |

#### 15. 状态管理测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **KeyedStateBackendTest** | `flink-runtime/.../state/` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 键控状态后端测试 |
| **StateBackendTestBase** | 同上 | ⭐⭐⭐ | ⭐⭐⭐⭐ | 状态后端测试基类 |
| **HeapKeyedStateBackendTest** | `flink-state-backends/.../heap/` | ⭐⭐⭐ | ⭐⭐⭐⭐ | 堆状态后端测试 |
| **RocksDBStateBackendTest** | `flink-state-backends/.../rocksdb/` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | RocksDB 后端测试 |

**学习重点**:

- ValueState, ListState, MapState 的使用
- 状态的快照和恢复
- 不同 StateBackend 的特性
- TTL 机制

#### 16. Channel State 测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **ChannelStateWriterImplTest** | `flink-runtime/.../checkpoint/channel/` | ⭐⭐⭐⭐ | ⭐⭐⭐ | Channel 状态写入测试 |
| **SequentialChannelStateReaderImplTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐ | Channel 状态读取测试 |

---

### 第 11-12 周: 高级主题

#### 17. 调度器测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **DefaultSchedulerTest** | `flink-runtime/.../scheduler/` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 默认调度器测试 |
| **SchedulerTestBase** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 调度器测试基类 |
| **ExecutionSlotAllocatorTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐ | Slot 分配测试 |

#### 18. Slot 管理测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **SlotPoolTest** | `flink-runtime/.../jobmaster/slotpool/` | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | Slot 池测试 |
| **DeclarativeSlotPoolTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 声明式 Slot 池 |
| **PhysicalSlotRequestBulkCheckerImplTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐ | Slot 请求测试 |

#### 19. TaskExecutor 测试

| 文件 | 路径 | 难度 | 推荐指数 | 说明 |
|------|------|------|---------|------|
| **TaskExecutorTest** | `flink-runtime/.../taskexecutor/` | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 任务执行器测试 |
| **TaskExecutorSubmissionTest** | 同上 | ⭐⭐⭐⭐ | ⭐⭐⭐ | 任务提交测试 |

---

## 🔍 按功能分类

### Watermark 和时间

| 文件 | 路径 | 难度 | 推荐指数 |
|------|------|------|---------|
| **WatermarkTest** | `flink-streaming-java/.../watermark/` | ⭐⭐ | ⭐⭐⭐⭐ |
| **WatermarkGeneratorTest** | 同上 | ⭐⭐⭐ | ⭐⭐⭐ |
| **TimestampAssignerTest** | 同上 | ⭐⭐ | ⭐⭐⭐ |

### 分区策略

| 文件 | 路径 | 难度 | 推荐指数 |
|------|------|------|---------|
| **StreamPartitionerTest** | `flink-streaming-java/.../partitioner/` | ⭐⭐ | ⭐⭐⭐⭐ |
| **HashPartitionerTest** | 同上 | ⭐⭐ | ⭐⭐⭐ |
| **KeyGroupRangeAssignmentTest** | `flink-runtime/.../state/` | ⭐⭐⭐ | ⭐⭐⭐ |

### 类型系统

| 文件 | 路径 | 难度 | 推荐指数 |
|------|------|------|---------|
| **TypeInformationTest** | `flink-core/.../api/common/typeinfo/` | ⭐⭐ | ⭐⭐⭐ |
| **TypeSerializerTest** | `flink-core/.../api/common/typeutils/` | ⭐⭐⭐ | ⭐⭐⭐ |

---

## 🎯 推荐阅读顺序

### 初学者路径 (第 1-4 周)

```
1. StreamExecutionEnvironmentTest      (理解环境)
   ↓
2. StreamMapTest                        (理解基础算子)
   ↓
3. OneInputStreamOperatorTestHarness   (理解测试框架)
   ↓
4. 编写自己的算子测试                    (实践)
   ↓
5. KeyedStateBackendTest               (理解状态)
```

### 进阶路径 (第 5-8 周)

```
1. StreamGraphGeneratorTest             (理解图生成)
   ↓
2. StreamingJobGraphGeneratorTest       (理解算子链)
   ↓
3. StreamTaskTest                       (理解任务执行)
   ↓
4. StreamTaskMailboxTestHarness        (掌握新测试框架)
   ↓
5. InputGateTest / ResultPartitionTest  (理解网络栈)
```

### 高级路径 (第 9-12 周)

```
1. CheckpointCoordinatorTest            (理解 Checkpoint)
   ↓
2. CheckpointCoordinatorTriggeringTest  (理解触发机制)
   ↓
3. RocksDBStateBackendTest              (理解状态后端)
   ↓
4. DefaultSchedulerTest                 (理解调度)
   ↓
5. TaskExecutorTest                     (理解任务执行器)
```

---

## 📝 测试文件命名规范

Flink 测试文件遵循以下命名规范:

### 单元测试

```
{ClassName}Test.java           # 基本单元测试
例如: StreamMapTest.java
```

### 集成测试

```
{ClassName}ITCase.java         # 集成测试用例
例如: StreamTaskITCase.java
```

### 性能测试

```
{ClassName}BenchmarkTest.java  # 性能基准测试
例如: SerializationBenchmarkTest.java
```

### 测试工具

```
{ClassName}TestHarness.java    # 测试框架
例如: OneInputStreamOperatorTestHarness.java

{ClassName}TestBase.java       # 测试基类
例如: StateBackendTestBase.java

Mock{ClassName}.java           # Mock 对象
例如: MockEnvironment.java

Testing{ClassName}.java        # 测试工具
例如: TestingTaskManagerRuntimeInfo.java
```

---

## 🔍 快速搜索技巧

### 使用命令行

```bash
# 1. 查找某个类的测试
find . -name "*StreamTaskTest.java"

# 2. 查找包含特定内容的测试
grep -r "checkpoint" --include="*Test.java" | head -20

# 3. 查找使用某个 Harness 的测试
grep -r "OneInputStreamOperatorTestHarness" --include="*.java"

# 4. 统计测试文件数量
find . -name "*Test.java" | wc -l

# 5. 查找某个功能的集成测试
find . -name "*ITCase.java" | grep -i "window"
```

### 在 IDE 中搜索

**IntelliJ IDEA**:

```
Ctrl + Shift + F (Windows/Linux)
Command + Shift + F (Mac)

搜索范围: Test Sources
文件掩码: *.java
搜索内容: 你要找的类或功能
```

**查找用法**:

```
Alt + F7: 查找某个类/方法的使用位置
Ctrl + Alt + H: 查看调用层次
Ctrl + H: 查看类型层次
```

---

## 📚 测试工具类详解

### 核心测试工具类

#### 1. OneInputStreamOperatorTestHarness

**位置**: `flink-streaming-java/.../util/OneInputStreamOperatorTestHarness.java`

**用途**: 测试单输入算子

**关键方法**:

```java
// 初始化
harness.open()

// 输入数据
harness.processElement(StreamRecord<IN>)

// 输入 Watermark
harness.processWatermark(Watermark)

// 获取输出
harness.extractOutputStreamRecords()
harness.getOutput()

// 关闭
harness.close()
```

**适用场景**:

- Map, Filter, FlatMap 等单输入算子
- 无状态算子
- 简单的有状态算子

#### 2. KeyedOneInputStreamOperatorTestHarness

**位置**: 同上

**用途**: 测试键控算子

**额外功能**:

- 支持 KeyedState
- 支持 Checkpoint
- 支持状态恢复

**适用场景**:

- 使用 KeyedState 的算子
- 需要测试 Checkpoint 的算子

#### 3. StreamTaskMailboxTestHarness

**位置**: `flink-streaming-java/.../tasks/StreamTaskMailboxTestHarness.java`

**用途**: 测试完整的 StreamTask

**特点**:

- 更贴近实际运行环境
- 支持 Mailbox 模型
- 支持多输入

**使用 Builder**:

```java
StreamTaskMailboxTestHarness<OUT> harness =
    new StreamTaskMailboxTestHarnessBuilder<>(
        OneInputStreamTask::new,
        outputType)
    .addInput(inputType)
    .setupOutputForSingletonOperatorChain(operator)
    .build();
```

#### 4. Mock 环境类

| 类名 | 用途 |
|------|------|
| **StreamMockEnvironment** | 模拟执行环境 |
| **MockInputSplitProvider** | 模拟输入分片提供者 |
| **TestTaskStateManager** | 模拟任务状态管理器 |
| **TestingTaskManagerRuntimeInfo** | 模拟 TaskManager 信息 |

---

## 🎓 学习建议

### 1. 从简单开始

```
入门级 ⭐
  → StreamExecutionEnvironmentTest
  → StreamMapTest
  → DataStreamTest

进阶级 ⭐⭐⭐
  → WindowOperatorTest
  → StreamTaskTest
  → CheckpointCoordinatorTest

专家级 ⭐⭐⭐⭐⭐
  → DefaultSchedulerTest
  → TaskExecutorTest
  → ChannelStateWriterImplTest
```

### 2. 结合源码阅读

```
1. 先运行测试
2. 设置断点调试
3. 跟踪到源码实现
4. 理解实现原理
5. 修改测试验证理解
```

### 3. 关注测试模式

- **Given-When-Then**: 准备 - 执行 - 验证
- **Setup-Exercise-Verify**: 设置 - 执行 - 验证
- **Arrange-Act-Assert**: 安排 - 行动 - 断言

### 4. 学习测试技巧

- Mock 的使用
- Fixture 的设计
- 边界条件测试
- 异常情况测试
- 性能测试

---

## 📊 测试覆盖率统计

### 主要模块测试覆盖

| 模块 | 测试文件数 | 代码覆盖率 | 说明 |
|------|-----------|-----------|------|
| flink-streaming-java | ~500 | ~80% | 流处理核心 |
| flink-runtime | ~800 | ~75% | 运行时核心 |
| flink-core | ~300 | ~85% | 基础组件 |
| flink-table | ~600 | ~70% | Table/SQL |
| flink-state-backends | ~100 | ~75% | 状态后端 |

**注**: 数据为估算值,实际数据可能有变化

---

## 🔗 相关文档

- [Flink 源码阅读指南](./flink-source-reading-guide.md) - 完整学习路线
- [Flink 学习计划表](./flink-learning-schedule.md) - 12周学习计划
- [Flink 代码示例集](./flink-code-examples.md) - 具体代码示例

---

## 💡 常见问题

### Q1: 如何运行单个测试?

**IntelliJ IDEA**:

```
1. 打开测试类
2. 右键测试方法
3. 选择 "Run 'testMethodName'"
```

**命令行**:

```bash
mvn test -Dtest=StreamMapTest
mvn test -Dtest=StreamMapTest#testBasicMap
```

### Q2: 测试失败怎么办?

1. 查看错误信息
2. 检查依赖是否正确
3. 清理重新编译: `mvn clean compile`
4. 更新 IDE 缓存: File → Invalidate Caches

### Q3: 如何添加自己的测试?

```java
// 1. 在对应的 test 目录创建测试类
package org.apache.flink.examples.test;

import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

public class MyOperatorTest {
    @Test
    public void testMyFeature() {
        // TODO: 实现测试
    }
}
```

### Q4: 如何 Mock 外部依赖?

```java
// 使用 Mockito
import static org.mockito.Mockito.*;

ExternalService mockService = mock(ExternalService.class);
when(mockService.getData()).thenReturn("test-data");

// 使用 Flink 提供的 Mock 类
StreamMockEnvironment mockEnv = new StreamMockEnvironment(...);
```

---

**版本历史**:

- v1.0 (2025-01-11): 初始版本,包含主要测试文件索引

---

**持续更新中...**

随着 Flink 版本迭代,测试文件可能会有变化。建议定期查看最新的源码。
