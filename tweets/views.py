from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from tweets.models import Tweet,Like
from tweets.forms import CreateTweetForm
from accounts.models import Profile
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from notifications.tasks import create_notification
from notifications.models import Notification





class CreateTweetView(CreateView):
    model = Tweet
    form_class = CreateTweetForm
    template_name = "tweets/user_tweets_create_list.html"
    success_url = reverse_lazy("tweets:my_tweets")

    def form_valid(self, form):
        # Assign logged-in user before saving
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        notifications_count = Notification.objects.notifications_for_user(self.request.user).count()

        
        context = super(CreateTweetView,self).get_context_data(**kwargs)
        # Pass the list of tweets to the template
        context['my_tweets'] = Tweet.objects.my_tweets(self.request.user)
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['notifications_count'] = notifications_count
        context['members_to_follow'] = members_to_follow
        context['notifications_count'] = notifications_count
        
        return context

class TweetUpdateView(UpdateView):
    model = Tweet
    template_name = "tweets/tweet_update.html"
    form_class = CreateTweetForm
    success_url = reverse_lazy("tweets:my_tweets")

    def get_queryset(self):
        return Tweet.objects.filter(author = self.request.user)
    def get_context_data(self, **kwargs):
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        notifications_count = Notification.objects.notifications_for_user(self.request.user).count()
        context = super(TweetUpdateView,self).get_context_data(**kwargs)
        # Pass the list of tweets to the template
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['members_to_follow'] = members_to_follow
        context['notifications_count'] = notifications_count
        
        
        return context
    
class DeleteTweetView(DeleteView):
    model = Tweet
    template_name = "tweets/tweet_delete.html"
    success_url = reverse_lazy("tweets:my_tweets")

    def get_queryset(self):
        return Tweet.objects.filter(author = self.request.user)
    
    def get_context_data(self, **kwargs):
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        notifications_count = Notification.objects.notifications_for_user(self.request.user).count()
        context = super(DeleteTweetView,self).get_context_data(**kwargs)
        # Pass the list of tweets to the template
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['members_to_follow'] = members_to_follow
        context['notifications_count'] = notifications_count
        
        
        return context


@login_required
@require_POST
def toggle_like(request):
    tweet_id = request.POST.get('tweet_id')
    tweet = get_object_or_404(Tweet, id=tweet_id)

    # Prevent duplicate likes
    like_obj,created = Like.objects.get_or_create(tweet=tweet, user=request.user)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

        recipient_username = tweet.author.username 
        verb = f"{request.user.username} liked your post"
        actor_username = request.user.username

        #send notification of like
        create_notification.delay(
        recipient_username = recipient_username,
        actor_username = actor_username,
        verb = verb,
        object_id = tweet.id
    )


    
    return JsonResponse(
        {"liked":liked,
        "likes_count":tweet.likes.count()
        }
    )

    






    
    
    
    
        
    
