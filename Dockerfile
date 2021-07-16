FROM python:3.9-buster as base
EXPOSE 5000

# WORKDIR creates the directory if it doesn't exist
WORKDIR /app/
COPY . .

ENTRYPOINT ["/bin/bash", "-c", "./start.sh"]

# simply set env
FROM base as dev
ENV FLASK_ENV=development
RUN pip install poetry && poetry install --no-root

FROM base as prod
ENV FLASK_ENV=production
RUN pip install poetry && poetry install --no-root --no-dev

FROM base as test
ENV FLASK_ENV=test
RUN pip install poetry && poetry install --no-root
RUN apt-get update
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && apt-get install ./chrome.deb -y && rm ./chrome.deb
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` &&\
 echo "Installing chromium webdriver version ${LATEST}" &&\
 curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip &&\
 apt-get install unzip -y &&\
 unzip ./chromedriver_linux64.zip
ENTRYPOINT ["poetry", "run", "pytest"]
