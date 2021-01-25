package me.quinnkump.app.scraper;

import com.github.jreddit.entity.Submission;
import redditjackal.entities.Post;
import redditjackal.entities.Reddit;
import redditjackal.entities.Subreddit;


import java.util.List;

public class RedditScraper {

    private Reddit reddit;
    public static void main(String args[]) {
        RedditScraper scraper = new RedditScraper("qk_stock_scraper", "quinnkump1", "uf0opTwpSa3x7Q", "GHv2ZweE0iwDuDv6zdPiiFndqOp9JA");
    }


    public <RedditToken> RedditScraper(String username, String password, String appId, String appSecret){

        String userAgent = "jReddit: Reddit API Wrapper for Java";
        String clientID = "JKJF3592jUIisfjNbZQ";
        String redirectURI = "https://www.example.com/auth";


    }
//        try {
//            String userAgent = "Stock Scraper v0.1";
//            String clientID = "uf0opTwpSa3x7Q";
//            String redirectURI = "https://www.example.com/auth";
//
//            RedditApp redditApp = new RedditInstalledApp(clientID, redirectURI);
//        } catch (Exception e){
//            System.out.printf("error is this: cuase: %s\nmessage: %s\n ", e.getCause(), e.getMessage());
//            System.err.println("Error logging into the Reddit account.");
//        }
//    }

}
