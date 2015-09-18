from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    courses = models.ManyToManyField('Course', db_table='enrolled_courses')
    notify_count = models.PositiveIntegerField(default=0)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)


class Course(models.Model):
    school = models.ForeignKey('School')

    designator = models.CharField(max_length=3)
    number = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

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
    # TODO rename this to Note
    author = models.ForeignKey(User)
    
    course = models.ForeignKey('Course')
    content = models.TextField()
    image = models.ImageField(upload_to='imgs/', blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    # TODO add field for uploaded media (docs, pictures, etc.)

    def __unicode__(self):
        if len(self.content) > 200:
            return "{0}..".format(self.content[:200])
        else:
            return self.content

    @property
    def rating(self):
        count = 0
        for p in PostData.objects.filter(post=self):
            if p.upvote is True:
                count += 1
            elif p.upvote is False:
                count -= 1
        return count

class PostData(models.Model):
    # TODO rename this to NoteData
    post = models.ForeignKey('Post')
    user = models.ForeignKey(User)

    upvote = models.NullBooleanField(default=None)
    noted = models.NullBooleanField(default=False)
    notified = models.NullBooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

# property to get related UserProfile from a User
User.profile = property(lambda user_id: UserProfile.objects.get_or_create(user=user_id)[0])
