FROM gcr.io/spark-operator/spark-py:v3.1.1-hadoop3

# using root user
USER root:root

# create directory for apps
RUN mkdir -p /app

# copy requirements
COPY requirements.txt .

# pip install
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy jar files
COPY /jars /opt/spark/jars

# set work directory
WORKDIR /app

# user
USER 1001