# TestHarness

## AbstractStreamOperatorTestHarness

Base class for {@code AbstractStreamOperator} test harnesses.

AbstractStreamOperatorTestHarness 是Apache Flink中用于测试流处理算子（StreamOperator）的核心测试工具基类。

[AbstractStreamOperatorTestHarness](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java) 是Apache Flink中用于测试流处理算子（StreamOperator）的核心测试工具基类。

### 主要用途

1. **模拟运行时环境**：为流处理算子提供完整的模拟执行环境，无需启动Flink集群即可进行单元测试
2. **状态管理测试**：支持算子状态的初始化、快照、恢复等完整生命周期测试
3. **时间控制**：提供精确的时间控制机制，支持处理时间和事件时间的测试
4. **输出验证**：自动收集和分类算子的各种输出，便于测试验证
5. **资源管理**：实现`AutoCloseable`接口，支持自动资源清理

### 类结构分析

#### 1. 类声明和泛型

```java
public class AbstractStreamOperatorTestHarness<OUT> implements AutoCloseable
```

- **泛型参数**：`<OUT>` 表示算子输出数据的类型
- **接口实现**：`AutoCloseable` 支持try-with-resources语法

#### 2. 核心字段

**算子相关：**

- `operator`：要测试的流处理算子实例
- `factory`：算子工厂，用于创建算子实例

**输出收集：**

- `outputList`：主流输出的线程安全队列
- `sideOutputLists`：侧输出的映射表，按`OutputTag`分类

**环境和配置：**

- `config`：流处理配置
- `executionConfig`：执行配置
- `environment`：模拟的运行时环境

**时间管理：**

- `processingTimeService`：处理时间服务
- `ttlTimeProvider`：TTL（Time To Live）时间提供者

**任务和状态：**

- `mockTask`：模拟的流任务
- `taskStateManager`：任务状态管理器
- `streamTaskStateInitializer`：流任务状态初始化器

#### 3. 构造函数群集

提供多种初始化方式：

- **基础构造函数**：[AbstractStreamOperatorTestHarness(operator, maxParallelism, parallelism, subtaskIndex)](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java)
- **工厂构造函数**：支持传入`StreamOperatorFactory`
- **环境构造函数**：支持自定义`MockEnvironment`
- **ID构造函数**：支持指定`OperatorID`

#### 4. 核心方法

**生命周期管理：**

- [setup()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/OneInputStreamOperatorTestHarness.java:196:4-203:5)：建立算子与模拟环境的连接
- [initializeState()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:512:4-514:5)：初始化算子状态，支持从检查点恢复
- [open()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:712:4-722:5)：打开算子，开始数据处理
- [close()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:774:4-787:5)：清理资源，关闭算子

**状态操作：**

- [snapshot()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:729:4-735:5)：对算子状态进行快照
- [repartitionOperatorState()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:520:4-599:5)：重新分区算子状态（用于并行度测试）
- [repackageState()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:654:4-710:5)：合并多个子任务的状态

**输出提取：**

- [getOutput()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:413:4-416:5)：获取所有输出
- [extractOutputValues()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:443:4-451:5)：提取输出值的列表
- [getSideOutput()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:426:4-429:5)：获取侧输出结果
- [extractOutputStreamRecords()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:431:4-441:5)：提取流记录

**时间控制：**

- [setProcessingTime()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:801:4-803:5)：设置处理时间
- [advanceTime()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:797:4-799:5)：推进时间
- [setStateTtlProcessingTime()](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/AbstractStreamOperatorTestHarness.java:805:4-807:5)：设置状态TTL时间

#### 5. 内部实现

**MockOutput类**：模拟输出实现，负责收集算子发出的：

- 水印（Watermark）
- 水印状态（WatermarkStatus）
- 延迟标记（LatencyMarker）
- 记录属性（RecordAttributes）
- 主流记录和侧输出记录

**TimeServiceManagerProvider**：内部时间服务管理器提供者

### 使用示例

```java
// 创建测试工具
OneInputStreamOperatorTestHarness<MyInput, MyOutput> harness =
    new OneInputStreamOperatorTestHarness<>(myOperator, inputSerializer);

// 设置和初始化
harness.setup(outputSerializer);
harness.initializeEmptyState();
harness.open();

// 输入测试数据
harness.processElement(inputRecord, 0);

// 验证输出
List<MyOutput> results = harness.extractOutputValues();
assertEquals(expectedOutput, results.get(0));

// 清理资源
harness.close();
```

这个类是Flink测试基础设施的核心，为编写可靠的流处理算子测试提供了强大而灵活的基础。它被广泛用于Flink内置算子的测试，以及用户自定义算子的测试开发。

