# 问题

## SQL 和 DataFrame 的执行流程

1. SQL 到 RDD 的基于源码的详细转换流程
2. DataFrame 到 RDD 的基于源码的详细转换流程

## Spark datasource v2 的源码流程

1. datasource v2 的源码流程。
2. driver 和 executor 是怎么在流程中交互的，配置和分区信息是怎么从 driver 传递给 executor 的？
3. push down filter 是如何实现的？
4. mongo-spark 中是怎么和 datasource v2 集成的？

## Executor 的执行

1. 解析 executor 是如何执行任务，是怎么使用线程池实现资源隔离？
2. spark executor 的 jvm 环境是怎么创建出来的，task 的代码是怎么加载的，怎么跑起来的？
3. spark.executor.cores, spark,executor.memory， spark.executor.memoryHead 是如何生效的？

## Spark Shuffle 的执行流程

1. shuffle 基于源码的详细执行流程。
2. shuffle 的数据结构和存储实现。
3. 不同 shuffle 算法的实现原理。
4. Hash 和 sort shuffle 的区别。

## Spark Structured Streaming 的执行流程

1. Structured Streaming 基于源码的详细执行流程
2. Structured Streaming 的数据结构实现。
3. Structured Streaming 的数据存储实现。
4. Structured Streaming 的水印实现。
5. Structured Streaming 的 window 实现。
6. Structured Streaming 的 checkpoint 实现。
7. Structured Streaming 的数据源实现。
8. Structured Streaming 的 sink 实现。
9. Structured Streaming 的端到端仅处理一次保证的实现。

## 数据倾斜

Spark 数据倾斜的解决方案有哪些？

## 调度

Spark 任务调度的方式有哪些？

## AQE

1. AQE 的原理是什么？
