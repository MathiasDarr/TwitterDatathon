package org.mddarr.dakobed.twitter.runnable;


import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.http.impl.nio.client.HttpAsyncClientBuilder;
import org.elasticsearch.ElasticsearchException;
import org.elasticsearch.action.admin.cluster.health.ClusterHealthRequest;
import org.elasticsearch.action.admin.cluster.health.ClusterHealthResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestClientBuilder;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.io.stream.Writeable;
import org.elasticsearch.common.xcontent.XContentType;
import org.elasticsearch.rest.RestStatus;
import org.joda.time.DateTime;
import java.time.format.DateTimeFormatter;
import java.time.LocalDateTime;

import org.mddarr.dakobed.twitter.model.Tweet;
import twitter4j.Status;


import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.CountDownLatch;

public class TweetsElasticSearchThread implements Runnable{
    private final Log log = LogFactory.getLog(getClass());
    private final CountDownLatch latch;
    private final String port;
    private final String host;
    private final String filter;
    private final DateTimeFormatter dtf = DateTimeFormatter.ofPattern("yyyy/MM/dd HH:mm:ss");
    private int recordCount;

    private final ArrayBlockingQueue<Status> statusQueue;

    public TweetsElasticSearchThread(ArrayBlockingQueue<Status> statusQueue, CountDownLatch latch, String host, int port, String filter){
        this.statusQueue = statusQueue;
        this.latch = latch;
        this.recordCount +=1;
        this.host = host;
        this.port = port;
        this.filter = filter;
    }

    public void run() {
        int tweetCount = 0;


//        final CredentialsProvider credsProvider = new BasicCredentialsProvider();
//        credsProvider.setCredentials(AuthScope.ANY,
//                new UsernamePasswordCredentials("master-user", "1!Master-user-password"));
        String scheme;
        if(this.host.equals("localhost")){
            scheme="http";
        }else{
            scheme="https";
        }

//        RestClientBuilder builder = RestClient.builder(new HttpHost(this.host, Integer.parseInt(this.port), scheme))
//                .setHttpClientConfigCallback(new RestClientBuilder.HttpClientConfigCallback() {
//                    public HttpAsyncClientBuilder customizeHttpClient(HttpAsyncClientBuilder httpClientBuilder) {
//                        return httpClientBuilder.setDefaultCredentialsProvider(credsProvider);
//                    }
//                });

//        RestClient client = RestClient.builder(
//                new HttpHost("localhost", 29200, "http")).build();
//        int port = 29200;
        RestHighLevelClient client = new RestHighLevelClient(RestClient.builder(new HttpHost(host, Integer.parseInt(port), "http")));

//        RestHighLevelClient client = new RestHighLevelClient(builder);

        while(latch.getCount() >0 ) {
            try {
                if(statusQueue.size()>0) {
                    Status status = statusQueue.poll();
                    tweetCount += 1;
                    Tweet tweet = statusToTweet(status, tweetCount);
                    System.out.println("The length of the content is " + tweet.getContent().length());

                    IndexRequest request = new IndexRequest("tweets");
                    String jsonString = "{" +
                            "\"username\":\"" +  tweet.getUsername()+"\"," +
                            "\"content\":\"" +  tweet.getContent()+"\"," +
                            "\"location\":\""  +  tweet.getLocation() +"\"," +
                            "\"date\":\""  +  tweet.getDate() +"\""
                            + "}";

                    request.source(jsonString, XContentType.JSON);
                    try {
                        IndexResponse response = client.index(request, RequestOptions.DEFAULT);
                        System.out.println(response);

                    } catch (ElasticsearchException e) {
                        if (e.status() == RestStatus.CONFLICT) {
                        }
                        System.out.println("The problem is " + jsonString);
                    }
                }

            } catch (Exception e) {
                System.out.println(e);
            }
        }
        close();
    }

    public void close(){
        log.info("Closing Producer");
        latch.countDown();
    }

    public Tweet statusToTweet(Status status, int id){

        LocalDateTime now = LocalDateTime.now();
        Tweet tweet = new Tweet();
        tweet.setDate(dtf.format(now));
        tweet.setUsername(status.getUser().getScreenName());
        tweet.setLocation(status.getUser().getLocation());
        tweet.setContent(status.getText());
        tweet.setLat(-12.0);
        tweet.setLng(12.0);
        return tweet;
    }
}
