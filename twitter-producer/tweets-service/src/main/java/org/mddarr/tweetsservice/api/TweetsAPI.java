package org.mddarr.tweetsservice.api;


import org.elasticsearch.client.RestHighLevelClient;
import org.mddarr.tweetsservice.TweetDTO;

import org.mddarr.tweetsservice.model.Article;
import org.mddarr.tweetsservice.services.TweetsService;
import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.*;

@RestController
@RequestMapping(value = "/tweets/")
public class TweetsAPI {
    @Autowired
    TweetsService tweetsService;

    @Autowired
    RestHighLevelClient highLevelClient;

//    public String getArticle(RestHighLevelClient client, String indexName) throws IOException {
//        GetRequest request = new GetRequest("articlesindex","_doc", "1");
//        try {
//            GetResponse getResponse = client.get(request, RequestOptions.DEFAULT);
//            System.out.println("response " + getResponse.toString());
//            return getResponse.toString();
//        } catch (ElasticsearchException e) {
//            if (e.status() == RestStatus.NOT_FOUND) {
//            }
//        }
//        return "df";
//    }

    @GetMapping(value="get")
    @CrossOrigin
    public List<TweetDTO> get(@RequestParam(value="keyword") String keyword, @RequestParam(value="lat") Double lat,
                              @RequestParam(value="lng") Double lng) throws IOException {
        List<TweetDTO>response = this.tweetsService.searchTweetsByKeyword(this.highLevelClient, keyword, lat, lng);
        return response;
    }



}
