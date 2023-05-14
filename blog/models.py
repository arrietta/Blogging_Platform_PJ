from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', default='default_image.jpg')
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='John')
    surname = models.CharField(max_length=255, default='Doe')
    info = models.TextField(default='No information available')
    image = models.ImageField(upload_to='profile_images')
    posts = models.ManyToManyField(Post, related_name='profiles')


    def __str__(self):
        return f'{self.name} {self.surname}'














