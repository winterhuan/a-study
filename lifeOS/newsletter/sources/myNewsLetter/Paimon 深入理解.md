# 深入理解 Apache Paimon：从架构原理到源码实践

- https://gemini.google.com/app/cf1d8b546b87ddf1
- https://paimon.apache.org/
- https://github.com/apache/paimon/

## 第一部分：背景与核心亮点

### Paimon 的诞生：为何需要新的流式湖仓格式

在实时数据处理领域，存储系统的能力往往是决定整个数据链路性能与时效性的关键瓶颈。Apache Paimon 的诞生，并非是对现有技术的简单重复，而是对流式计算时代存储挑战的一次深刻回应与架构重塑。

#### 流式计算对存储的挑战

传统的数据仓库架构，如以 Apache Hive 为代表的批处理系统，其设计初衷是为大规模的离线分析提供支持。这类系统通常采用不可变的、一次性写入的分区文件模式，对于数据的更新操作，往往需要重写整个分区，这导致了极高的延迟和计算成本，无法满足现代业务对数据实时性的苛刻要求。数据湖的出现虽然解决了数据格式多样性和存储成本的问题，但其核心架构依然延续了批处理的思想，在实时更新和低延迟查询方面力不从心。

随着 Apache Flink 等先进流计算引擎的崛起，业界迫切需要一种能够与流计算无缝对接的存储底座。这种存储不仅要能承载海量数据，还必须支持高频次的实时数据更新（Upsert）和删除（Delete），同时提供足够低的查询延迟，以支撑实时数仓、实时报表和实时数据应用等场景。

#### 对现有数据湖格式的实时化改造探索

在 Paimon 出现之前，社区进行了诸多将现有数据湖格式实时化的尝试，主要集中在对 Apache Hive 和 Apache Iceberg 的改造上，但这些探索都遇到了难以逾越的瓶颈。

- Hive 实时增强: 通过 Flink Hive Sink，社区实现了向 Hive 表的流式写入。该方案能够保证 Exactly-Once 的写入语义，并将数据延迟降低到分钟级别。然而，其本质仍是流式地追加文件到分区，并未从根本上解决更新问题。对于需要更新的场景，依然依赖于后续的批处理作业进行数据合并，查询性能也因小文件众多而表现不佳，无法满足真正的实时分析需求。

- Iceberg 实时增强: Apache Iceberg 凭借其优秀的元数据设计和 ACID 事务能力，为数据湖带来了革命性的进步。社区通过 Flink 与 Iceberg 的集成，实现了对数据湖的流式读写。然而，当面对包含大量更新的 CDC (Change Data Capture) 数据流时，Iceberg 的写时复制（Copy-on-Write）机制会产生性能问题。为了处理更新，需要读取相关数据文件，与新数据合并后写回新文件，这个过程涉及大量的读、写和计算操作，导致存储和计算成本高昂，维护也变得异常复杂。尽管后续引入了写时合并（Merge-on-Read）模式，但在 Flink 这种流式优先的引擎下，如何高效管理状态和索引，依然是一个巨大的挑战。

#### Paimon 的破局之道

正是为了解决上述困境，Apache Paimon（其前身为 Flink Table Store）应运而生。它源于 Apache Flink 社区提出的 FLIP-188 提案，其核心目标是为 Flink 的动态表（Dynamic Table）提供一个可直接查询、持久化的内置存储，从而构建一个真正意义上的流式数据仓库。Paimon 的设计从一开始就根植于流计算的语境，它并非试图在批处理架构上“修补”出流处理能力，而是为流处理量身打造一个原生的存储底座。

Paimon 的设计哲学是对现有“批改流”湖仓方案的颠覆。它并非在批处理为核心的架构上叠加流处理能力，而是围绕流计算（尤其是 Flink）的需求，构建了一个以流为核心、原生支持实时更新的存储架构。研究资料清晰地指出了将 Hive 和 Iceberg 等传统批处理架构应用于 Flink 流处理时遇到的架构失配问题，尤其是在 Upsert 场景下的成本和性能瓶颈。Paimon 的起源是 Flink 社区为了解决自身动态表存储问题而发起的，这决定了其与生俱来的“Flink-Native”基因。

#### 核心设计哲学：LSM 与湖仓格式的融合

Paimon 的核心创新在于，它巧妙地将数据库领域中用于处理高频写入和更新的成熟数据结构——LSM-Tree (Log-Structured Merge-Tree)，与现代数据湖的表格式（Table Format）进行了深度融合。

LSM-Tree 的核心思想是将随机写转化为顺序写，通过内存中的写缓冲（MemTable）和磁盘上的多层级文件（Sorted Runs）来组织数据。新的写入和更新首先进入内存，然后批量刷写到磁盘上最新的、不可变的 L0 层文件。后台的合并（Compaction）进程会异步地将多层级的文件进行归并，清理冗余数据，优化查询性能。

通过引入 LSM-Tree，Paimon 从根本上解决了数据湖上大规模实时更新的难题。它不再需要像 Copy-on-Write 那样重写整个数据文件，而是将更新作为新的记录追加到 LSM-Tree 中，极大地提升了写入性能和吞吐量。这种“以流为本”的设计范式，解释了为何 Paimon 能够如此自然地支持流式 CDC、提供灵活的合并引擎和完整的 Changelog 生成——这些都是流处理的核心诉求，而在传统湖仓格式中则往往是作为附加功能存在，实现起来更为复杂和低效。

### 核心能力概览

基于 LSM-Tree 与湖仓格式的创新结合，Paimon 提供了一系列强大的核心能力，使其成为构建实时湖仓的理想选择。

- 实时更新 (Real-time Updates): 借助 LSM 结构，Paimon 的主键表（Primary Key Table）能够支撑大规模、高吞吐的数据更新与删除操作。数据写入延迟可以稳定在分钟级，甚至在优化配置下达到亚分钟级，满足绝大多数实时分析场景的需求。

- 灵活的合并引擎 (Flexible Merge Engines): Paimon 认识到不同业务场景对数据合并的需求各异。为此，它提供了多种可插拔的合并引擎（Merge Engine）。用户可以在建表时通过 merge-engine 参数指定合并逻辑，例如：

	- deduplicate (默认): 只保留相同主键的最新一条记录。
	
	- partial-update: 用新记录中的非空字段更新旧记录，实现部分列更新。
	
	- aggregation: 对相同主键的记录进行预聚合，例如 SUM, MAX, MIN 等。
	
	- first-row: 只保留相同主键的第一条记录，忽略后续更新。  
	    这种灵活性使得 Paimon 能够在一个统一的存储层上，以最高效的方式处理各种复杂的数据逻辑。

- 完整的变更日志生成 (Complete Changelog Production): 在流式计算中，获取完整、正确的变更数据流（Changelog）对于下游的流式聚合、流式关联等操作至关重要。Paimon 的 changelog-producer 机制能够为任何输入的数据流生成包含 UPDATE_BEFORE 和 UPDATE_AFTER 的完整 Changelog。无论上游是 CDC 数据源还是普通的事实流，Paimon 都能保证下游消费者获得一致、准确的变更视图，极大地简化了端到端流式分析链路的构建。

