from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    courses = models.ManyToManyField('Course', db_table='enrolled_courses')
    schools = models.ManyToManyField('School', db_table='enrolled_schools')
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)


class Course(models.Model):
    school = models.ForeignKey('School')

    designator = models.CharField(max_length=3)
    number = models.CharField(max_length=3)
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=8, blank=True, null=True)

    def __unicode__(self):
        return '{0} {1} {2}'.format(self.designator, self.number, self.name)


class School(models.Model):
    name = models.CharField(max_length=50)
    state = models.CharField(max_length=25)
    city = models.CharField(max_length=25)
    # TODO add image field for college stamp, stamp will be gotten via API

    def __unicode__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User)
    course = models.ForeignKey('Course')

    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    # TODO add field for uploaded media (docs, pictures, etc.)

    def __unicode__(self):
        if len(self.content) > 30:
            return "{0}..".format(self.content[:30])
        else:
            return self.content


class PostData(models.Model):
    post = models.ForeignKey('Post')
    user = models.ForeignKey(User)

    upvote = models.BooleanField(default=False)
    downvote = models.BooleanField(default=False)
    noted = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

# property to get related UserProfile from a User
User.profile = property(lambda user_id: UserProfile.objects.get_or_create(user=user_id)[0])
