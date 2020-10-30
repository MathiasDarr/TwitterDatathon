# Twitter election 2020 datapipeline & analysis  #

### This repository contains a data pipeline & analysis of twitter data pertaining to the 2020 presidential election ###

### This project consists of ###

* Data Pipeline
    - Multithreaded java application that pushes twitter data into several destinations
        - Use the twitter4j library to stream tweets (requires twitter API keys)
            - http://twitter4j.org/en/
        - pushes data into 
            - individual kafka topics for each keyword provided at run time (uses avro serialization)
            - individual elasticsearch indices for each each keyword provided at run time
    
    - Airflow DAG
        - Use apache airflow to schedule workflows
        - Every hour
            - query the elastic-search indices & save data to S3 as parquet files.
            - delete data from the index (save disk space) 
        
    - Kafka connect connectors
        - elasticsearch sink connectors to move data directly into elasticsearch from kafka (these aren't currently working and I'm not sure what changed?) 
    - TODO     
        - The kafka connect elasticsearch sink isn't working properly, this would be preferable than pushing to ES directly from the twitter-producer java application (there
    are parsing errors at the moment due to unescaped protected characters resulting in not all of the data reaching elastic search.) 

* Spark NLP analysis
    - Sentiment Analysis with nltk & Stanford CoreNLP
        - Make use of dependency parsing to assign each subject identified in a tweet (could be presidential candidates) a sentiment score  
    
    - Utility functions for constructing spark dataframes over a range of dates & topics.  
    
    - Use spark.ml library to define Transformers & Pipeline for feature engineering
        - Use the stop words provided by nltk to identify the language of the tweet based upon ratios of stop words present in the tweet content
        - Define a transformer for parsing the users location string.  The geolocation field for the majority of tweets is null, therefore the only method of determining the location of the user who sends the tweet is to parse the location string into something meaningful.  Attempt to assign each tweet a city & state (limited to the United States for the time being).    
    - TODO
        - Extend the language identification to support more languages (currently supports english, spanish, french & italian)
        - KMeans model
        - Apply a spark streaming model which uses kafka as an input data source
        - The Spark job should run on EMR
        - Airflow DAG for generating a model every hour or every day.  
* Sentiment Ananlys data visualization
    - Map of united states with states colored according to the average sentiment for each candidate



### Running the twitter streaming pipeline  ### 
* The data pipeline has the following dependencies
    - docker
        - https://docs.docker.com/get-docker/
    - docker-compose
        - https://docs.docker.com/compose/install/
    - maven (If you want to compile the java code)
        - https://maven.apache.org/install.html 
    - airflow
        - pip install apache-airflow
    - boto3
        - pip install boto3
        - ensure aws credentials are correct.
        - Create a  
    - twitter API key
        - the twitter4j library requires a twitter API key
        - Set these environment variables on your computer.  The java application make use of these when configuring the client.  
            - export TWITTER_CONSUMER_KEY="your consumer key"
            - export TWITTER_CONSUMER_SECRET="your consumer secret"
            - export TWITTER_ACCESS_TOKEN="your access token"
            - export TWITTER_ACCESS_TOKEN_SECRET="your access token secret"

* Start zookeeper, schema registry,  kafka broker & elastic search
    - cd twitter-producer
    - docker-compose up --build
    
* Run the java application 
    - mvn clean package (compile with maven)
    - java -jar twitter-producer/target/twitter-producer-1.0-SNAPSHOT.jar http://localhost:9092 http://localhost:8081 localhost 29200 trump biden

* View the tweets coming into kafka
    - bash scripts/kafka/avro-consumer.sh trump
    - bash scripts/kafka/avro-consumer.sh biden
    
* View the tweets in elasticsearch
    - bash scripts/elasticsearch/queryES.sh trump
    - bash scripts/elasticsearch/queryES.sh biden
    
* Run the airflow DAG
    - airflow initdb (only required the first time )
    - run the airflow webserver 
        - airflow webserver -p 8080
    - run the airflow scheduler
        airflow scheduler
    - create an S3 bucket & edit the BUCKET variable at the top of dags/tweets_dag.py to the bucket just created
    - copy the airflow dag into the default airflow DAGs folder
        cp dags/tweets_dag.py $HOME/airflow/dags/tweets_dag.py (Copy the DAG file into the airflow DAGs folder)
    - the dag be triggered  from the airflow web client, however I am certain there is a method of doing this from the CLI.
    
* TODO
    - modify the script to allow a caller to pass a sentence or tweet lengthed input text to the script instead of the hardcoded text 
    
    
    
### How do I perform the NLP & Sentiment Analysis?    ###
* The spark NLP analysis performed in this repository has the following dependencies
    - Spark 2.4.6
    - Stanford CoreNLP
        - https://stanfordnlp.github.io/CoreNLP/download.html
    - nltk
    - boto3
    - pandas
    - plotly
      
* Run the CoreNLP server
    - unzip the download, cd to the stanford-corenlp-x.x.x directory 
    -  java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
            -preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
            -status_port 9000 -port 9000 -timeout 15000 &

* Load raw data, create spark dataframe & save dataframe to parquet 
    - Unzip the provided dataset into a 'data' folder in the root directory  
    - python3 create_dataframe_from_supplied_data.py 
    - dataframe can be loaded from parquet as demonstrated in the load_dataframe_from_parquet.py file. 
    
* Transform the data & save transformed dataframe to parquet
    - the dataframe_transformations.py script demonstrates how to use the spark.ml Pipeline & Transforms to perform feature engineering
    - python3 dataframe_transformations.py
        - creates column of identified language (using nltk stop words)
        - generates sentiment columns for subjects provided to the Transformer (for instance biden & trump)
        - parses the tweet users location string to assign tweet to a U.S state
        
* Run the sample script demonstrating dependency parsing using the nltk CoreNLPDependencyParser 
    - python3 sentiment_analysis/nltk_sentimenet_analysis.py

### Combining the provided data & the data received from the API ###
This project makes use of disparate data sources.  A demonstration of how to join the datasets into a single dataframe can be found in the join_dataframe.py file


### Plot the sentiment analysis ### 
* python3 plot_sentiment_analysis.py  (be patient this might take a secon)


### Spark relies on Java 8 so if you have Java 11 set as your current java version you can switch between them as follows  ### 
* update-java-alternatives --list
* sudo update-java-alternatives --set /path_to_java_version