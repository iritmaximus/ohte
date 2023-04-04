# Tests

## How to run tests

After installation tests can be run by first entering the
poetry shell environment with
```bash
poetry shell
```
and then invoking the script
```bash
poe test_full
```

After that the coverage report is available in `htmlcov` in the
root of the project (which can be opened by `poe openhtml` if you have firefox).
