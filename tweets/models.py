from django.db import models
from django.contrib.auth.models import User
import uuid

class TweetQuerySet(models.QuerySet):
    def latest_tweets(self):
        return self.order_by("-created_at")

    def tweets_for_user(self,user):
        following_users = user.following.values_list('following_id',flat = True)

        return self.filter(author__id__in = following_users)
    def my_tweets(self,user):
        return self.filter(author = user)


class TweetManager(models.Manager):
    def get_queryset(self):
        return TweetQuerySet(self.model,using= self._db)
    def latest_tweets(self):
        return self.get_queryset().latest_tweets()
    
    def tweets_for_user(self,user):
        return self.get_queryset().tweets_for_user(user).latest_tweets()
    def my_tweets(self,user):
        return self.get_queryset().my_tweets(user)
    

class Tweet(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tweets')
    content = models.TextField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_reply_to_tweet = models.ForeignKey('self',on_delete=models.CASCADE,related_name = 'replies',null=True,blank=True)

    objects = TweetManager()

    def __str__(self):
        return f"Post By {self.author.username}"
    class Meta:
        ordering = ["-created_at"]

class Like(models.Model):
    tweet = models.ForeignKey(Tweet,on_delete = models.CASCADE,related_name = 'likes')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('tweet','user')


class Retweet(models.Model):
    user = user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='retweets')
    tweet = models.ForeignKey(Tweet,on_delete = models.CASCADE,related_name = 'retweets')
    created_at = models.DateTimeField(auto_now_add=True)

    
    

    class Meta:
        unique_together = ('user','tweet')

def tweet_attachment_path_location(instance,filename):
    #get today date
    today_date = datetime.now().date()
    return "attachments/%s/%s/%s" % (instance.user.username,today_date,filename) 


class Attachment(models.Model):
    tweet = models.ForeignKey(Tweet,on_delete=models.CASCADE,related_name='attachments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'attachments')
    file = models.FileField(upload_to =tweet_attachment_path_location )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"attachment by {self.user.username} on {self.tweet}"
    






    
    