- 海量追加数据处理 (Huge Append Data Processing): 除了主键表，Paimon 还提供了无主键的追加表（Append-only Table），专门用于处理日志、埋点等只需追加写入的场景。追加表提供了极高的流式和批量写入性能，并内置了自动小文件合并（Compaction）机制。此外，它还支持 Z-order 等高级数据布局优化，通过对多列进行排序，提升多维过滤查询的性能。

- 全面的数据湖能力 (Comprehensive Data Lake Capabilities): 作为新一代的数据湖格式，Paimon 同样具备现代数据湖的所有核心优势，包括：

	- ACID 事务: 保证数据写入的原子性、一致性、隔离性和持久性。
	
	- 时间旅行 (Time Travel): 通过快照（Snapshot）机制，可以查询任意历史版本的数据。
	
	- Schema 演进: 支持安全地增加列、修改列类型等 Schema 变更操作。
	
	- 可扩展的元数据: 能够高效管理 PB 级别的数据集和海量分区。

## 第二部分：架构设计与核心概念

要深入理解 Paimon，必须首先掌握其精巧的架构设计和一系列核心概念。Paimon 的架构分为逻辑分层和物理布局，其核心概念则构成了理解其运行机制的基石。

### 宏观架构

Paimon 的整体架构设计清晰，层次分明，旨在实现计算与存储的分离，并与主流大数据生态系统无缝集成。

- 分层模型 (Layered Model): Paimon 的架构可以看作一个分层的模型。

	- 计算引擎层 (Compute Engine Layer): 位于最上层，是与用户直接交互的接口。Paimon 设计为可插拔的存储格式，能够被多种计算引擎读写，包括 Apache Flink、Apache Spark、Apache Hive、Trino、Presto、Doris 和 StarRocks 等。这种广泛的兼容性使其可以融入企业现有的技术栈。
	
	- 存储格式层 (Table Format Layer): 这是 Paimon 的核心所在，定义了数据如何被组织、管理和访问。它由内部的元数据层和数据层构成。
	
	- 物理存储层 (Physical Storage Layer): 位于最底层，负责数据的持久化。Paimon 可以部署在各种分布式文件系统或对象存储之上，如 HDFS、Amazon S3、Alibaba Cloud OSS、Google Cloud Storage 等。

- 读写流程概念 (Conceptual Read/Write Flow):

	- 写流程: 当数据写入 Paimon 表时，它首先被路由到对应的分区（Partition）和桶（Bucket）。在桶内部，数据被写入一个 LSM-Tree 结构。新的数据和更新首先进入内存缓冲区，然后被刷写到磁盘上最新的数据层（Level 0）。
	
	- 读流程: 当查询 Paimon 表时，计算引擎首先通过表的最新快照（Snapshot）定位到所有有效的数据文件。由于数据分布在 LSM-Tree 的多个层级，读取器需要将这些层级的数据进行合并（Merge-on-Read），并应用相应的合并引擎逻辑，才能生成最终的、一致性的数据视图。

- LSM-Tree 的核心角色 (The Core Role of LSM-Tree): LSM-Tree 是 Paimon 架构的灵魂。它将传统数据库中用于优化高频更新的结构引入到数据湖中，带来了革命性的变化。LSM-Tree 通过将随机写转化为顺序追加，极大地提升了写入性能，使其能够轻松应对来自 CDC 或流式 ETL 的高吞吐数据流。同时，其分层和合并的机制为实时更新、数据版本管理和高效查询优化提供了坚实的基础。

### 物理文件布局

Paimon 表在物理存储上的文件组织方式是其架构的具体体现，理解其目录结构和文件类型是排查问题和进行优化的前提。

- 目录结构 (Directory Structure): 一个 Paimon 表的所有文件都存储在一个基础目录下。其典型的目录结构如下所示：  

```text
    <warehouse>/<database>.db/<table>/  
    ├── snapshot/                   -- 存储 Snapshot 文件 (例如: snapshot-1, snapshot-2,...)  
    ├── manifest/                   -- 存储 Manifest List 和 Manifest 文件  
    ├── schema/                     -- 存储 Schema 文件 (例如: schema-0, schema-1,...)  
    ├── index/                      -- 存储表级索引文件 (例如: Bitmap Index)  
    ├── <partition_values>/         -- 分区目录 (例如: dt=2024-01-01/)  
    │   └── bucket-<bucket_id>/     -- 桶目录 (例如: bucket-0/)  
    │       ├── data-*.parquet      -- 数据文件 (构成 LSM-Tree 的 Sorted Run)  
    │       └── changelog-*.parquet -- Changelog 文件 (如果启用)  
    └──...  
```

- 文件组织 (File Organization): Paimon 采用分区（Partition）和桶（Bucket）两级结构来组织数据文件。数据首先根据分区键的值被归入不同的分区目录，然后在每个分区内，再根据分桶键的值被哈希到不同的桶目录中。这种结构使得查询可以快速地裁剪掉无关的分区和桶，从而大幅减少需要扫描的数据量。

### 核心元数据组件

Paimon 的元数据设计精巧，借鉴了 Apache Iceberg 的思想并结合自身 LSM 的特点进行了创新，是实现其所有高级功能的基础。

- Snapshot (快照):

	- 定义与作用: 快照是 Paimon 元数据的核心。每个快照是一个小的 JSON 文件，存储在 snapshot/ 目录下，文件名是一个单调递增的数字（如 snapshot-1）。它代表了表在某个特定时间点的完整、一致的状态。所有的读操作都是从一个特定的快照开始的。正是通过快照，Paimon 实现了 ACID 事务隔离和时间旅行（Time Travel）功能。

	- 文件内容: 一个 Snapshot JSON 文件包含了该快照的所有元信息，关键字段包括：

		- version, id: 快照的版本和唯一 ID。
		
		- schemaId: 当前快照使用的 Schema 文件的版本号。
		
		- baseManifestList: 指向一个清单列表文件，该文件记录了上一个快照的所有数据文件。
		
		- deltaManifestList: 指向一个清单列表文件，该文件只记录了本次提交新增的数据文件。
		
		- commitKind: 提交类型，如 APPEND, COMPACT, OVERWRITE。
		
		- commitUser: 提交者的标识。

- Manifest List & Manifest File (清单列表与清单文件):

	- 层级关系: Paimon 的元数据构成了一个树状的指针链条：Snapshot -> Manifest List -> Manifest File -> Data File。这种结构使得元数据管理可以扩展到海量文件。
	
	- Manifest List: 这是一个文本文件，每行记录一个 Manifest 文件的文件名。Paimon 在 Snapshot 中创新性地引入了 baseManifestList 和 deltaManifestList 的区分，这是其实现高效流式消费的核心。这种设计是 Paimon “流批一体”思想在元数据层面的直接体现。它在源头上就为流式和批式两种访问模式提供了各自最高效的元数据路径。对于流式读取，消费者只需关心 deltaManifestList 就能获取到最新的增量数据，无需扫描全量元数据，效率极高。对于批处理查询，引擎会合并 base 和 delta 列表，获取当前快照的完整数据视图，避免了流式作业在批式元数据结构上进行低效的“增量发现”，是其流式性能优越的关键所在。
	
	- Manifest File: 这是一个 Avro 格式的文件，包含了一系列被称为 ManifestEntry 的记录。每一条 ManifestEntry 都描述了一个数据文件（Data File）的元信息，包括：它是被新增（ADD）还是被删除（DELETE），它所属的分区和桶，它在 LSM-Tree 中的层级（Level），文件大小，以及关键的统计信息（如主键的最小值和最大值）。这些统计信息是查询优化器进行数据跳过（Data Skipping）的重要依据。

