package org.mddarr.tweets.producer.runnable;

import org.mddarr.tweets.producer.AppConfig;

import twitter4j.*;
import twitter4j.conf.ConfigurationBuilder;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import java.util.ArrayList;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.CountDownLatch;

/*
It would be silly to hardcode the keyword which I want to grab tweets... What I should do is add the option to pass in
a key or multiple.  For now just hard code somethign..

 */


public class TweetStreamsThread implements Runnable{

    private final Log log = LogFactory.getLog(getClass());
//    static final String CONSUMER_KEY = "sRSys6TAa2RpiMqrl6foK5b1M";
//    static final String CONSUMER_SECRET = "zjtDAsLmJCCBUrBD2mo5Gu5Jol47eroD5TI1GLdaqg9xyRC8AM";
//    static final String ACCESS_TOKEN = "330787843-HXik5hFVIqGdelSm0nn92F4pvyviMLwSNibQKETs";
//    static final String ACCESS_TOKEN_SECRET = "Jqoia2vWdI6H1CXr48PNscrHgmmm2IrDJAd9BgtJQtBBl";


    private final AppConfig appConfig;
    ArrayList<ArrayBlockingQueue<Status>> statusQueues;
    private final CountDownLatch latch;
    private final  StatusListener listener;
    private final ConfigurationBuilder cb;
    private final TwitterStream twitterStream;
    private final String[] topics;
    public TweetStreamsThread(AppConfig appConfig, ArrayList<ArrayBlockingQueue<Status>> queues, CountDownLatch latch){

        this.listener = getStatusListener();
        this.cb = getConfigurationBuilder();
        this.appConfig = appConfig;
        this.statusQueues = queues;
        this.latch = latch;

        TwitterStreamFactory tf = new TwitterStreamFactory(cb.build());
        twitterStream = tf.getInstance();
        twitterStream.addListener(listener);
        FilterQuery filtre = new FilterQuery();

        String[] keywordsArray = new String[appConfig.getTopics().size()];
        for(int i =0;i<appConfig.getTopics().size();i++){
            keywordsArray[i] = appConfig.getTopics().get(i);
        }
        this.topics = keywordsArray;

//        String[] keywordsArray = {"virus", "trump"}; //filter based on your choice of keywords
        filtre.track(keywordsArray);

        twitterStream.filter(filtre);

    }

    public StatusListener getStatusListener(){
        StatusListener listener = new StatusListener() {

            @Override
            public void onStatus(Status status) {
                for(int i=0; i < topics.length; i++){
                    if(status.getText().contains(topics[i])){
                        statusQueues.get(i).add(status);
                    }
                }
                //System.out.println(status.getUser().getName() + " " + status.getUser().getFollowersCount());
                status.getUser();
            }
            public void onDeletionNotice(StatusDeletionNotice statusDeletionNotice) {}
            public void onTrackLimitationNotice(int numberOfLimitedStatuses) {}
            public void onException(Exception ex) { ex.printStackTrace(); }

            @Override
            public void onScrubGeo(long l, long l1) { }
            @Override
            public void onStallWarning(StallWarning stallWarning) { }

        };
        return listener;
    }


    private ConfigurationBuilder getConfigurationBuilder(){
        ConfigurationBuilder cb = new ConfigurationBuilder();
        cb.setDebugEnabled(true)
                .setOAuthConsumerKey(AppConfig.getConsumerKey())
                .setOAuthConsumerSecret(AppConfig.getConsumerSecret())
                .setOAuthAccessToken(AppConfig.getAccessToken())
                .setOAuthAccessTokenSecret(AppConfig.getAccessTokenSecret());
        return cb;
    }

    public void run(){

    }

}
