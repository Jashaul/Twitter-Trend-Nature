from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Trends, Tweets, Sentiment
import json
from django.core import serializers
from datetime import datetime
from django.db import connection

def map_trend_to_dict(obj):
    trend_dict = {
        'id': obj[0],
        'trend': obj[1],
        'date': obj[2].strftime('%m/%d/%Y'),
        'positveRatio' : obj[7],
        'tweet_metrics': {
            'postiveTweets': obj[5],
            'positiveWords': obj[6].replace("  ", "").split(" "),
            'negativeTweets': obj[3],
            'negativeWords': obj[4].replace("  ", "").split(" ")
        }
    }
    return trend_dict

def map_tweet_to_dict(obj):
    tweet_dict = {
        'id': obj[0],
        'tweet': obj[1],
        'date': obj[2].strftime('%m/%d/%Y'),
        'user': obj[3],
        'hashtags': json.loads(obj[4]),
        'trend': obj[5],
        'trendDate': obj[6].strftime('%m/%d/%Y'),
        'sentiment': obj[-1]
    }
    return tweet_dict
    
class GetTrends(APIView):
    def get(self, request):
        sqlquery = '''  SELECT *
                        FROM TTN_trends
                        WHERE trend_date="2021-12-16"
                        LIMIT 10; '''
        with connection.cursor() as cursor:
            cursor.execute(sqlquery)
            data = cursor.fetchall()
        trend_dict = [map_trend_to_dict(row) for row in data]
        return Response({'status': 'success', 'data': trend_dict}, status=status.HTTP_200_OK)
    
class GetTweets(APIView):
    def get(self, request, q=None):
        if q:
            sqlquery = f'''  SELECT TTN_tweets.id, TTN_tweets.tweet_text, TTN_tweets.tweet_date, TTN_tweets.user, TTN_tweets.hashtags, TTN_trends.trend_name, TTN_trends.trend_date, TTN_sentiment.sentiment_type
                            FROM TTN_tweets
                            INNER JOIN TTN_trends
                            INNER JOIN TTN_sentiment
                            WHERE TTN_trends.trend_name="{q}" 
                            GROUP BY TTN_tweets.tweet_text
                            ORDER BY TTN_tweets.tweet_date DESC
                            LIMIT 5; '''
            with connection.cursor() as cursor:
                cursor.execute(sqlquery)
                data = cursor.fetchall()              
            tweet_dict = [map_tweet_to_dict(row) for row in data]
            return Response({'status': 'success', 'trendName': q, 'data': tweet_dict}, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'failed', 'message': 'ERROR'}, status=status.HTTP_400_BAD_REQUEST)