- Schema File (模式文件): 存储在 schema/ 目录下的 JSON 文件，定义了表的完整模式信息，包括所有列的名称、数据类型、是否可为空、主键、分区键以及表属性（WITH子句中的配置）等。当表结构发生变更时（Schema Evolution），Paimon 会创建一个新的、版本号递增的 Schema 文件，而旧的 Schema 文件仍然保留，以支持读取历史版本的数据。

### 核心数据组织

Paimon 通过分区和桶对数据进行宏观和微观上的组织，这对于写入的负载均衡和查询的性能至关重要。

- Partition (分区): 分区是一种可选的数据组织方式，与 Apache Hive 的概念完全相同。用户可以指定一个或多个列作为分区键。Paimon 会根据分区键的值将数据存储在不同的子目录中。例如，按天分区 PARTITIONED BY (dt)，那么 dt='2024-01-01' 的所有数据都会存放在 dt=2024-01-01/ 目录下。在查询时，如果 WHERE 条件中包含了对分区键的过滤（如 WHERE dt = '2024-01-01'），Paimon 就可以只扫描对应的分区目录，而忽略所有其他分区，这个过程称为分区裁剪（Partition Pruning），是大数据查询优化的首要手段。

- Bucket (桶):

	- 定义: 在每个分区内部（对于无分区表，则是在表级别），数据会被进一步划分为若干个桶。桶是 Paimon 进行读写的最小存储单元。每个桶在物理上都对应一个独立的 LSM-Tree。
	
	- 作用: 数据行根据 bucket-key（分桶键）的哈希值被确定性地路由到某个桶中。这保证了具有相同主键（通常主键也是分桶键的一部分）的数据一定会落在同一个桶里，这对于后续的合并操作（Merge）至关重要。同时，桶的数量（bucket 参数）直接决定了数据读写的最大并行度。例如，一个有 4 个桶的表，最多可以被 4 个并行的 Flink Sink Task 同时写入。

- LSM-Tree 单元: 将每个桶视为一个独立的 LSM-Tree 是理解 Paimon 工作原理的关键。对表的写入操作，实际上被分解为对多个独立的 LSM-Tree 的写入操作。对表的查询，也被分解为对多个 LSM-Tree 的并行查询。这种设计使得 Paimon 的并发控制和扩展性得到了极大的简化和增强。

## 第三部分：核心组件与流程源码剖析

理解 Paimon 的核心流程——写、读、合并——以及它们在代码层面的实现，是掌握 Paimon 并对其进行深度定制和优化的关键。本部分将深入剖析这些流程的关键组件和源码逻辑。

### 写流程（Write Path）深度解析

Paimon 的写流程是一个精心设计的、与 Flink Checkpoint 机制深度绑定的两阶段提交流程（2PC），旨在保证流式写入的 Exactly-Once 语义。

- 入口: FlinkSink: 当用户在 Flink SQL 中执行一个 INSERT INTO paimon_table... 语句时，Flink 的 Planner 会将这个操作翻译成一个 Paimon 的 FlinkSink。FlinkSink 是 Paimon 与 Flink Sink API v2 对接的实现，它负责创建 PaimonSinkWriter 和 PaimonCommitter，这是执行写入的两个核心角色。PaimonSinkWriter 在 Flink 的 TaskManager 上并行执行，负责接收数据并写入文件；PaimonCommitter 则在 JobManager 端（或专用的 Committer 线程）执行，负责最终的事务提交。

- 构建写入器: StreamWriteBuilder & TableWrite: 在 PaimonSinkWriter 初始化时，它会通过 table.newWriteBuilder() 方法来构建一个写入器。在 AbstractFileStoreTable 类中，newWriteBuilder() 方法会创建一个 StreamWriteBuilder 实例。这个 Builder 是一个配置中心，它会根据表的 OPTIONS（例如 merge-engine, changelog-producer 等）来配置并创建最终的 TableWrite 对象。TableWrite 是一个接口，其具体实现通常是 TableWriteImpl，它封装了向单个桶（LSM-Tree）写入数据的完整逻辑。

- 数据写入: TableWriteImpl.write(): PaimonSinkWriter 将从上游接收到的每一条数据（InternalRow）传递给 TableWriteImpl 的 write() 方法。在 write() 内部，数据首先根据其 bucket-key 被路由到对应的 RecordWriter。对于主键表，这个 RecordWriter 通常是 MergeTreeWriter。MergeTreeWriter 内部维护了一个内存中的写缓冲 WriteBuffer。数据行被写入 WriteBuffer 中，并在内存中进行排序。

- 内存管理: MemorySegmentPool: WriteBuffer 的内存并非直接从 JVM Heap 分配，而是通过 Paimon 的自定义内存管理模块 MemorySegmentPool 来获取。通常使用的是 HeapMemorySegmentPool。该池预先分配一大块内存，并将其切分为固定大小的页（MemorySegment）。WriteBuffer 在需要内存时向池中申请 MemorySegment，使用完毕后归还。这种机制避免了频繁的 GC，并能更精确地控制内存使用。当 WriteBuffer 的内存达到阈值（由 write-buffer-size 控制）时，它会触发一次刷盘（flush）操作，将内存中的有序数据写入磁盘，形成一个新的 L0 层数据文件。

- 两阶段提交 (2PC): 这是保证数据一致性和原子性的核心机制，与 Flink 的 Checkpoint 紧密相连。
	
	- prepareCommit() (预提交/第一阶段):
	
		1. 当 Flink JobManager 触发一次 Checkpoint 时，会向所有 PaimonSinkWriter 发送一个 Checkpoint Barrier。
		
		2. PaimonSinkWriter 收到 Barrier 后，会调用其内部 TableWriteImpl 的 prepareCommit() 方法。
		
		3. TableWriteImpl 会命令其管理的每个 MergeTreeWriter 执行 prepareCommit()。这一步是关键：MergeTreeWriter 会将 WriteBuffer 中剩余的所有数据强制刷写到磁盘，形成新的 L0 层文件。
		
		4. 如果在此期间触发了 Compaction，合并操作也会完成，生成新的高层级文件，并记录下哪些旧文件可以被标记为删除。
		
		5. 最终，MergeTreeWriter 会返回一个 CommitIncrement 对象，其中包含了本次 Checkpoint 间隔内产生的所有文件变更信息（新增的数据文件 DataFileMeta、删除的数据文件、新增的 Changelog 文件等）。
		
		6. PaimonSinkWriter 将这个 CommitIncrement 包装成一个 CommitMessage，并通过 Flink 的通信机制发送给 PaimonCommitter。
	
	- notifyCommit() (正式提交/第二阶段):

		1. 当所有 Task 的 Checkpoint 都成功完成，并且 Flink JobManager 完成了全局状态的快照后，JobManager 会回调所有算子的 notifyCheckpointComplete() 方法。
		
		2. PaimonCommitter 在其 notifyCheckpointComplete() 方法中接收到这个通知，意味着可以进行正式提交了。
		
		3. Committer 会聚合来自所有并行 Writer 的 CommitMessage，然后调用 FileStoreCommit.commit() 方法。
		
		4. FileStoreCommit 负责执行元数据操作：它会创建一个或多个新的 Manifest 文件，将所有 CommitMessage 中的文件变更（ADD/DELETE）记录进去。
		
		5. 最后，它会原子性地在 snapshot/ 目录下创建一个新的 snapshot-N 文件。这个新快照文件会指向刚刚创建的 Manifest List。这个文件的成功创建，标志着本次事务的最终成功，所有新写入的数据从这一刻起对外部查询可见。如果创建失败，由于数据文件和 Manifest 文件都已写入，系统可以回滚或重试，不会丢失数据。

