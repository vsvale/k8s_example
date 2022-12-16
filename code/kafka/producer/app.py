import os
import sys
import argparse
from dotenv import load_dotenv
from schema  import schema_customer
from producer import CustomerAvro
from object.dimcustomer import Customers

# get env
load_dotenv()

# load variables
get_dt_rows = 2
kafka_broker = "edh-kafka-bootstrap.ingestion.svc.cluster.local:9092"
schema_registry_server = "http://schema-registry-cp-schema-registry:8081"
kafka_topic_users_avro = "dimcustomer_producer_avro"

# init variables
users_object_name = Customers().get_multiple_rows(get_dt_rows)

# full schema
schema_key = schema_customer.key
schema_value = schema_customer.value

# producer avro all columns
CustomerAvro().avro_producer(kafka_broker, schema_registry_server, schema_key, schema_value, kafka_topic_users_avro, get_dt_rows)