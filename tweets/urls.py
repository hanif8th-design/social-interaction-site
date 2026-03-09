from django.urls import path
from tweets.views import (
    CreateTweetView,
    TweetUpdateView,
    DeleteTweetView,
    toggle_like
    )

app_name = "tweets"

urlpatterns = [
    path('my-tweets',CreateTweetView.as_view(),name = "my_tweets"),
    path('<uuid:pk>/tweet-update',TweetUpdateView.as_view(),name = "tweet-update"),
    path('<uuid:pk>/tweet-delete',DeleteTweetView.as_view(),name = "tweet-delete"),
    path('like/', toggle_like, name='toggle-like'),


    
]
