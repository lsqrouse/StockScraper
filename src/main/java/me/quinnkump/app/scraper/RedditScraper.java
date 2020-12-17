package me.quinnkump.app.scraper;

import redditjackal.entities.Reddit;

public class RedditScraper {

    private Reddit reddit;

    public RedditScraper(String username, String password, String appId, String appSecret){
        try {
            this.reddit = new Reddit(username, password, appId, appSecret);
        } catch (Exception e){
            System.err.println("Error logging into the Reddit account.");
        }
    }

}