#### 批处理和流式写入流程对比

| 特性    | 批处理模式 (Batch)    | 流式模式 (Streaming)      |
| ----- | ---------------- | --------------------- |
| 触发提交  | 作业结束时一次性提交       | 每次 Checkpoint 提交      |
| 事务协议  | 单阶段提交（作业完成→提交可见） | 两阶段提交 (2PC)           |
| 状态保存  | 不依赖 Flink 状态     | 依赖 Flink 状态（恢复一致性）    |
| 数据可见性 | 作业完成后一次性可见       | 每个 Checkpoint 成功后增量可见 |
| 典型场景  | 历史数据导入 / 离线计算    | 实时数据持续写入              |

### 读流程（Read Path）深度解析

Paimon 的读流程核心是 Merge-on-Read，即在查询时动态地合并多个数据文件和层级，以构建出特定快照下的完整数据视图。

- 入口: FlinkSource: 读取操作始于 FlinkSource。用户通过 FlinkSourceBuilder 可以方便地构建一个 Paimon Source，并可以配置投影（projection）、过滤（filter pushdown）、读取模式等。

- 快照发现: SnapshotManager & SnapshotSplitReader:

	- 当一个读取作业启动时，其核心任务 TableScan.plan() 首先需要确定从哪个快照开始读取。它会使用 SnapshotManager 工具类来与文件系统交互。SnapshotManager 提供了 latestSnapshot()、snapshot(long snapshotId) 等方法，可以根据 scan.mode 配置（如 latest、from-timestamp、from-snapshot）找到目标快照文件。
	
	- 确定起始快照后，SnapshotSplitReader 登场。它负责从该快照开始，递归地解析元数据树（Snapshot -> Manifest List -> Manifests），最终获取到构成该快照的所有数据文件（DataFileMeta）的列表。对于流式读取（streaming=true），SnapshotSplitReader 会持续地监控 snapshot/ 目录，一旦有新快照生成，它就会解析新快照的 deltaManifestList，找出增量的数据文件，并生成新的分片。

- 分片计划: SplitGenerator:
	
	- 获取到数据文件列表后，SplitGenerator 的任务是将这些文件打包成一个个的 Split。一个 Split 是 Flink Source Task 处理的基本工作单元，它通常包含了一个或多个属于同一个桶的数据文件。
	
	- 在生成分片的过程中，会进行重要的查询优化。如果查询带有 WHERE 条件，SplitGenerator 会利用分区信息进行分区裁剪，并利用 Manifest 文件中的统计信息（min/max key）进行数据跳过，直接过滤掉那些主键范围与查询条件不符的数据文件，避免为它们创建分片。最终生成的分片数量和并行度可以通过 scan.parallelism 参数来控制。

- 数据读取: PaimonRecordReader & Merge-on-Read:

	- Flink 的 Source Task 获得一个 Split 后，会创建一个 PaimonRecordReader 来执行实际的数据读取工作。
	
	- Reader 会打开 Split 中包含的所有数据文件。由于这些文件来自 LSM-Tree 的不同层级（Level 0, Level 1,...），它们之间可能存在主键相同但版本不同的记录。
	
	- Paimon 的 Merge-on-Read 机制在此刻启动。Reader 内部会使用一个多路归并排序器（如 KVExternalMerger），同时从所有打开的文件中读取数据。它会按照主键和序列号（sequence number）对记录进行排序，确保相同主键的记录能够被聚合在一起。
	
	- 然后，根据建表时指定的 merge-engine（如 deduplicate 会保留最新的一条，aggregation 会进行聚合），对这些相同主键的记录进行处理，最终只输出一条合并后的、对用户可见的最终结果行。
	
	- 在读取 Parquet 或 ORC 文件时，PaimonRecordReader 还会将查询中的过滤条件进一步下推到文件格式层面，利用行组/Stripe级别的统计信息和页级别的索引（如 Bloom Filter）来跳过不包含目标数据的行组或数据页，实现更细粒度的数据过滤。

### 合并流程（Compaction）深度解析

Compaction 是 LSM-Tree 架构的“后台清理工”，对于维持 Paimon 表的长期健康和查询性能至关重要。

- 为何需要 Compaction: LSM-Tree 的设计决定了写操作会不断在 L0 层产生新的、通常较小的有序文件（Sorted Run）。随着时间推移，L0 层的文件数量会越来越多。由于 Merge-on-Read 需要合并所有层级的文件，过多的 L0 文件会急剧增加查询时的归并开销，导致查询性能严重下降。Compaction 的目的就是定期将这些小文件合并成更少、更大的文件，并将其推向更高的层级（L1, L2,...），从而控制文件的总数量，维持系统的高查询性能。

- 触发机制 (Trigger Mechanism): Paimon 的 Compaction 并非随意触发，而是由一套精密的策略来控制。

	- 常规触发: Compaction 最主要的触发条件由 num-sorted-run.compaction-trigger 参数定义。系统会持续监控每个桶内的 Sorted Run 数量（L0 的文件数加上更高层级的数量）。一旦这个数量达到了该阈值，就会为这个桶规划并提交一个 Compaction 任务。

	- 写时暂停: 在写入压力极大的情况下，Compaction 的速度可能跟不上新文件的生成速度。为了防止 L0 文件无限累积最终耗尽内存（因为查询需要打开所有文件），Paimon 设立了一道“熔断”防线：num-sorted-run.stop-trigger。当一个桶内的 Sorted Run 数量达到这个更高的阈值时，向该桶的写入操作会被阻塞，直到 Compaction 完成、文件数量下降后才会恢复。这是一种反压机制，牺牲了短时的写入性能以保证系统的稳定性。

	- Full Compaction: 除了常规的增量 Compaction，Paimon 还支持 Full Compaction。它会将一个分区（或整个表）的所有数据文件合并成一个单一的、完全有序的大文件。这能最大程度地优化查询性能。Full Compaction 可以通过 full-compaction.delta-commits 参数（每隔N次提交触发一次）自动触发，也可以通过 CALL sys.compact() 存储过程手动触发。

