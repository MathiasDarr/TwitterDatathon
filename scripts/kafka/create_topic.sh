#! /bin/bash
/home/mddarr/libraries/confluent-5.2.1/bin/kafka-topics.sh --create \
    --zookeeper zookeeper:2181 \
    --topic tweets \
    --partitions 3 \
    --replication-factor 1



docker exec kafka bash /kafka/bin/kafka-topics.sh --create --bootstrap-server \
localhost:9092 --replication-factor 1 --partitions 1 --topic users