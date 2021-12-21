from django.db import models
import json

class Sentiment(models.Model):
    sentiment_type = models.CharField(max_length=200)
    
class Trends(models.Model):
    trend_name = models.CharField(max_length=200)
    trend_date = models.DateTimeField('date published')
    tweet_count = models.IntegerField(default=0)
    sentiment_ratio = models.IntegerField(default=0)
    positive_words = models.TextField(default="")
    negative_words = models.TextField(default="")
    positive_count = models.IntegerField(default=0)
    negative_count = models.IntegerField(default=0)
    
    def set_positive_words(self, x):
        if type(x) is list:
            self.positive_words = json.dumps(x)
        else:
            self.positive_words = x

    def get_positive_words(self):
        return json.loads(self.positive_words)
    
    def set_negative_words(self, x):
        if type(x) is list:
            self.negative_words = json.dumps(x)
        else:
            self.negative_words = x

    def get_negative_words(self):
        return json.loads(self.negative_words)
    
class Tweets(models.Model):
    tweet_text = models.CharField(max_length=200)
    tweet_date = models.DateTimeField('date published')
    user = models.CharField(max_length=200)
    hashtags = models.TextField()
    trend = models.ForeignKey(Trends, related_name='%(class)s_trend_name', on_delete=models.PROTECT)
    nature = models.ForeignKey(Sentiment, related_name='%(class)s_sentiment_type', on_delete=models.PROTECT)
    
    def set_hashtags(self, x):
        if type(x) is list:
            self.hashtags = json.dumps(x)
        else:
            self.hashtags = x

    def get_hashtags(self):
        return json.loads(self.hashtags)