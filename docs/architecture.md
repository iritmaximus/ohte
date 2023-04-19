# Architecture

This contains all the higher-level explanations of the different
parts of this project. All the single-function documentation
is already in the docstrings of the funcs so therefore I don't
"crosspost" those here.

## Structure

### Chess
The `chess` takes care of the rating calculations of players. It
can calculate new ratings of two players after a played game
depending on the result.


```mermaid
 classDiagram
      class ChessRating{
          white
          black
      }
```
`ChessRating` uses few helper functions to calculate the final
rating.
* `expected_scores()`
* `calculate_chess_rating(white_adjustment, black_adjustment)`

These functions are called by the `game_result()` method.
* `expected_scores()` calculates the likelihood of each player
winning that is needed for the final formula to calculate the ratings.
The expected score is based on the rating difference.

> "It then follows that for each 400 rating points of advantage over
the opponent, the expected score is magnified ten times in
comparison to the opponent's expected score." ~[Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system#Mathematical_details)

* `calculate_chess_rating(white_adjustment, black_adjustment)`
calculates the rating with the expected score. More information
about the formula can be found from [wikipedia](https://en.wikipedia.org/wiki/Elo_rating_system#Theory).
The adjustment values mentioned in the parameters are the amount
the rating is wanted to change per one game. In this project at
the moment the value is `24` when according to the formula
$K=16$ is for masters and $K=32$ is for weaker players.




### Config
The `config` takes care of the environment variables. It reads the `.env` file in the root of the project for `POSTGRES_URL`,
`TEST_POSTGRES_URL` and `ENV`. These can be used by invoking the functions
* `db_url()`
* `env()`

The `TEST_POSTGRES_URL` is reserved for test mocking.
The environment variables can be used with `from src import config` and then accessing the functions with `config.`. prefix.

### Database
The `db.py` handles the interaction with the database. All queries are implemented as functions in this file.
More details about the queryfunctions can be found from the docstrings.


The most important function however is the `create_db_connection(engine)`.
The function returns a connection to the database that can be then
used to query it. It needs an `sqlalchemy` engine (created with `sqlalchemy.create_engine()`, see sqlalchemy docs).
In this project the engine is created in `__init__.py`.

###

## API
Project uses `fastapi` to serve the data as an api over `http` for
easy access. With this implementation the api can be used as
a backend to a frontend app.

### Paths

Only users path is functional by now, others are placeholders.

#### /api/users

* GET [localhost:8000/api/users](http://localhost:8000/api/users) returns all users in the database with their `id`, `username` and `rating`
* POST [localhost:8000/api/users](http://localhost:8000/api/users) adds user given in the request body, ex. {"username": "<wanted_name>", "rating": <int>}
* GET [localhost:8000/api/users/<user_id>](http://localhost:8000/api/users/<user_id>) returns same data but of one user (selected by id)

#### /api/rating

* GET [localhost:8000/api/rating](http://localhost:8000/api/rating) returns all users in the database with their `id`, `username` and `rating` *sorted by their rating*
* GET [localhost:8000/api/rating/<user_id>](http://localhost:8000/api/rating/<user_id>) returns the rating of the user with corresponding id

#### /api/chess

* GET [localhost:8000/api/chess](http://localhost:8000/api/chess) returns all games in the database

#### /api/search
This is purely an idea, could possibly be dropped at any moment

* GET [localhost:8000/api/search](http://localhost:8000/api/search) ability to search the games or users somehow, dont know yet.
* GET [localhost:8000/api/search/user/<username>](http://localhost:8000/api/search/user/<username>) search users by username
