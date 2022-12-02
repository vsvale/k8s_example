# import libraries
import settings
from pyspark.sql.functions import *
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from schemas import schemadimcustomer
# main spark program
# init application
if __name__ == '__main__':

    # init session
    # set configs
    spark = SparkSession \
        .builder \
        .appName("example-dimcustomer-silver-py") \
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

    # set log level
    spark.sparkContext.setLogLevel("INFO")

    # variables
    customer_bronze = "s3a://lakehouse/bronze/example/customer/"
    address_bronze = "s3a://lakehouse/bronze/example/address/"
    customeraddress_bronze = "s3a://lakehouse/bronze/example/customeraddress/"

    destination_folder = "s3a://lakehouse/silver/example/dimcustomer/"
    write_delta_mode = "overwrite"
    # read bronze data

    customer_df = spark.read.format("delta").load(customer_bronze)
    customer_df = customer_df.alias("c")
    address_df = spark.read.format("delta").load(address_bronze)
    address_df = address_df.alias("a")
    customeraddress_df = spark.read.format("delta").load(customeraddress_bronze)
    customeraddress_df = customeraddress_df.alias("ca")

    silver_table = (
        customer_df
        .join(customeraddress_df, col("c.CustomerID")==col("ca.CustomerID"),"left")
        .join(address_df,col("a.AddressID")==col("ca.AddressID"),"left")
        .select(
            col("c.CustomerID").alias("CustomerKey"),
            col("a.AddressID").alias("GeographKey"),
            col("c.rowguid").alias("CustomerAlternateKey"),
            col("c.Title").alias("Title"),
            col("c.FirstName").alias("FirstName"),
            col("c.MiddleName").alias("MiddleName"),
            col("c.LastName").alias("LastName"),
            when(col("c.NameStyle")==lit(0),lit(False)).otherwise(lit(True)).alias("NameStyle"),
            lit(None).alias('BirthDate'),
            lit(None).alias('MaritalStatus'),
            col("c.Suffix").alias("Suffix"),
            when(col("c.Title").isin(["Sr.","Mr."]),"M").when(col("c.Title").isin(["Sra.","Ms."]),"F").otherwise(lit(None)).alias("Gender"),
            col("c.EmailAddress").alias("EmailAddress"),
            lit(None).alias("YearlyIncome"),
            lit(None).alias("TotalChildren"),
            lit(None).alias("NumberChildrenAtHome"),
            lit(None).alias("EnglishEducation"),
            lit(None).alias("SpanishEducation"),
            lit(None).alias("FrenchEducation"),
            lit(None).alias("EnglishOccupation"),
            lit(None).alias("SpanishOccupation"),
            lit(None).alias("FrenchOccupation"),
            lit(None).alias("HouseOwnerFlag"),
            lit(None).alias("NumberCarsOwned"),
            col("a.AddressLine1").alias("AddressLine1"),
            col("a.AddressLine2").alias("AddressLine2"),
            col("c.Phone").alias("Phone"),
            lit(None).alias("DateFirstPurchase"),
            lit(None).alias("CommuteDistance")
    )
    )

    silver_table = spark.createDataFrame(silver_table.rdd,schema=schemadimcustomer)

    # write to silver
    if DeltaTable.isDeltaTable(spark, destination_folder):
        dt_table = DeltaTable.forPath(spark, destination_folder)
        dt_table.alias("historical_data")\
            .merge(
                silver_table.alias("new_data"),
                '''
                historical_data.CustomerKey = new_data.CustomerKey 
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