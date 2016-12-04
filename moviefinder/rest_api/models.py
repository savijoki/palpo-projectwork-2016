from django.db import models



class Movie(models.Model):

    imdbId = models.CharField(max_length=32, blank=False, unique=True)
    title = models.CharField(max_length=256)
    director = models.CharField(max_length=256)
    writer = models.CharField(max_length=256)
    actors = models.CharField(max_length=1024)
    poster = models.CharField(max_length=256)
    genre = models.CharField(max_length=256)
    runtime = models.CharField(max_length=256)
    released = models.CharField(max_length=32)
    plot = models.CharField(max_length=2048)
    imdbLink = models.CharField(max_length=256)
    imdbRating = models.CharField(max_length=3)

    def as_json(self):
        return dict(
            imdbId=self.imdbId,
            title=self.title,
            director=self.director,
            writer=self.writer,
            actors=self.actors,
            poster=self.poster,
            genre=self.genre,
            runtime=self.runtime,
            released=self.released,
            plot=self.plot,
            imdbLink=self.imdbLink,
            imdbRating=self.imdbRating
        )
    def minimal_as_json(self):
        return dict(
            imdbId=self.imdbId,
            title=self.title,
            poster=self.poster,
            imdbLink=self.imdbLink,
            imdbRating=self.imdbRating
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
