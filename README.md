# Kafka Visualization

This is a repository to highlight the simplicity of deploying your own Kafka cluster, as well as your own Apache Druid and Apache Superset, to highlight the combination of streaming and visualization capabilities that are possible.

## Table of Contents

- [Background](#background)
- [Install](#install)
	- [Deploy the Services](#deploy)
- [Usage](#usage)
- [Contributing](#contributing)

## Background

Kafka, Druid and Superset as a combination allows for visualizations on top of queryable data streams. Connecting the components allow for strong visualizations that can help drive business insights. The usage of this repository is to deploy the three tech components using Docker-compose, and have them auto-configured such that you can simply use Apache Superset to view visualizations.

Scroll down to the usage section below to deploy the server components and load up the data and visualizations of this repository.

## Prerequisites

* Docker version 1.11 or later is installed and running.
* Docker Compose is installed. Docker Compose is installed by default with Docker for Mac and Docker for Windows.
* Internet connectivity
* Networking and Kafka on Docker
* Install curl (optional)

## Install

Please ensure you have all of the pre-requisites. If you are unable to run Docker on your machine with network connectivity, you will run into issues on these commands. These commands have been tested against Ubuntu on WSL2 and EC2.

### Deploy the Services

This step requires you to leverage docker-compose, similarly:

```
docker-compose -f docker/docker-compose.yml up -d
```

You will see a number of pull requests happening against the docker registries; this will take several minutes to complete. You can validate the install when running the command and seeing all of the services in the **Up** state:

```
docker-compose -f docker/docker-compose.yml ps
```

You will also require the docker image to product Kafka messages. Run this command to build it:

```
cd docker/kafka-producer
docker build . -t kafka-producer
```

### Configuring the Kafka Topics

1. Follow the instructions highlighted @ [Confluent](https://docs.confluent.io/platform/current/quickstart/ce-docker-quickstart.html?utm_medium=sem&utm_source=google&utm_campaign=ch.sem_br.brand_tp.prs_tgt.confluent-brand_mt.xct_rgn.namer_lng.eng_dv.all_con.confluent-docker&utm_term=confluent%20kafka%20docker&creative=&device=c&placement=&gclid=Cj0KCQiA4b2MBhD2ARIsAIrcB-R6KLxJrrHSPWOdIz5B107UqyDB79ovSCa9i9nG_gx-dLByGnnFsGEaApN8EALw_wcB#step-2-create-ak-topics-for-storing-your-data)
2. Use the same instructions to create a topic for **ocean-data**


## Usage

To load data into the Kafka topics, as well as create the Kafka topics, configure and run the following command:

```
docker run -e BOOTSTRAP_SERVERS="localhost:9092,localhost:9101" -e DATA_FILES="data/day1.json" -e UPLOAD_DELAY=5 -e KAFKA_TOPIC="ocean_data" -e SPLITTING_KEY="all_data" -e DATA_KEY="data.spotterId" --network="host" kafka-producer    
```

## Cleanup

```
docker-compose -f docker/docker-compose.yml down -v
```

### Contributors

This project exists thanks to all the people who contribute. 
<a href="https://github.com/RichardLitt/standard-readme/graphs/contributors"><img src="https://opencollective.com/standard-readme/contributors.svg?width=890&button=false" /></a>

