## Kafka tweets ElasticSearch pipeline

This repository contains a multithreaded java application which streams tweets using the Twitter4j library in one thread and
produces to a kafka topic with Avro serialization in another thread.  


To run the application

##### Compile the application  & run zookeeper, kafka broker, schema registry, kafka connect & ElasticSearch
mvn clean package 

docker-compose up 

##### Initialize the database

python3 LocationParser/pandasAlchemy.py 


#### Run the producer and give a command line argument on which to filter the tweets on
java -jar twitter-producer/target/twitter-producer-1.0-SNAPSHOT.jar virus      (The output to this is ugly, needs to get cleaned up)

#### Submit the ElasticSearch sink connector 


curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @scripts/connectors/es_sink.json

#### Verify that tweets are being sent to kafka topic w/ avro serialization (Using a wrapper script for the confluent local avro-consumer)  
bash scripts/avro-consumer.sh kafka-tweets

#### Query the ElasticSearch index to verify that tweets are arriving in ElasticSearch 
curl localhost:29200/kafka-tweets/_search | jq


#### If you do not have confluent kafka on your machine use the brokers console-consumer (does not support avro as far as I can tell)
docker exec kafka bash bin/kafka-console-consumer.sh --topic kafka-tweets --from-beginning --property print.key=true --bootstrap-server kafka:9092




curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @connectors/virus_sink.json

curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @connectors/virus_sink.json