from django.db import models


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=70, blank=False, default='')
    username = models.CharField(max_length=200, blank=False, default='')
    password = models.CharField(max_length=200, default=False)
    added_date = models.DateTimeField(auto_now_add=True, blank=False, )


class NewsStories(models.Model):
    headline = models.CharField(max_length=64, blank=False, )
    category = models.CharField(max_length=60, blank=False, )
    region = models.CharField(max_length=60, blank=False, )
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=False, )
    date_time = models.DateTimeField(auto_now_add=True, blank=False, )
    details = models.CharField(max_length=512, blank=False, )
