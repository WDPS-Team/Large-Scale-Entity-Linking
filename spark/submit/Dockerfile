FROM wdps_spark_base:v1

RUN apt update
RUN apt install -y zip
RUN apt install -y python3-pip
RUN pip3 install virtualenv
COPY log4j.properties /spark/conf/log4j.properties

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
CMD bash