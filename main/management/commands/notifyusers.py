from django.core.management.base import BaseCommand, CommandError
from django.core import mail
from django.conf import settings

from main.models import UserProfile, Post, PostData

# In production grab this value from ALLOWED_HOSTS
HOSTED_IP = 'http://52.88.79.68/'
MESSAGE_SUBJECT = 'Notedrop Notifications'

class Command(BaseCommand):
    def handle(self, *args, **options):
        connection = mail.get_connection()
        connection.open()
        queue = []

        for user in UserProfile.objects.all():
            if user.user.email and user.notify_count > 0:
                recipient = []
                messages = []
                for post in Post.objects.filter(course__in=user.courses.all()):
                    post_data, created = PostData.objects.get_or_create(post=post, user=user.user)
                    if post_data.notified is not True and user.notify_count <= post.rating:
                        message = (
                            'Post related to {course} received {rating} upvote(s)'.format(course=post.course, rating=post.rating),
                            'URL: {host}posts/{postid}/'.format(host=HOSTED_IP, postid=post.pk)
                        )
                        message =  ' '.join(message)
                        messages.append(message)
                        post_data.notified = True
                        post_data.save()

                if messages:
                    message_body = '\n\n'.join(messages)
                    email = mail.EmailMessage(MESSAGE_SUBJECT, message_body, settings.EMAIL_HOST_USER, recipient, connection=connection)
                    queue.append(email)


        connection.send_messages(queue)
        connection.close()
