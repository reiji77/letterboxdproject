import math
import numpy as np
import tmdbsimple as tmdb
tmdb.API_KEY = 'YOUR_TMDB_API_KEY'

def getTags(movieName):
    search = tmdb.Search()
    response = search.movie(query=movieName)
    if search.results:
        movie_id = search.results[0]['id']
        movie = tmdb.Movies(movie_id)
        details = movie.info()
        genres = details.get('genres', [])
        tags = [genre['name'] for genre in genres]
        return tags
    return []

def addDict(dct, key):
    if key in dct:
        dct[key] += 1
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
    print(cosine_similarity({"a": 5, "b": 4, "c": 5}, {"c": 5, "b": 4, "d": 6}))
