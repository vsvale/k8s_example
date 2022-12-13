# imports
from datetime import datetime, timedelta
from airflow.decorators import dag,task_group,task
from airflow.utils.dates import days_ago
from os import getenv
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from astronomer.providers.amazon.aws.sensors.s3 import S3KeySensorAsync
from astro import sql as aql
from astro.files import File
from astro.constants import FileType
from astro.sql.table import Table, Metadata
import sqlalchemy
from pandas import DataFrame

LANDING_ZONE = getenv("LANDING_ZONE", "landing")
LAKEHOUSE = getenv("LAKEHOUSE", "lakehouse")

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
tags=['example','spark','gold','s3','sensor','k8s','YugabyteDB','astrosdk'],description=description)
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
    def factinternetsalesreason_gold():
        sensor_landing_example_salesreason = S3KeySensor(
        task_id='t_sensor_landing_example_salesreason',
        bucket_name=LANDING_ZONE,
        bucket_key='example/dw-files/internetsalesreason/*',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        loads_s3_to_yugabytedb = aql.load_file(
        task_id="t_loads_salesreason_s3_to_yugabytedb",
        input_file=File(
            path="s3://landing/example/dw-files/internetsalesreason/factinternetsalesreason.csv",
            filetype=FileType.CSV,
            conn_id='minio'),
        output_table=Table(
            name="factinternetsalesreason",
            conn_id='yugabytedb_ysql',
            columns=[
                sqlalchemy.Column("SalesOrderNumber", sqlalchemy.String(20), nullable=False, key="SalesOrderNumber"),
                sqlalchemy.Column("SalesOrderLineNumber", sqlalchemy.Integer, nullable=False, key="SalesOrderLineNumber"),
                sqlalchemy.Column("SalesReasonKey", sqlalchemy.Integer, nullable=False, key="SalesReasonKey")
            ],
            metadata=Metadata(schema="public",database="salesdw")
        
        ),
        if_exists="replace",
        use_native_support=True,
        columns_names_capitalization="original",
        )
       
        
        sensor_landing_example_salesreason >> loads_s3_to_yugabytedb

    @task_group()
    def dimpromotion_gold():
        sensor_landing_example_promotion = S3KeySensor(
        task_id='t_sensor_landing_example_promotion',
        bucket_name=LANDING_ZONE,
        bucket_key='example/dw-files/promotion/*',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        loads_s3_to_temp = aql.load_file(
        task_id="t_loads_promotion_s3_to_temp",
        input_file=File(
            path="s3://landing/example/dw-files/promotion/",
            filetype=FileType.CSV,
            conn_id='minio'),
        output_table=Table(
            name="promotion_csv",
            conn_id='yugabytedb_ysql',
            columns=[
                sqlalchemy.Column("promotionkey", sqlalchemy.Integer, nullable=False, primary_key=True),
                sqlalchemy.Column("promotionalternatekey", sqlalchemy.Integer, nullable=False, key="promotionalternatekey"),
                sqlalchemy.Column("englishpromotionname", sqlalchemy.String(255), nullable=False, key="englishpromotionname"),
                sqlalchemy.Column("spanishpromotionname", sqlalchemy.String(255), nullable=False, key="spanishpromotionname"),
                sqlalchemy.Column("frenchpromotionname", sqlalchemy.String(255), nullable=False, key="frenchpromotionname"),
                sqlalchemy.Column("discountpct", sqlalchemy.Float, nullable=False, key="discountpct"),
                sqlalchemy.Column("englishpromotiontype", sqlalchemy.String(50), nullable=False, key="englishpromotiontype"),
                sqlalchemy.Column("spanishpromotiontype", sqlalchemy.String(50), nullable=False, key="spanishpromotiontype"),
                sqlalchemy.Column("frenchpromotiontype", sqlalchemy.String(50), nullable=False, key="frenchpromotiontype"),
                sqlalchemy.Column("englishpromotioncategory", sqlalchemy.String(50), nullable=False, key="englishpromotioncategory"),
                sqlalchemy.Column("spanishpromotioncategory", sqlalchemy.String(50), nullable=False, key="spanishpromotioncategory"),
                sqlalchemy.Column("frenchpromotioncategory", sqlalchemy.String(50), nullable=False, key="frenchpromotioncategory"),
                sqlalchemy.Column("startdate", sqlalchemy.TIMESTAMP, nullable=False, key="startdate"),
                sqlalchemy.Column("enddate", sqlalchemy.TIMESTAMP, nullable=False, key="enddate"),
                sqlalchemy.Column("minqty", sqlalchemy.Integer, nullable=False, key="minqty"),
                sqlalchemy.Column("maxqty", sqlalchemy.Integer, nullable=False, key="maxqty")
            ],
            metadata=Metadata(schema="public",database="salesdw")
        
        ),
        if_exists="replace",
        use_native_support=True,
        columns_names_capitalization="original"
        )

        load_to_yugabytedb = aql.merge(
            target_table=Table(
                name="dimpromotion",
                conn_id='yugabytedb_ysql',
                metadata=Metadata(schema="public",database="salesdw")
            ),
            source_table=loads_s3_to_temp,
            target_conflict_columns=["promotionkey"],
            columns={
                "promotionkey":"promotionkey",
                "promotionalternatekey":"promotionalternatekey",
                "englishpromotionname":"englishpromotionname",
                "spanishpromotionname":"spanishpromotionname",
                "frenchpromotionname":"frenchpromotionname",
                "discountpct":"discountpct",
                "englishpromotiontype":"englishpromotiontype",
                "spanishpromotiontype":"spanishpromotiontype",
                "frenchpromotiontype":"frenchpromotiontype",
                "englishpromotioncategory":"englishpromotioncategory",
                "spanishpromotioncategory":"spanishpromotioncategory",
                "frenchpromotioncategory":"frenchpromotioncategory",
                "startdate":"startdate",
                "enddate":"enddate",
                "minqty":"minqty",
                "maxqty":"maxqty"
            },
            if_conflicts="update",
        )

        truncate_results = aql.drop_table(table=Table(name="promotion_csv", conn_id="yugabytedb_ysql"))

        sensor_landing_example_promotion >> loads_s3_to_temp >> load_to_yugabytedb >> truncate_results
    [dimsalesterritory_gold()]
    dimpromotion_gold() >> factinternetsalesreason_gold()
    dimproductcategory_gold() >> dimproductsubcategory_gold()
dag = example_gold()