- 核心策略: UniversalCompaction:

	- Paimon 默认采用了类似于 RocksDB 的 Universal Compaction 策略。该策略的核心思想是，每次 Compaction 会尝试将所有 L0 层的文件与 L1 层的文件进行合并，生成新的 L1 层文件。如果 L1 层文件大小超过了某个阈值，它又会和 L2 层进行合并，以此类推。

	- CompactManager 的实现类（如 UniversalCompaction）是这个策略的大脑。它负责挑选哪些文件（SortedRun）参与本次合并。它会评估候选文件的大小、层级，并参考 compaction.size-ratio 等参数，以一种旨在平衡写放大（一次写入导致多次物理写入）、读放大（一次查询需要读取多个物理文件）和空间放大（存储冗余数据所需的额外空间）的方式来制定合并计划。

- 执行方式 (Execution Mode):

	- 内联合并 (Inline Compaction): 在默认配置下，Compaction 任务是由 Flink Sink Task 内部的后台线程池异步执行的。这种方式部署简单，无需额外资源。但缺点是 Compaction 会与正常的写流程竞争 CPU、内存和 IO 资源，在高负载下可能相互影响。

	- 专用合并作业 (Dedicated Compaction Job): 对于写入密集型或有多个作业同时写入同一张表的生产环境，最佳实践是采用专用 Compaction 作业。用户可以在写入作业的表配置中设置 'write-only'='true'，这将关闭 Sink 端的 Compaction 功能，使其只负责写入 L0 文件。然后，用户可以启动一个独立的、长时间运行的 Flink 流处理作业（使用 paimon-action jar），这个作业唯一的任务就是持续监控表的状态并执行 Compaction。这种方式实现了计算（写入）与存储整理（合并）的物理资源隔离，保证了写入流程的稳定性和低延迟，是保障生产环境稳定性的关键手段。

Paimon 的核心流程（写、读、合并）与 Flink 的分布式执行模型和 checkpoint 机制深度耦合，形成了一个有机的整体。这种紧耦合是其实现流式 Exactly-Once 和高性能的关键。TableWriteImpl 的两阶段提交流程与 Flink 的 snapshotState 和 notifyCheckpointComplete 生命周期完美对齐。这意味着 Paimon 的提交延迟、吞吐量直接受到 Flink Checkpoint 间隔和超时时间的影响。SplitGenerator 生成的分片被 Flink 的 Source 并行读取，Source 的并行度、数据倾斜等问题，直接影响整个 Flink 作业的拓扑和性能。内联合并会消耗 Sink 节点的 CPU 和内存，可能导致反压，进而影响 Flink 的 Checkpoint 进程。因此，对 Paimon 的性能调优本质上是对整个 Flink 作业的系统级调优。不能孤立地看待 Paimon 的某个流程。例如，写入慢可能不是 Paimon 本身的问题，而是因为 Checkpoint 间隔太短，导致频繁的 prepareCommit 和刷盘。查询慢可能与 Sink 端 Compaction 不及时有关。因此，Paimon 的运维和优化者必须具备 Flink 的系统级视野，综合考虑 Checkpoint 配置、资源分配、并行度设置以及 Paimon 自身的表参数，才能找到最优解。

## 第四部分：存储、配置与性能优化

掌握 Paimon 的物理存储细节、核心配置参数以及性能优化策略，是将 Paimon 从理论应用到生产实践的关键一步。本部分将详细解析这些内容，并提供可操作的指导。

### 文件格式详解

Paimon 的存储效率和查询性能在很大程度上取决于其底层文件的格式和结构。

- 数据文件 (Data Files):

	- 格式: Paimon 支持多种主流的列式存储格式，包括 Apache Parquet（默认）、Apache ORC，以及行式存储格式 Apache Avro。列式存储（Parquet/ORC）通过将同一列的数据连续存储，实现了极高的压缩率，并且在只查询部分列时能够实现高效的 I/O（列裁剪），是分析型场景的首选。Avro 作为行存格式，在写入和全列扫描时性能较好，但在分析查询中通常不如列存。
	
	- 物理结构: 在 Parquet/ORC 文件内部，数据被组织成更小的单元。例如，Parquet 文件由多个行组（Row Group）构成，每个行组包含多个列块（Column Chunk），而每个列块又由多个数据页（Data Page）组成。Paimon 充分利用了这种层级结构。在查询时，它不仅能跳过不相关的文件，还能利用文件元数据中记录的行组/Stripe级别的统计信息（min/max 值），跳过不包含查询结果的行组，实现更细粒度的谓词下推。
	
	- 行类型 (`_row_kind`): 这是 Paimon 数据文件中一个至关重要的“隐藏”列。对于主键表，写入的每一行数据都会被赋予一个行类型（Row Kind）值，例如 +I (INSERT), -U (UPDATE_BEFORE), +U (UPDATE_AFTER), -D (DELETE)。这个字段在物理文件中真实存在，是 Paimon 实现 Merge-on-Read 架构和生成完整 Changelog 的基础。读取器在合并数据时，正是根据 `_row_kind` 来决定如何处理具有相同主键的多个版本记录的。

- 元数据文件 (Metadata Files):

	- Snapshot: 快照文件采用 JSON 格式。这种选择使其具有良好的可读性，便于人工查看和调试，可以快速了解某个时间点表的元数据状态。
	
	- Manifest List / Manifest File: 清单列表是简单的文本文件，而清单文件则采用 Avro 格式。Avro 是一种二进制、支持 Schema 演进的数据序列化格式。选择 Avro 的优势在于：1) 紧凑高效：二进制格式比 JSON 更小，解析速度更快，适合机器高效读写，尤其是在元数据量巨大时。2) Schema 演进: Avro 内置了强大的 Schema 演进支持，使得 Paimon 可以在未来平滑地升级 Manifest 文件的结构，而不会破坏向后兼容性。

### 重要参数配置指南

Paimon 提供了丰富的配置参数，允许用户根据具体场景进行深度调优。以下表格列出了最核心的参数及其作用。

#### 表 1: 核心写入与合并参数

| 参数 (Key)                          | 默认值         | 描述                                                                                    |
| --------------------------------- | ----------- | ------------------------------------------------------------------------------------- |
| bucket                            | -1          | 桶数量。-1 为动态桶，-2 为延迟桶（Adaptive Bucket），>0 为固定桶。这是性能调优最关键的参数之一，直接影响写入并行度和数据分布。           |
| bucket-key                        | (none)      | 分桶键，决定数据如何哈希到不同的桶。未指定时，默认使用主键。                                                        |
| merge-engine                      | deduplicate | 主键表的合并引擎，定义了当遇到相同主键的数据时应如何合并，可选 partial-update, aggregation 等。                        |
| write-buffer-size                 | 256 MB      | 单个写入器（Writer）在内存中用于缓冲数据的空间大小。当写满后会触发刷盘（Flush）操作，形成 L0 文件。该值影响 L0 文件的大小和写入吞吐量。         |
| num-sorted-run.compaction-trigger | 5           | 触发一次常规合并（Compaction）的 Sorted Run 数量阈值。值越小，合并越频繁，有利于查询但增加写放大；值越大，则反之。这是权衡写入和查询性能的关键参数。 |
| num-sorted-run.stop-trigger       | 10          | 触发写入暂停的 Sorted Run 数量阈值。当合并速度跟不上写入速度时，为防止 OOM 而设立的保护机制。                               |
| full-compaction.delta-commits     | (none)      | 两次全量合并（Full Compaction）之间的增量提交（Commit）次数。配置此项可定期进行全量合并，最大化查询性能，但会消耗较多资源。              |
| changelog-producer                | none        | Changelog 生成策略。input, lookup, full-compaction 等不同策略在生成完整变更日志的同时，会带来不同程度的写入开销。         |
| write-only                        | false       | 是否关闭写入端的合并操作。设置为 true 时，写入任务只负责生成 L0 文件，通常配合专用的合并作业（Dedicated Compaction Job）使用。      |

