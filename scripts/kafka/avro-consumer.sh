#!/bin/bash
confluent local consume $1 -- --value-format avro --from-beginning --property print.key=true

docker exec -t broker  \
  kafka-console-consumer.sh \
    --bootstrap-server :9092 \
    --topic tweets
