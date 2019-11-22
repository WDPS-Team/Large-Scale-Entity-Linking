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

CMD /spark/bin/spark-class org.apache.spark.deploy.worker.Worker --webui-port 8080 spark://spark-master:7077

# -dev gcc gfortran freetype-dev musl-dev libpng-dev g++ lapack-dev
#RUN #RUN apt-get update
#RUN apt-get install scala=${SCALA_VERSION}
#RUN  wget http://scala-lang.org/files/archive/scala-.deb
#RUN dpkg -i scala-2.12.1.deb

#RUN apt-get install --no-cache --virtual=.build-dependencies wget ca-certificates && \
#    apk add --no-cache bash curl jq && \
#    cd "/tmp" && \
#    wget --no-verbose "https://downloads.typesafe.com/scala/${SCALA_VERSION}/scala-${SCALA_VERSION}.tgz" && \
#    tar xzf "scala-${SCALA_VERSION}.tgz" && \
#    mkdir "${SCALA_HOME}" && \
#    rm "/tmp/scala-${SCALA_VERSION}/bin/"*.bat && \
#    mv "/tmp/scala-${SCALA_VERSION}/bin" "/tmp/scala-${SCALA_VERSION}/lib" "${SCALA_HOME}" && \
#    ln -s "${SCALA_HOME}/bin/"* "/usr/bin/" && \
#    apk del .build-dependencies && \
#    rm -rf "/tmp/"*
#
##Scala instalation
#RUN export PATH="/usr/local/sbt/bin:$PATH" &&  apk update && apk add ca-certificates wget tar && mkdir -p "/usr/local/sbt" && wget -qO - --no-check-certificate "https://cocl.us/sbt-0.13.16.tgz" | tar xz -C /usr/local/sbt --strip-components=1 && sbt sbtVersion
#
#RUN apk add --no-cache python3
#
#RUN wget --no-verbose http://apache.mirror.iphh.net/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz && tar -xvzf spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz \
#      && mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} spark \
#      && rm spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz

# RUN pip3 install spacy==2.2.2