#!/bin/bash

echo "Starting app in $FLASK_ENV mode"
if [ "$FLASK_ENV" = "development" ]; then
    poetry run flask run --host "0.0.0.0"
elif [ "$FLASK_ENV" = "production" ]; then
    poetry run gunicorn "todo_app.app:create_app()" --bind "0.0.0.0:5000"
else
    echo "Unknown FLASK_ENV mode: $FLASK_ENV; quitting.";
fi
