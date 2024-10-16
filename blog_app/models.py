from django.db import models
from datetime import datetime


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20)

class Post(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=100000000)
    post_by = models.CharField(max_length=70)
    posted_on = models.DateTimeField(datetime)
    img_link = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(datetime)
    posted_by = models.CharField(max_length=70)

