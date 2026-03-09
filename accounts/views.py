from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.views import PasswordResetView,PasswordChangeView,PasswordChangeForm
from accounts.forms import LoginForm,RegisterForm,ProfileUpdateForm,UserUpdateForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import View,ListView,DetailView
from tweets.models import Tweet
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from accounts.decoraters import redirect_if_logged_in
from django.utils.decorators import method_decorator
from accounts.models import Profile,Follow
from django.views.decorators.http import require_POST
from django.db.models import Q
from notifications.tasks import create_follow_notification
from notifications.models import Notification




#auth views 

@redirect_if_logged_in
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request,data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(username = username,password = password)

            #if valid user it user = return user if not valid it returns None
            if user is not None:
                login(request,user)
                return redirect('accounts:home')
            else:
                messages.warning(request,"Invalid username or password")

        else:
            messages.warning(request,"Enter correct username password ")
    else:
        form = LoginForm()
    return render(request,"registration/login.html",context={'form':form})


def logout_view(request):
    if request.method == 'POST':
        logout(request) #delete session
        messages.success(request, "You have been logged out successfully.")
        return redirect('accounts:login')  # Redirect to login page
    else:
        return redirect('accounts:home')


@redirect_if_logged_in
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:login')
        else:
            messages.warning(request,"Enter correct inputs")
    else:
        form = RegisterForm()
    
    return render(request,"registration/signup.html",context={'form':form})




@method_decorator(redirect_if_logged_in,name = 'dispatch')
class CustomPasswordResetView(PasswordResetView):
    template_name='accounts/password_reset.html'
    email_template_name='accounts/password_reset_email.html'
    subject_template_name='accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')



class CustomPasswordChangeView(PasswordChangeView):
    form = PasswordChangeForm
    template_name = 'registration/change_password.html'
    success_url = reverse_lazy("accounts:home")

    def get_context_data(self, **kwargs):
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        context = super(CustomPasswordChangeView,self).get_context_data(**kwargs)

        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['members_to_follow'] = members_to_follow
        
        return context
    

# end auth views  
    



class HomeView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        members_to_follow = Profile.objects.members_to_follow(request.user)
        user_followings_count = request.user.following.count()
        user_follower_count = request.user.followers.count()
        latest_tweets = Tweet.objects.latest_tweets()
        tweets_for_user = Tweet.objects.tweets_for_user(request.user) 
        notifications_count = Notification.objects.notifications_for_user(self.request.user).count()


        
        
        context = {}
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['members_to_follow'] = members_to_follow
        context['latest_tweets'] = latest_tweets
        context['tweets_for_user'] = tweets_for_user
        context['notifications_count'] = notifications_count





        


        return render(request,"accounts/home.html",context)

@require_POST
def FollowView(request,pk):
        user_profile = request.user
        target_user = get_object_or_404(Profile,pk=pk).user

        if user_profile == target_user:
            messages.warning(request,"You cannot follow yourself")
            return redirect("accounts:home")
        
        follow_obj,created = Follow.objects.get_or_create(
            follower = user_profile,
            following = target_user
        )

        if not created:
            messages.warning(request,'You are already following this user')

        else:
            
            messages.success(request,'User created Successfully')
            
            #send notification
            recipient_username = target_user.username
            actor_username = user_profile.username
            verb = f"{actor_username} followed you"
            object_id = target_user.id

            create_follow_notification.delay(
                recipient_username = recipient_username,
                actor_username = actor_username,
                verb = verb,
                object_id = object_id
            )

            return redirect('accounts:home')

class FollowerListView(ListView):
    model = Follow
    template_name = "accounts/followers_and_following_list.html"
    context_object_name = 'follows'

    def get_queryset(self):
        
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return Follow.objects.filter(following=profile.user)
    
    def get_context_data(self,**kwargs):
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        notifications_count = Notification.objects.notifications_for_user(self.request.user).count()

        context = super(FollowerListView,self).get_context_data(**kwargs)
        context['list_type'] = 'followers'  # flag for template
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['notifications_count'] = notifications_count
        context['members_to_follow'] = members_to_follow
        return context


