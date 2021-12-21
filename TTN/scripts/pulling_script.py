import logging
import json

from numpy import positive
import fetch_tweets
import sql_methods as db
import pandas as pd
import model_operations as mo
logger = logging.getLogger(__name__)

def parse_tweets():
    # Fetch Data
    logger.info("Fetching today's trends")
    data = fetch_tweets.get_trends_and_tweets(10, 25)
    logger.info("Fetched Tweets")
    
    # Connect to Database
    conn = db.create_connection('db.sqlite3')
    cur = conn.cursor()
    
    sentiment_list = pd.read_sql_query("select sentiment_type from TTN_sentiment", conn).values.tolist()
    for val in ["Negative", "Positive"]:
        if len(sentiment_list) != 2 and val not in [ele.pop() for ele in sentiment_list]:
            cur.execute("INSERT INTO TTN_sentiment(sentiment_type) VALUES(?)", [val])
            conn.commit()
            
    sentiment_list = pd.read_sql_query("select * from TTN_sentiment", conn).values.tolist()
    sentiment_dict = dict()
    for key, val in sentiment_list:
        sentiment_dict[val] = key
    
    for trend in data:
        print(trend['name'])
        print(trend['timeStamp'])
        print(trend['tweetCount'])
        if trend['tweetCount'] > 0:
            df = pd.DataFrame(trend['tweetList'], columns = ['createdDate', 'createdBy', 'text', 'hashtags'])
            prediction, pos_words, neg_words = mo.predict(df['text'])
            df['sentiment'] = prediction
            
            trend_record_id = pd.read_sql_query(f'''SELECT id FROM TTN_trends WHERE trend_name="{trend['name']}"; ''', conn).values.tolist()
            if len(trend_record_id) == 0:
                total = pos_words[0]+neg_words[0]
                ratio = (pos_words[0]/total)*100
                cur.execute("INSERT INTO TTN_trends (trend_name, trend_date, tweet_count, positive_words, negative_words, positive_count, negative_count, sentiment_ratio) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", [trend['name'], trend['timeStamp'], total, pos_words[1], neg_words[1], pos_words[0], neg_words[0], ratio])
                conn.commit()
                trend_record_id = cur.lastrowid
            else:
                trend_record_id = trend_record_id[0][0]
                cur.execute("UPDATE TTN_trends SET trend_date = ? WHERE id = ?", (trend['timeStamp'], trend_record_id))
                conn.commit()
            
            df['createdDate'] = df['createdDate'].apply(lambda val: val.date())
            df['sentiment'] = df['sentiment'].apply(lambda val: sentiment_dict[val])
            df['hashtags'] = df['hashtags'].apply(lambda val: json.dumps(val))
            df['trend'] = trend_record_id
            cur.executemany("INSERT INTO TTN_tweets (tweet_date, user, tweet_text, hashtags, nature_id, trend_id) VALUES (?, ?, ?, ?, ?, ?);", df.values.tolist())
            conn.commit()
    
if __name__ == "__main__":
    parse_tweets()
    print("completed")