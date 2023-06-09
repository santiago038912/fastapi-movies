from fastapi import APIRouter
from typing import List, Optional
from config.database import Session
from models.movie import Movie as MovieModel
from pydantic import BaseModel, Field
from fastapi import Path, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from middleware.JWTBearer import JWTBearer
import uuid

from service.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()

@movie_router.get('/movies', tags=['movies'], response_model=List[Movie], status_code=200, dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    db = Session()
    result = MovieService(db).get_movies()
    
    return JSONResponse(content=jsonable_encoder(result, exclude_unset=False), status_code=200)

@movie_router.get('/movies/{id}',tags=['movies'])
def get_movie_by_id(id: str = Path(max_length=50, min_length=22)):

    db = Session()

    result = MovieService(db).get_movie_by_id(id)

    if not result:
        return JSONResponse(content={"message":"id does not exist"}, status_code=404)
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    

@movie_router.get('/movies/category/', tags=['movies'], response_model=List[Movie])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:

    db = Session()

    result = MovieService(db).get_movies_by_category(category)

    if not result:
        return JSONResponse(content={"message":"category does not exist"}, status_code=404)
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/movies/title/', tags=['movies'], response_model=List[Movie])
def get_movies_by_title(title: str = Query(min_length=3, max_length=30)) -> List[Movie]:
    db = Session()

    result = MovieService(db).get_movies_by_title(title)

    if not result:
        return JSONResponse(content={"message":"title does not exist"}, status_code=404)
    
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


# POST

@movie_router.post('/movies',tags=['movies'],)
def create_movie(movie: Movie):
    
    # id_exists = utils.if_id_exists(movies, movie.id)

    db = Session()

    MovieService(db).create_movie(movie)

    return JSONResponse(content={"message":"movie registered"}, status_code=201)
    
# PUT

@movie_router.put('/movies/{id}',tags=['movies'])
def update_movie_by_id(id: str, movie: Movie):

    db = Session()

    result = MovieService(db).get_movie_by_id(id)

    if not result:
        return JSONResponse(content={"message": "id does not exist"}, status_code=404)
    
    MovieService(db).update_movie_by_id(id, movie)

    return JSONResponse(content={"message": "movie updated"}, status_code=200)
    
# DELETE
    
@movie_router.delete("/movies/{id}", tags=['movies'])
def delete_movie_by_id(id: str):

    db = Session()

    result = MovieService(db).get_movie_by_id(id)

    if not result:
        return JSONResponse(content={"message": "id does not exist"}, status_code=404)
    
    MovieService(db).delete_movie_by_id(id)
    
    return JSONResponse(content={"message": "movie deleted"}, status_code=200)