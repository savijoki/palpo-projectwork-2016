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
    embed = models.TextField(blank=False, unique=True)

    def __unicode__(self):
        return self.embed

class SearchQuery(models.Model):
    # save all queries in lower case
    query = models.CharField(max_length=256, blank=False)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,null=True)
    search_time = models.DateTimeField(auto_now_add=True)
