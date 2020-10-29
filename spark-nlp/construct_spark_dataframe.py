import findspark
findspark.init()
import pyspark as ps
import os
import boto3


def getSparkInstance():
    java8_location= '/usr/lib/jvm/java-8-openjdk-amd64' # Set your own
    os.environ['JAVA_HOME'] = java8_location
    spark = ps.sql.SparkSession.builder \
        .master("local[4]") \
        .appName("individual") \
        .getOrCreate()
    return spark

if not os.path.exists('tmp/silly/how'):
    os.makedirs('tmp/silly/how')


def download_parquet_files(index, days):
    '''
    This function downloads parquet files from the specified topic & specified date range
    :return:
    '''
    s3 = boto3.resource('s3')
    bucket = 'datathon-election-tweets'
    tweets_bucket = s3.Bucket(bucket)
    tweet_parquet_files = [file.key for file in list(tweets_bucket.objects.filter(Prefix='{}/'.format(index)).all()) if file.key.split('.')[-1]=='parquet']
    client = boto3.client('s3')

    for file in tweet_parquet_files:
        day = file.split('/')[1]
        hour = file.split('/')[2][:2]

        folder = 'tmp/{}/{}/{}'.format(index,day,hour)

        if not os.path.exists(folder):
            os.makedirs(folder)
        for day in days:
            client.download_file(bucket, file, '{}/{}.parquet'.format(folder, day, hour))

download_parquet_files('trump',[1028])



def create_tweets_dataframe():
    spark = getSparkInstance()

    parquet_files = []
    for folder in os.listdir('tmp'):
        for file in os.listdir('tmp/'+folder):
            parquet_files.append('tmp/{}/{}'.format(folder,file))

    dataframes = []
    for file in parquet_files:
        df = spark.read.parquet(file)
        dataframes.append(df)

    df = dataframes[0]
    for dataf in dataframes[1:]:
        df = df.union(dataf)
    return df