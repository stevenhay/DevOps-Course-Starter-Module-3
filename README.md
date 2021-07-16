# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.tempalate` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

### Docker

To run the tests:

```bash
$ docker build --target test --tag todo-app:test .
$ docker run todo-app:test test
$ docker run -e TRELLO_API_KEY -e TRELLO_API_SECRET todo-app:test e2e_test
```

To build the docker image for development:

```bash
$ docker build --target dev --tag todo-app:dev .
```

Or production:

```bash
$ docker build --target prod --tag todo-app:prod .
```

Start the application on port 5000 using docker for development:

```bash
$ docker run --env-file ./.env.dev --mount type=bind,source="$(pwd)"/todo_app,target=/app/todo_app -p 5000:5000 todo-app:dev
```

Or production (using gunicorn):

```bash
$ docker run --env-file ./.env -p 5000:5000 todo-app:prod
```

NOTE: if using docker, you may wish to remove the FLASK_ENV variable within the .env file as it will overwrite the ones within the docker file if left.

### Vagrant

Start the application using vagrant by running:

```bash
$ vagrant up
```

### Poetry

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.
