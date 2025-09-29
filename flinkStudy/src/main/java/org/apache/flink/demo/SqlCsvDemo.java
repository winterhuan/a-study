package org.apache.flink.demo;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.table.api.bridge.java.StreamTableEnvironment;

import java.io.FileWriter;
import java.io.IOException;

/**
 * Flink SQL版本的CSV处理示例
 * 演示如何使用Flink SQL处理CSV文件数据
 */
public class SqlCsvDemo {

    private static final String CSV_FILE_PATH = "/tmp/sales_records.csv";

    public static void main(String[] args) throws Exception {
        // 创建示例数据
        createSampleData();
        
        // 设置流处理执行环境
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        
        // 创建表环境
        final StreamTableEnvironment tableEnv = StreamTableEnvironment.create(env);
        
        // 创建输入表 - 从CSV文件读取数据
        tableEnv.executeSql(
            "CREATE TABLE sales_records (" +
            "  transaction_id BIGINT," +
            "  product_name STRING," +
            "  category STRING," +
            "  quantity INT," +
            "  price DOUBLE," +
            "  transaction_time STRING" +
            ") WITH (" +
            "  'connector' = 'filesystem'," +
            "  'path' = 'file://" + CSV_FILE_PATH + "'," +
            "  'format' = 'csv'," +
            "  'csv.field-delimiter' = ','," +
            "  'csv.ignore-parse-errors' = 'true'" +
            ")"
        );
        
        // 创建输出表 - 打印到控制台
        tableEnv.executeSql(
            "CREATE TABLE sales_summary (" +
            "  category STRING," +
            "  total_sales DOUBLE," +
            "  record_count BIGINT" +
            ") WITH (" +
            "  'connector' = 'print'" +
            ")"
        );
        
        // 执行SQL查询: 按类别统计销售额
        tableEnv.executeSql(
            "INSERT INTO sales_summary " +
            "SELECT category, " +
            "       SUM(price * quantity) as total_sales, " +
            "       COUNT(*) as record_count " +
            "FROM sales_records " +
            "GROUP BY category"
        );
    }
    
    /**
     * 创建示例CSV数据文件
     */
    private static void createSampleData() {
        String[][] data = {
            {"1", "ProductA", "Electronics", "2", "299.99", "2023-01-01 10:00:00"},
            {"2", "ProductB", "Books", "1", "19.99", "2023-01-01 10:05:00"},
            {"3", "ProductC", "Electronics", "1", "199.99", "2023-01-01 10:10:00"},
            {"4", "ProductA", "Electronics", "1", "299.99", "2023-01-01 10:15:00"},
            {"5", "ProductD", "Clothing", "3", "49.99", "2023-01-01 10:20:00"},
            {"6", "ProductE", "Books", "2", "24.99", "2023-01-01 10:25:00"},
            {"7", "ProductF", "Beauty", "1", "99.99", "2023-01-01 10:30:00"},
            {"8", "ProductG", "Beauty", "2", "89.99", "2023-01-01 10:35:00"},
            {"9", "ProductH", "Clothing", "1", "79.99", "2023-01-01 10:40:00"},
            {"10", "ProductI", "Electronics", "1", "499.99", "2023-01-01 10:45:00"}
        };

        try (FileWriter writer = new FileWriter(CSV_FILE_PATH)) {
            // 写入CSV数据
            for (String[] row : data) {
                writer.append(String.join(",", row));
                writer.append("\n");
            }
            
            System.out.println("Sample CSV data file created at: " + CSV_FILE_PATH);
        } catch (IOException e) {
            System.err.println("Error writing CSV file: " + e.getMessage());
            e.printStackTrace();
        }
    }
}