class FollowingListView(ListView):
    model = Follow
    template_name  = "accounts/followers_and_following_list.html"
    context_object_name = 'follows'
    
    def get_queryset(self):
        profile = get_object_or_404(Profile,pk = self.kwargs['pk'])
        return Follow.objects.filter(follower=profile.user)

    def get_context_data(self, **kwargs):
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        notifications_count = Notification.objects.notifications_for_user(self.request.user).count()

        context = super(FollowingListView,self).get_context_data(**kwargs)

        context['list_type'] = 'following'  # flag for template
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['members_to_follow'] = members_to_follow
        context['notifications_count'] = notifications_count
        
        return context

@require_POST
def unfollow_user(request,pk):
    user_to_unfollow = get_object_or_404(Profile, id = pk )

    Follow.objects.filter(
        follower = request.user,
        following = user_to_unfollow.user
    ).delete()

    return redirect('accounts:followings', request.user.profile.pk)

class SearchUserView(ListView):
    model = User
    template_name = "accounts/search_results.html"
    context_object_name = 'users'

    def get_queryset(self):
        query = self.request.GET.get('q','')
        if query:
           return  User.objects.filter(
                Q(username__icontains = query)|
                Q(first_name__icontains = query)|
                Q(last_name__icontains = query)
           ).distinct()
        return User.objects.none()
    def get_context_data(self, **kwargs):
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        notifications_count = Notification.objects.notifications_for_user(self.request.user).count()

        context = super().get_context_data(**kwargs)
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['members_to_follow'] = members_to_follow
        context['notifications_count'] = notifications_count
        return context
    

class ProfileDetailView(DetailView):
    model = Profile
    template_name = "accounts/profile_info.html"
    context_object_name = "profile"

    def get_object(self):
        pk = self.kwargs['pk']
        return get_object_or_404(Profile,id = pk)
    def get_context_data(self, **kwargs):
        profile = self.get_object()
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        is_following = profile.is_followed_by(self.request.user)
        members_to_follow = Profile.objects.members_to_follow(self.request.user)
        user_followings_count = self.request.user.following.count()
        user_follower_count = self.request.user.followers.count()
        user_tweets = Tweet.objects.filter(author=profile.user)
        notifications_count = Notification.objects.notifications_for_user(self.request.user).count()

        

        context = super(ProfileDetailView,self).get_context_data(**kwargs)
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['members_to_follow'] = members_to_follow
        context['is_following'] = is_following
        context['user_followings_count'] = user_followings_count
        context['user_follower_count'] = user_follower_count
        context['members_to_follow'] = members_to_follow
        context['user_tweets'] = user_tweets
        context['notifications_count'] = notifications_count

        

        return context

def ProfileUpdateView(request):
    if request.method == "POST":
        ProfileForm = ProfileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        UserForm = UserUpdateForm(request.POST,instance=request.user)

        if ProfileForm.is_valid() and UserForm.is_valid():
            UserForm.save()
            ProfileForm.save()
            return redirect('accounts:profile-detail' ,pk = request.user.profile.pk)
        
    else:
        ProfileForm = ProfileUpdateForm(instance=request.user.profile)
        UserForm = UserUpdateForm(instance=request.user)


    members_to_follow = Profile.objects.members_to_follow(request.user)
    user_followings_count = request.user.following.count()
    user_follower_count = request.user.followers.count()
    notifications_count = Notification.objects.notifications_for_user(request.user).count()

    context = {}
    context['user_followings_count'] = user_followings_count
    context['user_follower_count'] = user_follower_count
    context['members_to_follow'] = members_to_follow
    context['profile_form'] = ProfileForm
    context['user_form'] = UserForm
    context['notifications_count'] = notifications_count

 
    return render(request,"accounts/profile_update.html",context)


    

    

    








    

    

    
        
    






    







   


    

        



            















