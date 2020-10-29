package org.mddarr.dakobed.twitter.model;

public class Tweet {

    private String date;
    private String id;
    private String content;
    private String username;
    private String location;
    private Double lat;
    private Double lng;
    public Tweet(){}

    public String getId() {
        return id;
    }
    public void setId(String id) {
        this.id = id;
    }

    public String getContent() {
        return content;
    }
    public void setContent(String content) {
        this.content = content;
    }

    public String getUsername() {
        return username;
    }
    public void setUsername(String username) {
        this.username = username;
    }

    public String getLocation() {
        return location;
    }
    public void setLocation(String location) {
        this.location = location;
    }

    public Double getLat() {return lat; }
    public Double getLng() { return lng;}

    public void setLat(Double lat) {
        this.lat = lat;
    }
    public void setLng(Double lng) {
        this.lng = lng;
    }

    public String getDate() { return date; }
    public void setDate(String date) { this.date = date; }

}