#### 表 2: 核心读取与元数据参数

| 参数 (Key)                        | 默认值     | 描述                                                                                                  |
| ------------------------------- | ------- | --------------------------------------------------------------------------------------------------- |
| scan.mode                       | default | Source 的读取模式，决定了从哪个快照开始读取数据。例如 latest（只读增量），from-timestamp（从指定时间点开始读存量和增量），incremental（读两个快照间的增量）等。 |
| scan.parallelism                | (none)  | Source 算子的读取并行度。不设置时由 Flink 框架自动推断。                                                                 |
| consumer-id                     | (none)  | 流式消费者的唯一标识。Paimon 会为每个 consumer-id 记录消费位点，以实现流式读取的 Exactly-Once。                                    |
| snapshot.num-retained.min       | 1       | 系统保证保留的最小快照数量。                                                                                      |
| snapshot.time-retained          | 1h      | 快照的最长保留时间。过期的快照及其相关文件将被清理。                                                                          |
| file-index.bloom-filter.columns | (none)  | 为指定的列创建 Bloom Filter 索引。对于高基数列的等值查询（= 或 IN），可以极大地提升过滤性能。                                            |
| deletion-vectors.enabled        | false   | 是否启用删除向量（Deletion Vectors）。启用后，更新和删除操作不会生成新的数据文件，而是在一个独立的索引文件中标记被删除的行，可大幅提升更新密集型场景下的查询性能。           |
| path                            | (none)  | 表文件在文件系统中的存储根路径。                                                                                    |

### 性能优化核心建议

Paimon 的性能调优是一个系统工程，核心在于管理 LSM-Tree 的“熵增”过程。所有的配置和优化手段，最终都是为了在“写入引入的无序性”和“查询需要的有序性”之间找到一个符合业务需求和资源限制的平衡点。LSM-Tree 的本质就是用“写入时的有序（内存排序后刷盘）”来换取“整体的无序（多层级文件）”，从而实现高写入吞吐。

Compaction 的作用就是“熵减”，通过消耗计算和 I/O 资源，将无序的多个小文件合并成有序的少量大文件，恢复系统的有序性，从而服务于查询。

一个优秀的 Paimon 架构师，其工作本质上是一个“数据热力学工程师”，需要深刻理解业务的读写模式，然后通过 Paimon 提供的丰富参数，去精确控制系统中数据有序度的生灭与平衡。

- 写入优化 (Write Tuning):

	- 合理设置 bucket: 这是最重要、最基础的调优手段。应根据数据总量、增量和更新频率，为表规划合适的桶数。目标是使稳定运行后，每个桶的数据量维持在推荐范围（例如 1GB 左右），避免数据倾斜。对于数据量未知或波动大的场景，可以采用动态桶（bucket=-1）或最新的自适应分桶（bucket=-2）来简化管理。
	
	- 调整写缓冲和 Flink Checkpoint: 增大 write-buffer-size 可以让内存缓冲更多数据，从而产生更大、更少的 L0 文件，减少了文件系统元数据操作的开销和刷盘频率。配合延长 Flink 的 execution.checkpointing.interval，可以显著提升写入吞吐量。但这会增加端到端的延迟，并消耗更多内存，需要在吞吐量和延迟之间做出权衡。
	
	- 本地合并 (Local Merging): 在某些场景下，如统计热门商品的点击量，会存在严重的主键数据倾斜。大量的更新操作都集中在少数几个主键上。此时可以开启 local-merge-buffer-size。该功能会在数据被 Shuffle 到 Sink 节点之前，在 Map 端进行一次本地的预聚合。这可以极大地减少网络传输的数据量和 Sink 端的状态操作，有效缓解热点问题。

- 查询优化 (Query Tuning):

	- 分区与主键设计: 精心设计表的分区键和主键。分区键应是查询中最常用的过滤条件（如日期、地区），以最大化分区裁剪的效果。主键的有序性也被 Paimon 利用，对主键的范围查询性能较好。
	
	- 使用索引 (Use Indexes): 对于经常用于等值过滤的高基数维度列（如 user_id），强烈建议开启 Bloom Filter 索引 (file-index.bloom-filter.columns)。查询时，Paimon 可以利用 Bloom Filter 快速判断一个数据文件或行组是否可能包含目标 user_id，从而跳过大量不相关的 I/O 操作。
	
	- 启用删除向量 (Enable Deletion Vectors): 对于更新和删除操作非常频繁的表，默认的 Merge-on-Read 模式在查询时需要读取大量包含旧版本数据的文件。启用 deletion-vectors.enabled 后，Paimon 会采用一种更接近 Merge-on-Write 的方式。更新和删除操作只会在一个高效的位图索引（删除向量）中标记哪些行已失效，而不会立即重写数据文件。查询时，读取器可以根据删除向量直接跳过这些失效的行，从而显著提升查询性能。但其代价是 Compaction 过程会变得更复杂。
	
	- Sort Compact: 对于追加表，特别是用于多维分析的场景，可以通过 CALL sys.compact 存储过程，并指定 order_strategy 为 z-order 或 hilbert，以及 order_by 的列。这会对数据文件进行重排序，将多维空间上邻近的点在物理存储上也尽可能排列在一起，从而在面对多列组合过滤条件时，能够更有效地进行数据跳过，提升查询性能。

- Compaction 优化 (Compaction Tuning):

	- 专用 Compaction 作业: 在生产环境中，特别是写入密集型或有多个数据源同时写入一张表的场景，强烈建议使用专用 Compaction 作业。通过在写入端设置 'write-only'='true'，将写入和合并的资源彻底隔离，可以避免 Compaction 影响写入的稳定性和延迟，是保障服务等级协议（SLA）的关键措施。
	
	- 调整 Compaction 触发阈值: 在写入吞吐和查询性能之间需要找到一个平衡点。适当调高 num-sorted-run.compaction-trigger 可以降低 Compaction 的频率，减少写放大，从而提升写入性能，但代价是瞬时文件数增多，可能影响查询性能。反之亦然。
	
	- Full Compaction 策略: Full Compaction 是一个非常消耗资源的操作，应谨慎配置。full-compaction.delta-commits 不宜设置得过小。对于非严格要求查询性能的场景，可以关闭自动 Full Compaction，改为在业务低峰期通过调度系统手动触发 CALL sys.compact() 来执行。

