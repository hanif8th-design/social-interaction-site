from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from comments.models import Comment
from tweets.models import Tweet
from notifications.tasks import create_notification


@login_required
@require_POST
def add_comment(request,pk):
    tweet = get_object_or_404(Tweet,id = pk)
    content = request.POST.get('content')
    
    if content:
        comment = Comment.objects.create(
            tweet = tweet,
            content = content,
            author = request.user,
        )

        recipient_username = tweet.author.username
        actor_username = comment.author.username
        verb = f"{actor_username} commented on your post"
        object_id = tweet.id


        create_notification.delay(
            recipient_username = recipient_username,
            actor_username = actor_username,
            verb = verb,
            object_id = object_id
        )
    return redirect("accounts:home")
