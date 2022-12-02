# import libraries
import settings
from pyspark.sql.functions import *
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from schemas import schemadimgeography
from schemas import schemadimsalesterritory
from pyspark.ml.feature import StringIndexer

# main spark program
# init application
if __name__ == '__main__':

    # init session
    # set configs
    spark = SparkSession \
        .builder \
        .appName("example-dimgeography-silver-py") \
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

    address_bronze = "s3a://lakehouse/bronze/example/address/"
    dimsalesterritory = "public.dimsalesterritory"
    destination_folder = "s3a://lakehouse/silver/example/dimgeography/"
    write_delta_mode = "overwrite"
    # read bronze data


    address_df = spark.read.format("delta").load(address_bronze)
    indexer_statecode = StringIndexer(inputCol="StateProvince", outputCol="StateProvinceCode")
    address_df = indexer_statecode.fit(address_df).transform(address_df)
    address_df = address_df.alias("a")

    dimsalesterritory_df = spark.read.jdbc(settings.YUGABYTEDB_JDBC, dimsalesterritory,
        properties={"user": settings.YUGABYTEDB_USER, "password": settings.YUGABYTEDB_PSWD})

    dimsalesterritory_df = spark.createDataFrame(dimsalesterritory_df.rdd,schema=schemadimsalesterritory)

    silver_table = (
        address_df
        .join(dimsalesterritory_df.alias("st"), col("a.CountryRegion")==col("st.salesterritorycountry"),"left")
        .select(
            col("a.AddressID").alias("GeographyKey"),
            col("a.City").alias("City"),
            col("a.StateProvinceCode").alias("StateProvinceCode"),
            col("a.StateProvince").alias("StateProvinceName"),
            when(col("a.CountryRegion").isin("United States"),1).otherwise(col("st.SalesTerritoryKey")).alias("CountryRegionCode"),
            col("a.CountryRegion").alias("EnglishCountryRegionName"),
            lit(None).alias("SpanishCountryRegionName"),
            lit(None).alias("FrenchCountryRegionName"),
            col("a.PostalCode").alias("PostalCode"),
            when(col("a.CountryRegion").isin("United States"),1).otherwise(col("st.SalesTerritoryKey")).alias("SalesTerritoryKey"),
            lit(None).alias("IpAddressLocator")
    ).distinct()
    )

    silver_table = spark.createDataFrame(silver_table.rdd,schema=schemadimgeography)

    # write to silver
    if DeltaTable.isDeltaTable(spark, destination_folder):
        dt_table = DeltaTable.forPath(spark, destination_folder)
        dt_table.alias("historical_data")\
            .merge(
                silver_table.alias("new_data"),
                '''
                historical_data.GeographyKey = new_data.GeographyKey 
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