# Using the app

## Installation

After cloning this repo
make sure you have at least `python>=3.10`, `poetry>=1.4` `docker>=20.10.23` and `docker-compose>=1.29.2` installed.
They can be installed from `apt`.
After that run

```bash
poetry install
```

### Env
Move the contents of `.env.example` to a new `.env` file in the project root.

## Using the project

### Database

This project utilizes `postgres` (also known as `postgresql`) as it's database.
The `postgres` instance contains two databases, one for production and the other for tests.
They can be named freely.

You have two options. You can use the provided `docker-compose.yaml` to use the database or create the two 
databases yourself.

#### Using docker-compose

If you are able to install `docker` and `docker-compose`, this method would be a lot easier to set up.
All you need to do after installing the project and the two `docker` executables is run
```bash
poe database
```
and the databases will be created and run, the "production" database at port `6432` (because `5432` is the default port
for postgres and is usually already taken) and for the "test" database at port `7432`.

If the database doesn't seem to update changes you have made to some file, run
```bash
poe database-remove
```
and it will recreate the databases from scratch. Note that YOU WILL LOSE YOUR DATA IN THE DATABASE.


#### Create them yourself

Before you can use the app you need to have an postgres user with permissions to use the previously
mentioned databases.

[More details can be found here.](./postgres.md)


### Env-file

Environment variables are configured by an `.env` file placed in the projects root (NOT `src`~~!!). This file contains all of the "secret" values, for example the database url.
The file contains three variables:
* `POSTGRES_URL`
* `TEST_POSTGRES_URL`
* `ENV`


The values should be:
* `POSTGRES_URL` is the postgres database connection string that contains the username, password, hostname, port number and database name.
This variable is used for the "production" database. The database name needs to be `ohte`
[More information about the url string](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)
* `TEST_POSTGRES_URL` is same format as the former `POSTGRES_URL`. This is used as the "test" database. The database name needs to be `test_ohte`.
* `ENV` is the environment the app is wanted to be run as, for example "production" or "development"

#### Note
If you are using the `docker-compose` to run the databases, use the variables provided in the `.env.example`.

### API
After running
```bash
$ uvicorn src.api:app
```
the api can be found at `localhost:8000/api`.
All of the api paths can be found in [architecture](./architecture.md).



#### Note
Add `--reload` flag to the uvicorn command to "hot-reload" the api while making changes or use
the command `poe dev`.


### The chess rating calculations

Project can be run by importing class `ChessRating` from `chess.py`
and invoking
```python
Chessrating(white_rating, black_rating)
```
where rating is the elo of a player (see elo in the beginning of README).


User can then invoke
```python
rating = ChessRating(x, y)
rating.game_result(1,0)
```
to indicate who has won the game, white or black (white is the first parameter).
A draw is also possible and that is denoted by giving both sides the parameter
1/2 or 0.5. The new rating is calculated when the game result
is given.

It is now possible to query the current rating of both sides by
accessing the property white or black of the class object
```python
print(rating.white)
print(rating.black)
```
