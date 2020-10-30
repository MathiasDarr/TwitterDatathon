from airflow import DAG
from datetime import datetime, timedelta
from airflow.models import BaseOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from elasticsearch import Elasticsearch, helpers, exceptions
import logging
import boto3

import findspark

findspark.init()
import pyspark as ps
import os

BUCKET = "datathon-election-tweets"


def getSparkInstance():
    java8_location = '/usr/lib/jvm/java-8-openjdk-amd64'  # Set your own
    os.environ['JAVA_HOME'] = java8_location

    spark = ps.sql.SparkSession.builder \
        .master("local[4]") \
        .appName("individual") \
        .getOrCreate()
    return spark


def scan_tweets_index(index):
    host = "localhost:29200"
    client = Elasticsearch(host)
    search_body = {
        "size": 10000,
        "query": {
            "match_all": {}
        }
    }
    resp = client.search(
        index=index,
        body=search_body,
        scroll='3m',  # time value for search
    )
    scroll_id = resp['_scroll_id']
    resp = client.scroll(
        scroll_id=scroll_id,
        scroll='1s',  # time value for search
    )
    resp = helpers.scan(
        client,
        scroll='3m',
        size=10,
    )
    return list(resp)


def deleteElasticSearchTweets():
    host = "localhost:29200"
    es = Elasticsearch(host)
    es.delete_by_query(index="tweets", body={"query": {"match_all": {}}})


def generate_directory_name_infer_time(index):
    current_time = datetime.now()
    # hour = '0' + str(current_time.hour) if current_time.hour < 10 else current_time.hour
    day = '0' + str(current_time.day) if current_time.day < 10 else current_time.day
    month = '0' + str(current_time.month) if current_time.month < 10 else current_time.month
    return 'tmp/{}/{}{}/'.format(index, month, day)


def generate_directory_name_supply(index, day, month):
    return 'tmp/{}/{}{}'.format(index, month, day)


def scanElasticSearchTweets():
    tweets_scan = scan_tweets_index('biden')
    biden_tweets = [tweet['_source'] for tweet in tweets_scan]

    tweets_scan = scan_tweets_index('trump')
    trump_tweets = [tweet['_source'] for tweet in tweets_scan]

    spark = getSparkInstance()
    sc = spark.sparkContext

    dataframe = spark.read.json(sc.parallelize(biden_tweets))
    directory_name = generate_directory_name_infer_time('biden')
    upload_dataframe_to_s3(dataframe, directory_name)

    dataframe = spark.read.json(sc.parallelize(trump_tweets))
    directory_name = generate_directory_name_infer_time('trump')
    upload_dataframe_to_s3(dataframe, directory_name)


def upload_dataframe_to_s3(dataframe, directory_name):
    s3 = boto3.client('s3')
    dataframe.repartition(1).write.mode('overwrite').parquet(directory_name)
    for root, dirs, files in os.walk(directory_name):
        parquet_files = [file for file in files if file.split('.')[-1] == 'parquet']
        for file in parquet_files:
            s3.upload_file(os.path.join(root, file), BUCKET, directory_name[4:] + file)


# scanElasticSearchTweets('trump')


default_args = {
    'owner': 'mddarr',
    'start_date': datetime(2020, 3, 1),
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'email_on_retry': False
}

tweets_pipeline_dag = DAG('tweets',
                          default_args=default_args,
                          description='Airflow DAG',
                          schedule_interval='0 * * * *',
                          catchup=False
                          )

scan_tweets_task = PythonOperator(
    task_id='scan_elastic_tweets',
    dag=tweets_pipeline_dag,
    python_callable=scanElasticSearchTweets,
)



delete_tweets_task = PythonOperator(
    task_id='delete_elastic_tweets',
    dag=tweets_pipeline_dag,
    python_callable=deleteElasticSearchTweets,
)

delete_tmp_directory = BashOperator(
    task_id='delete_directory',
    dag=tweets_pipeline_dag,
    bash_command='rm -rf tmp/',
)

scan_tweets_task >> delete_tweets_task >> delete_tmp_directory
