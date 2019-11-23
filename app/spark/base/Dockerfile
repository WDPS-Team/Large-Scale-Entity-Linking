FROM openjdk:8
ENV DAEMON_RUN=true
ENV SPARK_VERSION=2.4.4
ENV HADOOP_VERSION=2.7
ENV SCALA_VERSION=2.12.4
ENV SCALA_HOME=/usr/share/scala
ENV PYSPARK_PYTHON=python3

RUN apt-get update
RUN apt-get install wget tar bash

RUN wget -q http://apache.mirror.anlx.net/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN apt-get install -y python3 python3-venv

RUN apt install -y python3-pip
ADD requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
