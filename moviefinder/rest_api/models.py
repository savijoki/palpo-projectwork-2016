from django.db import models

# Create your models here.

class Movie(models.Model):
    imdbId = models.CharField(max_length=32, blank=False, primary_key=True)
    title = models.CharField(max_length=256,  blank=False)

class Trailer(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,null=False)
    embed = models.TextField(blank=False)

class SearchQuery(models.Model):
    # save all queries in lower case
    query = models.CharField(max_length=256, blank=False)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,null=True)
    search_time = models.DateTimeField(auto_now_add=True)
