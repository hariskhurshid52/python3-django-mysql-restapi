from django.db import models

# Create your models here.

class NewsAgency(models.Model):
    agency_name = models.CharField(max_length=64, blank=False, )
    website = models.CharField(max_length=60, blank=False, )
    code = models.CharField(max_length=60, blank=False, )
    date_time = models.DateTimeField(auto_now_add=True, blank=False, )
