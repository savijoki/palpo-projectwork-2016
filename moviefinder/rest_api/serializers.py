from rest_framework import serializers
from rest_api.models import Movie, Trailer


class TrailerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trailer
        fields = ('embed',)


class MovieSerializer(serializers.ModelSerializer):
    trailers = TrailerSerializer(many=True)

    class Meta:
        model = Movie
        depth = 1
        fields = ('title', 'imdbid', 'trailers',)



