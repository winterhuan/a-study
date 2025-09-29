use arrow::{
    array::{Int32Array, StringArray},
    datatypes::{DataType, Field, Schema},
    record_batch::RecordBatch,
};
use arrow_array::RecordBatchIterator;
use futures::stream::StreamExt;
use lance::{Dataset, dataset::WriteParams};
use std::sync::Arc;

// Using Arrow's own RecordBatchIterator to simplify the example.

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    let dataset_uri = "file:///tmp/test_dataset";

    println!("Creating Lance dataset example...");

    // Create schema
    let schema = Arc::new(Schema::new(vec![
        Field::new("id", DataType::Int32, false),
        Field::new("name", DataType::Utf8, false),
    ]));

    // Create sample data
    let batch1 = RecordBatch::try_new(
        schema.clone(),
        vec![
            Arc::new(Int32Array::from(vec![1, 2, 3, 4, 5])),
            Arc::new(StringArray::from(vec![
                "Alice", "Bob", "Charlie", "Diana", "Eve",
            ])),
        ],
    )?;

    let batch2 = RecordBatch::try_new(
        schema.clone(),
        vec![
            Arc::new(Int32Array::from(vec![6, 7, 8, 9, 10])),
            Arc::new(StringArray::from(vec![
                "Frank", "Grace", "Henry", "Iris", "Jack",
            ])),
        ],
    )?;

    let batches = vec![batch1, batch2];

    // Create dataset
    let write_params = WriteParams::default();
    // RecordBatchIterator expects an IntoIterator whose Item = Result<RecordBatch, ArrowError>.
    // We have an in-memory Vec<RecordBatch>, so map each batch into Ok(batch) to satisfy the API.
    // This uses Arrow's provided `RecordBatchIterator` instead of a custom reader implementation.
    let reader = RecordBatchIterator::new(batches.into_iter().map(Ok), schema.clone());
    Dataset::write(reader, dataset_uri, Some(write_params)).await?;
    println!("Dataset created successfully!");

    // Read dataset
    println!("\nReading dataset...");
    let dataset = Dataset::open(dataset_uri).await?;
    let scanner = dataset.scan();
    let mut stream = scanner.try_into_stream().await?;

    let mut all_batches = Vec::new();
    while let Some(batch) = stream.next().await {
        all_batches.push(batch?);
    }

    println!("Read {} batches", all_batches.len());
    for (i, batch) in all_batches.iter().enumerate() {
        println!("Batch {}: {} rows", i, batch.num_rows());
    }

    // Take specific rows
    println!("\nTaking specific rows...");
    // Indices are global row indices across the entire dataset (not per-batch).
    let indices: Vec<u64> = vec![0u64, 2u64, 4u64, 6u64, 8u64];

    match dataset.take(&indices[..], dataset.schema().clone()).await {
        Ok(batch) => {
            println!("Successfully took {} rows", batch.num_rows());

            // Display the taken data. Show the original global index for clarity.
            if let (Some(id_column), Some(name_column)) = (
                batch.column(0).as_any().downcast_ref::<Int32Array>(),
                batch.column(1).as_any().downcast_ref::<StringArray>(),
            ) {
                for (out_pos, orig_idx) in indices.iter().enumerate() {
                    println!(
                        "Row {}: id={}, name={}",
                        orig_idx,
                        id_column.value(out_pos),
                        name_column.value(out_pos)
                    );
                }
            } else {
                println!("Unexpected column types in taken batch");
            }
        }
        Err(e) => println!("Error taking rows: {}", e),
    }

    println!("\nAll examples completed successfully!");
    Ok(())
}
