from django.contrib import admin
from tweets.models import Tweet,Like,Attachment

@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    pass


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass





