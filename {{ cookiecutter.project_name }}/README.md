# Cobrademo

## Prerequisites
- [pyenv](https://github.com/pyenv/pyenv) (recommended)

## Project Structure

```bash
root/
 |-- dags/
 |   |-- project.py
 |-- src/
 |   |-- project/
 |   |-- |-- common/
 |   |-- |-- |-- spark.py
 |   |-- |-- jobs/
 |   |-- |-- transformations/
 |   |-- app.py
 |-- tests/
 |   |-- common/
 |   |-- | -- spark.py
 |   Dockerfile
 |   setup.py
```

The main Python module contains the ETL job `app.py`. By default `app.py` accepts a number of arguments:
- `--date` the execution date
- `--env` the environment we are executing in
- `--jobs` one or more jobs that needs to be executed

## Concepts

### Pin your python dependencies
In building your Python application and its dependencies for production, you want to make sure that your builds are predictable and deterministic.
 Therefore, always pin your dependencies. You can read more in the article: [Better package management](https://nvie.com/posts/better-package-management/)
When using pip-tools to manage dependencies, you define your dependencies in the `requirements.in` file.
This file can then be compiled into the `requirements.txt` file by running the command `pip-compile requirements.in` from your shell.

This compilation step makes sure every dependency gets pinned in the `requirements.txt` file,
ensuring that project won't break because of transitive dependencies being silently updated.
When a dependency does need to be updated, you can update the `requirements.in` file and re-compile it.
With this method, package updates always happen as a conscious decision by the developer.

The `pip-compile` command should be run from the same virtual environment as your project so conditional dependencies that require a specific Python version,
or other environment markers, resolve relative to your project's environment.

### Separate job breakdown from scheduling
Jobs can be found in the `jobs/` directory. A job function needs to be annotated with `@entrypoint("name")` and
the module needs to be imported in `app.py`. This approach is based on the article [Scaling a Mature Data Pipeline](https://medium.com/airbnb-engineering/scaling-a-mature-data-pipeline-managing-overhead-f34835cbc866)
 and can be used to manage scheduling overhead.

## Commands
Setup virtual environment:
- `pyenv local 3.6.x` to use a correct python version
- `python -m venv venv` to create a virtual environment
- `source ./venv/bin/activate` to activate the virtual environment
- `pip install pip-tools` to install pip tools

Tasks:
- `pip install -r requirements.txt` to install dependencies
- `pip install -r dev-requirements.txt` to install development dependencies
- `pip install -e .` to install the project in editable mode
- `python -m pytest --cov=src tests` runs all the tests and check coverage
- `python -m black dags src tests --check` checks PEP8 compliance issues
- `python -m black dags src tests` fixes PEP8 compliance issues