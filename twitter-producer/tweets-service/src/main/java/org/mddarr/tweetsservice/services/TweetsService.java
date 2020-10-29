package org.mddarr.tweetsservice.services;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.elasticsearch.action.admin.indices.create.CreateIndexRequest;
import org.elasticsearch.action.admin.indices.create.CreateIndexResponse;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.action.index.IndexResponse;
import org.elasticsearch.action.search.SearchRequest;
import org.elasticsearch.action.search.SearchResponse;
import org.elasticsearch.client.RequestOptions;
import org.elasticsearch.client.RestHighLevelClient;
import org.elasticsearch.common.document.DocumentField;
import org.elasticsearch.index.query.MatchQueryBuilder;
import org.elasticsearch.search.SearchHit;
import org.elasticsearch.search.SearchHits;
import org.elasticsearch.search.builder.SearchSourceBuilder;
import org.mddarr.tweetsservice.TweetDTO;
import org.springframework.data.elasticsearch.annotations.Document;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.util.*;

@Service
public class TweetsService {

    public List<TweetDTO> searchTweetsByKeyword(RestHighLevelClient client, String keyword, Double lat, Double lng) throws IOException {
        SearchRequest searchRequest = new SearchRequest("kafka-tweets");

        SearchSourceBuilder sourceBuilder = new SearchSourceBuilder();
        MatchQueryBuilder matchQueryBuilder = new MatchQueryBuilder("tweet_content", keyword);
        sourceBuilder.query(matchQueryBuilder);
        searchRequest.source(sourceBuilder);

        SearchResponse response = client.search(searchRequest, RequestOptions.DEFAULT);

        SearchHits hits = response.getHits();
        System.out.println(hits.getTotalHits());
        return parseTweetsFromHits(hits);
    }

    public List<TweetDTO> parseTweetsFromHits(SearchHits hits) throws JsonProcessingException {
        List<TweetDTO> tweets = new ArrayList<>();

        for (SearchHit hit : hits) {
            Map<String, DocumentField> fields = hit.getFields();
            Set<String> a = fields.keySet();

            String hitJson = hit.getSourceAsString();
            ObjectMapper objectMapper = new ObjectMapper();
            TweetDTO tweet = objectMapper.readValue(hitJson, TweetDTO.class);
            tweets.add(tweet);
        }
        return tweets;
    }

    public boolean addDocumentIndex(RestHighLevelClient client, String indexName) throws IOException {
        Map<String, Object> jsonMap = new HashMap<>();
        jsonMap.put("dumb", "stupid");

        jsonMap.put("postDate", new Date());
        jsonMap.put("message", "trying out Elasticsearch");
        IndexRequest indexRequest = new IndexRequest("articlesindex").type("_doc")
                .id("2").source(jsonMap);
        IndexResponse indexResponse = client.index(indexRequest, RequestOptions.DEFAULT);
        return true;
    }

    public boolean createIndex(RestHighLevelClient client, String indexName) throws IOException {
        CreateIndexRequest request = new CreateIndexRequest(indexName);
        //no options just straight forward
        CreateIndexResponse response = client.indices().create(request, RequestOptions.DEFAULT);
        return response.isAcknowledged();
    }


}