## OneInputStreamOperatorTestHarness

[OneInputStreamOperatorTestHarness](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/OneInputStreamOperatorTestHarness.java) 是Apache Flink中专门用于测试单输入流算子（`OneInputStreamOperator`）的测试工具类。继承自AbstractStreamOperatorTestHarness，并在此基础上增加了针对单输入算子的专用功能和便利方法。

### OneInputStreamOperatorTestHarness 详情

1. **单输入算子专用测试**：专门为只有一个输入流的算子提供测试环境
2. **简化元素输入**：提供便捷的方法来输入测试数据和水印
3. **多输入支持**：同时支持普通单输入算子和多输入算子（通过`MultipleInputStreamOperator`）
4. **完整生命周期测试**：支持从设置到关闭的完整算子生命周期测试

**输入管理：**

- `inputs`：`List<Input>` - 输入通道列表，主要用于多输入算子场景
- `currentWatermark`：`long` - 当前水印的时间戳，跟踪最新的

**元素处理：**

```java
// 用于向测试中的算子输入数据元素（自动包装成`StreamRecord`）
public void processElement(IN value, long timestamp) throws Exception
public void processElement(StreamRecord<IN> element) throws Exception
// 批量处理多个元素
public void processElements(Collection<StreamRecord<IN>> elements) throws Exception
```

**水印处理：**

```java
// 自动包装成`Watermark`对象
public void processWatermark(long watermark) throws Exception
// 处理水印状态变更
public void processWatermarkStatus(WatermarkStatus status) throws Exception
// 获取当前水印值
public long getCurrentWatermark()
```

**特殊算子支持：**

- endInput() 调用 BoundedOneInput.endInput()，用于有界流测试
- processRecordAttributes() 处理记录属性，用于高级流处理场景

**智能路由：**

```java
@Override
public void setup(TypeSerializer<OUT> outputSerializer) {
    super.setup(outputSerializer);
    if (operator instanceof MultipleInputStreamOperator) {
        checkState(inputs.isEmpty());
        inputs.addAll(((MultipleInputStreamOperator) operator).getInputs());
    }
}
```

**动态分发：**

```java
public void processElement(StreamRecord<IN> element) throws Exception {
    if (inputs.isEmpty()) {
        // 单输入模式：直接调用算子方法
        operator.setKeyContextElement1(element);
        getOneInputOperator().processElement(element);
    } else {
        // 多输入模式：通过Input接口路由
        checkState(inputs.size() == 1);
        Input input = inputs.get(0);
        input.setKeyContextElement(element);
        input.processElement(element);
    }
}
```

```java
// 创建测试工具
OneInputStreamOperatorTestHarness<String, String> harness =
    new OneInputStreamOperatorTestHarness<>(myOperator, inputSerializer);

// 设置和初始化
harness.setup(outputSerializer);
harness.initializeEmptyState();
harness.open();

// 输入测试数据
harness.processElement("hello", 1000L);      // 带时间戳的元素
harness.processElement("world", 2000L);      // 另一个元素
harness.processWatermark(3000L);             // 水印

// 处理更多元素
List<StreamRecord<String>> batch = Arrays.asList(
    new StreamRecord<>("test1", 4000L),
    new StreamRecord<>("test2", 5000L)
);
harness.processElements(batch);

// 验证输出
List<String> results = harness.extractOutputValues();
assertEquals(4, results.size()); // 两个元素 + 两个水印处理结果

// 清理资源
harness.close();
```

## MultiInputStreamOperatorTestHarness

[MultiInputStreamOperatorTestHarness](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/MultiInputStreamOperatorTestHarness.java) 是Apache Flink中专门用于测试多输入算子（`MultipleInputStreamOperator`）的测试工具类，继承自AbstractStreamOperatorTestHarness，完美解决如何测试多输入算子的多个输入通道。

### MultiInputStreamOperatorTestHarness 详情

1. **多输入算子专用测试**：专门为有多个输入流的算子提供测试环境
2. **多通道控制**：允许独立控制和测试算子的每个输入通道
3. **复杂流测试**：支持测试输入通道间的交互和协调逻辑
4. **完整水印管理**：为每个输入通道提供独立的水印和水印状态控制

**多通道元素处理：**

```java
public void processElement(int idx, StreamRecord<?> element) throws Exception {
    Input input = getCastedOperator().getInputs().get(idx);
    input.setKeyContextElement(element);
    input.processElement(element);
}
```

**参数详解：**

