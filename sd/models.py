from rest_framework.authtoken.models import Token
from django.db import models
from django.contrib.auth.models import AbstractUser
import social_distribution.settings as settings
import socket

from uuid import uuid4


class Node(models.Model):
    hostname = models.URLField(primary_key=True, default=settings.HOSTNAME)
    server_name = models.CharField(max_length=100)
    server_password = models.CharField(max_length=100)


class Author(AbstractUser):
    # Using username, password, first_name, last_name, email from AbstractUser
    host = models.ForeignKey(Node,
                             on_delete=models.CASCADE, default=settings.HOSTNAME, db_column='host')
    uuid = models.CharField(max_length=200,
                            primary_key=True, default=uuid4, editable=False, unique=True)
    displayName = AbstractUser.username
    github = models.CharField(max_length=100, blank=True)
    bio = models.CharField(max_length=500, blank=True)
    verified = models.BooleanField(default=False)


class Post(models.Model):
    title = models.CharField(max_length=100)
    source = models.CharField(default=settings.HOSTNAME, max_length=100)
    origin = models.CharField(default=settings.HOSTNAME, max_length=100)
    description = models.CharField(default="", max_length=100, blank=True)
    contentTypeChoices = [("text/markdown",     'text/markdown'),
                          ("text/plain",        'text/plain'),
                          ("application/base64", 'application/base64'),
                          ("image/png;base64",  'image/png;base64'),
                          ("image/jpeg;base64", 'image/jpeg;base64')]
    contentType = models.CharField(max_length=30)
    # TODO: TEMPORARY, how to do multiple content types?
    content = models.CharField(default="", max_length=5000, blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # TODO: comma separated values for now?
    categories = models.CharField(default="", max_length=100, blank=True)
    published = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True)
    visibilityChoices = [("PUBLIC",     "Public"),
                         ("FOAF",       "Friends of Friends"),
                         ("FRIENDS",    "Friends"),
                         ("PRIVATE",    "Private"),
                         ("SERVERONLY", "Local Friends")]
    visibility = models.CharField(max_length=30, choices=visibilityChoices)
    visibleTo = models.CharField(max_length=10000000, blank=True)
    unlistedChoices = [(False, "Listed"), (True, "Unlisted")]
    unlisted = models.BooleanField(max_length=30, choices=unlistedChoices)

    # TODO: update url with the post id and correct path based on api
    image = models.ImageField(blank=True)
    link_to_image = models.CharField(max_length=100000, blank=True)
    host = models.ForeignKey(Node,
                             on_delete=models.CASCADE, default=settings.HOSTNAME, db_column='host')


class Comment(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    contentTypeChoices = [("text/markdown",     'text/markdown'),
                          ("text/plain",        'text/plain')]
    contentType = models.CharField(max_length=30, choices=contentTypeChoices)
    published = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post')


class FriendRequest(models.Model):
    class Meta:
        unique_together = (('to_author', 'from_author'),)
    to_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="to_author")
    from_author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="from_author")
    date = models.DateTimeField(auto_now_add=True)


class Follow(models.Model):
    class Meta:
        unique_together = (('follower', 'following'),)
    follower = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name="following")
    date = models.DateTimeField(auto_now_add=True)


class Friend(models.Model):
    class Meta:
        unique_together = (('author', 'friend'),)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='author')
    friend = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='friend')
