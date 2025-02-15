from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField


# Create your models here.

class UserProfile(models.Model):
    '''
    Model for the User profile
    contains the username, email, password, login, last_login and date_joined
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    '''
    Additional attribute for the user
    1: Profile pic
    2: Title: Will add later
    '''
    forum_email = models.EmailField(unique=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return "@{}".format(self.user.username)


class Section(models.Model):
    title = models.CharField(max_length=265, blank=False, null=False)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.title


class SubSection(models.Model):
    title = models.CharField(max_length=355, blank=False, null=False)
    description = models.CharField(max_length=500)
    section = models.ForeignKey(Section, related_name='section', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def latestpost(self):
        return self.subsection.order_by('-created_date')


class Posts(models.Model):
    title = models.CharField(max_length=355)
    created_date = models.DateTimeField(default=timezone.now())
    last_update = models.DateTimeField(default=timezone.now())
    subsection = models.ForeignKey(SubSection, related_name='subsection', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.DO_NOTHING)

    def get_absolute_url(self):
        pass

    def latestcomment(self):
        return self.post.order_by('-created_date')


class Comments(models.Model):
    post = models.ForeignKey(Posts, related_name='post', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, related_name='userProfile', on_delete=models.DO_NOTHING)
    created_date = models.DateTimeField(default=timezone.now())
    last_update = models.DateTimeField(default=timezone.now())
    content = RichTextField()
