package org.mddarr.tweetsservice;

public class TweetDTO {
    String screename;
    String name;
    String tweet_content;
    String location;
    Long tweet_time;
    Long id;
    Double lat;
    Double lng;

    @Override
    public String toString() {
        return "TweetDTO{" +
                "screename='" + screename + '\'' +
                ", name='" + name + '\'' +
                ", tweet_content='" + tweet_content + '\'' +
                ", location='" + location + '\'' +
                ", tweet_time=" + tweet_time +
                ", id=" + id +
                '}';
    }

    public TweetDTO(){}

    public TweetDTO(String screename, String name, String tweet_content, String location, Long tweet_time, Long id, Double lat, Double lng) {
        this.screename = screename;
        this.name = name;
        this.tweet_content = tweet_content;
        this.location = location;
        this.tweet_time = tweet_time;
        this.id = id;
        this.lat = lat;
        this.lng = lng;
    }

    public Double getLat() {
        return lat;
    }

    public void setLat(Double lat) {
        this.lat = lat;
    }

    public Double getLng() {
        return lng;
    }

    public void setLng(Double lng) {
        this.lng = lng;
    }

    public String getScreename() {
        return screename;
    }

    public void setScreename(String screename) {
        this.screename = screename;
    }

    public String getContent() {
        return tweet_content;
    }

    public void setContent(String content) {
        this.tweet_content = content;
    }

    public String getLocation() {
        return location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getTweet_content() {
        return tweet_content;
    }

    public void setTweet_content(String tweet_content) {
        this.tweet_content = tweet_content;
    }

    public Long getTweet_time() {
        return tweet_time;
    }

    public void setTweet_time(Long tweet_time) {
        this.tweet_time = tweet_time;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }
}
