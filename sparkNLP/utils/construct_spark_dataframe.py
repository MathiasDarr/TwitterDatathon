import os
import boto3
from sparkNLP.utils.sparkSession import getSparkInstance

def download_parquet_files(index, days):
    '''
    This function downloads parquet files from the specified topic & specified date range

    index: Select the index/topic from which to download the data.  e.g biden or trump.
    days: List of days in format MMDD so 1028 -> October 28th.

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

# download_parquet_files('trump',[1028])



def create_tweets_dataframe(index):

    '''
    This function constructs a spark dataframe with the locally downloaded parquet files (downloaded from the download_parquet_files)
    and the index from which to construct the dataframe.

    I will want to extend this to allow the creation of a dataframe with multiple idices/topics but will have to be cognizant of
    the fact that there may be duplicates if I join data from multiple indices.
    '''

    spark = getSparkInstance()
    parquet_files = []
    directory = 'tmp/{}'.format(index)
    for folder in os.listdir(directory):
        for file in os.listdir('{}/{}/'.format('tmp/{}'.format(index),folder)):
            parquet_files.append('tmp/{}/{}/{}'.format(index, folder, file))

    # for file in os.listdir('tmp/'+folder):
    #         parquet_files.append('tmp/{}/{}'.format(folder,file))
    dataframes = []
    for file in parquet_files:
        df = spark.read.parquet(file)
        dataframes.append(df)

    df = dataframes[0]
    for dataf in dataframes[1:]:
        df = df.union(dataf)
    return df

def create_datafram_from_parquet(directory):
    spark = getSparkInstance()
    parquet_files = []
    for file in os.listdir(directory):
        parquet_files.append('{}/{}'.format(directory, file))
    dataframes = []
    for file in parquet_files:
        df = spark.read.parquet(file)
        dataframes.append(df)

    df = dataframes[0]
    for dataf in dataframes[1:]:
        df = df.union(dataf)
    return df

df = create_datafram_from_parquet('data')

