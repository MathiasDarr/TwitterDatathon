package org.mddarr.tweets.producer;

import com.typesafe.config.Config;

import java.util.ArrayList;
import java.util.Arrays;

public class AppConfig {

    private final String bootstrapServers;
    private final String schemaRegistryUrl;

    private final String applicationId;

    private final ArrayList<String> topics;

    private final String elastic_search_host;
    private final int elastic_search_port;


    private static final String CONSUMER_KEY = System.getenv("TWITTER_CONSUMER_KEY");
    private static final String CONSUMER_SECRET = System.getenv("TWITTER_CONSUMER_SECRET");
    private static final String ACCESS_TOKEN = System.getenv("TWITTER_ACCESS_TOKEN");
    private static final String ACCESS_TOKEN_SECRET = System.getenv("TWITTER_ACCESS_TOKEN_SECRET");


    public AppConfig(Config config, String[] arguments) {

        this.bootstrapServers = arguments[0];
        this.schemaRegistryUrl = arguments[1];

        this.elastic_search_host = arguments[2];
        this.elastic_search_port = Integer.parseInt(arguments[3]);

        topics = new ArrayList<>();
        topics.addAll(Arrays.asList(arguments).subList(4, arguments.length));
        this.applicationId = "my-app-v1.0.0"; //config.getString("kafka.streams.application.id");
    }

    public static String getConsumerKey() {
        return CONSUMER_KEY;
    }

    public static String getConsumerSecret() {
        return CONSUMER_SECRET;
    }

    public static String getAccessToken() {
        return ACCESS_TOKEN;
    }

    public static String getAccessTokenSecret() {
        return ACCESS_TOKEN_SECRET;
    }

    public int getQueuCapacity(){return 100;}
    public String getBootstrapServers() {
        return bootstrapServers;
    }
    public String getSchemaRegistryUrl() {
        return schemaRegistryUrl;
    }
    public String getApplicationId() {
        return applicationId;
    }

    public ArrayList<String> getTopics() {
        return topics;
    }

    public String getElastic_search_host() {
        return elastic_search_host;
    }

    public int getElastic_search_port() {
        return elastic_search_port;
    }
}
