import math
import numpy as np
import tmdbsimple as tmdb
tmdb.API_KEY = '3b21b61580c17301dc3a24426ad738e9'
import time
import pandas as pd
import userData
from collections import Counter

def createTasteProfile(movies):
    tasteDict = {}
    for movie in movies:
        tempDict1 = getDict(movie[0], movie[1])
        tempDict2 = tasteDict
        tasteDict = dict((Counter(tempDict1) + Counter(tempDict2)))
    return tasteDict

def getDict(movieName, rating):
    search = tmdb.Search()
    response = search.movie(query=movieName)
    dict = {}
    if search.results:
        movie_id = search.results[0]['id']
        movie = tmdb.Movies(movie_id)
        keywords = movie.keywords()['keywords']
        details = movie.info()
        genres = details.get('genres', [])
        cast = [cast_member['name'] for cast_member in movie.credits().get('cast', [])[:5]]
        director = [crew_member['name'] for crew_member in movie.credits().get('crew', []) if crew_member['job'] in ['Director']]
        tags = [keyword['name'] for keyword in keywords] +[genre['name'] for genre in genres]
        for feature in director + tags + cast:
            addDict(dict, feature, rating)
        return dict
    return None

def addDict(dct, key, rating):
    if key in dct:
        dct[key] += 1*rating
    else:
        dct[key] = 1*rating
    return dct

def norma(dct):
    return math.sqrt(sum(x*x for x in dct.values()))
        
def cosine_similarity(dict_1, dict_2):
    intersecting_keys = list(dict_1.keys() & dict_2.keys())
    List1 = list(dict_1[k] for k in intersecting_keys)
    List2 = list(dict_2[k] for k in intersecting_keys)
    similarity = np.dot(List1,List2) / (norma(dict_1) * norma(dict_2))
    return round(similarity, 2)

if __name__ == '__main__':
    cnx, cursor = userData.init_db()
    userData.get_movies(1, cursor)
    tasteDict = createTasteProfile(userData.get_movies(1, cursor))
    print(tasteDict)