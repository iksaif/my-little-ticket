FROM ubuntu:latest

RUN apt-get update && \
	apt-get install -y python3 python3-dev python3-pip && \
	apt-get clean

ENV ROOT=/opt/mlt

RUN mkdir $ROOT
WORKDIR $ROOT

ADD requirements.txt $ROOT/
RUN pip3 install -r requirements.txt gunicorn

RUN mkdir static storage
VOLUME ["$ROOT/storage/", "$ROOT/static/"]

ADD . $ROOT/
RUN pip3 install -e $ROOT/

EXPOSE 8000

COPY ./examples/start.sh .
ENTRYPOINT ["./start.sh"]
