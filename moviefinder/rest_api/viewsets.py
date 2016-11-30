import os
import json
import requests
from pprint import pprint
from django.http import JsonResponse
from django.db import transaction
from rest_api.models import Movie, SearchQuery, Trailer
from requests.exceptions import RequestException

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONF_DIR = os.path.join(BASE_DIR,'conf')
CONF_FILE =  os.path.join(CONF_DIR,'settings.ini')
from configparser import ConfigParser
config = ConfigParser()
config.read(CONF_FILE)
myapifilms_token =  config.get('MYAPIFILMS', 'secret_key')


def SearchQueryHandler(request, *args, **kwargs):
    response_json = {}
    query = request.GET.get('query', None)
    count = request.GET.get('count', 1)
    sid = transaction.savepoint()
    if query is None:
        return JsonResponse(json.dumps(response_json), safe=False, status=400)
    query = str(query).lower()
    try:
        omdb_res = requests.get('http://www.omdbapi.com/?t=%s&y=&plot=full&r=json' % query)
        omdb_res_json = omdb_res.json()
        query_db = SearchQuery(query=query)
        if int(omdb_res.status_code) == 200:
            response_json.update(omdb_res_json)
            imdbId = omdb_res_json['imdbID']
            title = omdb_res_json['Title']
            movie_db = Movie(title=title, imdbId=imdbId)
            movie_db.save()
            query_db.movie = movie_db
            myapifilms_res = requests.get(
                'http://www.myapifilms.com/trailerAddict/taapi?idIMDB=%s&token=%s&featured=&count=%s&credit=&format=json' %
                (imdbId, myapifilms_token, count)).json()
            try:
                trailers = myapifilms_res['data']['trailer']
                response_json['trailers'] = trailers
                for trailer in trailers:
                    trailer_db = Trailer(movie=movie_db,embed=trailer['embed'])
                    trailer_db.save()
            except KeyError as e:
                # add empty array
                response_json['trailers'] = []
    except RequestException as e:
        print(e)
        print("Connection problem to external API")
        transaction.savepoint_rollback(sid)
    else:
        query_db.save()
        transaction.savepoint_commit(sid)
    return JsonResponse(json.dumps(response_json), safe=False)