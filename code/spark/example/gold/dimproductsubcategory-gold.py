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
            .appName("example-dimproductsubcategory-gold") \
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
    origin_folder = "s3a://lakehouse/silver/example/dimproductsubcategory/"
    destination_table = "public.dimproductsubcategory"
    jsonOptions = {"timestampFormat": "yyyy-MM-dd'T'HH:mm:ss.sss'Z'"}
    destination_folder = "s3a://lakehouse/gold/example/dimproductsubcategory/"
    write_delta_mode = "overwrite"

    # read from destination
    dest_table_df = spark.read.jdbc(settings.YUGABYTEDB_JDBC, destination_table,
        properties={"user": settings.YUGABYTEDB_USER, "password": settings.YUGABYTEDB_PSWD})

    dest_table_df = spark.createDataFrame(dest_table_df.rdd,schema=schemadimproductsubcategory)

    # write to gold
    if DeltaTable.isDeltaTable(spark, destination_folder):
        dt_table = DeltaTable.forPath(spark, destination_folder)
        dt_table.alias("historical_data")\
            .merge(
                dest_table_df.alias("new_data"),
                '''
                historical_data.ProductSubcategoryKey = new_data.ProductSubcategoryKey 
                ''')\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()

    # reading from silver

    silver_df = spark.read.format("delta").load(origin_folder).distinct()

    silver_df = spark.createDataFrame(silver_df.rdd,schema=schemadimproductsubcategory)

    # write to gold
    if DeltaTable.isDeltaTable(spark, destination_folder):
        dt_table = DeltaTable.forPath(spark, destination_folder)
        dt_table.alias("historical_data")\
            .merge(
                silver_df.alias("new_data"),
                '''
                historical_data.ProductSubcategoryKey = new_data.ProductSubcategoryKey 
                ''')\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()
    else:
        silver_df.write\
            .mode(write_delta_mode)\
            .format("delta")\
            .save(destination_folder)


    final_df = spark.read.format("delta").load(destination_folder).distinct()
    
    print(final_df.show())

    final_df.write \
    .jdbc(settings.YUGABYTEDB_JDBC, destination_table, mode="overwrite",
          properties={"user": settings.YUGABYTEDB_USER, "password": settings.YUGABYTEDB_PSWD, "truncate":"true"})

    spark.stop()