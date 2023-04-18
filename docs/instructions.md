# Using the app

## Installation

Make sure you have at least `python>=3.10` and `poetry>=1.4` installed
After that run

```bash
poetry install
```

## Using the project
### API
After running
```bash
uvicorn src.api:app
```
the api can be found at `localhost:8000/api`.
All of the api paths can be found in [architecture](./architecture.md).



#### Note
Add `--reload` flag to the uvicorn command to "hot-reload" the api while making changes


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
