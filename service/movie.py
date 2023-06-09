from models.movie import Movie as MovieModel
from schemas.movie import Movie
import uuid

class MovieService():
    def __init__(self, db) -> None:
        self.db = db

    def get_movies(self):
        result = self.db.query(MovieModel).all()
        return result
    
    def get_movie_by_id(self, id: str):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()
        return result
    
    def get_movies_by_category(self, category: str):
        result = self.db.query(MovieModel).filter(MovieModel.category == category).all()
        return result
    
    def get_movies_by_title(self, title: str):
        result = self.db.query(MovieModel).filter(MovieModel.title == title).all()
        return result
    
    def create_movie(self, movie: Movie):

        movie.id = str(uuid.uuid4())
        newMovie = MovieModel(**movie.dict())

        self.db.add(newMovie)
        self.db.commit()

        return
    
    def update_movie_by_id(self, id: str, movie: Movie):
        result = self.db.query(MovieModel).filter(MovieModel.id == id).first()

        result.title = movie.title if movie.title else result.title
        result.overview = movie.overview if movie.overview else result.overview
        result.year = movie.year if movie.year else result.year
        result.rating = movie.rating if movie.rating else result.rating
        result.category = movie.category if movie.category else result.category

        self.db.commit()
        return
    
    def delete_movie_by_id(self, id: str):

        self.db.query(MovieModel).filter(MovieModel.id == id).delete()
        self.db.commit()
        return
