from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField(default=' ')
    image = models.ImageField(upload_to='post_images/', default='default_image.jpg')
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='John')
    surname = models.CharField(max_length=255, default='Doe')
    info = models.TextField(default='No information available')
    image = models.ImageField(upload_to='profile_images' ,default='default_image.jpg')
    posts = models.ManyToManyField(Post, related_name='profiles')
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    following = models.ManyToManyField(User, related_name='followers', blank=True)

    def follow(self, user):

        self.following.add(user)

    def __str__(self):
        return f'{self.name} {self.surname}'














