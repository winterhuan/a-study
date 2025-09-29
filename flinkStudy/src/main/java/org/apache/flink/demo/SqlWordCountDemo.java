package org.apache.flink.demo;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

/**
 * Flink SQL版本的WordCount示例
 * 演示如何使用Flink SQL进行简单的词频统计
 */
public class SqlWordCountDemo {

    public static void main(String[] args) throws Exception {
        // 设置流处理执行环境
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // 创建表环境
        final StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        
        // 创建输入表 - 使用内存中的数据
        tableEnv.executeSql(
            "CREATE TABLE words (" +
            "  word STRING" +
            ") WITH (" +
            "  'connector' = 'datagen'," +
            "  'rows-per-second' = '100'," +
            "  'fields.word.kind' = 'random'," +
            "  'fields.word.length' = '10'" +
            ")"
        );
        
        // 创建输出表 - 打印到控制台
        tableEnv.executeSql(
            "CREATE TABLE word_count (" +
            "  word STRING," +
            "  cnt BIGINT" +
            ") WITH (" +
            "  'connector' = 'print'" +
            ")"
        );
        
        // 执行SQL查询并将结果插入到输出表中
        tableEnv.executeSql(
            "INSERT INTO word_count " +
            "SELECT word, COUNT(*) AS cnt " +
            "FROM words " +
            "GROUP BY word"
        );
    }
}