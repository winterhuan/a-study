# Transformation

A {@code Transformation} represents the operation that creates a DataStream. Every DataStream has an underlying {@code Transformation} that is the origin of said DataStream.

Transformation 表示创建 DataStream 的操作。每个 DataStream 都有一个底层的 {@code Transformation}，它是该 DataStream 的来源。

API operations such as DataStream#map create a tree of {@code Transformation}s underneath. When the stream program is to be executed this graph is translated to a StreamGraph using StreamGraphGenerator.

API 操作，如 DataStream#map，会在底层创建一个 {@code Transformation} 树。
当流程序要执行时，这个图会被翻译成 StreamGraph，使用 StreamGraphGenerator。

A {@code Transformation} does not necessarily correspond to a physical operation at runtime. Some operations are only logical concepts. Examples of this are union, split/select data stream, partitioning.

一个 {@code Transformation} 不一定对应一个物理操作。一些操作只是逻辑概念。例如，union、split/select data stream、partitioning。

## PhysicalTransformation

A {@link Transformation} that creates a physical operation. It enables setting {@link ChainingStrategy}.

PhysicalTransformation 继承自 Transformation，用于创建实际的物理操作。它允许设置 {@link ChainingStrategy}（链接策略），这有助于优化任务链的执行。

## TransformationWithLineage

A {@link Transformation} that contains lineage information.

TransformationWithLineage 继承自 PhysicalTransformation，用于包含 lineage 信息。

## SinkTransformation

A {@link Transformation} for {@link Sink}.

SinkTransformation 继承自 TransformationWithLineage，用于表示 Sink 操作。

## SourceTransformation

A {@link PhysicalTransformation} for {@link Source}.

SourceTransformation 继承自 TransformationWithLineage，用于表示 Source 操作。
