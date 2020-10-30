#!/bin/bash

docker-compose exec broker kafka-topics --create --bootstrap-server \
localhost:9092 --replication-factor 1 --partitions 1 --topic users

docker exec kafka kafka-topics --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 1 --topic tweets
docker exec -it kafka kafka-console-producer --topic=tweets --bootstrap-server localhost:9092
docker exec -it kafka kafka-console-consumer --topic=tweets --bootstrap-server localhost:9092


docker exec broker kafka-topics  --list --bootstrap-server localhost:9092

docker exec -it kafka  --topic=test

kafka-console-producer.sh --topic=test \
--broker-list=`broker-list.sh`
>> Hello World!
>> I'm a Producer writing to 'hello-topic'

