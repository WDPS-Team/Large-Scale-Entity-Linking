FROM wdps_spark_base:v1

RUN apt update
RUN apt install -y zip
RUN apt install -y python3-pip
RUN python3 -m spacy download en_core_web_sm
CMD bash