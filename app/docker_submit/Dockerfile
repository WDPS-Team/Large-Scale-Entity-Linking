FROM openjdk:8
ENV DAEMON_RUN=true
ENV SPARK_VERSION=2.4.4
ENV HADOOP_VERSION=2.7
ENV SCALA_VERSION=2.12.4
ENV SCALA_HOME=/usr/share/scala

RUN apt-get update
RUN apt-get install wget tar bash

RUN wget -q http://apache.mirror.anlx.net/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN tar -xzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

RUN apt-get install -y python3 python3

ENV PYSPARK_PYTHON=python3

CMD bash

#FROM bde2020/spark-python-template:2.4.4-hadoop2.7
#
#RUN apk update
#RUN apk add make automake gcc g++ subversion python3-dev libxml2 libxml2-dev
## hotfix to install backend deps.
#RUN pip3 install spacy==2.2.2