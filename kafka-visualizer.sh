#!/bin/sh
#
# Usage as follows:
#
# ./kafka-visualizer.sh <setup> - Does the necessary builds as required
# ./kafka-visualizer.sh <start> - Starts the service
# ./kafka-visualizer.sh <stop> - Stops the service and removes all state
# ./kafka-visualizer.sh <status> - Returns the status
# ./kafka-visualizer.sh <upload> <file location> - Runs a docker container to upload the data to the kafka topic requested
action=$1
file=$2

if [ "$action" = "setup" ]; then
    echo "Starting Kafka-Visualizer via Docker-compose..."
    #docker-compose -f docker/docker-compose.yml build
    docker build -f docker/kafka-producer/Dockerfile docker/kafka-producer -t kafka-producer
fi

if [ "$action" = "start" ]; then
    echo "Starting Kafka-Visualizer via Docker-compose..."
    docker-compose -f docker/docker-compose.yml up -d
fi

if [ "$action" = "stop" ]; then
    echo "Stopping and removing all of the volumes for Kafka-Visualizer."
    docker-compose -f docker/docker-compose.yml down -v
fi

if [ "$action" = "upload" ]; then
    echo "Uploading the dataset to Apache Kafka."
    docker run -e BOOTSTRAP_SERVERS="broker:9092,broker:9101" -e DATA_FILES="$file" -e UPLOAD_DELAY=5 -e KAFKA_TOPIC="ocean_data" -e SPLITTING_KEY="all_data" -e DATA_KEY="data.spotterId" -e INITIAL_DELAY=1 --network="kafka-visualizer" kafka-producer 
fi

if [ "$action" = "status" ]; then
    docker-compose -f docker/docker-compose.yml ps
fi

echo "Finished!"