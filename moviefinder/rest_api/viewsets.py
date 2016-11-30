import os
import json
import requests
from pprint import pprint
from django.http import JsonResponse
from rest_framework.response import Response
from django.db import transaction
from rest_api.models import Movie, SearchQuery, Trailer
from requests.exceptions import RequestException
from rest_framework.views import APIView
from rest_api.serializers import MovieSerializer
from rest_framework import generics,mixins,views
from django.db import IntegrityError


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONF_DIR = os.path.join(BASE_DIR,'conf')
CONF_FILE =  os.path.join(CONF_DIR,'settings.ini')
from configparser import ConfigParser
config = ConfigParser()
config.read(CONF_FILE)
myapifilms_token =  config.get('MYAPIFILMS', 'secret_key')



class SearchByTitle(APIView):
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)
        count = int(request.GET.get('count', 1))
        if query is None:
            return JsonResponse(json.dumps({}), safe=False, status=400)
        sid = transaction.savepoint()
        query = str(query).lower()
        try:
            movie_local = Movie.objects.filter(searchquery__query=query)
            imdbId = title = ""
            if not movie_local.exists():
                omdb_res = requests.get('http://www.omdbapi.com/?t=%s&y=&plot=full&r=json' % query)
                if  int(omdb_res.status_code) == 200:
                    omdb_res_json = omdb_res.json()
                    title = omdb_res.json()['imdbID']
                    imdbId = omdb_res_json['Title']
                else:
                    raise RequestException()
            else:
                title = movie_local[0].title
                imdbId = movie_local[0].imdbid
            query_db = SearchQuery(query=query)
            movie_db, created = Movie.objects.get_or_create(imdbid=imdbId,title=title)
            query_db.movie = movie_db
            if created or count > len(Trailer.objects.filter(movie=movie_db)):
                myapifilms_res = requests.get(
                    'http://www.myapifilms.com/trailerAddict/taapi?idIMDB=%s&token=%s&featured=&count=%d&credit=&format=json' %
                    (imdbId, myapifilms_token, count)).json()
                try:
                    trailers = myapifilms_res['data']['trailer']
                    for trailer in trailers:
                        try:
                            trailer_db = Trailer(movie=movie_db, embed=trailer['embed'])
                            trailer_db.save()
                        except IntegrityError:
                            #unique constraint violation
                            pass
                except KeyError as e:
                    pass
            query_db.save()
            transaction.savepoint_commit(sid)
            serializer = MovieSerializer(movie_db)
            return Response(serializer.data)
        except RequestException as e:
            print(e)
            print("Connection problem to external API")
            transaction.savepoint_rollback(sid)
        except KeyError as e:
            print(e)
            print("KeyError")
        return JsonResponse(json.dumps({}), safe=False, status=400)


class SearchByImdbId(APIView):

    def get(self, request, *args, **kwargs):
        imdbId = request.GET.get('query', None)
        count = int(request.GET.get('count', 1))
        if imdbId is None:
            return JsonResponse(json.dumps({}), safe=False, status=400)
        sid = transaction.savepoint()
        try:
            movie_local = Movie.objects.filter(searchquery__query=imdbId)
            pprint(movie_local)
            imdbId = title = ""
            if not movie_local.exists():
                omdb_res = requests.get('http://www.omdbapi.com/?i=%s&y=&plot=full&r=json' % imdbId)
                if int(omdb_res.status_code) == 200:
                    omdb_res_json = omdb_res.json()
                    title = omdb_res.json()['imdbID']
                    imdbId = omdb_res_json['Title']
                else:
                    raise RequestException()
            else:
                title = movie_local[0].title
                imdbId = movie_local[0].imdbid
            query_db = SearchQuery(query=imdbId)
            movie_db, created = Movie.objects.get_or_create(imdbid=imdbId, title=title)
            query_db.movie = movie_db
            if created or count > len(Trailer.objects.filter(movie=movie_db)):
                myapifilms_res = requests.get(
                    'http://www.myapifilms.com/trailerAddict/taapi?idIMDB=%s&token=%s&featured=&count=%d&credit=&format=json' %
                    (imdbId, myapifilms_token, count)).json()
                try:
                    trailers = myapifilms_res['data']['trailer']
                    for trailer in trailers:
                        try:
                            trailer_db = Trailer(movie=movie_db, embed=trailer['embed'])
                            trailer_db.save()
                        except IntegrityError:
                            # unique constraint violation
                            pass
                except KeyError as e:
                    pass
            query_db.save()
            transaction.savepoint_commit(sid)
            serializer = MovieSerializer(movie_db)
            return Response(serializer.data)
        except RequestException as e:
            print(e)
            print("Connection problem to external API")
            transaction.savepoint_rollback(sid)
        except KeyError as e:
            print(e)
            print("KeyError")
        return JsonResponse(json.dumps({}), safe=False, status=400)