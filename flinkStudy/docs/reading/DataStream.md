# DataStream 相关

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
    - assignTimestampsAndWatermarks(WatermarkStrategy watermarkStrategy)：分配时间戳和水印，支持事件时间处理。

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

ConnectedStreams<T, R> 继承自 DataStream，用于连接两个不同类型的流，支持 co-函数操作。

## BroadcastStream<T>

BroadcastStream 继承自 DataStream，用于广播状态流。

## AllWindowedStream<T, W>

AllWindowedStream 继承自 DataStream，用于非键控窗口操作。