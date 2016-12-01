from django.db import models



class Movie(models.Model):

    imdbid = models.CharField(max_length=32, blank=False, unique=True)
    title = models.CharField(max_length=256,  blank=False)

    def as_json(self):
        return dict(
            imdbid=self.imdbid,
            title=self.title
        )


class Trailer(models.Model):
    movie = models.ForeignKey(Movie, related_name='trailers', on_delete=models.CASCADE, null=False)
    trailerid = models.IntegerField(unique=True)
    embed = models.TextField(blank=False)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.embed

    class Meta:
        ordering = ['movie', 'added', 'trailerid']

class SearchQuery(models.Model):
    # save all queries in lower case
    query = models.CharField(max_length=256, blank=False)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,null=True)
    search_time = models.DateTimeField(auto_now_add=True)
