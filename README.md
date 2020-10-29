# Twitter election 2020 datapipeline & analysis  #

### This repository contains a data pipeline & analysis of twitter data pertaining to the 2020 presedentail election ###

* Quick summary
* Version
* [Learn Markdown](https://bitbucket.org/tutorials/markdowndemo)

### How do I get set up? ###
This project has the following dependencies
* docker & docker-compose
* Install airflow
    - pip install apache-airflow
* spark 2.4


### This project consists of ###

* Data Pipeline
    - Multithreaded java application that pushes data into 
        - individual kafka topics for each keyword provided at run time
        - elasticsearch indices
    - Airflow DAG
        - Every hour query the elastic-search indices & save data to S3 as parquet files.
        - delete data from the index (save disk space) 

* Spark  NLP analysis

### How do I run the pipeline ? ### 
* Start zookeeper, schema registry,  kafka broker & elastic search
    - cd twitter-producer
    - docker-compose up --build
* Run the java application
    - java -jar twitter-producer/target/twitter-producer-1.0-SNAPSHOT.jar http://localhost:9092 http://localhost:8081 localhost 29200 virus trump biden
* Run the airflow DAG
    - airflow initdb (only required the first time )
    - airflow webserver -p 8080
    - airflow scheduler
    - cp tweets_dag.py $HOME/airflow/dags/tweets_dag.py (Copy the DAG file into the airflow DAGs folder)




update-java-alternatives --list
sudo update-java-alternatives --set /usr/lib/jvm/java-1.11.0-openjdk-amd64