- `idx`：输入通道的索引（从0开始）
- `element`：要处理的流记录
- **执行流程**：
  1. 获取指定索引的输入通道
  2. 设置键上下文
  3. 通过输入通道处理元素

**多通道水印处理：**

```java
public void processWatermark(int idx, Watermark mark) throws Exception {
    getCastedOperator().getInputs().get(idx).processWatermark(mark);
}

public void processWatermarkStatus(int idx, WatermarkStatus watermarkStatus) throws Exception {
    getCastedOperator().getInputs().get(idx).processWatermarkStatus(watermarkStatus);
}
```

**多通道记录属性处理：**

```java
public void processRecordAttributes(int idx, RecordAttributes recordAttributes)
        throws Exception {
    getCastedOperator().getInputs().get(idx).processRecordAttributes(recordAttributes);
}
```

**算子类型转换：**

```java
protected MultipleInputStreamOperator<OUT> getCastedOperator() {
    return (MultipleInputStreamOperator<OUT>) operator;
}
```

**用途：**

- 安全地将通用算子转换为多输入算子类型
- 提供对多输入算子特有方法的访问

```java
// 创建多输入算子测试工具
MultiInputStreamOperatorTestHarness<String> harness =
    new MultiInputStreamOperatorTestHarness<>(multiInputOperatorFactory);

// 为不同输入通道发送数据
harness.processElement(0, new StreamRecord<>("input0_data1", 1000L)); // 输入通道0
harness.processElement(1, new StreamRecord<>("input1_data1", 1500L)); // 输入通道1

// 为特定通道发送水印
harness.processWatermark(0, new Watermark(2000L)); // 水印到通道0
harness.processWatermark(1, new Watermark(2500L)); // 水印到通道1

// 处理水印状态
harness.processWatermarkStatus(0, WatermarkStatus.ACTIVE); // 通道0激活水印
harness.processWatermarkStatus(1, WatermarkStatus.IDLE);   // 通道1暂停水印

// 验证输出
List<String> results = harness.extractOutputValues();
```

## TwoInputStreamOperatorTestHarness

[TwoInputStreamOperatorTestHarness](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/util/TwoInputStreamOperatorTestHarness.java) 是Apache Flink中专门用于测试双输入算子（`TwoInputStreamOperator`）的测试工具类，继承自AbstractStreamOperatorTestHarness，它为具有两个输入流的算子提供了精确的测试控制能力。

### TwoInputStreamOperatorTestHarness 详情

1. **双输入算子专用测试**：专门为`TwoInputStreamOperator`及其子类设计
2. **双通道独立控制**：提供对两个输入通道的独立操作和控制
3. **连接算子测试**：特别适合测试Join、CoProcess等需要两个输入流的算子
4. **水印协调测试**：支持测试双输入流的水印处理和协调逻辑

**算子引用：**

```java
private final TwoInputStreamOperator<IN1, IN2, OUT> twoInputOperator;
```

**用途：**

- 保持对双输入算子的强类型引用
- 提供对双输入特有方法的访问

**第一输入通道：**

```java
public void processElement1(StreamRecord<IN1> element) throws Exception {
    twoInputOperator.setKeyContextElement1(element);
    twoInputOperator.processElement1(element);
}

public void processElement1(IN1 value, long timestamp) throws Exception {
    processElement1(new StreamRecord<>(value, timestamp));
}
```

**第二输入通道：**

```java
public void processElement2(StreamRecord<IN2> element) throws Exception {
    twoInputOperator.setKeyContextElement2(element);
    twoInputOperator.processElement2(element);
}

public void processElement2(IN2 value, long timestamp) throws Exception {
    processElement2(new StreamRecord<>(value, timestamp));
}
```

**设计模式：**

- **对称设计**：两个通道具有完全相同的API结构
- **便利方法**：自动创建`StreamRecord`并设置时间戳
- **键上下文**：正确设置对应通道的键上下文

**独立水印控制：**

```java
public void processWatermark1(Watermark mark) throws Exception {
    twoInputOperator.processWatermark1(mark);
}

public void processWatermark2(Watermark mark) throws Exception {
    twoInputOperator.processWatermark2(mark);
}
```

**同步水印处理：**

```java
public void processBothWatermarks(Watermark mark) throws Exception {
    twoInputOperator.processWatermark1(mark);
    twoInputOperator.processWatermark2(mark);
}
```

**水印状态控制：**

```java
public void processWatermarkStatus1(WatermarkStatus watermarkStatus) throws Exception {
    twoInputOperator.processWatermarkStatus1(watermarkStatus);
}

public void processWatermarkStatus2(WatermarkStatus watermarkStatus) throws Exception {
    twoInputOperator.processWatermarkStatus2(watermarkStatus);
}
```

