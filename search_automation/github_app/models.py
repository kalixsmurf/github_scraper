from django.db import models

# Create your models here.
class user(models.Model):
    username = models.CharField(max_length=150)
    nickname = models.CharField(max_length=150)
    biography = models.CharField(max_length=150)
    organization = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    profile_website = models.CharField(max_length=150)
    twitter_account = models.CharField(max_length=150)
    popular_repositories = models.CharField(max_length=150)
    all_repositories = models.CharField(max_length=150)

