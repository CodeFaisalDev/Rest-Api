from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# Create your models here.
class Stream(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    website = models.URLField()

    def __str__(self):
        return self.name
    
class WatchList(models.Model):
    title = models.CharField(max_length=100)
    storyline = models.TextField(max_length=200)
    active = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    average_review = models.FloatField(default=0)
    review_count = models.IntegerField(default=0)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE, default=None, related_name = "watchlist")

    def __str__(self):
        return self.title
    

class Review(models.Model):
    review_user  = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    watchlist = models.ForeignKey(WatchList, on_delete=models.CASCADE, related_name='reviews')

    def __str__(self):
        return str(self.rating) + ' | ' + self.watchlist.title
    