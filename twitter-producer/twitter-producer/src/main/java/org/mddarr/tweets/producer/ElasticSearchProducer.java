package org.mddarr.tweets.producer;

import org.apache.http.HttpHost;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.xcontent.XContentType;
import org.mddarr.avro.tweets.Tweet;
import org.mddarr.tweets.producer.model.TweetItem;

public class ElasticSearchProducer {
    private final String host;
    private final int port;
    private final String scheme;
    private final RestHighLevelClient client;
    public ElasticSearchProducer(AppConfig appConfig){
        host = appConfig.getElastic_search_host();
        port = appConfig.getElastic_search_port();
        if(this.host.equals("localhost")){
            scheme="http";
        }else{
            scheme="https";
        }
        RestHighLevelClient client = new RestHighLevelClient(RestClient.builder(new HttpHost("localhost", 29200, "http")));
        this.client = client;
//        this.client = new RestHighLevelClient(RestClient.builder(new HttpHost(this.host, this.port, scheme)));
    }

    private TweetItem avroTweetToTweetItem(Tweet tweet){
        TweetItem tweetItem = new TweetItem();
        tweetItem.setContent(tweet.getTweetContent());
        tweetItem.setDate(String.valueOf(tweet.getTweetTime()));
        tweetItem.setLocation(tweet.getLocation());
        tweetItem.setUsername(tweet.getScreename());
        return tweetItem;
    }

    public void postTweet(Tweet tweet, String topic){
        IndexRequest request = new IndexRequest(topic);
        TweetItem tweetItem = avroTweetToTweetItem(tweet);
        String jsonString = "{" +
                "\"username\":\"" +  tweetItem.getUsername()+"\"," +
                "\"content\":\"" +  tweetItem.getContent()+"\"," +
                "\"location\":\""  +  tweetItem.getLocation() +"\"," +
                "\"date\":\""  +  tweetItem.getDate() +"\""
                + "}";

        request.source(jsonString, XContentType.JSON);
        try {
            IndexResponse response = client.index(request, RequestOptions.DEFAULT);
            System.out.println(response);

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

}