**记录属性处理：**

```java
public void processRecordAttributes1(RecordAttributes recordAttributes) throws Exception {
    twoInputOperator.processRecordAttributes1(recordAttributes);
}

public void processRecordAttributes2(RecordAttributes recordAttributes) throws Exception {
    twoInputOperator.processRecordAttributes2(recordAttributes);
}
```

**有界流支持：**

```java
public void endInput1() throws Exception {
    if (operator instanceof BoundedMultiInput) {
        ((BoundedMultiInput) operator).endInput(1);
    }
}

public void endInput2() throws Exception {
    if (operator instanceof BoundedMultiInput) {
        ((BoundedMultiInput) operator).endInput(2);
    }
}
```

```java
// 创建双输入算子测试工具
TwoInputStreamOperatorTestHarness<String, Integer, String> harness =
    new TwoInputStreamOperatorTestHarness<>(joinOperator);

// 向第一个输入通道发送数据
harness.processElement1("hello", 1000L);
harness.processElement1("world", 2000L);

// 向第二个输入通道发送数据
harness.processElement2(42, 1500L);
harness.processElement2(84, 2500L);

// 处理水印
harness.processWatermark1(new Watermark(3000L));
harness.processWatermark2(new Watermark(3500L));

// 或者同时处理水印
harness.processBothWatermarks(new Watermark(4000L));

// 结束特定输入
harness.endInput1();
harness.endInput2();

// 验证输出
List<String> results = harness.extractOutputValues();
assertEquals(4, results.size()); // 两个Join结果
```

## TestHarness 总结

| 特性 | OneInputStreamOperatorTestHarness | TwoInputStreamOperatorTestHarness | MultiInputStreamOperatorTestHarness |
|------|----------------------------------|----------------------------------|------------------------------------|
| **输入通道数** | 1个（限制） | 2个（固定） | N个（动态） |
| **API复杂度** | 简单 | 中等 | 复杂 |
| **适用算子** | 单输入算子 | 双输入算子 | 多输入算子 |
| **使用场景** | 基础算子测试 | Join/CoProcess测试 | 复杂拓扑测试 |

## 实践

### StreamMapTest

[StreamMapTest](file:///home/maiscrm/workspace/a-study/flinkStudy/flink/flink-runtime/src/test/java/org/apache/flink/streaming/api/operators/StreamMapTest.java) 是Apache Flink中对`StreamMap`算子的单元测试类，使用 OneInputStreamOperatorTestHarness 进行实际的算子测试。

1. **算子功能验证**：测试`StreamMap`算子的核心映射功能是否正确
2. **生命周期测试**：验证RichFunction的open/close方法调用顺序
3. **时间语义测试**：确保元素时间戳和水印正确保持和转发
4. **集成测试示例**：为开发者提供使用测试工具的参考实现

**简单Map函数：**

```java
private static class Map implements MapFunction<Integer, String> {
    @Override
    public String map(Integer value) throws Exception {
        return "+" + (value + 1);
    }
}
```

**测试环境设置：**

```java
@Test
void testMap() throws Exception {
    StreamMap<Integer, String> operator = new StreamMap<Integer, String>(new Map());

    OneInputStreamOperatorTestHarness<Integer, String> testHarness =
            new OneInputStreamOperatorTestHarness<Integer, String>(operator);
```

**测试数据和预期输出：**

```java
long initialTime = 0L;
ConcurrentLinkedQueue<Object> expectedOutput = new ConcurrentLinkedQueue<Object>();

testHarness.open();

// 输入测试数据
testHarness.processElement(new StreamRecord<Integer>(1, initialTime + 1));
testHarness.processElement(new StreamRecord<Integer>(2, initialTime + 2));
testHarness.processWatermark(new Watermark(initialTime + 2));
testHarness.processElement(new StreamRecord<Integer>(3, initialTime + 3));

// 预期输出构建
expectedOutput.add(new StreamRecord<String>("+2", initialTime + 1));
expectedOutput.add(new StreamRecord<String>("+3", initialTime + 2));
expectedOutput.add(new Watermark(initialTime + 2));
expectedOutput.add(new StreamRecord<String>("+4", initialTime + 3));

// 断言验证
TestHarnessUtil.assertOutputEquals(
        "Output was not correct.", expectedOutput, testHarness.getOutput());
```

**测试要点：**

- **时间戳保持**：输出元素的时间戳与输入完全一致
- **水印转发**：水印被正确转发到输出
- **处理顺序**：元素和水印的处理顺序得到保持
