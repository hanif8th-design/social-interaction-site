from celery import shared_task
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from notifications.models import Notification
from tweets.models import Tweet



@shared_task
def create_notification(recipient_username,actor_username,verb,object_id):
    try:
        recipient = User.objects.get(username=recipient_username)
        actor = User.objects.get(username=actor_username)
        content_type = ContentType.objects.get_for_model(Tweet)
        object_id = object_id
        verb = verb

        if recipient != actor:


            Notification.objects.create(
                recipient = recipient,
                actor = actor,
                verb=verb,
                content_type = content_type,
                object_id = object_id,
                read = False

            )
    except User.DoesNotExist:
        # If either user does not exist, silently fail
        pass


@shared_task
def create_follow_notification(recipient_username,actor_username,verb,object_id):
    try:
        recipient = User.objects.get(username = recipient_username)
        actor = User.objects.get(username = actor_username)
        content_type = ContentType.objects.get_for_model(User)
        object_id = object_id
        read = False

        Notification.objects.create(
                recipient = recipient,
                actor = actor,
                verb=verb,
                content_type = content_type,
                object_id = object_id,
                read = False

            )
    except User.DoesNotExist:
        # If either user does not exist, silently fail
        pass









        

