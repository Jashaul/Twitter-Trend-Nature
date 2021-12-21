from django.contrib import admin
from .models import Sentiment, Trends, Tweets

# Register your models here.
admin.site.register(Sentiment)
admin.site.register(Trends)
admin.site.register(Tweets)