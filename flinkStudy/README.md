# Flink Study Project

This project contains examples and demos for Apache Flink.

## 项目结构

- [src/main/java](src/main/java): Java source code
- [docs](docs): Documentation
- [lib](lib): Flink connector JARs (created by download script)

## 环境要求

- Java 11 或更高版本
- Maven 3.0 或更高版本

## 依赖和连接器

一些 Flink SQL 连接器未发布到 Maven Central，必须以不同方式处理：

1. **在 Maven Central 中可用**:
   - `flink-connector-datagen` (用于测试/演示目的)

2. **不在 Maven Central 中可用**:
   - `flink-sql-connector-files` 和其他连接器必须从官方 Flink 发行版下载

## 如何处理 Flink 连接器

### 选项 1: 自动下载脚本

运行提供的脚本来自动下载可用的连接器：

```bash
./download-flink-connectors.sh
```

这会将连接器 JAR 下载到 [lib](lib) 目录。

### 选项 2: 手动下载

对于不在 Maven Central 中的连接器：

1. 从[官方网站](https://flink.apache.org/downloads/)下载 Flink 二进制发行版
2. 解压归档文件
3. 从 `opt` 目录复制所需的连接器 JAR 到你的 Flink `lib` 目录

### 选项 3: 与 Flink 发行版一起使用

如果你要与 Flink 发行版一起运行：

1. 将连接器 JAR 放在 Flink `lib` 目录中
2. 正常启动 Flink
3. 连接器将自动可用

## 构建项目

使用 Maven 构建项目：

```bash
mvn clean package
```

这将生成一个包含所有依赖的 fat jar 文件：`target/flink-demo-1.0-SNAPSHOT.jar`

## 运行示例

### 1. WordCount 示例（批处理）

这个示例使用内置的数据集进行词频统计：

```bash
java -cp target/flink-demo-1.0-SNAPSHOT.jar org.apache.flink.demo.WordCount
```

### 2. SocketStreamWordCount 示例（流处理）

这个示例从 socket 连接读取数据进行实时词频统计。

首先，打开一个终端并启动 netcat 服务：

```bash
nc -l 9999
```

然后在另一个终端运行 Flink 程序：

```bash
java -cp target/flink-demo-1.0-SNAPSHOT.jar org.apache.flink.demo.SocketStreamWordCount localhost 9999
```

现在可以在 netcat 终端中输入文本，Flink 程序会实时处理并显示词频统计结果。

### 3. WindowWordCount 示例（窗口流处理）

这个示例演示了基于时间窗口的流处理。

同样，首先启动 netcat 服务：

```bash
nc -l 9998
```

然后运行 Flink 程序：

```bash
java -cp target/flink-demo-1.0-SNAPSHOT.jar org.apache.flink.demo.WindowWordCount localhost 9998
```

程序会每5秒输出一次窗口内的词频统计结果。

### 4. SqlWordCountDemo 示例（Flink SQL）

这个示例演示了如何使用 Flink SQL 进行词频统计。

```bash
java -cp target/flink-demo-1.0-SNAPSHOT.jar org.apache.flink.demo.SqlWordCountDemo
```

该示例使用 datagen connector 自动生成随机单词，并使用 print connector 输出统计结果。

### 5. SqlCsvDemo 示例（Flink SQL处理CSV文件）

这个示例演示了如何使用 Flink SQL 处理 CSV 文件数据。

```bash
java -cp target/flink-demo-1.0-SNAPSHOT.jar org.apache.flink.demo.SqlCsvDemo
```

该示例会自动创建示例 CSV 文件 [/tmp/sales_records.csv](file:///tmp/sales_records.csv)，然后读取该文件，按类别统计销售额并输出结果。

## 在 Flink 集群上运行

要将程序提交到 Flink 集群运行，可以使用 Flink 的命令行工具：

```bash
# 假设 FLINK_HOME 是 Flink 的安装目录
$FLINK_HOME/bin/flink run target/flink-demo-1.0-SNAPSHOT.jar
```

对于需要参数的程序（如 SocketStreamWordCount 和 WindowWordCount），需要指定主机和端口：

```bash
$FLINK_HOME/bin/flink run target/flink-demo-1.0-SNAPSHOT.jar localhost 9999
```

## 项目依赖

该项目使用以下主要依赖：

- Flink Streaming API
- Flink Clients (用于本地执行和集群提交)
- Flink Table API & SQL (用于SQL示例)
- SLF4J (简单日志门面)

所有依赖都已在 `pom.xml` 中配置。
