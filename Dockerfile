FROM python:3.8.12-slim-buster

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN python3.8 -m nltk.downloader punkt

COPY . .

EXPOSE 8000

CMD python3.8 app.py

