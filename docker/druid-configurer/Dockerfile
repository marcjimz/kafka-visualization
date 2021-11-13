FROM docker pull curlimages/curl

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    && apk add --no-cache librdkafka-dev


COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

COPY data/ data/
COPY app/ app/

ENTRYPOINT ["sh", "-c", "python app/main.py --bootstrap-servers $BOOTSTRAP_SERVERS --data-files $DATA_FILES --upload-delay $UPLOAD_DELAY --topic $KAFKA_TOPIC --splitting-key $SPLITTING_KEY --data-key $DATA_KEY"]
