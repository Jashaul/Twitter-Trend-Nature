from django.urls import path
from . import views

urlpatterns = [
    # apis
    path('getTrends/', views.GetTrends.as_view()),
    path('getTweets/', views.GetTweets.as_view()),
    path('getTweets/<str:q>/', views.GetTweets.as_view())
]