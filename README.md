# Ohte
![example workflow](https://github.com/iritmaximus/ohte/actions/workflows/build.yml/badge.svg)

## Project-idea
Leaderboard for a chess club. Program that calculates and displays ratings of
chess players in a chess club. The rating is counted based on game-results and
uses official [Elo](https://en.wikipedia.org/wiki/Chess_rating_system#Elo_rating_system) rating system.

### List of possible components

* An API-like functionality so integration is easier to both graphical ui and web ui.
* Graphical user interface.
* Backend server API
* Database to store games/ratings
* Possible to save all moves of a game
* Integrate [stockfish](https://github.com/official-stockfish/Stockfish) (chess-engine) to analyze games that have moves
* Analyze openings
* Include the db things in the ui -> for ex. show list of all games
* Add ui to play games of chess
* Telegram bot to work as the interface to add/edit games + other things


## Documentation

### Architecture

#### Main components
* Chess rating calculator
* DB interface
* RESTful API to access all data
* Authentication (tokens?)

#### Add-on components
* Choose one to interact with data
    - Telegram bot
    - Local gui app
    - web frontend
* Analyze games

## Using the app

### Installation
### Running
### Tests
