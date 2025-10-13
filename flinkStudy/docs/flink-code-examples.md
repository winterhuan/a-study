# Apache Flink 源码学习代码示例集

> **版本**: 基于 Apache Flink 主分支
> **更新日期**: 2025-01-11
> **目标**: 通过完整代码示例加速 Flink 源码学习

## 📖 文档说明

本文档提供了一系列完整的代码示例,涵盖:

- ✅ Test Harness 的使用
- ✅ 自定义算子的实现和测试
- ✅ 状态管理的使用
- ✅ Checkpoint 的测试
- ✅ 从测试跟踪到源码的实例

所有示例都可以直接运行,帮助你快速理解 Flink 的核心机制。

---

## 📂 示例索引

| 序号 | 示例名称 | 难度 | 涵盖知识点 |
|------|---------|------|-----------|
| 1 | [WordCount 完整分析](#1-wordcount-完整分析) | ⭐ | DataStream API, 算子链 |
| 2 | [使用 OneInputStreamOperatorTestHarness](#2-使用-oneinputstreamoperatortestharness) | ⭐⭐ | 测试框架基础 |
| 3 | [自定义 Map 算子及测试](#3-自定义-map-算子及测试) | ⭐⭐ | 算子实现, 单元测试 |
| 4 | [有状态的计数器算子](#4-有状态的计数器算子) | ⭐⭐⭐ | KeyedState, Checkpoint |
| 5 | [滑动窗口 Top-N](#5-滑动窗口-top-n) | ⭐⭐⭐ | 窗口, ProcessFunction |
| 6 | [使用 StreamTaskMailboxTestHarness](#6-使用-streamtaskmailboxtestharness) | ⭐⭐⭐⭐ | 任务测试, Mailbox 模型 |
| 7 | [Checkpoint 完整流程测试](#7-checkpoint-完整流程测试) | ⭐⭐⭐⭐ | CheckpointCoordinator |
| 8 | [自定义 StateBackend 实现](#8-自定义-statebackend-实现) | ⭐⭐⭐⭐⭐ | 状态后端, 高级特性 |
| 9 | [从测试跟踪到源码实例](#9-从测试跟踪到源码实例) | ⭐⭐⭐ | 调试技巧 |
| 10 | [性能测试框架](#10-性能测试框架) | ⭐⭐⭐⭐ | 性能分析 |

---

## 1. WordCount 完整分析

### 📝 示例说明

这是 Flink 最经典的示例,展示了:

- StreamExecutionEnvironment 的使用
- DataStream API 基本操作
- 算子链的形成
- 批流统一的执行模式

### 💻 完整代码

```java
package org.apache.flink.examples;

import org.apache.flink.api.common.RuntimeExecutionMode;
import org.apache.flink.api.common.functions.FlatMapFunction;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.util.Collector;

/**
 * 经典的 WordCount 示例
 *
 * 知识点:
 * 1. StreamExecutionEnvironment 的创建和配置
 * 2. 数据源的创建 (fromData)
 * 3. 转换操作 (flatMap, keyBy, sum)
 * 4. 结果输出 (print)
 * 5. 作业执行 (execute)
 */
public class WordCountExample {

    public static void main(String[] args) throws Exception {
        // 1. 创建执行环境
        final StreamExecutionEnvironment env =
            StreamExecutionEnvironment.getExecutionEnvironment();

        // 2. 设置运行模式
        // STREAMING: 流式处理,产生增量更新
        // BATCH: 批处理,只在最后产生结果
        // AUTOMATIC: 根据数据源自动选择
        env.setRuntimeMode(RuntimeExecutionMode.AUTOMATIC);

        // 3. 设置并行度(可选)
        env.setParallelism(4);

        // 4. 创建数据源
        DataStream<String> text = env.fromData(
            "To be, or not to be,--that is the question:--",
            "Whether 'tis nobler in the mind to suffer",
            "The slings and arrows of outrageous fortune",
            "Or to take arms against a sea of troubles,"
        );

        // 5. 数据转换
        DataStream<Tuple2<String, Integer>> counts = text
            // flatMap: 一对多转换
            .flatMap(new Tokenizer())
            .name("tokenizer")  // 设置算子名称,便于监控
            // keyBy: 按 key 分组,这里按单词分组
            .keyBy(value -> value.f0)
            // sum: 聚合操作,累加计数
            .sum(1)
            .name("counter");

        // 6. 输出结果
        counts.print().name("print-sink");

        // 7. 执行作业
        // 注意: Flink 是懒执行的,只有调用 execute() 才会真正运行
        env.execute("WordCount Example");
    }

    /**
     * 分词器: 将句子拆分成单词
     *
     * 实现 FlatMapFunction 接口:
     * - 输入: String (一行文本)
     * - 输出: Tuple2<String, Integer> (单词, 计数)
     */
    public static final class Tokenizer
            implements FlatMapFunction<String, Tuple2<String, Integer>> {

        @Override
        public void flatMap(String value, Collector<Tuple2<String, Integer>> out) {
            // 1. 转小写并按非单词字符分割
            String[] tokens = value.toLowerCase().split("\\W+");

            // 2. 输出每个单词及其初始计数 1
            for (String token : tokens) {
                if (token.length() > 0) {
                    out.collect(new Tuple2<>(token, 1));
                }
            }
        }
    }
}
```

### 🔍 执行流程分析

```
用户代码                        Flink 内部转换
────────────────────────────────────────────────

env.fromData(...)           → SourceTransformation
    ↓
.flatMap(new Tokenizer())   → OneInputTransformation
    ↓                           (FlatMap 算子)
.keyBy(value -> value.f0)   → PartitionTransformation
    ↓                           (KeyBy 不是算子,是重分区)
.sum(1)                     → OneInputTransformation
    ↓                           (StreamGroupedReduce 算子)
.print()                    → SinkTransformation
    ↓                           (Print Sink)
env.execute()               → 生成 StreamGraph
                            → 生成 JobGraph (算子链优化)
                            → 提交执行
```

### 🎯 算子链分析

在这个例子中,以下算子会被链在一起:

```
Source → FlatMap → KeyBy → Reduce → Sink
         ─────────链1──────    ─────链2────
```

**链 1**: Source + FlatMap (满足链条件)

- 同一并行度
- 同一 Slot Sharing Group
- ForwardPartitioner

**链 2**: Reduce + Sink (满足链条件)

**不链**: KeyBy 是分区操作,会打断算子链

### 📚 从这个例子学到的

1. **从 `env.execute()` 入手**:

   ```bash
   # 设置断点
   StreamExecutionEnvironment.java:execute()

   # 观察调用栈
   execute()
     → executeAsync()
       → getStreamGraph()
         → StreamGraphGenerator.generate()
       → PipelineExecutor.execute()
   ```

2. **查看生成的 StreamGraph**:

   ```java
   StreamGraph streamGraph = env.getStreamGraph();
   System.out.println("Nodes: " + streamGraph.getStreamNodes().size());
   streamGraph.getStreamNodes().forEach((id, node) -> {
       System.out.println("Node " + id + ": " + node.getOperatorName());
   });
   ```

3. **理解算子类型**:
   - `Source`: `SourceTransformation`
   - `FlatMap`: `OneInputStreamOperator`
   - `KeyBy`: `PartitionTransformation` (不是算子!)
   - `Sum`: `StreamGroupedReduce`
   - `Sink`: `SinkTransformation`

---

## 2. 使用 OneInputStreamOperatorTestHarness

### 📝 示例说明

`OneInputStreamOperatorTestHarness` 是测试单输入算子最常用的工具,可以:

- 独立测试算子逻辑
- 控制输入数据和时间
- 验证输出结果
- 测试状态和 Checkpoint

### 💻 完整代码

```java
package org.apache.flink.test.examples;

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.streaming.api.operators.StreamMap;
import org.apache.flink.streaming.runtime.streamrecord.StreamRecord;
import org.apache.flink.streaming.util.OneInputStreamOperatorTestHarness;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * OneInputStreamOperatorTestHarness 使用示例
 *
 * 测试一个简单的 Map 算子
 */
public class MapOperatorTest {

    /**
     * 测试基本功能: 字符串转大写
     */
    @Test
    public void testBasicMap() throws Exception {
        // 1. 创建算子
        StreamMap<String, String> operator = new StreamMap<>(
            new MapFunction<String, String>() {
                @Override
                public String map(String value) {
                    return value.toUpperCase();
                }
            }
        );

        // 2. 创建测试 Harness
        OneInputStreamOperatorTestHarness<String, String> harness =
            new OneInputStreamOperatorTestHarness<>(operator);

        // 3. 打开算子(初始化)
        harness.open();

        // 4. 输入测试数据
        harness.processElement(new StreamRecord<>("hello"));
        harness.processElement(new StreamRecord<>("world"));

        // 5. 获取输出结果
        List<StreamRecord<String>> output = harness.extractOutputStreamRecords();

        // 6. 验证结果
        assertThat(output).hasSize(2);
        assertThat(output.get(0).getValue()).isEqualTo("HELLO");
        assertThat(output.get(1).getValue()).isEqualTo("WORLD");

        // 7. 关闭算子
        harness.close();
    }

    /**
     * 测试带时间戳的数据处理
     */
    @Test
    public void testMapWithTimestamp() throws Exception {
        StreamMap<String, String> operator = new StreamMap<>(
            value -> value.toUpperCase()
        );

        OneInputStreamOperatorTestHarness<String, String> harness =
            new OneInputStreamOperatorTestHarness<>(operator);

        harness.open();

        // 输入带时间戳的数据
        harness.processElement(new StreamRecord<>("hello", 1000L));
        harness.processElement(new StreamRecord<>("world", 2000L));

        List<StreamRecord<String>> output = harness.extractOutputStreamRecords();

        // 验证时间戳被保留
        assertThat(output.get(0).getTimestamp()).isEqualTo(1000L);
        assertThat(output.get(1).getTimestamp()).isEqualTo(2000L);

        harness.close();
    }

    /**
     * 测试 Watermark 处理
     */
    @Test
    public void testMapWithWatermark() throws Exception {
        StreamMap<String, String> operator = new StreamMap<>(
            value -> value.toUpperCase()
        );

        OneInputStreamOperatorTestHarness<String, String> harness =
            new OneInputStreamOperatorTestHarness<>(operator);

        harness.open();

        // 输入数据和 Watermark
        harness.processElement(new StreamRecord<>("hello", 1000L));
        harness.processWatermark(new org.apache.flink.streaming.api.watermark.Watermark(1500L));
        harness.processElement(new StreamRecord<>("world", 2000L));

        // 获取所有输出(包括 Watermark)
        List<Object> output = harness.getOutput();

        // 验证输出顺序
        assertThat(output).hasSize(3);
        assertThat(output.get(0)).isInstanceOf(StreamRecord.class);
        assertThat(output.get(1)).isInstanceOf(org.apache.flink.streaming.api.watermark.Watermark.class);
        assertThat(output.get(2)).isInstanceOf(StreamRecord.class);

        harness.close();
    }
}
```

### 🔍 Test Harness 工作原理

```java
// 1. 创建 Mock 环境
OneInputStreamOperatorTestHarness 内部:
├── StreamMockEnvironment: 模拟执行环境
├── StreamConfig: 算子配置
├── Output Collector: 收集输出
└── Time Service: 时间服务

// 2. 算子生命周期
harness.open()              → operator.setup()
                            → operator.initializeState()
                            → operator.open()

harness.processElement()    → operator.processElement()

harness.close()             → operator.close()
                            → operator.dispose()

// 3. 数据流转
输入数据 → processElement()
         → operator.processElement()
         → output.collect()
         → outputList.add()
```

### 📚 关键 API

| 方法 | 作用 | 示例 |
|------|------|------|
| `open()` | 初始化算子 | `harness.open()` |
| `processElement()` | 输入数据 | `harness.processElement(new StreamRecord<>("data"))` |
| `processWatermark()` | 输入 Watermark | `harness.processWatermark(new Watermark(1000L))` |
| `extractOutputStreamRecords()` | 获取输出记录 | `List<StreamRecord> output = harness.extractOutputStreamRecords()` |
| `getOutput()` | 获取所有输出 | `List<Object> output = harness.getOutput()` |
| `close()` | 关闭算子 | `harness.close()` |

---

## 3. 自定义 Map 算子及测试

### 📝 示例说明

展示如何:

- 实现自定义算子
- 继承 `AbstractStreamOperator`
- 编写完整的单元测试
- 处理异常情况

### 💻 完整代码

```java
package org.apache.flink.examples.custom;

import org.apache.flink.configuration.Configuration;
import org.apache.flink.streaming.api.operators.AbstractStreamOperator;
import org.apache.flink.streaming.api.operators.OneInputStreamOperator;
import org.apache.flink.streaming.runtime.streamrecord.StreamRecord;

/**
 * 自定义 Map 算子: 添加前缀并转大写
 *
 * 继承关系:
 * AbstractStreamOperator (基类)
 *   ↓
 * PrefixUpperCaseOperator (自定义算子)
 *
 * 实现接口:
 * OneInputStreamOperator (单输入算子接口)
 */
public class PrefixUpperCaseOperator
        extends AbstractStreamOperator<String>
        implements OneInputStreamOperator<String, String> {

    private static final long serialVersionUID = 1L;

    // 配置参数
    private final String prefix;

    // 运行时状态
    private transient long processedCount;

    public PrefixUpperCaseOperator(String prefix) {
        this.prefix = prefix;
    }

    /**
     * 算子初始化
     * 在算子启动时调用一次
     */
    @Override
    public void open() throws Exception {
        super.open();
        this.processedCount = 0;

        // 可以在这里:
        // 1. 初始化外部连接
        // 2. 加载配置
        // 3. 注册 Metrics

        getRuntimeContext().getMetricGroup()
            .counter("processedElements");
    }

    /**
     * 处理每一个输入元素
     * 这是算子的核心逻辑
     */
    @Override
    public void processElement(StreamRecord<String> element) throws Exception {
        // 1. 获取输入值
        String value = element.getValue();

        // 2. 执行转换逻辑
        String result = prefix + value.toUpperCase();

        // 3. 输出结果(保留原始时间戳)
        output.collect(element.replace(result));

        // 4. 更新计数器
        processedCount++;
    }

    /**
     * 算子关闭
     * 在算子停止时调用
     */
    @Override
    public void close() throws Exception {
        super.close();

        // 可以在这里:
        // 1. 关闭外部连接
        // 2. 清理资源
        // 3. 输出统计信息

        System.out.println("Processed " + processedCount + " elements");
    }
}
```

### 🧪 完整测试代码

```java
package org.apache.flink.examples.custom;

import org.apache.flink.streaming.runtime.streamrecord.StreamRecord;
import org.apache.flink.streaming.util.OneInputStreamOperatorTestHarness;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;

/**
 * PrefixUpperCaseOperator 的完整测试
 */
public class PrefixUpperCaseOperatorTest {

    /**
     * 测试正常情况
     */
    @Test
    public void testNormalCase() throws Exception {
        // 1. 创建算子实例
        PrefixUpperCaseOperator operator = new PrefixUpperCaseOperator("[PREFIX]");

        // 2. 创建测试 Harness
        OneInputStreamOperatorTestHarness<String, String> harness =
            new OneInputStreamOperatorTestHarness<>(operator);

        // 3. 打开算子
        harness.open();

        // 4. 输入测试数据
        harness.processElement(new StreamRecord<>("hello"));
        harness.processElement(new StreamRecord<>("world"));

        // 5. 获取输出
        List<StreamRecord<String>> output = harness.extractOutputStreamRecords();

        // 6. 验证结果
        assertThat(output).hasSize(2);
        assertThat(output.get(0).getValue()).isEqualTo("[PREFIX]HELLO");
        assertThat(output.get(1).getValue()).isEqualTo("[PREFIX]WORLD");

        // 7. 关闭算子
        harness.close();
    }

    /**
     * 测试空字符串
     */
    @Test
    public void testEmptyString() throws Exception {
        PrefixUpperCaseOperator operator = new PrefixUpperCaseOperator("[PREFIX]");
        OneInputStreamOperatorTestHarness<String, String> harness =
            new OneInputStreamOperatorTestHarness<>(operator);

        harness.open();

        // 输入空字符串
        harness.processElement(new StreamRecord<>(""));

        List<StreamRecord<String>> output = harness.extractOutputStreamRecords();

        // 验证: 空字符串也会被处理
        assertThat(output).hasSize(1);
        assertThat(output.get(0).getValue()).isEqualTo("[PREFIX]");

        harness.close();
    }

    /**
     * 测试时间戳保留
     */
    @Test
    public void testTimestampPreservation() throws Exception {
        PrefixUpperCaseOperator operator = new PrefixUpperCaseOperator("[PREFIX]");
        OneInputStreamOperatorTestHarness<String, String> harness =
            new OneInputStreamOperatorTestHarness<>(operator);

        harness.open();

        // 输入带时间戳的数据
        long timestamp = 123456789L;
        harness.processElement(new StreamRecord<>("hello", timestamp));

        List<StreamRecord<String>> output = harness.extractOutputStreamRecords();

        // 验证: 时间戳被保留
        assertThat(output.get(0).getTimestamp()).isEqualTo(timestamp);

        harness.close();
    }

    /**
     * 测试空前缀
     */
    @Test
    public void testEmptyPrefix() throws Exception {
        PrefixUpperCaseOperator operator = new PrefixUpperCaseOperator("");
        OneInputStreamOperatorTestHarness<String, String> harness =
            new OneInputStreamOperatorTestHarness<>(operator);

        harness.open();
        harness.processElement(new StreamRecord<>("hello"));

        List<StreamRecord<String>> output = harness.extractOutputStreamRecords();

        // 验证: 只转大写,没有前缀
        assertThat(output.get(0).getValue()).isEqualTo("HELLO");

        harness.close();
    }

    /**
     * 测试特殊字符
     */
    @Test
    public void testSpecialCharacters() throws Exception {
        PrefixUpperCaseOperator operator = new PrefixUpperCaseOperator("[PREFIX]");
        OneInputStreamOperatorTestHarness<String, String> harness =
            new OneInputStreamOperatorTestHarness<>(operator);

        harness.open();

        // 输入包含特殊字符的字符串
        harness.processElement(new StreamRecord<>("hello@world#123"));

        List<StreamRecord<String>> output = harness.extractOutputStreamRecords();

        // 验证: 特殊字符也被转大写
        assertThat(output.get(0).getValue()).isEqualTo("[PREFIX]HELLO@WORLD#123");

        harness.close();
    }

    /**
     * 测试多条数据处理
     */
    @Test
    public void testMultipleElements() throws Exception {
        PrefixUpperCaseOperator operator = new PrefixUpperCaseOperator("[PREFIX]");
        OneInputStreamOperatorTestHarness<String, String> harness =
            new OneInputStreamOperatorTestHarness<>(operator);

        harness.open();

        // 输入多条数据
        for (int i = 0; i < 100; i++) {
            harness.processElement(new StreamRecord<>("data" + i));
        }

        List<StreamRecord<String>> output = harness.extractOutputStreamRecords();

        // 验证: 所有数据都被正确处理
        assertThat(output).hasSize(100);
        for (int i = 0; i < 100; i++) {
            assertThat(output.get(i).getValue()).isEqualTo("[PREFIX]DATA" + i);
        }

        harness.close();
    }
}
```

### 🎯 学习重点

1. **算子生命周期**:

   ```
   构造函数 → open() → processElement() → close()
   ```

2. **如何输出数据**:

   ```java
   // 方式1: 保留原始时间戳
   output.collect(element.replace(newValue));

   // 方式2: 使用当前时间戳
   output.collect(new StreamRecord<>(newValue));
   ```

3. **如何注册 Metrics**:

   ```java
   getRuntimeContext().getMetricGroup()
       .counter("myCounter")
       .inc();
   ```

4. **测试的完整性**:
   - ✅ 正常情况
   - ✅ 边界情况(空字符串)
   - ✅ 时间戳处理
   - ✅ 特殊字符
   - ✅ 大量数据

---

## 4. 有状态的计数器算子

### 📝 示例说明

展示如何:

- 使用 KeyedState
- 实现 Checkpoint
- 测试状态的持久化和恢复

### 💻 完整代码

```java
package org.apache.flink.examples.stateful;

import org.apache.flink.api.common.functions.RichFlatMapFunction;
import org.apache.flink.api.common.state.ValueState;
import org.apache.flink.api.common.state.ValueStateDescriptor;
import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.configuration.Configuration;
import org.apache.flink.util.Collector;

/**
 * 有状态的计数器: 统计每个 key 出现的次数
 *
 * 使用 ValueState 存储计数
 * 支持 Checkpoint 和故障恢复
 */
public class StatefulCounter
        extends RichFlatMapFunction<String, Tuple2<String, Long>> {

    private static final long serialVersionUID = 1L;

    // 状态句柄
    private transient ValueState<Long> countState;

    @Override
    public void open(Configuration parameters) throws Exception {
        super.open(parameters);

        // 创建状态描述符
        ValueStateDescriptor<Long> descriptor = new ValueStateDescriptor<>(
            "count-state",  // 状态名称
            Types.LONG      // 状态类型
        );

        // 获取状态句柄
        countState = getRuntimeContext().getState(descriptor);
    }

    @Override
    public void flatMap(String key, Collector<Tuple2<String, Long>> out) throws Exception {
        // 1. 读取当前计数(如果不存在则为 null)
        Long currentCount = countState.value();

        // 2. 增加计数
        if (currentCount == null) {
            currentCount = 0L;
        }
        currentCount++;

        // 3. 更新状态
        countState.update(currentCount);

        // 4. 输出结果
        out.collect(new Tuple2<>(key, currentCount));
    }
}
```

### 🧪 完整测试代码

```java
package org.apache.flink.examples.stateful;

import org.apache.flink.api.common.typeinfo.Types;
import org.apache.flink.api.java.tuple.Tuple2;
import org.apache.flink.runtime.checkpoint.OperatorSubtaskState;
import org.apache.flink.streaming.runtime.streamrecord.StreamRecord;
import org.apache.flink.streaming.util.KeyedOneInputStreamOperatorTestHarness;
import org.apache.flink.streaming.util.OneInputStreamOperatorTestHarness;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * StatefulCounter 的完整测试
 * 包含状态和 Checkpoint 测试
 */
public class StatefulCounterTest {

    /**
     * 测试基本计数功能
     */
    @Test
    public void testBasicCounting() throws Exception {
        // 1. 创建 KeyedTestHarness (用于测试 KeyedState)
        KeyedOneInputStreamOperatorTestHarness<String, String, Tuple2<String, Long>> harness =
            new KeyedOneInputStreamOperatorTestHarness<>(
                new StreamFlatMap<>(new StatefulCounter()),
                key -> key,  // KeySelector
                Types.STRING  // Key 类型
            );

        // 2. 打开算子
        harness.open();

        // 3. 输入测试数据(相同的 key)
        harness.processElement("hello", 1000L);
        harness.processElement("hello", 2000L);
        harness.processElement("hello", 3000L);

        // 4. 获取输出
        List<Tuple2<String, Long>> output = harness.extractOutputValues();

        // 5. 验证: 计数递增
        assertThat(output).hasSize(3);
        assertThat(output.get(0).f1).isEqualTo(1L);
        assertThat(output.get(1).f1).isEqualTo(2L);
        assertThat(output.get(2).f1).isEqualTo(3L);

        harness.close();
    }

    /**
     * 测试多个 key
     */
    @Test
    public void testMultipleKeys() throws Exception {
        KeyedOneInputStreamOperatorTestHarness<String, String, Tuple2<String, Long>> harness =
            new KeyedOneInputStreamOperatorTestHarness<>(
                new StreamFlatMap<>(new StatefulCounter()),
                key -> key,
                Types.STRING
            );

        harness.open();

        // 输入不同的 key
        harness.processElement("hello", 1000L);
        harness.processElement("world", 1500L);
        harness.processElement("hello", 2000L);
        harness.processElement("world", 2500L);
        harness.processElement("hello", 3000L);

        List<Tuple2<String, Long>> output = harness.extractOutputValues();

        // 验证: 每个 key 独立计数
        assertThat(output).hasSize(5);
        assertThat(output.get(0)).isEqualTo(new Tuple2<>("hello", 1L));
        assertThat(output.get(1)).isEqualTo(new Tuple2<>("world", 1L));
        assertThat(output.get(2)).isEqualTo(new Tuple2<>("hello", 2L));
        assertThat(output.get(3)).isEqualTo(new Tuple2<>("world", 2L));
        assertThat(output.get(4)).isEqualTo(new Tuple2<>("hello", 3L));

        harness.close();
    }

    /**
     * 测试 Checkpoint 和状态恢复
     *
     * 这是最重要的测试!
     */
    @Test
    public void testCheckpointAndRestore() throws Exception {
        KeyedOneInputStreamOperatorTestHarness<String, String, Tuple2<String, Long>> harness =
            new KeyedOneInputStreamOperatorTestHarness<>(
                new StreamFlatMap<>(new StatefulCounter()),
                key -> key,
                Types.STRING
            );

        harness.open();

        // 第一阶段: 处理一些数据
        harness.processElement("hello", 1000L);
        harness.processElement("world", 1500L);
        harness.processElement("hello", 2000L);

        // 触发 Checkpoint,保存状态快照
        OperatorSubtaskState snapshot = harness.snapshot(1L, 2000L);

        // 清理输出
        harness.extractOutputValues();

        // 关闭 Harness
        harness.close();

        // ============ 模拟故障恢复 ============

        // 创建新的 Harness
        KeyedOneInputStreamOperatorTestHarness<String, String, Tuple2<String, Long>> restoredHarness =
            new KeyedOneInputStreamOperatorTestHarness<>(
                new StreamFlatMap<>(new StatefulCounter()),
                key -> key,
                Types.STRING
            );

        // 从快照恢复状态
        restoredHarness.initializeState(snapshot);
        restoredHarness.open();

        // 第二阶段: 继续处理数据
        restoredHarness.processElement("hello", 3000L);  // 应该是 3
        restoredHarness.processElement("world", 3500L);  // 应该是 2

        List<Tuple2<String, Long>> output = restoredHarness.extractOutputValues();

        // 验证: 状态被正确恢复
        assertThat(output).hasSize(2);
        assertThat(output.get(0)).isEqualTo(new Tuple2<>("hello", 3L));  // 恢复后继续计数
        assertThat(output.get(1)).isEqualTo(new Tuple2<>("world", 2L));

        restoredHarness.close();
    }

    /**
     * 测试多次 Checkpoint
     */
    @Test
    public void testMultipleCheckpoints() throws Exception {
        KeyedOneInputStreamOperatorTestHarness<String, String, Tuple2<String, Long>> harness =
            new KeyedOneInputStreamOperatorTestHarness<>(
                new StreamFlatMap<>(new StatefulCounter()),
                key -> key,
                Types.STRING
            );

        harness.open();

        // 第一个 Checkpoint
        harness.processElement("hello", 1000L);
        OperatorSubtaskState snapshot1 = harness.snapshot(1L, 1000L);

        // 第二个 Checkpoint
        harness.processElement("hello", 2000L);
        OperatorSubtaskState snapshot2 = harness.snapshot(2L, 2000L);

        // 第三个 Checkpoint
        harness.processElement("hello", 3000L);
        OperatorSubtaskState snapshot3 = harness.snapshot(3L, 3000L);

        harness.close();

        // 从第二个 Checkpoint 恢复
        KeyedOneInputStreamOperatorTestHarness<String, String, Tuple2<String, Long>> restoredHarness =
            new KeyedOneInputStreamOperatorTestHarness<>(
                new StreamFlatMap<>(new StatefulCounter()),
                key -> key,
                Types.STRING
            );

        restoredHarness.initializeState(snapshot2);
        restoredHarness.open();

        restoredHarness.processElement("hello", 4000L);

        List<Tuple2<String, Long>> output = restoredHarness.extractOutputValues();

        // 验证: 从第二个 Checkpoint 恢复,计数应该是 3
        assertThat(output.get(0).f1).isEqualTo(3L);

        restoredHarness.close();
    }
}
```

### 🎯 学习重点

1. **状态的使用**:

   ```java
   // 1. 定义状态描述符
   ValueStateDescriptor<Long> descriptor =
       new ValueStateDescriptor<>("name", Types.LONG);

   // 2. 获取状态句柄
   ValueState<Long> state = getRuntimeContext().getState(descriptor);

   // 3. 读取状态
   Long value = state.value();

   // 4. 更新状态
   state.update(newValue);

   // 5. 清除状态
   state.clear();
   ```

2. **Checkpoint 测试流程**:

   ```java
   // 1. 处理数据
   harness.processElement(...);

   // 2. 触发 Checkpoint
   OperatorSubtaskState snapshot = harness.snapshot(checkpointId, timestamp);

   // 3. 关闭原 Harness
   harness.close();

   // 4. 创建新 Harness
   newHarness = new ...();

   // 5. 恢复状态
   newHarness.initializeState(snapshot);
   newHarness.open();

   // 6. 继续处理数据
   newHarness.processElement(...);
   ```

3. **KeyedTestHarness vs OneInputTestHarness**:
   - `KeyedOneInputStreamOperatorTestHarness`: 用于测试 KeyedState
   - `OneInputStreamOperatorTestHarness`: 用于测试无状态算子

---

**[由于篇幅限制,后续示例将在下一部分继续...]**

**已包含的示例**:

1. ✅ WordCount 完整分析
2. ✅ OneInputStreamOperatorTestHarness 使用
3. ✅ 自定义 Map 算子及测试
4. ✅ 有状态的计数器算子

**待补充的示例** (将在 flink-test-index.md 或后续更新中提供):
5. 滑动窗口 Top-N
6. StreamTaskMailboxTestHarness 使用
7. Checkpoint 完整流程测试
8. 自定义 StateBackend
9. 从测试跟踪到源码实例
10. 性能测试框架

---

## 🎓 如何使用这些示例

### 1. 直接运行

```bash
# 复制代码到你的项目
# 添加必要的依赖
# 运行测试
mvn test
```

### 2. 调试学习

```
1. 在关键位置设置断点
2. 单步执行,观察变量
3. 跳转到 Flink 源码
4. 理解执行流程
```

### 3. 修改实验

```
1. 修改算子逻辑
2. 添加新的测试用例
3. 验证你的理解
4. 记录学习笔记
```

---

## 📚 相关文档

- [Flink 源码阅读指南](./flink-source-reading-guide.md) - 完整的学习路线
- [Flink 学习计划表](./flink-learning-schedule.md) - 12周学习计划
- [Flink 测试文件索引](./flink-test-index.md) - 测试文件速查

---

**版本历史**:

- v1.0 (2025-01-11): 初始版本,包含前 4 个核心示例
- 后续版本将补充更多高级示例
