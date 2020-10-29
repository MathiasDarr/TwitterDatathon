package org.mddarr.dakobed.twitter;


import com.typesafe.config.ConfigFactory;
import org.mddarr.dakobed.twitter.runnable.TweetStreamsThread;
import org.mddarr.dakobed.twitter.runnable.TweetsElasticSearchThread;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import twitter4j.Status;

import java.io.IOException;
import java.util.List;
import java.util.concurrent.*;

public class TwitterProducerMain {

    private Logger log = LoggerFactory.getLogger(TwitterProducerMain.class.getSimpleName());
    private ExecutorService executor;
    private CountDownLatch latch;
    private TweetStreamsThread tweetStreams;

    private TweetsElasticSearchThread elasticSearchThread;
    private TweetStreamsThread tweetsThread;
    public static void main(String[] args) throws IOException {
        TwitterProducerMain app = new TwitterProducerMain(args);
        app.start();
    }

    private TwitterProducerMain(String[] arguments){
        AppConfig appConfig = new AppConfig(ConfigFactory.load(), arguments);

        String filter_argument = appConfig.getTopics().get(0);
        String hostname = appConfig.getHost();
        int port = appConfig.getPort();
        latch = new CountDownLatch(2);
        executor = Executors.newFixedThreadPool(2);
        ArrayBlockingQueue<Status> statusQueue = new ArrayBlockingQueue<Status>(100);
        tweetsThread = new TweetStreamsThread(statusQueue, latch, filter_argument);
        elasticSearchThread = new TweetsElasticSearchThread(statusQueue, latch, hostname, port, filter_argument);

    }

    public void start() throws IOException {

        log.info("Application started!");
        executor.submit(tweetsThread);
        executor.submit(elasticSearchThread);
        log.info("Stuff submit");
        try {
            log.info("Latch await");
            latch.await();
            log.info("Threads completed");
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            shutdown();
            log.info("Application closed succesfully");
        }


//        RestHighLevelClient client = new RestHighLevelClient(
//                RestClient.builder(
//                        new HttpHost("localhost", 29200, "http"),
//                        new HttpHost("localhost", 9201, "http")));
//
//        IndexRequest request = new IndexRequest("tweets");
//        String jsonString = "{" +
//                "\"user\":\"frank\"," +
//                "\"postDate\":\"2020-03-02\"," +
//                "\"message\":\"created this document from Java\"" +
//                "}";
//
//        request.source(jsonString, XContentType.JSON);
//
//        try {
//            IndexResponse response = client.index(request, RequestOptions.DEFAULT);
//            System.out.println(response);
//
//        } catch (ElasticsearchException e) {
//            if (e.status() == RestStatus.CONFLICT) {
//            }
//        }
//
//
//        jsonString = "{" +
//                "\"user\":\"george\"," +
//                "\"postDate\":\"2020-03-02\"," +
//                "\"message\":\"created this document from Java\"" +
//                "}";
//        request.source(jsonString, XContentType.JSON);
//
//        try {
//            IndexResponse response = client.index(request, RequestOptions.DEFAULT);
//            System.out.println(response);
//
//        } catch (ElasticsearchException e) {
//            if (e.status() == RestStatus.CONFLICT) {
//            }
//        }
//        client.close();

//        CreateIndexRequest request = new CreateIndexRequest("users");
//        request.settings(Settings.builder()
//                .put("index.number_of_shards", 3)
//                .put("index.number_of_replicas", 2)
//        );
//        Map<String, Object> message = new HashMap<>();
//        message.put("type", "text");
//
//        Map<String, Object> properties = new HashMap<>();
//        properties.put("userId", message);
//        properties.put("name", message);
//
//        Map<String, Object> mapping = new HashMap<>();
//        mapping.put("properties", properties);
//        request.mapping(mapping);
//
//        CreateIndexResponse indexResponse = client.indices().create(request, RequestOptions.DEFAULT);
//        System.out.println("response id: "+indexResponse.index());
//
//
//        Map<String, Object> jsonMap = new HashMap<>();
//        jsonMap.put("user", "kimchy");
//        jsonMap.put("postDate", new Date());
//        jsonMap.put("message", "trying out Elasticsearch");
//        IndexRequest indexRequest = new IndexRequest("posts")
//                .id("1").source(jsonMap);
//
//
//
//        XContentBuilder builder = XContentFactory.jsonBuilder();
//        builder.startObject();
//        {
//            builder.field("user", "kimchy");
//            builder.timeField("postDate", new Date());
//            builder.field("message", "trying out Elasticsearch");
//        }
//        builder.endObject();
//        indexRequest = new IndexRequest("posts")
//                .id("1").source(builder);
//
//
//        IndexResponse indexResponse = client.index(request, RequestOptions.DEFAULT);
//
//
//        String index = indexResponse.getIndex();
//        String id = indexResponse.getId();
//        if (indexResponse.getResult() == DocWriteResponse.Result.CREATED) {
//
//        } else if (indexResponse.getResult() == DocWriteResponse.Result.UPDATED) {
//
//        }
//        ReplicationResponse.ShardInfo shardInfo = indexResponse.getShardInfo();
//        if (shardInfo.getTotal() != shardInfo.getSuccessful()) {
//
//        }
//        if (shardInfo.getFailed() > 0) {
//            for (ReplicationResponse.ShardInfo.Failure failure :
//                    shardInfo.getFailures()) {
//                String reason = failure.reason();
//            }
//        }


//        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
//            if (!executor.isShutdown()) {
//                log.info("Shutdown requested");
//                shutdown();
//            }
//        }));
//


    }

    private void shutdown() {
        if (!executor.isShutdown()) {
            log.info("Shutting down");
            executor.shutdownNow();
            try {
                if (!executor.awaitTermination(2000, TimeUnit.MILLISECONDS)) { //optional *
                    log.warn("Executor did not terminate in the specified time."); //optional *
                    List<Runnable> droppedTasks = executor.shutdownNow(); //optional **
                    log.warn("Executor was abruptly shut down. " + droppedTasks.size() + " tasks will not be executed."); //optional **
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }


}
