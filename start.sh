#!/bin/bash

if [ "$FLASK_ENV" = "development" ]; then
    echo "Starting app in DEVELOPMENT mode";
    poetry run flask run --host "0.0.0.0"
elif [ "$FLASK_ENV" = "production" ]; then
    echo "Starting app in PRODUCTION mode";
    poetry run gunicorn "todo_app.app:create_app()" --bind "0.0.0.0:5000"
else
    echo "Unknown FLASK_ENV mode; quitting.";
fi
