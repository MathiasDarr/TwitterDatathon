# Twitter election 2020 datapipeline & analysis  #

### This repository contains a data pipeline & analysis of twitter data pertaining to the 2020 presidential election ###

### This project consists of ###

* Data Pipeline
    - Multithreaded java application that pushes twitter data steamed from the twitter4j library into 
        - individual kafka topics for each keyword provided at run time
        - elasticsearch indices
    - Airflow DAG
        - Every hour query the elastic-search indices & save data to S3 as parquet files.
        - delete data from the index (save disk space) 
    - Kafka connect elasticsearch sink connectors to move data directly into elasticsearch into kafka (these aren't currently working and I'm not sure what changed?) 
    
#####    TODO:    #####
    - The kafka connect elasticsearch sink isn't working properly, this would be preferable than pushing to ES directly from the twitter-producer java application (there
    are parsing errors at the moment due to unescaped protected characters resulting in not all of the data reaching elastic search.) 

* NLP analysis
    - Utility functions for constructing spark dataframes over a range of dates & topics.  
    - Use spark.ml library to define Transformers & Pipeline for feature engineering
        - Use the stop words provided by nltk to identify the language of the tweet based upon ratios of stop words present in the tweet content
        - Define a transformer for parsing the users location string.  The geolocation field for the majority of tweets is null, therefore the only method of determining the location of the user who sends the tweet is to parse the location string into something meaningful.  Attempt to assign each tweet a city & state (limited to the United States for the time being).    
    - Sentiment Analysis 
    
#####  TODO: #####
    - Extend the language identification to support more languages
    - Make use of the spark ML Pipelines API
    - KMeans model
    - Sentiment analysis 
    - Apply a spark streaming model which uses kafka as an input data source
    - The Spark job should run on EMR
    - Airflow DAG for generating a model every hour or every day.  

* Tweets Query API 
    - API developed using Spring Boot (and/or Flask) for querying the elasticsearch tweet data based upon query parmaeterrs such as
        location, filter keywords)
#####  TODO: #####
    - Decouple the API from the pipeline.  Shoulden't take too long
    - Create a flask application and define a few routes making using of the python elasticsearch client        



### How do I get set up? ###
This project has the following dependencies
* docker & docker-compose
* maven (If you want to compile the java code)
* airflow
    - pip install apache-airflow
* spark 2.4
* nltk
    
### How do I run the pipeline ? ### 
* Start zookeeper, schema registry,  kafka broker & elastic search
    - cd twitter-producer
    - docker-compose up --build
* Run the java application
    - mvn clean package (compile with maven)
    - java -jar twitter-producer/target/twitter-producer-1.0-SNAPSHOT.jar http://localhost:9092 http://localhost:8081 localhost 29200 virus trump biden
* Run the airflow DAG
    - airflow initdb (only required the first time )
    - airflow webserver -p 8080
    - airflow scheduler
    - cp tweets_dag.py $HOME/airflow/dags/tweets_dag.py (Copy the DAG file into the airflow DAGs folder)
    - the pipeline can be run from the airflow web client, however I am certain there is a method of doing this from the CLI.

#### TODO ####
* modify the script to allow a caller to pass a sentance or tweet lengthed input text to the script instead of the hardcoded text 
    
    
## Reproduction of analysis ##
#### Generate the dataset #### 
* Unzip the provided dataset into a 'data' folder in the root directory
* Run the script to generate a Spark dataframe & save to data to parquet.  
    - python3 create_dataframe_from_supplied_data.py 
    - dataframe can be loaded from parquet as demonstrated in the load_dataframe_from_parquet.py file. 
* Transform the data 
    - the dataframe_transformations.py script demonstrates how to use the spark.ml Pipeline to perform transformations 
    - python3 dataframe_transformations.py
    
### How do I perform the Sentiment Analysis?    ###
* Download Stanford CoreNLP
    - https://stanfordnlp.github.io/CoreNLP/download.html  
* Run the CoreNLP server
    - unzip the download, cd to the stanford-corenlp-x.x.x directory 
    -  java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
            -preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
            -status_port 9000 -port 9000 -timeout 15000 &  
* Run the sample script demonstrating dependency parsing using the nltk CoreNLPDependencyParser 
    - python3 sentiment_analysis/nltk_sentimenet_analysis.py


   - Ensure that spark 2.4 is installed on your machine
   - In order to create 
   - Download Stanford CoreNLP
        - https://stanfordnlp.github.io/CoreNLP/download.html  
   - Run the CoreNLP server
        - unzip the download, cd to the stanford-corenlp-x.x.x directory 
        - run 
        java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
            -preload tokenize,ssplit,pos,lemma,ner,parse,depparse \
            -status_port 9000 -port 9000 -timeout 15000 &  
### Spark relies on Java 8 so if you have Java 11 set as your current java version you can switch between them as follows  ### 
* update-java-alternatives --list
* sudo update-java-alternatives --set /path_to_java_version