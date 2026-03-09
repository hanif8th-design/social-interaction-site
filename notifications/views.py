from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import ListView
from notifications.models import Notification
from accounts.models import Profile
from django.views.decorators.http import require_POST

class NotificationListView(ListView):
    model = Notification
    template_name = 'notifications/notifications_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.notifications_for_user(self.request.user)
    
    def get_context_data(self, **kwargs):
        notifications_count = Notification.objects.notifications_for_user(self.request.user).count()
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        context = super(NotificationListView,self).get_context_data(**kwargs)
        # Pass the list of tweets to the template
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['members_to_follow'] = members_to_follow
        context['notifications_count'] = notifications_count

        return context


@require_POST
def MarkAsReadView(request,pk):
    notification = get_object_or_404(Notification,id = pk)

    notification.read = True
    notification.save()

    return redirect("notifications:notification-list")

@require_POST
def mark_all_read(request):
    notifications_for_user = Notification.objects.notifications_for_user(request.user).update(read = True)
    return redirect("notifications:notification-list")

    


    




     
        
    



