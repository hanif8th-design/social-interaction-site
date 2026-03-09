from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from tweets.models import Tweet


class NotificationQuerySet(models.QuerySet):
    def notifications_for_user(self,user):
        return self.filter(recipient = user)

    def read(self):
        return self.filter(read = True)
    
    def unread(self):
        return self.filter(read = False)

class NotificationManager(models.Manager):
    def get_queryset(self):
        return NotificationQuerySet(self.model,self._db)
    
    def notifications_for_user(self,user):
        return self.get_queryset().unread()
    
    
    
    




class Notification(models.Model):
    recipient  = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notifications')
    actor = models.ForeignKey(User,on_delete=models.CASCADE,related_name='actions')
    verb = models.CharField()
    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type','object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    objects = NotificationManager()

    def __str__(self):
        return f"{self.actor} {self.verb}"

    class Meta:
        ordering = ["-created_at"]

    
        
    