## 第五部分：实践中的挑战与未来展望

任何一项技术在走向成熟和广泛应用的过程中，都会面临实践的检验和持续的演进。本部分将探讨 Paimon 在实际应用中可能遇到的挑战、其最新的发展动态以及未来的技术方向。

### 常见难点与异常问题排查

- 小文件问题:

	- 现象: HDFS 或对象存储上出现大量体积很小的数据文件。
	
	- 原因: 频繁的 Flink Checkpoint、较小的 write-buffer-size、数据源本身流量低，或者分区/桶的粒度划分过细，导致每次刷盘的数据量都很少。
	
	- 影响: 对 HDFS NameNode 造成巨大压力，降低文件系统性能；增加查询时需要打开和合并的文件数量，拖慢查询速度。
	
	- 解决方案: 1) 适当增大 write-buffer-size 和 Flink Checkpoint 间隔。2) 对于追加表，定期运行 CALL sys.compact 并指定 order_strategy 进行排序合并。3) 对于主键表，确保 Full Compaction 能够定期执行。4) 合理设计分区和分桶策略，避免数据过度拆分。

- 数据倾斜:

	- 现象: Flink 作业中，部分 Sink Task（或 Source Task）的负载远高于其他 Task，成为整个作业的瓶颈，表现为 Flink UI 上部分 Subtask 的 inQueue 或 outQueue 持续很高。
	
	- 原因: bucket-key 的选择不当，导致大量数据被哈希到少数几个桶中。
	
	- 解决方案: 1) 选择一个或多个值分布更均匀的列作为 bucket-key。2) 对于主键更新倾斜的场景，开启 local-merge-buffer-size 进行预聚合。3) 考虑使用动态桶（bucket=-1）或自适应分桶（bucket=-2），让 Paimon 自动处理数据分布。

- Checkpoint 超时:

	- 现象: Flink 作业因 Checkpoint Timeout 而失败，日志中通常伴有 Checkpoint expired before completing 的错误信息。
	
	- 原因: 在 Checkpoint 期间，Committer 节点需要完成元数据提交，这个过程可能非常耗时，尤其是在 Full Compaction 或单次写入数据量巨大时。如果提交时间超过了 Flink 配置的 execution.checkpointing.timeout，作业就会失败。
	
	- 解决方案: 1) 延长 Flink 的 Checkpoint 超时时间。2) 使用专用 Compaction 作业，减轻写入端 Committer 的压力。3) 针对 Committer 节点进行资源调优，如使用 Flink 的细粒度资源管理功能，单独增加 Committer 的内存（sink.committer-memory）。

- FileNotFoundException:

	- 现象: 流式读取作业在运行一段时间后或重启后，抛出 FileNotFoundException 或类似错误，提示某个快照或数据文件不存在。
	- 原因: Paimon 的后台清理线程会根据快照保留策略（snapshot.time-retained 和 snapshot.num-retained.min）定期删除过期的快照和不再被任何有效快照引用的数据文件。如果流式消费者的消费速度过慢，或者作业停机时间过长，其需要消费的旧快照可能已经被清理掉了。
	- 解决方案: 1) 确保为流式作业设置了唯一的 consumer-id。Paimon 会为每个 consumer-id 记录消费位点，并保证该位点之后的快照不会被提前删除。2) 合理配置快照保留策略，使其时长大于可接受的最大作业停机和恢复时间。

- Schema 演进冲突:

	- 现象: 尝试修改表结构时失败，或 CDC 入湖时上游的 DDL 未能正确同步。
	
	- 原因: Paimon 目前支持的 Schema 演进操作是有限的，主要包括增加列和部分安全的类型提升（如 INT 到 BIGINT）。删除列、重命名列等破坏性操作通常会被忽略或不支持，以保证对历史数据的可读性。
	- 解决方案: 在设计上应尽量避免破坏性的 Schema 变更。对于 Flink CDC 入湖场景，Paimon 的 MySqlSyncTableAction 等工具能够自动处理大部分兼容的 Schema 变更。对于不支持的变更，需要人工介入处理。

### 最新进展 (基于 1.1 版本及更新)

Paimon 社区保持着高速的迭代，不断推出重要功能以提升其易用性、性能和生态兼容性。近期版本（如 1.1）的亮点包括：

- REST Catalog: 这是一项重大改进。它提供了一个轻量级的、可通过 REST API 访问的 Catalog 服务。这意味着 Paimon 可以彻底摆脱对重量级 Hive Metastore 的依赖，极大地简化了部署架构，特别是在云原生和容器化环境中。同时，开放的 API 也避免了厂商锁定，增强了系统的灵活性。
- 外部文件模式 (External File Mode): 通过 data-file.external-paths 参数，Paimon 现在允许数据文件存储在表的主目录之外。这个功能解锁了许多高级应用场景，例如，可以将热数据存储在高性能的 SSD 上，而将冷数据自动归档到成本更低的对象存储中，实现冷热数据分层管理。
- 自适应分桶 (Adaptive Bucket / Postpone Bucket): 分桶策略一直是 Paimon 使用中的一个难点。为了解决这个问题，社区推出了自适应分桶模式（通过设置 bucket = -2 激活）。在这种模式下，新写入的数据会先进入一个临时区域，用户无需再预先规划桶的数量和担心 Compaction 的稳定性。后端的服务或专用的 Compaction 作业可以根据数据的实际情况，智能地进行合并和重分布（Rescaling）。这极大地降低了 Paimon 的使用门槛和运维复杂度。
- 生态系统扩展: Paimon 持续扩展其对底层文件系统的支持，新版本中增加了对腾讯云对象存储（COS）、Microsoft Azure Storage 和华为云对象存储服务（OBS）的原生支持，进一步拓宽了其部署选择。
- Iceberg 表原地升级: 对于已经在使用 Iceberg 的用户，Paimon 提供了从 Iceberg 表到 Paimon 表的原地升级工具（目前主要适用于 HDFS 等支持 rename 操作的文件系统），方便用户迁移和试用。

### 技术路线图与未来方向

Paimon 的发展路径清晰地呈现出“对内简化，对外开放”的成熟趋势。它在努力解决自身核心架构（LSM）带来的运维复杂性的同时，积极拥抱并融入更广泛的数据湖生态，谋求的是在“实时流式”这一垂直领域的领导地位，而非对其他湖仓格式的全面取代。

