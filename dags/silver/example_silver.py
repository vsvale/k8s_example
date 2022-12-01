# imports
from datetime import datetime, timedelta
from airflow.decorators import dag,task_group
from airflow.utils.dates import days_ago
from os import getenv
from airflow.providers.amazon.aws.sensors.s3_key import S3KeySensor
from airflow.providers.amazon.aws.operators.s3_delete_objects import S3DeleteObjectsOperator
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.providers.amazon.aws.operators.s3_list import S3ListOperator

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

description = "DAG to create dim and facts and save in silver"

@dag(schedule='@daily', default_args=default_args,catchup=False,
tags=['example','spark','silver','s3','sensor','k8s'],description=description)
def example_silver():
   
    @task_group()
    def dimcustomer_silver():
        # verify if new data has arrived on bronze bucket
        verify_customer_bronze = S3KeySensor(
        task_id='t_verify_customer_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='bronze/example/customer/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        verify_customeraddress_bronze = S3KeySensor(
        task_id='t_verify_customeraddress_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='bronze/example/customeraddress/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        verify_address_bronze = S3KeySensor(
        task_id='t_verify_address_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='bronze/example/address/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        silver_dimcustomer_spark_operator = SparkKubernetesOperator(
        task_id='t_silver_dimcustomer_spark_operator',
        namespace='processing',
        application_file='example-dimcustomer-silver.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_silver_dimcustomer_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_silver_dimcustomer_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='dimcustomer_silver.t_silver_dimcustomer_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_silver_example_dimcustomer_folder = S3ListOperator(
        task_id='t_list_silver_example_dimcustomer_folder',
        bucket=LAKEHOUSE,
        prefix='silver/example/dimcustomer',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        [verify_customer_bronze,verify_customeraddress_bronze,verify_address_bronze] >> silver_dimcustomer_spark_operator >> monitor_silver_dimcustomer_spark_operator >> list_silver_example_dimcustomer_folder

    @task_group()
    def dimcurrency_silver():
        # use spark-on-k8s to operate against the data
        silver_dimcurrency_spark_operator = SparkKubernetesOperator(
        task_id='t_silver_dimcurrency_spark_operator',
        namespace='processing',
        application_file='example-dimcurrency-silver.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_silver_dimcurrency_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_silver_dimcurrency_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='dimcurrency_silver.t_silver_dimcurrency_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_silver_example_dimcurrency_folder = S3ListOperator(
        task_id='t_list_silver_example_dimcurrency_folder',
        bucket=LAKEHOUSE,
        prefix='silver/example/dimcurrency',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)

        silver_dimcurrency_spark_operator >> monitor_silver_dimcurrency_spark_operator >> list_silver_example_dimcurrency_folder

    @task_group()
    def dimproductcategory_silver():
        # verify if new data has arrived on bronze bucket
        verify_productcategory_bronze = S3KeySensor(
        task_id='t_verify_productcategory_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='bronze/example/productcategory/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        silver_dimproductcategory_spark_operator = SparkKubernetesOperator(
        task_id='t_silver_dimproductcategory_spark_operator',
        namespace='processing',
        application_file='example-dimproductcategory-silver.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_silver_dimproductcategory_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_silver_dimproductcategory_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='dimproductcategory_silver.t_silver_dimproductcategory_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_silver_example_dimproductcategory_folder = S3ListOperator(
        task_id='t_list_silver_example_dimproductcategory_folder',
        bucket=LAKEHOUSE,
        prefix='silver/example/dimproductcategory',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_productcategory_bronze >> silver_dimproductcategory_spark_operator >> monitor_silver_dimproductcategory_spark_operator >> list_silver_example_dimproductcategory_folder

    @task_group()
    def dimproduct_silver():
        # verify if new data has arrived on bronze bucket
        verify_product_bronze = S3KeySensor(
        task_id='t_verify_product_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='bronze/example/product/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        verify_productsubcategory_bronze = S3KeySensor(
        task_id='t_verify_productsubcategory_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='silver/example/dimproductsubcategory/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        verify_productcategory_bronze = S3KeySensor(
        task_id='t_verify_productcategory_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='bronze/example/productcategory/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        verify_productmodel_bronze = S3KeySensor(
        task_id='t_verify_productmodel_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='bronze/example/productmodel/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')        

        verify_productmodelproductdescription_bronze = S3KeySensor(
        task_id='t_verify_productmodelproductdescription_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='bronze/example/productmodelproductdescription/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')    

        verify_productdescription_bronze = S3KeySensor(
        task_id='t_verify_productdescription_bronze',
        bucket_name=LAKEHOUSE,
        bucket_key='bronze/example/productdescription/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')    

        # use spark-on-k8s to operate against the data
        silver_dimproduct_spark_operator = SparkKubernetesOperator(
        task_id='t_silver_dimproduct_spark_operator',
        namespace='processing',
        application_file='example-dimproduct-silver.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_silver_dimproduct_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_silver_dimproduct_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='dimproduct_silver.t_silver_dimproduct_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_silver_example_dimproduct_folder = S3ListOperator(
        task_id='t_list_silver_example_dimproduct_folder',
        bucket=LAKEHOUSE,
        prefix='silver/example/dimproduct',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        [verify_product_bronze,verify_productsubcategory_bronze, verify_productcategory_bronze, verify_productmodel_bronze, verify_productmodelproductdescription_bronze, verify_productdescription_bronze] >> silver_dimproduct_spark_operator >> monitor_silver_dimproduct_spark_operator >> list_silver_example_dimproduct_folder

    @task_group()
    def dimdate_silver():
        # use spark-on-k8s to operate against the data
        silver_dimdate_spark_operator = SparkKubernetesOperator(
        task_id='t_silver_dimdate_spark_operator',
        namespace='processing',
        application_file='example-dimdate-silver.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_silver_dimdate_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_silver_dimdate_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='dimdate_silver.t_silver_dimdate_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_silver_example_dimdate_folder = S3ListOperator(
        task_id='t_list_silver_example_dimdate_folder',
        bucket=LAKEHOUSE,
        prefix='silver/example/dimdate',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)

        silver_dimdate_spark_operator >> monitor_silver_dimdate_spark_operator >> list_silver_example_dimdate_folder


    [dimcustomer_silver(),dimcurrency_silver(),dimdate_silver()]
    [dimproductcategory_silver() >> dimproduct_silver()]
    


dag = example_silver()