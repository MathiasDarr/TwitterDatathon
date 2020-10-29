package org.mddarr.dakobed.twitter;

import com.typesafe.config.Config;

import java.util.ArrayList;

public class AppConfig {
    private final ArrayList<String> topics;
    private final int port;
    private final String host;
    public ArrayList<String> getTopics() {
        return topics;
    }

    public int getPort() {
        return port;
    }

    public String getHost() {
        return host;
    }

    public AppConfig(Config config, String[] arguments){
        this.topics = new ArrayList();
        for(int i=2; i<arguments.length; i++){
            this.topics.add(arguments[i]);
        }
        this.host = arguments[0];
        this.port = Integer.parseInt(arguments[1]);
    }
}
