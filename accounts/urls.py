from django.urls import path,reverse_lazy
from accounts.views import (
    login_view,
    register_view,
    HomeView,
    logout_view,
    CustomPasswordResetView,
    CustomPasswordChangeView,
    FollowView,
    FollowerListView,
    FollowingListView,
    unfollow_user,
    SearchUserView,
    ProfileDetailView,
    ProfileUpdateView,
    )

from django.contrib.auth import views as auth_views


app_name = 'accounts'


urlpatterns = [
    path('',HomeView.as_view(),name = "home"),
    path('login/',login_view,name = "login"),
    path('register/',register_view,name = 'register'),
    path('logout/',logout_view,name = 'logout'),
    path('password-change/',CustomPasswordChangeView.as_view(),name = 'password-change'),
    path('<int:pk>/follow/',FollowView,name = 'follow'),
    path('<int:pk>/followers',FollowerListView.as_view(),name = "followers"),
    path('<int:pk>/followings',FollowingListView.as_view(),name = "followings"),
    path('<int:pk>/unfollow-user',unfollow_user,name = "unfollow_user"),
    path('search/', SearchUserView.as_view(), name='search_user'),
    path('<int:pk>/details-user/',ProfileDetailView.as_view(), name='profile-detail'),
    path('profile-update/',ProfileUpdateView, name='profile-update'),




    
    


    #password reset urls
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    
    # Password reset done (check your email page)
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='accounts/password_reset_done.html'
        ),
        name='password_reset_done'
    ),

    # Password reset confirm (set new password page)
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/password_reset_confirm.html',
            success_url=reverse_lazy('accounts:password_reset_complete')  # URL of CompleteView
        ),
        name='password_reset_confirm'
    ),

    #  Password reset complete (success page)
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='accounts/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),

    






]
