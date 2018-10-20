FROM python:3

ENV PYTHONUNBUFFERED 1
ENV ROOT=/opt/mlt

RUN mkdir $ROOT
WORKDIR $ROOT

RUN mkdir static storage
VOLUME ["$ROOT/storage/", "$ROOT/static/"]

ADD requirements.txt $ROOT/
RUN pip install -r requirements.txt gunicorn

ADD . $ROOT/
RUN pip install -e $ROOT/

EXPOSE 8000

COPY ./examples/start.sh .
ENTRYPOINT ["./start.sh"]
