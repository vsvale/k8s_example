### Create base image
- docker pull gcr.io/spark-operator/spark-py:v3.1.1-hadoop3
- docker build ./processing/spark/base_image -t vsvale/spark_base_image:3.1.1
- docker login
- docker push vsvale/spark_base_image:3.1.1