# bigdata

## 计算引擎

### Spark

Spark 是一个用于大规模数据处理的统一分析引擎。它提供 Scala、Java、Python 和 R（已废弃）语言的高级 API，以及支持数据分析通用计算图的优化引擎。它还支持丰富的高级工具集，包括用于 SQL 和 DataFrames 的 Spark SQL、用于 pandas 工作负载的 Spark 上的 pandas API、用于机器学习的 MLlib、用于图处理的 GraphX 以及用于流处理的 Structured Streaming。

- https://github.com/apache/spark
- https://spark.apache.org/docs/latest/

### Flink

Apache Flink 是一个在有界数据流和无界数据流上进行有状态计算分布式处理引擎和框架。Flink 设计旨在所有常见的集群环境中运行，以任意规模和内存级速度执行计算。

- https://github.com/apache/flink
- https://flink.apache.org/
- https://nightlies.apache.org/flink/flink-docs-release-2.1/zh/

### Fluss

Apache Fluss（孵化中）是一款为实时分析打造的流存储，可作为湖仓架构的实时数据层。凭借其列式流和实时更新能力，Fluss 与 Apache Flink 实现无缝集成，能够构建出高吞吐量、低延迟且经济高效的流数据仓库，专门适用于实时应用场景。

- https://github.com/apache/fluss
- https://fluss.apache.org/

## 分析型数据库

### Doris

Apache Doris 是基于 MPP 架构的易用、高性能、实时分析数据库，以其极快的速度和易用性而著称。在海量数据下，它只需要亚秒级的响应时间就能返回查询结果，不仅能支持高并发点查询场景，还能支持高吞吐量的复杂分析场景。
这一切使得 Apache Doris 成为报表分析、临时查询、统一数据仓库和数据湖查询加速等场景的理想工具。在 Apache Doris 上，用户可以构建各种应用，如用户行为分析、AB 测试平台、日志检索分析、用户画像分析和订单分析等。

- https://github.com/apache/doris
- https://doris.apache.org/zh-CN/docs/3.0/gettingStarted/what-is-apache-doris

### DuckDB

DuckDB 是一个高性能分析数据库系统。它设计得快速、可靠、便携、易用。DuckDB 提供了丰富的 SQL 方言，支持范围远远超出了基本 SQL。DuckDB 支持任意和嵌套的相关子查询、窗口函数、collations 校对、复杂类型（数组、结构体、映射）以及一些旨在使 SQL 更易于使用的扩展。

- https://github.com/duckdb/duckdb
- https://duckdb.org/
- https://duckdb.org/docs/stable/sql/dialect/friendly_sql.html
- https://shell.duckdb.org/

## 数据湖

### Paimon

一种 Lake 格式，支持使用 Flink 和 Spark 构建实时 Lakehouse 架构，用于流式和批处理操作。创新地结合了 Lake 格式和 LSM 结构，将实时流式更新引入 Lake 架构。

- https://github.com/apache/paimon/
- https://paimon.apache.org/

### Iceberg

Iceberg是一种用于大型分析表的高性能格式。Iceberg将SQL表的可靠性和简洁性带入大数据领域，同时使Spark、Trino、Flink、Presto、Hive和Impala等引擎能够安全地同时处理相同的表。

- https://github.com/apache/iceberg
- https://iceberg.apache.org/

### Hudi

Apache Hudi 是一个开放式数据湖平台，基于高性能开放表格式构建，可为您的数据湖带来数据库功能。
Hudi 采用功能强大的新增量处理框架，重新设计了缓慢的老式批量数据处理，可实现低延迟的分钟级分析。

- https://github.com/apache/hudi
- https://hudi.apache.org/cn/

### DuckLake

DuckLake 通过使用 Parquet 文件和您的 SQL 数据库，提供了先进的数据湖功能，同时避免了传统数据湖仓的复杂性。它是 DuckDB 团队推出的一种开放、独立的格式。

- https://github.com/duckdb/ducklake
- https://ducklake.select/
- https://duckdb.org/2025/09/17/ducklake-03.html
