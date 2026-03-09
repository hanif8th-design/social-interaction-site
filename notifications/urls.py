from django.urls import path
from notifications.views import NotificationListView,MarkAsReadView,mark_all_read

app_name = 'notifications'

urlpatterns = [
    path('notification-list/',NotificationListView.as_view(),name = 'notification-list'),
    path('mark-as-read/<int:pk>/',MarkAsReadView,name = 'mark_as_read'),
    path('mark-all-unread/',mark_all_read,name = 'mark_all_read'),



]