- Merge-on-Write (Deletion Vectors) 的成熟: 持续优化删除向量是 Paimon 近期的核心方向之一。目标是使其在主键表和追加表上都更加稳定和高效，并支持与异步 Compaction 更好地协同工作。这将是彻底解决更新密集型场景查询性能问题的关键。
- 与 Iceberg 深度融合: Paimon 计划支持直接生成 Iceberg 兼容的快照格式。这意味着一张 Paimon 表未来可能被原生的 Iceberg 读取器直接查询，这将极大地增强 Paimon 的生态互操作性，让用户可以在一个混合架构中无缝地利用 Paimon 的流式更新能力和 Iceberg 广泛的生态支持。
- 半结构化数据支持 (Variant Type): 为了更好地适应日志分析、事件流处理等场景，Paimon 计划引入对 VARIANT 类型的支持。这将使其能够高效地存储和查询 JSON 等半结构化数据，进一步扩展其应用领域。
- 更丰富的索引类型: 除了现有的 Min/Max 统计信息和 Bloom Filter，Paimon 路线图上还包括了 Bitmap 索引和倒排（Inverse）索引等更高级的索引类型。这些索引将为特定查询模式（如低基数列过滤、文本搜索等）带来数量级的性能提升。
- 查询与写入能力增强: Paimon 也在持续增强其核心能力，未来的计划包括：支持 Flink 的大规模 Lookup Join 优化、集成 Spark 的 Liquid Clustering 以实现更灵活的数据布局、提供更高级别的事务隔离（如可串行化）等。
- 无依赖轻量级 SDK: 为了降低客户端集成的复杂度和依赖冲突的风险，社区计划开发一个不依赖 Hadoop 相关库的轻量级 REST SDK，让各种语言和应用都能更轻松地与 Paimon 交互。

Paimon 正在从一个“需要专家来配置的强大工具”向一个“让更多人能轻松使用的强大平台”演进。其未来的竞争力不仅在于其强大的流式内核，更在于其能否成功降低自身复杂性，并无缝地嵌入到企业现有的、异构的数据湖生态体系中。

## 附录：技术问答

- Q1: Paimon, Hudi, Iceberg, Delta Lake 的核心区别是什么？我应该如何选择？

- A: 这四种主流数据湖格式的核心区别在于其设计哲学和最擅长的领域。

	- Paimon: 为流而生（LSM-based）。其架构与 Flink 深度绑定，在处理实时 CDC 数据入湖、高频更新、生成完整流式 Changelog 等场景下具有无与伦比的性能和架构优势。
	- Hudi: 功能最为全面和复杂，同时支持写时复制（COW）和写时合并（MOR）两种模式，提供了丰富的索引机制和并发控制选项。灵活性高，但学习曲线和运维成本也最高。
	- Iceberg: 设计简洁、开放，拥有强大的社区生态和优秀的元数据管理能力。其核心优势在于批处理场景的稳定性和与其他引擎的互操作性。
	- Delta Lake: 与 Spark 生态深度集成，提供了简单易用的 ACID 事务和时间旅行功能，在 Spark 技术栈中体验最为流畅。

	选择建议:
	
	- 如果你的核心场景是 Flink CDC 入湖、构建实时动态表，或者需要为下游提供高质量的流式变更数据，Paimon 是首选。
	- 如果你的技术栈以 Spark 为主，需要在灵活性和更新性能之间做权衡，可以考虑 Hudi 或 Delta Lake。
	- 如果你的主要场景是构建稳定、开放的批处理数仓，对生态兼容性要求高，Iceberg 是非常优秀的选择。

- Q2: 为什么我的 Paimon 写入作业会出现反压（Backpressure）？

- A: Paimon 写入作业出现反压通常由以下几个原因造成：

	1. Checkpoint 过于频繁: Flink 的 Checkpoint 会触发 Paimon 的 prepareCommit，导致内存数据刷盘。过于频繁的 Checkpoint 会导致 Sink 端持续忙于 I/O 操作，无法及时消费上游数据。
	2. Compaction 压力过大: 如果采用内联合并（Inline Compaction），合并操作会与数据写入竞争 CPU 和 I/O 资源。当写入速度远大于合并速度时，L0 文件堆积，最终可能触发写暂停（num-sorted-run.stop-trigger），从而产生反压。
	3. 数据倾斜: bucket-key 分布不均，导致数据集中写入少数几个桶（Bucket），造成部分 Sink Subtask 成为瓶颈。
	4. Committer 成为瓶颈: 在单次提交数据量巨大时，Committer 节点需要处理大量元数据，可能因 CPU 或内存不足而变慢。
	排查思路: 首先通过 Flink Web UI 观察反压的传递路径，定位到是哪个算子产生了反压。然后检查 Sink 节点的 Task Metrics，关注 Compaction 相关的指标。可以尝试延长 Checkpoint 间隔、将 Compaction 剥离为专用作业、检查 bucket-key 的合理性或开启本地合并来解决。

- Q3: bucket 设为-1（动态桶）和固定桶有什么区别？

- A:
	- 固定桶 (bucket > 0): 在建表时就必须指定一个固定的桶数。数据通过对 bucket-key 的哈希值取模来路由。
	
		- 优点: 行为可预测，性能稳定，支持多作业并发写入（只要不写入同一个分区）。	
		- 缺点: 需要预先规划和评估数据量来确定合适的桶数。如果桶数设置不当（过多或过少），会导致小文件或数据倾斜问题，且后期调整成本高（需要重写数据）。
		
	- 动态桶 (bucket = -1): 无需在建表时指定桶数。Paimon 会根据写入的数据动态地创建、分裂和合并桶。
	
		- 优点: 使用简单，无需预估数据量，能够自适应数据增长和分布。
		- 缺点: 其实现依赖于一个内部索引来维护主键到桶的映射，这会带来额外的性能开销，尤其是在跨分区更新时。目前，动态桶模式通常只支持单个作业写入同一个分区，以避免并发冲突。

- Q4: Paimon 如何保证流式读取的 Exactly-Once？

- A: Paimon 通过 consumer-id 机制 和 Flink 的 Checkpoint 协同工作来保证流式读取的 Exactly-Once 语义。

	1. 当一个流式读取作业启动时，必须为其指定一个唯一的 consumer-id。
	2. Paimon 会在文件系统上为这个 consumer-id 专门记录一个消费位点文件，该文件内容是消费者已经成功处理并完成 Checkpoint 的下一个快照 ID。
	3. 当 Flink 作业从故障中恢复时，Paimon Source 会读取这个位点文件，获取到上次成功消费的快照 ID，然后从该 ID 的下一个快照开始读取增量数据。
	4. 这个过程与 Flink 的状态恢复机制相结合，确保了数据既不会重复消费，也不会遗漏。前提是 Paimon 的快照保留时间（snapshot.time-retained）必须长于 Flink 作业可能的最大停机和恢复时间。

- Q5: 我可以在 Paimon 中执行 UPDATE 或 DELETE 语句吗？

- A: Paimon 存储层本身是支持更新和删除逻辑的，但能否直接执行 UPDATE 或 DELETE SQL 语句，取决于上层的计算引擎。

	- Flink SQL: 目前 Flink SQL 对 Paimon 的 DML 支持主要是通过流式 INSERT INTO 语句来实现的。对于主键表，向其 INSERT 一条已存在主键的记录，其效果就等同于 UPDATE（根据 merge-engine 的逻辑）。要表达 DELETE，需要上游数据源能产生 DELETE 类型的 Changelog 记录。
	- Spark SQL: Spark SQL 对 Paimon 的 DML 支持更为完善。你可以像操作普通数据库一样，直接在 Spark SQL 中对 Paimon 表执行 UPDATE... SET... WHERE...，DELETE FROM... WHERE... 以及 MERGE INTO 等语句。
	- Trino / Presto: 这类 OLAP 查询引擎目前主要支持对 Paimon 表的 SELECT 查询操作，DML 支持有限。