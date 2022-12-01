# import libraries
import settings
from pyspark.sql.functions import *
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from schemas import schemadimdate

# main spark program
if __name__ == '__main__':

    # init spark session
    spark = SparkSession \
            .builder \
            .appName("example-dimcdate-silver") \
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
    schema = schemadimdate
    input_topic = "dimdate_spark_stream_dwfiles"
    destination_folder = "s3a://lakehouse/silver/example/dimdate/"
    write_delta_mode = "overwrite"
    destination_table = "public.dimdate"
    jsonOptions = {"timestampFormat": "yyyy-MM-dd'T'HH:mm:ss.sss'Z'"}

    # reading data from apache kafka
    # stream operation mode
    # latest offset recorded on kafka and spark
    stream_table= spark \
        .read\
        .format("kafka") \
        .option("kafka.bootstrap.servers", settings.BOOTSTRAP_SERVERS) \
        .option("subscribe", input_topic) \
        .option("startingOffsets", "earliest") \
        .option("checkpoint", "checkpoint") \
        .load() \
        .select(from_json(col("value").cast("string"), schema, jsonOptions).alias("table_tpc"))

    stream_table = (stream_table
    .select(
        col('table_tpc.DateKey').alias('DateKey'),
        col('table_tpc.FullDateAlternateKey').alias('FullDateAlternateKey'),
        col('table_tpc.DayNumberOfWeek').alias('DayNumberOfWeek'),
        col('table_tpc.EnglishDayNameOfWeek').alias('EnglishDayNameOfWeek'),
        col('table_tpc.SpanishDayNameOfWeek').alias('SpanishDayNameOfWeek'),
        col('table_tpc.FrenchDayNameOfWeek').alias('FrenchDayNameOfWeek'),
        col('table_tpc.DayNumberOfMonth').alias('DayNumberOfMonth'),
        col('table_tpc.DayNumberOfYear').alias('DayNumberOfYear'),
        col('table_tpc.WeekNumberOfYear').alias('WeekNumberOfYear'),
        col('table_tpc.EnglishMonthName').alias('EnglishMonthName'),
        col('table_tpc.SpanishMonthName').alias('SpanishMonthName'),
        col('table_tpc.FrenchMonthName').alias('FrenchMonthName'),
        col('table_tpc.MonthNumberOfYear').alias('MonthNumberOfYear'),
        col('table_tpc.CalendarQuarter').alias('CalendarQuarter'),
        col('table_tpc.CalendarYear').alias('CalendarYear'),
        col('table_tpc.CalendarSemester').alias('CalendarSemester'),
        col('table_tpc.FiscalQuarter').alias('FiscalQuarter'),
        col('table_tpc.FiscalYear').alias('FiscalYear'),
        col('table_tpc.FiscalSemester').alias('FiscalSemester')
    )
    )

    silver_table = spark.createDataFrame(stream_table.rdd,schema=schemadimdate)

    # write to silver
    if DeltaTable.isDeltaTable(spark, destination_folder):
        dt_table = DeltaTable.forPath(spark, destination_folder)
        dt_table.alias("historical_data")\
            .merge(
                silver_table.alias("new_data"),
                '''
                historical_data.DateKey = new_data.DateKey 
                ''')\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()
    else:
        silver_table.write\
            .mode(write_delta_mode)\
            .format("delta")\
            .save(destination_folder)

    #verify count origin vs destination
    origin_count = stream_table.count()

    destiny = spark.read \
        .format("delta") \
        .load(destination_folder)
    
    destiny_count = destiny.count()

    print("origin",origin_count)
    print("destiny",destiny_count)

    if origin_count != destiny_count:
        raise AssertionError("Counts of origin and destiny are not equal")

    spark.stop()