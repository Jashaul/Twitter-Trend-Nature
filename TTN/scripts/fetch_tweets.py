import tweepy
from datetime import datetime
# import pandas as pd

# Authentication
#TODO: move keys to env_variables or config file
consumerKey = "llTRAvnjGzNJCCFbPAX5bmnRq"
consumerSecret = "u9xtbPXNahG653JiCM6TIKzJDeuJqj2kxFldRa8gHHXKpvsry0"
accessToken = "949329478999658497-Ea8J6uEJFDcEhEguGX0EKQCJSxR44ra"
accessTokenSecret = "HYr7DXPBwBb54r4mOvTFMVkOk8CEVAvvf4mpZ0HUPmuCS"

auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

def get_trends(woeid = 23424977, hashtag_only = False):
    trends = api.get_place_trends(woeid)
    trend_list = trends[0]['trends']
    trending_day = trends[0]['created_at']
    for trend in trend_list:
        if hashtag_only:
            if trend['name'][0] != '#':
                trend_list.remove(trend)
    
    return trend_list, trending_day

def get_tweets(keyword, count = 10):
    if keyword[0] == '#':
        keyword = keyword.replace("#", "%23", 1)
    tweets = tweepy.Cursor(api.search_tweets, q = keyword, lang = 'en', result_type = 'mixed', include_entities = True).items(count)
        
    tweet_list = []
    for tweet in tweets:
        hashtag_list = [val['text'] for val in tweet.entities['hashtags']]
        tweet_list.append([tweet.created_at, tweet.author.screen_name, tweet.text, hashtag_list])
    return tweet_list

def get_trends_and_tweets(trend_count = 10, tweet_count = 5):
    trends, time_stamp = get_trends()
    for trend in trends[:trend_count]:
        tweet_list = get_tweets(trend['name'], tweet_count)
        trend['tweetList'] = tweet_list
        trend['timeStamp'] = datetime.today().strftime('%Y-%m-%d')
        trend['tweetCount'] = len(tweet_list)
    print(trends)
    return trends[:trend_count]