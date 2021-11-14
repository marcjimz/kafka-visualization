FROM python:3.8.12-alpine

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    && apk add --no-cache librdkafka-dev

COPY data/ data/
COPY app/ app/
COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "-c", "python app/main.py --bootstrap-servers $BOOTSTRAP_SERVERS --data-files $DATA_FILES --upload-delay $UPLOAD_DELAY --topic $KAFKA_TOPIC --initial-delay $INITIAL_DELAY"]
