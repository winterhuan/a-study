# DataStream 相关

## StreamElement

An element in a data stream. Can be a record, a Watermark, or a RecordAttributes.

StreamElement 是数据流中的一个元素。可以是记录、Watermark或记录属性。

| 特性 | StreamRecord | Watermark | WatermarkStatus | LatencyMarker | RecordAttributes |
|------|-------------|-----------|----------------|---------------|----------------|
| **携带数据** | 实际元素值 | 时间戳 | 状态值 | 时间戳+追踪信息 | 属性标记 |
| **主要用途** | 数据传输 | 时间推进 | 活跃性控制 | 延迟测量 | 性能优化 |
| **用户影响** | 直接处理 | 时间语义 | 系统行为 | 监控指标 | 处理策略 |
| **稳定性** | 稳定 | 稳定 | 稳定 | 演进中 | 实验性 |

## StreamRecord

One value in a data stream. This stores the value and an optional associated timestamp.

StreamRecord 继承 StreamElement，是数据流中的一个值。它存储值和一个可选的相关时间戳。

```java
/** The actual value held by this record. */
private T value;

/** The timestamp of the record. */
private long timestamp;

/** Flag whether the timestamp is actually set. */
private boolean hasTimestamp;
```

## Watermark

继承 StreamElement，核心作用：

- 事件时间进度指示器：告诉算子当前已知的最大事件时间
- 触发窗口计算：当 Watermark 到达时，触发基于事件时间的窗口计算
- 延迟数据处理：帮助系统决定哪些迟到数据可以被丢弃，LateDataHandler 根据Watermark决定是否处理迟到数据

