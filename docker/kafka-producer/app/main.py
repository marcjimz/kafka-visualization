# importing required modules
import argparse
import json
import logging
from time import sleep

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

# create a parser object
parser = argparse.ArgumentParser(description = "Kafka client to product messages")
  
# add argument
parser.add_argument("--bootstrap-servers", help = "Commma-separated list of the Kafka broker servers", required=True)
parser.add_argument("--data-files", help = "Location on disk of data that is to be uploaded into the kafka topic, comma separated", required=True)
parser.add_argument("--upload-delay", help = "Speed in seconds of a delay between each file entry of the file", default=60, required=False)
parser.add_argument("--initial-delay", help = "Speed in seconds of a delay before the upload", default=5, required=False)
parser.add_argument("--topic", help = "Kafka topic to upload to", required=True)

# parse the arguments from standard input
args = parser.parse_args()
print(args)

if args.bootstrap_servers:
    bootstrap_servers=args.bootstrap_servers
if args.data_files:
    data_files = args.data_files.split(',')
if args.upload_delay:
    delay = int(args.upload_delay)
if args.topic:
    topic = args.topic
if args.initial_delay:
    initial_delay = int(args.initial_delay)
else:
    data_key = None
  
from confluent_kafka import Producer, KafkaError
from confluent_kafka.admin import AdminClient, NewTopic

import socket

conf = {'bootstrap.servers': bootstrap_servers,
        'client.id': socket.gethostname()}

logging.debug("Conf: %s" % conf)


# sleep as required in anticipation of bootup.
print("Sleeping...")
sleep(initial_delay)

producer = Producer(conf)
adminClient = AdminClient(conf)

# attempt to create topic if it doesn't already exist
newTopic = NewTopic(
         topic,
         num_partitions=1,
         replication_factor=1
    )

fs = adminClient.create_topics([newTopic])
for topic, f in fs.items():
    try:
        f.result()  # The result itself is None
        print("Topic {} created".format(topic))
    except Exception as e:
        # Continue if error code TOPIC_ALREADY_EXISTS, which may be true
        # Otherwise fail fast
        if e.args[0].code() != KafkaError.TOPIC_ALREADY_EXISTS:
            print("Failed to create topic {}: {}".format(topic, e))

print("Now processing files...")
sleep(5)

for file in data_files:
    print("Processing file")
    with open(file, 'r') as input:
        data = json.loads(input.read())
    key = None


    # We understand the data is in this format given a key, so we iterate and split:
    
    records = []
    for devices in data['all_data']:
        spotterId = devices['data']['spotterId']
        for waves in devices['data']['waves']:
            waves['spotterId'] = spotterId
            records.append(waves)

    print("Processing %s # of records..." % str(len(data)))
    for input in records:
        producer.produce(topic, key=input['spotterId'], value=json.dumps(input), on_delivery=acked)
        producer.poll(1)

# Wait up to 1 second for events. Callbacks will be invoked during
# this method call if the message is acknowledged.