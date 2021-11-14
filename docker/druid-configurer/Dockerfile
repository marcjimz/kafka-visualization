FROM curlimages/curl

COPY conf/supervisor-spec.json supervisor-spec.json

ENTRYPOINT ["sh", "-c", "sleep $INITIAL_DELAY && curl -X POST -H 'Content-Type: application/json' -d @supervisor-spec.json http://$DRUID_COORDINATOR_API/druid/indexer/v1/supervisor -i"]
