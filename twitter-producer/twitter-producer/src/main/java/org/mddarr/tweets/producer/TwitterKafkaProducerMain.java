package org.mddarr.tweets.producer;


import org.mddarr.tweets.producer.runnable.TweetStreamsThread;
import org.mddarr.tweets.producer.runnable.TweetsAvroProducerThread;
import com.typesafe.config.ConfigFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import twitter4j.Status;
import org.mddarr.tweets.producer.AppConfig;
import java.util.List;
import java.util.concurrent.*;

public class TwitterKafkaProducerMain {

    private Logger log = LoggerFactory.getLogger(TwitterKafkaProducerMain.class.getSimpleName());
    private ExecutorService executor;
    private CountDownLatch latch;
    private TweetStreamsThread tweetStreams;
    private TweetsAvroProducerThread tweetsProducer;
    private TweetStreamsThread tweetsThread;
    public static void main(String[] args) {
        TwitterKafkaProducerMain app = new TwitterKafkaProducerMain(args);
        app.start();
    }

    private TwitterKafkaProducerMain(String[] arguments){
        AppConfig appConfig = new AppConfig(ConfigFactory.load(), arguments);

        latch = new CountDownLatch(2);
        executor = Executors.newFixedThreadPool(2);
        ArrayBlockingQueue<Status> statusQueue = new ArrayBlockingQueue<Status>(appConfig.getQueuCapacity());
        tweetsThread = new TweetStreamsThread(appConfig, statusQueue, latch);
        tweetsProducer = new TweetsAvroProducerThread(appConfig,statusQueue,latch);
    }

    public void start() {

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
            if (!executor.isShutdown()) {
                log.info("Shutdown requested");
                shutdown();
            }
        }));

        log.info("Application started!");
        executor.submit(tweetsThread);
        executor.submit(tweetsProducer);
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
