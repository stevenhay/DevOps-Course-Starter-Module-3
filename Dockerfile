FROM python:3.9-buster as base
EXPOSE 5000

# WORKDIR creates the directory if it doesn't exist
WORKDIR /app/
COPY . .

RUN pip install poetry && poetry install --no-root --no-dev

ENTRYPOINT ["/bin/bash", "-c", "./start.sh"]

# simply set env
FROM base as dev
ENV FLASK_ENV=development

FROM base as prod
ENV FLASK_ENV=production
