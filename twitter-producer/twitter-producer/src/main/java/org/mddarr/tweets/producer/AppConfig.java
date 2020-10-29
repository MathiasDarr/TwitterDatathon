package org.mddarr.tweets.producer;

import com.typesafe.config.Config;

import java.util.ArrayList;

public class AppConfig {

    private final String bootstrapServers;
    private final String schemaRegistryUrl;

    private final String applicationId;



    private final ArrayList<String> topics;


    private final String elastic_search_host;
    private final String elastic_search_port;
    public AppConfig(Config config, String[] arguments) {

        this.bootstrapServers = arguments[0];
        this.schemaRegistryUrl = arguments[1];

        this.elastic_search_host = arguments[2];
        this.elastic_search_port = arguments[3];

        topics = new ArrayList<>();
        for(int i =4; i< arguments.length; i++){
            topics.add(arguments[i]);
        }
        this.applicationId = "my-app-v1.0.0"; //config.getString("kafka.streams.application.id");
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

    public String getElastic_search_port() {
        return elastic_search_port;
    }
}
