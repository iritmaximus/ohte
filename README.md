# Ohte
![example workflow](https://github.com/iritmaximus/ohte/actions/workflows/build.yml/badge.svg)

## Project-idea
Leaderboard for a chess club. Program that calculates and displays ratings of
chess players in a chess club. The rating is counted based on game-results and
uses official [Elo](https://en.wikipedia.org/wiki/Chess_rating_system#Elo_rating_system) rating system.


## Documentation

* [changelog](./docs/changelog.md)
* [hours](./docs/hours.md)
* [instructions](./docs/instructions.md)
* [tests](./docs/tests.md)
* [requirements](./docs/requirements.md)
* [architecture](./docs/architecture.md)

### Note
The command to invoke tests is slightly different than the
example setup as I am using poe and not invoke.
The poetry shell environment must be entered first after which
the commands are

```bash
poetry shell
poe start
poe test
poe coverage-report
```
