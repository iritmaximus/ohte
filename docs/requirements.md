# Requirements

## Components

### Main components
* Chess rating calculator
* DB interface
* RESTful API to access all data
* Authentication (tokens?)

### Add-on components
* Choose one to interact with data
    - Telegram bot
    - Local gui app
    - web frontend
* Analyze games

### List of all possible components (main and add-on)

* An API-like functionality so integration is easier to both graphical ui and web ui.
* Graphical user interface.
* Backend server API
* Database to store games/ratings
* Uses async/await
* Possible to save all moves of a game
* Integrate [stockfish](https://github.com/official-stockfish/Stockfish) (chess-engine) to analyze games that have moves
* Analyze openings
* Include the db things in the ui -> for ex. show list of all games
* Add ui to play games of chess
* Telegram bot to work as the interface to add/edit games + other things
* Many user roles to limit the rights of users

## User
For now the project will only have one general user role. Later
on it is possible to add more, for example, admin roles and such.
