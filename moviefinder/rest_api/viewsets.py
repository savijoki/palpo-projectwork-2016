import os
import json
import requests
import logging
import traceback
from datetime import  timedelta
from django.db import transaction
from django.db.models import Count
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from requests.exceptions import RequestException
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_api.models import Movie, SearchQuery, Trailer
from rest_api.serializers import MovieSerializer

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONF_DIR = os.path.join(BASE_DIR,'conf')
CONF_FILE =  os.path.join(CONF_DIR,'settings.ini')
from configparser import ConfigParser
config = ConfigParser()
config.read(CONF_FILE)
myapifilms_token =  config.get('MYAPIFILMS', 'secret_key')


class QueryType:
    IMDBID = 0
    TITLE = 1


class SearchByTitle(APIView):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', None)
        count = int(request.GET.get('count', 1))
        if query is None:
            return JsonResponse(json.dumps({}), safe=False, status=400)
        movie_db = search_and_save_movie(query, count, QueryType.TITLE)
        if movie_db is not None:
            serializer = MovieSerializer(movie_db, trailer_amount=count)
            return Response(serializer.data)
        return JsonResponse(json.dumps({}), safe=False, status=404)


class SearchByImdbId(APIView):

    def get(self, request, *args, **kwargs):
        imdbId = request.GET.get('query', None)
        count = int(request.GET.get('count', 1))
        if imdbId is None:
            return JsonResponse(json.dumps({}), safe=False, status=400)
        movie_db = search_and_save_movie(imdbId, count, QueryType.IMDBID)
        if movie_db is not None:
            serializer = MovieSerializer(movie_db, trailer_amount=count)
            return Response(serializer.data)
        return JsonResponse(json.dumps({}), safe=False, status=404)


class SearchTopSearches(APIView):

    def get(self, request, *args, **kwargs):
        days = 30
        try:
            days = abs(int(request.GET.get('days', 30)))
        except ValueError as e:
            pass
        from_date = timezone.now() - timedelta(days=days)
        top_queries = SearchQuery.objects.filter(search_time__gt=from_date, movie__isnull=False)\
            .values('movie').annotate(sum=Count('query')).order_by('-sum')[:10]
        movie_list = []
        for query in top_queries:
            movie = Movie.objects.get(pk=int(query['movie']))
            movie_json = movie.minimal_as_json()
            movie_json['searches'] = query['sum']
            movie_json['days'] = days
            movie_list.append(movie_json)
        return JsonResponse(json.dumps(movie_list), safe=False)


def search_and_save_movie(query, count, type):
    retval  = None
    sid = transaction.savepoint()
    query = str(query).lower()
    try:
        movie_local = Movie.objects.filter(searchquery__query=query)
        movie_dict = {}
        imdbId = None
        if not movie_local.exists():
            url  = "http://www.omdbapi.com/?t=%s&y=&plot=full&r=json" % query
            if type is QueryType.IMDBID:
                url = "http://www.omdbapi.com/?i=%s&y=&plot=full&r=json" % query
            omdb_res = requests.get(url)
            if int(omdb_res.status_code) == 200:
                omdb_res_json = omdb_res.json()
                if omdb_res_json.get('Error'):
                    logger.warning("Movie not found!")
                    return None
                movie_dict['imdbId'] = omdb_res_json['imdbID']
                imdbId = movie_dict['imdbId']
                movie_dict['title'] = omdb_res_json['Title']
                movie_dict['poster'] = omdb_res_json['Poster']
                movie_dict['director'] = omdb_res_json['Director']
                movie_dict['writer'] = omdb_res_json['Writer']
                movie_dict['actors'] = omdb_res_json['Actors']
                movie_dict['genre'] = omdb_res_json['Genre']
                movie_dict['plot'] = omdb_res_json['Plot']
                movie_dict['runtime'] = omdb_res_json['Runtime']
                movie_dict['released'] = omdb_res_json['Released']
                movie_dict['imdbRating'] = omdb_res_json['imdbRating']
            else:
                raise RequestException()
        else:
            imdbId = movie_local[0].imdbId
        query_db = SearchQuery(query=query)
        movie_db, created = Movie.objects.get_or_create(imdbId=imdbId)
        if created:
            movie_db.title = movie_dict['title']
            movie_db.poster = movie_dict['poster']
            movie_db.director = movie_dict['director']
            movie_db.writer = movie_dict['writer']
            movie_db.actors = movie_dict['actors']
            movie_db.genre = movie_dict['genre']
            movie_db.plot = movie_dict['plot']
            movie_db.runtime = movie_dict['runtime']
            movie_db.released = movie_dict['released']
            movie_db.imdbRating = movie_dict['imdbRating']
            movie_db.imdbLink = "http://www.imdb.com/title/%s/" % imdbId
            movie_db.save()
        query_db.movie = movie_db
        if created or count > len(Trailer.objects.filter(movie=movie_db)):
            myapifilms_res = requests.get(
                'http://www.myapifilms.com/trailerAddict/taapi?idIMDB=%s&'
                'token=%s&featured=&count=%d&credit=&format=json' %
                (imdbId, myapifilms_token, count)).json()
            try:
                trailers = myapifilms_res['data']['trailer']
                for trailer in trailers:
                    try:
                        trailer_db = Trailer(movie=movie_db, trailerid=int(trailer['trailer_id']),
                                             embed=trailer['embed'])
                        trailer_db.save()
                    except IntegrityError:
                        # unique constraint violation
                        logger.info("Tried to add same trailer %d to db." % int(trailer['trailer_id']))
                    except (ValueError, KeyError):
                        # trailer_id wasn't integer or key didn't exists
                        logger.warning("Problem with myapifilms API. "
                                       "Didn't provide some key or tailerid wasn't integer.")
                        logger.warning(traceback.print_exc())
            except KeyError:
                logger.warning("Myapifilms API didn't provide trailer for imdbId: %s" % imdbId)
                logger.info(traceback.print_exc())
        query_db.save()
        transaction.savepoint_commit(sid)
        retval = movie_db
    except RequestException:
        logger.error("Connection problem between server and external API. Rolling back transactions.")
        logger.error(traceback.print_exc())
        transaction.savepoint_rollback(sid)
    except KeyError as e:
        logger.error("KeyError somewhere.")
        logger.error(traceback.print_exc())
    return retval
