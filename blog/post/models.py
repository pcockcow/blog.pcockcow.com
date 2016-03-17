from django.db import models
from django.utils import timezone


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200, primary_key=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    post_no = models.IntegerField(null=False)
    name = models.CharField(max_length=200)

class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    hits = models.IntegerField(default=0)