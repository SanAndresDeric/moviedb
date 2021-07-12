from flask import Flask, render_template
from flask_restful import request, abort, Api, Resource

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

api = Api(app)

MOVIES = {
    1 : {"id" : 1, "title" : "The Shawshank Redemption", "release_year" : 1994, "genre" : "Drama"},
    2 : {"id" : 2, "title" : "The Godfather", "release_year" : 1972, "genre" : "Crime"},    
    3 : {"id" : 3, "title" : "The Dark Knight", "release_year" : 2008, "genre" : "Action"}    
}

## MovieList
# GET  : Returns a list of all movies in JSON format:
#        {
#            "data" : [
#                         { "id" : 1, ... },
#                         { "id" : 2, ... }
#                     ]
#        } 
# POST : Adds new movie. If successful, returns:
#        { 
#             "id"           : <ID>,
#             "title"        : <TITLE>,
#             "release_year" : <YEAR>,
#             "genre"        : <GENRE>     
#        }

class MovieList(Resource):
    def get(self):
        movie_list = [ movie_data for id, movie_data in MOVIES.items()]
        response_data = { "data" : movie_list }
        return response_data

    
    def post(self):
        request_data = request.get_json(force=True)

        if not request_data \
           or not 'title' in request_data \
           or not 'release_year' in request_data \
           or not 'genre' in request_data:

           abort(400)

        new_movie_id = int(max(MOVIES.keys())) + 1
        new_movie = {
            "id" : new_movie_id,
            "title" : request_data["title"],
            "release_year" : request_data["release_year"],
            "genre" : request_data["genre"]
        }

        MOVIES[new_movie_id] = new_movie

        return new_movie, 201

# Set up the API resource routing:
api.add_resource(MovieList, '/api/movies')

if __name__ == '__main__':
    app.run(debug=True)       
