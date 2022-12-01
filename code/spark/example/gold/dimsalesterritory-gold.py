# import libraries
import settings
from pyspark.sql.functions import *
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from schemas import schemadimsalesterritory
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, DateType, FloatType, BooleanType, DoubleType, ByteType

# main spark program
if __name__ == '__main__':

    # init spark session
    spark = SparkSession \
            .builder \
            .appName("example-dimsalesterritory-gold") \
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
    schema = schemadimsalesterritory
    input_topic = "dimsalesterritory_spark_stream_dwfiles"
    destination_table = "public.dimsalesterritory"
    jsonOptions = {"timestampFormat": "yyyy-MM-dd'T'HH:mm:ss.sss'Z'"}
    destination_folder = "s3a://lakehouse/gold/example/dimsalesterritory/"
    write_delta_mode = "overwrite"

    # reading data from apache kafka
    # stream operation mode
    # latest offset recorded on kafka and spark
    stream_table= spark \
        .read\
        .format("kafka") \
        .option("kafka.bootstrap.servers", settings.BOOTSTRAP_SERVERS) \
        .option("subscribe", input_topic) \
        .option("startingOffsets", "latest") \
        .option("checkpoint", "checkpoint") \
        .load() \
        .select(from_json(col("value").cast("string"), schema, jsonOptions).alias("table_tpc"))


    stream_table_col = (stream_table
    .select(
        col("table_tpc.SalesTerritoryKey").alias("SalesTerritoryKey"),
        col("table_tpc.SalesTerritoryAlternateKey").alias("SalesTerritoryAlternateKey"),
        col("table_tpc.SalesTerritoryRegion").alias("SalesTerritoryRegion"),
        col("table_tpc.SalesTerritoryCountry").alias("SalesTerritoryCountry"),
        col("table_tpc.SalesTerritoryGroup").alias("SalesTerritoryGroup"),
        col("table_tpc.SalesTerritoryImage").alias("SalesTerritoryImage"),
    )
    )

    dimsalesterritory_df = spark.read.jdbc(settings.YUGABYTEDB_JDBC, destination_table,
        properties={"user": settings.YUGABYTEDB_USER, "password": settings.YUGABYTEDB_PSWD}).load()

    current_df = (
        dimsalesterritory_df.alias("pg")
        .join(stream_table_col.alias("kfk"),on=[col("pg.SalesTerritoryKey")==col("kfk.SalesTerritoryKey")],how="left")
    )
    current_df = current_df.where((col("pg.SalesTerritoryKey").isNotNull()) & (col("kfk.SalesTerritoryKey").isNull()))
    current_df = current_df.select(
        col("pg.SalesTerritoryKey").alias("SalesTerritoryKey"),
        col("pg.SalesTerritoryAlternateKey").alias("SalesTerritoryAlternateKey"),
        col("pg.SalesTerritoryRegion").alias("SalesTerritoryRegion"),
        col("pg.SalesTerritoryCountry").alias("SalesTerritoryCountry"),
        col("pg.SalesTerritoryGroup").alias("SalesTerritoryGroup"),
        col("pg.SalesTerritoryImage").alias("SalesTerritoryImage"),
    )

    update_df = (
        dimsalesterritory_df.alias("pg")
        .join(stream_table_col.alias("kfk"),on=[col("pg.SalesTerritoryKey")==col("kfk.SalesTerritoryKey")],how="inner")
    )
    update_df = update_df.select(
        col("kfk.SalesTerritoryKey").alias("SalesTerritoryKey"),
        col("kfk.SalesTerritoryAlternateKey").alias("SalesTerritoryAlternateKey"),
        col("kfk.SalesTerritoryRegion").alias("SalesTerritoryRegion"),
        col("kfk.SalesTerritoryCountry").alias("SalesTerritoryCountry"),
        col("kfk.SalesTerritoryGroup").alias("SalesTerritoryGroup"),
        col("kfk.SalesTerritoryImage").alias("SalesTerritoryImage"),
    )

    insert_df = (
        stream_table_col.alias("kfk")
        .join(dimsalesterritory_df.alias("pg"),on=[col("pg.SalesTerritoryKey")==col("kfk.SalesTerritoryKey")],how="left")
    )
    insert_df = insert_df.where((col("kfk.SalesTerritoryKey").isNotNull()) & (col("pg.SalesTerritoryKey").isNull()))
    insert_df = insert_df.select(
        col("kfk.SalesTerritoryKey").alias("SalesTerritoryKey"),
        col("kfk.SalesTerritoryAlternateKey").alias("SalesTerritoryAlternateKey"),
        col("kfk.SalesTerritoryRegion").alias("SalesTerritoryRegion"),
        col("kfk.SalesTerritoryCountry").alias("SalesTerritoryCountry"),
        col("kfk.SalesTerritoryGroup").alias("SalesTerritoryGroup"),
        col("kfk.SalesTerritoryImage").alias("SalesTerritoryImage"),
    )

    aux_df = current_df.union(update_df)
    final_df = aux_df.union(insert_df)

    final_df.write \
    .jdbc(settings.YUGABYTEDB_JDBC, destination_table, mode="append", truncate="true",
          properties={"user": settings.YUGABYTEDB_USER, "password": settings.YUGABYTEDB_PSWD}).insertInto(destination_table)

    # save into gold
    gold_table = spark.createDataFrame(final_df.rdd,schema=schemadimsalesterritory)

    # write to gold
    if DeltaTable.isDeltaTable(spark, destination_folder):
        dt_table = DeltaTable.forPath(spark, destination_folder)
        dt_table.alias("historical_data")\
            .merge(
                gold_table.alias("new_data"),
                '''
                historical_data.SalesTerritoryKey = new_data.SalesTerritoryKey 
                ''')\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()
    else:
        gold_table.write\
            .mode(write_delta_mode)\
            .format("delta")\
            .save(destination_folder)


    spark.stop()