# import libraries
from k8s_example.code.spark.example.settings import *
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from schemas import schemadimpromotion
from pyspark.sql.functions import *

# main spark program
if __name__ == '__main__':

    # init spark session
    spark = SparkSession \
            .builder \
            .appName("dimpromotion-stream") \
            .config("spark.hadoop.fs.s3a.endpoint", S3ENDPOINT) \
            .config("spark.hadoop.fs.s3a.access.key", S3ACCESSKEY) \
            .config("spark.hadoop.fs.s3a.secret.key", S3SECRETKEY) \
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

    # refer to schema.py file
    schema = schemadimpromotion
    
    origin_folder = "s3a://landing/example/dw-files/promotion"

    destination_topic = "dimpromotion_spark_stream_dwfiles"

    landing_table = spark.readStream.options(header='False',delimiter=',').csv(origin_folder, schema=schema)
    landing_table.printSchema()
    print(landing_table.isStreaming)

    # trigger using processing time = interval of the micro-batches
    # formatting to deliver to apache kafka payload (value)
    write_into_topic = landing_table \
        .selectExpr("CAST(trim(PromotionKey) AS STRING) AS key", "to_json(struct(*)) AS value") \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", BOOTSTRAP_SERVERS) \
        .option("topic", destination_topic) \
        .option("checkpointLocation", "checkpoint") \
        .outputMode("append") \
        .trigger(processingTime="120 seconds") \
        .start()  \
        
    # monitoring streaming queries
    # structured streaming output info
    # read last progress & last status of query
    print(write_into_topic.lastProgress)
    print(write_into_topic.status)

    # block until query is terminated
    write_into_topic.awaitTermination()