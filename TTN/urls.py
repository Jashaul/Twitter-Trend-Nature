from django.urls import path
from . import views

urlpatterns = [
    # path('', views.index, name='index'),
    # path('dashboard/', views.index, name='index'),
    # apis
    path('getTrends/', views.GetTrends.as_view()),
    path('getTweets/', views.GetTweets.as_view()),
    path('getTweets/<str:q>/', views.GetTweets.as_view())
]