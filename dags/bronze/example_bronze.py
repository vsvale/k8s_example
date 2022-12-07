# imports
from datetime import datetime, timedelta
from airflow.decorators import dag,task_group
from airflow.utils.dates import days_ago
from os import getenv
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.providers.cncf.kubernetes.operators.spark_kubernetes import SparkKubernetesOperator
from airflow.providers.cncf.kubernetes.sensors.spark_kubernetes import SparkKubernetesSensor
from airflow.providers.amazon.aws.operators.s3 import S3ListOperator

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
    'max_active_run': 1}

description = "DAG to convert lading to delta and save it in lakehouse bronze"

@dag(schedule='@daily', default_args=default_args,catchup=False,
tags=['example','spark','bronze','s3','sensor','k8s'],description=description)

def example_bronze():
    @task_group()
    def customer_bronze():
        # verify if new data has arrived on landing bucket
        verify_customer_landing = S3KeySensor(
        task_id='t_verify_customer_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-customer/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_customer_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_customer_spark_operator',
        namespace='processing',
        application_file='example-customer-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_customer_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_customer_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='customer_bronze.t_bronze_customer_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_customer_folder = S3ListOperator(
        task_id='t_list_bronze_example_customer_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/customer',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_customer_landing >> bronze_customer_spark_operator >> monitor_bronze_customer_spark_operator >> list_bronze_example_customer_folder
    
    @task_group()
    def address_bronze():
        # verify if new data has arrived on landing bucket
        verify_address_landing = S3KeySensor(
        task_id='t_verify_address_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-address/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_address_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_address_spark_operator',
        namespace='processing',
        application_file='example-address-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_address_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_address_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='address_bronze.t_bronze_address_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_address_folder = S3ListOperator(
        task_id='t_list_bronze_example_address_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/address',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_address_landing >> bronze_address_spark_operator >> monitor_bronze_address_spark_operator >> list_bronze_example_address_folder

    @task_group()
    def customeraddress_bronze():
        # verify if new data has arrived on landing bucket
        verify_customeraddress_landing = S3KeySensor(
        task_id='t_verify_customeraddress_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-customeraddress/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_customeraddress_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_customeraddress_spark_operator',
        namespace='processing',
        application_file='example-customeraddress-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_customeraddress_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_customeraddress_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='customeraddress_bronze.t_bronze_customeraddress_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_customeraddress_folder = S3ListOperator(
        task_id='t_list_bronze_example_customeraddress_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/customeraddress',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_customeraddress_landing >> bronze_customeraddress_spark_operator >> monitor_bronze_customeraddress_spark_operator >> list_bronze_example_customeraddress_folder
    
    @task_group()
    def salesorderheader_bronze():
        # verify if new data has arrived on landing bucket
        verify_salesorderheader_landing = S3KeySensor(
        task_id='t_verify_salesorderheader_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-salesorderheader/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_salesorderheader_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_salesorderheader_spark_operator',
        namespace='processing',
        application_file='example-salesorderheader-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_salesorderheader_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_salesorderheader_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='salesorderheader_bronze.t_bronze_salesorderheader_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_salesorderheader_folder = S3ListOperator(
        task_id='t_list_bronze_example_salesorderheader_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/salesorderheader',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_salesorderheader_landing >> bronze_salesorderheader_spark_operator >> monitor_bronze_salesorderheader_spark_operator >> list_bronze_example_salesorderheader_folder

    @task_group()
    def productcategory_bronze():
        # verify if new data has arrived on landing bucket
        verify_productcategory_landing = S3KeySensor(
        task_id='t_verify_productcategory_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-productcategory/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_productcategory_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_productcategory_spark_operator',
        namespace='processing',
        application_file='example-productcategory-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_productcategory_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_productcategory_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='productcategory_bronze.t_bronze_productcategory_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_productcategory_folder = S3ListOperator(
        task_id='t_list_bronze_example_productcategory_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/productcategory',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_productcategory_landing >> bronze_productcategory_spark_operator >> monitor_bronze_productcategory_spark_operator >> list_bronze_example_productcategory_folder

    @task_group()
    def productmodel_bronze():
        # verify if new data has arrived on landing bucket
        verify_productmodel_landing = S3KeySensor(
        task_id='t_verify_productmodel_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-productmodel/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_productmodel_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_productmodel_spark_operator',
        namespace='processing',
        application_file='example-productmodel-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_productmodel_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_productmodel_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='productmodel_bronze.t_bronze_productmodel_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_productmodel_folder = S3ListOperator(
        task_id='t_list_bronze_example_productmodel_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/productmodel',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_productmodel_landing >> bronze_productmodel_spark_operator >> monitor_bronze_productmodel_spark_operator >> list_bronze_example_productmodel_folder

    @task_group()
    def productdescription_bronze():
        # verify if new data has arrived on landing bucket
        verify_productdescription_landing = S3KeySensor(
        task_id='t_verify_productdescription_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-productdescription/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_productdescription_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_productdescription_spark_operator',
        namespace='processing',
        application_file='example-productdescription-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_productdescription_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_productdescription_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='productdescription_bronze.t_bronze_productdescription_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_productdescription_folder = S3ListOperator(
        task_id='t_list_bronze_example_productdescription_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/productdescription',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_productdescription_landing >> bronze_productdescription_spark_operator >> monitor_bronze_productdescription_spark_operator >> list_bronze_example_productdescription_folder

    @task_group()
    def productmodelproductdescription_bronze():
        # verify if new data has arrived on landing bucket
        verify_productmodelproductdescription_landing = S3KeySensor(
        task_id='t_verify_productmodelproductdescription_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-productmodelproductdescription/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_productmodelproductdescription_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_productmodelproductdescription_spark_operator',
        namespace='processing',
        application_file='example-productmodelproductdescription-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_productmodelproductdescription_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_productmodelproductdescription_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='productmodelproductdescription_bronze.t_bronze_productmodelproductdescription_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_productmodelproductdescription_folder = S3ListOperator(
        task_id='t_list_bronze_example_productmodelproductdescription_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/productmodelproductdescription',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_productmodelproductdescription_landing >> bronze_productmodelproductdescription_spark_operator >> monitor_bronze_productmodelproductdescription_spark_operator >> list_bronze_example_productmodelproductdescription_folder

    @task_group()
    def product_bronze():
        # verify if new data has arrived on landing bucket
        verify_product_landing = S3KeySensor(
        task_id='t_verify_product_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-product/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_product_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_product_spark_operator',
        namespace='processing',
        application_file='example-product-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_product_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_product_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='product_bronze.t_bronze_product_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_product_folder = S3ListOperator(
        task_id='t_list_bronze_example_product_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/product',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_product_landing >> bronze_product_spark_operator >> monitor_bronze_product_spark_operator >> list_bronze_example_product_folder

    @task_group()
    def salesorderdetail_bronze():
        # verify if new data has arrived on landing bucket
        verify_salesorderdetail_landing = S3KeySensor(
        task_id='t_verify_salesorderdetail_landing',
        bucket_name=LANDING_ZONE,
        bucket_key='example/src-example-salesorderdetail/*/*.parquet',
        wildcard_match=True,
        timeout=18 * 60 * 60,
        poke_interval=120,
        aws_conn_id='minio')

        # use spark-on-k8s to operate against the data
        bronze_salesorderdetail_spark_operator = SparkKubernetesOperator(
        task_id='t_bronze_salesorderdetail_spark_operator',
        namespace='processing',
        application_file='example-salesorderdetail-bronze.yaml',
        kubernetes_conn_id='kubeconnect',
        do_xcom_push=True)

        # monitor spark application using sensor to determine the outcome of the task
        monitor_bronze_salesorderdetail_spark_operator = SparkKubernetesSensor(
        task_id='t_monitor_bronze_salesorderdetail_spark_operator',
        namespace="processing",
        application_name="{{ task_instance.xcom_pull(task_ids='salesorderdetail_bronze.t_bronze_salesorderdetail_spark_operator')['metadata']['name'] }}",
        kubernetes_conn_id="kubeconnect")

        # Confirm files are created
        list_bronze_example_salesorderdetail_folder = S3ListOperator(
        task_id='t_list_bronze_example_salesorderdetail_folder',
        bucket=LAKEHOUSE,
        prefix='bronze/example/salesorderdetail',
        delimiter='/',
        aws_conn_id='minio',
        do_xcom_push=True)    

        verify_salesorderdetail_landing >> bronze_salesorderdetail_spark_operator >> monitor_bronze_salesorderdetail_spark_operator >> list_bronze_example_salesorderdetail_folder

    
    bronze1 = [customer_bronze(),address_bronze()] >> customeraddress_bronze() >> salesorderheader_bronze()
    bronze2 = [productcategory_bronze(),productmodel_bronze(), productdescription_bronze()] >> productmodelproductdescription_bronze() >> product_bronze()
    [bronze1, bronze2] >> salesorderdetail_bronze()
    
dag = example_bronze()