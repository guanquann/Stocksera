from django.db import models
from django.contrib.auth.models import User


class Preferences(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    wsb_trending = models.BooleanField(default=False)
    crypto_trending = models.BooleanField(default=False)
    government = models.BooleanField(default=False)
    insider = models.BooleanField(default=False)
    jim_cramer = models.BooleanField(default=False)
    earnings = models.BooleanField(default=False)
    short_vol = models.BooleanField(default=False)
    ctb = models.BooleanField(default=False)


class Watchlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=20, default="SPY")
