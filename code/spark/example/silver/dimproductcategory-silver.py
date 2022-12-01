# import libraries
import settings
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import current_timestamp, current_date, col, lit, when
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, TimestampType, DateType
from schemas import schemaproductcategory
# main spark program
# init application
if __name__ == '__main__':

    # init session
    # set configs
    spark = SparkSession \
        .builder \
        .appName("example-dimproductcategory-silver-py") \
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
        .getOrCreate()

    # show configured parameters
    print(SparkConf().getAll())

    # set log level
    spark.sparkContext.setLogLevel("INFO")

    # variables
    bronze_table = "s3a://lakehouse/bronze/example/productcategory/"
    destination_folder = "s3a://lakehouse/silver/example/dimproductcategory/"
    write_delta_mode = "overwrite"
    # read bronze data

    bronze_df = spark.read.format("delta").load(bronze_table)
    bronze_df = bronze_df.alias("b")


    silver_table = (
        bronze_df
        .select(
            col("b.ProductCategoryID").alias("ProductCategoryKey"),
            col("b.ProductCategoryID").alias("ProductCategoryAlternateKey"),
            col("b.name").alias("EnglishProductCategoryName"),
            lit(None).alias("SpanishProductCategoryName"),
            lit(None).alias("FrenchProductCategoryName")
    )
    )

    silver_table = spark.createDataFrame(silver_table.rdd,schema=schemaproductcategory)

    # write to silver   
    if DeltaTable.isDeltaTable(spark, destination_folder):
        dt_table = DeltaTable.forPath(spark, destination_folder)
        dt_table.alias("historical_data")\
            .merge(
                silver_table.alias("new_data"),
                '''
                historical_data.ProductCategoryKey = new_data.ProductCategoryKey 
                ''')\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()
    else:
        silver_table.write\
            .mode(write_delta_mode)\
            .format("delta")\
            .save(destination_folder)

    #verify count origin vs destination
    origin_count = silver_table.count()

    destiny = spark.read \
        .format("delta") \
        .load(destination_folder)
    
    destiny_count = destiny.count()

    if origin_count != destiny_count:
        raise AssertionError("Counts of origin and destiny are not equal")

    # stop session
    spark.stop()