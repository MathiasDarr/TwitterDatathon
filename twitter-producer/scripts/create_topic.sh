#! /bin/bash


docker exec kafka bash /kafka/bin/kafka-topics.sh --create --bootstrap-server \
localhost:9092 --replication-factor 1 --partitions 1 --topic simple.elasticsearch.data
