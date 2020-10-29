#! /bin/bash
docker exec -t kafka bin/kafka-topics.sh \
    --bootstrap-server kafka:9092 \
    --list
