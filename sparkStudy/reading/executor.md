# Executor

是一个 JVM, 入口是 ExecutorBackend 的实现类。

CoarseGrainedExecutorBackend 是 Spark 的标准 Executor 后端实现，而 KubernetesExecutorBackend 是在 Kubernetes 环境中运行时使用的特化版本。

KubernetesExecutorBackend 重用了 CoarseGrainedExecutorBackend 的核心功能，但添加了 Kubernetes 特定的逻辑，如动态 Executor ID 生成和特定的错误处理机制。

KubernetesExecutorBackend main -> run 的关键代码如下:

```scala
val env = SparkEnv.createExecutorEnv(driverConf, execId, arguments.bindAddress,
  arguments.hostname, arguments.cores, cfg.ioEncryptionKey, isLocal = false)
// backendCreateFn 是 new CoarseGrainedExecutorBackend
val backend = backendCreateFn(env.rpcEnv, arguments, env, cfg.resourceProfile, execId)
env.rpcEnv.setupEndpoint("Executor", backend)
// 确保 Kubernetes 上运行的 Executor 进程保持运行状态，直到收到终止信号。这很重要，因为 Executor 需要持续运行以处理来自 Driver 的任务请求
env.rpcEnv.awaitTermination()
```

## CoarseGrainedExecutorBackend

CoarseGrainedExecutorBackend 是 Spark 中一个通用的 Executor 后端实现，主要用于在集群环境中运行任务。它是 Spark 执行任务的核心组件之一。

主要功能包括：

- 连接到 Driver 并注册自己
- 接收并执行分配给它的任务
- 向 Driver 报告任务状态更新
- 管理 Executor 的生命周期

继承了 IsolatedThreadSafeRpcEndpoint，当 setupEndpoint 之后，CoarseGrainedExecutorBackend 可以接收来自 Driver 的消息进行业务逻辑处理。

CoarseGrainedExecutorBackend 的完整生命周期如下：

- 通过 main 方法启动
- 调用 run 方法进行初始化
- 在 RPC 环境中设置端点，触发 onStart
- 连接并注册到 Driver
- 接收 Driver 消息执行任务
- 通过 statusUpdate 向 Driver 报告状态
- 接收关闭指令，优雅退出

onStart 方法 - 启动时调用：

- 注册信号处理器（用于优雅关闭）
- 解析资源信息
- 异步连接到 Driver 并注册 Executor

消息处理流程：

- RegisteredExecutor 消息：创建 Executor 实例
- LaunchTask 消息：调用 executor.launchTask 执行任务
- KillTask 消息：调用 executor.killTask 终止任务
- StopExecutor 消息：停止 Executor
