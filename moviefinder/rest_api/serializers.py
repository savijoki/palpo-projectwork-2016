from rest_framework import serializers
from rest_api.models import Movie, Trailer
from pprint import pprint


class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trailer
        fields = ('embed',)


class MovieSerializer(serializers.ModelSerializer):
    trailers = serializers.SerializerMethodField()
    
    def __init__(self, movie, *args, trailer_amount, **kwargs):
        super(MovieSerializer, self).__init__(movie, *args, **kwargs)
        self.movie = movie
        self.trailer_amount=trailer_amount

    def get_trailers(self,obj):
        query = Trailer.objects.filter(movie=self.movie)[:self.trailer_amount]
        serializer = TrailerSerializer(query, many=True)
        return serializer.data

    class Meta:
        model = Movie
        depth = 1
        fields = ('title', 'imdbid', 'trailers',)



