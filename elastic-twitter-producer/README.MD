## Dakobed Twitter Kafka & ElasticSearch Pipeline

Multithreaded Java application that streams tweets using twitter4j library in one thread, and produces to a Kafka topic in the other thread.  

Also Includes a Kafka connect connector for pushing the data into Elastic Search

#### Run the twitter pipeline locally
mvn clean package 


docker-compose -f tweets-compose.yaml up --build

#### Consume the tweets with kafka console consumer
docker exec kafka bash bin/kafka-console-consumer.sh --topic kafka-tweets --from-beginning --property print.key=true --bootstrap-server kafka:9092


#### Register the connector
 
curl -i -X POST -H "Accept:application/json" -H  "Content-Type:application/json" http://localhost:8083/connectors/ -d @dakobed-twitter-producer/connectors/es_sink.json


#### Verify that the tweets have been sinked to ES

bash scripts/elasticsearch/query.sh kafka-tweets



#### Build the docker image seperatly ..
docker build . -t dakobed:dakobed-twitter-producer


