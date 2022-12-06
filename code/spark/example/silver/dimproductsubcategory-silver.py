# import libraries
import settings
from pyspark.sql.functions import *
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from schemas import schemadimproductsubcategory

# main spark program
if __name__ == '__main__':

    # init spark session
    spark = SparkSession \
            .builder \
            .appName("example-dimproductsubcategory-silver") \
            .config("spark.hadoop.fs.s3a.endpoint", settings.S3ENDPOINT) \
            .config("spark.hadoop.fs.s3a.access.key", settings.S3ACCESSKEY) \
            .config("spark.hadoop.fs.s3a.secret.key", settings.S3SECRETKEY) \
            .config("spark.hadoop.fs.s3a.path.style.access", True) \
            .config("spark.hadoop.fs.s3a.fast.upload", True) \
            .config("spark.hadoop.fs.s3a.multipart.size", 104857600) \
            .config("fs.s3a.connection.maximum", 100) \
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.delta.logStore.class", "org.apache.spark.sql.delta.storage.S3SingleDriverLogStore") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .config("spark.sql.streaming.kafka.useDeprecatedOffsetFetching","false") \
            .getOrCreate()

    # set log level to info
    # [INFO] or [WARN] for more detailed logging info
    spark.sparkContext.setLogLevel("INFO")

    # refer to schemas.py file
    schema = schemadimproductsubcategory
    input_topic = "dimproductsubcategory_spark_stream_dwfiles"
    destination_folder = "s3a://lakehouse/silver/example/dimproductsubcategory/"
    write_delta_mode = "overwrite"
    jsonOptions = {"timestampFormat": "yyyy-MM-dd'T'HH:mm:ss.sss'Z'"}

    # reading data from apache kafka
    # stream operation mode
    # latest offset recorded on kafka and spark
    stream_table= spark \
        .readStream\
        .format("kafka") \
        .option("kafka.bootstrap.servers", settings.BOOTSTRAP_SERVERS) \
        .option("subscribe", input_topic) \
        .option("startingOffsets", "latest") \
        .option("checkpoint", "checkpoint") \
        .load() \
        .select(from_json(col("value").cast("string"), schema, jsonOptions).alias("table_tpc"))


    stream_table_col = (stream_table
    .select(
        col("table_tpc.ProductSubcategoryKey").alias("ProductSubcategoryKey"),
        col("table_tpc.ProductSubcategoryAlternateKey").alias("ProductSubcategoryAlternateKey"),
        col("table_tpc.EnglishProductSubcategoryName").alias("EnglishProductSubcategoryName"),
        col("table_tpc.SpanishProductSubcategoryName").alias("SpanishProductSubcategoryName"),
        col("table_tpc.FrenchProductSubcategoryName").alias("FrenchProductSubcategoryName"),
        col("table_tpc.ProductCategoryKey").alias("ProductCategoryKey"),
    )
    )

    def upsertToDelta(microBatchOutputDF, batchId):
        dt_table = DeltaTable.forPath(spark, destination_folder)
        dt_table.alias("historical_data")\
            .merge(
                stream_table.alias("new_data"),
                '''
                historical_data.ProductSubcategoryKey = new_data.ProductSubcategoryKey 
                ''')\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()\
            .execute()

    # write to silver
    if DeltaTable.isDeltaTable(spark, destination_folder):
        stream_table_col.writeStream \
        .format("delta") \
        .foreachBatch(upsertToDelta) \
        .outputMode("update") \
        .start()
    else:
        write_stream_table_col = (stream_table_col.writeStream
            .format("delta")
            .outputMode("append")
            .option("checkpointLocation", "checkpoint")
            .start(destination_folder)
        )


        print(write_stream_table_col.lastProgress)
        print(write_stream_table_col.status)
        write_stream_table_col.awaitTermination()