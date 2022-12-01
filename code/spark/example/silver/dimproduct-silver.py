# import libraries
import settings
from delta.tables import DeltaTable
from pyspark.sql import SparkSession
from pyspark import SparkConf
from pyspark.sql.functions import col, lit, when
from schemas import schemadimproduct

# main spark program
# init application
if __name__ == '__main__':

    # init session
    # set configs
    spark = SparkSession \
        .builder \
        .appName("example-dimproduct-silver-py") \
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
    bronze_table = "s3a://lakehouse/bronze/example/product/"
    silver_subcategory = "s3a://lakehouse/silver/example/dimproductsubcategory/"
    bronze_category = "s3a://lakehouse/bronze/example/productcategory/"
    bronze_model = "s3a://lakehouse/bronze/example/productmodel/"
    bronze_modelproductdescription = "s3a://lakehouse/bronze/example/productmodelproductdescription/"
    bronze_productdescription = "s3a://lakehouse/bronze/example/productdescription/"
    destination_folder = "s3a://lakehouse/silver/example/dimproduct/"
    write_delta_mode = "overwrite"

    # read bronze data
    bronze_df = spark.read.format("delta").load(bronze_table)
    bronze_df = bronze_df.alias("b")
    subcat_df = spark.read.format("delta").load(silver_subcategory)
    subcat_df = subcat_df.alias("sc")
    bronze_cat = spark.read.format("delta").load(bronze_category)
    bronze_cat = bronze_cat.alias("c")
    bronze_mod = spark.read.format("delta").load(bronze_model)
    bronze_mod = bronze_mod.alias("m")
    bronze_moddesc = spark.read.format("delta").load(bronze_modelproductdescription)
    bronze_moddesc = bronze_moddesc.alias("md")
    bronze_desc = spark.read.format("delta").load(bronze_productdescription)
    bronze_desc = bronze_desc.alias("d")

    silver_table = (
        bronze_df
        .join(subcat_df,on=[col("b.ProductSubcategoryKey")==col("sc.ProductSubcategoryKey")],how="left")
        .join(bronze_cat,on=[col("b.ProductCategoryID")==col("c.ProductCategoryID")],how="left")
        .join(bronze_mod,on=[col("b.ProductModelID")==col("m.ProductModelID")],how="left")
        .join(bronze_moddesc,on=[(col("m.ProductModelID")==col("md.ProductModelID")) & (col("md.Culture")==lit("en"))],how="left")
        .join(bronze_desc,on=[(col("d.ProductDescriptioniD")==col("md.ProductDescriptionID"))],how="left")
        .select(
            col('b.ProductID').alias('ProductKey'),
            col('b.ProductNumber').alias('ProductAlternateKey'),
            col('sc.ProductSubcategoryKey').alias('ProductSubcategoryKey'),
            lit(None).alias('WeightUnitMeasureCode'),
            lit(None).alias('SizeUnitMeasureCode'),
            col('b.Name').alias('EnglishProductName'),
            lit(None).alias('SpanishProductName'),
            lit(None).alias('FrenchProductName'),
            col('b.StandardCost').alias('StandardCost'),
            lit(None).alias('FinishedGoodsFlag'),
            col('b.Color').alias('Color'),
            lit(None).alias('SafetyStockLevel'),
            lit(None).alias('ReorderPoint'),
            col('b.ListPrice').alias('ListPrice'),
            col('b.Size').alias('Size'),
            lit(None).alias('SizeRange'),
            col('b.Weight').alias('Weight'),
            lit(None).alias('DaysToManufacture'),
            col('c.Name').alias('ProductLine'),
            col('b.ListPrice').alias('DealerPrice'),
            lit(None).alias('Class'),
            lit(None).alias('Style'),
            col('m.Name').alias('ModelName'),
            col('b.ThumbnailPhoto').alias('LargePhoto'),
            col('d.Description').alias('EnglishDescription'),
            lit(None).alias('FrenchDescription'),
            lit(None).alias('ChineseDescription'),
            lit(None).alias('ArabicDescription'),
            lit(None).alias('HebrewDescription'),
            lit(None).alias('ThaiDescription'),
            lit(None).alias('GermanDescription'),
            lit(None).alias('JapaneseDescription'),
            lit(None).alias('TurkishDescription'),
            col('b.SellStartDate').alias('StartDate'),
            col('b.SellEndDate').alias('EndDate'),
            when(col("b.DiscontinuedDate").isNull(),lit(True)).otherwise(lit(False)).alias("Status"),
        )   
    )

    silver_table = spark.createDataFrame(silver_table.rdd,schema=schemadimproduct)

   
    if DeltaTable.isDeltaTable(spark, destination_folder):
        dt_table = DeltaTable.forPath(spark, destination_folder)
        dt_table.alias("historical_data")\
            .merge(
                silver_table.alias("new_data"),
                '''
                historical_data.ProductKey = new_data.ProductKey 
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