A Watermark tells operators that no elements with a timestamp older or equal to the watermark timestamp should arrive at the operator. Watermarks are emitted at the sources and propagate through the operators of the topology. Operators must themselves emit watermarks to downstream operators using {@link org.apache.flink.streaming.api.operators.Output#emitWatermark(Watermark)}. Operators that do not internally buffer elements can always forward the watermark that they receive. Operators that buffer elements, such as window operators, must forward a watermark after emission of elements that is triggered by the arriving watermark.

Watermark 告诉算子时间戳早于或等于Watermark时间戳的元素不得到达算子。Watermark 从数据源处发出，并通过拓扑结构中的算子传播。
算子本身必须使用 {@link org.apache.flink.streaming.api.operators.Output#emitWatermark(Watermark)} 向下游算子 emit Watermark。
内部不缓冲元素的算子始终可以转发它们收到的 Watermark。
缓冲元素的算子（如窗口算子）必须在 emission 由到达的 Watermark 触发的元素后转发 Watermark。

```java
public void processWatermark(Watermark mark) throws Exception {
    // 1. 处理缓冲区中可以触发的元素
    triggerElementsBeforeWatermark(mark.getTimestamp());

    // 2. 发出处理结果
    emitBufferedResults();

    // 3. 转发Watermark（通常是相同的或稍后时间戳）
    output.emitWatermark(mark);
}
```

In some cases a watermark is only a heuristic and operators should be able to deal with late elements. They can either discard those or update the result and emit updates/retractions to downstream operations.

在某些情况下，Watermark 只是一种启发式方法，算子应该能够处理迟到 elements。他们可以丢弃这些 elements，或者更新结果并向下游操作发出更新/缩减。

Watermark 不是精确的：它是对事件时间进度的估计，而非绝对保证
可能存在迟到数据：即使Watermark已推进，仍可能有迟到元素到达
算子需容错处理：算子设计时必须考虑处理迟到数据的策略

protected final long timestamp;

When a source closes it will emit a final watermark with timestamp {@code Long.MAX_VALUE}. When an operator receives this it will know that no more input will be arriving in the future.

- MAX_WATERMARK：表示事件时间的结束，当Source关闭时发出，表示不会再有更多数据到达。
- UNINITIALIZED：表示Watermark生成前的初始状态，通常为负无穷大

## WatermarkStatus

继承 StreamElement，核心作用：
    - Watermark 活跃性控制：指示 Watermark 生成器是否处于活跃状态
    - 空闲检测：当上游输入长时间无数据时，发出IDLE状态
    - 下游通知：告知下游算子Watermark生成的状态变化
    - 联合处理：在多输入算子中协调不同输入的 Watermark 行为
    - 资源管理：在空闲时减少不必要的计算资源消耗

WatermarkStatus 继承 StreamElement，WatermarkStatus element 告知流任务是否应该继续期望来自发送它们的输入流的 watermarks。WatermarkStatus 有两种类型，即{@link WatermarkStatus#IDLE}和{@link WatermarkStatus#ACTIVE}。WatermarkStatus elements 在数据源处生成，并可能通过拓扑结构中的任务传播。它们直接反映发出任务的当前状态：{@link SourceStreamTask}或{@link StreamTask}如果将暂时停止发出任何 Watermark（即处于空闲状态），则发出{@link WatermarkStatus#IDLE}；一旦恢复发出 Watermark（即处于活跃状态），则发出{@link WatermarkStatus#ACTIVE}。任务在空闲和活跃状态之间切换时，负责将其状态进一步向下游传播。

源任务和下游任务被视为处于空闲或活跃状态的具体情况将在下面解释。
    - Source tasks: A source task is considered to be idle if its head operator, i.e. a {@link StreamSource}, will not emit watermarks for an indefinite amount of time. This is the case, for example, for Flink's Kafka Consumer, where sources might initially have no assigned partitions to read from, or no records can be read from the assigned partitions. Once the head {@link StreamSource} operator detects that it will resume emitting data, the source task is considered to be active. {@link StreamSource}s are responsible for toggling the status of the containing source task and ensuring that no watermarks will be emitted while the task is idle. This guarantee should be enforced on sources through {@link SourceFunction.SourceContext} implementations.
    -  源任务被视为处于空闲状态，如果其头部算子（即{@link StreamSource}）将在无限长的时间内不发出 Watermark。例如，对于Flink的Kafka消费者，这种情况可能发生在源最初没有分配到分区进行读取，或者无法从分配的分区读取记录。一旦头部{@link StreamSource}算子检测到它将恢复发出数据，源任务就被视为处于活跃状态。
    - Downstream tasks: a downstream task is considered to be idle if all its input streams are idle, i.e. the last received Watermark Status element from all input streams is a {@link WatermarkStatus#IDLE}. As long as one of its input streams is active, i.e. the last received Watermark Status element from the input stream is {@link WatermarkStatus#ACTIVE}, the task is active.
    - 下游任务被视为处于空闲状态，如果所有输入流都处于空闲状态，即从所有输入流接收到的最后一个Watermark状态元素都是{@link WatermarkStatus#IDLE}。只要有一个输入流处于活跃状态，即从该输入流接收到的最后一个Watermark状态元素是{@link WatermarkStatus#ACTIVE}，该任务就处于活跃状态。

Watermark Status elements received at downstream tasks also affect and control how their operators process and advance their watermarks. The below describes the effects (the logic is implemented as a {@link StatusWatermarkValve} which downstream tasks should use for such purposes):
下游任务接收到的 Watermark Status 元素也会影响和控制其算子如何处理和推进Watermark。下面描述了这些影响（该逻辑实现为{@link StatusWatermarkValve}，下游任务应使用它来实现这些目的）：
    - Since there may be watermark generators that might produce watermarks anywhere in the middle of topologies regardless of whether there are input data at the operator, the current status of the task must be checked before forwarding watermarks emitted from an operator. If the status is actually idle, the watermark must be blocked.
    - 由于可能存在在算子中生成Watermark的Watermark生成器，无论是否存在算子中的输入数据，Watermark可能在拓扑结构的中间生成。因此，在转发算子发出的Watermark之前，必须检查任务的当前状态。如果状态实际上为空闲，Watermark必须被阻止。
    - For downstream tasks with multiple input streams, the watermarks of input streams that are temporarily idle, or has resumed to be active but its watermark is behind the overall min watermark of the operator, should not be accounted for when deciding whether or not to advance the watermark and propagated through the operator chain.
    - 对于具有多个输入流的下游任务，临时空闲或已恢复但其 Watermark 落后于算子的最小Watermark的输入流的Watermark不应在决定是否推进Watermark和通过操作符链传播时考虑。

Note that to notify downstream tasks that a source task is permanently closed and will no longer send any more elements, the source should still send a {@link Watermark#MAX_WATERMARK} instead of {@link WatermarkStatus#IDLE}. Watermark Status elements only serve as markers for temporary status.

共同维护Flink流处理的时间语义正确性和系统性能。Watermark负责时间推进，Watermark status 负责管理Watermark生成的活跃性。

## LatencyMarker

Special record type carrying a timestamp of its creation time at a source operator and the vertexId and subtask index of the operator.

At sinks, the marker can be used to approximate the time a record needs to travel through the dataflow.

LatencyMarker 继承 StreamElement，是特殊记录类型，携带在源算子处创建时间的时戳以及该算子的vertexId和子任务索引。

在接收端，该标记可用于估算记录在数据流中传输所需的时间，是Flink流处理框架中用于延迟监控和性能测量的重要组件。

## RecordAttributes

A RecordAttributes describes the attributes of records from the current RecordAttributes until
the next one is received. It provides stream task with information that can be used to optimize the stream task's performance.

RecordAttributes 继承 StreamElement，描述从当前 RecordAttributes 直到下一个 RecordAttributes 的记录属性。为流任务提供可用于优化流任务性能的信息。

// 允许算子在高吞吐量（缓冲积压数据）和低延迟（立即处理）之间选择
private final boolean isBacklog; // 指示后续记录是否为积压状态

是Flink流处理框架中用于性能优化的实验性组件，主要用于在吞吐量和延迟之间提供优化的决策依据。

## DataStream

A DataStream represents a stream of elements of the same type. A DataStream can be transformed into another DataStream by applying a transformation。

DataStream 代表一个类型相同的数据流，DataStream 可以通过应用 transformation 来转换成另一个 DataStream。

### 关键字段

- environment（StreamExecutionEnvironment）：表示流执行的环境，管理作业的生命周期和资源。
- transformation（Transformation）：底层转换对象，定义了流的逻辑操作。

### 方法详情

DataStream 提供了丰富的方法，支持流处理的核心功能。以下是关键方法分类总结：

- 基础属性和配置：
    - getId()、getParallelism()、getType()：获取流的 ID、并行度和类型信息。
    - getExecutionEnvironment()：返回执行环境，用于访问配置。
    - clean(F f)：清理闭包函数，确保序列化安全。

- 转换操作（Transformation）：
    - map(MapFunction<T, R> mapper)：一对一映射，返回 SingleOutputStreamOperator<R>。
    - flatMap(FlatMapFunction<T, R> flatMapper)：一对多映射。
    - filter(FilterFunction filter)：过滤元素。
    - process(ProcessFunction<T, R> processFunction)：低级处理，支持定时器和状态。
    - transform(String operatorName, TypeInformation outTypeInfo, ...)：通用转换，支持自定义操作符。
- 分区和重分布（Partitioning）：
    - keyBy(KeySelector<T, K> key)：按键分区，返回 KeyedStream。
    - broadcast()：广播到所有下游实例。
    - shuffle()：通过洗牌均匀分布元素到下游操作，确保负载均衡（不是纯随机，而是伪随机均匀分配）。
    - rebalance()：轮询方式均匀分布。
    - rescale()：子集轮询分布。
    - global()：所有元素发送到第一个实例。
    - partitionCustom(Partitioner partitioner, KeySelector<T, K> keySelector)：自定义分区。
    - setConnectionType(StreamPartitioner partitioner)：内部方法，用于设置分区器，返回新的 DataStream。
- 多流操作：
    - union(DataStream... streams)：合并相同类型的流。
    - connect(DataStream dataStream)：连接不同类型的流，返回 ConnectedStreams。
    - coGroup(DataStream otherStream)、join(DataStream otherStream)：联合操作，支持窗口。
- 窗口和时间处理：
    - windowAll(WindowAssigner<T, W> assigner)：非键控窗口，返回 AllWindowedStream。
    - assignTimestampsAndWatermarks(WatermarkStrategy watermarkStrategy)：分配时间戳和Watermark，支持事件时间处理。

- Sink 和输出：
    - addSink(SinkFunction sinkFunction)：添加自定义 sink，返回 DataStreamSink。
    - sinkTo(Sink sink)：添加现代 sink（支持检查点）。
    - print()、printToErr()：输出到标准输出或错误流。
    - writeToSocket(...)：写入 socket。
    - executeAndCollect(...)：收集结果到本地迭代器，用于测试。
- 高级功能：
    - collectAsync()：异步收集元素，支持分布式执行。
    - fullWindowPartition()：分区窗口操作。

方法大多返回新的 DataStream 或子类实例，支持链式调用。许多方法使用 clean() 来处理函数，确保在分布式环境中序列化正确。

## SingleOutputStreamOperator

{@code SingleOutputStreamOperator} represents a user defined transformation applied on a {@link DataStream} with one predefined output type.

SingleOutputStreamOperator 继承自 DataStream，用于表示单输出流的操作，表示应用于 DataStream 上的用户定义转换，具有预定义的单一输出类型（如 map、filter），支持链式操作。

## DataStreamSource

The DataStreamSource represents the starting point of a DataStream.

DataStreamSource 继承自 SingleOutputStreamOperator，表示数据流的起点。

## DataStreamSink

A Stream Sink. This is used for emitting elements from a streaming topology.

DataStreamSink 是数据流的输出端，用于从流式拓扑中输出元素。

## KeyedStream<T, K>

KeyedStream 继承自 DataStream，用于键控流，支持按键分组的操作（如 keyed window）。

## ConnectedStreams<T, R>

ConnectedStreams<T, R> 用于连接两个不同类型的流，支持 co-函数操作。

## BroadcastStream<T>

BroadcastStream 用于广播状态流。

## AllWindowedStream<T, W>

AllWindowedStream 用于非键控窗口操作。
