# from rest_framework import serializers
# from .models import Tweets

# class TweetsSerializer(serializers.ModelSerializer):
#     product_name = serializers.CharField(max_length=200)
#     product_price = serializers.FloatField()
#     product_quantity = serializers.IntegerField(required=False, default=1)
#     tweet_text = serializers.CharField(max_length=200)
#     tweet_date = serializers.DateTimeField('date published')
#     user = serializers.CharField(max_length=200)
#     hashtags = serializers.TextField()
#     trend = serializers.CharField(source='trend.trend_name')
#     nature = serializers.CharField(source='nature.sentiment_type')

#     class Meta:
#         model = Tweets
        # fields = ('__all__')