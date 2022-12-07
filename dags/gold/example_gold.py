# imports
from datetime import datetime, timedelta
from airflow.decorators import dag,task_group,task
from airflow.utils.dates import days_ago
from os import getenv
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.amazon.aws.operators.s3_delete_objects import S3DeleteObjectsOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.providers.amazon.aws.operators.s3_list import S3ListOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
import pandas as pd
from minio import Minio
from sqlalchemy import create_engine
from deltalake import DeltaTable

LANDING_ZONE = getenv("LANDING_ZONE", "landing")
LAKEHOUSE = getenv("LAKEHOUSE", "lakehouse")
MINIO = getenv("MINIO", "minio.deepstorage.svc.Cluster.local:8686")
ACCESS_KEY = getenv("ACCESS_KEY", "raat9cl2bEWhbgtQ")
SECRET_ACCESS = getenv("SECRET_ACCESS", "zcJWBrrGkInYEWXf4Oc37tCIdJVeA0fb")
YUGABYTEDB = getenv("YUGABYTEDB", "postgresql://plumber:PlumberSDE@yb-tservers.database.svc.Cluster.local:5433/salesdw")

default_args = {
    'owner': 'vinicius da silva vale',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'email': ['viniciusdvale@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'max_active_run': 1,
    'depends_on_past':False}

description = "DAG to create dim and facts and save in gold and YugabyteDB"

@dag(schedule='@daily', default_args=default_args,catchup=False,
tags=['example','spark','gold','s3','sensor','k8s','YugabyteDB','astrosdk','postgresoperator'],description=description)
def example_gold():
   
    @task_group()
    def dimsalesterritory_gold():
        # use spark-on-k8s to operate against the data
        gold_dimsalesterritory_spark_operator = SparkKubernetesOperator(
        task_id='t_gold_dimsalesterritory_spark_operator',
        namespace='processing',
        application_file='example-dimsalesterritory-gold.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_gold_dimsalesterritory_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_gold_dimsalesterritory_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='dimsalesterritory_gold.t_gold_dimsalesterritory_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_gold_example_dimsalesterritory_folder = S3ListOperator(
        task_id='t_list_gold_example_dimsalesterritory_folder',
        bucket=LAKEHOUSE,
        prefix='gold/example/dimsalesterritory',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)

        gold_dimsalesterritory_spark_operator >> monitor_gold_dimsalesterritory_spark_operator >> list_gold_example_dimsalesterritory_folder

    @task_group()
    def dimproductsubcategory_gold():
        # verify if new data has arrived on silver
        verify_dimproductsubcategory_silver = S3KeySensor(
        task_id='t_verify_dimproductsubcategory_silver',
        bucket_name=LAKEHOUSE,
        bucket_key='silver/example/dimproductsubcategory/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        gold_dimproductsubcategory_spark_operator = SparkKubernetesOperator(
        task_id='t_gold_dimproductsubcategory_spark_operator',
        namespace='processing',
        application_file='example-dimproductsubcategory-gold.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_gold_dimproductsubcategory_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_gold_dimproductsubcategory_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='dimproductsubcategory_gold.t_gold_dimproductsubcategory_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_gold_example_dimproductsubcategory_folder = S3ListOperator(
        task_id='t_list_gold_example_dimproductsubcategory_folder',
        bucket=LAKEHOUSE,
        prefix='gold/example/dimproductsubcategory',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)
        
        verify_dimproductsubcategory_silver >> gold_dimproductsubcategory_spark_operator >> monitor_gold_dimproductsubcategory_spark_operator >> list_gold_example_dimproductsubcategory_folder

    @task_group()
    def dimproductcategory_gold():
        # verify if new data has arrived on silver
        verify_dimproductcategory_silver = S3KeySensor(
        task_id='t_verify_dimproductcategory_silver',
        bucket_name=LAKEHOUSE,
        bucket_key='silver/example/dimproductcategory/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        gold_dimproductcategory_spark_operator = SparkKubernetesOperator(
        task_id='t_gold_dimproductcategory_spark_operator',
        namespace='processing',
        application_file='example-dimproductcategory-gold.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_gold_dimproductcategory_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_gold_dimproductcategory_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='dimproductcategory_gold.t_gold_dimproductcategory_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_gold_example_dimproductcategory_folder = S3ListOperator(
        task_id='t_list_gold_example_dimproductcategory_folder',
        bucket=LAKEHOUSE,
        prefix='gold/example/dimproductcategory',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)
        
        verify_dimproductcategory_silver >> gold_dimproductcategory_spark_operator >> monitor_gold_dimproductcategory_spark_operator >> list_gold_example_dimproductcategory_folder

    @task_group()
    def dimproduct_gold():
        # verify if new data has arrived on silver
        verify_dimproduct_silver = S3KeySensor(
        task_id='t_verify_dimproductcategory_silver',
        bucket_name=LAKEHOUSE,
        bucket_key='silver/example/dimproduct/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # list all files inside of a bucket
        list_silver_example_dimproduct_folder = S3ListOperator(
        task_id='t_list_silver_example_dimproduct_folder',
        bucket=LAKEHOUSE,
        prefix='silver/example/dimproduct',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)

        # delete files from gold zone [old file]
        delete_gold_example_dimproduct_folder = S3DeleteObjectsOperator(
        task_id='delete_s3_file_landing_zone',
        bucket=LAKEHOUSE,
        keys='gold/example/dimproduct',
        aws_conn_id='minio'
        )

        # delete table to perform full load
        drop_dimproduct_yugabytedb_tb = PostgresOperator(
        task_id='t_drop_dimproduct_yugabytedb_tb',
        postgres_conn_id='yugabytedb_ysql',
        sql=""" DROP TABLE IF EXISTS public.dimproduct; """)

        # create table on postgres [if not exists] = yugabytedb [ysql]
        create_dimproduct_yugabytedb_tb = PostgresOperator(
            task_id='t_create_dimproduct_yugabytedb_tb',
            postgres_conn_id='yugabytedb_ysql',
            sql="""
                CREATE TABLE DimProduct(
	            ProductKey int GENERATED BY DEFAULT AS IDENTITY(START WITH 1 INCREMENT BY 1) NOT NULL,
	            ProductAlternateKey Varchar(25) NULL,
	            ProductSubcategoryKey int NULL,
	            WeightUnitMeasureCode Char(3) NULL,
	            SizeUnitMeasureCode Char(3) NULL,
	            EnglishProductName Varchar(50) NOT NULL,
	            SpanishProductName Varchar(50) NOT NULL,
	            FrenchProductName Varchar(50) NOT NULL,
	            StandardCost money NULL,
	            FinishedGoodsFlag Boolean NOT NULL,
	            Color Varchar(15) NOT NULL,
	            SafetyStockLevel smallint NULL,
	            ReorderPoint smallint NULL,
	            ListPrice money NULL,
	            Size Varchar(50) NULL,
	            SizeRange Varchar(50) NULL,
	            Weight Double precision NULL,
	            DaysToManufacture int NULL,
	            ProductLine Char(2) NULL,
	            DealerPrice money NULL,
	            Class Char(2) NULL,
	            Style Char(2) NULL,
	            ModelName Varchar(50) NULL,
	            LargePhoto Bytea NULL,
	            EnglishDescription Varchar(400) NULL,
	            FrenchDescription Varchar(400) NULL,
	            ChineseDescription Varchar(400) NULL,
	            ArabicDescription Varchar(400) NULL,
	            HebrewDescription Varchar(400) NULL,
	            ThaiDescription Varchar(400) NULL,
	            GermanDescription Varchar(400) NULL,
	            JapaneseDescription Varchar(400) NULL,
	            TurkishDescription Varchar(400) NULL,
	            StartDate Timestamp(3) NULL,
	            EndDate Timestamp(3) NULL,
	            Status Varchar(7) NULL
                );""")
        
#        # use spark-on-k8s to operate against the data
#        gold_dimproduct_spark_operator = SparkKubernetesOperator(
#        task_id='t_gold_dimproduct_spark_operator',
#        namespace='processing',
#        application_file='example-dimproduct-gold.yaml',
#        kubernetes_conn_id='kubeconnect',
#        do_xcom_push=True)
#
#        # monitor spark application using sensor to determine the outcome of the task
#        monitor_gold_dimproduct_spark_operator = SparkKubernetesSensor(
#        task_id='t_monitor_gold_dimproduct_spark_operator',
#        namespace="processing",
#        application_name="{{ task_instance.xcom_pull(task_ids='dimproduct_gold.t_gold_dimproduct_spark_operator')['metadata']['name'] }}",
#        kubernetes_conn_id="kubeconnect")
#
#        # Confirm files are created
#        list_gold_example_dimproduct_folder = S3ListOperator(
#        task_id='t_list_gold_example_dimproduct_folder',
#        bucket=LAKEHOUSE,
#        prefix='gold/example/dimproduct',
#        delimiter='/',
#        aws_conn_id='minio',
#        do_xcom_push=True)

        @task
        def save_dimproduct_yugabytedb():
            client = Minio(MINIO, ACCESS_KEY, SECRET_ACCESS, secure=False)
            try:
                response = client.get_object(LAKEHOUSE,'gold/example/dimproduct/*.parquet')
            finally:
                response.close()
                response.release_conn()
            dt = DeltaTable(response)
            df = dt.to_pyarrow_table().to_pandas()
            postgres_engine = create_engine(YUGABYTEDB)
            df.to_sql('public.dimproduct', postgres_engine, if_exists='append', index=False, chunksize=100)

        verify_dimproduct_silver >> list_silver_example_dimproduct_folder >> [delete_gold_example_dimproduct_folder,drop_dimproduct_yugabytedb_tb] >> create_dimproduct_yugabytedb_tb >> save_dimproduct_yugabytedb()

    [dimsalesterritory_gold()]
    dimproductcategory_gold() >> dimproductsubcategory_gold() >> dimproduct_gold()
dag = example_gold()