from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver

def user_profile_pic_path(instance,filename):
    today_date = datetime.now().date()
    return "profile/%s/%s/%s" % (instance.user.username,today_date,filename)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance,**kwargs):
    #get when user updated,create when new user created
    Profile.objects.get_or_create(user=instance)
    


class ProfileQuerySet(models.QuerySet):
    def members_to_follow(self,user):
        following_ids = user.following.values_list('following_id',flat = True)
        
        return self.exclude(user__id__in = following_ids).exclude(user__id = user.id)

class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model,using=self._db)

    def members_to_follow(self,user):
        return self.get_queryset().members_to_follow(user)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    bio = models.TextField(null=True,blank=True)
    profile_picture = models.ImageField(upload_to = user_profile_pic_path,null=True,blank = True)
    location = models.CharField(max_length=150,null=True,blank=True)
    website = models.URLField(max_length=200,blank=True,null=True)
    is_verified = models.BooleanField(default=False)
    joined_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    objects = ProfileManager()



    def __str__(self):
        return self.user.username
    



    def profile_picture_url(self):
        try:
            profile_picture = self.profile_picture.url
        except:
            profile_picture = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQvY5AvnYG148-qAbpTE0QtEGfEDLCifydDxcXqddtBmQAlxYIQckuMB_4&s"

        return profile_picture
    
    def full_name(self):
        return self.user.get_full_name()
    
    def is_followed_by(self,user):
        return Follow.objects.filter(follower=user,following=self.user).exists()
    





class Follow(models.Model):
    follower = models.ForeignKey(User,on_delete=models.CASCADE,related_name='following')
    following = models.ForeignKey(User,on_delete=models.CASCADE,related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower} is following {self.following}"
    

    class Meta:
        unique_together = ('follower','following')
